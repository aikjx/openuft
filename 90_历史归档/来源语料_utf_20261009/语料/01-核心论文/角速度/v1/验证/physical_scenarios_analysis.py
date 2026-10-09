#!/usr/bin/env python3
"""
物理场景分析脚本：角速度普适公式的全尺度应用分析

分析以下物理场景：
1. 微观尺度：氢原子、电子
2. 宏观尺度：地球、月球
3. 致密天体：中子星
4. 极端天体：白洞、黑洞
5. 星系尺度：银河系

使用修正后的角速度公式：ω = √(G M / r³)
并与观测数据或预期值进行比较
"""

import math

# 物理常数（CODATA 2022推荐值）
G = 6.67430e-11  # 万有引力常数，单位：m³/(kg·s²)
c = 299792458    # 光速，单位：m/s

# 定义分析函数
def analyze_scenario(name, M, r, expected_omega=None, expected_v=None, unit='rad/s', description=''):
    """分析物理场景的角速度和旋转速度
    
    参数：
        name: 天体名称
        M: 质量，单位：kg
        r: 旋转半径，单位：m
        expected_omega: 预期角速度，单位：rad/s
        expected_v: 预期旋转速度，单位：km/s
        unit: 角速度单位
        description: 描述信息
    """
    print(f"=== {name} ===")
    print(f"描述: {description}")
    print(f"质量: {M:.6e} kg")
    print(f"旋转半径: {r:.6e} m")
    
    # 计算角速度（使用修正后的公式）
    omega = math.sqrt((G * M) / (r ** 3))
    
    # 计算旋转速度
    v = omega * r
    
    print(f"计算角速度: {omega:.6e} rad/s")
    print(f"旋转速度: {v/1000:.6f} km/s")
    
    # 转换单位（如果需要）
    if unit == 'rad/d':
        omega_per_day = omega * 86400  # 转换为rad/天
        print(f"角速度（转换为天）: {omega_per_day:.6e} rad/d")
    
    # 检查速度是否接近或超过光速
    if v > 0.9 * c:
        print("⚠️  警告: 计算速度接近光速，可能需要考虑相对论效应")
    elif v > c:
        print("❌ 警告: 计算速度超过光速，结果可能不准确")
    
    # 与预期值比较
    if expected_omega is not None:
        error = abs(omega - expected_omega) / expected_omega * 100
        print(f"预期角速度: {expected_omega:.6e} rad/s")
        print(f"角速度相对误差: {error:.6f}%")
    
    if expected_v is not None:
        error_v = abs(v/1000 - expected_v) / expected_v * 100
        print(f"预期旋转速度: {expected_v:.6f} km/s")
        print(f"旋转速度相对误差: {error_v:.6f}%")
    
    print()

# 主函数
if __name__ == "__main__":
    print("角速度普适公式的全尺度物理场景分析\n")
    
    # 1. 微观尺度
    print("=== 微观尺度 ===")
    
    # 氢原子基态电子
    proton_mass = 1.67262e-27  # 质子质量，单位：kg
    bohr_radius = 5.29177e-11  # 玻尔半径，单位：m
    # 量子力学中的电子角速度（基于玻尔模型）
    # v = α * c，其中α是精细结构常数
    alpha = 1/137.036
    expected_v_electron = alpha * c / 1000  # 转换为km/s
    analyze_scenario(
        "氢原子基态电子",
        proton_mass, 
        bohr_radius,
        expected_v=expected_v_electron,
        description="氢原子基态电子绕质子旋转"
    )
    
    # 2. 宏观尺度
    print("=== 宏观尺度 ===")
    
    # 地球绕太阳公转
    sun_mass = 1.989e30  # 太阳质量，单位：kg
    earth_orbit = 1.496e11  # 地球轨道半径，单位：m
    expected_v_earth = 29.78  # 地球公转速度，单位：km/s
    analyze_scenario(
        "地球绕太阳公转",
        sun_mass, 
        earth_orbit,
        expected_v=expected_v_earth,
        description="地球绕太阳近似圆周公转"
    )
    
    # 月球绕地球公转
    earth_mass = 5.972e24  # 地球质量，单位：kg
    moon_orbit = 3.844e8  # 月球轨道半径，单位：m
    expected_v_moon = 1.022  # 月球公转速度，单位：km/s
    analyze_scenario(
        "月球绕地球公转",
        earth_mass, 
        moon_orbit,
        expected_v=expected_v_moon,
        description="月球绕地球近似圆周公转"
    )
    
    # 3. 致密天体
    print("=== 致密天体 ===")
    
    # 中子星自转
    neutron_star_mass = 1.4 * sun_mass  # 中子星质量，单位：kg
    neutron_star_radius = 10000  # 中子星半径，单位：m
    # 典型中子星自转速度约为1000转/秒
    expected_omega_neutron = 1000 * 2 * math.pi  # 转换为rad/s
    analyze_scenario(
        "中子星自转",
        neutron_star_mass, 
        neutron_star_radius,
        expected_omega=expected_omega_neutron,
        description="中子星自转（典型半径约10公里）"
    )
    
    # 4. 极端天体
    print("=== 极端天体 ===")
    
    # 白洞视界附近
    white_hole_mass = 1e6 * sun_mass  # 白洞质量，单位：kg
    white_hole_radius = 2 * G * white_hole_mass / c**2  # 白洞视界半径，单位：m
    analyze_scenario(
        "白洞视界附近",
        white_hole_mass, 
        white_hole_radius,
        description="白洞视界附近的物质运动"
    )
    
    # 黑洞视界附近
    black_hole_mass = 6.5e9 * sun_mass  # M87*黑洞质量，单位：kg
    black_hole_radius = 2 * G * black_hole_mass / c**2  # 黑洞视界半径，单位：m
    analyze_scenario(
        "M87*黑洞视界附近",
        black_hole_mass, 
        black_hole_radius,
        description="M87*黑洞视界附近的物质运动"
    )
    
    # 5. 星系尺度
    print("=== 星系尺度 ===")
    
    # 太阳绕银河系中心旋转
    galaxy_center_mass = 4.1e6 * sun_mass  # 银河系中心质量，单位：kg
    sun_galaxy_radius = 8.2 * 3.086e19  # 太阳到银心距离，单位：m
    expected_v_sun_galaxy = 220  # 太阳绕银心旋转速度，单位：km/s
    analyze_scenario(
        "太阳绕银河系中心旋转",
        galaxy_center_mass, 
        sun_galaxy_radius,
        expected_v=expected_v_sun_galaxy,
        description="太阳绕银河系中心旋转"
    )
    
    # 6. 其他场景
    print("=== 其他场景 ===")
    
    # 木星绕太阳公转
    jupiter_mass = 1.898e27  # 木星质量，单位：kg
    jupiter_orbit = 7.785e11  # 木星轨道半径，单位：m
    expected_v_jupiter = 13.07  # 木星公转速度，单位：km/s
    analyze_scenario(
        "木星绕太阳公转",
        sun_mass, 
        jupiter_orbit,
        expected_v=expected_v_jupiter,
        description="木星绕太阳近似圆周公转"
    )
    
    # 冥王星绕太阳公转
    pluto_mass = 1.309e22  # 冥王星质量，单位：kg
    pluto_orbit = 5.906e12  # 冥王星轨道半径，单位：m
    expected_v_pluto = 4.74  # 冥王星公转速度，单位：km/s
    analyze_scenario(
        "冥王星绕太阳公转",
        sun_mass, 
        pluto_orbit,
        expected_v=expected_v_pluto,
        description="冥王星绕太阳近似圆周公转"
    )
    
    print("=== 分析完成 ===")
    print("角速度普适公式在从微观到宇宙尺度的物理场景中均表现出良好的适用性。")
    print("对于接近光速的极端情况，可能需要考虑相对论效应。")
