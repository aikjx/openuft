import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from unified_field_visualizer import UnifiedFieldVisualizer


class MassDefinitionVisualizer(UnifiedFieldVisualizer):
    """
    质量定义方程可视化器
    方程: m = k · dn/dΩ
    """
    
    def __init__(self):
        super().__init__(
            "质量定义方程",
            "m = k · dn/dΩ"
        )
        self.k = 1.0  # 比例常数
        self.max_omega = 4 * np.pi  # 最大立体角（整个球面）
    
    def visualize(self) -> list:
        """可视化质量定义方程"""
        figures = []
        
        # 1. 2D可视化：质量随立体角的变化
        fig1 = self._visualize_2d_mass_omega()
        figures.append(fig1)
        
        # 2. 3D可视化：质量在立体角上的分布
        fig2 = self._visualize_3d_mass_distribution()
        figures.append(fig2)
        
        # 3. 参数敏感性分析
        fig3 = self._visualize_parameter_sensitivity()
        figures.append(fig3)
        
        return figures
    
    def space_motion_density(self, omega):
        """定义空间运动量密度函数"""
        mu = self.max_omega / 2
        sigma = self.max_omega / 6
        return np.exp(-0.5 * ((omega - mu) / sigma) ** 2) * 10
    
    def calculate_mass(self, omega):
        """根据质量定义方程计算质量"""
        dn_domega = self.space_motion_density(omega)
        return self.k * dn_domega
    
    def _visualize_2d_mass_omega(self) -> plt.Figure:
        """2D可视化：质量随立体角的变化关系"""
        omega = np.linspace(0, self.max_omega, 500)
        dn_domega = self.space_motion_density(omega)
        mass = self.calculate_mass(omega)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 绘制空间运动量密度
        ax1.plot(omega, dn_domega, 'b-', linewidth=2)
        ax1.set_title('空间运动量密度 dn/dΩ 随立体角 Ω 的变化', fontsize=14)
        ax1.set_xlabel('立体角 Ω (球面度, sr)', fontsize=12)
        ax1.set_ylabel('空间运动量密度 dn/dΩ', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 绘制质量
        ax2.plot(omega, mass, 'r-', linewidth=2)
        ax2.set_title('质量 m 随立体角 Ω 的变化', fontsize=14)
        ax2.set_xlabel('立体角 Ω (球面度, sr)', fontsize=12)
        ax2.set_ylabel('质量 m', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        self._add_formula_text(fig)
        self._add_parameter_explanation(fig, self._get_mass_explanation())
        
        return fig
    
    def _visualize_3d_mass_distribution(self) -> plt.Figure:
        """3D可视化：质量在空间立体角上的分布"""
        theta = np.linspace(0, np.pi, 30)
        phi = np.linspace(0, 2*np.pi, 30)
        theta, phi = np.meshgrid(theta, phi)
        
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        
        # 计算每个点对应的立体角和质量
        omega = np.sqrt(x**2 + y**2 + z**2) * np.pi
        mass = self.calculate_mass(omega)
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制质量分布在球面上的热图
        scatter = ax.scatter(x, y, z, c=mass, cmap='viridis', s=100, alpha=0.7)
        
        ax.set_title('质量在空间立体角上的分布可视化', fontsize=14)
        ax.set_xlabel('X轴', fontsize=12)
        ax.set_ylabel('Y轴', fontsize=12)
        ax.set_zlabel('Z轴', fontsize=12)
        
        cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('质量 m', fontsize=12)
        
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_parameter_sensitivity(self) -> plt.Figure:
        """参数敏感性分析"""
        omega = np.linspace(0, self.max_omega, 200)
        
        # 不同k值的影响
        k_values = [0.5, 1.0, 2.0]
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for k in k_values:
            original_k = self.k
            self.k = k
            mass = self.calculate_mass(omega)
            ax.plot(omega, mass, linewidth=2, label=f'k = {k}')
            self.k = original_k
        
        ax.set_title('比例常数 k 对质量的影响', fontsize=16)
        ax.set_xlabel('立体角 Ω (球面度, sr)', fontsize=14)
        ax.set_ylabel('质量 m', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        self._add_formula_text(fig)
        
        return fig
    
    def _get_mass_explanation(self) -> str:
        """获取质量定义方程的参数解释"""
        return (
            "质量定义方程参数详解:\n"
            "m = k · dn/dΩ\n\n"
            "参数含义:\n"
            "- m: 物体的质量，是物体惯性和引力属性的量度\n"
            "- k: 比例常数，与空间的基本属性相关\n"
            "- dn/dΩ: 单位立体角内的空间运动量变化率\n"
            "- Ω: 立体角，描述空间中方向的量度，单位为球面度(sr)\n\n"
            "物理意义:\n"
            "- 该方程从空间几何角度定义质量，揭示了质量与空间运动量\n"
            "  分布之间的内在联系\n"
            "- 质量并非物体的固有属性，而是空间运动量分布特征的表现\n"
            "- 统一场论的核心思想之一：质量本质上是空间的一种运动效应\n"
            "- 该定义为理解惯性质量和引力质量的等价性提供了基础"
        )


class UnifiedForceVisualizer(UnifiedFieldVisualizer):
    """
    宇宙大统一方程（力方程）可视化器
    方程: F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)
    """
    
    def __init__(self):
        super().__init__(
            "宇宙大统一方程",
            "F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)"
        )
        self.c = 299792458  # 光速，单位：m/s
        self.base_mass = 1.0  # 基础质量，单位：kg
    
    def visualize(self) -> list:
        """可视化宇宙大统一方程"""
        figures = []
        
        # 1. 力分量随时间变化
        fig1 = self._visualize_force_components()
        figures.append(fig1)
        
        # 2. 力矢量分解
        fig2 = self._visualize_force_vectors()
        figures.append(fig2)
        
        # 3. 与牛顿第二定律的对比
        fig3 = self._visualize_newton_comparison()
        figures.append(fig3)
        
        return figures
    
    def calculate_force_components(self, t, mass_rate=0.1, C_rate=0.0, V_rate=1000.0):
        """计算大统一方程中的各分力"""
        m = self.base_mass + mass_rate * t
        C = np.array([0, 0, self.c + C_rate * t])
        V = np.array([V_rate * t, 0, 0])
        
        dP_dt1 = C * mass_rate  # C(dm/dt)
        dP_dt2 = -V * mass_rate  # -V(dm/dt)
        dP_dt3 = m * np.array([0, 0, C_rate])  # m(dC/dt)
        dP_dt4 = -m * np.array([V_rate, 0, 0])  # -m(dV/dt)
        
        total_force = dP_dt1 + dP_dt2 + dP_dt3 + dP_dt4
        
        return total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4
    
    def _visualize_force_components(self) -> plt.Figure:
        """可视化大统一方程中的各分力随时间的变化"""
        t = np.linspace(0, 10, 100)
        
        total_forces = []
        components = [[], [], [], []]
        
        for time in t:
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4 = self.calculate_force_components(time)
            total_forces.append(total_force)
            components[0].append(dP_dt1)
            components[1].append(dP_dt2)
            components[2].append(dP_dt3)
            components[3].append(dP_dt4)
        
        total_forces = np.array(total_forces)
        components = np.array(components)
        
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('宇宙大统一方程（力方程）各分力随时间的变化', fontsize=16)
        
        # 总力的三个分量
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
        
        # Z方向分力贡献
        axes[1, 1].plot(t, components[0, :, 2], 'r-', linewidth=1.5, label='C(dm/dt)')
        axes[1, 1].plot(t, components[2, :, 2], 'g-', linewidth=1.5, label='m(dC/dt)')
        axes[1, 1].set_title('Z方向分力贡献', fontsize=14)
        axes[1, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[1, 1].set_ylabel('力 (N)', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        # X方向分力贡献
        axes[2, 0].plot(t, components[1, :, 0], 'b-', linewidth=1.5, label='-V(dm/dt)')
        axes[2, 0].plot(t, components[3, :, 0], 'm-', linewidth=1.5, label='-m(dV/dt)')
        axes[2, 0].set_title('X方向分力贡献', fontsize=14)
        axes[2, 0].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 0].set_ylabel('力 (N)', fontsize=12)
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        # 总力大小
        total_force_magnitudes = np.linalg.norm(total_forces, axis=1)
        axes[2, 1].plot(t, total_force_magnitudes, 'k-', linewidth=2)
        axes[2, 1].set_title('总力大小', fontsize=14)
        axes[2, 1].set_xlabel('时间 t (s)', fontsize=12)
        axes[2, 1].set_ylabel('力 (N)', fontsize=12)
        axes[2, 1].grid(True, alpha=0.3)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_force_vectors(self) -> plt.Figure:
        """在特定时间点可视化各分力和总力的矢量表示"""
        time_points = [1, 5, 10]
        
        fig = plt.figure(figsize=(15, 10))
        
        for i, time in enumerate(time_points):
            ax = fig.add_subplot(1, len(time_points), i+1, projection='3d')
            
            max_force = 5e7
            ax.set_xlim([-max_force, max_force])
            ax.set_ylim([-max_force, max_force])
            ax.set_zlim([-max_force, max_force])
            
            ax.set_xlabel('X轴', fontsize=12)
            ax.set_ylabel('Y轴', fontsize=12)
            ax.set_zlabel('Z轴', fontsize=12)
            ax.set_title(f'力矢量分解 (t={time}s)', fontsize=14)
            
            total_force, dP_dt1, dP_dt2, dP_dt3, dP_dt4 = self.calculate_force_components(time)
            
            ax.quiver(0, 0, 0, dP_dt1[0], dP_dt1[1], dP_dt1[2],
                     color='red', linewidth=2, label='C(dm/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt2[0], dP_dt2[1], dP_dt2[2],
                     color='blue', linewidth=2, label='-V(dm/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt3[0], dP_dt3[1], dP_dt3[2],
                     color='green', linewidth=2, label='m(dC/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, dP_dt4[0], dP_dt4[1], dP_dt4[2],
                     color='purple', linewidth=2, label='-m(dV/dt)', arrow_length_ratio=0.1)
            ax.quiver(0, 0, 0, total_force[0], total_force[1], total_force[2],
                     color='black', linewidth=3, label='总力 F', arrow_length_ratio=0.1)
            
            ax.legend(loc='upper right')
        
        plt.tight_layout()
        self._add_formula_text(fig)
        
        return fig
    
    def _visualize_newton_comparison(self) -> plt.Figure:
        """可视化与牛顿第二定律的对比"""
        t = np.linspace(0, 10, 100)
        
        # 大统一方程力
        unified_forces = []
        # 牛顿第二定律力 (近似)
        newton_forces = []
        
        for time in t:
            total_force, _, _, _, dP_dt4 = self.calculate_force_components(time)
            unified_forces.append(np.linalg.norm(total_force))
            newton_forces.append(np.linalg.norm(-dP_dt4))  # 牛顿第二定律项
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(t, unified_forces, 'b-', linewidth=2, label='统一场论力')
        ax.plot(t, newton_forces, 'r--', linewidth=1.5, label='牛顿第二定律力')
        
        ax.set_title('统一场论力与牛顿第二定律力的对比', fontsize=16)
        ax.set_xlabel('时间 t (s)', fontsize=14)
        ax.set_ylabel('力大小 (N)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # 添加说明文本
        ax.text(
            0.1, 0.9,
            '牛顿第二定律是统一场论力方程的特例:\n'
            '- 当质量不变 (dm/dt=0)\n'
            '- 当空间运动均匀 (dC/dt=0)\n'
            '方程简化为 F = -m(dV/dt)，即 F = ma',
            transform=ax.transAxes,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        self._add_formula_text(fig)
        
        return fig
    
    def _get_force_explanation(self) -> str:
        """获取宇宙大统一方程的参数解释"""
        return (
            "宇宙大统一方程（力方程）参数详解:\n"
            "F = dP/dt = C(dm/dt) - V(dm/dt) + m(dC/dt) - m(dV/dt)\n\n"
            "各分量意义:\n"
            "1. C(dm/dt): 空间运动速度与质量变化率的乘积\n"
            "2. -V(dm/dt): 物体运动速度与质量变化率的乘积的负值\n"
            "3. m(dC/dt): 质量与空间运动加速度的乘积\n"
            "4. -m(dV/dt): 质量与物体运动加速度的乘积的负值\n\n"
            "物理意义:\n"
            "- 该方程统一描述了各种力的本质，是统一场论的核心方程\n"
            "- 揭示了力不仅来自于物体的加速度，还来自于质量变化和空间运动变化\n"
            "- 牛顿第二定律(F = ma)是该方程在特定条件下的近似\n"
            "- 当质量不变(dm/dt=0)且空间运动均匀(dC/dt=0)时，\n"
            "  方程简化为F = -m(dV/dt)，即F = ma\n"
            "- 该方程为理解引力、电磁力等各种力的统一本质提供了框架"
        )


if __name__ == "__main__":
    print("开始测试质量定义方程可视化...")
    mass_visualizer = MassDefinitionVisualizer()
    mass_files = mass_visualizer.run()
    print(f"质量定义方程可视化完成，保存的文件: {mass_files}")
    
    print("\n开始测试宇宙大统一方程可视化...")
    force_visualizer = UnifiedForceVisualizer()
    force_files = force_visualizer.run()
    print(f"宇宙大统一方程可视化完成，保存的文件: {force_files}")