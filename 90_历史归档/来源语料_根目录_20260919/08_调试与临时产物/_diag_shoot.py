# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

def V2(r, ell=2):
    f = 1.0 - 2.0/r
    fp = 2.0/r**2
    return f*(ell*(ell+1)/r**2 + fp/r)

def shoot(w, ell=2, r0=2.001, r_end=80.0):
    rstar0 = r0 + 2*np.log(r0/2 - 1)
    u0 = np.exp(-1j*w*rstar0)
    up0 = -1j*w*u0
    def ode(r, y):
        f = 1.0 - 2.0/r
        V = V2(r, ell)
        return [y[1]/f, (V - w*w)*y[0]/f]
    sol = solve_ivp(ode, (r0, r_end), [u0, up0], t_eval=[r_end],
                    method="DOP853", rtol=1e-10, atol=1e-12)
    ulast = sol.y[0,-1]; up_last = sol.y[1,-1]
    rstar_last = r_end + 2*np.log(r_end/2 - 1)
    A_in = (ulast + (1j/w)*up_last) * np.exp(1j*w*rstar_last)/2
    return A_in

def F(x):
    w = complex(x[0], x[1])
    r = shoot(w)
    return [r.real, r.imag]

sol = root(F, [0.373, -0.09], method="hybr", tol=1e-10, options={"xtol":1e-10,"maxfev":5000})
wfound = complex(sol.x[0], sol.x[1])
print(f"Shooting root: w = {wfound.real:.6f} {wfound.imag:+.6f}i")
print(f"Reference    :   0.373670 -0.088960i")
