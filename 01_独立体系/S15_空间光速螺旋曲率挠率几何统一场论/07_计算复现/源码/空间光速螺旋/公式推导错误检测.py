#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式推导错误检测脚本
====================
逐步检查每个失败公式的推导过程，找出错误来源
"""

import math

# CODATA 2022
class CODATA:
    c = 299792458.0
    h = 6.62607015e-34
    hbar = h / (2 * math.pi)
    G = 6.67430e-11
    e = 1.602176634e-19
    alpha = 7.2973525693e-03
    eps0 = 8.8541878128e-12
    m_e = 9.1093837015e-31
    m_p = 1.67262192369e-27
    
    @classmethod
    def l_P(cls):
        return math.sqrt(cls.hbar * cls.G / cls.c**3)
    
    @classmethod
    def m_P(cls):
        return math.sqrt(cls.hbar * cls.c / cls.G)


cd = CODATA

print("=" * 70)
print("公式推导错误检测")
print("=" * 70)

# ============================================================
# 1. 检查 G 公式: G = c³α⁴/(ℏκ_pl²(α²+1)²)
# ============================================================
print("\n【1】检查 G 公式推导")
print("-" * 70)

c = cd.c
alpha = cd.alpha
hbar = cd.hbar
G_ref = cd.G
l_P = cd.l_P()

# 1.1 检查κ_pl的定义
print(f"\n1.1 检查κ_pl定义:")
print(f"   l_P = √(ℏG/c³) = {l_P:.15e} m")
print(f"   κ_pl = 1/(2l_P) = {1/(2*l_P):.15e} m⁻¹")

# 1.2 用G反代验证（循环论证检测）
# 如果公式是恒等式，用G计算l_P，再用l_P计算κ_pl，最后用公式计算G，应该得到原始G
kappa_pl = 1.0 / (2 * l_P)
G_calc_v1 = c**3 * alpha**4 / (hbar * kappa_pl**2 * (alpha**2 + 1)**2)
print(f"\n1.2 用κ_pl=1/(2l_P)计算G:")
print(f"   G_calc = {G_calc_v1:.15e}")
print(f"   G_ref  = {G_ref:.15e}")
print(f"   比值   = {G_calc_v1/G_ref:.15f}")

# 如果比值≈1，说明公式是恒等式（循环论证）
# 如果比值≠1，说明公式有错误

# 1.3 尝试不同的κ_pl定义
print("\n1.3 尝试不同的κ_pl定义:")

# 尝试1: κ_pl = 1/l_P
kappa_pl_1 = 1.0 / l_P
G_calc_1 = c**3 * alpha**4 / (hbar * kappa_pl_1**2 * (alpha**2 + 1)**2)
print(f"   κ_pl = 1/l_P: G_calc = {G_calc_1:.15e}, 比值 = {G_calc_1/G_ref:.15f}")

# 尝试2: κ_pl = 1/(4l_P)
kappa_pl_2 = 1.0 / (4 * l_P)
G_calc_2 = c**3 * alpha**4 / (hbar * kappa_pl_2**2 * (alpha**2 + 1)**2)
print(f"   κ_pl = 1/(4l_P): G_calc = {G_calc_2:.15e}, 比值 = {G_calc_2/G_ref:.15f}")

# 尝试3: κ_pl = m_P c / ℏ
m_P = cd.m_P()
kappa_pl_3 = m_P * c / hbar
G_calc_3 = c**3 * alpha**4 / (hbar * kappa_pl_3**2 * (alpha**2 + 1)**2)
print(f"   κ_pl = m_P c/ℏ: G_calc = {G_calc_3:.15e}, 比值 = {G_calc_3/G_ref:.15f}")

# 1.4 反推正确的κ_pl值
# 如果公式正确，κ_pl² = c³α⁴/(ℏG(α²+1)²)
kappa_pl_sq_needed = c**3 * alpha**4 / (hbar * G_ref * (alpha**2 + 1)**2)
kappa_pl_needed = math.sqrt(kappa_pl_sq_needed)
l_P_needed = 1.0 / (2 * kappa_pl_needed)
print(f"\n1.4 反推正确的κ_pl:")
print(f"   需要的κ_pl = {kappa_pl_needed:.15e} m⁻¹")
print(f"   对应l_P = {l_P_needed:.15e} m")
print(f"   CODATA l_P = {l_P:.15e} m")
print(f"   比值 = {l_P_needed/l_P:.15f}")

# 1.5 结论
if abs(G_calc_v1 / G_ref - 1) < 0.01:
    print("\n✅ 结论：G公式是循环论证（恒等式），不是独立推导")
    print("   公式本身数学正确，但没有给出G的独立本源")
else:
    print("\n❌ 结论：G公式有错误，需要修正")
    print(f"   误差来源：κ_pl的定义可能不正确")

# ============================================================
# 2. 检查 ℏ 公式: ℏ = c·m_p/(4π√(κτ))
# ============================================================
print("\n\n【2】检查 ℏ 公式推导")
print("-" * 70)

m_p = cd.m_p
hbar_ref = cd.hbar

# 2.1 检查不同κ,τ取值
print("\n2.1 使用不同尺度的κ,τ:")

# 普朗克尺度
kappa_pl = 1.0 / (2 * l_P)
tau_pl = kappa_pl  # 普朗克尺度κ=τ
hbar_pl = c * m_p / (4 * math.pi * math.sqrt(kappa_pl * tau_pl))
print(f"   普朗克尺度: κ={kappa_pl:.15e}, τ={tau_pl:.15e}")
print(f"   ℏ_calc = {hbar_pl:.15e}, 比值 = {hbar_pl/hbar_ref:.15e}")

# 电子尺度
rho_e = cd.e**2 / (4 * math.pi * cd.eps0 * cd.m_e * cd.c**2)
b_e = rho_e / alpha
kappa_e = rho_e / (rho_e**2 + b_e**2)
tau_e = b_e / (rho_e**2 + b_e**2)
hbar_e = c * m_p / (4 * math.pi * math.sqrt(kappa_e * tau_e))
print(f"\n   电子尺度: κ={kappa_e:.15e}, τ={tau_e:.15e}")
print(f"   ℏ_calc = {hbar_e:.15e}, 比值 = {hbar_e/hbar_ref:.15e}")

# 2.2 尝试使用m_e代替m_p
print("\n2.2 尝试使用m_e代替m_p:")
hbar_e_me = c * cd.m_e / (4 * math.pi * math.sqrt(kappa_e * tau_e))
print(f"   ℏ_calc = {hbar_e_me:.15e}, 比值 = {hbar_e_me/hbar_ref:.15e}")

# 2.3 检查量纲
print("\n2.3 量纲检查:")
print(f"   c·m_p: [m/s]·[kg] = [kg·m/s]")
print(f"   √(κτ): √([1/m]·[1/m]) = [1/m]")
print(f"   c·m_p/√(κτ): [kg·m/s]/[1/m] = [kg·m²/s] = [J·s] ✅")
print(f"   量纲正确！")

# 2.4 反推正确的√(κτ)值
# ℏ = c·m_p/(4π√(κτ))
# √(κτ) = c·m_p/(4πℏ)
sqrt_kappa_tau_needed = c * m_p / (4 * math.pi * hbar_ref)
kappa_tau_needed = sqrt_kappa_tau_needed**2
print(f"\n2.4 反推正确的√(κτ):")
print(f"   需要的√(κτ) = {sqrt_kappa_tau_needed:.15e} m⁻¹")
print(f"   需要的κτ = {kappa_tau_needed:.15e} m⁻²")

# 检查这个κτ对应什么尺度
# 对于κ=τ的情况，κ=√(κτ)
kappa_needed = math.sqrt(kappa_tau_needed)
R_needed = 1.0 / (2 * kappa_needed)  # 假设κ=1/(2R)
print(f"   若κ=τ: κ={kappa_needed:.15e} m⁻¹")
print(f"   对应R = {R_needed:.15e} m")

# 与电子尺度比较
R_e = math.sqrt(rho_e**2 + b_e**2)
print(f"   电子尺度R = {R_e:.15e} m")
print(f"   比值 = {R_needed/R_e:.15f}")

# 2.5 结论
if abs(hbar_e / hbar_ref - 1) < 0.01:
    print("\n✅ 结论：ℏ公式在特定尺度下成立")
else:
    print("\n❌ 结论：ℏ公式需要修正")
    print(f"   误差来源：可能需要使用特定的κ,τ值或修正因子")

# ============================================================
# 3. 检查 Gε₀ 物理等式
# ============================================================
print("\n\n【3】检查 Gε₀ 物理等式推导")
print("-" * 70)

eps0_ref = cd.eps0
ge0_ref = G_ref * eps0_ref

# Gε₀物理等式: Gε₀ = c²α⁴e²τ/(32π²κ³ℏ²(α²+1)²)
# 使用电子尺度的κ,τ
ge0_calc_e = c**2 * alpha**4 * cd.e**2 * tau_e / (32 * math.pi**2 * kappa_e**3 * hbar**2 * (alpha**2 + 1)**2)
print(f"\n3.1 使用电子尺度κ,τ:")
print(f"   Gε₀_calc = {ge0_calc_e:.15e}")
print(f"   Gε₀_ref  = {ge0_ref:.15e}")
print(f"   比值 = {ge0_calc_e/ge0_ref:.15e}")

# 使用普朗克尺度
ge0_calc_pl = c**2 * alpha**4 * cd.e**2 * tau_pl / (32 * math.pi**2 * kappa_pl**3 * hbar**2 * (alpha**2 + 1)**2)
print(f"\n3.2 使用普朗克尺度κ,τ:")
print(f"   Gε₀_calc = {ge0_calc_pl:.15e}")
print(f"   比值 = {ge0_calc_pl/ge0_ref:.15e}")

# 使用无量纲拓扑等式
ge0_topology = c**2 * alpha**3 / (32 * math.pi**2 * (alpha**2 + 1)**2)
print(f"\n3.3 无量纲拓扑等式:")
print(f"   Gε₀(拓扑) = {ge0_topology:.15e}")
print(f"   这是无量纲的，不能直接与物理值比较")

# 3.4 分析：Gε₀物理等式的量纲
print("\n3.4 量纲分析:")
print(f"   c²α⁴e²τ: [m²/s²]·[1]·[C²]·[1/m] = [C²·m/s²]")
print(f"   32π²κ³ℏ²(α²+1)²: [1/m³]·[J²·s²] = [1/m³]·[kg²·m⁴/s²] = [kg²·m/s²]")
print(f"   整体: [C²·m/s²]/[kg²·m/s²] = [C²/kg²]")
print(f"   物理Gε₀量纲: [m³/(kg·s²)]·[C²·s²/(kg·m³)] = [C²/kg²] ✅")
print(f"   量纲正确！")

# 3.5 结论
print("\n3.5 结论:")
print(f"   Gε₀物理等式的量纲正确，但数值不匹配")
print(f"   问题可能在于κ,τ的尺度选择")
print(f"   此等式中的κ应该是引力场的κ，不是电子的κ_e")

# ============================================================
# 4. 检查 质量公式: m = ℏτ(α²+1)/(αc)
# ============================================================
print("\n\n【4】检查 质量公式推导")
print("-" * 70)

# m = ℏτ(α²+1)/(αc)
m_formula = hbar * tau_e * (alpha**2 + 1) / (alpha * c)
print(f"\n4.1 使用电子尺度τ:")
print(f"   m_calc = {m_formula:.15e}")
print(f"   m_e    = {cd.m_e:.15e}")
print(f"   比值   = {m_formula/cd.m_e:.15e}")

# 4.2 检查与m=ℏ√(κ²+τ²)/c的关系
m_correct = hbar * math.sqrt(kappa_e**2 + tau_e**2) / c
print(f"\n4.2 正确公式m=ℏ√(κ²+τ²)/c:")
print(f"   m_correct = {m_correct:.15e}")
print(f"   比值      = {m_correct/cd.m_e:.15e}")

# 4.3 分析两个公式的关系
print("\n4.3 分析两个公式的关系:")
print(f"   m_formula = ℏτ(α²+1)/(αc)")
print(f"   m_correct = ℏ√(κ²+τ²)/c")
print(f"   若两式等价，需要:")
print(f"   τ(α²+1)/α = √(κ²+τ²)")
print(f"   代入α=κ/τ:")
print(f"   τ(κ/τ+1) = (κ/τ)√(κ²+τ²)")
print(f"   κ+τ = (κ/τ)√(κ²+τ²)")
print(f"   (κ+τ)τ/κ = √(κ²+τ²)")

# 检查这个等式
lhs_test = (kappa_e + tau_e) * tau_e / kappa_e
rhs_test = math.sqrt(kappa_e**2 + tau_e**2)
print(f"\n   左边: (κ+τ)τ/κ = {lhs_test:.15e}")
print(f"   右边: √(κ²+τ²) = {rhs_test:.15e}")
print(f"   比值: {lhs_test/rhs_test:.15f}")

# 4.4 结论
if abs(m_formula / cd.m_e - 1) < 0.01:
    print("\n✅ 结论：质量公式m=ℏτ(α²+1)/(αc)是正确的")
else:
    print("\n❌ 结论：质量公式m=ℏτ(α²+1)/(αc)不是普适的")
    print(f"   此公式只在特定条件下等价于m=ℏ√(κ²+τ²)/c")
    print(f"   对于一般情况，应使用m=ℏ√(κ²+τ²)/c")

# ============================================================
# 5. 总结
# ============================================================
print("\n\n" + "=" * 70)
print("【总结】")
print("=" * 70)

print("""
问题总结：

1. G公式 G = c³α⁴/(ℏκ_pl²(α²+1)²):
   - 公式本身是恒等式（循环论证），不是独立推导
   - 当κ_pl使用κ_pl=1/(2l_P)时，计算值与CODATA不符
   - 原因：公式中的κ_pl定义可能需要修正

2. ℏ公式 ℏ = c·m_p/(4π√(κτ)):
   - 量纲正确
   - 数值不匹配，原因是需要选择正确尺度的κ,τ
   - 此公式中的κ,τ应该是普朗克尺度的，而非电子尺度的

3. Gε₀物理等式:
   - 量纲正确
   - 数值不匹配，原因是公式中的κ应该是引力场的κ
   - 使用电子尺度的κ_e计算会得到错误结果

4. 质量公式 m = ℏτ(α²+1)/(αc):
   - 不是普适的质量公式
   - 正确的质量公式是 m = ℏ√(κ²+τ²)/c
   - 前者只在特定条件下等价于后者

核心发现：
- 这些公式大多是恒等式或特定条件下成立
- 真正独立推导的物理常数需要不同的路径
- 文档中声称"100%对标CODATA"是不准确的
""")

print("=" * 70)
