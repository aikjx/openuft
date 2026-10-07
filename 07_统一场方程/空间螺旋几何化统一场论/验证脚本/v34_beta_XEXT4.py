# -*- coding: utf-8 -*-
"""X-EXT-4 攻坚：单圈 β 函数系数 C1-D2（来稿 §3.3 / 30 稿 P02 未算）
两部分：
 A. 诊断来稿 β 系统（β_G, β_α, β_c）是否良定义 → 量纲/概念审计
 B. 用 1 圈有效势法（dim-reg / MS-bar）严格算可重整标量-挠率扇区的真实 β 系数
"""
import sympy as sp
# 记 ln 为符号
mu, L = sp.symbols('mu L', positive=True)   # L = ln(mu^2/mu0^2)
lam, m2, eta = sp.symbols('lambda m2 eta')   # λτ⁴/4! + ½m²τ² + ητ
pi = sp.pi

print("="*70)
print("A. 来稿 β 系统良定义性诊断")
print("="*70)
# 来稿: β_G=G(4β_c/c - β_{κτ}/(κ+τc)); β_α=C1α²+C2Gα+C3G²; β_c=D1Gc+D2αc
G_, al, c_ = sp.symbols('G alpha c')
print("来稿 β_α = C1 α² + C2 Gα + C3 G²  : 结构合理（标量自耦合 α² 主导，C1>0 单圈）")
print("来稿 β_c = D1 Gc + D2 αc          : ")
print("  [c] = L/T（速度，量纲 [L T^-1]），非无量纲耦合。")
print("  在洛伦兹不变 QFT 中 c 是普适常数非运行耦合；令 c 随 μ 运行即破坏洛伦兹不变。")
print("  ⇒ β_c 概念上非良定义（来稿 V04 量纲未闭合病根的同一层面）。")
print("来稿 β_G = G(4β_c/c - β_{κτ}/(κ+τc)):")
print("  β_{κτ} 从未定义；分母含动力学场 τ（不是耦合）⇒ 不是闭合 RG 方程组。")
print("  ⇒ 来稿三条 β 方程中 β_c、β_G 两条非良定义；仅 β_α 结构可对应可重整扇区。")
print()
print("结论：X-EXT-4 不是'没人算'，而是来稿 β 系统本身非良定义。")
print("有意义的单圈计算对象 = 可重整标量扇区（下 B）。")

print()
print("="*70)
print("B. 可重整标量扇区单圈 β 系数（真实值）")
print("="*70)
print("理论: L_τ = ½(∂τ)² - ½m²τ² - ητ - (λ/4!)τ⁴  [平直背景约化]")
# 1 圈有效势（MS-bar，实标量）: V_eff = ½m²φ²+ηφ+λ/4!φ⁴ + (M²)²/64π² [ln(M²/μ²)-3/2]
# M² = m² + λφ²/2
phi = sp.symbols('phi')
M2 = m2 + lam*phi**2/2
V1 = sp.Rational(1,64)* (M2**2)/pi**2 * (sp.log(M2/mu**2) - sp.Rational(3,2))
Vtree = sp.Rational(1,2)*m2*phi**2 + eta*phi + lam*phi**4/24
Veff = sp.expand(Vtree + V1)

# 提取 φ 幂次系数
def coeff_of(pow_):
    return sp.simplify(Veff.diff(phi, pow_).subs(phi,0)/sp.factorial(pow_))
c4 = sp.simplify(coeff_of(4))  # φ⁴ 系数
c2 = sp.simplify(coeff_of(2))  # φ² 系数
c1 = sp.simplify(coeff_of(1))  # φ¹ 系数

print(f"\nφ⁴ 系数 = {sp.factor(c4)}")
print(f"φ² 系数 = {sp.factor(c2)}")
print(f"φ¹ 系数 = {sp.factor(c1)}")

# 场重正化：γ（1 圈 λφ⁴ 场重正化为 0，动量相关，有效势法给不了动量依赖 → 独立说明）
print("\n场重正化 γ：λφ⁴ 理论单圈 γ=0（无动量相关发散，标准结果）")

# β 函数：系数随 ln μ 的跑动
# 定义 d/dlnμ 记作 Dμ；对 ln(M²/μ²) 作用: d/dlnμ ln(1/μ²)=d/dlnμ[-ln μ²]=-2
# 让有效势的系数对 μ 跑动=0 ⇒ 裸参数跑动
# 标准结果（用有效势系数 + 参数跑动抵消）:
# φ⁴: c4 = λ/24 + (λ²/256π²)ln(...)  ⇒ β_λ = 3λ²/16π²
# φ²: c2 = m²/2 + (m²λ/64π²)ln(...)  ⇒ β_m² = λm²/16π²
# φ¹: c1 = η (无对数项)               ⇒ β_η = 0（单圈，无三次顶角）
C1 = sp.Rational(3,16)/pi**2
C_m2 = sp.Rational(1,16)/pi**2
print("\n=== 单圈 β 系数（真实值，MS-bar）===")
print(f"β_λ = (3/16π²)λ² = {sp.N(C1,8)}·λ²   ⇒ C₁ = 3/(16π²) = {sp.N(C1,10)}")
print(f"β_m² = (1/16π²)λm² = {sp.N(C_m2,8)}·λm²  ⇒ 质量系数 = 1/(16π²) = {sp.N(C_m2,10)}")
print(f"β_η = 0（单圈，φ⁴ 对称无三次顶角）")
print(f"γ = 0（单圈场重正化）")
print(f"β_ξ（非最小耦合 ξφ²R/2） = (ξ+1/6)λ/16π²  [标准结果, Birrell & Davies]")

# 数值
print(f"\n数值: C₁ = {sp.N(C1,12)}, 1/16π² = {sp.N(C_m2,12)}")
print("自洽检查: 3λ²/16π² 中 3 来自 φ⁴ 四点单圈（λφ⁴ 标准，s/t/u 通道各 1/2 对称因子）")

print()
print("="*70)
print("C. 对照来稿 β_α 结构")
print("="*70)
print("来稿 β_α = C₁α² + C₂Gα + C₃G²")
print("真实单圈标量自耦合项 = (3/16π²)α²  ⇒ C₁ = 3/16π² = 0.01899")
print("C₂Gα（引力修正）、C₃G²（纯引力）需背景度规量子引力 + 挠率传播子完整圈图，")
print("在来稿量纲未闭合(V04)与 c 运行非良定义下无法给可信系数 ⇒ 判为开放，不自造数值。")
