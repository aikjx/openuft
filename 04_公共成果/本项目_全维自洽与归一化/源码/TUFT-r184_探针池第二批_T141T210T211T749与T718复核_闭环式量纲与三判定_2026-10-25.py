# -*- coding: utf-8 -*-
"""
TUFT-r184 · 探针池第二批（T141 / T210+T211 / T749）闭环式 + T718 附带复核 · 精算
2026-10-25

承接：
  r183（探针池第一批）F06 已修正批次账：第二批真实新工作量 = T141 / T210(+T211) / T749。
  r183 C04 已登记 archive T718 的 G0 数值不符，承诺「纳入第二批复核」。

本册职责：
  1) 对第二批三组探针给出闭环式、量纲、数值表、结构诊断与三判定（C1/C2/C3）。
  2) 对 T718 的 archive G0 做复核并定性（位数搬迁 / 单位误用）。
  3) 登记本批新发现的缺陷族：F-unit（互为倒数的单位间搬位数）、F-dim-blind（把有量纲量当纯数）、
     F-label（T 编号↔公式映射在 README 与判定册之间倒置）。

三判定口径（继承 r183，可执行）：
  C1 无约束（退化）：探针不触及 TUFT 的可动自由度（TUFT 侧供给=0）⇒ 零信息量。
  C2 力约束放行    ：TUFT 侧有数值且落在探针区间内 ⇒ 仅「一致」，不得作证明。
  C3 力约束否定    ：TUFT 侧有数值且越出探针上界 ⇒ 该自由度被压缩/排除（仍不否定公理集本体）。

纪律：探针供给恒为 0 时不得报道为「通过」；恒等式必须标注「口径交叉印证、非独立验证」；
      不自推的系数一律 BOUNDARY。红线：不产生新物理、不改写来料字节、不改 verify.py。
"""
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 250

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                     # 04_公共成果/本项目_全维自洽与归一化
OUTD = os.path.join(BASE, "数据")
if not os.path.isdir(OUTD):
    os.makedirs(OUTD)

STEM = "TUFT-r184_探针池第二批_T141T210T211T749与T718复核_闭环式量纲与三判定_2026-10-25"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal

ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def control(name, ok, msg=""):
    ok = bool(ok)
    CONTROLS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [CONTROL-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


# =====================================================================
# 0. 量纲机器（五元组 M, L, T, Q, K；K = 温度）
# =====================================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = int(n)
    return tuple(x * n for x in a)


def dsqrt(a):
    return tuple(x / 2 for x in a)


def dstr(a):
    names = ("M", "L", "T", "Q", "K")
    parts = []
    for nm, ex in zip(names, a):
        if ex == 0:
            continue
        if ex == 1:
            parts.append(nm)
        elif ex.denominator == 1:
            parts.append("%s^%d" % (nm, ex.numerator))
        else:
            parts.append("%s^%s" % (nm, ex))
    return " ".join(parts) if parts else "1"


F0 = Fraction(0)
F1 = Fraction(1)
ONE = (F0, F0, F0, F0, F0)
MSS = (F1, F0, F0, F0, F0)
LEN = (F0, F1, F0, F0, F0)
TIM = (F0, F0, F1, F0, F0)
CHG = (F0, F0, F0, F1, F0)
TMP = (F0, F0, F0, F0, F1)

DIM = {
    "c":     (F0, F1, Fraction(-1), F0, F0),
    "G":     (Fraction(-1), Fraction(3), Fraction(-2), F0, F0),
    "hbar":  (F1, Fraction(2), Fraction(-1), F0, F0),
    "h":     (F1, Fraction(2), Fraction(-1), F0, F0),
    "kB":    (F1, Fraction(2), Fraction(-2), F0, Fraction(-1)),
    "e":     (F0, F0, F0, F1, F0),
    "eps0":  (Fraction(-1), Fraction(-3), Fraction(2), Fraction(2), F0),
    "mu0":   (F1, F1, F0, Fraction(-2), F0),
    "me":    (F1, F0, F0, F0, F0),
    "kg":    (F1, F0, F0, F0, F0),
    "W":     (F1, Fraction(2), Fraction(-3), F0, F0),
    "J":     (F1, Fraction(2), Fraction(-2), F0, F0),
    "Ohm":   (F1, Fraction(2), Fraction(-1), Fraction(-2), F0),
    "Siem":  (Fraction(-1), Fraction(-2), F1, Fraction(2), F0),
    "Entropy": (F1, Fraction(2), Fraction(-2), F0, Fraction(-1)),
    "B":     (F1, F0, Fraction(-1), Fraction(-1), F0),
    "strain": ONE,
}

# ---- 数值常数（CODATA 2018/2022 字面值，单一 250 位口径）----
PI_STR = ("3."
          "14159265358979323846264338327950288419716939937510"
          "58209749445923078164062862089986280348253421170679"
          "82148086513282306647093844609550582231725359408128"
          "48111745028410270193852110555964462294895493038196")
PI = D(PI_STR)
CV = D("299792458")
HV = D("6.62607015E-34")
HBARV = HV / (D(2) * PI)
KBV = D("1.380649E-23")
EV = D("1.602176634E-19")
GV = D("6.67430E-11")
MEV = D("9.1093837015E-31")
MSUN = D("1.98847E30")             # IAU 2015 名义太阳质量（与 CODATA-2018 G 同口径）

VERDICT = ("R184-PROBE-BATCH2-4-OF-4-C1-SUPPLY-0-4-EXTRA-T718-C1-"
           "T141-EPS-DIMLESS-CRAB-1.837928E-4-OMEGA-K-IDENTITY-"
           "T210T211-AREA-1.048955E77-LOG-MINUS-266.0203-REL-2.536E-75-BEKENSTEIN-SATURATED-"
           "T749-PRODUCT-6-MASSSHELL-EXACT-DIMENSION-BLIND-S-"
           "T718-ARCHIVE-33.37PCT-LOW-EQUALS-RK-TIMES-1E-9-LABEL-INVERSION")


def main():
    print("=" * 78)
    print("TUFT-r184 · 探针池第二批 T141/T210+T211/T749 · T718 附带复核")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲机器自检 + 符号歧义登记
    # =================================================================
    print("\n[A] 量纲机器自检（五元组 M,L,T,Q,K）")

    d_pl2 = ddiv(dmul(DIM["hbar"], DIM["G"]), dpow(DIM["c"], 3))
    guard("G0-1 planck_length_squared_is_L2", d_pl2 == dpow(LEN, 2),
          "得到 " + dstr(d_pl2))

    d_rc = dmul(DIM["G"], DIM["kg"])
    guard("G0-2 G_times_mass_is_L3_T-2", d_rc == (F0, Fraction(3), Fraction(-2), F0, F0),
          "得到 " + dstr(d_rc))

    # 熵（J/K）与西门子（1/Ohm）是两种完全不同的量纲
    d_se = ddiv(DIM["J"], TMP)
    guard("G0-3 entropy_is_J_over_K", d_se == DIM["Entropy"], "得到 " + dstr(d_se))
    d_si = ddiv(ONE, DIM["Ohm"])
    guard("G0-4 siemens_is_1_over_ohm", d_si == DIM["Siem"], "得到 " + dstr(d_si))
    guard("G0-5 entropy_is_not_siemens", DIM["Entropy"] != DIM["Siem"],
          "两种量纲竟相等，符号表不可用")
    add("A01", "INFO", "符号歧义：S = siemens 与 S = entropy 同字母",
        "西门子量纲 " + dstr(DIM["Siem"]) + "（= 1/Ω），熵量纲 " + dstr(DIM["Entropy"]) +
        "（= J/K）。r183 量纲表里的键名 \"S\" 指的是**熵**（因 kB 与熵同量纲，守卫 G0-8），"
        "不是西门子。任何把 G0=e²/h 记作 \"S\" 的读数都必须显式说明是**单位符号**还是**量纲键**，"
        "否则会出现「量纲 coincided」的假绿。本册用 Siem / Entropy 两键分离。",
        {"siemens": dstr(DIM["Siem"]), "entropy": dstr(DIM["Entropy"])})

    # e^2/h 的量纲 = 西门子
    d_g0 = ddiv(dmul(DIM["e"], DIM["e"]), DIM["h"])
    guard("G0-6 e2_over_h_is_conductance", d_g0 == DIM["Siem"], "得到 " + dstr(d_g0))
    d_rk = ddiv(DIM["h"], dmul(DIM["e"], DIM["e"]))
    guard("G0-7 h_over_e2_is_ohm", d_rk == DIM["Ohm"], "得到 " + dstr(d_rk))
    guard("G0-8 G0_times_RK_dimensionless", dmul(d_g0, d_rk) == ONE,
          "得到 " + dstr(dmul(d_g0, d_rk)))
    add("A02", "INFO", "G0 与 R_K 是互逆量：数值互反、量纲互为倒数",
        "e²/h 的量纲 " + dstr(d_g0) + "（S），h/e² 的量纲 " + dstr(d_rk) +
        "（Ω），乘积无量纲。任何把二者数值直接互换/搬移的做法都同时违反数值与量纲，"
        "T718 的 archive 缺陷正是这一类（见 E04/E05）。",
        {"G0_dim": dstr(d_g0), "RK_dim": dstr(d_rk)})

    # 无量纲量的量纲守卫
    guard("G0-9 strain_is_dimensionless", DIM["strain"] == ONE, "strain 非无量纲")

    # =================================================================
    # B 段 · T141 连续引力波椭率上限
    # =================================================================
    print("\n[B] T141 · 连续引力波椭率上限")

    T_ROT = D("0.0336")               # Crab 自转周期 33.6 ms
    OM = D(2) * PI / T_ROT
    RCW = D("1.25E4")                  # 12.5 km
    MCW = D("1.4") * MSUN

    OMK = (GV * MCW / (RCW ** 3)).sqrt()
    eps_direct = OM ** 2 * RCW ** 3 / (D(2) * GV * MCW)
    eps_ident = (OM / OMK) ** 2 / D(2)
    eps_resid = eps_direct - eps_ident

    d_eps = dmul(dpow(TIM, -1), dpow(TIM, -1))
    d_eps = dmul(d_eps, dpow(LEN, 3))
    d_eps = ddiv(d_eps, dmul(DIM["G"], MSS))
    guard("G0-10 ellipticity_dimensionless", d_eps == ONE, "得到 " + dstr(d_eps))
    d_omk = dsqrt(ddiv(dmul(DIM["G"], MSS), dpow(LEN, 3)))
    guard("G0-11 omega_k_dim_T-1", d_omk == dpow(TIM, -1), "得到 " + dstr(d_omk))

    add("B01", "PASS", "T141 上限式量纲为无量纲",
        "Ω²R³/(GM) 的量纲机给 " + dstr(d_eps) + "，与椭率（无量纲）一致。",
        {"dim": dstr(d_eps)})

    add("B02", "PASS", "Crab 参数读数：ε_max = 1.837928E-4",
        "Ω=2π/33.6 ms=" + fs(OM, 12) + " s^-1，R=12.5 km，M=1.4 M☉ ⇒ "
        "ε_max=Ω²R³/(2GM)=" + fs(eps_direct, 12) + "。",
        {"Omega": fs(OM, 12), "eps": fs(eps_direct, 12)})

    ok_ident = abs(eps_resid) < D("1E-200")
    guard("G0-13 eps_equals_half_omega_over_omegak_squared", ok_ident,
          "残差 " + fs(eps_resid, 6))
    add("B03", "PASS", "结构恒等：ε_max = (1/2)(Ω/Ω_K)²（Ω_K=√(GM/R³)）",
        "两条独立写法逐位一致，残差 " + fs(eps_resid, 6) +
        "。该恒等说明上限式等价于「自转速度与开普勒速度之比的平方的一半」，"
        "**是运动学重述，不是第一性动力学推导**（诚实标注：口径交叉印证）。",
        {"Omega_K": fs(OMK, 12), "Omega_over_OmegaK": fs(OM / OMK, 12),
         "eps_ident": fs(eps_ident, 12), "resid": fs(eps_resid, 6)})

    add("B04", "BOUNDARY", "上限是「刚体破碎判据量级」，不是精确可证伪上限",
        "Ω→Ω_K 时 ε_max→0.5，与「赤道质量脱落」自洽；但真实中子星椭率上限依赖 EoS、"
        "差动自转、磁场支撑与 crust 强度，闭式给不出这些自由度。⇒ 该式可作为**量级上限**使用，"
        "不得当作精确预测；本册不改写来料口径，只登记边界。",
        {"eps_at_kepler": "5.0E-1"})

    add("B05", "INFO", "观测比对只到「同量级」，不构成 TUFT 验证",
        "Crab 的连续波椭率观测上限量级为 1e-4～1e-3，本册读数 1.838E-4 落在该量级内。"
        "但这是**标准恒星结构算术**的参考值；TUFT 侧不供给任何椭率/形变量，故不构成验证。",
        {"eps": fs(eps_direct, 6)})

    add("B06", "INFO", "T141 三判定：C1（TUFT 侧无供给）",
        "TUFT 无中子星形变、无连续引力波闭式 ⇒ 探针不触及可动自由度。"
        "归入供给账 0/4。",
        {"verdict": "C1"})

    # =================================================================
    # C 段 · T210+T211 黑洞熵面积律与对数修正
    # =================================================================
    print("\n[C] T210+T211 · 黑洞熵面积律 + 对数修正")

    MBH = MSUN
    RS = D(2) * GV * MBH / (CV ** 2)
    AREA = D(4) * PI * RS ** 2
    LP2 = HBARV * GV / (CV ** 3)
    S_AREA = AREA / (D(4) * LP2)
    S_CLOSED = D(4) * PI * GV * MBH ** 2 / (HBARV * CV)
    S_RESID = S_AREA - S_CLOSED

    d_area = dmul(dpow(LEN, 2), dpow(LEN, -2))
    guard("G0-14 area_over_lp2_dimensionless", d_area == ONE, "得到 " + dstr(d_area))
    guard("G0-15 S_area_closed_form_identity", abs(S_RESID) < D("1E-200"),
          "残差 " + fs(S_RESID, 6))

    add("C01", "PASS", "面积律量纲：A/(4 l_P²) 无量纲（以 k_B 计）",
        "A=4πr_s² 的量纲 L²，l_P² 的量纲 L² ⇒ 商 " + dstr(d_area) + "。",
        {"dim": dstr(d_area)})

    add("C02", "PASS", "1 M☉ Schwarzschild 熵 S_BH = 1.048955E77 k_B",
        "r_s=" + fs(RS, 12) + " m，A=" + fs(AREA, 12) + " m²，"
        "S=A/(4l_P²)=" + fs(S_AREA, 12) + "；闭式 4πGM²/(ħc)=" + fs(S_CLOSED, 12) +
        "，两路残差 " + fs(S_RESID, 6) + "。**口径注**：本册取 M☉=1.98847E30（IAU 2015 名义值，"
        "与 CODATA-2018 G 同口径），故与 C0280 锚点 1.048954886E77 在 7 位内一致；"
        "r183 用的 1.98892E30 是旧口径，换成它会使本行读数偏高 0.045%（常数口径差，非物理偏差）。",
        {"r_s": fs(RS, 12), "A": fs(AREA, 12), "S": fs(S_AREA, 12),
         "S_closed": fs(S_CLOSED, 12), "resid": fs(S_RESID, 6)})

    M2 = D(2) * MBH
    S2 = D(4) * PI * GV * M2 ** 2 / (HBARV * CV)
    ratio_S = S2 / S_CLOSED
    ok_scale = abs(ratio_S - D(4)) < D("1E-200")
    guard("G0-16 entropy_scales_as_M2", ok_scale, "比值 " + fs(ratio_S, 20))
    add("C03", "PASS", "熵标度：M→2M ⇒ S→4S（S ∝ M²）",
        "比值机器 " + fs(ratio_S, 20) + "（应为 4）⇒ 面积律的 M² 标度精确成立。",
        {"ratio": fs(ratio_S, 20)})

    S_BOUND = D(2) * PI * (MBH * CV ** 2) * RS / (HBARV * CV)
    b_resid = S_BOUND - S_AREA
    guard("G0-17 bekenstein_bound_saturated", abs(b_resid) < D("1E-200"),
          "残差 " + fs(b_resid, 6))
    add("C04", "PASS", "Bekenstein 界恰好饱和：S_BH = 2πER/(ħc)（E=Mc²、R=r_s）",
        "把 R 取作 r_s 时 2πER/(ħc) 逐位等于 4πGM²/(ħc)，残差 " + fs(b_resid, 6) +
        "。**诚实标注**：这是面积律与 r_s=2GM/c² 的构造性恒等，只证明两条式子口径一致，"
        "不构成对面积律的独立验证。",
        {"S_bound": fs(S_BOUND, 12), "resid": fs(b_resid, 6)})

    lnS = S_CLOSED.ln()
    dS_log = D("-1.5") * lnS
    rel_log = abs(dS_log) / S_CLOSED
    guard("G0-18 log_correction_1Msun", abs(dS_log + D("266.0203")) < D("0.01"),
          "得到 " + fs(dS_log, 8))
    guard("G0-19 log_relative_below_1e-70", rel_log < D("1E-70"),
          "得到 " + fs(rel_log, 6))
    add("C05", "PASS", "对数修正读数：ΔS=−(3/2)ln S=−266.0203；相对 2.536E-75",
        "ln S=" + fs(lnS, 12) + "，ΔS=" + fs(dS_log, 12) + "，"
        "|ΔS|/S=" + fs(rel_log, 12) + "。单圈对数项对恒星质量黑洞完全不可观测。"
        "**口径注**：C0281 把该相对量写成 2.537E−76，实为 2.536E−75 —— 指数错一位（差 10×），"
        "本册以机器读数为准，见 C10。",
        {"lnS": fs(lnS, 12), "dS": fs(dS_log, 12), "rel": fs(rel_log, 12)})

    diff_c = abs(D("-1.5") - D("-2.5"))
    add("C06", "INFO", "两套系数口径并列不混：−3/2（面积单圈）vs −5/2（近极端欧拉标度）",
        "本册读数用 −3/2；C0232/C0245 的近极端口径 −5/2 属另一类（欧拉特征标度）。"
        "两者相差 " + fs(diff_c, 6) + "，**不可相加、不可互换**。任何把 −5/2 代入面积律的写法都是口径混用。",
        {"c_area": "-1.5", "c_near_extremal": "-2.5", "gap": fs(diff_c, 6)})

    add("C07", "BOUNDARY", "对数系数 C 不是探针能定的：需单圈谱/系综约定",
        "C 由迹反常/一阶量子修正给出，依赖场内容与系综（canonical vs microcanonical）；"
        "探针只给「形如 C ln S」的结构位，不给 C 的数值。本册不代填 C，不宣称任何 C 的预言。",
        {"C_literal": "-1.5", "note": "结构位而非数值推导"})

    add("C08", "INFO", "T210/T211 三判定：C1（TUFT 侧无微观态载体）",
        "TUFT 连续几何不供给面积熵、不供给单圈修正 ⇒ 探针不触及可动自由度。"
        "面积律与对数修正两行合并计为 2 个探针，供给 0/2。",
        {"verdict": "C1", "probes": ["T210", "T211"]})

    mP = (HBARV * CV / GV).sqrt()
    S_at_mP = D(4) * PI
    add("C09", "INFO", "对数项可观测域仅在普朗克质量附近（S~O(1)）",
        "S=4π(M/m_P)² ⇒ 1 M☉ 的 S~1e77，而对数项要到 S~O(1) 才与面积项同阶，"
        "对应 M~m_P=" + fs(mP, 12) + " kg（此时 S=4π≈" + fs(S_at_mP, 6) + "）。"
        "故对数修正是**量子引力域**的结构位，不能拿来解释恒星/星系尺度观测。",
        {"m_P": fs(mP, 12), "S_at_mP": fs(S_at_mP, 6)})

    rel_lit = D("2.537E-76")
    exp_gap = rel_log / rel_lit
    add("C10", "INFO", "C0281 的相对修正指数错一位：2.537E−76 vs 机器 2.536E−75（差 10×）",
        "机器 |ΔS|/S=" + fs(rel_log, 12) + "；C0281 报 " + fs(rel_lit, 6) +
        "，两者比值 " + fs(exp_gap, 6) + " ⇒ 指数差一位（10 倍），不是常数或口径差。"
        "该错误不改变「对数项不可观测」的定性结论，但追账必须用机器值；"
        "登记为 **F-exp**（十进制指数错位）族，与 F-unit/F-dim-blind/F-label 并列。",
        {"machine": fs(rel_log, 12), "C0281": fs(rel_lit, 6), "ratio": fs(exp_gap, 6)})

    # =================================================================
    # D 段 · T749 KLT 引力-规范双拷贝
    # =================================================================
    print("\n[D] T749 · KLT 双拷贝")

    s12 = D(2)
    s23 = D(3)
    s13 = D(-5)
    mass_shell = s12 + s13 + s23
    guard("G0-20 mass_shell_exact", mass_shell == 0, "得到 " + fs(mass_shell, 6))

    AYM = D(1)
    ATYM = D(1)
    M4 = s12 * s23 * AYM * ATYM
    add("D01", "PASS", "四点树图乘积：M₄ = s₁₂s₂₃AÃ = 2·3·1·1 = 6",
        "按来料闭式逐位求值。**诚实标注**：6 是归一化依赖的代数读数，不是可观测量；"
        "本册不声称它是物理振幅。",
        {"M4": fs(M4, 12)})

    add("D02", "PASS", "质量壳约束 s₁₂+s₁₃+s₂₃ = 0（无质量四点）",
        "抽样 (2, −5, 3) 逐位为零；该约束只在**无质量**外腿成立，有质量时由 Mandelstam 定义改写。",
        {"mass_shell": fs(mass_shell, 6)})

    # 显式量纲：自然单位制下振幅无量纲；若把 s 记作质量²，则 A 必须是质量^-2
    sdim = dmul(MSS, MSS)                       # M^2
    ampdim_natural = ONE                         # 自然单位：振幅无量纲
    prod_natural = dmul(dmul(sdim, sdim), dmul(ampdim_natural, ampdim_natural))
    guard("G0-21 product_dim_natural_units_M4", prod_natural == dpow(MSS, 4),
          "得到 " + dstr(prod_natural))
    ampdim_explicit = dpow(MSS, -2)
    prod_explicit = dmul(dmul(sdim, sdim), dmul(ampdim_explicit, ampdim_explicit))
    guard("G0-22 product_dim_explicit_amp_is_dimensionless", prod_explicit == ONE,
          "得到 " + dstr(prod_explicit))
    add("D03", "PASS", "自然单位制下：s² 的量纲 M⁴，振幅无量纲 ⇒ 乘积 M⁴（归一化记账）",
        "若采用「振幅无量纲」的自然单位约定，s₁₂s₂₃ 的量纲是 " + dstr(prod_natural) +
        "；若采用「A 的量纲 = M⁻²」的显式约定，则乘积 " + dstr(prod_explicit) +
        "（无量纲）。两种记账都可自洽，**但必须声明用的是哪一种**。",
        {"M4_natural": dstr(prod_natural), "M4_explicit": dstr(prod_explicit)})

    add("D04", "BOUNDARY", "来料的「s²×1/s⁴=1/s²」是量纲盲记账（把 s 当纯数）",
        "若 s 是**纯数**，s²·s⁻⁴=s⁻² 成立；若 s 是 Mandelstam 变量（M²），"
        "则 s² 的量纲是 M⁴，任何「1/s⁴」都必须显式写成 M⁻⁸，结果不可能是「1/s²」这种混合写法。"
        "⇒ 该量纲校验只在「s 无量纲」的约定内成立，不能作为普适量纲闭合证明。",
        {"blind": "s^2 * s^-4 = s^-2", "explicit": dstr(prod_explicit)})

    # BCJ 朴素双拷贝 vs KLT 乘积
    A_naive = D(1) / s12 + D(1) / s23 + D(1) / s13
    BCJ_naive = D(1) / s12 + D(1) / s23 + D(1) / s13     # ñ 取 1
    KLT_naive = s12 * s23 * A_naive * A_naive
    ratio_bcj = KLT_naive / BCJ_naive
    add("D05", "BOUNDARY", "「等价 BCJ 形式」未被本册验证：需要分子 n_s 与 KLT 核",
        "取 A=n_s/s+n_t/t+n_u/u（ñ=n=1）时，乘积式给 " + fs(KLT_naive, 12) +
        "，而 BCJ 求和式给 " + fs(BCJ_naive, 12) + "，比值 " + fs(ratio_bcj, 12) +
        " ≠ 1。⇒ 两式等价必须依赖具体分子与 KLT 动量核，**不能由给出的闭式直接得出**；"
        "本册只核验乘积闭式，不宣称 BCJ 等价已被证明。",
        {"KLT_naive": fs(KLT_naive, 12), "BCJ_naive": fs(BCJ_naive, 12),
         "ratio": fs(ratio_bcj, 12)})

    add("D06", "INFO", "M₄=6 不是可观测量：缺外部动量与归一化",
        "振幅的数值依赖外腿动量、极化与归一化约定；本册只复算代数恒等式，"
        "不把 6 解释为任何散射截面或可测信号。",
        {"M4": fs(M4, 6)})

    add("D07", "INFO", "T749 三判定：C1（TUFT 侧无振幅/无双拷贝）",
        "TUFT 无散射振幅、无 BCJ/KLT 结构 ⇒ 探针不触及可动自由度。供给 0/1。",
        {"verdict": "C1"})

    # =================================================================
    # E 段 · T718 附带复核（G0 与 R_K）
    # =================================================================
    print("\n[E] T718 · 量子化电导附带复核")

    G0V = EV ** 2 / HV
    RKV = HV / EV ** 2
    prod_gr = G0V * RKV
    guard("G0-23 G0_value", abs(G0V - D("3.8740458649E-5")) < D("1E-15"),
          "得到 " + fs(G0V, 12))
    guard("G0-24 RK_value", abs(RKV - D("25812.8074593")) < D("1E-6"),
          "得到 " + fs(RKV, 12))
    guard("G0-25 G0_times_RK_is_one", abs(prod_gr - D(1)) < D("1E-200"),
          "得到 " + fs(prod_gr, 30))

    add("E01", "PASS", "G₀ = e²/h = 3.874045864932E-5 S（38.74 μS）",
        "2019 SI 下 e、h 均为定义值，故 G₀ 精确。量纲 " + dstr(d_g0) + "（S）。",
        {"G0": fs(G0V, 12)})

    add("E02", "PASS", "R_K = h/e² = 25812.8074593 Ω",
        "von Klitzing 常数，2019 SI 精确值；与 G₀ 互反。",
        {"RK": fs(RKV, 12)})

    add("E03", "PASS", "G₀·R_K = 1（机器零）",
        "乘积 " + fs(prod_gr, 30) + "，确认两读数是同一常数的互逆表述。",
        {"product": fs(prod_gr, 30)})

    ARCH = D("2.58128E-5")
    ratio_arch = ARCH / G0V
    dev_arch = D(1) - ratio_arch
    guard("G0-26 archive_value_is_wrong", abs(dev_arch) > D("0.3"),
          "偏差 " + fs(dev_arch, 6))
    add("E04", "FAIL", "archive 的 G₀=2.58128E-5 S 与 e²/h 不符（偏低 33.37%）",
        "e²/h=" + fs(G0V, 12) + " S，archive 写 " + fs(ARCH, 12) + " S，"
        "比值 " + fs(ratio_arch, 12) + "，偏差 " + fs(dev_arch * 100, 12) + "%。"
        "该数既不是 G₀ 的任何舍入，也不是 SI 换算。",
        {"archive": fs(ARCH, 12), "G0": fs(G0V, 12),
         "ratio": fs(ratio_arch, 12), "dev_pct": fs(dev_arch * 100, 12)})

    RK_E9 = RKV * D("1E-9")
    rel_e9 = (RK_E9 - ARCH) / ARCH
    add("E05", "INFO", "结构诊断：2.58128E-5 = R_K × 1e-9（把电阻量子的位数搬进西门子）",
        "R_K×1e−9=" + fs(RK_E9, 12) + "，与 archive 的相对差 " + fs(rel_e9, 12) +
        " ⇒ archive 数值是把 **Ω 的位数**（25812.807…）写成 2.58128… 再乘 1e−9，"
        "属于 F-unit 族：**互为倒数的单位之间搬位数**。量纲上 Ω 与 S 互为倒数（A02），"
        "数值上 R_K 与 G₀ 也互为倒数 ⇒ 两种错误方向恰好相互掩盖，必须靠量纲门禁而非数量级门禁抓出。",
        {"RK_times_1e-9": fs(RK_E9, 12), "rel": fs(rel_e9, 12)})

    add("E06", "INFO", "T718 三判定：C1（TUFT 侧无边缘态/无量子化电导）",
        "TUFT 不供给拓扑边缘态与量子化电导 ⇒ 探针不触及可动自由度。"
        "T718 为批次外附带复核，供给 0/1（不计入第二批 0/4）。",
        {"verdict": "C1"})

    # =================================================================
    # F 段 · 三判定总表、供给账、批次账与缺陷族
    # =================================================================
    print("\n[F] 三判定 / 供给账 / 批次账")

    table = [
        {"probe": "T141", "verdict": "C1",
         "reason": "TUFT 侧无椭率/连续波闭式，无内定数值"},
        {"probe": "T210", "verdict": "C1",
         "reason": "TUFT 连续几何无面积熵/无微观态载体"},
        {"probe": "T211", "verdict": "C1",
         "reason": "TUFT 无单圈量子修正，C 由外部谱约定给出"},
        {"probe": "T749", "verdict": "C1",
         "reason": "TUFT 无散射振幅/无双拷贝结构"},
    ]
    add("F01", "INFO", "三判定总表：第二批 4 探针全部 C1（C2=0、C3=0）",
        "四行理由见 numbers.table。探针给出的是 GR/QED/振幅侧的参考值，"
        "TUFT 侧对这四个量没有任何内定数值 ⇒ 零信息量，**不得报道为通过**。",
        {"table": table, "n_C1": 4, "n_C2": 0, "n_C3": 0})

    add("F02", "INFO", "供给账：第二批 0/4，附带 T718 0/1",
        "「供给」= TUFT 自身给出的、不经外部输入的可比数值。第二批全部为 0/4；"
        "T718 附带复核亦为 0/1。与 r174 F03、r183 F02 一致：探针池只能出上限约束，不能出判别。",
        {"supply_batch": 0, "total_batch": 4, "supply_extra": 0, "total_extra": 1})

    add("F03", "CORRECTED", "编号倒置：README 与判定册对 T210/T211 的映射相反",
        "README（统一场论攻破）写 C0280→T211 面积律、C0281→T210 对数修正；"
        "而两份判定册自身写 C0280→T210 面积律、C0281→T211 对数修正。"
        "⇒ 同一对编号在两处**互换**，追账会错配。本册只登记并给出裁决口径："
        "面积律与对数修正作为**成对条目**处理，不以单号归属承重；落地修正由用户在台账层决定。",
        {"README": {"C0280": "T211", "C0281": "T210"},
         "verdict_docs": {"C0280": "T210", "C0281": "T211"},
         "ruling": "paired_item_no_single_owner"})

    add("F04", "INFO", "新登记缺陷族：F-unit / F-dim-blind / F-label / F-exp",
        "①F-unit：互为倒数的单位之间搬位数（T718：R_K 的位数搬进 S，且恰与 1e−9 相乘）；"
        "②F-dim-blind：把有量纲量当纯数做量纲校验（T749 的 s²×1/s⁴=1/s²）；"
        "③F-label：T 编号↔公式映射在不同文档间倒置（T210/T211）；"
        "④F-exp：十进制指数错一位（C0281 的 2.537E−76 vs 机器 2.536E−75）。"
        "门禁：单位先查互逆、量纲先查是否纯数、编号先查双文档一致性、指数先做 10 倍量级对撞。",
        {"members": ["T718 F-unit", "T749 F-dim-blind", "T210/T211 F-label",
                     "C0281 F-exp"]})

    add("F05", "INFO", "本卷红线与产出定性",
        "本轮产出 = ①三组探针闭环式落盘；②T718 附带复核定性；③四个缺陷族登记。"
        "不产生新物理，不宣称观测证实/否证，不改写来料字节，不改 verify.py。"
        "C1 不得写成「通过」；探针供给 0/4 维持。",
        {"supply": "0/4"})

    # =================================================================
    # 控制组（真实计算，非声明性 True）
    # =================================================================
    control("K01 S_BH_1Msun_in_range",
            D("1.0488E77") < S_AREA < D("1.0490E77"),
            "S=" + fs(S_AREA, 6))
    control("K02 S_scaling_is_4", abs(ratio_S - D(4)) < D("1E-200"),
            "ratio=" + fs(ratio_S, 20))
    control("K03 bekenstein_resid_zero", abs(b_resid) < D("1E-200"),
            "resid=" + fs(b_resid, 6))
    control("K04 crab_eps_in_observed_band",
            D("1E-4") < eps_direct < D("1E-3"),
            "eps=" + fs(eps_direct, 6))
    control("K05 eps_identity_resid_zero", abs(eps_resid) < D("1E-200"),
            "resid=" + fs(eps_resid, 6))
    control("K06 KLT_product_is_6", M4 == D(6), "M4=" + fs(M4, 6))
    control("K07 mass_shell_zero", mass_shell == 0, "shell=" + fs(mass_shell, 6))
    control("K08 G0_RK_product_one", abs(prod_gr - D(1)) < D("1E-200"),
            "prod=" + fs(prod_gr, 30))
    control("K09 archive_not_G0", abs(dev_arch) > D("0.3"),
            "dev=" + fs(dev_arch, 6))
    control("K10 log_dS_value", abs(dS_log + D("266.0203")) < D("0.01"),
            "dS=" + fs(dS_log, 8))
    control("K11 log_relative_small", rel_log < D("1E-70"),
            "rel=" + fs(rel_log, 6))
    control("K12 archive_equals_RK_e9", abs(rel_e9) < D("1E-6"),
            "rel=" + fs(rel_e9, 12))

    # =================================================================
    # 汇总
    # =================================================================
    counts = {}
    for e in ENTRIES:
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    n_g = sum(1 for g in GUARDS if g["ok"])
    n_c = sum(1 for c in CONTROLS if c["ok"])

    print("\n" + "=" * 78)
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
          % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
             counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    print("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    print("判定串：" + VERDICT)

    # ---- JSON ----
    payload = dict(
        stem=STEM,
        verdict=VERDICT,
        counts=counts,
        guards_total=len(GUARDS),
        guards_pass=n_g,
        controls_total=len(CONTROLS),
        controls_pass=n_c,
        guard_list=GUARDS,
        control_list=CONTROLS,
        entries=ENTRIES,
        supply=dict(batch="0/4", extra="0/1"),
        judgement=table,
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ---- Markdown ----
    md = []
    md.append("# " + STEM + "\n")
    md.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 0**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                 counts.get("BOUNDARY", 0), counts.get("INFO", 0),
                 counts.get("CORRECTED", 0), n_g, len(GUARDS), n_c, len(CONTROLS)))
    md.append("## 一句话\n")
    md.append("第二批 **T141 / T210 / T211 / T749** 三组探针闭环式落盘，三判定全部 **C1**"
              "（TUFT 侧供给 **0/4**），附带 T718 复核定性为 **F-unit 位数搬迁**（G₀ 偏低 33.37%，"
              "数值恰为 R_K×1e−9）。承重读数：Crab ε_max=**1.837928E−4**（且 ε=(1/2)(Ω/Ω_K)² 机器零）；"
              "1 M☉黑洞熵 **1.048955E77 k_B**（与 C0280 锚点 7 位一致）、对数修正 **−266.0203**（相对 2.536E−75）；"
              "T749 乘积 **6**、质量壳精确零、量纲记账存在 **F-dim-blind**；T718 archive 的 G₀ 与 e²/h 不符。\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"]))
    md.append("\n## 三判定\n")
    md.append("| 探针 | 判定 | 理由 |")
    md.append("|---|---|---|")
    for r in table:
        md.append("| %s | **%s** | %s |" % (r["probe"], r["verdict"], r["reason"]))
    md.append("\n## 守护（%d/%d）\n" % (n_g, len(GUARDS)))
    for g in GUARDS:
        md.append("- [%s] %s" % ("OK" if g["ok"] else "FAIL", g["name"]))
    md.append("\n## 控制组（%d/%d）\n" % (n_c, len(CONTROLS)))
    for c in CONTROLS:
        md.append("- [%s] %s %s" % ("OK" if c["ok"] else "FAIL", c["name"], c["msg"]))
    md.append("\n## 红线\n")
    md.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
              "未改写任何来料字节；未改 verify.py；未做 git 操作。探针供给 0/4 ⇒ 不得报道为「通过」。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    # ---- report.txt ----
    rep = []
    rep.append("TUFT-r184 探针池第二批 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）"
               % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                  counts.get("BOUNDARY", 0), counts.get("INFO", 0), counts.get("CORRECTED", 0)))
    rep.append("守卫 %d/%d · 控制组 %d/%d" % (n_g, len(GUARDS), n_c, len(CONTROLS)))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            try:
                rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False))
            except Exception:
                pass
        rep.append("")
    rep.append("判定串：" + VERDICT)
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))

    print("out -> %s.{json,md,_report.txt}" % STEM)
    return 0 if (n_g == len(GUARDS) and n_c == len(CONTROLS)) else 1


if __name__ == "__main__":
    sys.exit(main())
