# 公式验证脚本：验证 f² = c²πZ/Z' 是否正确

import numpy as np

# 基本物理常数
c = 299792458          # 光速，m/s
G = 6.67430e-11        # 万有引力常数，m³ kg⁻¹ s⁻²
epsilon0 = 8.854187817e-12  # 真空介电常数，F/m

# 计算几何常数
Z = (G * c) / 2         # 引力几何常数
Z_prime = c / (8 * np.pi * epsilon0)  # 电磁几何常数

# 计算力的耦合系数 f
f = (c / 2) * np.sqrt(4 * np.pi * epsilon0 * G)

# 计算 f²
f_squared = f ** 2

# 计算 c²Z/(4Z') (修复后的公式)
formula_result = (c ** 2 * Z) / (4 * Z_prime)

# 计算原错误公式 c²πZ/(4Z') 用于对比
old_formula_result = (c ** 2 * np.pi * Z) / (4 * Z_prime)

# 计算之前的错误公式 c²πZ/Z' 用于对比
previous_error_result = (c ** 2 * np.pi * Z) / Z_prime

# 打印结果
print("=== 公式验证结果 ===")
print(f"光速 c = {c:.6e} m/s")
print(f"万有引力常数 G = {G:.6e} m³ kg⁻¹ s⁻²")
print(f"真空介电常数 epsilon0 = {epsilon0:.6e} F/m")
print()
print(f"引力几何常数 Z = {Z:.6e} m^4 kg^-1 s^-3")
print(f"电磁几何常数 Z' = {Z_prime:.6e} kg m^4 s^-3 A^-2")
print(f"Z/Z' = {Z/Z_prime:.6e}")
print(f"4πepsilon0G = {4 * np.pi * epsilon0 * G:.6e}")
print()
print(f"力的耦合系数 f = {f:.6f} kg/A")
print(f"f² = {f_squared:.6e} kg²/A²")
print()
print(f"=== 公式验证 ===")
print(f"正确公式: c²Z/(4Z') = {formula_result:.6e} kg²/A²")
print(f"原错误公式: c²πZ/(4Z') = {old_formula_result:.6e} kg²/A²")
print(f"之前的错误公式: c²πZ/Z' = {previous_error_result:.6e} kg²/A²")
print()
print(f"=== 对比结果 ===")
print(f"f² 与 正确公式的差值: {abs(f_squared - formula_result):.6e}")
print(f"f² 与 原错误公式的差值: {abs(f_squared - old_formula_result):.6e}")
print(f"f² 与 之前错误公式的差值: {abs(f_squared - previous_error_result):.6e}")
print()

# 验证 Z/Z' = 4πepsilon0G
ratio_verification = abs((Z / Z_prime) - (4 * np.pi * epsilon0 * G))
print(f"=== Z/Z' 验证 ===")
print(f"Z/Z' = {Z/Z_prime:.6e}")
print(f"4πepsilon0G = {4 * np.pi * epsilon0 * G:.6e}")
print(f"两者差值: {ratio_verification:.6e}")
print()

# 结论
if abs(f_squared - formula_result) < 1e-10:
    print("✅ 验证通过：f² = c²πZ/Z' 公式正确！")
else:
    print("❌ 验证失败：公式存在错误！")

if abs(f_squared - old_formula_result) > 1e-10:
    print("✅ 确认原公式 c²πZ/(4Z') 错误")
else:
    print("❌ 原公式验证异常")
