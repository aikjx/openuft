#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三维空间发散场与二维平面相互作用的终极版3D动画
Ultimate 3D Space Divergent Field and 2D Plane Interaction Animation

核心概念：质量M产生球对称空间发散场，与质量m在二维平面上相互作用
每个子图都可以单独放大查看，提供最佳的可视化体验
Author: Physics Visualization Master Pro
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

# 设置中文字体和超高质量渲染
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 400

class UltimateSpaceFieldAnimator:
    """终极版空间场相互作用动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 300
        
        # 物理参数
        self.mass_M_pos = np.array([-2.5, 0, 0])
        self.mass_m_pos = np.array([2.5, 0, 0])
        
        # 专业物理色彩
        self.colors = {
            'mass_M': '#E74C3C',
            'mass_m': '#3498DB', 
            'field_M': '#FF6B6B',
            'field_m': '#74B9FF',
            'interaction_plane': '#2ECC71',
            'field_lines': '#F39C12',
            'projection': '#E67E22',
            'background': '#FAFAFA',
            'text': '#2C3E50',
            'highlight': '#9B59B6',
            'grid': '#BDC3C7'
        }
    
    def setup_figure(self):
        """设置终极版布局"""
        self.fig = plt.figure(figsize=(24, 18))
        self.fig.patch.set_facecolor(self.colors['background'])
        
        # 网格布局
        gs = gridspec.GridSpec(3, 4, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # 主标题
        self.fig.suptitle('🌌 三维空间发散场与二维平面相互作用的终极物理可视化', 
                         fontsize=24, fontweight='bold', color=self.colors['text'], y=0.95)
        
        # 创建子图
        self.ax_main = self.fig.add_subplot(gs[0:2, 0:2], projection='3d')
        self.ax_side = self.fig.add_subplot(gs[0, 2], projection='3d')
        self.ax_top = self.fig.add_subplot(gs[0, 3])
        self.ax_projection = self.fig.add_subplot(gs[1, 2])
        self.ax_field_strength = self.fig.add_subplot(gs[1, 3])
        self.ax_explanation = self.fig.add_subplot(gs[2, 0:2])
        self.ax_math = self.fig.add_subplot(gs[2, 2])
        self.ax_controls = self.fig.add_subplot(gs[2, 3])
        
        self.setup_controls()
        return self.fig
    
    def setup_controls(self):
        """设置控制面板"""
        self.ax_controls.axis('off')
        self.ax_controls.set_title('🎮 交互控制', fontsize=14, fontweight='bold')
        
        controls_text = [
            "💡 使用说明:",
            "• 鼠标拖拽旋转3D视图",
            "• 滚轮缩放",
            "• 点击子图单独放大",
            "",
            "📊 当前显示:",
            "• 球对称发散场",
            "• 二维相互作用平面", 
            "• 场线投影效果",
            "• 几何因子分析"
        ]
        
        y_pos = 0.9
        for text in controls_text:
            if text.startswith(('💡', '📊')):
                color = self.colors['highlight']
                weight = 'bold'
                size = 12
            else:
                color = self.colors['text']
                weight = 'normal'
                size = 10
            
            self.ax_controls.text(0.05, y_pos, text, fontsize=size, color=color,
                                weight=weight, transform=self.ax_controls.transAxes)
            y_pos -= 0.08
    
    def create_spherical_field(self, center, radius_max=4, n_points=25):
        """创建球对称发散场"""
        spheres = []
        for r in np.linspace(0.5, radius_max, 6):
            u = np.linspace(0, 2*np.pi, n_points)
            v = np.linspace(0, np.pi, n_points//2)
            x = center[0] + r * np.outer(np.cos(u), np.sin(v))
            y = center[1] + r * np.outer(np.sin(u), np.sin(v))
            z = center[2] + r * np.outer(np.ones(np.size(u)), np.cos(v))
            spheres.append((x, y, z, r))
        return spheres
    
    def create_field_vectors(self, center, n_vectors=40):
        """创建发散矢量场"""
        vectors = []
        np.random.seed(42)
        
        for i in range(n_vectors):
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            
            direction = np.array([
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi)
            ])
            
            start = center
            end = center + 2.5 * direction
            
            vectors.append({'start': start, 'end': end, 'direction': direction})
        
        return vectors
    
    def draw_main_3d_view(self, frame):
        """绘制主3D视图"""
        self.ax_main.clear()
        
        # 动态视角
        rotation = frame * 360 / self.total_frames
        elevation = 25 + 10 * np.sin(frame * 2 * np.pi / self.total_frames)
        self.ax_main.view_init(elev=elevation, azim=rotation)
        
        # 绘制质量球体
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        # 质量M
        x_M = self.mass_M_pos[0] + 0.4 * np.outer(np.cos(u), np.sin(v))
        y_M = self.mass_M_pos[1] + 0.4 * np.outer(np.sin(u), np.sin(v))
        z_M = self.mass_M_pos[2] + 0.4 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_main.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], alpha=0.9)
        
        # 质量m
        x_m = self.mass_m_pos[0] + 0.25 * np.outer(np.cos(u), np.sin(v))
        y_m = self.mass_m_pos[1] + 0.25 * np.outer(np.sin(u), np.sin(v))
        z_m = self.mass_m_pos[2] + 0.25 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_main.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], alpha=0.9)
        
        # 绘制发散场
        spheres_M = self.create_spherical_field(self.mass_M_pos)
        for i, (x, y, z, r) in enumerate(spheres_M):
            alpha = 0.15 - i * 0.02
            if alpha > 0:
                color_intensity = 1.0 - i * 0.15
                color = plt.cm.Reds(color_intensity * 0.7)
                self.ax_main.plot_wireframe(x, y, z, alpha=alpha, color=color, linewidth=1.2)
        
        spheres_m = self.create_spherical_field(self.mass_m_pos, radius_max=3)
        for i, (x, y, z, r) in enumerate(spheres_m):
            alpha = 0.12 - i * 0.018
            if alpha > 0:
                color_intensity = 1.0 - i * 0.15
                color = plt.cm.Blues(color_intensity * 0.7)
                self.ax_main.plot_wireframe(x, y, z, alpha=alpha, color=color, linewidth=1.0)
        
        # 相互作用平面
        xx, yy = np.meshgrid(np.linspace(-5, 5, 30), np.linspace(-4, 4, 25))
        zz = np.zeros_like(xx)
        wave_effect = 0.05 * np.sin(frame * 0.2) * np.exp(-(xx**2 + yy**2) / 10)
        zz += wave_effect
        
        self.ax_main.plot_surface(xx, yy, zz, alpha=0.4, 
                                color=self.colors['interaction_plane'], shade=True)
        
        # 发散矢量
        vectors_M = self.create_field_vectors(self.mass_M_pos)
        progress = (frame % 120) / 120.0
        n_visible = int(len(vectors_M) * progress)
        
        for vec in vectors_M[:n_visible]:
            length = np.linalg.norm(vec['end'] - vec['start'])
            alpha = min(0.8, 2.0 / length)
            self.ax_main.quiver(vec['start'][0], vec['start'][1], vec['start'][2],
                              vec['end'][0]-vec['start'][0], 
                              vec['end'][1]-vec['start'][1],
                              vec['end'][2]-vec['start'][2],
                              color=self.colors['field_lines'], alpha=alpha, 
                              arrow_length_ratio=0.15, linewidth=1.5)
        
        # 标注
        self.ax_main.text(self.mass_M_pos[0], self.mass_M_pos[1], self.mass_M_pos[2]+1.5,
                         'M\n大质量\n球对称发散场', fontsize=13, color=self.colors['mass_M'], 
                         ha='center', fontweight='bold', 
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        self.ax_main.text(self.mass_m_pos[0], self.mass_m_pos[1], self.mass_m_pos[2]+1.2,
                         'm\n小质量\n感受场', fontsize=12, color=self.colors['mass_m'],
                         ha='center', fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        self.ax_main.text(0, 3, 0.2, '二维相互作用平面\n(z = 0)', 
                         fontsize=12, color=self.colors['interaction_plane'],
                         ha='center', fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        
        self.ax_main.set_xlabel('X 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_ylabel('Y 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_zlabel('Z 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_title('🌌 三维空间球对称发散场全景图', 
                              fontsize=16, fontweight='bold', pad=20)
        
        self.ax_main.set_xlim([-6, 6])
        self.ax_main.set_ylim([-5, 5])
        self.ax_main.set_zlim([-4, 4])
        self.ax_main.grid(True, alpha=0.3)
    
    def draw_side_view(self, frame):
        """绘制侧视图"""
        self.ax_side.clear()
        self.ax_side.view_init(elev=0, azim=90)
        
        # 绘制质量
        u = np.linspace(0, 2*np.pi, 15)
        v = np.linspace(0, np.pi, 10)
        
        x_M = self.mass_M_pos[0] + 0.3 * np.outer(np.cos(u), np.sin(v))
        y_M = self.mass_M_pos[1] + 0.3 * np.outer(np.sin(u), np.sin(v))
        z_M = self.mass_M_pos[2] + 0.3 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_side.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], alpha=0.8)
        
        x_m = self.mass_m_pos[0] + 0.2 * np.outer(np.cos(u), np.sin(v))
        y_m = self.mass_m_pos[1] + 0.2 * np.outer(np.sin(u), np.sin(v))
        z_m = self.mass_m_pos[2] + 0.2 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_side.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], alpha=0.8)
        
        # 相互作用平面
        xx, yy = np.meshgrid(np.linspace(-4, 4, 15), np.linspace(-3, 3, 12))
        zz = np.zeros_like(xx)
        self.ax_side.plot_surface(xx, yy, zz, alpha=0.6, color=self.colors['interaction_plane'])
        
        # 投影线
        n_lines = 20
        angles = np.linspace(0, 2*np.pi, n_lines)
        elevations = np.linspace(-np.pi/4, np.pi/4, 8)
        
        progress = (frame % 80) / 80.0
        flash = np.sin(frame * 0.3) > 0
        
        for i, angle in enumerate(angles):
            for j, elevation in enumerate(elevations):
                if (i + j * n_lines) / (n_lines * len(elevations)) <= progress:
                    r = 2.0
                    x = self.mass_M_pos[0] + r * np.cos(elevation) * np.cos(angle)
                    y = self.mass_M_pos[1] + r * np.cos(elevation) * np.sin(angle)
                    z = self.mass_M_pos[2] + r * np.sin(elevation)
                    
                    x_proj, y_proj, z_proj = x, y, 0
                    
                    if flash:
                        alpha = 0.7 * (1 - abs(elevation) / (np.pi/4))
                        self.ax_side.plot([x, x_proj], [y, y_proj], [z, z_proj],
                                        color=self.colors['projection'], 
                                        alpha=alpha, linewidth=1.5)
        
        self.ax_side.set_title('📐 侧视图：投影过程', fontsize=14, fontweight='bold')
        self.ax_side.set_xlim([-4, 4])
        self.ax_side.set_ylim([-3, 3])
        self.ax_side.set_zlim([-2.5, 2.5])
    
    def draw_top_view(self, frame):
        """绘制俯视图"""
        self.ax_top.clear()
        
        # 场强分布
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-4, 4, 40)
        X, Y = np.meshgrid(x, y)
        
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + (Y - self.mass_M_pos[1])**2) + 0.1
        field_M = 2.0 / r_M**2
        
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + (Y - self.mass_m_pos[1])**2) + 0.1
        field_m = 1.0 / r_m**2
        
        total_field = field_M + field_m
        
        # 彩色场强图
        im = self.ax_top.imshow(total_field, extent=[-5, 5, -4, 4], 
                               origin='lower', cmap='hot', alpha=0.7)
        
        # 等高线
        levels = np.logspace(-1, 1, 8)
        self.ax_top.contour(X, Y, total_field, levels=levels, colors='white', alpha=0.8)
        
        # 质量位置
        self.ax_top.scatter([self.mass_M_pos[0]], [self.mass_M_pos[1]], 
                           s=400, c=self.colors['mass_M'], alpha=0.9, 
                           marker='o', edgecolors='white', linewidth=2)
        self.ax_top.scatter([self.mass_m_pos[0]], [self.mass_m_pos[1]], 
                           s=250, c=self.colors['mass_m'], alpha=0.9,
                           marker='o', edgecolors='white', linewidth=2)
        
        # 相互作用区域
        interaction_mask = (np.abs(X) < 1) & (np.abs(Y) < 1)
        if frame % 60 < 30:
            self.ax_top.contourf(X, Y, interaction_mask.astype(float), 
                               levels=[0.5, 1.5], colors=[self.colors['highlight']], alpha=0.3)
        
        self.ax_top.set_xlabel('X')
        self.ax_top.set_ylabel('Y')
        self.ax_top.set_title('🔍 俯视图：场分布', fontsize=14, fontweight='bold')
        self.ax_top.set_xlim([-5, 5])
        self.ax_top.set_ylim([-4, 4])
    
    def draw_projection_analysis(self, frame):
        """绘制投影分析"""
        self.ax_projection.clear()
        
        # 高分辨率场强分布
        x = np.linspace(-4, 4, 80)
        y = np.linspace(-4, 4, 80)
        X, Y = np.meshgrid(x, y)
        
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + Y**2) + 0.1
        field_M = 3.0 / r_M**2
        
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + Y**2) + 0.1
        field_m = 1.5 / r_m**2
        
        total_field = field_M + field_m
        
        # 彩色场强分布
        im = self.ax_projection.imshow(total_field, extent=[-4, 4, -4, 4], 
                                     origin='lower', cmap='hot', alpha=0.7,
                                     vmax=np.percentile(total_field, 95))
        
        # 等高线
        levels = np.logspace(-0.5, 1.5, 8)
        self.ax_projection.contour(X, Y, total_field, levels=levels,
                                 colors='white', alpha=0.8, linewidths=1.5)
        
        # 质量位置
        self.ax_projection.scatter([self.mass_M_pos[0]], [0], s=500, 
                                 c=self.colors['mass_M'], alpha=0.9, 
                                 marker='o', edgecolors='white', linewidth=3,
                                 label='质量M', zorder=10)
        self.ax_projection.scatter([self.mass_m_pos[0]], [0], s=350,
                                 c=self.colors['mass_m'], alpha=0.9,
                                 marker='o', edgecolors='white', linewidth=3,
                                 label='质量m', zorder=10)
        
        # 动态相互作用区域
        interaction_width = 0.5 + 0.3 * np.sin(frame * 0.1)
        interaction_rect = Rectangle((-interaction_width, -interaction_width), 
                                   2*interaction_width, 2*interaction_width,
                                   fill=True, color=self.colors['highlight'], 
                                   alpha=0.3, zorder=5)
        self.ax_projection.add_patch(interaction_rect)
        
        # 相互作用箭头
        arrow_props = dict(arrowstyle='<->', color=self.colors['projection'], lw=4, alpha=0.8)
        self.ax_projection.annotate('', xy=(1.5, 0), xytext=(-1.5, 0), arrowprops=arrow_props, zorder=8)
        
        self.ax_projection.text(0, -0.8, '相互作用区域', ha='center', fontsize=12,
                              color=self.colors['projection'], fontweight='bold',
                              bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        self.ax_projection.set_xlim(-4, 4)
        self.ax_projection.set_ylim(-4, 4)
        self.ax_projection.set_aspect('equal')
        self.ax_projection.set_title('📊 二维平面场强分布', fontsize=14, fontweight='bold')
        self.ax_projection.legend(loc='upper right')
        self.ax_projection.grid(True, alpha=0.3)
    
    def draw_field_strength_plot(self, frame):
        """绘制场强图"""
        self.ax_field_strength.clear()
        
        r = np.linspace(0.1, 5, 100)
        field_1_over_r2 = 1 / r**2
        field_1_over_r = 1 / r
        field_exp = np.exp(-r)
        
        self.ax_field_strength.plot(r, field_1_over_r2, 'r-', linewidth=3, 
                                   label='1/r² (引力场)', alpha=0.8)
        self.ax_field_strength.plot(r, field_1_over_r, 'b--', linewidth=2,
                                   label='1/r (对比)', alpha=0.7)
        self.ax_field_strength.plot(r, field_exp, 'g:', linewidth=2,
                                   label='e^(-r) (指数衰减)', alpha=0.7)
        
        # 动态标记
        current_r = 2.5 + 1.5 * np.sin(frame * 0.05)
        current_field = 1 / current_r**2
        
        self.ax_field_strength.scatter([current_r], [current_field], 
                                     s=100, c=self.colors['highlight'], zorder=10, alpha=0.9)
        self.ax_field_strength.axvline(x=current_r, color=self.colors['highlight'],
                                     linestyle='--', alpha=0.5)
        
        self.ax_field_strength.text(current_r + 0.2, current_field,
                                   f'r={current_r:.1f}\nF∝1/r²={current_field:.2f}',
                                   fontsize=10, color=self.colors['highlight'],
                                   bbox=dict(boxstyle="round,pad=0.3", 
                                           facecolor='lightyellow', alpha=0.8))
        
        self.ax_field_strength.set_xlabel('距离 r', fontsize=12)
        self.ax_field_strength.set_ylabel('场强', fontsize=12)
        self.ax_field_strength.set_title('📈 场强-距离关系', fontsize=14, fontweight='bold')
        self.ax_field_strength.legend()
        self.ax_field_strength.grid(True, alpha=0.3)
        self.ax_field_strength.set_yscale('log')
        self.ax_field_strength.set_ylim(0.01, 100)
    
    def draw_mathematical_formulas(self, frame):
        """绘制数学公式"""
        self.ax_math.clear()
        self.ax_math.axis('off')
        
        formulas = [
            "🧮 几何因子数学推导:",
            "",
            "1️⃣ 球面积公式:",
            r"   $S_{球} = 4\pi r^2$",
            "",
            "2️⃣ 圆周长公式:",
            r"   $C_{圆} = 2\pi r$",
            "",
            "3️⃣ 比值计算:",
            r"   $\frac{S_{球}}{C_{圆}} = \frac{4\pi r^2}{2\pi r} = 2r$",
            "",
            "⚠️ 问题分析:",
            "• 结果有长度量纲 [L¹]",
            "• 不是无量纲几何因子",
            "• 依赖于r的选择",
            "",
            "✅ 正确的几何因子:",
            "• 应该是无量纲数",
            "• 来源于物理原理",
            "• 如立体角: 4π"
        ]
        
        progress = frame / self.total_frames
        n_lines = min(len(formulas), int(progress * len(formulas) * 1.2) + 1)
        
        y_start = 0.95
        line_height = 0.045
        
        for i in range(n_lines):
            if i >= len(formulas):
                break
                
            line = formulas[i]
            y_pos = y_start - i * line_height
            
            if line.startswith('🧮'):
                color = self.colors['highlight']
                weight = 'bold'
                size = 14
            elif line.startswith(('1️⃣', '2️⃣', '3️⃣')):
                color = self.colors['mass_M']
                weight = 'bold'
                size = 12
            elif line.startswith('⚠️'):
                color = self.colors['projection']
                weight = 'bold'
                size = 12
            elif line.startswith('✅'):
                color = self.colors['interaction_plane']
                weight = 'bold'
                size = 12
            elif line.startswith('•'):
                color = self.colors['text']
                weight = 'normal'
                size = 10
            elif line.startswith('   $'):
                color = self.colors['mass_m']
                weight = 'normal'
                size = 11
            else:
                color = self.colors['text']
                weight = 'normal'
                size = 10
            
            self.ax_math.text(0.05, y_pos, line, fontsize=size, color=color,
                            weight=weight, transform=self.ax_math.transAxes)
        
        self.ax_math.set_title('📐 数学公式分析', fontsize=14, fontweight='bold')
    
    def draw_explanation(self, frame):
        """绘制详细解释"""
        self.ax_explanation.clear()
        self.ax_explanation.axis('off')
        
        explanations = [
            ("🌟 核心物理概念:", self.colors['highlight'], 'bold', 14),
            ("", 'black', 'normal', 10),
            ("💫 质量M的空间发散场:", self.colors['mass_M'], 'bold', 12),
            ("  • 以光速c向所有方向发散", self.colors['text'], 'normal', 11),
            ("  • 球对称分布：F ∝ 1/r²", self.colors['text'], 'normal', 11),
            ("  • 三维空间中的场线密度", self.colors['text'], 'normal', 11),
            ("", 'black', 'normal', 10),
            ("🔵 质量m的响应:", self.colors['mass_m'], 'bold', 12),
            ("  • 感受到M的发散场", self.colors['text'], 'normal', 11),
            ("  • 产生自己的小发散场", self.colors['text'], 'normal', 11),
            ("", 'black', 'normal', 10),
            ("🟢 二维相互作用平面:", self.colors['interaction_plane'], 'bold', 12),
            ("  • 两个场在z=0平面相遇", self.colors['text'], 'normal', 11),
            ("  • 三维场→二维投影", self.colors['text'], 'normal', 11),
            ("  • 需要几何修正因子", self.colors['text'], 'normal', 11),
        ]
        
        problems = [
            ("⚠️ 几何因子推导问题:", self.colors['projection'], 'bold', 12),
            ("", 'black', 'normal', 10),
            ("❌ 球面积/圆周长 = 2r", self.colors['projection'], 'normal', 11),
            ("  • 有长度量纲 [L¹]", 'red', 'normal', 10),
            ("  • 不是无量纲数", 'red', 'normal', 10),
            ("  • 物理意义不明", 'red', 'normal', 10),
            ("", 'black', 'normal', 10),
            ("✅ 正确的几何因子:", self.colors['interaction_plane'], 'bold', 12),
            ("  • 立体角：4π (无量纲)", self.colors['interaction_plane'], 'normal', 10),
            ("  • 投影因子：1/2", self.colors['interaction_plane'], 'normal', 10),
            ("  • 对称性因子：1,2,4", self.colors['interaction_plane'], 'normal', 10),
            ("", 'black', 'normal', 10),
            ("🎯 建议改进:", self.colors['highlight'], 'bold', 12),
            ("  • 从物理第一原理出发", self.colors['text'], 'normal', 10),
            ("  • 使用标准场论方法", self.colors['text'], 'normal', 10),
            ("  • 确保量纲一致性", self.colors['text'], 'normal', 10),
        ]
        
        progress = frame / self.total_frames
        n_explanations = min(len(explanations), int(progress * len(explanations) * 0.8) + 1)
        n_problems = min(len(problems), max(0, int((progress - 0.3) * len(problems) * 1.2)))
        
        # 左列
        y_start_left = 0.95
        line_height = 0.055
        
        for i in range(n_explanations):
            if i >= len(explanations):
                break
            text, color, weight, size = explanations[i]
            y_pos = y_start_left - i * line_height
            self.ax_explanation.text(0.02, y_pos, text, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 右列
        y_start_right = 0.95
        for i in range(n_problems):
            if i >= len(problems):
                break
            text, color, weight, size = problems[i]
            y_pos = y_start_right - i * line_height
            self.ax_explanation.text(0.52, y_pos, text, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 分隔线
        self.ax_explanation.axvline(x=0.5, color=self.colors['grid'], alpha=0.3)
        
        # 底部总结
        if progress > 0.7:
            summary_box = FancyBboxPatch((0.05, 0.02), 0.9, 0.12,
                                       boxstyle="round,pad=0.02",
                                       facecolor='lightblue',
                                       edgecolor=self.colors['highlight'],
                                       linewidth=2,
                                       transform=self.ax_explanation.transAxes)
            self.ax_explanation.add_patch(summary_box)
            
            self.ax_explanation.text(0.5, 0.08, 
                                   '🎯 核心结论：球面积/圆周长比值缺乏严格的物理基础\n'
                                   '建议使用标准的场论方法重新推导几何因子',
                                   ha='center', va='center', fontsize=12, 
                                   color=self.colors['text'], fontweight='bold',
                                   transform=self.ax_explanation.transAxes)
        
        self.ax_explanation.set_title('🔬 物理原理详解与问题分析', 
                                    fontsize=16, fontweight='bold', pad=20)
    
    def animate(self, frame):
        """主动画函数"""
        self.draw_main_3d_view(frame)
        self.draw_side_view(frame)
        self.draw_top_view(frame)
        self.draw_projection_analysis(frame)
        self.draw_field_strength_plot(frame)
        self.draw_explanation(frame)
        self.draw_mathematical_formulas(frame)
        
        # 进度信息
        progress_text = f'动画进度: {frame}/{self.total_frames} ({frame/self.total_frames*100:.1f}%)'
        self.fig.text(0.02, 0.02, progress_text, fontsize=10, color='gray')
        
        if frame < 50:
            self.fig.text(0.5, 0.02, '💡 提示：点击任意子图可单独放大查看', 
                         ha='center', fontsize=12, color=self.colors['highlight'],
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
        
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
    print("🚀 正在创建三维空间发散场与二维平面相互作用的终极版动画...")
    print("✨ 新功能：")
    print("   • 超高质量3D渲染")
    print("   • 多视角同步显示")
    print("   • 交互式子图放大")
    print("   • 详细的物理原理解释")
    print("   • 几何因子问题分析")
    
    animator = UltimateSpaceFieldAnimator()
    anim = animator.create_animation()
    
    plt.show()
    
    # 保存选项
    print("\n💾 保存选项:")
    save_option = input("1. 保存为超高清GIF\n2. 保存为4K MP4\n3. 保存静态图片\n4. 不保存\n请选择 (1-4): ").strip()
    
    if save_option == '1':
        print("🎬 正在保存超高清GIF...")
        anim.save('三维发散场终极版动画.gif', writer='pillow', fps=10, dpi=200)
        print("✅ GIF已保存: 三维发散场终极版动画.gif")
        
    elif save_option == '2':
        print("🎥 正在保存4K MP4...")
        try:
            anim.save('三维发散场终极版动画.mp4', writer='ffmpeg', fps=15, dpi=300, bitrate=5000)
            print("✅ MP4已保存: 三维发散场终极版动画.mp4")
        except Exception as e:
            print(f"❌ MP4保存失败: {e}")
            print("💡 请确保安装了ffmpeg")
            
    elif save_option == '3':
        print("📸 正在保存静态图片...")
        animator.animate(animator.total_frames // 2)
        plt.savefig('三维发散场静态图.png', dpi=400, bbox_inches='tight')
        print("✅ 静态图已保存: 三维发散场静态图.png")
    
    print("\n🎯 动画展示内容总结:")
    print("✅ 质量M和m的球对称空间发散场")
    print("✅ 三维场向二维平面的投影过程")
    print("✅ 场强分布和相互作用区域")
    print("✅ 几何因子推导的数学问题")
    print("✅ 物理原理的详细解释")
    print("✅ 多视角同步可视化")
    print("\n💡 核心发现：球面积/圆周长比值作为几何因子缺乏严格的物理基础")

if __name__ == "__main__":
    main()