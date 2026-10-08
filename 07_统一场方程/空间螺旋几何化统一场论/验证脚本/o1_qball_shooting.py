# -*- coding: utf-8 -*-
"""电荷约束 Q-ball 求解器 —— 全维度统一场论短期①路径
15A 结论：来稿静态(ω=0)方程尾=√3 凝聚态，N∝r³ 体积发散，无有限 N 局域孤子。
关键：Q-ball 是时间依赖 ψ=e^{-iωt}φ(r)，ω>0 给尾指数衰减 e^{-ωr}/r → 可能局域化。
符号自洽模型（15A 修正）：场方程 ∂²ψ = -V1|ψ|²ψ + V2|ψ|⁴ψ
  能量 E0=∫[½|∇ψ|² + V1/4|ψ|⁴ - V2/6|ψ|⁶]d³x
Q-ball 方程：φ'' + 2φ'/r = ω²φ - V1φ³ + V2φ⁵,  φ'(0)=0, φ(∞)→0
存在条件 ω²≤V1²/(4V2)。V1=1.2,V2=0.4 → ω≤0.949
"""
import numpy as np
from scipy.integrate import solve_ivp

V1=1.2; V2=0.4

def rhs(r, y, w2):
    phi, dphi = y
    if r < 1e-12:
        # φ''(0)=(w2·φ - V1φ³+V2φ⁵)/3（由 2φ'/r→2φ''(0)）
        d2 = (w2*phi - V1*phi**3 + V2*phi**5)/3.0
        return [0.0, d2]
    d2 = w2*phi - V1*phi**3 + V2*phi**5 - 2*dphi/r
    return [dphi, d2]

def shoot(phi0, w2, rmax=20.0, npts=4000):
    """对给定 ω，从中心 φ(0)=phi0 积分，返回尾值 φ(rmax)"""
    sol = solve_ivp(rhs, (0, rmax), [phi0, 0.0], args=(w2,),
                    t_eval=np.linspace(0, rmax, npts), rtol=1e-10, atol=1e-13)
    return sol

print("== Q-ball 打靶：找 φ(0) 使尾衰减到 0 ==")
print(f"存在条件 ω≤sqrt(V1²/4V2)=sqrt({V1**2/(4*V2):.3f})={np.sqrt(V1**2/(4*V2)):.3f}\n")

results = {}
for w in [0.95, 0.9, 0.8, 0.7, 0.5, 0.3]:
    w2 = w*w
    # 中心值扫描范围：由 φ''(0)<0 需 w2 - V1A²+V2A⁴ < 0
    # 初选 A 区间，打靶找尾趋于 0
    found = None
    for A in np.linspace(1.05, 2.0, 30):
        sol = shoot(A, w2)
        tail = abs(sol.y[0][-1])
        # 找尾最小（衰减最彻底）
        if found is None or tail < found[1]:
            found = (A, tail, sol)
    A, tail, sol = found
    results[w] = (A, tail, sol)
    print(f" ω={w:.2f}: 最优中心 φ(0)={A:.4f}, |φ(rmax)|={tail:.3e}")

# 详细看 ω=0.7（中等），算物理量
print("\n== 物理量计算（ω=0.7, 最优解）==")
w = 0.7; w2 = w*w
A, tail, sol = results[w]
r = sol.t; phi = sol.y[0]; dphi = sol.y[1]
rmax = r[-1]
# 数值积分（梯形，含 r² 加权）
def integ(f):
    return np.trapezoid(f, r)
N  = integ(4*np.pi*r**2*phi**2)
Q  = w*N
E  = integ(4*np.pi*r**2*(0.5*dphi**2 + 0.5*w2*phi**2 + V1/4*phi**4 - V2/6*phi**6))
Esp = E/N
Cnum = integ(4*np.pi*r**2*phi**2*(3*V1*phi**2 - 5*V2*phi**4)*r**2)
C = Cnum/N
print(f" N(范数)={N:.6e}, Q(电荷)=w·N={Q:.6e}")
print(f" E(静能)={E:.6e}, 比能量 Esp=E/N={Esp:.6e}")
print(f" 形状系数 C={C:.6e}")
print(f" 尾(rmax={rmax}) |φ|={abs(phi[-1]):.3e} → 指数衰减确认: {'✅ 局域化' if abs(phi[-1])<1e-3 else '⚠ 未完全衰减'}")

# ω 依赖扫描
print("\n== ω 依赖（Q-ball 解族）==")
for w, (A, tail, sol) in results.items():
    r = sol.t; phi=sol.y[0]; dphi=sol.y[1]
    N = np.trapezoid(4*np.pi*r**2*phi**2, r)
    Q = w*N
    E = np.trapezoid(4*np.pi*r**2*(0.5*dphi**2+0.5*w*w*phi**2+V1/4*phi**4-V2/6*phi**6), r)
    print(f" ω={w:.2f}: φ(0)={A:.4f}, N={N:.4e}, Q={Q:.4e}, E={E:.4e}, E/N={E/N:.4e}")
