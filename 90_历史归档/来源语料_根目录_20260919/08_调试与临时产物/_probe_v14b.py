# -*- coding: utf-8 -*-
"""probe v14b: proven 4-real RK4, TUFT wall Neumann, scan s_out + seeds."""
import time, numpy as np
from scipy.optimize import root as sp_root
t0=time.time()

def make_grid(cm, dd, rmax=200.0):
    # wall radius
    from scipy.optimize import brentq
    rh = brentq(lambda r: 1+cm/r**2+dd/r**3, 1e-3, 5.0, xtol=1e-14)
    r = np.linspace(rh*(1+1e-9), rmax, 400000)
    g = 1+cm/r**2+dd/r**3
    F = np.exp(2/r)*np.sqrt(np.clip(g,0,None))
    s = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
    V = np.exp(-2/r)*6.0/r**2
    ipk = int(np.argmax(V))
    return rh, r, s, V, s[ipk]

def make_shooter(Vg, h):
    N = len(Vg)
    def shoot(w, init):
        a,b = float(w.real), float(w.imag)
        Wk0 = -a*a + b*b; twoab = 2*a*b
        u,v,us,vs = init
        for k in range(N-1):
            W = Vg[k]+Wk0
            k1u,k1v,k1us,k1vs = us,vs, W*u+twoab*v, W*v-twoab*u
            u2,v2 = u+0.5*h*k1u, v+0.5*h*k1v
            us2,vs2 = us+0.5*h*k1us, vs+0.5*h*k1vs
            k2u,k2v = us2,vs2
            Wm = Vg[k]+Wk0
            k2us,k2vs = Wm*u2+twoab*v2, Wm*v2-twoab*u2
            u3,v3 = u+0.5*h*k2u, v+0.5*h*k2v
            us3,vs3 = us+0.5*h*k2us, vs+0.5*h*k2vs
            k3u,k3v = us3,vs3
            k3us,k3vs = Wm*u3+twoab*v3, Wm*v3-twoab*u3
            u4,v4 = u+h*k3u, v+h*k3v
            us4,vs4 = us+h*k3us, vs+h*k3vs
            k4u,k4v = us4,vs4
            Wp = Vg[min(k+1,N-1)]+Wk0
            k4us,k4vs = Wp*u4+twoab*v4, Wp*v4-twoab*u4
            u  += h/6*(k1u+2*k2u+2*k3u+k4u)
            v  += h/6*(k1v+2*k2v+2*k3v+k4v)
            us += h/6*(k1us+2*k2us+2*k3us+k4us)
            vs += h/6*(k1vs+2*k2vs+2*k3vs+k4vs)
        psi = complex(u,v); psis = complex(us,vs)
        return psis/psi - 1j*complex(a,b)
    return shoot

def find(shoot, guess, tol=1e-11):
    def f(x):
        w=complex(x[0],x[1]); z=shoot(w,(1.,0.,0.,0.)); return [z.real,z.imag]
    try:
        sol=sp_root(f,[guess.real,guess.imag],method='hybr',
                    options={'xtol':tol,'maxfev':2500})
        w=complex(*sol.x); r=abs(shoot(w,(1.,0.,0.,0.)))
        return w, r, sol.success
    except Exception:
        return None,1e9,False

cm,dd=-0.5,0.0
rh,r,s,V,L = make_grid(cm,dd)
print("c=%s d=%s  r_h=%.6f  L(wall->peak)=%.4f  s(rmax)=%.2f"%(cm,dd,rh,L,s[-1]))
h=0.01
print(" s_out   w                              |F|")
for so in [8,10,12,15,20,25,30,40]:
    sg = np.arange(0, so+0.5*h, h)
    Vg = np.interp(sg, s, V)
    shoot = make_shooter(Vg, h)
    w,r,ok = find(shoot, complex(0.48,-0.08))
    if w is not None and r<1e-6:
        print(" %5.1f  %.8f %+.8f i   %.2e"%(so,w.real,w.imag,r))
    else:
        # try seed near GR
        w2,r2,ok2 = find(shoot, complex(0.40,-0.10))
        if w2 is not None and r2<1e-6:
            print(" %5.1f  %.8f %+.8f i   %.2e (seed GR)"%(so,w2.real,w2.imag,r2))
        else:
            print(" %5.1f  no clean root  r=%.1e"%(so, r if w is not None else r2))
print("elapsed %.1f s"%(time.time()-t0))
