# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part E：符号校正后的时间谐振 Q-ball（与 E0 泛函自洽）
由 V=V1/4 f^4 - V2/6 f^6 变分得到的正确场方程：
    f'' + (2/r)f' = (Omega^2 - V1 f^2 + V2 f^4) f      (Omega = omega0/c)
大 r 处 f''+2/r f' = Omega^2 f  -> 指数衰减 f~e^{-Omega r}/r => 有限 N。
校验存在局部化正定基态，并计算 N, E0, C, M, Q0, E_specific + rmax 收敛。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

V1 = 1.2; V2 = 0.4; q0 = 1.0; c = 1.0; Omega = 0.5
r0 = 1e-9

def rhs_f(r, y):
    f, df = y
    if r < 1e-12:
        return [df, 0.0]
    return [df, (Omega**2 - V1*f**2 + V2*f**4)*f]

def solve_from(a, rmx, step=0.2):
    sol = solve_ivp(rhs_f, [r0, rmx], [a, 0.0], rtol=1e-12, atol=1e-14, max_step=step, dense_output=True)
    return sol

def f_end(a, rmx):
    return solve_from(a, rmx).y[0][-1]

print("=== Part E：符号校正 Q-ball 扫描（Omega=0.5, c=1）===")
print(" a      f_end(40)   min f   max f")
prev = None; cands = []
for a in np.arange(0.1, 3.01, 0.1):
    sol = solve_from(a, 40)
    f = sol.y[0]; fe = f[-1]; fm = f.min(); fx = f.max()
    print(f"{a:5.2f}   {fe:+.3e}   {fm:+.2e}  {fx:.3e}")
    if prev is not None and prev[0]*fe < 0:
        cands.append((prev[1], a))
    prev = (fe, a)

print("\n变号区间:", [(round(x,2),round(y,2)) for x,y in cands])
# 求根并筛选正定、已衰减到 0 的候选
def compute(a_root, rmx):
    sol = solve_from(a_root, rmx, step=0.1)
    r = sol.t; f = sol.y[0]; df = sol.y[1]
    N = 4*np.pi*np.trapezoid(r**2*f**2, r)
    E0_sub = 4*np.pi*np.trapezoid(r**2*(0.5*df**2 + V1/4*f**4 - V2/6*f**6), r)
    E0_phys = E0_sub + 4*np.pi*np.trapezoid(r**2*(0.5*Omega**2*f**2), r)
    numC = 4*np.pi*np.trapezoid(r**2*(f**2*(3*V1*f**2 - 5*V2*f**4)*r**2), r)
    C = numC / N
    return dict(rmax=rmx, a=a_root, N=N, E0_sub=E0_sub, E0_phys=E0_phys, C=C,
                Q0=q0*Omega*N, M_sub=E0_sub/c**2, M_phys=E0_phys/c**2,
                E_spec_sub=E0_sub/N, E_spec_phys=E0_phys/N)

roots = []
for lo_, hi_ in cands:
    try:
        a_ = brentq(lambda a: f_end(a, 40), lo_, hi_, xtol=1e-13)
        # 检查正定
        f = solve_from(a_, 40).y[0]
        if f.min() >= 0 and abs(f[-1]) < 1e-4:
            roots.append(a_)
    except ValueError:
        pass
roots = sorted(set(round(x,13) for x in roots))
print("正定衰减根:", [f"{x:.8f}" for x in roots])

if roots:
    print("\n=== 守恒量（符号校正 Q-ball, Omega=0.5, c=1）===")
    for a_ in roots[:2]:
        print(f"\n-- a_c = {a_:.10f} --")
        for rmx in [15, 25, 40, 60]:
            d = compute(a_, rmx)
            print(f"  rmax={rmx:3d}: N={d['N']:.8e} E0_sub={d['E0_sub']:.8e} "
                  f"C={d['C']:.8e} Q0={d['Q0']:.8e} M_sub={d['M_sub']:.8e} "
                  f"E_spec_sub={d['E_spec_sub']:.8e}")
else:
    print("未找到正定衰减基态——需扩大扫描或调整参数。")
