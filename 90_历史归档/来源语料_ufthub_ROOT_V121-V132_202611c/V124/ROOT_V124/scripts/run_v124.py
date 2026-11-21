"""Run independent V124 synthetic models and write machine-readable results + figures."""
from pathlib import Path
import sys,json,csv,hashlib
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from spectrum_v124 import *

BASE=Path(__file__).resolve().parents[1]
RES=BASE/'results'; FIG=BASE/'figures'
RES.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)

ell=ELL; r=R_EARTH; dd=50_000.
fixed_b=phi_earth_analytic()/3
samples=exact_K_decimal(r,dd,ell,B=str(fixed_b))
check=prony_five_decimal(samples,r,dd)
fake=prony_five_decimal(fake_prony_decimal(r,dd,ell),r,dd)
heights=np.array([0,50e3,100e3,200e3,250e3,400e3,500e3,1000e3])
rows=[]
for h,e,p in zip(heights,earth_profile(heights),point_source_profile(heights)):
    rows.append({'height_km':int(h/1000),'epsilon_earth':float(e),
                 'epsilon_point_source':float(p),'enhancement_ratio':float(e/p)})
with (RES/'earth_finite_size_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

m=[]
for h in np.arange(0,550000,50000):
    x=moments_at_height(h,[ell,300000],[.6,.4]);
    m.append({'height_km':h/1000,'ell_effective_km':x['ell_effective_m']/1000,
              'curvature':x['curvature'],'spectral_variance_k':x['variance_k']})
with (RES/'positive_mixture_moments_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=m[0].keys());w.writeheader();w.writerows(m)

noise={str(sig):spectral_mc(n=4000,noise=sig) for sig in [1e-4,1e-3,1e-2]}
prec=[]
for dig in [12,14,16,18,20,22,25,30,40]:
    with mp.workdps(115):
        dvalues=[mp.nstr(mp.mpf(s),dig) for s in samples]
    try:
        c=prony_five_decimal(dvalues,r,dd)
        prec.append({'significant_digits':dig,'ell_m':c['ell_m'],
                     'ell_error_m':c['ell_m']-ell,'shape_residual':c['shape_residual']})
    except ValueError as exc:
        prec.append({'significant_digits':dig,'error':str(exc)})

metric={'model':'SYNTHETIC static spherical linear unscreened Yukawa',
        'earth_analytic_form_factor':phi_earth_analytic(),
        'ell_m':ell,'alpha_Y':ALPHA_Y,
        'five_height_true':check, 'five_height_fake':fake,
        'geometry_rows':rows,'double_spectrum_moments':m,'noise_experiment':noise,
        'decimal_precision_experiment':prec,
        'test_status':'run pytest and verify_all.sh separately'}
(RES/'V124_summary.json').write_text(json.dumps(metric,ensure_ascii=False,indent=2),encoding='utf-8')

fig,ax=plt.subplots(figsize=(8.7,4.8))
ax.semilogy(heights/1000,earth_profile(heights),'o-',label='Finite-size Earth (analytic density)')
ax.semilogy(heights/1000,point_source_profile(heights),'s--',label='Point mass at Earth center (invalid approx)')
ax.set(xlabel='Height above idealized spherical Earth (km)',ylabel='Extra radial acceleration / Newtonian acceleration',title='Short-range Yukawa source-size correction (synthetic)')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/'earth_shape_factor_comparison.png',dpi=160);plt.close(fig)

hplot=np.linspace(0,500000,250)
single=ideal_F_at_height(hplot,[ell],[1])
double=ideal_F_at_height(hplot,[ell,300000],[.6,.4])
fig,ax=plt.subplots(figsize=(8.7,4.8))
ax.plot(hplot/1000,single,label='Single 124.6 km')
ax.plot(hplot/1000,double,label='Positive mixture: 124.6 & 300 km')
ax.set(xlabel='Height (km)',ylabel='Geometrically normalized derivative F(h) / F(0)',title='Laplace spectrum after removing radius factor')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/'F_laplace_profiles.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.7,4.8))
ax.plot([v['height_km'] for v in m],[v['ell_effective_km'] for v in m],marker='o')
ax.axhline(ell/1000,ls='--',label='Short component')
ax.axhline(300,ls='--',label='Long component')
ax.set(xlabel='Height (km)',ylabel='Effective local range (km)',title='Positive mixtures must drift toward longer range')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/'effective_range_monotonic_drift.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(figsize=(8.7,4.8))
labels=['0.01%','0.1%','1%'];sigs=[1e-4,1e-3,1e-2]
ax.plot(labels,[noise[str(s)]['single']['fraction_H_positive']*100 for s in sigs],marker='o',label='Single, false positive sign')
ax.plot(labels,[noise[str(s)]['double']['fraction_H_positive']*100 for s in sigs],marker='s',label='Double, positive sign')
ax.set(xlabel='Independent F noise / F(0)',ylabel='Fraction with H > 0 (%)',ylim=(0,105),title='Sign alone is not a statistical detection (4000 runs each)')
ax.grid(True,alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/'sign_noise_false_positive.png',dpi=160);plt.close(fig)

print(json.dumps({'earth_shape':metric['earth_analytic_form_factor'],
                  'earth_epsilon400':rows[5]['epsilon_earth'],
                  'true_reconstruction':check,
                  'fake_reconstruction':fake,
                  'noise':noise},ensure_ascii=False,indent=2))
