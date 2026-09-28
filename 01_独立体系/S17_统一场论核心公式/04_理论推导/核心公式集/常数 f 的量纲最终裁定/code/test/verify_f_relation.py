#!/usr/bin/env python3
"""
验证张祥前统一场论中的关系式：
1/(4πε₀G) = Z'/Z = (c/(2f))²

其中：
- Z = Gc/2 (引力耦合常数)
- Z' = c/(8πε₀) (电磁耦合常数)
- f = c/2 · √(4πε₀G) (耦合常数)
"""

import math

# 基本物理常数
c = 299792458  # 光速，单位：m/s
ε0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11  # 万有引力常数，单位：m³/(kg·s²)

print("=== 验证张祥前统一场论关系式 ===")
print(f"使用的物理常数：")
print(f"光速 c = {c} m/s")
print(f"真空介电常数 ε0 = {ε0} F/m")
print(f"万有引力常数 G = {G} m³/(kg·s²)")
print()

# 详细计算过程
print("=== 详细计算过程 ===")

# 1. 计算 4πε₀G
four_pi_epsilon0_G = 4 * math.pi * ε0 * G
print(f"1. 4πε₀G = {four_pi_epsilon0_G:.6e}")

# 2. 计算左边：1/(4πε₀G)
left_side = 1 / four_pi_epsilon0_G
print(f"2. 左边：1/(4πε₀G) = {left_side:.6e}")
print()

# 3. 计算 Z = Gc/2
Z = G * c / 2
print(f"3. 引力耦合常数 Z = Gc/2 = {Z:.6e} m⁴/(kg·s³)")

# 4. 计算 Z' = c/(8πε₀)
Z_prime = c / (8 * math.pi * ε0)
print(f"4. 电磁耦合常数 Z' = c/(8πε₀) = {Z_prime:.6e} kg·m⁴/(s⁵·A²)")

# 5. 计算中间：Z'/Z
middle_side = Z_prime / Z
print(f"5. 中间：Z'/Z = {middle_side:.6e}")
print()

# 6. 计算 √(4πε₀G)
sqrt_four_pi_epsilon0_G = math.sqrt(four_pi_epsilon0_G)
print(f"6. √(4πε₀G) = {sqrt_four_pi_epsilon0_G:.6e}")

# 7. 计算 f = c/2 · √(4πε₀G)
f = (c / 2) * sqrt_four_pi_epsilon0_G
print(f"7. 耦合常数 f = c/2 · √(4πε₀G) = {f:.6e} kg/A")

# 8. 计算 c/(2f)
c_over_2f = c / (2 * f)
print(f"8. c/(2f) = {c_over_2f:.6e}")

# 9. 计算右边：(c/(2f))²
right_side = c_over_2f ** 2
print(f"9. 右边：(c/(2f))² = {right_side:.6e}")
print()

# 验证是否相等
print("=== 验证结果 ===")
print(f"左边与中间的相对误差：{(abs(left_side - middle_side) / left_side):.10e}")
print(f"左边与右边的相对误差：{(abs(left_side - right_side) / left_side):.10e}")
print(f"中间与右边的相对误差：{(abs(middle_side - right_side) / middle_side):.10e}")
print()

if math.isclose(left_side, middle_side, rel_tol=1e-10) and math.isclose(left_side, right_side, rel_tol=1e-10):
    print("✅ 验证成功！三个表达式相等。")
    print("关系式 1/(4πε₀G) = Z'/Z = (c/(2f))² 成立。")
else:
    print("❌ 验证失败！三个表达式不相等。")

# 额外验证：从 f 反推其他值
print()
print("=== 额外验证 ===")
print(f"从 f 计算 4πε₀G：4πε₀G = (2f/c)² = {(2*f/c)**2:.6e}")
print(f"与直接计算的 4πε₀G 相对误差：{(abs((2*f/c)**2 - four_pi_epsilon0_G) / four_pi_epsilon0_G):.10e}")
