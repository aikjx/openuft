import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# --- Physics & Mathematical Accuracy ---
# Physical Constants
m_p = 2.176434e-8  # kg (Planck mass, CODATA 2018)
G_exp = 6.67430e-11  # m^3 kg^-1 s^-2 (Gravitational constant, CODATA 2018 experimental value)
hbar = 1.0545718e-34  # J s (Reduced Planck constant)
c = 299792458       # m/s (Speed of light)

# Quantum proportional constant k (Eq 3.3)
k = 4 * np.pi * m_p

# Calculate G using quantum geometric expression (Eq 3.5)
G_theo = (16 * np.pi**2 * hbar * c) / k**2

# --- Clarity & Interpretability / Aesthetics & Professionalism ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=False)  # Use matplotlib's built-in math rendering instead of full LaTeX

# Create figure with subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# --- Subplot 1: G vs k Relationship (Eq 3.5) ---
k_range = np.linspace(0.5*k, 1.5*k, 100)  # Range around actual k value
G_values = (16 * np.pi**2 * hbar * c) / (k_range**2)

# Plot relationship
axs[0].plot(k_range, G_values, linewidth=2.0, color='cornflowerblue', label=r'$G = \frac{16\pi^2 \hbar c}{k^2}$')

# Mark actual values
axs[0].scatter(k, G_theo, s=150, color='red', edgecolor='black', zorder=5, label='Calculated $G$')
axs[0].scatter(k, G_exp, s=150, color='green', edgecolor='black', zorder=5, label='Experimental $G$ (CODATA 2018)')

# Connect calculated and experimental values with dashed line to show agreement
axs[0].plot([k, k], [min(G_theo, G_exp), max(G_theo, G_exp)], linestyle='--', color='gray', linewidth=1.5)

# --- Annotations & Emphasis ---
axs[0].text(0.05, 0.95, r'$G = \frac{16\pi^2 \hbar c}{k^2}$', transform=axs[0].transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# Add agreement text
deviation = abs((G_theo - G_exp) / G_exp) * 100
axs[0].annotate(f'Deviation: {deviation:.8f}%', xy=(k, G_theo), xytext=(10, -25), 
                textcoords='offset points', fontsize=10, 
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

# --- Axes & Labels ---
axs[0].set_xlabel(r'$Quantum Proportional Constant (k) [kg]$', fontsize=11)
axs[0].set_ylabel(r'$Gravitational Constant (G) [m^3 kg^{-1} s^{-2}]$', fontsize=11)
axs[0].set_title('Quantum Geometric Emergence of G', fontsize=12)
axs[0].legend(fontsize=9, loc='upper right')
axs[0].grid(True, alpha=0.3)

# --- Subplot 2: G in terms of Fundamental Constants ---
# Create a diagram showing G's dependence on hbar, c, and k
# Plot a central G node connected to its fundamental components

def create_connector(ax, x1, y1, x2, y2, label, color='gray'):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.5, zorder=1)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y, label, fontsize=9, ha='center', va='center', zorder=2)

# Plot G at center
axs[1].scatter(0.5, 0.5, s=2000, color='red', alpha=0.8, zorder=3)
axs[1].text(0.5, 0.5, r'$G$', fontsize=20, ha='center', va='center', color='white', zorder=4)

# Plot fundamental constants around G
constants = {
    r'$\hbar$': (0.1, 0.8, 'blue'),
    r'$c$': (0.9, 0.8, 'green'),
    r'$k$': (0.5, 0.2, 'orange'),
    r'$16\pi^2$': (0.1, 0.2, 'purple')
}

# Plot constant nodes
for const, (x, y, color) in constants.items():
    axs[1].scatter(x, y, s=1000, color=color, alpha=0.8, zorder=3)
    axs[1].text(x, y, const, fontsize=14, ha='center', va='center', color='white', zorder=4)
    create_connector(axs[1], 0.5, 0.5, x, y, '', color='gray')

# Add equation text
axs[1].text(0.5, 0.95, r'$G = \frac{16\pi^2 \hbar c}{k^2}$', 
            transform=axs[1].transAxes, fontsize=12, ha='center', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

# --- Axes & Labels ---
axs[1].set_title('G Dependence on Fundamental Constants', fontsize=12)
axs[1].axis('off')  # Hide axes for cleaner diagram

# --- Technical Output ---
plt.tight_layout()
plt.savefig('img/g_emergence.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('img/g_emergence.svg', format='svg', bbox_inches='tight')

print(f"Experimental G: {G_exp:.10e} m^3 kg^-1 s^-2")
print(f"Calculated G:   {G_theo:.10e} m^3 kg^-1 s^-2")
print(f"Deviation:      {deviation:.10f}%")
print("Figure generated: img/g_emergence.png, img/g_emergence.svg")