import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# ===================== 第一部分：欧拉公式可视化（复平面2D动画） =====================
def visualize_euler_formula():
    """
    可视化欧拉公式 e^(it) = cos(t) + i*sin(t)
    展示复平面上单位圆的旋转，实时显示实部(cos t)、虚部(sin t)和复指数的关系
    """
    # 创建画布和坐标轴
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.grid(True)
    ax1.set_title('欧拉公式可视化: $e^{it} = \\cos(t) + i\\sin(t)$', fontsize=14)
    ax1.set_xlabel('实部 (Re)')
    ax1.set_ylabel('虚部 (Im)')

    # 绘制单位圆
    theta_circle = np.linspace(0, 2*np.pi, 100)
    ax1.plot(np.cos(theta_circle), np.sin(theta_circle), 'gray', linestyle='--', alpha=0.5, label='单位圆')

    # 初始化绘制元素
    # 复指数点（红色）、实部投影线（蓝色）、虚部投影线（绿色）、旋转半径（黑色）
    point, = ax1.plot([], [], 'ro', markersize=8, label='$e^{it}$')
    real_line, = ax1.plot([], [], 'b-', alpha=0.7, label='Re($e^{it}$) = cos(t)')
    imag_line, = ax1.plot([], [], 'g-', alpha=0.7, label='Im($e^{it}$) = sin(t)')
    radius, = ax1.plot([], [], 'k-', alpha=0.5)

    # 动画更新函数
    def update_euler(frame):
        t = frame * 0.05  # 时间参数，控制旋转速度
        # 计算复指数的实部和虚部
        re = np.cos(t)
        im = np.sin(t)
        
        # 更新元素位置
        point.set_data([re], [im])
        real_line.set_data([0, re], [0, 0])  # 实轴投影
        imag_line.set_data([re, re], [0, im])  # 虚轴投影
        radius.set_data([0, re], [0, im])      # 旋转半径
        
        # 显示当前t值和对应的值
        ax1.set_title(f'欧拉公式可视化: $e^{{i{t:.2f}}} = \cos({t:.2f}) + i\sin({t:.2f}) = {re:.2f} + i{im:.2f}$', fontsize=14)
        return point, real_line, imag_line, radius

    # 创建动画
    ani1 = animation.FuncAnimation(
        fig1, update_euler, frames=250, interval=30, blit=True, repeat=True
    )
    ax1.legend(loc='upper right')
    return fig1, ani1

# ===================== 第二部分：张祥前空间螺旋运动公式可视化（3D轨迹） =====================
def visualize_ZUFT_spiral():
    """
    可视化张祥前空间螺旋运动公式：
    $\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ct \cdot \vec{k}$
    展示三维空间中的螺旋轨迹，体现圆周运动+光速直线运动的合成
    """
    # 定义核心参数（归一化处理，方便可视化）
    r = 0.2    # 螺旋半径
    omega = 2 * np.pi  # 角速度（1秒转1圈）
    c = 1      # 光速（归一化值，实际为3e8 m/s，这里简化为1）
    t = np.linspace(0, 5, 500)  # 时间范围

    # 计算螺旋轨迹坐标
    x = r * np.cos(omega * t)  # xy平面圆周运动x分量
    y = r * np.sin(omega * t)  # xy平面圆周运动y分量
    z = c * t                  # z轴光速直线运动分量

    # 创建3D画布
    fig2 = plt.figure(figsize=(10, 8))
    ax2 = fig2.add_subplot(111, projection='3d')

    # 绘制螺旋轨迹
    ax2.plot(x, y, z, 'purple', linewidth=2, label='空间螺旋运动轨迹')
    # 绘制z轴参考线（光速直线运动）
    ax2.plot([0]*len(t), [0]*len(t), z, 'gray', linestyle='--', alpha=0.5, label='z轴光速直线运动')
    # 绘制xy平面投影（圆周运动）
    ax2.plot(x, y, [0]*len(t), 'orange', linestyle=':', alpha=0.5, label='xy平面圆周运动投影')

    # 设置坐标轴标签和标题
    ax2.set_xlabel('X 轴')
    ax2.set_ylabel('Y 轴')
    ax2.set_zlabel('Z 轴 (光速方向)')
    ax2.set_title('张祥前空间螺旋运动公式可视化\n' + r'$\vec{r}(t) = r\cos\omega t \cdot \vec{i} + r\sin\omega t \cdot \vec{j} + ct \cdot \vec{k}$', fontsize=12)
    ax2.legend()
    ax2.grid(True)

    # 可选：添加动画展示点的运动过程
    # 初始化点
    point3d, = ax2.plot([], [], [], 'ro', markersize=8)
    def update_spiral(frame):
        idx = frame % len(t)
        point3d.set_data([x[idx]], [y[idx]])
        point3d.set_3d_properties([z[idx]])
        return point3d,

    ani2 = animation.FuncAnimation(
        fig2, update_spiral, frames=len(t), interval=20, blit=True, repeat=True
    )
    return fig2, ani2

# ===================== 运行可视化 =====================
if __name__ == '__main__':
    # 启动欧拉公式可视化（2D动画）
    fig1, ani1 = visualize_euler_formula()
    # 启动ZUFT螺旋运动可视化（3D轨迹+动画）
    fig2, ani2 = visualize_ZUFT_spiral()
    
    # 显示所有图形
    plt.show()