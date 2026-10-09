import sympy as sp
import numpy as np

class MotionMomentumEquation:
    """运动动量方程验证类"""
    
    def __init__(self, c=299792458.0):
        """初始化类实例"""
        self.c = c  # 光速
    
    def symbolic_derivation(self):
        """使用SymPy进行符号求导验证"""
        print("===== 符号求导验证 =====")
        
        # 定义符号变量
        m = sp.Symbol('m')
        Cx, Cy, Cz = sp.symbols('Cx Cy Cz')
        Vx, Vy, Vz = sp.symbols('Vx Vy Vz')
        
        # 定义动量分量 P = m(C - V)
        Px = m * (Cx - Vx)
        Py = m * (Cy - Vy)
        Pz = m * (Cz - Vz)
        
        # 计算动量大小
        P_mag = sp.sqrt(Px**2 + Py**2 + Pz**2)
        
        # 对质量求导
        dP_dm = sp.diff(Px, m)
        
        # 对速度分量求导
        dP_dVx = sp.diff(Px, Vx)
        
        print(f"运动动量x分量: Px = {Px}")
        print(f"运动动量y分量: Py = {Py}")
        print(f"运动动量z分量: Pz = {Pz}")
        print(f"运动动量大小: P_mag = {P_mag}")
        print(f"动量对质量的导数: dP/dm = {dP_dm}")
        print(f"动量对速度x分量的导数: dP/dVx = {dP_dVx}")
        
        # 验证静止动量的情况（V=0）
        Px_rest = Px.subs({Vx: 0, Vy: 0, Vz: 0})
        print(f"静止动量x分量（V=0）: Px_rest = {Px_rest}")
        
        return {
            'Px': Px,
            'Py': Py,
            'Pz': Pz,
            'P_mag': P_mag
        }
    
    def numerical_simulation(self):
        """数值模拟与验证"""
        print("\n===== 数值模拟验证 =====")
        
        # 生成速度范围（从0到0.9c）
        v_values = np.linspace(0, 0.9*self.c, 100)
        
        # 定义质量
        m = 1.0  # 1 kg
        
        # 矢量光速方向沿x轴
        Cx = self.c
        Cy = 0.0
        Cz = 0.0
        
        # 计算动量分量
        Px_values = m * (Cx - v_values)
        Py_values = m * Cy  # 速度沿x轴，y分量为0
        Pz_values = m * Cz  # 速度沿x轴，z分量为0
        
        # 计算动量大小
        P_mag_values = np.sqrt(Px_values**2 + Py_values**2 + Pz_values**2)
        
        # 与传统动量的比较
        P_traditional = m * v_values
        
        # 输出结果
        print(f"速度范围: 0 到 {0.9*self.c:.1e} m/s")
        print(f"运动动量x分量范围: {np.min(Px_values):.1e} 到 {np.max(Px_values):.1e} kg·m/s")
        print(f"最大动量大小: {np.max(P_mag_values):.1e} kg·m/s")
        print(f"静止动量大小（V=0）: {P_mag_values[0]:.1e} kg·m/s")
        print(f"传统动量与运动动量的关系: 当v << c时，P_traditional << P_rest")
        
        return {
            'v_values': v_values,
            'Px_values': Px_values,
            'P_mag_values': P_mag_values,
            'P_traditional': P_traditional
        }
    
    def verify_with_relativity(self):
        """验证与相对论质能方程的一致性"""
        print("\n===== 与相对论的一致性验证 =====")
        
        # 定义符号变量
        m0 = sp.Symbol('m0')  # 静止质量
        v = sp.Symbol('v')    # 物体速度
        c = sp.Symbol('c')    # 光速
        
        # 运动动量方程的动量大小
        P_mag = m0 * sp.sqrt(c**2 - 2*c*v + v**2)
        
        # 相对论质速关系
        m_rel = m0 / sp.sqrt(1 - v**2/c**2)
        
        # 相对论动量大小
        P_rel = m_rel * v
        
        print(f"运动动量大小: P_mag = {P_mag}")
        print(f"相对论质量: m_rel = {m_rel}")
        print(f"相对论动量: P_rel = {P_rel}")
        
        # 验证低速情况下的近似
        P_low_v = P_mag.series(v, 0, 3)  # 泰勒展开到v²项
        print(f"低速情况下的动量近似: P_low_v = {P_low_v}")
        
        return {
            'P_mag': P_mag,
            'm_rel': m_rel,
            'P_rel': P_rel,
            'P_low_v': P_low_v
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("===== 运动动量方程验证分析 =====")
        print(f"方程: P = m(C - V)")
        print(f"光速: c = {self.c} m/s")
        print("="*60)
        
        # 运行验证
        self.symbolic_derivation()
        self.numerical_simulation()
        self.verify_with_relativity()
        
        print("\n===== 验证完成 =====")

# 运行验证
if __name__ == "__main__":
    analyzer = MotionMomentumEquation()
    analyzer.run_analysis()