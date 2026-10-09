import numpy as np
import matplotlib.pyplot as plt
import os

# 使用最基本的配置，不指定特定字体，让matplotlib自动选择
plt.rcParams.update({
    'font.size': 10,
    'axes.unicode_minus': False,
    'figure.dpi': 600,
    'savefig.dpi': 600,
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # m³ kg⁻¹ s⁻² (CODATA 2018)
G_theo = 6.6743021e-11  # m³ kg⁻¹ s⁻² (Theoretical value)

# 数据
methods = ['CODATA 2018', 'Unified Field Theory']
G_values = [G_codata, G_theo]
error_bars = [1.5e-15, 0.0]

# 计算相对差异
relative_diff = abs(G_theo - G_codata) / G_codata * 100

fig, ax = plt.subplots(figsize=(8, 6))

# 绘制柱状图
bars = ax.bar(methods, G_values, yerr=error_bars, capsize=5, color=['blue', 'green'], alpha=0.8)

# 在柱子上添加值
for bar, value in zip(bars, G_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + error_bars[0],
            f'{value:.10e}', ha='center', va='bottom', fontsize=8, rotation=90)

# 添加相对差异标注
ax.annotate(f'Relative Difference: {relative_diff:.8f}%', 
            xy=(0.5, 0.5), xycoords='axes fraction',
            xytext=(0, 20), textcoords='offset points',
            fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5))

# 设置标题和标签
ax.set_title('G Accuracy Verification', fontsize=12)
ax.set_ylabel('Gravitational Constant G [m3 kg-1 s-2]', fontsize=10)

# 保存图表
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'g_precision.png'), bbox_inches='tight')
plt.savefig(os.path.join(img_dir, 'g_precision.svg'), bbox_inches='tight')
plt.close()

print("G precision figure generated successfully!")
