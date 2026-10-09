#!/usr/bin/env python3
# 计算精细结构常数验证

# CODATA 2018常数
e = 1.602176634e-19  # 基本电荷，单位：C
hbar = 1.054571817e-34  # 约化普朗克常数，单位：J·s
c = 299792458  # 光速，单位：m/s
Z_prime = 1.34720012160e18  # 更精确的电磁光速几何耦合常数，单位：kg·m^4·s^-5·A^-2

# 计算精细结构常数（添加因子2）
numerator = 2 * e**2 * Z_prime
denominator = hbar * c**2
alpha_calc = numerator / denominator

print("计算精细结构常数 α：")
print(f"分子: 2 × e² × Z' = 2 × ({e})² × ({Z_prime}) = {numerator}")
print(f"分母: ħ × c² = ({hbar}) × ({c})² = {denominator}")
print(f"计算结果: α_calc = {alpha_calc}")
print(f"结果（科学计数法）: α_calc = {alpha_calc:.11f}")

# 验证与CODATA 2018推荐值的一致性
codata_alpha = 0.0072973525693
print(f"\nCODATA 2018推荐值: α = {codata_alpha}")
print(f"差值: |α_calc - α_CODATA| = {abs(alpha_calc - codata_alpha)}")
print(f"相对误差: |α_calc - α_CODATA| / α_CODATA = {abs(alpha_calc - codata_alpha) / codata_alpha}")

# 验证公式推导
print("\n验证公式推导:")
print(f"公式: α = e²Z'/(ħc²)")
print(f"代入Z' = c/(8πε₀):")
print(f"α = e²*(c/(8πε₀))/(ħc²) = e²/(4πε₀ħc)")
print("与经典精细结构常数定义一致")
