# -*- coding: utf-8 -*-
"""r367 探查 4：额外点（PARTIAL）的充要条件

由探查 3b 的 3144 组数据浮出的规律：
  候选判据  PARTIAL ⟺ (n 为奇数且 n ≥ 3) ∧ (d 为偶数) ∧ (c 的既约分母 = 2，即半整数)

与既有卷的吻合度检查：
  r339 在 (n,d)=(3,2) 上见到的额外点 −11/2, −3/2, 5/2 全是半整数 ✓
  r346 定理 C：n=1 时 S=(1/d)Z（等号）⇒ 陪集上要么全要么空 ⇒ n=1 无 PARTIAL ✓
    （机理：c+m ∈ (1/d)Z ⟺ d(c+m) ∈ Z ⟺ dc ∈ Z，与 m 无关）

本探查：在更大网格上验证充要性，并给出 D 的取值表与机理线索。
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
    if D <= 1:
        return True, {0}
    g = [x % D for x in beta]
    wins = []
    for w in range(periods):
        s = set()
        for m in range(D):
            if g[0] == 0:
                s.add(m)
            for j in range(n - 1, -1, -1):
                g[j] = (g[j] + g[j + 1]) % D
        wins.append(s)
    return all(w == wins[0] for w in wins), wins[0]

CAP_D = 20000
rows = []
skip = 0
for n in range(1, 8):
    for d in range(1, n + 3):
        a = closedH(n, d)
        for q in range(1, 13):
            for p in range(0, q):
                if gcd(p, q) != 1 and p != 0:
                    continue          # 只取既约（p=0 除外）
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
                per, base = sol_classes(beta, D, n)
                cls = len(base)
                rows.append(dict(n=n, d=d, p=p, q=q, D=D, cls=cls, periodic=per,
                                 kind="EMPTY" if cls == 0 else
                                      ("FULL" if cls == D else "PARTIAL")))

print("=" * 90)
print("探查 4：PARTIAL 的充要条件（n=1..7, d=1..n+2, c=p/q 既约, q=1..12）")
print("=" * 90)
cnt = Counter(r["kind"] for r in rows)
print("[分流] 总 %d 组（SKIP: D>%d 的 %d 组）：%s" % (len(rows), CAP_D, skip, dict(cnt)))

def predict(n, d, cden):
    return (n % 2 == 1 and n >= 3) and (d % 2 == 0) and (cden == 2)

P = [r for r in rows if r["kind"] == "PARTIAL"]
viol = []
for r in rows:
    actual = (r["kind"] == "PARTIAL")
    pred = predict(r["n"], r["d"], F(r["p"], r["q"]).denominator)
    if actual != pred:
        viol.append((r, actual, pred))
print("[充要性] 组数 %d  违例 %d" % (len(rows), len(viol)))
for (r, a_, p_) in viol[:15]:
    print("   违例 n=%d d=%-2d c=%d/%d D=%-6d 实际PARTIAL=%s 预测=%s cls=%d"
          % (r["n"], r["d"], r["p"], r["q"], r["D"], a_, p_, r["cls"]))

print()
print("[PARTIAL 全表] %d 组" % len(P))
seen = {}
for r in sorted(P, key=lambda x: (x["n"], x["d"], x["q"])):
    key = (r["n"], r["d"])
    if key not in seen:
        seen[key] = (r["D"], r["cls"], r["q"])
for k in sorted(seen):
    print("   n=%d d=%-2d  D=%-8d 类数=%d  q=%d" % (k[0], k[1], seen[k][0], seen[k][1], seen[k][2]))

print()
print("[机理线索] 所有 PARTIAL 的 c 既约分母：%s"
      % sorted(set(r["q"] for r in P)))
print("[机理线索] 所有 PARTIAL 的 (n 奇偶, d 奇偶)：%s"
      % sorted(set((r["n"] % 2, r["d"] % 2) for r in P)))
print("[对照] 非 PARTIAL 中满足三条件的组数：%d"
      % sum(1 for r in rows if r["kind"] != "PARTIAL" and predict(r["n"], r["d"], F(r["p"], r["q"]).denominator)))
