# 经典物理实验数据计算脚本
# 用于计算张祥前统一场论中的常数Z、Z'和f

import math

# CODATA 2018 推荐值 (SI单位)
G = 6.67430e-11       # 万有引力常数，m³kg⁻¹s⁻²
c = 299792458         # 光速，m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，F/m

# 计算引力几何常数 Z
Z = G * c / 2

# 计算电磁几何常数 Z'
Z_prime = c / (8 * math.pi * epsilon0)

# 计算耦合常数 f
f = math.sqrt(Z / Z_prime) * (c / 2)

# 输出结果
print("=== 经典物理实验数据计算结果 ===")
print(f"引力几何常数 Z = {Z:.6e}")
print(f"电磁几何常数 Z' = {Z_prime:.6e}")
print(f"耦合常数 f = {f:.6e} (无量纲) 或 {f:.6f}")
print("==================================")

# 额外验证：计算Z/Z'的平方根部分
root_ratio = math.sqrt(Z / Z_prime)
print(f"\n额外验证:")
print(f"Z/Z' 的平方根 = {root_ratio:.6e}")
print(f"乘以 c/2 后 = {root_ratio * (c/2):.6e}")
