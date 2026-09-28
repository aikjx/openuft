#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate publication-ready plots for velocity, acceleration, and jerk vectors
from Zhang Xiangqian's Unified Field Theory.

Equations:
1. Velocity vector: V(t) = -rω sin(ωt)i + rω cos(ωt)j + pk
2. Acceleration vector: a(t) = -rω² cos(ωt)i - rω² sin(ωt)j + 0k
3. Jerk vector: j(t) = rω³ sin(ωt)i - rω³ cos(ωt)j + 0k

Objective: To accurately visualize the components and magnitudes of these vectors
as functions of time, adhering to the highest standards of scientific journals.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Create img directory if it doesn't exist
os.makedirs('img', exist_ok=True)

# --- 1. Physics & Mathematical Accuracy ---#
# Physical Parameters (SI units)
r = 1.0        # Helix radius (m)
omega = 1.0    # Angular velocity (rad/s)
p = 1.0        # Axial velocity (m/s)
t = np.linspace(0, 2*np.pi, 1000)  # Time range (one full rotation)

# Calculate vectors
# Velocity components
Vx = -r * omega * np.sin(omega * t)
Vy = r * omega * np.cos(omega * t)
Vz = p * np.ones_like(t)
V_mag = np.sqrt(Vx**2 + Vy**2 + Vz**2)

# Acceleration components
ax = -r * omega**2 * np.cos(omega * t)
ay = -r * omega**2 * np.sin(omega * t)
az = np.zeros_like(t)
a_mag = np.sqrt(ax**2 + ay**2 + az**2)

# Jerk components
jx = r * omega**3 * np.sin(omega * t)
jy = -r * omega**3 * np.cos(omega * t)
jz = np.zeros_like(t)
j_mag = np.sqrt(jx**2 + jy**2 + jz**2)

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

# --- 3. Create Plot ---#
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Velocity components
ax1.plot(t, Vx, label=r'$V_x(t) = -r\omega \sin(\omega t)$', linewidth=1.5, color='red')
ax1.plot(t, Vy, label=r'$V_y(t) = r\omega \cos(\omega t)$', linewidth=1.5, color='green')
ax1.plot(t, Vz, label=r'$V_z(t) = p$', linewidth=1.5, color='blue')
ax1.set_title(r'Velocity Vector Components vs. Time', fontsize=12)
ax1.set_xlabel(r'$t \, [\mathrm{s}]$', fontsize=11)
ax1.set_ylabel(r'$V \, [\mathrm{m/s}]$', fontsize=11)
ax1.legend(loc='upper right', frameon=True, fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_ylim(-1.5, 1.5)

# Plot 2: Acceleration components
ax2.plot(t, ax, label=r'$a_x(t) = -r\omega^2 \cos(\omega t)$', linewidth=1.5, color='red')
ax2.plot(t, ay, label=r'$a_y(t) = -r\omega^2 \sin(\omega t)$', linewidth=1.5, color='green')
ax2.plot(t, az, label=r'$a_z(t) = 0$', linewidth=1.5, color='blue')
ax2.set_title(r'Acceleration Vector Components vs. Time', fontsize=12)
ax2.set_xlabel(r'$t \, [\mathrm{s}]$', fontsize=11)
ax2.set_ylabel(r'$a \, [\mathrm{m/s^2}]$', fontsize=11)
ax2.legend(loc='upper right', frameon=True, fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_ylim(-1.5, 1.5)

# Plot 3: Jerk components
ax3.plot(t, jx, label=r'$j_x(t) = r\omega^3 \sin(\omega t)$', linewidth=1.5, color='red')
ax3.plot(t, jy, label=r'$j_y(t) = -r\omega^3 \cos(\omega t)$', linewidth=1.5, color='green')
ax3.plot(t, jz, label=r'$j_z(t) = 0$', linewidth=1.5, color='blue')
ax3.set_title(r'Jerk Vector Components vs. Time', fontsize=12)
ax3.set_xlabel(r'$t \, [\mathrm{s}]$', fontsize=11)
ax3.set_ylabel(r'$j \, [\mathrm{m/s^3}]$', fontsize=11)
ax3.legend(loc='upper right', frameon=True, fontsize=9)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.set_ylim(-1.5, 1.5)

# Plot 4: Vector magnitudes
ax4.plot(t, V_mag, label=r'$|\vec{V}|$', linewidth=1.5, color='red')
ax4.plot(t, a_mag, label=r'$|\vec{a}|$', linewidth=1.5, color='green')
ax4.plot(t, j_mag, label=r'$|\vec{j}|$', linewidth=1.5, color='blue')
ax4.set_title(r'Vector Magnitudes vs. Time', fontsize=12)
ax4.set_xlabel(r'$t \, [\mathrm{s}]$', fontsize=11)
ax4.set_ylabel(r'$|\vec{F}| \, [\mathrm{units}]$', fontsize=11)
ax4.legend(loc='upper right', frameon=True, fontsize=9)
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.set_ylim(0, 2.5)

# Add main title
fig.suptitle(r'Velocity, Acceleration, and Jerk Vectors in Cylindrical Spiral Motion', 
             fontsize=14, y=0.98)

# --- 4. Save Plot ---#
plt.tight_layout()
plt.savefig('img/vectors_components.svg', format='svg', bbox_inches='tight')
plt.savefig('img/vectors_components.pdf', format='pdf', bbox_inches='tight')
plt.savefig('img/vectors_components.png', format='png', bbox_inches='tight', dpi=600)

print("Vector components plot generated successfully!")
print("Files saved in img/ directory:")
print("  - vectors_components.svg (vector format for publication)")
print("  - vectors_components.pdf (vector format for backup)")
print("  - vectors_components.png (high-res raster for preview)")

# Show the plot (optional, comment out if running in non-interactive environment)
# plt.show()