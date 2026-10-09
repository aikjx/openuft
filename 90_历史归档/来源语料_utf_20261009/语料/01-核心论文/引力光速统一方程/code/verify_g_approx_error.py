#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证Z=0.01近似值时G的误差计算的准确性
"""

# 使用高精度浮点数计算
import decimal

# 设置高精度计算上下文
decimal.getcontext().prec = 30

# 定义常量
Z_exact = decimal.Decimal('0.010004524012147')  # Z精确值
Z_approx = decimal.Decimal('0.01')             # Z近似值
c = decimal.Decimal('299792458')               # 光速
G_codata_2018 = decimal.Decimal('6.67430e-11') # CODATA 2018推荐值

# 使用近似值计算G
G_approx = (2 * Z_approx) / c

# 计算绝对误差和相对误差
absolute_error = abs(G_approx - G_codata_2018)
relative_error = (absolute_error / G_codata_2018) * 100

# 输出详细计算过程和结果
print("=== Z=0.01近似值时G的误差计算验证 ===")
print(f"Z近似值 = {Z_approx}")
print(f"光速c = {c} m/s")
print(f"CODATA 2018 G推荐值 = {G_codata_2018:.15e} m³·kg⁻¹·s⁻²")
print()
print(f"计算G近似值: G = 2×Z/c = 2×{Z_approx}/{c}")
print(f"G近似值 = {G_approx:.15e} m³·kg⁻¹·s⁻²")
print()
print(f"计算绝对误差: |G近似 - G_CODATA| = |{G_approx:.15e} - {G_codata_2018:.15e}|")
print(f"绝对误差 = {absolute_error:.15e}")
print()
print(f"计算相对误差: (绝对误差/G_CODATA)×100% = ({absolute_error}/{G_codata_2018})×100%")
print(f"相对误差 = {relative_error:.10f}%")
print()
print("=== 结论 ===")
print(f"计算结果验证了使用Z=0.01近似值时的相对误差为{relative_error:.10f}%")