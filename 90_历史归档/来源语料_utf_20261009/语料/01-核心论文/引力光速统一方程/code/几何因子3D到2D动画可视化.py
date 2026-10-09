#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D到2D几何因子动画可视化
张祥前统一场论：从球对称三维空间到二维投影的几何因子 G = 4π/2π = 2

动画展示：
1. 三维球对称空间发散场 (4π立体角)
2. 投影过程的动态演示
3. 二维平面上的投影结果 (2π角度)
4. 几何因子的数学推导动画
5. 立体角积分的可视化

作者：基于张祥前统一场论
创建日期：2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge, FancyBboxPatch
import matplotlib.patches as patches
import time

# 设置中文字体和高质量显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

class GeometricFactorAnimator:
    """
    几何因子动画可视化类
    展示从3D球对称到2D投影的完整过程
    """
    
    def __init__(self):
        self.fig = None
        self.axes = []
        self.frame_count = 0
        self.total_frames = 200
        
        # 颜色方案
        self.colors = {
            'sphere': '#FF6B6B',
            'projection': '#4ECDC4',
            'vectors': '#45B7D1',
            'highlight': '#FFD93D',
            'text': '#2C3E50',
            'formula': '#8E44AD',
            'integration': '#E74C3C',
            'background': '#F8F9FA'
        }
        
        # 动画参数
        self.rotation_angle = 0
        self.projection_progress = 0
        self.integration_progress = 0
        
    def setup_figure(self):
        """设置图形布局"""
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.patch.set_facecolor(self.colors['background'])
        
        # 创建子图
        gs = self.fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 主要的3D可视化
        self.ax_3d = self.fig.add_subplot(gs[:2, :2], projection='3d')
        
        # 2D投影结果
        self.ax_2d = self.fig.add_subplot(gs[:2, 2])
        
        # 数学公式动画
        self.ax_formula = self.fig.add_subplot(gs[:2, 3])
        
        # 立体角积分可视化
        self.ax_integration = self.fig.add_subplot(gs[2, :2])
        
        # 几何因子对比
        self.ax_comparison = self.fig.add_subplot(gs[2, 2])
        
        # 物理意义说明
        self.ax_meaning = self.fig.add_subplot(gs[2, 3])
        
        self.axes = [self.ax_3d, self.ax_2d, self.ax_formula, 
                    self.ax_integration, self.ax_comparison, self.ax_meaning]
        
        return self.fig
    
    def create_sphere_data(self, resolution=30):
        """创建球面数据"""
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        return x, y, z, u, v
    
    def create_vector_field(self, n_vectors=12, radius_scale=1.5):
        """创建发散矢量场"""
        vectors = []
        
        # 均匀分布在球面上的矢量
        for i in range(n_vectors):
            for j in range(n_vectors//2):
                theta = 2 * np.pi * i / n_vectors
                phi = np.pi * j / (n_vectors//2)
                
                # 球面坐标到直角坐标
                x = radius_scale * np.sin(phi) * np.cos(theta)
                y = radius_scale * np.sin(phi) * np.sin(theta)
                z = radius_scale * np.cos(phi)
                
                vectors.append([0, 0, 0, x, y, z])
        
        return np.array(vectors)
    
    def animate_3d_sphere(self, frame):
        """动画3D球面和矢量场"""
        self.ax_3d.clear()
        
        # 旋转角度
        self.rotation_angle = frame * 2 * np.pi / self.total_frames
        
        # 创建球面
        x, y, z, u, v = self.create_sphere_data()
        
        # 绘制球面（半透明）
        self.ax_3d.plot_surface(x, y, z, alpha=0.3, color=self.colors['sphere'])
        
        # 绘制球面网格线
        self.ax_3d.plot_wireframe(x, y, z, alpha=0.2, color='gray', linewidth=0.5)
        
        # 创建发散矢量场
        vectors = self.create_vector_field()
        
        # 动态显示矢量（逐渐出现）
        n_visible = int((frame / self.total_frames) * len(vectors))
        
        for i in range(min(n_visible, len(vectors))):
            vec = vectors[i]
            # 添加旋转效果
            x_rot = vec[3] * np.cos(self.rotation_angle) - vec[4] * np.sin(self.rotation_angle)
            y_rot = vec[3] * np.sin(self.rotation_angle) + vec[4] * np.cos(self.rotation_angle)
            z_rot = vec[5]
            
            self.ax_3d.quiver(vec[0], vec[1], vec[2], x_rot, y_rot, z_rot,
                             color=self.colors['vectors'], alpha=0.8, 
                             arrow_length_ratio=0.1, linewidth=2)
        
        # 突出显示投影平面
        if frame > self.total_frames // 4:
            # 绘制XY平面（投影平面）
            xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 10), 
                               np.linspace(-1.5, 1.5, 10))
            zz = np.zeros_like(xx)
            self.ax_3d.plot_surface(xx, yy, zz, alpha=0.2, 
                                  color=self.colors['projection'])
        
        # 添加标题和标签
        self.ax_3d.set_title(f'3D球对称空间发散场\n总立体角 = 4π 立体弧度\n帧: {frame}/{self.total_frames}', 
                           fontsize=12, fontweight='bold')
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        
        # 设置视角
        self.ax_3d.view_init(elev=20, azim=frame * 2)
        
        # 设置坐标轴范围
        self.ax_3d.set_xlim([-2, 2])
        self.ax_3d.set_ylim([-2, 2])
        self.ax_3d.set_zlim([-2, 2])
    
    def animate_2d_projection(self, frame):
        """动画2D投影过程"""
        self.ax_2d.clear()
        
        # 投影进度
        self.projection_progress = min(1.0, frame / (self.total_frames * 0.6))
        
        # 绘制单位圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['sphere'], 
                       linewidth=3, linestyle='-')
        self.ax_2d.add_patch(circle)
        
        # 绘制投影区域（上半圆，逐渐填充）
        if self.projection_progress > 0:
            theta_max = np.pi * self.projection_progress
            theta = np.linspace(0, theta_max, 100)
            x_proj = np.cos(theta)
            y_proj = np.sin(theta)
            
            # 填充投影区域
            self.ax_2d.fill_between(x_proj, 0, y_proj, alpha=0.4, 
                                  color=self.colors['projection'])
            
            # 绘制投影矢量（动态出现）
            n_rays = int(12 * self.projection_progress)
            for i in range(n_rays + 1):
                if theta_max > 0:
                    angle = theta_max * i / max(1, n_rays)
                    x_end = np.cos(angle)
                    y_end = np.sin(angle)
                    
                    # 矢量颜色根据角度变化
                    color_intensity = 1 - (angle / np.pi) * 0.5
                    self.ax_2d.arrow(0, 0, x_end, y_end, 
                                   head_width=0.05, head_length=0.05,
                                   fc=self.colors['vectors'], 
                                   ec=self.colors['vectors'],
                                   alpha=color_intensity, linewidth=2)
        
        # 添加角度标记
        if self.projection_progress > 0.5:
            # 绘制角度弧
            angle_arc = Wedge((0, 0), 0.3, 0, 180 * self.projection_progress, 
                            facecolor=self.colors['highlight'], alpha=0.6)
            self.ax_2d.add_patch(angle_arc)
            
            # 角度标签
            mid_angle = np.pi * self.projection_progress / 2
            label_x = 0.4 * np.cos(mid_angle)
            label_y = 0.4 * np.sin(mid_angle)
            self.ax_2d.annotate(f'{self.projection_progress * 2:.1f}π', 
                              xy=(label_x, label_y), fontsize=12, 
                              color='red', fontweight='bold', ha='center')
        
        # 设置坐标轴
        self.ax_2d.set_xlim([-1.5, 1.5])
        self.ax_2d.set_ylim([-0.5, 1.5])
        self.ax_2d.set_aspect('equal')
        self.ax_2d.grid(True, alpha=0.3)
        self.ax_2d.set_title(f'2D投影过程\n投影角度 = {self.projection_progress * 2:.1f}π 弧度', 
                           fontsize=12, fontweight='bold')
    
    def animate_formula_derivation(self, frame):
        """动画数学公式推导"""
        self.ax_formula.clear()
        self.ax_formula.axis('off')
        
        # 公式推导步骤
        formulas = [
            r'几何因子推导',
            r'',
            r'1. 立体角元素:',
            r'$d\Omega = \sin(\theta) d\theta d\phi$',
            r'',
            r'2. 投影贡献:',
            r'$dF \propto \sin(\theta) d\Omega$',
            r'',
            r'3. 积分设置:',
            r'$\int \sin(\theta) d\Omega$',
            r'',
            r'4. 展开积分:',
            r'$\int_0^{2\pi} d\phi \int_0^{\pi} \sin^2(\theta) d\theta$',
            r'',
            r'5. 计算结果:',
            r'$= 2\pi \times \frac{\pi}{2} = \pi^2$',
            r'',
            r'6. 几何因子:',
            r'$G = \frac{4\pi}{2\pi} = 2$'
        ]
        
        # 动态显示公式
        formula_progress = frame / self.total_frames
        n_visible = int(len(formulas) * formula_progress)
        
        y_positions = np.linspace(0.95, 0.05, len(formulas))
        
        for i in range(min(n_visible, len(formulas))):
            formula = formulas[i]
            y_pos = y_positions[i]
            
            if i == 0:  # 标题
                self.ax_formula.text(0.5, y_pos, formula, fontsize=14, 
                                   transform=self.ax_formula.transAxes,
                                   ha='center', fontweight='bold', 
                                   color=self.colors['formula'])
            elif formula == '':  # 空行
                continue
            elif formula.startswith(r'$G ='):  # 最终结果
                # 添加高亮效果
                bbox_props = dict(boxstyle="round,pad=0.3", 
                                facecolor=self.colors['highlight'], alpha=0.7)
                self.ax_formula.text(0.05, y_pos, formula, fontsize=13, 
                                   transform=self.ax_formula.transAxes,
                                   color='red', fontweight='bold', bbox=bbox_props)
            elif '$' in formula:  # 数学公式
                self.ax_formula.text(0.1, y_pos, formula, fontsize=11, 
                                   transform=self.ax_formula.transAxes,
                                   color=self.colors['formula'])
            else:  # 普通文本
                self.ax_formula.text(0.05, y_pos, formula, fontsize=11, 
                                   transform=self.ax_formula.transAxes,
                                   color=self.colors['text'], fontweight='bold')
        
        # 添加边框
        if n_visible > len(formulas) * 0.8:
            bbox = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, 
                                boxstyle="round,pad=0.02", 
                                facecolor='lightblue', alpha=0.1,
                                edgecolor='blue', linewidth=2)
            self.ax_formula.add_patch(bbox)
    
    def animate_integration_visualization(self, frame):
        """动画立体角积分可视化"""
        self.ax_integration.clear()
        
        # 积分进度
        self.integration_progress = min(1.0, frame / (self.total_frames * 0.8))
        
        # 绘制积分区域
        theta_values = np.linspace(0, np.pi, 100)
        phi_values = np.linspace(0, 2 * np.pi, 100)
        
        # sin^2(θ) 函数
        sin_squared = np.sin(theta_values) ** 2
        
        # 动态显示积分区域
        theta_max_idx = int(len(theta_values) * self.integration_progress)
        
        if theta_max_idx > 0:
            # 绘制 sin^2(θ) 曲线
            self.ax_integration.plot(theta_values[:theta_max_idx], 
                                   sin_squared[:theta_max_idx],
                                   color=self.colors['integration'], 
                                   linewidth=3, label=r'$\sin^2(\theta)$')
            
            # 填充积分区域
            self.ax_integration.fill_between(theta_values[:theta_max_idx], 0, 
                                           sin_squared[:theta_max_idx],
                                           alpha=0.3, color=self.colors['integration'])
        
        # 添加积分标记
        if self.integration_progress > 0.5:
            # 当前积分值
            current_integral = np.trapz(sin_squared[:theta_max_idx], 
                                      theta_values[:theta_max_idx])
            
            self.ax_integration.text(0.7, 0.8, 
                                   f'当前积分值: {current_integral:.3f}',
                                   transform=self.ax_integration.transAxes,
                                   fontsize=12, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", 
                                           facecolor='yellow', alpha=0.7))
        
        # 设置坐标轴
        self.ax_integration.set_xlim([0, np.pi])
        self.ax_integration.set_ylim([0, 1.2])
        self.ax_integration.set_xlabel(r'$\theta$ (弧度)', fontsize=12)
        self.ax_integration.set_ylabel(r'$\sin^2(\theta)$', fontsize=12)
        self.ax_integration.set_title(r'立体角积分: $\int_0^{\pi} \sin^2(\theta) d\theta = \frac{\pi}{2}$', 
                                    fontsize=12, fontweight='bold')
        self.ax_integration.grid(True, alpha=0.3)
        self.ax_integration.legend()
        
        # 添加积分公式
        if self.integration_progress > 0.8:
            self.ax_integration.text(0.05, 0.9, 
                                   r'完整积分: $2\pi \times \frac{\pi}{2} = \pi^2$',
                                   transform=self.ax_integration.transAxes,
                                   fontsize=11, color='red', fontweight='bold')
    
    def animate_comparison(self, frame):
        """动画几何因子对比"""
        self.ax_comparison.clear()
        
        # 对比数据
        categories = ['3D球面\n4π sr', '2D投影\n2π rad', '几何因子\nG = 2']
        values = [4*np.pi, 2*np.pi, 2.0]
        colors = [self.colors['sphere'], self.colors['projection'], self.colors['highlight']]
        
        # 动态显示柱状图
        comparison_progress = min(1.0, frame / (self.total_frames * 0.7))
        visible_bars = int(len(categories) * comparison_progress)
        
        if visible_bars > 0:
            # 动态高度
            animated_values = []
            for i in range(visible_bars):
                if i < len(values):
                    animated_height = values[i] * min(1.0, (frame - i * 20) / 30)
                    animated_values.append(max(0, animated_height))
            
            bars = self.ax_comparison.bar(categories[:visible_bars], animated_values, 
                                        color=colors[:visible_bars], alpha=0.8,
                                        edgecolor='black', linewidth=2)
            
            # 添加数值标签
            for i, (bar, value) in enumerate(zip(bars, animated_values)):
                if value > 0:
                    height = bar.get_height()
                    if i == 2:  # 几何因子
                        label = f'{value:.1f}'
                    else:
                        label = f'{value:.2f}\n({value/np.pi:.1f}π)'
                    
                    self.ax_comparison.text(bar.get_x() + bar.get_width()/2., 
                                          height + 0.2, label,
                                          ha='center', va='bottom', 
                                          fontsize=10, fontweight='bold')
        
        self.ax_comparison.set_ylabel('数值', fontsize=12)
        self.ax_comparison.set_title('几何因子数值对比', fontweight='bold')
        self.ax_comparison.grid(True, alpha=0.3, axis='y')
        self.ax_comparison.set_ylim([0, 15])
    
    def animate_physical_meaning(self, frame):
        """动画物理意义说明"""
        self.ax_meaning.clear()
        self.ax_meaning.axis('off')
        
        meanings = [
            '物理意义:',
            '',
            '• 3D各向同性场',
            '• 球对称空间发散',
            '• 2D平面投影',
            '• 几何缩放因子',
            '',
            '张祥前统一场论:',
            '• 空间光速发散运动',
            '• 质量-空间位移关联',
            '• 引力-电磁统一',
            '',
            '结论: G = 2'
        ]
        
        # 动态显示文本
        meaning_progress = min(1.0, frame / (self.total_frames * 0.9))
        n_visible = int(len(meanings) * meaning_progress)
        
        y_positions = np.linspace(0.95, 0.05, len(meanings))
        
        for i in range(min(n_visible, len(meanings))):
            meaning = meanings[i]
            y_pos = y_positions[i]
            
            if meaning.endswith(':'):  # 标题
                self.ax_meaning.text(0.05, y_pos, meaning, fontsize=12, 
                                   transform=self.ax_meaning.transAxes,
                                   fontweight='bold', color=self.colors['formula'])
            elif meaning == '':  # 空行
                continue
            elif meaning.startswith('结论'):  # 结论
                bbox_props = dict(boxstyle="round,pad=0.3", 
                                facecolor=self.colors['highlight'], alpha=0.8)
                self.ax_meaning.text(0.05, y_pos, meaning, fontsize=13, 
                                   transform=self.ax_meaning.transAxes,
                                   color='red', fontweight='bold', bbox=bbox_props)
            else:  # 普通文本
                self.ax_meaning.text(0.05, y_pos, meaning, fontsize=10, 
                                   transform=self.ax_meaning.transAxes,
                                   color=self.colors['text'])
    
    def animate_frame(self, frame):
        """主动画函数"""
        self.frame_count = frame
        
        # 清除所有子图
        for ax in self.axes:
            if hasattr(ax, 'clear'):
                ax.clear()
        
        # 执行各个子动画
        self.animate_3d_sphere(frame)
        self.animate_2d_projection(frame)
        self.animate_formula_derivation(frame)
        self.animate_integration_visualization(frame)
        self.animate_comparison(frame)
        self.animate_physical_meaning(frame)
        
        # 更新总标题
        progress_percent = (frame / self.total_frames) * 100
        self.fig.suptitle(f'张祥前统一场论：3D→2D几何因子动画推导 (G = 4π/2π = 2)\n'
                         f'进度: {progress_percent:.1f}% | 帧: {frame}/{self.total_frames}', 
                         fontsize=16, fontweight='bold', y=0.95)
        
        return self.axes
    
    def create_animation(self, interval=100, save_gif=False):
        """创建完整动画"""
        # 设置图形
        self.setup_figure()
        
        # 创建动画
        anim = animation.FuncAnimation(
            self.fig, self.animate_frame, frames=self.total_frames,
            interval=interval, blit=False, repeat=True
        )
        
        # 保存为GIF（可选）
        if save_gif:
            print("正在保存动画为GIF文件...")
            anim.save('几何因子3D到2D动画.gif', writer='pillow', fps=10, dpi=100)
            print("动画已保存为: 几何因子3D到2D动画.gif")
        
        return anim
    
    def create_static_summary(self):
        """创建静态总结图"""
        fig_summary = plt.figure(figsize=(16, 10))
        fig_summary.suptitle('张祥前统一场论：几何因子推导总结 (G = 2)', 
                           fontsize=18, fontweight='bold')
        
        # 创建网格布局
        gs = fig_summary.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. 3D球面
        ax1 = fig_summary.add_subplot(gs[0, 0], projection='3d')
        x, y, z, _, _ = self.create_sphere_data()
        ax1.plot_surface(x, y, z, alpha=0.3, color=self.colors['sphere'])
        vectors = self.create_vector_field(8)
        for vec in vectors[::3]:  # 显示部分矢量
            ax1.quiver(vec[0], vec[1], vec[2], vec[3], vec[4], vec[5],
                      color=self.colors['vectors'], alpha=0.8, arrow_length_ratio=0.1)
        ax1.set_title('3D球对称场\n4π 立体弧度', fontweight='bold')
        
        # 2. 2D投影
        ax2 = fig_summary.add_subplot(gs[0, 1])
        circle = Circle((0, 0), 1, fill=False, color=self.colors['sphere'], linewidth=3)
        ax2.add_patch(circle)
        theta = np.linspace(0, np.pi, 100)
        x_proj = np.cos(theta)
        y_proj = np.sin(theta)
        ax2.fill_between(x_proj, 0, y_proj, alpha=0.4, color=self.colors['projection'])
        for i in range(9):
            angle = np.pi * i / 8
            x_end, y_end = np.cos(angle), np.sin(angle)
            ax2.arrow(0, 0, x_end, y_end, head_width=0.05, head_length=0.05,
                     fc=self.colors['vectors'], ec=self.colors['vectors'])
        ax2.set_xlim([-1.2, 1.2])
        ax2.set_ylim([-0.2, 1.2])
        ax2.set_aspect('equal')
        ax2.set_title('2D投影\n2π 弧度', fontweight='bold')
        
        # 3. 几何因子
        ax3 = fig_summary.add_subplot(gs[0, 2])
        ax3.axis('off')
        ax3.text(0.5, 0.7, r'几何因子', fontsize=16, ha='center', fontweight='bold',
                transform=ax3.transAxes, color=self.colors['formula'])
        ax3.text(0.5, 0.5, r'$G = \frac{4\pi}{2\pi} = 2$', fontsize=20, ha='center',
                transform=ax3.transAxes, color='red', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
        ax3.text(0.5, 0.3, '三维→二维\n投影缩放因子', fontsize=12, ha='center',
                transform=ax3.transAxes, color=self.colors['text'])
        
        # 4. 积分过程
        ax4 = fig_summary.add_subplot(gs[1, :])
        theta_vals = np.linspace(0, np.pi, 1000)
        sin_squared = np.sin(theta_vals) ** 2
        ax4.plot(theta_vals, sin_squared, color=self.colors['integration'], 
                linewidth=3, label=r'$\sin^2(\theta)$')
        ax4.fill_between(theta_vals, 0, sin_squared, alpha=0.3, 
                        color=self.colors['integration'])
        ax4.set_xlabel(r'$\theta$ (弧度)', fontsize=12)
        ax4.set_ylabel(r'$\sin^2(\theta)$', fontsize=12)
        ax4.set_title(r'立体角积分: $\int_0^{2\pi} d\phi \int_0^{\pi} \sin^2(\theta) d\theta = 2\pi \times \frac{\pi}{2} = \pi^2$', 
                     fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        # 添加关键公式
        ax4.text(0.7, 0.8, r'$\int_0^{\pi} \sin^2(\theta) d\theta = \frac{\pi}{2}$',
                transform=ax4.transAxes, fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        return fig_summary

def main():
    """主函数：创建和运行动画"""
    print("=" * 60)
    print("张祥前统一场论：3D→2D几何因子动画可视化")
    print("=" * 60)
    print("正在创建动画...")
    
    # 创建动画器
    animator = GeometricFactorAnimator()
    
    # 创建动画
    anim = animator.create_animation(interval=50, save_gif=False)
    
    # 创建静态总结图
    summary_fig = animator.create_static_summary()
    
    print("动画创建完成！")
    print("- 动画窗口将显示完整的推导过程")
    print("- 静态总结图展示关键结果")
    print("- 几何因子 G = 4π/2π = 2")
    print("=" * 60)
    
    # 保存静态图
    summary_fig.savefig('几何因子推导总结.png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    print("静态总结图已保存为: 几何因子推导总结.png")
    
    # 显示动画
    plt.show()
    
    return animator, anim

if __name__ == "__main__":
    animator, animation_obj = main()