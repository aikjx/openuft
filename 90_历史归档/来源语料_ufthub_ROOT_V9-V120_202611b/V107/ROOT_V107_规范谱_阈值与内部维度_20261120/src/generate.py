"""Deterministically generate ROOT V107 theory/model artifacts, never empirical measurements."""
from pathlib import Path
import json, csv, math
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .theory import summary,Benchmark,flow_at_mu,common_scale,required_ratio,split_required_log_ratio

ROOT=Path(__file__).resolve().parent.parent

def run():
    result=summary(prec=80)
    (ROOT/'results').mkdir(exist_ok=True);(ROOT/'figures').mkdir(exist_ok=True)
    (ROOT/'results'/'summary_THEORY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    toy=common_scale(2,1000,prec=70)
    mD=float(toy['m_doublet']);mT=float(toy['m_triplet']);mu=float(toy['mu'])
    logE=np.linspace(math.log10(Benchmark().m_z),18,301)
    series=[]
    for l in logE:
        E=10**float(l)
        sm=flow_at_mu(E,n_pairs=0,prec=36)
        same=flow_at_mu(E,n_pairs=2,m_doublet=1000,m_triplet=1000,prec=36)
        split=flow_at_mu(E,n_pairs=2,m_doublet=mD,m_triplet=mT,prec=36)
        series.append([E,*map(float,sm),*map(float,same),*map(float,split)])
    filename=ROOT/'results'/'one_loop_gauge_flow_ILLUSTRATIVE.csv'
    with filename.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f)
        w.writerow(['mu_GeV','SM_inv_alpha1','SM_inv_alpha2','SM_inv_alpha3',
                    'DEGENERATE_2pairs_inv_alpha1','DEGENERATE_2pairs_inv_alpha2','DEGENERATE_2pairs_inv_alpha3',
                    'SPLIT_2pairs_inv_alpha1','SPLIT_2pairs_inv_alpha2','SPLIT_2pairs_inv_alpha3'])
        w.writerows(series)
    arr=np.array(series)
    for idx,name,title in [(1,'01_SM_ONLY','SM: one-loop inverse couplings'),
                           (4,'02_COMPLETE_DEGENERATE','Two complete degenerate vectorlike SU(5) pairs'),
                           (7,'03_SPLIT_PAIRS_TOY','Two split vectorlike SU(5) pairs (theory-only fit)')]:
        fig,ax=plt.subplots(figsize=(9.5,5.4))
        for j,label in enumerate(['alpha1 inv','alpha2 inv','alpha3 inv']):
            ax.plot(arr[:,0],arr[:,idx+j],label=label,lw=2)
        if idx==7:
            ax.axvline(mu,ls='--',lw=1.4,label=f'common crossing ~{mu:.2e} GeV')
            ax.axvline(mT,ls=':',lw=1.1,label=f'triplet threshold ~{mT:.2e} GeV')
        ax.set_xscale('log');ax.set_xlim(Benchmark().m_z,1e18)
        ax.set_xlabel('Energy scale mu / GeV (log)');ax.set_ylabel('Inverse gauge coupling')
        ax.set_title(title+' | illustrative one-loop model, NOT observed')
        ax.legend(loc='upper center',ncol=2,fontsize=8);ax.grid(alpha=.2)
        fig.tight_layout();fig.savefig(ROOT/'figures'/(name+'_THEORY.png'),dpi=150)
        plt.close(fig)
    pairs=np.arange(1,7)
    logs=np.array([float(split_required_log_ratio(int(n))) for n in pairs])
    cap=math.log(Benchmark().planck_energy/Benchmark().m_z)
    fig,ax=plt.subplots(figsize=(8,5))
    ax.bar(pairs,logs)
    ax.axhline(cap,ls='--',label='log(M_Pl/MZ) bound')
    ax.set_xticks(pairs);ax.set_xlabel('Number of identical split vectorlike pairs')
    ax.set_ylabel('Required log(M_triplet/M_doublet) per pair')
    ax.set_title('One-loop threshold demand | NOT physical viability')
    ax.legend();ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(ROOT/'figures'/'04_SPLITTING_DEMAND_THEORY.png',dpi=150);plt.close(fig)
    print('Generated V107 model calculations:', filename.name, 'and four figures')
    return result

if __name__=='__main__':run()
