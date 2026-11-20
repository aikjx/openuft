"""Reproducible results: all theory/synthetic, no physical experiment."""
from pathlib import Path
import json, math, csv
from datetime import date
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .theory import full_summary,bpst_cumulative,min_boson_scale
from .ledger import build
from legacy.v107_theory import summary as v107_summary

ROOT=Path(__file__).resolve().parent.parent

def generate():
    ledger=build()
    old=v107_summary(prec=80)
    mu=float(old['two_pairs_toy']['mu_unify_GeV'])
    result=full_summary(mu)
    result['v107_reference_mu_GeV']=mu
    result['ledger']=ledger
    result['source_notes']=['V107 local original project','2026 PDG GUT review p->e+pi0 bound 2.4e34 yr','illustrative dim6 tau=8e34(Mx/1e16)^4 yr, not model independent']
    dst=ROOT/'results'/'mathematical_audit.json'
    dst.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'results'/'ledger_summary.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    # density/cumulative table
    ratios=np.geomspace(0.02,100,100)
    with (ROOT/'results'/'bpst_charge_THEORY.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['R_over_rho','Q_inside','source']);
        for x in ratios:w.writerow([f'{x:.12g}',f'{float(bpst_cumulative(float(x))):.16g}','BPST exact theoretical formula'])
    plt.figure(figsize=(8,4.2));plt.semilogx(ratios,[float(bpst_cumulative(float(x))) for x in ratios]);plt.xlabel('R / rho');plt.ylabel('Q(R)');plt.title('BPST SU(2) instanton: cumulative topological charge (THEORY)');plt.ylim(-.03,1.03);plt.grid(alpha=.22);plt.tight_layout();plt.savefig(ROOT/'figures'/'01_BPST_Q_THEORY.png',dpi=175);plt.close()
    # proton bound comparison, model conditional
    ms=np.geomspace(1e12,3e16,300)
    tau=8e34*(ms/1e16)**4
    plt.figure(figsize=(8,4.2));plt.loglog(ms,tau,label='Conditional dim-6 lifetime example');plt.axhline(2.4e34,ls='--',label='Super-K p -> e+ pi0 lower bound');plt.axvline(mu,ls=':',label='V107 toy crossing; MX=mu is an assumption');plt.xlabel('Assumed heavy X boson mass (GeV)');plt.ylabel('Partial proton lifetime (years)');plt.title('V107 toy crossing vs conditional proton decay constraint');plt.legend(fontsize=8);plt.grid(alpha=.22,which='both');plt.tight_layout();plt.savefig(ROOT/'figures'/'02_PROTON_CONDITIONAL_THEORY.png',dpi=175);plt.close()
    status=ledger['v108_dispositions'];names=[s for s,c in sorted(status.items(),key=lambda x:-x[1])];values=[status[x] for x in names]
    plt.figure(figsize=(10,5));plt.barh([n.replace('_',' ')[:38] for n in names[::-1]],values[::-1]);plt.xlabel('Issue count');plt.title('ROOT V108: 396 issue audit (NOT number of solved problems)');plt.tight_layout();plt.savefig(ROOT/'figures'/'03_396_ISSUE_AUDIT.png',dpi=170);plt.close()
    return result
if __name__=='__main__':
    d=generate(); print('generated 396 issue audit, topological proof data, conditional proton lifetime')
