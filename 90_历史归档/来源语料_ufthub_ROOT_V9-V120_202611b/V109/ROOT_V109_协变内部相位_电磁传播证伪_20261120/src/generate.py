"""Generate reproducible figures and model-only numerical outputs, not experimental evidence."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .axion_em import Profile, exact_rotation, wkb_angle, observed_mode_proxies, constrained_bound, one_loop_identifiability
from .symbolic_audit import run_symbolic_checks
from .ledger_audit import build as build_ledger
ROOT=Path(__file__).resolve().parents[1]

def save_fig(filename):
    plt.tight_layout()
    plt.savefig(ROOT/'figures'/filename,dpi=170,bbox_inches='tight')
    plt.close()

def build_all():
    p=Profile(amplitude=.4,omega=.7)
    lam=.08;duration=5.
    ks=[5.,10.,20.,40.,80.,120.]
    out=[]
    for k in ks:
        r=exact_rotation(k,lam,p,duration)
        v=observed_mode_proxies(k,lam,p,duration)
        out.append({'k':k,**r,**v,'relative_wkb_error':abs(r['angle']-r['wkb'])/max(abs(r['wkb']),1e-40)})
    with (ROOT/'results'/'polarization_scan_THEORY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)

    plt.figure(figsize=(8.8,4.8))
    plt.plot([x['k'] for x in out],[x['A_phase_axis'] for x in out],marker='o',label='full A-mode phase-axis')
    plt.plot([x['k'] for x in out],[x['E_phase_axis'] for x in out],marker='s',label='full E-mode phase-axis')
    plt.axhline(wkb_angle(lam,p,duration),linestyle='--',label='WKB endpoint')
    plt.xlabel('dimensionless photon wavenumber k');plt.ylabel('relative phase-axis angle (rad)')
    plt.title('ROOT V109 / ALP-like field: adiabatic convergence (THEORY)');plt.legend()
    save_fig('01_ADIABATIC_CONVERGENCE_THEORY.png')

    plt.figure(figsize=(8.8,4.8))
    plt.loglog([x['k'] for x in out],[abs(x['angle']-x['wkb']) for x in out],marker='o',label='|full - WKB|')
    plt.loglog([x['k'] for x in out],[.00065/x['k']**2 for x in out],linestyle='--',label='illustrative 1/k² trend')
    plt.xlabel('wavenumber k');plt.ylabel('absolute error (rad)')
    plt.title('Convergence is conditional, not exact (THEORY)');plt.legend()
    save_fig('02_WKB_ERROR_THEORY.png')

    bad=exact_rotation(.8,.35,Profile(amplitude=1.,omega=1.),2.5)
    cycle=exact_rotation(1.,.3,Profile(amplitude=1.,omega=1.),2*np.pi)
    plt.figure(figsize=(8.8,4.8))
    kinds=['slow wave', 'full phase cycle']
    num=[bad['angle'],cycle['angle']]
    approximation=[bad['wkb'],cycle['wkb']]
    x=np.arange(2)
    plt.bar(x-.18,num,.36,label='full-mode phase proxy')
    plt.bar(x+.18,approximation,.36,label='endpoint WKB (invalid here)')
    plt.xticks(x,kinds);plt.ylabel('angle (rad)');plt.title('Nonadiabatic counterexamples (THEORY)');plt.legend()
    save_fig('03_NONADIABATIC_COUNTEREXAMPLE_THEORY.png')

    delta=np.linspace(.04,1.0,100)
    sigmas=[1e-4,5e-4,1e-3]
    plt.figure(figsize=(8.8,4.8))
    for s in sigmas:
        plt.plot(delta,[constrained_bound(s,d) for d in delta],label=f'1 sigma = {s} rad')
    plt.xlabel('independently known |Delta theta|');plt.ylabel('conditional 95% scale on |lambda|')
    plt.title('Illustrative idealized noise: not an observed exclusion (THEORY)');plt.legend()
    save_fig('04_CONDITIONAL_SENSITIVITY_THEORY.png')

    examples={'benchmark':{'profile_amplitude':.4,'profile_frequency':.7,'dimensionless_lambda':.08,'dimensionless_T':5.,'wkb_rotation_rad':wkb_angle(lam,p,duration),'full_at_k_80_rad':out[-2]['angle']},
              'nonadiabatic':{'k':.8,'lambda':.35,'theta_amplitude':1.,'theta_frequency':1.,'T':2.5,'full':bad,'interpretation':'endpoint formula not valid'},
              'returning_phase':{'k':1.,'lambda':.3,'theta_amplitude':1.,'theta_frequency':1.,'T':2*np.pi,'full':cycle,'interpretation':'WKB zero; finite-frequency phase proxy nonzero'}}
    (ROOT/'results'/'nonadiabatic_examples_THEORY.json').write_text(json.dumps(examples,indent=2,ensure_ascii=False),encoding='utf-8')
    sym=run_symbolic_checks()
    (ROOT/'results'/'symbolic_checks.json').write_text(json.dumps(sym,indent=2),encoding='utf-8')
    led=build_ledger()
    output={'version':'ROOT V109','date':'2026-11-20','unified_theory_proven':False,'new_experiment':False,'root_specific_prediction':False,
            'model_class':'existing axion-like electrodynamics; conditional helix-phase interpretation',
            'units':'hbar=c=1; dimensionless numerical scales and time for examples',
            'benchmark':examples['benchmark'],'scan':out,
            'single_measurement_identifiability':one_loop_identifiability(.08,-.14031329107584793),
            'adiabatic_breakdown':bad,'closed_phase_cycle':cycle,
            'symbolic_passed':sum(sym.values()),'symbolic_total':len(sym),'ledger_summary':led,
            'evidence_level':'mathematical and numerical model only',
            'sources':['https://arxiv.org/abs/2610.19049','https://journals.aps.org/prd/abstract/10.1103/rqcf-mv2r','https://link.springer.com/article/10.1140/epjc/s10052-024-13004-0']}
    (ROOT/'results'/'V109_AUDIT_RESULTS.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
    return output
if __name__=='__main__':
    o=build_all();print('results written, symbolic',o['symbolic_passed'],'of',o['symbolic_total'])
