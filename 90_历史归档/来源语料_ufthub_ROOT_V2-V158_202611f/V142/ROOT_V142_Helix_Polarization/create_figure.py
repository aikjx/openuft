from pathlib import Path
import sys,math,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa F401
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p))
from src.physics import wave
fig=plt.figure(figsize=(9,6))
ax=fig.add_subplot(111,projection='3d')
zvals=np.linspace(0,4*math.pi,240)
E=[];B=[]
for z in zvals:
    e,b=wave(0,z);E.append(e);B.append(b)
E=np.array(E);B=np.array(B)
ax.plot(E[:,0],E[:,1],zvals,label='E field tip (not photon path)',lw=2)
ax.plot(B[:,0],B[:,1],zvals,label='B field tip (90 deg rotated)',lw=1.7)
ax.plot([0,0],[0,0],[0,float(zvals[-1])],linestyle=':',label='energy propagation +z')
ax.set(xlabel='x field amplitude',ylabel='y field amplitude',zlabel='z coordinate',title='Circular polarization: helical field patterns, straight energy flow')
ax.legend(loc='upper left',fontsize=8)
fig.tight_layout()
fig.savefig(p/'figures'/'polarization_helix.png',dpi=150)
plt.close(fig)
with (p/'results'/'wave_samples.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['z','Ex','Ey','Ez','Bx','By','Bz','Sx','Sy','Sz'])
    for z,e,b in zip(zvals,E,B):
        s=np.cross(e,b)
        w.writerow([f'{z:.12g}',*[f'{v:.12g}' for v in e],*[f'{v:.12g}' for v in b],*[f'{v:.12g}' for v in s]])
print('saved figure and CSV')
