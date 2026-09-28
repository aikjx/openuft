import math

# 物理常数
c = 299792458  # 光速 (m/s)
G = 6.67430e-11  # 万有引力常数 (m^3/kg/s^2)
h = 6.62607015e-34  # 普朗克常数 (J·s)

# 普朗克长度
lp = math.sqrt(G * h / (2 * math.pi * c**3))
print(f"普朗克长度: {lp:.2e} m")

# 电子康普顿半径
re = 3.862e-13  # 论文中使用的值
print(f"电子康普顿半径: {re:.2e} m")

# 计算源头归一化恒等式在不同尺度的值
def calc_identity(r):
    T = 2 * math.pi * r / c
    nu = c / (2 * math.pi * r)
    return (4 * math.pi**2 * r**3 * c**2) / (G * T**2 * h * nu)

# 验证普朗克尺度
lp_val = calc_identity(lp)
print(f"\n1. 源头归一化恒等式验证:")
print(f"   普朗克尺度恒等式值: {lp_val:.6f}")

# 验证电子尺度
re_val = calc_identity(re)
print(f"   电子尺度恒等式值: {re_val:.2e}")
print(f"   电子尺度与1的偏差: {math.log10(re_val):.2f} 个数量级")

# 验证电子质量计算
re_m = (c**2 * re) / G
print(f"\n2. 电子质量计算验证:")
print(f"   计算值: {re_m:.2e} kg")
print(f"   实际值: 9.11e-31 kg")
print(f"   偏差: {math.log10(re_m / 9.11e-31):.2f} 个数量级")

# 验证元电荷计算
epsilon0 = 8.8541878128e-12  # 真空介电常数
m_e = 9.11e-31  # 电子质量
e_calc = math.sqrt(4 * math.pi * epsilon0 * G * m_e**2)
print(f"\n3. 元电荷计算验证:")
print(f"   计算值: {e_calc:.2e} C")
print(f"   实际值: 1.602e-19 C")
print(f"   偏差: {math.log10(e_calc / 1.602e-19):.2f} 个数量级")

# 验证真空能密度计算
rho_vac = c**7 / (4 * math.pi * G**2 * h)
print(f"\n4. 真空能密度计算验证:")
print(f"   计算值: {rho_vac:.2e} kg/m^3")
print(f"   观测值: 1e-26 kg/m^3")
print(f"   偏差: {math.log10(rho_vac / 1e-26):.2f} 个数量级")

# 验证循环定义问题
print(f"\n5. 循环定义验证:")
print("   质量定义: m = c^2 r / G")
print("   螺旋半径定义: r = G m / c^2")
print("   代入后: m = c^2 * (G m / c^2) / G = m，完全循环")

# 验证太阳自转角速度
M_sun = 1.989e30  # 太阳质量
r_sun = G * M_sun / c**2  # 论文中的太阳螺旋半径
omega_sun = c / r_sun  # 论文中的太阳角速度
print(f"\n6. 太阳自转角速度验证:")
print(f"   论文计算值: {omega_sun:.2e} rad/s (约 {omega_sun/(2*math.pi):.2e} 转/秒)")
print(f"   实际观测值: 2.9e-6 rad/s (约 1/27 天/转)")
print(f"   偏差: {math.log10(omega_sun / 2.9e-6):.2f} 个数量级")
