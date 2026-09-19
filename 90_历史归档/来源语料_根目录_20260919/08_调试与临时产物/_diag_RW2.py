# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

def V_RW(r, ell=2):
    f = 1.0 - 2.0/r
    return f*(ell*(ell+1)/r**2 - 6.0/r**3)

def shoot(w, ell=2, r0=2.0001, r_end=200.0):
    rstar0 = r0 + 2*np.log(r0/2 - 1)
    u0 = np.exp(-1j*w*rstar0)
    up0 = -1j*w*u0
    def ode(r, y):
        f = 1.0 - 2.0/r
        V = V_RW(r, ell)
        return [y[1]/f, (V - w*w)*y[0]/f]
    sol = solve_ivp(ode, (r0, r_end), [u0, up0], t_eval=[r_end],
                    method="DOP853", rtol=1e-12, atol=1e-14)
    ulast = sol.y[0,-1]; up_last = sol.y[1,-1]
    rstar_last = r_end + 2*np.log(r_end/2 - 1)
    A_in = (ulast + (1j/w)*up_last) * np.exp(1j*w*rstar_last)/2
    return A_in

# 扫描附近
for wtry in [complex(0.37367,-0.08896), complex(0.38,-0.09), complex(0.37,-0.10)]:
    ain = shoot(wtry)
    print(f"w={wtry}: |A_in|={abs(ain):.4e}")

def F(x):
    w = complex(x[0], x[1])
    r = shoot(w)
    return [r.real, r.imag]

for guess in [[0.373,-0.09],[0.38,-0.09],[0.37,-0.10],[0.39,-0.08]]:
    try:
        sol = root(F, guess, method="hybr", tol=1e-12, options={"xtol":1e-12,"maxfev":8000})
        wf = complex(sol.x[0], sol.x[1])
        print(f"guess={guess} -> root: {wf.real:.6f}{wf.imag:+.6f}i  err={abs(wf-complex(0.37367,-0.08896)):.3e}")
    except Exception as e:
        print(guess, "fail", e)
