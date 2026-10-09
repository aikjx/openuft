from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 光速分量设置
c = 299792458.0
Cx, Cy, Cz = 0.6 * c, 0.8 * c, 0.0 * c

# 微观尺度时间范围（适合可视化）
t_3d = np.linspace(0, 1e-9, 100)

# 计算三维轨迹
X_3d = Cx * t_3d
Y_3d = Cy * t_3d
Z_3d = Cz * t_3d

# 创建三维可视化
fig = plt.figure(figsize=(15, 7))

# 左侧：三维空间轨迹
ax1 = fig.add_subplot(121, projection='3d')
trajectory = ax1.plot(X_3d, Y_3d, Z_3d, 'b-', linewidth=2)[0]

# 添加速度矢量
ax1.quiver(X_3d[-2], Y_3d[-2], Z_3d[-2], 
           X_3d[-1] - X_3d[-2], Y_3d[-1] - Y_3d[-2], Z_3d[-1] - Z_3d[-2],
           length=10, color='r', arrow_length_ratio=0.3)

ax1.set_title('三维空间运动轨迹', fontsize=14)
ax1.set_xlabel('X 位置 (m)', fontsize=10)
ax1.set_ylabel('Y 位置 (m)', fontsize=10)
ax1.set_zlabel('Z 位置 (m)', fontsize=10)
ax1.grid(True)

# 右侧：XY平面投影
ax2 = fig.add_subplot(122)
ax2.plot(X_3d, Y_3d, 'b-', linewidth=2)
ax2.set_title('XY平面投影轨迹', fontsize=14)
ax2.set_xlabel('X 位置 (m)', fontsize=12)
ax2.set_ylabel('Y 位置 (m)', fontsize=12)
ax2.grid(True)
ax2.axis('equal')  # 保持比例一致

plt.tight_layout()
plt.suptitle('时空同一化方程三维轨迹分析', fontsize=16, y=1.02)
plt.savefig('../visualizations/3d_space_trajectory.png', dpi=300, bbox_inches='tight')
plt.show()