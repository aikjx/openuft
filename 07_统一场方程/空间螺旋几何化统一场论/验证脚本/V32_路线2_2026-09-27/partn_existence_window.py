# -*- coding: utf-8 -*-
"""TUFT V3.2 路线2 —— Part N：修正参数（λ=4）后的双阱 Q-ball 干净基态
存在性（Coleman）：切线点 2V/φ² = m²-3λ²/(16η)。λ=4,η=4,m²=1 ⇒ 0.25>0，Q-ball 存在，窗口 ω<0.5。
势 V=½m²φ²-¼λφ⁴+⅙ηφ⁶；方程 φ''+(2/r)φ'=(m²-ω²)φ-λφ³+ηφ⁵。
方法：前向打靶，以 φ(R) 最小化/φ.min() 从正变负定位分离线 a_sep（干净衰减解），brentq 精求 R(a)。
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
m2=1.0; lam=4.0; eta=4.0; q0=1.0; c=1.0; r0=1e-9

# 存在性核验
print(f"Coleman 切线点 2V/φ² = m²-3λ²/16η = {m2-3*lam**2/(16*eta):+.4f} (>0 则 Q-ball 存在, ω<√此值)")

def fwd(a,om,rmx=50,step=0.4):
    return solve_ivp(lambda r,y:[y[1],(m2-om**2)*y[0]-lam*y[0]**3+eta*y[0]**5-(2/r)*y[1]],
                     [r0,rmx],[a,0.0],rtol=1e-11,atol=1e-13,max_step=step,dense_output=True)

om=0.3
# 粗扫：找 φ.min() 从 >0（衰减）变 <0（越零）的区间
prev=None; trans=None
print(f"\n=== Part N：ω={om}，定位分离线 a_sep ===")
for a in np.arange(0.2,2.0,0.01):
    sol=fwd(a,om); f=sol.y[0]; fm=f.min()
    s=np.sign(fm)
    if prev is not None and s!=prev and a>0.3:
        trans=(a-0.01,a); print(f"  φ.min() 符号变化于 a≈{a:.2f}（衰减→越零）"); break
    prev=s
if trans is None:
    print("  未找到符号变化区间"); raise SystemExit

a0,a1=trans
# 在区间内找 φ(R) 最小的 a（最接近干净衰减），再用 R(a) 精求
def Rres(a):
    sol=fwd(a,om); f=sol.y[0]; df=sol.y[1]; kap=np.sqrt(m2-om**2)
    return df[-1]+(kap+1.0/50.0)*f[-1]

# 细扫找 φ(50) 的极小（衰减最深处），作为 a_sep 初估
amin=None; best=1e9
for a in np.arange(a0,a1,0.0002):
    sol=fwd(a,om); fe=abs(sol.y[0][-1])
    if fe<best: best=fe; amin=a
print(f"  衰减最深 a≈{amin:.6f}, φ(50)≈{best:.2e}")
# 用 R(a) 在附近精求
ac=brentq(lambda a:Rres(a), amin-0.0005, amin+0.0005, xtol=1e-15, rtol=1e-14)
sol=fwd(ac,om); f=sol.y[0]
print(f"  brentq 精求 a_c={ac:.6f}: φ(0)={f[0]:.6f}, φ(50)={f[-1]:.2e}, min={f.min():+.1e}")

# 守恒量 + rmax 收敛
print("\n=== 守恒量（ω=0.3, a_c, c=1, m²=1, λ=4, η=4）===")
for rmx in [40,60,80,120]:
    sol=fwd(ac,om,rmx,step=0.15); r=sol.t; phi=sol.y[0]; dphi=sol.y[1]
    N =4*np.pi*np.trapezoid(r**2*phi**2,r)
    E0=4*np.pi*np.trapezoid(r**2*(0.5*dphi**2+0.5*m2*phi**2-lam/4*phi**4+eta/6*phi**6),r)
    E0_ph=E0+4*np.pi*np.trapezoid(r**2*(0.5*om**2*phi**2),r)
    numC=4*np.pi*np.trapezoid(r**2*(phi**2*(m2-3*lam*phi**2+5*eta*phi**4)*r**2),r)
    C=numC/N
    print(f"  rmax={rmx:3d}: N={N:.6e} E0={E0:+.6e} E0_ph={E0_ph:.6e} C={C:+.6e} "
          f"Q0={q0*om*N:.6e} M={E0/c**2:+.6e} Espec={E0/N:+.6e}")
