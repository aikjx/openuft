# -*- coding: utf-8 -*-
"""probe v14h: forward-from-boundary shooting VALIDATED on GR, then check s_out."""
import time, numpy as np
from scipy.optimize import root as sp_root
t0=time.time()

def shoot_forward(Vg, h, init):
    N=len(Vg); Wk0_base=-0; twoab=0
    u,v,us,vs = init
    for k in range(N-1):
        Wk0=-a*a+b*b; twoab=2*a*b
        W=Vg[k]+Wk0
        k1u,k1v,k1us,k1vs=us,vs,W*u+twoab*v,W*v-twoab*u
        u2,v2=u+0.5*h*k1u,v+0.5*h*k1v
        us2,vs2=us+0.5*h*k1us,vs+0.5*h*k1vs
        k2u,k2v=us2,vs2
        k2us,k2vs=W*u2+twoab*v2,W*v2-twoab*u2
        u3,v3=u+0.5*h*k2u,v+0.5*h*k2v
        us3,vs3=us+0.5*h*k2us,vs+0.5*h*k2vs
        k3u,k3v=us3,vs3
        k3us,k3vs=W*u3+twoab*v3,W*v3-twoab*u3
        u4,v4=u+h*k3u,v+h*k3v
        us4,vs4=us+h*k3us,vs+h*k3vs
        k4u,k4v=us4,vs4
        Wp=Vg[min(k+1,N-1)]+Wk0
        k4us,k4vs=Wp*u4+twoab*v4,Wp*v4-twoab*u4
        u+=h/6*(k1u+2*k2u+2*k3u+k4u); v+=h/6*(k1v+2*k2v+2*k3v+k4v)
        us+=h/6*(k1us+2*k2us+2*k3us+k4us); vs+=h/6*(k1vs+2*k2vs+2*k3vs+k4vs)
    psi=complex(u,v); psis=complex(us,vs)
    return psis/psi - 1j*complex(a,b)

# GR forward: start at horizon ingoing
rh=2.0; r0=2.001
r=np.linspace(r0,120.0,400000)
f=1-2/r; rstar=r+2*np.log(np.abs(r/2-1)); V=f*(6/r**2-6/r**3)
s0=r0+2*np.log(r0/2-1)
s=rstar-s0
h=0.01
GRtruth=complex(0.37367168441804166,-0.0889623156889341)
print("GR FORWARD horizon-ingoing -> outgoing match, scan s_out")
print(" truth=0.3736716844 -0.0889623157 i")
a=b=None
def solve(SO,seed):
    global a,b
    def Fv(x):
        global a,b
        a,b=float(x[0]),float(x[1])
        sg=np.arange(0,SO+0.5*h,h); Vg=np.interp(sg,s,V)
        init=(1.0,0.0,-b,a)  # psi=1, psi_s=-i w = b - i a
        return np.array([shoot_forward(Vg,h,init).real, shoot_forward(Vg,h,init).imag])
    sol=sp_root(Fv,seed,method='hybr',options={'xtol':1e-13,'maxfev':3000})
    global a,b; a,b=float(sol.x[0]),float(sol.x[1])
    return complex(*sol.x)
seed=[0.40,-0.10]
print(" s_out   w                              |w-truth|")
for SO in [10,20,30,50,80,120]:
    w=solve(float(SO),seed); seed=[w.real,w.imag]
    print(" %5.0f  %.8f %+.8f i   %.2e"%(SO,w.real,w.imag,abs(w-GRtruth)))
print("\nelapsed %.1f s"%(time.time()-t0))
