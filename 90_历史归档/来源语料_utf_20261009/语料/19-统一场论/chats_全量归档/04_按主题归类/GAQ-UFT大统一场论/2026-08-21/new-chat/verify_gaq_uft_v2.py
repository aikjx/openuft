"""
GAQ-UFT V50 修正版：全维自洽验证
修复点：
  1. ε₀ = e²/(4παℏc)  （原 α³ → 4πα）
  2. μ₀ = 4παℏ/(ce²)   （原 α³ → 4πα）
  3. Gε₀ = e²/(4πα m_P²)
  4. 电磁母方程：K_e = αℏc, S = q/e = τ_v/(ακ)
     （等价形式：K_e = ℏc/α, S = τ_v/κ）
"""
import mpmath as mp
mp.mp.dps = 250

# ===== CODATA-2022 =====
c       = mp.mpf("299792458")
h       = mp.mpf("6.62607015e-34")
hbar    = h / (2 * mp.pi)
e       = mp.mpf("1.602176634e-19")
G       = mp.mpf("6.67430e-11")
alpha   = mp.mpf("0.0072973525693")
eps0_CODATA = mp.mpf("8.8541878128e-12")
mu0_CODATA  = mp.mpf("1.25663706212e-6")  # CODATA 2022 推荐值（非 4πe-7）

# ===== 修正后的几何导出 =====
eps0_geo  = e**2 / (4 * mp.pi * alpha * hbar * c)
mu0_geo   = (4 * mp.pi * alpha * hbar) / (c * e**2)
mP        = mp.sqrt(hbar * c / G)
Omega_P   = c * mP / hbar

# Gε₀ 恒等式
LHS_Geps0 = G * eps0_geo
RHS_Geps0 = e**2 / (4 * mp.pi * alpha * mP**2)

# 引力耦合系数
K_G_original = -G * (hbar / c)**2
K_G_geo      = -(hbar**3) / (c * mP**2)

# 电磁耦合系数（两种等价形式）
K_e_form1 = alpha * hbar * c               # = e²/(4πε₀)
K_e_form2 = hbar * c / alpha                # 配合 S = τ_v/κ 使用
K_e_std   = e**2 / (4 * mp.pi * eps0_geo)  # 标准库仑系数

print("=" * 72)
print("一、修正后电磁常数 vs CODATA-2022")
print("=" * 72)
print(f"  ε₀_geo    = {eps0_geo:.16e}")
print(f"  ε₀_CODATA = {eps0_CODATA:.16e}")
print(f"  Δε₀       = {abs(eps0_geo - eps0_CODATA):.16e}")
print(f"  相对偏差   = {abs(eps0_geo - eps0_CODATA)/eps0_CODATA:.16e}")
print()
print(f"  μ₀_geo    = {mu0_geo:.16e}")
print(f"  μ₀_CODATA = {mu0_CODATA:.16e}")
print(f"  Δμ₀       = {abs(mu0_geo - mu0_CODATA):.16e}")
print(f"  相对偏差   = {abs(mu0_geo - mu0_CODATA)/mu0_CODATA:.16e}")
print()

print("=" * 72)
print("二、电磁关系闭环 c² = 1/(μ₀ε₀)")
print("=" * 72)
c_recover = 1 / mp.sqrt(mu0_geo * eps0_geo)
print(f"  c_recover = {c_recover:.12e}")
print(f"  c_input   = {c:.12e}")
print(f"  Δc        = {abs(c_recover - c):.15e}")
print()

print("=" * 72)
print("三、Gε₀ 耦合恒等式（修正后）")
print("=" * 72)
print(f"  LHS  G·ε₀_geo           = {LHS_Geps0:.16e}")
print(f"  RHS  e²/(4πα·m_P²)      = {RHS_Geps0:.16e}")
print(f"  Δ(Gε₀)                   = {abs(LHS_Geps0 - RHS_Geps0):.16e}")
print(f"  相对偏差                  = {abs(LHS_Geps0-RHS_Geps0)/LHS_Geps0:.16e}")
print()

print("=" * 72)
print("四、引力耦合系数（未受影响，确认通过）")
print("=" * 72)
print(f"  K_G = -G(ℏ/c)²  = {K_G_original:.14e}")
print(f"  K_G = -ℏ³/(c m_P²) = {K_G_geo:.14e}")
print(f"  ΔK_G = {abs(K_G_original - K_G_geo):.14e}")
print()

print("=" * 72)
print("五、电磁耦合系数两种等价形式 & 库仑还原")
print("=" * 72)
print(f"  K_e = αℏc          = {K_e_form1:.14e}")
print(f"  K_e = ℏc/α         = {K_e_form2:.14e}")
print(f"  K_e = e²/(4πε₀)    = {K_e_std:.14e}")
print(f"  Δ(form1 vs std)    = {abs(K_e_form1 - K_e_std):.14e}")
print()
# 注意：form1 和 form2 不等价！form1 配合 S=q/e 使用，form2 配合 S=τ_v/κ 使用
# 验证：对于基本电荷 (q=e, τ_v/κ=α)
# 形式1: U = K_e_form1 * (q1/e)(q2/e) / r = αℏc * 1 / r
# 形式2: U = K_e_form2 * (τ_v1/κ1)(τ_v2/κ2) / r = (ℏc/α) * α² / r = αℏc / r
U_form1 = K_e_form1 * 1 * 1   # q1/e=1, q2/e=1
U_form2 = K_e_form2 * alpha * alpha  # τ_v/κ = α
print(f"  基本电荷势能系数 (形式1, S=q/e):  {U_form1:.14e}")
print(f"  基本电荷势能系数 (形式2, S=τ_v/κ): {U_form2:.14e}")
print(f"  ΔU = {abs(U_form1 - U_form2):.14e}")
print(f"  标准 αℏc = {alpha * hbar * c:.14e}")
print()

print("=" * 72)
print("六、牛顿引力还原（确认通过）")
print("=" * 72)
m1 = mp.mpf("1.0")  # 1 kg
m2 = mp.mpf("1.0")
r  = mp.mpf("1.0")
Omega1 = c * m1 / hbar
Omega2 = c * m2 / hbar
F_G_geo = -hbar**3 / (c * mP**2) * Omega1 * Omega2 / r**2
F_G_newton = -G * m1 * m2 / r**2
print(f"  F_G (几何形式) = {F_G_geo:.14e} N")
print(f"  F_G (牛顿形式) = {F_G_newton:.14e} N")
print(f"  ΔF_G = {abs(F_G_geo - F_G_newton):.14e}")
print()

print("=" * 72)
print("七、库仑力还原（修正后）")
print("=" * 72)
q1 = e
q2 = e
F_e_geo = K_e_form1 * (q1/e) * (q2/e) / r**2
F_e_std = e**2 / (4 * mp.pi * eps0_geo * r**2)
print(f"  F_e (几何形式) = {F_e_geo:.14e} N")
print(f"  F_e (标准形式) = {F_e_std:.14e} N")
print(f"  ΔF_e = {abs(F_e_geo - F_e_std):.14e}")
print()

print("=" * 72)
print("八、普朗克尺度几何量")
print("=" * 72)
L_P = mp.sqrt(hbar * G / c**3)
T_P = L_P / c
print(f"  m_P    = {mP:.14e} kg")
print(f"  Ω_P    = {Omega_P:.14e} m⁻¹")
print(f"  L_P    = {L_P:.14e} m")
print(f"  T_P    = {T_P:.14e} s")
print(f"  ℏc/m_P² = G?  {abs(hbar*c/mP**2 - G)/G:.16e}")
print()

print("=" * 72)
print("九、α³ 来源追溯：如果坚持原公式需要什么条件")
print("=" * 72)
# 原公式 ε₀ = e²/(α_geo³ ℏc)，要等于 SI 的 ε₀ = e²/(4πα_SI ℏc)
# 需要 α_geo³ = 4πα_SI，即 α_geo = (4πα_SI)^(1/3)
alpha_geo_required = (4 * mp.pi * alpha)**(mp.mpf(1)/3)
print(f"  若 ε₀ = e²/(α_geo³·ℏc) 要匹配 SI，需要 α_geo = (4πα)^(1/3)")
print(f"  α_geo_required = {alpha_geo_required:.14e}")
print(f"  α_SI (输入)    = {alpha:.14e}")
print(f"  比值            = {alpha_geo_required/alpha:.14e}")
print(f"  → 原公式中的 α 不是标准精细结构常数，而是 (4πα)^(1/3) ≈ 0.451")
print(f"  → 但用户赋值 α = 0.007297，矛盾。故 α³ 为代数错误。")
print()

print("=" * 72)
print("十、修正因子闭环验证")
print("=" * 72)
# 原公式 → 修正公式的转换因子
F_correct = alpha**2 / (4 * mp.pi)  # ε₀_SI = ε₀_原 * F_correct
print(f"  修正因子 F = α²/(4π) = {F_correct:.16e}")
print(f"  1/F = 4π/α² = {1/F_correct:.16e}")
eps0_original = e**2 / (alpha**3 * hbar * c)
print(f"  ε₀_原 * F = {eps0_original * F_correct:.16e}")
print(f"  ε₀_修正   = {eps0_geo:.16e}")
print(f"  Δ = {abs(eps0_original * F_correct - eps0_geo):.16e}")
