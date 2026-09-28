import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import os
from scipy import ndimage

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置字体大小
plt.rcParams['font.size'] = 10
# 设置线条宽度
plt.rcParams['lines.linewidth'] = 1.5
# 设置图形分辨率
plt.rcParams['figure.dpi'] = 100

class GravitationalFieldSimulator:
    """圆周运动正电荷引力场模拟器"""
    
    def __init__(self, q=1.602176634e-19, r_c=1.0, omega=1.0e6):
        """
        初始化模拟器
        
        参数:
        q: 电荷量 (C)
        r_c: 圆周运动半径 (m)
        omega: 角频率 (rad/s)
        """
        # 物理常数
        self.c = 2.99792458e8  # 光速 (m/s)
        self.epsilon_0 = 8.8541878128e-12  # 真空介电常数 (F/m)
        
        # 模拟参数
        self.q = q  # 电荷量
        self.r_c = r_c  # 圆周运动半径
        self.omega = omega  # 角频率
        
        # 计算常数因子
        self.const_factor = -q / (4 * np.pi * self.epsilon_0 * self.c**2)
    
    def charge_position(self, t):
        """计算电荷在时刻t的位置"""
        x = self.r_c * np.cos(self.omega * t)
        y = self.r_c * np.sin(self.omega * t)
        z = 0.0
        return np.array([x, y, z])
    
    def charge_velocity(self, t):
        """计算电荷在时刻t的速度"""
        vx = -self.r_c * self.omega * np.sin(self.omega * t)
        vy = self.r_c * self.omega * np.cos(self.omega * t)
        vz = 0.0
        return np.array([vx, vy, vz])
    
    def charge_acceleration(self, t):
        """计算电荷在时刻t的加速度"""
        pos = self.charge_position(t)
        return -self.omega**2 * pos
    
    def gravitational_field(self, r, t):
        """计算空间点r在时刻t的引力场"""
        # 求解推迟时间 t_r = t - R/c，其中 R 是电荷到场点的距离
        # 使用迭代法求解推迟时间
        t_r = t  # 初始猜测
        max_iterations = 100
        tolerance = 1e-12
        
        for i in range(max_iterations):
            # 计算电荷在猜测推迟时间的位置
            r_q = self.charge_position(t_r)
            # 计算距离
            r_rel = r - r_q
            r_mag = np.linalg.norm(r_rel)
            # 计算新的推迟时间
            new_t_r = t - r_mag / self.c
            # 检查收敛
            if abs(new_t_r - t_r) < tolerance:
                t_r = new_t_r
                break
            t_r = new_t_r
        
        # 计算电荷在推迟时间的位置
        r_q = self.charge_position(t_r)
        
        # 计算距离矢量
        r_rel = r - r_q
        r_mag = np.linalg.norm(r_rel)
        
        # 避免奇点
        if r_mag < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # 计算径向单位矢量
        r_hat = r_rel / r_mag
        
        # 计算电荷在推迟时间的加速度
        a = self.charge_acceleration(t_r)
        
        # 计算加速度的横向分量
        a_perp = a - np.dot(a, r_hat) * r_hat
        
        # 计算引力场
        A = self.const_factor * a_perp / r_mag
        
        return A
    
    def field_strength(self, r, t):
        """计算空间点r在时刻t的引力场强度"""
        A = self.gravitational_field(r, t)
        return np.linalg.norm(A)
    
    def electric_field(self, r, t):
        """计算空间点r在时刻t的电场"""
        # 计算电荷位置
        r_q = self.charge_position(t)
        
        # 计算距离矢量
        r_rel = r - r_q
        r_mag = np.linalg.norm(r_rel)
        
        # 避免奇点
        if r_mag < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # 计算电场（库仑场）
        const_e = 1.0 / (4 * np.pi * self.epsilon_0)
        E = const_e * self.q * r_rel / r_mag**3
        
        return E
    
    def magnetic_field(self, r, t):
        """计算空间点r在时刻t的磁场"""
        # 计算电荷位置和速度
        r_q = self.charge_position(t)
        v = self.charge_velocity(t)
        
        # 计算距离矢量
        r_rel = r - r_q
        r_mag = np.linalg.norm(r_rel)
        
        # 避免奇点
        if r_mag < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # 计算磁场（毕奥-萨伐尔定律）
        const_b = 1.0 / (4 * np.pi * self.epsilon_0 * self.c**2)
        B = const_b * self.q * np.cross(v, r_rel) / r_mag**3
        
        return B
    
    def energy_density(self, r, t):
        """计算空间点r在时刻t的能量密度"""
        # 计算电场和磁场
        E = self.electric_field(r, t)
        B = self.magnetic_field(r, t)
        
        # 计算能量密度
        epsilon_0 = self.epsilon_0
        mu_0 = 1.0 / (epsilon_0 * self.c**2)
        energy = 0.5 * (epsilon_0 * np.dot(E, E) + mu_0 * np.dot(B, B))
        
        return energy

class Visualizer:
    """引力场可视化工具"""
    
    def __init__(self, simulator):
        """初始化可视化工具"""
        self.simulator = simulator
    
    def plot_field_vector(self, t, ax, x_range, y_range, step):
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
                A = self.simulator.gravitational_field(r, t)
                U[i, j] = A[0]
                V[i, j] = A[1]
        
        # 计算电荷位置
        r_q = self.simulator.charge_position(t)
        
        # 绘制矢量场
        # 计算矢量长度用于颜色映射
        mag = np.sqrt(U**2 + V**2)
        # 归一化矢量用于显示
        U_norm = U / (mag + 1e-30)
        V_norm = V / (mag + 1e-30)
        
        # 使用长度作为颜色
        ax.quiver(X, Y, U_norm, V_norm, mag, scale=20, width=0.002, cmap=cm.viridis, alpha=0.7)
        
        # 绘制电荷位置
        ax.plot(r_q[0], r_q[1], 'ro', markersize=8, label='正电荷')
        
        # 绘制电荷运动轨迹
        theta = np.linspace(0, 2*np.pi, 100)
        x_traj = self.simulator.r_c * np.cos(theta)
        y_traj = self.simulator.r_c * np.sin(theta)
        ax.plot(x_traj, y_traj, 'r--', alpha=0.5, label='运动轨迹')
        
        # 设置坐标轴
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'圆周运动正电荷引力场矢量图 (t={t:.2e} s)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_field_strength(self, t, ax, x_range, y_range, step):
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
                Z[i, j] = self.simulator.field_strength(r, t)
        
        # 处理零值和负值
        Z = np.maximum(Z, 1e-35)
        
        # 绘制强度分布
        im = ax.imshow(Z, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                       origin='lower', cmap=cm.plasma, norm=LogNorm(vmin=np.min(Z), vmax=np.max(Z)))
        
        # 计算电荷位置
        r_q = self.simulator.charge_position(t)
        
        # 绘制电荷位置
        ax.plot(r_q[0], r_q[1], 'ro', markersize=8, label='正电荷')
        
        # 绘制电荷运动轨迹
        theta = np.linspace(0, 2*np.pi, 100)
        x_traj = self.simulator.r_c * np.cos(theta)
        y_traj = self.simulator.r_c * np.sin(theta)
        ax.plot(x_traj, y_traj, 'r--', alpha=0.5, label='运动轨迹')
        
        # 设置坐标轴
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'引力场强度分布 (t={t:.2e} s)')
        ax.legend()
        
        return im
    
    def plot_strength_vs_distance(self, t, ax, r_range):
        """绘制引力场强度随距离的变化"""
        # 计算电荷位置
        r_q = self.simulator.charge_position(t)
        
        # 创建距离数组
        r = np.linspace(r_range[0], r_range[1], 100)
        
        # 计算强度
        strength = []
        for d in r:
            # 沿x轴正方向计算
            pos = r_q + np.array([d, 0, 0])
            strength.append(self.simulator.field_strength(pos, t))
        
        # 处理零值和负值
        strength = np.maximum(strength, 1e-35)
        
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
    
    def plot_3d_field_strength(self, t, ax, x_range, y_range, step):
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
                Z[i, j] = self.simulator.field_strength(r, t)
        
        # 处理零值和负值
        Z = np.maximum(Z, 1e-35)
        
        # 绘制3D表面图
        surf = ax.plot_surface(X, Y, Z, cmap=cm.plasma, norm=LogNorm(vmin=np.min(Z), vmax=np.max(Z)),
                              alpha=0.8, linewidth=0, antialiased=False)
        
        # 设置坐标轴
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_zlabel('引力场强度 (m/s²)')
        ax.set_title(f'3D引力场强度分布 (t={t:.2e} s)')
        
        return surf
    
    def plot_energy_density(self, t, ax, x_range, y_range, step):
        """绘制能量密度分布"""
        # 创建网格
        x = np.arange(x_range[0], x_range[1], step)
        y = np.arange(y_range[0], y_range[1], step)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个网格点的能量密度
        Z = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                r = np.array([X[i, j], Y[i, j], 0.0])
                Z[i, j] = self.simulator.energy_density(r, t)
        
        # 处理零值和负值
        Z = np.maximum(Z, 1e-35)
        
        # 绘制能量密度分布
        im = ax.imshow(Z, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                       origin='lower', cmap=cm.inferno, norm=LogNorm(vmin=np.min(Z), vmax=np.max(Z)))
        
        # 计算电荷位置
        r_q = self.simulator.charge_position(t)
        
        # 绘制电荷位置
        ax.plot(r_q[0], r_q[1], 'ro', markersize=8, label='正电荷')
        
        # 绘制电荷运动轨迹
        theta = np.linspace(0, 2*np.pi, 100)
        x_traj = self.simulator.r_c * np.cos(theta)
        y_traj = self.simulator.r_c * np.sin(theta)
        ax.plot(x_traj, y_traj, 'r--', alpha=0.5, label='运动轨迹')
        
        # 设置坐标轴
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'能量密度分布 (t={t:.2e} s)')
        ax.legend()
        
        return im
    
    def create_comprehensive_plot(self, t=0.0):
        """创建综合可视化"""
        # 设置空间范围
        x_range = [-3*self.simulator.r_c, 3*self.simulator.r_c]
        y_range = [-3*self.simulator.r_c, 3*self.simulator.r_c]
        step = 0.2  # 网格步长
        r_range = [0.1, 10.0]  # 距离范围
        
        # 创建图形
        fig = plt.figure(figsize=(18, 14))
        fig.suptitle('圆周运动正电荷引力场可视化：基于张祥前统一场论', fontsize=16, fontweight='bold')
        
        # 使用gridspec创建布局
        gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 1])
        
        # 子图1：引力场矢量图
        ax1 = fig.add_subplot(gs[0, 0])
        self.plot_field_vector(t, ax1, x_range, y_range, step)
        
        # 子图2：引力场强度分布图
        ax2 = fig.add_subplot(gs[0, 1])
        im = self.plot_field_strength(t, ax2, x_range, y_range, step)
        fig.colorbar(im, ax=ax2, label='引力场强度 (m/s²)')
        
        # 子图3：引力场强度随距离的变化
        ax3 = fig.add_subplot(gs[1, 0])
        self.plot_strength_vs_distance(t, ax3, r_range)
        
        # 子图4：3D引力场强度分布图
        ax4 = fig.add_subplot(gs[1, 1], projection='3d')
        surf = self.plot_3d_field_strength(t, ax4, x_range, y_range, step*2)
        fig.colorbar(surf, ax=ax4, label='引力场强度 (m/s²)', shrink=0.5)
        
        # 子图5：能量密度分布
        ax5 = fig.add_subplot(gs[2, :])
        im_energy = self.plot_energy_density(t, ax5, x_range, y_range, step)
        fig.colorbar(im_energy, ax=ax5, label='能量密度 (J/m³)')
        
        # 调整布局
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # 保存图像
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(current_dir, '圆周运动正电荷引力场可视化_优化版.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # 显示图像
        plt.show()
    
    def create_animation(self):
        """创建引力场随时间变化的动画"""
        # 设置空间范围
        x_range = [-3*self.simulator.r_c, 3*self.simulator.r_c]
        y_range = [-3*self.simulator.r_c, 3*self.simulator.r_c]
        step = 0.3  # 网格步长
        
        # 创建图形
        fig = plt.figure(figsize=(18, 12))
        fig.suptitle('圆周运动正电荷引力场演化', fontsize=14, fontweight='bold')
        
        # 使用gridspec创建布局
        gs = gridspec.GridSpec(2, 2, figure=fig)
        
        # 创建子图
        ax1 = fig.add_subplot(gs[0, 0])  # 引力场矢量图
        ax2 = fig.add_subplot(gs[0, 1])  # 引力场强度分布图
        ax3 = fig.add_subplot(gs[1, 0])  # 能量密度分布
        ax4 = fig.add_subplot(gs[1, 1], projection='3d')  # 3D引力场强度分布
        
        # 时间数组
        t_values = np.linspace(0, 2*np.pi/self.simulator.omega, 60)
        
        # 初始化函数
        def init():
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            return []
        
        # 更新函数
        def update(frame):
            t = t_values[frame]
            
            # 清除轴
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            
            # 绘制矢量场
            self.plot_field_vector(t, ax1, x_range, y_range, step)
            
            # 绘制强度分布
            im = self.plot_field_strength(t, ax2, x_range, y_range, step)
            
            # 绘制能量密度分布
            im_energy = self.plot_energy_density(t, ax3, x_range, y_range, step)
            
            # 绘制3D强度分布
            surf = self.plot_3d_field_strength(t, ax4, x_range, y_range, step*2)
            
            return []
        
        # 创建动画
        anim = FuncAnimation(fig, update, frames=len(t_values), init_func=init,
                           blit=True, interval=50)
        
        # 保存动画
        current_dir = os.path.dirname(os.path.abspath(__file__))
        anim_path = os.path.join(current_dir, '引力场演化动画_优化版.gif')
        anim.save(anim_path, writer='pillow', dpi=150)
        
        # 显示动画
        plt.show()

if __name__ == "__main__":
    # 创建模拟器
    simulator = GravitationalFieldSimulator(
        q=1.602176634e-19,  # 电荷量
        r_c=1.0,           # 圆周运动半径
        omega=1.0e6        # 角频率
    )
    
    # 创建可视化工具
    visualizer = Visualizer(simulator)
    
    # 创建综合可视化
    visualizer.create_comprehensive_plot(t=0.0)
    
    # 创建动画
    visualizer.create_animation()
    
    print("可视化完成！")
