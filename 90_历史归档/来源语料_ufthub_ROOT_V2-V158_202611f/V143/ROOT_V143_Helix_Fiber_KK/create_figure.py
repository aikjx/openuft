"""Optional figures: does not affect science calculations or tests."""
import json
from math import pi
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from src.physics import ALPHA,ELECTRON_MASS_KG,PLANCK_MASS_KG,null_helix_example
root=Path(__file__).resolve().parent
out=root/'figures';out.mkdir(exist_ok=True)

r=np.logspace(-24,0,500)
fig,ax=plt.subplots(figsize=(8,5))
ax.loglog(r,4*r*r,label='Minimal circle model')
ax.axhline(ALPHA,linestyle='--',label='Observed electromagnetic fine structure constant')
ax.scatter([ELECTRON_MASS_KG/PLANCK_MASS_KG],[4*(ELECTRON_MASS_KG/PLANCK_MASS_KG)**2],s=45,label='Electron mass inserted (model prediction)')
ax.set_xlabel('Mass / Planck mass')
ax.set_ylabel('Dimensionless alpha')
ax.set_title('ROOT V143: minimal KK mass-charge consistency check')
ax.grid(True,which='both',alpha=.3)
ax.legend(loc='upper left',fontsize=8)
fig.tight_layout();fig.savefig(out/'mass_coupling_mismatch.png',dpi=170);plt.close(fig)

h=null_helix_example()
t=np.linspace(0,4*pi,800)
fig=plt.figure(figsize=(8,6))
ax=fig.add_subplot(111,projection='3d')
ax.plot(h.radius*np.cos(h.omega*t),h.radius*np.sin(h.omega*t),h.axial_speed*t)
ax.set_xlabel('x / L');ax.set_ylabel('y / L');ax.set_zlabel('z / L')
ax.set_title('3D projection of a 5D null helical trajectory')
fig.tight_layout();fig.savefig(out/'projected_helix.png',dpi=170);plt.close(fig)
print('Wrote:',*[str(p) for p in out.glob('*.png')])
