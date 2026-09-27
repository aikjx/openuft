# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part D：有下界势 Q-ball 基态正定性诊断
判据：基态 Q-ball 的 f(r)>0 恒成立、f'(0)=0、f 单调衰减到 0（不穿越零点、指数尾）。
对 Omega 与振幅 a 扫描，找满足条件的解；若存在则算守恒量并做 rmax 收敛。
"""
import numpy as np
from scipy.integrate import solve_ivp

V1 = 1.2; V2p = 0.4; q0 = 1.0; c = 1.0
Omega = 0.5
r0 = 1e-9; rmax = 80.0

def rhs_f(r, y):
    f, df = y
    if r < 1e-12:
        return [df, 0.0]
    return [df, (V1*f**2 + V2p*f**4 - Omega)*f]

def integ(a, Om, rmx, step=0.25):
    global Omega
    Omega = Om
    sol = solve_ivp(rhs_f, [r0, rmx], [a, 0.0], rtol=1e-11, atol=1e-13, max_step=step, dense_output=True)
    r = sol.t; f = sol.y[0]
    return r, f

print("=== Part D：基态 Q-ball 正定性诊断（有下界势 V1=1.2, V2p=0.4）===")
for Om in [0.2, 0.3, 0.4, 0.5, 0.6]:
    found = None
    print(f"\n-- Omega={Om} --")
    for a in np.arange(0.01, 0.5, 0.01):
        r, f = integ(a, Om, rmax)
        fmin = f.min()
        # 正定性 + 已衰减到接近0 + 尾端幅值很小
        if fmin >= 0 and f[-1] < 1e-3 and f[-1] > -1e-3:
            if f[0] > 1e-6:  # 非平凡
                found = (a, fmin, f[-1], f.max())
                break
    if found:
        a, fmin, fend, fmax = found
        print(f"  找到正定衰减候选: a={a:.4f}, min f={fmin:.2e}, f(rmax)={fend:.2e}, max f={fmax:.4f}")
    else:
        print("  0.01~0.50 内未找到 f>0 且衰减到~0 的基态候选")
