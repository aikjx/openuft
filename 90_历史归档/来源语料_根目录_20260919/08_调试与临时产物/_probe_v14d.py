# -*- coding: utf-8 -*-
"""probe v14d: INWARD shoot from exact outgoing at s_out to wall, check psi_s(0)=0.
Box-insensitive: s_out only starts the exact asymptote; wall condition selects w."""
import time, numpy as np
from scipy.optimize import root as sp_root
t0=time.time()

def build(cm, dd, rmax=400.0):
    from scipy.optimize import brentq
    rh = brentq(lambda r: 1+cm/r**2+dd/r**3, 1e-3, 5.0, xtol=1e-14)
    r = np.linspace(rh*(1+1e-9), rmax, 600000)
    g = 1+cm/r**2+dd/r**3
    F = np.exp(2/r)*np.sqrt(np.clip(g,0,None))
    s = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
    V = np.exp(-2/r)*6.0/r**2
    return rh, s, V

def shoot_inward(s, V, h, s_out, w):
    """start at s_out: psi=1, psi_s=i w (pure outgoing). integrate to s=0. return psi_s(0)/psi(0)."""
    # grid from s_out down to 0
    sg = np.arange(s_out, -0.5*h, -h)
    Vg = np.interp(sg, s, V)
    N=len(Vg)
    a,b=w.real, w.imag
    Wk0=-a*a+b*b; twoab=2*a*b
    # init: psi=1 -> u=1,v=0 ; psi_s=i w = i(a+ib)= -b + i a -> us=-b, vs=a
    u,v = 1.0, 0.0
    us,vs = -b, a
    hh = -h   # step inward: s_out -> 0
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
    return psis/psi   # wall log-derivative; QNM => 0

cm,dd=-0.5,0.0
rh,s,V=build(cm,dd)
print("c=%s r_h=%.6f Vpeak=%.4f@s=%.3f"%(cm,rh,V.max(),s[np.argmax(V)]))
h=0.01
# scan |wall log-deriv| near real axis at large s_out
SO=60.0
print("\n|F=psi_s/psi at wall| at s_out=%.0f (log10)"%SO)
print("       "+"".join("%8.3f"%im for im in np.arange(-0.01,-0.20,-0.03)))
for re_ in np.arange(0.2,1.05,0.10):
    row="re=%.2f"%re_
    for im in np.arange(-0.01,-0.20,-0.03):
        try:
            f=shoot_inward(s,V,h,SO,complex(re_,im))
            row+=" %8.1f"%(np.log10(abs(f)))
        except Exception:
            row+="      nan"
    print(row)
print("\nelapsed %.1f s"%(time.time()-t0))
