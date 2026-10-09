import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 避免显示窗口，直接保存图片
plt.switch_backend('Agg')

# 创建图形和3D轴
fig = plt.figure(figsize=(12, 10), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# 定义角度范围
theta = np.linspace(0, np.pi, 100)
phi = np.linspace(0, 2*np.pi, 100)
theta_grid, phi_grid = np.meshgrid(theta, phi)

# 计算球坐标到笛卡尔坐标的转换
r = np.sin(theta_grid)  # μ(θ) = sinθ
x = r * np.sin(theta_grid) * np.cos(phi_grid)
y = r * np.sin(theta_grid) * np.sin(phi_grid)
z = r * np.cos(theta_grid)

# 计算投影效率值（用于颜色映射）
efficiency = np.sin(theta_grid)

# 绘制3D曲面
surf = ax.plot_surface(x, y, z, rstride=5, cstride=5, 
                       facecolors=cm.viridis(efficiency),
                       alpha=0.9, linewidth=0.5, edgecolor='k')

# 创建颜色映射的辅助标量映射
m = cm.ScalarMappable(cmap=cm.viridis)
m.set_array(efficiency)

# 添加颜色条
cbar = fig.colorbar(m, ax=ax, shrink=0.6, aspect=10)
cbar.set_label('Projection Efficiency μ(θ)', fontsize=14)
cbar.set_ticks([0, 0.5, 1])
cbar.set_ticklabels(['0', '0.5', '1'])

# 添加公式标签
ax.text(0, 0, 1.2, r'$\mu(\theta) = \sin\theta$', fontsize=20, 
        color='red', weight='bold', ha='center')

# 添加关键角度的标记
key_thetas = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, 5*np.pi/6, np.pi]
key_labels = ['0°', '30°', '45°', '60°', '90°', '120°', '135°', '150°', '180°']

for i, theta_val in enumerate(key_thetas):
    r_val = np.sin(theta_val)
    x_val = r_val * np.sin(theta_val)  # 在phi=0平面
    y_val = 0
    z_val = r_val * np.cos(theta_val)
    
    # 添加点标记
    ax.scatter(x_val, y_val, z_val, color='black', s=50, marker='o')
    
    # 添加角度标签（避免重叠）
    offset = 0.1
    ax.text(x_val + (offset if i < 4 else -offset), 
            y_val, 
            z_val + 0.1, 
            key_labels[i], 
            fontsize=10, ha='center')

# 设置坐标轴标签
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
ax.set_zlabel('Z', fontsize=14)

# 设置坐标轴范围
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)

# 添加标题
ax.set_title('3D Surface Plot of Projection Efficiency Function μ(θ) = sinθ', 
             fontsize=16, pad=20, weight='bold')

# 添加说明框
explanation = """
Key Features:
• Maximum efficiency at θ=90° (equator)
• Zero efficiency at θ=0° and 180° (poles)
• This function determines how 3D spatial motion
  projects onto 2D interaction plane
"""

# 在图表右侧添加说明框
props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
ax.text2D(0.02, 0.02, explanation, transform=ax.transAxes, fontsize=12, 
          verticalalignment='bottom', bbox=props)

# 优化视角
ax.view_init(elev=30, azim=45)

# 添加网格
ax.grid(True, linestyle='--', alpha=0.7)

# 保存为SVG格式
save_path = r'd:\a10\aikjx\code\my_lib\utf\01-核心论文\引力光速统一方程\Nature\projection_efficiency.svg'
plt.savefig(save_path, format='svg', dpi=300, bbox_inches='tight')
print(f'Chart saved to: {save_path}')

# 保存为PNG格式作为备份
png_path = save_path.replace('.svg', '.png')
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f'PNG version saved to: {png_path}')

plt.close()
