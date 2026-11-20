"""Generate auditable theoretical and SYNTHETIC data; no actual observations."""
import csv
import json
from pathlib import Path
import math
import sys
import numpy as np
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_v90 import *

def generate(root:Path):
    out=root/'results'; out.mkdir(exist_ok=True)
    fig=root/'figures'; fig.mkdir(exist_ok=True)
    dlist=[450e-6,600e-6,850e-6,1.25e-3]
    g1=Geometry(dlist[0]);g2=Geometry(dlist[1])
    benchmark=eft_phase_components(g1,1e-14,1e-14,1.)
    benchmark.update({'concurrence':pure_concurrence(benchmark['newton']),
        'equivalent_charge_C_not_physically_fractional':residual_charge_equivalent(1e-14,1e-14),
        'one_elementary_electric_charge_to_Newton_strength_ratio':K_E*E**2/(G*(1e-14)**2),
        'uniform_sphere_radius_m_at_3500_kg_m3':sphere_radius(1e-14,3500),
        'geometry_m':{'d':g1.d,'s_a':g1.s_a,'s_b':g1.s_b},
        'provenance':'THEORY, NOT OBSERVED',
        'caveat':'1PN and one-loop are coefficients from a potential convention, not apparatus gauge-invariant readouts'})
    (out/'v89_reproduction_benchmark.json').write_text(json.dumps(benchmark,ensure_ascii=False,indent=2),encoding='utf-8')
    scans=[]
    sig_even=1e-4 # sigma per already projected (even) phase at each distance, arbitrary scenario
    for lam in np.geomspace(1e-4,1.,121):
        lam=float(lam)
        delta=yukawa_kernel(g1,lam)-power_kernel(g1)
        projected=newton_nulled_signal(g1,g2,lam)
        sigma_s=sig_even*np.linalg.norm(newton_nulled_weights(g1,g2))
        ide=identifiability(dlist,g1.s_a,g1.s_b,lam)
        scans.append(dict(lambda_m=lam,F1_m_inv=power_kernel(g1),
            FYminusF1_m_inv=delta,
            relative_yukawa_shape=abs(delta/power_kernel(g1)),
            nulled_alpha_1_rad=projected,
            hypothetical_alpha_for_5sigma=5*sigma_s/abs(projected),
            hypothetical_sigma_even_rad=sig_even,
            shape_condition_number=ide['condition_number'],
            sv_min_to_max=ide['normalised_separation'],
            label='THEORY/SYNTHETIC, NOT EXPERIMENT'))
    with (out/'yukawa_identifiability_scan_THEORY.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=scans[0].keys());w.writeheader();w.writerows(scans)
    # independent arbitrary precision validation, avoid cancellation from floating point geometry
    mp.mp.dps=90
    d,a,b=map(mp.mpf,['0.00045','0.0002','0.0002'])
    rs=[d+(a-b)/2,d+(a+b)/2,d-(a+b)/2,d+(b-a)/2]
    signs=[1,-1,-1,1]
    comparisons=[]
    for lam_str in ['0.001','0.01','0.1','1','10']:
        l=mp.mpf(lam_str)
        F1=mp.fsum([sg/r for sg,r in zip(signs,rs)])
        FY=mp.fsum([sg*mp.exp(-r/l)/r for sg,r in zip(signs,rs)])
        delta_high=FY-F1
        # same physical decimal data, unrounded, independent direct exponential sums
        g=Geometry(float(d),float(a),float(b))
        delta_stable=yukawa_delta_series(g,float(l)) if float(l)>=5*max(g.distances()) else yukawa_kernel_naive(g,float(l))-power_kernel(g)
        comparisons.append(dict(lambda_m=lam_str,
            direct_mpmath_90digit_delta=str(delta_high),
            stable_double_delta=delta_stable,
            relative_error_vs_high_precision=float(abs(mp.mpf(str(delta_stable))-delta_high)/abs(delta_high))
            ))
    (out/'independent_precision_check.json').write_text(json.dumps({'precision_digits':90,'comparisons':comparisons,
       'claim':'Independent high-precision theoretical kernel arithmetic, not experimental precision.'},indent=2),encoding='utf-8')
    # Synthetic null: gaussian, sigma defined on even projected phase per point
    rng=np.random.default_rng(20261118)
    n=10_000
    w=newton_nulled_weights(g1,g2)
    synthetic=rng.normal(0.,sig_even,(n,2))@w/(sig_even*np.linalg.norm(w))
    null_results={'replicates':n,'noise_model':'SYNTHETIC independent Gaussian on 2 parity-even phase readings',
        'sigma_even_rad':sig_even,'z_mean':float(synthetic.mean()),
        'z_sd_sample':float(synthetic.std(ddof=1)),
        'fraction_abs_z_gt_3':float(np.mean(np.abs(synthetic)>3)),
        'not_real_experiment':True}
    (out/'synthetic_null_validation.json').write_text(json.dumps(null_results,indent=2),encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x=[r['lambda_m'] for r in scans]
    plt.figure(figsize=(7.5,4.8))
    plt.loglog(x,[r['relative_yukawa_shape'] for r in scans],label='|FY-F1| / |F1|')
    plt.xlabel('Yukawa range lambda (m)');plt.ylabel('Relative nonlocal shape')
    plt.title('ROOT V90: nonlocal Yukawa suppression (THEORY)')
    plt.grid(True);plt.legend();plt.tight_layout();plt.savefig(fig/'relative_yukawa_suppression.png',dpi=160);plt.close()
    plt.figure(figsize=(7.5,4.8))
    plt.loglog(x,[r['shape_condition_number'] for r in scans])
    plt.xlabel('Yukawa range lambda (m)');plt.ylabel('Condition number [F1, FY]')
    plt.title('ROOT V90: long-range shape degeneracy (THEORY)')
    plt.grid(True);plt.tight_layout();plt.savefig(fig/'parameter_identifiability.png',dpi=160);plt.close()
    plt.figure(figsize=(7.5,4.8))
    plt.loglog(x,[abs(r['nulled_alpha_1_rad']) for r in scans],label='|Newton-nulled phase|, alpha=1')
    plt.axhline(sig_even*np.linalg.norm(w),linestyle='--',label='1 sigma (hypothetical)')
    plt.xlabel('Yukawa range lambda (m)');plt.ylabel('Projected phase magnitude (rad)')
    plt.title('ROOT V90: illustrative precision scenario, NOT measurements')
    plt.grid(True);plt.legend();plt.tight_layout();plt.savefig(fig/'nulled_signal_vs_noise.png',dpi=160);plt.close()
    return {'benchmark':benchmark,'synthetic_null':null_results,'precision_checks':comparisons,
            'num_scan_points':len(scans),'output_figures':3}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(generate(root),ensure_ascii=False,indent=2))
