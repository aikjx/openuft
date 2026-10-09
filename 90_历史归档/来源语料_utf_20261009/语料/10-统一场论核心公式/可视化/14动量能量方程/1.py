import os
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"  # 解决负号显示问题
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

"""
教科书级别：动量能量方程可视化
方程：P = m(C - V)

参数说明（教科书级别）：
- P：动量矢量
- m：物体质量
- C：空间运动速度矢量（光速）
- V：物体运动速度矢量
"""

class MomentumEnergyEquation:
    """动量能量方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.m_base = 1.0   # 基础质量，单位：kg
    
    def calculate_momentum(self, mass=None, velocity=None):
        """计算动量
        P = m(C - V)
        假设C沿Z轴方向，V在XY平面内
        """
        # 使用默认值或传入值
        m = self.m_base if mass is None else mass
        
        # 如果没有传入速度，使用默认值
        if velocity is None:
            v_magnitude = 0.1 * self.c  # 默认速度为光速的10%
            v_direction = 0             # 默认方向沿X轴
            vx = v_magnitude * np.cos(v_direction)
            vy = v_magnitude * np.sin(v_direction)
            vz = 0
        else:
            # 假设传入的是速度矢量 [vx, vy, vz]
            vx, vy, vz = velocity
        
        # 定义空间运动速度矢量C（沿Z轴）
        cx, cy, cz = 0, 0, self.c
        
        # 计算动量分量
        px = m * (cx - vx)
        py = m * (cy - vy)
        pz = m * (cz - vz)
        
        return np.array([px, py, pz]), np.array([cx, cy, cz]), np.array([vx, vy, vz])
    
    def visualize_momentum_vectors(self):
        """可视化动量矢量、空间速度矢量和物体速度矢量的关系"""
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 为不同速度创建多个矢量图
        speeds = [0.0, 0.3, 0.6, 0.9]  # 物体速度与光速的比例
        colors = ['blue', 'green', 'orange', 'red']
        labels = [f'v = {speed}c' for speed in speeds]
        
        # 计算并绘制每个速度下的矢量
        for i, speed in enumerate(speeds):
            # 创建相对于光速的速度
            vx = speed * self.c
            vy = 0
            vz = 0
            velocity = [vx, vy, vz]
            
            # 计算动量和速度矢量
            momentum, c_vector, v_vector = self.calculate_momentum(velocity=velocity)
            
            # 偏移起点以便更好地可视化多个矢量
            offset = i * 0.5  # 轻微偏移
            
            # 绘制空间速度矢量C
            ax.quiver(offset, offset, offset, c_vector[0], c_vector[1], c_vector[2],
                     length=self.c * 0.00000001, color='black', linewidth=2, label=f'C (c={speed})' if i == 0 else "",
                     arrow_length_ratio=0.1)
            
            # 绘制物体速度矢量V
            ax.quiver(offset, offset, offset, v_vector[0], v_vector[1], v_vector[2],
                     length=self.c * 0.00000001, color=colors[i], linewidth=2, label=labels[i],
                     arrow_length_ratio=0.1)
            
            # 绘制动量矢量P
            ax.quiver(offset, offset, offset, momentum[0], momentum[1], momentum[2],
                     length=self.c * self.m_base * 0.00000000001, color=colors[i], linewidth=3, 
                     label=f'P ({speed}c)' if i == 0 else "", arrow_length_ratio=0.1, linestyle='--')
        
        # 设置标题和标签
        ax.set_title('动量矢量与速度的关系 (P = m(C - V))', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('Z坐标', fontsize=12)
        
        # 设置坐标轴范围
        limit = self.c * 0.00000001 * 1.2
        ax.set_xlim(-limit/2, limit*1.5)
        ax.set_ylim(-limit/2, limit*1.5)
        ax.set_zlim(-limit/2, limit*1.5)
        
        # 添加图例
        ax.legend()
        
        return fig
    
    def visualize_momentum_vs_velocity(self):
        """可视化动量大小与物体速度的关系"""
        # 创建速度范围（从0到接近光速）
        v_ratio = np.linspace(0, 0.99, 100)  # 物体速度与光速的比例
        v_values = v_ratio * self.c
        
        # 计算不同速度下的动量大小
        momentum_magnitudes = []
        
        for v in v_values:
            momentum, _, _ = self.calculate_momentum(velocity=[v, 0, 0])
            momentum_magnitude = np.linalg.norm(momentum)
            momentum_magnitudes.append(momentum_magnitude)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制动量-速度关系
        ax.plot(v_ratio, momentum_magnitudes, 'b-', linewidth=2.5)
        
        # 设置标题和标签
        ax.set_title('动量大小与物体速度的关系', fontsize=16)
        ax.set_xlabel('速度/光速 (v/c)', fontsize=14)
        ax.set_ylabel('动量大小 (kg·m/s)', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加关键点标记
        key_v_ratios = [0.0, 0.3, 0.6, 0.9]
        for v_ratio_key in key_v_ratios:
            idx = np.argmin(np.abs(v_ratio - v_ratio_key))
            ax.scatter(v_ratio[idx], momentum_magnitudes[idx], color='red', s=80, zorder=5)
            ax.annotate(f'{v_ratio_key}c',
                       xy=(v_ratio[idx], momentum_magnitudes[idx]),
                       xytext=(v_ratio[idx]+0.02, momentum_magnitudes[idx]*0.8),
                       arrowprops=dict(facecolor='black', shrink=0.05, width=1),
                       fontsize=10)
        
        return fig
    
    def visualize_3d_momentum_space(self):
        """3D可视化动量空间"""
        # 创建速度网格（在XY平面内）
        vx_ratio = np.linspace(-0.5, 0.5, 20)  # X方向速度与光速的比例
        vy_ratio = np.linspace(-0.5, 0.5, 20)  # Y方向速度与光速的比例
        VX, VY = np.meshgrid(vx_ratio, vy_ratio)
        
        # 计算动量分量
        PX = np.zeros_like(VX)
        PY = np.zeros_like(VY)
        PZ = np.zeros_like(VX)
        
        for i in range(len(vx_ratio)):
            for j in range(len(vy_ratio)):
                vx = VX[i, j] * self.c
                vy = VY[i, j] * self.c
                momentum, _, _ = self.calculate_momentum(velocity=[vx, vy, 0])
                PX[i, j], PY[i, j], PZ[i, j] = momentum
        
        # 计算动量大小
        P_magnitude = np.sqrt(PX**2 + PY**2 + PZ**2)
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制3D动量表面
        surf = ax.plot_surface(PX * 1e-8, PY * 1e-8, PZ * 1e-8, 
                              facecolors=cm.viridis(P_magnitude / np.max(P_magnitude)),
                              linewidth=0, antialiased=True, alpha=0.8)
        
        # 添加颜色条
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('动量大小', fontsize=12)
        
        # 设置标题和标签
        ax.set_title('3D动量空间可视化', fontsize=16)
        ax.set_xlabel('PX × 10⁸ (kg·m/s)', fontsize=12)
        ax.set_ylabel('PY × 10⁸ (kg·m/s)', fontsize=12)
        ax.set_zlabel('PZ × 10⁸ (kg·m/s)', fontsize=12)
        
        return fig
    
    def visualize_momentum_components(self):
        """可视化动量分量与速度的关系"""
        # 创建速度范围（从0到接近光速）
        v_ratio = np.linspace(0, 0.99, 100)  # 物体速度与光速的比例
        v_values = v_ratio * self.c
        
        # 计算不同速度下的动量分量
        px_values = []
        py_values = []
        pz_values = []
        
        for v in v_values:
            # 让速度沿45度方向，这样会影响多个动量分量
            vx = v * np.cos(np.pi/4)
            vy = v * np.sin(np.pi/4)
            momentum, _, _ = self.calculate_momentum(velocity=[vx, vy, 0])
            px, py, pz = momentum
            px_values.append(px)
            py_values.append(py)
            pz_values.append(pz)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制动量分量
        ax.plot(v_ratio, px_values, 'r-', linewidth=1.5, label='PX分量')
        ax.plot(v_ratio, py_values, 'g-', linewidth=1.5, label='PY分量')
        ax.plot(v_ratio, pz_values, 'b-', linewidth=1.5, label='PZ分量')
        
        # 设置标题和标签
        ax.set_title('动量分量与物体速度的关系', fontsize=16)
        ax.set_xlabel('速度/光速 (v/c)', fontsize=14)
        ax.set_ylabel('动量分量 (kg·m/s)', fontsize=14)
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
            """添加专业级别的参数解释文本框"""
        params_text = "动量能量方程参数详解 (教科书级别):\n" + \
                      "P = m(C - V)\n" + \
                      "\n参数含义:\n" + \
                      "- P: 物体的动量矢量，单位为千克·米/秒(kg·m/s)\n" + \
                      "- m: 物体的质量，单位为千克(kg)\n" + \
                      "- C: 空间运动速度矢量（光速），大小为c=299,792,458米/秒\n" + \
                      "- V: 物体相对于观察者的运动速度矢量\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了动量的本质是质量乘以空间运动速度与物体运动速度的差值\n" + \
                      "- 体现了统一场论中空间运动与物体运动的关系\n" + \
                      "- 当物体静止时(V=0)，动量为P = mC，即静止动量\n" + \
                      "- 当物体运动时，动量会减小，因为C-V的差值减小\n" + \
                      "- 动量的方向由(C-V)的方向决定\n" + \
                      "- 该方程是统一场论中动量定义的核心表达式\n" + \
                      "- 与相对论动量公式相比，该方程提供了更本质的动量定义"
        
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
    
    # 创建动量能量方程可视化对象
    momentum_eq = MomentumEnergyEquation()
    
    # 显示动量矢量可视化
    fig_vectors = momentum_eq.visualize_momentum_vectors()
    momentum_eq.add_parameter_explanation(fig_vectors)
    
    # 显示动量-速度关系
    fig_momentum_velocity = momentum_eq.visualize_momentum_vs_velocity()
    momentum_eq.add_parameter_explanation(fig_momentum_velocity)
    
    # 显示3D动量空间
    fig_3d = momentum_eq.visualize_3d_momentum_space()
    momentum_eq.add_parameter_explanation(fig_3d)
    
    # 显示动量分量与速度的关系
    fig_components = momentum_eq.visualize_momentum_components()
    momentum_eq.add_parameter_explanation(fig_components)
    
    # 添加方程到图形中
    equation_text = "动量能量方程: P = m(C - V)"
    fig_momentum_velocity.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_vectors.savefig('./img/动量矢量可视化.png', dpi=300, bbox_inches='tight')
    fig_momentum_velocity.savefig('./img/动量-速度关系.png', dpi=300, bbox_inches='tight')
    fig_3d.savefig('./img/3D动量空间.png', dpi=300, bbox_inches='tight')
    fig_components.savefig('./img/动量分量与速度关系.png', dpi=300, bbox_inches='tight')
    
    print("动量能量方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")