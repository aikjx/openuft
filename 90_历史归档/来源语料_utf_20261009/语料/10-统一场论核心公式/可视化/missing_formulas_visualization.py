import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from unified_field_visualizer import UnifiedFieldVisualizer


class SpacetimeUnificationVisualizer(UnifiedFieldVisualizer):
    """
    时空同一化方程可视化器
    方程: r = ct
    """
    
    def __init__(self):
        super().__init__(
            "时空同一化方程",
            "r = ct"
        )
        self.c = 299792458  # 光速，单位：m/s
    
    def visualize(self) -> list:
        """可视化时空同一化方程"""
        figures = []
        
        # 1. 时空关系可视化
        fig1 = self._visualize_spacetime_relation()
        figures.append(fig1)
        
        # 2. 时空图
        fig2 = self._visualize_spacetime_diagram()
        figures.append(fig2)
        
        # 3. 光速不变原理可视化
        fig3 = self._visualize_light_speed_constancy()
        figures.append(fig3)
        
        return figures
    
    def _visualize_spacetime_relation(self) -> plt.Figure:
        """可视化空间距离与时间的关系"""
        # 时间范围（秒）
        time_range = np.linspace(0, 1e-5, 100)
        
        # 计算对应的空间距离
        distance = self.c * time_range
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(time_range, distance, 'b-', linewidth=2.5)
        
        ax.set_title('时空同一化关系 (r = ct)', fontsize=16)
        ax.set_xlabel('时间 t (s)', fontsize=14)
        ax.set_ylabel('空间距离 r (m)', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点
        reference_times = [1e-6, 5e-6, 1e-5]
        for t in reference_times:
            d = self.c * t
            ax.scatter(t, d, color='red', s=50, zorder=5)
            ax.annotate(f't={t:.1e}s, r={d:.1e}m',
                       xy=(t, d),
                       xytext=(t*1.1, d*0.9),
                       arrowprops=dict(facecolor='black', shrink=0.05),
                       fontsize=10)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_spacetime_diagram(self) -> plt.Figure:
        """可视化时空图"""
        # 时间范围
        time = np.linspace(-10, 10, 100)
        
        # 光速世界线
        light_cone = self.c * np.abs(time)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 绘制光锥
        ax.plot(time, light_cone, 'b-', linewidth=2, label='光锥边界')
        ax.plot(time, -light_cone, 'b-', linewidth=2)
        
        # 填充光锥内部
        ax.fill_between(time, -light_cone, light_cone, color='blue', alpha=0.1, label='光锥内部')
        
        # 绘制时间轴
        ax.axvline(0, color='k', linestyle='--', linewidth=1, label='时间轴')
        
        # 绘制空间轴
        ax.axhline(0, color='k', linestyle='--', linewidth=1, label='空间轴')
        
        ax.set_title('时空图与光锥', fontsize=16)
        ax.set_xlabel('时间 t', fontsize=14)
        ax.set_ylabel('空间坐标 x', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加说明文本
        ax.text(
            0.1, 0.9,
            '时空同一化方程 r = ct 揭示了：\n'
            '- 空间和时间是统一的整体\n'
            '- 光速是连接空间和时间的常数\n'
            '- 光锥内是因果可及的区域\n'
            '- 光锥外是因果不可及的区域',
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_light_speed_constancy(self) -> plt.Figure:
        """可视化光速不变原理"""
        # 不同参考系的速度
        reference_frames = [0, 0.5*self.c, 0.8*self.c]
        
        # 时间范围
        time = np.linspace(0, 1e-6, 100)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 绘制不同参考系中的光信号
        for v in reference_frames:
            # 光信号在静止参考系中的位置
            light_position = self.c * time
            
            # 参考系本身的位置
            frame_position = v * time
            
            # 相对位置
            relative_position = light_position - frame_position
            
            label = f'参考系速度: {v/self.c:.1f}c' if v != 0 else '静止参考系'
            ax.plot(time, relative_position, linewidth=2, label=label)
        
        ax.set_title('光速不变原理可视化', fontsize=16)
        ax.set_xlabel('时间 t (s)', fontsize=14)
        ax.set_ylabel('光信号相对位置 (m)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加说明文本
        ax.text(
            0.1, 0.9,
            '光速不变原理：\n'
            '- 光在真空中的速度在所有惯性参考系中都相同\n'
            '- 与光源和观察者的运动状态无关\n'
            '- 这是时空同一化方程的直接结果\n'
            '- 也是相对论的基本假设之一',
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        self._add_formula_text(fig)
        
        return fig


class RestMomentumVisualizer(UnifiedFieldVisualizer):
    """
    静止动量方程可视化器
    方程: P = mC
    """
    
    def __init__(self):
        super().__init__(
            "静止动量方程",
            "P = mC"
        )
        self.c = 299792458  # 光速，单位：m/s
    
    def visualize(self) -> list:
        """可视化静止动量方程"""
        figures = []
        
        # 1. 静止动量与质量关系
        fig1 = self._visualize_momentum_mass()
        figures.append(fig1)
        
        # 2. 动量矢量可视化
        fig2 = self._visualize_momentum_vector()
        figures.append(fig2)
        
        # 3. 与经典动量对比
        fig3 = self._visualize_classical_comparison()
        figures.append(fig3)
        
        return figures
    
    def calculate_rest_momentum(self, mass):
        """计算静止动量"""
        return mass * self.c
    
    def _visualize_momentum_mass(self) -> plt.Figure:
        """可视化静止动量与质量的关系"""
        mass_range = np.linspace(0, 10, 100)
        momentum = [self.calculate_rest_momentum(m) for m in mass_range]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(mass_range, momentum, 'b-', linewidth=2.5)
        
        ax.set_title('静止动量与质量的关系 (P = mC)', fontsize=16)
        ax.set_xlabel('质量 (kg)', fontsize=14)
        ax.set_ylabel('静止动量 P (kg·m/s)', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # 添加参考点
        reference_masses = [1, 5, 10]
        for m in reference_masses:
            p = self.calculate_rest_momentum(m)
            ax.scatter(m, p, color='red', s=50, zorder=5)
            ax.annotate(f'm={m}kg, P={p:.1e}kg·m/s',
                       xy=(m, p),
                       xytext=(m*1.1, p*0.9),
                       arrowprops=dict(facecolor='black', shrink=0.05),
                       fontsize=10)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_momentum_vector(self) -> plt.Figure:
        """可视化静止动量的矢量性质"""
        # 不同质量的动量矢量
        masses = [1, 2, 3]
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 光速方向（沿Z轴）
        c_direction = np.array([0, 0, 1])
        
        for mass in masses:
            momentum_magnitude = self.calculate_rest_momentum(mass)
            momentum_vector = c_direction * momentum_magnitude
            
            # 绘制动量矢量
            ax.quiver(
                0, 0, 0,
                momentum_vector[0], momentum_vector[1], momentum_vector[2],
                length=momentum_magnitude/1e9,  # 缩放以适应图形
                color=self._get_color_for_mass(mass),
                linewidth=2,
                label=f'm={mass}kg, P={momentum_magnitude:.1e}kg·m/s'
            )
        
        ax.set_title('静止动量矢量可视化', fontsize=16)
        ax.set_xlabel('X轴', fontsize=12)
        ax.set_ylabel('Y轴', fontsize=12)
        ax.set_zlabel('Z轴 (光速方向)', fontsize=12)
        
        # 设置坐标轴范围
        max_momentum = self.calculate_rest_momentum(max(masses))
        scale = max_momentum / 1e9 * 1.2
        ax.set_xlim([-scale, scale])
        ax.set_ylim([-scale, scale])
        ax.set_zlim([0, scale])
        
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_classical_comparison(self) -> plt.Figure:
        """可视化与经典动量的对比"""
        mass = 1.0  # 1kg质量
        velocity_range = np.linspace(0, 0.99*self.c, 100)
        
        # 经典动量
        classical_momentum = mass * velocity_range
        
        # 相对论动量
        relativistic_momentum = mass * velocity_range / np.sqrt(1 - (velocity_range/self.c)**2)
        
        # 静止动量
        rest_momentum = np.full_like(velocity_range, self.calculate_rest_momentum(mass))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(velocity_range/self.c, classical_momentum, 'g-', linewidth=2, label='经典动量')
        ax.plot(velocity_range/self.c, relativistic_momentum, 'r-', linewidth=2, label='相对论动量')
        ax.plot(velocity_range/self.c, rest_momentum, 'b--', linewidth=1.5, label='静止动量 (P=mC)')
        
        ax.set_title('静止动量与其他动量形式的对比', fontsize=16)
        ax.set_xlabel('速度 v/c', fontsize=14)
        ax.set_ylabel('动量 (kg·m/s)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加说明文本
        ax.text(
            0.1, 0.9,
            '静止动量的物理意义：\n'
            '- 即使物体静止，也具有由光速决定的动量\n'
            '- 这是统一场论的重要概念\n'
            '- 揭示了质量与光速的内在联系\n'
            '- 静止动量 P = mC 是物体最基本的动量形式',
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        self._add_formula_text(fig)
        
        return fig
    
    def _get_color_for_mass(self, mass):
        """根据质量获取颜色"""
        colors = {1: 'red', 2: 'green', 3: 'blue'}
        return colors.get(mass, 'black')


class SpaceWaveVisualizer(UnifiedFieldVisualizer):
    """
    空间波动方程可视化器
    方程: ∂²A/∂t² - c²∇²A = 0
    """
    
    def __init__(self):
        super().__init__(
            "空间波动方程",
            "∂²A/∂t² - c²∇²A = 0"
        )
        self.c = 299792458  # 光速，单位：m/s
    
    def visualize(self) -> list:
        """可视化空间波动方程"""
        figures = []
        
        # 1. 一维波动可视化
        fig1 = self._visualize_1d_wave()
        figures.append(fig1)
        
        # 2. 二维波动可视化
        fig2 = self._visualize_2d_wave()
        figures.append(fig2)
        
        # 3. 波动传播可视化
        fig3 = self._visualize_wave_propagation()
        figures.append(fig3)
        
        return figures
    
    def _visualize_1d_wave(self) -> plt.Figure:
        """可视化一维空间波动"""
        # 空间坐标
        x = np.linspace(-10, 10, 200)
        
        # 时间点
        times = [0, 1, 2, 3]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for t in times:
            # 一维波函数
            wave = np.sin(x - self.c * t * 0.1) * np.exp(-0.1 * x**2)
            
            ax.plot(x, wave, linewidth=2, label=f't={t}s')
        
        ax.set_title('一维空间波动', fontsize=16)
        ax.set_xlabel('空间坐标 x', fontsize=14)
        ax.set_ylabel('波幅 A', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_2d_wave(self) -> plt.Figure:
        """可视化二维空间波动"""
        # 空间坐标
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        
        # 计算距离
        r = np.sqrt(X**2 + Y**2)
        
        # 波函数
        wave = np.sin(r - self.c * 0.1) * np.exp(-0.05 * r**2)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制等高线图
        contour = ax.contourf(X, Y, wave, levels=50, cmap='viridis')
        
        # 添加颜色条
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('波幅 A', fontsize=12)
        
        ax.set_title('二维空间波动', fontsize=16)
        ax.set_xlabel('X坐标', fontsize=14)
        ax.set_ylabel('Y坐标', fontsize=14)
        ax.set_aspect('equal')
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_wave_propagation(self) -> plt.Figure:
        """可视化波动传播过程"""
        # 空间坐标
        x = np.linspace(-20, 20, 200)
        
        # 时间点
        times = [0, 0.5, 1.0, 1.5]
        
        fig, axes = plt.subplots(len(times), 1, figsize=(12, 12))
        
        for i, t in enumerate(times):
            # 波函数
            wave = np.sin(x - self.c * t * 0.05) * np.exp(-0.05 * (x - self.c * t * 0.05)**2)
            
            axes[i].plot(x, wave, 'b-', linewidth=2)
            axes[i].set_title(f'波的传播 (t={t}s)', fontsize=14)
            axes[i].set_xlabel('空间坐标 x', fontsize=12)
            axes[i].set_ylabel('波幅 A', fontsize=12)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_ylim([-1.2, 1.2])
        
        plt.tight_layout()
        
        # 在最后一个子图下方添加公式
        self._add_formula_text(fig, position=(0.5, 0.01))
        
        return fig


if __name__ == "__main__":
    print("开始测试时空同一化方程可视化...")
    spacetime_visualizer = SpacetimeUnificationVisualizer()
    spacetime_files = spacetime_visualizer.run()
    print(f"时空同一化方程可视化完成，保存的文件: {spacetime_files}")
    
    print("\n开始测试静止动量方程可视化...")
    rest_momentum_visualizer = RestMomentumVisualizer()
    rest_momentum_files = rest_momentum_visualizer.run()
    print(f"静止动量方程可视化完成，保存的文件: {rest_momentum_files}")
    
    print("\n开始测试空间波动方程可视化...")
    space_wave_visualizer = SpaceWaveVisualizer()
    space_wave_files = space_wave_visualizer.run()
    print(f"空间波动方程可视化完成，保存的文件: {space_wave_files}")