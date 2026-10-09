#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量公式ω取值修正验证
======================
检查m = ℏαω/(c²√(α²+1))中ω的正确取值
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

cd = CODATA
c = cd.c
hbar = cd.hbar
alpha = cd.alpha
m_e = cd.m_e

print("=" * 70)
print("质量公式ω取值修正验证")
print("=" * 70)

# 计算电子的几何参数
rho_e = cd.e**2 / (4 * math.pi * cd.eps0 * cd.m_e * c**2)
b_e = rho_e / alpha
kappa_e = rho_e / (rho_e**2 + b_e**2)
tau_e = b_e / (rho_e**2 + b_e**2)

print(f"\n电子几何参数:")
print(f"  ρ_e = {rho_e:.15e} m")
print(f"  b_e = {b_e:.15e} m")
print(f"  κ_e = {kappa_e:.15e} m⁻¹")
print(f"  τ_e = {tau_e:.15e} m⁻¹")
print(f"  κ_e²+τ_e² = {kappa_e**2+tau_e**2:.15e} m⁻²")

# 正确的质量公式
m_correct = hbar * math.sqrt(kappa_e**2 + tau_e**2) / c
print(f"\n正确质量公式 m=ℏ√(κ²+τ²)/c:")
print(f"  m_correct = {m_correct:.15e} kg")
print(f"  m_e(CODATA) = {m_e:.15e} kg")
print(f"  比值 = {m_correct/m_e:.15f}")

# 方法1: 使用康普顿频率
# ω_C = m_ec²/ℏ
omega_C = m_e * c**2 / hbar
m_from_omega_C = hbar * alpha * omega_C / (c**2 * math.sqrt(alpha**2 + 1))
print(f"\n方法1: 使用康普顿频率ω_C = m_ec²/ℏ")
print(f"  ω_C = {omega_C:.15e} rad/s")
print(f"  m = ℏαω_C/(c²√(α²+1)) = {m_from_omega_C:.15e} kg")
print(f"  比值 = {m_from_omega_C/m_e:.15f}")

# 方法2: 从τ_e反推ω
# τ = αω/(c(α²+1))
# ω = τ·c(α²+1)/α
omega_from_tau = tau_e * c * (alpha**2 + 1) / alpha
m_from_tau = hbar * alpha * omega_from_tau / (c**2 * math.sqrt(alpha**2 + 1))
print(f"\n方法2: 从τ_e反推ω")
print(f"  ω = τ_e·c(α²+1)/α = {omega_from_tau:.15e} rad/s")
print(f"  m = ℏαω/(c²√(α²+1)) = {m_from_tau:.15e} kg")
print(f"  比值 = {m_from_tau/m_e:.15f}")

# 方法3: 从κ_e反推ω
# κ = α²ω/(c(α²+1))
# ω = κ·c(α²+1)/α²
omega_from_kappa = kappa_e * c * (alpha**2 + 1) / alpha**2
m_from_kappa = hbar * alpha * omega_from_kappa / (c**2 * math.sqrt(alpha**2 + 1))
print(f"\n方法3: 从κ_e反推ω")
print(f"  ω = κ_e·c(α²+1)/α² = {omega_from_kappa:.15e} rad/s")
print(f"  m = ℏαω/(c²√(α²+1)) = {m_from_kappa:.15e} kg")
print(f"  比值 = {m_from_kappa/m_e:.15f}")

# 方法4: 使用正确的m表达式
# m = ℏαω/(c²√(α²+1))
# 反推ω = m·c²√(α²+1)/(ℏα)
omega_correct = m_e * c**2 * math.sqrt(alpha**2 + 1) / (hbar * alpha)
print(f"\n方法4: 从m反推正确的ω")
print(f"  ω = m_ec²√(α²+1)/(ℏα) = {omega_correct:.15e} rad/s")

# 验证
m_from_correct_omega = hbar * alpha * omega_correct / (c**2 * math.sqrt(alpha**2 + 1))
print(f"  验证: m = ℏαω/(c²√(α²+1)) = {m_from_correct_omega:.15e} kg")
print(f"  比值 = {m_from_correct_omega/m_e:.15f}")

# 关键分析
print("\n\n" + "=" * 70)
print("【关键分析】")
print("=" * 70)

print(f"""
问题：为什么方法1（使用康普顿频率）计算结果错误？

答案：ω_C = m_ec²/ℏ 是从 E=mc² 和 E=ℏω 得到的频率，
但这个频率并不等于几何本征频率！

几何本征频率应该从 κ,τ 的定义反推：
  τ = αω/(c(α²+1))
  ω = τ·c(α²+1)/α

这对应于：
  ω = ω_C · √(α²+1)/α

也就是说，几何本征频率比康普顿频率大 √(α²+1)/α ≈ 137 倍！

这是因为：
  E = ℏω_几何 ≠ m_ec²
  
实际上：
  m_ec² = ℏ√(κ²+τ²)·c （从正确的质量公式）
        = ℏαω/(c√(α²+1)) （代入κ²+τ²的表达式）
        
所以：
  m_ec² = ℏαω/(c√(α²+1))
  ω = m_ec²·c√(α²+1)/(ℏα)

这表明几何本征频率不是康普顿频率，而是康普顿频率的 √(α²+1)/α 倍。
""")

# 验证关系
omega_C = m_e * c**2 / hbar
omega_geometric = tau_e * c * (alpha**2 + 1) / alpha
ratio_omegas = omega_geometric / omega_C
expected_ratio = math.sqrt(alpha**2 + 1) / alpha

print(f"ω_几何 / ω_康普顿 = {ratio_omegas:.15f}")
print(f"预期 √(α²+1)/α = {expected_ratio:.15f}")
print(f"一致性: {abs(ratio_omegas - expected_ratio) < 1e-10}")

print("\n" + "=" * 70)
