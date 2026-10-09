import numpy as np
from scipy.constants import epsilon_0, mu_0, c

print("=== 验证 c = 1/√(μ₀ε₀) 公式 ===\n")

# 获取国际推荐的标准常数
epsilon_0_value = epsilon_0  # 真空介电常数 (F/m)
mu_0_value = mu_0            # 真空磁导率 (N/A² 或 H/m)
c_defined = c                # 光速的定义值 (m/s)

print(f"国际推荐值：")
print(f"ε₀ = {epsilon_0_value:.12e} F/m")
print(f"μ₀ = {mu_0_value:.12e} H/m")
print(f"c  = {c_defined:.0f} m/s (定义值)")
print()

# 通过公式计算光速
c_calculated = 1 / np.sqrt(mu_0_value * epsilon_0_value)

print(f"通过公式计算：")
print(f"1/√(μ₀ε₀) = {c_calculated:.8f} m/s")
print()

# 计算相对误差
relative_error = abs(c_calculated - c_defined) / c_defined * 100

print(f"验证结果：")
print(f"定义的光速值：{c_defined:.0f} m/s")
print(f"计算的光速值：{c_calculated:.8f} m/s")
print(f"相对误差：{relative_error:.15e} %")
print()

# 更精确的验证（使用更高精度）
print("=== 高精度验证 ===")

# 使用CODATA 2018推荐值进行更精确计算
# 这些值来自最新的物理常数表
epsilon_0_precise = 8.8541878128e-12  # 精确值
mu_0_precise = 1.25663706212e-6      # 精确值

c_precise_calculated = 1 / np.sqrt(mu_0_precise * epsilon_0_precise)

print(f"使用CODATA 2018精确值：")
print(f"ε₀ = {epsilon_0_precise:.12e} F/m")
print(f"μ₀ = {mu_0_precise:.12e} H/m")
print(f"计算的光速：{c_precise_calculated:.12f} m/s")
print(f"定义的光速：{c_defined:.0f} m/s")

precision_error = abs(c_precise_calculated - c_defined) / c_defined * 100
print(f"精度误差：{precision_error:.20e} %")
print()

# 验证公式的数学恒等性
print("=== 数学恒等性验证 ===")
product = mu_0_value * epsilon_0_value
inverse_square = 1 / (c_defined ** 2)

print(f"μ₀ε₀ = {product:.12e}")
print(f"1/c² = {inverse_square:.12e}")
print(f"比值：{product / inverse_square:.16f}")

# 结论
print("\n" + "="*50)
if relative_error < 1e-10:
    print("✅ 验证通过！公式 c = 1/√(μ₀ε₀) 完全正确！")
    print("这是麦克斯韦电磁理论的基石，证明了光是一种电磁波。")
else:
    print("❌ 验证失败！")
    
print("="*50)
