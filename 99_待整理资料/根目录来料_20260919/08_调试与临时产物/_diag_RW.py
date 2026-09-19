# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

# Regge-Wheeler 势 (l=2 引力轴向): V = f [l(l+1)/r^2 - 6/r^3]
def V_RW(r, ell=2):
    f = 1.0 - 2.0/r
    return f*(ell*(ell+1)/r**2 - 6.0/r**3)

def shoot(w, ell=2, r0=2.001, r_end=80.0):
    rstar0 = r0 + 2*np.log(r0/2 - 1)
    u0 = np.exp(-1j*w*rstar0)
    up0 = -1j*w*u0
    def ode(r, y):
        f = 1.0 - 2.0/r
        V = V_RW(r, ell)
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

sol = root(F, [0.373, -0.09], method="hybr", tol=1e-11, options={"xtol":1e-11,"maxfev":5000})
wfound = complex(sol.x[0], sol.x[1])
print(f"RW shooting root: w = {wfound.real:.6f} {wfound.imag:+.6f}i")
print(f"Reference      :   0.373670 -0.088960i")
print(f"err = {abs(wfound-complex(0.37367,-0.08896)):.3e}")
