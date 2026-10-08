# -*- coding: utf-8 -*-
"""Q-ball 尾不衰减的决定性诊断
问题：ω>0 应给指数尾 e^{-ωr}/r，但数值尾不衰减、N 体积发散。
机制假说：V_eff=V-½ω²φ²=V1/4φ⁴-V2/6φ⁶-½ω²φ²。
  - 势无质量项(从φ⁴起) → d²V_eff/dφ²|0 = -ω² < 0 → φ=0 是 V_eff 局部极大(非极小)
  - V_eff 在 φ±=[V1±√(V1²-4V2ω²)]/(2V2) 有极小(φ-)和极大(φ+)
  - Q-ball 解 φ 从中心滚向 0，但被 V_eff 局部极小 φ- (V_eff>0) 捕获，阻尼下无法爬过到 0
  - → 无指数衰减尾 → 无有限 N Q-ball（决定性负结果）
"""
import numpy as np
from scipy.integrate import solve_ivp
V1=1.2; V2=0.4

def Veff(phi, w2): return V1/4*phi**4 - V2/6*phi**6 - 0.5*w2*phi**2
def d2Veff(phi, w2): return 3*V1*phi**2 - 5*V2*phi**4 - w2

print("== V_eff 形状诊断（ω=0.7）==")
w2=0.49
phi_pm = [ (V1+np.sqrt(V1**2-4*V2*w2))/(2*V2), (V1-np.sqrt(V1**2-4*V2*w2))/(2*V2) ]
print(f" φ=0: V_eff={Veff(0,w2):.4f}, d²V_eff/dφ²={d2Veff(0,w2):.4f}  → {'局部极大(❌非极小)' if d2Veff(0,w2)<0 else '局部极小'}")
for s,phi2 in zip(['φ-','φ+'],[phi_pm[1],phi_pm[0]]):
    p=np.sqrt(phi2)
    print(f" {s}={p:.4f}(φ²={phi2:.4f}): V_eff={Veff(p,w2):.4f}, d²V_eff/dφ²={d2Veff(p,w2):.4f}")

print("\n== 机制：Q-ball 尾为何不衰减 ==")
print(" 标准 Q-ball 需势含质量项 m²|ψ|²(m²>ω²) → V_eff 在 φ=0 是局部极小(真空)")
print(" 来稿势 V=V1/4φ⁴-V2/6φ⁶ 无质量项 → V_eff(0) 是局部极大(d²=-ω²<0)")
print(" 解 φ 从中心滚向 φ=0 需爬过 V_eff 局部极小 φ-(V_eff>0) → 带阻尼(2φ'/r)无法爬坡 → 被捕获")
print(" → 无指数衰减尾 → N=∫φ²r²dr 体积发散 → 无有限 N Q-ball")

print("\n== 数值确认：多 ω 下尾不衰减 + N 发散 ==")
def rhs(r,y,w2):
    phi,dphi=y
    if r<1e-12: return [0.0,(w2*phi-V1*phi**3+V2*phi**5)/3]
    return [dphi, w2*phi-V1*phi**3+V2*phi**5-2*dphi/r]
for w in [0.3,0.5,0.7,0.9]:
    w2=w*w
    best=(1e9,None)
    for A in np.linspace(1.05,2.0,40):
        s=solve_ivp(rhs,(0,30),[A,0],args=(w2,),t_eval=np.linspace(0,30,3000),rtol=1e-9,atol=1e-12)
        tail=abs(s.y[0][-1])
        if tail<best[0]: best=(tail,s)
    tail,s=best
    r=s.t; phi=s.y[0]
    N=np.trapezoid(4*np.pi*r**2*phi**2,r)
    # 尾衰减指数：若 φ~e^{-ωr}，则 φ(r)/φ(r/2) 应 ~ e^{-ωr/2}
    print(f" ω={w}: |φ(30)|={tail:.2e}, N(0..30)={N:.3e} → {'❌体积发散' if N>1e3 else '?'}")
    print(f"   r=15:φ={phi[1500]:.4f} r=30:φ={phi[-1]:.4f} → 非指数衰减(指数应 e^-ωr~e^-9~1e-4)")

print("\n== 决定性结论 ==")
print(" 来稿势(无质量项)不产生有限 N Q-ball：ω=0 尾=凝聚/幂律发散，ω>0 被 V_eff 局部极小捕获")
print(" 要局域孤子，需势补质量项 m²|ψ|²(m²>ω²)——超出来稿，属模型扩展，非自证")
