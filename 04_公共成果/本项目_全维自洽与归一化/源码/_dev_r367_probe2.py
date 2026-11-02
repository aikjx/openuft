# -*- coding: utf-8 -*-
"""r367 探查 2：X-R366-2 —— 广域搜索「N = D」的反例（轨道数 k > 1）

背景（r366 归约）：
  H = D·n! 是一个周期；解集 S̄ ⊂ Z/H；稳定子阶 = H/N；轨道数
      k = |S|·N / H
  r366 实测 PARTIAL：|S| = n!、N = D ⇒ k = 1（单轨道）
  ⇒ N = D ⟺ k = 1

关键观察（本卷新增）：
  β_n = D·b_n = D·a_n = D·d ≡ 0 (mod D)
  ⇒ f(m) = Σ β_i C(m,i) 模 D 之后**最高次项恒消失** ⇒ deg(f mod D) ≤ n−1
  这一步是几何类独有的（一般整值多项式的 β_n 未必是 D 的倍数）

反例搜索：找 k > 1 的几何陪集。找到即否证 N = D。
对照：一般整值多项式上 k > 1 很常见（r358：C(m,2) mod 2 解集 {0,1}，k=2）
"""
from fractions import Fraction as F
from math import comb, gcd
from itertools import combinations

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
    """r366 定理 H（超曲面 X_d ⊂ CP^{n+1}）"""
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

def divisors(x):
    ds = []; i = 1
    while i * i <= x:
        if x % i == 0:
            ds.append(i)
            if i != x // i: ds.append(x // i)
        i += 1
    return sorted(ds)

def fval(beta, m, n):
    return sum(beta[i] * comb(m, i) for i in range(n + 1))

CAP = 300000
rows = []
skip = 0
for n in range(1, 6):
    for d in range(1, n + 3):
        a = closedH(n, d)
        for q in range(1, 7):
            for p in list(range(-q, q + 1)):
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b)
                beta = [int(x * D) for x in b]
                H = D * fact(n)
                if H > CAP or H < 2:
                    skip += 1
                    continue
                ds = divisors(H)
                sols = set(m for m in range(H) if fval(beta, m, n) % D == 0)
                ns = len(sols)
                if ns == 0 or ns == H:
                    rows.append(dict(n=n, d=d, p=p, q=q, D=D, H=H, ns=ns,
                                     N=None, k=None, kind="EMPTY" if ns == 0 else "FULL"))
                    continue
                Nx = None
                for T in ds:
                    if all((((m + T) % H) in sols) == (m in sols) for m in range(H)):
                        Nx = T; break
                k = ns * Nx / H if Nx else None
                rows.append(dict(n=n, d=d, p=p, q=q, D=D, H=H, ns=ns, N=Nx,
                                 k=k, kind="PARTIAL"))

print("=" * 88)
print("探查 2：广域反例搜索（n=1..5, d=1..n+2, c=p/q, q=1..6, p=−q..q）")
print("=" * 88)
P = [r for r in rows if r["kind"] == "PARTIAL"]
E = [r for r in rows if r["kind"] == "EMPTY"]
Fu = [r for r in rows if r["kind"] == "FULL"]
print("[分流] 总 %d 组（分母 %d）：PARTIAL=%d  EMPTY=%d  FULL=%d  SKIP(H>%d)=%d"
      % (len(rows), len(rows) + skip, len(P), len(E), len(Fu), CAP, skip))

bad = [r for r in P if r["N"] != r["D"]]
print("[N vs D] PARTIAL %d 组中 N≠D 的 %d 组" % (len(P), len(bad)))
for r in bad[:12]:
    print("   反例 n=%d d=%d c=%d/%d  D=%d N=%s |S|=%d H=%d k=%s"
          % (r["n"], r["d"], r["p"], r["q"], r["D"], r["N"], r["ns"], r["H"], r["k"]))

ks = {}
for r in P:
    ks[r["k"]] = ks.get(r["k"], 0) + 1
print("[轨道数 k 的分布] " + str(sorted(ks.items())))
multi = [r for r in P if r["k"] and r["k"] > 1]
print("[k>1 的组] %d 组" % len(multi))
for r in multi[:12]:
    print("   k>1: n=%d d=%d c=%d/%d D=%d N=%s |S|=%d H=%d k=%s"
          % (r["n"], r["d"], r["p"], r["q"], r["D"], r["N"], r["ns"], r["H"], r["k"]))

print()
print("样例 PARTIAL（前 14 组）")
for r in P[:14]:
    print("   n=%d d=%-2d c=%d/%d  D=%-6d N=%-6s |S|=%-6d H=%-7d k=%s"
          % (r["n"], r["d"], r["p"], r["q"], r["D"], r["N"], r["ns"], r["H"], r["k"]))
