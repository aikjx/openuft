import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：运动动量方程可视化
方程：P = m(C - V)

参数说明（教科书级别）：
- P：运动动量矢量
- m：运动物体的质量
- C：空间本身的运动速度矢量（光速）
- V：物体相对于观察者的运动速度矢量
"""

class MotionMomentumEquation:
    """运动动量方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.base_mass = 1.0  # 基础质量，单位：kg
        
    def calculate_motion_momentum(self, mass, velocity):
        """根据运动动量方程计算运动动量
        P = m(C - V)
        这里假设C沿Z轴方向
        """
        # 定义空间运动速度矢量C（沿Z轴方向，大小为光速）
        C = np.array([0, 0, self.c])
        
        # 计算运动动量矢量
        momentum_vector = mass * (C - velocity)
        
        return momentum_vector
    
    def visualize_velocity_effect(self):
        """可视化不同速度下的动量变化"""
        # 创建图形
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 设置坐标轴范围
        max_axis = self.c * 1.2e-8  # 缩放因子，便于可视化
        ax.set_xlim([-max_axis, max_axis])
        ax.set_ylim([-max_axis, max_axis])
        ax.set_zlim([-max_axis, max_axis])
        
        # 设置坐标轴标签
        ax.set_xlabel('X轴', fontsize=12)
        ax.set_ylabel('Y轴', fontsize=12)
        ax.set_zlabel('Z轴', fontsize=12)
        
        # 设置标题
        ax.set_title('不同运动速度下的动量矢量可视化', fontsize=14)
        
        # 固定质量
        mass = self.base_mass  # kg
        
        # 不同速度值（以光速的百分比表示）
        velocity_percentages = [0, 20, 40, 60, 80]  # % c
        colors = ['blue', 'green', 'yellow', 'orange', 'red']
        
        scale_factor = 1e-8  # 缩放因子，便于可视化
        
        # 绘制空间运动速度矢量C
        C = np.array([0, 0, self.c])
        scaled_C = C * scale_factor
        ax.quiver(0, 0, 0, scaled_C[0], scaled_C[1], scaled_C[2],
                 color='purple', linewidth=2, label='C (空间运动速度)', arrow_length_ratio=0.1)
        
        # 绘制不同速度下的动量矢量
        for i, (percent, color) in enumerate(zip(velocity_percentages, colors)):
            # 计算速度矢量（沿Z轴方向）
            velocity_magnitude = percent / 100 * self.c
            velocity = np.array([0, 0, velocity_magnitude])
            
            # 计算动量矢量
            momentum = self.calculate_motion_momentum(mass, velocity)
            scaled_momentum = momentum * scale_factor
            
            # 绘制速度矢量
            scaled_velocity = velocity * scale_factor
            ax.quiver(0, 0, 0, scaled_velocity[0], scaled_velocity[1], scaled_velocity[2],
                     color=color, linestyle='dashed', arrow_length_ratio=0.1)
            
            # 绘制动量矢量
            ax.quiver(0, 0, 0, scaled_momentum[0], scaled_momentum[1], scaled_momentum[2],
                     color=color, length=1, normalize=False, arrow_length_ratio=0.1)
            
            # 添加标签
            label_pos = scaled_momentum * 1.1  # 标签位置在矢量末端外侧
            ax.text(label_pos[0], label_pos[1], label_pos[2],
                   f'V={percent}%c\n|p|={np.linalg.norm(momentum):.2e} kg·m/s',
                   color=color, fontsize=9)
        
        # 添加图例
        legend_elements = [
            plt.Line2D([0], [0], color='purple', lw=2, label='C (空间运动速度)'),
            plt.Line2D([0], [0], color='blue', lw=2, label='V=0%c'),
            plt.Line2D([0], [0], color='green', lw=2, label='V=20%c'),
            plt.Line2D([0], [0], color='yellow', lw=2, label='V=40%c'),
            plt.Line2D([0], [0], color='orange', lw=2, label='V=60%c'),
            plt.Line2D([0], [0], color='red', lw=2, label='V=80%c')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return fig
    
    def visualize_momentum_velocity_relationship(self):
        """可视化动量大小与速度的关系"""
        # 生成速度百分比数据
        velocity_percentages = np.linspace(0, 99, 100)  # % c
        
        # 计算动量大小
        momentum_magnitudes = []
        for percent in velocity_percentages:
            velocity_magnitude = percent / 100 * self.c
            velocity = np.array([0, 0, velocity_magnitude])
            momentum = self.calculate_motion_momentum(self.base_mass, velocity)
            momentum_magnitudes.append(np.linalg.norm(momentum))
        
        # 创建图形
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # 绘制动量大小-速度关系
        ax.plot(velocity_percentages, momentum_magnitudes, 'b-', linewidth=2)
        
        # 设置坐标轴和标题
        ax.set_title('运动动量大小与速度的关系', fontsize=14)
        ax.set_xlabel('速度 V (% c)', fontsize=12)
        ax.set_ylabel('动量大小 |P| (kg·m/s)', fontsize=12)
        
        # 添加网格
        ax.grid(True, alpha=0.3)
        
        # 添加关键点标记
        key_percentages = [0, 50, 90, 99]
        for percent in key_percentages:
            idx = np.argmin(np.abs(velocity_percentages - percent))
            ax.plot(velocity_percentages[idx], momentum_magnitudes[idx], 'ro')
            ax.text(velocity_percentages[idx]+1, momentum_magnitudes[idx],
                   f'V={percent}%c', fontsize=9)
        
        # 添加方程到图形中
        equation_text = "运动动量方程: P = m(C - V)"
        fig.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
        
        return fig
    
    def add_parameter_explanation(self, fig):
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
            """添加专业级别的参数解释文本框"""
        params_text = "运动动量方程参数详解 (教科书级别):\n" + \
                      "1. P: 运动动量矢量，描述运动物体的动量状态\n" + \
                      "2. m: 运动物体的质量\n" + \
                      "3. C: 空间本身的运动速度矢量，其模长为光速c\n" + \
                      "   (c = 299,792,458 m/s)\n" + \
                      "4. V: 物体相对于观察者的运动速度矢量\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程表明物体的动量是其质量乘以空间运动速度与物体运动速度的差值\n" + \
                      "- 当物体静止时(V=0)，动量为P = mC，即静止动量方程\n" + \
                      "- 随着物体速度V增加，动量减小，当V趋近于C时，动量趋近于零\n" + \
                      "- 这一关系揭示了为什么物体无法达到或超过光速\n" + \
                      "- 统一场论中动量的定义超越了经典力学，将空间运动纳入考量"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建运动动量方程可视化对象
    motion_momentum_eq = MotionMomentumEquation()
    
    # 显示速度效应可视化
    fig_velocity_effect = motion_momentum_eq.visualize_velocity_effect()
    motion_momentum_eq.add_parameter_explanation(fig_velocity_effect)
    
    # 显示动量-速度关系可视化
    fig_relationship = motion_momentum_eq.visualize_momentum_velocity_relationship()
    motion_momentum_eq.add_parameter_explanation(fig_relationship)
    
    # 保存图形为PNG文件
    fig_velocity_effect.savefig('./img/不同速度下的动量矢量.png', dpi=300, bbox_inches='tight')
    fig_relationship.savefig('./img/动量-速度关系.png', dpi=300, bbox_inches='tight')
    
    print("运动动量方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")