import math
from scipy import constants  # 导入CODATA 2018标准物理常数

# ===================== 步骤1：定义核心物理常数（CODATA 2018） =====================
# 基础常数（带单位说明，确保量纲一致）
c = constants.speed_of_light          # 真空中光速，m/s (≈299792458)
G = constants.gravitational_constant  # 万有引力常数，m³/(kg·s²) (≈6.67430×10^-11)
eps0 = constants.epsilon_0            # 真空介电常数，F/m (≈8.8541878128×10^-12)
h_bar = constants.hbar                # 约化普朗克常数，J·s (≈1.054571817×10^-34)
e = constants.elementary_charge       # 电子电荷，C (≈1.602176634×10^-19)
# 使用已知的精细结构常数值
alpha_exp = 1/137.035999084  # 精细结构常数实验值（≈1/137.035999084）

print("=== 核心物理常数（CODATA 2018）===")
print(f"光速 c = {c:.9e} m/s")
print(f"万有引力常数 G = {G:.9e} m³/(kg·s²)")
print(f"真空介电常数 ε₀ = {eps0:.9e} F/m")
print(f"约化普朗克常数 ħ = {h_bar:.9e} J·s")
print(f"电子电荷 e = {e:.9e} C")
print(f"精细结构常数实验值 α_exp = {alpha_exp:.12f} (1/α≈{1/alpha_exp:.6f})")
print("-" * 80)

# ===================== 步骤2：计算几何常数 Z = Gc/2 =====================
Z = (G * c) / 2
print("=== 步骤2：计算引力几何常数 Z = Gc/2 ===")
print(f"Z = ({G:.9e} × {c:.9e}) / 2 = {Z:.9e} m⁴/(kg·s³)")
print(f"理论预言Z≈0.01，计算值Z≈{Z:.6f}，吻合度：{(Z/0.01-1)*100:.4f}%")
print("-" * 80)

# ===================== 步骤3：计算电磁几何常数 Z' = c/(8πε₀) =====================
Z_prime = c / (8 * math.pi * eps0)
print("=== 步骤3：计算电磁几何常数 Z' = c/(8πε₀) ===")
print(f"Z' = {c:.9e} / (8×π×{eps0:.9e}) = {Z_prime:.9e} kg·m⁴/(s³·C²)")
print("-" * 80)

# ===================== 步骤4：验证精细结构常数 α = 2e²Z'/(ħc²) =====================
# 计算理论值
alpha_calc = (2 * e**2 * Z_prime) / (h_bar * c**2)
# 计算相对误差
relative_error = abs((alpha_calc - alpha_exp) / alpha_exp) * 100

print("=== 步骤4：验证精细结构常数 α = 2e²Z'/(ħc²) ===")
print(f"理论计算值 α_calc = {alpha_calc:.12f} (1/α≈{1/alpha_calc:.6f})")
print(f"实验参考值 α_exp = {alpha_exp:.12f} (1/α≈{1/alpha_exp:.6f})")
print(f"相对误差 = {relative_error:.8f}% (论文标注≈0.00065%)")
print("-" * 80)

# ===================== 步骤5：验证普朗克质量 m_p = c/(4πZ) =====================
m_p = c / (4 * math.pi * Z)
# 使用已知的普朗克质量标准值
m_p_std = 2.176434e-08  # 普朗克质量标准值，单位kg
print("=== 步骤5：验证普朗克质量 m_p = c/(4πZ) ===")
print(f"理论计算值 m_p = {m_p:.9e} kg")
print(f"CODATA标准值 m_p_std = {m_p_std:.9e} kg")
print(f"相对偏差 = {abs((m_p - m_p_std)/m_p_std)*100:.4f}%")
print("-" * 80)

# ===================== 步骤6：还原牛顿引力定律和库仑定律 =====================
print("=== 步骤6：验证经典定律还原 ===")
# 引力定律：F = Gm₁m₂/r² = (2Z/c)m₁m₂/r²
print("牛顿引力定律还原：F = Gm₁m₂/r² = (2Z/c)m₁m₂/r²")
print(f"  验证 2Z/c = {2*Z/c:.9e} m³/(kg·s²)，与G={G:.9e} 完全一致")

# 库仑定律：F = (1/(4πε₀))q₁q₂/r² = (2Z'/c)q₁q₂/r²
coulomb_const = 1/(4*math.pi*eps0)  # 库仑常数
print("库仑定律还原：F = (1/(4πε₀))q₁q₂/r² = (2Z'/c)q₁q₂/r²")
print(f"  库仑常数 1/(4πε₀) = {coulomb_const:.9e} kg·m³/(s⁴·A²)")
print(f"  验证 2Z'/c = {2*Z_prime/c:.9e} kg·m³/(s⁴·A²)，完全一致")