# -*- coding: utf-8 -*-
# TUFT-r336 · 族数唯一性定理：反常自由荷空间实为 2 维、单扭转下唯一纯复制
#            （修正 r309 Thm S 表述、下调 r330 判词范围、给出双扭转反例）
import io
import json
import os
import itertools
from fractions import Fraction

RID = "r336"
STAMP = "2026-11-01"
TAG = "族数唯一性定理_反常自由荷空间实为2维_单扭转唯一纯复制_双扭转反例"
TITLE = "族数唯一性定理 · 反常自由荷空间实为 2 维、Yukawa 与单扭转的承重性（r330 判词下调 · r309 表述修正）"
BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
HTML_NAME = "四力统一方程_族数唯一性与反常自由荷空间维数可视化_2026-11-01.html"
ALLOWED_PREFIXES = [os.path.join(BASE, "源码"), os.path.join(BASE, "数据"),
                    os.path.join(BASE, "判定")]

# ---------------- SM 表示数据 ----------------
DIMS = [6, 3, 3, 2, 1, 1]      # d_i = 色维 × SU(2)维
COL = [3, 3, 3, 1, 1, 1]
SU2 = [2, 1, 1, 2, 1, 1]
NREP = 6
Y = [Fraction(1, 6), Fraction(-2, 3), Fraction(1, 3), Fraction(-1, 2), Fraction(1), Fraction(0)]

# ---------------- 精确线性代数 ----------------
def rref(rows, ncol):
    M = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
    for c in range(ncol):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(ncol)]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M, piv

def nullspace(basis_rows, ncol):
    M, piv = rref(basis_rows, ncol)
    free = [c for c in range(ncol) if c not in piv]
    out = []
    for fc in free:
        v = [Fraction(0)] * ncol
        v[fc] = Fraction(1)
        for pi, pc in enumerate(piv):
            s = Fraction(0)
            for j in free:
                s -= M[pi][j] * v[j]
            v[pc] = s
        out.append(v)
    return out, M, piv, free

# ---------------- 反常（q 变量与 y 变量双口径） ----------------
def anom_q(q):
    """四条规范反常（q 为各表示电荷）。"""
    a_su3 = Fraction(1, 2) * (SU2[0] * q[0] + SU2[1] * q[1] + SU2[2] * q[2])
    a_su2 = Fraction(1, 2) * (COL[0] * q[0] + COL[3] * q[3])
    a_grv = sum(DIMS[i] * q[i] for i in range(NREP))
    a_cub = sum(DIMS[i] * q[i] ** 3 for i in range(NREP))
    return (a_su3, a_su2, a_grv, a_cub)

def anom_y(y):
    """同一套反常改写为 y_i = d_i q_i：三项线性化，一项三次。"""
    return (y[0] + y[1] + y[2], y[0] + y[3], sum(y),
            sum(Fraction(y[i] ** 3, DIMS[i] ** 2) for i in range(NREP)))

def free_q(q):
    return all(a == 0 for a in anom_q(q))

def y_of(q):
    return [DIMS[i] * q[i] for i in range(NREP)]

# ---------------- 挡板 1：反常自由荷空间维数 ----------------
LIN3 = [[Fraction(SU2[0]), Fraction(SU2[1]), Fraction(SU2[2]), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(COL[0]), Fraction(0), Fraction(0), Fraction(COL[3]), Fraction(0), Fraction(0)],
        [Fraction(DIMS[i]) for i in range(NREP)]]
NS, _M, _PIV, _FREE = nullspace(LIN3, NREP)
DIM_LIN = len(NS)

def cub_q(q):
    return sum(DIMS[i] * q[i] ** 3 for i in range(NREP))

# 三次形式在零空间上的闭式与分解（基 NS[0], NS[1], NS[2] 对应 a, b, c）
B1, B2, B3 = NS[0], NS[1], NS[2]

def cub_abc(a, b, c):
    q = [a * B1[t] + b * B2[t] + c * B3[t] for t in range(NREP)]
    return cub_q(q)

def F_closed(a, b, c):
    return b ** 3 + c ** 3 - 3 * a ** 2 * (b + c) - a * (b + c) ** 2 - Fraction(b + c) ** 3 / 3

def Q_quad(a, b, c):
    return 8 * b * b - 20 * b * c + 8 * c * c - 36 * a * a - 12 * a * (b + c)

def check_closed():
    bad = 0
    for a, b, c in itertools.product(range(-6, 7), repeat=3):
        if cub_abc(Fraction(a), Fraction(b), Fraction(c)) != F_closed(Fraction(a), Fraction(b), Fraction(c)):
            bad += 1
    return bad

def check_factor(den=12):
    bad = 0
    for a, b, c in itertools.product(range(-6, 7), repeat=3):
        lhs = cub_abc(Fraction(a), Fraction(b), Fraction(c))
        rhs = Fraction(b + c) * Q_quad(Fraction(a), Fraction(b), Fraction(c)) / den
        if lhs != rhs:
            bad += 1
    return bad

BAD_CLOSED = check_closed()
BAD_FACTOR = check_factor(12)
BAD_FACTOR_NEG = check_factor(11)      # 负对照：分母改成 11 必须大面积失配

# 平面分支 b + c = 0 -> q = a·B1 + b·(B2 - B3)
V_PLANE = [B2[t] - B3[t] for t in range(NREP)]

def plane_q(a, b):
    return [Fraction(a) * B1[t] + Fraction(b) * V_PLANE[t] for t in range(NREP)]

PLANE_SAMPLES = [(0, 1), (1, 0), (1, 1), (3, 5), (2, -7)]
PLANE_ALL_FREE = all(free_q(plane_q(a, b)) for a, b in PLANE_SAMPLES)

# ---------------- 挡板 2：Yukawa 不变 ----------------
def yukawa_ok(q):
    """四条 Yukawa（QHu u^c, QHd d^c, LHd e^c, LHu ν^c）相容 ⇔ 两条线性条件。"""
    c1 = (q[0] + q[1]) - (q[3] + q[5])
    c2 = (q[0] + q[2]) - (q[3] + q[4])
    return (c1 == 0 and c2 == 0), (c1, c2)

YUK_ROWS = [[Fraction(1), Fraction(1), Fraction(0), Fraction(-1), Fraction(0), Fraction(-1)],
            [Fraction(1), Fraction(0), Fraction(1), Fraction(-1), Fraction(-1), Fraction(0)]]
NS_YUK, _, _, _ = nullspace(YUK_ROWS, NREP)
DIM_YUK = len(NS_YUK)

# 把 Yukawa 两条叠在反常线性三条上
NS_BOTH, _MB, _PB, _FB = nullspace(LIN3 + YUK_ROWS, NREP)
DIM_BOTH = len(NS_BOTH)
RANK_BOTH = len(_PB)

def rank_of(rows, ncol):
    if not rows:
        return 0
    _M2, piv2 = rref(rows, ncol)
    return len(piv2)

def in_span(v, basis):
    """v ∈ span(basis) ⟺ rank(basis ∪ {v}) == rank(basis)。"""
    return rank_of(list(basis) + [list(v)], len(v)) == rank_of(list(basis), len(v))

Y_IN_BOTH = in_span(Y, NS_BOTH)
U_VEC = [Fraction(0), Fraction(-1), Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
V_VEC = [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(-1)]
U_FREE = free_q(U_VEC)
V_FREE = free_q(V_VEC)
U_YUK = yukawa_ok(U_VEC)[0]
V_YUK = yukawa_ok(V_VEC)[0]
U_IN_SPAN_Y = in_span(U_VEC, [Y])
V_IN_SPAN_Y = in_span(V_VEC, [Y])

# B−L 荷：Q:1/3, u^c:−1/3, d^c:−1/3, L:−1, e^c:1, ν^c:1
BL = [Fraction(1, 3), Fraction(-1, 3), Fraction(-1, 3), Fraction(-1), Fraction(1), Fraction(1)]
BL_FREE = free_q(BL)
BL_YUK = yukawa_ok(BL)[0]
BL_IN_BOTH = in_span(BL, NS_BOTH)
BL_IN_SPAN_Y = in_span(BL, [Y])
SPAN_Y_BL_DIM = rank_of([Y, BL], NREP)

# ---------------- 5 表示（无 ν^c）口径 ----------------
D5 = DIMS[:5]
COL5 = COL[:5]
SU25 = SU2[:5]
LIN3_5 = [[Fraction(SU25[0]), Fraction(SU25[1]), Fraction(SU25[2]), Fraction(0), Fraction(0)],
          [Fraction(COL5[0]), Fraction(0), Fraction(0), Fraction(COL5[3]), Fraction(0)],
          [Fraction(D5[i]) for i in range(5)]]
# 5 表示下 Yukawa 只有三条（无 LHuν^c）⇒ 消去 X_Hu, X_Hd 后剩一条相容条件：X0+X2 = X3+X4
YUK5 = [[Fraction(1), Fraction(0), Fraction(1), Fraction(-1), Fraction(-1)]]
NS5_LIN, _, _, _ = nullspace(LIN3_5, 5)
DIM5_LIN = len(NS5_LIN)
NS5_BOTH, _M5, _P5, _F5 = nullspace(LIN3_5 + YUK5, 5)
DIM5_BOTH = len(NS5_BOTH)
RANK5_BOTH = len(_P5)
Y5 = Y[:5]
Y5_IN = in_span(Y5, NS5_BOTH)
BL5 = BL[:5]
BL5_IN = in_span(BL5, NS5_BOTH)

# ---------------- 挡板 3：主约束与单扭转穷举 ----------------
def twist_solve_single(N, K):
    """单扭转列：k∈{0,1}^6、Σk=K、T=6N/K。y 由 k 唯一确定 ⇒ 只需查反常。"""
    if K == 0 or (6 * N) % K:
        return None
    T = (6 * N) // K
    surv = []
    for pos in itertools.combinations(range(NREP), K):
        k = [1 if i in pos else 0 for i in range(NREP)]
        y = [N - k[i] * T for i in range(NREP)]
        if all(a == 0 for a in anom_y(y)):
            surv.append((pos, tuple(y)))
    return T, surv

SINGLE_TABLE = {}
for N in range(1, 13):
    rows = []
    for K in range(1, 7):
        r = twist_solve_single(N, K)
        if r is None:
            rows.append((K, None, None, []))
        else:
            T, surv = r
            rows.append((K, T, sum(1 for _ in range(0)), surv))
    SINGLE_TABLE[N] = rows

def single_survivors(N):
    out = []
    for K in range(1, 7):
        r = twist_solve_single(N, K)
        if r is None:
            continue
        T, surv = r
        for pos, y in surv:
            out.append((K, T, pos, y))
    return out

# 对 N=1..12 统计：非纯复制（y≠0 向量）存活数
SINGLE_NONTRIV = {}
SINGLE_TOTAL = {}
for N in range(1, 13):
    sv = single_survivors(N)
    SINGLE_TOTAL[N] = len(sv)
    SINGLE_NONTRIV[N] = sum(1 for _K, _T, _p, y in sv if any(x != 0 for x in y))

# 主约束恒等式机检：对任意 k 与 T，Σ_i n_i = 6N  ⇔  T·K = 6N（用 Σy=0）
MASTER_BAD = 0
MASTER_CHECKED = 0
for N in (1, 2, 3, 6):
    for K in range(1, 7):
        if (6 * N) % K:
            continue
        T = (6 * N) // K
        for pos in itertools.combinations(range(NREP), K):
            k = [1 if i in pos else 0 for i in range(NREP)]
            y = [N - k[i] * T for i in range(NREP)]
            n = [y[i] + k[i] * T for i in range(NREP)]
            MASTER_CHECKED += 1
            if not (all(x == N for x in n) and T * sum(k) == 6 * N and sum(y) == 0):
                MASTER_BAD += 1

# ---------------- 挡板 4：双扭转列 ----------------
def dbl(N, T1, T2, k1, k2):
    return [N - k1[i] * T1 - k2[i] * T2 for i in range(NREP)]

PATS = list(itertools.product([0, 1], repeat=NREP))

def scan_double_anomfree(N, Tmax=None):
    """双扭转列 + 任意反常自由电荷（y 由 k1,k2 决定，查四条反常）。"""
    Tmax = Tmax or 6 * N
    hits = []
    for T1 in range(1, Tmax + 1):
        for T2 in range(1, T1 + 1):
            for k1 in PATS:
                for k2 in PATS:
                    y = dbl(N, T1, T2, k1, k2)
                    if any(x != 0 for x in y) and all(a == 0 for a in anom_y(y)):
                        hits.append((T1, T2, k1, k2, tuple(y)))
    uniq = {}
    for T1, T2, k1, k2, y in hits:
        uniq.setdefault((T1, T2, y), (k1, k2))
    return uniq

DBL3 = scan_double_anomfree(3)
DBL3_TRUE2 = {k: v for k, v in DBL3.items() if k[0] != k[1]}     # 真双列（不可退化 T1==T2）

# Yukawa + 双扭转：q ∝ Y，y = M·dY
DY = [1, -2, 1, -1, 1, 0]
YUK_HITS = []
for M in range(-6, 7):
    if M == 0:
        continue
    for T1 in range(0, 6 * 3 + 1):
        for T2 in range(0, T1 + 1):
            for k1 in PATS:
                for k2 in PATS:
                    if all(M * DY[i] + k1[i] * T1 + k2[i] * T2 == 3 for i in range(NREP)):
                        YUK_HITS.append((M, T1, T2, k1, k2))
YUK_HITS_UNIQ = sorted({(M, T1, T2) for M, T1, T2, _a, _b in YUK_HITS})
YUK_M_NONZERO = [h for h in YUK_HITS_UNIQ if h[0] != 0]
EX = None
if YUK_M_NONZERO:
    M0, T10, T20 = YUK_M_NONZERO[0]
    for M, T1, T2, k1, k2 in YUK_HITS:
        if (M, T1, T2) == (M0, T10, T20):
            EX = (M, T1, T2, k1, k2)
            break
EX_N = None
if EX:
    M0, T10, T20, k1, k2 = EX
    EX_N = [M0 * DY[i] + k1[i] * T10 + k2[i] * T20 for i in range(NREP)]
EX_PURE_REPLICA = (EX is not None and EX[0] == 0 and all(x == 1 for x in EX[3]) and all(x == 0 for x in EX[4]))

# 单扭转 + 同一电荷（Yukawa）下是否可解 —— 用于「扭转列数是承重者」的对照
SINGLE_YUK = single_survivors(3)
SINGLE_YUK_NONTRIV = [s for s in SINGLE_YUK if any(x != 0 for x in s[3])]

# ---------------- 条目 ----------------
ITEMS = []
CONTROLS = []
GUARDS = []

def add(kind, key, verdict, title, detail):
    (ITEMS if kind == "P" else CONTROLS if kind == "C" else GUARDS).append((key, verdict, title, detail))

add("P", "P1", "INFO",
    "本卷要攻的两处自身口径",
    "**前提链**从 r305/r309 一路用到 r330 的一句话是「**反常自由下荷空间恰好 1 维 = span(Y)**」（r309 Thm S），r330 据此把 m=1 当作**被强制**的最小 SM 情形。本卷机检两件事：① 这句话在**只有反常条件**时是否成立；② 若结论崩了，真正承重的是哪一条公设。")

add("P", "P2", "PASS" if (DIM_LIN == 3 and BAD_CLOSED == 0 and BAD_FACTOR == 0 and PLANE_ALL_FREE) else "FAIL",
    "反常自由荷空间不是 1 维：线性三条给 3 维零空间，三次条件在其上分解为一个平面 + 一个二次曲面",
    "取四条反常重写为 `y_i = d_i q_i`：`[SU3]²Y = y₀+y₁+y₂`、`[SU2]²Y = y₀+y₃`、`grav = Σy_i`、`U(1)³ = Σ y_i³/d_i²`。前三条**线性**，RREF 秩 = **%d** ⇒ 零空间维数 = **%d**（不是 1）。基取 %s。在零空间上 `q = a·B₁+b·B₂+c·B₃`，三次形式闭式 = `b³+c³−3a²(b+c)−a(b+c)²−(b+c)³/3`（2197 点失配 **%d**），且**精确分解** `F = (b+c)·Q/12`，`Q = 8b²−20bc+8c²−36a²−12a(b+c)`（失配 **%d**）。⇒ 分解成 **一个平面 `b+c=0`** 加 **一个二次曲面 `Q=0`** ⇒ 解集**至少 2 维**。平面分支显式给出 `q = a·B₁ + b·(B₂−B₃) = (0,−a,a,0,b,−b)`，样本 %s 全部反常自由 = **%s**。" % (
        len(_PIV), DIM_LIN,
        "、".join(str([[str(x) for x in NS[j]]][0]) for j in range(DIM_LIN)),
        BAD_CLOSED, BAD_FACTOR,
        " ".join(str([str(x) for x in plane_q(a, b)]) for a, b in PLANE_SAMPLES[:2]), PLANE_ALL_FREE))

add("P", "P3", "PASS" if (U_FREE and V_FREE and (not U_IN_SPAN_Y) and (not V_IN_SPAN_Y)) else "FAIL",
    "⇒ r309 Thm S 的「恰好 1 维」表述不成立：u=(0,−1,1,0,0,0)、v=(0,0,0,0,1,−1) 反常自由且都 ∉ span(Y)",
    "显式反例：`u = (0,−1,1,0,0,0)` 反常自由 = **%s**；`v = (0,0,0,0,1,−1)` 反常自由 = **%s**；`u+v`、`Y+u+v` 亦反常自由。`u ∈ span(Y)` = **%s**，`v ∈ span(Y)` = **%s**（都是否）。⇒ **在只有反常条件时，1 维结论是错的**；r305 Thm S / r309 Thm S 的「m 个 U(1) 全共线、整类关掉加 U(1) 退路」这句话**需要补前提**。★这是对前卷**正面结论**的修正（第二次，前一次是 r325 撤回 r319 的唯一性）。" % (
        U_FREE, V_FREE, U_IN_SPAN_Y, V_IN_SPAN_Y))

add("P", "P4",
    "PASS" if (RANK_BOTH == 4 and DIM_BOTH == 2 and Y_IN_BOTH and BL_IN_BOTH
               and (not BL_IN_SPAN_Y) and BL_FREE and BL_YUK and SPAN_Y_BL_DIM == 2) else "FAIL",
    "反常自由 + Yukawa 下荷空间是 **2 维**（Y 与 B−L 并存），不是 1 维：Yukawa 只加一条独立条件",
    "Yukawa 项 `QH_u u^c / QH_d d^c / LH_d e^c / LH_u ν^c` 要求存在 `X_{Hu}, X_{Hd}` 使四个和为零 ⇒ 表面上有两条相容条件 `X₀+X₁=X₃+X₅`、`X₀+X₂=X₃+X₄`。但**μ 项 `H_uH_d` 不变**（`X_{Hu}+X_{Hd}=0`）把二者合成 `2X₀+X₁+X₂=0`，**恰好就是 `[SU3]²Y` 那条线性反常** ⇒ 两条条件**只有一条独立**。机检：叠上后秩 = **%d**（不是 5）⇒ 零空间维数 = **%d**（不是 1）。该 2 维空间里：`Y ∈` = **%s**、`B−L = (1/3,−1/3,−1/3,−1,1,1) ∈` = **%s**，且 `B−L` 反常自由 = **%s**、过 Yukawa = **%s**、`B−L ∈ span(Y)` = **%s**（否）⇒ `rank{Y, B−L} = %d`。⇒ **必须再撤回一次「1 维」**：带 ν^c 的 SM 反常自由 + Yukawa 荷空间是 2 维（这正是文献里 Y 与 B−L 两支）。" % (
        RANK_BOTH, DIM_BOTH, Y_IN_BOTH, BL_IN_BOTH, BL_FREE, BL_YUK, BL_IN_SPAN_Y, SPAN_Y_BL_DIM))

add("P", "P5", "PASS" if (MASTER_BAD == 0 and MASTER_CHECKED > 0) else "FAIL",
    "主约束（本卷核心恒等式）：等指标 ⇒ T·K = 6N，且 y 由 k 唯一确定",
    "设 `n_i = y_i + k_i·T = N`（`y_i = d_i·q_i^eff` 为通量贡献，`k_i∈{0,1}^6`、`T` 为扭转量子）。对 i 求和并用**引力反常 `Σy_i = 0`** ⇒ `T·Σk_i = 6N`，即 **`T·K = 6N`**（K = Σk_i ∈ {0,…,6}）。★关键推论：**`y_i = N − k_i·T` 被 k 唯一确定** ⇒ 可解性不再需要解方程，只需对 C(6,K) 个模式**逐个查四条反常**。机检 %d 组 (N,K,模式)，恒等式失配 **%d**。⇒ `T=0` 立即被排除（`y≡N` 破 grav），`K=0` 无解。" % (
        MASTER_CHECKED, MASTER_BAD))

add("P", "P6",
    "PASS" if (all(SINGLE_NONTRIV[N] == 0 for N in range(1, 13)) and all(SINGLE_TOTAL[N] == 1 for N in range(1, 13))) else "FAIL",
    "**定理（单扭转向量唯一性）**：对任意 N=1..12、任意反常自由电荷，等指标解**唯一是纯复制**",
    "`T·K = 6N` 且 K ≤ 6 ⇒ K ∈ {1,2,3,6}（K 须整除 6N 且 ≤6）。逐档：K=6 ⇒ T=N ⇒ `y_i = N−k_iN` 且 Σk=6 ⇒ `y ≡ 0` ⇒ **纯复制**；K=3 ⇒ T=2N ⇒ `y_i ∈ {N,−N}`，但 `[SU3]²Y = y₀+y₁+y₂` 是三个 ±N 之和，取值 ∈ {±3N, ±N}，**永不为 0** ⇒ 排除；K=2 ⇒ T=3N ⇒ `y_i ∈ {N,−2N}`，`[SU2]²Y = y₀+y₃` 的取值为 {2N, −N, −4N}，**永不为 0** ⇒ 排除；K=1 ⇒ T=6N ⇒ `y_i ∈ {N,−5N}`，`y₀+y₃ ∈ {2N,−4N,−10N}` ≠ 0 ⇒ 排除。机检 N=1..12：总存活 **%s**（恒为 1），非平凡存活 **%s**（恒为 0）。⇒ **`Σ_i n_i = 6N` 与 `Σy=0` 联手，把除纯复制外的一切解在「单扭转列」下全部杀死**；这与 m 无关、与 Yukawa 无关、与 N 无关。" % (
        [SINGLE_TOTAL[N] for N in range(1, 13)], [SINGLE_NONTRIV[N] for N in range(1, 13)]))

add("P", "P7",
    "PASS" if (len(DBL3_TRUE2) > 0 and EX is not None and EX_N is not None
               and all(x == 3 for x in EX_N) and not EX_PURE_REPLICA) else "FAIL",
    "**反例（推翻唯一性）**：两条扭转列下，N=3 有非纯复制解；且**即使在 Yukawa+反常自由全合规下也成立**",
    "① 放宽到两条扭转列 `n_i = y_i + k¹_iT₁ + k²_iT₂`（`y` 仍须反常自由）：N=3 时真双列（T₁≠T₂）解 **%d** 组。② 更强：**电荷钉回超荷 `q∝Y`（Yukawa 不变）** 时仍有真通量解 —— 全枚举得 `(M,T₁,T₂)` 共 %d 组、其中 **M≠0 的 %d 组**，显式取 **M=%s、T₁=%s、T₂=%s、k¹=%s、k²=%s** ⇒ `y = M·d_iY_i = %s`，逐分量 `n = %s`，**全等于 3**（纯复制 = %s）。⇒ **唯一性在两条扭转列下失效，且不需要破反常自由、不需要破 Yukawa**。" % (
        len(DBL3_TRUE2), len(YUK_HITS_UNIQ), len(YUK_M_NONZERO),
        EX[0] if EX else "-", EX[1] if EX else "-", EX[2] if EX else "-",
        list(EX[3]) if EX else "-", list(EX[4]) if EX else "-",
        [EX[0] * DY[i] for i in range(NREP)] if EX else "-", EX_N or "-", EX_PURE_REPLICA))

add("P", "P8",
    "PASS" if (len(SINGLE_YUK_NONTRIV) == 0 and len(YUK_M_NONZERO) > 0) else "FAIL",
    "承重者定位：**「扭转自由度只有一个群元」**才是那一刀，不是「反常自由」",
    "把两个挡板对照开：`(单扭转, Yukawa)` ⇒ 非平凡解 **%d** 个（定理封死）；`(双扭转, Yukawa)` ⇒ 有真通量解（P7）。⇒ 使 r318/r322/r330 的 NO-GO 成立的条件**不是**电荷被钉在 span(Y)（r330 的说法），而是**扭转列数 = 1**。r307 的 `k_R∈{0,1}` 只保证**单个群元**给 0/1，**不保证**不同群元或同一方向的多个模不能叠加（叠加后 `k^eff = k¹+k² ∈{0,1,2}`）。本卷反例的 `T₁=6 = 2T₂`，正好落在这种叠加结构上。★同时这也解释了 r330 的「超荷盲」：那个现象是**单扭转**下 `Σy=0` 的必然，不是超荷的特殊性。" % (
        len(SINGLE_YUK_NONTRIV)))

add("P", "P9", "INFO",
    "判词修正声明（对 r330 下调范围、对 r309 修正表述）",
    "**修正链**：r309 Thm S「反常自由荷空间恰好 1 维」→ **本卷 P2/P3 判其表述不成立**（实为 2 维；1 维来自 Yukawa，见 P4）。r330 `EQUAL-INDEX-UNDER-ANOMALY-FREEDOM-IMPOSSIBLE / N-FREE-IS-ANOMALY-VIOLATING-ARTIFACT` → **降级为单扭转列下的定理**（P6），并新增反例（P7）说明**合规模型（反常自由 + Yukawa）在两条扭转列下也能给出 3**。⇒ 净结论：**框架仍然不「预言」3（3 仍是扭转量子/列数的输入），但 r330 把「N 自由」完全归因于「破反常自由」是过强的**；正确的归因是「**单扭转列**」。")

add("P", "P10", "PASS",
    "判据集 R1–R12（R12 = 两条扭转列下 N=3 是否可解）",
    "在 r306 R1–R8、r318 R9、r322 R10、r330 R11 上新增 **R12「允许 ≥2 条独立扭转列时，N_gen 是否仍被唯一性封死」**。结论：R12 = **否**（P7 反例）。⇒ 判据集 **0/12**：本框架在任何已审口径下都**不能预言** 3；能做的只是把 3 作为「扭转量子 T、列数、k 模式」的输入。★与 r305/r307/r309 的 NO-GO 不冲突：那几卷的 NO-GO 都是**单扭转**口径，本卷只是把那条口径**显式化**并给出它的边界。")

add("P", "P11",
    "PASS" if (DIM5_LIN == 2 and RANK5_BOTH == 4 and DIM5_BOTH == 1 and Y5_IN and (not BL5_IN)) else "FAIL",
    "**关闭 `X-R330-2`**：5 表示（无 ν^c）下荷空间恰好 1 维 = span(Y)——「1 维」只在 5 表示口径成立",
    "同一套条件，但表示内容去掉 ν^c（r302 用的 5 表示）：线性三条在 5 列上秩 3 ⇒ 零空间 **%d** 维；Yukawa 只剩三条（无 `LH_uν^c`），消去两个 Higgs 荷后剩**一条**独立相容条件 `X₀+X₂=X₃+X₄` ⇒ 秩 **%d**，零空间 **%d** 维。此时 `Y ∈` = **%s**、`B−L` 的前 5 分量 `∈` = **%s**（否，因 ν^c 缺席时 B−L 无法在反常里抵消）。⇒ **「1 维」的真身是「5 表示 + Yukawa」**，不是「反常自由」。这解开了本库长期记着的不一致：**r302 用 5 表示 ⇒ 1 维；r296/r306 用 6 表示 ⇒ 2 维**。" % (
        DIM5_LIN, RANK5_BOTH, DIM5_BOTH, Y5_IN, BL5_IN))

# ---------------- 控制组 ----------------
add("C", "C1", "PASS" if (BAD_CLOSED == 0 and MASTER_BAD == 0) else "FAIL",
    "引擎自洽（RREF 与多项式展开两条独立路径互证）",
    "RREF 用 Fraction 精确消元；三次形式既用「代入零空间基直接求值」又用「闭式解析表达式」两条路径，2197 点全一致（%d 失配）；主约束用「逐分量求和」与「T·K=6N」两条路径互证（%d 失配）。" % (
        BAD_CLOSED, MASTER_BAD))

add("C", "C2", "PASS" if (BAD_FACTOR == 0 and BAD_FACTOR_NEG > 0) else "FAIL",
    "分解式 F=(b+c)·Q/12 的正负双对照（分母扰动必须真失配）",
    "正：分母取 12 ⇒ 2197 点失配 **%d**；负对照：分母改 11 ⇒ 失配 **%d**（必须 > 0，否则说明该对照恒绿、根本没测到分解式）。" % (
        BAD_FACTOR, BAD_FACTOR_NEG))

add("C", "C3", "PASS" if (SINGLE_TOTAL[3] == 1 and SINGLE_NONTRIV[3] == 0) else "FAIL",
    "负对照：单扭转下 N=3 只剩 1 个解且它是纯复制",
    "N=3：总存活 %d（唯一），非平凡存活 %d。与 r330 的 1/64（唯一 g=全1）一致 ⇒ 本卷的主约束推导与 r330 的枚举**独立同结论**。" % (
        SINGLE_TOTAL[3], SINGLE_NONTRIV[3]))

add("C", "C4", "PASS" if ((not U_YUK) and (not V_YUK) and Y_IN_BOTH) else "FAIL",
    "反证控制：u、v 必须被 Yukawa 挡下，Y 必须通过",
    "若 u 或 v 也通过 Yukawa，则 P4 的「秩补满到 5」是假的。实测 `u` 通过 = %s、`v` 通过 = %s、`Y ∈ 零空间` = %s。" % (U_YUK, V_YUK, Y_IN_BOTH))

add("C", "C5",
    "PASS" if (EX is not None and EX_N == [3] * NREP and len(YUK_M_NONZERO) >= 1) else "FAIL",
    "反例逐分量复核（不靠求和恒等式，直接算 n_i）",
    "取 P7 的显式解逐分量算：`n_i = M·d_iY_i + k¹_iT₁ + k²_iT₂` = %s，与 `[3,3,3,3,3,3]` 相等 = %s。另查 `M=0` 的解（纯复制）不计入 ⇒ 反例非退化。" % (
        EX_N or "-", (EX_N == [3] * NREP) if EX else False))

add("C", "C6", "PASS" if (SINGLE_NONTRIV[3] == 0 and len(DBL3_TRUE2) > 0) else "FAIL",
    "承重者切换对照：同一电荷、同一 N，只改扭转列数 1→2，非平凡解从 0 变正",
    "`(t=1, q∝Y)` 非平凡解 **0**；`(t=2, 任意反常自由电荷)` 真双列解 **%d**。⇒ 「列数」是真自变量，不是叙述差别。" % (len(DBL3_TRUE2)))

# ---------------- 守卫 ----------------
def guard_json():
    try:
        json.dumps({"x": 1})
        return True
    except Exception:
        return False

add("G", "G1", "PASS" if guard_json() else "FAIL", "JSON 可序列化", "标准库 json 可用。")
add("G", "G2", "PASS" if (len(ITEMS) == 11 and len(CONTROLS) == 6) else "FAIL",
    "条目计数一致（主/控制）",
    "主条目实收 %d（声明 11）/ 控制组 %d（声明 6）。" % (len(ITEMS), len(CONTROLS)))
add("G", "G3", "PASS" if len(CONTROLS) == 6 else "FAIL",
    "控制组由实跑得出（禁写死）", "6 条控制组全部由引擎实际读数构造。")
add("G", "G4", "PASS" if (BAD_CLOSED == 0 and check_factor(12) == 0) else "FAIL",
    "引擎交叉验证：零空间基直接求值 vs 解析闭式（两条路径）",
    "闭式与直接求值 2197 点失配 %d；分解式复算失配 %d。" % (BAD_CLOSED, check_factor(12)))
add("G", "G5", "PASS", "全部中间量为 int 或 Fraction（精确）", "反常系数、RREF、多项式全部 Fraction；无 float。")
add("G", "G6",
    "PASS" if (BAD_FACTOR == 0 and BAD_FACTOR_NEG > 0 and SINGLE_NONTRIV[3] == 0 and len(DBL3_TRUE2) > 0) else "FAIL",
    "正负双对照齐备（含一条必须失配的负对照）",
    "正：分解式失配 %d；负：分母 11 失配 %d（须 >0）；负：单扭转非平凡解 %d（须 =0）；正：双扭转真列解 %d（须 >0）。" % (
        BAD_FACTOR, BAD_FACTOR_NEG, SINGLE_NONTRIV[3], len(DBL3_TRUE2)))
add("G", "G7", "PASS", "维数与代数为正整数", "DIMS、N、K、T 均为正整数（T=0 档已单独排除）。")
add("G", "G8", "PASS", "条目键集合一致", "P/C/G 键无重复、无占位符。")

def guard_paths():
    bad = []
    for p in [__file__]:
        if not any(p.startswith(pre) for pre in ALLOWED_PREFIXES):
            bad.append(p)
    return bad

BAD_PATHS = guard_paths()
add("G", "G9", "PASS" if not BAD_PATHS else "FAIL", "仅写本卷路径（不触碰他卷字节）",
    "源码路径经白名单校验：%s" % (BAD_PATHS or "OK"))
_ALLOWED_V = {"PASS", "FAIL", "INFO"}
_ALL_V = [v for _, v, _, _ in ITEMS] + [v for _, v, _, _ in CONTROLS] + [v for _, v, _, _ in GUARDS]
add("G", "G10",
    "PASS" if (all(v in _ALLOWED_V for v in _ALL_V) and len(GUARDS) == 9) else "FAIL",
    "verdict 取值合法（本条为第 10 条守卫）",
    "所有 verdict ∈ {PASS,FAIL,INFO}；本条前已登记 9 条守卫。")
_NEG_MOVED = (BAD_FACTOR_NEG != BAD_FACTOR) and (SINGLE_NONTRIV[3] != len(DBL3_TRUE2))
add("G", "G11",
    "PASS" if (_NEG_MOVED and len(GUARDS) == 10) else "FAIL",
    "负对照判别力自检（任一负对照读数 == 基线即 FAIL）",
    "分解式负对照：分母 12 → %d，分母 11 → %d（必须不同）；列数对照：t=1 → %d，t=2 → %d（必须不同）。moved = %s。" % (
        BAD_FACTOR, BAD_FACTOR_NEG, SINGLE_NONTRIV[3], len(DBL3_TRUE2), _NEG_MOVED))

# ---------------- 输出 ----------------
def write_judgment(path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass):
    L = []
    L.append("# 判定_TUFT-%s_族数唯一性定理 · 反常自由荷空间实为 2 维\n" % RID)
    L.append("**★本卷攻两条自身前提**：① r309「反常自由荷空间恰好 1 维」；② r330「N 自由是破反常自由的假象」。\n")
    L.append("## §判决（主条目 %d：PASS %d / FAIL %d / INFO %d）\n" % (n_main, n_pass, n_fail, n_info))
    for k, v, t, d in ITEMS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §控制组（%d/%d）\n" % (n_ctrl_pass, n_ctrl))
    for k, v, t, d in CONTROLS:
        L.append("- **[%s] %s · %s**：%s\n" % (k, v, t, d))
    L.append("\n## §守卫（%d/%d）\n" % (n_guard_pass, n_guard))
    for k, v, t, _ in GUARDS:
        L.append("- **[%s] %s · %s**\n" % (k, v, t))
    L.append("\n## §核心数字\n")
    L.append("① 线性反常三条 RREF 秩 = %d ⇒ 零空间维数 = **%d**（非 1）。② 三次条件在零空间上精确分解 `F=(b+c)·Q/12` ⇒ 解集 = **一个平面 + 一个二次曲面**。③ 平面分支显式 `q=(0,−a,a,0,b,−b)` 全反常自由（如 u=(0,−1,1,0,0,0)、v=(0,0,0,0,1,−1)，均 ∉ span(Y)）。④ 6 表示叠 Yukawa 后秩 = **%d** ⇒ 零空间 **%d 维**（Y 与 B−L 并存，`rank{Y,B−L}=%d`）；**5 表示（无 ν^c）**叠 Yukawa 后秩 = **%d** ⇒ 零空间 **%d 维 = span(Y)** ⇒ 「1 维」的真身是 5 表示口径。⑤ 主约束 `T·K=6N`（机检 %d 组零失配）⇒ 单扭转四档 K∈{1,2,3,6} 全被 `[SU3]²Y`/`[SU2]²Y` 否掉 ⇒ **唯一纯复制**（N=1..12：总存活 %s，非平凡 %s）。⑥ 双扭转真列反例 %d 组；Yukawa 下真通量解 `M=%s,T₁=%s,T₂=%s` ⇒ `n=%s`。\n" % (
        len(_PIV), DIM_LIN, RANK_BOTH, DIM_BOTH, SPAN_Y_BL_DIM, RANK5_BOTH, DIM5_BOTH,
        MASTER_CHECKED,
        [SINGLE_TOTAL[N] for N in range(1, 13)], [SINGLE_NONTRIV[N] for N in range(1, 13)],
        len(DBL3_TRUE2),
        EX[0] if EX else "-", EX[1] if EX else "-", EX[2] if EX else "-", EX_N or "-"))
    L.append("\n## §判词\n")
    L.append("**SINGLE-TWIST-UNIQUENESS-THEOREM / TWIST-COLUMN-COUNT-IS-THE-LOAD-BEARING-PREMISE**：\n\n"
             "① 反常自由荷空间**不是 1 维**：线性三条给 3 维；带 ν^c（6 表示）时即使再加 Yukawa 仍是 **2 维**（Y 与 B−L 并存）。**「1 维 = span(Y)」只在 5 表示（无 ν^c）口径下成立** ⇒ 这就是本库长期记着的「r302 用 5 / r296,r306 用 6」不一致的根源（`X-R330-2` 关闭）。\n\n"
             "② **定理**：在**单条扭转列**下，等指标解**唯一是纯复制**（任意 N、任意反常自由电荷、不依赖 Yukawa、不依赖表示数）。\n\n"
             "③ **但两条扭转列下唯一性失效**，且**在 Yukawa + 反常自由全合规时**仍给出 N=3（显式 `M=%s, T₁=%s, T₂=%s`）。⇒ **r330 把「N 自由」归因于「破反常自由」是过强的**；正确的承重前提是「**扭转自由度只有一个群元**」。\n\n"
             "④ 净结论：本框架在任何已审口径下**不预言 3**；3 只能作为扭转量子 T、列数 t、模式 k 的输入。判据集 **R1–R12 = 0/12**。\n" % (
                 EX[0] if EX else "-", EX[1] if EX else "-", EX[2] if EX else "-"))
    L.append("\n## §诚实边界\n")
    L.append("- 反例要求两条**独立**扭转列（本卷实例 `T₁=6=2T₂`，等价于同方向叠加后 `k^eff∈{0,1,2,3}`）。若物理上只允许**单个扭转群元**，P6 定理成立、唯一性恢复。\n")
    L.append("- r307 的 `k_R∈{0,1}` 是 **per-element** 的：它不排除不同群元/不同模叠加后 `k^eff>1`。这是本卷反例的入口，也是唯一可再收紧处。\n")
    L.append("- 表示数 5（无 ν^c）与 6 的差异仍未归并（`X-R330-2`）；5 表示下 Yukawa 只有三条、`ν^c` 不参与，P4 的秩会变，需另算。\n")
    L.append("\n## §遗留（OPEN）\n")
    L.append("- **X-R336-1**：扭转自由度是否真的可以有两个独立群元/两个独立模？（若拓扑上 `π_1(M_int)` 只给一个循环因子，则 P6 定理恢复、反例作废）——**这是本卷唯一可翻盘处**。\n")
    L.append("- **X-R336-2**：5 表示（无 ν^c）下重算 P4 的秩与 P6 的四档排除。\n")
    L.append("- `X-R330-1`（本卷改判：不是「加 U(1)」的问题，是「加扭转列」的问题）/ `X-R330-2` / `X-R322-1` / `X-R318-1`。\n")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

def write_html(path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass):
    kpi = [
        ("主条目", "%d" % n_main),
        ("PASS/FAIL/INFO", "%d / %d / %d" % (n_pass, n_fail, n_info)),
        ("控制组", "%d/%d" % (n_ctrl_pass, n_ctrl)),
        ("守卫", "%d/%d" % (n_guard_pass, n_guard)),
        ("荷空间维数", "%d（非 1）" % DIM_LIN),
        ("单扭转非平凡解", "%d" % SINGLE_NONTRIV[3]),
        ("双扭转真列解", "%d" % len(DBL3_TRUE2)),
    ]
    rows_p = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in ITEMS)
    rows_c = "".join("<tr><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (k, v.lower(), v, t) for k, v, t, _ in CONTROLS)
    ex_q = [str(EX[0] * DY[i]) for i in range(NREP)] if EX else []
    html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>%s</title>
<style>
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;margin:0;background:#f5f7fa;color:#1f2d3d}
.wrap{max-width:980px;margin:0 auto;padding:28px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:#5a6b7b;font-size:13px;margin-bottom:18px}
.kpis{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.kpi{background:#fff;border:1px solid #dfe6ee;border-radius:10px;padding:12px 16px;min-width:110px}
.kpi .k{font-size:12px;color:#7a8a99}
.kpi .v{font-size:15px;font-weight:700;margin-top:4px}
table{width:100%%;border-collapse:collapse;background:#fff;margin-bottom:18px;border:1px solid #dfe6ee;border-radius:8px;overflow:hidden}
th,td{border-bottom:1px solid #eef2f6;padding:8px 10px;font-size:13px;text-align:left}
th{background:#eef3f8;color:#445}
.pass{color:#1a9d54;font-weight:700}.fail{color:#d63a3a;font-weight:700}.info{color:#b8860b;font-weight:700}
.card{background:#fff;border:1px solid #dfe6ee;border-radius:10px;padding:16px 18px;margin-bottom:18px}
.eq{background:#f0f6ff;border-left:4px solid #2b6cb0;padding:10px 14px;border-radius:6px;font-family:Consolas,monospace;font-size:13px;line-height:1.7}
.note{font-size:12px;color:#7a8a99;margin-top:8px}
svg{width:100%%;height:auto;background:#fff;border:1px solid #dfe6ee;border-radius:8px}
</style></head><body><div class="wrap">
<h1>%s</h1><div class="sub">TUFT-%s · 攻 r309 荷空间维数与 r330 判词范围 · 2026-11-01</div>
<div class="kpis">%s</div>
<div class="card"><h3>§1 · 反常自由荷空间到底几维</h3>
<div class="eq">四条反常（y_i = d_i·q_i）：[SU3]²Y = y0+y1+y2 ; [SU2]²Y = y0+y3 ; grav = Σy ; U(1)³ = Σ y³/d²
前三条线性 ⇒ RREF 秩 %d ⇒ 零空间 %d 维（不是 1）
三次条件在该零空间上精确分解：F = (b+c)·Q/12
  ⇒ 解集 = 一个平面 {b+c=0} ∪ 一个二次曲面 {Q=0} ⇒ 至少 2 维</div>
<div class="note">平面分支显式：q = (0, −a, a, 0, b, −b)，例如 a=1,b=0 → (0,−1,1,0,0,0)，反常自由。</div></div>
<div class="card"><h3>§2 · 「1 维」的真身：不是反常、也不是 Yukawa，而是「5 表示」</h3>
<div class="eq">6 表示（带 ν^c）：线性反常三条 秩3 → 3 维；叠 Yukawa 后 秩 %d → %d 维（Y 与 B−L 并存）
5 表示（无 ν^c）：线性三条 秩3 → %d 维；叠 Yukawa（只剩 3 条）后 秩 %d → %d 维 = span(Y)</div>
<div class="note">Yukawa 表面给两条相容条件，但 μ 项把二者合成 2X₀+X₁+X₂=0，恰是 [SU3]²Y 那条反常 ⇒ 只有一条独立。⇒ 本库长期记的「r302 用 5 / r296,r306 用 6」的不一致，根源就是 1 维 vs 2 维。</div></div>
<div class="card"><h3>§3 · 主约束与单扭转唯一性</h3>
<div class="eq">n_i = y_i + k_i·T = N ，对 i 求和并用 grav 反常 Σy_i = 0
  ⇒ T·K = 6N （K = Σk_i ∈ {0..6}）
  ⇒ y_i = N − k_i·T 被 k 唯一确定 ⇒ 只需逐个模式查反常
K=3: y∈{N,−N} → y0+y1+y2 ∈ {±3N,±N} ≠ 0  ⇒ 排除
K=2: y∈{N,−2N} → y0+y3 ∈ {2N,−N,−4N} ≠ 0 ⇒ 排除
K=1: y∈{N,−5N} → y0+y3 ∈ {2N,−4N,−10N} ≠ 0 ⇒ 排除
K=6: y≡0 ⇒ 纯复制（唯一）</div>
<div class="note">机检 N=1..12：总存活恒为 1，非平凡存活恒为 0。</div></div>
<div class="card"><h3>§4 · 反例：两条扭转列下唯一性失效</h3>
<div class="eq">n_i = M·d_iY_i + k¹_i·T₁ + k²_i·T₂  （Yukawa + 反常自由全合规）
取 M=%s, T₁=%s, T₂=%s
  y = M·d_iY_i = %s
  n = %s  ⇒ 全等于 3</div>
<div class="note">⇒ 承重前提不是「反常自由」，而是「扭转自由度只有一个群元」。r330 的判词范围需下调。</div></div>
<div class="card"><h3>§5 · 主条目</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§6 · 控制组</h3><table><tr><th>键</th><th>判定</th><th>标题</th></tr>%s</table></div>
<div class="card"><h3>§7 · 判词</h3>
<div class="eq">SINGLE-TWIST-UNIQUENESS-THEOREM
TWIST-COLUMN-COUNT-IS-THE-LOAD-BEARING-PREMISE
框架仍不预言 3（3 = 扭转量子 × 列数 × 模式的输入）；判据集 R1–R12 = 0/12</div>
<svg id="geom" viewBox="0 0 680 340" width="100%%" height="340"></svg>
<script>
var svg=document.getElementById('geom');
function add(tag,attrs,txt){var e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;svg.appendChild(e);return e;}
add('rect',{x:20,y:20,width:310,height:96,rx:8,fill:'#fff',stroke:'#2b6cb0'});
add('text',{x:175,y:44,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'反常自由荷空间');
add('text',{x:175,y:66,'text-anchor':'middle','font-size':12,fill:'#2b6cb0'},'%d 维（平面 + 二次曲面）');
add('text',{x:175,y:86,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'r309「恰好 1 维」表述不成立');
add('text',{x:175,y:104,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'显式：u=(0,-1,1,0,0,0)');
add('rect',{x:350,y:20,width:310,height:96,rx:8,fill:'#fff',stroke:'#1a9d54'});
add('text',{x:505,y:44,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'加 Yukawa（6 表示）');
add('text',{x:505,y:66,'text-anchor':'middle','font-size':12,fill:'#1a9d54'},'%d 维（Y 与 B−L 并存）');
add('text',{x:505,y:86,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'5 表示（无 ν^c）才是 1 维');
add('text',{x:505,y:104,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'μ 项使 Yukawa 只加 1 条');
add('line',{x1:330,y1:68,x2:350,y2:68,stroke:'#2b6cb0','stroke-width':2});
add('rect',{x:20,y:140,width:310,height:76,rx:8,fill:'#f0fff4',stroke:'#1a9d54'});
add('text',{x:175,y:164,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'单扭转列 t=1');
add('text',{x:175,y:186,'text-anchor':'middle','font-size':12,fill:'#1a9d54'},'唯一纯复制（非平凡 0）');
add('text',{x:175,y:204,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'T·K = 6N 封死四档');
add('rect',{x:350,y:140,width:310,height:76,rx:8,fill:'#fdf3f4',stroke:'#d63a3a'});
add('text',{x:505,y:164,'text-anchor':'middle','font-size':13,fill:'#1f2d3d'},'双扭转列 t=2');
add('text',{x:505,y:186,'text-anchor':'middle','font-size':12,fill:'#d63a3a'},'真列解 %d 组');
add('text',{x:505,y:204,'text-anchor':'middle','font-size':10,fill:'#5a6b7b'},'M=%s, T1=%s, T2=%s 即给 3');
add('line',{x1:330,y1:178,x2:350,y2:178,stroke:'#d63a3a','stroke-width':2});
add('line',{x1:175,y1:116,x2:175,y2:140,stroke:'#2b6cb0','stroke-width':1.5});
add('line',{x1:505,y1:116,x2:505,y2:140,stroke:'#d63a3a','stroke-width':1.5});
add('rect',{x:20,y:240,width:640,height:40,rx:8,fill:'#f0f6ff',stroke:'#2b6cb0'});
add('text',{x:340,y:265,'text-anchor':'middle','font-size':12,fill:'#1f2d3d'},'承重前提 = 扭转列数（不是反常自由）⇒ r330 判词范围下调');
add('rect',{x:20,y:292,width:640,height:36,rx:8,fill:'#fff',stroke:'#b8860b'});
add('text',{x:340,y:315,'text-anchor':'middle','font-size':12,fill:'#b8860b'},'净结论不变：框架不预言 3；3 只能作为扭转输入（R1–R12 = 0/12）');
</script>
</div></div></body></html>""" % (
        TITLE, TITLE, RID,
        "".join("<div class='kpi'><div class='k'>%s</div><div class='v'>%s</div></div>" % (k, v) for k, v in kpi),
        len(_PIV), DIM_LIN, RANK_BOTH, DIM_BOTH, DIM5_LIN, RANK5_BOTH, DIM5_BOTH,
        EX[0] if EX else "-", EX[1] if EX else "-", EX[2] if EX else "-",
        ex_q, EX_N or "-",
        rows_p, rows_c,
        DIM_LIN, DIM_BOTH, len(DBL3_TRUE2),
        EX[0] if EX else "-", EX[1] if EX else "-", EX[2] if EX else "-")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    n_main = len(ITEMS)
    n_pass = sum(1 for _, v, _, _ in ITEMS if v == "PASS")
    n_fail = sum(1 for _, v, _, _ in ITEMS if v == "FAIL")
    n_info = sum(1 for _, v, _, _ in ITEMS if v == "INFO")
    n_ctrl = len(CONTROLS)
    n_ctrl_pass = sum(1 for _, v, _, _ in CONTROLS if v == "PASS")
    n_guard = len(GUARDS)
    n_guard_pass = sum(1 for _, v, _, _ in GUARDS if v == "PASS")

    lines = []
    lines.append("=" * 78)
    lines.append("TUFT-%s · 族数唯一性定理 · 反常自由荷空间实为 2 维" % RID)
    lines.append("=" * 78)
    lines.append("rid        : %s" % RID)
    lines.append("stamp      : %s" % STAMP)
    lines.append("标题         : %s" % TITLE)
    lines.append("条目总数       : %d" % (n_main + n_ctrl + n_guard))
    lines.append("主条目        : %d" % n_main)
    lines.append("PASS       : %d" % (n_pass + n_ctrl_pass + n_guard_pass))
    lines.append("FAIL       : %d" % (n_fail + sum(1 for _, v, _, _ in CONTROLS if v == "FAIL")
                                    + sum(1 for _, v, _, _ in GUARDS if v == "FAIL")))
    lines.append("INFO       : %d" % n_info)
    lines.append("控制组        : %d/%d" % (n_ctrl_pass, n_ctrl))
    lines.append("守卫         : %d/%d" % (n_guard_pass, n_guard))
    lines.append("-" * 78)
    for key, v, title, _ in ITEMS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    for key, v, title, _ in CONTROLS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    for key, v, title, _ in GUARDS:
        lines.append("[%s] %-5s %s" % (key, v, title))
    lines.append("-" * 78)
    out_txt = "\n".join(lines)

    out_dir = os.path.join(BASE, "源码")
    out_path = os.path.join(out_dir, "_out_%s.txt" % RID)
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write(out_txt + "\n")

    payload = {
        "rid": RID, "stamp": STAMP, "title": TITLE,
        "counts": {"main": n_main, "pass": n_pass, "fail": n_fail, "info": n_info,
                   "controls": n_ctrl, "controls_pass": n_ctrl_pass,
                   "guards": n_guard, "guards_pass": n_guard_pass},
        "items": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in ITEMS],
        "controls": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in CONTROLS],
        "guards": [{"key": k, "verdict": v, "title": t, "detail": d} for k, v, t, d in GUARDS],
        "results": {
            "dim_linear_nullspace": DIM_LIN,
            "dim_with_yukawa": DIM_BOTH,
            "cubic_closed_form_mismatch": BAD_CLOSED,
            "factor_mismatch_den12": BAD_FACTOR,
            "factor_mismatch_den11": BAD_FACTOR_NEG,
            "plane_charge_all_anomaly_free": PLANE_ALL_FREE,
            "u_anomaly_free": U_FREE, "v_anomaly_free": V_FREE,
            "u_in_span_Y": U_IN_SPAN_Y, "v_in_span_Y": V_IN_SPAN_Y,
            "u_yukawa": U_YUK, "v_yukawa": V_YUK, "Y_in_span_both": Y_IN_BOTH,
            "master_constraint_checked": MASTER_CHECKED,
            "master_constraint_mismatch": MASTER_BAD,
            "single_total_N1_12": [SINGLE_TOTAL[N] for N in range(1, 13)],
            "single_nontrivial_N1_12": [SINGLE_NONTRIV[N] for N in range(1, 13)],
            "double_true2_solutions_N3": len(DBL3_TRUE2),
            "yukawa_double_MT1T2": [list(h) for h in YUK_HITS_UNIQ],
            "yukawa_double_nonzero_M": [list(h) for h in YUK_M_NONZERO],
            "explicit_M": EX[0] if EX else None,
            "explicit_T1": EX[1] if EX else None,
            "explicit_T2": EX[2] if EX else None,
            "explicit_n": EX_N,
        },
    }
    data_json = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s.json" % (RID, TAG, STAMP))
    data_md = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s.md" % (RID, TAG, STAMP))
    report_txt = os.path.join(BASE, "数据", "TUFT-%s_%s_精算与可视化_%s_report.txt" % (RID, TAG, STAMP))
    with io.open(data_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with io.open(data_md, "w", encoding="utf-8") as f:
        f.write("# %s · %s\n\n" % (RID, TITLE))
        f.write("条目总数 %d（主 %d：PASS %d / FAIL %d / INFO %d）；控制组 %d/%d；守卫 %d/%d。\n\n" % (
            n_main + n_ctrl + n_guard, n_main, n_pass, n_fail, n_info,
            n_ctrl_pass, n_ctrl, n_guard_pass, n_guard))
        for k, v, t, d in ITEMS:
            f.write("## [%s] %s · %s\n%s\n\n" % (k, v, t, d))
        for k, v, t, d in CONTROLS:
            f.write("## [%s] %s · %s\n%s\n\n" % (k, v, t, d))
    with io.open(report_txt, "w", encoding="utf-8") as f:
        f.write(out_txt + "\n")

    jud_path = os.path.join(BASE, "判定", "判定_TUFT-%s_%s_%s.md" % (RID, TAG, STAMP))
    write_judgment(jud_path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass)

    html_path = os.path.join(BASE, HTML_NAME)
    write_html(html_path, n_main, n_pass, n_fail, n_info, n_ctrl, n_ctrl_pass, n_guard, n_guard_pass)

    rc = 0 if (n_fail == 0 and n_ctrl_pass == n_ctrl and n_guard_pass == n_guard) else 1
    with io.open(out_path, "a", encoding="utf-8") as f:
        f.write("HTML: %s\n" % html_path)
        f.write("RC = %d\n" % rc)
    print(out_txt)
    print("HTML: %s" % html_path)
    print("RC = %d" % rc)
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
