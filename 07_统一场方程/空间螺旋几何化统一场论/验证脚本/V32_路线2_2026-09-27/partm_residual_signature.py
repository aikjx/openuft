# -*- coding: utf-8 -*-
"""Part M：高分辨率 R(a) 变号诊断，精确定位双阱 Q-ball 分离线
R(a)=φ'(R)+(κ+1/R)φ(R)：在干净衰减解处=0。粗扫定位变号区间，细扫确认。
m²=1, λ=5, η=4（Coleman 窗口 0<ω<1）
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
m2=1.0; lam=5.0; eta=4.0; r0=1e-9

def fwd(a,om,rmx=45,step=0.4):
    return solve_ivp(lambda r,y:[y[1],(m2-om**2)*y[0]-lam*y[0]**3+eta*y[0]**5-(2/r)*y[1]],
                     [r0,rmx],[a,0.0],rtol=1e-11,atol=1e-13,max_step=step,dense_output=True)

def Rf(a,om,rmx=45):
    sol=fwd(a,om,rmx); f=sol.y[0]; df=sol.y[1]
    kap=np.sqrt(max(m2-om**2,1e-12))
    return df[-1]+(kap+1.0/rmx)*f[-1]

om=0.5
print(f"=== Part M：ω={om} R(a) 变号诊断（Coleman 窗口 0<ω<1）===")
# 粗扫
prev=None; crosses=[]
for a in np.arange(0.30,1.40,0.01):
    Rv=Rf(a,om)
    s=np.sign(Rv)
    if prev is not None and s!=prev:
        crosses.append((a-0.01,a,Rv))
    prev=s
print(f"粗扫变号区间数: {len(crosses)}")
for c in crosses: print(f"  a∈[{c[0]:.3f},{c[1]:.3f}]  R(a1)={c[2]:+.3e}")

# 对每个变号区间 brentq 精求
for (a0,a1,_) in crosses:
    try:
        ac=brentq(lambda a:Rf(a,om),a0,a1,xtol=1e-15,rtol=1e-14)
    except ValueError:
        continue
    sol=fwd(ac,om,rmx=45); f=sol.y[0]
    # 验证：全程正、中心非零、远场衰减
    if f.min()>0 and f[0]>0.1 and abs(f[-1])<1e-5:
        print(f"  干净分离线解: a_c=φ(0)={f[0]:.6f}, φ(45)={f[-1]:.2e}, min={f.min():+.1e}")
    else:
        print(f"  a_c={ac:.6f}: 验证失败 f(0)={f[0]:.3f} min={f.min():+.1e} f(45)={f[-1]:.2e}")
