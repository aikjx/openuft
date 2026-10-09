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
教科书级别：静止动量方程可视化
方程：p₀ = m₀C₀

参数说明（教科书级别）：
- p₀：静止动量矢量
- m₀：静止质量
- C₀：静止物体周围空间运动的速度矢量，其模长为光速c
"""

class RestMomentumEquation:
    """静止动量方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.base_mass = 1.0  # 基础质量，单位：kg
        
    def calculate_rest_momentum(self, mass, direction=np.array([1, 0, 0])):
        """根据静止动量方程计算静止动量
        p₀ = m₀C₀
        """
        # 归一化方向矢量
        direction = np.array(direction)
        unit_direction = direction / np.linalg.norm(direction)
        
        # 计算静止动量矢量（C₀的大小为光速c）
        momentum_vector = mass * self.c * unit_direction
        
        return momentum_vector
    
    def visualize_momentum_vector(self):
        """可视化不同质量下的静止动量矢量"""
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 设置坐标轴范围
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-5, 5])
        
        # 设置坐标轴标签
        ax.set_xlabel('X轴', fontsize=12)
        ax.set_ylabel('Y轴', fontsize=12)
        ax.set_zlabel('Z轴', fontsize=12)
        
        # 设置标题
        ax.set_title('静止动量矢量可视化', fontsize=14)
        
        # 不同质量值
        masses = [0.5, 1.0, 1.5, 2.0]  # kg
        
        # 不同方向
        directions = [
            [1, 0, 0],   # X轴正方向
            [0, 1, 0],   # Y轴正方向
            [0, 0, 1],   # Z轴正方向
            [1, 1, 1]    # 对角线方向
        ]
        
        # 颜色列表
        colors = ['r', 'g', 'b', 'purple']
        
        # 绘制动量矢量
        scale_factor = 1e-8  # 缩放因子，便于可视化
        for i, (mass, direction, color) in enumerate(zip(masses, directions, colors)):
            # 计算动量矢量
            momentum = self.calculate_rest_momentum(mass, direction)
            scaled_momentum = momentum * scale_factor
            
            # 绘制矢量
            ax.quiver(0, 0, 0, scaled_momentum[0], scaled_momentum[1], scaled_momentum[2],
                     color=color, length=1, normalize=False, arrow_length_ratio=0.1)
            
            # 添加标签
            label_pos = scaled_momentum * 1.1  # 标签位置在矢量末端外侧
            ax.text(label_pos[0], label_pos[1], label_pos[2],
                   f'm₀={mass}kg\n|p₀|={np.linalg.norm(momentum):.2e} kg·m/s',
                   color=color, fontsize=10)
        
        # 添加图例
        legend_elements = [
            plt.Line2D([0], [0], color='r', lw=2, label='m₀=0.5kg'),
            plt.Line2D([0], [0], color='g', lw=2, label='m₀=1.0kg'),
            plt.Line2D([0], [0], color='b', lw=2, label='m₀=1.5kg'),
            plt.Line2D([0], [0], color='purple', lw=2, label='m₀=2.0kg')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return fig
    
    def visualize_mass_momentum_relationship(self):
        """可视化质量与动量大小的关系"""
        # 生成质量数据
        masses = np.linspace(0.1, 5, 100)  # kg
        
        # 计算动量大小
        momentum_magnitudes = [np.linalg.norm(self.calculate_rest_momentum(m)) for m in masses]
        
        # 创建图形
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # 绘制质量-动量关系
        ax.plot(masses, momentum_magnitudes, 'b-', linewidth=2)
        
        # 设置坐标轴和标题
        ax.set_title('静止动量大小与质量的关系', fontsize=14)
        ax.set_xlabel('静止质量 m₀ (kg)', fontsize=12)
        ax.set_ylabel('静止动量大小 |p₀| (kg·m/s)', fontsize=12)
        
        # 添加网格
        ax.grid(True, alpha=0.3)
        
        # 添加方程到图形中
        equation_text = "静止动量方程: p₀ = m₀C₀"
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
        params_text = "静止动量方程参数详解 (教科书级别):\n" + \
                      "1. p₀: 静止动量矢量，描述静止物体所具有的动量\n" + \
                      "2. m₀: 静止质量，表示物体在静止参考系中的质量\n" + \
                      "3. C₀: 静止物体周围空间运动的速度矢量，其模长为光速c\n" + \
                      "   (c = 299,792,458 m/s)\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了静止物体仍然具有动量，这是统一场论的重要发现\n" + \
                      "- 静止动量的存在表明即使物体静止，其周围空间仍以光速运动\n" + \
                      "- 动量大小与质量成正比，比例系数为光速c\n" + \
                      "- 静止动量的方向由空间运动的方向决定\n" + \
                      "- 这一概念为理解质量与能量的等价性提供了新视角"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建静止动量方程可视化对象
    rest_momentum_eq = RestMomentumEquation()
    
    # 显示动量矢量可视化
    fig_vector = rest_momentum_eq.visualize_momentum_vector()
    rest_momentum_eq.add_parameter_explanation(fig_vector)
    
    # 显示质量-动量关系可视化
    fig_relationship = rest_momentum_eq.visualize_mass_momentum_relationship()
    rest_momentum_eq.add_parameter_explanation(fig_relationship)
    
    # 保存图形为PNG文件
    fig_vector.savefig('./img/静止动量矢量可视化.png', dpi=300, bbox_inches='tight')
    fig_relationship.savefig('./img/质量-动量关系.png', dpi=300, bbox_inches='tight')
    
    print("静止动量方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")