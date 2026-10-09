#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证统一场论中万有引力常数与光速涌现性论文的数值计算正确性
"""

# CODATA 2018基本常数
hbar = 1.0545718176461565e-34  # J·s
c = 299792458  # m/s
m_p = 2.176434e-8  # kg
G_exp = 6.67430e-11  # m³·kg⁻¹·s⁻² (CODATA 2018)

# 地球基本参数
M_earth = 5.972e24  # kg
R_earth = 6.371e6  # m
g_exp = 9.81  # m/s²

print("=== 验证万有引力常数计算 ===")
# 计算G理论值
g_num = hbar * c / (m_p ** 2)
print(f"计算得到的G: {g_num:.10e} m³·kg⁻¹·s⁻²")
print(f"论文中的G: 6.6743021e-11 m³·kg⁻¹·s⁻²")
print(f"CODATA 2018实验值: {G_exp:.10e} m³·kg⁻¹·s⁻²")

# 计算相对偏差
relative_deviation = abs((g_num - G_exp) / G_exp) * 100
print(f"相对偏差: {relative_deviation:.10f}%")
print(f"论文中的相对偏差: 0.00003149%")
print()

print("=== 验证地球表面重力加速度计算 ===")
# 计算g理论值
g_theo = g_num * M_earth / (R_earth ** 2)
print(f"计算得到的g: {g_theo:.6f} m/s²")
print(f"论文中的g: 9.81998 m/s²")
print(f"实际测量值: {g_exp} m/s²")

# 计算相对误差
relative_error = abs((g_theo - g_exp) / g_exp) * 100
print(f"相对误差: {relative_error:.6f}%")
print(f"论文中的相对误差: 0.1017%")
print()

print("=== 验证量子比例常数k ===")
k = 4 * 3.14159265359 * m_p
print(f"k = 4π m_p: {k:.10e} kg")

# 计算基于k的G
G_from_k = (16 * (3.14159265359 ** 2) * hbar * c) / (k ** 2)
print(f"基于k计算的G: {G_from_k:.10e} m³·kg⁻¹·s⁻²")
print(f"与标准G的偏差: {abs((G_from_k - G_exp) / G_exp) * 100:.10f}%")
