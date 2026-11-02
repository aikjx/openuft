# -*- coding: utf-8 -*-
"""r367 探查 3：绕开 H 枚举，直接在 Z/D 上数「整点剩余类」

动机：H = D·n! 的枚举太贵（探查 2 有 188 组因 H>3e5 被跳过）。
换判法：解集就是 {m : P(c+m) ∈ Z}，若它以 D 为周期，则只需扫 m ∈ [0, 3D) 看
        三个周期窗是否平移一致，并数出 mod D 的剩余类个数。
        类数 = 1 ⇒ 单轨道 ⇒ N = D；类数 ≥ 2 ⇒ 直接否证 N = D。

这个判法把代价从 O(D·n!) 降到 O(D)，可搜远更大的网格。
"""
from fractions import Fraction as F
from math import gcd

def fact(k):
    p = 1
    for i in range(2, k + 1): p *= i
    return p

def Cgen(x, r):
    if r < 0: return F(0)
    p = F(1)
    for u in range(r): p *= (x - u)
    return p / fact(r)

def closedH(n, d):
    return [Cgen(n + 1, m) - Cgen(n + 1 - d, n + 1 - m) for m in range(n + 1)]

def bvec(a, c):
    n = len(a) - 1
    out = []
    for i in range(n + 1):
        s = F(0)
        for j in range(i, n + 1):
            t = j - i
            num = F(1)
            for u in range(t): num *= (c - u)
            s += F(a[j]) * num / fact(t)
        out.append(s)
    return out

def lcm_den(b):
    L = 1
    for x in b: L = L * x.denominator // gcd(L, x.denominator)
    return L or 1

def qval(b, m):
    n = len(b) - 1
    s = F(0)
    for i in range(n + 1):
        t = F(1)
        for u in range(i): t *= (m - u)
        s += b[i] * t / fact(i)
    return s

CAP_D = 20000
PERIODS = 3
rows = []
skip = 0
for n in range(1, 6):
    for d in range(1, n + 3):
        a = closedH(n, d)
        for q in range(1, 13):
            for p in list(range(-q, q + 1)):
                if gcd(abs(p), q) != 1 and p != 0:
                    pass  # 保留非最简，作为口径自守的对照
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b)
                if D > CAP_D:
                    skip += 1
                    continue
                if D <= 1:
                    rows.append(dict(n=n, d=d, p=p, q=q, D=D, cls=1, ns_rel=1.0,
                                     periodic=True, kind="FULL"))
                    continue
                # 扫 3 个周期窗
                wins = []
                for w in range(PERIODS):
                    wins.append([m for m in range(w * D, (w + 1) * D)
                                 if qval(b, m).denominator == 1])
                base = set(x - 0 * D for x in wins[0])
                periodic = all(set(x - w * D for x in wins[w]) == base
                               for w in range(PERIODS))
                cls = len(base)
                rows.append(dict(n=n, d=d, p=p, q=q, D=D, cls=cls,
                                 ns_rel=cls / float(D), periodic=periodic,
                                 kind="EMPTY" if cls == 0 else
                                      ("FULL" if cls == D else "PARTIAL")))

print("=" * 88)
print("探查 3：在 Z/D 上数整点剩余类（n=1..5, d=1..n+2, q=1..12, p=−q..q）")
print("=" * 88)
from collections import Counter
cnt = Counter(r["kind"] for r in rows)
print("[分流] 总 %d 组（SKIP: D>%d 的 %d 组）：%s"
      % (len(rows), CAP_D, skip, dict(cnt)))

P = [r for r in rows if r["kind"] == "PARTIAL"]
print("[PARTIAL] %d 组" % len(P))
bad_per = [r for r in P if not r["periodic"]]
print("  其中解集不以 D 为周期的：%d 组" % len(bad_per))
for r in bad_per[:8]:
    print("    非周期 n=%d d=%d c=%d/%d D=%d cls=%d" % (r["n"], r["d"], r["p"], r["q"], r["D"], r["cls"]))

clsdist = Counter(r["cls"] for r in P)
print("[PARTIAL 的类数分布] " + str(sorted(clsdist.items())))
multi = [r for r in P if r["cls"] > 1]
print("[类数 > 1 的组] %d 组" % len(multi))
for r in multi[:15]:
    print("    多类 n=%d d=%-2d c=%d/%-2d D=%-6d 类数=%d"
          % (r["n"], r["d"], r["p"], r["q"], r["D"], r["cls"]))

print()
print("PARTIAL 的 (n,d) 分布")
nd = Counter((r["n"], r["d"]) for r in P)
for k in sorted(nd): print("   n=%d d=%-2d : %d 组" % (k[0], k[1], nd[k]))
