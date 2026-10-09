#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版几何因子原理动画
Simplified Geometric Factor Animation

清晰展示三维球面与二维圆的关系，避免乱码问题
Author: Physics Visualization
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle

# 设置字体，避免乱码
plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

class SimpleGeometricFactorAnimator:
    """简化几何因子动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 200
        
        # 颜色配置
        self.colors = {
            'sphere': '#FF6B6B',
            'circle': '#4ECDC4',
            'highlight': '#FFD93D',
            'text': '#2C3E50',
            'correct': '#27AE60',
            'incorrect': '#E74C3C'
        }
    
    def setup_figure(self):
        """设置图形"""
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.patch.set_facecolor('white')
        
        # 主标题
        self.fig.suptitle('Geometric Factor Analysis: 3D Sphere vs 2D Circle', 
                         fontsize=18, fontweight='bold')
        
        # 创建子图
        self.ax_3d = self.fig.add_subplot(221, projection='3d')
        self.ax_2d = self.fig.add_subplot(222)
        self.ax_calc = self.fig.add_subplot(223)
        self.ax_problem = self.fig.add_subplot(224)
        
        return self.fig
    
    def draw_3d_sphere(self, frame):
        """绘制3D球面"""
        self.ax_3d.clear()
        
        # 创建球面
        u = np.linspace(0, 2*np.pi, 25)
        v = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # 绘制球面
        self.ax_3d.plot_surface(x, y, z, alpha=0.7, color=self.colors['sphere'])
        
        # 绘制赤道圆
        theta = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(theta)
        circle_y = np.sin(theta)
        circle_z = np.zeros_like(theta)
        self.ax_3d.plot(circle_x, circle_y, circle_z, 
                       color=self.colors['highlight'], linewidth=4)
        
        # 动态旋转
        rotation = frame * 360 / self.total_frames
        self.ax_3d.view_init(elev=20, azim=rotation)
        
        # 标注 (避免使用上标符号)
        self.ax_3d.text(0, 0, 1.5, 'Sphere Area = 4*pi*r^2', 
                       fontsize=12, ha='center', color=self.colors['text'])
        
        self.ax_3d.set_title('3D Sphere', fontsize=14, fontweight='bold')
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
    
    def draw_2d_circle(self, frame):
        """绘制2D圆"""
        self.ax_2d.clear()
        
        # 绘制圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['circle'], linewidth=3)
        self.ax_2d.add_patch(circle)
        
        # 动态填充
        progress = (frame % 100) / 100.0
        if progress < 0.5:
            # 显示周长
            theta = np.linspace(0, 2*np.pi*progress*2, int(100*progress*2))
            if len(theta) > 0:
                x_circle = np.cos(theta)
                y_circle = np.sin(theta)
                self.ax_2d.plot(x_circle, y_circle, color=self.colors['highlight'], 
                              linewidth=5, label='Circumference = 2*pi*r')
        else:
            # 显示面积
            theta = np.linspace(0, 2*np.pi, 100)
            x_circle = np.cos(theta)
            y_circle = np.sin(theta)
            self.ax_2d.fill(x_circle, y_circle, alpha=0.3, 
                          color=self.colors['circle'], label='Area = pi*r^2')
        
        self.ax_2d.set_xlim(-1.5, 1.5)
        self.ax_2d.set_ylim(-1.5, 1.5)
        self.ax_2d.set_aspect('equal')
        self.ax_2d.set_title('2D Circle', fontsize=14, fontweight='bold')
        self.ax_2d.legend()
        self.ax_2d.grid(True, alpha=0.3)
    
    def draw_calculation(self, frame):
        """绘制计算过程"""
        self.ax_calc.clear()
        self.ax_calc.axis('off')
        
        # 计算步骤
        steps = [
            "Calculation Steps:",
            "",
            "Step 1: Sphere Area = 4*pi*r^2",
            "Step 2: Circle Circumference = 2*pi*r",
            "Step 3: Ratio = (4*pi*r^2) / (2*pi*r) = 2*r",
            "Step 4: When r = 1, Ratio = 2",
            "",
            "Result: Geometric Factor = 2"
        ]
        
        # 动态显示
        progress = frame / self.total_frames
        n_steps = min(len(steps), int(progress * len(steps) * 2))
        
        y_positions = np.linspace(0.9, 0.1, len(steps))
        
        for i in range(n_steps):
            if i < len(steps):
                step = steps[i]
                color = self.colors['highlight'] if i == n_steps-1 else self.colors['text']
                weight = 'bold' if step.startswith('Step') or step.startswith('Result') else 'normal'
                size = 14 if step.startswith('Calculation') else 12
                
                self.ax_calc.text(0.05, y_positions[i], step, 
                                fontsize=size, color=color, weight=weight,
                                transform=self.ax_calc.transAxes)
        
        self.ax_calc.set_title('Mathematical Derivation', fontsize=14, fontweight='bold')
    
    def draw_problems(self, frame):
        """绘制问题分析"""
        self.ax_problem.clear()
        self.ax_problem.axis('off')
        
        problems = [
            "Problems with this derivation:",
            "",
            "1. Dimensional inconsistency:",
            "   Sphere area [L^2] / Circumference [L^1] = [L^1]",
            "   Result has length dimension, not dimensionless!",
            "",
            "2. Physical meaning unclear:",
            "   Why divide sphere area by circle circumference?",
            "   What does this ratio represent physically?",
            "",
            "3. Arbitrary unit dependence:",
            "   Result depends on choosing r = 1",
            "   Lacks generality",
            "",
            "Conclusion: This derivation has fundamental flaws"
        ]
        
        progress = frame / self.total_frames
        n_lines = min(len(problems), int(progress * len(problems) * 1.2))
        
        y_start = 0.95
        line_height = 0.06
        
        for i in range(n_lines):
            if i < len(problems):
                line = problems[i]
                y_pos = y_start - i * line_height
                
                if line.startswith("Problems") or line.startswith("Conclusion"):
                    color = self.colors['incorrect']
                    weight = 'bold'
                    size = 13
                elif line.startswith(tuple('123')):
                    color = self.colors['incorrect']
                    weight = 'bold'
                    size = 12
                elif line.startswith("   "):
                    color = self.colors['text']
                    weight = 'normal'
                    size = 11
                else:
                    color = self.colors['text']
                    weight = 'normal'
                    size = 11
                
                self.ax_problem.text(0.05, y_pos, line, 
                                   fontsize=size, color=color, weight=weight,
                                   transform=self.ax_problem.transAxes)
        
        self.ax_problem.set_title('Critical Analysis', fontsize=14, fontweight='bold')
    
    def animate(self, frame):
        """主动画函数"""
        self.draw_3d_sphere(frame)
        self.draw_2d_circle(frame)
        self.draw_calculation(frame)
        self.draw_problems(frame)
        
        # 添加帧数
        self.fig.text(0.02, 0.02, f'Frame: {frame}/{self.total_frames}', 
                     fontsize=10, color='gray')
        
        plt.tight_layout()
    
    def create_animation(self):
        """创建动画"""
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.total_frames,
            interval=100, blit=False, repeat=True
        )
        
        return anim

def main():
    """主函数"""
    print("Creating simplified geometric factor animation...")
    print("This animation shows the problems with the sphere/circle ratio derivation")
    
    animator = SimpleGeometricFactorAnimator()
    anim = animator.create_animation()
    
    # 显示动画
    plt.show()
    
    # 保存选项
    save_gif = input("Save as GIF? (y/n): ").lower().strip()
    if save_gif == 'y':
        print("Saving GIF...")
        anim.save('geometric_factor_analysis.gif', writer='pillow', fps=10, dpi=100)
        print("GIF saved as: geometric_factor_analysis.gif")
    
    print("\nKey findings:")
    print("1. The sphere area / circle circumference ratio has length dimension")
    print("2. Geometric factors should be dimensionless")
    print("3. The physical meaning of this ratio is unclear")
    print("4. Standard physics uses different approaches for geometric factors")

if __name__ == "__main__":
    main()