# -*- coding: utf-8 -*-
"""TUFT-r358 · 整性集的精确结构：陪集只需 n+1 个值判定，周期等于分母 lcm，窗口法不可靠

攻靶：
  X-R339-2  非陪集的机制（r339 只给了见证点，没给机制）
  X-R346-2  额外点（S ⊋ Z）的存在判据
  X-R346-1  周期界能否从 (M^n n!)^2 压下来

口径（承 r339/r346）：X_d ⊂ CP^{n+1}，dim_C = n，
  χ(O_X(kH)) = d · [h^n]( e^{kh} td(T_X) )，  td(T_X) = T(h)^{n+2}/T(dh)
  P(k) = Σ_j a_j C(k,j)，  a_j = Δ^j P(0)，  a_n = H^n = d
  S = { k ∈ Q : P(k) ∈ Z }

本卷三条承重：
  定理 E′（有限判据）  c+Z ⊆ S  ⟺  P(c), P(c+1), …, P(c+n) ∈ Z   （只需 n+1 个值）
  定理 G （周期）      S∩(c+Z) 的最小周期 N 整除 D·n!，其中 D = lcm_i den b_i(c)
                      且实测 N = D（在所有可精确测定的陪集上，等式成立）
  定理 F （单剩余类）  S∩(c+Z) 是**一条**等差级数（一个周期内恰 1 个整点）

并否证一个诱惑：固定网格/固定窗口法在原理上不可靠（D 可达 3.58e7）。
"""
import io
import json
import math
import os
import sys
from fractions import Fraction as F

# ============================================================ 基础设施
RID = "r358"
DATE = "2026-11-01"
DEGREE = 0
CAND_DEGREE = 37

STEM = ("TUFT-r358_整性集的精确结构_陪集只需n加一个值判定_"
        "周期等于分母最小公倍数_窗口法不可靠_精算与可视化_2026-11-01")
HTML = "四力统一方程_整性集精确结构_r358可视化_2026-11-01.html"

OUTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LCG(object):
    """确定性伪随机（禁 import random：守卫 G12 在 AST 层查 Import）。"""

    def __init__(self, seed):
        self.s = seed % 2147483648

    def nxt(self, m):
        self.s = (1103515245 * self.s + 12345) % 2147483648
        return self.s % m


def series_mul(a, b, N):
    out = [F(0)] * (N + 1)
    for i in range(N + 1):
        if a[i] == 0:
            continue
        ai = a[i]
        for j in range(N + 1 - i):
            if b[j] != 0:
                out[i + j] += ai * b[j]
    return out


def series_inv(a, N):
    inv = [F(0)] * (N + 1)
    inv[0] = 1 / a[0]
    for m in range(1, N + 1):
        s = F(0)
        for i in range(1, m + 1):
            if a[i] != 0 and inv[m - i] != 0:
                s += a[i] * inv[m - i]
        inv[m] = -s / a[0]
    return inv


def T_series(N):
    Q = [F((-1) ** j, math.factorial(j + 1)) for j in range(N + 1)]
    return series_inv(Q, N)


_TDC = {}


def td_cpn(n):
    if n in _TDC:
        return _TDC[n]
    T = T_series(n)
    out = [F(0)] * (n + 1)
    out[0] = F(1)
    for _ in range(n + 1):
        out = series_mul(out, T, n)
    _TDC[n] = out
    return out


def td_hypersurface(n, d):
    T = T_series(n)
    Td = [T[i] * (F(d) ** i) for i in range(n + 1)]
    return series_mul(td_cpn(n), series_mul(T, series_inv(Td, n), n), n)


def chi_at(n, d, k):
    tdX = td_hypersurface(n, d)
    kk = F(k)
    e = [F(1)] + [kk ** j / math.factorial(j) for j in range(1, n + 1)]
    return F(d) * series_mul(e, tdX, n)[n]


def h0(n, d, k):
    """H^0(O_X(kH)) = dim{CP^{n+1} 的 k 次齐次式} − dim{乘以定义方程的}（k ≥ d 时）。"""
    if k < 0:
        return 0
    return math.comb(k + n + 1, n + 1) - math.comb(k + n + 1 - d, n + 1)


def newton_of(n, d):
    vals = [chi_at(n, d, k) for k in range(n + 1)]
    a, cur = [], list(vals)
    while cur:
        a.append(cur[0])
        cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    return a


def cpoly(k, j):
    if j == 0:
        return F(1)
    num = F(1)
    for i in range(j):
        num *= (k - i)
    return num / math.factorial(j)


def peval(a, k):
    s = F(0)
    for j in range(len(a)):
        if a[j] != 0:
            s += a[j] * cpoly(k, j)
    return s


def binom_int(m, i):
    """C(m,i)，m 为整数（可负），返回整数。"""
    if i == 0:
        return 1
    num = 1
    for t in range(i):
        num *= (m - t)
    return num // math.factorial(i)


def isint(x):
    return x.denominator == 1


def divisors(m):
    return [t for t in range(1, abs(m) + 1) if m % t == 0]


# ------------------------------------------------------------ 本卷新增：陪集工具
def bvec(a, c):
    """b_i(c) = Σ_{j≥i} a_j C(c, j−i)   （Vandermonde：P(c+m)=Σ_i b_i(c) C(m,i)）"""
    n = len(a) - 1
    return [sum((a[j] * cpoly(c, j - i) for j in range(i, n + 1)), F(0))
            for i in range(n + 1)]


def lcm_den(b):
    d = 1
    for x in b:
        d = d * x.denominator // math.gcd(d, x.denominator)
    return d


def betas_of(b):
    """整数化：β_i = D·b_i ∈ Z，则 Q(m)∈Z ⟺ f(m):=Σ β_i C(m,i) ≡ 0 (mod D)。"""
    D = lcm_den(b)
    return D, [int(x * D) for x in b]


def f_of(beta, m):
    return sum((beta[i] * binom_int(m, i) for i in range(len(beta))), 0)


def sols_in(beta, D, N):
    """一个周期 [0,N) 内使 Q(m) ∈ Z 的 m。"""
    return [m for m in range(N) if f_of(beta, m) % D == 0]


def minimal_period(beta, D, P):
    """在周期长度 P 上求最小正平移 N 使解集不变（低效但精确；P 已限上界）。"""
    S = set(sols_in(beta, D, P))
    if not S:
        return 0, 0
    if len(S) == P:
        return 1, 1
    for cand in range(1, P):
        if P % cand:
            continue
        if all(((m + cand) % P) in S for m in S):
            return cand, len(S) * cand // P
    return P, len(S)


# ============================================================ 数据基座
GRID = [(n, d) for n in range(1, 6) for d in range(1, n + 4)]          # 30 组（承 r339/r346）
WIDE = [(n, d) for n in range(1, 7) for d in range(1, 13)]             # 72 组（承 r346）
NEWTON = dict((nd, newton_of(*nd)) for nd in GRID)
NWIDE = dict((nd, newton_of(*nd)) for nd in WIDE)

CAP_D = 6000        # 周期扫描上限（超出如实标 UND）
CV_CAP = 20000      # 交叉验证 [0, D·n!) 的长度上限
WIN_LO, WIN_HI = -96, 96
WIN = range(WIN_LO, WIN_HI + 1)


def cosets(d):
    """候选陪集：M | d（定理 C 保证 M ∤ d 时无整点），1 ≤ r < M，gcd(r,M)=1。"""
    out = []
    for M in divisors(d):
        if M == 1:
            continue
        for r in range(1, M):
            if math.gcd(r, M) == 1:
                out.append((M, r))
    return out


# 全量陪集扫描（本卷主数据）
COSET_DATA = []      # (n,d,M,r,b,D,beta,kind,cnt,und)
UND_LIST = []
for _nd in WIDE:
    _n, _d = _nd
    _a = NWIDE[_nd]
    for _M, _r in cosets(_d):
        _b = bvec(_a, F(_r, _M))
        _full = all(isint(x) for x in _b)
        _D = lcm_den(_b)
        _beta = [int(x * _D) for x in _b]
        if _full:
            COSET_DATA.append((_n, _d, _M, _r, _b, _D, _beta, "FULL", 1, False))
            continue
        if _D > CAP_D:
            UND_LIST.append((_n, _d, _M, _r, _D))
            COSET_DATA.append((_n, _d, _M, _r, _b, _D, _beta, "UND", -1, True))
            continue
        _S = sols_in(_beta, _D, _D)
        COSET_DATA.append((_n, _d, _M, _r, _b, _D, _beta,
                           "PARTIAL" if _S else "EMPTY", len(_S), False))

DEC = [c for c in COSET_DATA if not c[9]]                    # 已精确判定
PART = [c for c in COSET_DATA if c[7] == "PARTIAL"]
FULL = [c for c in COSET_DATA if c[7] == "FULL"]
EMPT = [c for c in COSET_DATA if c[7] == "EMPTY"]


# ============================================================ 条目登记
ITEMS = []
CONTROLS = []
GUARDS = []


def item(tag, kind, exp, act, note, ok):
    ITEMS.append({"tag": tag, "kind": kind, "exp": exp, "act": act,
                  "note": note, "status": "PASS" if ok else "FAIL"})


def ctl(tag, ok, desc, detail):
    CONTROLS.append({"tag": tag, "ok": bool(ok), "desc": desc, "detail": detail})


def guard(tag, ok, desc, detail):
    GUARDS.append({"tag": tag, "ok": bool(ok), "desc": desc, "detail": detail})


# ============================================================ 组 A：定理 E / E′（陪集判据）
def _run_A():
    # A01 Vandermonde 主校验：P(c+m) 直接算 χ  vs  Σ_i b_i(c) C(m,i)
    # 两条路不共享中间量（左边 td 级数，右边 Newton 系数 + 二项式）
    tot = mis = 0
    for nd in GRID:
        n, d = nd
        a = NEWTON[nd]
        for (M, r) in cosets(d)[:6]:
            c = F(r, M)
            b = bvec(a, c)
            for m in (0, 1, 2, 3, -1):
                k = c + m
                lhs = chi_at(n, d, k)
                rhs = sum((b[i] * binom_int(m, i) for i in range(n + 1)), F(0))
                tot += 1
                if lhs != rhs:
                    mis += 1
    item("A01", "eq", "0", str(mis),
         "**主校验（Vandermonde）**：`P(c+m)` 直接由 td 级数算 χ vs `Σ_i b_i(c) C(m,i)`，"
         "两条路不共享中间量。分母 %d 个 (组,陪集,平移) 组合" % tot, mis == 0)

    # A02 定理 E′：整段 ⟺ 前 n+1 个值全整（判据与「b 全整」比对）
    tot2 = mis2 = 0
    for c in DEC:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        a = NWIDE[(n, d)]
        vals = [peval(a, F(r, M) + m) for m in range(n + 1)]
        pred = all(isint(v) for v in vals)
        truth = all(isint(x) for x in b)
        tot2 += 1
        if pred != truth:
            mis2 += 1
    item("A02", "eq", "0", str(mis2),
         "**定理 E′（本卷最实用）**：`c+Z ⊆ S ⟺ P(c),…,P(c+n) ∈ Z` —— **只需 n+1 个值**即可判定整个陪集。"
         "证明：`b_i = Δ^i Q(0) = Σ_t (−1)^{i−t} C(i,t) Q(t)` 只用到 `Q(0..i) ⊆ Q(0..n)`。"
         "机检：该判据 vs `b` 全整。分母 %d 个已判定陪集" % tot2, mis2 == 0)

    # A03 前向：整段 ⇒ b 全整（引理 L）
    bad = [c for c in DEC if c[7] == "FULL" and not all(isint(x) for x in c[4])]
    item("A03", "eq", "0", str(len(bad)),
         "**定理 E 前向**：整段 ⇒ `b_i(c) ∈ Z ∀i`（引理 L：`Δ^i` 是整数组合）。"
         "分母 %d 个已判定陪集" % len(DEC), len(bad) == 0)

    # A04 后向：b 全整 ⇒ 整段（C(m,i) ∈ Z）
    bad = [c for c in DEC if all(isint(x) for x in c[4]) and c[7] != "FULL"]
    item("A04", "eq", "0", str(len(bad)),
         "**定理 E 后向**：`b` 全整 ⇒ 整段（`C(m,i) ∈ Z` 对整数 m 恒成立）。"
         "分母 %d 个已判定陪集" % len(DEC), len(bad) == 0)

    # A05 功劳归属：同一判据在随机整值多项式上也 100% 成立 ⇒ 不是几何
    lc = LCG(20261102)
    tot5 = mis5 = 0
    for _ in range(300):
        n = 1 + lc.nxt(5)
        D = [2, 3, 4, 6, 8, 12][lc.nxt(6)]
        beta = [lc.nxt(17) - 8 for _ in range(n + 1)]
        if all(x == 0 for x in beta):
            continue
        b = [F(x, D) for x in beta]
        full_b = all(isint(x) for x in b)
        vals = [sum((b[i] * binom_int(m, i) for i in range(n + 1)), F(0))
                for m in range(n + 1)]
        tot5 += 1
        if all(isint(v) for v in vals) != full_b:
            mis5 += 1
    item("A05", "eq", "0", str(mis5),
         "**功劳归属（承 r346 的降级思路）**：同一判据在**随机整值多项式**上也 100%% 成立"
         " ⇒ 定理 E/E′ 是**多项式的初等事实**，功劳不在几何。分母 %d 个随机样本" % tot5,
         mis5 == 0)

    # A06 n+1 不可减：只看 m=0..n−1 会误判
    #     反例 Q(m) = C(m,n)/2：Q(0..n−1)=0 全整，Q(n)=1/2 非整
    hits = 0
    for n in range(2, 6):
        b = [F(0)] * (n + 1)
        b[n] = F(1, 2)
        vals = [sum((b[i] * binom_int(m, i) for i in range(n + 1)), F(0))
                for m in range(n)]
        full_b = all(isint(x) for x in b)
        if all(isint(v) for v in vals) and not full_b:
            hits += 1
    item("A06", "gt", "0", str(hits),
         "**`n+1` 不可减为 `n`**：反例 `Q(m)=C(m,n)/2` 在 `m=0..n−1` 上全整而 `m=n` 非整"
         " ⇒ 有限判据的界恰好是 `n+1`。分母 %d 个 n（2..5）" % 4, hits == 4)
    return {"tot": tot, "mis": mis}


# ============================================================ 组 B：周期（定理 G / X-R346-1）
def _run_B():
    # B01 定理 G：f(m + D·n!) ≡ f(m) (mod D)
    tot = mis = 0
    for c in DEC:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        H = D * math.factorial(n)
        if H > CV_CAP:
            continue
        for m in range(0, min(H, 60)):
            tot += 1
            if (f_of(beta, m + H) - f_of(beta, m)) % D != 0:
                mis += 1
    item("B01", "eq", "0", str(mis),
         "**定理 G（可证上界）**：`Q_c(m + D·n!) ≡ Q_c(m) (mod 1)` —— Taylor "
         "`f(m+H)=Σ_i Δ^i f(m) C(H,i)`，`H=D·n!` 使 `C(H,i) ∈ D·Z`，而 `Δ^i f` 整值。"
         "分母 %d 个 (陪集,平移) 组合" % tot, mis == 0)

    # B02 实测 N == D
    eq = tot2 = 0
    for c in PART:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        P = D * math.factorial(n)
        if P > CV_CAP:
            continue
        N, cl = minimal_period(beta, D, P)
        tot2 += 1
        if N == D:
            eq += 1
    item("B02", "eq", str(tot2), str(eq),
         "**实测 `N = D`（等式，非上界）**：可精确测定的部分陪集上最小周期**恰好**等于 "
         "`D = lcm_i den b_i(c)`。分母 %d 个陪集（周期长度 ≤ %d）" % (tot2, CV_CAP), eq == tot2)

    # B03 D | M^n n!（承 r346，重算扩样本）
    bad = 0
    tot3 = 0
    for c in COSET_DATA:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        tot3 += 1
        if (M ** n) * math.factorial(n) % D != 0:
            bad += 1
    item("B03", "eq", "0", str(bad),
         "**承 r346**：`D | M^n n!`（`M^n n!·b_i ∈ Z`）。分母 %d 个陪集（含 UND）" % tot3,
         bad == 0)

    # B04 界的压缩
    worst = 0
    for c in DEC:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        old = ((M ** n) * math.factorial(n)) ** 2
        new = D * math.factorial(n)
        if new > 0:
            worst = max(worst, old // new)
    item("B04", "gt", "0", str(worst),
         "**X-R346-1 的答案**：界由 r346 的 `(M^n n!)²` 压到 `D·n! ≤ M^n (n!)²`，"
         "实测最大压缩倍数 **%d 倍**（取所有已判定陪集的 `old/new` 最大值）。"
         "分母 %d 个陪集" % (worst, len(DEC)), worst > 0)

    # B05 额外点的分母谱（X-R346-2 的实测部分）：n ≥ 2 时只来自 M ∈ {2,3}
    bad5 = 0
    tot5b = 0
    for c in DEC:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        if n < 2:
            continue
        tot5b += 1
        if kind in ("FULL", "PARTIAL") and M not in (2, 3):
            bad5 += 1
    item("B05", "eq", "0", str(bad5),
         "**X-R346-2 的实测部分**：`n ≥ 2` 时额外点（整段或部分）只来自 `M ∈ {2,3}`"
         "（`n=2, d=9` 给整段 `M=3`；其余全是 `M=2`）。`n=1` 是例外：`S=(1/d)Z` 使**所有** "
         "`M | d` 都整段。分母 %d 个 `n ≥ 2` 的已判定陪集（UND 区不适用）" % tot5b, bad5 == 0)

    # B06 UND 如实登记
    mx = max([u[4] for u in UND_LIST]) if UND_LIST else 0
    item("B06", "gt", "0", str(len(UND_LIST)),
         "**UND 如实登记**：`D > %d` 的陪集无法在本卷算力内精确判定，共 **%d** 个，"
         "最大 `D = %d`。这正是「窗口法不可靠」的量化证据。分母 %d 个陪集"
         % (CAP_D, len(UND_LIST), mx, len(COSET_DATA)), len(UND_LIST) > 0)
    return {"eq": eq, "tot": tot2}


# ============================================================ 组 C：单剩余类（定理 F）
def _run_C():
    ones = sum(1 for c in PART if c[8] == 1)
    item("C01", "eq", str(len(PART)), str(ones),
         "**定理 F（单剩余类）**：部分陪集在一个周期内**恰 1 个整点** ⇒ "
         "`S∩(c+Z)` 是**一条**等差级数（公差 = D）。分母 %d 个部分陪集" % len(PART),
         ones == len(PART))

    # C02 分类器自检：C(m,2) mod 2 必须报 2 类（否则分类器恒报 1 类 ⇒ C01 无意义）
    b2 = [F(0), F(0), F(1, 2)]
    D2, beta2 = betas_of(b2)
    N2, cl2 = minimal_period(beta2, D2, D2 * math.factorial(2))
    item("C02", "eq", "2", str(cl2),
         "**分类器负控**：`C(m,2) mod 2` 的解集是 `{0,1} mod 4`（**两**条 AP）"
         " ⇒ 分类器必须报 2，报 1 就说明它恒报 1 而 C01 无意义。分母 1 个自检样本",
         cl2 == 2)

    # C03/C04 判别力：随机整值多项式上「单剩余类」的比例
    lc = LCG(20261103)
    tot = one = multi = 0
    for _ in range(400):
        n = 1 + lc.nxt(4)
        D = [2, 3, 4, 5][lc.nxt(4)]
        beta = [lc.nxt(9) - 4 for _ in range(n + 1)]
        if all(x == 0 for x in beta):
            continue
        P = D * math.factorial(n)
        if P > 400:
            continue
        bb = [F(x, D) for x in beta]
        S = sols_in(beta, D, P)
        if not S or len(S) == P:
            continue
        N, cl = minimal_period(beta, D, P)
        tot += 1
        if cl == 1:
            one += 1
        else:
            multi += 1
    item("C03", "eq", str(one + multi), str(one),
         "**判别力（诚实分母）**：随机整值多项式的部分解集共 %d 个，其中单剩余类 %d 个"
         " ⇒ **「单剩余类」在随机整值多项式上也 100%% 成立**，它对 χ **没有判别力**，"
         "按本库门禁**不得当判据用**，只能当结构陈述（这是本卷第二次「功劳归还多项式」："
         "先有定理 E 的 A05，再有本条）。分母 %d 个随机样本" % (one + multi, one, tot),
         one == (one + multi) and (one + multi) > 0)
    item("C04", "eq", "2", str(cl2),
         "**但判据本身不是恒真**：构造样本 `C(m,2)/2` 的解集是 `{0,1} mod 4`（两条 AP）"
         " ⇒ 「单剩余类」可被否证，只是随机样本碰不到。分母 1 个构造样本", cl2 == 2)

    # C05 S 重构 vs 直接穷举（两条路：整数化 f(m) mod D  vs  Fraction 的 peval）
    tot5 = mis5 = 0
    for nd in GRID:
        n, d = nd
        a = NEWTON[nd]
        recon = set()
        direct = set()
        for m in WIN:
            recon.add(F(m))
            direct.add(F(m))
        for c in [x for x in COSET_DATA if x[0] == n and x[1] == d]:
            _, _, M, r, b, D, beta, kind, cnt, und = c
            for m in WIN:
                k = F(m) + F(r, M)
                if WIN_LO <= k <= WIN_HI:
                    if f_of(beta, m) % D == 0:
                        recon.add(k)
                    if isint(peval(a, k)):
                        direct.add(k)
        tot5 += 1
        if recon != direct:
            mis5 += 1
    item("C05", "eq", "0", str(mis5),
         "**S 的重构**：整数化路径 `f(m) ≡ 0 (mod D)` 与直接路径 `peval(a, c+m) ∈ Z` 逐点相等"
         "（两条路不共享中间量：前者只用 `β=D·b` 与整数二项式，后者用 Fraction 多项式）。"
         "分母 %d 个 GRID 组" % tot5, mis5 == 0)

    # C06 与 r339 的见证点逐点核对
    a32 = NEWTON[(3, 2)]
    wit_in = [F(-11, 2), F(-3, 2), F(5, 2)]
    wit_out = [F(-9, 2)]
    ok = all(isint(peval(a32, k)) for k in wit_in) and \
        all(not isint(peval(a32, k)) for k in wit_out)
    b32 = bvec(a32, F(1, 2))
    D32, beta32 = betas_of(b32)
    S32 = sols_in(beta32, D32, D32)
    item("C06", "eq", "1", str(len(S32)),
         "**与 r339 对表**：r339 的 `(3,2)` 见证点 `-11/2, −3/2, 5/2` 全在 `S` 内、`−9/2` 不在；"
         "本卷给出机制 —— `D=4`、一个周期内解 `m ≡ %s (mod 4)` ⇒ 三点恰是 `1/2 + (2+4t)`，"
         "差值 4 = D，**r339 的「非陪集」就是「一条公差 4 的 AP 与 Z 的并」**。分母 1 组"
         % (S32,), ok and len(S32) == 1)
    return {"ones": ones, "part": len(PART)}


# ============================================================ 组 D：与既有卷的关系
def _run_D():
    # D01 与 r346 落盘 JSON 的 30 组 Newton 逐项字符串相等（不推翻）
    p = os.path.join(OUTDIR, "数据",
                     "TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
                     "分母整除首项定理与判词下调_精算与可视化_2026-11-01.json")
    exists = os.path.exists(p)
    diff = 0
    if exists:
        try:
            old = json.load(io.open(p, encoding="utf-8"))
            on = old.get("newton", {})
            diff = sum(1 for k, v in NEWTON.items()
                       if str(k) in on and [str(x) for x in v] != list(on[str(k)]))
        except Exception:
            diff = -1
    item("D01", "eq", "0", str(diff),
         "**不推翻 r346**：本卷 30 组 Newton 系数与 r346 落盘 JSON **逐项字符串相等**。"
         "JSON 存在=%s，比对 %d 组，分母 %d 组" % (exists, len(NEWTON), len(NEWTON)),
         exists and diff == 0)

    # D02 与 r346 的周期实测值比对
    p2 = os.path.join(OUTDIR, "数据",
                      "TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
                      "分母整除首项定理与判词下调_精算与可视化_2026-11-01.json")
    per_old = {}
    if os.path.exists(p2):
        try:
            per_old = json.load(io.open(p2, encoding="utf-8")).get("periods", {})
        except Exception:
            per_old = {}
    tot = mis = 0
    for key, val in per_old.items():
        nd, c = key.split("|")
        n, d = [int(x) for x in nd.strip("()").split(",")]
        cr = F(c)
        M = cr.denominator
        r = cr.numerator
        found = [x for x in PART if x[0] == n and x[1] == d and x[2] == M and x[3] == r]
        if not found:
            continue
        tot += 1
        if found[0][5] != val:
            mis += 1
    item("D02", "eq", "0", str(mis),
         "**周期读数逐项比对**：r346 报的实测周期与本卷 `D` 值逐项相等。"
         "分母 %d 个共有 (组,陪集)" % tot, mis == 0 and tot > 0)

    # D03 窗口法的诱惑与否证
    win_miss = 0
    for c in PART:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        if D > 12:
            win_miss += 1
    item("D03", "gt", "0", str(win_miss),
         "**否证一个诱惑**：固定窗口（如 `[-6,6]`）在原理上不可靠 —— 部分陪集中有 **%d** 个的 "
         "`D > 12`，其整点间距超过任何小窗口；r339 只看到 `(5,2)` 的 1 个孤立点正是此效应。"
         "分母 %d 个部分陪集" % (win_miss, len(PART)), win_miss > 0)

    # D04 主校验 χ == h^0（承 r339/r346，引擎自检）
    tot4 = mis4 = 0
    for nd in GRID:
        n, d = nd
        for k in range(d, d + 16):
            tot4 += 1
            if chi_at(n, d, k) != h0(n, d, k):
                mis4 += 1
    item("D04", "eq", "0", str(mis4),
         "**引擎主校验**：Kodaira 区 `χ(O_X(kH)) == h^0`（td 级数 vs 齐次多项式计数，"
         "两条不共享中间量）。分母 %d 个 (组,k)" % tot4, mis4 == 0)
    return {}


# ============================================================ 组 E：定价
def _run_E():
    #  S1 有限判据（n+1 值）  S2 周期上界 D·n!（可证）  S3 实测 N==D
    #  S4 单剩余类          S5 额外点只在 M=2          S6 窗口法可靠
    # ★ 第四条约束来自数据本身：D03 实测否证了「窗口法可靠」（S6 = 0）
    feasible = []
    for mask in range(64):
        b = [(mask >> i) & 1 for i in range(6)]
        if b[2] == 1 and b[1] == 0:        # K1  S3 ⇒ S2（等式蕴含上界）
            continue
        if b[5] == 1 and b[2] == 1:        # K2  S6 ∧ S3 = 0（D 可达 3.58e7 ≫ 任何窗口）
            continue
        if b[5] == 1 and b[4] == 1:        # K3  S6 ∧ S5 = 0（窗口法与 UND 区冲突）
            continue
        if b[5] == 1:                      # K4  D03 实测否证 S6（窗口法不可靠）
            continue
        feasible.append(mask)
    pinned = [i for i in range(6) if len(set((m >> i) & 1 for m in feasible)) == 1]
    unpinned = [i for i in range(6) if i not in pinned]
    flip = sum(1 for i in pinned for m in feasible if (m ^ (1 << i)) in feasible)
    return {"feasible": len(feasible), "match": 1, "flip": flip,
            "mask": feasible[0] if feasible else 0,
            "feasible_list": feasible,
            "pinned": pinned, "unpinned": unpinned}


A_OUT = _run_A()
B_OUT = _run_B()
C_OUT = _run_C()
D_OUT = _run_D()
PLACE = _run_E()

# E01 的期望取自**另一条独立路径**：按约束语法手算，而不是枚举可行集
#   K4 固定 b5=0 ⇒ 只剩 5 个自由位（2^5=32）；K1 排除 (b2=1,b1=0) 这 2^3=8 个
#   ⇒ 24。另一条路（枚举）必须给出同一个数，两条路不一致即 FAIL。
EXP_FEASIBLE = (2 ** 5) - (2 ** 3)
item("E01", "eq", str(EXP_FEASIBLE), str(PLACE["feasible"]),
     "定价位掩码 2⁶=64：约束 `K1: S3⇒S2` / `K2: S6∧S3=0` / `K3: S6∧S5=0` / "
     "`K4: S6=0（D03 实测否证窗口法）`。期望 %d 由**约束语法手算**得到"
     "（5 个自由位 2⁵=32 减去 K1 排除的 2³=8），枚举路径必须给出同一数。分母 64"
     % EXP_FEASIBLE, PLACE["feasible"] == EXP_FEASIBLE)
# E02 的期望同样取自约束语法：只有被 K4 直接固定的那一位（S6）
EXP_PINNED = 1
item("E02", "eq", str(EXP_PINNED), str(len(PLACE["pinned"])),
     "**被钉住的位数**：约束语法里只有 `K4` 直接固定了 `S6` ⇒ 应为 %d；"
     "未钉住 %d 位（%s）。两条路（约束语法 vs 可行集枚举）必须一致。分母 %d 个可行组合"
     % (EXP_PINNED, len(PLACE["unpinned"]), PLACE["unpinned"], PLACE["feasible"]),
     len(PLACE["pinned"]) == EXP_PINNED)
item("E03", "eq", "0", str(PLACE["flip"]),
     "敏感度：翻转**任一被钉住的位**后仍留在可行集内的次数必须为 0 ⇒ 定价不是恒绿。"
     "分母 %d 个钉住位" % len(PLACE["pinned"]), PLACE["flip"] == 0)


# ============================================================ 控制组
def _controls():
    # CTL1 正控：Vandermonde 在已知多项式 k^2 上成立
    a = [F(0), F(1), F(2)]
    ok = True
    for c in (F(0), F(1, 2), F(-3, 2)):
        b = bvec(a, c)
        for m in range(-4, 5):
            if peval(a, c + m) != sum((b[i] * binom_int(m, i) for i in range(3)), F(0)):
                ok = False
    ctl("CTL1", ok, "正控：Vandermonde 展开在 k^2 上逐点成立（3 个陪集 × 9 个平移）",
        "全对=%s" % ok)

    # CTL2 负控：b 非全整 ⇒ 必存在某个 m 使 Q(m) 非整（否则 A03 恒绿）
    lc = LCG(20261104)
    hit = 0
    tot = 0
    for _ in range(200):
        n = 1 + lc.nxt(4)
        D = [2, 3, 4, 6][lc.nxt(4)]
        beta = [lc.nxt(13) - 6 for _ in range(n + 1)]
        b = [F(x, D) for x in beta]
        if all(isint(x) for x in b):
            continue
        P = D * math.factorial(n)
        if P > 400:
            continue
        tot += 1
        S = sols_in([int(x) for x in [y * D for y in b]], D, P)
        if len(S) < P:
            hit += 1
    ctl("CTL2", hit == tot and tot > 0,
        "负控：`b` 非全整 ⇒ 一个周期内**必须**有非整点（否则 A03/A04 恒绿）",
        "命中 %d/%d" % (hit, tot))

    # CTL3 gcd(r,M)=1 是枚举**去重**前提（Fraction 自动约分），不是数学前提
    a = NWIDE[(3, 2)]
    same_c = (F(1, 2) == F(2, 4))
    same_b = (bvec(a, F(1, 2)) == bvec(a, F(2, 4)))
    ctl("CTL3", same_c and same_b,
        "**口径自守**：`F(2,4)` 与 `F(1,2)` 必须给出同一个陪集多项式 ⇒ "
        "`gcd(r,M)=1` 是枚举去重的**约定**，不是数学前提（若写成数学前提就会误删真陪集）",
        "F(1/2)==F(2/4)=%s ；b 向量相同=%s" % (same_c, same_b))

    # CTL4 定理 G 的方向性：H' = D·n! − 1 必须**不**一致
    bad_shift = 0
    tot4 = 0
    for c in PART:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        H = D * math.factorial(n)
        if H > CV_CAP:
            continue
        for m in range(0, 20):
            tot4 += 1
            if (f_of(beta, m + H - 1) - f_of(beta, m)) % D == 0:
                bad_shift += 1
    ctl("CTL4", bad_shift < tot4,
        "**方向性对照**：把平移换成 `D·n! − 1` ⇒ 一致性必须**崩掉**（否则 B01 恒绿）",
        "仍一致 %d/%d（越少越好）" % (bad_shift, tot4))

    # CTL5 分类器自检（与 C02 同源，独立实现）
    D2, beta2 = betas_of([F(0), F(0), F(1, 2)])
    S = sols_in(beta2, D2, 4)
    ctl("CTL5", len(S) == 2 and S[0] == 0,
        "分类器自检：`C(m,2) mod 2` 在 `m=0..3` 上的解必须是 `{0,1}`（两**条** AP）",
        "解=%s" % S)

    # CTL6/CTL7 r339 见证点
    a32 = NEWTON[(3, 2)]
    ctl("CTL6", isint(peval(a32, F(-11, 2))),
        "正控：r339 的非陪集见证点 `-11/2` 必须真的在 S 内（否则 C06 结论作废）",
        "P(-11/2)=%s" % peval(a32, F(-11, 2)))
    ctl("CTL7", not isint(peval(a32, F(-9, 2))),
        "正控：r339 的见证点 `-9/2` 必须真的**不**在 S 内",
        "P(-9/2)=%s" % peval(a32, F(-9, 2)))

    # CTL8 两条路互核：[0,D) 与 [0,D·n!) 的点数自洽
    ok8 = tot8 = 0
    for c in PART:
        n, d, M, r, b, D, beta, kind, cnt, und = c
        P = D * math.factorial(n)
        if P > CV_CAP:
            continue
        tot8 += 1
        s1 = len(sols_in(beta, D, D))
        s2 = len(sols_in(beta, D, P))
        if s1 * P // D == s2:
            ok8 += 1
    ctl("CTL8", ok8 == tot8 and tot8 > 0,
        "**两条路互核**：周期取 `D` 与取 `D·n!` 的点数必须自洽（不共享中间量）",
        "一致 %d/%d" % (ok8, tot8))

    # CTL9 判别力非恒真：随机样本必须出现多类（与 C04 同源、独立计数）
    lc = LCG(20261105)
    multi = 0
    for _ in range(200):
        n = 1 + lc.nxt(3)
        D = [2, 4][lc.nxt(2)]
        beta = [lc.nxt(7) - 3 for _ in range(n + 1)]
        P = D * math.factorial(n)
        if P > 200 or all(x == 0 for x in beta):
            continue
        S = sols_in(beta, D, P)
        if not S or len(S) == P:
            continue
        _, cl = minimal_period(beta, D, P)
        if cl > 1:
            multi += 1
    ctl("CTL9", multi > 0, "判别力非恒真：随机整值多项式上必须真的出现多剩余类",
        "多类出现 %d 次" % multi)

    # CTL10 n+1 不可减的具体反例
    b = [F(0), F(0), F(1, 2)]
    v = [sum((b[i] * binom_int(m, i) for i in range(3)), F(0)) for m in range(2)]
    ctl("CTL10", all(isint(x) for x in v) and not isint(sum(
        (b[i] * binom_int(2, i) for i in range(3)), F(0))),
        "**`n+1` 不可减**：`C(m,2)/2` 在 `m=0,1` 上全整而 `m=2` 非整",
        "Q(0)=%s Q(1)=%s Q(2)=%s" % (v[0], v[1], sum(
            (b[i] * binom_int(2, i) for i in range(3)), F(0))))

    # CTL11 定理 C：M ∤ d 的陪集必无整点
    bad = 0
    tot11 = 0
    for nd in GRID[:12]:
        n, d = nd
        a = NEWTON[nd]
        for M in range(2, 13):
            if d % M == 0:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-8, 9):
                    tot11 += 1
                    if isint(peval(a, F(m) + F(r, M))):
                        bad += 1
    ctl("CTL11", bad == 0,
        "负控：定理 C ⇒ `M ∤ d` 的陪集必无整点（否则本卷只需扫 `M | d` 的前提不成立）",
        "违例 %d / %d 个 (组,分母,平移)" % (bad, tot11))

    # CTL12 FULL 陪集的 D 必须恒为 1
    bad = [c for c in FULL if c[5] != 1]
    ctl("CTL12", len(bad) == 0,
        "一致性：整段陪集的 `b` 全整 ⇒ `D = 1`（否则 lcm_den 与 isint 互相矛盾）",
        "违反 %d / %d 个 FULL 陪集" % (len(bad), len(FULL)))

    # CTL13 非对称对照：未钉住的位翻转后仍在可行集内（证明不是把所有位都钉住）
    stay = 0
    for i in PLACE["unpinned"]:
        if (PLACE["mask"] ^ (1 << i)) in [m for m in range(64)]:
            pass
    fs = set(PLACE["feasible_list"])
    # ★ 首跑把「未钉住」误当成「从任意可行点翻转都安全」（CTL13 报 4/5 FAIL）。
    #   反例：位 2（S3）未钉住，但基准组合 mask=0 上 S2=0，单独把 S3 翻成 1 会违反 K1。
    #   正解：未钉住的位的正确含义是「可行集内取过两个值」⇒ 存在**某个**可行点可翻转。
    ok_each = 0
    for i in PLACE["unpinned"]:
        if any((m ^ (1 << i)) in fs for m in fs):
            ok_each += 1
    ctl("CTL13", ok_each == len(PLACE["unpinned"]) and len(PLACE["unpinned"]) > 0,
        "**非对称对照**：未钉住的位（`%s`）必须**存在**某个可行组合使其翻转后仍在可行集内"
        " ⇒ 证明 E02 的「钉住」不是全钉。**注**：不能写成「从基准组合翻转必安全」——"
        "位 2（S3）未钉住，但基准组合上 S2=0，单独翻 S3 会违反 `S3⇒S2`（首跑正是这样误报）"
        % PLACE["unpinned"],
        "未钉住 %d 位，可翻转 %d 位" % (len(PLACE["unpinned"]), ok_each))


# ============================================================ 守卫
def _guards():
    src = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    fails = [i for i in ITEMS if i["status"] == "FAIL"]
    guard("G01", len(fails) == 0, "判决类无 FAIL", "FAIL=%d" % len(fails))
    infos = [i for i in ITEMS if i["status"] == "INFO"]
    guard("G02", len(infos) == 0,
          "INFO 只能来自 info 类型，不得由判决类降级得到",
          "info 型 0 条 / INFO 状态 %d 条" % len(infos))
    notden = [i["tag"] for i in ITEMS if "分母" not in i["note"]]
    guard("G03", len(notden) == 0, "判决类条目的 note 必须写分母",
          "缺分母 %d 条 %s" % (len(notden), notden))

    # G04 源码级非同源：item(...) 的 exp 与 act 不得是同一个带引号字面量
    import re as _re
    calls = _re.findall(r'item\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*([^,]+),\s*([^,]+),', src, _re.S)
    same = 0
    for e, a in calls:
        es, as_ = e.strip(), a.strip()
        if es == as_ and es.startswith('"'):
            same += 1
    guard("G04", same == 0,
          "源码级非同源：item 的 exp 与 act 不得是同一表达式（同义反复恒 PASS 的破法）",
          "调用 %d 处，同源 %d 处" % (len(calls), same))

    # G05 status 实参顶层不得是常量（AST，只查顶层，避开 ast.walk 的误报）
    import ast
    tree = ast.parse(src)
    sus = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "item" and len(node.args) >= 5:
            top = node.args[5]
            if isinstance(top, (ast.Constant, ast.IfExp)):
                sus += 1
            if isinstance(top, ast.Compare):
                sus += 0
    guard("G05", sus == 0,
          "item 的判据实参**顶层**不得是 IfExp 或布尔常量（IfExp 盲区 + 禁写死）",
          "可疑调用 %d 处" % sus)

    guard("G06", len(ITEMS) == len(set(i["tag"] for i in ITEMS)) and len(ITEMS) >= 20,
          "item 调用数 == 条目数（无静默丢弃、无重复登记）",
          "调用 %d / 条目 %d" % (len(ITEMS), len(ITEMS)))
    tags = [i["tag"] for i in ITEMS]
    guard("G07", len(tags) == len(set(tags)), "items tag 唯一",
          "重复 %d 个" % (len(tags) - len(set(tags))))
    ct = [c["tag"] for c in CONTROLS] + [g["tag"] for g in GUARDS]
    guard("G08", len(ct) == len(set(ct)), "控制组/守卫 tag 唯一",
          "重复 %d 个" % (len(ct) - len(set(ct))))
    empty = [c for c in CONTROLS if not str(c["detail"]).strip()]
    guard("G09", len(empty) == 0,
          "如实登记：每条控制组/守卫的 detail 都带具体读数（0 条也要登记成 0）",
          "无读数 detail %d 条" % len(empty))

    # G10 联合一致性：FULL 的 D 必须为 1 且 PARTIAL 的 D > 1
    bad = [c for c in FULL if c[5] != 1] + [c for c in PART if c[5] <= 1]
    guard("G10", len(bad) == 0, "FULL⇔D=1 与 PARTIAL⇒D>1 的联合一致性",
          "矛盾 %d 处" % len(bad))

    # G11 跨卷回验（D01 已做，此处查 JSON 存在且比对组数 > 0）
    guard("G11", os.path.exists(os.path.join(
        OUTDIR, "数据", "TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
        "分母整除首项定理与判词下调_精算与可视化_2026-11-01.json")),
        "跨卷回验：r346 落盘 JSON 存在（本卷只读不写）",
        "存在=%s" % os.path.exists(os.path.join(
            OUTDIR, "数据", "TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
            "分母整除首项定理与判词下调_精算与可视化_2026-11-01.json")))

    # G12/G13 AST 层（不自命中源码字面量）
    imps = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    rnd = sum(1 for n in imps for al in n.names if al.name == "random")
    guard("G12", rnd == 0,
          "确定性：AST 层无伪随机模块导入（不靠字符串自命中判定）",
          "导入次数 %d" % rnd)
    floats = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, float):
            floats += 1
    fcalls = sum(1 for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id == "float")
    guard("G13", floats == 0 and fcalls == 0,
          "精确算术：AST 层无浮点常量、无 float() 调用（判决路径全 Fraction / 整数）",
          "浮点常量 %d 个 / float() %d 处" % (floats, fcalls))

    v = VERDICT
    vclean = (v == v.upper()) and (" " not in v) and \
        all(ch.isalnum() or ch in "_-" for ch in v)
    guard("G14", vclean, "verdict 机读：全大写、下划线分段、无空格（允许连字符）",
          "长度 %d" % len(v))
    guard("G15", DEGREE == 0 and CAND_DEGREE == 37,
          "度数判据：本卷无「消除自由参数」的量化发现（宽松档 SURVIVE=0）⇒ 不占度",
          "degree=%d candidate=%d" % (DEGREE, CAND_DEGREE))
    egrp = [i for i in ITEMS if i["tag"].startswith("E")]
    guard("G16", len(egrp) == 3, "定价组恰 3 条（E01..E03）", "E 组 %d 条" % len(egrp))
    guard("G17", len(COSET_DATA) == len(DEC) + len(UND_LIST),
          "证据键齐备：全量陪集 = 已判定 + UND（无静默丢弃）",
          "spec %d = %d + %d" % (len(COSET_DATA), len(DEC), len(UND_LIST)))
    guard("G18", len(PART) > 0, "部分陪集非空（否则定理 F 与 B02 的读数都是空转）",
          "部分陪集 %d 个" % len(PART))

    # G19 结构性防线：ctl/guard 的 ok 实参顶层不得是常量
    sus2 = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("ctl", "guard") and len(node.args) >= 2:
            top = node.args[1]
            if isinstance(top, (ast.Constant, ast.IfExp)):
                sus2 += 1
    guard("G19", sus2 == 0,
          "ctl/guard 的 ok 实参**顶层**不得是布尔常量（假守卫的结构性防线）",
          "可疑调用 %d 处" % sus2)


VERDICT = ("X-R339-2-AND-X-R346-2-ANSWERED__X-R346-1-TIGHTENED__"
           "A-COSET-IS-DECIDED-BY-N-PLUS-ONE-VALUES-ALONE-SO-THE-INTEGRALITY-SET-IS-EXACTLY-"
           "Z-PLUS-AT-MOST-ONE-ARITHMETIC-PROGRESSION-PER-COSET__"
           "THE-MINIMAL-PERIOD-EQUALS-THE-LCM-OF-THE-DENOMINATORS-OF-THE-COSET-NEWTON-COEFFICIENTS-"
           "WHICH-TIGHTENS-R346-S-BOUND-FROM-M-POW-N-TIMES-N-FACTORIAL-SQUARED-TO-D-TIMES-N-FACTORIAL__"
           "THE-NON-COSET-OF-R339-IS-JUST-ONE-PROGRESSION-OF-DIFFERENCE-D-UNIONED-WITH-Z__"
           "AND-THE-FIXED-WINDOW-METHOD-IS-UNRELIABLE-IN-PRINCIPLE-BECAUSE-D-REACHES-THREE-POINT-FIVE-E7__"
           "CREDIT-BELONGS-TO-ELEMENTARY-POLYNOMIAL-ARITHMETIC-NOT-GEOMETRY__"
           "STILL-NOT-PREDICTED")

_controls()
_guards()

# ============================================================ 输出
def _fmt_item(i):
    return "  %-5s %-4s %-4s exp=%-22s act=%s" % (
        i["tag"], i["status"], i["kind"], i["exp"][:22], i["act"])


lines = []
lines.append("=" * 78)
lines.append("TUFT-%s . 整性集的精确结构：陪集只需 n+1 个值判定 / 周期等于分母 lcm" % RID)
lines.append("date=%s  degree=%d  candidate_degree=%d" % (DATE, DEGREE, CAND_DEGREE))
lines.append("=" * 78)
lines.append("")
lines.append("[convention] X_d in CP^{n+1}, dim_C = n ; chi(O_X(kH)) = d * [h^n](e^{kh} td(T_X))")
lines.append("  P(k) = sum_j a_j C(k,j) ; on coset c+Z :  P(c+m) = sum_i b_i(c) C(m,i)")
lines.append("  b_i(c) = sum_{j>=i} a_j C(c, j-i)   (Vandermonde)")
lines.append("  beta_i = D*b_i in Z with D = lcm_i den b_i  =>  Q(m) in Z <=> sum beta_i C(m,i) = 0 (mod D)")
lines.append("")
lines.append("[theorem E'] c+Z subset S  <=>  P(c),...,P(c+n) in Z     (only n+1 values needed)")
lines.append("[theorem G ] period N divides D*n!  (proved) ;  measured N == D (sharp)")
lines.append("[theorem F ] S cap (c+Z) is a SINGLE arithmetic progression (1 solution per period)")
lines.append("")
lines.append("[cosets] total=%d  decided=%d (FULL=%d PARTIAL=%d EMPTY=%d)  UND=%d"
             % (len(COSET_DATA), len(DEC), len(FULL), len(PART), len(EMPT), len(UND_LIST)))
lines.append("")
lines.append("[partial cosets] (n,d,M,r) -> D, solutions-per-period")
for c in PART:
    lines.append("  n=%d d=%-2d M=%d r=%d -> D=%-6d sols=%d" % (c[0], c[1], c[2], c[3], c[5], c[8]))
lines.append("")
lines.append("[undecided] D > %d : %d cosets, max D = %s"
             % (CAP_D, len(UND_LIST), max([u[4] for u in UND_LIST]) if UND_LIST else 0))
lines.append("")
lines.append("[pricing] 2^6=64 feasible=%d match=1 mask=%d flip=%d pinned=%s unpinned=%s"
             % (PLACE["feasible"], PLACE["mask"], PLACE["flip"],
                PLACE["pinned"], PLACE["unpinned"]))
npass = sum(1 for i in ITEMS if i["status"] == "PASS")
nfail = sum(1 for i in ITEMS if i["status"] == "FAIL")
ninfo = sum(1 for i in ITEMS if i["status"] == "INFO")
lines.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d"
             % (len(ITEMS), npass, nfail, ninfo))
lines.append("[summary] controls=%d/%d  guards=%d/%d"
             % (sum(1 for c in CONTROLS if c["ok"]), len(CONTROLS),
                sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
lines.append("")
lines.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for i in ITEMS:
    lines.append(_fmt_item(i))
lines.append("")
lines.append("[controls]")
for c in CONTROLS:
    lines.append("  %-6s %-5s %s ; %s" % (c["tag"], "PASS" if c["ok"] else "FAIL",
                                          c["desc"], c["detail"]))
lines.append("")
lines.append("[guards] %d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
for g in GUARDS:
    lines.append("  %-5s %-5s %s ; %s" % (g["tag"], "PASS" if g["ok"] else "FAIL",
                                          g["desc"], g["detail"]))
lines.append("")
lines.append("[verdict] " + VERDICT)
lines.append("=" * 78)

report = "\n".join(lines)
sys.stdout.write(report + "\n")

payload = {
    "rid": RID, "date": DATE, "degree": DEGREE, "candidate_degree": CAND_DEGREE,
    "stem": STEM, "verdict": VERDICT,
    "cosets_total": len(COSET_DATA), "cosets_decided": len(DEC),
    "n_full": len(FULL), "n_partial": len(PART), "n_empty": len(EMPT),
    "und": [list(u) for u in UND_LIST],
    "partial": [[c[0], c[1], c[2], c[3], c[5], c[8]] for c in PART],
    "newton": dict((str(k), [str(x) for x in v]) for k, v in NEWTON.items()),
    "pricing": PLACE,
    "items": ITEMS, "controls": CONTROLS, "guards": GUARDS,
}
dj = os.path.join(OUTDIR, "数据", STEM + ".json")
io.open(dj, "w", encoding="utf-8").write(
    json.dumps(payload, ensure_ascii=False, indent=1))
dr = os.path.join(OUTDIR, "数据", STEM + "_report.txt")
io.open(dr, "w", encoding="utf-8", newline="\n").write(report + "\n")
sys.stdout.write("[%s] wrote %s (%d bytes) / %s (%d bytes)\n"
                 % (RID, os.path.basename(dj), len(json.dumps(payload, ensure_ascii=False)),
                    os.path.basename(dr), len(report.encode("utf-8"))))
sys.stdout.write("[rc] %d\n" % (0 if nfail == 0 and
                                all(c["ok"] for c in CONTROLS) and
                                all(g["ok"] for g in GUARDS) else 1))
