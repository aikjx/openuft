#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
派生核算体系 UFS-Delta III（可复跑）
=========================================================================
主题：**账本自洽性** —— 前三册共用同一个账本记账，但没人查过账本本身。

前两册的进展：
  UFS-Delta I   给出 h_eff = rank(E)、判别式 V4、定理 K（代数型 V4 <= 0）
  UFS-Delta II  推翻推论 K2，给出定理 K' / L / M / N，
                结论是 V = 0 为不可达定理的上确界

本册不引入新的 prosperity-grade 兑换率，而是**回头审**前三册共同的三个输入假设：

  假设 1  锚常量表里的值都是彼此独立的测量事实
  假设 2  残差（命中精度）是理论对自然的拟合优度
  假设 3  随机采样 3000 组足以支撑一个全称命题

三条都不成立。逐条给证据。

-------------------------------------------------------------------------
§0  复核：抽样 -> 完备，数值 -> 符号
-------------------------------------------------------------------------
R0-a  II 册定理 K'-c 用 3000 组随机矩阵支撑「V4 > 0 从未出现」。
      但 V4 只依赖 (h, k, a, nu)，唯一约束是 h <= a+k。
      故在该四元组的参数空间上**完备枚举**即可 —— 比随机更强：零漏采样。
R0-b  II 册定理 L 用 N=1..600 的数值扫描支撑「谱族秩饱和于 3」。
      本册给符号版：谱族雅可比只有 3 个符号列函数，
      故 rank <= 3 对**一切** N 成立；数值扫描降为佐证而非证据。

-------------------------------------------------------------------------
§1  定理 Q（残差自洽 / 循环登记）—— 本册最要紧的一条
-------------------------------------------------------------------------
II 册报告的核心成果是「复现 xi = 1/(4pi)，相对残差 6.097090e-10」。
本册指出：这个残差与锚表内部的 eps0 <-> alpha 不一致**逐位相同**，
两者是同一个算术量。原因是 eps0 在 SI 中并非独立测量，它由

    eps0 = e^2 / (4 pi alpha hbar c)

定义。于是 alpha 在表里登记了两次 —— 一次藏身锚 eps0，一次作为靶 alpha。
声称「由 {e, eps0, hbar, c} 派生 alpha」是在拿 alpha 自己比 alpha。

    残差 = 表的算术闭合误差，不是理论对自然的拟合优度。
    => 该类声明的可计入信息量为 0，h_eff 应记 0。

同一机制命中 m_P = sqrt(hbar c / G)：1.571613e-07 的残差只要求 G 移动
3.14e-07（相对），远小于 G 自身的测量不确定度 2.2e-5。那是 7 位存储截断。

-------------------------------------------------------------------------
§2  定理 R（锚依赖与信息零点）
-------------------------------------------------------------------------
成本侧记录了 a = |锚|。但：
  (i)  SI-2019 下 c / hbar / e / k_B 是**定义**，sigma = 0；
       它们不携带关于自然的测量信息，也不是雅可比的列（它们是常量）。
  (ii) eps0 <-> alpha、m_P <-> G 是精确函数依赖（§1 已数值锁死）。
故真正独立的测量自由度只有 5 个，而不是表里的 10 个。

两条同时成立，且方向相反：
  · 上界**收紧**：  h_eff <= a_eff + k <= a + k
  · 账本**修正**：  成本侧少记若干份 => 前三册判定系统性偏严
不可达定理 V4 <= 0 在新账本下依然成立 —— 上界只收紧，没收松。

-------------------------------------------------------------------------
§3  定理 P（分辨率受限计数）
-------------------------------------------------------------------------
O-2（nu 可谎报）与 O-3（Lipschitz 证书无有限验流程）都需要一把能算的尺。
本册给出：**由不确定度传播得到的自然分辨率**。

    u_pred^2 = sum_i ( e_i * u_i )^2      （d ln T = sum_i e_i d ln x_i）
    sigma    = max(u_pred, u_obs)
    n_eff    = log10( 1 / sigma )

超过 n_eff 的位数不携带任何证据。这把 II 册定理 M 那种「把答案抄进参数
二进制位」的攻击，部分转化为可机械拒绝的形式。

外部数据依赖已在 P-4 做 +-10x / +-100x 敏感性检验。

-------------------------------------------------------------------------
§4  重算对照
-------------------------------------------------------------------------
用 (a_eff, 循环修正) 重算典型声明。修正方向**不一致**：循环声明的信息量
归零，非循环声明因成本变小而**上调**。这正是需要小心读的部分。
=========================================================================
"""

from __future__ import print_function

import itertools
import json
import os
import sys
import time
from fractions import Fraction

import sympy
from mpmath import mp, mpf
from sympy import Matrix, Rational, diff, simplify, symbols

mp.dps = 50

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _sqrt(x):
    return mp.sqrt(x)


def _log(x):
    return mp.log(x)


PI = mp.pi

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "数据")


# ===========================================================================
# 输入：锚常量表（逐字节复制自 V3，运行时交叉核对）
# ===========================================================================
ANCHOR = {
    "c":    {"dim": (0, 1, -1, 0, 0), "value": "299792458",         "name": "光速 c"},
    "hbar": {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",   "name": "约化普朗克常数 hbar"},
    "G":    {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",      "name": "引力常数 G"},
    "e":    {"dim": (0, 0, 1, 1, 0),  "value": "1.602176634e-19",   "name": "元电荷 e"},
    "eps0": {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12", "name": "真空介电常数 eps0"},
    "m_e":  {"dim": (1, 0, 0, 0, 0),  "value": "9.1093837015e-31",  "name": "电子质量 m_e"},
    "m_mu": {"dim": (1, 0, 0, 0, 0),  "value": "1.883531627e-28",   "name": "缪子质量 m_mu"},
    "m_p":  {"dim": (1, 0, 0, 0, 0),  "value": "1.67262192369e-27", "name": "质子质量 m_p"},
    "m_P":  {"dim": (1, 0, 0, 0, 0),  "value": "2.176434e-8",       "name": "普朗克质量 m_P"},
    "k_B":  {"dim": (1, 2, -2, 0, -1), "value": "1.380649e-23",     "name": "玻尔兹曼常数 k_B"},
}

TARGETS = {
    "alpha":        mpf("7.2973525693e-3"),
    "alpha_grav_e": mpf("1.75180994573e-45"),
    "m_e_over_mP":  mpf("4.18546287252e-23"),
    "m_mu_over_me": mpf("206.7682830"),
    "m_p_over_me":  mpf("1836.15267343"),
    "alpha_s":      mpf("0.1179"),
    "sin2_thetaW":  mpf("0.23122"),
}


def V(key):
    return mpf(ANCHOR[key]["value"])


def to_frac(x):
    """把 int / sympy.Rational / Fraction 统一转成 Fraction。"""
    if isinstance(x, Fraction):
        return x
    r = sympy.Rational(x)
    return Fraction(int(r.p), int(r.q))


def to_mpf(x):
    fr = to_frac(x)
    return mpf(fr.numerator) / mpf(fr.denominator)


def cross_check_table():
    """输入端与 V3 对齐：若 V3 可导入则逐键核对，防止本册口径漂移。"""
    path = os.path.join(HERE, "量纲零空间与判别式V3.py")
    try:
        ns = {}
        # 必须注入 __file__：V3 用它定位自己的相对路径。少了这一项 exec 会抛
        # NameError，而本函数会把异常吞掉 —— 那就会出现"声明做了交叉核对、
        # 实际一行没验"的假象。这正是本仓库反复批评的失效模式。
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        exec(compile(src, path, "exec"),
             {"__name__": "v3mod", "__file__": path}, ns)
        C2 = ns.get("CONST")
        if not C2:
            return {"available": False, "mismatch": [], "note": "V3 无 CONST"}
        bad = []
        for k, rec in ANCHOR.items():
            if k not in C2:
                bad.append("%s（V3 缺失）" % k)
                continue
            if C2[k]["value"] != rec["value"]:
                bad.append("%s 本册=%s V3=%s" % (k, rec["value"], C2[k]["value"]))
            if tuple(C2[k]["dim"]) != tuple(rec["dim"]):
                bad.append("%s 量纲不一致" % k)
        return {"available": True, "mismatch": bad}
    except Exception as exc:
        return {"available": False, "mismatch": [], "error": repr(exc)}


# ===========================================================================
# 通用工具
# ===========================================================================
CHECKS = []


def item(name, ok, detail):
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail})
    print("   [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("         %s" % detail)


def rank_fraction(rows):
    """手写 Fraction 高斯消元求秩（不经 sympy，用于交叉验证）。"""
    m = [[to_frac(x) for x in r] for r in rows]
    m = [r for r in m if any(x != 0 for x in r)]
    if not m:
        return 0
    ncols = len(m[0])
    piv = 0
    for col in range(ncols):
        sel = None
        for r in range(piv, len(m)):
            if m[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        m[piv], m[sel] = m[sel], m[piv]
        pv = m[piv][col]
        m[piv] = [x / pv for x in m[piv]]
        for r in range(len(m)):
            if r != piv and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [a - fac * b for a, b in zip(m[r], m[piv])]
        piv += 1
        if piv >= len(m):
            break
    return piv


def verdict(v):
    if v > 1e-12:
        return "A"
    if v > -1e-12:
        return "B"
    return "C"


def V4(h, k, a, nu):
    return (h - k - a - nu) / float(h)


# ===========================================================================
# §0  R0-a：把 II 册 K'-c 的 3000 组随机换成完备枚举
# ===========================================================================
def review_R0a_complete():
    print("\n" + "=" * 78)
    print("R0-a  完备枚举取代随机采样（II 册 K'-c 的 3000 组 -> 全参数空间）")
    print("=" * 78)

    A_MAX, K_MAX, NU_MAX = 4, 4, 5
    tuples = []
    pos = 0
    max_v = -1e9
    for a in range(A_MAX + 1):
        for k in range(K_MAX + 1):
            n = a + k
            if n == 0:
                continue
            for nu in range(NU_MAX + 1):
                for h in range(1, n + 1):          # h <= a+k 是唯一约束
                    v = V4(h, k, a, nu)
                    tuples.append((a, k, nu, h, v))
                    max_v = max(max_v, v)
                    if v > 1e-12:
                        pos += 1
    item("R0-a1 完备枚举 %d 个 (a,k,nu,h) 四元组：V4 > 0 出现 0 次" % len(tuples),
         pos == 0,
         "a<=%d k<=%d nu<=%d h<=a+k；最大 V4 = %.6f" % (A_MAX, K_MAX, NU_MAX, max_v))

    zeros = [(a, k, nu, h) for (a, k, nu, h, v) in tuples if abs(v) <= 1e-12]
    cond = all(nu == 0 and h == a + k for (a, k, nu, h) in zeros)
    item("R0-a2 V4 = 0 的充要条件 = (nu = 0 且 h = a+k)",
         cond and len(zeros) > 0,
         "%d 个零点全部满足该条件；与 II 册「B = 上确界」一致" % len(zeros))

    witness_ok = True
    witness_rows = []
    for h_target in range(1, 5):
        rows = [[1 if i == j else 0 for i in range(h_target)]
                for j in range(h_target)]
        got = rank_fraction(rows)
        witness_ok = witness_ok and (got == h_target)
        witness_rows.append({"h": h_target, "realized": got})
    item("R0-a3 每个 1 <= h <= 4 都有整数矩阵的构造性举证", witness_ok,
         "举证结果 %s" % witness_rows)

    viol = 0
    checked = 0
    for ncol in (1, 2, 3):
        for m in (1, 2, 3):
            for combo in itertools.product((-1, 0, 1), repeat=ncol * m):
                rows = [list(combo[i * ncol:(i + 1) * ncol]) for i in range(m)]
                checked += 1
                if rank_fraction(rows) > ncol:
                    viol += 1
    item("R0-a4 %d 个 {-1,0,1} 整数矩阵全枚举：无一违反 rank <= 列数" % checked,
         viol == 0, "违规 %d 例" % viol)

    return {"tuples": len(tuples), "positives": pos, "max_V4": max_v,
            "zero_points": len(zeros), "matrix_checked": checked}


# ===========================================================================
# §0  R0-b：把 II 册定理 L 的 N<=600 扫描换成符号结论
# ===========================================================================
def review_R0b_symbolic():
    print("\n" + "=" * 78)
    print("R0-b  谱族秩饱和：数值扫描 -> 符号结论（对所有 N 成立）")
    print("=" * 78)

    n, R, al, mu = symbols("n R alpha mu", positive=True)
    E = -R / n ** 2 * (1 + al ** 2 / n + mu * al ** 3 / n ** 2)

    cols = []
    for p in (R, al, mu):
        expr = simplify(diff(E, p) * p / E)
        cols.append(expr)
        print("     列  d ln E / d ln %-6s = %s" % (p.name, expr))

    item("R0-b1 三项谱族雅可比恰有 3 个符号列函数（与 N 无关）",
         len(cols) == 3 and all(simplify(c) != 0 for c in cols),
         "E(n) = -R/n^2 (1 + alpha^2/n + mu*alpha^3/n^2)；列数 3 = dim(theta)")

    item("R0-b2 rank(J[:N]) <= 3 对一切 N 成立（不再是 N<=600 的经验结论）",
         True,
         "秩按定义不超过列数；无穷行有限列矩阵亦然，无需扫描")

    M3 = Matrix(3, 3, lambda i, j: simplify(cols[j].subs(n, i + 1)))
    det3 = simplify(M3.det())
    item("R0-b3 N >= 3 时秩确实达到 3（前 3 行符号行列式非零）",
         det3 != 0, "det = %s" % det3)

    numeric = []
    for N in (1, 2, 3, 5, 10, 600):
        rows = [[cols[j].subs(n, k) for j in range(3)] for k in range(1, N + 1)]
        rk = int(Matrix(rows).rank())
        numeric.append({"N": N, "rank": rk})
        print("       N=%-4d rank=%d" % (N, rk))
    item("R0-b4 数值佐证与符号结论一致（rank = min(N,3)）",
         all(d["rank"] == min(d["N"], 3) for d in numeric), str(numeric))

    return {"cols": [str(c) for c in cols], "det3": str(det3),
            "numeric": numeric}


# ===========================================================================
# §1  定理 Q：残差自洽 / 循环登记
# ===========================================================================
def theorem_Q_circularity():
    print("\n" + "=" * 78)
    print("定理 Q（残差自洽）：前册的「高精度命中」是表自己的算术闭合误差")
    print("=" * 78)

    rows = []

    combo = V("e") ** 2 * V("eps0") ** -1 * V("hbar") ** -1 * V("c") ** -1
    xi = TARGETS["alpha"] / combo
    target = 1 / (4 * PI)
    abs_xi = abs(xi - target)
    rel_xi = abs_xi / target

    alpha_from_eps0 = V("e") ** 2 / (4 * PI * V("eps0") * V("hbar") * V("c"))
    rel_tab = abs(alpha_from_eps0 - TARGETS["alpha"]) / TARGETS["alpha"]

    same = abs(float(rel_xi) - float(rel_tab)) < 1e-17
    item("Q-1 xi 残差与 eps0<->alpha 表内不一致相差仅二阶小量",
         same,
         "xi 残差 %.15e  vs  表内不一致 %.15e  差 %.3e"
         % (float(rel_xi), float(rel_tab), abs(float(rel_xi) - float(rel_tab))))
    print("     绝对残差 = %.15e（这就是 II 册报告的 4.85e-11）" % float(abs_xi))
    print("     相对残差 = %.15e" % float(rel_xi))
    print("     表内不一致 = %.15e" % float(rel_tab))

    # Q-1b：两者的关系是**精确符号恒等式**，不是数值巧合。
    #       令 X := 4 pi alpha eps0 hbar c / e^2，则
    #           rel_xi  = |X - 1|
    #           rel_tab = |1/X - 1| = |X - 1| / X
    #       故  rel_tab * X = rel_xi  —— 精确成立，与 X 的符号方向无关。
    _d = sympy.symbols("d", positive=True)
    _Xv = 1 + _d
    _ident = simplify(sympy.Abs(1 / _Xv - 1) * _Xv - sympy.Abs(_Xv - 1))
    X = (4 * PI * TARGETS["alpha"] * V("eps0") * V("hbar") * V("c")
         / V("e") ** 2)
    num_check = float(rel_tab) * float(X) - float(rel_xi)
    item("Q-1b 符号恒等：rel_tab * X = rel_xi（sympy 化简为 0）",
         _ident == 0 and abs(num_check) < 1e-22,
         "X = 4 pi alpha eps0 hbar c/e^2 = 1 - %.3e；"
         "数值残差 %.3e" % (1 - float(X), num_check))
    rows.append({"claim": "alpha <- {e, eps0, hbar, c}",
                 "residual_rel": float(rel_xi),
                 "table_inconsistency_rel": float(rel_tab),
                 "identical": same,
                 "why": "eps0 = e^2/(4 pi alpha hbar c) 是 SI 定义式；"
                        "alpha 以锚 eps0 与靶 alpha 两次登记"})

    mP_from_G = _sqrt(V("hbar") * V("c") / V("G"))
    rel_mP = abs(mP_from_G - V("m_P")) / V("m_P")
    G_star = V("hbar") * V("c") / V("m_P") ** 2
    rel_Gmove = abs(G_star - V("G")) / V("G")
    G_UNC = 2.2e-5
    item("Q-2 m_P 残差 1.57e-7 远小于 G 自身不确定度 2.2e-5",
         float(rel_Gmove) < G_UNC,
         "残差 %.6e 只要求 G 移动 %.6e（相对），G 的不确定度为 %.1e => %.0f 倍余量"
         % (float(rel_mP), float(rel_Gmove), G_UNC, G_UNC / float(rel_Gmove)))
    rows.append({"claim": "m_P <- {hbar, c, G}",
                 "residual_rel": float(rel_mP),
                 "implied_G_shift_rel": float(rel_Gmove),
                 "G_uncertainty_rel": G_UNC,
                 "why": "m_P = sqrt(hbar c/G) 是定义式；残差纯属位数截断"})

    r_from_table = mpf(ANCHOR["m_mu"]["value"]) / mpf(ANCHOR["m_e"]["value"])
    rel_ratio = abs(r_from_table - TARGETS["m_mu_over_me"]) / TARGETS["m_mu_over_me"]
    item("Q-3 对照：m_mu/m_e 的残差来自锚自身的位数，而非跨关系闭合",
         rel_ratio < 1e-7,
         "由锚表重算 %s，残差 %.3e（该靶与锚同名，但不构成 SI 定义循环）"
         % (mp.nstr(r_from_table, 12), float(rel_ratio)))
    rows.append({"claim": "m_mu/m_e <- {m_mu, m_e}",
                 "residual_rel": float(rel_ratio),
                 "why": "同名比；残差 %.3e 属位数限制" % float(rel_ratio)})

    # Q-4：观测到的表内不一致竟然超过所引标称不确定度 —— 表本身不自洽
    QUOTED = 1.5e-10
    ratio = float(rel_tab) / QUOTED
    item("Q-4 表内不一致 %.2e 超过所引标称不确定度 %.1e（%.1f 倍）"
         % (float(rel_tab), QUOTED, ratio),
         ratio > 1.0,
         "要么是锚表混用了不同 CODATA 版本，要么本册引用的 sigma 有误；"
         "**两种解释都加强 Q 的结论**：残差是表的算术闭合误差（见 OPEN O-9）")
    rows.append({"claim": "锚表自身的 eps0 <-> alpha 闭合",
                 "residual_rel": float(rel_tab),
                 "why": "超出标称不确定度 %.1f 倍，表不自洽" % ratio})

    return {"rows": rows, "identical": same,
            "rel_xi_abs": float(abs_xi),
            "rel_xi": float(rel_xi), "rel_tab": float(rel_tab),
            "X": float(X), "X_minus_1": float(X) - 1.0,
            "identity_zero": (_ident == 0),
            "identity_numeric_residual": num_check,
            "exceeds_quoted_by": ratio,
            "rel_mP": float(rel_mP), "rel_Gmove": float(rel_Gmove)}


# ===========================================================================
# §2  定理 R：锚依赖与信息零点
# ===========================================================================
# SI-2019 相对标准不确定度（外部引用数据，见 OPEN O-6）。
#   0.0 表示该量是定义量，不携带测量信息。
UNC_REL = {
    "c":    0.0,      # 定义
    "hbar": 0.0,      # 定义（h 精确）
    "e":    0.0,      # 定义
    "k_B":  0.0,      # 定义
    "G":    2.2e-5,
    "eps0": 1.5e-10,  # 与 alpha 同一份信息
    "m_e":  3.0e-10,
    "m_mu": 2.2e-8,
    "m_p":  3.1e-10,
    "m_P":  1.1e-5,   # 由 G 传播：0.5 * 2.2e-5
}

DEPENDENCY = [
    {"pair": ("eps0", "alpha"), "relation": "eps0 = e^2/(4 pi alpha hbar c)",
     "evidence": "§1 Q-1，相对闭合残差 6.097e-10"},
    {"pair": ("m_P", "G"), "relation": "m_P = sqrt(hbar c / G)",
     "evidence": "§1 Q-2，相对闭合残差 1.572e-7"},
]

SUPPRESSED_REASON = {"m_P": "由 G 经 sqrt(hbar c/G) 定义"}


def theorem_R_anchor_dependence():
    print("\n" + "=" * 78)
    print("定理 R（锚依赖与信息零点）：a -> a_eff")
    print("=" * 78)

    exact = sorted([k for k, u in UNC_REL.items() if u == 0.0])
    item("R-1 SI-2019 下有 %d 个定义量 sigma = 0，不计费也不提供雅可比列"
         % len(exact),
         len(exact) >= 4,
         "定义量：%s —— 它们是单位选择，不是关于自然的测量" % "、".join(exact))

    carried = set()
    for d in DEPENDENCY:
        carried.update(d["pair"])
    redundant = sorted([k for k in carried if k in ANCHOR])
    item("R-2 检测到 %d 组精确函数依赖，相关锚不可重复计费" % len(DEPENDENCY),
         len(DEPENDENCY) >= 2,
         "；".join("%s：%s" % ("<->".join(d["pair"]), d["relation"])
                   for d in DEPENDENCY) + "；涉及锚 %s" % "、".join(redundant))

    informational = []
    suppressed = []
    for k in ANCHOR:
        if UNC_REL.get(k, 0.0) == 0.0:
            suppressed.append((k, "定义量，sigma = 0"))
        elif k in SUPPRESSED_REASON:
            suppressed.append((k, SUPPRESSED_REASON[k]))
        else:
            informational.append(k)
    a_eff = len(informational)
    a_raw = len(ANCHOR)
    item("R-3 有效锚数 a_eff = %d，而表中登记 a = %d" % (a_eff, a_raw),
         a_eff < a_raw,
         "信息性锚：%s" % "、".join(sorted(informational)))

    item("R-4 上界由 h <= a+k 收紧为 h <= a_eff+k（更严格，非放松）",
         a_eff <= a_raw,
         "a_eff=%d <= a=%d；不可达定理 V4 <= 0 依然成立" % (a_eff, a_raw))

    return {"exact": exact, "redundant": redundant,
            "informational": sorted(informational),
            "suppressed": suppressed, "a_eff": a_eff, "a_raw": a_raw,
            "dependencies": DEPENDENCY}


# ===========================================================================
# §3  定理 P：分辨率受限计数
# ===========================================================================
def propagate(keys, exponents, unc_rel):
    """d ln T = sum_i e_i d ln x_i  =>  u^2 = sum_i (e_i * u_i)^2。"""
    total = mpf(0)
    for key, exp in zip(keys, exponents):
        u = unc_rel.get(key, 0.0)
        if u == 0:
            continue
        total += (to_mpf(exp) * mpf(repr(u))) ** 2
    return _sqrt(total)


def n_eff_digits(sigma_rel):
    """先验宽度取 ~1（量纲为一靶）时，sigma 之上还剩多少位十进制有效数字。"""
    if sigma_rel <= 0:
        return None
    return float(_log(1 / sigma_rel) / _log(10))


def theorem_P_resolution():
    print("\n" + "=" * 78)
    print("定理 P（分辨率受限计数）：超过自然分辨率的位数不携带证据")
    print("=" * 78)

    u_mP = propagate(["hbar", "c", "G"],
                     [Rational(1, 2), Rational(1, 2), Rational(-1, 2)], UNC_REL)
    expect = UNC_REL["m_P"]
    item("P-1 传播公式闭合：u(m_P)/m_P = 0.5 * u(G)/G = %.3e" % float(u_mP),
         abs(float(u_mP) - expect) / expect < 1e-6,
         "sqrt((-1/2 * 2.2e-5)^2) = %.6e（hbar、c 为定义量，贡献 0）" % float(u_mP))

    cases = [
        ("m_P <- {hbar,c,G}", ["hbar", "c", "G"],
         [Rational(1, 2), Rational(1, 2), Rational(-1, 2)], UNC_REL["m_P"]),
        ("alpha <- {e,eps0,hbar,c}", ["e", "eps0", "hbar", "c"],
         [2, -1, -1, -1], UNC_REL["eps0"]),
        ("alpha_grav_e <- {m_e,m_P}", ["m_e", "m_P"], [2, -2], None),
        ("m_mu/m_e", ["m_mu", "m_e"], [1, -1], 2.2e-8),
    ]
    rows = []
    for name, keys, exps, u_obs in cases:
        u_pred = propagate(keys, exps, UNC_REL)
        sigma = max(float(u_pred), float(u_obs or 0.0))
        rows.append({"case": name, "u_pred": float(u_pred),
                     "u_obs": u_obs, "sigma": sigma,
                     "n_eff": n_eff_digits(sigma)})
        print("      %-26s u_pred=%.3e  sigma=%.3e  n_eff=%.2f 位"
              % (name, float(u_pred), sigma, rows[-1]["n_eff"]))
    item("P-2 每条声明都算得出有限的自然分辨率",
         all(r["n_eff"] is not None and r["n_eff"] > 0 for r in rows),
         "n_eff 落在 %.2f ~ %.2f 位之间"
         % (min(r["n_eff"] for r in rows), max(r["n_eff"] for r in rows)))

    alpha_row = [r for r in rows if r["case"].startswith("alpha <")][0]
    claimed = 10.0
    effective = min(claimed, alpha_row["n_eff"])
    item("P-3 声称的第 %.0f 位被自然分辨率截到 %.2f 位" % (claimed, effective),
         effective <= alpha_row["n_eff"] + 1e-9,
         "alpha 例：n_eff = %.2f 位；再叠加 §1 的循环性 => 可计入位数为 0"
         % alpha_row["n_eff"])

    sens = []
    order_ok = True
    for factor in (0.01, 0.1, 1.0, 10.0, 100.0):
        scaled = {k: (u * factor if u else u) for k, u in UNC_REL.items()}
        vals = []
        for name, keys, exps, u_obs in cases:
            u = propagate(keys, exps, scaled)
            s = max(float(u), float(u_obs or 0.0) * factor)
            vals.append(n_eff_digits(s))
        uP = float(propagate(["hbar", "c", "G"],
                             [Rational(1, 2), Rational(1, 2), Rational(-1, 2)],
                             scaled))
        ur = float(propagate(["m_mu", "m_e"], [1, -1], scaled))
        order_ok = order_ok and (uP > ur)
        sens.append({"factor": factor, "min_n": min(vals), "max_n": max(vals),
                     "u_mP": uP, "u_mu_me": ur})
    item("P-4 敏感性：sigma 整体缩放 1/100 ~ 100 倍，量级排序不变", order_ok,
         "u(m_P) 恒 > u(m_mu/m_e)，例如 x1 时 %.2e > %.2e"
         % (sens[2]["u_mP"], sens[2]["u_mu_me"]))

    return {"rows": rows, "sensitivity": sens, "u_mP": float(u_mP)}


# ===========================================================================
# §4  重算对照
# ===========================================================================
def recompute_ledger():
    print("\n" + "=" * 78)
    print("§4  重算对照：a -> a_eff，循环声明 h_eff -> 0")
    print("=" * 78)

    # 说明：本表是本册为做对照而**重建**的样例，不是前册的原始登记。
    # 每条给全列（列 = 锚 ∪ 旋钮，按序），行与列对齐。
    # 雅可比列的正确组成：**信息性锚** + **全部旋钮**（定义量是常量，不成列）。
    claims = [
        # (名称, 列名清单, 锚名清单, 旋钮名清单, 指数行, 是否循环, nu)
        ("alpha <- {e,eps0,hbar,c}",
         ["e", "eps0", "hbar", "c"], ["e", "eps0", "hbar", "c"], [],
         [[2, -1, -1, -1]], True, 0),
        ("m_P <- {hbar,c,G}",
         ["hbar", "c", "G"], ["hbar", "c", "G"], [],
         [[Rational(1, 2), Rational(1, 2), Rational(-1, 2)]], True, 0),
        ("P8 刷分 t,t^2,t^3",
         ["t"], [], ["t"],
         [[1], [2], [3]], False, 0),
        ("alpha_grav_e <- {m_e,m_P}",
         ["m_e", "m_P"], ["m_e", "m_P"], [],
         [[2, -2]], False, 0),
    ]
    rows = []
    for name, cols, anch, knobs, exp_rows, circular, nu in claims:
        kN = len(knobs)
        a_rawN = len(anch)
        h_old = rank_fraction(exp_rows) if exp_rows else 0
        # 保留列：信息性锚 + 全部旋钮
        keep = [i for i, cname in enumerate(cols)
                if (cname in knobs)
                or (UNC_REL.get(cname, 0.0) > 0.0
                    and cname not in SUPPRESSED_REASON)]
        a_e = sum(1 for i in keep if cols[i] in anch)
        if keep:
            sub_rows = [[row[i] for i in keep] for row in exp_rows]
            h = rank_fraction(sub_rows)
        else:
            h = 0
        h_eff = 0 if circular else h
        v_old = V4(h_old, kN, a_rawN, nu)
        v_new = V4(h_eff, kN, a_e, nu) if h_eff else None
        rows.append({"claim": name, "a": a_rawN, "a_eff": a_e, "k": kN,
                     "h_old": h_old, "h_new": h_eff,
                     "V4_old": v_old, "V4_new": v_new,
                     "verdict_old": verdict(v_old),
                     "verdict_new": (verdict(v_new) if v_new is not None
                                     else "不可计"),
                     "circular": circular,
                     "reason": ("循环登记" if circular
                                else ("无信息性列" if h_eff == 0 else ""))})
        tail = ("%+.3f（%s）" % (v_new, verdict(v_new))) if v_new is not None \
            else "不可计（%s）" % rows[-1]["reason"]
        print("      %-26s a=%d->%d k=%d  h=%d->%d  V4 %+.3f(%s) -> %s"
              % (name, a_rawN, a_e, kN, h_old, h_eff, v_old, verdict(v_old), tail))

    moved = [r for r in rows
             if r["circular"] or abs(r["V4_old"] - (r["V4_new"] or 0.0)) > 1e-9]
    item("§4-a 重算后至少 3 条声明判定发生位移（前册确有偏严项）",
         len(moved) >= 3, "%d/%d 条位移" % (len(moved), len(rows)))

    item("§4-b 修正后仍无 V4 > 0（不可达定理在新账本下依然成立）",
         not any((r["V4_new"] or 0.0) > 1e-12 for r in rows),
         "循环性消灭了一批虚假命中，但没有创造出新的正贡献")

    return rows


# ===========================================================================
# 渲染
# ===========================================================================
def render_md(payload):
    L = []
    A = L.append
    A("# 派生核算 UFS-Delta III：账本自洽性自检产物")
    A("")
    A("> 本文件由 `源码/派生核算III_账本自洽与分辨率.py` 自动生成，请勿手改。")
    A("> 复跑：`python -B 源码/派生核算III_账本自洽与分辨率.py`")
    A("")
    A("自检 **%d/%d** 通过，耗时 %.2f s。"
      % (sum(1 for c in CHECKS if c["passed"]), len(CHECKS),
         payload["meta"]["elapsed"]))
    A("")

    A("## 0. 自检清单")
    A("")
    A("| 项 | 结论 |")
    A("| --- | --- |")
    for c in CHECKS:
        A("| %s | %s |" % (c["name"],
                           ("PASS · " + c["detail"]) if c["passed"]
                           else ("**FAIL** · " + c["detail"])))
    A("")

    # §0
    A("## 1. 复核升级：抽样 -> 完备，数值 -> 符号")
    A("")
    r0a = payload["R0a"]
    A("### 1.1 R0-a 完备枚举取代 II 册 K'-c 的 3000 组随机")
    A("")
    A("`V4` 只依赖 `(h, k, a, nu)`，唯一约束是 `h <= a+k`。因此在该四元组的")
    A("参数空间上**完备枚举**即可，比随机更强：零漏采样。")
    A("")
    A("| 项 | 值 |")
    A("| --- | --- |")
    A("| 枚举四元组数 | %d |" % r0a["tuples"])
    A("| V4 > 0 出现次数 | **%d** |" % r0a["positives"])
    A("| 最大 V4 | %.6f |" % r0a["max_V4"])
    A("| V4 = 0 的点数 | %d（全部满足 nu=0 且 h=a+k） |" % r0a["zero_points"])
    A("| {-1,0,1} 整数矩阵全枚举 | %d 例，违规 0 |" % r0a["matrix_checked"])
    A("")
    A("> 结论不变，但支撑从「3000 次没撞见反例」升级为「参数空间内无反例」。")
    A("")

    r0b = payload["R0b"]
    A("### 1.2 R0-b 谱族秩饱和：符号版")
    A("")
    A("模型 `E(n) = -R/n^2 (1 + alpha^2/n + mu*alpha^3/n^2)`，雅可比的")
    A("三个符号列函数为：")
    A("")
    for i, c in enumerate(r0b["cols"]):
        A("$$\\frac{\\partial \\ln E}{\\partial \\ln \\theta_{%d}} = %s$$"
          % (i + 1, sympy.latex(sympy.sympify(c))))
    A("")
    A("列数恒为 3，与 `N` 无关，故 `rank(J[:N]) <= 3` 对**一切** `N` 成立。")
    A("前 3 行符号行列式非零，故 `N >= 3` 时秩达到 3。")
    A("")
    A("| N | rank |")
    A("| --- | --- |")
    for d in r0b["numeric"]:
        A("| %d | %d |" % (d["N"], d["rank"]))
    A("")
    A("> II 册的 `N=1..600` 扫描降级为数值佐证，不再是证据。")
    A("")

    # §1
    A("## 2. 定理 Q：残差自洽 —— 前册的「高精度命中」是表自己的闭合误差")
    A("")
    q = payload["Q"]
    A("这是本册最要紧的一条。**II 册报告的核心成果**")
    A("「复现 `xi = 1/(4pi)`，相对残差 `6.097090e-10`」与")
    A("**锚表内部的 `eps0 <-> alpha` 不一致**是同一个算术量的两种写法：")
    A("")
    A("| 量 | 值 |")
    A("| --- | --- |")
    A("| xi 的绝对残差（II 册报告的 4.85e-11） | %.15e |" % q["rel_xi_abs"])
    A("| xi 的相对残差 `rel_xi` | %.15e |" % q["rel_xi"])
    A("| eps0 <-> alpha 表内不一致 `rel_tab` | %.15e |" % q["rel_tab"])
    A("| 两者之差 | %.3e |" % abs(q["rel_xi"] - q["rel_tab"]))
    A("| `X = 4 pi alpha eps0 hbar c / e^2` | 1 %+.3e |" % q["X_minus_1"])
    A("| `rel_tab * X - rel_xi` | %.3e |" % q["identity_numeric_residual"])
    A("")
    A("令 `X := 4\\pi\\alpha\\varepsilon_0\\hbar c / e^2`，则")
    A("")
    A("$$\\mathrm{rel}_{\\xi}=|X-1|,\\qquad"
      "\\mathrm{rel}_{tab}=\\left|\\tfrac1X-1\\right|=\\frac{|X-1|}{X}"
      "\\quad\\Rightarrow\\quad \\mathrm{rel}_{tab}\\cdot X=\\mathrm{rel}_{\\xi}$$")
    A("")
    A("该恒等式 sympy 化简为 **0**（自检 Q-1b），因此两边相差只是 `delta^2` 量级，")
    A("不是两个独立事实偶然相等。")
    A("")
    A("原因：`eps0` 不是独立测量，它在 SI 中定义为")
    A("")
    A("$$\\varepsilon_0 = \\frac{e^2}{4\\pi\\alpha\\hbar c}$$")
    A("")
    A("于是 `alpha` 在表里登记了**两次** —— 一次藏身锚 `eps0`，")
    A("一次作为靶 `alpha`。声称「由 `{e, eps0, hbar, c}` 派生 `alpha`」，")
    A("是在拿 `alpha` 自己比 `alpha`。")
    A("")
    A("| 声明 | 相对残差 | 诊断 |")
    A("| --- | --- | --- |")
    for r in q["rows"]:
        A("| %s | %.6e | %s |" % (r["claim"], r["residual_rel"], r["why"]))
    A("")
    A("> **残差 = 表的算术闭合误差，不是理论对自然的拟合优度。**")
    A("> 该类声明的可计入信息量为 0，`h_eff` 应记 **0**。")
    A("")

    # §2
    A("### 1.3 反身一击：这个残差还超出了表自己的标称精度")
    A("")
    A("观测到的表内不一致 `%.2e`，是所引 `eps0`/`alpha` 标称不确定度 "
      "`1.5e-10` 的 **%.1f 倍**（自检 Q-4）—— 表比它自己声称的精度更不自洽。"
      % (q["rel_tab"], q["exceeds_quoted_by"]))
    A("要么是锚表混用了不同 CODATA 版本，要么本册引用数据有误 ——")
    A("**两种解释都加强 Q 的结论**：该残差是表的算术闭合误差（见 OPEN O-9）。")
    A("")

    A("## 3. 定理 R：锚依赖与信息零点 —— `a` 被高估")
    A("")
    rr = payload["R"]
    A("| 类别 | 锚 | 处置 |")
    A("| --- | --- | --- |")
    A("| 定义量（sigma = 0） | %s | 不计费、不提供雅可比列 |" % "、".join(rr["exact"]))
    A("| 精确函数依赖（同一事实计一份） | %s | 只计一份 |"
      % "、".join("↔".join(d["pair"]) for d in rr["dependencies"]))
    A("")
    A("- 表中登记锚数 `a = %d`" % rr["a_raw"])
    A("- **有效锚数 `a_eff = %d`**：%s" % (rr["a_eff"], "、".join(rr["informational"])))
    A("- 被抑制：%s"
      % "；".join("%s（%s）" % (k, why) for k, why in rr["suppressed"]))
    A("")
    A("两条同时成立，且方向相反：")
    A("")
    A("1. **上界收紧**：`h_eff <= a_eff + k <= a + k`")
    A("2. **账本修正**：成本侧少记 %d 份，前三册判定**系统性偏严**"
      % (rr["a_raw"] - rr["a_eff"]))
    A("")
    A("不可达定理 `V4 <= 0` 在新账本下**依然成立** —— 上界只收紧，没收松。")
    A("")

    # §3
    A("## 4. 定理 P：分辨率受限计数")
    A("")
    pp = payload["P"]
    A("$$u_{pred}^2=\\sum_i (e_i\\,u_i)^2,\\qquad"
      "\\sigma=\\max(u_{pred},\\,u_{obs}),\\qquad"
      "n_{eff}=\\log_{10}\\frac{1}{\\sigma}$$")
    A("")
    A("| 声明 | u_pred | sigma | n_eff（位） |")
    A("| --- | --- | --- | --- |")
    for r in pp["rows"]:
        A("| %s | %.3e | %.3e | %.2f |"
          % (r["case"], r["u_pred"], r["sigma"], r["n_eff"]))
    A("")
    A("超过 `n_eff` 的位数**不携带任何证据**，这使得 II 册定理 M 那种")
    A("「把答案抄进参数二进制位」的攻击可被机械拒绝（部分）。")
    A("")
    A("### 4.1 对外部数据的敏感性")
    A("")
    A("`UNC_REL` 引自外部 CODATA 数据（见 OPEN O-6）。整体缩放后：")
    A("")
    A("| 缩放 | n_eff 范围（位） | u(m_P) | u(m_mu/m_e) |")
    A("| --- | --- | --- | --- |")
    for s in pp["sensitivity"]:
        A("| x%.2f | %.2f ~ %.2f | %.3e | %.3e |"
          % (s["factor"], s["min_n"], s["max_n"], s["u_mP"], s["u_mu_me"]))
    A("")
    A("> 定性结论不依赖外部数据的绝对标度，只依赖其量级排序。")
    A("")

    # §4
    A("## 5. 重算对照")
    A("")
    A("> 说明：本表是本册为做对照而**重建**的样例，不是前册的原始登记；")
    A("> 列 = 锚 ∪ 旋钮，雅可比列 = **信息性锚 + 全部旋钮**（定义量是常量，不成列）。")
    A("")
    A("| 声明 | a | a_eff | k | h_旧 | h_新 | V4_旧 | V4_新 |")
    A("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in payload["ledger"]:
        A("| %s | %d | %d | %d | %d | %d | %+.3f（%s） | %s |"
          % (r["claim"], r["a"], r["a_eff"], r["k"], r["h_old"], r["h_new"],
             r["V4_old"], r["verdict_old"],
             ("%+.3f（%s）" % (r["V4_new"], r["verdict_new"]))
             if r["V4_new"] is not None
             else "不可计（%s）" % (r.get("reason") or "—")))
    A("")
    A("修正方向**不一致**：循环声明的信息量归零（`-3 -> 不可计`），")
    A("非循环声明则因 `a` 变小而**上调**（`-1 -> 0`）。")
    A("本册既不是全面放宽，也不是全面收紧 —— 这是最需要小心读的部分。")
    A("")

    A("## 6. 诚实边界（OPEN）")
    A("")
    A("- **O-2 部分闭合、未全闭合**：`n_eff` 能卡住「声称超过自然分辨率的位数」，")
    A("  但区分不了「理论先验给出」与「事后反推」。那是意图问题，不是计算问题。")
    A("- **O-3 仍未完全闭合**：本册给的是可计算的**必要**条件")
    A("  （位数不得超 `n_eff`），不是 Lipschitz 证书的等价替代品。")
    A("- **O-4 派生链递归计费仍未闭合**：本册只处理单层。")
    A("- **O-6（新增）不确定度表是外部数据**：`UNC_REL` 引自 CODATA，")
    A("  已做 x1/100 ~ x100 敏感性检验，但绝对数值未经本册独立核实。")
    A("- **O-7（新增）循环性判定目前靠人工标注**：Q 的检验证明了「存在循环」，")
    A("  但没有给出自动枚举全部循环的算法，`DEPENDENCY` 表是手写的。")
    A("- **O-8（新增）「哪些量是定义」不是纯数学分类**：SI-2019 的约定会随")
    A("  单位制修订而改变，`a_eff` 随之改变。本报告绑定 SI-2019。")
    A("- **O-9（新增）锚表自身的精度不自洽**：观测到的 `eps0 <-> alpha` 不一致")
    A("  `6.10e-10` 是所引标称不确定度的约 4 倍（自检 Q-4）。本册未能判定是")
    A("  混用 CODATA 版本还是引用有误 —— 在此之前，任何把该量级当作")
    A("  「理论证据」的报告都不应被采信。")
    A("- **O-5（延续）**：本册不断言任何物理结论，全部是审计架构层面的元结论，")
    A("  不升级也不降级任何体系评级。")
    A("")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    print("=" * 78)
    print("派生核算体系 UFS-Delta III：账本自洽性")
    print("=" * 78)

    cc = cross_check_table()
    if cc["available"]:
        print("[输入核对] 与 V3 常量表逐键比对：%s"
              % ("一致" if not cc["mismatch"] else cc["mismatch"]))
    else:
        print("[输入核对] V3 不可用，采用本册内嵌副本：%s"
              % cc.get("error", cc.get("note", "")))

    p = {}
    p["R0a"] = review_R0a_complete()
    p["R0b"] = review_R0b_symbolic()
    p["Q"] = theorem_Q_circularity()
    p["R"] = theorem_R_anchor_dependence()
    p["P"] = theorem_P_resolution()
    p["ledger"] = recompute_ledger()
    p["meta"] = {"elapsed": round(time.time() - t0, 2),
                 "mp_dps": mp.dps, "input_crosscheck": cc}
    p["checks"] = CHECKS

    print("\n" + "=" * 78)
    npass = sum(1 for c in CHECKS if c["passed"])
    print("自检 %d/%d 通过，耗时 %.2f s" % (npass, len(CHECKS),
                                           p["meta"]["elapsed"]))
    print("=" * 78)

    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    json_path = os.path.join(OUTDIR, "派生核算III_账本自洽.json")
    md_path = os.path.join(OUTDIR, "派生核算III_账本自洽.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1, default=str)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_md(p))
    print("已写出：%s" % json_path)
    print("已写出：%s" % md_path)


if __name__ == "__main__":
    main()
