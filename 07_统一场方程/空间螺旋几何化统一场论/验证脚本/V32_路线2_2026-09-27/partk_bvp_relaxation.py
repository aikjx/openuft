# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part K：solve_bvp 松弛法解双阱 Q-ball 干净基态
场方程：φ'' + (2/r)φ' = (m²-ω²)φ - λφ³ + ηφ⁵,  m²=1,λ=5,η=4
边界：φ'(0)=0（中心正则）, φ(R)=0（远处衰减）。初值：薄墙 tanh 型台阶。
BVP 松弛法对分离线型孤立解鲁棒（不受打靶对初值超敏感影响）。
"""
import numpy as np
from scipy.integrate import solve_bvp
m2=1.0; lam=5.0; eta=4.0; q0=1.0; c=1.0
phi_true=1.0   # 真真空

R=60.0
r=np.linspace(1e-6, R, 3000)

def fw(r, y, om):
    phi, dphi = y
    d2 = (m2-om**2)*phi - lam*phi**3 + eta*phi**5 - (2/r)*dphi
    return np.vstack([dphi, d2])

def bc(ya, yb, om):
    return np.array([ya[1], yb[0]])   # phi'(0)=0, phi(R)=0

def guess(r, wall, delta):
    phi = phi_true * 0.5*(1.0 - np.tanh((r-wall)/delta))
    dphi = phi_true * 0.5*(-1.0/delta)*(1.0/np.cosh((r-wall)/delta)**2)
    return np.vstack([phi, dphi])

print("=== Part K：solve_bvp 松弛法（双阱 Q-ball）===")
for om in [0.3,0.5,0.7,0.9,0.99]:
    converged=False
    for wall in [10,15,20]:
        for delta in [1.0,2.0]:
            y0=guess(r,wall,delta)
            try:
                sol=solve_bvp(fw,bc,r,y0,args=(om,),max_nodes=200000,tol=1e-9)
                phi=sol.sol(r)[0]
                if sol.success and abs(phi[0])>0.2 and abs(phi[-1])<1e-3 and phi.min()>0:
                    converged=True
                    a_c=phi[0]
                    dphi=sol.sol(r)[1]
                    N =4*np.pi*np.trapezoid(r**2*phi**2,r)
                    E0=4*np.pi*np.trapezoid(r**2*(0.5*dphi**2+0.5*m2*phi**2-lam/4*phi**4+eta/6*phi**6),r)
                    E0_ph=E0+4*np.pi*np.trapezoid(r**2*(0.5*om**2*phi**2),r)
                    numC=4*np.pi*np.trapezoid(r**2*(phi**2*(m2-3*lam*phi**2+5*eta*phi**4)*r**2),r)
                    C=numC/N
                    print(f"  ω={om} (wall={wall},δ={delta}): 干净基态 a_c=φ(0)={a_c:.6f}, φ(R)={phi[-1]:.2e}, min={phi.min():+.1e}")
                    print(f"     N={N:.6e} E0={E0:+.6e} E0_ph={E0_ph:.6e} C={C:+.6e} "
                          f"Q0={q0*om*N:.6e} Espec={E0/N:+.6e}")
                    break
            except Exception:
                pass
        if converged: break
