#!/usr/bin/env python3
"""Optional visualization of normalized toy model, not a fit to experiments."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v146 import illustrative_six_d
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    print('Optional matplotlib not installed'); raise SystemExit(0)
R=[.48+i*(2.7-.48)/600 for i in range(601)]
fig,ax=plt.subplots(figsize=(9.4,5.6))
for n in (1,2,3,4):
    p=illustrative_six_d(n).reduce()
    ax.plot(R,[p.v(r) for r in R],label=f'n = {n}',linewidth=2)
    ex=p.stable()
    if ex and .48<=ex.radius<=2.7:
        ax.scatter(ex.radius,ex.value,s=42,zorder=10)
ax.axhline(0,color='gray',linewidth=1,linestyle='--')
ax.set(xlim=(.48,2.7),ylim=(-5,4),xlabel='Internal radius R / L0',ylabel='Normalized Einstein-frame potential',title='ROOT V146 | Flux stabilization: illustrative parameters')
ax.text(.49,3.65,'Chosen couplings make n = 3 Minkowski; not an independent prediction',fontsize=9)
ax.grid(alpha=.22)
ax.legend()
fig.tight_layout()
fig.savefig(ROOT/'figures'/'radion_potential.png',dpi=170)
fig.savefig(ROOT/'figures'/'radion_potential.svg')
plt.close(fig)

fig,ax=plt.subplots(figsize=(9,4.6))
vals=[illustrative_six_d(n).reduce().stable() for n in range(9)]
ax.bar([str(n) for n in range(9)],[v.radius if v else 0 for v in vals])
ax.set(xlabel='Integer flux n',ylabel='Local-minimum radius R / L0',title='Only homogeneous radial extrema are tested')
for n,v in enumerate(vals):
    if v is None: ax.text(n,.035,'none',ha='center',fontsize=8,rotation=90)
    else: ax.text(n,v.radius+.02,f'{v.radius:.3f}',ha='center',fontsize=9)
ax.set_ylim(0,1.19)
ax.grid(axis='y',alpha=.23)
fig.tight_layout()
fig.savefig(ROOT/'figures'/'flux_radius.png',dpi=170)
fig.savefig(ROOT/'figures'/'flux_radius.svg')
plt.close(fig)
print('Generated 4 visuals')
