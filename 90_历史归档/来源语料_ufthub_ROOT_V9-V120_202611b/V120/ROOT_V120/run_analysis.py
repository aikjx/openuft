"""Run deterministic, local-only V120 synthetic verification; write CSV/JSON/figures.

All values labelled as model predictions or Monte Carlo simulations.
"""
import csv
import json
from pathlib import Path
from math import pi,log,sqrt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from rootv120 import (
 R_EARTH,MU_EARTH_REF,C_LIGHT,ELL_PRE_REGISTERED,ALPHA_PRE_REGISTERED,
 ground_fraction,relative_yukawa,apparent_gm,two_range_gm,finite_spectrum,
 near_circular_precession_rad,extra_clock_shift,fit_profile_gls,fixed_hypothesis_gls,HBAR,E_CHARGE)

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
ell=ELL_PRE_REGISTERED; de=50000.; eps0=ground_fraction()
h=np.arange(6)*de
ks=apparent_gm(h,ell,epsilon_ground=eps0)
kd=two_range_gm(h,ell,300000.,epsilon_ground=eps0)
s1=finite_spectrum(ks,de);s2=finite_spectrum(kd,de)

with (OUT/'six_heights.csv').open('w',newline='',encoding='utf8') as f:
    wr=csv.writer(f)
    wr.writerow(['height_km','single_K_over_muinf','dual_K_over_muinf','difference'])
    for x,a,b in zip(h/1000,ks,kd):wr.writerow([f'{x:.0f}',f'{a:.15f}',f'{b:.15f}',f'{b-a:.15f}'])
with (OUT/'altitude_predictions.csv').open('w',newline='',encoding='utf8') as f:
    wr=csv.writer(f)
    wr.writerow(['height_km','yukawa_g_ratio','delta_g_m_s2','delta_K_over_muinf'])
    for km in [0,100,200,300,400,500,1000,5900]:
        frac=float(eps0*relative_yukawa(km*1000,ell))
        delta_g=float(frac*MU_EARTH_REF/(R_EARTH+1000*km)**2)
        wr.writerow([km,frac,delta_g,frac])

# Noiseless physical falsification: fit single range to dual range training data
train=np.array([0.,100000.,200000.]);hold=300000.
ytrain=two_range_gm(train,ell,300000.,epsilon_ground=eps0)
def triple_res(ell_try):
    x=relative_yukawa(train,ell_try)
    ratio=(ytrain[0]-ytrain[1])/(ytrain[1]-ytrain[2])
    return (x[0]-x[1])/(x[1]-x[2])-ratio
ellfit=brentq(triple_res,30000.,1000000.)
f=relative_yukawa(train,ellfit)
cc=(ytrain[0]-ytrain[1])/(f[0]-f[1]); aa=ytrain[0]-cc*f[0]
holdpred=aa+cc*float(relative_yukawa(hold,ellfit))
holdtrue=float(two_range_gm(np.array([hold]),ell,300000.,epsilon_ground=eps0)[0])

# Monte Carlo measurement model: each measured K / mu_inf receives independent
# Gaussian noise (not derived from real tracking or geoid datasets).
rng=np.random.default_rng(20261120)
noise_trials=12000
noise_records=[]
base=ks
for sigma in [0.,1e-9,1e-8,1e-7]:
    Y=base+rng.normal(0.,sigma,size=(noise_trials,len(base)))
    D=np.diff(Y,axis=1)
    H=D[:,:-2]*D[:,2:]-D[:,1:-1]**2
    J=D[:,0]*D[:,3]-D[:,1]*D[:,2]
    with np.errstate(divide='ignore',invalid='ignore'):
        q5=J/(2*H[:,0])
        q6=np.sqrt(H[:,1]/H[:,0])
        ell5=np.where((q5>0)&(q5<1),-de/np.log(q5),np.nan)
        ell6=np.where((q6>0)&(q6<1),-de/np.log(q6),np.nan)
    valid5=np.isfinite(ell5)
    valid6=np.isfinite(ell6)
    h0_positive=float((H[:,0]>0).mean())
    all_h_checks=((H[:,0]<H[:,1])&(H[:,1]<H[:,2])&(H[:,2]<0))
    # H0<H1<H2<0 is equivalent to all 3 negatives and both ratios in (0,1).
    r={
      'sigma_K_per_mu_inf':sigma,'trials':noise_trials,
      'H0_wrong_positive_fraction':h0_positive,
      'all_3_H_negative_increasing_fraction':float(all_h_checks.mean()),
      'five_height_valid_q_fraction':float(valid5.mean()),
      'six_height_valid_q_fraction':float(valid6.mean()),
      'five_height_ell_km_median_if_valid':float(np.nanmedian(ell5)/1000) if valid5.any() else None,
      'six_height_ell_km_median_if_valid':float(np.nanmedian(ell6)/1000) if valid6.any() else None
    }
    noise_records.append(r)
with (OUT/'noise_monte_carlo.csv').open('w',newline='',encoding='utf8') as ff:
    w=csv.DictWriter(ff,fieldnames=noise_records[0].keys());w.writeheader();w.writerows(noise_records)

# 3-height ratio estimator (0,100,200 km), independent Gaussian noise.
trial3=2500
points=np.array([0.,100000.,200000.])
true3=apparent_gm(points,ell,epsilon_ground=eps0)
observed=true3+rng.normal(0.,1e-7,(trial3,3))
three_est=[]
for row in observed:
    ratio=(row[0]-row[1])/(row[1]-row[2])
    def eq(L):
        x=relative_yukawa(points,L)
        return (x[0]-x[1])/(x[1]-x[2])-ratio
    lo,hi=10000.,1000000.
    try:
        if eq(lo)*eq(hi)<0:
            three_est.append(brentq(eq,lo,hi)/1000.)
        else:
            three_est.append(float('nan'))
    except (ValueError,OverflowError):
        three_est.append(float('nan'))
three_est=np.asarray(three_est)
valid3=three_est[np.isfinite(three_est)]

# GLS example with diagonal errors (no actual orbit observations).
h7=np.arange(7)*50000.
clean7=apparent_gm(h7,ell,epsilon_ground=eps0)
fit_clean=fit_profile_gls(clean7,h7)
sim_noise=rng.normal(0.,1e-7,len(h7))
fit_noisy=fit_profile_gls(clean7+sim_noise,h7,cov=(1e-7)**2*np.eye(len(h7)))

pre=near_circular_precession_rad(400000.,ell,eps0)
shift=extra_clock_shift(0.,400000.,ell,eps0)
metrics={
  'label':'MODEL-ONLY, NOT OBSERVATIONAL VALIDATION',
  'seed':20261120,'Earth_radius_m':R_EARTH,
  'lambda_m':ell,'alpha_yukawa':ALPHA_PRE_REGISTERED,
  'epsilon_ground_improved':eps0,
  'epsilon_ground_uniform':ground_fraction(model='uniform'),
  'quadratic_fR_a_m2':ell**2/6,
  'scalar_mass_energy_eV':HBAR*C_LIGHT/(ell*E_CHARGE),
  'single':{'H0':float(s1.H[0]),'H1_over_H0':float(s1.H[1]/s1.H[0]),
             'q_five':s1.q_five,'lambda_five_km':s1.ell_five_m/1000.,
             'lambda_six_km':s1.ell_six_m/1000.,
             'H0_negative':bool(s1.H[0]<0),
             'yukawa_shape_residual_float64':s1.yukawa_shape_residual},
  'dual':{'H0':float(s2.H[0]),'H0_positive':bool(s2.H[0]>0),
          'three_height_false_lambda_km':ellfit/1000.,
          'heldout_300km_abs_K_over_muinf':abs(holdpred-holdtrue)},
  'orbit_400km':{'delta_acceleration_m_s2':float(eps0*relative_yukawa(400000,ell)*MU_EARTH_REF/(R_EARTH+400000)**2),
                 'periapsis_precession_rad_per_radial_cycle':pre,
                 'precession_degrees':pre*180/pi},
  'clock_ground_400km':{'fractional_extra_gravitational_redshift':shift},
  'noise_monte_carlo':noise_records,
  'three_height_monte_carlo':{'sigma':1e-7,'trials':trial3,
    'valid_count':int(len(valid3)), 'quantile_2p5_km':float(np.quantile(valid3,.025)),
    'median_km':float(np.median(valid3)), 'quantile_97p5_km':float(np.quantile(valid3,.975))},
  'profile_gls_clean':fit_clean,
  'profile_gls_one_noise_realization':fit_noisy,
  'fixed_candidate_vs_GR_synthetic':fixed_hypothesis_gls(ks,h,1e-14*np.eye(len(h)))
}
with (OUT/'metrics.json').open('w',encoding='utf8') as f: json.dump(metrics,f,indent=2,ensure_ascii=False)

heights=np.linspace(0,1000,400)
ratios=eps0*relative_yukawa(heights*1000,ell)
fig,ax=plt.subplots(figsize=(8,4.4))
ax.semilogy(heights,ratios,linewidth=2,label='pre-registered single Yukawa')
ax.set(xlabel='Altitude above Earth (km)',ylabel='Predicted delta g / g_Newton',
       title='Hypothesis only: alpha=1/3, range=124.6 km')
ax.grid(True,alpha=.3);ax.legend();fig.tight_layout()
fig.savefig(FIG/'yukawa_altitude_prediction.png',dpi=170)
plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.4))
xs=[max(1e-12,r['sigma_K_per_mu_inf']) for r in noise_records[1:]]
ax.semilogx(xs,[r['H0_wrong_positive_fraction']*100 for r in noise_records[1:]],marker='o',label='false positive H0 sign')
ax.semilogx(xs,[r['all_3_H_negative_increasing_fraction']*100 for r in noise_records[1:]],marker='s',label='all three H signs and ratios pass')
ax.set(xlabel='Independent Gaussian sigma in apparent GM / true GM',ylabel='Fraction of trials (%)',
       title='Synthetic MC: raw Hankel tests are noise fragile',ylim=(0,105))
ax.legend();ax.grid(True,alpha=.3);fig.tight_layout()
fig.savefig(FIG/'hankel_noise_stress.png',dpi=170)
plt.close(fig)
print(json.dumps(metrics,ensure_ascii=False,indent=2))
