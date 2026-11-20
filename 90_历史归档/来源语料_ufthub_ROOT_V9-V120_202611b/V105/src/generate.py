"""Produce independent numerical and visual benchmarks; THEORY data only."""
from pathlib import Path
import json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .holonomy import su2_wilson_trace,su2_closed_form,su3_wilson_trace,su3_closed_form,small_loop_ratio
from .eft import PhaseEFT,DIMENSIONS

ROOT = Path(__file__).resolve().parents[1]

def run():
    results=ROOT/'results'; results.mkdir(exist_ok=True)
    figures=ROOT/'figures'; figures.mkdir(exist_ok=True)
    alpha,beta=0.35,0.60
    su2=su2_wilson_trace(alpha,beta)
    su3=su3_wilson_trace(alpha,beta)
    A,B=np.meshgrid(np.linspace(0,np.pi/2,141),np.linspace(0,np.pi/2,141))
    values=1-2*np.sin(A)**2*np.sin(B)**2
    fig,ax=plt.subplots(figsize=(7.2,5.2))
    contour=ax.contourf(A,B,values,levels=35)
    ax.set_xlabel('alpha [rad]');ax.set_ylabel('beta [rad]')
    ax.set_title('ROOT V105 | SU(2) normalized Wilson commutator trace (THEORY)')
    fig.colorbar(contour,ax=ax,label='Tr(W) / 2')
    fig.tight_layout();fig.savefig(figures/'01_SU2_WILSON_THEORY.png',dpi=160);plt.close(fig)

    epsilons=[0.2,0.1,0.05,0.025,0.0125]
    leading=[]
    for e in epsilons:
        ratio,expected=small_loop_ratio(e)
        leading.append({'epsilon':e,'normalized_frobenius_residual':float(np.linalg.norm(ratio-expected))})
    with open(results/'SMALL_LOOP_THEORY.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['epsilon','normalized_frobenius_residual']);w.writeheader();w.writerows(leading)
    eft=PhaseEFT(1e3,1.0,c1=0.2,c2=0.3,c3=0.4)
    summary={
        'status':'THEORY_ONLY_NO_DISCOVERY',
        'angles_rad':{'alpha':alpha,'beta':beta},
        'u1_commutator_trace':1.0,
        'su2_wilson_trace':su2,
        'su2_exact_formula':su2_closed_form(alpha,beta),
        'su3_embedded_wilson_trace':su3,
        'su3_exact_formula':su3_closed_form(alpha,beta),
        'max_formula_absolute_error':float(max(abs(su2-su2_closed_form(alpha,beta)),abs(su3-su3_closed_form(alpha,beta)))),
        'toy_eft':{'f_GeV':eft.f_GeV,'Lambda_GeV':eft.Lambda_GeV,'canonical_theta_mass_GeV':eft.canon_mass_GeV(),'source_test_GeV4':eft.source_GeV4(1e-4,-2e-4,3e-4)},
        'dimension_table_natural_units_M_power':DIMENSIONS,
        'limitations':['This is a known non-Abelian gauge-theory identity, not a newly established force law.','A single U(1) phase cannot replace noncommuting SU(2)/SU(3) gauge data.','The toy EFT introduces independent parameters and does not predict G.','No experiment or complete four-force unified theory.']
    }
    with open(results/'ROOT_V105_SUMMARY_THEORY.json','w',encoding='utf-8') as f:json.dump(summary,f,ensure_ascii=False,indent=2)
    return summary

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
