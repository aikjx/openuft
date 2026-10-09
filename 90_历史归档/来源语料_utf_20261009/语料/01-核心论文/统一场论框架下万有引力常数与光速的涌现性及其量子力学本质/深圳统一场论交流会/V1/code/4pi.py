import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

# 设置LaTeX渲染和字体
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Times New Roman']})
rc('text', usetex=True)

# 设置参数
r = 1.0          # 螺旋半径
omega = 2.0      # 角速度 (rad/s)
c = 3.0          # 光速 (归一化为1)

# 计算轴向速度，确保满足光速约束：(r*omega)^2 + h^2 = c^2
h = np.sqrt(c**2 - (r*omega)**2)  # 轴向速度

# 生成时间点
T = 2*np.pi / omega   # 周期
t = np.linspace(0, 4*T, 1000)  # 四个周期

# 创建3D图像
fig = plt.figure(figsize=(12, 10), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# 添加中心物体（球体），代表产生螺旋运动的物体
center = np.array([0, 0, 0])
ax.scatter(center[0], center[1], center[2], color='red', s=1000, label='Central Object')

# 绘制多条不同角度的螺旋线，体现空间的4π立体角分布
num_helices = 8  # 螺旋线数量
for i in range(num_helices):
    # 为每条螺旋线设置不同的初始角度
    phi = 2 * np.pi * i / num_helices
    
    # 计算螺旋轨迹，每条螺旋线从不同角度出发
    x = r * np.cos(omega * t + phi)
    y = r * np.sin(omega * t + phi)
    z = h * t
    
    # 绘制螺旋线
    ax.plot(x, y, z, linewidth=1.5, alpha=0.8, label=f'Helix {i+1}')

# 绘制从中心物体向各个方向发散的射线，体现4π立体角
num_rays = 20  # 射线数量
for i in range(num_rays):
    # 生成均匀分布在球面上的方向向量
    theta = 2 * np.pi * i / num_rays  # 方位角
    phi = np.arccos(2 * np.random.rand() - 1)  # 仰角，均匀分布
    
    # 方向向量
    dx = np.sin(phi) * np.cos(theta)
    dy = np.sin(phi) * np.sin(theta)
    dz = np.cos(phi)
    
    # 射线长度
    length = 2.5
    
    # 绘制射线
    ax.quiver(0, 0, 0, dx, dy, dz, length=length, color='gray', alpha=0.5, arrow_length_ratio=0.05)

# 绘制xy平面的赤道圆
theta_circle = np.linspace(0, 2*np.pi, 100)
x_circle = r * np.cos(theta_circle)
y_circle = r * np.sin(theta_circle)
z_circle = np.zeros_like(theta_circle)
ax.plot(x_circle, y_circle, z_circle, linestyle='--', color='black', alpha=0.5, label='Equatorial Plane')

# 设置坐标轴标签
ax.set_xlabel(r'$x$', fontsize=14)
ax.set_ylabel(r'$y$', fontsize=14)
ax.set_zlabel(r'$z$', fontsize=14)

# 设置标题，使用LaTeX命令\pi代替Unicode字符π
ax.set_title(r'Cylindrical Helical Motion of Space Around an Object (4$\pi$ Solid Angle Distribution)', fontsize=16)

# 设置坐标轴范围，保证比例
max_range = 2.0
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(0, 4*h*T)

# 添加图例
ax.legend(loc='upper right', frameon=True, fontsize=10)

# 保存图像到img文件夹，移除tight_layout避免3D图布局问题
plt.savefig('../img/4pi_solid_angle.png', format='png', bbox_inches='tight', dpi=600)
plt.savefig('../img/4pi_solid_angle.svg', format='svg', bbox_inches='tight')

# 显示图像
plt.show()

print("4π立体角空间螺旋运动图像已生成，保存为../img/4pi_solid_angle.png和../img/4pi_solid_angle.svg")
