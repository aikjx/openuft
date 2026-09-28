#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证电荷几何本源恒等式
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

# 验证电荷几何本源恒等式
def verify_charge_identity():
    """验证电荷几何本源恒等式 e² = 4πε₀ωr²mc"""
    print("1. 电荷几何本源恒等式验证:")
    
    # 以电子为例
    m_e = 9.10938356e-31  # 电子质量 (kg)
    r_e = 2.8179403262e-15  # 电子经典半径 (m)
    omega = c / r_e  # 角速度
    
    # 计算等式右边
    right_side = 4 * pi * epsilon_0 * omega * r_e**2 * m_e * c
    print(f"   等式右边计算: {right_side:.6e} C²")
    print(f"   元电荷平方实验值: {e**2:.6e} C²")
    print(f"   误差: {abs(right_side - e**2)/e**2 * 100:.6f}%")
    print()
    
    # 验证量纲
    print("   量纲分析:")
    print("   左边 e²: C²")
    print("   右边 4πε₀ωr²mc:")
    print("   ε₀: F/m = C²/(N·m²) = C²·s²/(kg·m³)")
    print("   ω: s⁻¹")
    print("   r²: m²")
    print("   m: kg")
    print("   c: m/s")
    print("   综合: C²·s²/(kg·m³) * s⁻¹ * m² * kg * m/s = C²")
    print("   量纲一致: ✓")
    print()

# 验证从电荷几何本源恒等式推导的G表达式
def verify_g_from_charge_identity():
    """验证从电荷几何本源恒等式推导的G表达式"""
    print("2. 从电荷几何本源恒等式推导G:")
    
    # 以电子为例
    m_e = 9.10938356e-31  # 电子质量 (kg)
    r_e = 2.8179403262e-15  # 电子经典半径 (m)
    omega = c / r_e  # 角速度
    
    # 从电荷几何本源恒等式 e² = 4πε₀ωr²mc 解出G
    # 结合双隐含量核心桥梁 m = ω²r³/G
    # 代入得: e² = 4πε₀ωr²*(ω²r³/G)*c = 4πε₀ω³r⁵c/G
    # 解出: G = 4πε₀ω³r⁵c/e²
    G_calculated = (4 * pi * epsilon_0 * omega**3 * r_e**5 * c) / e**2
    print(f"   从电荷几何本源恒等式计算G: {G_calculated:.6e} m³·kg⁻¹·s⁻²")
    print(f"   实验值G: {G:.6e} m³·kg⁻¹·s⁻²")
    print(f"   误差: {abs(G_calculated - G)/G * 100:.6f}%")
    print()

# 主函数
def main():
    """主函数"""
    print_header("电荷几何本源恒等式验证")
    verify_charge_identity()
    verify_g_from_charge_identity()
    print("验证完成!")

if __name__ == "__main__":
    main()
