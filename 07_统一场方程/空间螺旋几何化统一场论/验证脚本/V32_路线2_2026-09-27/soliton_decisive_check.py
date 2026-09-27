# -*- coding: utf-8 -*-
"""决定性核验：静态方程 ψ''+(2/r)ψ'=V1 ψ³ - V2 ψ⁵ (V1=1.2,V2=0.4) 是否有有限 N 局域孤子？
并发代理 15B 声称 ψ0≈0.7645 得 N≈1006.64 有限；我 Part A 曾得到 ψ~A/r 尾、N 发散。
这是直接矛盾，需用同一方程、同一参数亲自复算判定。
"""
import numpy as np
from scipy.integrate import solve_ivp
V1,V2=1.2,0.4; r0=1e-9

def fwd(psi0, rmax, step=0.2):
    return solve_ivp(lambda r,y:[y[1], V1*y[0]**3 - V2*y[0]**5 - (2/r)*y[1]],
                     [r0,rmax],[psi0,0.0],rtol=1e-12,atol=1e-14,max_step=step,dense_output=True)

print("静态方程 ψ''+(2/r)ψ' = 1.2ψ³ - 0.4ψ⁵")
for psi0 in [0.7645, 0.75, 0.8, 0.7, 1.0]:
    sol=fwd(psi0, 2e4)
    r=sol.t; psi=sol.y[0]
    # 计算 r²ψ² 是否趋于常数（幂尾）或趋 0（衰减）
    last=r2psi2 = r[-1]**2*psi[-1]**2
    # N 在 rmax 处的累积（看是否随 rmax 增长）
    N=4*np.pi*np.trapezoid(r**2*psi**2, r)
    print(f"ψ(0)={psi0:.4f}: ψ(2e4)={psi[-1]:+.3e}, r²ψ²(2e4)={last:+.3e}, N(2e4)={N:.4e}, "
          f"ψ 符号{'+' if psi.min()>=0 else '-'}")
