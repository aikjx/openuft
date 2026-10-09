import math

# CODATA 2018 常数
c = 299792458  # 光速，单位：m/s
epsilon_0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11  # 万有引力常数，单位：m³·kg⁻¹·s⁻²

# 计算 Z' = c/(8π ε₀)
def calculate_z_prime():
    z_prime = c / (8 * math.pi * epsilon_0)
    return z_prime

# 计算引力耦合常数 Z = Gc/2
def calculate_gravitational():
    z = (G * c) / 2
    return z

# 分析Z'与Z的对比
def analyze_comparison():
    z_prime = calculate_z_prime()
    z = calculate_gravitational()
    ratio = z_prime / z
    
    print(f"=== Z' 与 Z 的对比分析 ===")
    print(f"Z' = c/(8π ε₀) = {z_prime:.6e} kg·m⁴·s⁻⁵·A⁻²")
    print(f"Z = Gc/2 = {z:.6e} m⁴·kg⁻¹·s⁻³")
    print(f"Z'/Z = {ratio:.6e}")
    print(f"Z'/Z 近似值: {ratio:.2e}")
    
    print("\n=== 对称性分析 ===")
    print("1. 两者都以光速 c 为分子，体现了时空基本运动的统一性")
    print("2. 分母分别是与引力和电磁相关的经典常数（G 和 ε₀）乘以简单几何因子（2 和 8π）")
    print("3. 比值 Z'/Z ≈ 1.346×10²⁰，反映了时空两种运动模式（旋转与径向发散）内禀强度的巨大差异")
    
    return z_prime, z, ratio

if __name__ == "__main__":
    analyze_comparison()
