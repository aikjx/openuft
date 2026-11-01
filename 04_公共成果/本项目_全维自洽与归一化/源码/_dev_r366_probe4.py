# -*- coding: utf-8 -*-
"""r366 探查 4：定理 H 是否跨出 Fano（X-R358-2 的适用范围）

要点：χ 在短正合列上加性 + Koszul
      0 → O_{CP^{n+1}}(k−d) → O_{CP^{n+1}}(k) → O_X(k) → 0
  ⇒ χ(O_X(k)) = C(n+1+k,n+1) − C(n+1+k−d,n+1)   【对任意 d>=1 成立，不需要消灭定理】
  ⇒ a_m = Δ^m χ(0) = C(n+1,m) − C(n+1−d, n+1−m) 【广义二项式，d>n+1 时 n+1−d 为负】

若成立，则 r339/r346/r358 三卷绕 td 级数算 χ 的路径是「充分不必要」——
χ 与全部牛顿系数只要 Koszul 三行。本卷要检验这条并给出边界。
"""
from fractions import Fraction as F
from math import comb

def _fact(k):
    p = 1
    for i in range(2, k + 1): p *= i
    return p

BERN = [1, F(1, 2), F(1, 6), 0, F(-1, 30), 0, F(1, 42), 0, F(-1, 30),
        0, F(5, 66), 0, F(-691, 2730), 0, F(7, 6), 0, F(-3617, 510)]

def Tser(N): return [F(BERN[k]) / _fact(k) for k in range(N + 1)]

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

def stir2(r, m):
    if m == 0: return 1 if r == 0 else 0
    if m > r: return 0
    if m == 1 or m == r: return 1
    return m * stir2(r - 1, m) + stir2(r - 1, m - 1)

def pathA(n, d):
    """td 路径：χ(k)=d·[h^n](e^{kh}T(h)^{n+2}/T(dh))"""
    N = n; T = Tser(N)
    num = ppow(T, n + 2, N)
    den = [T[k] * F(d) ** k for k in range(N + 1)]
    Fs = pdiv(num, den, N)
    A = [F(d) * Fs[n - r] / _fact(r) for r in range(n + 1)]
    return [sum((A[r] * stir2(r, m) for r in range(m, n + 1)), F(0)) * _fact(m)
            for m in range(n + 1)]

def Cgen(x, r):
    """广义二项式：x 任意整数，r>=0"""
    if r < 0: return 0
    p = F(1)
    for u in range(r): p *= (x - u)
    return p / _fact(r)

def closedH(n, d):
    return [Cgen(n + 1, m) - Cgen(n + 1 - d, n + 1 - m) for m in range(n + 1)]

def chi_koszul(n, d, k):
    """独立第三条路径：直接 Koszul 计数 χ(k)=C(n+1+k,N)−C(n+1+k−d,N)（大 k 时用 χ 加性）"""
    def Cc(x, r):
        if r < 0: return F(0)
        p = F(1)
        for u in range(r): p *= (x - u)
        return p / _fact(r)
    return Cc(n + 1 + k, n + 1) - Cc(n + 1 + k - d, n + 1)

def pathC(n, d):
    a = []
    for m in range(n + 1):
        s = F(0)
        for i in range(m + 1):
            s += F((-1) ** (m - i) * comb(m, i)) * chi_koszul(n, d, i)
        a.append(s)
    return a

print("=" * 88)
print("探查 4：定理 H 对 d>n+1（CY / 一般型）是否仍成立")
print("        路径 A = td 级数；路径 C = Koszul 计数；闭式 = C(n+1,m)−C(n+1−d,n+1−m)")
print("=" * 88)
tot = 0; bad = 0
for n in range(1, 7):
    for d in range(1, n + 6):
        aA = pathA(n, d)
        aC = pathC(n, d)
        aH = closedH(n, d)
        tot += 1
        ok = all(F(x) == F(y) == F(z) for x, y, z in zip(aA, aC, aH))
        if not ok:
            bad += 1
            print("  MISMATCH n=%d d=%d" % (n, d))
            print("    A=%s" % [str(x) for x in aA])
            print("    C=%s" % [str(x) for x in aC])
            print("    H=%s" % [str(x) for x in aH])
        # 打几个代表
        if d in (n, n + 1, n + 2, n + 3) and n <= 4:
            print("  n=%d d=%-2d %-6s a=%s"
                  % (n, d, {n: "Fano", n + 1: "Fano边界", n + 2: "CY", n + 3: "一般型"}.get(d, ""),
                     [str(int(x)) for x in aH]))
print("-" * 88)
print("[探查4] 组数=%d  失配=%d  ⇒ 定理 H %s"
      % (tot, bad, "对所有 d>=1 成立（不限于 Fano）" if bad == 0 else "有反例"))
print()
print("CY 与一般型的 χ(O_X) 自检（a_0）：")
for n in range(1, 6):
    for d in (n + 2, n + 3):
        print("  n=%d d=%-2d  a_0=χ(O_X)=%s" % (n, d, closedH(n, d)[0]))
