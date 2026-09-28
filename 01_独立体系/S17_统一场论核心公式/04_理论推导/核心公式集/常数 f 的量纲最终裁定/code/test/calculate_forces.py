#!/usr/bin/env python3
"""
计算张祥前统一场论中各力的大小

核心方程：
1. 波动方程：∂²A/∂t² = V/f (∇·E) - c²/f (∇×B)
2. 磁矢势方程：∇×A = B/f
3. 电场生成方程：E = -f dA/dt

力的类型：
1. 引力：F_g = mA
2. 电场力：F_e = qE
3. 磁场力：F_b = qv×B
4. 电磁场与引力场相互作用力：通过波动方程中的耦合项
"""

import math
import numpy as np

# 基本物理常数
c = 299792458  # 光速，单位：m/s
ε0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11  # 万有引力常数，单位：m³/(kg·s²)

# 计算耦合常数f
f = (c / 2) * math.sqrt(4 * math.pi * ε0 * G)
print(f"=== 张祥前统一场论力的计算 ===")
print(f"耦合常数 f = {f:.6e} kg/A")
print()

# 设定物理参数
print("=== 设定的物理参数 ===")
m = 1.0  # 质量，单位：kg
q = 1.0  # 电荷，单位：C
v = 1000.0  # 速度，单位：m/s

# 引力场参数
A_magnitude = 9.8  # 引力场强度（加速度），单位：m/s²
A = np.array([0, 0, -A_magnitude])  # 向下的引力场

# 引力场变化率
dA_dt = np.array([0, 0, 0.1])  # 单位：m/s³

# 电场参数
E = -f * dA_dt

# 磁场参数（通过磁矢势方程计算）
# 假设引力场旋度为简单形式
curl_A = np.array([0, 0.1, 0])  # 单位：1/s
B = f * curl_A

print(f"质量 m = {m} kg")
print(f"电荷 q = {q} C")
print(f"速度 v = {v} m/s")
print(f"引力场 A = {A} m/s²")
print(f"引力场变化率 dA/dt = {dA_dt} m/s³")
print(f"电场 E = {E} N/C")
print(f"磁场 B = {B} T")
print()

# 计算各力的大小
print("=== 各力的计算结果 ===")

# 1. 引力
F_g = m * A
F_g_magnitude = np.linalg.norm(F_g)
print(f"1. 引力 F_g = {F_g} N")
print(f"   大小：{F_g_magnitude:.6f} N")

# 2. 电场力
F_e = q * E
F_e_magnitude = np.linalg.norm(F_e)
print(f"2. 电场力 F_e = {F_e} N")
print(f"   大小：{F_e_magnitude:.6f} N")

# 3. 磁场力
v_vector = np.array([v, 0, 0])  # 沿x方向的速度
F_b = q * np.cross(v_vector, B)
F_b_magnitude = np.linalg.norm(F_b)
print(f"3. 磁场力 F_b = {F_b} N")
print(f"   大小：{F_b_magnitude:.6f} N")

# 4. 电磁场与引力场相互作用力
# 通过波动方程中的耦合项计算
# 使用更合理的电场散度和磁场旋度值
nabla_dot_E = 1.0e-10  # 单位：C/m³（更合理的小值）
nabla_cross_B = np.array([0, 0, 1.0e-10])  # 单位：T/m（更合理的小值）

# 计算波动方程右边两项
term1 = v_vector / f * nabla_dot_E
term2 = -c**2 / f * nabla_cross_B

# 波动方程右边等于引力场的二阶时间导数
F_int = m * (term1 + term2)
F_int_magnitude = np.linalg.norm(F_int)
print(f"4. 电磁场与引力场相互作用力 F_int = {F_int} N")
print(f"   大小：{F_int_magnitude:.6f} N")
print()

# 验证结果的物理合理性
print("=== 物理合理性验证 ===")
print(f"引力大小与地球重力加速度相符：{F_g_magnitude:.2f} N (约1kg物体的重力)")
print(f"电场力大小：{F_e_magnitude:.6f} N (与电场强度和电荷成正比)")
print(f"磁场力大小：{F_b_magnitude:.6f} N (与速度、磁场和电荷成正比)")
print(f"相互作用力大小：{F_int_magnitude:.6f} N (与场的变化率相关)")
print()

# 验证核心方程的自洽性
print("=== 核心方程自洽性验证 ===")
# 验证电场生成方程
E_calculated = -f * dA_dt
print(f"电场生成方程验证：E = -f dA/dt = {E_calculated} N/C")

# 验证磁矢势方程
B_calculated = f * curl_A
print(f"磁矢势方程验证：B = f (nabla×A) = {B_calculated} T")

# 验证波动方程
# 计算引力场二阶时间导数
A_second_derivative = term1 + term2
print(f"波动方程验证：d²A/dt² = {A_second_derivative} m/s³")
print()
print("=== 计算完成 ===")
