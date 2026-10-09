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
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.gridspec import GridSpec

# Configure matplotlib for better rendering with Chinese support
plt.rcParams.update({
    'text.usetex': False,
    'mathtext.fontset': 'cm',  # 使用Computer Modern字体
    'mathtext.default': 'it',  # 默认使用斜体
    'axes.unicode_minus': False,
    'font.family': ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'serif', 'DejaVu Serif'],
    'font.serif': ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Computer Modern', 'Times New Roman', 'DejaVu Serif'],
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'figure.autolayout': True
})

class GrandUnificationPlotter:
    """Create Nature-style visualizations for cosmic grand unification equations"""
    
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
        self.figsize = (12, 10)
        self.dpi = 300
    
    def space_time_visualization(self, output_file="space_time_visualization.png"):
        """Visualize space-time unification and 3D spiral space-time"""
        
        # Create figure
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        gs = GridSpec(2, 1, height_ratios=[1, 1])
        
        # Upper part: space-time grid visualization
        ax1 = fig.add_subplot(gs[0], projection='3d')
        
        # Create grid
        x = np.linspace(-1, 1, 10)
        y = np.linspace(-1, 1, 10)
        z = np.linspace(-1, 1, 10)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Plot grid lines
        for i in range(len(x)):
            for j in range(len(y)):
                ax1.plot(X[i, j, :], Y[i, j, :], Z[i, j, :], 'k-', alpha=0.1)
        for i in range(len(x)):
            for k in range(len(z)):
                ax1.plot(X[i, :, k], Y[i, :, k], Z[i, :, k], 'k-', alpha=0.1)
        for j in range(len(y)):
            for k in range(len(z)):
                ax1.plot(X[:, j, k], Y[:, j, k], Z[:, j, k], 'k-', alpha=0.1)
        
        # Add time dimension visualization
        time_color = self.nature_colors['blue']
        t = np.linspace(-1, 1, 100)
        x_t = 0.3 * np.cos(2*np.pi*t)
        y_t = 0.3 * np.sin(2*np.pi*t)
        z_t = t
        ax1.plot(x_t, y_t, z_t, color=time_color, linewidth=3)
        ax1.scatter(x_t[-1], y_t[-1], z_t[-1], color=time_color, s=100, zorder=5)
        ax1.text(x_t[-1]+0.1, y_t[-1]+0.1, z_t[-1], 'Time Direction', color=time_color, fontsize=12)
        
        # Set title and labels
        ax1.set_title('Four-Dimensional Space-Time Unification Illustration', fontsize=16, pad=20)
        ax1.set_xlabel('X', fontsize=12)
        ax1.set_ylabel('Y', fontsize=12)
        ax1.set_zlabel('Z', fontsize=12)
        
        # Set axis limits
        ax1.set_xlim([-1.2, 1.2])
        ax1.set_ylim([-1.2, 1.2])
        ax1.set_zlim([-1.2, 1.2])
        
        # Set viewing angle
        ax1.view_init(elev=30, azim=45)
        
        # Lower part: 3D spiral space-time
        ax2 = fig.add_subplot(gs[1], projection='3d')
        
        # Create spiral
        t = np.linspace(0, 6*np.pi, 200)
        r = 1.0
        x = r * np.cos(t)
        y = r * np.sin(t)
        z = t/(2*np.pi)
        
        # Plot spiral
        ax2.plot(x, y, z, color=self.nature_colors['purple'], linewidth=3)
        
        # Plot spiral tube surface
        theta = np.linspace(0, 2*np.pi, 20)
        t_grid, theta_grid = np.meshgrid(t, theta)
        r_surface = r + 0.05 * np.cos(theta_grid)
        x_surface = r_surface * np.cos(t_grid)
        y_surface = r_surface * np.sin(t_grid)
        z_surface = t_grid/(2*np.pi)
        
        ax2.plot_surface(x_surface, y_surface, z_surface, color=self.nature_colors['purple'], 
                        alpha=0.3, edgecolor='none')
        
        # Set title and labels
        ax2.set_title('3D Spiral Space-Time Structure Illustration', fontsize=16, pad=20)
        ax2.set_xlabel('X', fontsize=12)
        ax2.set_ylabel('Y', fontsize=12)
        ax2.set_zlabel('Z', fontsize=12)
        
        # Set axis limits
        ax2.set_xlim([-1.2, 1.2])
        ax2.set_ylim([-1.2, 1.2])
        ax2.set_zlim([0, 3])
        
        # Set viewing angle
        ax2.view_init(elev=30, azim=45)
        
        # Add equation description
        fig.text(0.5, 0.01, 'Unified Field Theory: Space-Time Unification and 3D Spiral Space-Time Structure', 
                 ha='center', fontsize=14, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.98])
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
        print(f"Space-time visualization saved as: {output_file}")
    
    def grand_unification_illustration(self, output_file="grand_unification_illustration.png"):
        """Visualize the physical significance of cosmic grand unification equations"""
        
        # Create figure
        fig = plt.figure(figsize=(12, 8), dpi=self.dpi)
        
        # Use GridSpec layout
        gs = GridSpec(1, 1)
        ax = fig.add_subplot(gs[0])
        
        # Plot relationship network between unified field theory equations
        # Set node positions
        nodes = {
            'Space-Time Unification': (0.2, 0.8),
            '3D Spiral Space-Time': (0.5, 0.9),
            'Mass Definition': (0.8, 0.8),
            'Gravitational Field Definition': (0.1, 0.5),
            'Momentum Equation': (0.5, 0.6),
            'Electromagnetic Field Equation': (0.9, 0.5),
            'Energy Equation': (0.5, 0.3),
            'Cosmic Grand Unification Equation': (0.5, 0.1)
        }
        
        # Plot connections between nodes
        connections = [
            ('Space-Time Unification', '3D Spiral Space-Time'),
            ('3D Spiral Space-Time', 'Mass Definition'),
            ('Mass Definition', 'Gravitational Field Definition'),
            ('Gravitational Field Definition', 'Momentum Equation'),
            ('Mass Definition', 'Momentum Equation'),
            ('Momentum Equation', 'Electromagnetic Field Equation'),
            ('Electromagnetic Field Equation', 'Energy Equation'),
            ('Momentum Equation', 'Energy Equation'),
            ('Gravitational Field Definition', 'Energy Equation'),
            ('Energy Equation', 'Cosmic Grand Unification Equation'),
            ('Electromagnetic Field Equation', 'Cosmic Grand Unification Equation'),
            ('Gravitational Field Definition', 'Cosmic Grand Unification Equation')
        ]
        
        # Plot connection lines
        for start, end in connections:
            x_start, y_start = nodes[start]
            x_end, y_end = nodes[end]
            ax.plot([x_start, x_end], [y_start, y_end], 'k-', alpha=0.5, linewidth=1)
        
        # Plot nodes
        node_colors = {
            'Space-Time Unification': self.nature_colors['blue'],
            '3D Spiral Space-Time': self.nature_colors['cyan'],
            'Mass Definition': self.nature_colors['green'],
            'Gravitational Field Definition': self.nature_colors['yellow'],
            'Momentum Equation': self.nature_colors['orange'],
            'Electromagnetic Field Equation': self.nature_colors['red'],
            'Energy Equation': self.nature_colors['purple'],
            'Cosmic Grand Unification Equation': 'black'
        }
        
        for node, (x, y) in nodes.items():
            color = node_colors[node]
            size = 300 if node == 'Cosmic Grand Unification Equation' else 200
            ax.scatter(x, y, color=color, s=size, edgecolor='white', linewidth=2, zorder=3)
            ax.text(x, y, node, ha='center', va='center', fontsize=10, fontweight='bold', zorder=4)
        
        # Add equation illustration
        equation_y = 0.1
        ax.text(0.5, equation_y - 0.08, 'Cosmic Grand Unification Equation Integrates All Fundamental Interactions', 
                ha='center', fontsize=14, fontweight='bold')
        
        # Set axis
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.axis('off')
        
        # Set title
        ax.set_title('Unified Field Theory Equation System and Cosmic Grand Unification Equation Relationship', fontsize=18, pad=20)
        
        plt.tight_layout()
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
        print(f"Cosmic grand unification equation relationship diagram saved as: {output_file}")
    
    def field_interaction_3d(self, output_file="field_interaction_3d.png"):
        """3D visualization of the unification of four fundamental interactions"""
        
        # Create figure
        fig = plt.figure(figsize=(12, 10), dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create spherical grid
        phi = np.linspace(0, 2 * np.pi, 30)
        theta = np.linspace(0, np.pi, 15)
        phi_grid, theta_grid = np.meshgrid(phi, theta)
        
        # Convert to Cartesian coordinates
        r = 1.0
        x = r * np.sin(theta_grid) * np.cos(phi_grid)
        y = r * np.sin(theta_grid) * np.sin(phi_grid)
        z = r * np.cos(theta_grid)
        
        # Plot gravitational field (radial)
        u_grav = x
        v_grav = y
        w_grav = z
        ax.quiver(x, y, z, u_grav, v_grav, w_grav, 
                 color=self.nature_colors['blue'], length=0.2, normalize=True, 
                 alpha=0.6, label='Gravitational Field')
        
        # Plot electromagnetic field (circular)
        u_elec = -y
        v_elec = x
        w_elec = np.zeros_like(z)
        ax.quiver(x, y, z, u_elec, v_elec, w_elec, 
                 color=self.nature_colors['red'], length=0.2, normalize=True, 
                 alpha=0.6, label='Electromagnetic Field')
        
        # Plot weak interaction (spiral direction)
        u_weak = -y * np.cos(theta_grid)
        v_weak = x * np.cos(theta_grid)
        w_weak = np.sin(theta_grid)
        ax.quiver(x, y, z, u_weak, v_weak, w_weak, 
                 color=self.nature_colors['green'], length=0.2, normalize=True, 
                 alpha=0.6, label='Weak Interaction')
        
        # Plot strong interaction (radial oscillation)
        r_strong = r + 0.1 * np.sin(4*phi_grid)
        x_strong = r_strong * np.sin(theta_grid) * np.cos(phi_grid)
        y_strong = r_strong * np.sin(theta_grid) * np.sin(phi_grid)
        z_strong = r_strong * np.cos(theta_grid)
        u_strong = x_strong - x
        v_strong = y_strong - y
        w_strong = z_strong - z
        ax.quiver(x, y, z, u_strong, v_strong, w_strong, 
                 color=self.nature_colors['orange'], length=0.2, normalize=True, 
                 alpha=0.6, label='Strong Interaction')
        
        # Plot central unification point
        ax.scatter(0, 0, 0, color='black', s=200, edgecolor='white', linewidth=2)
        ax.text(0, 0, 0, 'Unified', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Set title and labels
        ax.set_title('3D Visualization of the Unification of Four Fundamental Interactions', fontsize=16, pad=20)
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
        
        # Add legend
        ax.legend(loc='upper right', fontsize=12)
        
        # Add equation description
        fig.text(0.5, 0.01, 'Cosmic Grand Unification: Theoretical Unification of All Fundamental Interactions', 
                 ha='center', fontsize=14, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
        print(f"Four fundamental interactions unification visualization saved as: {output_file}")
    
    def physical_constants_relation(self, output_file="physical_constants_relation.png"):
        """Visualize the relationships between physical constants"""
        
        # Create figure
        fig = plt.figure(figsize=(12, 8), dpi=self.dpi)
        ax = fig.add_subplot(111)
        
        # Define physical constants and their relationships
        constants = {
            'Speed of Light c': {'value': 3e8, 'color': self.nature_colors['blue'], 'pos': (0.2, 0.8)},
            'Gravitational Constant G': {'value': 6.67e-11, 'color': self.nature_colors['green'], 'pos': (0.8, 0.8)},
            'Planck Constant ħ': {'value': 1.05e-34, 'color': self.nature_colors['red'], 'pos': (0.5, 0.3)},
            'Vacuum Permittivity ε₀': {'value': 8.85e-12, 'color': self.nature_colors['orange'], 'pos': (0.2, 0.2)},
            'Vacuum Permeability μ₀': {'value': 1.26e-6, 'color': self.nature_colors['purple'], 'pos': (0.8, 0.2)}
        }
        
        # Plot constant nodes
        for name, data in constants.items():
            x, y = data['pos']
            ax.scatter(x, y, s=300, color=data['color'], edgecolor='white', linewidth=2, zorder=3)
            ax.text(x, y, name, ha='center', va='center', fontsize=12, fontweight='bold', color='white')
            # Display value
            ax.text(x, y-0.1, f"{data['value']:g}", ha='center', fontsize=10)
        
        # Plot relationship lines between constants
        relations = [
            ('Speed of Light c', 'Vacuum Permittivity ε₀'),
            ('Speed of Light c', 'Vacuum Permeability μ₀'),
            ('Gravitational Constant G', 'Planck Constant ħ'),
            ('Speed of Light c', 'Planck Constant ħ'),
            ('Vacuum Permittivity ε₀', 'Vacuum Permeability μ₀'),
            ('Vacuum Permeability μ₀', 'Speed of Light c'),
            ('Vacuum Permittivity ε₀', 'Speed of Light c')
        ]
        
        for start, end in relations:
            x1, y1 = constants[start]['pos']
            x2, y2 = constants[end]['pos']
            ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.6, linewidth=1)
        
        # Add equations using proper LaTeX formatting with newline characters
        equations = r"""$c = \frac{1}{\sqrt{\mu_0 \epsilon_0}}$
$E = mc^2$
$E = \hbar \omega$
$F = G\frac{m_1m_2}{r^2}$"""
        ax.text(0.5, 0.5, equations,
                ha='center', va='center', fontsize=16, bbox=dict(boxstyle="round,pad=1", facecolor='lightgray', alpha=0.7))
        
        # Add description
        fig.text(0.5, 0.01, 'Physical Constant Relationships in Unified Field Theory: Bridge from Quantum Mechanics to General Relativity', 
                 ha='center', fontsize=14, fontweight='bold')
        
        # Set axis
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.axis('off')
        
        # Set title
        ax.set_title('Physical Constants Relationship Visualization', fontsize=18, pad=20)
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
        print(f"Physical constants relationship visualization saved as: {output_file}")

def main():
    # Create visualization instance
    visualizer = GrandUnificationPlotter()
    
    # Create output directory
    output_dir = "visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate all visualization images
    visualizer.space_time_visualization(os.path.join(output_dir, "space_time_visualization.png"))
    visualizer.grand_unification_illustration(os.path.join(output_dir, "grand_unification_illustration.png"))
    visualizer.field_interaction_3d(os.path.join(output_dir, "field_interaction_3d.png"))
    visualizer.physical_constants_relation(os.path.join(output_dir, "physical_constants_relation.png"))
    
    print("\nAll unified field theory visualization images have been successfully generated!")

if __name__ == "__main__":
    main()