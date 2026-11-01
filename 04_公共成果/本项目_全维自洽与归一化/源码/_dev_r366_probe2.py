# -*- coding: utf-8 -*-
"""r366 探查 2：定理 H（牛顿系数完全闭式）+ 判别力量化

猜想（由探查 1 数据浮出）：
  Fano 超曲面 X_d ⊂ CP^{n+1}（1<=d<=n+1）的 χ 的牛顿系数
      a_m = C(n+1, m) - C(n+1-d, n+1-m)
  即 (a_0..a_n) 由 (n,d) 两个参数完全钉死，零自由度。

推论（本卷承重件）：
  Int(Z) 的整值多项式有 n+1 个自由整数参数，几何类只有 2 个 (n,d)
  ⇒ n>=3 时几何类是 Int(Z) 中的零测真子集 ⇒ 系数值（而非整性）才有判别力。
"""
from fractions import Fraction as F
from math import comb

def _fact(k):
    p = 1
    for i in range(2, k + 1):
        p *= i
    return p

BERN = [1, F(1, 2), F(1, 6), 0, F(-1, 30), 0, F(1, 42), 0, F(-1, 30),
        0, F(5, 66), 0, F(-691, 2730), 0, F(7, 6), 0, F(-3617, 510)]

def Tser(N):
    return [F(BERN[k]) / _fact(k) for k in range(N + 1)]

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
        for j in range(1, min(i, len(b) - 1) + 1):
            s -= b[j] * o[i - j]
        o[i] = s / b0
    return o

def stir2(r, m):
    if m == 0: return 1 if r == 0 else 0
    if m > r: return 0
    if m == 1 or m == r: return 1
    return m * stir2(r - 1, m) + stir2(r - 1, m - 1)

def pathA(n, d):
    N = n; T = Tser(N)
    num = ppow(T, n + 2, N)
    den = [T[k] * F(d) ** k for k in range(N + 1)]
    Fs = pdiv(num, den, N)
    A = [F(d) * Fs[n - r] / _fact(r) for r in range(n + 1)]
    return [sum((A[r] * stir2(r, m) for r in range(m, n + 1)), F(0)) * _fact(m)
            for m in range(n + 1)]

def C2(x, y):
    """普通二项式（x 非负整数，y>x 或 y<0 时为 0）"""
    if y < 0 or y > x: return 0
    return comb(x, y)

def closedH(n, d):
    return [C2(n + 1, m) - C2(n + 1 - d, n + 1 - m) for m in range(n + 1)]

print("=" * 78)
print("探查 2：定理 H 广域验证（路径 A = td 级数；闭式 = C(n+1,m)-C(n+1-d,n+1-m)）")
print("=" * 78)
tot = 0; bad = 0
rows = []
for n in range(1, 9):
    for d in range(1, n + 2):
        aA = pathA(n, d); aH = closedH(n, d)
        tot += 1
        ok = all(F(x) == F(y) for x, y in zip(aA, aH))
        if not ok:
            bad += 1
            print("  MISMATCH n=%d d=%d  A=%s H=%s" % (n, d, aA, aH))
        rows.append((n, d, aH))
print("[定理H] 组数=%d  失配=%d" % (tot, bad))

# 展示几行
print("-" * 78)
print("样例（n,d） -> a 向量")
for (n, d, aH) in rows:
    if n <= 6 and d in (1, 2, n, n + 1):
        print("  n=%d d=%-2d  a=%s   a0=%d  a_n=%d" % (n, d, aH, aH[0], aH[n]))

# ---- 判别力量化：随机 Int(Z) 多项式通过率 ----
print("-" * 78)
print("判别力：随机整值多项式（a ∈ Z^{n+1} 随机）满足定理 H 的比例")
class LCG:
    def __init__(s, seed): s.s = seed & 0xFFFFFFFF
    def next(s):
        s.s = (1103515245 * s.s + 12345) & 0xFFFFFFFF
        return (s.s >> 8) & 0xFFFFFF
rng = LCG(20261102)
M = 40   # a_m ∈ [-M, M]
for n in (3, 4, 5, 6):
    NS = 4000
    hit = 0
    for _ in range(NS):
        a = [rng.next() % (2 * M + 1) - M for _ in range(n + 1)]
        d = a[n]
        if 1 <= d <= n + 1:
            if a == closedH(n, d):
                hit += 1
    print("  n=%d  样本=%d  命中=%d  通过率=%.6f" % (n, NS, hit, hit / NS))

# ---- 敏感性：几何 a 扰动一位 ----
print("-" * 78)
print("敏感性：几何 a 上单独扰动一位（+1）后仍通过定理 H 的比例")
for n in (3, 4, 5, 6):
    tot2 = 0; survive = 0
    for d in range(1, n + 2):
        a = closedH(n, d)
        for m in range(n + 1):
            b = list(a); b[m] += 1
            tot2 += 1
            dd = b[n]
            if 1 <= dd <= n + 1 and b == closedH(n, dd):
                survive += 1
    print("  n=%d  扰动=%d  仍通过=%d  存活率=%.6f" % (n, tot2, survive, survive / tot2))
