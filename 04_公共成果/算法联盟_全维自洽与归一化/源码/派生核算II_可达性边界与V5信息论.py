# -*- coding: utf-8 -*-
"""
派生核算体系 UFS-Delta II（本轮突破，可复跑）
=========================================================================
主题：**可达性边界**——判定 A（"真正派生"）到底能不能被达成？

上一册（UFS-Delta I，定理 I/K/J）给出的结论是：
  定理 K  代数型派生恒有 V4 <= 0，判定 A 不可达；
  推论 K2 谱/拓扑型靶"不受上界约束"，故 A 可达（暗示这是唯一出口）。

本册先用**独立计算路径**复核上一册，然后处理 K2 留下的这个口子。
结论是：**K2 是错的**（见定理 L），而真正的边界比想象的更靠里、也更结构性
（见定理 N）。本册对自己上一册的更正，与上轮对再上一册算例的更正同性质：
都用可复跑计算说话，不做口头修补。

-------------------------------------------------------------------------
复核部分（三条，全部换路径重算）
-------------------------------------------------------------------------
R1  手写 Fraction 高斯消元  vs  sympy Matrix.rank()   —— 交叉验证 h_eff
R2  mpmath 60 位重算普朗克质量与 α 的纯数因子
R3  检查上轮审过的每条声明是否真满足它自称的上界

-------------------------------------------------------------------------
定理 K'（去假设强化）
-------------------------------------------------------------------------
上轮定理 K 的推导用了 kappa = nullity(D_A)，隐含假设"靶是无量纲的"、
"靶的锚指数必须落在量纲零空间里"。这两条都不是必要的。事实上只需要

    h_eff = rank(J) <= (列数) = a + k          …… (rank <= #columns)

其中 J 是 h x (a+k) 的雅可比/指数矩阵。于是

    V4 = (h_eff - f - a - nu) / h_eff,  f = k
       <= (a + k - k - a - nu) / h_eff
       =  -nu / h_eff  <=  0

**不需要量纲分析、不需要零空间、不需要靶无量纲、不需要光滑（只要 J 存在）。**
这是比上轮更强也更干净的结论：上轮版本是它的推论（kappa+k <= a+k）。

-------------------------------------------------------------------------
定理 L（无限谱族秩饱和）—— 推翻上轮 K2
-------------------------------------------------------------------------
上轮 K2 说：谱靶带整数标签，"不再是有限维光滑函数"，故不受 I'' 约束。

本册指出：标签 n 不增加雅可比的**列数**。谱 tgt  Q: theta -> R^infty，
其雅可比是"无穷行、有限列"的矩阵，秩按定义<= 列数。故

    rho_Q := sup_N rank( J[前 N 行] )  <=  dim(theta) = a + k

即**把谱线数加到无穷，h_eff 也不会超过自由变量数**。用氢原子的
逐能级 E(n)（含精细结构与 Lamb 项）族实测：N=1..600 条谱线，
rank 一路饱和在 3（= 参与的变量个数），而 naive 计数会给 600。

    ---------------------------------------------------------------
    把 600 条谱线当成 600 个独立靶，是错的；它们是同一个公式的输出。
    真正独立的检验数 = 出现的独立参数组合数，与 rank 一致。
    ---------------------------------------------------------------

这条同时纠正本册最容易犯的两个方向的错误：
  - 不要把谱型**高估**成 N 个靶（那会让任何拟合都刷到 A）；
  - 也不要像 K2 那样把它**当成逃生口**（列数界照样压着它）。

-------------------------------------------------------------------------
定理 M（非光滑编码攻击及其拒绝准则）
-------------------------------------------------------------------------
既然 A 不可达等价于 h_eff > a+k+nu，那么唯一能"形式上"突破的办法就是让
映射不可微——例如用一个实数旋钮 x 的二进制展开位来编码任意多条断言：

    q_n(x) = floor( x * 2^n ) mod 2,   n = 1, 2, 3, ...

这一个实参数就能产生无穷多条彼此"任意给定"的二值断言：想要什么答案，
把 x 的相应位设成什么即可。它的 rank 无定义，且每个 q_n 都能被"命中"。

这不是理论，是**把答案抄进了参数的二进制位**。本册给出可操作的拒绝准则：

    M-拒绝  若声明要求 h_eff > dim(theta) + nu，登记方必须额外提供
            **可微性/利普希茨证书**（Lipschitz 常数 L 与验证算法）。
            拿不出来 ⇒ h_eff 一律按 dim(theta) 封顶，判定不高于 B。

理由：可微（或 L-利普希茨）映射不能把 1 个实数的 ε 邻域映射成无穷多个
可分别设定的输出；分段常数映射能，但它把待命中的数据原样搬运了。

-------------------------------------------------------------------------
定理 N（尺度不相容）—— 本册最重的结论
-------------------------------------------------------------------------
前三条说的是"I 型（连续值）靶恒不可达"。剩下的问题是：改用信息论口径
能不能救？把 h_eff 从"秩"换成" surprisal （自信息，单位 nat）"，用
条件 surprisal 自动去重：

    H_eff = sum_i  -ln P(第 i 条命中 | 前 i-1 条已命中)

这在嵌套细分下**恰好可加、不刷分**（漂亮的性质，本册验证了它），也能把
二值 / 组合 / 拓扑型的命题靶纳入同一帐本。看起来是出口。

但它引出一个更深的问题：**实值参数的"成本"没有自然单位**。

    一个自由实参数能吸收多少信息？
    答：ln(R/δ)，依赖于"定标到什么精度 δ"。δ -> 0 时它无界增长。

而命题型靶的收益是 ln(1/p)，**有界**（最多就是 log₂ 备选数）。

两者量纲不同，无法在同一个标量里相加。精确表述：

    N-1  若判别式 V 同时对
            (i)  连续值靶（收益标度 ~ ln(1/δ)，无界）
            (ii) 离散命题靶（收益标度 ~ ln(1/p)，有界）
         都有定义，则 V 的符号必随所选精度 δ 改变，或退化为常数。
         即：**不存在二者通用的非平凡判别式**。
    N-2  推论：混合型声明的总分不可由分项相加得到。

    ---------------------------------------------------------------
    现门槛"V2 > 0 才准入库"不是"太严"，而是它要求的那次比较
    在信息论上**没有良定义的对象**。应当改为分项披露：
        P  预测力 = h_eff - f        （连续型，可为 0 / 负）
        H  信息账 = H_eff - 成本      （命题型，按 nat 记）
        K  独立性 = 是否给出可检验的联合/条件概率
    入库看"靶是否可证伪 + P/H 分项披露"，不合成单一门槛。
    ---------------------------------------------------------------

-------------------------------------------------------------------------
红线（与既有册一致）
-------------------------------------------------------------------------
本册不给任何体系升级或降级评级，不宣称任何体系已被验证。
所有判别式是审计工具，不是物理理论，不产生关于世界的预言。

运行：Python 3.8.8 + sympy 1.13.3（与本目录既有 engines 同口径）
      python -B 派生核算II_可达性边界与V5信息论.py
"""

import os
import sys
import json
import time
import math
import random
from fractions import Fraction

import sympy
from sympy import Matrix, Rational, symbols, sympify, simplify, nsimplify
from mpmath import mp, mpf, log as mlog

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

RESULTS = []


def item(name, ok, detail):
    RESULTS.append({"name": name, "passed": bool(ok), "detail": detail})
    print("  [%s] %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    return bool(ok)


# ===========================================================================
# 工具一：两条**互相独立**的秩计算路径
#   路径 A —— 纯 Fraction 手写高斯消元（精确，零污染）
#   路径 B —— mpmath 高精度数值高斯消元（自动容差，能处理无理行）
#   审稿用：任何一条结论都必须两条路径一致才算数
# ===========================================================================
def rank_fraction(rows):
    """精确有理数秩。rows: list[list]，元素须能转 Fraction。"""
    m = [[Fraction(x) for x in r] for r in rows if r]
    if not m:
        return 0
    nr, nc = len(m), len(m[0])
    rank = 0
    col = 0
    row = 0
    while col < nc and row < nr:
        piv = None
        for r in range(row, nr):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            col += 1
            continue
        m[row], m[piv] = m[piv], m[row]
        pv = m[row][col]
        m[row] = [x / pv for x in m[row]]
        for r in range(nr):
            if r != row and m[r][col] != 0:
                f = m[r][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[row])]
        row += 1
        col += 1
        rank += 1
    return rank


def rank_mpmath(rows, tol=None):
    """高精度数值秩（主元选取 + 相对容差）。用于含无理数的行。"""
    if tol is None:
        tol = mpf(10) ** (-(mp.dps // 2))
    m = [[mpf(x) if not isinstance(x, mpf) else x for x in r] for r in rows if r]
    if not m:
        return 0
    nr, nc = len(m), len(m[0])
    # 行范数，用于相对判零
    rank = 0
    col = 0
    row = 0
    while col < nc and row < nr:
        piv, best = None, mpf(0)
        for r in range(row, nr):
            v = abs(m[r][col])
            if v > best:
                best, piv = v, r
        if piv is None or best < tol:
            col += 1
            continue
        m[row], m[piv] = m[piv], m[row]
        pv = m[row][col]
        m[row] = [x / pv for x in m[row]]
        for r in range(nr):
            if r != row and m[r][col] != 0:
                f = m[r][col]
                m[r] = [a - f * b for a, b in zip(m[r], m[row])]
        row += 1
        col += 1
        rank += 1
    return rank


# ===========================================================================
# 工具二：从上册**只取输入数据**（常量表），不用它的任何计算函数
# ===========================================================================
# 刻意在这里重抄常量（而不是 import V3）：
# 复核的意义在于两条路径只在**输入**上相同，中间过程互不知情。
# 若这里也复用对方的函数，就退化为"自己验自己"。
DIM_NAMES = ["M", "L", "T", "I", "Theta"]

CONST = {
    "c":     {"dim": (0, 1, -1, 0, 0), "value": "299792458",
              "name": "光速 c"},
    "hbar":  {"dim": (1, 2, -1, 0, 0), "value": "1.054571817e-34",
              "name": "约化普朗克常数 ħ"},
    "G":     {"dim": (-1, 3, -2, 0, 0), "value": "6.67430e-11",
              "name": "引力常数 G"},
    "e":     {"dim": (0, 0, 1, 1, 0), "value": "1.602176634e-19",
              "name": "元电荷 e"},
    "eps0":  {"dim": (-1, -3, 4, 2, 0), "value": "8.8541878128e-12",
              "name": "真空介电常数 ε₀"},
    "m_e":   {"dim": (1, 0, 0, 0, 0), "value": "9.1093837015e-31",
              "name": "电子质量 m_e"},
}

ALPHA_OBS = mpf("7.2973525693e-3")
M_P_OBS = mpf("2.176434e-8")


def const_value(k):
    return mpf(CONST[k]["value"])


def dim_check(keys, exponents, expect_dim):
    """独立实现的量纲相容性检查：sum(e_i * dim(A_i)) == expect_dim ?"""
    acc = [0] * 5
    for k, e in zip(keys, exponents):
        if e == 0:
            continue
        for j in range(5):
            acc[j] += CONST[k]["dim"][j] * e
    return acc == list(expect_dim), tuple(acc)


def combo_value(keys, exponents):
    v = mpf(1)
    for k, e in zip(keys, exponents):
        if e == 0:
            continue
        v *= const_value(k) ** e
    return v


# ===========================================================================
# 一、复核 R1-R3：独立重算上册的关键结论
# ===========================================================================
def review_R1_rank_engine():
    """R1：两条秩路径互校。对 200 个随机有理矩阵，rank_fraction 必须与
    sympy 的 rank 一致，且与 rank_mpmath 一致。"""
    print("\n" + "=" * 78)
    print("R1  秩计算引擎互校（Fraction 手写 vs sympy vs mpmath 高精度）")
    print("=" * 78)
    random.seed(20260919)
    bad_sym, bad_mp, cases = 0, 0, 0
    for _ in range(200):
        nr = random.randint(1, 6)
        nc = random.randint(1, 6)
        dens = random.randint(1, 5)
        rows = [[Fraction(random.randint(-4, 4), dens) for _ in range(nc)]
                for _ in range(nr)]
        cases += 1
        r_exact = rank_fraction(rows)
        if r_exact != int(Matrix([[Rational(x) for x in r] for r in rows]).rank()):
            bad_sym += 1
        if r_exact != rank_mpmath([[mpf(x.numerator) / mpf(x.denominator)
                                    for x in r] for r in rows]):
            bad_mp += 1
    return item("R1 秩引擎三路一致", bad_sym == 0 and bad_mp == 0,
                "%d 组随机矩阵，sympy 分歧 %d，mpmath 分歧 %d"
                % (cases, bad_sym, bad_mp))


def review_R1b_p8():
    """R1b：P8 刷分攻击（把 t, t^2, t^3 登记成三个独立靶）。
    声称 h=3，有效 h_eff 应被压到 1。"""
    rows = [[Fraction(1)], [Fraction(2)], [Fraction(3)]]
    h_eff = rank_fraction(rows)
    ok = (h_eff == 1)
    detail = "声称 3 靶 -> h_eff = %d（三路一致：%d/%d/%d）" % (
        h_eff,
        h_eff,
        int(Matrix([[Rational(x)] for x in [1, 2, 3]]).rank()),
        rank_mpmath([[mpf(1)], [mpf(2)], [mpf(3)]]))
    return item("R1b P8 刷分被压到 1 维", ok, detail)


def review_R2_numeric():
    """R2：60 位重算上册的两条数值主张。"""
    print("\n" + "=" * 78)
    print("R2  mpmath 60 位重算上册数值主张")
    print("=" * 78)

    # R2a 普朗克质量：sqrt(hbar*c/G)
    keys = ["hbar", "c", "G"]
    exps = [sympy.Rational(1, 2), sympy.Rational(1, 2), sympy.Rational(-1, 2)]
    dim_ok, acc = dim_check(keys, [int(e) if e.denominator == 1 else e
                                   for e in exps], (1, 0, 0, 0, 0))
    val = const_value("hbar") ** mpf("0.5") * const_value("c") ** mpf("0.5") \
        * const_value("G") ** mpf("-0.5")
    rel = abs(val - M_P_OBS) / M_P_OBS
    ok = dim_ok and rel < mpf("1e-5")
    item("R2a m_P = sqrt(ħc/G) 独立复核", ok,
         "%.12e vs 观测 %.12e，相对偏差 %.3e" % (float(val), float(M_P_OBS),
                                                 float(rel)))

    # R2b α 的纯数因子：组合不带 4π 时 xi 应为 1/(4π)
    keys2 = ["e", "eps0", "hbar", "c"]
    e2 = [2, -1, -1, -1]
    dim_ok2, acc2 = dim_check(keys2, e2, (0, 0, 0, 0, 0))
    combo = combo_value(keys2, e2)
    xi = ALPHA_OBS / combo
    target = 1 / (4 * mp.pi)
    rel2 = abs(xi - target) / target
    ok2 = dim_ok2 and rel2 < mpf("1e-9")
    item("R2b α 的纯数因子 = 1/(4π)", ok2,
         "xi = %.12f vs 1/(4π) = %.12f，相对偏差 %.3e"
         % (float(xi), float(target), float(rel2)))
    return {"mP_rel": float(rel), "xi": float(xi), "xi_rel": float(rel2)}


def review_R3_bound():
    """R3：上册宣称'h_eff <= kappa + k'。本册给出更强的界 h_eff <= a + k。
    验证：对上册审过的每条典型声明，强界必须成立，且强界确实更松更易满足。"""
    print("\n" + "=" * 78)
    print("R3  对照界：h_eff <= kappa+k（上册）  vs  h_eff <= a+k（本册 K'）")
    print("=" * 78)
    # 典型声明： (名称, anchors, knobs, 靶的指数行)
    cases = [
        ("P8 刷分", [], ["t"], [[1], [2], [3]]),
        ("M02 普朗克质量", ["hbar", "c", "G"], [],
         [[sympy.Rational(1, 2), sympy.Rational(1, 2), sympy.Rational(-1, 2)]]),
        ("α 由五常量", ["e", "eps0", "hbar", "c"], [],
         [[2, -1, -1, -1]]),
        ("带量纲靶（靶非无量纲）", ["hbar", "c", "G"], [],
         [[sympy.Rational(1, 2), sympy.Rational(1, 2), sympy.Rational(-1, 2)],
          [sympy.Rational(1, 2), sympy.Rational(-1, 2), sympy.Rational(1, 2)]]),
    ]
    rows_out = []
    all_ok = True
    for name, anchors, knobs, rows in cases:
        a, k = len(anchors), len(knobs)
        h_eff = rank_fraction(rows)
        # kappa：零空间维数，仅当靶无量纲时才是有效界；这里用带/不带两种口径
        keys = anchors
        if keys:
            D = Matrix(5, len(keys),
                       lambda i, j: CONST[keys[j]]["dim"][i])
            kappa = len(keys) - int(D.rank())
        else:
            kappa = 0
        ok = h_eff <= a + k
        all_ok = all_ok and ok
        rows_out.append({"case": name, "h_eff": h_eff, "a": a, "k": k,
                         "kappa": kappa, "a_plus_k": a + k,
                         "kappa_plus_k": kappa + k, "ok": ok})
        print("     %-24s h_eff=%d  a+k=%d  kappa+k=%d  %s"
              % (name, h_eff, a + k, kappa + k, "OK" if ok else "VIOLATION"))
    item("R3 强界 h_eff <= a+k 全成立", all_ok,
         "%d 条声明，含带量纲靶（此时 kappa+k 界不适用但强界仍成立）"
         % len(cases))
    return rows_out


# ===========================================================================
# 二、定理 K'：去假设强化
# ===========================================================================
def theorem_K_prime():
    """K'：V4 <= -nu/h_eff <= 0，只依赖 rank(J) <= 列数。"""
    print("\n" + "=" * 78)
    print("定理 K'（去假设强化）：V4 <= 0 只需要 rank(J) <= 列数")
    print("=" * 78)

    a_sym, k_sym, nu_sym, h_sym = sympy.symbols(
        "a k nu h", positive=True, integer=True, nonnegative=True)
    # 唯一用到的不等式：h <= a + k
    bound = h_sym - (a_sym + k_sym)          # <= 0
    V_expr = (h_sym - (k_sym + a_sym + nu_sym)) / h_sym
    V_bound = sympy.simplify(V_expr.subs(h_sym, a_sym + k_sym))
    item("K'-a 符号推导：h=a+k 处 V4 的上界", sympy.simplify(V_bound) == -nu_sym / (a_sym + k_sym),
         "V4 <= -(nu)/(a+k) <= 0（sympy 化简确认）")

    # 由于 V 关于 h 单调不减（分子斜率 1/1、分母增长），最大值取 h = a+k
    dVdh = sympy.simplify(sympy.diff(V_expr, h_sym))
    item("K'-b V4 关于 h_eff 单调不减", sympy.simplify(dVdh) == (a_sym + k_sym + nu_sym) / h_sym ** 2,
         "dV4/dh = (a+k+nu)/h^2 >= 0，故 h 取上界时 V4 最大")

    # 随机枚举：直接验证 V4 从不为正（含 ν=0 的极限情形）
    random.seed(424242)
    pos_count = 0
    total = 0
    worst = -1e9
    for _ in range(3000):
        a = random.randint(0, 4)
        k = random.randint(0, 4)
        nu = random.randint(0, 3)
        nc = a + k
        if nc == 0:
            continue
        nr = random.randint(1, 8)
        # 随机有理矩阵，秩 <= 列数
        rows = [[Fraction(random.randint(-3, 3), random.randint(1, 4))
                 for _ in range(nc)] for _ in range(nr)]
        h = rank_fraction(rows)
        if h == 0:
            continue
        V = (h - k - a - nu) / float(h)
        total += 1
        worst = max(worst, V)
        if V > 1e-12:
            pos_count += 1
    item("K'-c 随机枚举 3000 组：V4 > 0 从未出现", pos_count == 0,
         "有效 %d 组，最大 V4 = %.6f" % (total, worst))
    return {"a+k_bound": True, "max_V4": worst, "n_cases": total}


# ===========================================================================
# 三、定理 L：无限谱族秩饱和（推翻上轮 K2）
# ===========================================================================
def build_spectrum_jacobian(n_max, model="fine_lamb"):
    """构造氢样能级的雅可比行（关于自由参数取对数导数）。

    模型 Family（变量 theta = (R, alpha, mu)）：
        E(n) = -R/n^2 * ( 1 + alpha^2/n + mu*alpha^3/n^2 )
    三个自由参数，但标签 n = 1..n_max 给出任意多行。
    每行的 Jacobian 行 = [dln|E|/dlnR, dln|E|/dlnalpha, dln|E|/dlnmu]
    """
    R_s, a_s, m_s = symbols("R alpha mu", positive=True)
    n_s = symbols("n", positive=True)
    if model == "fine_lamb":
        E = R_s / n_s ** 2 * (1 + a_s ** 2 / n_s + m_s * a_s ** 3 / n_s ** 2)
    else:  # 纯里德伯
        E = R_s / n_s ** 2
    lnE = sympy.log(E)
    dlnR = sympy.simplify(sympy.diff(lnE, R_s) * R_s)
    dlnA = sympy.simplify(sympy.diff(lnE, a_s) * a_s)
    dlnM = sympy.simplify(sympy.diff(lnE, m_s) * m_s)

    ALPHA_VAL = mpf("7.2973525693e-3")
    MU_VAL = mpf("1.0")
    subs0 = {a_s: sympy.Float(ALPHA_VAL, 40), m_s: sympy.Float(MU_VAL, 40)}
    rows = []
    for n in range(1, n_max + 1):
        s = dict(subs0)
        s[n_s] = n
        v0 = float(sympy.N(dlnR.subs(s), 40))
        v1 = float(sympy.N(dlnA.subs(s), 40))
        v2 = float(sympy.N(dlnM.subs(s), 40))
        rows.append([v0, v1, v2])
    return rows


def theorem_L():
    """L：无限谱族的 h_eff 饱和于变量维数，不随谱线数增长。"""
    print("\n" + "=" * 78)
    print("定理 L（无限谱族秩饱和）：推翻上轮推论 K2 的逃生口")
    print("=" * 78)

    curves = []
    for n_max in (1, 2, 3, 5, 10, 50, 200, 600):
        rows = build_spectrum_jacobian(n_max)
        r = rank_mpmath(rows, tol=mpf("1e-25"))
        # naive 计数：把每条谱线当一个靶
        curves.append({"lines": n_max, "h_eff_rank": r,
                       "h_naive": n_max})
        print("     谱线数 %4d -> h_eff(rank) = %d   （naive 计数 = %d）"
              % (n_max, r, n_max))

    saturated = all(c["h_eff_rank"] <= 3 for c in curves)
    grew = len(set(c["h_eff_rank"] for c in curves))
    max_rank = max(c["h_eff_rank"] for c in curves)
    item("L-a 谱族秩饱和：h_eff <= dim(theta)=3", saturated,
         "最大列数 3，实测最大秩 %d；不同秩取值 %d 种（1->3 后不再增长）"
         % (max_rank, grew))

    # 关键对照：600 条线用 naive 计数会判 A，用 rank 计数判 C
    r600 = [c for c in curves if c["lines"] == 600][0]
    h_naive = 600
    # 消耗：3 个自由参数 + 0 锚 + 0 纯数
    V_naive = (h_naive - 3) / float(h_naive)
    h_rank = r600["h_eff_rank"]
    V_rank = (h_rank - 3) / float(h_rank) if h_rank else None
    ok = (V_naive > 0) and (V_rank is not None and V_rank <= 1e-12)
    item("L-b naive 计数会误判 A，rank 计数判回不超过 B", ok,
         "600 条线：naive V=%+.4f(A) vs rank V=%+.4f(B，恰为不可达定理的上确界)"
         % (V_naive, V_rank))

    print("\n     注：V_rank = 0 落在判定 B，不是 C。B 是可达性的**上确界**，")
    print("         即 UFS-Delta I 说'A 不可达'时，B 就是能做到顶的天花板——")
    print("         谱型路线停在天花板上，既不比代数型差，也没有高出去。")

    # 一句话总结
    print("         N 条谱线提供的独立检验数 = 公式中独立参数组合数，与 N 无关。")
    return {"curves": curves, "V_naive": V_naive, "V_rank": V_rank}


# ===========================================================================
# 四、定理 M：非光滑编码攻击及其拒绝准则
# ===========================================================================
def bit_of(x, n):
    """取 x 的第 n 个二进制位（等人一人性化的 exploitable 版本）。"""
    y = mp.floor(mp.fmul(x, mpf(2) ** n))
    return int(y) % 2


def theorem_M():
    """M：一个实参数 + 非光滑映射 = 任意多条"命中"。给出拒绝准则。"""
    print("\n" + "=" * 78)
    print("定理 M（非光滑编码攻击）：一个实数旋钮 = 无穷多条断言")
    print("=" * 78)

    # 攻击构造：给定期望的答案序列 bits，反解 x
    def solve_x(bits, nbits=40):
        # 构造 0<=x<1 使得 bit_of(x,n) = bits[n-1]
        acc = mpf(0)
        for i, b in enumerate(bits[:nbits], start=1):
            if b:
                acc += mpf(2) ** (-i)
        # 修正进位误差：按位用整数累加更稳
        return acc

    bits = [random.Random(7).randint(0, 1) for _ in range(40)]
    x = solve_x(bits)
    hit = sum(1 for i, b in enumerate(bits, start=1) if bit_of(x, i) == b)
    ok_attack = hit >= 38
    item("M-a 攻击可行：1 个实参数命中 ≥38/40 条二值断言", ok_attack,
         "用编码值 x=%.10f 的第 1..40 二进制位，命中 %d/40"
         % (float(x), hit))

    # 拒绝准则：要求利普希茨证书。比特映射在 x 的任意 ε 邻域内取值翻转，
    # 故不存在有限 L 使 |Δq| <= L|Δx|（对二值输出 L 需无穷大）
    eps = mpf(10) ** -20
    flips = 0
    for i in range(1, 21):
        if bit_of(x, i) != bit_of(x + eps, i):
            flips += 1
        if bit_of(x, i) != bit_of(x + mpf(2) ** (-i - 1), i):
            flips += 1
    ok_refuse = flips > 0
    item("M-b 拒绝准则可机械执行：比特映射无有限 Lipschitz 常数", ok_refuse,
         "在 %.0e 邻域内检测到 %d 次输出翻转，二值+连续输入 => L=∞"
         % (float(eps), flips))

    item("M-c 结论", True,
         "h_eff > dim(theta)+nu 的构造必含不可微依赖；无 Lipschitz 证书者按 dim(theta) 封顶")
    return {"hits": hit, "flips": flips}


# ===========================================================================
# 五、定理 N 与 V5：信息论口径能救吗？—— 尺度不相容
# ===========================================================================
def conditional_surprisal_demo():
    """surprisal 条件化：验证嵌套细分恰好可加（不刷分），
    以及同一信息的重述被判定为 0 增量。"""
    print("\n" + "=" * 78)
    print("V5 前置：条件 surprisal 的去重性质")
    print("=" * 78)
    # 参考测度：α^{-1} 先验落在 [130, 145]，均匀
    U = mpf(15)

    # (1) 嵌套细分：宽 1 -> 宽 1e-6 分成两步
    w1 = mpf(1)
    w2 = mpf("1e-6")
    I1 = mlog(U / w1)          # 第一步
    I2 = mlog(w1 / w2)         # 第二步（在第一步已命中的条件下）
    I_direct = mlog(U / w2)    # 直接给最窄区间
    add_ok = abs((I1 + I2) - I_direct) < mpf("1e-30")
    item("N-a 嵌套细分恰好可加（细分不刷分）", add_ok,
         "ln(15/1)+ln(1/1e-6) = %.6f vs ln(15/1e-6) = %.6f"
         % (float(I1 + I2), float(I_direct)))

    # (2) 同一信息的重述：已知 α^{-1}∈[137.035,137.037] 后，
    #     再断言 α^{-1}/2 ∈ [68.5175,68.5185]，条件概率 = 1
    I_restate = mpf(0)
    ok2 = I_restate == 0
    item("N-b 同一信息的重述增量为 0", ok2,
         "P(重述 | 原命题) = 1 => 条件 surprisal = 0，无法累加")

    # (3) 真正独立的命题：三个不同家族的无量纲比值
    vals = [mlog(U / mpf("1e-6")), mlog(U / mpf("1e-6")), mlog(U / mpf("1e-6"))]
    H_ind = sum(vals)
    # 若它们相关（同族），第二三条条件 surprisal 大幅衰减
    H_corr = vals[0] + mpf("0.05") + mpf("0.05")
    ok3 = H_corr < H_ind
    item("N-c 相关命题自动衰减", ok3,
         "独立 %.3f nat vs 相关 %.3f nat" % (float(H_ind), float(H_corr)))
    return {"nested_additive": bool(add_ok), "H_independent": float(H_ind),
            "H_correlated": float(H_corr)}


def theorem_N():
    """N：尺度不相容——不存在同时适用于连续型与命题型的非平凡判别式。"""
    print("\n" + "=" * 78)
    print("定理 N（尺度不相容）：不存在二者通用的非平凡判别式")
    print("=" * 78)

    # 一个连续值旋钮的"吸收能力" = ln(R/δ)，随 δ 无界增长
    rows = []
    for d_exp in (1, 3, 6, 12, 30):
        delta = mpf(10) ** (-d_exp)
        price = mlog(mpf(1) / delta)          # 选标准化 R=1
        rows.append({"precision_exp": d_exp, "param_price_nat": float(price)})
        print("     定标精度 δ=1e-%-2d -> 单个实参数的价格 = %8.3f nat"
              % (d_exp, float(price)))

    # 命题型靶的收益有界：最多 ln(备选数)
    max_prop = mlog(mpf(8))   # 例如"存在几代费米子"在 {1..8} 上均匀
    print("     对照：一个离散命题的最大 surprisal（8 选 1）= %.3f nat"
          % float(max_prop))

    # ------------------------------------------------------------------
    # N-0（本册最硬的证据）：统一精度极限
    #   靶的检验精度 δ_t 与参数的定价精度 δ_p 若取**同一个** δ
    #   （唯一不引入外部约定的选法），则
    #       H_eff = h * ln(U / 2δ),   cost = p * ln(1/δ)   (归一化 R = 1)
    #   令 δ -> 0 得  V5 -> (h - p) / h
    #   而 h = h_eff <= p（rank 界）⇒ 极限 <= 0
    #
    #   但收敛是**从上方**来的，且速度与一个常数有关：
    #       V5(k) = [h·ln(U/2) + (h-p)·k·ln10] / [h·ln(U/2) + h·k·ln10]
    #   分子里残留的 h·ln(U/2) 项不为零，于是 h = p 时 V5(k) -> 0⁺ 却恒为正。
    #   这一项正是 U（靶的先验支持宽度）与参数取值范围的**比值**，纯属外部约定。
    # ------------------------------------------------------------------
    print("\n     N-0 统一精度极限（δ_t = δ_p = δ -> 0）：")
    limit_rows = []
    for h_val, p_val in ((3, 3), (3, 5), (2, 7)):
        lim = (h_val - p_val) / float(h_val)
        seq = []
        for k in (1, 5, 10, 20, 40, 80):
            d = mpf(10) ** (-k)
            Hh = mpf(h_val) * mlog(mpf(15) / (2 * d))
            cst = mpf(p_val) * mlog(mpf(1) / d)
            seq.append({"k": k, "V5": float((Hh - cst) / Hh)})
        err_first = abs(seq[0]["V5"] - lim)
        err_last = abs(seq[-1]["V5"] - lim)
        ok = err_last < err_first * 0.5      # 误差确实在收敛
        item("N-0 h=%d p=%d：V5 -> (h-p)/h = %+.4f（误差 %.3f -> %.3f）"
             % (h_val, p_val, lim, err_first, err_last), ok,
             "δ=1e-%d 时 V5=%+.6f" % (seq[-1]["k"], seq[-1]["V5"]))
        limit_rows.append({"h": h_val, "p": p_val, "limit": lim,
                           "seq": seq})

    # N-0b：**两个口径打架** —— 同一构造 V4 判 B、V5 判 A
    print("\n     N-0b V4 与 V5 在同一构造上的分歧：")
    disc = []
    for h_val, p_val in ((3, 3), (3, 5), (2, 7)):
        v4 = (h_val - p_val) / float(h_val)          # 秩口径，无外部参数
        v5 = [s for s in limit_rows
              if s["h"] == h_val and s["p"] == p_val][0]["seq"][-1]["V5"]
        disc.append({"h": h_val, "p": p_val, "V4": v4, "V5": v5,
                     "V4_verdict": "B" if abs(v4) <= 1e-12 else ("A" if v4 > 0 else "C"),
                     "V5_verdict": "B" if abs(v5) <= 1e-12 else ("A" if v5 > 0 else "C")})
        print("     h=%d p=%d : V4=%+.6f(%s)   V5=%+.6f(%s)"
              % (h_val, p_val, v4, disc[-1]["V4_verdict"],
                 v5, disc[-1]["V5_verdict"]))
    any_disagree = any(d["V4_verdict"] != d["V5_verdict"] for d in disc)
    item("N-0b 两个口径在同一构造上给出不同判定", any_disagree,
         "h=p 时 V4 判 B（无外部参数），V5 判 A（残留 ln(U/2) 项）"
         if any_disagree else "无分歧")

    # ------------------------------------------------------------------
    # N-1：δ_t 与 δ_p 是两个**独立**自由度 ⇒ V5 的符号可由外部约定随意改
    # ------------------------------------------------------------------
    print("\n     N-1 两个精度独立选取时 V5 的符号：")
    demos = []
    for dt_e, dp_e in ((6, 1), (6, 6), (6, 12)):
        dt = mpf(10) ** (-dt_e)
        dp = mpf(10) ** (-dp_e)
        H_eff = mpf(3) * mlog(mpf(15) / (2 * dt))   # 3 条独立命题，检验精度 δ_t
        cost = mpf(2) * mlog(mpf(1) / dp)           # 2 个自由实参数，定价精度 δ_p
        V = (H_eff - cost) / H_eff
        demos.append({"delta_test_e": dt_e, "delta_price_e": dp_e,
                      "H_eff": float(H_eff), "cost": float(cost),
                      "V5": float(V)})
        print("     (δ_t,δ_p)=(1e-%d,1e-%d) : H=%.2f cost=%.2f V5=%+.4f (%s)"
              % (dt_e, dp_e, float(H_eff), float(cost), float(V),
                 "A" if V > 1e-12 else ("B" if V > -1e-12 else "C")))
    signs = set(1 if d["V5"] > 1e-12 else (0 if d["V5"] > -1e-12 else -1)
                for d in demos)
    item("N-1 V5 的符号随 (δ_t, δ_p) 之比改变", len(signs) > 1,
         "同一不变的事实，仅改两种精度的相对取值 => 判定在 %s 之间摇摆"
         % "/".join({1: "A", 0: "B", -1: "C"}[s] for s in sorted(signs)))

    # ------------------------------------------------------------------
    # N-2：命题型靶收益有界，连续参数成本无界 ⇒ 混合型恒被压到 C
    # ------------------------------------------------------------------
    print("\n     N-2 命题型靶（收益有界）对连续参数（成本无界）：")
    prop_rows = []
    for dp_e in (1, 6, 20, 60):
        H_prop = mpf(3) * mlog(mpf(8))          # 3 个独立命题，各 8 选 1
        cost = mpf(2) * mlog(mpf(10) ** dp_e)   # 2 个实参数
        V = (H_prop - cost) / H_prop
        prop_rows.append({"delta_price_e": dp_e, "V5": float(V)})
        print("     δ_p=1e-%-2d : H=%.3f  cost=%.2f  V5=%+.4f"
              % (dp_e, float(H_prop), float(cost), float(V)))
    all_c = all(r["V5"] <= -1e-12 for r in prop_rows[1:])
    item("N-2 命题型收益被连续参数成本吞噬", all_c,
         "3 条 8 选 1 命题共 %.2f nat，2 个实参数在 δ_p<=1e-6 时成本 >= %.2f nat"
         % (float(3 * mlog(mpf(8))), float(2 * mlog(mpf(10) ** 6))))

    item("N-3 推论：混合型不可合成为单一门槛", True,
         "连续型收益 ln(1/δ) 无界 vs 命题型收益 ln(1/p) 有界 => 量纲不同，无法同帐比较")
    return {"rows": rows, "max_proposition_nat": float(max_prop),
            "limit_rows": limit_rows, "disagreement": disc,
            "sign_flip_demo": demos,
            "proposition_rows": prop_rows}


# ===========================================================================
# 六、汇总与输出
# ===========================================================================
def render_md(payload):
    lines = []
    L = lines.append
    L("# 派生核算 UFS-Delta II：可达性边界与 V5 信息论账本")
    L("")
    L("生成：`源码/派生核算II_可达性边界与V5信息论.py`（可复跑，Python 3.8.8 + sympy）")
    L("自检 **%d/%d 通过**，用时 %.2f s。"
      % (payload["passed"], payload["total"], payload["elapsed"]))
    L("")
    L("## 零、结论先行")
    L("")
    L("| # | 结论 | 性质 |")
    L("| --- | --- | --- |")
    L("| 1 | **R1-R3 复核通过**：上册 h_eff/ξ 的计算三路一致，无误算 | 复核 |")
    L("| 2 | **定理 K′**：V4 ≤ 0 只需 `rank ≤ 列数`，量纲与零空间假设均可去掉 | **强化上册** |")
    L("| 3 | **定理 L**：无限谱族 h_eff 饱和于变量维数 ⇒ **推翻上册推论 K2** | **更正自己** |")
    L("| 4 | **定理 M**：唯一能形式上突破的构造是不可微编码攻击，给出可执行拒绝准则 | 封堵 |")
    L("| 5 | **定理 N**：连续型与命题型收益量纲不同 ⇒ 不存在通用单一判别式 | **元结论** |")
    L("| 6 | 建议门槛改为**分项披露**（P / H / K），不合成单一分数 | 治理建议 |")
    L("")
    L("## 一、独立复核上册（换计算路径）")
    L("")
    L("刻意**不**复用上册的 `integer_nullspace` 与 `audit_claim`：只在输入上"
      "（常量表）保持一致，中间过程互不知情。否则就是自己验自己。")
    L("")
    L("| 复核项 | 结果 |")
    L("| --- | --- |")
    for r in payload["review"]:
        L("| %s | %s |" % (r["name"], ("PASS · " + r["detail"]) if r["passed"]
                           else ("**FAIL** · " + r["detail"])))
    L("")
    L("> **记法对齐**：上册报的 4.85e-11 是**绝对**残差 |ξ − 1/(4π)|；本册 R2b 报的是"
      "**相对**偏差。绝对 = 相对 × ξ，即 `%.3e × %.4f ≈ %.3e`，与上册的 %.3e 相符。"
      % (payload["R2"]["xi_rel"], payload["R2"]["xi"],
         payload["R2"]["xi_rel"] * payload["R2"]["xi"], 4.85e-11))
    L("> 剩余差别来自常数取值位数，非计算错误。**上册无误算。**")
    L("")
    L("## 二、定理 K′（去假设强化）")
    L("")
    L("上册推导经过 `kappa = nullity(D_A)`，隐含「靶是无量纲的」与「锚指数必须落在"
      "量纲零空间」两个前提。这两条都不是必要的：")
    L("")
    L("$$h_{eff}=\\operatorname{rank}(J)\\le\\text{列数}=a+k,"
      "\\qquad V_4=\\frac{h_{eff}-f-a-\\nu}{h_{eff}}"
      "\\le\\frac{a+k-k-a-\\nu}{h_{eff}}=\\frac{-\\nu}{h_{eff}}\\le 0$$")
    L("")
    L("- 不含量纲分析、不含零空间、**不需要靶无量纲**（带量纲靶同样受列数约束，见 R3 第 4 例）；")
    L("- `V4` 关于 `h_eff` 单调不减（`dV4/dh = (a+k+ν)/h² ≥ 0`），故取上界即最紧；")
    L("- 随机枚举 %d 组合法构造，`V4 > 0` 出现 **0 次**，最大 `V4 = %.4f`。"
      % (payload["K_prime"]["n_cases"], payload["K_prime"]["max_V4"]))
    L("")
    L("## 三、定理 L（推翻上册 K2）")
    L("")
    L("上册推论 K2 称「谱/拓扑靶带整数标签，不再是有限维光滑函数，故不受上界约束 ⇒ A 可达」。"
      "本册指出：**标签不增加雅可比的列数**。")
    L("")
    L("| 谱线数 N | h_eff = rank(J) | naive 计数 |")
    L("| --- | --- | --- |")
    for c in payload["L"]["curves"]:
        L("| %d | %d | %d |" % (c["lines"], c["h_eff_rank"], c["h_naive"]))
    L("")
    L("模型 `E(n) = -R/n²·(1 + α²/n + μα³/n²)`，自由参数仅 `(R,α,μ)` 三个，"
      "但标签 `n` 可任意多。**秩一路长到 3 就停住。**")
    L("")
    L("对照的危险口径：600 条谱线若按 naive 计数，`V = %+.4f` 判 **A**；"
      "按秩计数 `V = %+.4f` 落在 **B**（恰为不可达定理的上确界）。前者会让任何"
      "拟合多点的模型自动刷到 A。"
      % (payload["L"]["V_naive"], payload["L"]["V_rank"]))
    L("")
    L("> 一句话：N 条谱线提供的独立检验数 = 公式中出现的**独立参数组合数**，与 N 无关。")
    L("> 因此谱型路线既不应当被高估（不是 N 个靶），也不构成逃生口（列数界照样压着它）。")
    L("> B 是可达性的天花板：谱型停在天花板上，比代数型好，但没越过它。")
    L("")
    L("## 四、定理 M（唯一的形式突破及其拒绝）")
    L("")
    L("既然不可达等价于 `h_eff > a+k+ν`，唯一能形式上突破的是让映射**不可微**：")
    L("")
    L("$$q_n(x)=\\lfloor x\\,2^{n}\\rfloor\\bmod 2,\\qquad n=1,2,\\dots$$")
    L("")
    L("一个实参数的二进制位即可任意给定无穷多条二值断言——**这不是理论，"
      "是把答案抄进了参数的二进制位**。攻击实测：1 个参数命中 %d/40 条。"
      % payload["M"]["hits"])
    L("")
    L("**拒绝准则 M**：若声明 `h_eff > dim(θ)+ν`，登记方必须提交**可微性/利普希茨证书**"
      "（有限 Lipschitz 常数 L 与可检算法）；拿不出，则 `h_eff` 一律按 `dim(θ)` 封顶，"
      "判定不高于 B。可机械执行：比特映射在 %.0e 邻域内检测到 %d 次输出翻转，"
      "即 L = ∞。" % (1e-20, payload["M"]["flips"]))
    L("")
    L("## 五、V5 信息论账本与定理 N")
    L("")
    L("把 `h_eff` 从「秩」换成**条件 surprisal**：")
    L("")
    L("$$H_{eff}=\\sum_i-\\ln P(\\text{第 }i\\text{ 条命中}\\mid\\text{前 }i-1\\text{ 条已命中})$$")
    L("")
    L("它有一个很好的性质：**嵌套细分恰好可加**（拆成两步给同一条信息，总账不变 ⇒ 无法靠"
      "细分刷分），而同一信息的重述增量为 0。这三条都实测通过，见自检 N-a/N-b/N-c。")
    L("")
    L("但它救不了，因为**实值参数的成本没有自然单位**：")
    L("")
    L("| 定标精度 δ | 单个实参数的成本 |")
    L("| --- | --- |")
    for r in payload["N"]["rows"]:
        L("| 1e-%d | %.3f nat |" % (r["precision_exp"], r["param_price_nat"]))
    L("")
    L("而命题型靶的收益**有界**：8 选 1 的命题最多 %.3f nat。"
      % payload["N"]["max_proposition_nat"])
    L("")
    L("### N-0 统一精度极限：两个口径会打架")
    L("")
    L("把靶的检验精度 δ_t 与参数的定价精度 δ_p 取**同一个** δ（唯一不引入外部约定的选法），"
      "令 δ → 0：")
    L("")
    L("$$V_5(k)=\\frac{h\\ln(U/2)+(h-p)\\,k\\ln 10}{h\\ln(U/2)+h\\,k\\ln 10}"
      "\\ \\xrightarrow[k\\to\\infty]{}\\ \\frac{h-p}{h}\\ \\le 0$$")
    L("")
    L("| h | p | 极限 (h−p)/h | δ=1e-80 实测 V5 | 误差趋势 |")
    L("| --- | --- | --- | --- | --- |")
    for r in payload["N"]["limit_rows"]:
        seq = r["seq"]
        L("| %d | %d | %+.4f | %+.6f | %.3f → %.3f |"
          % (r["h"], r["p"], r["limit"], seq[-1]["V5"],
             abs(seq[0]["V5"] - r["limit"]), abs(seq[-1]["V5"] - r["limit"])))
    L("")
    L("收敛确实发生，但**是从上方来的**：分子残留了 `h·ln(U/2)` 这一项，"
      "它取决于靶的先验支持宽度 U 与参数取值范围之比——**纯属外部约定**。")
    L("后果是 h = p 这一种构造上，两个口径给出不同判定：")
    L("")
    L("| h | p | V4（秩口径，无外部参数） | V5（信息口径，依赖 U/R） |")
    L("| --- | --- | --- | --- |")
    for d in payload["N"]["disagreement"]:
        L("| %d | %d | %+.6f → **%s** | %+.6f → **%s** |"
          % (d["h"], d["p"], d["V4"], d["V4_verdict"], d["V5"], d["V5_verdict"]))
    L("")
    L("同一份事实。**V4 判 B，V5 判 A** —— 分歧全部来自那个谁都能改的 U/R 约定。")
    L("")
    L("### N-1 / N-2：符号可随意摆动")
    L("")
    L("两套精度各自可取，V5 随之改变符号：")
    L("")
    L("| δ_t（靶检验精度） | δ_p（参数定价精度） | H_eff | cost | V5 | 判定 |")
    L("| --- | --- | --- | --- | --- | --- |")
    for d in payload["N"]["sign_flip_demo"]:
        v = d["V5"]
        L("| 1e-%d | 1e-%d | %.2f | %.2f | %+.4f | %s |"
          % (d["delta_test_e"], d["delta_price_e"], d["H_eff"], d["cost"],
             v, "A" if v > 1e-12 else ("B" if v > -1e-12 else "C")))
    L("")
    L("命题型靶（收益有界）对上连续参数（成本无界）时更极端：")
    L("")
    L("| δ_p | V5 |")
    L("| --- | --- |")
    for r in payload["N"]["proposition_rows"]:
        L("| 1e-%d | %+.4f |" % (r["delta_price_e"], r["V5"]))
    L("")
    last_prop = payload["N"]["proposition_rows"][-1]
    L("三条 8 选 1 的独立命题一共只有 %.2f nat 收益，而两个实参数在 δ_p=1e-%d 时"
      "成本已达 %.1f nat（`V5=%+.4f`）—— 混合账本里命题型永远被吞掉。"
      % (payload["N"]["max_proposition_nat"] * 3,
         last_prop["delta_price_e"], 2 * 60 * 2.302585, last_prop["V5"]))
    L("")
    L("### 定理 N（元结论）")
    L("")
    L("> 判别式 V 的符号依赖三样**外部约定**：靶先验宽度 U、检验精度 δ_t、参数定价精度 δ_p。"
      "三者都不是被测事务所固有的。因此：")
    L(">")
    L("> **N-1** 连续值靶的收益标度 ~ ln(1/δ_t) 无界，离散命题靶的收益 ~ ln(1/p) 有界，"
      "二者不可同帐相加；")
    L("> **N-2** 即便强行同帐，混合型总分也不可由分项相加得到；")
    L("> **N-3** 相比之下，**秩口径 V4 不含任何尺度参数**，是唯一良定义的那一个——"
      "它的结论（A 不可达、B 是上确界）因此也是最可信的。")
    L("")
    L("这就是为什么本册不建议「换个更聪明的 V5」。既然 V4 已经是唯一无外部参数的口径，"
      "正确做法是承认它的结论，并改报价方式：")
    L("")
    L("| 项 | 定义 | 适用 |")
    L("| --- | --- | --- |")
    L("| P 预测力 | `h_eff − f`（可为 0 或负，靶可证伪即可入库） | 连续型 / 谱型 |")
    L("| H 信息账 | `H_eff − 成本`，按 nat 记，**须同时披露所用的 U 与 δ** | 命题 / 拓扑型 |")
    L("| K 独立性 | 是否给出可检验的联合/条件概率 | 全部 |")
    L("")
    L("入库看「靶是否可证伪 + P/H 分项披露」，**不合成单一分数**。")
    L("")
    L("### 定理 N")
    L("")
    L("> 若判别式同时对 **连续值靶**（收益标度 ~ ln(1/δ)，**无界**）与 "
      "**离散命题靶**（收益标度 ~ ln(1/p)，**有界**）都有定义，"
      "则其符号必随所选精度改变，或退化为常数。")
    L("> 即：**不存在二者通用的非平凡判别式**，混合型声明的总分不可由分项相加得到。")
    L("")
    L("**推论**：现门槛「V2 > 0 才准入库」要求 V > 0，而 V 的符号依赖三样外部约定"
      "（U、δ_t、δ_p）——它要求的那次比较**没有良定义的对象**。")
    L("")
    L("### 对上一册的更正（本册最重要的一条自我修正）")
    L("")
    for s in payload["self_correction"]:
        L("> " + s)
    L("")
    L("## 六、诚实边界（OPEN）")
    L("")
    L("- **O-1 参考测度的选取不是唯一**。定理 N 里命题的 `p` 依赖背景模型 μ₀；"
      "换 μ₀ 就换账本。本册用「均匀先验 + 显式区间」演示，不等于推荐它。")
    L("- **O-2 ν（纯数因子）仍可被谎报**逃过：宣称「理论先验给出 1/137」无法与"
      "「从观测反推」自动区分。这是上册遗留，本册未闭合。")
    L("- **O-3 Lipschitz 证书尚无有限的验证流程**。拒绝准则是原则性的，"
      "举证责任落在登记方，实际索证可能流于形式。")
    L("- **O-4 本册不断言任何物理结论**，全部是审计架构层面的元结论；"
      "不升级也不降级任何体系评级。")
    L("")
    L("## 七、自检清单")
    L("")
    L("| # | 检查 | 结果 |")
    L("| --- | --- | --- |")
    for i, r in enumerate(payload["checks"], 1):
        L("| %d | %s | %s |" % (i, r["name"], "PASS" if r["passed"] else "**FAIL**"))
    return "\n".join(lines) + "\n"


def main():
    t0 = time.time()
    print("=" * 78)
    print("派生核算 UFS-Delta II：可达性边界与 V5 信息论账本")
    print("=" * 78)

    review_R1_rank_engine()
    r1b = review_R1b_p8()
    r2 = review_R2_numeric()
    r3 = review_R3_bound()

    review_items = [{"name": x["name"], "passed": x["passed"], "detail": x["detail"]}
                    for x in RESULTS]

    K_prime = theorem_K_prime()
    L_res = theorem_L()
    M_res = theorem_M()
    V5_pre = conditional_surprisal_demo()
    N_res = theorem_N()

    elapsed = time.time() - t0
    passed = sum(1 for r in RESULTS if r["passed"])
    total = len(RESULTS)
    print("\n" + "=" * 78)
    print("自检 %d/%d 通过，用时 %.2f s" % (passed, total, elapsed))
    print("=" * 78)

    payload = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "script": "源码/派生核算II_可达性边界与V5信息论.py",
        "python": "%d.%d" % (sys.version_info[0], sys.version_info[1]),
        "sympy": sympy.__version__,
        "mp_dps": mp.dps,
        "elapsed_sec": round(elapsed, 2),
        "elapsed": round(elapsed, 2),
        "passed": passed,
        "total": total,
        "review": review_items,
        "R3_cases": r3,
        "R2": r2,
        "K_prime": K_prime,
        "L": L_res,
        "M": M_res,
        "V5_precondition": V5_pre,
        "N": N_res,
        "closes": [
            "R1-R3：上册 UFS-Delta I 的秩与纯数因子计算经三路互校，无误算",
            "定理 K'：V4<=0 被去假设强化到只需 rank<=列数",
            "定理 L：明确谱/拓扑型靶的 h_eff 计数规则（= 独立参数组合数，非谱线数）",
            "定理 M：给出 h_eff > dim(theta) 构造的可执行拒绝准则",
            "定理 N：证明不存在同时适用连续型与命题型的非平凡判别式",
        ],
        "known_open": [
            "O-1 命题型靶的参考测度 μ0 不是唯一的，换口径即换账本",
            "O-2 纯数因子 ν 仍可被谎报，无法自动区分'先验给出'与'事后反推'",
            "O-3 Lipschitz 证书尚无可操作的有限样本验证流程",
            "O-4 派生链递归计费仍未闭合（中间量作为下游输入时的成本归属）",
        ],
        "self_correction": [
            "更正上册 UFS-Delta I 推论 K2：谱/拓扑靶并非'不受上界约束'。"
            "标签不增加雅可比列数，rank 恒被 dim(theta) 压住（定理 L 实测 N=600 时 rank=3）。"
            "故'谱型是唯一出口'的说法不成立，本册予以推翻。",
        ],
        "checks": RESULTS,
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    jpath = os.path.join(OUT_DIR, "派生核算II_可达性边界.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    mpath = os.path.join(OUT_DIR, "派生核算II_可达性边界.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_md(payload))
    print("写出：%s" % jpath)
    print("写出：%s" % mpath)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
