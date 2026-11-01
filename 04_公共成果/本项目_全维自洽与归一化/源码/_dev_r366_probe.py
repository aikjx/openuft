# -*- coding: utf-8 -*-
"""r366 探查 1：几何类牛顿系数是否被 td 钉死

两条独立路径（不共享中间量）：
  路径 A（td / 几何）：F(h)=T(h)^{n+2}/T(dh) 展开得 c_j
                       A_r = d·c_{n-r}/r!
                       a_m = m!·Σ_{r>=m} A_r S(r,m)
  路径 B（组合 / 计数）：Fano 超曲面 X_d ⊂ CP^{n+1}（d<=n+1）上 h^i(O(k))=0 (i>0)
                       χ(k) = C(n+1+k,n+1) - C(n+1+k-d,n+1)
                       a_m = Δ^m χ(0) = Σ_i (-1)^{m-i} C(m,i) χ(i)

再加两个闭式候选：
  a_n     = d
  a_{n-1} = d(2n+1-d)/2
"""
from fractions import Fraction as F
from math import comb

NMAX = 10

# T(h) = h/(1-e^{-h}) = Σ B_k^+ h^k / k!
BERN = [1, F(1, 2), F(1, 6), 0, F(-1, 30), 0, F(1, 42), 0, F(-1, 30),
        0, F(5, 66), 0, F(-691, 2730), 0, F(7, 6)]
def Tser(N):
    out = []
    for k in range(N + 1):
        out.append(F(BERN[k], 1) / F(comb(k, 0)) if False else F(BERN[k]) / _fact(k))
    return out

def _fact(k):
    p = 1
    for i in range(2, k + 1):
        p *= i
    return p

def pmul(a, b, N):
    out = [F(0)] * (N + 1)
    for i, ai in enumerate(a):
        if i > N:
            break
        for j, bj in enumerate(b):
            if i + j > N:
                break
            out[i + j] += ai * bj
    return out

def ppow(a, k, N):
    out = [F(0)] * (N + 1)
    out[0] = F(1)
    for _ in range(k):
        out = pmul(out, a, N)
    return out

def pdiv(a, b, N):
    """a/b 截断到 N 阶（b[0]!=0）"""
    out = [F(0)] * (N + 1)
    b0 = b[0]
    for i in range(N + 1):
        s = a[i] if i < len(a) else F(0)
        for j in range(1, min(i, len(b) - 1) + 1):
            s -= b[j] * out[i - j]
        out[i] = s / b0
    return out

def stirling2(r, m):
    if m == 0:
        return 1 if r == 0 else 0
    if m > r:
        return 0
    if m == 1 or m == r:
        return 1
    return m * stirling2(r - 1, m) + stirling2(r - 1, m - 1)

def pathA(n, d):
    """返回 [a_0..a_n]（Fraction）"""
    N = n
    T = Tser(N)
    num = ppow(T, n + 2, N)                     # T(h)^{n+2}
    den = [T[k] * F(d) ** k for k in range(N + 1)]  # T(dh)
    Fser = pdiv(num, den, N)                    # c_j
    A = [F(d) * Fser[n - r] / _fact(r) for r in range(n + 1)]
    a = []
    for m in range(n + 1):
        s = F(0)
        for r in range(m, n + 1):
            s += A[r] * stirling2(r, m)
        a.append(s * _fact(m))
    return a, Fser

def chi_count(n, d, k):
    """路径 B：Fano 超曲面 h^0 计数（k<0 时 C(...,n+1)=0）"""
    def C(x, r):
        if x < r or x < 0:
            return 0
        # x 为非负整数
        p = 1
        for i in range(r):
            p = p * (x - i) // (i + 1)
        return p
    return C(n + 1 + k, n + 1) - C(n + 1 + k - d, n + 1)

def pathB(n, d):
    a = []
    for m in range(n + 1):
        s = 0
        for i in range(m + 1):
            s += (-1) ** (m - i) * comb(m, i) * chi_count(n, d, i)
        a.append(F(s))
    return a

print("=" * 78)
print("探查 1：路径 A（td 级数） vs 路径 B（组合计数） vs 闭式")
print("=" * 78)
bad = 0
tot = 0
for n in range(1, 7):
    for d in range(1, n + 2):
        aA, Fser = pathA(n, d)
        aB = pathB(n, d)
        ok = (aA == aB)
        tot += 1
        if not ok:
            bad += 1
        # 闭式检查
        cn = aA[n] == d
        cn1 = (n >= 1) and (aA[n - 1] == F(d * (2 * n + 1 - d), 2))
        print("n=%d d=%-2d  A=%s  B=%s  match=%s  a_n=d:%s  a_{n-1}闭式:%s"
              % (n, d, [str(x) for x in aA], [str(x) for x in aB],
                 "OK" if ok else "MISMATCH", cn, cn1))
        if not (cn and cn1):
            bad += 1
print("-" * 78)
print("[探查1] 组数=%d  失配=%d" % (tot, bad))
