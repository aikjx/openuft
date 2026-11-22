#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_v134 import create_results

base=Path(__file__).resolve().parents[1]
fig=base/'figures';fig.mkdir(parents=True,exist_ok=True)
res, trans=create_results()

fig1,ax=plt.subplots(figsize=(8,4.8))
arr=np.array(trans['Q']);t=np.array(trans['time'])
for j in range(3): ax.plot(t,arr[:,j],label=f'Q{j+1}')
ax.set(xlabel='Proper-time parameter s (toy units)',ylabel='SU(2) charge component',title='V134: non-Abelian internal charge precession')
ax.legend();fig1.tight_layout();fig1.savefig(fig/'01_SU2_color_precession.png',dpi=175);plt.close(fig1)

fig2,ax=plt.subplots(figsize=(8,4.8))
d=np.array([x['delta'] for x in res['plaquette']]);err=np.array([x['loop_minus_leading'] for x in res['plaquette']])
ax.loglog(d,err,'o-',label='||W - exp(-i F delta^2)||')
ax.loglog(d,err[0]*(d/d[0])**3,'--',label='O(delta^3) reference')
ax.set(xlabel='Square loop side delta',ylabel='Matrix error',title='V134: Wilson plaquette small-loop expansion')
ax.legend();fig2.tight_layout();fig2.savefig(fig/'02_wilson_small_loop.png',dpi=175);plt.close(fig2)

fig3,ax=plt.subplots(figsize=(7.5,4.8))
labels=['Pure frame gauge','Constant non-Abelian A']
values=[res['flat_moving_frame_curvature_norm'],res['constant_nonabelian_curvature_norm']]
ax.bar(labels,values);ax.set(ylabel='Frobenius norm of Fxy',title='V134: connection does not imply curvature')
fig3.tight_layout();fig3.savefig(fig/'03_flat_vs_nonflat.png',dpi=175);plt.close(fig3)
print('Created', len(list(fig.glob('*.png'))),'plots')
