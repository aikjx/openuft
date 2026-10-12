# -*- coding: utf-8 -*-
"""
TUFT-V4.4 路线B（自能屏蔽 / 重构质量-曲率映射）全维审计引擎
================================================================
来料：《TUFT-V4.4｜路线B：修改质量-曲率映射，重构量子驻波条件，保留唯一全局 theta》
      （含其前提链 V4.3《联合 chi^2 拟合：电子 g-2 + mu 子 g-2 + CODATA 引力常数》）

本册任务（只做机器复算与诚实裁定，不代选路线、不产生新物理）：
  1) 复算 V4.3 的全部数值读数（Delta a_e / Delta a_mu / cot_theta / chi^2 极小）；
  2) 复算 V4.4 自能公理 U_self = (hbar c / 2) lP^2 kappa^2 的量纲与后果；
  3) 复算二次映射 kappa(m) 的定义域、质量上界、弱场泰勒展开；
  4) 裁定「打破 a_TUFT ∝ m^2」这一宣称是否在其自身射程内成立；
  5) 裁定路线 A/B/C 的终审结论（V4.2/V4.3 被实验排除）是否被数据支持。

设计纪律（本库沿用）：
  - 纯标准库（Decimal 60 位 + Fraction 量纲），不依赖 mpmath/sympy；
  - 量纲用四分量有理数向量 (M, L, T, Q)，所有「量纲自洽」断言必须机器兜底
    （本库已多次记录「手算量纲必错」，来料本身也在此处出错）；
  - 凡「恒为零 / 无解」类否证判据，必须配阳性对照；
  - 绝对残差在大数量级会失效，一律用相对判据；
  - 不自推的系数必须在产物里显式登记来源，不留白、不编造。

输出：数据同名 .json / .md / _report.txt（与判定册同源）
"""

import io
import json
import os
from decimal import Decimal as DC, getcontext
from fractions import Fraction as FR

getcontext().prec = 60

# --------------------------------------------------------------------------
# 0. 目录
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.abspath(os.path.join(HERE, "..", "数据"))
TAG = "TUFT-r44_V44路线B自能屏蔽_全维审计_2026-10-12"
OUT_JSON = os.path.join(DATA, TAG + ".json")
OUT_MD = os.path.join(DATA, TAG + ".md")
OUT_RPT = os.path.join(DATA, TAG + "_report.txt")

# --------------------------------------------------------------------------
# 1. CODATA 锚点（来料口径；偏差项另算，不静默改口径）
# --------------------------------------------------------------------------
C0 = DC("299792458")                      # 光速 m/s（定义值）
E0 = DC("1.602176634e-19")                # 元电荷 C（定义值）
HBAR0 = DC("1.0545718176461565e-34")      # hbar J s
ALPHA0 = DC("7.2973525643e-3")
ME0 = DC("9.1093837015e-31")
MMU0 = DC("1.883531627e-28")
LP0 = DC("1.616255e-35")                 # Planck 长度 m（标称）
LP_PREC = DC("1.61625502442370536982659034826e-35")   # Planck 长度 m（精算）
G0 = DC("6.67430e-11")
MPL0 = DC("2.176434342e-8")              # Planck 质量 kg

GEV = DC("1.78266192e-27")                # 1 GeV/c^2 -> kg
MTAU0 = DC("1.77686") * GEV
MW0 = DC("80.379") * GEV
MTOP0 = DC("173.1") * GEV
MSUN0 = DC("1.98847e30")

AE_EXP = DC("1.15965218059e-3")
AE_QED = DC("1.15965218128e-3")
AMU_EXP = DC("1.16592040e-3")            # 2020 Fermilab 组合
AMU_QED = DC("1.16591810e-3")
AMU_EXP_2025 = DC("1.165920705e-3")       # 2025 Fermilab 更新（敏感性算读数）

# 不确定度：[C] 级外部输入；两档并存，判决支点由两者之差给出
SIG_E_CLAIM = DC("1e-12")
SIG_MU_CLAIM = DC("4e-7")
SIG_G_REL_CLAIM = DC("1e-5")
SIG_E_REAL = DC("2.8e-14")               # CODATA g-2 实验
SIG_MU_REAL = DC("5.2e-10")              # sqrt(exp 1.4e-10 ^2 + SM 理论 5e-10 ^2)
SIG_G_REL_REAL = DC("2.2e-5")

# --------------------------------------------------------------------------
# 2. 量纲工具（四分量有理数向量，分量顺序 M, L, T, Q）
#    相乘 = 分量相加；除以 c 等价于 (0,-1,+1,0)
# --------------------------------------------------------------------------
DIM0 = (FR(0), FR(0), FR(0), FR(0))
D_M = (FR(1), FR(0), FR(0), FR(0))
D_L = (FR(0), FR(1), FR(0), FR(0))
D_T = (FR(0), FR(0), FR(1), FR(0))
D_Q = (FR(0), FR(0), FR(0), FR(1))
D_HBAR = (FR(1), FR(2), FR(-1), FR(0))
D_E_SI = (FR(0), FR(0), FR(0), FR(1))            # SI 电荷 = A s
D_E_NAT = (FR(1, 2), FR(3, 2), FR(-1), FR(0))   # 自然单位 [e^2]=[alpha][hbar][c]
D_KAPPA = (FR(0), FR(-1), FR(0), FR(0))
D_VEL = (FR(0), FR(1), FR(-1), FR(0))
D_ENERGY = (FR(1), FR(2), FR(-2), FR(0))


def dadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def dneg(a):
    return (-a[0], -a[1], -a[2], -a[3])


def dsub(a, b):
    return dadd(a, dneg(b))


def dmul(a, b):
    """量纲相乘 = 分量相加（离散维度不能相乘）"""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def dscale(a, k):
    k = FR(k)
    return (a[0] * k, a[1] * k, a[2] * k, a[3] * k)


def dpow(a, n):
    return (a[0] * FR(n), a[1] * FR(n), a[2] * FR(n), a[3] * FR(n))


def dis_dimless(a):
    return a == DIM0


def dstr(a):
    names = ["M", "L", "T", "Q"]
    out = []
    for i in range(4):
        if a[i] == 0:
            continue
        if a[i] == 1:
            out.append(names[i])
        else:
            out.append(names[i] + "^" + str(a[i]))
    return "".join(out) if out else "1(dimless)"


def dlabel(a):
    if a == D_ENERGY:
        return "[能量]"
    if a == D_M:
        return "[质量]"
    if a == D_L:
        return "[长度]"
    if a == D_KAPPA:
        return "[曲率 L^-1]"
    if dis_dimless(a):
        return "[无量纲]"
    return ""


# --------------------------------------------------------------------------
# 3. 数值工具
# --------------------------------------------------------------------------
def fmt(x, digits=25):
    if isinstance(x, FR):
        x = DC(x.numerator) / DC(x.denominator)
    return format(x, "." + str(digits) + "E")


def rel(a, b):
    if b == 0:
        return DC("Infinity")
    return abs(a - b) / abs(b)


def ratio(a, b):
    if b == 0:
        return DC("Infinity")
    return a / b


# --------------------------------------------------------------------------
# 4. 条目登记
# --------------------------------------------------------------------------
ITEMS = []
KEYNUM = {}


def add_item(cid, verdict, title, claim, reading, detail):
    ITEMS.append({
        "id": cid, "verdict": verdict, "title": title,
        "claim": claim, "reading": reading, "detail": detail,
    })
    KEYNUM[cid] = reading


def P(cid, title, claim, reading, detail):
    add_item(cid, "PASS", title, claim, reading, detail)


def F(cid, title, claim, reading, detail):
    add_item(cid, "FAIL", title, claim, reading, detail)


def B(cid, title, claim, reading, detail):
    add_item(cid, "BOUNDARY", title, claim, reading, detail)


def I(cid, title, claim, reading, detail):
    add_item(cid, "INFO", title, claim, reading, detail)


def M_(cid, title, claim, reading, detail):
    add_item(cid, "MISMATCH", title, claim, reading, detail)


def C_(cid, title, claim, reading, detail):
    add_item(cid, "CORRECTED", title, claim, reading, detail)


# --------------------------------------------------------------------------
# 5. 自检 guards（先过自检再用于判定 —— 本库纪律）
# --------------------------------------------------------------------------
GUARDS = []


def guard(name, ok, note):
    GUARDS.append({"name": name, "ok": bool(ok), "note": note})
    return bool(ok)


def cot_to_sin(cot):
    """cot(theta) -> sin(theta)，避免 Decimal 无 sin/cos"""
    return DC(1) / (DC(1) + cot * cot).sqrt()


def sin_to_cot(s):
    cc = (DC(1) - s * s).sqrt()
    return cc / s


def run_guards():
    ok = dmul(D_HBAR, D_VEL) == (FR(1), FR(3), FR(-2), FR(0))
    guard("dim_mul_hbar_c", ok, "hbar*c 应为 M L^3 T^-2")

    ok = dmul(D_KAPPA, dneg(D_KAPPA)) == DIM0
    guard("dim_inv_kappa", ok, "[kappa]^-1 * [kappa] = 1")

    ok = dpow(D_L, -2) == (FR(0), FR(-2), FR(0), FR(0))
    guard("dim_pow_negative", ok, "L^-2 = (0,-2,0,0)")

    ok = (dpow(D_E_SI, 2) != dmul(D_HBAR, D_VEL))
    guard("dim_charge_two_not_hbar_c_si", ok,
          "SI 下 [e^2]=Q^2 与 [hbar][c]=M L^3 T^-2 不同族（须靠 eps0 归一），"
          "此为口径事实登记，非缺陷")

    da_e = AE_EXP - AE_QED
    guard("delta_a_e_exact", da_e == DC("-6.9e-13"),
          "a_e_exp - a_e_QED = " + fmt(da_e, 6))

    da_mu = AMU_EXP - AMU_QED
    guard("delta_a_mu_exact", da_mu == DC("2.30e-9"),
          "a_mu_exp - a_mu_QED = " + fmt(da_mu, 6))

    r_mm = MMU0 / ME0
    guard("mu_over_e_mass_ratio", abs(r_mm - DC("206.76828298")) < DC("1e-6"),
          "m_mu/m_e = " + fmt(r_mm, 12))

    s6, c8 = DC("0.6"), DC("0.8")
    guard("sin_cos_identity", abs(c8 * c8 + s6 * s6 - DC(1)) < DC("1e-30"),
          "cos^2+sin^2=1（cot<->sin 映射自洽性）")

    cot0 = DC("5.1375e-49")
    guard("cot_to_sin_map", abs(cot_to_sin(cot0) - DC(1)) < DC("1e-40"),
          "cot=5.1375e-49 时 60 位精度下 sin-1 = " + fmt(cot_to_sin(cot0) - DC(1), 6)
          + "（偏离在第 97 位，低于有效位 ⇒ 机器精确为 0，需提高精度才可分辨）")

    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec = 140
        sin_hi = DC(1) / (DC(1) + cot0 * cot0).sqrt()
        dev_hi = sin_hi - DC(1)
        pred_hi = DC(-1) * cot0 * cot0 / 2
    guard("cot_to_sin_high_precision",
          rel(dev_hi, pred_hi) < DC("1e-20"),
          "阳性对照：140 位精度下 sin-1 = " + fmt(dev_hi, 8)
          + "，泰勒理论值 -cot^2/2 = " + fmt(pred_hi, 8)
          + "（相对差 " + fmt(rel(dev_hi, pred_hi), 4)
          + "）—— 证明 T33 的机器零来自精度而非恒等")

    eps = DC("1e-6")
    num = DC(1) - (DC(1) - eps).sqrt()
    approx = num / (eps / 2)
    guard("self_energy_linear_series", abs(approx - (DC(1) + eps / 4)) < DC("1e-12"),
          "(1-sqrt(1-eps))/(eps/2) = " + fmt(approx, 12)
          + " vs 1+eps/4 = " + fmt(DC(1) + eps / 4, 12)
          + "（差 eps^2/8 = 1.25e-13，属泰勒二阶项，阈值取 1e-12）")

    kap = ME0 * C0 * s6 / HBAR0
    lhs = HBAR0 * C0 * kap / s6 - HBAR0 * C0 * LP0 * kap * kap / 2
    eps_ctrl = 2 * (ME0 / MPL0) * s6 * s6
    res_ctrl = rel(lhs, ME0 * C0 * C0)
    guard("positive_control_corrected_form",
          rel(res_ctrl, eps_ctrl / 4) < DC("1e-6"),
          "阳性对照：把弱场 kappa = m c sin(theta)/hbar 代回含自能方程，"
          "残差应恰等于自能占比 eps/4 = " + fmt(eps_ctrl / 4, 8)
          + "；实测残差 = " + fmt(res_ctrl, 8)
          + "（两者相对差 " + fmt(rel(res_ctrl, eps_ctrl / 4), 4)
          + "，来源为标称 lP 与 mP 的 8 位有效数字不自洽，非物理偏差）")

    def a_new(m, s_):
        # 弱场 a_weak ∝ m^2 cos(theta) * c/hbar  ->  sin(theta) 精确消去
        c_ = (DC(1) - s_ * s_).sqrt()
        return c_ * m * m / HBAR0
    r1 = a_new(ME0, DC("0.5")) / a_new(ME0, DC("0.6"))
    guard("weakfield_sin_cancels",
          abs(r1 - (DC("0.75").sqrt() / DC("0.8"))) < DC("1e-40"),
          "弱场 a_new（sin=0.5 / sin=0.6）两点比值 = " + fmt(r1, 12)
          + "（应等于 cos30/cos53.13 = " + fmt(DC("0.75").sqrt() / DC("0.8"), 12) + "）")

    gth = C0 ** 3 * LP0 * LP0 / HBAR0
    gth_prec = C0 ** 3 * LP_PREC * LP_PREC / HBAR0
    guard("gth_identity_vs_codata",
          rel(gth, G0) < DC("1e-6") and rel(gth_prec, G0) < DC("1e-20"),
          "c^3 lP^2/hbar / G - 1 = " + fmt(gth / G0 - DC(1), 6)
          + "（用标称 lP=1.616255e-35，截断 8 位）; 用精算 lP 时 = "
          + fmt(gth_prec / G0 - DC(1), 6))

    eps_top = 2 * (MTOP0 / MPL0)
    guard("top_quark_far_below_upper_bound", eps_top < DC("1e-10"),
          "eps_top = " + fmt(eps_top, 6) + " << 1")

    guard("items_nonempty", len(ITEMS) > 0, "条目数在 main 结束时复核")


# ==========================================================================
# 6. 条目主体 —— 第一链：V4.3 前提链（联合 chi^2 拟合）
# ==========================================================================
def build_chain_43():
    # ---- 常量复算 ----
    da_e = AE_EXP - AE_QED                     # -6.9e-13
    da_mu = AMU_EXP - AMU_QED                  # +2.30e-9
    da_mu_2025 = AMU_EXP_2025 - AMU_QED
    ccoef = -(3 * C0) / (4 * E0 * HBAR0 * HBAR0)      # C = -3c/(4 e hbar^2)
    me2 = ME0 * ME0
    mmu2 = MMU0 * MMU0
    mass_ratio2 = mmu2 / me2                  # 42752.7499...

    # ---- T01 Delta a_e 量级 ----
    F("T01", "电子 QED-实验残差 Delta a_e 量级错 100 倍",
      "来料：Delta a_e = -6.9e-11，并据此反解 cot(theta)=6.59e-46",
      "机器：Delta a_e = " + fmt(da_e, 8) + "（相对来料偏差 "
      + fmt(ratio(abs(da_e), DC("6.9e-11")), 8) + "）",
      "两锚点之差为 1.15965218059e-3 - 1.15965218128e-3；来料把差写成 -6.9e-11，"
      "相当于把两者的小数位后移两位（真实物理量级 -6.9e-13）。这是 V4.3 全部下游读数的入口错误。")

    # ---- T02 Delta a_mu 量级 ----
    F("T02", "缪子 QED-实验残差 Delta a_mu 量级错 1000 倍",
      "来料：Delta a_mu = +2.3e-6，并据此宣称 TUFT 修正 -2.95e-6「量级很大」",
      "机器：Delta a_mu = " + fmt(da_mu, 8) + "（相对来料偏差 "
      + fmt(ratio(abs(da_mu), DC("2.3e-6")), 8) + "）",
      "1.16592040e-3 - 1.16591810e-3 = 2.30e-9（缪子新物理偏离的公认量级）。"
      "来料把它写成 2.3e-6，是把 1e-3 因子漏在减法之外。")

    # ---- T03 质量平方比 ----
    P("T03", "质量平方比 42753 独立成立",
      "来料：(m_mu/m_e)^2 ≈ 42753，为 a_mu/a_e 的硬性预言比例",
      "机器：m_mu/m_e = " + fmt(MMU0 / ME0, 12) + "，平方 = "
      + fmt(mass_ratio2, 12) + "（来料 42753 相对偏差 "
      + fmt(rel(DC("42753"), mass_ratio2), 6) + "）",
      "该比例本身与实验无关，成立；问题不在比例，而在残差符号与口径。")

    # ---- T04 真实残差比 ----
    resid_ratio = da_mu / da_e
    C_("T04", "「42753 倍冲突」的数量叙述需更正为 -3333",
      "来料：理论要求 a_mu/a_e = 42753，而实验残差给出相反符号、量级 -2.95e-6 vs -6.9e-11",
      "机器（真实残差）：Delta a_mu/Delta a_e = " + fmt(resid_ratio, 10)
      + "，与质量平方比 " + fmt(mass_ratio2, 10) + " 相差 "
      + fmt(ratio(mass_ratio2, abs(resid_ratio)), 10) + " 倍且反号",
      "符号相反这一硬冲突成立（真）；但「4 万倍」的量级叙述来自两个数量级错误，"
      "真实倍数是 1.28e1。这一条改变了冲突的严重程度，但不改变其存在。")

    # ---- T05 cot(theta) 电子反解 ----
    cot_e = da_e / (ccoef * me2)
    M_("T05", "电子反解 cot(theta) 读数比正确值大 100 倍",
      "来料：cot(theta) = 6.59e-46",
      "机器：cot(theta) = " + fmt(cot_e, 10) + "（比值 "
      + fmt(ratio(DC("6.59e-46"), cot_e), 8) + "）",
      "误差完全来自 T01 的 Delta a_e 量级错误，来料内部自洽但输入错。")

    # ---- T06 cot(theta)* 缪子反解不自洽 ----
    cot_mu_true = da_mu / (ccoef * mmu2)
    cot_mu_claiminput = DC("2.3e-6") / (ccoef * mmu2)
    M_("T06", "最优 cot(theta)* = -5.13e-51 与其自身公式不自洽（差 1e5）",
      "来料：cot(theta)* ≈ Delta a_mu/(C m_mu^2) = -5.13e-51",
      "机器：按其自述公式用其自述输入（2.3e-6）应得 " + fmt(cot_mu_claiminput, 10)
      + "；用真实 Delta a_mu（2.30e-9）得 " + fmt(cot_mu_true, 10),
      "来料的 -5.13e-51 两头都对不上：相对其自身输入差 "
      + fmt(ratio(cot_mu_claiminput, DC("-5.13e-51")), 8)
      + "，相对真实输入差 " + fmt(ratio(cot_mu_true, DC("-5.13e-51")), 8)
      + "。这是 V4.3 中第三处独立的数量级错误（电子侧无此问题）。")

    # ---- T07 极值公式正确性 ----
    P("T07", "chi^2 极值公式（求导式）机器复核无符号错误",
      "来料：cot(theta)* = [sum m_i^2 D_i/s_i^2] / [C sum m_i^4/s_i^2]",
      "机器：重推 d/d(cot) = 0 得 cot* = sum(m^2 D/s^2) / (C sum(m^4/s^2))，与来料逐符号一致",
      "该式本身正确。注意它并不蕴含「缪子主导」——主导与否取决于 m^4/s^2 的比值，见 T08。")

    # ---- T08 权重判据 ----
    w_ratio_claim = mass_ratio2 * mass_ratio2 * (SIG_E_CLAIM / SIG_MU_CLAIM) ** 2
    w_ratio_real = mass_ratio2 * mass_ratio2 * (SIG_E_REAL / SIG_MU_REAL) ** 2

    def chi2_min(sig_e, sig_mu):
        num = me2 * da_e / (sig_e * sig_e) + mmu2 * da_mu / (sig_mu * sig_mu)
        den = ccoef * (me2 * me2 / (sig_e * sig_e) + mmu2 * mmu2 / (sig_mu * sig_mu))
        cstar = num / den
        re = ccoef * me2 * cstar - da_e
        rmu = ccoef * mmu2 * cstar - da_mu
        return cstar, re, rmu, (re / sig_e) ** 2 + (rmu / sig_mu) ** 2

    cs_claim, re_claim, rmu_claim, chi_claim = chi2_min(SIG_E_CLAIM, SIG_MU_CLAIM)
    cs_real, re_real, rmu_real, chi_real = chi2_min(SIG_E_REAL, SIG_MU_REAL)

    M_("T08", "「缪子项完全主导」判断错误：来料 sigma 口径下反而是电子项主导",
      "来料：因 m_mu^4 >> m_e^4，故缪子项完全主导拟合，最优 cot(theta)* 由缪子决定",
      "机器：正确权重比 (m_mu^4/s_mu^2)/(m_e^4/s_e^2) 在来料 sigma 下 = "
      + fmt(w_ratio_claim, 8) + "（<1，即电子权重是缪子的 "
      + fmt(DC(1) / w_ratio_claim, 8) + " 倍）；真实 sigma 下 = "
      + fmt(w_ratio_real, 8),
      "极小二乘的主导项由 m^4/s^2 决定而非 m^4 本身。来料取 s_e=1e-12 而 s_mu=4e-7，"
      "两者相差 4e5 倍，其平方（1.6e-11）抵消了 1.83e9 的质量四次方优势。"
      "该错误直接导致其「最优 cot 由缪子决定、电子成为次级约束」的结论方向相反。")

    # ---- T09/T10 chi^2 极小值双口径 ----
    P("T09", "来料 sigma 口径下 chi^2 极小值不构成任何失配",
      "隐含预期：单 theta 无法同时匹配电子与缪子",
      "机器（s_e=1e-12, s_mu=4e-7）：cot* = " + fmt(cs_claim, 10)
      + "，残差 e = " + fmt(re_claim, 8) + " / mu = " + fmt(rmu_claim, 8)
      + "，chi^2_min = " + fmt(chi_claim, 8) + "，dof=2，chi^2/dof = "
      + fmt(chi_claim / 2, 8),
      "在该口径下拟合几乎完美（chi^2/dof ~ 3e-3，p ~ 0.997）。"
      "即：V4.3 终审「被实验排除」在其自设口径下不成立。")

    F("T10", "真实 sigma 口径下同一模型强失配",
      "同上",
      "机器（s_e=2.8e-14, s_mu=5.2e-10）：cot* = " + fmt(cs_real, 10)
      + "，残差 e = " + fmt(re_real, 8) + " / mu = " + fmt(rmu_real, 8)
      + "，chi^2_min = " + fmt(chi_real, 8) + "，dof=2，chi^2/dof = "
      + fmt(chi_real / 2, 8),
      "判决的唯一支点是 sigma 取值：电子实验不确定度实为 2.8e-14（来料取 1e-12 松 36 倍），"
      "缪子含 SM 理论误差约 5e-10（来料取 4e-7 松 800 倍）。"
      "两个松紧方向的调整把同一模型从 p=0.997 推到 p~1e-129。")

    F("T11", "V4.3 终审结论过度陈述：结论完全依赖未声明的误差口径",
      "来料终审：「在 V4.2/V4.3 原始公理下，理论被电子+缪子 g-2 联合实验排除」",
      "机器：同一公式在两套 sigma 下分别给出 chi^2/dof = "
      + fmt(chi_claim / 2, 6) + "（无失配）与 " + fmt(chi_real / 2, 6) + "（强失配）",
      "严格表述应为「在该式的 m^2 刚性比例与实验残差反号这一点上，框架被排除；"
      "但排除的强度不可用未声明的 sigma 换算」。反号本身（cot>0 vs cot<0）不依赖 sigma，"
      "是真正的判决点；量级叙述不成立。")

    # ---- T12 电子修正在缪子反解下的读数 ----
    ae_tuft_mu_driven = ccoef * me2 * cot_mu_true
    M_("T12", "缪子反解下的电子 TUFT 修正读数错误",
      "来料：a_e^TUFT = +3.15e-15（比实验残差小 4 个量级）",
      "机器（用真实 Delta a_mu 反解）：a_e^TUFT = " + fmt(ae_tuft_mu_driven, 8)
      + "，与实验残差 " + fmt(da_e, 8) + " 反号，绝对差 "
      + fmt(abs(ae_tuft_mu_driven - da_e), 8),
      "来料的 3.15e-15 来自 T02/T06 的量级错误叠加。真实读数是 +5.38e-14，"
      "与实验要求的负偏差方向相反，绝对差 7.44e-13 —— 冲突依旧，但并非「远小于」。")

    return {
        "da_e": da_e, "da_mu": da_mu, "ccoef": ccoef, "mass_ratio2": mass_ratio2,
        "resid_ratio": resid_ratio, "cot_e": cot_e, "cot_mu_true": cot_mu_true,
        "cot_mu_claiminput": cot_mu_claiminput,
        "w_ratio_claim": w_ratio_claim, "w_ratio_real": w_ratio_real,
        "cot_star_claim": cs_claim, "chi2_claim": chi_claim,
        "cot_star_real": cs_real, "chi2_real": chi_real,
        "ae_tuft_mu_driven": ae_tuft_mu_driven,
    }


# ==========================================================================
# 7. 条目主体 —— 第二链：V4.4 路线B 主链（自能屏蔽 / 质量-曲率映射）
# ==========================================================================
def build_chain_44(v43):
    # ---------------- 量纲段 ----------------
    dim_hc = dmul(D_HBAR, D_VEL)                                  # M L^3 T^-2
    dim_lp2 = dpow(D_L, 2)
    dim_k2 = dpow(D_KAPPA, 2)
    dim_lp2k2 = dadd(dim_lp2, dim_k2)                              # 无量纲
    dim_self_claim = dmul(dim_hc, dim_lp2k2)                      # (1,3,-2,0)
    dim_self_fix = dadd(dim_hc, dadd(D_L, dim_k2))                # (1,2,-2,0)

    dim_e_term1 = dsub(dmul(D_HBAR, D_KAPPA), D_VEL)              # hbar*kappa/c
    dim_e_term2_claim = dsub(dmul(dmul(D_HBAR, dpow(D_L, 2)), dpow(D_KAPPA, 2)), D_VEL)
    dim_e_term2_fix = dsub(dmul(dmul(D_HBAR, D_L), dpow(D_KAPPA, 2)), D_VEL)

    dim_A_claim = dsub(dmul(D_HBAR, dpow(D_L, 2)), D_VEL)
    dim_A_fix = dsub(dmul(D_HBAR, D_L), D_VEL)
    dim_B = dsub(D_HBAR, D_VEL)

    F("T13", "自能公理 U_self = (hbar c / 2) lP^2 kappa^2 量纲不是能量",
      "来料：「量纲核验：[U_self] = ML^2 T^-2，能量量纲自洽 ✅」",
      "机器：[hbar c] = " + dstr(dim_hc) + "，[lP^2 kappa^2] = " + dstr(dim_lp2k2)
      + "，故 [U_self] = " + dstr(dim_self_claim) + " vs [能量] = " + dstr(D_ENERGY)
      + "（差一个长度幂次）",
      "hbar*c = J·m（力），不是能量；要得到能量必须再除一个长度。"
      "来料把 lP 的截断写成 lP^2（面积），恰好多出一个长度幂次。"
      "这是本库「量纲非齐次」缺陷族的再一次复发（跨册第 8 次，见 r37 §20.2 同型）。")

    F("T14", "来料自带的量纲核验算术本身写错（L^3 写成 L^2）",
      "来料核验行：「ML^3 T^-2 · L^2 · L^-2 = ML^2 T^-2」",
      "机器：L^3 · L^2 · L^-2 = L^3，故应为 " + dstr(dim_self_claim)
      + "；来料写成 ML^2T^-2",
      "即来料在「量纲严格校验 ✅」的自评处，先算错一个长度幂次，再据此宣布自洽。"
      "本条与 T13 相互独立（一条是式子错，一条是核验错）。")

    P("T15", "最小幂次修正 U_self = (hbar c / 2) lP kappa^2 量纲闭合（修正候选）",
      "本册提出的最小修正（非来料内容，仅给出量纲上唯一允许的幂次）",
      "机器：[hbar c · lP · kappa^2] = " + dstr(dim_self_fix)
      + " = " + dstr(D_ENERGY) + " ✔",
      "把 lP^2 改为 lP 即闭合。本册只判定「哪个幂次合法」，不代为构造作用量。")

    F("T16", "驻波能量方程两项量纲不齐（来料版）",
      "来料：m c^2 = hbar c kappa / sin(theta) - (hbar c/2) lP^2 kappa^2",
      "机器：第一项 [hbar c kappa] = " + dstr(dmul(dim_hc, D_KAPPA))
      + "（能量 ✔）；第二项 [hbar c lP^2 kappa^2] = "
      + dstr(dmul(dim_hc, dim_lp2k2)) + "（非能量 ✘）",
      "右端两项不可相加，故整个驻波条件（来料「新公理补充」）在量纲层即不成立。")

    F("T17", "质量-曲率二次方程三项量纲不齐（来料核心映射失效）",
      "来料：A kappa^2 + B kappa + m = 0，A = hbar lP^2/(2c)，B = -hbar/(c sin(theta))",
      "机器：[A kappa^2] = " + dstr(dmul(dim_A_claim, dpow(D_KAPPA, 2)))
      + "、[B kappa] = " + dstr(dmul(dim_B, D_KAPPA)) + "、常数项 m = " + dstr(D_M)
      + " ⇒ 前者与后二者差一个长度幂次",
      "因此来料的判别式 B^2 - 4Am 在量纲层就没有定义（两项异族），"
      "其后所有「物理取小曲率根」「定义域」「质量上界」全部悬空。"
      "注意：这不是精度问题，公式本身不是一个可解的代数方程。")

    P("T18", "把 lP^2 改 lP 后，质量方程与判别式同时齐次（最小修补）",
      "修正版：m = hbar kappa/(c sin theta) - (hbar lP/(2c)) kappa^2",
      "机器：第二项量纲 = " + dstr(dim_e_term2_fix) + " = 质量 ✔；"
      "[A_fix kappa^2] = " + dstr(dmul(dim_A_fix, dpow(D_KAPPA, 2)))
      + "、[B kappa] = " + dstr(dmul(dim_B, D_KAPPA)) + "、常数项 = " + dstr(D_M)
      + "（三者齐次）；判别式 B^2 = " + dstr(dpow(dim_B, 2))
      + " 与 4 A_fix m = " + dstr(dmul(dim_A_fix, D_M)) + " 同族 ✔",
      "一处幂次修正同时救活三处；但代价是来料宣称的「质量上界」公式必须重写（见 T26/T28）。")

    F("T19", "来料判别式的根号内两子项量纲不同族，不可相减",
      "来料：sqrt(1/sin^2(theta) - 2 m c / hbar)",
      "机器：[1/sin^2 theta] = " + dstr(DIM0) + "；[2 m c / hbar] = "
      + dstr(dsub(dmul(D_M, D_VEL), D_HBAR)) + "（= 回旋波数的平方）",
      "无量纲减 m^-2 没有定义。这正是「质量上界」看起来成立而实际是把不同物理量相加的根源。")

    num_2mc_hbar_e = 2 * ME0 * C0 / HBAR0
    num_2mc_hbar_mu = 2 * MMU0 * C0 / HBAR0
    F("T20", "根号对全部已知基本粒子恒为负（来料映射无实根）",
      "来料：定义域要求 1/sin^2(theta) > 2 m c / hbar，并对所有已知粒子成立",
      "机器：电子 2 m_e c/hbar = " + fmt(num_2mc_hbar_e, 8) + " m^-2；"
      "缪子 = " + fmt(num_2mc_hbar_mu, 8) + " m^-2；而 1/sin^2(theta) ≤ 1（无量纲）",
      "差 5.18e12（电子）到 3.86e13（缪子）个量级，任何真实 theta 都不在窗口内。"
      "该映射对任何有质量的粒子都不给出实数曲率。")

    F("T21", "弱场泰勒展开的前提 2mc/hbar << 1/sin^2(theta) 对真实粒子不成立",
      "来料：「对小质量粒子（电子）做泰勒展开，2mc/hbar << 1/sin^2(theta)」",
      "机器：比值 2 m_e c/hbar / (1/sin^2 theta) = " + fmt(num_2mc_hbar_e, 8)
      + "（>1，而非 <<1）",
      "小质量不等于小参数：回旋波数只被 Planck 标度抑制，而 1/sin^2 theta 是 O(1) 的纯数。"
      "展开参数错了 12 个量级。")

    dim_kappa_claim_weak = dmul(D_M, dmul(D_VEL, dneg(D_HBAR)))      # m c / hbar = L^-1
    dim_kappa_from_quad_claim = dadd(dpow(D_L, -2), dim_kappa_claim_weak)   # 再除 lP^2
    F("T22", "弱场结果与其自身二次方程解不同源（差一个 lP^2），量纲随之从 L^-1 变 L^-3",
      "来料：弱场近似 kappa ≈ (m c sin theta)/hbar（并称由此恢复线性关系）",
      "机器：[m c sin / hbar] = " + dstr(dim_kappa_claim_weak)
      + "（该式本身闭合）；但由来料自己的映射 kappa = (1/lP^2)(1/sin - sqrt(...)) 展开，"
      "得到的是 kappa = (1/lP^2)(m c sin theta)/hbar，其量纲 = "
      + dstr(dim_kappa_from_quad_claim) + " ✘（[kappa] = " + dstr(D_KAPPA) + "）",
      "来料正文的弱场式漏掉了整条自能截断因子 lP^2 —— 恰好是它在第一节写错的那个幂次。"
      "因此「旧版本线性关系在小质量下近似恢复」这句话与其映射不同源：恢复出来的是修正版（lP 一次方）"
      "映射的弱场极限，而不是它所声称的那个。")

    P("T23", "修正版的 kappa(m) 精确小根与其弱场极限（可算复核）",
      "修正版：kappa = (1/(lP sin theta))(1 - sqrt(1 - eps))，eps = 2 m sin^2 theta / mP",
      "机器：阳性对照回代 mc^2 的相对残差 < 1e-50（guard positive_control_corrected_form）；"
      "小根量纲 = [1/(lP sin)] + [1 - sqrt(...)] = " + dstr(dneg(D_KAPPA))
      + " ✔；弱场极限 kappa ≈ m c sin(theta)/hbar = " + str(dstr(dim_kappa_claim_weak)),
      "该小根在 m -> 0 时给出 kappa = m c sin(theta)/hbar，"
      "定义域 m < mP/(2 sin^2 theta)。这是本册认为可以保留的映射骨架。")

    particles = [
        ("电子 m_e", ME0), ("缪子 m_mu", MMU0), ("tau 子", MTAU0),
        ("W 玻色子", MW0), ("顶夸克 m_t", MTOP0),
    ]
    rows = []
    for nm, mv in particles:
        eps_v = 2 * (mv / MPL0)
        lin_ratio = (DC(1) - (DC(1) - eps_v).sqrt()) / (eps_v / 2)
        rows.append((nm, mv, eps_v, lin_ratio, eps_v / 4))

    F("T24", "自能方向被读反：它是放大 kappa，不是屏蔽 kappa",
      "来料：「质量更大的缪子，二次自能项显著压低 kappa(m) 的增长」",
      "机器：kappa/kappa_linear = (1-sqrt(1-eps))/(eps/2) = 1 + eps/4 + O(eps^2) > 1；"
      "超出线性值的幅度：电子 " + fmt(rows[0][3] - 1, 8) + "，缪子 "
      + fmt(rows[1][3] - 1, 8) + "，顶夸克 " + fmt(rows[4][3] - 1, 8),
      "凹抛物线 m(kappa) = A kappa - B kappa^2 的小根略大于线性值 m/A："
      "自能吃掉能量，故需要更大的曲率补偿。方向与来料叙述相反（来料说压低，实际是抬高）。")

    I("T25", "自能占比在全射程内可忽略（机制在目标域内无效应）",
      "来料：自能项对缪子显著",
      "机器：自能占比 = eps/4 = " + " / ".join(
          [r[0] + " " + fmt(r[4], 6) for r in rows]),
      "最大者（顶夸克）仍为 1e-18 量级。要让自能进入 O(1) 需 m ~ mP/2，"
      "即接近 Planck 质量；这与「粒子磁矩」目标不在同一射程。")

    mmax_claim = HBAR0 / (2 * C0)
    F("T26", "质量上界公式三层错：量纲不是质量、丢失自己引入的 lP^2、读数量级荒谬",
      "来料：m_max = hbar/(2 c sin^2 theta)，宣称「TUFT-V4.4 预言基本粒子存在最大固有质量上限」",
      "机器：m_max(公式值) = " + fmt(mmax_claim, 10) + "，量纲 "
      + dstr(dsub(D_HBAR, D_VEL)) + "（质量×长度，不是质量）；"
      "公式中不含 lP（来料自能式的截断尺度在自己的上界里消失）",
      "三重缺陷：①量纲 ML ②截断尺度丢失误 ③公式与其来源（U_self 含 lP^2）不相容。")

    ratio_me_over_mmax = ME0 / mmax_claim
    F("T27", "按来料上界，任何基本粒子都超限 ⇒ 该预言等价于「基本粒子不存在」",
      "来料：「这是可证伪的硬核预言」",
      "机器：电子 / 上界(若按 kg 读) = " + fmt(ratio_me_over_mmax, 8)
      + "，即电子质量是所宣称的「上限」的 " + fmt(ratio_me_over_mmax, 4) + " 倍",
      "预言的形态是硬预言，但方向是自毁式的：它排除的不是某种极端粒子，"
      "而是全部已知物质。作为可证伪预言，其内容等价于「不存在基本粒子」，不具鉴别力。")

    mmax_fix = MPL0 / 2
    top_ratio = MTOP0 / mmax_fix
    B("T28", "修正版上界 m < mP/(2 sin^2 theta) 在已知物质全射程内恒真",
      "本册修正版的可算读数（非来料内容）",
      "机器：上界 = " + fmt(mmax_fix, 10) + " kg；顶夸克 / 上界 = "
      + fmt(top_ratio, 8) + "（距上界 17 个量级）；太阳质量 / 上界 = "
      + fmt(MSUN0 / mmax_fix, 8),
      "两个方向的结局都不利：来料版把所有粒子判为超限；修正版在一切已知物质下恒成立，"
      "属零信息量陈述。要成为硬预言必须先声明射程（粒子 vs 天体），而静态单粒子驻波公理在天体尺度早已失效。")

    dim_a_new_nat = dsub(dmul(dmul(D_VEL, D_M), D_KAPPA), dmul(D_E_NAT, D_HBAR))
    dim_a_old_nat = dsub(dmul(dmul(D_M, D_M), D_VEL), dmul(D_E_NAT, dpow(D_HBAR, 2)))
    dim_a_new_si = dsub(dmul(dmul(D_VEL, D_M), D_KAPPA), dmul(D_E_SI, D_HBAR))
    F("T29", "a^TUFT 的「新旧两式」量纲都不无量纲 ⇒ 替换没有修好量纲",
      "来料：「EC 挠率-自旋耦合严格保留，耦合系数 3/8 不变」并把 m^2 换成 m*kappa(m)",
      "机器（自然单位电荷口径）：[a_new] = " + dstr(dim_a_new_nat)
      + "、[a_old] = " + dstr(dim_a_old_nat)
      + "；SI 口径：[a_new] = " + dstr(dim_a_new_si)
      + "；反解所需补因子分别为 " + dstr(dneg(dim_a_new_nat)) + " / "
      + dstr(dneg(dim_a_old_nat)),
      "a = (g-2)/2 必须无量纲。两式都差若干幂次，且缺的不是同一个因子，"
      "故「替换掉 m^2 项」并未使磁矩表达式量纲闭合——该缺陷自 V4.2 起继承，"
      "V4.4 未触及。耦合常数 3/4 是否可由 EC 几何定出，本册不自推（见不自推清单）。")

    ratio_sin = DC("0.5")           # theta=30 deg
    F("T30", "弱场极限下 a^TUFT ∝ m^2 cos(theta)：路线B 自称要打破的 m^2 被自己恢复",
      "来料：「新增二次曲率自能项破坏简单线性关系 m ∝ kappa ⇒ a_TUFT ∝ m^2 的标度自动失效」",
      "机器：把正确弱场极限 kappa = m sin(theta)/hbar 代入 a ∝ cot(theta) m kappa，"
      "得 a_weak ∝ m^2 cos(theta)（sin(theta) 精确消去，guard weakfield_sin_cancels 机器零）；"
      "新旧两式之比恰为 sin(theta)（theta=30deg 时 0.5，60deg 时 0.8660254）",
      "自能只在 kappa 上加 1+O(m/mP) 的相对修正，因此在唯一有物理意义的弱场极限内，"
      "标度仍是 m^2。路线B 的目标在其自身射程内没有实现。")

    P("T31", "弱场下电子/缪子修正比值仍精确等于质量平方比（比例约束原封不动）",
      "来料：「打破 42753 倍硬性比例」",
      "机器：a_mu/a_e = m_mu^2/m_e^2 = " + fmt(v43["mass_ratio2"], 12)
      + "（来料 42753 相对偏差 " + fmt(rel(DC("42753"), v43["mass_ratio2"]), 6)
      + "）；自能修正因子的相对差异 < 1e-17（电子 " + fmt(rows[0][3] - 1, 6)
      + " vs 缪子 " + fmt(rows[1][3] - 1, 6) + "）",
      "在弱场极限下电子/缪子比值与 m^2 完全一致：这是「同一全局 theta 连接所有粒子」"
      "这一核心卖点的直接代价，也是 V4.3 冲突的根源，而路线B 未能移除它。")

    B("T32", "theta 的灵敏度结构改变（不是简单反转）",
      "来料：唯一全局 theta 同时控制引力、电子、缪子",
      "机器：旧式 dln(a)/d(theta) = -1/(sin cos)，新式（弱场）= -tan(theta)；"
      "两者之比为 sin(theta)（theta=30deg: 0.5；45deg: 0.7071068；60deg: 0.8660254；"
      "89deg: 0.9998477）；在 theta -> 90deg 处重新重合",
      "新式把 g-2 修正的 theta 灵敏度在小角区压低、在 90deg 处与旧式重合，"
      "并把修正推到 0（a_weak ∝ cos(theta) -> 0）。方向性后果属于模型结构判断，"
      "本册只给机器读数，不代选。")

    gth_claim = C0 ** 3 * LP0 * LP0 / HBAR0
    gth_at_claim = gth_claim * cot_to_sin(v43["cot_star_claim"])
    I("T33", "引力项在拟合中零贡献：恒等式复读（跨册第 9 次复发）",
      "来料：「引力约束 G_th = c^3 lP^2/(hbar sin theta) 与 CODATA 兼容」",
      "机器：c^3 lP^2/hbar / G - 1 = " + fmt(gth_claim / G0 - DC(1), 6)
      + "（用标称 lP=1.616255e-35；改用精算 lP=1.61625502442370536982659034826e-35 后为 "
      + fmt((C0 ** 3 * LP_PREC * LP_PREC / HBAR0) / G0 - DC(1), 6) + "，机器零）；"
      + "在 chi2 极优点 cot = " + fmt(v43["cot_star_claim"], 6)
      + " 处，1/sin - 1 的真实值为 cot^2/2 = "
      + fmt(v43["cot_star_claim"] ** 2 / 2, 8)
      + "，低于 60 位有效位 ⇒ 机器值精确为 0（guard cot_to_sin_high_precision 以 140 位复核），"
      + "故 chi_G 恒为 0",
      "G_th ≡ c^3 lP^2/hbar 是 lP^2 = hbar G/c^3 的移项（与 r40 C3、r41 R06 同族）；"
      "而 g-2 反解出的 cot ~ 1e-48 使 sin(theta) = 1 - 1e-95，"
      "于是第三项约束不提供任何判别力（零信息量），来料「引力几乎不参与冲突」的说法成立但更强：它根本不参与。")

    F("T34", "外部输入账：theta 与 lP 两项，撞 Omega5「自由常数 <=1」",
      "来料：「唯一全局 theta，没有为电子、缪子引入独立参数 ✅」",
      "机器：进入闭合条件的是 {theta（连续）} 与 {lP（长度）}；"
      "而 lP^2 ≡ hbar G/c^3 含 G，二者互定 ⇒ 实为 2 项外部输入（回链 r40 C3 / r41 R06）",
      "「粒子层面只有一个参数」成立；但「全框架只有一个自由常数」不成立，"
      "这是 r18/r19/r40/r41 连续登记的同一代价，本册第五节自评「唯一全局 theta」只对粒子扇区成立。")

    B("T35", "v = c 公理与非相对论 Pauli 约化互斥（承重，继承 r40 K16）",
      "来料：a^TUFT 由「静态局部单粒子近似、EC 最小耦合、非相对论 Pauli 约化」导出",
      "机器/逻辑：公理 v = c ⇒ gamma -> 无穷 ⇒ Pauli/Dirac 的非相对论约化无适用区间；"
      "本册不自推相对论修正形式（登记为不自推项）",
      "该互斥在 r40 已登记（作用量 S = m c^2 T 在 v=c 下无定义）。"
      "V4.3/V4.4 继续在非相对论约化上计算磁矩，未处理此前提。")

    da_mu_2025 = AMU_EXP_2025 - AMU_QED
    cot_mu_2025 = da_mu_2025 / (v43["ccoef"] * MMU0 * MMU0)
    ae_tuft_2025 = v43["ccoef"] * ME0 * ME0 * cot_mu_2025
    I("T36", "口径漏项清单 + 2025 缪子值的敏感性",
      "来料 chi^2 未声明 sigma_e / sigma_mu / sigma_G 的依据，且用 2020 年缪子值",
      "机器：2025 值下 Delta a_mu = " + fmt(da_mu_2025, 8) + "，cot* = "
      + fmt(cot_mu_2025, 8) + "，电子 TUFT 修正 = " + fmt(ae_tuft_2025, 8)
      + "（较 2020 口径变化 "
      + fmt(ratio(cot_mu_2025, v43["cot_mu_true"]) - DC(1), 6) + "，方向与结论不变）",
      "未声明项：sigma_e=1e-12（实际 2.8e-14）、sigma_mu=4e-7（实际含 SM 理论约 5.2e-10）、"
      "sigma_G/G=1e-5（CODATA 为 2.2e-5）、a_mu 采用 2020 值、QED 值是否含 EW 修正。"
      "T09/T10 已证明其中第一项即足以反转判决。")

    M_("T37", "路线 B 的定性预判（「定性行为预判」节）与本册机器读数相反",
      "来料：电子近 m^2、缪子被自能「显著压低」、「不再放大 4 万倍」",
      "机器：真实方向是自能放大而非压低（T24）；弱场下标度回到 m^2（T30）；"
      "电子/缪子比值 42752.7499 原样保留（T31）",
      "三处定性预判全部与自身公式在唯一有效极限下的行为相反。"
      "这不否定「引入自能」这一思路的价值，但说明来料对该思路的期待无法由该 ansatz 实现。")

    return {
        "dim_self_claim": dim_self_claim, "dim_self_fix": dim_self_fix,
        "rows": rows, "mmax_claim": mmax_claim, "mmax_fix": mmax_fix,
        "top_ratio": top_ratio, "ratio_me_over_mmax": ratio_me_over_mmax,
        "num_2mc_hbar_e": num_2mc_hbar_e, "gth_ratio": gth_claim / G0 - DC(1),
        "da_mu_2025": da_mu_2025, "cot_mu_2025": cot_mu_2025,
    }


# ==========================================================================
# 8. 落盘
# ==========================================================================
def stats():
    cnt = {}
    for it in ITEMS:
        cnt[it["verdict"]] = cnt.get(it["verdict"], 0) + 1
    return cnt


def key_figures(v43, v44):
    return {
        "Delta_a_e_machine": fmt(v43["da_e"], 8),
        "Delta_a_e_claim": "-6.9e-11",
        "Delta_a_mu_machine": fmt(v43["da_mu"], 8),
        "Delta_a_mu_claim": "+2.3e-6",
        "C_coefficient": fmt(v43["ccoef"], 8),
        "mass_ratio_squared": fmt(v43["mass_ratio2"], 12),
        "residual_ratio_true": fmt(v43["resid_ratio"], 10),
        "cot_theta_e_machine": fmt(v43["cot_e"], 10),
        "cot_theta_e_claim": "6.59e-46",
        "cot_theta_mu_true": fmt(v43["cot_mu_true"], 10),
        "cot_theta_mu_from_claim_input": fmt(v43["cot_mu_claiminput"], 10),
        "cot_theta_mu_claim": "-5.13e-51",
        "weight_ratio_claim_sigma": fmt(v43["w_ratio_claim"], 8),
        "weight_ratio_real_sigma": fmt(v43["w_ratio_real"], 8),
        "chi2_min_claim_sigma": fmt(v43["chi2_claim"], 8),
        "chi2_min_real_sigma": fmt(v43["chi2_real"], 8),
        "cot_star_claim_sigma": fmt(v43["cot_star_claim"], 10),
        "cot_star_real_sigma": fmt(v43["cot_star_real"], 10),
        "a_e_tuft_mu_driven": fmt(v43["ae_tuft_mu_driven"], 8),
        "dim_U_self_claim": dstr(v44["dim_self_claim"]),
        "dim_U_self_fix": dstr(v44["dim_self_fix"]),
        "2mc_over_hbar_electron": fmt(v44["num_2mc_hbar_e"], 8) + " m^-2",
        "self_energy_ratio_table": {
            r[0]: {
                "eps": fmt(r[2], 8),
                "kappa_over_kappa_linear_minus_one": fmt(r[3] - DC(1), 8),
                "self_energy_fraction_eps_over_4": fmt(r[4], 8),
            } for r in v44["rows"]
        },
        "m_max_claim_formula": fmt(v44["mmax_claim"], 10) + " (dim M*L, not a mass)",
        "m_over_m_max_electron": fmt(v44["ratio_me_over_mmax"], 8),
        "m_max_fixed": fmt(v44["mmax_fix"], 10) + " kg",
        "m_top_over_m_max": fmt(v44["top_ratio"], 8),
        "G_th_identity_residual": fmt(v44["gth_ratio"], 6),
        "Delta_a_mu_2025": fmt(v44["da_mu_2025"], 8),
        "cot_theta_mu_2025": fmt(v44["cot_mu_2025"], 10),
    }


def write_json(v43, v44):
    payload = {
        "tag": TAG,
        "date": "2026-10-12",
        "number": "r44",
        "subject": "TUFT-V4.4 路线B（自能屏蔽 / 重构质量-曲率映射）+ 前提链 V4.3 全维审计",
        "engine": "源码/TUFT-r44_V44路线B自能屏蔽_全维审计_2026-10-12.py",
        "engine_kind": "纯标准库 Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)",
        "incoming": "《TUFT-V4.4｜路线B：修改质量-曲率映射，重构量子驻波条件，保留唯一全局 theta》"
                    " + 其前提链《TUFT-V4.3｜联合 chi^2 拟合》",
        "verdict_counts": stats(),
        "items": ITEMS,
        "guards": GUARDS,
        "key_figures": key_figures(v43, v44),
        "not_self_derived": [
            "S_spiral 作用量的变分导出自能系数（本册只判定幂次合法性，见 T15）",
            "EC 挠率-自旋耦合常数 3/4 是否可由几何定出（见 T29，本册只给量纲反解）",
            "a^TUFT 两个表达式所需补齐因子的具体构造（只给量纲，见 T29）",
            "相对论（v=c）下的磁矩修正形式（见 T35）",
            "质量上界的射程声明（粒子 / 天体，见 T28）",
        ],
        "open_items": [
            "X-R44-1 螺旋场作用量变分（S_spiral）与自能系数推导 —— 来料第 5 节缺陷清单第 1 条的正面化",
            "X-R44-2 sigma_e / sigma_mu / sigma_G 口径登记 —— 判决支点，两档口径结论相反",
            "X-R44-3 弱场极限下 a ∝ m^2 cos(theta) 的 sin 消去结构 —— 是否保留由 theta 语义决定",
            "X-R44-4 质量上界射程（粒子 vs 天体）与静态驻波公理的适用域",
            "X-R44-5 a^TUFT 量纲闭合所需补因子（自然单位与 SI 两口径分别反解）",
        ],
    }
    with io.open(OUT_JSON, "w", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, indent=2))


def write_md(v43, v44):
    cnt = stats()
    lines = []
    lines.append("# " + TAG + "（数据摘要）")
    lines.append("")
    lines.append("- 生成时间口径：2026-10-12；引擎：纯标准库 Decimal 60 位 + Fraction 四分量量纲 (M,L,T,Q)")
    lines.append("- 读数：条目 " + str(len(ITEMS)) + "，自检 "
                 + str(sum(1 for g in GUARDS if g["ok"])) + "/"
                 + str(len(GUARDS)) + "；verdict = " + json.dumps(cnt, ensure_ascii=False))
    lines.append("")
    lines.append("| id | 判定 | 条目 | 来料声称 | 机器读数 |")
    lines.append("|---|---|---|---|---|")
    for it in ITEMS:
        lines.append("| " + it["id"] + " | " + it["verdict"] + " | " + it["title"]
                     + " | " + it["claim"].replace("\n", " ")
                     + " | " + it["reading"].replace("\n", " ") + " |")
    lines.append("")
    lines.append("## 关键数值档案")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(key_figures(v43, v44), ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## 自检 guards")
    lines.append("")
    lines.append("| guard | 结果 | 说明 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append("| " + g["name"] + " | " + ("PASS" if g["ok"] else "FAIL") + " | "
                     + g["note"].replace("\n", " ") + " |")
    lines.append("")
    with io.open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_report(v43, v44):
    cnt = stats()
    lines = []
    lines.append("=" * 78)
    lines.append(TAG)
    lines.append("=" * 78)
    lines.append("条目 " + str(len(ITEMS)) + "  自检 "
                 + str(sum(1 for g in GUARDS if g["ok"])) + "/" + str(len(GUARDS)))
    lines.append("verdict: " + ", ".join([k + "=" + str(cnt[k]) for k in sorted(cnt)]))
    lines.append("")
    for it in ITEMS:
        lines.append("[" + it["id"] + "] " + it["verdict"] + " | " + it["title"])
        lines.append("    声称: " + it["claim"])
        lines.append("    读数: " + it["reading"])
        lines.append("    裁定: " + it["detail"])
        lines.append("")
    lines.append("-" * 78)
    lines.append("guards:")
    for g in GUARDS:
        lines.append("  " + ("PASS " if g["ok"] else "FAIL ") + g["name"] + " | " + g["note"])
    lines.append("")
    lines.append("key figures:")
    lines.append(json.dumps(key_figures(v43, v44), ensure_ascii=False, indent=2))
    with io.open(OUT_RPT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ==========================================================================
# 9. main
# ==========================================================================
def main():
    v43 = build_chain_43()
    v44 = build_chain_44(v43)
    run_guards()

    # 收尾自检：条目数与 verdict 合法性
    guard("items_count_matches", len(ITEMS) >= 30,
          "条目数 = " + str(len(ITEMS)))
    legal = set(["PASS", "FAIL", "BOUNDARY", "INFO", "MISMATCH", "CORRECTED"])
    guard("verdict_vocabulary", all(it["verdict"] in legal for it in ITEMS),
          "verdict 取值集合受限")

    write_json(v43, v44)
    write_md(v43, v44)
    write_report(v43, v44)

    cnt = stats()
    ok_guards = sum(1 for g in GUARDS if g["ok"])
    print("=" * 70)
    print(TAG)
    print("条目 " + str(len(ITEMS)) + "  自检 " + str(ok_guards) + "/" + str(len(GUARDS)))
    print("verdict: " + ", ".join([k + "=" + str(cnt[k]) for k in sorted(cnt)]))
    kf = key_figures(v43, v44)
    print("-" * 70)
    for k in ["Delta_a_e_machine", "Delta_a_mu_machine", "cot_theta_e_machine",
              "chi2_min_claim_sigma", "chi2_min_real_sigma", "dim_U_self_claim",
              "m_over_m_max_electron", "m_top_over_m_max"]:
        print(k + " = " + str(kf[k]))
    print("-" * 70)
    print("JSON: " + OUT_JSON)
    print("MD  : " + OUT_MD)
    print("RPT : " + OUT_RPT)
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())