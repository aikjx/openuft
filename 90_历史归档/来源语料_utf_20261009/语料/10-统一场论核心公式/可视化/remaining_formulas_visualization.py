import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from unified_field_visualizer import UnifiedFieldVisualizer


class ChargeDefinitionVisualizer(UnifiedFieldVisualizer):
    """
    电荷定义方程可视化器
    方程: q = ∫(dm/dt)·dS
    """
    
    def __init__(self):
        super().__init__(
            "电荷定义方程",
            "q = ∫(dm/dt)·dS"
        )
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
    
    def visualize(self) -> list:
        """可视化电荷定义方程"""
        figures = []
        
        # 1. 电荷与质量变化率关系
        fig1 = self._visualize_charge_mass_rate()
        figures.append(fig1)
        
        # 2. 电荷分布可视化
        fig2 = self._visualize_charge_distribution()
        figures.append(fig2)
        
        # 3. 积分过程可视化
        fig3 = self._visualize_integration_process()
        figures.append(fig3)
        
        return figures
    
    def calculate_charge(self, dm_dt, area):
        """根据电荷定义方程计算电荷"""
        return dm_dt * area
    
    def _visualize_charge_mass_rate(self) -> plt.Figure:
        """可视化电荷与质量变化率的关系"""
        mass_rate_range = np.linspace(0, 2, 100)
        area = 1.0  # 单位面积
        
        charge = [self.calculate_charge(dm_dt, area) for dm_dt in mass_rate_range]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(mass_rate_range, charge, 'b-', linewidth=2.5)
        
        ax.set_title('电荷与质量变化率的关系 (q = ∫(dm/dt)·dS)', fontsize=16)
        ax.set_xlabel('质量变化率 dm/dt (kg/s)', fontsize=14)
        ax.set_ylabel('电荷 q', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点
        reference_rates = [0.5, 1.0, 1.5]
        for rate in reference_rates:
            q = self.calculate_charge(rate, area)
            ax.scatter(rate, q, color='red', s=50, zorder=5)
            ax.annotate(f'dm/dt={rate}kg/s, q={q:.2f}',
                       xy=(rate, q),
                       xytext=(rate*1.1, q*0.9),
                       arrowprops=dict(facecolor='black', shrink=0.05),
                       fontsize=10)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_charge_distribution(self) -> plt.Figure:
        """可视化电荷分布"""
        # 空间坐标
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        
        # 计算距离
        r = np.sqrt(X**2 + Y**2)
        
        # 质量变化率分布
        dm_dt_distribution = self.dm_dt * np.exp(-0.1 * r**2)
        
        # 电荷密度分布
        charge_density = dm_dt_distribution
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制等高线图
        contour = ax.contourf(X, Y, charge_density, levels=50, cmap='plasma')
        
        # 添加颜色条
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('电荷密度', fontsize=12)
        
        ax.set_title('电荷分布可视化', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_integration_process(self) -> plt.Figure:
        """可视化积分过程"""
        # 空间坐标
        x = np.linspace(0, 10, 100)
        
        # 质量变化率分布
        dm_dt = self.dm_dt * np.exp(-0.1 * (x - 5)**2)
        
        # 计算累积电荷
        cumulative_charge = np.cumsum(dm_dt) * (x[1] - x[0])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 绘制质量变化率分布
        ax1.plot(x, dm_dt, 'b-', linewidth=2)
        ax1.set_title('质量变化率分布 dm/dt', fontsize=14)
        ax1.set_xlabel('位置 x', fontsize=12)
        ax1.set_ylabel('质量变化率 dm/dt', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 绘制累积电荷
        ax2.plot(x, cumulative_charge, 'r-', linewidth=2)
        ax2.set_title('累积电荷 ∫(dm/dt)·dS', fontsize=14)
        ax2.set_xlabel('位置 x', fontsize=12)
        ax2.set_ylabel('累积电荷 q', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        self._add_formula_text(fig)
        
        return fig


class MagneticVectorPotentialVisualizer(UnifiedFieldVisualizer):
    """
    磁矢势方程可视化器
    方程: A = k × (dm/dt) × V₁/r
    """
    
    def __init__(self):
        super().__init__(
            "磁矢势方程",
            "A = k × (dm/dt) × V₁/r"
        )
        self.k = 1.0  # 比例常数
        self.dm_dt = 0.5  # 质量变化率
        self.v1_base = np.array([1.0, 0.0, 0.0])  # 速度矢量
        self.r_max = 5.0  # 最大半径
    
    def visualize(self) -> list:
        """可视化磁矢势方程"""
        figures = []
        
        # 1. 2D磁矢势分布
        fig1 = self._visualize_potential_2d()
        figures.append(fig1)
        
        # 2. 3D磁矢势分布
        fig2 = self._visualize_potential_3d()
        figures.append(fig2)
        
        # 3. 势与距离关系
        fig3 = self._visualize_potential_distance()
        figures.append(fig3)
        
        return figures
    
    def calculate_magnetic_potential(self, x, y, z, v1_factor=1.0):
        """计算磁矢势"""
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        r = np.sqrt(x**2 + y**2 + z**2)
        r_safe = np.maximum(r, 1e-6)
        
        v1 = self.v1_base * v1_factor
        
        # 计算磁矢势
        A_x = self.k * self.dm_dt * v1[0] / r_safe
        A_y = self.k * self.dm_dt * v1[1] / r_safe
        A_z = self.k * self.dm_dt * v1[2] / r_safe
        
        return np.array([A_x, A_y, A_z])
    
    def _visualize_potential_2d(self) -> plt.Figure:
        """2D可视化磁矢势分布"""
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        A = self.calculate_magnetic_potential(X, Y, Z)
        A_x, A_y, A_z = A
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制矢量场
        ax.quiver(X, Y, A_x, A_y, color='blue', alpha=0.8)
        
        ax.set_title('磁矢势分布（XY平面）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # 添加速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5,
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5,
                'V₁', fontsize=14, color='red')
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_potential_3d(self) -> plt.Figure:
        """3D可视化磁矢势分布"""
        phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.r_max * np.sin(theta) * np.cos(phi)
        y = self.r_max * np.sin(theta) * np.sin(phi)
        z = self.r_max * np.cos(theta)
        
        A = self.calculate_magnetic_potential(x, y, z)
        A_x, A_y, A_z = A
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制矢量场
        ax.quiver(x, y, z, A_x, A_y, A_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制速度矢量指示
        scale = self.r_max * 0.6
        ax.quiver(0, 0, 0, self.v1_base[0] * scale, self.v1_base[1] * scale, self.v1_base[2] * scale,
                 length=scale, color='red', linewidth=3, label='V₁')
        
        ax.set_title('磁矢势分布（3D视图）', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=12)
        ax.set_ylabel('Y坐标', fontsize=12)
        ax.set_zlabel('Z坐标', fontsize=12)
        
        limit = self.r_max * 1.2
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_potential_distance(self) -> plt.Figure:
        """可视化磁矢势与距离的关系"""
        r = np.linspace(0.1, self.r_max, 100)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)
        
        A = self.calculate_magnetic_potential(x, y, z)
        A_x, A_y, A_z = A
        
        # 计算势的大小
        potential_magnitude = np.sqrt(A_x**2 + A_y**2 + A_z**2)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(r, potential_magnitude, 'b-', linewidth=2, label='磁矢势大小')
        
        # 绘制1/r参考曲线
        reference = 1/r * np.max(potential_magnitude) / np.max(1/r)
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r参考曲线')
        
        ax.set_title('磁矢势与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('磁矢势大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig


class NuclearForceVisualizer(UnifiedFieldVisualizer):
    """
    核力场定义方程可视化器
    方程: F_n = G_n × (m1m2/r²) × exp(-r/λ)
    """
    
    def __init__(self):
        super().__init__(
            "核力场定义方程",
            "F_n = G_n × (m1m2/r²) × exp(-r/λ)"
        )
        self.G_n = 1.0  # 核力常数
        self.m1 = 1.0  # 质量1
        self.m2 = 1.0  # 质量2
        self.lambda_n = 1.0  # 核力范围参数
        self.r_max = 10.0  # 最大距离
    
    def visualize(self) -> list:
        """可视化核力场定义方程"""
        figures = []
        
        # 1. 核力与距离关系
        fig1 = self._visualize_force_distance()
        figures.append(fig1)
        
        # 2. 核力与库仑力对比
        fig2 = self._visualize_force_comparison()
        figures.append(fig2)
        
        # 3. 核力范围可视化
        fig3 = self._visualize_force_range()
        figures.append(fig3)
        
        return figures
    
    def calculate_nuclear_force(self, r):
        """计算核力"""
        return self.G_n * (self.m1 * self.m2 / r**2) * np.exp(-r / self.lambda_n)
    
    def _visualize_force_distance(self) -> plt.Figure:
        """可视化核力与距离的关系"""
        r = np.linspace(0.1, self.r_max, 200)
        force = self.calculate_nuclear_force(r)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(r, force, 'b-', linewidth=2.5)
        
        ax.set_title('核力与距离的关系 (F_n = G_n × (m1m2/r²) × exp(-r/λ))', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('核力 F_n', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点
        max_force_idx = np.argmax(force)
        ax.scatter(r[max_force_idx], force[max_force_idx], color='red', s=50, zorder=5)
        ax.annotate(f'最大力: r={r[max_force_idx]:.2f}, F={force[max_force_idx]:.2f}',
                   xy=(r[max_force_idx], force[max_force_idx]),
                   xytext=(r[max_force_idx]*1.1, force[max_force_idx]*0.8),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_force_comparison(self) -> plt.Figure:
        """可视化核力与库仑力的对比"""
        r = np.linspace(0.1, self.r_max, 200)
        
        # 核力
        nuclear_force = self.calculate_nuclear_force(r)
        
        # 库仑力（为了对比，按比例缩放）
        coulomb_force = 1/r**2 * np.max(nuclear_force) / np.max(1/r**2)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(r, nuclear_force, 'b-', linewidth=2, label='核力')
        ax.plot(r, coulomb_force, 'r--', linewidth=2, label='库仑力（参考）')
        
        ax.set_title('核力与库仑力的对比', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('力大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加说明文本
        ax.text(
            0.1, 0.9,
            '核力的特点：\n'
            '- 短程力：随着距离增加指数衰减\n'
            '- 饱和性：每个核子只与邻近核子作用\n'
            '- 强度大：在短距离内比库仑力强得多\n'
            '- 与电荷无关：质子-质子、质子-中子、中子-中子间力大致相同',
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_force_range(self) -> plt.Figure:
        """可视化核力的作用范围"""
        r = np.linspace(0.1, self.r_max, 200)
        force = self.calculate_nuclear_force(r)
        
        # 不同λ值的影响
        lambda_values = [0.5, 1.0, 2.0]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for lambda_n in lambda_values:
            original_lambda = self.lambda_n
            self.lambda_n = lambda_n
            current_force = self.calculate_nuclear_force(r)
            ax.plot(r, current_force, linewidth=2, label=f'λ={lambda_n}')
            self.lambda_n = original_lambda
        
        ax.set_title('核力范围参数 λ 的影响', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('核力 F_n', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig


if __name__ == "__main__":
    print("开始测试电荷定义方程可视化...")
    charge_visualizer = ChargeDefinitionVisualizer()
    charge_files = charge_visualizer.run()
    print(f"电荷定义方程可视化完成，保存的文件: {charge_files}")
    
    print("\n开始测试磁矢势方程可视化...")
    magnetic_potential_visualizer = MagneticVectorPotentialVisualizer()
    magnetic_potential_files = magnetic_potential_visualizer.run()
    print(f"磁矢势方程可视化完成，保存的文件: {magnetic_potential_files}")
    
    print("\n开始测试核力场定义方程可视化...")
    nuclear_force_visualizer = NuclearForceVisualizer()
    nuclear_force_files = nuclear_force_visualizer.run()
    print(f"核力场定义方程可视化完成，保存的文件: {nuclear_force_files}")