#!/usr/bin/env python3
"""Optional plots of normalized Einstein-frame radius potential, no extra claims."""
from pathlib import Path
import math
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise SystemExit('Optional matplotlib not installed. Core verification does not require it.')
ROOT=Path(__file__).resolve().parents[1]; (ROOT/'plots').mkdir(exist_ok=True)
H=1.; nc=5;ns=2; x0=50/3;y0=1.;Lambda=43/50

def ve(u,v):
    x=x0*math.exp(2*u);y=y0*math.exp(2*v)
    w=2*Lambda -24/x -2/y +8*H*nc**2/x**2 +H*ns**2/(4*y**2)
    return w*x0*x0*y0/(x*x*y)
for var in ['CP2','S2']:
    xs=[-0.5+i/400 for i in range(401)]
    ys=[ve(x,0) if var=='CP2' else ve(0,x) for x in xs]
    plt.figure(figsize=(8,4.6))
    plt.plot(xs,ys)
    plt.axhline(0,linestyle='--',linewidth=0.8)
    plt.xlabel('log radius shift: '+('ln(R_CP2/R0)' if var=='CP2' else 'ln(R_S2/R0)'))
    plt.ylabel('Relative potential (normalized; arbitrary overall factor)')
    plt.title('ROOT V136: homogeneous radius potential, '+var)
    plt.tight_layout(); plt.savefig(ROOT/'plots'/('radius_potential_'+var+'.png'),dpi=170)
    plt.close()
print('Optional plots created successfully.')
