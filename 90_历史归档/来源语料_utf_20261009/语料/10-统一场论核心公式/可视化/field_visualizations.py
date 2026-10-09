import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from unified_field_visualizer import UnifiedFieldVisualizer


class ElectricFieldVisualizer(UnifiedFieldVisualizer):
    """
    电场定义方程可视化器
    方程: E = k × (dm/dt) × (V₁ × V₂)/r³
    """
    
    def __init__(self):
        super().__init__(
            "电场定义方程",
            "E = k × (dm/dt) × (V₁ × V₂)/r³"
        )
        self.k = 1.0  # 比例常数
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
        self.v1_base = np.array([1.0, 0.0, 0.0])  # 电荷运动速度基础矢量
        self.v2_base = np.array([0.0, 1.0, 0.0])  # 空间运动速度基础矢量
        self.r_max = 5.0  # 最大半径，用于可视化
    
    def visualize(self) -> list:
        """可视化电场定义方程"""
        figures = []
        
        # 1. 2D电场分布
        fig1 = self._visualize_field_2d()
        figures.append(fig1)
        
        # 2. 3D电场分布
        fig2 = self._visualize_field_3d()
        figures.append(fig2)
        
        # 3. 场强与距离关系
        fig3 = self._visualize_field_strength_distance()
        figures.append(fig3)
        
        # 4. 速度影响分析
        fig4 = self._visualize_velocity_effect()
        figures.append(fig4)
        
        return figures
    
    def calculate_electric_field(self, x, y, z, v1_factor=1.0, v2_factor=1.0):
        """计算电场强度"""
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        r = np.sqrt(x**2 + y**2 + z**2)
        r_safe = np.maximum(r, 1e-6)
        
        v1 = self.v1_base * v1_factor
        v2 = self.v2_base * v2_factor
        
        # 计算叉积 V₁ × V₂
        cross_product_x = v1[1] * v2[2] - v1[2] * v2[1]
        cross_product_y = v1[2] * v2[0] - v1[0] * v2[2]
        cross_product_z = v1[0] * v2[1] - v1[1] * v2[0]
        
        E_x = self.k * self.dm_dt * cross_product_x / (r_safe**3)
        E_y = self.k * self.dm_dt * cross_product_y / (r_safe**3)
        E_z = self.k * self.dm_dt * cross_product_z / (r_safe**3)
        
        return np.array([E_x, E_y, E_z])
    
    def _visualize_field_2d(self) -> plt.Figure:
        """在XY平面上可视化电场分布"""
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        E = self.calculate_electric_field(X, Y, Z)
        E_x, E_y, E_z = E
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.quiver(X, Y, E_x, E_y, color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        ax.arrow(0, 0, self.v2_base[0] * self.r_max * 0.5, self.v2_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='green', ec='green')
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, r'$V_1$', fontsize=14, color='red')
        ax.text(self.v2_base[0] * self.r_max * 0.5, self.v2_base[1] * self.r_max * 0.5 + 0.5, r'$V_2$', fontsize=14, color='green')
        
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
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_field_3d(self) -> plt.Figure:
        """3D可视化电场分布"""
        phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.r_max * np.sin(theta) * np.cos(phi)
        y = self.r_max * np.sin(theta) * np.sin(phi)
        z = self.r_max * np.cos(theta)
        
        E = self.calculate_electric_field(x, y, z)
        E_x, E_y, E_z = E
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.quiver(x, y, z, E_x, E_y, E_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制速度矢量指示
        scale = self.r_max * 0.6
        ax.quiver(0, 0, 0, self.v1_base[0] * scale, self.v1_base[1] * scale, self.v1_base[2] * scale,
                 length=scale, color='red', linewidth=3, label=r'$V_1$')
        ax.quiver(0, 0, 0, self.v2_base[0] * scale, self.v2_base[1] * scale, self.v2_base[2] * scale,
                 length=scale, color='green', linewidth=3, label=r'$V_2$')
        
        ax.set_title('电场分布（3D视图）', fontsize=16)
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
    
    def _visualize_field_strength_distance(self) -> plt.Figure:
        """可视化场强大小与距离的关系"""
        r = np.linspace(0.1, self.r_max, 100)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)
        
        E = self.calculate_electric_field(x, y, z)
        E_x, E_y, E_z = E
        
        field_magnitude = np.sqrt(E_x**2 + E_y**2 + E_z**2)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(r, field_magnitude, 'b-', linewidth=2, label='场强大小')
        
        # 绘制1/r³参考曲线
        reference = 1/(r**3) * np.max(field_magnitude) / np.max(1/(r**3))
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r³参考曲线')
        
        ax.set_title('电场强度与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('场强大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_velocity_effect(self) -> plt.Figure:
        """可视化速度变化对电场的影响"""
        x = np.linspace(-self.r_max, self.r_max, 15)
        y = np.linspace(-self.r_max, self.r_max, 15)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        velocity_combinations = [(0.5, 1.0), (1.0, 1.0), (1.0, 1.5)]
        
        fig, axes = plt.subplots(1, len(velocity_combinations), figsize=(18, 6))
        fig.suptitle('不同速度组合对电场的影响', fontsize=16)
        
        for i, (v1_factor, v2_factor) in enumerate(velocity_combinations):
            E = self.calculate_electric_field(X, Y, Z, v1_factor, v2_factor)
            E_x, E_y, E_z = E
            
            axes[i].quiver(X, Y, E_x, E_y, color='blue', alpha=0.8)
            
            axes[i].set_title(f'V$_{{1}}$ = {v1_factor}×基础值, V$_{{2}}$ = {v2_factor}×基础值', fontsize=14)
            axes[i].set_xlabel('X坐标', fontsize=12)
            if i == 0:
                axes[i].set_ylabel('Y坐标', fontsize=12)
            axes[i].set_aspect('equal')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        self._add_formula_text(fig)
        
        return fig


class MagneticFieldVisualizer(UnifiedFieldVisualizer):
    """
    磁场定义方程可视化器
    方程: B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]
    """
    
    def __init__(self):
        super().__init__(
            "磁场定义方程",
            "B = k × (dm/dt) × [(V₁ × (V₂ × r))/r⁵]"
        )
        self.k = 1.0  # 比例常数
        self.dm_dt = 0.5  # 质量变化率，单位：kg/s
        self.v1_base = np.array([1.0, 0.0, 0.0])  # 电荷运动速度基础矢量
        self.v2_base = np.array([0.0, 0.0, 1.0])  # 空间运动速度基础矢量
        self.r_max = 5.0  # 最大半径，用于可视化
    
    def visualize(self) -> list:
        """可视化磁场定义方程"""
        figures = []
        
        # 1. 2D磁场分布
        fig1 = self._visualize_field_2d()
        figures.append(fig1)
        
        # 2. 3D磁场分布
        fig2 = self._visualize_field_3d()
        figures.append(fig2)
        
        # 3. 场强与距离关系
        fig3 = self._visualize_field_strength_distance()
        figures.append(fig3)
        
        # 4. 环形分布特征
        fig4 = self._visualize_circular_pattern()
        figures.append(fig4)
        
        return figures
    
    def calculate_magnetic_field(self, x, y, z, v1_factor=1.0, v2_factor=1.0):
        """计算磁感应强度"""
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        r = np.sqrt(x**2 + y**2 + z**2)
        r_safe = np.maximum(r, 1e-6)
        
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
        
        B_x = self.k * self.dm_dt * cross2_x / (r_safe**5)
        B_y = self.k * self.dm_dt * cross2_y / (r_safe**5)
        B_z = self.k * self.dm_dt * cross2_z / (r_safe**5)
        
        return np.array([B_x, B_y, B_z])
    
    def _visualize_field_2d(self) -> plt.Figure:
        """在XY平面上可视化磁场分布"""
        from matplotlib.patches import Circle
        
        x = np.linspace(-self.r_max, self.r_max, 20)
        y = np.linspace(-self.r_max, self.r_max, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        B = self.calculate_magnetic_field(X, Y, Z)
        B_x, B_y, B_z = B
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.quiver(X, Y, B_x, B_y, color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        # V₂沿Z轴，在XY平面上用圆点表示
        circle = Circle((0, 0), 0.3, fill=True, color='green')
        ax.add_patch(circle)
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, 'V₁', fontsize=14, color='red')
        ax.text(0.5, 0.5, 'V₂ (向外)', fontsize=14, color='green')
        
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
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_field_3d(self) -> plt.Figure:
        """3D可视化磁场分布"""
        phi = np.linspace(0, 2*np.pi, 30)
        r_values = np.linspace(0.5, self.r_max, 4)
        
        x, y, z = [], [], []
        for r in r_values:
            for angle in phi:
                x.append(r * np.cos(angle))
                y.append(r * np.sin(angle))
                z.append(0)
        
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.quiver(x, y, z, B_x, B_y, B_z, length=0.3, color='blue', alpha=0.7)
        
        # 绘制速度矢量指示
        scale = self.r_max * 0.6
        ax.quiver(0, 0, 0, self.v1_base[0] * scale, self.v1_base[1] * scale, self.v1_base[2] * scale,
                 length=scale, color='red', linewidth=3, label='V₁')
        ax.quiver(0, 0, 0, self.v2_base[0] * scale, self.v2_base[1] * scale, self.v2_base[2] * scale,
                 length=scale, color='green', linewidth=3, label='V₂')
        
        ax.set_title('磁场分布（3D视图）', fontsize=16)
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
    
    def _visualize_field_strength_distance(self) -> plt.Figure:
        """可视化磁感应强度与距离的关系"""
        r = np.linspace(0.1, self.r_max, 100)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)
        
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        field_magnitude = np.sqrt(B_x**2 + B_y**2 + B_z**2)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(r, field_magnitude, 'b-', linewidth=2, label='磁感应强度大小')
        
        # 绘制1/r⁵参考曲线
        reference = 1/(r**5) * np.max(field_magnitude) / np.max(1/(r**5))
        ax.plot(r, reference, 'r--', linewidth=1.5, label='1/r⁵参考曲线')
        
        ax.set_title('磁感应强度与距离的关系', fontsize=16)
        ax.set_xlabel('距离 r', fontsize=14)
        ax.set_ylabel('磁感应强度大小', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_circular_pattern(self) -> plt.Figure:
        """可视化磁场的环形分布特征"""
        from matplotlib.patches import Circle
        
        phi = np.linspace(0, 2*np.pi, 100)
        radius = self.r_max * 0.8
        
        x = radius * np.cos(phi)
        y = radius * np.sin(phi)
        z = np.zeros_like(x)
        
        B = self.calculate_magnetic_field(x, y, z)
        B_x, B_y, B_z = B
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制圆形路径
        ax.plot(x, y, 'k--', linewidth=1.5, label='圆形路径')
        
        # 在圆形路径上绘制磁场矢量
        step = 5
        ax.quiver(x[::step], y[::step], B_x[::step], B_y[::step], color='blue', alpha=0.8)
        
        # 绘制速度矢量指示
        ax.arrow(0, 0, self.v1_base[0] * self.r_max * 0.5, self.v1_base[1] * self.r_max * 0.5, 
                 head_width=0.3, head_length=0.4, fc='red', ec='red')
        # V₂沿Z轴，在XY平面上用圆点表示
        circle = Circle((0, 0), 0.3, fill=True, color='green')
        ax.add_patch(circle)
        
        ax.text(self.v1_base[0] * self.r_max * 0.5 + 0.5, self.v1_base[1] * self.r_max * 0.5, 'V₁', fontsize=14, color='red')
        ax.text(0.5, 0.5, 'V₂ (向外)', fontsize=14, color='green')
        
        ax.set_title('磁场的环形分布特征', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig


class EnergyEquationVisualizer(UnifiedFieldVisualizer):
    """
    能量方程可视化器
    方程: E = mC²
    """
    
    def __init__(self):
        super().__init__(
            "能量方程",
            "E = mC²"
        )
        self.c = 299792458  # 光速，单位：m/s
        self.m_base = 1.0  # 基础质量，单位：kg
    
    def visualize(self) -> list:
        """可视化能量方程"""
        figures = []
        
        # 1. 质能关系
        fig1 = self._visualize_energy_mass()
        figures.append(fig1)
        
        # 2. 对数刻度关系
        fig2 = self._visualize_log_scale()
        figures.append(fig2)
        
        # 3. 不同物体能量对比
        fig3 = self._visualize_energy_comparison()
        figures.append(fig3)
        
        # 4. 核反应能量转换
        fig4 = self._visualize_nuclear_reactions()
        figures.append(fig4)
        
        return figures
    
    def calculate_energy(self, mass=None):
        """计算能量"""
        m = self.m_base if mass is None else mass
        return m * self.c**2
    
    def _visualize_energy_mass(self) -> plt.Figure:
        """可视化能量与质量的关系"""
        mass_range = np.linspace(0, 10*self.m_base, 100)
        energies = [self.calculate_energy(mass) for mass in mass_range]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(mass_range, energies, 'b-', linewidth=2.5)
        
        ax.set_title('质能关系 (E = mc²)', fontsize=16)
        ax.set_xlabel('质量 (kg)', fontsize=14)
        ax.set_ylabel('能量 (J)', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点
        mass_1kg = 1.0
        energy_1kg = self.calculate_energy(mass_1kg)
        ax.scatter(mass_1kg, energy_1kg, color='red', s=100, zorder=5)
        ax.annotate(f'1 kg 对应能量: {energy_1kg:.2e} J',
                   xy=(mass_1kg, energy_1kg),
                   xytext=(1.2, energy_1kg * 0.7),
                   arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                   fontsize=12)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_log_scale(self) -> plt.Figure:
        """以对数刻度可视化能量与质量的关系"""
        mass_range = np.logspace(-30, 1, 100)
        energies = [self.calculate_energy(mass) for mass in mass_range]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.loglog(mass_range, energies, 'b-', linewidth=2.5)
        
        ax.set_title('质能关系 (对数刻度)', fontsize=16)
        ax.set_xlabel('质量 (kg)', fontsize=14)
        ax.set_ylabel('能量 (J)', fontsize=14)
        ax.grid(True, which="both", alpha=0.3)
        
        # 添加物理参考点
        electron_mass = 9.1093837015e-31
        electron_energy = self.calculate_energy(electron_mass)
        ax.scatter(electron_mass, electron_energy, color='red', s=50, zorder=5)
        ax.annotate('电子', xy=(electron_mass, electron_energy),
                   xytext=(electron_mass*2, electron_energy*5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        proton_mass = 1.67262192369e-27
        proton_energy = self.calculate_energy(proton_mass)
        ax.scatter(proton_mass, proton_energy, color='green', s=50, zorder=5)
        ax.annotate('质子', xy=(proton_mass, proton_energy),
                   xytext=(proton_mass*2, proton_energy*5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        mass_1kg = 1.0
        energy_1kg = self.calculate_energy(mass_1kg)
        ax.scatter(mass_1kg, energy_1kg, color='blue', s=50, zorder=5)
        ax.annotate('1 kg', xy=(mass_1kg, energy_1kg),
                   xytext=(mass_1kg*2, energy_1kg*0.5),
                   arrowprops=dict(facecolor='black', shrink=0.05),
                   fontsize=10)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_energy_comparison(self) -> plt.Figure:
        """可视化不同质量下的能量对比"""
        from matplotlib import cm
        
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
        
        labels = list(masses.keys())
        energy_values = [self.calculate_energy(mass) for mass in masses.values()]
        log_energies = np.log10(energy_values)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        y_pos = np.arange(len(labels))
        bars = ax.barh(y_pos, log_energies, align='center', alpha=0.7)
        
        colors = cm.rainbow(np.linspace(0, 1, len(labels)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        ax.set_title('不同质量物体的能量对比 (E = mc²)', fontsize=16)
        ax.set_xlabel('能量的对数 (log₁₀(E))', fontsize=14)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        
        # 添加数值标签
        for i, v in enumerate(energy_values):
            exponent = int(np.floor(np.log10(v)))
            coeff = v / (10**exponent)
            label = f'{coeff:.2f}×10^{exponent}'
            ax.text(log_energies[i] + 0.1, i, label, va='center', fontsize=10)
        
        fig.tight_layout()
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_nuclear_reactions(self) -> plt.Figure:
        """可视化核反应中的质量能量转换"""
        # 核反应示例：氘+氚→氦+中子
        mass_deuterium = 3.34449437e-27  # 氘
        mass_tritium = 5.00826743e-27    # 氚
        mass_helium = 6.64465733e-27     # 氦-4
        mass_neutron = 1.67492749804e-27 # 中子
        
        mass_before = mass_deuterium + mass_tritium
        mass_after = mass_helium + mass_neutron
        
        mass_defect = mass_before - mass_after
        energy_released = self.calculate_energy(mass_defect)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.array([0, 1])
        width = 0.35
        
        ax.bar(x[0] - width/2, mass_before, width, label='反应前总质量')
        ax.bar(x[0] + width/2, mass_after, width, label='反应后总质量')
        ax.bar(x[1], energy_released, width, color='red', label='释放的能量')
        
        ax.set_title('核反应中的质量能量转换', fontsize=16)
        ax.set_xlabel('反应阶段', fontsize=14)
        ax.set_ylabel('质量 (kg)', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(['质量对比', '释放能量'])
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(loc='upper left')
        
        # 添加双Y轴
        ax2 = ax.twinx()
        ax2.set_ylabel('能量 (J)', fontsize=14)
        ax2.bar(x[1], energy_released, width, color='red', alpha=0)
        
        # 添加数值标签
        ax.text(x[0] - width/2, mass_before, f'{mass_before:.4e} kg', ha='center', va='bottom')
        ax.text(x[0] + width/2, mass_after, f'{mass_after:.4e} kg', ha='center', va='bottom')
        ax2.text(x[1], energy_released, f'{energy_released:.4e} J', ha='center', va='bottom')
        
        # 添加质量亏损说明
        ax.text(
            0.5, 0.5*mass_before,
            f'质量亏损: {mass_defect:.4e} kg\n对应能量: {energy_released:.4e} J',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontsize=12
        )
        
        fig.tight_layout()
        self._add_formula_text(fig)
        
        return fig


if __name__ == "__main__":
    print("开始测试电场定义方程可视化...")
    electric_visualizer = ElectricFieldVisualizer()
    electric_files = electric_visualizer.run()
    print(f"电场定义方程可视化完成，保存的文件: {electric_files}")
    
    print("\n开始测试磁场定义方程可视化...")
    magnetic_visualizer = MagneticFieldVisualizer()
    magnetic_files = magnetic_visualizer.run()
    print(f"磁场定义方程可视化完成，保存的文件: {magnetic_files}")
    
    print("\n开始测试能量方程可视化...")
    energy_visualizer = EnergyEquationVisualizer()
    energy_files = energy_visualizer.run()
    print(f"能量方程可视化完成，保存的文件: {energy_files}")