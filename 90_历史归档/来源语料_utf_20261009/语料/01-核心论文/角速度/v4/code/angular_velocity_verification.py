#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角速度终极求导与全尺度验证总报告 - 计算验证
基于张祥前统一场论（ZUFT）的角速度公式验证
"""

import math

# 常量定义
c = 299792458  # 光速，m/s
G = 6.67430e-11  # 万有引力常数，N·m²/kg²

# 测试质量
sun_mass = 1.9885e30  # 太阳质量，kg
earth_mass = 5.972e24  # 地球质量，kg
galaxy_mass = 1.90e41  # 银河系总质量，kg
m87_mass = 6.5e9 * sun_mass  # M87*黑洞质量，kg

# 测试距离
earth_sun_distance = 1.4960e11  # 日地平均距离，m
earth_radius = 6.371e6  # 地球半径，m
galaxy_orbital_radius = 8.5 * 3.086e19  # 太阳距银心距离，m

# 氢原子参数
bohr_radius = 5.29177210903e-11  # 玻尔半径，m
fine_structure_constant = 7.297e-3  # 精细结构常数


def calculate_angular_velocity_formula2(M, R):
    """
    使用公式(2)计算角速度：ω = √(GM/R³)
    """
    return math.sqrt(G * M / (R ** 3))


def calculate_angular_velocity_formula1(M, R, r):
    """
    使用公式(1)计算角速度：ω = c/r * √(r_g/R)
    其中 r_g = 2GM/c²
    """
    r_g = (2 * G * M) / (c ** 2)
    return (c / r) * math.sqrt(r_g / R)


def calculate_earth_rotation_angular_velocity():
    """
    计算地球自转角速度
    """
    # 使用论文中给出的r_g值：8.87e-3 m
    r_g = 8.87e-3
    print(f"r_g: {r_g}")
    print(f"earth_radius: {earth_radius}")
    ratio = r_g / (earth_radius ** 3)
    print(f"ratio: {ratio}")
    sqrt_ratio = math.sqrt(ratio)
    print(f"sqrt_ratio: {sqrt_ratio}")
    result = c * sqrt_ratio
    print(f"result: {result}")
    return result


def calculate_hydrogen_angular_velocity():
    """
    计算氢原子基态电子轨道角速度
    """
    v = fine_structure_constant * c
    return v / bohr_radius


def calculate_galaxy_orbital_velocity(M, R):
    """
    计算星系轨道速度：v = √(GM/R)
    """
    return math.sqrt(G * M / R)


def calculate_black_hole_angular_velocity(M):
    """
    计算黑洞视界附近的特征角速度
    """
    r_g = (2 * G * M) / (c ** 2)
    return c / r_g


def main():
    print("=== 角速度终极求导与全尺度验证总报告 - 计算验证 ===")
    print(f"真空光速 c = {c:.2f} m/s")
    print(f"万有引力常数 G = {G:.6e} N·m²/kg²")
    print()
    
    # 1. 地球绕太阳公转的角速度验证
    print("1. 地球绕太阳公转的角速度验证")
    print("==================================================")
    print(f"太阳质量: {sun_mass:.4e} kg")
    print(f"日地平均距离: {earth_sun_distance:.4e} m")
    
    omega_earth_sun = calculate_angular_velocity_formula2(sun_mass, earth_sun_distance)
    print(f"\n理论角速度: {omega_earth_sun:.6e} rad/s")
    
    # 计算周期
    period = 2 * math.pi / omega_earth_sun
    period_days = period / (24 * 3600)
    print(f"理论周期: {period:.2e} s = {period_days:.4f} 天")
    
    # 观测值
    observed_period_days = 365.2422
    print(f"观测周期: {observed_period_days} 天")
    
    # 误差计算
    error = abs((period_days - observed_period_days) / observed_period_days)
    print(f"相对误差: {error:.6e}")
    print()
    
    # 2. 地球自转的角速度验证
    print("2. 地球自转的角速度验证")
    print("==================================================")
    print(f"地球质量: {earth_mass:.4e} kg")
    print(f"地球半径: {earth_radius:.4e} m")
    
    omega_earth_rotation = calculate_earth_rotation_angular_velocity()
    print(f"\n理论角速度: {omega_earth_rotation:.6e} rad/s")
    
    # 观测值
    observed_omega = 7.2921159e-5
    print(f"观测角速度: {observed_omega:.6e} rad/s")
    
    # 误差计算
    error = abs((omega_earth_rotation - observed_omega) / observed_omega)
    print(f"相对误差: {error:.6e}")
    print()
    
    # 3. 氢原子的角速度验证
    print("3. 氢原子的角速度验证")
    print("==================================================")
    print(f"玻尔半径: {bohr_radius:.4e} m")
    print(f"精细结构常数: {fine_structure_constant:.6f}")
    
    omega_hydrogen = calculate_hydrogen_angular_velocity()
    print(f"\n理论角速度: {omega_hydrogen:.6e} rad/s")
    print()
    
    # 4. 太阳绕银河系中心旋转的速度验证
    print("4. 太阳绕银河系中心旋转的速度验证")
    print("==================================================")
    print(f"银河系总质量: {galaxy_mass:.4e} kg")
    print(f"太阳距银心距离: {galaxy_orbital_radius:.4e} m")
    
    velocity_galaxy = calculate_galaxy_orbital_velocity(galaxy_mass, galaxy_orbital_radius)
    print(f"\n理论轨道速度: {velocity_galaxy:.2f} m/s")
    
    # 观测值
    observed_velocity = 2.2e5
    print(f"观测轨道速度: {observed_velocity:.2f} m/s")
    
    # 误差计算
    error = abs((velocity_galaxy - observed_velocity) / observed_velocity)
    print(f"相对误差: {error:.6e}")
    print()
    
    # 5. M87*黑洞视界附近的角速度验证
    print("5. M87*黑洞视界附近的角速度验证")
    print("==================================================")
    print(f"M87*黑洞质量: {m87_mass:.4e} kg")
    
    omega_black_hole = calculate_black_hole_angular_velocity(m87_mass)
    print(f"\n特征角速度: {omega_black_hole:.6e} rad/s")
    
    # 计算特征周期
    period = 2 * math.pi / omega_black_hole
    period_days = period / (24 * 3600)
    print(f"特征周期: {period:.2e} s = {period_days:.2f} 天")
    print()
    
    print("=== 验证完成 ===")


if __name__ == "__main__":
    main()
