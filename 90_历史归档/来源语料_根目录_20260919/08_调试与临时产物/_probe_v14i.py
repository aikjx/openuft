# -*- coding: utf-8 -*-
"""probe v14i: clean |F| map of wall log-deriv to enumerate all TUFT roots."""
import time, numpy as np
from scipy.optimize import root as sp_root
from scipy.optimize import brentq
t0=time.time()

def build(c,d,rmax=600.0):
    rh=brentq(lambda r:1+c/r**2+d/r**3,1e-3,5.0,xtol=1e-14)
    r=np.linspace(rh*(1+1e-12),rmax,600000)
    g=1+c/r**2+d/r**3
    F=np.exp(2/r)*np.sqrt(np.clip(g,0,None))
    s=np.concatenate([[0.0],np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
    V=np.exp(-2/r)*6.0/r**2
    return rh,s,V

def finward(s,V,h,s_out,w):
    sg=np.arange(s_out,-0.5*h,-h); Vg=np.interp(sg,s,V)
    a,b=w.real,w.imag; Wk0=-a*a+b*b; twoab=2*a*b
    u,v=1.0,0.0; us,vs=-b,a; hh=-h
    for k in range(len(Vg)-1):
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
        Wp=Vg[min(k+1,len(Vg)-1)]+Wk0
        k4us,k4vs=Wp*u4+twoab*v4,Wp*v4-twoab*u4
        u+=hh/6*(k1u+2*k2u+2*k3u+k4u); v+=hh/6*(k1v+2*k2v+2*k3v+k4v)
        us+=hh/6*(k1us+2*k2us+2*k3us+k4us); vs+=hh/6*(k1vs+2*k2vs+2*k3vs+k4vs)
    return abs(complex(us,vs)/complex(u,v))

cm,dd=-0.5,0.0
rh,s,V=build(cm,dd)
print("c=%s r_h=%.5f L=%.4f"%(cm,rh,s[np.argmax(V)]))
h=0.005; SO=150.0
print("\nlog10|Fwall| at s_out=%.0f  (rows=Re, cols=Im)"%SO)
print("        "+"".join("%8.3f"%im for im in np.arange(-0.02,-0.60,-0.08)))
for re_ in np.arange(0.3,3.2,0.15):
    row="Re=%5.2f"%re_
    for im in np.arange(-0.02,-0.60,-0.08):
        row+=" %8.1f"%np.log10(finward(s,V,h,SO,complex(re_,im)))
    print(row)
print("\nelapsed %.1f s"%(time.time()-t0))
