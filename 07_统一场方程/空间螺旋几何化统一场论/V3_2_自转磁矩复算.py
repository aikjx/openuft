# -*- coding: utf-8 -*-
# TUFT V3.2 —— 自转孤子内禀电流 -> 磁偶极矩 μ 与 g 因子（检验是否依赖场形状 C）
# 结论（对照 15B §6D）：质荷同形 + 非相对论刚体自转 => μ=(Q/2M)L => g=2，
# 径向矩 I4 在比值中消去，C 不进入 g，也不产生反常磁矩 g-2。形状相关 g 修正需
# 破坏质荷同形（相对论自转/荷质独立剖面）。
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
V1,V2=1.2,0.4; r_max=40.0; q0=1.0; omega0=0.2
def rhs(r,y):
    psi,dpsi=y
    d2=-(2.0/r)*dpsi - V1*psi**3 + V2*psi**5 if r>1e-12 else -V1*psi**3+V2*psi**5
    return [dpsi,d2]
def shoot(p): return solve_ivp(rhs,[0,r_max],[p,0.0],rtol=1e-13,atol=1e-14,dense_output=True).sol(r_max)[0]
psi0=brentq(shoot,0.75,0.80,xtol=1e-14)
sol=solve_ivp(rhs,[0,r_max],[psi0,0.0],rtol=1e-13,atol=1e-14,dense_output=True)
pf=lambda r: sol.sol(r)
f2=lambda r: abs(pf(r)[0])**2
N,_=quad(lambda r:4*np.pi*r**2*f2(r),0,r_max,limit=500)
Q=q0*omega0*N
rho=lambda r: q0*omega0*f2(r)
I4=quad(lambda r: rho(r)*r**4,0,r_max,limit=500)[0]
mu_over_Omega=0.5*(4*np.pi/3.0)*I4
r2mom,_=quad(lambda r: r*r*rho(r)*4*np.pi*r**2,0,r_max,limit=500)
print(f"psi0={psi0}")
print(f"N={N}  Q={Q}")
print(f"I4=∫ρ r⁴ dr = {I4:.6e}")
print(f"μ_z/Ω = {mu_over_Omega:.6e}")
print(f"<r²>_ρ = {r2mom/Q:.6e} ; 均匀球 μ/Ω=Q<r²>/5 = {Q*(r2mom/Q)/5:.6e}")
print("质荷同形刚体自转: μ=(Q/2M)L => g=2 (形状矩 I4 在比值中消去, C 不进入 g)")
