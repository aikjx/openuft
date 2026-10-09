#!/usr/bin/env python3
"""
验证统一场论中万有引力常数的量子尺度计算
"""

print("=== 使用论文中给出的具体数值验证计算 ===")

# 论文中使用的数值
hbar_paper = 1.0545718176461565e-34  # J·s，约化普朗克常数
c = 299792458  # m/s，光速
m_p_paper = 2.176434e-8  # kg，论文中使用的普朗克质量
G_exp = 6.67430e-11  # m³·kg⁻¹·s⁻²，CODATA 2018万有引力常数实验值

# 论文中计算的分子和分母
numerator_paper = 3.161526780362677e-26  # J·m
denominator_paper = 4.7378610316e-16  # kg²
G_theo_paper = 6.6730001e-11  # m³·kg⁻¹·s⁻²，论文中计算的理论值

print("=== 论文中使用的数值 ===")
print(f"约化普朗克常数 ℏ = {hbar_paper:.16e} J·s")
print(f"光速 c = {c} m/s")
print(f"普朗克质量 m_p = {m_p_paper:.6e} kg")
print(f"CODATA 2018万有引力常数实验值 G_exp = {G_exp:.6e} m³·kg⁻¹·s⁻²")

# 重新计算分子和分母
print(f"\n=== 重新计算验证 ===")
calculated_numerator = hbar_paper * c
print(f"论文中分子 ℏc = {numerator_paper:.16e} J·m")
print(f"实际计算分子 ℏc = {calculated_numerator:.16e} J·m")
print(f"分子一致: {abs(numerator_paper - calculated_numerator) < 1e-26}")

calculated_denominator = m_p_paper ** 2
print(f"\n论文中分母 m_p² = {denominator_paper:.12e} kg²")
print(f"实际计算分母 m_p² = {calculated_denominator:.12e} kg²")
print(f"分母一致: {abs(denominator_paper - calculated_denominator) < 1e-28}")
print(f"分母差异: {abs(denominator_paper - calculated_denominator):.16e} kg²")

# 计算理论值
calculated_G_theo = calculated_numerator / calculated_denominator
print(f"\n论文中理论值 G_theo = {G_theo_paper:.12e} m³·kg⁻¹·s⁻²")
print(f"实际计算理论值 G_theo = {calculated_G_theo:.12e} m³·kg⁻¹·s⁻²")
print(f"理论值一致: {abs(G_theo_paper - calculated_G_theo) < 1e-22}")
print(f"理论值差异: {abs(G_theo_paper - calculated_G_theo):.16e} m³·kg⁻¹·s⁻²")

# 使用论文中的数值计算
paper_calculation = numerator_paper / denominator_paper
print(f"\n=== 使用论文中给出的分子分母计算 ===")
print(f"论文中分子 / 论文中分母 = {paper_calculation:.12e} m³·kg⁻¹·s⁻²")
print(f"与论文理论值一致: {abs(paper_calculation - G_theo_paper) < 1e-22}")

# 计算相对偏差
paper_relative_deviation = abs((G_theo_paper - G_exp) / G_exp) * 100
actual_relative_deviation = abs((calculated_G_theo - G_exp) / G_exp) * 100
print(f"\n=== 相对偏差计算 ===")
print(f"论文中相对偏差: {paper_relative_deviation:.8f}%")
print(f"实际计算相对偏差: {actual_relative_deviation:.8f}%")

# 地球表面重力加速度验证
print("\n=== 地球表面重力加速度计算 ===")
M = 5.972e24  # kg，地球质量
R = 6.371e6  # m，地球平均半径
g_exp = 9.81  # m/s²，实际测量的地球表面重力加速度

# 论文中计算的g_theo
g_theo_paper = 9.818  # m/s²

# 使用论文中的G_theo计算
g_theo_from_paper_G = G_theo_paper * M / (R ** 2)
print(f"使用论文中G_theo计算的g_theo: {g_theo_from_paper_G:.6f} m/s²")
print(f"与论文g_theo一致: {abs(g_theo_from_paper_G - g_theo_paper) < 1e-4}")

# 使用实际计算的G_theo计算
g_theo_from_actual_G = calculated_G_theo * M / (R ** 2)
print(f"使用实际计算G_theo计算的g_theo: {g_theo_from_actual_G:.6f} m/s²")

# 相对误差计算
paper_relative_error = abs((g_theo_paper - g_exp) / g_exp) * 100
actual_relative_error = abs((g_theo_from_actual_G - g_exp) / g_exp) * 100
print(f"\n论文中相对误差: {paper_relative_error:.6f}%")
print(f"实际计算相对误差: {actual_relative_error:.6f}%")
