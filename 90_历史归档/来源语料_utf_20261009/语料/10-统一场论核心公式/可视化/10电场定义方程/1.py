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
教科书级别：电场定义方程可视化
方程：E = k × (dm/dt) × (V_1 × V_2)/r^3

参数说明（教科书级别）：
- E：电场强度矢量
- k：比例常数
- dm/dt：电荷所在位置的质量变化率
- V_1：电荷的运动速度矢量
- V_2：单位电荷所在位置的空间运动速度矢量
- r：位置矢量
- r^3：位置矢量大小的立方
"""

class ElectricFieldEquation:
    """电场定义方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数，实际应用中需根据单位制确定
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
        self.v1_base = np.array([1.0, 0.0, 0.0])  # 电荷运动速度基础矢量
        self.v2_base = np.array([0.0, 1.0, 0.0])  # 空间运动速度基础矢量
        self.r_max = 5.0  # 最大半径，用于可视化
    
    def calculate_electric_field(self, x, y, z, v1_factor=1.0, v2_factor=1.0):
        """计算电场强度
        E = k × (dm/dt) × (V_1 × V_2)/r^3
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
        
        # 计算叉积 V₁ × V₂
        cross_product_x = v1[1] * v2[2] - v1[2] * v2[1]
        cross_product_y = v1[2] * v2[0] - v1[0] * v2[2]
        cross_product_z = v1[0] * v2[1] - v1[1] * v2[0]
        
        # 计算电场强度
        E_x = self.k * self.dm_dt * cross_product_x / (r_safe**3)
        E_y = self.k * self.dm_dt * cross_product_y / (r_safe**3)
        E_z = self.k * self.dm_dt * cross_product_z / (r_safe**3)
        
        return np.array([E_x, E_y, E_z])
    
    def visualize_field_2d(self):
        """在XY平面上可视化电场分布"""
        # 创建网格点
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)  # XY平面
        
        # 计算电场
        E = self.calculate_electric_field(X, Y, Z)
        E_x, E_y, E_z = E
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制场矢量
        ax.quiver(X, Y, E_x, E_y, color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        ax.arrow(0, 0, self.v2_base[0] * self.r_max * 0.5, self.v2_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='green', ec='green')
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, r'$V_1$', fontsize=14, color='red')
        ax.text(self.v2_base[0] * self.r_max * 0.5, self.v2_base[1] * self.r_max * 0.5 + 0.5, r'$V_2$', fontsize=14, color='green')
        
        # 设置标题和标签
        ax.set_title('电场分布（XY平面）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # 添加颜色标记表示场强大小
        field_magnitude = np.sqrt(E_x**2 + E_y**2 + E_z**2)
        scatter = ax.scatter(X, Y, c=field_magnitude, cmap='viridis', s=100, alpha=0.6)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('场强大小', fontsize=12)
        
        return fig
    
    def visualize_field_3d(self):
        """3D可视化电场分布"""
        # 创建网格点
        phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.r_max * np.sin(theta) * np.cos(phi)
        y = self.r_max * np.sin(theta) * np.sin(phi)
        z = self.r_max * np.cos(theta)
        
        # 计算电场
        E = self.calculate_electric_field(x, y, z)
        E_x, E_y, E_z = E
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制场矢量
        ax.quiver(x, y, z, E_x, E_y, E_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制速度矢量指示
        scale = self.r_max * 0.6
        ax.quiver(0, 0, 0, self.v1_base[0] * scale, self.v1_base[1] * scale, self.v1_base[2] * scale,
                 length=scale, color='red', linewidth=3, label=r'$V_1$')
        ax.quiver(0, 0, 0, self.v2_base[0] * scale, self.v2_base[1] * scale, self.v2_base[2] * scale,
                 length=scale, color='green', linewidth=3, label=r'$V_2$')
        
        # 设置标题和标签
        ax.set_title('电场分布（3D视图）', fontsize=16)
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
        
        # 计算电场
        E = self.calculate_electric_field(x, y, z)
        E_x, E_y, E_z = E
        
        # 计算场强大小
        field_magnitude = np.sqrt(E_x**2 + E_y**2 + E_z**2)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制场强-距离关系
        ax.plot(r, field_magnitude, 'b-', linewidth=2, label='场强大小')
        
        # 绘制1/r³参考曲线（按比例）
        reference = 1/(r**3) * np.max(field_magnitude) / np.max(1/(r**3))
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r³参考曲线')
        
        # 设置标题和标签
        ax.set_title('电场强度与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('场强大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def visualize_velocity_effect(self):
        """可视化速度变化对电场的影响"""
        # 创建网格点
        x = np.linspace(-self.r_max, self.r_max, 15)
        y = np.linspace(-self.r_max, self.r_max, 15)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 选择几个速度因子组合
        velocity_combinations = [(0.5, 1.0), (1.0, 1.0), (1.0, 1.5)]
        
        # 创建图形
        fig, axes = plt.subplots(1, len(velocity_combinations), figsize=(18, 6))
        fig.suptitle('不同速度组合对电场的影响', fontsize=16)
        
        # 为每个速度组合创建一个子图
        for i, (v1_factor, v2_factor) in enumerate(velocity_combinations):
            # 计算电场
            E = self.calculate_electric_field(X, Y, Z, v1_factor, v2_factor)
            E_x, E_y, E_z = E
            
            # 绘制场矢量
            axes[i].quiver(X, Y, E_x, E_y, color='blue', alpha=0.8)
            
            # 设置标题和标签
            axes[i].set_title(f'V$_{{1}}$ = {v1_factor}×基础值, V$_{{2}}$ = {v2_factor}×基础值', fontsize=14)
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
            """添加专业级别的参数解释文本框"""
        # Ensure img directory exists
        img_dir = './img'
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        
        params_text = "电场定义方程参数详解 (教科书级别):\n" + \
                      r"$E = k × (dm/dt) × (V_1 × V_2)/r^3$\n" + \
                      "\n参数含义:\n" + \
                      "- E: 电场强度矢量，描述空间中某点的电场强弱和方向\n" + \
                      "- k: 比例常数，与单位制和物理常数相关\n" + \
                      "- dm/dt: 电荷所在位置的质量变化率，单位为kg/s\n" + \
                      r"- V$_1$: 电荷的运动速度矢量\n" + \
                      r"- V$_2$: 单位电荷所在位置的空间运动速度矢量\n" + \
                      "- r: 位置矢量，从原点指向场点的矢量\n" + \
                      r"- r$^3$: 位置矢量大小的立方项\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了电场的本质来源于两个速度矢量的叉积\n" + \
                      "- 电场强度与质量变化率成正比\n" + \
                      r"- 电场强度与V$_1$和V$_2$的叉积成正比，体现了电磁感应的本质\n" + \
                      "- 电场强度与距离的立方成反比，这与库仑定律的平方反比律不同\n" + \
                      "- 方程表明电场是一种与空间运动相关的物理场\n" + \
                      "- 该定义为理解电磁现象提供了统一场论的视角\n" + \
                      r"- 当V$_1$和V$_2$平行时，叉积为零，电场强度也为零"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    # 创建电场定义方程可视化对象
    electric_eq = ElectricFieldEquation()
    
    # 显示2D场分布
    fig_2d = electric_eq.visualize_field_2d()
    electric_eq.add_parameter_explanation(fig_2d)
    
    # 显示3D场分布
    fig_3d = electric_eq.visualize_field_3d()
    electric_eq.add_parameter_explanation(fig_3d)
    
    # 显示场强-距离关系
    fig_distance = electric_eq.visualize_field_strength_vs_distance()
    electric_eq.add_parameter_explanation(fig_distance)
    
    # 显示速度影响
    fig_velocity = electric_eq.visualize_velocity_effect()
    electric_eq.add_parameter_explanation(fig_velocity)
    
    # 添加方程到图形中
    equation_text = r"电场定义方程: $E = k × (dm/dt) × (V_1 × V_2)/r^3$"
    fig_2d.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_2d.savefig('./img/电场分布2D.png', dpi=300, bbox_inches='tight')
    fig_3d.savefig('./img/电场分布3D.png', dpi=300, bbox_inches='tight')
    fig_distance.savefig('./img/场强-距离关系.png', dpi=300, bbox_inches='tight')
    fig_velocity.savefig('./img/不同速度对电场的影响.png', dpi=300, bbox_inches='tight')
    
    print("电场定义方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")