#!/usr/bin/env python3
"""
精确的一步步数值计算，确保每一步都有明确的数值代入，没有任何跳跃
公式：f = √(Z/Z') · (c/2)
其中：
  Z = Gc/2 （引力光速统一耦合常数）
  Z' = c/(8πε₀) （电磁光速几何耦合常数）
"""

import math

print("="*85)
print("张祥前统一场论常数f的精确一步步数值计算")
print("="*85)
print()

# 1. 定义物理常数（精确数值）
print("1. 物理常数定义（精确数值）：")
print("-" * 50)
c = 299792458.0          # 光速，单位：m/s（精确值）
eps0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
G = 6.67430e-11          # 万有引力常数，单位：m³/(kg·s²)
pi = math.pi             # 圆周率
print(f"   光速 c = {c} m/s")
print(f"   真空介电常数 ε₀ = {eps0} F/m")
print(f"   万有引力常数 G = {G} m³/(kg·s²)")
print(f"   圆周率 π = {pi}")
print()

# 2. 计算引力光速统一耦合常数 Z = Gc/2
print("2. 计算引力光速统一耦合常数 Z = Gc/2：")
print("-" * 50)
print(f"   步骤1：计算 G * c = {G} * {c}")
G_times_c = G * c
print(f"   结果：G * c = {G_times_c}")
print(f"   步骤2：计算 Z = (G * c) / 2 = {G_times_c} / 2")
Z = G_times_c / 2
print(f"   结果：Z = {Z} m⁴/(kg·s³)")
print()

# 3. 计算电磁光速几何耦合常数 Z' = c/(8πε₀)
print("3. 计算电磁光速几何耦合常数 Z' = c/(8πε₀)：")
print("-" * 50)
print(f"   步骤1：计算 8 * π = 8 * {pi}")
_8pi = 8 * pi
print(f"   结果：8π = {_8pi}")
print(f"   步骤2：计算 8π * ε₀ = {_8pi} * {eps0}")
_8pi_eps0 = _8pi * eps0
print(f"   结果：8πε₀ = {_8pi_eps0}")
print(f"   步骤3：计算 Z' = c / (8πε₀) = {c} / {_8pi_eps0}")
Z_prime = c / _8pi_eps0
print(f"   结果：Z' = {Z_prime} kg·m⁴/(C²·s³)")
print()

# 4. 计算 Z/Z' 的比值
print("4. 计算 Z/Z' 的比值：")
print("-" * 50)
print(f"   Z/Z' = {Z} / {Z_prime}")
Z_ratio = Z / Z_prime
print(f"   结果：Z/Z' = {Z_ratio}")
print()

# 5. 计算 √(Z/Z')
print("5. 计算 √(Z/Z')：")
print("-" * 50)
print(f"   √(Z/Z') = √({Z_ratio})")
sqrt_Z_ratio = math.sqrt(Z_ratio)
print(f"   结果：√(Z/Z') = {sqrt_Z_ratio}")
print()

# 6. 计算 c/2
print("6. 计算 c/2：")
print("-" * 50)
print(f"   c/2 = {c} / 2")
c_half = c / 2
print(f"   结果：c/2 = {c_half} m/s")
print()

# 7. 最终计算 f = √(Z/Z') · (c/2)
print("7. 最终计算 f = √(Z/Z') · (c/2)：")
print("-" * 50)
print(f"   f = {sqrt_Z_ratio} * {c_half}")
f = sqrt_Z_ratio * c_half
print(f"   结果：f = {f} C·m/(kg·s)")
print()

# 8. 转换为常用单位
print("8. 单位转换（1A = 1C/s，所以 1C·m/(kg·s) = 1A·m/kg）：")
print("-" * 50)
print(f"   f = {f} A·m/kg")
print()

# 9. 结果总结
print("9. 结果总结：")
print("-" * 50)
print(f"   物理常数：")
print(f"   - 光速 c = {c} m/s")
print(f"   - 真空介电常数 ε₀ = {eps0} F/m")
print(f"   - 万有引力常数 G = {G} m³/(kg·s²)")
print()
print(f"   中间计算：")
print(f"   - Z = {Z} m⁴/(kg·s³)")
print(f"   - Z' = {Z_prime} kg·m⁴/(C²·s³)")
print(f"   - Z/Z' = {Z_ratio}")
print(f"   - √(Z/Z') = {sqrt_Z_ratio}")
print(f"   - c/2 = {c_half} m/s")
print()
print(f"   最终结果：")
print(f"   - f = {f} A·m/kg")
print(f"   - f ≈ {f:.6f} A·m/kg")
print()
print("="*85)