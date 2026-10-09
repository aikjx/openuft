import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
宇宙大统一方程（力方程）与空间螺旋运动结合可视化
方程：F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)

此实现特别关注空间螺旋运动中各个力的方向展示
"""

class SpiralForceVisualization:
    """宇宙大统一方程与空间螺旋运动结合可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.base_mass = 1.0  # 基础质量，单位：kg
        self.spiral_radius = 1.0  # 螺旋半径
        self.spiral_pitch = 0.5  # 螺距
        self.angular_velocity = 1.0  # 角速度
        
    def spiral_position(self, t):
        """计算螺旋运动中的位置坐标"""
        x = self.spiral_radius * np.cos(self.angular_velocity * t)
        y = self.spiral_radius * np.sin(self.angular_velocity * t)
        z = self.spiral_pitch * t
        return np.array([x, y, z])
        
    def spiral_velocity(self, t):
        """计算螺旋运动中的速度矢量"""
        vx = -self.spiral_radius * self.angular_velocity * np.sin(self.angular_velocity * t)
        vy = self.spiral_radius * self.angular_velocity * np.cos(self.angular_velocity * t)
        vz = self.spiral_pitch
        return np.array([vx, vy, vz])
        
    def spiral_acceleration(self, t):
        """计算螺旋运动中的加速度矢量"""
        ax = -self.spiral_radius * self.angular_velocity**2 * np.cos(self.angular_velocity * t)
        ay = -self.spiral_radius * self.angular_velocity**2 * np.sin(self.angular_velocity * t)
        az = 0
        return np.array([ax, ay, az])
        
    def calculate_forces(self, t, mass_rate=0.01, C_rate=0.0):
        """计算大统一方程中的各分力，考虑螺旋运动"""
        # 定义质量随时间变化
        m = self.base_mass + mass_rate * t
        
        # 定义物体运动速度矢量V（螺旋运动速度）
        V = self.spiral_velocity(t)
        
        # 定义空间运动速度矢量C（假设沿螺旋轴线的方向，随时间有小变化）
        # 这里我们让C与螺旋运动的切向速度相关联
        tangent_dir = V / np.linalg.norm(V)  # 切向单位向量
        C = self.c * tangent_dir + np.array([0, 0, C_rate * t])
        
        # 计算各分力
        dP_dt1 = C * mass_rate  # C(dm/dt)
        dP_dt2 = -V * mass_rate  # -V(dm/dt)
        dP_dt3 = m * np.array([0, 0, C_rate])  # m(dC/dt)（简化为轴向）
        dP_dt4 = -m * self.spiral_acceleration(t)  # -m(dV/dt)
        
        # 总力
        total_force = dP_dt1 + dP_dt2 + dP_dt3 + dP_dt4
        
        return total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4, V, C, m
        
    def visualize_spiral_trajectory(self):
        """可视化螺旋运动轨迹和力方向"""
        # 生成时间数据
        t = np.linspace(0, 10, 200)  # s
        
        # 计算轨迹点
        positions = np.array([self.spiral_position(time) for time in t])
        
        # 创建3D图形
        fig = plt.figure(figsize=(15, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制螺旋轨迹
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=1.5, alpha=0.7, label='螺旋轨迹')
        
        # 选择几个时间点显示力矢量
        time_points = [2, 5, 8]  # s
        colors = ['r', 'g', 'm']
        
        for i, time in enumerate(time_points):
            # 计算位置
            pos = self.spiral_position(time)
            
            # 计算各力
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4, V, C, m = self.calculate_forces(time)
            
            # 为了可视化，我们需要缩放力矢量
            force_scale = 0.05 / np.max([np.linalg.norm(f) for f in [total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4]])
            velocity_scale = 0.1 / np.linalg.norm(V)
            C_scale = 0.00000001 / np.linalg.norm(C)  # C需要特别小的缩放比例
            
            # 绘制分力矢量
            ax.quiver(pos[0], pos[1], pos[2], dP_dt1[0], dP_dt1[1], dP_dt1[2],
                     color='red', linewidth=1.5, label=f'C(dm/dt) (t={time}s)', arrow_length_ratio=0.3, alpha=0.7)
            ax.quiver(pos[0], pos[1], pos[2], dP_dt2[0], dP_dt2[1], dP_dt2[2],
                     color='green', linewidth=1.5, label=f'-V(dm/dt) (t={time}s)', arrow_length_ratio=0.3, alpha=0.7)
            ax.quiver(pos[0], pos[1], pos[2], dP_dt3[0], dP_dt3[1], dP_dt3[2],
                     color='blue', linewidth=1.5, label=f'm(dC/dt) (t={time}s)', arrow_length_ratio=0.3, alpha=0.7)
            ax.quiver(pos[0], pos[1], pos[2], dP_dt4[0], dP_dt4[1], dP_dt4[2],
                     color='purple', linewidth=1.5, label=f'-m(dV/dt) (t={time}s)', arrow_length_ratio=0.3, alpha=0.7)
            
            # 绘制总力矢量
            ax.quiver(pos[0], pos[1], pos[2], total_force[0], total_force[1], total_force[2],
                     color='black', linewidth=3, label=f'总力F (t={time}s)', arrow_length_ratio=0.3)
            
            # 绘制速度矢量
            ax.quiver(pos[0], pos[1], pos[2], V[0], V[1], V[2],
                     color='orange', linewidth=2, label=f'速度V (t={time}s)', arrow_length_ratio=0.3)
            
            # 绘制C矢量（空间运动速度）
            ax.quiver(pos[0], pos[1], pos[2], C[0], C[1], C[2],
                     color='cyan', linewidth=2, label=f'空间速度C (t={time}s)', arrow_length_ratio=0.3)
            
            # 标记点
            ax.scatter(pos[0], pos[1], pos[2], color=colors[i], s=100, marker='o')
            ax.text(pos[0], pos[1], pos[2], f't={time}s', color=colors[i], fontsize=12)
        
        # 设置坐标轴标签
        ax.set_xlabel('X轴', fontsize=14)
        ax.set_ylabel('Y轴', fontsize=14)
        ax.set_zlabel('Z轴', fontsize=14)
        
        # 设置标题
        ax.set_title('空间螺旋运动中的大统一方程力方向可视化', fontsize=16)
        
        # 添加图例
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        # 添加方程说明
        equation_text = "宇宙大统一方程：F = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)"
        fig.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
        
        return fig
        
    def visualize_force_analysis(self):
        """可视化力的分析，包括螺旋运动中各力分量随时间的变化"""
        # 生成时间数据
        t = np.linspace(0, 10, 100)  # s
        
        # 存储各力数据
        total_forces = []
        dP_dt1_list = []
        dP_dt2_list = []
        dP_dt3_list = []
        dP_dt4_list = []
        
        for time in t:
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4, _, _, _ = self.calculate_forces(time)
            total_forces.append(total_force)
            dP_dt1_list.append(dP_dt1)
            dP_dt2_list.append(dP_dt2)
            dP_dt3_list.append(dP_dt3)
            dP_dt4_list.append(dP_dt4)
        
        # 转换为numpy数组
        total_forces = np.array(total_forces)
        dP_dt1_list = np.array(dP_dt1_list)
        dP_dt2_list = np.array(dP_dt2_list)
        dP_dt3_list = np.array(dP_dt3_list)
        dP_dt4_list = np.array(dP_dt4_list)
        
        # 创建图形
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('空间螺旋运动中的力分量分析', fontsize=16)
        
        # X方向力分量
        axes[0, 0].plot(t, total_forces[:, 0], 'k-', linewidth=2, label='总力X')
        axes[0, 0].plot(t, dP_dt1_list[:, 0], 'r-', linewidth=1, label='C(dm/dt)')
        axes[0, 0].plot(t, dP_dt2_list[:, 0], 'g-', linewidth=1, label='-V(dm/dt)')
        axes[0, 0].plot(t, dP_dt3_list[:, 0], 'b-', linewidth=1, label='m(dC/dt)')
        axes[0, 0].plot(t, dP_dt4_list[:, 0], 'm-', linewidth=1, label='-m(dV/dt)')
        axes[0, 0].set_title('X方向力分量', fontsize=14)
        axes[0, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[0, 0].set_ylabel('力 (N)', fontsize=12)
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Y方向力分量
        axes[0, 1].plot(t, total_forces[:, 1], 'k-', linewidth=2, label='总力Y')
        axes[0, 1].plot(t, dP_dt1_list[:, 1], 'r-', linewidth=1, label='C(dm/dt)')
        axes[0, 1].plot(t, dP_dt2_list[:, 1], 'g-', linewidth=1, label='-V(dm/dt)')
        axes[0, 1].plot(t, dP_dt3_list[:, 1], 'b-', linewidth=1, label='m(dC/dt)')
        axes[0, 1].plot(t, dP_dt4_list[:, 1], 'm-', linewidth=1, label='-m(dV/dt)')
        axes[0, 1].set_title('Y方向力分量', fontsize=14)
        axes[0, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[0, 1].set_ylabel('力 (N)', fontsize=12)
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        
        # Z方向力分量
        axes[1, 0].plot(t, total_forces[:, 2], 'k-', linewidth=2, label='总力Z')
        axes[1, 0].plot(t, dP_dt1_list[:, 2], 'r-', linewidth=1, label='C(dm/dt)')
        axes[1, 0].plot(t, dP_dt2_list[:, 2], 'g-', linewidth=1, label='-V(dm/dt)')
        axes[1, 0].plot(t, dP_dt3_list[:, 2], 'b-', linewidth=1, label='m(dC/dt)')
        axes[1, 0].plot(t, dP_dt4_list[:, 2], 'm-', linewidth=1, label='-m(dV/dt)')
        axes[1, 0].set_title('Z方向力分量', fontsize=14)
        axes[1, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[1, 0].set_ylabel('力 (N)', fontsize=12)
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # 力大小随时间变化
        total_force_magnitudes = np.linalg.norm(total_forces, axis=1)
        dP_dt1_magnitudes = np.linalg.norm(dP_dt1_list, axis=1)
        dP_dt2_magnitudes = np.linalg.norm(dP_dt2_list, axis=1)
        dP_dt3_magnitudes = np.linalg.norm(dP_dt3_list, axis=1)
        dP_dt4_magnitudes = np.linalg.norm(dP_dt4_list, axis=1)
        
        axes[1, 1].plot(t, total_force_magnitudes, 'k-', linewidth=2, label='总力大小')
        axes[1, 1].plot(t, dP_dt1_magnitudes, 'r-', linewidth=1, label='C(dm/dt)')
        axes[1, 1].plot(t, dP_dt2_magnitudes, 'g-', linewidth=1, label='-V(dm/dt)')
        axes[1, 1].plot(t, dP_dt3_magnitudes, 'b-', linewidth=1, label='m(dC/dt)')
        axes[1, 1].plot(t, dP_dt4_magnitudes, 'm-', linewidth=1, label='-m(dV/dt)')
        axes[1, 1].set_title('各力大小随时间变化', fontsize=14)
        axes[1, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[1, 1].set_ylabel('力 (N)', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        # 螺旋运动参数
        positions = np.array([self.spiral_position(time) for time in t])
        velocities = np.array([self.spiral_velocity(time) for time in t])
        accelerations = np.array([self.spiral_acceleration(time) for time in t])
        
        axes[2, 0].plot(t, positions[:, 0], 'r-', label='X位置')
        axes[2, 0].plot(t, positions[:, 1], 'g-', label='Y位置')
        axes[2, 0].plot(t, positions[:, 2], 'b-', label='Z位置')
        axes[2, 0].set_title('螺旋运动位置坐标', fontsize=14)
        axes[2, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 0].set_ylabel('位置', fontsize=12)
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        axes[2, 1].plot(t, np.linalg.norm(velocities, axis=1), 'k-', linewidth=2, label='速度大小')
        axes[2, 1].plot(t, np.linalg.norm(accelerations, axis=1), 'm-', linewidth=2, label='加速度大小')
        axes[2, 1].set_title('速度和加速度大小', fontsize=14)
        axes[2, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 1].set_ylabel('速度/加速度', fontsize=12)
        axes[2, 1].grid(True, alpha=0.3)
        axes[2, 1].legend()
        
        # 调整布局
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        
        return fig
        
    def create_animated_visualization(self):
        """创建空间螺旋运动中力方向的动画可视化"""
        # 创建图形
        fig = plt.figure(figsize=(15, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # 生成完整轨迹
        t_full = np.linspace(0, 10, 200)
        positions_full = np.array([self.spiral_position(time) for time in t_full])
        
        # 绘制完整轨迹
        ax.plot(positions_full[:, 0], positions_full[:, 1], positions_full[:, 2], 'b-', linewidth=1, alpha=0.3)
        
        # 初始化物体点
        point, = ax.plot([], [], [], 'ro', markersize=10)
        
        # 初始化力矢量
        force_arrows = []
        labels = ['总力F', 'C(dm/dt)', '-V(dm/dt)', 'm(dC/dt)', '-m(dV/dt)', '速度V', '空间速度C']
        colors = ['black', 'red', 'green', 'blue', 'purple', 'orange', 'cyan']
        
        # 创建箭头对象并添加到图例
        for color, label in zip(colors, labels):
            # 创建占位箭头用于图例
            arrow = ax.quiver([], [], [], [], [], [], color=color, linewidth=2, label=label)
            force_arrows.append(arrow)
        
        # 设置坐标轴范围
        max_range = np.max([np.max(positions_full[:, 0]), np.max(positions_full[:, 1]), np.max(positions_full[:, 2])])
        ax.set_xlim([-max_range*1.5, max_range*1.5])
        ax.set_ylim([-max_range*1.5, max_range*1.5])
        ax.set_zlim([-max_range*0.5, max_range*1.5])
        
        # 设置标签和标题
        ax.set_xlabel('X轴')
        ax.set_ylabel('Y轴')
        ax.set_zlabel('Z轴')
        ax.set_title('空间螺旋运动中力方向的动态可视化')
        
        # 添加图例
        ax.legend(loc='upper right')
        
        # 添加方程说明
        equation_text = "宇宙大统一方程：F = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)"
        fig.text(0.5, 0.01, equation_text, ha='center', fontsize=12, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
        
        def update(frame):
    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
                """更新动画帧"""
            # 计算当前时间
            t = frame * 0.1
            
            # 计算位置和各力
            pos = self.spiral_position(t)
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4, V, C, m = self.calculate_forces(t)
            
            # 更新物体点位置
            point.set_data([pos[0]], [pos[1]])
            point.set_3d_properties([pos[2]])
            
            # 为了可视化，缩放力矢量
            force_scale = 0.05 / np.max([np.linalg.norm(f) for f in [total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4]])
            velocity_scale = 0.1 / np.linalg.norm(V)
            C_scale = 0.00000001 / np.linalg.norm(C)  # C需要特别小的缩放比例
            
            # 更新各力矢量
            all_forces = [total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4, V, C]
            scales = [force_scale, force_scale, force_scale, force_scale, force_scale, velocity_scale, C_scale]
            
            for i, (force, scale, arrow) in enumerate(zip(all_forces, scales, force_arrows)):
                # 更新箭头数据
                arrow.set_segments([[[pos[0], pos[1], pos[2]], 
                                    [pos[0] + force[0]*scale, pos[1] + force[1]*scale, pos[2] + force[2]*scale]]])
            
            # 更新标题显示当前时间
            ax.set_title(f'空间螺旋运动中力方向的动态可视化 (t={t:.1f}s)')
            
            return (point,) + tuple(force_arrows)
        
        # 创建动画
        ani = FuncAnimation(fig, update, frames=100, interval=200, blit=True)
        
        return fig, ani

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建空间螺旋运动与大统一方程结合的可视化对象
    spiral_vis = SpiralForceVisualization()
    
    # 显示螺旋轨迹和力方向可视化
    fig_spiral = spiral_vis.visualize_spiral_trajectory()
    
    # 显示力分量分析可视化
    fig_analysis = spiral_vis.visualize_force_analysis()
    
    # 创建动画可视化
    fig_animation, ani = spiral_vis.create_animated_visualization()
    
    # 保存图形为PNG文件
    fig_spiral.savefig('./img/三维螺旋时空方程可视化.png', dpi=300, bbox_inches='tight')
    fig_analysis.savefig('./img/螺旋运动力分量分析.png', dpi=300, bbox_inches='tight')
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")