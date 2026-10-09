import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制平面
xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.5, color='gray')

# 点源位置
source = np.array([0, 0, 1])
ax.scatter(*source, color='red', s=100, label='Source')

# 粒子数量
n_particles = 100

# 生成各向同性方向
theta = np.arccos(2 * np.random.rand(n_particles) - 1)  # 极角（0到π）
phi = 2 * np.pi * np.random.rand(n_particles)  # 方位角（0到2π）

# 速度向量
vx = np.sin(theta) * np.cos(phi)
vy = np.sin(theta) * np.sin(phi)
vz = np.cos(theta)

# 粒子初始位置（点源）
x = np.full(n_particles, source[0])
y = np.full(n_particles, source[1])
z = np.full(n_particles, source[2])

# 创建粒子散点图
particles = ax.scatter(x, y, z, color='blue', s=5, label='Particles')

# 文本显示统计信息
text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=10)

# 跟踪哪些粒子击中了平面
hit_plane = np.zeros(n_particles, dtype=bool)

# 动画更新函数
def update(num):
    global x, y, z, hit_plane
    
    # 移动未击中平面的粒子
    for i in range(n_particles):
        if not hit_plane[i]:
            x[i] += vx[i] * 0.05
            y[i] += vy[i] * 0.05
            z[i] += vz[i] * 0.05
            if z[i] <= 0:
                hit_plane[i] = True
                z[i] = 0  # 固定在平面上

    # 更新散点图
    particles._offsets3d = (x, y, z)
    
    # 统计击中平面的粒子数
    count = np.sum(hit_plane)
    ratio = count / n_particles if n_particles > 0 else 0
    text.set_text(f"Hit plane: {count}/{n_particles} = {ratio:.2f}\nGeometric factor: 2 (4pi/2pi)")
    
    return particles, text

# 初始化动画
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=False, repeat=True)

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-0.1, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Isotropic Particle Flow Through Plane (Geometric Factor = 2)')
ax.legend()

print("Animation starting... Close the window to stop.")
plt.show()
