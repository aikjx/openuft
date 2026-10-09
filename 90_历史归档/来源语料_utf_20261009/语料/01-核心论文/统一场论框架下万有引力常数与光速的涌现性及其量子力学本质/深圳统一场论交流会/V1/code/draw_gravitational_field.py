#!/usr/bin/env python3
"""
绘制引力场强度随距离的变化

公式: g = G * k * n / (Ω * r²)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义参数（归一化）
G = 1.0  # 万有引力常数，归一化为1
k = 1.0  # 量子比例常数，归一化为1
n = 1.0  # 空间位移矢量条数，归一化为1
Omega = 4.0 * np.pi  # 立体角，单位球面

# 距离范围（从0.1到10，避免r=0的奇点）
r = np.linspace(0.1, 10.0, 1000)

# 计算引力场强度的大小（取绝对值）
g = G * k * n / (Omega * r**2)

# 创建图像
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)

# 绘制引力场强度随距离的变化
ax.plot(r, g, linewidth=2, color='cornflowerblue', 
        label=r'$g = \frac{G k n}{\Omega r^2}$')

# 在图中标记地球表面重力加速度的典型值
ax.axhline(y=9.81, color='red', linestyle='--', linewidth=1, 
           label=r'Earth Surface Gravity ($g \approx 9.81 \, m/s^2$)')
ax.text(0.2, 9.81 + 0.5, r'$g_{Earth} \approx 9.81 \, m/s^2$', 
        fontsize=12, color='red', ha='left')

# 添加坐标轴标签
ax.set_xlabel(r'Distance ($r$) [arb. units]', fontsize=12)
ax.set_ylabel(r'Gravitational Field Strength ($g$) [arb. units]', fontsize=12)

# 设置标题
ax.set_title(r'Gravitational Field Strength vs. Distance', fontsize=14)

# 添加图例
ax.legend(loc='upper right', fontsize=10, frameon=True)

# 设置坐标轴范围
ax.set_ylim(0, max(g) * 1.2)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图像
plt.tight_layout()
plt.savefig('../img/gravitational_field.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/gravitational_field.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print("Gravitational field strength image generated and saved to ../img/")
