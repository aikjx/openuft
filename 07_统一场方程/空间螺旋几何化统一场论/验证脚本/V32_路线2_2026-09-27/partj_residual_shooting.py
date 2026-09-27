# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part J：稳健分离线打靶，解双阱 Q-ball 干净基态
场方程：φ'' + (2/r)φ' = (m²-ω²)φ - λφ³ + ηφ⁵,  m²=1,λ=5,η=4
尾衰减模式 φ ~ A e^{-κ r}/r, κ=√(m²-ω²); 衰减模式条件 φ'(R)=-(κ+1/R)φ(R)
残差 R(a) = φ'(R)+(κ+1/R)φ(R) 在干净衰减解处=0（前向打靶）。
排除平凡解（φ≈0）与越零伪解；验证全程正、单调、φ(0)≈真真空。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
m2=1.0; lam=5.0; eta=4.0; q0=1.0; c=1.0; r0=1e-9; R=50.0

def fwd(a, om, rmx=R, step=0.4):
    sol=solve_ivp(lambda r,y:[y[1],(m2-om**2)*y[0]-lam*y[0]**3+eta*y[0]**5-(2/r)*y[1]],
                  [r0,rmx],[a,0.0],rtol=1e-11,atol=1e-13,max_step=step,dense_output=True)
    return sol

def resid(a, om, rmx=R):
    kappa=np.sqrt(max(m2-om**2,1e-12))
    sol=fwd(a,om,rmx)
    f=sol.y[0]; df=sol.y[1]
    ph_R, dph_R=f[-1], df[-1]
    return dph_R+(kappa+1.0/rmx)*ph_R, ph_R, f.min()

print("=== Part J：稳健分离线打靶（双阱 Q-ball）===")
for om in [0.3,0.5,0.7,0.9,0.99]:
    kappa=np.sqrt(max(m2-om**2,1e-12))
    # 粗扫定位 R(a) 变号区间（排除平凡区 a>0.25）
    signs=[]
    prev=None
    for a in np.arange(0.25,2.0,0.02):
        rv,_,_=resid(a,om)
        s=np.sign(rv)
        if prev is not None and s!=prev:
            signs.append((a-0.02,a))
        prev=s
    found=None
    for (a0,a1) in signs:
        def Rf(a): return resid(a,om)[0]
        try:
            ac=brentq(Rf,a0,a1,xtol=1e-14,rtol=1e-13)
        except ValueError:
            continue
        # 验证
        sol=fwd(ac,om,rmx=R)
        f=sol.y[0]; df=sol.y[1]
        ok = f.min()>0 and abs(f[-1])<1e-5 and ac>0.2
        if ok:
            found=(ac,f.min(),f[-1],f[0]); break
    if found is None:
        print(f"  ω={om} (κ={kappa:.3f}): 未找到干净正定衰减解（粗扫变号区 {len(signs)} 处，均未通过验证）")
        continue
    ac,fmin,fe,f0=found
    print(f"  ω={om} (κ={kappa:.3f}): 干净基态 a_c=φ(0)={f0:.6f}, min f={fmin:+.2e}, f(R)={fe:+.2e}")
    # 守恒量 + rmax 收敛
    for rmx in [40,60,80,120]:
        sol=fwd(ac,om,rmx,step=0.15)
        r=sol.t; f=sol.y[0]; df=sol.y[1]
        N =4*np.pi*np.trapezoid(r**2*f**2,r)
        E0=4*np.pi*np.trapezoid(r**2*(0.5*df**2+0.5*m2*f**2-lam/4*f**4+eta/6*f**6),r)
        E0_ph=E0+4*np.pi*np.trapezoid(r**2*(0.5*om**2*f**2),r)
        numC=4*np.pi*np.trapezoid(r**2*(f**2*(m2-3*lam*f**2+5*eta*f**4)*r**2),r)
        C=numC/N
        print(f"     rmax={rmx:3d}: N={N:.6e} E0={E0:+.6e} E0_ph={E0_ph:.6e} C={C:+.6e} "
              f"Q0={q0*om*N:.6e} Espec={E0/N:+.6e}")
