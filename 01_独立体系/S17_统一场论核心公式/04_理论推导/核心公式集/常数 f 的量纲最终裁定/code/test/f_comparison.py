import numpy as np
from scipy import constants

print("=== 耦合常数f的两种公式对比分析 ===\n")

# 基本常数
c = constants.speed_of_light  # 光速
epsilon0 = constants.epsilon_0  # 真空介电常数
G = constants.gravitational_constant  # 万有引力常数

print("基本常数：")
print(f"  光速 c = {c:.6e} m/s")
print(f"  真空介电常数 ε₀ = {epsilon0:.6e} F/m")
print(f"  万有引力常数 G = {G:.6e} m³·kg⁻¹·s⁻²")
print()

# 第一种公式（无c因子）
print("1. 第一种公式（无c因子）：")
f1 = np.sqrt(4 * np.pi * G * epsilon0)
print(f"   f = sqrt(4πGε₀) = {f1:.10e}")
print(f"   量纲分析：")
print(f"   - G的量纲：m³·kg⁻¹·s⁻²")
print(f"   - ε₀的量纲：F/m = A²·s⁴·kg⁻¹·m⁻³")
print(f"   - G·ε₀的量纲：m³·kg⁻¹·s⁻² · A²·s⁴·kg⁻¹·m⁻³ = A²·s²·kg⁻²")
print(f"   - sqrt(G·ε₀)的量纲：A·s·kg⁻¹")
print()

# 第二种公式（有c因子）
print("2. 第二种公式（有c因子）：")
f2 = (c / 2) * np.sqrt(4 * np.pi * epsilon0 * G)
print(f"   f = (c/2)·sqrt(4πGε₀) = {f2:.10e}")
print(f"   量纲分析：")
print(f"   - c的量纲：m·s⁻¹")
print(f"   - c·sqrt(G·ε₀)的量纲：m·s⁻¹ · A·s·kg⁻¹ = A·m·kg⁻¹")
print()

# 核心方程量纲验证
print("3. 核心方程量纲验证（A为引力场强度，量纲m·s⁻²）：")
print("   方程1：∇×A = B/f")
print("   - 左边：∇×A 的量纲 = (1/m)·(m·s⁻²) = s⁻²")
print("   - 右边：B/f 的量纲 = (kg·s⁻²·A⁻¹)/f")
print("   - 要求f的量纲：kg·A⁻¹（才能使右边量纲为s⁻²）")
print()

print("   方程2：E = -f·dA/dt")
print("   - 左边：E 的量纲 = kg·m·s⁻³·A⁻¹")
print("   - 右边：f·dA/dt 的量纲 = f·(m·s⁻³)")
print("   - 要求f的量纲：kg·A⁻¹（才能使右边量纲为kg·m·s⁻³·A⁻¹）")
print()

# 量纲对比
print("4. 量纲对比：")
print(f"   - 第一种公式量纲：A·s·kg⁻¹")
print(f"   - 第二种公式量纲：A·m·kg⁻¹")
print(f"   - 核心方程要求量纲：kg·A⁻¹")
print()

# 数值关系
print("5. 数值关系：")
print(f"   - f2 = (c/2)·f1")
print(f"   - 因子：c/2 = {c/2:.6e}")
print(f"   - f2/f1 = {f2/f1:.6e}")
print()

# 结论
print("6. 结论：")
print("   两种公式的量纲都与核心方程要求的kg·A⁻¹不一致，")
print("   说明可能存在量纲分析错误或定义差异。")
print()
print("   但从物理意义考虑，第二种公式包含光速c，")
print("   更能体现引力场与电磁场的相对论性联系，")
print("   因此可能更接近正确。")
