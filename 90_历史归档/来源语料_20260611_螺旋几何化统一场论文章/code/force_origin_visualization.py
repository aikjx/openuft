#!/usr/bin/env python3
# ====================================================
# 算法联盟最高权限·力的本源结构可视化系统
# 可视化内容：空间螺旋3D图、力谱对数柱状图、曲率挠率比值图
# ====================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

alpha = 1 / 137.035999084
N = 1 / (alpha**2 * (1 - alpha))

forces = {
    '引力': {'factor': 1/alpha**2, 'color': '#1f77b4', 'order': -2},
    '强核力': {'factor': 1/alpha, 'color': '#ff7f0e', 'order': -1},
    '弱核力': {'factor': 1, 'color': '#2ca02c', 'order': 0},
    '电磁力': {'factor': alpha, 'color': '#d62728', 'order': 1},
    '第五力': {'factor': alpha**2, 'color': '#9467bd', 'order': 2},
    '第六力': {'factor': alpha**3, 'color': '#8c564b', 'order': 3},
    '第七力': {'factor': alpha**4, 'color': '#e377c2', 'order': 4},
}

for name, data in forces.items():
    data['normalized'] = data['factor'] / N
    data['percentage'] = data['normalized'] * 100

fig = plt.figure(figsize=(20, 15))

# ========== 图1：空间螺旋3D几何图 ==========
ax1 = fig.add_subplot(221, projection='3d')
theta = np.linspace(0, 20 * np.pi, 1000)
rho_val = 1
b_val = alpha * rho_val
x = rho_val * np.cos(theta)
y = rho_val * np.sin(theta)
z = b_val * theta
ax1.plot(x, y, z, color='#1f77b4', linewidth=2, label=f'α = {alpha:.6f}')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('空间螺旋几何结构\nR(θ) = (ρcosθ, ρsinθ, bθ)', fontsize=14)
ax1.legend()

# ========== 图2：力谱对数柱状图 ==========
ax2 = fig.add_subplot(222)
names = list(forces.keys())
factors = [forces[name]['factor'] for name in names]
colors = [forces[name]['color'] for name in names]
y_pos = np.arange(len(names))
ax2.barh(y_pos, np.log10(factors), color=colors)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(names)
ax2.set_xlabel('log10(强度因子)')
ax2.set_title('力的本源结构——强度因子谱', fontsize=14)
for i, (name, data) in enumerate(forces.items()):
    ax2.text(np.log10(data['factor']) + 0.1, i, 
             f'{data["factor"]:.2e}', va='center', fontsize=10)

# ========== 图3：归一化能量占比饼图 ==========
ax3 = fig.add_subplot(223)
percentages = [forces[name]['percentage'] for name in names]
colors = [forces[name]['color'] for name in names]
wedges, texts, autotexts = ax3.pie(percentages, labels=names, colors=colors,
                                   autopct='%1.4f%%', startangle=90,
                                   textprops={'fontsize': 8})
ax3.set_title('力的归一化能量占比', fontsize=14)

# ========== 图4：曲率与挠率关系图 ==========
ax4 = fig.add_subplot(224)
kappa = rho_val / (rho_val**2 + b_val**2)
tau = b_val / (rho_val**2 + b_val**2)
alpha_calc = tau / kappa
ax4.scatter(kappa, tau, s=200, c='#1f77b4', label=f'α = τ/κ = {alpha_calc:.6f}')
ax4.plot([0, kappa*2], [0, tau*2], 'r--', label=f'斜率 = α')
ax4.set_xlabel('曲率 κ')
ax4.set_ylabel('挠率 τ')
ax4.set_title('曲率-挠率关系图', fontsize=14)
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.savefig('force_origin_visualization.png', dpi=150, bbox_inches='tight')
print("可视化图像已保存为 force_origin_visualization.png")

# ========== 输出力的本源结构数据 ==========
print("\n" + "="*80)
print("力的本源结构数据")
print("="*80)
print(f"归一化因子 N = {N:.15f}")
print("\n" + "-"*80)
print(f"{'力类型':<10} {'阶数':<6} {'强度因子':<20} {'归一化强度':<20} {'能量占比':<15}")
print("-"*80)
for name, data in forces.items():
    print(f"{name:<10} {data['order']:<6} {data['factor']:<20.6e} {data['normalized']:<20.15f} {data['percentage']:<15.10e}")
print("-"*80)

# ========== 规律总结 ==========
print("\n" + "="*80)
print("力的本源结构规律总结")
print("="*80)
print("1. 力系按精细结构常数α的幂次排列：F_n = α^n")
print("2. 归一化强度：f_n = α^n / N")
print("3. 几何来源：α = τ/κ = b/ρ（曲率与挠率的比值）")
print("4. 归一化因子：N = Σ(α^n) = 1/[α²(1-α)] ≈ 18917")
print("5. 能量分布：引力占99.27%，其余力占0.73%")
print(f"6. 空间螺旋参数：ρ={rho_val}, b={b_val:.6f}, α={alpha:.6f}")

# ========== 高阶力物理效应预测 ==========
print("\n" + "="*80)
print("高阶力物理效应预测")
print("="*80)
print("第五力(α²) - 量子涨落力：")
print("  - 效应：微小的引力屏蔽或增强效应")
print("  - 量级：约5.3×10^-5，在纳米尺度可能观测")
print("  - 实验：高精度扭秤实验、原子干涉仪")
print("\n第六力(α³) - 暗能量力：")
print("  - 效应：宇宙加速膨胀的微观起源")
print("  - 量级：约3.9×10^-7")
print("  - 关联：可能与真空能量密度相关")
print("\n第七力(α⁴) - 暗物质力：")
print("  - 效应：暗物质相互作用的微观机制")
print("  - 量级：约2.8×10^-9")
print("  - 实验：暗物质探测实验可能间接验证")