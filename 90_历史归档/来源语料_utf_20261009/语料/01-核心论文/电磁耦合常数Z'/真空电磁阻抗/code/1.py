import numpy as np
import matplotlib.pyplot as plt

# 常数定义（CODATA 2018）
c = 299792458  # m/s
Z0 = 376.730313668  # Ω
ZP = 29.9792458  # Ω
Z_prime = 1.347200e18  # kg·m⁴·s⁻³·C⁻²
Z_prime_norm = Z_prime * (8 * np.pi) / c**2  # Ω

# 数据准备
constants = ['$Z_0$', '$Z_P$', "$Z'$", "$Z'_\mathrm{norm}$"]
values = [Z0, ZP, Z_prime, Z_prime_norm]
units = ['Ω', 'Ω', 'kg·m⁴·s⁻³·C⁻²', 'Ω']
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

# 创建图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 主图：对数尺度对比
x_pos = np.arange(len(constants))
bars = ax1.bar(x_pos, values, color=colors, alpha=0.8, log=True)

ax1.set_ylabel('数值（对数尺度）', fontsize=12)
ax1.set_title('电磁常数几何化对比', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (bar, value, unit) in enumerate(zip(bars, values, units)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height*1.1,
             f'{value:.3e} {unit}', ha='center', va='bottom', rotation=45)

ax1.set_xticks(x_pos)
ax1.set_xticklabels(constants, fontsize=12)

# 子图：线性尺度下的阻抗对比（仅显示阻抗量纲的常数）
impedance_constants = ['$Z_0$', '$Z_P$', "$Z'_\mathrm{norm}$"]
impedance_values = [Z0, ZP, Z_prime_norm]
impedance_colors = ['#2E86AB', '#A23B72', '#C73E1D']

bars2 = ax2.bar(impedance_constants, impedance_values, color=impedance_colors, alpha=0.8)
ax2.set_ylabel('阻抗值 (Ω)', fontsize=12)
ax2.set_title('阻抗量纲常数对比（线性尺度）', fontsize=12)
ax2.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for bar, value in zip(bars2, impedance_values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{value:.2f} Ω', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 输出关键关系比值
print(f"Z₀/Z_P = {Z0/ZP:.6f} (理论值 = 4π = {4*np.pi:.6f})")
print(f"Z'_norm/Z_P = {Z_prime_norm/ZP:.6f} (理论值 = 0.5)")
print(f"Z₀/Z'_norm = {Z0/Z_prime_norm:.6f} (理论值 = 8π = {8*np.pi:.6f})")
