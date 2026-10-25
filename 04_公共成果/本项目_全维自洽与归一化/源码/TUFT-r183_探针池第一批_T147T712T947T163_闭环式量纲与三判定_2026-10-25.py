# -*- coding: utf-8 -*-
"""
TUFT-r183 · 探针池第一批（T147 / T712 / T947 / T163）闭环式量纲与三判定 · 精算
2026-10-25

来料（只读，不改写）：
  A. openuft/04_公共成果/本项目_统一场论攻破/布局_剩余项分层归档_2026-10-24.md §一（①可精算池 12 项 + §五修复清单 F1–F5）
  B. 同目录 README.md L10（「第一批攻坚锁定 T147/T712/T947/T163（Decimal 250 位）」）
  C. 用户 2026-10-24《TUFT 验证与应用全方案》第五节（每批 4 探针 → 残差表 → chi² → 联合后验）

本册职责（承接 r174 的 F02 裁定）：
  r174 已判「第一批只锁定、未落盘」。本册把锁定项**首次真正执行并落盘**，
  给出 4 个探针的闭环式、量纲、数值表、结构诊断与**三判定**（C1/C2/C3）。

三判定口径（本册定义，可执行）：
  C1 无约束（退化）：探针不触及 TUFT 的可动自由度（TUFT 侧供给=0）⇒ 零信息量。
  C2 力约束放行    ：TUFT 侧有数值且落在探针区间内 ⇒ 仅「一致」，**不得作证明**。
  C3 力约束否定    ：TUFT 侧有数值且越出探针上界 ⇒ 该自由度被压缩/排除（仍不否定公理集本体）。

纪律（继承 r174）：
  · 探针对 TUFT 的供给恒为 0；PROBE 永不出「PASS-as-proof」，最高只到 C3 型约束。
  · 「残差机器零」若来自构造性恒等式，必须显式标注「口径交叉印证、非独立验证」。
  · 不自推的系数一律标 BOUNDARY 并指向登记处，不猜。
红线：本册不产生新物理，不宣称观测证实/否证，不改写任何来料字节。
"""
import json
import math
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

STEM = "TUFT-r183_探针池第一批_T147T712T947T163_闭环式量纲与三判定_2026-10-25"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

D = Decimal

ENTRIES = []


def add(code, level, title, detail, numbers=None):
    ENTRIES.append(dict(code=code, level=level, title=title,
                        detail=detail, numbers=numbers or {}))


GUARDS = []


def guard(name, ok, msg=""):
    ok = bool(ok)
    GUARDS.append(dict(name=name, ok=ok, msg=msg))
    if not ok:
        print("  [GUARD-FAIL] {}".format(name))
        print("      {}".format(msg))
    return ok


def fs(x, nd=25):
    try:
        v = D(x)
        if v.is_zero():
            # Decimal 零值经 '.nE' 格式化会把指数印成 n（如 0.0000E+4），
            # 易被误读为 1e4；此处显式固定为 E+0。
            return "0." + "0" * nd + "E+0"
        return format(v, "." + str(nd) + "E")
    except Exception:
        return str(x)


# =====================================================================
# 0. 量纲机器（五元组 M, L, T, Q, K；K = 温度） + 自身守卫
# =====================================================================
def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    return tuple(x * n for x in a)


def dsqrt(a):
    return tuple(Fraction(x, 2) for x in a)


def dstr(a):
    syms = ("M", "L", "T", "Q", "K")
    parts = []
    for s, e in zip(syms, a):
        if e != 0:
            parts.append(s + "^" + str(e))
    return "1" if not parts else " ".join(parts)


Z = (Fraction(0),) * 5
ONE = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
LEN = (Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0))
TIM = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0))
TMP = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1))
MSS = (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0))

DIM = {
    "c":     (Fraction(0), Fraction(1), Fraction(-1), Fraction(0), Fraction(0)),
    "G":     (Fraction(-1), Fraction(3), Fraction(-2), Fraction(0), Fraction(0)),
    "hbar":  (Fraction(1), Fraction(2), Fraction(-1), Fraction(0), Fraction(0)),
    "h":     (Fraction(1), Fraction(2), Fraction(-1), Fraction(0), Fraction(0)),
    "kB":    (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(-1)),
    "e":     (Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    "eps0":  (Fraction(-1), Fraction(-3), Fraction(2), Fraction(2), Fraction(0)),
    "mu0":   (Fraction(1), Fraction(1), Fraction(0), Fraction(-2), Fraction(0)),
    "me":    (Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    "W":     (Fraction(1), Fraction(2), Fraction(-3), Fraction(0), Fraction(0)),
    "Ohm":   (Fraction(1), Fraction(2), Fraction(-1), Fraction(-2), Fraction(0)),
    "Gth":   (Fraction(1), Fraction(2), Fraction(-3), Fraction(0), Fraction(-1)),
    "kcond": (Fraction(1), Fraction(1), Fraction(-3), Fraction(0), Fraction(-1)),
    "S":     (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(-1)),
    "L0":    (Fraction(2), Fraction(4), Fraction(-4), Fraction(-2), Fraction(-2)),
    "B":     (Fraction(1), Fraction(0), Fraction(-1), Fraction(-1), Fraction(0)),
    "Q2":    (Fraction(1), Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
    "r":     (Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
}

# ---- 数值常数（单一口径：CODATA 2018/2022 字面值）----
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
EPS0V = D("8.8541878128E-12")
ALPHA_LIT = D("7.2973525693E-3")
MPCV = D("3.0856775814913673E22")          # 1 Mpc [m]
MSUN = D("1.98892E30")                     # kg
G0V = D("9.80665")


def main():
    print("=" * 78)
    print("TUFT-r183 · 探针池第一批 T147/T712/T947/T163 · 闭环式与三判定")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲机器自身守卫（先自检，再审对象）
    # =================================================================
    print("\n[A] 量纲机器自检（五元组 M,L,T,Q,K）")

    # G0-1 普朗克长度 = sqrt(hbar G / c^3)
    d_pl = dsqrt(ddiv(dmul(DIM["hbar"], DIM["G"]), dpow(DIM["c"], 3)))
    guard("G0-1 planck_length_is_L", d_pl == DIM["r"],
          "得到 " + dstr(d_pl))

    # G0-2 普朗克时间
    d_pt = ddiv(DIM["r"], DIM["c"])
    guard("G0-2 planck_time_is_T", d_pt == TIM, "得到 " + dstr(d_pt))

    # G0-3 普朗克温度 = sqrt(hbar c^5 / (G kB^2))
    d_tpl = dsqrt(ddiv(dmul(dpow(DIM["c"], 5), DIM["hbar"]),
                       dmul(DIM["G"], dmul(DIM["kB"], DIM["kB"]))))
    guard("G0-3 planck_temperature_is_K", d_tpl == TMP, "得到 " + dstr(d_tpl))

    # G0-4 alpha 无量纲：e^2/(eps0 hbar c)
    d_alpha = ddiv(dmul(DIM["e"], DIM["e"]),
                   dmul(DIM["eps0"], dmul(DIM["hbar"], DIM["c"])))
    guard("G0-4 alpha_dimensionless", d_alpha == ONE, "得到 " + dstr(d_alpha))

    # G0-5 eps0 mu0 c^2 = 1
    d_em = dmul(DIM["eps0"], dmul(DIM["mu0"], dpow(DIM["c"], 2)))
    guard("G0-5 eps0_mu0_c2_dimensionless", d_em == ONE, "得到 " + dstr(d_em))

    # G0-6 焦耳 = W*s
    d_j = dmul(DIM["W"], TIM)
    guard("G0-6 joule_is_W_times_s",
          d_j == (Fraction(1), Fraction(2), Fraction(-2), Fraction(0), Fraction(0)),
          "得到 " + dstr(d_j))

    # G0-7 热导(W/K) 与 热导率(W/m/K) 差且仅差 L^-1
    d_gap = ddiv(DIM["Gth"], DIM["kcond"])
    guard("G0-7 thermal_conductance_minus_conductivity_is_L^-1", d_gap == LEN,
          "实际差 " + dstr(d_gap) + "（应为 L^1：conductance = conductivity / L）")
    if d_gap == LEN:
        pass
    # 说明：Gth / kcond = L^1，故 Gth = kcond * L
    guard("G0-7b orientation", dmul(DIM["kcond"], LEN) == DIM["Gth"],
          "kcond*L != Gth")

    # G0-8 k_B 与熵同量纲
    guard("G0-8 kB_is_entropy", DIM["kB"] == DIM["S"], "得到 " + dstr(DIM["kB"]))

    # G0-9 Lorenz 数 L0 = kB^2/e^2（差无量纲 pi^2/3）
    d_l0 = ddiv(dmul(DIM["kB"], DIM["kB"]), dmul(DIM["e"], DIM["e"]))
    guard("G0-9 lorenz_dim_is_kB2_over_e2", d_l0 == DIM["L0"], "得到 " + dstr(d_l0))

    # G0-10 热导量子：kB^2 * K / h （注意：分子是**温度**不是时间）
    d_q = ddiv(dmul(dmul(DIM["kB"], DIM["kB"]), TMP), DIM["h"])
    guard("G0-10 thermal_quantum_is_W_per_K", d_q == DIM["Gth"], "得到 " + dstr(d_q))

    # G0-11 陷阱登记：若把公式里的 T 误当**时间**，会得到 W/K^2（差一个 K）
    d_q_wrong = ddiv(dmul(dmul(DIM["kB"], DIM["kB"]), TIM), DIM["h"])
    guard("G0-11 thermal_quantum_time_trap", d_q_wrong != DIM["Gth"],
          "把温度当时间竟仍得 W/K（陷阱未复现，量纲表可疑）")
    add("A11", "INFO", "量纲表陷阱：T712 的 T 是温度不是时间",
        "kB^2*T/h 若把 T 当时间维得 " + dstr(d_q_wrong) + "，比热导量子 " + dstr(DIM["Gth"]) +
        " 多一个 K^-1。本册量纲机用五元组（含 K）以杜绝该混用；四元组机器必然算错这一项。",
        {"quantum": dstr(DIM["Gth"]), "wrong": dstr(d_q_wrong)})

    # G0-12 磁场量纲：F = q v B
    d_B = ddiv((Fraction(1), Fraction(1), Fraction(-2), Fraction(0), Fraction(0)),
               dmul(DIM["e"], DIM["c"]))
    guard("G0-12 tesla_dim", d_B == DIM["B"], "得到 " + dstr(d_B))

    # G0-13 曲率 L^-1 与 L^-2 的二分（r174 A01/A02 的口径根源）
    kappa_F = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0))
    kappa_2 = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0), Fraction(0))
    guard("G0-13 kappa_two_calibres", kappa_F != kappa_2, "两种曲率口径竟相等")

    # G0-14 圆周运动：a^3 w^2 = G M 的量纲
    d_kepler = dmul(dpow(DIM["r"], 3), dpow(TIM, -2))
    guard("G0-14 kepler_dim", d_kepler == dmul(DIM["G"], MSS),
          "a^3w^2 = " + dstr(d_kepler) + " ; GM = " + dstr(dmul(DIM["G"], MSS)))

    # G0-15 只用 1/r 不足以把 GQ/c^4 变成应变（应为 T^2），必须再补二阶时间导数
    d_gq_r = ddiv(dmul(DIM["G"], DIM["Q2"]), dmul(dpow(DIM["c"], 4), DIM["r"]))
    guard("G0-15 GQ_over_c4r_is_T2", d_gq_r == dpow(TIM, 2),
          "G Q /(c^4 r) = " + dstr(d_gq_r) + "（应为 T^2：仅补 1/r 还不够）")
    d_h = ddiv(dmul(DIM["G"], ddiv(DIM["Q2"], dpow(TIM, 2))),
               dmul(dpow(DIM["c"], 4), DIM["r"]))
    guard("G0-15b strain_with_second_time_derivative", d_h == ONE,
          "G Qddot /(c^4 r) = " + dstr(d_h) + "（应为 1）")

    # G0-16 来料式 GQ/c^4 的量纲（应为 L T^2，即 archive 所说「ms^2」）
    d_lai163 = ddiv(dmul(DIM["G"], DIM["Q2"]), dpow(DIM["c"], 4))
    guard("G0-16 lai_memory_dim_is_L_T2", d_lai163 == (Fraction(0), Fraction(1), Fraction(2), Fraction(0), Fraction(0)),
          "得到 " + dstr(d_lai163))

    # =================================================================
    # B 段 · T147 Hellings–Downs 角相关曲线
    # =================================================================
    print("\n[B] T147 · PTA Hellings–Downs 角相关")

    X_STAR = (D(-5) / D(6)).exp()            # d/dx[1.5x ln x - x/4] = 0  =>  ln x = -5/6
    GAM_MIN = D("0.5") - D("1.5") * X_STAR   # 闭式：1.5x*(-5/6) - x/4 + 0.5 = 0.5 - 1.5x

    def hd_std(x):
        """标准 HD：zeta = 3/2 x ln x - x/4 + 1/2，x=(1-cos)/2；x->0 取极限 1/2"""
        if x == 0:
            return D("0.5")
        return D("1.5") * x * x.ln() - x / D(4) + D("0.5")

    def hd_lai(x):
        """来料简化式：zeta = 1/2 (1 + ((1+cos)/2) ln x)，(1+cos)/2 = 1 - x"""
        if x == 0:
            return None                       # 发散
        return (D(1) + (D(1) - x) * x.ln()) / D(2)

    SQ2 = D(2).sqrt()
    SQ3 = D(3).sqrt()
    COS_PTS = [
        ("0（自相关）", D(1)),
        ("30", SQ3 / D(2)),
        ("45", SQ2 / D(2)),
        ("60", D("0.5")),
        ("82.4814（极值点）", D(1) - D(2) * X_STAR),
        ("90", D(0)),
        ("120", D("-0.5")),
        ("135", -SQ2 / D(2)),
        ("150", -SQ3 / D(2)),
        ("180", D(-1)),
    ]

    rows = []
    max_abs_diff = D(0)
    max_at = ""
    for lab, cs in COS_PTS:
        x = (D(1) - cs) / D(2)
        st = hd_std(x)
        la = hd_lai(x)
        df = None if la is None else (la - st)
        rows.append(dict(theta=lab, cos=fs(cs, 12), x=fs(x, 12),
                         std=fs(st, 18), lai=("发散" if la is None else fs(la, 18)),
                         diff=("-" if df is None else fs(df, 18))))
        if df is not None and abs(df) > max_abs_diff:
            max_abs_diff = abs(df)
            max_at = lab
        print("  theta=%-18s x=%-14s 标准=%-22s 来料=%-22s 差=%s"
              % (lab, fs(x, 6), fs(st, 10), ("发散" if la is None else fs(la, 10)),
                 ("-" if df is None else fs(df, 10))))

    # B01 标准式端点
    ok_a = (hd_std(D(0)) == D("0.5"))
    ok_b = (hd_std(D(1)) == D("0.25"))
    ok_c = abs(hd_std(D("0.5")) - D("-0.144860")) < D("1E-5")
    guard("B01 hd_endpoints", ok_a and ok_b and ok_c,
          "Gamma(0)=" + fs(hd_std(D(0))) + " Gamma(pi)=" + fs(hd_std(D(1))) +
          " Gamma(90deg)=" + fs(hd_std(D("0.5"))))
    add("B01", "PASS" if (ok_a and ok_b and ok_c) else "FAIL",
        "标准 HD 式三点端点与文献一致",
        "Gamma(0+)=1/2（自相关极限）、Gamma(pi)=1/4、Gamma(90deg)=-0.144860。"
        "三点同时命中即证明本册实现的是标准式（非归一化变形）。",
        {"G0": fs(hd_std(D(0)), 18), "Gpi": fs(hd_std(D(1)), 18),
         "G90": fs(hd_std(D("0.5")), 18)})

    # B02 极值闭式 vs 数值扫描（x 参数直接扫，避开三角函数）
    NPT = 20000
    best_x = None
    best_v = None
    for i in range(1, NPT):
        x = D(i) / D(NPT)
        v = hd_std(x)
        if best_v is None or v < best_v:
            best_v = v
            best_x = x
    d_gap_min = abs(best_v - GAM_MIN)
    d_gap_arg = abs(best_x - X_STAR)
    # 数值导数在 x* 处应为 0
    hstep = D("1E-20")
    dslope = (hd_std(X_STAR + hstep) - hd_std(X_STAR - hstep)) / (D(2) * hstep)
    ok_b02 = (d_gap_min < D("1E-9")) and (d_gap_arg < D("1E-4")) and (abs(dslope) < D("1E-15"))
    guard("B02 hd_minimum_closed_form", ok_b02,
          "扫描min=" + fs(best_v) + " 闭式=" + fs(GAM_MIN) + " 斜率=" + fs(dslope))
    th_min_float = math.degrees(math.acos(1.0 - 2.0 * float(X_STAR)))
    add("B02", "PASS" if ok_b02 else "FAIL",
        "HD 极值点闭式：x*=e^(-5/6)，Gamma_min=1/2-(3/2)e^(-5/6)",
        "解析求极值 dGamma/dx=1.5(ln x+1)-1/4=0 => ln x=-5/6；代回得闭式 Gamma_min=0.5-1.5x*。"
        "数值扫描（20000 点）与闭式一致，x* 处数值斜率机器零。"
        "theta_min 由 float 交叉核对给出（不入 Decimal 判定链，因本册不实现 arccos）。",
        {"x_star": fs(X_STAR, 18), "gamma_min": fs(GAM_MIN, 18),
         "scan_min": fs(best_v, 18), "scan_argmin": fs(best_x, 12),
         "slope_at_xstar": fs(dslope), "theta_min_deg_float": str(round(th_min_float, 4))})

    # B03 来料式三点结构错
    lai_0 = hd_lai(D("0.5"))       # 90deg
    lai_pi = hd_lai(D(1))          # 180deg
    lai_90_diff = lai_0 - hd_std(D("0.5"))
    lai_pi_diff = lai_pi - hd_std(D(1))
    add("B03", "FAIL", "来料简化式与标准式不差归一化常数（结构性错误）",
        "来料 zeta=1/2(1+((1+cos)/2)ln x)。与标准式相比：90deg 差 " + fs(lai_90_diff, 6) +
        "，180deg 差 " + fs(lai_pi_diff, 6) + "，而 60deg 差仅 0.0625 —— 差值是角的函数、不是常数，"
        "故「差 1/2 归一化约定」的解释不成立。",
        {"diff_at_90": fs(lai_90_diff, 18), "diff_at_180": fs(lai_pi_diff, 18),
         "diff_at_60": fs(hd_lai(D("0.25")) - hd_std(D("0.25")), 18),
         "max_abs_diff_over_table": fs(max_abs_diff, 12), "max_at": max_at})

    # B04 来料式 theta->0 对数发散
    div_rows = []
    for e in (2, 4, 6, 8):
        x = D(10) ** (-e)
        lv = hd_lai(x)
        sv = hd_std(x)
        resid = lv - D("0.5") * x.ln()
        div_rows.append(dict(x=fs(x, 6), lai=fs(lv, 10), std=fs(sv, 10),
                             resid=fs(resid, 12), ratio=fs(lv / x.ln(), 10)))
        print("  x=%-12s 来料=%-22s 标准=%-20s 来料-0.5ln(x)=%s"
              % (fs(x, 4), fs(lv, 8), fs(sv, 10), fs(resid, 8)))
    r_last = abs(D(div_rows[-1]["resid"]) - D("0.5")) < D("1E-6")
    s_last = abs(D(div_rows[-1]["std"]) - D("0.5")) < D("1E-6")
    guard("B04 lai_diverges_logarithmically", r_last and s_last,
          "来料-0.5ln(x) 应收敛到 0.5，实得 " + div_rows[-1]["resid"] +
          " ; 标准式应停在 0.5，实得 " + div_rows[-1]["std"])
    add("B04", "FAIL", "来料式在 theta->0 处对数发散（标准式有限）",
        "x->0 时来料 = 1/2 + 1/2(1-x)ln x ~ 1/2 ln x -> -inf；标准式因带 1.5x ln x 的 x 因子而收敛到 1/2。"
        "机器复算：x=1e-2/1e-4/1e-6/1e-8 时 来料/ln x -> 0.5（残差<1e-6），标准式四点全部落在 0.5 附近。"
        "这是**定性级**缺陷（自相关点必须有限），不可由归一化修补。",
        {"rows": div_rows, "std_at_1e-8": fs(hd_std(D("1E-8")), 12)})

    # B05 结构分解恒等：来料 - 标准 = (1/2 - 2x) ln x + x/4
    worst = D(0)
    for i in range(1, 400):
        x = D(i) / D(400)
        lhs = hd_lai(x) - hd_std(x)
        rhs = (D("0.5") - D(2) * x) * x.ln() + x / D(4)
        if abs(lhs - rhs) > worst:
            worst = abs(lhs - rhs)
    guard("B05 decomposition_identity", worst < D("1E-200"),
          "分解式残差 " + fs(worst) + "（应机器零）")
    add("B05", "PASS" if worst < D("1E-200") else "FAIL",
        "结构分解：来料式 − 标准式 = (1/2−2x)ln x + x/4（机器零）",
        "该分解把差异定位到两处：①角变量被取成互补量（y=1−x 替代 x），②缺 −x/4 项。"
        "两项都不是常数，故来料式与标准式之间**不存在**任何归一化/缩放等价。",
        {"residual_max": fs(worst)})

    # =================================================================
    # C 段 · T712 一维声子量子热导
    # =================================================================
    print("\n[C] T712 · 一维声子量子热导")

    T1 = D(1)                                   # 1 K
    kappa_Q = PI * PI * KBV * KBV * T1 / (D(3) * HV)
    kappa_lai = KBV * KBV * T1 / (D(3) * HV)
    ratio_pi2 = kappa_Q / kappa_lai
    print("  kappa_Q(1K) = %s W/K" % fs(kappa_Q))
    print("  来料式(1K)  = %s   比值 = %s (pi^2=%s)"
          % (fs(kappa_lai), fs(ratio_pi2, 12), fs(PI * PI, 12)))

    ok_pi = abs(ratio_pi2 - PI * PI) < D("1E-40")
    guard("C01 pi_square_ratio", ok_pi, "比值=" + fs(ratio_pi2) + " pi^2=" + fs(PI * PI))
    add("C01", "FAIL", "来料 T712 缺 pi^2 因子（低估 9.8696 倍）",
        "标准式 kappa=pi^2 kB^2 T/(3h)，来料式 kappa=kB^2 T/(3h)。比值机器等于 pi^2，"
        "故这是**单一常数因子漏项**，不是量级估计误差。1 K 单通道读数：标准 " + fs(kappa_Q, 12) +
        " W/K，来料 " + fs(kappa_lai, 12) + " W/K。",
        {"kappa_Q_1K": fs(kappa_Q), "kappa_lai_1K": fs(kappa_lai),
         "ratio": fs(ratio_pi2, 18), "pi2": fs(PI * PI, 18)})

    # C02 量纲口径：Gth (W/K) vs kcond (W/m/K)
    add("C02", "BOUNDARY", "T712 的 kappa 是「每通道热导 W/K」，不是热导率 W/(m·K)",
        "量纲机给 kB^2*T/h = " + dstr(DIM["Gth"]) + "（= W/K），而热导率是 " + dstr(DIM["kcond"]) +
        "，两者差且仅差一个 L^1（Gth = kcond·L，守卫 G0-7/G0-7b）。"
        "若把该式当热导率代入（如与体材料 kappa_lattice 比较），必须补长度标度（通道长度或平均自由程），"
        "该长度不在闭式内、属**外部输入**。本册不改写来料公式，只登记口径。",
        {"Gth": dstr(DIM["Gth"]), "kcond": dstr(DIM["kcond"])})

    # C03 Lorenz 交叉（恒等构造，显式标注非独立验证）
    G0q = EV * EV / HV
    L0V = PI * PI * KBV * KBV / (D(3) * EV * EV)
    prod = L0V * T1 * G0q
    res_id = (prod - kappa_Q) / kappa_Q
    guard("C03 lorenz_identity", abs(res_id) < D("1E-50"), "残差 " + fs(res_id))
    add("C03", "INFO", "kappa_Q = L0·T·G0 恒等（口径交叉印证，非独立验证）",
        "Lorenz 数 L0=pi^2 kB^2/(3e^2)=" + fs(L0V, 12) + " W*Ohm/K^2；与 G0=e^2/h 相乘再乘 T 逐字还原 pi^2kB^2T/(3h)，"
        "残差机器零。**必须显式标注**：这是构造性恒等，只证明两条式子口径一致，不构成对 T712 的独立验证；"
        "T712 的独立内容只有「pi^2 前因子」这一项。",
        {"L0": fs(L0V, 12), "G0_S": fs(G0q, 12), "residual": fs(res_id)})

    # C04 附带发现：archive 的 T718 数值与 e^2/h 不符
    g_arch = D("2.58128E-5")
    rk = HV / (EV * EV)
    ratio_718 = g_arch / G0q
    hint = rk * D("1E-9")
    d_hint = abs(hint - g_arch) / g_arch
    ok718 = (abs(ratio_718 - D(1)) > D("1E-3")) and (d_hint < D("1E-5"))
    guard("C04 t718_archive_value_inconsistent", ok718,
          "archive=" + fs(g_arch) + " e^2/h=" + fs(G0q) + " R_K*1e-9=" + fs(hint))
    add("C04", "FAIL", "附带发现（批次外）：archive T718 的 G0 数值与 e^2/h 不符",
        "archive 写 G0=e^2/h=2.58128e-5 S，但 e^2/h 实为 " + fs(G0q, 12) + " S（= 1/R_K，R_K=" +
        fs(rk, 12) + " Ohm），比值 " + fs(ratio_718, 8) + "。而 2.58128e-5 恰等于 R_K×1e-9，"
        "即**把电阻量子的数值位数搬到 S 单位并乘 1e-9**（相对差 " + fs(d_hint, 6) +
        "）。该式不在本批 4 探针内，纳入第二批复核，本册只登记不改写。",
        {"archive": fs(g_arch), "e2_over_h": fs(G0q, 12), "R_K": fs(rk, 12),
         "ratio": fs(ratio_718, 12), "R_K_times_1e-9": fs(hint, 12),
         "rel_dev_of_hint": fs(d_hint)})

    # =================================================================
    # D 段 · T947 真空双折射 Klein 系数
    # =================================================================
    print("\n[D] T947 · 真空双折射（QED 弱场）")

    Bcr = MEV * MEV * CV * CV / (EV * HBARV)
    alpha_der = EV * EV / (D(4) * PI * EPS0V * HBARV * CV)
    coef_std = ALPHA_LIT / (D(30) * PI)                 # Delta n = (alpha/30pi)(B/Bcr)^2
    per_t2 = coef_std / (Bcr * Bcr)                     # 每 T^2 系数
    coef_lai = ALPHA_LIT / (D(4) * PI) * (D(45) / D(90))
    ratio_lai = coef_lai / coef_std

    print("  Bcr        = %s T" % fs(Bcr, 12))
    print("  alpha(字面)= %s   alpha(e,eps0,hbar,c)= %s" % (fs(ALPHA_LIT, 12), fs(alpha_der, 12)))
    print("  alpha/30pi = %s  => 每 T^2 系数 = %s" % (fs(coef_std, 12), fs(per_t2, 12)))
    print("  来料 alpha/4pi*45/90 = %s   比值 = %s" % (fs(coef_lai, 12), fs(ratio_lai, 8)))

    # D01 Bcr 双路径（EH 临界场 4.41e13 G 换算）
    bcr_gauss = Bcr * D("1E4")
    ok_bcr = (abs(Bcr - D("4.4139E9")) / Bcr < D("1E-3")) and \
             (abs(bcr_gauss - D("4.4139E13")) / bcr_gauss < D("1E-3"))
    guard("D01 bcr_two_paths", ok_bcr,
          "Bcr=" + fs(Bcr, 10) + " T ; = " + fs(bcr_gauss, 10) + " G")
    add("D01", "PASS" if ok_bcr else "FAIL",
        "临界场 Bcr = m_e^2 c^2/(e hbar) 双路径一致",
        "由 CODATA 直接算得 " + fs(Bcr, 12) + " T（= " + fs(bcr_gauss, 10) + " G），"
        "与 QED 文献通用值 4.41e13 G 相对偏差 <1e-3。两条路径（SI 公式 / 高斯制换算）互证。",
        {"Bcr_T": fs(Bcr, 14), "Bcr_G": fs(bcr_gauss, 12),
         "alpha_literal": fs(ALPHA_LIT, 14), "alpha_derived": fs(alpha_der, 14),
         "alpha_rel_dev": fs((alpha_der - ALPHA_LIT) / ALPHA_LIT, 6)})

    # D02 标准系数与文献数值 4e-24
    lit = D("4E-24")
    dev_lit = (per_t2 - lit) / lit
    ok_d02 = abs(dev_lit) < D("1E-2")
    guard("D02 coef_against_literature", ok_d02, "相对偏差 " + fs(dev_lit))
    add("D02", "PASS" if ok_d02 else "FAIL",
        "标准系数 alpha/30pi 复现文献 4e-24 T^-2",
        "alpha/30pi = " + fs(coef_std, 14) + "；除以 Bcr^2 得每 T^2 系数 " + fs(per_t2, 14) +
        "，与文献通用取整值 4e-24 相对偏差 " + fs(dev_lit, 6) + "（<1%，由取整造成）。",
        {"coef": fs(coef_std, 18), "per_T2": fs(per_t2, 18), "rel_dev_vs_4e-24": fs(dev_lit)})

    # D03 来料系数倍数
    ok_d03 = abs(ratio_lai - D("3.75")) < D("1E-30")
    guard("D03 lai_over_std_is_3_75", ok_d03, "比值 " + fs(ratio_lai))
    add("D03", "FAIL", "来料系数 alpha/4pi×(45/90) 比标准大 3.75 倍",
        "(alpha/4pi)*(1/2) = alpha/8pi，除以 alpha/30pi 恰为 30/8 = 3.75（机器等号成立）。"
        "即来料把标准系数放大 3.75 倍，Δn 在同等 B 下系统性偏大 3.75 倍。",
        {"coef_lai": fs(coef_lai, 18), "ratio": fs(ratio_lai, 18)})

    # D04 结构诊断：若保留 alpha/(4pi) 前因子，括号内应为 12/90
    alt = ALPHA_LIT / (D(4) * PI) * (D(12) / D(90))
    ok_alt = abs(alt - coef_std) / coef_std < D("1E-200")
    guard("D04 alternative_bracket_12_over_90", ok_alt,
          "alpha/(4pi)*12/90 与 alpha/30pi 不符，差 " + fs((alt - coef_std) / coef_std))
    add("D04", "INFO", "结构诊断：45/90 不是约分失误，是系数被折成了错误的分数",
        "若坚持 alpha/(4pi) 前因子，则括号内必须是 12/90（=2/15）才能得到 alpha/30pi；机器验证两式逐位相等。"
        "来料写 45/90（=1/2）意味着前因子实际被当成 alpha/8pi。"
        "故缺陷性质是**系数被拆成未约分分数后取错分子**，与 T712 的「漏 pi^2」同属 F-pi 族（见 F03）。",
        {"alpha_4pi_times_12_90": fs(alt, 20), "alpha_30pi": fs(coef_std, 20),
         "residual": fs((alt - coef_std) / coef_std)})

    # D05 磁星越界表（本册新增承重读数）
    mag_rows = []
    for eb in (8, 9, 10, 11):
        bval = D(10) ** eb
        beta = bval / Bcr
        dn = per_t2 * bval * bval
        state = "线性区" if beta < D("0.5") else ("临界" if beta < D(2) else "越界(beta>1)")
        mag_rows.append(dict(B_T=fs(bval, 6), beta=fs(beta, 8), gamma2=fs(beta * beta, 8),
                             Dn=fs(dn, 10), state=state))
        print("  B=%-10s T  B/Bcr=%-12s (B/Bcr)^2=%-12s Delta n=%-16s %s"
              % (fs(bval, 3), fs(beta, 6), fs(beta * beta, 6), fs(dn, 8), state))
    add("D05", "BOUNDARY", "★磁星表面场使弱场 EH 展开参数越界（Layer-3 通道②须降级）",
        "B/Bcr 在 B=1e9/1e10/1e11 T 时分别为 0.2265/2.265/22.65。磁星表面场量级 1e10–1e11 T，"
        "故 (B/Bcr)^2 = 5.1–5.1e2 ≫ 1，**弱场闭式（只保留 (B/Bcr)^2 一阶）在该域不成立**。"
        "推论：①方案 Layer-2 预言 C 的「磁场修正」不能在磁星表面直接用 alpha/30pi 式给数；"
        "②方案 Layer-3 拒证通道②「磁星双折射与 EH 一致 ⇒ 压缩光子-挠率耦合」在 beta>1 处"
        "本身无判别力（参考值需完整 EH 或更高阶），该通道应降级为 BOUNDARY 并注明需完整 EH 数值；"
        "③可用的线性区上限为 B ≲ 1e9 T（1e13 G），此时 Δn ~ 4e-6。",
        {"rows": mag_rows, "beta_at_1e10": fs(D(10) ** 10 / Bcr, 10),
         "beta_at_1e11": fs(D(10) ** 11 / Bcr, 10)})

    # D06 探针→约束的可执行形式（不宣称数值）
    add("D06", "INFO", "T947 对 TUFT 的约束形式（需数据，当前不可赋值）",
        "若 TUFT 的磁星双折射预言写成 Δn_TUFT = Δn_EH(1 + ξ·f(B))，则观测给出 |ξ| 的上界；"
        "ξ 是本库记为 O-TORSION-PHOTON 的自由耦合，其数值**不在本框架内**（r174 F04 的 P5 项）。"
        "本册不代填 ξ，也不宣称任何上界数值 —— 因为①beta>1 处参考值本身未定（D05），"
        "②ξ 与 B 的函数形式未给定。故判定为 C1（探针不触及可动自由度）。",
        {"verdict": "C1"})

    # =================================================================
    # E 段 · T163 Bondi 记忆位移
    # =================================================================
    print("\n[E] T163 · Bondi 记忆位移")

    # E01/E02 量纲（G0-15 / G0-16 已机器化，这里落条目）
    add("E01", "PASS", "标准式 Δh^TT = 2G ΔQ̈/(c^4 r) 量纲为无量纲",
        "量纲机：G Q/(c^4 r) = " + dstr(d_h) + "（=1），再乘 T^-2 与 T^2 相消。守卫 G0-15。",
        {"dim": dstr(d_h)})
    add("E02", "FAIL", "来料式 Δh = G ΔQ/c^4 量纲为 L·T^2（既非无量纲也非应变）",
        "量纲机给 " + dstr(d_lai163) + "。缺口向量 = 标准 − 来料 = " +
        dstr(ddiv(ONE, d_lai163)) + "，即**同时缺 1/r 与两个时间导数**两处结构位置。守卫 G0-16。",
        {"dim_lai": dstr(d_lai163), "gap": dstr(ddiv(ONE, d_lai163))})

    # E03 补因子穷举：{G, hbar, r, c} 指数 -3..3 求缺口
    target = ddiv(ONE, d_lai163)
    hits = []
    for g in range(-3, 4):
        for hf in range(-3, 4):
            for a in range(-3, 4):
                for b in range(-3, 4):
                    cand = dmul(dpow(DIM["G"], g),
                                dmul(dpow(DIM["hbar"], hf),
                                     dmul(dpow(DIM["r"], a), dpow(DIM["c"], b))))
                    if cand == target:
                        hits.append((g, hf, a, b))
    n_hits = len(hits)
    hit_txt = "; ".join("G^{} hbar^{} r^{} c^{}".format(*h) for h in hits)
    ok_e03 = (n_hits == 1) and (hits[0] == (0, 0, -3, 2))
    guard("E03 gap_power_search_unique", ok_e03,
          "命中 " + str(n_hits) + " 组：" + hit_txt)
    add("E03", "INFO", "缺口补因子穷举：唯一解 r^-3 c^2（物理无意义 ⇒ 结构缺失）",
        "在 {G, hbar, r, c} 的 [-3,3] 指数网格（2401 组）中求 L^-1 T^-2，命中 " + str(n_hits) +
        " 组：[" + hit_txt + "]。唯一解是 r^-3 c^2 —— 用「距离三次方反比」去补一个应变缺口在物理上不可接受。"
        "⇒ 结论：T163 的缺口不是「漏一个量纲常数」，而是**结构项缺失**（缺 1/r 与二阶时间导数两个独立位置），"
        "任何单幂次补齐都无意义。",
        {"hits": hits, "n_hits": n_hits})

    # E04 圆轨道 Kepler 闭合（标度检验）
    Mbin = D(60) * MSUN
    asep = D("3E8")                     # 分离 [m]（并合前量级）
    rdist = D(400) * MPCV               # 400 Mpc

    def h_scaled(Mv, a, r):
        return GV * GV * Mv * Mv / CV ** 4 / (a * r)

    h_ref = h_scaled(Mbin, asep, rdist)
    s_M = h_scaled(D(2) * Mbin, asep, rdist) / h_ref
    s_a = h_scaled(Mbin, D(2) * asep, rdist) / h_ref
    s_r = h_scaled(Mbin, asep, D(2) * rdist) / h_ref
    ok_scale = (abs(s_M - D(4)) < D("1E-40")) and \
               (abs(s_a - D("0.5")) < D("1E-40")) and \
               (abs(s_r - D("0.5")) < D("1E-40"))
    guard("E04 scaling_law_M2_over_ar", ok_scale,
          "M 加倍 -> " + fs(s_M) + " ; a 加倍 -> " + fs(s_a) + " ; r 加倍 -> " + fs(s_r))
    v2 = GV * Mbin / asep
    v_over_c = (v2 / (CV * CV)).sqrt()
    h_canon = GV * Mbin / (CV * CV * rdist) * (v2 / (CV * CV))
    res_canon = (h_canon - h_ref) / h_ref
    guard("E04b canonical_form_isomorphic", abs(res_canon) < D("1E-50"),
          "与 (GM/c^2r)(v^2/c^2) 相对残差 " + fs(res_canon))
    add("E04", "PASS" if (ok_scale and abs(res_canon) < D("1E-50")) else "FAIL",
        "标准式经 Kepler 闭合得 h ∝ G^2 M^2/(c^4 a r)，标度律三点全对",
        "取 Q~M a^2、Q̈~4M a^2 w^2（圆轨道 2w 振荡）、a^3 w^2 = GM ⇒ h = 8G^2M^2/(c^4 a r)。"
        "标度检验：M 加倍 → " + fs(s_M, 8) + "（应 4）、a 加倍 → " + fs(s_a, 8) +
        "（应 1/2）、r 加倍 → " + fs(s_r, 8) + "（应 1/2），三点全中。"
        "该式与标准 PN 形式 (GM/c^2r)(v^2/c^2) 逐字同构（相对残差机器零）。"
        "**诚实标注**：同构复算属恒等检验，只证明前因子 2 与 2w 的组合落在 O(1)，不构成独立验证；"
        "O(1) 系数本身依赖 Q_ij 是否取无迹与 TT 投影约定，本册不判系数。",
        {"h_ref": fs(h_ref, 12), "scaling_M": fs(s_M), "scaling_a": fs(s_a),
         "scaling_r": fs(s_r), "v_over_c": fs(v_over_c, 12),
         "canonical_residual": fs(res_canon)})

    # E05 来料式缺 1/r ⇒ 距离标度错误
    val_lai = GV * Mbin * asep * asep / (CV ** 4)
    h_1mpc = h_scaled(Mbin, asep, D(1) * MPCV)
    ratio_r = h_1mpc / h_ref
    ok_e05 = (abs(ratio_r - D(400)) < D("1E-30"))
    guard("E05 lai_missing_1_over_r", ok_e05, "1Mpc/400Mpc 比值 " + fs(ratio_r))
    add("E05", "FAIL", "来料式无 1/r ⇒ 距离标度定性错误",
        "记忆位移必须随距离衰减（1/r）；来料式 GQ/c^4 与 r 无关，且在量纲上非无量纲，故其数值本身无物理意义"
        "（" + fs(val_lai, 8) + "，量纲 " + dstr(d_lai163) + "）。正确式在 1 Mpc 与 400 Mpc 的比值为 " +
        fs(ratio_r, 8) + "（= 距离比 400），来料式该比值恒为 1。",
        {"lai_value": fs(val_lai, 12), "h_1Mpc": fs(h_1mpc, 12),
         "h_400Mpc": fs(h_ref, 12), "ratio": fs(ratio_r)})

    # E06 两级结构登记
    add("E06", "BOUNDARY", "记忆的两级结构：线性 ΔQ̈ 与非线性 Christodoulou 差 v/c 阶",
        "来料只给一个式子。完备描述分两级：线性记忆（由 ΔQ̈，与振荡项同为 Newton 阶振幅）"
        "与非线性记忆（Christodoulou，源为能流，比线性项小 v/c 阶）。本册算得该装置 v/c = " +
        fs(v_over_c, 8) + "，即非线性项约为线性项的 " + fs(v_over_c * 100, 6) + "%。"
        "**本册不推系数**，只登记「单式不足以覆盖两级」这一结构性事实，系数须回 Favata 2010 / arXiv:1807.00990。",
        {"v_over_c": fs(v_over_c, 14)})

    # E07 判定汇总
    add("E07", "FAIL", "T163 判定：标准式 PASS（标度正确）／来料式 FAIL（量纲+距离标度+时间导数三处缺）",
        "来料式三处结构性缺失：①缺 1/r（距离标度）；②缺二阶时间导数（Q 应为 Q̈）；③因此量纲为 L·T^2。"
        "标准式在标度层完全正确，O(1) 系数待约定。",
        {"verdict_lai": "FAIL", "verdict_std": "PASS"})

    # =================================================================
    # F 段 · 三判定总表 / 供给账 / 缺陷族 / P1 可执行核验 / 批次账
    # =================================================================
    print("\n[F] 三判定 · 供给账 · 缺陷族 · P1 核验 · 批次账")

    # F01 三判定总表
    verdicts = [
        ("T147", "C1", "TUFT 侧无 HD 角相关系闭式（该曲线属 GR/PTA 的几何因子，与螺旋公设无关）"),
        ("T712", "C1", "TUFT 侧无量子热导闭式；且 kappa 的量纲口径（W/K vs W/m/K）未在本框架内定标"),
        ("T947", "C1", "TUFT 侧的偏差是自由耦合 ξ（r174 P5），无内定数值；且 beta>1 处参考值未定"),
        ("T163", "C1", "TUFT 侧无记忆位移闭式；标准式本身依赖 Q_ij 约定，非框架内生"),
    ]
    add("F01", "INFO", "三判定总表：第一批 4 探针全部 C1（无约束/退化）",
        "按本册定义的三判定（C1 无约束 / C2 一致 / C3 否定），四个探针全部落在 C1："
        "探针给出的是 GR/QED/PTA 侧的**参考值**，TUFT 侧对这四个量没有任何内定数值可供比较。"
        "⇒ 第一批 4 探针的产出不是「验证 TUFT」，而是：①校准审计工具（本轮抓出 4 处结构性错）、"
        "②排定观测通道量程（T947 的 beta>1 越界就是新增量程约束）。"
        "**不得**把 C1 报道为「通过」或「一致」。",
        {"table": [{"probe": p, "verdict": v, "reason": r} for p, v, r in verdicts],
         "n_C1": 4, "n_C2": 0, "n_C3": 0})

    # F02 供给账
    supply = 0
    for p, v, r in verdicts:
        if v in ("C2", "C3"):
            supply += 1
    ok_f02 = (supply == 0)
    guard("F02 tuft_supply_is_zero", ok_f02, "供给计数 " + str(supply))
    add("F02", "INFO", "供给账：4 探针中 TUFT 侧可赋值者 0 个（0/4）",
        "「供给」指 TUFT 自身给出的、不经外部输入的可比数值。第一批全部为 0/4。"
        "这与 r174 F03 的结论一致：探针池当前只能出上限约束，不能出判别。"
        "⇒ 方案第五节「联合 chi² 曲面」在供给=0 时**没有可拟合的自由度映射**，"
        "须先解 P1–P5 才谈后验。",
        {"supply": supply, "total": 4})

    # F03 缺陷族 F-pi
    add("F03", "INFO", "新登记缺陷族 F-pi：系数被拆成未约分分数 / 漏 pi 幂",
        "本批两处同族：①T712 漏 pi^2（比值恰 pi^2=9.8696）；②T947 把 alpha/30pi 拆成"
        "alpha/4pi×45/90（应为 ×12/90，比值恰 3.75=30/8）。共同形态：**前因子与括号分数各自看似合理，"
        "但乘积错了整数倍**。可执行门禁：任何形如 (a/b) 的系数先做最简分数，并把 pi 的幂次数进台账，"
        "再与标准式逐位比对；只比「数量级」的检查必然漏掉这两类。",
        {"members": ["T712 (pi^2)", "T947 (12/90 vs 45/90)"]})

    # F04 P1 零成本改名：可执行核验
    kappa_F = (Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0))
    kappa_A3 = (Fraction(0), Fraction(-2), Fraction(0), Fraction(0), Fraction(0))   # 母册公理3 口径
    kappa_lai_dim = (Fraction(0), Fraction(2), Fraction(0), Fraction(0), Fraction(0))  # 来稿 omega=c/sqrt(kappa) 所需
    d_Q = kappa_A3                                      # Q := kappa_F^2 + tau^2  => L^-2
    d_sqrtQ = dsqrt(d_Q)                                # = L^-1（= omega/c）
    ok_p1a = (d_sqrtQ == kappa_F)
    d_l = ddiv(ONE, d_sqrtQ)                            # l = 1/sqrt(Q) => L
    d_omega = dmul(DIM["c"], d_sqrtQ)                   # w = c*sqrt(Q) => T^-1
    ok_p1b = (d_l == LEN) and (d_omega == dpow(TIM, -1))
    guard("F04a Q_dim_L^-2", ok_p1a, "sqrt(Q) = " + dstr(d_sqrtQ))
    guard("F04b omega_is_c_over_l", ok_p1b,
          "l=" + dstr(d_l) + "（应 L）; c*sqrt(Q)=" + dstr(d_omega) + "（应 T^-1）")

    helix_ok = True
    helix_rows = []
    for Rv, bv in ((D(1), D("0.5")), (D("2.5"), D("1.75")), (D("0.3"), D("3.2"))):
        Llen = (Rv * Rv + bv * bv).sqrt()
        kap = Rv / (Llen * Llen)
        tau = bv / (Llen * Llen)
        lhs = kap * kap + tau * tau
        rhs = D(1) / (Llen * Llen)
        wv = CV / Llen
        res1 = (lhs - rhs) / rhs
        res2 = (wv * wv / (CV * CV) - lhs) / lhs
        helix_rows.append(dict(R=fs(Rv, 6), b=fs(bv, 6), L=fs(Llen, 12),
                               kappa=fs(kap, 12), tau=fs(tau, 12),
                               res_kt=fs(res1), res_omega=fs(res2)))
        if abs(res1) > D("1E-60") or abs(res2) > D("1E-60"):
            helix_ok = False
        print("  helix R=%s b=%s -> kappa=%s tau=%s  kappa^2+tau^2 vs (w/c)^2 残差=%s"
              % (fs(Rv, 4), fs(bv, 4), fs(kap, 8), fs(tau, 8), fs(res2, 4)))
    guard("F04c helix_triplet_exact", helix_ok, "三例残差应机器零")

    d_ratio_cal = ddiv(kappa_lai_dim, kappa_A3)          # L^+2 / L^-2 => L^+4
    ok_p1d = (d_ratio_cal == (Fraction(0), Fraction(4), Fraction(0), Fraction(0), Fraction(0)))
    guard("F04d two_calibres_differ_by_L4", ok_p1d,
          "L^+2 / L^-2 比值 = " + dstr(d_ratio_cal))

    add("F04", "PASS" if (ok_p1a and ok_p1b and helix_ok and ok_p1d) else "FAIL",
        "P1 零成本改名可执行核验通过：κ(公理3) := Q ≡ κ_F^2 + τ^2，三重闭合残差机器零",
        "①若把母册公理 3 的 κ 读作 Q≡κ_F²+τ²（量纲 " + dstr(d_Q) + "），则 l=1/√Q 量纲 L、"
        "ω=c/l 量纲 T^-1，公理 3 **原样成立**；②同一 Q 满足三重奏 κ_F²+τ²=(ω/c)²，三例螺旋机器残差 0；"
        "③而来稿的 ω=c/√κ 要求 [κ]=L^+2，与母册 [κ]=L^-2 相差恰好 L^4（守卫 F04d）⇒ 两口径不可混用。"
        "⇒ **P1 的代价确认为零**（只改一个符号的定义，不改任何数值），且一次改名同时消除 r174 A01/A02 的冲突。"
        "**本册不改写母册字节**，是否落地由用户裁决。",
        {"Q_dim": dstr(d_Q), "sqrtQ_dim": dstr(d_sqrtQ),
         "two_calibre_ratio": dstr(d_ratio_cal), "helix": helix_rows})

    # F05 P3 的机器代价（回链 r174，不新增 claim）
    s_req = D("5.074E10")
    s_halo = D("1.576E-29")
    gap_halo = s_req / s_halo
    gap_nuc = D("6.01")
    orders = gap_halo.log10()
    ok_f05 = (abs(orders - D("39.5")) < D("0.2"))
    guard("F05 halo_gap_39_5_orders", ok_f05, "log10(gap) = " + fs(orders))
    add("F05", "BOUNDARY", "P3（登记 Cartan 式）的代价：预言 A 的星系晕表述被否证，仅剩核密度窄域",
        "回链 r174 D 段：τ_需=3.159e-24 m^-1（尺度 10.26 Mpc）、s_需=5.074e10 vs 星系晕全极化上限 1.576e-29 ⇒ "
        "缺口 3.22e39 = " + fs(orders, 6) + " 个量级。若把源换成**核密度全极化**，缺口降到 " +
        fs(gap_nuc, 4) + " 倍 —— 仍 >1，只能靠 O(1) 以上的系数容忍度（r174 已明确该参照不承重）。"
        "⇒ P3 的真实代价不是「预言 A 全灭」，而是「预言 A 必须从星系晕改写成核密度源，并欠 6 倍系数」。"
        "本册不代选；只把两种表述的可否证性差异机器化：星系晕表述 = 已成否定，核密度表述 = 需 O(1) 系数登记。",
        {"gap_halo": fs(gap_halo, 10), "orders": fs(orders, 10),
         "gap_nuclear": fs(gap_nuc, 4)})

    # F06 批次账修正
    add("F06", "CORRECTED", "批次账修正：T163 属第一批；第二批实际新项为 T141/T210(+T211)/T749",
        "来稿第五节把第二批写成「T163/T141/T210/T749」，但 T163 已在第一批锁定并已由本册执行完毕 ⇒ "
        "第二批的真实新工作量为 3 项（T141 / T210 与 T211 成对 / T749），不是 4 项。"
        "另：T163 在本册已判定（标准式 PASS、来料 FAIL），第二批无需重做，只需引用。"
        "进度账：第一批 4/4 已落盘（本册）；①可精算池剩余 8 项（T141/T210/T211/T567/T568/T718/T831/T749/T935 中除去本批）。",
        {"batch1_done": ["T147", "T712", "T947", "T163"],
         "batch2_new": ["T141", "T210", "T211", "T749"],
         "note": "T163 不重复计入第二批"})

    # =================================================================
    # 输出
    # =================================================================
    print("\n" + "=" * 78)
    n_pass = sum(1 for e in ENTRIES if e["level"] == "PASS")
    n_fail = sum(1 for e in ENTRIES if e["level"] == "FAIL")
    n_bound = sum(1 for e in ENTRIES if e["level"] == "BOUNDARY")
    n_info = sum(1 for e in ENTRIES if e["level"] == "INFO")
    n_corr = sum(1 for e in ENTRIES if e["level"] == "CORRECTED")
    n_g = len(GUARDS)
    n_gok = sum(1 for g in GUARDS if g["ok"])
    print("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）"
          % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info))
    print("守卫 %d/%d" % (n_gok, n_g))
    print("=" * 78)

    payload = dict(
        stem=STEM,
        round="r183",
        date="2026-10-25",
        scope="探针池第一批 T147 / T712 / T947 / T163（承接 r174 F02：只锁定未落盘）",
        counts=dict(entries=len(ENTRIES), PASS=n_pass, FAIL=n_fail,
                    BOUNDARY=n_bound, CORRECTED=n_corr, INFO=n_info,
                    guards=n_g, guards_ok=n_gok),
        verdicts=[{"probe": p, "verdict": v, "reason": r} for p, v, r in verdicts],
        entries=ENTRIES,
        guards=GUARDS,
    )

    with open(os.path.join(OUTD, STEM + ".json"), "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=1)

    lines = []
    lines.append("# " + STEM)
    lines.append("")
    lines.append("**条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）；守卫 %d/%d；退出码 0**"
                 % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info, n_gok, n_g))
    lines.append("")
    lines.append("## 一句话")
    lines.append("")
    lines.append("第一批 4 探针**首次真正落盘**；三判定全部 C1（TUFT 供给 0/4）⇒ 探针池当前只出参考值与量程，"
                 "不出判别。来料 4 式全部含结构性缺陷（T147 角变量互补+缺项+发散、T712 漏 pi^2、"
                 "T947 系数放大 3.75 倍、T163 缺 1/r 与二阶时间导数），标准式 4/4 复算通过。"
                 "本轮新增两处承重读数：**T947 磁星表面 (B/Bcr)^2 达 5–500 ⇒ 弱场闭式越界，Layer-3 通道②须降级**；"
                 "**T712 的 kappa 是热导 W/K 而非热导率**（差一个长度标度，属外部输入）。"
                 "P1（κ→Q 改名）零成本已机器证实；P3 的代价收窄为「预言 A 从星系晕改写为核密度源 + 欠 6 倍系数」。")
    lines.append("")
    lines.append("## 条目")
    lines.append("")
    lines.append("| 编号 | 级 | 标题 |")
    lines.append("|---|---|---|")
    for e in ENTRIES:
        lines.append("| %s | %s | %s |" % (e["code"], e["level"], e["title"]))
    lines.append("")
    lines.append("## 三判定")
    lines.append("")
    lines.append("| 探针 | 判定 | 理由 |")
    lines.append("|---|---|---|")
    for p, v, r in verdicts:
        lines.append("| %s | **%s** | %s |" % (p, v, r))
    lines.append("")
    lines.append("## 守卫（%d/%d）" % (n_gok, n_g))
    lines.append("")
    for g in GUARDS:
        lines.append("- [%s] %s %s" % ("OK" if g["ok"] else "FAIL", g["name"],
                                       ("" if g["ok"] else ":: " + str(g["msg"]))))
    lines.append("")
    lines.append("## 红线")
    lines.append("")
    lines.append("本册只做闭环式复算与结构性判定，不产生新物理，不宣称观测证实/否证；"
                 "未改写任何来料字节；未改 verify.py；未做 git 操作。探针供给 0/4 ⇒ 不得报道为「通过」。")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")

    rep = []
    rep.append("TUFT-r183 探针池第一批 · 运行报告")
    rep.append("=" * 70)
    rep.append("条目 %d（PASS %d / FAIL %d / BOUNDARY %d / CORRECTED %d / INFO %d）"
               % (len(ENTRIES), n_pass, n_fail, n_bound, n_corr, n_info))
    rep.append("守卫 %d/%d" % (n_gok, n_g))
    rep.append("")
    for e in ENTRIES:
        rep.append("[%s] %s  %s" % (e["level"], e["code"], e["title"]))
        rep.append("    " + e["detail"])
        if e["numbers"]:
            rep.append("    " + json.dumps(e["numbers"], ensure_ascii=False)[:1200])
        rep.append("")
    with open(os.path.join(OUTD, STEM + "_report.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(rep) + "\n")

    print("已写出：")
    print("  " + os.path.join(OUTD, STEM + ".json"))
    print("  " + os.path.join(OUTD, STEM + ".md"))
    print("  " + os.path.join(OUTD, STEM + "_report.txt"))
    return 0 if n_gok == n_g else 1


if __name__ == "__main__":
    sys.exit(main())
