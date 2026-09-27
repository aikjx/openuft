# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part G：正确有下界势 Q-ball，定位紧凑干净基态并算守恒量
方程：f'' + (2/r)f' = (Omega^2 - V1 f^2 - V2p f^4) f
提高 Omega 使孤子更紧凑；找 f>0、在 rmax 内已指数衰减（f_end<<1）的局部化解；
对选定的干净基态计算 N, E0, M, C, Q0, Espec 并做 rmax 收敛。
"""
import numpy as np
from scipy.integrate import solve_ivp

V1 = 1.2; V2p = 0.4; q0 = 1.0; c = 1.0
r0 = 1e-9

def rhs_f(r, y):
    f, df = y
    if r < 1e-12:
        return [df, 0.0]
    return [df, (Omega**2 - V1*f**2 - V2p*f**4)*f]

def run(a, rmx, step=0.2):
    sol = solve_ivp(rhs_f, [r0, rmx], [a, 0.0], rtol=1e-11, atol=1e-13, max_step=step, dense_output=True)
    return sol

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

print("=== Part G：紧凑干净基态定位（Omega 扫描）===")
best = None
for Om in [0.6, 0.7, 0.8, 0.9]:
    Omega = Om
    found = None
    for a in np.arange(0.2, 2.6, 0.02):
        sol = run(a, 50)
        f = sol.y[0]
        if f.min() >= 0 and abs(f[-1]) < 1e-6:  # 正定 + 已衰减
            found = (a, f.max(), f[-1])
            break
    if found:
        a, fmax, fe = found
        print(f"Omega={Om}: 紧凑基态 a_c={a:.4f}, max f={fmax:.4f}, f(50)={fe:.1e}  <-- 干净局部化")
        best = (Om, a)
        break
    else:
        print(f"Omega={Om}: 0.2~2.6 内未找到 f>0 且在 r=50 衰减到<1e-6 的解")

if best is None:
    # 若都没有，放宽到更细扫描 + 更大 rmax
    print("\n放宽判据重扫...")
    for Om in [0.6,0.7,0.8]:
        Omega = Om
        for a in np.arange(0.2,2.6,0.005):
            sol = run(a,80)
            f=sol.y[0]
            if f.min()>=0 and abs(f[-1])<1e-5:
                print(f"Omega={Om}: 候选 a={a:.4f} f(80)={f[-1]:.1e}"); best=(Om,a); break
        if best: break

if best:
    Om, a_c = best
    Omega = Om
    print(f"\n=== 守恒量（Omega={Om}, a_c={a_c:.4f}, c=1, V2p=0.4）===")
    for rmx in [25, 50, 80, 120]:
        d = compute(a_c, rmx)
        print(f"  rmax={rmx:4d}: N={d['N']:.8e} E0={d['E0']:.8e} E0_ph={d['E0_ph']:.8e} "
              f"C={d['C']:.8e} Q0={d['Q0']:.8e} M={d['M']:.8e} M_ph={d['M_ph']:.8e}")
else:
    print("未定位到干净基态（需再调参）")
