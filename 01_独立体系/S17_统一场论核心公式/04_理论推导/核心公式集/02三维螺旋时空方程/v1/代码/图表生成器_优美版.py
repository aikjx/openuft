#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论：优雅的图表生成器
专注于清晰的布局和优美的可视化
"""

import matplotlib.pyplot as plt
import numpy as np

class ElegantChartGenerator:
    """优雅的图表生成器"""
    
    def __init__(self, r=1.0, omega=1.0, p=1.0):
        self.r = r          # 螺旋半径
        self.omega = omega  # 角速度
        self.p = p          # 轴向速度
        self.t = np.linspace(0, 4*np.pi, 1000)
        
        # 设置优雅的样式
        self.setup_style()
        
    def setup_style(self):
        """设置优雅的matplotlib样式"""
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = '#f8f9fa'
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['axes.linewidth'] = 1.2
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        plt.rcParams['font.family'] = ['SimHei', 'DejaVu Sans', 'Microsoft YaHei']  # 添加中文字体支持
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['axes.titlesize'] = 13
        plt.rcParams['legend.fontsize'] = 9
        plt.rcParams['figure.titlesize'] = 16
        
        # 定义优雅的颜色方案
        self.colors = {
            'primary': '#2c3e50',     # 深蓝灰
            'secondary': '#e74c3c',   # 红色
            'tertiary': '#3498db',    # 蓝色
            'accent': '#27ae60',       # 绿色
            'highlight': '#f39c12',    # 橙色
            'neutral': '#95a5a6'      # 中性灰
        }
        
    def create_velocity_analysis(self):
        """创建速度分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Velocity Field Analysis', fontweight='bold', y=0.98)
        
        # 计算速度分量
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        Vy = self.r * self.omega * np.cos(self.omega * self.t)
        Vz = np.full_like(self.t, self.p)
        V_magnitude = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        theoretical_V = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        
        # 子图1：速度分量
        axes[0,0].plot(self.t, Vx, color=self.colors['secondary'], linewidth=2, label='Vₓ')
        axes[0,0].plot(self.t, Vy, color=self.colors['tertiary'], linewidth=2, label='Vᵧ')
        axes[0,0].plot(self.t, Vz, color=self.colors['accent'], linewidth=2, label='V𝓏')
        axes[0,0].set_xlabel('Time (s)')
        axes[0,0].set_ylabel('Velocity Components (m/s)')
        axes[0,0].set_title('Velocity Components vs Time', fontweight='bold')
        axes[0,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,0].grid(True, alpha=0.4)
        
        # 子图2：速度模
        axes[0,1].plot(self.t, V_magnitude, color=self.colors['primary'], 
                       linewidth=2.5, label='Calculated')
        axes[0,1].axhline(y=theoretical_V, color=self.colors['highlight'], 
                          linestyle='--', linewidth=2, label=f'Theory = {theoretical_V:.3f}')
        axes[0,1].set_xlabel('Time (s)')
        axes[0,1].set_ylabel('Speed Magnitude |V| (m/s)')
        axes[0,1].set_title('Constant Speed Verification', fontweight='bold')
        axes[0,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,1].grid(True, alpha=0.4)
        
        # 子图3：速度矢量相位图
        axes[1,0].plot(Vx, Vy, color=self.colors['tertiary'], linewidth=1.8, alpha=0.8)
        axes[1,0].scatter(Vx[0], Vy[0], color=self.colors['secondary'], s=100, 
                         label='Start', zorder=5, edgecolors='black', linewidth=2)
        axes[1,0].scatter(Vx[-1], Vy[-1], color=self.colors['accent'], s=100, 
                         label='End', zorder=5, edgecolors='black', linewidth=2)
        axes[1,0].set_xlabel('Vₓ (m/s)')
        axes[1,0].set_ylabel('Vᵧ (m/s)')
        axes[1,0].set_title('XY Plane Velocity Vector Trajectory', fontweight='bold')
        axes[1,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,0].grid(True, alpha=0.4)
        axes[1,0].axis('equal')
        
        # 子图4：速度分布直方图
        n, bins, patches = axes[1,1].hist(V_magnitude, bins=30, color=self.colors['tertiary'], 
                                         alpha=0.7, edgecolor='black', linewidth=1.2)
        axes[1,1].axvline(x=theoretical_V, color=self.colors['secondary'], 
                          linestyle='--', linewidth=2, label=f'Theory = {theoretical_V:.3f}')
        axes[1,1].set_xlabel('Speed Magnitude (m/s)')
        axes[1,1].set_ylabel('Frequency')
        axes[1,1].set_title('Speed Magnitude Distribution', fontweight='bold')
        axes[1,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,1].grid(True, alpha=0.4, axis='y')
        
        plt.tight_layout()
        plt.savefig('Elegant_Velocity_Analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Elegant velocity analysis saved: Elegant_Velocity_Analysis.png")
        
    def create_acceleration_analysis(self):
        """创建加速度分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Acceleration Field Analysis', fontweight='bold', y=0.98)
        
        # 计算加速度分量
        ax = -self.r * self.omega**2 * np.cos(self.omega * self.t)
        ay = -self.r * self.omega**2 * np.sin(self.omega * self.t)
        az = np.zeros_like(self.t)
        a_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
        theoretical_a = self.r * self.omega**2
        
        # 子图1：加速度分量
        axes[0,0].plot(self.t, ax, color=self.colors['secondary'], linewidth=2, label='aₓ')
        axes[0,0].plot(self.t, ay, color=self.colors['tertiary'], linewidth=2, label='aᵧ')
        axes[0,0].plot(self.t, az, color=self.colors['accent'], linewidth=2, label='a𝓏')
        axes[0,0].set_xlabel('Time (s)')
        axes[0,0].set_ylabel('Acceleration Components (m/s²)')
        axes[0,0].set_title('Acceleration Components vs Time', fontweight='bold')
        axes[0,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,0].grid(True, alpha=0.4)
        
        # 子图2：加速度模
        axes[0,1].plot(self.t, a_magnitude, color=self.colors['primary'], 
                       linewidth=2.5, label='Calculated')
        axes[0,1].axhline(y=theoretical_a, color=self.colors['highlight'], 
                          linestyle='--', linewidth=2, label=f'Theory = {theoretical_a:.3f}')
        axes[0,1].set_xlabel('Time (s)')
        axes[0,1].set_ylabel('Acceleration Magnitude |a| (m/s²)')
        axes[0,1].set_title('Constant Centripetal Acceleration', fontweight='bold')
        axes[0,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,1].grid(True, alpha=0.4)
        
        # 子图3：向心加速度分布
        theta = np.linspace(0, 2*np.pi, 100)
        a_centripetal = self.r * self.omega**2
        axes[1,0].fill_between(theta, 0, a_centripetal, color=self.colors['tertiary'], 
                              alpha=0.6, label=f'Centripetal = {a_centripetal:.3f}')
        axes[1,0].set_xlabel('Angle θ (rad)')
        axes[1,0].set_ylabel('Acceleration (m/s²)')
        axes[1,0].set_title('Centripetal Acceleration Distribution', fontweight='bold')
        axes[1,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,0].grid(True, alpha=0.4)
        
        # 子图4：速度-加速度相位关系
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        axes[1,1].plot(self.t, Vx, color=self.colors['tertiary'], linewidth=2, 
                       label='Vₓ', alpha=0.8)
        axes[1,1].plot(self.t, ax/(self.r*self.omega), color=self.colors['secondary'], 
                       linewidth=2, label='aₓ/(rω)', linestyle='--')
        axes[1,1].set_xlabel('Time (s)')
        axes[1,1].set_ylabel('Normalized Values')
        axes[1,1].set_title('Velocity-Acceleration Phase Relationship', fontweight='bold')
        axes[1,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,1].grid(True, alpha=0.4)
        
        plt.tight_layout()
        plt.savefig('Elegant_Acceleration_Analysis.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Elegant acceleration analysis saved: Elegant_Acceleration_Analysis.png")
        
    def create_energy_analysis(self):
        """创建能量分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Energy Conservation Analysis', fontweight='bold', y=0.98)
        
        # 计算能量分量
        V_magnitude = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        kinetic_energy = 0.5 * V_magnitude**2
        
        V_rot = self.r * self.omega
        V_lin = self.p
        KE_rot = 0.5 * V_rot**2
        KE_lin = 0.5 * V_lin**2
        
        # 子图1：能量分量分解
        energy_total = np.full_like(self.t, kinetic_energy)
        ke_rot_array = np.full_like(self.t, KE_rot)
        ke_lin_array = np.full_like(self.t, KE_lin)
        
        axes[0,0].fill_between(self.t, 0, ke_rot_array, color=self.colors['secondary'], 
                              alpha=0.6, label='Rotational KE')
        axes[0,0].fill_between(self.t, ke_rot_array, energy_total, color=self.colors['tertiary'], 
                              alpha=0.6, label='Linear KE')
        axes[0,0].set_xlabel('Time (s)')
        axes[0,0].set_ylabel('Kinetic Energy Density (J/kg)')
        axes[0,0].set_title('Energy Component Decomposition', fontweight='bold')
        axes[0,0].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,0].grid(True, alpha=0.4)
        
        # 子图2：能量守恒验证
        axes[0,1].plot(self.t, energy_total, color=self.colors['accent'], linewidth=2.5)
        axes[0,1].axhline(y=kinetic_energy, color=self.colors['highlight'], 
                          linestyle='--', linewidth=2, 
                          label=f'Theory = {kinetic_energy:.3f} J/kg')
        axes[0,1].set_xlabel('Time (s)')
        axes[0,1].set_ylabel('Total Kinetic Energy (J/kg)')
        axes[0,1].set_title('Energy Conservation Verification', fontweight='bold')
        axes[0,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[0,1].grid(True, alpha=0.4)
        
        # 子图3：能量分配饼图
        rot_ratio = KE_rot / kinetic_energy
        lin_ratio = KE_lin / kinetic_energy
        
        wedges, texts, autotexts = axes[1,0].pie([rot_ratio, lin_ratio], 
                                                 labels=['Rotational', 'Linear'],
                                                 colors=[self.colors['secondary'], self.colors['tertiary']],
                                                 autopct='%1.1f%%',
                                                 startangle=90,
                                                 explode=(0.05, 0))
        axes[1,0].set_title('Energy Distribution Ratio', fontweight='bold')
        
        # 美化饼图文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # 子图4：参数-能量关系
        omega_range = np.linspace(0.5, 2.0, 100)
        energy_curve = 0.5 * (self.r**2 * omega_range**2 + self.p**2)
        
        axes[1,1].plot(omega_range, energy_curve, color=self.colors['primary'], 
                       linewidth=2.5, marker='o', markersize=3)
        axes[1,1].scatter([self.omega], [kinetic_energy], color=self.colors['secondary'], 
                         s=150, edgecolors='black', linewidth=2, label='Current', zorder=5)
        axes[1,1].set_xlabel('Angular Velocity ω (rad/s)')
        axes[1,1].set_ylabel('Total Kinetic Energy (J/kg)')
        axes[1,1].set_title('Angular Velocity-Energy Relationship', fontweight='bold')
        axes[1,1].legend(frameon=True, fancybox=True, shadow=True)
        axes[1,1].grid(True, alpha=0.4)
        
        plt.tight_layout()
        plt.savefig('Elegant_Energy_Analysis.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Elegant energy analysis saved: Elegant_Energy_Analysis.png")
        
    def create_3d_trajectory(self):
        """创建3D轨迹图"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 计算螺旋轨迹
        x = self.r * np.cos(self.omega * self.t)
        y = self.r * np.sin(self.omega * self.t)
        z = self.p * self.t
        
        # 绘制螺旋线
        ax.plot(x, y, z, color=self.colors['primary'], linewidth=2.5, alpha=0.8)
        
        # 标记关键点
        key_times = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        key_labels = ['Start', '90°', '180°', '270°', '360°']
        colors_key = [self.colors['secondary'], self.colors['tertiary'], 
                    self.colors['accent'], self.colors['highlight'], self.colors['neutral']]
        
        for t_key, label, color in zip(key_times, key_labels, colors_key):
            x_key = self.r * np.cos(self.omega * t_key)
            y_key = self.r * np.sin(self.omega * t_key)
            z_key = self.p * t_key
            ax.scatter(x_key, y_key, z_key, color=color, s=100, 
                     edgecolors='black', linewidth=2, zorder=5)
            ax.text(x_key, y_key, z_key + 0.3, label, fontsize=10, 
                   fontweight='bold', ha='center')
        
        # 设置标签和标题
        ax.set_xlabel('X (m)', fontweight='bold')
        ax.set_ylabel('Y (m)', fontweight='bold')
        ax.set_zlabel('Z (m)', fontweight='bold')
        ax.set_title('3D Helical Motion Trajectory', fontweight='bold', fontsize=14)
        
        # 设置视角
        ax.view_init(elev=20, azim=45)
        
        # 美化网格
        ax.grid(True, alpha=0.3)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        plt.tight_layout()
        plt.savefig('Elegant_3D_Trajectory.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        print("✓ Elegant 3D trajectory saved: Elegant_3D_Trajectory.png")
        
    def generate_all_charts(self):
        """生成所有优雅图表"""
        print("Generating elegant charts for helical motion analysis...")
        print("-" * 60)
        
        self.create_velocity_analysis()
        self.create_acceleration_analysis()
        self.create_energy_analysis()
        self.create_3d_trajectory()
        
        print("-" * 60)
        print("✅ All elegant charts generated successfully!")
        print("\nGenerated files:")
        print("- Elegant_Velocity_Analysis.png")
        print("- Elegant_Acceleration_Analysis.png")
        print("- Elegant_Energy_Analysis.png")
        print("- Elegant_3D_Trajectory.png")
        print("=" * 60)


def main():
    """主函数"""
    generator = ElegantChartGenerator(r=1.0, omega=1.0, p=1.0)
    generator.generate_all_charts()


if __name__ == "__main__":
    main()
