#!/usr/bin/env python3
# ====================================================
# Algorithm Alliance - Force Origin Structure Visualization
# Visualizations: 3D Space Spiral, Force Spectrum Log Bar Chart, Curvature-Torsion Diagram
# ====================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

alpha = 1 / 137.035999084
N = 1 / (alpha**2 * (1 - alpha))

forces = {
    'Gravity': {'factor': 1/alpha**2, 'color': '#1f77b4', 'order': -2},
    'Strong': {'factor': 1/alpha, 'color': '#ff7f0e', 'order': -1},
    'Weak': {'factor': 1, 'color': '#2ca02c', 'order': 0},
    'Electro': {'factor': alpha, 'color': '#d62728', 'order': 1},
    '5th Force': {'factor': alpha**2, 'color': '#9467bd', 'order': 2},
    '6th Force': {'factor': alpha**3, 'color': '#8c564b', 'order': 3},
    '7th Force': {'factor': alpha**4, 'color': '#e377c2', 'order': 4},
}

for name, data in forces.items():
    data['normalized'] = data['factor'] / N
    data['percentage'] = data['normalized'] * 100

fig = plt.figure(figsize=(20, 15))

# ========== Plot 1: 3D Space Spiral ==========
ax1 = fig.add_subplot(221, projection='3d')
theta = np.linspace(0, 20 * np.pi, 1000)
rho_val = 1
b_val = alpha * rho_val
x = rho_val * np.cos(theta)
y = rho_val * np.sin(theta)
z = b_val * theta
ax1.plot(x, y, z, color='#1f77b4', linewidth=2, label=f'alpha = {alpha:.6f}')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Space Spiral Geometry\nR(theta) = (rho*cos(theta), rho*sin(theta), b*theta)', fontsize=14)
ax1.legend()

# ========== Plot 2: Force Spectrum Log Bar Chart ==========
ax2 = fig.add_subplot(222)
names = list(forces.keys())
factors = [forces[name]['factor'] for name in names]
colors = [forces[name]['color'] for name in names]
y_pos = np.arange(len(names))
ax2.barh(y_pos, np.log10(factors), color=colors)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(names)
ax2.set_xlabel('log10(Intensity Factor)')
ax2.set_title('Force Origin Structure - Intensity Spectrum', fontsize=14)
for i, (name, data) in enumerate(forces.items()):
    ax2.text(np.log10(data['factor']) + 0.1, i, 
             f'{data["factor"]:.2e}', va='center', fontsize=10)

# ========== Plot 3: Normalized Energy Pie Chart ==========
ax3 = fig.add_subplot(223)
percentages = [forces[name]['percentage'] for name in names]
colors = [forces[name]['color'] for name in names]
wedges, texts, autotexts = ax3.pie(percentages, labels=names, colors=colors,
                                   autopct='%1.4f%%', startangle=90,
                                   textprops={'fontsize': 8})
ax3.set_title('Normalized Energy Distribution', fontsize=14)

# ========== Plot 4: Curvature-Torsion Relationship ==========
ax4 = fig.add_subplot(224)
kappa = rho_val / (rho_val**2 + b_val**2)
tau = b_val / (rho_val**2 + b_val**2)
alpha_calc = tau / kappa
ax4.scatter(kappa, tau, s=200, c='#1f77b4', label=f'alpha = tau/kappa = {alpha_calc:.6f}')
ax4.plot([0, kappa*2], [0, tau*2], 'r--', label=f'Slope = alpha')
ax4.set_xlabel('Curvature kappa')
ax4.set_ylabel('Torsion tau')
ax4.set_title('Curvature-Torsion Relationship', fontsize=14)
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.savefig('force_origin_visualization_en.png', dpi=150, bbox_inches='tight')
print("Visualization saved as force_origin_visualization_en.png")

# ========== Output data ==========
print("\n" + "="*80)
print("FORCE ORIGIN STRUCTURE DATA")
print("="*80)
print(f"Normalization Factor N = {N:.15f}")
print(f"Fine Structure Constant alpha = {alpha:.15f}")
print("\n" + "-"*80)
print(f"{'Force':<10} {'Order':<6} {'Intensity':<20} {'Normalized':<20} {'Percentage':<15}")
print("-"*80)
for name, data in forces.items():
    print(f"{name:<10} {data['order']:<6} {data['factor']:<20.6e} {data['normalized']:<20.15f} {data['percentage']:<15.10e}")
print("-"*80)

# ========== Summary ==========
print("\n" + "="*80)
print("FORCE ORIGIN STRUCTURE LAWS")
print("="*80)
print("1. Forces are ordered by powers of alpha: F_n = alpha^n")
print("2. Normalized intensity: f_n = alpha^n / N")
print("3. Geometric origin: alpha = tau/kappa = b/rho")
print("4. Normalization factor: N = sum(alpha^n) = 1/[alpha^2(1-alpha)] ~ 18917")
print("5. Energy distribution: Gravity 99.27%, others 0.73%")
print("6. Space spiral: rho=1, b=alpha, kappa~0.9999, tau~0.0073")

# ========== Predictions ==========
print("\n" + "="*80)
print("HIGHER-ORDER FORCE PHYSICAL EFFECTS")
print("="*80)
print("5th Force (alpha^2) - Quantum Fluctuation Force:")
print("  - Effect: Weak gravitational shielding/enhancement")
print("  - Scale: ~5.3e-5, observable at nanometer scale")
print("  - Experiments: High-precision torsion balance, atom interferometry")
print("\n6th Force (alpha^3) - Dark Energy Force:")
print("  - Effect: Microscopic origin of cosmic acceleration")
print("  - Scale: ~3.9e-7")
print("  - Correlation: May relate to vacuum energy density")
print("\n7th Force (alpha^4) - Dark Matter Force:")
print("  - Effect: Microscopic mechanism of dark matter interaction")
print("  - Scale: ~2.8e-9")
print("  - Experiments: Dark matter detection (LUX, XENON)")