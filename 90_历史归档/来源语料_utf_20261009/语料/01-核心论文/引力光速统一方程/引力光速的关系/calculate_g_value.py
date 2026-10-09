import math
from decimal import Decimal, getcontext

# 设置高精度计算上下文，指定精度位数
getcontext().prec = 100

# 使用高精度计算 π
pi_high = Decimal(math.pi)

# 计算 16 * π² 的高精度值
denominator_high = Decimal(16) * (pi_high ** Decimal(2))

# 计算 G = 1 / (16 * π²) 的高精度值
G_theory_high = Decimal(1) / denominator_high

# 引力常数的国家标准值（CODATA 2018推荐值）: 6.67430×10^-11 m³ kg^-1 s^-2
G_standard = 6.67430e-11

# 使用常规浮点数计算（用于对比）
pi = math.pi
denominator = 16 * (pi**2)
G_theory = 1 / denominator

# 打印高精度计算结果
print("===== 高精度计算结果 =====")
print(f"π 的高精度值: {pi_high}")
print(f"π² 的高精度值: {pi_high**2}")
print(f"16 * π² 的高精度值: {denominator_high}")
print(f"G = 1 / (16 * π²) 的高精度计算结果: {G_theory_high}")
print(f"G (理论计算值，保留20位小数) ≈ {G_theory_high:.20f}")
print()

# 打印引力常数的国家标准值及其比较
print("===== 与国家标准值比较 =====")
print(f"引力常数国家标准值 (CODATA 2018): {G_standard:.20f} m³ kg^-1 s^-2")
print(f"理论计算值 (G = 1/(16π²)): {float(G_theory_high):.20f}")
print()

# 计算相对差异
if G_standard != 0:
    relative_diff = abs(float(G_theory_high) - G_standard) / G_standard * 100
    print(f"理论值与标准值的相对差异: {relative_diff:.10f}%")
print()

# 显示更多小数位以便精细比较
print("===== 超精细数值比较 =====")
print(f"理论计算值 (60位小数): {G_theory_high:.60f}")
print(f"国家标准值 (60位小数): {Decimal(G_standard):.60f}")
print()

# 计算并显示绝对差异
absolute_diff = abs(float(G_theory_high) - G_standard)
print(f"绝对差异: {absolute_diff:.60f}")
print()

# 重要说明：关于理论计算值与国家标准值的差异解释
print("="*60)
print("重要说明")
print("="*60)
print("1. 这里计算的 G = 1/(16π²) 是一个理论公式的数值解，与物理学中实际测量的引力常数 G 是不同的概念。")
print("2. 物理学中的引力常数 G 是一个实验测量值，约为 6.67430×10^-11 m³ kg^-1 s^-2，而这里计算的理论值约为 0.00633。")
print("3. 这种巨大差异 (约95亿%) 表明这两个值在物理意义和量纲上都完全不同。")
print("4. 理论公式 G = 1/(16π²) 可能在特定的理论框架中有其应用，但与实际的引力常数G不可直接比较。")
print("5. 本计算仅作为数学公式的数值验证，不代表物理学中的实际引力常数。")
print("="*60)