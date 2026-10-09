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
教科书级别：宇宙大统一方程（力方程）可视化
方程：F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)

参数说明（教科书级别）：
- F：力矢量
- P：动量矢量
- m：物体质量
- C：空间运动速度矢量（光速）
- V：物体运动速度矢量
- t：时间
"""

class UnifiedForceEquation:
    """宇宙大统一方程（力方程）可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.base_mass = 1.0  # 基础质量，单位：kg
        
    def calculate_force_components(self, t, mass_rate=0.1, C_rate=0.0, V_rate=1000.0):
        """计算大统一方程中的各分力
        F = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)
        这里假设C沿Z轴方向，V沿X轴方向随时间线性变化
        """
        # 定义质量随时间变化
        m = self.base_mass + mass_rate * t
        
        # 定义空间运动速度矢量C（沿Z轴方向，假设随时间有小变化）
        C = np.array([0, 0, self.c + C_rate * t])
        
        # 定义物体运动速度矢量V（沿X轴方向，随时间线性变化）
        V = np.array([V_rate * t, 0, 0])
        
        # 计算各分力
        dP_dt1 = C * mass_rate  # C(dm/dt)
        dP_dt2 = -V * mass_rate  # -V(dm/dt)
        dP_dt3 = m * np.array([0, 0, C_rate])  # m(dC/dt)
        dP_dt4 = -m * np.array([V_rate, 0, 0])  # -m(dV/dt)
        
        # 总力
        total_force = dP_dt1 + dP_dt2 + dP_dt3 + dP_dt4
        
        return total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4
    
    def visualize_force_components(self):
        """可视化大统一方程中的各分力随时间的变化"""
        # 生成时间数据
        t = np.linspace(0, 10, 100)  # s
        
        # 存储各分力和总力的数据
        total_forces = []
        components = [[], [], [], []]  # 四个分力
        
        for time in t:
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4 = self.calculate_force_components(time)
            total_forces.append(total_force)
            components[0].append(dP_dt1)
            components[1].append(dP_dt2)
            components[2].append(dP_dt3)
            components[3].append(dP_dt4)
        
        # 转换为numpy数组便于处理
        total_forces = np.array(total_forces)
        components = np.array(components)
        
        # 创建图形
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('宇宙大统一方程（力方程）各分力随时间的变化', fontsize=16)
        
        # 绘制总力的三个分量
        axes[0, 0].plot(t, total_forces[:, 0], 'r-', linewidth=2)
        axes[0, 0].set_title('总力 X分量', fontsize=14)
        axes[0, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[0, 0].set_ylabel('力 (N)', fontsize=12)
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[0, 1].plot(t, total_forces[:, 1], 'g-', linewidth=2)
        axes[0, 1].set_title('总力 Y分量', fontsize=14)
        axes[0, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[0, 1].set_ylabel('力 (N)', fontsize=12)
        axes[0, 1].grid(True, alpha=0.3)
        
        axes[1, 0].plot(t, total_forces[:, 2], 'b-', linewidth=2)
        axes[1, 0].set_title('总力 Z分量', fontsize=14)
        axes[1, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[1, 0].set_ylabel('力 (N)', fontsize=12)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 绘制四个分力的Z分量（主要贡献者）
        axes[1, 1].plot(t, components[0, :, 2], 'r-', linewidth=1.5, label='C(dm/dt)')
        axes[1, 1].plot(t, components[2, :, 2], 'g-', linewidth=1.5, label='m(dC/dt)')
        axes[1, 1].set_title('Z方向分力贡献', fontsize=14)
        axes[1, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[1, 1].set_ylabel('力 (N)', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        # 绘制四个分力的X分量
        axes[2, 0].plot(t, components[1, :, 0], 'b-', linewidth=1.5, label='-V(dm/dt)')
        axes[2, 0].plot(t, components[3, :, 0], 'm-', linewidth=1.5, label='-m(dV/dt)')
        axes[2, 0].set_title('X方向分力贡献', fontsize=14)
        axes[2, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 0].set_ylabel('力 (N)', fontsize=12)
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        # 绘制总力大小随时间变化
        total_force_magnitudes = np.linalg.norm(total_forces, axis=1)
        axes[2, 1].plot(t, total_force_magnitudes, 'k-', linewidth=2)
        axes[2, 1].set_title('总力大小', fontsize=14)
        axes[2, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 1].set_ylabel('力 (N)', fontsize=12)
        axes[2, 1].grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        
        return fig
    
    def visualize_force_vectors(self):
        """在特定时间点可视化各分力和总力的矢量表示"""
        # 选择几个关键时间点
        time_points = [1, 5, 10]  # s
        
        # 创建图形
        fig = plt.figure(figsize=(15, 10))
        
        # 为每个时间点创建一个子图
        for i, time in enumerate(time_points):
            ax = fig.add_subplot(1, len(time_points), i+1, projection='3d')
            
            # 设置坐标轴范围
            max_force = 5e7  # 根据计算结果调整
            ax.set_xlim([-max_force, max_force])
            ax.set_ylim([-max_force, max_force])
            ax.set_zlim([-max_force, max_force])
            
            # 设置坐标轴标签
            ax.set_xlabel('X轴', fontsize=12)
            ax.set_ylabel('Y轴', fontsize=12)
            ax.set_zlabel('Z轴', fontsize=12)
            
            # 设置标题
            ax.set_title(f'力矢量分解 (t={time}s)', fontsize=14)
            
            # 计算各分力
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4 = self.calculate_force_components(time)
            
            # 绘制各分力矢量
            ax.quiver(0, 0, 0, dP_dt1[0], dP_dt1[1], dP_dt1[2],
                     color='red', linewidth=2, label='C(dm/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt2[0], dP_dt2[1], dP_dt2[2],
                     color='blue', linewidth=2, label='-V(dm/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt3[0], dP_dt3[1], dP_dt3[2],
                     color='green', linewidth=2, label='m(dC/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt4[0], dP_dt4[1], dP_dt4[2],
                     color='purple', linewidth=2, label='-m(dV/dt)', arrow_length_ratio=0.1)
            
            # 绘制总力矢量
            ax.quiver(0, 0, 0, total_force[0], total_force[1], total_force[2],
                     color='black', linewidth=3, label='总力 F', arrow_length_ratio=0.1)
            
            # 添加图例
            ax.legend(loc='upper right')
        
        # 调整布局
        plt.tight_layout()
        
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
        params_text = "宇宙大统一方程（力方程）参数详解 (教科书级别):\n" + \
                      "F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)\n" + \
                      "\n各分量意义:\n" + \
                      "1. C(dm/dt): 空间运动速度与质量变化率的乘积，反映质量变化引起的力\n" + \
                      "2. -V(dm/dt): 物体运动速度与质量变化率的乘积的负值\n" + \
                      "3. m(dC/dt): 质量与空间运动加速度的乘积\n" + \
                      "4. -m(dV/dt): 质量与物体运动加速度的乘积的负值（牛顿第二定律项）\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程统一描述了各种力的本质，是统一场论的核心方程\n" + \
                      "- 揭示了力不仅来自于物体的加速度，还来自于质量变化和空间运动变化\n" + \
                      "- 牛顿第二定律(F = ma)是该方程在特定条件下的近似\n" + \
                      "- 当质量不变(dm/dt=0)且空间运动均匀(dC/dt=0)时，\n" + \
                      "  方程简化为F = -m(dV/dt)，即F = ma（符号差异源于参考系）\n" + \
                      "- 该方程为理解引力、电磁力等各种力的统一本质提供了框架"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建宇宙大统一方程可视化对象
    unified_eq = UnifiedForceEquation()
    
    # 显示力分量随时间变化可视化
    fig_time_evolution = unified_eq.visualize_force_components()
    unified_eq.add_parameter_explanation(fig_time_evolution)
    
    # 显示力矢量分解可视化
    fig_vector_decomposition = unified_eq.visualize_force_vectors()
    unified_eq.add_parameter_explanation(fig_vector_decomposition)
    
    # 添加方程到图形中
    equation_text = "宇宙大统一方程（力方程）: F = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)"
    fig_time_evolution.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_time_evolution.savefig('./img/力分量随时间变化.png', dpi=300, bbox_inches='tight')
    fig_vector_decomposition.savefig('./img/力矢量分解.png', dpi=300, bbox_inches='tight')
    
    print("宇宙大统一方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")