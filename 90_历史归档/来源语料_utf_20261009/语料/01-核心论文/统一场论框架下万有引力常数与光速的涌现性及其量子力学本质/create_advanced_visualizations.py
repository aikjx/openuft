import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter

# 设置全局样式
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'Times New Roman',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (12, 8),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.format': 'png',
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
    'axes.facecolor': 'white',
    'figure.facecolor': 'white'
})

# 1. 时空同一化方程可视化
def plot_spacetime_unification():
    """Plot spacetime unification equation r(t) = ct"""
    t = np.linspace(0, 10, 100)
    c = 3.0e8  # Speed of light, m/s
    r = c * t
    
    fig, ax = plt.subplots()
    ax.plot(t, r/1e9, 'b-', linewidth=2, label='$r(t) = ct$')
    ax.set_xlabel('Time $t$ (s)')
    ax.set_ylabel('Spatial Displacement $r(t)$ (Gm)')
    ax.set_title('Spacetime Unification Equation')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    ax.text(0.05, 0.95, f'$c = {c:.2e}$ m/s', transform=ax.transAxes, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    plt.savefig('spacetime_unification.png')
    plt.close()
    print("Generated: Spacetime Unification Equation")

# 2. 三维螺旋时空方程可视化
def plot_3d_spiral_spacetime():
    """Plot 3D spiral spacetime equation"""
    t = np.linspace(0, 10, 500)
    r = 1.0  # Spiral radius
    omega = 2 * np.pi  # Angular frequency
    h = 0.5  # Linear velocity component
    
    # Parametric equations
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot spiral
    ax.plot(x, y, z, 'b-', linewidth=2, label='Spiral Spacetime Trajectory')
    
    # Plot projections
    ax.plot(x, y, np.zeros_like(z), 'r--', alpha=0.5, label='XY Plane Projection')
    ax.plot(x, np.zeros_like(y), z, 'g--', alpha=0.5, label='XZ Plane Projection')
    ax.plot(np.zeros_like(x), y, z, 'm--', alpha=0.5, label='YZ Plane Projection')
    
    # Add arrows indicating direction
    for i in range(0, len(t), 50):
        ax.quiver(x[i], y[i], z[i], 
                  -r*omega*np.sin(omega*t[i]), 
                  r*omega*np.cos(omega*t[i]), 
                  h, 
                  length=0.3, color='k', alpha=0.8)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Time Dimension)')
    ax.set_title('3D Spiral Spacetime Equation')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    plt.savefig('3d_spiral_spacetime.png')
    plt.close()
    print("Generated: 3D Spiral Spacetime Equation")

# 3. 万有引力常数与光速的关系
def plot_gravitational_constant_vs_speed():
    """Plot relationship between gravitational constant and speed of light"""
    # Planck constant
    hbar = 1.054571817e-34  # J·s
    # Planck mass
    m_p = 2.176434e-8  # kg
    # Quantum geometry constant
    k = 4 * np.pi * m_p
    
    # Range of speed of light
    c = np.linspace(1.0e8, 5.0e8, 100)  # m/s
    
    # Calculate gravitational constant
    G = (16 * np.pi**2 * hbar * c) / k**2
    
    fig, ax = plt.subplots()
    ax.plot(c/1e8, G/1e-11, 'b-', linewidth=2, label='$G = \frac{16\pi^2 \hbar c}{k^2}$')
    ax.set_xlabel('Speed of Light $c$ ($\times 10^8$ m/s)')
    ax.set_ylabel('Gravitational Constant $G$ ($\times 10^{-11}$ m³·kg⁻¹·s⁻²)')
    ax.set_title('Relationship Between G and c')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add current c value
    c_current = 2.99792458e8
    G_current = (16 * np.pi**2 * hbar * c_current) / k**2
    ax.plot(c_current/1e8, G_current/1e-11, 'ro', markersize=8, label='Current c')
    ax.text(c_current/1e8 + 0.1, G_current/1e-11, 
            f'$c = {c_current:.2e}$ m/s\n$G = {G_current:.6e}$ m³·kg⁻¹·s⁻²',
            verticalalignment='center')
    
    ax.legend(loc='best')
    plt.savefig('gravitational_constant_vs_speed.png')
    plt.close()
    print("Generated: Relationship Between G and c")

# 4. 质量与空间位移矢量密度的关系
def plot_mass_vs_vector_density():
    """Plot relationship between mass and space displacement vector density"""
    # Quantum geometry constant
    k = 2.734987626169219e-07  # kg
    
    # Number of space displacement vectors
    n = np.linspace(1, 100, 100)
    # Solid angle
    Omega = 4 * np.pi  # Spherical solid angle
    
    # Calculate mass
    m = k * n / Omega
    
    fig, ax = plt.subplots()
    ax.plot(n, m/1e-8, 'b-', linewidth=2, label='$m = k \cdot \frac{n}{\Omega}$')
    ax.set_xlabel('Number of Space Vectors $n$')
    ax.set_ylabel('Mass $m$ ($\times 10^{-8}$ kg)')
    ax.set_title('Mass vs Space Vector Density')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add parameter explanation
    ax.text(0.05, 0.95, f'$k = {k:.2e}$ kg\n$\Omega = {Omega:.2f}$ sr', 
            transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.savefig('mass_vs_vector_density.png')
    plt.close()
    print("Generated: Mass vs Space Vector Density")

# 5. 量子比例常数k与普朗克质量的关系
def plot_quantum_geometry_constant():
    """Plot relationship between quantum geometry constant k and Planck mass"""
    # Planck mass range
    m_p = np.linspace(1.0e-8, 3.0e-8, 100)  # kg
    
    # Calculate quantum geometry constant
    k = 4 * np.pi * m_p
    
    fig, ax = plt.subplots()
    ax.plot(m_p/1e-8, k/1e-7, 'b-', linewidth=2, label='$k = 4\pi m_p$')
    ax.set_xlabel('Planck Mass $m_p$ ($\times 10^{-8}$ kg)')
    ax.set_ylabel('Quantum Geometry Constant $k$ ($\times 10^{-7}$ kg)')
    ax.set_title('Quantum Geometry Constant vs Planck Mass')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add current value
    m_p_current = 2.176434e-8
    k_current = 4 * np.pi * m_p_current
    ax.plot(m_p_current/1e-8, k_current/1e-7, 'ro', markersize=8, label='Current Value')
    ax.text(m_p_current/1e-8 + 0.1, k_current/1e-7, 
            f'$m_p = {m_p_current:.2e}$ kg\n$k = {k_current:.2e}$ kg',
            verticalalignment='center')
    
    ax.legend(loc='best')
    plt.savefig('quantum_geometry_constant.png')
    plt.close()
    print("Generated: Quantum Geometry Constant vs Planck Mass")

# 6. 空间螺旋运动可视化（2D投影）
def plot_spiral_motion_2d():
    """Plot 2D projection of space spiral motion"""
    t = np.linspace(0, 10, 500)
    r = 1.0
    omega = 2 * np.pi
    h = 0.5
    
    # Parametric equations
    x = r * np.cos(omega * t)
    y = r * np.sin(omega * t)
    z = h * t
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # XY plane projection (circular motion)
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('XY Plane Projection (Circular Motion)')
    ax1.axis('equal')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # XZ plane projection (spiral projection)
    ax2.plot(t, x, 'r-', linewidth=2, label='X Component')
    ax2.plot(t, z, 'g-', linewidth=2, label='Z Component')
    ax2.set_xlabel('Time t')
    ax2.set_ylabel('Displacement')
    ax2.set_title('XZ Plane Projection')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig('spiral_motion_2d.png')
    plt.close()
    print("Generated: 2D Projection of Spiral Motion")

# 7. 万有引力常数等价性验证图
def plot_gravitational_constant_equivalence():
    """Plot equivalence of two expressions for gravitational constant"""
    # Planck mass range
    m_p = np.linspace(1.0e-8, 3.0e-8, 100)  # kg
    
    # Planck constant
    hbar = 1.054571817e-34  # J·s
    c = 2.99792458e8  # m/s
    
    # Calculate quantum geometry constant
    k = 4 * np.pi * m_p
    
    # Two ways to calculate G
    G1 = (16 * np.pi**2 * hbar * c) / k**2  # Unified field theory expression
    G2 = (hbar * c) / m_p**2  # Quantum gravity standard expression
    
    fig, ax = plt.subplots()
    ax.plot(m_p/1e-8, G1/1e-11, 'b-', linewidth=2, label='UTF: $G = \frac{16\pi^2 \hbar c}{k^2}$')
    ax.plot(m_p/1e-8, G2/1e-11, 'r--', linewidth=2, label='QG: $G = \frac{\hbar c}{m_p^2}$')
    ax.set_xlabel('Planck Mass $m_p$ ($\times 10^{-8}$ kg)')
    ax.set_ylabel('Gravitational Constant $G$ ($\times 10^{-11}$ m³·kg⁻¹·s⁻²)')
    ax.set_title('Equivalence of G Expressions')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add equivalence explanation
    ax.text(0.05, 0.95, r'Mathematical Equivalence: $\frac{16\pi^2 \hbar c}{k^2} = \frac{\hbar c}{m_p^2}$', 
            transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.savefig('gravitational_constant_equivalence.png')
    plt.close()
    print("Generated: Equivalence of G Expressions")

# 8. 电子双缝干涉实验的几何解释
def plot_double_slit_geometry():
    """Plot geometric interpretation of electron double-slit experiment"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Draw experimental setup
    ax.plot([-5, 5], [0, 0], 'k-', linewidth=2, label='Double-Slit Screen')
    ax.plot([-1, -1], [-0.5, 0.5], 'k-', linewidth=1)
    ax.plot([1, 1], [-0.5, 0.5], 'k-', linewidth=1)
    ax.plot([-1.2, -0.8], [0, 0], 'k--', linewidth=1)
    ax.plot([0.8, 1.2], [0, 0], 'k--', linewidth=1)
    
    # Draw electron paths
    ax.plot([-8, -1], [0, 0], 'b-', linewidth=1, alpha=0.5)
    ax.plot([-8, 1], [0, 0], 'b-', linewidth=1, alpha=0.5)
    
    # Draw space waves
    x = np.linspace(-8, 8, 1000)
    y1 = 0.5 * np.sin(2 * np.pi * (x + 1) / 2) * np.exp(-0.1 * (x + 1)**2)
    y2 = 0.5 * np.sin(2 * np.pi * (x - 1) / 2) * np.exp(-0.1 * (x - 1)**2)
    y_total = y1 + y2
    
    ax.plot(x, y1, 'g--', linewidth=1, alpha=0.5, label='Space Wave from Slit 1')
    ax.plot(x, y2, 'r--', linewidth=1, alpha=0.5, label='Space Wave from Slit 2')
    ax.plot(x, y_total, 'm-', linewidth=2, label='Total Space Wave')
    
    # Draw detector screen
    ax.plot([8, 8], [-2, 2], 'k-', linewidth=2, label='Detector Screen')
    
    # Mark interference fringes
    for i in range(-3, 4):
        if i == 0:
            ax.plot([8, 8.5], [i*0.4, i*0.4], 'c-', linewidth=3, alpha=0.8)
        else:
            ax.plot([8, 8.3], [i*0.4, i*0.4], 'c-', linewidth=2, alpha=0.6)
    
    ax.set_xlabel('Position x')
    ax.set_ylabel('Wave Amplitude')
    ax.set_title('Geometric Interpretation of Double-Slit Experiment')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-2, 2)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')
    
    # Add explanation text
    ax.text(-9, 1.5, 'Electron', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    ax.text(-3, 1.5, 'Space Waves', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    ax.text(6, 1.5, 'Interference Fringes', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.savefig('double_slit_geometry.png')
    plt.close()
    print("Generated: Double-Slit Experiment Geometric Interpretation")

# 9. 质量与引力场关系图
def plot_mass_vs_gravitational_field():
    """Plot relationship between mass and gravitational field"""
    # Mass range
    M = np.linspace(1.0e24, 1.0e25, 100)  # kg
    
    # Gravitational constant
    G = 6.67430e-11  # m³·kg⁻¹·s⁻²
    # Distance (Earth radius)
    r = 6.371e6  # m
    
    # Calculate gravitational field strength
    g = (G * M) / r**2
    
    fig, ax = plt.subplots()
    ax.plot(M/1e24, g, 'b-', linewidth=2, label='$g = \frac{GM}{r^2}$')
    ax.set_xlabel('Mass $M$ ($\times 10^{24}$ kg)')
    ax.set_ylabel('Gravitational Field Strength $g$ (m/s²)')
    ax.set_title('Mass vs Gravitational Field Strength')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best')
    
    # Add Earth reference value
    M_earth = 5.972e24
    g_earth = (G * M_earth) / r**2
    ax.plot(M_earth/1e24, g_earth, 'ro', markersize=8, label='Earth')
    ax.text(M_earth/1e24 + 0.1, g_earth, 
            f'Earth: $g = {g_earth:.2f}$ m/s²',
            verticalalignment='center')
    
    plt.savefig('mass_vs_gravitational_field.png')
    plt.close()
    print("Generated: Mass vs Gravitational Field Strength")

# 10. 统一场论与其他理论对比图
def plot_theory_comparison():
    """Plot comparison between unified field theory and other theories"""
    theories = ['Newtonian Gravity', 'General Relativity', 'Quantum Field Theory', 'Unified Field Theory']
    
    # Rating for each indicator (1-5)
    gravity_essence = [2, 4, 3, 5]
    mass_essence = [2, 3, 3, 5]
    spacetime_view = [1, 4, 2, 5]
    computational_precision = [3, 4, 4, 5]
    physical_interpretation = [2, 3, 2, 5]
    
    x = np.arange(len(theories))
    width = 0.15
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.bar(x - 2*width, gravity_essence, width, label='Gravity Essence')
    ax.bar(x - width, mass_essence, width, label='Mass Essence')
    ax.bar(x, spacetime_view, width, label='Spacetime View')
    ax.bar(x + width, computational_precision, width, label='Computational Precision')
    ax.bar(x + 2*width, physical_interpretation, width, label='Physical Interpretation')
    
    ax.set_xlabel('Theories')
    ax.set_ylabel('Rating (1-5)')
    ax.set_title('Comparison Between Theories')
    ax.set_xticks(x)
    ax.set_xticklabels(theories)
    ax.legend(loc='best')
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    plt.tight_layout()
    plt.savefig('theory_comparison.png')
    plt.close()
    print("Generated: Theory Comparison")

# 主函数
if __name__ == "__main__":
    print("Generating advanced visualizations for unified field theory core concepts...")
    print("="*60)
    
    # Call all plotting functions
    plot_spacetime_unification()
    plot_3d_spiral_spacetime()
    plot_gravitational_constant_vs_speed()
    plot_mass_vs_vector_density()
    plot_quantum_geometry_constant()
    plot_spiral_motion_2d()
    plot_gravitational_constant_equivalence()
    plot_double_slit_geometry()
    plot_mass_vs_gravitational_field()
    plot_theory_comparison()
    
    print("="*60)
    print("All visualizations generated successfully!")
    print("Generated files:")
    print("1. spacetime_unification.png - Spacetime Unification Equation")
    print("2. 3d_spiral_spacetime.png - 3D Spiral Spacetime Equation")
    print("3. gravitational_constant_vs_speed.png - Relationship Between G and c")
    print("4. mass_vs_vector_density.png - Mass vs Space Vector Density")
    print("5. quantum_geometry_constant.png - Quantum Geometry Constant vs Planck Mass")
    print("6. spiral_motion_2d.png - 2D Projection of Spiral Motion")
    print("7. gravitational_constant_equivalence.png - Equivalence of G Expressions")
    print("8. double_slit_geometry.png - Double-Slit Experiment Geometric Interpretation")
    print("9. mass_vs_gravitational_field.png - Mass vs Gravitational Field Strength")
    print("10. theory_comparison.png - Comparison Between Theories")
