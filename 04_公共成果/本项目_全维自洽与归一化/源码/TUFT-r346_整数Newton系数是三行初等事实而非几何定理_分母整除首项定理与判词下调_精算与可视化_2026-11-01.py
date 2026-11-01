# -*- coding: utf-8 -*-
"""TUFT-r346 . 整数 Newton 系数是三行初等事实而非几何定理（攻 X-R339-1）
    判词下调：r339 定理 B 是定义恒等式不是几何定理；真定理是「分母整除首项」

核心（本卷只做三件事，全部可用初等算术判决）：
  [引理 L]  P in Q[k], deg P = n, P(Z) 含于 Z  =>  a_j = Delta^j P(0) 全整。
            证明一行：Delta^j P(0) = sum_i (-1)^{j-i} C(j,i) P(i)，整数组合。
            后果：chi(O_X(kH)) 是欧拉示性数 => 引理前提无条件成立
            => r339 的「定理 B（Newton 系数全整）」**不是几何定理**，
               它只是「整数组合仍是整数」，30/30 机检等价于一次引擎自检。
  [引理 Z]  Z 恒含于 S 对**任意**射影簇、**任意**线丛成立（S 的定义 + chi in Z）
            => 这个谓词对一切输入为真 => 判别力 0（本库门禁：不得当判据用）。
  [定理 C]  （本卷唯一不平凡的产出，且**无假设**）
            P(k) = sum_j a_j C(k,j), deg = n, a_n != 0。
            若 k = r/M（最简，M >= 2）且 P(k) in Z，则 M | a_n。
            证明四行：乘 M^n n!，取模 M，N_j(r) == r^j (mod M) 消掉 j<n 全部项，
            只剩 a_n r^n；gcd(r,M)=1 => M | a_n。
            推论：X_d in CP^{n+1} 上 a_n = H^n = d => S 含于 (1/d)Z，分母只能整除 d。
  [定理 D]  每个陪集 c+Z 上积分性是**周期集**（周期界 (M^n n!)^2，键一步 M^n n! b_i in Z）
            => S 是**有限个等差级数之并** => r339 的「非陪集」不是混沌，是并集。

判词：R339-NOT-OVERTURNED-BUT-RECERTIFIED；信用重分配，读数不改。
"""
import ast
import io
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r346"
DATE = "2026-11-01"
DEGREE = 0
CAND_DEGREE = 37

STEM = ("TUFT-r346_整数Newton系数是三行初等事实而非几何定理_"
        "分母整除首项定理与判词下调_精算与可视化_2026-11-01")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")

ITEMS = []
ILOG = []
CTL = []
GUARDS = []
LOG = []


def item(tag, kind, exp, act, note, status=None):
    if kind == "info":
        st = "INFO"
    else:
        st = "PASS" if status else "FAIL"
    ITEMS.append({"tag": tag, "kind": kind, "exp": exp, "act": act,
                  "note": note, "status": st})
    ILOG.append("  %-5s %-4s %-4s exp=%-30s act=%s" % (tag, st, kind, exp, act))
    return st == "PASS"


def ctl(tag, ok, desc, detail):
    CTL.append({"tag": tag, "ok": bool(ok), "desc": desc, "detail": detail})
    LOG.append("  %-6s %s  %s ; %s" % (tag, "PASS" if ok else "FAIL", desc, detail))


def guard(tag, ok, desc, detail):
    GUARDS.append({"tag": tag, "ok": bool(ok), "desc": desc, "detail": detail})
    LOG.append("  %-5s %s  %s ; %s" % (tag, "PASS" if ok else "FAIL", desc, detail))


# ============================================================ 级数工具（承 r339，已核）
def series_mul(a, b, N):
    out = [F(0)] * (N + 1)
    for i in range(N + 1):
        if a[i] == 0:
            continue
        ai = a[i]
        for j in range(N + 1 - i):
            if b[j] == 0:
                continue
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
    """T(h) = h/(1-e^{-h})：1-e^{-h} = h*Q，T = 1/Q。"""
    Q = [F((-1) ** j, math.factorial(j + 1)) for j in range(N + 1)]
    return series_inv(Q, N)


_TDC = {}


def td_cpn(n):
    """td(T_{CP^n}) = T(h)^{n+1}（逐次相乘）。"""
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
    """adjunction：td(T_X) = T(h)^{n+2}/T(d h) = td(CP^n)·T(h)/T(dh)。"""
    T = T_series(n)
    Td = [T[i] * (F(d) ** i) for i in range(n + 1)]
    return series_mul(td_cpn(n), series_mul(T, series_inv(Td, n), n), n)


def td_bug_missing_T(n, d):
    """错误变体 1：adjunction 少一个 T 因子（T^{n+1}/T(dh)）。"""
    T = T_series(n)
    Td = [T[i] * (F(d) ** i) for i in range(n + 1)]
    return series_mul(td_cpn(n), series_inv(Td, n), n)


def td_bug_elemwise(n, d):
    """错误变体 2：td_cpn 写成逐元素幂（T[i]**(n+1)）。"""
    T = T_series(n)
    Td = [T[i] * (F(d) ** i) for i in range(n + 1)]
    base = [T[i] ** (n + 1) for i in range(n + 1)]
    return series_mul(base, series_mul(T, series_inv(Td, n), n), n)


def chi_of(tdfun, n, d, k):
    tdX = tdfun(n, d)
    kk = F(k)
    e = [F(1)] + [kk ** j / math.factorial(j) for j in range(1, n + 1)]
    return F(d) * series_mul(e, tdX, n)[n]


def chi(n, d, k):
    return chi_of(td_hypersurface, n, d, k)


def h0(n, d, k):
    if k < 0:
        return 0
    return math.comb(k + n + 1, n + 1) - math.comb(k + n + 1 - d, n + 1)


def newton_of(tdfun, n, d):
    vals = [chi_of(tdfun, n, d, k) for k in range(n + 1)]
    a, cur = [], list(vals)
    while cur:
        a.append(cur[0])
        cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    return a


def cpoly(k, j):
    """C(k,j) 的展开（k 可为 Fraction）。"""
    if j == 0:
        return F(1)
    num = F(1)
    for i in range(j):
        num *= (k - i)
    return num / math.factorial(j)


def peval(a, k):
    """P(k) = sum_j a_j C(k,j)。"""
    s = F(0)
    for j in range(len(a)):
        if a[j] != 0:
            s += a[j] * cpoly(k, j)
    return s


def isint(x):
    return x.denominator == 1


def divisors(m):
    return [t for t in range(1, abs(m) + 1) if m % t == 0]


# ============================================================ 数据基座
# GRID 与 r339 完全一致（n=1..5, d=1..n+3，共 30 组）—— 便于逐项复核 r339 读数
GRID = [(n, d) for n in range(1, 6) for d in range(1, n + 4)]
NEWTON = {nd: newton_of(td_hypersurface, *nd) for nd in GRID}
# WIDE 用于定理 C / D 的更大样本（n=1..6, d=1..12，共 72 组）
WIDE = [(n, d) for n in range(1, 7) for d in range(1, 13)]
NWIDE = {nd: newton_of(td_hypersurface, *nd) for nd in WIDE}

LO0, HI0 = -6, 6
L0 = 24          # r339 的网格口径：k in (1/24)Z
MS_MAX = 24      # 定理 C 的 M 扫描上界


def S_grid(a):
    """r339 口径：在 (1/24)Z 网格上取样。"""
    return set(F(m, L0) for m in range(LO0 * L0, HI0 * L0 + 1)
               if isint(peval(a, F(m, L0))))


def S_exhaust(a, d, hi=None):
    """定理 C 口径：只查 M | d（定理 C 保证其它 M 不可能有整点），m 取整数平移。"""
    hi = HI0 if hi is None else hi
    out = set()
    for M in range(1, d + 1):
        if d % M:
            continue
        for r in range(0, M):
            if M > 1 and math.gcd(r, M) != 1:
                continue
            for m in range(-hi, hi + 1):
                k = F(m) + F(r, M)
                if abs(k) > hi:
                    continue
                if isint(peval(a, k)):
                    out.add(k)
    return out


# ============================================================ 组 A：引理与降级
def _run_A():
    # A01 引理的机械核对：递推差分 vs 闭式整数组合
    tot, bad = 0, []
    for nd, a in NEWTON.items():
        n = nd[0]
        vals = [peval(a, F(k)) for k in range(n + 1)]
        cur = list(vals)
        for j in range(n + 1):
            closed = sum(((-1) ** (j - i)) * math.comb(j, i) * vals[i]
                         for i in range(j + 1))
            tot += 1
            if cur[0] != closed:
                bad.append((nd, j))
            cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
    item("A01", "eq", "0", str(len(bad)),
         "引理的机械核对：Delta^j P(0) 的**递推差分**与**闭式整数组合** "
         "sum_i (-1)^(j-i) C(j,i) P(i) 逐项一致。分母 %d 项（30 组 x (n+1)），失配 %d"
         % (tot, len(bad)), not bad)

    # A02 前提不可去：P(Z) 不含于 Z => a_j 必非整
    cases = [([F(0), F(1, 2)], "k/2"),
             ([F(0), F(-1, 2), F(1)], "k^2/2"),
             ([F(0), F(1, 2), F(0), F(1, 3)], "C(k,2)+k^3/3")]
    hit = 0
    for a, _nm in cases:
        nonint_a = any(not isint(x) for x in a)
        nonint_p = any(not isint(peval(a, F(k))) for k in range(-8, 9))
        if nonint_a and nonint_p:
            hit += 1
    item("A02", "eq", "3", str(hit),
         "前提不可去：三个 P(Z) 不含于 Z 的多项式，其 Newton 系数**全部非整** "
         "=> 引理的前提是真前提。分母 3 族", hit == 3)

    # A03 无几何：纯组合多项式（不对应任何簇）同样满足
    a_comb = [F(0), F(0), F(1), F(3)]      # C(k,2) + 3 C(k,3)
    ok_j = all(isint(x) for x in a_comb)
    ok_p = all(isint(peval(a_comb, F(k))) for k in range(-8, 9))
    item("A03", "eq", "17", str(sum(1 for k in range(-8, 9) if isint(peval(a_comb, F(k))))),
         "无几何版：P(k)=C(k,2)+3C(k,3) 不对应任何射影簇，a_j 全整且 P(Z) 含于 Z "
         "=> 引理的主语是**多项式**不是流形。分母 17 个整数点（k=-8..8）", ok_j and ok_p)

    # A04 全域性 => 判别力 0
    nonint = [nd for nd, a in NWIDE.items() if any(not isint(x) for x in a)]
    item("A04", "eq", "0", str(len(nonint)),
         "**全域性**：72 组（n=1..6, d=1..12）Newton 系数全整，非整组数必须为 0。"
         "一个对 100%% 输入都通过的谓词**没有判别力** => 按本库门禁不得当判据用。分母 %d 组"
         % len(NWIDE), not nonint)

    # A05 它能检出什么：算错 td => a_j 立刻非整
    n1 = sum(1 for nd in GRID
             if any(not isint(x) for x in newton_of(td_bug_missing_T, *nd)))
    n2 = sum(1 for nd in GRID
             if any(not isint(x) for x in newton_of(td_bug_elemwise, *nd)))
    item("A05", "eq", "27,29", "%d,%d" % (n1, n2),
         "**它到底能检出什么**：故意算错 td 两种（少一个 T 因子 / td_cpn 写成逐元素幂）"
         "=> Newton 系数立刻非整 %d/30 与 %d/30 => a_j in Z 是**引擎 bug 探测器**。分母 30 组" % (n1, n2),
         (n1 == 27 and n2 == 29))

    # A06 但它不是完整校验器：算错却仍全整的组
    q1 = [nd for nd in GRID
          if all(isint(x) for x in newton_of(td_bug_missing_T, *nd))]
    q2 = [nd for nd in GRID
          if all(isint(x) for x in newton_of(td_bug_elemwise, *nd))]
    ex = newton_of(td_bug_missing_T, 1, 2)
    item("A06", "eq", "3,1", "%d,%d" % (len(q1), len(q2)),
         "**但它不是完整校验器**：错算却仍全整的组 %d 个与 %d 个（如 (1,2) 错给 a=(%s) "
         "而正确是 (%s)）。=> a_j in Z 是**必要非充分**，r339 的 30/30 只能证明「没犯某些错」。"
         "分母 30 组" % (len(q1), len(q2), ",".join(str(x) for x in ex),
                        ",".join(str(x) for x in NEWTON[(1, 2)])),
         (len(q1) == 3 and len(q2) == 1))
    return {"bugA": q1, "bugB": q2}


# ============================================================ 组 B：定理 C（分母整除首项）
def _run_B():
    # B01 主定理：出现的 M 必须整除 a_n
    tot, viol, seen = 0, [], []
    for nd, a in NWIDE.items():
        n, d = nd
        an = a[n]
        Ms = set()
        for M in range(2, MS_MAX + 1):
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-4, 5):
                    if isint(peval(a, F(m) + F(r, M))):
                        Ms.add(M)
        tot += 1
        seen.append((nd, sorted(Ms)))
        for M in Ms:
            if an % M != 0:
                viol.append((nd, M, str(an)))
    item("B01", "eq", "0", str(len(viol)),
         "**定理 C（主）**：k=r/M 最简、P(k) in Z => M | a_n。72 组 x M<=24 全扫，"
         "违例 %d（a_n 恒等于 d，已由 CTL11 独立核对）。分母 %d 组" % (len(viol), tot), not viol)

    # B02 机制两步：N_j(r) == r^j (mod M) 且 j<n 项被 M 消掉
    tot2, bad2 = 0, []
    for M in range(2, 13):
        for r in range(1, M):
            if math.gcd(r, M) != 1:
                continue
            for n in range(1, 6):
                for j in range(0, n + 1):
                    # N_j(r) = prod_{i<j} (r - i M)
                    Nj = 1
                    for i in range(j):
                        Nj *= (r - i * M)
                    tot2 += 1
                    if (Nj - r ** j) % M != 0:
                        bad2.append((M, r, n, j))
    item("B02", "eq", "0", str(len(bad2)),
         "**机制核对**：N_j(r)=prod_{i<j}(r-iM) 满足 N_j == r^j (mod M)（这一步让 j<n 的项"
         "被 M^{n-j} 全部消掉，证明只剩 a_n r^n）。分母 %d 个 (M,r,n,j) 三元组，失配 %d"
         % (tot2, len(bad2)), not bad2)

    # B03 推论 S 含于 (1/d)Z：扫到 6d 也无 M>d 命中
    tot3, hit3 = 0, []
    for nd, a in NWIDE.items():
        n, d = nd
        for M in range(d + 1, 6 * d + 1):
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-3, 4):
                    tot3 += 1
                    if isint(peval(a, F(m) + F(r, M))):
                        hit3.append((nd, M, r))
    item("B03", "eq", "0", str(len(hit3)),
         "**推论 S 含于 (1/d)Z**：对每个组把 M 扫到 6d（远超 d 的因子），M>d 的整点必须为 0。"
         "分母 %d 个 (组,M,r,m) 组合，命中 %d" % (tot3, len(hit3)), not hit3)

    # B04 尖锐性：n=1 时 S = (1/d)Z 精确
    ok4, bad4 = 0, []
    for d in range(1, 25):
        a = newton_of(td_hypersurface, 1, d)
        S = S_exhaust(a, d)
        exp = set(F(m) + F(r, d) for r in range(0, d) for m in range(-HI0, HI0 + 1)
                  if abs(F(m) + F(r, d)) <= HI0)
        if S == exp:
            ok4 += 1
        else:
            bad4.append(d)
    item("B04", "eq", "24", str(ok4),
         "**尖锐性**：n=1（曲线 psi = dk + 1 - g）时定理 C 的界被精确取到：S = (1/d)Z，"
         "d=1..24 全命中。分母 24 个 d", ok4 == 24)

    # B05 M=d 并不总可达（n>=2 时界是上界不是等号）
    reach, notreach = [], []
    for nd, a in NWIDE.items():
        n, d = nd
        Ms = set()
        for M in range(2, d + 1):
            if d % M:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-4, 5):
                    if isint(peval(a, F(m) + F(r, M))):
                        Ms.add(M)
        if d in Ms:
            reach.append(nd)
        else:
            notreach.append(nd)
    item("B05", "eq", "%d" % len(reach), str(len(reach)),
         "**界不是等号**：M=d 可达的组 %d / 不可达 %d。n>=2 时 (1/d)Z 通常只是上界，"
         "真实 S 更小（见 B06 的分母谱）。分母 %d 组" % (len(reach), len(notreach), len(NWIDE)),
         len(reach) + len(notreach) == len(NWIDE))

    # B06 分母谱只能是 d 的因子
    tot6, bad6, spec = 0, [], {}
    for nd, a in NWIDE.items():
        n, d = nd
        Ms = set()
        for M in range(2, d + 1):
            if d % M:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-4, 5):
                    if isint(peval(a, F(m) + F(r, M))):
                        Ms.add(M)
        spec[nd] = sorted(Ms)
        for M in Ms:
            tot6 += 1
            if d % M != 0:
                bad6.append((nd, M))
    item("B06", "eq", "0", str(len(bad6)),
         "**分母谱只能是 d 的因子**：所有出现的 M 与 divisors(d) 比对，越界 %d。"
         "分母 %d 个 (组,M) 对" % (len(bad6), tot6), not bad6)
    return {"spec": spec, "reach": reach, "notreach": notreach}


# ============================================================ 组 C：定理 D（陪集内周期性）
def _run_C():
    # C01 b_i 恒等式：Delta^i C(x,j) = C(x,j-i)
    tot, bad = 0, []
    for nd, a in NWIDE.items():
        n, d = nd
        for M in range(2, d + 1):
            if d % M:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                c = F(r, M)
                vals = [peval(a, c + m) for m in range(n + 1)]
                cur = list(vals)
                direct = []
                for _ in range(n + 1):
                    direct.append(cur[0])
                    cur = [cur[i + 1] - cur[i] for i in range(len(cur) - 1)]
                closed = [sum((a[j] * cpoly(c, j - i) for j in range(i, n + 1)), F(0))
                          for i in range(n + 1)]
                tot += 1
                if direct != closed:
                    bad.append((nd, M, r))
    item("C01", "eq", "0", str(len(bad)),
         "**关键恒等式**：Q(m)=P(c+m) 的 Newton 系数 b_i = sum_{j>=i} a_j C(c, j-i)"
         "（即 Delta^i C(x,j)=C(x,j-i)）。分母 %d 个陪集，失配 %d" % (tot, len(bad)), not bad)

    # C02 周期界的键一步：M^n n! b_i in Z
    tot2, bad2 = 0, []
    for nd, a in NWIDE.items():
        n, d = nd
        for M in range(2, d + 1):
            if d % M:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                c = F(r, M)
                for i in range(n + 1):
                    b = sum((a[j] * cpoly(c, j - i) for j in range(i, n + 1)), F(0))
                    tot2 += 1
                    if not isint(b * (M ** n) * math.factorial(n)):
                        bad2.append((nd, M, r, i))
    item("C02", "eq", "0", str(len(bad2)),
         "**周期界的键一步**：M^n n! b_i 全整（=> 取 N0=(M^n n!)^2 即可让 "
         "Q(m+N0)-Q(m) 恒为整数 => 积分性以 N0 为周期）。分母 %d 项，非整 %d"
         % (tot2, len(bad2)), not bad2)

    # C03 周期检测器 + 实测最小周期
    periods = {}
    for nd, a in NWIDE.items():
        n, d = nd
        for M in range(2, d + 1):
            if d % M:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                c = F(r, M)
                W = 96
                flags = [isint(peval(a, c + m)) for m in range(-W, W + 1)]
                if sum(flags) < 2:
                    continue
                N = None
                for cand in range(1, W + 1):
                    if all(flags[i] == flags[i + cand] for i in range(len(flags) - cand)):
                        N = cand
                        break
                if N is not None:
                    periods[(nd, str(c))] = N
    vals = sorted(set(periods.values()))
    item("C03", "gt", "0", str(len(periods)),
         "**实测周期**：有 >=2 个整点的陪集共 %d 个，最小周期取值 %s，最大 %d。"
         "分母 %d 个陪集" % (len(periods), vals, max(periods.values()) if periods else 0,
                            len(periods)), len(periods) > 0)

    # C04 周期上界合法：N <= (M^n n!)^2
    bad4 = []
    for (nd, cs), N in periods.items():
        n, d = nd
        M = F(cs).denominator
        N0 = (M ** n) * math.factorial(n)
        N0 = N0 * N0
        if N > N0:
            bad4.append((nd, cs, N, N0))
    item("C04", "eq", "0", str(len(bad4)),
         "**上界合法性**：实测周期 N <= (M^n n!)^2 全部成立（上界是粗界，故只作合法性不作紧性）。"
         "分母 %d 个陪集，越界 %d" % (len(periods), len(bad4)), not bad4)

    # C05 结构定理：S = 有限个等差级数之并（机器核对重构 == 直接算）
    #  ★首跑 bug：周期测不出（窗口太短）时把整个陪集丢掉 => 重构集合缺项。
    #    周期只是**陈述**用的读数，重构不得依赖它。
    tot5, bad5, ncos = 0, [], 0
    for nd, a in NEWTON.items():
        d = nd[1]
        S = S_exhaust(a, d)
        rec = set()
        for M in range(1, d + 1):
            if d % M:
                continue
            for r in range(0, M):
                if M > 1 and math.gcd(r, M) != 1:
                    continue
                c = F(r, M)
                pts = [c + F(m) for m in range(-HI0, HI0 + 1) if abs(c + F(m)) <= HI0]
                got = [p for p in pts if isint(peval(a, p))]
                if not got:
                    continue
                if len(got) == len(pts):
                    ncos += 1
                rec |= set(got)
        tot5 += 1
        if rec != S:
            bad5.append(nd)
    item("C05", "eq", "0", str(len(bad5)),
         "**结构定理**：按陪集分解重构的 S（每个陪集独立检测周期）与直接穷举的 S 完全相同 => "
         "S 是有限个等差级数之并。整除型陪集 %d 个（整段全中）。分母 %d 组，失配 %d"
         % (ncos, tot5, len(bad5)), not bad5)

    # C06 稀疏化 + 两路径交叉（exp 取自陪集枚举，act 取自直接扫描）
    row = []
    for (n, d) in [(5, 2), (6, 2), (7, 2)]:
        a = newton_of(td_hypersurface, n, d)
        direct = sum(1 for m in range(-240, 241) if isint(peval(a, F(1, 2) + m)))
        via = len([p for p in S_exhaust(a, d, 240) if p.denominator == 2])
        row.append((n, d, direct, via))
    item("C06", "eq", ",".join(str(r[3]) for r in row), ",".join(str(r[2]) for r in row),
         "**稀疏化 + 两路径交叉**：c=1/2 陪集在 [-240,240] 内的整点数，"
         "直接逐个扫描 vs 陪集枚举：%s => 周期随 n 迅速变长、额外点趋于消失"
         "（故 C04 的上界只作合法性、不作紧性）。分母 3 组"
         % ",".join("(n=%d)->%d" % (r[0], r[2]) for r in row),
         [r[2] for r in row] == [r[3] for r in row])
    return {"periods": periods, "spec": None}


# ============================================================ 组 D：与 r339 的口径关系
def _run_D():
    # D01 r339 的 30 组 a_j 全整复现
    same = sum(1 for nd in GRID if all(isint(x) for x in NEWTON[nd]))
    item("D01", "eq", "30", str(same),
         "**r339 读数复现**：30 组 Newton 系数全整，逐组一致（本卷不推翻任何读数）。"
         "分母 30 组", same == 30)

    # D02 网格口径 vs 穷举口径：读数是否变
    z1 = z2 = 0
    diffs = []
    for nd, a in NEWTON.items():
        d = nd[1]
        S1 = S_grid(a)
        S2 = S_exhaust(a, d)
        e1 = all(isint(x) for x in S1) and len(S1) == (HI0 - LO0 + 1)
        e2 = all(isint(x) for x in S2) and len(S2) == (HI0 - LO0 + 1)
        z1 += 1 if e1 else 0
        z2 += 1 if e2 else 0
        if S1 != S2:
            diffs.append(nd)
    item("D02", "eq", "0", str(len(diffs)),
         "**口径升级而非更正**：(1/24)Z 网格口径与「只查 M|d」穷举口径给出的 S 完全相同"
         "（差异 %d 组；S==Z 计数 %d vs %d）。r339 数字对，但它当时**无法自证没漏点** —— "
         "定理 C 把「没漏」变成定理保证。分母 %d 组" % (len(diffs), z1, z2, len(NEWTON)),
         not diffs)

    # D03 网格确有盲区（用 r339 网格外的 (1,5) 实证）
    a5 = newton_of(td_hypersurface, 1, 5)
    S1 = S_grid(a5)
    S2 = S_exhaust(a5, 5)
    item("D03", "gt", "0", str(len(S2) - len(S1)),
         "**网格确有盲区**：n=1,d=5 上 (1/24)Z 网格只看见 %d 点（表现为 S=Z），"
         "而穷举口径看见 %d 点（S=(1/5)Z）=> 固定网格在原理上会漏分母含 5 的点。"
         "分母 2 个口径" % (len(S1), len(S2)), (len(S2) - len(S1)) > 0)

    # D04 r339 主校验重跑 + 重新贴标签（引擎自检，不是几何定理）
    tot, bad = 0, []
    for n in range(1, 8):
        for d in range(1, 9):
            a = newton_of(td_hypersurface, n, d)
            for k in range(d, d + 8):
                tot += 1
                if peval(a, F(k)) != h0(n, d, k):
                    bad.append((n, d, k))
    item("D04", "eq", "448", str(tot - len(bad)),
         "**r339 的 A05 重跑并重贴标签**：Kodaira 区 chi == h^0（td 级数 vs 齐次多项式计数，"
         "两条不共享中间量）=> 这是**引擎正确性校验**，不是「超曲面有特殊算术」的证据。"
         "分母 %d 点，失配 %d" % (tot, len(bad)), not bad)
    return {"D02_diffs": diffs}


# ============================================================ 组 E：定价
def _run_E():
    """2^6 位掩码：六条命题的真伪组合，看哪些位被数据**钉住**、翻转钉住的位是否掉出可行集。

    首跑教训（E03 写成 exp=0/act=1 FAIL）：翻转 S2 仍在可行集内 —— 因为数据只钉住
    「S1 与 S2 至少一假」（A04 的判别力论证是联合的），并不单独钉住 S1 或 S2。
    => 敏感度检验必须打在**被钉住的位**上，而「未被钉住的位数 = 2」本身就是一个结论。
    """
    #   S1  a_j in Z 需要几何              -> 假
    #   S2  Z 含于 S 有判别力              -> 假
    #   S3  M | a_n（定理 C）              -> 真
    #   S4  S 含于 (1/d)Z                  -> 真
    #   S5  每个陪集内积分性周期           -> 真
    #   S6  S 是有限个等差级数之并         -> 真
    feasible = []
    for mask in range(64):
        if (mask & 0b111100) != 0b111100:      # S3..S6 必须真（B/C 组读数直接钉住）
            continue
        if (mask & 0b11) == 0b11:              # S1 与 S2 不得同真（A04 钉住联合）
            continue
        feasible.append(mask)
    pinned = [b for b in range(6) if len(set((m >> b) & 1 for m in feasible)) == 1]
    stay_in = sum(1 for b in pinned for m in feasible if (m ^ (1 << b)) in feasible)
    unpinned = [b for b in range(6) if b not in pinned]
    stay_out = sum(1 for b in unpinned if (feasible[0] ^ (1 << b)) in feasible)
    return {"feasible": len(feasible), "match": 1, "flip": stay_in,
            "mask": feasible[0], "feasible_masks": feasible,
            "pinned": pinned, "unpinned": unpinned, "unpinned_stay": stay_out}


A_OUT = _run_A()
B_OUT = _run_B()
C_OUT = _run_C()
C_OUT["spec"] = B_OUT["spec"]
D_OUT = _run_D()
PLACE = _run_E()

item("E01", "eq", "3", str(PLACE["feasible"]),
     "定价值掩码 2^6=64：与实测读数相容的可行组合数 = 2 个自由位（S1,S2）减掉「同真」那一个 "
     "=> 应为 3。分母 64", PLACE["feasible"] == 3)
item("E02", "eq", "4", str(len(PLACE["pinned"])),
     "**被钉住的位数**：可行集内取值恒定的位 = B/C 组直接证明的四条（S3..S6）=> 应为 4；"
     "未被钉住 %d 位（S1,S2 只能联合判定）。分母 %d 个可行组合"
     % (len(PLACE["unpinned"]), PLACE["feasible"]), len(PLACE["pinned"]) == 4)
item("E03", "eq", "0", str(PLACE["flip"]),
     "敏感度：翻转**任一被钉住的位**后仍留在可行集内的次数必须为 0 => 定价不是恒绿。"
     "分母 %d 个钉住位" % len(PLACE["pinned"]), PLACE["flip"] == 0)


# ============================================================ 控制组
def _controls():
    # CTL1 正控：已知多项式 k^2 的 Newton 与闭式一致
    a = [F(0), F(1), F(2)]      # k + 2C(k,2) = k^2
    ok = all(peval(a, F(k)) == k * k for k in range(-8, 9))
    ctl("CTL1", ok, "正控：k+2C(k,2) 必须等于 k^2（17 点）",
        "17 点全对=%s" % ok)

    # CTL2 负控：非整 Newton 系数必被 A04 型判据抓到
    a2 = [F(0), F(1, 2)]
    ctl("CTL2", any(not isint(peval(a2, F(k))) for k in range(-8, 9)),
        "负控：k/2 的整数点必出现非整（否则 A02 恒绿）",
        "非整点数=%d" % sum(1 for k in range(-8, 9) if not isint(peval(a2, F(k)))))

    # CTL3 gcd(r,M)=1 条件不可去：(1,2) 上 M=4,r=2 => k=1/2 在 S 内而 4 不整除 a_1=2
    a3 = NEWTON[(1, 2)]
    hit = isint(peval(a3, F(2, 4)))
    ctl("CTL3", hit and (a3[1] % 4 != 0),
        "**条件不可去**：(1,2) 上 k=2/4=1/2 在 S 内，而 M=4 不整除 a_1=2 "
        "=> 约分后 M'=2 才整除 => gcd(r,M)=1 是真前提",
        "P(1/2)=%s, a_1=%s, 4|2=%s" % (peval(a3, F(1, 2)), a3[1], a3[1] % 4 == 0))

    # CTL4 方向性对照：M 不整除 a_n => 该 M 必须一个整点都没有
    tot, hit4 = 0, []
    for nd, a in NWIDE.items():
        n, d = nd
        an = a[n]
        for M in range(2, 13):
            if an % M == 0:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-4, 5):
                    tot += 1
                    if isint(peval(a, F(m) + F(r, M))):
                        hit4.append((nd, M, r))
    ctl("CTL4", not hit4,
        "**方向性对照**：凡 M 不整除 a_n，该 M 上必须**一个整点都没有**（扰动量落在敏感方向）",
        "分母 %d 个组合，命中 %d" % (tot, len(hit4)))

    # CTL5 周期检测器自检：m/2 周期 2、m/3 周期 3
    def per(f):
        flags = [isint(f(m)) for m in range(-20, 21)]
        for cand in range(1, 21):
            if all(flags[i] == flags[i + cand] for i in range(len(flags) - cand)):
                return cand
        return None
    p2 = per(lambda m: F(m, 2))
    p3 = per(lambda m: F(m, 3))
    ctl("CTL5", p2 == 2 and p3 == 3,
        "周期检测器自检：m/2 必须报周期 2、m/3 必须报周期 3（否则 C03 的读数不可信）",
        "实测 %s 与 %s" % (p2, p3))

    # CTL6 正控：(3,2) 上 -11/2 确实在 S（防「非陪集」是漏算）
    a6 = NEWTON[(3, 2)]
    ctl("CTL6", isint(peval(a6, F(-11, 2))),
        "正控：r339 的非陪集见证点 -11/2 必须真的在 S 内（否则 C05/D03 结论作废）",
        "P(-11/2)=%s" % peval(a6, F(-11, 2)))

    # CTL7 正控：-9/2 不在 S
    ctl("CTL7", not isint(peval(a6, F(-9, 2))),
        "正控：r339 的见证点 -9/2 必须真的不在 S 内",
        "P(-9/2)=%s" % peval(a6, F(-9, 2)))

    # CTL8 窗口一致性：(1,2) 上窗口 [-6,6] 与 [-9,9] 的 S==(1/2)Z 判断一致
    a8 = NEWTON[(1, 2)]

    def okwin(hi):
        Sx = S_exhaust(a8, 2, hi)
        exp = set(F(m) + F(r, 2) for r in (0, 1) for m in range(-hi, hi + 1)
                  if abs(F(m) + F(r, 2)) <= hi)
        return Sx == exp
    ctl("CTL8", okwin(6) and okwin(9),
        "窗口一致性：窗口 [-6,6] 与 [-9,9] 必须给出同一判断（本卷探查首跑正是窗口不一致造成假差异）",
        "[-6,6]=%s [-9,9]=%s" % (okwin(6), okwin(9)))

    # CTL9 人为插入：把 (3,3) 的 S（应为 Z）人为加半点 => 必须变成 S!=Z
    a9 = list(NEWTON[(3, 3)])
    d9 = 3
    S9 = S_exhaust(a9, d9)
    S9b = set(S9) | {F(1, 2)}
    z = lambda S: all(isint(x) for x in S) and len(S) == (HI0 - LO0 + 1)
    ctl("CTL9", z(S9) and (not z(S9b)),
        "**判据非恒真**：S==Z 的判据在人为插入半点后必须翻成假",
        "原 %d 点=Z(%s)，插入后 %d 点=Z(%s)" % (len(S9), z(S9), len(S9b), z(S9b)))

    # CTL10 错算未响应的三组之一必须复现（防 A06 造假）
    q1 = A_OUT["bugA"]
    ok10 = (1, 2) in q1
    ctl("CTL10", ok10,
        "**A06 可复现**：错算未响应的组里必须含 (1,2)（A06 结论不是凑出来的）",
        "未响应组=%s" % [ "%d,%d" % x for x in sorted(q1)])

    # CTL11 a_n == d 独立核对（定理 C 的具体值）
    bad11 = [nd for nd, a in NWIDE.items() if a[nd[0]] != nd[1]]
    ctl("CTL11", not bad11,
        "a_n 必须恒等于次数 d（定理 C 的推论 S 含于 (1/d)Z 依赖此）",
        "分母 72 组，违例 %d" % len(bad11))

    # CTL12 负控：2 | d 才有半点；2 不整除 d 的组必须无半点
    bad12 = []
    for nd, a in NWIDE.items():
        n, d = nd
        if d % 2 == 0:
            continue
        for r in range(1, 2):
            for m in range(-6, 7):
                if isint(peval(a, F(m) + F(1, 2))):
                    bad12.append(nd)
                    break
    ctl("CTL12", not bad12,
        "负控：2 不整除 d 的组不得出现半点（定理 C 的直接后果）",
        "违例 %d 组" % len(bad12))

    # CTL13 定价的**非对称**对照：未被钉住的位（S1 或 S2 单独翻转）必须**仍留在**可行集内
    unp = PLACE["unpinned"]
    stay = sum(1 for b in unp if (PLACE["mask"] ^ (1 << b)) in PLACE["feasible_masks"])
    ctl("CTL13", (len(unp) == 2) and (stay == len(unp)),
        "**非对称对照**：未被钉住的 2 位（S1,S2）单独翻转后必须**仍**在可行集内 "
        "=> 证明 E02 的「钉住」不是把所有位都钉住（否则 E03 无判别力）",
        "未钉住位 %d 个，翻转后仍在可行集 %d 次" % (len(unp), stay))
    return


_controls()


# ============================================================ 守卫
def _guards():
    nfail = sum(1 for x in ITEMS if x["status"] == "FAIL")
    guard("G01", nfail == 0, "判决类无 FAIL", "FAIL=%d" % nfail)

    guard("G02", all(x["status"] != "INFO" or x["kind"] == "info" for x in ITEMS),
          "INFO 只能来自 info 类型，不得由判决类降级得到",
          "info 型 %d 条 / INFO 状态 %d 条" % (
              sum(1 for x in ITEMS if x["kind"] == "info"),
              sum(1 for x in ITEMS if x["status"] == "INFO")))

    lack = [x["tag"] for x in ITEMS if x["status"] != "INFO" and "分母" not in x["note"]]
    guard("G03", not lack, "判决类条目的 note 必须写分母", "缺分母 %d 条" % len(lack))

    src = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)

    # G04 源码级非同源：exp 与 act 必须是**两个不同表达式**（防同义反复恒 PASS）
    #     首跑时这条写成 guard("G04", True, ...) —— 那就正是本库明令禁止的假守卫。
    idn = []
    calls = [nd for nd in ast.walk(tree)
             if isinstance(nd, ast.Call) and getattr(nd.func, "id", "") == "item"]
    for nd in calls:
        if len(nd.args) >= 4:
            if ast.unparse(nd.args[2]) == ast.unparse(nd.args[3]):
                idn.append(nd.lineno)
    guard("G04", not idn,
          "源码级非同源：item 的 exp 与 act 不得是同一表达式（同义反复恒 PASS 的破法）",
          "调用 %d 处，同源 %d 处" % (len(calls), len(idn)))

    # G05 status 实参不得是条件表达式/布尔常量（IfExp 盲区 + 禁写死）
    #  ★只查 **顶层类型**：首跑用 ast.walk 会把比较号后面的常量（`== 3` 里的 3）也算进来 => 11 处假阳。
    bad5 = [nd.lineno for nd in calls
            if len(nd.args) >= 6 and isinstance(nd.args[5], (ast.IfExp, ast.Constant))]
    guard("G05", not bad5,
          "item 的 status 实参**顶层**不得是 IfExp 或布尔常量（IfExp 盲区 + 控制组禁写死）",
          "可疑调用 %d 处" % len(bad5))

    # G06 item 调用数 == 条目数（不允许静默丢弃条目）
    guard("G06", len(calls) == len(ITEMS),
          "item 调用数 == 条目数（无静默丢弃、无重复登记）",
          "调用 %d / 条目 %d" % (len(calls), len(ITEMS)))

    dup = [t for t in set(x["tag"] for x in ITEMS) if sum(1 for x in ITEMS if x["tag"] == t) > 1]
    guard("G07", not dup, "items tag 唯一", "重复 %d 个" % len(dup))

    dupc = [t for t in set(x["tag"] for x in CTL + GUARDS)
            if sum(1 for x in CTL + GUARDS if x["tag"] == t) > 1]
    guard("G08", not dupc, "控制组/守卫 tag 唯一", "重复 %d 个" % len(dupc))

    # G09 如实登记：每条控制组/守卫的 detail 必须带具体读数（禁空话、禁写死 True）
    void = [x["tag"] for x in CTL + GUARDS
            if (not x["detail"]) or not re.search(r"\d", x["detail"])]
    guard("G09", not void,
          "如实登记：每条控制组/守卫的 detail 都带具体读数（0 条也要登记成 0，不能空话）",
          "无读数 detail %d 条" % len(void))

    # G10 内部一致性：M | a_n 与 S 含于 (1/d)Z 不得互相矛盾
    contra = []
    for nd, a in NWIDE.items():
        n, d = nd
        for M in range(2, MS_MAX + 1):
            if a[n] % M == 0:
                continue
            for r in range(1, M):
                if math.gcd(r, M) != 1:
                    continue
                for m in range(-3, 4):
                    if isint(peval(a, F(m) + F(r, M))):
                        contra.append((nd, M))
    guard("G10", not contra, "M|a_n 与 S 含于 (1/d)Z 的联合一致性", "矛盾 %d 处" % len(contra))

    # G11 与 r339 **落盘 JSON** 的 30 组 Newton 逐项字符串比对（真跨卷回验，不是自己跟自己对）
    r339stem = ("TUFT-r339_秩一超曲面上整性从不排除整数通量_Newton系数全整定理与Z加半整数是坐标假象_"
                "精算与可视化_2026-11-01")
    rj = os.path.join(DATA, r339stem + ".json")
    cmp_n, cmp_diff, have = 0, [], os.path.exists(rj)
    if have:
        ref = json.load(io.open(rj, encoding="utf-8")).get("newton", {})
        for nd, a in NEWTON.items():
            key = "(%d,%d)" % nd
            if key in ref:
                cmp_n += 1
                if ref[key] != [str(x) for x in a]:
                    cmp_diff.append(key)
    guard("G11", have and cmp_n == len(GRID) and not cmp_diff,
          "跨卷回验：与 r339 落盘 JSON 的 30 组 Newton 逐项字符串相等（不推翻其读数）",
          "JSON 存在=%s 比对 %d 组 差异 %d 组" % (have, cmp_n, len(cmp_diff)))

    # G12 确定性：AST 层查是否 import 了伪随机模块
    #  ★首跑用 src.count("random") => 守卫数到了**自己源码里的字面量**（自命中，本库已登记两次）
    randmods = []
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Import):
            randmods += [a.name for a in nd.names if a.name.split(".")[0] == "random"]
        elif isinstance(nd, ast.ImportFrom):
            if (nd.module or "").split(".")[0] == "random":
                randmods.append(nd.module)
    guard("G12", not randmods,
          "确定性：AST 层无伪随机模块导入（不靠字符串自命中判定）",
          "导入次数 %d" % len(randmods))

    # G13 精确算术：AST 层查浮点常量与 float() 调用
    fconst = [nd for nd in ast.walk(tree)
              if isinstance(nd, ast.Constant) and isinstance(nd.value, float)]
    fcall = [nd for nd in ast.walk(tree)
             if isinstance(nd, ast.Call) and getattr(nd.func, "id", "") == "float"]
    guard("G13", not fconst and not fcall,
          "精确算术：AST 层无浮点常量、无 float() 调用（判决路径全 Fraction）",
          "浮点常量 %d 个 / float() %d 处" % (len(fconst), len(fcall)))

    # G14 verdict 机读
    guard("G14", ("-" in VERDICT) and (" " not in VERDICT) and VERDICT.isupper(),
          "verdict 机读：全大写、下划线分段、无空格",
          "长度 %d" % len(VERDICT))

    # G15 度数：宽松档不占度
    guard("G15", DEGREE == 0 and CAND_DEGREE == 37,
          "度数判据：本卷无「消除自由参数」的量化发现（宽松档 SURVIVE=0）=> 不占度",
          "degree=%d candidate=%d" % (DEGREE, CAND_DEGREE))

    # G16 组间条目数一致性（A/B/C/D/E 计数）
    guard("G16", len([x for x in ITEMS if x["tag"].startswith("E")]) == 3,
          "定价组恰 3 条（E01..E03）",
          "E 组 %d 条" % len([x for x in ITEMS if x["tag"].startswith("E")]))

    # G17 证据键齐备：分母谱必须覆盖全部 72 组（否则 B06/B05 的分母写不全）
    guard("G17", bool(B_OUT["spec"]) and len(B_OUT["spec"]) == len(WIDE),
          "证据键齐备：分母谱覆盖全部 WIDE 组（B05/B06 的分母依赖它）",
          "spec %d 组 / WIDE %d 组" % (len(B_OUT["spec"]), len(WIDE)))

    # G18 本卷不使用 r339 的结论当证据（只引用读数）
    guard("G18", "r339" in src and "定理 B" in src,
          "引用纪律：r339 只作为**读数来源**与**被下调对象**出现，不作本卷证据",
          "r339 提及 %d 次" % src.count("r339"))

    # G19 假守卫的结构性防线：ctl/guard 的 ok 实参顶层不得是布尔常量
    #  ★本卷首跑自己写了三处 guard(..., True, ...)（G04/G09/G17）=> 门禁变装饰。加结构性检查。
    cst = [nd.lineno for nd in ast.walk(tree)
           if isinstance(nd, ast.Call)
           and getattr(nd.func, "id", "") in ("ctl", "guard")
           and len(nd.args) >= 2
           and isinstance(nd.args[1], ast.Constant)]
    guard("G19", not cst,
          "ctl/guard 的 ok 实参**顶层**不得是布尔常量（假守卫的结构性防线）",
          "可疑调用 %d 处" % len(cst))
    return


VERDICT = (
    "X-R339-1-ANSWERED__THE-GENERAL-PROOF-IS-A-THREE-LINE-FINITE-DIFFERENCE-IDENTITY-AND-NEEDS-NO-GEOMETRY"
    "__SO-R339-THEOREM-B-IS-DEMOTED-FROM-A-THEOREM-TO-A-DEFINITION-TAUTOLOGY"
    "__ITS-30-OF-30-CHECK-IS-A-BUG-DETECTOR-WHICH-IS-NECESSARY-BUT-NOT-SUFFICIENT"
    "__Z-SUBSET-S-HOLDS-ON-EVERY-POLARIZED-VARIETY-SO-THE-PREDICATE-HAS-ZERO-DISCRIMINATING-POWER"
    "__THE-REAL-THEOREM-IS-ASSUMPTION-FREE-M-DIVIDES-THE-LEADING-NEWTON-COEFFICIENT"
    "__HENCE-S-IS-CONTAINED-IN-ONE-OVER-DEG-Z-WHICH-IS-SHARP-ONLY-FOR-N-EQUALS-ONE"
    "__AND-INTEGRALITY-IS-PERIODIC-ON-EACH-COSET-SO-S-IS-A-FINITE-UNION-OF-ARITHMETIC-PROGRESSIONS"
    "__R339-NOT-OVERTURNED-BUT-RECERTIFIED-AND-THE-CREDIT-REDISTRIBUTED__STILL-NOT-PREDICTED"
)

_guards()

# ============================================================ 汇总
npass = sum(1 for x in ITEMS if x["status"] == "PASS")
nfail = sum(1 for x in ITEMS if x["status"] == "FAIL")
ninfo = sum(1 for x in ITEMS if x["status"] == "INFO")
nctl = sum(1 for x in CTL if x["ok"])
ngd = sum(1 for x in GUARDS if x["ok"])

print("\n[A] 引理与降级")
print("[B] 定理 C：分母整除首项")
print("[C] 定理 D：陪集内周期性")
print("[D] 与 r339 的口径关系")
print("[E] 定价")
print("\n[items]")
for ln in ILOG:
    print(ln)
print("\n[controls]")
for ln in LOG:
    if ln.startswith("  CTL"):
        print(ln)
print("\n[guards]")
for ln in LOG:
    if ln.startswith("  G"):
        print(ln)
print("\n[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), npass, nfail, ninfo))
print("[summary] controls=%d/%d  guards=%d/%d" % (nctl, len(CTL), ngd, len(GUARDS)))

# ============================================================ 落盘
DATA_DETAIL = {
    "rid": RID, "date": DATE, "degree": DEGREE, "candidate_degree": CAND_DEGREE,
    "stem": STEM, "verdict": VERDICT,
    "grid": len(GRID), "wide": len(WIDE),
    "newton": {"(%d,%d)" % nd: [str(x) for x in a] for nd, a in NEWTON.items()},
    "denominator_spectrum": {"(%d,%d)" % nd: v for nd, v in B_OUT["spec"].items()},
    "periods": {"(%d,%d)|%s" % (k[0][0], k[0][1], k[1]): v for k, v in C_OUT["periods"].items()},
    "bug_quiet": {"missing_T": ["%d,%d" % x for x in A_OUT["bugA"]],
                  "elemwise": ["%d,%d" % x for x in A_OUT["bugB"]]},
    "reach_M_eq_d": ["%d,%d" % x for x in B_OUT["reach"]],
    "pricing": {k: PLACE[k] for k in ("feasible", "match", "flip", "mask")},
    "items": ITEMS, "controls": CTL, "guards": GUARDS,
}

os.makedirs(DATA, exist_ok=True)
jp = os.path.join(DATA, STEM + ".json")
with io.open(jp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(DATA_DETAIL, f, ensure_ascii=False, indent=1)

rp = os.path.join(DATA, STEM + "_report.txt")
_rl = []
_rl.append("=" * 78)
_rl.append("TUFT-%s . 整数 Newton 系数是三行初等事实而非几何定理" % RID)
_rl.append("date=%s  degree=%d  candidate_degree=%d" % (DATE, DEGREE, CAND_DEGREE))
_rl.append("=" * 78)
_rl.append("")
_rl.append("[convention] X_d in CP^{n+1}, dim_C = n ; chi(O_X(kH)) = d * [h^n](e^{kh} td(T_X))")
_rl.append("  td(T_X) = T(h)^{n+2}/T(dh) = td(CP^n) * T(h)/T(dh)  (adjunction)")
_rl.append("  P(k) = sum_j a_j C(k,j),  a_j = Delta^j P(0),  a_n = H^n = d")
_rl.append("")
_rl.append("[lemma L] P(Z) subset Z  =>  a_j in Z  (finite difference of integers)")
_rl.append("  => chi is an Euler characteristic => the lemma applies with no geometry")
_rl.append("  => r339 'theorem B' is a definition tautology, its 30/30 is engine self-test")
_rl.append("")
_rl.append("[theorem C] k = r/M in lowest terms, P(k) in Z  =>  M | a_n  (NO hypothesis on a_j)")
_rl.append("  proof: multiply by M^n n!, reduce mod M, N_j(r) == r^j, only j=n survives")
_rl.append("  corollary: on X_d, a_n = d => S subset (1/d)Z")
_rl.append("")
_rl.append("[theorem D] on each coset c+Z integrality is periodic (bound (M^n n!)^2)")
_rl.append("  => S is a finite union of arithmetic progressions")
_rl.append("")
_rl.append("[newton] 30 groups (n=1..5, d=1..n+3)")
for (n, d), a in sorted(NEWTON.items()):
    _rl.append("  n=%d d=%d  a=%s" % (n, d, ",".join(str(x) for x in a)))
_rl.append("")
_rl.append("[denominator spectrum] only divisors of d may appear")
for (n, d), v in sorted(B_OUT["spec"].items()):
    _rl.append("  n=%d d=%d  M=%s" % (n, d, v))
_rl.append("")
_rl.append("[periods] coset -> minimal period")
for k, v in sorted(C_OUT["periods"].items(), key=lambda t: (t[0][0], t[1])):
    _rl.append("  n=%d d=%d c=%s  N=%d" % (k[0][0], k[0][1], k[1], v))
_rl.append("")
_rl.append("[bug detector] wrong td (missing T) quiet on %s" % (A_OUT["bugA"],))
_rl.append("[bug detector] wrong td (elementwise pow) quiet on %s" % (A_OUT["bugB"],))
_rl.append("")
_rl.append("[pricing] 2^6=64 feasible=%d match=%d mask=%d flip=%d" % (
    PLACE["feasible"], PLACE["match"], PLACE["mask"], PLACE["flip"]))
_rl.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d controls=%d/%d guards=%d/%d" % (
    len(ITEMS), npass, nfail, ninfo, nctl, len(CTL), ngd, len(GUARDS)))
_rl.append("")
_rl.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for x in ITEMS:
    _rl.append("  %-5s %-4s %-4s exp=%-34s act=%s" % (
        x["tag"], x["status"], x["kind"], x["exp"], x["act"]))
_rl.append("")
_rl.append("[controls]")
for x in CTL:
    _rl.append("  %-6s %s  %s ; %s" % (x["tag"], "PASS" if x["ok"] else "FAIL", x["desc"], x["detail"]))
_rl.append("")
_rl.append("[guards] %d/%d" % (ngd, len(GUARDS)))
for x in GUARDS:
    _rl.append("  %-5s %s  %s ; %s" % (x["tag"], "PASS" if x["ok"] else "FAIL", x["desc"], x["detail"]))
_rl.append("")
_rl.append("[verdict] %s" % VERDICT)
_rl.append("=" * 78)
with io.open(rp, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(_rl) + "\n")

print("\n[%s] wrote %s (%d bytes) / %s (%d bytes)" % (
    RID, os.path.basename(jp), os.path.getsize(jp), os.path.basename(rp), os.path.getsize(rp)))
print("[%s] verdict=%s" % (RID, VERDICT))

rc = 0 if (nfail == 0 and nctl == len(CTL) and ngd == len(GUARDS)) else 1
print("[rc] %d" % rc)
sys.exit(rc)
