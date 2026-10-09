import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 光速
c = 299792458.0

plt.figure(figsize=(15, 7))

# 左侧：相对论时空光锥
plt.subplot(121)
t_rel = np.linspace(0, 1e-6, 100)
x_rel = np.linspace(0, 300, 100)
T_rel, X_rel = np.meshgrid(t_rel, x_rel)

light_cone = c**2 * T_rel**2 - X_rel**2

plt.contourf(T_rel, X_rel, light_cone, 20, cmap='viridis', alpha=0.8)
plt.contour(T_rel, X_rel, light_cone, levels=[0], colors='red', linewidths=2)
plt.colorbar(label='ds² 值')
plt.title('相对论时空光锥', fontsize=14)
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('空间位置 x (m)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 右侧：时空同一化关系
plt.subplot(122)
t_uni = np.linspace(0, 1e-6, 100)
x_uni = c * t_uni

plt.plot(t_uni, x_uni, 'r-', linewidth=3, label=f'x = ct (c = {c:.2e} m/s)')
plt.fill_between(t_uni, x_uni, alpha=0.3, color='red')
plt.title('时空同一化关系', fontsize=14)
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('空间位置 x (m)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

plt.tight_layout()
plt.suptitle('时空同一化方程与相对论时空观对比', fontsize=16, y=1.02)
plt.savefig('../visualizations/relativity_comparison.png', dpi=300, bbox_inches='tight')
plt.show()