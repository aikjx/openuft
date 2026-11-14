import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 物理常数
c = 3e8  # 光速 (m/s)

class CircleMotion:
    def __init__(self, a, omega, z_const):
        """
        初始化平面圆周运动参数
        a: 旋转半径 (m)
        omega: 角速度 (rad/s)
        z_const: z轴常数位置 (m)
        """
        self.a = a
        self.omega = omega
        self.z_const = z_const
        # 验证速度
        self.v_rot = a * omega
        self.v_total = self.v_rot
        print(f"旋转速度: {self.v_rot:.2e} m/s")
        print(f"合速度: {self.v_total:.2e} m/s")
        print(f"光速: {c:.2e} m/s")
        print(f"速度误差: {(self.v_total - c)/c * 100:.6f}%")
    
    def position(self, t):
        """计算t时刻的位置矢量"""
        x = self.a * np.cos(self.omega * t)
        y = self.a * np.sin(self.omega * t)
        z = self.z_const
        return np.array([x, y, z])
    
    def velocity(self, t):
        """计算t时刻的速度矢量"""
        vx = -self.a * self.omega * np.sin(self.omega * t)
        vy = self.a * self.omega * np.cos(self.omega * t)
        vz = 0
        return np.array([vx, vy, vz])
    
    def acceleration(self, t):
        """计算t时刻的加速度矢量"""
        ax = -self.a * self.omega**2 * np.cos(self.omega * t)
        ay = -self.a * self.omega**2 * np.sin(self.omega * t)
        az = 0
        return np.array([ax, ay, az])
    
    def curvature(self):
        """计算曲率"""
        return 1 / self.a
    
    def torsion(self):
        """计算挠率"""
        return 0
    
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
    
    def plot_trajectory(self, t_start=0, t_end=None, num_points=1000):
        """绘制圆周运动轨迹"""
        if t_end is None:
            t_end = 2 * np.pi / self.omega
        t = np.linspace(t_start, t_end, num_points)
        positions = np.array([self.position(ti) for ti in t])
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', label='Circle Trajectory')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Plane Circle Motion')
        ax.legend()
        plt.savefig('circle_trajectory.png')
        plt.show()

# 测试用例
if __name__ == "__main__":
    # 示例参数：选择合适的a, omega满足光速约束
    a = 1e-10  # 旋转半径
    v_rot = c  # 旋转速度设为光速
    omega = v_rot / a  # 角速度
    z_const = 0  # z轴常数位置
    
    print("=== 平面圆周运动验证 ===")
    circle = CircleMotion(a, omega, z_const)
    
    # 验证速度
    print("\n=== 速度验证 ===")
    t_test = 0.0
    v = circle.velocity(t_test)
    v_mag = np.linalg.norm(v)
    print(f"t={t_test}时速度: {v}")
    print(f"速度大小: {v_mag:.2e} m/s")
    print(f"与光速的误差: {(v_mag - c)/c * 100:.6f}%")
    
    # 验证加速度指向中心
    print("\n=== 加速度验证 ===")
    a_vec = circle.acceleration(t_test)
    pos = circle.position(t_test)
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
    kappa = circle.curvature()
    tau = circle.torsion()
    print(f"曲率 kappa: {kappa:.2e} m^-1")
    print(f"挠率 tau: {tau:.2e} m^-1")
    
    # 验证Frenet标架的垂直性
    print("\n=== Frenet标架验证 ===")
    T, N, B = circle.frenet_frame(t_test)
    print(f"切向量 T: {T}")
    print(f"法向量 N: {N}")
    print(f"副法向量 B: {B}")
    print(f"T·N: {np.dot(T, N):.6f}")
    print(f"N·B: {np.dot(N, B):.6f}")
    print(f"B·T: {np.dot(B, T):.6f}")
    print(f"标架是否正交: {abs(np.dot(T, N)) < 1e-10 and abs(np.dot(N, B)) < 1e-10 and abs(np.dot(B, T)) < 1e-10}")
    
    # 绘制轨迹
    print("\n=== 轨迹绘制 ===")
    circle.plot_trajectory()
    print("轨迹已保存为 circle_trajectory.png")
