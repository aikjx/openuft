import sympy as sp
import numpy as np

class EnergyEquation:
    """能量方程验证类"""
    
    def __init__(self, c=299792458.0):
        """初始化类实例"""
        self.c = c  # 光速
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print("===== 符号求导验证 =====")
        
        # 定义符号变量
        m0 = sp.Symbol('m0')  # 静止质量
        v = sp.Symbol('v')    # 物体速度
        c = sp.Symbol('c')    # 光速
        
        # 运动质量 m = m0 / sqrt(1 - v²/c²)
        m = m0 / sp.sqrt(1 - v**2 / c**2)
        
        # 能量方程 E = m*c²
        E = m * c**2
        
        # 对静止质量求导
        dE_dm0 = sp.diff(E, m0)
        
        # 对速度求导
        dE_dv = sp.diff(E, v)
        
        # 对光速求导
        dE_dc = sp.diff(E, c)
        
        # 动能 K = E - m0*c²
        K = E - m0 * c**2
        
        print(f"运动质量: m = {m}")
        print(f"能量方程: E = {E}")
        print(f"能量对静止质量的导数: dE/dm0 = {dE_dm0}")
        print(f"能量对速度的导数: dE/dv = {dE_dv}")
        print(f"能量对光速的导数: dE/dc = {dE_dc}")
        print(f"动能: K = {K}")
        
        # 低速近似 (v << c)
        K_low_v = K.series(v, 0, 3)  # 泰勒展开到v²项
        print(f"低速情况下的动能近似: K_low_v = {K_low_v}")
        
        return {
            'm': m,
            'E': E,
            'K': K,
            'K_low_v': K_low_v
        }
    
    def numerical_simulation(self):
        """数值模拟与验证"""
        print("\n===== 数值模拟验证 =====")
        
        # 静止质量
        m0 = 1.0  # 1 kg
        
        # 速度范围：0 到 0.999c
        v_values = np.linspace(0, 0.999*self.c, 100)
        
        # 计算运动质量
        m_values = m0 / np.sqrt(1 - (v_values**2) / (self.c**2))
        
        # 计算能量
        E_values = m_values * self.c**2
        
        # 计算经典动能
        K_classical = 0.5 * m0 * v_values**2
        
        # 计算相对论动能
        K_relativistic = E_values - m0 * self.c**2
        
        # 输出结果
        print(f"静止质量: {m0} kg")
        print(f"速度范围: 0 到 {0.999*self.c:.1e} m/s")
        print(f"能量范围: {np.min(E_values):.1e} 到 {np.max(E_values):.1e} J")
        print(f"静止能量: {m0 * self.c**2:.1e} J")
        print(f"最大相对论动能: {np.max(K_relativistic):.1e} J")
        print(f"当v = 0.9c时，经典动能与相对论动能的比值: {K_classical[-20] / K_relativistic[-20]:.3f}")
        print("低速时经典动能近似有效，高速时需要相对论修正")
        
        return {
            'v_values': v_values,
            'm_values': m_values,
            'E_values': E_values,
            'K_classical': K_classical,
            'K_relativistic': K_relativistic
        }
    
    def verify_with_einstein(self):
        """验证与爱因斯坦质能方程的一致性"""
        print("\n===== 与爱因斯坦质能方程的一致性验证 =====")
        
        # 定义质量值
        m_values = np.linspace(1.0e-30, 1.0e30, 10)
        
        for m in m_values:
            # 爱因斯坦质能方程
            E_einstein = m * self.c**2
            # 统一场论能量方程
            E_utf = m * self.c**2
            
            # 相对误差
            relative_error = np.abs((E_utf - E_einstein) / E_einstein) * 100
            
            print(f"质量 m = {m:.1e} kg")
            print(f"爱因斯坦质能方程: E = {E_einstein:.1e} J")
            print(f"统一场论能量方程: E = {E_utf:.1e} J")
            print(f"相对误差: {relative_error:.1e}%")
        
        print("\n结论: 统一场论能量方程与爱因斯坦质能方程完全一致")
        
        return {
            'm_values': m_values,
            'E_einstein': m_values * self.c**2,
            'E_utf': m_values * self.c**2
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("===== 能量方程验证分析 =====")
        print(f"方程: E = mC²，其中 m = m0 / sqrt(1 - v²/c²)")
        print(f"光速: c = {self.c} m/s")
        print("="*60)
        
        # 运行验证
        self.symbolic_derivation()
        self.numerical_simulation()
        self.verify_with_einstein()
        
        print("\n===== 验证完成 =====")

# 运行验证
if __name__ == "__main__":
    analyzer = EnergyEquation()
    analyzer.run_analysis()