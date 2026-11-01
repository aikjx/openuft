# -*- coding: utf-8 -*-
"""r366 探查 3：X-R358-1（N=D 是否恒成立）与 X-R358-2（D(c) 闭式）

工具（沿用 r358 的整数化）：
  a_m    = C(n+1,m) - C(n+1-d, n+1-m)          （定理 H，本卷闭式）
  b_i(c) = Σ_{j>=i} a_j C(c, j-i)
  D      = lcm_i den b_i(c)
  β_i    = D·b_i ∈ Z
  f(m)   = Σ_i β_i C(m,i)   ⇒   Q_c(m)∈Z ⟺ f(m) ≡ 0 (mod D)

两个周期（r358 只报了解集周期，本卷把两者分开）：
  T_f = f(m) mod D 作为序列的最小周期（可证上界 D·n!）
  N   = 解集 {m : f(m)≡0 mod D} 的最小正平移
  N | T_f

判据（替代「扫窗口」的笨办法，且不受窗口大小影响）：
  f(m+T) − f(m) = Σ_k C(m,k)·γ_k(T)，  γ_k(T) = Σ_{i>k} β_i C(T, i−k)
  Newton 基 {C(m,k)} 是 Z-基 ⇒ 对所有 m 有 f(m+T)≡f(m) (mod D)
  ⟺ γ_k(T) ≡ 0 (mod D) 对所有 k=0..n−1（k=n 恒 0）
"""
from fractions import Fraction as F
from math import comb, gcd
from functools import lru_cache

def _fact(k):
    p = 1
    for i in range(2, k + 1): p *= i
    return p

def C2(x, y):
    if y < 0 or y > x: return 0
    return comb(x, y)

def closedH(n, d):
    return [C2(n + 1, m) - C2(n + 1 - d, n + 1 - m) for m in range(n + 1)]

def bvec(a, c):
    """b_i = Σ_{j>=i} a_j C(c, j-i)，c 为 Fraction"""
    n = len(a) - 1
    out = []
    for i in range(n + 1):
        s = F(0)
        for j in range(i, n + 1):
            # C(c, t) 广义：c(c-1)...(c-t+1)/t!
            t = j - i
            num = F(1)
            for u in range(t):
                num *= (c - u)
            s += F(a[j]) * num / _fact(t)
        out.append(s)
    return out

def lcm_den(b):
    L = 1
    for x in b:
        L = L * x.denominator // gcd(L, x.denominator)
    return L

def betas(b, D):
    return [int(x * D) for x in b]

def gamma_ok(beta, D, T, n):
    """检查 T 是否为 f 的周期：γ_k(T) ≡ 0 mod D 对所有 k"""
    for k in range(n):
        s = 0
        for i in range(k + 1, n + 1):
            # C(T, i-k)
            t = i - k
            if t > T:
                c = 0
            else:
                c = comb(T, t)
            s += beta[i] * c
        if s % D != 0:
            return False
    return True

def divisors(x):
    ds = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            ds.append(i)
            if i != x // i: ds.append(x // i)
        i += 1
    return sorted(ds)

print("=" * 86)
print("探查 3：N 与 D 的关系（X-R358-1）")
print("=" * 86)
CAP = 400000     # H = D·n! 的上限，超过则跳过（诚实标记 SKIP）
rows = []
skip = 0
for n in range(1, 6):
    for d in range(1, n + 2):
        a = closedH(n, d)
        for q in range(1, 5):
            for p in range(0, q):
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b)
                if D == 0: D = 1
                beta = betas(b, D)
                H = D * _fact(n)
                if H > CAP:
                    skip += 1
                    continue
                ds = divisors(H)
                Tf = None
                for T in ds:
                    if gamma_ok(beta, D, T, n):
                        Tf = T; break
                # 解集周期 N：在 [0,H) 上取解集，求最小正平移
                sols = set(m for m in range(H) if sum(beta[i] * comb(m, i) for i in range(n + 1)) % D == 0)
                Nx = None
                for T in ds:
                    if all(((m + T) in sols) == (m in sols) for m in range(H)):
                        Nx = T; break
                rows.append((n, d, p, q, D, Tf, Nx, len(sols), H))
print("  n d  p/q    D      T_f    N     |S|   H       N==D?  T_f==D?")
bad = 0
for (n, d, p, q, D, Tf, Nx, ns, H) in rows:
    eq = (Nx == D)
    if not eq: bad += 1
    print("  %d %-2d %d/%d  %-6d %-6s %-6s %-5d %-7d %-6s %s"
          % (n, d, p, q, D, Tf, Nx, ns, H, "YES" if eq else "NO!!",
             "YES" if Tf == D else ("-" if Tf is None else "NO")))
print("-" * 86)
print("[探查3] 组数=%d  SKIP(D·n!>%d)=%d  N≠D 的组数=%d" % (len(rows), CAP, skip, bad))
