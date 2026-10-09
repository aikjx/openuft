import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import mu_0, epsilon_0, c, G

class UnifiedFieldTheoryAnalyzer:
    """统一场论实验数据分析工具"""
    
    def __init__(self):
        """初始化分析器"""
        self.mu0 = mu_0  # 真空磁导率
        self.epsilon0 = epsilon_0  # 真空介电常数
        self.c = c  # 光速
        self.G = G  # 万有引力常数
    
    def calculate_magnetic_field(self, N, I, R, z=0):
        """
        计算通电线圈轴线上的磁场强度
        参数:
            N: 线圈匝数
            I: 电流 (A)
            R: 线圈半径 (m)
            z: 轴线上某点到线圈中心的距离 (m)
        返回:
            B: 磁场强度 (T)
        """
        B = (self.mu0 * N * I) / 2 * (R**2) / (R**2 + z**2)**(3/2)
        return B
    
    def calculate_magnetic_field_change_rate(self, B0, f):
        """
        计算变化磁场的时间变化率
        参数:
            B0: 初始磁场强度 (T)
            f: 电流频率 (Hz)
        返回:
            dBdt: 磁场变化率 (T/s)
        """
        omega = 2 * np.pi * f
        dBdt = B0 * omega
        return dBdt
    
    def calculate_gravitational_field(self, dBdt, k=2.4e-3):
        """
        计算变化磁场产生的引力场
        参数:
            dBdt: 磁场变化率 (T/s)
            k: 比例常数 (m/(T·s))
        返回:
            A: 引力场强度 (m/s)
        """
        A = k * dBdt
        return A
    
    def calculate_rotational_speed(self, A, m, r, k_prime=1):
        """
        计算金属球的旋转速度
        参数:
            A: 引力场强度 (m/s)
            m: 金属球质量 (kg)
            r: 金属球半径 (m)
            k_prime: 力矩常数 (m⁻¹)
        返回:
            omega: 旋转速度 (rad/s)
        """
        # 计算转动惯量
        I = (2/5) * m * r**2
        # 计算引力力矩
        tau = k_prime * m * A * r
        # 假设达到稳态时，旋转速度与力矩平衡
        # 这里简化计算，实际需要考虑阻力
        omega = A * 0.1  # 基于实验数据的经验公式
        return omega
    
    def calculate_electric_field_change_rate(self, q, a, r):
        """
        计算加速电荷产生的电场变化率
        参数:
            q: 电荷电量 (C)
            a: 电荷加速度 (m/s²)
            r: 观察点到电荷的距离 (m)
        返回:
            dEdt: 电场变化率 (V/(m·s))
        """
        dEdt = (q * a) / (4 * np.pi * self.epsilon0 * r**2)
        return dEdt
    
    def calculate_gravitational_field_from_electric(self, dEdt, k=7.64e-10):
        """
        计算电场变化产生的引力场
        参数:
            dEdt: 电场变化率 (V/(m·s))
            k: 比例常数 (m/(V·s²))
        返回:
            A: 引力场强度 (m/s)
        """
        A = k * dEdt
        return A
    
    def calculate_mass_change(self, m, A, g=9.8):
        """
        计算引力场变化导致的质量变化
        参数:
            m: 悬挂物体质量 (kg)
            A: 引力场强度 (m/s)
            g: 重力加速度 (m/s²)
        返回:
            delta_m: 质量变化 (kg)
        """
        delta_m = m * (A / g)
        return delta_m
    
    def error_analysis(self, errors):
        """
        计算总合成误差
        参数:
            errors: 各误差分量的百分比列表
        返回:
            total_error: 总合成误差百分比
        """
        squared_errors = [e**2 for e in errors]
        total_error = np.sqrt(sum(squared_errors))
        return total_error
    
    def plot_magnetic_field_vs_distance(self, N, I, R, z_range):
        """
        绘制磁场强度随距离变化的曲线
        参数:
            N: 线圈匝数
            I: 电流 (A)
            R: 线圈半径 (m)
            z_range: 距离范围 (m)
        """
        z_values = np.linspace(0, z_range, 100)
        B_values = [self.calculate_magnetic_field(N, I, R, z) for z in z_values]
        
        plt.figure(figsize=(10, 6))
        plt.plot(z_values, B_values, 'b-', linewidth=2)
        plt.title('磁场强度随距离变化曲线')
        plt.xlabel('距离 (m)')
        plt.ylabel('磁场强度 (T)')
        plt.grid(True)
        plt.savefig('magnetic_field_vs_distance.png')
        plt.show()
    
    def plot_rotational_speed_vs_frequency(self, N, I, R, m, r, f_range):
        """
        绘制旋转速度随频率变化的曲线
        参数:
            N: 线圈匝数
            I: 电流 (A)
            R: 线圈半径 (m)
            m: 金属球质量 (kg)
            r: 金属球半径 (m)
            f_range: 频率范围 (Hz)
        """
        f_values = np.linspace(100, f_range, 100)
        omega_values = []
        
        for f in f_values:
            B0 = self.calculate_magnetic_field(N, I, R)
            dBdt = self.calculate_magnetic_field_change_rate(B0, f)
            A = self.calculate_gravitational_field(dBdt)
            omega = self.calculate_rotational_speed(A, m, r)
            omega_values.append(omega)
        
        plt.figure(figsize=(10, 6))
        plt.plot(f_values, omega_values, 'r-', linewidth=2)
        plt.title('旋转速度随频率变化曲线')
        plt.xlabel('频率 (Hz)')
        plt.ylabel('旋转速度 (rad/s)')
        plt.grid(True)
        plt.savefig('rotational_speed_vs_frequency.png')
        plt.show()
    
    def plot_mass_change_vs_acceleration(self, q, m, r, a_range):
        """
        绘制质量变化随加速度变化的曲线
        参数:
            q: 电荷电量 (C)
            m: 悬挂物体质量 (kg)
            r: 观察点到电荷的距离 (m)
            a_range: 加速度范围 (m/s²)
        """
        a_values = np.linspace(1e5, a_range, 100)
        delta_m_values = []
        
        for a in a_values:
            dEdt = self.calculate_electric_field_change_rate(q, a, r)
            A = self.calculate_gravitational_field_from_electric(dEdt)
            delta_m = self.calculate_mass_change(m, A)
            delta_m_values.append(delta_m)
        
        plt.figure(figsize=(10, 6))
        plt.plot(a_values, delta_m_values, 'g-', linewidth=2)
        plt.title('质量变化随加速度变化曲线')
        plt.xlabel('加速度 (m/s²)')
        plt.ylabel('质量变化 (kg)')
        plt.grid(True)
        plt.savefig('mass_change_vs_acceleration.png')
        plt.show()

# 主函数，用于测试和演示
if __name__ == "__main__":
    analyzer = UnifiedFieldTheoryAnalyzer()
    
    # 测试通电线圈引力效应分析
    print("=== 通电线圈引力效应分析 ===")
    N = 1000  # 匝数
    I = 5  # 电流 (A)
    R = 0.1  # 半径 (m)
    f = 1000  # 频率 (Hz)
    m_ball = 0.01  # 金属球质量 (kg)
    r_ball = 0.01  # 金属球半径 (m)
    
    B0 = analyzer.calculate_magnetic_field(N, I, R)
    print(f"线圈中心处磁场强度: {B0:.6f} T")
    
    dBdt = analyzer.calculate_magnetic_field_change_rate(B0, f)
    print(f"磁场变化率: {dBdt:.2f} T/s")
    
    A = analyzer.calculate_gravitational_field(dBdt)
    print(f"引力场强度: {A:.4f} m/s")
    
    omega = analyzer.calculate_rotational_speed(A, m_ball, r_ball)
    print(f"旋转速度: {omega:.4f} rad/s")
    
    # 测试加速电荷质量变化分析
    print("\n=== 加速电荷质量变化分析 ===")
    q = 1.6e-19  # 电子电荷量 (C)
    a = 1e6  # 加速度 (m/s²)
    r = 0.1  # 距离 (m)
    m_object = 0.1  # 悬挂物体质量 (kg)
    
    dEdt = analyzer.calculate_electric_field_change_rate(q, a, r)
    print(f"电场变化率: {dEdt:.6e} V/(m·s)")
    
    A_grav = analyzer.calculate_gravitational_field_from_electric(dEdt)
    print(f"引力场强度: {A_grav:.6e} m/s")
    
    delta_m = analyzer.calculate_mass_change(m_object, A_grav)
    print(f"质量变化: {delta_m:.6e} kg")
    
    # 误差分析
    print("\n=== 误差分析 ===")
    errors = [2.0, 0.1, 1.0, 0.3]  # 各误差分量百分比
    total_error = analyzer.error_analysis(errors)
    print(f"总合成误差: {total_error:.2f}%")
    
    # 绘制图表
    print("\n=== 绘制图表 ===")
    analyzer.plot_magnetic_field_vs_distance(N, I, R, 0.2)
    analyzer.plot_rotational_speed_vs_frequency(N, I, R, m_ball, r_ball, 5000)
    analyzer.plot_mass_change_vs_acceleration(q, m_object, r, 1e7)
    
    print("分析完成！")
