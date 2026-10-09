import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# --- Physics & Mathematical Accuracy ---
# Physical Parameters
c = 299792458  # m/s (speed of light)
r = 1.0        # Spiral radius (arbitrary units for visualization)
omega = 1.0    # Angular velocity (arbitrary units for visualization)
h = np.sqrt(c**2 - (r * omega)**2)  # Axial velocity to satisfy c^2 = h^2 + (rω)^2

# Time range for plotting
t = np.linspace(0, 2*np.pi, 1000)

# Calculate spiral coordinates (Eq 2.1)
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# --- Clarity & Interpretability / Aesthetics & Professionalism ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=False)  # Use matplotlib's built-in math rendering instead of full LaTeX

# Create 3D plot
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')

# Plot spiral motion
ax.plot(x, y, z, linewidth=2.0, color='cornflowerblue', label=r'Spiral Path: $\vec{r}(t) = r\cos\omega t\vec{i} + r\sin\omega t\vec{j} + ht\vec{k}$')

# Add velocity components
# Radial component (circular in xy-plane)
ax.plot(x, y, np.zeros_like(x), linestyle='--', linewidth=1.5, color='gray', alpha=0.7, label='Radial Component')
# Axial component (z-direction)
ax.plot(np.zeros_like(z), np.zeros_like(z), z, linestyle='-.', linewidth=1.5, color='darkorange', alpha=0.7, label='Axial Component')

# Add arrows to show direction
# Arrow parameters
arrow_scale = 0.1
arrow_pos = int(len(t)/2)  # Middle of the spiral

# Velocity vector components
v_x = -r * omega * np.sin(omega * t[arrow_pos])
v_y = r * omega * np.cos(omega * t[arrow_pos])
v_z = h

# Normalize velocity vector for display
v_mag = np.sqrt(v_x**2 + v_y**2 + v_z**2)
v_unit = [v_x/v_mag, v_y/v_mag, v_z/v_mag]

# Plot velocity arrow at the middle point
ax.quiver(x[arrow_pos], y[arrow_pos], z[arrow_pos], 
          v_unit[0], v_unit[1], v_unit[2], 
          length=arrow_scale, color='red', linewidth=2, label='Velocity Vector')

# --- Annotations & Emphasis ---
# Add equation in a text box
equation_text = r'$\vec{r}(t) = r\cos\omega t\vec{i} + r\sin\omega t\vec{j} + ht\vec{k}$\nwith $h^2 + (r\omega)^2 = c^2$'
ax.text2D(0.02, 0.98, equation_text, transform=ax.transAxes, fontsize=10, 
         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Axes & Labels ---
ax.set_xlabel(r'$x$', fontsize=11)
ax.set_ylabel(r'$y$', fontsize=11)
ax.set_zlabel(r'$z$', fontsize=11)
ax.set_title('Space Spiral Motion at Light Speed', fontsize=12)
ax.legend(loc='upper right', fontsize=9)

# Set limits and ticks
max_range = max(np.max(x), np.max(y), np.max(z))
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(0, np.max(z))
ax.tick_params(axis='both', which='major', labelsize=10)

# --- Technical Output ---
plt.tight_layout()
plt.savefig('img/space_spiral_motion.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('img/space_spiral_motion.svg', format='svg', bbox_inches='tight')

print("Figure generated: img/space_spiral_motion.png, img/space_spiral_motion.svg")