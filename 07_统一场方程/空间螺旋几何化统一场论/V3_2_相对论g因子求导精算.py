# -*- coding: utf-8 -*-
# TUFT V3.2 §6F —— 相对论转动 g 偏移的求导证明 + 精算
# 闭式: γ=1+β²/2+3β⁴/8, γ²=1+β²+3β⁴/4, β=b r sinθ
#   g/2 = 2μ/L = 1 - K b² + O(b⁴),  K=(1/2)(A5/A3)(I6/I4)=(2/5)(I6/I4)
#   A3=∫sin³=4/3, A5=∫sin⁵=16/15
# 主根 ψ0≈0.7645: I4≈4.0239e4, I6≈2.6424e7 => K≈262.6678（小 b 数值外推逐位吻合）
# 物理: g<2（负号，γ vs γ² 加权不对称），与电子 g>2 相反，非电子 g−2 解释。
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
V1,V2=1.2,0.4; r_max=40.0
def rhs(r,y):
    psi,dpsi=y
    d2=-(2.0/r)*dpsi - V1*psi**3 + V2*psi**5 if r>1e-12 else -V1*psi**3+V2*psi**5
    return [dpsi,d2]
def shoot(p): return solve_ivp(rhs,[0,r_max],[p,0.0],rtol=1e-13,atol=1e-14,dense_output=True).sol(r_max)[0]
psi0=brentq(shoot,0.75,0.80,xtol=1e-14)
sol=solve_ivp(rhs,[0,r_max],[psi0,0.0],rtol=1e-13,atol=1e-14,dense_output=True)
f2=lambda r: abs(sol.sol(r)[0])**2
A3,A5,A7=4/3,16/15,32/21
Ik={k:quad(lambda r,k=k:f2(r)*r**k,0,r_max,limit=800,epsabs=1e-12,epsrel=1e-12)[0] for k in (4,6,8)}
def ghalf(b,order):
    mu=A3*Ik[4]+0.5*b**2*A5*Ik[6]; L=A3*Ik[4]+b**2*A5*Ik[6]
    if order>=4:
        mu+=(3/8)*b**4*A7*Ik[8]; L+=(3/4)*b**4*A7*Ik[8]
    return mu/L
K=0.5*(A5/A3)*(Ik[6]/Ik[4])
print(f"psi0={psi0}")
print(f"I4={Ik[4]:.8e} I6={Ik[6]:.8e} I8={Ik[8]:.8e}")
print(f"K=(2/5)(I6/I4) = {K:.6f}")
for b in [1e-4,1e-3,3e-3,1e-2,2e-2,3e-2]:
    print(f"b={b:.0e}: g/2 O(b²)={ghalf(b,2):.10f}  O(b⁴)={ghalf(b,4):.10f}  K_num={(1-ghalf(b,2))/b**2:.4f}")
