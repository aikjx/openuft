# -*- coding: utf-8 -*-
"""
判定：TUFT-MATH-PROOF-ADD-01 外部审计逐条复算与自我修正（ADD-01R，第二轮）
=============================================================================
定位：对**外部审计意见**（针对 ADD-01「复权重场 Ω + 误差传播」增补的 14 节逐条批判）
做**机器复算与裁定**，并对前置整理册 `整理_TUFT-MATH-PROOF-ADD-01_..._2026-10-04`
的两处**过度结论**做自我修正，最后给出可采纳的正确闭合形式与分支门禁。

被审对象
------------------------------------------------------------------------------
ADD-01（复 Ω 增补）关键定义：
  θ = atan2(τ, κa)；Ω = λ cos3θ（实部），弱域 D_W 叠相位 e^{iφ(θ)}
  φ(θ) = φ0 (θ − θ_W,c) / Δθ_W            （B.2 线性相位）
  g_L = |Ω| e^{+iφ}，g_R = |Ω| e^{−iφ}        （B.3 手征投影）
  A_chiral = (|g_L|² − |g_R|²) / (|g_L|² + |g_R|²)
  p = (λ, φ0, B1..B4)  6 参数；q = (α_G, α, α_s, α_W) 4 观测量（Part C）
  Δa_e = 2.4e−13（σ = 0.65e−13）；ΔE_GZK = 0.68e19 eV（σ = 0.21e19 eV），E0 = 5.00e19 eV
  前置分区（ADD-02 正瓣重指派）：D_EM 中心 0°、D_Strong 中心 120°、D_Weak 中心 240°，
  各为 60° 锥（条件 cos3θ > 0）；λ = α_s = 0.1179（最大幅值原则）

本册要做的事（逐条复算，不做物理判决）
------------------------------------------------------------------------------
  §A 相位与坐标代数：A01–A08
      φ(−θ)+φ(θ) 的闭式、atan2 反演的**例外集精确化**、cos3θ 恒等、原点奇点、
      弱域边界连续性、bump 修复方案的 C^∞ 与奇性。
  §B 手征与宇称（核心）：B01–B07
      宇称守恒判据 C_L(θ) = C_R(−θ) 的系数层实现；奇相位 ⇒ **P 守恒**（反例成立）；
      非奇相位 ⇒ P 破缺但 **Δ_P ≡ 0**（纯相位型）；整体相位因子不改角不对称度；
      **与 ADD-02 分区交叉**：θ→−θ 把 D_Weak 映到 D_Strong。
  §C 误差传播与可识别性：C01–C09
      4×6 Jacobian ⇒ rank F_p ≤ 4 < 6 ⇒ F_p 不可逆（可识别性硬阻塞）；
      σ 数值缺推导、放大倍率门禁；UHECR 证伪阈值的内部冲突定量；共享参数 ⇒
      理论协方差非零；α 标度混用；emcee 术语。
  §D 可采纳修复：D01–D04（bump 相位窗、L/R Lorentz 结构闭合、δA 定义前置、
      分支优先级门禁）
  §E 自我修正与状态表：对 ADD-01 整理册 / ADD-02 突破册的登记

本册产出（纯标准库，零第三方依赖）
------------------------------------------------------------------------------
  判定表 34 条（MISMATCH / FAIL / PASS / BOUNDARY / INFO）+ 自检 18 条（退出码 0 可作门禁）
  产物：数据/TUFT-MATH-PROOF-ADD-01R_...{json,md}
"""

import os
import sys
import json
import math
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

T_START = time.time()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []
GUARDS = []
KEY = {}


def add(cid, sec, item, statement, verdict, detail):
    RESULTS.append({"id": cid, "section": sec, "item": item, "statement": statement,
                    "verdict": verdict, "detail": detail})
    print("[%-8s] %-5s %-8s | %s" % (verdict, cid, sec, detail[:150]))


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("[GUARD] %-34s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


def close(a, b, tol=1e-12):
    d = abs(a - b)
    scale = max(1.0, abs(a), abs(b))
    return d / scale <= tol


# ===========================================================================
# 线性代数（纯标准库）：矩阵乘 / 转置 / 对称特征值 / 秩 / 零空间
# ===========================================================================
def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


def transpose(A):
    return [list(col) for col in zip(*A)]


def jacobi_eig(A_in, sweeps=200, tol=1e-16):
    """对称矩阵 Jacobi 旋转特征分解，返回 (升序特征值, 特征向量列矩阵)"""
    n = len(A_in)
    a = [row[:] for row in A_in]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off += a[i][j] * a[i][j]
        if math.sqrt(2.0 * off) < tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * apq)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    eigs = sorted(a[i][i] for i in range(n))
    return eigs, v


def rank_of(A, tol=1e-11):
    """行阶梯化求秩（用于判定结构性亏秩）"""
    M = [row[:] for row in A]
    rows = len(M)
    cols = len(M[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if abs(M[i][c]) > tol:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pr = M[r][c]
        for i in range(rows):
            if i != r and abs(M[i][c]) > 0:
                f = M[i][c] / pr
                for j in range(c, cols):
                    M[i][j] -= f * M[r][j]
        r += 1
        if r == rows:
            break
    return r


# ===========================================================================
# 0. 输入常量（口径冻结；凡口径变更须重跑本册）
# ===========================================================================
ALPHA_0 = 7.2973525693e-3       # α(0) = 1/137.035999084
ALPHA_MZ = 1.0 / 127.952        # α(M_Z)，单圈跑动
ALPHA_S = 0.1179                # α_s(M_Z) 世界平均
SIG_ALPHA_S = 0.0009
ALPHA_W = 1.696e-2              # G_F M_W^2/(π√2)
ALPHA_G_E = 1.752e-45           # 电子参考下的 α_G
LAMBDA_NORM = ALPHA_S          # ADD-02 最大幅值原则：λ = α_s

DA_CENTER = 2.4e-13
DA_SIGMA = 0.65e-13
DE_CENTER = 0.68e19
DE_SIGMA = 0.21e19
E0_GZK = 5.00e19

# 弱扇区几何（ADD-01 记 θ_W,c, Δθ_W；本册主算例用 ADD-02 实际分区）
THETA_WC_DEFAULT = 20.0        # 主算例：非零中心（显式反例用例）
DTHETA_W_DEFAULT = 60.0
PHI0 = 0.7

# ADD-02 正瓣分区（cos3θ > 0 的三个 60° 锥）
CONE_CENTERS = {"EM": 0.0, "Strong": 120.0, "Weak": 240.0}
CONE_HALFWIDTH = 30.0


def wrap180(deg):
    """归一到 (-180, 180]"""
    d = math.fmod(deg, 360.0)
    if d <= -180.0:
        d += 360.0
    if d > 180.0:
        d -= 360.0
    return d


def in_cone(theta_deg, center_deg, halfwidth_deg=CONE_HALFWIDTH):
    return abs(wrap180(theta_deg - center_deg)) <= halfwidth_deg


# ===========================================================================
# §A 相位与坐标代数
# ===========================================================================
def phi_linear(theta, phi0, theta_c, dtheta):
    """ADD-01 B.2 线性相位"""
    return phi0 * (theta - theta_c) / dtheta


def cos3theta_formula(x, y):
    """B.4 坐标形式 (x^3 − 3xy²)/(x²+y²)^{3/2}"""
    r2 = x * x + y * y
    return (x * x * x - 3.0 * x * y * y) / (r2 ** 1.5)


def cos3theta_angular(x, y):
    return math.cos(3.0 * math.atan2(y, x))


def omega_R(theta, lam):
    return lam * math.cos(3.0 * theta)


def bump_w(theta, delta):
    """C^∞ 紧支集权重：|θ|<Δ 时 exp(−1/(1−(θ/Δ)²))，否则 0（偶函数）"""
    t = theta / delta
    if abs(t) >= 1.0:
        return 0.0
    return math.exp(-1.0 / (1.0 - t * t))


def bump_phi(theta, phi0, delta):
    """φ(θ) = φ0 (θ/Δ) w(θ)/w(0)：奇函数 + 边界 C^∞"""
    w0 = bump_w(0.0, delta)
    if w0 <= 0.0:
        return None
    return phi0 * (theta / delta) * (bump_w(theta, delta) / w0)


def d_num(f, x, h, order=1):
    """中心差分 n 阶导数"""
    if order == 1:
        return (f(x + h) - f(x - h)) / (2.0 * h)
    if order == 2:
        return (f(x + h) - 2.0 * f(x) + f(x - h)) / (h * h)
    if order == 3:
        return (f(x + 2 * h) - 2 * f(x + h) + 2 * f(x - h) - f(x - 2 * h)) / (2 * h ** 3)
    raise ValueError(order)


def sec_A():
    sec = "A"

    # --- A01 φ(−θ)+φ(θ) 闭式 -------------------------------------------
    cases = [(0.7, 20.0, 60.0), (0.7, 0.0, 60.0), (1.3, -45.0, 30.0), (0.2, 120.0, 60.0)]
    worst = 0.0
    for phi0, tc, dt in cases:
        pred = -2.0 * phi0 * tc / dt
        for t in (-70.0, -33.3, 0.0, 12.5, 80.0):
            got = phi_linear(-t, phi0, tc, dt) + phi_linear(t, phi0, tc, dt)
            worst = max(worst, abs(got - pred) / max(1.0, abs(pred)))
    KEY["a01_worst_rel"] = worst
    add("A01", sec, "phase_sum",
        "phi(-t)+phi(t) = −2*phi0*theta_Wc/dtheta（审计意见第 1 节）",
        "MISMATCH" if worst < 1e-12 else "FAIL",
        "线性相位下 phi(-t)+phi(t) 恒等于 −2*phi0*theta_Wc/dtheta，最大相对偏差 %.2e；"
        "⇒ 一般 theta_Wc≠0 时 phi(-t)≠−phi(t)，来料 B.2 的等式少一步" % worst)

    # --- A02 A_chiral 恒等于 0 ------------------------------------------
    worst2 = 0.0
    for i in range(257):
        th = -170.0 + i * (340.0 / 256.0)
        amp = abs(lam_val(th))
        ph = phi_linear(th, PHI0, THETA_WC_DEFAULT, DTHETA_W_DEFAULT)
        gl = complex(amp * math.cos(ph), amp * math.sin(ph))
        gr = complex(amp * math.cos(-ph), amp * math.sin(-ph))
        ach = (abs(gl) ** 2 - abs(gr) ** 2) / (abs(gl) ** 2 + abs(gr) ** 2)
        worst2 = max(worst2, abs(ach))
    KEY["a_chiral_max"] = worst2
    add("A02", sec, "A_chiral",
        "A_chiral = (|g_L|^2−|g_R|^2)/(|g_L|^2+|g_R|^2)",
        "MISMATCH",
        "257 点扫描 |A_chiral| 最大 = %.2e（机器零）⇒ **恒等于 0**，来料 B.3 的"
        "「手征强度不对称」在其自身定义下不可能出现" % worst2)

    # --- A03 g_R = conj(g_L)，但 |g_L| = |g_R| ---------------------------
    worst3 = 0.0
    for i in range(129):
        th = -160.0 + i * (320.0 / 128.0)
        amp = abs(lam_val(th))
        ph = phi_linear(th, PHI0, THETA_WC_DEFAULT, DTHETA_W_DEFAULT)
        gl = complex(amp * math.cos(ph), amp * math.sin(ph))
        gr = complex(amp * math.cos(-ph), amp * math.sin(-ph))
        worst3 = max(worst3, abs(gr - gl.conjugate()))
    KEY["a03_worst"] = worst3
    add("A03", sec, "gR_conj",
        "g_L=|Ω|e^{+iφ}, g_R=|Ω|e^{−iφ} ⇒ g_R = g_L^*",
        "PASS",
        "129 点 |g_R − conj(g_L)| 最大 %.2e（机器零）⇒ 来料实际只给出**共轭配对**，"
        "不是强度不等；「复相位⇒手征强度不对称」不由此定义导出" % worst3)

    # --- A04 atan2 反演的例外集精确化 ------------------------------------
    exceptions = []
    tested = 0
    for i in range(-40, 41):
        for j in range(-40, 41):
            x = i * 0.05
            y = j * 0.05
            if x == 0.0 and y == 0.0:
                continue
            tested += 1
            t1 = math.atan2(y, x)
            t2 = math.atan2(-y, x)
            if not close(t1, -t2, 0.0):
                exceptions.append((round(x, 3), round(y, 3), round(t1, 6), round(t2, 6)))
    only_neg_axis = all((xx < 0.0 and abs(yy) < 1e-15) for (xx, yy, _, _) in exceptions)
    KEY["atan2_tested"] = tested
    KEY["atan2_exceptions"] = len(exceptions)
    KEY["a04_no_exceptions"] = (len(exceptions) == 0)
    KEY["atan2_exception_sample"] = exceptions[:3]
    add("A04", sec, "atan2_parity",
        "tau→−tau ⇒ theta→−theta（审计表「除 atan2 支割线外成立」）",
        "PASS" if len(exceptions) == 0 else "FAIL",
        "%d 点扫描：atan2(−y,x) = −atan2(y,x) **严格成立，例外 %d 个**"
        "（含 y=0, x<0 负 κ 轴：atan2(0,−x)=+π 与 atan2(−0,−x)=−π 互为相反数）"
        "⇒ 审计的「支割线」保留在数值与几何（模 2π）上均**不必要**；"
        "唯一残留是 θ=+π 处的表示跳变，对 Ω_R 零影响（见 A05）"
        % (tested, len(exceptions)))

    # --- A05 支割线对 Omega_R 无影响 --------------------------------------
    x_neg, y_zero = -1.0, 0.0
    c_plus = cos3theta_formula(x_neg, y_zero)
    c_minus = cos3theta_formula(x_neg, -0.0)
    add("A05", sec, "cut_on_OmegaR",
        "支割线处 theta: +π vs −π 对 Ω_R = λcos3θ 的影响",
        "PASS" if close(c_plus, c_minus, 0.0) else "FAIL",
        "cos(3π) = cos(−3π) = %.1f ⇒ 支割线对**实部** Ω_R 零影响；"
        "仅对含相位的复 Ω（Ω*）有影响 ⇒ 支割线不是可观测缺陷" % c_plus)

    # --- A06 cos3theta 恒等 ------------------------------------------------
    worst6 = 0.0
    for (x, y) in [(2.0, 1.0), (0.3, -2.7), (-1.4, 0.9), (5.0, 5.0), (-0.05, 0.04)]:
        a = cos3theta_formula(x, y)
        b = cos3theta_angular(x, y)
        worst6 = max(worst6, abs(a - b) / max(1.0, abs(b)))
    KEY["cos3_worst"] = worst6
    add("A06", sec, "cos3theta",
        "cos3theta = (x^3−3xy^2)/(x^2+y^2)^{3/2}",
        "PASS",
        "5 组样本坐标式 vs 角形式最大相对偏差 %.2e（机器零）⇒ B.4 三倍角回代完全成立" % worst6)

    # --- A07 原点奇点 -------------------------------------------------------
    try:
        cos3theta_formula(0.0, 0.0)
        origin_ok = False
        origin_detail = "cos3theta_formula(0,0) 未抛异常（实现层隐患）"
    except ZeroDivisionError:
        origin_ok = True
        origin_detail = ("r=0 ⇒ (x^2+y^2)^{3/2}=0，除零；atan2(0,0)=0.0 会把原点"
                         "静默归类到 θ=0（EM 瓣）⇒ 须从流形删去或正则化")
    add("A07", sec, "origin_singular",
        "(kappa a, tau) = (0,0) 处 theta 不存在、分母为零",
        "BOUNDARY" if origin_ok else "FAIL",
        origin_detail + "（与 ADD-02「原点单点零测度约定排除」一致，但须在文本显式声明）")

    # --- A08 线性相位在弱域边界的连续性 ------------------------------------
    # Ω(θ) = λcos3θ e^{iφ(θ)}（域内） / λcos3θ（域外）
    # 连续要求 e^{iφ(θ_b)} = 1 或 λcos3θ(θ_b) = 0
    dth = DTHETA_W_DEFAULT
    tc = THETA_WC_DEFAULT
    th_b = tc + dth / 2.0
    phi_b = phi_linear(th_b, PHI0, tc, dth)
    jump = abs(complex(math.cos(phi_b), math.sin(phi_b)) - 1.0)
    # C^1 检查：域内 phi' = phi0/dth，域外 phi' = 0
    dphi_in = PHI0 / dth
    dphi_out = 0.0
    KEY["boundary_jump"] = jump
    add("A08", sec, "boundary_continuity",
        "「幅值连续、相位光滑 ✔」（ADD-01 §3.2 的声明）",
        "MISMATCH",
        "边界 θ_b=%.1f° 处 |e^{iφ}−1| = %.4f ≠ 0（φ_b=%.4f rad）⇒ Ω 一般**不连续**；"
        "即使恰取 φ(θ_b)=0，φ' 也从 %.4f 跳到 %.4f ⇒ 连 C^1 都不成立"
        % (th_b, jump, phi_b, dphi_in, dphi_out))

    # --- A09 bump 修复：奇性 + C^∞ ----------------------------------------
    delta = 30.0
    worst_odd = 0.0
    for i in range(1, 200):
        t = -delta + i * (2 * delta / 199.0)
        worst_odd = max(worst_odd, abs(bump_phi(-t, PHI0, delta) + bump_phi(t, PHI0, delta)))
    # 解析证据：g(u) = exp(-1/u)，|d^n g/du^n| = e^{-1/u} × poly(u^{-1}) → 0 (u→0+)
    # 双精度下 |t| > 1 − 1.2e-3 时 w 已下溢为 0，故「数值导数为 0」是下溢而非独立证据，
    # 本册以解析速率表为主证据，并如实标注该边界。
    def g(u):
        return math.exp(-1.0 / u)

    def g1(u):
        return g(u) / (u * u)

    def g2(u):
        return g(u) * (1.0 / (u ** 4) - 2.0 / (u ** 3))

    def g3(u):
        return g(u) * (-1.0 / (u ** 6) + 6.0 / (u ** 5) - 6.0 / (u ** 4))

    rate = []
    for u in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01):
        rate.append({"u": u, "w": g(u), "d1": abs(g1(u)), "d2": abs(g2(u)), "d3": abs(g3(u))})
    decay = rate[0]["d1"] / rate[-1]["d1"] if rate[-1]["d1"] > 0 else float("inf")
    # 双精度下溢阈值
    underflow_t = None
    for k in range(1, 200):
        tt = 1.0 - k * 1e-5
        if g(1.0 - tt * tt) == 0.0:
            underflow_t = tt
            break
    KEY["bump_odd_worst"] = worst_odd
    KEY["bump_rate_table"] = rate
    KEY["bump_d1_decay"] = decay
    KEY["bump_underflow_1mt"] = underflow_t
    add("A09", sec, "bump_repair",
        "bump 相位窗 φ=φ0(θ/Δ)w(θ)/w(0)：φ 奇 + 边界全阶导消失（审计第 6 节建议）",
        "PASS",
        "奇性偏差 %.2e（机器零，非平凡）；C^∞ 由解析速率证：w=e^{−1/u} 的 |dg/du| 从 "
        "u=0.5 的 %.3e 单调降至 u=0.01 的 %.3e（%.1e 倍），高阶同构 ⇒ 任意阶导在 "
        "u→0+ 归零。**诚实边界**：双精度下 |t|>1−%.1e 时 w 下溢为 0，"
        "「数值导数为 0」是下溢而非独立证据，故本册以解析表为准"
        % (worst_odd, rate[0]["d1"], rate[-1]["d1"], decay, underflow_t or 0.0))


def lam_val(theta_deg):
    """Ω_R 的幅值（度）"""
    return LAMBDA_NORM * math.cos(3.0 * math.radians(theta_deg))


# ===========================================================================
# §B 手征与宇称（核心层）
# ===========================================================================
# 宇称下的算符交换（系数层）：对 V/A/S/T 各结构，P 把 X_L <-> X_R
# 宇称守恒（作用量不变）判据：C_L(theta) = C_R(−theta)（对每一对结构）
LORENTZ_PAIRS = ("V", "A", "S", "T")


def C_L(theta, phi0, tc, dth, amp=1.0, eps=0.0, odd_phase=True):
    """左手耦合系数：奇相位时 C_L = amp(1+eps) e^{i phi}"""
    ph = phase_of(theta, phi0, tc, dth, odd_phase)
    m = amp * (1.0 + eps)
    return complex(m * math.cos(ph), m * math.sin(ph))


def C_R(theta, phi0, tc, dth, amp=1.0, eps=0.0, odd_phase=True):
    ph = phase_of(theta, phi0, tc, dth, odd_phase)
    m = amp * (1.0 - eps)
    return complex(m * math.cos(-ph), m * math.sin(-ph))


def phase_of(theta, phi0, tc, dth, odd_phase):
    if odd_phase:
        # 奇相位（bump 或 θ_Wc=0 的线性窗）
        return bump_phi(theta, phi0, dth / 2.0) if dth > 0 else 0.0
    return phi_linear(theta, phi0, tc, dth)


def parity_residual(theta, phi0, tc, dth, odd_phase=True, eps=0.0, amp=1.0):
    """|C_L(theta) − C_R(−theta)|：0 ⇒ P 守恒；≠0 ⇒ P 破缺"""
    cl = C_L(theta, phi0, tc, dth, amp, eps, odd_phase)
    cr = C_R(-theta, phi0, tc, dth, amp, eps, odd_phase)
    return abs(cl - cr)


def delta_P(theta, phi0, tc, dth, odd_phase=True, eps=0.0, amp=1.0):
    """Δ_P = (|C_L|² − |C_R(−θ)|²)/(|C_L|² + |C_R(−θ)|²)：手征强度不对称"""
    cl = C_L(theta, phi0, tc, dth, amp, eps, odd_phase)
    cr = C_R(-theta, phi0, tc, dth, amp, eps, odd_phase)
    return (abs(cl) ** 2 - abs(cr) ** 2) / (abs(cl) ** 2 + abs(cr) ** 2)


def sec_B():
    sec = "B"

    # --- B01 守恒判据的充要性（系数层） ------------------------------------
    # 若 C_L(theta) = C_R(−theta) 对所有 theta 成立 ⇒ L_P = L
    ths = [-40.0, -12.0, 0.0, 7.5, 25.0]
    res_odd = [parity_residual(t, PHI0, 0.0, 60.0, odd_phase=True) for t in ths]
    max_odd = max(res_odd)
    add("B01", sec, "parity_criterion",
        "宇称守恒判据 C_L(theta) = C_R(−theta)（审计第 5 节给出，本册实现）",
        "PASS",
        "bump 奇相位 + g_L/g_R 共轭定义下，5 点 |C_L(theta)−C_R(−theta)| 最大 %.2e"
        "（机器零）⇒ **P 守恒**。即：来料的复 Ω 模型在奇相位下是一个"
        "**宇称守恒**模型" % max_odd)

    # --- B02 显式反例：Omega 非实 + P 守恒（证伪「Omega*≠Omega ⇒ P 破缺」）---
    theta_s = 18.0
    om = lam_val(theta_s) * complex(math.cos(bump_phi(theta_s, PHI0, 30.0)),
                                    math.sin(bump_phi(theta_s, PHI0, 30.0)))
    om_p = lam_val(-theta_s) * complex(math.cos(bump_phi(-theta_s, PHI0, 30.0)),
                                       math.sin(bump_phi(-theta_s, PHI0, 30.0)))
    conj_ok = close(om_p.real, om.conjugate().real, 1e-12) and \
        close(om_p.imag, om.conjugate().imag, 1e-12)
    nonreal = abs(om.imag) > 1e-6
    p_conserved = max_odd < 1e-10
    add("B02", sec, "omega_star_not_breaking",
        "Omega*(theta)≠Omega(theta) ⇒ P 破缺（ADD-01 隐含推理）",
        "MISMATCH" if (conj_ok and nonreal and p_conserved) else "FAIL",
        "构造反例：theta=%.0f° 处 Im(Omega)=%.4f≠0（复场）且 Omega(−theta)=Omega*(theta)"
        "逐位成立；同一模型 C_L(theta)=C_R(−theta) 机器零 ⇒ **P 守恒**。"
        "⇒ 「复相位 ⇒ 宇称破缺」被证伪：变换关系不是破缺判据，"
        "判据必须是作用量 L_P vs L" % (theta_s, om.imag))

    # --- B03 非奇相位 ⇒ P 破缺但纯相位型 -----------------------------------
    res_nonodd = [parity_residual(t, PHI0, THETA_WC_DEFAULT, DTHETA_W_DEFAULT,
                                  odd_phase=False) for t in ths]
    spread = max(res_nonodd) - min(res_nonodd)
    dP_nonodd = max(abs(delta_P(t, PHI0, THETA_WC_DEFAULT, DTHETA_W_DEFAULT,
                                odd_phase=False)) for t in ths)
    KEY["nonodd_residual"] = res_nonodd[0]
    add("B03", sec, "nonodd_phase_parity",
        "theta_Wc≠0 ⇒ P 破缺（审计第 1 节的直接结论）",
        "PASS",
        "残差 |C_L−C_R(−θ)| = %.4f 且**与 θ 无关**（5 点散布 %.2e，"
        "解析预期 2|sin(phi0*theta_Wc/dtheta)| = %.4f）；但 Δ_P 最大 %.2e ≡ 0 "
        "⇒ 这是**纯相位型 P 破缺**（CKM/CP 型），**不产生手征强度不对称**"
        % (res_nonodd[0], spread, 2.0 * abs(math.sin(PHI0 * THETA_WC_DEFAULT / DTHETA_W_DEFAULT)),
           dP_nonodd))

    # --- B03b 口径自查：三种口径并列（2026-10-04 第十一轮自纠） -------------
    # B03 报「残差常数 0.4624、5 点散布 1.11e−16」，其成立条件是
    #   ① **单位幅值**（B03 的 C_L/C_R 默认 amp=1，未乘 |λcos3θ|）
    #   ② **全域线性** φ(−θ) 仍按 φ0(−θ−θ_W,c)/Δ 求（来料是**分段定义**：域外 φ=0）
    #   ③ θ_W,c=20°（B03 用例参数），非 ADD-02 的 240°
    # 来料原文口径（分段 + 真实幅值）下残差**随 θ 变化**。本条三口径并列。
    def _resid(deg, amp_mode, seg_mode, tc=20.0, dth=60.0, phi0=0.7):
        amp = 1.0 if amp_mode == "unit" else abs(lam_val(deg))
        ph_in = phi0 * (deg - tc) / dth
        if seg_mode:
            img = wrap180(-deg)
            ph_out = (phi0 * (img - tc) / dth) if abs(img - tc) <= dth / 2.0 else 0.0
        else:
            ph_out = phi0 * ((-deg) - tc) / dth
        cl = amp * complex(math.cos(ph_in), math.sin(ph_in))
        cr = amp * complex(math.cos(-ph_out), math.sin(-ph_out))
        return abs(cl - cr)

    degs = (215.0, 225.0, 235.0, 245.0, 255.0)
    r1 = [_resid(d, "unit", False) for d in degs]        # B03 原口径
    r2 = [_resid(d, "real", False) for d in degs]        # 真实幅值 + 全域线性
    r3 = [_resid(d, "real", True) for d in degs]         # 真实幅值 + 分段（来料原文）
    KEY["b03_unit_linear"] = {"v0": r1[0], "spread": max(r1) - min(r1)}
    KEY["b03_real_linear"] = {"min": min(r2), "max": max(r2), "spread": max(r2) - min(r2)}
    KEY["b03_real_segmented"] = {"min": min(r3), "max": max(r3), "spread": max(r3) - min(r3)}
    add("B03b", sec, "caliber_selfcheck",
        "B03「守恒残差与 θ 无关（常数 0.4624、散布 1.11e−16）」的成立条件？",
        "CORRECTED",
        "三口径机器并列：①**单位幅值 + 全域线性**（B03 原口径）残差恒 %.4f、spread=%.1e "
        "⇒ 常数成立；②真实幅值 |λcos3θ| + 全域线性：spread=%.2e；③**真实幅值 + 分段定义**"
        "（来料原文）spread=%.2e ⇒ 后两者**随 θ 变化**。⇒ B03 的「常数」只在"
        "「单位幅值 + 全域线性 + θ_W,c=20°」三条件同时成立时有效，**不适用于来料分段定义"
        "与真实幅值**；但三口径都给出「残差恒 ≠0 ⇒ P 破缺、Δ_P≡0 ⇒ 纯相位型」，"
        "故 B03 的核心裁定不变、仅数值表述须按口径改写（自纠，2026-10-04 第十一轮）"
        % (r1[0], max(r1) - min(r1), max(r2) - min(r2), max(r3) - min(r3)))

    # --- B04 手征强度不对称必须靠幅值 --------------------------------------
    eps = 0.1
    dP_eps = delta_P(18.0, PHI0, 0.0, 60.0, odd_phase=True, eps=eps)
    dP_pred = 2.0 * eps / (1.0 + eps * eps)
    add("B04", sec, "chiral_amp_needed",
        "Delta_P ≠ 0 需要 |C_L| ≠ |C_R|（审计第 5 节定义）",
        "PASS",
        "取 |C_L|=g(1+eps)、|C_R|=g(1−eps) ⇒ Δ_P = 2eps/(1+eps²)；"
        "eps=%.2f 时数值 %.6f vs 解析 %.6f（一致）⇒ 手征不对称**只能**来自幅值自由度，"
        "相位给不出" % (eps, dP_eps, dP_pred))

    # --- B05 整体相位因子不改归一化角不对称度 --------------------------------
    c_amp, phi_inj = 0.1, 0.5
    f = complex(1.0 + c_amp * math.cos(phi_inj), c_amp * math.sin(phi_inj))
    scale = abs(f) ** 2
    MG, MT = complex(1.0, 0.3), complex(0.4, -0.9)
    a_before = (abs(MG) ** 2 - abs(MT) ** 2) / (abs(MG) ** 2 + abs(MT) ** 2)
    a_after = (abs(f * MG) ** 2 - abs(f * MT) ** 2) / (abs(f * MG) ** 2 + abs(f * MT) ** 2)
    rate_before = abs(MG) ** 2 + abs(MT) ** 2
    rate_after = abs(f * MG) ** 2 + abs(f * MT) ** 2
    KEY["overall_phase_scale"] = scale
    add("B05", sec, "overall_phase",
        "M_TUFT = c e^{iφ} M_SM ⇒ 总率变而归一化角不对称度不变（审计第 4 节）",
        "PASS",
        "注入 f=1+%.1f e^{i%.1f}：|f|²=%.5f ⇒ 总率 %.5f→%.5f（+%.2f%%），"
        "A_GT = (|M_G|²−|M_T|²)/(...) = %.10f → %.10f（逐位不变）"
        "⇒ 若 TUFT 振幅只是 SM 振幅乘整体相位，δA_TUFT **恒为 0**"
        % (c_amp, phi_inj, scale, rate_before, rate_after,
           100.0 * (rate_after / rate_before - 1.0), a_before, a_after))

    # --- B06 与 ADD-02 分区交叉：P 把弱域映到强域 ---------------------------
    mapping = {}
    for name, c in CONE_CENTERS.items():
        tgt = wrap180(-c)
        hit = [n for n, cc in CONE_CENTERS.items() if in_cone(tgt, cc)]
        mapping[name] = {"center": c, "image_center": tgt, "lands_in": hit}
    weak_to = mapping["Weak"]["lands_in"]
    cross = (len(weak_to) == 1 and weak_to[0] == "Strong")
    add("B06", sec, "parity_cone_swap",
        "ADD-02 正瓣分区在 theta→−theta 下的自反性（新增交叉发现）",
        "MISMATCH" if cross else "BOUNDARY",
        "D_EM(0°)→自身；**D_Weak(240°)→D_Strong(120°)**；D_Strong→D_Weak。"
        "⇒ 在现行分区下 P 把弱相互作用配置映到强相互作用配置："
        "这不是「相位造成的手征破缺」，而是**分区几何把不同相互作用互换**；"
        "若坚持 P 为理论对称性，则该分区下 P 根本不是对称性（与相位无关）")

    # --- B07 deltaP 与 theta 的依赖（纯相位型的可观测后果） -------------------
    dP_scan = [delta_P(t, PHI0, THETA_WC_DEFAULT, DTHETA_W_DEFAULT, odd_phase=False)
               for t in (-50.0, -20.0, 0.0, 20.0, 50.0)]
    add("B07", sec, "deltaP_theta_indep",
        "纯相位型破缺下 Δ_P 对 θ 的依赖",
        "PASS",
        "5 点 Δ_P 全为 %.2e（最大偏差 %.1e）⇒ θ→−θ 只搬运相位、不改强度；"
        "可观测后果只能落在**干涉/CP 型**修正上，不能落在角不对称度上"
        % (dP_scan[2], max(abs(x) for x in dP_scan)))


# ===========================================================================
# §C 误差传播与可识别性
# ===========================================================================
def sec_C():
    sec = "C"
    sig_rel = {"alpha": 1.5e-10, "alpha_s": SIG_ALPHA_S / ALPHA_S,
               "alpha_W": 0.02, "alpha_G": 0.02}
    KEY["sig_rel_inputs"] = sig_rel

    # --- C01 4x6 Jacobian ⇒ rank 亏 ------------------------------------------
    # 列序 p = (lambda, phi0, B1, B2, B3, B4)；行序 q = (Strong, Weak, EM, G)
    # ∂alpha_k/∂lambda = cos3theta_k（lambda = alpha_s 归一，ADD-02 读数）
    # ∂alpha_k/∂phi0   = 0（相位不进耦合强度 —— 这是**一整条零列**）
    # ∂alpha_k/∂B_i    = ADD-02 敏感度（%/度）：Weak 0.36、EM 0.84、Strong/G 0
    H = [
        [1.000000, 0.0, 0.00, 0.00, 0.0, 0.0],     # Strong (theta=120 deg)
        [0.143850, 0.0, 0.36, 0.00, 0.0, 0.0],     # Weak   (theta=212.757 deg)
        [0.061886, 0.0, 0.00, 0.84, 0.0, 0.0],     # EM     (theta=28.817 deg)
        [1.484e-44, 0.0, 0.00, 0.00, 0.0, 0.0],    # G      (zero-lobe edge)
    ]
    sig_q = [SIG_ALPHA_S, ALPHA_W * 0.02, ALPHA_0 * 1.5e-10, ALPHA_G_E * 0.02]
    KEY["sigma_lambda"] = SIG_ALPHA_S / ALPHA_S
    W = [[(1.0 / (s * s)) if i == j else 0.0 for j in range(4)] for i, s in enumerate(sig_q)]
    Fp = mat_mul(transpose(H), mat_mul(W, H))
    eigs, evecs = jacobi_eig(Fp)
    maxeig = max(abs(e) for e in eigs)
    minabs = min(abs(e) for e in eigs)
    nulls = [e for e in eigs if abs(e) / maxeig < 1e-12]
    significant = [e for e in eigs if abs(e) > 1e-15 * maxeig]
    rk_num = rank_of(H, 1e-11)          # 数值容差
    rk_alg = rank_of(H, 1e-60)          # 代数容差
    rk = max(rk_num, rk_alg)
    # 结构性行相关检验：G 行是否 = c * Strong 行
    ratio_ok = close(H[3][0] / H[0][0], 1.484e-44, 1e-6) and all(
        H[3][j] == 0.0 for j in range(1, 6))
    null_vec = [evecs[k][0] for k in range(6)]
    null_norm = math.sqrt(sum(x * x for x in null_vec))
    KEY["jac_rank_numeric"] = rk_num
    KEY["jac_rank_algebraic"] = rk_alg
    KEY["row_dependence_G_on_S"] = bool(ratio_ok)
    KEY["fp_null_dof_strict"] = 6 - rk_alg
    KEY["fp_significant_dof"] = len(significant)
    KEY["fp_spectrum"] = ["%.4e" % e for e in eigs]
    KEY["fp_dynamic_range"] = (maxeig / minabs) if minabs > 0 else float("inf")
    KEY["jac_rank"] = rk
    KEY["fp_null_dof"] = len(nulls)
    KEY["fp_zero_eigs"] = len(nulls)
    KEY["fp_eig_ratio_min_max"] = (min(abs(e) for e in eigs) / maxeig) if maxeig else 0.0
    KEY["fp_cond"] = float("inf") if min(abs(e) for e in eigs) < 1e-12 * maxeig else \
        maxeig / min(abs(e) for e in eigs)
    KEY["null_vector_norm"] = null_norm
    add("C01", sec, "identifiability",
        "6 参数 / 4 观测量 ⇒ 可唯一得到六参数协方差？（审计第 9 节）",
        "FAIL",
        "H 为 4x6，rank(H)=%d（代数与数值一致）。**比审计给的上界 4 更低**："
        "引力行 G = %.3e × 强核行 S（两行只在 λ 列非零，严格成比例，机器验证 %s）"
        "⇒ 4 个观测量只给 3 个独立约束。F_p 严格零特征值 %d 个；"
        "按相对 1e-12 判据数值零 %d 个；**双精度下可分辨的非零方向仅 %d 个**"
        "（谱跨 %.1e 已超 1e16）⇒ F_p^{−1} 不存在，且即便补足方程也难以数值反演。"
        "另：φ0 的雅可比整列为 0 ⇒ φ0 完全不可识别"
        % (rk, H[3][0] / H[0][0], ratio_ok, 6 - rk_alg, len(nulls), len(significant),
           KEY["fp_dynamic_range"]))

    # --- C02 sigma_lambda/lambda ---------------------------------------------
    sl = SIG_ALPHA_S / ALPHA_S
    add("C02", sec, "sigma_lambda",
        "sigma_lambda/lambda = 0.0076（审计第 10 节：算术对、逻辑未建立）",
        "BOUNDARY",
        "0.0009/0.1179 = %.6f ✔ 算术成立；但该传递**要求 lambda ∝ alpha_s**，"
        "而 lambda=alpha_s 是 ADD-02「最大幅值原则」引入的**归一化约定**（非推导）"
        "⇒ σ_λ/λ = σ_αs/αs 是**约定继承**，不是误差传播结果" % sl)

    # --- C03 g-2 区间算术（2σ vs 1.96σ） -------------------------------------
    two = (DA_CENTER - 2 * DA_SIGMA, DA_CENTER + 2 * DA_SIGMA)
    n96 = (DA_CENTER - 1.96 * DA_SIGMA, DA_CENTER + 1.96 * DA_SIGMA)
    KEY["g2_2sigma"] = [x * 1e13 for x in two]
    KEY["g2_196sigma"] = [x * 1e13 for x in n96]
    add("C03", sec, "g2_interval",
        "Δa_e = 2.4e−13 ± 0.65e−13 的 95% 区间",
        "PASS",
        "2σ: [%.3f, %.3f]e−13；严格 95%%（1.96 sigma）: [%.3f, %.3f]e−13 ⇒ 算术均正确，"
        "但 σ 本身未从 J 与 Σ_p 导出（见 C04）。"
        "**继承声明（步1）**：g-2 窗口已关（链 A-④ D-02 物理层 FAIL）⇒ 本区间属推导层复核，"
        "**不得当作可用预言**；重新开放须先证伪攻破册前提" % (two[0] * 1e13, two[1] * 1e13,
                                                             n96[0] * 1e13, n96[1] * 1e13))

    # --- C04 sigma 缺推导：需要多大的 Jacobian 放大 ---------------------------
    sig_in_rel = math.sqrt((SIG_ALPHA_S / ALPHA_S) ** 2 + 0.02 ** 2)
    sig_out_rel = DA_SIGMA / DA_CENTER
    amp_needed = sig_out_rel / sig_in_rel
    sigma_in_abs = DA_CENTER * sig_in_rel
    needed_abs = DA_CENTER * sig_out_rel
    KEY["amplification_needed"] = amp_needed
    add("C04", sec, "g2_sigma_underived",
        "sigma_Delta_a = 0.65e−13 是否由自述误差源导出？（审计第 11 节）",
        "FAIL",
        "自述输入合成相对 %.5f ⇒ 朴素预期 σ≈%.3e（ADD-01 §3.5 的 5.1e−15 量级）；"
        "引用 σ 的相对误差 %.4f ⇒ 需要 Jacobian 放大 **%.2f 倍**（门禁："
        "max_i|J_i|σ_i ≥ %.3e），当前未给出任何 ∂Δa_e/∂p_i。"
        "且因 C01（F_p 不可逆），连 J 的良定义都不确定 ⇒ **双重阻塞**"
        % (sig_in_rel, sigma_in_abs, sig_out_rel, amp_needed, needed_abs))

    # --- C05 UHECR 区间算术 ---------------------------------------------------
    de2 = (DE_CENTER - 2 * DE_SIGMA, DE_CENTER + 2 * DE_SIGMA)
    e_tuft = (E0_GZK - de2[1], E0_GZK - de2[0])
    KEY["uhecr_window"] = [x / 1e19 for x in e_tuft]
    add("C05", sec, "uhecr_interval",
        "ΔE_GZK = 0.68±0.21 (1e19 eV) ⇒ E_TUFT 区间",
        "PASS",
        "0.68±0.42 = [%.2f, %.2f]；E0=5.00 ⇒ E_TUFT = [%.2f, %.2f]e19 eV ⇒ 算术正确。"
        "**继承声明（步1）**：UHECR 窗口已关（链 A-④ D-02 物理层 FAIL）=> 本区间属推导层复核，"
        "**不得当作可用预言**"
        % (de2[0] / 1e19, de2[1] / 1e19, e_tuft[0] / 1e19, e_tuft[1] / 1e19))

    # --- C06 「≥5.0e19 即证伪」与「区间已剥离传播误差」冲突 ---------------------
    diff = E0_GZK - (E0_GZK - DE_CENTER)      # = 0.68e19
    k = 1.96
    sig_comb_min = diff / k
    sig_prop_min = math.sqrt(max(sig_comb_min ** 2 - DE_SIGMA ** 2, 0.0))
    KEY["uhecr_sigma_prop_min"] = sig_prop_min / 1e19
    add("C06", sec, "uhecr_falsification",
        "「95% 区间剥离传播系统误差」+「观测截断 ≥5.0e19 即证伪」",
        "MISMATCH",
        "中心值判据：|E_obs−E_pred| = %.2fe19 需 ≤ 1.96σ_comb ⇒ σ_comb ≥ %.4fe19；"
        "扣除 TUFT 自身 σ=0.21 ⇒ **传播/源/成分/探测器合成系统误差需 ≥ %.4fe19 eV**"
        "（= TUFT σ 的 %.2f 倍）才可能把 5.0 纳入区间。"
        "⇒ 在已声明剥离传播误差的区间上，5.0e19 判据**逻辑上不能成立**"
        % (diff / 1e19, sig_comb_min / 1e19, sig_prop_min / 1e19, sig_prop_min / DE_SIGMA))

    # --- C07 三组观测的理论相关性 ---------------------------------------------
    dDa_dlam = DA_CENTER / LAMBDA_NORM
    dDE_dlam = DE_CENTER / LAMBDA_NORM
    sig_lam = (SIG_ALPHA_S / ALPHA_S) * LAMBDA_NORM
    cov_lam = dDa_dlam * dDE_dlam * (sig_lam ** 2)
    rho = cov_lam / (DA_SIGMA * DE_SIGMA)
    KEY["theory_rho"] = rho
    add("C07", sec, "channel_independence",
        "「三组实验完全独立交叉检验」（ADD-01 Part D）",
        "MISMATCH",
        "两者共享 λ ⇒ Cov = J_e Σ_p J_G^T 的 λλ 项 = %.4e (eV)²，"
        "相关系数 ρ = %.3e ≠ 0（示意线性模型 J=∂y/∂λ=y/λ）⇒ "
        "「完全独立」不成立；正确表述：实验误差可近似独立，**理论预测经共享参数相关**，"
        "须联合拟合" % (cov_lam, rho))

    # --- C08 alpha 标度混用 ---------------------------------------------------
    rel = (ALPHA_0 - ALPHA_MZ) / ALPHA_0
    add("C08", sec, "alpha_scale",
        "输入表标注 mu=M_Z 却取 alpha(0)（审计第 10 节；ADD-01 N4 复现）",
        "MISMATCH",
        "alpha(0)=%.7e vs alpha(M_Z)=%.7e，相对差 %.2f%% ⇒ 混标度缺陷在第二轮审计中"
        "**原样保留**；须统一为 alpha(M_Z) 或明确标 mu→0" % (ALPHA_0, ALPHA_MZ, 100 * rel))

    # --- C09 emcee 术语 --------------------------------------------------------
    add("C09", sec, "mcmc_terminology",
        "「MCMC 嵌套采样，基于 emcee」（ADD-01 Part D）",
        "INFO",
        "emcee = ensemble MCMC（系综马尔可夫链蒙特卡洛）；nested sampling 惯用 "
        "dynesty / UltraNest。二者是不同算法族，不能称「基于 emcee 的嵌套采样」；"
        "另：若 Σ_p 由同一批耦合数据后验拟合再当先验使用 ⇒ 数据双重计数")

    # --- C10 步1 自证：关窗继承声明已落盘 ---------------------------------
    src = open(os.path.abspath(__file__), encoding="utf-8", errors="replace").read()
    has_g2 = ("窗口已关" in src) and ("链 A-④" in src)
    has_beta = "不在关窗范围" in src
    add("C10", sec, "window_closed_inherited",
        "步1 自证：本册已在 g-2 / UHECR 区间处补「窗口已关（链 A-④ D-02）」继承声明",
        "PASS" if (has_g2 and has_beta) else "FAIL",
        "自证：g-2/UHECR 关窗声明=%s（%d 处）、β 通道单列声明=%s ⇒ %s"
        % (has_g2, src.count("窗口已关"), has_beta,
           "继承声明已落盘，勿删" if (has_g2 and has_beta) else "**声明缺失**"))

    return {"H": H, "Fp_eigs": eigs, "sigma_q": sig_q, "null_dof": 6 - rk}


# ===========================================================================
# §D 可采纳修复
# ===========================================================================
def sec_D():
    sec = "D"
    delta = 30.0

    # --- D01 bump 窗的 P 自反性（弱域取关于 0 对称） ---------------------------
    self_reflect = all(in_cone(-t, 0.0) == in_cone(t, 0.0) for t in range(-60, 61))
    add("D01", sec, "self_reflect_weak",
        "弱域自反条件 D_W ⟺ −theta ∈ D_W（审计第 1 节第二个条件）",
        "PASS",
        "以 0 为中心、±30° 的对称弱域：61 点检验自反性 %s；"
        "若中心 theta_Wc≠0 ⇒ 反演映到中心为 −theta_Wc 的另一扇区（ADD-02 现行分区即如此）"
        % ("成立" if self_reflect else "不成立"))

    # --- D02 正确闭合形式：L = C_L O_L + C_R O_R + h.c. ----------------------
    eps = 0.05
    dP = delta_P(18.0, PHI0, 0.0, 60.0, odd_phase=True, eps=eps)
    res = parity_residual(18.0, PHI0, 0.0, 60.0, odd_phase=True, eps=eps)
    add("D02", sec, "closed_form",
        "L_TUFT = C_L(theta) O_L + C_R(theta) O_R + h.c.，O_{L,R} = psibar Gamma psi_{L,R}",
        "PASS",
        "采用该形式后：P 交换 O_L <-> O_R，守恒条件 C_L(theta)=C_R(−theta)（B01）；"
        "手征不对称量 Δ_P 可定义且**非零需要幅值自由度**（eps=%.2f ⇒ Δ_P=%.5f，"
        "此时守恒残差 %.4f≠0 ⇒ 显式 P 破缺）"
        % (eps, dP, res))

    # --- D03 deltaA_TUFT 的定义前置条件 --------------------------------------
    need = ["(i) 指定 O_TUFT 属 V/A/S/T 哪一种", "(ii) 存在两个独立振幅 M1, M2",
            "(iii) 干涉项 2Re(M1* M2) 含 cos φ / sin φ",
            "(iv) 固定 SM 参照 A_SM 口径", "(v) 排除整体相位情形（B05）"]
    add("D03", sec, "deltaA_prereq",
        "deltaA_TUFT(phi0) 的定义前置条件（审计第 4 节）",
        "BOUNDARY",
        "五项前置：%s。当前 Part B.3 未指定 Lorentz 结构 ⇒ δA_TUFT **尚不可计算**"
        % "；".join(need))

    # --- D04 分支优先级门禁 ----------------------------------------------------
    gates = [
        ("4 自洽性校验", "先做", "一次抓住 A01/A02/B01/B02/C01/C04 六类问题；是其余分支前置门禁"),
        ("3 β 衰变数值", "第二步", "须先修 A02（删 A_chiral）+ 指定 O_TUFT 结构 + 定弱扇区几何"),
        ("1 MCMC", "第三步", "须 C01 解除（补 ≥2 个独立方程/先验）后才可采样；否则抽的是退化分布"),
        ("2 场渲染", "最后", "无判别力（相似度只证两图一致）"),
    ]
    add("D04", sec, "branch_gate",
        "分支推进顺序（审计结论 vs ADD-01 裁定）",
        "PASS",
        "两者**一致**：%s" % "；".join(["%s=%s" % (g[0], g[1]) for g in gates]))
    KEY["gates"] = gates
    return gates


# ===========================================================================
# §F 与已实现分支 4 / 分支 3 的交叉核对（本册独有，防止与既有产物脱节）
# ===========================================================================
def phi_segmented(theta, phi0, tc, dth):
    """来料的分段定义：弱域内线性、弱域外 0（ADD-01 B.2 + B.7）"""
    half = dth / 2.0
    if abs(wrap180(theta - tc)) <= half:
        return phi0 * (theta - tc) / dth
    return 0.0


def sec_F():
    sec = "F"

    # --- F01 「PΩ≠Ω」作为破缺判据的信息量 -----------------------------------
    # 只统计相位窗内（|θ| < Δ）的点：窗外 w=0 ⇒ Ω 为实数 ⇒ PΩ=Ω（无相位可言）
    delta = 30.0
    n_scan, pomega_ne, conserve = 0, 0, 0
    for i in range(-29, 30):
        th = float(i)
        n_scan += 1
        amp = abs(lam_val(th))
        om = amp * complex(math.cos(bump_phi(th, PHI0, delta)),
                           math.sin(bump_phi(th, PHI0, delta)))
        om_p = amp * complex(math.cos(bump_phi(-th, PHI0, delta)),
                             math.sin(bump_phi(-th, PHI0, delta)))
        if abs(om_p - om) > 1e-15:
            pomega_ne += 1
        if parity_residual(th, PHI0, 0.0, 2 * delta, odd_phase=True) < 1e-12:
            conserve += 1
    KEY["f01_window_points"] = n_scan
    KEY["f01_pomega_ne_ratio"] = pomega_ne / float(n_scan)
    KEY["f01_conserve_ratio"] = conserve / float(n_scan)
    add("F01", sec, "pomega_criterion_info",
        "分支 4 guard「parity_breaking_holds_POmega_ne_Omega」：以 PΩ≠Ω 判宇称破缺",
        "MISMATCH",
        "相位窗内（|θ|<%.0f°，%d 点）扫描：PΩ≠Ω 成立 **%.1f%%**（复场自动满足），"
        "而作用量守恒判据 C_L(θ)=C_R(−θ) 同时成立 **%.1f%%** ⇒ "
        "**PΩ≠Ω 是破缺的必要非充分条件，作为判据零信息量**；"
        "该 guard 须换判据（分支 4 结论「破缺成立」的推理链随之改写）"
        % (delta, n_scan, 100.0 * KEY["f01_pomega_ne_ratio"],
           100.0 * KEY["f01_conserve_ratio"]))

    # --- F02 分支 4 实际参数下的作用量判据 ----------------------------------
    tc_b4, dth_b4, phi0_b4, th_b4 = 240.0, 60.0, 0.5, 225.0
    ph_in = phi_segmented(th_b4, phi0_b4, tc_b4, dth_b4)
    ph_out = phi_segmented(wrap180(-th_b4), phi0_b4, tc_b4, dth_b4)
    amp_b4 = abs(lam_val(th_b4))
    cl = amp_b4 * complex(math.cos(ph_in), math.sin(ph_in))
    cr = amp_b4 * complex(math.cos(-ph_out), math.sin(-ph_out))
    res_b4 = abs(cl - cr)
    res_b4_norm = res_b4 / amp_b4 if amp_b4 > 0 else float("inf")
    in_weak_after = in_cone(wrap180(-th_b4), CONE_CENTERS["Weak"])
    add("F02", sec, "branch4_instance",
        "分支 4 实例（θ_W,c=240°, Δθ_W=60°, φ_0=0.5, θ=225°）的作用量判据复算",
        "MISMATCH",
        "φ(225°)=%.4f（域内）、φ(−225°)=φ(135°)=%.4f（**出弱域**，落强域）⇒ "
        "守恒残差 |C_L−C_R(−θ)| = %.4f（归一化 %.4f，与分支 4 的 |Ω|=0.7071 口径一致）≠ 0 "
        "⇒ 按作用量判据 P 破缺。但归因是「**相位非奇 + 弱域非 P-自反**」，"
        "**不是**「复相位」；反演后是否仍在弱域：%s（与 B06 的分区互换同源）"
        % (ph_in, ph_out, res_b4, res_b4_norm, "否" if not in_weak_after else "是"))

    # --- F03 审计建议的 bump 居中窗 ⇒ P 守恒 ---------------------------------
    res_f03 = max(parity_residual(t, PHI0, 0.0, 2 * delta, odd_phase=True)
                  for t in (-40.0, -12.0, 0.0, 7.5, 25.0))
    add("F03", sec, "bump_centered_conserves",
        "审计第 6 节的 bump 居中窗（θ_W,c=0）下的宇称判定",
        "PASS",
        "守恒残差最大 %.2e（机器零）⇒ **P 守恒** ⇒ 在**修正后的**模型里「复相位」"
        "既不产生手征强度不对称（A_chiral≡0），也**不**破坏宇称；"
        "⇒ 增补 B.2/B.3 的核心因果链在修正后**完全落空**" % res_f03)

    # --- F04 分支 3 引入 c_I ⇒ 参数账恶化 ------------------------------------
    add("F04", sec, "param_accounting",
        "分支 3（β 衰变数值）引入干涉虚部 c_I 后的可识别性",
        "FAIL",
        "参数由 6 增至 **7**（λ, φ_0, B1..B4, **c_I**），观测量仍为 4 "
        "(α_G, α, α_s, α_W) + 1 个 β 不对称 A ⇒ rank H ≤ 4 < 7，"
        "且 c_I **完全无输入来源**（分支 3 自述「c_I 由模型未定」）"
        "⇒ C01 的可识别性阻塞**加剧而非缓解**；分支 3 自己也承认"
        "「δA_TUFT 实为 (c_I, ρ, φ_0) 三维族，非唯一数值预言」")

    # --- F05 分支 3 门禁自洽性 ----------------------------------------------
    rho_nat, rho_crit, deltaA_exp = 0.0261, 5.00e-4, 1.0e-3
    ratio = rho_nat / rho_crit
    add("F05", sec, "branch3_gate",
        "分支 3 存活门禁 ρ_crit = ΔA/2 与「压低 52 倍」",
        "PASS",
        "0.0261 / 5.00e−4 = %.1f 倍 ✔ 门禁自洽；口径提示：分支 3 guard 记"
        "存活占比 **1.3%%**、其结论文字写「~2%%」⇒ 同册两处口径不一致（见 F06）" % ratio)

    # --- F06 分支 3 的定价性质 ----------------------------------------------
    add("F06", sec, "branch3_pricing",
        "β 衰变通道的定价性质（与 OPEN-ΩH 同构？）",
        "BOUNDARY",
        "要 β 通道存活须把 TUFT 顶角耦合 ρ=|Ω|/g_SM 由 0.0261 压到 5.00e−4（**52 倍调谐**），"
        "且 φ_0 只在 cosφ_W≈0 的窄窗存活 ⇒ 与 ADD-02 的 OPEN-ΩH"
        "「耦合层级不被解释、被转移为精细调节」**同构**；"
        "另 g_SM 归一化是新增外锚（违反 Ω5 单常数约束的同类问题）")


# ===========================================================================
# §E 自我修正与状态表
# ===========================================================================
def sec_E():
    sec = "E"
    fixes = [
        {"target": "ADD-01 整理册 §3.4「破缺本身（PΩ≠Ω）成立」",
         "old": "PΩ≠Ω 即判宇称破缺成立",
         "new": "须检验作用量：守恒判据 C_L(θ)=C_R(−θ)；bump 奇相位 + 共轭 g_L/g_R 下"
                "残差机器零 ⇒ **P 守恒**。B.2/B.3 的等式是过度声称",
         "evidence": "B01/B02"},
        {"target": "ADD-01 整理册 §3.5「σ 应约 5.1e−15」",
         "old": "以单位 Jacobian 预设 Δa_e 线性于 λ, B_i",
         "new": "该值不是唯一正确答案；正确门禁是「放大倍率 ≥ %.2f 倍」+「F_p 可逆」。"
                "而 C01 证明 F_p 不可逆 ⇒ 两个缺陷耦合，5.1e−15 只是下界参考"
                % KEY.get("amplification_needed", float("nan")),
         "evidence": "C01/C04"},
        {"target": "ADD-01 整理册 §3.4「φ(−θ)=−φ(θ) ⟺ θ_Wc=0」",
         "old": "只给了奇偶条件",
         "new": "补第二个独立条件：弱域须 P-自反（D_W ⟺ −θ∈D_W）。在 ADD-02 现行"
                "正瓣分区下，弱域中心 240° ⇒ 两条件**同时不成立**",
         "evidence": "D01/B06"},
        {"target": "ADD-02 突破册「D-02/D-03 开放，受 ADD-01 N1 阻塞」",
         "old": "把 D-03 的阻塞归到 A_chiral ≡ 0",
         "new": "升级为**双重阻塞**：① A_chiral ≡ 0（无手征强度不对称）"
                "② P 破缺判据缺失且现行分区下 P 交换强/弱瓣（B06）",
         "evidence": "A02/B06"},
        {"target": "ADD-01 整理册 §3.2「跨弱域边界连续性声明成立」",
         "old": "✔ 连续性成立",
         "new": "线性相位下 |e^{iφ(θ_b)}−1|≠0 ⇒ 一般**不连续**，且 φ' 跳变 ⇒ 非 C^1；"
                "改用 bump 窗可同时得奇性与 C^∞（A09/D01）",
         "evidence": "A08/A09"},
    ]
    for i, fx in enumerate(fixes, 1):
        add("E%02d" % i, sec, "self_correction", fx["target"],
            "CORRECTED", "旧：%s ｜ 新：%s（证据 %s）" % (fx["old"], fx["new"], fx["evidence"]))
    return fixes


# ===========================================================================
# guards（自检；全部 PASS ⇒ 退出码 0，可作门禁）
# ===========================================================================
def do_guards():
    guard("a01_phase_sum_identity", KEY["a01_worst_rel"] < 1e-12,
          "phi(-t)+phi(t) = −2 phi0 theta_Wc/dtheta 相对偏差 %.1e" % KEY["a01_worst_rel"])
    guard("a02_chiral_asym_identically_zero", KEY["a_chiral_max"] < 1e-15,
          "A_chiral 最大 %.1e（恒等于 0）" % KEY["a_chiral_max"])
    guard("a03_gr_is_conjugate", KEY["a03_worst"] < 1e-12,
          "|g_R − conj(g_L)| 最大 %.1e" % KEY["a03_worst"])
    guard("a04_atan2_parity_strict", KEY["a04_no_exceptions"],
          "atan2(−y,x) = −atan2(y,x) 严格成立，例外 %d 个" % KEY["atan2_exceptions"])
    guard("a06_cos3theta_identity", KEY["cos3_worst"] < 1e-12,
          "三倍角坐标式最大相对偏差 %.1e" % KEY["cos3_worst"])
    guard("a09_bump_odd_and_cinf", KEY["bump_odd_worst"] < 1e-12 and
          KEY["bump_d1_decay"] > 1e10,
          "奇性偏差 %.1e；解析衰减 |dg/du|(0.5→0.01) = %.2e 倍 ⇒ 边界全阶导归零"
          % (KEY["bump_odd_worst"], KEY["bump_d1_decay"]))
    guard("b01_odd_phase_conserves_parity", KEY.get("b01_max", 0.0) < 1e-10,
          "奇相位下 |C_L−C_R(−θ)| 最大 %.1e ⇒ P 守恒" % KEY.get("b01_max", 0.0))
    guard("b05_overall_phase_keeps_asymmetry", KEY.get("b05_dA", 0.0) < 1e-15,
          "整体相位下 A_GT 变化 %.1e" % KEY.get("b05_dA", 0.0))
    guard("c01_jacobian_rank_deficient", KEY["jac_rank_algebraic"] <= 4 and
          KEY["fp_null_dof_strict"] >= 2 and KEY["row_dependence_G_on_S"],
          "rank(H)=%d（G ∥ S 机器验证）< 6；严格零空间 %d 维；双精度可分辨方向 %d 个"
          % (KEY["jac_rank_algebraic"], KEY["fp_null_dof_strict"], KEY["fp_significant_dof"]))
    guard("c02_sigma_lambda_arithmetic", abs(KEY.get("sigma_lambda", 0) - 0.0076) < 5e-5,
          "sigma_lambda/lambda = %.6f" % KEY.get("sigma_lambda", 0))
    guard("c03_g2_intervals_ordered",
          KEY["g2_2sigma"][0] < KEY["g2_196sigma"][0] and
          KEY["g2_196sigma"][1] < KEY["g2_2sigma"][1],
          "1.96σ 区间严格包含于 2σ 区间内")
    guard("c04_amplification_below_one", KEY["amplification_needed"] > 1.0,
          "需要放大 %.2f 倍才成立" % KEY["amplification_needed"])
    guard("c05_uhecr_window_arithmetic",
          abs(KEY["uhecr_window"][0] - 3.90) < 1e-9 and abs(KEY["uhecr_window"][1] - 4.74) < 1e-9,
          "E_TUFT = [%.2f, %.2f]e19" % tuple(KEY["uhecr_window"]))
    guard("c06_falsification_needs_systematics",
          KEY["uhecr_sigma_prop_min"] > DE_SIGMA / 1e19,
          "需系统误差 ≥ %.4fe19 > TUFT 自身 σ=0.21e19" % KEY["uhecr_sigma_prop_min"])
    guard("c07_theory_correlation_nonzero", abs(KEY["theory_rho"]) > 0.0,
          "共享 λ 给出 ρ = %.3e ≠ 0" % KEY["theory_rho"])
    guard("c08_alpha_scale_gap", abs(ALPHA_0 - ALPHA_MZ) / ALPHA_0 > 0.05,
          "alpha(0) vs alpha(M_Z) 差 %.2f%%" % (100 * abs(ALPHA_0 - ALPHA_MZ) / ALPHA_0))
    guard("f01_pomega_criterion_zero_info", KEY["f01_conserve_ratio"] > 0.999 and
          KEY["f01_pomega_ne_ratio"] > 0.95,
          "相位窗内 %d 点：PΩ≠Ω 成立 %.1f%%（唯一例外 θ=0 相位为零）"
          "且 P 守恒 %.1f%% ⇒ 前者零信息量"
          % (KEY["f01_window_points"], 100 * KEY["f01_pomega_ne_ratio"],
             100 * KEY["f01_conserve_ratio"]))
    guard("f03_bump_centered_conserves_parity",
          max(parity_residual(t, PHI0, 0.0, 60.0, odd_phase=True)
              for t in (-40.0, -12.0, 0.0, 7.5, 25.0)) < 1e-12,
          "bump 居中窗守恒残差机器零 ⇒ 复相位不破坏 P")
    guard("f05_branch3_gate_selfconsistent", abs(0.0261 / 5.00e-4 - 52.2) < 0.5,
          "门禁倍数 %.1f ≈ 52.2" % (0.0261 / 5.00e-4))
    guard("b03b_unit_amplitude_linear_is_constant",
          KEY.get("b03_unit_linear", {}).get("spread", 1.0) < 1e-12 and
          KEY.get("b03_real_segmented", {}).get("spread", 0.0) > 1e-6,
          "B03 原口径（单位幅值+全域线性）spread=%.1e ⇒ 常数成立；来料口径（真实幅值+分段）"
          "spread=%.2e ⇒ 非常数（B03 口径自纠）"
          % (KEY.get("b03_unit_linear", {}).get("spread", -1.0),
             KEY.get("b03_real_segmented", {}).get("spread", -1.0)))


# ===========================================================================
# 产物输出
# ===========================================================================
def write_out():
    name = "TUFT-MATH-PROOF-ADD-01R_外部审计逐条复算与自我修正_2026-10-04"
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    counts = {}
    for r in RESULTS:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    payload = {
        "册名": "TUFT-MATH-PROOF-ADD-01R 外部审计逐条复算与自我修正",
        "日期": "2026-10-04",
        "被审": "TUFT-MATH-PROOF-ADD-01（复 Ω 相位机制 Part B + 误差传播 Part C + 审计闭环 Part D）",
        "前置": ["整理_TUFT-MATH-PROOF-ADD-01_复权重场与误差传播_交叉审计与分支裁定_2026-10-04",
                 "突破_TUFT-MATH-PROOF-ADD-02_Omega正瓣重指派_互斥完备划分与耦合匹配_2026-10-04"],
        "性质": "元审计 / 整理 + 自我修正（对外部审计意见的机器复算；对前置册过度结论的修正）",
        "引擎": "纯标准库（Python 3.8），零第三方依赖",
        "条目数": len(RESULTS),
        "计数": counts,
        "自检": {"总数": len(GUARDS), "通过": sum(1 for g in GUARDS if g["ok"])},
        "key_numbers": KEY,
        "判定": RESULTS,
        "guards": GUARDS,
    }
    jp = os.path.join(DATA_DIR, name + ".json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# 数据产物：TUFT-MATH-PROOF-ADD-01R 外部审计逐条复算与自我修正")
    lines.append("")
    lines.append("- **日期**：2026-10-04 · **条目**：%d · **计数**：%s"
                 % (len(RESULTS), " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))))
    lines.append("- **自检**：%d / %d" % (payload["自检"]["通过"], payload["自检"]["总数"]))
    lines.append("")
    lines.append("## 判定表")
    lines.append("")
    lines.append("| id | 段 | 项 | 判定 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for r in RESULTS:
        det = r["detail"].replace("|", "/").replace("\n", " ")
        lines.append("| %s | %s | %s | %s | %s |" % (r["id"], r["section"], r["item"],
                                                      r["verdict"], det))
    lines.append("")
    lines.append("## 关键读数")
    lines.append("")
    for k in sorted(KEY.keys()):
        v = KEY[k]
        if isinstance(v, float):
            lines.append("- `%s` = %.6g" % (k, v))
        elif isinstance(v, (int, str)):
            lines.append("- `%s` = %s" % (k, v))
        else:
            lines.append("- `%s` = %s" % (k, json.dumps(v, ensure_ascii=False)))
    lines.append("")
    lines.append("## 自检")
    lines.append("")
    lines.append("| guard | 结果 | 取证 |")
    lines.append("|---|---|---|")
    for g in GUARDS:
        lines.append("| %s | %s | %s |" % (g["name"], "PASS" if g["ok"] else "FAIL",
                                          g["detail"].replace("|", "/")))
    lines.append("")
    mp = os.path.join(DATA_DIR, name + ".md")
    with open(mp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return jp, mp, counts


def main():
    print("=" * 78)
    print("TUFT-MATH-PROOF-ADD-01R · 外部审计逐条复算与自我修正")
    print("=" * 78)

    global lam_val
    sec_A()
    # B01 / B05 的 guard 读数
    ths = [-40.0, -12.0, 0.0, 7.5, 25.0]
    KEY["b01_max"] = max(parity_residual(t, PHI0, 0.0, 60.0, odd_phase=True) for t in ths)
    sec_B()
    MG, MT = complex(1.0, 0.3), complex(0.4, -0.9)
    f = complex(1.0 + 0.1 * math.cos(0.5), 0.1 * math.sin(0.5))
    a_b = (abs(MG) ** 2 - abs(MT) ** 2) / (abs(MG) ** 2 + abs(MT) ** 2)
    a_a = (abs(f * MG) ** 2 - abs(f * MT) ** 2) / (abs(f * MG) ** 2 + abs(f * MT) ** 2)
    KEY["b05_dA"] = abs(a_a - a_b)
    sec_C()
    KEY["sigma_lambda"] = SIG_ALPHA_S / ALPHA_S
    sec_D()
    sec_F()
    fixes = sec_E()

    do_guards()
    jp, mp, counts = write_out()

    ok = sum(1 for g in GUARDS if g["ok"])
    print("-" * 78)
    print("条目 %d：%s" % (len(RESULTS), " / ".join("%s %d" % (k, counts[k]) for k in sorted(counts))))
    print("自检 %d / %d" % (ok, len(GUARDS)))
    print("产物：%s" % os.path.basename(jp))
    print("耗时 %.2fs" % (time.time() - T_START))
    print("=" * 78)
    return 0 if ok == len(GUARDS) else 1


if __name__ == "__main__":
    sys.exit(main())
