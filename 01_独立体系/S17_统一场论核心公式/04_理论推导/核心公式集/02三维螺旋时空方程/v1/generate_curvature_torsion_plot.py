#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate publication-ready plots for curvature and torsion in cylindrical spiral motion
from Zhang Xiangqian's Unified Field Theory.

Equations:
1. Curvature radius: ρ = (r²ω² + p²) / (rω²)
2. Torsion: τ = (pω) / (p² + r²ω²)

Objective: To accurately visualize how curvature and torsion depend on the parameters
r, ω, and p, adhering to the highest standards of scientific journals.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Create img directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# --- 1. Physics & Mathematical Accuracy ---#
# Base Physical Parameters (SI units)
r_base = 1.0        # Helix radius (m)
omega_base = 1.0    # Angular velocity (rad/s)
p_base = 1.0        # Axial velocity (m/s)

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
    'figure.figsize': (10, 8),
    'figure.autolayout': True
})

# --- 3. Create Subplots ---#
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# --- 4. Plot 1: Curvature vs p (varying axial velocity) ---#
p_values = np.linspace(0.1, 5.0, 100)  # Vary p from 0.1 to 5.0
# Curvature calculation
rho = (r_base**2 * omega_base**2 + p_values**2) / (r_base * omega_base**2)
ax1.plot(p_values, rho, linewidth=2.0, color='blue')
ax1.set_title(r'Curvature Radius vs. Axial Velocity', fontsize=12)
ax1.set_xlabel(r'$p \, [\mathrm{m/s}]$', fontsize=11)
ax1.set_ylabel(r'$\rho \, [\mathrm{m}]$', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlim(0, 5.0)
ax1.set_ylim(0, 26)

# --- 5. Plot 2: Torsion vs p (varying axial velocity) ---#
tau = (p_values * omega_base) / (p_values**2 + r_base**2 * omega_base**2)
ax2.plot(p_values, tau, linewidth=2.0, color='red')
ax2.set_title(r'Torsion vs. Axial Velocity', fontsize=12)
ax2.set_xlabel(r'$p \, [\mathrm{m/s}]$', fontsize=11)
ax2.set_ylabel(r'$\tau \, [\mathrm{m^{-1}}]$', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlim(0, 5.0)
ax2.set_ylim(0, 0.5)

# --- 6. Plot 3: Curvature vs r (varying radius) ---#
r_values = np.linspace(0.1, 5.0, 100)  # Vary r from 0.1 to 5.0
rho = (r_values**2 * omega_base**2 + p_base**2) / (r_values * omega_base**2)
ax3.plot(r_values, rho, linewidth=2.0, color='green')
ax3.set_title(r'Curvature Radius vs. Helix Radius', fontsize=12)
ax3.set_xlabel(r'$r \, [\mathrm{m}]$', fontsize=11)
ax3.set_ylabel(r'$\rho \, [\mathrm{m}]$', fontsize=11)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.set_xlim(0, 5.0)
ax3.set_ylim(0, 6)

# --- 7. Plot 4: Torsion vs r (varying radius) ---#
tau = (p_base * omega_base) / (p_base**2 + r_values**2 * omega_base**2)
ax4.plot(r_values, tau, linewidth=2.0, color='purple')
ax4.set_title(r'Torsion vs. Helix Radius', fontsize=12)
ax4.set_xlabel(r'$r \, [\mathrm{m}]$', fontsize=11)
ax4.set_ylabel(r'$\tau \, [\mathrm{m^{-1}}]$', fontsize=11)
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.set_xlim(0, 5.0)
ax4.set_ylim(0, 0.5)

# Add main title
fig.suptitle(r'Curvature and Torsion in Cylindrical Spiral Motion', 
             fontsize=14, y=0.98)

# --- 8. Save Plot ---#
plt.tight_layout()
plt.savefig('img/curvature_torsion.svg', format='svg', bbox_inches='tight')
plt.savefig('img/curvature_torsion.pdf', format='pdf', bbox_inches='tight')
plt.savefig('img/curvature_torsion.png', format='png', bbox_inches='tight', dpi=600)

print("Curvature and torsion plot generated successfully!")
print("Files saved in img/ directory:")
print("  - curvature_torsion.svg (vector format for publication)")
print("  - curvature_torsion.pdf (vector format for backup)")
print("  - curvature_torsion.png (high-res raster for preview)")

# Show the plot (optional, comment out if running in non-interactive environment)
# plt.show()