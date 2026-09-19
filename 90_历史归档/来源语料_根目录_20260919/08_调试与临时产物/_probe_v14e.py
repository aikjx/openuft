# -*- coding: utf-8 -*-
"""probe v14e: fine scan near cavity fundamental, refine root, check s_out stability."""
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
    sg = np.arange(s_out, -0.5*h, -h)
    Vg = np.interp(sg, s, V)
    N=len(Vg); a,b=w.real,w.imag
    Wk0=-a*a+b*b; twoab=2*a*b
    u,v = 1.0,0.0; us,vs=-b,a; hh=-h
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

cm,dd=-0.5,0.0
rh,s,V=build(cm,dd)
print("c=%s r_h=%.6f"%(cm,rh))
h=0.005
SO=80.0
print("\nFine |wall log-deriv| near cavity fundamental, s_out=%.0f"%SO)
print("       "+"".join("%8.3f"%im for im in np.arange(-0.01,-0.13,-0.02)))
for re_ in np.arange(0.7,1.25,0.05):
    row="re=%.2f"%re_
    for im in np.arange(-0.01,-0.13,-0.02):
        f=shoot_inward(s,V,h,SO,complex(re_,im))
        row+=" %8.1f"%np.log10(abs(f))
    print(row)

# refine root near (1.0,-0.04)
def Fvec(x, SO):
    w=complex(x[0],x[1]); f=shoot_inward(s,V,h,SO,w); return [f.real,f.imag]
print("\nRoot refinement + s_out stability:")
print(" s_out   w                              |Fwall|")
prev=None
for SO in [40,50,60,80,100]:
    seed = [1.0,-0.04] if prev is None else [prev.real,prev.imag]
    sol=sp_root(Fvec, seed, args=(SO,), method='hybr', options={'xtol':1e-12,'maxfev':2000})
    w=complex(*sol.x); f=shoot_inward(s,V,h,SO,w)
    print(" %5.0f  %.8f %+.8f i   %.2e"%(SO,w.real,w.imag,abs(f)))
    prev=w
print("\nelapsed %.1f s"%(time.time()-t0))
