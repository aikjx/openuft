import numpy as np
import matplotlib.pyplot as plt
import os

# 使用极简配置，避免任何可能的字体问题
plt.rcParams.clear()
plt.rcParams.update({
    'figure.dpi': 600,
    'savefig.dpi': 600,
    'axes.unicode_minus': False,
})

# 确保img目录存在
code_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(os.path.dirname(code_dir), 'img')
os.makedirs(img_dir, exist_ok=True)

# 物理常数
G_codata = 6.67430e-11  # CODATA 2018
G_theo = 6.6743021e-11  # 理论值

# 数据
methods = ['CODATA', 'Theory']
G_values = [G_codata, G_theo]

# 创建图表
fig, ax = plt.figure(figsize=(6, 4)), plt.gca()

# 绘制简单柱状图
bars = ax.bar(methods, G_values, color=['blue', 'green'], alpha=0.8)

# 简化的标题和标签，避免特殊字符
ax.set_title('G Constant Comparison')
ax.set_ylabel('G (m^3 kg^-1 s^-2)')

# 简化显示，不添加数值标签

# 保存图表，使用PNG格式
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'g_precision.png'), format='png', bbox_inches='tight')
plt.close()

print("Simple G precision figure generated successfully!")
