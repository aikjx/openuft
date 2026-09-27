# -*- coding: utf-8 -*-
"""Part O：λ=5,ω=0.5 精细景观——直接打印 φ(50) 与 φ.min()，看分离线结构
V_pot 在 a≈1.037 有正极大 (+0.212)，衰减解应在其附近。
"""
import numpy as np
from scipy.integrate import solve_ivp
m2=1.0; lam=5.0; eta=4.0; r0=1e-9; om=0.5

def fwd(a,rmx=50,step=0.4):
    return solve_ivp(lambda r,y:[y[1],(m2-om**2)*y[0]-lam*y[0]**3+eta*y[0]**5-(2/r)*y[1]],
                     [r0,rmx],[a,0.0],rtol=1e-11,atol=1e-13,max_step=step,dense_output=True)

print("a        φ(50)          φ.min()    标签")
for a in np.arange(1.00,1.08,0.0005):
    sol=fwd(a); f=sol.y[0]; fe=f[-1]; fm=f.min()
    tag=''
    if fm>0 and abs(fe)<1e-3: tag='<POS-DECAY?>'
    if fm<0: tag='<CROSS>'
    print(f"{a:.4f}  {fe:+.3e}  {fm:+.3e}  {tag}")
