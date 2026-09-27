# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part I：后向打靶求双阱 Q-ball 干净基态
正确场方程：φ'' + (2/r)φ' = (m²-ω²)φ - λφ³ + ηφ⁵,  m²=1,λ=5,η=4
尾模式 φ ~ A e^{-κ r}/r, κ=√(m²-ω²);  φ'(R) = -φ(R)(κ + 1/R)
后向积分到 r0，根寻使 φ'(r0)=0（中心光滑）。r 方向用 -r（从 R 到 0）。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
m2=1.0; lam=5.0; eta=4.0; q0=1.0; c=1.0

def deriv(s, y, om, kappa):
    # 沿 r 积分，从大到小：dφ/dr, dφ'/dr
    f, df = y
    return [df, (m2-om**2)*f - lam*f**3 + eta*f**5 - (2/s)*df]

def shoot_center(eps, om, R):
    kappa=np.sqrt(max(m2-om**2,1e-12))
    y0=[eps, -eps*(kappa+1.0/R)]
    sol=solve_ivp(deriv,[R,r0],[*y0],t_eval=None,rtol=1e-12,atol=1e-14,max_step=0.2,
                  args=(om,kappa),dense_output=True)
    f0,df0=sol.sol(1e-8)
    return df0   # 中心导数，目标=0

r0=1e-6
R=40.0

def center_amplitude(om, eps_lo, eps_hi):
    def resid(eps): return shoot_center(eps, om, R)
    # 先求符号变化区间
    a,b=eps_lo,eps_hi
    try:
        eps=brentq(resid, a, b, xtol=1e-13, rtol=1e-12)
        return eps
    except ValueError as e:
        return None

print("=== Part I：后向打靶 Q-ball（m²=1, λ=5, η=4）===")
for om in [0.3,0.5,0.7,0.9]:
    kappa=np.sqrt(max(m2-om**2,1e-12))
    eps=center_amplitude(om, 1e-12, 5e-5)
    if eps is None:
        # 扩展上界
        eps=center_amplitude(om, 1e-12, 1e-2)
    if eps is None:
        print(f"  ω={om}: 未找到中心正则解 (κ={kappa:.3f})")
        continue
    # 用找到的 ε 重建完整轮廓（前向 + 后向拼接）
    sol_fwd=solve_ivp(lambda r,y: [y[1],(m2-om**2)*y[0]-lam*y[0]**3+eta*y[0]**5-(2/r)*y[1]],
                      [r0,R],[eps,0.0],rtol=1e-12,atol=1e-14,max_step=0.2,dense_output=True)
    r=sol_fwd.t; f=sol_fwd.y[0]; df=sol_fwd.y[1]
    a_c=f[0]
    N =4*np.pi*np.trapezoid(r**2*f**2,r)
    E0=4*np.pi*np.trapezoid(r**2*(0.5*df**2+0.5*m2*f**2-lam/4*f**4+eta/6*f**6),r)
    E0_ph=E0+4*np.pi*np.trapezoid(r**2*(0.5*om**2*f**2),r)
    numC=4*np.pi*np.trapezoid(r**2*(f**2*(m2-3*lam*f**2+5*eta*f**4)*r**2),r)
    C=numC/N
    print(f"  ω={om} (κ={kappa:.3f}): ε={eps:.3e}, a_c=φ(0)={a_c:.6f}, f(R)={f[-1]:.2e}")
    print(f"     N={N:.6e}  E0={E0:+.6e}  E0_ph={E0_ph:.6e}  C={C:+.6e}")
    print(f"     Q0={q0*om*N:.6e}  M=E0/c²={E0:+.6e}  Espec={E0/N:+.6e}")
