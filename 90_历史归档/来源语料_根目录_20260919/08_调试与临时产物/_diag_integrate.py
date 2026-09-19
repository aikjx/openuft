# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import solve_ivp

# 直接在 r* 里积分 Schwarzschild 标量方程
# d2u/dr*2 + (w^2 - V) u = 0, V = f(l(l+1)/r^2 + f'/r), f=1-2/r
# r* = r + 2 ln(r/2 - 1), dr*/dr = 1/f

def V_of_r(r, ell=2):
    f = 1.0 - 2.0/r
    fp = 2.0/r**2
    return f*(ell*(ell+1)/r**2 + fp/r)

def ode_rstar(r, y, w, ell=2):
    f = 1.0 - 2.0/r
    V = V_of_r(r, ell)
    # y=[u, du/dr*]
    # d/dr* = f d/dr;  du/dr* = f du/dr
    # d2u/dr*2 = (w^2 - V) u
    # 用 r 作自变量: du/dr = (1/f) du/dr*;  d(du/dr*)/dr = (1/f) d2u/dr*2
    # y[1] = du/dr*;  dy[1]/dr = (1/f)(V - w^2) u
    return [y[1]/f, (V - w*w)*y[0]/f]

# 从近 horizon 开始: r=2.01, u=e^{-iw r*}, du/dr*=-iw u
r_h = 2.0
r0 = 2.001
# r*(r0) = r0 + 2 ln(r0/2 - 1)
rstar0 = r0 + 2*np.log(r0/2 - 1)
w = complex(0.37367, -0.08896)
u0 = np.exp(-1j*w*rstar0)
up0 = -1j*w*u0

sol = solve_ivp(ode_rstar, (r0, 50.0), [u0, up0], args=(w,),
                t_eval=np.linspace(r0, 50.0, 5000), method="DOP853",
                rtol=1e-10, atol=1e-12)
u = sol.y[0]
rlast = sol.t[-1]
ulast = u[-1]
# 渐近: u ~ A_out e^{+iw r*} + A_in e^{-iw r*}
rstar_last = rlast + 2*np.log(rlast/2 - 1)
# du/dr* = sol.y[1,-1]
up_last = sol.y[1,-1]
# A_in = (u + i/w du/dr*) / (2 e^{-iw r*})
A_in = (ulast + (1j/w)*up_last) * np.exp(1j*w*rstar_last)/2
A_out = (ulast - (1j/w)*up_last) * np.exp(-1j*w*rstar_last)/2
print(f"At r={rlast:.2f}: |u|={abs(ulast):.4e}")
print(f"|A_out|={abs(A_out):.4e}  |A_in|={abs(A_in):.4e}")
print(f"ratio |A_in/A_out| = {abs(A_in/A_out):.4e}  (QNM => ~0)")
