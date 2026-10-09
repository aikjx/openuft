"""
Generate a publication-ready, vector-based physics visualization in Python for the equation/phenomenon:
'Gravitational-Light Speed Unification Equation and Core Theoretical Framework'

Objective: To accurately and clearly depict the core equations and theoretical framework of the Gravitational-Light Speed Unification Equation, adhering to the highest standards of scientific journals.

Key Specifications:
1.  **Physics & Mathematical Accuracy:**
    *   Equation Representation: $Z = \frac{G \cdot c}{2}$, $\vec{r}(t)=\vec{C}t$, $\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$, $m = k \cdot \frac{dn}{d\Omega}$
    *   Physical Parameters: Define and use physical constants with SI units. G=6.67430e-11 m³ kg⁻¹ s⁻², c=2.99792458e8 m/s, Z=0.010004524012147 kg⁻¹ m⁴ s⁻³.
    *   Data Range: Specify appropriate ranges for each visualization.

2.  **Clarity & Interpretability:**
    *   Axes Labels: Use LaTeX for quantity and SI units.
    *   Tick Labels: Legible font size (10-11pt), appropriate density.
    *   Legend: Concise, informative, positioned appropriately.
    *   Title: Descriptive and informative for each figure.

3.  **Aesthetics & Professionalism:**
    *   Plotting Style: Use a scientific style template. Preferred: 'seaborn-v0_8-paper'.
    *   Color Palette: Use a colorblind-friendly and publication-standard palette. Limit colors to 2-3 main ones.
    *   Line Styles & Markers: Differentiate curves using line styles and markers. Line width: 1.5-2.0 pt.
    *   Font: Use a serif font like 'Times New Roman' or 'Computer Modern' for titles, labels, and annotations (10-12pt for text).

4.  **Mathematical Representation:**
    *   All mathematical expressions in labels, titles, legends, and annotations must be rendered using LaTeX.

5.  **Technical Output:**
    *   Format: Primary output must be a vector format (PNG or SVG) for scalability and LaTeX embedding.
    *   Resolution: Export with 600 DPI (for PNG previews).
    *   Figure Size: Tailor to journal requirements (e.g., 3.5 inches for single column, 7 inches for double column).
    *   File Naming: Descriptive and consistent, saved to '../img/' directory.

6.  **Reproducibility:**
    *   Code Comments: Extensive comments explaining steps, formulas, and parameters.
    *   Parameterization: Define all key parameters at the beginning of the script.

7.  **Annotations & Emphasis:**
    *   Highlight key physical features and critical points.
    *   Provide brief explanations for critical variables or phenomena directly on the plot if space permits.

**Specific Plot Types:**
*   **Formula Visualization:** Create a clean, professional visualization of the core Gravitational-Light Speed Unification Equation $Z = \frac{G \cdot c}{2}$.
*   **3D Spiral Plot:** Create a 3D visualization of the spatial spiral motion equation.
*   **Conceptual Diagram:** Illustrate the mass geometrization concept and spatial dynamics.

**Preferred Libraries:**
*   Core: `matplotlib`, `numpy`
*   Enhancements: `seaborn` (for styles and palettes), `sympy` (for symbolic math and LaTeX rendering)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from matplotlib import rc

# Set LaTeX rendering and font settings
rc('font',**{'family':'serif','serif':['Times New Roman']})
rc('text', usetex=True)
plt.style.use('seaborn-v0_8-paper')

# Define physical constants
G = 6.67430e-11  # m³ kg⁻¹ s⁻² (gravitational constant)
c = 2.99792458e8  # m/s (speed of light)
Z = 0.010004524012147  # kg⁻¹ m⁴ s⁻³ (Zhang Xiangqian constant)

# Create img directory if it doesn't exist
import os
if not os.path.exists('../img'):
    os.makedirs('../img')

# 1. Gravitational-Light Speed Unification Equation Visualization
plt.figure(figsize=(5, 3))
ax = plt.gca()

# Set background to white for better LaTeX embedding
ax.set_facecolor('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

# Display the core equation
core_eq = r"$Z = \frac{G \cdot c}{2}$"
ax.text(0.5, 0.5, core_eq, fontsize=36, ha='center', va='center', transform=ax.transAxes)

# Add annotations for constants
ax.text(0.2, 0.3, r"$Z$: Zhang Xiangqian Constant", fontsize=12, ha='center', va='center', transform=ax.transAxes)
ax.text(0.5, 0.3, r"$G$: Gravitational Constant", fontsize=12, ha='center', va='center', transform=ax.transAxes)
ax.text(0.8, 0.3, r"$c$: Speed of Light", fontsize=12, ha='center', va='center', transform=ax.transAxes)

# Add title
ax.set_title("Gravitational-Light Speed Unification Equation", fontsize=16, y=1.1)

plt.tight_layout()
plt.savefig('../img/gravitational_light_speed_unification_eq.png', format='png', dpi=600, bbox_inches='tight')
plt.savefig('../img/gravitational_light_speed_unification_eq.svg', format='svg', bbox_inches='tight')
plt.close()

# 2. Spatial Spiral Motion Visualization
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Set parameters for spiral motion
t = np.linspace(0, 10, 1000)
r = 1  # radius of the spiral
omega = 1  # angular frequency
h = 0.5  # pitch parameter (axial speed component)

# Calculate spiral coordinates
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# Plot the spiral
ax.plot(x, y, z, linewidth=2.0, color='blue', label='Spiral Motion')

# Add arrows to show direction
arrow_positions = [0, 250, 500, 750]
for pos in arrow_positions:
    ax.quiver(x[pos], y[pos], z[pos], 
              x[pos+1]-x[pos], y[pos+1]-y[pos], z[pos+1]-z[pos],
              length=0.5, normalize=True, color='red', arrow_length_ratio=0.3)

# Add labels and title
ax.set_xlabel(r'$x$ [m]', fontsize=12)
ax.set_ylabel(r'$y$ [m]', fontsize=12)
ax.set_zlabel(r'$z$ [m]', fontsize=12)
ax.set_title("Spatial Cylindrical Spiral Motion", fontsize=14, pad=20)
ax.legend(fontsize=10, loc='upper left')

# Add equation as annotation
equation = r"$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ht \cdot \vec{k}$"
ax.text2D(0.05, 0.95, equation, transform=ax.transAxes, fontsize=12, 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../img/spatial_spiral_motion.png', format='png', dpi=600, bbox_inches='tight')
plt.savefig('../img/spatial_spiral_motion.svg', format='svg', bbox_inches='tight')
plt.close()

# 3. Mass Geometrization Visualization
plt.figure(figsize=(6, 4))
ax = plt.gca()

# Plot a 3D sphere representation in 2D to illustrate mass geometrization
circle = plt.Circle((0.5, 0.5), 0.3, color='lightblue', alpha=0.7)
ax.add_artist(circle)

# Add radial lines to represent spatial displacement vectors
num_lines = 16
for i in range(num_lines):
    angle = (i / num_lines) * 2 * np.pi
    x_start = 0.5
    y_start = 0.5
    x_end = 0.5 + 0.4 * np.cos(angle)
    y_end = 0.5 + 0.4 * np.sin(angle)
    ax.plot([x_start, x_end], [y_start, y_end], 'k-', alpha=0.8, linewidth=1.0)
    
    # Add arrow at the end
    arrow_length = 0.05
    ax.arrow(x_end - arrow_length * np.cos(angle), y_end - arrow_length * np.sin(angle), 
             arrow_length * np.cos(angle), arrow_length * np.sin(angle), 
             head_width=0.02, head_length=0.02, fc='k', ec='k')

# Set axis limits and remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Add equation and explanation
equation = r"$m = k \cdot \frac{dn}{d\Omega}$"
ax.text(0.5, 0.1, equation, fontsize=20, ha='center', va='center')
ax.text(0.5, 0.03, "Mass as Geometric Measure of Spatial Motion", fontsize=12, ha='center', va='center')

plt.title("Mass Geometrization Concept", fontsize=14, y=-0.1)
plt.tight_layout()
plt.savefig('../img/mass_geometrization.png', format='png', dpi=600, bbox_inches='tight')
plt.savefig('../img/mass_geometrization.svg', format='svg', bbox_inches='tight')
plt.close()

# 4. Spacetime Identity Visualization
plt.figure(figsize=(6, 4))
ax = plt.gca()

# Plot a simple spacetime diagram
x = np.linspace(0, 10, 100)
t = x / c * 1e9  # convert to nanoseconds for visualization

ax.plot(t, x, 'b-', linewidth=2.0, label=r'$\vec{r}(t)=\vec{C}t$')

# Add grid lines for better readability
ax.grid(True, linestyle='--', alpha=0.7)

# Add labels and title
ax.set_xlabel(r'$t$ [ns]', fontsize=12)
ax.set_ylabel(r'$r$ [m]', fontsize=12)
ax.set_title("Spacetime Identity Principle", fontsize=14)
ax.legend(fontsize=10, loc='upper left')

# Add annotation about constant speed
ax.text(0.1, 0.8, r"Constant speed: $c = \frac{dr}{dt}$", transform=ax.transAxes, fontsize=12, 
        bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../img/spacetime_identity.png', format='png', dpi=600, bbox_inches='tight')
plt.savefig('../img/spacetime_identity.svg', format='svg', bbox_inches='tight')
plt.close()

print("All figures generated successfully!")
print("Saved to: ../img/")
print("Files:")
print("- gravitational_light_speed_unification_eq.png/svg")
print("- spatial_spiral_motion.png/svg")
print("- mass_geometrization.png/svg")
print("- spacetime_identity.png/svg")