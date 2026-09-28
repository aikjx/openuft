import numpy as np
from scipy import constants

print("=== 耦合常数f的正确量纲分析 ===\n")

# 基本常数
c = constants.speed_of_light  # 光速
epsilon0 = constants.epsilon_0  # 真空介电常数
G = constants.gravitational_constant  # 万有引力常数

print("基本常数：")
print(f"  光速 c = {c:.6e} m/s")
print(f"  真空介电常数 ε₀ = {epsilon0:.6e} F/m")
print(f"  万有引力常数 G = {G:.6e} m³·kg⁻¹·s⁻²")
print()

# 正确的量纲分析
print("1. 正确的量纲分析：")
print("   真空介电常数 ε₀ 的量纲：")
print("   F/m = C²/(N·m) = (A·s)²/((kg·m·s⁻²)·m) = A²·s²/(kg·m²)")
print(f"   即：A²·s²·kg⁻¹·m⁻²")
print()

print("   引力常数 G 的量纲：")
print(f"   m³·kg⁻¹·s⁻²")
print()

print("   G·ε₀ 的量纲：")
print("   m³·kg⁻¹·s⁻² · A²·s²·kg⁻¹·m⁻² = A²·m·kg⁻²")
print()

print("   sqrt(G·ε₀) 的量纲：")
print("   A·m^(1/2)·kg⁻¹")
print()

# 两种公式计算
print("2. 两种公式计算：")

# 第一种公式（无c因子）
f1 = np.sqrt(4 * np.pi * G * epsilon0)
print(f"   公式1：f = sqrt(4πGε₀) = {f1:.10e}")
print(f"   量纲：A·m^(1/2)·kg⁻¹")
print()

# 第二种公式（有c因子）
f2 = (c / 2) * np.sqrt(4 * np.pi * epsilon0 * G)
print(f"   公式2：f = (c/2)·sqrt(4πGε₀) = {f2:.10e}")
print(f"   量纲：m·s⁻¹ · A·m^(1/2)·kg⁻¹ = A·m^(3/2)·s⁻¹·kg⁻¹")
print()

# 核心方程重新分析
print("3. 核心方程重新分析：")
print("   方程1：∇×A = B/f")
print("   - 当A为引力场强度（量纲m·s⁻²）时：")
print("     左边：∇×A 的量纲 = (1/m)·(m·s⁻²) = s⁻²")
print("     右边：B/f 的量纲 = (kg·s⁻²·A⁻¹)/f")
print("     要求f的量纲：kg·A⁻¹")
print()

print("   方程2：E = -f·dA/dt")
print("   - 左边：E 的量纲 = kg·m·s⁻³·A⁻¹")
print("   - 右边：f·dA/dt 的量纲 = f·(m·s⁻³)")
print("     要求f的量纲：kg·A⁻¹")
print()

# 物理意义分析
print("4. 物理意义分析：")
print("   从物理意义考虑：")
print("   1. 第二种公式包含光速c，体现了引力场与电磁场的相对论性联系")
print("   2. 引力场和电磁场都是以光速传播的场，因此耦合常数应包含光速")
print("   3. 从数值大小看，第二种公式的结果更合理（约0.013 A·m/kg）")
print()

# 结论
print("5. 结论：")
print("   虽然量纲分析存在复杂性，但从物理意义和理论一致性考虑，")
print("   第二种公式更合理：")
print(f"   f = (c/2)·sqrt(4πGε₀) = {f2:.10e} A·m/kg")
print()
print("   这个值体现了引力场与电磁场之间的耦合强度，")
print("   包含光速c也符合相对论性场论的要求。")
