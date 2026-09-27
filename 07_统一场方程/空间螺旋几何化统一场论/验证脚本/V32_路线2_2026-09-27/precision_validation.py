# -*- coding: utf-8 -*-
"""TUFT V3.2 攻坚 —— 综合精算验证脚本
对关键解析公式做数值精算核实：符号不自洽系数、Coleman 存在窗口、V_min、
微扰展开系数、LW 辐射功率结构。
"""
import numpy as np

print("="*70)
print("A. 符号不自洽精算（来稿参数 V1=1.2, V2=0.4）")
print("="*70)
V1,V2=1.2,0.4
# 来稿能量密度 W = 0.5|grad|^2 + V1/4|psi|^4 - V2/6|psi|^6
# L 的势 V(s)= V1/4 s^2 - V2/6 s^3,  V'(s)=V1/2 s - V2/2 s^2
# 场方程(正确) ∂²ψ = -∂V/∂ψ* = -ψ V'(s) = -(V1/2 s - V2/2 s^2)ψ
c_V1_corr, c_V2_corr = V1/2, V2/2          # 正确方程系数 (负号前)
c_V1_sub,  c_V2_sub  = V1,   V2            # 来稿方程系数
print(f"  正确方程 ∂²ψ = -({V1/2:.3f}|ψ|²ψ - {V2/2:.3f}|ψ|⁴ψ)")
print(f"  来稿方程 ∂²ψ = +({V1:.1f}|ψ|²ψ - {V2:.1f}|ψ|⁴ψ)")
print(f"  ⇒ 符号整体相反，且系数差 {V1/(V1/2):.0f} 倍（四/六次项均如此）")
print(f"  来稿方程对应势 W=-V1/4|ψ|^4+V2/6|ψ|^6 = -{V1/4:.3f}|ψ|^4+{V2/6:.4f}|ψ|^6（无下界、类快子）")

print()
print("="*70)
print("B. A1 微扰展开系数验证（ψ0 实）")
print("="*70)
# |ψ0+δ|^2(ψ0+δ) = ψ0^3 + 3ψ0^2 δ  (一阶)
print(f"  |ψ|²ψ ≈ ψ0³ + 3ψ0²δ  ⇒ 一阶系数 3（来稿写 (2|ψ0|²+ψ0²)，实 ψ0 下 =3ψ0² ✓）")
print(f"  |ψ|⁴ψ ≈ ψ0⁵ + 5ψ0⁴δ  ⇒ 一阶系数 5（来稿写 (4|ψ0|⁴+|ψ0|²ψ0²)，实 ψ0 下 =5ψ0⁴ ✓）")
print(f"  微扰方程系数: 3V1-5V2·(ψ0²) = 3*{V1}-5*{V2}·ψ0² = {3*V1:.1f}-{5*V2:.1f}ψ0²")
print(f"  （对 ψ0=1: {3*V1-5*V2:.1f}; 实际是空间依赖的，来自 (3V1|ψ0|²-5V2|ψ0|⁴)）")

print()
print("="*70)
print("C. Coleman Q-ball 存在性窗口精算")
print("="*70)
m2,eta=1.0,4.0
for lam in [4.0,5.0]:
    win = m2 - 3*lam**2/(16*eta)          # 2V/φ² at tangent point
    # V_min: 真真空 φ² 由 m²-λφ²+ηφ⁴=0
    disc = lam**2 - 4*m2*eta
    if disc>=0:
        s=(lam-np.sqrt(disc))/(2*eta)      # 较小根（局部极值）
        sm=(lam+np.sqrt(disc))/(2*eta)     # 较大根
        Vmin=0.5*m2*sm - lam/4*sm**2 + eta/6*sm**3
        Vs= 0.5*m2*s  - lam/4*s**2  + eta/6*s**3
        print(f"  λ={lam}: 切线点 2V/φ²={win:+.4f}; V_min(φ²={sm:.4f})={Vmin:+.4f}; V(局部极值 φ²={s:.4f})={Vs:+.4f}")
        print(f"    ⇒ 窗口{'空(无Q-ball)' if win<=0 else '存在但 V_min>0 需查'}; Q-ball 存在需 win>0 且 Vmin<0")
    else:
        print(f"  λ={lam}: 判别式<0，V 单调，无真空")

print()
print("="*70)
print("D. LW 辐射功率结构（来稿 P0 系数）")
print("="*70)
eps0=8.8541878128e-12; c=299792458.0; mu0=1.25663706212e-6
coef = 1.0/(6*np.pi*eps0*c**3)
coef_mu0 = mu0/(6*np.pi*c)
print(f"  P0 系数 Q0²/6πε0c³ = {coef:.3e}  (= μ0 Q0²/6πc × ... 核对: μ0/6πc={coef_mu0:.3e})")
print(f"  经典 Larmor: P=Q²a²γ⁶/6πε0c³; TUFT 修正: ×(1+𝒞)")

print()
print("="*70)
print("E. 质荷关系（A2）代数验证：M = Q0/(c²q0ω0)·E_specific")
print("="*70)
# E_specific = [∫(0.5|∇ψ0|²+V1/4|ψ0|⁴-V2/6|ψ0|⁶)]/[∫|ψ0|²]
print(f"  E_specific = E0/N：由静止孤子轮廓与耦合决定，与 ω0 无关（来稿 A2 定义）")
print(f"  量纲: [E_specific]=能量, [Q0/(c²q0ω0)]=电荷/(速度²·电荷·频率)=1/(速度²/频率)… 需 q0,c 取自然单位")
print(f"  ⇒ M=Q0·E_specific/(c²q0ω0)：电荷与质量同源（同一标量包络场孤子），非独立输入参数")
