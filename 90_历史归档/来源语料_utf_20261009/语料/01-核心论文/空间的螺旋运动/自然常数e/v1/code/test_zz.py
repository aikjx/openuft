# 按理论定义重新计算Z、Z'（对比代码中的值）
import sympy as sp
from decimal import Decimal, getcontext
getcontext().prec = 20

# 基础常数（与代码一致）
c = Decimal('299792458')
G = Decimal('6.67430e-11')
eps0 = Decimal('8.8541878128e-12')
pi = Decimal('3.14159265358979323846')

# 理论定义的Z、Z'
Z_theory = (G * c) / 2  # Z = Gc/2
Z_prime_theory = c / (8 * pi * eps0)  # Z' = c/(8πε₀)

# 代码中使用的Z、Z'
Z_code = Decimal('1.35e27')
Z_prime_code = Decimal('3.34e-16')

print(f"理论定义 Z = Gc/2 = {Z_theory} (≈ {Z_theory:.2e})")
print(f"代码中 Z = {Z_code} (偏差：{abs(Z_code - Z_theory)/Z_theory*100:.2f}%)")
print(f"理论定义 Z' = c/(8πε₀) = {Z_prime_theory} (≈ {Z_prime_theory:.2e})")
print(f"代码中 Z' = {Z_prime_code} (偏差：{abs(Z_prime_code - Z_prime_theory)/Z_prime_theory*100:.2f}%)")

# 验证文档中的公式 G = k1 * c² / Z
# 从 Z = Gc/2 解出 G
G_from_Z = (2 * Z_theory) / c
print(f"\n从 Z = Gc/2 解出 G: {G_from_Z} (与输入 G 的偏差：{abs(G_from_Z - G)/G*100:.2f}%)")

# 验证文档中的公式形式
k1 = (G * Z_theory) / (c ** 2)
print(f"比例系数 k1 = {k1}")
