import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, Arrow

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：磁场定义方程可视化
方程：B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]

参数说明（教科书级别）：
- B：磁感应强度矢量
- k：比例常数
- dm/dt：电荷所在位置的质量变化率
- V₁：电荷的运动速度矢量
- V₂：单位电荷所在位置的空间运动速度矢量
- r：位置矢量
- r⁵：位置矢量大小的五次方
"""

class MagneticFieldEquation:
    """磁场定义方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数，实际应用中需根据单位制确定
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
        self.v1_base = np.array([1.0, 0.0, 0.0])  # 电荷运动速度基础矢量
        self.v2_base = np.array([0.0, 0.0, 1.0])  # 空间运动速度基础矢量
        self.r_max = 5.0  # 最大半径，用于可视化
    
    def calculate_magnetic_field(self, x, y, z, v1_factor=1.0, v2_factor=1.0):
        """计算磁感应强度
        B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]
        """
        # 转换为numpy数组
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        # 计算位置矢量大小r
        r = np.sqrt(x**2 + y**2 + z**2)
        
        # 避免除零错误
        r_safe = np.maximum(r, 1e-6)
        
        # 定义速度矢量
        v1 = self.v1_base * v1_factor
        v2 = self.v2_base * v2_factor
        
        # 计算第一个叉积 V₂ × r
        cross1_x = v2[1] * z - v2[2] * y
        cross1_y = v2[2] * x - v2[0] * z
        cross1_z = v2[0] * y - v2[1] * x
        
        # 计算第二个叉积 V₁ × (V₂ × r)
        cross2_x = v1[1] * cross1_z - v1[2] * cross1_y
        cross2_y = v1[2] * cross1_x - v1[0] * cross1_z
        cross2_z = v1[0] * cross1_y - v1[1] * cross1_x
        
        # 计算磁感应强度
        B_x = self.k * self.dm_dt * cross2_x / (r_safe**5)
        B_y = self.k * self.dm_dt * cross2_y / (r_safe**5)
        B_z = self.k * self.dm_dt * cross2_z / (r_safe**5)
        
        return np.array([B_x, B_y, B_z])
    
    def visualize_field_2d(self):
        """在XY平面上可视化磁场分布"""
        # 创建网格点
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)  # XY平面
        
        # 计算磁场
        B = self.calculate_magnetic_field(X, Y, Z)
        B_x, B_y, B_z = B
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制场矢量
        ax.quiver(X, Y, B_x, B_y, color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        # V₂沿Z轴，在XY平面上用圆点表示
        circle = Circle((0, 0), 0.3, fill=True, color='green')
        ax.add_patch(circle)
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, 'V₁', fontsize=14, color='red')
        ax.text(0.5, 0.5, 'V₂ (向外)', fontsize=14, color='green')
        
        # 设置标题和标签
        ax.set_title('磁场分布（XY平面）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # 添加颜色标记表示场强大小
        field_magnitude = np.sqrt(B_x**2 + B_y**2 + B_z**2)
        scatter = ax.scatter(X, Y, c=field_magnitude, cmap='viridis', s=100, alpha=0.6)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('磁感应强度大小', fontsize=12)
        
        return fig
    
    def visualize_field_3d(self):
        """3D可视化磁场分布"""
        # 创建网格点（主要在XY平面附近）
        phi = np.linspace(0, 2*np.pi, 30)
        r_values = np.linspace(0.5, self.r_max, 4)
        
        # 创建3D网格
        x, y, z = [], [], []
        for r in r_values:
            for angle in phi:
                x.append(r * np.cos(angle))
                y.append(r * np.sin(angle))
                z.append(0)  # 在XY平面上
        
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        # 计算磁场
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制场矢量
        ax.quiver(x, y, z, B_x, B_y, B_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制速度矢量指示
        scale = self.r_max * 0.6
        ax.quiver(0, 0, 0, self.v1_base[0] * scale, self.v1_base[1] * scale, self.v1_base[2] * scale,
                 length=scale, color='red', linewidth=3, label='V₁')
        ax.quiver(0, 0, 0, self.v2_base[0] * scale, self.v2_base[1] * scale, self.v2_base[2] * scale,
                 length=scale, color='green', linewidth=3, label='V₂')
        
        # 设置标题和标签
        ax.set_title('磁场分布（3D视图）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('Z坐标', fontsize=12)
        
        # 设置坐标轴范围
        limit = self.r_max * 1.2
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        # 添加图例
        ax.legend()
        
        return fig
    
    def visualize_field_strength_vs_distance(self):
        """可视化磁感应强度与距离的关系"""
        # 计算不同距离处的场强
        r = np.linspace(0.1, self.r_max, 100)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)
        
        # 计算磁场
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        # 计算场强大小
        field_magnitude = np.sqrt(B_x**2 + B_y**2 + B_z**2)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制场强-距离关系
        ax.plot(r, field_magnitude, 'b-', linewidth=2, label='磁感应强度大小')
        
        # 绘制1/r⁵参考曲线（按比例）
        reference = 1/(r**5) * np.max(field_magnitude) / np.max(1/(r**5))
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r⁵参考曲线')
        
        # 设置标题和标签
        ax.set_title('磁感应强度与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('磁感应强度大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def visualize_circular_pattern(self):
        """可视化磁场的环形分布特征"""
        # 创建圆形路径上的点
        phi = np.linspace(0, 2*np.pi, 100)
        radius = self.r_max * 0.8
        
        x = radius * np.cos(phi)
        y = radius * np.sin(phi)
        z = np.zeros_like(x)
        
        # 计算磁场
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制圆形路径
        ax.plot(x, y, 'k--', linewidth=1.5, label='圆形路径')
        
        # 在圆形路径上绘制磁场矢量
        step = 5  # 每隔5个点绘制一个矢量
        ax.quiver(x[::step], y[::step], B_x[::step], B_y[::step], color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        # V₂沿Z轴，在XY平面上用圆点表示
        circle = Circle((0, 0), 0.3, fill=True, color='green')
        ax.add_patch(circle)
        
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, 'V₁', fontsize=14, color='red')
        ax.text(0.5, 0.5, 'V₂ (向外)', fontsize=14, color='green')
        
        # 设置标题和标签
        ax.set_title('磁场的环形分布特征', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
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
        params_text = "磁场定义方程参数详解 (教科书级别):\n" + \
                      "B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]\n" + \
                      "\n参数含义:\n" + \
                      "- B: 磁感应强度矢量，描述空间中某点的磁场强弱和方向\n" + \
                      "- k: 比例常数，与单位制和物理常数相关\n" + \
                      "- dm/dt: 电荷所在位置的质量变化率，单位为kg/s\n" + \
                      "- V₁: 电荷的运动速度矢量\n" + \
                      "- V₂: 单位电荷所在位置的空间运动速度矢量\n" + \
                      "- r: 位置矢量，从原点指向场点的矢量\n" + \
                      "- r⁵: 位置矢量大小的五次方项\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了磁场的本质来源于三重叉积结构(V₁ × (V₂ × r))\n" + \
                      "- 磁场强度与质量变化率成正比\n" + \
                      "- 磁场强度与距离的五次方成反比，比电场衰减更快\n" + \
                      "- 方程表明磁场是一种具有环形特性的物理场\n" + \
                      "- 当V₁与V₂平行时，三重叉积结构会产生环形磁场\n" + \
                      "- 该定义为理解磁现象提供了统一场论的视角\n" + \
                      "- 磁场的环形分布特征与安培环路定理描述的结果一致"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建磁场定义方程可视化对象
    magnetic_eq = MagneticFieldEquation()
    
    # 显示2D场分布
    fig_2d = magnetic_eq.visualize_field_2d()
    magnetic_eq.add_parameter_explanation(fig_2d)
    
    # 显示3D场分布
    fig_3d = magnetic_eq.visualize_field_3d()
    magnetic_eq.add_parameter_explanation(fig_3d)
    
    # 显示场强-距离关系
    fig_distance = magnetic_eq.visualize_field_strength_vs_distance()
    magnetic_eq.add_parameter_explanation(fig_distance)
    
    # 显示环形分布特征
    fig_circular = magnetic_eq.visualize_circular_pattern()
    magnetic_eq.add_parameter_explanation(fig_circular)
    
    # 添加方程到图形中
    equation_text = "磁场定义方程: B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]"
    fig_2d.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_2d.savefig('./img/磁场分布2D.png', dpi=300, bbox_inches='tight')
    fig_3d.savefig('./img/磁场分布3D.png', dpi=300, bbox_inches='tight')
    fig_distance.savefig('./img/磁感应强度-距离关系.png', dpi=300, bbox_inches='tight')
    fig_circular.savefig('./img/磁场环形分布.png', dpi=300, bbox_inches='tight')
    
    print("磁场定义方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")