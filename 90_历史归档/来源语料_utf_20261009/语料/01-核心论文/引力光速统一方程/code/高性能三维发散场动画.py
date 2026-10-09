#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高性能三维空间发散场动画 - 性能优化版
High Performance 3D Space Divergent Field Animation

优化策略：
1. 减少重复计算
2. 使用缓存机制
3. 优化渲染频率
4. 简化复杂图形
5. 内存管理优化

Author: Performance Optimization Master
Date: 2025-09-16
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
import matplotlib.gridspec as gridspec
from functools import lru_cache
import gc

# 性能优化设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 100  # 降低DPI提升性能
plt.rcParams['animation.html'] = 'html5'
plt.rcParams['animation.embed_limit'] = 50  # 限制嵌入大小

class HighPerformanceSpaceFieldAnimator:
    """高性能空间场动画器"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 200  # 减少总帧数
        self.update_interval = 120  # 更新间隔(ms)
        
        # 物理参数
        self.mass_M_pos = np.array([-2.5, 0, 0])
        self.mass_m_pos = np.array([2.5, 0, 0])
        
        # 简化色彩配置
        self.colors = {
            'mass_M': '#E74C3C',
            'mass_m': '#3498DB', 
            'field_M': '#FF6B6B',
            'field_m': '#74B9FF',
            'interaction_plane': '#2ECC71',
            'field_lines': '#F39C12',
            'projection': '#E67E22',
            'text': '#2C3E50',
            'highlight': '#9B59B6'
        }
        
        # 缓存预计算数据
        self._cache_initialized = False
        self._sphere_data = {}
        self._field_data = {}
        self._vector_data = {}
        
        # 性能监控
        self.frame_times = []
        self.last_frame_time = None
        
    def _initialize_cache(self):
        """初始化缓存数据"""
        if self._cache_initialized:
            return
            
        print("正在初始化缓存数据...")
        
        # 预计算球面数据
        self._precompute_sphere_data()
        
        # 预计算场强数据
        self._precompute_field_data()
        
        # 预计算矢量数据
        self._precompute_vector_data()
        
        self._cache_initialized = True
        print("缓存初始化完成!")
    
    @lru_cache(maxsize=32)
    def _get_sphere_mesh(self, radius, n_points=15):
        """缓存球面网格数据"""
        u = np.linspace(0, 2*np.pi, n_points)
        v = np.linspace(0, np.pi, n_points//2)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z
    
    def _precompute_sphere_data(self):
        """预计算球面数据"""
        # 为不同半径预计算球面
        radii = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        for r in radii:
            self._sphere_data[r] = self._get_sphere_mesh(r, 12)  # 减少点数
    
    def _precompute_field_data(self):
        """预计算场强分布数据"""
        # 低分辨率网格提升性能
        x = np.linspace(-4, 4, 40)  # 从80降到40
        y = np.linspace(-4, 4, 40)
        X, Y = np.meshgrid(x, y)
        
        # M的场强
        r_M = np.sqrt((X - self.mass_M_pos[0])**2 + Y**2) + 0.1
        field_M = 3.0 / r_M**2
        
        # m的场强
        r_m = np.sqrt((X - self.mass_m_pos[0])**2 + Y**2) + 0.1
        field_m = 1.5 / r_m**2
        
        self._field_data = {
            'X': X, 'Y': Y,
            'field_M': field_M,
            'field_m': field_m,
            'total_field': field_M + field_m
        }
    
    def _precompute_vector_data(self):
        """预计算矢量数据"""
        np.random.seed(42)
        n_vectors = 20  # 减少矢量数量
        
        vectors_M = []
        vectors_m = []
        
        for i in range(n_vectors):
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            
            direction = np.array([
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi)
            ])
            
            # M的矢量
            start_M = self.mass_M_pos
            end_M = self.mass_M_pos + 2.0 * direction
            vectors_M.append({'start': start_M, 'end': end_M})
            
            # m的矢量
            start_m = self.mass_m_pos
            end_m = self.mass_m_pos + 1.5 * direction
            vectors_m.append({'start': start_m, 'end': end_m})
        
        self._vector_data = {'M': vectors_M, 'm': vectors_m}
    
    def setup_figure(self):
        """设置优化的图形布局"""
        self.fig = plt.figure(figsize=(18, 12))  # 减小尺寸
        self.fig.patch.set_facecolor('#FAFAFA')
        
        # 简化布局 - 2x3网格
        gs = gridspec.GridSpec(2, 3, figure=self.fig, hspace=0.3, wspace=0.3)
        
        self.fig.suptitle('高性能三维空间发散场动画 - 几何因子原理展示', 
                         fontsize=18, fontweight='bold', y=0.95)
        
        # 创建子图
        self.ax_main = self.fig.add_subplot(gs[0, 0:2], projection='3d')
        self.ax_side = self.fig.add_subplot(gs[0, 2], projection='3d')
        self.ax_projection = self.fig.add_subplot(gs[1, 0])
        self.ax_field_strength = self.fig.add_subplot(gs[1, 1])
        self.ax_explanation = self.fig.add_subplot(gs[1, 2])
        
        return self.fig
    
    def draw_main_3d_view(self, frame):
        """优化的主3D视图"""
        # 只在必要时清除
        if frame % 5 == 0:  # 每5帧清除一次
            self.ax_main.clear()
        
        # 简化视角变化
        rotation = frame * 2  # 减慢旋转速度
        self.ax_main.view_init(elev=20, azim=rotation)
        
        # 绘制质量球体 - 使用缓存数据
        if 0.4 in self._sphere_data:
            x_M, y_M, z_M = self._sphere_data[0.4]
            x_M = x_M + self.mass_M_pos[0]
            y_M = y_M + self.mass_M_pos[1]
            z_M = z_M + self.mass_M_pos[2]
            self.ax_main.plot_surface(x_M, y_M, z_M, color=self.colors['mass_M'], 
                                    alpha=0.8, shade=False)  # 关闭阴影提升性能
        
        if 0.25 in self._sphere_data:
            x_m, y_m, z_m = self._sphere_data[0.25]
            x_m = x_m + self.mass_m_pos[0]
            y_m = y_m + self.mass_m_pos[1]
            z_m = z_m + self.mass_m_pos[2]
            self.ax_main.plot_surface(x_m, y_m, z_m, color=self.colors['mass_m'], 
                                    alpha=0.8, shade=False)
        
        # 简化发散场绘制 - 只显示几个关键球面
        key_radii = [1.0, 2.0, 3.0]
        for i, r in enumerate(key_radii):
            if r in self._sphere_data:
                x, y, z = self._sphere_data[r]
                alpha = 0.1 - i * 0.03
                if alpha > 0:
                    # M的场
                    x_M_field = x + self.mass_M_pos[0]
                    y_M_field = y + self.mass_M_pos[1]
                    z_M_field = z + self.mass_M_pos[2]
                    self.ax_main.plot_wireframe(x_M_field, y_M_field, z_M_field, 
                                              alpha=alpha, color=self.colors['field_M'], 
                                              linewidth=0.8)
                    
                    # m的场 (较小)
                    if r <= 2.0:
                        x_m_field = x * 0.7 + self.mass_m_pos[0]
                        y_m_field = y * 0.7 + self.mass_m_pos[1]
                        z_m_field = z * 0.7 + self.mass_m_pos[2]
                        self.ax_main.plot_wireframe(x_m_field, y_m_field, z_m_field,
                                                  alpha=alpha*0.8, color=self.colors['field_m'],
                                                  linewidth=0.6)
        
        # 简化相互作用平面
        xx, yy = np.meshgrid(np.linspace(-4, 4, 15), np.linspace(-3, 3, 12))
        zz = np.zeros_like(xx)
        self.ax_main.plot_surface(xx, yy, zz, alpha=0.3, 
                                color=self.colors['interaction_plane'], shade=False)
        
        # 动态矢量 - 减少数量
        if frame % 3 == 0:  # 每3帧更新一次
            vectors_M = self._vector_data['M']
            progress = (frame % 60) / 60.0
            n_visible = int(len(vectors_M) * progress)
            
            for vec in vectors_M[:n_visible]:
                self.ax_main.quiver(vec['start'][0], vec['start'][1], vec['start'][2],
                                  vec['end'][0]-vec['start'][0], 
                                  vec['end'][1]-vec['start'][1],
                                  vec['end'][2]-vec['start'][2],
                                  color=self.colors['field_lines'], alpha=0.6, 
                                  arrow_length_ratio=0.1, linewidth=1.0)
        
        # 简化标注
        self.ax_main.text(self.mass_M_pos[0], self.mass_M_pos[1], self.mass_M_pos[2]+1.2,
                         'M', fontsize=12, color=self.colors['mass_M'], 
                         ha='center', fontweight='bold')
        self.ax_main.text(self.mass_m_pos[0], self.mass_m_pos[1], self.mass_m_pos[2]+1.0,
                         'm', fontsize=11, color=self.colors['mass_m'],
                         ha='center', fontweight='bold')
        
        self.ax_main.set_title('三维球对称发散场', fontsize=14, fontweight='bold')
        self.ax_main.set_xlim([-5, 5])
        self.ax_main.set_ylim([-4, 4])
        self.ax_main.set_zlim([-3, 3])
    
    def draw_side_view(self, frame):
        """优化的侧视图"""
        if frame % 8 == 0:  # 降低更新频率
            self.ax_side.clear()
            self.ax_side.view_init(elev=0, azim=90)
            
            # 简化质量绘制
            self.ax_side.scatter([self.mass_M_pos[0]], [self.mass_M_pos[1]], [self.mass_M_pos[2]],
                               s=200, c=self.colors['mass_M'], alpha=0.8)
            self.ax_side.scatter([self.mass_m_pos[0]], [self.mass_m_pos[1]], [self.mass_m_pos[2]],
                               s=150, c=self.colors['mass_m'], alpha=0.8)
            
            # 简化平面
            xx, yy = np.meshgrid(np.linspace(-3, 3, 8), np.linspace(-2, 2, 6))
            zz = np.zeros_like(xx)
            self.ax_side.plot_surface(xx, yy, zz, alpha=0.5, 
                                    color=self.colors['interaction_plane'])
            
            # 简化投影线
            if frame % 16 < 8:  # 闪烁效果
                angles = np.linspace(0, 2*np.pi, 8)
                for angle in angles:
                    r = 1.5
                    x = self.mass_M_pos[0] + r * np.cos(angle)
                    y = self.mass_M_pos[1] + r * np.sin(angle)
                    z = self.mass_M_pos[2] + r * 0.3 * np.sin(angle)
                    
                    self.ax_side.plot([x, x], [y, y], [z, 0],
                                    color=self.colors['projection'], alpha=0.6, linewidth=1.5)
            
            self.ax_side.set_title('侧视图：投影过程', fontsize=12, fontweight='bold')
            self.ax_side.set_xlim([-3, 3])
            self.ax_side.set_ylim([-2, 2])
            self.ax_side.set_zlim([-2, 2])
    
    def draw_projection_analysis(self, frame):
        """优化的投影分析"""
        if frame % 6 == 0:  # 降低更新频率
            self.ax_projection.clear()
            
            # 使用预计算的场强数据
            X, Y = self._field_data['X'], self._field_data['Y']
            total_field = self._field_data['total_field']
            
            # 简化场强显示
            im = self.ax_projection.imshow(total_field, extent=[-4, 4, -4, 4], 
                                         origin='lower', cmap='hot', alpha=0.6,
                                         vmax=np.percentile(total_field, 90))
            
            # 简化等高线
            levels = np.logspace(-0.5, 1.0, 5)  # 减少等高线数量
            self.ax_projection.contour(X, Y, total_field, levels=levels,
                                     colors='white', alpha=0.7, linewidths=1.0)
            
            # 质量位置
            self.ax_projection.scatter([self.mass_M_pos[0]], [0], s=300, 
                                     c=self.colors['mass_M'], alpha=0.9, 
                                     marker='o', edgecolors='white', linewidth=2)
            self.ax_projection.scatter([self.mass_m_pos[0]], [0], s=200,
                                     c=self.colors['mass_m'], alpha=0.9,
                                     marker='o', edgecolors='white', linewidth=2)
            
            # 简化相互作用区域
            interaction_width = 0.8
            interaction_rect = Rectangle((-interaction_width, -interaction_width), 
                                       2*interaction_width, 2*interaction_width,
                                       fill=True, color=self.colors['highlight'], 
                                       alpha=0.2)
            self.ax_projection.add_patch(interaction_rect)
            
            self.ax_projection.set_xlim(-4, 4)
            self.ax_projection.set_ylim(-4, 4)
            self.ax_projection.set_aspect('equal')
            self.ax_projection.set_title('二维场强分布', fontsize=12, fontweight='bold')
    
    def draw_field_strength_plot(self, frame):
        """优化的场强图"""
        if frame % 10 == 0:  # 进一步降低更新频率
            self.ax_field_strength.clear()
            
            r = np.linspace(0.1, 5, 50)  # 减少数据点
            field_1_over_r2 = 1 / r**2
            
            self.ax_field_strength.plot(r, field_1_over_r2, 'r-', linewidth=2, 
                                       label='1/r² (引力场)', alpha=0.8)
            
            # 简化动态标记
            current_r = 2.5 + np.sin(frame * 0.1)
            current_field = 1 / current_r**2
            
            self.ax_field_strength.scatter([current_r], [current_field], 
                                         s=80, c=self.colors['highlight'], alpha=0.8)
            
            self.ax_field_strength.set_xlabel('距离 r')
            self.ax_field_strength.set_ylabel('场强')
            self.ax_field_strength.set_title('场强-距离关系', fontsize=12, fontweight='bold')
            self.ax_field_strength.legend()
            self.ax_field_strength.set_yscale('log')
            self.ax_field_strength.set_ylim(0.01, 100)
    
    def draw_explanation(self, frame):
        """优化的解释文本"""
        if frame % 15 == 0:  # 最低更新频率
            self.ax_explanation.clear()
            self.ax_explanation.axis('off')
            
            # 简化文本内容
            explanations = [
                "核心物理概念:",
                "",
                "质量M的发散场:",
                "• 球对称分布",
                "• F ∝ 1/r²",
                "",
                "二维相互作用平面:",
                "• 三维场→二维投影",
                "• 需要几何修正",
                "",
                "几何因子问题:",
                "• 球面积/圆周长 = 2r",
                "• 有长度量纲",
                "• 不是无量纲数",
                "",
                "正确的几何因子:",
                "• 应该无量纲",
                "• 来源于物理原理"
            ]
            
            progress = frame / self.total_frames
            n_lines = min(len(explanations), int(progress * len(explanations)) + 1)
            
            y_start = 0.95
            line_height = 0.05
            
            for i in range(n_lines):
                if i >= len(explanations):
                    break
                    
                line = explanations[i]
                y_pos = y_start - i * line_height
                
                if line.endswith(':'):
                    color = self.colors['highlight']
                    weight = 'bold'
                    size = 11
                elif line.startswith('•'):
                    color = self.colors['text']
                    weight = 'normal'
                    size = 9
                else:
                    color = self.colors['text']
                    weight = 'normal'
                    size = 10
                
                self.ax_explanation.text(0.05, y_pos, line, fontsize=size, color=color,
                                       weight=weight, transform=self.ax_explanation.transAxes)
            
            self.ax_explanation.set_title('物理原理解释', fontsize=12, fontweight='bold')
    
    def animate(self, frame):
        """优化的主动画函数"""
        import time
        start_time = time.time()
        
        # 绘制各个子图
        self.draw_main_3d_view(frame)
        self.draw_side_view(frame)
        self.draw_projection_analysis(frame)
        self.draw_field_strength_plot(frame)
        self.draw_explanation(frame)
        
        # 性能监控
        frame_time = time.time() - start_time
        self.frame_times.append(frame_time)
        
        # 显示性能信息
        if len(self.frame_times) > 10:
            avg_time = np.mean(self.frame_times[-10:])
            fps = 1.0 / avg_time if avg_time > 0 else 0
            self.fig.text(0.02, 0.02, f'FPS: {fps:.1f} | 帧时间: {frame_time*1000:.1f}ms', 
                         fontsize=9, color='gray')
        
        # 内存管理
        if frame % 50 == 0:
            gc.collect()  # 定期垃圾回收
        
        plt.tight_layout()
    
    def create_animation(self):
        """创建优化的动画"""
        self._initialize_cache()
        self.setup_figure()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.total_frames,
            interval=self.update_interval, blit=False, repeat=True
        )
        
        return anim

def main():
    """主函数"""
    print("🚀 正在创建高性能三维空间发散场动画...")
    print("⚡ 性能优化特性:")
    print("   • 数据缓存机制")
    print("   • 降低渲染频率")
    print("   • 简化图形复杂度")
    print("   • 内存管理优化")
    print("   • 实时性能监控")
    
    animator = HighPerformanceSpaceFieldAnimator()
    anim = animator.create_animation()
    
    plt.show()
    
    # 性能报告
    if animator.frame_times:
        avg_time = np.mean(animator.frame_times)
        max_time = np.max(animator.frame_times)
        min_time = np.min(animator.frame_times)
        avg_fps = 1.0 / avg_time if avg_time > 0 else 0
        
        print(f"\n📊 性能报告:")
        print(f"   平均FPS: {avg_fps:.1f}")
        print(f"   平均帧时间: {avg_time*1000:.1f}ms")
        print(f"   最大帧时间: {max_time*1000:.1f}ms")
        print(f"   最小帧时间: {min_time*1000:.1f}ms")
    
    # 保存选项
    save_option = input("\n💾 保存选项:\n1. 保存为优化GIF\n2. 保存为轻量MP4\n3. 不保存\n请选择 (1-3): ").strip()
    
    if save_option == '1':
        print("🎬 正在保存优化GIF...")
        anim.save('高性能三维发散场动画.gif', writer='pillow', fps=8, dpi=100)
        print("✅ 优化GIF已保存!")
        
    elif save_option == '2':
        print("🎥 正在保存轻量MP4...")
        try:
            anim.save('高性能三维发散场动画.mp4', writer='ffmpeg', fps=10, dpi=150, bitrate=2000)
            print("✅ 轻量MP4已保存!")
        except Exception as e:
            print(f"❌ MP4保存失败: {e}")
    
    print("\n🎯 动画优化效果:")
    print("✅ 流畅的3D渲染")
    print("✅ 高效的数据处理")
    print("✅ 优化的内存使用")
    print("✅ 实时性能监控")
    print("✅ 清晰的物理概念展示")

if __name__ == "__main__":
    main()