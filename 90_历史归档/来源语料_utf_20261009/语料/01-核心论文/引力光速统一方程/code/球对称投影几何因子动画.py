#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
几何因子底层原理动画演示
Geometric Factor Fundamental Principle Animation

直观展示球对称场与平面投影的几何关系
Author: Physics Visualization
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as patches

# 设置中文字体和参数
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 100

class GeometricFactorAnimator:
    """几何因子原理动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 200
        
        # 颜色配置
        self.colors = {
            'sphere': '#FF6B6B',
            'plane': '#4ECDC4', 
            'vectors': '#45B7D1',
            'projection': '#96CEB4',
            'highlight': '#FFD93D',
            'text': '#2C3E50',
            'formula': '#8E44AD'
        }
        
    def setup_figure(self):
        """设置图形布局"""
        self.fig = plt.figure(figsize=(20, 14))
        self.fig.patch.set_facecolor('white')
        
        # 主标题
        self.fig.suptitle('几何因子的底层原理：球面积与圆周长的几何关系', 
                         fontsize=20, fontweight='bold', color=self.colors['text'])
        
        # 创建子图 (2x3 布局)
        self.ax_3d = self.fig.add_subplot(231, projection='3d')
        self.ax_projection = self.fig.add_subplot(232)
        self.ax_calculation = self.fig.add_subplot(233)
        self.ax_formula = self.fig.add_subplot(234)
        self.ax_comparison = self.fig.add_subplot(235)
        self.ax_conclusion = self.fig.add_subplot(236)
        
        return self.fig
    
    def draw_sphere_and_circle(self, frame):
        """绘制球面和圆的对比"""
        self.ax_3d.clear()
        
        # 创建球面
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # 绘制球面
        self.ax_3d.plot_surface(x, y, z, alpha=0.6, color=self.colors['sphere'])
        
        # 绘制赤道圆
        theta = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(theta)
        circle_y = np.sin(theta)
        circle_z = np.zeros_like(theta)
        self.ax_3d.plot(circle_x, circle_y, circle_z, 
                       color=self.colors['highlight'], linewidth=4, label='赤道圆')
        
        # 动态旋转视角
        rotation = frame * 2 * np.pi / self.total_frames
        self.ax_3d.view_init(elev=20, azim=rotation * 180 / np.pi)
        
        self.ax_3d.set_title('三维球面 vs 二维圆', fontsize=14, fontweight='bold')
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.legend()
        
    def draw_area_comparison(self, frame):
        """绘制面积对比"""
        self.ax_projection.clear()
        
        # 绘制圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['plane'], linewidth=3)
        self.ax_projection.add_patch(circle)
        
        # 动态填充显示面积
        progress = (frame % 100) / 100.0
        if progress < 0.5:
            # 显示圆周长
            theta = np.linspace(0, 2*np.pi*progress*2, int(100*progress*2))
            x_circle = np.cos(theta)
            y_circle = np.sin(theta)
            self.ax_projection.plot(x_circle, y_circle, color=self.colors['highlight'], 
                                  linewidth=5, label=f'圆周长: 2πr')
        else:
            # 显示圆面积
            theta = np.linspace(0, 2*np.pi, 100)
            x_circle = np.cos(theta)
            y_circle = np.sin(theta)
            self.ax_projection.fill(x_circle, y_circle, alpha=0.3, 
                                  color=self.colors['plane'], label='圆面积: πr^2')
        
        self.ax_projection.set_xlim(-1.5, 1.5)
        self.ax_projection.set_ylim(-1.5, 1.5)
        self.ax_projection.set_aspect('equal')
        self.ax_projection.set_title('二维圆的周长与面积', fontsize=14, fontweight='bold')
        self.ax_projection.legend()
        self.ax_projection.grid(True, alpha=0.3)
        
    def draw_calculation_steps(self, frame):
        """绘制计算步骤"""
        self.ax_calculation.clear()
        self.ax_calculation.axis('off')
        
        # 计算步骤文本
        steps = [
            "步骤1: 球面积 = 4πr^2",
            "步骤2: 圆周长 = 2πr", 
            "步骤3: 比值 = 4πr^2 / 2πr = 2r",
            "步骤4: 单位半径时 r=1",
            "步骤5: 几何因子 = 2×1 = 2"
        ]
        
        # 动态显示步骤
        progress = frame / self.total_frames
        n_steps = min(len(steps), int(progress * len(steps) * 2))
        
        y_positions = np.linspace(0.9, 0.1, len(steps))
        
        for i in range(n_steps):
            color = self.colors['highlight'] if i == n_steps-1 else self.colors['text']
            weight = 'bold' if i == n_steps-1 else 'normal'
            self.ax_calculation.text(0.05, y_positions[i], steps[i], 
                                   fontsize=14, color=color, weight=weight,
                                   transform=self.ax_calculation.transAxes)
        
        self.ax_calculation.set_title('几何因子计算过程', fontsize=14, fontweight='bold')
        
    def draw_formula_derivation(self, frame):
        """绘制公式推导"""
        self.ax_formula.clear()
        self.ax_formula.axis('off')
        
        # 公式推导
        formulas = [
            r"球面积: $S_{球} = 4\pi r^2$",
            r"圆周长: $C_{圆} = 2\pi r$",
            r"几何比值: $\frac{S_{球}}{C_{圆}} = \frac{4\pi r^2}{2\pi r} = 2r$",
            r"单位半径: $r = 1$",
            r"几何因子: $G_f = 2 \times 1 = 2$"
        ]
        
        progress = frame / self.total_frames
        n_formulas = min(len(formulas), int(progress * len(formulas) * 1.5) + 1)
        
        y_positions = np.linspace(0.85, 0.15, len(formulas))
        
        for i in range(n_formulas):
            color = self.colors['formula'] if i == n_formulas-1 else self.colors['text']
            size = 16 if i == n_formulas-1 else 14
            self.ax_formula.text(0.05, y_positions[i], formulas[i], 
                               fontsize=size, color=color,
                               transform=self.ax_formula.transAxes)
        
        self.ax_formula.set_title('数学公式推导', fontsize=14, fontweight='bold')
        
    def draw_dimension_comparison(self, frame):
        """绘制维度对比"""
        self.ax_comparison.clear()
        
        # 创建对比图表
        categories = ['球面积\n(3D→2D)', '圆周长\n(1D)', '几何因子\n(比值)']
        values = [4*np.pi, 2*np.pi, 2]
        colors_bar = [self.colors['sphere'], self.colors['plane'], self.colors['highlight']]
        
        # 动态显示柱状图
        progress = (frame % 50) / 50.0
        display_values = [v * progress for v in values]
        
        bars = self.ax_comparison.bar(categories, display_values, color=colors_bar, alpha=0.7)
        
        # 添加数值标签
        for bar, val in zip(bars, values):
            height = bar.get_height()
            if height > 0.1:
                self.ax_comparison.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                      f'{val:.2f}', ha='center', va='bottom', fontsize=12)
        
        self.ax_comparison.set_ylabel('数值大小')
        self.ax_comparison.set_title('维度与几何量对比', fontsize=14, fontweight='bold')
        self.ax_comparison.grid(True, alpha=0.3)
        
    def draw_conclusion(self, frame):
        """绘制结论"""
        self.ax_conclusion.clear()
        self.ax_conclusion.axis('off')
        
        # 结论文本
        conclusions = [
            "核心原理:",
            "• 球面积代表三维空间的总'容量'",
            "• 圆周长代表二维边界的'长度'", 
            "• 几何因子2反映了维度差异",
            "",
            "物理意义:",
            "• 从3D球面到2D平面的几何映射",
            "• 体现了空间维度约化的数学本质",
            "• 连接了几何形状与物理相互作用",
            "",
            "数学验证:",
            "几何因子 = 4πr^2 / (2πr) = 2r = 2 (当r=1)"
        ]
        
        progress = frame / self.total_frames
        n_lines = min(len(conclusions), int(progress * len(conclusions) * 1.2))
        
        y_start = 0.95
        line_height = 0.07
        
        for i in range(n_lines):
            line = conclusions[i]
            y_pos = y_start - i * line_height
            
            if line.startswith("核心原理:") or line.startswith("物理意义:") or line.startswith("数学验证:"):
                color = self.colors['formula']
                weight = 'bold'
                size = 14
            elif line.startswith("•"):
                color = self.colors['text']
                weight = 'normal'
                size = 12
            else:
                color = self.colors['text']
                weight = 'normal'
                size = 12
                
            self.ax_conclusion.text(0.05, y_pos, line, 
                                  fontsize=size, color=color, weight=weight,
                                  transform=self.ax_conclusion.transAxes)
        
        self.ax_conclusion.set_title('几何因子的物理本质', fontsize=14, fontweight='bold')
    
    def animate(self, frame):
        """主动画函数"""
        self.draw_sphere_and_circle(frame)
        self.draw_area_comparison(frame)
        self.draw_calculation_steps(frame)
        self.draw_formula_derivation(frame)
        self.draw_dimension_comparison(frame)
        self.draw_conclusion(frame)
        
        # 添加帧数显示
        self.fig.text(0.02, 0.02, f'Frame: {frame}/{self.total_frames}', 
                     fontsize=10, color='gray')
        
        plt.tight_layout()
        
    def create_animation(self):
        """创建并返回动画对象"""
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.total_frames,
            interval=100, blit=False, repeat=True
        )
        
        return anim

def main():
    """主函数"""
    print("正在创建几何因子原理动画...")
    
    animator = GeometricFactorAnimator()
    anim = animator.create_animation()
    
    # 显示动画
    plt.show()
    
    # 可选：保存为GIF
    save_gif = input("是否保存为GIF文件? (y/n): ").lower().strip()
    if save_gif == 'y':
        print("正在保存GIF文件...")
        anim.save('几何因子原理动画.gif', writer='pillow', fps=10, dpi=80)
        print("GIF文件已保存为: 几何因子原理动画.gif")

if __name__ == "__main__":
    main()
         