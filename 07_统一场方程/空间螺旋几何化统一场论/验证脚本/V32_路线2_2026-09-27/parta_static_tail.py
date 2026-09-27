# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part A：来稿静态径向方程可解性/局域性检验
方程：psi'' + (2/r)psi' = V1 psi^3 - V2 psi^5  （V1=1.2, V2=0.4）
判据：局域有限范数孤子要求 psi(r) 衰减快于 r^{-3/2}。
渐近分析预告：r 大时三次项主导 -> psi ~ A/r -> r^2 psi^2 -> A^2 = 常数，
N = 4pi*int r^2 psi^2 dr ~ 4pi*A^2*rmax 发散。
本脚本数值验证该预告（用 u = r psi 消奇点）。
"""
import numpy as np
from scipy.integrate import solve_ivp

V1 = 1.2; V2 = 0.4

def rhs(r, y):
    u, du = y
    if r < 1e-12:
        return [du, 0.0]
    return [du, (V1*u**3 - V2*u**5) / r**2]

r0 = 1e-8
rmax = 5e4

def shoot(a):
    """a = psi(0)。u≈a r 起步。"""
    u0 = a*r0
    du0 = a + 0.5*(V1*a**3 - V2*a**5)*r0**2
    sol = solve_ivp(rhs, [r0, rmax], [u0, du0],
                    rtol=1e-11, atol=1e-13, dense_output=True)
    r = sol.t; u = sol.y[0]
    psi = u / r
    return r, psi, sol

# 扫描中心振幅，观察尾部行为与范数
print("=== Part A: 来稿静态方程（无频率项）===")
for a in [0.5, 0.75, 1.0, 1.5]:
    r, psi, sol = shoot(a)
    # psi*r 应趋于常数 A
    idx = (r > 1e3) & (r < 5e4)
    if idx.sum() > 0:
        A = np.mean(psi[idx]*r[idx])
        # 累积范数 N(rmax)
        N = 4*np.pi*np.trapezoid(r**2 * psi**2, r)
        # 尾部 r^2 psi^2 是否 -> 常数
        tail = (r**2*psi**2)[-1]
        print(f"a={a:5.2f}: psi(0)=a, psi*r -> A≈{A:+.4e}, "
              f"r^2 psi^2(r=rmax)≈{tail:.4e}, N(rmax={rmax:g})≈{N:.3e}")
    else:
        print(f"a={a:5.2f}: 未积分到远端（发散/振荡）")

# 特写：展示 r^2 psi^2 是否趋于常数（若趋于常数 -> N 对数/线性发散）
a = 0.75
r, psi, sol = shoot(a)
r_chk = np.geomspace(1e2, 5e4, 6)
psi_chk = np.array([sol.sol(rr)[0]/rr for rr in r_chk])
print("\n局部性检查（a=0.75）:  r^2*psi^2 随 r 变化")
for rr, pc in zip(r_chk, psi_chk):
    print(f"  r={rr:9.3g}:  psi(r)={pc:.4e}   r^2 psi^2={rr**2*pc**2:.6e}")
