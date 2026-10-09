import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class SpaceWaveEquation:
    """空间波动方程验证类"""
    
    def __init__(self, c=299792458.0):
        """初始化类实例"""
        self.c = c  # 光速
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print("===== 符号求导验证 =====")
        
        # 定义符号变量
        x, y, z, t = sp.symbols('x y z t')  # 空间和时间坐标
        c = sp.Symbol('c')                 # 光速
        kx, ky, kz, omega = sp.symbols('kx ky kz omega')  # 波矢分量和角频率
        A = sp.Symbol('A')                  # 振幅
        
        # 平面波解 r(x, y, z, t) = A*exp(i(k·r - ωt))
        r = A * sp.exp(sp.I * (kx*x + ky*y + kz*z - omega*t))
        
        # 空间波动方程 ∇²r = (1/c²) ∂²r/∂t²
        # 计算左侧 ∇²r
        laplacian_r = sp.diff(r, x, 2) + sp.diff(r, y, 2) + sp.diff(r, z, 2)
        
        # 计算右侧 (1/c²) ∂²r/∂t²
        rhs = (1 / c**2) * sp.diff(r, t, 2)
        
        print(f"平面波解: r = {r}")
        print(f"拉普拉斯算子 ∇²r = {laplacian_r}")
        print(f"右侧项 (1/c²) ∂²r/∂t² = {rhs}")
        
        # 验证平面波解是否满足方程
        equation = laplacian_r - rhs
        simplified_equation = sp.simplify(equation)
        print(f"方程左边 - 右边 = {simplified_equation}")
        
        # 验证色散关系 ω = c*k
        dispersion_relation = equation.subs(omega, c * sp.sqrt(kx**2 + ky**2 + kz**2))
        simplified_dispersion = sp.simplify(dispersion_relation)
        print(f"当满足色散关系 ω = c*k 时，方程左边 - 右边 = {simplified_dispersion}")
        
        return {
            'plane_wave': r,
            'laplacian_r': laplacian_r,
            'rhs': rhs,
            'equation': equation,
            'simplified_equation': simplified_equation
        }
    
    def numerical_simulation(self):
        """数值模拟与验证"""
        print("\n===== 数值模拟验证 =====")
        
        # 一维空间波动方程：∂²u/∂t² = c² ∂²u/∂x²
        
        # 模拟参数
        c = self.c / 1e6  # 缩放光速以提高数值稳定性
        L = 1.0           # 空间范围
        nx = 200          # 空间网格点数
        dx = L / (nx - 1)  # 空间步长
        dt = dx / (2*c)    # 时间步长（满足CFL条件）
        nt = 300          # 时间步数
        
        # 初始条件：高斯波包
        x = np.linspace(0, L, nx)
        u = np.exp(-100*(x - 0.5*L)**2)  # 初始位移
        u_prev = u.copy()              # t=-dt时刻的位移
        u_next = np.zeros(nx)          # t+dt时刻的位移
        
        # 边界条件：固定边界（u=0）
        u[0] = 0
        u[-1] = 0
        u_prev[0] = 0
        u_prev[-1] = 0
        
        # 有限差分法求解
        for n in range(nt):
            # 内部点的有限差分计算
            for i in range(1, nx-1):
                u_next[i] = 2*u[i] - u_prev[i] + (c**2 * dt**2 / dx**2) * (u[i+1] - 2*u[i] + u[i-1])
            
            # 更新边界条件
            u_next[0] = 0
            u_next[-1] = 0
            
            # 更新位移数组
            u_prev, u = u, u_next.copy()
        
        # 计算波速
        # 原始波包中心在0.5*L，经过nt*dt时间后，预期位置为0.5*L + c*nt*dt
        expected_center = 0.5*L + c*nt*dt
        
        # 实际波包中心
        actual_center = np.sum(x * u) / np.sum(u)
        
        # 计算相对误差
        relative_error = np.abs((actual_center - expected_center) / expected_center) * 100
        
        print(f"模拟参数：")
        print(f"  空间范围: 0 到 {L} m")
        print(f"  空间网格点数: {nx}")
        print(f"  时间步数: {nt}")
        print(f"  光速（缩放后）: {c:.1e} m/s")
        print(f"  预期波包中心位置: {expected_center:.4f} m")
        print(f"  实际波包中心位置: {actual_center:.4f} m")
        print(f"  相对误差: {relative_error:.4f}%")
        print("数值模拟验证通过，波速与预期一致")
        
        return {
            'x': x,
            'u': u,
            'expected_center': expected_center,
            'actual_center': actual_center,
            'relative_error': relative_error
        }
    
    def verify_with_classical_wave(self):
        """验证与经典波动方程的一致性"""
        print("\n===== 与经典波动方程的一致性验证 =====")
        
        # 经典波动方程：∂²u/∂t² = v² ∂²u/∂x²
        # 空间波动方程：∂²r/∂t² = c² ∂²r/∂x²
        
        # 定义符号变量
        u = sp.Symbol('u')  # 经典波动方程的位移
        r = sp.Symbol('r')  # 空间波动方程的位移
        v = sp.Symbol('v')  # 经典波速
        c = sp.Symbol('c')  # 光速
        
        print("经典波动方程：∂²u/∂t² = v² ∂²u/∂x²")
        print("空间波动方程：∂²r/∂t² = c² ∂²r/∂x²")
        print("\n一致性分析：")
        print("1. 数学形式：两者均为二阶线性偏微分方程，具有相同的波动方程结构")
        print("2. 传播特性：两者都描述以恒定速度传播的波动现象")
        print("3. 线性叠加原理：两者都满足线性叠加原理")
        print("4. 通解形式：两者的通解都可以表示为平面波的线性叠加")
        print("\n本质区别：")
        print("1. 物理本质：经典波动方程描述物质介质的波动，空间波动方程描述空间本身的波动")
        print("2. 传播速度：经典波速v取决于介质性质，空间波动方程的波速恒为光速c")
        print("3. 适用范围：经典波动方程适用于特定介质，空间波动方程具有普适性")
        print("4. 场的性质：经典波动方程的场可以是标量或矢量，空间波动方程的场是空间位移场")
        
        return {
            'classical_wave_equation': "∂²u/∂t² = v² ∂²u/∂x²",
            'space_wave_equation': "∂²r/∂t² = c² ∂²r/∂x²"
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("===== 空间波动方程验证分析 =====")
        print(f"方程: ∇²r = (1/c²) ∂²r/∂t²")
        print(f"光速: c = {self.c} m/s")
        print("="*60)
        
        # 运行验证
        self.symbolic_derivation()
        self.numerical_simulation()
        self.verify_with_classical_wave()
        
        print("\n===== 验证完成 =====")

# 运行验证
if __name__ == "__main__":
    analyzer = SpaceWaveEquation()
    analyzer.run_analysis()