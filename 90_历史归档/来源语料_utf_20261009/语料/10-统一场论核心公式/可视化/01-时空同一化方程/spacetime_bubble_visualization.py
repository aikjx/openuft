import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题

class SpaceTimeBubbleVisualizer:
    def __init__(self):
        # 主方程参数
        self.C = np.array([1, 1, 1])  # 光速在各方向的分量
        self.t_max = 2.0  # 最大时间
        self.t_steps = 50  # 时间步数
        self.bubble_color = 'deepskyblue'  # 各向发散运动颜色
        self.bubble_alpha = 0.3  # 各向发散运动透明度
        
    def plot_static_bubble(self):
        """绘制静态的时空各向发散运动图"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 生成时间和轨迹数据
        t = np.linspace(0, self.t_max, self.t_steps)
        
        # 绘制多个不同时间点的各向发散运动
        num_bubbles = 5  # 显示的各向发散运动数量
        time_points = np.linspace(0, self.t_max, num_bubbles)
        
        for i, bubble_time in enumerate(time_points):
            # 计算各向发散运动半径
            radius = np.linalg.norm(self.C) * bubble_time
            
            # 计算透明度随时间变化
            current_alpha = self.bubble_alpha * (i + 1) / num_bubbles
            
            # 创建球面数据
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x = radius * np.outer(np.cos(u), np.sin(v))
            y = radius * np.outer(np.sin(u), np.sin(v))
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            # 绘制球面
            surf = ax.plot_surface(x, y, z, color=self.bubble_color, alpha=current_alpha, linewidth=0.5, edgecolor='white', shade=True)
            
            # 在球面上添加光效点
            if i == num_bubbles - 1:  # 只在最大的各向发散运动上添加
                num_points = 20
                theta = np.random.rand(num_points) * 2 * np.pi
                phi = np.random.rand(num_points) * np.pi
                point_x = radius * np.cos(theta) * np.sin(phi)
                point_y = radius * np.sin(theta) * np.sin(phi)
                point_z = radius * np.cos(phi)
                ax.scatter(point_x, point_y, point_z, color='white', s=20, alpha=0.8)
        
        # 绘制时间箭头，显示膨胀方向
        end_radius = np.linalg.norm(self.C) * self.t_max
        ax.quiver(0, 0, 0, end_radius, end_radius, end_radius, color='red', arrow_length_ratio=0.1, 
                  linewidth=2, label=r'时间演化方向')
        
        # 设置坐标轴范围和标签
        max_range = end_radius * 1.2
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        ax.set_xlabel('X 坐标', fontsize=12)
        ax.set_ylabel('Y 坐标', fontsize=12)
        ax.set_zlabel('Z 坐标', fontsize=12)
        
        # 设置标题
        plt.title('时空同一化方程的各向发散运动膨胀可视化', fontsize=16, pad=20)
        
        # 添加方程说明
        equation_text = r'$r(t) = |\vec{{C}}|t$，其中 $\vec{{C}}$ 为光速矢量'
        plt.figtext(0.5, 0.02, equation_text, ha='center', fontsize=14)
        
        # 添加图例
        ax.legend(loc='upper right', fontsize=10)
        
        # 设置视角
        ax.view_init(elev=30, azim=45)
        
        plt.tight_layout()
        return fig
    
    def animate_bubble(self):
        """创建动态各向发散运动膨胀动画"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 生成时间数据
        t = np.linspace(0, self.t_max, self.t_steps)
        
        # 计算最大各向发散运动半径
        max_radius = np.linalg.norm(self.C) * self.t_max
        
        # 设置坐标轴范围
        ax.set_xlim([-max_radius * 1.2, max_radius * 1.2])
        ax.set_ylim([-max_radius * 1.2, max_radius * 1.2])
        ax.set_zlim([-max_radius * 1.2, max_radius * 1.2])
        
        # 设置坐标轴标签和标题
        ax.set_xlabel('X 坐标', fontsize=12)
        ax.set_ylabel('Y 坐标', fontsize=12)
        ax.set_zlabel('Z 坐标', fontsize=12)
        plt.title('时空各向发散运动动态膨胀可视化', fontsize=16, pad=20)
        
        # 添加方程说明
        equation_text = r'$r(t) = |\vec{{C}}|t$，其中 $\vec{{C}}$ 为光速矢量'
        plt.figtext(0.5, 0.02, equation_text, ha='center', fontsize=14)
        
        # 初始化球面和时间文本
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        initial_radius = 0.01  # 初始半径
        x = initial_radius * np.outer(np.cos(u), np.sin(v))
        y = initial_radius * np.outer(np.sin(u), np.sin(v))
        z = initial_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        surf = ax.plot_surface(x, y, z, color=self.bubble_color, alpha=self.bubble_alpha, linewidth=0.5, edgecolor='white')
        time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, fontsize=12)
        radius_text = ax.text2D(0.05, 0.90, '', transform=ax.transAxes, fontsize=12)
        
        # 初始化函数
        def init():
            # 重置球面为最小状态
            surf._vec._facecolors3d = np.array([self.bubble_color] * x.shape[0] * x.shape[1])
            surf._vec._edgecolors3d = np.array(['white'] * x.shape[0] * x.shape[1])
            surf._vec._alpha3d = np.array([self.bubble_alpha] * x.shape[0] * x.shape[1])
            time_text.set_text('')
            radius_text.set_text('')
            return surf, time_text, radius_text
        
        # 更新函数
        def update(frame):
            # 计算当前时间和半径
            current_time = t[frame]
            current_radius = np.linalg.norm(self.C) * current_time
            
            # 更新球面数据
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x = current_radius * np.outer(np.cos(u), np.sin(v))
            y = current_radius * np.outer(np.sin(u), np.sin(v))
            z = current_radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            # 更新表面数据
            surf._vec._x = x.ravel()
            surf._vec._y = y.ravel()
            surf._vec._z = z.ravel()
            
            # 更新文本
            time_text.set_text(f'时间 t = {current_time:.2f}')
            radius_text.set_text(f'各向发散运动半径 r = {current_radius:.2f}')
            
            return surf, time_text, radius_text
        
        # 创建动画
        ani = FuncAnimation(
            fig, update, frames=self.t_steps,
            init_func=init, interval=100, blit=True
        )
        
        return fig, ani
    
    def plot_radius_evolution(self):
        """绘制各向发散运动半径随时间演化的图表"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 生成时间数据
        t = np.linspace(0, self.t_max, self.t_steps)
        
        # 计算半径随时间变化
        radius = np.linalg.norm(self.C) * t
        
        # 绘制半径-时间曲线
        ax.plot(t, radius, 'b-', linewidth=3)
        ax.fill_between(t, 0, radius, color='lightblue', alpha=0.3)
        
        # 添加光速标签
        c_value = np.linalg.norm(self.C)
        ax.axline((0, 0), slope=c_value, color='r', linestyle='--', alpha=0.5, label=f'光速 = {c_value:.2f}')
        
        # 设置标签和标题
        ax.set_title('时空各向发散运动半径随时间的演化', fontsize=16)
        ax.set_xlabel('时间 t', fontsize=12)
        ax.set_ylabel('各向发散运动半径 r', fontsize=12)
        
        # 添加网格和图例
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(fontsize=10)
        
        # 添加方程说明
        equation_text = r'$r(t) = |\vec{{C}}|t = ct$，其中 $c = |\vec{{C}}|$ 为光速'
        plt.figtext(0.5, 0.01, equation_text, ha='center', fontsize=12)
        
        plt.tight_layout()
        return fig
    
    def show_all(self):
        """显示所有可视化图表"""
        # 静态各向发散运动图
        fig1 = self.plot_static_bubble()
        
        # 半径演化图
        fig2 = self.plot_radius_evolution()
        
        # 显示图表
        plt.show()

# 主程序
if __name__ == "__main__":
    # 创建可视化器实例
    visualizer = SpaceTimeBubbleVisualizer()
    
    # 显示所有可视化图表
    visualizer.show_all()
    
    # 如果需要保存动画，可以取消下面的注释
    # fig, ani = visualizer.animate_bubble()
    # ani.save('spacetime_bubble.gif', writer='pillow', fps=10)
    # plt.close(fig)