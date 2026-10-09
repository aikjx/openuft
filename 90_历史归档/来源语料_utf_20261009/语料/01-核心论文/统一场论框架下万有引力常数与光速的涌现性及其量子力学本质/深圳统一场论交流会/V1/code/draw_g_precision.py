#!/usr/bin/env python3
"""
绘制G的精度验证：理论值与CODATA 2018实验值的比较
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 设置LaTeX渲染和字体
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 定义实际数值
G_theo = 6.6743021e-11  # 统一场论理论值，单位：m³·kg⁻¹·s⁻²
G_exp = 6.67430e-11      # CODATA 2018实验值，单位：m³·kg⁻¹·s⁻²
G_exp_uncertainty = 0.000015e-11  # 实验不确定度

# 计算相对偏差
deviation = abs(G_theo - G_exp) / G_exp * 100

# 创建图像
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)

# 绘制理论值和实验值的对比
x = np.array([0.5, 1.5])
y = np.array([G_theo, G_exp])
error = np.array([0, G_exp_uncertainty])

# 绘制柱状图
ax.bar(x[0], y[0], width=0.4, color='cornflowerblue', label='Theoretical Value')
ax.bar(x[1], y[1], width=0.4, color='red', label='CODATA 2018 Experimental Value')

# 添加误差棒
ax.errorbar(x[1], y[1], yerr=error[1], fmt='none', color='black', capsize=5)

# 添加坐标轴标签
ax.set_xlabel(r'Value Type', fontsize=12)
ax.set_ylabel(r'Gravitational Constant $G$ ($m^3 \cdot kg^{-1} \cdot s^{-2}$)', fontsize=12)

# 设置标题
ax.set_title(r'Precision Verification of $G$: Theoretical vs. Experimental Value', fontsize=14)

# 设置x轴刻度标签
ax.set_xticks(x)
ax.set_xticklabels(['Theoretical Value', 'Experimental Value'])

# 添加相对偏差文本
theo_text = f'Theoretical: ${G_theo:.7e}$'
exp_text = f'Experimental: ${G_exp:.5e}({int(G_exp_uncertainty*1e16)})$'
dev_text = f'Relative Deviation: ${deviation:.8f}\%$'

ax.text(0.5, y[0] + 0.5e-12, theo_text, 
        ha='center', fontsize=12, color='cornflowerblue')
ax.text(1.5, y[1] + 0.5e-12, exp_text, 
        ha='center', fontsize=12, color='red')
ax.text(1.0, max(y) + 1.0e-12, dev_text, 
        ha='center', fontsize=14, color='green', weight='bold')

# 添加图例
ax.legend(loc='upper right', fontsize=10, frameon=True)

# 设置坐标轴范围
ax.set_ylim(min(y) - 2.0e-12, max(y) + 2.0e-12)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图像
plt.tight_layout()
plt.savefig('../img/g_precision.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/g_precision.svg', format='svg', bbox_inches='tight')

# 关闭图像
plt.close()

print(f"G precision verification image generated. Relative deviation: {deviation:.8f}%")
