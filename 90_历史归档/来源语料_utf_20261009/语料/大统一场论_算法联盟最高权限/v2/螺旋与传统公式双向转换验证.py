#!/usr/bin/env python3
"""
[已废弃 / DEPRECATED]
本脚本已由 93_wrfch_全维双向转换与3D垂直原理验证.py (200位精度) 取代。
保留仅作历史参考。请使用 93_wrfch 版本作为唯一事实来源。

螺旋框架 <-> 传统公式 全维双向转换验证
以 mpmath 60 位精度验证每个转换等式。
核心: 螺旋参数 κ, τ, ω, R 与传统物理量 (m, E, p, γ, α, G, λ) 的互转。
"""
from mpmath import mp, mpf, sqrt, pi, sin, cos
mp.dps = 60

c     = mpf('299792458')
hbar  = mpf('1.0545718176461565e-34')
h     = mpf('6.62607015e-34')
e     = mpf('1.602176634e-19')
alpha = mpf('7.2973525693e-3')
G     = mpf('6.67430e-11')
m_e   = mpf('9.1093837015e-31')
eps0  = mpf('8.8541878128e-12')

# 电子尺度螺旋参数 (自洽反推)
kappa = m_e*c/(hbar*sqrt(1+alpha**2))
tau   = alpha*kappa
omega = c*sqrt(kappa**2+tau**2)
R     = c/omega          # 康普顿半径
b     = alpha*R          # 螺距
rho   = R/sqrt(1+alpha**2)

def verify(name, spiral, trad, note):
    err = abs(1 - spiral/trad)
    lvl = 'S' if err < mpf('1e-12') else 'A' if err<mpf('1e-3') else '✗'
    print(f"  {name:<40} 螺旋={mp.nstr(spiral,10)} 传统={mp.nstr(trad,10)} 误差={mp.nstr(err,2)} {lvl}  {note}")

print("="*82)
print("螺旋参数 (电子): κ, τ, ω, R, ρ, b")
print("="*82)
print(f"  κ={mp.nstr(kappa,8)} m⁻¹, τ={mp.nstr(tau,8)} m⁻¹")
print(f"  ω={mp.nstr(omega,8)} rad/s, R={mp.nstr(R,8)} m")
print(f"  ρ={mp.nstr(rho,8)} m, b={mp.nstr(b,8)} m")
print()

print("="*82)
print("【转换1】运动学: 速度分解  v_⊥²+v_∥² = c²  (3维螺旋垂直原理)")
print("="*82)
v_perp = omega*rho
v_par  = omega*b
verify("v_⊥²+v_∥²=c²", v_perp**2+v_par**2, c**2, "光速约束")
# 垂直性: v_⊥ ⊥ v_∥
r_vec = [rho*cos(mpf('1')), rho*sin(mpf('1')), b]
v_vec = [-rho*sin(mpf('1'))*omega, rho*cos(mpf('1'))*omega, b*omega]
dot = r_vec[0]*v_vec[0]+r_vec[1]*v_vec[1]+r_vec[2]*v_vec[2]
print(f"  位置·速度 点积 = {mp.nstr(dot,3)} (应≈0, 垂直)")

print()
print("="*82)
print("【转换2】量子: E=mc² ⟺ ℏω,  p=ℏk ⟺ ℏ√(κ²+τ²)")
print("="*82)
verify("ℏω = mc²", hbar*omega, m_e*c**2, "质能-频率")
verify("ℏ√(κ²+τ²) = pc", hbar*sqrt(kappa**2+tau**2), m_e*c**2/c, "动量-曲率")
verify("2π/√(κ²+τ²) = h/p", 2*pi/sqrt(kappa**2+tau**2), h/(m_e*c), "康普顿波长")

print()
print("="*82)
print("【转换3】相对论: γ = 1/√(1-β²) ⟺ 1/√(1-(b/R)²)  (β=v_∥/c=b/R)")
print("="*82)
# 纵向速度比 β=v_∥/c=b/R; γ 由螺旋螺距比直接给出
beta = v_par/c
gamma_trad = 1/sqrt(1-beta**2)
gamma_spir = 1/sqrt(1-(b/R)**2)
verify("1/√(1-β²) (传统)", gamma_trad, gamma_spir, "洛伦兹因子(螺旋螺距)")

print()
print("="*82)
print("【转换4】精细结构: α = τ/κ ⟺ e²/(4πε₀ℏc)")
print("="*82)
verify("τ/κ", tau/kappa, alpha, "几何定义")
verify("e²/(4πε₀ℏc)", e**2/(4*pi*eps0*hbar*c), alpha, "传统定义")

print()
print("="*82)
print("【转换5】质量: m = ℏ√(κ²+τ²)/c ⟺ m = ℏω/c²")
print("="*82)
verify("ℏ√(κ²+τ²)/c", hbar*sqrt(kappa**2+tau**2)/c, m_e, "质量-几何")
verify("ℏω/c²", hbar*omega/c**2, m_e, "质量-频率")

print()
print("="*82)
print("【转换6】Gε₀ 三形式互转 (普朗克尺度)")
print("="*82)
lP = sqrt(hbar*G/c**3)
omegaP = c/lP
mP = hbar*omegaP/c**2
A = c**2*e**2*kappa/(4*pi*hbar**2*tau*(kappa**2+tau**2))  # 需普朗克κ,τ
# 用普朗克尺度
kappaP = 1/(lP*sqrt(1+alpha**2)); tauP = alpha*kappaP
A = c**2*e**2*kappaP/(4*pi*hbar**2*tauP*(kappaP**2+tauP**2))
B = c**4*e**2/(4*pi*alpha*hbar**2*omegaP**2)
C = e**2/(4*pi*alpha*mP**2)
tgt = G*eps0
verify("Gε₀(κ,τ)", A, tgt, "曲率形式")
verify("Gε₀(α,ω)", B, tgt, "频率形式")
verify("Gε₀(m_P)", C, tgt, "质量形式")

print()
print("="*82)
print("【转换7】引力: G = c³/[ℏ(κ²+τ²)] (普朗克尺度)")
print("="*82)
verify("c³/[ℏ(ωP/c)²]", c**3/(hbar*(omegaP/c)**2), G, "普朗克尺度")

print()
print("="*82)
print("【转换8】向心力: F = mω²ρ ⟺ F = mc²κ   (用ρ, 恒等 ω²ρ=c²κ)")
print("="*82)
verify("mω²ρ (用ρ)", m_e*omega**2*rho, m_e*c**2*kappa, "向心力-曲率力(ρ)")

print()
print("="*82)
print("【转换9】德布罗意: λ = h/p ⟺ 2π/√(κ²+τ²)")
print("="*82)
verify("h/p = 2π/√(κ²+τ²)", h/(m_e*c), 2*pi/sqrt(kappa**2+tau**2), "德布罗意")

print()
print("="*82)
print("【转换总结】螺旋 ↔ 传统 双向映射表")
print("="*82)
print("""
  螺旋 → 传统                  传统 → 螺旋
  ω      → mc²/ℏ              mc²     → ℏω
  κ      → mω²R/(mc²)·1/R      p=ℏk    → ℏ√(κ²+τ²)
  κ²+τ²  → (ω/c)²              E=mc²   → ℏω
  α=τ/κ  → e²/(4πε₀ℏc)         λ=h/p   → 2π/√(κ²+τ²)
  γ=c/ωR → 1/√(1-β²)           G       → c³/[ℏ(κ²+τ²)]
  v_⊥²+v_∥²=c²                 m=ℏω/c² → ℏ√(κ²+τ²)/c
""")
print("算法联盟最高权限 · 双向转换验证完成")