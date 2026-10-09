"""
Generate all publication-ready figures for the paper "统一场论框架下万有引力常数的量子几何涌现与光速关联_核心简化版.md"

This script creates the following 6 figures:
1. spiral_motion.png - 空间光速螺旋运动示意图
2. spiral_projection.png - 空间光速螺旋运动的平面投影
3. mass_vector_relation.png - 质量与空间位移矢量条数关系
4. gravitational_field.png - 引力场强度随距离变化
5. g_quantum_origin.png - G的量子几何起源
6. g_precision.png - G的精度验证

All figures are saved to the ../img/ directory with high quality settings.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
import os

# Set up directories
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# Set font settings with Chinese support
plt.rcParams['font.sans-serif'] = ['SimHei']  # Chinese font
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign rendering
plt.style.use('seaborn-v0_8-paper')

# Disable LaTeX for Chinese text, enable for math symbols only
rc('text.latex', preamble=r'\usepackage{amsmath}')
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=False)  # Disable full LaTeX rendering to avoid Chinese issues

# Physical constants
g = 9.81  # m/s² (Earth's gravity)
G_codata = 6.67430e-11  # m³ kg⁻¹ s⁻² (CODATA 2018)
G_theo = 6.6743021e-11  # m³ kg⁻¹ s⁻² (Theoretical value)
c = 299792458  # m/s (speed of light)
hbar = 1.054571817e-34  # J·s (reduced Planck constant)
m_p = np.sqrt(hbar * c / G_codata)  # kg (Planck mass)

# 1. 空间光速螺旋运动示意图 (spiral_motion.png)
def generate_spiral_motion():
    # Set parameters for spiral motion
    r = 1.0          # Helical radius (m)
    omega = 2*np.pi  # Angular velocity (rad/s)
    h = 0.5          # Axial velocity (m/s)
    t = np.linspace(0, 5, 1000)
    
    # Calculate coordinates
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # Create 3D plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot helical trajectory
    ax.plot(x, y, z, linewidth=2.0, color='cornflowerblue', label='螺旋轨迹')
    
    # Add direction arrows
    arrow_positions = [0, 250, 500, 750]
    for pos in arrow_positions:
        ax.quiver(x[pos], y[pos], z[pos], 
                  x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
                  length=0.5, normalize=True, color='red', arrow_length_ratio=0.3)
    
    # Add labels and title
    ax.set_xlabel(r'$x$ [m]', fontsize=12)
    ax.set_ylabel(r'$y$ [m]', fontsize=12)
    ax.set_zlabel(r'$z$ [m]', fontsize=12)
    ax.set_title('空间光速螺旋运动示意图', fontsize=14, pad=20)
    ax.legend(fontsize=10, loc='upper left')
    
    # Add equation
    equation = r"$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$"
    ax.text2D(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
              bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))
    
    # Save figure
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_motion.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'spiral_motion.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ spiral_motion.png/svg generated")

# 2. 空间光速螺旋运动的平面投影 (spiral_projection.png)
def generate_spiral_projection():
    # Set parameters for spiral motion
    r = 1.0          # Helical radius (m)
    omega = 2*np.pi  # Angular velocity (rad/s)
    h = 0.5          # Axial velocity (m/s)
    t = np.linspace(0, 5, 1000)
    
    # Calculate coordinates
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    # Create 2x1 subplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Left plot: xy plane projection (circular motion)
    ax1.plot(x, y, linewidth=2.0, color='cornflowerblue')
    ax1.set_aspect('equal')
    ax1.set_xlabel(r'$x$ [m]', fontsize=12)
    ax1.set_ylabel(r'$y$ [m]', fontsize=12)
    ax1.set_title('xy平面投影 (圆周运动)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Right plot: xz plane projection (helix)
    ax2.plot(x, z, linewidth=2.0, color='cornflowerblue')
    ax2.set_xlabel(r'$x$ [m]', fontsize=12)
    ax2.set_ylabel(r'$z$ [m]', fontsize=12)
    ax2.set_title('xz平面投影 (螺旋线)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Add direction arrows
    for pos in [250, 750]:
        # xy plane
        ax1.arrow(x[pos] - 0.1*(x[pos+1]-x[pos]), y[pos] - 0.1*(y[pos+1]-y[pos]), 
                 0.2*(x[pos+1]-x[pos]), 0.2*(y[pos+1]-y[pos]), 
                 head_width=0.1, head_length=0.1, fc='red', ec='red')
        # xz plane
        ax2.arrow(x[pos] - 0.1*(x[pos+1]-x[pos]), z[pos] - 0.1*(z[pos+1]-z[pos]), 
                 0.2*(x[pos+1]-x[pos]), 0.2*(z[pos+1]-z[pos]), 
                 head_width=0.1, head_length=1.0, fc='red', ec='red')
    
    plt.suptitle('空间光速螺旋运动的平面投影', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'spiral_projection.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'spiral_projection.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ spiral_projection.png/svg generated")

# 3. 质量与空间位移矢量条数关系 (mass_vector_relation.png)
def generate_mass_vector_relation():
    # Mass values (kg)
    mass_values = [m_p, 1.0, 1.0e3, 5.972e24]  # Planck mass, 1kg, 1ton, Earth mass
    mass_labels = ['普朗克质量', '1 kg', '1 ton', '地球质量']
    mass_labels_en = ['$m_p$', '$1kg$', '$1ton$', '$M_\oplus$']
    
    # Calculate space displacement vector numbers
    n_values = [1, 1/m_p, 1e3/m_p, 5.972e24/m_p]
    
    # Create log-log plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot points
    ax.loglog(mass_values, n_values, 'o', markersize=8, color='cornflowerblue', label='理论值')
    
    # Add trendline
    x_log = np.log10(mass_values)
    y_log = np.log10(n_values)
    coeff = np.polyfit(x_log, y_log, 1)
    trendline = 10**(coeff[1]) * (np.array(mass_values)**coeff[0])
    ax.loglog(mass_values, trendline, '--', color='red', label=f'趋势线: $n = {10**coeff[1]:.2e} m^{coeff[0]:.2f}$')
    
    # Label each point
    for i, (mass, n, label, label_en) in enumerate(zip(mass_values, n_values, mass_labels, mass_labels_en)):
        ax.annotate(f'{label}\n({label_en})\nn={n:.2e}', 
                   (mass, n), xytext=(10, -10), textcoords='offset points', 
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.5))
    
    # Add labels and title
    ax.set_xlabel(r'质量 $m$ [kg]', fontsize=12)
    ax.set_ylabel(r'空间位移矢量条数 $n$', fontsize=12)
    ax.set_title('质量与空间位移矢量条数关系', fontsize=14)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, loc='upper left')
    
    # Add equation
    equation = r"$n = \frac{m}{m_p}$"
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'mass_vector_relation.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ mass_vector_relation.png/svg generated")

# 4. 引力场强度随距离变化 (gravitational_field.png)
def generate_gravitational_field():
    # Earth parameters
    M_earth = 5.972e24  # kg
    R_earth = 6.371e6   # m
    
    # Distance range (from Earth's surface to 2R_earth)
    r = np.linspace(R_earth, 2*R_earth, 1000)
    
    # Calculate gravitational field strength
    g = G_codata * M_earth / r**2
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot g(r)
    ax.plot((r - R_earth)/1e6, g, linewidth=2.0, color='cornflowerblue', label=r'$g(r) = \frac{GM}{r^2}$')
    
    # Add Earth's surface g value
    ax.axhline(g[0], color='red', linestyle='--', alpha=0.7, label=f'地球表面 $g = {g[0]:.2f} m/s^2$')
    
    # Add labels and title
    ax.set_xlabel(r'距离地球表面高度 $h$ [km]', fontsize=12)
    ax.set_ylabel(r'引力场强度 $g$ [m/s²]', fontsize=12)
    ax.set_title('引力场强度随距离变化', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, loc='upper right')
    
    # Add annotation
    ax.annotate('引力场随距离平方衰减', xy=(1.0, g[500]), xytext=(2.0, 7.0),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'gravitational_field.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'gravitational_field.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ gravitational_field.png/svg generated")

# 5. G的量子几何起源 (g_quantum_origin.png)
def generate_g_quantum_origin():
    # Plot showing G vs m_p^2 relationship
    m_p_values = np.linspace(1e-9, 4e-8, 1000)  # kg
    G_values = hbar * c / m_p_values**2  # kg⁻¹ m³ s⁻²
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot relationship
    ax.loglog(m_p_values, G_values, linewidth=2.0, color='cornflowerblue', label=r'$G = \frac{\hbar c}{m_p^2}$')
    
    # Mark actual values
    ax.plot(m_p, G_codata, 'o', markersize=10, color='red', label=f'实际值\n$m_p={m_p:.2e}kg$\n$G={G_codata:.2e}m^3kg^{-1}s^{-2}$')
    
    # Add labels and title
    ax.set_xlabel(r'普朗克质量 $m_p$ [kg]', fontsize=12)
    ax.set_ylabel(r'万有引力常数 $G$ [m³ kg⁻¹ s⁻²]', fontsize=12)
    ax.set_title('G的量子几何起源', fontsize=14)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, loc='upper right')
    
    # Add equation
    equation = r"$G = \frac{16\pi^2 \hbar c}{k^2} = \frac{\hbar c}{m_p^2}$"
    ax.text(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'g_quantum_origin.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ g_quantum_origin.png/svg generated")

# 6. G的精度验证 (g_precision.png)
def generate_g_precision():
    # Data for precision comparison
    methods = ['CODATA 2018实验值', '统一场论理论值']
    G_values = [G_codata, G_theo]
    error_bars = [1.5e-15, 0.0]  # CODATA uncertainty, theoretical value has no uncertainty
    
    # Calculate relative difference
    relative_diff = abs(G_theo - G_codata) / G_codata * 100
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot values with error bars
    bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, color=['cornflowerblue', 'lightgreen'], alpha=0.8)
    
    # Add exact values on bars
    for bar, value in zip(bars, G_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + error_bars[0],
                f'{value:.10e} m³/kg/s²', ha='center', va='bottom', fontsize=9)
    
    # Add relative difference annotation
    ax.annotate(f'相对偏差: {relative_diff:.8f}%', 
                xy=(0.5, 0.5), xycoords='axes fraction', 
                xytext=(0, 20), textcoords='offset points',
                fontsize=12, ha='center', 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.7))
    
    # Add labels and title
    ax.set_ylabel(r'万有引力常数 $G$ [m³ kg⁻¹ s⁻²]', fontsize=12)
    ax.set_title('G的精度验证', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'g_precision.png'), format='png', bbox_inches='tight', dpi=600)
    plt.savefig(os.path.join(img_dir, 'g_precision.svg'), format='svg', bbox_inches='tight')
    plt.close()
    print("✓ g_precision.png/svg generated")

# Main function to generate all figures
def main():
    print("开始生成所有图表...")
    generate_spiral_motion()
    generate_spiral_projection()
    generate_mass_vector_relation()
    generate_gravitational_field()
    generate_g_quantum_origin()
    generate_g_precision()
    print("\n所有图表已成功生成到 img 目录！")
    print(f"输出目录: {img_dir}")

if __name__ == "__main__":
    main()