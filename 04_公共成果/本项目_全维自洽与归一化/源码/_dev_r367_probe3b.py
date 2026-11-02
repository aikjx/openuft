# -*- coding: utf-8 -*-
"""r367 探查 3b：整数化 + 有限差分递推，在 Z/D 上数整点剩余类（快一个量级）

递推（避开 Fraction 与 comb）：
  g_j(m) := Σ_{i≥j} β_i C(m, i−j)，  f(m) = g_0(m) = Σ_i β_i C(m,i)
  由 C(m+1,t) = C(m,t) + C(m,t−1) 得
      g_j(m+1) = g_j(m) + g_{j+1}(m)，  g_{n+1} ≡ 0
  初值 m=0：C(0,t) = [t=0] ⇒ g_j(0) = β_j
  全程取 mod D ⇒ 小整数加法，每步 O(n)

判法：扫 3 个周期窗 [0,D)、[D,2D)、[2D,3D)，
      若三窗的 (m mod D) 集合相同 ⇒ 解集以 D 为周期，类数 = |该集合|
      类数 = 1 ⇒ 单轨道 ⇒ N = D；类数 ≥ 2 ⇒ 否证
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter

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

def sol_classes(beta, D, n, periods=3):
    """返回 (periodic, cls_set, total)"""
    if D <= 1:
        return True, {0}, periods * 1
    g = [x % D for x in beta]
    wins = []
    total = 0
    for w in range(periods):
        s = set()
        for m in range(D):
            if g[0] == 0:
                s.add(m)
            for j in range(n - 1, -1, -1):
                g[j] = (g[j] + g[j + 1]) % D
        wins.append(s)
        total += len(s)
    base = wins[0]
    per = all(w == base for w in wins)
    return per, base, total

CAP_D = 6000
rows = []
skip = 0
for n in range(1, 6):
    for d in range(1, n + 3):
        a = closedH(n, d)
        for q in range(1, 13):
            for p in range(-q, q + 1):
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b)
                if D > CAP_D:
                    skip += 1
                    continue
                beta = [int(x * D) for x in b]
                if D <= 1:
                    rows.append(dict(n=n, d=d, p=p, q=q, D=1, cls=1,
                                     periodic=True, kind="FULL"))
                    continue
                per, base, tot = sol_classes(beta, D, n)
                cls = len(base)
                rows.append(dict(n=n, d=d, p=p, q=q, D=D, cls=cls, periodic=per,
                                 kind="EMPTY" if cls == 0 else
                                      ("FULL" if cls == D else "PARTIAL")))

print("=" * 88)
print("探查 3b：整数化递推，在 Z/D 上数整点剩余类")
print("=" * 88)
cnt = Counter(r["kind"] for r in rows)
print("[分流] 总 %d 组（SKIP: D>%d 的 %d 组）：%s" % (len(rows), CAP_D, skip, dict(cnt)))

P = [r for r in rows if r["kind"] == "PARTIAL"]
print("[PARTIAL] %d 组" % len(P))
bad_per = [r for r in P if not r["periodic"]]
print("  解集不以 D 为周期的：%d 组" % len(bad_per))
for r in bad_per[:10]:
    print("    非周期 n=%d d=%d c=%d/%d D=%d 类数=%d" % (r["n"], r["d"], r["p"], r["q"], r["D"], r["cls"]))

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
for k in sorted(nd):
    print("   n=%d d=%-2d : %d 组" % (k[0], k[1], nd[k]))
print()
print("类数=1 的 PARTIAL 样例（前 10）")
for r in [x for x in P if x["cls"] == 1][:10]:
    print("   n=%d d=%-2d c=%d/%-2d D=%d" % (r["n"], r["d"], r["p"], r["q"], r["D"]))
