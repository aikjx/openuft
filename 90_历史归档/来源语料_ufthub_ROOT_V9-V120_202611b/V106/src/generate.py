"""Reproducible theory data + plots; no experiments or observations."""
from pathlib import Path
import json, csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .running import Benchmark,B,intersection,invariant,inverse_at,optimal_spread,benchmark_scan
from .anomaly import anomaly_coefficients,su5_normalization
from .geometry import X,Y,Z,matrix_holonomy,matrix_curvature_two_phase,su2_holonomy_small_loop_error

ROOT=Path(__file__).resolve().parents[1]
def run():
    (ROOT/'results').mkdir(exist_ok=True);(ROOT/'figures').mkdir(exist_ok=True)
    bench=Benchmark();inv=bench.inv_couplings()
    pairs={str(i+1)+str(j+1):intersection(i,j,bench) for i,j in [(0,1),(0,2),(1,2)]}
    summary={
      'evidence':'THEORY/MODEL/ONE_LOOP (NOT experimental finding)',
      'assumptions':'minimal SM one-loop; SU5-normalized alpha1; fixed illustrative MZ benchmark; no thresholds/no 2loops',
      'benchmark':vars(bench),'beta_coefficients':B.tolist(),'inverse_MZ':inv.tolist(),
      'pairwise':pairs,'one_loop_invariant':invariant(bench),'best_fit':optimal_spread(bench),
      'toy_input_scan':benchmark_scan(n=10001,seed=106),
      'anomaly_coefficients':{k:str(v) for k,v in anomaly_coefficients().items()},
      'su5_normalization':{k:str(v) for k,v in su5_normalization().items()},
      'SU2_Fxy_for_length_1m':[[[float(z.real),float(z.imag)] for z in row] for row in matrix_curvature_two_phase(1)],
      'holonomy_errors':{str(h):su2_holonomy_small_loop_error(h) for h in [.2,.1,.05,.025,.0125]},
      'decisive_limit':'no complete four-force unification; no prediction G; no experimental data'
    }
    (ROOT/'results'/'numerical_summary_THEORY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    t=np.linspace(0,40,401)
    rows=[(ti,bench.m_z_gev*math.exp(ti),*inverse_at(ti,bench)) for ti in t]
    with open(ROOT/'results'/'gauge_running_ONE_LOOP_THEORY.csv','w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['log_mu_over_MZ','mu_GeV','alpha1_inverse_SU5','alpha2_inverse','alpha3_inverse']);wr.writerows(rows)
    fig,ax=plt.subplots(figsize=(9,5.6)); col=['C0','C1','C2']
    for i in range(3):ax.plot(np.log10(bench.m_z_gev)+t/np.log(10),[r[i+2] for r in rows],label=f'alpha{i+1}^-1',color=col[i])
    ax.set_xlabel('log10(mu / GeV)');ax.set_ylabel('inverse gauge coupling (one-loop)');ax.set_title('Minimal SM: one-loop couplings do not meet exactly');ax.legend();ax.grid(alpha=.25)
    fig.tight_layout();fig.savefig(ROOT/'figures'/'01_ONE_LOOP_NONUNIFICATION_THEORY.png',dpi=165);plt.close(fig)
    hs=np.logspace(-2.7,-.4,55); errors=np.array([su2_holonomy_small_loop_error(float(h)) for h in hs])
    fig,ax=plt.subplots(figsize=(8,5));ax.loglog(hs,errors,'o-',ms=2,label='||W-(I+h²[X,Y])||');ax.loglog(hs,errors[0]*(hs/hs[0])**3,'--',label='reference O(h³)')
    ax.set_xlabel('dimensionless loop side h');ax.set_ylabel('Frobenius error');ax.legend();ax.grid(alpha=.25);ax.set_title('Non-Abelian Wilson loop: small-area limit')
    fig.tight_layout();fig.savefig(ROOT/'figures'/'02_NONABELIAN_HOLONOMY_CONVERGENCE_THEORY.png',dpi=165);plt.close(fig)
    return summary
