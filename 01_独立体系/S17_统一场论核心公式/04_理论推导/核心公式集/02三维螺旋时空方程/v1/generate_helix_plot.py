#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a publication-ready 3D helix plot for the cylindrical spiral spacetime equation
from Zhang Xiangqian's Unified Field Theory.

Equation: vec{R}(t) = r cos(omega t) hat{i} + r sin(omega t) hat{j} + p t hat{k}

Objective: To accurately and clearly depict the 3D cylindrical spiral motion of space points,
adhering to the highest standards of scientific journals.

Key Specifications:
1. Physics & Mathematical Accuracy:
   - Equation: vec{R}(t) = r cos(omega t) hat{i} + r sin(omega t) hat{j} + p t hat{k}
   - Physical Parameters: r=1.0 m, omega=1.0 rad/s, p=1.0 m/s, t from 0 to 10 s
   - Verify speed constraint: sqrt(r^2 omega^2 + p^2) = c (constant)

2. Clarity & Interpretability:
   - Axes Labels: Position components with SI units, LaTeX rendered
   - Title: Descriptive,概括图的核心内容
   - Legend: Clear, informative
   - Font: Professional, consistent

3. Aesthetics & Professionalism:
   - Plotting Style: Scientific, publication-ready
   - Color Palette: Colorblind-friendly, publication-standard
   - Line Styles: Clear, professional

4. Mathematical Representation:
   - All mathematical expressions in LaTeX

5. Technical Output:
   - Format: Vector format (PDF, SVG) and high-res PNG
   - Resolution: 600 DPI
   - Figure Size: Suitable for journal publication

6. Reproducibility:
   - Code Comments: Extensive, explaining steps and parameters
   - Parameterization: All key parameters defined at the beginning

7. Annotations & Emphasis:
   - Highlight key features: Helix radius, pitch, direction
   - Add equation annotation

Preferred Libraries:
- Core: matplotlib, numpy
- Enhancements: mpl_toolkits.mplot3d for 3D plotting
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Create img directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# --- 1. Physics & Mathematical Accuracy ---#
# Physical Parameters (SI units)
r = 1.0        # Helix radius (m)
omega = 1.0    # Angular velocity (rad/s)
p = 1.0        # Axial velocity (m/s)
t = np.linspace(0, 10, 1000)  # Time range (s)

# Calculate speed to verify constant constraint
speed = np.sqrt(r**2 * omega**2 + p**2)
print(f"Constant speed verification: v = {speed:.4f} m/s")

# Calculate position components using the cylindrical spiral equation
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = p * t

# --- 2. Plotting Setup ---#
# Set matplotlib settings for publication-quality
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern'],
    'text.usetex': True,
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'legend.fontsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'figure.figsize': (8, 6),  # Suitable for journal publication
    'figure.autolayout': True
})

# --- 3. Create 3D Plot ---#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the cylindrical spiral
trajectory = ax.plot(x, y, z, 
                     linewidth=2.0, 
                     color='blue', 
                     alpha=0.8, 
                     label=r'$\vec{R}(t) = r\cos(\omega t)\hat{i} + r\sin(\omega t)\hat{j} + pt\hat{k}$')

# Add starting point marker
ax.scatter(x[0], y[0], z[0], 
           s=50, 
           color='red', 
           marker='o', 
           label='Starting Point')

# Add direction arrow at midpoint
mid_idx = len(t) // 2
ax.quiver(x[mid_idx], y[mid_idx], z[mid_idx],
          x[mid_idx+1] - x[mid_idx-1],
          y[mid_idx+1] - y[mid_idx-1],
          z[mid_idx+1] - z[mid_idx-1],
          length=0.5,
          normalize=True,
          color='green',
          label='Motion Direction')

# --- 4. Axes and Labels ---#
ax.set_xlabel(r'$x \, [\mathrm{m}]$', fontsize=11, labelpad=10)
ax.set_ylabel(r'$y \, [\mathrm{m}]$', fontsize=11, labelpad=10)
ax.set_zlabel(r'$z \, [\mathrm{m}]$', fontsize=11, labelpad=10)

# Set axis limits for better visualization
max_range = np.max([np.max(x)-np.min(x), np.max(y)-np.min(y), np.max(z)-np.min(z)]) / 2
target_center = np.mean(x), np.mean(y), np.mean(z)
ax.set_xlim(target_center[0] - max_range, target_center[0] + max_range)
ax.set_ylim(target_center[1] - max_range, target_center[1] + max_range)
ax.set_zlim(target_center[2] - max_range, target_center[2] + max_range)

# --- 5. Title and Legend ---#
ax.set_title(r'3D Cylindrical Spiral Spacetime Motion', fontsize=12, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0), frameon=True, fancybox=True, shadow=False)

# --- 6. Add Equation Annotation ---#
equation_text = r'$\vec{R}(t) = r\cos(\omega t)\hat{i} + r\sin(\omega t)\hat{j} + pt\hat{k}$'
ax.text2D(0.05, 0.95, equation_text, transform=ax.transAxes, 
          fontsize=12, verticalalignment='top', 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8))

# Add parameter values annotation
params_text = f'r = {r} m, $\omega$ = {omega} rad/s, p = {p} m/s'
ax.text2D(0.05, 0.88, params_text, transform=ax.transAxes, 
          fontsize=10, verticalalignment='top', 
          bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.8))

# --- 7. Add Grid and Minor Ticks ---#
ax.grid(True, linestyle='--', alpha=0.5)
ax.xaxis._axinfo['tick']['outward_factor'] = 0
ax.xaxis._axinfo['tick']['inward_factor'] = 0.4
ax.yaxis._axinfo['tick']['outward_factor'] = 0
ax.yaxis._axinfo['tick']['inward_factor'] = 0.4
ax.zaxis._axinfo['tick']['outward_factor'] = 0
ax.zaxis._axinfo['tick']['inward_factor'] = 0.4

# --- 8. Add Projection Lines ---#
# Add projection of helix onto xy-plane
ax.plot(x, y, np.full_like(x, ax.get_zlim3d()[0]), 
         linestyle=':', color='gray', alpha=0.5, label='Projection onto xy-plane')

# --- 9. Technical Output ---#
# Save in multiple formats for different use cases
plt.savefig('img/3d_cylindrical_spiral.pdf', format='pdf', bbox_inches='tight', dpi=600)
plt.savefig('img/3d_cylindrical_spiral.svg', format='svg', bbox_inches='tight')
plt.savefig('img/3d_cylindrical_spiral.png', format='png', bbox_inches='tight', dpi=600)

print("Figure generated successfully!")
print("Files saved in img/ directory:")
print("  - 3d_cylindrical_spiral.pdf (vector format for publication)")
print("  - 3d_cylindrical_spiral.svg (vector format for web)")
print("  - 3d_cylindrical_spiral.png (high-res raster for preview)")

# Show the plot (optional, comment out if running in non-interactive environment)
# plt.show()