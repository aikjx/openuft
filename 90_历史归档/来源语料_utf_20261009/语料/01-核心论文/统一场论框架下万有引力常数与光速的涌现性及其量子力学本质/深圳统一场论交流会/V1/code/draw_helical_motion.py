"""
Generate a publication-ready, vector-based physics visualization for the cylindrical helical motion equation:
$vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$

This script creates a 3D plot of the helical motion, showing the spatial trajectory of a point moving with both rotational and translational components.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
import os

# --- Set up directories ---
img_dir = "img"
os.makedirs(img_dir, exist_ok=True)

# --- Physics & Mathematical Accuracy ---
# Physical parameters
r = 1.0          # Helical radius (m)
omega = 2*np.pi  # Angular velocity (rad/s)
h = 0.5          # Axial velocity (m/s)
c = np.sqrt((r*omega)**2 + h**2)  # Speed of light constraint (m/s)

# Time range for plotting
t = np.linspace(0, 5, 1000)  # 5 seconds

# Calculate coordinates
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# --- Plotting settings for publication quality ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=True)  # Enable LaTeX rendering
rc('axes', labelsize=12)  # Axis label font size
rc('xtick', labelsize=10)  # X tick label font size
rc('ytick', labelsize=10)  # Y tick label font size
rc('legend', fontsize=10)  # Legend font size
rc('figure', titlesize=14)  # Figure title font size

# --- Create 3D plot ---
fig = plt.figure(figsize=(8, 6))  # Double column width for better visibility
ax = fig.add_subplot(111, projection='3d')

# Plot helical trajectory
ax.plot(x, y, z, linewidth=2.0, color='cornflowerblue', label=r'Helical Trajectory')

# Plot the axis of rotation (z-axis)
ax.plot([0, 0], [0, 0], [0, max(z)], linewidth=1.5, color='red', linestyle='--', label=r'Axis of Rotation')

# Add a few key points to highlight the motion
key_times = [0, np.pi/(2*omega), np.pi/omega, 3*np.pi/(2*omega), 2*np.pi/omega]
for i, t_key in enumerate(key_times):
    x_key = r * np.cos(omega * t_key)
    y_key = r * np.sin(omega * t_key)
    z_key = h * t_key
    ax.scatter(x_key, y_key, z_key, s=50, color='darkorange', alpha=0.8)
    ax.text(x_key, y_key, z_key + 0.1, f'$t={t_key:.2f}s$', fontsize=9)

# --- Add annotations and labels ---
ax.set_xlabel(r'$x$ (m)', fontsize=12, labelpad=10)
ax.set_ylabel(r'$y$ (m)', fontsize=12, labelpad=10)
ax.set_zlabel(r'$z$ (m)', fontsize=12, labelpad=10)

ax.set_title(r'Cylindrical Helical Motion of Space Points', fontsize=14)

# --- Set viewing angle for best visibility ---
ax.view_init(elev=30, azim=45)

# --- Add equation in a text box ---
eq_text = r'$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$'
ax.text2D(0.02, 0.98, eq_text, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Add speed constraint ---
speed_text = rf'$c = \sqrt{{(r\omega)^2 + h^2}} = {c:.2f} \, \mathrm{{m/s}}$'
ax.text2D(0.02, 0.92, speed_text, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))

# --- Legend ---
ax.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95), frameon=True)

# --- Add grid and adjust layout ---
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# --- Save in multiple formats for different uses ---
plt.savefig(os.path.join(img_dir, 'helical_motion_3d.pdf'), format='pdf', bbox_inches='tight', dpi=600)
plt.savefig(os.path.join(img_dir, 'helical_motion_3d.svg'), format='svg', bbox_inches='tight')
plt.savefig(os.path.join(img_dir, 'helical_motion_3d.png'), format='png', bbox_inches='tight', dpi=600)

print(f"Helical motion plot generated and saved to {img_dir}")
plt.close()