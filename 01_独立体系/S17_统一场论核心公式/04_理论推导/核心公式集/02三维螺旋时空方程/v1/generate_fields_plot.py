#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate publication-ready plots for the geometric origin of electromagnetic and gravitational fields
from Zhang Xiangqian's Unified Field Theory.

Equations:
1. Electric Field: E ∝ p k̂ (axial component)
2. Magnetic Field: B ∝ rω [cos(ωt) î + sin(ωt) ĵ] (rotational component)
3. Gravitational Field: g ∝ -rω² [cos(ωt) î + sin(ωt) ĵ] (centripetal component)

Objective: To accurately visualize these fields and their relation to the cylindrical spiral motion,
adhering to the highest standards of scientific journals.
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
t = np.linspace(0, 2*np.pi, 1000)  # Time range (one full rotation)

# Calculate field components
# Normalize for visualization purposes
scale_factor = 0.5

# Magnetic field components
Bx = scale_factor * r * omega * np.cos(omega * t)
By = scale_factor * r * omega * np.sin(omega * t)
Bz = np.zeros_like(t)
B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)

# Gravitational field components
gx = -scale_factor * r * omega**2 * np.cos(omega * t)
gy = -scale_factor * r * omega**2 * np.sin(omega * t)
gz = np.zeros_like(t)
g_mag = np.sqrt(gx**2 + gy**2 + gz**2)

# Electric field components (constant in z-direction)
Ex = np.zeros_like(t)
Ey = np.zeros_like(t)
Ez = scale_factor * p * np.ones_like(t)
E_mag = np.sqrt(Ex**2 + Ey**2 + Ez**2)

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
    'figure.figsize': (12, 10),
    'figure.autolayout': True
})

# --- 3. Create Plot ---#
fig = plt.figure(figsize=(14, 12))

# --- 4. Plot 1: Magnetic and Gravitational Fields in XY Plane (2D) ---#
ax1 = fig.add_subplot(2, 2, 1)

# Plot magnetic field components
ax1.plot(t, Bx, label='Bx(t)', 
         linewidth=2.0, color='red', linestyle='-')
ax1.plot(t, By, label='By(t)', 
         linewidth=2.0, color='red', linestyle='--')
ax1.plot(t, B_mag, label='|B| (constant)', 
         linewidth=1.5, color='red', linestyle=':')

# Plot gravitational field components
ax1.plot(t, gx, label='gx(t)', 
         linewidth=2.0, color='blue', linestyle='-')
ax1.plot(t, gy, label='gy(t)', 
         linewidth=2.0, color='blue', linestyle='--')
ax1.plot(t, g_mag, label='|g| (constant)', 
         linewidth=1.5, color='blue', linestyle=':')

ax1.set_title('Magnetic and Gravitational Field Components', fontsize=12)
ax1.set_xlabel('t [s]', fontsize=11)
ax1.set_ylabel('Field Strength [arb. units]', fontsize=11)
ax1.legend(loc='upper right', frameon=True, fontsize=8)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlim(0, 2*np.pi)
ax1.set_ylim(-2.5, 2.5)

# --- 5. Plot 2: Electric Field (Constant in Z-direction) ---#
ax2 = fig.add_subplot(2, 2, 2)

# Plot electric field components
ax2.plot(t, Ex, label='Ex(t) = 0', 
         linewidth=2.0, color='green', linestyle='-')
ax2.plot(t, Ey, label='Ey(t) = 0', 
         linewidth=2.0, color='green', linestyle='--')
ax2.plot(t, Ez, label='Ez(t) (constant)', 
         linewidth=2.0, color='green', linestyle='-')
ax2.plot(t, E_mag, label='|E| (constant)', 
         linewidth=1.5, color='green', linestyle=':')

ax2.set_title('Electric Field Components', fontsize=12)
ax2.set_xlabel('t [s]', fontsize=11)
ax2.set_ylabel('Field Strength [arb. units]', fontsize=11)
ax2.legend(loc='upper right', frameon=True, fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlim(0, 2*np.pi)
ax2.set_ylim(-0.5, 1.5)

# --- 6. Plot 3: Field Magnitudes Comparison ---#
ax3 = fig.add_subplot(2, 2, 3)

ax3.plot(t, B_mag, label='|B|', 
         linewidth=2.0, color='red', linestyle='-')
ax3.plot(t, g_mag, label='|g|', 
         linewidth=2.0, color='blue', linestyle='-')
ax3.plot(t, E_mag, label='|E|', 
         linewidth=2.0, color='green', linestyle='-')

ax3.set_title('Field Magnitudes Comparison', fontsize=12)
ax3.set_xlabel('t [s]', fontsize=11)
ax3.set_ylabel('|F| [arb. units]', fontsize=11)
ax3.legend(loc='upper right', frameon=True, fontsize=10)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.set_xlim(0, 2*np.pi)
ax3.set_ylim(0, 1.5)

# --- 7. Plot 4: 3D Field Visualization ---#
ax4 = fig.add_subplot(2, 2, 4, projection='3d')

# Create spatial grid for vector field visualization
x_grid, y_grid = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
z_grid = np.zeros_like(x_grid)

# Calculate field vectors at a specific time (t = pi/2)
t_sample = np.pi / 2
Bx_sample = scale_factor * r * omega * np.cos(omega * t_sample)
By_sample = scale_factor * r * omega * np.sin(omega * t_sample)

gx_sample = -scale_factor * r * omega**2 * np.cos(omega * t_sample)
gy_sample = -scale_factor * r * omega**2 * np.sin(omega * t_sample)

Ez_sample = scale_factor * p

# Plot vector field at t = pi/2
# Magnetic field vectors (red, in XY plane)
ax4.quiver(x_grid, y_grid, z_grid, 
           Bx_sample * np.ones_like(x_grid), 
           By_sample * np.ones_like(y_grid), 
           np.zeros_like(z_grid), 
           color='red', length=0.5, normalize=True, label='B (t=pi/2)')

# Gravitational field vectors (blue, in XY plane, opposite to B)
ax4.quiver(x_grid, y_grid, z_grid, 
           gx_sample * np.ones_like(x_grid), 
           gy_sample * np.ones_like(y_grid), 
           np.zeros_like(z_grid), 
           color='blue', length=0.5, normalize=True, label='g (t=pi/2)')

# Electric field vectors (green, along Z-axis)
ax4.quiver(x_grid, y_grid, z_grid, 
           np.zeros_like(x_grid), 
           np.zeros_like(y_grid), 
           Ez_sample * np.ones_like(z_grid), 
           color='green', length=0.5, normalize=True, label='E (constant)')

ax4.set_title('3D Field Vectors Visualization', fontsize=12)
ax4.set_xlabel('x [m]', fontsize=11)
ax4.set_ylabel('y [m]', fontsize=11)
ax4.set_zlabel('z [m]', fontsize=11)
ax4.legend(loc='upper right', frameon=True, fontsize=8)
ax4.set_xlim(-2, 2)
ax4.set_ylim(-2, 2)
ax4.set_zlim(-2, 2)

# --- 8. Add Main Title ---#
fig.suptitle('Geometric Origin of Electromagnetic and Gravitational Fields', 
             fontsize=14, y=0.98)

# --- 9. Save Plot ---#
plt.tight_layout()
plt.savefig('img/fields_geometric_origin.svg', format='svg', bbox_inches='tight')
plt.savefig('img/fields_geometric_origin.pdf', format='pdf', bbox_inches='tight')
plt.savefig('img/fields_geometric_origin.png', format='png', bbox_inches='tight', dpi=600)

print("Fields geometric origin plot generated successfully!")
print("Files saved in img/ directory:")
print("  - fields_geometric_origin.svg (vector format for publication)")
print("  - fields_geometric_origin.pdf (vector format for backup)")
print("  - fields_geometric_origin.png (high-res raster for preview)")

# Show the plot (optional, comment out if running in non-interactive environment)
# plt.show()