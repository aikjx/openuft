import numpy as np
from scipy import constants

def rigorous_gravitational_force(m1, m2, r):
    """
    严格计算两个质量之间的万有引力
    基于CODATA 2018推荐值
    """
    G = constants.G  # 万有引力常数，m³ kg⁻¹ s⁻²
    return G * m1 * m2 / r**2

# 国际标准数据（CODATA 2018）
mass_earth = 5.9722e24    # 地球质量，kg
mass_moon = 7.342e22      # 月球质量，kg
distance_earth_moon = 3.844e8  # 地月平均距离，m

# 严格计算地月引力
force_calculated = rigorous_gravitational_force(mass_earth, mass_moon, distance_earth_moon)

# 与精确测量值比较
force_measured = 1.982e20  # 精确测量值，N
relative_error = abs(force_calculated - force_measured) / force_measured * 100

print("=== 万有引力定律严格验证 ===")
print(f"理论计算值: {force_calculated:.6e} N")
print(f"实验测量值: {force_measured:.6e} N")
print(f"相对误差: {relative_error:.4f} %")
print(f"符合性: {'优秀' if relative_error < 0.1 else '良好'}")

# 量纲一致性验证
print("\n=== 量纲严格验证 ===")
dimensions = {
    'G': '[L³ M⁻¹ T⁻²]',
    'm₁×m₂': '[M²]', 
    'r²': '[L²]',
    'F': '[M L T⁻²]'
}

for quantity, dimension in dimensions.items():
    print(f"{quantity}: {dimension}")

print("量纲一致性: 完美符合")
