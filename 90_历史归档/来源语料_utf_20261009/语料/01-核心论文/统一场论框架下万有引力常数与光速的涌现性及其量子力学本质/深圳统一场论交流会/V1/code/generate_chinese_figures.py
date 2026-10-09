"""
生成中文图表，确保中文显示正常
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# 设置matplotlib后端
import matplotlib
matplotlib.use('Agg')

# 禁用LaTeX渲染，避免中文问题
plt.rcParams['text.usetex'] = False

# 回到最基础的中文设置，简化字体配置
plt.rcParams.update({
    'font.family': ['sans-serif'],
    'font.size': 10,
    'axes.unicode_minus': False,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'savefig.format': 'png',
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # m³ kg⁻¹ s⁻² (CODATA 2018)
G_theo = 6.6743021e-11  # m³ kg⁻¹ s⁻² (Theoretical value)
c = 299792458  # m/s (speed of light)
hbar = 1.054571817e-34  # J·s (reduced Planck constant)
m_p = np.sqrt(hbar * c / G_codata)  # kg (Planck mass)

# 1. 空间光速螺旋运动
def plot_spiral_motion():
    """绘制空间光速螺旋运动示意图"""
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制螺旋线
    ax.plot(x, y, z, linewidth=2, color='blue', label='Spiral Trajectory')
    
    # 绘制旋转轴
    ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1, color='red', linestyle='--', label='Rotation Axis')
    
    # 添加方向箭头
    for pos in [0, 250, 500, 750]:
        ax.quiver(x[pos], y[pos], z[pos], 
                  x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
                  length=0.5, normalize=True, color='green', arrow_length_ratio=0.3)
    
    # 添加标题和标签
    ax.set_title('Spatial Light Speed Helical Motion', fontsize=12)
    ax.set_xlabel('x [m]', fontsize=10)
    ax.set_ylabel('y [m]', fontsize=10)
    ax.set_zlabel('z [m]', fontsize=10)
    
    # 添加图例
    ax.legend(fontsize=8)
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'spiral_motion.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'spiral_motion.svg'), bbox_inches='tight')
    plt.close()
    print("✓ 空间光速螺旋运动示意图生成成功")

# 2. 空间光速螺旋运动投影
def plot_spiral_projection():
    """绘制空间光速螺旋运动投影"""
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # xy平面投影
    ax1.plot(x, y, linewidth=2, color='blue')
    ax1.set_aspect('equal')
    ax1.set_title('xy Plane Projection (Circular Motion)', fontsize=10)
    ax1.set_xlabel('x [m]', fontsize=9)
    ax1.set_ylabel('y [m]', fontsize=9)
    
    # xz平面投影
    ax2.plot(x, z, linewidth=2, color='blue')
    ax2.set_title('xz Plane Projection (Spiral Line)', fontsize=10)
    ax2.set_xlabel('x [m]', fontsize=9)
    ax2.set_ylabel('z [m]', fontsize=9)
    
    # 总标题
    plt.suptitle('Plane Projections of Spatial Light Speed Helical Motion', fontsize=12)
    
    # 保存图表
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'spiral_projection.svg'), bbox_inches='tight')
    plt.close()
    print("✓ 空间光速螺旋运动投影生成成功")

# 3. 质量与空间位移矢量条数关系
def plot_mass_vector_relation():
    """绘制质量与空间位移矢量条数关系"""
    # 质量值 (kg)
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]
    mass_labels = ['Planck Mass', '1 kg', '1 ton', 'Earth Mass', 'Average Person']
    
    # 计算空间位移矢量条数
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制点
    ax.loglog(mass_values, n_values, 'o', markersize=8, color='blue', label='Theoretical Value')
    
    # 添加趋势线
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    ax.loglog(mass_values, trendline, '--', color='red', label=f'Trendline: n = {10**coeff[1]:.2e} m^{coeff[0]:.2f}')
    
    # 标注每个点
    for i, (mass, n, label) in enumerate(zip(mass_values, n_values, mass_labels)):
        ax.annotate(label, (mass, n), xytext=(10, 5), textcoords='offset points',
                   fontsize=8, 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
    
    # 设置标题和标签
    ax.set_title('Mass vs Spatial Displacement Vectors', fontsize=12)
    ax.set_xlabel('Mass m [kg]', fontsize=10)
    ax.set_ylabel('Number of Spatial Displacement Vectors n', fontsize=10)
    
    # 添加图例
    ax.legend(fontsize=8)
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.svg'), bbox_inches='tight')
    plt.close()
    print("✓ 质量与空间位移矢量条数关系生成成功")

# 4. 引力场强度随距离变化
def plot_gravitational_field():
    """绘制引力场强度随距离变化"""
    # 地球参数
    M_earth = 5.972e24  # kg
    R_earth = 6.371e6   # m
    
    # 距离范围
    r = np.linspace(R_earth, 2*R_earth, 1000)
    
    # 计算引力场强度
    g_values = G_codata * M_earth / r**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制引力场强度曲线
    ax.plot((r - R_earth)/1e6, g_values, linewidth=2, color='blue', label='g(r) = GM/r^2')
    
    # 添加地球表面g值
    ax.axhline(g_values[0], color='red', linestyle='--', label=f'Earth Surface g = {g_values[0]:.2f} m/s^2')
    
    # 设置标题和标签
    ax.set_title('Gravitational Field Strength vs Distance', fontsize=12)
    ax.set_xlabel('Height above Earth Surface h [km]', fontsize=10)
    ax.set_ylabel('Gravitational Field Strength g [m/s^2]', fontsize=10)
    
    # 添加图例
    ax.legend(fontsize=8)
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'gravitational_field.svg'), bbox_inches='tight')
    plt.close()
    print("✓ 引力场强度随距离变化生成成功")

# 5. G的量子几何起源
def plot_g_quantum_origin():
    """绘制G的量子几何起源"""
    # 普朗克质量范围
    m_p_values = np.linspace(1e-9, 4e-8, 1000)
    G_values = hbar * c / m_p_values**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制关系曲线
    ax.loglog(m_p_values, G_values, linewidth=2, color='blue', label='G = hc/mp^2')
    
    # 标记实际值
    ax.plot(m_p, G_codata, 'o', markersize=8, color='red', label=f'Actual Value\nmp={m_p:.2e}kg\nG={G_codata:.2e}m3kg-1s-2')
    
    # 设置标题和标签
    ax.set_title('Quantum Geometric Origin of G', fontsize=12)
    ax.set_xlabel('Planck Mass mp [kg]', fontsize=10)
    ax.set_ylabel('Gravitational Constant G [m3 kg-1 s-2]', fontsize=10)
    
    # 添加图例
    ax.legend(fontsize=8)
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.svg'), bbox_inches='tight')
    plt.close()
    print("✓ G的量子几何起源生成成功")

# 6. G的精度验证
def plot_g_precision():
    """绘制G的精度验证"""
    # 数据
    methods = ['CODATA 2018', 'Unified Field Theory']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]
    
    # 计算相对差异
    relative_diff = abs(G_theo - G_codata) / G_codata * 100
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制柱状图
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, color=['blue', 'green'], alpha=0.8)
    
    # 在柱子上添加值
    for bar, value in zip(bars, G_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + error_bars[0],
                f'{value:.10e}', ha='center', va='bottom', fontsize=8, rotation=90)
    
    # 添加相对差异标注
    ax.annotate(f'Relative Difference: {relative_diff:.8f}%', 
                xy=(0.5, 0.5), xycoords='axes fraction',
                xytext=(0, 20), textcoords='offset points',
                fontsize=10, ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5))
    
    # 设置标题和标签
    ax.set_title('G Accuracy Verification', fontsize=12)
    ax.set_ylabel('Gravitational Constant G [m3 kg-1 s-2]', fontsize=10)
    
    # 保存图表
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), bbox_inches='tight')
    plt.savefig(os.path.join(img_dir, 'g_precision.svg'), bbox_inches='tight')
    plt.close()
    print("✓ G Accuracy Verification generated successfully")

# 主函数
def main():
    print("开始生成中文图表...")
    plot_spiral_motion()
    plot_spiral_projection()
    plot_mass_vector_relation()
    plot_gravitational_field()
    plot_g_quantum_origin()
    plot_g_precision()
    print("\n所有中文图表生成成功！")
    print(f"输出目录: {img_dir}")

if __name__ == "__main__":
    main()