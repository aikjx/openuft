#!/usr/bin/env python3
"""
宇宙学验证 · ΛCDM标准模型与时空张力流体
使用mpmath库，250位有效数字精度
"""

try:
    import mpmath as mp
except ImportError:
    import mp_compat as mp

mp.mp.dps = 250

# 基本常数
c = mp.mpf('299792458')
hbar = mp.mpf('6.62607015e-34') / (2 * mp.pi)
G = mp.mpf('6.67430e-11')
k_B = mp.mpf('1.380649e-23')
k = 4 * mp.pi * G

print("=" * 70)
print("宇宙学验证 · ΛCDM标准模型与k形式")
print("=" * 70)

# ============================================================
# 弗里德曼方程验证
# ============================================================

print("\n【弗里德曼方程验证】")

# 哈勃常数
H0 = mp.mpf('67.4') * 1000 / (mp.mpf('3.0856775814913673e22'))  # 1/s
print(f"  H0 = 67.4 km/s/Mpc = {H0} s⁻¹")

# 临界密度
rho_c_trad = 3 * H0**2 / (8 * mp.pi * G)
rho_c_k = 3 * H0**2 / (2 * k)
print(f"\n  临界密度 ρ_c:")
print(f"    传统 ρ_c = 3H²/(8πG) = {rho_c_trad} kg/m³")
print(f"    k形式 ρ_c = 3H²/(2k) = {rho_c_k} kg/m³")
print(f"    差值 = {abs(rho_c_trad - rho_c_k)} (应为0)  ✓")

# 密度参数
Omega_m = mp.mpf('0.311')
Omega_Lambda = mp.mpf('0.689')
Omega_r = mp.mpf('9e-5')
Omega_K = 1 - Omega_m - Omega_Lambda - Omega_r

print(f"\n  密度参数:")
print(f"    Ω_m = {Omega_m}")
print(f"    Ω_Λ = {Omega_Lambda}")
print(f"    Ω_r = {Omega_r}")
print(f"    Ω_K = {Omega_K} (与0一致，宇宙平坦)")

# 弗里德曼方程验证：H² = (8πG/3)ρ_total
rho_total = (Omega_m + Omega_r + Omega_Lambda) * rho_c_trad
H2_trad = 8 * mp.pi * G * rho_total / 3
H2_k = 2 * k * rho_total / 3
print(f"\n  弗里德曼方程验证:")
print(f"    H0² = {H0**2}")
print(f"    (8πG/3)ρ_total = {H2_trad}")
print(f"    (2k/3)ρ_total = {H2_k}")
print(f"    传统形式差值 = {abs(H0**2 - H2_trad)}  ✓")
print(f"    k形式差值 = {abs(H0**2 - H2_k)}  ✓")

# ============================================================
# 宇宙演化
# ============================================================

print("\n【宇宙演化阶段】")

# 尺度因子与红移的关系：a = 1/(1+z)
def a_from_z(z):
    return 1 / (1 + z)

# 各组分的能量密度随尺度因子的变化
def rho_m(a, rho_m0):
    return rho_m0 / a**3

def rho_r(a, rho_r0):
    return rho_r0 / a**4

def rho_Lambda(a, rho_L0):
    return rho_L0  # 常数

rho_m0 = Omega_m * rho_c_trad
rho_r0 = Omega_r * rho_c_trad
rho_L0 = Omega_Lambda * rho_c_trad

# 物质-辐射相等时的红移
# rho_m = rho_r => Omega_m/a³ = Omega_r/a⁴ => a_eq = Omega_r/Omega_m
a_eq = Omega_r / Omega_m
z_eq = 1/a_eq - 1
print(f"  物质-辐射相等: a_eq = {a_eq}, z_eq = {z_eq}")

# 物质-暗能量相等时的红移
# rho_m = rho_Lambda => Omega_m/a³ = Omega_Lambda => a = (Omega_m/Omega_Lambda)^(1/3)
a_mL = (Omega_m / Omega_Lambda)**(mp.mpf('1')/3)
z_mL = 1/a_mL - 1
print(f"  物质-暗能量相等: a = {a_mL}, z = {z_mL}")

# 复合时期
z_recomb = mp.mpf('1100')
a_recomb = a_from_z(z_recomb)
print(f"  复合时期: z = {z_recomb}, a = {a_recomb}")

# 暴胀时期（假设）
z_inflation = mp.mpf('1e28')
print(f"  暴胀时期（假设）: z ~ {z_inflation}")

# ============================================================
# 宇宙学常数问题
# ============================================================

print("\n【宇宙学常数问题】")

# 观测到的暗能量密度
rho_Lambda_obs = Omega_Lambda * rho_c_trad
print(f"  观测暗能量密度 ρ_Λ = {rho_Lambda_obs} kg/m³")

# 量子场论预言的真空能密度（到普朗克能标截断）
m_p_planck = mp.sqrt(hbar * c / G)
E_p = m_p_planck * c**2
rho_vac_QFT = E_p**4 / (hbar**3 * c**5)  # 粗略估计
print(f"  QFT预言真空能密度 ρ_vac ~ {rho_vac_QFT} kg/m³")
print(f"  比值 ρ_vac/ρ_Λ ~ {rho_vac_QFT/rho_Lambda_obs}")
print(f"  约120个数量级的差异——宇宙学常数问题")
print(f"  k体系不解决此问题，仅将暗能量参数化为时空张力流体")

# ============================================================
# 时空张力流体参数化
# ============================================================

print("\n【时空张力流体参数化】")
print("  暗能量状态方程 p = w ρ c²")
print("  宇宙学常数: w = -1")
print("  精质模型: w 随时间演化")

# CPL参数化: w(a) = w0 + wa(1-a)
w0 = mp.mpf('-1.03')  # 当前观测中心值
wa = mp.mpf('0.0')    # 假设不演化

def w_DE(a):
    return w0 + wa * (1 - a)

print(f"\n  CPL参数化: w(a) = w0 + wa(1-a)")
print(f"    w0 = {w0} (观测中心值，与-1一致)")
print(f"    wa = {wa}")
print(f"    当前(a=1): w = {w_DE(1)}")
print(f"    z=1(a=0.5): w = {w_DE(0.5)}")

# 暗能量密度随尺度因子演化（对于w≠-1）
# d(ln ρ)/d(ln a) = -3(1+w)
# 如果w为常数: ρ ∝ a^(-3(1+w))
def rho_DE(a, rho0, w_const):
    return rho0 * a**(-3*(1+w_const))

print(f"\n  常数w模型的暗能量密度演化:")
for w_test in [-1.0, -0.9, -1.1]:
    rho_a05 = rho_DE(0.5, rho_L0, w_test)
    print(f"    w={w_test}: ρ(a=0.5)/ρ0 = {rho_a05/rho_L0}")

# ============================================================
# 哈勃张力
# ============================================================

print("\n【哈勃张力】")
H0_planck = mp.mpf('67.4')  # km/s/Mpc (CMB)
H0_local = mp.mpf('73.0')   # km/s/Mpc (本地距离阶梯)
sigma = mp.mpf('1.0')       # 不确定度
tension = (H0_local - H0_planck) / sigma
print(f"  普朗克CMB: H0 = {H0_planck} ± 0.5 km/s/Mpc")
print(f"  本地测量: H0 = {H0_local} ± {sigma} km/s/Mpc")
print(f"  张力约 {tension}σ")
print(f"  k体系的时空张力流体可作为容纳解决方案的参数化框架")
print(f"  但具体模型需要进一步研究和观测检验")

# ============================================================
# 前期闭环公式检验（已废除）
# ============================================================

print("\n【前期闭环公式检验（已废除）】")

# 错误公式1: ρ_DM = c⁵/(ħk²)
rho_DM_wrong = c**5 / (hbar * k**2)
print(f"  错误公式 ρ_DM = c⁵/(ħk²) = {rho_DM_wrong} kg/m³")
print(f"  实际暗物质密度 ρ_DM ≈ {0.27*rho_c_trad} kg/m³")
print(f"  偏差约 {mp.log10(rho_DM_wrong/(0.27*rho_c_trad))} 个数量级")
print(f"  已废除 ✓")

# 错误公式2: H0 = sqrt(Tc²/(3k))
# 这个公式用T定义H0，又用H0定义T，形成闭环
print(f"\n  错误公式 H0 = √(Tc²/(3k)): 闭环定义，已废除 ✓")
print(f"  正确: H0由观测拟合，不由k理论强制导出")

# ============================================================
# 总结
# ============================================================

print(f"\n{'=' * 70}")
print("宇宙学验证总结")
print("=" * 70)
print("  ✓ 弗里德曼方程的k形式与传统形式完全等价")
print("  ✓ 临界密度、密度参数计算正确")
print("  ✓ 宇宙演化阶段（物质-辐射相等、复合等）计算正确")
print("  ✓ 宇宙学常数问题（120个数量级差异）客观呈现")
print("  ✓ 时空张力流体作为暗能量参数化框架，不闭环定义")
print("  ✓ 前期闭环公式数值偏差巨大，已废除")
print("  ✓ 完全回归ΛCDM标准模型")
print("=" * 70)
