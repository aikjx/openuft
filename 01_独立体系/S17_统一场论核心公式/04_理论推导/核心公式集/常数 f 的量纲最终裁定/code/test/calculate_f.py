#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论常数f的数值计算

功能：
1. 计算统一场论耦合常数f的数值
2. 验证f与引力几何常数Z和电磁几何常数Z'的关系
3. 验证等式 1/(4πε₀G) = (c/(2f))²

引用：
张祥前统一场论耦合常数f的全面验证：量纲分析、数值计算与多维向量导数证明
"""

import math
import numpy as np
from scipy import constants


def calculate_f():
    """计算统一场论耦合常数f"""
    print("=== 张祥前统一场论常数f的数值计算 ===")
    print("基于基本物理常数：光速c、真空介电常数ε₀、万有引力常数G")
    print("=" * 60)
    
    # 基本常数（CODATA 2018）
    c = constants.speed_of_light  # 光速，单位：m/s
    epsilon0 = constants.epsilon_0  # 真空介电常数，单位：F/m
    G = constants.gravitational_constant  # 万有引力常数，单位：m³/kg/s²
    
    print(f"光速 c = {c} m/s")
    print(f"真空介电常数 ε₀ = {epsilon0:.12e} F/m")
    print(f"万有引力常数 G = {G:.10e} m³/kg/s²")
    print("=" * 60)
    
    # 计算步骤1：计算4πε₀G
    term1 = 4 * np.pi * epsilon0 * G
    print(f"1. 4π ε₀ G = {term1:.10e}")
    
    # 计算步骤2：计算平方根
    sqrt_term = np.sqrt(term1)
    print(f"2. sqrt(4π ε₀ G) = {sqrt_term:.10e}")
    
    # 计算步骤3：计算f的最终值
    f = (c / 2) * sqrt_term
    print(f"3. f = (c/2) * sqrt(4π ε₀ G) = {f:.10e} kg/A")
    print(f"   约等于：{f:.6f} kg/A")
    
    print("=" * 60)
    
    # 验证f与Z、Z'的关系
    print("=== 验证f与几何耦合常数Z、Z'的关系 ===")
    Z = (G * c) / 2  # 引力耦合常数
    Z_prime = c / (8 * np.pi * epsilon0)  # 电磁耦合常数
    print(f"引力几何常数 Z = {Z:.10e} m⁴/kg/s³")
    print(f"电磁几何常数 Z' = {Z_prime:.10e} kg·m⁴/s⁵/A²")
    
    f_from_Z = (c / 2) * np.sqrt(Z / Z_prime)
    print(f"从Z和Z'计算f：{f_from_Z:.10e} kg/A")
    print(f"相对误差：{(f_from_Z - f)/f:.2e}")
    
    print("=" * 60)
    
    # 验证等式 1/(4πε₀G) = (c/(2f))²
    print("=== 验证等式 1/(4πε₀G) = (c/(2f))² ===")
    left_side = 1 / (4 * np.pi * epsilon0 * G)
    right_side = (c / (2 * f)) ** 2
    print(f"左边 1/(4π ε₀ G) = {left_side:.10e}")
    print(f"右边 (c/(2f))² = {right_side:.10e}")
    print(f"相对误差：{(right_side - left_side)/left_side:.2e}")
    print(f"验证结果：{'✓ 等式成立' if abs((right_side - left_side)/left_side) < 1e-10 else '✗ 等式不成立'}")
    
    print("=" * 60)
    
    return f


if __name__ == "__main__":
    calculate_f()
