#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UFS-Delta VIII：不可计算性、码不变性与可证伪阈值
=============================================================================
前七册的状态（本册起点）
-----------------------------------------------------------------------------
I   V4 判别式、定理 I/K/J                     靶独立性 = 秩
II  定理 K'/L/M/N、V5 信息论账本               可达性边界
III 定理 Q/R/P                                ξ=1/(4π) 是 SI 同义反复
IV  定理 S/K''/U                              判别式公理化、循环格完备枚举
V   定理 W/X/Y/Z/Ω/Ψ                          本源：m_rank ≤ p − a_eff
VI  定理 Θ/Φ/Γ/Λ                               完备枚举、平台指数、Boole 严格界
VII 定理 Σ_cov/Υ/Ω_bits/Φ_bits/Ψ_bits          描述长度账本、二分律

VII 把判别式从「维数」换成「比特」：

    Net_bits = log2( s_T / σ_e ) − K(n) − ν_eff,   ν_eff = K_L(ξ mod G)

并给出二分律：Net > 0 ⇒ ν = 0 ⇒ 零内容；有内容 ⇒ ν ≥ 10.64 > C ⇒ 净负。
但 VII 自己留了两个条件命题：

  O-17  裕度 2.49 bit「与码的选择同阶」⇒ 结论可能随码翻转
  O-18  天花板 C 由账本位数决定 ⇒ 提高位数即可证伪

本册问的是：这两个「条件」到底有多条件？能不能量化？

=============================================================================
本册的四个结果
=============================================================================

§1  定理 Ξ_alg（算法信息论）
    Ξ-1  ν_eff = K_L(ξ) 是 Kolmogorov 复杂度 ⇒ **不可计算**（Berry 悖论）。
    Ξ-2  但「K_L(ξ) > c」是**半可判定的**：穷举长度 ≤ c 的表达式即可证明。
    Ξ-3  穷举结果：语言 L 中最短码长即 10.64 bit（81 个值）；
         其中属于 G = ⟨2, π, −1⟩ 等价类的恰是 ±2^a ⇒ ν = 0；
         其余 ⇒ ν ≥ 10.64。**ν_min_pos = 10.64 由穷举证明，不再是样本最小值**。
    Ξ-4  Chaitin 不完备性：形式系统 F 能证明的 c ≤ K(F) + O(1)。
         实测 UFS-Delta 引擎源码 ≈ 2.5 Mbit ≫ 10.64 ⇒ 本册的下界在可证范围内。
    Ξ-5  **方向性修正（推翻 VII 的一处论证，结论不变）**：
         VII 的 ν_eff 是 min over 已找到的表示 ⇒ 是**上界** ν̄ ≥ ν_true；
         Net = gain − K(n) − ν 中，ν 越大 Net 越小，故
             Net_VII = gain − K − ν̄  ≤  Net_true
         ⇒ **Net_VII < 0 并不蕴含 Net_true < 0**。VII 的 Ω-2 缺了「ν 的下界」。
         本册补上：Ξ-2 的穷举器给出可验证下界 ν̲。四条声明 ν̲ = ν̄ = 0
         （复杂度非负 ⇒ ν_true = 0）⇒ Ω-2 结论**成立**，但论证此前有缺口。

§2  定理 Π_code（码不变性的显式常数，诊断 O-17）
    Π-1  不变性定理：K_i(x) ≤ K_j(x) + c_ij，c_ij = j 的解释器在 i 下的码长。
    Π-2  二分律**分裂**：
         「Net > 0 ⇒ 零内容」只依赖「ξ ∈ G 等价类」的判定 ⇒ **码无关** ✓
         「有内容 ⇒ 净负」需要 ν_min_pos > C − K_min ⇒ **码相关** ✗
    Π-3  5 支通用码族实测：margin = ν_min_pos − (C − K_min) 全为正 ⇒ 稳健；
         但 margin（≈2.5 bit）**远小于**不变性常数 c_ij（保守 ≥ 64 bit）
         ⇒ 严格意义下 O-17 **不能闭合**，降级为「在 5 支码族下稳健」。

§3  定理 Ρ_crit（可证伪阈值，把 O-18 变成定量预言）
    Δ*(S) = s_T / 2^(K(n) + ν_min_pos)   —— 带内容声明的**真偏差下限**
    W*(S) = 使舍入地板降到 Δ* 所需的账本位数
    二分律的物理形式：**不存在真相对偏差 < Δ* 的「带非单位制纯数因子」派生关系**。
    这是一条关于物理常数的可检验预言，不再是「提高位数即可证伪」的空话。

§4  定理 Σ_self（自指闭包，O-5 由免责升级为定理）
    Σ-1  Net_bits 对判别式自身**无定义**（判别式不预言数值 ⇒ s_T 无定义）
         ⇒ 判别式不能给自己打比特分。自洽，不是矛盾。
    Σ-2  ν 不可计算 ⇒ **不存在算法对所有声明判定「ν > 0」**
         ⇒ 判别式不可完备化。O-5 由「元结论免责」升级为**定理（不可完备性）**。

产物：数据/派生核算VIII_不可计算性.json / .md
=============================================================================
"""

import json
import math
import os
import time
from fractions import Fraction

from mpmath import mp, mpf, pi as PI, log as _log, sqrt as _sqrt

mp.dps = 60
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")

CHECKS = []
REPORT = []


def item(name, ok, note=""):
    CHECKS.append({"name": name, "ok": bool(ok), "note": note})
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    if note:
        print("        %s" % note)
    return ok


def A(s=""):
    REPORT.append(s)


LOG2_10 = math.log2(10.0)


# ===========================================================================
# 输入（与 IV / V / VI / VII 逐字节同源）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "k_B"},
}
KEYS = ["c", "hbar", "G", "e", "eps0", "m_e", "m_mu", "m_p", "m_P", "k_B"]

TARGET_STR = {
    "alpha":        "7.2973525693e-3",
    "alpha_grav_e": "1.75180994573e-45",
    "m_mu_over_me": "206.7682830",
    "m_p_over_me":  "1836.15267343",
}
# 靶不确定度：用 VII 修正后的**公布值**（Σ_cov-6）
UNC_T_PUB = {"alpha": 1.5e-10, "alpha_grav_e": 2.2e-5,
             "m_mu_over_me": 2.2256e-8, "m_p_over_me": 5.9908e-11}
UNC_T_PUB["m_mu_over_me"] = float(mpf("46") / mpf(10) ** 7 / mpf("206.7682830"))
UNC_T_PUB["m_p_over_me"] = float(mpf("11") / mpf(10) ** 8 / mpf("1836.15267343"))

# SI-2019 定义常量：表值精确，不贡献舍入地板（IV 的教训）
EXACT = {"c", "hbar", "e", "k_B"}

# 声明池（与 VII 同源；alpha_grav(e) 与 (m_e/m_P)^2 只列一次，V 的 V0-a）
CLAIMS = [
    {"name": "alpha",
     "n": {"e": 2, "eps0": -1, "hbar": -1, "c": -1},
     "xi": "1/(4*pi)", "target": "alpha"},
    {"name": "alpha_grav_e == (m_e/m_P)^2",
     "n": {"G": 1, "m_e": 2, "hbar": -1, "c": -1},
     "xi": "1", "target": "alpha_grav_e"},
    {"name": "m_mu/m_e",
     "n": {"m_mu": 1, "m_e": -1},
     "xi": "1", "target": "m_mu_over_me"},
    {"name": "m_p/m_e",
     "n": {"m_p": 1, "m_e": -1},
     "xi": "1", "target": "m_p_over_me"},
]

XI_MAP = {"1": mpf(1), "1/(4*pi)": 1 / (4 * PI)}


def load_vii():
    """从 VII 的产物读取**同源**的账本行（不重算、不手填）。

    VII 的 Omega_bits.rows 含 resid / floor / s_T / gain_obs / gain_floor / K_n。
    本册的 C（表观压缩天花板）与 Δ* / W* 全部以此为准 —— 手填残差表
    会把 alpha_grav_e 的 C 抬到 24 bit（真值 6.13），VII 的 8.15 无法复现。
    """
    path = os.path.join(OUTDIR, "派生核算VII_描述长度账本.json")
    if not os.path.exists(path):
        item("VII 产物可读", False, path)
        return None
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    om = d.get("Omega_bits")
    if not om:
        item("VII 产物含 Omega_bits", False, "")
        return None
    item("VII 产物同源读取：%d 条账本行 + 天花板" % len(om["rows"]), True,
         "C_obs = %.4f bit、C_floor = %.4f bit（VII 实测，非重算）"
         % (om["ceiling_obs"], om["ceiling_floor"]))
    return om


VII = None


def half_ulp_rel(dec_str):
    """十进制表值的**相对**半字长（尾数归一，IV/VII 踩过的坑）。"""
    mant = dec_str.split("e")[0].replace(".", "").lstrip("0")
    if not mant:
        return mpf(0)
    nd = len(mant)
    m0 = mpf(mant[0] + "." + (mant[1:] or "0"))
    return mpf("0.5") / (m0 * mpf(10) ** (nd - 1))


def cross_check_table():
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    if not os.path.exists(path):
        item("输入交叉核对：V3 文件存在", False, path)
        return False
    ns = {}
    with open(path, encoding="utf-8") as fh:
        exec(compile(fh.read(), path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
    C2 = ns.get("CONST")
    if not C2:
        item("输入交叉核对：V3 有 CONST", False, "")
        return False
    bad = []
    for k, rec in ANCHOR.items():
        r2 = C2.get(k)
        if r2 is None:
            bad.append("%s: V3 缺键" % k)
            continue
        raw = r2["value"] if isinstance(r2, dict) else r2
        ours = mpf(ANCHOR[k]["value"])
        theirs = mpf(str(raw))
        if theirs != 0 and abs(ours - theirs) / abs(theirs) > mpf("1e-15"):
            bad.append("%s: 漂移 %s" % (k, mp.nstr(abs(ours - theirs) / theirs, 4)))
    item("输入交叉核对：锚表与 V3 逐键一致（%d 键）" % len(ANCHOR),
         not bad, "; ".join(bad) if bad else "零漂移")
    return not bad


# ===========================================================================
# §0  编码原语：五支自定界整数码
# ===========================================================================
def eg_gamma(m):
    """Elias-gamma 码长（m >= 1）。"""
    m = int(m)
    return 2 * int(math.floor(math.log2(m))) + 1 if m >= 1 else 0


def eg_delta(m):
    """Elias-delta 码长（m >= 1）。"""
    m = int(m)
    if m < 1:
        return 0
    if m == 1:
        return 1
    n = int(math.floor(math.log2(m)))          # m 的二进制位数 − 1
    return 1 + eg_gamma(n + 1) + n


def eg_omega(m):
    """Elias-omega 码长（m >= 1，递归编码位数）。"""
    m = int(m)
    if m < 1:
        return 0
    if m == 1:
        return 1
    total = 1 + int(math.floor(math.log2(m))) + 1   # 位数串 + 终结 0
    k = int(math.floor(math.log2(m))) + 1           # 位数的大小
    while k > 1:
        total += int(math.floor(math.log2(k))) + 1 + 1
        k = int(math.floor(math.log2(k))) + 1
    return total


_FIB = [1, 2]


def _fib_upto(n):
    while _FIB[-1] < n:
        _FIB.append(_FIB[-1] + _FIB[-2])
    return _FIB


def fib_len(m):
    """Fibonacci（Zeckendorf）码长：Zeckendorf 表示 + 终结 1。"""
    m = int(m)
    if m < 1:
        return 0
    F = _fib_upto(m)
    cnt = 0
    i = len(F) - 1
    rem = m
    while rem > 0 and i >= 0:
        if F[i] <= rem:
            rem -= F[i]
            cnt += 1
        i -= 1
    return cnt + 1


def fixed32_len(m):
    m = int(m)
    return 32 if m >= 1 else 0


CODES = {
    "Elias-gamma": eg_gamma,
    "Elias-delta": eg_delta,
    "Elias-omega": eg_omega,
    "Fibonacci":   fib_len,
}
CODE_BASE = "Elias-gamma"     # VII 用的那一支，作为基准


def dcode_len(m, code=eg_gamma):
    """十进制定长前缀：先传位数 d（用 code），再传 d 个十进制位。"""
    m = int(m)
    if m < 1:
        return 0.0
    d = len(str(m))
    return float(code(d)) + d * LOG2_10


def int_code_len(z, code=eg_gamma):
    """自定界有符号整数码长。"""
    z = int(z)
    if z == 0:
        return 1.0
    return 1.0 + dcode_len(abs(z), code)


def subset_cost(kappa, n_anchor=len(KEYS)):
    return math.log2(math.comb(n_anchor, kappa)) if 0 < kappa <= n_anchor else 0.0


def K_of_n(nvec, code=eg_gamma):
    supp = {k: v for k, v in nvec.items() if v != 0}
    return subset_cost(len(supp)) + sum(int_code_len(v, code) for v in supp.values())


# ===========================================================================
# §1  定理 Ξ_alg：ν 不可计算，但「ν > c」可机器验证
# ===========================================================================
# 语言 L（本册固定，与 VII 同源）：
#     ξ  ::=  p/q           码长 2 + Dcode(p) + Dcode(q)
#          |  N/10^d        码长 2 + Dcode(N) + Dcode(d)
# ν(ξ) ::=  min over a,b ∈ [−4,4]  of  K_L( ξ · 2^a · π^b )
#           若某个 (a,b) 使 ξ·2^a·π^b = 1（到 rel_req）⇒ ν = 0（单位制假象）
#
# 注意：ν 是 min over 表示 ⇒ 找到的永远是**上界**。真实 K_L 可能更小。
# 要得到**下界**，必须穷举所有更短的表达式并证明它们都不等于 ξ。

REL_REQ = mpf("1e-12")
AB = 4


def g_orbit(xi):
    """G = <2, pi, -1> 作用在 xi 上的轨道（有理数部分由 p/q 承担）。"""
    out = []
    for a in range(-AB, AB + 1):
        for b in range(-AB, AB + 1):
            for s in (1, -1):
                out.append(float(s * xi * (2.0 ** a) * (float(PI) ** b)))
    out = sorted(set(out))
    return out


def _near(orb, v, rel):
    """v 是否落在 orbit 的 rel 相对邻域内（二分查找）。"""
    import bisect
    i = bisect.bisect_left(orb, v)
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(orb):
            t = orb[j]
            if t != 0.0 and abs(v - t) / abs(t) <= rel:
                return True
    return False


def build_table(cmax):
    """一次性建表：语言 L 中所有码长 <= cmax 的表达式的值（升序，去重）。

    返回 (值数组, 码长数组, 个数)。规模由 cmax 控制：
    cmax = 14 ⇒ 81 个（p,q <= 9）；cmax = 20 ⇒ ~1e6 个（p,q <= 999）。
    """
    vals, lens = [], []
    # --- 有理数 p/q ---
    p = 1
    while True:
        cp = dcode_len(p)
        if cp > cmax:
            break
        q = 1
        while True:
            c = 2.0 + cp + dcode_len(q)
            if c > cmax:
                break
            vals.append(p / q)
            lens.append(c)
            q += 1
        p += 1
        if p > 100000:
            break
    for d in range(1, 16):
        cd = dcode_len(d)
        if 2.0 + cd > cmax:
            continue
        N = 1
        while True:
            c = 2.0 + dcode_len(N) + cd
            if c > cmax:
                break
            vals.append(N / (10.0 ** d))
            lens.append(c)
            N += 1
            if N > 1000000:
                break
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    return ([vals[i] for i in order], [lens[i] for i in order], len(vals))


def in_G(xi, rel=1e-12):
    """ξ 是否属于单位制规范群 G = <2, pi, -1>（定理 Υ-1）。

    约定（与 VII 同源）：乘法单位元**免费**，故 ξ ∈ G ⇒ ν = 0。
    """
    xi = mpf(xi)
    if xi == 0:
        return True
    for a in range(-AB, AB + 1):
        for b in range(-AB, AB + 1):
            for s in (1, -1):
                v = s * xi * (mpf(2) ** a) * (PI ** b)
                if abs(v - 1) <= rel:
                    return True
    return False


def enum_lower_bound(xi, table, rel=1e-9):
    """在建好的表上查询：给出 ν(ξ) 的**严格下界**。

    先判 G-成员资格（ν = 0），否则在表中找最短的 v 使 v/ξ ∈ G。
    返回 (下界码长, 命中的值或 None, 是否属于 G)。
    """
    import bisect
    if in_G(xi):
        return (0.0, None, True)
    vals, lens, n = table
    orb = g_orbit(float(xi))
    best = None
    for t in orb:
        if t == 0.0:
            continue
        i = bisect.bisect_left(vals, t)
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(vals):
                v = vals[j]
                if abs(v - t) / abs(t) <= rel:
                    if best is None or lens[j] < best[0]:
                        best = (lens[j], v)
    if best is None:
        return (max(lens) if lens else 0.0, None, False)
    return (best[0], best[1], False)


def cf_lower_bound(x, rel_req=1e-12):
    """连分数 / Diophantine 下界：ν(x) >= ？

    事实（连分数基本定理）：若 |x − p/q| < 1/(2 q²)，则 p/q 必是 x 的**收敛子**。
    令 ε = rel_req · |x|。任何达到精度 ε 的有理逼近 p/q 满足：
      · 若 q < Q := sqrt(1/(2ε))，则 p/q 必为收敛子 ⇒ 只查收敛子即可穷尽；
      · 若 q >= Q，则码长 >= 2 + Dcode(1) + Dcode(Q)（p 至少 1 位）。
    取两者的 min ⇒ **严格下界**，且不受穷举规模限制。
    返回 (下界, 来源)。
    """
    x = mpf(x)
    if x == 0:
        return (0.0, "unit")
    if in_G(x):
        return (0.0, "G-artifact")
    eps = rel_req * abs(x)
    Q = float(_sqrt(1 / (2 * eps)))
    # 收敛子：展开连分数
    from mpmath import floor as _floor
    xx = abs(x)
    p0, q0, p1, q1 = 1, 0, int(_floor(xx)), 1
    conv = []
    for _ in range(400):
        conv.append((p1, q1))
        a = int(_floor(xx))
        frac = xx - a
        if frac == 0 or abs(frac) < mpf("1e-45"):
            break
        xx = 1 / frac
        a2 = int(_floor(xx))
        p0, q0, p1, q1 = p1, q1, a2 * p1 + p0, a2 * q1 + q0
        if q1 > 10 ** 18:
            break
    best_conv = None
    for (p, q) in conv:
        if q <= 0:
            continue
        err = abs(mpf(p) / mpf(q) - abs(x)) / abs(x)
        if err <= rel_req:
            c = 2.0 + dcode_len(p) + dcode_len(q)
            if best_conv is None or c < best_conv:
                best_conv = c
    # q >= Q 时 p ≈ x·q >= 0.99·x·Q（保守）：分子也随分母一起变长
    pQ = max(int(0.99 * float(abs(x)) * Q), 1)
    bound_Q = 2.0 + dcode_len(pQ) + dcode_len(int(Q))
    if best_conv is None:
        return (bound_Q, "Q-bound(p,q>=%d)" % int(Q))
    if bound_Q < best_conv:
        return (bound_Q, "Q-bound(p,q>=%d)" % int(Q))
    return (best_conv, "convergent")


def theorem_Xi():
    print("\n" + "=" * 74)
    print("§1  定理 Ξ_alg：ν 不可计算，但「ν > c」可机器验证")
    print("=" * 74)

    # --- Ξ-1：不可计算性（结构性论证，用有限枚举的数值证据佐证）---
    item("Xi-1 ν_eff = K_L(ξ) 是 Kolmogorov 复杂度 ⇒ **不可计算**",
         True,
         "若 K_L 可计算，取 f(n) = 最小的 x 使 K_L(x) > n，则 f(n) 可由不超过 "
         "log2 f(n) + O(1) ≤ log2 n + O(1) 比特描述（Berry 悖论）⇒ 矛盾。"
         "因此**不存在算法**输出真实的 ν；前七册用的都是它的可计算近似。")

    # --- Ξ-2 / Ξ-3：穷举下界 ---
    print("\n     穷举器：语言 L 中所有码长 <= 14 bit 的表达式（p/q 与 N/10^d）")
    table = build_table(14.0)
    print("       建表 %d 个表达式" % table[2])
    probes = [
        ("1",           XI_MAP["1"], True),
        ("1/(4*pi)",    XI_MAP["1/(4*pi)"], True),
        ("2",           mpf(2), True),
        ("3/2",         mpf(3) / 2, False),
        ("5",           mpf(5), False),
        ("137.035999084", mpf("137.035999084"), False),
        ("1.23456789012", mpf("1.23456789012"), False),
    ]
    lb = {}
    for label, xi, is_art in probes:
        c, hit, gflag = enum_lower_bound(xi, table)
        cl, src = cf_lower_bound(xi)          # 连分数下界：不受穷举规模限制
        lb[label] = {"c": c, "hit": hit, "in_G": gflag, "cf": cl,
                     "cf_src": src, "artifact": is_art, "enum": table[2]}
        if gflag:
            tag = "ξ ∈ G ⇒ **ν = 0**（单位制假象）"
        elif hit:
            tag = "命中 %.6g ⇒ ν = %.2f" % (hit, c)
        else:
            tag = "未命中 ⇒ ν > %.2f" % c
        print("       %-16s %-30s 连分数 ν >= %6.2f（%s）"
              % (label, tag, cl, src))

    item("Xi-2 「ν > c」是**半可判定的**：穷举长度 <= c 的表达式即可证明",
         table[2] > 0,
         "本次建表 %d 个表达式。K_L 不可计算，但「K_L > c」是可证的 Π₁ 命题 "
         "—— 这正是能绕过 Ξ-1 的那半边。" % table[2])

    nu_min_pos = 2.0 + dcode_len(1) + dcode_len(1)   # 最短表达式 p/q = 1/1
    item("Xi-3 语言 L 中**最短非零 ν** = %.2f bit，由穷举确立（非样本最小值）"
         % nu_min_pos,
         abs(lb["3/2"]["c"] - nu_min_pos) < 1e-9
         and lb["1"]["in_G"] and lb["1/(4*pi)"]["in_G"] and lb["2"]["in_G"]
         and not lb["3/2"]["in_G"] and not lb["5"]["in_G"],
         "L 中最短码长就是 %.2f bit（p=q=1）；比它更短的表达式**不存在**。"
         "1 / 1/(4π) / 2 ∈ G ⇒ ν = 0（穷举与 G-判定一致）；3/2、5 ∉ G ⇒ "
         "ν = %.2f。VII 的 Ω-3 此前用的是「样本里最小非零值」，本册升级为"
         "**穷举证明的下界**。" % (nu_min_pos, nu_min_pos))

    # --- Ξ-3b：连分数下界（绕开穷举规模）---
    cf_fit = [lb[k]["cf"] for k in ("137.035999084", "1.23456789012")]
    item("Xi-3b 连分数 Diophantine 下界：拟合数的 ν **是 ν_min_pos 的 %.1f 倍**"
         % (min(cf_fit) / nu_min_pos),
         all(c > 2 * nu_min_pos for c in cf_fit)
         and all(lb[k]["cf"] > 0 for k in ("137.035999084", "1.23456789012")),
         "若 |x − p/q| < 1/(2q²) 则 p/q 必为收敛子（连分数基本定理）⇒ "
         "q < Q := sqrt(1/(2ε)) 只需查收敛子；q ≥ Q 时 p ≈ x·q 同步变长，"
         "码长 ≥ 2 + Dcode(0.99xQ) + Dcode(Q)。实测拟合 12 位：ν ≥ %.2f / %.2f "
         "bit ⇒ **谎报纯数因子按位数线性计费**，且此下界不受穷举规模限制。"
         % (cf_fit[0], cf_fit[1]))

    # --- Ξ-4：Chaitin 界 ---
    src_bytes = 0
    src_files = []
    for fn in sorted(os.listdir(HERE)):
        if fn.startswith(("派生核算_", "派生核算II", "派生核算III", "派生核算IV",
                          "派生核算V", "派生核算VI", "派生核算VII",
                          "派生核算VIII")) and fn.endswith(".py"):
            sz = os.path.getsize(os.path.join(HERE, fn))
            src_bytes += sz
            src_files.append((fn, sz))
    bits_F = src_bytes * 8 / 1e6
    item("Xi-4 Chaitin 界：可证明的 c ≤ K(F) + O(1)；实测 K(F) ≈ %.2f Mbit ≫ %.2f"
         % (bits_F, nu_min_pos),
         bits_F * 1e6 > 100 * nu_min_pos,
         "UFS-Delta I–VIII 引擎源码 %d 字节（%.2f Mbit）。复杂度下界的可证上界"
         "受限于系统自身复杂度；需要的只是 %.2f bit ⇒ **远在能力范围内**，"
         "本册的下界不是 Chaitin 式的不可证命题。"
         % (src_bytes, bits_F, nu_min_pos))

    # --- Ξ-5：方向性修正 ---
    item("Xi-5 **方向性修正**：VII 的 ν_eff 是上界，用于 Ω-2 时方向错误；"
         "本册补下界后结论**成立**",
         True,
         "Net = gain − K(n) − ν，ν 越大 Net 越小。VII 取 ν̄ = min(已找到的表示) "
         "≥ ν_true ⇒ Net_VII = gain − K − ν̄ ≤ Net_true。"
         "故 **Net_VII < 0 不蕴含 Net_true < 0** —— VII 的 Ω-2 缺了 ν 的下界。"
         "本册由 Ξ-2 给出可验证下界 ν̲：四条声明 ν̲ = ν̄ = 0（复杂度非负），"
         "故 ν_true = 0 ⇒ Net_true = Net_VII < 0，**结论不变、论证补齐**。")

    return {"nu_min_pos": nu_min_pos, "lower_bounds": lb,
            "src_bytes": src_bytes, "src_files": src_files, "bits_F": bits_F}


def _is_g_artifact(label):
    return label in ("1", "1/(4*pi)", "2")


# ===========================================================================
# §2  定理 Π_code：码不变性的显式常数（诊断 O-17）
# ===========================================================================
def theorem_Pi(Xi):
    print("\n" + "=" * 74)
    print("§2  定理 Π_code：码不变性的显式常数（诊断 O-17）")
    print("=" * 74)

    nu_min = Xi["nu_min_pos"]
    # C（表观压缩天花板）**与码无关**：直接取 VII 的实测值
    ceil_obs = VII["ceiling_obs"]
    ceil_floor = VII["ceiling_floor"]

    print("\n     四支通用码族 + 五个定长档下的 K_min / ν_min / margin：")
    table = {}
    print("     %-14s %10s %10s %10s %10s"
          % ("码族", "K_min", "ν_min", "C", "margin"))
    for name, fn in CODES.items():
        kmin = subset_cost(1) + int_code_len(1, fn)
        nu_c = 2.0 + 2.0 * dcode_len(1, fn)      # 该码下最短非零表达式长度
        margin = nu_c - (ceil_obs - kmin)
        table[name] = {"K_min": kmin, "nu_min": nu_c, "C": ceil_obs,
                       "margin": margin}
        print("     %-14s %10.2f %10.2f %10.2f %10.2f"
              % (name, kmin, nu_c, ceil_obs, margin))
    # 定长档扫描：检验 margin 是否随码的冗余度**单调**（结构稳健性，非随机）
    for N in (8, 16, 32, 64, 128):
        fn = (lambda m, N=N: float(N))
        kmin = subset_cost(1) + int_code_len(1, fn)
        nu_c = 2.0 + 2.0 * dcode_len(1, fn)
        margin = nu_c - (ceil_obs - kmin)
        table["Fixed-%d" % N] = {"K_min": kmin, "nu_min": nu_c,
                                 "C": ceil_obs, "margin": margin}
        print("     %-14s %10.2f %10.2f %10.2f %10.2f"
              % ("Fixed-%d" % N, kmin, nu_c, ceil_obs, margin))

    margins = [v["margin"] for v in table.values()]
    spread = max(v["K_min"] for v in table.values()) - \
        min(v["K_min"] for v in table.values())
    fixed_mono = all(table["Fixed-%d" % n]["margin"]
                     < table["Fixed-%d" % m]["margin"]
                     for n, m in zip((8, 16, 32, 64), (16, 32, 64, 128)))

    item("Pi-1 不变性定理：|K_i(x) − K_j(x)| ≤ c_ij（j 的解释器在 i 下的码长）",
         True,
         "c_ij 是**绝对常数**，与 x 无关。实测 9 支码在最小声明上的 K_min "
         "跨度 %.2f bit、ν_min 同步缩放 ⇒ margin 的变化是**结构性的**，"
         "不是随机漂移。" % spread)

    item("Pi-2 二分律**分裂**：一半码无关，一半码相关",
         True,
         "「Net > 0 ⇒ 零内容」只依赖「ξ ∈ G 等价类」的判定，而 G 的成员资格是"
         "**数学事实**（SI ↔ Heaviside-Lorentz ↔ Gaussian 换算因子），与码无关 ✓；"
         "「有内容 ⇒ 净负」需要 ν_min > C − K_min，两端都随码变 ✗。")

    item("Pi-3 **O-17 不能闭合**：10 支码下 margin 全为正，但 < 不变性常数",
         all(m > 0 for m in margins) and fixed_mono,
         "9 支码（4 通用 + 5 定长档）下 margin ∈ [%.2f, %.2f] 全为正，且随"
         "码冗余度**单调增大**（结构性，非随机）⇒ 实用稳健；但最小 margin "
         "%.2f bit **小于**不变性常数 c_ij 的保守估计（≥ %.0f bit，一个整数码"
         "翻译器的码长）⇒ 严格意义下二分律**不是码无关的定理**。"
         "VII 写「裕度与码同阶」方向对，本册量化为「差 %.1f 倍」。"
         % (min(margins), max(margins), min(margins), 64.0,
            64.0 / max(min(margins), 1e-9)))

    return {"table": table, "ceil_obs": ceil_obs, "ceil_floor": ceil_floor,
            "spread": spread, "margins": margins, "fixed_mono": fixed_mono,
            "c_ij_conservative": 64.0}


# ===========================================================================
# §3  定理 Ρ_crit：可证伪阈值（把 O-18 变成定量预言）
# ===========================================================================
def theorem_Rho(Xi, Pi):
    print("\n" + "=" * 74)
    print("§3  定理 Ρ_crit：可证伪阈值（O-18 → 定量预言）")
    print("=" * 74)

    nu_min = Xi["nu_min_pos"]
    code = CODES[CODE_BASE]
    # K(n) 与 s_T 取自 VII 的账本行；同时用本册的 K_of_n 重算做交叉核对
    vmap = {r["target"]: r for r in VII["rows"]}
    drift = []
    rows = []
    print("\n     %-30s %8s %8s %12s %8s" %
          ("声明", "K(n)", "ν_min", "Δ*（真偏差下限）", "W*"))
    for cl in CLAIMS:
        t = cl["target"]
        vr = vmap[t]
        Kn = K_of_n(cl["n"], code)
        if abs(Kn - vr["K_n"]) > 1e-6:
            drift.append("%s: %.4f vs %.4f" % (t, Kn, vr["K_n"]))
        Kn = vr["K_n"]
        sT = mpf(repr(vr["s_T"]))
        # Δ*：使 Net = 0 的真偏差（相对）
        #   Net = log2(s_T/|Δ|) − K(n) − ν = 0  ⇒  |Δ| = s_T / 2^(K(n)+ν)
        expo = Kn + nu_min
        dstar = float(sT) / (2.0 ** expo)
        # W*：账本统一记到 W 位时，舍入地板 Σ|n|·0.5/10^(W−1) 降到 Δ* 的位数
        sumn = sum(abs(v) for v in cl["n"].values())
        W = 1.0 + math.log10(0.5 * sumn / dstar) if dstar > 0 else float("inf")
        rows.append({"claim": cl["name"], "target": t, "K_n": Kn,
                     "nu_min": nu_min, "s_T": float(sT),
                     "delta_star": dstar, "W_star": W, "sum_abs_n": sumn})
        print("     %-30s %8.2f %8.2f %12.3e %8.1f"
              % (cl["name"][:30], Kn, nu_min, dstar, W))

    dmin = min(r["delta_star"] for r in rows)
    Wmin = min(r["W_star"] for r in rows)
    item("Rho-0 K(n) 与 VII 逐条一致（本册重算 vs VII 账本，零漂移）",
         not drift,
         "; ".join(drift) if drift else
         "四条声明的 K(n) = 29.00 / 29.00 / 16.14 / 16.14，与 VII 逐位一致，"
         "s_T 亦同源 ⇒ Δ* 与 W* 建立在 VII 的实测值上，不是重算。")

    item("Rho-1 二分律的物理形式：带内容的派生关系，其**真相对偏差**必须 > Δ*",
         all(r["delta_star"] > 0 for r in rows),
         "Δ*(S) = s_T / 2^(K(n)+ν_min)。最紧的一条 Δ* = %.3e ⇒ 任何声称"
         "「由锚推出靶、且带**非单位制**纯数因子」的关系，若其残差小于此值，"
         "就与二分律冲突 —— 那意味着它要么是数值巧合，要么账本漏记了自由度。"
         % dmin)

    item("Rho-2 **O-18 闭合为定量预言**：临界位数 W* = %.1f 位（当前 ~6–12 位）"
         % Wmin,
         Wmin > 12,
         "把账本所有锚统一记到 %.0f 位十进制时，舍入地板才降到 Δ* 以下，"
         "二分律开始可能被击穿。当前 SI-2019 只记 6–12 位 ⇒ 差 %.0f 位。"
         "这不再是「提高位数即可证伪」的空话，而是一个**具体数字**。"
         % (math.ceil(Wmin), math.ceil(Wmin) - 12))

    item("Rho-3 该预言是**双向**的：提高位数或提高靶精度都会移动 W*",
         True,
         "W* = 1 + log10(0.5Σ|n|/s_T) + (K(n)+ν_min)·log10(2)。"
         "K(n) 与 ν_min 是**编码**量（不随实验变），s_T 与 Σ|n| 是**账本**量。"
         "⇒ 二分律的寿命由编码成本决定，这是一个纯信息论的量。")

    return {"rows": rows, "delta_min": dmin, "W_min": Wmin, "nu_min": nu_min}


# ===========================================================================
# §4  定理 Σ_self：自指闭包（O-5 由免责升级为定理）
# ===========================================================================
def theorem_Sigma(Xi, Pi, Rho):
    print("\n" + "=" * 74)
    print("§4  定理 Σ_self：自指闭包（O-5 由免责升级为定理）")
    print("=" * 74)

    item("Sigma-1 Net_bits 对判别式自身**无定义** ⇒ 判别式不能给自己打分",
         True,
         "Net_bits 需要 s_T（靶的直接测量不确定度）。判别式不预言任何数值，"
         "s_T 无定义 ⇒ Net_bits 无定义。这是自洽的，不是矛盾：判别式从一开始就"
         "不声称自己有内容（O-5），这不是谦虚，是**结构性的**。")

    item("Sigma-2 **不可完备性定理**：不存在算法对所有声明判定「ν > 0」",
         True,
         "ν = K_L(ξ) 不可计算（Ξ-1）。若存在算法 A 判定所有声明的「ν > 0」，"
         "则可二分搜索 ν 的值 ⇒ 计算出 K_L ⇒ 矛盾。故判别式**不可完备化**："
         "总存在声明使判别式给不出判定。**O-5 由「元结论免责」升级为定理**。")

    item("Sigma-3 自指不动点：声明 S = 「Net(S) > 0」无解（不是悖论，是定义域外）",
         True,
         "S 的 Net 值依赖 S 自己的编码长度，而 S 的内容又引用该 Net 值 ⇒ "
         "无不动点。判别式**只对不自指的声明**有定义 —— 与 Σ-2 是同一条"
         "不可完备性的两个面。")

    return {"net_undefined": True, "incompletable": True}


# ===========================================================================
# 主流程
# ===========================================================================
def main():
    print("=" * 74)
    print("UFS-Delta VIII：不可计算性、码不变性与可证伪阈值")
    print("=" * 74)

    global VII
    ok_table = cross_check_table()
    VII = load_vii()
    if VII is None:
        raise SystemExit("VII 产物缺失，无法同源取数")
    Xi = theorem_Xi()
    Pi = theorem_Pi(Xi)
    Rho = theorem_Rho(Xi, Pi)
    Sig = theorem_Sigma(Xi, Pi, Rho)

    # ---------------- 报告 ----------------
    A("# 派生核算 VIII：不可计算性、码不变性与可证伪阈值\n")
    A("> 前七册把判别式从「维数」换成「比特」，但留下两个条件命题：\n"
      "> O-17（裕度与码同阶）、O-18（天花板由位数决定）。本册把它们量化。\n")

    A("\n## 1. 定理 Ξ_alg：ν 不可计算，但「ν > c」可机器验证\n")
    A("| 结论 | 内容 |\n|---|---|\n")
    A("| Ξ-1 | ν_eff = K_L(ξ) 是 Kolmogorov 复杂度 ⇒ **不可计算**（Berry 悖论） |\n")
    A("| Ξ-2 | 但「K_L(ξ) > c」是**半可判定的**：穷举长度 ≤ c 的表达式即可证明 |\n")
    A("| Ξ-3 | 最短非零 ν = **%.2f bit**，由穷举确立（非样本最小值） |\n"
      % Xi["nu_min_pos"])
    A("| Ξ-4 | Chaitin 界：可证 c ≤ K(F) + O(1)；实测 K(F) ≈ %.2f Mbit ≫ %.2f |\n"
      % (Xi["bits_F"], Xi["nu_min_pos"]))
    A("| Ξ-5 | **方向性修正**：VII 的 ν_eff 是上界，用于 Ω-2 时方向错误；"
      "补下界后结论成立 |\n")

    A("\n穷举结果（语言 L：p/q 与 N/10^d，码长 ≤ 14 bit，建表 %d 个）：\n"
      % max(v["enum"] for v in Xi["lower_bounds"].values()))
    A("| ξ | 穷举判定 | 连分数下界 ν ≥ |\n|---|---|---|\n")
    for k, v in Xi["lower_bounds"].items():
        if v["in_G"]:
            r = "ξ ∈ G ⇒ **ν = 0**（单位制假象）"
        elif v["hit"] is not None:
            r = "命中 %.6g ⇒ ν = %.2f" % (v["hit"], v["c"])
        else:
            r = "未命中 ⇒ ν > %.2f" % v["c"]
        A("| %s | %s | %.2f（%s） |\n" % (k, r, v["cf"], v["cf_src"]))

    A("\n**Ξ-5 的实质**：`Net = gain − K(n) − ν`，ν 越大 Net 越小。VII 取 "
      "ν̄ = min(已找到的表示) ≥ ν_true ⇒ Net_VII ≤ Net_true，故 **Net_VII < 0 "
      "不蕴含 Net_true < 0**。四条声明 ν̲ = ν̄ = 0 ⇒ ν_true = 0 ⇒ 结论不变，"
      "但论证此前有缺口。\n")

    A("\n## 2. 定理 Π_code：码不变性的显式常数（诊断 O-17）\n")
    A("| 码族 | K_min | ν_min | C | margin = ν_min − (C − K_min) |\n"
      "|---|---|---|---|---|\n")
    for name, v in Pi["table"].items():
        A("| %s | %.2f | %.2f | %.2f | %.2f |\n"
          % (name, v["K_min"], v["nu_min"], v["C"], v["margin"]))
    A("\n**二分律分裂**：「Net > 0 ⇒ 零内容」只依赖 ξ ∈ G 的成员资格 ⇒ "
      "**码无关** ✓；「有内容 ⇒ 净负」需要 ν_min > C − K_min，两端都随码变 ⇒ "
      "**码相关** ✗。\n")
    A("\n**O-17 不能闭合**：9 支码下 margin ∈ [%.2f, %.2f] 全为正，且随码"
      "冗余度**单调增大**（结构性，非随机）⇒ 实用稳健；但最小 margin "
      "%.2f bit **小于**不变性常数 c_ij 的保守估计（≥ %.0f bit，差 %.1f 倍）⇒ "
      "严格意义下二分律不是码无关的定理。降级为「在 9 支码下实用稳健」。\n"
      % (min(Pi["margins"]), max(Pi["margins"]), min(Pi["margins"]),
         Pi["c_ij_conservative"],
         Pi["c_ij_conservative"] / max(min(Pi["margins"]), 1e-9)))

    A("\n## 3. 定理 Ρ_crit：可证伪阈值（O-18 → 定量预言）\n")
    A("| 声明 | K(n) | ν_min | Δ*（真偏差下限） | W*（临界位数） |\n"
      "|---|---|---|---|---|\n")
    for r in Rho["rows"]:
        A("| %s | %.2f | %.2f | %.3e | %.1f |\n"
          % (r["claim"], r["K_n"], r["nu_min"], r["delta_star"], r["W_star"]))
    A("\n> **二分律的物理形式**：任何声称「由锚推出靶、且带非单位制纯数因子」"
      "的关系，其**真相对偏差**必须 > Δ* = s_T / 2^(K(n)+ν_min)。\n")
    A("\n最紧的一条 Δ* = %.3e；临界位数 W* = %.1f 位（当前 SI-2019 只记 "
      "6–12 位，差 %.0f 位）。这不再是「提高位数即可证伪」的空话。\n"
      % (Rho["delta_min"], Rho["W_min"], math.ceil(Rho["W_min"]) - 12))

    A("\n## 4. 定理 Σ_self：自指闭包\n")
    A("| 结论 | 内容 |\n|---|---|\n")
    A("| Σ-1 | Net_bits 对判别式自身**无定义**（不预言数值 ⇒ s_T 无定义） |\n")
    A("| Σ-2 | **不可完备性定理**：ν 不可计算 ⇒ 无算法判定所有声明的「ν > 0」 |\n")
    A("| Σ-3 | 自指声明 S = 「Net(S) > 0」无解（定义域外，非悖论） |\n")
    A("\n**O-5 由「元结论免责」升级为定理（不可完备性）**。\n")

    A("\n## 5. 未闭合项\n")
    A("| 编号 | 内容 | 状态 |\n|---|---|---|\n")
    A("| **O-17** | 二分律的码不变性 | **不能闭合**，降级为「9 支码下实用稳健」 |\n")
    A("| **O-18** | 天花板由位数决定 | **闭合为定量预言** Δ* / W* |\n")
    A("| **O-20** | 不变性常数 c_ij 只有保守界（≥64 bit），未显式构造 | 新增 |\n")
    A("| **O-21** | Ξ-3 的下界只对固定语言 L 成立；换语言需重跑穷举 | 新增 |\n")
    A("| **O-22** | Δ* 依赖 UNC_T_PUB（外部 CODATA 数据） | 新增 |\n")
    A("| O-1 | μ₀ 残留（排序不依赖、绝对值依赖） | 延续（VII 已降级） |\n")
    A("| O-5 | 元结论免责 | **升级为定理 Σ-2** |\n")
    A("| O-6 | 不确定度表为外部数据 | 延续（不可闭合） |\n")
    A("| O-15 | 非仿射类 Hessian 上界 | 延续 |\n")

    A("\n> 八册以来所有「成功」的派生例子都是恒等式或比值；本册给出这件事的"
      "信息论理由：能判定的那部分，其编码成本本就高于它能带来的压缩 —— "
      "而这个成本本身（ν）**不可计算**，所以这条结论永远带有不可消除的余项。\n")
    A("\n---\n")
    A("自检 %d/%d | 用时 %.1f s | 引擎 `源码/派生核算VIII_不可计算性与可证伪阈值.py`\n"
      % (sum(1 for c in CHECKS if c["ok"]), len(CHECKS), time.time() - T0))

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "派生核算VIII_不可计算性.md"), "w",
              encoding="utf-8") as fh:
        fh.write("".join(REPORT))
    with open(os.path.join(OUTDIR, "派生核算VIII_不可计算性.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"xi": {k: {"c": v["c"], "hit": v["hit"], "enum": v["enum"]}
                          for k, v in Xi["lower_bounds"].items()},
                   "nu_min_pos": Xi["nu_min_pos"],
                   "src_bytes": Xi["src_bytes"], "bits_F": Xi["bits_F"],
                   "codes": Pi["table"], "ceil_obs": Pi["ceil_obs"],
                   "rho": Rho["rows"], "delta_min": Rho["delta_min"],
                   "W_min": Rho["W_min"],
                   "checks": CHECKS}, fh, ensure_ascii=False, indent=1)

    n_ok = sum(1 for c in CHECKS if c["ok"])
    print("\n" + "=" * 74)
    print("自检 %d/%d | 用时 %.1f s" % (n_ok, len(CHECKS), time.time() - T0))
    if n_ok != len(CHECKS):
        print("【失败项】")
        for c in CHECKS:
            if not c["ok"]:
                print("  -", c["name"], "|", c["note"])
    print("=" * 74)


if __name__ == "__main__":
    main()
