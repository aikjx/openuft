# 力的比例关系计算验证
import numpy as np

# 基本常数
c = 299792458          # 光速，m/s
G = 6.67430e-11        # 万有引力常数，m³ kg⁻¹ s⁻²
epsilon0 = 8.854187817e-12  # 真空介电常数，F/m
k = 1/(4 * np.pi * epsilon0)  # 库仑常数

# 基本粒子质量和电荷
m_proton = 1.6726219e-27  # 质子质量，kg
m_electron = 9.1093837e-31  # 电子质量，kg
q_proton = 1.60217663e-19   # 质子电荷，C
q_electron = -1.60217663e-19  # 电子电荷，C

# 计算常数 f
f = (c / 2) * np.sqrt(4 * np.pi * epsilon0 * G)
print(f"常数 f = {f:.6f} kg/A")
print()

# 1. 质子-电子间力的计算（r=1e-10 m）
r = 1e-10  # 距离，m
print("1. 质子-电子间力的计算（r=1e-10 m）:")

# 电磁力
F_e_pe = k * abs(q_proton * q_electron) / r**2
print(f"电磁力: {F_e_pe:.6e} N")

# 引力
F_g_pe = G * m_proton * m_electron / r**2
print(f"引力: {F_g_pe:.6e} N")

# 强核力（简化模型）
# 假设强核力在距离r处的强度为 G * m_proton * m_electron / r**3 * r (短程修正)
F_n_pe = G * m_proton * m_electron / r**3 * r
print(f"强核力: {F_n_pe:.6e} N")

# 弱核力
F_w_pe = F_n_pe / 1e13
print(f"弱核力: {F_w_pe:.6e} N")

# 比例关系
print(f"电磁力/引力比值: {F_e_pe/F_g_pe:.6e}")
print(f"强核力/电磁力比值: {F_n_pe/F_e_pe:.6e}")
print(f"弱核力/强核力比值: {F_w_pe/F_n_pe:.6e}")
print()

# 2. 质子-质子间力的计算（r=1e-10 m）
print("2. 质子-质子间力的计算（r=1e-10 m）:")

# 电磁力
F_e_pp = k * q_proton**2 / r**2
print(f"电磁力: {F_e_pp:.6e} N")

# 引力
F_g_pp = G * m_proton**2 / r**2
print(f"引力: {F_g_pp:.6e} N")

# 强核力
F_n_pp = G * m_proton**2 / r**3 * r
print(f"强核力: {F_n_pp:.6e} N")

# 弱核力
F_w_pp = F_n_pp / 1e13
print(f"弱核力: {F_w_pp:.6e} N")

# 比例关系
print(f"电磁力/引力比值: {F_e_pp/F_g_pp:.6e}")
print(f"强核力/电磁力比值: {F_n_pp/F_e_pp:.6e}")
print(f"弱核力/强核力比值: {F_w_pp/F_n_pp:.6e}")
print()

# 3. 电子-电子间力的计算（r=1e-10 m）
print("3. 电子-电子间力的计算（r=1e-10 m）:")

# 电磁力
F_e_ee = k * q_electron**2 / r**2
print(f"电磁力: {F_e_ee:.6e} N")

# 引力
F_g_ee = G * m_electron**2 / r**2
print(f"引力: {F_g_ee:.6e} N")

# 强核力
F_n_ee = G * m_electron**2 / r**3 * r
print(f"强核力: {F_n_ee:.6e} N")

# 弱核力
F_w_ee = F_n_ee / 1e13
print(f"弱核力: {F_w_ee:.6e} N")

# 比例关系
print(f"电磁力/引力比值: {F_e_ee/F_g_ee:.6e}")
print(f"强核力/电磁力比值: {F_n_ee/F_e_ee:.6e}")
print(f"弱核力/强核力比值: {F_w_ee/F_n_ee:.6e}")
print()

# 4. 质子-中子间力的计算（r=1e-10 m）
print("4. 质子-中子间力的计算（r=1e-10 m）:")
m_neutron = 1.67492749804e-27  # 中子质量，kg

# 电磁力（中子不带电）
F_e_pn = 0.0
print(f"电磁力: {F_e_pn:.6e} N")

# 引力
F_g_pn = G * m_proton * m_neutron / r**2
print(f"引力: {F_g_pn:.6e} N")

# 强核力
F_n_pn = G * m_proton * m_neutron / r**3 * r
print(f"强核力: {F_n_pn:.6e} N")

# 弱核力
F_w_pn = F_n_pn / 1e13
print(f"弱核力: {F_w_pn:.6e} N")

# 比例关系
print(f"引力/强核力比值: {F_g_pn/F_n_pn:.6e}")
print(f"弱核力/强核力比值: {F_w_pn/F_n_pn:.6e}")
