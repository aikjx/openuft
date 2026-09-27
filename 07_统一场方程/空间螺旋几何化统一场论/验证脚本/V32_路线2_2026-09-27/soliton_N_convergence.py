# -*- coding: utf-8 -*-
"""量化反驳：对并发代理声称的主根 ψ0=0.7645，计算 N 随 rmax 的变化，证明 N 发散（非有限 1006.64）"""
import numpy as np
from scipy.integrate import solve_ivp
V1,V2=1.2,0.4; r0=1e-9; psi0=0.7645
print("ψ''+(2/r)ψ'=1.2ψ³-0.4ψ⁵, ψ(0)=0.7645 （并发代理声称 N≈1006.64）")
print(f"{'rmax':>12} | {'ψ(rmax)':>12} | {'N(rmax)':>14} | 注")
for rmax in [2,5,10,20,50,100,200,500,1000,2000,5000]:
    sol=solve_ivp(lambda r,y:[y[1],V1*y[0]**3-V2*y[0]**5-(2/r)*y[1]],
                  [r0,rmax],[psi0,0.0],rtol=1e-11,atol=1e-13,max_step=0.2,dense_output=True)
    r=sol.t;psi=sol.y[0]
    N=4*np.pi*np.trapezoid(r**2*psi**2,r)
    print(f"{rmax:>12} | {psi[-1]:+.6e} | {N:>14.4e} | {'增至 √3=1.732' if abs(psi[-1]-1.732)<0.1 else ''}")
