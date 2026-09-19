# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

# 从无穷远向内积分 (稳定方向)
# 无穷远出射: u = e^{+iw r*}, du/dr* = +iw u
# 向内积分到近 horizon, 检查 horizon 是否纯入射 (e^{-iw r*})

def V_RW(r, ell=2):
    f = 1.0 - 2.0/r
    return f*(ell*(ell+1)/r**2 - 6.0/r**3)

def V_scalar(r, ell=2):
    f = 1.0 - 2.0/r
    return f*ell*(ell+1)/r**2

def shoot_inward(w, Vfunc, ell=2, r_max=300.0, r_end=2.001):
    rstar_max = r_max + 2*np.log(r_max/2 - 1)
    u0 = np.exp(1j*w*rstar_max)       # outgoing at infinity
    up0 = 1j*w*u0
    def ode(r, y):
        f = 1.0 - 2.0/r
        V = Vfunc(r, ell)
        return [y[1]/f, (V - w*w)*y[0]/f]
    sol = solve_ivp(ode, (r_max, r_end), [u0, up0], t_eval=[r_end],
                    method="DOP853", rtol=1e-12, atol=1e-14)
    ulast = sol.y[0,-1]; up_last = sol.y[1,-1]
    # horizon: 纯入射 e^{-iw r*} => du/dr* = -iw u
    # 残差: du/dr* + iw u = 0
    res = up_last + 1j*w*ulast
    return res

for name, Vf in [("RW", V_RW), ("scalar", V_scalar)]:
    def F(x, Vf=Vf):
        w = complex(x[0], x[1])
        r = shoot_inward(w, Vf)
        return [r.real, r.imag]
    sol = root(F, [0.373, -0.09], method="hybr", tol=1e-12,
               options={"xtol":1e-12,"maxfev":8000})
    wf = complex(sol.x[0], sol.x[1])
    print(f"{name}: w = {wf.real:.6f}{wf.imag:+.6f}i  err vs 0.37367-0.08896i = {abs(wf-complex(0.37367,-0.08896)):.3e}")
