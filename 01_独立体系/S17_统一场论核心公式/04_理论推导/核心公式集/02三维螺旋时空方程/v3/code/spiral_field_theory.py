import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

# 物理常数
c0 = constants.c  # 真空光速
G = constants.G  # 万有引力常数

class SpiralFieldTheory:
    """空间光速螺旋统一场论计算工具"""
    
    def __init__(self, R=None, omega=None, v_parallel=None):
        """初始化螺旋参数"""
        self.R = R  # 旋转半径
        self.omega = omega  # 角速度
        self.v_parallel = v_parallel  # 轴向滑行速度
        self.validate_parameters()
    
    def validate_parameters(self):
        """验证参数是否满足光速约束"""
        if self.R is not None and self.omega is not None:
            v_perp = self.R * self.omega
            if self.v_parallel is None:
                self.v_parallel = np.sqrt(c0**2 - v_perp**2)
            else:
                # 验证光速约束
                v_total = np.sqrt(v_perp**2 + self.v_parallel**2)
                if not np.isclose(v_total, c0):
                    raise ValueError(f"参数不满足光速约束: v_total = {v_total}, c0 = {c0}")
    
    def get_position(self, t):
        """计算空间点的位置矢量"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        x = self.R * np.cos(self.omega * t)
        y = self.R * np.sin(self.omega * t)
        z = self.v_parallel * t
        return np.array([x, y, z])
    
    def get_velocity(self, t):
        """计算空间点的速度矢量"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        vx = -self.R * self.omega * np.sin(self.omega * t)
        vy = self.R * self.omega * np.cos(self.omega * t)
        vz = self.v_parallel
        return np.array([vx, vy, vz])
    
    def get_acceleration(self, t):
        """计算空间点的加速度矢量"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        ax = -self.R * self.omega**2 * np.cos(self.omega * t)
        ay = -self.R * self.omega**2 * np.sin(self.omega * t)
        az = 0
        return np.array([ax, ay, az])
    
    def get_jerk(self, t):
        """计算空间点的急动度矢量"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        jx = self.R * self.omega**3 * np.sin(self.omega * t)
        jy = -self.R * self.omega**3 * np.cos(self.omega * t)
        jz = 0
        return np.array([jx, jy, jz])
    
    def get_curvature(self):
        """计算螺旋的曲率"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        v_perp = self.R * self.omega
        return (v_perp * self.omega) / c0**2
    
    def get_torsion(self):
        """计算螺旋的挠率"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        v_perp = self.R * self.omega
        return (self.v_parallel * self.omega) / c0**2
    
    def get_gamma(self):
        """计算洛伦兹因子"""
        return c0 / self.v_parallel
    
    @staticmethod
    def calculate_gravitational_parameters(M, r):
        """计算引力场中的空间螺旋参数"""
        r_g = 2 * G * M / c0**2  # 引力半径
        v_perp = np.sqrt(2 * G * M / r)  # 旋转线速度
        v_parallel = c0 * np.sqrt(1 - r_g / r)  # 轴向滑行速度
        
        # 计算R和omega（假设R=1m用于演示）
        R = 1.0
        omega = v_perp / R
        
        return {
            'r_g': r_g,
            'v_perp': v_perp,
            'v_parallel': v_parallel,
            'R': R,
            'omega': omega
        }
    
    @staticmethod
    def calculate_electron_parameters(U):
        """计算电场加速下电子的参数"""
        U0 = 511e3  # 电子固有加速电压
        v_perp = c0 / (1 + U / U0)
        v_parallel = np.sqrt(c0**2 - v_perp**2)
        
        # 计算R和omega（假设R=1e-15m，电子经典半径量级）
        R = 1e-15
        omega = v_perp / R
        
        return {
            'v_perp': v_perp,
            'v_parallel': v_parallel,
            'R': R,
            'omega': omega
        }
    
    def plot_spiral(self, t_max=1e-6, num_points=1000):
        """绘制螺旋运动轨迹"""
        if self.R is None or self.omega is None:
            raise ValueError("需要设置R和omega参数")
        
        t = np.linspace(0, t_max, num_points)
        positions = np.array([self.get_position(ti) for ti in t])
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=1.5)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('空间光速螺旋运动轨迹')
        ax.grid(True)
        plt.show()

def run_comprehensive_verification():
    """运行全面的验证计算"""
    print("=== 空间光速螺旋统一场论 全面计算验证 ===")
    print(f"真空光速 c0 = {c0:.2f} m/s")
    print(f"万有引力常数 G = {G:.6e} m^3/(kg·s^2)")
    print()
    
    # 1. 核心方程验证
    print("1. 核心光速约束母方程验证")
    print("=" * 50)
    
    # 测试案例1：静止物体周围空间
    print("\n测试案例1：静止物体周围空间")
    v_perp = 1.0  # 假设微小旋转速度
    v_parallel = np.sqrt(c0**2 - v_perp**2)
    total_speed = np.sqrt(v_perp**2 + v_parallel**2)
    print(f"旋转线速度 v_perp = {v_perp:.2f} m/s")
    print(f"轴向滑行速度 v_parallel = {v_parallel:.2f} m/s")
    print(f"合速率验证: {total_speed:.2f} m/s (应等于c0)")
    print(f"误差: {abs(total_speed - c0):.2e} m/s")
    
    # 测试案例2：近光速运动
    print("\n测试案例2：近光速运动")
    v_perp = 0.99 * c0
    v_parallel = np.sqrt(c0**2 - v_perp**2)
    total_speed = np.sqrt(v_perp**2 + v_parallel**2)
    print(f"旋转线速度 v_perp = {v_perp:.2f} m/s ({v_perp/c0*100:.2f}% c0)")
    print(f"轴向滑行速度 v_parallel = {v_parallel:.2f} m/s ({v_parallel/c0*100:.2f}% c0)")
    print(f"合速率验证: {total_speed:.2f} m/s (应等于c0)")
    print(f"误差: {abs(total_speed - c0):.2e} m/s")
    
    # 2. 引力效应验证
    print("\n2. 引力效应验证")
    print("=" * 50)
    
    # 不同物体的参数
    objects = [
        {"name": "一杯水", "M": 0.5, "r": 0.05},
        {"name": "月球", "M": 7.342e22, "r": 1737e3},
        {"name": "地球", "M": 5.972e24, "r": 6371e3},
        {"name": "太阳", "M": 1.989e30, "r": 6.96e8},
        {"name": "黑洞", "M": 1.989e30, "r": 2 * G * 1.989e30 / c0**2}  # 视界处
    ]
    
    print("\n物体引力参数计算:")
    print("{:<10} {:<20} {:<20} {:<20} {:<20} {:<20}".format(
        "物体", "引力半径 (m)", "观测位置 (m)", "旋转线速度 (m/s)", "轴向滑行速度 (m/s)", "合速率验证"))
    print("-" * 120)
    
    for obj in objects:
        params = SpiralFieldTheory.calculate_gravitational_parameters(obj["M"], obj["r"])
        total_speed = np.sqrt(params["v_perp"]**2 + params["v_parallel"]**2)
        print("{:<10} {:<20.2e} {:<20.2e} {:<20.2f} {:<20.2f} {:<20.2f}".format(
            obj["name"], params["r_g"], obj["r"], params["v_perp"], params["v_parallel"], total_speed))
    
    # 3. 电子加速验证
    print("\n3. 电子加速验证")
    print("=" * 50)
    
    voltages = [0, 511e3, 1e6, 10e6]
    print("\n电子加速参数计算:")
    print("{:<15} {:<20} {:<20} {:<20}".format(
        "加速电压 (kV)", "旋转线速度 (m/s)", "轴向滑行速度 (m/s)", "合速率验证"))
    print("-" * 80)
    
    for U in voltages:
        params = SpiralFieldTheory.calculate_electron_parameters(U)
        total_speed = np.sqrt(params["v_perp"]**2 + params["v_parallel"]**2)
        print("{:<15.1f} {:<20.2f} {:<20.2f} {:<20.2f}".format(
            U/1000, params["v_perp"], params["v_parallel"], total_speed))
    
    # 4. 洛伦兹因子验证
    print("\n4. 洛伦兹因子验证")
    print("=" * 50)
    
    speeds = [0, 0.5*c0, 0.9*c0, 0.99*c0, 0.999*c0]
    print("\n速度与洛伦兹因子关系:")
    print("{:<20} {:<20} {:<20}".format(
        "速度 (m/s)", "速度 (%c0)", "洛伦兹因子 γ"))
    print("-" * 60)
    
    for v in speeds:
        v_perp = v
        v_parallel = np.sqrt(c0**2 - v_perp**2)
        gamma = c0 / v_parallel
        print("{:<20.2f} {:<20.2f} {:<20.6f}".format(
            v, v/c0*100, gamma))
    
    # 5. 极限状态验证
    print("\n5. 极限状态验证")
    print("=" * 50)
    
    # 光子极限（零质量）
    print("\n光子极限状态:")
    v_perp_photon = 0
    v_parallel_photon = c0
    total_speed_photon = np.sqrt(v_perp_photon**2 + v_parallel_photon**2)
    print(f"旋转线速度 v_perp = {v_perp_photon:.2f} m/s")
    print(f"轴向滑行速度 v_parallel = {v_parallel_photon:.2f} m/s")
    print(f"合速率验证: {total_speed_photon:.2f} m/s (应等于c0)")
    
    # 黑洞视界极限
    print("\n黑洞视界极限状态:")
    v_perp_blackhole = c0
    v_parallel_blackhole = 0
    total_speed_blackhole = np.sqrt(v_perp_blackhole**2 + v_parallel_blackhole**2)
    print(f"旋转线速度 v_perp = {v_perp_blackhole:.2f} m/s")
    print(f"轴向滑行速度 v_parallel = {v_parallel_blackhole:.2f} m/s")
    print(f"合速率验证: {total_speed_blackhole:.2f} m/s (应等于c0)")
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    run_comprehensive_verification()
