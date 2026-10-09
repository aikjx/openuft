# 按理论定义重新计算，使用E和E'避免与现有ZZ'混淆
import sympy as sp
from decimal import Decimal, getcontext
getcontext().prec = 20

# 基础常数
c = Decimal('299792458')
G = Decimal('6.67430e-11')
eps0 = Decimal('8.8541878128e-12')
pi = Decimal('3.14159265358979323846')

# 理论定义（使用E和E'替代Z和Z'）
E_theory = (G * c) / 2  # E = Gc/2
E_prime_theory = c / (8 * pi * eps0)  # E' = c/(8πε₀)

# 代码中原始使用的值（对比用）
original_Z = Decimal('1.35e27')
original_Z_prime = Decimal('3.34e-16')

print(f"理论定义 E = Gc/2 = {E_theory} (≈ {E_theory:.2e})")
print(f"原始代码中 Z = {original_Z} (与E的偏差：{abs(original_Z - E_theory)/E_theory*100:.2f}%)")
print(f"理论定义 E' = c/(8πε₀) = {E_prime_theory} (≈ {E_prime_theory:.2e})")
print(f"原始代码中 Z' = {original_Z_prime} (与E'的偏差：{abs(original_Z_prime - E_prime_theory)/E_prime_theory*100:.2f}%)")
