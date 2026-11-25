"""Optional plotting (matplotlib). Source quantities use c=1 and L0 normalization."""
import sys,math,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v148.helix import NullHelix
from root_v148.emwave import CircularWave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

h=NullHelix(.6,1,.8)
N=400
figdir=ROOT/'figures';figdir.mkdir(exist_ok=True)

for beta,filename,title in [(0.,'helix_lab.png','Helical spatial projection | beta = 0'),(.8,'helix_boost.png','Same null worldline | axial beta = 0.8')]:
    b=h.boost(beta)
    ts=[i*4*math.pi/(N-1)/abs(b.omega) for i in range(N)]
    pts=[b.position(t) for t in ts]
    fig=plt.figure(figsize=(7.2,5.4))
    ax=fig.add_subplot(111,projection='3d')
    ax.plot([p[0] for p in pts],[p[1] for p in pts],[p[2] for p in pts],linewidth=2.4)
    ax.set_xlabel('x / L0');ax.set_ylabel('y / L0');ax.set_zlabel('z / L0')
    ax.set_title(title)
    ax.set_xlim(-.8,.8);ax.set_ylim(-.8,.8)
    ax.set_zlim(-.8,max(1.2,b.u*ts[-1]+.2))
    ax.text2D(.05,.94,f'kappa={b.curvature():.6f} |tau|={abs(b.torsion()):.6f}',transform=ax.transAxes,fontsize=10)
    plt.tight_layout();fig.savefig(figdir/filename,dpi=170);plt.close(fig)

betas=[-0.95+i*1.90/380 for i in range(381)]
fig,ax=plt.subplots(figsize=(7.4,4.6))
ax.plot(betas,[h.boost(b).curvature() for b in betas],label='Spatial curvature kappa')
ax.plot(betas,[h.boost(b).torsion() for b in betas],label='Spatial torsion tau')
ax.axvline(.8,ls='--',lw=1.0,label='beta=u (tau=0)')
ax.axhline(0,lw=.6)
ax.set(xlabel='Lorentz boost beta along axis',ylabel='1 / L0',title='Spatial Frenet invariants are not Lorentz scalars')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(figdir/'boost_curvature_torsion.png',dpi=170);plt.close(fig)

w=CircularWave(1.,1.,1)
phases=[2*math.pi*i/400 for i in range(401)]
fig,ax=plt.subplots(figsize=(7.2,4.4))
ax.plot(phases,[w.fields(s,0)[0][0] for s in phases],label='E_x')
ax.plot(phases,[w.fields(s,0)[0][1] for s in phases],label='E_y')
ax.plot(phases,[w.poynting(s,0)[2] for s in phases],label='S_z (energy flux)',ls='--')
ax.set(xlabel='Phase k(t-z)',ylabel='Normalized field / energy flux',title='Rotating fields with straight energy transport')
ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(figdir/'em_rotating_fields.png',dpi=170);plt.close(fig)
print('Figures generated:',len(list(figdir.glob('*.png'))))
