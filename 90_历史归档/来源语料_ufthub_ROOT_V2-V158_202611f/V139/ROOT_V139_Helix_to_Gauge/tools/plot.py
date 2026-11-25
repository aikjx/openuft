from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import LightHelix,berry_curvature_theta_phi
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
figdir=root/'figures'
figdir.mkdir(exist_ok=True)
h=LightHelix.from_curvature_torsion(.6,.8)
t=[10*math.pi*i/850 for i in range(851)]
x=[h.position(tt)[0] for tt in t]
y=[h.position(tt)[1] for tt in t]
z=[h.position(tt)[2] for tt in t]
fig=plt.figure(figsize=(9,6))
ax=fig.add_subplot(111,projection='3d')
ax.plot(x,y,z,lw=1.8)
ax.set(xlabel='x/L',ylabel='y/L',zlabel='z/L',title='Light-speed spatial helix (candidate kinematics; c=1)')
fig.tight_layout();fig.savefig(figdir/'helix_reconstruction.png',dpi=150);plt.close(fig)
angles=[i*math.pi/600 for i in range(601)]
fig,ax=plt.subplots(figsize=(8,4.5))
for m in [1,2,3]:ax.plot(angles,[berry_curvature_theta_phi(v,m) for v in angles],label=f'winding n={m}')
ax.set(xlabel='polar angle theta [rad]',ylabel='Berry F_theta_phi',title='Berry curvature: a geometric field, not assumed physical EM')
ax.legend();ax.grid(True,alpha=.3)
fig.tight_layout();fig.savefig(figdir/'berry_curvature.png',dpi=150);plt.close(fig)
print('figures generated',figdir)
