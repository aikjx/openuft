import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 物理常数
c = 3e8  # 光速 (m/s)

class SpiralMotion:
    def __init__(self, a, omega, p):
        """
        初始化圆柱螺旋运动参数
        a: 旋转半径 (m)
        omega: 角速度 (rad/s)
        p: 轴向速度 (m/s)
        """
        self.a = a
        self.omega = omega
        self.p = p
        # 验证光速约束
        self.v_rot = a * omega
        self.v_total = np.sqrt(self.v_rot**2 + p**2)
        print(f"旋转速度: {self.v_rot:.2e} m/s")
        print(f"轴向速度: {p:.2e} m/s")
        print(f"合速度: {self.v_total:.2e} m/s")
        print(f"光速: {c:.2e} m/s")
        print(f"速度误差: {(self.v_total - c)/c * 100:.6f}%")
    
    def position(self, t):
        """计算t时刻的位置矢量"""
        x = self.a * np.cos(self.omega * t)
        y = self.a * np.sin(self.omega * t)
        z = self.p * t
        return np.array([x, y, z])
    
    def velocity(self, t):
        """计算t时刻的速度矢量"""
        vx = -self.a * self.omega * np.sin(self.omega * t)
        vy = self.a * self.omega * np.cos(self.omega * t)
        vz = self.p
        return np.array([vx, vy, vz])
    
    def acceleration(self, t):
        """计算t时刻的加速度矢量"""
        ax = -self.a * self.omega**2 * np.cos(self.omega * t)
        ay = -self.a * self.omega**2 * np.sin(self.omega * t)
        az = 0
        return np.array([ax, ay, az])
    
    def curvature(self):
        """计算曲率"""
        numerator = self.a * self.omega**2
        denominator = self.v_total**2
        return numerator / denominator
    
    def torsion(self):
        """计算挠率"""
        numerator = self.p * self.omega
        denominator = self.v_total**2
        return numerator / denominator
    
    def frenet_frame(self, t):
        """计算Frenet标架"""
        v = self.velocity(t)
        a = self.acceleration(t)
        
        # 单位切向量
        T = v / np.linalg.norm(v)
        
        # 单位法向量
        N = a / np.linalg.norm(a)
        
        # 单位副法向量
        B = np.cross(T, N)
        B = B / np.linalg.norm(B)
        
        return T, N, B
    
    def plot_trajectory(self, t_start=0, t_end=1e-7, num_points=1000):
        """绘制螺旋运动轨迹"""
        t = np.linspace(t_start, t_end, num_points)
        positions = np.array([self.position(ti) for ti in t])
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', label='Spiral Trajectory')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Cylindrical Spiral Motion')
        ax.legend()
        plt.savefig('spiral_trajectory.png')
        plt.show()

# 测试用例
if __name__ == "__main__":
    # 示例参数：选择合适的a, omega, p满足光速约束
    a = 1e-10  # 旋转半径
    v_rot = c * 0.6  # 旋转速度设为光速的60%
    omega = v_rot / a  # 角速度
    p = np.sqrt(c**2 - v_rot**2)  # 轴向速度
    
    print("=== 圆柱螺旋运动验证 ===")
    spiral = SpiralMotion(a, omega, p)
    
    # 验证速度恒为光速
    print("\n=== 速度验证 ===")
    t_test = 0.0
    v = spiral.velocity(t_test)
    v_mag = np.linalg.norm(v)
    print(f"t={t_test}时速度: {v}")
    print(f"速度大小: {v_mag:.2e} m/s")
    print(f"与光速的误差: {(v_mag - c)/c * 100:.6f}%")
    
    # 验证加速度指向中心
    print("\n=== 加速度验证 ===")
    a_vec = spiral.acceleration(t_test)
    pos = spiral.position(t_test)
    print(f"t={t_test}时位置: {pos}")
    print(f"t={t_test}时加速度: {a_vec}")
    # 检查加速度是否与径向位置反方向
    radial_dir = pos[:2] / np.linalg.norm(pos[:2]) if np.linalg.norm(pos[:2]) > 0 else np.array([1, 0])
    acc_dir = a_vec[:2] / np.linalg.norm(a_vec[:2]) if np.linalg.norm(a_vec[:2]) > 0 else np.array([1, 0])
    dot_product = np.dot(radial_dir, acc_dir)
    print(f"径向方向与加速度方向的点积: {dot_product:.6f}")
    print(f"加速度是否指向中心: {abs(dot_product + 1) < 1e-10}")
    
    # 计算曲率和挠率
    print("\n=== 微分几何参数 ===")
    kappa = spiral.curvature()
    tau = spiral.torsion()
    print(f"曲率 kappa: {kappa:.2e} m^-1")
    print(f"挠率 tau: {tau:.2e} m^-1")
    
    # 验证Frenet标架的垂直性
    print("\n=== Frenet标架验证 ===")
    T, N, B = spiral.frenet_frame(t_test)
    print(f"切向量 T: {T}")
    print(f"法向量 N: {N}")
    print(f"副法向量 B: {B}")
    print(f"T·N: {np.dot(T, N):.6f}")
    print(f"N·B: {np.dot(N, B):.6f}")
    print(f"B·T: {np.dot(B, T):.6f}")
    print(f"标架是否正交: {abs(np.dot(T, N)) < 1e-10 and abs(np.dot(N, B)) < 1e-10 and abs(np.dot(B, T)) < 1e-10}")
    
    # 绘制轨迹
    print("\n=== 轨迹绘制 ===")
    spiral.plot_trajectory()
    print("轨迹已保存为 spiral_trajectory.png")
