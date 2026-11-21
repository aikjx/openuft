"""Deterministic offline result generation for V131 (matplotlib optional for PNGs)."""
import csv,json,math,pathlib
from v131 import *
ROOT=pathlib.Path(__file__).resolve().parents[1]
(ROOT/'data').mkdir(parents=True,exist_ok=True)
r=main_result()
(ROOT/'data'/'v131_results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
lo=r['triplet_octet_allowed']['lower_GeV'];hi=r['triplet_octet_allowed']['upper_GeV']
scales=[10**(math.log10(lo)+(math.log10(1e16)-math.log10(lo))*i/150) for i in range(151)]
rows=[]
for mu in scales:
    z=triplet_octet_at_scale(mu)
    rows.append({'MU_GeV':mu,'Mtriplet_GeV':z['Mtriplet_GeV'],
                 'Moctet_GeV':z['Moctet_GeV'],'valid_weak_scale_thresholds':int(z['physical_thresholds']),
                 'residual_max_inv_alpha':z['residual_max_inverse']})
with (ROOT/'data'/'threshold_scan.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    single=one_triplet_solution()
    tmax=math.log(1e17/MZ)
    mus=np.geomspace(MZ,1e17,400)
    for kind,masses,title,filename in [
       ('SM',[],'Standard Model: no exact one-loop crossing','one_loop_SM.png'),
       ('triplet',[(single['Mtriplet_GeV'],TRIPLET)],'Triplet threshold: formal one-loop crossing','one_loop_triplet.png')]:
        fig,ax=plt.subplots(figsize=(9,5.2))
        for i,label in enumerate(['alpha1^-1','alpha2^-1','alpha3^-1']):
            ax.plot(mus,[inv_couplings(float(mu),masses)[i] for mu in mus],label=label)
        ax.set_xscale('log');ax.set_xlabel('Energy scale [GeV]');ax.set_ylabel('Inverse gauge coupling');ax.set_title(title)
        ax.axvline(single['MU_GeV'],linestyle=':',linewidth=1.2,label='toy MU')
        ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(ROOT/'figures'/filename,dpi=155);plt.close(fig)
    valid=[z for z in rows if z['valid_weak_scale_thresholds']]
    fig,ax=plt.subplots(figsize=(9,5.2))
    ax.plot([z['MU_GeV'] for z in valid],[z['Mtriplet_GeV'] for z in valid],label='Weyl SU(2) triplet mass')
    ax.plot([z['MU_GeV'] for z in valid],[z['Moctet_GeV'] for z in valid],label='Weyl SU(3) octet mass')
    ax.axhline(MZ,linestyle=':',label='MZ threshold floor')
    ax.axvline(hi,linestyle=':',label='upper MU bound')
    ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Formal unified scale MU [GeV]');ax.set_ylabel('Required mass [GeV]')
    ax.set_title('Triplet + octet: physical threshold feasibility window')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures'/'threshold_feasible_window.png',dpi=155);plt.close(fig)
except ImportError:
    print('matplotlib unavailable; JSON and CSV generated')
print('Generated V131 data',ROOT)
