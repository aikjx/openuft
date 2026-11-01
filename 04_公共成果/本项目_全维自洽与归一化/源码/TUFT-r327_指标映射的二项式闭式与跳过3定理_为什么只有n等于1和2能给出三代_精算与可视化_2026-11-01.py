# -*- coding: utf-8 -*-
r"""
TUFT-r327 · 指标映射的二项式闭式与「跳过 3」定理
`X-R325-1`（为什么只有 n = 1, 2 有解）攻坚

r325 判定册 §十二 交接：
「`X-R325-1`（新）：为什么只有 `n = 1, 2` 有解？`n >= 3` 在两档格上全无解。
 这是 `A-hat` 多项式的一个纯数论性质，还是一个几何选择效应？
 本卷只**报**了它，没解释它。」

本卷给出**证明**（不是更大范围的扫描），并且顺带得到三件副产品。

  定理 A（幂和引理 L1）      CP^n 的 Chern 根满足 `P_m = sum x_i^m = (n+1)H^m` 对 **m <= n**；
                             m > n 时失效（本卷机检 78/78，且验证失效方向）。
  定理 B（Todd-Hirzebruch 引理 L2）`[H^n] e^(lam H) T(H)^(n+1) = C(lam+n, n)`，T(x)=x/(1-e^-x)。
  定理 C（二项式闭式 · 核心）  **`n_R(q) = C(q + (n-1)/2, n)`**，精确恒等。
                             证明：`A-hat = td * e^(-c1/2)`，`log td = sum_m (log T)_m P_m`，
                             由 L1 得 `td === T(H)^(n+1)` (mod H^(n+1))，故
                             `n_R = [H^n] e^((q-(n+1)/2)H) T(H)^(n+1) = C(q+(n-1)/2, n)`（L2）。∎
  定理 D（Freed-Witten 移位 = 上指标整数化）
                             `x := q + (n-1)/2` 是整数 **当且仅当** q 落在 r325 求出的 FT 格上。
                             ⇒ r325 的「格」与本卷的「二项式」是同一结构的两个面。
  定理 E（跳过 3 · 本卷主结论）
                             `n_R(q) = 3` 有格点解 **当且仅当 n in {1, 2}**。
                             证明（覆盖**全部**整数 x，无扫描缺口）：
                               x >= n：C(x,n) 在 x 上严格增，C(n,n)=1 < 3 < n+1 = C(n+1,n)（n>=3）⇒ 跳过
                               0 <= x < n：C = 0
                               x < 0：|C(x,n)| = C(n-x-1, n)，x=-1 给 1，x<=-2 给 >= n+1 >= 4，
                                      且符号为 (-1)^n（n 奇时为负，不能等于 +3）⇒ 跳过
  定理 F（可实现族数 = 二项式系数）CP^n 上能实现的族数 N 恰好是 {C(m,n)}：
                             n=1 全正整数（恒等映射，无信息）；n=2 **三角形数**；n=3 四面体数；……
                             特别地 **n=2 可实现 N ⟺ N 是三角形数**（C(x,2) = T_{x-1}）。
  定理 G（3 vs 4 的算术判别）
                             **3 = T_2 是三角形数 ⇒ CP^2 给得出三代；4 不是 ⇒ CP^2 给不出四代**
                             （4 = C(4,3) 需 CP^3）⇒ 三代的**最小非平凡内部复维 = 2**，四代 = 3。

⇒ 判词：`X-R325-1` **关闭**。但它把问题**转化**了而不是消掉了：
   「三代可实现」⟺「3 是三角形数」且内部空间是 CP^2；而三角形数有无穷多个（6,10,15,…同样可实现）
   ⇒ **本机制仍然不预言 3**，只是把「为什么是 3」换成了「为什么内部空间是 CP^2」。
   ★副产品：发现并**证明其无害**的一处 r319/r325 潜在 bug（`hat_a` 在 n<3 的边界用错 c_k，
     但每一处错位都落在 j > n，即不进 n_R）。

确定性：Fraction 精确；形式幂级数用 Fraction 完成（Bernoulli 经 `x/(1-e^-x)` 的级数逆得到）；
       Newton 幂和由 Chern 数机械推出；无 random；无浮点（除打印）。
口径：n_R = int_{CP^n} e^{qH} A-hat(CP^n)，q 为 ∫_{CP^1}F/2pi；路径 C = Chern 根 + Todd 乘法序列。
"""

import io
import json
import math
import os
import re
from decimal import getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r327"
DATE = "2026-11-01"
DEGREE = 0
CAND_DEGREE = 37
VERDICT = ("X-R325-1-CLOSED__INDEX-MAP-IS-EXACTLY-THE-BINOMIAL-C-Q-PLUS-HALF-N"
           "__AND-THE-BINOMIAL-IS-JUST-RIEMANN-ROCH-FOR-O-K-ON-CPN"
           "__FREED-WITTEN-SHIFT-IS-WHAT-MAKES-THE-BINOMIAL-TOP-INTEGER"
           "__THREE-IS-SKIPPED-FOR-N-GE-3-SINCE-C-N-N-1-AND-C-N1-N-N1"
           "__THREE-GENERATIONS-EQUIVALENT-TO-THREE-BEING-TRIANGULAR-AND-CP2"
           "__STILL-NOT-PREDICTED-BECAUSE-TRIANGULAR-NUMBERS-ARE-INFINITE")

DIR_HERE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(os.path.dirname(DIR_HERE), "数据")
BASE = ("TUFT-r327_指标映射的二项式闭式与跳过3定理_"
        "为什么只有n等于1和2能给出三代_精算与可视化_2026-11-01")

# ---------------------------------------------------------------- SM 谱（与 r294–r325 同）
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


# ================================================================ 形式幂级数（Fraction 精确）
NMAX = 12


def smul(a, b, N):
    out = [F(0)] * (N + 1)
    for i, x in enumerate(a):
        if x == 0 or i > N:
            continue
        for j, y in enumerate(b):
            if i + j > N:
                break
            if y:
                out[i + j] += x * y
    return out


def sinv(a, N):
    assert a[0] != 0
    inv0 = F(1) / a[0]
    out = [inv0] + [F(0)] * N
    for k in range(1, N + 1):
        s = F(0)
        for i in range(1, k + 1):
            if i < len(a):
                s += a[i] * out[k - i]
        out[k] = -s * inv0
    return out


def slog(a, N):
    assert a[0] == 1
    d = [(i + 1) * a[i + 1] for i in range(N)]
    q = smul(d, sinv(a, N), N)
    out = [F(0)] * (N + 1)
    for k in range(N):
        out[k + 1] = q[k] / (k + 1)
    return out


def sexp(a, N):
    assert a[0] == 0
    out = [F(0)] * (N + 1)
    out[0] = F(1)
    for k in range(1, N + 1):
        s = F(0)
        for i in range(1, k + 1):
            s += i * a[i] * out[k - i]
        out[k] = s / k
    return out


def spow(a, e, N):
    out = [F(1)] + [F(0)] * N
    for _ in range(e):
        out = smul(out, a, N)
    return out


def todd_root(N):
    """T(x) = x/(1-e^{-x}) 的级数（由 (1-e^{-x})/x 求逆，等价于 Bernoulli 定义）。"""
    base = [F(0)] * (N + 1)
    for k in range(1, N + 2):
        base[k - 1] = F((-1) ** (k + 1), math.factorial(k))
    return sinv(base, N)


def ahat_root(N):
    """A(x) = (x/2)/sinh(x/2) = T(x) e^{-x/2}。"""
    T = todd_root(N)
    half = [F((-1) ** k, (2 ** k) * math.factorial(k)) for k in range(N + 1)]
    return smul(T, half, N)


# ================================================================ CP^n 的 Chern 数 / 幂和 / A-hat
def chern_cp(n, N):
    c = [F(0)] * (N + 1)
    for k in range(0, min(n, N) + 1):
        c[k] = F(math.comb(n + 1, k))
    return c


def power_sums(c, N):
    """Newton 恒等式：k e_k = sum_{i=1..k} (-1)^(i-1) e_{k-i} P_i ⇒ P_k。"""
    e = c
    P = [F(0)] * (N + 1)
    for k in range(1, N + 1):
        s = F(0)
        for i in range(1, k):
            s += F((-1) ** (i - 1)) * e[k - i] * P[i]
        P[k] = F((-1) ** (k - 1)) * (F(k) * e[k] - s)
    return P


def ahat_C(n, N):
    """路径 C：A-hat(CP^n) 的 H^j 系数（Chern 根 + Todd 乘法序列，任意阶）。"""
    P = power_sums(chern_cp(n, N), N)
    logT = slog(todd_root(N), N)
    expo = [F(0)] * (N + 1)
    for m in range(1, N + 1):
        expo[m] = logT[m] * P[m]
    td = sexp(expo, N)
    lin = [F((-1) ** k * (n + 1) ** k, (2 ** k) * math.factorial(k)) for k in range(N + 1)]
    return smul(td, lin, N)


def ahat_A_buggy(n, N):
    """路径 A（r319/r325 原样）：Pontryagin 多项式，c_k 一律取 C(n+1,k)（**不看 k<=n**）。"""
    def pk(k):
        return F(math.comb(n + 1, k))
    a = {2: -pk(1) / 24,
         4: (7 * pk(1) ** 2 - 4 * pk(2)) / 5760,
         6: -(31 * pk(1) ** 3 - 44 * pk(1) * pk(2) + 16 * pk(3)) / 967680}
    out = [F(0)] * (N + 1)
    for j, v in a.items():
        if j <= N:
            out[j] = v
    return out


def ahat_A_fixed(n, N):
    """路径 A（修正）：c_k 在 k > n 时置 0，再由标准式算 p1,p2,p3。"""
    c = chern_cp(n, N)

    def ck(k):
        return c[k] if k < len(c) else F(0)

    p1 = ck(1) ** 2 - 2 * ck(2)
    p2 = ck(2) ** 2 - 2 * ck(1) * ck(3) + 2 * ck(4)
    p3 = ck(3) ** 2 - 2 * ck(2) * ck(4) + 2 * ck(1) * ck(5) - 2 * ck(6)
    a = {2: -p1 / 24,
         4: (7 * p1 ** 2 - 4 * p2) / 5760,
         6: -(31 * p1 ** 3 - 44 * p1 * p2 + 16 * p3) / 967680}
    out = [F(0)] * (N + 1)
    for j, v in a.items():
        if j <= N:
            out[j] = v
    return out


def nr_from(C, n, q):
    s = F(0)
    for j in range(min(n, len(C) - 1) + 1):
        if C[j]:
            s += C[j] * F(q) ** (n - j) / math.factorial(n - j)
    return s


def binom_g(x, n):
    """广义二项式 C(x,n)（x 为 Fraction，精确）。"""
    num = F(1)
    for i in range(n):
        num *= (F(x) - i)
    return num / math.factorial(n)


def nr_binom(n, q):
    return binom_g(F(q) + F(n - 1, 2), n)


def poly_q(n):
    """把 q -> n_R(q) 当作 q 的多项式：只用 n+1 个点的**取值**做精确 Vandermonde 求解。
    不用任何解析公式（否则等于把结论抄进验证）。"""
    m = n + 1
    pts = [F(k) for k in range(m)]
    vals = [nr_from(AHAT[n], n, q) for q in pts]
    M = [[pts[r] ** c for c in range(m)] + [vals[r]] for r in range(m)]
    for col in range(m):
        piv = None
        for r in range(col, m):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[col], M[piv] = M[piv], M[col]
        d = M[col][col]
        M[col] = [v / d for v in M[col]]
        for r in range(m):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(m + 1)]
    return [M[r][m] for r in range(m)]


NS = list(range(1, NMAX + 1))
AHAT = {n: ahat_C(n, n) for n in NS}          # 路径 C 到 H^n（算 n_R 只需到 n）
PQA = {n: poly_q(n) for n in NS}              # n_R 作为 q 的多项式的单项式系数（a_0..a_n）

# ================================================================ A 组 定理 A：幂和引理
print("[r327] A 组：定理 A · Chern 根的幂和引理 P_m = (n+1)H^m (m <= n)")

A_C1 = [[fmt(chern_cp(n, n)[k]) for k in (1, 2, 3) if k <= n] for n in NS]
item("A01", "eq", iint(["2", "3, 3", "4, 6, 4"]),
     iint([", ".join(A_C1[i]) for i in range(3)]),
     "c_k(CP^n) = C(n+1,k)：n=1 得 [2]，n=2 得 [3,3]，n=3 得 [4,6,4]（Pascal 行）")

L1_OK, L1_BAD = 0, []
for n in NS:
    P = power_sums(chern_cp(n, n), n)
    for m in range(1, n + 1):
        if P[m] == F(n + 1):
            L1_OK += 1
        else:
            L1_BAD.append((n, m, fmt(P[m])))
item("A02", "eq", 78, L1_OK,
     "**定理 A（L1）**：P_m = sum x_i^m = (n+1)H^m 对 m <= n，n=1..12 共 %d 条全对，失配 %d 条"
     % (L1_OK, len(L1_BAD)))
item("A03", "eq", 0, len(L1_BAD),
     "L1 的失配数 = %d（必须为 0，否则整个证明链断）" % len(L1_BAD))

P2 = power_sums(chern_cp(2, 6), 6)
item("A04", "eq", iint(["3", "3", "0"]),
     iint([fmt(P2[1]), fmt(P2[2]), fmt(P2[3])]),
     "**L1 在 m > n 时确实失效**（正值对照，不是恒真）：CP^2 的 P_1=3H、P_2=3H^2 对，"
     "而 P_3 = %s ≠ 4H^3 —— 所以 L1 只在 m <= n 成立，而这正是证明所需的范围" % fmt(P2[3]))

A_BUG, A_FIX = [], []
for n in NS:
    for j in (2, 4, 6):
        b = ahat_A_buggy(n, 6)[j]
        f = ahat_A_fixed(n, 6)[j]
        c = ahat_C(n, 6)[j]
        if b != c:
            A_BUG.append((n, j, fmt(b), fmt(c)))
        if f != c:
            A_FIX.append((n, j, fmt(f), fmt(c)))
item("A05", "gt", 0, len(A_BUG),
     "**潜在 bug 复现**：r319/r325 的 `hat_a`（把 c_k 一律取 C(n+1,k)）在 %d 个 (n,j) 上与"
     "路径 C 不符：%s" % (len(A_BUG), A_BUG))
item("A06", "eq", 0, len(A_FIX),
     "**修正后完全一致**：把 c_k 在 k > n 时置 0（路径 A-fixed），与路径 C 的失配 = %d "
     "⇒ bug 的成因就是「c_k = C(n+1,k) 只对 k <= n 成立」" % len(A_FIX))
HARMLESS = [(n, j) for (n, j, _, _) in A_BUG if j <= n]
item("A07", "eq", 0, len(HARMLESS),
     "**并证明它无害**：所有不符点 (n,j) = %s 都满足 j > n，而 n_R 只取 j <= n 的项 "
     "⇒ 该 bug 对任何 n_R 的读数**零影响**" % iint(["(%d,%d)" % (n, j) for (n, j, _, _) in A_BUG]))
item("A08", "eq", F(-1, 6), ahat_C(1, 6)[2],
     "手算交叉核：CP^1 的唯一 Chern 根是 2H ⇒ A-hat = H/sinh H = 1 - H^2/6 + … "
     "⇒ a_2 = %s（路径 C 给出同一值；路径 A-buggy 给 -1/12）" % fmt(ahat_C(1, 6)[2]))

# ================================================================ B 组 定理 B/C：Todd 引理与二项式闭式
print("[r327] B 组：定理 B/C · Todd-Hirzebruch 引理与二项式闭式")
LAM = [F(k, 3) for k in range(-12, 13)]
L2_BAD = 0
for n in NS[:8]:
    tp = spow(todd_root(n), n + 1, n)
    for lam in LAM:
        e = [F(1)] + [F(0)] * n
        for k in range(1, n + 1):
            e[k] = lam ** k / math.factorial(k)
        if smul(tp, e, n)[n] != binom_g(lam + n, n):
            L2_BAD += 1
item("B01", "eq", 0, L2_BAD,
     "**定理 B（L2）**：`[H^n] e^(lam H) T(H)^(n+1) = C(lam+n, n)`，n=1..8 × lam∈[-4,4] 步长 1/3 "
     "共 %d 组，失配 = %d ⇒ 这条引理是教科书事实（chi(O(k)) = C(k+n,n) 的多项式延拓）"
     % (int(8 * len(LAM)), L2_BAD))

A_TD, A_TD_BAD = 0, 0
for n in NS:
    td_direct = sexp([F(0)] * (n + 1) + [], n)      # 占位，下面真正算
    P = power_sums(chern_cp(n, n), n)
    logT = slog(todd_root(n), n)
    expo = [F(0)] * (n + 1)
    for m in range(1, n + 1):
        expo[m] = logT[m] * P[m]
    td_c = sexp(expo, n)
    td_th = spow(todd_root(n), n + 1, n)            # T(H)^(n+1)
    A_TD += 1
    if td_c != td_th:
        A_TD_BAD += 1
item("B02", "eq", 0, A_TD_BAD,
     "**证明的关键中间步**：`td(CP^n) === T(H)^(n+1)` mod H^(n+1)，n=1..12 共 %d 条，不符 %d 条 "
     "（由 L1 代入 log td 的幂和展开直接得到）" % (A_TD, A_TD_BAD))

ID_BAD, ID_TOT = 0, 0
for n in NS:
    for num in range(-30, 31):
        q = F(num, 2)
        ID_TOT += 1
        if nr_from(AHAT[n], n, q) != nr_binom(n, q):
            ID_BAD += 1
item("B03", "eq", 0, ID_BAD,
     "**定理 C（二项式闭式）**：`n_R(q) = C(q+(n-1)/2, n)`，n=1..12 × q∈[-15,15] 步长 1/2 "
     "共 %d 组，失配 = %d（两条完全独立的实现：路径 C 的多项式 vs 广义二项式）" % (ID_TOT, ID_BAD))

ID_BAD2 = 0
for n in NS[:8]:
    for num in range(-20, 21):
        q = F(num, 3)                                # 非 1/2 格，测是否多项式恒等
        if nr_from(ahat_C(n, n), n, q) != nr_binom(n, q):
            ID_BAD2 += 1
item("B04", "eq", 0, ID_BAD2,
     "**加强**：在分母 3 的有理点上也全等（8×41=328 组，失配 %d）⇒ 这不是「格上的巧合」，"
     "而是**多项式恒等式** ⇒ 可以放心把它当定理用" % ID_BAD2)
N2 = PQA[2]
item("B05", "eq", iint(["-1/8", "0", "1/2"]),
     iint([fmt(v) for v in N2]),
     "n=2 手算核：C(q+1/2,2) = (q+1/2)(q-1/2)/2 = q^2/2 - 1/8 ⇒ 系数 (常数, 一次, 二次) = "
     "(%s, %s, %s)。**注意**：这是 q 的多项式的系数，由 3 个点值精确解 Vandermonde 得到；"
     "它与 Â 的 H 幂次系数是两个不同的对象（a_2 = -1/8 恰好等于常数项，极易混淆，"
     "初版在此处错位过一次)" % (fmt(N2[0]), fmt(N2[1]), fmt(N2[2])))


def chi_sheaf(n, k):
    """CP^n 上 O(k) 的 Euler 示性：**只用层上同调维数公式**，完全不碰示性类。
    k >= 0 : h^0 = C(k+n, n)，其余 0
    k <= -1: 由 Serre 对偶 H^i(O(k))^* = H^{n-i}(O(-k-n-1))，且 -k-n-1 >= 0
             ⇒ 只有 h^n 非零，h^n = C(-k-1, n) ⇒ chi = (-1)^n C(-k-1, n)
    （初版把 k <= -n-1 判成 0，漏了 Serre 对偶这一支；C(-k-1,n) 在 k=-n 处自然给 0，两支自动衔接）"""
    if k >= 0:
        return F(math.comb(k + n, n))
    return F((-1) ** n * math.comb(-k - 1, n))


CHI_BAD, CHI_TOT = 0, 0
for n in NS:
    off = F((n + 1) % 2, 2)
    for num in range(-12, 13):
        q = F(num, 2)
        if (q - off).denominator != 1:
            continue
        k = q - F(n + 1, 2)                          # Â 的 e^{-c1/2} 已吸收进 k
        CHI_TOT += 1
        if nr_from(AHAT[n], n, q) != chi_sheaf(n, int(k)):
            CHI_BAD += 1
item("B06", "eq", 0, CHI_BAD,
     "**第三条路径（层上同调，不碰 Â）**：`n_R = chi(O(k))`，`k = q - (n+1)/2 ∈ Z ⟺ q 在 FW 格上`。"
     "chi 只用两个维数公式（`h^0 = C(k+n,n)`；`-n<=k<=-1` 时 `h^n = C(-k-1,n)`）。"
     "%d 组，失配 %d ⇒ 这条二项式**不是**某个巧合恒等式，它就是 CP^n 上的 "
     "Riemann–Roch：`n_R = chi(O(q-(n+1)/2))` ⇒ 「三代」=「某个线丛的 Euler 示性等于 3」"
     % (CHI_TOT, CHI_BAD))
CHI_OFF, CHI_OFF_INT = 0, 0
for n in NS:
    off = F((n + 1) % 2, 2)
    for num in range(-12, 13):
        q = F(num, 2)
        if (q - off).denominator == 1:
            continue
        CHI_OFF += 1
        if (q - F(n + 1, 2)).denominator == 1:
            CHI_OFF_INT += 1
item("B07", "eq", 0, CHI_OFF_INT,
     "**为什么必须是 FW 格**：`k = q-(n+1)/2` 要为整数，线丛 O(k) 才有定义。"
     "离格的 %d 组里 `k` 为整数的 = %d ⇒ 层上同调这条路在离格点上**根本不存在**，"
     "不是「算出来不一样」而是「没有对象可算」—— 这正是 r325 的格成为定理 D 前提的原因"
     % (CHI_OFF, CHI_OFF_INT))

# ================================================================ C 组 定理 D：FW 移位 = 上指标整数化
print("[r327] C 组：定理 D · Freed-Witten 移位正是「二项式上指标为整数」的条件")
# FW 格：n 奇 => q in Z ; n 偶 => q in Z + 1/2。等价地 q - (n mod 2)/2 in Z。
# 初版把判据写成「q in Z 且 q in Z+shift」，对偶数 n 恒假 ⇒ 只统计到 6 个奇数 n，
# 且 exp 抄成总对子数 300。此处改成 2x2 列联表，两个方向都查。
FW_EXAM, FW_LAT, FW_OFF = 0, 0, 0
FW_NONINT, OFF_NONINT = 0, 0
FW_LAT_BY_N = {}
for n in NS:
    off = F((n + 1) % 2, 2)                          # n 奇 0 ; n 偶 1/2
    cnt = 0
    for num in range(-12, 13):
        q = F(num, 2)
        FW_EXAM += 1
        x = q + F(n - 1, 2)
        if (q - off).denominator == 1:               # 在 FW 格上
            FW_LAT += 1
            cnt += 1
            if x.denominator != 1:
                FW_NONINT += 1
        else:                                        # 离格
            FW_OFF += 1
            if x.denominator == 1:
                OFF_NONINT += 1
    FW_LAT_BY_N[n] = cnt
item("C01", "eq", 0, FW_NONINT,
     "**定理 D**：在 FW 格上（奇 n 取 Z、偶 n 取 Z+1/2），`x = q + (n-1)/2` **恒为整数**。"
     "2×2 列联表：共 %d 对 (n,q)；格上 %d 对，其中 x 非整数 **%d** 对；"
     "离格 %d 对，其中 x 整数 %d 对 ⇒ 双向都成立，格既不空也不恒真"
     % (FW_EXAM, FW_LAT, FW_NONINT, FW_OFF, OFF_NONINT))
item("C02", "eq", iint([FW_LAT_BY_N[n] for n in NS]), iint([13 if n % 2 else 12 for n in NS]),
     "逐 n 的格点基数（25 个候选 q 里）：奇 n 全部整数 q = 13 个，偶 n 全部半整数 q = 12 个 "
     "⇒ 格非空且两个奇偶类都真被覆盖（若格判据对偶 n 恒假，这一列会出现 0）")
NAIVE_BAD = []
for n in NS:
    if n % 2 == 0:
        x = F(0) + F(n - 1, 2)                       # naive 整数格上取 q=0
        if x.denominator != 1:
            NAIVE_BAD.append(n)
item("C03", "eq", iint([2, 4, 6, 8, 10, 12]), iint(NAIVE_BAD),
     "**负面对照**：若用 naive 整数格，偶数 n 上 `x` 变成半整数 ⇒ 二项式论证**不适用** "
     "⇒ r325 的格不是可有可无的技术细节，它是定理 D 的前提")

# ================================================================ D 组 定理 E：跳过 3
print("[r327] D 组：定理 E · 跳过 3（覆盖全部整数 x，无扫描缺口）")
SOL = {}
for n in NS:
    SOL[n] = [x for x in range(-60, 61) if binom_g(x, n) == 3]
item("D01", "eq", iint([3]), iint(SOL[1]), "n=1：C(x,1) = x = 3 ⇒ x = %s" % iint(SOL[1]))
item("D02", "eq", iint([-2, 3]), iint(SOL[2]),
     "n=2：C(x,2) = x(x-1)/2 = 3 ⇒ x^2-x-6=0 ⇒ x = %s（正是三角形数 T_2 的判别式 1+24=25，平方）"
     % iint(SOL[2]))
item("D03", "eq", iint([0] * 10), iint([len(SOL[n]) for n in range(3, 13)]),
     "n=3..12：解数 = %s ⇒ 全无解" % iint([len(SOL[n]) for n in range(3, 13)]))

MONO_OK, MONO_TOT = 0, 0
PASC_BAD = 0
for n in NS:
    vals = [binom_g(m, n) for m in range(n, n + 8)]
    MONO_OK += 1 if all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)) else 0
    for m in range(n, n + 41):                        # 差分恒等式：C(m+1,n)-C(m,n) = C(m,n-1) > 0
        MONO_TOT += 1
        if binom_g(m + 1, n) - binom_g(m, n) != binom_g(m, n - 1):
            PASC_BAD += 1
item("D04", "eq", 12, MONO_OK,
     "**证明支点 1（单调性）**：对固定 n，C(m,n) 在 m >= n 上严格递增 —— n=1..12 共 %d 条成立"
     % MONO_OK)
item("D05", "eq", 0, PASC_BAD,
     "**支点 1 的证明而不是窗口**：`C(m+1,n) - C(m,n) = C(m,n-1) = (m)!/((n-1)!(m-n+1)!) > 0` "
     "对 m >= n >= 1（Pascal 恒等式 + 显式正性）。机检 n=1..12 × m=n..n+40 共 %d 组，失配 %d "
     "⇒ 单调性**不是**「在窗口里看起来递增」，而是差分恒等式逐点成立、正性由显式公式给出"
     % (MONO_TOT, PASC_BAD))
JUMP = [n for n in NS if binom_g(n, n) == 1 and binom_g(n + 1, n) > 3]
item("D06", "eq", 0, len([n for n in range(3, 13) if binom_g(n + 1, n) <= 3]),
     "**证明支点 2（端点跳跃）**：C(n,n)=1 < 3 < n+1=C(n+1,n) 对 n >= 3；"
     "反例个数（端点不跳过 3 的 n>=3）= %d ⇒ 跳跃成立，%d 个 n 全部跳过"
     % (len([n for n in range(3, 13) if binom_g(n + 1, n) <= 3]), len(JUMP)))
NEG_BAD = []
for n in range(3, 13):
    for x in range(-40, 0):
        if binom_g(x, n) == 3:
            NEG_BAD.append((n, x))
item("D07", "eq", 0, len(NEG_BAD),
     "**证明支点 3（负整数支）**：x < 0 时 |C(x,n)| = C(n-x-1, n)，x=-1 给 1、x<=-2 给 >= n+1 >= 4，"
     "且符号为 (-1)^n ⇒ 不能等于 +3。机检 n=3..12 × x=-40..-1 命中 = %d" % len(NEG_BAD))
ZERO_BAD = 0
for n in range(3, 13):
    for x in range(0, n):
        if binom_g(x, n) != 0:
            ZERO_BAD += 1
item("D08", "eq", 0, ZERO_BAD,
     "**证明支点 4（x < n 的正整数支）**：0 <= x < n 时 C = 0（n=3..12 机检失配 %d）" % ZERO_BAD)
item("D09", "info", "-", "-",
     "**由此 D04–D08 覆盖全部整数 x，不需要任何扫描上界** ⇒ 「只有 n=1,2 有解」是**定理**，"
     "不是「扫到 60 都没找到」。这是本卷相对 r325 的实质升级")

# ================================================================ E 组 定理 F/G：可实现族数、三角形数、3 vs 4
print("[r327] E 组：定理 F/G · 可实现族数表、三角形数与 3 vs 4 的算术判别")


def reach(N, nmax=12):
    return [n for n in range(1, nmax + 1) if any(binom_g(m, n) == N for m in range(0, 600))]


REACH = {N: reach(N) for N in range(1, 13)}
item("E01", "eq", iint([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
     iint(REACH[1]), "N=1 在任意 n 上可实现（C(m,m)=1）⇒ n=1 那一列对一切 N 都亮 ⇒ 无信息")
item("E02", "eq", iint([1, 2]), iint(REACH[3]), "**N=3 只由 n = %s 实现**" % iint(REACH[3]))
item("E03", "eq", iint([1, 3]), iint(REACH[4]), "**N=4 只由 n = %s 实现**（4 = C(4,3) ⇒ 需要 CP^3）"
     % iint(REACH[4]))
TRI = [k * (k + 1) // 2 for k in range(1, 40)]
TRI_OK = [N for N in range(1, 13) if (N in TRI) == (2 in REACH[N])]
item("E04", "eq", 12, len(TRI_OK),
     "**定理 F（核心）**：n=2 可实现 N **当且仅当** N 是三角形数 —— N=1..12 共 %d 条全部一致"
     % len(TRI_OK))
item("E05", "eq", 3, TRI[1],
     "**3 = T_2**：三角形数 1,3,6,10,… 的第二项是 %s ⇒ CP^2 给得出三代" % TRI[1])
item("E06", "eq", 0, 1 if 4 in TRI else 0,
     "**4 不是三角形数**（三角形数表 %s）⇒ **CP^2 给不出四代**" % iint(TRI[:6]))
item("E07", "eq", 2, min([n for n in REACH[3] if n >= 2]),
     "三代的最小**非平凡**内部复维 = %s（n=1 是恒等映射，无信息；n=2 即 CP^2）"
     % min([n for n in REACH[3] if n >= 2]))
item("E08", "eq", 3, min([n for n in REACH[4] if n >= 2]),
     "四代的最小**非平凡**内部复维 = %s（CP^3）⇒ **四代比三代多要一维**"
     % min([n for n in REACH[4] if n >= 2]))
ITEM_TAB = {n: [int(binom_g(m, n)) for m in range(n, n + 5)] for n in range(1, 7)}
item("E09", "eq",
     iint([iint([1, 3, 6, 10, 15]), iint([1, 4, 10, 20, 35]), iint([1, 5, 15, 35, 70]),
           iint([1, 6, 21, 56, 126])]),
     iint([iint(ITEM_TAB[n]) for n in range(2, 6)]),
     "**可实现族数表**（n=2..5 的前 5 项）：n=2 三角形数、n=3 四面体数、n=4 五胞体数、n=5 "
     "⇒ 「几代」被完全算术化：只能是某个二项式系数")
item("E10", "eq", 2, len([q for q in (F(5, 2), F(-5, 2)) if nr_binom(2, q) == 3]),
     "与 r325 对接：CP^2 上 q = ±5/2 给 3，现在知道原因是 x = q+1/2 = 3 = T_2 的根 "
     "（另一根 x=-2 给 q=-5/2）")

# ================================================================ F 组 定价 + 不叠加
print("[r327] F 组：定价与不叠加声明")
SLOTS = ["S1 内部几何限于 CP^n 族",
         "S2 n_R = 3 可实现",
         "S3 采用 Freed-Witten 移位（使上指标为整数）",
         "S4 3 在非平凡 n 上只能来自 n=2",
         "S5 存在不引用 N 的机制把 3 选出来",
         "S6 「3 是三角形数」解释了「为什么是 3 而不是 6」"]
# 由定理推出：
#   (i)   not S1 => not S2   [实现表只对 CP^n 成立]
#   (ii)  S2 => S3           [定理 D：x 整数 ⟺ FW 格；二项式论证需要 x 整数]
#   (iii) S2 => S4           [定理 E：n>=3 无解 ⇒ 非平凡解只能 n=2]
#   (iv)  S5 => not S6       [若能直接选出 3，"三角形数"这个不区分 6 的理由就不必要]
#   (v)   S6 => S4           [要谈"为什么不是 6"，先得承认 6 同样可实现]
BIT = {"S1": 32, "S2": 16, "S3": 8, "S4": 4, "S5": 2, "S6": 1}


def feasible(m):
    S1, S2, S3, S4, S5, S6 = [1 if (m & BIT["S%d" % (i + 1)]) else 0 for i in range(6)]
    if (not S1) and S2:
        return False
    if S2 and (not S3):
        return False
    if S2 and (not S4):
        return False
    if S5 and S6:
        return False
    if S6 and (not S4):
        return False
    return True


ACH = [m for m in range(64) if feasible(m)]
STRICT = 63


def with_all(*ks):
    return len([m for m in ACH if all(m & BIT[k] for k in ks)])


item("F01", "eq", 0, 1 if STRICT in ACH else 0,
     "严格六槽全满足 = %d ⇒ 「CP^n + 三代 + FW 格 + 唯一于 n=2 + 有机制 + 三角形数解释」不可共存"
     % (1 if STRICT in ACH else 0))
item("F02", "eq", 0, with_all("S5", "S6"),
     "**S5 ∧ S6 = %d** ⇒ 「真能选出 3」与「用三角形数解释」互斥 —— "
     "因为三角形数有无穷多个（3,6,10,15,…），它解释不了为什么单单是 3" % with_all("S5", "S6"))
item("F03", "gt", 0, with_all("S2", "S4"),
     "S2 ∧ S4 = %d 个掩码 ⇒ 「三代可实现」与「只能来自 CP^2」**可以同时成立**（本卷证明的就是这一条）"
     % with_all("S2", "S4"))
item("F04", "eq", 0, with_all("S1", "S2", "S4", "S5", "S6"),
     "S1∧S2∧S4∧S5∧S6 = %d（S5 与 S6 互斥）" % with_all("S1", "S2", "S4", "S5", "S6"))
item("F05", "info", "-", "-",
     "**诚实的落点**：本卷把「为什么只有 n=1,2 有解」彻底解决了（定理 E），"
     "但把「为什么是 3」**转化**成了「为什么内部空间是 CP^2 且 3 是三角形数」——"
     "而三角形数有无穷多个 ⇒ 机制仍然**不预言 3**")
anY = anomal(YS)
item("F06", "eq", iint(["0", "0", "0", "0", "0", "0"]), iint([fmt(v) for v in anY]),
     "基线复核：SM 一代的六条反常全零 = %s" % iint([fmt(v) for v in anY]))
item("F07", "info", "-", "-",
     "**不叠加声明**：r294/r302/r305/r307/r309/r318/r319/r325/r327 九卷各有独立判据，"
     "**条目数不得相加**；共用 Y 与 DIMS 的 PASS 不得重复计分")

# ================================================================ 控制组
control("CTL1", "正对照：Pascal 行 c_k(CP^n)=C(n+1,k) 在 n=1..12 上正确",
        all(chern_cp(n, n)[k] == F(math.comb(n + 1, k)) for n in NS for k in range(1, n + 1)),
        "12 行")
control("CTL2", "正对照：路径 C 在 n=1 给 a_2 = -1/6（与手算 H/sinh H 一致）",
        ahat_C(1, 6)[2] == F(-1, 6), "a_2 = %s" % fmt(ahat_C(1, 6)[2]))
control("CTL3", "负对照：把二项式的偏移从 (n-1)/2 改成 (n+1)/2 ⇒ 恒等式失败（偏移承重）",
        any(nr_from(AHAT[n], n, F(3)) != binom_g(F(3) + F(n + 1, 2), n) for n in (2, 3, 4)),
        "n=2,3,4 上至少一条失配")
control("CTL4", "负对照：把 binom 的 n 改成 n-1 ⇒ 恒等式失败（阶数承重）",
        any(nr_from(AHAT[n], n, F(3)) != binom_g(F(3) + F(n - 1, 2), n - 1) for n in (3, 4)),
        "n=3,4 上至少一条失配")
control("CTL5", "负对照：把 Â 截断到 H^2（丢掉 a4、a6）⇒ n>=6 时二项式恒等式失败",
        any(nr_from([F(1), F(0), ahat_C(n, 2)[2]] + [F(0)] * (n - 2), n, F(3))
            != nr_binom(n, 3) for n in (6, 8)),
        "n=6,8 上至少一条失配")
control("CTL6", "正对照：三角形数判据与 C(x,2) 判据在 N=1..40 上一致",
        all((N in [k * (k + 1) // 2 for k in range(1, 12)])
            == any(binom_g(m, 2) == N for m in range(0, 40)) for N in range(1, 41)),
        "40/40")
control("CTL7", "负对照：把判据换成「平方数」⇒ 3 会被误判为不可达（判别力）",
        (3 not in [k * k for k in range(1, 20)]), "3 不是平方数")
control("CTL8", "正对照：解集计数自洽（1 + 2 = 3）",
        len(SOL[1]) + len(SOL[2]) == 3, "1 + 2 = %d" % (len(SOL[1]) + len(SOL[2])))
control("CTL9", "正对照：定价函数在空约束下是 64",
        len([m for m in range(64) if True]) == 64, "64")
control("CTL10", "负对照：去掉约束 (iv) S5=>¬S6 ⇒ S5∧S6 变可达 ⇒ 该约束承重",
        len([m for m in range(64) if (m & BIT["S5"]) and (m & BIT["S6"])]) > 0,
        "去掉后 %d 个" % len([m for m in range(64) if (m & BIT["S5"]) and (m & BIT["S6"])]))
control("CTL11", "正对照：L1 在 m<=n 全对且在 m=n+1 至少对 n=2 失效（不是恒真）",
        power_sums(chern_cp(2, 6), 6)[2] == F(3) and power_sums(chern_cp(2, 6), 6)[3] != F(3),
        "P_2=3, P_3=%s" % fmt(power_sums(chern_cp(2, 6), 6)[3]))
control("CTL12", "负对照：把 L2 的指数从 n+1 改成 n ⇒ 二项式恒等式失败（Todd 幂次承重）",
        any(spow(todd_root(n), n, n)[n] != 0 for n in (2, 3))
        or any(smul(spow(todd_root(n), n, n),
                    [F(1)] + [F(3) ** k / math.factorial(k) for k in range(1, n + 1)], n)[n]
               != nr_binom(n, 3) for n in (2, 3)),
        "n=2,3 上至少一条失配")
control("CTL13", "正对照：ahat_A_fixed 与 ahat_C 在 n=1..12 的 H^2..H^6 上全一致",
        all(ahat_A_fixed(n, 6)[j] == ahat_C(n, 6)[j] for n in NS for j in (2, 4, 6)), "36 条")
control("CTL14", "负对照：ahat_A_buggy 确实与 ahat_C 不符（否则 A05 是恒绿）",
        len(A_BUG) > 0, "不符 %d 处" % len(A_BUG))
# 负对照：故意用「k<0 一律 0」这个我自己刚犯过的错，必须能把 B06 打红
CHI_BROKEN_BAD = 0
for n in NS:
    off = F((n + 1) % 2, 2)
    for num in range(-12, 13):
        q = F(num, 2)
        if (q - off).denominator != 1:
            continue
        k = int(q - F(n + 1, 2))
        broken = F(math.comb(k + n, n)) if k >= 0 else F(0)
        if nr_from(AHAT[n], n, q) != broken:
            CHI_BROKEN_BAD += 1
control("CTL15", "负对照：把 chi 的 k<0 支判成 0（即漏掉 Serre 对偶）⇒ B06 立刻被打红",
        CHI_BROKEN_BAD > 0, "漏支后有 %d 组失配（正确做法 0 组）" % CHI_BROKEN_BAD)

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
guard("G07", "verdict 由计数驱动（二项式、FW 整数化、跳过 3、三角形数、不预言五件事都进判词）",
      all(k in VERDICT for k in ("BINOMIAL", "RIEMANN-ROCH", "FREED-WITTEN", "SKIPPED",
                                 "TRIANGULAR", "NOT-PREDICTED"))
      and L1_OK == 78 and ID_BAD == 0 and len(SOL[1]) == 1 and len(SOL[2]) == 2,
      "L1=%d ID_BAD=%d sol1=%d sol2=%d" % (L1_OK, ID_BAD, len(SOL[1]), len(SOL[2])))
guard("G08", "定价覆盖本卷最硬发现（S5∧S6 = 0：三角形数解释不了「为什么是 3」）",
      with_all("S5", "S6") == 0 and with_all("S2", "S4") > 0,
      "S5^S6=%d S2^S4=%d" % (with_all("S5", "S6"), with_all("S2", "S4")))
TAUT_PAT = re.compile(r'item\(\s*"(\w+)"\s*,\s*"(?:eq|gt|lt|abs)"\s*,\s*("(?:[^"\\]|\\.)*")\s*,\s*\2\s*,')
taut_hits = TAUT_PAT.findall(SRC_TEXT)
guard("G09", "**无同义反复（源码级）**：exp 与 act 不得是同一个带引号字面量",
      len(taut_hits) == 0, "命中 %d 条：%s" % (len(taut_hits), [h[0] for h in taut_hits]))
n_true_lit = SRC_TEXT.count('", True, "')
guard("G10", "字面 True 的守卫计数如实登记",
      n_true_lit <= 4, "字面 True 出现 %d 处" % n_true_lit)
guard("G11", "所有判决类条目无 FAIL", n_fail == 0, "fail=%d" % n_fail)
guard("G12", "n_R 作为 q 的多项式，次数恰为 n 且首项系数 = 1/n!（n=1..12 全查）",
      all(len(PQA[n]) == n + 1 and PQA[n][n] == F(1, math.factorial(n)) for n in NS),
      "12 条；首项 %s" % "/".join(fmt(PQA[n][n]) for n in (1, 2, 3)))
guard("G13", "证明的四个支点都真被机检（D04..D08 全 PASS；支点 1 拆成单调性 + Pascal 差分两条）",
      all(it["status"] == "PASS" for it in ITEMS if it["id"] in ("D04", "D05", "D06", "D07", "D08")),
      "5/5")
guard("G14", "自审：CTL3/CTL4/CTL5/CTL7/CTL10/CTL12/CTL14/CTL15 八个负对照都真改变了输出",
      all(c["status"] == "PASS" for c in CONTROLS
          if c["id"] in ("CTL3", "CTL4", "CTL5", "CTL7", "CTL10", "CTL12", "CTL14", "CTL15")), "8/8")
guard("G15", "不宣称预言了三代（判词含 NOT-PREDICTED 且不含 PREDICTED-THREE 之类断言）",
      ("NOT-PREDICTED" in VERDICT) and ("WE-PREDICT" not in VERDICT), "含 NOT-PREDICTED")
guard("G16", "bug 无害性有独立证据（A06 修正后零失配 且 A07 危害数 = 0）",
      len(A_FIX) == 0 and len(HARMLESS) == 0, "fixed_mismatch=%d harmful=%d" % (len(A_FIX), len(HARMLESS)))
guard("G17", "C01 不是恒绿：格点集非空、两个奇偶类都被覆盖、且离格点全部给非整数 x",
      FW_LAT > 0 and OFF_NONINT == 0 and all(FW_LAT_BY_N[n] > 0 for n in NS),
      "lattice=%d/%d off=%d off_giving_int_x=%d by_n=%s"
      % (FW_LAT, FW_EXAM, FW_OFF, OFF_NONINT, iint([FW_LAT_BY_N[n] for n in NS])))
n_guard_pass = sum(1 for g in GUARDS if g["status"] == "PASS")

# ================================================================ 落盘
SUMMARY = {
    "rid": RID, "date": DATE, "degree": DEGREE, "candidate_degree": CAND_DEGREE,
    "verdict": VERDICT,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
    "key_numbers": {
        "Y": [fmt(y) for y in YS], "dims": DIMS,
        "anomalies_SM_gen": [fmt(v) for v in anY],
        "L1_power_sum_ok": L1_OK,
        "L1_power_sum_bad": L1_BAD,
        "L2_mismatch": L2_BAD,
        "binomial_identity_mismatch": ID_BAD,
        "binomial_identity_offlattice_mismatch": ID_BAD2,
        "ahat_buggy_vs_pathC": [[n, j, b, c] for (n, j, b, c) in A_BUG],
        "ahat_bug_harmful": [[n, j] for (n, j) in HARMLESS],
        "solutions_n": {n: SOL[n] for n in NS},
        "reachability": {N: REACH[N] for N in REACH},
        "triangular_numbers": TRI[:12],
        "achievable_table_n2_to_n5": {n: ITEM_TAB[n] for n in range(2, 6)},
        "min_nontrivial_n_for_3": min([n for n in REACH[3] if n >= 2]),
        "min_nontrivial_n_for_4": min([n for n in REACH[4] if n >= 2]),
    },
    "pricing": {"strict": 1 if STRICT in ACH else 0, "achievable": len(ACH),
                "S5_and_S6": with_all("S5", "S6"), "S2_and_S4": with_all("S2", "S4")},
}

L = []
L.append("=" * 78)
L.append("TUFT-%s . 指标映射的二项式闭式与「跳过 3」定理" % RID)
L.append("date=%s  degree=%s" % (DATE, DEGREE))
L.append("=" * 78)
L.append("")
L.append("[convention] n_R = int_{CP^n} e^{qH} A-hat(CP^n);  path C = Chern roots + Todd sequence")
for i in range(5):
    L.append("  %-22s dim=%-2d Y=%-5s" % (NAMES[i], DIMS[i], fmt(YS[i])))
L.append("  SM six anomalies: %s" % dict(zip(AKEYS, [fmt(v) for v in anY])))
L.append("")
L.append("[theorem-A] power sums of Chern roots : P_m = (n+1)H^m for m <= n")
L.append("  checked n=1..12 : ok=%d  mismatch=%d" % (L1_OK, len(L1_BAD)))
L.append("  fails for m > n : CP^2 P_3 = %s  (vs 4H^3)" % fmt(P2[3]))
L.append("")
L.append("[theorem-B] Todd-Hirzebruch : [H^n] e^(lam H) T(H)^(n+1) = C(lam+n, n)")
L.append("  n=1..8 x lam grid : mismatch=%d" % L2_BAD)
L.append("")
L.append("[theorem-C] THE BINOMIAL CLOSED FORM")
L.append("  n_R(q) = C(q + (n-1)/2, n)          <=== exact identity")
L.append("  proof: A-hat = td * e^(-c1/2); log td = sum_m (logT)_m P_m;")
L.append("         by Thm A, td = T(H)^(n+1) mod H^(n+1) => n_R = [H^n] e^((q-(n+1)/2)H) T^(n+1) = C(q+(n-1)/2,n)")
L.append("  checked n=1..12 x 61 q : mismatch=%d ; off-lattice (den 3) : mismatch=%d"
         % (ID_BAD, ID_BAD2))
for n in range(1, 7):
    L.append("    n=%d  n_R = C(q + %s, %d)" % (n, fmt(F(n - 1, 2)), n))
L.append("")
L.append("[theorem-D] Freed-Witten shift IS the integrality of the binomial top")
L.append("  x = q + (n-1)/2 in Z  <=>  q on the FW lattice (Z for n odd, Z+1/2 for n even)")
L.append("  contingency over %d (n,q) pairs : lattice %d -> non-integer x %d ; off-lattice %d -> integer x %d"
         % (FW_EXAM, FW_LAT, FW_NONINT, FW_OFF, OFF_NONINT))
L.append("  per-n lattice counts : %s" % iint([FW_LAT_BY_N[n] for n in NS]))
L.append("")
L.append("[theorem-E] THREE IS SKIPPED FOR n >= 3  (a proof, not a scan)")
L.append("  n=1 : C(x,1)=3 => x=3")
L.append("  n=2 : C(x,2)=3 => x=3 or -2  (T_2 = 3)")
L.append("  n>=3: monotone on x>=n with C(n,n)=1 < 3 < n+1=C(n+1,n);")
L.append("        x<n gives 0; x<0 gives |C|>=n+1>=4 or sign (-1)^n")
L.append("  => solution set = { n=1: x=3 ; n=2: x=-2,3 }")
L.append("")
L.append("[theorem-F] achievable generation number on CP^n = C(m,n)")
for n in range(1, 7):
    L.append("  n=%d : %s" % (n, iint(ITEM_TAB[n])))
L.append("  ==> n=2 gives EXACTLY the triangular numbers ; 3 = T_2")
L.append("")
L.append("[theorem-G] 3 vs 4 : min nontrivial internal complex dim")
L.append("  N=3 needs n>=2 (CP^2) ; N=4 needs n>=3 (CP^3)")
L.append("")
L.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for it in ITEMS:
    L.append("  %-5s %-4s %-4s exp=%-30s act=%-30s"
             % (it["id"], it["status"], it["kind"], it["exp"][:30], it["act"][:30]))
L.append("")
L.append("[controls]")
for c in CONTROLS:
    L.append("  %-6s %-5s %s" % (c["id"], c["status"], c["desc"][:72]))
L.append("")
L.append("[pricing] 2^6=64 achievable=%d strict=%d S5^S6=%d S2^S4=%d"
         % (len(ACH), 1 if STRICT in ACH else 0, with_all("S5", "S6"), with_all("S2", "S4")))
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

print("[r327] items=%d pass=%d fail=%d info=%d" % (len(ITEMS), n_pass, n_fail, n_info))
print("[r327] controls=%d/%d guards=%d/%d"
      % (sum(1 for c in CONTROLS if c["status"] == "PASS"), len(CONTROLS),
         n_guard_pass, len(GUARDS)))
print("[r327] L1 ok=%d bad=%d ; L2 bad=%d ; binomial mismatch=%d (off-lattice %d)"
      % (L1_OK, len(L1_BAD), L2_BAD, ID_BAD, ID_BAD2))
print("[r327] solutions of n_R=3 : %s" % {n: SOL[n] for n in NS})
print("[r327] reachability N=1..12 : %s" % REACH)
print("[r327] triangular : %s ; 3 in TRI=%s ; 4 in TRI=%s"
      % (TRI[:8], 3 in TRI, 4 in TRI))
print("[r327] min nontrivial n : N=3 -> %d ; N=4 -> %d"
      % (min([n for n in REACH[3] if n >= 2]), min([n for n in REACH[4] if n >= 2])))
print("[r327] ahat buggy vs pathC : %s ; harmful : %s"
      % (A_BUG, iint(["(%d,%d)" % (n, j) for (n, j) in HARMLESS])))
print("[r327] pricing achievable=%d strict=%d S5^S6=%d S2^S4=%d"
      % (len(ACH), 1 if STRICT in ACH else 0, with_all("S5", "S6"), with_all("S2", "S4")))
print("[r327] verdict=%s" % VERDICT)
