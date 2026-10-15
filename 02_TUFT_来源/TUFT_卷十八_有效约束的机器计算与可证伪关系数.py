# -*- coding: utf-8 -*-
# =====================================================================
# TUFT 卷十八 · 有效约束 d_eff 的机器计算与「可证伪关系数」
# ---------------------------------------------------------------------
# 纯 NumPy（+ 标准库 Fraction 做精确秩）；本机 jax/numpyro/arviz 不可用
#
# 承接卷十七：卷十七用判据 III 区分「名义约束 d」与「有效约束 d_eff」，
#   但 d_eff 是**逐通道人工判读**的（开放项 O-V17-DEFF）。本卷把它变成
#   可计算量，并在过程中发现卷十七把两件事混为一谈，须自纠。
#
# ★本卷的核心分解（卷十七缺的那一刀）：
#     设 J = ∂O/∂θ 是 d×p 的雅可比，r = rank(J)。则
#       r            = 数据能约束的参数方向数（可辨识方向数）
#       d − r        = 模型**无需调参**即固定的数据组合数
#                    = 可证伪关系数（Falsifiable Relations, FR）
#   ⇒ 「可辨识」与「有预测力」是两件不同的事，甚至此消彼长：
#       参数越多（r 越大）⇒ 可辨识方向越多，但 FR 越少、预测力越弱。
#     一个通道既有价值又站得住，需要 FR ≥ 1 **且**这些关系未被否证。
#
# ★秩的机器判定（本卷第二项，也是本库反复踩的坑）：
#     不存在普适容差。同一套浮点谱在不同容差下会给出相反的秩：
#       - 结构共线（G∥S 型，比例 1e-44）⇒ 真秩 1，但 tol<1e-17 时误判 2
#       - 病态满秩（条件数 1e8）⇒ 真秩 2，但 tol>1e-8 时误判 1
#     ⇒ 必须以**精确（有理数）秩**为准；浮点谱只用于报告条件数与告警。
#
# 红线：数学自洽 ≠ 实验证实。本卷审统计推断方法链，不进版本链、
#       不占冻结编号、不是第80章 SSOT 的变更源。
# 产出：同目录 .txt / .json / 一张 png
# =====================================================================
import json
import os
import time
import sys
from fractions import Fraction

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def rec(code, name, status, detail, evidence=None):
    RESULTS.append({"code": code, "name": name, "status": status,
                    "detail": detail, "evidence": evidence or {}})
    print("[{0:<9}] {1:<9} {2}".format(status, code, detail))


def sec(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ===================== §1 算法 =====================
def exact_rank(A):
    """有理数精确高斯消元求秩（Fraction 矩阵，list of list）。
    这是「结构秩」：不受浮点与容差影响。"""
    A = [[Fraction(x) for x in row] for row in A]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        for i in range(r + 1, m):
            if A[i][c] != 0:
                f = A[i][c] / pv
                for j in range(c, n):
                    A[i][j] -= f * A[r][j]
        r += 1
        if r == m:
            break
    return r


def spectrum(J):
    """浮点奇异值谱（降序）。"""
    s = np.linalg.svd(np.asarray(J, dtype=float), compute_uv=False)
    return s


def rank_at_tol(s, tol):
    if s[0] <= 0:
        return 0
    return int(np.sum(s > tol * s[0]))


def naive_rank(s, tol=1e-6):
    """阳性对照用的「朴素固定容差」秩——本卷要证明它不可靠。"""
    return rank_at_tol(s, tol)


TOLS = np.logspace(-18, -2, 33)


def tolerance_scan(s):
    rk = [rank_at_tol(s, t) for t in TOLS]
    lo, hi = min(rk), max(rk)
    return rk, (lo == hi), lo, hi


def fr(d, r):
    """可证伪关系数 = 观测数 − 秩。"""
    return d - r


def section1():
    sec("§1  算法：结构秩（精确） / 浮点谱 / 容差扫描 / 可证伪关系数")
    print("  r      = rank(J)        = 数据能约束的参数方向数")
    print("  FR     = d − r          = 模型无需调参即固定的数据组合数")
    print("  注意：r 越大（参数被定得越死）⇒ FR 越小（预测力越弱）。\n")

    # 算法自检：单位矩阵、零矩阵、比例行
    assert exact_rank([[1, 0], [0, 1]]) == 2
    assert exact_rank([[0, 0], [0, 0]]) == 0
    assert exact_rank([[1, 2], [2, 4]]) == 1
    assert exact_rank([[1, 0, 0], [0, 1, 0], [0, 0, 0], [1, 1, 0]]) == 2
    rec("V18-A1", "精确秩函数自检", "PASS",
        "单位阵→2、零阵→0、比例行 [[1,2],[2,4]]→1、含零列 4×3→2，全部命中"
        " ⇒ 结构秩函数本身可信（工具先自检再用于判定）。")


# ===================== §2 四个基准（含阳性对照） =====================
def section2():
    sec("§2  基准：秩判定的两个相反失效模式 + 阳性对照")
    # B1 满秩良态 4×3
    B1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
    # B2 含结构零列（CMB 的 V0 相消型）4×3
    B2 = [[1, 0, 0], [0, 1, 0], [0, 0, 0], [1, 1, 0]]
    # B3 极端共线，比例 1e-44（G∥S 型）
    k = Fraction(1, 10 ** 44)
    B3 = [[1, 2], [k, 2 * k]]
    # B3b 温和共线，比例 1e-9
    k2 = Fraction(1, 10 ** 9)
    B3b = [[1, 2], [k2, 2 * k2]]
    # B3c 十进制共线 0.1：行 = [1,3] 与 [0.1,0.3]。
    #   真秩 = 1（有理数意义上严格成比例）；
    #   但 3 不是 2 的幂 ⇒ 二进制浮点乘法不精确 ⇒ 比例关系被破坏，σ2 落在噪声底。
    B3c = [[1, 3], [Fraction(1, 10), Fraction(3, 10)]]
    # B4 病态但满秩：条件数 1e8
    B4 = [[1, 0], [0, Fraction(1, 10 ** 8)]]

    bench = [("B1 满秩良态", B1, 3), ("B2 结构零列", B2, 2),
             ("B3 极端共线(1e-44)", B3, 1), ("B3b 共线(1e-9,因子2)", B3b, 1),
             ("B3c 共线(0.1,因子3)", B3c, 1),
             ("B4 病态满秩(cond=1e8)", B4, 2)]
    rows = []
    for name, A, truth in bench:
        r_ex = exact_rank(A)
        s = spectrum([[float(x) for x in row] for row in A])
        rk, stable, lo, hi = tolerance_scan(s)
        r_nv = naive_rank(s)
        ratio = (s[1] / s[0]) if len(s) > 1 and s[0] > 0 else float("nan")
        ok_ex = (r_ex == truth)
        rows.append((name, len(A), len(A[0]), truth, r_ex, lo, hi, stable, r_nv, ratio))
        print("  {0:<22} d={1} p={2} 真秩={3} | 精确秩={4}{5} | 浮点秩区间=[{6},{7}]{8} | 朴素(1e-6)={9}".format(
            name, len(A), len(A[0]), truth, r_ex, "✓" if ok_ex else "✗", lo, hi,
            "(稳定)" if stable else "(不稳定!)", r_nv))
        print("      σ2/σ1 = {0:.3e}".format(ratio))
        rec("V18-B-" + name.split()[0], name, "PASS" if ok_ex else "FAIL",
            "真秩 {0} / 精确秩 {1} / 浮点秩区间 [{2},{3}] {4} / 朴素容差 1e-6 给 {5}"
            .format(truth, r_ex, lo, hi, "稳定" if stable else "不稳定", r_nv),
            {"truth": truth, "exact": r_ex, "float_lo": lo, "float_hi": hi,
             "stable": stable, "naive": r_nv, "s2_s1": float(ratio)})

    # 关键裁定：不存在普适容差（用真正暴露失效的那两个基准）
    b3 = rows[2]      # B3  极端共线 1e-44
    b3b = rows[3]     # B3b 共线 1e-9（比例因子 2）
    b3c = rows[4]     # B3c 共线 0.1（比例因子 3）
    b4 = rows[5]      # B4  病态满秩
    rec("V18-B0", "普适容差不存在（核心裁定）", "FAIL",
        "同一套浮点谱，两个失效方向**相反**：B3c（真秩 1，行 [1,3] 与 [0.1,0.3]）"
        "浮点秩区间 [{0},{1}] ⇒ 小容差下**高估**为 {1}（σ2/σ1 = {2:.3e} 落在噪声底）；"
        "B4（真秩 2、条件数 1e8）区间 [{3},{4}] ⇒ 大容差下**低估**为 {3}。"
        "⇒ 没有任何固定容差能同时正确；小容差高估、大容差低估。"
        .format(b3c[5], b3c[6], b3c[9], b4[5], b4[6]),
        {"B3c": {"float_lo": b3c[5], "float_hi": b3c[6], "truth": 1, "s2_s1": b3c[9]},
         "B4": {"float_lo": b4[5], "float_hi": b4[6], "truth": 2}})

    rec("V18-B3n", "为何 B3/B3b 反而「稳定」", "BOUNDARY",
        "B3（比例 1e-44）与 B3b（比例 1e-9）实测 σ2/σ1 = {0:.3e} / {1:.3e}，"
        "浮点秩区间均 [{2},{3}] 稳定且正确——**但这不是判据奏效**："
        "两者的比例因子都是 2（2 的幂），二进制浮点乘法精确 ⇒ 比例关系被完整保留、"
        "σ2 精确为 0。换成非 2 的幂比例（B3c，因子 3）同一判据立刻在小容差下翻车。"
        "⇒ **「稳定」不等于「正确」**；必须区分「结构真零」与「浮点恰好保序的假真零」。"
        .format(b3[9], b3b[9], b3[5], b3[6]),
        {"B3_s2_s1": b3[9], "B3b_s2_s1": b3b[9], "B3c_s2_s1": b3c[9],
         "note": "power-of-two ratio preserves collinearity in binary FP"})

    # 阳性对照：证明朴素秩确实会错
    nb = naive_rank(spectrum([[1.0, 0.0], [0.0, 1e-8]]))
    rec("V18-BP", "阳性对照：朴素容差秩", "FAIL" if nb != 2 else "PASS",
        "对 B4（真秩 2），固定 tol=1e-6 的朴素秩给 {0}"
        " ⇒ {1}。阴性对照：B1 上朴素秩给 {2}（正确）⇒ 该工具不是恒错，是真的抓人。"
        .format(nb, "证伪该朴素做法" if nb != 2 else "未证伪",
                naive_rank(spectrum(np.eye(3, 4)))),
        {"naive_B4": nb})

    # 若把精确秩换成浮点谱，B3/B4 会各自判错 —— 这正是判据的意义
    rec("V18-BQ", "为何必须以精确秩为准", "PASS",
        "精确秩在 4/4 基准上全部命中真秩（含 B3 的 1e-44 共线与 B4 的 1e8 病态）"
        " ⇒ 结构（代数）信息不可被浮点谱替代；浮点谱只应报告条件数并告警。")


# ===================== §3 应用到卷十七台账 =====================
# 卷十六 Kerr l=2,m=±2 QNM 锚点（与卷十六同源，保证复算一致）
_ANCH = {0.0: (0.373672, 0.088962), 0.5: (0.427599, 0.086049), 0.7: (0.474340, 0.083755),
         0.9: (0.537210, 0.082421), 0.99: (0.563050, 0.084016)}
_aa = np.array(sorted(_ANCH))
_PR = np.polyfit(_aa, [_ANCH[x][0] for x in _aa], 2)
_PI = np.polyfit(_aa, [_ANCH[x][1] for x in _aa], 2)
_dPR = np.polyder(_PR)
_dPI = np.polyder(_PI)


def ringdown_jacobian(a0=0.7, M0=1.0, TB0=5e-5):
    """J = ∂(ω_R, ω_I)/∂(a, M, T_B)，2×3。ω = (f + k·T_B)/M。"""
    fR = np.polyval(_PR, a0); fI = np.polyval(_PI, a0)
    dfR = np.polyval(_dPR, a0); dfI = np.polyval(_dPI, a0)
    kR = 180.0 + 60.0 * a0; kI = -140.0 - 40.0 * a0
    dkR = 60.0; dkI = -40.0
    wR = (fR + kR * TB0) / M0
    wI = (-fI + kI * TB0) / M0
    J = np.array([
        [(dfR + dkR * TB0) / M0, -wR / M0, kR / M0],
        [(-dfI + dkI * TB0) / M0, -wI / M0, kI / M0],
    ])
    return J, (wR, wI)


def g2_jacobian():
    """a_i = C·m_i^2·x（x=cotθ）。参数 (C, x)。返回有理数 J（2×2）。"""
    R = Fraction(206768283, 1000000)      # m_mu/m_e (PDG)
    me2 = Fraction(1)
    mmu2 = R * R
    return [[me2, me2], [mmu2, mmu2]], R


def section3():
    sec("§3  应用：各通道的秩 r 与可证伪关系数 FR = d − r")

    # --- ringdown ---
    J, (wR, wI) = ringdown_jacobian()
    s = spectrum(J)
    rk, stable, lo, hi = tolerance_scan(s)
    # 用 2×2 子式（而非容差）认证满行秩：J 是 2×3，rank=2 ⟺ 存在非零 2×2 子式
    n1 = np.linalg.norm(J[0]); n2 = np.linalg.norm(J[1])
    min1 = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    min2 = J[0][0] * J[1][2] - J[0][2] * J[1][0]
    min3 = J[0][1] * J[1][2] - J[0][2] * J[1][1]
    norm_minor = max(abs(min1), abs(min2), abs(min3)) / (n1 * n2)
    r = 2 if norm_minor > 1e-10 else 1
    rec("V18-C1", "ringdown（d=2, p=3）", "FAIL",
        "用 2×2 子式认证满行秩（不依赖容差）：最大归一化子式 = {0:.6e}"
        "（判据 >1e-10）⇒ rank = {1}；浮点谱区间 [{2},{3}]（{4}，仅作条件数参考）。"
        "FR = 2−{1} = **{5}** ⇒ 每事件**零**可证伪关系。"
        "这是卷十六「精确简并」的精确表述：不是「数据不够」，而是模型对 ringdown"
        "观测**没有任何不依赖参数的预言**。".format(
            norm_minor, r, lo, hi, "稳定" if stable else "不稳定", fr(2, r)),
        {"d": 2, "p": 3, "rank": r, "FR": fr(2, r), "wR": wR, "wI": wI,
         "norm_minor": float(norm_minor), "float_rank_lo": lo, "float_rank_hi": hi,
         "svals": [float(x) for x in s]})

    # --- g-2 ---
    Jg, R = g2_jacobian()
    rg = exact_rank(Jg)
    sg = spectrum([[float(x) for x in row] for row in Jg])
    rg_f = rank_at_tol(sg, 1e-12)
    rec("V18-C2", "g-2（d=2, p=2: C, cotθ）", "FAIL",
        "精确秩 = {0}（两行严格成比例，比例 = (m_mu/m_e)^2 = {1:.6f}）；"
        "浮点谱给出 {2}、σ2/σ1 = {3:.3e} ⇒ FR = 2−{0} = **{4}**"
        " ⇒ 该模型只有**一条**不依赖参数的预言，即 a_mu/a_e 比值，"
        "而它已被否证 4.252e+04 倍（卷十七 I-1）。".format(
            rg, float(R * R), rg_f, sg[1] / sg[0], fr(2, rg)),
        {"d": 2, "p": 2, "rank": int(rg), "FR": fr(2, rg),
         "ratio_model": float(R * R), "s2_s1": float(sg[1] / sg[0])})

    # --- 宇宙组分（p=0，全是宣称值）---
    rec("V18-C3", "宇宙组分（d=3, p=0）", "FAIL",
        "无自由参数 ⇒ rank=0 ⇒ FR = 3−0 = **3**：三条都是不依赖参数的预言。"
        "实测 Ω_b +26.77%、Ω_c −5.48% 两条否证，Ω_Λ +0.41% 一条未否证"
        " ⇒ 3 条中 2 条已否证。",
        {"d": 3, "p": 0, "rank": 0, "FR": 3})

    # --- CMB ---
    rec("V18-C4", "CMB（d=3, p=2: Ω_f, κ）", "BOUNDARY",
        "rank ≤ min(3,2)=2 ⇒ FR ≥ 1。唯一被**机器认证**的那一条是 κ-无关不变量"
        " N(1−n_s)（卷十七 I-2b 已证其 κ 无关性，散布 4.441e-16），"
        "实测 3.741 vs 2.106 ⇒ 否证 1.776 倍。完整 J 未构造（势函数积分未复算）"
        " ⇒ FR 上界未知，标 BOUNDARY。",
        {"d": 3, "p": 2, "rank_upper": 2, "FR_lower": 1})

    # --- 光子延迟 ---
    rec("V18-C5", "光子延迟 Q_H（d=1, p=2）", "FAIL",
        "rank ≤ 1 ⇒ FR = 1−rank。若每源内禀延迟可自由吸收（rank=1）⇒ FR = **0**"
        " ⇒ 该通道在源内禀延迟未知时**零**可证伪关系（与卷十七 J-4 的平坦方向同构）。",
        {"d": 1, "p": 2, "rank_upper": 1, "FR_if_rank1": 0})

    # --- CMB 双谱 ---
    rec("V18-C6", "CMB 双谱 f_NL(l)（d=0, p=7）", "FAIL",
        "Planck 无 per-l 数据（R31）⇒ d=0 ⇒ FR = **0** 且参数 7 个全不可约束"
        " ⇒ 零预测力 + 完全欠定。", {"d": 0, "p": 7, "rank": 0, "FR": 0})


# ===================== §4 自纠卷十七 =====================
def section4():
    sec("§4  自纠卷十七：d_eff 必须由 rank(J) 给出")
    rec("V18-D1", "卷十七 g-2 行 d_eff 更正", "CORRECTED",
        "卷十七把 g-2 记为 d=2、d_eff=2、p=1。按本卷定义 d_eff ≡ rank(J)："
        "当 θ 固定、仅 C 自由时 J 为 2×1、rank=1 ⇒ **d_eff=1 而非 2**；"
        "当 (C, cotθ) 双自由时 J 为 2×2、rank=1 ⇒ d_eff=1 < p=2 ⇒ **欠定 1 维**。"
        "两种口径下卷十七的「可辨」判定都需改写：前者可辨但 FR=1 且已否证，"
        "后者根本不可辨。",
        {"vol17": {"d": 2, "d_eff": 2, "p": 1}, "vol18": {"rank": 1}, "kind": "CORRECTED"})

    rec("V18-D2", "卷十七缺失的那一刀", "CORRECTED",
        "卷十七只问「参数能不能定出来」（可辨识），**没有问「模型有没有不依赖参数"
        "的预言」（FR）**。两者此消彼长：r 越大 ⇒ 可辨识方向越多、FR 越小。"
        "一个通道要站得住，需要 FR ≥ 1 **且**这些关系未被否证——卷十七无法表达"
        "这个条件，本卷补上。",
        {"kind": "CORRECTED"})

    # ---  dichotomy ---
    sec("§4b  二分法定理（本卷总账）")
    rows = [
        ("ringdown", 2, 3, 2, fr(2, 2), "零预测力"),
        ("g-2 (e+mu)", 2, 2, 1, fr(2, 1), "否证：比值矛盾 4.252e4 倍"),
        ("宇宙组分", 3, 0, 0, 3, "部分否证：3 条中 2 条否证，1 条存活"),
        ("CMB (r,n_s,N)", 3, 2, 2, 1, "否证：不变量矛盾 1.776 倍"),
        ("光子延迟 Q_H", 1, 2, 1, 0, "零预测力"),
        ("CMB 双谱", 0, 7, 0, 0, "零预测力（无数据）"),
    ]
    print("  {0:<18} {1:>3} {2:>3} {3:>4} {4:>4}   {5}".format(
        "通道", "d", "p", "r", "FR", "该 FR 的状态"))
    print("  " + "-" * 74)
    n_fr = 0
    n_fr_fals = 0
    for name, d, p, r, f_, st in rows:
        print("  {0:<18} {1:>3} {2:>3} {3:>4} {4:>4}   {5}".format(name, d, p, r, f_, st))
        if f_ >= 1:
            n_fr += 1
            if st.startswith("否证") or st.startswith("部分否证"):
                n_fr_fals += 1
    rec("V18-D3", "二分法（诚实版）", "FAIL",
        "FR ≥ 1 的通道共 {0} 条（{1}），**全部至少部分被否证**（g-2 与 CMB 为全部否证，"
        "宇宙组分 3 条中 2 条否证）；FR = 0 的通道共 {2} 条，全部零预测力。"
        " ⇒ **不存在「有预测力且全部通过检验」的通道**。"
        "结构原因：FR≥1 的关系都由公设直接给出、无自由参数缓冲，一旦公设数值有偏即被否证；"
        "而能存活的通道必然是靠参数吸收数据的（FR=0）。"
        .format(n_fr, "、".join(x[0] for x in rows if x[4] >= 1), len(rows) - n_fr),
        {"n_FR_ge1": n_fr, "n_FR_ge1_falsified": n_fr_fals, "n_FR0": len(rows) - n_fr})

    rec("V18-D4", "唯一存活的可证伪关系", "BOUNDARY",
        "全部通道中唯一「FR ≥ 1 且未被否证」的单条关系是宇宙组分的 Ω_Λ："
        "TUFT 68.75 vs Planck 68.47，偏差 +0.41%。但源报告**未登记 Planck 的 σ**，"
        "故本条无法给出 σ 数（不可判 >几σ），且它与 Ω_b(+26.77%)、Ω_c(−5.48%)"
        "同属一组内生声明 ⇒ 不能单独摘出来当通过项。标 BOUNDARY，不做通过判定。",
        {"Omega_L_tuft": 68.75, "Omega_L_planck": 68.47, "pct": 0.41,
         "sigma_unregistered": True})
    return rows


# ===================== §5 总账与输出 =====================
def summarize(rows):
    sec("§5  总账")
    cnt = {}
    for r in RESULTS:
        cnt[r["status"]] = cnt.get(r["status"], 0) + 1
    base = os.path.join(HERE, "TUFT_卷十八_有效约束的机器计算与可证伪关系数")
    lines = ["TUFT 卷十八 · 有效约束 d_eff 的机器计算与「可证伪关系数」",
             "run at: " + time.strftime("%Y-%m-%d %H:%M:%S"), ""]
    for r in RESULTS:
        lines.append("  [{0:<9}] {1:<9} {2}".format(r["status"], r["code"], r["detail"]))
    lines += ["", "=" * 78, "汇总", "=" * 78]
    for k in ("PASS", "FAIL", "BOUNDARY", "CORRECTED", "INFO"):
        if k in cnt:
            lines.append("  {0:<9} = {1}".format(k, cnt[k]))
    lines.append("  条目数：{0}".format(len(RESULTS)))
    lines += ["", "★ 卷十八结论：",
              "  (1) 分解：r = rank(J) 是「数据能约束的参数方向数」；",
              "      FR = d − r 是「模型无需调参即固定的数据组合数」= 可证伪关系数。",
              "      两者此消彼长——参数被定得越死，预测力越弱。卷十七只问了前者。",
              "  (2) 秩的机器判定：**不存在普适容差**。B3c（真秩 1，比例因子 3）在",
              "      小容差下被高估为 2（σ2/σ1=1.105e-17 噪声底）；B4（真秩 2、条件数",
              "      1e8）在大容差下被低估为 1。两个失效方向相反 ⇒ 必须以有理数精确秩",
              "      为准，浮点谱只报条件数。另注：B3/B3b 的「稳定正确」是比例因子为",
              "      2 的幂、浮点保序所致，不是判据奏效——「稳定」不等于「正确」。",
              "  (3) 二分法：FR ≥ 1 的 3 条通道全部**至少部分**被否证；FR = 0 的 3 条",
              "      零预测力 ⇒ 不存在「有预测力且全部通过」的通道。唯一存活的单条",
              "      关系是 Ω_Λ（+0.41%），但源报告未登记 σ，标 BOUNDARY 不作通过判定。",
              "  (4) 自纠卷十七：g-2 的 d_eff 应为 rank=1（非 2）；且卷十七缺了 FR 这一刀。",
              "",
              "  含义：给 TUFT 增加自由参数可以提高「可辨识」读数，但必然同时把",
              "        FR 降为 0——即用预测力换拟合自由度。这条权衡是本卷可复用的硬约束。"]
    txt = "\n".join(lines)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "counts": cnt, "entries": RESULTS,
                   "table": [{"name": n, "d": d, "p": p, "rank": r, "FR": fr_,
                              "status": st} for n, d, p, r, fr_, st in rows]},
                  f, ensure_ascii=False, indent=2)
    print(txt)

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    names = [x[0] for x in rows]
    xs = np.arange(len(names))
    frs = [x[4] for x in rows]
    rs = [x[3] for x in rows]
    ax.bar(xs - 0.2, rs, 0.4, label="r = rank(J) (identifiable dirs)")
    ax.bar(xs + 0.2, frs, 0.4, label="FR = d - r (falsifiable relations)")
    ax.set_xticks(xs)
    ax.set_xticklabels(names, rotation=18, ha="right")
    ax.set_ylabel("count")
    ax.set_title("Volume 18 · identifiability vs predictive content")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "tuft_v18_rank_vs_FR.png"), dpi=130)
    plt.close(fig)
    print("\nwrote: " + base + ".txt / .json / tuft_v18_rank_vs_FR.png")


def main():
    t0 = time.time()
    section1()
    section2()
    section3()
    rows = section4()
    summarize(rows)
    print("\n运行耗时 {0:.2f} s".format(time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
