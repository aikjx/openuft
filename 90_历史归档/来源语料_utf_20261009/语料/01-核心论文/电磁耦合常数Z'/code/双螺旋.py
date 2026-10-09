import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return min(zs)

# 创建图形
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

# 球面参数
theta = np.linspace(0, np.pi, 50)
phi = np.linspace(0, 2*np.pi, 50)
theta, phi = np.meshgrid(theta, phi)

# 球面坐标
r = 1.0
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# 绘制透明球面
ax.plot_surface(x, y, z, alpha=0.1, color='gray')

# 双螺旋流线参数化
t = np.linspace(0, 4*np.pi, 200)

# 右旋螺旋（红色）- 对应电场相位 +π/2
x_right = 1.2 * np.sin(t) * np.cos(t + np.pi/2)
y_right = 1.2 * np.sin(t) * np.sin(t + np.pi/2) 
z_right = 1.2 * np.cos(t)

# 左旋螺旋（蓝色）- 对应磁场相位 -π/2
x_left = 1.2 * np.sin(t) * np.cos(-t - np.pi/2)
y_left = 1.2 * np.sin(t) * np.sin(-t - np.pi/2)
z_left = 1.2 * np.cos(t)

# 绘制双螺旋流线
ax.plot(x_right, y_right, z_right, 'r-', linewidth=3, label='右旋能流 (电场 E, 相位 +π/2)')
ax.plot(x_left, y_left, z_left, 'b-', linewidth=3, label='左旋能流 (磁场 B, 相位 -π/2)')

# 添加能流方向箭头
arrow_indices = [50, 100, 150]
for i in arrow_indices:
    # 右旋箭头
    arrow_r = Arrow3D([x_right[i], x_right[i+5]], 
                     [y_right[i], y_right[i+5]], 
                     [z_right[i], z_right[i+5]], 
                     mutation_scale=20, lw=2, arrowstyle="-|>", color="red")
    ax.add_artist(arrow_r)
    
    # 左旋箭头  
    arrow_l = Arrow3D([x_left[i], x_left[i+5]], 
                     [y_left[i], y_left[i+5]], 
                     [z_left[i], z_left[i+5]], 
                     mutation_scale=20, lw=2, arrowstyle="-|>", color="blue")
    ax.add_artist(arrow_l)

# 标注关键几何参数
# 球半径标注
ax.plot([0, 1], [0, 0], [0, 0], 'k--', alpha=0.5)
ax.text(0.5, -0.2, -0.2, r'$R=1$ (球面半径)', fontsize=12)

# 立体角标注
ax.text(-1.5, -1.5, 0, r'立体角: $\Omega = 4\pi$', fontsize=14, color='purple')
ax.text(-1.5, -1.5, -0.3, r'双层覆盖: $2 \times 4\pi = 8\pi$', fontsize=14, color='purple')

# 相位差标注
ax.text(1.2, 0, 1.2, r'$\Delta\phi = \pi$', fontsize=16, color='green')
ax.plot([1, 1.2], [0, 0], [1, 1.2], 'g--', alpha=0.7)

# 能流密度矢量
S_arrow = Arrow3D([0, 0.8], [0, 0], [0, 0.8], 
                 mutation_scale=25, lw=3, arrowstyle="-|>", color="orange")
ax.add_artist(S_arrow)
ax.text(0.4, 0, 0.4, r'$\mathbf{S} = \mathbf{E} \times \mathbf{B}$', fontsize=14, color='orange')

# 坐标轴标注
ax.text(1.5, 0, 0, 'X', fontsize=14, color='black')
ax.text(0, 1.5, 0, 'Y', fontsize=14, color='black')  
ax.text(0, 0, 1.5, 'Z', fontsize=14, color='black')

# 设置视角
ax.view_init(elev=30, azim=45)

# 设置坐标轴范围
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

# 标签和标题
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title('张祥前统一场论：双螺旋球面流几何结构\n'
            'Red: 右旋能流 (电场E, 相位+π/2) | Blue: 左旋能流 (磁场B, 相位-π/2)', 
            fontsize=16, pad=20)

# 添加图例
ax.legend(loc='upper left', bbox_to_anchor=(0, 1))

# 添加数学公式标注框
formula_text = (
    r'$\begin{aligned}'
    r'&\text{能流密度: }\mathbf{S} = \mathbf{E} \times \mathbf{B}\\'
    r'&\text{相位关系: }\phi_E - \phi_B = \frac{\pi}{2}\\'
    r'&\text{几何因子: }8\pi = 2 \times 4\pi\\'
    r'&\text{旋向定义: }\varphi_\pm = \omega t \pm kz'
    r'\end{aligned}$'
)
ax.text2D(-0.1, 0.1, formula_text, transform=ax.transAxes, fontsize=13,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

plt.tight_layout()
plt.show()
