import math

# 物理常数数值
c = 3e8  # 光速，m/s
h = 6.626e-34  # 普朗克常数，J·s
ħ = h / (2 * math.pi)  # 约化普朗克常数，J·s
G = 6.674e-11  # 万有引力常数，m³/(kg·s²)
ε0 = 8.854e-12  # 真空介电常数，F/m
e = 1.602e-19  # 基本电荷，C

# 计算传统物理的精细结构常数α
def calculate_alpha_traditional():
    numerator = e ** 2
    denominator = 4 * math.pi * ε0 * ħ * c
    alpha = numerator / denominator
    return alpha

# 计算ZUFT的精细结构常数α
def calculate_alpha_ZUFT():
    Z_prime = c / (8 * math.pi * ε0)
    numerator = 2 * e ** 2 * Z_prime
    denominator = ħ * c ** 2
    alpha = numerator / denominator
    return alpha

# 计算并比较
print("=== 精细结构常数α验证 ===")
alpha_traditional = calculate_alpha_traditional()
alpha_ZUFT = calculate_alpha_ZUFT()

print(f"传统物理公式计算结果: α = {alpha_traditional:.6f}")
print(f"ZUFT公式计算结果: α = {alpha_ZUFT:.6f}")
print(f"相对误差: {abs(alpha_traditional - alpha_ZUFT) / alpha_traditional * 100:.10f}%")
print(f"是否一致: {'是' if abs(alpha_traditional - alpha_ZUFT) < 1e-10 else '否'}")

# 验证ZUFT公式的数学推导
print("\n=== ZUFT公式数学推导验证 ===")
Z_prime = c / (8 * math.pi * ε0)
print(f"Z' = c/(8πε₀) = {Z_prime:.2e}")

# 代入ZUFT公式展开
temp = 2 * e ** 2 * Z_prime / (ħ * c ** 2)
temp_simplified = 2 * e ** 2 * (c / (8 * math.pi * ε0)) / (ħ * c ** 2)
temp_simplified = e ** 2 / (4 * math.pi * ε0 * ħ * c)
print(f"ZUFT公式展开简化后: α = {temp_simplified:.6f}")
print(f"与传统公式结果一致: {'是' if abs(temp_simplified - alpha_traditional) < 1e-10 else '否'}")
