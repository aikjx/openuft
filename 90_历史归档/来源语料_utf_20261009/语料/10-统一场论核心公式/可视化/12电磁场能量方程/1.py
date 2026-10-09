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
教科书级别：电磁场能量方程可视化
方程：W = k × (1/2) × (E² + B²) × V

参数说明（教科书级别）：
- W：电磁场能量
- k：比例常数
- E：电场强度
- B：磁感应强度
- V：体积
"""

class ElectromagneticEnergyEquation:
    """电磁场能量方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.k = 1.0  # 比例常数，实际应用中需根据单位制确定
        self.E_base = 1.0  # 基础电场强度，单位：V/m
        self.B_base = 1.0  # 基础磁感应强度，单位：T
        self.V_base = 1.0  # 基础体积，单位：m³
    
    def calculate_energy(self, E=None, B=None, V=None):
        """计算电磁场能量
        W = k × (1/2) × (E² + B²) × V
        """
        # 使用默认值或传入值
        E_val = self.E_base if E is None else E
        B_val = self.B_base if B is None else B
        V_val = self.V_base if V is None else V
        
        # 计算电场能量密度
        energy_density_electric = 0.5 * self.k * E_val**2
        
        # 计算磁场能量密度
        energy_density_magnetic = 0.5 * self.k * B_val**2
        
        # 计算总能量
        total_energy = (energy_density_electric + energy_density_magnetic) * V_val
        
        return total_energy, energy_density_electric, energy_density_magnetic
    
    def visualize_energy_vs_fields(self):
        """可视化能量与电磁场强度的关系"""
        # 创建电场强度和磁感应强度的范围
        E_range = np.linspace(0, 3*self.E_base, 100)
        B_range = np.linspace(0, 3*self.B_base, 100)
        
        # 计算不同场强下的能量
        total_energies = []
        electric_energies = []
        magnetic_energies = []
        
        for E in E_range:
            total_energy, electric_energy, magnetic_energy = self.calculate_energy(E=E, B=E)  # 假设E=B以简化可视化
            total_energies.append(total_energy)
            electric_energies.append(electric_energy * self.V_base)
            magnetic_energies.append(magnetic_energy * self.V_base)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制总能量和分量能量
        ax.plot(E_range, total_energies, 'k-', linewidth=2.5, label='总电磁场能量')
        ax.plot(E_range, electric_energies, 'r-', linewidth=1.5, label='电场能量')
        ax.plot(E_range, magnetic_energies, 'b-', linewidth=1.5, label='磁场能量')
        
        # 设置标题和标签
        ax.set_title('电磁场能量与场强的关系', fontsize=16)
        ax.set_xlabel('场强 (相对单位)', fontsize=14)
        ax.set_ylabel('能量 (相对单位)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def visualize_energy_surface(self):
        """3D可视化能量随电场和磁场强度的变化曲面"""
        # 创建电场强度和磁感应强度的网格
        E_range = np.linspace(0, 3*self.E_base, 50)
        B_range = np.linspace(0, 3*self.B_base, 50)
        E, B = np.meshgrid(E_range, B_range)
        
        # 计算总能量
        total_energy = 0.5 * self.k * (E**2 + B**2) * self.V_base
        
        # 创建图形
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制3D曲面
        surf = ax.plot_surface(E, B, total_energy, cmap=cm.viridis, 
                             linewidth=0, antialiased=True, alpha=0.8)
        
        # 添加颜色条
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('总电磁场能量', fontsize=12)
        
        # 设置标题和标签
        ax.set_title('电磁场能量随电场和磁场强度的变化', fontsize=16)
        ax.set_xlabel('电场强度 E', fontsize=12)
        ax.set_ylabel('磁感应强度 B', fontsize=12)
        ax.set_zlabel('总能量 W', fontsize=12)
        
        return fig
    
    def visualize_energy_density_comparison(self):
        """可视化电场和磁场能量密度的对比"""
        # 创建不同场强组合的情况
        cases = [
            {'name': '纯电场', 'E': 2.0, 'B': 0.0},
            {'name': '纯磁场', 'E': 0.0, 'B': 2.0},
            {'name': '电场主导', 'E': 2.0, 'B': 1.0},
            {'name': '磁场主导', 'E': 1.0, 'B': 2.0},
            {'name': '相等场强', 'E': 2.0, 'B': 2.0}
        ]
        
        # 计算每种情况下的能量密度
        labels = [case['name'] for case in cases]
        electric_energy_densities = []
        magnetic_energy_densities = []
        
        for case in cases:
            _, electric_density, magnetic_density = self.calculate_energy(
                E=case['E'], B=case['B'], V=1.0)  # V=1.0时，能量等于能量密度
            electric_energy_densities.append(electric_density)
            magnetic_energy_densities.append(magnetic_density)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 设置条形图位置
        x = np.arange(len(labels))
        width = 0.35
        
        # 绘制条形图
        rects1 = ax.bar(x - width/2, electric_energy_densities, width, label='电场能量密度')
        rects2 = ax.bar(x + width/2, magnetic_energy_densities, width, label='磁场能量密度')
        
        # 设置标题和标签
        ax.set_title('不同场强组合下的能量密度对比', fontsize=16)
        ax.set_xlabel('场强组合情况', fontsize=14)
        ax.set_ylabel('能量密度 (相对单位)', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        
        # 添加数值标签
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{:.2f}'.format(height),
                           xy=(rect.get_x() + rect.get_width() / 2, height),
                           xytext=(0, 3),  # 3点垂直偏移
                           textcoords="offset points",
                           ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        
        # 调整布局
        fig.tight_layout()
        
        return fig
    
    def visualize_energy_conservation(self):
        """可视化能量守恒关系"""
        # 创建场强变化
        t = np.linspace(0, 10, 100)
        
        # 定义电场和磁场随时间变化的函数（满足能量守恒）
        E = self.E_base * np.sin(t)
        B = np.sqrt(self.E_base**2 - E**2)
        
        # 计算总能量
        total_energy = 0.5 * self.k * (E**2 + B**2) * self.V_base
        
        # 创建图形
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 绘制电场和磁场随时间变化
        color = 'tab:red'
        ax1.set_xlabel('时间', fontsize=14)
        ax1.set_ylabel('场强', fontsize=14, color=color)
        ax1.plot(t, E, 'r-', linewidth=1.5, label='电场强度 E')
        ax1.plot(t, B, 'b-', linewidth=1.5, label='磁感应强度 B')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3)
        
        # 创建第二个y轴显示总能量
        ax2 = ax1.twinx()
        color = 'tab:green'
        ax2.set_ylabel('总能量', fontsize=14, color=color)
        ax2.plot(t, total_energy, 'g-', linewidth=2, label='总电磁场能量')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # 设置标题
        ax1.set_title('电磁场能量守恒关系', fontsize=16)
        
        # 合并图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        # 调整布局
        fig.tight_layout()
        
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
        params_text = "电磁场能量方程参数详解 (教科书级别):\n" + \
                      "W = k × (1/2) × (E² + B²) × V\n" + \
                      "\n参数含义:\n" + \
                      "- W: 电磁场能量，单位为焦耳(J)\n" + \
                      "- k: 比例常数，在真空中与介电常数ε₀和磁导率μ₀相关\n" + \
                      "- E: 电场强度矢量的大小，单位为伏特每米(V/m)\n" + \
                      "- B: 磁感应强度矢量的大小，单位为特斯拉(T)\n" + \
                      "- V: 包含电磁场的体积，单位为立方米(m³)\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程描述了电磁场中储存的总能量\n" + \
                      "- 电磁场能量由电场能量和磁场能量两部分组成\n" + \
                      "- 电场能量密度为(1/2)kE²，磁场能量密度为(1/2)kB²\n" + \
                      "- 在真空中，k=1/ε₀c²=μ₀/2，其中c是光速\n" + \
                      "- 方程体现了电场和磁场可以相互转化但总能量守恒\n" + \
                      "- 对于电磁波，电场能量和磁场能量相等，且以光速传播\n" + \
                      "- 该方程是统一场论中能量守恒的重要体现"
        
        # 在图形中添加参数说明文本框
        fig.text(0.02, 0.02, params_text, fontsize=10, 
                 verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建并显示可视化
if __name__ == "__main__":
# Ensure img directory exists
img_dir = './img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    # 创建电磁场能量方程可视化对象
    energy_eq = ElectromagneticEnergyEquation()
    
    # 显示能量与场强关系
    fig_energy_fields = energy_eq.visualize_energy_vs_fields()
    energy_eq.add_parameter_explanation(fig_energy_fields)
    
    # 显示能量变化曲面
    fig_energy_surface = energy_eq.visualize_energy_surface()
    energy_eq.add_parameter_explanation(fig_energy_surface)
    
    # 显示能量密度对比
    fig_energy_density = energy_eq.visualize_energy_density_comparison()
    energy_eq.add_parameter_explanation(fig_energy_density)
    
    # 显示能量守恒关系
    fig_conservation = energy_eq.visualize_energy_conservation()
    energy_eq.add_parameter_explanation(fig_conservation)
    
    # 添加方程到图形中
    equation_text = "电磁场能量方程: W = k × (1/2) × (E² + B²) × V"
    fig_energy_fields.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_energy_fields.savefig('./img/能量与场强关系.png', dpi=300, bbox_inches='tight')
    fig_energy_surface.savefig('./img/能量变化曲面.png', dpi=300, bbox_inches='tight')
    fig_energy_density.savefig('./img/能量密度对比.png', dpi=300, bbox_inches='tight')
    fig_conservation.savefig('./img/能量守恒关系.png', dpi=300, bbox_inches='tight')
    
    print("电磁场能量方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")