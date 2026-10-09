import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# 确保中文显示正常的关键配置
plt.rcParams.update({
    'font.family': ['sans-serif'],
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans'],
    'axes.unicode_minus': False,  # 解决负号显示问题
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.size': 10,
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # m³ kg⁻¹ s⁻² (CODATA 2018)
G_theo = 6.6743021e-11  # 理论值
c = 299792458  # m/s
hbar = 1.054571817e-34  # J·s
m_p = np.sqrt(hbar * c / G_codata)  # 普朗克质量

# 1. 空间光速螺旋运动
def plot_spiral_motion():
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(x, y, z, linewidth=2, color='blue', label='螺旋轨迹')
    ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1, color='red', linestyle='--', label='旋转轴')
    
    for pos in [0, 250, 500, 750]:
        ax.quiver(x[pos], y[pos], z[pos], 
                  x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
                  length=0.5, normalize=True, color='green', arrow_length_ratio=0.3)
    
    ax.set_title('空间光速螺旋运动示意图')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'spiral_motion.png'), bbox_inches='tight')
    plt.close()
    print("✓ 空间光速螺旋运动示意图生成成功")

# 2. 空间光速螺旋运动投影
def plot_spiral_projection():
    r = 1.0
    omega = 2*np.pi
    h = 0.5
    t = np.linspace(0, 5, 1000)
    
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.plot(x, y, linewidth=2, color='blue')
    ax1.set_aspect('equal')
    ax1.set_title('xy平面投影（圆周运动）')
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    
    ax2.plot(x, z, linewidth=2, color='blue')
    ax2.set_title('xz平面投影（螺旋线）')
    ax2.set_xlabel('x [m]')
    ax2.set_ylabel('z [m]')
    
    plt.suptitle('空间光速螺旋运动的平面投影')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), bbox_inches='tight')
    plt.close()
    print("✓ 空间光速螺旋运动投影生成成功")

# 3. 质量与空间位移矢量条数关系
def plot_mass_vector_relation():
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]
    mass_labels = ['普朗克质量', '1 kg', '1吨', '地球质量', '普通人质量']
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(mass_values, n_values, 'o', markersize=8, color='blue', label='理论值')
    
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    ax.loglog(mass_values, trendline, '--', color='red', label=f'趋势线: n = {10**coeff[1]:.2e} m^{coeff[0]:.2f}')
    
    for i, (mass, n, label) in enumerate(zip(mass_values, n_values, mass_labels)):
        ax.annotate(label, (mass, n), xytext=(10, 5), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
    
    ax.set_title('质量与空间位移矢量条数关系')
    ax.set_xlabel('质量 m [kg]')
    ax.set_ylabel('空间位移矢量条数 n')
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), bbox_inches='tight')
    plt.close()
    print("✓ 质量与空间位移矢量条数关系生成成功")

# 4. 引力场强度随距离变化
def plot_gravitational_field():
    M_earth = 5.972e24  # kg
    R_earth = 6.371e6   # m
    r = np.linspace(R_earth, 2*R_earth, 1000)
    g_values = G_codata * M_earth / r**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot((r - R_earth)/1e6, g_values, linewidth=2, color='blue', label='g(r) = GM/r²')
    ax.axhline(g_values[0], color='red', linestyle='--', label=f'地球表面 g = {g_values[0]:.2f} m/s²')
    
    ax.set_title('引力场强度随距离变化')
    ax.set_xlabel('距离地球表面高度 h [km]')
    ax.set_ylabel('引力场强度 g [m/s²]')
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), bbox_inches='tight')
    plt.close()
    print("✓ 引力场强度随距离变化生成成功")

# 5. G的量子几何起源
def plot_g_quantum_origin():
    m_p_values = np.linspace(1e-9, 4e-8, 1000)
    G_values = hbar * c / m_p_values**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(m_p_values, G_values, linewidth=2, color='blue', label='G = ħc/mₚ²')
    ax.plot(m_p, G_codata, 'o', markersize=8, color='red', label=f'实际值\nmₚ={m_p:.2e}kg\nG={G_codata:.2e}m³kg⁻¹s⁻²')
    
    ax.set_title('G的量子几何起源')
    ax.set_xlabel('普朗克质量 mₚ [kg]')
    ax.set_ylabel('万有引力常数 G [m³ kg⁻¹ s⁻²]')
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的量子几何起源生成成功")

# 6. G的精度验证
def plot_g_precision():
    methods = ['CODATA 2018实验值', '统一场论理论值']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]
    
    relative_diff = abs(G_theo - G_codata) / G_codata * 100
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, color=['blue', 'green'], alpha=0.8)
    
    for bar, value in zip(bars, G_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + error_bars[0],
                f'{value:.10e}', ha='center', va='bottom', fontsize=8, rotation=90)
    
    ax.annotate(f'相对偏差: {relative_diff:.8f}%', 
                xy=(0.5, 0.5), xycoords='axes fraction',
                xytext=(0, 20), textcoords='offset points',
                fontsize=10, ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5))
    
    ax.set_title('G的精度验证')
    ax.set_ylabel('万有引力常数 G [m³ kg⁻¹ s⁻²]')
    
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的精度验证生成成功")

# 主函数
def main():
    print("开始生成修复后的中文图表...")
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
