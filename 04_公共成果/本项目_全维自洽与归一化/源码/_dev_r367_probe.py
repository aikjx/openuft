# -*- coding: utf-8 -*-
"""r367 探查 1：完全交的牛顿系数闭式（X-R366-1）

设置：X = X_{d_1..d_r} ⊂ CP^N，dim_C X = n = N − r

路径 T（td 级数，承重既有口径）：
  χ(k) = (Πd_i) · [h^n]( e^{kh} · T(h)^{N+1} / Π_i T(d_i h) )
  （由 ∫_X α = (Πd_i)·[h^n](α)，td(T_X) = T(h)^{N+1}/Π T(d_i h)）

路径 K（Koszul 复形 + χ 加性，本卷闭式）：
  0 → O(k−Σd) → … → ⊕_S O(k−d_S) → … → O(k) → O_X(k) → 0
  χ(O_X(k)) = Σ_{S⊆[r]} (−1)^{|S|} C(N + k − d_S, N)
  a_m = Δ^m χ(0) = Σ_{S⊆[r]} (−1)^{|S|} C(N − d_S, N − m)

r=1 自检：N=n+1 ⇒ a_m = C(n+1, n+1−m) − C(n+1−d, n+1−m) = C(n+1,m) − C(n+1−d,n+1−m)
         与 r366 定理 H 完全一致（用 C(n+1,n+1−m)=C(n+1,m)）
"""
from fractions import Fraction as F
from math import comb
from itertools import combinations

def fact(k):
    p = 1
    for i in range(2, k + 1):
        p *= i
    return p

BERN = [F(1), F(1, 2), F(1, 6), F(0), F(-1, 30), F(0), F(1, 42), F(0), F(-1, 30),
        F(0), F(5, 66), F(0), F(-691, 2730), F(0), F(7, 6), F(0), F(-3617, 510),
        F(0), F(43867, 798)]

def Tser(N):
    return [F(BERN[k]) / fact(k) for k in range(N + 1)]

def pmul(a, b, N):
    o = [F(0)] * (N + 1)
    for i, ai in enumerate(a):
        if i > N: break
        for j, bj in enumerate(b):
            if i + j > N: break
            o[i + j] += ai * bj
    return o

def ppow(a, k, N):
    o = [F(0)] * (N + 1); o[0] = F(1)
    for _ in range(k): o = pmul(o, a, N)
    return o

def pdiv(a, b, N):
    o = [F(0)] * (N + 1); b0 = b[0]
    for i in range(N + 1):
        s = a[i] if i < len(a) else F(0)
        for j in range(1, min(i, len(b) - 1) + 1): s -= b[j] * o[i - j]
        o[i] = s / b0
    return o

def stir2(r_, m):
    if m == 0: return 1 if r_ == 0 else 0
    if m > r_: return 0
    if m == 1 or m == r_: return 1
    return m * stir2(r_ - 1, m) + stir2(r_ - 1, m - 1)

def Cgen(x, r_):
    if r_ < 0: return F(0)
    p = F(1)
    for u in range(r_): p *= (x - u)
    return p / fact(r_)

def pathT(N, ds, k=None):
    """td 路径：返回牛顿系数向量 a_0..a_n"""
    r = len(ds); n = N - r
    T = Tser(n)
    num = ppow(T, N + 1, n)
    den = [F(0)] * (n + 1); den[0] = F(1)
    for d in ds:
        den = pmul(den, [T[j] * F(d) ** j for j in range(n + 1)], n)
    Fs = pdiv(num, den, n)
    deg = 1
    for d in ds: deg *= d
    A = [F(deg) * Fs[n - q] / fact(q) for q in range(n + 1)]
    return [sum((A[q] * stir2(q, m) for q in range(m, n + 1)), F(0)) * fact(m)
            for m in range(n + 1)]

def pathK(N, ds):
    """Koszul 闭式：a_m = Σ_{S⊆[r]} (−1)^{|S|} C(N − d_S, N − m)"""
    r = len(ds); n = N - r
    out = []
    for m in range(n + 1):
        s = F(0)
        for kk in range(r + 1):
            for S in combinations(range(r), kk):
                dS = sum(ds[i] for i in S)
                s += F((-1) ** kk) * Cgen(N - dS, N - m)
        out.append(s)
    return out

print("=" * 84)
print("探查 1：完全交的牛顿系数闭式 —— td 路径 vs Koszul 闭式")
print("=" * 84)
tot = 0; bad = 0
rows = []
for N in range(2, 7):
    for r in range(1, N):
        n = N - r
        if n < 1: continue
        grid = []
        if r == 1:
            grid = [(d,) for d in range(1, 7)]
        elif r == 2:
            grid = [(a, b) for a in range(1, 5) for b in range(1, 5)]
        else:
            grid = [(a, b, c) for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]
        for ds in grid:
            aT = pathT(N, list(ds))
            aK = pathK(N, list(ds))
            tot += 1
            if aT != aK:
                bad += 1
                if bad <= 8:
                    print("  MISMATCH N=%d ds=%s  T=%s  K=%s"
                          % (N, ds, [str(x) for x in aT], [str(x) for x in aK]))
            rows.append((N, r, ds, aK))
print("-" * 84)
print("[探查1] 组数=%d  失配=%d" % (tot, bad))

print()
print("样例（含 r=1 与 r366 定理 H 的退化自检）")
for (N, r, ds, aK) in rows:
    if (r == 1 and N in (3, 5)) or (r == 2 and N in (4, 5)) or (r == 3 and N == 5):
        print("  N=%d r=%d ds=%-10s a=%s" % (N, r, str(ds), [str(int(x)) for x in aK]))

# r=1 自检：闭式应等于 r366 定理 H
print()
print("r=1 退化自检（本卷闭式 vs r366 定理 H）")
bad2 = 0
for (N, r, ds, aK) in rows:
    if r != 1: continue
    n = N - 1; d = ds[0]
    H = [Cgen(n + 1, m) - Cgen(n + 1 - d, n + 1 - m) for m in range(n + 1)]
    if aK != H:
        bad2 += 1
        print("  MISMATCH N=%d d=%d  K=%s H=%s" % (N, d, aK, H))
print("  r=1 组数=%d  与定理 H 失配=%d" % (sum(1 for x in rows if x[1] == 1), bad2))
