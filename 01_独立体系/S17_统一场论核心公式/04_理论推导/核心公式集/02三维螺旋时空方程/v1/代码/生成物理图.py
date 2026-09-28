#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持
plt.rcParams.update({
    'font.family': ['SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
    'axes.unicode_minus': False
})

# 参数设置
r = 1.0
omega = 1.0
p = 1.0

# 图5：物理诠释
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 子图1：场强分量
theta = np.linspace(0, 2*np.pi, 100)

# 电场（直线分量）
E_magnitude = p
axes[0,0].axhline(y=E_magnitude, color='blue', linewidth=3, label=f'电场强度 E = {E_magnitude:.1f}')

# 磁场（旋转分量）
B_magnitude = r * omega
axes[0,0].plot(theta, B_magnitude * np.cos(theta), color='red', linewidth=3, label='磁场分量 B(θ)')
axes[0,0].set_xlabel('相位 θ (rad)')
axes[0,0].set_ylabel('场强 (相对单位)')
axes[0,0].set_title('电磁场分量变化')
axes[0,0].legend()
axes[0,0].grid(True)
axes[0,0].set_xlim(0, 2*np.pi)

# 子图2：引力场分布
r_range = np.linspace(0.5, 3.0, 100)
g_field = r * omega**2 * (r / r_range)**2

axes[0,1].plot(r_range, g_field, 'green', linewidth=2.5)
axes[0,1].scatter([r], [r * omega**2], color='red', s=100, 
                 edgecolors='black', linewidth=2, label='参考点', zorder=5)
axes[0,1].set_xlabel('距离 r (m)')
axes[0,1].set_ylabel('引力场强度 (相对单位)')
axes[0,1].set_title('引力场径向分布 ∝ 1/r²')
axes[0,1].legend()
axes[0,1].grid(True)
axes[0,1].set_yscale('log')

# 子图3：统一场相位关系
phase = np.linspace(0, 2*np.pi, 100)

# 归一化的场分量
E_normalized = np.ones_like(phase) * p / np.sqrt(r**2 * omega**2 + p**2)
B_normalized = r * omega * np.cos(phase) / np.sqrt(r**2 * omega**2 + p**2)
g_normalized = -np.sin(phase)

axes[1,0].plot(phase, E_normalized, 'b-', linewidth=2, label='电场分量')
axes[1,0].plot(phase, B_normalized, 'r-', linewidth=2, label='磁场分量')
axes[1,0].plot(phase, g_normalized, 'g-', linewidth=2, label='引力分量')
axes[1,0].set_xlabel('相位 ωt (rad)')
axes[1,0].set_ylabel('归一化场强')
axes[1,0].set_title('统一场相位关系')
axes[1,0].legend()
axes[1,0].grid(True)
axes[1,0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 子图4：场强矢量图
x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
X, Y = np.meshgrid(x, y)

# 计算每个点的场强（简化模型）
R = np.sqrt(X**2 + Y**2)
R[R < 0.5] = 0.5

# 引力场（指向中心）
Ex = -X / R**2
Ey = -Y / R**2

axes[1,1].quiver(X, Y, Ex, Ey, np.sqrt(Ex**2 + Ey**2), cmap='viridis', alpha=0.7)
circle = plt.Circle((0, 0), r, fill=False, edgecolor='red', linewidth=2, linestyle='--')
axes[1,1].add_patch(circle)
axes[1,1].set_xlabel('X (m)')
axes[1,1].set_ylabel('Y (m)')
axes[1,1].set_title('引力场矢量分布')
axes[1,1].set_aspect('equal')
axes[1,1].grid(True)

plt.suptitle('物理场的几何起源诠释', fontsize=16)
plt.tight_layout()
plt.savefig('05_物理场诠释.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ 图5：物理诠释 生成成功')