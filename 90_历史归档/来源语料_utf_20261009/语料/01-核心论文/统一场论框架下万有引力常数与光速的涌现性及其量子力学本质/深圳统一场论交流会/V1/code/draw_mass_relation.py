#!/usr/bin/env python3
"""
绘制质量与空间位移矢量条数的关系

公式: m = k * n / Ω
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义参数
k = 1.0  # 量子比例常数，归一化为1
Omega = 4.0 * np.pi  # 立体角，单位球面

# 空间位移矢量条数范围
n = np.linspace(1, 100, 100)

# 计算质量
m = k * n / Omega

# 创建图像
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)

# 绘制质量与空间位移矢量条数的关系
ax.plot(n, m, linewidth=2, color='cornflowerblue', 
        label=r'$m = k \frac{n}{\Omega}$')

# 计算普朗克质量（n=1）
m_p = k * 1 / Omega  # 普朗克质量

# 标记普朗克质量点
ax.scatter(1, m_p, color='red', s=100, label='Planck Mass (n=1)')
ax.text(1 + 2, m_p + 0.01, r'$m_p = k \frac{1}{4\pi}$', 
        fontsize=12, color='red', ha='left')

# 添加地球质量对应的n值的文本说明
n_earth = 2.744e32  # 地球对应的空间位移矢量条数
ax.text(50, 0.1, r'Earth Mass: $n \approx 2.744 \times 10^{32}$', 
        fontsize=12, color='green', ha='center')

# 添加坐标轴标签
ax.set_xlabel(r'Number of Space Displacement Vectors ($n$)', fontsize=12)
ax.set_ylabel(r'Mass ($m$) [arb. units]', fontsize=12)

# 设置标题
ax.set_title(r'Relation between Mass and Number of Space Displacement Vectors', fontsize=14)

# 添加图例
ax.legend(loc='upper left', fontsize=10, frameon=True)

# 设置坐标轴范围
ax.set_xlim(0, 105)
ax.set_ylim(0, max(m) * 1.2)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图像
plt.tight_layout()
plt.savefig('../img/mass_vector_relation.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/mass_vector_relation.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print("Mass vector relation image generated and saved to ../img/")
