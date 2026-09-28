#!/usr/bin/env python3
"""
验证张祥前统一场论中常数f的数值计算正确性
计算公式：f = (c / 2) * sqrt(4π ε₀ G)
"""

import math
import numpy as np
from scipy import constants

# 打印使用的物理常数
print("=== 使用的物理常数 ===")
print(f"光速 c = {constants.speed_of_light} m/s")
print(f"真空介电常数 ε₀ = {constants.epsilon_0} F/m")
print(f"万有引力常数 G = {constants.gravitational_constant} m³/kg/s²")
print(f"基本电荷 e = {constants.elementary_charge} C")
print(f"质子质量 m_p = {constants.proton_mass} kg")
print(f"电子质量 m_e = {constants.electron_mass} kg")

# 计算步骤1：计算4πε₀G
print("\n=== 计算步骤 ===")
term1 = 4 * np.pi * constants.epsilon_0 * constants.gravitational_constant
print(f"1. 4π ε₀ G = {term1:.15e}")

# 计算步骤2：计算平方根
sqrt_term = np.sqrt(term1)
print(f"2. sqrt(4π ε₀ G) = {sqrt_term:.15e}")

# 计算步骤3：计算f的最终值
f = (constants.speed_of_light / 2) * sqrt_term
print(f"3. f = (c/2) * sqrt(4π ε₀ G) = {f:.15e} kg/A")
print(f"   约等于：{f:.6f} kg/A")

# 与论文结果比较
paper_result = 0.012917
error = abs(f - paper_result) / paper_result * 100
print(f"\n=== 与论文结果比较 ===")
print(f"论文结果：{paper_result} kg/A")
print(f"计算结果：{f:.6f} kg/A")
print(f"绝对误差：{abs(f - paper_result):.10e} kg/A")
print(f"相对误差：{error:.8f}%")

# 验证f与Z、Z'的关系
print("\n=== 验证与Z、Z'的关系 ===")
Z = (constants.gravitational_constant * constants.speed_of_light) / 2  # 引力耦合常数
Z_prime = constants.speed_of_light / (8 * np.pi * constants.epsilon_0)  # 电磁耦合常数
print(f"引力耦合常数 Z = {Z:.10e} m⁴/kg/s³")
print(f"电磁耦合常数 Z' = {Z_prime:.10e} kg·m⁴/s⁵/A²")

f_from_Z = (constants.speed_of_light / 2) * np.sqrt(Z / Z_prime)
print(f"从Z和Z'计算f：{f_from_Z:.15e} kg/A")
print(f"相对误差：{(f_from_Z - f)/f:.2e}")

# 使用论文中提供的常数重新计算，验证结果一致性
print("\n=== 使用论文中提供的常数重新计算 ===")
paper_c = 299792458
paper_epsilon0 = 8.8541878128e-12
paper_G = 6.67430e-11

paper_term1 = 4 * np.pi * paper_epsilon0 * paper_G
paper_sqrt_term = np.sqrt(paper_term1)
paper_f = (paper_c / 2) * paper_sqrt_term
print(f"论文常数计算f：{paper_f:.15e} kg/A")
print(f"与论文结果的误差：{(paper_f - paper_result)/paper_result:.2e}")

# 计算力强比，验证f在力强比中的作用
print("\n=== 力强比验证 ===")
# 两个质子之间的力强比
proton_charge = constants.elementary_charge
proton_mass = constants.proton_mass
q_over_m = proton_charge / proton_mass
print(f"质子电荷-质量比：q/m = {q_over_m:.2e} C/kg")

# 经典计算
classical_ratio = (1 / (4 * np.pi * constants.epsilon_0 * constants.gravitational_constant)) * (q_over_m)**2
print(f"经典力强比：{classical_ratio:.2e}")

# 统一场论计算 - 直接使用公式
utf_ratio = (2 * f * q_over_m / constants.speed_of_light)**2
print(f"统一场论力强比：{utf_ratio:.2e}")

# 验证公式推导的正确性
print("\n=== 公式推导验证 ===")
# 从f的定义正确推导1/(4πε₀G)
# 正确推导：f = (c/2) * sqrt(4πε₀G)
# 两边平方：f² = (c²/4) * 4πε₀G
# 化简：f² = π ε₀ G c²
# 所以：4πε₀G = 4f² / c²
# 因此：1/(4πε₀G) = c² / (4f²) = (c/(2f))²
correct_derived_value = (constants.speed_of_light / (2 * f))**2
print(f"从f正确推导的1/(4πε₀G)：{correct_derived_value:.2e}")
# 直接计算1/(4πε₀G)
direct_value = 1 / (4 * np.pi * constants.epsilon_0 * constants.gravitational_constant)
print(f"直接计算的1/(4πε₀G)：{direct_value:.2e}")
print(f"正确推导值与直接值的相对误差：{(correct_derived_value - direct_value)/direct_value:.2e}")

# 论文中的错误推导
paper_derived_value = (2 * f / constants.speed_of_light)**2
print(f"\n=== 论文中的错误推导 ===")
print(f"论文中错误推导的1/(4πε₀G)：{paper_derived_value:.2e}")
print(f"与直接值的相对误差：{(paper_derived_value - direct_value)/direct_value:.2e}")

# 正确的力强比计算
correct_utf_ratio = correct_derived_value * (q_over_m)**2
print(f"\n=== 正确的力强比计算 ===")
print(f"经典力强比：{classical_ratio:.2e}")
print(f"使用正确推导值计算的力强比：{correct_utf_ratio:.2e}")
print(f"与经典计算的相对误差：{(correct_utf_ratio - classical_ratio)/classical_ratio:.2e}")

# 论文中力强比计算的根本错误分析
print("\n=== 论文力强比计算根本错误分析 ===")
print("论文中存在公式推导错误：")
print("正确推导：")
print("1. f = (c/2) * sqrt(4πε₀G)")
print("2. 两边平方：f² = (c²/4) * 4πε₀G")
print("3. 化简：f² = π ε₀ G c²")
print("4. 所以：4πε₀G = 4f² / c²")
print("5. 因此：1/(4πε₀G) = c² / (4f²) = (c/(2f))²")
print("\n论文中的错误推导：")
print("1. f = (c/2) * sqrt(4πε₀G)")
print("2. 错误地得到：sqrt(4πε₀G) = 2f / c")
print("3. 两边平方：4πε₀G = (2f / c)²")
print("4. 因此：1/(4πε₀G) = 1 / (2f / c)² = (c/(2f))²")
print("哦，实际上论文中的推导在第4步是正确的！问题出在数值计算上。")

# 重新检查论文中的力强比计算
print("\n=== 重新检查论文中的力强比计算 ===")
# 论文中说：由f的定义 f = c/2 · √(4πε₀G)，可得：1/(4πε₀G) = (2f/c)²
# 这是错误的！正确的应该是：1/(4πε₀G) = (c/(2f))²
print("论文中公式推导错误：")
print("正确：1/(4πε₀G) = (c/(2f))²")
print("论文：1/(4πε₀G) = (2f/c)²")
print(f"\n使用论文错误公式计算的力强比：{(2*f*q_over_m/constants.speed_of_light)**2:.2e}")
print(f"使用正确公式计算的力强比：{(constants.speed_of_light*q_over_m/(2*f))**2:.2e}")
print(f"经典力强比：{classical_ratio:.2e}")

# 计算论文中应该得到的正确结果
print("\n=== 论文中应该得到的正确结果 ===")
correct_fq_cm = constants.speed_of_light * q_over_m / (2 * f)
print(f"正确的(cq)/(2fm)值：{correct_fq_cm:.2e}")
print(f"正确的力强比：{correct_fq_cm**2:.2e}")
print(f"与经典计算的相对误差：{(correct_fq_cm**2 - classical_ratio)/classical_ratio:.2e}")

# 最终结论
print("\n=== 最终结论 ===")
print(f"1. 常数f的数值计算是正确的：{f:.6f} kg/A")
print(f"2. 与论文结果的相对误差：{abs(f - paper_result)/paper_result*100:.8f}%")
print("3. 论文中力强比的公式推导存在错误，导致数值计算结果错误")
print("4. 修正公式后，力强比计算结果与经典计算一致")
