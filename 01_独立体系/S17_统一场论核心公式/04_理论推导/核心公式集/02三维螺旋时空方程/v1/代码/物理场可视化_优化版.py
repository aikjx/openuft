#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论：物理场可视化优化版
优雅展示电场、磁场、引力场的统一起源
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持
plt.rcParams.update({
    'font.family': ['SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
    'axes.unicode_minus': False
})

class PhysicsFieldVisualizer:
    """物理场可视化器"""
    
    def __init__(self, r=1.0, omega=1.0, p=1.0):
        self.r = r          # 螺旋半径
        self.omega = omega  # 角速度
        self.p = p          # 轴向速度
        
        # 设置优雅的科学配色方案
        self.setup_colors()
        
    def setup_colors(self):
        """设置科学可视化配色"""
        self.colors = {
            'electric': '#0066cc',     # 电场 - 深蓝
            'magnetic': '#cc0000',     # 磁场 - 深红
            'gravity': '#009900',      # 引力场 - 深绿
            'neutral': '#666666',      # 中性灰
            'background': '#f0f0f0',   # 背景灰
            'highlight': '#ff9900'      # 高亮橙
        }
        
    def create_field_interpretation(self):
        """创建物理场诠释图"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Unified Field Theory: Geometric Origin of Physical Fields', 
                   fontsize=16, fontweight='bold', y=0.98)
        
        # 子图1：场强分量
        theta = np.linspace(0, 2*np.pi, 200)
        
        # 电场（直线分量）
        E_magnitude = self.p
        axes[0,0].axhline(y=E_magnitude, color=self.colors['electric'], 
                          linewidth=3, label=f'E-field = {E_magnitude:.2f}')
        
        # 磁场（旋转分量）
        B_magnitude = self.r * self.omega
        axes[0,0].plot(theta, B_magnitude * np.cos(theta), 
                       color=self.colors['magnetic'], linewidth=3, label='B-field(θ)')
        
        axes[0,0].set_xlabel('Phase θ (rad)', fontweight='bold')
        axes[0,0].set_ylabel('Field Strength (normalized)', fontweight='bold')
        axes[0,0].set_title('Electromagnetic Field Components', fontweight='bold')
        axes[0,0].legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].set_xlim(0, 2*np.pi)
        axes[0,0].set_ylim(-B_magnitude*1.2, B_magnitude*1.2)
        
        # 子图2：引力场分布
        r_range = np.linspace(0.5, 3.0, 150)
        g_field = self.r * self.omega**2 * (self.r / r_range)**2
        
        axes[0,1].plot(r_range, g_field, color=self.colors['gravity'], 
                       linewidth=3, marker='o', markersize=4, alpha=0.8)
        axes[0,1].scatter([self.r], [self.r * self.omega**2], 
                         color=self.colors['highlight'], s=200, 
                         edgecolors='black', linewidth=2, label='Reference Point', zorder=5)
        
        axes[0,1].set_xlabel('Distance r (m)', fontweight='bold')
        axes[0,1].set_ylabel('Gravitational Field Strength', fontweight='bold')
        axes[0,1].set_title('Gravitational Field: 1/r² Distribution', fontweight='bold')
        axes[0,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].set_yscale('log')
        
        # 子图3：统一场相位关系
        phase = np.linspace(0, 2*np.pi, 200)
        
        # 归一化的场分量
        normalization = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        E_normalized = np.ones_like(phase) * self.p / normalization
        B_normalized = self.r * self.omega * np.cos(phase) / normalization
        g_normalized = -np.sin(phase)
        
        axes[1,0].plot(phase, E_normalized, color=self.colors['electric'], 
                       linewidth=2.5, label='E-field', marker='s', markersize=3)
        axes[1,0].plot(phase, B_normalized, color=self.colors['magnetic'], 
                       linewidth=2.5, label='B-field', marker='^', markersize=3)
        axes[1,0].plot(phase, g_normalized, color=self.colors['gravity'], 
                       linewidth=2.5, label='G-field', marker='o', markersize=3)
        
        axes[1,0].set_xlabel('Phase ωt (rad)', fontweight='bold')
        axes[1,0].set_ylabel('Normalized Field Strength', fontweight='bold')
        axes[1,0].set_title('Unified Field Phase Relationships', fontweight='bold')
        axes[1,0].legend(frameon=True, fancybox=True, shadow=True, ncol=3, loc='upper right')
        axes[1,0].grid(True, alpha=0.3)
        axes[1,0].axhline(y=0, color=self.colors['neutral'], linestyle='-', linewidth=1, alpha=0.5)
        axes[1,0].set_ylim(-1.2, 1.2)
        
        # 子图4：场强矢量图
        x = np.linspace(-3, 3, 15)
        y = np.linspace(-3, 3, 15)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个点的场强（简化模型）
        R = np.sqrt(X**2 + Y**2)
        R[R < 0.5] = 0.5
        
        # 引力场（指向中心）
        Ex = -X / R**2
        Ey = -Y / R**2
        magnitude = np.sqrt(Ex**2 + Ey**2)
        
        # 创建矢量场图
        quiver = axes[1,1].quiver(X, Y, Ex, Ey, magnitude, 
                                 cmap='viridis', alpha=0.7, scale=15, width=0.003)
        
        # 添加参考圆
        circle = plt.Circle((0, 0), self.r, fill=False, edgecolor=self.colors['highlight'], 
                          linewidth=2, linestyle='--', label='Helical Radius')
        axes[1,1].add_patch(circle)
        
        # 添加中心点
        axes[1,1].scatter(0, 0, color=self.colors['gravity'], s=150, 
                         edgecolors='black', linewidth=2, label='Mass Center', zorder=5)
        
        axes[1,1].set_xlabel('X (m)', fontweight='bold')
        axes[1,1].set_ylabel('Y (m)', fontweight='bold')
        axes[1,1].set_title('Gravitational Field Vector Distribution', fontweight='bold')
        axes[1,1].legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
        axes[1,1].grid(True, alpha=0.3)
        axes[1,1].set_aspect('equal')
        
        # 添加颜色条
        cbar = plt.colorbar(quiver, ax=axes[1,1], fraction=0.046, pad=0.04)
        cbar.set_label('Field Magnitude', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('Elegant_Physics_Fields.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Physics fields visualization saved: Elegant_Physics_Fields.png")
        
    def create_field_evolution(self):
        """创建场演化动态图"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Field Evolution Along Helical Path', fontsize=16, fontweight='bold')
        
        # 时间点
        time_points = [0, np.pi/2, np.pi]
        titles = ['Start (t=0)', 'Quarter Cycle (t=π/2)', 'Half Cycle (t=π)']
        
        for idx, (t_point, title) in enumerate(zip(time_points, titles)):
            ax = axes[idx]
            
            # 计算当前时刻的场
            x = self.r * np.cos(self.omega * t_point)
            y = self.r * np.sin(self.omega * t_point)
            
            # 电场矢量（恒定向上）
            ax.arrow(0, 0, 0, self.p, head_width=0.15, head_length=0.1, 
                    fc=self.colors['electric'], ec=self.colors['electric'], 
                    linewidth=2, label='E-field')
            
            # 磁场矢量（旋转）
            Bx = -self.r * self.omega * np.sin(self.omega * t_point)
            By = self.r * self.omega * np.cos(self.omega * t_point)
            ax.arrow(0, 0, Bx, By, head_width=0.15, head_length=0.1, 
                    fc=self.colors['magnetic'], ec=self.colors['magnetic'], 
                    linewidth=2, label='B-field')
            
            # 引力场矢量（指向中心）
            gx = -x / (x**2 + y**2) * 0.5
            gy = -y / (x**2 + y**2) * 0.5
            ax.arrow(0, 0, gx, gy, head_width=0.15, head_length=0.1, 
                    fc=self.colors['gravity'], ec=self.colors['gravity'], 
                    linewidth=2, label='G-field')
            
            # 标记粒子位置
            ax.scatter(x, y, color=self.colors['highlight'], s=200, 
                     edgecolors='black', linewidth=2, zorder=5)
            
            # 设置坐标轴
            limit = 2.5
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.set_xlabel('X', fontweight='bold')
            ax.set_ylabel('Y', fontweight='bold')
            ax.set_title(f'{title}\nPosition: ({x:.2f}, {y:.2f})', fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color=self.colors['neutral'], linestyle='-', alpha=0.3)
            ax.axvline(x=0, color=self.colors['neutral'], linestyle='-', alpha=0.3)
            ax.set_aspect('equal')
            
            # 添加图例
            if idx == 2:  # 只在最后一个子图显示图例
                ax.legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('Elegant_Field_Evolution.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Field evolution visualization saved: Elegant_Field_Evolution.png")
        
    def create_energy_distribution(self):
        """创建能量分布图"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Energy Distribution in Unified Field Theory', fontsize=16, fontweight='bold')
        
        # 计算能量密度
        total_energy = 0.5 * (self.r**2 * self.omega**2 + self.p**2)
        E_energy = 0.5 * self.p**2
        B_energy = 0.5 * self.r**2 * self.omega**2
        
        # 子图1：能量组成饼图
        labels = ['Electric Field', 'Magnetic Field']
        sizes = [E_energy, B_energy]
        colors = [self.colors['electric'], self.colors['magnetic']]
        
        wedges, texts, autotexts = axes[0,0].pie(sizes, labels=labels, colors=colors, 
                                                 autopct='%1.1f%%', startangle=90,
                                                 explode=(0.05, 0))
        axes[0,0].set_title('Electromagnetic Energy Distribution', fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        # 子图2：能量密度分布
        theta = np.linspace(0, 2*np.pi, 200)
        E_density = np.full_like(theta, E_energy)
        B_density = B_energy * np.cos(theta)**2  # 磁场能量密度的周期变化
        
        axes[0,1].fill_between(theta, 0, E_density, alpha=0.6, 
                              color=self.colors['electric'], label='E-field Energy')
        axes[0,1].fill_between(theta, E_density, E_density + B_density, 
                              alpha=0.6, color=self.colors['magnetic'], label='B-field Energy')
        
        axes[0,1].set_xlabel('Phase θ (rad)', fontweight='bold')
        axes[0,1].set_ylabel('Energy Density (J/kg)', fontweight='bold')
        axes[0,1].set_title('Total Energy Density Distribution', fontweight='bold')
        axes[0,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,1].grid(True, alpha=0.3)
        
        # 子图3：参数-能量关系
        omega_range = np.linspace(0.1, 2.0, 100)
        E_constant = np.full_like(omega_range, E_energy)
        B_variable = 0.5 * self.r**2 * omega_range**2
        total_variable = E_constant + B_variable
        
        axes[1,0].plot(omega_range, E_constant, color=self.colors['electric'], 
                       linewidth=3, label='Electric Energy')
        axes[1,0].plot(omega_range, B_variable, color=self.colors['magnetic'], 
                       linewidth=3, label='Magnetic Energy')
        axes[1,0].plot(omega_range, total_variable, color=self.colors['gravity'], 
                       linewidth=3, label='Total Energy', linestyle='--')
        
        # 标记当前参数点
        current_E = E_energy
        current_B = B_energy
        current_total = total_energy
        
        axes[1,0].scatter([self.omega], [current_E], color=self.colors['electric'], 
                         s=150, edgecolors='black', linewidth=2, zorder=5)
        axes[1,0].scatter([self.omega], [current_B], color=self.colors['magnetic'], 
                         s=150, edgecolors='black', linewidth=2, zorder=5)
        axes[1,0].scatter([self.omega], [current_total], color=self.colors['gravity'], 
                         s=150, edgecolors='black', linewidth=2, zorder=5)
        
        axes[1,0].set_xlabel('Angular Velocity ω (rad/s)', fontweight='bold')
        axes[1,0].set_ylabel('Energy (J/kg)', fontweight='bold')
        axes[1,0].set_title('Energy vs Angular Velocity', fontweight='bold')
        axes[1,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,0].grid(True, alpha=0.3)
        
        # 子图4：能流分析
        t = np.linspace(0, 4*np.pi, 200)
        x = self.r * np.cos(self.omega * t)
        y = self.r * np.sin(self.omega * t)
        z = self.p * t
        
        # Poynting矢量模（简化表示）
        S_magnitude = np.abs(self.p * self.r * self.omega)
        S_array = np.full_like(t, S_magnitude)
        
        axes[1,1].plot(t, S_array, color=self.colors['highlight'], linewidth=3)
        axes[1,1].set_xlabel('Time (s)', fontweight='bold')
        axes[1,1].set_ylabel('Poynting Vector Magnitude', fontweight='bold')
        axes[1,1].set_title(f'Energy Flow Rate (Constant = {S_magnitude:.3f})', fontweight='bold')
        axes[1,1].grid(True, alpha=0.3)
        axes[1,1].fill_between(t, 0, S_array, alpha=0.3, color=self.colors['highlight'])
        
        plt.tight_layout()
        plt.savefig('Elegant_Energy_Distribution.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Energy distribution analysis saved: Elegant_Energy_Distribution.png")
        
    def generate_all_visualizations(self):
        """生成所有物理场可视化"""
        print("Generating elegant physics field visualizations...")
        print("-" * 60)
        
        self.create_field_interpretation()
        self.create_field_evolution()
        self.create_energy_distribution()
        
        print("-" * 60)
        print("✅ All physics field visualizations generated!")
        print("\nGenerated files:")
        print("- Elegant_Physics_Fields.png")
        print("- Elegant_Field_Evolution.png") 
        print("- Elegant_Energy_Distribution.png")
        print("=" * 60)

def main():
    """主函数"""
    visualizer = PhysicsFieldVisualizer(r=1.0, omega=1.0, p=1.0)
    visualizer.generate_all_visualizations()

if __name__ == "__main__":
    main()