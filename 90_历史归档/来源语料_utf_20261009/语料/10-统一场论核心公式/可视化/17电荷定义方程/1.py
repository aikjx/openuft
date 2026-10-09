import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：电荷定义方程可视化
方程：Q = k ∫(dm/dt)(V × r)/r³ dV

参数说明（教科书级别）：
- Q：电荷量
- k：比例常数
- dm/dt：质量变化率
- V：电荷运动速度
- r：位置矢量
- r³：位置矢量的模的立方
- dV：体积元
"""

class ChargeDefinitionEquation:
    """电荷定义方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数
        self.c = 1.0  # 归一化的光速
        self.dm_dt = 1.0  # 质量变化率
        self.v_magnitude = 0.5  # 电荷运动速度大小
        
        # 设置3D可视化的参数
        self.grid_size = 20  # 网格大小
        self.grid_range = 3.0  # 网格范围
    
    def charge_field(self, x, y, z, q=1.0):
        """模拟点电荷的电场分布
        用于可视化电荷的电场效应
        """
        # 计算到电荷中心的距离
        r = np.sqrt(x**2 + y**2 + z**2)
        
        # 避免除零错误
        r_safe = np.maximum(r, 1e-6)
        
        # 电场强度 E ∝ q/r²
        E = q / (r_safe**2)
        
        # 计算电场方向（径向）
        if isinstance(x, np.ndarray):
            Ex = E * x / r_safe
            Ey = E * y / r_safe
            Ez = E * z / r_safe
        else:
            Ex = E * x / r_safe if r_safe > 0 else 0
            Ey = E * y / r_safe if r_safe > 0 else 0
            Ez = E * z / r_safe if r_safe > 0 else 0
            
        return Ex, Ey, Ez
    
    def charge_current_effect(self, x, y, z, vx, vy, vz):
        """模拟运动电荷产生的磁场效应
        简化的毕奥-萨伐尔定律近似
        """
        # 计算位置矢量和速度矢量的叉乘效应
        r = np.sqrt(x**2 + y**2 + z**2)
        r_safe = np.maximum(r, 1e-6)
        
        # 计算速度与位置矢量的叉乘 (V × r)
        cross_x = vy * z - vz * y
        cross_y = vz * x - vx * z
        cross_z = vx * y - vy * x
        
        # 磁场强度 B ∝ (V × r)/r³
        Bx = cross_x / (r_safe**3)
        By = cross_y / (r_safe**3)
        Bz = cross_z / (r_safe**3)
        
        # 归一化以便可视化
        B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
        B_mag_safe = np.maximum(B_mag, 1e-6)
        
        Bx = Bx / B_mag_safe
        By = By / B_mag_safe
        Bz = Bz / B_mag_safe
        
        return Bx, By, Bz
    
    def visualize_point_charge_electric_field(self):
        """可视化点电荷的电场分布"""
        # 创建2D网格
        x = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        y = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 计算电场
        Ex, Ey, Ez = self.charge_field(X, Y, Z, q=1.0)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制电场矢量场
        magnitude = np.sqrt(Ex**2 + Ey**2)
        
        # 绘制电场流线
        stream = ax.streamplot(X, Y, Ex, Ey, density=1.5, color=magnitude, 
                              cmap='coolwarm', linewidth=1, arrowsize=1.5)
        
        # 添加颜色条
        cbar = fig.colorbar(stream.lines, ax=ax)
        cbar.set_label('电场强度相对大小', fontsize=12)
        
        # 绘制点电荷
        charge_pos = (0, 0)
        charge_color = 'red' if 1.0 > 0 else 'blue'
        charge_circle = Circle(charge_pos, 0.2, color=charge_color, label=f'点电荷 Q={1.0:.1f}')
        ax.add_patch(charge_circle)
        
        # 设置标题和标签
        ax.set_title('点电荷的电场分布', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 设置坐标轴比例
        ax.set_aspect('equal')
        
        return fig
    
    def visualize_moving_charge_effect(self):
        """可视化运动电荷的效应"""
        # 创建3D网格
        x = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        y = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 设置电荷运动速度（沿x轴）
        vx = self.v_magnitude * self.c
        vy = 0
        vz = 0
        
        # 计算磁场效应
        Bx, By, Bz = self.charge_current_effect(X, Y, Z, vx, vy, vz)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制磁场矢量场（2D投影）
        magnitude = np.sqrt(Bx**2 + By**2)
        
        # 绘制磁场流线
        stream = ax.streamplot(X, Y, Bx, By, density=1.5, color=magnitude, 
                              cmap='viridis', linewidth=1, arrowsize=1.5)
        
        # 添加颜色条
        cbar = fig.colorbar(stream.lines, ax=ax)
        cbar.set_label('磁场强度相对大小', fontsize=12)
        
        # 绘制运动电荷
        charge_pos = (0, 0)
        charge_circle = Circle(charge_pos, 0.2, color='red', label=f'运动电荷 Q=1.0')
        ax.add_patch(charge_circle)
        
        # 绘制速度矢量
        ax.arrow(0, 0, vx/2, 0, head_width=0.3, head_length=0.3, fc='blue', ec='blue', 
                linewidth=2, label=f'速度 v={vx:.1f}')
        
        # 设置标题和标签
        ax.set_title('运动电荷产生的磁场效应', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 设置坐标轴比例
        ax.set_aspect('equal')
        
        return fig
    
    def visualize_charge_definition_3d(self):
        """3D可视化电荷定义方程的物理含义"""
        # 创建3D网格
        x = np.linspace(-self.grid_range, self.grid_range, 20)
        y = np.linspace(-self.grid_range, self.grid_range, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 计算(V × r)/r³项的分布
        # 假设速度沿x轴
        vx = self.v_magnitude * self.c
        vy = 0
        vz = 0
        
        # 计算(V × r)/r³
        r = np.sqrt(X**2 + Y**2 + Z**2)
        r_safe = np.maximum(r, 1e-6)
        
        # 叉乘项 (V × r)
        cross_x = vy * Z - vz * Y
        cross_y = vz * X - vx * Z
        cross_z = vx * Y - vy * X
        
        # 计算 (V × r)/r³
        term_x = cross_x / (r_safe**3)
        term_y = cross_y / (r_safe**3)
        term_z = cross_z / (r_safe**3)
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制矢量场
        step = 3  # 减少矢量数量以避免拥挤
        ax.quiver(X[::step, ::step], Y[::step, ::step], Z[::step, ::step],
                 term_x[::step, ::step], term_y[::step, ::step], term_z[::step, ::step],
                 length=0.5, normalize=True, color='blue', arrow_length_ratio=0.3)
        
        # 绘制电荷位置
        ax.scatter(0, 0, 0, color='red', s=100, marker='o', label='电荷位置')
        
        # 绘制速度矢量
        ax.quiver(0, 0, 0, vx/2, vy/2, vz/2, color='green',
                 arrow_length_ratio=0.3, label=f'速度 v={vx:.1f}')
        
        # 设置标题和标签
        ax.set_title('电荷定义方程中的 (V × r)/r³ 项可视化', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('Z坐标', fontsize=12)
        ax.legend()
        
        return fig
    
    def visualize_charge_relation(self):
        """可视化电荷与质量变化率、速度的关系"""
        # 创建图形和子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 子图1: 电荷与质量变化率的关系
        dm_dt_values = np.linspace(0.1, 2.0, 50)
        q_values = self.k * dm_dt_values  # 简化模型：Q ∝ dm/dt
        
        ax1.plot(dm_dt_values, q_values, 'b-', linewidth=2.5)
        ax1.set_title('电荷与质量变化率的关系', fontsize=14)
        ax1.set_xlabel('质量变化率 dm/dt', fontsize=12)
        ax1.set_ylabel('电荷量 Q', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.text(0.5*np.max(dm_dt_values), 0.7*np.max(q_values), 
                'Q ∝ dm/dt', fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
        
        # 子图2: 电荷与速度的关系
        v_values = np.linspace(0, 0.99, 50)  # 速度比例（v/c）
        q_eff_values = self.k * self.dm_dt * v_values  # 简化模型：Q_eff ∝ v
        
        ax2.plot(v_values, q_eff_values, 'g-', linewidth=2.5)
        ax2.set_title('电荷与速度的关系', fontsize=14)
        ax2.set_xlabel('速度比例 v/c', fontsize=12)
        ax2.set_ylabel('有效电荷量 Q_eff', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.text(0.5*np.max(v_values), 0.7*np.max(q_eff_values), 
                'Q_eff ∝ v', fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
        
        fig.suptitle('电荷定义方程中的比例关系', fontsize=16)
        
        return fig
    
    def visualize_charges_interaction(self):
        """可视化两个电荷之间的相互作用"""
        # 创建2D网格
        x = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        y = np.linspace(-self.grid_range, self.grid_range, self.grid_size)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # 定义两个电荷的位置和电荷量
        q1 = 1.0  # 电荷1
        pos1 = (-1.5, 0)  # 电荷1位置
        q2 = -1.0  # 电荷2（异号）
        pos2 = (1.5, 0)  # 电荷2位置
        
        # 计算总电场
        Ex1, Ey1, Ez1 = self.charge_field(X-pos1[0], Y-pos1[1], Z, q1)
        Ex2, Ey2, Ez2 = self.charge_field(X-pos2[0], Y-pos2[1], Z, q2)
        Ex_total = Ex1 + Ex2
        Ey_total = Ey1 + Ey2
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制电场流线
        magnitude = np.sqrt(Ex_total**2 + Ey_total**2)
        stream = ax.streamplot(X, Y, Ex_total, Ey_total, density=1.5, color=magnitude, 
                              cmap='coolwarm', linewidth=1, arrowsize=1.5)
        
        # 添加颜色条
        cbar = fig.colorbar(stream.lines, ax=ax)
        cbar.set_label('电场强度相对大小', fontsize=12)
        
        # 绘制电荷
        charge_color1 = 'red' if q1 > 0 else 'blue'
        charge_color2 = 'red' if q2 > 0 else 'blue'
        
        charge1 = Circle(pos1, 0.2, color=charge_color1, label=f'电荷 Q1={q1:.1f}')
        charge2 = Circle(pos2, 0.2, color=charge_color2, label=f'电荷 Q2={q2:.1f}')
        ax.add_patch(charge1)
        ax.add_patch(charge2)
        
        # 设置标题和标签
        ax.set_title('两个异号电荷之间的电场分布', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 设置坐标轴比例
        ax.set_aspect('equal')
        
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
            """添加专业级别的参数解释文本框"""
        params_text = "电荷定义方程参数详解 (教科书级别):\n" + \
                      "Q = k ∫(dm/dt)(V × r)/r³ dV\n" + \
                      "\n参数含义:\n" + \
                      "- Q: 电荷量，表示电荷的多少\n" + \
                      "- k: 比例常数，与单位制选择有关\n" + \
                      "- dm/dt: 质量变化率，表示单位时间内质量的变化\n" + \
                      "- V: 电荷的运动速度矢量\n" + \
                      "- r: 位置矢量，从电荷指向场点\n" + \
                      "- r³: 位置矢量模的立方\n" + \
                      "- dV: 体积元\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程从统一场论角度定义了电荷的本质\n" + \
                      "- 揭示电荷是质量随时间变化并伴随空间运动的表现\n" + \
                      "- (V × r)/r³项描述了运动的方向性特征\n" + \
                      "- 电荷的电场分布为E ∝ Q/r²，方向沿径向\n" + \
                      "- 运动电荷产生磁场，B ∝ (V × r)/r³\n" + \
                      "- 电荷量与质量变化率、运动速度成正比\n" + \
                      "- 该定义将电磁现象与质量、运动等基本物理量统一起来\n" + \
                      "- 正负电荷表示质量变化的不同方向或运动的对称性" 
        
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
    
    # 创建电荷定义方程可视化对象
    charge_eq = ChargeDefinitionEquation()
    
    # 显示点电荷电场分布
    fig_point_charge = charge_eq.visualize_point_charge_electric_field()
    charge_eq.add_parameter_explanation(fig_point_charge)
    
    # 显示运动电荷效应
    fig_moving_charge = charge_eq.visualize_moving_charge_effect()
    charge_eq.add_parameter_explanation(fig_moving_charge)
    
    # 显示电荷定义3D可视化
    fig_charge_def_3d = charge_eq.visualize_charge_definition_3d()
    charge_eq.add_parameter_explanation(fig_charge_def_3d)
    
    # 显示电荷关系
    fig_charge_relation = charge_eq.visualize_charge_relation()
    charge_eq.add_parameter_explanation(fig_charge_relation)
    
    # 显示电荷相互作用
    fig_charges_interaction = charge_eq.visualize_charges_interaction()
    charge_eq.add_parameter_explanation(fig_charges_interaction)
    
    # 添加方程到图形中
    equation_text = "电荷定义方程: Q = k ∫(dm/dt)(V × r)/r³ dV"
    fig_point_charge.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_point_charge.savefig('./img/点电荷电场分布.png', dpi=300, bbox_inches='tight')
    fig_moving_charge.savefig('./img/运动电荷磁场效应.png', dpi=300, bbox_inches='tight')
    fig_charge_def_3d.savefig('./img/电荷定义3D可视化.png', dpi=300, bbox_inches='tight')
    fig_charge_relation.savefig('./img/电荷比例关系.png', dpi=300, bbox_inches='tight')
    fig_charges_interaction.savefig('./img/电荷相互作用.png', dpi=300, bbox_inches='tight')
    
    print("电荷定义方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")