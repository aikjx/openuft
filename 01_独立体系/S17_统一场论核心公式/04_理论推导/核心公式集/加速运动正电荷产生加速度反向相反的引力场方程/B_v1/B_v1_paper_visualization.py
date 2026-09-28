#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B_v1公式论文顶尖Python可视化
高质量科学论文可视化脚本
展示B_v1公式的核心概念、推导过程和物理意义
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
from mpl_toolkits.mplot3d import Axes3D

# 全面抑制所有警告
warnings.filterwarnings('ignore')

# 设置中文字体和数学符号字体（使用支持中文和数学的字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei UI', 'SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']  # 用来正常显示中文标签
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['mathtext.fontset'] = 'cm'  # 使用Computer Modern字体集（更好支持数学符号）
plt.rcParams['text.usetex'] = False  # 禁用LaTeX以确保中文兼容性
plt.rcParams['axes.formatter.use_mathtext'] = True  # 使用mathtext渲染数学符号

class Bv1Visualization:
    """B_v1公式论文可视化类"""
    
    def __init__(self):
        """初始化可视化类"""
        self.fig = plt.figure(figsize=(16, 12), dpi=100)
        self.fig.suptitle('B_v1公式论文可视化', fontsize=20, fontweight='bold')
        
    def plot_core_formula(self, ax):
        """绘制核心公式"""
        ax.clear()
        ax.set_title('核心公式：B_v1', fontsize=16)
        ax.axis('off')
        
        # 核心公式
        formula = '''B_θ = (-q/(4πε₀c³r)) · A × r̂
        
        其中：
        q: 电荷量
        ε₀: 真空介电常数
        c: 光速
        r: 距离
        A: 加速度矢量
        r̂: 径向单位矢量'''
        
        ax.text(0.1, 0.9, formula, fontsize=14, ha='left', va='top', 
                transform=ax.transAxes)
        
    def plot_vector_field(self, ax):
        """绘制矢量场：辐射磁场的方向和强度"""
        ax.clear()
        ax.set_title('辐射磁场矢量场', fontsize=16)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        
        # 创建网格
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        z = np.linspace(-2, 2, 10)
        X, Y, Z = np.meshgrid(x, y, z)
        
        # 电荷位置（原点）
        q_pos = np.array([0, 0, 0])
        
        # 计算距离和单位矢量
        r = np.sqrt(X**2 + Y**2 + Z**2)
        r[r < 0.1] = 0.1  # 避免除零
        
        # 径向单位矢量
        ux = X / r
        uy = Y / r
        uz = Z / r
        
        # 假设加速度方向沿z轴
        a_vec = np.array([0, 0, 1])
        
        # 计算磁场矢量 (B = -q/(4πε0c³r) * A × r_hat)
        # 简化为比例关系
        Bx = -(a_vec[1] * uz - a_vec[2] * uy) / r
        By = -(a_vec[2] * ux - a_vec[0] * uz) / r
        Bz = -(a_vec[0] * uy - a_vec[1] * ux) / r
        
        # 归一化矢量长度以增强可视化效果
        B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
        B_mag[B_mag < 1e-10] = 1e-10
        Bx = Bx / B_mag * 0.1
        By = By / B_mag * 0.1
        Bz = Bz / B_mag * 0.1
        
        # 绘制矢量场
        ax.quiver(X, Y, Z, Bx, By, Bz, length=0.1, color='blue', alpha=0.7)
        
        # 绘制电荷位置
        ax.scatter(q_pos[0], q_pos[1], q_pos[2], color='red', s=100, label='电荷')
        
        # 绘制加速度矢量
        ax.quiver(q_pos[0], q_pos[1], q_pos[2], a_vec[0], a_vec[1], a_vec[2], 
                  length=0.5, color='green', label='加速度')
        
        ax.legend()
        ax.set_box_aspect([1, 1, 1])
        
    def plot_derivation_steps(self, ax):
        """绘制公式推导步骤"""
        ax.clear()
        ax.set_title('公式推导步骤', fontsize=16)
        ax.axis('off')
        
        derivation = '''1. 辐射电场：
        E_rad = (q/(4πε₀c²r)) · r̂ × (r̂ × a)
        
        2. 辐射磁场：
        B_rad = (1/c) · r̂ × E_rad
        
        3. 代入电场表达式：
        B_rad = (q/(4πε₀c³r)) · r̂ × (r̂ × (r̂ × a))
        
        4. 应用矢量恒等式：
        r̂ × (r̂ × a) = a - (r̂·a)r̂
        
        5. 简化：
        r̂ × (r̂ × (r̂ × a)) = r̂ × a
        
        6. 应用叉乘反交换律：
        r̂ × a = -a × r̂
        
        7. 最终得到B_v1公式：
        B_θ = (-q/(4πε₀c³r)) · a × r̂'''
        
        ax.text(0.1, 0.9, derivation, fontsize=12, ha='left', va='top', 
                transform=ax.transAxes)
        
    def plot_vector_identity(self, ax):
        """绘制矢量恒等式"""
        ax.clear()
        ax.set_title('矢量恒等式可视化', fontsize=16)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        
        # 绘制坐标系
        ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.5)
        
        # 径向单位矢量
        r_hat = np.array([1, 0])
        
        # 加速度矢量
        a = np.array([0.5, 1])
        
        # 绘制矢量
        ax.quiver(0, 0, r_hat[0], r_hat[1], color='red', label='r̂', angles='xy', scale_units='xy', scale=1)
        ax.quiver(0, 0, a[0], a[1], color='green', label='a', angles='xy', scale_units='xy', scale=1)
        
        # 计算 r̂ × (r̂ × a)
        cross1 = np.cross(np.append(r_hat, 0), np.append(a, 0))[2]
        cross2 = np.cross(np.append(r_hat, 0), np.array([0, 0, cross1]))[:2]
        
        # 计算 a - (r̂·a)r̂
        dot_product = np.dot(r_hat, a)
        rhs = a - dot_product * r_hat
        
        # 绘制结果矢量
        ax.quiver(0, 0, cross2[0], cross2[1], color='blue', label='r̂×(r̂×a)', angles='xy', scale_units='xy', scale=1)
        ax.quiver(0, 0, rhs[0], rhs[1], color='purple', label='a - (r̂·a)r̂', angles='xy', scale_units='xy', scale=1)
        
        # 添加公式
        formula = 'r̂ × (r̂ × a) = a - (r̂·a)r̂'
        ax.text(0.1, 1.3, formula, fontsize=14, ha='left', va='top')
        
        ax.legend()
        
    def plot_retarded_time(self, ax):
        """绘制推迟时间效应"""
        ax.clear()
        ax.set_title('推迟时间效应', fontsize=16)
        ax.set_xlabel('时间 t')
        ax.set_ylabel('距离 r')
        
        # 时间范围
        t = np.linspace(0, 5, 100)
        
        # 光速
        c = 1
        
        # 距离随时间变化
        r = c * t
        
        # 推迟时间
        t_prime = t - r/c  # 等于0，因为 r = ct
        
        # 绘制距离-时间关系
        ax.plot(t, r, 'b-', label='r = ct')
        ax.plot(t, t_prime, 'r--', label="t' = t - r/c")
        
        # 添加说明
        ax.text(1, 3, '推迟时间：信号以光速传播', fontsize=12)
        ax.text(1, 2.5, "观测到的是电荷在 t' 时刻的状态", fontsize=12)
        
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_physical_meaning(self, ax):
        """绘制物理意义：距离衰减和加速度依赖"""
        ax.clear()
        ax.set_title('物理意义分析', fontsize=16)
        ax.set_xlabel('距离 r')
        ax.set_ylabel('磁场强度 |B|')
        
        # 距离范围
        r = np.linspace(0.1, 5, 100)
        
        # 磁场强度与距离的关系 (1/r 衰减)
        B_r = 1 / r
        
        # 不同加速度的影响
        a_values = [0.5, 1, 2]
        colors = ['r', 'g', 'b']
        labels = [f'a = {a}' for a in a_values]
        
        for a, color, label in zip(a_values, colors, labels):
            B_a = a / r
            ax.plot(r, B_a, color=color, label=label)
        
        # 添加说明
        ax.text(3, 0.8, '磁场强度与加速度成正比', fontsize=12)
        ax.text(3, 0.6, '与距离成反比（辐射场特征）', fontsize=12)
        
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_comparison(self, ax):
        """绘制与经典电动力学的比较"""
        ax.clear()
        ax.set_title('与经典电动力学的比较', fontsize=16)
        ax.axis('off')
        
        comparison = '''经典电动力学辐射磁场：
        B_rad = (q/(4πε₀c³r)) · r̂ × (r̂ × a)
        
        B_v1公式：
        B_θ = (-q/(4πε₀c³r)) · a × r̂
        
        通过矢量恒等式化简：
        r̂ × (r̂ × a) = a - (r̂·a)r̂
        r̂ × (r̂ × (r̂ × a)) = r̂ × a = -a × r̂
        
        结论：两者完全一致！'''
        
        ax.text(0.1, 0.9, comparison, fontsize=12, ha='left', va='top', 
                transform=ax.transAxes)
        
    def create_visualization(self):
        """创建完整的可视化"""
        # 创建子图
        gs = self.fig.add_gridspec(3, 3, height_ratios=[1, 1.5, 1])
        
        # 核心公式
        ax1 = self.fig.add_subplot(gs[0, 0])
        self.plot_core_formula(ax1)
        
        # 矢量场
        ax2 = self.fig.add_subplot(gs[1, 0], projection='3d')
        self.plot_vector_field(ax2)
        
        # 公式推导
        ax3 = self.fig.add_subplot(gs[1, 1])
        self.plot_derivation_steps(ax3)
        
        # 矢量恒等式
        ax4 = self.fig.add_subplot(gs[0, 1])
        self.plot_vector_identity(ax4)
        
        # 推迟时间
        ax5 = self.fig.add_subplot(gs[0, 2])
        self.plot_retarded_time(ax5)
        
        # 物理意义
        ax6 = self.fig.add_subplot(gs[1, 2])
        self.plot_physical_meaning(ax6)
        
        # 与经典理论比较
        ax7 = self.fig.add_subplot(gs[2, :])
        self.plot_comparison(ax7)
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        
    def save_visualization(self, filename='B_v1_visualization.png'):
        """保存可视化"""
        self.fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"可视化已保存为：{filename}")

if __name__ == "__main__":
    # 创建可视化实例
    viz = Bv1Visualization()
    
    # 创建可视化
    viz.create_visualization()
    
    # 保存可视化
    viz.save_visualization()
    
    # 显示可视化
    plt.show()
