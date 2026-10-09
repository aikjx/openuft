#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版双质量引力动画
Fixed Dual-Mass Gravity Animation

修复了引力场线方向和双质量相互作用的可视化问题
Author: Algorithm Alliance - Gravity Animation Specialist
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 120

class FixedGravityAnimator:
    """修复版引力动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 200
        
        # 物理参数
        self.mass_M_pos = np.array([-3, 0, 0])  # 大质量M
        self.mass_m_pos = np.array([3, 0, 0])   # 小质量m
        
        # 颜色配置
        self.colors = {
            'mass_M': '#E74C3C',           # 红色 - 大质量M
            'mass_m': '#3498DB',           # 蓝色 - 小质量m
            'field_M': '#FF6B6B',          # 浅红色 - M的引力场
            'field_m': '#74B9FF',          # 浅蓝色 - m的引力场
            'interaction': '#F39C12',      # 橙色 - 相互作用
            'plane': '#2ECC71',            # 绿色 - 相互作用平面
            'background': '#FAFAFA'
        }
    
    def setup_figure(self):
        """设置图形布局"""
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.patch.set_facecolor(self.colors['background'])
        
        # 主标题
        self.fig.suptitle('🔧 修复版：双质量引力系统的正确可视化', 
                         fontsize=18, fontweight='bold', color='#2C3E50')
        
        # 创建子图
        self.ax_3d = self.fig.add_subplot(221, projection='3d')
        self.ax_field = self.fig.add_subplot(222)
        self.ax_forces = self.fig.add_subplot(223)
        self.ax_explanation = self.fig.add_subplot(224)
        
        return self.fig
    
    def create_gravity_field_lines(self, center_pos, n_lines=20, color='red', inward=True):
        """创建正确的引力场线（向心收敛）"""
        field_lines = []
        
        for i in range(n_lines):
            # 随机生成球面上的起始点
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            
            # 起始半径
            start_radius = 4.0
            
            # 创建向心收敛的场线
            t = np.linspace(0, 1, 50)
            
            # 场线从外向内收敛到质量中心
            radii = start_radius * (1 - 0.9 * t)  # 向内收敛
            
            # 添加轻微的螺旋效果
            theta_spiral = theta + 0.5 * t
            
            x = center_pos[0] + radii * np.sin(phi) * np.cos(theta_spiral)
            y = center_pos[1] + radii * np.sin(phi) * np.sin(theta_spiral)
            z = center_pos[2] + radii * np.cos(phi)
            
            field_lines.append((x, y, z, color))
        
        return field_lines
    
    def create_interaction_field_lines(self):
        """创建两个质量之间的相互作用场线"""
        interaction_lines = []
        
        for i in range(8):
            # 创建连接两个质量的弯曲路径
            t = np.linspace(0, 1, 30)
            
            # 基础直线路径
            base_x = self.mass_M_pos[0] + t * (self.mass_m_pos[0] - self.mass_M_pos[0])
            base_y = self.mass_M_pos[1] + t * (self.mass_m_pos[1] - self.mass_M_pos[1])
            base_z = self.mass_M_pos[2] + t * (self.mass_m_pos[2] - self.mass_M_pos[2])
            
            # 添加正弦波动
            amplitude = 0.5
            frequency = 2 + i * 0.5
            phase = i * np.pi / 4
            
            x = base_x
            y = base_y + amplitude * np.sin(frequency * np.pi * t + phase)
            z = base_z + amplitude * 0.5 * np.cos(frequency * np.pi * t + phase)
            
            interaction_lines.append((x, y, z))
        
        return interaction_lines
    
    def draw_3d_gravity_system(self, frame):
        """绘制3D引力系统"""
        self.ax_3d.clear()
        
        # 设置动态视角
        rotation = frame * 360 / self.total_frames
        self.ax_3d.view_init(elev=20, azim=rotation)
        
        # 绘制质量球体
        u = np.linspace(0, 2*np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        
        # 质量M（大球）
        x_M = self.mass_M_pos[0] + 0.4 * np.outer(np.cos(u), np.sin(v))
        y_M = self.mass_M_pos[1] + 0.4 * np.outer(np.sin(u), np.sin(v))
        z_M = self.mass_M_pos[2] + 0.4 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_3d.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], alpha=0.8)
        
        # 质量m（小球）
        x_m = self.mass_m_pos[0] + 0.25 * np.outer(np.cos(u), np.sin(v))
        y_m = self.mass_m_pos[1] + 0.25 * np.outer(np.sin(u), np.sin(v))
        z_m = self.mass_m_pos[2] + 0.25 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_3d.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], alpha=0.8)
        
        # 绘制M的引力场线（红色，向心）
        field_lines_M = self.create_gravity_field_lines(self.mass_M_pos, 15, self.colors['field_M'])
        for x, y, z, color in field_lines_M:
            self.ax_3d.plot(x, y, z, color=color, alpha=0.6, linewidth=2)
            
            # 添加箭头指示引力方向（向内）
            mid_idx = len(x) // 2
            arrow_start = np.array([x[mid_idx], y[mid_idx], z[mid_idx]])
            arrow_end = np.array([x[mid_idx+5], y[mid_idx+5], z[mid_idx+5]])
            arrow_dir = arrow_end - arrow_start
            
            self.ax_3d.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                            arrow_dir[0], arrow_dir[1], arrow_dir[2],
                            color=color, alpha=0.8, arrow_length_ratio=0.3)
        
        # 绘制m的引力场线（蓝色，向心）
        field_lines_m = self.create_gravity_field_lines(self.mass_m_pos, 10, self.colors['field_m'])
        for x, y, z, color in field_lines_m:
            self.ax_3d.plot(x, y, z, color=color, alpha=0.6, linewidth=2)
            
            # 添加箭头指示引力方向（向内）
            mid_idx = len(x) // 2
            arrow_start = np.array([x[mid_idx], y[mid_idx], z[mid_idx]])
            arrow_end = np.array([x[mid_idx+5], y[mid_idx+5], z[mid_idx+5]])
            arrow_dir = arrow_end - arrow_start
            
            self.ax_3d.quiver(arrow_start[0], arrow_start[1], arrow_start[2],
                            arrow_dir[0], arrow_dir[1], arrow_dir[2],
                            color=color, alpha=0.8, arrow_length_ratio=0.3)
        
        # 绘制相互作用场线（橙色）
        interaction_lines = self.create_interaction_field_lines()
        for x, y, z in interaction_lines:
            self.ax_3d.plot(x, y, z, color=self.colors['interaction'], 
                          alpha=0.7, linewidth=3, linestyle='--')
        
        # 绘制相互作用平面
        xx, yy = np.meshgrid(np.linspace(-5, 5, 20), np.linspace(-4, 4, 16))
        zz = np.zeros_like(xx)
        self.ax_3d.plot_surface(xx, yy, zz, alpha=0.2, color=self.colors['plane'])
        
        # 标注
        self.ax_3d.text(self.mass_M_pos[0], self.mass_M_pos[1], self.mass_M_pos[2]+1,
                       'M\n大质量\n向心引力场', ha='center', fontsize=10, 
                       color=self.colors['mass_M'], fontweight='bold')
        
        self.ax_3d.text(self.mass_m_pos[0], self.mass_m_pos[1], self.mass_m_pos[2]+1,
                       'm\n小质量\n向心引力场', ha='center', fontsize=10,
                       color=self.colors['mass_m'], fontweight='bold')
        
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.set_title('✅ 正确的双质量引力场可视化', fontsize=14, fontweight='bold')
        
        # 设置坐标轴范围
        self.ax_3d.set_xlim([-6, 6])
        self.ax_3d.set_ylim([-5, 5])
        self.ax_3d.set_zlim([-4, 4])
    
    def draw_field_strength_comparison(self, frame):
        """绘制场强对比图"""
        self.ax_field.clear()
        
        # 创建场强分布
        x = np.linspace(-6, 6, 100)
        y = np.linspace(-4, 4, 80)
        X, Y = np.meshgrid(x, y)
        
        # M的引力场强（1/r²，向心）
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + (Y - self.mass_M_pos[1])**2) + 0.1
        field_M = 3.0 / r_M**2
        
        # m的引力场强（1/r²，向心）
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + (Y - self.mass_m_pos[1])**2) + 0.1
        field_m = 1.5 / r_m**2
        
        # 总场强
        total_field = field_M + field_m
        
        # 绘制场强等高线
        contour = self.ax_field.contourf(X, Y, total_field, levels=20, cmap='hot', alpha=0.7)
        self.ax_field.contour(X, Y, total_field, levels=10, colors='white', alpha=0.5, linewidths=0.5)
        
        # 绘制质量位置
        self.ax_field.scatter([self.mass_M_pos[0]], [self.mass_M_pos[1]], 
                            s=400, c=self.colors['mass_M'], alpha=0.9, 
                            marker='o', edgecolors='white', linewidth=2, label='质量M')
        self.ax_field.scatter([self.mass_m_pos[0]], [self.mass_m_pos[1]], 
                            s=250, c=self.colors['mass_m'], alpha=0.9,
                            marker='o', edgecolors='white', linewidth=2, label='质量m')
        
        # 绘制引力矢量场（向心）
        x_vec = np.linspace(-5, 5, 15)
        y_vec = np.linspace(-3, 3, 10)
        X_vec, Y_vec = np.meshgrid(x_vec, y_vec)
        
        # 计算指向M的引力矢量
        dx_M = self.mass_M_pos[0] - X_vec
        dy_M = self.mass_M_pos[1] - Y_vec
        r_M_vec = np.sqrt(dx_M**2 + dy_M**2) + 0.1
        fx_M = dx_M / r_M_vec**3
        fy_M = dy_M / r_M_vec**3
        
        # 计算指向m的引力矢量
        dx_m = self.mass_m_pos[0] - X_vec
        dy_m = self.mass_m_pos[1] - Y_vec
        r_m_vec = np.sqrt(dx_m**2 + dy_m**2) + 0.1
        fx_m = 0.5 * dx_m / r_m_vec**3
        fy_m = 0.5 * dy_m / r_m_vec**3
        
        # 总引力矢量
        fx_total = fx_M + fx_m
        fy_total = fy_M + fy_m
        
        # 绘制矢量场
        self.ax_field.quiver(X_vec, Y_vec, fx_total, fy_total, 
                           alpha=0.6, scale=20, color='white', width=0.003)
        
        self.ax_field.set_xlabel('X')
        self.ax_field.set_ylabel('Y')
        self.ax_field.set_title('🌡️ 引力场强分布（向心收敛）', fontsize=14, fontweight='bold')
        self.ax_field.legend()
        self.ax_field.set_aspect('equal')
        
        # 添加颜色条
        plt.colorbar(contour, ax=self.ax_field, shrink=0.8, label='场强')
    
    def draw_force_analysis(self, frame):
        """绘制力的分析"""
        self.ax_forces.clear()
        
        # 绘制两个质量
        circle_M = Circle(self.mass_M_pos[:2], 0.4, color=self.colors['mass_M'], alpha=0.8)
        circle_m = Circle(self.mass_m_pos[:2], 0.25, color=self.colors['mass_m'], alpha=0.8)
        self.ax_forces.add_patch(circle_M)
        self.ax_forces.add_patch(circle_m)
        
        # 绘制相互作用力（牛顿第三定律）
        force_scale = 2.0
        
        # M对m的引力（向左）
        self.ax_forces.arrow(self.mass_m_pos[0], self.mass_m_pos[1], 
                           -force_scale, 0, head_width=0.3, head_length=0.3,
                           fc=self.colors['interaction'], ec=self.colors['interaction'],
                           linewidth=3, alpha=0.8)
        self.ax_forces.text(self.mass_m_pos[0]-1, self.mass_m_pos[1]+0.8, 
                          'F(M→m)', ha='center', fontsize=12, 
                          color=self.colors['interaction'], fontweight='bold')
        
        # m对M的引力（向右）
        self.ax_forces.arrow(self.mass_M_pos[0], self.mass_M_pos[1], 
                           force_scale, 0, head_width=0.3, head_length=0.3,
                           fc=self.colors['interaction'], ec=self.colors['interaction'],
                           linewidth=3, alpha=0.8)
        self.ax_forces.text(self.mass_M_pos[0]+1, self.mass_M_pos[1]+0.8, 
                          'F(m→M)', ha='center', fontsize=12,
                          color=self.colors['interaction'], fontweight='bold')
        
        # 添加等号表示力的大小相等
        self.ax_forces.text(0, 2, '|F(M→m)| = |F(m→M)|', ha='center', fontsize=14,
                          color=self.colors['interaction'], fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
        
        # 添加牛顿万有引力定律
        self.ax_forces.text(0, -2.5, r'$F = G\frac{Mm}{r^2}$', ha='center', fontsize=16,
                          color='#2C3E50', fontweight='bold',
                          bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))
        
        self.ax_forces.set_xlim(-5, 5)
        self.ax_forces.set_ylim(-3.5, 3.5)
        self.ax_forces.set_aspect('equal')
        self.ax_forces.set_title('⚖️ 牛顿第三定律：作用力与反作用力', fontsize=14, fontweight='bold')
        self.ax_forces.grid(True, alpha=0.3)
    
    def draw_explanation(self, frame):
        """绘制修复说明"""
        self.ax_explanation.clear()
        self.ax_explanation.axis('off')
        
        explanations = [
            "🔧 算法联盟 - 引力动画修复报告",
            "",
            "❌ 原始问题:",
            "• 只显示质量M的发散场",
            "• 场线方向错误（应该向心收敛）",
            "• 缺少质量m的引力场",
            "• 没有体现双向相互作用",
            "",
            "✅ 修复内容:",
            "• 添加了质量m的向心引力场（蓝色）",
            "• 修正了场线方向（从发散改为收敛）",
            "• 增加了相互作用场线（橙色虚线）",
            "• 显示了牛顿第三定律的力平衡",
            "• 正确的引力矢量场可视化",
            "",
            "🎯 物理原理:",
            "• 引力是吸引力，场线向质量中心收敛",
            "• 两个质量都产生引力场",
            "• 相互作用力大小相等，方向相反",
            "• 场强遵循1/r²定律",
            "",
            "📊 技术改进:",
            "• 使用正确的向心矢量场",
            "• 双色编码区分不同质量的场",
            "• 动态箭头指示引力方向",
            "• 实时场强分布计算"
        ]
        
        y_start = 0.95
        line_height = 0.035
        
        for i, line in enumerate(explanations):
            y_pos = y_start - i * line_height
            
            if line.startswith("🔧"):
                color = self.colors['interaction']
                weight = 'bold'
                size = 14
            elif line.startswith(("❌", "✅", "🎯", "📊")):
                color = '#2C3E50'
                weight = 'bold'
                size = 12
            elif line.startswith("•"):
                color = '#34495E'
                weight = 'normal'
                size = 10
            else:
                color = '#2C3E50'
                weight = 'normal'
                size = 11
            
            self.ax_explanation.text(0.05, y_pos, line, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 添加修复状态指示
        status_box = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.08,
                                          boxstyle="round,pad=0.02",
                                          facecolor='lightgreen',
                                          edgecolor=self.colors['interaction'],
                                          linewidth=2,
                                          transform=self.ax_explanation.transAxes)
        self.ax_explanation.add_patch(status_box)
        
        self.ax_explanation.text(0.5, 0.06, 
                               '✅ 修复完成：双质量引力系统现在正确显示向心引力场和相互作用',
                               ha='center', va='center', fontsize=11, 
                               color='#2C3E50', fontweight='bold',
                               transform=self.ax_explanation.transAxes)
    
    def animate(self, frame):
        """主动画函数"""
        self.draw_3d_gravity_system(frame)
        self.draw_field_strength_comparison(frame)
        self.draw_force_analysis(frame)
        self.draw_explanation(frame)
        
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
    print("🔧 算法联盟 - 引力动画修复程序启动")
    print("正在修复双质量引力系统的可视化问题...")
    
    animator = FixedGravityAnimator()
    anim = animator.create_animation()
    
    plt.show()
    
    print("\n✅ 修复完成！主要改进：")
    print("• 修正了引力场线方向（从发散改为向心收敛）")
    print("• 添加了质量m的引力场可视化")
    print("• 增加了双向相互作用效果")
    print("• 正确显示了牛顿第三定律")
    print("• 改进了场强分布的可视化")
    
    # 保存选项
    save_option = input("\n💾 是否保存修复版动画？(y/n): ").lower().strip()
    if save_option == 'y':
        print("正在保存...")
        anim.save('修复版双质量引力动画.gif', writer='pillow', fps=10, dpi=150)
        print("✅ 已保存为: 修复版双质量引力动画.gif")

if __name__ == "__main__":
    main()