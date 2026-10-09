import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, epsilon_0, hbar, e, G, m_e, m_p, alpha, pi

# 计算 Z' 和 Z
Z_prime = alpha * hbar * c / e**2  # 修正后的正确公式
Z = G * c / 2  # 注意：此定义基于张祥前理论，与主流物理学不同
Z_ratio = Z / Z_prime

# 电子-电子和质子-质子力比
F_ratio_ee = (e**2/(4*pi*epsilon_0)) / (G*m_e**2)
F_ratio_pp = (e**2/(4*pi*epsilon_0)) / (G*m_p**2)

# 可视化分析
particles = ['Electron', 'Proton']
force_ratios = [F_ratio_ee, F_ratio_pp]

plt.figure(figsize=(8,6))
plt.bar(particles, np.log10(force_ratios), color=['blue','red'])
plt.ylabel('log10(Electric/Gravitational Force Ratio)')
plt.title('Electric vs Gravitational Force Comparison')
plt.grid(True, axis='y')
plt.savefig('./Z_prime_force_ratio.png')

# 可视化 Z 和 Z' 的量纲对比
constants = ['Z (gravity)', "Z' (electromagnetic)"]
values = [Z, Z_prime]
plt.figure(figsize=(8,6))
plt.bar(constants, np.log10(values), color=['green','orange'])
plt.ylabel('log10(Value in SI units)')
plt.title('Comparison of Z and Z` Constants')
plt.grid(True, axis='y')
plt.savefig('./Z_Zprime_comparison.png')

