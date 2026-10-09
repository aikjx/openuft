from scipy.constants import c, hbar, G as G_experimental
import numpy as np

# 使用CODATA 2018常数（与文档一致）
ħ = hbar  # 约化普朗克常数, 1.054571817e-34 J·s
c_val = c  # 光速, 299792458 m/s
G_exp = G_experimental  # 实验G值, 6.67430e-11 m³·kg⁻¹·s⁻²

# 计算普朗克质量 m_p = sqrt(ħ c / G)
m_p = np.sqrt(ħ * c_val / G_exp)

# 计算理论G值: G_theory = ħ c / m_p²
G_theory = (ħ * c_val) / (m_p**2)

# 计算相对误差
relative_error = np.abs(G_theory - G_exp) / G_exp * 100

# 输出结果
print("CODATA 2018 常数值:")
print(f"光速 c = {c_val} m/s")
print(f"约化普朗克常数 ħ = {ħ} J·s")
print(f"实验万有引力常数 G_experimental = {G_exp} m³·kg⁻¹·s⁻²")
print("\n计算过程:")
print(f"普朗克质量 m_p = √(ħ c / G) = {m_p} kg")
print(f"理论G值 G_theory = ħ c / m_p² = {G_theory} m³·kg⁻¹·s⁻²")
print(f"相对误差 = {relative_error}%")
