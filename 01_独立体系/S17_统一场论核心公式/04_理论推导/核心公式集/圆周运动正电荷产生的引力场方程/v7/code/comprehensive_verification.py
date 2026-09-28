import math

# 物理常数（CODATA 2018推荐值）
c = 299792458  # 光速，m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，F/m
e = 1.602176634e-19  # 电子电荷，C
hbar = 1.054571817e-34  # 约化普朗克常数，J·s

print('=' * 60)
print('=== 全面验证计算结果 ===')
print('=' * 60)

# 1. 计算几何常数 Z'
print('\n1. 计算几何常数 Z\':')
print('-' * 40)
Z_prime = c / (8 * math.pi * epsilon0)
print(f'公式: Z\' = c/(8πε₀)')
print(f'计算值: {Z_prime}')
print(f'科学计数法: {Z_prime:.6e} m')
print(f'文件中值: 1.347200e+18 m')
print(f'是否一致: {abs(Z_prime - 1.347200e+18) < 1e12}')

# 2. 计算精细结构常数
print('\n2. 计算精细结构常数 α:')
print('-' * 40)

# 标准公式计算
alpha_standard = (e**2) / (4 * math.pi * epsilon0 * hbar * c)
print(f'标准公式: α = e²/(4πε₀ħc)')
print(f'标准计算值: {alpha_standard:.10f}')
print(f'科学计数法: {alpha_standard:.6e}')

# 使用Z'公式计算
alpha_using_Z = (2 * e**2 * Z_prime) / (hbar * c**2)
print(f'\n使用Z\'公式: α = 2e²Z\'/(ħc²)')
print(f'计算值: {alpha_using_Z:.10f}')
print(f'科学计数法: {alpha_using_Z:.6e}')
print(f'文件中值: 7.29735e-3')
print(f'是否一致: {abs(alpha_using_Z - 7.29735e-3) < 1e-8}')

# 3. 验证公式等价性
print('\n3. 验证公式等价性:')
print('-' * 40)
print('标准公式: α = e²/(4πε₀ħc)')
print('Z\'公式: α = 2e²Z\'/(ħc²)')
print('代入 Z\' = c/(8πε₀):')
print('α = 2e²*(c/(8πε₀))/(ħc²) = 2e²c/(8πε₀ħc²) = e²/(4πε₀ħc)')
print('结论: 两个公式完全等价 ✓')

# 4. 与CODATA推荐值比较
print('\n4. 与CODATA推荐值比较:')
print('-' * 40)
codata_alpha = 7.2973525693e-3
print(f'CODATA 2018推荐值: {codata_alpha:.10f}')
print(f'计算值与CODATA偏差: {abs(alpha_using_Z - codata_alpha):.12f}')
print(f'相对误差: {abs((alpha_using_Z - codata_alpha)/codata_alpha):.12f}')
print(f'误差是否可接受 (<1e-6): {abs((alpha_using_Z - codata_alpha)/codata_alpha) < 1e-6}')

# 5. 详细数值计算过程
print('\n5. 详细数值计算过程:')
print('-' * 40)
print(f'分子: 2 × ({e})² × ({Z_prime:.6e})')
print(f'= 2 × ({e**2:.6e}) × ({Z_prime:.6e})')
print(f'= 2 × {e**2:.6e} × {Z_prime:.6e}')
print(f'= {2 * e**2 * Z_prime:.6e}')
print()
print(f'分母: {hbar} × ({c})²')
print(f'= {hbar:.6e} × {c**2:.6e}')
print(f'= {hbar * c**2:.6e}')
print()
print(f'α = 分子/分母 = {2 * e**2 * Z_prime:.6e} / {hbar * c**2:.6e}')
print(f'= {alpha_using_Z:.6e}')

print('\n' + '=' * 60)
print('=== 验证完成 ===')
print('=' * 60)
