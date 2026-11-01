# -*- coding: utf-8 -*-
"""r366 探查 3b：修 bug 后重跑 X-R358-1 / X-R358-2

修正（探查 3 的两处错）：
  1) 平移不变性必须在环 Z/H 上检查（(m+T) % H），否则窗口右端恒假 ⇒ N 求不到（None）
  2) 解集为空时「任何 T 都不变」⇒ 周期退化，不得与「部分陪集」混在一起统计
     （r358 纪律的延伸：凡报「空」必须单独分流并报 D）

分流：
  EMPTY   |S|=0        —— 该陪集上没有整点
  FULL    |S|=H        —— 该陪集整段属于 S（D=1 时必 FULL）
  PARTIAL 0<|S|<H      —— 才是 r358「N=D」所谈的对象
"""
from fractions import Fraction as F
from math import comb, gcd

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
    n = len(a) - 1
    out = []
    for i in range(n + 1):
        s = F(0)
        for j in range(i, n + 1):
            t = j - i
            num = F(1)
            for u in range(t): num *= (c - u)
            s += F(a[j]) * num / _fact(t)
        out.append(s)
    return out

def lcm_den(b):
    L = 1
    for x in b: L = L * x.denominator // gcd(L, x.denominator)
    return L

def divisors(x):
    ds = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            ds.append(i)
            if i != x // i: ds.append(x // i)
        i += 1
    return sorted(ds)

def fval(beta, m, n):
    return sum(beta[i] * comb(m, i) for i in range(n + 1))

CAP = 60000
rows = []
skip = 0
for n in range(1, 5):
    for d in range(1, n + 2):
        a = closedH(n, d)
        for q in range(1, 5):
            for p in range(0, q):
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b) or 1
                beta = [int(x * D) for x in b]
                H = D * _fact(n)
                if H > CAP:
                    skip += 1
                    continue
                ds = divisors(H)
                sols = set(m for m in range(H) if fval(beta, m, n) % D == 0)
                ns = len(sols)
                kind = "EMPTY" if ns == 0 else ("FULL" if ns == H else "PARTIAL")
                # 环形最小平移
                Nx = None
                for T in ds:
                    if all((((m + T) % H) in sols) == (m in sols) for m in range(H)):
                        Nx = T; break
                # f 序列周期
                Tf = None
                for T in ds:
                    ok = True
                    for m in range(H):
                        if (fval(beta, (m + T) % H, n) - fval(beta, m, n)) % D != 0:
                            ok = False; break
                    if ok: Tf = T; break
                rows.append((n, d, p, q, D, Tf, Nx, ns, H, kind))

print("  n d  p/q   D      T_f   N     |S|   H      kind      N==D?")
for (n, d, p, q, D, Tf, Nx, ns, H, kind) in rows:
    if kind == "PARTIAL" or D <= 8:
        print("  %d %-2d %d/%d  %-6d %-5s %-5s %-5d %-6d %-9s %s"
              % (n, d, p, q, D, Tf, Nx, ns, H, kind,
                 "-" if kind != "PARTIAL" else ("YES" if Nx == D else "NO!!")))

print("-" * 80)
from collections import Counter
cnt = Counter(r[9] for r in rows)
print("[分流] " + "  ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())))
P = [r for r in rows if r[9] == "PARTIAL"]
ok = sum(1 for r in P if r[6] == r[4])
print("[PARTIAL] 组数=%d  N==D 的=%d  N≠D 的=%d" % (len(P), ok, len(P) - ok))
for r in P:
    if r[6] != r[4]:
        print("   反例 n=%d d=%d c=%d/%d  D=%d N=%s |S|=%d H=%d" % (r[0], r[1], r[2], r[3], r[4], r[6], r[7], r[8]))
E = [r for r in rows if r[9] == "EMPTY"]
print("[EMPTY] 组数=%d  D 取值=%s" % (len(E), sorted(set(r[4] for r in E))[:14]))
F_ = [r for r in rows if r[9] == "FULL"]
print("[FULL]  组数=%d  D 取值=%s" % (len(F_), sorted(set(r[4] for r in F_))))
print("[SKIP]  H>CAP 的组=%d（CAP=%d）" % (skip, CAP))
# X-R358-2：D 的素因子是否都来自 c 的分母
print("-" * 80)
print("[X-R358-2] D 的素因子 vs c 分母 q 的素因子")
def pf(x):
    s = set(); d = 2
    while d * d <= x:
        while x % d == 0: s.add(d); x //= d
        d += 1
    if x > 1: s.add(x)
    return s
viol = 0
for (n, d, p, q, D, Tf, Nx, ns, H, kind) in rows:
    if not set(pf(D)) <= set(pf(q)):
        viol += 1
        print("   违例 n=%d d=%d q=%d D=%d  pf(D)=%s pf(q)=%s" % (n, d, q, D, pf(D), pf(q)))
print("   组数=%d  违例=%d" % (len(rows), viol))
