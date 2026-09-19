# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from scipy.optimize import brentq, root as sp_root

def geo(c, d, l=2.0, rmax=60.0, Nr=200000):
    def wallf(r): return 1.0 + c/r**2 + d/r**3
    rs = np.linspace(1e-3, 5.0, 200000)
    v = wallf(rs)
    rh = None
    for i in range(len(rs)-1):
        if v[i]*v[i+1] < 0:
            rh = brentq(wallf, rs[i], rs[i+1], xtol=1e-15); break
    r = np.linspace(rh*(1+1e-12), rmax, Nr)
    F = np.exp(2.0/r)*np.sqrt(1.0 + c/r**2 + d/r**3)
    s = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]+F[:-1])*np.diff(r))])
    V = np.exp(-2.0/r)*l*(l+1)/r**2
    return rh, r, s, V

def solve_probe(c,d,wguess,s_out=30.0,l=2.0):
    rh,r,s,V = geo(c,d)
    Vs = interp1d(s, V, kind='cubic', fill_value='extrapolate')
    def rhs(x,y,w):
        a,b = w
        Vm = Vs(x); W = Vm - a*a + b*b; ab = 2*a*b
        u1,u2,u3,u4 = y
        return [u3, u4, W*u1 + ab*u2, W*u2 - ab*u1]
    def resid(xw):
        a,b = xw
        sol = solve_ivp(rhs,[0,s_out],[1.0,0.0,0.0,0.0],args=((a,b),),
                        method='DOP853',rtol=1e-11,atol=1e-13)
        u1,u2,u3,u4 = sol.y[:,-1]
        psi = complex(u1,u2); dps = complex(u3,u4)
        w = complex(a,b)
        Fout = dps/psi - 1j*w   # =0 means pure outgoing
        return [Fout.real, Fout.imag]
    g = wguess
    sol = sp_root(resid,g,method='hybr',options={'xtol':1e-13,'maxfev':3000})
    a,b = sol.x
    return complex(a,b), np.hypot(*resid(sol.x)), sol.success

for (c,d,g) in [(-0.5,0.0,(0.45,-0.05)),(-0.5,0.0,(0.30,-0.25)),
                (-0.29,-0.05,(0.35,-0.05)),(-0.29,-0.05,(0.25,-0.25))]:
    try:
        w,res,ok = solve_probe(c,d,g)
        print(f"c={c} g={g}: w={w:.6f}  resid={res:.2e}  conv={ok}")
    except Exception as e:
        import traceback; print("fail",c,repr(e))
