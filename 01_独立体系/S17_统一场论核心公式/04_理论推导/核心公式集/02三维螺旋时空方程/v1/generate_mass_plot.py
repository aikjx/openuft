#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate publication-ready plots for the geometric definition of mass
from Zhang Xiangqian's Unified Field Theory.

Equations:
1. Mass geometric definition (integral form): m = k * n / Ω
2. Simplified form when Ω=4π: n = m / m_p (since k=4π m_p)
3. Quantum proportion constant: k = 4π m_p

Objective: To accurately visualize the relationship between mass, spatial displacement lines,
and the quantum proportion constant, adhering to the highest standards of scientific journals.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Create img directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# --- 1. Physics & Mathematical Accuracy ---#
# Physical Parameters (SI units)
m_p = 2.176434e-8  # Planck mass (kg)
k = 4 * np.pi * m_p  # Quantum proportion constant
Omega = 4 * np.pi     # Solid angle (full sphere)

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
    'figure.figsize': (12, 6),
    'figure.autolayout': True
})

# --- 3. Create Subplots ---#
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- 4. Plot 1: Number of Lines vs Mass (n = m / m_p) ---#
m_values = np.linspace(1e-30, 1e-7, 100)  # Mass from 1e-30 kg to 1e-7 kg
n_values = m_values / m_p  # Calculate number of lines

ax1.plot(m_values, n_values, linewidth=2.0, color='blue')
ax1.set_title(r'Number of Spatial Displacement Lines vs. Mass', fontsize=12)
ax1.set_xlabel(r'$m \, [\mathrm{kg}]$', fontsize=11)
ax1.set_ylabel(r'$n \, [\mathrm{dimensionless}]$', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlim(1e-30, 1e-7)
ax1.set_ylim(1e-22, 1e1)

# Add annotations for common masses
# Electron mass: ~9.11e-31 kg
electron_mass = 9.11e-31
ax1.plot(electron_mass, electron_mass / m_p, 'ro', markersize=8, label=r'Electron Mass')
ax1.text(electron_mass * 1.5, electron_mass / m_p, r'$m_e$', fontsize=10, color='red')

# Proton mass: ~1.67e-27 kg
proton_mass = 1.67e-27
ax1.plot(proton_mass, proton_mass / m_p, 'go', markersize=8, label=r'Proton Mass')
ax1.text(proton_mass * 1.5, proton_mass / m_p, r'$m_p$', fontsize=10, color='green')

# Planck mass: ~2.18e-8 kg
ax1.plot(m_p, m_p / m_p, 'bo', markersize=8, label=r'Planck Mass')
ax1.text(m_p * 1.5, m_p / m_p, r'$m_{Planck}$', fontsize=10, color='blue')

ax1.legend(loc='upper left', frameon=True, fontsize=9)

# --- 5. Plot 2: Mass vs Solid Angle (for constant n and k) ---#
Omega_values = np.linspace(0.1, 10*np.pi, 100)  # Solid angle from 0.1 to 10π
n_constant = 100  # Constant number of lines for visualization
m_omega = k * n_constant / Omega_values  # Calculate mass

ax2.plot(Omega_values, m_omega, linewidth=2.0, color='red')
ax2.set_title(r'Mass vs. Solid Angle (Constant n=100)', fontsize=12)
ax2.set_xlabel(r'$\Omega \, [\mathrm{rad}]$', fontsize=11)
ax2.set_ylabel(r'$m \, [\mathrm{kg}]$', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlim(0, 10*np.pi)
ax2.set_ylim(0, 5e-6)

# Add vertical line for full sphere (Omega=4π)
ax2.axvline(x=4*np.pi, color='green', linestyle='--', linewidth=1.5, 
            label=r'$\Omega = 4\pi$ (Full Sphere)')
ax2.legend(loc='upper right', frameon=True, fontsize=9)

# --- 6. Add Main Title ---#
fig.suptitle(r'Geometric Definition of Mass in Cylindrical Spiral Motion', 
             fontsize=14, y=0.98)

# --- 7. Save Plot ---#
plt.tight_layout()
plt.savefig('img/mass_geometric_definition.svg', format='svg', bbox_inches='tight')
plt.savefig('img/mass_geometric_definition.pdf', format='pdf', bbox_inches='tight')
plt.savefig('img/mass_geometric_definition.png', format='png', bbox_inches='tight', dpi=600)

print("Mass geometric definition plot generated successfully!")
print("Files saved in img/ directory:")
print("  - mass_geometric_definition.svg (vector format for publication)")
print("  - mass_geometric_definition.pdf (vector format for backup)")
print("  - mass_geometric_definition.png (high-res raster for preview)")

# Show the plot (optional, comment out if running in non-interactive environment)
# plt.show()