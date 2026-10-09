"""
Generate a publication-ready, vector-based physics visualization for the mass geometric definition equation:
$m = k \frac{n}{\Omega}$

This script creates a 2D plot showing the relationship between mass, spatial displacement lines, and solid angle.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# --- Set up directories ---
img_dir = "img"
os.makedirs(img_dir, exist_ok=True)

# --- Physics & Mathematical Accuracy ---
# Physical parameters
k = 4 * np.pi * 2.176434e-8  # Quantum proportionality constant in kg (k = 4π m_p, m_p is Planck mass)

# --- Plotting settings for publication quality ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=True)  # Enable LaTeX rendering
rc('axes', labelsize=12)  # Axis label font size
rc('xtick', labelsize=10)  # X tick label font size
rc('ytick', labelsize=10)  # Y tick label font size
rc('legend', fontsize=10)  # Legend font size
rc('figure', titlesize=14)  # Figure title font size

# --- Create plot for mass vs. spatial displacement lines (n) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Two subplots side by side

# Plot 1: Mass vs. Spatial Displacement Lines (fixed solid angle Ω = 4π)
Omega_fixed = 4 * np.pi  # Solid angle in steradians (full sphere)
n_values = np.linspace(1, 100, 100)  # Number of spatial displacement lines
m_values = k * n_values / Omega_fixed  # Mass values in kg

ax1.plot(n_values, m_values, linewidth=2.0, color='cornflowerblue', label=r'Mass')
ax1.set_xlabel(r'Number of Spatial Displacement Lines ($n$)', fontsize=12)
ax1.set_ylabel(r'Mass ($m$) [kg]', fontsize=12)
ax1.set_title(r'Mass vs. Spatial Displacement Lines ($\Omega = 4\pi$)', fontsize=13)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper left')

# Add equation in a text box
equation1 = r'$m = k \frac{n}{\Omega}$'
ax1.text(0.05, 0.95, equation1, transform=ax1.transAxes, fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# Plot 2: Mass vs. Solid Angle (fixed number of lines n = 10)
n_fixed = 10  # Fixed number of spatial displacement lines
Omega_values = np.linspace(0.1, 16*np.pi, 100)  # Solid angle from 0.1 to 4 times full sphere
m_values2 = k * n_fixed / Omega_values  # Mass values in kg

ax2.plot(Omega_values / np.pi, m_values2, linewidth=2.0, color='darkorange', label=r'Mass')
ax2.set_xlabel(r'Solid Angle ($\Omega / \pi$) [sr]', fontsize=12)
ax2.set_ylabel(r'Mass ($m$) [kg]', fontsize=12)
ax2.set_title(r'Mass vs. Solid Angle ($n = 10$)', fontsize=13)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='upper right')

# --- Add annotations and details ---
# Add a horizontal line for Planck mass in Plot 1
m_p = 2.176434e-8  # Planck mass in kg
ax1.axhline(m_p, color='red', linestyle='--', linewidth=1.5, label=r'Planck Mass')
ax1.legend(loc='upper left')

# Add some key points to Plot 1
key_n = [1, 10, 50, 100]
for n_key in key_n:
    m_key = k * n_key / Omega_fixed
    ax1.scatter(n_key, m_key, s=50, color='darkorange', alpha=0.8)
    ax1.text(n_key + 1, m_key, f'$n={n_key}$', fontsize=9)

# Add some key points to Plot 2
key_Omega_pi = [1, 2, 4, 8]
for Omega_pi_key in key_Omega_pi:
    Omega_key = Omega_pi_key * np.pi
    m_key = k * n_fixed / Omega_key
    ax2.scatter(Omega_pi_key, m_key, s=50, color='cornflowerblue', alpha=0.8)
    ax2.text(Omega_pi_key + 0.1, m_key, f'$\Omega/{np.pi}={Omega_pi_key}$', fontsize=9)

# --- Adjust layout and save ---
plt.tight_layout()

# --- Save in multiple formats for different uses ---
plt.savefig(os.path.join(img_dir, 'mass_definition_geometry.pdf'), format='pdf', bbox_inches='tight', dpi=600)
plt.savefig(os.path.join(img_dir, 'mass_definition_geometry.svg'), format='svg', bbox_inches='tight')
plt.savefig(os.path.join(img_dir, 'mass_definition_geometry.png'), format='png', bbox_inches='tight', dpi=600)

print(f"Mass definition plot generated and saved to {img_dir}")
plt.close()

# --- Create a schematic diagram for spatial displacement lines ---
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Create a central point representing the object
ax.scatter(0, 0, 0, s=200, color='red', label=r'Object (Mass $m$)')

# Generate spatial displacement lines in a helical pattern
n_lines = 12  # Number of lines to visualize
radius = 1.0  # Base radius
height = 1.5  # Height of the visualization

for i in range(n_lines):
    # Calculate angle for each line
    theta = 2 * np.pi * i / n_lines
    
    # Create points for the line
    z = np.linspace(0, height, 100)
    r = radius + 0.2 * np.sin(5 * z)  # Slight variation in radius for helical effect
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Plot the line
    ax.plot(x, y, z, linewidth=1.5, color='cornflowerblue', alpha=0.7)
    
    # Add an arrow at the end of each line
    ax.quiver(x[-2], y[-2], z[-2], x[-1]-x[-2], y[-1]-y[-2], z[-1]-z[-2], length=0.2, color='darkorange', arrow_length_ratio=0.5)

# --- Set plot properties ---
ax.set_xlabel(r'$x$ (m)', fontsize=12)
ax.set_ylabel(r'$y$ (m)', fontsize=12)
ax.set_zlabel(r'$z$ (m)', fontsize=12)
ax.set_title(r'Schematic of Spatial Displacement Lines', fontsize=14)

# Set viewing angle for best visibility
ax.view_init(elev=20, azim=45)

# Add a text box with explanation
explanation = r'Spatial displacement lines emanate from the object and represent the geometric nature of mass.'
ax.text2D(0.02, 0.98, explanation, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Adjust layout and save ---
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'spatial_displacement_schematic.pdf'), format='pdf', bbox_inches='tight', dpi=600)
plt.savefig(os.path.join(img_dir, 'spatial_displacement_schematic.svg'), format='svg', bbox_inches='tight')
plt.savefig(os.path.join(img_dir, 'spatial_displacement_schematic.png'), format='png', bbox_inches='tight', dpi=600)

print(f"Spatial displacement schematic generated and saved to {img_dir}")
plt.close()
