# -*- coding: utf-8 -*-
"""
GAQ-UFT《全维统一——全域双向分形统一场论大全书》核心数值验证
============================================================
所有书中数字的可复算来源。精度：mpmath 60 位有效数字（用户历史偏好 250 位，
此处 60 位已远超物理常数实验精度，必要时可上调）。
数据基准：CODATA 2022 / PDG 2024 / Planck 2018 / SH0ES 2022。

运行：python verify_core.py
"""
import mpmath as mp

mp.mp.dps = 60

# ============ 1. CODATA 2022 基础常数（实验/定义值） ============
c  = mp.mpf("299792458")            # m/s   定义值（精确）
h  = mp.mpf("6.62607015e-34")       # J·s   定义值（精确）
e  = mp.mpf("1.602176634e-19")      # C     定义值（精确）
eps0 = mp.mpf("8.8541878128e-12")   # F/m   CODATA 2022
mu0  = mp.mpf("1.25663706212e-6")   # N/A²  CODATA 2022
G  = mp.mpf("6.67430e-11")          # m³/(kg·s²) CODATA 2022
kB = mp.mpf("1.380649e-23")         # J/K   定义值（精确）
me = mp.mpf("9.1093837139e-31")     # kg    电子质量 CODATA 2022
mp_kg = mp.mpf("1.67262192595e-27") # kg    质子质量
mn_kg = mp.mpf("1.67492750056e-27") # kg    中子质量
u_kg  = mp.mpf("1.66053906892e-27") # kg    原子质量单位
NA = mp.mpf("6.02214076e23")        # mol⁻¹ 定义值
alpha_inv_CODATA = mp.mpf("137.035999084")  # CODATA 2022 α⁻¹

hbar = h / (2*mp.pi)

# 轻子质量 (MeV/c²), PDG 2024
me_MeV  = mp.mpf("0.51099895069")
mmu_MeV = mp.mpf("105.6583755")
mtau_MeV= mp.mpf("1776.86")

# 哈勃常数
H0_Planck, sH0_Planck = mp.mpf("67.36"), mp.mpf("0.54")    # km/s/Mpc Planck 2018 官方组合（TT+lowE+lensing+BAO）
H0_SH0ES,  sH0_SH0ES  = mp.mpf("73.04"), mp.mpf("1.04")    # km/s/Mpc SH0ES 2022

print("="*78)
print(" [1] 基础关系：α 与 ε₀·ħ·c 的相容性")
print("="*78)
# 由 e,ħ,c,ε₀ 反算 α
alpha_calc = e**2 / (4*mp.pi*eps0*hbar*c)
alpha_inv_calc = 1/alpha_calc
print(f"  α(由e,ħ,c,ε₀算) = {mp.nstr(alpha_calc, 16)}")
print(f"  α⁻¹(算)         = {mp.nstr(alpha_inv_calc, 16)}")
print(f"  α⁻¹(CODATA2022) = {alpha_inv_CODATA}")
rel = abs(alpha_inv_calc - alpha_inv_CODATA)/alpha_inv_CODATA
print(f"  相对偏差         = {mp.nstr(rel, 4)}")
print(f"  结论：α=e²/(4πε₀ħc) 与 CODATA 相容（在 ε₀ 不确定度内）——这是定义性恒等式，不是新定律。")

print()
print("="*78)
print(" [2] Gε₀ 耦合恒等式：q_P²/m_P² = 4πε₀G")
print("="*78)
# 普朗克单位
mP = mp.sqrt(hbar*c/G)          # 普朗克质量
lP = mp.sqrt(hbar*G/c**3)       # 普朗克长度
tP = mp.sqrt(hbar*G/c**5)       # 普朗克时间
qP = mp.sqrt(4*mp.pi*eps0*hbar*c)  # 普朗克电荷
TP = mp.sqrt(hbar*c**5/(G*kB**2))  # 普朗克温度
print(f"  m_P = {mp.nstr(mP,10)} kg")
print(f"  ℓ_P = {mp.nstr(lP,10)} m")
print(f"  t_P = {mp.nstr(tP,10)} s")
print(f"  q_P = {mp.nstr(qP,10)} C")
print(f"  T_P = {mp.nstr(TP,10)} K")
# 恒等式验证
lhs = qP**2 / mP**2
rhs = 4*mp.pi*eps0*G
print(f"  q_P²/m_P²   = {mp.nstr(lhs, 12)} C²/kg²")
print(f"  4πε₀G       = {mp.nstr(rhs, 12)} C²/kg²")
print(f"  相对偏差     = {mp.nstr(abs(lhs-rhs)/rhs, 4)}  → 恒等式成立(定义性)")
print(f"  注：该恒等式由 Planck 单位定义直接推出，是'真'但'平凡'；")
print(f"      框架若赋予其动力学内容，则属假设，需实验检验。")

print()
print("="*78)
print(" [3] 无量纲耦合比：电磁力/引力 与 α_G")
print("="*78)
# 两电子间 库仑力/引力
F_ratio = (e**2/(4*mp.pi*eps0)) / (G*me**2)
print(f"  两电子静电力/引力 = {mp.nstr(F_ratio, 6)}  ≈ 4.17×10⁴²")
print(f"  1/(比值)          = {mp.nstr(1/F_ratio, 6)}  ≈ 2.40×10⁻⁴³")
# 引力精细结构常数 α_G = G m_e²/(ħc)
alphaG = G*me**2/(hbar*c)
print(f"  α_G = G m_e²/(ħc) = {mp.nstr(alphaG, 6)}")
print(f"  α/α_G             = {mp.nstr(alpha_calc/alphaG, 6)}")

print()
print("="*78)
print(" [4] 大数巧合（Eddington-Dirac 数值对应）")
print("="*78)
ratio_mP_me = mP/me
print(f"  m_P/m_e        = {mp.nstr(ratio_mP_me, 6)}")
print(f"  √(α_G⁻¹)       = {mp.nstr(mp.sqrt(1/alphaG), 6)}")
print(f"  二者之比       = {mp.nstr(ratio_mP_me/mp.sqrt(1/alphaG), 6)}")
print(f"  注：m_P/m_e = √(α_G⁻¹) 是定义恒等式（非巧合）：")
print(f"      m_P=√(ħc/G), α_G=Gm_e²/(ħc) ⇒ m_P/m_e=√(1/α_G)，代数上严格成立。")
# 宇宙年龄/普朗克时间
age_universe_yrs = mp.mpf("1.38e10")   # 年，Planck 2018 近似
age_sec = age_universe_yrs * mp.mpf("3.15576e7")
ratio_age = age_sec/tP
print(f"  宇宙年龄/t_P   = {mp.nstr(ratio_age, 6)}")
print(f"  注：这类 ~10⁶⁰/10⁴⁰ 的数值对应在物理上无公认解释，属'巧合'类别，本框架可提出几何解释但须实验验证。")

print()
print("="*78)
print(" [5] Koide 公式：Q=(m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)²")
print("="*78)
Q = (me_MeV+mmu_MeV+mtau_MeV)/(mp.sqrt(me_MeV)+mp.sqrt(mmu_MeV)+mp.sqrt(mtau_MeV))**2
print(f"  Q = {mp.nstr(Q, 12)}")
print(f"  2/3 = {mp.nstr(mp.mpf(2)/3, 12)}")
dev = abs(Q - mp.mpf(2)/3)/(mp.mpf(2)/3)
print(f"  相对偏差 = {mp.nstr(dev, 6)}  ≈ 9.2×10⁻⁶")
print(f"  结论：这是真实的高精度经验规律（非标准模型导出），本框架可作为'质量谱几何起源'的检验靶。")

print()
print("="*78)
print(" [6] 哈勃张力：Planck vs SH0ES")
print("="*78)
dH = H0_SH0ES - H0_Planck
sH = mp.sqrt(sH0_Planck**2 + sH0_SH0ES**2)
sigma = dH/sH
print(f"  ΔH0 = {mp.nstr(dH,6)} km/s/Mpc")
print(f"  合成不确定度 σ = {mp.nstr(sH,6)}")
print(f"  显著性 = {mp.nstr(sigma,4)}σ")
print(f"  结论：两个独立测量之差 ~5σ 级，是当前宇宙学的核心张力；任何统一框架都应能给出可检验的新机制。")

print()
print("="*78)
print(" [7] 电弱参数核对（PDG 2024）")
print("="*78)
mZ = mp.mpf("91.1876")   # GeV
mW = mp.mpf("80.3692")   # GeV
mH = mp.mpf("125.25")    # GeV
mt = mp.mpf("172.69")    # GeV
sin2thW = 1 - (mW/mZ)**2
print(f"  m_W = {mW} GeV, m_Z = {mZ} GeV, m_H = {mH} GeV, m_t = {mt} GeV")
print(f"  sin²θ_W = 1-(m_W/m_Z)² = {mp.nstr(sin2thW,8)}  (CODATA/PDG 有效值 ≈ 0.2312)")
# CKM 最大元
Vud, Vus, Vub = mp.mpf("0.97373"), mp.mpf("0.2243"), mp.mpf("0.00382")
Vcd, Vcs, Vcb = mp.mpf("0.221"),  mp.mpf("0.975"),  mp.mpf("0.0408")
Vtd, Vts, Vtb = mp.mpf("0.008"),  mp.mpf("0.0388"), mp.mpf("1.013")
print(f"  |Vud|²+|Vus|²+|Vub|² = {mp.nstr(Vud**2+Vus**2+Vub**2, 8)} （第一行归一应≈1）")

print()
print("="*78)
print(" [8] 框架可验证性快照：已证实 vs 假设 vs OPEN")
print("="*78)
print("  已证实（实验/定义）：α 定义式、Planck 单位、Koide 经验律、哈勃张力存在、")
print("                        CKM 幺正性、电弱参数（均有实测误差）")
print("  框架假设（待检验）：v≡c 全域约束、κ²+τ²=(ωℓ_P/c)²、32 维流形、Gε₀ 耦合的动力学内容、")
print("                        暗物质/暗能量几何起源、意识方程化")
print("  OPEN：质量谱从 Koide 到全族的第一性推导、PMNS/CKM 的拓扑推导、哈勃张力的调解机制、")
print("        变化电磁场产生引力场的实验证据")
print()
print("验证完成。所有数值均以 mpmath 高精度复算，见附录 C 与 code/verify_core.py。")
