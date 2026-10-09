#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间理论可视化脚本
用于生成统一场论时间本质论文中的关键图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置工作目录和图表样式
import os

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # 切换到脚本所在目录

plt.style.use('default')  # 使用默认样式
plt.rcParams.update({
    'text.usetex': False,
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (8, 6),
    'figure.dpi': 300,
    'axes.facecolor': '#f8f9fa',
    'figure.facecolor': 'white',
    'axes.grid': True,
    'grid.color': '#e0e0e0',
    'grid.linestyle': '--',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']  # 支持中文的字体
})

def plot_time_dilation():
    """
    绘制时间膨胀效应图
    """
    # 生成速度数据（从0到0.999c）
    v = np.linspace(0, 0.999, 1000)  # 以光速c为单位
    
    # 计算时间膨胀因子
    gamma = 1 / np.sqrt(1 - v**2)
    
    # 创建图表
    plt.figure()
    plt.plot(v, gamma, 'b-', linewidth=2)
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.5)
    
    # 添加文本说明
    for v_val in [0.1, 0.5, 0.8, 0.95]:
        gamma_val = 1 / np.sqrt(1 - v_val**2)
        plt.annotate(f'v={v_val}c, γ={gamma_val:.2f}', 
                    xy=(v_val, gamma_val), 
                    xytext=(v_val+0.02, gamma_val+0.5),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    # 设置坐标轴和标题
    plt.xlabel('相对速度 (c)')
    plt.ylabel('时间膨胀因子 γ')
    plt.title('狭义相对论中的时间膨胀效应')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 设置坐标轴范围
    plt.xlim(0, 1)
    plt.ylim(0.8, 10)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('时间膨胀效应图.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_gravitational_time_dilation():
    """
    绘制引力时间膨胀效应图
    """
    # 生成距离数据（以史瓦西半径为单位）
    r_over_rs = np.linspace(1.1, 10, 1000)  # r/rs，rs是史瓦西半径
    
    # 计算引力时间膨胀因子
    gamma_grav = np.sqrt(1 - 1/r_over_rs)
    
    # 创建图表
    plt.figure()
    plt.plot(r_over_rs, gamma_grav, 'g-', linewidth=2)
    plt.axvline(x=1, color='r', linestyle='--', alpha=0.5, label='黑洞视界')
    
    # 添加文本说明
    plt.annotate('黑洞视界 (r=rs)', 
                xy=(1, 0.5), 
                xytext=(1.5, 0.6),
                arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8))
    
    # 设置坐标轴和标题
    plt.xlabel('距离/史瓦西半径 (r/rs)')
    plt.ylabel('引力时间膨胀因子')
    plt.title('广义相对论中的引力时间膨胀效应')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 设置坐标轴范围
    plt.xlim(1, 10)
    plt.ylim(0, 1.1)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('引力时间膨胀效应图.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_spacetime_equivalence():
    """
    绘制时空同一化关系图
    """
    # 生成时间数据
    t = np.linspace(0, 10, 100)
    c = 3e8  # 光速，单位：m/s
    
    # 计算空间位移
    r = c * t
    
    # 创建图表
    plt.figure()
    plt.plot(t, r/1e9, 'purple', linewidth=2)  # 转换为吉米(Gm)便于显示
    
    # 添加物理意义标注
    plt.fill_between(t, r/1e9, alpha=0.2, color='purple', label='时空同一化区域')
    
    # 设置坐标轴和标题
    plt.xlabel('时间 (s)')
    plt.ylabel('空间位移 (Gm)')
    plt.title('时空同一化原理：空间位移与时间的关系')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 添加光速说明
    plt.text(5, 12, f'光速 c = {c/1e8:.1f}×10⁸ m/s', fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('时空同一化关系图.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_time_field_distribution():
    """
    绘制时间场分布三维图
    """
    from mpl_toolkits.mplot3d import Axes3D
    
    # 创建网格
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # 计算距离
    R = np.sqrt(X**2 + Y**2)
    R[R == 0] = 1e-10  # 避免除零错误
    
    # 计算时间场分布 (根据论文中的公式)
    T0 = 1.0
    c = 1.0  # 归一化光速
    t = 1.0  # 固定时间
    T = T0 * np.exp(-c * t / R)
    
    # 创建三维图表
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制三维表面
    surf = ax.plot_surface(X, Y, T, cmap='viridis', alpha=0.8)
    
    # 添加颜色条
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='时间场强度 T')
    
    # 设置坐标轴和标题
    ax.set_xlabel('X 坐标')
    ax.set_ylabel('Y 坐标')
    ax.set_zlabel('时间场强度 T')
    ax.set_title('时间场的空间分布 (t=1)')
    
    # 设置视角
    ax.view_init(30, 45)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('时间场空间分布图.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_quantum_entanglement_time():
    """
    绘制量子纠缠中的时间关联图
    """
    # 生成时间数据
    t = np.linspace(0, 10, 100)
    
    # 计算纠缠粒子的关联强度 (简化模型)
    correlation = np.exp(-t/2) * np.cos(2*np.pi*t/3) + 0.5
    
    # 创建图表
    plt.figure()
    plt.plot(t, correlation, 'm-', linewidth=2)
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='经典关联阈值')
    
    # 标记量子纠缠区域
    plt.fill_between(t, correlation, 0.5, where=(correlation > 0.5), 
                     color='lightgreen', alpha=0.3, label='量子纠缠区域')
    
    # 设置坐标轴和标题
    plt.xlabel('时间 (任意单位)')
    plt.ylabel('纠缠关联强度')
    plt.title('量子纠缠中的时间关联特性')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 设置坐标轴范围
    plt.xlim(0, 10)
    plt.ylim(0, 1.5)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('量子纠缠时间关联图.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_multidimensional_spacetime():
    """
    绘制多维时空示意图
    """
    # 创建四维时空的投影图
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 生成参数
    theta = np.linspace(0, 2*np.pi, 50)
    phi = np.linspace(0, np.pi, 50)
    theta, phi = np.meshgrid(theta, phi)
    
    # 四维球面在三维空间中的投影
    r = 1.0
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    # 绘制时空流形
    surf = ax.plot_surface(x, y, z, color='cyan', alpha=0.3, edgecolor='blue')
    
    # 绘制时间轴
    ax.plot([0, 0], [0, 0], [0, -2], 'r-', linewidth=3, label='时间轴')
    
    # 添加标签
    ax.text(0, 0, -2.2, '时间维', color='red', fontsize=12)
    
    # 设置坐标轴和标题
    ax.set_xlabel('X 空间维')
    ax.set_ylabel('Y 空间维')
    ax.set_zlabel('Z 空间维')
    ax.set_title('多维时空示意图：四维时空在三维空间的投影')
    
    # 设置坐标轴范围
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-2.5, 1.5)
    
    # 添加图例
    ax.legend()
    
    # 设置视角
    ax.view_init(30, 45)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('多维时空示意图.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """
    主函数，生成所有图表
    """
    print("开始生成时间理论相关图表...")
    
    # 生成各个图表
    plot_time_dilation()
    print("时间膨胀效应图生成完成")
    
    plot_gravitational_time_dilation()
    print("引力时间膨胀效应图生成完成")
    
    plot_spacetime_equivalence()
    print("时空同一化关系图生成完成")
    
    plot_time_field_distribution()
    print("时间场空间分布图生成完成")
    
    plot_quantum_entanglement_time()
    print("量子纠缠时间关联图生成完成")
    
    plot_multidimensional_spacetime()
    print("多维时空示意图生成完成")
    
    print("所有图表生成完成！")

if __name__ == "__main__":
    main()
