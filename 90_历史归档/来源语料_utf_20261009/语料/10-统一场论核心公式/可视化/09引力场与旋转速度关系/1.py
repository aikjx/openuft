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
教科书级别：引力场与旋转速度关系方程可视化
方程：A = -k × (dm/dt) × (ω × r)/r³

参数说明（教科书级别）：
- A：引力场强度矢量
- k：比例常数
- dm/dt：物体质量变化率
- ω：旋转角速度矢量
- r：位置矢量
- r³：位置矢量大小的立方
"""

class GravitationalFieldRotation:
    """引力场与旋转速度关系方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数，实际应用中需根据单位制确定
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
        self.omega_base = 1.0  # 基础角速度，单位：rad/s
        self.r_max = 5.0  # 最大半径，用于可视化
    
    def calculate_gravitational_field(self, x, y, z, omega_factor=1.0):
        """计算引力场强度
        A = -k × (dm/dt) × (ω × r)/r³
        假设角速度ω沿Z轴方向
        """
        # 转换为numpy数组
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        # 计算位置矢量大小r
        r = np.sqrt(x**2 + y**2 + z**2)
        
        # 避免除零错误
        r_safe = np.maximum(r, 1e-6)
        
        # 定义角速度矢量（沿Z轴）
        omega = np.array([0, 0, self.omega_base * omega_factor])
        
        # 计算叉积 ω × r
        cross_product_x = omega[1] * z - omega[2] * y
        cross_product_y = omega[2] * x - omega[0] * z
        cross_product_z = omega[0] * y - omega[1] * x
        
        # 计算引力场强度
        A_x = -self.k * self.dm_dt * cross_product_x / (r_safe**3)
        A_y = -self.k * self.dm_dt * cross_product_y / (r_safe**3)
        A_z = -self.k * self.dm_dt * cross_product_z / (r_safe**3)
        
        return np.array([A_x, A_y, A_z])
    
    def visualize_field_2d(self):
        """在XY平面上可视化引力场分布"""
        # 创建网格点
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)  # XY平面
        
        # 计算引力场
        A = self.calculate_gravitational_field(X, Y, Z)
        A_x, A_y, A_z = A
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制场矢量
        ax.quiver(X, Y, A_x, A_y, color='blue', alpha=0.8)
        
        # 绘制角速度方向指示
        ax.arrow(0, 0, 0, 0, 0, self.r_max * 0.8, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        ax.text(0.5, self.r_max * 0.85, 'ω', fontsize=14, color='red')
        
        # 设置标题和标签
        ax.set_title('引力场与旋转速度关系（XY平面）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # 添加颜色标记表示场强大小
        field_magnitude = np.sqrt(A_x**2 + A_y**2 + A_z**2)
        scatter = ax.scatter(X, Y, c=field_magnitude, cmap='viridis', s=100, alpha=0.6)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('场强大小', fontsize=12)
        
        return fig
    
    def visualize_field_3d(self):
        """3D可视化引力场分布"""
        # 创建网格点
        phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.r_max * np.sin(theta) * np.cos(phi)
        y = self.r_max * np.sin(theta) * np.sin(phi)
        z = self.r_max * np.cos(theta)
        
        # 计算引力场
        A = self.calculate_gravitational_field(x, y, z)
        A_x, A_y, A_z = A
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制场矢量
        ax.quiver(x, y, z, A_x, A_y, A_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制角速度方向指示
        ax.quiver(0, 0, 0, 0, 0, self.r_max * 1.2, length=self.r_max * 0.8, 
                 color='red', linewidth=3, label='ω')
        
        # 设置标题和标签
        ax.set_title('引力场与旋转速度关系（3D视图）', fontsize=16)
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
        """可视化场强大小与距离的关系"""
        # 计算不同距离处的场强
        r = np.linspace(0.1, self.r_max, 100)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)
        
        # 计算引力场
        A = self.calculate_gravitational_field(x, y, z)
        A_x, A_y, A_z = A
        
        # 计算场强大小
        field_magnitude = np.sqrt(A_x**2 + A_y**2 + A_z**2)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制场强-距离关系
        ax.plot(r, field_magnitude, 'b-', linewidth=2, label='场强大小')
        
        # 绘制1/r³参考曲线（按比例）
        reference = 1/(r**3) * np.max(field_magnitude) / np.max(1/(r**3))
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r³参考曲线')
        
        # 设置标题和标签
        ax.set_title('引力场强度与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('场强大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def visualize_omega_effect(self):
        """可视化角速度变化对引力场的影响"""
        # 创建网格点
        x = np.linspace(-self.r_max, self.r_max, 15)
        y = np.linspace(-self.r_max, self.r_max, 15)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 选择几个角速度因子
        omega_factors = [0.5, 1.0, 1.5]
        
        # 创建图形
        fig, axes = plt.subplots(1, len(omega_factors), figsize=(18, 6))
        fig.suptitle('不同角速度对引力场的影响', fontsize=16)
        
        # 为每个角速度因子创建一个子图
        for i, omega_factor in enumerate(omega_factors):
            # 计算引力场
            A = self.calculate_gravitational_field(X, Y, Z, omega_factor)
            A_x, A_y, A_z = A
            
            # 绘制场矢量
            axes[i].quiver(X, Y, A_x, A_y, color='blue', alpha=0.8)
            
            # 设置标题和标签
            axes[i].set_title(f'角速度 ω = {omega_factor}×基础值', fontsize=14)
            axes[i].set_xlabel('X坐标', fontsize=12)
            if i == 0:
                axes[i].set_ylabel('Y坐标', fontsize=12)
            axes[i].set_aspect('equal')
            axes[i].grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
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
        params_text = "引力场与旋转速度关系方程参数详解 (教科书级别):\n" + \
                      "A = -k × (dm/dt) × (ω × r)/r³\n" + \
                      "\n参数含义:\n" + \
                      "- A: 引力场强度矢量，描述空间中某点的引力场强弱和方向\n" + \
                      "- k: 比例常数，与单位制和物理常数相关\n" + \
                      "- dm/dt: 物体质量变化率，单位为kg/s\n" + \
                      "- ω: 旋转角速度矢量，描述物体旋转的快慢和方向\n" + \
                      "- r: 位置矢量，从原点指向场点的矢量\n" + \
                      "- r³: 位置矢量大小的立方项\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了引力场与旋转运动的内在联系\n" + \
                      "- 引力场强度与质量变化率成正比\n" + \
                      "- 引力场强度与角速度和位置矢量的叉积成正比\n" + \
                      "- 引力场强度与距离的立方成反比，这与牛顿万有引力的平方反比律不同\n" + \
                      "- 负号表示引力场的方向与(ω×r)方向相反\n" + \
                      "- 方程表明旋转运动在统一场论中对引力场有着重要贡献\n" + \
                      "- 该关系为理解宇宙中天体运动和引力现象提供了新视角"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建引力场与旋转速度关系可视化对象
    grav_rot_eq = GravitationalFieldRotation()
    
    # 显示2D场分布
    fig_2d = grav_rot_eq.visualize_field_2d()
    grav_rot_eq.add_parameter_explanation(fig_2d)
    
    # 显示3D场分布
    fig_3d = grav_rot_eq.visualize_field_3d()
    grav_rot_eq.add_parameter_explanation(fig_3d)
    
    # 显示场强-距离关系
    fig_distance = grav_rot_eq.visualize_field_strength_vs_distance()
    grav_rot_eq.add_parameter_explanation(fig_distance)
    
    # 显示角速度影响
    fig_omega = grav_rot_eq.visualize_omega_effect()
    grav_rot_eq.add_parameter_explanation(fig_omega)
    
    # 添加方程到图形中
    equation_text = "引力场与旋转速度关系方程: A = -k × (dm/dt) × (ω × r)/r³"
    fig_2d.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_2d.savefig('./img/引力场分布2D.png', dpi=300, bbox_inches='tight')
    fig_3d.savefig('./img/引力场分布3D.png', dpi=300, bbox_inches='tight')
    fig_distance.savefig('./img/场强-距离关系.png', dpi=300, bbox_inches='tight')
    fig_omega.savefig('./img/不同角速度对引力场的影响.png', dpi=300, bbox_inches='tight')
    
    print("引力场与旋转速度关系方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")