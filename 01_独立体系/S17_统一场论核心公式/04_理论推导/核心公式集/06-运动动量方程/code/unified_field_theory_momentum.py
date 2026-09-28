"""
Generate publication-ready, vector-based physics visualizations for Zhang Xiangqian's Unified Field Theory momentum formula P = m(C - V)

Objective: To accurately and clearly depict the geometric relationship and physical implications of the core momentum formula, adhering to the highest standards of scientific journals.

Key Specifications:
1. Physics & Mathematical Accuracy:
   - Equation Representation: P = m(C - V), P0 = m0C0, cosθ = v/c
   - Physical Parameters: c = 3e8 m/s (speed of light), m0 = 1 kg (rest mass)
   - Data Range: v from 0 to c, θ from 0 to π/2

2. Clarity & Interpretability:
   - Axes Labels: Include physical quantities and SI units
   - Legend: Concise, informative, positioned appropriately
   - Title: Descriptive, summarizing core content

3. Aesthetics & Professionalism:
   - Plotting Style: 'seaborn-v0_8-paper' for scientific appearance
   - Color Palette: Colorblind-friendly, low saturation, high contrast
   - Line Styles & Markers: Clear differentiation, appropriate line widths
   - Font: Serif font (Times New Roman/Computer Modern)

4. Mathematical Representation:
   - Simple mathematical expressions using matplotlib's built-in rendering

5. Technical Output:
   - Format: Vector formats (PNG, SVG) for scalability
   - Resolution: 600 DPI for PNG
   - File Naming: Descriptive and consistent

6. Reproducibility:
   - Extensive comments explaining steps, formulas, and parameters
   - Parameterization of key constants

Preferred Libraries: matplotlib, numpy, seaborn
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import os

# --- 1. Physics & Mathematical Accuracy ---#
# Physical Constants
c = 3e8  # m/s (speed of light)
m0 = 1.0  # kg (rest mass)

# Create output directory if it doesn't exist
output_dir = '../img'
os.makedirs(output_dir, exist_ok=True)

# --- 2. Plot 1: Geometric Relationship of Vector Speeds (C, V, C-V) ---#
def plot_vector_speed_geometry():
    """
    Plot the geometric relationship between vector light speed C, object speed V, and relative speed U = C - V
    forming a right triangle with cosθ = v/c
    """
    # Set up font rendering
    rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
    rc('text', usetex=False)
    
    # Create figure with appropriate size for journal (single column: 3.5 inches)
    plt.figure(figsize=(3.5, 3.5))
    
    # Generate data for the vector triangle
    theta = np.pi / 3  # 60 degrees for visualization
    v = c * np.cos(theta)  # v = c * cosθ
    
    # Vector components
    # C: vector light speed (magnitude c, angle θ from x-axis)
    Cx = c * np.cos(theta)
    Cy = c * np.sin(theta)
    
    # V: object speed (magnitude v, along x-axis)
    Vx = v
    Vy = 0
    
    # U: relative speed = C - V
    Ux = Cx - Vx
    Uy = Cy - Vy
    
    # Plot vectors
    plt.quiver(0, 0, Cx, Cy, angles='xy', scale_units='xy', scale=1, 
               color='blue', width=0.015, label=r'$\vec{C}$ (Vector Light Speed)')
    plt.quiver(0, 0, Vx, Vy, angles='xy', scale_units='xy', scale=1, 
               color='red', width=0.015, label=r'$\vec{V}$ (Object Speed)')
    plt.quiver(Vx, Vy, Ux, Uy, angles='xy', scale_units='xy', scale=1, 
               color='green', width=0.015, label=r'$\vec{U} = \vec{C} - \vec{V}$ (Relative Speed)')
    
    # Plot triangle sides with dashed lines for clarity
    plt.plot([0, Cx], [0, Cy], 'b--', alpha=0.5, linewidth=1.0)
    plt.plot([Vx, Cx], [Vy, Cy], 'g--', alpha=0.5, linewidth=1.0)
    
    # Add labels for magnitudes
    plt.text(Cx/2, Cy/2, r'$c$', fontsize=12, color='blue', ha='right')
    plt.text(Vx/2, Vy/2 - 0.5e7, r'$v$', fontsize=12, color='red')
    plt.text(Vx + Ux/2, Vy + Uy/2, r'$c\sqrt{1-v^2/c^2}$', fontsize=12, color='green', ha='left')
    
    # Add angle θ
    theta_text = r'$\theta$' if theta != 0 else ''
    plt.text(0.1e8, 0.1e8, theta_text, fontsize=14, color='purple')
    
    # Draw angle arc
    arc_radius = 1e7
    arc_x = np.linspace(0, arc_radius * np.cos(theta), 50)
    arc_y = np.linspace(0, arc_radius * np.sin(theta), 50)
    plt.plot(arc_x, arc_y, color='purple', linestyle='--', linewidth=1.0)
    
    # Set axis limits
    max_val = c * 1.2
    plt.xlim(0, max_val)
    plt.ylim(0, max_val)
    
    # Set axes labels
    plt.xlabel('Speed Component (m/s)', fontsize=11)
    plt.ylabel('Speed Component (m/s)', fontsize=11)
    
    # Add title
    plt.title(r'Geometric Relationship: $\vec{C} = \vec{V} + \vec{U}$', fontsize=12)
    
    # Add legend outside the plot for clarity
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=10)
    
    # Add geometric constraint equation
    plt.text(0.02, 0.98, r'$\cos\theta = v/c$', transform=plt.gca().transAxes, 
             fontsize=12, verticalalignment='top', 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))
    
    # Remove grid lines for cleaner appearance
    plt.grid(False)
    
    # Adjust layout for better spacing
    plt.tight_layout()
    
    # Save in multiple formats
    plt.savefig(f'{output_dir}/vector_speed_geometry.png', format='png', bbox_inches='tight', dpi=600)
    plt.savefig(f'{output_dir}/vector_speed_geometry.svg', format='svg', bbox_inches='tight')
    plt.close()
    
    print("Figure 1 generated: vector_speed_geometry.png, vector_speed_geometry.svg")

# --- 3. Plot 2: Momentum Formula Visualization ---#
def plot_momentum_formula():
    """
    Visualization of the unified field theory momentum formula P = m(C - V)
    showing the relationship between momentum, mass, and velocity vectors
    """
    rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
    rc('text', usetex=False)
    
    plt.figure(figsize=(3.5, 2.5))
    
    # Generate data for momentum visualization
    # Use a range of velocities from 0 to just below c to avoid division by zero
    v_values = np.linspace(0, 0.9999*c, 1000)
    
    # Calculate gamma factor and mass
    gamma = 1 / np.sqrt(1 - (v_values / c)**2)
    m_values = m0 * gamma
    
    # Calculate momentum magnitude according to unified field theory
    # |P| = m * |C - V| = m * c * sqrt(1 - v^2/c^2) = m0 c
    p_utf = m_values * c * np.sqrt(1 - (v_values / c)**2)  # Should be constant m0 c
    p_relativistic = m_values * v_values  # Relativistic momentum for comparison
    
    # Plot momentum values
    plt.plot(v_values / c, p_utf / (m0 * c), color='blue', linestyle='-', linewidth=2.0, label=r'$|\vec{P}| = m|\vec{C} - \vec{V}| = m_0 c$')
    plt.plot(v_values / c, p_relativistic / (m0 * c), color='red', linestyle='--', linewidth=2.0, label=r'$|\vec{p}| = \gamma m_0 v$ (Relativistic)')
    
    # Set axis labels
    plt.xlabel('Velocity Ratio (v/c)', fontsize=11)
    plt.ylabel('Normalized Momentum (|P|/(m0 c))', fontsize=11)
    
    # Add title
    plt.title(r'Momentum Formula: $\vec{P} = m(\vec{C} - \vec{V})$', fontsize=12)
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Add text explaining the result
    plt.text(0.05, 0.8, r'$|\vec{C} - \vec{V}| = c\sqrt{1-v^2/c^2}$', fontsize=11, 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))
    plt.text(0.05, 0.65, r'$m = \gamma m_0$', fontsize=11, 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.5))
    
    # Remove grid lines
    plt.grid(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figures
    plt.savefig(f'{output_dir}/momentum_formula.png', format='png', bbox_inches='tight', dpi=600)
    plt.savefig(f'{output_dir}/momentum_formula.svg', format='svg', bbox_inches='tight')
    plt.close()
    
    print("Figure 2 generated: momentum_formula.png, momentum_formula.svg")

# --- 4. Plot 3: Mass-Velocity Relationship (Relativistic Mass) ---#
def plot_mass_velocity_relation():
    """
    Plot the mass-velocity relationship (relativistic mass increase)
    derived from the unified field theory momentum formula
    """
    rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
    rc('text', usetex=False)
    
    plt.figure(figsize=(3.5, 2.5))
    
    # Generate data
    # Use a range of velocities from 0 to just below c to avoid division by zero
    v_values = np.linspace(0, 0.9999*c, 1000)
    gamma = 1 / np.sqrt(1 - (v_values / c)**2)
    m_values = m0 * gamma
    
    # Plot mass increase
    plt.plot(v_values / c, m_values / m0, color='purple', linestyle='-', linewidth=2.0)
    
    # Add labels and title
    plt.xlabel('Velocity Ratio (v/c)', fontsize=11)
    plt.ylabel('Mass Ratio (m/m0)', fontsize=11)
    plt.title(r'Mass-Velocity Relationship: $m = \frac{m_0}{\sqrt{1-v^2/c^2}}$', fontsize=12)
    
    # Add asymptote line
    plt.axvline(x=1, color='gray', linestyle='--', linewidth=1.0)
    plt.text(0.95, 2, r'$v \to c$', fontsize=10, rotation=90, verticalalignment='center')
    
    # Remove grid lines
    plt.grid(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figures
    plt.savefig(f'{output_dir}/mass_velocity_relation.png', format='png', bbox_inches='tight', dpi=600)
    plt.savefig(f'{output_dir}/mass_velocity_relation.svg', format='svg', bbox_inches='tight')
    plt.close()
    
    print("Figure 3 generated: mass_velocity_relation.png, mass_velocity_relation.svg")

# --- 5. Plot 4: Force Equation Components ---#
def plot_force_components():
    """
    Visualization of the unified force equation components
    F = dm/dt (C - V) + m dC/dt - m dV/dt
    """
    rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
    rc('text', usetex=False)
    
    plt.figure(figsize=(3.5, 3.0))
    
    # Create a diagram to show the force components
    # Using arrows to represent different components
    
    # Plot the main force arrow
    plt.quiver(0, 0, 0, 10, angles='xy', scale_units='xy', scale=1, 
               color='black', width=0.02, label=r'$\vec{F} = \frac{d\vec{P}}{dt}$')
    
    # Plot the three components
    # 1. dm/dt (C - V)
    plt.quiver(0, 0, -3, 8, angles='xy', scale_units='xy', scale=1, 
               color='blue', width=0.015, label=r'$\frac{dm}{dt}(\vec{C} - \vec{V})$')
    
    # 2. m dC/dt
    plt.quiver(0, 0, 3, 6, angles='xy', scale_units='xy', scale=1, 
               color='red', width=0.015, label=r'$m\frac{d\vec{C}}{dt}$')
    
    # 3. -m dV/dt
    plt.quiver(0, 0, 0, 3, angles='xy', scale_units='xy', scale=1, 
               color='green', width=0.015, label=r'$-m\frac{d\vec{V}}{dt}$')
    
    # Set axis limits
    plt.xlim(-5, 5)
    plt.ylim(0, 12)
    
    # Hide axis labels as this is a conceptual diagram
    plt.xticks([])
    plt.yticks([])
    
    # Add title
    plt.title('Unified Force Equation Components', fontsize=12)
    
    # Add the full equation as text
    plt.text(0.05, 0.1, 
             r'$\vec{F} = \frac{dm}{dt}(\vec{C} - \vec{V}) + m\frac{d\vec{C}}{dt} - m\frac{d\vec{V}}{dt}$', 
             fontsize=11, ha='left', 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))
    
    # Add legend outside the plot
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=10)
    
    # Remove grid lines
    plt.grid(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figures
    plt.savefig(f'{output_dir}/force_components.png', format='png', bbox_inches='tight', dpi=600)
    plt.savefig(f'{output_dir}/force_components.svg', format='svg', bbox_inches='tight')
    plt.close()
    
    print("Figure 4 generated: force_components.png, force_components.svg")

# --- 6. Plot 5: Visualization of the Two Postulates ---#
def plot_postulates_visualization():
    """
    Visualization of the two fundamental postulates:
    1. Spacetime Unification: Time is a measure of space motion at light speed
    2. Mass Geometrization: Mass is a measure of space motion intensity
    """
    rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
    rc('text', usetex=False)
    
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.5), sharey=False)
    
    # Left plot: Spacetime Unification
    ax1 = axes[0]
    
    # Time as a function of space displacement
    t_values = np.linspace(0, 1e-8, 100)
    R_values = c * t_values  # R = C t, |C| = c
    
    ax1.plot(t_values * 1e8, R_values / 1e0, 'b-', linewidth=2.0)
    ax1.set_xlabel('Time (×10⁻⁸ s)', fontsize=11)
    ax1.set_ylabel('Space Displacement (m)', fontsize=11)
    ax1.set_title(r'Spacetime Unification: $\vec{R}(t) = \vec{C} t$', fontsize=12)
    ax1.grid(False)
    
    # Add text explaining the postulate
    ax1.text(0.1, 0.1, r'$|\vec{C}| = c = 3×10^8$ m/s', fontsize=10, 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))
    
    # Right plot: Mass Geometrization
    ax2 = axes[1]
    
    # Mass as proportional to spatial motion density
    theta_values = np.linspace(0.1, np.pi/2, 100)
    # Simplified model: m ∝ 1/sinθ (since Δn/ΔΩ ∝ 1/sinθ for spherical distribution)
    m_geo = 1 / np.sin(theta_values)
    
    ax2.plot(theta_values * 180 / np.pi, m_geo, 'r-', linewidth=2.0)
    ax2.set_xlabel('Angle θ (°)', fontsize=11)
    ax2.set_ylabel('Normalized Mass (m/m0)', fontsize=11)
    ax2.set_title(r'Mass Geometrization: $m = k \frac{Δn}{ΔΩ}$', fontsize=12)
    ax2.grid(False)
    
    # Add text explaining the postulate
    ax2.text(10, 3, r'$m ∝$ Space Motion Density', fontsize=10, 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='salmon', alpha=0.5))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figures
    plt.savefig(f'{output_dir}/postulates_visualization.png', format='png', bbox_inches='tight', dpi=600)
    plt.savefig(f'{output_dir}/postulates_visualization.svg', format='svg', bbox_inches='tight')
    plt.close()
    
    print("Figure 5 generated: postulates_visualization.png, postulates_visualization.svg")

# --- Main Execution ---#
if __name__ == "__main__":
    # Set seaborn style for publication quality
    plt.style.use('seaborn-v0_8-paper')
    
    # Generate all figures
    plot_vector_speed_geometry()
    plot_momentum_formula()
    plot_mass_velocity_relation()
    plot_force_components()
    plot_postulates_visualization()
    
    print("\nAll figures generated successfully!")
    print(f"Figures saved in: {output_dir}")
