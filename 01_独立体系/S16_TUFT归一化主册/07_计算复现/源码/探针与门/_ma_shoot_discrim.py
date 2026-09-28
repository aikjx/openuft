# -*- coding: utf-8 -*-
"""_ma_shoot_discrim.py — RW scalar (s=0) shooting discrimination
判别实验：shooting + 已知 RW 标量势（v24 已验证），能否复现门 A 靶 w0？
YES -> V_H 组装有错（shooting 方法 OK）
NO  -> shooting 本身对 QNM 数值不稳（谱/连分数才是正路）
"""
import numpy as np
import math, sys, time
sys.path.insert(0, r'D:\a10\aikjx\code\my_lib')
from scipy.integrate import solve_ivp

w0 = 0.37367168441804166 - 0.08896231568893410j   # l=2 scalar RW QNM

def V_RW(r, w):
    """标量 s=0 Schwarzschild RW 势（v24 同款）：l=2, V=f(l(l+1)/r^2 + f'/r)"""
    f = 1.0 - 2.0/r
    return f*(6.0/r**2 - 2.0/(r*r*r)*1.0)  # f'=2/r^2, V=f(6/r^2 + 2/r^3)

def rhs(r, y, w):
    R, Rp = y
    dV = 1.0 - 2.0/r
    return [Rp, ((2.0*r-2.0)/(r*(r-2.0))*Rp - V_RW(r, w)/(r*(r-2.0))*R)]

def match_RW(w, eps=1e-4, Rmax=200.0):
    r0 = 2.0*(1.0 + 1e-6)
    dr0 = r0 - 2.0
    # 视界入波：s=0 -> xi=-i sigma+, sigma+ = 2w（a=0,rp=2,rm=0 => sigma+=2w*2/2=2w? 核对）
    # Leaver scalar: xi=-i sigma+, sigma+=(2w rp)/(rp-rm)=2w*2/2=2w => xi=-2iw
    rho = -2j*w
    R0 = dr0**rho
    Rp0 = rho*dr0**(rho-1.0)
    sol = solve_ivp(lambda r, y: rhs(r, y, w), (r0, Rmax), [R0, Rp0],
                    rtol=1e-12, atol=1e-14, method='DOP853',
                    dense_output=True, max_step=2.0)
    if not sol.success:
        return 1e30
    R_f, Rp_f = sol.y[0,-1], sol.y[1,-1]
    # 无穷远出射 s=0: R ~ r^{-1} e^{iwr}（QNM 出射波）=> R'/R = iw - 1/r
    target = 1j*w - 1.0/Rmax
    return Rp_f/R_f - target

print("== 判别实验：shooting + 标量 RW 势 ==")
t0=time.time()
mm = abs(match_RW(w0))
print("  |match_RW(w0)| = %.3e  (%.1f s)" % (mm, time.time()-t0))
print("  若 ~0 => shooting 方法 OK，问题在 V_H 组装")
print("  若 ~O(0.1-1) => shooting 对 QNM 数值不稳，谱/连分数为正路")
