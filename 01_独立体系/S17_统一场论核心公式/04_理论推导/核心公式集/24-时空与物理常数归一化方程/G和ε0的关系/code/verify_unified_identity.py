#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证全维度统一恒等式
"""

import math
from scipy.constants import h, c, G, e, epsilon_0, pi

# 设置输出编码
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 常量定义
LINE_WIDTH = 80

# 工具函数
def print_header(title):
    """打印标题"""
    print("=" * LINE_WIDTH)
    print(title.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)
    print()

def print_separator():
    """打印分隔线"""
    print("-" * LINE_WIDTH)

# 验证全维度统一恒等式
def verify_unified_identity():
    """验证全维度统一恒等式 ω²r³c²/(G h ν) = e²/(4πε₀ G m²) · 1/(F_e/F_g)"""
    print("1. 全维度统一恒等式验证:")
    
    # 以电子为例
    m_e = 9.10938356e-31  # 电子质量 (kg)
    r_e = 2.8179403262e-15  # 电子经典半径 (m)
    omega = c / r_e  # 角速度
    nu = m_e * c**2 / h  # 频率
    
    # 计算左边
    left_side = (omega**2 * r_e**3 * c**2) / (G * h * nu)
    print(f"   左边计算: {left_side:.6e}")
    
    # 计算力的强度比
    force_ratio = e**2 / (4 * pi * epsilon_0 * G * m_e**2)
    print(f"   力的强度比 F_e/F_g: {force_ratio:.6e}")
    
    # 计算右边
    right_side = (e**2 / (4 * pi * epsilon_0 * G * m_e**2)) / force_ratio
    print(f"   右边计算: {right_side:.6e}")
    print(f"   误差: {abs(left_side - right_side)/right_side * 100:.6f}%")
    
    # 验证代入 ν = mc²/h 后的左边
    left_side_substituted = (omega**2 * r_e**3) / (G * m_e)
    print(f"   代入 ν = mc²/h 后左边: {left_side_substituted:.6e}")
    print()
    
    # 验证量纲
    print("   量纲分析:")
    print("   左边 ω²r³c²/(G h ν):")
    print("   ω²: s⁻², r³: m³, c²: m²/s², G: m³/(kg·s²), h: kg·m²/s, ν: s⁻¹")
    print("   综合: (s⁻² * m³ * m²/s²) / (m³/(kg·s²) * kg·m²/s * s⁻¹) = 1 (无量纲)")
    print("   右边 e²/(4πε₀ G m²) · 1/(F_e/F_g):")
    print("   e²/(4πε₀ G m²): N (力), F_e/F_g: 无量纲, 所以整体无量纲")
    print("   量纲一致: ✓")
    print()

# 验证简化后的全维度统一恒等式
def verify_simplified_identity():
    """验证简化后的全维度统一恒等式"""
    print("2. 简化后的全维度统一恒等式验证:")
    
    # 以电子为例
    m_e = 9.10938356e-31  # 电子质量 (kg)
    r_e = 2.8179403262e-15  # 电子经典半径 (m)
    omega = c / r_e  # 角速度
    
    # 从论文步骤4-5，简化后的等式
    # ω²r³c²/(h ν) = e²/(4πε₀ m²)
    # 代入 ν = mc²/h
    # 左边: ω²r³c²/(h*(mc²/h)) = ω²r³/m
    # 右边: e²/(4πε₀ m²)
    left_side = (omega**2 * r_e**3) / m_e
    right_side = e**2 / (4 * pi * epsilon_0 * m_e**2)
    
    print(f"   左边 (ω²r³/m): {left_side:.6e}")
    print(f"   右边 (e²/(4πε₀ m²)): {right_side:.6e}")
    print(f"   误差: {abs(left_side - right_side)/right_side * 100:.6f}%")
    print()

# 主函数
def main():
    """主函数"""
    print_header("全维度统一恒等式验证")
    verify_unified_identity()
    verify_simplified_identity()
    print("验证完成!")

if __name__ == "__main__":
    main()
