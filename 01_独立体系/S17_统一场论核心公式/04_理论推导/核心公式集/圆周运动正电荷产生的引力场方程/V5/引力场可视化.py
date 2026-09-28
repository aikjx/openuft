import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 物理常数
c = 2.99792458e8  # 光速 (m/s)
epsilon_0 = 8.8541878128e-12  # 真空介电常数 (F/m)

# 模拟参数
q = 1.602176634e-19  # 电荷量 (C)，使用电子电荷
r_c = 1.0  # 圆周运动半径 (m)
omega = 1.0e6  # 角频率 (rad/s)

# 计算常数因子
const_factor = -q / (4 * np.pi * epsilon_0 * c**2)

# 电荷位置函数
def charge_position(t):
    """计算电荷在时刻t的位置"""
    x = r_c * np.cos(omega * t)
    y = r_c * np.sin(omega * t)
    z = 0.0
    return np.array([x, y, z])

# 电荷加速度函数
def charge_acceleration(t):
    """计算电荷在时刻t的加速度"""
    pos = charge_position(t)
    return -omega**2 * pos

# 引力场计算函数
def gravitational_field(r, t):
    """计算空间点r在时刻t的引力场"""
    # 计算电荷位置
    r_q = charge_position(t)
    
    # 计算距离矢量
    r_rel = r - r_q
    r_mag = np.linalg.norm(r_rel)
    
    # 避免奇点
    if r_mag < 1e-10:
        return np.array([0.0, 0.0, 0.0])
    
    # 计算径向单位矢量
    r_hat = r_rel / r_mag
    
    # 计算电荷加速度
    a = charge_acceleration(t)
    
    # 计算加速度的横向分量
    a_perp = a - np.dot(a, r_hat) * r_hat
    
    # 计算引力场
    A = const_factor * a_perp / r_mag
    
    return A

# 引力场强度计算函数
def field_strength(r, t):
    """计算空间点r在时刻t的引力场强度"""
    A = gravitational_field(r, t)
    return np.linalg.norm(A)

# 绘制引力场矢量图
def plot_field_vector(t, ax, x_range, y_range, step):
    """在指定时间t绘制引力场矢量图"""
    # 创建网格
    x = np.arange(x_range[0], x_range[1], step)
    y = np.arange(y_range[0], y_range[1], step)
    X, Y = np.meshgrid(x, y)
    
    # 计算每个网格点的引力场
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r = np.array([X[i, j], Y[i, j], 0.0])
            A = gravitational_field(r, t)
            U[i, j] = A[0]
            V[i, j] = A[1]
    
    # 计算电荷位置
    r_q = charge_position(t)
    
    # 绘制矢量场
    ax.quiver(X, Y, U, V, scale=1e20, width=0.002, color='blue', alpha=0.7)
    
    # 绘制电荷位置
    ax.plot(r_q[0], r_q[1], 'ro', markersize=8, label='正电荷')
    
    # 绘制电荷运动轨迹
    theta = np.linspace(0, 2*np.pi, 100)
    x_traj = r_c * np.cos(theta)
    y_traj = r_c * np.sin(theta)
    ax.plot(x_traj, y_traj, 'r--', alpha=0.5, label='运动轨迹')
    
    # 设置坐标轴
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(f'圆周运动正电荷引力场矢量图 (t={t:.2e} s)')
    ax.legend()
    ax.grid(True, alpha=0.3)

# 绘制引力场强度分布图
def plot_field_strength(t, ax, x_range, y_range, step):
    """在指定时间t绘制引力场强度分布图"""
    # 创建网格
    x = np.arange(x_range[0], x_range[1], step)
    y = np.arange(y_range[0], y_range[1], step)
    X, Y = np.meshgrid(x, y)
    
    # 计算每个网格点的引力场强度
    Z = np.zeros_like(X)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r = np.array([X[i, j], Y[i, j], 0.0])
            Z[i, j] = field_strength(r, t)
    
    # 绘制强度分布
    im = ax.imshow(Z, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                   origin='lower', cmap=cm.jet, norm=LogNorm(vmin=1e-30, vmax=1e-20))
    
    # 计算电荷位置
    r_q = charge_position(t)
    
    # 绘制电荷位置
    ax.plot(r_q[0], r_q[1], 'ro', markersize=8, label='正电荷')
    
    # 绘制电荷运动轨迹
    theta = np.linspace(0, 2*np.pi, 100)
    x_traj = r_c * np.cos(theta)
    y_traj = r_c * np.sin(theta)
    ax.plot(x_traj, y_traj, 'r--', alpha=0.5, label='运动轨迹')
    
    # 设置坐标轴
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(f'引力场强度分布 (t={t:.2e} s)')
    ax.legend()
    
    return im

# 绘制引力场强度随距离的变化
def plot_strength_vs_distance(t, ax, r_range):
    """绘制引力场强度随距离的变化"""
    # 计算电荷位置
    r_q = charge_position(t)
    
    # 创建距离数组
    r = np.linspace(r_range[0], r_range[1], 100)
    
    # 计算强度
    strength = []
    for d in r:
        # 沿x轴正方向计算
        pos = r_q + np.array([d, 0, 0])
        strength.append(field_strength(pos, t))
    
    # 绘制强度曲线
    ax.plot(r, strength, 'b-', linewidth=2, label='引力场强度')
    
    # 绘制1/r衰减曲线（作为参考）
    ref_strength = np.array(strength[0]) * r[0] / r
    ax.plot(r, ref_strength, 'r--', linewidth=1, label='1/r衰减参考')
    
    # 设置坐标轴
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('距离 (m)')
    ax.set_ylabel('引力场强度 (m/s²)')
    ax.set_title('引力场强度随距离的变化')
    ax.legend()
    ax.grid(True, alpha=0.3)

# 绘制3D引力场强度分布图
def plot_3d_field_strength(t, ax, x_range, y_range, step):
    """绘制3D引力场强度分布图"""
    # 创建网格
    x = np.arange(x_range[0], x_range[1], step)
    y = np.arange(y_range[0], y_range[1], step)
    X, Y = np.meshgrid(x, y)
    
    # 计算每个网格点的引力场强度
    Z = np.zeros_like(X)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            r = np.array([X[i, j], Y[i, j], 0.0])
            Z[i, j] = field_strength(r, t)
    
    # 绘制3D表面图
    surf = ax.plot_surface(X, Y, Z, cmap=cm.jet, norm=LogNorm(vmin=1e-30, vmax=1e-20),
                          alpha=0.8, linewidth=0, antialiased=False)
    
    # 设置坐标轴
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('引力场强度 (m/s²)')
    ax.set_title(f'3D引力场强度分布 (t={t:.2e} s)')
    
    return surf

# 主函数
def main():
    """主函数，创建综合可视化"""
    # 设置时间点
    t = 0.0  # 初始时刻
    
    # 设置空间范围
    x_range = [-3*r_c, 3*r_c]
    y_range = [-3*r_c, 3*r_c]
    step = 0.2  # 网格步长
    r_range = [0.1, 10.0]  # 距离范围
    
    # 创建图形
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('圆周运动正电荷引力场可视化：基于张祥前统一场论', fontsize=16, fontweight='bold')
    
    # 使用gridspec创建布局
    gs = gridspec.GridSpec(2, 2, figure=fig)
    
    # 子图1：引力场矢量图
    ax1 = fig.add_subplot(gs[0, 0])
    plot_field_vector(t, ax1, x_range, y_range, step)
    
    # 子图2：引力场强度分布图
    ax2 = fig.add_subplot(gs[0, 1])
    im = plot_field_strength(t, ax2, x_range, y_range, step)
    fig.colorbar(im, ax=ax2, label='引力场强度 (m/s²)')
    
    # 子图3：引力场强度随距离的变化
    ax3 = fig.add_subplot(gs[1, 0])
    plot_strength_vs_distance(t, ax3, r_range)
    
    # 子图4：3D引力场强度分布图
    ax4 = fig.add_subplot(gs[1, 1], projection='3d')
    surf = plot_3d_field_strength(t, ax4, x_range, y_range, step*2)
    fig.colorbar(surf, ax=ax4, label='引力场强度 (m/s²)', shrink=0.5)
    
    # 调整布局
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # 保存图像
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(current_dir, '圆周运动正电荷引力场可视化.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # 显示图像
    plt.show()

# 创建动画
def create_animation():
    """创建引力场随时间变化的动画"""
    # 设置空间范围
    x_range = [-3*r_c, 3*r_c]
    y_range = [-3*r_c, 3*r_c]
    step = 0.3  # 网格步长
    
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('圆周运动正电荷引力场演化', fontsize=14, fontweight='bold')
    
    # 时间数组
    t_values = np.linspace(0, 2*np.pi/omega, 50)
    
    # 初始化函数
    def init():
        ax1.clear()
        ax2.clear()
        return []
    
    # 更新函数
    def update(frame):
        t = t_values[frame]
        
        # 清除轴
        ax1.clear()
        ax2.clear()
        
        # 绘制矢量场
        plot_field_vector(t, ax1, x_range, y_range, step)
        
        # 绘制强度分布
        im = plot_field_strength(t, ax2, x_range, y_range, step)
        
        return []
    
    # 创建动画
    anim = FuncAnimation(fig, update, frames=len(t_values), init_func=init,
                       blit=True, interval=50)
    
    # 保存动画
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    anim_path = os.path.join(current_dir, '引力场演化动画.gif')
    anim.save(anim_path, writer='pillow', dpi=150)
    
    # 显示动画
    plt.show()

if __name__ == "__main__":
    # 运行主函数
    main()
    
    # 创建动画
    create_animation()
    
    print("可视化完成！")
