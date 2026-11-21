"""Recreate ROOT V126 synthetic artifacts and diagnostics.
No external observational files are used. Time-independent toy sources only.
"""
from __future__ import annotations
from pathlib import Path
import csv,json,sys
import numpy as np
from v126_core import *

if '--verify-only' in sys.argv:
    # Fast numerical reproducibility gate. Full plotting and Monte Carlo
    # remain independently runnable with: python scripts/run_v126.py
    root=Path(__file__).resolve().parents[1]
    result=json.loads((root/'results/v126_summary_SYNTHETIC.json').read_text(encoding='utf-8'))
    src,amp,centre=sim_multi_center_geometry()
    fn=lambda x:point_trace(x,src,amp,ELL)
    rr=[50e3,150e3,250e3,350e3]
    means=[shell_average(fn,centre,r) for r in rr]
    e0=inverse_three_shells(*rr[:3],*means[:3])
    e1=inverse_three_shells(*rr[1:],*means[1:])
    weak=weak_k_squared(fn,centre,150e3,radial_count=26,theta=12,phi=24)
    assert abs(e0-ELL)<1e-3 and abs(e1-ELL)<1e-3
    assert abs(weak*ELL**2-1)<1e-5
    assert result['real_satellite_data_fitted'] is False
    assert result['physical_four_force_unification_proved'] is False
    assert len(result['noise'])==5
    assert np.allclose(result['single_shell_windows_ell_km'],[e0/1000,e1/1000],atol=1e-6)
    print('V126_CORE_NUMERIC_OK two three-shell inversions + 3-D weak test + results metadata')
    sys.exit(0)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
(RESULTS:=ROOT/'results').mkdir(exist_ok=True)
(FIGS:=ROOT/'figures').mkdir(exist_ok=True)
sources,strengths,center=sim_multi_center_geometry()
single=lambda pts:point_trace(pts,sources,strengths,ELL)
second_ell=300e3
secondary=lambda pts:point_trace(pts,sources,strengths,second_ell)
secondary_factor=float(single(center)/secondary(center))
double=lambda pts:single(pts)+secondary_factor*secondary(pts)
trace_c=float(single(center))
dirs,weights=sphere_quadrature(32,64)
radii=np.array([0,30,50,100,130,150,200,230,250,300,350])*1000.
rows=[]
for r in radii:
    m1=shell_average(single,center,r,dirs,weights)
    m2=shell_average(double,center,r,dirs,weights)
    pred=trace_c*float(sinhc(r/ELL))
    rows.append({'shell_radius_km':r/1000,'single_mean_E':m1/1e-9,
       'single_analytic_E':pred/1e-9,'relative_quadrature_error':(m1-pred)/pred,
       'mixed_mean_E':m2/1e-9,'single_normalized':m1/trace_c,
       'mixed_normalized':m2/float(double(center))})
with (RESULTS/'shell_mean_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)

ra=np.array([50e3,150e3,250e3,350e3])
m_single=np.array([shell_average(single,center,x,dirs,weights) for x in ra])
m_mix=np.array([shell_average(double,center,x,dirs,weights) for x in ra])
window_single=[inverse_three_shells(*ra[i:i+3],*m_single[i:i+3])/1000 for i in [0,1]]
window_mixed=[inverse_three_shells(*ra[i:i+3],*m_mix[i:i+3])/1000 for i in [0,1]]

# For 4 data points, regress unknown b + amplitude*sinhc(k*r) at every k.
# This is an overidentified test (4 equations, 3 fitted parameters).
def fit_three_parameter_shell_shape(radii_m, measurements):
    y=np.asarray(measurements,float)
    norm=float(np.median(np.abs(y)))
    yy=y/norm
    def solve_for_k(ell):
        S=np.asarray(sinhc(radii_m/ell))
        design=np.column_stack((S,np.ones(len(S))))
        coeff=np.linalg.lstsq(design,yy,rcond=None)[0]
        residual=yy-design@coeff
        return float(np.dot(residual,residual)),coeff,residual
    fit=minimize_scalar(lambda ell:solve_for_k(ell)[0],bounds=(40e3,600e3),method='bounded',options={'xatol':1e-7})
    rss,coeff,resid=solve_for_k(fit.x)
    return {'ell_fit_km':float(fit.x/1000),'amplitude_fit_over_normalization':float(coeff[0]),
        'common_bias_over_normalization':float(coeff[1]), 'relative_rms_residual':float(np.sqrt(rss/len(yy))),
        'relative_residuals':resid.tolist()}
fit_single=fit_three_parameter_shell_shape(ra,m_single)
fit_double=fit_three_parameter_shell_shape(ra,m_mix)

# Weak-form 3D compactly supported test, no T finite-difference at any point.
weak_ksq=weak_k_squared(single,center,150e3,radial_count=36,theta=16,phi=32)

# Noise on each SHELL MEAN. A common offset is shared across the three radii.
# This is a toy covariance model; no real sensor transfer function is assumed.
noise_summary=[]
rng=np.random.default_rng(20261121)
a,b,c=50e3,150e3,300e3
clean=np.array([shell_average(single,center,r,dirs,weights) for r in [a,b,c]])
noise_trials=2500
for sigma_fraction in (0,0.002,0.005,0.01,0.02):
    common=rng.normal(0,.5*trace_c,size=(noise_trials,1))
    err=rng.normal(0,sigma_fraction*trace_c,size=(noise_trials,3))
    observations=clean[None,:]+common+err
    two=[];three=[]
    for y in observations:
        try:
            v=inverse_two_shells(a,c,float(y[0]),float(y[2]))
            if np.isfinite(v) and 10e3<v<1e7:two.append(v/1000)
        except (ValueError,ZeroDivisionError):pass
        try:
            v=inverse_three_shells(a,b,c,*[float(x) for x in y])
            if np.isfinite(v) and 10e3<v<1e7:three.append(v/1000)
        except (ValueError,ZeroDivisionError):pass
    def summarize(x):
        return {'valid_fraction':len(x)/noise_trials,'q2p5_q50_q97p5_km':np.quantile(x,[.025,.5,.975]).tolist() if len(x) else None}
    noise_summary.append({'sigma_per_shell_mean_over_center_trace':sigma_fraction,
       'common_bias_sigma_over_center_trace':.5,'trials':noise_trials,
       'two_shell':summarize(two),'three_shell_common_bias_removed':summarize(three)})

# Synthetic sparse sampling quadrature error exercise.
quad=[]
for nt,np_ in ((4,8),(6,12),(8,16),(12,24),(16,32),(24,48),(32,64)):
    dirs1,w1=sphere_quadrature(nt,np_)
    m=shell_average(single,center,300e3,dirs1,w1)
    pred=trace_c*float(sinhc(300e3/ELL))
    quad.append({'theta_nodes':nt,'phi_nodes':np_,'samples':nt*np_,
       'relative_error_at_300km':abs(m/pred-1)})

# Finite measurement rank: y_i = θ S(k r_i)+b ; k parameter dimensionless x=k/k_ref.
def derivative_sinhc_x(rad):
    z=rad/ELL
    return (z*np.cosh(z)-np.sinh(z))/z if z else 0.
rank=[]
for rlist in ([50e3,300e3],[50e3,150e3,300e3],[50e3,150e3,250e3,350e3]):
    j=np.array([[float(sinhc(x/ELL)),1.,derivative_sinhc_x(x)] for x in rlist])
    sv=np.linalg.svd(j,compute_uv=False)
    rank.append({'number_of_shells':len(rlist),'parameters':3,'matrix_rank':int(np.linalg.matrix_rank(j)),
                 'nonzero_singular_values':sv.tolist(),'residual_degrees_of_freedom':max(0,len(rlist)-3)})

result={'study':'ROOT V126','status':'SYNTHETIC_MATHEMATICS_ONLY','source':'asymmetric point masses inside Earth toy geometry',
 'fixed_ell_km':ELL/1000,'center_altitude_km':float((np.linalg.norm(center)-EARTH_R)/1000),
 'center_trace_E':trace_c/1e-9,'test_sphere_radius_km':[float(x/1000) for x in ra],
 'single_shell_windows_ell_km':window_single,'mixed_shell_windows_ell_km':window_mixed,
 'mixed_second_ell_km':second_ell/1000,'mixed_source_strength_multiplier':secondary_factor,
 'weak_form_k2_m_minus2':float(weak_ksq),'weak_form_relative_error':float(weak_ksq*ELL**2-1),
 'single_4shell_fit':fit_single,'mixed_4shell_fit':fit_double,'noise':noise_summary,
 'quadrature':quad,'design_rank':rank,
 'real_satellite_data_fitted':False,'physical_four_force_unification_proved':False}
(RESULTS/'v126_summary_SYNTHETIC.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')

plt.figure(figsize=(8.4,4.7))
plt.plot(radii/1000,[r['single_normalized'] for r in rows],'o-',label='single k = 1/124.6 km')
plt.plot(radii/1000,[r['mixed_normalized'] for r in rows],'s-',label='mixed k = 1/124.6 & 1/300 km')
plt.xlabel('Radius of vacuum sampling sphere (km)');plt.ylabel('Mean trace / central trace')
plt.title('Modified Helmholtz spherical-mean law (SYNTHETIC)');plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(FIGS/'01_spherical_mean_single_and_mixed_SYNTHETIC.png',dpi=155);plt.close()

plt.figure(figsize=(8,4.5))
angles=np.linspace(0,2*np.pi,300)
q=center[None,:]+150e3*np.column_stack((np.cos(angles),np.sin(angles),np.zeros(len(angles))))
plt.plot(angles,point_trace(q,sources,strengths,ELL)/1e-9)
plt.axhline(float(shell_average(single,center,150e3))/1e-9,linestyle='--',label='full sphere mean (not a circle mean)')
plt.xlabel('Azimuth along an equatorial sampling circle (radians)');plt.ylabel('Trace (E)')
plt.title('Non-spherical source: trace depends on angle (SYNTHETIC)');plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(FIGS/'02_non_spherical_angular_variation_SYNTHETIC.png',dpi=155);plt.close()

plt.figure(figsize=(8.4,4.7))
pos=np.arange(2)
plt.plot(pos,window_single,'o-',label='single-range exact data')
plt.plot(pos,window_mixed,'s-',label='mixed-range exact data')
plt.xticks(pos,['r = 50,150,250 km','r = 150,250,350 km']);plt.ylabel('Inferred ell from 3 shells (km)')
plt.title('Four-shell holdout exposes mixed-scale drift (SYNTHETIC)');plt.legend();plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(FIGS/'03_four_shell_model_diagnostic_SYNTHETIC.png',dpi=155);plt.close()

plt.figure(figsize=(8.4,4.7))
sigs=[];a2=[];b2=[];a3=[];b3=[]
for item in noise_summary:
    sig=item['sigma_per_shell_mean_over_center_trace']*100
    if sig==0:continue
    sigs.append(sig)
    lo,mid,hi=item['two_shell']['q2p5_q50_q97p5_km']
    a2.append(mid);b2.append([mid-lo,hi-mid])
    lo,mid,hi=item['three_shell_common_bias_removed']['q2p5_q50_q97p5_km']
    a3.append(mid);b3.append([mid-lo,hi-mid])
plt.errorbar(np.arange(len(sigs))-.08,a2,yerr=np.array(b2).T,fmt='o',capsize=3,label='2 shells; biased by common offset')
plt.errorbar(np.arange(len(sigs))+.08,a3,yerr=np.array(b3).T,fmt='s',capsize=3,label='3 shells; common offset cancels')
plt.axhline(ELL/1000,linestyle='--',label='true 124.6 km')
plt.xticks(np.arange(len(sigs)),[f'{x:g}%' for x in sigs]);plt.xlabel('Independent noise / central trace (per shell mean)')
plt.ylabel('Inferred ell, median and 95% toy quantile (km)')
plt.title('Common calibration offset vs random noise (SYNTHETIC)');plt.legend(fontsize=8);plt.grid(alpha=.25);plt.tight_layout()
plt.savefig(FIGS/'04_bias_and_noise_SYNTHETIC.png',dpi=155);plt.close()

print(json.dumps({'new_ell_km':window_single,'mixed_ell_km':window_mixed,
       'weak_relative_error':result['weak_form_relative_error'],
       'four_shell_relative_residual':fit_double['relative_rms_residual'],
       'noise_summary':noise_summary,'rank':rank},indent=2))
