#!/usr/bin/env python3
"""
绘制空间光速螺旋运动方程

方程: r(t) = r*cos(ωt)i + r*sin(ωt)j + ht*k
约束: h² + (rω)² = c²
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义参数，确保满足光速约束
r = 1.0  # 螺旋半径
c = 10.0  # 光速，增大c值确保c² > (r*omega)²
omega = 2.0  # 角速度 (rad/s)，减小omega值确保满足约束

h = np.sqrt(c**2 - (r*omega)**2)  # 轴向速度

# 时间范围
T = 2.0 * np.pi / omega  # 一个旋转周期
t = np.linspace(0, 4.0 * T, 1000)  # 四个周期

# 计算三维螺旋坐标
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t

# 创建3D图
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# 绘制螺旋线
ax.plot(x, y, z, linewidth=2, color='cornflowerblue', 
        label=r'$\vec{r}(t) = r\cos(\omega t)\vec{i} + r\sin(\omega t)\vec{j} + ht\vec{k}$')

# 绘制螺旋线在xy平面的投影
ax.plot(x, y, np.zeros_like(x), linewidth=1, color='gray', linestyle='--', 
        label='XY Plane Projection')

# 绘制螺旋线在xz平面的投影
ax.plot(x, np.zeros_like(x), z, linewidth=1, color='green', linestyle='--', 
        label='XZ Plane Projection')

# 添加起点和终点标记
ax.scatter(x[0], y[0], z[0], color='red', s=100, label='Start Point')
ax.scatter(x[-1], y[-1], z[-1], color='blue', s=100, label='End Point')

# 添加坐标轴标签
ax.set_xlabel(r'$x$', fontsize=14)
ax.set_ylabel(r'$y$', fontsize=14)
ax.set_zlabel(r'$z$', fontsize=14)

# 设置标题
ax.set_title(r'Light Speed Helical Motion in Space', fontsize=16)

# 添加图例
ax.legend(loc='upper right', fontsize=10, frameon=True)

# 设置坐标轴刻度和范围
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(0, 1.5 * max(z))
ax.set_xticks([-1.0, 0.0, 1.0])
ax.set_yticks([-1.0, 0.0, 1.0])
ax.set_zticks(np.linspace(0, 1.5 * max(z), 5))

# 保存图像
plt.savefig('../img/spiral_motion.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/spiral_motion.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print("Light speed helical motion image generated and saved to ../img/")
