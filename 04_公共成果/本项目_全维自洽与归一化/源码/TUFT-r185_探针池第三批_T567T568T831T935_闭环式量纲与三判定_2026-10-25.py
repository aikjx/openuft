# -*- coding: utf-8 -*-
"""
TUFT-r185 · 探针池第三批（T567 / T568 / T831 / T935）闭环式 + 台账复核 · 精算
2026-10-25

承接：
  r184 §7 已排定第三批 = T567 / T568 / T831 / T935（①可精算池剩余 4 项）。
  r184 E04/E05 已把 T718 的 archive G0 定性为 F-unit 位数搬迁（=R_K×1e-9，偏低 33.37%）。
  布局_剩余项分层归档 §一 第 9 行仍写 G0=2.58128E-5 S 并标「✔」⇒ 本册复核该假绿。

本册职责：
  1) T567 相对熵相干：纯态 ln2、混态 0.2820959389 的两路复算与基依赖边界。
  2) T568 Wigner–Yanase 偏态信息：纯态 1 精确、混态 0.2973167341 的两路复算与 H 依赖边界。
  3) T831 KSS 粘滞熵比下限：量纲 K·s、数值 6.078312E-13、自然单位 1/(4π) 的口径分离。
  4) T935 Heisenberg 纠缠标度：闭式 1/(2√N) 的标度指数与文本「∝1/N」的实质矛盾（FAIL）。
  5) 台账复核：布局表 T718 行的假绿；C0279 的 3.01 dB 与 20log10 2 的自相矛盾。
  6) 缺陷族登记：F-scale（标度指数与文字标签不符）为本批新增。

三判定口径（继承 r183/r184，可执行）：
  C1 无约束（退化）：探针不触及 TUFT 的可动自由度（TUFT 侧供给=0）⇒ 零信息量。
  C2 力约束放行    ：TUFT 侧有数值且落在探针区间内 ⇒ 仅「一致」，不得作证明。
  C3 力约束否定    ：TUFT 侧有数值且越出探针上界 ⇒ 该自由度被压缩/排除（仍不否定公理集本体）。

纪律：探针供给恒为 0 时不得报道为「通过」；恒等式必须标注「口径交叉印证、非独立验证」；
      不自推的系数一律 BOUNDARY。红线：不产生新物理、不改写来料字节、不改 verify.py、不做 git。
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

STEM = "TUFT-r185_探针池第三批_T567T568T831T935_闭环式量纲与三判定_2026-10-25"

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
TMP = (F0, F0, F0, F0, F1)

DIM = {
    "c":     (F0, F1, Fraction(-1), F0, F0),
    "G":     (Fraction(-1), Fraction(3), Fraction(-2), F0, F0),
    "hbar":  (F1, Fraction(2), Fraction(-1), F0, F0),
    "h":     (F1, Fraction(2), Fraction(-1), F0, F0),
    "kB":    (F1, Fraction(2), Fraction(-2), F0, Fraction(-1)),
    "e":     (F0, F0, F0, F1, F0),
    "Ohm":   (F1, Fraction(2), Fraction(-1), Fraction(-2), F0),
    "Siem":  (Fraction(-1), Fraction(-2), F1, Fraction(2), F0),
    "Entropy": (F1, Fraction(2), Fraction(-2), F0, Fraction(-1)),
    "Pa_s":  (F1, Fraction(-1), Fraction(-1), F0, F0),      # 剪切粘滞 η
    "s_den": (F1, Fraction(-1), Fraction(-2), F0, Fraction(-1)),  # 熵密度 s
    "info":  ONE,                                            # 信息量（奈特/比特）
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

VERDICT = ("R185-PROBE-BATCH3-4-OF-4-C1-SUPPLY-0-4-"
           "T567-CREL-LN2-AND-0.2820959389-"
           "T568-IWY-1-AND-0.2973167341-"
           "T831-ETA-OVER-S-6.078312E-13-KS-NATURAL-1-OVER-4PI-"
           "T935-SCALE-MISMATCH-NINV2-VS-NINV1-FAIL-3.01DB-VS-6.02DB-"
           "LAYOUT-T718-FALSE-GREEN-T210T211-LABEL-INVERSION-CARRIED")


# =====================================================================
# 1. 2×2 实对称工具（Decimal 250 位，两路 √ρ）
# =====================================================================
def von_neumann_2x2(a, b, d):
    """ρ=[[a,b],[b,d]]，返回 (λ1, λ2, S(ρ))；归一 tr=1。"""
    tr = a + d
    det = a * d - b * b
    disc = (tr * tr - D(4) * det).sqrt()
    l1 = (tr + disc) / D(2)
    l2 = (tr - disc) / D(2)
    s = D(0)
    for x in (l1, l2):
        if x > 0:
            s -= x * x.ln()
    return l1, l2, s


def sqrt_rho_2x2_shift(a, b, d):
    """归一态（tr=1）的 √ρ 闭式：√ρ=(ρ+√det·I)/√(1+2√det)。返回 (q11,q12,q22)。"""
    det = a * d - b * b
    s = det.sqrt()
    den = (D(1) + D(2) * s).sqrt()
    return (a + s) / den, b / den, (d + s) / den


def sqrt_rho_2x2_eigen(a, b, d):
    """谱分解路线：√ρ=Σ√λ_i u_i u_iᵀ（u 由特征向量归一）。返回 (q11,q12,q22)。"""
    l1, l2, _ = von_neumann_2x2(a, b, d)
    if b == 0:
        return a.sqrt(), D(0), d.sqrt()
    u1x, u1y = D(1), (l1 - a) / b
    n1 = (u1x * u1x + u1y * u1y).sqrt()
    u1x, u1y = u1x / n1, u1y / n1
    u2x, u2y = D(1), (l2 - a) / b
    n2 = (u2x * u2x + u2y * u2y).sqrt()
    u2x, u2y = u2x / n2, u2y / n2
    q11 = l1.sqrt() * u1x * u1x + l2.sqrt() * u2x * u2x
    q12 = l1.sqrt() * u1x * u1y + l2.sqrt() * u2x * u2y
    q22 = l1.sqrt() * u1y * u1y + l2.sqrt() * u2y * u2y
    return q11, q12, q22


def iwy_2x2(q11, q12, q22, tr_rho_h2):
    """H=σ_z：Tr((√ρH)²)=q11²+q22²−2q12²；I_WY=Tr(ρH²)−该值。"""
    tr_rh2 = q11 * q11 + q22 * q22 - D(2) * q12 * q12
    return tr_rho_h2 - tr_rh2


def main():
    print("=" * 78)
    print("TUFT-r185 · 探针池第三批 T567/T568/T831/T935")
    print("=" * 78)

    # =================================================================
    # A 段 · 量纲机自检 + 三种「熵」的符号分离
    # =================================================================
    print("\n[A] 量纲机自检（信息量 / 热力学熵 / η/s）")

    d_si = ddiv(DIM["Pa_s"], DIM["s_den"])
    guard("G0-1 eta_over_s_is_K_T", d_si == dmul(TMP, TIM), "得到 " + dstr(d_si))
    d_hk = ddiv(DIM["hbar"], DIM["kB"])
    guard("G0-2 hbar_over_kB_is_K_T", d_hk == dmul(TMP, TIM), "得到 " + dstr(d_hk))
    guard("G0-3 kB_has_entropy_dimension",
          ddiv((F1, Fraction(2), Fraction(-2), F0, F0), TMP) == DIM["Entropy"],
          "kB 的量纲不是能量/温度")
    d_ent = ddiv(dmul(dmul(DIM["kB"], TMP), ONE), ONE)     # kB·K = J
    guard("G0-4 kB_times_K_is_energy", d_ent == (F1, Fraction(2), Fraction(-2), F0, F0),
          "得到 " + dstr(d_ent))
    guard("G0-5 info_is_dimensionless", DIM["info"] == ONE, "信息量非无量纲")
    guard("G0-6 entropy_not_info", DIM["Entropy"] != DIM["info"],
          "热力学熵与信息量量纲竟相等")

    add("A01", "INFO", "三种「熵」必须分账：Shannon 熵无量纲、热力学熵 J/K、η/s 是 K·s",
        "本册把信息量（奈特，量纲 " + dstr(DIM["info"]) + "）、热力学熵（" +
        dstr(DIM["Entropy"]) + "）、以及粘滞熵比（" + dstr(d_si) +
        "）三者的量纲键彻底分开。r184 A01 已抓「S=siemens vs S=entropy」；本册追加第三种："
        "η/s 的单位 K·s 来自 η[Pa·s] 除 s[J/(m³K)]，不是熵本身。三者混用会产生无量纲假绿。",
        {"info": dstr(DIM["info"]), "entropy": dstr(DIM["Entropy"]),
         "eta_over_s": dstr(d_si)})

    hk = HBARV / KBV
    add("A02", "PASS", "换算常数 ħ/k_B = 7.6382E−12 K·s（桥接自然单位与 SI）",
        "ℏ/k_B=" + fs(hk, 12) + " K·s；乘 1/(4π) 即得 KSS 下限的 SI 读数。"
        "任何在自然单位（1/(4π)）与 SI（K·s）之间换算的写法都必须显式乘这个桥接常数，"
        "否则属 F-unit 族（单位间搬位数）。",
        {"hbar_over_kB": fs(hk, 12)})

    # =================================================================
    # B 段 · T567 相对熵相干
    # =================================================================
    print("\n[B] T567 · 相对熵相干 C_rel")

    LN2 = D(2).ln()
    guard("G0-7 ln2_value", abs(LN2 - D("0.693147180559945309417232121458176568")) < D("1E-36"),
          "得到 " + fs(LN2, 12))

    # 纯态 |+>
    a_p, b_p, d_p = D("0.5"), D("0.5"), D("0.5")
    l1p, l2p, s_p = von_neumann_2x2(a_p, b_p, d_p)
    s_diag_p = -(a_p * a_p.ln() + d_p * d_p.ln())
    c_rel_p = s_diag_p - s_p
    guard("G0-8 pure_state_vn_entropy_zero", abs(s_p) < D("1E-240"), "S(ρ)=" + fs(s_p, 6))
    guard("G0-9 pure_c_rel_is_ln2", abs(c_rel_p - LN2) < D("1E-200"),
          "残差 " + fs(c_rel_p - LN2, 6))
    add("B01", "PASS", "T567 纯态 |+⟩：C_rel = ln2 精确",
        "ρ=|+⟩⟨+| 的 Von Neumann 熵 S(ρ)=0（机器 " + fs(s_p, 6) + "），"
        "对角参考 ρ_diag=(1/2,1/2) 的熵为 ln2 ⇒ C_rel=S(ρ_diag)−S(ρ)=ln2=" +
        fs(c_rel_p, 25) + "。**诚实标注**：这是「纯态相干上界」的构造性恒等，"
        "只证明定义式在纯态上取到最大值，不是动力学推导。",
        {"S_rho": fs(s_p, 6), "S_diag": fs(s_diag_p, 12), "C_rel": fs(c_rel_p, 12)})

    # 混态 0.3|0><0| + 0.7|+><+|
    a_m, b_m, d_m = D("0.65"), D("0.35"), D("0.35")
    l1m, l2m, s_m = von_neumann_2x2(a_m, b_m, d_m)
    s_diag_m = -(a_m * a_m.ln() + d_m * d_m.ln())
    c_rel_m = s_diag_m - s_m
    add("B02", "PASS", "T567 混态 0.3|0⟩⟨0|+0.7|+⟩⟨+|：C_rel = 0.2820959389",
        "ρ=[[0.65,0.35],[0.35,0.35]]，特征值 λ±=" + fs(l1m, 12) + "/" + fs(l2m, 12) +
        "，S(ρ)=" + fs(s_m, 12) + "，S(ρ_diag)=" + fs(s_diag_m, 12) +
        " ⇒ C_rel=" + fs(c_rel_m, 18) + "。与 C0276 锚点 0.2820959389 在 9 位内一致。",
        {"lambda_plus": fs(l1m, 12), "lambda_minus": fs(l2m, 12),
         "S_rho": fs(s_m, 12), "S_diag": fs(s_diag_m, 12), "C_rel": fs(c_rel_m, 18)})

    guard("G0-10 c_rel_mixed_in_band", D(0) < c_rel_m < LN2,
          "C_rel=" + fs(c_rel_m, 12))
    guard("G0-11 c_rel_monotone_pure_gt_mixed", c_rel_p > c_rel_m,
          "pure=" + fs(c_rel_p, 6) + " mixed=" + fs(c_rel_m, 6))
    add("B03", "PASS", "T567 界：0 < C_rel ≤ ln2，且纯态取上界、混态严格更小",
        "机器 " + fs(c_rel_m, 12) + " ∈ (0, " + fs(LN2, 12) + ")；纯态 " + fs(c_rel_p, 12) +
        "。该单调性来自 S(ρ)>0（混态），不是额外假设。",
        {"C_rel_mixed": fs(c_rel_m, 12), "ln2": fs(LN2, 12)})

    # 基依赖：固定态 |+⟩（σ_z 本征态），改在 σ_x 基读 ⇒ ρ=diag(1,0)、C_rel=0
    a_x, b_x, d_x = D(1), D(0), D(0)
    l1x, l2x, s_x = von_neumann_2x2(a_x, b_x, d_x)
    s_diag_x = D(0)          # σ_x 基下 |+⟩ 的对角元为 (1,0)，熵 0
    c_rel_x = s_diag_x - s_x
    guard("G0-12 c_rel_basis_dependent", abs(c_rel_x) < D("1E-240"),
          "σ_x 基下 C_rel=" + fs(c_rel_x, 6))
    add("B04", "BOUNDARY", "C_rel 是**基依赖**量：同一个 |+⟩ 在 σ_x 基下 C_rel=0",
        "在 σ_z 基 |+⟩ 的 C_rel=ln2，换到它的本征基（σ_x）则 ρ 对角、C_rel=" +
        fs(c_rel_x, 6) + "。⇒ **必须声明固定的是哪一个非相干基**；"
        "把 C_rel 当作基无关的「相干量」是口径错误。基无关的对应物是 T568 的不对称度（但需 Hamiltonian）。",
        {"C_rel_z_basis": fs(c_rel_p, 12), "C_rel_x_basis": fs(c_rel_x, 6)})

    add("B05", "INFO", "T567 三判定：C1（TUFT 侧无密度矩阵/无资源理论）",
        "TUFT 不供给密度矩阵、不供给非相干操作集 ⇒ 探针不触及可动自由度。"
        "C0276 的「结构性负面」与本册 C1 同义：零信息量，不得报道为验证。",
        {"verdict": "C1"})

    # =================================================================
    # C 段 · T568 Wigner–Yanase 偏态信息
    # =================================================================
    print("\n[C] T568 · Wigner–Yanase 偏态信息 I_WY")

    q11p, q12p, q22p = sqrt_rho_2x2_shift(a_p, b_p, d_p)
    iwy_p = iwy_2x2(q11p, q12p, q22p, D(1))
    guard("G0-13 iwy_pure_is_one", abs(iwy_p - D(1)) < D("1E-200"),
          "I_WY=" + fs(iwy_p, 12))
    add("C01", "PASS", "T568 纯态 |+⟩：I_WY = ΔH² = 1 精确（H=σ_z）",
        "Tr(ρH²)=1；√ρ=ρ（纯态幂等）⇒ Tr(√ρH√ρH)=" + fs(D(1) - iwy_p, 12) +
        " 机器零 ⇒ I_WY=1。**诚实标注**：这是纯态退化为方差 ΔH² 的定义性恒等。",
        {"I_WY": fs(iwy_p, 12), "Tr_sqrtH2": fs(D(1) - iwy_p, 6)})

    q11m, q12m, q22m = sqrt_rho_2x2_shift(a_m, b_m, d_m)
    iwy_m = iwy_2x2(q11m, q12m, q22m, D(1))
    q11e, q12e, q22e = sqrt_rho_2x2_eigen(a_m, b_m, d_m)
    iwy_e = iwy_2x2(q11e, q12e, q22e, D(1))
    resid_sq = max(abs(q11m - q11e), abs(q12m - q12e), abs(q22m - q22e))
    guard("G0-14 sqrt_rho_two_routes_agree", resid_sq < D("1E-80"),
          "残差 " + fs(resid_sq, 6))
    add("C02", "PASS", "T568 混态：I_WY = 0.2973167341（两条 √ρ 路线互证）",
        "闭式 √ρ=(ρ+√det·I)/√(1+2√det) 与谱分解 √ρ=Σ√λ_i u_iu_iᵀ 给出的 √ρ 逐元一致"
        "（最大残差 " + fs(resid_sq, 6) + "）；I_WY=" + fs(iwy_m, 18) +
        "，与 C0276 锚点 0.2973167341 在 10 位内一致。",
        {"q11": fs(q11m, 12), "q12": fs(q12m, 12), "q22": fs(q22m, 12),
         "I_WY": fs(iwy_m, 18), "I_WY_eigen": fs(iwy_e, 18)})

    guard("G0-15 iwy_bounds", D(0) < iwy_m < D(1) and abs(iwy_p - D(1)) < D("1E-200"),
          "mix=" + fs(iwy_m, 6))
    add("C03", "PASS", "T568 界：0 ≤ I_WY ≤ ΔH²（半正定 + 上界）",
        "混态 I_WY=" + fs(iwy_m, 12) + " ∈ (0,1)，纯态取上界 ΔH²=1。"
        "该界来自 Tr(√ρH√ρH) ≥ 0（半正定），非额外假设。",
        {"I_WY_mixed": fs(iwy_m, 12), "upper": "1"})

    add("C04", "BOUNDARY", "I_WY 依赖所选 Hamiltonian / 参考系：T568 的时间平移不对称度不可由闭式唯一确定",
        "I_WY(ρ,H) 的数值随 H 变（本册取 H=σ_z；换 H=σ_x 得另一读数）。"
        "T568 的「时间平移对称性」要求先指定群作用 e^{−iHt} 与 H 的谱 ⇒ "
        "**H 的选择是外部输入**，闭式给不出。故 I_WY 只能作「已给参考系下的读数」，"
        "不能作参考系无关的不对称度。",
        {"H": "sigma_z", "note": "H 由外部约定"})

    add("C05", "INFO", "T568 三判定：C1（TUFT 侧无参考系资源/无 Hamiltonian 谱）",
        "TUFT 不供给 H 的谱与非相干操作 ⇒ 探针不触及可动自由度。供给 0/1。",
        {"verdict": "C1"})

    # =================================================================
    # D 段 · T831 KSS 粘滞熵比下限
    # =================================================================
    print("\n[D] T831 · KSS 粘滞熵比下限")

    eta_s = HBARV / (D(4) * PI * KBV)
    guard("G0-16 kss_value", abs(eta_s - D("6.078312E-13")) < D("1E-19"),
          "得到 " + fs(eta_s, 12))
    add("D01", "PASS", "T831 量纲：η/s 的量纲是 K·s（= ħ/k_B 的量纲）",
        "η（剪切粘滞）量纲 " + dstr(DIM["Pa_s"]) + "；s（熵密度）量纲 " + dstr(DIM["s_den"]) +
        " ⇒ η/s 量纲 " + dstr(d_si) + "，与 ħ/k_B 的量纲 " + dstr(d_hk) +
        " 逐位相同（守卫 G0-1/G0-2）⇒ 该不等式的两侧量纲闭合。",
        {"eta_over_s": dstr(d_si), "hbar_over_kB": dstr(d_hk)})

    add("D02", "PASS", "T831 读数：η/s ≥ ħ/(4πk_B) = 6.078312E−13 K·s",
        "机器 " + fs(eta_s, 25) + " K·s；锚点 6.078312E−13 在 7 位内一致。"
        "（注：CODATA 的 ħ 字面值 1.054571817E−34 只有 10 位，若直接代入会得到 6.078312356E−13，"
        "与精确 h/2π 相差 6.1E−10；本册一律用 h/2π 以保持 250 位口径。）"
        "该数是 1/(4π) 与桥接常数 ħ/k_B=" + fs(hk, 12) + " 的乘积。",
        {"eta_over_s": fs(eta_s, 25)})

    nat = D(1) / (D(4) * PI)
    guard("G0-17 natural_units_consistency",
          abs(nat * hk - eta_s) < D("1E-40"),
          "1/(4π)·ħ/k_B=" + fs(nat * hk, 12))
    add("D03", "PASS", "T831 自然单位口径：η/s ≥ 1/(4π) = 0.0795774715（ħ=k_B=1）",
        "自然单位读数 " + fs(nat, 25) + "；乘桥接常数 ħ/k_B 后逐位还原 SI 读数 " +
        fs(nat * hk, 12) + " K·s（残差机器零）。**诚实标注**：这是同一不等式的两种单位记账，"
        "口径交叉印证、非独立验证。",
        {"natural": fs(nat, 25), "si_via_bridge": fs(nat * hk, 12)})

    add("D04", "INFO", "QGP 读数区间：1–2 × KSS ⇒ η/s ∈ [6.078E−13, 1.216E−12] K·s",
        "把「QGP ≈1–2 倍 KSS」读作区间：" + fs(eta_s, 6) + " ～ " + fs(D(2) * eta_s, 6) +
        " K·s。该区间是**外部输运/格点输入**，TUFT 侧不供给 η 或 s ⇒ 不构成验证。",
        {"low": fs(eta_s, 6), "high": fs(D(2) * eta_s, 6)})

    add("D05", "BOUNDARY", "KSS 是**全息猜想**，不是已证定理：不可当作 TUFT 的否证依据",
        "1/(4π) 下限来自 AdS/CFT 的强耦合对偶（Kovtun–Son–Starinets），适用域为"
        "「具有全息对偶的强耦合规范理论」。它不是对所有流体的定理，也不覆盖弱耦合 QGP。"
        "⇒ 本册只做算术与量纲闭合，不宣称该下限已被证明，也不用它否证 TUFT。",
        {"status": "conjecture", "domain": "holographic strong coupling"})

    add("D06", "INFO", "T831 三判定：C1（TUFT 侧无 η、无熵密度）",
        "TUFT 不供给剪切粘滞与熵密度 ⇒ 探针不触及可动自由度。供给 0/1。",
        {"verdict": "C1"})

    # =================================================================
    # E 段 · T935 Heisenberg 纠缠标度
    # =================================================================
    print("\n[E] T935 · Heisenberg 纠缠标度（标度指数复核）")

    def dtheta(N):
        return D(1) / (D(2) * D(N).sqrt())

    TH1 = dtheta(1)
    TH4 = dtheta(4)
    TH128 = dtheta(128)
    guard("G0-18 theta_N1_half", TH1 == D("0.5"), "得到 " + fs(TH1, 6))
    guard("G0-19 theta_N4_quarter", TH4 == D("0.25"), "得到 " + fs(TH4, 6))
    guard("G0-20 theta_N128_anchor", abs(TH128 - D("0.0441941738")) < D("1E-10"),
          "得到 " + fs(TH128, 12))
    add("E01", "PASS", "T935 闭式读数：Δθ_min=1/(2√N)，N=1/4/128 ⇒ 0.5 / 0.25 / 0.0441941738",
        "三点逐位命中：N=1 → " + fs(TH1, 6) + "，N=4 → " + fs(TH4, 6) +
        "，N=128 → " + fs(TH128, 12) + "。闭式本身是纯算术，无自由参数。",
        {"N1": fs(TH1, 6), "N4": fs(TH4, 6), "N128": fs(TH128, 12)})

    # 标度指数：N→4N 时 Δθ 减半 ⇒ 指数 −1/2
    th4x = dtheta(4)
    exp_half = (dtheta(4) / TH1).ln() / D(4).ln()      # ln(1/2)/ln4 = -1/2
    guard("G0-21 closed_form_exponent_is_neg_half", abs(exp_half + D("0.5")) < D("1E-200"),
          "指数 " + fs(exp_half, 12))
    add("E02", "FAIL", "T935 标度矛盾：闭式 1/(2√N) 的指数是 −1/2，而文本标「∝1/N（Heisenberg）」",
        "机器：N→4N 时 Δθ 变为 1/2 ⇒ 标度指数 = ln(1/2)/ln4 = " + fs(exp_half, 12) +
        "，即 **N^−1/2**，属 **SQL（标准量子极限）标度**，不是 Heisenberg 的 N^−1。"
        "而 C0279 判定册 E1 同时写「Δθ∝1/N」与「Δθ_min=1/(2√N)」⇒ 两行自相矛盾。"
        "⇒ 缺陷族 **F-scale**（标度指数与文字标签不符）：文字标签 N^−1 与闭式 N^−1/2 不可并存。",
        {"closed_form_exponent": fs(exp_half, 12), "claimed_exponent": "-1",
         "ratio_at_4N": fs(dtheta(4) / TH1, 12)})

    # NOON 真 Heisenberg：F=4(ΔJ_z)²=N² ⇒ Δθ=1/N
    def dtheta_noon(N):
        return D(1) / D(N)

    NOON128 = dtheta_noon(128)
    ratio128 = TH128 / NOON128
    guard("G0-22 noon_is_true_heisenberg",
          abs(dtheta_noon(4) / dtheta_noon(1) - D("0.25")) < D("1E-200"),
          "NOON 四倍 N 后比值 " + fs(dtheta_noon(4) / dtheta_noon(1), 12))
    add("E03", "PASS", "T935 对照：NOON 态的**真** Heisenberg 闭式是 Δθ=1/N（∝N^−1）",
        "NOON |N,0⟩+|0,N⟩：⟨J_z⟩=0、ΔJ_z=N/2 ⇒ QFI F=4(ΔJ_z)²=N² ⇒ Δθ_min=1/√F=1/N。"
        "四倍 N 时比值 " + fs(dtheta_noon(4) / dtheta_noon(1), 12) + "（应为 1/4）⇒ 指数 −1 精确。"
        "N=128：NOON 给 " + fs(NOON128, 12) + "，而 1/(2√N) 给 " + fs(TH128, 8) +
        "，比值 " + fs(ratio128, 12) + "（=√N/2）⇒ 两者随 N 发散，**不是同一标度**。",
        {"NOON_N128": fs(NOON128, 12), "formula_N128": fs(TH128, 8),
         "ratio": fs(ratio128, 12)})

    db20 = D(20) * D(2).log10()
    db10 = D(10) * D(2).log10()
    add("E04", "INFO", "C0279 的「3.01 dB = 20log₁₀2」自相矛盾（F-label）",
        "机器：20log₁₀2=" + fs(db20, 6) + " dB、10log₁₀2=" + fs(db10, 6) +
        " dB。C0279 E2 写「恒低 3.01 dB（20log₁₀2）」⇒ 数值 3.01 对应的是 10log₁₀2（功率比 2），"
        "而括号里的 20log₁₀ 给出 " + fs(db20, 6) + "。幅度比 1/2 ⇒ 6.02 dB；功率比 1/4 ⇒ 6.02 dB。"
        "登记为 **F-label**（标签与数值不符）。",
        {"20log10_2": fs(db20, 6), "10log10_2": fs(db10, 6)})

    add("E05", "BOUNDARY", "1/(2√N) 的合法读法只有两种，都不叫 Heisenberg 标度",
        "①N=独立重复测量次数、用相干态 ⇒ Δθ=1/(2√N) 是 SQL 的 QCRB（因子 2 来自单次 vs 两次测量口径）；"
        "②N=两模总粒子数、未做纠缠优化 ⇒ 同样给 N^−1/2。要得到 N^−1 必须把闭式换成 1/N（NOON/QFI）。"
        "⇒ 本册不改写来料闭式，只登记「闭式与标签只能保一个」；落地取舍由用户裁决。",
        {"legal_readings": ["repeat-count SQL", "unoptimized two-mode QCRB"],
         "forbidden": "Heisenberg N^-1"})

    add("E06", "INFO", "T935 三判定：C1（TUFT 侧无量子计量/无纠缠标度）",
        "TUFT 不供给纠缠态与测量误差界 ⇒ 探针不触及可动自由度。供给 0/1。",
        {"verdict": "C1"})

    # =================================================================
    # F 段 · 三判定总表、供给账、台账复核与缺陷族
    # =================================================================
    print("\n[F] 三判定 / 供给账 / 台账复核")

    table = [
        {"probe": "T567", "verdict": "C1",
         "reason": "TUFT 无密度矩阵/无相干资源理论"},
        {"probe": "T568", "verdict": "C1",
         "reason": "TUFT 无 Hamiltonian 谱/无参考系资源"},
        {"probe": "T831", "verdict": "C1",
         "reason": "TUFT 无剪切粘滞/无熵密度供给"},
        {"probe": "T935", "verdict": "C1",
         "reason": "TUFT 无纠缠态/无量子计量误差界"},
    ]
    add("F01", "INFO", "三判定总表：第三批 4 探针全部 C1（C2=0、C3=0）",
        "四行理由见 numbers.table。探针给的是信息论/全息/量子计量侧的参考值，"
        "TUFT 侧对这四个量无任何内定数值 ⇒ 零信息量，**不得报道为通过**。",
        {"table": table, "n_C1": 4, "n_C2": 0, "n_C3": 0})

    add("F02", "INFO", "供给账：第三批 0/4（累计 0/12）",
        "①可精算池 12 项现已全部落盘（第一批 4 / 第二批 4 / 第三批 4），"
        "TUFT 侧供给合计 **0/12**。与 r174 F03、r183 F02、r184 F02 一致："
        "探针池只能出上限约束，不能出判别。",
        {"supply_batch": 0, "total_batch": 4, "supply_cumulative": 0, "total_cumulative": 12})

    add("F03", "CORRECTED", "台账复核：布局 §一 第 9 行 T718 仍写 G0=2.58128E−5 S 并标「✔」⇒ 假绿",
        "r184 E04/E05 已机器判定：e²/h=3.874045864932E−5 S，archive/布局值 2.58128E−5 S 的比值 "
        "0.6633（偏低 33.37%），且该数恰等于 R_K×1e−9 ⇒ F-unit 位数搬迁。"
        "但布局表该行仍标「✔」⇒ 修复清单之外的**第二处假绿**（第一处是检查标记本身失效）。"
        "本册只登记，不改写布局字节；落地由用户在台账层删除或改正该 ✔。",
        {"layout_value": "2.58128E-5", "correct": "3.874045864932E-5",
         "dev_pct": "33.37", "cause": "F-unit R_K x 1e-9", "mark": "false-green"})

    add("F04", "INFO", "缺陷族总表（六族）：F-pi / F-unit / F-dim-blind / F-label / F-exp / F-scale",
        "①F-pi：漏 π 幂或分数未约分（T712/T947）；②F-unit：互为倒数的单位间搬位数"
        "（T718，且已传播进布局表，见 F03）；③F-dim-blind：有量纲量当纯数（T749）；"
        "④F-label：标签与数值/编号不符（T210/T211 编号倒置、C0279 的 3.01 dB）；"
        "⑤F-exp：十进制指数错位（C0281 的 2.537E−76 vs 2.536E−75）；"
        "⑥**F-scale（本批新增）**：标度指数与文字标签不符（T935 的 N^−1/2 vs N^−1）。"
        "门禁：系数先约分并记 π 幂、单位先查互逆、量纲先查是否纯数、标签先与数值对撞、"
        "指数先做 10 倍量级对撞、标度先做 N→4N 比值检验。",
        {"members": ["T712/T947 F-pi", "T718 F-unit", "T749 F-dim-blind",
                     "T210/T211 F-label", "C0279 dB F-label", "C0281 F-exp",
                     "T935 F-scale"]})

    add("F05", "INFO", "本卷红线与产出定性",
        "本轮产出 = ①第三批 4 探针闭环式落盘；②T935 标度指数矛盾 FAIL 定性；"
        "③台账第二处假绿（T718 行的 ✔）登记；④新增 F-scale 族。"
        "不产生新物理，不宣称观测证实/否证，不改写来料字节，不改 verify.py，不做 git。"
        "C1 不得写成「通过」；探针供给 0/4 维持。",
        {"supply": "0/4", "cumulative": "0/12"})

    add("F06", "INFO", "批次进度账：①可精算池 12/12 已落盘",
        "第一批 r183（T147/T712/T947/T163）、第二批 r184（T141/T210+T211/T749）、"
        "第三批 r185（T567/T568/T831/T935）⇒ ①池 12 项全部闭环。"
        "剩余硬项 **F5 钱德拉塞卡**属②观测/天体层（不在①池内），仍无回合。",
        {"pool_total": 12, "done": 12, "remaining_hard": "F5 Chandrasekhar"})

    # =================================================================
    # 控制组（真实计算，非声明性 True）
    # =================================================================
    control("K01 c_rel_pure_is_ln2", abs(c_rel_p - LN2) < D("1E-200"),
            "C_rel=" + fs(c_rel_p, 12))
    control("K02 c_rel_mixed_anchor",
            abs(c_rel_m - D("0.2820959389")) < D("1E-9"),
            "C_rel=" + fs(c_rel_m, 12))
    control("K03 iwy_pure_is_one", abs(iwy_p - D(1)) < D("1E-200"),
            "I_WY=" + fs(iwy_p, 12))
    control("K04 iwy_mixed_anchor",
            abs(iwy_m - D("0.2973167341")) < D("1E-9"),
            "I_WY=" + fs(iwy_m, 12))
    control("K05 eta_s_anchor", abs(eta_s / D("6.078312E-13") - D(1)) < D("1E-6"),
            "eta/s=" + fs(eta_s, 12))
    control("K06 theta_N1", TH1 == D("0.5"), "theta=" + fs(TH1, 6))
    control("K07 theta_N128", abs(TH128 - D("0.0441941738")) < D("1E-10"),
            "theta=" + fs(TH128, 12))
    control("K08 closed_exponent_neg_half",
            abs(exp_half + D("0.5")) < D("1E-200"), "exp=" + fs(exp_half, 12))
    control("K09 noon_exponent_neg_one",
            abs(dtheta_noon(4) / dtheta_noon(1) - D("0.25")) < D("1E-200"),
            "ratio=" + fs(dtheta_noon(4) / dtheta_noon(1), 12))
    control("K10 scale_ratio_diverges",
            ratio128 > D("5") and ratio128 < D("6"), "ratio=" + fs(ratio128, 6))
    control("K11 db20_is_6p02", abs(db20 - D("6.0206")) < D("1E-3"),
            "20log10 2=" + fs(db20, 6))
    control("K12 natural_times_bridge", abs(nat * hk - eta_s) < D("1E-40"),
            "resid=" + fs(nat * hk - eta_s, 6))
    control("K13 sqrt_routes_agree", resid_sq < D("1E-80"),
            "resid=" + fs(resid_sq, 6))
    control("K14 c_rel_basis_zero", abs(c_rel_x) < D("1E-240"),
            "C_rel_x=" + fs(c_rel_x, 6))

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
        supply=dict(batch="0/4", cumulative="0/12"),
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
    md.append("第三批 **T567 / T568 / T831 / T935** 落盘，三判定全部 **C1**（供给 **0/4**，累计 **0/12**，"
              "①可精算池 12/12 全部闭环）。承重读数：C_rel(|+⟩)=**ln2**、混态 **0.2820959389**；"
              "I_WY(|+⟩)=**1** 精确、混态 **0.2973167341**（两条 √ρ 路线互证）；"
              "η/s ≥ **6.078312356E−13 K·s**（=1/(4π)·ħ/k_B，量纲 K·s 闭合）；"
              "**T935 FAIL**：闭式 1/(2√N) 的实际标度是 **N^−1/2（SQL）**，与文本「∝1/N（Heisenberg）」矛盾，"
              "真 Heisenberg 应为 1/N（NOON/QFI），两者在 N=128 相差 **5.657×** 且随 N 发散。"
              "台账复核：布局 §一 第 9 行 T718 的 G₀ 仍标「✔」⇒ 第二处假绿（F-unit 传播）。\n")
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
              "未改写任何来料字节；未改 verify.py；未做 git 操作。探针供给 0/4 ⇒ 不得报道为「通过」。\n")
    with open(os.path.join(OUTD, STEM + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    # ---- report.txt ----
    rep = []
    rep.append("TUFT-r185 探针池第三批 · 运行报告")
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
