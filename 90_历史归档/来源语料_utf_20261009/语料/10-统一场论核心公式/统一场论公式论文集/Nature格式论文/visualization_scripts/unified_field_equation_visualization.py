# -*- coding: utf-8 -*-
import sys
import io
import os

# Ensure UTF-8 encoding for standard output
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Set environment variable to ensure proper matplotlib rendering
os.environ['PYTHONIOENCODING'] = 'utf-8'

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Configure matplotlib for better rendering with Chinese support
plt.rcParams.update({
    'text.usetex': False,
    'mathtext.fontset': 'cm',
    'mathtext.default': 'it',
    'axes.unicode_minus': False,
    'font.family': ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'serif', 'DejaVu Serif'],
    'font.serif': ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Computer Modern', 'Times New Roman', 'DejaVu Serif'],
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'figure.autolayout': True
})

class UnifiedFieldPlotter:
    """Create Nature-style visualizations for unified gravitational and electromagnetic field equations"""
    
    def __init__(self):
        # Nature journal common color palette
        self.nature_colors = {
            'blue': '#0173B2',
            'cyan': '#029E73', 
            'green': '#009E73',
            'yellow': '#D55E00',
            'orange': '#E69F00',
            'red': '#CC78BC',
            'purple': '#56B4E9'
        }
        # Set default parameters
        self.figsize = (10, 7)
        self.dpi = 300
    
    def cross_product_visualization(self, output_file="cross_product_3d.png"):
        """Visualize cross product operation \vec{A} \times \vec{B}"""
        
        # Create figure
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # Define two vectors
        A = np.array([1, 0, 0])  # Vector A along x-axis
        B = np.array([0, 1, 0])  # Vector B along y-axis
        C = np.cross(A, B)       # Cross product result, should be along z-axis
        
        # Plot vectors
        origin = np.zeros(3)
        
        # Plot vector A
        ax.quiver(*origin, *A, color=self.nature_colors['blue'], arrow_length_ratio=0.15, linewidth=2)
        
        # Plot vector B
        ax.quiver(*origin, *B, color=self.nature_colors['green'], arrow_length_ratio=0.15, linewidth=2)
        
        # Plot cross product result C
        ax.quiver(*origin, *C, color=self.nature_colors['red'], arrow_length_ratio=0.15, linewidth=3)
        
        # Add vector labels
        ax.text(A[0]*1.1, A[1], A[2], '\\vec{A}', color=self.nature_colors['blue'], fontsize=14)
        ax.text(B[0], B[1]*1.1, B[2], '\\vec{B}', color=self.nature_colors['green'], fontsize=14)
        ax.text(C[0], C[1], C[2]*1.3, '\\vec{A} \\times \\vec{B}', color=self.nature_colors['red'], fontsize=14)
        
        # Plot coordinate plane
        xx, yy = np.meshgrid([-1, 1], [-1, 1])
        zz = np.zeros_like(xx)
        ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')
        
        # Set axis limits and labels
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        
        # Set title
        ax.set_title('Geometric Representation of Cross Product \\vec{A} \\times \\vec{B}', fontsize=16, pad=20)
        
        # Add custom legend
        from matplotlib.lines import Line2D
        custom_lines = [
            Line2D([0], [0], color=self.nature_colors['blue'], lw=2),
            Line2D([0], [0], color=self.nature_colors['green'], lw=2),
            Line2D([0], [0], color=self.nature_colors['red'], lw=3)
        ]
        ax.legend(custom_lines, ['\\vec{A}', '\\vec{B}', '\\vec{A} \\times \\vec{B}'], 
                 loc='upper left', fontsize=12)
        
        # Set viewing angle
        ax.view_init(elev=30, azim=45)
        
        # Add equation
        fig.text(0.5, 0.01, 'Unified Equation of Gravitational and Electromagnetic Fields: \\vec{A} \\times \\vec{B} = \\frac{c^{2}}{\\epsilon_0}\\vec{j} + \\frac{1}{\\epsilon_0}\\frac{\\partial\\vec{D}}{\\partial t}', 
                 ha='center', fontsize=14, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
        os.makedirs(output_dir, exist_ok=True)
        # Save with full path
        full_output_path = os.path.join(output_dir, output_file)
        plt.savefig(full_output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        print(f"Cross product visualization saved to: {full_output_path}")

    
    def field_interaction_visualization(self, output_file="field_interaction_visualization.png"):
        """Visualize the interaction between gravitational and electromagnetic fields"""
        
        # Create figure
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = fig.add_subplot(111)
        
        # Plot gravitational field vectors
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        
        # Simulate gravitational field from central mass
        r = np.sqrt(X**2 + Y**2)
        r[r < 0.1] = 0.1
        Gx = -X / r**3
        Gy = -Y / r**3
        
        # Simulate electromagnetic field (circular)
        Ex = -Y / r**2
        Ey = X / r**2
        
        # Plot gravitational field
        stream1 = ax.streamplot(X, Y, Gx, Gy, color=self.nature_colors['blue'], linewidth=1, density=1.5)
        
        # Plot electromagnetic field (circular)
        stream2 = ax.streamplot(X, Y, Ex, Ey, color=self.nature_colors['green'], linewidth=1, density=1.5)
        
        # Plot central source
        ax.plot(0, 0, 'o', color='black', markersize=10)
        
        # Plot circular indication for cross product direction (perpendicular to paper)
        circle = plt.Circle((0, 0), 2.5, fill=False, 
                           color=self.nature_colors['red'], linestyle='--', alpha=0.7)
        ax.add_patch(circle)
        
        # Add direction indicator
        angle = np.pi/6
        arrow_x = 2.5 * np.cos(angle)
        arrow_y = 2.5 * np.sin(angle)
        ax.annotate('', xy=(arrow_x, arrow_y), xytext=(0.8*arrow_x, 0.8*arrow_y),
                    arrowprops=dict(facecolor=self.nature_colors['red'], shrink=0, width=2, headwidth=10))
        ax.text(2.7 * np.cos(angle), 2.7 * np.sin(angle), 'Interaction Direction', 
                color=self.nature_colors['red'], fontsize=12, rotation=angle*180/np.pi)
        
        # Set title and labels
        ax.set_title('Visualization of Gravitational and Electromagnetic Field Interaction', fontsize=16)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.grid(False)
        # Add legend (using custom Line2D objects)
        from matplotlib.lines import Line2D
        custom_lines = [
            Line2D([0], [0], color=self.nature_colors['blue'], lw=2),
            Line2D([0], [0], color=self.nature_colors['green'], lw=2)
        ]
        ax.legend(custom_lines, ['Gravitational Field \\vec{A}', 'Electromagnetic Field \\vec{B}'], loc='lower right')
        
        # Add equation
        fig.text(0.5, 0.01, 'Unified Equation of Gravitational and Electromagnetic Fields: \\vec{A} \\times \\vec{B} = \\frac{c^{2}}{\\epsilon_0}\\vec{j} + \\frac{1}{\\epsilon_0}\\frac{\\partial\\vec{D}}{\\partial t}', 
                 ha='center', fontsize=14, fontweight='bold')
        
        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save with full path
        full_output_path = os.path.join(output_dir, output_file)
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.savefig(full_output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        print(f"Field interaction visualization saved to: {full_output_path}")
    
    def maxwell_ampere_comparison(self, output_file="maxwell_ampere_comparison.png"):
        """Visualize the relationship between Ampère-Maxwell law and unified equation"""
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi)
        
        # Left: Ampère-Maxwell law
        ax1.text(0.5, 0.8, 'Ampère-Maxwell Law', ha='center', fontsize=16, fontweight='bold')
        ax1.text(0.5, 0.6, '$\\nabla \\times \\vec{B} = \\mu_0\\vec{j} + \\mu_0\\epsilon_0\\frac{\\partial\\vec{E}}{\\partial t}$', 
                ha='center', fontsize=16)
        
        # Add current and displacement current visualization
        x = np.linspace(-1, 1, 50)
        y = np.zeros_like(x)
        ax1.plot(x, y, 'k-', linewidth=3)
        ax1.plot(0, 0, 'o', color='black', markersize=8)
        
        # Add current direction arrow
        ax1.annotate('', xy=(0.8, 0.1), xytext=(0.2, 0.1),
                    arrowprops=dict(facecolor=self.nature_colors['blue'], shrink=0, width=2, headwidth=8))
        ax1.text(0.5, 0.15, 'Conduction Current', color=self.nature_colors['blue'], fontsize=12)
        
        # Add displacement current region
        circle = plt.Circle((0, 0), 0.5, fill=False, color=self.nature_colors['red'], linestyle='--', linewidth=2)
        ax1.add_patch(circle)
        ax1.text(0, -0.6, 'Displacement Current Region', color=self.nature_colors['red'], fontsize=12)
        
        # Add magnetic field lines
        for r in np.linspace(0.6, 1.0, 3):
            theta = np.linspace(0, 2*np.pi, 100)
            circle_x = r * np.cos(theta)
            circle_y = r * np.sin(theta)
            ax1.plot(circle_x, circle_y, self.nature_colors['green'], linestyle='-', alpha=0.7)
        
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_aspect('equal')
        ax1.axis('off')
        
        # Right: Unified field theory equation
        ax2.text(0.5, 0.8, 'Unified Field Theory Equation', ha='center', fontsize=16, fontweight='bold')
        ax2.text(0.5, 0.6, '$\\vec{A} \\times \\vec{B} = \\frac{c^{2}}{\\epsilon_0}\\vec{j} + \\frac{1}{\\epsilon_0}\\frac{\\partial\\vec{D}}{\\partial t}$', 
                ha='center', fontsize=16)
        
        # Add field interaction visualization
        # Plot gravitational field (radial)
        for angle in np.linspace(0, 2*np.pi, 8):
            r_values = np.linspace(0.1, 1.0, 50)
            x = r_values * np.cos(angle)
            y = r_values * np.sin(angle)
            ax2.plot(x, y, self.nature_colors['blue'], linestyle='-', alpha=0.7)
        
        # Plot electromagnetic field (circular)
        for r in np.linspace(0.3, 0.9, 3):
            theta = np.linspace(0, 2*np.pi, 100)
            circle_x = r * np.cos(theta)
            circle_y = r * np.sin(theta)
            ax2.plot(circle_x, circle_y, self.nature_colors['green'], linestyle='-', alpha=0.7)
        
        # Add central source
        ax2.plot(0, 0, 'o', color='black', markersize=8)
        
        # Add interaction indicator
        arrow_x = 1.0 * np.cos(np.pi/4)
        arrow_y = 1.0 * np.sin(np.pi/4)
        ax2.annotate('', xy=(arrow_x, arrow_y), xytext=(0.7*arrow_x, 0.7*arrow_y),
                    arrowprops=dict(facecolor=self.nature_colors['red'], shrink=0, width=2, headwidth=8))
        ax2.text(1.1 * np.cos(np.pi/4), 1.1 * np.sin(np.pi/4), 'Field Interaction', 
                color=self.nature_colors['red'], fontsize=12, rotation=45)
        
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-1.2, 1.2)
        ax2.set_aspect('equal')
        ax2.axis('off')
        
        # Add unified equation
        fig.text(0.5, 0.01, 'Unified Equation of Gravitational and Electromagnetic Fields: \\vec{A} \\times \\vec{B} = \\frac{c^{2}}{\\epsilon_0}\\vec{j} + \\frac{1}{\\epsilon_0}\\frac{\\partial\\vec{D}}{\\partial t}', 
                 ha='center', fontsize=14, fontweight='bold')
        
        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save with full path
        full_output_path = os.path.join(output_dir, output_file)
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.savefig(full_output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        print(f"Ampère-Maxwell law and unified equation comparison saved to: {full_output_path}")
    
    def field_transformation_3d(self, output_file="field_transformation_3d.png"):
        """3D visualization of transformation from gravitational to electromagnetic field"""
        
        # Create figure
        fig = plt.figure(figsize=(12, 9), dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create grid
        phi = np.linspace(0, 2 * np.pi, 20)
        theta = np.linspace(0, np.pi, 10)
        
        # Convert spherical to Cartesian coordinates
        phi_grid, theta_grid = np.meshgrid(phi, theta)
        
        # Radial field (gravitational field)
        r = 1.0
        x1 = r * np.sin(theta_grid) * np.cos(phi_grid)
        y1 = r * np.sin(theta_grid) * np.sin(phi_grid)
        z1 = r * np.cos(theta_grid)
        
        # Radial vectors
        u1 = x1
        v1 = y1
        w1 = z1
        
        # Circular field (electromagnetic field)
        r2 = 1.2
        x2 = r2 * np.sin(theta_grid) * np.cos(phi_grid)
        y2 = r2 * np.sin(theta_grid) * np.sin(phi_grid)
        z2 = r2 * np.cos(theta_grid)
        
        # Circular vectors (perpendicular to radial direction)
        u2 = -y2
        v2 = x2
        w2 = np.zeros_like(z2)
        
        # Plot gravitational field (radial)
        ax.quiver(x1, y1, z1, u1, v1, w1, 
                 color=self.nature_colors['blue'], length=0.2, normalize=True, alpha=0.7)
        
        # Plot electromagnetic field (circular)
        ax.quiver(x2, y2, z2, u2, v2, w2, 
                 color=self.nature_colors['green'], length=0.2, normalize=True, alpha=0.7)
        
        # Plot center
        ax.scatter(0, 0, 0, color='black', s=100)
        
        # Set title and labels
        ax.set_title('3D Visualization of Transformation and Interaction Between Gravitational and Electromagnetic Fields', fontsize=16, pad=20)
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        
        # Set axis limits
        max_range = 1.5
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        # Set viewing angle
        ax.view_init(elev=30, azim=45)
        
        # Add custom legend
        from matplotlib.lines import Line2D
        custom_lines = [
            Line2D([0], [0], color=self.nature_colors['blue'], lw=2),
            Line2D([0], [0], color=self.nature_colors['green'], lw=2)
        ]
        ax.legend(custom_lines, ['Gravitational Field \\vec{A}', 'Electromagnetic Field \\vec{B}'], 
                 loc='upper right', fontsize=12)
        
        # Add equation
        fig.text(0.5, 0.01, 'Unified Equation of Gravitational and Electromagnetic Fields: \\vec{A} \\times \\vec{B} = \\frac{c^{2}}{\\epsilon_0}\\vec{j} + \\frac{1}{\\epsilon_0}\\frac{\\partial\\vec{D}}{\\partial t}', 
                 ha='center', fontsize=14, fontweight='bold')
        
        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save with full path
        full_output_path = os.path.join(output_dir, output_file)
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.savefig(full_output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        print(f"3D field transformation visualization saved to: {full_output_path}")

if __name__ == "__main__":
    # Create visualization directory
    import os
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize plotter
    plotter = UnifiedFieldPlotter()
    
    # Generate various visualizations
    plotter.cross_product_visualization(os.path.join(output_dir, 'cross_product_3d.png'))
    plotter.field_interaction_visualization(os.path.join(output_dir, 'field_interaction.png'))
    plotter.maxwell_ampere_comparison(os.path.join(output_dir, 'maxwell_ampere_comparison.png'))
    plotter.field_transformation_3d(os.path.join(output_dir, 'field_transformation_3d.png'))
    
    print("All unified field theory equation visualization images have been successfully generated!")