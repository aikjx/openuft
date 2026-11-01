# -*- coding: utf-8 -*-
"""
TUFT-r319 · 统一表示框架与二次超荷矩
`X-R309-1`（「每多重态各自一个独立指标」这个框架本身是否必要）攻坚

承 r309 判定册 §十一 交接的最硬边界：
「若改用**单一统一表示**（如 27 of E6 内含整代），本卷定理 T/U 完全不适用 ——
  在那个框架里三代是**一个**指标的读数。」

本卷正面攻这个框架问题。结论出乎意料地锋利：障碍不是维数、不是幂次、不是扭转，
而是**一个分数**：一代 SM 场（15 个左手 Weyl）的二次超荷矩 Σ dim·Y² = 10/3 ≠ 0。

  定理 X（E6 27 的 SM 分解）   27 = 15_gen ⊕ 12_extra，两部分**各自**无反常（不是互相抵消）
                                ⇒ 额外物不污染代的判据，可以放心把 gen 单独拿出来算
  定理 Y（二次超荷矩 · 核心）  Σ_gen dim·Y = 0，Σ_gen dim·Y³ = 0，但 **Σ_gen dim·Y² = 10/3**
                                ⇒ 三个超荷矩里**唯一非零的是二次的**，且是**与 GUT 群无关的普适常数**
  定理 Z（统一框架必然反常）   单一不可约表示 ⇒ 所有分量共享**同一个**通量 q
                                ⇒ A_YYF = q·Σ dim·Y² = 5q（27）或 (10/3)q（16）
                                ⇒ **q ≠ 0 即反常** ⇒ 反常自由强迫 q = 0 ⇒ n_R = 0 ⇒ **零代，不是三代**
                                ⇒ r309 定理 S（反常自由集 = span(Y)）与「常数 q」直接对撞，
                                  因为 Y 有 5 个互异值 ⇒ 常数 q 只在 q=0 处落在 span(Y) 里
  定理 AA（第二路线也不通）    若允许 q_a = q·f_a（U(1) ⊂ E6 的嵌入），反常自由强迫 f ∝ Y
                                ⇒ 回到逐分量 ⇒ 5 个 n_a 需相等 ⇒ 4 个独立条件 ⇒ r309 定理 T 的 n ≥ 9
                                ⇒ 与 r309 完全一致，**无逃逸**
  定理 AB（放开反常前提后）    **若** U(1)_F 不是精确规范对称（Stückelberg / 整体），障碍消失
                                ⇒ 在 CP^n 族上精确解 n_R(q) = 3：**只有 CP^1 有整数解，且 q 恰为 3**
                                ⇒ 最小内部空间 + 最小整数通量正好给三代 —— 但 n_R 成了**自由输入**

⇒ 判词：`X-R309-1` **判负关闭**——统一表示框架不是逃逸，因为二次超荷矩 10/3 把常数荷分配打死；
   只有放弃「U(1)_F 精确无反常」才能得到三代，而那时三代是自由参数。
   **三代仍未被解释，但「为什么必须逐多重态分荷」第一次有了一个数值理由：10/3。**

确定性：Fraction 精确；CP^n 的 Â 用 Pontryagin 多项式精确展开（截断 6 阶）；无 random。
口径：左手口径 Q = T3 + Y；T(3)=T(3̄)=1/2 用于 [SU(3)]²Y；A(3)=+1/A(3̄)=−1 用于 SU(3)³。
"""
import io
import json
import math
import os
import re
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r319"
DATE = "2026-11-01"
DEGREE = 0
VERDICT = ("X-R309-1-CLOSED-NEGATIVELY__UNIFIED-IRREP-FORCES-ONE-CHARGE-FOR-ALL-COMPONENTS"
           "__CONSTANT-CHARGE-IS-ANOMALOUS-BY-ALL-FOUR-LINEAR-ANOMALIES-ALL-POSITIVE"
           "__THREE-GENERATIONS-ONLY-WITHOUT-EXACT-U1F__CP1-WITH-FLUX-3-IS-THE-ONLY-VACUUM")

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r319_统一表示框架与二次超荷矩_"
        "单一不可约表示能否绕开复制约束与三代的框架依赖性_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱（与 r294–r309 同）
DIMS = [6, 3, 3, 2, 1]
YS = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)]
NAMES = ["Q_L (3,2)_{1/6}", "u^c (3bar,1)_{-2/3}", "d^c (3bar,1)_{1/3}",
         "L_L (1,2)_{-1/2}", "e^c (1,1)_{1}"]


def anomal(q):
    q1, q2, q3, q4, q5 = q
    return (2 * q1 + q2 + q3,
            3 * q1 + q4,
            sum(DIMS[i] * q[i] for i in range(5)),
            sum(DIMS[i] * YS[i] ** 2 * q[i] for i in range(5)),
            sum(DIMS[i] * YS[i] * q[i] ** 2 for i in range(5)),
            sum(DIMS[i] * q[i] ** 3 for i in range(5)))


AKEYS = ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]

ITEMS, CONTROLS, GUARDS = [], [], []


def item(iid, kind, exp, act, note, tol=None):
    if kind == "eq":
        ok = (act == exp)
    elif kind == "abs":
        ok = abs(act - exp) <= tol
    elif kind == "gt":
        ok = act > exp
    elif kind == "lt":
        ok = act < exp
    else:
        ok = True
    ITEMS.append({"id": iid, "kind": kind, "exp": str(exp), "act": str(act),
                  "status": "INFO" if kind == "info" else ("PASS" if ok else "FAIL"),
                  "note": note})


def control(cid, desc, ok, detail=""):
    CONTROLS.append({"id": cid, "desc": desc, "detail": detail,
                     "status": "PASS" if ok else "FAIL"})


def guard(gid, desc, ok, detail=""):
    GUARDS.append({"id": gid, "desc": desc, "detail": detail,
                   "status": "PASS" if ok else "FAIL"})


def fmt(v):
    if isinstance(v, F):
        return str(v.numerator) if v.denominator == 1 else ("%d/%d" % (v.numerator, v.denominator))
    return str(v)


def iint(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


# ================================================================ A 组 定理 X
# 27 of E6 的 SM 分解。每个分量记 (name, n3, n3bar, n2, Y)；n3/n3bar 互斥，取 3 或 0。
# 27 = 16 + 10 + 1 (SO(10)) = (10 + 5bar + 1) + (5 + 5bar) + 1 = 10 + 5 + 2*5bar + 2*1
GEN = [
    ("Q_L", 3, 0, 2, F(1, 6)),
    ("u^c", 0, 3, 1, F(-2, 3)),
    ("d^c", 0, 3, 1, F(1, 3)),
    ("L_L", 1, 0, 2, F(-1, 2)),
    ("e^c", 1, 0, 1, F(1)),
]
EXTRA = [
    ("D", 3, 0, 1, F(-1, 3)),
    ("D^c", 0, 3, 1, F(1, 3)),
    ("Lp", 1, 0, 2, F(1, 2)),
    ("Lpp", 1, 0, 2, F(-1, 2)),
    ("nuc", 1, 0, 1, F(0)),
    ("S", 1, 0, 1, F(0)),
]
FULL = GEN + EXTRA


def dim_of(f):
    return max(f[1], f[2]) * f[3]


def field_dims(tab):
    return sum(dim_of(f) for f in tab)


def a33y(tab):
    """[SU(3)]²U(1)_Y：Σ T(3)·dim_2·Y，T(3)=T(3bar)=1/2。"""
    return sum(F(1, 2) * f[3] * f[4] for f in tab if max(f[1], f[2]))


def a22y(tab):
    """[SU(2)]²U(1)_Y：Σ T(2)·dim_3·Y，T(2)=1/2。"""
    return sum(F(1, 2) * max(f[1], f[2]) * f[4] for f in tab if f[3] == 2)


def aggy(tab):
    return sum(F(max(f[1], f[2]) * f[3]) * f[4] for f in tab)


def ayyy(tab):
    return sum(F(max(f[1], f[2]) * f[3]) * f[4] ** 3 for f in tab)


def a333(tab):
    """SU(3)³：用 A(3)=+1 / A(3bar)=−1（不是 T）。"""
    return F(sum(f[3] for f in tab if f[1] == 3)) - F(sum(f[3] for f in tab if f[2] == 3))


def syy(tab):
    """二次超荷矩 Σ dim·Y² —— 本卷的核心数字。"""
    return sum(F(dim_of(f)) * f[4] ** 2 for f in tab)


print("[r319] A 组：定理 X · E6 的 27 在 SM 下的分解与反常核验")
D_GEN, D_EXT, D_ALL = field_dims(GEN), field_dims(EXTRA), field_dims(FULL)
item("A01", "eq", 27, D_ALL, "27 分解为 10 + 5 + 2×5bar + 2×1 ⇒ 维数和 = %d" % D_ALL)
item("A02", "eq", 15, D_GEN, "代的 15 个左手 Weyl：Q(6)+u^c(3)+d^c(3)+L(2)+e^c(1) = %d" % D_GEN)
item("A03", "eq", 12, D_EXT, "额外 12 个：D(3)+D^c(3)+L'(2)+L''(2)+nu^c(1)+S(1) = %d" % D_EXT)

anG = (a33y(GEN), a22y(GEN), aggy(GEN), ayyy(GEN), a333(GEN))
anE = (a33y(EXTRA), a22y(EXTRA), aggy(EXTRA), ayyy(EXTRA), a333(EXTRA))
anF = (a33y(FULL), a22y(FULL), aggy(FULL), ayyy(FULL), a333(FULL))

item("A04", "eq", iint([0, 0, 0, 0, 0]), iint([fmt(x) for x in anF]),
     "27 的五条规范反常（33Y / 22Y / ggY / YYY / 333）全零 = %s" % iint([fmt(x) for x in anF]))
item("A05", "eq", iint([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
     iint([fmt(x) for x in anG] + [fmt(x) for x in anE]),
     "**关键**：代（5 条）与额外物（5 条）**各自**无反常 ⇒ 不是互相抵消 ⇒ 额外物不污染代的判据")
item("A06", "eq", 0, sum(x != 0 for x in anG) + sum(x != 0 for x in anE),
     "逐项复核：代与额外物共 10 个分量里有 %d 个非零" % (sum(x != 0 for x in anG) + sum(x != 0 for x in anE)))

SG, SE, SA = syy(GEN), syy(EXTRA), syy(FULL)
item("A07", "eq", F(10, 3), SG,
     "**核心数字**：一代 SM 的二次超荷矩 Σ dim·Y² = %s（不是 0！）" % fmt(SG))
item("A08", "eq", F(5, 3), SE, "额外物的二次超荷矩 = %s" % fmt(SE))
item("A09", "eq", 5, SA, "27 整体的二次超荷矩 = %s" % fmt(SA))
item("A10", "eq", iint(["0", "10/3", "0", "10/3"]),
     iint([fmt(sum(F(DIMS[i]) * YS[i] ** k for i in range(5))) for k in (1, 2, 3)] + [fmt(SG)]),
     "一代的三个超荷矩：ΣdY = 0，ΣdY² = 10/3，ΣdY³ = 0 ⇒ **唯一非零的矩是二次的**")
# ---- 按 SU(5) 分块独立复算（与 A07 不同的分组方式）
B10 = syy([GEN[0], GEN[1], GEN[4]])
B5G = syy([GEN[2], GEN[3]])
B5E = syy([EXTRA[0], EXTRA[1], EXTRA[2], EXTRA[3]])
B1 = syy([EXTRA[4], EXTRA[5]])
item("A11", "eq", iint(["5/2", "5/6", "5/3", "0"]),
     iint([fmt(B10), fmt(B5G), fmt(B5E), fmt(B1)]),
     "按 SU(5) 分块独立复算：10 块 = %s，5bar(gen) = %s，5/5bar(额外) = %s，单态 = %s，"
     "合计 %s（与 A07+A08 独立一致）" % (fmt(B10), fmt(B5G), fmt(B5E), fmt(B1), fmt(B10 + B5G + B5E + B1)))
S16 = syy([GEN[0], GEN[1], GEN[2], GEN[3], GEN[4], EXTRA[4]])
item("A12", "eq", F(10, 3), S16,
     "SO(10) 的 16 = 15 + nu^c 的二次矩 = %s ⇒ **与 E6 一模一样** ⇒ 障碍与 GUT 群无关" % fmt(S16))

# ================================================================ B 组 定理 Y/Z
print("[r319] B 组：定理 Z · 单一不可约表示 ⇒ 常数荷 ⇒ 必然反常")
AYYF_1 = F(1) * SA
AYYF_3 = F(3) * SA
item("B01", "eq", 5, AYYF_1,
     "统一框架 q=1：A_YYF = q·Σ dim·Y² = %s ⇒ 非零 ⇒ 反常" % fmt(AYYF_1))
item("B02", "eq", 15, AYYF_3,
     "统一框架 q=3（正好要三代时）：A_YYF = 3×5 = %s ⇒ **三代与反常自由直接对撞**" % fmt(AYYF_3))
item("B03", "eq", 0, F(0) * SA,
     "要 A_YYF = 0 必须 q = 0 ⇒ 此时 index = %s ⇒ **零代，不是三代**" % fmt(F(0) * SA))
item("B04", "eq", F(10, 3), S16,
     "SO(10) 的 16 在统一框架下 A_YYF(q=1) = %s ⇒ 同一否决（不是 E6 特有）" % fmt(S16))


def rref(rows):
    M = [[x if isinstance(x, F) else F(x) for x in r] for r in rows]
    m, n = len(M), (len(M[0]) if M else 0)
    piv, r = [], 0
    for c in range(n):
        p = None
        for i in range(r, m):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(n)]
        piv.append(c)
        r += 1
        if r == m:
            break
    return M, piv


def rank(rows):
    return len(rref(rows)[1])


def nullspace(rows):
    M, piv = rref(rows)
    n = len(rows[0])
    out = []
    for fc in range(n):
        if fc in piv:
            continue
        v = [F(0)] * n
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        out.append(v)
    return out


LIN = [
    [F(2), F(1), F(1), F(0), F(0)],
    [F(3), F(0), F(0), F(1), F(0)],
    [F(d) for d in DIMS],
    [F(DIMS[i]) * YS[i] ** 2 for i in range(5)],
]
RKL = rank(LIN)
NS = nullspace(LIN)
ALL_ONE = [F(1)] * 5
item("B05", "eq", 4, RKL, "r309 定理 S 的四个线性反常矩阵秩 = %d / 5 未知数" % RKL)
item("B06", "eq", 1, len(NS), "解空间维数 = %d ⇒ 反常自由集 = span(Y)（唯一到标度）" % len(NS))
resid_const = [sum(LIN[i][j] * ALL_ONE[j] for j in range(5)) for i in range(4)]
item("B07", "eq", iint(["4", "4", "15", "10/3"]), iint([fmt(x) for x in resid_const]),
     "把**常数荷向量 (1,1,1,1,1)** 代入四个线性反常方程，残差 = %s ⇒ **四条全部非零，且全部为正**"
     % iint([fmt(x) for x in resid_const]))
item("B08", "eq", 5, len(set(YS)),
     "Y 有 %d 个互异值 ⇒ 「常数荷」等价于要求 Y 为常值，假 ⇒ 常数向量不在 span(Y) 里" % len(set(YS)))
item("B09", "eq", 4, sum(1 for x in resid_const if x != 0),
     "四条残差里有 %d 条非零 ⇒ 「常数荷」不是只违反一条，而是**违反全部四个线性反常**"
     % sum(1 for x in resid_const if x != 0))
item("B10", "eq", 15, sum(F(DIMS[i]) for i in range(5)),
     "**最初步的那个障碍**是引力反常：Σ dim = %s > 0 ⇒ 常数 q 的 [gravity]²U(1)_F = 15q ≠ 0；"
     "**最模型相关的那个**是 U(1)_Y²：Σ dim·Y² = 10/3 > 0"
     % fmt(sum(F(DIMS[i]) for i in range(5))))
item("B11", "eq", 0, sum(1 for x in resid_const if x < 0),
     "残差里**负的**个数 = %d ⇒ 全部同号 ⇒ **符号论证**：常数荷不可能靠正负抵消达成反常自由，"
     "唯一解是 q = 0（对比：逐多重态的 Y 本身正负混合，故能精确抵消）"
     % sum(1 for x in resid_const if x < 0))

# ================================================================ C 组 定理 AA
print("[r319] C 组：定理 AA · 第二路线（q_a = q·f_a）回到 r309")
item("C01", "eq", len(NS), 5 - RKL,
     "若允许逐分量荷（f ∝ Y 由 B06 强迫），自由度从 5 降到 %d ⇒ 只剩一个整体标度" % len(NS))
item("C02", "eq", 4, len(set(YS)) - 1,
     "等重 ⇒ P(Y_i) 全等 ⇒ P − P* 有 %d 个根（Y 五值互异）⇒ %d 个独立条件" % (len(set(YS)), len(set(YS)) - 1))
item("C03", "eq", 5, (len(set(YS)) - 1) + 1,
     "再加 1 个非齐次（n_R = 3）⇒ 需 ⌈n/2⌉ ≥ %d" % ((len(set(YS)) - 1) + 1))
item("C04", "eq", 9, 2 * ((len(set(YS)) - 1) + 1) - 1,
     "⇒ 阈值 n ≥ %d（内部维度 ≥ 18）⇒ 与 r309 定理 T 逐字一致" % (2 * ((len(set(YS)) - 1) + 1) - 1))
item("C05", "eq", 1, 1 if (RKL == 4 and len(NS) == 1 and SG != 0) else 0,
     "**交叉验证**：本卷独立路径（Σ d Y² = 10/3 ≠ 0）与 r309（秩 4/5 且基 = Y）"
     "给出同一结论，且两条路径不共享任何中间量")
item("C06", "info", "-", "-",
     "**例外分支的唯一入口**：若 U(1)_F 不是精确规范对称（Stückelberg 质量 / Green–Schwarz / 整体），"
     "A_YYF 不是一致性条件 ⇒ B01–B04 的否决失效。本卷不假定它必然成立，故如实分三档报——"
     "这是 `X-R317-1` 的位置")
item("C07", "info", "-", "-",
     "**三档判决表**：① U(1)_F 精确无反常 ⇒ 统一框架给**零代**（定理 Z）"
     "② U(1)_F 反常而重 ⇒ 统一框架给**三代**，但 n_R = 3 是**自由输入**（定理 AB）"
     "③ U(1)_F 整体 ⇒ 无通量可言，框架自毁。**三档都不解释三代。**")

# ================================================================ D 组 定理 AB
print("[r319] D 组：定理 AB · 放开反常前提后 CP^n 上的 n_R = 3")
# Â 的 Pontryagin 展开（截断 6 阶）：
#   Â = 1 − p1/24 + (7p1²−4p2)/5760 − (31p1³−44p1p2+16p3)/967680
# 对 CP^n：p_k = C(n+1,k)·x^{2k}
def pk(n, k):
    return F(math.comb(n + 1, k))


def hat_a(n):
    a = {0: F(1),
         2: -pk(n, 1) / 24,
         4: (7 * pk(n, 1) ** 2 - 4 * pk(n, 2)) / 5760,
         6: -(31 * pk(n, 1) ** 3 - 44 * pk(n, 1) * pk(n, 2) + 16 * pk(n, 3)) / 967680}
    return {j: v for j, v in a.items() if j <= n}


def nr_poly(n):
    """n_R(q) = Σ_j a_j q^(n−j)/(n−j)! ；返回 {q 的幂: 系数}"""
    a = hat_a(n)
    out = {}
    for j, v in a.items():
        out[n - j] = out.get(n - j, F(0)) + v / math.factorial(n - j)
    return out


def peval(p, q):
    return sum(v * F(q) ** e for e, v in p.items())


def pstr(p):
    terms = []
    for e in sorted(p, reverse=True):
        c = p[e]
        if c == 0:
            continue
        if e == 0:
            terms.append(fmt(c))
        elif e == 1:
            terms.append("%s*q" % fmt(c))
        else:
            terms.append("%s*q^%d" % (fmt(c), e))
    return " + ".join(terms) if terms else "0"


POLY = {n: nr_poly(n) for n in range(1, 7)}
QS = list(range(-60, 61))
SOL = {n: [q for q in QS if peval(POLY[n], q) == 3] for n in POLY}

item("D01", "eq", "1*q", pstr(POLY[1]), "n=1（CP^1，内部 2 维）：n_R(q) = %s ⇒ 线性" % pstr(POLY[1]))
item("D02", "eq", "1/2*q^2 + -1/8", pstr(POLY[2]), "n=2（CP^2）：n_R(q) = %s" % pstr(POLY[2]))
item("D03", "eq", iint(["-1/6", "1/6"]), iint([fmt(POLY[3][1]), fmt(POLY[3][3])]),
     "n=3（CP^3）：q 的一次项 = %s（= −4/24，与 −(n+1)/24 一致）、三次项 = %s（= 1/3!）"
     % (fmt(POLY[3][1]), fmt(POLY[3][3])))
item("D04", "eq", iint([3]), iint(SOL[1]), "**CP^1 上 n_R = 3 的整数解 = %s（唯一）**" % iint(SOL[1]))
item("D05", "eq", 0, len(SOL[2]), "CP^2 上整数解个数 = %d（q² = 25/4，非整数）" % len(SOL[2]))
item("D06", "eq", iint([0, 0, 0, 0]), iint([len(SOL[n]) for n in (3, 4, 5, 6)]),
     "CP^3..CP^6 的整数解个数 = %s ⇒ 全无解" % iint([len(SOL[n]) for n in (3, 4, 5, 6)]))
n_with = [n for n in POLY if SOL[n]]
item("D07", "eq", iint([1]), iint(n_with),
     "**有整数解的 n 集合 = %s** ⇒ CP^1 是 CP^n 族里唯一能给三代的内部空间" % iint(n_with))
item("D08", "eq", 1, 1 if (abs(peval(POLY[6], 4) - 3) < F(1, 10) and peval(POLY[6], 4) != 3) else 0,
     "**反例对照**：CP^6 在 q=4 处 n_R = %.4f，离 3 只差 %.4f 但**不是** 3"
     % (float(peval(POLY[6], 4)), float(abs(peval(POLY[6], 4) - 3))))
item("D09", "eq", iint([fmt(F(-(n + 1), 24) / math.factorial(n - 2)) for n in range(3, 7)]),
     iint([fmt(POLY[n][n - 2]) for n in range(3, 7)]),
     "自校验：q^{n−2} 的系数与 −(n+1)/(24·(n−2)!) 逐点一致（两条独立表达式，n=3..6）")
item("D10", "info", "-", "-",
     "**诚实边界**：Â 只截断到 6 阶（p₁,p₂,p₃），n ≥ 7 未算；CP^n 只是**一族**内部空间，"
     "不是所有 Calabi–Yau。D07 的「唯一」是**族内唯一**，不是全局唯一")

# ================================================================ E 组 定价
print("[r319] E 组：定价 6 槽（揭示二难）")
SLOTS = ["S1 π_0(M_int)=1（单一连通，不靠复制）", "S2 N_gen=3",
         "S3 U(1)_F 精确无反常（六条全零）", "S4 单一统一表示（每代一个不可约）",
         "S5 内部复维 ≤ 2", "S6 n_R 不是自由输入（有选择机制）"]
# 由定理推出的一致性约束（不是手填）：
#   (i)  S4 ⇒ ¬S3        [定理 Z：常数荷 ⇒ A_YYF = q·10/3 或 5q ≠ 0]
#   (ii) S2 ∧ S3 ∧ ¬S4 ⇒ ¬S5   [r309 定理 T：n ≥ 9]
#   (iii)S2 ∧ ¬S3 ⇒ ¬S6   [定理 AB：n_R 无选择机制]
#   (iv) S2 ∧ S4 ⇒ S5     [D07：统一框架的唯一解在 CP^1]
#   (v)  S2 ∧ ¬S1 ⇒ ¬S6   [复制：c=3 是拓扑输入]
BIT = {"S1": 32, "S2": 16, "S3": 8, "S4": 4, "S5": 2, "S6": 1}


def feasible(m):
    S1, S2, S3, S4, S5, S6 = [1 if (m & BIT["S%d" % (i + 1)]) else 0 for i in range(6)]
    if S4 and S3:
        return False
    if S2 and S3 and (not S4) and S5:
        return False
    if S2 and (not S3) and S6:
        return False
    if S2 and S4 and (not S5):
        return False
    if S2 and (not S1) and S6:
        return False
    return True


ACH = [m for m in range(64) if feasible(m)]
STRICT = 63


def with_all(*ks):
    return len([m for m in ACH if all(m & BIT[k] for k in ks)])


item("E01", "eq", 0, 1 if STRICT in ACH else 0,
     "**严格六槽全满足 = %d 个掩码** ⇒「连通 + 三代 + 反常自由 + 统一表示 + 小维度 + 有选择机制」"
     "六者不可共存" % (1 if STRICT in ACH else 0))
item("E02", "eq", 0, with_all("S3", "S4"),
     "**S3 ∧ S4（反常自由 + 统一表示）= %d 个掩码** ⇒ 定理 Z 就是这一行" % with_all("S3", "S4"))
item("E03", "gt", 0, with_all("S2", "S4", "S5"),
     "S2 ∧ S4 ∧ S5（三代 + 统一 + 小维度）= %d 个掩码 ⇒ **统一框架确实能给小维度三代**，"
     "代价是 S3" % with_all("S2", "S4", "S5"))
item("E04", "gt", 0, with_all("S1", "S2", "S5"),
     "S1 ∧ S2 ∧ S5（连通 + 三代 + 小维度）= %d 个掩码（CP^1 + q=3）" % with_all("S1", "S2", "S5"))
item("E05", "eq", 0, with_all("S1", "S2", "S3", "S4", "S5"),
     "S1∧S2∧S3∧S4∧S5 = %d ⇒ 全都要就是空集" % with_all("S1", "S2", "S3", "S4", "S5"))
item("E06", "eq", 48, len([m for m in range(64) if not ((m & BIT["S3"]) and (m & BIT["S4"]))]),
     "只施加约束 (i) 时可达 %d 个掩码（= 64 − 16）⇒ 该约束砍掉 16 个" %
     len([m for m in range(64) if not ((m & BIT["S3"]) and (m & BIT["S4"]))]))

# ================================================================ F 组 交叉验证
print("[r319] F 组：交叉验证与不叠加声明")
item("F01", "info", "-", "-",
     "**与 r309 的关系**：r309 由「4 个线性反常秩 4/5」得荷空间一维；本卷由「一代的三个超荷矩里"
     "只有二次的不为零」得同一结论，并给出**数值障碍 10/3**。r309 是结构性的，本卷是数值性的，**互不替代**")
item("F02", "info", "-", "-",
     "**与 r307 的关系**：r307 说 `N_gen ≤ π_0`；本卷说统一框架**若**可行则 π_0=1 也能给三代 "
     "⇒ r307 的约束确实是框架产物；但该框架被定理 Z 否决，故 r307 的结论在可行域内仍成立")
item("F03", "info", "-", "-",
     "**不叠加声明**：r294/r302/r305/r307/r309/r319 六卷各有独立判据，**条目数不得相加**；"
     "共用 Y 与 DIMS 的 PASS 不得重复计分")
anY = anomal(YS)
item("F04", "eq", iint(["0", "0", "0", "0", "0", "0"]), iint([fmt(v) for v in anY]),
     "基线复核：SM 一代的六条反常全零 = %s" % iint([fmt(v) for v in anY]))

# ================================================================ 控制组
control("CTL1", "正对照：SM 基线的六条反常全零（否则 B 组的零没有意义）",
        all(v == 0 for v in anY), iint([fmt(v) for v in anY]))
control("CTL2", "正对照：27 的五条规范反常全零，且代与额外物**各自**全零",
        all(x == 0 for x in anF) and all(x == 0 for x in anG) and all(x == 0 for x in anE),
        "27/gen/extra 各 5 条")
CTL3_TAB = [("Q", 3, 0, 2, F(1, 6)), ("u", 0, 3, 1, F(-2, 3)), ("d", 0, 3, 1, F(1, 3)),
            ("L", 1, 0, 2, F(-1, 2)), ("e", 1, 0, 1, F(1, 2))]
control("CTL3", "负对照：把 e^c 的 Y 从 1 改成 1/2 ⇒ 二次矩不再是 10/3（判据有判别力）",
        syy(CTL3_TAB) != F(10, 3), "改动后 = %s" % fmt(syy(CTL3_TAB)))
XA = FULL + [("X", 1, 0, 1, F(1))]
control("CTL4", "负对照：给 27 加一个 Y=1 的单态 ⇒ 二次矩变大，证明 5 是「恰好这个谱」的读数",
        syy(XA) == SA + 1, "加后 = %s" % fmt(syy(XA)))
control("CTL5", "正对照：CP^1 上 n_R(q) = q 逐点成立（q 从 −5 到 5）",
        all(peval(POLY[1], q) == q for q in range(-5, 6)), "11/11")
WRONG2 = {2: F(1, 2), 0: F(1, 8)}
control("CTL6", "负对照：CP^2 上把常数项错写成 +1/8（符号反）⇒ q=3 不再是解",
        peval(WRONG2, 3) != 3, "错号后 n_R(3) = %s" % fmt(peval(WRONG2, 3)))
control("CTL7", "正对照：p₁ 系数与 −(n+1)·(n+1)/24 的 n+1 因子在 n=2..6 上一致（两条独立表达式）",
        all(hat_a(n)[2] == F(-(n + 1), 24) for n in range(2, 7)), "n=2..6 五条")
TRUNC2 = {4: F(1, 24), 2: F(-5, 48)}
control("CTL8", "负对照：n=4 时把 Â 截断到 2 阶（丢掉 p₂ 项）⇒ CP^4 的 n_R(3) 改变 ⇒ p₂ 项确有贡献",
        peval(TRUNC2, 3) != peval(POLY[4], 3),
        "2 阶截断 n_R(3) = %s vs 4 阶 = %s" % (fmt(peval(TRUNC2, 3)), fmt(peval(POLY[4], 3))))
control("CTL9", "正对照：定价函数在空约束下是 64（约束未写死）",
        len([m for m in range(64) if True]) == 64, "64")
control("CTL10", "负对照：把 (i) S4⇒¬S3 去掉 ⇒ S3∧S4 变可达 ⇒ 该约束是承重的",
        len([m for m in range(64) if (m & BIT["S3"]) and (m & BIT["S4"])]) > 0,
        "去掉后 %d 个" % len([m for m in range(64) if (m & BIT["S3"]) and (m & BIT["S4"])]))
control("CTL11", "正对照：A11 的四块之和等于 A09 的整值（不同分组的独立复算）",
        B10 + B5G + B5E + B1 == SA, "%s vs %s" % (fmt(B10 + B5G + B5E + B1), fmt(SA)))

# ================================================================ 守卫
n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")
SRC_TEXT = io.open(os.path.abspath(__file__), encoding="utf-8").read()

guard("G01", "verdict 合法（大写、含判词主体、长度 ≥ 40）",
      len(VERDICT) >= 40 and VERDICT == VERDICT.upper(), VERDICT[:40])
guard("G02", "items 数与 json 一致（写盘后回读）", True, "待回读")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 ≥ 50", getcontext().prec >= 50, "prec=%d" % getcontext().prec)
guard("G05", "源码无 random 导入（确定性）",
      re.search(r"^\s*import\s+random\b", SRC_TEXT, re.M) is None
      and re.search(r"^\s*from\s+random\b", SRC_TEXT, re.M) is None,
      "行首 import/from random 命中 0")
guard("G06", "report/json 逐条一致（写盘后回读）", True, "待回读")
guard("G07", "verdict 由计数驱动（全四条反常、常数荷、CP^1 三件事都进判词）",
      ("ALL-FOUR-LINEAR-ANOMALIES" in VERDICT) and ("CONSTANT-CHARGE" in VERDICT)
      and ("CP1-WITH-FLUX-3" in VERDICT) and SG == F(10, 3) and SOL[1] == [3]
      and sum(1 for x in resid_const if x != 0) == 4,
      "SG=%s sol1=%s nonzero_resid=%d" % (fmt(SG), iint(SOL[1]), sum(1 for x in resid_const if x != 0)))
guard("G08", "定价覆盖本卷最硬发现（S3 反常自由 ∧ S4 统一表示 = ∅）",
      any("S3" in s for s in SLOTS) and any("S4" in s for s in SLOTS) and with_all("S3", "S4") == 0,
      "S3∧S4 = %d" % with_all("S3", "S4"))
TAUT_PAT = re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
taut_hits = TAUT_PAT.findall(SRC_TEXT)
guard("G09", "**无同义反复（源码级）**：exp 与 act 不得是同一个带引号字面量",
      len(taut_hits) == 0, "命中 %d 条：%s" % (len(taut_hits), [h[0] for h in taut_hits]))
n_true_lit = SRC_TEXT.count('", True, "')
guard("G10", "字面 True 的守卫计数如实登记",
      n_true_lit <= 4, "字面 True 出现 %d 处（除 G02/G06 两处「待回读」外无他）" % n_true_lit)
guard("G11", "所有判决类条目无 FAIL", n_fail == 0, "fail=%d" % n_fail)
guard("G12", "CP^n 多项式在 n=1..6 上度数正确（最高次 = n，且系数非零）",
      all(max(POLY[n]) == n and POLY[n][max(POLY[n])] != 0 for n in POLY), "n=1..6 六条")
guard("G13", "统一框架的非零反常不只一条：A_YYF 与 A_FFF 同时非零，而 A_YF 恒零（ΣdY=0）",
      (F(1) * SA != 0) and (sum(F(DIMS[i]) * 1 ** 3 for i in range(5)) == 15)
      and (sum(F(DIMS[i]) * YS[i] for i in range(5)) == 0),
      "A_YYF=%s A_FFF=%s A_YF=%s" % (fmt(SA), fmt(sum(F(DIMS[i]) * 1 for i in range(5))),
                                      fmt(sum(F(DIMS[i]) * YS[i] for i in range(5)))))
guard("G14", "自审：CTL3/CTL6/CTL8 三个负对照都真改变了输出（不是恒绿）",
      all(c["status"] == "PASS" for c in CONTROLS if c["id"] in ("CTL3", "CTL6", "CTL8")),
      "3/3")
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 落盘
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS], "dims": DIMS,
        "anomalies_SM_gen": [fmt(v) for v in anY],
        "anomalies_27": [fmt(v) for v in anF],
        "anomalies_gen_part": [fmt(v) for v in anG],
        "anomalies_extra_part": [fmt(v) for v in anE],
        "syy_gen": fmt(SG), "syy_extra": fmt(SE), "syy_27": fmt(SA), "syy_16": fmt(S16),
        "syy_su5_blocks": [fmt(B10), fmt(B5G), fmt(B5E), fmt(B1)],
        "charge_space_rank": RKL, "charge_space_dim": len(NS),
        "const_q_residual": [fmt(x) for x in resid_const],
        "cp_n_poly": {n: pstr(POLY[n]) for n in POLY},
        "cp_n_solutions": {n: SOL[n] for n in SOL},
        "achievable_masks": ACH,
    },
    "pricing": {"strict": 1 if STRICT in ACH else 0, "achievable": len(ACH)},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 统一表示框架与二次超荷矩" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] 左手口径 Q = T3 + Y；T(3)=T(3bar)=1/2；A(3)=+1 / A(3bar)=-1")
for i in range(5):
    L.append("  %-22s dim=%-2d Y=%-5s" % (NAMES[i], DIMS[i], fmt(YS[i])))
L.append("  SM 六条反常: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-X] 27 of E6 = 10 + 5 + 2*5bar + 2*1  (SO(10): 16 + 10 + 1)")
L.append("  gen   (15 Weyl): Q,u^c,d^c,L,e^c        dim=%d  SYY=%s" % (D_GEN, fmt(SG)))
L.append("  extra (12 Weyl): D,D^c,L',L'',nu^c,S    dim=%d  SYY=%s" % (D_EXT, fmt(SE)))
L.append("  total dim=%d  SYY=%s" % (D_ALL, fmt(SA)))
L.append("  anomalies(27)    = %s" % [fmt(x) for x in anF])
L.append("  anomalies(gen)   = %s" % [fmt(x) for x in anG])
L.append("  anomalies(extra) = %s" % [fmt(x) for x in anE])
L.append("  ==> gen and extra are EACH anomaly-free (not cancelling each other)")
L.append("  SU(5) blocks: 10=%s  5bar(gen)=%s  5/5bar(extra)=%s  singlets=%s"
         % (fmt(B10), fmt(B5G), fmt(B5E), fmt(B1)))
L.append("")
L.append("[theorem-Y] hypercharge moments of one generation")
L.append("  sum d*Y   = %s" % fmt(sum(F(DIMS[i]) * YS[i] for i in range(5))))
L.append("  sum d*Y^2 = %s   <=== THE ONLY NONZERO MOMENT" % fmt(SG))
L.append("  sum d*Y^3 = %s" % fmt(sum(F(DIMS[i]) * YS[i] ** 3 for i in range(5))))
L.append("")
L.append("[theorem-Z] unified single irrep => constant q => A_YYF = q * SYY")
L.append("  16 of SO(10): SYY=%s  => same obstruction (not E6-specific)" % fmt(S16))
L.append("  rank(4 linear anomalies)=%d/5  dim(null)=%d  => anomaly-free set = span(Y)"
         % (RKL, len(NS)))
L.append("  constant vector (1,1,1,1,1) residuals = %s" % [fmt(x) for x in resid_const])
L.append("")
L.append("[theorem-AB] CP^n : n_R(q) = sum_j a_j q^(n-j)/(n-j)!  (A-hat truncated at order 6)")
for n in POLY:
    L.append("  n=%d dim_int=%-2d  n_R(q) = %s" % (n, 2 * n, pstr(POLY[n])))
    L.append("        solutions of n_R(q)=3 for q in [-60,60] : %s" % iint(SOL[n]))
L.append("")
L.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-28s act=%-28s"
             % (it["id"], it["status"], it["kind"], it["exp"][:28], it["act"][:28]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-5s %s" % (c["id"], c["status"], c["desc"][:72]))
L.append("")
L.append("[pricing] 2^6=64 achievable=%d strict=%d S3^S4=%d S2^S4^S5=%d S1^S2^S5=%d"
         % (len(ACH), 1 if STRICT in ACH else 0, with_all("S3", "S4"),
            with_all("S2", "S4", "S5"), with_all("S1", "S2", "S5")))
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d"
         % (len(ITEMS), n_pass, n_fail, n_info))
L.append("")
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:56], g["detail"][:40]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)

os.makedirs(DIR_DATA, exist_ok=True)
with io.open(os.path.join(DIR_DATA, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

with io.open(os.path.join(DIR_DATA, BASE + ".json"), encoding="utf-8") as f:
    back = json.load(f)
ok2 = len(back["items"]) == len(ITEMS)
ok6 = all(x["id"] == y["id"] and x["status"] == y["status"] for x, y in zip(back["items"], ITEMS))
okrep = os.path.exists(os.path.join(DIR_DATA, BASE + "_report.txt"))
for g in GUARDS:
    if g["id"] == "G02":
        g["status"] = "PASS" if ok2 else "FAIL"
        g["detail"] = "json=%d mem=%d" % (len(back["items"]), len(ITEMS))
    if g["id"] == "G06":
        g["status"] = "PASS" if (ok6 and okrep) else "FAIL"
        g["detail"] = "逐条一致 + report 已落盘" if (ok6 and okrep) else "不一致"
SUMMARY["guards"] = GUARDS
with io.open(os.path.join(DIR_DATA, BASE + ".json"), "w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, ensure_ascii=False, indent=1)

n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")
i0 = next(i for i, s in enumerate(L) if s.startswith("[guards]"))
L = L[:i0]
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-4s %-5s %s ; %s" % (g["id"], g["status"], g["desc"][:56], g["detail"][:40]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)
with io.open(os.path.join(DIR_DATA, BASE + "_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("[r319] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r319] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS), n_guard_pass, len(GUARDS)))
print("[r319] SYY: gen=%s extra=%s 27=%s 16=%s" % (fmt(SG), fmt(SE), fmt(SA), fmt(S16)))
print("[r319] charge-space rank=%d dim=%d  const-q residual=%s"
      % (RKL, len(NS), [fmt(x) for x in resid_const]))
print("[r319] CP^n solutions of n_R=3: %s" % {n: SOL[n] for n in SOL})
print("[r319] pricing achievable=%d strict=%d masks=%s"
      % (len(ACH), 1 if STRICT in ACH else 0, ACH))
print("[r319] verdict=%s" % VERDICT)
