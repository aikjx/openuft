#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
时间势差验证脚本
用于验证论文《宇宙航行：时间势差——将二十万年压缩为半个小时以内神奇科技》中的计算合理性
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 常量定义
SPEED_OF_LIGHT = 299792458  # 光速，单位：米/秒
LY_TO_METERS = 9.461e15  # 光年转换为米的系数
YEAR_TO_SECONDS = 365.25 * 24 * 3600  # 年转换为秒的系数
HOUR_TO_SECONDS = 3600  # 小时转换为秒的系数


def lorentz_factor(v):
    """
    计算洛伦兹因子
    v: 速度，单位：米/秒
    返回: 洛伦兹因子 gamma
    """
    if v >= SPEED_OF_LIGHT:
        raise ValueError("速度不能超过光速")
    return 1 / np.sqrt(1 - (v**2 / SPEED_OF_LIGHT**2))


def time_dilation(t_proper, gamma):
    """
    计算时间膨胀
    t_proper: 固有时间，单位：秒
    gamma: 洛伦兹因子
    返回: 膨胀后的时间，单位：秒
    """
    return t_proper * gamma


def calculate_required_velocity(distance, t_observer, t_proper):
    """
    根据距离、观察者时间和固有时计算所需的速度
    distance: 距离，单位：米
    t_observer: 观察者时间，单位：秒
    t_proper: 固有时间，单位：秒
    返回: 所需速度，单位：米/秒
    """
    # 根据洛伦兹变换，t_observer = gamma * t_proper
    gamma = t_observer / t_proper
    
    # 从gamma计算速度
    v = SPEED_OF_LIGHT * np.sqrt(1 - 1/gamma**2)
    
    # 验证该速度是否能在观察者时间内完成距离
    v_required_by_distance = distance / t_observer
    
    if v_required_by_distance > SPEED_OF_LIGHT:
        print(f"警告：根据距离和时间，需要的速度为{v_required_by_distance/SPEED_OF_LIGHT:.10f}c，超过光速")
    
    return v, v_required_by_distance


def analyze_time_dilation_ratio(K, t_ship_hours):
    """
    分析时间势差比
    K: 时间势差比 T宇宙/T飞船
    t_ship_hours: 飞船内时间，单位：小时
    返回: 地球时间，单位：小时
    """
    t_earth_hours = K * t_ship_hours
    print(f"时间势差比K = {K:.2f} 时：")
    print(f"  飞船内时间 = {t_ship_hours:.2f} 小时")
    print(f"  地球时间 = {t_earth_hours:.2f} 小时")
    return t_earth_hours


def verify_paper_claims():
    """
    验证论文中的声明
    """
    print("=== 论文声明验证 ===")
    print()
    
    # 论文核心参数
    distance_ly = 200000  # 往返距离，单位：光年
    t_earth_hours = 2.0   # 地球等待时间，单位：小时
    t_ship_hours = 0.5    # 飞船内时间，单位：小时
    
    # 转换单位
    distance_m = distance_ly * LY_TO_METERS
    t_earth_seconds = t_earth_hours * HOUR_TO_SECONDS
    t_ship_seconds = t_ship_hours * HOUR_TO_SECONDS
    
    print(f"论文参数:")
    print(f"  往返距离 = {distance_ly} 光年")
    print(f"  地球等待时间 = {t_earth_hours} 小时")
    print(f"  飞船内时间 = {t_ship_hours} 小时")
    print()
    
    # 计算时间势差比K
    K_paper = t_earth_seconds / t_ship_seconds
    print(f"计算时间势差比K:")
    print(f"  K = T宇宙/T飞船 = {t_earth_seconds}/{t_ship_seconds} = {K_paper:.2f} 倍")
    print()
    
    # 计算所需速度
    print("计算所需速度:")
    v_relativistic, v_required_by_distance = calculate_required_velocity(
        distance_m, t_earth_seconds, t_ship_seconds)
    
    print(f"  相对论计算所需速度 = {v_relativistic/SPEED_OF_LIGHT:.10f}c")
    print(f"  距离-时间计算所需速度 = {v_required_by_distance/SPEED_OF_LIGHT:.10f}c")
    print()
    
    # 分析传统方式下的时间
    print("传统方式（无时间膨胀）分析:")
    t_traditional_years = distance_ly / SPEED_OF_LIGHT  # 以光年为距离单位，光速为1c时的年数
    print(f"  以光速飞行所需时间 = {t_traditional_years:.2f} 年")
    print()
    
    # 计算不同速度下的时间膨胀
    print("不同速度下的时间膨胀效应:")
    velocities = [0.9, 0.95, 0.99, 0.999, 0.9999, 0.99999, 0.999999]
    for v_ratio in velocities:
        v = v_ratio * SPEED_OF_LIGHT
        gamma = lorentz_factor(v)
        t_ship = t_earth_seconds / gamma
        t_ship_h = t_ship / HOUR_TO_SECONDS
        
        # 计算在该速度下飞行所需的地球时间
        t_earth_required = distance_m / v
        t_earth_required_h = t_earth_required / HOUR_TO_SECONDS
        t_earth_required_y = t_earth_required / YEAR_TO_SECONDS
        
        print(f"  速度 = {v_ratio:.6f}c:")
        print(f"    洛伦兹因子 gamma = {gamma:.6f}")
        print(f"    若地球时间为{t_earth_hours}小时，飞船时间 = {t_ship_h:.6f}小时")
        print(f"    飞行所需地球时间 = {t_earth_required_h:.2f}小时 ({t_earth_required_y:.2f}年)")
    print()
    
    # 计算实现论文效果所需的gamma值
    print("实现论文效果分析:")
    gamma_required = t_earth_seconds / t_ship_seconds
    v_required = SPEED_OF_LIGHT * np.sqrt(1 - 1/gamma_required**2)
    print(f"  需要的洛伦兹因子 gamma = {gamma_required:.2f}")
    print(f"  对应的速度 = {v_required/SPEED_OF_LIGHT:.10f}c")
    
    # 验证速度是否能在2小时内完成20万光年
    distance_2h_light = SPEED_OF_LIGHT * t_earth_seconds
    distance_2h_light_ly = distance_2h_light / LY_TO_METERS
    print(f"  光在2小时内行进的距离 = {distance_2h_light_ly:.6f} 光年")
    print(f"  与目标距离的比值 = {distance_2h_light_ly/distance_ly:.12f}")
    
    # 计算需要的空间压缩比例
    space_compression_ratio = distance_ly / distance_2h_light_ly
    print(f"  需要的空间压缩比例 = {space_compression_ratio:.2f} 倍")
    print()
    
    # 结论
    print("=== 结论 ===")
    if v_required_by_distance > SPEED_OF_LIGHT:
        print("1. 根据传统相对论，仅靠速度无法实现论文中的时间效应，因为需要超光速")
    
    print(f"2. 论文中时间势差比K = {K_paper:.2f} 倍的计算在数学上是正确的")
    print(f"3. 要实现20万光年的旅程在2小时内完成，需要空间压缩 {space_compression_ratio:.2f} 倍")
    print("4. 论文提出的'时间泡'和'人工场扫描'技术若能实现空间压缩，从数学上可以解释其结论")


def generate_plots():
    """
    生成可视化图表
    """
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
        
        # 1. 速度与洛伦兹因子的关系图
        plt.figure(figsize=(10, 6))
        v_ratios = np.linspace(0, 0.99999, 1000)
        gammas = [lorentz_factor(v_ratio * SPEED_OF_LIGHT) for v_ratio in v_ratios]
        
        plt.plot(v_ratios, gammas)
        plt.title('速度与洛伦兹因子的关系')
        plt.xlabel('速度 (c)')
        plt.ylabel('洛伦兹因子 (γ)')
        plt.grid(True)
        plt.axvline(x=0.9, color='r', linestyle='--', alpha=0.5)
        plt.axvline(x=0.99, color='g', linestyle='--', alpha=0.5)
        plt.axvline(x=0.999, color='b', linestyle='--', alpha=0.5)
        plt.savefig('speed_gamma_relation.png', dpi=300, bbox_inches='tight')
        
        # 2. 时间膨胀因子与速度的关系
        plt.figure(figsize=(10, 6))
        t_proper = 1.0  # 1小时的固有时
        t_dilated = [t_proper * gamma for gamma in gammas]
        
        plt.plot(v_ratios, t_dilated)
        plt.title('速度与时间膨胀的关系 (固有时 = 1小时)')
        plt.xlabel('速度 (c)')
        plt.ylabel('膨胀后的时间 (小时)')
        plt.grid(True)
        plt.axhline(y=4, color='r', linestyle='--', alpha=0.5, label='K = 4')
        plt.legend()
        plt.savefig('time_dilation_relation.png', dpi=300, bbox_inches='tight')
        
        # 3. 距离-时间-速度关系
        plt.figure(figsize=(10, 6))
        distances_ly = np.array([1, 10, 100, 1000, 10000, 100000, 200000])
        
        # 计算不同距离下，以不同速度飞行所需的时间
        speeds = [0.9, 0.99, 0.999, 0.9999]
        colors = ['r', 'g', 'b', 'purple']
        
        for i, v_ratio in enumerate(speeds):
            v = v_ratio * SPEED_OF_LIGHT
            gamma = lorentz_factor(v)
            
            # 地球时间
            t_earth_years = distances_ly / v_ratio  # 光年/光速比 = 年数
            # 飞船时间
            t_ship_years = t_earth_years / gamma
            
            plt.plot(distances_ly, t_ship_years, marker='o', linestyle='-', color=colors[i], 
                     label=f'速度 = {v_ratio}c')
        
        # 添加论文中的目标点
        plt.plot(200000, 0.5/24/365, marker='*', markersize=15, color='gold', 
                 label='论文目标 (20万光年，0.5小时)')
        
        plt.title('不同速度下航行距离与飞船时间的关系')
        plt.xlabel('距离 (光年)')
        plt.ylabel('飞船时间 (年)')
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
        plt.legend()
        plt.savefig('distance_time_relation.png', dpi=300, bbox_inches='tight')
        
        print("图表已生成：")
        print("  - speed_gamma_relation.png: 速度与洛伦兹因子关系图")
        print("  - time_dilation_relation.png: 速度与时间膨胀关系图")
        print("  - distance_time_relation.png: 距离-时间-速度关系图")
        
    except Exception as e:
        print(f"生成图表时出错: {e}")
        print("跳过图表生成，继续计算")


if __name__ == "__main__":
    print("=" * 80)
    print("时间势差验证程序")
    print("验证论文《宇宙航行：时间势差——将二十万年压缩为半个小时以内神奇科技》")
    print("=" * 80)
    print()
    
    # 验证论文声明
    verify_paper_claims()
    
    # 生成可视化图表
    generate_plots()
    
    print()
    print("验证完成！")
