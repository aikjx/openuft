from __future__ import annotations
from pathlib import Path
import sys, json, csv, math
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_v130 import *
root=Path(__file__).resolve().parents[1]
(root/'data').mkdir(exist_ok=True)
with (root/'data'/'v130_results.json').open('w',encoding='utf-8') as f:
    json.dump(compute_summary(),f,indent=2,ensure_ascii=False)
with (root/'data'/'running.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['log10_mu_GeV','mu_GeV','alpha1_inv_SM','alpha2_inv_SM','alpha3_inv_SM','alpha1_inv_MSSM_toy','alpha2_inv_MSSM_toy','alpha3_inv_MSSM_toy'])
    a0=inverse_couplings()
    for i in range(450):
        lmz=math.log10(MZ_GEV); x=lmz+(19.0-lmz)*i/449; mu=10**x
        writer.writerow([f'{x:.10f}',f'{mu:.12g}',
                         *(f'{v:.12f}' for v in alpha_inv_at(mu,a0,B_SM)),
                         *(f'{v:.12f}' for v in alpha_inv_at(mu,a0,B_MSSM))])
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for scheme,b in [('standard_model',B_SM),('mssm_single_regime_toy',B_MSSM)]:
        X=[math.log10(MZ_GEV)+(19-math.log10(MZ_GEV))*i/300 for i in range(301)]
        Y=[alpha_inv_at(10**x,a0,b) for x in X]
        fig,ax=plt.subplots(figsize=(9,5.2))
        for k,name in enumerate([r'$\alpha_1^{-1}$',r'$\alpha_2^{-1}$',r'$\alpha_3^{-1}$']):
            ax.plot(X,[v[k] for v in Y],label=name)
        ax.set_xlabel(r'$\log_{10}(\mu/\mathrm{GeV})$')
        ax.set_ylabel('Inverse gauge coupling')
        ax.set_title('One-loop gauge running — '+scheme.replace('_',' '))
        ax.grid(alpha=.25);ax.legend();fig.tight_layout()
        fig.savefig(root/'figures'/f'coupling_{scheme}.png',dpi=150)
        plt.close(fig)
except ImportError:
    print('matplotlib absent: plotting skipped, core results still generated')
print('Results generated under',root)
