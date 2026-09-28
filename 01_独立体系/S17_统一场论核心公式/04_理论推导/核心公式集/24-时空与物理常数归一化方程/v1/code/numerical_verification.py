# 数值验证脚本

"""
验证修订版论文中的公式在实际数值计算中的正确性
"""

import math
import json

class FormulaVerifier:
    """公式验证器"""
    
    def __init__(self):
        """初始化物理常数"""
        # 物理常数（标准值）
        self.constants = {
            'c': 299792458,          # 光速 (m/s)
            'G': 6.67430e-11,         # 万有引力常数 (m³/kg/s²)
            'h': 6.62607015e-34,      # 普朗克常数 (J·s)
            'hbar': 1.054571817e-34,   # 约化普朗克常数 (J·s)
            'k_B': 1.380649e-23,       # 玻尔兹曼常数 (J/K)
            'epsilon0': 8.8541878128e-12,  # 真空介电常数 (F/m)
            'e': 1.602176634e-19,      # 元电荷 (C)
            'm_e': 9.1093837015e-31,   # 电子质量 (kg)
            'lambda_e': 2.42631023867e-12,  # 电子康普顿波长 (m)
            'M_sun': 1.98847e30,       # 太阳质量 (kg)
            'R_earth_orbit': 1.496e11,  # 地球公转轨道半径 (m)
            'T_earth_orbit': 3.154e7,   # 地球公转周期 (s)
            'm_earth': 5.972e24,       # 地球质量 (kg)
        }
    
    def verify_electron_properties(self):
        """验证电子相关属性"""
        c = self.constants['c']
        G = self.constants['G']
        m_e = self.constants['m_e']
        lambda_e = self.constants['lambda_e']
        epsilon0 = self.constants['epsilon0']
        e = self.constants['e']
        
        # 计算电子螺旋半径
        r_e = lambda_e / (2 * math.pi)
        
        # 计算电子角速度
        omega_e = c / r_e
        
        # 计算电子质量（基于几何公式）
        m_e_calc = (c**2 * r_e) / G
        
        # 计算元电荷（基于几何公式）
        e_calc = math.sqrt(4 * math.pi * epsilon0 * G * m_e**2)
        
        # 计算误差
        m_error = abs(m_e_calc - m_e) / m_e * 100
        e_error = abs(e_calc - e) / e * 100
        
        return {
            '电子螺旋半径 r_e': r_e,
            '电子角速度 ω_e': omega_e,
            '电子质量计算值 m_e': m_e_calc,
            '电子质量实际值 m_e': m_e,
            '元电荷计算值 e': e_calc,
            '元电荷实际值 e': e,
            '电子质量误差': m_error,
            '元电荷误差': e_error
        }
    
    def verify_solar_system(self):
        """验证太阳系相关属性"""
        c = self.constants['c']
        G = self.constants['G']
        M_sun = self.constants['M_sun']
        R_earth_orbit = self.constants['R_earth_orbit']
        T_earth_orbit = self.constants['T_earth_orbit']
        m_earth = self.constants['m_earth']
        
        # 计算太阳空间螺旋半径
        r_M = (G * M_sun) / (c**2)
        
        # 计算太阳角速度
        omega_M = c / r_M
        
        # 计算地球公转周期（基于开普勒第三定律）
        T_calc = 2 * math.pi * math.sqrt(R_earth_orbit**3 / (G * M_sun))
        
        # 计算地球公转向心力
        F = m_earth * omega_M**2 * r_M**3 / R_earth_orbit**2
        
        # 计算误差
        T_error = abs(T_calc - T_earth_orbit) / T_earth_orbit * 100
        
        return {
            '太阳空间螺旋半径 r_M': r_M,
            '太阳角速度 ω_M': omega_M,
            '地球公转周期计算值 T': T_calc,
            '地球公转周期实际值 T': T_earth_orbit,
            '地球公转向心力 F': F,
            '公转周期误差': T_error
        }
    
    def verify_black_hole(self):
        """验证黑洞相关属性"""
        c = self.constants['c']
        G = self.constants['G']
        h = self.constants['h']
        k_B = self.constants['k_B']
        M = self.constants['M_sun']  # 1倍太阳质量
        
        # 计算黑洞空间螺旋半径
        r = (G * M) / (c**2)
        
        # 计算黑洞角速度
        omega = c / r
        
        # 计算黑洞频率
        nu = omega / (2 * math.pi)
        
        # 计算黑洞霍金温度
        T_H = (h * nu) / (8 * math.pi * k_B)
        
        # 计算黑洞视界半径
        R_s = 2 * r
        
        return {
            '黑洞空间螺旋半径 r': r,
            '黑洞角速度 ω': omega,
            '黑洞频率 ν': nu,
            '黑洞霍金温度 T_H': T_H,
            '黑洞视界半径 R_s': R_s
        }
    
    def run_all_verifications(self):
        """运行所有验证"""
        results = {
            '微观系统（电子）': self.verify_electron_properties(),
            '宏观系统（太阳系）': self.verify_solar_system(),
            '宇观系统（黑洞）': self.verify_black_hole()
        }
        return results
    
    def print_results(self, results):
        """打印验证结果"""
        print("=== 数值验证结果 ===")
        
        for case_name, case_results in results.items():
            print(f"\n{case_name}:")
            for key, value in case_results.items():
                if '误差' in key:
                    print(f"  {key}: {value:.6f}%")
                else:
                    # 格式化数值输出
                    if abs(value) < 1e-6 or abs(value) > 1e6:
                        print(f"  {key}: {value:.6e}")
                    else:
                        print(f"  {key}: {value:.6f}")
        
        # 检查误差是否都小于1%
        all_accurate = True
        for case_name, case_results in results.items():
            for key, value in case_results.items():
                if '误差' in key and value > 1:
                    all_accurate = False
                    break
        
        print(f"\n=== 验证总结 ===")
        if all_accurate:
            print("✓ 所有验证结果误差均小于1%，符合预期")
        else:
            print("✗ 部分验证结果误差超过1%，需要检查")

if __name__ == '__main__':
    verifier = FormulaVerifier()
    results = verifier.run_all_verifications()
    verifier.print_results(results)
    
    # 保存结果到文件
    with open('verification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n验证结果已保存到 verification_results.json")
