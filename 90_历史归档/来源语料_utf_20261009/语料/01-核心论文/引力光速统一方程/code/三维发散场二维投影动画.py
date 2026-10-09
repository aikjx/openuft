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
from matplotlib.widgets import Button
import matplotlib.gridspec as gridspec

# 设置中文字体和超高质量渲染
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 13
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 400
plt.rcParams['animation.html'] = 'html5'

class SpaceFieldInteractionAnimator:
    """终极版空间场相互作用动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 400
        self.current_view = 'overview'  # 当前视图模式
        self.paused = False
        
        # 物理参数
        self.mass_M_pos = np.array([-2.5, 0, 0])  # 质量M位置
        self.mass_m_pos = np.array([2.5, 0, 0])   # 质量m位置
        self.interaction_plane_z = 0               # 相互作用平面z=0
        
        # 颜色配置 - 专业物理可视化色彩
        self.colors = {
            'mass_M': '#E74C3C',        # 深红色质量M
            'mass_m': '#3498DB',        # 深蓝色质量m
            'field_M': '#FF6B6B',       # M的场 - 渐变红
            'field_m': '#74B9FF',       # m的场 - 渐变蓝
            'interaction_plane': '#2ECC71',  # 翠绿色相互作用平面
            'field_lines': '#F39C12',   # 橙色场线
            'projection': '#E67E22',    # 深橙色投影
            'background': '#FAFAFA',    # 极淡灰背景
            'text': '#2C3E50',
            'highlight': '#9B59B6',     # 紫色高亮
            'grid': '#BDC3C7'           # 浅灰网格
        }
        
        # 创建专业级颜色映射
        self.field_cmap_M = LinearSegmentedColormap.from_list(
            'field_M', ['white', '#FADBD8', '#F1948A', '#E74C3C', '#C0392B'], N=256)
        self.field_cmap_m = LinearSegmentedColormap.from_list(
            'field_m', ['white', '#D6EAF8', '#85C1E9', '#3498DB', '#2980B9'], N=256)
        
        # 动画控制
        self.animation_speed = 1.0
        self.show_field_lines = True
        self.show_projections = True
        
    def setup_figure(self):
        """设置终极版高质量图形布局"""
        # 创建主窗口
        self.fig = plt.figure(figsize=(24, 18))
        self.fig.patch.set_facecolor(self.colors['background'])
        
        # 创建网格布局
        gs = gridspec.GridSpec(3, 4, figure=self.fig, hspace=0.3, wspace=0.3)
        
        # 主标题
        self.fig.suptitle('三维空间发散场与二维平面相互作用的终极物理可视化', 
                         fontsize=24, fontweight='bold', color=self.colors['text'], y=0.95)
        
        # 创建子图 - 可单独放大
        self.ax_main = self.fig.add_subplot(gs[0:2, 0:2], projection='3d')      # 主3D视图
        self.ax_side = self.fig.add_subplot(gs[0, 2], projection='3d')          # 侧视图
        self.ax_top = self.fig.add_subplot(gs[0, 3], projection='3d')           # 俯视图
        self.ax_projection = self.fig.add_subplot(gs[1, 2])                     # 投影分析
        self.ax_field_strength = self.fig.add_subplot(gs[1, 3])                 # 场强分布
        self.ax_explanation = self.fig.add_subplot(gs[2, 0:2])                  # 详细解释
        self.ax_math = self.fig.add_subplot(gs[2, 2])                           # 数学公式
        self.ax_controls = self.fig.add_subplot(gs[2, 3])                       # 控制面板
        
        # 添加交互按钮
        self.setup_interactive_controls()
        
        return self.fig
    
    def setup_interactive_controls(self):
        """设置交互控制"""
        self.ax_controls.axis('off')
        self.ax_controls.set_title('交互控制', fontsize=14, fontweight='bold')
        
        # 添加说明文本
        controls_text = [
            "🎮 交互功能:",
            "• 鼠标拖拽旋转3D视图",
            "• 滚轮缩放",
            "• 点击子图可单独放大",
            "",
            "📊 当前显示:",
            "• 球对称发散场",
            "• 二维相互作用平面", 
            "• 场线投影效果",
            "• 几何因子推导"
        ]
        
        y_pos = 0.9
        for text in controls_text:
            if text.startswith('🎮') or text.startswith('📊'):
                color = self.colors['highlight']
                weight = 'bold'
                size = 12
            elif text.startswith('•'):
                color = self.colors['text']
                weight = 'normal'
                size = 10
            else:
                color = self.colors['text']
                weight = 'normal'
                size = 10
            
            self.ax_controls.text(0.05, y_pos, text, fontsize=size, color=color,
                                weight=weight, transform=self.ax_controls.transAxes)
            y_pos -= 0.08
    
    def create_spherical_field(self, center, radius_max=3, n_points=20):
        """创建球对称发散场"""
        # 创建球面网格
        u = np.linspace(0, 2*np.pi, n_points)
        v = np.linspace(0, np.pi, n_points//2)
        
        spheres = []
        for r in np.linspace(0.5, radius_max, 6):
            x = center[0] + r * np.outer(np.cos(u), np.sin(v))
            y = center[1] + r * np.outer(np.sin(u), np.sin(v))
            z = center[2] + r * np.outer(np.ones(np.size(u)), np.cos(v))
            spheres.append((x, y, z, r))
        
        return spheres
    
    def create_field_vectors(self, center, n_vectors=50):
        """创建从中心发散的场矢量"""
        vectors = []
        
        # 随机生成球面上的点
        np.random.seed(42)  # 固定随机种子保证一致性
        
        for i in range(n_vectors):
            # 球坐标
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            
            # 转换为直角坐标
            direction = np.array([
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi)
            ])
            
            # 矢量起点和终点
            start = center
            end = center + 2.5 * direction
            
            vectors.append({
                'start': start,
                'end': end,
                'direction': direction,
                'theta': theta,
                'phi': phi
            })
        
        return vectors
    
    def draw_main_3d_view(self, frame):
        """绘制主要的3D视图 - 终极版"""
        self.ax_main.clear()
        
        # 动态视角控制
        rotation = frame * 360 / self.total_frames
        elevation = 25 + 10 * np.sin(frame * 2 * np.pi / self.total_frames)
        self.ax_main.view_init(elev=elevation, azim=rotation)
        
        # 绘制高质量质量球体
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        # 质量M - 更大更显眼
        x_M = self.mass_M_pos[0] + 0.4 * np.outer(np.cos(u), np.sin(v))
        y_M = self.mass_M_pos[1] + 0.4 * np.outer(np.sin(u), np.sin(v))
        z_M = self.mass_M_pos[2] + 0.4 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_main.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], 
                                alpha=0.9, shade=True)
        
        # 质量m
        x_m = self.mass_m_pos[0] + 0.25 * np.outer(np.cos(u), np.sin(v))
        y_m = self.mass_m_pos[1] + 0.25 * np.outer(np.sin(u), np.sin(v))
        z_m = self.mass_m_pos[2] + 0.25 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_main.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], 
                                alpha=0.9, shade=True)
        
        # 绘制多层球对称发散场 - M
        spheres_M = self.create_spherical_field(self.mass_M_pos, radius_max=4, n_points=25)
        for i, (x, y, z, r) in enumerate(spheres_M):
            alpha = 0.15 - i * 0.02
            if alpha > 0:
                # 使用渐变色
                color_intensity = 1.0 - i * 0.15
                color = plt.cm.Reds(color_intensity * 0.7)
                self.ax_main.plot_wireframe(x, y, z, alpha=alpha, 
                                          color=color, linewidth=1.2)
        
        # 绘制多层球对称发散场 - m
        spheres_m = self.create_spherical_field(self.mass_m_pos, radius_max=3, n_points=20)
        for i, (x, y, z, r) in enumerate(spheres_m):
            alpha = 0.12 - i * 0.018
            if alpha > 0:
                color_intensity = 1.0 - i * 0.15
                color = plt.cm.Blues(color_intensity * 0.7)
                self.ax_main.plot_wireframe(x, y, z, alpha=alpha,
                                          color=color, linewidth=1.0)
        
        # 绘制相互作用平面 - 更精细
        xx, yy = np.meshgrid(np.linspace(-5, 5, 30), np.linspace(-4, 4, 25))
        zz = np.zeros_like(xx)
        
        # 添加波纹效果
        wave_effect = 0.05 * np.sin(frame * 0.2) * np.exp(-(xx**2 + yy**2) / 10)
        zz += wave_effect
        
        self.ax_main.plot_surface(xx, yy, zz, alpha=0.4, 
                                color=self.colors['interaction_plane'],
                                shade=True, linewidth=0)
        
        # 绘制动态发散矢量场
        if self.show_field_lines:
            vectors_M = self.create_field_vectors(self.mass_M_pos, 40)
            vectors_m = self.create_field_vectors(self.mass_m_pos, 25)
            
            # 动态显示进度
            progress = (frame % 120) / 120.0
            n_visible_M = int(len(vectors_M) * progress)
            n_visible_m = int(len(vectors_m) * progress)
            
            # M的场矢量
            for vec in vectors_M[:n_visible_M]:
                length = np.linalg.norm(vec['end'] - vec['start'])
                alpha = min(0.8, 2.0 / length)  # 距离越近越明显
                self.ax_main.quiver(vec['start'][0], vec['start'][1], vec['start'][2],
                                  vec['end'][0]-vec['start'][0], 
                                  vec['end'][1]-vec['start'][1],
                                  vec['end'][2]-vec['start'][2],
                                  color=self.colors['field_lines'], alpha=alpha, 
                                  arrow_length_ratio=0.15, linewidth=1.5)
            
            # m的场矢量
            for vec in vectors_m[:n_visible_m]:
                length = np.linalg.norm(vec['end'] - vec['start'])
                alpha = min(0.6, 1.5 / length)
                self.ax_main.quiver(vec['start'][0], vec['start'][1], vec['start'][2],
                                  vec['end'][0]-vec['start'][0], 
                                  vec['end'][1]-vec['start'][1],
                                  vec['end'][2]-vec['start'][2],
                                  color=self.colors['projection'], alpha=alpha,
                                  arrow_length_ratio=0.12, linewidth=1.2)
        
        # 高质量标注
        self.ax_main.text(self.mass_M_pos[0], self.mass_M_pos[1], self.mass_M_pos[2]+1.5,
                         'M\n大质量\n球对称发散场', fontsize=13, color=self.colors['mass_M'], 
                         ha='center', fontweight='bold', 
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        self.ax_main.text(self.mass_m_pos[0], self.mass_m_pos[1], self.mass_m_pos[2]+1.2,
                         'm\n小质量\n感受场', fontsize=12, color=self.colors['mass_m'],
                         ha='center', fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # 平面标注
        self.ax_main.text(0, 3, 0.2, '二维相互作用平面\n(z = 0)', 
                         fontsize=12, color=self.colors['interaction_plane'],
                         ha='center', fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        
        # 设置坐标轴
        self.ax_main.set_xlabel('X 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_ylabel('Y 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_zlabel('Z 轴', fontsize=12, fontweight='bold')
        self.ax_main.set_title('🌌 三维空间球对称发散场全景图', 
                              fontsize=16, fontweight='bold', pad=20)
        
        # 设置坐标轴范围和网格
        self.ax_main.set_xlim([-6, 6])
        self.ax_main.set_ylim([-5, 5])
        self.ax_main.set_zlim([-4, 4])
        self.ax_main.grid(True, alpha=0.3)
    
    def draw_side_view(self, frame):
        """绘制侧视图 - 强调投影过程"""
        self.ax_side.clear()
        
        # 固定侧视角度 - 从YZ平面看
        self.ax_side.view_init(elev=0, azim=90)
        
        # 绘制质量球体
        u = np.linspace(0, 2*np.pi, 15)
        v = np.linspace(0, np.pi, 10)
        
        # 质量M
        x_M = self.mass_M_pos[0] + 0.3 * np.outer(np.cos(u), np.sin(v))
        y_M = self.mass_M_pos[1] + 0.3 * np.outer(np.sin(u), np.sin(v))
        z_M = self.mass_M_pos[2] + 0.3 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_side.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], alpha=0.8)
        
        # 质量m
        x_m = self.mass_m_pos[0] + 0.2 * np.outer(np.cos(u), np.sin(v))
        y_m = self.mass_m_pos[1] + 0.2 * np.outer(np.sin(u), np.sin(v))
        z_m = self.mass_m_pos[2] + 0.2 * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_side.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], alpha=0.8)
        
        # 绘制相互作用平面
        xx, yy = np.meshgrid(np.linspace(-4, 4, 15), np.linspace(-3, 3, 12))
        zz = np.zeros_like(xx)
        self.ax_side.plot_surface(xx, yy, zz, alpha=0.6,
                                color=self.colors['interaction_plane'])
        
        # 动态投影线效果
        if self.show_projections:
            n_lines = 20
            angles = np.linspace(0, 2*np.pi, n_lines)
            elevations = np.linspace(-np.pi/4, np.pi/4, 8)
            
            progress = (frame % 80) / 80.0
            flash = np.sin(frame * 0.3) > 0  # 闪烁效果
            
            for i, angle in enumerate(angles):
                for j, elevation in enumerate(elevations):
                    if (i + j * n_lines) / (n_lines * len(elevations)) <= progress:
                        # 球面上的点
                        r = 2.0
                        x = self.mass_M_pos[0] + r * np.cos(elevation) * np.cos(angle)
                        y = self.mass_M_pos[1] + r * np.cos(elevation) * np.sin(angle)
                        z = self.mass_M_pos[2] + r * np.sin(elevation)
                        
                        # 投影到平面
                        x_proj, y_proj, z_proj = x, y, 0
                        
                        if flash:
                            alpha = 0.7 * (1 - abs(elevation) / (np.pi/4))
                            self.ax_side.plot([x, x_proj], [y, y_proj], [z, z_proj],
                                            color=self.colors['projection'], 
                                            alpha=alpha, linewidth=1.5)
        
        self.ax_side.set_xlabel('X')
        self.ax_side.set_ylabel('Y')
        self.ax_side.set_zlabel('Z')
        self.ax_side.set_title('📐 侧视图：投影过程', fontsize=14, fontweight='bold')
        
        self.ax_side.set_xlim([-4, 4])
        self.ax_side.set_ylim([-3, 3])
        self.ax_side.set_zlim([-2.5, 2.5])
    
    def draw_top_view(self, frame):
        """绘制俯视图 - 从上往下看"""
        self.ax_top.clear()
        
        # 俯视角度
        self.ax_top.view_init(elev=90, azim=0)
        
        # 绘制质量在XY平面的投影
        self.ax_top.scatter([self.mass_M_pos[0]], [self.mass_M_pos[1]], [0],
                          s=400, c=self.colors['mass_M'], alpha=0.9, 
                          marker='o', edgecolors='darkred', linewidth=2)
        self.ax_top.scatter([self.mass_m_pos[0]], [self.mass_m_pos[1]], [0],
                          s=250, c=self.colors['mass_m'], alpha=0.9,
                          marker='o', edgecolors='darkblue', linewidth=2)
        
        # 绘制场的等强度线
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-4, 4, 40)
        X, Y = np.meshgrid(x, y)
        
        # M的场强分布
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + (Y - self.mass_M_pos[1])**2) + 0.1
        field_M = 2.0 / r_M**2
        
        # m的场强分布
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + (Y - self.mass_m_pos[1])**2) + 0.1
        field_m = 1.0 / r_m**2
        
        # 总场强
        total_field = field_M + field_m
        
        # 动态等高线
        levels = np.logspace(-1, 1, 8)
        contour = self.ax_top.contour(X, Y, total_field, levels=levels,
                                    colors=[self.colors['field_lines']], alpha=0.7)
        
        # 相互作用区域高亮
        interaction_mask = (np.abs(X) < 1) & (np.abs(Y) < 1)
        if frame % 60 < 30:
            self.ax_top.contourf(X, Y, interaction_mask.astype(float), 
                               levels=[0.5, 1.5], colors=[self.colors['highlight']], alpha=0.3)
        
        self.ax_top.set_xlabel('X')
        self.ax_top.set_ylabel('Y')
        self.ax_top.set_title('🔍 俯视图：场分布', fontsize=14, fontweight='bold')
        
        self.ax_top.set_xlim([-5, 5])
        self.ax_top.set_ylim([-4, 4])
        self.ax_top.set_zlim([-0.1, 0.1])
    
    def draw_projection_analysis(self, frame):
        """绘制投影分析图"""
        self.ax_projection.clear()
        
        # 绘制圆形表示相互作用平面的截面
        circle = Circle((0, 0), 2, fill=False, color=self.colors['interaction_plane'], 
                       linewidth=3, label='相互作用平面截面')
        self.ax_projection.add_patch(circle)
        
        # 绘制质量M和m在平面上的投影
        self.ax_projection.scatter([-2], [0], s=400, c=self.colors['mass_M'], 
                                 alpha=0.8, label='质量M投影', marker='o')
        self.ax_projection.scatter([2], [0], s=300, c=self.colors['mass_m'],
                                 alpha=0.8, label='质量m投影', marker='o')
        
        # 动态显示场强分布
        progress = (frame % 120) / 120.0
        
        # 创建场强分布
        x = np.linspace(-3, 3, 50)
        y = np.linspace(-3, 3, 50)
        X, Y = np.meshgrid(x, y)
        
        # M的场强 (1/r^2分布)
        r_M = np.sqrt((X + 2)**2 + Y**2) + 0.1
        field_M = 1 / r_M**2
        
        # m的场强
        r_m = np.sqrt((X - 2)**2 + Y**2) + 0.1
        field_m = 0.5 / r_m**2
        
        # 总场强
        total_field = field_M + field_m
        
        # 绘制场强等高线
        levels = np.linspace(0, np.max(total_field)*0.8, 10)
        contour = self.ax_projection.contour(X, Y, total_field, levels=levels, 
                                           colors=self.colors['field_lines'], alpha=0.6)
        
        # 绘制相互作用区域 (动态高亮)
        interaction_x = np.linspace(-1, 1, 20)
        interaction_y = np.linspace(-0.5, 0.5, 10)
        IX, IY = np.meshgrid(interaction_x, interaction_y)
        
        if frame % 80 < 40:  # 闪烁效果
            self.ax_projection.contourf(IX, IY, np.ones_like(IX), levels=[0, 1],
                                      colors=[self.colors['projection']], alpha=0.3)
        
        # 添加箭头表示相互作用
        self.ax_projection.annotate('', xy=(1, 0), xytext=(-1, 0),
                                  arrowprops=dict(arrowstyle='<->', 
                                                color=self.colors['projection'],
                                                lw=3))
        self.ax_projection.text(0, -0.3, '相互作用', ha='center', fontsize=12,
                              color=self.colors['projection'], fontweight='bold')
        
        self.ax_projection.set_xlim(-3.5, 3.5)
        self.ax_projection.set_ylim(-3.5, 3.5)
        self.ax_projection.set_aspect('equal')
        self.ax_projection.set_title('二维平面上的场相互作用', fontsize=14, fontweight='bold')
        self.ax_projection.legend(loc='upper right')
        self.ax_projection.grid(True, alpha=0.3)
    
    def draw_explanation(self, frame):
        """绘制原理解释"""
        self.ax_explanation.clear()
        self.ax_explanation.axis('off')
        
        # 动态显示解释文本
        explanations = [
            "物理原理解释:",
            "",
            "1. 质量M产生球对称空间发散场",
            "   • 场向所有方向以光速c发散",
            "   • 三维空间中的球面波",
            "",
            "2. 质量m也产生类似的发散场",
            "   • 两个场在空间中重叠",
            "",
            "3. 相互作用发生在二维平面上",
            "   • 三维球面场投影到二维平面",
            "   • 需要几何修正因子",
            "",
            "4. 几何因子的来源:",
            "   • 球面积: 4πr^2 (三维总量)",
            "   • 平面截面: πr^2 (二维有效量)",
            "   • 比值: 4πr^2/πr^2 = 4",
            "",
            "5. 考虑对称性和投影效应",
            "   • 实际几何因子 ≈ 2",
            "",
            "核心思想: 三维→二维的几何约化"
        ]
        
        progress = frame / self.total_frames
        n_lines = min(len(explanations), int(progress * len(explanations) * 1.5))
        
        y_start = 0.95
        line_height = 0.04
        
        for i in range(n_lines):
            line = explanations[i]
            y_pos = y_start - i * line_height
            
            # 设置不同的文本样式
            if line.endswith(":"):
                color = self.colors['mass_M']
                weight = 'bold'
                size = 13
            elif line.startswith("   •"):
                color = self.colors['field_M']
                weight = 'normal'
                size = 11
            elif line.startswith("核心思想:"):
                color = self.colors['projection']
                weight = 'bold'
                size = 14
            elif line.strip().isdigit() or line.strip().startswith(tuple('12345')):
                color = self.colors['mass_m']
                weight = 'bold'
                size = 12
            else:
                color = self.colors['text']
                weight = 'normal'
                size = 11
            
            self.ax_explanation.text(0.05, y_pos, line, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 添加边框
        bbox = dict(boxstyle="round,pad=0.02", facecolor='lightyellow', alpha=0.8)
        self.ax_explanation.text(0.5, 0.02, 
                               f'帧数: {frame}/{self.total_frames}',
                               ha='center', fontsize=10, color='gray',
                               transform=self.ax_explanation.transAxes, bbox=bbox)
    
    def animate(self, frame):
        """主动画函数"""
        # 清除之前的内容并重绘
        self.draw_main_3d_view(frame)
        self.draw_side_view(frame)
        self.draw_projection_analysis(frame)
        self.draw_explanation(frame)
        
        plt.tight_layout()
    
    def create_animation(self):
        """创建动画"""
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.total_frames,
            interval=80, blit=False, repeat=True
        )
        
        return anim

def main():
    """主函数"""
    print("正在创建三维空间发散场与二维平面相互作用动画...")
    print("这将展示几何因子产生的物理原理")
    
    animator = SpaceFieldInteractionAnimator()
    anim = animator.create_animation()
    
    # 显示动画
    plt.show()
    
    # 询问是否保存
    save_option = input("\n选择保存选项:\n1. 保存为GIF\n2. 保存为MP4\n3. 不保存\n请输入选项 (1/2/3): ").strip()
    
    if save_option == '1':
        print("正在保存为GIF文件...")
        anim.save('三维发散场二维投影动画.gif', writer='pillow', fps=12, dpi=150)
        print("GIF文件已保存!")
    elif save_option == '2':
        print("正在保存为MP4文件...")
        try:
            anim.save('三维发散场二维投影动画.mp4', writer='ffmpeg', fps=15, dpi=200)
            print("MP4文件已保存!")
        except:
            print("MP4保存失败，请确保安装了ffmpeg")
    
    print("\n动画展示了:")
    print("• 质量M和m产生的球对称空间发散场")
    print("• 三维场如何投影到二维相互作用平面")
    print("• 几何因子产生的物理原理")
    print("• 从三维到二维的几何约化过程")

if __name__ == "__main__":
    main()    def
 draw_projection_analysis(self, frame):
        """绘制投影分析图 - 增强版"""
        self.ax_projection.clear()
        
        # 创建高分辨率场强分布
        x = np.linspace(-4, 4, 80)
        y = np.linspace(-4, 4, 80)
        X, Y = np.meshgrid(x, y)
        
        # M的场强分布 (1/r²)
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + Y**2) + 0.1
        field_M = 3.0 / r_M**2
        
        # m的场强分布
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + Y**2) + 0.1
        field_m = 1.5 / r_m**2
        
        # 总场强
        total_field = field_M + field_m
        
        # 绘制彩色场强分布
        im = self.ax_projection.imshow(total_field, extent=[-4, 4, -4, 4], 
                                     origin='lower', cmap='hot', alpha=0.7,
                                     vmax=np.percentile(total_field, 95))
        
        # 添加等高线
        levels = np.logspace(-0.5, 1.5, 8)
        contour = self.ax_projection.contour(X, Y, total_field, levels=levels,
                                           colors='white', alpha=0.8, linewidths=1.5)
        
        # 绘制质量位置
        self.ax_projection.scatter([self.mass_M_pos[0]], [0], s=500, 
                                 c=self.colors['mass_M'], alpha=0.9, 
                                 marker='o', edgecolors='white', linewidth=3,
                                 label='质量M', zorder=10)
        self.ax_projection.scatter([self.mass_m_pos[0]], [0], s=350,
                                 c=self.colors['mass_m'], alpha=0.9,
                                 marker='o', edgecolors='white', linewidth=3,
                                 label='质量m', zorder=10)
        
        # 动态相互作用区域
        progress = (frame % 100) / 100.0
        interaction_width = 0.5 + 0.3 * np.sin(frame * 0.1)
        
        # 相互作用区域矩形
        interaction_rect = Rectangle((-interaction_width, -interaction_width), 
                                   2*interaction_width, 2*interaction_width,
                                   fill=True, color=self.colors['highlight'], 
                                   alpha=0.3, zorder=5)
        self.ax_projection.add_patch(interaction_rect)
        
        # 相互作用箭头
        arrow_props = dict(arrowstyle='<->', color=self.colors['projection'],
                          lw=4, alpha=0.8)
        self.ax_projection.annotate('', xy=(1.5, 0), xytext=(-1.5, 0),
                                  arrowprops=arrow_props, zorder=8)
        
        # 标注
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
        """绘制场强随距离变化图"""
        self.ax_field_strength.clear()
        
        # 距离数组
        r = np.linspace(0.1, 5, 100)
        
        # 不同的场强分布
        field_1_over_r2 = 1 / r**2  # 1/r²分布
        field_1_over_r = 1 / r      # 1/r分布
        field_exp = np.exp(-r)      # 指数衰减
        
        # 绘制不同的场强曲线
        self.ax_field_strength.plot(r, field_1_over_r2, 'r-', linewidth=3, 
                                   label='1/r² (引力场)', alpha=0.8)
        self.ax_field_strength.plot(r, field_1_over_r, 'b--', linewidth=2,
                                   label='1/r (对比)', alpha=0.7)
        self.ax_field_strength.plot(r, field_exp, 'g:', linewidth=2,
                                   label='e^(-r) (指数衰减)', alpha=0.7)
        
        # 动态标记当前距离
        current_r = 2.5 + 1.5 * np.sin(frame * 0.05)
        current_field = 1 / current_r**2
        
        self.ax_field_strength.scatter([current_r], [current_field], 
                                     s=100, c=self.colors['highlight'], 
                                     zorder=10, alpha=0.9)
        self.ax_field_strength.axvline(x=current_r, color=self.colors['highlight'],
                                     linestyle='--', alpha=0.5)
        
        # 标注
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
        """绘制数学公式推导"""
        self.ax_math.clear()
        self.ax_math.axis('off')
        
        # 动态显示公式
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
            
            # 设置不同样式
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
        """绘制详细物理解释 - 终极版"""
        self.ax_explanation.clear()
        self.ax_explanation.axis('off')
        
        # 创建多列布局
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
        
        # 动态显示
        progress = frame / self.total_frames
        n_explanations = min(len(explanations), int(progress * len(explanations) * 0.8) + 1)
        n_problems = min(len(problems), max(0, int((progress - 0.3) * len(problems) * 1.2)))
        
        # 左列 - 物理概念
        y_start_left = 0.95
        line_height = 0.055
        
        for i in range(n_explanations):
            if i >= len(explanations):
                break
            text, color, weight, size = explanations[i]
            y_pos = y_start_left - i * line_height
            self.ax_explanation.text(0.02, y_pos, text, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 右列 - 问题分析
        y_start_right = 0.95
        for i in range(n_problems):
            if i >= len(problems):
                break
            text, color, weight, size = problems[i]
            y_pos = y_start_right - i * line_height
            self.ax_explanation.text(0.52, y_pos, text, fontsize=size, color=color,
                                   weight=weight, transform=self.ax_explanation.transAxes)
        
        # 添加分隔线
        self.ax_explanation.axvline(x=0.5, color=self.colors['grid'], alpha=0.3, 
                                  transform=self.ax_explanation.transAxes)
        
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
        """主动画函数 - 终极版"""
        # 绘制所有子图
        self.draw_main_3d_view(frame)
        self.draw_side_view(frame)
        self.draw_top_view(frame)
        self.draw_projection_analysis(frame)
        self.draw_field_strength_plot(frame)
        self.draw_explanation(frame)
        self.draw_mathematical_formulas(frame)
        
        # 添加全局信息
        progress_text = f'动画进度: {frame}/{self.total_frames} ({frame/self.total_frames*100:.1f}%)'
        self.fig.text(0.02, 0.02, progress_text, fontsize=10, color='gray')
        
        # 添加交互提示
        if frame < 50:
            self.fig.text(0.5, 0.02, '💡 提示：点击任意子图可单独放大查看', 
                         ha='center', fontsize=12, color=self.colors['highlight'],
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
    
    def create_animation(self):
        """创建终极版动画"""
        self.setup_figure()
        
        # 创建动画对象
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.total_frames,
            interval=100, blit=False, repeat=True
        )
        
        # 添加鼠标点击事件
        def on_click(event):
            """处理鼠标点击事件 - 放大子图"""
            if event.inaxes:
                # 创建新窗口显示放大的子图
                fig_zoom = plt.figure(figsize=(12, 10))
                ax_zoom = fig_zoom.add_subplot(111, projection='3d' if hasattr(event.inaxes, 'zaxis') else None)
                
                # 复制当前子图内容到新窗口
                if event.inaxes == self.ax_main:
                    self.draw_main_3d_view(self.total_frames // 2)
                    ax_zoom.set_title('🌌 三维空间球对称发散场 - 放大视图', fontsize=16)
                elif event.inaxes == self.ax_projection:
                    self.draw_projection_analysis(self.total_frames // 2)
                    ax_zoom.set_title('📊 二维平面场强分布 - 放大视图', fontsize=16)
                # 可以添加更多子图的放大处理
                
                plt.show()
        
        self.fig.canvas.mpl_connect('button_press_event', on_click)
        
        return anim

def main():
    """主函数 - 终极版"""
    print("🚀 正在创建三维空间发散场与二维平面相互作用的终极版动画...")
    print("✨ 新功能：")
    print("   • 超高质量3D渲染")
    print("   • 多视角同步显示")
    print("   • 交互式子图放大")
    print("   • 详细的物理原理解释")
    print("   • 几何因子问题分析")
    
    animator = SpaceFieldInteractionAnimator()
    anim = animator.create_animation()
    
    # 显示动画
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
        animator.animate(animator.total_frames // 2)  # 保存中间帧
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