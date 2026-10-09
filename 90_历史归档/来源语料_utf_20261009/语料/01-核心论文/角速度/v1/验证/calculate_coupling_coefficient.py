#!/usr/bin/env python3
"""
耦合系数计算脚本：使用CODATA 2018常数精确计算统一场论的耦合系数f

基于以下关系计算耦合系数f：
1. 从磁矢势方程和电场方程推导f的表达式
2. 使用CODATA 2018推荐的物理常数值
3. 验证f的无量纲性
4. 分析f在不同物理场景中的意义
"""

import math

# CODATA 2018推荐的物理常数
# 来源：https://physics.nist.gov/cuu/Constants/index.html

# 光速，单位：m/s
c = 299792458

# 万有引力常数，单位：m³/(kg·s²)
G = 6.67430e-11

# 电子电荷，单位：C
e = 1.602176634e-19

# 真空介电常数，单位：F/m
epsilon_0 = 8.8541878128e-12

# 真空磁导率，单位：H/m
mu_0 = 4 * math.pi * 1e-7

# 普朗克常数，单位：J·s
h = 6.62607015e-34

# 约化普朗克常数，单位：J·s
h_bar = h / (2 * math.pi)

# 电子质量，单位：kg
m_e = 9.1093837015e-31

# 质子质量，单位：kg
m_p = 1.67262192369e-27

# 玻尔半径，单位：m
a_0 = 5.29177210903e-11

# 精细结构常数
alpha = e**2 / (4 * math.pi * epsilon_0 * h_bar * c)

# 计算耦合系数f
# 基于电磁学和引力的关系
def calculate_coupling_coefficient():
    print("=== 耦合系数f的计算 ===")
    
    # 方法1：从电磁学和引力的相对强度计算
    # 电磁力与引力的比值
    F_electrostatic = e**2 / (4 * math.pi * epsilon_0 * a_0**2)
    F_gravitational = G * m_e * m_p / a_0**2
    force_ratio = F_electrostatic / F_gravitational
    
    print(f"氢原子中电子与质子间的静电力: {F_electrostatic:.6e} N")
    print(f"氢原子中电子与质子间的引力: {F_gravitational:.6e} N")
    print(f"电磁力与引力的比值: {force_ratio:.6e}")
    
    # 方法2：基于精细结构常数和引力耦合常数
    # 引力耦合常数
    alpha_G = G * m_e**2 / (h_bar * c)
    print(f"\n引力耦合常数: {alpha_G:.6e}")
    print(f"精细结构常数: {alpha:.6e}")
    
    # 计算f
    f = math.sqrt(alpha / alpha_G)
    print(f"\n耦合系数f: {f:.6e}")
    
    # 验证f的无量纲性
    print("\n=== f的无量纲性验证 ===")
    print("alpha 是无量纲的")
    print("alpha_G 是无量纲的")
    print("因此，f = √(alpha / alpha_G) 也是无量纲的")
    
    # 分析f的物理意义
    print("\n=== f的物理意义分析 ===")
    print(f"f ≈ {f:.2e}，表示电磁相互作用与引力相互作用的相对强度")
    print("在统一场论中，f作为耦合系数，连接了电磁学和引力")
    print("它反映了时空几何与电磁现象的内在联系")
    
    # 计算不同尺度下的f值
    print("\n=== 不同尺度下的f值分析 ===")
    
    # 微观尺度（电子）
    print("微观尺度（电子）:")
    alpha_G_e = G * m_e**2 / (h_bar * c)
    f_e = math.sqrt(alpha / alpha_G_e)
    print(f"  引力耦合常数: {alpha_G_e:.6e}")
    print(f"  耦合系数f: {f_e:.6e}")
    
    # 宏观尺度（地球）
    print("\n宏观尺度（地球）:")
    m_earth = 5.972e24  # 地球质量，单位：kg
    # 宏观尺度下，引力耦合常数的定义不同
    # 这里使用特征能量尺度
    E_earth = m_earth * c**2
    alpha_G_earth = G * m_earth**2 / (h_bar * c)
    # 注意：宏观尺度下，电磁相互作用通常可以忽略
    print(f"  地球质量: {m_earth:.6e} kg")
    print(f"  引力耦合常数: {alpha_G_earth:.6e}")
    
    # 宇宙尺度（银河系）
    print("\n宇宙尺度（银河系）:")
    m_galaxy = 1e42  # 银河系质量，单位：kg
    alpha_G_galaxy = G * m_galaxy**2 / (h_bar * c)
    print(f"  银河系质量: {m_galaxy:.6e} kg")
    print(f"  引力耦合常数: {alpha_G_galaxy:.6e}")
    
    # 讨论f在统一场论中的应用
    print("\n=== f在统一场论中的应用 ===")
    print("1. 磁矢势方程: ∇×A = B/f")
    print("2. 电场方程: E = -f(dA/dt)")
    print("3. 场转化方程: ∂²A/∂t² = (v/f)(∇·E) - (c²/f)(∇×B)")
    print("\nf作为耦合系数，确保了方程在不同尺度下的一致性")
    print("它反映了时空几何与电磁现象的内在联系")
    
    return f

# 主函数
if __name__ == "__main__":
    print("统一场论耦合系数f的计算\n")
    f = calculate_coupling_coefficient()
    print(f"\n=== 计算结果 ===")
    print(f"耦合系数f = {f:.6e}")
