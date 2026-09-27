# -*- coding: utf-8 -*-
# TUFT V3.2 —— 相对论转动 ansatz：局域 boost 破坏质荷同形，μ(γ加权)/L(γ²加权) -> g 偏移
# 结论（对照 15B §6E）：b=ω/c 增大，g/2=2μ/L 从 1.0000 下降到 ~0.869（g<2），形状经 γ 加权矩进入；
# 但方向与电子 g>2 相反，且是刚体式局域 boost（非自洽旋转孤子，r>c/ω 超光速需截断），
# 不能当电子反常磁矩解释。非相对极限 b→0 精确回 g=2。
import numpy as np
from scipy.integrate import solve_ivp
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

def integrals(b,Rc):
    Nr,Nth=240,96
    rr,_=np.polynomial.legendre.leggauss(Nr); rr=0.5*(rr+1)*Rc; wr=0.5*Rc*np.ones(Nr)
    tt,wt=np.polynomial.legendre.leggauss(Nth); tt=0.5*(tt+1)*np.pi; wth=0.5*np.pi*wt
    mu=L=0.0
    for i in range(Nr):
        r=rr[i]
        for j in range(Nth):
            s=np.sin(tt[j]); beta=b*r*s
            if beta>=0.999: continue
            gam=1/np.sqrt(1-beta*beta); rho=f2(r)
            mu+= np.pi*b*rho*gam*r**4*s**3 * wr[i]*wth[j]
            L += 2*np.pi*b*rho*gam*gam*r**4*s**3 * wr[i]*wth[j]
    return mu,L

for b in [1e-4,3e-3,1e-2,2e-2]:
    Rc=min(r_max,0.90/b)
    mu,L=integrals(b,Rc)
    print(f"b={b:.0e} Rc={Rc:7.2f}: μ/L={mu/L:.8f}  g/2=2μ/L={2*mu/L:.8f}")
