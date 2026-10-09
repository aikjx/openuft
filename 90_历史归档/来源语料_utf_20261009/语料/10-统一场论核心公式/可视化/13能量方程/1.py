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
教科书级别：能量方程可视化
方程：E = mC²

参数说明（教科书级别）：
- E：能量
- m：物体质量
- C：光速
"""

class EnergyEquation:
    """能量方程可视化类"""
    
    def __init__(self):
        """初始化参数"""
        self.c = 299792458  # 光速，单位：m/s
        self.m_base = 1.0  # 基础质量，单位：kg
    
    def calculate_energy(self, mass=None):
        """计算能量
        E = mC²
        """
        # 使用默认值或传入值
        m = self.m_base if mass is None else mass
        
        # 计算能量
        energy = m * self.c**2
        
        return energy
    
    def visualize_energy_vs_mass(self):
        """可视化能量与质量的关系"""
        # 创建质量范围
        mass_range = np.linspace(0, 10*self.m_base, 100)
        
        # 计算不同质量下的能量
        energies = [self.calculate_energy(mass) for mass in mass_range]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制能量-质量关系
        ax.plot(mass_range, energies, 'b-', linewidth=2.5)
        
        # 设置标题和标签
        ax.set_title('质能关系 (E = mc²)', fontsize=16)
        ax.set_xlabel('质量 (kg)', fontsize=14)
        ax.set_ylabel('能量 (J)', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点（1kg质量对应的能量）
        mass_1kg = 1.0
        energy_1kg = self.calculate_energy(mass_1kg)
        ax.scatter(mass_1kg, energy_1kg, color='red', s=100, zorder=5)
        ax.annotate(f'1 kg 对应能量: {energy_1kg:.2e} J',
                   xy=(mass_1kg, energy_1kg),
                   xytext=(1.2, energy_1kg * 0.7),
                   arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                   fontsize=12)
        
        return fig
    
    def visualize_log_scale(self):
        """以对数刻度可视化能量与质量的关系"""
        # 创建质量范围（对数分布）
        mass_range = np.logspace(-30, 1, 100)  # 从10^-30 kg到10 kg
        
        # 计算不同质量下的能量
        energies = [self.calculate_energy(mass) for mass in mass_range]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制对数刻度的能量-质量关系
        ax.loglog(mass_range, energies, 'b-', linewidth=2.5)
        
        # 设置标题和标签
        ax.set_title('质能关系 (对数刻度)', fontsize=16)
        ax.set_xlabel('质量 (kg)', fontsize=14)
        ax.set_ylabel('能量 (J)', fontsize=14)
        ax.grid(True, which="both", alpha=0.3)
        
        # 添加一些物理参考点
        # 电子质量 (9.1093837015×10^-31 kg)
        electron_mass = 9.1093837015e-31
        electron_energy = self.calculate_energy(electron_mass)
        ax.scatter(electron_mass, electron_energy, color='red', s=50, zorder=5)
        ax.annotate('电子', xy=(electron_mass, electron_energy),
                   xytext=(electron_mass*2, electron_energy*5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        # 质子质量 (1.67262192369×10^-27 kg)
        proton_mass = 1.67262192369e-27
        proton_energy = self.calculate_energy(proton_mass)
        ax.scatter(proton_mass, proton_energy, color='green', s=50, zorder=5)
        ax.annotate('质子', xy=(proton_mass, proton_energy),
                   xytext=(proton_mass*2, proton_energy*5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        # 1kg质量
        mass_1kg = 1.0
        energy_1kg = self.calculate_energy(mass_1kg)
        ax.scatter(mass_1kg, energy_1kg, color='blue', s=50, zorder=5)
        ax.annotate('1 kg', xy=(mass_1kg, energy_1kg),
                   xytext=(mass_1kg*2, energy_1kg*0.5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        return fig
    
    def visualize_energy_comparison(self):
        """可视化不同质量下的能量对比"""
        # 创建常见物体的质量列表（kg）
        masses = {
            '电子': 9.1093837015e-31,
            '质子': 1.67262192369e-27,
            '碳原子': 1.9944235e-26,
            '红细胞': 9e-14,
            '尘埃颗粒': 1e-9,
            '纸张': 5e-5,
            '硬币': 0.005,
            '苹果': 0.15,
            '笔记本电脑': 2.0,
            '人体': 70.0,
            '汽车': 1500.0,
            '大象': 5000.0
        }
        
        # 计算对应能量
        labels = list(masses.keys())
        energy_values = [self.calculate_energy(mass) for mass in masses.values()]
        
        # 将能量转换为对数刻度以便比较
        log_energies = np.log10(energy_values)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 设置条形图位置
        y_pos = np.arange(len(labels))
        
        # 绘制水平条形图
        bars = ax.barh(y_pos, log_energies, align='center', alpha=0.7)
        
        # 设置不同颜色以便区分
        colors = cm.rainbow(np.linspace(0, 1, len(labels)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # 设置标题和标签
        ax.set_title('不同质量物体的能量对比 (E = mc²)', fontsize=16)
        ax.set_xlabel('能量的对数 (log₁₀(E))', fontsize=14)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        
        # 添加数值标签（科学计数法）
        for i, v in enumerate(energy_values):
            exponent = int(np.floor(np.log10(v)))
            coeff = v / (10**exponent)
            label = f'{coeff:.2f}×10^{exponent}'
            ax.text(log_energies[i] + 0.1, i, label, va='center', fontsize=10)
        
        # 调整布局
        fig.tight_layout()
        
        return fig
    
    def visualize_nuclear_reactions(self):
        """可视化核反应中的质量能量转换"""
        # 核反应示例：氘+氚→氦+中子
        # 质量数据（kg）
        mass_deuterium = 3.34449437e-27  # 氘
        mass_tritium = 5.00826743e-27    # 氚
        mass_helium = 6.64465733e-27     # 氦-4
        mass_neutron = 1.67492749804e-27 # 中子
        
        # 计算反应前后的总质量
        mass_before = mass_deuterium + mass_tritium
        mass_after = mass_helium + mass_neutron
        
        # 计算质量亏损和释放的能量
        mass_defect = mass_before - mass_after
        energy_released = self.calculate_energy(mass_defect)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 设置条形图位置
        x = np.array([0, 1])
        width = 0.35
        
        # 绘制反应前后的质量
        ax.bar(x[0] - width/2, mass_before, width, label='反应前总质量')
        ax.bar(x[0] + width/2, mass_after, width, label='反应后总质量')
        
        # 绘制释放的能量
        ax.bar(x[1], energy_released, width, color='red', label='释放的能量')
        
        # 设置双Y轴
        ax2 = ax.twinx()
        ax2.set_ylabel('能量 (J)', fontsize=14)
        
        # 为第二个Y轴设置相同的条形高度
        ax2.bar(x[1], energy_released, width, color='red', alpha=0)
        
        # 设置标题和标签
        ax.set_title('核反应中的质量能量转换', fontsize=16)
        ax.set_xlabel('反应阶段', fontsize=14)
        ax.set_ylabel('质量 (kg)', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(['质量对比', '释放能量'])
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(loc='upper left')
        
        # 添加数值标签
        ax.text(x[0] - width/2, mass_before, f'{mass_before:.4e} kg', ha='center', va='bottom')
        ax.text(x[0] + width/2, mass_after, f'{mass_after:.4e} kg', ha='center', va='bottom')
        ax2.text(x[1], energy_released, f'{energy_released:.4e} J', ha='center', va='bottom')
        
        # 添加质量亏损说明
        ax.text(0.5, 0.5*mass_before, 
                f'质量亏损: {mass_defect:.4e} kg\n对应能量: {energy_released:.4e} J', 
                ha='center', va='center', 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontsize=12)
        
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
            """添加专业级别的参数解释文本框"""
        params_text = "能量方程参数详解 (教科书级别):\n" + \
                      "E = mC²\n" + \
                      "\n参数含义:\n" + \
                      "- E: 物体所蕴含的总能量，单位为焦耳(J)\n" + \
                      "- m: 物体的质量，单位为千克(kg)\n" + \
                      "- C: 真空中的光速，约为299,792,458米/秒(m/s)\n" + \
                      "\n物理意义:\n" + \
                      "- 该方程揭示了质量和能量的等价性和可转换性\n" + \
                      "- 任何有质量的物体都蕴含着巨大的能量\n" + \
                      "- 能量和质量是同一物理实体的不同表现形式\n" + \
                      "- 能量变化必然伴随质量变化，反之亦然\n" + \
                      "- 核反应中释放的能量来源于核子结合能对应的质量亏损\n" + \
                      "- 该方程是统一场论中的核心方程之一\n" + \
                      "- 方程表明能量守恒和质量守恒实际上是统一的能量-质量守恒定律"
        
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
    
    # 创建能量方程可视化对象
    energy_eq = EnergyEquation()
    
    # 显示能量与质量关系
    fig_energy_mass = energy_eq.visualize_energy_vs_mass()
    energy_eq.add_parameter_explanation(fig_energy_mass)
    
    # 显示对数刻度关系
    fig_log = energy_eq.visualize_log_scale()
    energy_eq.add_parameter_explanation(fig_log)
    
    # 显示不同物体的能量对比
    fig_comparison = energy_eq.visualize_energy_comparison()
    energy_eq.add_parameter_explanation(fig_comparison)
    
    # 显示核反应中的质量能量转换
    fig_nuclear = energy_eq.visualize_nuclear_reactions()
    energy_eq.add_parameter_explanation(fig_nuclear)
    
    # 添加方程到图形中
    equation_text = "能量方程: E = mC²"
    fig_energy_mass.text(0.5, 0.01, equation_text, ha='center', fontsize=14, 
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # 保存图形为PNG文件
    fig_energy_mass.savefig('./img/能量与质量关系.png', dpi=300, bbox_inches='tight')
    fig_log.savefig('./img/对数刻度能量关系.png', dpi=300, bbox_inches='tight')
    fig_comparison.savefig('./img/不同物体能量对比.png', dpi=300, bbox_inches='tight')
    fig_nuclear.savefig('./img/核反应质量能量转换.png', dpi=300, bbox_inches='tight')
    
    print("能量方程可视化已保存为PNG文件")
    
    # 在交互式环境中显示图形
    try:
        plt.show()
    except:
        print("在非交互式环境中运行，图形已保存但不显示")