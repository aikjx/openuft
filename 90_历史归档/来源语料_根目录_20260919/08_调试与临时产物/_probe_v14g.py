# -*- coding: utf-8 -*-
"""probe v14g: VALIDATE inward-shoot on GR Schwarzschild RW (known 0.373672-0.088962i).
If same method drifts here -> TUFT result untrustworthy. Wall here = horizon ingoing."""
import time, numpy as np
from scipy.optimize import root as sp_root
t0=time.time()

# GR Schwarzschild RW l=2: f=1-2/r, V=f(6/r^2 - 6/r^3), r*=r+2 ln(r/2-1)
rh=2.0
r=np.linspace(rh*(1+1e-6),120.0,400000)
f=1-2/r
rstar=r+2*np.log(np.abs(r/2-1))
V=f*(6/r**2-6/r**3)
# r* local: horizon r* -> -inf. Use global r*. Outgoing at r*->+inf.
# We shoot INWARD from large r* (outgoing) to near horizon, check ingoing regularity.
# Simpler & standard: forward from horizon ingoing. But we want to test THIS inward engine.

def shoot_inward(s, V, h, s_out, w):
    """start at s_out: pure outgoing. integrate inward. At inner end impose check."""
    sg=np.arange(s_out,-0.5*h,-h); Vg=np.interp(sg,s,V)
    N=len(Vg); a,b=w.real,w.imag; Wk0=-a*a+b*b; twoab=2*a*b
    u,v=1.0,0.0; us,vs=-b,a; hh=-h
    for k in range(N-1):
        W=Vg[k]+Wk0
        k1u,k1v,k1us,k1vs=us,vs,W*u+twoab*v,W*v-twoab*u
        u2,v2=u+0.5*hh*k1u,v+0.5*hh*k1v
        us2,vs2=us+0.5*hh*k1us,vs+0.5*hh*k1vs
        k2u,k2v=us2,vs2
        k2us,k2vs=W*u2+twoab*v2,W*v2-twoab*u2
        u3,v3=u+0.5*hh*k2u,v+0.5*hh*k2v
        us3,vs3=us+0.5*hh*k2us,vs+0.5*hh*k2vs
        k3u,k3v=us3,vs3
        k3us,k3vs=W*u3+twoab*v3,W*v3-twoab*u3
        u4,v4=u+hh*k3u,v+hh*k3v
        us4,vs4=us+hh*k3us,vs+hh*k3vs
        k4u,k4v=us4,vs4
        Wp=Vg[min(k+1,N-1)]+Wk0
        k4us,k4vs=Wp*u4+twoab*v4,Wp*v4-twoab*u4
        u+=hh/6*(k1u+2*k2u+2*k3u+k4u); v+=hh/6*(k1v+2*k2v+2*k3v+k4v)
        us+=hh/6*(k1us+2*k2us+2*k3us+k4us); vs+=hh/6*(k1vs+2*k2vs+2*k3vs+k4vs)
    psi=complex(u,v); psis=complex(us,vs)
    return psis/psi

# GR: set local s = r* - r*_inner. inner boundary near horizon.
# Choose inner r0=2.001, outer s_out. Inner BC = ingoing. We shoot inward and at inner
# check that solution is ingoing: psi_s/psi should equal -i w at the inner point.
r0=2.001
s0=r0+2*np.log(r0/2-1)
sg=np.linspace(0, rstar[-1]-s0, 400000)  # local s=0 at r0
Vg_full=np.interp(sg, rstar-s0, V)
h=0.01
GRtruth=complex(0.37367168441804166,-0.0889623156889341)
print("GR inward-outgoing -> inner ingoing check (psi_s/psi + i w = 0 at inner)")
print(" truth=%.12f %+.12f i"%(GRtruth.real,GRtruth.imag))
def solve(SO,seed):
    def Fv(x):
        w=complex(x[0],x[1]); f=shoot_inward(sg,Vg_full,h,float(SO),w)
        # inner should be INGOING: psi_s/psi = -i w  -> f + i w =0
        return [(f+1j*w).real,(f+1j*w).imag]
    sol=sp_root(Fv,seed,method='hybr',options={'xtol':1e-13,'maxfev':3000})
    return complex(*sol.x)
seed=[0.40,-0.10]
print(" s_out   w                              |w-truth|")
for SO in [20,40,60,100,150]:
    w=solve(SO,seed); seed=[w.real,w.imag]
    print(" %5.0f  %.8f %+.8f i   %.2e"%(SO,w.real,w.imag,abs(w-GRtruth)))
print("\nelapsed %.1f s"%(time.time()-t0))
