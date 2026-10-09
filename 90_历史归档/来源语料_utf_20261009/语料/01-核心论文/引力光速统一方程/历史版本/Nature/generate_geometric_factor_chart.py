import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.lines import Line2D
import matplotlib.patches as patches

# 避免显示窗口，直接保存图片
plt.switch_backend('Agg')

# 创建图形
fig = plt.figure(figsize=(12, 10), dpi=300)
ax = fig.add_subplot(111, aspect='equal')

# 设置坐标轴范围
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# 隐藏坐标轴
ax.axis('off')

# 绘制单位球面（二维投影）
circle = Circle((0, 0), 1, fill=False, edgecolor='black', linewidth=2)
ax.add_patch(circle)

# 绘制赤道平面（二维相互作用平面）
equator = Line2D([-1.2, 1.2], [0, 0], color='blue', linestyle='--', linewidth=2)
ax.add_line(equator)

# 绘制北极点和南极点
ax.plot(0, 1, 'ro', markersize=8)
ax.plot(0, -1, 'ro', markersize=8)
ax.text(0.1, 1.05, 'North Pole', fontsize=12)
ax.text(0.1, -1.15, 'South Pole', fontsize=12)

# 绘制不同角度的投影示例
angles = [30, 60, 90, 120, 150]
colors = ['red', 'orange', 'green', 'purple', 'brown']

for i, angle in enumerate(angles):
    theta = np.radians(angle)
    # 计算球面上点的坐标
    x = np.sin(theta)
    y = np.cos(theta)
    
    # 绘制从原点到球面上点的连线
    ax.plot([0, x], [0, y], color=colors[i], linestyle='-', linewidth=1.5)
    
    # 绘制球面上的点
    ax.plot(x, y, 'o', color=colors[i], markersize=6)
    
    # 绘制到赤道平面的投影线（垂直线）
    ax.plot([x, x], [0, y], color=colors[i], linestyle='--', linewidth=1)
    
    # 绘制投影点
    ax.plot(x, 0, 's', color=colors[i], markersize=5)
    
    # 添加角度标签
    ax.text(x*1.1, y*1.1, f'θ={angle}°', fontsize=10, color=colors[i])

# 绘制积分示意区域
wedge = Wedge((0, 0), 1, 0, 180, width=0.1, color='lightblue', alpha=0.5)
ax.add_patch(wedge)
ax.text(0.3, 0.3, 'Integration Area', fontsize=12, color='blue')

# 添加公式说明
formula_text = r"""
$\eta = \frac{1}{4\pi}\int_{0}^{2\pi}\int_{0}^{\pi} \sin\theta \cdot \mu(\theta) \, d\theta d\phi = 2$

where $\mu(\theta) = \sin\theta$ is the projection efficiency function
"""

ax.text(0, -1.3, formula_text, fontsize=14, ha='center', bbox=dict(facecolor='wheat', alpha=0.7, boxstyle='round'))

# 添加解释框
explanation = """
Physical Significance of Geometric Factor 2:
1. Projection of 3D isotropic spatial motion onto 2D interaction plane
2. Sum of projection efficiencies from all directions results in factor 2
3. This factor forms the key geometric basis for unifying gravity and electromagnetism
"""

ax.text(0, 1.2, explanation, fontsize=12, ha='center', va='center',
        bbox=dict(facecolor='lightgreen', alpha=0.7, boxstyle='round,pad=0.5'))

# 添加标题
ax.set_title('Gravitational Constant Geometric Factor: Spatial Projection Visualization', 
             fontsize=16, pad=20, weight='bold')

# 保存为SVG格式
save_path = r'd:\a10\aikjx\code\my_lib\utf\01-核心论文\引力光速统一方程\Nature\geometric_factor_projection.svg'
plt.savefig(save_path, format='svg', dpi=300, bbox_inches='tight')
print(f'Chart saved to: {save_path}')

# 保存为PNG格式作为备份
png_path = save_path.replace('.svg', '.png')
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f'PNG version saved to: {png_path}')

plt.close()
