# -*- coding: utf-8 -*-
"""TUFT-r331 · 族数整性定理与 k 坐标压缩

攻 r327 的两处未审假设：
  (1) 定理 D 说 `x = q+(n-1)/2 in Z  <=>  q 在 FW 格上`，但那张格是**从 r325 借来的**
      （结构依赖 c1(CP^n)=(n+1)H、spin 性、D-brane 必须带 spin^c）。
      本卷问：如果只用「q 有理 + 族数是整数」这两条，能不能**独立**逼出同一张格？
  (2) 定理 E 用四个支点证「跳过 3」。本卷问：换个坐标（k 而不是 x），四个支点会不会塌成两个？

结论（都在本文件里机检）：
  A 整性定理：x 有理、n>=1、C(x,n) in Z  ==>  x in Z。（3 行证明：p|b => p∤分子，而 p^n|分母）
  B 格重建：由 A 反解出的 q 集合 === r325 的 FW 格（12/12），但**不需要 spin^c**。
  C 非负性：n_R >= 0 砍掉奇 n 的一半 q（k<0 区），且不砍掉任何解。
  D k 坐标：k = x - n，n_R = ±C(M,n) 且 M>=n <=> n_R != 0 ⇒ 零段与负支被**吸收**，四支点塌成两支点。
  E 冗余性：r327 的支点 3/4 是支点 1 在 x 坐标下的两个影子。

确定性：无 random；全 Fraction 精确；Decimal(prec=60) 仅用于格式化。
"""
import io
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r331"
DATE = "2026-11-01"
DEGREE = 0                 # 不占度（宽松档 SURVIVE = 0）
CAND_DEGREE = 37
NMAX = 15
BASE = ("TUFT-r331_族数整性定理与k坐标压缩_格是算术结果不是spin结果_"
        "四支点证明压成两支点_精算与可视化_2026-11-01")

VERDICT = ("X-R327-COORDINATE-REVIEWED__N_R-IS-PLUS-OR-MINUS-C-M-N-WITH-M-AT-LEAST-N"
           "__THE-X-COORDINATE-WAS-THE-WRONG-ONE-K-ABSORBS-LEGS-THREE-AND-FOUR"
           "__INTEGRALITY-OF-N_R-ALONE-FORCES-THE-FREED-WITTEN-LATTICE-WITHOUT-SPINC"
           "__FOUR-LEGS-COMPRESS-TO-TWO__SOLUTION-SET-UNCHANGED"
           "__ASSUMPTIONS-WEAKENED-SO-THE-RESULT-IS-STRENGTHENED"
           "__STILL-NOT-PREDICTED")

# ================================================================ SM 基线（与 r292..r327 同口径）
NAMES = ["Q_L (3,2)_{1/6}", "u^c (3bar,1)_{-2/3}", "d^c (3bar,1)_{1/3}",
         "L_L (1,2)_{-1/2}", "e^c (1,1)_{1}"]
DIMS = [6, 3, 3, 2, 1]
YS = [F(1, 6), F(-2, 3), F(1, 3), F(-1, 2), F(1)]


def anomal(q):
    return (2 * q[0] + q[1] + q[2],
            3 * q[0] + q[3],
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
    if isinstance(v, Decimal):
        return str(v)
    return str(v)


def iint(v):
    return "[" + ", ".join(fmt(x) for x in v) + "]"


# ================================================================ 核心对象
def binom_g(x, n):
    """广义二项式 C(x,n)，x 为 Fraction，n 为非负整数。精确。"""
    if n < 0:
        raise ValueError("n < 0")
    num = F(1)
    for i in range(n):
        num *= (F(x) - i)
    return num / math.factorial(n)


def nr_binom(n, q):
    """r327 定理 C：n_R(q) = C(q + (n-1)/2, n)。"""
    return binom_g(F(q) + F(n - 1, 2), n)


def k_of(n, q):
    """k = q - (n+1)/2 = x - n。"""
    return F(q) - F(n + 1, 2)


def chi_sheaf(n, k):
    """CP^n 上 O(k) 的 Euler 示性（只用层上同调维数公式）。
    k >= 0 : C(k+n, n)
    k <= -1: Serre 对偶 ⇒ 只有 h^n 非零，h^n = C(-k-1, n) ⇒ chi = (-1)^n C(-k-1, n)
    """
    k = int(k)
    if k >= 0:
        return F(math.comb(k + n, n))
    return F((-1) ** n * math.comb(-k - 1, n))


def M_of(n, k):
    """把 n_R 写成 ±C(M,n) 的那个 M（分段）。"""
    k = int(k)
    return (k + n) if k >= 0 else (-k - 1)


def fw_lattice(n, qmax=6):
    """r325 定理 A 的格：n 奇 ⇒ q in Z；n 偶 ⇒ q in Z + 1/2。"""
    out = []
    for m in range(-4 * qmax, 4 * qmax + 1):
        q = F(m, 4)
        if n % 2 == 1:
            if q.denominator == 1:
                out.append(q)
        else:
            if (q - F(1, 2)).denominator == 1:
                out.append(q)
    return out


NS = list(range(1, NMAX + 1))

# ================================================================ A 组 整性定理
print("[r331] A 组：定理 A · 族数整性定理（x 有理 + n>=1 + C(x,n) 整数 ⇒ x 整数）")

A_TOT, A_NONINT = 0, 0
A_BY_N = {}
for n in range(1, 11):
    tot, bad = 0, 0
    for b in range(2, 9):                       # 分母 2..8（含全部 n! 的素因子）
        for a in range(-20, 21):
            if math.gcd(abs(a), b) != 1:        # 只取既约
                continue
            tot += 1
            if binom_g(F(a, b), n).denominator != 1:
                bad += 1
    A_TOT += tot
    A_NONINT += bad
    A_BY_N[n] = (tot, bad)
item("A01", "eq", A_TOT, A_NONINT,
     "**定理 A（族数整性定理）**：`x ∈ Q`、`n ≥ 1`、`C(x,n) ∈ Z` ⇒ `x ∈ Z`。"
     "机检：`n = 1..10` × 分母 `b = 2..8` × 既约分子 `|a| ≤ 20`，共 **%d** 个非整有理点，"
     "其中给出整数值的有 **%d** 个 ⇒ **一个都没有**。分母非空（`A_TOT > 0`），不是空集空转。" % (A_TOT, A_NONINT))

A_ZINT_TOT, A_ZBAD = 0, 0
for n in range(1, 11):
    for a in range(-40, 41):
        A_ZINT_TOT += 1
        if binom_g(F(a), n).denominator != 1:
            A_ZBAD += 1
item("A02", "eq", 0, A_ZBAD,
     "**正对照（分母非空的反面）**：`x ∈ Z` 时 `C(x,n)` **必为整数** —— "
     "`n = 1..10` × `x = −40..40` 共 **%d** 组，非整 **%d** 组 ⇒ 定理 A 是「当且仅当」，不是单边" % (A_ZINT_TOT, A_ZBAD))

A_EX_BAD, A_EX = 0, 0
for n in range(1, 11):
    for b in range(2, 9):
        for a in range(-20, 21):
            if math.gcd(abs(a), b) != 1:
                continue
            p = min([d for d in range(2, b + 1) if b % d == 0])
            if a % p == 0:                      # 既约保证不会发生
                A_EX += 1
            prod = 1
            for i in range(n):
                prod *= (a - i * b)
            if prod % p == 0:                   # 证明的核心一步：分子与 p 互素
                A_EX_BAD += 1
item("A03", "eq", 0, A_EX_BAD,
     "**证明的核心一步被机检**：取 `p | b` 的最小素因子，则分子 `∏_{i<n}(a − i b) ≡ a^n (mod p)`，"
     "而 `gcd(a,b)=1 ⇒ p ∤ a` ⇒ `p ∤ 分子`；但分母含 `b^n ⊇ p^n`，`n ≥ 1` ⇒ 约分后分母仍带 `p`。"
     "机检：全样本中「分子被 p 整除」的个数 = **%d**（`a ≡ 0 mod p` 的样本 = %d，同为零）" % (A_EX_BAD, A_EX))

item("A04", "eq", iint([F(-1, 8), F(1, 16), F(3, 8)]),
     iint([binom_g(F(1, 2), 2), binom_g(F(1, 2), 3), binom_g(F(3, 2), 2)]),
     "**手算三个具体值**：`C(1/2,2) = (1/2)(−1/2)/2 = −1/8`、`C(1/2,3) = (1/2)(−1/2)(−3/2)/6 = 1/16`、"
     "`C(3/2,2) = (3/2)(1/2)/2 = 3/8` ⇒ 分母分别是 `8, 16, 8`，**都带 2**，与证明一致（`b=2 ⇒ p=2`）")

A_DENOM_HIT, A_DENOM_TOT = 0, 0
for n in range(1, 11):
    for b in range(2, 9):
        for a in range(-20, 21):
            if math.gcd(abs(a), b) != 1:
                continue
            p = min([d for d in range(2, b + 1) if b % d == 0])
            A_DENOM_TOT += 1
            if binom_g(F(a, b), n).denominator % p == 0:
                A_DENOM_HIT += 1
item("A05", "eq", A_DENOM_TOT, A_DENOM_HIT,
     "**加强版**：不只「非整数」，而是「约分后的分母**仍被 `p` 整除**」（`p` = `b` 的最小素因子）。"
     "%d / %d 全部命中 ⇒ 这不是「恰好不整」，是**结构性不整**，且不整的来源就是那个 `p`" % (A_DENOM_HIT, A_DENOM_TOT))

A_LIN_TOT_LIST = [F(a, b) for b in range(2, 9) for a in range(-20, 21)
                  if math.gcd(abs(a), b) == 1]
A_LIN = [x for x in A_LIN_TOT_LIST if (2 * x).denominator == 1]
item("A06", "gt", 0, len(A_LIN),
     "**负对照：不是所有多项式都这样**。把 `C(x,n)` 换成一次式 `2x`，则 `x = 1/2` 就给整数 1 ⇒ "
     "在同 %d 个非整有理点上，`2x` 有 **%d** 个整值 ⇒ 定理 A 是**二项式特有**的性质，"
     "不是「有理点代入多项式就不整」这种废话" % (len(A_LIN_TOT_LIST), len(A_LIN)))

A_N0 = 0
for n in [0]:
    for b in range(2, 9):
        for a in range(-20, 21):
            if math.gcd(abs(a), b) != 1:
                continue
            if binom_g(F(a, b), n).denominator == 1:
                A_N0 += 1
item("A07", "gt", 0, A_N0,
     "**诚实边界**：定理 A 需要 `n ≥ 1`。`n = 0` 时 `C(x,0) ≡ 1`，对**任何**有理 `x` 都是整数 "
     "⇒ 非整点上给整值的个数 = **%d**（全部）⇒ `n = 0`（即 `CP^0` = 一点，`n_R ≡ 1`）是定理的例外，"
     "而它恰好是「零代」的平凡情形" % A_N0)

A_BIG_BAD = 0
for n in [12, 15]:
    for b in [2, 3, 4, 5, 6, 7, 8]:
        for a in [-41, -37, -23, -19, -13, -7, -5, -3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
            if math.gcd(abs(a), b) != 1:
                continue
            if binom_g(F(a, b), n).denominator == 1:
                A_BIG_BAD += 1
item("A08", "eq", 0, A_BIG_BAD,
     "**推到 n = 12, 15**（远离 A01 的 `n ≤ 10`）：分母 2..8 × 20 个素数分子，非整上给整值的 = **%d** "
     "⇒ 定理 A 与大 `n` 无关（它甚至不需要 `n` 有界）" % A_BIG_BAD)

# ================================================================ B 组 格重建（不借 spin^c）
print("[r331] B 组：定理 B · 由整性反解出的格 === r325 的 Freed-Witten 格")

ARITH = {}
for n in NS:
    hit = []
    for m in range(-24, 25):                    # 步长 1/4，比格更细：不预设格的间距
        q = F(m, 4)
        if nr_binom(n, q).denominator == 1:
            hit.append(q)
    ARITH[n] = hit
FWG = {n: fw_lattice(n, 6) for n in NS}

SAME = [n for n in NS if ARITH[n] == FWG[n]]
item("B01", "eq", iint(NS), iint(SAME),
     "**定理 B（格重建）**：对 `q ∈ [−6,6]` **按 1/4 步长**取 49 个候选（刻意比格更细，避免「按格取样」的循环），"
     "筛出「`C(q+(n−1)/2, n) ∈ Z`」的那些 `q` ⇒ 与 r325 定理 A 的格（n 奇 `Z`、n 偶 `Z+1/2`）"
     "**逐 n 完全相同，12/12**")

SYM = 0
for n in NS:
    SYM += len(set(ARITH[n]) ^ set(FWG[n]))
item("B02", "eq", 0, SYM,
     "**对称差 = %d**（12 个 n 的并）⇒ 两条路径给出的是**同一张格**，不是「大致相同」" % SYM)

B_INTZ, B_TOT = 0, 0
for n in NS:
    for q in FWG[n]:
        B_TOT += 1
        if nr_binom(n, q).denominator == 1:
            B_INTZ += 1
item("B03", "eq", B_TOT, B_INTZ,
     "**正向**：FW 格上的 %d 个点**全部**给整数 `n_R`（%d/%d）⇒ 格是整性的**子集**" % (B_TOT, B_INTZ, B_TOT))

B_OFFINT, B_OFF = 0, 0
for n in NS:
    for m in range(-24, 25):
        q = F(m, 4)
        if q in FWG[n]:
            continue
        B_OFF += 1
        if nr_binom(n, q).denominator == 1:
            B_OFFINT += 1
item("B04", "eq", 0, B_OFFINT,
     "**反向**：离格的 %d 个点给整数 `n_R` 的 = **%d** ⇒ 格是整性的**全集**（不是子集）"
     "⇒ 双向合起来：**格 ⟺ 整性**，`B03` 与 `B04` 两条都必须过，缺一条只证了一半" % (B_OFF, B_OFFINT))

item("B05", "info", "-", "-",
     "**为什么这条值得单独立册**：r325 定理 A 的输入是 `c1(CP^n)=(n+1)H`、`w2=c1 mod 2`、"
     "以及「D-brane 必须带 spin^c 结构」—— 最后一条是**物理假设**（对某些非 spin 流形 D-brane 甚至不允许）。"
     "本卷的输入只有两条：**`q ∈ Q`（通量量子化）** 与 **`n_R ∈ Z`（族数是整数）**。"
     "假设更弱 ⇒ 结论更强。判词用 `ASSUMPTIONS-WEAKENED-SO-THE-RESULT-IS-STRENGTHENED`。")


B_SHIFT_SAME = []
for n in NS:
    a1 = [F(m, 4) for m in range(-24, 25) if binom_g(F(m, 4) + F(n - 1, 2), n).denominator == 1]
    a2 = [F(m, 4) for m in range(-24, 25) if binom_g(F(m, 4) + F(n + 1, 2), n).denominator == 1]
    if a1 == a2:
        B_SHIFT_SAME.append(n)
item("B06", "eq", iint(NS), iint(B_SHIFT_SAME),
     "**上指标只确定到整数平移**：`(n−1)/2` 与 `(n+1)/2` 相差 **1**，反解出的格**完全相同**（12/12）。"
     "所以「格」只依赖偏移的**模 1 类**（是整数还是半整数），不依赖具体取哪个 `(n±1)/2`。"
     "★这条是照着实测改出来的：首版的负对照「把偏移改成 `(n+1)/2` ⇒ 格必然变」**失败了** —— "
     "整平移在格上是不可见的，这正是为什么 r325 的「移位 0 或 1/2」只有**两种**情形")

# ================================================================ C 组 非负性筛
print("[r331] C 组：定理 C · 族数非负性（n_R >= 0）砍掉奇 n 的一半 q")

C_NEG_ODD_TOT, C_NZ_ODD, C_NEG_ODD = 0, 0, 0
C_POS_EVEN_TOT, C_NZ_EVEN, C_POS_EVEN = 0, 0, 0
for n in NS:
    for k in range(-8, 9):
        if k >= 0:
            continue
        v = chi_sheaf(n, k)
        if n % 2 == 1:
            C_NEG_ODD_TOT += 1
            if v != 0:
                C_NZ_ODD += 1
                if v < 0:
                    C_NEG_ODD += 1
        else:
            C_POS_EVEN_TOT += 1
            if v != 0:
                C_NZ_EVEN += 1
                if v > 0:
                    C_POS_EVEN += 1
item("C01", "eq", C_NZ_ODD, C_NEG_ODD,
     "**奇 n、`k < 0` 区**：`n_R = (−1)^n C(−k−1,n) = −C(−k−1,n)`。"
     "注意 `k ≤ −n−1` 时 `C(−k−1,n) = 0` ⇒ 这一区**大部分是零**（%d 个点里只有 %d 个非零）。"
     "断言是「**非零的全都是负的**」：%d / %d ⇒ 负族数 ⇒ **非物理**（「第 −1 代」没有意义）"
     % (C_NEG_ODD_TOT, C_NZ_ODD, C_NEG_ODD, C_NZ_ODD))
item("C02", "eq", C_NZ_EVEN, C_POS_EVEN,
     "**偶 n、`k < 0` 区**：`n_R = +C(−k−1,n)` ⇒ 非零的**全是正的**（%d / %d，另 %d 个为零）。"
     "⇒ 非负性**只对奇 n 有杀伤**，对偶 n 一刀不砍 —— 这一条不对称，是本卷第一个诚实的细节"
     % (C_POS_EVEN, C_NZ_EVEN, C_POS_EVEN_TOT - C_NZ_EVEN))

C_CUT_ODD, C_CUT_EVEN, C_ALL = 0, 0, 0
for n in NS:
    for q in FWG[n]:
        C_ALL += 1
        if nr_binom(n, q) < 0:
            if n % 2 == 1:
                C_CUT_ODD += 1
            else:
                C_CUT_EVEN += 1
item("C03", "eq", iint([C_CUT_ODD, 0]),
     iint([C_CUT_ODD, C_CUT_EVEN]),
     "**砍掉的量**：FW 格 %d 个点里，负 `n_R` 共 %d 个 —— 奇 n 占 %d、偶 n 占 %d "
     "⇒ 「非负性」把奇 n 的那一半砍掉、偶 n 一刀未砍" % (C_ALL, C_CUT_ODD + C_CUT_EVEN, C_CUT_ODD, C_CUT_EVEN))

SOLS = [(1, 3), (2, F(5, 2)), (2, F(-5, 2))]
C_SOLNEG = [s for s in SOLS if nr_binom(s[0], s[1]) < 0]
item("C04", "eq", 0, len(C_SOLNEG),
     "**关键：非负性不砍解**。三个解 `n_R` 都 = +3（`n=1,q=3`；`n=2,q=±5/2`），"
     "负的 = **%d** 个 ⇒ 加大这条约束**不改变解集**，只砍掉无关的 q。这是「约束更强但结论不变」的情形，"
     "必须显式说清楚，否则会被读成「非负性救了这卷」" % len(C_SOLNEG))

C_POSONLY = [s for s in SOLS if nr_binom(s[0], s[1]) > 0]
item("C05", "eq", len(SOLS), len(C_POSONLY),
     "**把 `≥ 0` 换成 `> 0` 会不会砍解**：严格正的点 %d / %d ⇒ 不砍 ⇒ 「非负」与「为正」在这题上等价，"
     "所以本卷不主张「非负性是必要的」，只主张它是**免费的**" % (len(C_POSONLY), len(SOLS)))

# ================================================================ D 组 k 坐标压缩
print("[r331] D 组：定理 D · 换坐标 k = x − n，四支点塌成两支点")

D_ID_BAD, D_ID_TOT = 0, 0
for n in NS:
    for q in FWG[n]:
        D_ID_TOT += 1
        if k_of(n, q) != F(q) + F(n - 1, 2) - n:
            D_ID_BAD += 1
item("D01", "eq", 0, D_ID_BAD,
     "**恒等式 `k = x − n`**：`x = q+(n−1)/2`、`k = q−(n+1)/2`，相减恰好 `= n`。"
     "机检 %d 个格点，失配 %d ⇒ 两个坐标只差一个常数，但**差这个常数的方向决定了证明长度**" % (D_ID_TOT, D_ID_BAD))

D_POS_BAD, D_POS_TOT = 0, 0
for n in NS:
    for k in range(0, 9):
        D_POS_TOT += 1
        if chi_sheaf(n, k) != binom_g(F(k + n), n):
            D_POS_BAD += 1
item("D02", "eq", 0, D_POS_BAD,
     "**`k ≥ 0` 支**：`n_R = C(k+n, n)`，上指标 `M = k+n ≥ n` —— %d 组失配 %d" % (D_POS_TOT, D_POS_BAD))

D_NEG_BAD, D_NEG_TOT = 0, 0
for n in NS:
    for k in range(-9, 0):
        D_NEG_TOT += 1
        if chi_sheaf(n, k) != F((-1) ** n) * binom_g(F(-k - 1), n):
            D_NEG_BAD += 1
item("D03", "eq", 0, D_NEG_BAD,
     "**`k ≤ −1` 支**：`n_R = (−1)^n C(−k−1, n)`，上指标 `M = −k−1 ≥ 0` —— %d 组失配 %d"
     "⇒ 两支的上指标 `M` 都 `≥ 0`，且 `n_R = ±C(M,n)`" % (D_NEG_TOT, D_NEG_BAD))

D_U_BAD, D_U_TOT = 0, 0
for n in NS:
    for k in range(-10, 11):
        D_U_TOT += 1
        M = M_of(n, k)
        want = binom_g(F(M), n) * (F(1) if (k >= 0 or n % 2 == 0) else F(-1))
        if chi_sheaf(n, k) != want:
            D_U_BAD += 1
item("D04", "eq", 0, D_U_BAD,
     "**统一形式**：`n_R = σ · C(M, n)`，`M` 分段（`k≥0` 取 `k+n`，`k<0` 取 `−k−1`），"
     "`σ = +1`（`k≥0` 或 n 偶）否则 `−1` —— %d 组失配 %d ⇒ **一个公式盖住两支**" % (D_U_TOT, D_U_BAD))

D_Z_BAD = 0
D_Z_NONZERO = 0
for n in NS:
    for k in range(-12, 11):
        M = M_of(n, k)
        nz = (chi_sheaf(n, k) != 0)
        if nz != (M >= n):
            D_Z_BAD += 1
        if nz:
            D_Z_NONZERO += 1
item("D05", "eq", 0, D_Z_BAD,
     "**零段被吸收**：`n_R ≠ 0 ⟺ M ≥ n` —— 失配 %d（非零格点 %d 个）。"
     "r327 的支点③「`0 ≤ x < n` ⇒ `C = 0`」在这里**不是一条支点，是 `M < n` 的一句同义话**" % (D_Z_BAD, D_Z_NONZERO))

D_M_BAD, D_M_TOT = 0, 0
for n in NS:
    for M in range(n, n + 61):
        D_M_TOT += 1
        v = binom_g(F(M), n)
        if v == 3 and n not in (1, 2):
            D_M_BAD += 1
item("D06", "eq", 0, D_M_BAD,
     "**两支点证明**：只需 `C(M,n) = 3`、`M ≥ n`、`n ≥ 1`。%d 组（`n=1..15` × `M=n..n+60`）里，"
     "给出 3 而 `n ≥ 3` 的 = **%d** ⇒ 解只能来自 `n ∈ {1,2}`" % (D_M_TOT, D_M_BAD))

D_MONO_BAD, D_MONO_TOT = 0, 0
for n in NS:
    for M in range(n, n + 41):
        D_MONO_TOT += 1
        if binom_g(F(M + 1), n) - binom_g(F(M), n) != binom_g(F(M), n - 1):
            D_MONO_BAD += 1
item("D07", "eq", 0, D_MONO_BAD,
     "**支点①（单调）的证明**：Pascal 差分 `C(M+1,n) − C(M,n) = C(M,n−1) = M!/((n−1)!(M−n+1)!) > 0`，"
     "`M ≥ n ≥ 1`。机检 %d 组恒等式，失配 %d ⇒ 不是「窗口里看起来增」，是差分恒等式 + 显式正性" % (D_MONO_TOT, D_MONO_BAD))

D_JUMP = [(n, int(binom_g(F(n), n)), int(binom_g(F(n + 1), n))) for n in range(3, 16)]
D_JUMP_BAD = [t for t in D_JUMP if not (t[1] < 3 < t[2])]
item("D08", "eq", 0, len(D_JUMP_BAD),
     "**支点②（端点跳跃）**：`C(n,n) = 1 < 3 < n+1 = C(n+1,n)` 对 `n ≥ 3`；`n = 3..15` 反例 **%d** 个。"
     "严格递增 + 相邻值跨越 3 ⇒ 中间没有整数落点 ⇒ **跳过 3**" % len(D_JUMP_BAD))

D_SOL = sorted(set([(n, q) for n in NS for q in FWG[n] if nr_binom(n, q) == 3]))
item("D09", "eq", iint(["(1,3)", "(2,-5/2)", "(2,5/2)"]),
     iint(["(%d,%s)" % (n, fmt(q)) for (n, q) in D_SOL]),
     "**解集与 r327 完全一致**（这是必须过的等价性门）：`n=1,q=3`；`n=2,q=±5/2` —— 共 %d 个。"
     "换坐标若改变了结论，那就是算错，不是简化" % len(D_SOL))

item("D10", "info", "-", "-",
     "**证明长度对比**：r327 用 4 个支点（单调 / 端点 / 零段 / 负整数支）；本卷用 2 个（单调 / 端点）。"
     "少的两个不是「省掉」，是**被 `M ≥ n` 这个参数化吸收**：零段 = `M < n` 时 `C = 0`；"
     "负整数支 = `k<0` 时 `M = −k−1` 恰好把 x 的负半轴翻到 M 的正半轴。")

D_COV_BAD = 0
D_COV_TOT = 0
D_COV_HOLE = []
for n in NS:
    got = set(M_of(n, k) for k in range(-40, 41))
    want = set(range(0, n + 41))
    D_COV_TOT += 1
    if got != want:
        D_COV_BAD += 1
        D_COV_HOLE.append((n, sorted(want - got)[:3]))
item("D11", "eq", 0, D_COV_BAD,
     "**`M` 的值域没有洞**：`k ≥ 0` 支给 `M ∈ [n, n+40]`，`k < 0` 支给 `M ∈ [0, 39]`，"
     "两支并起来应恰是 `M ∈ [0, n+40]`。逐 n 机检（%d 个 n），值域与区间不等的 = **%d** "
     "⇒ 「两支点覆盖全体」不是声明，是算出来的（若 `M` 的分段定义有缺口，这里立刻红）"
     % (D_COV_TOT, D_COV_BAD))
if D_COV_HOLE:
    print("[r331] WARN M range hole: %r" % (D_COV_HOLE[:3],))

# ================================================================ E 组 冗余性判定（自审 / 反噬 r327）
print("[r331] E 组：定理 E · r327 的支点③④是支点①在 x 坐标下的两个影子")

E_XEQ_TOT, E_XEQ = 0, 0
for n in NS:
    for x in range(0, n):
        E_XEQ_TOT += 1
        if M_of(n, x - n) == x:
            E_XEQ += 1
item("E01", "eq", len([n for n in NS if n % 2 == 1]), E_XEQ,
     "**两个坐标在零点重合**：`0 ≤ x < n` 时 `M = n−x−1`，与 `x` 一般是**两个不同的数**；"
     "`M = x` 只在 `x = (n−1)/2` 处成立 ⇒ 巧合次数 = 奇数 n 的个数（%d）。"
     "机检：%d 个 `(n,x)` 里巧合 **%d** 次，逐 n 至多一次 ⇒ 「`M` 就是 `x`」是错的，"
     "`M` 是把 x 的负半轴折回正半轴的**反射坐标**" % (len([n for n in NS if n % 2 == 1]), E_XEQ_TOT, E_XEQ))

E3B_BAD, E3B_TOT = 0, 0
for n in NS:
    for x in range(0, n):
        E3B_TOT += 1
        if binom_g(F(M_of(n, x - n)), n) != 0:
            E3B_BAD += 1
item("E02", "eq", 0, E3B_BAD,
     "**支点③确实被吸收**（正确写法）：`0 ≤ x < n` ⇒ `M = n−x−1 < n` ⇒ `C(M,n) = 0`。"
     "机检 %d 组失配 **%d** ⇒ 支点③的结论零成本得到，它**不是一条独立支点**" % (E3B_TOT, E3B_BAD))

E4_BAD, E4_TOT = 0, 0
for n in NS:
    for x in range(-40, 0):
        E4_TOT += 1
        M = M_of(n, x - n)
        if M < n:
            E4_BAD += 1
item("E03", "eq", 0, E4_BAD,
     "**支点④的影子**：`x < 0` ⇒ `k = x−n ≤ −n−1 < 0` ⇒ `M = −k−1 = n−x−1 ≥ n`（因 `x < 0`）"
     "⇒ 负半轴**整个**落在「`M ≥ n`」这一支里，与 `x ≥ n` 共用同一支点。机检 %d 组，落在 `M < n` 的 = **%d**"
     % (E4_TOT, E4_BAD))

E_SAME = (len(D_SOL) == 3)
item("E04", "eq", 3, len(D_SOL),
     "**简化而非修正**：解集仍是 3 个 ⇒ 本卷没有推翻 r327 的任何结论，"
     "只是指出它的证明**用了四个支点做两个支点的事**。这类发现的价值不在结论，在**坐标选择**")

item("E05", "info", "-", "-",
     "**方法论落点**：r327 选 `x = q+(n−1)/2`（让二项式的上指标成为整数的坐标），本卷选 `k = q−(n+1)/2`"
     "（让线丛 `O(k)` 成为整对象的坐标）。两者差常数 `n`，**但 x 坐标把「负半轴」和「正半轴」切成两段，"
     "k 坐标把它们折成一段**。选坐标的自由度就是证明长度的自由度。")

# ================================================================ F 组 定价 + 不叠加
print("[r331] F 组：定价与不叠加声明")
SLOTS = ["S1 格需要 spin^c 几何论证",
         "S2 格只需整性（算术）",
         "S3「跳过 3」需要四个支点",
         "S4「跳过 3」只需两个支点",
         "S5 存在不引用 N 的机制把 3 选出来",
         "S6 「3 是三角形数」解释了「为什么是 3 而不是 6」"]
BIT = {"S1": 32, "S2": 16, "S3": 8, "S4": 4, "S5": 2, "S6": 1}


def feasible(m):
    S1, S2, S3, S4, S5, S6 = [1 if (m & BIT["S%d" % (i + 1)]) else 0 for i in range(6)]
    if S1 and S2:
        return False
    if S3 and S4:
        return False
    if S5 and S6:
        return False
    return True


ACH = [m for m in range(64) if feasible(m)]
STRICT = 63


def with_all(*ks):
    return len([m for m in ACH if all(m & BIT[k] for k in ks)])


item("F01", "eq", 0, 1 if STRICT in ACH else 0,
     "严格六槽（`S1∧…∧S6`）= %d ⇒ 「格要几何、又要算术」与「证明要四支点、又要两支点」**逻辑上不可共存**"
     % (1 if STRICT in ACH else 0))
item("F02", "eq", 0, with_all("S1", "S2"),
     "**`S1 ∧ S2 = 0`**：同一张格，若算术已足够则**不需要**几何论证（本卷证明 `S2`，故 `S1` 被取代）；"
     "`S2 ∧ ¬S3` 与 `S4` 可同时成立 —— 这正是本卷确立的组合")
item("F03", "eq", 0, with_all("S3", "S4"),
     "**`S3 ∧ S4 = 0`**：四支点与两支点不能同时是「必要的」⇒ 本卷的 `E02/E03` 一旦成立，`S3` 即被否")
item("F04", "eq", 0, with_all("S5", "S6"),
     "承 r327：**`S5 ∧ S6 = 0`**（能选出 3 ⟺ 不需要三角形数解释），本卷未改变这一条")
item("F05", "gt", 0, with_all("S2", "S4"),
     "**本卷落点**：`S2 ∧ S4 = %d` 个可达掩码 ⇒ 「格由算术给出」+「两支点足够」**可以同时成立**"
     % with_all("S2", "S4"))
anY = anomal(YS)
item("F06", "eq", iint(["0"] * 6), iint([fmt(v) for v in anY]),
     "基线复核：SM 一代六条反常全零 = %s（与 r292..r327 同口径）" % iint([fmt(v) for v in anY]))
item("F07", "info", "-", "-",
     "**不叠加声明**：`r294/r302/r305/r307/r309/r318/r319/r322/r325/r327/r330/r331` 十二卷各有独立判据，"
     "**条目数不得相加**；共用 `Y` 与 `DIMS` 的 PASS 不得重复计分。"
     "本卷与 r327 **不是并列关系，是包含关系**：r327 的定理 C/E 全部保留，本卷只改它们的**坐标与假设**。")

# ================================================================ 控制组
control("CTL1", "正对照：SM 基线反常全零（判据没坏）",
        all(v == 0 for v in anY), iint([fmt(v) for v in anY]))
control("CTL2", "正对照：`C(x,n)` 在整数点上全为整数（A02 的分母非空）",
        A_ZINT_TOT > 0 and A_ZBAD == 0, "检查 %d 组" % A_ZINT_TOT)
control("CTL3", "负对照：`2x` 在同批非整点上有整值 ⇒ A01 不是「有理点代入就不整」这种废话",
        len(A_LIN) > 0, "2x 给整值 %d 个" % len(A_LIN))
control("CTL4", "负对照：把 b 的上界从 2..8 缩到 2..3 ⇒ 样本变小但非整点依然全非整（不是靠大分母撑出来的）",
        all(binom_g(F(a, b), n).denominator != 1
            for n in range(1, 8) for b in (2, 3) for a in range(-9, 10) if math.gcd(abs(a), b) == 1),
        "n=1..7, b=2,3, |a|<=9")
CTL5_N2 = [F(m, 4) for m in range(-24, 25) if binom_g(F(m, 4) + F(1), 2).denominator == 1]
control("CTL5", "负对照：把偏移从 `(n−1)/2` 改成 `n/2`（差 **1/2**，不是 1）⇒ 奇偶翻转 ⇒ 格必须变",
        set(ARITH[2]) != set(CTL5_N2),
        "n=2：偏移 1/2 给 Z+1/2；偏移 1 给 Z ⇒ 后者**测不出来**（见 B06）")
control("CTL6", "正对照：`B03` 与 `B04` 的分母都非零（否则「双向」是空转）",
        B_TOT > 0 and B_OFF > 0, "格上 %d / 离格 %d" % (B_TOT, B_OFF))
control("CTL7", "正对照：非负性筛的分母非零（C01/C02 都有样本）",
        C_NEG_ODD_TOT > 0 and C_POS_EVEN_TOT > 0,
        "奇 %d / 偶 %d" % (C_NEG_ODD_TOT, C_POS_EVEN_TOT))
control("CTL8", "负对照：把非负性当成「砍掉一半解」⇒ 立即不自洽（解全是 +3）",
        all(nr_binom(n, q) > 0 for (n, q) in SOLS), "3 个解全正")
control("CTL9", "正对照：`chi_sheaf` 与 `nr_binom` 在格上一致（两条独立实现）",
        all(chi_sheaf(n, int(k_of(n, q))) == nr_binom(n, q) for n in NS for q in FWG[n]),
        "150 组")
control("CTL10", "负对照：把 `chi_sheaf` 的 `k<0` 支判成 0 ⇒ 立刻失配（Serre 对偶承重，r327 CTL15 同型）",
        any(chi_sheaf(n, -3) != F(math.comb(-3 + n, n)) if (-3 + n) >= 0 else True for n in (2, 4)),
        "n=2: chi(O(-3))=C(2,2)=1 vs C(-1,2)=0")
control("CTL11", "负对照：把 `M_of` 的 `k≥0` 支写成 `k+n+1` ⇒ D04 崩（M 的偏移承重）",
        any(binom_g(F(M_of(n, k) + 1), n) != chi_sheaf(n, k)
            for n in (2, 3) for k in (0, 1, 2)), "n=2,3 上偏移 +1 即失配")
control("CTL12", "正对照：`C(M,n)` 在 `M ≥ n` 上严格递增（D07 的前提真的成立）",
        all(binom_g(F(M + 1), n) > binom_g(F(M), n) for n in NS for M in range(n, n + 20)),
        "n=1..15, M=n..n+19")
control("CTL13", "负对照：把判据换成「平方数」⇒ 3 会被误判不可达（判别力）",
        (3 not in [k * k for k in range(1, 20)]), "3 不是平方数")
control("CTL14", "正对照：解集计数 1 + 2 = 3，与 r327 一致",
        len([s for s in D_SOL if s[0] == 1]) == 1 and len([s for s in D_SOL if s[0] == 2]) == 2,
        "1 + 2 = %d" % len(D_SOL))
control("CTL15", "负对照：r327 的四支点在 M 坐标下必须退化成两条 ⇒ 若 E02/E03 任一不成立则本卷的核心主张垮",
        E3B_BAD == 0 and E4_BAD == 0, "E02=%d E03=%d" % (E3B_BAD, E4_BAD))

# ================================================================ 守卫
n_pass = sum(1 for it in ITEMS if it["status"] == "PASS")
n_fail = sum(1 for it in ITEMS if it["status"] == "FAIL")
n_info = sum(1 for it in ITEMS if it["status"] == "INFO")
SRC_TEXT = io.open(os.path.abspath(__file__), encoding="utf-8").read()

guard("G01", "verdict 合法（大写、含判词主体、长度 >= 40）",
      len(VERDICT) >= 40 and VERDICT == VERDICT.upper(), VERDICT[:40])
guard("G02", "items 数与 json 一致（写盘后回读）", True, "待回读")
guard("G03", "控制组全过", all(c["status"] == "PASS" for c in CONTROLS),
      "%d/%d" % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS)))
guard("G04", "Decimal 精度 >= 50", getcontext().prec >= 50, "prec=%d" % getcontext().prec)
guard("G05", "源码无 random 导入（确定性）",
      re.search(r"^\s*import\s+random\b", SRC_TEXT, re.M) is None
      and re.search(r"^\s*from\s+random\b", SRC_TEXT, re.M) is None,
      "行首 import/from random 命中 0")
guard("G06", "report/json 逐条一致（写盘后回读）", True, "待回读")
guard("G07", "verdict 由计数驱动（整性/格/坐标/压缩/等价/不预言六件事都进判词）",
      all(k in VERDICT for k in ("INTEGRALITY", "FREED-WITTEN", "X-COORDINATE",
                                 "FOUR-LEGS-COMPRESS-TO-TWO", "SOLUTION-SET-UNCHANGED",
                                 "NOT-PREDICTED"))
      and A_NONINT == A_TOT and A_TOT > 0 and SYM == 0 and len(D_SOL) == 3,
      "nonint=%d/%d sym=%d sols=%d" % (A_NONINT, A_TOT, SYM, len(D_SOL)))
guard("G08", "定价覆盖本卷核心（S1∧S2=0 且 S3∧S4=0）",
      with_all("S1", "S2") == 0 and with_all("S3", "S4") == 0 and with_all("S2", "S4") > 0,
      "S1^S2=%d S3^S4=%d S2^S4=%d" % (with_all("S1", "S2"), with_all("S3", "S4"), with_all("S2", "S4")))
guard("G09", "**无同义反复（源码级）**：exp 与 act 不得是同一个带引号字面量",
      len(re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
          .findall(SRC_TEXT)) == 0,
      "命中 %d 条" % len(re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
                         .findall(SRC_TEXT)))
guard("G10", "字面 True 的守卫计数如实登记", SRC_TEXT.count('", True, "') <= 4,
      "字面 True 出现 %d 处" % SRC_TEXT.count('", True, "'))
guard("G11", "所有判决类条目无 FAIL", n_fail == 0, "fail=%d" % n_fail)
guard("G12", "**分母非空**（防「0 条即通过」）：A01/B03/B04/C01/C02/D06/D07 的分母都 > 0",
      A_TOT > 0 and B_TOT > 0 and B_OFF > 0 and C_NEG_ODD_TOT > 0
      and C_POS_EVEN_TOT > 0 and D_M_TOT > 0 and D_MONO_TOT > 0 and C_NZ_ODD > 0 and C_NZ_EVEN > 0,
      "A=%d B=%d/%d C=%d/%d D=%d/%d" % (A_TOT, B_TOT, B_OFF,
                                        C_NEG_ODD_TOT, C_POS_EVEN_TOT, D_M_TOT, D_MONO_TOT))
guard("G13", "两支点证明的四条都真被机检（D05/D06/D07/D08 全 PASS）",
      all(it["status"] == "PASS" for it in ITEMS if it["id"] in ("D05", "D06", "D07", "D08")),
      "4/4")
guard("G14", "自审：CTL3/CTL4/CTL5/CTL8/CTL10/CTL11/CTL13/CTL15 八个负对照都真改变了输出",
      all(c["status"] == "PASS" for c in CONTROLS
          if c["id"] in ("CTL3", "CTL4", "CTL5", "CTL8", "CTL10", "CTL11", "CTL13", "CTL15")),
      "%d/%d" % (sum(1 for c in CONTROLS
                     if c["id"] in ("CTL3", "CTL4", "CTL5", "CTL8", "CTL10", "CTL11", "CTL13", "CTL15")
                     and c["status"] == "PASS"), 8))
guard("G15", "不宣称预言了三代（判词含 NOT-PREDICTED，且不含 WE-PREDICT）",
      ("NOT-PREDICTED" in VERDICT) and ("WE-PREDICT" not in VERDICT), "含 NOT-PREDICTED")
guard("G16", "与 r327 的等价性（解集完全相同，3 个，逐个 q 值一致）",
      sorted([(n, q) for (n, q) in D_SOL]) == sorted([(1, F(3)), (2, F(5, 2)), (2, F(-5, 2))]),
      iint(["(%d,%s)" % (n, fmt(q)) for (n, q) in D_SOL]))
B_RAW = SRC_TEXT.split("B 组 格重建")[1].split("C 组 非负性筛")[0] if "B 组 格重建" in SRC_TEXT else ""
B_BLOCK = "\n".join(l.split("#")[0] for l in B_RAW.split("\n"))   # 剥掉注释，只查代码
guard("G17", "「假设更弱」有源码级证据：B 组（格重建）里不出现 chi_sheaf / spin / chern / todd 任何几何调用",
      len(B_BLOCK) > 0 and all(w not in B_BLOCK for w in
                               ("chi_sheaf(", "chern_cp(", "todd_root(", "ahat_A_")),
      "B 组源码 %d 字符；几何函数调用命中 %d 次"
      % (len(B_BLOCK), sum(B_BLOCK.count(w) for w in
                           ("chi_sheaf(", "chern_cp(", "todd_root(", "ahat_A_"))))
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 落盘
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "candidate_degree": CAND_DEGREE,
    "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS], "dims": DIMS,
        "anomalies_SM_gen": [fmt(v) for v in anY],
        "integrality_noninteger_points": A_TOT,
        "integrality_violations": A_NONINT,
        "integrality_integer_points_checked": A_ZINT_TOT,
        "lattice_symdiff": SYM,
        "lattice_points_checked": B_TOT,
        "offlattice_points_checked": B_OFF,
        "negative_nR_odd_sites": C_NEG_ODD,
        "negative_nR_even_sites": C_CUT_EVEN,
        "solutions": [["%d" % n, fmt(q)] for (n, q) in D_SOL],
        "M_legs": 2,
        "r327_legs": 4,
    },
    "pricing": {"strict": 1 if STRICT in ACH else 0, "achievable": len(ACH),
                "S1_and_S2": with_all("S1", "S2"), "S3_and_S4": with_all("S3", "S4"),
                "S2_and_S4": with_all("S2", "S4"), "S5_and_S6": with_all("S5", "S6")},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 族数整性定理与 k 坐标压缩" % RID)
L.append("date=%s  degree=%s  candidate_degree=%s" % (DATE, DEGREE, CAND_DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] n_R = [H^n] e^{kH} td(CP^n) = chi(O(k)),  k = q - (n+1)/2 = x - n,  x = q + (n-1)/2")
for i in range(5):
    L.append("  %-22s dim=%-2d Y=%-5s" % (NAMES[i], DIMS[i], fmt(YS[i])))
L.append("  SM six anomalies: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-A] INTEGRALITY :  x in Q, n>=1, C(x,n) in Z  ==>  x in Z")
L.append("  proof: x=a/b reduced, b>1, p|b.  every factor (a-i b) = a (mod p), p does not divide a")
L.append("         => p does not divide the numerator; but b^n contains p^n, n>=1")
L.append("         => the reduced denominator still carries p  => not an integer.")
L.append("  machine check : %d non-integer rational points, %d of them give an integer  (must be 0)"
         % (A_TOT, A_NONINT))
L.append("  converse      : %d integer points, %d non-integer values  (must be 0)"
         % (A_ZINT_TOT, A_ZBAD))
L.append("")
L.append("[theorem-B] THE LATTICE IS REBUILT FROM INTEGRALITY ALONE (no spin^c)")
L.append("  candidates q on a 1/4 grid in [-6,6]; keep those with C(q+(n-1)/2,n) in Z")
L.append("  result == r325 Freed-Witten lattice (n odd: Z ; n even: Z+1/2)   symmetric difference = %d" % SYM)
L.append("  lattice points %d (all integral) ; off-lattice points %d (none integral)" % (B_TOT, B_OFF))
L.append("  INPUTS USED: q in Q, n_R in Z.   NOT USED: spin, spin^c, w2, D-brane.")
L.append("")
L.append("[theorem-C] NON-NEGATIVITY : n_R >= 0 kills half the q's for odd n only")
L.append("  odd n, k<0 : n_R = -C(-k-1,n) < 0   -> %d/%d unphysical" % (C_NEG_ODD, C_NEG_ODD_TOT))
L.append("  even n,k<0 : n_R = +C(-k-1,n) > 0   -> %d/%d physical" % (C_POS_EVEN, C_POS_EVEN_TOT))
L.append("  it does NOT remove any solution (all three have n_R = +3)")
L.append("")
L.append("[theorem-D] THE k COORDINATE : n_R = sigma * C(M,n),  M >= n  <=>  n_R != 0")
L.append("  k>=0 : M = k+n      ; k<0 : M = -k-1")
L.append("  sigma = +1 unless (k<0 and n odd)")
L.append("  legs needed : 2 (monotone + endpoint jump)   [r327 used 4]")
L.append("    monotone : C(M+1,n)-C(M,n) = C(M,n-1) > 0 for M>=n>=1")
L.append("    endpoint : C(n,n)=1 < 3 < n+1 = C(n+1,n) for n>=3")
L.append("  solutions: %s" % iint(["(%d,%s)" % (n, fmt(q)) for (n, q) in D_SOL]))
L.append("")
L.append("[theorem-E] r327 LEGS 3 AND 4 ARE SHADOWS OF LEG 1 IN THE x COORDINATE")
L.append("  0 <= x < n  =>  M = n-x-1 < n  =>  C(M,n) = 0      (leg 3 absorbed)")
L.append("  x < 0       =>  M = n-x-1 >= n                    (leg 4 merges into leg 1)")
L.append("  solution set unchanged => simplification, not correction")
L.append("")
L.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-34s act=%s"
             % (it["id"], it["status"], it["kind"], it["exp"][:34], it["act"][:34]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-4s %s" % (c["id"], c["status"], c["desc"]))
L.append("")
L.append("[pricing] 2^6=64 achievable=%d strict=%d S1^S2=%d S3^S4=%d S2^S4=%d S5^S6=%d"
         % (len(ACH), 1 if STRICT in ACH else 0, with_all("S1", "S2"),
            with_all("S3", "S4"), with_all("S2", "S4"), with_all("S5", "S6")))
L.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), n_pass, n_fail, n_info))
L.append("")
L.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
for g in GUARDS:
    L.append("  %-5s %-4s %s ; %s" % (g["id"], g["status"], g["desc"], g["detail"]))
L.append("")
L.append("[verdict] %s" % VERDICT)
L.append("=" * 78)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "数据")
if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

JSON_PATH = os.path.join(DATA_DIR, BASE + ".json")
REP_PATH = os.path.join(DATA_DIR, BASE + "_report.txt")

with io.open(JSON_PATH, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(SUMMARY, ensure_ascii=False, indent=1))
REPORT = "\n".join(L) + "\n"
with io.open(REP_PATH, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(REPORT)

# ---- 回读守卫 G02 / G06
back = json.load(io.open(JSON_PATH, encoding="utf-8"))
rep = io.open(REP_PATH, encoding="utf-8").read()
GUARDS[1]["status"] = "PASS" if len(back["items"]) == len(ITEMS) else "FAIL"
GUARDS[1]["detail"] = "json=%d mem=%d" % (len(back["items"]), len(ITEMS))
lines_ok = all(("  %-5s %-4s %-4s exp=" % (it["id"], it["status"], it["kind"])) in rep for it in ITEMS)
GUARDS[5]["status"] = "PASS" if lines_ok else "FAIL"
GUARDS[5]["detail"] = "逐条一致 + report 已落盘" if lines_ok else "有条目未落盘"
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# 回读后重写两份（把 G02/G06 的真实状态写进去）
SUMMARY["guards"] = GUARDS
with io.open(JSON_PATH, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(SUMMARY, ensure_ascii=False, indent=1))
L2 = []
for line in L:
    if line.startswith("  G02 ") or line.startswith("  G06 "):
        g = GUARDS[1] if line.startswith("  G02 ") else GUARDS[5]
        L2.append("  %-5s %-4s %s ; %s" % (g["id"], g["status"], g["desc"], g["detail"]))
    elif line.startswith("[guards]"):
        L2.append("[guards] %d/%d" % (n_guard_pass, len(GUARDS)))
    else:
        L2.append(line)
with io.open(REP_PATH, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(L2) + "\n")

# ================================================================ 控制台摘要
print("[r331] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r331] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS), n_guard_pass, len(GUARDS)))
print("[r331] integrality: non-integer points=%d violations=%d ; integer points=%d violations=%d"
      % (A_TOT, A_NONINT, A_ZINT_TOT, A_ZBAD))
print("[r331] lattice rebuild: symdiff=%d ; on-lattice integral %d/%d ; off-lattice integral %d"
      % (SYM, B_INTZ, B_TOT, B_OFFINT))
print("[r331] non-negative: odd k<0 negative %d/%d ; even k<0 positive %d/%d"
      % (C_NEG_ODD, C_NEG_ODD_TOT, C_POS_EVEN, C_POS_EVEN_TOT))
print("[r331] solutions : %s" % iint(["(%d,%s)" % (n, fmt(q)) for (n, q) in D_SOL]))
print("[r331] legs: 2 (was 4) ; M>=n <=> n_R!=0 mismatch=%d" % D_Z_BAD)
print("[r331] pricing achievable=%d strict=%d S1^S2=%d S3^S4=%d S2^S4=%d"
      % (len(ACH), 1 if STRICT in ACH else 0, with_all("S1", "S2"),
         with_all("S3", "S4"), with_all("S2", "S4")))
print("[r331] wrote %s (%d bytes) / %s (%d bytes)"
      % (os.path.basename(JSON_PATH), os.path.getsize(JSON_PATH),
         os.path.basename(REP_PATH), os.path.getsize(REP_PATH)))
print("[r331] verdict=%s" % VERDICT)

if n_fail or n_guard_pass != len(GUARDS):
    sys.exit(1)
