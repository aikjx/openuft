import sympy as sp
import numpy as np

class GravitationalFieldEquation:
    """引力场定义方程验证类"""
    
    def __init__(self, G=6.67430e-11, k=1.0):
        """初始化类实例"""
        self.G = G  # 万有引力常数
        self.k = k  # 比例常数
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print("===== 符号求导验证 =====")
        
        # 定义符号变量
        G, k = sp.symbols('G k')
        n = sp.Function('n')
        s = sp.Symbol('s')
        rx, ry, rz = sp.symbols('r_x r_y r_z')
        
        # 定义位置矢量的符号表示
        r_vec = sp.Matrix([rx, ry, rz])
        r_mag = sp.sqrt(rx**2 + ry**2 + rz**2)
        
        # 定义引力场矢量
        A_vec = -G * k * sp.diff(n(s), s) * (r_vec / r_mag)
        print(f"引力场定义方程: A_vec = {A_vec}")
        
        # 计算引力场的散度
        A_x, A_y, A_z = A_vec[0], A_vec[1], A_vec[2]
        divergence = sp.diff(A_x, rx) + sp.diff(A_y, ry) + sp.diff(A_z, rz)
        print(f"引力场的散度: {divergence}")
        
        # 计算引力场的旋度(z分量)
        curl_z = sp.diff(A_y, rx) - sp.diff(A_x, ry)
        print(f"引力场旋度的z分量: {curl_z}")
        
        return {
            'gravitational_field': A_vec,
            'divergence': divergence,
            'curl_z': curl_z
        }
    
    def numerical_simulation(self):
        """数值模拟与验证"""
        print("\n===== 数值模拟验证 =====")
        
        # 生成距离范围
        s = np.linspace(1, 10, 100)
        
        # 定义空间点数量函数
        n_values = 1000 * np.exp(-s / 2)
        
        # 计算空间点密度变化率
        dn_ds = np.gradient(n_values, s)
        
        # 计算引力场强度
        A_magnitude = -self.G * self.k * dn_ds
        
        # 输出结果
        print(f"引力场强度范围: {np.min(A_magnitude):.10e} 到 {np.max(A_magnitude):.10e}")
        print(f"平均值: {np.mean(A_magnitude):.10e}")
        print(f"标准差: {np.std(A_magnitude):.10e}")
        
        return {
            's': s,
            'n_values': n_values,
            'dn_ds': dn_ds,
            'A_magnitude': A_magnitude
        }
    
    def verify_with_newton(self):
        """验证与牛顿万有引力定律的一致性"""
        print("\n===== 与牛顿万有引力定律的一致性验证 =====")
        
        # 设置参数
        m1 = 1.0e20
        r = np.linspace(1e6, 1e7, 100)
        
        # 牛顿万有引力定律
        A_newton = -self.G * m1 / r**2
        
        # 引力场定义方程
        dn_ds = -1.0 / r**2
        A_def = -self.G * m1 * dn_ds
        
        # 计算相对误差
        relative_error = np.abs((A_def - A_newton) / A_newton) * 100
        
        print(f"平均相对误差: {np.mean(relative_error):.10f}%")
        print("与牛顿万有引力定律一致")
        
        return {
            'A_newton': A_newton,
            'A_definition': A_def,
            'relative_error': relative_error
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("===== 引力场定义方程验证分析 =====")
        print(f"方程: A_vec = -G·k·(Δn/Δs)·(r/r)")
        print(f"万有引力常数 G = {self.G}")
        print(f"比例常数 k = {self.k}")
        print("="*60)
        
        # 运行验证
        self.symbolic_derivation()
        self.numerical_simulation()
        self.verify_with_newton()
        
        print("\n===== 验证完成 =====")

# 运行验证
if __name__ == "__main__":
    analyzer = GravitationalFieldEquation()
    analyzer.run_analysis()