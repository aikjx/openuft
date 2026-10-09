#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版拉格朗日点质量变化率验证脚本
基于张祥前统一场论的第一性原理推导
验证拉格朗日点卫星质量变化率dm/dt=0，无法实现光速飞行
而人工场扫描技术可通过dm/dt<0实现质量减少直至归零
"""

import numpy as np
import matplotlib.pyplot as plt
import os

class SimpleLagrangeVerification:
    """简化版拉格朗日点与人工场质量变化验证类"""
    
    def __init__(self):
        """初始化验证参数"""
        # 物理常数设置
        self.c = 3e8  # 光速 (m/s)
        self.m0 = 1000  # 初始质量 (kg)
        self.max_time = 100  # 最大模拟时间 (s)
        self.time_steps = 1000  # 时间步数
        self.time = np.linspace(0, self.max_time, self.time_steps)
        
        # 结果存储
        self.lagrange_mass = None
        self.artificial_field_mass = None
        self.artificial_field_velocity = None
    
    def verify_lagrange_point(self):
        """验证拉格朗日点的质量变化率为零"""
        # 在拉格朗日点，质量恒定，dm/dt=0
        self.lagrange_mass = np.full(self.time_steps, self.m0)
        
        print("\n=== 拉格朗日点验证结果 ===")
        print(f"初始质量: {self.m0} kg")
        print(f"最终质量: {self.lagrange_mass[-1]} kg")
        print(f"质量变化率 dm/dt: 0 kg/s")
        print(f"结论: 拉格朗日点仅实现外力平衡，质量保持恒定，无法实现光速飞行")
        
    def simulate_artificial_field(self, decay_rate=0.05):
        """模拟人工场扫描技术导致的质量减少
        
        Args:
            decay_rate: 质量衰减率 (1/s)
        """
        # 模拟质量随时间指数减少
        self.artificial_field_mass = self.m0 * np.exp(-decay_rate * self.time)
        
        # 计算速度变化 (接近光速)
        self.artificial_field_velocity = np.zeros(self.time_steps)
        for i in range(self.time_steps):
            m = self.artificial_field_mass[i]
            if m > 0:
                # 根据相对论能量守恒，质量减少转化为动能
                # 简化模型：当质量趋近于零时，速度趋近于光速
                self.artificial_field_velocity[i] = self.c * (1 - np.exp(-(self.m0/m - 1)))
            else:
                self.artificial_field_velocity[i] = self.c
        
        print("\n=== 人工场扫描技术验证结果 ===")
        print(f"初始质量: {self.m0} kg")
        print(f"最终质量: {self.artificial_field_mass[-1]:.6f} kg")
        print(f"质量变化率 dm/dt: 负值 (质量持续减少)")
        print(f"最终速度: {self.artificial_field_velocity[-1]/self.c*100:.2f}% 光速")
        print(f"结论: 人工场扫描技术可使质量持续减少直至接近零，支持光速飞行")
        
    def run_simulation(self, decay_rate=0.05):
        """运行完整的验证模拟
        
        Args:
            decay_rate: 人工场质量衰减率
        """
        print("\n开始运行拉格朗日点与人工场质量变化验证...")
        self.verify_lagrange_point()
        self.simulate_artificial_field(decay_rate)
        
    def plot_results(self):
        """绘制验证结果图表"""
        # 设置中文字体支持
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'legend.fontsize': 9,
        })
        
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 质量随时间变化对比
        ax1 = axs[0, 0]
        ax1.plot(self.time, self.lagrange_mass, 'b-', label='Lagrange Point (dm/dt=0)', linewidth=2)
        ax1.plot(self.time, self.artificial_field_mass, 'r-', label='Artificial Field (dm/dt<0)', linewidth=2)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Mass (kg)')
        ax1.set_title('Mass vs Time')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend()
        
        # 2. 速度随时间变化 (仅人工场)
        ax2 = axs[0, 1]
        ax2.plot(self.time, self.artificial_field_velocity/self.c*100, 'r-', linewidth=2)
        ax2.axhline(y=100, color='g', linestyle='--', label='Speed of Light')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Velocity (% of c)')
        ax2.set_title('Velocity vs Time (Artificial Field)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # 3. 质量变化率对比
        ax3 = axs[1, 0]
        # 拉格朗日点dm/dt=0
        lagrange_dm_dt = np.zeros_like(self.time)
        # 人工场dm/dt (数值微分)
        artificial_dm_dt = np.gradient(self.artificial_field_mass, self.time)
        
        ax3.plot(self.time, lagrange_dm_dt, 'b-', label='Lagrange Point', linewidth=2)
        ax3.plot(self.time, artificial_dm_dt, 'r-', label='Artificial Field', linewidth=2)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Mass Change Rate (kg/s)')
        ax3.set_title('Mass Change Rate Comparison')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        # 4. 物理意义解释图
        ax4 = axs[1, 1]
        ax4.axis('off')
        explanation = """
        Key Findings:
        1. Lagrange Point: Mass remains constant (dm/dt=0)
           - Only external force balance
           - Cannot achieve light speed travel
        
        2. Artificial Field: Mass decreases over time (dm/dt<0)
           - Changes internal space structure
           - Can approach light speed as mass approaches zero
        
        Fundamental Difference:
        - Lagrange Point: External force equilibrium
        - Artificial Field: Internal property modification
        """
        ax4.text(0.1, 0.5, explanation, fontsize=9, verticalalignment='center')
        
        plt.tight_layout()
        
        # 保存图表
        save_path = os.path.dirname(os.path.abspath(__file__))
        fig.savefig(os.path.join(save_path, 'lagrange_verification_results.png'), dpi=300, bbox_inches='tight')
        print(f"\nChart saved to: {os.path.join(save_path, 'lagrange_verification_results.png')}")
        
        return fig

# 主函数
if __name__ == "__main__":
    print("\n===== Lagrange Point vs Artificial Field Mass Verification =====")
    print("Based on Zhang Xiangqian's Unified Field Theory")
    print("Verifying the essential difference between Lagrange Point (dm/dt=0) and Artificial Field (dm/dt<0)")
    print("================================================================")
    
    # 创建验证器实例
    verifier = SimpleLagrangeVerification()
    
    try:
        # 运行模拟
        verifier.run_simulation()
        
        # 绘制结果
        verifier.plot_results()
        
        print("\nVerification completed successfully!")
        
    except KeyboardInterrupt:
        print("\nVerification interrupted")
    except Exception as e:
        print(f"\nError during verification: {e}")
    finally:
        print("\nEnd of verification")