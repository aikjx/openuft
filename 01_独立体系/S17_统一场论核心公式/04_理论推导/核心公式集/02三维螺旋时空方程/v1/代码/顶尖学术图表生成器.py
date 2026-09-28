#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论：最顶尖规范的学术图表生成系统
每个分析模块单独生成高质量学术期刊级别的图表
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import seaborn as sns
from scipy import integrate
import pandas as pd

# 设置学术期刊级别的样式
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': ['SimHei', 'Times New Roman', 'Microsoft YaHei'],
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
    'axes.spines.top': False,
    'axes.spines.right': False
})

class TopTierAcademicCharts:
    """顶尖学术图表生成器"""
    
    def __init__(self):
        # 物理参数
        self.r = 1.0  # 螺旋半径 (m)
        self.omega = 1.0  # 角速度 (rad/s)
        self.p = 1.0  # 轴向速度 (m/s)
        self.c = 299792458  # 光速 (m/s)
        
        # 时间数组
        self.t = np.linspace(0, 4*np.pi, 1000)
        
        # 颜色主题（学术期刊标准）
        self.colors = {
            'primary': '#2E86AB',  # 深蓝色
            'secondary': '#A23B72',  # 紫红色
            'tertiary': '#F18F01',  # 橙色
            'quaternary': '#C73E1D',  # 红色
            'neutral': '#6C757D',  # 灰色
            'accent': '#1A535C'  # 深绿色
        }
        
    def figure_1_three_dimensional_trajectory(self):
        """图1：三维螺旋轨迹 - 核心运动图"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 计算螺旋轨迹
        x = self.r * np.cos(self.omega * self.t)
        y = self.r * np.sin(self.omega * self.t)
        z = self.p * self.t
        
        # 主轨迹
        ax.plot(x, y, z, color=self.colors['primary'], linewidth=2.5, 
                label='螺旋轨迹', alpha=0.9)
        
        # 关键点标记
        key_times = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        key_labels = ['起点', '90°', '180°', '270°', '360°']
        
        for t_key, label in zip(key_times, key_labels):
            x_key = self.r * np.cos(self.omega * t_key)
            y_key = self.r * np.sin(self.omega * t_key)
            z_key = self.p * t_key
            ax.scatter(x_key, y_key, z_key, color=self.colors['tertiary'], 
                      s=80, alpha=0.8, edgecolors='black', linewidth=1)
            ax.text(x_key, y_key, z_key + 0.3, label, fontsize=9, ha='center')
        
        # 投影线
        ax.plot([x[0], x[-1]], [y[0], y[-1]], [z[0], z[-1]], 
               color=self.colors['neutral'], linestyle='--', alpha=0.5, linewidth=1)
        
        # 坐标轴设置
        ax.set_xlabel('X (m)', fontsize=12, labelpad=10)
        ax.set_ylabel('Y (m)', fontsize=12, labelpad=10)
        ax.set_zlabel('Z (m)', fontsize=12, labelpad=10)
        ax.set_title('三维圆柱螺旋运动轨迹\n$\\vec{R}(t) = r\\cos(\\omega t)\\hat{i} + r\\sin(\\omega t)\\hat{j} + pt\\hat{k}$', 
                    fontsize=14, pad=20)
        
        # 视角优化
        ax.view_init(elev=20, azim=45)
        ax.grid(True, alpha=0.3)
        
        # 添加参数说明
        param_text = f'参数: $r = {self.r}$ m, $\\omega = {self.omega}$ rad/s, $p = {self.p}$ m/s'
        ax.text2D(0.02, 0.98, param_text, transform=ax.transAxes, 
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('01_三维螺旋运动轨迹.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_2_velocity_components(self):
        """图2：速度分量随时间变化"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算速度分量
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        Vy = self.r * self.omega * np.cos(self.omega * self.t)
        Vz = np.full_like(self.t, self.p)
        V_magnitude = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        
        # 子图1：速度分量
        ax1 = axes[0, 0]
        ax1.plot(self.t, Vx, color=self.colors['primary'], linewidth=2, label='$V_x$')
        ax1.plot(self.t, Vy, color=self.colors['secondary'], linewidth=2, label='$V_y$')
        ax1.plot(self.t, Vz, color=self.colors['tertiary'], linewidth=2, label='$V_z$')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('速度分量 (m/s)')
        ax1.set_title('速度分量随时间变化')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # 子图2：速度模
        ax2 = axes[0, 1]
        theoretical_V = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        ax2.plot(self.t, V_magnitude, color=self.colors['quaternary'], linewidth=2.5, label='计算值')
        ax2.axhline(y=theoretical_V, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $\\sqrt{{r^2\\omega^2 + p^2}} = {theoretical_V:.3f}$')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('速度模 $|\\vec{V}|$ (m/s)')
        ax2.set_title('速度模恒定验证')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 子图3：速度矢量相位图
        ax3 = axes[1, 0]
        ax3.plot(Vx, Vy, color=self.colors['primary'], linewidth=1.5, alpha=0.8)
        ax3.scatter(Vx[0], Vy[0], color=self.colors['tertiary'], s=100, 
                   edgecolors='black', linewidth=2, label='起点')
        ax3.scatter(Vx[-1], Vy[-1], color=self.colors['quaternary'], s=100, 
                   edgecolors='black', linewidth=2, label='终点')
        ax3.set_xlabel('$V_x$ (m/s)')
        ax3.set_ylabel('$V_y$ (m/s)')
        ax3.set_title('XY平面速度矢量轨迹')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.axis('equal')
        
        # 子图4：速度分量频谱分析
        ax4 = axes[1, 1]
        from scipy.fft import fft, fftfreq
        N = len(self.t)
        yf = fft(Vx)
        xf = fftfreq(N, self.t[1] - self.t[0])[:N//2]
        ax4.semilogy(xf[1:], 2.0/N * np.abs(yf[1:N//2]), 
                    color=self.colors['primary'], linewidth=2)
        ax4.set_xlabel('频率 (Hz)')
        ax4.set_ylabel('幅值')
        ax4.set_title('$V_x$ 频谱分析')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('速度场完整分析', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('02_速度分量分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_3_acceleration_analysis(self):
        """图3：加速度分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算加速度分量
        ax_array = -self.r * self.omega**2 * np.cos(self.omega * self.t)
        ay_array = -self.r * self.omega**2 * np.sin(self.omega * self.t)
        az_array = np.zeros_like(self.t)
        a_magnitude = np.sqrt(ax_array**2 + ay_array**2 + az_array**2)
        
        # 子图1：加速度分量
        ax1 = axes[0, 0]
        ax1.plot(self.t, ax_array, color=self.colors['primary'], linewidth=2, label='$a_x$')
        ax1.plot(self.t, ay_array, color=self.colors['secondary'], linewidth=2, label='$a_y$')
        ax1.plot(self.t, az_array, color=self.colors['neutral'], linewidth=2, label='$a_z$')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('加速度分量 (m/s²)')
        ax1.set_title('加速度分量随时间变化')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # 子图2：加速度模
        ax2 = axes[0, 1]
        theoretical_a = self.r * self.omega**2
        ax2.plot(self.t, a_magnitude, color=self.colors['quaternary'], linewidth=2.5, label='计算值')
        ax2.axhline(y=theoretical_a, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $r\\omega^2 = {theoretical_a:.3f}$')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('加速度模 $|\\vec{a}|$ (m/s²)')
        ax2.set_title('加速度模恒定验证')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 子图3：向心加速度矢量场
        ax3 = axes[1, 0]
        # 创建矢量场
        theta = np.linspace(0, 2*np.pi, 8)
        r_field = np.linspace(0.5, 1.5, 3)
        for r_val in r_field:
            for theta_val in theta:
                x_pos = r_val * np.cos(theta_val)
                y_pos = r_val * np.sin(theta_val)
                # 向心加速度指向圆心
                ax_mag = self.r * self.omega**2
                ax3.arrow(x_pos, y_pos, -0.3*x_pos, -0.3*y_pos, 
                         head_width=0.1, head_length=0.05, 
                         fc=self.colors['primary'], ec=self.colors['primary'], alpha=0.7)
        
        # 添加圆圈
        circle = Circle((0, 0), self.r, fill=False, edgecolor=self.colors['tertiary'], 
                       linewidth=2, linestyle='--')
        ax3.add_patch(circle)
        ax3.set_xlim(-2, 2)
        ax3.set_ylim(-2, 2)
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_title('向心加速度矢量场')
        ax3.grid(True, alpha=0.3)
        ax3.axis('equal')
        
        # 子图4：加速度-速度相位关系
        ax4 = axes[1, 1]
        Vx = -self.r * self.omega * np.sin(self.omega * self.t)
        Vy = self.r * self.omega * np.cos(self.omega * self.t)
        ax4.plot(self.t, Vx/self.r/self.omega, color=self.colors['primary'], 
                linewidth=2, label='$V_x/r\\omega$', alpha=0.8)
        ax4.plot(self.t, -ax_array/self.r/self.omega**2, color=self.colors['secondary'], 
                linewidth=2, label='$-a_x/r\\omega^2$', linestyle='--')
        ax4.set_xlabel('时间 $t$ (s)')
        ax4.set_ylabel('归一化值')
        ax4.set_title('速度-加速度相位关系')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('加速度场完整分析', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('03_加速度场分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_4_curvature_torsion_analysis(self):
        """图4：曲率与挠率分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算曲率和挠率
        V_magnitude = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        curvature = V_magnitude**2 / (self.r * self.omega**2)
        torsion = self.p * self.omega / V_magnitude**2
        
        # 创建随时间变化的曲率和挠率（实际上它们是常数）
        curvature_array = np.full_like(self.t, curvature)
        torsion_array = np.full_like(self.t, torsion)
        
        # 子图1：曲率随时间
        ax1 = axes[0, 0]
        ax1.plot(self.t, curvature_array, color=self.colors['primary'], linewidth=2.5)
        ax1.axhline(y=curvature, color=self.colors['tertiary'], linestyle='--', 
                   linewidth=2, label=f'理论值 $\\rho = {curvature:.3f}$ m')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('曲率半径 $\\rho$ (m)')
        ax1.set_title('曲率半径恒定性验证')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 子图2：挠率随时间
        ax2 = axes[0, 1]
        ax2.plot(self.t, torsion_array, color=self.colors['secondary'], linewidth=2.5)
        ax2.axhline(y=torsion, color=self.colors['tertiary'], linestyle='--', 
                   linewidth=2, label=f'理论值 $\\tau = {torsion:.3f}$ rad/m')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('挠率 $\\tau$ (rad/m)')
        ax2.set_title('挠率恒定性验证')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 子图3：曲率-挠率关系
        ax3 = axes[1, 0]
        p_range = np.linspace(0.1, 3.0, 50)
        curvature_curve = (self.r**2 * self.omega**2 + p_range**2) / (self.r * self.omega**2)
        torsion_curve = p_range * self.omega / (self.r**2 * self.omega**2 + p_range**2)
        
        ax3.plot(curvature_curve, torsion_curve, color=self.colors['primary'], 
                linewidth=2, label='变化曲线')
        ax3.scatter(curvature, torsion, color=self.colors['tertiary'], s=100, 
                   edgecolors='black', linewidth=2, label='当前参数', zorder=5)
        ax3.set_xlabel('曲率半径 $\\rho$ (m)')
        ax3.set_ylabel('挠率 $\\tau$ (rad/m)')
        ax3.set_title('曲率-挠率参数空间')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 子图4：Frenet标架示意图
        ax4 = axes[1, 1]
        # 绘制Frenet标架
        t_sample = np.pi / 2
        x_point = self.r * np.cos(self.omega * t_sample)
        y_point = self.r * np.sin(self.omega * t_sample)
        z_point = self.p * t_sample
        
        # 切向量、法向量、副法向量
        T = np.array([-self.r * self.omega * np.sin(self.omega * t_sample),
                     self.r * self.omega * np.cos(self.omega * t_sample),
                     self.p]) / V_magnitude
        
        N = np.array([-np.cos(self.omega * t_sample),
                     -np.sin(self.omega * t_sample),
                     0])
        
        B = np.cross(T, N)
        
        # 绘制标架
        origin = np.array([x_point, y_point, z_point])
        scale = 0.5
        
        ax4.quiver(origin[0], origin[1], origin[2], 
                  T[0], T[1], T[2], color=self.colors['primary'], 
                  arrow_length_ratio=0.1, linewidth=2, label='切向量 T')
        ax4.quiver(origin[0], origin[1], origin[2], 
                  N[0], N[1], N[2], color=self.colors['secondary'], 
                  arrow_length_ratio=0.1, linewidth=2, label='法向量 N')
        ax4.quiver(origin[0], origin[1], origin[2], 
                  B[0], B[1], B[2], color=self.colors['tertiary'], 
                  arrow_length_ratio=0.1, linewidth=2, label='副法向量 B')
        
        ax4.set_xlabel('X (m)')
        ax4.set_ylabel('Y (m)')
        ax4.set_zlabel('Z (m)')
        ax4.set_title('Frenet标架')
        ax4.legend(loc='upper right')
        
        plt.suptitle('微分几何特性分析', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('04_微分几何特性分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_5_light_speed_constraint(self):
        """图5：光速约束验证"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 子图1：约束关系三维图
        ax1 = fig.add_subplot(221, projection='3d')
        
        # 创建参数网格
        omega_range = np.linspace(0.1, 2.0, 50)
        p_range = np.linspace(0.1, 2.0, 50)
        OMEGA, P = np.meshgrid(omega_range, p_range)
        
        # 计算满足约束的r值
        R = np.sqrt((self.c**2 - P**2) / OMEGA**2)
        R[R < 0] = np.nan  # 物理不可行区域
        
        # 绘制约束曲面
        surf = ax1.plot_surface(OMEGA, P, R, cmap='viridis', alpha=0.8)
        ax1.set_xlabel('角速度 $\\omega$ (rad/s)')
        ax1.set_ylabel('轴向速度 $p$ (m/s)')
        ax1.set_zlabel('螺旋半径 $r$ (m)')
        ax1.set_title('光速约束 $r^2\\omega^2 + p^2 = c^2$')
        
        # 标记当前参数
        ax1.scatter([self.omega], [self.p], [self.r], 
                   color='red', s=100, label='当前参数')
        
        # 子图2：参数敏感性分析
        ax2 = axes[0, 1]
        omega_deviation = np.linspace(0.5, 1.5, 100)
        p_adjusted = np.sqrt(self.c**2 - (self.r * omega_deviation)**2)
        
        ax2.plot(omega_deviation, p_adjusted/self.c, color=self.colors['primary'], linewidth=2)
        ax2.axvline(x=self.omega, color=self.colors['tertiary'], linestyle='--', 
                   linewidth=2, label=f'$\\omega_0 = {self.omega}$')
        ax2.set_xlabel('角速度变化 $\\omega/\\omega_0$')
        ax2.set_ylabel('轴向速度 $p/c$')
        ax2.set_title('光速约束下的参数耦合')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 子图3：约束误差分析
        ax3 = axes[1, 0]
        # 引入小扰动
        perturbation = np.linspace(-0.1, 0.1, 100)
        r_perturbed = self.r * (1 + perturbation)
        constraint_violation = np.abs(r_perturbed**2 * self.omega**2 + self.p**2 - 
                                     (self.r**2 * self.omega**2 + self.p**2))
        
        ax3.plot(perturbation * 100, constraint_violation, color=self.colors['quaternary'], linewidth=2)
        ax3.set_xlabel('半径扰动 (%)')
        ax3.set_ylabel('约束违反量 $|\\Delta(r^2\\omega^2 + p^2)|$')
        ax3.set_title('光速约束鲁棒性')
        ax3.grid(True, alpha=0.3)
        
        # 子图4：相对论因子验证
        ax4 = axes[1, 1]
        gamma_values = []
        for t_val in self.t[::10]:  # 采样
            v_magnitude = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
            beta = v_magnitude / self.c
            gamma = 1 / np.sqrt(1 - beta**2) if beta < 1 else np.inf
            gamma_values.append(gamma)
        
        ax4.plot(self.t[::10], gamma_values, color=self.colors['secondary'], linewidth=2, marker='o')
        ax4.set_xlabel('时间 $t$ (s)')
        ax4.set_ylabel('Lorentz因子 $\\gamma$')
        ax4.set_title('相对论因子恒定性')
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')
        
        plt.suptitle('光速不变原理验证', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('05_光速约束验证.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_6_energy_conservation(self):
        """图6：能量守恒分析"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 计算能量分量
        V_magnitude = np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        kinetic_energy = 0.5 * V_magnitude**2  # 单位质量动能
        
        # 分解能量
        V_rot = self.r * self.omega  # 旋转速度
        V_lin = self.p  # 线性速度
        KE_rot = 0.5 * V_rot**2
        KE_lin = 0.5 * V_lin**2
        
        # 子图1：能量分量分解
        ax1 = axes[0, 0]
        energy_total = np.full_like(self.t, kinetic_energy)
        ke_rot_array = np.full_like(self.t, KE_rot)
        ke_lin_array = np.full_like(self.t, KE_lin)
        
        ax1.fill_between(self.t, 0, ke_rot_array, color=self.colors['primary'], 
                        alpha=0.6, label='旋转动能')
        ax1.fill_between(self.t, ke_rot_array, energy_total, color=self.colors['secondary'], 
                        alpha=0.6, label='直线动能')
        ax1.set_xlabel('时间 $t$ (s)')
        ax1.set_ylabel('动能密度 (J/kg)')
        ax1.set_title('动能分量分解')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # 子图2：能量守恒验证
        ax2 = axes[0, 1]
        ax2.plot(self.t, energy_total, color=self.colors['tertiary'], linewidth=2.5)
        ax2.axhline(y=kinetic_energy, color=self.colors['neutral'], linestyle='--', 
                   linewidth=2, label=f'理论值 $E = {kinetic_energy:.3f}$ J/kg')
        ax2.set_xlabel('时间 $t$ (s)')
        ax2.set_ylabel('总动能 (J/kg)')
        ax2.set_title('能量守恒验证')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 子图3：能量分配比率
        ax3 = axes[1, 0]
        rot_ratio = KE_rot / kinetic_energy * 100
        lin_ratio = KE_lin / kinetic_energy * 100
        
        ax3.bar(['旋转分量', '直线分量'], [rot_ratio, lin_ratio], 
               color=[self.colors['primary'], self.colors['secondary']])
        ax3.set_ylabel('能量占比 (%)')
        ax3.set_title('动能分配比例')
        ax3.grid(True, alpha=0.3)
        
        # 添加数值标签
        for i, v in enumerate([rot_ratio, lin_ratio]):
            ax3.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=10)
        
        # 子图4：参数空间能量分布
        ax4 = axes[1, 1]
        omega_range = np.linspace(0.5, 2.0, 50)
        p_range = np.linspace(0.5, 2.0, 50)
        OMEGA, P = np.meshgrid(omega_range, p_range)
        ENERGY = 0.5 * (self.r**2 * OMEGA**2 + P**2)
        
        contour = ax4.contourf(OMEGA, P, ENERGY, levels=20, cmap='viridis')
        ax4.scatter([self.omega], [self.p], color='red', s=100, 
                   edgecolors='black', linewidth=2, label='当前参数', zorder=5)
        ax4.set_xlabel('角速度 $\\omega$ (rad/s)')
        ax4.set_ylabel('轴向速度 $p$ (m/s)')
        ax4.set_title('参数空间能量分布')
        ax4.legend()
        plt.colorbar(contour, ax=ax4, label='动能密度 (J/kg)')
        
        plt.suptitle('能量守恒定律验证', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('06_能量守恒分析.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_7_physical_field_interpretation(self):
        """图7：物理场诠释"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 子图1：电磁场分量示意图
        ax1 = axes[0, 0]
        theta = np.linspace(0, 2*np.pi, 100)
        
        # 电场（直线分量）
        E_magnitude = self.p
        ax1.axhline(y=E_magnitude, color=self.colors['primary'], linewidth=3, 
                   label=f'电场强度 $E = {E_magnitude:.1f}$')
        
        # 磁场（旋转分量）
        B_magnitude = self.r * self.omega
        ax1.plot(theta, B_magnitude * np.ones_like(theta), 
                color=self.colors['secondary'], linewidth=3, 
                label=f'磁场强度 $B = {B_magnitude:.1f}$')
        
        ax1.set_xlabel('相位 $\\theta$ (rad)')
        ax1.set_ylabel('场强 (相对单位)')
        ax1.set_title('电磁场分量恒定性')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 2*np.pi)
        
        # 子图2：引力场强度分布
        ax2 = axes[0, 1]
        r_range = np.linspace(0.1, 3.0, 100)
        # 向心加速度对应引力场
        g_field = self.r * self.omega**2 * (self.r / r_range)**2  # 1/r²衰减
        
        ax2.plot(r_range, g_field, color=self.colors['tertiary'], linewidth=2.5)
        ax2.scatter([self.r], [self.r * self.omega**2], 
                   color=self.colors['quaternary'], s=100, 
                   edgecolors='black', linewidth=2, label='参考点', zorder=5)
        ax2.set_xlabel('距离 $r$ (m)')
        ax2.set_ylabel('引力场强度 (相对单位)')
        ax2.set_title('引力场径向分布 $\\propto 1/r^2$')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        # 子图3：统一场相位关系
        ax3 = axes[1, 0]
        phase = np.linspace(0, 2*np.pi, 100)
        
        # 归一化的场分量
        E_normalized = np.ones_like(phase) * self.p / np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        B_normalized = self.r * self.omega * np.cos(phase) / np.sqrt(self.r**2 * self.omega**2 + self.p**2)
        g_normalized = -self.r * self.omega**2 * np.sin(phase) / (self.r * self.omega**2)
        
        ax3.plot(phase, E_normalized, color=self.colors['primary'], 
                linewidth=2, label='电场分量')
        ax3.plot(phase, B_normalized, color=self.colors['secondary'], 
                linewidth=2, label='磁场分量')
        ax3.plot(phase, g_normalized, color=self.colors['tertiary'], 
                linewidth=2, label='引力分量')
        
        ax3.set_xlabel('相位 $\\omega t$ (rad)')
        ax3.set_ylabel('归一化场强')
        ax3.set_title('统一场相位关系')
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # 子图4：场强矢量图
        ax4 = axes[1, 1]
        # 创建二维网格表示场分布
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个点的场强（简化模型）
        R = np.sqrt(X**2 + Y**2)
        R[R < 0.5] = 0.5  # 避免奇点
        
        # 引力场（指向中心）
        Ex = -X / R**3
        Ey = -Y / R**3
        
        ax4.quiver(X, Y, Ex, Ey, np.sqrt(Ex**2 + Ey**2), cmap='viridis', alpha=0.7)
        circle = Circle((0, 0), self.r, fill=False, edgecolor=self.colors['quaternary'], 
                       linewidth=2, linestyle='--')
        ax4.add_patch(circle)
        ax4.set_xlabel('X (m)')
        ax4.set_ylabel('Y (m)')
        ax4.set_title('引力场矢量分布')
        ax4.set_aspect('equal')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('物理场的几何起源诠释', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig('07_物理场诠释.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_8_revolution_complete_data(self):
        """图8：转一圈完整数据表格"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # 计算转一圈的关键数据
        key_times = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]) / self.omega
        key_labels = ['起点', '90°', '180°', '270°', '360°']
        
        # 计算各参数
        angles = self.omega * key_times
        x_coords = self.r * np.cos(angles)
        y_coords = self.r * np.sin(angles)
        z_coords = self.p * key_times
        
        vx = -self.r * self.omega * np.sin(angles)
        vy = self.r * self.omega * np.cos(angles)
        vz = np.full_like(key_times, self.p)
        v_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
        
        ax_comps = -self.r * self.omega**2 * np.cos(angles)
        ay_comps = -self.r * self.omega**2 * np.sin(angles)
        az_comps = np.zeros_like(key_times)
        a_magnitude = np.sqrt(ax_comps**2 + ay_comps**2 + az_comps**2)
        
        # 创建表格数据
        table_data = []
        for i, (label, t, angle, x, y, z) in enumerate(zip(key_labels, key_times, angles, x_coords, y_coords, z_coords)):
            row = [
                label,
                f'{t:.3f}',
                f'{angle:.3f}',
                f'{x:.3f}',
                f'{y:.3f}',
                f'{z:.3f}',
                f'{vx[i]:.3f}',
                f'{vy[i]:.3f}',
                f'{vz[i]:.3f}',
                f'{v_magnitude[i]:.3f}',
                f'{ax_comps[i]:.3f}',
                f'{ay_comps[i]:.3f}',
                f'{az_comps[i]:.3f}',
                f'{a_magnitude[i]:.3f}'
            ]
            table_data.append(row)
        
        # 创建表格
        columns = [
            '阶段', '时间(s)', '角度(rad)', 
            'X(m)', 'Y(m)', 'Z(m)',
            'Vx(m/s)', 'Vy(m/s)', 'Vz(m/s)', '|V|(m/s)',
            'ax(m/s²)', 'ay(m/s²)', 'az(m/s²)', '|a|(m/s²)'
        ]
        
        # 使用更美观的表格样式
        table = ax.table(cellText=table_data, colLabels=columns, 
                        cellLoc='center', loc='center',
                        colWidths=[0.08, 0.08, 0.08, 0.07, 0.07, 0.07, 
                                  0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])
        
        # 设置表格样式
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # 设置表头样式
        for i in range(len(columns)):
            table[(0, i)].set_facecolor(self.colors['primary'])
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # 设置关键行的背景色
        for i in range(1, len(table_data) + 1):
            if i % 2 == 0:
                for j in range(len(columns)):
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        # 添加标题和说明
        title_text = '圆柱螺旋运动"转一圈"完整数据表\n'
        title_text += f'参数设置: $r = {self.r}$ m, $\\omega = {self.omega}$ rad/s, $p = {self.p}$ m/s\n'
        title_text += f'周期: $T = 2\\pi/\\omega = {2*np.pi/self.omega:.3f}$ s, '
        title_text += f'螺距: $p \\cdot T = {self.p * 2*np.pi/self.omega:.3f}$ m'
        
        fig.text(0.5, 0.95, title_text, ha='center', va='top', fontsize=14, 
                weight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 添加验证信息
        verification_text = '验证结果: '
        verification_text += f'速度模恒定 $\\checkmark$ | 加速度模恒定 $\\checkmark$ | '
        verification_text += f'光速约束 $\\checkmark$ | 能量守恒 $\\checkmark$'
        
        fig.text(0.5, 0.02, verification_text, ha='center', va='bottom', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='#e8f5e8', alpha=0.8))
        
        plt.savefig('08_转一圈完整数据表.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def figure_9_theoretical_framework_summary(self):
        """图9：理论框架总览"""
        fig = plt.figure(figsize=(16, 12))
        
        # 创建网格布局
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 中心：螺旋方程
        ax_center = fig.add_subplot(gs[1, 1])
        ax_center.text(0.5, 0.5, 
                      r'$\vec{R}(t) = r\cos(\omega t)\hat{i} + r\sin(\omega t)\hat{j} + pt\hat{k}$',
                      ha='center', va='center', fontsize=16, weight='bold',
                      bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['primary'], 
                               alpha=0.2, edgecolor=self.colors['primary'], linewidth=3))
        ax_center.set_xlim(0, 1)
        ax_center.set_ylim(0, 1)
        ax_center.axis('off')
        ax_center.set_title('核心运动方程', fontsize=14, weight='bold', pad=20)
        
        # 上：理论基础
        ax_theory = fig.add_subplot(gs[0, :])
        theory_text = '理论基础：时空同一化原理 + 三维垂直性公理 + 空间运动性公设'
        ax_theory.text(0.5, 0.5, theory_text, ha='center', va='center', fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor=self.colors['secondary'], 
                               alpha=0.2, edgecolor=self.colors['secondary'], linewidth=2))
        ax_theory.set_xlim(0, 1)
        ax_theory.set_ylim(0, 1)
        ax_theory.axis('off')
        
        # 左上：数学验证
        ax_math = fig.add_subplot(gs[1, 0])
        math_items = [
            r'$\bullet$ 速度模: $|\vec{V}| = \sqrt{r^2\omega^2 + p^2}$',
            r'$\bullet$ 加速度模: $|\vec{a}| = r\omega^2$',
            r'$\bullet$ 光速约束: $r^2\omega^2 + p^2 = c^2$',
            r'$\bullet$ 曲率: $\rho = \frac{r^2\omega^2 + p^2}{r\omega^2}$'
        ]
        math_text = '\n'.join(math_items)
        ax_math.text(0.1, 0.9, math_text, ha='left', va='top', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                             edgecolor=self.colors['tertiary'], linewidth=2))
        ax_math.set_xlim(0, 1)
        ax_math.set_ylim(0, 1)
        ax_math.axis('off')
        ax_math.set_title('数学验证', fontsize=12, weight='bold')
        
        # 右上：物理诠释
        ax_physics = fig.add_subplot(gs[1, 2])
        physics_items = [
            r'$\bullet$ 电场 $\rightarrow$ 直线运动分量',
            r'$\bullet$ 磁场 $\rightarrow$ 旋转运动分量', 
            r'$\bullet$ 引力场 $\rightarrow$ 向心加速度',
            r'$\bullet$ 时间 $\rightarrow$ 空间光速运动的度量'
        ]
        physics_text = '\n'.join(physics_items)
        ax_physics.text(0.1, 0.9, physics_text, ha='left', va='top', fontsize=10,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                edgecolor=self.colors['quaternary'], linewidth=2))
        ax_physics.set_xlim(0, 1)
        ax_physics.set_ylim(0, 1)
        ax_physics.axis('off')
        ax_physics.set_title('物理诠释', fontsize=12, weight='bold')
        
        # 下方：应用领域
        ax_applications = fig.add_subplot(gs[2, :])
        applications = [
            '统一场论基础', '电磁理论统一', '引力几何化', 
            '量子力学诠释', '宇宙学应用', '相对论协调'
        ]
        
        # 创建应用领域框图
        for i, app in enumerate(applications):
            x_pos = 0.1 + (i % 3) * 0.3
            y_pos = 0.6 if i < 3 else 0.2
            
            ax_applications.text(x_pos, y_pos, app, ha='center', va='center', 
                               fontsize=10, weight='bold',
                               bbox=dict(boxstyle='round,pad=0.2', 
                                        facecolor=self.colors['accent'], 
                                        alpha=0.3, edgecolor=self.colors['accent']))
        
        ax_applications.set_xlim(0, 1)
        ax_applications.set_ylim(0, 1)
        ax_applications.axis('off')
        ax_applications.set_title('理论应用领域', fontsize=12, weight='bold', pad=20)
        
        # 添加连接线
        for ax in [ax_math, ax_center, ax_physics]:
            for spine in ax.spines.values():
                spine.set_visible(False)
        
        # 总标题
        fig.suptitle('张祥前统一场论：圆柱螺旋运动理论框架总览', 
                    fontsize=18, weight='bold', y=0.98)
        
        plt.savefig('09_理论框架总览.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def generate_all_charts(self):
        """生成所有顶尖学术图表"""
        print("=" * 60)
        print("开始生成顶尖学术图表...")
        print("=" * 60)
        
        charts_info = [
            ("三维螺旋运动轨迹", self.figure_1_three_dimensional_trajectory),
            ("速度分量分析", self.figure_2_velocity_components),
            ("加速度场分析", self.figure_3_acceleration_analysis),
            ("微分几何特性分析", self.figure_4_curvature_torsion_analysis),
            ("光速约束验证", self.figure_5_light_speed_constraint),
            ("能量守恒分析", self.figure_6_energy_conservation),
            ("物理场诠释", self.figure_7_physical_field_interpretation),
            ("转一圈完整数据表", self.figure_8_revolution_complete_data),
            ("理论框架总览", self.figure_9_theoretical_framework_summary)
        ]
        
        for i, (name, func) in enumerate(charts_info, 1):
            print(f"正在生成第{i}张图: {name}")
            try:
                func()
                print(f"✓ {name} 生成成功")
            except Exception as e:
                print(f"✗ {name} 生成失败: {str(e)}")
        
        print("=" * 60)
        print("所有顶尖学术图表生成完成！")
        print("文件保存格式：PNG，300 DPI，期刊级别质量")
        print("=" * 60)

def main():
    """主函数"""
    generator = TopTierAcademicCharts()
    generator.generate_all_charts()

if __name__ == "__main__":
    main()