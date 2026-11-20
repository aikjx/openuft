from pathlib import Path
import sys, math, json, csv
from dataclasses import replace
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.quantum_gravity_audit import *
P=Config()
Ds=(450e-6,600e-6,850e-6)

def write_csv(fname,head,rows):
    with (ROOT/'data'/fname).open('w',newline='',encoding='utf-8-sig') as fh:
        w=csv.writer(fh);w.writerow(head);w.writerows(rows)

base=stats(P)
base['three_distance_filter']=null_projection(P,Ds)
base['decimal_90_digit_filter']=decimal_null_determinant(P,Ds)
base['identifiability_design_singular_values']=np.linalg.svd(two_coupling_design(P,Ds),compute_uv=False).tolist()
base['interpretation']={
 'Newton_entanglement':'conditional pure-state quantum two-body model, not observed',
 '1PN':'a conventional scattering-matched potential term, not a standalone gauge-invariant phase',
 'EFT_loop':'leading EFT long-range term, not a measured loop effect',
 'three_distance':'algebraic null filter overwhelmed by roundoff and experimental uncertainty',
 'classical_mediator':'local classical communication no-entanglement; general classical-field models contested'
}
(ROOT/'results/numerical_summary.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf8')

rs=np.geomspace(300e-6,3e-3,140)
scan=[]
for d in rs:
    p=replace(P,d=float(d))
    t=scale_terms(p)
    scan.append((d,t['newton'],abs(t['one_pn_potential']),abs(t['eft_loop_potential']),
                 t['pn_over_newton'],t['eft_over_newton'],pure_concurrence(phases(p))))
write_csv('distance_scan_SYNTHETIC.csv', ['d_m','phase_Newton_rad','abs_phase_1PN_rad','abs_phase_EFT_rad',
                 'relative_1PN','relative_EFT','ideal_concurrence'],scan)

ms=np.geomspace(1e-16,3e-12,115)
rows=[]
for m in ms:
    p=replace(P,m1=float(m),m2=float(m));u=scale_terms(p)
    rows.append((m,u['newton'],u['one_pn_potential'],u['eft_loop_potential'],pure_concurrence(phases(p))))
write_csv('mass_scan_SYNTHETIC.csv',['m1_m2_kg','phase_N_rad','phase_1PN_rad','phase_EFT_rad','C_ideal'],rows)

gammas=np.linspace(0,0.11,140)
rows=[]
for gamma in gammas:
    p=replace(P,gamma1=float(gamma),gamma2=float(gamma))
    rows.append((gamma,negativity(rho_dephased(p))))
write_csv('dephasing_scan_SYNTHETIC.csv',['gamma_per_s','negativity'],rows)

charge_ratios=np.linspace(-2,2,161)
rows=[];q0=q_equivalent(P)
for k in charge_ratios:
    p=replace(P,q1=q0,q2=q0*float(k))
    rows.append((k,cross(phases(p)),pure_concurrence(phases(p))))
write_csv('charge_degeneracy_SYNTHETIC.csv',['q2_over_q_equal','phase_total_rad','C_ideal'],rows)

# Calibrated synthetic readings: noise orders of magnitude > EFT correction.
# Never interpret as measured signal.
rng=np.random.default_rng(20261118)
sigma=1e-3
rows=[]
for d in Ds:
    pp=replace(P,d=d)
    true=cross(phases(pp))
    for i in range(30):
        rows.append((d,i,true,true+float(rng.normal(scale=sigma)),sigma,'SYNTHETIC'))
write_csv('mock_observations_SYNTHETIC.csv',['d_m','trial','Newt_phase_rad','synthetic_observed_rad','sigma_rad','label'],rows)

plt.figure(figsize=(8,5))
plt.plot(np.asarray(scan)[:,0]*1e6,np.asarray(scan)[:,1],label='Newtonian nonlocal phase')
plt.xlabel('Center separation d (micrometers)');plt.ylabel('Nonlocal phase (rad)')
plt.title('ROOT V89: frozen-path phase vs distance (model)');plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(ROOT/'results/distance_phase.png',dpi=170);plt.close()
plt.figure(figsize=(8,5))
plt.plot(gammas,[x[1] for x in rows[:0]] if False else [negativity(rho_dephased(replace(P,gamma1=float(g),gamma2=float(g)))) for g in gammas])
plt.xlabel('Local dephasing gamma (1/s)');plt.ylabel('Negativity')
plt.title('ROOT V89: entanglement vs decoherence (model)');plt.grid(alpha=.3);plt.tight_layout()
plt.savefig(ROOT/'results/decoherence.png',dpi=170);plt.close()
plt.figure(figsize=(8,5))
arr=np.asarray(scan)
plt.loglog(arr[:,0]*1e6,abs(arr[:,4]),label='Representative 1PN / Newton phase')
plt.loglog(arr[:,0]*1e6,abs(arr[:,5]),label='EFT loop / Newton phase')
plt.xlabel('Center separation d (micrometers)');plt.ylabel('Absolute ratio')
plt.title('ROOT V89: many orders of magnitude separate regimes')
plt.grid(alpha=.3);plt.legend();plt.tight_layout()
plt.savefig(ROOT/'results/PN_EFT_ratios.png',dpi=170);plt.close()
plt.figure(figsize=(8,5))
charge=np.asarray([(k,cross(phases(replace(P,q1=q0,q2=q0*float(k))))) for k in charge_ratios])
plt.plot(charge[:,0],charge[:,1])
plt.axhline(0,ls='--');plt.xlabel('q1*q2 / (q_equal^2)');plt.ylabel('Total nonlocal phase (rad)')
plt.title('ROOT V89: Coulomb-Newtown 1/r exact degeneracy (toy model)')
plt.grid(alpha=.3);plt.tight_layout()
plt.savefig(ROOT/'results/coulomb_false_positive.png',dpi=170);plt.close()
plt.figure(figsize=(8,5))
flt=base['three_distance_filter']
vals=[abs(flt['loop_projection_analytic']),abs(flt['naive_float_projection'])]
plt.bar(['EFT true term','double rounding artifact'],vals)
plt.yscale('log');plt.ylabel('Absolute filtered phase (rad)')
plt.title('ROOT V89: catastrophic cancellation in 3-distance null filter')
plt.tight_layout();plt.savefig(ROOT/'results/numerical_precision_trap.png',dpi=170);plt.close()

summary={'date':'2026-11-18','version':'V89','unit_tests':'run via pytest',
         'physics_status':'Existing low-energy mathematical models; no new quantum-gravity observation',
         'data_sources':['NIST CODATA G, h, c','toy model parameters','APS/Nature literature 2025-2026'],
         'data_is_synthetic':True,'datasets':5,'plots':5}
(ROOT/'results/dataset_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'phase_N':base['phase_terms']['newton'],'phase_1PN':base['phase_terms']['one_pn_potential'],
                  'phase_EFT':base['phase_terms']['eft_loop_potential'],'C_ideal':base['concurrence'],
                  'ratio_roundoff_to_EFT':flt['float_false_signal_ratio'],'csv_files':5,'png_files':5},ensure_ascii=False,indent=2))
