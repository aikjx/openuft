import math

# 物理常数
c = 299792458  # 光速，m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，F/m
e = 1.602176634e-19  # 电子电荷，C
hbar = 1.054571817e-34  # 约化普朗克常数，J·s

# 计算几何常数 Z'
Z_prime = c / (8 * math.pi * epsilon0)
print('=== 计算结果 ===')
print(f'Z\' = {Z_prime} m')
print(f'Z\' (科学计数法): {Z_prime:.6e} m')

# 标准精细结构常数公式
alpha_standard = (e**2) / (4 * math.pi * epsilon0 * hbar * c)
print(f'\n标准公式计算 alpha: {alpha_standard}')
print(f'alpha (科学计数法): {alpha_standard:.6e}')

# 使用Z'计算 alpha（正确公式）
alpha_using_Z = (2 * e**2 * Z_prime) / (hbar * c**2)
print(f'\n使用Z\'公式计算 alpha: {alpha_using_Z}')
print(f'alpha (科学计数法): {alpha_using_Z:.6e}')

# CODATA推荐值
print(f'\nCODATA推荐值: ~7.2973525693e-3')

# 验证公式是否正确
print(f'\n=== 公式验证 ===')
print('标准公式: alpha = e²/(4πε₀ħc)')
print('使用Z\'公式: alpha = 2e²Z\'/(ħc²)')
print('因为 Z\' = c/(8πε₀)，所以:')
print('2e²Z\'/(ħc²) = 2e²*(c/(8πε₀))/(ħc²) = e²/(4πε₀ħc)')
print('与标准公式完全一致，验证通过！')
