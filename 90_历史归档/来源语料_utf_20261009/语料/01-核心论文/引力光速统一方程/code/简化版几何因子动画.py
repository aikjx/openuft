#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版几何因子动画：3D球面到2D投影的核心变换
专注展示几何因子 G = 4π/2π = 2 的核心数学原理

核心动画内容：
1. 旋转的3D球面（4π立体角）
2. 实时投影到2D平面（2π角度）
3. 几何因子的动态计算
4. 数学公式的同步显示

作者：基于张祥前统一场论
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge
import time

# 设置显示参数
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 100

class SimpleGeometricFactorAnimation:
    """简化的几何因子动画类"""
    
    def __init__(self):
        self.fig = None
        self.total_frames = 120
        
        # 颜色配置
        self.colors = {
            'sphere': '#FF4444',
            'projection': '#44AAFF', 
            'vectors': '#44FF44',
            'highlight': '#FFAA00',
            'text': '#000000'
        }
    
    def setup_animation(self):
        """设置动画布局"""
        self.fig = plt.figure(figsize=(16, 8))
        
        # 创建子图
        self.ax_3d = self.fig.add_subplot(121, projection='3d')
        self.ax_2d = self.fig.add_subplot(122)
        
        return self.fig
    
    def create_sphere_vectors(self, n_vectors=16):
        """创建球面矢量"""
        vectors = []
        
        # 在球面上均匀分布矢量
        for i in range(n_vectors):
            for j in range(n_vectors//2):
                theta = 2 * np.pi * i / n_vectors  # 方位角
                phi = np.pi * j / (n_vectors//2)   # 极角
                
                # 球坐标转直角坐标
                x = np.sin(phi) * np.cos(theta)
                y = np.sin(phi) * np.sin(theta)
                z = np.cos(phi)
                
                vectors.append([x, y, z])
        
        return np.array(vectors)
    
    def animate_frame(self, frame):
        """主动画函数"""
        # 清除画布
        self.ax_3d.clear()
        self.ax_2d.clear()
        
        # 计算旋转角度
        rotation = frame * 3 * np.pi / self.total_frames
        
        # === 3D球面动画 ===
        self.animate_3d_sphere(frame, rotation)
        
        # === 2D投影动画 ===
        self.animate_2d_projection(frame)
        
        # === 更新标题 ===
        progress = frame / self.total_frames * 100
        self.fig.suptitle(f'几何因子动画：G = 4π/2π = 2  |  进度: {progress:.0f}%', 
                         fontsize=14, fontweight='bold')
    
    def animate_3d_sphere(self, frame, rotation):
        """动画3D球面"""
        # 创建球面
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # 绘制半透明球面
        self.ax_3d.plot_surface(x, y, z, alpha=0.2, color=self.colors['sphere'])
        
        # 绘制球面网格
        self.ax_3d.plot_wireframe(x, y, z, alpha=0.3, color='gray', linewidth=0.5)
        
        # 创建发散矢量
        vectors = self.create_sphere_vectors(12)
        
        # 动态显示矢量（旋转效果）
        for i, vec in enumerate(vectors):
            if i % 3 == 0:  # 只显示部分矢量以避免过于密集
                # 应用旋转
                x_rot = vec[0] * np.cos(rotation) - vec[1] * np.sin(rotation)
                y_rot = vec[0] * np.sin(rotation) + vec[1] * np.cos(rotation)
                z_rot = vec[2]
                
                # 矢量长度随时间变化
                scale = 1.2 + 0.3 * np.sin(frame * 0.2 + i)
                
                self.ax_3d.quiver(0, 0, 0, x_rot*scale, y_rot*scale, z_rot*scale,
                                 color=self.colors['vectors'], alpha=0.8, 
                                 arrow_length_ratio=0.1, linewidth=2)
        
        # 突出显示赤道平面（投影平面）
        theta_plane = np.linspace(0, 2*np.pi, 50)
        x_plane = 1.5 * np.cos(theta_plane)
        y_plane = 1.5 * np.sin(theta_plane)
        z_plane = np.zeros_like(x_plane)
        
        self.ax_3d.plot(x_plane, y_plane, z_plane, 
                       color=self.colors['projection'], linewidth=3, alpha=0.8)
        
        # 设置3D图属性
        self.ax_3d.set_xlim([-2, 2])
        self.ax_3d.set_ylim([-2, 2])
        self.ax_3d.set_zlim([-2, 2])
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.set_title('3D球对称空间\n总立体角 = 4π 立体弧度', fontweight='bold')
        
        # 动态视角
        self.ax_3d.view_init(elev=20 + 10*np.sin(frame*0.1), azim=frame*2)
    
    def animate_2d_projection(self, frame):
        """动画2D投影"""
        # 绘制单位圆
        circle = Circle((0, 0), 1, fill=False, color=self.colors['sphere'], 
                       linewidth=3)
        self.ax_2d.add_patch(circle)
        
        # 计算投影进度
        projection_progress = (np.sin(frame * 0.1) + 1) / 2  # 0到1之间振荡
        
        # 绘制动态投影区域
        if projection_progress > 0:
            theta_max = np.pi * projection_progress
            theta = np.linspace(0, theta_max, 100)
            x_proj = np.cos(theta)
            y_proj = np.sin(theta)
            
            # 填充投影区域
            self.ax_2d.fill_between(x_proj, 0, y_proj, alpha=0.4, 
                                  color=self.colors['projection'])
            
            # 绘制投影矢量
            n_rays = max(1, int(12 * projection_progress))
            for i in range(n_rays):
                angle = theta_max * i / max(1, n_rays-1) if n_rays > 1 else 0
                x_end = np.cos(angle)
                y_end = np.sin(angle)
                
                # 矢量颜色渐变
                alpha = 1 - (angle / np.pi) * 0.5
                self.ax_2d.arrow(0, 0, x_end, y_end, 
                               head_width=0.04, head_length=0.04,
                               fc=self.colors['vectors'], ec=self.colors['vectors'],
                               alpha=alpha, linewidth=1.5)
        
        # 绘制角度弧
        if projection_progress > 0.1:
            angle_deg = projection_progress * 180
            wedge = Wedge((0, 0), 0.3, 0, angle_deg, 
                         facecolor=self.colors['highlight'], alpha=0.6)
            self.ax_2d.add_patch(wedge)
            
            # 角度标签
            mid_angle = np.pi * projection_progress / 2
            label_x = 0.4 * np.cos(mid_angle)
            label_y = 0.4 * np.sin(mid_angle)
            self.ax_2d.text(label_x, label_y, f'{projection_progress*2:.1f}π', 
                          fontsize=12, color='red', fontweight='bold', ha='center')
        
        # 显示几何因子计算
        geometric_factor = 4 * np.pi / (2 * np.pi) if projection_progress > 0.5 else 0
        if geometric_factor > 0:
            self.ax_2d.text(0.02, 0.98, f'几何因子 G = 4π/2π = {geometric_factor:.1f}', 
                          transform=self.ax_2d.transAxes, fontsize=12, 
                          fontweight='bold', color='red',
                          bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
        
        # 显示当前投影角度
        current_angle = projection_progress * 2 * np.pi
        self.ax_2d.text(0.02, 0.02, f'当前投影角: {current_angle:.2f} 弧度\n= {projection_progress*2:.1f}π', 
                      transform=self.ax_2d.transAxes, fontsize=10, 
                      bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.7))
        
        # 设置2D图属性
        self.ax_2d.set_xlim([-1.3, 1.3])
        self.ax_2d.set_ylim([-0.3, 1.3])
        self.ax_2d.set_aspect('equal')
        self.ax_2d.grid(True, alpha=0.3)
        self.ax_2d.set_title('2D投影结果\n投影角度 = 2π 弧度', fontweight='bold')
        self.ax_2d.set_xlabel('X')
        self.ax_2d.set_ylabel('Y')
    
    def create_animation(self, interval=80):
        """创建动画"""
        # 设置图形
        self.setup_animation()
        
        # 创建动画对象
        anim = animation.FuncAnimation(
            self.fig, self.animate_frame, frames=self.total_frames,
            interval=interval, blit=False, repeat=True
        )
        
        return anim
    
    def save_animation(self, filename='几何因子动画.gif', fps=12):
        """保存动画为GIF"""
        anim = self.create_animation()
        print(f"正在保存动画为 {filename}...")
        anim.save(filename, writer='pillow', fps=fps, dpi=100)
        print(f"动画已保存！")
        return anim

def create_mathematical_summary():
    """创建数学总结图"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('张祥前统一场论：几何因子数学推导总结', fontsize=16, fontweight='bold')
    
    # 1. 3D立体角
    ax1 = axes[0, 0]
    ax1.text(0.5, 0.7, '3D球面立体角', fontsize=14, ha='center', fontweight='bold')
    ax1.text(0.5, 0.5, r'$\Omega_{3D} = 4\pi$ 立体弧度', fontsize=12, ha='center')
    ax1.text(0.5, 0.3, '球面总面积 = 4πr^2\n单位球面积 = 4π', fontsize=10, ha='center')
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    ax1.axis('off')
    
    # 2. 2D投影角
    ax2 = axes[0, 1]
    ax2.text(0.5, 0.7, '2D投影角度', fontsize=14, ha='center', fontweight='bold')
    ax2.text(0.5, 0.5, r'$\Omega_{2D} = 2\pi$ 弧度', fontsize=12, ha='center')
    ax2.text(0.5, 0.3, '半圆周长 = πr\n单位半圆 = π\n完整投影 = 2π', fontsize=10, ha='center')
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])
    ax2.axis('off')
    
    # 3. 积分推导
    ax3 = axes[1, 0]
    theta = np.linspace(0, np.pi, 1000)
    sin_squared = np.sin(theta) ** 2
    ax3.plot(theta, sin_squared, 'r-', linewidth=2, label=r'$\sin^2(\theta)$')
    ax3.fill_between(theta, 0, sin_squared, alpha=0.3, color='red')
    ax3.set_xlabel(r'$\theta$ (弧度)')
    ax3.set_ylabel(r'$\sin^2(\theta)$')
    ax3.set_title(r'积分: $\int_0^{\pi} \sin^2(\theta) d\theta = \frac{\pi}{2}$')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # 4. 几何因子
    ax4 = axes[1, 1]
    ax4.text(0.5, 0.8, '几何因子', fontsize=16, ha='center', fontweight='bold')
    ax4.text(0.5, 0.6, r'$G = \frac{\Omega_{3D}}{\Omega_{2D}} = \frac{4\pi}{2\pi} = 2$', 
             fontsize=14, ha='center', color='red', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
    ax4.text(0.5, 0.4, '物理意义：\n三维球对称场投影到\n二维平面的缩放因子', 
             fontsize=11, ha='center')
    ax4.text(0.5, 0.2, '张祥前统一场论：\n空间发散运动的几何效应', 
             fontsize=10, ha='center', style='italic')
    ax4.set_xlim([0, 1])
    ax4.set_ylim([0, 1])
    ax4.axis('off')
    
    plt.tight_layout()
    return fig

def main():
    """主函数"""
    print("=" * 50)
    print("几何因子动画可视化")
    print("张祥前统一场论：G = 4π/2π = 2")
    print("=" * 50)
    
    # 创建动画
    animator = SimpleGeometricFactorAnimation()
    
    print("正在创建动画...")
    anim = animator.create_animation(interval=100)
    
    # 创建数学总结
    summary_fig = create_mathematical_summary()
    
    print("动画创建完成！")
    print("- 左侧：3D球对称空间发散场（4π立体角）")
    print("- 右侧：2D投影结果（2π角度）")
    print("- 几何因子：G = 4π/2π = 2")
    
    # 保存图像
    summary_fig.savefig('几何因子数学总结.png', dpi=300, bbox_inches='tight')
    print("数学总结图已保存为: 几何因子数学总结.png")
    
    # 显示动画
    plt.show()
    
    return animator, anim

if __name__ == "__main__":
    animator, animation_obj = main()