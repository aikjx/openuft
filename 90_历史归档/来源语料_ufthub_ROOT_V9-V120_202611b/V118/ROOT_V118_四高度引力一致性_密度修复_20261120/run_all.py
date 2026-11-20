"""Generate ROOT V118 reproducible synthetic experiments and figures.

All distances and outputs are model inputs, not observed gravity anomalies.
"""
import json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src import model as m
ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results';FIG=ROOT/'figures'
RESULTS.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
H=(0.,400e3,800e3,1200e3)
H_SAT=(300e3,500e3,700e3,900e3)
P=['uniform','inverse_r','earth_analytic','five_shell_reference']
base={p:{str(int(h/1e3))+'km':m.yukawa_excess(h,profile=p) for h in H} for p in P}
k1=[m.effective_gm(h) for h in H]
closure=m.four_altitude_validation(H,k1)
k2=[1+m.yukawa_excess(h)+m.yukawa_excess(h,300e3,.1) for h in H]
closure_bad=m.four_altitude_validation(H,k2)
ksat=[m.effective_gm(h) for h in H_SAT]
closure_sat=m.four_altitude_validation(H_SAT,ksat)
# 2500 synthetic 0.1 ppm independent instrument errors in K / (GM).
rng=np.random.default_rng(20261120)
noise_level=1e-7
noisy=[];inferred=[];failed=0
for i in range(2500):
    kn=np.array(k1)+rng.normal(0,noise_level,size=4)
    try:
        result=m.four_altitude_validation(H,kn.tolist())
        noisy.append(result['fractional_fourth_residual'])
        inferred.append(result['ell_m'])
    except ValueError:failed+=1
noisy=np.asarray(noisy);inferred=np.asarray(inferred)
# Relevant model degeneracies: alpha=0 -> K constant, differences cannot infer ell.
assert len(noisy)>2400
all_results={
 'metadata':{'research_version':'ROOT V118','date':'2026-11-20',
   'scientific_result':'conditional classical model calculations; four-force unification OPEN',
   'observation_status':'All K values and recovered anomalies are synthetic, NOT satellite observations'},
 'inputs':{'radius_m':m.R_EARTH,'ell_m':m.ELL_BASELINE,'alpha':m.ALPHA_BASELINE,
           'baselines_km':[h/1000 for h in H],
           'satellite_like_km':[h/1000 for h in H_SAT]},
 'density':base,
 'analytic_vs_five_shell_relative_error':
    (base['earth_analytic']['0km']/base['five_shell_reference']['0km']-1),
 'three_altitude_ratio':m.altitude_invariant(m.ELL_BASELINE,H[:3]),
 'single_scalar_four_altitude':closure,
 'single_scalar_satellite_like_four_altitude':closure_sat,
 'two_scalar_counterexample':{
       'second_range_m':300e3,'second_alpha':.1,
       'first_three_fitted_range_m':closure_bad['ell_m'],
       'out_of_sample_fractional_residual':closure_bad['fractional_fourth_residual']},
 'epicyclic':{str(int(h/1000))+'km':m.epicyclic_observables(h) for h in [0.,100e3,400e3,500e3,710e3,800e3,1200e3]},
 'synthetic_noise_experiment':{'random_seed':20261120,'draws':2500,'noise_1sigma_fractional_GM':noise_level,
       'successful_inversions':len(noisy),'rejected_outside_bracket':failed,
       'median_inferred_ell_m':float(np.median(inferred)),
       'ell_95_percentile_interval_m':[float(np.percentile(inferred,2.5)),float(np.percentile(inferred,97.5))],
       'heldout_residual_95_percentile_interval':[float(np.percentile(noisy,2.5)),float(np.percentile(noisy,97.5))]},
 'history':{'ledger_issues':396,'prior_version':'ROOT V117 original ZIP retained'},
 'five_key_OPEN':['derive G without measured input','derive SU(3)xSU(2)xU(1) and fermion reps',
    'quantum-gravity UV consistency','predict a genuinely exclusive observable',
    'independent experimental validation']
}
(RESULTS/'V118_RESULTS.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2),encoding='utf-8')
# Figure 1: correction from realistic Earth shape.
heights=np.linspace(0,1100e3,350)
plt.figure(figsize=(8,5))
for p in P:
    vals=np.array([m.yukawa_excess(h,profile=p) for h in heights]);
    plt.semilogy(heights/1000,100*vals,label=p)
plt.xlabel('Height above spherical Earth (km)');plt.ylabel('Yukawa / Newtonian force (%)')
plt.title('Source-density correction at range 124.6 km (synthetic)')
plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'01_density_correction.png',dpi=165);plt.close()
# Figure 2: 3-altitude ratio unique on displayed range, independent of Earth density.
ells=np.geomspace(40e3,1200e3,250)
ratios=[m.altitude_invariant(ell,H[:3]) for ell in ells]
plt.figure(figsize=(8,5));plt.loglog(ells/1000,ratios)
plt.axvline(m.ELL_BASELINE/1000,linestyle='--',label='V117 candidate range')
plt.xlabel('Yukawa range (km)');plt.ylabel('(K0-K400)/(K400-K800)')
plt.title('Three-altitude invariant: density & amplitude cancel')
plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'02_three_altitude_invariant.png',dpi=165);plt.close()
# Figure 3: false model's held-out fourth altitude.
plt.figure(figsize=(8,5))
x=[h/1000 for h in H]
plt.plot(x,k1,'o-',label='single Yukawa source (4th matches)')
plt.plot(x,k2,'s-',label='two range source truth')
plt.plot(x[-1],closure_bad['fourth_predicted'],'x',markersize=12,label='single-range 4th prediction (2-range input)')
plt.xlabel('Height (km)');plt.ylabel('Apparent GM / baseline GM')
plt.title('Out-of-sample check reveals missing second scalar')
plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'03_four_altitude_holdout.png',dpi=165);plt.close()
# Figure 4: radial pericentre precession near circular equatorial spherical orbit.
plt.figure(figsize=(8,5))
pres=[m.epicyclic_observables(h)['pericenter_advance_rad_per_radial_period']*180/math.pi
      for h in heights]
plt.semilogy(heights/1000,pres)
plt.xlabel('Circular orbit altitude above sphere (km)')
plt.ylabel('Extra apsidal advance (degrees / radial cycle)')
plt.title('Nearly circular orbit in the ideal spherical Yukawa test model')
plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'04_epicyclic_precession.png',dpi=165);plt.close()
# Figure 5: noise distribution synthetic only.
plt.figure(figsize=(8,5))
plt.hist(noisy*1e6,bins=45)
plt.xlabel('4th-altitude held-out residual (parts per million of baseline GM)')
plt.ylabel('Synthetic trials')
plt.title('Monte Carlo measurement-noise propagation (0.1 ppm K noise)')
plt.grid(alpha=.2);plt.tight_layout();plt.savefig(FIG/'05_synthetic_noise.png',dpi=165);plt.close()
print(json.dumps({'source_fraction_percent':100*base['earth_analytic']['0km'],
 'rhoprime_vs_5shell_percent':100*all_results['analytic_vs_five_shell_relative_error'],
 'three_altitude_invariant':all_results['three_altitude_ratio'],
 'two_range_4th_residual':closure_bad['fractional_fourth_residual'],
 'precession_400km_deg':all_results['epicyclic']['400km']['pericenter_advance_rad_per_radial_period']*180/math.pi,
 'noise_inversions':len(noisy),'history_items':396},ensure_ascii=False,indent=2))
