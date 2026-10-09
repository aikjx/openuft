#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兼容版几何因子动画：3D到2D几何变换可视化
张祥前统一场论：几何因子 G = 4π/2π = 2

专为Python 3.8+设计，避免版本兼容性问题
展示核心数学概念：从球对称3D空间到2D平面投影的几何因子推导

作者：基于张祥前统一场论
创建日期：2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge
import math

# 设置matplotlib参数
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 80
plt.rcParams['animation.html'] = 'html5'

class GeometricFactorVisualizer:
    """几何因子可视化器 - 兼容版本"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 100
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
        
    def setup_figure(self):
        """设置图形和子图"""
        self.fig = plt.figure(figsize=(15, 8))
        self.fig.patch.set_facecolor('white')
        
        # 创建子图网格
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
                
                x = 1.3 * np.sin(phi) * np.cos(theta)
                y = 1.3 * np.sin(phi) * np.sin(theta)
                z = 1.3 * np.cos(phi)
                
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
        self.ax_3d.plot_surface(x, y, z, alpha=0.3, color=self.colors['sphere'])
        self.ax_3d.plot_wireframe(x, y, z, alpha=0.2, color='gray', linewidth=0.5)
        
        # 绘制矢量场
        vectors = self.create_vector_field(6)
        
        # 只显示部分矢量，避免过于密集
        for i, vec in enumerate(vectors[::2]):  # 每隔一个显示
            # 应用旋转变换
            x_rot = vec[3] * np.cos(rotation) - vec[4] * np.sin(rotation)
            y_rot = vec[3] * np.sin(rotation) + vec[4] * np.cos(rotation)
            z_rot = vec[5]
            
            self.ax_3d.quiver(vec[0], vec[1], vec[2], x_rot, y_rot, z_rot,
                             color=self.colors['vectors'], alpha=0.8, 
                             arrow_length_ratio=0.15, linewidth=1.5)
        
        # 绘制投影平面（XY平面）
        if frame > 20:
            plane_size = 1.8
            xx, yy = np.meshgrid([-plane_size, plane_size], [-plane_size, plane_size])
            zz = np.zeros_like(xx)
            self.ax_3d.plot_surface(xx, yy, zz, alpha=0.2, color=self.colors['projection'])
        
        # 设置3D图属性
        self.ax_3d.set_xlim([-2, 2])
        self.ax_3d.set_ylim([-2, 2])
        self.ax_3d.set_zlim([-2, 2])
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.set_title('3D球对称场\n4π 立体角', fontweight='bold', fontsize=11)
        
        # 动态视角
        self.ax_3d.view_init(elev=20, azim=frame * 3)
    
    def animate_2d_projection(self, frame):
        """动画2D投影"""
        self.ax_2d.clear()
        
        # 投影进度（0到1）
        progress = min(1.0, frame / (self.total_frames * 0.8))
        
        # 绘制单位圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['sphere'], linewidth=2)
        self.ax_2d.add_patch(circle)
        
        # 绘制投影区域
        if progress > 0:
            theta_max = self.pi * progress
            theta = np.linspace(0, theta_max, 50)
            x_proj = np.cos(theta)
            y_proj = np.sin(theta)
            
            # 填充投影区域
            self.ax_2d.fill_between(x_proj, 0, y_proj, alpha=0.4, 
                                  color=self.colors['projection'])
            
            # 绘制投影射线
            n_rays = max(1, int(8 * progress))
            for i in range(n_rays):
                if n_rays > 1:
                    angle = theta_max * i / (n_rays - 1)
                else:
                    angle = 0
                
                x_end = np.cos(angle)
                y_end = np.sin(angle)
                
                self.ax_2d.plot([0, x_end], [0, y_end], 
                               color=self.colors['vectors'], linewidth=2, alpha=0.8)
                
                # 添加箭头
                if i % 2 == 0:  # 每隔一个添加箭头
                    self.ax_2d.annotate('', xy=(x_end, y_end), xytext=(0.7*x_end, 0.7*y_end),
                                      arrowprops=dict(arrowstyle='->', 
                                                    color=self.colors['vectors'], lw=1.5))
        
        # 绘制角度弧
        if progress > 0.2:
            angle_deg = progress * 180
            wedge = Wedge((0, 0), 0.25, 0, angle_deg, 
                         facecolor=self.colors['highlight'], alpha=0.7)
            self.ax_2d.add_patch(wedge)
            
            # 角度标签
            self.ax_2d.text(0.35, 0.15, f'{progress*2:.1f}π', 
                          fontsize=11, color='red', fontweight='bold')
        
        # 设置2D图属性
        self.ax_2d.set_xlim([-1.3, 1.3])
        self.ax_2d.set_ylim([-0.3, 1.3])
        self.ax_2d.set_aspect('equal')
        self.ax_2d.grid(True, alpha=0.3)
        self.ax_2d.set_title('2D投影\n2π 弧度', fontweight='bold', fontsize=11)
        self.ax_2d.set_xlabel('X')
        self.ax_2d.set_ylabel('Y')
    
    def animate_math_derivation(self, frame):
        """动画数学推导"""
        self.ax_math.clear()
        self.ax_math.axis('off')
        
        # 推导步骤
        steps = [
            '几何因子推导:',
            '',
            '1. 立体角元素:',
            'dΩ = sin(θ)dθdφ',
            '',
            '2. 投影贡献:',
            'dF ∝ sin(θ)dΩ',
            '',
            '3. 积分:',
            '∫sin(θ)dΩ = π^2',
            '',
            '4. 几何因子:',
            'G = 4π/2π = 2'
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
                                bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.8))
            else:
                self.ax_math.text(0.1, y_pos, step, fontsize=10, 
                                transform=self.ax_math.transAxes,
                                color=self.colors['text'])
    
    def animate_integral_plot(self, frame):
        """动画积分图"""
        self.ax_integral.clear()
        
        # 积分进度
        integral_progress = min(1.0, frame / (self.total_frames * 0.9))
        
        # θ值
        theta_full = np.linspace(0, self.pi, 200)
        theta_partial = theta_full[:int(len(theta_full) * integral_progress)]
        
        # sin^2(θ)函数
        sin_squared_full = np.sin(theta_full) ** 2
        sin_squared_partial = sin_squared_full[:len(theta_partial)]
        
        # 绘制完整曲线（淡色）
        self.ax_integral.plot(theta_full, sin_squared_full, 'lightgray', 
                            linewidth=1, alpha=0.5)
        
        # 绘制当前积分区域
        if len(theta_partial) > 0:
            self.ax_integral.plot(theta_partial, sin_squared_partial, 
                                color=self.colors['formula'], linewidth=2)
            self.ax_integral.fill_between(theta_partial, 0, sin_squared_partial,
                                        alpha=0.3, color=self.colors['formula'])
        
        # 设置图属性
        self.ax_integral.set_xlim([0, self.pi])
        self.ax_integral.set_ylim([0, 1.1])
        self.ax_integral.set_xlabel('θ (弧度)', fontsize=10)
        self.ax_integral.set_ylabel('sin^2(θ)', fontsize=10)
        self.ax_integral.set_title('积分: ∫sin^2(θ)dθ = π/2', fontweight='bold', fontsize=11)
        self.ax_integral.grid(True, alpha=0.3)
        
        # 显示当前积分值
        if integral_progress > 0.1:
            current_value = np.trapz(sin_squared_partial, theta_partial)
            self.ax_integral.text(0.6, 0.8, f'当前值: {current_value:.2f}', 
                                transform=self.ax_integral.transAxes, fontsize=9,
                                bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue'))
    
    def animate_comparison(self, frame):
        """动画对比图"""
        self.ax_comparison.clear()
        
        # 对比数据
        categories = ['3D\n4π', '2D\n2π', 'G\n2']
        values = [4*self.pi, 2*self.pi, 2.0]
        colors = [self.colors['sphere'], self.colors['projection'], self.colors['highlight']]
        
        # 动态显示柱状图
        comparison_progress = min(1.0, frame / (self.total_frames * 0.6))
        
        for i in range(len(categories)):
            if i < len(categories) * comparison_progress:
                height = values[i] * min(1.0, (frame - i * 15) / 20)
                height = max(0, height)
                
                bar = self.ax_comparison.bar(categories[i], height, 
                                           color=colors[i], alpha=0.8, width=0.6)
                
                # 添加数值标签
                if height > 0.1:
                    if i == 2:  # 几何因子
                        label = f'{height:.1f}'
                    else:
                        label = f'{height:.1f}'
                    
                    self.ax_comparison.text(bar[0].get_x() + bar[0].get_width()/2, 
                                          height + 0.2, label,
                                          ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        self.ax_comparison.set_ylabel('数值', fontsize=10)
        self.ax_comparison.set_title('数值对比', fontweight='bold', fontsize=11)
        self.ax_comparison.set_ylim([0, 14])
        self.ax_comparison.grid(True, alpha=0.3, axis='y')
    
    def animate_final_result(self, frame):
        """动画最终结果"""
        self.ax_result.clear()
        self.ax_result.axis('off')
        
        # 最终结果显示
        if frame > self.total_frames * 0.7:
            # 主要结果
            self.ax_result.text(0.5, 0.7, '几何因子', fontsize=16, 
                              ha='center', fontweight='bold', 
                              transform=self.ax_result.transAxes,
                              color=self.colors['formula'])
            
            self.ax_result.text(0.5, 0.5, 'G = 4π/2π = 2', fontsize=18, 
                              ha='center', fontweight='bold',
                              transform=self.ax_result.transAxes,
                              color='red',
                              bbox=dict(boxstyle="round,pad=0.3", 
                                      facecolor='yellow', alpha=0.9))
            
            self.ax_result.text(0.5, 0.3, '张祥前统一场论\n3D→2D投影缩放因子', 
                              fontsize=12, ha='center',
                              transform=self.ax_result.transAxes,
                              color=self.colors['text'])
        
        # 进度显示
        progress = frame / self.total_frames * 100
        self.ax_result.text(0.5, 0.1, f'进度: {progress:.0f}%', 
                          fontsize=10, ha='center',
                          transform=self.ax_result.transAxes,
                          color='gray')
    
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
        self.fig.suptitle(f'张祥前统一场论：几何因子动画推导 G = 4π/2π = 2', 
                         fontsize=14, fontweight='bold')
    
    def create_animation(self, interval=120):
        """创建动画"""
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate_frame, frames=self.total_frames,
            interval=interval, blit=False, repeat=True
        )
        
        return anim
    
    def save_animation_gif(self, filename='几何因子动画.gif'):
        """保存动画为GIF"""
        anim = self.create_animation(interval=150)
        print(f"正在保存动画为 {filename}...")
        try:
            anim.save(filename, writer='pillow', fps=8, dpi=80)
            print(f"动画已成功保存为: {filename}")
        except Exception as e:
            print(f"保存动画时出错: {e}")
        return anim

def create_static_summary():
    """创建静态总结图"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('张祥前统一场论：几何因子推导总结', fontsize=16, fontweight='bold')
    
    # 1. 3D球面示意
    ax1 = axes[0, 0]
    ax1.text(0.5, 0.8, '3D球对称空间', fontsize=14, ha='center', fontweight='bold')
    ax1.text(0.5, 0.6, '总立体角 = 4π 立体弧度', fontsize=12, ha='center')
    ax1.text(0.5, 0.4, '球面积分：∫∫dΩ = 4π', fontsize=11, ha='center')
    ax1.text(0.5, 0.2, '各向同性发散场', fontsize=10, ha='center', style='italic')
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    ax1.axis('off')
    
    # 2. 2D投影示意
    ax2 = axes[0, 1]
    ax2.text(0.5, 0.8, '2D平面投影', fontsize=14, ha='center', fontweight='bold')
    ax2.text(0.5, 0.6, '投影角度 = 2π 弧度', fontsize=12, ha='center')
    ax2.text(0.5, 0.4, '半圆积分：∫dθ = π', fontsize=11, ha='center')
    ax2.text(0.5, 0.2, '完整投影 = 2π', fontsize=10, ha='center', style='italic')
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])
    ax2.axis('off')
    
    # 3. 数学积分
    ax3 = axes[1, 0]
    theta = np.linspace(0, np.pi, 200)
    sin_squared = np.sin(theta) ** 2
    ax3.plot(theta, sin_squared, 'r-', linewidth=2, label='sin^2(θ)')
    ax3.fill_between(theta, 0, sin_squared, alpha=0.3, color='red')
    ax3.set_xlabel('θ (弧度)')
    ax3.set_ylabel('sin^2(θ)')
    ax3.set_title('积分：∫₀^π sin^2(θ)dθ = π/2')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # 4. 几何因子结果
    ax4 = axes[1, 1]
    ax4.text(0.5, 0.8, '几何因子', fontsize=16, ha='center', fontweight='bold')
    ax4.text(0.5, 0.6, 'G = 4π/2π = 2', fontsize=18, ha='center', 
             color='red', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.9))
    ax4.text(0.5, 0.4, '物理意义：', fontsize=12, ha='center', fontweight='bold')
    ax4.text(0.5, 0.3, '三维球对称场投影到', fontsize=11, ha='center')
    ax4.text(0.5, 0.2, '二维平面的缩放因子', fontsize=11, ha='center')
    ax4.text(0.5, 0.05, '张祥前统一场论核心结果', fontsize=10, ha='center', 
             style='italic', color='blue')
    ax4.set_xlim([0, 1])
    ax4.set_ylim([0, 1])
    ax4.axis('off')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("=" * 60)
    print("张祥前统一场论：几何因子动画可视化")
    print("兼容版本 - 适用于Python 3.8+")
    print("=" * 60)
    
    # 创建可视化器
    visualizer = GeometricFactorVisualizer()
    
    print("正在创建动画...")
    
    # 创建动画
    anim = visualizer.create_animation(interval=120)
    
    # 创建静态总结
    summary_fig = create_static_summary()
    
    print("动画创建完成！")
    print("\n核心内容：")
    print("- 3D球对称空间：4π立体角")
    print("- 2D平面投影：2π弧度")
    print("- 几何因子：G = 4π/2π = 2")
    print("- 数学推导：立体角积分")
    print("\n张祥前统一场论的核心数学结果")
    
    # 保存静态图
    try:
        summary_fig.savefig('几何因子推导总结.png', dpi=300, bbox_inches='tight')
        print("\n静态总结图已保存为: 几何因子推导总结.png")
    except Exception as e:
        print(f"保存图像时出错: {e}")
    
    # 显示动画
    plt.show()
    
    return visualizer, anim

if __name__ == "__main__":
    visualizer, animation_obj = main()