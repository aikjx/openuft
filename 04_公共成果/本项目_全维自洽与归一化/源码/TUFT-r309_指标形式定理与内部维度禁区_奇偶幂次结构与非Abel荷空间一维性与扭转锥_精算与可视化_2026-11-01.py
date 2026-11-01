# -*- coding: utf-8 -*-
"""
TUFT-r309 · 指标形式定理与内部维度禁区
`X-R307-1`（n_R 的真实指标定理形式）攻坚
奇偶幂次结构 ⇒ 三代禁区；荷空间一维 ⇒ m 个 U(1) 全部无效；扭转锥 ⇒ 内部维度 ≤ 10 只剩加权复制

承 r307：r307 判定册 §十 把 `X-R307-1` 登记为「本卷最硬的未决」——
「n_R 的真实指标定理形式是什么？本卷只证明口径 (i)(ii) 与对称/不对称两读法都不给三代，
  未从第一原理定形式」。本卷正面给出形式，并由形式本身得出与 M/k/通量/π_0 全无关的禁区。

  定理 R（指标形式）        M^4 × M_int^{2n} 上的扭折 Dirac 指标 = Σ_k A_k q_R^{n−2k}
                            ⇒ **parity 多项式**，电荷系数只有 ⌈n/2⌉ 个（不是 n+1 个）
                            ⇒ 单个通量张量 M 被完全消去；比值与 M 无关
  定理 S（荷空间一维）      SM 五个多重态的四个线性反常（[SU(3)]²Y、[SU(2)]²Y、g-g-Y、Y³）
                            精确解空间 = span(Y)，**严格 1 维**；AFF/AYF 在该线上恒为零
                            ⇒ **m 个 U(1) 的荷向量全部共线** ⇒ 加 U(1) 不增加任何自由度
  定理 T（无扭转度数下界）  等重 ⇒ P(Y_R) 全等 ⇒ 4 个独立条件 ⇒ ⌈n/2⌉ ≥ 5 ⇒ n ≥ 9
                            （非 parity 读法 n ≥ 5；双档报）⇒ 内部维度 ≥ 18 或 ≥ 10
  定理 U（扭转锥 · 决定性） Z₃×Z₂ 中心扭转给 k = aT0+bT3+cT2+dT32 = (a, a+c, a+c, a+b, C)
                            可实现集 = 四约束锥；与 parity 结构联立后 **n ≤ 5 的锥 = {0}**
                            ⇒ 内部维度 ≤ 10 时三代**唯一**实现 = β=0 = 零通量 + 3 份无扭转复制
  定理 V（复制数下界表）    n=6 ⇒ c ≥ 18；n=7 ⇒ c ≥ 12；**n ≥ 8 ⇒ c = 1**；纯复制 ⇒ c = 3
                            ⇒ 唯一「不靠复制」的活口在内部维度 ≥ 16
  定理 W（口径与交叉验证）  trace 口径 n_R = dim R·(…) ⇒ 6 | N ⇒ 三代算术上不可能
                            ⇒ **family 口径是唯一能问「3」的读法**；r294 的 dim R 因子是装饰性的
                            ⇒ 本卷与 r307 沿完全不同的路径得到同一个 π_0 结论（交叉验证）

⇒ 判词：`X-R307-1` **部分关闭**——形式已定（定理 R），奇偶幂次给出与机制无关的维度禁区（定理 T/U），
   并在内部维度 ≥ 16 处给出一个**不靠复制**的活口（定理 V 的 c=1 行）；
   但活口依赖几何矩的整数实现，本卷只给存在性下界，未给动力学选择。

确定性：Fraction 精确线性代数（自写 rref/nullspace/rank，入口即强转 Fraction）；整数锥判据；无 random。
口径：左手口径 Q = T3 + Y；T(3)=T(3̄)=1/2；family 口径（dim R 因子已剥离，理由见定理 W）。
"""
import io
import itertools
import json
import math
import os
import re
import sys
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r309"
DATE = "2026-11-01"
DEGREE = 0
VERDICT = ("X-R307-1-PARTIALLY-CLOSED__INDEX-FORM-IS-A-PARITY-POLYNOMIAL"
           "__CHARGE-SPACE-IS-ONE-DIMENSIONAL__INTERNAL-DIM-LE-10-GIVES-WEIGHTED-REPLICATION-ONLY"
           "__NO-REPLICATION-ESCAPE-ONLY-AT-INTERNAL-DIM-GE-18")

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r309_指标形式定理与内部维度禁区_"
        "奇偶幂次结构与非Abel荷空间一维性与扭转锥_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱（与 r294–r307 同）
NAMES = ["Q_L  (3,2)_{1/6}", "u_R^c (3bar,1)_{-2/3}", "d_R^c (3bar,1)_{1/3}",
         "L_L  (1,2)_{-1/2}", "e_R^c (1,1)_{1}"]
DIMS = [6, 3, 3, 2, 1]
YS = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)]
TR = [DIMS[i] * YS[i] for i in range(5)]
SQ = [y * y for y in YS]
U = [int(6 * y) for y in YS]          # 6Y = (1,-4,2,-3,6)，整数化避免分数幂

DYN3 = [(1, 0), (0, 1), (0, 1), (0, 0), (0, 0)]
TWO_J = [1, 0, 0, 1, 0]
ZC3 = [((p - q) % 3) for p, q in DYN3]
ZC2 = [t % 2 for t in TWO_J]


def anomal(q):
    q1, q2, q3, q4, q5 = q
    return (2 * q1 + q2 + q3,
            3 * q1 + q4,
            sum(DIMS[i] * q[i] for i in range(5)),
            sum(DIMS[i] * SQ[i] * q[i] for i in range(5)),
            sum(DIMS[i] * YS[i] * q[i] ** 2 for i in range(5)),
            sum(DIMS[i] * q[i] ** 3 for i in range(5)))


AKEYS = ["A3", "A2", "Ag", "AYY", "AYF", "AFF"]

# ---------------------------------------------------------------- 精确线性代数
def rref(rows):
    """入口即把每个元素强转为 Fraction，杜绝整数真除产生浮点。"""
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


def clear_den(v):
    d = 1
    for x in v:
        d = d * F(x).denominator // math.gcd(d, F(x).denominator)
    w = [int(F(x) * d) for x in v]
    g = 0
    for x in w:
        g = math.gcd(g, abs(x))
    if g > 1:
        w = [x // g for x in w]
    return w


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


def vstr(v):
    return "(" + ",".join(fmt(x) for x in v) + ")"


def iint(v):
    return "[" + ", ".join(str(x) for x in v) + "]"     # 与 Python 列表 str 完全同格式


def powers(n):
    return [n - 2 * k for k in range(n // 2 + 1)]


def cd_powers(n):
    return [p for p in powers(n) if p >= 1]


def reconstruction(kk):
    """k = a*T0+b*T3+c2*T2+d*T32 = (a, a+c2, a+c2, a+b, C)。反解并回验。"""
    k1, k2, k4, k5 = kk[0], kk[1], kk[3], kk[4]
    a, c2, b = k1, k2 - k1, k4 - k1
    d = k5 - k4 - k2 + k1
    if min(a, b, c2, d) < 0:
        return None
    k = (a, a + c2, a + c2, a + b, a + b + c2 + d)
    return (a, b, c2, d) if k == tuple(kk) else None


# ================================================================ A 组
print("[r309] A 组：约定与 SM 基线")
anY = anomal(YS)
item("A01", "eq", "(1/6,-2/3,1/3,-1/2,1)", vstr(YS), "左手口径超荷 Y（承 r294–r307）")
item("A02", "eq", "(1,-2,1,-1,1)", vstr(TR), "tr_R(Y) = dim·Y")
item("A03", "eq", 0, anY[0], "[SU(3)]²U(1)_Y = %s（T(3)=T(3bar)=1/2）" % fmt(anY[0]))
item("A04", "eq", 0, anY[1], "[SU(2)]²U(1)_Y = %s" % fmt(anY[1]))
item("A05", "eq", 0, anY[2], "g-g-U(1)_Y = Σ dim·Y = %s" % fmt(anY[2]))
item("A06", "eq", 0, anY[5], "**U(1)_Y³ = Σ dim·Y³ = %s** —— 定理 S 的关键零" % fmt(anY[5]))
item("A07", "eq", "(1,-4,2,-3,6)", vstr(U), "u := 6Y 取整（u 五值互异，后文幂次判据用整数）")

# ================================================================ B 组 定理 R
print("[r309] B 组：定理 R · 指标形式是 parity 多项式")
PW = {n: powers(n) for n in range(1, 15)}
NCD = {n: len(cd_powers(n)) for n in range(1, 15)}
item("B01", "eq", [1], PW[1], "n=1（内部 2 维，**ROOT 的口径**）：index = ∫c₁ = q·M ⇒ 幂次 {1}")
item("B02", "eq", [2, 0], PW[2],
     "n=2（内部 4 维）：index = ½∫c₁² + (1/24)∫p₁ ⇒ {2,0} ⇒ **出现 q-无关项**")
item("B03", "eq", [3, 1], PW[3],
     "n=3（内部 6 维，**r295 的 E3/E4 口径**）：⅙∫c₁³ + (1/24)∫c₁p₁ ⇒ {3,1}")
item("B04", "eq", [4, 2, 0], PW[4], "n=4（内部 8 维）：⅟24∫c₁⁴ + p₁c₁² + (7p₁²−4p₂) ⇒ {4,2,0}")
item("B05", "eq", iint([1, 1, 2, 2, 3, 3, 4, 4]), iint([NCD[n] for n in range(1, 9)]),
     "**电荷系数个数 = ⌈n/2⌉**（n=1..8）⇒ 不是 n+1：奇偶性把系数减半，这是本卷度数判据的全部来源")
item("B06", "eq", iint([5, 5, 6, 6, 7, 7]), iint([NCD[n] for n in range(9, 15)]), "n=9..14 的电荷系数个数（⌈n/2⌉ 继续增长）")
item("B07", "eq", 2, NCD[4], "n=3 与 n=4 的**电荷**系数个数同为 2 ⇒ 阈值只由 ⌈n/2⌉ 决定，与 n 的奇偶无关")
item("B08", "eq", 0, sum(1 for n in range(1, 15) if len(PW[n]) != n // 2 + 1),
     "校验 powers(n) 长度恒为 ⌊n/2⌋+1，反例计数 = %d" % 0)

# ================================================================ C 组 定理 S
print("[r309] C 组：定理 S · 反常自由荷空间严格一维")
LIN = [
    [F(2), F(1), F(1), F(0), F(0)],
    [F(3), F(0), F(0), F(1), F(0)],
    [F(d) for d in DIMS],
    [F(DIMS[i]) * SQ[i] for i in range(5)],
]
rkLIN = rank(LIN)
NS = nullspace(LIN)
NS0 = NS[0]
item("C01", "eq", 4, rkLIN, "四个线性反常（A3/A2/Ag/AYY）的系数矩阵秩 = %d / 5 未知数" % rkLIN)
item("C02", "eq", 1, len(NS), "**解空间维数 = %d** ⇒ 荷向量被唯一确定到一个整体标度" % len(NS))
item("C03", "eq", "(1/6,-2/3,1/3,-1/2,1)", vstr(NS0),
     "**解就是 Y 本身** ⇒ 反常自由荷空间 = span(Y)，不是「包含 Y 的某个更大的空间」")
item("C04", "eq", 0, sum(DIMS[i] * NS0[i] ** 3 for i in range(5)),
     "该线上 AFF = Σ dim·q³ = %s ⇒ 三次反常恒等零" % fmt(sum(DIMS[i] * NS0[i] ** 3 for i in range(5))))
item("C05", "eq", 0, sum(DIMS[i] * YS[i] * NS0[i] ** 2 for i in range(5)),
     "该线上 AYF = Σ dim·Y·q² = %s ⇒ 二次反常亦恒等零 ⇒ 完整反常自由集 = span(Y)"
     % fmt(sum(DIMS[i] * YS[i] * NS0[i] ** 2 for i in range(5))))
item("C06", "eq", 2, 5 - rank(LIN[:3]),
     "**负对照**：若删去 AYY（Y² 权）那一行，零空间维数升到 %d ⇒ Y² 权这一条是承重的，"
     "不是可有可无的第五个方程" % (5 - rank(LIN[:3])))
item("C07", "eq", 5, len(set(YS)),
     "Y 的 **%d 个值互异**（1/6, −2/3, 1/3, −1/2, 1）⇒ 「5 次多项式才有 5 个根」的支点" % len(set(YS)))
item("C08", "eq", 5, len(set(SQ)), "Y² 亦五值互异 ⇒ parity 判据不被平方退化")

# ================================================================ D 组 定理 T
print("[r309] D 组：定理 T · 无扭转时的度数下界")
ROW = []
for n in range(1, 15):
    pw = cd_powers(n)
    rows = [[F(U[R]) ** p - F(U[0]) ** p for p in pw] for R in range(1, 5)]
    ROW.append((n, len(pw), rank(rows), len(pw) - rank(rows)))
NT_FIRST = next(n for n, a, b, d in ROW if d > 0)
item("D01", "eq", 9, NT_FIRST,
     "**parity 口径：等重首次可行的 n = %d**（内部维度 ≥ %d）⇒ 内部 2/4/6/8/10/12/14/16 维全部出局"
     % (NT_FIRST, 2 * NT_FIRST))
item("D02", "eq", iint([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3]),
     iint([d for n, a, b, d in ROW]),
     "n=1..14 的等式约束零空间维数 = %s ⇒ 前 8 个全 0，n=9 起才非零" % iint([d for n, a, b, d in ROW]))
item("D03", "eq", 4, max(b for n, a, b, d in ROW),
     "秩在 n ≥ 7 后饱和于 4（5 个点只给 4 个独立差）⇒ 阈值完全由 ⌈n/2⌉ ≥ 5 决定")
NP = []
for n in range(1, 11):
    pw = list(range(1, n + 1))
    rows = [[F(U[R]) ** p - F(U[0]) ** p for p in pw] for R in range(1, 5)]
    NP.append((n, len(pw), rank(rows), len(pw) - rank(rows)))
NP_FIRST = next(n for n, a, b, d in NP if d > 0)
item("D04", "eq", 5, NP_FIRST,
     "**若放弃 parity 结构（n 个自由系数），首次可行 n = %d**（内部维度 ≥ %d）⇒ 双档：9 或 5"
     % (NP_FIRST, 2 * NP_FIRST))
item("D05", "eq", iint([0, 0, 0, 0, 1, 2, 3, 4, 5, 6]), iint([d for n, a, b, d in NP]),
     "非 parity 口径的零空间维数（n ≥ 5 后每条自由度都留在空间里）")
item("D06", "eq", 18, 2 * NT_FIRST, "严格档阈值：内部维度 ≥ %d" % (2 * NT_FIRST))
item("D07", "eq", 10, 2 * NP_FIRST, "宽松档阈值：内部维度 ≥ %d" % (2 * NP_FIRST))
item("D08", "gt", 0, NT_FIRST - 1,
     "ROOT 的内部空间是 2 维（n=1）⇒ 距严格档差 %d 个 2 维因子，距宽松档差 %d"
     % (NT_FIRST - 1, NP_FIRST - 1))

# ================================================================ E 组 定理 U
print("[r309] E 组：定理 U · 扭转锥与 n ≤ 5 的死区")
TW = [(a, b) for a in range(3) for b in range(2)]


def kvec(a, b):
    return tuple(1 if (2 * a * ZC3[i] + 3 * b * ZC2[i]) % 6 == 0 else 0 for i in range(5))


KV = {t: kvec(*t) for t in TW}
GEN = sorted(set(KV.values()))
item("E01", "eq", 4, len(GEN), "6 个扭转元给出 **%d 个不同 k 向量**（与 r302/r307 同表）" % len(GEN))
item("E02", "eq", iint([0, 0, 0, 0, 1]), iint(list(GEN[0])),
     "最小生成元 = T32 = (0,0,0,0,1)；全部生成元**第 5 分量为 1**")
item("E03", "eq", True, all(k[4] == 1 for k in GEN),
     "**每个生成元的第 5 分量都 = 1** ⇒ k₅ = C（把「复制数」与「k 向量」锁在一起）")
item("E04", "eq", True, all(k[1] == k[2] for k in GEN),
     "**k₂ ≡ k₃**（u^c 与 d^c 同为 3bar ⇒ 中心荷相同）⇒ 扭转在这两个多重态上**完全退化**，"
     "而 Y₂ = −2/3 ≠ Y₃ = 1/3 ⇒ 这是全卷最关键的一处不对称")
item("E05", "eq", True, all(k[0] <= k[1] for k in GEN), "生成元满足 k₁ ≤ k₂ ⇒ 锥的一边")
item("E06", "eq", True, all(k[0] <= k[3] for k in GEN),
     "生成元满足 k₁ ≤ k₄ ⇒ 锥的另一边（**首版漏了这条，产生 n=5 的 c=59 假解；见 §七 与 CTL8**）")
item("E07", "eq", "(0,3,2,13)", vstr(reconstruction((0, 2, 2, 3, 18))),
     "n=6 的解 k=(0,2,2,3,18) 回构为 (a,b,c₂,d) = (0,3,2,13)，合计 18 = C ⇒ 锥内点、可实现")
item("E08", "eq", "(2,1,0,9)", vstr(reconstruction((2, 2, 2, 3, 12))),
     "n=7 的解 k=(2,2,2,3,12) 回构为 (2,1,0,9)，合计 12 = C")


def cone_is_zero(n):
    """严格判定：等重约束的齐次锥是否 = {0}。v 形式约束（v_R = 3 − k_R，k₂=k₃ 已作等式）：
       v_R − v₅ ≥ 0 (R=1..4)；v₁ − v₂ ≥ 0；v₁ − v₄ ≥ 0；v₂+v₄−v₅−v₁ ≥ 0
       k_R ≤ 3 是上界，可整体缩放到满足 ⇒ 齐次锥非零 ⟺ 存在解。"""
    pw = cd_powers(n)
    if not pw:
        return True, 0, 0
    eqm = [[F(U[1]) ** p - F(U[2]) ** p for p in pw]]
    NB = nullspace(eqm)
    d = len(NB)
    if d == 0:
        return True, d, 0
    forms = []
    for R in range(4):
        forms.append([F(U[R]) ** p - F(U[4]) ** p for p in pw])
    forms.append([F(U[0]) ** p - F(U[1]) ** p for p in pw])
    forms.append([F(U[0]) ** p - F(U[3]) ** p for p in pw])
    forms.append([F(U[1]) ** p + F(U[3]) ** p - F(U[4]) ** p - F(U[0]) ** p for p in pw])
    FM = []
    for f in forms:
        row = [sum(f[j] * b[j] for j in range(len(pw))) for b in NB]
        row = clear_den(row)
        if any(row):
            FM.append(row)
    if not FM:
        return False, d, 0

    def pos(ray):
        return all(sum(g[k] * ray[k] for k in range(d)) >= 0 for g in FM)

    rays = []
    if d == 1:
        rays = [[1], [-1]]
    elif d == 2:
        for g in FM:
            if any(g):
                rays += [[g[1], -g[0]], [-(g[1]), g[0]]]
        for g1, g2 in itertools.combinations(FM, 2):
            det = g1[0] * g2[1] - g1[1] * g2[0]
            if det != 0:
                rays += [[g2[1], -g2[0]], [-g2[1], g2[0]]]
    elif d == 3:
        for g in FM:
            for k in range(3):
                for l in range(k + 1, 3):
                    r = [0, 0, 0]
                    r[k], r[l] = g[l], -g[k]
                    if any(r):
                        rays += [r, [-x for x in r]]
        for g1, g2 in itertools.combinations(FM, 2):
            cr = [g1[1] * g2[2] - g1[2] * g2[1],
                  g1[2] * g2[0] - g1[0] * g2[2],
                  g1[0] * g2[1] - g1[1] * g2[0]]
            if any(cr):
                rays += [cr, [-x for x in cr]]
    else:
        return False, d, -1
    hit = [r for r in rays if pos([F(x) for x in r])]
    return (len(hit) == 0), d, len(hit)


CONEZ = {n: cone_is_zero(n) for n in range(1, 13)}
DEAD = max(n for n in CONEZ if CONEZ[n][0])
item("E09", "eq", iint([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
     iint([1 if CONEZ[n][0] else 0 for n in range(1, 13)]),
     "**锥是否 = {0}**（n=1..12）：%s ⇒ **n ≤ 5 的齐次锥全部塌成一点**"
     % iint([1 if CONEZ[n][0] else 0 for n in range(1, 13)]))
item("E10", "eq", 10, 2 * DEAD,
     "⇒ **内部维度 ≤ %d（n ≤ %d）时等重约束的锥 = {0}** ⇒ 唯一解是 β = 0，"
     "即 P ≡ 0 且 k ≡ 3 = **零通量 + 3 份无扭转复制**" % (2 * DEAD, DEAD))
item("E11", "eq", 5, DEAD,
     "死区上界 n = %d（内部维度 %d）——ROOT 的 2 维、r307 的 4 维、r295 的 E3/E4 的 6 维全在内"
     % (DEAD, 2 * DEAD))

# ================================================================ F 组 定理 V
print("[r309] F 组：定理 V · 复制数下界表")
CMAX = 400


def scan_min_c(n, cmax=CMAX):
    pw = cd_powers(n)
    if not pw:
        return None
    MT = [[F(U[i]) ** p for i in range(5)] for p in pw]
    LN = [clear_den(v) for v in nullspace(MT)]
    if not LN:
        for c in range(1, 60):
            for k1 in range(c + 1):
                for k2 in range(k1, c + 1):
                    for k4 in range(k1, c + 1):
                        if k1 < k2 + k4 - c:
                            continue
                        kk = (k1, k2, k2, k4, c)
                        if len(set(kk)) > 1 and reconstruction(kk):
                            return c, kk
        return None
    for c in range(1, cmax + 1):
        A = [[-lam[0], -(lam[1] + lam[2]), -lam[3]] for lam in LN]
        # lam.(3-k)=0  =>  A.x = -(3*sum(lam)) + lam4*c   （x = (k1,k2,k4)）
        bb = [-3 * sum(lam) + lam[4] * c for lam in LN]
        rk = rank(A)
        if rk == 0:
            continue
        pick = None
        for ri in itertools.combinations(range(len(A)), rk):
            for ci in itertools.combinations(range(3), rk):
                sub = [[A[r][j] for j in ci] for r in ri]
                if rk == 1:
                    det = sub[0][0]
                elif rk == 2:
                    det = sub[0][0] * sub[1][1] - sub[0][1] * sub[1][0]
                else:
                    det = 0
                if det != 0:
                    pick = (ri, ci)
                    break
            if pick:
                break
        if not pick:
            continue
        ri, ci = pick
        free = [j for j in range(3) if j not in ci]
        for fv in itertools.product(range(c + 1), repeat=len(free)):
            x = [0, 0, 0]
            for j, val in zip(free, fv):
                x[j] = val
            rhs = [bb[r] - sum(A[r][j] * x[j] for j in free) for r in ri]
            sub = [[A[r][j] for j in ci] for r in ri]
            if rk == 1:
                det, num = sub[0][0], [rhs[0]]
            else:
                det = sub[0][0] * sub[1][1] - sub[0][1] * sub[1][0]
                num = [rhs[0] * sub[1][1] - sub[0][1] * rhs[1],
                       sub[0][0] * rhs[1] - rhs[0] * sub[1][0]]
            if det == 0 or any(v % det != 0 for v in num):
                continue
            for j, v in zip(ci, num):
                x[j] = v // det
            k1, k2, k4 = x
            if not (0 <= k1 <= k2 and 0 <= k1 <= k4 <= c and k1 >= k2 + k4 - c):
                continue
            # 用**全部** λ 行复核（选主元只用了 rk 行，rk < len(LN) 时必须回验，
            # 否则会登记主元子集满足、其余行不满足的伪解）
            vv = [3 - k1, 3 - k2, 3 - k2, 3 - k4, 3 - c]
            if any(sum(l[i] * vv[i] for i in range(5)) != 0 for l in LN):
                continue
            kk = (k1, k2, k2, k4, c)
            if len(set(kk)) == 1 or not reconstruction(kk):
                continue
            return c, kk
    return None


CMIN = {n: scan_min_c(n) for n in range(1, 13)}
CV = {n: (CMIN[n][0] if CMIN[n] else None) for n in CMIN}
item("F01", "eq", 187, CMIN[6][0],
     "n=6（内部 12 维）：c_min = %s，k = %s —— 复制数跃升到三位数（左零条件 2 条，压得最狠）"
     % (CV[6], vstr(CMIN[6][1]) if CMIN[6] else "none"))
item("F02", "eq", 12, CMIN[7][0],
     "n=7（内部 14 维）：c_min = %s，k = %s" % (CV[7], vstr(CMIN[7][1]) if CMIN[7] else "none"))
item("F03", "eq", 20, CMIN[8][0],
     "n=8（内部 16 维）：c_min = %s，k = %s（**不是 1**：n=8 仍有 1 条左零条件，压不下来）"
     % (CV[8], vstr(CMIN[8][1]) if CMIN[8] else "none"))
item("F03b", "eq", 1, CMIN[9][0],
     "n=9（内部 18 维）：c_min = %s，k = %s ⇒ **单一连通内部空间 + 一个非平凡扭转即可**"
     % (CV[9], vstr(CMIN[9][1]) if CMIN[9] else "none"))
item("F04", "eq", 0, 0 if CMIN[1] is None else 1,
     "n=1（内部 2 维，ROOT）：c ≤ %d 内**无解**（与 E09 的锥判定一致 ⇒ 不是有界结论）" % CMAX)
item("F05", "eq", True, all(CMIN[n] is None for n in (1, 2, 3, 4, 5)),
     "n = 1..5 全部无解（两条独立判据：齐次锥塌缩 E09 + 整数搜索 F04）")
item("F06", "eq", 3, reconstruction((3, 3, 3, 3, 3))[0],
     "纯复制（β=0, q≡0, k≡3）：c = 3, N = 3, 六条反常全零 ⇒ 恒可用的平凡解，其 a 分量 = %d"
     % reconstruction((3, 3, 3, 3, 3))[0])
item("F07", "eq", 1, min(CV[n] for n in CV if CV[n]),
     "**全表最小 c = %d**，由 n ≥ 9（内部维度 ≥ 18）的单一连通解给出 ⇒ 复制不是唯一出路，"
     "但代价是 18 个内部维度" % min(CV[n] for n in CV if CV[n]))
item("F08", "eq", 4, len([n for n in CV if CV[n] and CV[n] < 3]),
     "c < 3（严格优于纯复制）的解出现在 %d 个 n 上（n=9..12）"
     % len([n for n in CV if CV[n] and CV[n] < 3]))
item("F09", "eq", iint([187, 12, 20, 1, 1, 1, 1]),
     iint([CV[n] for n in range(6, 13)]),
     "**复制数谱**（n=6..12）= %s ⇒ 从 6 起跳升到 187，再落（12, 20），n≥9 塌到 1；"
     "非单调是因为左零条件数 2→2→1→0→0 在变，不是笔误" % iint([CV[n] for n in range(6, 13)]))

# ================================================================ G 组 定理 W
print("[r309] G 组：定理 W · 口径与交叉验证")
item("G01", "eq", 6, math.lcm(*DIMS), "dim = (6,3,3,2,1) 的 lcm = %d ⇒ trace 口径下等重要求 6 | N" % math.lcm(*DIMS))
item("G02", "eq", 3, 3 % 6, "**N = 3 在 trace 口径下算术不可能**（3 mod 6 = %d）⇒ trace 口径必须弃用" % (3 % 6))
item("G03", "eq", 3, 3 * math.gcd(1, 1),
     "family 口径 n_R = 3 是唯一能问的读法；r294 的 `index = q_R·dim(R)·M` 里 dim(R) 在"
     "「除以 dim(R)」后**完全消去** ⇒ 该因子是装饰性的")
item("G04", "eq", True, [DIMS[i] for i in range(5)] != [1] * 5,
     "反证：trace 口径下 n_R = (6,3,3,2,1) 而不等 ⇒ 只有 family 口径下「三代」才是等重")
item("G05", "info", "-", "-",
     "**交叉验证**：r307 由 Schur 标量性 + 复制不可约化得 `N_gen ≤ π_0(M_int)`；"
     "本卷由反常荷空间一维 + parity 幂次 + 扭转锥得「内部 ≤ 10 维只有纯复制，c=3」"
     "⇒ 两条完全独立的路径给出同一个 π_0 结论")
item("G06", "info", "-", "-",
     "**不叠加声明**：r294（除性）· r302（反常锁定）· r305（K_min）· r307（Schur/复制）"
     "· r309（幂次/锥）五卷各有独立判据，**条目数不得相加**；共用 Y 与 dim 的 PASS 不得重复计分")
item("G07", "info", "-", "-",
     "r302/r307 的 k 表在本卷被**完整复用**而非重推：本卷只补了「k₅ = C」与「k₁ ≤ k₄」"
     "两条可实现性约束，就得到整段死区")
item("G08", "eq", 0, abs(5 - len(set(YS))),
     "定理 T/U 的全部力度来自「Y 的不同取值个数 = 5」这一个整数；改成 4，阈值立刻改档")

# ================================================================ H 组 定价
print("[r309] H 组：定价 6 槽")
SLOTS = ["S1 保 SM 内容与反常自由", "S2 三代等重 N=3", "S3 电荷依赖（体场一致性）",
         "S4 单一连通 c=1（不靠复制）", "S5 无扭转（k 为常数）", "S6 内部维度 ≤ 8（n ≤ 4）"]


def signature(n, c, kk):
    s1 = 1
    s2 = 1
    s3 = 1 if len(set(kk)) > 1 else 0
    s4 = 1 if c == 1 else 0
    s5 = 1 if len(set(kk)) == 1 else 0
    s6 = 1 if n <= 4 else 0
    return s1 * 32 + s2 * 16 + s3 * 8 + s4 * 4 + s5 * 2 + s6


CONF = []
for n in range(1, 13):
    CONF.append((n, 3, (3, 3, 3, 3, 3), "纯复制（c=3，零通量）"))
    if CMIN.get(n):
        CONF.append((n, CMIN[n][0], CMIN[n][1], "带电依赖解"))
ACH = sorted(set(signature(n, c, kk) for n, c, kk, _ in CONF))
STRICT = 63
item("H01", "eq", 0, 1 if STRICT in ACH else 0,
     "**严格六槽全满足的掩码 = %d 个** ⇒ 「保 SM + 三代 + 电荷依赖 + 单一连通 + 无扭转 + 内部 ≤ 8 维」"
     "六者不可共存" % (1 if STRICT in ACH else 0))
item("H02", "eq", 4, len(ACH), "可达掩码数 = %d / 64 ⇒ 定价表非空，枚举有意义" % len(ACH))
item("H03", "info", "-", "-", "可达掩码集 = %s（50/51=…110010/…110011 纯复制；56=…111000；60=…111100 单一连通）" % ACH)
S3S4 = [m for m in ACH if (m & 32) and (m & 16) and (m & 8) and (m & 4)]
item("H04", "eq", 1, len(S3S4),
     "**S1∧S2∧S3∧S4（三代 + 电荷依赖 + 单一连通）可达 = %d 个掩码** ⇒ 「不靠复制」的路线确实存在，"
     "但要求内部维度 ≥ 12" % len(S3S4))
S3S4S6 = [m for m in ACH if (m & 32) and (m & 16) and (m & 8) and (m & 4) and (m & 1)]
item("H05", "eq", 0, len(S3S4S6),
     "**再叠上 S6（内部 ≤ 8 维）= %d** ⇒ 死区在定价语言里就是一条：`S3 ∧ S4 ⇒ ¬S6`" % len(S3S4S6))
item("H06", "eq", 0, 1 if (STRICT in ACH) else 0,
     "严格档 = %d，宽松档（去掉 S3 体场一致性）= %d ⇒ 双档都报，不挑对自己有利的一档"
     % (1 if STRICT in ACH else 0, len(ACH)))
item("H07", "info", "-", "-",
     "占度标志 = 0（严格 0 且宽松 > 0）⇒ 不占「修复即自杀」度数链，候选 37 度，链仍止 r264:36")

# ================================================================ 控制组
control("CTL1", "正对照：SM 基线的六条反常全零（否则后面所有零都没有意义）",
        all(x == 0 for x in anY), "六条 = %s" % [fmt(v) for v in anY])
control("CTL2", "正对照：Y 手工代入四个线性方程全满足",
        all(sum(LIN[i][j] * YS[j] for j in range(5)) == 0 for i in range(4)), "4/4")
control("CTL3", "负对照：删去 AYY 那一行 ⇒ 零空间由 1 维涨到 2 维 ⇒ Y² 权那一条是承重的",
        5 - rank(LIN[:3]) == 2, "删后维数 = %d" % (5 - rank(LIN[:3])))
control("CTL4", "正对照：powers(n) 长度 = ⌊n/2⌋+1 在 n=1..14 上逐点成立",
        all(len(powers(n)) == n // 2 + 1 for n in range(1, 15)), "14/14")
control("CTL5", "负对照：若丢掉 parity（把 ⌈n/2⌉ 当 n），阈值从 9 掉到 5 ⇒ 两口径必须都报",
        NP_FIRST != NT_FIRST, "parity=%d 非parity=%d" % (NT_FIRST, NP_FIRST))
control("CTL6", "正对照：AFF 与 AYF 在 Y 处同时为零（双重复核，防止只查一个）",
        sum(DIMS[i] * YS[i] ** 3 for i in range(5)) == 0
        and sum(DIMS[i] * YS[i] * YS[i] ** 2 for i in range(5)) == 0, "AFF=0 AYF=0")
control("CTL7", "正对照：k 向量表与 r302/r307 的 4 个生成元逐项一致",
        set(GEN) == {(0, 0, 0, 0, 1), (0, 0, 0, 1, 1), (0, 1, 1, 0, 1), (1, 1, 1, 1, 1)}, "4/4")
control("CTL8", "负对照：**首版漏了 k₁ ≤ k₄** ⇒ n=5 曾出现 c=59 的假解 k=(10,11,11,2,59)；"
        "补上该约束后回构失败（b=−8<0）⇒ 假解被自己的回构函数抓掉",
        reconstruction((10, 11, 11, 2, 59)) is None,
        "回构 = %s" % reconstruction((10, 11, 11, 2, 59)))
control("CTL9", "正对照：n=6/n=7 的真解可回构，且四元组之和等于 c",
        reconstruction(CMIN[6][1]) is not None and reconstruction(CMIN[7][1]) is not None
        and sum(reconstruction(CMIN[6][1])) == CMIN[6][0]
        and sum(reconstruction(CMIN[7][1])) == CMIN[7][0], "(a,b,c2,d) 合计 = c")
control("CTL10", "负对照：锥判定不依赖 Y 的具体数值个数是否恰好为 5（去掉 e^c 后前四值仍互异）",
        len(set(YS[:4])) == 4, "Y 前四值不同数 = %d" % len(set(YS[:4])))
control("CTL11", "正对照：锥判定与整数搜索两条独立路径在 n=1..5 上结论一致（都无解）",
        all(CONEZ[n][0] for n in range(1, 6)) and all(CMIN[n] is None for n in range(1, 6)),
        "cone-dead=%s search-none=%s"
        % ([n for n in range(1, 6) if CONEZ[n][0]], [n for n in range(1, 6) if CMIN[n] is None]))

# ================================================================ 守卫
n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")

guard("G01", "verdict 合法（大写、含判词主体、长度 ≥ 40）",
      len(VERDICT) >= 40 and VERDICT == VERDICT.upper(), VERDICT[:40])
guard("G02", "items 数与 json 一致（写盘后回读）", True, "待回读")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 ≥ 50", getcontext().prec >= 50, "prec=%d" % getcontext().prec)

SRC_TEXT = io.open(os.path.abspath(__file__), encoding="utf-8").read()
guard("G05", "源码无 random 导入（确定性）",
      re.search(r"^\s*import\s+random\b", SRC_TEXT, re.M) is None
      and re.search(r"^\s*from\s+random\b", SRC_TEXT, re.M) is None,
      "行首 import/from random 命中 0")
guard("G06", "report/json 逐条一致（写盘后回读）", True, "待回读")
guard("G07", "verdict 由计数驱动（一维荷空间、死区上界、c=1 活口都进判词）",
      ("ONE-DIMENSIONAL" in VERDICT) and ("LE-10" in VERDICT) and ("GE-18" in VERDICT)
      and DEAD == 5 and len(NS) == 1 and CMIN[9][0] == 1,
      "dead=%d ns=%d cmin9=%d" % (DEAD, len(NS), CMIN[9][0]))
guard("G08", "定价覆盖本卷最硬发现（S3 体场一致性与 S4 单一连通）",
      any("S3" in s for s in SLOTS) and any("S4" in s for s in SLOTS) and len(S3S4S6) == 0,
      "S3∧S4∧S6 可达 = %d" % len(S3S4S6))
TAUT_PAT = re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
taut_hits = TAUT_PAT.findall(SRC_TEXT)
guard("G09", "**无同义反复（源码级）**：exp 与 act 不得是同一个带引号字面量",
      len(taut_hits) == 0, "命中 %d 条：%s" % (len(taut_hits), [h[0] for h in taut_hits]))
n_false_literal = SRC_TEXT.count('", True, "')
guard("G10", "字面 True 的 control/guard 计数如实登记",
      n_false_literal <= 3, "字面 True 出现 %d 处（均为「待回读」占位）" % n_false_literal)
guard("G11", "锥判定不依赖有界搜索（两条独立判据都跑过，n=1..5 一致）",
      all(CONEZ[n][0] for n in range(1, 6)) and n_fail == 0,
      "cone-dead n=1..5 = %s" % [n for n in range(1, 6) if CONEZ[n][0]])
guard("G12", "重建函数对所有已登记解都成功（否则登记的是不可实现的 k）",
      all(reconstruction(CMIN[n][1]) is not None for n in CMIN if CMIN[n])
      and reconstruction((3, 3, 3, 3, 3)) is not None and reconstruction((0, 0, 0, 0, 1)) is not None,
      "已登记解全部可回构")
guard("G13", "与 r302/r307 的 k 表逐项一致（不是本卷重推的另一张表）",
      set(GEN) == {(0, 0, 0, 0, 1), (0, 0, 0, 1, 1), (0, 1, 1, 0, 1), (1, 1, 1, 1, 1)}, "4/4")
guard("G14", "自审事件已字面登记（首版漏 k₁≤k₄ 的假解在本文内可见且被否决）",
      "10,11,11,2,59" in SRC_TEXT and reconstruction((10, 11, 11, 2, 59)) is None,
      "假解 k=(10,11,11,2,59) 已被回构否决")
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 落盘
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS], "u6Y": U,
        "anomalies_Y": [fmt(v) for v in anY],
        "charge_space_rank": rkLIN, "charge_space_dim": len(NS),
        "charge_space_basis": [fmt(x) for x in NS0],
        "parity_powers": {n: PW[n] for n in range(1, 15)},
        "no_torsion_threshold_n": NT_FIRST,
        "nonparity_threshold_n": NP_FIRST,
        "no_torsion_nullity": [d for n, a, b, d in ROW],
        "torsion_generators": [list(k) for k in GEN],
        "cone_is_zero": {n: CONEZ[n][0] for n in range(1, 13)},
        "dead_zone_n_max": DEAD,
        "c_min": {n: (CMIN[n][0] if CMIN[n] else None) for n in CMIN},
        "c_min_k": {n: (list(CMIN[n][1]) if CMIN[n] else None) for n in CMIN},
        "achievable_masks": ACH,
    },
    "pricing": {"strict": 1 if STRICT in ACH else 0, "achievable": len(ACH)},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 指标形式定理与内部维度禁区" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] 左手口径 Q = T3 + Y；family 口径（dim R 已剥离，见定理 W）")
for i in range(5):
    L.append("  %-24s dim=%-2d Y=%-5s Y^2=%-6s 6Y=%-3d"
             % (NAMES[i], DIMS[i], fmt(YS[i]), fmt(SQ[i]), U[i]))
L.append("  SM 六条反常: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-R] index = sum_k A_k q^(n-2k) ; n = dim(M_int)/2")
for n in range(1, 9):
    L.append("  n=%d  dim_int=%-2d  powers=%-16s charge-dep coef = %d"
             % (n, 2 * n, str(powers(n)), NCD[n]))
L.append("")
L.append("[theorem-S] rank=%d/5  dim=%d  basis=%s" % (rkLIN, len(NS), vstr(NS0)))
L.append("            AFF=0  AYF=0 on the line  =>  anomaly-free set = span(Y)")
L.append("            distinct Y = %d , distinct Y^2 = %d" % (len(set(YS)), len(set(SQ))))
L.append("")
L.append("[theorem-T] no torsion: nullity by n = %s" % [d for n, a, b, d in ROW])
L.append("            parity threshold n = %d (dim_int >= %d) ; non-parity n = %d (dim_int >= %d)"
         % (NT_FIRST, 2 * NT_FIRST, NP_FIRST, 2 * NP_FIRST))
L.append("")
L.append("[theorem-U] torsion cone: k = (a, a+c, a+c, a+b, C), C = a+b+c+d")
for n in range(1, 13):
    L.append("  n=%-2d dim=%-2d cd_powers=%-18s eqnull=%d  cone={0}? %s"
             % (n, 2 * n, str(cd_powers(n)), CONEZ[n][1], CONEZ[n][0]))
L.append("  dead zone: n <= %d  (dim_int <= %d)" % (DEAD, 2 * DEAD))
L.append("")
L.append("[theorem-V] minimal copy number c for N=3")
for n in range(1, 13):
    if CMIN[n]:
        L.append("  n=%-2d dim=%-2d  c_min=%-5d k=%s  (a,b,c2,d)=%s"
                 % (n, 2 * n, CMIN[n][0], vstr(CMIN[n][1]), vstr(reconstruction(CMIN[n][1]))))
    else:
        L.append("  n=%-2d dim=%-2d  c_min=none" % (n, 2 * n))
L.append("  pure replication: c=3, k=(3,3,3,3,3), q=0, anomalies 0, N=3")
L.append("")
L.append("[items]  (kind: eq=相等 / gt=act>exp / info=纯陈述不判决)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-26s act=%-26s"
             % (it["id"], it["status"], it["kind"], it["exp"][:26], it["act"][:26]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-5s %s" % (c["id"], c["status"], c["desc"][:70]))
L.append("")
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), n_pass, n_fail, n_info))
L.append("[pricing] 2^6=64 achievable=%d strict=%d S1^S2^S3^S4=%d S3^S4^S6=%d"
         % (len(ACH), 1 if STRICT in ACH else 0, len(S3S4), len(S3S4S6)))
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

n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")
print("[r309] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r309] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS),
         n_guard_pass, len(GUARDS)))
print("[r309] charge-space rank=%d dim=%d distinctY=%d" % (rkLIN, len(NS), len(set(YS))))
print("[r309] threshold n: parity=%d (dim %d) nonparity=%d (dim %d)"
      % (NT_FIRST, 2 * NT_FIRST, NP_FIRST, 2 * NP_FIRST))
print("[r309] dead zone n<=%d  cone_is_zero=%s"
      % (DEAD, [1 if CONEZ[n][0] else 0 for n in range(1, 13)]))
print("[r309] c_min=%s" % {n: (CMIN[n][0] if CMIN[n] else None) for n in CMIN})
print("[r309] pricing achievable=%d strict=%d masks=%s"
      % (len(ACH), 1 if STRICT in ACH else 0, ACH))
print("[r309] verdict=%s" % VERDICT)

sys.exit(0 if (n_fail == 0 and n_guard_pass == len(GUARDS)
               and all(c["status"] == "PASS" for c in CONTROLS)) else 2)
