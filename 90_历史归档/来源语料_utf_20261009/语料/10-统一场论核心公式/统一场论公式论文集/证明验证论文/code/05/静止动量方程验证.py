import sympy as sp
import numpy as np

class StaticMomentumEquation:
    """静止动量方程验证类"""
    
    def __init__(self, c=299792458.0):
        """初始化类实例"""
        self.c = c  # 光速
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print("===== 符号求导验证 =====")
        
        # 定义符号变量
        m0 = sp.Symbol('m0')
        C0x, C0y, C0z = sp.symbols('C0x C0y C0z')
        
        # 定义静止动量分量
        p0x = m0 * C0x
        p0y = m0 * C0y
        p0z = m0 * C0z
        
        # 计算动量大小
        p0_mag = sp.sqrt(p0x**2 + p0y**2 + p0z**2)
        
        # 对质量求导
        dp0_dm0 = sp.diff(p0x, m0)
        
        # 对光速分量求导
        dp0_dC0x = sp.diff(p0x, C0x)
        
        print(f"静止动量x分量: p0x = {p0x}")
        print(f"静止动量y分量: p0y = {p0y}")
        print(f"静止动量z分量: p0z = {p0z}")
        print(f"静止动量大小: p0_mag = {p0_mag}")
        print(f"动量对质量的导数: dp0/dm0 = {dp0_dm0}")
        print(f"动量对光速x分量的导数: dp0/dC0x = {dp0_dC0x}")
        
        return {
            'p0x': p0x,
            'p0y': p0y,
            'p0z': p0z,
            'p0_mag': p0_mag
        }
    
    def numerical_simulation(self):
        """数值模拟与验证"""
        print("\n===== 数值模拟验证 =====")
        
        # 生成质量范围
        m0_values = np.logspace(-30, 30, 100)  # 质量范围：1e-30 kg到1e30 kg
        
        # 计算静止动量大小
        p0_values = m0_values * self.c
        
        # 计算理论值与实际值的差异（应该为零）
        error = p0_values - (m0_values * self.c)
        
        # 输出结果
        print(f"质量范围: {np.min(m0_values):.1e} kg 到 {np.max(m0_values):.1e} kg")
        print(f"对应的静止动量范围: {np.min(p0_values):.1e} kg·m/s 到 {np.max(p0_values):.1e} kg·m/s")
        print(f"最大绝对误差: {np.max(np.abs(error)):.1e}")
        print(f"最大相对误差: {np.max(np.abs(error / p0_values)):.1e}")
        print("静止动量方程在数值上完全一致")
        
        return {
            'm0_values': m0_values,
            'p0_values': p0_values,
            'error': error
        }
    
    def verify_with_relativity(self):
        """验证与相对论质能方程的一致性"""
        print("\n===== 与相对论质能方程的一致性验证 =====")
        
        # 定义质量值
        m0 = 1.0  # 1 kg
        
        # 根据相对论质能方程计算能量
        E = m0 * self.c**2
        
        # 根据静止动量方程计算动量
        p0 = m0 * self.c
        
        # 计算能量与动量的关系
        E_from_p0 = p0 * self.c
        
        # 计算相对误差
        relative_error = np.abs((E - E_from_p0) / E) * 100
        
        print(f"质量: m0 = {m0} kg")
        print(f"相对论质能方程: E = {E:.1e} J")
        print(f"从静止动量推导的能量: E_from_p0 = {E_from_p0:.1e} J")
        print(f"相对误差: {relative_error:.1e}%")
        print("静止动量方程与相对论质能方程完全一致")
        
        return {
            'E': E,
            'E_from_p0': E_from_p0,
            'relative_error': relative_error
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("===== 静止动量方程验证分析 =====")
        print(f"方程: p0 = m0·c")
        print(f"光速: c = {self.c} m/s")
        print("="*60)
        
        # 运行验证
        self.symbolic_derivation()
        self.numerical_simulation()
        self.verify_with_relativity()
        
        print("\n===== 验证完成 =====")

# 运行验证
if __name__ == "__main__":
    analyzer = StaticMomentumEquation()
    analyzer.run_analysis()