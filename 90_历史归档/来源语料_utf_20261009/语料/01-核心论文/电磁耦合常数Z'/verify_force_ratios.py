import math

# CODATA 2018 常数
c = 299792458  # 光速，单位：m/s
epsilon_0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11  # 万有引力常数，单位：m³·kg⁻¹·s⁻²
e = 1.602176634e-19  # 基本电荷，单位：C
m_p = 1.67262192369e-27  # 质子质量，单位：kg
m_e = 9.1093837015e-31  # 电子质量，单位：kg

# 计算 Z' = c/(8π ε₀)
def calculate_z_prime():
    z_prime = c / (8 * math.pi * epsilon_0)
    return z_prime

# 计算引力耦合常数 Z = Gc/2
def calculate_gravitational():
    z = (G * c) / 2
    return z

# 计算力强比谱系
def calculate_force_ratios():
    z_prime = calculate_z_prime()
    z = calculate_gravitational()
    ratio_z = z_prime / z
    
    print(f"=== 力强比谱系分析 ===")
    print(f"Z'/Z = {ratio_z:.6e}")
    print()
    
    # 质子-质子力强比
    q_p = e
    force_ratio_pp = ratio_z * (abs(q_p * q_p) / (m_p * m_p))
    print(f"质子-质子力强比 (F_e/F_g):")
    print(f"  |q1 q2|/(m1 m2) = {abs(q_p * q_p) / (m_p * m_p):.6e}")
    print(f"  F_e/F_g = {force_ratio_pp:.6e}")
    print(f"  近似值: {force_ratio_pp:.2e}")
    print()
    
    # 质子-电子力强比
    q_e = -e
    force_ratio_pe = ratio_z * (abs(q_p * q_e) / (m_p * m_e))
    print(f"质子-电子力强比 (F_e/F_g):")
    print(f"  |q1 q2|/(m1 m2) = {abs(q_p * q_e) / (m_p * m_e):.6e}")
    print(f"  F_e/F_g = {force_ratio_pe:.6e}")
    print(f"  近似值: {force_ratio_pe:.2e}")
    print()
    
    # 电子-电子力强比
    force_ratio_ee = ratio_z * (abs(q_e * q_e) / (m_e * m_e))
    print(f"电子-电子力强比 (F_e/F_g):")
    print(f"  |q1 q2|/(m1 m2) = {abs(q_e * q_e) / (m_e * m_e):.6e}")
    print(f"  F_e/F_g = {force_ratio_ee:.6e}")
    print(f"  近似值: {force_ratio_ee:.2e}")
    print()
    
    print("=== 力强比谱系总结 ===")
    print(f"质子-质子: ~{10**math.floor(math.log10(force_ratio_pp))}")
    print(f"质子-电子: ~{10**math.floor(math.log10(force_ratio_pe))}")
    print(f"电子-电子: ~{10**math.floor(math.log10(force_ratio_ee))}")
    print()
    print("与论文中提到的谱系一致：")
    print("质子-质子: ~10^36")
    print("质子-电子: ~10^39")
    print("电子-电子: ~10^42")
    
    return force_ratio_pp, force_ratio_pe, force_ratio_ee

if __name__ == "__main__":
    calculate_force_ratios()
