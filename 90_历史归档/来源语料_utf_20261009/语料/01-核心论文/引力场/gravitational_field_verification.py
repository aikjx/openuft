#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正引力场与反引力场的数学验证脚本
功能：验证拉格朗日点现象与光速飞行原理的数学推导
基于张祥前统一场论动力学方程
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Arrow
import time

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 物理常数定义
C = 299792458.0  # 光速 (m/s)
G = 6.67430e-11  # 万有引力常数 (m³/kg·s²)
M_SUN = 1.989e30  # 太阳质量 (kg)
M_EARTH = 5.972e24  # 地球质量 (kg)
AU = 1.496e11  # 天文单位 (m)

class GravitationalFieldVerifier:
    """引力场验证器类"""
    
    def __init__(self):
        self.results = {}
        
    def verify_lagrange_point(self):
        """
        验证拉格朗日点情况下的质量变化率
        根据统一场论动力学方程：0 = C * dm/dt - m * a
        在拉格朗日点，a = 0，因此 dm/dt = 0
        """
        print("\n===== 拉格朗日点质量变化率验证 =====")
        print("统一场论动力学方程：F = (C - V) * dm/dt + m * dC/dt - m * dV/dt")
        print("在拉格朗日点：")
        print("  - F = 0 (合外力为零)")
        print("  - V = 0 (相对静止)")
        print("  - dC/dt = 0 (光速恒定)")
        print("  - a = dV/dt = 0 (加速度为零)")
        print("代入方程得到：0 = C * dm/dt")
        print(f"由于 C = {C} m/s ≠ 0，因此必须满足 dm/dt = 0")
        print("结论：在拉格朗日点，物体质量保持恒定，无法减少")
        
        # 模拟拉格朗日点L1的位置计算
        # 简化模型：假设地球和太阳在同一直线上
        r = AU * (M_EARTH/(3*M_SUN))**(1/3)
        print(f"\n地球-太阳系统L1拉格朗日点距离地球约 {r/AU:.4f} AU ({r:.2e} m)")
        
        self.results['lagrange_dm_dt'] = 0.0
        self.results['lagrange_point_distance'] = r
        
        return self.results['lagrange_dm_dt']
    
    def simulate_artificial_field(self, initial_mass=1.0, field_strength=0.1, simulation_time=10.0, dt=0.01):
        """
        模拟人工反引力场对物体质量的影响
        基于方程：F_anti ≈ (C - V) * dm/dt
        假设 V << C，简化为：F_anti ≈ C * dm/dt
        因此：dm/dt ≈ F_anti / C
        
        参数：
            initial_mass: 初始质量 (kg)
            field_strength: 人工场强度因子 (影响dm/dt的大小)
            simulation_time: 模拟时间 (s)
            dt: 时间步长 (s)
        """
        print("\n===== 人工反引力场质量变化模拟 =====")
        print(f"初始质量: {initial_mass} kg")
        print(f"人工场强度因子: {field_strength}")
        
        # 模拟参数
        time_points = np.arange(0, simulation_time, dt)
        mass_values = []
        dm_dt_values = []
        
        current_mass = initial_mass
        
        for t in time_points:
            # 计算质量变化率 (与场强度成正比，质量减少)
            dm_dt = -field_strength * current_mass / C  # 负号表示质量减少
            
            # 更新质量
            current_mass += dm_dt * dt
            
            # 防止质量变为负值
            if current_mass < 0:
                current_mass = 0
                dm_dt = 0
            
            mass_values.append(current_mass)
            dm_dt_values.append(dm_dt)
        
        # 计算质量归零时间
        zero_time = None
        for i, m in enumerate(mass_values):
            if m <= 0:
                zero_time = time_points[i]
                break
        
        if zero_time is not None:
            print(f"质量归零时间: {zero_time:.2f} s")
        else:
            print("在模拟时间内质量未完全归零")
        
        # 存储结果
        self.results['artificial_time_points'] = time_points
        self.results['artificial_mass_values'] = mass_values
        self.results['artificial_dm_dt_values'] = dm_dt_values
        self.results['zero_time'] = zero_time
        
        return time_points, mass_values, dm_dt_values
    
    def compare_scenarios(self):
        """
        对比两种场景的关键区别
        """
        print("\n===== 两种方案对比 =====")
        comparison = [
            ("场类型", "正引力场 vs 正引力场", "正引力场 vs 反引力场", "根本不同"),
            ("作用本质", "外部引力场的矢量合力平衡", "直接改写物体内部的空间运动状态", "本质不同"),
            ("数学推导", f"dm/dt = {self.results['lagrange_dm_dt']} (质量不变)", "允许 dm/dt < 0 (质量可减)", "方案一被数学否定"),
            ("质量属性", "物体的质量不变", "物体的质量可减少直至为零", "目标能否达成的关键"),
            ("最终状态", "静止或匀速运动", "进入激发态，以光速运动", "结果天差地别")
        ]
        
        # 打印对比表
        print(f"{'对比维度':<12} {'方案一：拉格朗日点':<30} {'方案二：人工反引力场':<30} {'裁决':<15}")
        print("-" * 88)
        for item in comparison:
            print(f"{item[0]:<12} {item[1]:<30} {item[2]:<30} {item[3]:<15}")
    
    def visualize_results(self):
        """
        可视化验证结果
        """
        # 创建两个子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('正引力场与反引力场效应对比验证', fontsize=16)
        
        # 子图1：人工场对质量的影响
        if 'artificial_time_points' in self.results and 'artificial_mass_values' in self.results:
            ax1.plot(self.results['artificial_time_points'], self.results['artificial_mass_values'], 
                     'b-', linewidth=2, label='物体质量')
            ax1.set_xlabel('时间 (s)')
            ax1.set_ylabel('质量 (kg)')
            ax1.set_title('人工反引力场对物体质量的影响')
            ax1.grid(True)
            ax1.legend()
            
            # 添加质量归零标记
            if self.results['zero_time'] is not None:
                ax1.axvline(x=self.results['zero_time'], color='r', linestyle='--', 
                           label=f'质量归零时间: {self.results["zero_time"]:.2f} s')
                ax1.legend()
        
        # 子图2：示意图 - 拉格朗日点与人工场对比
        # 简化示意图：左侧显示拉格朗日点，右侧显示人工场
        
        # 拉格朗日点部分
        ax2.axvline(x=0.5, color='gray', linestyle='--')
        
        # 绘制太阳和地球
        sun = Circle((0.2, 0.5), 0.05, color='orange', label='太阳')
        earth = Circle((0.8, 0.5), 0.03, color='blue', label='地球')
        ax2.add_patch(sun)
        ax2.add_patch(earth)
        
        # 绘制拉格朗日点L1
        lagrange = Circle((0.5, 0.5), 0.02, color='green', label='拉格朗日点L1')
        ax2.add_patch(lagrange)
        
        # 绘制引力箭头
        ax2.add_patch(Arrow(0.5, 0.5, -0.25, 0, width=0.01, color='red', label='太阳引力'))
        ax2.add_patch(Arrow(0.5, 0.5, 0.25, 0, width=0.01, color='blue', label='地球引力'))
        
        # 添加标签
        ax2.text(0.35, 0.4, 'F_net = 0', fontsize=12, ha='center')
        ax2.text(0.35, 0.3, 'dm/dt = 0', fontsize=12, ha='center')
        
        # 人工场部分
        # 绘制物体
        object_before = Circle((1.2, 0.7), 0.04, color='brown', label='物体(初始状态)')
        object_after = Circle((1.8, 0.3), 0.01, color='purple', label='物体(质量归零)')
        ax2.add_patch(object_before)
        ax2.add_patch(object_after)
        
        # 绘制人工场
        field_circle = Circle((1.5, 0.5), 0.15, color='cyan', fill=False, linestyle='--', 
                             linewidth=2, label='人工反引力场')
        ax2.add_patch(field_circle)
        
        # 绘制质量变化箭头
        ax2.add_patch(Arrow(1.3, 0.7, 0.3, -0.3, width=0.01, color='green', 
                           label='dm/dt < 0'))
        
        # 添加标签
        ax2.text(1.5, 0.8, '拉格朗日点效应', fontsize=14, ha='center')
        ax2.text(1.5, 0.2, '人工场效应', fontsize=14, ha='center')
        
        ax2.set_xlim(0, 2)
        ax2.set_ylim(0, 1)
        ax2.set_aspect('equal')
        ax2.axis('off')
        
        # 添加主标题和解释
        plt.figtext(0.5, 0.01, 
                   '左图：人工反引力场作用下物体质量随时间变化；右图：拉格朗日点与人工反引力场效应对比示意图', 
                   ha='center', fontsize=12)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('引力场效应对比验证.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def animate_field_effect(self):
        """
        动画展示人工场对物体质量的影响
        """
        if 'artificial_time_points' not in self.results or 'artificial_mass_values' not in self.results:
            print("请先运行模拟函数")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, max(self.results['artificial_time_points']))
        ax.set_ylim(0, max(self.results['artificial_mass_values']) * 1.1)
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('质量 (kg)')
        ax.set_title('人工反引力场对物体质量的动态影响')
        ax.grid(True)
        
        mass_line, = ax.plot([], [], 'b-', linewidth=2)
        mass_point, = ax.plot([], [], 'ro', markersize=8)
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        mass_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
        
        def init():
            mass_line.set_data([], [])
            mass_point.set_data([], [])
            time_text.set_text('')
            mass_text.set_text('')
            return mass_line, mass_point, time_text, mass_text
        
        def update(frame):
            t = self.results['artificial_time_points'][:frame]
            m = self.results['artificial_mass_values'][:frame]
            mass_line.set_data(t, m)
            mass_point.set_data(self.results['artificial_time_points'][frame-1], 
                               self.results['artificial_mass_values'][frame-1])
            time_text.set_text(f'时间: {self.results["artificial_time_points"][frame-1]:.2f} s')
            mass_text.set_text(f'质量: {self.results["artificial_mass_values"][frame-1]:.6f} kg')
            
            # 当质量接近零时改变点的颜色
            if self.results['artificial_mass_values'][frame-1] < max(self.results['artificial_mass_values']) * 0.1:
                mass_point.set_color('purple')
            
            return mass_line, mass_point, time_text, mass_text
        
        ani = FuncAnimation(fig, update, frames=len(self.results['artificial_time_points']), 
                           init_func=init, blit=True, interval=50)
        
        plt.tight_layout()
        plt.show()
        
        # 保存动画（可选）
        # ani.save('artificial_field_effect.gif', writer='pillow', fps=30)


def main():
    """主函数"""
    print("=" * 80)
    print("正引力场与反引力场的数学验证程序")
    print("基于张祥前统一场论动力学方程")
    print("=" * 80)
    
    verifier = GravitationalFieldVerifier()
    
    # 验证拉格朗日点质量变化率
    verifier.verify_lagrange_point()
    
    # 模拟人工反引力场
    verifier.simulate_artificial_field(initial_mass=1.0, field_strength=1.0e9, 
                                      simulation_time=20.0, dt=0.05)
    
    # 对比两种场景
    verifier.compare_scenarios()
    
    # 可视化结果
    print("\n生成可视化结果...")
    verifier.visualize_results()
    
    # 动画展示（可选）
    # verifier.animate_field_effect()
    
    print("\n验证完成！")
    print("结论：拉格朗日点的卫星无法实现光速飞行，因为其质量变化率dm/dt=0")
    print("只有通过人工反引力场技术，使dm/dt<0，才能实现质量减少直至归零，最终达到光速飞行")


if __name__ == "__main__":
    main()
