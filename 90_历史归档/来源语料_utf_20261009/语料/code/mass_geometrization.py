import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# --- Physics & Mathematical Accuracy ---
# Physical Constants
m_p = 2.176434e-8  # kg (Planck mass, CODATA 2018)
G = 6.67430e-11    # m^3 kg^-1 s^-2 (Gravitational constant, CODATA 2018)
hbar = 1.0545718e-34  # J s (Reduced Planck constant)
c = 299792458       # m/s (Speed of light)

# Quantum proportional constant k (Eq 3.3)
k = 4 * np.pi * m_p

# --- Clarity & Interpretability / Aesthetics & Professionalism ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=False)  # Use matplotlib's built-in math rendering instead of full LaTeX

# Create figure with subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# --- Subplot 1: Mass vs Space Displacement Vectors (Eq 3.7) ---
# Object masses for comparison (from electron to Earth)
objects = {
    'Electron': 9.1093837015e-31,  # kg
    'Proton': 1.67262192369e-27,    # kg
    'Human': 70.0,                   # kg
    'Earth': 5.972e24               # kg
}

# Calculate space displacement vector count for each object (Eq 3.7: n = m/m_p)
object_names = list(objects.keys())
masses = np.array(list(objects.values()))
n_values = masses / m_p

# Plot on log-log scale
axs[0].scatter(masses, n_values, s=100, color='cornflowerblue', edgecolor='black', alpha=0.8)
axs[0].set_xscale('log')
axs[0].set_yscale('log')

# Add labels for each object
for i, name in enumerate(object_names):
    axs[0].annotate(name, xy=(masses[i], n_values[i]), xytext=(5, 5), textcoords='offset points', fontsize=9)

# Add theoretical line n = m/m_p
m_theory = np.logspace(-32, 26, 100)
n_theory = m_theory / m_p
axs[0].plot(m_theory, n_theory, linestyle='--', color='gray', linewidth=1.5, label=r'Theoretical: $n = \frac{m}{m_p}$')

# --- Annotations & Emphasis ---
axs[0].text(0.05, 0.95, r'$m = k \frac{n}{\Omega}$', transform=axs[0].transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Axes & Labels ---
axs[0].set_xlabel(r'$Mass (m) [kg]$', fontsize=11)
axs[0].set_ylabel(r'$Space Displacement Vectors (n)$', fontsize=11)
axs[0].set_title('Mass Geometrization: Mass vs Space Displacement Vectors', fontsize=12)
axs[0].legend(fontsize=9, loc='lower right')
axs[0].grid(True, alpha=0.3)

# --- Subplot 2: Relationship Between k, m_p, and Omega ---
# Visualize the relationship k = 4π m_p and Omega = 4π
# Create a polar plot to show spatial distribution
ax2 = axs[1].inset_axes([0.5, 0.1, 0.45, 0.45], polar=True)

# Create points on a sphere (Omega = 4π)
theta = np.linspace(0, 2*np.pi, 50)
for phi in np.linspace(0, np.pi, 10):
    r = 1.0
    ax2.plot(theta, np.full_like(theta, r), color='gray', alpha=0.3, linewidth=0.5)
    ax2.scatter(theta, np.full_like(theta, r), color='gray', alpha=0.2, s=5)

# Add Planck mass point
ax2.scatter(0, 1, s=150, color='red', edgecolor='black', label=r'Planck Mass ($m_p$)')

# Add text explanation
ax2.text(0.5, 0.5, r'$\Omega = 4\pi$', transform=ax2.transAxes, fontsize=9, 
         horizontalalignment='center', verticalalignment='center')

# Hide polar plot axes for cleaner look
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_ylim(0, 1.2)

# --- Main plot in subplot 2: k vs m_p relationship ---
# Create data for k vs m_p
m_p_range = np.linspace(0.5*m_p, 2*m_p, 100)
k_values = 4 * np.pi * m_p_range

# Plot relationship
axs[1].plot(m_p_range, k_values, linewidth=2.0, color='cornflowerblue', label=r'$k = 4\pi m_p$')

# Mark actual values
axs[1].scatter(m_p, k, s=100, color='red', edgecolor='black', zorder=5)
axs[1].annotate(r'Actual $m_p$ and $k$', xy=(m_p, k), xytext=(-50, 20), 
                textcoords='offset points', fontsize=10, 
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

# --- Annotations & Emphasis ---
equation_text = r'$m = k \cdot \frac{dn}{d\Omega}$ (Differential)\\$m = k \cdot \frac{n}{\Omega}$ (Integral)'
axs[1].text(0.05, 0.95, equation_text, transform=axs[1].transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Axes & Labels ---
axs[1].set_xlabel(r'$Planck Mass (m_p) [kg]$', fontsize=11)
axs[1].set_ylabel(r'$Quantum Proportional Constant (k) [kg]$', fontsize=11)
axs[1].set_title('Quantum Proportional Constant and Mass Geometrization', fontsize=12)
axs[1].legend(fontsize=9, loc='lower right')
axs[1].grid(True, alpha=0.3)

# --- Technical Output ---
plt.tight_layout()
plt.savefig('img/mass_geometrization.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('img/mass_geometrization.svg', format='svg', bbox_inches='tight')

print("Figure generated: img/mass_geometrization.png, img/mass_geometrization.svg")