#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无乱码几何因子动画：3D到2D几何变换可视化
Zhang Xiangqian Unified Field Theory: Geometric Factor G = 4π/2π = 2

完全兼容版本，解决中文显示问题
展示核心数学概念：从球对称3D空间到2D平面投影的几何因子推导

Author: Based on Zhang Xiangqian Unified Field Theory
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge
import math

# 设置matplotlib参数以支持中文显示
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['figure.dpi'] = 100

class GeometricFactorAnimator:
    """几何因子动画器 - 无乱码版本"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 120
        self.current_frame = 0
        
        # 颜色配置
        self.colors = {
            'sphere': '#FF4444',
            'projection': '#4488FF', 
            'vectors': '#44AA44',
            'highlight': '#FFAA00',
            'text': '#000000',
            'formula': '#AA44AA'
        }
        
        # 数学常数
        self.pi = np.pi
        
        # 文本标签（避免中文乱码）
        self.labels = {
            'title_3d': '3D Spherical Field\n4π steradians',
            'title_2d': '2D Projection\n2π radians', 
            'title_math': 'Mathematical Derivation',
            'title_integral': 'Integration: ∫sin^2(θ)dθ = π/2',
            'title_comparison': 'Value Comparison',
            'title_result': 'Geometric Factor',
            'geometric_factor': 'G = 4π/2π = 2',
            'zhang_theory': 'Zhang Xiangqian Unified Field Theory',
            'projection_factor': '3D→2D Projection Scaling Factor'
        }
        
    def setup_figure(self):
        """设置图形和子图"""
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('white')
        
        # 创建子图网格 (2x3)
        self.ax_3d = self.fig.add_subplot(231, projection='3d')
        self.ax_2d = self.fig.add_subplot(232)
        self.ax_math = self.fig.add_subplot(233)
        self.ax_integral = self.fig.add_subplot(234)
        self.ax_comparison = self.fig.add_subplot(235)
        self.ax_result = self.fig.add_subplot(236)
        
        return self.fig
    
    def create_sphere_surface(self, resolution=20):
        """创建球面数据"""
        u = np.linspace(0, 2 * self.pi, resolution)
        v = np.linspace(0, self.pi, resolution)
        
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        return x, y, z
    
    def create_vector_field(self, n_vectors=8):
        """创建球面矢量场"""
        vectors = []
        
        for i in range(n_vectors):
            for j in range(n_vectors//2):
                theta = 2 * self.pi * i / n_vectors
                phi = self.pi * j / (n_vectors//2)
                
                x = 1.4 * np.sin(phi) * np.cos(theta)
                y = 1.4 * np.sin(phi) * np.sin(theta)
                z = 1.4 * np.cos(phi)
                
                vectors.append([0, 0, 0, x, y, z])
        
        return vectors
    
    def animate_3d_view(self, frame):
        """动画3D视图"""
        self.ax_3d.clear()
        
        # 旋转角度
        rotation = frame * 4 * self.pi / self.total_frames
        
        # 创建球面
        x, y, z = self.create_sphere_surface()
        
        # 绘制球面
        self.ax_3d.plot_surface(x, y, z, alpha=0.25, color=self.colors['sphere'])
        self.ax_3d.plot_wireframe(x, y, z, alpha=0.15, color='gray', linewidth=0.5)
        
        # 绘制矢量场
        vectors = self.create_vector_field(6)
        
        # 显示部分矢量
        for i, vec in enumerate(vectors[::3]):  # 每隔2个显示
            # 应用旋转变换
            x_rot = vec[3] * np.cos(rotation) - vec[4] * np.sin(rotation)
            y_rot = vec[3] * np.sin(rotation) + vec[4] * np.cos(rotation)
            z_rot = vec[5]
            
            # 矢量长度动画
            scale = 0.8 + 0.2 * np.sin(frame * 0.2 + i)
            
            self.ax_3d.quiver(vec[0], vec[1], vec[2], 
                             x_rot*scale, y_rot*scale, z_rot*scale,
                             color=self.colors['vectors'], alpha=0.8, 
                             arrow_length_ratio=0.12, linewidth=2)
        
        # 绘制投影平面（XY平面）
        if frame > 20:
            plane_size = 1.6
            xx, yy = np.meshgrid([-plane_size, plane_size], [-plane_size, plane_size])
            zz = np.zeros_like(xx)
            self.ax_3d.plot_surface(xx, yy, zz, alpha=0.2, color=self.colors['projection'])
            
            # 平面边界
            boundary = np.linspace(-plane_size, plane_size, 50)
            zeros = np.zeros_like(boundary)
            self.ax_3d.plot(boundary, plane_size*np.ones_like(boundary), zeros, 
                           color=self.colors['projection'], linewidth=2)
            self.ax_3d.plot(boundary, -plane_size*np.ones_like(boundary), zeros, 
                           color=self.colors['projection'], linewidth=2)
            self.ax_3d.plot(plane_size*np.ones_like(boundary), boundary, zeros, 
                           color=self.colors['projection'], linewidth=2)
            self.ax_3d.plot(-plane_size*np.ones_like(boundary), boundary, zeros, 
                           color=self.colors['projection'], linewidth=2)
        
        # 设置3D图属性
        self.ax_3d.set_xlim([-2, 2])
        self.ax_3d.set_ylim([-2, 2])
        self.ax_3d.set_zlim([-2, 2])
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.set_title(self.labels['title_3d'], fontweight='bold', fontsize=11)
        
        # 动态视角
        self.ax_3d.view_init(elev=25 + 5*np.sin(frame*0.05), azim=frame * 2.5)
    
    def animate_2d_projection(self, frame):
        """动画2D投影"""
        self.ax_2d.clear()
        
        # 投影进度（0到1，带振荡）
        base_progress = min(1.0, frame / (self.total_frames * 0.7))
        oscillation = 0.1 * np.sin(frame * 0.3)
        progress = max(0, min(1, base_progress + oscillation))
        
        # 绘制单位圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['sphere'], linewidth=3)
        self.ax_2d.add_patch(circle)
        
        # 绘制投影区域
        if progress > 0:
            theta_max = self.pi * progress
            theta = np.linspace(0, theta_max, 60)
            x_proj = np.cos(theta)
            y_proj = np.sin(theta)
            
            # 填充投影区域
            self.ax_2d.fill_between(x_proj, 0, y_proj, alpha=0.4, 
                                  color=self.colors['projection'])
            
            # 绘制投影射线
            n_rays = max(1, int(10 * progress))
            for i in range(n_rays):
                if n_rays > 1:
                    angle = theta_max * i / (n_rays - 1)
                else:
                    angle = 0
                
                x_end = np.cos(angle)
                y_end = np.sin(angle)
                
                # 射线颜色渐变
                alpha = 1 - (angle / self.pi) * 0.4
                
                self.ax_2d.plot([0, x_end], [0, y_end], 
                               color=self.colors['vectors'], linewidth=2.5, alpha=alpha)
                
                # 添加箭头（每隔一个）
                if i % 2 == 0 and progress > 0.3:
                    arrow_start = 0.6
                    self.ax_2d.annotate('', 
                                      xy=(x_end, y_end), 
                                      xytext=(arrow_start*x_end, arrow_start*y_end),
                                      arrowprops=dict(arrowstyle='->', 
                                                    color=self.colors['vectors'], 
                                                    lw=2, alpha=alpha))
        
        # 绘制角度弧
        if progress > 0.15:
            angle_deg = progress * 180
            wedge = Wedge((0, 0), 0.3, 0, angle_deg, 
                         facecolor=self.colors['highlight'], alpha=0.7)
            self.ax_2d.add_patch(wedge)
            
            # 角度标签
            mid_angle = self.pi * progress / 2
            label_x = 0.4 * np.cos(mid_angle)
            label_y = 0.4 * np.sin(mid_angle)
            self.ax_2d.text(label_x, label_y, f'{progress*2:.1f}π', 
                          fontsize=12, color='red', fontweight='bold', ha='center')
        
        # 显示当前角度值
        if progress > 0.1:
            angle_text = f'Angle: {progress*2:.2f}π rad'
            self.ax_2d.text(0.02, 0.98, angle_text, 
                          transform=self.ax_2d.transAxes, fontsize=10,
                          bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.8))
        
        # 设置2D图属性
        self.ax_2d.set_xlim([-1.4, 1.4])
        self.ax_2d.set_ylim([-0.4, 1.4])
        self.ax_2d.set_aspect('equal')
        self.ax_2d.grid(True, alpha=0.3)
        self.ax_2d.set_title(self.labels['title_2d'], fontweight='bold', fontsize=11)
        self.ax_2d.set_xlabel('X')
        self.ax_2d.set_ylabel('Y')
    
    def animate_math_derivation(self, frame):
        """动画数学推导"""
        self.ax_math.clear()
        self.ax_math.axis('off')
        
        # 推导步骤（英文避免乱码）
        steps = [
            'Geometric Factor Derivation:',
            '',
            '1. Solid angle element:',
            '   dΩ = sin(θ)dθdφ',
            '',
            '2. Projection contribution:',
            '   dF ∝ sin(θ)dΩ',
            '',
            '3. Integration setup:',
            '   ∫ sin(θ)dΩ',
            '',
            '4. Calculate integral:',
            '   = 2π × π/2 = π^2',
            '',
            '5. Geometric factor:',
            '   G = 4π/2π = 2'
        ]
        
        # 动态显示步骤
        step_progress = frame / self.total_frames
        n_visible = int(len(steps) * step_progress)
        
        y_positions = np.linspace(0.95, 0.05, len(steps))
        
        for i in range(min(n_visible, len(steps))):
            step = steps[i]
            y_pos = y_positions[i]
            
            if i == 0:  # 标题
                self.ax_math.text(0.5, y_pos, step, fontsize=12, 
                                transform=self.ax_math.transAxes,
                                ha='center', fontweight='bold', color=self.colors['formula'])
            elif step == '':  # 空行
                continue
            elif 'G = 4π/2π = 2' in step:  # 最终结果
                self.ax_math.text(0.1, y_pos, step, fontsize=12, 
                                transform=self.ax_math.transAxes,
                                color='red', fontweight='bold',
                                bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.9))
            elif step.startswith('   '):  # 缩进的公式
                self.ax_math.text(0.15, y_pos, step, fontsize=10, 
                                transform=self.ax_math.transAxes,
                                color=self.colors['formula'], family='monospace')
            else:  # 普通步骤
                self.ax_math.text(0.05, y_pos, step, fontsize=10, 
                                transform=self.ax_math.transAxes,
                                color=self.colors['text'], fontweight='bold')
        
        self.ax_math.set_title(self.labels['title_math'], fontweight='bold', fontsize=11)
    
    def animate_integral_plot(self, frame):
        """动画积分图"""
        self.ax_integral.clear()
        
        # 积分进度
        integral_progress = min(1.0, frame / (self.total_frames * 0.8))
        
        # θ值
        theta_full = np.linspace(0, self.pi, 300)
        theta_partial = theta_full[:int(len(theta_full) * integral_progress)]
        
        # sin^2(θ)函数
        sin_squared_full = np.sin(theta_full) ** 2
        sin_squared_partial = sin_squared_full[:len(theta_partial)]
        
        # 绘制完整曲线（淡色背景）
        self.ax_integral.plot(theta_full, sin_squared_full, 'lightgray', 
                            linewidth=1.5, alpha=0.4, linestyle='--')
        
        # 绘制当前积分区域
        if len(theta_partial) > 0:
            self.ax_integral.plot(theta_partial, sin_squared_partial, 
                                color=self.colors['formula'], linewidth=3)
            self.ax_integral.fill_between(theta_partial, 0, sin_squared_partial,
                                        alpha=0.4, color=self.colors['formula'])
            
            # 添加积分边界线
            if len(theta_partial) > 1:
                boundary_x = theta_partial[-1]
                boundary_y = sin_squared_partial[-1]
                self.ax_integral.axvline(x=boundary_x, color='red', linestyle=':', alpha=0.8)
                self.ax_integral.plot([boundary_x], [boundary_y], 'ro', markersize=6)
        
        # 设置图属性
        self.ax_integral.set_xlim([0, self.pi])
        self.ax_integral.set_ylim([0, 1.1])
        self.ax_integral.set_xlabel('θ (radians)', fontsize=10)
        self.ax_integral.set_ylabel('sin^2(θ)', fontsize=10)
        self.ax_integral.set_title(self.labels['title_integral'], fontweight='bold', fontsize=11)
        self.ax_integral.grid(True, alpha=0.3)
        
        # 添加π标记
        pi_ticks = [0, self.pi/4, self.pi/2, 3*self.pi/4, self.pi]
        pi_labels = ['0', 'π/4', 'π/2', '3π/4', 'π']
        self.ax_integral.set_xticks(pi_ticks)
        self.ax_integral.set_xticklabels(pi_labels)
        
        # 显示当前积分值
        if integral_progress > 0.1:
            if len(theta_partial) > 1:
                current_value = np.trapz(sin_squared_partial, theta_partial)
                theoretical_value = self.pi / 2
                
                value_text = f'Current: {current_value:.3f}\nTheoretical: π/2 ≈ {theoretical_value:.3f}'
                self.ax_integral.text(0.65, 0.8, value_text, 
                                    transform=self.ax_integral.transAxes, fontsize=9,
                                    bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))
    
    def animate_comparison(self, frame):
        """动画对比图"""
        self.ax_comparison.clear()
        
        # 对比数据
        categories = ['3D Sphere\n4π sr', '2D Projection\n2π rad', 'Factor G\n2']
        values = [4*self.pi, 2*self.pi, 2.0]
        colors = [self.colors['sphere'], self.colors['projection'], self.colors['highlight']]
        
        # 动态显示柱状图
        comparison_progress = min(1.0, frame / (self.total_frames * 0.6))
        
        bars = []
        for i in range(len(categories)):
            if i < len(categories) * comparison_progress:
                # 动画高度
                height = values[i] * min(1.0, (frame - i * 20) / 25)
                height = max(0, height)
                
                bar = self.ax_comparison.bar(categories[i], height, 
                                           color=colors[i], alpha=0.8, width=0.6,
                                           edgecolor='black', linewidth=1)
                bars.append((bar, height, i))
                
                # 添加数值标签
                if height > 0.2:
                    if i == 2:  # 几何因子
                        label = f'{height:.1f}'
                    else:
                        label = f'{height:.2f}'
                    
                    self.ax_comparison.text(bar[0].get_x() + bar[0].get_width()/2, 
                                          height + 0.3, label,
                                          ha='center', va='bottom', 
                                          fontsize=11, fontweight='bold')
        
        # 添加理论值参考线
        if comparison_progress > 0.8:
            for i, val in enumerate(values):
                if i < len(bars):
                    self.ax_comparison.axhline(y=val, color='red', linestyle='--', 
                                             alpha=0.5, linewidth=1)
        
        self.ax_comparison.set_ylabel('Value', fontsize=11)
        self.ax_comparison.set_title(self.labels['title_comparison'], fontweight='bold', fontsize=11)
        self.ax_comparison.set_ylim([0, 15])
        self.ax_comparison.grid(True, alpha=0.3, axis='y')
        
        # 旋转x轴标签以避免重叠
        plt.setp(self.ax_comparison.get_xticklabels(), rotation=0, ha='center')
    
    def animate_final_result(self, frame):
        """动画最终结果"""
        self.ax_result.clear()
        self.ax_result.axis('off')
        
        # 最终结果显示
        if frame > self.total_frames * 0.6:
            # 主要结果
            self.ax_result.text(0.5, 0.8, self.labels['title_result'], fontsize=16, 
                              ha='center', fontweight='bold', 
                              transform=self.ax_result.transAxes,
                              color=self.colors['formula'])
            
            # 几何因子公式
            formula_alpha = min(1.0, (frame - self.total_frames * 0.6) / (self.total_frames * 0.2))
            self.ax_result.text(0.5, 0.6, self.labels['geometric_factor'], fontsize=20, 
                              ha='center', fontweight='bold',
                              transform=self.ax_result.transAxes,
                              color='red', alpha=formula_alpha,
                              bbox=dict(boxstyle="round,pad=0.4", 
                                      facecolor='yellow', alpha=0.9*formula_alpha))
            
            # 理论说明
            if frame > self.total_frames * 0.8:
                self.ax_result.text(0.5, 0.4, self.labels['zhang_theory'], 
                                  fontsize=12, ha='center',
                                  transform=self.ax_result.transAxes,
                                  color=self.colors['text'], fontweight='bold')
                
                self.ax_result.text(0.5, 0.3, self.labels['projection_factor'], 
                                  fontsize=11, ha='center',
                                  transform=self.ax_result.transAxes,
                                  color=self.colors['text'])
        
        # 进度显示
        progress = frame / self.total_frames * 100
        self.ax_result.text(0.5, 0.1, f'Progress: {progress:.0f}%', 
                          fontsize=10, ha='center',
                          transform=self.ax_result.transAxes,
                          color='gray')
        
        # 添加装饰性边框
        if frame > self.total_frames * 0.9:
            from matplotlib.patches import Rectangle
            rect = Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=2, 
                           edgecolor=self.colors['formula'], facecolor='none',
                           transform=self.ax_result.transAxes)
            self.ax_result.add_patch(rect)
    
    def animate_frame(self, frame):
        """主动画函数"""
        self.current_frame = frame
        
        # 执行各个子动画
        self.animate_3d_view(frame)
        self.animate_2d_projection(frame)
        self.animate_math_derivation(frame)
        self.animate_integral_plot(frame)
        self.animate_comparison(frame)
        self.animate_final_result(frame)
        
        # 更新总标题
        progress_percent = (frame / self.total_frames) * 100
        title = f'Zhang Xiangqian Unified Field Theory: Geometric Factor G = 4π/2π = 2 | Progress: {progress_percent:.0f}%'
        self.fig.suptitle(title, fontsize=14, fontweight='bold')
    
    def create_animation(self, interval=100):
        """创建动画"""
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate_frame, frames=self.total_frames,
            interval=interval, blit=False, repeat=True
        )
        
        return anim
    
    def save_animation_gif(self, filename='geometric_factor_animation.gif'):
        """保存动画为GIF"""
        anim = self.create_animation(interval=120)
        print(f"Saving animation as {filename}...")
        try:
            anim.save(filename, writer='pillow', fps=10, dpi=100)
            print(f"Animation successfully saved as: {filename}")
        except Exception as e:
            print(f"Error saving animation: {e}")
        return anim

def create_static_summary():
    """创建静态总结图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Zhang Xiangqian Unified Field Theory: Geometric Factor Derivation Summary', 
                 fontsize=16, fontweight='bold')
    
    # 1. 3D球面示意
    ax1 = axes[0, 0]
    ax1.text(0.5, 0.85, '3D Spherical Symmetric Space', fontsize=14, ha='center', fontweight='bold')
    ax1.text(0.5, 0.7, 'Total Solid Angle = 4π steradians', fontsize=12, ha='center')
    ax1.text(0.5, 0.55, 'Sphere Integration: ∫∫dΩ = 4π', fontsize=11, ha='center')
    ax1.text(0.5, 0.4, 'Isotropic Divergent Field', fontsize=10, ha='center', style='italic')
    ax1.text(0.5, 0.25, 'Space moves at light speed c', fontsize=10, ha='center', color='blue')
    ax1.text(0.5, 0.1, 'in cylindrical spiral pattern', fontsize=10, ha='center', color='blue')
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    ax1.axis('off')
    
    # 2. 2D投影示意
    ax2 = axes[0, 1]
    ax2.text(0.5, 0.85, '2D Planar Projection', fontsize=14, ha='center', fontweight='bold')
    ax2.text(0.5, 0.7, 'Projection Angle = 2π radians', fontsize=12, ha='center')
    ax2.text(0.5, 0.55, 'Semicircle Integration: ∫dθ = π', fontsize=11, ha='center')
    ax2.text(0.5, 0.4, 'Complete Projection = 2π', fontsize=10, ha='center', style='italic')
    ax2.text(0.5, 0.25, 'Interaction occurs on plane', fontsize=10, ha='center', color='blue')
    ax2.text(0.5, 0.1, 'perpendicular to mass line', fontsize=10, ha='center', color='blue')
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])
    ax2.axis('off')
    
    # 3. 数学积分
    ax3 = axes[1, 0]
    theta = np.linspace(0, np.pi, 300)
    sin_squared = np.sin(theta) ** 2
    ax3.plot(theta, sin_squared, 'r-', linewidth=3, label='sin^2(θ)')
    ax3.fill_between(theta, 0, sin_squared, alpha=0.3, color='red')
    ax3.set_xlabel('θ (radians)', fontsize=12)
    ax3.set_ylabel('sin^2(θ)', fontsize=12)
    ax3.set_title('Integration: ∫₀^π sin^2(θ)dθ = π/2', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=11)
    
    # 添加π标记
    pi_ticks = [0, np.pi/2, np.pi]
    pi_labels = ['0', 'π/2', 'π']
    ax3.set_xticks(pi_ticks)
    ax3.set_xticklabels(pi_labels)
    
    # 4. 几何因子结果
    ax4 = axes[1, 1]
    ax4.text(0.5, 0.85, 'Geometric Factor', fontsize=18, ha='center', fontweight='bold')
    ax4.text(0.5, 0.65, 'G = 4π/2π = 2', fontsize=22, ha='center', 
             color='red', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.4", facecolor='yellow', alpha=0.9))
    ax4.text(0.5, 0.45, 'Physical Meaning:', fontsize=14, ha='center', fontweight='bold')
    ax4.text(0.5, 0.35, '3D spherical symmetric field', fontsize=12, ha='center')
    ax4.text(0.5, 0.25, 'projected to 2D plane', fontsize=12, ha='center')
    ax4.text(0.5, 0.15, 'scaling factor', fontsize=12, ha='center')
    ax4.text(0.5, 0.05, 'Zhang Xiangqian Unified Field Theory Core Result', 
             fontsize=11, ha='center', style='italic', color='blue', fontweight='bold')
    ax4.set_xlim([0, 1])
    ax4.set_ylim([0, 1])
    ax4.axis('off')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("=" * 70)
    print("Zhang Xiangqian Unified Field Theory: Geometric Factor Animation")
    print("Compatible Version - No Chinese Character Issues")
    print("=" * 70)
    
    # 创建可视化器
    animator = GeometricFactorAnimator()
    
    print("Creating animation...")
    
    # 创建动画
    anim = animator.create_animation(interval=100)
    
    # 创建静态总结
    summary_fig = create_static_summary()
    
    print("Animation created successfully!")
    print("\nCore Content:")
    print("- 3D Spherical Symmetric Space: 4π steradians")
    print("- 2D Planar Projection: 2π radians")
    print("- Geometric Factor: G = 4π/2π = 2")
    print("- Mathematical Derivation: Solid angle integration")
    print("\nZhang Xiangqian Unified Field Theory Core Mathematical Result")
    
    # 保存静态图
    try:
        summary_fig.savefig('geometric_factor_summary.png', dpi=300, bbox_inches='tight')
        print("\nStatic summary saved as: geometric_factor_summary.png")
    except Exception as e:
        print(f"Error saving image: {e}")
    
    # 显示动画
    plt.show()
    
    return animator, anim

if __name__ == "__main__":
    animator, animation_obj = main()