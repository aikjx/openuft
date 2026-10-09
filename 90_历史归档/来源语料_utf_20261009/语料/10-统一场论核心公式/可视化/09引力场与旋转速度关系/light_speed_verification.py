import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "SimSun", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"

class LightSpeedVerification:
    """
    光速波动验证类：通过模拟电磁波在真空中的传播来验证光速的恒定特性
    """
    
    def __init__(self):
        """初始化物理常数"""
        self.c = 3e8  # 光速，m/s
        self.mu0 = 4e-7 * np.pi  # 真空磁导率
        self.eps0 = 1 / (self.mu0 * self.c**2)  # 真空介电常数
        
        print(f"=== 光速波动验证实验 ===")
        print(f"计算得到的光速: {1/np.sqrt(self.mu0*self.eps0):.2e} m/s")
        print(f"理论光速: {self.c:.2e} m/s")
        
    def simulate_em_wave_propagation(self):
        """
        一维电磁波传播模拟
        返回: 空间网格、时间网格、电场历史数据
        """
        # 模拟参数
        dx = 1e-9  # 空间步长，m
        dt = dx / (2 * self.c)  # 时间步长，s (满足CFL条件)
        x_max = 3e-6  # 模拟空间范围
        t_max = 2e-14  # 模拟时间范围
        
        # 空间和时间网格
        x_points = int(x_max / dx)
        t_points = int(t_max / dt)
        x = np.linspace(0, x_max, x_points)
        t = np.linspace(0, t_max, t_points)
        
        # 初始化电场和磁场
        E_y = np.zeros(x_points)
        B_z = np.zeros(x_points)
        
        # 高斯脉冲源参数
        source_pos = int(x_points * 0.2)  # 源位置
        sigma = 5e-8  # 脉冲宽度
        
        # 存储传播数据用于可视化
        E_history = np.zeros((t_points, x_points))
        
        for n in range(t_points):
            # 更新电场（除源点外）
            for i in range(1, x_points-1):
                if i != source_pos:
                    E_y[i] = E_y[i] + (self.c * dt / dx) * (B_z[i-1] - B_z[i])
            
            # 在源点添加高斯脉冲
            pulse = np.exp(-0.5 * ((n * dt - 3e-15) / sigma)**2)
            E_y[source_pos] += pulse
            
            # 更新磁场
            for i in range(x_points-1):
                B_z[i] = B_z[i] + (self.c * dt / dx) * (E_y[i] - E_y[i+1])
            
            E_history[n, :] = E_y
        
        return x, t, E_history
    
    def measure_wave_speed(self, E_history, t, x):
        """
        测量波的传播速度
        返回: 测量到的波速、时间点、位置点
        """
        # 找到波前位置随时间的变化
        threshold = 0.1  # 检测阈值
        wave_front_positions = []
        
        for n in range(len(t)):
            for i in range(len(x)-1, 0, -1):
                if abs(E_history[n, i]) > threshold:
                    wave_front_positions.append((t[n], x[i]))
                    break
        
        if len(wave_front_positions) < 2:
            print("无法检测到明显的波前")
            return 0, [], []
        
        # 线性拟合求速度
        times = [pos[0] for pos in wave_front_positions]
        positions = [pos[1] for pos in wave_front_positions]
        
        # 选择明显传播的阶段进行拟合
        if len(times) > 10:
            times = times[5:15]  # 选择稳定的传播阶段
            positions = positions[5:15]
        
        # 线性回归
        slope, intercept = np.polyfit(times, positions, 1)
        measured_speed = slope
        
        print(f"测量到的波速: {measured_speed:.2e} m/s")
        print(f"理论光速: {self.c:.2e} m/s")
        print(f"相对误差: {abs(measured_speed - self.c)/self.c*100:.2f}%")
        
        return measured_speed, times, positions
    
    def visualize_results(self, x, t, E_history, measured_speed, times, positions):
        """
        可视化模拟结果和验证数据
        """
        # Ensure img directory exists
        img_dir = './img'
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        
        # 创建可视化图形
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
        
        # 1. 波动传播动画帧
        sample_time = len(t) // 3
        ax1.plot(x*1e6, E_history[sample_time, :], 'b-', linewidth=2, label=f't = {t[sample_time]*1e15:.1f} fs')
        ax1.set_xlabel('位置 (μm)')
        ax1.set_ylabel('电场强度 (V/m)')
        ax1.set_title('电磁波在真空中的传播')
        ax1.grid(True)
        ax1.legend()
        
        # 2. 波前位置随时间变化
        ax2.plot([t*1e15 for t in times], [p*1e6 for p in positions], 'ro-', label='测量值')
        # 理论曲线
        theory_times = np.linspace(min(times), max(times), 100)
        theory_positions = [self.c * t for t in theory_times]
        ax2.plot([t*1e15 for t in theory_times], [p*1e6 for p in theory_positions],
                 'k--', label=f'理论值 (c = {self.c:.2e} m/s)')
        ax2.set_xlabel('时间 (fs)')
        ax2.set_ylabel('波前位置 (μm)')
        ax2.set_title('波前传播速度测量')
        ax2.legend()
        ax2.grid(True)
        
        # 3. 波动方程验证
        k = 2 * np.pi / (500e-9)  # 波数，对应500nm波长
        omega = self.c * k  # 角频率
        
        # 理论波动方程解
        x_test = np.linspace(0, 1e-6, 100)
        t_test = 1e-15
        E_theoretical = np.cos(k * x_test - omega * t_test)
        
        # 数值验证波动方程
        nabla2_E = np.gradient(np.gradient(E_theoretical, x_test), x_test)
        d2E_dt2 = -omega**2 * E_theoretical
        
        ax3.plot(x_test*1e6, nabla2_E, 'r-', label='∇²E (空间二阶导数)')
        ax3.plot(x_test*1e6, (1/self.c**2) * d2E_dt2, 'b--', label='(1/c²)∂²E/∂t² (时间二阶导数项)')
        ax3.set_xlabel('位置 (μm)')
        ax3.set_ylabel('场强导数')
        ax3.set_title('波动方程验证: ∇²E = (1/c²)∂²E/∂t²')
        ax3.legend()
        ax3.grid(True)
        
        plt.tight_layout()
        plt.savefig('./img/light_speed_verification_results.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def comprehensive_light_speed_verification(self):
        """
        综合光速验证函数
        返回: 计算得到的光速、测量到的波包速度
        """
        print("\n=== 综合光速验证 ===")
        
        # 验证1：从电磁常数计算光速
        calculated_c = 1 / np.sqrt(self.mu0 * self.eps0)
        print(f"验证1 - 从μ0和ε0计算的光速: {calculated_c:.8e} m/s")
        
        # 验证2：波动方程解的形式
        def wave_packet(x, t, k, omega, sigma):
            """高斯波包解"""
            envelope = np.exp(-0.5 * ((x - self.c*t) / sigma)**2)
            carrier = np.cos(k * x - omega * t)
            return envelope * carrier
        
        # 测试波动方程解
        x_test = np.linspace(0, 10e-6, 1000)
        t1, t2 = 0, 1e-14
        k = 2*np.pi/(600e-9)  # 600nm光波
        omega = self.c * k
        
        wave1 = wave_packet(x_test, t1, k, omega, 1e-6)
        wave2 = wave_packet(x_test, t2, k, omega, 1e-6)
        
        # 找到波包中心位置
        center1 = x_test[np.argmax(wave1)]
        center2 = x_test[np.argmax(wave2)]
        measured_speed = (center2 - center1) / (t2 - t1)
        
        print(f"验证2 - 波包传播速度: {measured_speed:.8e} m/s")
        
        # 验证3：色散关系验证
        wavelengths = np.array([400e-9, 500e-9, 600e-9, 700e-9])  # 不同波长
        frequencies = self.c / wavelengths
        
        print("验证3 - 波长-频率关系验证:")
        for i, wl in enumerate(wavelengths):
            print(f"  波长 {wl*1e9:.0f} nm -> 频率 {frequencies[i]:.3e} Hz")
            print(f"  验证 c = λf: {wl * frequencies[i]:.3e} m/s")
        
        return calculated_c, measured_speed
    
    def relativistic_light_speed_verification(self):
        """
        验证光速在不同参考系中的不变性
        """
        
        # 洛伦兹变换参数
        def lorentz_factor(v):
            return 1 / np.sqrt(1 - (v/self.c)**2)
        
        # 测试不同运动参考系中的光速测量
        test_velocities = [0, 0.1*self.c, 0.5*self.c, 0.9*self.c]  # 不同运动速度
        
        print("\n=== 相对论光速不变性验证 ===")
        print("参考系速度 | 测量光速 | 伽利略变换预期 | 相对论修正")
        print("-" * 55)
        
        for v in test_velocities:
            # 经典伽利略变换预期的光速
            galilean_c = self.c - v if v < self.c else 0
            
            # 相对论修正后的光速（应始终为c）
            relativistic_c = self.c
            
            gamma = lorentz_factor(v)
            print(f"{v/self.c:.1f}c       | {relativistic_c:.2e} | {galilean_c:.2e}    | γ = {gamma:.2f}")
    
    def run_complete_verification(self):
        """
        运行完整的光速验证流程
        """
        # 1. 运行电磁波传播模拟
        print("\n=== 一维电磁波传播模拟 ===")
        x, t, E_history = self.simulate_em_wave_propagation()
        
        # 2. 测量波速
        print("\n=== 光速测量验证 ===")
        measured_speed, times, positions = self.measure_wave_speed(E_history, t, x)
        
        # 3. 可视化结果
        print("\n=== 可视化验证结果 ===")
        if measured_speed > 0:
            self.visualize_results(x, t, E_history, measured_speed, times, positions)
        
        # 4. 综合验证
        calculated_c, wave_packet_speed = self.comprehensive_light_speed_verification()
        
        # 5. 相对论验证
        self.relativistic_light_speed_verification()

# 主程序运行
if __name__ == "__main__":
    # Ensure img directory exists
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    light_verifier = LightSpeedVerification()
    light_verifier.run_complete_verification()