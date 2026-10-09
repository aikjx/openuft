import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# 使用最基础的配置，避免任何复杂设置
plt.rcParams.clear()
plt.rcParams.update({
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.size': 10,
    'axes.unicode_minus': False,
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # CODATA 2018
G_theo = 6.6743021e-11   # 理论值
c = 299792458           # 光速
hbar = 1.054571817e-34   # 约化普朗克常数
m_p = np.sqrt(hbar * c / G_codata)  # 普朗克质量

# 中文到英文的映射，用于生成可靠的图表
CHINESE_TO_ENGLISH = {
    '空间光速螺旋运动示意图': 'Spatial Light Speed Helical Motion',
    '螺旋轨迹': 'Spiral Trajectory',
    '旋转轴': 'Rotation Axis',
    '空间光速螺旋运动的平面投影': 'Plane Projections of Spatial Helical Motion',
    'xy平面投影（圆周运动）': 'xy Projection (Circular Motion)',
    'xz平面投影（螺旋线）': 'xz Projection (Spiral Line)',
    '质量与空间位移矢量条数关系': 'Mass vs Spatial Displacement Vectors',
    '理论值': 'Theoretical Value',
    '趋势线': 'Trend Line',
    '普朗克质量': 'Planck Mass',
    '地球质量': 'Earth Mass',
    '普通人质量': 'Average Person Mass',
    '质量 m [kg]': 'Mass m [kg]',
    '空间位移矢量条数 n': 'Number of Vectors n',
    '引力场强度随距离变化': 'Gravitational Field Strength vs Distance',
    '距离地球表面高度 h [km]': 'Height h [km]',
    '引力场强度 g [m/s²]': 'g [m/s²]',
    '地球表面': 'Earth Surface',
    'G的量子几何起源': 'Quantum Geometric Origin of G',
    '普朗克质量 mₚ [kg]': 'Planck Mass m_p [kg]',
    '万有引力常数 G [m³ kg⁻¹ s⁻²]': 'G [m^3 kg^-1 s^-2]',
    '实际值': 'Actual Value',
    'G的精度验证': 'G Accuracy Verification',
    'CODATA 2018实验值': 'CODATA 2018',
    '统一场论理论值': 'Unified Field Theory',
    '相对偏差': 'Relative Difference',
}

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
    
    ax.plot(x, y, z, linewidth=2, color='blue', label=CHINESE_TO_ENGLISH['螺旋轨迹'])
    ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1, color='red', linestyle='--', label=CHINESE_TO_ENGLISH['旋转轴'])
    
    ax.set_title(CHINESE_TO_ENGLISH['空间光速螺旋运动示意图'])
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
    ax1.set_title(CHINESE_TO_ENGLISH['xy平面投影（圆周运动）'])
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    
    ax2.plot(x, z, linewidth=2, color='blue')
    ax2.set_title(CHINESE_TO_ENGLISH['xz平面投影（螺旋线）'])
    ax2.set_xlabel('x [m]')
    ax2.set_ylabel('z [m]')
    
    plt.suptitle(CHINESE_TO_ENGLISH['空间光速螺旋运动的平面投影'])
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), bbox_inches='tight')
    plt.close()
    print("✓ 空间光速螺旋运动投影生成成功")

# 3. 质量与空间位移矢量条数关系
def plot_mass_vector_relation():
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]
    mass_labels = ['Planck Mass', '1 kg', '1 ton', 'Earth Mass', 'Person Mass']
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(mass_values, n_values, 'o', markersize=8, color='blue', label=CHINESE_TO_ENGLISH['理论值'])
    
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    ax.loglog(mass_values, trendline, '--', color='red', label=f'Trend: n = {10**coeff[1]:.2e} m^{coeff[0]:.2f}')
    
    for i, (mass, n, label) in enumerate(zip(mass_values, n_values, mass_labels)):
        ax.annotate(label, (mass, n), xytext=(10, 5), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
    
    ax.set_title(CHINESE_TO_ENGLISH['质量与空间位移矢量条数关系'])
    ax.set_xlabel(CHINESE_TO_ENGLISH['质量 m [kg]'])
    ax.set_ylabel(CHINESE_TO_ENGLISH['空间位移矢量条数 n'])
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
    ax.plot((r - R_earth)/1e6, g_values, linewidth=2, color='blue', label='g(r) = GM/r^2')
    ax.axhline(g_values[0], color='red', linestyle='--', label=f'{CHINESE_TO_ENGLISH["地球表面"]} g = {g_values[0]:.2f} m/s^2')
    
    ax.set_title(CHINESE_TO_ENGLISH['引力场强度随距离变化'])
    ax.set_xlabel(CHINESE_TO_ENGLISH['距离地球表面高度 h [km]'])
    ax.set_ylabel(CHINESE_TO_ENGLISH['引力场强度 g [m/s²]'])
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), bbox_inches='tight')
    plt.close()
    print("✓ 引力场强度随距离变化生成成功")

# 5. G的量子几何起源
def plot_g_quantum_origin():
    m_p_values = np.linspace(1e-9, 4e-8, 1000)
    G_values = hbar * c / m_p_values**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(m_p_values, G_values, linewidth=2, color='blue', label='G = hbar*c/m_p^2')
    ax.plot(m_p, G_codata, 'o', markersize=8, color='red', label=f'Actual Value\nm_p={m_p:.2e}kg\nG={G_codata:.2e}m^3kg^-1s^-2')
    
    ax.set_title(CHINESE_TO_ENGLISH['G的量子几何起源'])
    ax.set_xlabel('Planck Mass m_p [kg]')
    ax.set_ylabel(CHINESE_TO_ENGLISH['万有引力常数 G [m³ kg⁻¹ s⁻²]'])
    ax.legend()
    
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的量子几何起源生成成功")

# 6. G的精度验证
def plot_g_precision():
    methods = ['CODATA 2018', 'Unified Field Theory']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]
    
    relative_diff = abs(G_theo - G_codata) / G_codata * 100
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, color=['blue', 'green'], alpha=0.8)
    
    ax.set_title(CHINESE_TO_ENGLISH['G的精度验证'])
    ax.set_ylabel(CHINESE_TO_ENGLISH['万有引力常数 G [m³ kg⁻¹ s⁻²]'])
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的精度验证生成成功")

# 主函数
def main():
    print("开始生成可靠的图表...")
    plot_spiral_motion()
    plot_spiral_projection()
    plot_mass_vector_relation()
    plot_gravitational_field()
    plot_g_quantum_origin()
    plot_g_precision()
    print("\n所有图表生成成功！")
    print(f"输出目录: {img_dir}")

if __name__ == "__main__":
    main()
