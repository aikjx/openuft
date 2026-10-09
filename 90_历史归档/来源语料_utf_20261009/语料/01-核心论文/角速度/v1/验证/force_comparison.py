#!/usr/bin/env python3
"""
力的相对强度比较脚本

计算10个经典情况下引力与其他力的大小，比较它们的相对强度
"""

import math

# 物理常数（CODATA 2022推荐值）
G = 6.67430e-11  # 万有引力常数，单位：m³/(kg·s²)
e = 1.602176634e-19  # 电子电荷，单位：C
epsilon_0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
m_e = 9.1093837015e-31  # 电子质量，单位：kg
m_p = 1.67262192369e-27  # 质子质量，单位：kg
m_n = 1.67492749804e-27  # 中子质量，单位：kg
c = 299792458  # 光速，单位：m/s
h_bar = 1.054571817e-34  # 约化普朗克常数，单位：J·s

# 计算引力

def calculate_gravitational_force(m1, m2, r):
    """计算两个物体间的引力
    
    参数：
        m1: 物体1的质量，单位：kg
        m2: 物体2的质量，单位：kg
        r: 两物体间的距离，单位：m
    
    返回：
        引力大小，单位：N
    """
    return G * m1 * m2 / (r ** 2)

# 计算静电力
def calculate_electrostatic_force(q1, q2, r):
    """计算两个电荷间的静电力
    
    参数：
        q1: 电荷1的电量，单位：C
        q2: 电荷2的电量，单位：C
        r: 两电荷间的距离，单位：m
    
    返回：
        静电力大小，单位：N
    """
    return (q1 * q2) / (4 * math.pi * epsilon_0 * r ** 2)

# 计算核力（近似）
def calculate_nuclear_force(r):
    """近似计算核力大小
    
    参数：
        r: 核子间的距离，单位：m
    
    返回：
        核力大小，单位：N
    """
    # 核力的近似形式，使用汤川势
    if r > 1e-15:  # 核力作用范围约为1飞米
        return 0
    else:
        # 核力强度约为10^4 N在近距离
        return 1e4 * math.exp(-r / 1e-15)

# 计算场景1：氢原子中电子与质子间的引力与静电力
def scenario1():
    print("=== 场景1：氢原子中电子与质子间的力 ===")
    r = 5.29177e-11  # 玻尔半径，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_e, m_p, r)
    
    # 计算静电力
    F_elec = calculate_electrostatic_force(e, -e, r)
    
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print(f"静电力: {abs(F_elec):.6e} N")
    print(f"静电力与引力的比值: {abs(F_elec)/F_grav:.6e}")
    print()

# 计算场景2：地球表面物体的重力与电磁力
def scenario2():
    print("=== 场景2：地球表面物体的力 ===")
    m_earth = 5.972e24  # 地球质量，单位：kg
    r_earth = 6.371e6  # 地球半径，单位：m
    m_object = 1.0  # 物体质量，单位：kg
    
    # 计算重力
    F_grav = calculate_gravitational_force(m_earth, m_object, r_earth)
    
    # 估计物体间的电磁力（假设两个1kg物体各带1μC电荷，距离1m）
    q = 1e-6  # 电荷，单位：C
    r = 1.0  # 距离，单位：m
    F_elec = calculate_electrostatic_force(q, q, r)
    
    print(f"地球质量: {m_earth:.6e} kg")
    print(f"物体质量: {m_object:.6e} kg")
    print(f"重力: {F_grav:.6e} N")
    print(f"两个1kg带电物体(1μC)间的电磁力: {F_elec:.6e} N")
    print()

# 计算场景3：地球与太阳间的引力
def scenario3():
    print("=== 场景3：地球与太阳间的引力 ===")
    m_earth = 5.972e24  # 地球质量，单位：kg
    m_sun = 1.989e30  # 太阳质量，单位：kg
    r = 1.496e11  # 日地距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_earth, m_sun, r)
    
    print(f"地球质量: {m_earth:.6e} kg")
    print(f"太阳质量: {m_sun:.6e} kg")
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print()

# 计算场景4：月球与地球间的引力
def scenario4():
    print("=== 场景4：月球与地球间的引力 ===")
    m_moon = 7.342e22  # 月球质量，单位：kg
    m_earth = 5.972e24  # 地球质量，单位：kg
    r = 3.844e8  # 地月距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_moon, m_earth, r)
    
    print(f"月球质量: {m_moon:.6e} kg")
    print(f"地球质量: {m_earth:.6e} kg")
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print()

# 计算场景5：两个质子间的引力与核力
def scenario5():
    print("=== 场景5：两个质子间的力 ===")
    r = 1e-15  # 核子间距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_p, m_p, r)
    
    # 计算静电力
    F_elec = calculate_electrostatic_force(e, e, r)
    
    # 计算核力
    F_nuclear = calculate_nuclear_force(r)
    
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print(f"静电力: {F_elec:.6e} N")
    print(f"核力: {F_nuclear:.6e} N")
    print(f"核力与引力的比值: {F_nuclear/F_grav:.6e}")
    print()

# 计算场景6：两个电子间的引力与静电力
def scenario6():
    print("=== 场景6：两个电子间的力 ===")
    r = 1e-10  # 电子间距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_e, m_e, r)
    
    # 计算静电力
    F_elec = calculate_electrostatic_force(e, e, r)
    
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print(f"静电力: {F_elec:.6e} N")
    print(f"静电力与引力的比值: {F_elec/F_grav:.6e}")
    print()

# 计算场景7：木星与太阳间的引力
def scenario7():
    print("=== 场景7：木星与太阳间的引力 ===")
    m_jupiter = 1.898e27  # 木星质量，单位：kg
    m_sun = 1.989e30  # 太阳质量，单位：kg
    r = 7.785e11  # 木星到太阳的距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_jupiter, m_sun, r)
    
    print(f"木星质量: {m_jupiter:.6e} kg")
    print(f"太阳质量: {m_sun:.6e} kg")
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print()

# 计算场景8：中子星表面的引力
def scenario8():
    print("=== 场景8：中子星表面的引力 ===")
    m_neutron = 1.4 * 1.989e30  # 中子星质量，单位：kg（约1.4倍太阳质量）
    r_neutron = 1e4  # 中子星半径，单位：m
    m_object = 1.0  # 物体质量，单位：kg
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_neutron, m_object, r_neutron)
    
    print(f"中子星质量: {m_neutron:.6e} kg")
    print(f"中子星半径: {r_neutron:.6e} m")
    print(f"物体质量: {m_object:.6e} kg")
    print(f"引力: {F_grav:.6e} N")
    print()

# 计算场景9：黑洞视界附近的引力
def scenario9():
    print("=== 场景9：黑洞视界附近的引力 ===")
    m_blackhole = 10 * 1.989e30  # 黑洞质量，单位：kg（约10倍太阳质量）
    r_schwarzschild = 2 * G * m_blackhole / c**2  # 史瓦西半径，单位：m
    m_object = 1.0  # 物体质量，单位：kg
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_blackhole, m_object, r_schwarzschild)
    
    print(f"黑洞质量: {m_blackhole:.6e} kg")
    print(f"史瓦西半径: {r_schwarzschild:.6e} m")
    print(f"物体质量: {m_object:.6e} kg")
    print(f"引力: {F_grav:.6e} N")
    print()

# 计算场景10：银河系中心与太阳间的引力
def scenario10():
    print("=== 场景10：银河系中心与太阳间的引力 ===")
    m_galaxy = 4.1e6 * 1.989e30  # 银河系中心质量，单位：kg（约410万倍太阳质量）
    m_sun = 1.989e30  # 太阳质量，单位：kg
    r = 8.2 * 3.086e19  # 太阳到银心的距离，单位：m
    
    # 计算引力
    F_grav = calculate_gravitational_force(m_galaxy, m_sun, r)
    
    print(f"银河系中心质量: {m_galaxy:.6e} kg")
    print(f"太阳质量: {m_sun:.6e} kg")
    print(f"距离: {r:.6e} m")
    print(f"引力: {F_grav:.6e} N")
    print()

# 主函数
def main():
    print("=== 10个经典情况下力的相对强度比较 ===")
    print()
    
    scenario1()
    scenario2()
    scenario3()
    scenario4()
    scenario5()
    scenario6()
    scenario7()
    scenario8()
    scenario9()
    scenario10()
    
    print("=== 比较总结 ===")
    print("1. 微观尺度（原子、核子）：电磁力和核力远大于引力")
    print("2. 宏观尺度（地球、太阳系）：引力主导")
    print("3. 极端天体（中子星、黑洞）：引力极强")
    print("4. 宇宙尺度（星系）：引力主导大尺度结构")
    print("5. 统一场论需要在不同尺度下正确描述这些力的相对强度")

if __name__ == "__main__":
    main()
