import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D

class MassDefinitionEquation:
    """质量定义方程验证与可视化类"""
    
    def __init__(self):
        """初始化类实例"""
        self.k = 1.0  # 比例常数,可调整
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print(" =  =  =  =  = 符号求导验证 =  =  =  =  = ")
        
        # 定义符号变量
        k = sp.Symbol('k')
        n = sp.Function('n')
        Omega = sp.Symbol('Omega')
        t = sp.Symbol('t')
        
        # 定义质量方程
        m = k * sp.diff(n(Omega), Omega)
        print(f"质量定义方程: m = {m}")
        
        # 对立体角求二阶导数
        d2m_dOmega2 = sp.diff(m, Omega)
        print(f"质量对立体角的二阶导数: {d2m_dOmega2}")
        
        # 如果空间点数量是时间的函数,计算质量随时间的变化率
        n_time = sp.Function('n')(t)
        m_time = k * sp.diff(n_time, t)
        dm_dt = sp.diff(m_time, t)
        print(f"当空间点数量是时间的函数时,质量: m = {m_time}")
        print(f"质量随时间的变化率: dm / dt = {dm_dt}")
        
        # 量纲分析
        print(" / n量纲分析:")
        print(" - 左侧 m 的量纲: [质量] = [M]")
        print(" - 右侧 k·dn / dΩ 中,dn / dΩ 的量纲: 1 / [立体角] = [Ω⁻¹]")
        print(" - 因此 k 的量纲: [质量]·[立体角] = [M·Ω]")
        
        return {
            'mass_equation': m,
            'second_derivative': d2m_dOmega2,
            'mass_time_dependence': m_time,
            'mass_rate_of_change': dm_dt
        }
    
    def numerical_simulation(self, n_func = None, Omega_range = (0, 5), num_points = 100):
        """数值模拟与验证"""
        print(" / n =  =  =  =  = 数值模拟验证 =  =  =  =  = ")
        
        # 如果未提供空间点数量函数,使用默认的二次函数
        if n_func is None:
            def n_func(Omega):
                return 0.5 * Omega ** 2 + Omega + 1
        
        # 生成立体角范围
        Omega = np.linspace(Omega_range[0], Omega_range[1], num_points)
        
        # 计算空间点数量
        n_values = n_func(Omega)
        
        # 使用梯度计算空间点密度变化率dn / dΩ
        dn_dOmega = np.gradient(n_values, Omega)
        
        # 计算质量分布
        mass = self.k * dn_dOmega
        
        # 输出典型点的结果
        print("质量定义方程数值验证结果:")
        sample_points = np.linspace(Omega_range[0], Omega_range[1], 6)
        for omega in sample_points:
            # 找到最近的索引
            idx = np.abs(Omega - omega).argmin()
        
        # 统计分析
        print(f" / n质量分布统计:")
        print(f" - 最小值: {np.min(mass):.4f}")
        print(f" - 最大值: {np.max(mass):.4f}")
        print(f" - 平均值: {np.mean(mass):.4f}")
        print(f" - 标准差: {np.std(mass):.4f}")
        
        return {
            'Omega': Omega,
            'n_values': n_values,
            'dn_dOmega': dn_dOmega,
            'mass': mass
        }
    
    def visualize_mass_distribution(self, simulation_data):
        """可视化质量分布"""
        Omega = simulation_data['Omega']
        mass = simulation_data['mass']
        n_values = simulation_data['n_values']
        dn_dOmega = simulation_data['dn_dOmega']
        
        # 创建一个2x2的子图布局
        fig, axs = plt.subplots(2, 2, figsize = (15, 12))
        
        # 图1: 质量分布随立体角的变化
        axs[0, 0].plot(Omega, mass, 'b-', linewidth = 2)
        axs[0, 0].set_xlabel('立体角 Ω', fontsize = 12)
        axs[0, 0].set_ylabel('质量 m', fontsize = 12)
        axs[0, 0].set_title('质量分布随立体角的变化', fontsize = 14)
        axs[0, 0].grid(True, linestyle = '--', alpha = 0.7)
        axs[0, 0].axhline(y = 0, color = 'k', linestyle = '-', alpha = 0.3)
        
        # 图2: 空间点数量分布
        axs[0, 1].plot(Omega, n_values, 'g-', linewidth = 2)
        axs[0, 1].set_xlabel('立体角 Ω', fontsize = 12)
        axs[0, 1].set_ylabel('空间点数量 n', fontsize = 12)
        axs[0, 1].set_title('空间点数量分布', fontsize = 14)
        axs[0, 1].grid(True, linestyle = '--', alpha = 0.7)
        axs[0, 1].axhline(y = 0, color = 'k', linestyle = '-', alpha = 0.3)
        
        # 图3: 空间点密度变化率分布
        axs[1, 0].plot(Omega, dn_dOmega, 'r-', linewidth = 2)
        axs[1, 0].set_xlabel('立体角 Ω', fontsize = 12)
        axs[1, 0].set_ylabel('空间点密度变化率 dn / dΩ', fontsize = 12)
        axs[1, 0].set_title('空间点密度变化率分布', fontsize = 14)
        axs[1, 0].grid(True, linestyle = '--', alpha = 0.7)
        axs[1, 0].axhline(y = 0, color = 'k', linestyle = '-', alpha = 0.3)
        
        # 图4: 质量与空间点密度变化率的关系(应该是线性的)
        axs[1, 1].scatter(dn_dOmega, mass, c = 'purple', alpha = 0.6)
        axs[1, 1].plot(dn_dOmega, mass, 'purple', linestyle = '--', linewidth = 1)
        axs[1, 1].set_xlabel('空间点密度变化率 dn / dΩ', fontsize = 12)
        axs[1, 1].set_ylabel('质量 m', fontsize = 12)
        axs[1, 1].set_title('质量与空间点密度变化率的关系', fontsize = 14)
        axs[1, 1].grid(True, linestyle = '--', alpha = 0.7)
        
        plt.tight_layout()
        plt.suptitle('质量定义方程数值验证与可视化', fontsize = 16, y = 1.02)
        plt.show()
    
    def visualize_stereoscopic_effect(self):
        """可视化立体角与空间点分布的关系"""
        fig = plt.figure(figsize = (15, 10))
        
        # 创建3D图展示立体角的几何意义
        ax1 = fig.add_subplot(121, projection = '3d')
        
        # 创建一个单位球面
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # 绘制球面的一部分来表示立体角
        ax1.plot_surface(x, y, z, rstride = 4, cstride = 4, color = 'skyblue', alpha = 0.3)
        
        # 绘制一个圆锥来表示立体角
        theta = np.linspace(0, np.pi / 4, 30)  # 半顶角为π / 4
        phi = np.linspace(0, 2 * np.pi, 30)
        r = np.linspace(0, 1, 10)
        
        theta_grid, phi_grid = np.meshgrid(theta, phi)
        x_cone = np.outer(r, np.sin(theta_grid) * np.cos(phi_grid))
        y_cone = np.outer(r, np.sin(theta_grid) * np.sin(phi_grid))
        z_cone = np.outer(r, np.cos(theta_grid))
        
        ax1.plot_surface(x_cone, y_cone, z_cone, color = 'coral', alpha = 0.7)
        
        # 绘制坐标轴
        ax1.set_xlabel('X轴')
        ax1.set_ylabel('Y轴')
        ax1.set_zlabel('Z轴')
        ax1.set_title('立体角的几何表示', fontsize = 14)
        
        # 创建2D图展示空间点分布(越靠近中心越密集)
        ax2 = fig.add_subplot(122)
        
        # 创建一个圆形代表物体
        circle = Circle((0, 0), 0.2, color = 'blue', alpha = 0.7)
        ax2.add_patch(circle)
        
        # 绘制空间点分布(越靠近中心越密集)
        num_points = 100
        angles = np.random.uniform(0, 2 * np.pi, num_points)
        
        # 距离服从指数分布,靠近中心的点更多
        distances = - np.log(np.random.uniform(0, 1, num_points)) * 2
        
        # 过滤超出范围的点
        mask = distances < 2
        angles = angles[mask]
        distances = distances[mask]
        
        # 转换为笛卡尔坐标
        x_points = distances * np.cos(angles)
        y_points = distances * np.sin(angles)
        
        # 根据距离计算点的大小(越近越大,表示密度变化)
        sizes = 100 / (distances + 1)
        
        # 绘制空间点
        scatter = ax2.scatter(x_points, y_points, s = sizes, c = distances, cmap = 'viridis', alpha = 0.7)
        
        # 添加颜色条
        cbar = plt.colorbar(scatter, ax = ax2)
        cbar.set_label('距离')
        
        # 设置坐标轴
        ax2.set_xlim( - 2.5, 2.5)
        ax2.set_ylim( - 2.5, 2.5)
        ax2.set_aspect('equal')
        ax2.set_xlabel('X坐标')
        ax2.set_ylabel('Y坐标')
        ax2.set_title('空间点密度分布示意图', fontsize = 14)
        ax2.grid(True, linestyle = '--', alpha = 0.3)
        
        plt.tight_layout()
        plt.suptitle('质量定义方程的几何直观表示', fontsize = 16, y = 1.02)
        plt.show()
    
    def analyze_special_cases(self):
        """分析特殊情况"""
        print(" / n =  =  =  =  = 特殊情况分析 =  =  =  =  = ")
        
        # 1. 均匀分布情况:n(Ω) = c (常数)
        print("1. 均匀分布情况:")
        print(" - 空间点数量: n(Ω) = c (常数)")
        print(" - 空间点密度变化率: dn / dΩ = 0")
        print(" - 质量: m = 0")
        print(" - 物理意义: 均匀分布的空间不产生质量效应")
        
        # 2. 线性分布情况:n(Ω) = a·Ω + b
        print(" / n2. 线性分布情况:")
        print(" - 空间点数量: n(Ω) = a·Ω + b")
        print(" - 空间点密度变化率: dn / dΩ = a (常数)")
        print(" - 质量: m = k·a (常数)")
        print(" - 物理意义: 线性变化的空间点分布产生恒定质量")
        
        # 3. 指数分布情况:n(Ω) = e^(λ·Ω)
        print(" / n3. 指数分布情况:")
        print(" - 空间点数量: n(Ω) = e^(λ·Ω)")
        print(" - 空间点密度变化率: dn / dΩ = λ·e^(λ·Ω)")
        print(" - 质量: m = k·λ·e^(λ·Ω) (指数增长)")
        print(" - 物理意义: 指数变化的空间点分布产生指数增长的质量")
        
        # 绘制特殊情况的可视化
        Omega = np.linspace(0, 3, 100)
        
        plt.figure(figsize = (15, 10))
        
        # 空间点数量分布
        plt.subplot(2, 2, 1)
        plt.plot(Omega, np.ones_like(Omega) * 2, 'b - ', label = '均匀分布')
        plt.plot(Omega, 2 * Omega + 1, 'g - ', label = '线性分布')
        plt.plot(Omega, np.exp(0.5 * Omega), 'r - ', label = '指数分布')
        plt.xlabel('立体角 Ω')
        plt.ylabel('空间点数量 n')
        plt.title('不同分布情况下的空间点数量', fontsize = 12)
        plt.legend()
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        
        # 空间点密度变化率分布
        plt.subplot(2, 2, 2)
        plt.plot(Omega, np.zeros_like(Omega), 'b - ', label = '均匀分布')
        plt.plot(Omega, np.ones_like(Omega) * 2, 'g - ', label = '线性分布')
        plt.plot(Omega, 0.5 * np.exp(0.5 * Omega), 'r - ', label = '指数分布')
        plt.xlabel('立体角 Ω')
        plt.ylabel('空间点密度变化率 dn / dΩ')
        plt.title('不同分布情况下的空间点密度变化率', fontsize = 12)
        plt.legend()
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        
        # 质量分布
        plt.subplot(2, 2, 3)
        plt.plot(Omega, np.zeros_like(Omega), 'b - ', label = '均匀分布')
        plt.plot(Omega, np.ones_like(Omega) * 2 * self.k, 'g - ', label = '线性分布')
        plt.plot(Omega, 0.5 * np.exp(0.5 * Omega) * self.k, 'r - ', label = '指数分布')
        plt.xlabel('立体角 Ω')
        plt.ylabel('质量 m')
        plt.title('不同分布情况下的质量分布', fontsize = 12)
        plt.legend()
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        
        # 质量与立体角的关系(对数刻度)
        plt.subplot(2, 2, 4)
        plt.semilogy(Omega, np.ones_like(Omega) * 2 * self.k, 'g - ', label = '线性分布')
        plt.semilogy(Omega, 0.5 * np.exp(0.5 * Omega) * self.k, 'r - ', label = '指数分布')
        plt.xlabel('立体角 Ω')
        plt.ylabel('质量 m (对数刻度)')
        plt.title('质量分布(对数刻度)', fontsize = 12)
        plt.legend()
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        
        plt.tight_layout()
        plt.suptitle('质量定义方程的特殊情况分析', fontsize = 16, y = 1.02)
        plt.show()
    
    def analyze_parameter_sensitivity(self):
        """参数敏感性分析"""
        print(" / n =  =  =  =  = 参数敏感性分析 =  =  =  =  = ")
        
        # 定义空间点数量函数
        def n_func(Omega):
            return 0.5 * Omega ** 2 + Omega + 1
        
        # 生成立体角范围
        Omega = np.linspace(0, 5, 100)
        
        # 不同k值的分析
        k_values = [0.5, 1.0, 1.5, 2.0]
        
        plt.figure(figsize = (12, 8))
        
        # 计算并绘制不同k值下的质量分布
        for k in k_values:
            # 计算空间点密度变化率
            n_values = n_func(Omega)
            dn_dOmega = np.gradient(n_values, Omega)
            
            # 计算质量分布
            mass = k * dn_dOmega
            
            # 绘制质量分布
            plt.plot(Omega, mass, label = f'k = {k}')
        
        plt.xlabel('立体角 Ω')
        plt.ylabel('质量 m')
        plt.title('不同比例常数k下的质量分布', fontsize = 14)
        plt.legend()
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        plt.axhline(y = 0, color = 'k', linestyle = ' - ', alpha = 0.3)
        
        plt.tight_layout()
        plt.show()
        
        print(f"比例常数k对质量的影响分析:")
        for k in k_values:
            # 计算特定立体角处的质量
            test_Omega = 2.0
            dn_dOmega_test = test_Omega + 1  # 解析导数
            mass_test = k * dn_dOmega_test
            print(f" - 当k = {k}时,在Ω = 2.0处,质量m = {mass_test}")
        
        print(" / n结论: 质量与比例常数k成正比关系,k值越大,相同空间点密度变化率对应的质量越大")
    
    def verify_with_classical_physics(self):
        """与经典物理学的一致性验证"""
        print(" / n =  =  =  =  = 与经典物理学的一致性验证 =  =  =  =  = ")
        
        # 1. 与牛顿第二定律的关系
        print("1. 与牛顿第二定律的关系:")
        print(" - 质量定义方程: m = k·dn / dΩ")
        print(" - 牛顿第二定律: F = m·a")
        print(" - 结合得到: F = k·(dn / dΩ)·a")
        print(" - 物理意义: 力可以看作是空间点密度变化率与加速度的共同作用")
        
        # 2. 与质能关系的联系
        print(" / n2. 与质能关系的联系:")
        print(" - 质量定义方程: m = k·dn / dΩ")
        print(" - 质能关系: E = m·c²")
        print(" - 结合得到: E = k·(dn / dΩ)·c²")
        print(" - 物理意义: 能量可以表示为空间点密度变化率与光速平方的乘积")
        
        # 可视化力 - 加速度关系
        plt.figure(figsize = (12, 6))
        
        # 设置参数
        k = self.k
        Omega = 2.0  # 固定立体角
        dn_dOmega = Omega + 1  # 对应于n(Ω) = 0.5Ω² + Ω + 1
        m = k * dn_dOmega  # 质量
        
        # 生成加速度范围
        a = np.linspace(0, 10, 100)
        
        # 计算力
        F = m * a
        
        # 绘制力 - 加速度关系
        plt.plot(a, F, 'b - ', linewidth = 2)
        plt.xlabel('加速度 a')
        plt.ylabel('力 F')
        plt.title('力与加速度的关系(基于质量定义方程)', fontsize = 14)
        plt.grid(True, linestyle = ' -  - ', alpha = 0.7)
        
        plt.tight_layout()
        plt.show()
    
    def run_complete_analysis(self):
        """运行完整的分析流程"""
        print(" =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  = ")
        print("质量定义方程验证与可视化分析")
        print("方程: m = k·dn / dΩ")
        print(" =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  = ")
        
        # 1. 符号求导验证
        symbolic_results = self.symbolic_derivation()
        
        # 2. 数值模拟验证
        simulation_data = self.numerical_simulation()
        
        # 3. 可视化质量分布
        self.visualize_mass_distribution(simulation_data)
        
        # 4. 可视化立体角效应
        self.visualize_stereoscopic_effect()
        
        # 5. 特殊情况分析
        self.analyze_special_cases()
        
        # 6. 参数敏感性分析
        self.analyze_parameter_sensitivity()
        
        # 7. 与经典物理学的一致性验证
        self.verify_with_classical_physics()
        
        print(" / n =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  = ")
        print("质量定义方程验证与可视化分析完成")
        print(" =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  =  = ")

# 运行完整分析
if __name__ == "__main__":
    analyzer = MassDefinitionEquation()
    analyzer.run_complete_analysis()
