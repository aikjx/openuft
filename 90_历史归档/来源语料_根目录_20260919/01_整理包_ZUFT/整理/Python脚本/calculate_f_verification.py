import numpy as np

# CODATA 2018 推荐值 (使用SI单位)
G = 6.67430e-11       # m^3 kg^-1 s^-2
c = 299792458         # m/s
epsilon_0 = 8.8541878128e-12  # F/m

# 直接计算 4πε₀G
term = 4 * np.pi * epsilon_0 * G
print(f"4πε₀G = {term:.6e}")

# 计算平方根
sqrt_term = np.sqrt(term)
print(f"sqrt(4πε₀G) = {sqrt_term:.6e}")

# 计算 f = sqrt(4πε₀G) * c/2
f = sqrt_term * (c / 2)
print(f"f = {f:.6e}")
print(f"f = {f:.4f}")

# 验证论文中的数值
print(f"计算结果 f ≈ {f:.6e}")
print(f"计算结果 f ≈ {f:.4f}")
print("注意：论文中的值可能存在错误，计算结果基于CODATA 2018常数")
