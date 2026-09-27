# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part H（终版）：双阱势 Q-ball，定位干净基态并算守恒量
作用量 L = 0.5|∂_μψ|² - V(|ψ|),  V = 0.5 m²φ² - 0.25 λφ⁴ + (1/6)ηφ⁶  (双阱，真真空 φ=1)
正确场方程：φ'' + (2/r)φ' = (m²-ω²)φ - λφ³ + ηφ⁵   （尾衰减需 m²>ω²）
参数 m²=1, λ=5, η=4, q0=1, c=1。
"""
import numpy as np
from scipy.integrate import solve_ivp
m2=1.0; lam=5.0; eta=4.0; q0=1.0; c=1.0; r0=1e-9

def rhs_f(r,y,om):
    f,df=y
    if r<1e-12: return [df,0.0]
    return [df, (m2-om**2)*f - lam*f**3 + eta*f**5]

def run(a, rmx, om, step=0.35):
    return solve_ivp(rhs_f,[r0,rmx],[a,0.0],rtol=1e-11,atol=1e-13,max_step=step,dense_output=True,args=(om,))

def compute(a_root, rmx, om, step=0.12):
    sol=run(a_root,rmx,om,step)
    r=sol.t; f=sol.y[0]; df=sol.y[1]
    N =4*np.pi*np.trapezoid(r**2*f**2,r)
    E0=4*np.pi*np.trapezoid(r**2*(0.5*df**2 + 0.5*m2*f**2 - lam/4*f**4 + eta/6*f**6),r)
    E0_ph=E0+4*np.pi*np.trapezoid(r**2*(0.5*om**2*f**2),r)
    # 形状系数 C：重构势二阶结构类比（🟡）; 用 V 的 Hessian 权重 (m²-3λφ²+5ηφ⁴)·φ²·r²
    numC=4*np.pi*np.trapezoid(r**2*(f**2*(m2 - 3*lam*f**2 + 5*eta*f**4)*r**2),r)
    C=numC/N
    return dict(rmax=rmx,a=a_root,N=N,E0=E0,E0_ph=E0_ph,C=C,
                Q0=q0*om*N,M=E0/c**2,M_ph=E0_ph/c**2,Espec=E0/N,Espec_ph=E0_ph/N)

# 真真空
s=(-lam+np.sqrt(lam**2+4*eta*m2))/(2*eta)  # m²-λs+ηs²=0 的较大根 -> φ²
f_true=np.sqrt(max(s,0))
Vtv=0.5*m2*s - lam/4*s**2 + eta/6*s**3
print(f"双阱势: m²=1,λ=5,η=4; 真真空 φ_true={f_true:.4f}, V(φ_true)={Vtv:+.4f}")

print("=== Part H：双阱 Q-ball 干净基态定位 ===")
hits={}
for om in [0.3,0.5,0.7,0.9]:
    for a in np.arange(0.20,1.60,0.002):
        sol=run(a,50,om)
        f=sol.y[0]
        if f.min()>0 and abs(f[-1])<1e-6:
            hits[om]=(a,f.max(),f[-1])
            print(f"  ω={om}: 干净基态 a_c={a:.4f}, max f={f.max():.4f}, f(50)={f[-1]:.1e}")
            break
    if om not in hits:
        print(f"  ω={om}: 0.20~1.60 内未找到")

if hits:
    # 展示全部命中 + 对每个算守恒量（选 max f 最靠近真真空的）
    print("\n=== 守恒量（各命中，rmax 收敛）===")
    for om,(a,_,_) in hits.items():
        print(f"--- ω={om}, a_c={a:.4f} ---")
        for rmx in [30,50,80,120]:
            d=compute(a,rmx,om)
            print(f"   rmax={rmx:3d}: N={d['N']:.6e} E0={d['E0']:+.6e} E0_ph={d['E0_ph']:.6e} "
                  f"C={d['C']:+.6e} Q0={d['Q0']:.6e} M={d['M']:+.6e} Espec={d['Espec']:+.6e}")
