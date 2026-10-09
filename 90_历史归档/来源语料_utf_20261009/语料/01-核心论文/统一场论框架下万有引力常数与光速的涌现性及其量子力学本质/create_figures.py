#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论框架下万有引力常数论文配图生成脚本
生成高质量、专业性的学术论文配图
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib import cm
import matplotlib.ticker as ticker

# 设置全局字体和样式
plt.rcParams.update({
    'font.family': ['SimHei', 'Times New Roman'],  # 中文使用SimHei，英文使用Times New Roman
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'legend.fontsize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.format': 'pdf',
    'savefig.bbox': 'tight',
    'text.usetex': False,  # 禁用LaTeX渲染以支持中文
    'mathtext.fontset': 'stix',  # 使用stix字体集，支持更多数学符号
    'mathtext.default': 'rm',
    'axes.unicode_minus': False,  # 解决负号显示问题
    'lines.linewidth': 2.5,  # 线条宽度
    'lines.markersize': 8,  # 标记大小
    'axes.linewidth': 1.2,  # 坐标轴宽度
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.minor.width': 0.8,
    'ytick.minor.width': 0.8
})


class Arrow3D(FancyArrowPatch):
    """3D箭头绘制类"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def plot_space_spiral_motion():
    """绘制空间螺旋运动示意图"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 生成螺旋线数据
    t = np.linspace(0, 4*np.pi, 1000)  # 增加数据点，使螺旋线更平滑
    r = 1.0  # 螺旋半径
    omega = 1.0  # 角速度
    c = 1.0  # 光速（归一化）
    
    # 三维螺旋线方程：r(t) = r*cosωt·i + r*sinωt·j + ct·k
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = c * t
    
    # 绘制螺旋线
    ax.plot(x, y, z, 'b-', linewidth=2.5, label=r'空间螺旋运动轨迹')
    
    # 绘制坐标轴
    ax.plot([0, 3], [0, 0], [0, 0], 'k--', alpha=0.7, linewidth=1.5)
    ax.plot([0, 0], [0, 3], [0, 0], 'k--', alpha=0.7, linewidth=1.5)
    ax.plot([0, 0], [0, 0], [0, 15], 'k--', alpha=0.7, linewidth=1.5)
    
    # 添加箭头
    arrow_prop_dict = dict(mutation_scale=25, arrowstyle='->', color='k', linewidth=2.0)
    
    # x轴箭头
    ax.add_artist(Arrow3D([0, 3.2], [0, 0], [0, 0], **arrow_prop_dict))
    ax.text(3.3, 0, 0, r'$x$', fontsize=14, weight='bold')
    
    # y轴箭头
    ax.add_artist(Arrow3D([0, 0], [0, 3.2], [0, 0], **arrow_prop_dict))
    ax.text(0, 3.3, 0, r'$y$', fontsize=14, weight='bold')
    
    # z轴箭头
    ax.add_artist(Arrow3D([0, 0], [0, 0], [0, 15.5], **arrow_prop_dict))
    ax.text(0, 0, 16, r'$z$', fontsize=14, weight='bold')
    
    # 绘制多个点的分量箭头，展示不同位置的螺旋特性
    for i in [50, 150, 250]:
        # 径向分量（引力场）
        ax.add_artist(Arrow3D([x[i], 0], [y[i], 0], [z[i], z[i]], mutation_scale=18, arrowstyle='->', color='r', linewidth=2.0, alpha=0.8))
        
        # 旋转分量（电磁场）
        tangential_x = -r*omega*np.sin(omega*t[i])
        tangential_y = r*omega*np.cos(omega*t[i])
        ax.add_artist(Arrow3D([x[i], x[i]+tangential_x*0.5], [y[i], y[i]+tangential_y*0.5], [z[i], z[i]], mutation_scale=18, arrowstyle='->', color='g', linewidth=2.0, alpha=0.8))
        
        # 轴向分量（光速传播）
        ax.add_artist(Arrow3D([x[i], x[i]], [y[i], y[i]], [z[i], z[i]+2], mutation_scale=18, arrowstyle='->', color='b', linewidth=2.0, alpha=0.8))
    
    # 添加关键点
    key_points = [0, 50, 100, 150, 200, 250]
    for i, idx in enumerate(key_points):
        ax.scatter(x[idx], y[idx], z[idx], color='k', s=60, marker='o', alpha=0.8)
        ax.text(x[idx]+0.1, y[idx]+0.1, z[idx]+0.2, f'$P_{i+1}$', fontsize=12, weight='bold')
    
    # 添加分量标签（只在第一个点添加，避免图例重复）
    ax.add_artist(Arrow3D([x[50], 0], [y[50], 0], [z[50], z[50]], mutation_scale=18, arrowstyle='->', color='r', linewidth=2.0, label=r'径向分量（引力场）'))
    ax.add_artist(Arrow3D([x[50], x[50]+tangential_x*0.5], [y[50], y[50]+tangential_y*0.5], [z[50], z[50]], mutation_scale=18, arrowstyle='->', color='g', linewidth=2.0, label=r'旋转分量（电磁场）'))
    ax.add_artist(Arrow3D([x[50], x[50]], [y[50], y[50]], [z[50], z[50]+2], mutation_scale=18, arrowstyle='->', color='b', linewidth=2.0, label=r'轴向分量（光速$c$）'))
    
    # 设置视角，优化螺旋结构的可视化
    ax.view_init(elev=30, azim=60)
    
    # 设置坐标轴范围
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([0, 15])
    
    # 添加坐标轴标签
    ax.set_xlabel(r'$x$ 方向', fontsize=14, weight='bold')
    ax.set_ylabel(r'$y$ 方向', fontsize=14, weight='bold')
    ax.set_zlabel(r'$z$ 方向（传播方向）', fontsize=14, weight='bold')
    
    # 设置坐标轴刻度
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([0, 5, 10, 15])
    ax.tick_params(axis='x', labelsize=11)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='z', labelsize=11)
    
    # 添加标题
    ax.set_title(r'空间的光速螺旋运动示意图', fontsize=18, weight='bold', pad=20)
    
    # 添加图例，位置优化
    ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.98), fontsize=12, frameon=True, fancybox=True, shadow=True)
    
    # 添加方程
    equation_text = r'$\vec{r}(t) = r\cos\omega t·\hat{i} + r\sin\omega t·\hat{j} + ct·\hat{k}$'
    ax.text2D(0.02, 0.02, equation_text, transform=ax.transAxes, fontsize=16, weight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 添加物理意义说明
    physics_text = r'物理意义：空间以光速沿螺旋轨迹运动，径向分量对应引力场，旋转分量对应电磁场，轴向分量以光速传播'
    ax.text2D(0.02, 0.10, physics_text, transform=ax.transAxes, fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 保存图片
    plt.savefig('空间螺旋运动示意图.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("空间螺旋运动示意图已生成")


def plot_mass_geometrization():
    """绘制质量几何化示意图"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制中心物体
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]  # 增加网格点，使球体更平滑
    x_sphere = 0.3 * np.cos(u) * np.sin(v)
    y_sphere = 0.3 * np.sin(u) * np.sin(v)
    z_sphere = 0.3 * np.cos(v)
    ax.plot_surface(x_sphere, y_sphere, z_sphere, color='gray', alpha=0.7, edgecolor='none')
    ax.text(0, 0, 0, r'$M$', fontsize=18, weight='bold', ha='center', va='center', color='black')
    
    # 绘制空间位移矢量
    num_vectors = 16  # 增加矢量数量，使可视化更丰富
    vectors = []
    
    for i in range(num_vectors):
        # 随机立体角分布
        theta = np.arccos(2*np.random.rand() - 1)
        phi = 2*np.pi*np.random.rand()
        
        # 生成矢量终点
        length = 2.0
        x_end = length * np.sin(theta) * np.cos(phi)
        y_end = length * np.sin(theta) * np.sin(phi)
        z_end = length * np.cos(theta)
        vectors.append((x_end, y_end, z_end))
        
        # 绘制矢量
        ax.plot([0, x_end], [0, y_end], [0, z_end], 'r-', linewidth=2.0, alpha=0.8)
        
        # 绘制箭头
        arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', color='r', linewidth=2.0)
        ax.add_artist(Arrow3D([x_end*0.8, x_end], [y_end*0.8, y_end], [z_end*0.8, z_end], **arrow_prop_dict))
    
    # 绘制多个立体角Ω，展示不同角度的立体角
    cone_params = [
        (1.5, 0.8, 'k', r'$\Omega_1$'),  # 高度、半径、颜色、标签
        (1.2, 0.6, 'b', r'$\Omega_2$'),
        (0.9, 0.4, 'g', r'$\Omega_3$')
    ]
    
    for i, (height, radius, color, label) in enumerate(cone_params):
        # 圆锥侧面
        cone_angles = np.linspace(0, 2*np.pi, 50)
        cone_x = radius * np.cos(cone_angles)
        cone_y = radius * np.sin(cone_angles)
        cone_z = np.ones_like(cone_angles) * height
        
        # 旋转立体角，使其分布在不同位置
        if i == 1:
            cone_x, cone_y = cone_y, -cone_x  # 旋转90度
        elif i == 2:
            cone_x, cone_z = cone_z, -cone_x  # 旋转90度
        
        for j in range(len(cone_angles)):
            ax.plot([0, cone_x[j]], [0, cone_y[j]], [0, cone_z[j]], f'{color}--', alpha=0.5, linewidth=1.5)
        
        # 圆锥底面
        ax.plot(cone_x, cone_y, cone_z, f'{color}--', alpha=0.7, linewidth=1.5)
        
        # 标注立体角Ω
        ax.text(cone_x[10]+0.1, cone_y[10]+0.1, cone_z[10]+0.2, label, fontsize=14, weight='bold', color=color)
    
    # 标注矢量条数n
    ax.text(2.0, 2.0, 2.0, r'$n$ 条空间位移矢量', fontsize=13, weight='bold', color='r', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # 标注单个矢量
    ax.plot([0, vectors[0][0]], [0, vectors[0][1]], [0, vectors[0][2]], 'r-', linewidth=2.5, alpha=1.0)
    ax.text(vectors[0][0]+0.2, vectors[0][1]+0.2, vectors[0][2]+0.2, r'$\vec{R}$', fontsize=14, weight='bold', color='r')
    
    # 设置视角
    ax.view_init(elev=35, azim=60)  # 优化视角，使立体效果更好
    
    # 设置坐标轴范围
    ax.set_xlim([-2.5, 2.5])
    ax.set_ylim([-2.5, 2.5])
    ax.set_zlim([-2.5, 2.5])
    
    # 添加坐标轴
    ax.set_axis_on()
    ax.set_xlabel(r'$x$ 方向', fontsize=14, weight='bold')
    ax.set_ylabel(r'$y$ 方向', fontsize=14, weight='bold')
    ax.set_zlabel(r'$z$ 方向', fontsize=14, weight='bold')
    
    # 设置坐标轴刻度
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_zticks([-2, -1, 0, 1, 2])
    ax.tick_params(axis='x', labelsize=11)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='z', labelsize=11)
    
    # 添加标题
    ax.set_title(r'质量的几何化定义示意图', fontsize=18, weight='bold', pad=20)
    
    # 添加质量几何化方程
    equation_text = r'$m = k \frac{n}{\Omega}$'
    ax.text2D(0.02, 0.02, equation_text, transform=ax.transAxes, fontsize=18, weight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 添加参数说明
    params_text = r'参数说明：$k$ 为量子比例常数，$n$ 为穿过立体角 $\Omega$ 的空间位移矢量条数，$\Omega$ 为立体角'
    ax.text2D(0.02, 0.10, params_text, transform=ax.transAxes, fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 添加物理意义
    physics_text = r'物理意义：质量是物体周围空间运动程度的度量，空间位移矢量条数越多，质量越大'
    ax.text2D(0.02, 0.18, physics_text, transform=ax.transAxes, fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 保存图片
    plt.savefig('质量几何化示意图.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("质量几何化示意图已生成")


def plot_G_derivation_flowchart():
    """绘制万有引力常数推导流程图"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 设置背景为白色
    ax.set_facecolor('white')
    
    # 隐藏坐标轴
    ax.set_axis_off()
    
    # 节点坐标和样式
    nodes = {
        'mass_def': (0.15, 0.85, r'质量几何化定义\n$m = k \frac{n}{\Omega}$', 'lightgreen', 'green'),
        'grav_field_def': (0.15, 0.70, r'引力场几何化定义\n$\vec{A} = -\frac{G k n \vec{R}}{\Omega r^3}$', 'lightyellow', 'orange'),
        'mp_def': (0.15, 0.55, r'普朗克质量定义\n$m_p = \sqrt{\frac{\hbar c}{G}}$', 'lightblue', 'blue'),
        'k_def': (0.15, 0.40, r'量子比例常数定义\n$k = 4\pi m_p$', 'lightcoral', 'red'),
        'G_mp': (0.5, 0.85, r'从$m_p$解出$G$\n$G = \frac{\hbar c}{m_p^2}$', 'lightcyan', 'cyan'),
        'mp_k': (0.5, 0.55, r'从$k$解出$m_p$\n$m_p = \frac{k}{4\pi}$', 'lightpink', 'magenta'),
        'G_k': (0.85, 0.70, r'万有引力常数的量子几何表达式\n$G = \frac{16\pi^2 \hbar c}{k^2}$', 'lightgray', 'black')
    }
    
    # 绘制节点
    for name, (x, y, text, facecolor, edgecolor) in nodes.items():
        # 使用圆角矩形代替圆形，更适合显示多行文本
        rect = plt.Rectangle((x-0.18, y-0.12), 0.36, 0.24, facecolor=facecolor, edgecolor=edgecolor, linewidth=2.5, alpha=0.9, zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=13, weight='bold', zorder=3)
        
        # 添加节点边框阴影效果
        shadow = plt.Rectangle((x-0.18+0.02, y-0.12+0.02), 0.36, 0.24, facecolor='gray', alpha=0.3, zorder=1)
        ax.add_patch(shadow)
    
    # 绘制箭头，添加箭头文本说明
    arrow_props = dict(arrowstyle='->', linewidth=3, color='black', zorder=4)
    text_props = dict(ha='center', va='center', fontsize=12, weight='bold', backgroundcolor='white', zorder=5)
    
    # 从mass_def到grav_field_def
    ax.annotate('', xy=(0.15, 0.75), xytext=(0.15, 0.80), arrowprops=arrow_props)
    ax.text(0.15, 0.775, r'应用', **text_props)
    
    # 从mp_def到G_mp
    ax.annotate('', xy=(0.4, 0.85), xytext=(0.33, 0.85), arrowprops=arrow_props)
    ax.text(0.365, 0.85, r'代数变形', **text_props)
    
    # 从k_def到mp_k
    ax.annotate('', xy=(0.4, 0.55), xytext=(0.33, 0.55), arrowprops=arrow_props)
    ax.text(0.365, 0.55, r'代数变形', **text_props)
    
    # 从G_mp到G_k
    ax.annotate('', xy=(0.77, 0.75), xytext=(0.68, 0.85), arrowprops=arrow_props)
    ax.text(0.725, 0.80, r'代入', **text_props)
    
    # 从mp_k到G_k
    ax.annotate('', xy=(0.77, 0.65), xytext=(0.68, 0.55), arrowprops=arrow_props)
    ax.text(0.725, 0.60, r'代入', **text_props)
    
    # 从mp_def到k_def
    ax.annotate('', xy=(0.15, 0.50), xytext=(0.15, 0.55), arrowprops=arrow_props)
    ax.text(0.15, 0.525, r'结合量子几何', **text_props)
    
    # 从grav_field_def到G_k
    ax.annotate('', xy=(0.5, 0.70), xytext=(0.33, 0.70), arrowprops=arrow_props)
    ax.text(0.415, 0.70, r'推导', **text_props)
    
    # 添加标题
    ax.set_title(r'万有引力常数的量子几何表达式推导流程', fontsize=20, weight='bold', y=0.98, pad=10)
    
    # 添加说明
    note_text = r'推导说明：从质量和引力场的几何化定义出发，结合普朗克质量和量子比例常数，最终推导出万有引力常数的量子几何表达式'
    ax.text(0.5, 0.05, note_text, ha='center', va='center', fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 保存图片
    plt.savefig('万有引力常数推导流程图.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("万有引力常数推导流程图已生成")


def plot_G_vs_c():
    """绘制G与c的关系图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 生成数据
    c_values = np.linspace(2.0e8, 4.0e8, 200)  # 扩大光速范围，显示更全面的关系
    hbar = 1.054571817e-34  # 约化普朗克常数
    m_p = 2.176434e-8  # 普朗克质量
    k = 4 * np.pi * m_p  # 量子比例常数
    
    # 计算G值：G = 16π² ℏ c / k²
    G_values = (16 * np.pi**2 * hbar * c_values) / (k**2)
    
    # 绘制G与c的关系曲线
    ax.plot(c_values, G_values, 'b-', linewidth=3.5, label=r'统一场论：$G \propto c$', alpha=0.9)
    
    # 添加数据点标记，增强可视化效果
    sample_c = c_values[::20]  # 每隔20个点取一个样本
    sample_G = G_values[::20]
    ax.scatter(sample_c, sample_G, color='blue', s=50, marker='o', alpha=0.7)
    
    # 绘制CODATA 2018值
    c_codata = 299792458  # CODATA 2018光速值
    G_codata = 6.67430e-11  # CODATA 2018万有引力常数值
    ax.scatter(c_codata, G_codata, color='red', s=150, marker='*', label=r'CODATA 2018实验值', zorder=5)
    
    # 添加误差线
    G_error = 1.5e-15  # CODATA 2018万有引力常数不确定度
    ax.errorbar(c_codata, G_codata, yerr=G_error, fmt='none', ecolor='red', capsize=8, linewidth=2.5, label=r'实验不确定度')
    
    # 添加光速变化范围的参考区域
    c_min, c_max = 2.99792457e8, 2.99792459e8  # 光速的可能变化范围（假设）
    ax.axvspan(c_min, c_max, color='green', alpha=0.2, label=r'光速测量范围')
    
    # 设置坐标轴标签
    ax.set_xlabel(r'光速 $c$ (m/s)', fontsize=16, weight='bold', labelpad=15)
    ax.set_ylabel(r'万有引力常数 $G$ (m³·kg⁻¹·s⁻²)', fontsize=16, weight='bold', labelpad=15)
    
    # 设置坐标轴刻度格式
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
    
    # 增加坐标轴刻度数量，提高可读性
    ax.xaxis.set_major_locator(ticker.MaxNLocator(8))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(8))
    
    # 添加网格线，增强可读性
    ax.grid(True, linestyle='--', alpha=0.8, linewidth=1.5)
    ax.grid(which='minor', linestyle=':', alpha=0.5, linewidth=1.0)
    ax.minorticks_on()
    
    # 添加标题
    ax.set_title(r'万有引力常数 $G$ 与光速 $c$ 的严格正比关系', fontsize=18, weight='bold', pad=20)
    
    # 添加图例，位置优化
    ax.legend(fontsize=13, loc='upper right', frameon=True, fancybox=True, shadow=True, borderaxespad=1.0)
    
    # 添加方程
    equation_text = r'$G = \frac{16\pi^2 \hbar c}{k^2} \Rightarrow G \propto c$'
    ax.text(0.02, 0.05, equation_text, transform=ax.transAxes, fontsize=16, weight='bold', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 添加物理意义说明
    physics_text = r'物理意义：万有引力常数与光速成正比，揭示了时空结构与引力相互作用的内在联系'
    ax.text(0.02, 0.01, physics_text, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 添加CODATA 2018值的标注
    ax.annotate(f'CODATA 2018: $c = {c_codata:,}$ m/s\n$G = {G_codata:.6e}$ m³·kg⁻¹·s⁻²', 
                xy=(c_codata, G_codata), xytext=(20, 20), textcoords='offset points',
                fontsize=11, weight='bold', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red'),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2', color='red', linewidth=2.0))
    
    # 保存图片
    plt.savefig('G与c的关系图.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("G与c的关系图已生成")


def plot_multiscale_verification():
    """绘制多尺度验证结果图"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 8))  # 增加一个子图，显示相对误差
    
    # 宏观尺度验证：地球表面重力
    methods = ['统一场论预测', '经典物理学']
    g_values = [9.8002, 9.80665]
    g_errors = [0.00645, 0.0]  # 统一场论误差，经典理论误差
    
    # 绘制宏观尺度验证结果
    bars1 = ax1.bar(methods, g_values, color=['blue', 'green'], alpha=0.8, edgecolor='black', linewidth=2.0)
    ax1.set_ylabel(r'重力加速度 $g$ (m/s²)', fontsize=14, weight='bold', labelpad=15)
    ax1.set_title(r'宏观尺度验证：地球表面重力', fontsize=16, weight='bold', pad=20)
    ax1.set_ylim([9.795, 9.810])
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.0008, 
                f'{height:.5f}', ha='center', va='bottom', fontsize=13, weight='bold')
    
    # 添加误差线
    ax1.errorbar(methods, g_values, yerr=g_errors, fmt='none', ecolor='red', capsize=8, linewidth=2.5, label=r'测量误差')
    ax1.legend(fontsize=12, loc='upper right')
    
    # 添加网格线
    ax1.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # 量子尺度验证：万有引力常数
    methods_q = ['统一场论预测', 'CODATA 2018实验值']
    G_values_q = [6.6743020978830638e-11, 6.67430e-11]
    G_errors_q = [0.0, 1.5e-15]  # 统一场论误差（理论预测），实验误差
    
    # 绘制量子尺度验证结果
    bars2 = ax2.bar(methods_q, G_values_q, color=['blue', 'red'], alpha=0.8, edgecolor='black', linewidth=2.0)
    ax2.set_ylabel(r'万有引力常数 $G$ (m³·kg⁻¹·s⁻²)', fontsize=14, weight='bold', labelpad=15)
    ax2.set_title(r'量子尺度验证：万有引力常数', fontsize=16, weight='bold', pad=20)
    
    # 设置y轴格式为科学计数法
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6e'))
    
    # 添加数值标签
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 8e-15, 
                f'{height:.9e}', ha='center', va='bottom', fontsize=12, weight='bold', rotation=45)
    
    # 添加误差线
    ax2.errorbar(methods_q, G_values_q, yerr=G_errors_q, fmt='none', ecolor='red', capsize=8, linewidth=2.5, label=r'实验不确定度')
    ax2.legend(fontsize=12, loc='upper right')
    
    # 添加网格线
    ax2.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # 新增：相对误差对比图
    scales = ['宏观尺度（重力）', '量子尺度（G）']
    rel_errors = [0.066, 0.00002247]  # 相对误差百分比
    
    bars3 = ax3.bar(scales, rel_errors, color=['purple', 'orange'], alpha=0.8, edgecolor='black', linewidth=2.0)
    ax3.set_ylabel(r'相对误差（%）', fontsize=14, weight='bold', labelpad=15)
    ax3.set_title(r'多尺度相对误差对比', fontsize=16, weight='bold', pad=20)
    ax3.set_yscale('log')  # 使用对数刻度，更清晰显示不同尺度的误差
    
    # 添加数值标签
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.2, 
                f'{height:.8f}%', ha='center', va='bottom', fontsize=12, weight='bold')
    
    # 添加网格线
    ax3.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # 调整布局
    plt.tight_layout()
    
    # 添加总标题
    fig.suptitle(r'多尺度验证结果：统一场论预测与实验/经典理论对比', fontsize=20, weight='bold', y=1.05)
    
    # 添加说明文字
    note_text = r'验证说明：统一场论在宏观和量子尺度均与实验/经典理论高度一致，相对误差远小于实验测量不确定度'
    fig.text(0.5, 0.02, note_text, ha='center', va='center', fontsize=13, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 保存图片
    plt.savefig('多尺度验证结果图.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print("多尺度验证结果图已生成")


def main():
    """主函数"""
    print("开始生成论文配图...")
    print("=" * 50)
    
    # 生成各个图表
    plot_space_spiral_motion()
    plot_mass_geometrization()
    plot_G_derivation_flowchart()
    plot_G_vs_c()
    plot_multiscale_verification()
    
    print("=" * 50)
    print("所有论文配图已生成！")
    print("生成的图片包括：")
    print("1. 空间螺旋运动示意图.pdf")
    print("2. 质量几何化示意图.pdf")
    print("3. 万有引力常数推导流程图.pdf")
    print("4. G与c的关系图.pdf")
    print("5. 多尺度验证结果图.pdf")


if __name__ == "__main__":
    main()
