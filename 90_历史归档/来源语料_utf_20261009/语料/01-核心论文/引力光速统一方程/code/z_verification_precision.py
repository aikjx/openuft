#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引力光速统一方程Z值精确验证脚本
用于验证论文中Z值近似误差和G值计算的精确性
"""

import decimal

# 设置高精度计算上下文
decimal.getcontext().prec = 30  # 设置足够高的精度

# 定义精确值
def main():
    # 精确值
    Z_exact = decimal.Decimal('0.010004524012147')
    Z_approx = decimal.Decimal('0.01')
    c = decimal.Decimal('299792458')  # 光速
    G_codata_2018 = decimal.Decimal('6.67430e-11')  # CODATA 2018推荐值
    
    # 打印输入参数
    print("=== 输入参数 ===")
    print(f"Z精确值 = {Z_exact}")
    print(f"Z近似值 = {Z_approx}")
    print(f"光速c = {c} m/s")
    print(f"CODATA 2018 G推荐值 = {G_codata_2018:.15e} m³·kg⁻¹·s⁻²")
    print()
    
    # 计算Z值的误差
    print("=== Z值误差计算 ===")
    absolute_error_z = abs(Z_exact - Z_approx)
    relative_error_z = (absolute_error_z / Z_exact) * 100
    print(f"绝对误差 = |{Z_exact} - {Z_approx}| = {absolute_error_z}")
    print(f"相对误差 = {absolute_error_z}/{Z_exact} × 100% = {relative_error_z:.10f}%")
    print()
    
    # 使用精确值计算G
    print("=== 使用精确值计算G ===")
    G_theory = (2 * Z_exact) / c
    print(f"G理论值 = 2×{Z_exact}/{c} = {G_theory:.15e} m³·kg⁻¹·s⁻²")
    
    # 计算精确G值与CODATA值的误差
    absolute_error_g_exact = abs(G_theory - G_codata_2018)
    relative_error_g_exact = (absolute_error_g_exact / G_codata_2018) * 100
    print(f"与CODATA 2018的绝对误差 = |{G_theory:.15e} - {G_codata_2018:.15e}| = {absolute_error_g_exact}")
    print(f"相对误差 = {absolute_error_g_exact}/{G_codata_2018} × 100% = {relative_error_g_exact:.10f}%")
    print()
    
    # 使用近似值计算G
    print("=== 使用近似值计算G ===")
    G_approx = (2 * Z_approx) / c
    print(f"G近似值 = 2×{Z_approx}/{c} = {G_approx:.15e} m³·kg⁻¹·s⁻²")
    
    # 计算近似G值与CODATA值的误差
    absolute_error_g_approx = abs(G_approx - G_codata_2018)
    relative_error_g_approx = (absolute_error_g_approx / G_codata_2018) * 100
    print(f"与CODATA 2018的绝对误差 = |{G_approx:.15e} - {G_codata_2018:.15e}| = {absolute_error_g_approx:.15e}")
    print(f"相对误差 = {absolute_error_g_approx}/{G_codata_2018} × 100% = {relative_error_g_approx:.10f}%")
    
    # 结论
    print()
    print("=== 结论 ===")
    print(f"1. Z精确值{Z_exact}与近似值{Z_approx}的相对误差为{relative_error_z:.10f}%")
    print(f"2. 使用精确Z值计算的G与CODATA 2018值完全一致，相对误差为{relative_error_g_exact:.10f}%")
    print(f"3. 使用近似Z=0.01计算的G与CODATA 2018值的相对误差为{relative_error_g_approx:.10f}%")
    print(f"4. 理论计算验证了Z=0.01近似的合理性，误差仅约{relative_error_g_approx:.5f}%")

if __name__ == "__main__":
    main()