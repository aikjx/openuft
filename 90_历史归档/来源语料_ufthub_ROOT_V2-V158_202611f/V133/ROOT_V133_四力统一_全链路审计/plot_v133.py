#!/usr/bin/env python3
"""Optional: redraw included PNG charts. Requires matplotlib."""
import csv
import math
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
with (ROOT/'data/running_curves.csv').open(encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(9,5.5))
x=[float(r['log10_mu_GeV']) for r in rows]
for name,label in [('alpha1_inv','SU(5)-normalized U(1)'),('alpha2_inv','SU(2)'),('alpha3_inv','SU(3)')]:
    ax.plot(x,[float(r[name]) for r in rows],label=label,linewidth=2)
ax.set(xlabel='log10 (energy scale / GeV)',ylabel='inverse dimensionless gauge coupling',title='SM one-loop running: three couplings do not meet')
ax.legend();ax.grid(alpha=.3);fig.tight_layout();fig.savefig(ROOT/'plots/SM_one_loop_running.png',dpi=170);plt.close(fig)
with (ROOT/'data/berry_phase_convergence.csv').open(encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(8,5.2))
for theta in (0.35,0.6,1.1):
    rr=[r for r in rows if math.isclose(float(r['polar_angle_rad']),theta) and int(r['helicity'])==1]
    ax.loglog([int(r['sample_count']) for r in rr],[float(r['absolute_phase_error_rad']) for r in rr],marker='o',label=f'polar angle {theta:g} rad')
ax.set(xlabel='number of points around k-direction loop',ylabel='absolute holonomy phase error (rad)',title='Photon Berry phase: numerical convergence')
ax.legend();ax.grid(alpha=.3,which='both');fig.tight_layout();fig.savefig(ROOT/'plots/Berry_phase_convergence.png',dpi=170);plt.close(fig)
print('Saved:',*[p.name for p in sorted((ROOT/'plots').glob('*.png'))])
