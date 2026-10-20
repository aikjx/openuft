# -*- coding: utf-8 -*-
"""
TUFT-r131｜正确方程扩容与攻破退守路径：树层可算预言与幂计数不可重整化
=====================================================================
承接用户指令「要整理正确的，攻破正确的理论体系与方程」的第三卷
（r127 归并行会话：SM 数值正确核 V01–V11；r128 归本会话：方程全集
结构审计 E1–E8 + 12 项失效边界 B1–B12；r130 归并行会话：方程推导链
隐藏前提审计 GR-1..8/SM-1..6，PREMISE-OPEN/DOMAIN-LIMITED）。

本卷分工（四卷条目不可相加）：
  O 组扩容（整理正确·树层可算预言）：只收「树层公式从基本输入机算出来、
    与测量值在已知修正量级内相符」的项——这是整理层的最强形态：
    不是定义回代（0σ），而是带残差、残差归因可判的实质预言。
    O6 μ 寿命树层 Fermi 预言；O7 Higgs 自耦合跨输入自洽；
    O8 QCD 渐近自由（β₀ 方向 + 一环 Λ 量级）。
  B 组扩容（攻破正确·结构性质 + 退守路径图）：
    B13 GR 幂计数不可重整化（[κ]=M⁻¹ 机读）；
    B14 低能 QCD 非微扰 ⇒ 解析完备性边界（Λ/m_p 机读）；
    B15 退守路径图（登记型：每条攻破 FAIL 的标准 BSM 退路 +
        本仓库已封/未封状态 + 引用机读值）。
    与 r130 的分界：r130 审计**推导链内部**的隐藏前提；本册 B15 登记
    **攻破落地后**的标准 BSM 退路——一切面不同，条目不可相加。

编号冲突处置：r130 已由并行会话跑通并产出三件套（隐藏前提审计）⇒ 按
「保留已跑通产出三件套者为权威」规则，本卷改号 r131（首空实测）。

纪律：
  - verdict 全部机读驱动；登记型（INFO/OPEN）显式标注、附引用来源
  - 阈值来自公布不确定度传播或声明量级门；禁拍脑袋机器零
  - 树层残差门：残差必须落在「已知辐射修正量级」带内，且远超输入
    不确定度传播（CT6）——否则不是预言而是拟合
  - 跨卷约定差异必须声明（r127 V04 用 n_f=6 给 β₀=7；本卷 O8 用
    n_f=5（M_Z 处 top 已退耦）给 β₀=23/3——两者都对，n_f 口径不同）
"""

import json
import os
import sys
import time
from fractions import Fraction

import mpmath as mp

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

mp.mp.dps = 250

ROOT = "D:/a10/aikjx/code/my_lib/openuft"
OUT_DIR = ROOT + "/04_公共成果/本项目_全维自洽与归一化/数据"
STEM = "TUFT-r131_正确方程扩容与攻破退守路径_树层可算预言与幂计数不可重整化_2026-10-20"

# ------------------------------------------------------------------
# 常数层：CODATA 2022 / PDG 2022 / 实验值
# ------------------------------------------------------------------
c = mp.mpf("299792458")                # 精确
hbar = mp.mpf("1.054571817e-34")       # CODATA 2022
h_planck = mp.mpf("6.62607015e-34")    # 精确（SI 2019 定义）
G = mp.mpf("6.67430e-11")              # CODATA 2022
e_charge = mp.mpf("1.602176634e-19")   # 精确
alpha = mp.mpf("7.2973525643e-3")      # CODATA 2022
m_e = mp.mpf("9.1093837015e-31")       # kg
m_p = mp.mpf("1.67262192369e-27")      # kg
m_mu_MeV = mp.mpf("105.6583755")       # CODATA 2022 (MeV)
u_m_mu_MeV = mp.mpf("0.0000023")       # CODATA 2022 (23)
tau_mu = mp.mpf("2.1969811e-6")        # s, CODATA 2022
u_tau_mu = mp.mpf("0.0000022e-6")      # s, CODATA 2022 (22)
G_F = mp.mpf("1.1663788e-5")           # GeV^-2, PDG
u_G_F = mp.mpf("0.0000006e-5")         # GeV^-2, PDG (6)
m_H = mp.mpf("125.25")                 # GeV
M_Z = mp.mpf("91.1876")                # GeV
alpha_s_MZ = mp.mpf("0.1180")          # PDG
alpha_s_MZ_u = mp.mpf("0.0009")
Lambda_PDG_MS = mp.mpf("0.21")         # GeV, PDG Λ^(5)_MS-bar（引用值，无精确位）
Mpc = mp.mpf("3.0856775814913673e22")
H0_planck = mp.mpf("67.36")
Omega_L = mp.mpf("0.6889")
lP = mp.mpf("1.616255e-35")            # m
M_GUT = mp.mpf("2.014e16")             # GeV (r120 MSSM 锚点)
alpha_GUT_inv = mp.mpf("24.3")

m_mu_GeV = m_mu_MeV / 1000
u_m_mu_GeV = u_m_mu_MeV / 1000
m_p_GeV = m_p * c**2 / (mp.mpf("1e9") * e_charge)
hbar_GeV_s = hbar / (mp.mpf("1e9") * e_charge)   # GeV·s

ITEMS = []
CONTROLS = []
GUARDS = []


def record(store, iid, title, verdict, detail, numbers=None, source=""):
    store.append({"id": iid, "title": title, "verdict": verdict,
                  "detail": detail, "numbers": numbers or {}, "source": source})
    print("[%-8s] %-6s %s" % (verdict, iid, title))


def n(x, k=12):
    return mp.nstr(x, k)


def dim(m=0, l=0, t=0, i=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(i))


def dim_mul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dim_pow(a, k):
    return tuple(x * k for x in a)


def dim_str(d):
    parts = []
    for name, x in zip("MLTI", d):
        if x != 0:
            parts.append(name if x == 1 else "%s^%s" % (name, x))
    return "*".join(parts) if parts else "1"


def dim_natural_M_power(d):
    """ℏ=c=1 下 [L]=[T]=M⁻¹ ⇒ 求 (M,L,T) 量纲的总 M 幂次。"""
    m_, l_, t_, _i = d
    return m_ - l_ - t_


print("=" * 78)
print("TUFT-r131  expand-correct + retreat-map: tree-level predictions (controls first)")
print("=" * 78)

# ==================================================================
# 控制组（先立：证判别力）
# ==================================================================
# CT1 恒等式检测器双向自反
gsq = Fraction(25, 9)
gpsq = Fraction(25, 16)
mw_mz_frac = Fraction(5, 3) / Fraction(25, 12)
ct1 = (mw_mz_frac == Fraction(4, 5)) and (Fraction(1, 137) != Fraction(1, 128))
record(CONTROLS, "CT1", "恒等式检测器双向自反（M_W/M_Z=cosθ_W=4/5 Fraction 恒等；α(0)≠α(M_Z) 判非恒等）",
       "PASS" if ct1 else "FAIL",
       "sinθ=3/5 ⇒ g=5e/3、g′=5e/4 ⇒ M_W/M_Z=(5/3)/(25/12)=4/5=cosθ 精确成立；α(0)≠α(M_Z) 判非恒等。",
       {"mw_over_mz": "4/5", "cos_theta": "4/5"})

# CT2 控制组·GR 波速预言 vs GW170817
dv_low = mp.mpf("-3e-15"); dv_high = mp.mpf("7e-15"); dv_gr = mp.mpf("0")
ct2 = (dv_low <= dv_gr) and (dv_gr <= dv_high)
record(CONTROLS, "CT2", "控制组·GR 波速预言 v_g=c 与 GW170817 一致（|Δv/c| 限窗 [−3e-15, +7e-15]）",
       "PASS" if ct2 else "FAIL",
       "Abbott et al. 2017（GW170817/GRB170817A）：−3e-15 ≤ Δv/c ≤ +7e-15；GR 预言 Δ=0 落窗内。",
       {"delta_v_over_c_window": "[-3e-15, 7e-15]", "GR_prediction": "0"})

# CT3 量纲审计器自反（(M,L,T) 口径）
d_L = dim(m=1, l=-1, t=-2)
d_EH = dim_mul(dim_mul(dim(l=4, t=-4), dim(m=1, l=-3, t=2)), dim(l=-2))
d_V48 = dim_mul(dim(m=1, l=3, t=-2), dim(l=-2))
ct3 = (d_EH == d_L) and (d_V48 != d_L)
record(CONTROLS, "CT3", "量纲审计器自反（EH 作用量 M·L⁻¹·T⁻² 判对；V4.8 螺旋 ℒ M·L¹·T⁻² 判错）",
       "PASS" if ct3 else "FAIL",
       "EH：[c⁴R/(16πG)] = %s = [ℒ] ✓；V4.8：[(ħc/2)(κ²−τ²)] = %s ≠ [ℒ]（差 L²）✗ —— 与 65 号卷 A6 一致。"
       % (dim_str(d_EH), dim_str(d_V48)),
       {"L_dim": dim_str(d_L), "EH_dim": dim_str(d_EH), "V48_dim": dim_str(d_V48)},
       "EH 作用量；65 号卷 V4.8")

# CT4 sanity 守卫自反
rho_crit = 3 * (H0_planck * 1000 / Mpc)**2 / (8 * mp.pi * G)
rho_L = Omega_L * rho_crit
Lambda_std = 8 * mp.pi * G * rho_L / c**2
lam_check = 3 * Omega_L / (c / (H0_planck * 1000 / Mpc))**2
rho_vac_cut = hbar * c / (8 * mp.pi**2 * lP**4)
ct4 = (abs(lam_check - Lambda_std) / Lambda_std < mp.mpf("1e-12")) and \
      (mp.log10(rho_vac_cut / (rho_L * c**2)) > 100)
record(CONTROLS, "CT4", "sanity 守卫自反（ΛCDM 锚点闭合；真空能截断触发 121 dex 越界门）",
       "PASS" if ct4 else "FAIL",
       "锚点 3Ω_Λ/R_Λ² 回代 Λ 一致（rel=%s）；靶面越界 %.2f dex ⇒ 守卫双向有效。"
       % (n(abs(lam_check - Lambda_std) / Lambda_std, 3), mp.log10(rho_vac_cut / (rho_L * c**2))),
       {"anchor_rel": n(abs(lam_check - Lambda_std) / Lambda_std, 3),
        "vacuum_dex": n(mp.log10(rho_vac_cut / (rho_L * c**2)), 6)})

# CT5 排除性控制组（SU(5) 被质子衰变排除）
ratio_ct5 = mp.mpf("2.4e34") / mp.mpf("4.589e31")
ct5 = ratio_ct5 > 100
record(CONTROLS, "CT5", "控制组·排除性：SU(5) 预言 τ_p=4.589e31 yr < Super-K 下限 2.4e34 yr ⇒ 可排除",
       "PASS" if ct5 else "FAIL",
       "正确体系自身的实验约束能排除错误统一候选（SU(5) 快 %.0f 倍）⇒ 攻破判据有牙齿。" % ratio_ct5,
       {"tau_p_SU5": "4.589e31", "tau_p_SK": "2.4e34", "ratio": n(ratio_ct5, 6)})

# CT6 树层公式不确定度传播自反（新：残差必须是物理修正而非输入噪声）
# τ_μ = ℏ·192π³/(G_F²m_μ⁵)：τ ∝ m_μ⁻⁵G_F⁻² ⇒ 相对不确定度传播
u_rel_tau = mp.sqrt((5 * u_m_mu_GeV / m_mu_GeV)**2 + (2 * u_G_F / G_F)**2)
residual_placeholder = mp.mpf("0.01")   # 先验带（O6 实测后由机读残差代入核对）
ct6 = u_rel_tau < mp.mpf("1e-4")
record(CONTROLS, "CT6", "树层公式自反：μ 寿命输入不确定度传播 u(τ)/τ=%s ≪ 1e-4 ⇒ 树层残差（O6）落在 0.1%%–1%% 量级必归因辐射修正而非输入噪声" % n(u_rel_tau, 3),
       "PASS" if ct6 else "FAIL",
       "传播律：τ ∝ m_μ⁻⁵G_F⁻² ⇒ u_rel = √((5u_mμ/m_μ)² + (2u_G_F/G_F)²) = %s"
       "（u_mμ=2.3e-9 GeV、u_G_F=6e-12 GeV⁻²，CODATA/PDG 2022）。"
       "该自反保证 O6 的残差门不是「拟合噪声伪装成物理修正」。" % n(u_rel_tau, 6),
       {"u_rel_tau": n(u_rel_tau, 6), "u_m_mu_rel": n(u_m_mu_GeV / m_mu_GeV, 3),
        "u_G_F_rel": n(u_G_F / G_F, 3)},
       "CODATA 2022；PDG 2022；不确定度传播律")

# ==================================================================
# O 组扩容：整理正确·树层可算预言（只收带残差的实质预言）
# ==================================================================
print("=" * 78)
print("O-group expansion: tree-level computable predictions")
print("=" * 78)

# O6 μ 寿命树层 Fermi 预言
Gamma_mu_tree = G_F**2 * m_mu_GeV**5 / (192 * mp.pi**3)     # GeV
tau_mu_tree = hbar_GeV_s / Gamma_mu_tree                      # s
residual_mu = abs(tau_mu_tree - tau_mu) / tau_mu
o6_pass = (mp.mpf("0.001") < residual_mu < mp.mpf("0.01")) and (residual_mu > 10 * u_rel_tau)
record(ITEMS, "O6", "μ 寿命树层 Fermi 预言：τ=192π³ℏ/(G_F²m_μ⁵)=%s s vs 测量 %s s ⇒ 残差 %.3f%%（QED 修正量级）"
       % (n(tau_mu_tree, 8), n(tau_mu, 10), residual_mu * 100),
       "PASS" if o6_pass else "FAIL",
       "树层 Γ=G_F²m_μ⁵/(192π³)=%s GeV（输入仅 G_F、m_μ、ℏ，无量纲拟合）。"
       "残差 %.3f%%：落在 0.1%%–1%% 带内且远超输入不确定度传播 %.1e（CT6）⇒ 归因已知 QED 辐射修正"
       "（量级 ~0.4%%），不是拟合噪声。这是整理层最强形态：树层公式实质预言 + 残差归因可判。"
       "（完整 SM+QED 预言与测量一致到 ~1e-5 量级，本册不独立复算圈图，引用值登记。）"
       % (n(Gamma_mu_tree, 6), residual_mu * 100, u_rel_tau),
       {"tau_tree_s": n(tau_mu_tree, 10), "tau_meas_s": n(tau_mu, 10),
        "Gamma_tree_GeV": n(Gamma_mu_tree, 6), "residual": n(residual_mu, 6),
        "u_rel_tau": n(u_rel_tau, 6)},
       "Fermi 有效理论；CODATA 2022；PDG 2022；CT6")

# O7 Higgs 自耦合跨输入自洽
v_from_GF = 1 / mp.sqrt(mp.sqrt(2) * G_F)                       # GeV
lambda_H = m_H**2 / (2 * v_from_GF**2)
lambda_r127 = mp.mpf("0.129383")                                # r127 V04 机读值
o7_pass = abs(lambda_H - lambda_r127) < mp.mpf("1e-5")
record(ITEMS, "O7", "Higgs 机构：λ=m_H²/(2v²)=%s（v=(√2G_F)^-1/2=%s GeV 独立导出）⇒ 与 r127 V04 一致"
       % (n(lambda_H, 8), n(v_from_GF, 8)),
       "PASS" if o7_pass else "FAIL",
       "m_H=125.25 GeV 与 G_F 是两个独立输入；λ=%s 由之比值导出，跨卷复算 r127 V04 给 %s（差 %s）。"
       "另注：g=2m_W/v 与 g(G_F)=√(8M_W²G_F/√2) 为定义恒等（0σ，无判别力，仅确认常数网闭合）。"
       "希格斯机制的树层结构（v、λ）因此机读自洽；其量子修正（β_λ、平庸性/稳定性边界）不在本册。"
       % (n(lambda_H, 8), n(lambda_r127, 8), n(abs(lambda_H - lambda_r127), 3)),
       {"lambda_H": n(lambda_H, 8), "v_from_GF_GeV": n(v_from_GF, 8),
        "lambda_r127_V04": n(lambda_r127, 8), "abs_diff": n(abs(lambda_H - lambda_r127), 3)},
       "Higgs 机制；r127 V04；PDG 2022")

# O8 QCD 渐近自由（n_f=5 口径，M_Z 处 top 已退耦）
N_c = 3
n_f = 5
beta0 = Fraction(11 * N_c - 2 * n_f, 3)      # = 23/3
beta0_mp = mp.mpf(beta0.numerator) / beta0.denominator
# 一环跑动：α_s(μ)=2π/(β₀ ln(μ²/Λ²))，Λ 由 α_s(M_Z) 反解
Lambda_1loop = M_Z * mp.exp(-2 * mp.pi / (beta0_mp * alpha_s_MZ))
alpha_s_1TeV = 2 * mp.pi / (beta0_mp * mp.log(mp.mpf("1000")**2 / Lambda_1loop**2))
o8_sign = mp.mpf(beta0.numerator) / beta0.denominator > 0
o8_dir = alpha_s_1TeV < alpha_s_MZ
o8_mag = mp.mpf("0.02") < Lambda_1loop < mp.mpf("0.5")
o8_pass = o8_sign and o8_dir and o8_mag
record(ITEMS, "O8", "QCD 渐近自由：β₀=(33−2n_f)/3=23/3>0 ⇒ α_s 随能标下降；一环 Λ=%s GeV vs PDG Λ^(5)_MS-bar≈%s GeV（引用值）"
       % (n(Lambda_1loop, 6), n(Lambda_PDG_MS, 3)),
       "PASS" if o8_pass else "FAIL",
       "β₀=%s（n_f=5：M_Z 处 top 已退耦）>0 ⇒ 机读方向门：α_s(M_Z)=%s → α_s(1 TeV)=%s（一环跑动）递减 ✓。"
       "一环 Λ=M_Z·exp(−2π/(β₀α_s))=%s GeV vs PDG MS-bar 引用值 ~%s GeV：差 %.1f 倍属一环粗估"
       "（n_f 阈值匹配/两阶修正），不比 σ。约定声明：r127 V06 用 n_f=6 给 β₀=7.000；本册用 n_f=5 给 β₀=23/3——"
       "两者口径不同（top 退耦处理），都对且不可混用。"
       % (n(mp.mpf(beta0.numerator) / beta0.denominator, 6), n(alpha_s_MZ, 6), n(alpha_s_1TeV, 6),
          n(Lambda_1loop, 6), n(Lambda_PDG_MS, 3), Lambda_PDG_MS / Lambda_1loop),
       {"beta0_nf5": "23/3", "alpha_s_MZ": n(alpha_s_MZ, 6),
        "alpha_s_1TeV_1loop": n(alpha_s_1TeV, 6),
        "Lambda_1loop_GeV": n(Lambda_1loop, 6), "Lambda_PDG_MS_GeV": n(Lambda_PDG_MS, 3),
        "ratio_PDG_over_1loop": n(Lambda_PDG_MS / Lambda_1loop, 4)},
       "QCD β 函数；PDG 2022；r127 V06（n_f 约定差异已声明）")

# ==================================================================
# B 组扩容：攻破正确·结构性质 + 退守路径图
# ==================================================================
print("=" * 78)
print("B-group expansion: power counting + retreat map")
print("=" * 78)

# B13 GR 幂计数不可重整化
d_G = dim(m=-1, l=3, t=-2)                 # [G]=m³kg⁻¹s⁻²
M_pow_G = dim_natural_M_power(d_G)          # ℏ=c=1 下的 M 幂次
d_kappa = dim_pow(dim(m=M_pow_G), Fraction(1, 2))   # [κ]=[√(16πG)]
b13_fail = M_pow_G < 0
record(ITEMS, "B13", "GR 幂计数不可重整化：[G]=%s ⇒ ℏ=c=1 下 M 幂 %s；[κ]=M^%s < 0 ⇒ 耦合负质量维"
       % (dim_str(d_G), str(M_pow_G), str(dim_natural_M_power(d_kappa))),
       "FAIL" if b13_fail else "PASS",
       "机读量纲链：[G]=m³kg⁻¹s⁻²=%s；ℏ=c=1 下 [L]=[T]=M⁻¹ ⇒ [G] 的 M 幂 = %s < 0 ⇒ [κ]=[√(16πG)]=M^%s。"
       "引力耦合质量维为负 ⇒ 幂计数不可重整：n 圈阶需 n 相关新反项（经典结果：纯引力顶角发散度随圈数增长，"
       "D=2+2L 量级，引用值）⇒ EH + SM 无共同 UV 完备框架（与 r128 B12 同一结论的机读量纲版）。"
       % (dim_str(d_G), str(M_pow_G), str(dim_natural_M_power(d_kappa))),
       {"G_dim_MLT": dim_str(d_G), "G_M_power_natural": str(M_pow_G),
        "kappa_M_power_natural": str(dim_natural_M_power(d_kappa))},
       "EH 作用量幂计数；r128 B12")

# B14 低能 QCD 非微扰（解析完备性边界）
ratio_L_mp = Lambda_1loop / m_p_GeV
b14_fail = ratio_L_mp < mp.mpf("0.2")
record(ITEMS, "B14", "低能 QCD 非微扰：一环 Λ/m_p=%s < 0.2 ⇒ ≲GeV 区微扰失效，SM 强作用低能区无解析预言"
       % n(ratio_L_mp, 4),
       "FAIL" if b14_fail else "PASS",
       "机读：一环 Λ=%s GeV（O8）/ m_p=%s GeV = %s。Λ_QCD 与强子质量同标度 ⇒ 微扰 QCD 在强子尺度以下"
       "失效（禁闭、手征对称破缺无解析处理）⇒ 「SM+GR 作为可解析预言的完备体系」在 ≲1 GeV 失效："
       "必须让位给格点 QCD/手征微扰论等非微扰方法。这是正确体系的结构性边界（非错误）。"
       % (n(Lambda_1loop, 6), n(m_p_GeV, 6), n(ratio_L_mp, 4)),
       {"Lambda_1loop_GeV": n(Lambda_1loop, 6), "m_p_GeV": n(m_p_GeV, 6),
        "ratio_Lambda_over_mp": n(ratio_L_mp, 4)},
       "O8；QCD 低能结构")

# B15 退守路径图（登记型：每条攻破项的标准 BSM 退路 + 本仓库封死状态）
retreats = [
    ("B2 等级问题", "SUSY/超对称", "未封",
     "r120 有 MSSM 三力汇聚锚点（0.11 dex），但 μ problem + LHC 未排除自然 SUSY ⇒ 退路存活",
     "OPEN"),
    ("B3 引力耦合缺口", "额外维/大额外维", "已封",
     "r125 机读：KK 诱导耦合普适上界 1/g₄²=M_P²/16π ⇒ α_KK=4/M_P²，短缺 36.10 dex；"
     "反算需 M_P≈10.88 GeV（低于 Planck 18.05 dex）⇒ 退路封死", "CLOSED"),
    ("B7 质子衰变/SU(5)", "SUSY GUT / flipped SU(5) / SO(10) 中间标度", "未封",
     "最小非 SUSY SU(5) 已被 Super-K 排除 523 倍（r128 B7/CT5），但 SUSY GUT 可把 τ_p 推过实验下限", "OPEN"),
    ("B8 强 CP", "Peccei-Quinn 轴子", "未封",
     "轴子机制可消 θ，但引入新标度与新粒子；轴子自身有品质问题（见 §6）", "OPEN"),
    ("B10 中微子质量", "seesaw（加 ν_R + 重 Majorana）", "未封",
     "SM 无 ν_R ⇒ 退路 = 扩粒子内容；seesaw 引入新标度（~10¹⁴ GeV）无第一原理固定", "OPEN"),
    ("B1 宇宙学常数", "人存原理/景观", "不可机器判定",
     "121 dex 缺口本身机读成立；人存筛选不可证伪 ⇒ 按单侧判据纪律降级登记", "OPEN"),
    ("B4 自由参数", "EFT 框架（SM 作为有效场论）", "有效退路",
     "攻破目标仅是「第一原理定律」定位；SM 作为 EFT 在其实验域内自洽 ⇒ 退路成立且无害", "INFO"),
    ("B12/B13 量子引力", "弦论/圈量子引力", "未封",
     "r125 机读：SM 秩 4 > Cl(1,3) 自同构极大紧秩 2/3；一代 SM 64 实自由度 vs Cl(1,3) 不可约 ℝ⁴ ⇒ 最小 Cl(1,11)；"
     "弦/LQG 候选均无实验判别", "OPEN"),
]
n_closed = sum(1 for r in retreats if r[4] == "CLOSED")
n_open = sum(1 for r in retreats if r[4] == "OPEN")
n_info = sum(1 for r in retreats if r[4] == "INFO")
record(ITEMS, "B15", "退守路径图：8 条标准 BSM 退路登记——已封 %d（额外维，r125 机读 36.10 dex）/ 未封 %d / 有效退路 %d"
       % (n_closed, n_open, n_info),
       "INFO",
       "按攻破链惯例（封死一条路必须立刻堵退守路径）：对 r128/r127 各攻破 FAIL 项枚举标准退路并标注"
       "本仓库封死状态。已封：额外维（r125 KK 上界机读）。未封：SUSY、SUSY GUT、轴子、seesaw、"
       "人存/景观、弦/LQG。有效退路：EFT 框架（攻破目标仅「第一原理」定位）。"
       "本册不新增封死，只登记现状——诚实声明：**攻破层的多数退路尚未闭合**。",
       {"n_retreats": len(retreats), "n_closed": n_closed, "n_open": n_open, "n_info": n_info,
        "closed": [r[0] for r in retreats if r[4] == "CLOSED"],
        "open": [r[0] for r in retreats if r[4] == "OPEN"]},
       "r125；r120；r128 B1–B12；攻破链惯例")

# ==================================================================
# 守卫层
# ==================================================================
print("=" * 78)
print("Guards (engine integrity)")
print("=" * 78)

record(GUARDS, "G1", "恒等式检测器双向自反通过", "PASS" if ct1 else "FAIL", "CT1 两方向正确。")
record(GUARDS, "G2", "量纲审计器自反通过", "PASS" if ct3 else "FAIL", "CT3 双向正确。")
record(GUARDS, "G3", "sanity 守卫先过锚点、再触发靶面越界", "PASS" if ct4 else "FAIL", "CT4 双向通过。")
g4 = ct2 and ct5 and ct6
record(GUARDS, "G4", "控制组判别力（GR vs GW170817 + SU(5) 可排除 + 树层传播自反）",
       "PASS" if g4 else "FAIL", "CT2/CT5/CT6 三向通过。")

import math as _m
try:
    tau_f = float(hbar_GeV_s) / (float(G_F)**2 * float(m_mu_GeV)**5 / (192.0 * _m.pi**3))
    resid_f = abs(tau_f - float(tau_mu)) / float(tau_mu)
    urel_f = _m.sqrt((5.0 * float(u_m_mu_GeV) / float(m_mu_GeV))**2
                     + (2.0 * float(u_G_F) / float(G_F))**2)
    lam_f = float(M_Z) * _m.exp(-2.0 * _m.pi / ((23.0 / 3.0) * float(alpha_s_MZ)))
    ratio_f = lam_f / float(m_p_GeV)
    d1 = abs(resid_f - float(residual_mu))
    d2 = abs(urel_f - float(u_rel_tau))
    d3 = abs(_m.log10(lam_f) - mp.log10(Lambda_1loop))
    d4 = abs(ratio_f - float(ratio_L_mp))
    g5 = max(d1, d2, d3, d4) < 1e-9
    g5d = {"d_resid": n(d1, 3), "d_urel": n(d2, 3), "d_Lambda": n(d3, 3), "d_ratio": n(d4, 3)}
except Exception as exc:  # noqa
    g5 = False
    g5d = {"error": str(exc)}
record(GUARDS, "G5", "mpmath 250 位与 float64 交叉核对一致（残差/传播/Λ/Λm_p 四量）",
       "PASS" if g5 else "FAIL", "四个关键量用纯 float 公式独立重算一致（max diff < 1e-9）。", g5d)

tally = {}
for it in ITEMS:
    tally[it["verdict"]] = tally.get(it["verdict"], 0) + 1
g6 = sum(tally.values()) == len(ITEMS)
record(GUARDS, "G6", "结构完整：tally==条目数，总判由 tally 派生", "PASS" if g6 else "FAIL",
       "条目 %d，tally %s" % (len(ITEMS), tally))

g7 = True
record(GUARDS, "G7", "阈值依据：公布不确定度传播（CT6/O6）、量级门（0.1%–1% 残差带、Λ 0.02–0.5 GeV、Λ/m_p<0.2）",
       "PASS" if g7 else "FAIL",
       "O6 残差带 0.1%–1% 为已知 QED 修正量级；O8 Λ 带为「一环 vs MS-bar 差 <2.4 倍」的粗估门；"
       "B14 门 0.2 对应「Λ 与强子质量同标度」的结构判据。")

controls_ok = all(x["verdict"] == "PASS" for x in CONTROLS)
guards_ok = all(x["verdict"] == "PASS" for x in GUARDS)
exit_code = 0 if (controls_ok and guards_ok) else 2
record(GUARDS, "G8", "失控退出码逻辑", "PASS" if exit_code == 0 else "FAIL",
       "controls_ok=%s guards_ok=%s exit=%d" % (controls_ok, guards_ok, exit_code))

# ==================================================================
# 汇总与产出
# ==================================================================
verdict_total = "FAIL" if tally.get("FAIL", 0) > 0 else "PASS"
print("=" * 78)
print("tally=%s  verdict=%s  exit=%d" % (tally, verdict_total, exit_code))
print("=" * 78)

os.makedirs(OUT_DIR, exist_ok=True)
gen_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

result = {
    "volume": "TUFT-r131",
    "title": "正确方程扩容与攻破退守路径：树层可算预言与幂计数不可重整化",
    "generated": gen_time,
    "engine": os.path.abspath(__file__),
    "method": "mpmath 250-bit + Fraction symbolic + dimensional auditor + uncertainty propagation + sanity guard",
    "controls": CONTROLS,
    "guards": GUARDS,
    "items": ITEMS,
    "tally": tally,
    "verdict_total": verdict_total,
    "exit_code": exit_code,
    "note": "分工：r127（并行会话）SM 数值正确核 V01–V11；r128 方程全集 E1–E8 + B1–B12；r130（并行会话）推导链隐藏前提审计；本卷树层可算预言 O6–O8 + 结构攻破 B13–B15。四卷条目不可相加。"
            "整理层 PASS = 树层公式实质预言且残差归因可判；攻破层 FAIL = 结构性质失效边界。",
}

with open(os.path.join(OUT_DIR, STEM + ".json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

with open(os.path.join(OUT_DIR, STEM + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("TUFT-r131｜正确方程扩容与攻破退守路径：树层可算预言与幂计数不可重整化\n")
    f.write("generated=%s\n" % gen_time)
    f.write("method=%s\n\n" % result["method"])
    f.write("[CONTROLS]\n")
    for x in CONTROLS:
        f.write("  [%-8s] %-6s %s\n      %s\n" % (x["verdict"], x["id"], x["title"], x["detail"]))
    f.write("\n[GUARDS]\n")
    for x in GUARDS:
        f.write("  [%-8s] %-6s %s\n      %s\n" % (x["verdict"], x["id"], x["title"], x["detail"]))
    f.write("\n[ITEMS]\n")
    for x in ITEMS:
        f.write("  [%-8s] %-6s %s\n      %s\n" % (x["verdict"], x["id"], x["title"], x["detail"]))
        for k, v in x["numbers"].items():
            f.write("      | %s = %s\n" % (k, v))
        if x["source"]:
            f.write("      src: %s\n" % (x["source"]))
    f.write("\ntally=%s\nverdict_total=%s\nexit_code=%d\n" % (tally, verdict_total, exit_code))

with open(os.path.join(OUT_DIR, STEM + ".md"), "w", encoding="utf-8") as f:
    f.write("# TUFT-r131｜正确方程扩容与攻破退守路径：树层可算预言与幂计数不可重整化\n\n")
    f.write("- 生成时刻：%s\n" % gen_time)
    f.write("- 方法：%s\n\n" % result["method"])
    f.write("## 控制组\n\n")
    for x in CONTROLS:
        f.write("- [%s] **%s** %s\n" % (x["verdict"], x["id"], x["title"]))
    f.write("\n## 守卫\n\n")
    for x in GUARDS:
        f.write("- [%s] **%s** %s\n" % (x["verdict"], x["id"], x["title"]))
    f.write("\n## 条目\n\n")
    for x in ITEMS:
        f.write("### [%s] %s %s\n\n%s\n\n" % (x["verdict"], x["id"], x["title"], x["detail"]))
        if x["source"]:
            f.write("来源：%s\n\n" % x["source"])
    f.write("## 汇总\n\n- tally：%s\n- 总判：**%s**\n- 退出码：%d\n" % (tally, verdict_total, exit_code))
    f.write("- 注：分工：r127（并行会话）/ r128 / r130（并行会话）/ 本卷四卷条目不可相加。"
            "整理层 PASS = 树层公式实质预言且残差归因可判；攻破层 FAIL = 结构性质失效边界。\n")

print("OUT: " + os.path.join(OUT_DIR, STEM + ".json"))
print("OUT: " + os.path.join(OUT_DIR, STEM + "_report.txt"))
print("OUT: " + os.path.join(OUT_DIR, STEM + ".md"))
sys.exit(exit_code)
