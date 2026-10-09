#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solid Angle Geometric Visualization: 3D Space vs 2D Projection
Total solid angle (3D space): 4π steradians
Hemispherical solid angle (2D projection): 2π radians  
Geometric factor: G = 4π/2π = 2

Mathematical derivation and visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch

# Set up clean plotting style
plt.style.use('default')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True

class SolidAngleVisualizer:
    """
    Solid Angle Visualizer with Mathematical Derivation
    
    Key Mathematical Concepts:
    1. Solid angle Ω is measured in steradians (sr)
    2. For a sphere: Ω = 4π sr (total solid angle)
    3. For hemisphere projection: Ω = 2π sr
    4. Geometric factor G = 4π/2π = 2
    """
    
    def __init__(self):
        self.fig = None
        self.colors = {
            'sphere': '#FF6B6B',
            'circle': '#4ECDC4', 
            'projection': '#45B7D1',
            'vector': '#96CEB4',
            'text': '#2C3E50'
        }
        
    def mathematical_derivation(self):
        """
        Mathematical Derivation of Solid Angles:
        
        1. Solid Angle Definition:
           dΩ = dA/r^2 where dA is surface element, r is radius
           
        2. For unit sphere (r=1):
           dΩ = dA = sin(θ)dθdφ
           
        3. Total solid angle (full sphere):
           Ω_total = ∫∫ sin(θ)dθdφ 
           θ: [0,π], φ: [0,2π]
           = ∫₀^2π dφ ∫₀π sin(θ)dθ
           = 2π × [-cos(θ)]₀π
           = 2π × [1-(-1)] = 4π
           
        4. Hemispherical projection (upper hemisphere):
           Ω_hemi = ∫∫ sin(θ)dθdφ
           θ: [0,π/2], φ: [0,2π]  
           = 2π × [-cos(θ)]₀^(π/2)
           = 2π × [0-(-1)] = 2π
           
        5. Geometric Factor:
           G = Ω_total/Ω_hemi = 4π/2π = 2
        """
        print("Mathematical Derivation Complete")
        return {
            'total_solid_angle': 4*np.pi,
            'hemispherical_angle': 2*np.pi,
            'geometric_factor': 2.0
        }
    
    def create_sphere_points(self, n_points=1000):
        """生成球面上的均匀分布点"""
        # 使用球坐标系生成均匀分布
        u = np.random.uniform(0, 1, n_points)
        v = np.random.uniform(0, 1, n_points)
        
        theta = 2 * np.pi * u  # 方位角 [0, 2π]
        phi = np.arccos(2 * v - 1)  # 极角 [0, π]
        
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta) 
        z = np.cos(phi)
        
        return x, y, z
    
    def plot_3d_solid_angle(self, ax):
        """Plot 3D solid angle visualization"""
        # Create unit sphere
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_sphere, y_sphere, z_sphere, 
                       alpha=0.3, color=self.colors['sphere'])
        
        # Draw rays from origin (solid angle boundaries)
        n_rays = 16
        for i in range(n_rays):
            theta = 2 * np.pi * i / n_rays
            for j in range(8):
                phi = np.pi * j / 8
                x_end = np.sin(phi) * np.cos(theta)
                y_end = np.sin(phi) * np.sin(theta)
                z_end = np.cos(phi)
                ax.plot([0, x_end], [0, y_end], [0, z_end], 
                       color=self.colors['vector'], alpha=0.5, linewidth=0.8)
        
        # Mathematical annotation
        ax.text(0, 0, 1.4, r'Total Solid Angle = 4π sr', fontsize=12, 
               color=self.colors['text'], ha='center', weight='bold')
        ax.text(0, 0, -1.6, r'∫∫ sin(θ)dθdφ = 4π', fontsize=10, 
               color=self.colors['text'], ha='center', style='italic')
        
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5]) 
        ax.set_zlim([-1.5, 1.5])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Solid Angle: 4π steradians', fontsize=14, weight='bold')
    
    def plot_2d_projection(self, ax):
        """Plot 2D hemispherical projection"""
        # Draw unit circle
        circle = Circle((0, 0), 1, fill=False, color=self.colors['circle'], 
                       linewidth=3, linestyle='-')
        ax.add_patch(circle)
        
        # Draw semicircle (upper half)
        theta = np.linspace(0, np.pi, 100)
        x_semi = np.cos(theta)
        y_semi = np.sin(theta)
        ax.fill_between(x_semi, 0, y_semi, alpha=0.3, color=self.colors['projection'])
        
        # Draw rays
        n_rays = 12
        for i in range(n_rays + 1):
            angle = np.pi * i / n_rays
            x_end = np.cos(angle)
            y_end = np.sin(angle)
            ax.plot([0, x_end], [0, y_end], 
                   color=self.colors['vector'], linewidth=1.5, alpha=0.8)
        
        # Mathematical annotations
        ax.annotate(r'2π radians', xy=(0, 0), xytext=(-0.4, 0.4), 
                   fontsize=12, weight='bold', color=self.colors['text'],
                   arrowprops=dict(arrowstyle='->', color=self.colors['text']))
        
        # Add integration bounds
        ax.text(1.2, 0.5, r'θ ∈ [0, π/2]', fontsize=10, color='red')
        ax.text(1.2, 0.3, r'φ ∈ [0, 2π]', fontsize=10, color='red')
        
        ax.set_xlim([-1.5, 1.8])
        ax.set_ylim([-0.5, 1.5])
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('2D Projection: 2π radians', fontsize=14, weight='bold')
        ax.text(0, -0.3, 'Hemispherical Projection', fontsize=10, ha='center', 
               color=self.colors['text'], style='italic') 
   
    def plot_geometric_factor(self, ax):
        """Plot geometric factor derivation"""
        # Create clean background
        bbox = FancyBboxPatch((0.05, 0.2), 0.9, 0.6, 
                             boxstyle="round,pad=0.02", 
                             facecolor='lightblue', alpha=0.1)
        ax.add_patch(bbox)
        
        # Main formula
        ax.text(0.5, 0.7, r'Geometric Factor: $G = \frac{4\pi}{2\pi} = 2$', 
               fontsize=20, weight='bold', ha='center', va='center',
               color=self.colors['text'], transform=ax.transAxes)
        
        # Step-by-step derivation
        derivation_text = [
            r'1. Total solid angle (sphere): $\Omega_{total} = 4\pi$ sr',
            r'2. Hemispherical angle: $\Omega_{hemi} = 2\pi$ sr', 
            r'3. Geometric factor: $G = \frac{\Omega_{total}}{\Omega_{hemi}} = \frac{4\pi}{2\pi} = 2$',
            r'4. Physical meaning: 3D → 2D projection scaling factor'
        ]
        
        y_positions = [0.55, 0.45, 0.35, 0.25]
        colors = ['red', 'blue', 'green', 'purple']
        
        for i, (text, y_pos, color) in enumerate(zip(derivation_text, y_positions, colors)):
            ax.text(0.05, y_pos, text, fontsize=12, ha='left', va='center',
                   color=color, transform=ax.transAxes, weight='bold')
        
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.axis('off')
        ax.set_title('Mathematical Derivation: G = 2', fontsize=16, weight='bold', pad=20)
    
    def create_comprehensive_visualization(self):
        """Create comprehensive solid angle visualization"""
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.suptitle('Solid Angle Geometry: 3D Space vs 2D Projection\nG = 4π/2π = 2', 
                         fontsize=18, weight='bold', y=0.95)
        
        # Print mathematical derivation first
        results = self.mathematical_derivation()
        
        # 3D solid angle plot
        ax1 = self.fig.add_subplot(221, projection='3d')
        self.plot_3d_solid_angle(ax1)
        
        # 2D projection plot  
        ax2 = self.fig.add_subplot(222)
        self.plot_2d_projection(ax2)
        
        # Geometric factor derivation
        ax3 = self.fig.add_subplot(223)
        self.plot_geometric_factor(ax3)
        
        # Numerical comparison
        ax4 = self.fig.add_subplot(224)
        self.plot_numerical_comparison(ax4)
        
        plt.tight_layout()
        return self.fig
    
    def plot_numerical_comparison(self, ax):
        """Plot numerical comparison"""
        categories = ['3D Solid Angle\n(4π sr)', '2D Projection\n(2π rad)', 'Geometric Factor\n(G)']
        values = [4*np.pi, 2*np.pi, 2.0]
        colors = [self.colors['sphere'], self.colors['circle'], self.colors['projection']]
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add numerical labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if value == 2.0:
                label = f'{value:.1f}'
            else:
                label = f'{value:.3f}\n({value/np.pi:.1f}π)'
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   label, ha='center', va='bottom', fontsize=11, weight='bold')
        
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title('Numerical Comparison', fontsize=14, weight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0, max(values) * 1.3])
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=0, ha='center', fontsize=10)

def create_interactive_demo():
    """Create interactive demonstration with clear mathematical derivation"""
    print("=" * 60)
    print("SOLID ANGLE GEOMETRIC ANALYSIS")
    print("=" * 60)
    print("Mathematical Derivation:")
    print("1. Solid angle element: dΩ = sin(θ)dθdφ")
    print("2. Total solid angle (sphere): ∫∫ sin(θ)dθdφ = 4π sr")
    print("   Integration bounds: θ ∈ [0,π], φ ∈ [0,2π]")
    print("3. Hemispherical angle: ∫∫ sin(θ)dθdφ = 2π sr") 
    print("   Integration bounds: θ ∈ [0,π/2], φ ∈ [0,2π]")
    print("4. Geometric factor: G = 4π/2π = 2")
    print("=" * 60)
    
    # Numerical verification
    total_angle = 4 * np.pi
    hemi_angle = 2 * np.pi
    geometric_factor = total_angle / hemi_angle
    
    print(f"Numerical Results:")
    print(f"• Total solid angle: {total_angle:.6f} steradians")
    print(f"• Hemispherical angle: {hemi_angle:.6f} steradians")
    print(f"• Geometric factor G: {geometric_factor:.1f}")
    print("=" * 60)
    
    # Create visualization
    visualizer = SolidAngleVisualizer()
    fig = visualizer.create_comprehensive_visualization()
    
    # Save figure
    plt.savefig('solid_angle_geometry.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("✓ Visualization saved as: solid_angle_geometry.png")
    
    plt.show()
    return visualizer

def verify_integration():
    """Numerical verification of the analytical results"""
    print("\nNumerical Integration Verification:")
    print("-" * 40)
    
    # Numerical integration for verification
    def integrand(theta, phi):
        return np.sin(theta)
    
    # Full sphere integration (Monte Carlo approximation)
    n_samples = 1000000
    theta_full = np.random.uniform(0, np.pi, n_samples)
    phi_full = np.random.uniform(0, 2*np.pi, n_samples)
    
    integral_full = np.mean(integrand(theta_full, phi_full)) * np.pi * 2 * np.pi
    
    # Hemisphere integration
    theta_hemi = np.random.uniform(0, np.pi/2, n_samples)
    phi_hemi = np.random.uniform(0, 2*np.pi, n_samples)
    
    integral_hemi = np.mean(integrand(theta_hemi, phi_hemi)) * (np.pi/2) * 2 * np.pi
    
    print(f"Analytical full sphere: 4π = {4*np.pi:.6f}")
    print(f"Numerical full sphere: {integral_full:.6f}")
    print(f"Analytical hemisphere: 2π = {2*np.pi:.6f}")
    print(f"Numerical hemisphere: {integral_hemi:.6f}")
    print(f"Geometric factor (analytical): {4*np.pi/(2*np.pi):.6f}")
    print(f"Geometric factor (numerical): {integral_full/integral_hemi:.6f}")

if __name__ == "__main__":
    # Run demonstration
    demo = create_interactive_demo()
    
    # Verify with numerical integration
    verify_integration()