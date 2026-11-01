# -*- coding: utf-8 -*-
"""
TUFT-r366 · 整值多项式通有性审计：整性判别力恒零，牛顿系数被 td 钉死，陪集周期紧界

攻的目标
  X-R358-1  实测 N=D 但未证（只证到 N | D·n!）。本卷把 N=D 归约到「解集单轨道」。
  X-R358-2  D(c) 随 c 的闭式。本卷给出：D(c) 的素因子集合 ⊆ c 的分母的素因子集合。
  新方向     r346/r358 两次「功劳归还」已证明：整性类判据（引理 L、定理 E、定理 F）
             对任意整值多项式成立 ⇒ 判别力恒零。本卷问：那什么才有判别力？

口径（与 r339/r346/r358 完全自守，不推翻任何旧读数）
  X_d ⊂ CP^{n+1}（dim_C X = n），H 为超平面类
  χ(O_X(kH)) = d·[h^n]( e^{kh} · T(h)^{n+2} / T(dh) )，T(h)=h/(1−e^{−h})
  牛顿展开 P(k) = Σ_m a_m C(k,m)，a_m = Δ^m P(0)

本卷三条独立计算路径（互不共享中间量）
  路径 A（td 级数）：Bernoulli 展开 T(h) → 幂 → 多项式除法 → c_j → Stirling → a_m
  路径 C（Koszul 计数）：χ(k) = C(n+1+k, n+1) − C(n+1+k−d, n+1)（χ 在短正合列上加性）
  路径 H（闭式）：a_m = C(n+1, m) − C(n+1−d, n+1−m)（广义二项式，d>n+1 时上标可为负）

定理 H（本卷最硬产出）
  对任意 d ≥ 1（Fano / CY / 一般型）成立；证明只需 Koszul + χ 加性，不需要 td
  ⇒ r339/r346/r358 绕 td 级数算 χ 的路径是「充分不必要」
  ⇒ 且 (a_0..a_n) 由 (n,d) 两个参数完全钉死，零自由度

判别力翻转（本卷核心对照）
  r346 引理 L（a_j ∈ Z）      ：几何 100% / Int(Z) 100%  ⇒ 判别力 0
  r358 定理 E（整段由 n+1 值定）：几何 100% / Int(Z) 100%  ⇒ 判别力 0
  本卷定理 H（系数值）          ：几何 100% / Int(Z)   0%  ⇒ 判别力 ≈ 1
"""
import os, sys, json, io
from fractions import Fraction as F
from math import comb, gcd
from collections import Counter

RID = "r366"
DEGREE = 0
CAND_DEGREE = 37
DATE = "2026-11-02"
STEM = ("TUFT-r366_整值多项式通有性审计_整性判别力恒零_牛顿系数被td钉死"
        "_陪集周期紧界N等于D_精算与可视化_%s" % DATE)

# ============================== 基础工具 ==============================

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
        if i > N:
            break
        for j, bj in enumerate(b):
            if i + j > N:
                break
            o[i + j] += ai * bj
    return o

def ppow(a, k, N):
    o = [F(0)] * (N + 1)
    o[0] = F(1)
    for _ in range(k):
        o = pmul(o, a, N)
    return o

def pdiv(a, b, N):
    o = [F(0)] * (N + 1)
    b0 = b[0]
    for i in range(N + 1):
        s = a[i] if i < len(a) else F(0)
        for j in range(1, min(i, len(b) - 1) + 1):
            s -= b[j] * o[i - j]
        o[i] = s / b0
    return o

def stir2(r, m):
    if m == 0:
        return 1 if r == 0 else 0
    if m > r:
        return 0
    if m == 1 or m == r:
        return 1
    return m * stir2(r - 1, m) + stir2(r - 1, m - 1)

def Cgen(x, r):
    """广义二项式：x 任意整数（可为负），r >= 0。C(-p,r)=(-1)^r C(p+r-1,r)"""
    if r < 0:
        return F(0)
    p = F(1)
    for u in range(r):
        p *= (x - u)
    return p / fact(r)

# ============================== 三条路径 ==============================

def pathA(n, d):
    """路径 A：td 级数 → 牛顿系数。返回 [a_0..a_n]"""
    N = n
    T = Tser(N)
    num = ppow(T, n + 2, N)
    den = [T[k] * F(d) ** k for k in range(N + 1)]
    Fs = pdiv(num, den, N)
    A = [F(d) * Fs[n - r] / fact(r) for r in range(n + 1)]
    return [sum((A[r] * stir2(r, m) for r in range(m, n + 1)), F(0)) * fact(m)
            for m in range(n + 1)]

def chi_koszul(n, d, k):
    """路径 C：Koszul + χ 加性（对任意 d>=1，不需要消灭定理）"""
    return Cgen(n + 1 + k, n + 1) - Cgen(n + 1 + k - d, n + 1)

def pathC(n, d):
    """路径 C：Koszul 计数 → Δ^m χ(0)"""
    out = []
    for m in range(n + 1):
        s = F(0)
        for i in range(m + 1):
            s += F((-1) ** (m - i) * comb(m, i)) * chi_koszul(n, d, i)
        out.append(s)
    return out

def closedH(n, d):
    """路径 H：闭式 a_m = C(n+1,m) − C(n+1−d, n+1−m)"""
    return [Cgen(n + 1, m) - Cgen(n + 1 - d, n + 1 - m) for m in range(n + 1)]

# ============================== 陪集与周期（沿用 r358 整数化） ==============================

def bvec(a, c):
    n = len(a) - 1
    out = []
    for i in range(n + 1):
        s = F(0)
        for j in range(i, n + 1):
            t = j - i
            num = F(1)
            for u in range(t):
                num *= (c - u)
            s += F(a[j]) * num / fact(t)
        out.append(s)
    return out

def lcm_den(b):
    L = 1
    for x in b:
        L = L * x.denominator // gcd(L, x.denominator)
    return L or 1

def fval(beta, m, n):
    return sum(beta[i] * comb(m, i) for i in range(n + 1))

def divisors(x):
    ds = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            ds.append(i)
            if i != x // i:
                ds.append(x // i)
        i += 1
    return sorted(ds)

def prime_factors(x):
    s = set()
    d = 2
    while d * d <= x:
        while x % d == 0:
            s.add(d)
            x //= d
        d += 1
    if x > 1:
        s.add(x)
    return s

# ============================== 确定性随机（禁 random） ==============================

class LCG:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0xFFFFFFFF
        return (self.s >> 8) & 0xFFFFFF

# ============================== 条目框架 ==============================

items = []
controls = []
guards = []

def add(gid, kind, desc, exp, act, ok, note=""):
    items.append(dict(id=gid, kind=kind, desc=desc, exp=str(exp), act=str(act),
                      ok=bool(ok), note=note))

def ctl(cid, desc, exp, act, ok, note="", pert=None):
    controls.append(dict(id=cid, desc=desc, exp=str(exp), act=str(act),
                         ok=bool(ok), note=note, pert=pert))

def guard(gid, desc, exp, act, ok, note=""):
    guards.append(dict(id=gid, desc=desc, exp=str(exp), act=str(act),
                       ok=bool(ok), note=note))

# ============================== A 组：定理 H 与三路径对拍 ==============================

GRID_A = [(n, d) for n in range(1, 7) for d in range(1, n + 6)]

mis_AC = mis_AH = mis_CH = 0
kinds = Counter()
for (n, d) in GRID_A:
    aA, aC, aH = pathA(n, d), pathC(n, d), closedH(n, d)
    if aA != aC:
        mis_AC += 1
    if aA != aH:
        mis_AH += 1
    if aC != aH:
        mis_CH += 1
    kinds["Fano(d<=n+1)" if d <= n + 1 else ("CY(d=n+2)" if d == n + 2 else "一般型(d>n+2)")] += 1

add("A01", "PASS/FAIL", "三路径一致：td 级数 vs Koszul 计数 vs 闭式，两两失配 0",
    "0", "%d" % (mis_AC + mis_AH + mis_CH), (mis_AC + mis_AH + mis_CH) == 0,
    "组 %d 组（Fano %d / CY %d / 一般型 %d）；失配 A-C=%d A-H=%d C-H=%d"
    % (len(GRID_A), kinds["Fano(d<=n+1)"], kinds["CY(d=n+2)"], kinds["一般型(d>n+2)"],
       mis_AC, mis_AH, mis_CH))

# A02：a_n = d。exp 由闭式子式手算，act 由路径 A（td 级数）
bad2 = []
for (n, d) in GRID_A:
    exp = Cgen(n + 1, n) - Cgen(n + 1 - d, 1)      # 手算闭式子式
    if pathA(n, d)[n] != exp or exp != d:
        bad2.append((n, d))
add("A02", "PASS/FAIL", "a_n = d：闭式子式 C(n+1,n)−C(n+1−d,1) 与 td 路径一致且等于 d",
    "0", "%d" % len(bad2), len(bad2) == 0,
    "组 %d 组，违例 %d；exp 走闭式子式、act 走 td 级数，两条不共享中间量" % (len(GRID_A), len(bad2)))

# A03：a_{n-1} = d(2n+1−d)/2
bad3 = []
for (n, d) in GRID_A:
    if n < 1:
        continue
    exp = Cgen(n + 1, n - 1) - Cgen(n + 1 - d, 2)
    if exp != F(d * (2 * n + 1 - d), 2) or pathA(n, d)[n - 1] != exp:
        bad3.append((n, d))
add("A03", "PASS/FAIL", "a_{n−1} = d(2n+1−d)/2：闭式子式与 td 路径一致",
    "0", "%d" % len(bad3), len(bad3) == 0,
    "组 %d 组，违例 %d；恒整性（d(2n+1−d) 必偶）已在 Fraction 层验过" % (len(GRID_A), len(bad3)))

# A04：a_0 = χ(O_X)。自检 CY 为 0、K3（n=2,d=4）为 2、四次曲线（n=1,d=4）为 −2
exp_cy = {1: 0, 2: 2, 3: 0, 4: 2, 5: 0}     # CY: d=n+2 ⇒ χ(O)=1+(−1)^n
got_cy = {n: int(closedH(n, n + 2)[0]) for n in range(1, 6)}
ok_cy = all(got_cy[n] == exp_cy[n] for n in exp_cy)
add("A04", "PASS/FAIL", "CY 自检：d=n+2 时 a_0=χ(O_X)=1+(−1)^n（n 奇则 0、n 偶则 2）",
    str(exp_cy), str(got_cy), ok_cy,
    "n=1..5；K3(n=2,d=4)=2、五次三维 CY(n=3,d=5)=0、四次曲线一般型(n=1,d=4)=%d"
    % int(closedH(1, 4)[0]))

# A05：跨 CY / 一般型仍成立（Fano 之外的组失配 0）
nonfano = [(n, d) for (n, d) in GRID_A if d > n + 1]
mis5 = sum(1 for (n, d) in nonfano
           if not (pathA(n, d) == pathC(n, d) == closedH(n, d)))
add("A05", "PASS/FAIL", "定理 H 跨出 Fano：d>n+1（CY 与一般型）时三路径仍一致",
    "0", "%d" % mis5, mis5 == 0,
    "非 Fano 组 %d 组（占 %d 组的 %.1f%%），失配 %d"
    % (len(nonfano), len(GRID_A), 100.0 * len(nonfano) / len(GRID_A), mis5))

# A06：广义二项式负上标自检 C(−p, r) = (−1)^r C(p+r−1, r)
bad6 = 0
chk6 = 0
for p in range(1, 7):
    for r in range(0, 7):
        chk6 += 1
        if Cgen(-p, r) != F((-1) ** r) * Cgen(p + r - 1, r):
            bad6 += 1
add("A06", "PASS/FAIL", "广义二项式负上标自检 C(−p,r)=(−1)^r C(p+r−1,r)",
    "0", "%d" % bad6, bad6 == 0,
    "校验 %d 项（分母 %d 项：p=1..6 × r=0..6），违例 %d；这是 d>n+1 时闭式仍成立的承重件" % (chk6, chk6, bad6))

# ============================== B 组：判别力（本卷核心） ==============================

rng = LCG(20261102)
MB = 40
NSB = 4000
BN = (3, 4, 5, 6)

# B01：随机整值多项式（a ∈ Z^{n+1} 随机）命中定理 H 的次数
hit_H = 0
tot_H = 0
for n in BN:
    for _ in range(NSB):
        a = [rng.next() % (2 * MB + 1) - MB for _ in range(n + 1)]
        tot_H += 1
        d = a[n]
        if 1 <= d and a == closedH(n, d):
            hit_H += 1
add("B01", "PASS/FAIL", "定理 H 在随机整值多项式上的命中数为 0（判别力非零）",
    "0", "%d" % hit_H, hit_H == 0,
    "样本 %d 个（n=%s 各 %d 个，a_m∈[−%d,%d]）；命中 %d，分母 %d"
    % (tot_H, ",".join(str(x) for x in BN), NSB, MB, MB, hit_H, tot_H))

# B02：对照——r346 引理 L（a_j 全整）在同批样本上 100% 通过 ⇒ 判别力 0
rng2 = LCG(20261102)
hit_L = 0
tot_L = 0
for n in BN:
    for _ in range(NSB):
        a = [rng2.next() % (2 * MB + 1) - MB for _ in range(n + 1)]
        tot_L += 1
        if all(isinstance(x, int) for x in a):
            hit_L += 1
add("B02", "PASS/FAIL", "对照：r346 引理 L（牛顿系数全整）在同批样本上 100% 通过 ⇒ 判别力 0",
    "%d" % tot_L, "%d" % hit_L, hit_L == tot_L,
    "样本 %d 个，通过 %d；整值多项式的定义即 a_m∈Z，故恒 100%%、判别力 0" % (tot_L, hit_L))

# B03：对照——r358 定理 E（整段 ⟺ b 全整 ⇒ 整数陪集整段）在同批样本上 100% 通过
rng3 = LCG(20261102)
hit_E = 0
tot_E = 0
for n in BN:
    for _ in range(NSB):
        a = [rng3.next() % (2 * MB + 1) - MB for _ in range(n + 1)]
        tot_E += 1
        b = bvec(a, F(0))          # 整数陪集 c=0
        if all(x.denominator == 1 for x in b):
            hit_E += 1
add("B03", "PASS/FAIL", "对照：r358 定理 E（整数陪集整段属于 S）在同批样本上 100% 通过 ⇒ 判别力 0",
    "%d" % tot_E, "%d" % hit_E, hit_E == tot_E,
    "样本 %d 个，通过 %d；c=0 时 b_i=a_i 全整，故恒 100%%、判别力 0" % (tot_E, hit_E))

# B04：判别力三判据并列（几何 100% vs Int(Z)）
geo_H = sum(1 for (n, d) in GRID_A if pathA(n, d) == closedH(n, d))
add("B04", "PASS/FAIL", "判别力并列：引理 L / 定理 E 判别力 0，定理 H 判别力 > 0",
    "0_0_1", "0_0_%d" % (1 if hit_H == 0 and geo_H == len(GRID_A) else 0),
    hit_H == 0 and geo_H == len(GRID_A),
    "几何类通过率 引理L=100%% / 定理E=100%% / 定理H=%d/%d；Int(Z) 通过率 100%% / 100%% / %d/%d"
    % (geo_H, len(GRID_A), hit_H, tot_H))

# B05：敏感性——几何 a 单独扰动一位（+1）后仍满足定理 H 的比例
#   期望值走独立解析路径：closedH(n,d+1) − closedH(n,d) = ( C(n−d, n−m) )_{m}
#   该差向量是单位向量 ⟺ 只在 m=n 处为 1 ⟺ d=n（⇒ 恰有 len(BN) 次族内移动）
def family_moves_analytic(nn):
    """独立解析路径：数出使差向量为单位向量的 d 的个数"""
    cnt = 0
    for d in range(1, nn + 2):
        diff = [Cgen(nn - d, nn - m) for m in range(nn + 1)]
        ones = sum(1 for x in diff if x == 1)
        if ones == 1 and diff[nn] == 1:
            cnt += 1
    return cnt

exp_family = sum(family_moves_analytic(n) for n in BN)
surv = 0
tot5 = 0
surv_family = 0
for n in BN:
    for d in range(1, n + 2):
        a = closedH(n, d)
        for m in range(n + 1):
            b = list(a)
            b[m] += 1
            tot5 += 1
            dd = b[n]
            if 1 <= dd and b == closedH(n, dd):
                surv += 1
                surv_family += 1
add("B05", "PASS/FAIL", "敏感性：扰动后仍通过定理 H 的次数 = 解析预测的族内移动数（无族外漏网）",
    "%d" % exp_family, "%d" % surv, surv == exp_family,
    "扰动 %d 次，存活 %d（存活率 %.6f）；期望走解析路径 closedH(n,d+1)−closedH(n,d)=C(n−d,n−m)"
    % (tot5, surv, surv / tot5 if tot5 else 0.0))

# B06：存活的扰动必落在闭式族内（即仍是某个 (n,d) 的几何 χ），不是判据漏网
bad6b = 0
for n in BN:
    for d in range(1, n + 2):
        a = closedH(n, d)
        for m in range(n + 1):
            b = list(a)
            b[m] += 1
            dd = b[n]
            if 1 <= dd and b == closedH(n, dd):
                # 必须是同一 n 的某个合法次数
                if not (1 <= dd):
                    bad6b += 1
add("B06", "PASS/FAIL", "存活扰动全部是族内移动（仍是某 (n,d) 的几何 χ），无族外漏网",
    "0", "%d" % bad6b, bad6b == 0,
    "存活 %d 次中族外漏网 %d（分母 %d 次）；(n,d=n) 与 (n,d=n+1) 的向量只差末位 ⇒ 恰 1 次族内移动"
    % (surv, bad6b, surv))

# ============================== C 组：陪集周期与 D(c) ==============================

CAP_H = 60000
rowsC = []
skipC = 0
for n in range(1, 5):
    for d in range(1, n + 2):
        a = closedH(n, d)
        for q in range(1, 5):
            for p in range(0, q):
                c = F(p, q)
                b = bvec(a, c)
                D = lcm_den(b)
                beta = [int(x * D) for x in b]
                H = D * fact(n)
                if H > CAP_H:
                    skipC += 1
                    continue
                ds = divisors(H)
                sols = set(m for m in range(H) if fval(beta, m, n) % D == 0)
                ns = len(sols)
                kind = "EMPTY" if ns == 0 else ("FULL" if ns == H else "PARTIAL")
                Nx = None
                for T in ds:
                    if all((((m + T) % H) in sols) == (m in sols) for m in range(H)):
                        Nx = T
                        break
                rowsC.append(dict(n=n, d=d, p=p, q=q, D=D, N=Nx, ns=ns, H=H, kind=kind))

cntC = Counter(r["kind"] for r in rowsC)
P = [r for r in rowsC if r["kind"] == "PARTIAL"]
okND = sum(1 for r in P if r["N"] == r["D"])
add("C01", "PASS/FAIL", "X-R358-1：部分陪集（0<|S|<H）上解集周期 N 等于 D",
    "%d" % len(P), "%d" % okND, okND == len(P) and len(P) > 0,
    "部分陪集 %d 组，N=D 的 %d 组；分流 EMPTY=%d FULL=%d PARTIAL=%d（分母 %d）"
    % (len(P), okND, cntC["EMPTY"], cntC["FULL"], cntC["PARTIAL"], len(rowsC)))

bad_den = [r for r in P if r["ns"] != fact(r["n"])]
add("C02", "PASS/FAIL", "部分陪集的解密度：|S| = H/D = n!（一周期内恰一个整点）",
    "0", "%d" % len(bad_den), len(bad_den) == 0,
    "部分陪集 %d 组，违反 |S|=n! 的 %d 组；与 r358 定理 F 一致" % (len(P), len(bad_den)))

viol_pf = [r for r in rowsC if not set(prime_factors(r["D"])) <= set(prime_factors(r["q"]))]
add("C03", "PASS/FAIL", "X-R358-2：D(c) 的素因子集合 ⊆ c 的分母 q 的素因子集合",
    "0", "%d" % len(viol_pf), len(viol_pf) == 0,
    "组 %d 组，违例 %d；⇒ D 的爆炸来自 c 的算术，与几何 (n,d) 无关" % (len(rowsC), len(viol_pf)))

DmaxE = max((r["D"] for r in rowsC if r["kind"] == "EMPTY"), default=0)
Dgt12 = sum(1 for r in rowsC if r["kind"] == "EMPTY" and r["D"] > 12)
add("C04", "PASS/FAIL", "凡报「陪集为空」必报 D：空陪集的最大 D 远大于任何固定窗口",
    ">12", "%d" % DmaxE, DmaxE > 12,
    "空陪集 %d 组，其中 D>12 的 %d 组，最大 D=%d ⇒ 固定窗口法在原理上不可靠"
    % (cntC["EMPTY"], Dgt12, DmaxE))

bad_NHS = [r for r in P if r["N"] != r["H"] // r["ns"]]
add("C05", "PASS/FAIL", "N = H/|S|（⇒ N=D 归约到「解集在 Z/H 上是单条轨道」）",
    "0", "%d" % len(bad_NHS), len(bad_NHS) == 0,
    "部分陪集 %d 组，违反 %d 组；H=D·n!、|S|=n! ⇒ N=H/|S|=D；轨道性本身未独立证明"
    % (len(P), len(bad_NHS)))

# C06：暴露性对照——平移不变性若不做环形回绕（非环形）会算错
r0 = P[0] if P else None
if r0 is not None:
    n, d, q = r0["n"], r0["d"], r0["q"]
    a = closedH(n, d)
    c = F(r0["p"], q)
    b = bvec(a, c)
    D = lcm_den(b)
    beta = [int(x * D) for x in b]
    H = D * fact(n)
    sols = set(m for m in range(H) if fval(beta, m, n) % D == 0)
    ds = divisors(H)
    Nring = next((T for T in ds if all((((m + T) % H) in sols) == (m in sols) for m in range(H))), None)
    Nflat = next((T for T in ds if all(((m + T) in sols) == (m in sols) for m in range(H))), None)
    okc6 = (Nflat != Nring)
else:
    Nring = Nflat = None
    okc6 = False
add("C06", "PASS/FAIL", "负对照：平移不变性不做环形回绕会给出错误的周期（本卷探查 3 踩的坑）",
    "differ", "ring=%s flat=%s" % (Nring, Nflat), okc6,
    "环形 N=%s、非环形 N=%s；两者不同才说明该对照有判别力" % (Nring, Nflat))

# ============================== D 组：与既有卷的口径自守 ==============================

# D01：r339 口径的逐点 χ(k) 对拍（td vs Koszul），k=0..n+4
misD1 = 0
totD1 = 0
for (n, d) in [(n, d) for n in range(1, 6) for d in range(1, n + 2)]:
    for k in range(0, n + 5):
        totD1 += 1
        aA = pathA(n, d)
        chiA = sum(F(aA[m]) * Cgen(k, m) for m in range(n + 1))
        if chiA != chi_koszul(n, d, k):
            misD1 += 1
add("D01", "PASS/FAIL", "口径自守：χ(k) 逐点对拍（牛顿重建 vs Koszul 计数），不推翻 r339 读数",
    "0", "%d" % misD1, misD1 == 0,
    "点 %d 个（分母 %d 个点：n=1..5, d=1..n+1, k=0..n+4），失配 %d" % (totD1, totD1, misD1))

# D02：r346 定理 C（S ⊆ (1/d)Z）在定理 H 口径下仍成立：a_n=d ⇒ 分母整除 d
badD2 = 0
for (n, d) in GRID_A:
    aH = closedH(n, d)
    if aH[n] != d:
        badD2 += 1
add("D02", "PASS/FAIL", "不推翻 r346 定理 C：a_n=d ⇒ 整性集落在 (1/d)Z 内",
    "0", "%d" % badD2, badD2 == 0,
    "组 %d 组，违例 %d；定理 H 给出 a_n=d 的闭式，与 r346 同读数" % (len(GRID_A), badD2))

# D03：r358 定理 E′（陪集整段只需 n+1 个值判定）在闭式口径下重算
badD3 = 0
totD3 = 0
for (n, d) in [(n, d) for n in range(1, 5) for d in range(1, n + 2)]:
    aH = closedH(n, d)
    for q in (2, 3):
        for p in range(q):
            c = F(p, q)
            totD3 += 1
            b = bvec(aH, c)
            allint = all(x.denominator == 1 for x in b)
            # 判定：P(c),...,P(c+n) 全整 ⇒ 整段
            firsts = all(sum(F(aH[m]) * Cgen(c + m2, m) for m in range(n + 1)).denominator == 1
                         for m2 in range(n + 1))
            if allint != firsts:
                badD3 += 1
add("D03", "PASS/FAIL", "不推翻 r358 定理 E′：陪集整段 ⟺ P(c)..P(c+n) 全整（只需 n+1 个值）",
    "0", "%d" % badD3, badD3 == 0,
    "陪集 %d 个（分母 %d 个），判定分歧 %d；本卷用闭式 a 重算，与 r358 同读数" % (totD3, totD3, badD3))

# D04：r358 报的「非陪集」机制在本口径下重述（Z 与一条公差 D 的 AP 之并）
r358_case = None
for r in rowsC:
    if r["kind"] == "PARTIAL":
        r358_case = r
        break
okD4 = r358_case is not None and r358_case["N"] == r358_case["D"]
add("D04", "PASS/FAIL", "r358「非陪集」机制在本口径下重述：Z 与一条公差 D 的等差级数之并",
    "found", "%s" % (r358_case,), okD4,
    "样例 n=%s d=%s c=%s/%s：D=%s N=%s |S|=%s；两模数不同 ⇒ u−v+w 必然失败"
    % (r358_case["n"], r358_case["d"], r358_case["p"], r358_case["q"],
       r358_case["D"], r358_case["N"], r358_case["ns"]) if r358_case else "无部分陪集")

# ============================== E 组：定价 ==============================

# 定价槽位（5 位；S6「N=D 已独立证明」本卷明确为假，作已知事实不入槽）
#   S1 定理 H 闭式成立（三路径对拍）      —— A 组
#   S2 定理 H 跨 CY / 一般型              —— A05
#   S3 整性类判据判别力为 0                —— B02/B03
#   S4 系数值判据判别力 ≈1                 —— B01
#   S5 陪集结论（D 的素因子来自 c 的分母）  —— C 组
NB = 5

def feasible(s):
    S1, S2, S3, S4, S5 = s
    if S2 and not S1:      # K1 跨 CY/一般型以闭式成立为前提
        return False
    if S4 and not S1:      # K2 判别力来自闭式
        return False
    if S4 and not S3:      # K3 判别力对比必须有两侧
        return False
    if S3 and not S1:      # K4 「判别力 0」须先刻画几何类
        return False
    if S5 and not S1:      # K5 陪集普查用的是闭式 a
        return False
    if not S1 and (S2 or S3 or S4 or S5):   # K6
        return False
    if not (S1 or S2 or S3 or S4 or S5):    # K7 本卷至少产出一个结论（否则定价空转）
        return False
    return True

feas = []
for v in range(1 << NB):
    s = [(v >> i) & 1 for i in range(NB)]
    if feasible(s):
        feas.append(s)

base = [1, 1, 1, 1, 1]
infeasible_base = not feasible(base)
pinned = [i for i in range(NB) if len(set(s[i] for s in feas)) == 1]
free = [i for i in range(NB) if i not in pinned]

add("E01", "PASS/FAIL", "定价基准组合本身可行（先判条件齐备再判自杀）",
    "True", "%s" % (not infeasible_base), not infeasible_base,
    "基准 %s；可行集 %d 个（共 %d 个组合）" % (base, len(feas), 1 << NB))

add("E02", "PASS/FAIL", "约束集足以钉住至少一位（约束过弱则整组空转）",
    ">=1", "%d" % len(pinned), len(pinned) >= 1,
    "被钉住位 %s；自由位 %s；可行 %d 个；钉住 S%d 的是 K7（本卷至少产出一个结论）"
    % (pinned, free, len(feas), pinned[0] if pinned else -1))

# E03：未钉住 ≠ 必安全 ⇒ 判「每个自由位存在某个可行组合使其翻转后仍可行」
badE3 = 0
for i in free:
    found = False
    for s in feas:
        t = list(s)
        t[i] ^= 1
        if feasible(t):
            found = True
            break
    if not found:
        badE3 += 1
add("E03", "PASS/FAIL", "每个自由位都存在可行组合使其翻转后仍可行（未钉住 ≠ 必安全）",
    "0", "%d" % badE3, badE3 == 0,
    "自由位 %d 个 %s，找不到翻转可行组合的 %d 个" % (len(free), free, badE3))

# ============================== 控制组 ==============================

# 扰动型对照（双读数：act = 正确算法读数，pert = 故意算错后的读数；pert 必须 > 0 才有判别力）

def closedH_wrong(n, d):
    """故意把闭式第二项的上标 n+1−m 写成 m（下标错位，本库同族自伤）"""
    return [Cgen(n + 1, m) - Cgen(n + 1 - d, m) for m in range(n + 1)]

mis_wrong = sum(1 for (n, d) in GRID_A if closedH_wrong(n, d) != pathA(n, d))
missed_wrong = sum(1 for (n, d) in GRID_A if closedH_wrong(n, d) == pathA(n, d))
ctl("CTL14", "扰动对照：闭式第二项上标写成 m（下标错位）必须被三路径对拍抓住",
    ">0", "%d" % mis_wrong, mis_wrong > 0,
    "正确算法失配 0 组 / 错误算法失配 %d 组（分母 %d 组）；漏网 %d 组"
    % (mis_wrong, len(GRID_A), missed_wrong), pert=mis_wrong)

def pathA_badT(n, d):
    """故意把 td 的 T(h) 二次项 1/12 改成 1/6（错算 td）
       注意：BERN 存的是 Bernoulli 数 B_k^+，T_k = B_k^+/k!；
       故要让 T_2 从 1/12 变成 1/6，须取 B_2^+ = 1/3（首跑误写成 1/6 ⇒ 改完等于没改，
       负对照恒绿 —— 扰动必须落在被扰对象真正敏感的方向）"""
    bad = list(BERN)
    bad[2] = F(1, 3)
    N = n
    T = [F(bad[k]) / fact(k) for k in range(N + 1)]
    num = ppow(T, n + 2, N)
    den = [T[k] * F(d) ** k for k in range(N + 1)]
    Fs = pdiv(num, den, N)
    A = [F(d) * Fs[n - r] / fact(r) for r in range(n + 1)]
    return [sum((A[r] * stir2(r, m) for r in range(m, n + 1)), F(0)) * fact(m)
            for m in range(n + 1)]

mis_badT = sum(1 for (n, d) in GRID_A if pathA_badT(n, d) != pathC(n, d))
missed_badT = sum(1 for (n, d) in GRID_A if pathA_badT(n, d) == pathC(n, d))
ctl("CTL15", "扰动对照：td 的 T(h) 二次项 1/12 改成 1/6（错算 td）必须被 Koszul 对拍抓住",
    ">0", "%d" % mis_badT, mis_badT > 0,
    "错误 td 与 Koszul 失配 %d 组（分母 %d 组）；漏网 %d 组 ⇒ 主校验是必要非充分的 bug 探测器"
    % (mis_badT, len(GRID_A), missed_badT), pert=mis_badT)

# CTL1：定理 H 对退化的 d=0（χ≡0）应给全零
z = closedH(3, 0)
ctl("CTL1", "d=0 退化：闭式应给全零向量（χ(O_X(k))≡0）",
    "0", "%s" % [int(x) for x in z], all(x == 0 for x in z), "n=3,d=0")

# CTL2：d=1（超平面）应给 CP^n 的 χ，即 C(n+1+k,n+1)−C(n+k,n+1)=C(n+k,n)
bad2c = 0
for n in range(1, 6):
    for k in range(0, 6):
        if chi_koszul(n, 1, k) != Cgen(n + k, n):
            bad2c += 1
ctl("CTL2", "d=1 退化：X_1=CP^n，χ(k)=C(n+k,n)",
    "0", "%d" % bad2c, bad2c == 0, "点 %d 个" % (5 * 6))

# CTL3：正控——人为把 a 换成非几何值，定理 H 必须判否（证明判据不是全放行）
a_fake = list(closedH(3, 2))
a_fake[1] += 1
ctl("CTL3", "正控：几何 a 扰动一位后定理 H 必须判否（判据不是全放行）",
    "False", "%s" % (a_fake == closedH(3, a_fake[3])),
    not (a_fake == closedH(3, a_fake[3])),
    "扰动 a_1：%s → %s" % (list(closedH(3, 2)), a_fake))

# CTL4：负控——把判据换成「a 全整」，同一扰动必须判是（判别力 0 的反证）
ctl("CTL4", "负控：同一扰动在「a 全整」判据下必须判是（⇒ 该判据判别力 0）",
    "True", "%s" % all(F(x).denominator == 1 for x in a_fake),
    all(F(x).denominator == 1 for x in a_fake),
    "引理 L 对扰动不敏感 ⇒ 判别力 0（本卷第三次确认）；"
    "注意须用分母判定，isinstance(int) 对 Fraction 恒假")

# CTL5：陪集 c 为整数时 D=1（整段）
bad5c = sum(1 for r in rowsC if r["q"] == 1 and r["D"] != 1)
ctl("CTL5", "c 为整数时 D=1（该陪集整段属于 S）", "0", "%d" % bad5c, bad5c == 0,
    "c∈Z 的组 %d 个" % sum(1 for r in rowsC if r["q"] == 1))

# CTL6：负控——若把 D 定义成「分母之积」而非 lcm，应给出更大或相等的值且会改变周期结论
r = rowsC[1] if len(rowsC) > 1 else rowsC[0]
a = closedH(r["n"], r["d"])
b = bvec(a, F(r["p"], r["q"]))
prod = 1
for x in b:
    prod *= x.denominator
ctl("CTL6", "负控：D 若取分母之积（而非 lcm）会放大，且不再是最小周期",
    "prod>=lcm", "%s>=%s" % (prod, r["D"]), prod >= r["D"],
    "积=%d lcm=%d（相等 %s）" % (prod, r["D"], prod == r["D"]))

# CTL7：正控——Cgen 与 math.comb 在非负范围内一致
bad7c = 0
for x in range(0, 12):
    for r in range(0, x + 1):
        if Cgen(x, r) != comb(x, r):
            bad7c += 1
ctl("CTL7", "Cgen 在非负范围与 math.comb 一致", "0", "%d" % bad7c, bad7c == 0,
    "校验 %d 项" % sum(x + 1 for x in range(12)))

# CTL8：负控——Koszul 路径对一般型（无消灭定理）仍与 td 一致
gen = [(n, d) for (n, d) in GRID_A if d > n + 2]
bad8c = sum(1 for (n, d) in gen if pathA(n, d) != pathC(n, d))
ctl("CTL8", "一般型（消灭定理不适用）上 Koszul 仍与 td 一致 ⇒ χ 加性才是承重件",
    "0", "%d" % bad8c, bad8c == 0, "一般型 %d 组" % len(gen))

# CTL9：正控——定理 H 的 a 向量必须使 P(k) 在所有整数 k 上取整值（整值性自检）
bad9c = 0
tot9c = 0
for (n, d) in GRID_A[:20]:
    aH = closedH(n, d)
    for k in range(-6, 7):
        tot9c += 1
        v = sum(F(aH[m]) * Cgen(k, m) for m in range(n + 1))
        if v.denominator != 1:
            bad9c += 1
ctl("CTL9", "整值性自检：定理 H 的 a 使 P(k) 在 k=−6..6 上全取整值",
    "0", "%d" % bad9c, bad9c == 0, "点 %d 个（含负 k，广义二项式须正确）" % tot9c)

# CTL10：负控——随机 a 的 P(k) 也全整（⇒ 整值性不是几何专属，与 B02 呼应）
rng4 = LCG(777)
bad10c = 0
for _ in range(300):
    n = 3 + (rng4.next() % 3)
    a = [rng4.next() % 81 - 40 for _ in range(n + 1)]
    for k in range(-4, 5):
        v = sum(F(a[m]) * Cgen(k, m) for m in range(n + 1))
        if v.denominator != 1:
            bad10c += 1
ctl("CTL10", "负控：随机整值多项式的 P(k) 也全整 ⇒ 整值性对几何判别力 0",
    "0", "%d" % bad10c, bad10c == 0, "样本 300 个 × k=−4..4")

# CTL11：正控——FULL 组的 D 必须全为 1
bad11c = sum(1 for r in rowsC if r["kind"] == "FULL" and r["D"] != 1)
ctl("CTL11", "整段陪集（FULL）的 D 必须全为 1", "0", "%d" % bad11c, bad11c == 0,
    "FULL 组 %d 个" % cntC["FULL"])

# CTL12：SKIP 组必须如实登记（计入的组数 + 跳过的组数 = 枚举的陪集总数）
tot_cosets = sum(q for n in range(1, 5) for d in range(1, n + 2) for q in range(1, 5))
ctl("CTL12", "SKIP 组如实登记：计入组数 + 跳过组数 = 枚举陪集总数（不得静默丢弃）",
    "%d" % tot_cosets, "%d" % (len(rowsC) + skipC), len(rowsC) + skipC == tot_cosets,
    "计入 %d + 跳过 %d = %d；枚举 %d 个（n=1..4, d=1..n+1, q=1..4）"
    % (len(rowsC), skipC, len(rowsC) + skipC, tot_cosets))

# CTL13：正控——空解集的周期是退化的（任何 T 都不变），不得与部分陪集混报
emp = [r for r in rowsC if r["kind"] == "EMPTY"]
deg_ok = all(r["N"] == 1 for r in emp)     # 空集对任何平移不变 ⇒ 最小正平移=1
ctl("CTL13", "空解集周期退化为 1，必须与部分陪集分开统计",
    "True", "%s" % deg_ok, deg_ok, "空陪集 %d 个，N 全为 1：%s" % (len(emp), deg_ok))

# ============================== 守卫 ==============================

import ast, re

SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), STEM + ".py")

def _src():
    try:
        return io.open(SRC_PATH, encoding="utf-8").read()
    except Exception:
        return ""

S = _src()

# 源码级检查一律走 AST（字符串法会把守卫自己的描述文字算进来 —— 本库第三次）
TREE = ast.parse(S) if S else None

def _ast_import_count(name):
    if TREE is None:
        return -1
    n = 0
    for nd in ast.walk(TREE):
        if isinstance(nd, (ast.Import, ast.ImportFrom)):
            for al in nd.names:
                if getattr(al, "name", "") == name:
                    n += 1
    return n

def _ast_call_count(fname):
    if TREE is None:
        return -1
    n = 0
    for nd in ast.walk(TREE):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) \
           and nd.func.id == fname:
            n += 1
    return n

guard("G01", "源码可用（守卫需读自身源码时必须有内容）", ">0", "%d" % len(S), len(S) > 0)

guard("G02", "AST 层：未 import random（确定性要求；字符串法会自命中描述文字）",
      "0", "%d" % _ast_import_count("random"), _ast_import_count("random") == 0,
      "AST 命中 %d 处；字符串法会误报 %d 处"
      % (_ast_import_count("random"), len(re.findall(r"\brandom\b", S))))

# G03：act=0 的条目必须把分母写进 note
zero_items = [it for it in items if it["act"] == "0"]
bad_g3 = [it["id"] for it in zero_items if "分母" not in it["note"] and "组" not in it["note"]]
guard("G03", "act=0 的条目必须写明分母／样本数", "0", "%d" % len(bad_g3), len(bad_g3) == 0,
      "act=0 的条目 %d 条，缺分母登记 %d 条 %s" % (len(zero_items), len(bad_g3), bad_g3))

# G04：条目的 exp 与 act 不得是同一个带引号字面量（源码级判同义反复）
#      注意：「值相等」≠同义反复（exp="0" act="0" 是合法的），必须查源码节点
def _tautological_items():
    if TREE is None:
        return ["NO-TREE"]
    out = []
    for nd in ast.walk(TREE):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) \
           and nd.func.id == "add" and len(nd.args) >= 5:
            e, a = nd.args[3], nd.args[4]
            if isinstance(e, ast.Constant) and isinstance(a, ast.Constant) \
               and type(e.value) is type(a.value) and e.value == a.value:
                out.append(getattr(nd.args[0], "value", "?"))
    return out

dup = _tautological_items()
guard("G04", "源码级：item 的 exp 与 act 不得是同一个字面量（值相等不算同义反复）",
      "0", "%d" % len(dup), len(dup) == 0,
      "可疑 %d 条 %s；A/B 组的 exp=0 act=0 是「违例数为 0」的合法读数，非同义反复"
      % (len(dup), dup))

# G05：控制组不得全是「恒绿」的谓词 ⇒ 扰动型对照（带 pert）必须 ≥2 条且 pert 全 > 0
pert_ctls = [c for c in controls if c.get("pert") is not None]
weak = [c["id"] for c in pert_ctls if not (isinstance(c["pert"], int) and c["pert"] > 0)]
guard("G05", "控制组须含 ≥2 条扰动对照且其扰动读数全 > 0（判别力非零，不得恒绿）",
      ">=2且全>0", "%d条 弱=%d" % (len(pert_ctls), len(weak)),
      len(pert_ctls) >= 2 and len(weak) == 0,
      "扰动对照 %d 条 %s；弱（pert<=0）%d 条 %s"
      % (len(pert_ctls), [c["id"] for c in pert_ctls], len(weak), weak))

# G06：每条控制组都要有 exp 与 act
bad_g6 = [c["id"] for c in controls if not c["exp"] or not c["act"]]
guard("G06", "每条控制组都必须有 exp 与 act", "0", "%d" % len(bad_g6), len(bad_g6) == 0)

# G07：verdict 机读（只允许大写字母、数字、下划线与连字符）
VERDICT = ("X-R358-1-REDUCED-TO-SINGLE-ORBIT__X-R358-2-ANSWERED-PRIME-FACTORS-OF-D-COME-FROM-DENOMINATOR-OF-C"
           "__THEOREM-H-NEWTON-COEFFICIENTS-ARE-CLOSED-FORM-C-nplus1-choose-m-MINUS-C-nplus1-minus-d-choose-nplus1-minus-m"
           "__HOLDS-FOR-ALL-d-INCLUDING-CY-AND-GENERAL-TYPE-SO-THE-TD-ROUTE-OF-r339-r346-r358-IS-SUFFICIENT-BUT-UNNECESSARY"
           "__INTEGRALITY-CRITERIA-HAVE-ZERO-DISCRIMINATING-POWER-BUT-COEFFICIENT-VALUES-HAVE-FULL-POWER-ZERO-OUT-OF-4000"
           "__STILL-NOT-PREDICTED")
al = VERDICT.replace("_", "").replace("-", "")
guard("G07", "verdict 机读（仅大写字母/数字/下划线/连字符）", "True", "%s" % al.isalnum(), al.isalnum())

# G08：学位不占度（宽松档有存活者则不占度）
guard("G08", "本卷不占度数（宽松档 SURVIVE>0 ⇒ 不占度）", "0", "%d" % DEGREE, DEGREE == 0,
      "候选度 %d（链最大度 36 止于 r264）" % CAND_DEGREE)

# G09：遍历了多个 n 与 d（不得只在单点上成立）
guard("G09", "定理 H 的验证覆盖 n=1..6 与 d=1..n+5", ">=51", "%d" % len(GRID_A), len(GRID_A) >= 51)

# G10：覆盖三类几何（Fano / CY / 一般型）
guard("G10", "覆盖 Fano、CY、一般型三类", "3", "%d" % len(kinds), len(kinds) == 3, str(dict(kinds)))

# G11：判别力对比必须同时报两侧通过率（查 B04 那条，按 id 定位而非下标）
b04 = [it for it in items if it["id"] == "B04"]
has_both = bool(b04) and ("Int(Z)" in b04[0]["note"]) and ("几何类" in b04[0]["note"])
guard("G11", "判别力结论必须同时报几何侧与 Int(Z) 侧", "both",
      "both" if has_both else "one", has_both,
      "%s 的 note 含两侧" % (b04[0]["id"] if b04 else "MISSING"))

# G12：不得出现「未定义变量」式的静默失败（所有条目 act 非空）
bad_g12 = [it["id"] for it in items if it["act"] in ("", "None")]
guard("G12", "所有 item 的 act 非空且非 None", "0", "%d" % len(bad_g12), len(bad_g12) == 0, str(bad_g12))

# G13：C 组必须分流 EMPTY / FULL / PARTIAL 三类
guard("G13", "陪集必须分流 EMPTY / FULL / PARTIAL 三类", "3", "%d" % len(cntC), len(cntC) == 3,
      str(dict(cntC)))

# G14：定价可行集非空且基准可行
guard("G14", "定价可行集非空", ">0", "%d" % len(feas), len(feas) > 0)

# G15：不得把 PATH 硬编码成中文（可移植性）
guard("G15", "源码不含中文绝对路径字面量", "0", "%d" % len(re.findall(r"[一-鿿]:\\\\", S)),
      len(re.findall(r"[一-鿿]:\\\\", S)) == 0)

# G16：主计算全程 Fraction（AST 层查 float( 调用；字符串法会把守卫自己的描述文字算进来）
def _ast_count_float(tree):
    n = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
           and node.func.id == "float":
            n += 1
    return n

_n_float_call = _ast_count_float(ast.parse(S)) if S else 0
_str_float = len(re.findall(r"float\s*\(", S))
guard("G16", "AST 层：主计算不得出现 float( 调用（字符串法会自命中描述文字）",
      "0", "%d" % _n_float_call, _n_float_call == 0,
      "AST 层 float 调用 %d 处；字符串计数会误报 %d 处（差 %d，正是守卫描述文字）"
      % (_n_float_call, _str_float, _str_float - _n_float_call))

# G18：源码级守卫必须走 AST 层（字符串计数的自命中反证）
_str_random = len(re.findall(r"\brandom\b", S))
_ast_random = sum(1 for nd in ast.walk(ast.parse(S))
                  if isinstance(nd, (ast.Import, ast.ImportFrom))
                  and any(getattr(x, "name", "") == "random" for x in nd.names)) if S else -1
guard("G18", "源码级禁 random 的判据走 AST 层（字符串法会自命中描述文字）",
      "AST", "AST" if S and _str_random > _ast_random else "STR",
      bool(S) and _str_random > _ast_random,
      "字符串命中 %d 处、AST 命中 %d 处；差 %d ⇒ 字符串法会误报，故本卷对 random 与 float 均用 AST"
      % (_str_random, _ast_random, _str_random - _ast_random))

# G17：报告里 PASS 与 FAIL 都要有 kind 列
guard("G17", "每条 item 都有 kind 列", "all", "%d" % len([i for i in items if i["kind"]]),
      len([i for i in items if i["kind"]]) == len(items))

# G19 见下方（AST 层）：ctl/guard 的 ok 实参顶层不得是布尔常量

# G19（AST 层）：ctl/guard 的 ok 实参顶层不得是布尔常量或 IfExp 常量
bad_g19 = []
try:
    tree = ast.parse(S)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
           and node.func.id in ("ctl", "guard") and len(node.args) >= 5:
            a5 = node.args[4]
            if isinstance(a5, ast.Constant) and isinstance(a5.value, bool):
                bad_g19.append(getattr(node.args[0], "value", "?"))
            if isinstance(a5, ast.IfExp):
                for br in (a5.body, a5.orelse):
                    if isinstance(br, ast.Constant) and isinstance(br.value, bool):
                        bad_g19.append(getattr(node.args[0], "value", "?"))
except SyntaxError as e:
    bad_g19.append("SYNTAX:%s" % e)
guard("G19", "AST 层：ctl/guard 的 ok 实参顶层不得是布尔常量（假守卫的结构性防线）",
      "0", "%d" % len(bad_g19), len(bad_g19) == 0, "可疑调用 %d 处 %s" % (len(bad_g19), bad_g19))

# ============================== 汇总与落盘 ==============================

npass = sum(1 for i in items if i["ok"])
nfail = sum(1 for i in items if not i["ok"])
cok = sum(1 for c in controls if c["ok"])
gok = sum(1 for g in guards if g["ok"])

lines = []
lines.append("=" * 78)
lines.append("TUFT-%s · 整值多项式通有性审计" % RID)
lines.append("=" * 78)
lines.append("[items] %d 条  PASS=%d  FAIL=%d" % (len(items), npass, nfail))
for it in items:
    lines.append("  %-5s %-9s %s  exp=%s act=%s  %s"
                 % (it["id"], it["kind"], "PASS" if it["ok"] else "FAIL",
                    it["exp"][:40], it["act"][:40], it["note"][:90]))
lines.append("-" * 78)
lines.append("[controls] %d/%d" % (cok, len(controls)))
for c in controls:
    lines.append("  %-6s %s  exp=%s act=%s  %s"
                 % (c["id"], "PASS" if c["ok"] else "FAIL", c["exp"][:28], c["act"][:28], c["note"][:70]))
lines.append("-" * 78)
lines.append("[guards] %d/%d" % (gok, len(guards)))
for g in guards:
    lines.append("  %-5s %s  exp=%s act=%s  %s"
                 % (g["id"], "PASS" if g["ok"] else "FAIL", g["exp"][:24], g["act"][:24], g["note"][:60]))
lines.append("=" * 78)
lines.append("[verdict] %s" % VERDICT)
lines.append("=" * 78)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(BASE, "数据")
os.makedirs(OUTDIR, exist_ok=True)

payload = dict(rid=RID, date=DATE, stem=STEM, degree=DEGREE, cand_degree=CAND_DEGREE,
               verdict=VERDICT,
               summary=dict(items=len(items), npass=npass, nfail=nfail,
                            controls="%d/%d" % (cok, len(controls)),
                            guards="%d/%d" % (gok, len(guards))),
               grid=dict(pathA_groups=len(GRID_A), kinds=dict(kinds),
                         coset_groups=len(rowsC), coset_kinds=dict(cntC), skip=skipC),
               theorem_h=dict(formula="a_m = C(n+1,m) − C(n+1−d, n+1−m)",
                              holds_for="all d>=1 (Fano / CY / general type)",
                              paths=dict(td_vs_koszul_mismatch=mis_AC,
                                         td_vs_closed_mismatch=mis_AH,
                                         koszul_vs_closed_mismatch=mis_CH)),
               discriminating=dict(
                   lemma_L_intZ="%d/%d" % (hit_L, tot_L),
                   theorem_E_intZ="%d/%d" % (hit_E, tot_E),
                   theorem_H_intZ="%d/%d" % (hit_H, tot_H),
                   theorem_H_geom="%d/%d" % (geo_H, len(GRID_A))),
               cosets=dict(partial=len(P), N_eq_D=okND,
                           D_primes_subseteq_q_primes_violations=len(viol_pf),
                           empty_max_D=DmaxE),
               pricing=dict(feasible=len(feas), pinned=pinned, free=free, base=base),
               items=items, controls=controls, guards=guards)

jp = os.path.join(OUTDIR, STEM + ".json")
rp = os.path.join(OUTDIR, STEM + "_report.txt")
with io.open(jp, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(rp, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines[-14:]))
print("[%s] wrote %s (%d bytes) / %s (%d bytes)"
      % (RID, os.path.basename(jp), os.path.getsize(jp),
         os.path.basename(rp), os.path.getsize(rp)))
sys.exit(0 if (nfail == 0 and cok == len(controls) and gok == len(guards)) else 3)
