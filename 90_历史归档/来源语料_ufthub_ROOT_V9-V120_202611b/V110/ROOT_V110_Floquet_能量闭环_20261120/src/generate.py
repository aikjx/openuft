"""Generate all V110 numerical benchmark artifacts (not observations)."""
from pathlib import Path
import sys, json, csv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.v110 import P,floquet,leading_mu,monodromy_scan,run_coupled,propagator
from src.symbolic_audit import checks

R=ROOT/'results';F=ROOT/'figures'
R.mkdir(exist_ok=True);F.mkdir(exist_ok=True)
p=P()
a=floquet(p,1);b=floquet(p,-1)
scan=monodromy_scan(n=161)
with (R/'floquet_scan_THEORY.csv').open('w',encoding='utf-8',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=list(scan[0]));w.writeheader();w.writerows(scan)
res=run_coupled(duration=180,nt=1401)
with (R/'backreaction_energy_THEORY.csv').open('w',encoding='utf-8',newline='') as fp:
    w=csv.writer(fp);w.writerow(['t','theta','theta_dot','A_plus','A_minus','E_theta','E_em','E_total'])
    for i,t in enumerate(res['t']):
        w.writerow([float(t),float(res['y'][0,i]),float(res['y'][1,i]),float(res['y'][2,i]),float(res['y'][4,i]),float(res['Etheta'][i]),float(res['Eem'][i]),float(res['Etotal'][i])])

plt.figure(figsize=(9,5));plt.plot([r['Omega'] for r in scan],[r['mu_plus'] for r in scan],label='h=+1 Floquet growth')
plt.plot([r['Omega'] for r in scan],[r['mu_minus'] for r in scan],ls='--',label='h=-1 Floquet growth')
plt.axvline(2.,c='gray',lw=1,ls=':');plt.xlabel('Driving frequency Omega / reference');plt.ylabel('mu / reference')
plt.title('ROOT V110 - Floquet instability (prescribed background)');plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(F/'01_FLOQUET_BAND_THEORY.png',dpi=160);plt.close()

plt.figure(figsize=(9,5));plt.plot(res['t'],res['Etheta'],label='Internal phase energy');plt.plot(res['t'],res['Eem'],label='Photon-mode energy')
plt.plot(res['t'],res['Etotal'],label='Total energy',lw=1.4,ls='--');plt.xlabel('Dimensionless time');plt.ylabel('Energy / reference')
plt.title('ROOT V110 - Coupled backreaction (finite-mode toy)');plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(F/'02_ENERGY_EXCHANGE_THEORY.png',dpi=160);plt.close()

plt.figure(figsize=(9,5));plt.plot(res['t'],(res['Etotal']-res['Etotal'][0])/res['Etotal'][0]);plt.xlabel('Dimensionless time');plt.ylabel('Relative total-energy residual')
plt.title('ROOT V110 - Conservation residual, DOP853');plt.grid(alpha=.2);plt.tight_layout();plt.savefig(F/'03_CONSERVATION_RESIDUAL_THEORY.png',dpi=160);plt.close()

# det/hel trace diagnostics across band
plt.figure(figsize=(9,5));plt.plot([r['Omega'] for r in scan],[r['trace_plus']-r['trace_minus'] for r in scan],label='trace(M+) - trace(M-)')
plt.xlabel('Driving frequency Omega');plt.ylabel('Difference (numerical only)');plt.title('ROOT V110 - Half-period symmetry diagnostic')
plt.grid(alpha=.2);plt.tight_layout();plt.savefig(F/'04_HELICITY_TRACE_RESIDUAL_THEORY.png',dpi=160);plt.close()

summary={
 'experiment':'theoretical/synthetic only; NOT experimental data',
 'conventions':'c=hbar=1, externally driven periodic pseudoscalar and finite-mode classical backreaction toy',
 'floquet_reference':{'k':p.k,'g':p.g,'theta0':p.theta0,'Omega':p.Omega,'trace_plus':a['trace'],
                      'trace_minus':b['trace'],'det_plus':a['det'],'det_minus':b['det'],
                      'mu_plus':a['mu'],'mu_minus':b['mu'],'leading_weak_coupling_mu':leading_mu(p),
                      'relative_mu_error':abs(a['mu']-leading_mu(p))/leading_mu(p)},
 'self_consistent_toy':{'max_relative_total_energy_drift':res['max_relative_energy_drift'],
                        'initial_total_energy':float(res['Etotal'][0]),
                        'max_photon_energy':float(np.max(res['Eem'])),
                        'min_theta_energy':float(np.min(res['Etheta'])),
                        'initial_photon_energy':float(res['Eem'][0]),
                        'initial_theta_energy':float(res['Etheta'][0]),
                        'photon_energy_gain_factor':float(np.max(res['Eem'])/res['Eem'][0]),
                        'time_range':[float(res['t'][0]),float(res['t'][-1])]},
 'scan':{'points':len(scan),'max_growth':max(z['mu_plus'] for z in scan),
         'freq_at_peak':max(scan,key=lambda z:z['mu_plus'])['Omega'],
         'max_trace_hel_diff':max(abs(z['trace_plus']-z['trace_minus']) for z in scan),
         'max_det_deviation':max(abs(z['det_plus']-1) for z in scan)},
 'symbolic_checks':checks(),
 'interpretation':'All numerical outputs are idealized theoretical model calculations; no evidence for new forces or quantum-gravity unification.'
}
(R/'V110_NUMERICAL_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'mu':a['mu'],'mu_weak':leading_mu(p),'energy_drift':res['max_relative_energy_drift'],'max_Eem':max(res['Eem']),'min_Etheta':min(res['Etheta']),'peak_Omega':summary['scan']['freq_at_peak'],'scan_n':len(scan)},indent=2))
