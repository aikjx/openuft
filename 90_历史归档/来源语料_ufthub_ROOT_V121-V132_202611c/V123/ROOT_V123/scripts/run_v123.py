"""Generate auditable ROOT V123 outputs; synthetic only."""
import json, csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootv120 import R_EARTH,ELL_PRE_REGISTERED,ground_fraction
from rootv122 import epsilon
from rootv123 import (synthetic_three,invert_three_heights,synthetic_mc,
    compare_synthetic_single_double,orbit_comparison,adjacent_difference_ratio,
    inverse_condition_number,amplitude_sign_and_fixed_alpha_test)

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'results'; FIG=ROOT/'figures'
RES.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
step=100_000.;r=R_EARTH
three=synthetic_three(r,step,ELL_PRE_REGISTERED,ground_fraction())
fit=invert_three_heights(three,r,step)
noise_levels=(1e-9,1e-8,1e-7,1e-6)
monte=[synthetic_mc(n=2500,noise_sigma=s,seed=20261121+i)
       for i,s in enumerate(noise_levels)]
shared=synthetic_mc(n=2500,noise_sigma=1e-7,shared_sigma=1e-5,seed=20261121)
lin=inverse_condition_number(three,r,step,np.eye(3)*1e-14)
dual=compare_synthetic_single_double()
orbit=orbit_comparison()
heights_fixed=np.arange(6,dtype=float)*50_000.
fakes={}
for label,amp in [('fixed',ground_fraction()),
                  ('wrong_coupling_quarter',ground_fraction()/4),
                  ('repulsive',-ground_fraction())]:
    fake_y=1+amp*__import__('rootv120').relative_yukawa(heights_fixed,ELL_PRE_REGISTERED)
    fakes[label]=amplitude_sign_and_fixed_alpha_test(fake_y,heights_fixed)
allout={
  'scope':'SYNTHETIC model-internal mathematics; no satellite observations ingested',
  'hypothesis':{'ell_m':ELL_PRE_REGISTERED,'alpha_yukawa':1/3,
    'ground_epsilon':ground_fraction(),'density':'Fayet 2026 approximate spherical analytic model'},
  'three_height_fixed_candidate':fit,
  'Kovermu_three_height_synthetic':three.tolist(),
  'linear_error_propagation_independent_1e-7':lin,
  'monte_carlo':monte,'monte_carlo_shared_additive':shared,
  'single_double_windows':dual,'orbit_comparison':orbit,
  'three_layer_amplitude_counterexamples':fakes,
  'data_provenance':{'real_observations_used':False,'GLS_real_orbit_completed':False}
}
(RES/'summary.json').write_text(json.dumps(allout,indent=2,ensure_ascii=False),encoding='utf-8')
with (RES/'window_inversion_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['window_start_km','single_range_inferred_km','double_range_inferred_km'])
    for i,(a,b) in enumerate(zip(dual['single_ell_windows_m'],dual['double_ell_windows_m'])):
        w.writerow([dual['heights_km'][i],a/1000,b/1000])
with (RES/'noise_mc_SYNTHETIC.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['sigma_K_div_mu','valid_n','invalid_n','p2.5_ell_m','median_ell_m','p97.5_ell_m'])
    for row in monte:
        w.writerow([row['noise_sigma_independent'],row['accepted'],row['invalid'],*(row['p2_5_p50_p97_5_m'] or [None]*3)])

# Figure: monotonic Q(k) (model identity, not observation)
ells=np.linspace(50e3,450e3,500)
q=[adjacent_difference_ratio(1/x,r,step) for x in ells]
plt.figure(figsize=(7.5,4.5));plt.plot(ells/1000,q)
plt.axvline(ELL_PRE_REGISTERED/1e3,linestyle='--',label='pre-registered range')
plt.xlabel('Yukawa range (km)');plt.ylabel('Three-height difference ratio Q')
plt.title('Exact monotone relation (synthetic geometry)');plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(FIG/'ratio_vs_range.png',dpi=160);plt.close()

# Figure: distinct spectra with same surface anomaly, synthetic demonstration
x=np.array(dual['heights_km'])
plt.figure(figsize=(7.5,4.5))
plt.plot(x,dual['single_values'],marker='o',label='one range 124.6 km')
plt.plot(x,dual['double_values'],marker='x',label='equal surface anomalies: 124.6 and 300 km')
plt.xlabel('Height above spherical reference (km)');plt.ylabel('K / GM∞')
plt.title('Synthetic observable: not actual satellite measurements')
plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(FIG/'single_double_K.png',dpi=160);plt.close()

plt.figure(figsize=(7.5,4.5))
plt.plot(x[:len(dual['single_ell_windows_m'])],np.array(dual['single_ell_windows_m'])/1000,
         marker='o',label='single range')
plt.plot(x[:len(dual['double_ell_windows_m'])],np.array(dual['double_ell_windows_m'])/1000,
         marker='x',label='double range (spurious effective range)')
plt.xlabel('Three-height window start (km)');plt.ylabel('Inferred Yukawa range (km)')
plt.title('Window stability discriminates synthetic multi-range mixtures')
plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(FIG/'sliding_window_ranges.png',dpi=160);plt.close()

plt.figure(figsize=(7.5,4.5))
p=[r['p2_5_p50_p97_5_m'] for r in monte]
xs=np.array(noise_levels)
med=np.array([a[1] if a is not None else np.nan for a in p])/1000
lo=np.array([a[0] if a is not None else np.nan for a in p])/1000
hi=np.array([a[2] if a is not None else np.nan for a in p])/1000
plt.errorbar(xs,med,yerr=[med-lo,hi-med],marker='o',capsize=3)
plt.axhline(ELL_PRE_REGISTERED/1000,linestyle='--',label='truth')
plt.xscale('log');plt.xlabel('Independent 1σ noise on K / GM∞')
plt.ylabel('Recovered range with 95% MC quantiles (km)')
plt.title('2,500 Monte-Carlo trials per noise level (synthetic)')
plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(FIG/'three_height_noise.png',dpi=160);plt.close()
print(json.dumps({
 'Q':fit['Q'],'ell_m':fit['ell_m'],
 'ell_bounds_m':[fit['ell_lower'],fit['ell_upper']],
 'sigma_ell_m_linear':lin['sigma_ell_m_linear'],
 'MC':[(m['noise_sigma_independent'],m['invalid'],m['p2_5_p50_p97_5_m']) for m in monte],
 'shared':shared,
 'two_range_windows_km':list(np.array(dual['double_ell_windows_m'])/1e3),
 'orbit':orbit,
 'three_layer_amplitude':fakes},indent=2))
