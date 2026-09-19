# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

# Riccati: h = du/dr* / u,  dh/dr* = (V - w^2) - h^2
# horizon: h = -iw (ingoing); infinity: h -> +iw (outgoing)
# 在 r 里: dh/dr = (dr*/dr)^{-1} [(V-w^2)-h^2] = f[(V-w^2)-h^2]

def V_RW(r, ell=2):
    f = 1.0 - 2.0/r
    return f*(ell*(ell+1)/r**2 - 6.0/r**3)

def V_scalar(r, ell=2):
    f = 1.0 - 2.0/r
    return f*ell*(ell+1)/r**2

def riccati_residual(w, Vfunc, ell=2, r0=2.0001, r_end=500.0):
    # h0 = -iw at horizon (ingoing)
    h0 = -1j*w
    def ode(r, h):
        f = 1.0 - 2.0/r
        V = Vfunc(r, ell)
        return [f*(V - w*w - h[0]**2)]
    sol = solve_ivp(ode, (r0, r_end), [h0], t_eval=[r_end],
                    method="DOP853", rtol=1e-11, atol=1e-13)
    h_end = sol.y[0,-1]
    # infinity outgoing: h -> +iw
    return h_end - 1j*w

for name, Vf in [("RW", V_RW), ("scalar", V_scalar)]:
    def F(x, Vf=Vf):
        w = complex(x[0], x[1])
        r = riccati_residual(w, Vf)
        return [r.real, r.imag]
    sol = root(F, [0.373, -0.09], method="hybr", tol=1e-12,
               options={"xtol":1e-12,"maxfev":8000})
    wf = complex(sol.x[0], sol.x[1])
    print(f"{name}: w = {wf.real:.6f}{wf.imag:+.6f}i  err vs 0.37367-0.08896i = {abs(wf-complex(0.37367,-0.08896)):.3e}")
