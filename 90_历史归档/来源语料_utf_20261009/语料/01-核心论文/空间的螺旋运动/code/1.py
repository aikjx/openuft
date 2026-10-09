import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib
# 设置matplotlib支持中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 定义符号变量
t, r, omega, h, c = sp.symbols('t r omega h c', real=True)

# 定义位移矢量分量
x = r * sp.cos(omega * t)
y = r * sp.sin(omega * t)
z = h * t

# 计算速度分量（对时间t求导）
vx = sp.diff(x, t)
vy = sp.diff(y, t)
vz = sp.diff(z, t)

print("速度分量：")
print(f"vx = {vx}")
print(f"vy = {vy}")
print(f"vz = {vz}")

# 计算速度的模平方
v_squared = vx**2 + vy**2 + vz**2
print(f"\n速度模平方的表达式：v_squared = {v_squared}")

# 简化表达式
v_squared_simplified = sp.simplify(v_squared)
print(f"简化后的速度模平方：v_squared_simplified = {v_squared_simplified}")

# 根据三角恒等式 sin^2 + cos^2 = 1，进一步简化
v_squared_final = r**2 * omega**2 + h**2
print(f"进一步简化（理论结果）：v_squared_final = {v_squared_final}")

# 验证两者是否相等
print(f"\n是否相等？{v_squared_simplified == v_squared_final}")

# 瞬时速度的模
v_norm = sp.sqrt(v_squared_final)
print(f"\n瞬时速度的模：|V| = {v_norm}")

# 根据理论，速度模必须等于光速c，因此有约束条件：r^2*omega^2 + h^2 = c^2
constraint = sp.Eq(v_squared_final, c**2)
print(f"\n光速约束条件：{constraint}")

# 数值验证：选择一组满足约束条件的参数，计算不同时间点的速度模
print("\n" + "="*50)
print("数值验证部分")
print("="*50)

# 设定光速c（数值，单位m/s）
c_val = 3e8
# 设定螺旋半径r和角速度omega，然后根据约束计算h
r_val = 1.0  # 1米
omega_val = 0.5 * c_val / r_val  # 使得旋转分量 r*omega = 0.5*c

# 计算直线速度h，使得约束成立：h^2 = c^2 - (r*omega)^2
h_val = np.sqrt(c_val**2 - (r_val * omega_val)**2)
print(f"设定的参数：")
print(f"  c = {c_val:.2e} m/s")
print(f"  r = {r_val} m")
print(f"  omega = {omega_val:.2e} rad/s")
print(f"  旋转速度分量 v_rot = r*omega = {r_val * omega_val:.2e} m/s")
print(f"  直线速度分量 h = {h_val:.2e} m/s")
print(f"  检查约束：(r*omega)^2 + h^2 = {(r_val*omega_val)**2 + h_val**2:.2e}，应与 c^2 = {c_val**2:.2e} 相等")

# 计算不同时间点的速度模
time_points = np.linspace(0, 10, 5)  # 从0到10秒，取5个时间点
print(f"\n在不同时间点计算速度的模（应恒为c）：")
for t_val in time_points:
    # 速度分量数值
    vx_val = -r_val * omega_val * np.sin(omega_val * t_val)
    vy_val = r_val * omega_val * np.cos(omega_val * t_val)
    vz_val = h_val
    # 速度模
    v_norm_val = np.sqrt(vx_val**2 + vy_val**2 + vz_val**2)
    print(f"  t = {t_val:.2f} s, |V| = {v_norm_val:.2e} m/s, 相对误差 = {abs(v_norm_val - c_val)/c_val*100:.2e}%")

# 验证是否恒等于c（数值精度内）
tolerance = 1e-10
all_close = all(abs(np.sqrt((r_val*omega_val)**2 + h_val**2) - c_val) < tolerance for _ in time_points)
print(f"\n所有时间点的速度模是否都等于c（误差<{tolerance}）？ {all_close}")

# 可视化部分
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 可视化参数设置（使用适合绘图的缩放值）
c_plot = 10.0  # 绘图用的总速度（单位：任意单位/s）
r_plot = 2.0  # 螺旋半径
v_rot = 6.0  # 旋转速度分量
omega_plot = v_rot / r_plot  # 角速度
h_plot = np.sqrt(c_plot**2 - v_rot**2)  # 直线速度分量

t_vals = np.linspace(0, 2, 100)  # 时间数组

# 计算轨迹
x_vals = r_plot * np.cos(omega_plot * t_vals)
y_vals = r_plot * np.sin(omega_plot * t_vals)
z_vals = h_plot * t_vals

# 计算速度分量
vx_vals = -r_plot * omega_plot * np.sin(omega_plot * t_vals)
vy_vals = r_plot * omega_plot * np.cos(omega_plot * t_vals)
vz_vals = np.full_like(t_vals, h_plot)

# 计算速度模
v_norm_vals = np.sqrt(vx_vals**2 + vy_vals**2 + vz_vals**2)

# 创建静态可视化图
fig = plt.figure(figsize=(12, 10))

# 1. 3D螺旋轨迹图
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(x_vals, y_vals, z_vals, label='空间螺旋运动轨迹', linewidth=2)
ax1.set_title('(1) 空间的螺旋运动轨迹')
ax1.set_xlabel('X轴')
ax1.set_ylabel('Y轴')
ax1.set_zlabel('Z轴')
ax1.legend()
ax1.grid(True)

# 2. 速度分量随时间变化图
ax2 = fig.add_subplot(222)
ax2.plot(t_vals, vx_vals, label='vx (旋转分量)', linestyle='-', color='r', linewidth=1.5)
ax2.plot(t_vals, vy_vals, label='vy (旋转分量)', linestyle='--', color='g', linewidth=1.5)
ax2.plot(t_vals, vz_vals, label='vz (直线分量)', linestyle='-.', color='b', linewidth=1.5)
ax2.set_title('(2) 速度分量随时间变化')
ax2.set_xlabel('时间 t')
ax2.set_ylabel('速度分量')
ax2.legend()
ax2.grid(True)

# 3. 速度模随时间变化图
ax3 = fig.add_subplot(223)
ax3.plot(t_vals, v_norm_vals, label='速度模 |V|', color='purple', linewidth=2)
ax3.axhline(y=c_plot, linestyle='--', color='red', label=f'总速度 c = {c_plot}', linewidth=1.5)
ax3.set_title('(3) 速度模随时间变化')
ax3.set_xlabel('时间 t')
ax3.set_ylabel('速度模')
ax3.legend()
ax3.grid(True)

# 4. XY平面投影图
ax4 = fig.add_subplot(224)
ax4.plot(x_vals, y_vals, label='XY平面投影（圆形轨迹）', color='orange', linewidth=2)
ax4.set_aspect('equal')
ax4.set_title('(4) XY平面投影')
ax4.set_xlabel('X轴')
ax4.set_ylabel('Y轴')
ax4.legend()
ax4.grid(True)

plt.tight_layout()
plt.savefig('螺旋运动可视化.png', dpi=300, bbox_inches='tight')
plt.close()

# 创建动画可视化
fig_anim = plt.figure(figsize=(10, 8))
ax_anim = fig_anim.add_subplot(111, projection='3d')

# 设置坐标轴范围
max_range = np.array([x_vals.max()-x_vals.min(), y_vals.max()-y_vals.min(), z_vals.max()-z_vals.min()]).max() / 2.0
mid_x = (x_vals.max()+x_vals.min()) * 0.5
mid_y = (y_vals.max()+y_vals.min()) * 0.5
mid_z = (z_vals.max()+z_vals.min()) * 0.5

ax_anim.set_xlim(mid_x - max_range, mid_x + max_range)
ax_anim.set_ylim(mid_y - max_range, mid_y + max_range)
ax_anim.set_zlim(mid_z - max_range, mid_z + max_range)

ax_anim.set_title('空间螺旋运动动画演示')
ax_anim.set_xlabel('X轴')
ax_anim.set_ylabel('Y轴')
ax_anim.set_zlabel('Z轴')

# 初始化轨迹线和质点
line, = ax_anim.plot([], [], [], 'b-', linewidth=2, label='运动轨迹')
point, = ax_anim.plot([], [], [], 'ro', markersize=8, label='当前位置')
velocity_arrow = ax_anim.quiver([], [], [], [], [], [], color='g', length=0.5, normalize=True, label='速度矢量')

ax_anim.legend()
ax_anim.grid(True)

# 初始化函数
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point

# 更新函数
def update(frame):
    # 更新轨迹
    line.set_data(x_vals[:frame], y_vals[:frame])
    line.set_3d_properties(z_vals[:frame])
    
    # 更新质点位置（使用列表形式避免警告）
    point.set_data([x_vals[frame]], [y_vals[frame]])
    point.set_3d_properties([z_vals[frame]])
    
    # 更新速度矢量（重新创建，使用更可靠的清除方式）
    scale = 0.1
    
    # 清除所有collections（quiver使用collections）
    for coll in ax_anim.collections[:]:
        coll.remove()
    
    # 创建新的速度矢量箭头
    ax_anim.quiver(
        x_vals[frame], y_vals[frame], z_vals[frame],
        vx_vals[frame]*scale, vy_vals[frame]*scale, vz_vals[frame]*scale,
        color='g', length=0.5, normalize=True
    )
    
    return line, point

# 创建动画
ani = FuncAnimation(fig_anim, update, frames=len(t_vals), init_func=init, interval=50, blit=False)

# 保存动画
ani.save('螺旋运动动画.gif', writer='pillow', fps=20)
plt.close()

print("\n可视化完成！")
print("已生成文件：")
print("1. 螺旋运动可视化.png (静态图)")
print("2. 螺旋运动动画.gif (动画)")

# ==================================================
# 可视化部分
# ==================================================
print("\n" + "="*50)
print("可视化部分")
print("="*50)

# 生成数据点用于可视化
t_vals = np.linspace(0, 0.5, 500)  # 更短的时间范围，以便清晰看到螺旋轨迹
x_vals = r_val * np.cos(omega_val * t_vals)
y_vals = r_val * np.sin(omega_val * t_vals)
z_vals = h_val * t_vals

# 计算速度分量
vx_vals = -r_val * omega_val * np.sin(omega_val * t_vals)
vy_vals = r_val * omega_val * np.cos(omega_val * t_vals)
vz_vals = np.full_like(t_vals, h_val)

# 计算速度模
v_norm_vals = np.sqrt(vx_vals**2 + vy_vals**2 + vz_vals**2)

# 创建一个包含多个子图的图形
fig = plt.figure(figsize=(15, 12))

# 1. 3D螺旋轨迹图
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(x_vals, y_vals, z_vals, label='空间螺旋运动轨迹')
ax1.set_xlabel('X坐标 (m)')
ax1.set_ylabel('Y坐标 (m)')
ax1.set_zlabel('Z坐标 (m)')
ax1.set_title('(a) 空间螺旋运动3D轨迹')
ax1.legend()
ax1.grid(True)

# 2. 速度分量随时间变化图
ax2 = fig.add_subplot(222)
ax2.plot(t_vals, vx_vals, label='vx (旋转分量)', linestyle='-', color='r')
ax2.plot(t_vals, vy_vals, label='vy (旋转分量)', linestyle='--', color='g')
ax2.plot(t_vals, vz_vals, label='vz (直线分量)', linestyle='-.', color='b')
ax2.set_xlabel('时间 t (s)')
ax2.set_ylabel('速度分量 (m/s)')
ax2.set_title('(b) 速度分量随时间变化')
ax2.legend()
ax2.grid(True)

# 3. 速度模随时间变化图
ax3 = fig.add_subplot(223)
ax3.plot(t_vals, v_norm_vals, label='速度模 |V|', color='purple')
ax3.axhline(y=c_val, linestyle='--', color='red', label=f'光速 c = {c_val:.2e} m/s')
ax3.set_xlabel('时间 t (s)')
ax3.set_ylabel('速度模 (m/s)')
ax3.set_title('(c) 速度模随时间变化')
ax3.legend()
ax3.grid(True)

# 4. 投影图 - XY平面投影
ax4 = fig.add_subplot(224)
ax4.plot(x_vals, y_vals, label='XY平面投影（圆形轨迹）', color='orange')
ax4.set_xlabel('X坐标 (m)')
ax4.set_ylabel('Y坐标 (m)')
ax4.set_title('(d) XY平面投影')
ax4.axis('equal')  # 确保圆形显示为正圆
ax4.legend()
ax4.grid(True)

# 调整子图间距
plt.tight_layout()

# 保存静态图像
plt.savefig('螺旋运动可视化.png', dpi=300, bbox_inches='tight')

# 显示图像
plt.show()

# 额外创建一个动画，展示空间螺旋运动的动态过程
print("\n" + "="*50)
print("创建动画...")
print("="*50)

# 生成用于动画的数据
t_anim = np.linspace(0, 0.5, 100)
x_anim = r_val * np.cos(omega_val * t_anim)
y_anim = r_val * np.sin(omega_val * t_anim)
z_anim = h_val * t_anim

# 创建动画图形
fig_anim = plt.figure(figsize=(10, 8))
ax_anim = fig_anim.add_subplot(111, projection='3d')

# 设置坐标轴范围
total_length = z_anim[-1]
ax_anim.set_xlim(-r_val*1.2, r_val*1.2)
ax_anim.set_ylim(-r_val*1.2, r_val*1.2)
ax_anim.set_zlim(0, total_length*1.1)

# 设置标签和标题
ax_anim.set_xlabel('X坐标 (m)')
ax_anim.set_ylabel('Y坐标 (m)')
ax_anim.set_zlabel('Z坐标 (m)')
ax_anim.set_title('空间螺旋运动动态演示')

# 初始化轨迹线和当前位置点
trajectory, = ax_anim.plot([], [], [], 'b-', linewidth=2, label='运动轨迹')
current_point, = ax_anim.plot([], [], [], 'ro', markersize=8, label='当前位置')

# 添加速度向量箭头
velocity_arrow = ax_anim.quiver([], [], [], [], [], [], length=1, color='g', label='速度向量')

# 添加图例
ax_anim.legend()
ax_anim.grid(True)

# 初始化函数
def init():
    trajectory.set_data([], [])
    trajectory.set_3d_properties([])
    current_point.set_data([], [])
    current_point.set_3d_properties([])
    velocity_arrow.set_segments([])
    return trajectory, current_point, velocity_arrow

# 更新函数
def update(frame):
    # 更新轨迹
    trajectory.set_data(x_anim[:frame+1], y_anim[:frame+1])
    trajectory.set_3d_properties(z_anim[:frame+1])
    
    # 更新当前位置
    current_point.set_data([x_anim[frame]], [y_anim[frame]])
    current_point.set_3d_properties([z_anim[frame]])
    
    # 更新速度向量
    # 计算当前速度向量的分量
    vx = vx_vals[frame]
    vy = vy_vals[frame]
    vz = vz_vals[frame]
    
    # 调整向量长度以便可视化
    arrow_scale = 1e-9  # 速度向量太大，需要缩放
    velocity_arrow.set_segments([[[x_anim[frame], y_anim[frame], z_anim[frame]],
                                 [x_anim[frame] + vx*arrow_scale, 
                                  y_anim[frame] + vy*arrow_scale, 
                                  z_anim[frame] + vz*arrow_scale]]])
    
    return trajectory, current_point, velocity_arrow

# 创建并保存动画
ani = FuncAnimation(fig_anim, update, frames=len(t_anim), init_func=init, interval=50, blit=True)

# 保存动画为GIF
ani.save('螺旋运动动画.gif', writer='pillow', fps=20)

print("动画创建完成！")
print("可视化结果已保存为：")
print("1. 螺旋运动可视化.png（静态图像）")
print("2. 螺旋运动动画.gif（动态动画）")
