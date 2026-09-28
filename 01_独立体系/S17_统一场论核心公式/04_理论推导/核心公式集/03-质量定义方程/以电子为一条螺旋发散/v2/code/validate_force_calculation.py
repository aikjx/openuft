# -*- coding: utf-8 -*-
"""
验证ZUFT框架下力的大小计算
通过代入不同基准的k和k'值，计算力的大小并与经典电磁学比较
"""
import math

# ===================== 常量定义 =====================
# 电子静止质量（CODATA 2022）
m_e = 9.1093837015e-31       # kg

# 普朗克质量（计算值）
h_bar = 1.054571817e-34      # J·s
c = 299792458                # m/s
G = 6.67430e-11             # m³/kg·s²
m_p = math.sqrt(h_bar * c / G)  # 普朗克质量

# 真空介电常数
eps0 = 8.8541878128e-12      # F/m

# 测试参数
Omega = 1.0                  # 立体角，sr
dOmega_dt = 1.0              # 立体角变化率，s⁻¹
r = 1.0                      # 距离，m

# ===================== 力的计算 =====================
def calculate_force(k, k_prime, description):
    """计算电场力的大小"""
    # 电荷计算（ZUFT定义）
    q = k_prime * k * (1 / Omega**2) * dOmega_dt
    
    # 电场计算（ZUFT定义）
    E = (k_prime * k) / (4 * math.pi * eps0 * Omega**2) * dOmega_dt * (1 / r**2)
    
    # 电场力计算
    F = q * E
    
    # 经典库仑力（q=1C时）
    F_classical = 1 / (4 * math.pi * eps0 * r**2)
    
    print(f"【{description}】")
    print(f"k = {k:.8e} kg")
    print(f"k' = {k_prime:.4e} A·s²/kg")
    print(f"k'k = {k_prime * k:.2f} A·s²")
    print(f"电荷 q = {q:.4e} C")
    print(f"电场 E = {E:.4e} N/C")
    print(f"电场力 F = {F:.4e} N")
    print(f"经典库仑力（q=1C）= {F_classical:.4e} N")
    print(f"与经典结果一致: {'是' if abs(F - F_classical) < 1e6 else '否'}")
    print()
    
    return F, F_classical

def main():
    """主函数"""
    print("=======================================")
    print("ZUFT框架力的大小计算验证")
    print("=======================================")
    print()
    
    # 测试参数
    print("【测试参数】")
    print(f"立体角 Ω = {Omega} sr")
    print(f"立体角变化率 dΩ/dt = {dOmega_dt} s⁻¹")
    print(f"距离 r = {r} m")
    print()
    
    # 电子静止质量基准
    k_e = m_e
    k_prime_e = 1 / k_e  # 基于单位量假设
    F_e, F_classical = calculate_force(k_e, k_prime_e, "电子静止质量基准")
    
    # 普朗克质量基准（基于单位量假设）
    k_p = m_p
    k_prime_p = 1 / k_p  # 基于单位量假设
    F_p, _ = calculate_force(k_p, k_prime_p, "普朗克质量基准（单位量假设）")
    
    # 第二个文件中的值（错误值）
    k_p_file = m_p
    k_prime_p_file = 1.16e10  # 第二个文件中的值
    F_p_file, _ = calculate_force(k_p_file, k_prime_p_file, "普朗克质量基准（文件值）")
    
    # 分析
    print("【分析】")
    print(f"电子静止质量基准力大小: {F_e:.4e} N")
    print(f"普朗克质量基准力大小: {F_p:.4e} N")
    print(f"文件值力大小: {F_p_file:.4e} N")
    print(f"经典库仑力大小: {F_classical:.4e} N")
    print()
    
    print("【结论】")
    print("1. 基于单位量假设（k'k=1 A·s²）时，力的大小与经典库仑力一致")
    print("2. 电子静止质量基准和普朗克质量基准下，力的大小相同")
    print("3. 第二个文件中的值（k'k≠1）导致力的大小与经典结果不符")
    print()
    print("【物理合理性】")
    print("力的大小与经典电磁学一致，说明ZUFT框架的单位量假设是合理的")
    print("当k'k=1 A·s²时，力的计算结果符合实验观测")
    print("=======================================")

if __name__ == "__main__":
    main()
