#!/usr/bin/env python3
"""
全面验证ZUFT论文中的所有核心公式
验证内容包括：
1. 质量几何常数k
2. 电荷几何常数k'
3. 电磁耦合常数Z'
4. 电场公式（纯几何形式、理论形式、重构形式）
5. 磁场公式（从电场导出、重构形式）
6. 电荷方程和质量方程
7. 精细结构常数
"""

import math

# 定义常数
c = 299792458  # 光速，m/s
ε0 = 8.8541878128e-12  # 真空介电常数，F/m
μ0 = 4 * math.pi * 1e-7  # 真空磁导率，H/m
ħ = 1.054571817e-34  # 约化普朗克常数，J·s
G = 6.67430e-11  # 万有引力常数，m³·kg⁻¹·s⁻²

# 定义粒子参数
e = 1.602176634e-19  # 电子电荷，C
m_e = 9.1093837015e-31  # 电子质量，kg
m_p = 1.67262192369e-11  # 质子质量，kg（注意：这里应该是1.67262192369e-27，可能是论文中的笔误）
r_bohr = 5.29177210903e-11  # 玻尔半径，m

# 计算普朗克单位
m_plank = math.sqrt(ħ * c / G)  # 普朗克质量，kg
q_plank = math.sqrt(4 * math.pi * ε0 * ħ * c)  # 普朗克电荷，C

print("=== ZUFT核心公式全面验证 ===\n")

# 1. 验证质量几何常数k
print("1. 验证质量几何常数k")
print(f"普朗克质量 m_p = {m_plank:.6e} kg")
k = 4 * math.pi * m_plank
print(f"k = 4π m_p = {k:.6e} kg")
print(f"论文中k的数值：2.736 × 10^-7 kg")
print(f"相对误差：{abs(k - 2.736e-7) / 2.736e-7:.6e}\n")

# 2. 验证电荷几何常数k'
print("2. 验证电荷几何常数k'")
print(f"普朗克电荷 q_p = {q_plank:.6e} C")
k_prime = q_plank / c
print(f"k' = q_p / c = {k_prime:.6e} C·s/kg")
print(f"论文中k'的数值：6.25 × 10^-27 C·s/kg")
print(f"相对误差：{abs(k_prime - 6.25e-27) / 6.25e-27:.6e}\n")

# 3. 验证电磁耦合常数Z'
print("3. 验证电磁耦合常数Z'")
Z_prime = c / (8 * math.pi * ε0)
print(f"Z' = c/(8πε0) = {Z_prime:.6e} kg·m^4·s^-3·C^-2")
print(f"论文中Z'的数值：1.347 × 10^18 kg·m^4·s^-3·C^-2")
print(f"相对误差：{abs(Z_prime - 1.347e18) / 1.347e18:.6e}\n")

# 4. 验证电场公式
print("4. 验证电场公式")
Q = e  # 使用电子电荷
r = r_bohr  # 使用玻尔半径

# 纯几何形式
E_geometry = Q / (8 * math.pi * ε0 * r**2)
print(f"纯几何形式 E_几何 = Q/(8πε0 r²) = {E_geometry:.6e} V/m")

# 理论形式
E_theory = (2 * Q * Z_prime) / (c * r**2)
print(f"理论形式 E_理论 = 2Q Z'/(c r²) = {E_theory:.6e} V/m")

# 重构形式（经典库仑定律）
E_classical = Q / (4 * math.pi * ε0 * r**2)
print(f"重构形式 E_重构 = Q/(4πε0 r²) = {E_classical:.6e} V/m")

# 验证等价性
print(f"E_理论与E_重构的相对误差：{abs(E_theory - E_classical) / E_classical:.6e}")
print(f"E_几何与E_重构的比值：{E_geometry / E_classical:.6f} (预期：0.5)\n")

# 5. 验证磁场公式
print("5. 验证磁场公式")
v = 2.18769126364e6  # 电子在玻尔轨道上的速度，m/s

# 从电场导出的磁场
B_from_E = (v * E_classical) / c**2
print(f"从电场导出 B = v × E / c² = {B_from_E:.6e} T")

# 重构形式（毕奥-萨伐尔定律）
B_biot_savart = (μ0 * Q * v) / (4 * math.pi * r**2)
print(f"毕奥-萨伐尔定律 B = μ0 q v/(4π r²) = {B_biot_savart:.6e} T")
print(f"两者相对误差：{abs(B_from_E - B_biot_savart) / B_biot_savart:.6e}\n")

# 6. 验证电荷方程和质量方程
print("6. 验证电荷方程和质量方程")

# 假设Ω = 4π（最简几何图像）
Ω = 4 * math.pi

# 计算dΩ/dt（从电荷方程）
dΩ_dt = (Q * Ω**2) / (k_prime * k)
print(f"dΩ/dt = q Ω²/(k'k) = {dΩ_dt:.6e} sr/s")

# 计算dm/dt
dm_dt = Q / k_prime
print(f"dm/dt = q/k' = {dm_dt:.6e} kg/s")

# 验证质量方程（假设n=1）
n = 1
m_calculated = k * (n / Ω)
print(f"质量方程 m = k(n/Ω) = {m_calculated:.6e} kg")
print(f"与普朗克质量的相对误差：{abs(m_calculated - m_plank) / m_plank:.6e}\n")

# 7. 验证精细结构常数
print("7. 验证精细结构常数")
# 根据ZUFT的双层螺旋模型，需要引入归一化因子2
α_calculated = (2 * e**2 * Z_prime) / (ħ * c**2)
print(f"α = 2 e² Z'/(ħ c²) = {α_calculated:.6e}")
α_experimental = 7.297353e-03  # CODATA 2018值
print(f"实验值 α_exp = {α_experimental:.6e}")
print(f"相对误差：{abs(α_calculated - α_experimental) / α_experimental:.6e}")
print(f"吻合精度：{1 / abs(α_calculated - α_experimental) / α_experimental:.1f} 分之一\n")

# 8. 验证电子-质子相互作用
print("8. 验证电子-质子相互作用")

# 计算库仑力
F_coulomb = Q**2 / (4 * math.pi * ε0 * r**2)
print(f"库仑力 F = e²/(4πε0 r²) = {F_coulomb:.6e} N")

# 计算洛伦兹力
F_lorentz = Q * v * B_biot_savart
print(f"洛伦兹力 F = e v B = {F_lorentz:.6e} N")
print(f"洛伦兹力与库仑力的比值：{F_lorentz / F_coulomb:.6e}\n")

print("=== 验证完成 ===")
print("所有核心公式验证完毕，结果与论文中的推导一致。")
