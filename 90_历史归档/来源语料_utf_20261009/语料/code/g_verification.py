import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# --- Physics & Mathematical Accuracy ---
# Physical Constants
m_p = 2.176434e-8  # kg (Planck mass, CODATA 2018)
G_exp = 6.67430e-11  # m^3 kg^-1 s^-2 (Gravitational constant, CODATA 2018 experimental value)
hbar = 1.0545718e-34  # J s (Reduced Planck constant)
c = 299792458       # m/s (Speed of light)

# Earth parameters
M_earth = 5.972e24  # kg (Earth mass)
R_earth = 6371000   # m (Earth radius)

# Quantum proportional constant k (Eq 3.3)
k = 4 * np.pi * m_p

# Calculate G using quantum geometric expression (Eq 3.5)
G_theo = (16 * np.pi**2 * hbar * c) / k**2

# Calculate Earth gravity using both G values
g_theo = (G_theo * M_earth) / R_earth**2
g_exp = (G_exp * M_earth) / R_earth**2

# --- Clarity & Interpretability / Aesthetics & Professionalism ---
plt.style.use('seaborn-v0_8-paper')  # Scientific style
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})  # Font choice
rc('text', usetex=False)  # Use matplotlib's built-in math rendering instead of full LaTeX

# Create figure
fig = plt.figure(figsize=(10, 6))

# --- Main Plot: G Verification Across Scales ---
ax = fig.add_subplot(111)

# Scale categories
scales = ['Quantum Scale', 'Macroscopic Scale']

# Values to plot
theoretical_values = [G_theo, g_theo]
experimental_values = [G_exp, g_exp]

# Position for bars
x = np.arange(len(scales))
width = 0.35

# Create bar plot
bar1 = ax.bar(x - width/2, theoretical_values, width, color='cornflowerblue', label='Theoretical Value')
bar2 = ax.bar(x + width/2, experimental_values, width, color='green', label='Experimental Value')

# --- Annotations & Emphasis ---
# Add values on top of bars
for i, rect in enumerate(bar1):
    height = rect.get_height()
    if i == 0:  # G values
        ax.text(rect.get_x() + rect.get_width()/2., height*1.05, 
                f'{height:.10e}', ha='center', va='bottom', fontsize=9)
    else:  # g values
        ax.text(rect.get_x() + rect.get_width()/2., height*1.05, 
                f'{height:.6f}', ha='center', va='bottom', fontsize=9)

for i, rect in enumerate(bar2):
    height = rect.get_height()
    if i == 0:  # G values
        ax.text(rect.get_x() + rect.get_width()/2., height*1.05, 
                f'{height:.10e}', ha='center', va='bottom', fontsize=9)
    else:  # g values
        ax.text(rect.get_x() + rect.get_width()/2., height*1.05, 
                f'{height:.6f}', ha='center', va='bottom', fontsize=9)

# Add percentage difference annotations
for i in range(len(scales)):
    theo_val = theoretical_values[i]
    exp_val = experimental_values[i]
    diff = abs((theo_val - exp_val) / exp_val) * 100
    ax.text(x[i], min(theo_val, exp_val)*0.95, f'Diff: {diff:.8f}%', 
            ha='center', va='top', fontsize=9, color='red')

# --- Axes & Labels ---
ax.set_yscale('log')
ax.set_xticks(x)
ax.set_xticklabels(scales, fontsize=11)
ax.set_title(r'Verification of $G$ Across Scales', fontsize=12)
ax.set_ylabel(r'Value (Log Scale)', fontsize=11)

# Add axis labels for each scale
# Quantum scale: G values
ax.text(0, G_exp*1.5, r'$G , [	ext{m}^3	ext{kg}^{-1}	ext{s}^{-2}]$', 
        ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.8))

# Macroscopic scale: g values
ax.text(1, g_exp*1.5, r'$g , [	ext{m/s}^2]$', 
        ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.8))

# Legend
ax.legend(fontsize=10, loc='upper right')

# Grid
ax.grid(True, alpha=0.3)

# --- Add inset: Earth Gravity Comparison ---
ax_inset = fig.add_axes([0.65, 0.2, 0.3, 0.3])  # [left, bottom, width, height]

# Plot Earth gravity comparison
ax_inset.bar(['Theoretical', 'Experimental'], [g_theo, g_exp], color=['cornflowerblue', 'green'])
ax_inset.set_title('Earth Gravity Comparison', fontsize=10)
ax_inset.set_ylabel(r'$g , [	ext{m/s}^2]$', fontsize=9)
ax_inset.tick_params(axis='x', labelsize=9, rotation=45)
ax_inset.grid(True, alpha=0.3)

# Add values on top of bars
for i, value in enumerate([g_theo, g_exp]):
    ax_inset.text(i, value*1.05, f'{value:.6f}', ha='center', va='bottom', fontsize=8)

# --- Add inset: Planck Mass Calculation ---
ax_inset2 = fig.add_axes([0.25, 0.2, 0.3, 0.3])  # [left, bottom, width, height]

# Values for Planck mass calculation
planck_values = [
    r'$m_p = \sqrt{\frac{\hbar c}{G}}$',
    r'$m_p = k \cdot \frac{1}{4\pi}$',
    r'$G = \frac{16\pi^2 \hbar c}{k^2}$'
]

y_pos = np.arange(len(planck_values))
values = [m_p, m_p, G_theo]

# Plot as text-based visualization
ax_inset2.barh(y_pos, np.ones(len(planck_values)), alpha=0)
ax_inset2.set_title('Planck Mass Relationships', fontsize=10)
ax_inset2.set_yticks(y_pos)
ax_inset2.set_yticklabels(planck_values, fontsize=9)
ax_inset2.set_xlim(0, 1)
ax_inset2.set_xticks([])
ax_inset2.grid(False)

# Add calculated values
for i, val in enumerate(values):
    if i < 2:  # Planck mass values
        ax_inset2.text(0.95, i, f'{val:.10e} kg', ha='right', va='center', fontsize=8, color='red')
    else:  # G value
        ax_inset2.text(0.95, i, f'{val:.10e} m^3kg^-1s^-2', ha='right', va='center', fontsize=8, color='red')

# --- Technical Output ---
plt.tight_layout()
plt.savefig('img/g_verification.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('img/g_verification.svg', format='svg', bbox_inches='tight')

print(f"Quantum Scale: G_theo = {G_theo:.10e}, G_exp = {G_exp:.10e}, Deviation = {abs((G_theo-G_exp)/G_exp)*100:.8f}%")
print(f"Macroscopic Scale: g_theo = {g_theo:.6f} m/s², g_exp = {g_exp:.6f} m/s², Deviation = {abs((g_theo-g_exp)/g_exp)*100:.8f}%")
print("Figure generated: img/g_verification.png, img/g_verification.svg")