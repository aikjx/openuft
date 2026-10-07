# -*- coding: utf-8 -*-
"""
S03-V18.9
来稿：GAQ-UFT V3.4「中微子振荡的拓扑场重联机制」（§1-§7，含分支 A/B/C 三选一）

编号说明：V18_7（加框可导出性）与 V18_8（分支三 CKM 起源）已由并行链占用，
          本册顺延为 V18_9；条目前缀同步为 V9-*，避免与 V18_8 内部的 V7-* 前缀混淆。
任务：(A) 对来稿 §1-§6 做自洽性与可否证性审计；(B) 对 §7 三条候选分支做可行性裁定；
      (C) 回答「是否直接往下推导三味耦合 PDE」。

纯标准库（math / cmath / decimal / sys / os / io），Python 3.8+
红线：本册全部为自洽性/可否证性裁定与标准物理事实的独立复算，
      不含任何对 GAQ 主张的正面支持证据。所有 PASS 仅指
      「该式在机器精度下自洽」或「外部事实被独立复算」。

输出：07_计算复现/运行记录/S03_V18_9_中微子振荡拓扑重联_审计与分支可行性报告.txt
"""

import sys
import os
import io
import math
import cmath
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PI = math.pi

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))      # 07_计算复现/源码
CALC = os.path.dirname(HERE)                            # 07_计算复现
SYSROOT = os.path.dirname(CALC)                         # S03_GAQ几何原子与作用量子
LOGDIR = os.path.join(CALC, "运行记录")
REPORT_NAME = "S03_V18_9_中微子振荡拓扑重联_审计与分支可行性报告.txt"

# ---------------------------------------------------------------------------
# 输出器
# ---------------------------------------------------------------------------
LINES = []
COUNTS = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0, "CORRECTED": 0}
ITEMS = []


def emit(text=""):
    LINES.append(text)


def rec(code, verdict, title):
    COUNTS[verdict] += 1
    ITEMS.append((code, verdict, title))
    emit("[%s] %s  %s" % (verdict, code, title))


def P(code, title):
    rec(code, "PASS", title)


def F(code, title):
    rec(code, "FAIL", title)


def B(code, title):
    rec(code, "BOUNDARY", title)


def I(code, title):
    rec(code, "INFO", title)


def C(code, title):
    rec(code, "CORRECTED", title)


def table(headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for k in range(len(headers)):
            widths[k] = max(widths[k], len(str(r[k])))
    fmt = " | ".join("{:<%d}" % w for w in widths)
    emit("  " + fmt.format(*headers))
    emit("  " + "-+-".join("-" * w for w in widths))
    for r in rows:
        emit("  " + fmt.format(*[str(x) for x in r]))


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    return ok


# ---------------------------------------------------------------------------
# 外部事实基准（CODATA / PDG-NuFIT 常用值；仅作对照，不作拟合）
# ---------------------------------------------------------------------------
HBARC = 1.973269804e-07          # eV*m  (hbar*c, CODATA 2018)
EV = 1.602176634e-19             # J
KCONV = 1.0 / (4.0 * HBARC * 1.0e9)   # phi = KCONV * dm2[eV^2] * L[m] / E[GeV]

DM21 = 7.42e-05                  # eV^2  (NuFIT 5.x / PDG 2024)
DM31 = 2.515e-03                 # eV^2  (正常序；来稿用旧值 2.43e-3)
DM31_OLD = 2.43e-03              # eV^2  来稿 §4 取值
S12SQ = 0.304
S13SQ = 0.02221
S23SQ = 0.573
DELTA_CP = 197.0 * PI / 180.0
M_NU_LIMIT = 0.45                # eV  (KATRIN 2024, 90% CL)
SUM_M_LIMIT = 0.12               # eV  (Planck+BAO 宇宙学上限)
N_EFF_SM = 3.044                 # SM 标准值
N_EFF_PLANCK = 2.99
N_EFF_SIGMA = 0.17


def phase_sm(dm2, L_m, E_gev):
    """SM 真空振荡相位 phi = dm2 c^4 L /(4 hbar c E)。dm2[eV^2], L[m], E[GeV]"""
    return dm2 * L_m / (4.0 * HBARC * E_gev * 1.0e9)


def prob_two_flavor(dm2, L_m, E_gev, theta):
    """两味真空概率 sin^2(2θ) sin^2(Δm^2 L /(4E))。"""
    return (math.sin(2.0 * theta) ** 2) * (math.sin(phase_sm(dm2, L_m, E_gev)) ** 2)


def prob_gaq_code(dm2, L_m, E_gev, theta):
    """来稿 §4 代码原样：phase = dm2 * L /(4*E)，L 以 m 计、E 以 GeV 计。"""
    ph = dm2 * L_m / (4.0 * E_gev)
    return (math.sin(2.0 * theta) ** 2) * (math.sin(ph) ** 2)


# ---------------------------------------------------------------------------
# PMNS 与三味精确概率（真空）
# ---------------------------------------------------------------------------
def pmns(s12sq, s13sq, s23sq, delta):
    s12 = math.sqrt(s12sq)
    c12 = math.sqrt(1.0 - s12sq)
    s13 = math.sqrt(s13sq)
    c13 = math.sqrt(1.0 - s13sq)
    s23 = math.sqrt(s23sq)
    c23 = math.sqrt(1.0 - s23sq)
    e = cmath.exp(1j * delta)
    ec = e.conjugate()
    return [
        [c12 * c13, s12 * c13, s13 * ec],
        [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13],
    ]


def prob_three(U, a, b, dm21, dm31, L_m, E_gev):
    """P(nu_a -> nu_b)：A = Σ_i U[bi] conj(U[ai]) exp(-i m_i^2 L /(2E))。"""
    p21 = 2.0 * phase_sm(dm21, L_m, E_gev)
    p31 = 2.0 * phase_sm(dm31, L_m, E_gev)
    ph = (0.0, p21, p31)
    amp = 0j
    for i in range(3):
        amp += U[b][i] * (U[a][i].conjugate()) * cmath.exp(-1j * ph[i])
    return abs(amp) ** 2


# ---------------------------------------------------------------------------
# 高精度（decimal）工具：π 用 Machin 公式算，不硬编码
# ---------------------------------------------------------------------------
DPREC = 260


def d_pi():
    old = getcontext().prec
    getcontext().prec = DPREC + 25

    def atan_inv(x):
        x = Decimal(x)
        total = Decimal(0)
        term = Decimal(1) / x
        x2 = x * x
        n = 0
        lim = Decimal(10) ** (-(DPREC + 12))
        while True:
            t = term / Decimal(2 * n + 1)
            total += t if n % 2 == 0 else -t
            term = term / x2
            n += 1
            if abs(t) < lim:
                break
        return total

    val = 16 * atan_inv(5) - 4 * atan_inv(239)
    getcontext().prec = old
    return +val


PI_D = d_pi()


def dsin(x):
    """Decimal 正弦：先模 2π 归约，再用三象限对称化到 |x|<=π/2，泰勒展开。"""
    getcontext().prec = DPREC
    two = Decimal(2)
    tp = two * PI_D
    x = Decimal(x)
    n = int((x / tp).to_integral_value(rounding="ROUND_HALF_EVEN"))
    x = x - Decimal(n) * tp
    half = PI_D / two
    if x > half:
        x = PI_D - x
    elif x < -half:
        x = -PI_D - x
    total = Decimal(0)
    term = x
    k = 0
    lim = Decimal(10) ** (-(DPREC + 5))
    while True:
        total += term
        k += 1
        term = -term * x * x / Decimal((2 * k) * (2 * k + 1))
        if abs(term) < lim:
            break
    return +total


def dsin2(x):
    s = dsin(x)
    return s * s


# ---------------------------------------------------------------------------
# 圆螺旋几何（承接 V18_5 / V18_6）
# ---------------------------------------------------------------------------
def helix_geom(R, a, T):
    """r(t)=(R cos t, R sin t, a t)：kappa, tau, ds/dt, ∫τ ds, ∫τκ ds（沿 t∈[0,T]）。"""
    den = R * R + a * a
    kappa = R / den
    tau = a / den
    dsdt = math.sqrt(den)
    int_tau_ds = tau * dsdt * T
    int_tau_kappa_ds = tau * kappa * dsdt * T
    return kappa, tau, dsdt, int_tau_ds, int_tau_kappa_ds


def m_from_geom(kappa, tau):
    """GAQ 既有口径 m = (hbar/c) sqrt(kappa^2+tau^2)；返回 w = sqrt(k^2+t^2) [1/m]。"""
    return math.sqrt(kappa * kappa + tau * tau)


# ===========================================================================
emit("=" * 78)
emit("S03-V18.9  GAQ-UFT V3.4 中微子振荡（拓扑场重联）来稿审计与分支可行性裁定")
emit("=" * 78)
emit("")
emit("来稿七节：§1 前置公理 / §2 振荡几何起源 / §3 概率场论式 / §4 数值框架 /")
emit("          §5 预言 / §6 缺口 / §7 分支 A(三味PDE+FDTD) B(Berry不变量) C(宇宙学退耦)")
emit("")
emit("红线：本册不给出任何对 GAQ 主张的正面支持证据；PASS 仅指「自洽」或「外部事实复算」。")
emit("")

# ===========================================================================
# 第 1 节 实现验证器（先校准工具，再判来稿）
# ===========================================================================
emit("-" * 78)
emit("第 1 节  实现验证器（自检）")
emit("-" * 78)
emit("")

# SC1：π 的 260 位（Machin 自算）与 math.pi 一致
d_pi_diff = abs(float(PI_D) - PI)
check("SC1 Decimal 自算 π 与 math.pi 一致", d_pi_diff < 1e-15, "差 %.3e" % d_pi_diff)

# SC2：换算系数 KCONV 与经验系数 1.267 的一致性
k_emp = 1.267e-3
check("SC2 相位换算系数（SI 严格式 vs 经验式 1.267）",
      abs(KCONV - k_emp) / k_emp < 1e-3,
      "SI %.6e vs 经验 %.6e，相对差 %.3e" % (KCONV, k_emp, abs(KCONV - k_emp) / k_emp))

# SC3：三味概率归一性
U0 = pmns(S12SQ, S13SQ, S23SQ, DELTA_CP)
worst_norm = 0.0
for Lm in (1.0e3, 2.95e5, 1.3e7, 1.5e11):
    for Eg in (0.001, 1.0, 10.0):
        for a in range(3):
            s = sum(prob_three(U0, a, b, DM21, DM31, Lm, Eg) for b in range(3))
            worst_norm = max(worst_norm, abs(s - 1.0))
check("SC3 三味概率归一 Σ_b P(a→b)=1", worst_norm < 1e-12, "最大偏差 %.3e" % worst_norm)

# SC4：三味在 θ13→0 且 Δm21→0 时退化为两味
U2 = pmns(S12SQ, 1e-12, S23SQ, 0.0)
worst_two = 0.0
for Lm in (1.0e4, 2.95e5, 1.0e6, 5.0e6):
    p3 = 1.0 - prob_three(U2, 1, 1, 1e-14, DM31, Lm, 1.0)
    th23 = math.asin(math.sqrt(S23SQ))
    p2 = prob_two_flavor(DM31, Lm, 1.0, th23)
    worst_two = max(worst_two, abs(p3 - p2))
check("SC4 θ13→0/Δm21→0 时三味退化为两味", worst_two < 1e-9,
      "最大偏差 %.3e" % worst_two)

# SC5：Decimal(260) 的 sin² 与 float 一致
worst_hp = 0.0
for ph in (0.1, 0.7853981, 1.5707963, 3.1415926, 12.7):
    v_hp = float(dsin2(Decimal(repr(ph))))
    v_fl = math.sin(ph) ** 2
    worst_hp = max(worst_hp, abs(v_hp - v_fl))
check("SC5 Decimal(260) sin² 与 float 一致", worst_hp < 1e-14, "最大偏差 %.3e" % worst_hp)

# SC6：∫τ ds 尺度不变性复现（承接 V18_6 SC6）
rows = []
base = None
for lam in (1.0, 2.0, 5.0, 10.0, 100.0):
    k_, t_, _, it_, _ = helix_geom(1.0 * lam, 0.3 * lam, 2.0 * PI)
    if base is None:
        base = it_
    rows.append((lam, "%.10e" % k_, "%.10e" % t_, "%.12f" % it_, "%.3e" % abs(it_ - base)))
maxdev = max(float(r[4]) for r in rows)
check("SC6 ∫τ ds 尺度不变（复现 V18_6 SC6）", maxdev < 1e-9, "最大偏差 %.3e" % maxdev)

table(["缩放 λ", "曲率 κ", "挠率 τ", "∫τ ds", "与 λ=1 之差"], rows)
emit("")
emit("  SC1-SC6 全部校准后，下面的判定才有效。")
emit("")

# ===========================================================================
# 第 2 节  V9-a：来稿 §4 数值框架的单位错误（硬错）
# ===========================================================================
emit("-" * 78)
emit("第 2 节  来稿 §4 代码缺 ℏc 换算 ⇒ 振荡长度错 197.36 倍")
emit("-" * 78)
emit("")
emit("  来稿 §4 原样：phase = dm2 * L /(4*E)，其中 dm2 [eV^2]、L [m]、E [GeV]。")
emit("  SI 严格式：phi = dm2 c^4 L /(4 hbar c E) = KCONV * dm2 * L[m] / E[GeV]，")
emit("  KCONV = 1/(4*hbar c*1e9) = %.6e。" % KCONV)
emit("  来稿式相对 SI 式的相位倍数 = (1/4)/KCONV = %.4f。" % ((0.25) / KCONV))
emit("")

rows = []
ratios = []
for label, dm2, Eg in (("Δm²_21 @ 1 MeV（反应堆）", DM21, 0.001),
                       ("Δm²_31 @ 0.6 GeV（T2K）", DM31, 0.6),
                       ("Δm²_31 @ 1 GeV（大气）", DM31, 1.0),
                       ("Δm²_21 @ 10 MeV（太阳）", DM21, 0.01)):
    # 第一振荡极大：phi = pi/2
    L_si = (PI / 2.0) * Eg / (KCONV * dm2)
    L_gaq = (PI / 2.0) * 4.0 * Eg / dm2
    ratios.append(L_si / L_gaq)
    rows.append((label, "%.4e" % dm2, "%.3f" % Eg,
                 "%.4e" % L_si, "%.4e" % L_gaq, "%.6f" % (L_si / L_gaq)))
table(["基线", "Δm² [eV²]", "E [GeV]", "SI 正确第一极大 [m]", "来稿式 [m]", "比值"], rows)
emit("")

ratio_exact = (0.25) / KCONV
check("SC7 来稿式/正确式的相位倍数与解析值一致",
      all(abs(x - ratio_exact) / ratio_exact < 1e-12 for x in ratios),
      "解析 %.6f，实测 %d 条基线最大相对差 %.2e"
      % (ratio_exact, len(ratios),
         max(abs(x - ratio_exact) / ratio_exact for x in ratios)))
emit("  来稿 §4 的曲线把振荡长度压小 %.2f 倍（相位放大同倍数）。" % ratio_exact)
emit("  后果：§4 声称的『弱场真空极限 GAQ 公式完全还原 SM 两味振荡概率』")
emit("  **从未被该代码实际检验过**——它算出的曲线不是 SM 曲线。")
emit("")
F("V9-a", "来稿 §4 数值框架缺 ℏc 换算，振荡长度错 %.2f 倍；『已还原 SM』的声称未获检验" % ratio_exact)
emit("      射程：纯单位错误，可修复（乘 KCONV 即可）；但修复前 §4 的一切数值结论无效。")
emit("")

# ===========================================================================
# 第 3 节  V9-b：Φ_B = ∮τ ds 与 SM 相位的标度冲突（核心二难）
# ===========================================================================
emit("-" * 78)
emit("第 3 节  来稿 §2 的几何相位 Φ_B = ∮τ ds 与 SM 相位不相容（核心二难）")
emit("-" * 78)
emit("")
emit("  SM 相位 phi_SM = Δm^2 c^4 L /(4 hbar c E) ∝ L/E；")
emit("  来稿 Φ_B = ∮τ ds，τ 是构型几何量（V18_6 SC6 已证 ∫τ ds 无量纲且尺度不变），")
emit("  沿世界线积分给 Φ_B = τ * s ∝ L，**与能量 E 无关**。")
emit("")

# 取一个代表性构型：m_nu = 0.05 eV 的康普顿波长倒数
m_nu = 0.05
lam_c = HBARC / m_nu          # hbar/(m c) = hbar c /(m c^2) [m]
tau_nu = 1.0 / lam_c
emit("  取 m_nu = %.3f eV ⇒ 康普顿波长 λ_C = hbar c /(m c^2) = %.4e m，" % (m_nu, lam_c))
emit("  对应构型挠率量级 τ_nu ~ 1/λ_C = %.4e 1/m。" % tau_nu)
emit("")

rows = []
for Eg in (0.5, 1.0, 2.0, 5.0, 10.0):
    Lm = 2.95e5
    p_sm = phase_sm(DM31, Lm, Eg)
    p_gaq = tau_nu * Lm
    rows.append(("T2K 295 km", "%.2f" % Eg, "%.6e" % p_sm, "%.6e" % p_gaq,
                 "%.3e" % (p_gaq / p_sm)))
for Lm in (1.0e3, 1.0e5, 2.95e5, 1.3e7):
    p_sm = phase_sm(DM31, Lm, 1.0)
    p_gaq = tau_nu * Lm
    rows.append(("%.1e m" % Lm, "1.00", "%.6e" % p_sm, "%.6e" % p_gaq,
                 "%.3e" % (p_gaq / p_sm)))
table(["基线", "E [GeV]", "φ_SM", "Φ_B = τ·L", "Φ_B/φ_SM"], rows)
emit("")

# E 依赖性检验：比值是否恒定
r_list = [tau_nu * 2.95e5 / phase_sm(DM31, 2.95e5, Eg) for Eg in (0.5, 1.0, 2.0, 5.0, 10.0)]
spread = (max(r_list) - min(r_list)) / (sum(r_list) / len(r_list))
check("SC8 Φ_B/φ_SM 随 E 显著变化（标度冲突）", spread > 1.0,
      "相对展布 %.3f（若标度相容应≈0）" % spread)
emit("  Φ_B/φ_SM 在 E=0.5→10 GeV 上变化 %.2f 倍 ⇒ 两者标度不同（∝L vs ∝L/E）。" %
     (max(r_list) / min(r_list)))
emit("")
emit("  **二难（本册核心裁定）**：")
emit("    (i) 若 τ 与 E 无关（几何量的定义），则 Φ_B ∝ L 不含 1/E ⇒ 不能还原 SM 相位，")
emit("        §4 的『弱场极限完全还原 SM』不成立；")
emit("    (ii) 若允许 τ = τ(E) 以吸收 1/E，则 τ 成为自由函数 ⇒ 对任意观测恒可拟合，")
emit("         §2 的相位公式不可证伪（与 V18.1 P1 / V18.6 V6-j 同族失败模式）。")
emit("  两条路都不给 GAQ 带来可检验内容。")
emit("")
F("V9-b", "Φ_B=∮τ ds 与 SM 相位标度冲突（∝L vs ∝L/E），且陷入『不可还原／不可证伪』二难")
emit("      射程：否定的是 §2 用几何相位**替代**质量相位项这一具体替换，")
emit("      不否定几何相位本身可作为附加相位存在（但那需先给耦合系数）。")
emit("")

# ===========================================================================
# 第 4 节  V9-c：§3 的 Δm² ∝ ∫(τκ) 差 与既有质量口径冲突（标度指数 1 vs 2）
# ===========================================================================
emit("-" * 78)
emit("第 4 节  来稿 §3 的 Δm² ∝ ∫(τ₂κ₂ − τ₁κ₁) ds 与既有质量口径冲突")
emit("-" * 78)
emit("")
emit("  既有 GAQ 口径（V18_5 采用、V18_2 复核）：m = (hbar/c) sqrt(κ^2+τ^2)")
emit("      ⇒ Δm²_ij ∝ (κ_i^2+τ_i^2) − (κ_j^2+τ_j^2)   —— 平方和之差")
emit("  来稿 §3：Δm² ∝ ∫(τ₂κ₂ − τ₁κ₁) ds               —— 乘积之差")
emit("  两者一般不等；更决定性的是**标度指数不同**。")
emit("")

rows = []
prev = None
for lam in (1.0, 2.0, 5.0, 10.0, 100.0):
    # 构型 1：R=1.0, a=0.30；构型 2：R=1.4, a=0.55（整体按 λ 缩放）
    k1, t1, ds1, _, itk1 = helix_geom(1.0 * lam, 0.30 * lam, 2.0 * PI)
    k2, t2, ds2, _, itk2 = helix_geom(1.4 * lam, 0.55 * lam, 2.0 * PI)
    # 读法 A：积分域随曲线缩放（沿各自的完整周期 T=2π）
    d_prod = itk2 - itk1
    d_sumsq = (k2 * k2 + t2 * t2) - (k1 * k1 + t1 * t1)
    if prev is None:
        prev = (d_prod, d_sumsq)
    rows.append((lam, "%.6e" % d_prod, "%.6e" % d_sumsq,
                 "%.6e" % (d_prod / d_sumsq),
                 "%.4f" % (prev[0] / d_prod), "%.4f" % (prev[1] / d_sumsq)))
table(["λ", "读法A ∫(τκ)差 ds", "平方和之差", "比值", "乘积差 ∝ λ^?", "平方和差 ∝ λ^?"], rows)
emit("")

# 标度指数拟合
import_stat = []
for lam in (1.0, 2.0, 5.0, 10.0):
    k1, t1, ds1, _, itk1 = helix_geom(1.0 * lam, 0.30 * lam, 2.0 * PI)
    k2, t2, ds2, _, itk2 = helix_geom(1.4 * lam, 0.55 * lam, 2.0 * PI)
    import_stat.append((math.log(lam), math.log(abs(itk2 - itk1)),
                        math.log(abs((k2 * k2 + t2 * t2) - (k1 * k1 + t1 * t1)))))
# 用两点估计幂指数
x1, y1a, y1b = import_stat[0]
x2, y2a, y2b = import_stat[-1]
pow_prod = (y2a - y1a) / (x2 - x1)
pow_sumsq = (y2b - y1b) / (x2 - x1)
check("SC9 读法 A 下 ∫(τκ)差 与 平方和差 的标度指数不同",
      abs(pow_prod - pow_sumsq) > 0.5,
      "∫(τκ)差 ∝ λ^%.3f，平方和差 ∝ λ^%.3f" % (pow_prod, pow_sumsq))
emit("  读法 A（积分域随曲线缩放）：∫(τκ)差 ∝ λ^%.3f，而 m² 差 ∝ λ^%.3f" % (pow_prod, pow_sumsq))
emit("  ⇒ 同一条曲线整体放大 λ 倍，两种口径给出**不同的质量谱变换律**（指数 1 vs 2）。")
emit("")
emit("  读法 B（积分域取固定弧长 S₀，不随 λ 缩放）：∫τκ ds ∝ λ^-2，与 m² 差同标度，")
emit("  但积分值依赖外加的 S₀ ⇒ 多引入一个外加长度尺度（合流 V18_3 的『外加尺度初值』）。")
emit("")
B("V9-c-r", "来稿 §3 未声明 ∫...ds 的积分域 ⇒ 两种读法给出不同标度（λ^-1 vs λ^-2）")
emit("      读法 A 与既有质量口径**标度指数冲突（1 vs 2）**；读法 B 虽同标度但须外加弧长尺度。")
emit("      此为口径歧义，须来稿显式声明后才能判定，故不直接计 FAIL。")
emit("")
F("V9-c", "§3 的 Δm² 表达式与既有质量口径 m=(ℏ/c)√(κ²+τ²) 冲突（乘积差 vs 平方和差）")
emit("      射程：这是**来稿内部与既有裁定**的冲突；修复方式是二选一并声明，")
emit("      与 C0041（质量量纲封锁）同源但落点不同：C0041 是量纲，本条是标度指数与形式。")
emit("")

# ===========================================================================
# 第 5 节  V9-d：参数账与恒可拟合（自由度过量 + 3 个零信息方向）
# ===========================================================================
emit("-" * 78)
emit("第 5 节  三味参数账：自由度 ≥ 11 对约束 6，且含 3 个零信息方向")
emit("-" * 78)
emit("")
emit("  既有口径下 m_i = (hbar/c) w_i，w_i = sqrt(κ_i^2+τ_i^2) [1/m]。")
emit("  给定外加质量锚 m_1 与实测 Δm^2，则 w_i 全部确定：")
emit("      m_i = sqrt(m_1^2 + Δm^2_i1)，w_i = m_i /(hbar c)")
emit("  但 (κ_i, τ_i) 在此约束下仍可在半径 w_i 的圆周上**任意**取（角度自由）：")
emit("      τ_i = r_i w_i，κ_i = w_i sqrt(1 − r_i^2)，r_i ∈ (0,1)")
emit("  ⇒ 每个构型有 1 个不改变任何质量观测值的连续自由度 ⇒ **3 个零信息方向**。")
emit("")


def build_configs(m1, dm21, dm31, r_list):
    ms = [m1, math.sqrt(m1 * m1 + dm21), math.sqrt(m1 * m1 + dm31)]
    ws = [x / HBARC for x in ms]
    out = []
    for w, r in zip(ws, r_list):
        out.append((w * math.sqrt(max(0.0, 1.0 - r * r)), w * r))
    return out, ms


def dm2_from_configs(cfg):
    ws = [m_from_geom(k, t) for k, t in cfg]
    ms = [x * HBARC for x in ws]
    return ms[1] ** 2 - ms[0] ** 2, ms[2] ** 2 - ms[0] ** 2


m1_anchor = 0.01   # eV，外加质量锚（V18_3 已判质量标度为公设边界，此处显式承担）
rows = []
worst_fit = 0.0
rng_state = 12345


def lcg():
    """纯标准库伪随机（避免依赖 random 的跨版本序列差异）。"""
    global rng_state
    rng_state = (1103515245 * rng_state + 12345) % (2 ** 31)
    return rng_state / float(2 ** 31)


for trial in range(5):
    r_list = [0.05 + 0.9 * lcg() for _ in range(3)]
    cfg, ms = build_configs(m1_anchor, DM21, DM31, r_list)
    d21c, d31c = dm2_from_configs(cfg)
    e21 = abs(d21c - DM21) / DM21
    e31 = abs(d31c - DM31) / DM31
    worst_fit = max(worst_fit, e21, e31)
    rows.append(("第 %d 组" % (trial + 1),
                 "%.3f / %.3f / %.3f" % tuple(r_list),
                 "%.6e" % d21c, "%.6e" % d31c, "%.2e" % max(e21, e31)))
table(["随机构型", "r₁ / r₂ / r₃", "Δm²_21 复算", "Δm²_31 复算", "相对残差"], rows)
emit("")
check("SC10 任意随机 r 组都能精确复现目标 Δm²（恒可拟合）", worst_fit < 1e-12,
      "最大相对残差 %.3e" % worst_fit)
emit("  5 组随机 (κ,τ) 全部机器零复现目标 Δm^2 ⇒ 质量侧对 (κ,τ) 只约束 3 个组合量 w_i，")
emit("  余下 3 个方向是**零信息**的。")
emit("")

# 冗余方向的显式演示
cfgA, _ = build_configs(m1_anchor, DM21, DM31, (0.20, 0.50, 0.80))
cfgB, _ = build_configs(m1_anchor, DM21, DM31, (0.60, 0.30, 0.90))
same_m = all(abs(m_from_geom(a[0], a[1]) - m_from_geom(b[0], b[1])) /
             m_from_geom(a[0], a[1]) < 1e-12 for a, b in zip(cfgA, cfgB))
diff_geom = max(abs(a[0] - b[0]) / a[0] + abs(a[1] - b[1]) / a[1]
                for a, b in zip(cfgA, cfgB))
table(["构型", "κ₁", "τ₁", "κ₂", "τ₂", "κ₃", "τ₃"],
      [("A (r=0.2/0.5/0.8)",) + tuple("%.6e" % v for v in
                                       (cfgA[0][0], cfgA[0][1], cfgA[1][0], cfgA[1][1], cfgA[2][0], cfgA[2][1])),
       ("B (r=0.6/0.3/0.9)",) + tuple("%.6e" % v for v in
                                       (cfgB[0][0], cfgB[0][1], cfgB[1][0], cfgB[1][1], cfgB[2][0], cfgB[2][1]))])
emit("")
emit("  A、B 两组 κ/τ 完全不同（κ 与 τ 的相对差之和最大 %.3f），但 w_i 全同（相对差 < 1e-12）"
     % diff_geom)
emit("  ⇒ 所有质量类观测量相同，而构型本身不同 ⇒ 存在 3 维不可识别方向。")
check("SC11 不同 (κ,τ) 给出相同质量谱（冗余方向存在）", same_m and diff_geom > 0.1,
      "质量一致=%s，几何相对差 %.3f" % (same_m, diff_geom))
emit("")

rows = [
    ("实测约束（观测量）", "2×Δm² + 3×θ + 1×δ_CP", "6"),
    ("GAQ 几何参数", "3 构型 ×(κ,τ)", "6"),
    ("重联耦合（若为酉矩阵）", "3 角 + 1 Dirac 相位", "4"),
    ("质量标度锚", "m₁ 外加（V18_3 判为公设边界）", "1"),
    ("合计自由参数", "", "≥ 11"),
    ("其中零信息方向", "r₁,r₂,r₃（+2 个 Majorana 相位不可观测）", "≥ 3"),
]
table(["参数账项", "内容", "数目"], rows)
emit("")
emit("  约束 6、参数 ≥ 11、冗余 ≥ 3 ⇒ 对**任意** PMNS 参数组合恒存在 (κ,τ,耦合) 解")
emit("  ⇒ 该构造不可证伪（与 V18.1 P1、V18.2 V2-e、V18.6 V6-j 同族，本族第 4 次）。")
emit("")
F("V9-d", "三味参数账不过约束：参数 ≥11 对约束 6 且含 3 个零信息方向 ⇒ 恒可拟合、不可证伪")
emit("      射程：否定的是『当前形式的三味重联构造』，不是『中微子有几何构型』这一想法本身；")
emit("      若要复活，须先给 (a) τ_i 的独立定义、(b) 混合角的第一性表达式，使自由度降到 ≤ 6。")
emit("")
emit("  【与并行链 V18_8（分支三 CKM，S03-C0045..C0053）的口径对照，防误读为冲突】")
emit("  V18_8 C0047 判『体系内无量纲连续自由度仅 1（κ/τ），CKM 需 4 个 ⇒ 缺 3』；")
emit("  本册说『参数 ≥11』。二者不矛盾，因计数对象不同：")
emit("    - 本册的 (κ_i,τ_i) 共 6 个是**有量纲**量（1/m），其模长 w_i 承载质量，")
emit("      而质量标度按 V18_3 是**外加**公设 ⇒ 有量纲侧不产生预测，只产生拟合能力；")
emit("    - 若按 V18_8 的口径只数**无量纲**自由度，则每个构型仅 κ_i/τ_i 一个比值，")
emit("      共 3 个，加上重联耦合的 4 个无量纲参数 = 7，对无量纲观测量（3 角 + 1 相位 = 4）")
emit("      ⇒ 仍然过约束不成立，结论一致：**恒可拟合**。")
emit("  ⇒ 两条链从『有量纲模长』与『无量纲比值』两侧给出同一结论，互为交叉印证；")
emit("  且本册的 3 个零信息方向（r_i）正是『有量纲模长外加、无量纲比值自由』的直接后果。")
emit("")

# ===========================================================================
# 第 6 节  V9-e：最轻态质量 → 0 时构型退化为直线（零质量态张力）
# ===========================================================================
emit("-" * 78)
emit("第 6 节  m₁ → 0 极限下最轻态构型退化为直线（内部张力）")
emit("-" * 78)
emit("")
emit("  振荡实验只测 Δm^2，允许最轻态严格 m₁ = 0（正常序）。既有口径 m ∝ sqrt(κ^2+τ^2)：")
emit("      m₁ = 0 ⇒ κ₁ = τ₁ = 0 ⇒ 曲率挠率全零 ⇒ 场线是**直线**，无螺旋、无缠绕。")
emit("  但来稿 §1 要求「三种稳定的螺旋缠绕拓扑构型」、§5-2 称「缠绕数是唯一的本征标记」。")
emit("")
rows = []
for m1t in (0.0, 1.0e-04, 1.0e-03, 1.0e-02, 0.05):
    w1 = m1t / HBARC
    rows.append(("m₁ = %.5f eV" % m1t, "%.4e" % w1,
                 "直线（κ=τ=0）" if w1 == 0 else "λ_C = %.4e m" % (1.0 / w1)))
table(["最轻态质量", "w₁ = m₁/(ℏc) [1/m]", "构型含义"], rows)
emit("")
emit("  严格 m₁ = 0 时该态既无螺旋也无缠绕数 ⇒ 与「三种不同螺旋缠绕构型」不相容；")
emit("  且按 V18_6 V6-c/V6-e，无加框的直线/平面曲线没有 Lk ⇒ 「缠绕数唯一本征标记」对该态失效。")
emit("")
B("V9-e", "m₁=0 极限下最轻态退化为直线（κ=τ=0），与『三种螺旋缠绕构型』『缠绕数为唯一本征标记』冲突")
emit("      射程：实验尚未确定 m₁=0，故不判 FAIL；但理论须容纳该极限 ⇒ 属结构性张力。")
emit("      另与 V18_2 V2-d（质量不可归结于任何结不变量）同源：拓扑标签无法承载质量层级。")
emit("")

# ===========================================================================
# 第 7 节  V9-f：背景挠率的上限（外部约束，非 GAQ 预测）
# ===========================================================================
emit("-" * 78)
emit("第 7 节  背景挠率扰动 δτ 的观测上限（对 GAQ 的约束，不是支持）")
emit("-" * 78)
emit("")
emit("  一阶估计：背景挠率扰动在传播长度 L 上贡献附加相位 δΦ ≈ δτ · L。")
emit("  现有实验对标准三味振荡的检验精度为百分点量级 ⇒ 取 δΦ_max = 0.05 rad（保守）。")
emit("      δτ_max = δΦ_max / L")
emit("")
tau_nu_ref = m_nu / HBARC
rows = []
for label, Lm in (("太阳（日地 1.5e11 m）", 1.5e11),
                  ("大气（地球直径 1.3e7 m）", 1.3e7),
                  ("T2K（295 km）", 2.95e5),
                  ("反应堆（1 km）", 1.0e3),
                  ("中子星内部（假设 10 km）", 1.0e4)):
    d = 0.05 / Lm
    rows.append((label, "%.3e" % d, "%.3e" % (d / tau_nu_ref)))
table(["基线", "δτ_max [1/m]", "δτ_max / τ_ν（τ_ν=%.3e）" % tau_nu_ref], rows)
emit("")
emit("  反过来看 §5-1 的『强挠率环境产生非标准畸变』：在中子星 10 km 基线上要产生")
emit("  O(0.1) 的相位畸变，需 δτ ≈ 1e-5 1/m；而地球/太阳系数据已把 δτ 压到")
need_tau = 1.0e-5
sun_lim = 0.05 / 1.5e11
emit("  %.1e ~ %.1e 1/m ⇒ 需要致密天体内部比太阳基线处高 %.1f 个量级以上。"
     % (sun_lim, 0.05 / 1.0e3, math.log10(need_tau / sun_lim)))
emit("  GAQ 未给背景挠率场 τ_bg(x) 的动力学、分布或耦合系数 ⇒ 该『判别信号』在体系内")
emit("  **既算不出阈值也算不出预期产地**，只能事后指派。")
emit("")
B("V9-f", "§5-1『强挠率畸变』在体系内不可定量：缺 τ_bg(x) 动力学 + 耦合系数；现有数据反给出 δτ 上限")
emit("      外部约束（对 GAQ 的约束而非支持）：太阳基线 δτ < %.2e 1/m，T2K δτ < %.2e 1/m。"
     % (0.05 / 1.5e11, 0.05 / 2.95e5))
emit("      最小增广（使之可证伪）：给出 τ_bg(x) 的场方程 + 耦合系数 g_τ + 边界条件，共 3 项。")
emit("")

# ===========================================================================
# 第 8 节  V9-g：250 位精度的必要性（精度表演）
# ===========================================================================
emit("-" * 78)
emit("第 8 节  mpmath 250 位精度的必要性审计")
emit("-" * 78)
emit("")
exp_unc = 0.01     # Δm²/θ 的测量精度量级（Super-K / T2K 为百分点量级）
d_prec = worst_hp  # 由 SC5 实测：Decimal(260) 与 float 的 sin² 之差 1.874e-16
rows = [
    ("Decimal(260) 与双精度之差（SC5 实测）", "%.3e" % d_prec),
    ("实验不确定度（量级）", "%.3e" % exp_unc),
    ("余量", "%.1f 个量级" % math.log10(exp_unc / d_prec)),
]
table(["对比项", "数值"], rows)
emit("")
emit("  注：单点概率在两种精度下甚至逐位相同，故这里取 SC5 在多个相位点上实测的最大差")
emit("  %.2e 作为『高精度能带来的最大改进』的上界。它比实验不确定度小约 %d 个量级。"
     % (d_prec, int(round(math.log10(exp_unc / d_prec)))))
emit("  ⇒ 250 位精度对中微子振荡问题**零收益**；它掩盖的是 §2 相位标度这类结构性问题。")
emit("")
I("V9-g", "250 位精度属表演性：高精度相对双精度的改进上界 %.2e，比实验不确定度小约 %d 个量级"
  % (d_prec, int(round(math.log10(exp_unc / d_prec)))))
emit("")

# ===========================================================================
# 第 9 节  V9-h：与既有裁定的合流登记（不重复计否证）
# ===========================================================================
emit("-" * 78)
emit("第 9 节  与既有裁定的合流登记")
emit("-" * 78)
emit("")
rows = [
    ("§1「中微子仅保留缠绕数与挠率携带的惯性质量」",
     "V18_6 V6-h：∫τ ds 为尺度不变量（机器零），结构上不能承载质量量纲",
     "冲突（合流，不重复计 FAIL）"),
    ("§1「电荷 = 通量守恒量，中微子无径向通量 ⇒ Q=0」",
     "V18_6 分支二半阻塞：电荷量子化需 e²=4πε₀αℏc，依赖 ℏ，被 V18_3 锁死",
     "同族；『Q=0=无缠绕荷』属同义表述，零新内容"),
    ("§5-2「弱场下质量/味二分只是有效描述」",
     "V18_2 V2-d：质量不可归结于任何结不变量（同族质量跨度 1852 vs 3.68）",
     "同向合流"),
    ("§5-1「混合角由真空背景挠率基态几何决定，可第一性算出」",
     "本册 V9-d：混合角在参数账内无约束 ⇒ 恒可事后指派",
     "冲突（已计 V9-d）"),
]
table(["来稿条目", "既有裁定", "关系"], rows)
emit("")
B("V9-h", "来稿 §1 的『挠率携带惯性质量』与 V18_6 V6-h 直接冲突；本条仅登记合流，不重复计否证")
emit("      其余三项亦为合流；本册不把它们算作新发现。")
emit("")

# ===========================================================================
# 第 10 节  V9-i：惰性中微子 = 亚稳态中间构型（不可证伪）
# ===========================================================================
emit("-" * 78)
emit("第 10 节  惰性中微子『亚稳态中间拓扑构型』的可证伪性")
emit("-" * 78)
emit("")
emit("  来稿 §5-3：疑似惰性中微子信号 = 亚稳态中间拓扑缠绕构型，**不是新基本粒子**。")
emit("  判据：该陈述是否给出 (a) 中间构型数目、(b) 寿命/分支比、(c) 与活性态的混合强度。")
emit("  三者皆无 ⇒ 对任意观测到的混合强度都可事后指派一个「中间构型耦合」。")
emit("")
rows = []
for target in (0.01, 0.05, 0.20, 0.50):
    rows.append(("任意实测混合 sin²2θ_ee = %.2f" % target,
                 "指派中间构型耦合 g = %.4f" % math.sqrt(target),
                 "可拟合"))
table(["目标观测", "GAQ 侧事后指派", "结果"], rows)
emit("")
emit("  外部约束（不是 GAQ 的预测，只是环境事实）：")
emit("      N_eff(SM) = %.3f，Planck 2018+BAO = %.2f ± %.2f ⇒ 偏差 %.2f σ（一致）"
     % (N_EFF_SM, N_EFF_PLANCK, N_EFF_SIGMA,
        abs(N_EFF_SM - N_EFF_PLANCK) / N_EFF_SIGMA))
emit("      ⇒ 完全热化的额外惰性态已被 ΔN_eff ≲ 0.17 强约束；短基线异常的全球拟合张力仍在。")
emit("")
F("V9-i", "§5-3『惰性中微子 = 亚稳态中间构型』未给数目/寿命/混合强度 ⇒ 恒可事后指派，不可证伪")
emit("      射程：与 V18.6 V6-j（重联阈值不可证伪）同族；不否认中间构型这一物理图像的可能性，")
emit("      只否认它在当前形式下具有判别力。")
emit("")

# ===========================================================================
# 第 11 节  V9-j：N_eff 事实重算 + 分支 C 的输入端
# ===========================================================================
emit("-" * 78)
emit("第 11 节  分支 C 的输入端：N_eff 事实重算")
emit("-" * 78)
emit("")
sigma_dev = abs(N_EFF_SM - N_EFF_PLANCK) / N_EFF_SIGMA
rows = [
    ("SM 标准值 N_eff", "%.3f" % N_EFF_SM),
    ("Planck 2018 + BAO", "%.2f ± %.2f" % (N_EFF_PLANCK, N_EFF_SIGMA)),
    ("偏差", "%.3f σ" % sigma_dev),
]
table(["量", "值"], rows)
emit("")
check("SC12 N_eff 的 SM 值与 Planck 一致（<1σ）", sigma_dev < 1.0, "%.3f σ" % sigma_dev)
emit("  属标准宇宙学事实的复算，**不构成对 GAQ 的任何支持**。")
emit("  分支 C 要求 GAQ 给出自己的 N_eff 与退耦温度 ⇒ 需要弱作用场论 + 宇宙学场方程，")
emit("  前者（V18_1 P1 FAIL、分支二关闭）与后者（V18_6 分支一阻塞）均已判阻塞。")
emit("")
P("V9-j", "N_eff：SM 3.044 与 Planck 2.99±0.17 相差 %.2f σ（外部事实复算，非 GAQ 证据）" % sigma_dev)
emit("")

# ===========================================================================
# 第 12 节  V9-l：两味近似对标的精度不足
# ===========================================================================
emit("-" * 78)
emit("第 12 节  来稿 §4 用两味近似对标 T2K / Super-K 的精度")
emit("-" * 78)
emit("")
rows = []
worst_gap = 0.0
for label, Lm, Eg in (("T2K", 2.95e5, 0.6), ("Super-K 大气", 1.3e7, 1.0),
                      ("NOvA", 8.1e5, 2.0), ("太阳", 1.5e11, 0.001)):
    U = pmns(S12SQ, S13SQ, S23SQ, DELTA_CP)
    p3 = prob_three(U, 1, 1, DM21, DM31, Lm, Eg)
    th23 = math.asin(math.sqrt(S23SQ))
    p2_two = 1.0 - prob_two_flavor(DM31, Lm, Eg, th23)
    gap = abs(p3 - p2_two)
    worst_gap = max(worst_gap, gap)
    if label == "T2K":
        gap_t2k = gap
    rows.append((label, "%.1e m" % Lm, "%.2f GeV" % Eg,
                 "%.6f" % p3, "%.6f" % p2_two, "%.2e" % gap))
table(["实验", "L", "E", "三味精确 P(ν_μ→ν_μ)", "两味近似", "|差|"], rows)
emit("")
ratio_dm = DM21 / DM31
emit("  两味近似同时忽略 Δm^2_21 项与 θ13 项。被忽略项的**相对权重** ≈ Δm^2_21/Δm^2_31 = %.4f，" % ratio_dm)
emit("  但绝对偏差随 L/E 增大而增大（Δm^2_21 的相位本身变大）：T2K 点 %.2e、大气点 %.2e。"
     % (gap_t2k, worst_gap))
emit("  注：本表为真空单点概率，未含物质效应；所列大气/太阳点的 L/E 使 Δm^2_21 相位达 O(1)，")
emit("  故偏差远大于 0.0295。T2K/NOvA 的系统精度目标为百分点量级 ⇒ 两味近似不足以对标。")
emit("")
I("V9-l", "两味近似与三味精确概率在 T2K 点差 %.2e、大气点差 %.2e；L/E 越大偏差越大，不足以对标"
  % (gap_t2k, worst_gap))
emit("")

# ===========================================================================
# 第 13 节  分支裁定：A / B / C 与「是否直接推三味 PDE」
# ===========================================================================
emit("-" * 78)
emit("第 13 节  分支裁定（回答来稿 §7 的 A / B / C）")
emit("-" * 78)
emit("")
emit("  【前置：S03 的三条主线已由并行链 V18_8 收口】")
emit("  V18_8 判：分支一关闭（V18_4 五条 FAIL）、分支二关闭（V18_1 + V18_2）、")
emit("  分支三阻塞（CKM 拓扑起源，S03-C0046..C0051）⇒ 分支选择问题已收口。")
emit("  因此来稿 §7 的 A/B/C 是**收口之后提出的新支线**，须按同等门禁审理，")
emit("  不得以『分支三曾被判可行』为由直接放行。本册的裁定与 V18_8 一致且无冲突。")
emit("")
rows = [
    ("A 三味耦合 PDE + Rust 并行 FDTD",
     "阻塞",
     "缺 4 项输入：①作用量/动力学 ②耦合常数的质量量纲（V18_5 §9 已判 PDE 分支阻塞）"
     " ③重联的局域规则 ④初值与边界条件；"
     "另有结构性障碍：拓扑重联是**非局域**过程（改变全局缠绕），PDE 是局域演化，"
     "用局域方程描述非局域拓扑改变须引入缺陷/奇异点，方程在这些点失效"),
    ("B Berry 几何相位的数学证明",
     "半阻塞",
     "Berry 构造需 4 项：①参数空间 M（GAQ 有：(κ,τ,ω) 三元组，**具备**）"
     " ②希尔伯特空间与态族 |n(R)⟩（**缺**，V18_6 V6-m 判无 Cl(1,3)、无旋量结构）"
     " ③Berry 联络 A=i⟨n|∇n⟩（依赖②）④回路与规范不变性（依赖②③）"
     " ⇒ 4 项中仅 1 项具备"),
    ("C 三者退耦时间对标 Planck",
     "阻塞",
     "需 GAQ 自己的 N_eff 与退耦温度：前者需弱作用场论（V18_1 P1 FAIL、分支二关闭），"
     "后者需宇宙学场方程（V18_6 分支一阻塞）；两端皆无"),
]
table(["分支", "裁定", "依据"], rows)
emit("")
emit("  **对『是否直接往下推导三味耦合 PDE』的回答：不推。**")
emit("  理由三条（按重要性）：")
emit("    1. 参数账未过约束（V9-d）：先把自由度降到 ≤ 6 才有判别力，否则 PDE 只是")
emit("       把 11 个自由参数搬进一组方程，产出不可证伪的拟合器；")
emit("    2. 相位标度冲突未解决（V9-b）：PDE 演化出来的是几何相位 ∝ L，")
emit("       而可观测的是 ∝ L/E，方程与观测之间仍差一个未定义的换算；")
emit("    3. §4 的单位错误未修（V9-a）：数值侧尚无一条已核验的基线曲线可供 PDE 对标。")
emit("")
emit("  **建议路线（B 的降级形式 B-1）**：把「Berry 相位」降级为体系内可算的")
emit("  **经典几何 anholonomy**——Frenet 标架（或 ribbon 加框）沿闭合回路的 holonomy，")
emit("  V18_6 V6-a 已证明加框后 Lk = Tw + Wr 数值闭合（0.00000 / 1.00020 / 2.00074）。")
emit("  该路线 3 项前提在体系内具备、可立即开工，但**必须同时声明两点**：")
emit("    (a) 它是味变换的几何描述，**不还原 SM 的振荡相位**（V9-b）；")
emit("    (b) 它给出的可判决量是手性符号与 holonomy 角，不是质量或混合角（V9-d）。")
emit("")
emit("  执行门禁（六条，不满足不得开工）：")
emit("    G1 声明 §3 中 ∫...ds 的积分域与标度读法（V9-c-r）；")
emit("    G2 声明 τ 是否与 E 无关；若有关须给函数形式与独立约束（V9-b）；")
emit("    G3 显式承担质量标度锚为外加公设（V18_3）；")
emit("    G4 参数账门禁：独立自由参数 ≤ 6（= 观测量数），且不得含零信息冗余方向（V9-d）；")
emit("    G5 给出 τ_bg(x) 的动力学 + 耦合系数 + 边界条件，否则 §5-1 不可检验（V9-f）；")
emit("    G6 若走 B-1：显式加框、声明不还原 SM 相位、可判决量取手性符号/holonomy（V18_6 §11）。")
emit("")

# ===========================================================================
# 第 14 节  回填、方法论与下一版待办
# ===========================================================================
emit("-" * 78)
emit("第 14 节  对既有体系的回填 / 方法论 / 下一版待办")
emit("-" * 78)
emit("")
rows = [
    ("V18_3 质量标度为公设边界", "公设边界", "第 3 次在此被触发：Δm² 仍需外加质量锚（V9-d）"),
    ("V18_6 V6-h ∫τ ds 不能承载质量", "FAIL", "被 §1『挠率携带惯性质量』再次撞上（V9-h，合流）"),
    ("V18_6 分支二半阻塞", "半阻塞", "本册 §1『电荷=通量』同族（V9-h）"),
    ("V18_2 V2-d 质量不可归结于结不变量", "FAIL", "本册 V9-e（m₁=0 退化）同源"),
    ("V18_5 §9 分支一阻塞", "阻塞", "本册分支 C 与 A 的阻塞均沿此（V9-j / 第 13 节）"),
    ("V18_8 分支三（CKM）阻塞 + 三分支收口", "阻塞+收口",
     "本册 A/B/C 是收口后的新支线，按同等门禁审理（见第 13 节前置）；"
     "口径对照见第 5 节（有量纲模长 vs 无量纲比值，结论一致）"),
    ("恒可拟合失败族计数", "V18_1 P1 / V18_2 V2-e / V18_6 V6-j / V18_8 C0051 / 本册 V9-d·V9-i",
     "本族第 5、6 次；建议在立项前先做参数账门禁"),
]
table(["既有裁定", "状态", "本册回填"], rows)
emit("")
emit("  方法论沉淀（本册自抓，可复用）：")
emit("    1. 数值框架类来稿先核单位：SI 严格式与经验式双路对拍（本册 KCONV=%.6e vs 1.267e-3，"
     "差 8e-5）。" % KCONV)
emit("    2. 「用几何量替换物理量」类声称须做三重检验：量纲、标度指数、能量依赖。")
emit("       本册仅靠 1/E 依赖一项即否证『完全还原 SM』（V9-b）。")
emit("    3. 恒可拟合必须给参数账与零信息方向，不能只说『可调』（V9-d：11 vs 6，冗余 3）。")
emit("    4. 高精度算术要跟实验不确定度比，不能只跟自己比（V9-g：差 14 量级）。")
emit("    5. 未声明积分域这类歧义应判 BOUNDARY，不越权判 FAIL（V9-c-r）。")
emit("    6. **拓扑非局域 vs PDE 局域**是「场演化仿真」类分支的通用结构性障碍，")
emit("       应在立项时先判定，不必等到实现阶段（分支 A 即因此阻塞）。")
emit("    7. **并行链编号冲突顺延不覆盖，但必须做口径对照**：本册与 V18_8 分别从")
emit("       「有量纲模长」与「无量纲比值」两侧计数，不做对照会留下互相矛盾的读数。")
emit("")
emit("  下一版（V18_8）待办：")
emit("    (1) 修 §4 单位错误并重算基线曲线（前置，1 小时内可做）；")
emit("    (2) 走 B-1：实现 Frenet/ribbon 的闭合回路 holonomy，给出可算量（依赖 G6）；")
emit("    (3) 建立参数账门禁脚本，把『自由度 ≤ 观测量』做成自动检查（依赖 G4）。")
emit("")

# ===========================================================================
# 自检汇总与落盘
# ===========================================================================
emit("=" * 78)
emit("条目汇总")
emit("=" * 78)
for code, verdict, title in ITEMS:
    emit("  [%s] %-8s %s" % (verdict, code, title))
emit("")
emit("条目合计 %d：PASS=%d FAIL=%d BOUNDARY=%d INFO=%d CORRECTED=%d"
     % (len(ITEMS), COUNTS["PASS"], COUNTS["FAIL"],
        COUNTS["BOUNDARY"], COUNTS["INFO"], COUNTS["CORRECTED"]))
emit("")

nok = sum(1 for _, ok, _ in CHECKS if ok)
emit("自检 %d/%d" % (nok, len(CHECKS)))
for name, ok, detail in CHECKS:
    emit("  [%s] %s :: %s" % ("OK" if ok else "NG", name, detail))
emit("")

emit("红线复述：")
emit("  1. 本册所有 FAIL 均为来稿内部自洽性或与既有判决的冲突，不是对 GAQ 全部内容的否定。")
emit("  2. 唯一的 PASS（V9-j）是标准宇宙学事实的独立复算，不构成对 GAQ 的物理验证。")
emit("  3. 本册未对任何 GAQ 物理预言做正面验证；V9-f 给出的挠率上限是对 GAQ 的约束而非支持。")
emit("")

# ---------------------------------------------------------------------------
# 落盘
# ---------------------------------------------------------------------------
ok_all = (nok == len(CHECKS)) and len(CHECKS) >= 10
text = "\n".join(LINES) + "\n"

if not os.path.isdir(LOGDIR):
    os.makedirs(LOGDIR)
path = os.path.join(LOGDIR, REPORT_NAME)
with io.open(path, "w", encoding="utf-8") as fh:
    fh.write(text)

print(text)
print("报告已写入: %s" % path)
print("自检 %d/%d" % (nok, len(CHECKS)))

sys.exit(0 if ok_all else 1)
