#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一场论核心论文图片生成脚本
使用Matplotlib、NumPy、SciPy等库生成科学可视化图片
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# 设置全局样式 - 顶尖论文标准
plt.style.use('default')  # 使用白底黑字的学术风格
plt.rcParams.update({
    # 字体设置 - 支持中文
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'SimSun', 'DejaVu Serif'],
    'font.sans-serif': ['Arial', 'SimHei', 'DejaVu Sans'],
    'mathtext.fontset': 'cm',
    
    # 字体大小
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.titlesize': 14,
    
    # 图片设置
    'figure.figsize': (8, 6),  # 标准论文图尺寸
    'figure.dpi': 600,  # 超高分辨率
    'savefig.dpi': 600,
    'savefig.format': 'png',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'savefig.facecolor': 'white',
    'savefig.edgecolor': 'white',
    
    # 线条和标记
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
    'lines.markeredgewidth': 0.5,
    
    # 坐标轴设置
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.minor.width': 0.4,
    'ytick.minor.width': 0.4,
    
    # 网格线
    'grid.linewidth': 0.4,
    'grid.linestyle': ':',
    
    # 图例
    'legend.frameon': True,
    'legend.framealpha': 0.9,
    'legend.edgecolor': 'black',
    'legend.fancybox': False,
    
    # 箱线图
    'boxplot.boxprops.linewidth': 0.8,
    'boxplot.whiskerprops.linewidth': 0.8,
    'boxplot.capprops.linewidth': 0.8,
    'boxplot.medianprops.linewidth': 1.0,
    
    # 误差线
    'errorbar.capsize': 3,
    
    # 颜色循环 - 使用更符合学术规范的配色
    'axes.prop_cycle': plt.cycler(
        color=['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
               '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
})

# 自定义颜色映射
blue_cmap = LinearSegmentedColormap.from_list('blue_cmap', ['#000033', '#003366', '#0066CC', '#3399FF', '#66CCFF'])
red_cmap = LinearSegmentedColormap.from_list('red_cmap', ['#330000', '#660000', '#CC0000', '#FF3333', '#FF6666'])


def generate_figure_1():
    """
    图片1：空间光速螺旋运动示意图
    """
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # 生成螺旋线数据
    t = np.linspace(0, 10, 1000)
    r = 1.0  # 螺旋半径
    omega = 1.0  # 角速度
    h = np.sqrt(1 - (r*omega)**2)  # 轴向速度分量
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 绘制螺旋线
    ax.plot(x, y, z, color='#66CCFF', linewidth=2, label='空间螺旋运动轨迹')
    
    # 绘制光速矢量分解
    ax.quiver(0, 0, 0, 0, 0, h, color='#FF3333', length=5, normalize=True, label='轴向速度分量 h')
    ax.quiver(0, 0, 0, r*omega, 0, 0, color='#FF3333', length=2, normalize=True, label='圆周速度分量 rω')
    ax.quiver(0, 0, 0, r*omega, 0, h, color='#FFFF00', length=5, normalize=True, label='光速矢量 C')
    
    # 绘制中心物体
    ax.scatter(0, 0, 0, color='#FFFFFF', s=500, marker='o', label='中心物体')
    
    # 设置坐标轴
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, 10)
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_zlabel('Z 轴')
    ax.set_title('空间光速螺旋运动示意图')
    
    # 添加图例
    ax.legend(loc='upper left', bbox_to_anchor=(0.85, 0.95))
    
    # 添加数学公式
    formula_text = r"""
    $\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$
    $h^2 + (r\omega)^2 = c^2$
    $|\vec{C}| = c = 299792458$ m/s
    """
    ax.text(0.85, 0.85, 0.85, formula_text, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#000033", edgecolor="#66CCFF"))
    
    # 保存图片
    plt.savefig('01_空间光速螺旋运动.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片1：空间光速螺旋运动示意图")


def generate_figure_2():
    """
    图片2：质量几何化定义示意图
    """
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # 生成球体数据
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 0.5 * np.outer(np.cos(u), np.sin(v))
    y = 0.5 * np.outer(np.sin(u), np.sin(v))
    z = 0.5 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # 绘制半透明球体
    ax.plot_surface(x, y, z, color='#66CCFF', alpha=0.3, rstride=5, cstride=5)
    
    # 绘制空间位移矢量
    n_vectors = 20
    theta = np.random.uniform(0, 2*np.pi, n_vectors)
    phi = np.random.uniform(0, np.pi, n_vectors)
    
    vector_length = np.linspace(1, 3, n_vectors)
    x_vec = vector_length * np.sin(phi) * np.cos(theta)
    y_vec = vector_length * np.sin(phi) * np.sin(theta)
    z_vec = vector_length * np.cos(phi)
    
    ax.quiver(0, 0, 0, x_vec, y_vec, z_vec, color='#00FF00', length=1, normalize=False, alpha=0.8)
    
    # 绘制立体角
    phi_sector = np.pi/4
    theta_sector = np.pi/3
    
    # 生成扇形区域
    u_sector = np.linspace(0, theta_sector, 50)
    v_sector = np.linspace(0, phi_sector, 50)
    x_sector = 0.5 * np.outer(np.cos(u_sector), np.sin(v_sector))
    y_sector = 0.5 * np.outer(np.sin(u_sector), np.sin(v_sector))
    z_sector = 0.5 * np.outer(np.ones(np.size(u_sector)), np.cos(v_sector))
    
    ax.plot_surface(x_sector, y_sector, z_sector, color='#FFFF00', alpha=0.5, rstride=5, cstride=5)
    
    # 设置坐标轴
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_zlabel('Z 轴')
    ax.set_title('质量几何化定义示意图')
    
    # 添加数学公式
    formula_text = r"""
    $m = k \cdot \frac{dn}{d\Omega}$ （微分形式）
    $m = k \frac{n}{\Omega}$ （积分形式）
    普朗克质量：n=1, Ω=4π
    """
    ax.text(0.85, 0.15, 0.15, formula_text, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#003300", edgecolor="#00FF00"))
    
    # 保存图片
    plt.savefig('02_质量几何化定义.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片2：质量几何化定义示意图")


def generate_figure_3():
    """
    图片3：引力场的几何化起源示意图
    """
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    
    # 生成引力场流线数据
    x, y = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    
    # 引力场强度（反比于距离平方）
    r = np.sqrt(x**2 + y**2)
    r[r < 0.5] = 0.5  # 避免中心奇点
    
    gx = -x / r**3
    gy = -y / r**3
    
    # 绘制引力场流线
    ax.streamplot(x, y, gx, gy, color='#FF6666', linewidth=1, density=1.5, arrowstyle='->')
    
    # 绘制中心物体
    circle = plt.Circle((0, 0), 0.5, color='#66CCFF', label='质量为M的物体')
    ax.add_artist(circle)
    
    # 绘制不同距离处的加速度矢量
    distances = [1.5, 2.5, 3.5]
    for d in distances:
        theta = np.pi/4
        x_pos = d * np.cos(theta)
        y_pos = d * np.sin(theta)
        
        g_mag = 1 / d**2
        gx_pos = -x_pos / d**3
        gy_pos = -y_pos / d**3
        
        ax.quiver(x_pos, y_pos, gx_pos, gy_pos, color='#FFFFFF', scale=5, label=f'd={d}, g={g_mag:.2f}')
    
    # 设置坐标轴
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_title('引力场的几何化起源示意图')
    
    # 添加公式
    formula_text = r"""
    $\vec{g} = -G k \frac{n \vec{r}}{\Omega r^3}$
    引力场是空间向物体加速运动的加速度场
    """
    ax.text(0.7, 0.8, formula_text, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#330000", edgecolor="#FF6666"))
    
    # 保存图片
    plt.savefig('03_引力场的几何化起源.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片3：引力场的几何化起源示意图")


def generate_figure_4():
    """
    图片4：万有引力常数推导流程图
    """
    fig = plt.figure(figsize=(16, 9), facecolor='#000033')
    
    # 定义流程步骤
    steps = [
        {"text": "空间光速螺旋运动公设", "formula": "\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}"},
        {"text": "质量几何化定义", "formula": "m = k \frac{n}{\Omega}"},
        {"text": "引力场几何化定义", "formula": "\vec{g} = -G k \frac{n \vec{r}}{\Omega r^3}"},
        {"text": "引力作用力推导", "formula": "\vec{F} = m \vec{g}"},
        {"text": "万有引力常数涌现", "formula": "G = \frac{16\pi^2 \hbar c}{k^2}"}
    ]
    
    # 绘制流程节点和箭头
    for i, step in enumerate(steps):
        # 绘制节点
        rect = patches.Rectangle((i*3, 2), 2.5, 2, linewidth=2, edgecolor='#66CCFF', facecolor='#000066')
        fig.gca().add_patch(rect)
        
        # 添加文本
        plt.text(i*3 + 1.25, 3.25, step["text"], ha='center', va='center', color='#FFFFFF', fontsize=14, fontweight='bold')
        plt.text(i*3 + 1.25, 2.75, step["formula"], ha='center', va='center', color='#66CCFF', fontsize=12)
        
        # 绘制箭头
        if i < len(steps) - 1:
            plt.arrow(i*3 + 2.5, 3, 0.5, 0, width=0.1, head_width=0.3, head_length=0.3, fc='#FFFF00', ec='#FFFF00')
    
    # 绘制实验验证结果
    verif_rect = patches.Rectangle((1.5, 5), 11, 1.5, linewidth=2, edgecolor='#00FF00', facecolor='#003300')
    fig.gca().add_patch(verif_rect)
    
    plt.text(7, 5.75, "实验验证结果：与CODATA 2018实验值偏差仅0.00003149%", 
             ha='center', va='center', color='#00FF00', fontsize=14, fontweight='bold')
    
    # 设置坐标轴
    plt.xlim(0, 15)
    plt.ylim(0, 8)
    plt.axis('off')
    
    # 添加标题
    plt.title('万有引力常数推导流程图', color='#FFFFFF', fontsize=18, fontweight='bold', y=0.95)
    
    # 保存图片
    plt.savefig('04_万有引力常数推导流程图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片4：万有引力常数推导流程图")


def generate_figure_5():
    """
    图片5：量子力学波粒二象性的几何解释
    """
    fig = plt.figure(figsize=(16, 9))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
    
    # 左侧：粒子性
    ax1 = plt.subplot(gs[0])
    
    # 绘制粒子运动轨迹
    x_particle = np.linspace(-4, 4, 100)
    y_particle = 0.5 * np.sin(2 * x_particle)  # 简单的波动轨迹
    
    ax1.plot(x_particle, y_particle, color='#FF6600', linewidth=2, label='粒子运动轨迹')
    ax1.scatter(0, 0, color='#FF6600', s=200, marker='o', label='粒子')
    
    # 绘制双缝
    slit1 = plt.Rectangle((1.5, -0.5), 0.1, 1, color='#CCCCCC')
    slit2 = plt.Rectangle((2.5, -0.5), 0.1, 1, color='#CCCCCC')
    ax1.add_artist(slit1)
    ax1.add_artist(slit2)
    
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-2, 2)
    ax1.set_xlabel('X 轴')
    ax1.set_ylabel('Y 轴')
    ax1.set_title('粒子性：物体在空间中的运动')
    ax1.legend()
    
    # 右侧：波动性
    ax2 = plt.subplot(gs[1])
    
    # 绘制空间波
    x_wave = np.linspace(-4, 4, 200)
    y_wave = 0.5 * np.sin(2 * x_wave)
    
    # 绘制入射波
    ax2.plot(x_wave[x_wave < 1.5], y_wave[x_wave < 1.5], color='#66CCFF', linewidth=2, label='入射空间波')
    
    # 绘制通过双缝后的波
    wave1 = 0.3 * np.sin(2 * (x_wave - 1.5))
    wave2 = 0.3 * np.sin(2 * (x_wave - 2.5))
    
    ax2.plot(x_wave[x_wave > 1.5], wave1[x_wave > 1.5], color='#66CCFF', linewidth=1, linestyle='--')
    ax2.plot(x_wave[x_wave > 2.5], wave2[x_wave > 2.5], color='#66CCFF', linewidth=1, linestyle='--')
    
    # 绘制干涉图案
    interference = 0.3 * np.sin(2 * (x_wave - 1.5)) + 0.3 * np.sin(2 * (x_wave - 2.5))
    ax2.plot(x_wave[x_wave > 3], interference[x_wave > 3], color='#FF6600', linewidth=2, label='干涉图案')
    
    # 绘制双缝
    slit1 = plt.Rectangle((1.5, -0.5), 0.1, 1, color='#CCCCCC')
    slit2 = plt.Rectangle((2.5, -0.5), 0.1, 1, color='#CCCCCC')
    ax2.add_artist(slit1)
    ax2.add_artist(slit2)
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-1, 1)
    ax2.set_xlabel('X 轴')
    ax2.set_ylabel('Y 轴')
    ax2.set_title('波动性：空间的螺旋运动')
    ax2.legend()
    
    # 添加标题
    fig.suptitle('量子力学波粒二象性的几何解释', fontsize=18, fontweight='bold')
    
    # 添加说明
    fig.text(0.5, 0.05, '粒子性是对物体运动的描述，波动性是对空间运动的描述', ha='center', color='#FFFFFF', fontsize=14)
    
    # 保存图片
    plt.savefig('05_量子力学波粒二象性的几何解释.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片5：量子力学波粒二象性的几何解释")


def generate_figure_6():
    """
    图片6：不同引力理论对比图表
    """
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, polar=True)
    
    # 定义对比维度
    categories = ['引力本质', '质量本质', '时空观', '数学复杂度', '实验验证', '量子兼容性']
    n_categories = len(categories)
    
    # 定义角度
    angles = [n / float(n_categories) * 2 * np.pi for n in range(n_categories)]
    angles += angles[:1]  # 闭合
    
    # 定义理论数据（0-10分）
    theories = {
        '牛顿引力': {'values': [6, 5, 4, 9, 8, 2], 'color': '#FF6666'},
        '广义相对论': {'values': [8, 7, 9, 3, 9, 5], 'color': '#66CCFF'},
        '统一场论': {'values': [9, 9, 8, 8, 8, 9], 'color': '#00FF00'}
    }
    
    # 绘制雷达图
    for name, theory in theories.items():
        values = theory['values']
        values += values[:1]  # 闭合
        ax.plot(angles, values, color=theory['color'], linewidth=2, linestyle='solid', label=name)
        ax.fill(angles, values, color=theory['color'], alpha=0.25)
    
    # 添加标签
    plt.xticks(angles[:-1], categories, color='#FFFFFF', size=12)
    
    # 设置坐标轴
    ax.set_rscale('linear')
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color='#FFFFFF', size=10)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # 添加标题
    plt.title('不同引力理论对比', size=18, color='#FFFFFF', y=1.1)
    
    # 添加图例
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # 保存图片
    plt.savefig('06_不同引力理论对比图表.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片6：不同引力理论对比图表")


def generate_figure_7():
    """
    图片7：空间位移矢量的物理意义示意图
    """
    fig = plt.figure(figsize=(16, 9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    
    # 上栏：几何意义
    ax1 = plt.subplot(gs[0], facecolor='#000033')
    
    # 绘制空间位移矢量
    ax1.arrow(0, 0, 3, 2, color='#66CCFF', width=0.1, head_width=0.3, head_length=0.3)
    
    # 绘制坐标系
    ax1.axhline(0, color='#CCCCCC', linestyle='--', linewidth=1)
    ax1.axvline(0, color='#CCCCCC', linestyle='--', linewidth=1)
    
    # 添加标注
    ax1.text(1.5, 1, '空间位移矢量', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax1.text(3.2, 2.2, '\(\vec{r}\)', color='#66CCFF', fontsize=16)
    
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')
    ax1.set_title('几何意义：空间位移矢量的数学定义', color='#FFFFFF')
    
    # 下栏：物理意义
    ax2 = plt.subplot(gs[1], facecolor='#330000')
    
    # 绘制中心物体
    circle = plt.Circle((0, 0), 1, color='#66CCFF', label='物体')
    ax2.add_artist(circle)
    
    # 绘制空间位移矢量
    n_vectors = 12
    for i in range(n_vectors):
        angle = 2 * np.pi * i / n_vectors
        length = 3
        ax2.arrow(0, 0, length*np.cos(angle), length*np.sin(angle), color='#00FF00', width=0.05, head_width=0.2, head_length=0.2)
    
    # 添加连接线条
    ax2.plot([0, 8], [0, 0], color='#FFFFFF', linestyle='--', linewidth=1)
    ax2.plot([0, -8], [0, 0], color='#FFFFFF', linestyle='--', linewidth=1)
    
    # 添加物理量标注
    ax2.text(3, 2, '质量', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax2.text(3, 1, 'm = k n/Ω', color='#00FF00', fontsize=12)
    
    ax2.text(6, 2, '引力', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax2.text(6, 1, '\(\vec{g} = -G k n \vec{r}/(Ω r^3)\)', color='#00FF00', fontsize=12)
    
    ax2.text(3, -2, '量子现象', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax2.text(3, -3, '空间螺旋运动的表现', color='#00FF00', fontsize=12)
    
    ax2.set_xlim(-8, 8)
    ax2.set_ylim(-4, 4)
    ax2.set_aspect('equal')
    ax2.set_title('物理意义：空间位移矢量与物理量的关系', color='#FFFFFF')
    
    # 添加标题
    fig.suptitle('空间位移矢量的物理意义示意图', fontsize=18, fontweight='bold', color='#FFFFFF')
    
    # 添加特性列表
    fig.text(0.85, 0.5, "空间位移矢量特性：\n1. 真实物理实体\n2. 光速运动\n3. 方向性和螺旋特性\n4. 连接几何与物理", 
             ha='left', va='center', color='#FFFFFF', fontsize=12, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#000000", edgecolor="#66CCFF"))
    
    # 保存图片
    plt.savefig('07_空间位移矢量的物理意义示意图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片7：空间位移矢量的物理意义示意图")


def generate_figure_8():
    """
    图片8：量子纠缠的几何解释示意图
    """
    fig = plt.figure(figsize=(16, 9), facecolor='#000033')
    ax = fig.add_subplot(111)
    
    # 绘制纠缠粒子
    particle1 = plt.Circle((-3, 0), 0.5, color='#00FF00', label='纠缠粒子1')
    particle2 = plt.Circle((3, 0), 0.5, color='#FF6600', label='纠缠粒子2')
    ax.add_artist(particle1)
    ax.add_artist(particle2)
    
    # 绘制粒子标签
    ax.text(-3, 0, '粒子1', ha='center', va='center', color='#000000', fontsize=14, fontweight='bold')
    ax.text(3, 0, '粒子2', ha='center', va='center', color='#000000', fontsize=14, fontweight='bold')
    
    # 绘制空间连接
    ax.plot([-3, 3], [0, 0], color='#FFFF00', linewidth=2, linestyle='--', label='空间整体性连接')
    
    # 绘制光速参考系
    light_cone = patches.Ellipse((0, 0), 10, 10, linewidth=2, edgecolor='#66CCFF', facecolor='none', linestyle='--', label='光速参考系')
    ax.add_artist(light_cone)
    
    # 添加光速参考系说明
    ax.text(0, 5.5, '光速参考系', ha='center', va='center', color='#66CCFF', fontsize=14, fontweight='bold')
    ax.text(0, 4.5, '（空间距离为零）', ha='center', va='center', color='#66CCFF', fontsize=12)
    
    # 设置坐标轴
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.set_title('量子纠缠的几何解释示意图', color='#FFFFFF')
    ax.legend()
    
    # 添加说明
    ax.text(0, -5, '非定域关联与观察者描述框架有关', ha='center', va='center', color='#FFFFFF', fontsize=14)
    
    # 保存图片
    plt.savefig('08_量子纠缠的几何解释示意图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片8：量子纠缠的几何解释示意图")


def generate_figure_9():
    """
    图片9：地球重力加速度计算验证示意图
    """
    fig = plt.figure(figsize=(16, 9))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
    
    # 左侧：地球模型和计算过程
    ax1 = plt.subplot(gs[0])
    
    # 绘制地球
    earth = plt.Circle((0, 0), 2, color='#66CCFF', label='地球')
    ax1.add_artist(earth)
    
    # 添加地球参数
    ax1.text(0, 0, '地球', ha='center', va='center', color='#000000', fontsize=14, fontweight='bold')
    ax1.text(0, 2.5, '质量：M = 5.972×10²⁴ kg', ha='center', va='center', color='#FFFFFF', fontsize=12)
    ax1.text(0, 2.1, '半径：R = 6.371×10⁶ m', ha='center', va='center', color='#FFFFFF', fontsize=12)
    
    # 绘制重力加速度矢量
    ax1.arrow(0, 2, 0, -0.5, color='#FF6666', width=0.1, head_width=0.3, head_length=0.3, label='重力加速度 g')
    
    # 添加计算过程
    calc_text = r"""
    计算过程：
    1. 质量几何化：M = k n/Ω
    2. 引力场：\(\vec{g} = -G k n \vec{r}/(Ω r^3)\)
    3. 代入得：g = G M / R²
    4. 计算值：g_calc = 9.81998 m/s²
    5. 实验值：g_exp = 9.81 m/s²
    6. 误差：0.1017%
    """
    ax1.text(3, 0, calc_text, ha='left', va='center', color='#FFFFFF', fontsize=12, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#000033", edgecolor="#66CCFF"))
    
    ax1.set_xlim(-3, 8)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X 轴')
    ax1.set_ylabel('Y 轴')
    ax1.set_title('地球重力加速度计算', color='#FFFFFF')
    ax1.legend()
    
    # 右侧：对比结果
    ax2 = plt.subplot(gs[1])
    
    # 定义数据
    methods = ['统一场论计算值', '实验测量值']
    values = [9.81998, 9.81]
    errors = [0.001, 0.005]  # 误差范围
    
    # 绘制柱状图
    bars = ax2.bar(methods, values, yerr=errors, capsize=5, color=['#66CCFF', '#FF6666'])
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001, f'{height:.5f}', ha='center', va='bottom', color='#FFFFFF')
    
    # 设置坐标轴
    ax2.set_ylim(9.805, 9.825)
    ax2.set_ylabel('重力加速度 g (m/s²)', color='#FFFFFF')
    ax2.set_title('计算值与实验值对比', color='#FFFFFF')
    
    # 添加误差说明
    ax2.text(0.5, 0.05, '误差范围：±0.001（计算值），±0.005（实验值）', ha='center', va='center', 
             transform=ax2.transAxes, color='#FFFFFF', fontsize=12)
    
    # 保存图片
    plt.savefig('09_地球重力加速度计算验证示意图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片9：地球重力加速度计算验证示意图")


def generate_figure_10():
    """
    图片10：统一场论未来研究方向思维导图
    """
    fig = plt.figure(figsize=(16, 9), facecolor='#003300')
    
    # 绘制中心主题
    center_circle = plt.Circle((0.5, 0.5), 0.15, color='#00FF00', transform=fig.transFigure)
    fig.gca().add_artist(center_circle)
    
    fig.text(0.5, 0.5, '统一场论未来研究', ha='center', va='center', color='#000000', fontsize=16, fontweight='bold')
    
    # 定义研究方向
    research_directions = [
        {
            "name": "四种基本力统一",
            "content": "扩展到强相互作用和弱相互作用",
            "position": (0.8, 0.8)
        },
        {
            "name": "量子计算新方案",
            "content": "基于光速空间螺旋运动的抗退相干技术",
            "position": (0.2, 0.8)
        },
        {
            "name": "引力控制探索",
            "content": "调制空间光速运动控制引力强度",
            "position": (0.9, 0.5)
        },
        {
            "name": "精密测量验证",
            "content": "高精度光速测量验证G与c关联",
            "position": (0.1, 0.5)
        },
        {
            "name": "宇宙学应用",
            "content": "探索宇宙起源、暗物质和暗能量",
            "position": (0.8, 0.2)
        },
        {
            "name": "与主流理论融合",
            "content": "与弦理论、圈量子引力等融合",
            "position": (0.2, 0.2)
        }
    ]
    
    # 绘制研究方向节点和连接线
    for rd in research_directions:
        # 绘制连接线
        fig.gca().plot([0.5, rd["position"][0]], [0.5, rd["position"][1]], color='#FFFFFF', linewidth=2)
        
        # 绘制节点
        node_circle = plt.Circle(rd["position"], 0.1, color='#006600', transform=fig.transFigure)
        fig.gca().add_artist(node_circle)
        
        # 添加文本
        fig.text(rd["position"][0], rd["position"][1] + 0.05, rd["name"], ha='center', va='center', color='#FFFFFF', fontsize=14, fontweight='bold', transform=fig.transFigure)
        fig.text(rd["position"][0], rd["position"][1] - 0.05, rd["content"], ha='center', va='center', color='#00FF00', fontsize=12, transform=fig.transFigure)
    
    # 设置坐标轴
    plt.axis('off')
    
    # 保存图片
    plt.savefig('10_统一场论未来研究方向思维导图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片10：统一场论未来研究方向思维导图")


def generate_figure_11():
    """
    图片11：空间位移矢量条数计算示意图
    """
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    
    # 定义典型物体的质量（kg）
    objects = {
        '电子': 9.109*10**-31,
        '质子': 1.672*10**-27,
        '70kg人': 70,
        '地球': 5.972*10**24,
        '太阳': 1.989*10**30
    }
    
    # 计算空间位移矢量条数（n = m / m_p，m_p = 2.176*10**-8 kg）
    m_p = 2.176*10**-8
    n_values = {name: m / m_p for name, m in objects.items()}
    
    # 准备数据
    mass_values = list(objects.values())
    n_values_list = list(n_values.values())
    object_names = list(objects.keys())
    
    # 绘制对数对数图
    ax.loglog(mass_values, n_values_list, 'o-', color='#FF6666', linewidth=2, markersize=10)
    
    # 添加数据点标签
    for i, name in enumerate(object_names):
        ax.annotate(name, (mass_values[i], n_values_list[i]), 
                    xytext=(5, 5), textcoords='offset points', 
                    color='#FFFFFF', fontsize=12)
    
    # 添加公式
    ax.text(0.05, 0.05, r'$n = \frac{m}{m_p}$', transform=ax.transAxes, 
            color='#66CCFF', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#000033", edgecolor="#66CCFF"))
    
    # 设置坐标轴
    ax.set_xlabel('质量 m (kg)', color='#FFFFFF')
    ax.set_ylabel('空间位移矢量条数 n', color='#FFFFFF')
    ax.set_title('不同质量物体对应的空间位移矢量条数', color='#FFFFFF')
    
    # 添加网格
    ax.grid(True, which='both', color='#333333', linestyle='--')
    
    # 保存图片
    plt.savefig('11_空间位移矢量条数计算示意图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片11：空间位移矢量条数计算示意图")


def generate_figure_12():
    """
    图片12：波函数塌缩的几何解释示意图
    """
    fig = plt.figure(figsize=(16, 9))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
    
    # 左侧：未观察状态
    ax1 = plt.subplot(gs[0])
    
    # 绘制模糊的螺旋线条（表示未观察时的空间运动）
    t = np.linspace(0, 4*np.pi, 100)
    r = 0.5 + 0.3 * np.sin(5*t)
    
    x = r * np.cos(t)
    y = r * np.sin(t)
    
    ax1.plot(x, y, color='#66CCFF', linewidth=2, alpha=0.5, label='空间螺旋运动')
    
    # 绘制中心物体
    ax1.scatter(0, 0, color='#FFFFFF', s=200, marker='o', label='物体')
    
    # 添加标注
    ax1.text(0, -1.2, '未观察状态：空间螺旋运动', ha='center', va='center', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax1.text(0, -1.6, '（波函数状态）', ha='center', va='center', color='#66CCFF', fontsize=12)
    
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X 轴')
    ax1.set_ylabel('Y 轴')
    ax1.legend()
    
    # 右侧：观察后状态
    ax2 = plt.subplot(gs[1])
    
    # 绘制清晰的粒子轨迹
    x_particle = np.linspace(-1, 1, 100)
    y_particle = 0.3 * np.sin(5*x_particle)
    
    ax2.plot(x_particle, y_particle, color='#FF6666', linewidth=2, label='粒子轨迹')
    ax2.scatter(0, 0, color='#FFFFFF', s=200, marker='o', label='物体')
    
    # 绘制观察者
    observer = plt.Circle((0.5, 0.5), 0.1, color='#00FF00')
    ax2.add_artist(observer)
    ax2.text(0.5, 0.5, 'O', ha='center', va='center', color='#000000', fontsize=12, fontweight='bold')
    ax2.text(0.5, 0.7, '观察者', ha='center', va='center', color='#00FF00', fontsize=12)
    
    # 添加标注
    ax2.text(0, -1.2, '观察后状态：粒子轨迹', ha='center', va='center', color='#FFFFFF', fontsize=14, fontweight='bold')
    ax2.text(0, -1.6, '（波函数塌缩）', ha='center', va='center', color='#FF6666', fontsize=12)
    
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(-1, 1)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X 轴')
    ax2.set_ylabel('Y 轴')
    ax2.legend()
    
    # 添加标题
    fig.suptitle('波函数塌缩的几何解释示意图', fontsize=18, fontweight='bold', color='#FFFFFF')
    
    # 添加说明
    fig.text(0.5, 0.05, '波函数塌缩是观察者描述框架的切换，而非物理状态的突变', ha='center', color='#FFFFFF', fontsize=14)
    
    # 保存图片
    plt.savefig('12_波函数塌缩的几何解释示意图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("生成图片12：波函数塌缩的几何解释示意图")


if __name__ == "__main__":
    # 设置工作目录
    import os
    os.chdir('d:\\a10\\aikjx\\code\\my_lib\\utf\\01-核心论文\\统一场论框架下万有引力常数与光速的涌现性及其量子力学本质\\深圳统一场论交流会\\V1')
    
    # 生成所有图片
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    generate_figure_5()
    generate_figure_6()
    generate_figure_7()
    generate_figure_8()
    generate_figure_9()
    generate_figure_10()
    generate_figure_11()
    generate_figure_12()
    
    print("所有图片生成完成！")
