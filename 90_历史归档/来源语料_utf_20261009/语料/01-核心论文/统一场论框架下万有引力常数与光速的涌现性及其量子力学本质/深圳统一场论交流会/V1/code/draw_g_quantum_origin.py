#!/usr/bin/env python3
"""
绘制G的量子几何起源

公式: G = 16π²ħc / k²
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义参数（归一化）
hbar = 1.0  # 约化普朗克常数，归一化为1
c = 1.0  # 光速，归一化为1

# 量子比例常数k的范围
k = np.linspace(0.1, 10.0, 1000)

# 计算G
g = (16.0 * np.pi**2 * hbar * c) / (k**2)

# 创建图像
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)

# 绘制G随k的变化
ax.plot(k, g, linewidth=2, color='cornflowerblue', 
        label=r'$G = \frac{16\pi^2 \hbar c}{k^2}$')

# 计算量子比例常数k = 4π m_p对应的G值
k_quantum = 4.0 * np.pi  # 归一化的k值
G_quantum = (16.0 * np.pi**2 * hbar * c) / (k_quantum**2)

# 标记量子比例常数点
ax.scatter(k_quantum, G_quantum, color='red', s=100, 
           label=r'Quantum Proportionality Constant ($k = 4\pi m_p$)')
ax.text(k_quantum + 0.5, G_quantum + 0.5, r'$k = 4\pi m_p$', 
        fontsize=12, color='red', ha='left')

# 添加坐标轴标签
ax.set_xlabel(r'Quantum Proportionality Constant ($k$) [arb. units]', fontsize=12)
ax.set_ylabel(r'Gravitational Constant ($G$) [arb. units]', fontsize=12)

# 设置标题
ax.set_title(r'Quantum Geometric Origin of Gravitational Constant $G$', fontsize=14)

# 添加图例
ax.legend(loc='upper right', fontsize=10, frameon=True)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图像
plt.tight_layout()
plt.savefig('../img/g_quantum_origin.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/g_quantum_origin.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print("G quantum origin image generated and saved to ../img/")
