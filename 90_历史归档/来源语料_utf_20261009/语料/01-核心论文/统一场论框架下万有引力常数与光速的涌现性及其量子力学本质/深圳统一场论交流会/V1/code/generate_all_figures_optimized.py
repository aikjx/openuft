"""
优化版：生成统一场论论文的所有图表

This script creates 6 optimized figures for the paper with improved Chinese rendering and visual quality.
All figures are saved to the ../img/ directory with high quality settings.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Set up directories
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# --- 修复中文乱码的渲染设置 --- 
# 设置matplotlib的后端为Agg（适合生成图像文件）
import matplotlib
matplotlib.use('Agg')

# 修复中文乱码的关键设置
plt.rcParams.update({
    # 全局字体设置 - 确保使用系统中存在的中文黑体字体
    'font.family': ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS'],
    'font.size': 10,
    
    # 坐标轴设置
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'axes.unicode_minus': False,  # 解决负号显示问题
    
    # 刻度设置
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    
    # 图例设置
    'legend.fontsize': 10,
    
    # 科学计数法设置
    'axes.formatter.use_mathtext': True,
    'axes.formatter.limits': (-3, 4),
    
    # 图像设置
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 600,
    'savefig.format': 'png',
    
    # 修复中文显示的关键设置
    'text.usetex': False,  # 禁用LaTeX渲染，避免中文问题
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS'],
    'font.serif': ['Times New Roman', 'SimHei', 'Microsoft YaHei'],
})

# --- 优化的样式设置 --- 
plt.style.use('seaborn-v0_8-whitegrid')

# --- 物理常数 --- 
g = 9.81  # m/s² (Earth's gravity)
G_codata = 6.67430e-11  # m³ kg⁻¹ s⁻² (CODATA 2018)
G_theo = 6.6743021e-11  # m³ kg⁻¹ s⁻² (Theoretical value)
c = 299792458  # m/s (speed of light)
hbar = 1.054571817e-34  # J·s (reduced Planck constant)
m_p = np.sqrt(hbar * c / G_codata)  # kg (Planck mass)

# --- 1. 空间光速螺旋运动示意图 (spiral_motion.png) --- 
def generate_spiral_motion():
    """优化版：空间光速螺旋运动示意图"""
    # 参数设置
    r = 1.0          # 螺旋半径 (m)
    omega = 2*np.pi  # 角速度 (rad/s)
    h = 0.5          # 轴向速度 (m/s)
    t = np.linspace(0, 5, 1000)
    
    # 计算坐标
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 创建3D图表
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    
    # 设置背景颜色
    ax.set_facecolor('white')
    
    # 绘制螺旋轨迹（优化线条样式）
    ax.plot(x, y, z, linewidth=2.5, color='#1f77b4', label='螺旋轨迹', alpha=0.9)
    
    # 绘制旋转轴（优化样式）
    ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1.5, color='#e377c2', linestyle='--', label='旋转轴')
    
    # 添加方向箭头（优化样式和数量）
    arrow_positions = [0, 250, 500, 750]
    for pos in arrow_positions:
        ax.quiver(x[pos], y[pos], z[pos], 
                  x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
                  length=0.5, normalize=True, color='#d62728', arrow_length_ratio=0.3, linewidth=1.0)
    
    # 添加关键点（优化样式）
    key_times = [0, np.pi/(2*omega), np.pi/omega, 3*np.pi/(2*omega), 2*np.pi/omega]
    for i, t_key in enumerate(key_times):
        x_key = r * np.cos(omega * t_key)
        y_key = r * np.sin(omega * t_key)
        z_key = h * t_key
        ax.scatter(x_key, y_key, z_key, s=60, color='#ff7f0e', alpha=0.9, edgecolors='black')
        ax.text(x_key, y_key, z_key + 0.2, f'$t={t_key:.2f}s$', fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # 设置坐标轴标签和标题（优化中文显示）
    ax.set_xlabel('x [m]', fontsize=12, labelpad=10)
    ax.set_ylabel('y [m]', fontsize=12, labelpad=10)
    ax.set_zlabel('z [m]', fontsize=12, labelpad=10)
    ax.set_title('空间光速螺旋运动示意图', fontsize=14, pad=20, fontweight='bold')
    
    # 设置视角（优化观察角度）
    ax.view_init(elev=30, azim=45)
    
    # 添加方程标注（优化样式）
    equation = r'$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$'
    ax.text2D(0.02, 0.95, equation, transform=ax.transAxes, fontsize=12, 
              bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.7))
    
    # 添加光速约束标注
    c_value = np.sqrt((r*omega)**2 + h**2)
    speed_text = rf'$c = \sqrt{{(r\omega)^2 + h^2}} = {c_value:.2f} \, \mathrm{{m/s}}$'
    ax.text2D(0.02, 0.90, speed_text, transform=ax.transAxes, fontsize=11, 
              bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    # 添加图例（优化位置）
    ax.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95), frameon=True, fontsize=10)
    
    # 优化网格样式
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表（优化格式和质量）
    plt.savefig(os.path.join(img_dir, 'spiral_motion.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'spiral_motion.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 spiral_motion.png/svg 生成成功")

# --- 2. 空间光速螺旋运动的平面投影 (spiral_projection.png) --- 
def generate_spiral_projection():
    """优化版：空间光速螺旋运动的平面投影"""
    # 参数设置
    r = 1.0          # 螺旋半径 (m)
    omega = 2*np.pi  # 角速度 (rad/s)
    h = 0.5          # 轴向速度 (m/s)
    t = np.linspace(0, 5, 1000)
    
    # 计算坐标
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # 创建2x1子图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
    
    # 左图：xy平面投影（圆周运动）
    ax1.plot(x, y, linewidth=2.0, color='#1f77b4', alpha=0.9)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x [m]', fontsize=12)
    ax1.set_ylabel('y [m]', fontsize=12)
    ax1.set_title('xy平面投影 (圆周运动)', fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # 右图：xz平面投影（螺旋线）
    ax2.plot(x, z, linewidth=2.0, color='#1f77b4', alpha=0.9)
    ax2.set_xlabel('x [m]', fontsize=12)
    ax2.set_ylabel('z [m]', fontsize=12)
    ax2.set_title('xz平面投影 (螺旋线)', fontsize=12, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    # 添加方向箭头（优化样式）
    for pos in [250, 750]:
        # xy平面
        ax1.arrow(x[pos] - 0.1*(x[pos+1]-x[pos]), y[pos] - 0.1*(y[pos+1]-y[pos]), 
                 0.2*(x[pos+1]-x[pos]), 0.2*(y[pos+1]-y[pos]), 
                 head_width=0.1, head_length=0.1, fc='#d62728', ec='#d62728', linewidth=1.0)
        # xz平面
        ax2.arrow(x[pos] - 0.1*(x[pos+1]-x[pos]), z[pos] - 0.1*(z[pos+1]-z[pos]), 
                 0.2*(x[pos+1]-x[pos]), 0.2*(z[pos+1]-z[pos]), 
                 head_width=0.1, head_length=0.5, fc='#d62728', ec='#d62728', linewidth=1.0)
    
    # 添加关键点（优化样式）
    key_positions = [0, 250, 500, 750]
    for pos in key_positions:
        ax1.scatter(x[pos], y[pos], s=40, color='#ff7f0e', alpha=0.9, edgecolors='black')
        ax2.scatter(x[pos], z[pos], s=40, color='#ff7f0e', alpha=0.9, edgecolors='black')
    
    # 设置总标题
    plt.suptitle('空间光速螺旋运动的平面投影', fontsize=14, fontweight='bold', y=1.02)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'spiral_projection.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 spiral_projection.png/svg 生成成功")

# --- 3. 质量与空间位移矢量条数关系 (mass_vector_relation.png) --- 
def generate_mass_vector_relation():
    """优化版：质量与空间位移矢量条数关系"""
    # 质量值 (kg)
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]  # 普朗克质量, 1kg, 1ton, 地球质量, 普通人质量
    mass_labels = ['普朗克质量', '1 kg', '1 ton', '地球质量', '普通人质量']
    mass_labels_en = ['$m_p$', '$1kg$', '$1ton$', '$M_\oplus$', '$70kg$']
    
    # 计算空间位移矢量条数
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    # 创建对数-对数图表
    fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
    
    # 设置背景颜色
    ax.set_facecolor('white')
    
    # 绘制点（优化样式）
    scatter = ax.loglog(mass_values, n_values, 'o', markersize=10, color='#1f77b4', 
                       alpha=0.9, markeredgecolor='black', markeredgewidth=1.5, label='理论值')
    
    # 添加趋势线（优化样式）
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    ax.loglog(mass_values, trendline, '--', color='#d62728', linewidth=2.0, 
             label=f'趋势线: $n = {10**coeff[1]:.2e} m^{coeff[0]:.2f}$')
    
    # 标注每个点（优化样式和位置）
    for i, (mass, n, label, label_en) in enumerate(zip(mass_values, n_values, mass_labels, mass_labels_en)):
        # 调整标注位置，避免重叠
        if i == 0:
            xytext = (10, 10)
        elif i == 4:  # 普通人质量点
            xytext = (10, -20)
        else:
            xytext = (10, -10)
        
        ax.annotate(f'{label}\n({label_en})\nn={n:.2e}', 
                   (mass, n), xytext=xytext, textcoords='offset points', 
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    
    # 设置坐标轴标签和标题（优化中文显示）
    ax.set_xlabel('质量 $m$ [kg]', fontsize=12, fontweight='bold')
    ax.set_ylabel('空间位移矢量条数 $n$', fontsize=12, fontweight='bold')
    ax.set_title('质量与空间位移矢量条数关系', fontsize=14, fontweight='bold', pad=20)
    
    # 优化网格样式
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # 添加方程标注（优化样式）
    equation = r"$n = \frac{m}{m_p}$"
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    # 添加图例（优化位置）
    ax.legend(loc='upper left', frameon=True, fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 mass_vector_relation.png/svg 生成成功")

# --- 4. 引力场强度随距离变化 (gravitational_field.png) --- 
def generate_gravitational_field():
    """优化版：引力场强度随距离变化"""
    # 地球参数
    M_earth = 5.972e24  # kg
    R_earth = 6.371e6   # m
    
    # 距离范围（从地球表面到2R_earth）
    r = np.linspace(R_earth, 2*R_earth, 1000)
    
    # 计算引力场强度
    g_values = G_codata * M_earth / r**2
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    
    # 设置背景颜色
    ax.set_facecolor('white')
    
    # 绘制引力场强度曲线（优化样式）
    ax.plot((r - R_earth)/1e6, g_values, linewidth=2.5, color='#1f77b4', 
           alpha=0.9, label=r'$g(r) = \frac{GM}{r^2}$')
    
    # 添加地球表面g值（优化样式）
    ax.axhline(g_values[0], color='#d62728', linestyle='--', linewidth=2.0, alpha=0.8, 
              label=f'地球表面 $g = {g_values[0]:.2f} m/s^2$')
    
    # 添加普通人高度的g值（优化）
    human_height = 1.7  # m
    g_human = G_codata * M_earth / (R_earth + human_height)**2
    ax.axhline(g_human, color='#ff7f0e', linestyle='-.', linewidth=2.0, alpha=0.8, 
              label=f'普通人高度 $g = {g_human:.6f} m/s^2$')
    
    # 设置坐标轴标签和标题（优化中文显示）
    ax.set_xlabel('距离地球表面高度 $h$ [km]', fontsize=12, fontweight='bold')
    ax.set_ylabel('引力场强度 $g$ [m/s²]', fontsize=12, fontweight='bold')
    ax.set_title('引力场强度随距离变化', fontsize=14, fontweight='bold', pad=20)
    
    # 优化网格样式
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 添加标注（优化样式和位置）
    ax.annotate('引力场随距离平方衰减', xy=(1.0, g_values[500]), xytext=(2.0, 8.0),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.8))
    
    # 添加图例（优化位置）
    ax.legend(loc='upper right', frameon=True, fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'gravitational_field.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 gravitational_field.png/svg 生成成功")

# --- 5. G的量子几何起源 (g_quantum_origin.png) --- 
def generate_g_quantum_origin():
    """优化版：G的量子几何起源"""
    # 普朗克质量范围
    m_p_values = np.linspace(1e-9, 4e-8, 1000)  # kg
    G_values = hbar * c / m_p_values**2  # kg⁻¹ m³ s⁻²
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    
    # 设置背景颜色
    ax.set_facecolor('white')
    
    # 绘制G与m_p²的关系（优化样式）
    ax.loglog(m_p_values, G_values, linewidth=2.5, color='#1f77b4', alpha=0.9, 
             label=r'$G = \frac{\hbar c}{m_p^2}$')
    
    # 标记实际值（优化样式）
    ax.plot(m_p, G_codata, 'o', markersize=12, color='#d62728', alpha=0.9, 
           markeredgecolor='black', markeredgewidth=1.5, 
           label=f'实际值\n$m_p={m_p:.2e}kg$\n$G={G_codata:.2e}m^3kg^{-1}s^{-2}$')
    
    # 设置坐标轴标签和标题（优化中文显示）
    ax.set_xlabel('普朗克质量 $m_p$ [kg]', fontsize=12, fontweight='bold')
    ax.set_ylabel('万有引力常数 $G$ [m³ kg⁻¹ s⁻²]', fontsize=12, fontweight='bold')
    ax.set_title('G的量子几何起源', fontsize=14, fontweight='bold', pad=20)
    
    # 优化网格样式
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # 添加方程标注（优化样式）
    equation = r"$G = \frac{16\pi^2 \hbar c}{k^2} = \frac{\hbar c}{m_p^2}$"
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8))
    
    # 添加图例（优化位置）
    ax.legend(loc='upper right', frameon=True, fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 g_quantum_origin.png/svg 生成成功")

# --- 6. G的精度验证 (g_precision.png) --- 
def generate_g_precision():
    """优化版：G的精度验证"""
    # 数据
    methods = ['CODATA 2018实验值', '统一场论理论值']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]  # CODATA不确定度，理论值无不确定度
    
    # 计算相对差异
    relative_diff = abs(G_theo - G_codata) / G_codata * 100
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    
    # 设置背景颜色
    ax.set_facecolor('white')
    
    # 绘制柱状图（优化样式）
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=8, 
                 color=['#1f77b4', '#2ca02c'], alpha=0.9, edgecolor='black', linewidth=1.5)
    
    # 在柱子上添加精确值（优化样式）
    for bar, value in zip(bars, G_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + error_bars[0],
                f'{value:.10e} m³/kg/s²', ha='center', va='bottom', fontsize=9, 
                rotation=90, rotation_mode='anchor')
    
    # 添加相对差异标注（优化样式）
    ax.annotate(f'相对偏差: {relative_diff:.8f}%', 
                xy=(0.5, 0.5), xycoords='axes fraction', 
                xytext=(0, 30), textcoords='offset points',
                fontsize=12, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8))
    
    # 设置坐标轴标签和标题（优化中文显示）
    ax.set_ylabel('万有引力常数 $G$ [m³ kg⁻¹ s⁻²]', fontsize=12, fontweight='bold')
    ax.set_title('G的精度验证', fontsize=14, fontweight='bold', pad=20)
    
    # 优化网格样式
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'g_precision.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ 优化版 g_precision.png/svg 生成成功")

# --- 主函数 --- 
def main():
    print("开始生成优化版图表...")
    generate_spiral_motion()
    generate_spiral_projection()
    generate_mass_vector_relation()
    generate_gravitational_field()
    generate_g_quantum_origin()
    generate_g_precision()
    print("\n所有优化版图表已成功生成到 img 目录！")
    print(f"输出目录: {img_dir}")

if __name__ == "__main__":
    main()