#!/usr/bin/env python3
"""
为统一场论核心论文创建顶尖科学图片
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, PathPatch
import matplotlib.path as mpath
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置全局样式
plt.rcParams.update({
    'font.size': 14,
    'font.weight': 'bold',
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'axes.titleweight': 'bold',
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.figsize': (12, 8),
    'savefig.dpi': 300,
    'savefig.format': 'png',
    'savefig.bbox': 'tight',
    'savefig.transparent': False,
    'savefig.facecolor': 'white',
})

# 创建自定义配色方案
cmap_blue = cm.get_cmap('Blues', 10)
cmap_purple = cm.get_cmap('Purples', 10)
cmap_green = cm.get_cmap('Greens', 10)
cmap_red = cm.get_cmap('Reds', 10)

# 1. 空间圆柱状螺旋运动示意图
def create_spiral_motion():
    """创建空间圆柱状螺旋运动示意图"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 生成螺旋线数据
    t = np.linspace(0, 8 * np.pi, 500)
    r = 2  # 螺旋半径
    h = 0.5  # 螺距系数
    x = r * np.cos(t)
    y = r * np.sin(t)
    z = h * t
    
    # 绘制多条螺旋线，模拟空间中多个几何点的运动
    for i in range(5):
        phase = i * 2 * np.pi / 5
        x_i = r * np.cos(t + phase)
        y_i = r * np.sin(t + phase)
        z_i = h * t
        ax.plot(x_i, y_i, z_i, linewidth=2, alpha=0.8, color=cmap_blue(i / 5))
    
    # 绘制中心物体
    ax.scatter(0, 0, max(z)/2, s=800, color='red', alpha=0.9, edgecolor='black', linewidth=2)
    
    # 绘制坐标轴
    ax.set_xlabel('X 轴', fontsize=16, fontweight='bold')
    ax.set_ylabel('Y 轴', fontsize=16, fontweight='bold')
    ax.set_zlabel('Z 轴', fontsize=16, fontweight='bold')
    
    # 设置标题
    ax.set_title('空间圆柱状螺旋运动示意图', fontsize=20, fontweight='bold', pad=20)
    
    # 添加注释
    ax.text(0, 0, max(z) + 2, r'物体', fontsize=14, ha='center', color='red', fontweight='bold')
    ax.text(3, 3, max(z)/2, r'空间几何点的螺旋运动', fontsize=14, color='blue', fontweight='bold')
    
    # 添加公式
    ax.text2D(0.05, 0.95, r'$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$', 
              transform=ax.transAxes, fontsize=16, color='black', fontweight='bold')
    ax.text2D(0.05, 0.90, r'满足 $h^2 + (r\omega)^2 = c^2$', 
              transform=ax.transAxes, fontsize=14, color='black')
    
    # 设置视角
    ax.view_init(elev=30, azim=45)
    
    # 保存图片
    plt.savefig('空间圆柱状螺旋运动示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. 时空同一化原理示意图
def create_spacetime_unification():
    """创建时空同一化原理示意图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左侧：传统时空观
    ax1.set_title('传统时空观', fontsize=18, fontweight='bold')
    ax1.set_xlabel('空间', fontsize=16, fontweight='bold')
    ax1.set_ylabel('时间', fontsize=16, fontweight='bold')
    
    # 绘制传统时空图
    ax1.plot([0, 5], [0, 0], 'b-', linewidth=2, label='空间轴')
    ax1.plot([0, 0], [0, 5], 'r-', linewidth=2, label='时间轴')
    ax1.plot([0, 4], [0, 3], 'g--', linewidth=2, label='物体运动')
    ax1.scatter(2, 1.5, s=100, color='black')
    ax1.annotate('事件点', xy=(2, 1.5), xytext=(2.5, 2), arrowprops=dict(facecolor='black', shrink=0.05))
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 右侧：统一场论时空观
    ax2.set_title('统一场论时空观', fontsize=18, fontweight='bold')
    ax2.set_xlabel('空间位移', fontsize=16, fontweight='bold')
    ax2.set_ylabel('空间位移', fontsize=16, fontweight='bold')
    
    # 绘制时空同一化图
    ax2.plot([0, 5], [0, 0], 'b-', linewidth=2, label='X方向空间')
    ax2.plot([0, 0], [0, 5], 'g-', linewidth=2, label='Y方向空间')
    ax2.plot([0, 5], [0, 5], 'r-', linewidth=3, label='时空同一化')
    ax2.scatter(3, 3, s=150, color='red', alpha=0.8)
    ax2.annotate(r'$\vec{r}(t) = \vec{C}t$', xy=(3, 3), xytext=(3.5, 3.5), 
                 arrowprops=dict(facecolor='red', shrink=0.05), fontsize=14, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 添加说明文字
    fig.text(0.5, 0.01, '统一场论认为：时间不是独立维度，而是空间位移的度量', 
             ha='center', fontsize=16, fontweight='bold', color='darkred')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('时空同一化原理示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. 质量的几何化定义示意图
def create_mass_geometry():
    """创建质量的几何化定义示意图"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    
    # 绘制中心物体
    center = Circle((0, 0), 0.5, color='red', alpha=0.9, edgecolor='black', linewidth=2)
    ax.add_patch(center)
    ax.text(0, 0, '物体', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # 绘制透明球体（立体角）
    sphere = Circle((0, 0), 5, color='green', alpha=0.1, edgecolor='black', linestyle='--', linewidth=1)
    ax.add_patch(sphere)
    ax.text(5.2, 0, r'立体角 $\Omega$', ha='left', va='center', fontsize=14, color='green')
    
    # 绘制空间位移线
    for i in range(30):
        angle = i * 2 * np.pi / 30
        x = 5 * np.cos(angle)
        y = 5 * np.sin(angle)
        arrow = FancyArrowPatch(
            (0, 0), (x, y),
            arrowstyle='->',
            lw=2,
            color=cmap_blue(i / 30),
            alpha=0.7
        )
        ax.add_patch(arrow)
    
    # 绘制无限小立体角
    theta = np.pi / 6
    r = 5
    arc = PathPatch(mpath.Path([(0, 0), (r*np.cos(theta), r*np.sin(theta)), (r, 0), (0, 0)]), 
                   color='purple', alpha=0.2, edgecolor='purple', linewidth=2)
    ax.add_patch(arc)
    ax.text(r*np.cos(theta/2), r*np.sin(theta/2), r'$d\Omega$', fontsize=14, color='purple', fontweight='bold')
    
    # 设置坐标轴
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.set_xlabel('X 方向', fontsize=16, fontweight='bold')
    ax.set_ylabel('Y 方向', fontsize=16, fontweight='bold')
    ax.set_title('质量的几何化定义示意图', fontsize=20, fontweight='bold', pad=20)
    
    # 添加公式
    ax.text(0.05, 0.95, r'$m = k \cdot \frac{dn}{d\Omega}$', transform=ax.transAxes, 
            fontsize=20, color='black', fontweight='bold')
    ax.text(0.05, 0.90, r'$m$: 质量, $k$: 量子比例常数, $dn$: 空间位移矢量条数, $d\Omega$: 立体角元', 
            transform=ax.transAxes, fontsize=12, color='black')
    
    # 添加说明
    ax.text(0.05, 0.1, '质量是单位立体角内空间位移矢量的条数密度', 
            transform=ax.transAxes, fontsize=14, color='darkred', fontweight='bold')
    
    # 保存图片
    plt.savefig('质量的几何化定义示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. 双重对称性约束示意图
def create_double_symmetry():
    """创建双重对称性约束示意图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左侧：空间各向同性（4π对称性）
    ax1.set_title('空间各向同性（4π）', fontsize=18, fontweight='bold')
    ax1.set_xlabel('X 方向', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Y 方向', fontsize=16, fontweight='bold')
    ax1.set_aspect('equal')
    
    # 绘制球体
    circle = Circle((0, 0), 4, color='blue', alpha=0.1, edgecolor='blue', linewidth=2)
    ax1.add_patch(circle)
    
    # 绘制多条从中心出发的射线
    for i in range(20):
        angle = i * 2 * np.pi / 20
        x = 4 * np.cos(angle)
        y = 4 * np.sin(angle)
        ax1.plot([0, x], [0, y], 'b-', alpha=0.6, linewidth=1.5)
    
    ax1.text(0, 0, '物体', ha='center', va='center', fontsize=14, fontweight='bold', color='red')
    ax1.scatter(0, 0, s=100, color='red')
    
    # 右侧：螺旋运动对称性（4π）
    ax2.set_title('螺旋运动对称性（4π）', fontsize=18, fontweight='bold')
    ax2.set_xlabel('角度', fontsize=16, fontweight='bold')
    ax2.set_ylabel('螺旋参数', fontsize=16, fontweight='bold')
    
    # 绘制螺旋运动的周期对称性
    theta = np.linspace(0, 4 * np.pi, 200)
    y = np.sin(theta)
    ax2.plot(theta, y, 'r-', linewidth=3, alpha=0.8)
    ax2.axvline(x=2*np.pi, color='black', linestyle='--', alpha=0.5)
    ax2.axvline(x=4*np.pi, color='black', linestyle='--', alpha=0.5)
    ax2.annotate('周期：2π', xy=(2*np.pi, 0), xytext=(2*np.pi+0.5, 0.5), 
                 arrowprops=dict(facecolor='black', shrink=0.05))
    ax2.annotate('双重周期：4π', xy=(4*np.pi, 0), xytext=(4*np.pi-1.5, 0.5), 
                 arrowprops=dict(facecolor='black', shrink=0.05))
    ax2.grid(True, alpha=0.3)
    
    # 底部：双重对称性约束结果
    fig.text(0.5, 0.02, r'双重对称性约束：$k = 4\pi m_p$', 
             ha='center', fontsize=20, fontweight='bold', color='purple')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('双重对称性约束示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. 万有引力常数的量子几何表达式示意图
def create_gravitational_constant():
    """创建万有引力常数的量子几何表达式示意图"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # 设置标题
    ax.set_title('万有引力常数的量子几何表达式', fontsize=22, fontweight='bold', pad=30)
    
    # 绘制核心公式
    ax.text(0.5, 0.6, r'$G = \frac{16\pi^2 \hbar c}{k^2}$', 
            ha='center', va='center', fontsize=48, fontweight='bold', color='purple')
    
    # 绘制公式分解
    ax.text(0.25, 0.45, r'$G$: 万有引力常数', fontsize=16, ha='center', color='blue')
    ax.text(0.5, 0.45, r'$16\pi^2$: 双重对称性因子', fontsize=16, ha='center', color='red')
    ax.text(0.75, 0.45, r'$\hbar$: 约化普朗克常数', fontsize=16, ha='center', color='green')
    
    ax.text(0.33, 0.35, r'$c$: 光速', fontsize=16, ha='center', color='orange')
    ax.text(0.67, 0.35, r'$k$: 量子比例常数', fontsize=16, ha='center', color='brown')
    
    # 绘制等价关系
    ax.text(0.5, 0.25, r'等价于量子引力标准形式：', fontsize=18, ha='center', color='black')
    ax.text(0.5, 0.15, r'$G = \frac{\hbar c}{m_p^2}$', 
            ha='center', fontsize=24, fontweight='bold', color='blue')
    
    # 绘制涌现本质说明
    ax.text(0.5, 0.05, r'万有引力常数 $G$ 是由量子力学、相对论和量子引力尺度共同涌现的物理量', 
            ha='center', fontsize=16, color='darkred', fontweight='bold')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('万有引力常数的量子几何表达式.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. 量子力学的几何诠释示意图
def create_quantum_geometry():
    """创建量子力学的几何诠释示意图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左侧：波粒二象性的几何解释
    ax1.set_title('波粒二象性的几何解释', fontsize=18, fontweight='bold')
    ax1.set_xlabel('位置', fontsize=16, fontweight='bold')
    ax1.set_ylabel('空间波强度', fontsize=16, fontweight='bold')
    
    # 绘制粒子
    ax1.scatter(5, 0, s=200, color='red', edgecolor='black', label='粒子')
    
    # 绘制空间波
    x = np.linspace(0, 10, 200)
    wave = np.sin(2 * np.pi * x / 2)
    ax1.plot(x, wave, 'b-', linewidth=2, label='空间波')
    
    # 绘制双缝
    ax1.plot([3, 3], [-1.5, 1.5], 'k-', linewidth=3)
    ax1.plot([3, 3], [-0.5, 0.5], 'w-', linewidth=3)
    ax1.plot([7, 7], [-1.5, 1.5], 'k-', linewidth=3)
    ax1.plot([7, 7], [-0.5, 0.5], 'w-', linewidth=3)
    ax1.text(3, -1.8, '缝1', ha='center')
    ax1.text(7, -1.8, '缝2', ha='center')
    
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-2, 2)
    
    # 右侧：不确定性原理的几何解释
    ax2.set_title('不确定性原理的几何解释', fontsize=18, fontweight='bold')
    ax2.set_xlabel('位置确定度', fontsize=16, fontweight='bold')
    ax2.set_ylabel('动量确定度', fontsize=16, fontweight='bold')
    
    # 绘制不确定性关系
    x = np.linspace(0.1, 10, 100)
    y = 1 / x
    ax2.plot(x, y, 'r-', linewidth=3, label=r'$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$')
    ax2.fill_between(x, y, 10, alpha=0.2, color='red')
    
    # 绘制几何解释
    ax2.scatter(2, 0.5, s=150, color='blue', label='确定的位置')
    ax2.scatter(0.5, 2, s=150, color='green', label='确定的动量')
    ax2.scatter(5, 0.2, s=150, color='purple', label='不确定的位置')
    ax2.scatter(0.2, 5, s=150, color='orange', label='不确定的动量')
    
    ax2.legend(fontsize=12, loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    
    # 底部说明
    fig.text(0.5, 0.01, '统一场论将量子现象还原为空间的光速螺旋运动', 
             ha='center', fontsize=18, fontweight='bold', color='darkred')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('量子力学的几何诠释示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

# 7. 统一场论框架下的引力与量子力学统一示意图
def create_unified_framework():
    """创建统一场论框架下的引力与量子力学统一示意图"""
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # 设置标题
    ax.set_title('统一场论框架下的引力与量子力学统一', fontsize=24, fontweight='bold', pad=40)
    
    # 绘制中心概念
    center_circle = Circle((0.5, 0.5), 0.3, color='yellow', alpha=0.3, edgecolor='black', linewidth=3)
    ax.add_patch(center_circle)
    ax.text(0.5, 0.5, '空间几何运动', ha='center', va='center', fontsize=22, fontweight='bold')
    
    # 绘制分支概念
    # 1. 引力
    gravity_circle = Circle((0.2, 0.8), 0.15, color='blue', alpha=0.3, edgecolor='black', linewidth=2)
    ax.add_patch(gravity_circle)
    ax.text(0.2, 0.8, '引力', ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(0.2, 0.72, r'$G = \frac{16\pi^2 \hbar c}{k^2}$', ha='center', fontsize=14, color='blue')
    
    # 2. 相对论
    relativity_circle = Circle((0.8, 0.8), 0.15, color='green', alpha=0.3, edgecolor='black', linewidth=2)
    ax.add_patch(relativity_circle)
    ax.text(0.8, 0.8, '相对论', ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(0.8, 0.72, r'$\vec{r}(t) = \vec{C}t$', ha='center', fontsize=14, color='green')
    
    # 3. 量子力学
    quantum_circle = Circle((0.2, 0.2), 0.15, color='red', alpha=0.3, edgecolor='black', linewidth=2)
    ax.add_patch(quantum_circle)
    ax.text(0.2, 0.2, '量子力学', ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(0.2, 0.12, '几何化诠释', ha='center', fontsize=14, color='red')
    
    # 4. 质量
    mass_circle = Circle((0.8, 0.2), 0.15, color='purple', alpha=0.3, edgecolor='black', linewidth=2)
    ax.add_patch(mass_circle)
    ax.text(0.8, 0.2, '质量', ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(0.8, 0.12, r'$m = k \cdot \frac{dn}{d\Omega}$', ha='center', fontsize=14, color='purple')
    
    # 绘制连接箭头
    # 中心到引力
    arrow1 = FancyArrowPatch((0.5, 0.5+0.3*np.sin(np.pi/4)), (0.2+0.15*np.sin(3*np.pi/4), 0.8-0.15*np.cos(3*np.pi/4)),
                           arrowstyle='->', lw=3, color='black', alpha=0.7)
    ax.add_patch(arrow1)
    
    # 中心到相对论
    arrow2 = FancyArrowPatch((0.5, 0.5+0.3*np.sin(np.pi/4)), (0.8-0.15*np.sin(np.pi/4), 0.8-0.15*np.cos(np.pi/4)),
                           arrowstyle='->', lw=3, color='black', alpha=0.7)
    ax.add_patch(arrow2)
    
    # 中心到量子力学
    arrow3 = FancyArrowPatch((0.5, 0.5-0.3*np.sin(np.pi/4)), (0.2+0.15*np.sin(5*np.pi/4), 0.2+0.15*np.cos(5*np.pi/4)),
                           arrowstyle='->', lw=3, color='black', alpha=0.7)
    ax.add_patch(arrow3)
    
    # 中心到质量
    arrow4 = FancyArrowPatch((0.5, 0.5-0.3*np.sin(np.pi/4)), (0.8-0.15*np.sin(7*np.pi/4), 0.2+0.15*np.cos(7*np.pi/4)),
                           arrowstyle='->', lw=3, color='black', alpha=0.7)
    ax.add_patch(arrow4)
    
    # 绘制核心公设
    ax.text(0.5, 0.05, '核心公设：空间螺旋运动、时空同一化、物理量几何化、双重对称性约束', 
            ha='center', fontsize=16, color='darkred', fontweight='bold')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('统一场论框架下的引力与量子力学统一.png', dpi=300, bbox_inches='tight')
    plt.close()

# 8. G与c的关系图
def create_g_c_relationship():
    """创建G与c的关系图"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    
    # 设置标题
    ax.set_title('万有引力常数G与光速c的关系', fontsize=22, fontweight='bold', pad=20)
    
    # 生成数据
    c_values = np.linspace(1e8, 4e8, 100)  # 光速范围
    hbar = 1.054571817e-34  # 约化普朗克常数
    k = 2.734988e-7  # 量子比例常数
    G_values = (16 * np.pi**2 * hbar * c_values) / (k**2)
    
    # 绘制关系曲线
    ax.plot(c_values, G_values, 'r-', linewidth=3, label=r'$G = \frac{16\pi^2 \hbar c}{k^2}$')
    
    # 标记当前光速对应的G值
    c_current = 299792458  # 当前光速
    G_current = (16 * np.pi**2 * hbar * c_current) / (k**2)
    ax.scatter(c_current, G_current, s=200, color='blue', edgecolor='black', label=f'当前值: c={c_current:.2e} m/s, G={G_current:.2e} m³·kg⁻¹·s⁻²')
    
    # 设置坐标轴
    ax.set_xlabel('光速 c (m/s)', fontsize=16, fontweight='bold')
    ax.set_ylabel('万有引力常数 G (m³·kg⁻¹·s⁻²)', fontsize=16, fontweight='bold')
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    # 添加图例
    ax.legend(fontsize=12)
    
    # 添加说明
    ax.text(0.05, 0.95, r'G 与 c 成正比关系：$G \propto c$', 
            transform=ax.transAxes, fontsize=18, color='darkred', fontweight='bold')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig('万有引力常数与光速的关系.png', dpi=300, bbox_inches='tight')
    plt.close()

# 主函数
def main():
    """生成所有图片"""
    print("正在生成顶尖科学图片...")
    
    # 生成各个图片
    create_spiral_motion()
    print("✓ 空间圆柱状螺旋运动示意图")
    
    create_spacetime_unification()
    print("✓ 时空同一化原理示意图")
    
    create_mass_geometry()
    print("✓ 质量的几何化定义示意图")
    
    create_double_symmetry()
    print("✓ 双重对称性约束示意图")
    
    create_gravitational_constant()
    print("✓ 万有引力常数的量子几何表达式.png")
    
    create_quantum_geometry()
    print("✓ 量子力学的几何诠释示意图")
    
    create_unified_framework()
    print("✓ 统一场论框架下的引力与量子力学统一.png")
    
    create_g_c_relationship()
    print("✓ 万有引力常数与光速的关系.png")
    
    print("\n所有图片生成完成！")
    print("图片已保存到当前目录。")

if __name__ == "__main__":
    main()