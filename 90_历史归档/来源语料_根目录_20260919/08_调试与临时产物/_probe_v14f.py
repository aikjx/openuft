# -*- coding: utf-8 -*-
"""probe v14f: extend s_out, Richardson extrapolate to infinity. Also grid-step check."""
import time, numpy as np
from scipy.optimize import root as sp_root
t0=time.time()

def build(cm, dd, rmax=800.0):
    from scipy.optimize import brentq
    rh = brentq(lambda r: 1+cm/r**2+dd/r**3, 1e-3, 5.0, xtol=1e-14)
    r = np.linspace(rh*(1+1e-9), rmax, 800000)
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

cm,dd=-0.5,0.0
rh,s,V=build(cm,dd)
print("c=%s r_h=%.6f  s(rmax)=%.1f  Vpeak=%.4f@s=%.3f"%(cm,rh,s[-1],V.max(),s[np.argmax(V)]))

def solve(SO,h,seed):
    def Fv(x):
        w=complex(x[0],x[1]); f=shoot_inward(s,V,h,SO,w); return [f.real,f.imag]
    sol=sp_root(Fv,seed,method='hybr',options={'xtol':1e-13,'maxfev':3000})
    return complex(*sol.x)

h=0.005
SOS=[40,60,80,100,150,200,300]
roots=[]
seed=[0.98,-0.05]
print("\n s_out    w                              |Fwall|")
for SO in SOS:
    w=solve(float(SO),h,seed); f=shoot_inward(s,V,h,float(SO),w)
    print(" %5.0f   %.8f %+.8f i   %.2e"%(SO,w.real,w.imag,abs(f)))
    roots.append((SO,w)); seed=[w.real,w.imag]

# Richardson: error ~ V(s_out) ~ decays; try simple extrapolate using last 3 (100,150,200,300)
import numpy as np
print("\nRichardson extrapolation (assume error ~ exp(-2|Im w| s_out)):")
# use last three s_out to fit w(s)=w_inf + C*exp(-a s)
# simpler: linear in 1/s_out
def rich(pts):
    xs=np.array([p[0] for p in pts],float); yr=np.array([p[1].real for p in pts]); yi=np.array([p[1].imag for p in pts])
    return yr,yi
for label,sel in [("last3 (150,200,300)",roots[-3:]),("last2 (200,300)",roots[-2:])]:
    pass
# 1/s extrapolation
xs=np.array([1.0/so for so,_ in roots[-3:]])
yr=np.array([w.real for _,w in roots[-3:]])
yi=np.array([w.imag for _,w in roots[-3:]])
pr=np.polyfit(xs,yr,1); pi=np.polyfit(xs,yi,1)
print("  ~w(1/s) extrap limit: Re=%.6f  Im=%.6f"%(pr[-1],pi[-1]))
print("\nelapsed %.1f s"%(time.time()-t0))
