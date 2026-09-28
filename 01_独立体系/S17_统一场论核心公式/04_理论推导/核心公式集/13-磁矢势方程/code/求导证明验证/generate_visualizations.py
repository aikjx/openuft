#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
张祥前统一场论磁矢势方程可视化脚本

该脚本用于生成磁矢势方程推导过程的可视化图表，包括常数比较、
电磁力与引力强度比、精细结构常数验证等。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch
from matplotlib.gridspec import GridSpec

# 设置中文字体和数学符号字体
# 使用更通用的字体配置，避免特定字体依赖
mpl.rcParams['font.family'] = ['sans-serif']
mpl.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Microsoft YaHei', 'sans-serif']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['mathtext.fontset'] = 'dejavusans'
mpl.rcParams['mathtext.default'] = 'regular'

# 1. 生成常数比较图表
def plot_constants_comparison():
    """绘制引力耦合常数Z、电磁光速几何耦合常数Z'和耦合常数f的比较图"""
    
    # CODATA 2018 常数
    G = 6.67430e-11  # 万有引力常数，单位：m³·kg⁻¹·s⁻²
    c = 299792458    # 光速，单位：m/s
    epsilon0 = 8.8541878128e-12  # 真空介电常数，单位：F·m⁻¹
    
    # 计算常数
    Z = (G * c) / 2
    Z_prime = c / (8 * np.pi * epsilon0)
    f = np.sqrt(Z / Z_prime) * (c / 2)
    
    # 准备数据
    constants = ['引力耦合常数 Z', '电磁光速几何耦合常数 Z\'', '耦合常数 f']
    values = [Z, Z_prime, f]
    log_values = [np.log10(abs(val)) for val in values]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制条形图
    bars = ax.bar(constants, log_values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    # 添加数值标签
    for bar, log_val, val in zip(bars, log_values, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'10^{log_val:.1f}',
                ha='center', va='bottom', fontsize=12)
        ax.text(bar.get_x() + bar.get_width()/2., height - 0.5,
                f'{val:.2e}',
                ha='center', va='top', fontsize=10, rotation=90, color='white')
    
    # 设置图表属性
    ax.set_ylabel('对数刻度 (log₁₀)', fontsize=14)
    ax.set_title('统一场论常数比较', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(min(log_values) - 1, max(log_values) + 1)
    
    # 添加单位说明（使用mathtext格式）
    unit_labels = [r'($m^4 \cdot kg^{-1} \cdot s^{-3}$)', '', r'($m/s$)']
    for i, unit in enumerate(unit_labels):
        ax.text(i, log_values[i] - 1.5, unit, ha='center', fontsize=10, color='gray')
    
    plt.tight_layout()
    plt.savefig('constants_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("[OK] 生成常数比较图表: constants_comparison.png")

# 2. 生成电磁力与引力强度比图表
def plot_force_ratio():
    """绘制电磁力与引力强度比的可视化图表"""
    
    # CODATA 2018 常数
    G = 6.67430e-11
    c = 299792458
    epsilon0 = 8.8541878128e-12
    
    # 计算强度比
    Z = (G * c) / 2
    Z_prime = c / (8 * np.pi * epsilon0)
    force_ratio = Z_prime / Z
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制强度比的对数表示
    categories = ['电磁力强度', '引力强度']
    values = [np.log10(Z_prime), np.log10(Z)]
    
    bars = ax.bar(categories, values, color=['#ff7f0e', '#1f77b4'], width=0.6)
    
    # 添加数值标签
    for bar, val, actual_val in zip(bars, values, [Z_prime, Z]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'10^{val:.1f}',
                ha='center', va='bottom', fontsize=12)
        ax.text(bar.get_x() + bar.get_width()/2., height - 0.5,
                f'{actual_val:.2e}',
                ha='center', va='top', fontsize=10, rotation=90, color='white')
    
    # 添加强度比说明
    ax.text(0.5, max(values) + 1.5,
            f'电磁力与引力强度比: Z\'/Z = {force_ratio:.2e}',
            ha='center', va='bottom', fontsize=14, fontweight='bold', color='red')
    
    # 设置图表属性
    ax.set_ylabel('对数刻度 (log₁₀)', fontsize=14)
    ax.set_title('电磁力与引力强度比较', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(min(values) - 1, max(values) + 2)
    
    plt.tight_layout()
    plt.savefig('force_ratio_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("[OK] 生成电磁力与引力强度比图表: force_ratio_comparison.png")

# 3. 生成精细结构常数验证图表
def plot_fine_structure_constant():
    """
    绘制精细结构常数的经典计算与通过Z'计算的比较图
    """
    
    # CODATA 2018 常数
    e = 1.602176634e-19  # 基本电荷，单位：C
    hbar = 1.054571817e-34  # 约化普朗克常数，单位：J·s
    c = 299792458  # 光速，单位：m/s
    epsilon0 = 8.8541878128e-12  # 真空介电常数，单位：F·m⁻¹
    
    # 计算 Z'
    Z_prime = c / (8 * np.pi * epsilon0)
    
    # 经典精细结构常数计算
    alpha_classical = (e ** 2) / (4 * np.pi * epsilon0 * hbar * c)
    
    # 通过 Z' 计算精细结构常数
    alpha_unified = (2 * e ** 2 * Z_prime) / (hbar * c ** 2)
    
    # 相对误差
    relative_error = abs(alpha_unified - alpha_classical) / alpha_classical * 100
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左侧图表：精细结构常数比较
    categories = ['经典计算', '通过 Z\' 计算']
    alpha_values = [alpha_classical, alpha_unified]
    
    bars = ax1.bar(categories, alpha_values, color=['#1f77b4', '#2ca02c'], width=0.6)
    
    for bar, val in zip(bars, alpha_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.00001,
                f'{val:.8f}',
                ha='center', va='bottom', fontsize=12)
    
    ax1.set_ylabel('精细结构常数 α', fontsize=14)
    ax1.set_title('精细结构常数计算比较', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0.007297, 0.007298)
    
    # 右侧图表：相对误差
    ax2.bar(['相对误差'], [relative_error], color=['#d62728'], width=0.3)
    ax2.text(0, max(relative_error + 0.000001, 0.000002),
            f'{relative_error:.10f}%',
            ha='center', va='bottom', fontsize=12)
    ax2.set_ylabel('相对误差 (%)', fontsize=14)
    ax2.set_title('计算相对误差', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    # 避免相对误差为0时ylim上下限相同
    if relative_error == 0:
        ax2.set_ylim(0, 0.000005)
    else:
        ax2.set_ylim(0, relative_error * 2)
    
    # 整体标题
    fig.suptitle('精细结构常数验证', fontsize=16, fontweight='bold')
    
    # 调整边距
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('fine_structure_constant_verification.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("[OK] 生成精细结构常数验证图表: fine_structure_constant_verification.png")

# 4. 生成方程推导流程图
def plot_derivation_flowchart():
    """
    绘制磁矢势方程 ∇×A = (1/f)B 的推导流程图
    """
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 设置背景颜色
    fig.patch.set_facecolor('#f5f5f5')
    
    # 节点位置 (x, y, text) - 使用mathtext格式表示数学符号
    nodes = {
        '公设1': (0.2, 0.8, r'时空同一化公设：$R = C t$'),
        '公设2': (0.5, 0.8, '物理量几何化公设'),
        'A定义': (0.1, 0.6, r'引力场定义：$A = d^2R/dt^2$'),
        'E定义': (0.3, 0.6, r'电场定义：$E = -\partial A/\partial t$'),
        'B定义': (0.5, 0.6, r'磁场定义：$B = (1/c^2)V\times E$'),
        '代入': (0.3, 0.4, r'代入$E = -\partial A/\partial t$到B定义'),
        '旋度关系': (0.1, 0.2, r'建立$V\times(\partial A/\partial t)$与$\nabla\times A$的比例关系'),
        'Z定义': (0.3, 0.2, r'几何常数$Z = Gc/2, Z^{\prime} = c/(8\pi\varepsilon_0)$'),
        'f定义': (0.5, 0.2, r'耦合常数$f = \sqrt{Z/Z^{\prime}}·(c/2)$'),
        '核心方程': (0.7, 0.5, r'核心方程：$\nabla\times A = (1/f)B$'),
    }
    
    # 边连接关系
    edges = [
        ('公设1', 'A定义'),
        ('公设2', 'A定义'),
        ('公设2', 'B定义'),
        ('A定义', 'E定义'),
        ('E定义', '代入'),
        ('B定义', '代入'),
        ('代入', '旋度关系'),
        ('旋度关系', '核心方程'),
        ('公设2', 'Z定义'),
        ('Z定义', 'f定义'),
        ('f定义', '核心方程'),
        ('代入', '核心方程'),
    ]
    
    # 绘制节点
    node_coords = {}
    for node_name, (x, y, text) in nodes.items():
        # 绘制节点圆圈
        circle = plt.Circle((x, y), 0.1, fill=True, color='#1f77b4', alpha=0.8)
        ax.add_patch(circle)
        
        # 存储节点坐标
        node_coords[node_name] = (x, y)
        
        # 添加节点文本
        ax.text(x, y, text, ha='center', va='center', fontsize=12, 
                color='white', fontweight='bold', wrap=True)
        
        # 添加节点标题
        ax.text(x, y + 0.12, node_name, ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 绘制边
    for start_node, end_node in edges:
        # 获取节点坐标
        start_x, start_y = node_coords[start_node]
        end_x, end_y = node_coords[end_node]
        
        # 计算箭头起点和终点（避免与圆圈重叠）
        dx = end_x - start_x
        dy = end_y - start_y
        dist = np.sqrt(dx**2 + dy**2)
        
        # 箭头起点（从圆圈边缘开始）
        arrow_start_x = start_x + (dx / dist) * 0.1
        arrow_start_y = start_y + (dy / dist) * 0.1
        
        # 箭头终点（到圆圈边缘结束）
        arrow_end_x = end_x - (dx / dist) * 0.1
        arrow_end_y = end_y - (dy / dist) * 0.1
        
        # 绘制箭头
        arrow = FancyArrowPatch(
            (arrow_start_x, arrow_start_y),
            (arrow_end_x, arrow_end_y),
            connectionstyle="arc3,rad=0.1",
            arrowstyle="->",
            color='#333333',
            linewidth=2,
            alpha=0.7,
            zorder=10
        )
        ax.add_patch(arrow)
    
    # 整体标题 - 使用mathtext格式表示数学符号
    fig.suptitle(r'磁矢势方程 $\nabla\times A = (1/f)B$ 推导流程图', fontsize=18, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.savefig('derivation_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("[OK] 生成方程推导流程图: derivation_flowchart.png")

# 5. 生成耦合常数f的直观理解图表
def plot_coupling_constant_f():
    """
    生成耦合常数f的直观理解图表，展示f与c的关系
    """
    
    # CODATA 2018 常数
    G = 6.67430e-11
    c = 299792458
    epsilon0 = 8.8541878128e-12
    
    # 计算常数
    Z = (G * c) / 2
    Z_prime = c / (8 * np.pi * epsilon0)
    f = np.sqrt(Z / Z_prime) * (c / 2)
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左侧图表：f与c的比较
    categories = ['耦合常数 f', '光速 c']
    values = [f, c]
    log_values = [np.log10(val) for val in values]
    
    bars = ax1.bar(categories, log_values, color=['#2ca02c', '#1f77b4'], width=0.6)
    
    for bar, log_val, val in zip(bars, log_values, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'10^{log_val:.1f}',
                ha='center', va='bottom', fontsize=12)
        ax1.text(bar.get_x() + bar.get_width()/2., height - 0.5,
                f'{val:.2e}',
                ha='center', va='top', fontsize=10, rotation=90, color='white')
    
    ax1.set_ylabel('对数刻度 (log₁₀)', fontsize=14)
    ax1.set_title('耦合常数 f 与光速 c 的比较', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 右侧图表：f的物理意义
    ax2.text(0.5, 0.7, f'f = {f:.6f} m/s', ha='center', fontsize=24, fontweight='bold', color='#2ca02c')
    ax2.text(0.5, 0.5, '约为步行速度的1/100', ha='center', fontsize=16, color='#555555')
    ax2.text(0.5, 0.3, '解释了为什么电磁场变化产生的引力效应', ha='center', fontsize=14, color='#555555')
    ax2.text(0.5, 0.2, '极其微弱，难以观测', ha='center', fontsize=14, color='#555555')
    
    ax2.axis('off')
    ax2.set_title('耦合常数 f 的物理意义', fontsize=14, fontweight='bold')
    
    # 整体标题
    fig.suptitle('耦合常数 f 的直观理解', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('coupling_constant_f.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("[OK] 生成耦合常数f的直观理解图表: coupling_constant_f.png")

# 主函数
def main():
    """主可视化函数"""
    
    print("张祥前统一场论磁矢势方程可视化脚本")
    print("=" * 60)
    print()
    
    # 1. 常数比较图表
    plot_constants_comparison()
    
    # 2. 电磁力与引力强度比图表
    plot_force_ratio()
    
    # 3. 精细结构常数验证图表
    plot_fine_structure_constant()
    
    # 4. 方程推导流程图
    plot_derivation_flowchart()
    
    # 5. 耦合常数f的直观理解图表
    plot_coupling_constant_f()
    
    print("=" * 60)
    print("可视化图表生成完成！")
    print("生成的图表文件：")
    print("1. constants_comparison.png - 统一场论常数比较")
    print("2. force_ratio_comparison.png - 电磁力与引力强度比较")
    print("3. fine_structure_constant_verification.png - 精细结构常数验证")
    print("4. derivation_flowchart.png - 方程推导流程图")
    print("5. coupling_constant_f.png - 耦合常数f的直观理解")

if __name__ == "__main__":
    main()