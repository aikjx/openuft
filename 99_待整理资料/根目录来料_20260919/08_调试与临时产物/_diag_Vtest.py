# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp

def make_ode(Vfunc):
    def ode_rstar(r, y, w, ell=2):
        f = 1.0 - 2.0/r
        V = Vfunc(r, ell)
        return [y[1]/f, (V - w*w)*y[0]/f]
    return ode_rstar

def V1(r, ell=2):
    """V = f l(l+1)/r^2  (no f'/r)"""
    f = 1.0 - 2.0/r
    return f*ell*(ell+1)/r**2

def V2(r, ell=2):
    """V = f(l(l+1)/r^2 + f'/r)"""
    f = 1.0 - 2.0/r
    fp = 2.0/r**2
    return f*(ell*(ell+1)/r**2 + fp/r)

r0 = 2.001
rstar0 = r0 + 2*np.log(r0/2 - 1)
w = complex(0.37367, -0.08896)
u0 = np.exp(-1j*w*rstar0)
up0 = -1j*w*u0

for name, Vfunc in [("V1=f*l(l+1)/r^2", V1), ("V2=f(l(l+1)/r^2+f'/r)", V2)]:
    sol = solve_ivp(make_ode(Vfunc), (r0, 50.0), [u0, up0], args=(w,),
                    t_eval=[50.0], method="DOP853", rtol=1e-10, atol=1e-12)
    ulast = sol.y[0,-1]; up_last = sol.y[1,-1]
    rlast = 50.0
    rstar_last = rlast + 2*np.log(rlast/2 - 1)
    A_in = (ulast + (1j/w)*up_last) * np.exp(1j*w*rstar_last)/2
    A_out = (ulast - (1j/w)*up_last) * np.exp(-1j*w*rstar_last)/2
    print(f"{name}: |A_in/A_out|={abs(A_in/A_out):.4e}  (QNM=>~0)")
