import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# 全局样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 9)
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['grid.alpha'] = 0.2

# 定义参数
r = 2.5
omega = 1.8
h = 0.6
t = np.linspace(0, 12 * np.pi, 1500)
x = r * np.cos(omega * t)
y = r * np.sin(omega * t)
z = h * t
pitch = (2 * np.pi * h) / omega

# 3D绘图
fig = plt.figure(facecolor='#f8f9fa')
ax = fig.add_subplot(111, projection='3d', facecolor='white')

# 渐变色螺旋线 - 修复后的版本
cmap = plt.cm.plasma
colors = cmap(t / t.max())
points = np.array([x, y, z]).T.reshape(-1, 1, 3)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = Line3DCollection(segments, colors=colors, linewidths=3, zorder=5)
ax.add_collection(lc)

# 添加运动方向箭头
t_arrow = 8 * np.pi
x_arrow = r * np.cos(omega * t_arrow)
y_arrow = r * np.sin(omega * t_arrow)
z_arrow = h * t_arrow
dx = -r * omega * np.sin(omega * t_arrow)
dy = r * omega * np.cos(omega * t_arrow)
dz = h
ax.quiver(x_arrow, y_arrow, z_arrow, dx, dy, dz, color='red', length=3, arrow_length_ratio=0.1, zorder=10, label='运动切向')

# 标注参数
ax.text2D(0.02, 0.98, f'$r={r:.1f}, \omega={omega:.1f}, h={h:.1f}$\n螺距 $P={pitch:.2f}$', 
          transform=ax.transAxes, fontsize=13, verticalalignment='top',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

# 坐标轴设置
ax.set_xlabel('$X = r\cos\omega t$', fontsize=14, labelpad=12)
ax.set_ylabel('$Y = r\sin\omega t$', fontsize=14, labelpad=12)
ax.set_zlabel('$Z = ht$', fontsize=14, labelpad=12)
ax.set_title('圆柱螺旋线运动轨迹', fontsize=16, pad=25)

# 等比例坐标轴
max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2
mid_x, mid_y, mid_z = (x.max()+x.min())/2, (y.max()+y.min())/2, (z.max()+z.min())/2
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# 视角与图例
ax.view_init(elev=30, azim=60)
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('helix_3d_fixed.png', dpi=300, bbox_inches='tight')
print("Plot saved successfully as helix_3d_fixed.png!")
plt.close()