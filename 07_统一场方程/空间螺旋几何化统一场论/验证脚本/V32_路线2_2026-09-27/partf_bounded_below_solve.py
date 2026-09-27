# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part F：正确有下界势 Q-ball 基态求解
势 V(f)=V1/4 f^4 + V2p/6 f^6（V2p>0 => 有下界，基态为真极值而非鞍点）
由 V 变分（∂_μ∂^μψ = -V'ψ）并代入 ψ=f e^{-iωt} 得正确方程：
    f'' + (2/r)f' = (Omega^2 - V1 f^2 - V2p f^4) f ,  f'(0)=0, f(∞)=0
大 r: f''+2/r f' = Omega^2 f -> 指数衰减 e^{-Omega r}/r => 有限 N。
目标：稳健打靶出正定衰减基态，计算 N, E0, M, C, Q0, E_specific + rmax 收敛。
"""
import numpy as np
from scipy.integrate import solve_ivp

V1 = 1.2; V2p = 0.4; q0 = 1.0; c = 1.0; Omega = 0.5
r0 = 1e-9

def rhs_f(r, y):
    f, df = y
    if r < 1e-12:
        return [df, 0.0]
    return [df, (Omega**2 - V1*f**2 - V2p*f**4)*f]

def run(a, rmx, step=0.2):
    sol = solve_ivp(rhs_f, [r0, rmx], [a, 0.0], rtol=1e-11, atol=1e-13, max_step=step, dense_output=True)
    return sol

print(f"=== Part F：正确有下界势 Q-ball（V1={V1}, V2p={V2p}, Omega={Omega}, c=1）===")
print(" a      f(0)    max|f|   min f    f_end(60)  尾行为")
decayed = []
prev = None
for a in np.arange(0.30, 2.01, 0.02):
    sol = run(a, 60)
    f = sol.y[0]; fm = f.max(); fmin = f.min(); fe = f[-1]
    # 判据：全程 f>0 且尾端已衰减到很小
    mono = fmin >= 0
    tag = 'DECAY' if (mono and abs(fe) < 1e-5) else ('POS-DEC' if (mono and fe < 0.05) else ('POS' if mono else 'CROSS'))
    if tag in ('DECAY','POS-DEC'):
        decayed.append((a, fe, fm))
    print(f"{a:5.2f}  {a:6.3f}  {fm:8.4f}  {fmin:+8.4f}  {fe:9.2e}  {tag}")
    prev = (fe, a)

print("\n正定且尾端衰减候选 a:", [f"{x[0]:.3f}" for x in decayed])

def compute(a_root, rmx):
    sol = run(a_root, rmx, step=0.1)
    r = sol.t; f = sol.y[0]; df = sol.y[1]
    N = 4*np.pi*np.trapezoid(r**2*f**2, r)
    E0 = 4*np.pi*np.trapezoid(r**2*(0.5*df**2 + V1/4*f**4 + V2p/6*f**6), r)
    E0_ph = E0 + 4*np.pi*np.trapezoid(r**2*(0.5*Omega**2*f**2), r)
    numC = 4*np.pi*np.trapezoid(r**2*(f**2*(3*V1*f**2 + 5*V2p*f**4)*r**2), r)
    C = numC / N
    return dict(rmax=rmx, a=a_root, N=N, E0=E0, E0_ph=E0_ph, C=C,
                Q0=q0*Omega*N, M=E0/c**2, M_ph=E0_ph/c**2,
                Espec=E0/N, Espec_ph=E0_ph/N)

# 取最显著（最大振幅）的衰减候选做守恒量 + rmax 收敛
print("\n=== 守恒量 + 收敛检查 ===")
chosen = decayed[-1] if decayed else (1.0,)
a_c = chosen[0]
print(f"选定 a_c = {a_c:.4f}")
for rmx in [15, 30, 60, 100]:
    d = compute(a_c, rmx)
    print(f"  rmax={rmx:4d}: N={d['N']:.8e}  E0={d['E0']:.8e}  E0_ph={d['E0_ph']:.8e}  "
          f"C={d['C']:.8e}  Q0={d['Q0']:.8e}  M={d['M']:.8e}  M_ph={d['M_ph']:.8e}")
