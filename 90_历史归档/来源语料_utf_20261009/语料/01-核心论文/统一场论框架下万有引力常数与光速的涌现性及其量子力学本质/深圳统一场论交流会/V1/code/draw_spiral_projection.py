#!/usr/bin/env python3
"""
绘制空间光速螺旋运动的平面投影

包括xy平面投影（圆周运动）和xz平面投影（螺旋线）
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义参数，确保满足光速约束
r = 1.0  # 螺旋半径
c = 10.0  # 光速，增大c值确保c² > (r*omega)²
omega = 2.0  # 角速度 (rad/s)，减小omega值确保满足约束

# 计算轴向速度
h = np.sqrt(c**2 - (r*omega)**2)  # 轴向速度

# 时间范围
T = 2.0 * np.pi / omega  # 一个旋转周期
t = np.linspace(0, 4.0 * T, 1000)  # 四个周期

# 计算三维螺旋坐标
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# 创建图像，包含两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# 左图：xy平面投影（圆周运动）
ax1.plot(x, y, linewidth=2, color='cornflowerblue', label=r'$x-y$ Projection')
ax1.scatter(x[0], y[0], color='red', s=100, label='Start Point')
ax1.scatter(x[-1], y[-1], color='blue', s=100, label='End Point')
ax1.set_aspect('equal')
ax1.set_xlabel(r'$x$', fontsize=12)
ax1.set_ylabel(r'$y$', fontsize=12)
ax1.set_title(r'$xy$-Plane Projection (Circular Motion)', fontsize=14)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.7)

# 右图：xz平面投影（螺旋线）
ax2.plot(x, z, linewidth=2, color='cornflowerblue', label=r'$x-z$ Projection')
ax2.scatter(x[0], z[0], color='red', s=100, label='Start Point')
ax2.scatter(x[-1], z[-1], color='blue', s=100, label='End Point')
ax2.set_xlabel(r'$x$', fontsize=12)
ax2.set_ylabel(r'$z$', fontsize=12)
ax2.set_title(r'$xz$-Plane Projection (Helical Line)', fontsize=14)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.7)

# 整体标题
fig.suptitle(r'Plane Projections of Light Speed Helical Motion in Space', fontsize=16, y=1.02)

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('../img/spiral_projection.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/spiral_projection.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print("Space light speed helical motion projections generated and saved to ../img/")