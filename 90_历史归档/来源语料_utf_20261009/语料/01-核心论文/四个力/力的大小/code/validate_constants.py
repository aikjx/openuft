# 几何常数计算
import numpy as np

c = 299792458          # 光速，m/s
G = 6.67430e-11        # 万有引力常数，m³ kg⁻¹ s⁻²
epsilon0 = 8.854187817e-12  # 真空介电常数，F/m

# 计算引力几何常数 Z
Z = (G * c) / 2
print(f"引力几何常数 Z = {Z:.6e} m^4 kg^-1 s^-3")

# 计算电磁几何常数 Z'
Z_prime = c / (8 * np.pi * epsilon0)
print(f"电磁几何常数 Z' = {Z_prime:.6e} kg m^4 s^-3 A^-2")

# 计算 Z'/Z 比值
ratio = Z_prime / Z
print(f"Z'/Z 比值 = {ratio:.6e}")

# 计算常数 f
f = (c / 2) * np.sqrt(4 * np.pi * epsilon0 * G)
print(f"常数 f = {f:.6f} kg/A")
print(f"f的精确值（科学计数法）：{f:.10e} kg/A")
