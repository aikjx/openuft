#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间理论计算验证脚本
用于验证《时间的本质：从物理学基础到统一场论的深度解析》附录C中的计算结果
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 物理常数
C = 299792458  # 光速，单位：m/s
G = 6.67430e-11  # 万有引力常数，单位：m^3/(kg·s^2)
M_SUN = 1.989e30  # 太阳质量，单位：kg
M_PROTON = 1.67262e-27  # 质子质量，单位：kg


def verify_gps_time_effect():
    """
    验证GPS卫星时间效应
    """
    print("=== GPS卫星时间效应验证 ===")
    
    # 参数设置
    h = 20180e3  # GPS卫星轨道高度，单位：m
    R = 6371e3  # 地球半径，单位：m
    r = R + h  # 到地心距离，单位：m
    v = 3870  # 卫星运行速度，单位：m/s
    M = 5.972e24  # 地球质量，单位：kg
    delta_t0 = 86400  # 一天时间，单位：s
    
    # 计算狭义相对论效应
    delta_t_sr = - (v**2) / (2 * C**2) * delta_t0
    print(f"狭义相对论效应（每天）: {delta_t_sr * 1e6:.2f} μs")
    
    # 计算广义相对论效应
    delta_t_gr = (G * M) / (r * C**2) * delta_t0
    print(f"广义相对论效应（每天）: {delta_t_gr * 1e6:.2f} μs")
    
    # 计算总时间差
    delta_t_total = delta_t_sr + delta_t_gr
    print(f"总时间差（每天）: {delta_t_total * 1e6:.2f} μs")
    
    # 与实际观测结果比较
    observed = 38e-6  # 实际观测结果，单位：s
    error = abs(delta_t_total - observed) / observed * 100
    print(f"与实际观测结果的相对误差: {error:.2f}%")
    
    return delta_t_total, delta_t_sr, delta_t_gr


def verify_blackhole_time_dilation():
    """
    验证黑洞附近时间膨胀效应
    """
    print("\n=== 黑洞附近时间膨胀效应验证 ===")
    
    # 参数设置
    M = 1e6 * M_SUN  # 黑洞质量，单位：kg
    r_s = 2 * G * M / C**2  # 史瓦西半径，单位：m
    print(f"黑洞质量: {M:.2e} kg")
    print(f"史瓦西半径: {r_s:.2e} m")
    
    # 计算不同距离处的时间膨胀因子
    r_ratio_list = [1.0, 1.5, 2.0, 5.0, 10.0, 100.0, 1000.0]
    print("\n不同距离处的时间膨胀因子：")
    print("距离(r/rs) | 时间膨胀因子(T/T0) | 物理意义")
    print("-" * 60)
    
    results = []
    for r_ratio in r_ratio_list:
        r = r_ratio * r_s
        # 计算时间膨胀因子
        time_dilation = math.exp(-G * M / (r * C**2))
        # 确定物理意义描述
        if r_ratio == 1.0:
            meaning = "事件视界处时间静止"
        else:
            meaning = f"时间流逝速度为远处的{time_dilation*100:.2f}%"
        
        print(f"{r_ratio:<12.1f} | {time_dilation:<22.4f} | {meaning}")
        results.append((r_ratio, time_dilation))
    
    return results


def verify_spiral_motion():
    """
    验证空间螺旋运动与时间的关系
    """
    print("\n=== 空间螺旋运动与时间的关系验证 ===")
    
    # 参数设置
    r0 = 1.0  # 初始空间半径，单位：m
    omega = 1.0e-18  # 空间扩张率，单位：s^-1
    Omega = 2.0e-18  # 空间旋转率，单位：s^-1
    
    # 计算不同时间点的结果
    years_list = [0, 1e6, 1e9, 1e10, 1e12]
    print("\n时间随空间螺旋运动的变化：")
    print("时间（年） | 空间半径（m） | 垂直速度分量（m/s） | 时间膨胀因子")
    print("-" * 70)
    
    results = []
    for years in years_list:
        t = years * 365.25 * 24 * 3600  # 转换为秒
        # 计算空间半径
        r = r0 * math.exp(omega * t)
        # 计算垂直速度分量
        v_perp = r0 * math.sqrt(omega**2 + Omega**2) * math.exp(omega * t)
        # 计算时间膨胀因子
        if v_perp >= C:
            time_dilation = 0  # 理论上不应该超过光速，这里做保护
        else:
            time_dilation = math.sqrt(1 - (v_perp**2) / (C**2))
        
        print(f"{years:<11.0g} | {r:<15.6g} | {v_perp:<24.2e} | {time_dilation:<12.3f}")
        results.append((years, r, v_perp, time_dilation))
    
    return results


def verify_mass_time_relation():
    """
    验证质量与时间场的关系
    """
    print("\n=== 质量与时间场的关系验证 ===")
    
    # 参数设置
    T0 = 1 / C  # 时间场强度参考值
    r0 = 1.0e-15  # 特征长度，单位：m
    R = 1.0e-14  # 积分半径，单位：m
    
    print(f"参数设置：")
    print(f"T0 = {T0:.2e} s/m")
    print(f"r0 = {r0:.2e} m")
    print(f"R = {R:.2e} m")
    
    # 定义积分函数
    def integrand(r):
        return math.exp(-r/r0) * (1 - r/r0)
    
    # 数值积分
    integral_result, error = integrate.quad(integrand, 0, R)
    print(f"\n积分结果: {integral_result:.6e}")
    print(f"理论积分结果: {r0 * (1 - math.exp(-R/r0) * (1 + R/r0)):.6e}")
    
    # 计算质量
    M = 4 * math.pi * (C**3 / G) * T0 * r0 * integral_result
    print(f"\n计算得到的质量: {M:.6e} kg")
    print(f"质子质量: {M_PROTON:.6e} kg")
    
    # 计算相对误差
    rel_error = abs(M - M_PROTON) / M_PROTON * 100
    print(f"相对误差: {rel_error:.4f}%")
    
    return M, rel_error


def plot_results(gps_results, bh_results, spiral_results, mass_result):
    """
    绘制计算结果图表
    """
    # 创建图表目录
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. GPS时间效应图表
    plt.figure(figsize=(10, 6))
    effects = ['狭义相对论效应', '广义相对论效应', '总时间差']
    values = [gps_results[1] * 1e6, gps_results[2] * 1e6, gps_results[0] * 1e6]
    colors = ['red', 'green', 'blue']
    
    bars = plt.bar(effects, values, color=colors)
    plt.title('GPS卫星时间效应（单位：μs/天）')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        if height < 0:
            ypos = -5
        else:
            ypos = 5
        plt.text(bar.get_x() + bar.get_width()/2., height + ypos/100*max(values),
                f'{height:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('GPS时间效应验证图.png', dpi=300)
    print("\nGPS时间效应验证图已保存")
    
    # 2. 黑洞时间膨胀图表
    plt.figure(figsize=(10, 6))
    r_ratios = [item[0] for item in bh_results]
    time_factors = [item[1] for item in bh_results]
    
    plt.semilogx(r_ratios, time_factors, 'o-', linewidth=2, markersize=8)
    plt.title('黑洞附近时间膨胀因子')
    plt.xlabel('距离（r/rs）')
    plt.ylabel('时间膨胀因子（T/T0）')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # 添加数据点标签
    for i, (r_ratio, factor) in enumerate(zip(r_ratios, time_factors)):
        if i % 2 == 0 or factor == 0:  # 避免标签过于密集
            plt.annotate(f'{factor:.4f}', (r_ratio, factor), 
                        xytext=(5, 5), textcoords='offset points')
    
    plt.tight_layout()
    plt.savefig('黑洞时间膨胀验证图.png', dpi=300)
    print("黑洞时间膨胀验证图已保存")
    
    # 3. 空间螺旋运动图表
    plt.figure(figsize=(12, 6))
    years = [item[0] for item in spiral_results]
    r_values = [item[1] for item in spiral_results]
    v_values = [item[2] for item in spiral_results]
    time_factors = [item[3] for item in spiral_results]
    
    # 创建两个子图
    ax1 = plt.subplot(121)
    ax1.semilogx(years, r_values, 'o-', color='blue', linewidth=2)
    ax1.set_title('空间半径随时间的变化')
    ax1.set_xlabel('时间（年）')
    ax1.set_ylabel('空间半径（m）')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2 = plt.subplot(122)
    ax2.semilogx(years, time_factors, 'o-', color='red', linewidth=2)
    ax2.set_title('时间膨胀因子随时间的变化')
    ax2.set_xlabel('时间（年）')
    ax2.set_ylabel('时间膨胀因子')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_ylim(0.8, 1.05)
    
    plt.tight_layout()
    plt.savefig('空间螺旋运动时间效应验证图.png', dpi=300)
    print("空间螺旋运动时间效应验证图已保存")
    
    # 4. 质量验证结果图表
    plt.figure(figsize=(8, 6))
    masses = ['计算质量', '质子质量']
    values = [mass_result[0], M_PROTON]
    
    bars = plt.bar(masses, values, color=['blue', 'green'])
    plt.title('质量验证结果（单位：kg）')
    plt.yscale('log')
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{height:.2e}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('质量时间场关系验证图.png', dpi=300)
    print("质量时间场关系验证图已保存")


def main():
    """
    主函数
    """
    print("时间理论计算验证脚本")
    print("====================")
    
    # 运行各项验证
    gps_results = verify_gps_time_effect()
    bh_results = verify_blackhole_time_dilation()
    spiral_results = verify_spiral_motion()
    mass_result = verify_mass_time_relation()
    
    # 绘制结果图表
    try:
        plot_results(gps_results, bh_results, spiral_results, mass_result)
        print("\n所有图表已成功生成！")
    except Exception as e:
        print(f"\n生成图表时出错: {e}")
    
    print("\n验证完成！")


if __name__ == "__main__":
    main()
