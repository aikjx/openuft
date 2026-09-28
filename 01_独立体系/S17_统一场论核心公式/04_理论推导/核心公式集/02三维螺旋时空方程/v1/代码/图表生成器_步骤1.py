#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
t = np.linspace(0, 4*np.pi, 1000)

# 图2：速度分析
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 计算速度分量
Vx = -r * omega * np.sin(omega * t)
Vy = r * omega * np.cos(omega * t)
Vz = np.full_like(t, p)
V_magnitude = np.sqrt(Vx**2 + Vy**2 + Vz**2)

# 子图1：速度分量
axes[0,0].plot(t, Vx, 'r-', linewidth=2, label='Vx')
axes[0,0].plot(t, Vy, 'g-', linewidth=2, label='Vy')
axes[0,0].plot(t, Vz, 'b-', linewidth=2, label='Vz')
axes[0,0].set_xlabel('时间 t (s)')
axes[0,0].set_ylabel('速度分量 (m/s)')
axes[0,0].set_title('速度分量随时间变化')
axes[0,0].legend()
axes[0,0].grid(True)

# 子图2：速度模
theoretical_V = np.sqrt(r**2 * omega**2 + p**2)
axes[0,1].plot(t, V_magnitude, 'k-', linewidth=2.5, label='计算值')
axes[0,1].axhline(y=theoretical_V, color='r', linestyle='--', linewidth=2)
axes[0,1].set_xlabel('时间 t (s)')
axes[0,1].set_ylabel('速度模 |V| (m/s)')
axes[0,1].set_title('速度模恒定验证')
axes[0,1].legend()
axes[0,1].grid(True)

# 子图3：速度矢量相位图
axes[1,0].plot(Vx, Vy, 'b-', linewidth=1.5)
axes[1,0].scatter(Vx[0], Vy[0], color='red', s=100, label='起点')
axes[1,0].scatter(Vx[-1], Vy[-1], color='orange', s=100, label='终点')
axes[1,0].set_xlabel('Vx (m/s)')
axes[1,0].set_ylabel('Vy (m/s)')
axes[1,0].set_title('XY平面速度矢量轨迹')
axes[1,0].legend()
axes[1,0].grid(True)
axes[1,0].axis('equal')

# 子图4：速度大小分布
axes[1,1].hist(V_magnitude, bins=30, color='skyblue', alpha=0.7, edgecolor='black')
axes[1,1].axvline(x=theoretical_V, color='red', linestyle='--', linewidth=2)
axes[1,1].set_xlabel('速度模 (m/s)')
axes[1,1].set_ylabel('频次')
axes[1,1].set_title('速度模分布')
axes[1,1].grid(True)

plt.suptitle('速度场完整分析', fontsize=16)
plt.tight_layout()
plt.savefig('02_速度分量分析.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ 图2：速度分析 生成成功')