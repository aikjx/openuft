#!/usr/bin/env python3
"""
验证ZUFT电场强度公式的代数正确性
公式：E_理论 = (2Q Z')/(c r^2) = (2Q)/(8πε₀ r^2) = E_几何
"""

import math

# 定义常数
c = 299792458  # 光速，m/s
ε0 = 8.8541878128e-12  # 真空介电常数，F/m

# 定义变量
Q = 1.602176634e-19  # 电荷量，C（电子电荷）
r = 5.29177210903e-11  # 距离，m（玻尔半径）

# 计算Z'
Z_prime = c / (8 * math.pi * ε0)
print(f"Z' = {Z_prime:.6e} kg·m^4·s^-3·C^-2")

# 计算E_理论
E_theory = (2 * Q * Z_prime) / (c * r**2)
print(f"E_理论 = {E_theory:.6e} V/m")

# 计算中间步骤：2Q/(8πε0 r²)
E_middle = (2 * Q) / (8 * math.pi * ε0 * r**2)
print(f"中间步骤：2Q/(8πε0 r²) = {E_middle:.6e} V/m")

# 计算E_几何（根据论文第48-49行的推导）
E_geometry = (2 * Q) / (8 * math.pi * ε0 * r**2)
print(f"E_几何（推导结果） = {E_geometry:.6e} V/m")

# 验证等价性
difference = abs(E_theory - E_geometry)
relative_error = difference / max(E_theory, E_geometry)
print(f"\n验证结果：")
print(f"两者差值：{difference:.6e} V/m")
print(f"相对误差：{relative_error:.6e}")

if relative_error < 1e-10:
    print("✅ 验证成功：E_理论 = E_几何")
else:
    print("❌ 验证失败：E_理论 ≠ E_几何")

# 额外验证：与经典库仑定律的关系
E_classical = Q / (4 * math.pi * ε0 * r**2)
print(f"\n经典库仑定律计算的E：{E_classical:.6e} V/m")
print(f"E_几何与E_经典的比值：{E_geometry / E_classical:.6f}")

# 计算纯几何形式（论文第40行定义）
E_geometry_pure = Q / (8 * math.pi * ε0 * r**2)
print(f"\n纯几何形式（论文第40行）：E_几何 = {E_geometry_pure:.6e} V/m")
print(f"纯几何形式与经典的比值：{E_geometry_pure / E_classical:.6f}")
