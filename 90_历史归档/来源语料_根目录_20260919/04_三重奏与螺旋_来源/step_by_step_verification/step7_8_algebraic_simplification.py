"""
================================================================================
STEP 7-8: 验证代数化简和最终公式
================================================================================
"""

import numpy as np
from scipy.constants import c, e, epsilon_0, hbar, mu_0, G

print("=" * 90)
print("STEP 7-8: 代数化简和最终公式验证")
print("=" * 90)

alpha = e**2 / (4 * np.pi * epsilon_0 * hbar * c)

print("\n【7.1】代入质量-电荷关系")
print("-" * 90)
print("公式(6): 4πm/t = c²q")
print("\n将公式(6)代入公式(9): 4πGm/t = α²q/ε₀")
print("\n变换过程:")
print("  左边: G × (4πm/t) = G × c²q")
print("  右边: α²q/ε₀")
print("\n得到: Gc²q = α²q/ε₀")

print("\n约去 q (q ≠ 0):")
print("  Gc² = α²/ε₀")
print("这是公式(10)")

print("\n【7.2】代数验证")
print("-" * 90)

G_calc_intermediate = alpha**2 / (epsilon_0 * c**2)
print(f"从公式(10)解出 G:")
print(f"  G = α² / (ε₀c²)")
print(f"  G = {alpha**2:.10f} / ({epsilon_0:.10e} × {c:.10e}²)")
print(f"  G = {G_calc_intermediate:.20e}")

print("\n【7.3】引入经典电磁关系")
print("-" * 90)
print("公式(11): μ₀ = 1/(ε₀c²)")
print("\n这是麦克斯韦方程的直接推论，是标准物理的正确结论！")
print("验证:")

mu_0_standard = mu_0
mu_0_calculated = 1 / (epsilon_0 * c**2)

print(f"  μ₀(标准值) = {mu_0_standard:.20e}")
print(f"  1/(ε₀c²)    = {mu_0_calculated:.20e}")
print(f"  相对误差     = {abs(mu_0_standard - mu_0_calculated) / mu_0_standard * 100:.20e}%")

print("\n✓ 结论: μ₀ = 1/(ε₀c²) 是精确成立的（单位制定义）")

print("\n【7.4】最终代换")
print("-" * 90)
print("将公式(11)代入公式(10): Gc² = α²/ε₀")
print("\n  Gc² = α² × μ₀c²")
print("  Gc² = α²μ₀c²")
print("\n两边同时除以 c² (c ≠ 0):")
print("  G = α²μ₀")
print("这是最终公式(12)！")

print("\n【7.5】最终公式验证")
print("-" * 90)

G_final = alpha**2 * mu_0
G_experimental = G

print(f"理论预测 G = α²μ₀:")
print(f"  α² = {alpha**2:.18f}")
print(f"  μ₀ = {mu_0:.10e}")
print(f"  G = {G_final:.20e}")

print(f"\n实验测量 G (CODATA):")
print(f"  G = {G_experimental:.20e}")

error = abs(G_final - G_experimental) / G_experimental
print(f"\n相对误差: {error * 100:.10f}%")
print(f"绝对误差: {abs(G_final - G_experimental):.20e}")

print("\n【7.6】数值一致性分析")
print("-" * 90)

print("\n关键发现:")
print(f"  α²μ₀ = {G_final:.15e}")
print(f"  G_exp = {G_experimental:.15e}")
print(f"  比值  = {G_final/G_experimental:.15f}")

print(f"\n⚠️  注意: 比值 ≈ 1.0026164")
print(f"⚠️  这意味着理论值比实验值大约 0.26%")
print(f"⚠️  这个差异不是随机误差，而是系统性偏差！")

print("\n【7.7】差异来源分析")
print("-" * 90)
print("0.26% 的差异必然来自推导链条中的某个假设！")

print("\n可能来源1: 公式(6) 4πm/t = c²q")
print("  - 如果改为 4πm/t = k·c²q")
print("  - 其中 k ≠ 1")
print("  - 那么最终结果会变成 G = k·α²μ₀")

k_needed = G_experimental / (alpha**2 * mu_0)
print(f"\n所需修正因子 k = G_exp / (α²μ₀) = {k_needed:.10f}")

print("\n可能来源2: 公式(8) α²q/ε₀")
print("  - 如果标准形式应该是其他表达式")
print("  - 而不是 α²q/ε₀")

print("\n可能来源3: 公式(9) 4πGm/t = α²q/ε₀")
print("  - 这个等式本身就是人为构造的")
print("  - 缺乏物理基础")

print("\n【7.8】等价形式验证")
print("-" * 90)

G_form2 = alpha**2 / (epsilon_0 * c**2)
diff_form = abs(G_final - G_form2)

print(f"G = α²μ₀            = {G_final:.20e}")
print(f"G = α²/(ε₀c²)      = {G_form2:.20e}")
print(f"差值                 = {diff_form:.30e}")

print("\n✓ 结论: 两种数学形式完全等价")

print("\n【7.9】Z'/Z 恒等式验证")
print("-" * 90)

Z_ratio_1 = 4 * np.pi * G * epsilon_0
m_P = np.sqrt(hbar * c / G)
q_P = np.sqrt(4 * np.pi * epsilon_0 * hbar * c)
Z_ratio_2 = q_P**2 / m_P**2
Z_ratio_3 = 4 * np.pi * alpha**2 / c**2

print(f"4πGε₀             = {Z_ratio_1:.20e}")
print(f"q_P²/m_P²         = {Z_ratio_2:.20e}")
print(f"4πα²/c²           = {Z_ratio_3:.20e}")

print(f"\n相对误差:")
print(f"  |4πGε₀ - q_P²/m_P²|/|4πGε₀| = {abs(Z_ratio_1-Z_ratio_2)/Z_ratio_1:.20e}")
print(f"  |4πGε₀ - 4πα²/c²|/|4πGε₀| = {abs(Z_ratio_1-Z_ratio_3)/Z_ratio_1:.20e}")

print("\n✓ 结论: 4πGε₀ = q_P²/m_P² 精确成立")
print("⚠️  4πGε₀ ≠ 4πα²/c²，差异为 0.26%")

print("\n" + "=" * 90)
print("STEP 7-8 验证结果:")
print("✓ 公式(10): 代数推导正确")
print("✓ 公式(11): 标准物理恒等式，100% 正确")
print("✓ 公式(12): 代数化简正确")
print("⚠️  核心结果 G = α²μ₀: 数学上正确，但与实验有 0.26% 差异")
print("=" * 90)
