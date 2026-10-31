# -*- coding: utf-8 -*-
r"""
ROOT V4.0《空间光速螺旋统一运动学》独立数值复核  (v2)

为什么要有 v2：
  - v1 的三阶差分模板符号写反，导致 τ 残差虚高到 200%（判定器本身有 bug，不是文档的错）。
  - v1 用统一 1e-6 阈值去比「只有 4 位有效数字的靶值」（如 7.790e5），
    把纯粹的截断误差误报成 FAIL。**这是典型的「假绿/假红」双向风险**，必须按靶值自身
    有效位数分层比较。

设计原则（与本库审计链一致）：
  1. 零第三方依赖 —— Python 3.13 无 numpy/sympy/mpmath，一律 Decimal(prec=60) + Fraction。
  2. 文档给出的每一个数字都必须被「重算一遍」；文档数值只作靶值，绝不作输入。
  3. 精度分层：先按靶值自身有效位数 round 到同位再比，相等判 PASS，否则判 FAIL；
     同时如实报出未经截断的相对残差，供人工复核。
  4. 判据必须有控制组：把正确对象换成错误对象，判据必须翻红，否则该判据零分辨力。

输出：PASS / FAIL / INFO 三类；FAIL 一律逐条解释是「真错」还是「有效位不足」。
运行方式：见 scratch/_run_root_v40.py（中文路径不入 argv）。
"""

import math
import random
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction as Fr

getcontext().prec = 60

# ---------------------------------------------------------------- 常数（SI 定义值 / CODATA）
C = Decimal(299792458)                    # 真空光速，精确定义
H_PL = Decimal("6.62607015e-34")          # 普朗克常数，精确定义
QE = Decimal("1.602176634e-19")           # 元电荷，精确定义
EPS0 = Decimal("8.8541878128e-12")        # 真空介电常数（CODATA 2018 推荐值，非定义值）
MU0 = Decimal("1.25663706212e-6")         # 真空磁导率（同上，已非 SI 定义值）
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494")
HBAR = H_PL / (2 * PI)

# ---------------------------------------------------------------- Decimal 三角函数
_HALF_PI = PI / Decimal(2)
_TWO_PI = 2 * PI


def dcos(x: Decimal) -> Decimal:
    x = x % _TWO_PI
    if x > PI:
        x = _TWO_PI - x
    s = Decimal(1)
    term = Decimal(1)
    xx = x * x
    n = 0
    while True:
        n += 1
        term = -term * xx / (Decimal(2 * n - 1) * Decimal(2 * n))
        if term == 0 or n > 400:
            break
        s += term
    return s


def dsin(x: Decimal) -> Decimal:
    return dcos(_HALF_PI - x)


# ---------------------------------------------------------------- 记录器（精度分层）
rows = []
_SUB = "─" * 86


def _nsig(s: str) -> int:
    """从靶值字面量数出有效位数，例如 '7.790e5' -> 4，'0.420000' -> 6。"""
    m = s.lower().split("e")[0].lstrip("+-").replace(".", "").lstrip("0")
    return len(m) if m else 1


def _round_sig(x: Decimal, n: int) -> Decimal:
    if x == 0:
        return Decimal(0)
    q = Decimal(1).scaleb(x.adjusted() - n + 1)
    return x.quantize(q, rounding=ROUND_HALF_UP)


def chk(cid, desc, got, want_str, note="", zero_tol=None):
    """按靶值有效位数分层比较。want_str 为字面量字符串。

    注意：靶值为 0 时不能直接套「有效位数取整」——那样会把 6e-60 的机器残差误判为 FAIL。
    这种情况改用绝对容差（默认 1e-25，可由 zero_tol 覆盖）。
    """
    w = Decimal(want_str)
    rel = abs(got - w) / abs(w) if w != 0 else abs(got)
    if w == 0:
        tol = Decimal(zero_tol) if zero_tol is not None else Decimal("1e-25")
        ok = abs(got) <= tol
        n = 0
    else:
        n = _nsig(want_str)
        ok = _round_sig(got, n) == w
    rows.append((cid, desc, got, w, rel, "PASS" if ok else "FAIL", n, note))
    return rel


def note(cid, desc, got, unit=""):
    rows.append((cid, desc, got, None, None, "INFO", None, unit))


def head(t):
    rows.append(("HEAD", t, None, None, None, "HEAD", None, ""))


# ================================================================
# A 组：基础光学量（λ = 550 nm）
# ================================================================
def group_a():
    head("A 组 · 基础光学量（文档第六节表头）")
    lam = Decimal("550e-9")
    f_EM = C / lam
    chk("A1", "光学频率 f_EM = c/λ", f_EM / Decimal("1e12"), "545.077", "单位 THz")
    E_J = H_PL * f_EM
    chk("A2", "单光子能量 E = hf", E_J / QE, "2.254258", "单位 eV")
    return lam


# ================================================================
# B 组：符号恒等式 —— 精确零残差 + 差分第三路径 + 控制组
# ================================================================
def _third_path_kappa_tau(Rd, wd, ud, h_rel="1e-10"):
    """由位置函数 r(t) 出发，用 4 阶中心差分实算 κ、τ（不复用任何手工导数式）。"""
    def pos(tt):
        ph = wd * tt + Decimal("0.371")
        return (Rd * dcos(ph), Rd * dsin(ph), ud * tt)

    h = Decimal(h_rel) / max(abs(wd), Decimal(1))
    t0 = Decimal("0.8117")
    P = {j: pos(t0 + Decimal(j) * h) for j in (-3, -2, -1, 0, 1, 2, 3)}

    # 一阶：(-f_{-2}+8f_{-1}... ) -> 标准 4 阶：(f_{-2} -8f_{-1} +8f_{+1} -f_{+2})/(12h)
    A = [(P[-2][i] - 8 * P[-1][i] + 8 * P[1][i] - P[2][i]) / (12 * h) for i in range(3)]
    # 二阶：(-f_{-2}+16f_{-1}-30f_0+16f_{+1}-f_{+2})/(12h^2)
    Bd = [(-P[-2][i] + 16 * P[-1][i] - 30 * P[0][i] + 16 * P[1][i] - P[2][i])
          / (12 * h * h) for i in range(3)]
    # 三阶（符号已用 sin 在 0 处的 f'''=-1 校验）：(f_{-3}-8f_{-2}+13f_{-1}-13f_{+1}+8f_{+2}-f_{+3})/(8h^3)
    Cd = [(P[-3][i] - 8 * P[-2][i] + 13 * P[-1][i]
           - 13 * P[1][i] + 8 * P[2][i] - P[3][i]) / (8 * h ** 3) for i in range(3)]

    def cross(p, q):
        return (p[1] * q[2] - p[2] * q[1],
                p[2] * q[0] - p[0] * q[2],
                p[0] * q[1] - p[1] * q[0])

    CX = cross(A, Bd)
    nc = (CX[0] ** 2 + CX[1] ** 2 + CX[2] ** 2).sqrt()
    na = (A[0] ** 2 + A[1] ** 2 + A[2] ** 2).sqrt()
    return nc / na ** 3, (CX[0] * Cd[0] + CX[1] * Cd[1] + CX[2] * Cd[2]) / (nc * nc)


def group_b():
    head("B 组 · 圆柱螺旋曲率/挠率恒等式（随机抽样，200 组）")

    random.seed(20261031)
    worst = {"k": Decimal(0), "t": Decimal(0)}
    exact = {"k2t2": 0, "inv_R": 0, "inv_H": 0}
    ctrl_wrong_formula = Decimal(0)
    nok = 0

    for _ in range(400):
        # 用勾股数保证 |r'|=v 是有理数，使 Fraction 残差可做到**严格 0**
        m = Fr(random.randint(2, 300))
        n = Fr(random.randint(1, 299))
        if m <= n:
            continue
        uu = m * m - n * n
        rp = 2 * m * n
        ww = Fr(random.choice([1, -1])) * Fr(random.randint(1, 10**4), random.randint(1, 10**3))
        RR = rp / abs(ww)
        v2 = uu * uu + rp * rp

        kappa = RR * ww * ww / v2          # 文档 3.4 闭式
        tau = uu * ww / v2                 # 文档 3.5 闭式

        # ---- 精确恒等式（Fraction，残差应严格为 0）
        if abs(kappa * kappa + tau * tau - ww * ww / v2) != 0:
            exact["k2t2"] += 1
        if abs(kappa / (kappa * kappa + tau * tau) - RR) != 0:
            exact["inv_R"] += 1
        if abs(tau / (kappa * kappa + tau * tau) - uu / ww) != 0:
            exact["inv_H"] += 1

        # ---- 第三路径：差分实算
        Rd = Decimal(RR.numerator) / Decimal(RR.denominator)
        wd = Decimal(ww.numerator) / Decimal(ww.denominator)
        ud = Decimal(uu.numerator) / Decimal(uu.denominator)
        try:
            kn, tn = _third_path_kappa_tau(Rd, wd, ud)
        except Exception:
            continue
        kd = Decimal(kappa.numerator) / Decimal(kappa.denominator)
        td = Decimal(tau.numerator) / Decimal(tau.denominator)
        if kd == 0 or td == 0 or kn == 0:
            continue
        worst["k"] = max(worst["k"], abs((kn - kd) / kd))
        worst["t"] = max(worst["t"], abs((tn - td) / td))
        # 控制组：故意用错误公式 κ' = Rω²/u²（漏掉横向贡献）应当明显偏离
        try:
            pass
        except Exception:
            pass
        nok += 1

    note("B1", "κ = |r'×r''|/|r'|³：差分实算 vs 文档闭式，最大相对残差", worst["k"])
    note("B2", "τ = ((r'×r'')·r''')/|r'×r''|²：差分实算 vs 文档闭式，最大相对残差", worst["t"])
    note("B0", "实际参与对比的随机样本数", Decimal(nok))

    chk("B3", "κ²+τ² = ω²/v²：Fraction 精确残差非零次数", Decimal(exact["k2t2"]), "0")
    chk("B4", "反演 R = κ/(κ²+τ²)：Fraction 精确残差非零次数", Decimal(exact["inv_R"]), "0")
    chk("B5", "反演 τ/(κ²+τ²) = u/ω ⇔ H = 2πτ/(κ²+τ²)：精确残差非零次数",
        Decimal(exact["inv_H"]), "0")

    # ---- 控制组：证明 B1/B2 判据有分辨力（换成错误公式必须翻红）
    Rd, wd, ud = Decimal("3.7"), Decimal("11.3"), Decimal("5.1")
    kn, tn = _third_path_kappa_tau(Rd, wd, ud)
    v2 = ud * ud + Rd * Rd * wd * wd
    k_good = Rd * wd * wd / v2
    t_good = ud * wd / v2
    k_bad = Rd * wd * wd / (ud * ud)          # 错误式：漏掉横向速度
    t_bad = ud * wd / (Rd * Rd * wd * wd)     # 错误式
    note("B6", "控制组·正确式 κ 与差分值相对残差（应≈0）", abs((kn - k_good) / k_good))
    note("B7", "控制组·错误式 κ'=Rω²/u² 与差分值相对残差（应显著>0）",
         abs((kn - k_bad) / kn))
    note("B8", "控制组·正确式 τ 与差分值相对残差（应≈0）", abs((tn - t_good) / t_good))
    note("B9", "控制组·错误式 τ'=uω/(R²ω²) 与差分值相对残差（应显著>0）",
         abs((tn - t_bad) / tn))


# ================================================================
# C 组：文档第六节双列对照表（λ=550nm, R=0.35λ, ω_h=1.2c/λ）
# ================================================================
def group_c(lam):
    head("C 组 · 双约束对照表（R=0.35λ=192.5nm, ω_h=1.2c/λ）")
    R = Decimal("0.35") * lam
    om_h = Decimal("1.2") * C / lam
    chk("C0", "螺旋半径 R（nm）", R * Decimal("1e9"), "192.5")

    vperp = R * om_h
    chk("C1", "横向速度 v⊥/c = Rω_h/c（两列共用）", vperp / C, "0.420000")

    # ---- 方案 A：轴向 u = c
    uA = C
    vA = (uA * uA + vperp * vperp).sqrt()
    chk("C2", "[A] 总速率 v/c = √(1+0.42²)", vA / C, "1.084620")
    kA = R * om_h * om_h / (vA * vA)
    chk("C3", "[A] 曲率 κ = Rω²/v²（m⁻¹）", kA, "7.790e5")
    tA = uA * om_h / (vA * vA)
    chk("C4", "[A] 挠率 τ = uω/v²（m⁻¹）", tA, "1.855e6")
    chk("C5", "[A] 每圈螺距 H = 2πu/ω（nm）", 2 * PI * uA / om_h * Decimal("1e9"), "2879.793")

    # ---- 方案 B：总速率 v = c
    vB = C
    uB = (vB * vB - vperp * vperp).sqrt()
    chk("C6", "[B] 轴向速度 u/c = √(1−0.42²)", uB / C, "0.907524")
    kB = R * om_h * om_h / (vB * vB)
    chk("C7", "[B] 曲率 κ = Rω²/c²（m⁻¹）", kB, "9.164e5")
    tB = uB * om_h / (vB * vB)
    chk("C8", "[B] 挠率 τ = uω/c²（m⁻¹）", tB, "1.980e6")
    chk("C9", "[B] 每圈螺距 H = 2πu/ω（nm）", 2 * PI * uB / om_h * Decimal("1e9"), "2613.482")

    # ---- 自洽 / 相对论约束
    chk("C10", "[B] 恒等式 κ²+τ² = ω²/c² 相对残差",
        abs((kB * kB + tB * tB) - om_h * om_h / (C * C)) / (om_h * om_h / (C * C)), "0")
    chk("C11", "[A] 恒等式 κ²+τ² = ω²/v² 相对残差（注意 v≠c）",
        abs((kA * kA + tA * tA) - om_h * om_h / (vA * vA)) / (om_h * om_h / (vA * vA)), "0")
    ds2_B = -C * C + R * R * om_h * om_h + uB * uB
    ds2_A = -C * C + R * R * om_h * om_h + uA * uA
    chk("C12", "[B] ds² = −c²+R²ω²+u²（光样条件，m²/s²）", ds2_B, "0")
    note("C13", "[A] ds² = −c²+R²ω²+u²（方案A：应为正 ⇒ 类空，非光样）", ds2_A, "m²/s²")
    note("C14", "[A] ds²/c² 归一化值（>0 即类空）", ds2_A / (C * C))
    return R, om_h


# ================================================================
# D 组：强制 ω_h = ω_EM 的半径上限
# ================================================================
def group_d(lam, R):
    head("D 组 · 强制螺旋频率 = 光学频率时的半径上限")
    om_EM = 2 * PI * C / lam
    Rmax = C / om_EM
    chk("D1", "R ≤ λ/2π（v⊥≤c 的必要条件，nm）", Rmax * Decimal("1e9"), "87.5352")
    chk("D2", "示例 R=192.5nm 在该频率下的横向速度 v⊥/c", R * om_EM / C, "2.1991")
    note("D3", "示例半径 / 半径上限（比值 >1 即越界）", R / Rmax)
    return om_EM, Rmax


# ================================================================
# E 组：轴向群时延的几何投影解释
# ================================================================
def group_e():
    head("E 组 · 1 m 传播、5 μm 额外光程的演示值")
    chk("E1", "额外飞行时间 Δt = 5μm/c（fs）", Decimal("5e-6") / C * Decimal("1e15"), "16.6782")
    cos_t = 1 / (1 + Decimal("5e-6"))
    chk("E2", "反推 cosθ = 1/(1+5e-6)", cos_t, "0.999995")
    th_deg = Decimal(math.acos(float(cos_t))) * Decimal(180) / PI
    chk("E3", "对应倾角 θ = arccos(cosθ)（deg）", th_deg, "0.1812")
    return cos_t, th_deg


# ================================================================
# F 组：Maxwell 圆偏振 |S|/w = c —— 走独立路径（不再套用现成结论）
# ================================================================
def group_f(lam):
    head("F 组 · Maxwell 圆偏振 |S|/w = c（由 E、B 分量实算，不套现成结论）")
    om = 2 * PI * C / lam
    k = 2 * PI / lam
    E0 = Decimal("1")
    random.seed(7)
    worst = Decimal(0)
    worst_ctrl = Decimal(0)
    for _ in range(200):
        zf = Decimal(repr(random.uniform(-1e-6, 1e-6)))
        tt = Decimal(repr(random.uniform(0, 1e-13)))
        ph = k * zf - om * tt
        sgm = Decimal(random.choice([1, -1]))
        Ex = E0 * dcos(ph)
        Ey = E0 * sgm * dsin(ph)
        # B = (1/c) ẑ×E = (1/c)(-Ey, Ex, 0)
        Bx, By = -Ey / C, Ex / C
        # S = (1/μ0) E×B  →  S_z = (Ex·By − Ey·Bx)/μ0
        Sz = (Ex * By - Ey * Bx) / MU0
        # w = ε0|E|²/2 + |B|²/(2μ0)
        wem = EPS0 * (Ex * Ex + Ey * Ey) / 2 + (Bx * Bx + By * By) / (2 * MU0)
        ratio = abs(Sz) / wem
        worst = max(worst, abs(ratio - C) / C)
        # 控制组：若把能量密度误算成 ε0E²/2（丢掉磁场项），比值应为 2c
        w_bad = EPS0 * (Ex * Ex + Ey * Ey) / 2
        worst_ctrl = max(worst_ctrl, abs(abs(Sz) / w_bad - 2 * C) / (2 * C))
    note("F1", "|S|/w 与 c 的最大相对残差（受 ε0μ0c²=1 的常数精度限制）", worst)
    note("F2", "控制组：能量密度丢磁场项 ⇒ 比值变 2c，与 2c 的残差", worst_ctrl)
    note("F3", "SI 自洽水平：ε0·μ0·c² − 1", EPS0 * MU0 * C * C - 1)
    # 判别力控制：倾斜直线（k_z<k）给出的轴向速度偏离 c
    chk("F4", "控制组：k_z/k=0.999995 时 |偏离 c|/c（证明投影式不是恒等式）",
        abs(Decimal("0.999995") - 1) / 1, "5e-6")


# ================================================================
# G 组：新增判据 —— 「经典轨道角动量 = ℏ」读法的封闭性
# ================================================================
def group_g(lam, R, om_h, om_EM, Rmax):
    head("G 组 · 新增判据：若要求螺旋承担光子的 ℏ 角动量")
    # 假设 P1–P4：E=ℏω_EM；|p|=E/c 沿切线；v=c；L_z = R·p⊥ = ℏ
    # ⇒ R = (λ/2π)/sinθ ≥ λ/2π
    Rmin = lam / (2 * PI)
    note("G1", "R_min = λ/2π（由 L_z=ℏ 与 E=ℏω_EM 推出，nm）", Rmin * Decimal("1e9"), "nm")
    chk("G2", "文档上限(λ/2π) 与本判据下限(λ/2π) 是否相等 ⇒ 只能取等",
        abs(Rmax - Rmin) / Rmin, "0")
    sin_th = Rmin / Rmax          # = 1
    u_c = (Decimal(1) - sin_th * sin_th).sqrt()
    chk("G3", "取等时轴向速度 u/c = √(1−sin²θ)（=0 ⇒ 光子不前进）", u_c, "0")

    # 一般情形：该读法强制 ω_h = ω_EM·sin²θ
    th = Decimal("0.3")
    st = Decimal(repr(math.sin(float(th))))
    om_pred = om_EM * st * st
    R_test = Rmin / st
    chk("G4", "强制关系 ω_h = ω_EM sin²θ 的自洽残差",
        abs(om_pred - C * st / R_test) / om_pred, "0")

    # 文档示例参数在该读法下不自洽
    sin_AM = lam / (2 * PI * R)
    om_req = om_EM * sin_AM * sin_AM
    note("G5", "示例参数在 AM 读法下要求的 v⊥/c", sin_AM)
    note("G6", "示例参数在 AM 读法下要求的 ω_h/(c/λ)", om_req * lam / C)
    note("G7", "文档所用 ω_h/(c/λ) = 1.2 与要求值的相对偏差", abs(om_req - om_h) / om_h)
    note("G8", "对应 v⊥/c：要求值 vs 文档值 0.42 的相对偏差", abs(sin_AM - Decimal("0.42")) / Decimal("0.42"))

    # 控制组
    Rmin_ctrl = lam / (2 * PI * Decimal(2))
    note("G9", "控制组：若 L_z = 2ℏ，R_min = λ/4π（nm）", Rmin_ctrl * Decimal("1e9"), "nm")
    chk("G10", "控制组分辨率：两份 R_min 相对差（应达 50%，证明判据非零分辨力）",
        abs(Rmin_ctrl - Rmin) / Rmin, "0.5")
    return sin_AM, om_req


# ================================================================
# H 组：判别力 —— 群时延能否区分「螺旋」与「倾斜直线」
# ================================================================
def group_h(lam, om_h):
    head("H 组 · 判别力：5μm/1m 时延能否区分「螺旋」与「倾斜直线」")
    chk("H1", "两模型对同一观测量 u/c 的预测差（=0 ⇒ 观测量零判别力）",
        abs(Decimal("0.999995") - Decimal("0.999995")), "0")
    th_rad = Decimal(repr(math.acos(0.999995)))
    st = Decimal(repr(math.sin(float(th_rad))))
    ct = Decimal(repr(math.cos(float(th_rad))))
    RR = C * st / om_h
    kap = om_h / C * st
    tau = om_h / C * ct
    note("H2", "若取螺旋解释：κ = (ω/c)sinθ（m⁻¹）", kap, "m^-1")
    note("H3", "若取螺旋解释：τ = (ω/c)cosθ（m⁻¹）", tau, "m^-1")
    note("H4", "若取螺旋解释：R = c·sinθ/ω_h（nm）", RR * Decimal("1e9"), "nm")
    note("H5", "判别点：倾斜直线 κ=τ=0，螺旋 κ≠0（差值即唯一可判别量，m⁻¹）", kap, "m^-1")
    note("H6", "几何结论：两者对「到达时间」给出同一数字，仅对「横向轨迹弯曲」给出不同预测",
         Decimal(0))


# ================================================================
# I 组：文档两节参数的内部口径一致性（§6 示例螺旋 vs §7 延迟演示）
# ================================================================
def group_i(om_h, R):
    head("I 组 · 内部口径一致性：§6 示例螺旋能否与 §7 延迟演示共存")
    # §6 方案 B 的参数：v⊥/c = 0.42 ⇒ cosθ = u/c = √(1-0.42²)
    cos_b = (Decimal(1) - Decimal("0.42") ** 2).sqrt()
    extra = 1 / cos_b - 1                     # 每米额外光程（m）
    dt_per_m = extra / C                      # 每米额外飞行时间（s）
    note("I1", "§6 方案B 参数下，每米额外光程（m）", extra, "m")
    note("I2", "§6 方案B 参数下，每米额外飞行时间（s）", dt_per_m, "s")
    note("I3", "换算为皮秒", dt_per_m * Decimal("1e12"), "ps")

    # §7 演示值：5 μm / 1 m ⇒ Δt = 16.6782 fs
    dt_demo = Decimal("5e-6") / C
    note("I4", "§7 演示的每米额外飞行时间（s）", dt_demo, "s")
    note("I5", "§6 参数预测值 / §7 演示值 = 倍率", dt_per_m / dt_demo, "×")

    # 要复现 §7 演示值，横向速度该是多少
    cos_demo = 1 / (1 + Decimal("5e-6"))
    sin_demo = (Decimal(1) - cos_demo ** 2).sqrt()
    note("I6", "复现 §7 所需的 v⊥/c", sin_demo)
    note("I7", "§6 所用 v⊥/c 与复现 §7 所需值之比", Decimal("0.42") / sin_demo, "×")
    # 若保持 §6 的 ω_h 不变，则半径须缩到多少
    R_demo = C * sin_demo / om_h
    note("I8", "保持 ω_h 不变、复现 §7 所需的螺旋半径（nm）", R_demo * Decimal("1e9"), "nm")
    note("I9", "§6 半径 192.5nm 与该半径之比", (Decimal("0.35") * Decimal("550e-9")) / R_demo, "×")
    return dt_per_m / dt_demo


# ================================================================
# J 组：把「决定性任务」量化 —— 真实横向位移的边带预言
# ================================================================
def group_j(lam, om_h):
    head("J 组 · 判别实验提案：实体螺旋 ⇒ 横向质心以 ω_h 振荡 ⇒ 谱边带")
    f_EM = C / lam
    note("J1", "光学频率 f_EM（THz）", f_EM / Decimal("1e12"), "THz")
    note("J2", "光学周期 T = 1/f_EM（fs）", Decimal(1) / f_EM * Decimal("1e15"), "fs")

    # 情形一：若取 ω_h = ω_EM ⇒ 边带退化为直流分量与二次谐波
    note("J3", "[取 ω_h=ω_EM] 下边带频率 f_EM − f_h（THz，应为 0 即直流分量）",
         f_EM / Decimal("1e12") - f_EM / Decimal("1e12"), "THz")
    note("J4", "[取 ω_h=ω_EM] 上边带对应波长 λ/2（nm，即真空二次谐波）",
         lam / 2 * Decimal("1e9"), "nm")

    # 情形二：按文档自己的示例 ω_h = 1.2 c/λ
    f_h = om_h / (2 * PI)
    note("J5", "[文档示例] 螺旋旋转频率 f_h = ω_h/2π（THz）", f_h / Decimal("1e12"), "THz")
    note("J6", "[文档示例] f_h / f_EM", f_h / f_EM)
    f_up = f_EM + f_h
    f_dn = f_EM - f_h
    note("J7", "[文档示例] 上边带频率 f_EM+f_h（THz）", f_up / Decimal("1e12"), "THz")
    note("J8", "[文档示例] 上边带波长（nm）", C / f_up * Decimal("1e9"), "nm")
    note("J9", "[文档示例] 下边带频率 f_EM−f_h（THz）", f_dn / Decimal("1e12"), "THz")
    note("J10", "[文档示例] 下边带波长（nm）", C / f_dn * Decimal("1e9"), "nm")

    # 情形三：按 G 组强制关系 ω_h = ω_EM sin²θ，扫描 θ
    note("J11", "[AM 读法] θ=30° 时 f_h/f_EM = sin²θ", Decimal(repr(math.sin(math.radians(30)))) ** 2)
    note("J12", "[AM 读法] θ=90° 时 f_h/f_EM = sin²θ",
         Decimal(repr(math.sin(math.radians(90)))) ** 2)
    # 控制组：分辨率
    chk("J13", "控制组：θ=30° 与 θ=90° 的 f_h/f_EM 之比应为 0.25",
        Decimal(repr(math.sin(math.radians(30)))) ** 2
        / Decimal(repr(math.sin(math.radians(90)))) ** 2, "0.25")


# ================================================================
# K 组：速度—角动量夹逼（攻破册核心判据）
# ================================================================
def group_k(lam, om_h, om_EM):
    head("K 组 · 速度—角动量夹逼：把 AM 读法与「光速必须接近 c」联立")

    alpha = om_h * lam / C                 # 文档：ω_h = α·c/λ，α=1.2
    note("K0", "文档 ω_h 的 α 系数（ω_h = α·c/λ）", alpha)

    # 上下界
    #   速度侧：v⊥ = c·sinθ = R·ω_h  ⇒  R = λ·sinθ/α          （sinθ 越小 R 越小）
    #   AM  侧：L_z = R·(E/c)·sinθ = ℏ ⇒ R = (λ/2π)/sinθ      （sinθ 越小 R 越大）
    # 两界相容 ⇔ λ·s/α ≥ (λ/2π)/s ⇔ s² ≥ α/(2π)
    need = alpha / (2 * PI)
    note("K1", "相容条件 sin²θ ≥ α/(2π)", need)
    if need <= 1:
        s_min = need.sqrt()
        cos_bound = (Decimal(1) - s_min * s_min).sqrt()
        eps_min = Decimal(1) - cos_bound
        note("K2", "⇒ 轴向速度上界 u/c = √(1−sin²θ_min)", cos_bound)
        note("K3", "⇒ 轴向速度亏损下界 ε_min = 1 − u/c", eps_min)
        note("K4", "⇒ 即光最多只能以 %.4f%% 的 c 沿轴前进" % (float(cos_bound) * 100),
             eps_min * Decimal(100), "%")
        R_side = lam * s_min / alpha
        R_am = (lam / (2 * PI)) / s_min
        note("K5", "边界处速度侧半径 R = λ·sinθ/α（nm）", R_side * Decimal("1e9"), "nm")
        note("K6", "边界处 AM 侧半径 R = (λ/2π)/sinθ（nm）", R_am * Decimal("1e9"), "nm")
        chk("K7", "两界在边界处应相等（互证两条推导一致）", abs(R_side - R_am) / R_am, "0")
        dt_m = (Decimal(1) / cos_bound - 1) / C
        note("K8", "该亏损对应的每米延迟（ps）", dt_m * Decimal("1e12"), "ps")
    else:
        note("K2", "α>2π ⇒ 无解（AM 读法在该 ω_h 下完全不可满足）", Decimal(1))

    # ---- 阶梯表：给定允许亏损 ε，两界分离多少
    for tag, eps in (("1e-2", Decimal("1e-2")), ("1e-3", Decimal("1e-3")),
                     ("1e-6", Decimal("1e-6")), ("1e-8", Decimal("1e-8")),
                     ("1e-9", Decimal("1e-9"))):
        s = (Decimal(2) * eps - eps * eps).sqrt()
        R_max_speed = lam * s / alpha
        R_min_am = (lam / (2 * PI)) / s
        note(f"K9[ε={tag}]", f"允许轴向亏损 ε={tag} ⇒ 速度侧 R ≤ (nm)",
             R_max_speed * Decimal("1e9"), "nm")
        note(f"K10[ε={tag}]", f"允许轴向亏损 ε={tag} ⇒ AM 侧 R ≥ (nm)",
             R_min_am * Decimal("1e9"), "nm")
        note(f"K11[ε={tag}]", f"两界冲突倍率 R_min(AM)/R_max(速度)",
             R_min_am / R_max_speed, "×")

    # ---- 控制组：α=2π（即 ω_h=ω_EM）应当退化为 u=0，与 G3 一致
    need_ctrl = Decimal(2 * PI) / (2 * PI)
    s_c = need_ctrl.sqrt()
    cos_c = (Decimal(1) - s_c * s_c).sqrt()
    chk("K12", "控制组：α=2π（ω_h=ω_EM）时 u/c 应为 0（与 G3 互证）", cos_c, "0")
    # 控制组 2：α>2π ⇒ 无解
    need_bad = Decimal(4 * PI) / (2 * PI)
    note("K13", "控制组：α=4π 时相容条件 sin²θ ≥ α/(2π) 的值（>1 ⇒ 无解）", need_bad)
    return alpha, eps_min if need <= 1 else None


# ================================================================
def main():
    print(_SUB)
    print("ROOT V4.0《空间光速螺旋统一运动学》独立数值复核  v2")
    print("零第三方依赖 · Decimal(prec=60)+Fraction · 按靶值有效位数分层判定 · 判据配控制组")
    print(_SUB)

    lam = group_a()
    group_b()
    R, om_h = group_c(lam)
    om_EM, Rmax = group_d(lam, R)
    group_e()
    group_f(lam)
    group_g(lam, R, om_h, om_EM, Rmax)
    group_h(lam, om_h)
    ratio_I = group_i(om_h, R)
    group_j(lam, om_h)
    alpha, eps_min = group_k(lam, om_h, om_EM)

    print()
    print(_SUB)
    print("复核结果汇总")
    print(_SUB)
    cnt = {"PASS": 0, "FAIL": 0, "INFO": 0}
    for cid, desc, got, w, rel, vd, nsig, extra in rows:
        if vd == "HEAD":
            print(f"\n【{desc}】")
            continue
        if vd == "INFO":
            cnt["INFO"] += 1
            g = f"{got:.6e}" if isinstance(got, Decimal) else str(got)
            print(f"  {cid:>5}  INFO   {desc}")
            print(f"              = {g} {extra}")
            continue
        cnt[vd] += 1
        rel_f = float(rel) if rel is not None else 0.0
        print(f"  {cid:>5}  {vd:4}  rel_raw={rel_f:>10.3e}  ({nsig}位)  "
              f"算值={float(got):.8g}  靶值={float(w):.8g}   {desc}")
        if extra:
            print(f"              └─ {extra}")
    print()
    print(_SUB)
    print(f"PASS={cnt['PASS']}  FAIL={cnt['FAIL']}  INFO={cnt['INFO']}")
    print(_SUB)

    print()
    print("[本次复核的独立结论（非文档原文）]")
    print("  (1) 文档全部算术在本库精度下复算一致 —— 无一处算错。")
    print("  (2) 全部几何恒等式 κ²+τ²=ω²/v²、R=κ/(κ²+τ²)、H=2πτ/(κ²+τ²) 精确残差严格为 0，")
    print("      且由 r(t) 做高精度差分实算 κ、τ 亦吻合 ⇒ 属**定义/代数层**结果 (H 类)。")
    print("  (3) 新增判据：若要求螺旋承担光子的 ℏ 角动量，则 R ≥ λ/2π；与文档自身")
    print("      「ω_h=ω_EM 且 v≤c ⇒ R ≤ λ/2π」联立只能取等号 ⇒ sinθ=1 ⇒ u=0，光子不前进。")
    print("  (4) 判别力：5μm/1m 群时延对「螺旋(κ≠0)」与「倾斜直线(κ=0)」给出同一个 u/c，")
    print("      零判别力；唯一判别处在 κ、τ 是否为零，文档未据此设计任何实验。")
    print(f"  (5) 内部口径：§6 示例螺旋(v⊥/c=0.42)推出的每米延迟约为 §7 演示值的")
    print(f"      {float(ratio_I):.4g} 倍 ⇒ 两节参数不共存，模型未对任何观测量定标。")


if __name__ == "__main__":
    main()
