import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

# 设置中文字体 - Windows系统通用字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
plt.rcParams["text.usetex"] = False  # 使用 Matplotlib 的内置渲染
plt.rcParams["mathtext.fontset"] = "cm"  # 使用 CMU Serif 字体渲染数学公式

class SpaceTimeUnificationVisualizer:
    def __init__(self):
        # 主方程参数
        self.C = np.array([1, 0.8, 0.6])  # 速度矢量
        self.t_max = 2.0  # 最大时间
        self.t_steps = 50  # 时间步数
        
    def plot_static_3d(self):
        """绘制静态的3D时空轨迹图"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 生成时间和轨迹数据
        t = np.linspace(0, self.t_max, self.t_steps)
        x = self.C[0] * t
        y = self.C[1] * t
        z = self.C[2] * t
        
        # 绘制3D轨迹
        ax.plot(x, y, z, 'b-', linewidth=3, label='时空轨迹')
        
        # 绘制起点
        ax.scatter([0], [0], [0], color='r', s=150, zorder=5, label='原点')
        
        # 绘制终点
        ax.scatter([x[-1]], [y[-1]], [z[-1]], color='g', s=150, zorder=5, label='终点')
        
        # 绘制速度矢量
        ax.quiver(0, 0, 0, self.C[0], self.C[1], self.C[2], color='m', arrow_length_ratio=0.1, 
                  linewidth=3, label=r'速度矢量 $\vec{C}$')
        
        # 添加粒子动画效果
        particles = min(10, len(t))
        particle_indices = np.linspace(0, len(t)-1, particles, dtype=int)
        for i in particle_indices:
            ax.scatter([x[i]], [y[i]], [z[i]], color='orange', s=60, alpha=0.7)
        
        # 设置坐标轴范围和标签
        max_range = max(np.max(x), np.max(y), np.max(z)) * 1.3
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        ax.set_xlabel('X 坐标', fontsize=14, labelpad=10)
        ax.set_ylabel('Y 坐标', fontsize=14, labelpad=10)
        ax.set_zlabel('Z 坐标', fontsize=14, labelpad=10)
        
        # 设置标题
        plt.title('时空同一化方程的3D可视化\nUnified Field Theory: Spacetime Unification', 
                  fontsize=18, pad=30, fontweight='bold')
        
        # 添加方程说明
        equation_text = r'$\vec{r}(t) = \vec{C}t = x\vec{i} + y\vec{j} + z\vec{k}$'
        plt.figtext(0.5, 0.02, equation_text, ha='center', fontsize=16, fontweight='bold')
        
        # 添加图例
        ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
        
        # 设置视角
        ax.view_init(elev=20, azim=45)
        
        # 设置背景
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('w')
        ax.yaxis.pane.set_edgecolor('w')
        ax.zaxis.pane.set_edgecolor('w')
        ax.xaxis.pane.set_alpha(0.1)
        ax.yaxis.pane.set_alpha(0.1)
        ax.zaxis.pane.set_alpha(0.1)
        
        plt.tight_layout()
        return fig
    
    def plot_components(self):
        """绘制各分量随时间变化的曲线图"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('时空同一化方程分量分析\nComponent Analysis of Spacetime Unification Equation', 
                     fontsize=18, fontweight='bold', y=1.02)
        
        # 生成时间数据
        t = np.linspace(0, self.t_max, self.t_steps)
        
        # 计算各分量
        x = self.C[0] * t
        y = self.C[1] * t
        z = self.C[2] * t
        
        # 绘制x分量
        axes[0].plot(t, x, 'r-', linewidth=3, marker='o', markersize=4)
        axes[0].set_title('X分量: x(t) = C_x * t', fontsize=15, pad=15)
        axes[0].set_xlabel('时间 t', fontsize=13)
        axes[0].set_ylabel('x 坐标', fontsize=13)
        axes[0].grid(True, linestyle='--', alpha=0.7)
        axes[0].tick_params(axis='both', which='major', labelsize=11)
        
        # 绘制y分量
        axes[1].plot(t, y, 'g-', linewidth=3, marker='s', markersize=4)
        axes[1].set_title('Y分量: y(t) = C_y * t', fontsize=15, pad=15)
        axes[1].set_xlabel('时间 t', fontsize=13)
        axes[1].set_ylabel('y 坐标', fontsize=13)
        axes[1].grid(True, linestyle='--', alpha=0.7)
        axes[1].tick_params(axis='both', which='major', labelsize=11)
        
        # 绘制z分量
        axes[2].plot(t, z, 'b-', linewidth=3, marker='^', markersize=4)
        axes[2].set_title('Z分量: z(t) = C_z * t', fontsize=15, pad=15)
        axes[2].set_xlabel('时间 t', fontsize=13)
        axes[2].set_ylabel('z 坐标', fontsize=13)
        axes[2].grid(True, linestyle='--', alpha=0.7)
        axes[2].tick_params(axis='both', which='major', labelsize=11)
        
        plt.tight_layout()
        return fig
    
    def animate_3d(self):
        """创建3D动画展示时空轨迹"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 生成时间和轨迹数据
        t = np.linspace(0, self.t_max, self.t_steps)
        x = self.C[0] * t
        y = self.C[1] * t
        z = self.C[2] * t
        
        # 设置坐标轴范围
        max_range = max(np.max(x), np.max(y), np.max(z)) * 1.3
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        # 设置坐标轴标签和标题
        ax.set_xlabel('X 坐标', fontsize=14, labelpad=10)
        ax.set_ylabel('Y 坐标', fontsize=14, labelpad=10)
        ax.set_zlabel('Z 坐标', fontsize=14, labelpad=10)
        ax.set_title('时空同一化方程的动态可视化\nDynamic Visualization of Spacetime Unification', 
                     fontsize=18, pad=30, fontweight='bold')
        
        # 添加方程说明
        equation_text = r'$\vec{r}(t) = \vec{C}t = x\vec{i} + y\vec{j} + z\vec{k}$'
        fig.text(0.5, 0.02, equation_text, ha='center', fontsize=16, fontweight='bold')
        
        # 初始化轨迹线和移动点
        trajectory_line, = ax.plot([], [], [], 'b-', linewidth=2, alpha=0.7)
        moving_point, = ax.plot([], [], [], 'ro', markersize=12)
        time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, fontsize=14, 
                              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 添加图例
        legend_elements = [mpatches.Patch(color='blue', label='时空轨迹'),
                          mpatches.Patch(color='red', label='运动质点')]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
        
        # 设置背景
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # 初始化函数
        def init():
            trajectory_line.set_data([], [])
            trajectory_line.set_3d_properties([])
            moving_point.set_data([], [])
            moving_point.set_3d_properties([])
            time_text.set_text('')
            return trajectory_line, moving_point, time_text
        
        # 更新函数
        def update(frame):
            # 更新轨迹线
            trajectory_line.set_data(x[:frame+1], y[:frame+1])
            trajectory_line.set_3d_properties(z[:frame+1])
            
            # 更新移动点
            moving_point.set_data([x[frame]], [y[frame]])
            moving_point.set_3d_properties([z[frame]])
            
            # 更新时间文本
            time_text.set_text(f'时间 t = {t[frame]:.2f}')
            
            return trajectory_line, moving_point, time_text
        
        # 创建动画
        ani = FuncAnimation(
            fig, update, frames=self.t_steps,
            init_func=init, interval=100, blit=True
        )
        
        return fig, ani
    
    def show_all(self):
        """显示所有可视化图表"""
        # 静态3D图
        fig1 = self.plot_static_3d()
        
        # 分量曲线图
        fig2 = self.plot_components()
        
        # 显示图表
        plt.show()

# 主程序
if __name__ == "__main__":
    # 创建可视化器实例
    visualizer = SpaceTimeUnificationVisualizer()
    
    # 显示所有可视化图表
    visualizer.show_all()
    
    # 如果需要保存动画，可以取消下面的注释
    # fig, ani = visualizer.animate_3d()
    # ani.save('space_time_unification.gif', writer='pillow', fps=10)
    # plt.close(fig)