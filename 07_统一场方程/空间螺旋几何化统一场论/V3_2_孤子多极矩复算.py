# -*- coding: utf-8 -*-
# TUFT V3.2 孤子电磁多极矩与径向矩量化（球对称→仅单极；形状修正C无辐射通道）
# 结论（对照同目录 15B 文档 §6B）：ρ=q0ω0f(r)² 球对称且无电流 => 除总电荷Q0外所有电磁多极矩为0，
# 刚性绝热辐射恒为点电荷Larmor P=(Q0²/6πε0c³)γ⁴a²；C=num_C/N≈12.85 是场能加权径向二次矩比值，
# 非标准电磁多极矩，刚体模型内无辐射通道。
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
V1,V2=1.2,0.4; c=299792458.0; eps0=8.8541878128e-12
q0=1.0; omega0=0.2; r_max=40.0

def rhs(r,y):
    psi,dpsi=y
    d2=-(2.0/r)*dpsi - V1*psi**3 + V2*psi**5 if r>1e-12 else -V1*psi**3+V2*psi**5
    return [dpsi,d2]
def shoot(psi0): return solve_ivp(rhs,[0,r_max],[psi0,0.0],rtol=1e-13,atol=1e-14,dense_output=True).sol(r_max)[0]
psi0=brentq(shoot,0.75,0.80,xtol=1e-14)
sol=solve_ivp(rhs,[0,r_max],[psi0,0.0],rtol=1e-13,atol=1e-14,dense_output=True)
pf=lambda r: sol.sol(r)
print(f"psi0={psi0}")
def q(r): return q0*omega0*abs(pf(r)[0])**2

N,_=quad(lambda r:4*np.pi*r**2*abs(pf(r)[0])**2,0,r_max,limit=500)
Q0=q0*omega0*N
print(f"N={N}  Q0={Q0}")
r1,_=quad(lambda r: r*q(r)*4*np.pi*r**2, 0,r_max,limit=500)
r2,_=quad(lambda r: r*r*q(r)*4*np.pi*r**2,0,r_max,limit=500)
print(f"<r>_rho = {r1/Q0:.6e}   <r^2>_rho = {r2/Q0:.6e}")

def phi(r):
    inside,_=quad(lambda s: q(s)*4*np.pi*s**2,0,r,limit=300)
    outside,_=quad(lambda s: q(s)*4*np.pi*s, r,r_max,limit=300)
    return 1/(4*np.pi*eps0)*(inside/r + outside)
Eem,_=quad(lambda r: 0.5*q(r)*phi(r)*4*np.pi*r**2,0,r_max,limit=300)
print(f"E_em = {Eem:.6e}  (长度标度未锚定,仅示意)")

def Cnumf(r):
    p=abs(pf(r)[0]); return 4*np.pi*r**2*( (p*p)*(3*V1*(p*p)-5*V2*(p*p)**2)*r**2 )
Cnum,_=quad(Cnumf,0,r_max,limit=500)
print(f"C = num_C/N = {Cnum/N:.6f}")
