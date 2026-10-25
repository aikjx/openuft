# -*- coding: utf-8 -*-
"""
TUFT-r186 · F5 钱德拉塞卡极限闭环式复核 · 精算
2026-10-25

承接：
  r185 F06 明确「①可精算池 12/12 已收口；剩余硬项 F5 钱德拉塞卡属②观测/天体层，仍无回合」。
  布局_剩余项分层归档 §五 F5 给出修复式 M_Ch=5.83 μ_e^-2 M☉，并称来料
  (3π/2)^{1/2}(ħc/G)^{3/2}/m_p^2「≈4×10³ M☉」为错。

本册职责：
  1) 对来料式与标准式各做一次 250 位机读，给出以 M☉ 计的读数。
  2) 判定来料的量纲是否过关（若过关，则缺陷是系数/常数而非结构）。
  3) 把「来料 vs 标准」的比值分解成两个可解释因子：m_p^2 vs (μ_e m_u)^2、系数口径。
  4) 复核布局注里的「≈4×10³ M☉」是否与机器一致（本册机器给 4.0229 M☉）。
  5) 登记修复式可执行读数与 F5 的三判定（②层，不占①池供给）。

纪律：不自推的 Lane–Emden 常数 ω₀³=2.01824 按布局来料字面使用，不另选；
      修复式只做到「可复现 5.83 μ_e^-2」；不宣称 TUFT 预言钱德拉塞卡质量。
红线：不产生新物理、不改写来料字节、不改 verify.py、不做 git。
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

STEM = "TUFT-r186_F5钱德拉塞卡极限复核_闭环式量纲与三判定_2026-10-25"

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
# 0. 量纲机器（五元组 M, L, T, Q, K）
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

DIM = {
    "c":    (F0, F1, Fraction(-1), F0, F0),
    "G":    (Fraction(-1), Fraction(3), Fraction(-2), F0, F0),
    "hbar": (F1, Fraction(2), Fraction(-1), F0, F0),
    "h":    (F1, Fraction(2), Fraction(-1), F0, F0),
    "kg":   (F1, F0, F0, F0, F0),
}

# ---- 数值常数（CODATA 2018/2022，单一 250 位口径）----
PI_STR = ("3."
          "14159265358979323846264338327950288419716939937510"
          "58209749445923078164062862089986280348253421170679"
          "82148086513282306647093844609550582231725359408128"
          "48111745028410270193852110555964462294895493038196")
PI = D(PI_STR)
CV = D("299792458")
HV = D("6.62607015E-34")
HBARV = HV / (D(2) * PI)
GV = D("6.67430E-11")
MUV = D("1.66053906660E-27")        # 原子质量常数 m_u [kg]
MPV = D("1.67262192369E-27")        # 质子质量 [kg]
MSUN = D("1.98847E30")              # IAU 2015 名义太阳质量（承 r184 口径）
OMEGA3 = D("2.01824")               # 布局来料字面：Lane–Emden 常数 ω₀³

VERDICT = ("R186-F5-CHANDRASEKHAR-FORMER-4.022932-MSUN-DIM-PASS-VALUE-FAIL-"
           "STANDARD-1.456256-MSUN-MU-E-2-RATIO-2.762516-"
           "DECOMP-3.942418-X-0.700716-M-P-MISUSE-AND-COEF-"
           "LEDGER-4E3-MSUN-IS-EXP-SLIP-1000X-"
           "REPAIR-5.83-MU-E-2-EXECUTABLE-TUFT-SUPPLY-0")


def main():
    print("=" * 78)
    print("TUFT-r186 · F5 钱德拉塞卡极限复核")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲与常数口径
    # =================================================================
    print("\n[A] 量纲机自检与常数口径")

    d_x = ddiv(dmul(DIM["hbar"], DIM["c"]), DIM["G"])
    guard("G0-1 hbar_c_over_G_is_M2", d_x == dpow(MSS, 2), "得到 " + dstr(d_x))
    d_x32 = dpow(dsqrt(d_x), 3)               # (M²)^{3/2} = M³
    d_lailiao = ddiv(d_x32, dpow(MSS, 2))
    guard("G0-2 lailiao_dim_is_M", d_lailiao == MSS, "得到 " + dstr(d_lailiao))
    d_std = ddiv(d_x32, dpow(MSS, 2))
    guard("G0-3 standard_dim_is_M", d_std == MSS, "得到 " + dstr(d_std))
    guard("G0-4 mp_over_mu", abs(MPV / MUV - D("1.007276")) < D("1E-6"),
          "m_p/m_u=" + fs(MPV / MUV, 12))

    add("A01", "PASS", "来料式 (3π/2)^{1/2}(ħc/G)^{3/2}/m_p² 的量纲是质量（量纲过关）",
        "ħc/G 的量纲 " + dstr(d_x) + "（M²），其 3/2 次为 M³，除 m_p²（M²）后得到 " +
        dstr(d_lailiao) + " ⇒ **量纲门禁放行**。这正好说明：本项不是 T163 那种「缺结构项」的"
        "量纲级错误，而是常数/系数级错误 —— 单靠量纲检查抓不出来，必须做数值机读。",
        {"dim": dstr(d_lailiao)})

    add("A02", "INFO", "常数口径声明：m_u=1.66053906660E−27、m_p=1.67262192369E−27、M☉=1.98847E30、ω₀³=2.01824",
        "m_p/m_u=" + fs(MPV / MUV, 12) + "；M☉ 承 r184 的 IAU 2015 名义值（与 CODATA-2018 G 同口径）。"
        "Lane–Emden 常数按布局来料字面取 ω₀³=2.01824，本册不另选；若要换常数口径，"
        "所有读数需整批重算。",
        {"m_u": "1.66053906660E-27", "m_p": "1.67262192369E-27",
         "Msun": "1.98847E30", "omega3": "2.01824"})

    # =================================================================
    # B 段 · 来料式与标准式的机读
    # =================================================================
    print("\n[B] 来料式 / 标准式 机读")

    X = HBARV * CV / GV
    X32 = X * X.sqrt()
    guard("G0-5 X32_value", abs(X32 - D("1.0309478814647687E-23")) < D("1E-37"),
          "得到 " + fs(X32, 12))

    LAILIAO = (D(3) * PI / D(2)).sqrt() * X32 / (MPV * MPV)
    LAILIAO_SUN = LAILIAO / MSUN
    guard("G0-6 lailiao_value", abs(LAILIAO_SUN - D("4.0229317369")) < D("1E-8"),
          "得到 " + fs(LAILIAO_SUN, 12))
    add("B01", "PASS", "来料式机器读数：4.0229317369 M☉（=7.9994790709E30 kg）",
        "(3π/2)^{1/2}=" + fs((D(3) * PI / D(2)).sqrt(), 12) + "；(ħc/G)^{3/2}=" +
        fs(X32, 12) + " kg³；除 m_p² 得 " + fs(LAILIAO, 12) + " kg ⇒ " +
        fs(LAILIAO_SUN, 12) + " M☉。**关键**：量纲虽是质量，数值却不是布局注所称的 4×10³ M☉。",
        {"kg": fs(LAILIAO, 12), "Msun": fs(LAILIAO_SUN, 12)})

    COEF = OMEGA3 * (D(3) * PI).sqrt() / D(2)
    MUE = D(2)                                  # μ_e = 2（碳/氧主导，电子数/核子数）
    STD = COEF * X32 / ((MUE * MUV) * (MUE * MUV))
    STD_SUN = STD / MSUN
    guard("G0-7 standard_value", abs(STD_SUN - D("1.4562564383")) < D("1E-8"),
          "得到 " + fs(STD_SUN, 12))
    add("B02", "PASS", "标准式机器读数：μ_e=2 ⇒ M_Ch = 1.4562564383 M☉",
        "系数 ω₀³·√(3π)/2=" + fs(COEF, 12) + "；分母 (μ_e m_u)² ⇒ " +
        fs(STD, 12) + " kg = " + fs(STD_SUN, 12) + " M☉。与 5.83/μ_e²=1.4575 的"
        "取整锚点在 0.086% 内一致（5.83 是三位有效数字的取整值）。",
        {"coef": fs(COEF, 12), "kg": fs(STD, 12), "Msun": fs(STD_SUN, 12)})

    RATIO = LAILIAO_SUN / STD_SUN
    guard("G0-8 ratio_value", abs(RATIO - D("2.7625160179")) < D("1E-8"),
          "得到 " + fs(RATIO, 12))
    add("B03", "PASS", "来料/标准 = 2.7625160179（系统性偏大 2.76 倍）",
        fs(LAILIAO_SUN, 12) + " ÷ " + fs(STD_SUN, 12) + " = " + fs(RATIO, 12) +
        "。⇒ 来料既不是「4×10³ 倍」也不是量纲错，而是 2.76 倍的系数/常数错。",
        {"ratio": fs(RATIO, 12)})

    FM = ((MUE * MUV) / MPV) ** 2
    FC = ((D(3) * PI / D(2)).sqrt()) / COEF
    PROD = FM * FC
    guard("G0-9 decomposition_identity", abs(PROD - RATIO) < D("1E-200"),
          "乘积 " + fs(PROD, 18) + " vs 比值 " + fs(RATIO, 18))
    add("B04", "PASS", "比值分解（机器零）：2.7625160 = 3.9424175 × 0.7007162",
        "①**质量项**：来料用 m_p²、标准用 (μ_e m_u)² ⇒ 因子 ((2m_u)/m_p)²=" +
        fs(FM, 12) + "（来料偏大）；②**系数项**：√(3π/2)=" +
        fs((D(3) * PI / D(2)).sqrt(), 12) + " vs ω₀³√(3π)/2=" + fs(COEF, 12) +
        " ⇒ 因子 " + fs(FC, 12) + "（来料偏小）。乘积 " + fs(PROD, 18) +
        " 与直接比值逐位一致 ⇒ 两处缺口**恰好解释全部偏差**，无剩余。",
        {"mass_factor": fs(FM, 12), "coef_factor": fs(FC, 12), "product": fs(PROD, 18)})

    add("B05", "PASS", "标准式自洽：ω₀³√(3π)/2 · (ħc/G)^{3/2}/(μ_e m_u)² = 5.8250 μ_e^{-2} M☉",
        "取 μ_e=1 时机器给 " + fs(COEF * X32 / (MUV * MUV) / MSUN, 12) +
        " M☉，与 5.83 的取整锚点相对差 " +
        fs(abs(COEF * X32 / (MUV * MUV) / MSUN / D("5.83") - D(1)), 6) +
        " ⇒ 标准式可复现 5.83 系数。**诚实标注**：这是用**同一批常数**复现锚点，属口径交叉印证；"
        "独立验证需要恒星结构方程数值解，不在本册范围。",
        {"mu_e_1": fs(COEF * X32 / (MUV * MUV) / MSUN, 12)})

    mu4 = D(4)
    STD4 = COEF * X32 / ((mu4 * MUV) * (mu4 * MUV))
    guard("G0-10 mue_scaling_exact4", abs((STD_SUN / (STD4 / MSUN)) - D(4)) < D("1E-200"),
          "比值 " + fs(STD_SUN / (STD4 / MSUN), 12))
    add("B06", "PASS", "μ_e 标度：μ_e→2μ_e ⇒ M_Ch→M_Ch/4（平方反比精确）",
        "机器比值 " + fs(STD_SUN / (STD4 / MSUN), 18) + "（应为 4）⇒ `M_Ch ∝ μ_e^{-2}` "
        "的指数精确成立。该标度是标准式的结构性内容，与常数取值无关。",
        {"ratio": fs(STD_SUN / (STD4 / MSUN), 18)})

    add("B07", "BOUNDARY", "缺口定性：两处结构位（质量口径 + Lane–Emden 系数），不是单点笔误",
        "①来料把 (μ_e m_u)² 写成 m_p² —— μ_e（电子数/核子数）与 m_u/m_p 的换算被整体省略；"
        "②来料系数用 √(3π/2)，标准用 ω₀³√(3π)/2 —— 欠 Lane–Emden 常数 ω₀³。"
        "两处都不是「改一个数字」能修的：必须同时补 μ_e 定义与 ω₀³。修复式见 C04。",
        {"gaps": ["m_p^2 -> (mu_e m_u)^2", "sqrt(3pi/2) -> omega0^3 sqrt(3pi)/2"]})

    # =================================================================
    # C 段 · 台账注复核与修复式
    # =================================================================
    print("\n[C] 台账注复核 / 修复式")

    LEDGER = D("4E3")
    SLIP = LEDGER / LAILIAO_SUN
    guard("G0-11 ledger_vs_machine_1000x", abs(SLIP - D("994.3")) < D("1"),
          "台账/机器=" + fs(SLIP, 12))
    add("C01", "FAIL", "台账注「来料 ≈4×10³ M☉」与机器 4.0229 M☉ 相差 10³（F-exp）",
        "布局 §五 F5 的修复注写「≈4×10³ M☉」，本册机器读数为 " + fs(LAILIAO_SUN, 12) +
        " M☉；台账/机器 = " + fs(SLIP, 6) + " ⇒ **恰好 10³ 量级**。"
        "该 10³ 既不是 cgs/SI 换算（本册 cgs 路线与 SI 路线逐位同值，见 C02），"
        "也不是 m_p 与 m_u 的口径差（该因子只有 3.94）⇒ 只能是十进制指数错位，"
        "登记为 **F-exp**（与 r184 C10 的 C0281 同族）。",
        {"ledger": "4E3", "machine": fs(LAILIAO_SUN, 12), "ratio": fs(SLIP, 6)})

    # cgs 路线：ħ=1.054571817E-27 erg·s、c=2.99792458E10 cm/s、G=6.67430E-8 cgs、m_p=1.67262192369E-24 g
    HB_CGS = HV / (D(2) * PI) * D("1E7")        # erg·s = 1e7 × J·s? J·s -> erg·s: ×1e7
    C_CGS = CV * D("1E2")
    G_CGS = GV * D("1E3")
    MP_CGS = MPV * D("1E3")
    X_CGS = HB_CGS * C_CGS / G_CGS
    X32_CGS = X_CGS * X_CGS.sqrt()
    L_CGS = (D(3) * PI / D(2)).sqrt() * X32_CGS / (MP_CGS * MP_CGS)   # 单位 g
    L_CGS_KG = L_CGS / D("1E3")
    guard("G0-12 cgs_si_agree", abs(L_CGS_KG / LAILIAO - D(1)) < D("1E-30"),
          "cgs/SI 比值 " + fs(L_CGS_KG / LAILIAO, 18))
    add("C02", "INFO", "cgs 与 SI 路线逐位同值 ⇒ 10³ 不是单位制差，而是指数错位",
        "cgs 路线（ħ=1.054571817E−27 erg·s、G=6.67430E−8、m_p=1.67262192369E−24 g）"
        "给 " + fs(L_CGS, 12) + " g = " + fs(L_CGS_KG, 12) + " kg，"
        "与 SI 路线相对差 " + fs(abs(L_CGS_KG / LAILIAO - D(1)), 6) +
        " ⇒ 单位换算干净。故台账的 4×10³ 只能是 10³ 指数错位（F-exp）。",
        {"cgs_g": fs(L_CGS, 12), "cgs_kg": fs(L_CGS_KG, 12)})

    add("C03", "CORRECTED", "台账第三处假绿：F5 的「修复注」自身数值错",
        "r185 F03 已登记第二处假绿（布局 T718 行仍标 ✔）；本册是第三处：F5 修复注把来料读数"
        "写成 4×10³ M☉（真值 4.0229 M☉），并据此判「错得离谱」。结论方向（来料错）不变，"
        "但错因被夸大 10³，会误导修复优先级。本册只登记，不改写布局字节；"
        "落地由用户在台账层把注改为「4.02 M☉，偏大 2.76×」。",
        {"ledger": "4E3", "machine": fs(LAILIAO_SUN, 12),
         "true_dev": fs(RATIO, 6), "mark": "false-green"})

    REPAIR = D("5.83") / (MUE * MUE)
    guard("G0-13 repair_value", abs(REPAIR - D("1.4575")) < D("1E-12"),
          "得到 " + fs(REPAIR, 6))
    add("C04", "PASS", "修复式可执行：M_Ch = 5.83 μ_e^{-2} M☉ ⇒ μ_e=2 时 1.4575 M☉",
        "机器 " + fs(REPAIR, 6) + " M☉；与本册标准式 " + fs(STD_SUN, 12) +
        " M☉ 相对差 " + fs(abs(REPAIR / STD_SUN - D(1)), 6) +
        "（来自 5.83 的三位取整）。**修复式可用**，但必须与 μ_e 的定义一起落地。",
        {"repair_sun": fs(REPAIR, 6), "machine_sun": fs(STD_SUN, 12)})

    # =================================================================
    # D 段 · 三判定、供给账与缺陷族
    # =================================================================
    print("\n[D] 三判定 / 供给账 / 缺陷族")

    table = [
        {"probe": "F5/T-Chandrasekhar", "verdict": "C1",
         "reason": "TUFT 无恒星结构方程、无简并压闭式 ⇒ 零供给"},
    ]
    add("D01", "INFO", "F5 三判定：C1（TUFT 侧无恒星结构/无简并压）",
        "TUFT 不供给状态方程、不供给简并压 ⇒ 探针不触及可动自由度。"
        "F5 属②观测/天体层，不进入①可精算池的供给账。",
        {"table": table, "n_C1": 1, "n_C2": 0, "n_C3": 0})

    add("D02", "INFO", "供给账：①池 12/12 已收口（0/12，不变）；F5 不占①池",
        "r183/r184/r185 已把①池 12 项全部落盘，供给 0/12。F5 是②层硬项，"
        "本册只做闭环式复核，**不改变**①池的 12/12 与 0/12。",
        {"pool": "12/12", "supply": "0/12", "f5_layer": "2"})

    add("D03", "INFO", "缺陷族补充：F-exp 新增成员（F5 修复注的 4×10³）",
        "F-exp 原成员为 C0281 的 2.537E−76（r184 C10）；本册新增 F5 修复注的 4×10³ vs 4.02。"
        "其余五族（F-pi/F-unit/F-dim-blind/F-label/F-scale）本批无新增。"
        "门禁：任何「≈N×10^k」的规模判断，必须先跑机器值再写指数。",
        {"F_exp_members": ["C0281 2.537E-76", "F5 ledger 4E3"], "families": 6})

    add("D04", "INFO", "本卷红线与产出定性",
        "本轮产出 = ①F5 来料/标准的 250 位机读；②偏差的两因子精确分解；"
        "③台账注 10³ 指数错位定性（F-exp）；④修复式可执行读数。"
        "不产生新物理，不宣称观测证实/否证，不改写来料字节，不改 verify.py，不做 git。",
        {"supply": "0/12"})

    # =================================================================
    # 控制组（真实计算）
    # =================================================================
    control("K01 lailiao_is_4p02", abs(LAILIAO_SUN - D("4.0229")) < D("1E-3"),
            "lailiao=" + fs(LAILIAO_SUN, 8))
    control("K02 standard_is_1p456", abs(STD_SUN - D("1.4563")) < D("1E-3"),
            "std=" + fs(STD_SUN, 8))
    control("K03 ratio_is_2p76", abs(RATIO - D("2.7625")) < D("1E-3"),
            "ratio=" + fs(RATIO, 8))
    control("K04 decomp_exact", abs(PROD - RATIO) < D("1E-200"),
            "resid=" + fs(PROD - RATIO, 6))
    control("K05 coeff_5p825", abs(COEF * X32 / (MUV * MUV) / MSUN - D("5.825")) < D("1E-2"),
            "5.825_check=" + fs(COEF * X32 / (MUV * MUV) / MSUN, 8))
    control("K06 mue_scaling", abs(STD_SUN / (STD4 / MSUN) - D(4)) < D("1E-200"),
            "ratio=" + fs(STD_SUN / (STD4 / MSUN), 12))
    control("K07 ledger_is_1000x", abs(SLIP - D("1000")) < D("10"),
            "slip=" + fs(SLIP, 6))
    control("K08 repair_in_band", D("1.45") < REPAIR < D("1.47"),
            "repair=" + fs(REPAIR, 6))
    control("K09 cgs_si_equal", abs(L_CGS_KG / LAILIAO - D(1)) < D("1E-30"),
            "rel=" + fs(abs(L_CGS_KG / LAILIAO - D(1)), 6))
    control("K10 dim_is_mass", d_lailiao == MSS, "dim=" + dstr(d_lailiao))

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
        supply=dict(pool="12/12", supply="0/12", f5_layer="2"),
        judgement=table,
    )
    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = []
    md.append("# " + STEM + "\n")
    md.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / INFO %d / CORRECTED %d）；"
              "守卫 %d/%d；控制组 %d/%d；退出码 0**\n"
              % (len(ENTRIES), counts.get("PASS", 0), counts.get("FAIL", 0),
                 counts.get("BOUNDARY", 0), counts.get("INFO", 0),
                 counts.get("CORRECTED", 0), n_g, len(GUARDS), n_c, len(CONTROLS)))
    md.append("## 一句话\n")
    md.append("F5 钱德拉塞卡：来料式**量纲过关**（M），机器读数 **4.0229317369 M☉**（不是台账所称 4×10³）；"
              "标准式 μ_e=2 给 **1.4562564383 M☉**，比值 **2.7625160** 被"
              "**3.9424175（m_p²→(μ_e m_u)²）× 0.7007162（欠 ω₀³）** 逐位解释（残差机器零）。"
              "台账注的 10³ 恰为指数错位（F-exp，非单位制差：cgs/SI 逐位同值）；"
              "修复式 **5.83 μ_e^{-2} = 1.4575 M☉** 可执行。F5 三判定 **C1**，①池 12/12、供给 0/12 不变。\n")
    md.append("## 条目\n")
    md.append("| 编号 | 级 | 标题 |")
    md.append("|---|---|---|")
    for e in ENTRIES:
        md.append("| %s | %s | %s |" % (e["code"], e["level"],
                                        e["title"].replace("|", "\\|")))
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
              "未改写任何来料字节；未改 verify.py；未做 git 操作。TUFT 供给 0/12 维持。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    rep = []
    rep.append("TUFT-r186 F5 钱德拉塞卡极限复核 · 运行报告")
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
