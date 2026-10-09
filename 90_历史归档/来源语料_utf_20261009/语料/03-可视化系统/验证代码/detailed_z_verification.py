#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细验证张祥前常数Z的精确值
通过计算确认正确的Z值，比较新旧值的差异
"""
import numpy as np

# 已知常数
G_codata_2018 = 6.67430e-11  # m³·kg⁻¹·s⁻² (CODATA 2018推荐值)
c = 299792458                # m·s⁻¹ (光速)

# 项目中广泛使用的Z值
Z_project = 0.0100065  # kg⁻¹·m⁴·s⁻³

# 根据引力光速统一方程Z = (G * c) / 2 计算精确Z值
Z_calculated = (G_codata_2018 * c) / 2

# 输出详细计算结果
print("===== 张祥前常数Z的精确值验证 =====")
print(f"使用CODATA 2018推荐值 G = {G_codata_2018} m³·kg⁻¹·s⁻²")
print(f"光速 c = {c} m·s⁻¹")
print(f"\n根据公式 Z = (G * c) / 2 计算:")
print(f"Z = ({G_codata_2018} * {c}) / 2")
print(f"Z = {G_codata_2018 * c} / 2")
print(f"Z = {Z_calculated} kg⁻¹·m⁴·s⁻³ (精确计算值)")
print(f"\n项目中使用的值: Z = {Z_project} kg⁻¹·m⁴·s⁻³")

# 计算差异
absolute_diff = abs(Z_calculated - Z_project)
relative_diff = (absolute_diff / Z_calculated) * 100

print(f"\n两者差异:")
print(f"绝对误差: {absolute_diff}")
print(f"相对误差: {relative_diff:.6f}%")

# 验证反向计算: 使用不同Z值计算G，与CODATA值比较
G_from_calculated = (2 * Z_calculated) / c
G_from_project = (2 * Z_project) / c

print(f"\n===== 反向验证: 使用Z值计算G =====")
print(f"使用精确Z值计算G: G = (2 * {Z_calculated}) / {c} = {G_from_calculated} m³·kg⁻¹·s⁻²")
print(f"与CODATA值的差异: {abs(G_from_calculated - G_codata_2018)}")
print(f"\n使用项目中Z值计算G: G = (2 * {Z_project}) / {c} = {G_from_project} m³·kg⁻¹·s⁻²")
print(f"与CODATA值的差异: {abs(G_from_project - G_codata_2018)}")

# 结论
print(f"\n===== 结论 =====")
print(f"正确的张祥前常数Z值应为: {Z_calculated}")
print(f"为了保持公式G=2Z/c与CODATA 2018值的一致性，应使用此精确值。")
print("所有相关文件中的Z值0.0100065应更新为此精确值。")