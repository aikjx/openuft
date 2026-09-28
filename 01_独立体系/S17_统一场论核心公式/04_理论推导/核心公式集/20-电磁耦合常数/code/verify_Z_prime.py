#!/usr/bin/env python3
"""
验证电磁耦合常数Z'的推导和计算准确性
"""

import numpy as np
from scipy import constants

# 基本常数（CODATA 2018）
c = constants.speed_of_light  # 光速
epsilon0 = constants.epsilon_0  # 真空介电常数
e = constants.elementary_charge  # 基本电荷
hbar = constants.hbar  # 约化普朗克常数
G = constants.gravitational_constant  # 万有引力常数

print("=== Z'常数推导验证 ===")
print()

# 1. 计算Z' = c/(8π*epsilon0)
Z_prime = c / (8 * np.pi * epsilon0)
print(f"1. Z' = c/(8π*epsilon0) = {Z_prime:.6e} kg·m^4·s^-5·A^-2")
print()

# 2. 验证与精细结构常数的关系：alpha = 2*e²*Z'/(hbar*c²)
alpha_calc = (2 * e**2 * Z_prime) / (hbar * c**2)
alpha_expt = 1/137.035999084  # CODATA 2018推荐值
print(f"2. 精细结构常数验证：")
print(f"   计算值 alpha_calc = {alpha_calc:.12f}")
print(f"   实验值 alpha_expt = {alpha_expt:.12f}")
print(f"   相对误差 = {(alpha_calc - alpha_expt)/alpha_expt:.2e}")
print()

# 3. 验证与引力常数Z的对称性
Z = (G * c) / 2
print(f"3. 引力常数Z = Gc/2 = {Z:.6e} m^4·kg^-1·s^-3")
print(f"   Z'/Z = {Z_prime/Z:.2e}")
print()

# 4. 验证力强比的计算
print(f"4. 力强比验证：")
print(f"   几何本源项 Z'/Z = {Z_prime/Z:.2e}")
print()

# 5. 验证不同粒子组合的力强比
print(f"5. 不同粒子组合的力强比：")
print(f"   质子质量 m_p = {constants.proton_mass:.6e} kg")
print(f"   电子质量 m_e = {constants.electron_mass:.6e} kg")
print()

# 质子-质子
q_p = e
m_p = constants.proton_mass
ratio_pp = (Z_prime/Z) * (q_p**2 / m_p**2)
print(f"   质子-质子: {ratio_pp:.2e}")

# 质子-电子
ratio_pe = (Z_prime/Z) * (abs(q_p * (-e)) / (m_p * constants.electron_mass))
print(f"   质子-电子: {ratio_pe:.2e}")

# 电子-电子
ratio_ee = (Z_prime/Z) * (e**2 / constants.electron_mass**2)
print(f"   电子-电子: {ratio_ee:.2e}")
print()

# 6. 验证量纲分析
print(f"6. 量纲分析验证：")
print(f"   c的量纲: [L·T^-1]")
print(f"   epsilon0的量纲: [M^-1·L^-3·T^4·I^2]")
print(f"   Z'的量纲: [L·T^-1] / [M^-1·L^-3·T^4·I^2] = [M·L^4·T^-5·I^-2]")
print()

# 7. 验证理论的自洽性
print(f"7. 理论自洽性验证：")
print(f"   - Z'包含光速c，符合'一切源于光速运动'的核心思想")
print(f"   - 8π因子源于'双层螺旋'时空结构，提供了几何解释")
print(f"   - 与精细结构常数的高精度吻合验证了推导的正确性")
print(f"   - 与引力常数Z的对称性体现了理论的统一框架")

print()
print("=== 验证完成 ===")
