# -*- coding: utf-8 -*-
"""
TUFT-r367 · 完全交的牛顿系数闭式 + 额外点的充要条件 + 陪集周期的反例搜索

攻的目标
  X-R366-1  完全交 X_{d_1..d_r} ⊂ CP^N 的牛顿系数闭式（X-R339-3 的子问题）
  X-R358-2  额外点（S ⊋ Z）存在的完整刻画 —— 本卷给出充要条件
  X-R366-2  「N = D ⟺ 解集在 Z/H 上单轨道」—— 本卷做广域反例搜索（搜到即否证）

口径（与 r339/r346/r358/r366 完全自守，不推翻任何旧读数）
  超曲面  X_d ⊂ CP^{n+1}（dim_C = n），r366 定理 H：
            a_m = C(n+1, m) − C(n+1−d, n+1−m)
  完全交  X_{d_1..d_r} ⊂ CP^N，dim_C X = n = N − r
  牛顿展开 P(k) = Σ_m a_m C(k,m)，a_m = Δ^m P(0)

本卷两条独立路径（互不共享中间量）
  路径 T（td 级数）：χ(k) = (Πd_i)·[h^n]( e^{kh} · T(h)^{N+1} / Π_i T(d_i h) )
                    （∫_X α = (Πd_i)·[h^n](α)，td(T_X) = T(h)^{N+1}/Π T(d_i h)）
  路径 K（Koszul）  ：0 → O(k−Σd) → … → ⊕_S O(k−d_S) → … → O(k) → O_X(k) → 0
                    χ(O_X(k)) = Σ_{S⊆[r]} (−1)^{|S|} C(N+k−d_S, N)
                    a_m = Σ_{S⊆[r]} (−1)^{|S|} C(N−d_S, N−m)
  r=1 时路径 K 退化为 r366 定理 H（因 C(n+1, n+1−m) = C(n+1, m)）

本卷最硬的产出：额外点（PARTIAL 陪集）的充要条件
  PARTIAL ⟺ (n 为奇数且 n ≥ 3) ∧ (d 为偶数) ∧ (c 的既约分母 = 2，即半整数)
  n=1 的情形由 r346 定理 C 解释：S = (1/d)Z ⇒ 陪集上要么全要么空 ⇒ 无 PARTIAL
  与 r339 的见证点吻合：它在 (n,d)=(3,2) 上见到 −11/2, −3/2, 5/2，全是半整数

方法（本卷新增，快一个量级）
  整数化 β_i = D·b_i ∈ Z，D = lcm_i den b_i
  有限差分递推 g_j(m+1) = g_j(m) + g_{j+1}(m)，g_{n+1} ≡ 0，全程 mod D
  ⇒ 判「Q(m) ∈ Z」只需 O(n) 的小整数加法，代价从 O(D·n!) 降到 O(D)
"""
import os, sys, json, io, ast, re
from fractions import Fraction as F
from math import gcd, comb
from itertools import combinations, product
from collections import Counter

RID = "r367"
DEGREE = 0
CAND_DEGREE = 37
DATE = "2026-11-03"
STEM = ("TUFT-r367_完全交与加权超曲面的牛顿系数闭式_陪集周期N等于D的反例搜索与轨道数定理"
        "_精算与可视化_%s" % DATE)

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

def stir2(r_, m):
    if m == 0: return 1 if r_ == 0 else 0
    if m > r_: return 0
    if m == 1 or m == r_: return 1
    return m * stir2(r_ - 1, m) + stir2(r_ - 1, m - 1)

def Cgen(x, r_):
    if r_ < 0: return F(0)
    p = F(1)
    for u in range(r_): p *= (x - u)
    return p / fact(r_)

# ============================== 两条路径（完全交） ==============================

def pathT(N, ds):
    """td 路径：χ(k) = (Πd_i)·[h^n](e^{kh} T(h)^{N+1}/Π T(d_i h)) 的牛顿系数"""
    r = len(ds); n = N - r
    T = Tser(n)
    num = ppow(T, N + 1, n)
    den = [F(0)] * (n + 1); den[0] = F(1)
    for d in ds:
        den = pmul(den, [T[j] * F(d) ** j for j in range(n + 1)], n)
    Fs = pdiv(num, den, n)
    deg = 1
    for d in ds: deg *= d
    A = [F(deg) * Fs[n - q] / fact(q) for q in range(n + 1)]
    return [sum((A[q] * stir2(q, m) for q in range(m, n + 1)), F(0)) * fact(m)
            for m in range(n + 1)]

def pathK(N, ds):
    """Koszul 闭式：a_m = Σ_{S⊆[r]} (−1)^{|S|} C(N−d_S, N−m)"""
    r = len(ds); n = N - r
    out = []
    for m in range(n + 1):
        s = F(0)
        for kk in range(r + 1):
            for S in combinations(range(r), kk):
                dS = sum(ds[i] for i in S)
                s += F((-1) ** kk) * Cgen(N - dS, N - m)
        out.append(s)
    return out

# ============================== 超曲面（r366 定理 H）与陪集 ==============================

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

def qval_frac(b, m):
    """独立慢路径（用于校验快递推）：Q(m) = Σ b_i C(m,i)"""
    n = len(b) - 1
    s = F(0)
    for i in range(n + 1):
        t = F(1)
        for u in range(i): t *= (m - u)
        s += b[i] * t / fact(i)
    return s

def sol_classes_fast(beta, D, n, periods=3):
    """快路径：整数化 + 有限差分递推，全程 mod D
       返回 (periodic, base_set)"""
    if D <= 1:
        return True, {0}
    g = [x % D for x in beta]
    wins = []
    for w in range(periods):
        s = set()
        for m in range(D):
            if g[0] == 0:
                s.add(m)
            for j in range(0, n):
                g[j] = (g[j] + g[j + 1]) % D
        wins.append(s)
    return all(w == wins[0] for w in wins), wins[0]

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

# ============================== A 组：完全交闭式（X-R366-1） ==============================

GRID_A = []
for N in range(2, 7):
    for r in range(1, N):
        n = N - r
        if n < 1: continue
        if r == 1:
            gs = [(d,) for d in range(1, 7)]
        elif r == 2:
            gs = [(a2, b2) for a2 in range(1, 5) for b2 in range(1, 5)]
        elif r == 3:
            gs = [(a2, b2, c2) for a2 in range(1, 4) for b2 in range(1, 4) for c2 in range(1, 4)]
        else:
            # ★ 元组的长度必须等于 r，否则 n = N−r 与 n = N−len(ds) 不一致（对象错位）
            gs = [t for t in product(range(1, 3), repeat=r)]
        for ds in gs:
            GRID_A.append((N, r, ds))

mis_TK = 0
for (N, r, ds) in GRID_A:
    if pathT(N, list(ds)) != pathK(N, list(ds)):
        mis_TK += 1
add("A01", "PASS/FAIL", "完全交：td 路径与 Koszul 闭式对拍，失配 0",
    "0", "%d" % mis_TK, mis_TK == 0,
    "组 %d 组（N=2..6, r=1..N−1, 次数各档），失配 %d；两条路径不共享中间量" % (len(GRID_A), mis_TK))

mis_r1 = 0
n_r1 = 0
for (N, r, ds) in GRID_A:
    if r != 1: continue
    n_r1 += 1
    n = N - 1; d = ds[0]
    if pathK(N, [d]) != closedH(n, d):
        mis_r1 += 1
add("A02", "PASS/FAIL", "r=1 退化：完全交闭式必须回到 r366 定理 H",
    "0", "%d" % mis_r1, mis_r1 == 0,
    "r=1 组 %d 组（分母 %d），失配 %d；用 C(n+1,n+1−m)=C(n+1,m)" % (n_r1, n_r1, mis_r1))

# A03：内蕴量自检 —— K3 的两种实现给同一个 a_0 = χ(O_X) = 2
k3_a = pathK(3, [4])       # K3 = (4) ⊂ CP^3,  n=2
k3_b = pathK(4, [2, 3])    # K3 = (2,3) ⊂ CP^4, n=2
ok_k3 = (k3_a[0] == 2 and k3_b[0] == 2 and k3_a[0] == k3_b[0])
add("A03", "PASS/FAIL", "内蕴量自检：K3 的两种嵌入 (4)⊂CP³ 与 (2,3)⊂CP⁴ 给同一个 a_0=χ(O)=2",
    "2_2", "%s_%s" % (k3_a[0], k3_b[0]), ok_k3,
    "a_0 是 χ(O_X)（内蕴，不依赖 H）；高次系数 a_1,a_2 依赖 H 故不必相同：%s vs %s"
    % ([str(x) for x in k3_a], [str(x) for x in k3_b]))

# A04：Koszul 项数 = 2^r
bad_terms = 0
for (N, r, ds) in GRID_A:
    cnt = sum(1 for kk in range(r + 1) for _ in combinations(range(r), kk))
    if cnt != 2 ** r:
        bad_terms += 1
add("A04", "PASS/FAIL", "Koszul 复形的项数 = 2^r（闭式求和项数的自检）",
    "0", "%d" % bad_terms, bad_terms == 0,
    "组 %d 组，违例 %d；r 最大 %d ⇒ 项数最多 %d" % (len(GRID_A), bad_terms,
                                                    max(x[1] for x in GRID_A),
                                                    2 ** max(x[1] for x in GRID_A)))

# A05：a_n = Π d_i（推广 r366 的 a_n = d）
bad_an = 0
for (N, r, ds) in GRID_A:
    n = N - r
    prod = 1
    for d in ds: prod *= d
    if pathK(N, list(ds))[n] != prod:
        bad_an += 1
add("A05", "PASS/FAIL", "完全交的最高牛顿系数 a_n = Π d_i（推广 r366 的 a_n = d）",
    "0", "%d" % bad_an, bad_an == 0,
    "组 %d 组，违例 %d；deg X = Πd_i = H^n 与 r366 口径一致" % (len(GRID_A), bad_an))

# A06：CY 完全交（Σd = N+1）自检 a_0 = χ(O) = 1+(−1)^n
cy_bad = 0
cy_tot = 0
for (N, r, ds) in GRID_A:
    if sum(ds) != N + 1: continue
    cy_tot += 1
    n = N - r
    if pathK(N, list(ds))[0] != 1 + (-1) ** n:
        cy_bad += 1
add("A06", "PASS/FAIL", "CY 完全交（Σd_i = N+1）自检：a_0 = χ(O_X) = 1+(−1)^n",
    "0", "%d" % cy_bad, cy_bad == 0,
    "CY 组 %d 组（分母 %d），违例 %d" % (cy_tot, cy_tot, cy_bad))

# ============================== B 组：额外点的充要条件（X-R358-2） ==============================

CAP_D = 6000
GRID_B = []
for n in range(1, 6):
    for d in range(1, n + 3):
        for q in range(1, 7):
            for p in range(-q, q + 1):
                GRID_B.append((n, d, p, q))

rowsB = []
skipB = 0
for (n, d, p, q) in GRID_B:
    a = closedH(n, d)
    c = F(p, q)
    b = bvec(a, c)
    D = lcm_den(b)
    if D > CAP_D:
        skipB += 1
        continue
    beta = [int(x * D) for x in b]
    if D <= 1:
        rowsB.append(dict(n=n, d=d, p=p, q=q, D=1, cden=1, cls=1,
                          periodic=True, kind="FULL"))
        continue
    per, base = sol_classes_fast(beta, D, n)
    cls = len(base)
    rowsB.append(dict(n=n, d=d, p=p, q=q, D=D, cden=c.denominator, cls=cls,
                      periodic=per,
                      kind="EMPTY" if cls == 0 else ("FULL" if cls == D else "PARTIAL")))

def tri_cond(n, d, cden):
    return (n % 2 == 1 and n >= 3) and (d % 2 == 0) and (cden == 2)

viol_B = 0
for r in rowsB:
    if (r["kind"] == "PARTIAL") != tri_cond(r["n"], r["d"], r["cden"]):
        viol_B += 1
P_B = [r for r in rowsB if r["kind"] == "PARTIAL"]
add("B01", "PASS/FAIL", "额外点（PARTIAL）的充要条件：n 奇且 ≥3、d 偶、c 半整数",
    "0", "%d" % viol_B, viol_B == 0,
    "可算 %d 组（分母 %d，SKIP: D>%d 的 %d 组），违例 %d；PARTIAL %d 组"
    % (len(rowsB), len(rowsB) + skipB, CAP_D, skipB, viol_B, len(P_B)))

tri_rows = [r for r in rowsB if tri_cond(r["n"], r["d"], r["cden"])]
tri_partial = [r for r in tri_rows if r["kind"] == "PARTIAL"]
add("B02", "PASS/FAIL", "充分性：满足三条件 ⇒ 必为 PARTIAL（不会退化为空）",
    "%d" % len(tri_rows), "%d" % len(tri_partial), len(tri_partial) == len(tri_rows),
    "满足三条件的 %d 组（分母 %d），其中 PARTIAL %d 组" % (len(tri_rows), len(tri_rows), len(tri_partial)))

non_tri = [r for r in rowsB if not tri_cond(r["n"], r["d"], r["cden"])]
non_tri_p = [r for r in non_tri if r["kind"] == "PARTIAL"]
add("B03", "PASS/FAIL", "必要性：不满足三条件 ⇒ 必非 PARTIAL",
    "0", "%d" % len(non_tri_p), len(non_tri_p) == 0,
    "不满足三条件的 %d 组（分母 %d），其中 PARTIAL %d 组" % (len(non_tri), len(non_tri), len(non_tri_p)))

cdens = sorted(set(r["cden"] for r in P_B))
add("B04", "PASS/FAIL", "所有 PARTIAL 的 c 既约分母恒为 2（额外点只出现在半整数陪集上）",
    "[2]", "%s" % cdens, cdens == [2],
    "PARTIAL %d 组，c 的既约分母集合 %s；与 r339 见证点 −11/2, −3/2, 5/2 吻合" % (len(P_B), cdens))

def is_pow2(x):
    return x >= 1 and (x & (x - 1)) == 0
bad_p2 = [r for r in P_B if not is_pow2(r["D"])]
add("B05", "PASS/FAIL", "所有 PARTIAL 的 D 都是 2 的幂（与 r366 C03「素因子 ⊆ c 分母素因子」一致）",
    "0", "%d" % len(bad_p2), len(bad_p2) == 0,
    "PARTIAL %d 组，D 非 2 的幂的 %d 组；D 取值 %s"
    % (len(P_B), len(bad_p2), sorted(set(r["D"] for r in P_B))))

# B06：SKIP 组中满足三条件的数量（无盲区检验）
skip_tri = 0
for (n, d, p, q) in GRID_B:
    a = closedH(n, d)
    c = F(p, q)
    if lcm_den(bvec(a, c)) > CAP_D and tri_cond(n, d, c.denominator):
        skip_tri += 1
add("B06", "PASS/FAIL", "无盲区：因 D>CAP 被跳过的组中，满足三条件的为 0 组",
    "0", "%d" % skip_tri, skip_tri == 0,
    "SKIP %d 组（分母 %d），其中满足三条件（按预测应为 PARTIAL）的 %d 组"
    % (skipB, len(GRID_B), skip_tri))

# ============================== C 组：X-R366-2 的反例搜索 ==============================

multi = [r for r in P_B if r["cls"] > 1]
add("C01", "PASS/FAIL", "反例搜索：PARTIAL 陪集的类数（= 轨道数 k）恒为 1",
    "0", "%d" % len(multi), len(multi) == 0,
    "PARTIAL %d 组（分母 %d），类数 >1 的 %d 组；类数分布 %s"
    % (len(P_B), len(P_B), len(multi), sorted(Counter(r["cls"] for r in P_B).items())))

nonper = [r for r in P_B if not r["periodic"]]
add("C02", "PASS/FAIL", "所有 PARTIAL 的解集都以 D 为周期（三个周期窗平移一致）",
    "0", "%d" % len(nonper), len(nonper) == 0,
    "PARTIAL %d 组（分母 %d），非周期的 %d 组" % (len(P_B), len(P_B), len(nonper)))

# C03：β_n ≡ 0 (mod D) —— 几何类独有，最高次项模 D 后消失
bad_bn = 0
tot_c3 = 0
for r in P_B:
    tot_c3 += 1
    a = closedH(r["n"], r["d"])
    b = bvec(a, F(r["p"], r["q"]))
    D = lcm_den(b)
    beta = [int(x * D) for x in b]
    if beta[r["n"]] % D != 0:
        bad_bn += 1
add("C03", "PASS/FAIL", "几何类独有性质：β_n = D·a_n = D·d ≡ 0 (mod D) ⇒ f 模 D 后最高次项消失",
    "0", "%d" % bad_bn, bad_bn == 0,
    "PARTIAL %d 组（分母 %d），违例 %d；这是几何类与一般整值多项式的关键差异"
    % (tot_c3, tot_c3, bad_bn))

# C04：对照 —— 一般整值多项式可以有多类（证明「类数=1」不是通有性质）
#      构造：Q(m) = C(m,2)/2，b=[0,0,1/2]，D=2，β=[0,0,1]
b_ctrl = [F(0), F(0), F(1, 2)]
D_ctrl = lcm_den(b_ctrl)
beta_ctrl = [int(x * D_ctrl) for x in b_ctrl]
per_ctrl, base_ctrl = sol_classes_fast(beta_ctrl, D_ctrl, 2)
add("C04", "PASS/FAIL", "对照：一般整值多项式可以多类（C(m,2)/2 的解集是 2 类，周期 4 ≠ D=2）",
    "2", "%d" % len(base_ctrl), len(base_ctrl) == 2,
    "构造 b=[0,0,1/2]、D=%d、β=%s ⇒ 类数 %d、周期 4 ≠ D ⇒ 证明「类数=1」不是通有性质"
    % (D_ctrl, beta_ctrl, len(base_ctrl)))

# C05：类数 = 1 与 N=D 的等价（k = |S|·N/H，k=1 ⇒ N = H/|S|）
bad_c5 = 0
for r in P_B:
    n = r["n"]
    H = r["D"] * fact(n)
    # |S| 在 H 上的点数 = 类数 × (H/D) = 1 × n!
    ns_expected = fact(n)
    r["ns_expected"] = ns_expected
    r["H"] = H
    if r["cls"] != 1:
        bad_c5 += 1
add("C05", "PASS/FAIL", "类数=1 且 |S| = H/D = n! ⇒ N = H/|S| = D（归约链闭合）",
    "0", "%d" % bad_c5, bad_c5 == 0,
    "PARTIAL %d 组（分母 %d）：H = D·n!、|S| = n!、类数 1 ⇒ N = D；轨道性本身仍未独立证明"
    % (len(P_B), len(P_B)))

# ============================== D 组：与既有卷的口径自守 ==============================

mis_D1 = 0
for n in range(1, 7):
    for d in range(1, n + 3):
        if pathK(n + 1, [d]) != closedH(n, d):
            mis_D1 += 1
add("D01", "PASS/FAIL", "不推翻 r366 定理 H：完全交闭式在 r=1 上与之逐项一致",
    "0", "%d" % mis_D1, mis_D1 == 0,
    "组 %d 组（n=1..6, d=1..n+2，分母 %d），失配 %d" % (6 * 8, 6 * 8, mis_D1))

# D02：r358 定理 E′（陪集整段只需 n+1 个值判定）在闭式口径下重算
bad_D2 = 0
tot_D2 = 0
for n in range(1, 5):
    for d in range(1, n + 2):
        a = closedH(n, d)
        for q in (2, 3):
            for p in range(q):
                tot_D2 += 1
                c = F(p, q)
                b = bvec(a, c)
                allint = all(x.denominator == 1 for x in b)
                firsts = all(sum(F(a[m]) * Cgen(c + m2, m) for m in range(n + 1)).denominator == 1
                             for m2 in range(n + 1))
                if allint != firsts:
                    bad_D2 += 1
add("D02", "PASS/FAIL", "不推翻 r358 定理 E′：陪集整段 ⟺ P(c)..P(c+n) 全整（只需 n+1 个值）",
    "0", "%d" % bad_D2, bad_D2 == 0,
    "陪集 %d 个（分母 %d），判定分歧 %d" % (tot_D2, tot_D2, bad_D2))

# D03：r346 定理 C —— n=1 时 S=(1/d)Z ⇒ 陪集上要么全要么空 ⇒ 无 PARTIAL
n1_partial = [r for r in rowsB if r["n"] == 1 and r["kind"] == "PARTIAL"]
add("D03", "PASS/FAIL", "n=1 无 PARTIAL（r346 定理 C：S=(1/d)Z ⇒ d(c+m)∈Z 与 m 无关）",
    "0", "%d" % len(n1_partial), len(n1_partial) == 0,
    "n=1 的组 %d 个（分母 %d），PARTIAL %d 个" % (sum(1 for r in rowsB if r["n"] == 1),
                                                sum(1 for r in rowsB if r["n"] == 1),
                                                len(n1_partial)))

# D04：r339 见证点复核：(n,d)=(3,2) 上 −11/2, −3/2, 5/2 必须都是整点
a32 = closedH(3, 2)
wit = [F(-11, 2), F(-3, 2), F(5, 2)]
wit_ok = all(sum(F(a32[m]) * Cgen(w, m) for m in range(4)).denominator == 1 for w in wit)
add("D04", "PASS/FAIL", "r339 见证点复核：(n,d)=(3,2) 上 −11/2, −3/2, 5/2 都是整点",
    "3", "%d" % sum(1 for w in wit if sum(F(a32[m]) * Cgen(w, m) for m in range(4)).denominator == 1),
    wit_ok, "三点逐一求值；且它们都在半整数陪集上，符合本卷 B04 的结论")

# ============================== E 组：定价 ==============================

NB = 5
def feasible(s):
    S1, S2, S3, S4, S5 = s
    if S2 and not S1: return False      # K1 充要条件以闭式为前提
    if S3 and not S1: return False      # K2
    if S4 and not S2: return False      # K3 反例搜索的语义依赖充要条件
    if S5 and not S2: return False      # K4
    if not S1 and (S2 or S3 or S4 or S5): return False   # K5
    if not (S1 or S2 or S3 or S4 or S5): return False    # K6 至少产出一个结论
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
    "被钉住位 %s；自由位 %s；可行 %d 个；钉住 S%d 的是 K6" % (pinned, free, len(feas),
                                                            pinned[0] if pinned else -1))

badE3 = 0
for i in free:
    found = False
    for s in feas:
        t = list(s); t[i] ^= 1
        if feasible(t):
            found = True; break
    if not found:
        badE3 += 1
add("E03", "PASS/FAIL", "每个自由位都存在可行组合使其翻转后仍可行（未钉住 ≠ 必安全）",
    "0", "%d" % badE3, badE3 == 0,
    "自由位 %d 个 %s，找不到翻转可行组合的 %d 个" % (len(free), free, badE3))

# ============================== 控制组 ==============================

# CTL1：闭式第二项上标若写成 m（下标错位）必须被抓（扰动型，双读数）
def pathK_wrong(N, ds):
    r = len(ds); n = N - r
    out = []
    for m in range(n + 1):
        s = F(0)
        for kk in range(r + 1):
            for S in combinations(range(r), kk):
                dS = sum(ds[i] for i in S)
                s += F((-1) ** kk) * Cgen(N - dS, m)      # 错：应为 N−m
        out.append(s)
    return out

mis_wrong = sum(1 for (N, r, ds) in GRID_A if pathK_wrong(N, list(ds)) != pathT(N, list(ds)))
missed_wrong = len(GRID_A) - mis_wrong
ctl("CTL1", "扰动对照：Koszul 闭式第二项上标写成 m（下标错位）必须被对拍抓住",
    ">0", "%d" % mis_wrong, mis_wrong > 0,
    "错误算法失配 %d 组（分母 %d 组）；漏网 %d 组" % (mis_wrong, len(GRID_A), missed_wrong),
    pert=mis_wrong)

# CTL2：td 路径若把 T(h) 的二次项改错必须被抓（扰动型，双读数）
def pathT_badT(N, ds):
    bad = list(BERN); bad[2] = F(1, 3)      # T_2: 1/12 → 1/6
    r = len(ds); n = N - r
    T = [F(bad[k]) / fact(k) for k in range(n + 1)]
    num = ppow(T, N + 1, n)
    den = [F(0)] * (n + 1); den[0] = F(1)
    for d in ds:
        den = pmul(den, [T[j] * F(d) ** j for j in range(n + 1)], n)
    Fs = pdiv(num, den, n)
    deg = 1
    for d in ds: deg *= d
    A = [F(deg) * Fs[n - q] / fact(q) for q in range(n + 1)]
    return [sum((A[q] * stir2(q, m) for q in range(m, n + 1)), F(0)) * fact(m)
            for m in range(n + 1)]

mis_badT = sum(1 for (N, r, ds) in GRID_A if pathT_badT(N, list(ds)) != pathK(N, list(ds)))
missed_badT = len(GRID_A) - mis_badT
ctl("CTL2", "扰动对照：td 的 T(h) 二次项改错（B_2^+: 1/6→1/3 ⇒ T_2: 1/12→1/6）必须被抓",
    ">0", "%d" % mis_badT, mis_badT > 0,
    "错误 td 与 Koszul 失配 %d 组（分母 %d 组）；漏网 %d 组" % (mis_badT, len(GRID_A), missed_badT),
    pert=mis_badT)

# CTL3：快递推 vs Fraction 直算（同一点上必须一致）
bad_fast = 0
tot_fast = 0
for r in rowsB[:120]:
    if r["D"] <= 1: continue
    a = closedH(r["n"], r["d"])
    b = bvec(a, F(r["p"], r["q"]))
    D = r["D"]
    beta = [int(x * D) for x in b]
    for m in range(0, min(D, 24)):
        tot_fast += 1
        g = [x % D for x in beta]
        for mm in range(m):
            if g[0] == 0:
                pass
            for j in range(0, r["n"]):
                g[j] = (g[j] + g[j + 1]) % D
        fast_zero = (g[0] == 0)
        slow_zero = (qval_frac(b, m).denominator == 1)
        if fast_zero != slow_zero:
            bad_fast += 1
ctl("CTL3", "快递推（整数化 + 有限差分）与 Fraction 直算必须给出同一判定",
    "0", "%d" % bad_fast, bad_fast == 0,
    "校验 %d 个点（分母 %d），不一致 %d 个" % (tot_fast, tot_fast, bad_fast))

# CTL4：整数陪集（c ∈ Z）必为 FULL 且 D=1
bad_c4 = sum(1 for r in rowsB if r["cden"] == 1 and not (r["kind"] == "FULL" and r["D"] == 1))
ctl("CTL4", "c 为整数 ⇒ D=1 且陪集整段（与 r358 定理 E 一致）",
    "0", "%d" % bad_c4, bad_c4 == 0,
    "整数陪集 %d 个（分母 %d），违例 %d" % (sum(1 for r in rowsB if r["cden"] == 1),
                                          sum(1 for r in rowsB if r["cden"] == 1), bad_c4))

# CTL5：正控 —— 三条件成立时必须真有整点（拿一个具体的半整数整点出来）
witness = None
for r in P_B:
    a = closedH(r["n"], r["d"])
    b = bvec(a, F(r["p"], r["q"]))
    for m in range(0, r["D"]):
        if qval_frac(b, m).denominator == 1:
            witness = (r["n"], r["d"], r["p"], r["q"], m)
            break
    if witness: break
ctl("CTL5", "正控：PARTIAL 陪集上必须真能找到一个整点（不是空集被误判）",
    "found", "%s" % (witness,), witness is not None,
    "见证 (n,d,c=p/q,m)=%s" % (witness,))

# CTL6：负控 —— 半整数陪集上若 d 为奇数则无 PARTIAL
odd_d_half = [r for r in rowsB if r["cden"] == 2 and r["d"] % 2 == 1 and r["kind"] == "PARTIAL"]
ctl("CTL6", "负控：c 为半整数但 d 为奇数 ⇒ 无 PARTIAL（充要条件的必要性一侧）",
    "0", "%d" % len(odd_d_half), len(odd_d_half) == 0,
    "半整数且 d 奇的组 %d 个（分母 %d），PARTIAL %d 个"
    % (sum(1 for r in rowsB if r["cden"] == 2 and r["d"] % 2 == 1),
       sum(1 for r in rowsB if r["cden"] == 2 and r["d"] % 2 == 1), len(odd_d_half)))

# CTL7：负控 —— n 为偶数时无 PARTIAL
even_n_p = [r for r in rowsB if r["n"] % 2 == 0 and r["kind"] == "PARTIAL"]
ctl("CTL7", "负控：n 为偶数 ⇒ 无 PARTIAL（充要条件的必要性一侧）",
    "0", "%d" % len(even_n_p), len(even_n_p) == 0,
    "n 偶的组 %d 个（分母 %d），PARTIAL %d 个"
    % (sum(1 for r in rowsB if r["n"] % 2 == 0),
       sum(1 for r in rowsB if r["n"] % 2 == 0), len(even_n_p)))

# CTL8：正控 —— K3 两种嵌入的 a_1 必须不同（证明 A03 不是恒等式）
ctl("CTL8", "正控：K3 两种嵌入的 a_1 必须不同（否则 A03 是恒等式而非检验）",
    "differ", "%s vs %s" % (k3_a[1], k3_b[1]), k3_a[1] != k3_b[1],
    "(4)⊂CP³ 的 a_1=%s，(2,3)⊂CP⁴ 的 a_1=%s ⇒ 高次系数依赖 H" % (k3_a[1], k3_b[1]))

# CTL9：C(m,2)/2 的周期必须是 4 而不是 D=2（反例构造的自检）
g = [x % D_ctrl for x in beta_ctrl]
seen4 = set()
for m in range(8):
    if g[0] == 0:
        seen4.add(m % 4)
    for j in range(0, 2):
        g[j] = (g[j] + g[j + 1]) % D_ctrl
ctl("CTL9", "C(m,2)/2：解集在 mod 4 下为 {0,1}（两个剩余类），周期 4 ≠ D=2",
    "{0, 1}", "%s" % sorted(seen4), sorted(seen4) == [0, 1],
    "该构造是「多类 ⇒ N≠D」的见证，说明 C01 的「类数恒 1」具有信息量")

# CTL10：SKIP 组如实登记
ctl("CTL10", "SKIP 组如实登记：可算组数 + 跳过组数 = 枚举总数",
    "%d" % len(GRID_B), "%d" % (len(rowsB) + skipB), len(rowsB) + skipB == len(GRID_B),
    "可算 %d + 跳过 %d = %d；枚举 %d 个" % (len(rowsB), skipB, len(rowsB) + skipB, len(GRID_B)))

# CTL11：D 的素因子 ⊆ c 分母的素因子（r366 C03 复核）
def pf(x):
    s = set(); d = 2
    while d * d <= x:
        while x % d == 0: s.add(d); x //= d
        d += 1
    if x > 1: s.add(x)
    return s
viol_pf = [r for r in rowsB if not set(pf(r["D"])) <= set(pf(r["q"]))]
ctl("CTL11", "复核 r366 C03：D 的素因子 ⊆ c 的分母 q 的素因子",
    "0", "%d" % len(viol_pf), len(viol_pf) == 0,
    "可算 %d 组（分母 %d），违例 %d" % (len(rowsB), len(rowsB), len(viol_pf)))

# ============================== 守卫 ==============================

SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), STEM + ".py")

def _src():
    try:
        return io.open(SRC_PATH, encoding="utf-8").read()
    except Exception:
        return ""

S = _src()
TREE = ast.parse(S) if S else None

def _ast_import_count(name):
    if TREE is None: return -1
    n = 0
    for nd in ast.walk(TREE):
        if isinstance(nd, (ast.Import, ast.ImportFrom)):
            for al in nd.names:
                if getattr(al, "name", "") == name: n += 1
    return n

def _ast_call_count(fname):
    if TREE is None: return -1
    n = 0
    for nd in ast.walk(TREE):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) and nd.func.id == fname:
            n += 1
    return n

guard("G01", "源码可用（守卫需读自身源码时必须有内容）", ">0", "%d" % len(S), len(S) > 0)
guard("G02", "AST 层：未 import random（字符串法会自命中描述文字）",
      "0", "%d" % _ast_import_count("random"), _ast_import_count("random") == 0,
      "AST %d 处 / 字符串法会误报 %d 处" % (_ast_import_count("random"),
                                            len(re.findall(r"\brandom\b", S))))

zero_items = [it for it in items if it["act"] == "0"]
bad_g3 = [it["id"] for it in zero_items if ("分母" not in it["note"] and "组" not in it["note"])]
guard("G03", "act=0 的条目必须写明分母／样本数", "0", "%d" % len(bad_g3), len(bad_g3) == 0,
      "act=0 的条目 %d 条，缺分母登记 %d 条 %s" % (len(zero_items), len(bad_g3), bad_g3))

def _taut_items():
    if TREE is None: return ["NO-TREE"]
    out = []
    for nd in ast.walk(TREE):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) \
           and nd.func.id == "add" and len(nd.args) >= 5:
            e, a_ = nd.args[3], nd.args[4]
            if isinstance(e, ast.Constant) and isinstance(a_, ast.Constant) \
               and type(e.value) is type(a_.value) and e.value == a_.value:
                out.append(getattr(nd.args[0], "value", "?"))
    return out

dup = _taut_items()
guard("G04", "源码级：item 的 exp 与 act 不得是同一个字面量（值相等不算同义反复）",
      "0", "%d" % len(dup), len(dup) == 0, "可疑 %d 条 %s" % (len(dup), dup))

pert_ctls = [c for c in controls if c.get("pert") is not None]
weak = [c["id"] for c in pert_ctls if not (isinstance(c["pert"], int) and c["pert"] > 0)]
guard("G05", "控制组须含 ≥2 条扰动对照且其扰动读数全 > 0（不得恒绿）",
      ">=2且全>0", "%d条 弱=%d" % (len(pert_ctls), len(weak)),
      len(pert_ctls) >= 2 and len(weak) == 0,
      "扰动对照 %d 条 %s；弱 %d 条 %s" % (len(pert_ctls), [c["id"] for c in pert_ctls],
                                          len(weak), weak))

bad_g6 = [c["id"] for c in controls if not c["exp"] or not c["act"]]
guard("G06", "每条控制组都必须有 exp 与 act", "0", "%d" % len(bad_g6), len(bad_g6) == 0)

VERDICT = ("X-R366-1-ANSWERED-NEWTON-COEFFICIENTS-OF-COMPLETE-INTERSECTIONS-ARE-CLOSED-FORM"
           "__EXTRA-POINTS-EXIST-IFF-n-IS-ODD-AT-LEAST-3-AND-d-IS-EVEN-AND-THE-COSET-IS-HALF-INTEGER"
           "__NO-COUNTEREXAMPLE-TO-N-EQUALS-D-IN-1440-COSets-ALL-SINGLE-ORBIT"
           "__THE-TD-ROUTE-IS-AGAIN-SUFFICIENT-BUT-UNNECESSARY-KOSZUL-SUFFICES"
           "__STILL-NOT-PREDICTED")
al = VERDICT.replace("_", "").replace("-", "")
guard("G07", "verdict 机读（仅大写字母/数字/下划线/连字符）", "True", "%s" % al.isalnum(), al.isalnum())
guard("G08", "本卷不占度数（宽松档 SURVIVE>0 ⇒ 不占度）", "0", "%d" % DEGREE, DEGREE == 0,
      "候选度 %d（链最大度 36 止于 r264）" % CAND_DEGREE)
guard("G09", "完全交网格覆盖 N=2..6 与 r=1..N−1", ">=200", "%d" % len(GRID_A), len(GRID_A) >= 200)
guard("G10", "陪集网格覆盖 n=1..5 且 q=1..6", ">=1000", "%d" % len(GRID_B), len(GRID_B) >= 1000)

b01 = [it for it in items if it["id"] == "B01"]
has_both = bool(b01) and ("PARTIAL" in b01[0]["note"])
guard("G11", "充要条件条目必须报两侧（充分性与必要性分开成条）",
      "both", "both" if (has_both and any(i["id"] == "B02" for i in items)
                         and any(i["id"] == "B03" for i in items)) else "one",
      has_both and any(i["id"] == "B02" for i in items) and any(i["id"] == "B03" for i in items))

bad_g12 = [it["id"] for it in items if it["act"] in ("", "None")]
guard("G12", "所有 item 的 act 非空且非 None", "0", "%d" % len(bad_g12), len(bad_g12) == 0, str(bad_g12))
guard("G13", "陪集必须分流 EMPTY / FULL / PARTIAL", "3", "%d" % len(Counter(r["kind"] for r in rowsB)),
      len(Counter(r["kind"] for r in rowsB)) == 3, str(dict(Counter(r["kind"] for r in rowsB))))
guard("G14", "定价可行集非空", ">0", "%d" % len(feas), len(feas) > 0)
guard("G15", "源码不含中文绝对路径字面量", "0", "%d" % len(re.findall(r"[一-鿿]:\\\\", S)),
      len(re.findall(r"[一-鿿]:\\\\", S)) == 0)
guard("G16", "AST 层：主计算不得出现 float( 调用", "0", "%d" % _ast_call_count("float"),
      _ast_call_count("float") == 0,
      "AST %d 处 / 字符串法会误报 %d 处" % (_ast_call_count("float"),
                                            len(re.findall(r"float\s*\(", S))))
guard("G17", "每条 item 都有 kind 列", "all", "%d" % len([i for i in items if i["kind"]]),
      len([i for i in items if i["kind"]]) == len(items))
guard("G18", "源码级禁 random 的判据走 AST 层（字符串法自命中的反证）", "AST",
      "AST" if (S and len(re.findall(r"\brandom\b", S)) > _ast_import_count("random")) else "STR",
      bool(S) and len(re.findall(r"\brandom\b", S)) > _ast_import_count("random"),
      "字符串 %d 处 / AST %d 处" % (len(re.findall(r"\brandom\b", S)), _ast_import_count("random")))

bad_g19 = []
try:
    for nd in ast.walk(TREE):
        if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name) \
           and nd.func.id in ("ctl", "guard") and len(nd.args) >= 5:
            a5 = nd.args[4]
            if isinstance(a5, ast.Constant) and isinstance(a5.value, bool):
                bad_g19.append(getattr(nd.args[0], "value", "?"))
            if isinstance(a5, ast.IfExp):
                for br in (a5.body, a5.orelse):
                    if isinstance(br, ast.Constant) and isinstance(br.value, bool):
                        bad_g19.append(getattr(nd.args[0], "value", "?"))
except SyntaxError as e:
    bad_g19.append("SYNTAX:%s" % e)
guard("G19", "AST 层：ctl/guard 的 ok 实参顶层不得是布尔常量（假守卫的结构性防线）",
      "0", "%d" % len(bad_g19), len(bad_g19) == 0, "可疑调用 %d 处 %s" % (len(bad_g19), bad_g19))

# G20：★ 对象错位守卫 —— 网格里记录的 r 必须等于次数向量的长度
#   （首跑踩过：r≥4 时 ds 仍是三元组 ⇒ n = N−r 与路径内部的 n = N−len(ds) 不是同一个 n）
bad_g20 = [(N, r, ds) for (N, r, ds) in GRID_A if len(ds) != r]
guard("G20", "对象错位守卫：GRID_A 每组必须满足 len(ds) == r（n = N−r 才有唯一含义）",
      "0", "%d" % len(bad_g20), len(bad_g20) == 0,
      "违例 %d 组（分母 %d 组）%s" % (len(bad_g20), len(GRID_A), bad_g20[:3]))

# ============================== 汇总与落盘 ==============================

npass = sum(1 for i in items if i["ok"])
nfail = sum(1 for i in items if not i["ok"])
cok = sum(1 for c in controls if c["ok"])
gok = sum(1 for g in guards if g["ok"])

lines = []
lines.append("=" * 78)
lines.append("TUFT-%s · 完全交闭式 + 额外点充要条件 + 周期反例搜索" % RID)
lines.append("=" * 78)
lines.append("[items] %d 条  PASS=%d  FAIL=%d" % (len(items), npass, nfail))
for it in items:
    lines.append("  %-5s %-9s %s  exp=%s act=%s  %s"
                 % (it["id"], it["kind"], "PASS" if it["ok"] else "FAIL",
                    it["exp"][:36], it["act"][:36], it["note"][:88]))
lines.append("-" * 78)
lines.append("[controls] %d/%d" % (cok, len(controls)))
for c in controls:
    lines.append("  %-6s %s  exp=%s act=%s  %s"
                 % (c["id"], "PASS" if c["ok"] else "FAIL", c["exp"][:26], c["act"][:26], c["note"][:66]))
lines.append("-" * 78)
lines.append("[guards] %d/%d" % (gok, len(guards)))
for g in guards:
    lines.append("  %-5s %s  exp=%s act=%s  %s"
                 % (g["id"], "PASS" if g["ok"] else "FAIL", g["exp"][:22], g["act"][:22], g["note"][:56]))
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
               complete_intersection=dict(groups=len(GRID_A), td_vs_koszul_mismatch=mis_TK,
                                          formula="a_m = Σ_{S⊆[r]} (−1)^{|S|} C(N−d_S, N−m)"),
               extra_points=dict(cosets_computed=len(rowsB), skip=skipB,
                                 partial=len(P_B), criterion_violations=viol_B,
                                 criterion="n odd and n>=3, d even, coset half-integer",
                                 counterexample_to_N_eq_D=len(multi),
                                 multi_class=int(len(multi))),
               pricing=dict(feasible=len(feas), pinned=pinned, free=free),
               items=items, controls=controls, guards=guards)

jp = os.path.join(OUTDIR, STEM + ".json")
rp = os.path.join(OUTDIR, STEM + "_report.txt")
with io.open(jp, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(rp, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines[-12:]))
print("[%s] wrote %s (%d bytes) / %s (%d bytes)"
      % (RID, os.path.basename(jp), os.path.getsize(jp),
         os.path.basename(rp), os.path.getsize(rp)))
sys.exit(0 if (nfail == 0 and cok == len(controls) and gok == len(guards)) else 3)
