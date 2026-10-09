#!/usr/bin/env python3
# 计算力强比验证

# CODATA 2018常数
c = 299792458  # 光速，单位：m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11  # 万有引力常数，单位：m^3/(kg·s^2)

# 粒子常数
m_p = 1.67262192369e-27  # 质子质量，单位：kg
q_p = 1.602176634e-19  # 质子电荷，单位：C
m_e = 9.1093837015e-31  # 电子质量，单位：kg
q_e = -1.602176634e-19  # 电子电荷，单位：C

import math

# 计算Z'和Z
pi8 = 8 * math.pi
Z_prime = c / (pi8 * epsilon0)
Z = (G * c) / 2

print("计算Z'和Z:")
print(f"Z' = {Z_prime:.11e} kg·m^4·s^-5·A^-2")
print(f"Z = {Z:.11e} m^4·kg^-1·s^-3")
print(f"Z'/Z = {Z_prime/Z:.11e} kg^2/C^2")

# 计算电荷-质量比
q_over_m_p = abs(q_p) / m_p
q_over_m_e = abs(q_e) / m_e
print("\n计算电荷-质量比:")
print(f"|q_p|/m_p = {q_over_m_p:.11e} C/kg")
print(f"|q_e|/m_e = {q_over_m_e:.11e} C/kg")

# 计算粒子属性项
print("\n计算粒子属性项 (|q1 q2|/(m1 m2)):")

# 1. 质子-质子系统
pp_term = (q_over_m_p) ** 2
print(f"1. 质子-质子系统: {pp_term:.11e} C^2/kg^2")

# 2. 质子-电子系统
pe_term = q_over_m_p * q_over_m_e
print(f"2. 质子-电子系统: {pe_term:.11e} C^2/kg^2")

# 3. 电子-电子系统
ee_term = (q_over_m_e) ** 2
print(f"3. 电子-电子系统: {ee_term:.11e} C^2/kg^2")

# 计算力强比
print("\n计算力强比 (电磁力/引力):")

# 1. 质子-质子系统
pp_ratio = (Z_prime / Z) * pp_term
print(f"1. 质子-质子系统: {pp_ratio:.11e} (≈10^{math.log10(pp_ratio):.0f})")

# 2. 质子-电子系统
pe_ratio = (Z_prime / Z) * pe_term
print(f"2. 质子-电子系统: {pe_ratio:.11e} (≈10^{math.log10(pe_ratio):.0f})")

# 3. 电子-电子系统
ee_ratio = (Z_prime / Z) * ee_term
print(f"3. 电子-电子系统: {ee_ratio:.11e} (≈10^{math.log10(ee_ratio):.0f})")

# 验证与论文结果的一致性
print("\n验证与论文结果的一致性:")
print(f"论文中质子-质子力强比: ≈1.235×10^36")
print(f"计算结果: ≈{pp_ratio:.3e}")
print(f"差异: {abs(pp_ratio - 1.235e36)/1.235e36:.11e}")

print(f"论文中质子-电子力强比: ≈2.268×10^39")
print(f"计算结果: ≈{pe_ratio:.3e}")
print(f"差异: {abs(pe_ratio - 2.268e39)/2.268e39:.11e}")

print(f"论文中电子-电子力强比: ≈4.163×10^42")
print(f"计算结果: ≈{ee_ratio:.3e}")
print(f"差异: {abs(ee_ratio - 4.163e42)/4.163e42:.11e}")
