import pint
from math import pi

# 创建单位注册器
ureg = pint.UnitRegistry()

# 定义常数及其单位
c = 299792458 * ureg.meter / ureg.second  # 光速，单位 m/s
epsilon0 = 8.8541878128e-12 * ureg.farad / ureg.meter  # 真空介电常数，单位 F/m

# 计算 Z'
Z_prime = c / (8 * pi * epsilon0)

print(f"Z' 的数值: {Z_prime.magnitude:.6e}")
print(f"Z' 的单位: {Z_prime.units}")

# 将单位转换为基本 SI 单位（千克、米、秒、安培）
Z_prime_base = Z_prime.to_base_units()
print(f"Z' 的基本 SI 单位: {Z_prime_base.units}")

# 验证量纲是否与 m^2/(s·F) 一致
expected_unit = ureg.meter**2 / (ureg.second * ureg.farad)
print(f"预期单位: {expected_unit}")

# 检查 Z' 的单位是否与预期单位等价
if Z_prime.dimensionality == expected_unit.dimensionality:
    print("量纲验证通过：Z' 的单位与 m^2/(s·F) 等价。")
else:
    print("量纲验证失败。")

# 输出量纲信息
print(f"\nZ' 的量纲: {Z_prime.dimensionality}")