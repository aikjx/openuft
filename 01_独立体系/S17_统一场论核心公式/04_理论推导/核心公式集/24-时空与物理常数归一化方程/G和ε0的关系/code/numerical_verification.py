#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数值验证，确认公式与实验值的一致性
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

# 数值验证函数
def numerical_verification():
    """数值验证"""
    # 基本常数
    m_e = 9.10938356e-31  # 电子质量 (kg)
    r_e = 2.8179403262e-15  # 电子经典半径 (m)
    omega = c / r_e  # 角速度
    nu = m_e * c**2 / h  # 频率
    
    print("1. 基本参数:")
    print(f"   电子质量: {m_e:.6e} kg")
    print(f"   电子经典半径: {r_e:.6e} m")
    print(f"   角速度: {omega:.6e} rad/s")
    print(f"   频率: {nu:.6e} Hz")
    print()
    
    print("2. 核心公理验证:")
    print(f"   ωr = {omega * r_e:.6e} m/s")
    print(f"   c = {c:.6e} m/s")
    print(f"   误差: {abs(omega * r_e - c)/c * 100:.6f}%")
    print()
    
    print("3. 双隐含量核心桥梁验证:")
    # 验证右边: m = hν/c²
    m_right = (h * nu) / c**2
    print(f"   右边 (hν/c²): {m_right:.6e} kg")
    print(f"   电子质量: {m_e:.6e} kg")
    print(f"   误差: {abs(m_right - m_e)/m_e * 100:.6f}%")
    
    # 验证左边: m = ω²r³/G
    m_left = (omega**2 * r_e**3) / G
    print(f"   左边 (ω²r³/G): {m_left:.6e} kg")
    print(f"   电子质量: {m_e:.6e} kg")
    print(f"   误差: {abs(m_left - m_e)/m_e * 100:.6f}%")
    print()
    
    print("4. 电荷几何本源恒等式验证:")
    # 验证 e² = 4πε₀ωr²mc
    calculated_e_squared = 4 * pi * epsilon_0 * omega * r_e**2 * m_e * c
    print(f"   计算e²: {calculated_e_squared:.6e} C²")
    print(f"   实验值e²: {e**2:.6e} C²")
    print(f"   误差: {abs(calculated_e_squared - e**2)/e**2 * 100:.6f}%")
    print()
    
    print("5. 全维度统一恒等式验证:")
    # 验证 ω²r³c²/(G h ν) = e²/(4πε₀ G m²)
    left_side = (omega**2 * r_e**3 * c**2) / (G * h * nu)
    right_side = e**2 / (4 * pi * epsilon_0 * G * m_e**2)
    print(f"   左边: {left_side:.6e}")
    print(f"   右边: {right_side:.6e}")
    print(f"   误差: {abs(left_side - right_side)/right_side * 100:.6f}%")
    print()
    
    print("6. 力的强度比验证:")
    force_ratio = e**2 / (4 * pi * epsilon_0 * G * m_e**2)
    print(f"   计算力的强度比: {force_ratio:.6e}")
    print(f"   实验值约为: 4.17e42")
    print(f"   误差: {abs(force_ratio - 4.17e42)/4.17e42 * 100:.6f}%")
    print()
    
    print("7. G的表达式验证:")
    # 从力的强度比解出G
    G_calculated = e**2 / (4 * pi * epsilon_0 * force_ratio * m_e**2)
    print(f"   从力的强度比计算G: {G_calculated:.6e} m³·kg⁻¹·s⁻²")
    print(f"   实验值G: {G:.6e} m³·kg⁻¹·s⁻²")
    print(f"   误差: {abs(G_calculated - G)/G * 100:.6f}%")
    print()
    
    print("8. G和ε0关系表达式验证:")
    # 验证 G = e²/(4πε₀ m²)
    G_expression = e**2 / (4 * pi * epsilon_0 * m_e**2)
    print(f"   从表达式计算G: {G_expression:.6e} m³·kg⁻¹·s⁻²")
    print(f"   实验值G: {G:.6e} m³·kg⁻¹·s⁻²")
    print(f"   误差: {abs(G_expression - G)/G * 100:.6f}%")
    print()
    
    print("9. 电荷e版归一化恒等式验证:")
    # 验证 e²/(4πε₀ r²) = G m²/r²
    left_normalized = e**2 / (4 * pi * epsilon_0 * r_e**2)
    right_normalized = G * m_e**2 / r_e**2
    print(f"   左边: {left_normalized:.6e} N")
    print(f"   右边: {right_normalized:.6e} N")
    print(f"   误差: {abs(left_normalized - right_normalized)/max(left_normalized, right_normalized) * 100:.6f}%")
    print()

# 主函数
def main():
    """主函数"""
    print_header("数值验证")
    numerical_verification()
    print("数值验证完成!")

if __name__ == "__main__":
    main()
