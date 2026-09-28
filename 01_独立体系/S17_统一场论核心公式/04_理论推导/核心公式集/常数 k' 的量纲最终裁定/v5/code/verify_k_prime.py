import numpy as np

# CODATA 2018基本物理常数值
c = 299792458  # 光速 (m/s)
hbar = 1.0545718176461563e-34  # 约化普朗克常数 (J·s)
epsilon0 = 8.8541878128e-12  # 真空介电常数 (F/m)
ke = 1 / (4 * np.pi * epsilon0)  # 库仑常数 (N·m²/C²)
G = 6.67430e-11  # 牛顿引力常数 (m³·kg⁻¹·s⁻²)
e = 1.602176634e-19  # 基本电荷 (C)
m_e = 9.1093837015e-31  # 电子质量 (kg)
m_p = np.sqrt(hbar * c / G)  # 普朗克质量 (kg)

print("=== CODATA 2018基本物理常数值 ===")
print(f"光速 c = {c:.9e} m/s")
print(f"约化普朗克常数 ħ = {hbar:.9e} J·s")
print(f"真空介电常数 ε₀ = {epsilon0:.9e} F/m")
print(f"库仑常数 k_e = {ke:.9e} N·m²/C²")
print(f"牛顿引力常数 G = {G:.9e} m³·kg⁻¹·s⁻²")
print(f"基本电荷 e = {e:.9e} C")
print(f"电子质量 m_e = {m_e:.9e} kg")
print(f"普朗克质量 m_p = {m_p:.9e} kg")
print()

# 计算质量常数 k
k = 4 * np.pi * m_p
print("=== 质量常数 k 计算 ===")
print(f"k = 4πm_p = {k:.9e} kg")
print()

# 1. 尝试通过库仑常数 ke 反求 r_k 和 k'
print("=== 方法1: 通过库仑常数 ke 反求 ===")
print("公式: k_e = (c³/(2ħ²))·r_k")
print("反推: r_k = (2ħ²k_e)/c³")
r_k_method1 = (2 * hbar**2 * ke) / c**3
print(f"r_k = {r_k_method1:.9e}")

# 计算 k'
k_prime_method1 = r_k_method1 / k
print(f"k' = r_k/k = {k_prime_method1:.9e}")
print(f"量纲: [I T² M⁻¹] = A·s²/kg")
print()

# 2. 尝试通过 (eG)/c³ 计算 k'
print("=== 方法2: 通过 (eG)/c³ 计算 ===")
print("公式: k' = (eG)/c³")
k_prime_method2 = (e * G) / c**3
print(f"k' = (eG)/c³ = {k_prime_method2:.9e}")
print(f"量纲: [I T² M⁻¹] = A·s²/kg")
print()

# 3. 文档裁定值
print("=== 方法3: 文档裁定值 ===")
k_prime_official = 6.25e-27
print(f"文档裁定的 k' = {k_prime_official:.9e} C·s/kg")

# 计算 r_k (按量纲 [I T] 理解)
r_k_official = k * k_prime_official
print(f"r_k = k·k' = {r_k_official:.9e} C·s")
print()

# 4. 验证电荷定义方程的数值自洽性
print("=== 验证电荷定义方程的数值自洽性 ===")
print("公式: q = k'·k·(1/Ω²)·(dΩ/dt)")
print("示例: 取 Ω = 1 sr, dΩ/dt = 1 sr/s")
q_example = k_prime_official * k * (1/1**2) * 1
print(f"q = {q_example:.9e} C")
print()

# 5. 尝试导出库仑常数 ke
print("=== 尝试从 k' 导出库仑常数 ke ===")
print("尝试不同的公式组合:")

# 尝试1: ke = (c³/G)·(k'²/k)
try:
    ke_attempt1 = (c**3 / G) * (k_prime_official**2 / k)
    print(f"尝试1: ke = (c³/G)·(k'²/k) = {ke_attempt1:.9e}")
    print(f"与CODATA值的相对误差: {(ke_attempt1 - ke)/ke * 100:.2f}%")
except Exception as e:
    print(f"尝试1计算失败: {e}")

# 尝试2: ke = (c³/hbar²)·(k'²/k)
try:
    ke_attempt2 = (c**3 / hbar**2) * (k_prime_official**2 / k)
    print(f"尝试2: ke = (c³/ħ²)·(k'²/k) = {ke_attempt2:.9e}")
    print(f"与CODATA值的相对误差: {(ke_attempt2 - ke)/ke * 100:.2f}%")
except Exception as e:
    print(f"尝试2计算失败: {e}")

# 尝试3: ke = (c³/(2*hbar²))·(k·k')
try:
    ke_attempt3 = (c**3 / (2 * hbar**2)) * (k * k_prime_official)
    print(f"尝试3: ke = (c³/(2ħ²))·(k·k') = {ke_attempt3:.9e}")
    print(f"与CODATA值的相对误差: {(ke_attempt3 - ke)/ke * 100:.2f}%")
except Exception as e:
    print(f"尝试3计算失败: {e}")
print()

# 6. 量纲分析验证
print("=== 量纲分析验证 ===")
print("k' 的理论量纲: [I T² M⁻¹] = A·s²/kg")
print("验证方法1的量纲:")
print("r_k = (2ħ²ke)/c³ 的量纲:")
print("ħ²: [M² L⁴ T⁻²]")
print("ke: [M L³ T⁻⁴ I⁻²]")
print("c³: [L³ T⁻³]")
print("r_k: [M² L⁴ T⁻²]·[M L³ T⁻⁴ I⁻²]/[L³ T⁻³] = [M³ L⁴ T⁻³ I⁻²]")
print("k: [M]")
print("k' = r_k/k: [M³ L⁴ T⁻³ I⁻²]/[M] = [M² L⁴ T⁻³ I⁻²] (量纲不符)")
print()

print("验证方法2的量纲:")
print("k' = (eG)/c³ 的量纲:")
print("e: [I T]")
print("G: [L³ M⁻¹ T⁻²]")
print("c³: [L³ T⁻³]")
print("k': [I T]·[L³ M⁻¹ T⁻²]/[L³ T⁻³] = [I T² M⁻¹] (量纲相符)")
print()

# 7. 总结
print("=== 总结 ===")
print(f"方法1计算的 k': {k_prime_method1:.9e} (量纲不符)")
print(f"方法2计算的 k': {k_prime_method2:.9e} (量纲相符，数值过小)")
print(f"文档裁定的 k': {k_prime_official:.9e} (理论采用值)")
print()
print("结论:")
print("1. k' 的量纲 [I T² M⁻¹] 是明确且自洽的")
print("2. 从第一性原理直接推导出与裁定值一致的 k' 解析式存在困难")
print("3. 文档裁定的 k' ≈ 6.25×10⁻²⁷ C·s/kg 是理论内部的最终采用值")
print("4. 理论的最终验证需要依赖实验检验，如变化电磁场产生可测引力场的预言")
