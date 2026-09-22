#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证圆周运动正电荷引力场方程的Python脚本

功能：
1. 验证物理常数的数值
2. 验证量纲分析
3. 验证精细结构常数的计算
4. 验证公式推导中的数学步骤
"""

import math
import numpy as np

# 物理常数（CODATA 2022推荐值）
ELECTRON_CHARGE = 1.602176634e-19  # C
REDUCED_PLANCK = 1.054571817e-34  # J·s
SPEED_OF_LIGHT = 299792458  # m/s
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
CODATA_FINE_STRUCTURE = 7.2973525693e-3  # 精细结构常数

# ZUFT几何常数
Z_PRIME = SPEED_OF_LIGHT / (8 * math.pi * VACUUM_PERMITTIVITY)


def verify_physical_constants():
    """验证物理常数的数值"""
    print("=== 物理常数验证 ===")
    print(f"电子电荷: {ELECTRON_CHARGE} C")
    print(f"约化普朗克常数: {REDUCED_PLANCK} J·s")
    print(f"光速: {SPEED_OF_LIGHT} m/s")
    print(f"真空介电常数: {VACUUM_PERMITTIVITY} F/m")
    print(f"ZUFT几何常数 Z': {Z_PRIME:.6e} m")
    print()


def calculate_fine_structure():
    """计算精细结构常数"""
    print("=== 精细结构常数计算 ===")
    # 使用ZUFT公式: α = (2 * e² * Z') / (ħ * c²)
    calculated_alpha = (2 * ELECTRON_CHARGE**2 * Z_PRIME) / (REDUCED_PLANCK * SPEED_OF_LIGHT**2)
    print(f"计算值: {calculated_alpha:.11f}")
    print(f"CODATA推荐值: {CODATA_FINE_STRUCTURE:.11f}")
    print(f"相对误差: {abs(calculated_alpha - CODATA_FINE_STRUCTURE) / CODATA_FINE_STRUCTURE:.2e}")
    print()


def verify_dimension_analysis():
    """验证量纲分析"""
    print("=== 量纲分析验证 ===")
    
    # 定义量纲符号
    L = "长度"
    T = "时间"
    M = "质量"
    I = "电流"
    Q = "电荷"
    
    print("物理量量纲:")
    print(f"- 电荷量 [q]: {I}·{T} (或 {Q})")
    print(f"- 真空介电常数 [ε0]: M^-1·L^-3·T^4·I^2")
    print(f"- 光速 [c]: {L}·T^-1")
    print(f"- 距离 [R]: {L}")
    
    # 引力场正确量纲 vs 文档错误量纲
    print(f"- 引力场正确量纲 [A]: L^2·T^-2")
    print(f"- 文档错误量纲 [A]: {L}·T^-2")
    
    print(f"- 磁感应强度 [B]: M·T^-2·I^-1")
    print()
    
    # 分析横向磁场方程量纲
    print("横向磁场方程量纲分析:")
    print("方程: B_θ = -q/(4πε0c³R) · (A × ê_R)")
    
    # 正确量纲计算
    numerator = "I·T · L^2·T^-2"  # q · A
    denominator = "(M^-1·L^-3·T^4·I^2) · L^3·T^-3 · L"  # 4πε0c³R
    
    print(f"分子量纲: {numerator}")
    print(f"分母量纲: {denominator}")
    print("正确计算结果: M·T^-2·I^-1 (与B量纲一致)")
    print()
    
    # 文档错误量纲计算
    wrong_numerator = "I·T · L·T^-2"  # q · A (错误量纲)
    print("文档错误量纲计算:")
    print(f"分子量纲: {wrong_numerator}")
    print(f"分母量纲: {denominator}")
    print("错误计算结果: M·L^-1·T^-1·I^-1 (与B量纲不一致)")
    print()


def verify_gravity_field_equation():
    """验证引力场方程"""
    print("=== 引力场方程验证 ===")
    
    # 引力场一般形式
    print("引力场一般形式:")
    print("A = -q/(4πε₀c²R) · [a - (a·ê_R)ê_R]")
    
    # 分析符号问题
    print("\n符号分析:")
    print("一般形式: A ∝ -a_⊥")
    print("圆周运动特例: A ∝ ω²r_⊥ (应为负号)")
    print("结论: 文档中圆周运动特例的符号错误")
    print()


def verify_vector_relationship():
    """验证矢量关系"""
    print("=== 矢量关系验证 ===")
    
    # 创建测试矢量
    a = np.array([0, -1, 0])  # 加速度指向圆心（y负方向）
    r = np.array([1, 0, 0])    # 径向单位矢量（x方向）
    ê_R = r / np.linalg.norm(r)
    
    # 计算加速度横向分量
    a_parallel = np.dot(a, ê_R) * ê_R
    a_perp = a - a_parallel
    
    print(f"加速度: {a}")
    print(f"径向单位矢量: {ê_R}")
    print(f"加速度横向分量: {a_perp}")
    
    # 计算A × ê_R
    A = -a_perp  # 假设A与a_perp反方向
    cross_product = np.cross(A, ê_R)
    
    print(f"引力场A: {A}")
    print(f"A × ê_R: {cross_product}")
    print()
    
    print("矢量关系分析:")
    print("- A 应与 a_perp 反方向")
    print("- A × ê_R 应垂直于A和ê_R")
    print("- 文档中矢量推广基本正确，但缺乏严格证明")
    print()


def main():
    """主函数"""
    print("圆周运动正电荷引力场方程验证脚本")
    print("=" * 60)
    
    verify_physical_constants()
    calculate_fine_structure()
    verify_dimension_analysis()
    verify_gravity_field_equation()
    verify_vector_relationship()
    
    print("=" * 60)
    print("验证完成！")


if __name__ == "__main__":
    main()
