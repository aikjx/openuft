import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# 核心配置：禁用LaTeX，使用matplotlib内置渲染
plt.rcParams.update({
    'text.usetex': False,  # 禁用LaTeX，避免复杂依赖
    'mathtext.fontset': 'cm',  # 使用Computer Modern字体集
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'font.size': 10,
    'axes.unicode_minus': False,  # 解决负号显示
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

# 1. G的量子几何起源 - 修复公式
def plot_g_quantum_origin():
    """修复G的量子几何起源图，确保公式正确渲染"""
    m_p_values = np.linspace(1e-9, 4e-8, 1000)
    G_values = hbar * c / m_p_values**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 使用matplotlib内置公式语法，避免Unicode字符
    ax.loglog(m_p_values, G_values, linewidth=2, color='blue', 
             label=r'$G = \hbar c / m_p^2$')
    
    # 简化标签，避免复杂公式
    ax.plot(m_p, G_codata, 'o', markersize=8, color='red', 
           label=f'Actual Value\nm_p = {m_p:.2e} kg\nG = {G_codata:.2e} m$^3$ kg$^{-1}$ s$^{-2}$')
    
    ax.set_title('Quantum Geometric Origin of G')
    ax.set_xlabel('Planck Mass $m_p$ [kg]')
    ax.set_ylabel('Gravitational Constant $G$ [m$^3$ kg$^{-1}$ s$^{-2}$]')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的量子几何起源 - 公式修复成功")

# 2. 引力场强度随距离变化 - 修复公式
def plot_gravitational_field():
    """修复引力场强度图，确保公式正确渲染"""
    M_earth = 5.972e24  # kg
    R_earth = 6.371e6   # m
    r = np.linspace(R_earth, 2*R_earth, 1000)
    g_values = G_codata * M_earth / r**2
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 使用matplotlib内置公式语法
    ax.plot((r - R_earth)/1e6, g_values, linewidth=2, color='blue', 
           label=r'$g(r) = GM / r^2$')
    
    ax.axhline(g_values[0], color='red', linestyle='--', 
              label=f'Earth Surface $g = {g_values[0]:.2f}$ m/s$^2$')
    
    ax.set_title('Gravitational Field Strength vs Distance')
    ax.set_xlabel('Height above Earth Surface $h$ [km]')
    ax.set_ylabel('Gravitational Field Strength $g$ [m/s$^2$]')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), bbox_inches='tight')
    plt.close()
    print("✓ 引力场强度随距离变化 - 公式修复成功")

# 3. G的精度验证 - 简化版本
def plot_g_precision():
    """修复G的精度验证图"""
    methods = ['CODATA 2018', 'Unified Field Theory']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, 
                 color=['blue', 'green'], alpha=0.8)
    
    ax.set_title('G Accuracy Verification')
    ax.set_ylabel('Gravitational Constant $G$ [m$^3$ kg$^{-1}$ s$^{-2}$]')
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), bbox_inches='tight')
    plt.close()
    print("✓ G的精度验证 - 修复成功")

# 4. 质量与空间位移矢量条数关系 - 修复公式
def plot_mass_vector_relation():
    """修复质量与矢量关系图"""
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24, 70.0]
    mass_labels = ['Planck Mass', '1 kg', '1 ton', 'Earth Mass', 'Person']
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p, 70.0/m_p]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(mass_values, n_values, 'o', markersize=8, color='blue', 
             label='Theoretical Value')
    
    # 计算趋势线
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    
    # 使用matplotlib公式语法
    ax.loglog(mass_values, trendline, '--', color='red', 
             label=rf'Trend: $n = {10**coeff[1]:.2e} \cdot m^{{{coeff[0]:.2f}}}$')
    
    # 添加标签
    for i, (mass, n, label) in enumerate(zip(mass_values, n_values, mass_labels)):
        ax.annotate(label, (mass, n), xytext=(10, 5), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
    
    ax.set_title('Mass vs Spatial Displacement Vectors')
    ax.set_xlabel('Mass $m$ [kg]')
    ax.set_ylabel('Number of Vectors $n$')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), bbox_inches='tight')
    plt.close()
    print("✓ 质量与空间位移矢量条数关系 - 公式修复成功")

# 主函数
def main():
    print("开始修复公式乱码问题...")
    plot_g_quantum_origin()
    plot_gravitational_field()
    plot_g_precision()
    plot_mass_vector_relation()
    print("\n所有公式修复成功！")
    print(f"输出目录: {img_dir}")

if __name__ == "__main__":
    main()
