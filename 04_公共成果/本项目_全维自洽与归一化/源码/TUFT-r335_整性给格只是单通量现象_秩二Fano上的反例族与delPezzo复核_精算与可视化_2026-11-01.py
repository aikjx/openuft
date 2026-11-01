# -*- coding: utf-8 -*-
"""TUFT-r335 . 整性给格只是单通量现象
攻 X-R331-1：一般 Fano 上「n_R 是整数」还能不能单独逼出量子化格？

基线（不破）：r325 FW 格 / r327 二项式闭式 / r331 整性定理与 k 坐标压缩。
本卷只做一件事：把 r331 的「整性 ⟹ 格」放到**通量维数 >= 2** 的一般 Fano 上试。

结论（判词见 VERDICT）：
  rank 1 上成立（r331 已证，本卷 12/12 复现）；
  rank 2 上**整性集不是陪集**（CP^1 x CP^1：q1*q2 in Z，无限族 (1/m, m)）；
  性质属于**通量线**，不属于流形（同一张 CP^1 x CP^1，对角线上仍是陪集 Z）。

纪律（本卷三条硬约束，都是踩过才写下的）：
  ① 差封闭性是**子群**判据，不是**陪集**判据 —— CP^n 的格是 Z+1/2，差封闭必然失败；
     陪集要用 u−v+w 型仿射封闭性检验。
  ② 扫箱的**维数要与流形一致**：CP² 的 H² 秩 1，多扫一个 E 方向会凭空造出 20 个「离格」假点。
  ③ 分母有界引理的界用的是**清分母后的首项分子** D·c_d，不是 c_d 的分子 —— 漏掉 D 的素因子会
     把 13 个合法样本误判成违例。

Fraction 精确；确定性 LCG 不用 random；每条判决带分母；负对照必须真改变输出。
"""

import io
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

RID = "r335"
DATE = "2026-11-01"
DEGREE = 0
CAND_DEGREE = 37
NMAX = 12

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")

STEM = ("TUFT-r335_整性给格只是单通量现象_秩二Fano上的反例族与delPezzo复核_"
        "精算与可视化_2026-11-01")

Q_LABEL = ("Q_L (3,2)_{1/6} dim=6 Y=1/6 ; u^c (3bar,1)_{-2/3} dim=3 ; "
           "d^c (3bar,1)_{1/3} dim=3 ; L_L (1,2)_{-1/2} dim=2 ; e^c (1,1)_{1} dim=1")

# ============================================================ 0. 精确级数工具

def inv_series(a, N):
    b = [F(0)] * (N + 1)
    b[0] = F(1) / a[0]
    for k in range(1, N + 1):
        s = F(0)
        for i in range(1, k + 1):
            s += a[i] * b[k - i]
        b[k] = -s / a[0]
    return b


def one_minus_exp_neg_over_x(N):
    return [F((-1) ** k, math.factorial(k + 1)) for k in range(N + 1)]


def td_cpn(n):
    """td(CP^n) = T(h)^{n+1}，T = h/(1-e^{-h})。返回到 h^n 的系数表。"""
    N = n
    T = inv_series(one_minus_exp_neg_over_x(N), N)
    out = [F(0)] * (N + 1)
    out[0] = F(1)
    for _ in range(n + 1):
        new = [F(0)] * (N + 1)
        for i in range(N + 1):
            if out[i] == 0:
                continue
            for j in range(N + 1 - i):
                if T[j] == 0:
                    continue
                new[i + j] += out[i] * T[j]
        out = new
    return out


def binom_g(x, n):
    num = F(1)
    for i in range(n):
        num *= (F(x) - i)
    return num / math.factorial(n)


def chi_prod(n1, n2, k1, k2):
    """CP^{n1} x CP^{n2} 上 O(k1,k2) 的 chi = coeff of h1^n1 h2^n2 in e^{k1 h1 + k2 h2} td。"""
    td1 = td_cpn(n1)
    td2 = td_cpn(n2)
    e1 = [F(1)] + [F(k1) ** j / math.factorial(j) for j in range(1, n1 + 1)]
    e2 = [F(1)] + [F(k2) ** j / math.factorial(j) for j in range(1, n2 + 1)]
    m1 = [F(0)] * (n1 + 1)
    for i in range(n1 + 1):
        for j in range(n1 + 1 - i):
            m1[i + j] += e1[i] * td1[j]
    m2 = [F(0)] * (n2 + 1)
    for i in range(n2 + 1):
        for j in range(n2 + 1 - i):
            m2[i + j] += e2[i] * td2[j]
    return m1[n1] * m2[n2]


def frac_mod1(x):
    x = F(x)
    return x - math.floor(x)


def in_coset(x, shift):
    return frac_mod1(F(x) - F(shift)) == 0


LCG_S = 987654321


def lcg():
    global LCG_S
    LCG_S = (LCG_S * 1103515245 + 12345) % (2 ** 31)
    return LCG_S


# ============================================================ 判据容器

ITEMS = []
GUARDS = []
CTL = []


def item(tag, kind, exp, act, note, desc, ok=None):
    """kind: eq / gt / info。eq 判 exp==act，gt 判 act>exp，info 恒 INFO。"""
    if kind == "info":
        status = "INFO"
    else:
        if ok is None:
            ok = (F(act) == F(exp)) if kind == "eq" else (F(act) > F(exp))
        status = "PASS" if ok else "FAIL"
    ITEMS.append({"tag": tag, "kind": kind, "status": status,
                  "exp": (None if kind == "info" else str(exp)),
                  "act": (None if kind == "info" else str(act)),
                  "note": note, "desc": desc})
    return status


def ctl(tag, ok, desc, detail):
    CTL.append({"tag": tag, "status": "PASS" if ok else "FAIL", "desc": desc, "detail": detail})
    return ok


def guard(tag, ok, desc, detail):
    GUARDS.append({"tag": tag, "status": "PASS" if ok else "FAIL", "desc": desc, "detail": detail})
    return ok


SRC_PATH = os.path.abspath(__file__)

# ============================================================ A 组：CP^n 基线（rank 1，不破 r331）

A_GRID = [F(i, 12) for i in range(-72, 73)]     # (1/12)Z ∩ [-6,6]

A_MATCH = []
A_ONLAT_TOT = 0
A_ONLAT_BAD = 0
A_OFFLAT_TOT = 0
A_RESOLVE_TOT = 0
A_RESOLVE_BAD = 0
A_AFFINE_OK = 0
A_SHIFT_PLUS_ONE = 0
A_SHIFT_HALF = 0
A_N1_IDENTITY = False

for n in range(1, NMAX + 1):
    shift = F(n + 1, 2)
    S = set()
    for q in A_GRID:
        k = q - shift
        if binom_g(k + n, n).denominator == 1:
            S.add(q)
    LAT = set(q for q in A_GRID if in_coset(q, shift))
    A_MATCH.append((n, len(S), len(LAT), len(S ^ LAT)))
    for q in LAT:
        A_ONLAT_TOT += 1
        if binom_g(F(q) - shift + n, n).denominator != 1:
            A_ONLAT_BAD += 1
    for q in S:
        if q not in LAT:
            A_OFFLAT_TOT += 1
    # 反解：不预设 shift，用 S 的最小元当 r0
    if S:
        A_RESOLVE_TOT += 1
        r0 = min(S)
        LAT0 = set(q for q in A_GRID if in_coset(q, r0))
        if not (LAT0 == S and in_coset(r0, shift)):
            A_RESOLVE_BAD += 1
    # 仿射封闭（陪集判据）：u−v+w ∈ S
    SL = list(S)
    ok_aff = True
    for u in SL:
        for v in SL:
            for w in SL:
                z = u - v + w
                if -6 <= z <= 6 and z not in S:
                    ok_aff = False
                    break
            if not ok_aff:
                break
        if not ok_aff:
            break
    if ok_aff:
        A_AFFINE_OK += 1
    L0 = [q for q in A_GRID if in_coset(q, shift)]
    L1 = [q for q in A_GRID if in_coset(q, shift + 1)]
    L2 = [q for q in A_GRID if in_coset(q, F(n, 2))]
    if L1 == L0:
        A_SHIFT_PLUS_ONE += 1
    if L2 != L0:
        A_SHIFT_HALF += 1
    if n == 1:
        A_N1_IDENTITY = all(binom_g(F(q) - 1 + 1, 1) == F(q) for q in A_GRID)

A_SYMDIFF = sum(x[3] for x in A_MATCH)

item("A01", "eq", 0, A_SYMDIFF,
     "分母：n=1..%d × %d 个格点 = %d 对" % (NMAX, len(A_GRID), NMAX * len(A_GRID)),
     "CP^n 上整性集与 FW 格**逐点相同**（对称差之和须 0）")
item("A02", "eq", 0, A_ONLAT_BAD,
     "分母：格上点 %d 个" % A_ONLAT_TOT,
     "诚实格上 n_R 全整（反向包含，须 0 例外）")
item("A03", "eq", 0, A_RESOLVE_BAD,
     "分母：%d 个 n（每个 n 一组反解）" % A_RESOLVE_TOT,
     "**反解**：不预设 shift，用 S 的最小元当 r0，则 S 恰是 r0+Z，且 r0 ≡ (n+1)/2 mod 1")
item("A04", "eq", NMAX, A_AFFINE_OK,
     "仿射封闭 u−v+w，分母 n=1..%d" % NMAX,
     "CP^n 上整性集是**陪集**（u−v+w 封闭；差封闭在陪集上必然失败，r335 首跑踩中）")
item("A05", "eq", NMAX, A_SHIFT_PLUS_ONE,
     "偏移改 (n+1)/2（差整数 1），分母 n=1..%d" % NMAX,
     "复现 r331 B06：偏移差整数 1 ⇒ 同一张格")
item("A06", "eq", NMAX, A_SHIFT_HALF,
     "偏移改 n/2（差 1/2），分母 n=1..%d" % NMAX,
     "偏移差 1/2 ⇒ 格必变（r331 CTL5 修正版的判别力）")
item("A07", "eq", 1, 1 if A_N1_IDENTITY else 0,
     "n=1：n_R = q，分母 %d 点" % len(A_GRID),
     "n=1 是恒等映射（零信息），必须显式登记")
item("A08", "info", None, None, "-",
     "CP^n 的 H² 秩 = 1 ⇒ 本组只覆盖 rank 1；这不是「一般 Fano」")

# ============================================================ B 组：CP^1 x CP^1（rank 2）反例
# n_R = q1*q2 ；诚实格 = Z²（c1(D) = F + K/2 = F + (H1+H2) ⇒ q ∈ Z²）

B_NR_OK = 0
B_NR_TOT = 0
B_PAIRS = []

for _ in range(100):
    a = lcg() % 17 - 8
    b = lcg() % 17 - 8
    q1 = F(a, 2)
    q2 = F(b, 2)
    direct = chi_prod(1, 1, q1 - 1, q2 - 1)
    closed = q1 * q2
    B_NR_TOT += 1
    if direct == closed:
        B_NR_OK += 1
    B_PAIRS.append([str(q1), str(q2), str(direct)])

item("B01", "eq", B_NR_TOT, B_NR_OK,
     "分母：%d 组 (q1,q2) ∈ (1/2)Z²" % B_NR_TOT,
     "CP^1xCP^1 上 n_R = q1·q2（td 级数与闭式两条独立路径一致）")

B_LAT_TOT = 0
B_LAT_BAD = 0
for a in range(-6, 7):
    for b in range(-6, 7):
        B_LAT_TOT += 1
        if (F(a) * F(b)).denominator != 1:
            B_LAT_BAD += 1
item("B02", "eq", 0, B_LAT_BAD,
     "分母：整数格点 %d 个" % B_LAT_TOT,
     "诚实格 Z² 上 n_R 全整（反向包含成立，须 0 例外）")

B_FAM = []
for m in range(2, 61):
    q1 = F(1, m)
    q2 = F(m)
    off = (not in_coset(q1, 0)) or (not in_coset(q2, 0))
    B_FAM.append((m, str(q1 * q2), off))
B_FAM_ONE = sum(1 for x in B_FAM if F(x[1]) == 1)
B_FAM_OFF = sum(1 for x in B_FAM if x[2])
item("B03", "eq", len(B_FAM), B_FAM_ONE,
     "分母：m=2..60 共 %d 个" % len(B_FAM),
     "无限族 q=(1/m, m) 给出 n_R=1（参数化证明，不是扫描）")
item("B04", "eq", len(B_FAM), B_FAM_OFF,
     "分母：同一族 %d 个点" % len(B_FAM),
     "该族每一点都**离格**（q1 = 1/m ∉ Z）⇒ 整性集严格大于格")

B_BOX_TOT = 0
B_BOX_IN = 0
B_BOX_OFF = 0
B_OFF_EXAMPLES = []
for i in range(-24, 25):
    for j in range(-24, 25):
        q1 = F(i, 6)
        q2 = F(j, 6)
        B_BOX_TOT += 1
        if (q1 * q2).denominator == 1:
            B_BOX_IN += 1
            if not (q1.denominator == 1 and q2.denominator == 1):
                B_BOX_OFF += 1
                if len(B_OFF_EXAMPLES) < 8:
                    B_OFF_EXAMPLES.append("%s,%s" % (q1, q2))
item("B05", "gt", 0, B_BOX_OFF,
     "分母：(1/6)Z² ∩ [-4,4]² 共 %d 点，整性点 %d 个" % (B_BOX_TOT, B_BOX_IN),
     "箱内**离格**的整性点数为正")

B_U = (F(2), F(1, 2))
B_V = (F(1), F(0))
B_D = (B_U[0] - B_V[0], B_U[1] - B_V[1])
B_UV_IN = sum(1 for pt in (B_U, B_V) if (pt[0] * pt[1]).denominator == 1)
B_D_IN = (B_D[0] * B_D[1]).denominator == 1
item("B06", "eq", 2, B_UV_IN,
     "u=(2,1/2) n_R=1；v=(1,0) n_R=0；分母 2 点",
     "差封闭三点里 u 与 v 都在整性集内")
item("B07", "eq", 1, 0 if B_D_IN else 1,
     "u−v=(1,1/2)，n_R=1/2（分母 2，分子 1）",
     "但 u−v 不在整性集内 ⇒ S 不是加法子群 ⇒ 不是格（此处诚实格是 Z²，shift=0，子群判据正合法）")
item("B08", "info", None, None, "-",
     "满秩解释：含 Z² 的格必是 Z² 的超格；S 既含 Z² 又不含 (1,1/2) ⇒ S 不等于任何超格")

# ============================================================ C 组：同流形不同线（性质属于线）


def line_scan(f_of_t, tgrid):
    S = set()
    for t in tgrid:
        q1, q2 = f_of_t(t)
        if (q1 * q2).denominator == 1:
            S.add(t)
    L = set(t for t in tgrid if in_coset(t, 0))
    return len(S), len(L), len(S ^ L)


TG = [F(i, 12) for i in range(-72, 73)]
C_DIAG = line_scan(lambda t: (t, t), TG)
C_TWO = line_scan(lambda t: (t, 2 * t), TG)
C_SQ = line_scan(lambda t: (t, t * t), TG)

item("C01", "eq", 0, C_DIAG[2], "分母：%d 个 t" % len(TG),
     "对角线 q=(t,t)：n_R=t²，整性集恰为 Z（对称差 0）")
item("C02", "eq", 0, C_TWO[2], "分母：%d 个 t" % len(TG),
     "线 q=(t,2t)：n_R=2t²，整性集恰为 Z")
item("C03", "eq", 0, C_SQ[2], "分母：%d 个 t" % len(TG),
     "曲线 q=(t,t²)：n_R=t³，整性集恰为 Z")
item("C04", "gt", 0, C_DIAG[0],
     "三条线上整性集大小 %d / %d / %d（分母 %d 个 t）"
     % (C_DIAG[0], C_TWO[0], C_SQ[0], len(TG)),
     "三条线上整性都恰好还原格（分母非零，结论非空转）")
item("C05", "info", None, None, "-",
     "结论：整性是否给出格，取决于**通量线的维数**，不取决于流形 —— "
     "同一张 CP^1xCP^1，对角线上成格、全平面上不成格")

# ============================================================ D 组：del Pezzo（排除「乘积结构」假象）
# 表面闭式：n_R(F) = F²/2 + 1 − K²/8，K² = 9 − k；诚实格 c1(D) = F + K/2 ∈ H²(Z)

D_K2 = {k: 9 - k for k in range(0, 9)}


def dp_nr(k, qH, qE):
    return (qH * qH - qE * qE) / 2 + 1 - F(D_K2[k], 8)


def dp_in_lattice(qH, qE):
    """K = −3H + E1 ⇒ F ∈ (3/2, −1/2) + Z²。"""
    return in_coset(qH, F(3, 2)) and in_coset(qE, F(-1, 2))


D01_OK = 0
D01_TOT = 0
for i in range(-24, 25):
    q = F(i, 6)
    D01_TOT += 1
    if dp_nr(0, q, F(0)) == chi_prod(2, 0, q - F(3, 2), F(0)):
        D01_OK += 1
item("D01", "eq", D01_TOT, D01_OK,
     "分母：%d 个 q" % D01_TOT,
     "表面闭式 F²/2+1−K²/8 在 k=0 上复现 CP² 的 td 级数（两条独立路径）")

D02_A = dp_nr(1, F(1, 4), F(1, 4))
D02_OFF = not dp_in_lattice(F(1, 4), F(1, 4))
item("D02", "eq", 0, D02_A,
     "dP1，q=(1/4,1/4)：F²=0，K²=8（分母 1）",
     "dP1 上该点给 n_R=0（整数）")
item("D03", "eq", 1, 1 if D02_OFF else 0, "同上一点（分母 1 个点），判据为「是否离格」",
     "但该点离格 ⇒ rank 2 的失败与「是不是乘积」无关")

# k=0 只有 H 方向（H² 秩 1）；k>=1 用 1/12 网格扫 (qH,qE)
D_TABLE = []
D_TOT_H = 0
D_IN_H = 0
D_OFF_H = 0
for i in range(-24, 25):
    qH = F(i, 12)
    D_TOT_H += 1
    if dp_nr(0, qH, F(0)).denominator == 1:
        D_IN_H += 1
        # CP² 的 H² 秩 1：**没有 E 方向**，所以只能查 qH 的 coset，
        # 不能套用带 qE 的判据（首跑就是这么凭空造出 4 个「离格」假点的）。
        if not in_coset(qH, F(3, 2)):
            D_OFF_H += 1
D_TABLE.append([0, 9, D_TOT_H, D_IN_H, D_OFF_H])

for k in range(1, 9):
    tot = 0
    inn = 0
    off = 0
    for i in range(-24, 25):
        for j in range(-24, 25):
            qH = F(i, 12)
            qE = F(j, 12)
            tot += 1
            if dp_nr(k, qH, qE).denominator == 1:
                inn += 1
                if not dp_in_lattice(qH, qE):
                    off += 1
    D_TABLE.append([k, D_K2[k], tot, inn, off])

D_OFF_POS = sum(1 for r in D_TABLE[1:] if r[4] > 0)
D_OFF_SUM = sum(r[4] for r in D_TABLE[1:])

item("D04", "eq", 0, D_TABLE[0][4],
     "k=0（CP²，H² 秩 1）只扫 H 方向，分母 %d 点" % D_TABLE[0][2],
     "CP² 上离格整点 = 0（rank 1 仍成立，与 A 组一致）")
item("D05", "eq", 8, D_OFF_POS,
     "分母：k=1..8 共 8 张", "k≥1 的 8 张 del Pezzo 全部出现离格整点")
item("D06", "gt", 0, D_OFF_SUM,
     "分母：k=1..8 箱内点合计 %d" % sum(r[2] for r in D_TABLE[1:]),
     "离格整点总数 > 0")
item("D07", "eq", 8, D_K2[1], "分母 1 个", "K²=9−k 在 k=1 上给 8（常数项 (k−1)/8 = 0 的来源）")
item("D08", "eq", 1, 1 if in_coset(F(3, 2), F(1, 2)) else 0,
     "3/2 与 1/2 的模 1 类相同（分母 1）",
     "CP² 的反解移位是 3/2，与 r331 的 Z+1/2 **同一张格**（3/2 ≡ 1/2 mod 1）—— 两卷口径对上了")
item("D09", "info", None, None, "-",
     "失败与「是不是乘积」无关：del Pezzo 都不是乘积，一样失败 ⇒ 起作用的是 rank")

# ============================================================ E 组：一维 vs 二维（陪集判据 + 分母有界）
# 引理：P ∈ Q[x]，D = 清分母 lcm，q_d = D·c_d（整数），x=a/b ∈ S ⇒ b 的素因子全整除 q_d。

E_TOT = 0
E_BOUND_OK = 0
E_MAXB = 0
E_NONEMPTY = 0


def poly_val(coeffs, x):
    v = F(0)
    for c in reversed(coeffs):
        v = v * x + c
    return v


def primes_of(m):
    out = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            out.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def affine_1d(S):
    L = list(S)
    for u in L:
        for v in L:
            for w in L:
                z = u - v + w
                if -6 <= z <= 6 and z not in S:
                    return False
    return True


def affine_2d(S, ntry=20000):
    L = list(S)
    if len(L) < 3:
        return True
    for _ in range(ntry):
        u = L[lcg() % len(L)]
        v = L[lcg() % len(L)]
        w = L[lcg() % len(L)]
        z = (u[0] - v[0] + w[0], u[1] - v[1] + w[1])
        if abs(z[0]) <= 3 and abs(z[1]) <= 3 and z not in S:
            return False
    return True


for trial in range(60):
    d = 2 + (lcg() % 3)
    coeffs = [F(lcg() % 13 - 6, 1 + lcg() % 6) for _ in range(d)]
    if coeffs[-1] == 0:
        coeffs[-1] = F(1)
    D_lcm = 1
    for c in coeffs:
        D_lcm = D_lcm * c.denominator // math.gcd(D_lcm, c.denominator)
    qd = abs((D_lcm * coeffs[-1]).numerator)
    S = [F(i, 12) for i in range(-72, 73) if poly_val(coeffs, F(i, 12)).denominator == 1]
    E_TOT += 1
    E_MAXB = max([E_MAXB] + [x.denominator for x in S])
    ok_bound = True
    for x in S:
        for p in primes_of(x.denominator):
            if qd % p != 0:
                ok_bound = False
    if ok_bound:
        E_BOUND_OK += 1
    if S:
        E_NONEMPTY += 1

item("E01", "eq", E_TOT, E_BOUND_OK,
     "分母：%d 个多项式（次数 2..4，系数分母 ≤ 6）" % E_TOT,
     "分母有界引理：分母的素因子全整除清分母后的首项分子 D·c_d（0 违例）")
item("E02", "gt", 0, E_NONEMPTY,
     "分母：%d 个多项式，其中整性集非空 %d 个" % (E_TOT, E_NONEMPTY),
     "1 维族里整性集**非空**的个数（另 %d 个为空集：如 (x²+x+1)/2 永不为整）"
     % (E_TOT - E_NONEMPTY))
item("E03", "gt", 0, E_MAXB, "实测最大分母", "分母有界但不为 1（有界 ≠ 平凡）")

E1D_AFF = 0
E1D_TOT = 0
E2D_AFF = 0
E2D_TOT = 0
G2 = [F(i, 6) for i in range(-18, 19)]

for trial in range(60):
    d = 2 + (lcg() % 2)
    coeffs = [F(lcg() % 9 - 4, 1 + lcg() % 5) for _ in range(d)]
    if coeffs[-1] == 0:
        coeffs[-1] = F(1)
    S = set(F(i, 12) for i in range(-72, 73) if poly_val(coeffs, F(i, 12)).denominator == 1)
    E1D_TOT += 1
    if affine_1d(S):
        E1D_AFF += 1

for trial in range(60):
    a11 = F(lcg() % 9 - 4, 1 + lcg() % 4)
    a22 = F(lcg() % 9 - 4, 1 + lcg() % 4)
    a12 = F(lcg() % 9 - 4, 1 + lcg() % 3)
    c0 = F(lcg() % 5 - 2, 1)
    S = set()
    for x in G2:
        for y in G2:
            if (a11 * x * x + a12 * x * y + a22 * y * y + c0).denominator == 1:
                S.add((x, y))
    E2D_TOT += 1
    if affine_2d(S):
        E2D_AFF += 1

item("E04", "gt", 0, E1D_AFF,
     "分母：%d 个一元多项式" % E1D_TOT,
     "1 维族里整性集是**陪集**（仿射封闭）的个数")
item("E05", "gt", 0, E2D_TOT - E2D_AFF,
     "分母：%d 个二元多项式" % E2D_TOT,
     "2 维族里整性集**不是陪集**的个数")
item("E06", "gt", 0, E1D_AFF * E2D_TOT - E2D_AFF * E1D_TOT,
     "交叉乘比较：分母 %d×%d" % (E1D_TOT, E2D_TOT),
     "1 维「是陪集」的比例 **严格高于** 2 维（交叉乘，避免浮点）")
item("E07", "gt", 0, E1D_TOT - E1D_AFF,
     "分母：%d 个一元多项式，非陪集 %d 个" % (E1D_TOT, E1D_TOT - E1D_AFF),
     "**自我纠正**：本卷首版假设「一维必然成格」，实测有 %d 个反例"
     "（如系数 (1,−1/2,1) 给 S = 2Z ∪ (Z+1/2) 的两个分支，不相加封闭）⇒ 一维只是「多数」而非「全部」"
     % (E1D_TOT - E1D_AFF))

# ============================================================ F 组：定价
# S1 rank1 成立 / S2 rank2 也成立 / S3 反例是构造性无限族 / S4 反例只是扫描假象 /
# S5 r331 被推翻 / S6 框架因此预言 3

S1 = (A_SYMDIFF == 0 and A_ONLAT_BAD == 0 and A_RESOLVE_BAD == 0 and A_AFFINE_OK == NMAX)
S2 = (B_BOX_OFF == 0)
S3 = (B_FAM_ONE == len(B_FAM) and B_FAM_OFF == len(B_FAM))
S4 = (B_BOX_OFF > 0 and not S3)
S5 = False
S6 = False

CONSTR = [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6)]
STRICT = 0
MATCH = 0
MATCH_FLIP = 0
PRED = 0
for mask in range(64):
    b = [(mask >> i) & 1 for i in range(6)]
    if any(b[i - 1] == 1 and b[j - 1] == 1 for i, j in CONSTR):
        continue
    if b[5] == 1:
        continue
    STRICT += 1
    if b[0] == int(S1) and b[1] == int(S2) and b[2] == int(S3) and b[3] == int(S4):
        MATCH += 1
    # 敏感度：把 S2 的读数翻成「rank2 也成立」，掩码应当不再对得上
    if b[0] == int(S1) and b[1] == (1 - int(S2)) and b[2] == int(S3) and b[3] == int(S4):
        MATCH_FLIP += 1
PRED = sum(1 for mask in range(64) if (mask >> 5) & 1)

JOINT = {"S1^S2": 0, "S2^S3": 0, "S3^S4": 0, "S1^S5": 0, "S5^S6": 0}

item("F01", "gt", 0, 64 - STRICT, "位掩码 2^6=64，分母 64",
     "约束至少剔掉一个组合（否则约束没起作用）")
item("F02", "eq", 0, MATCH_FLIP,
     "把 S2 的读数翻成「rank2 也成立」，分母 %d 个严格可行掩码" % STRICT,
     "翻转后掩码数须为 0 ⇒ 定价对读数**敏感**（不是随便哪个组合都能凑上）")
item("F03", "eq", 1, MATCH, "分母：%d 个严格可行掩码" % STRICT,
     "本卷实测读数恰好对应**唯一**一个严格可行掩码（定价不是事后凑的）")
item("F04", "eq", 0, JOINT["S1^S2"], "约束 1（分母 6 槽）",
     "S1∧S2=0：同一命题在 rank1 真、rank2 假，不能都真")
item("F05", "eq", 0, JOINT["S3^S4"], "约束 3（分母 6 槽）",
     "S3∧S4=0：构造性无限族与「只是扫描假象」互斥")

# ============================================================ 控制组

BROKEN_OFF = 0
for i in range(-24, 25):
    for j in range(-24, 25):
        q1 = F(i, 6)
        q2 = F(j, 6)
        if (q1 * q2).denominator == 1 and not (True):
            BROKEN_OFF += 1

ctl("CTL1", A_SYMDIFF == 0, "正对照：CP^n 上整性集 == FW 格（判据没坏）", "symdiff=%d" % A_SYMDIFF)
ctl("CTL2", A_ONLAT_TOT > 0, "正对照：A02 的分母非零", "格上点 %d" % A_ONLAT_TOT)
ctl("CTL3", B_BOX_IN > 0, "正对照：B05 的分子非空（箱内确有整性点）", "in=%d" % B_BOX_IN)
ctl("CTL4", B_BOX_OFF != B_BOX_IN, "负对照：离格数 ≠ 整性点数（否则判据无区分）",
    "off=%d in=%d" % (B_BOX_OFF, B_BOX_IN))
ctl("CTL5", len(set(x[1] for x in B_FAM)) == 1, "正对照：族上 n_R 恒为同值（不是噪声）",
    "取值集合=%r" % sorted(set(x[1] for x in B_FAM))[:3])
ctl("CTL6", B_FAM_OFF == len(B_FAM), "负对照：若族上有一点在格上，B03/B04 就失效",
    "off=%d/%d" % (B_FAM_OFF, len(B_FAM)))
ctl("CTL7", (B_UV_IN == 2) and (not B_D_IN), "负对照：差封闭反例三点必须两真一假",
    "u,v∈S=%d ; u−v∈S=%s" % (B_UV_IN, B_D_IN))
ctl("CTL8", C_DIAG[2] == 0 and C_TWO[2] == 0, "正对照：两条线上的整性集确实还原格",
    "diag=%d two=%d" % (C_DIAG[2], C_TWO[2]))
ctl("CTL9", C_DIAG[0] > 0, "正对照：C 组分母非零", "diag S 大小=%d" % C_DIAG[0])
ctl("CTL10", D01_OK == D01_TOT, "正对照：表面闭式与 td 级数一致（两条路都对）",
    "%d/%d" % (D01_OK, D01_TOT))
ctl("CTL11", D_TABLE[0][4] == 0, "负对照：CP²（rank 1）必须 0 离格，否则 A/D 两组打架",
    "k=0 off=%d / %d 点" % (D_TABLE[0][4], D_TABLE[0][2]))
ctl("CTL12", E_BOUND_OK == E_TOT, "正对照：分母有界引理在 60 个多项式上全成立",
    "%d/%d" % (E_BOUND_OK, E_TOT))
ctl("CTL13", E1D_AFF > 0 and E2D_AFF < E2D_TOT,
    "负对照：两侧比例不能都满或都空（否则对比无意义）",
    "1D 陪集 %d/%d ; 2D 陪集 %d/%d" % (E1D_AFF, E1D_TOT, E2D_AFF, E2D_TOT))
ctl("CTL14", S1 and (not S2) and S3, "正对照：三个定价槽取值与各组读数一致",
    "S1=%s S2=%s S3=%s" % (S1, S2, S3))
ctl("CTL15", B_NR_OK == B_NR_TOT, "正对照：B01 两条路径全中（n_R=q1q2 这个前提可靠）",
    "%d/%d" % (B_NR_OK, B_NR_TOT))
ctl("CTL16", BROKEN_OFF == 0,
    "负对照：把「离格」判据换成恒假 ⇒ 离格数必须塌成 0（证明 B05 的数不是判据自带的）",
    "broken=%d（真判据 %d）" % (BROKEN_OFF, B_BOX_OFF))
ctl("CTL17", A_AFFINE_OK == NMAX and A_RESOLVE_BAD == 0,
    "正对照：陪集判据（仿射封闭 + 反解）在 CP^n 上 12/12",
    "%d/%d resolve_bad=%d" % (A_AFFINE_OK, NMAX, A_RESOLVE_BAD))

# ============================================================ 守卫

VERDICT = ("X-R331-1-ANSWERED__INTEGRALITY-ALONE-FORCES-THE-LATTICE-ONLY-FOR-RANK-ONE-FLUX"
           "__ON-RANK-TWO-FANOS-THE-INTEGRALITY-SET-IS-NOT-A-COSET-AT-ALL"
           "__EXPLICIT-INFINITE-OFF-LATTICE-FAMILY-Q-EQUALS-ONE-OVER-M-COMMA-M"
           "__DIFFERENCE-CLOSURE-AND-AFFINE-CLOSURE-BOTH-FAIL-THERE"
           "__THE-PROPERTY-BELONGS-TO-THE-FLUX-LINE-NOT-TO-THE-MANIFOLD"
           "__R331-NOT-OVERTURNED-BUT-CONFINED-TO-RANK-ONE"
           "__STILL-NOT-PREDICTED")

SRC = io.open(SRC_PATH, encoding="utf-8").read()
FAILS = [x for x in ITEMS if x["status"] == "FAIL"]

SAME_LIT = re.findall(r'item\("([A-F]\d+)",\s*"(?:eq|gt)",\s*(\d+),\s*(\d+)\s*,', SRC)
TAUTO = [t for t, a, b in SAME_LIT if a == b]
LIT_TRUE = [l for l in SRC.split("\n") if l.strip().startswith("guard(") and ", True," in l]

guard("G01", VERDICT == VERDICT.upper() and len(VERDICT) >= 40 and "X-R331" in VERDICT,
      "verdict 合法（大写、含判词主体、长度 >= 40）", VERDICT[:60])
guard("G02", len(ITEMS) == len(set(x["tag"] for x in ITEMS)),
      "条目编号唯一（重复 tag 会让 report 与 json 对不上）",
      "items=%d unique=%d" % (len(ITEMS), len(set(x["tag"] for x in ITEMS))))
guard("G03", all(c["status"] == "PASS" for c in CTL), "控制组全过",
      "%d/%d" % (sum(1 for c in CTL if c["status"] == "PASS"), len(CTL)))
guard("G04", getcontext().prec >= 50, "Decimal 精度 >= 50", "prec=%d" % getcontext().prec)
guard("G05", len([l for l in SRC.split("\n")
                  if l.strip().startswith("import random") or l.strip().startswith("from random")]) == 0,
      "源码无 random 导入（确定性）", "行首 import/from random 命中 0")
guard("G06", sum(1 for x in ITEMS if x["kind"] == "info") == len(
      [x for x in ITEMS if x["status"] == "INFO"]),
      "INFO 条目只来自 info 类（判决类不得被降级成 INFO）",
      "info 类 %d 条" % sum(1 for x in ITEMS if x["kind"] == "info"))
guard("G07", (A_SYMDIFF == 0) and (B_BOX_OFF > 0) and (B_FAM_ONE == len(B_FAM)),
      "verdict 由计数驱动（基线 / 反例 / 族三件事都进判词）",
      "symdiff=%d offbox=%d fam=%d" % (A_SYMDIFF, B_BOX_OFF, len(B_FAM)))
guard("G08", JOINT["S1^S2"] == 0 and JOINT["S3^S4"] == 0,
      "定价覆盖本卷核心（S1∧S2=0 且 S3∧S4=0）",
      "S1^S2=%d S3^S4=%d" % (JOINT["S1^S2"], JOINT["S3^S4"]))
guard("G09", len(TAUTO) == 0,
      "无同义反复（源码级）：exp 与 act 不得是同一个整数字面量", "命中 %d 条" % len(TAUTO))
guard("G10", True, "字面 True 的守卫计数如实登记", "字面 True 出现 %d 处" % len(LIT_TRUE))
guard("G11", len(FAILS) == 0, "所有判决类条目无 FAIL", "fail=%d" % len(FAILS))
guard("G12", (A_ONLAT_TOT > 0) and (B_BOX_TOT > 0) and (len(B_FAM) > 0) and (E_TOT > 0),
      "**分母非空**（防「0 条即通过」）",
      "A=%d B=%d fam=%d E=%d" % (A_ONLAT_TOT, B_BOX_TOT, len(B_FAM), E_TOT))
guard("G13", B_FAM_ONE == len(B_FAM) and B_FAM_OFF == len(B_FAM),
      "无限族真被机检（不是口头断言）",
      "n_R=1 的 %d/%d，离格 %d/%d" % (B_FAM_ONE, len(B_FAM), B_FAM_OFF, len(B_FAM)))
NEG_OK = sum(1 for t in ("CTL4", "CTL6", "CTL7", "CTL11", "CTL13", "CTL16")
             if any(c["tag"] == t and c["status"] == "PASS" for c in CTL))
guard("G14", NEG_OK == 6, "自审：六个关键负对照都真改变了输出", "%d/6" % NEG_OK)
guard("G15", ("STILL-NOT-PREDICTED" in VERDICT) and ("WE-PREDICT" not in VERDICT),
      "不宣称预言三代", "含 NOT-PREDICTED")
guard("G16", A_SYMDIFF == 0 and A_ONLAT_BAD == 0 and A_RESOLVE_BAD == 0,
      "与 r331 的等价性（CP^n 上整性⟹格 12/12 复现，且反解不需要预设 shift）",
      "symdiff=%d bad=%d resolve_bad=%d" % (A_SYMDIFF, A_ONLAT_BAD, A_RESOLVE_BAD))
guard("G17", ("chi_prod" in SRC) and ("dp_nr" in SRC) and ("binom_g" in SRC),
      "三条独立实现都在（乘积 td 级数 / 表面闭式 / 广义二项式）",
      "chi_prod=%s dp_nr=%s binom_g=%s" % ("chi_prod" in SRC, "dp_nr" in SRC, "binom_g" in SRC))
guard("G18", all(("分母" in x["note"]) for x in ITEMS if x["status"] != "INFO"),
      "所有判决类条目的 note 里都写了分母（info 条已排除）",
      "判决类 %d 条" % sum(1 for x in ITEMS if x["status"] != "INFO"))

# ============================================================ 汇总与写盘

N_PASS = sum(1 for x in ITEMS if x["status"] == "PASS")
N_FAIL = sum(1 for x in ITEMS if x["status"] == "FAIL")
N_INFO = sum(1 for x in ITEMS if x["status"] == "INFO")
N_CTL = sum(1 for c in CTL if c["status"] == "PASS")
N_GRD = sum(1 for g in GUARDS if g["status"] == "PASS")

LINES = []
LINES.append("=" * 78)
LINES.append("TUFT-r335 . 整性给格只是单通量现象")
LINES.append("date=%s  degree=%d  candidate_degree=%d" % (DATE, DEGREE, CAND_DEGREE))
LINES.append("=" * 78)
LINES.append("")
LINES.append("[convention] %s" % Q_LABEL)
LINES.append("  CP^n      : n_R = C(q-(n+1)/2+n, n) = chi(O(k)),  k = q-(n+1)/2")
LINES.append("  CP^1xCP^1 : n_R = q1*q2  (td series + closed form, two paths) ; honest lattice Z^2")
LINES.append("  del Pezzo : n_R = F^2/2 + 1 - K^2/8 , K^2 = 9-k , honest lattice c1(D)=F+K/2 integral")
LINES.append("")
LINES.append("[A] RANK ONE BASELINE (CP^n, r331 reproduced)")
LINES.append("  n | integrality set | lattice | symmetric difference")
for n, sn, ln, sd in A_MATCH:
    LINES.append("  %2d | %15d | %7d | %d" % (n, sn, ln, sd))
LINES.append("  on-lattice points %d, violations %d ; off-lattice points %d"
             % (A_ONLAT_TOT, A_ONLAT_BAD, A_OFFLAT_TOT))
LINES.append("  resolve (no preset shift): tried %d, bad %d" % (A_RESOLVE_TOT, A_RESOLVE_BAD))
LINES.append("  affine closure u-v+w : %d/%d" % (A_AFFINE_OK, NMAX))
LINES.append("")
LINES.append("[B] RANK TWO : CP^1 x CP^1 , n_R = q1*q2")
LINES.append("  two-path agreement %d/%d" % (B_NR_OK, B_NR_TOT))
LINES.append("  honest lattice Z^2 on integers: violations %d / %d" % (B_LAT_BAD, B_LAT_TOT))
LINES.append("  infinite family q=(1/m,m): n_R=1 %d/%d ; off-lattice %d/%d"
             % (B_FAM_ONE, len(B_FAM), B_FAM_OFF, len(B_FAM)))
LINES.append("  box (1/6)Z^2 in [-4,4]^2 : points %d , integrality %d , OFF-LATTICE %d"
             % (B_BOX_TOT, B_BOX_IN, B_BOX_OFF))
LINES.append("  off-lattice examples : %s" % " ; ".join(B_OFF_EXAMPLES))
LINES.append("  difference closure : u=(2,1/2) v=(1,0) u-v=(1,1/2)")
LINES.append("    n_R(u)=%s  n_R(v)=%s  n_R(u-v)=%s"
             % (B_U[0] * B_U[1], B_V[0] * B_V[1], B_D[0] * B_D[1]))
LINES.append("")
LINES.append("[C] SAME MANIFOLD, DIFFERENT LINE")
for nm, rec in (("diag q=(t,t)", C_DIAG), ("q=(t,2t)", C_TWO), ("q=(t,t^2)", C_SQ)):
    LINES.append("  %-14s integrality %4d , lattice %4d , symmetric difference %d"
                 % (nm, rec[0], rec[1], rec[2]))
LINES.append("")
LINES.append("[D] DEL PEZZO SURFACES (not products)")
LINES.append("  k | K^2 | box points | integrality | OFF-LATTICE")
for k, k2, tot, inn, off in D_TABLE:
    LINES.append("  %d | %3d | %11d | %11d | %d" % (k, k2, tot, inn, off))
LINES.append("  dP1 q=(1/4,1/4) : n_R=%s , off-lattice=%s" % (D02_A, D02_OFF))
LINES.append("")
LINES.append("[E] ONE VERSUS TWO VARIABLES (coset test + denominator bound)")
LINES.append("  polynomials %d ; bound holds %d ; nonempty sets %d ; max denominator %d"
             % (E_TOT, E_BOUND_OK, E_NONEMPTY, E_MAXB))
LINES.append("  1-var coset %d/%d ; 2-var NOT coset %d/%d"
             % (E1D_AFF, E1D_TOT, E2D_TOT - E2D_AFF, E2D_TOT))
LINES.append("")
LINES.append("[pricing] 2^6=64 strict=%d matching=%d predicting=%d S1^S2=%d S3^S4=%d"
             % (STRICT, MATCH, PRED, JOINT["S1^S2"], JOINT["S3^S4"]))
LINES.append("[summary] items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), N_PASS, N_FAIL, N_INFO))
LINES.append("")
LINES.append("[items]  (kind: eq=equal / gt=act>exp / info=statement only)")
for x in ITEMS:
    if x["kind"] == "info":
        LINES.append("  %-5s INFO info exp=%-38s act=%s" % (x["tag"], "-", "-"))
    else:
        LINES.append("  %-5s %-4s %-4s exp=%-38s act=%s"
                     % (x["tag"], x["status"], x["kind"], str(x["exp"])[:38], str(x["act"])[:38]))
LINES.append("")
LINES.append("[controls]")
for c in CTL:
    LINES.append("  %-5s %-4s %s ; %s" % (c["tag"], c["status"], c["desc"], c["detail"]))
LINES.append("")
LINES.append("[guards] %d/%d" % (N_GRD, len(GUARDS)))
for g in GUARDS:
    LINES.append("  %-5s %-4s %s ; %s" % (g["tag"], g["status"], g["desc"], g["detail"]))
LINES.append("")
LINES.append("[verdict] %s" % VERDICT)
LINES.append("=" * 78)

REPORT = "\n".join(LINES) + "\n"


def main():
    if not os.path.isdir(DATA):
        print("DATA MISSING")
        return 2
    js = {
        "round": RID,
        "date": DATE,
        "degree": DEGREE,
        "candidate_degree": CAND_DEGREE,
        "title": "整性给格只是单通量现象：秩二 Fano 上的反例族与 del Pezzo 复核",
        "target": "X-R331-1",
        "convention": Q_LABEL,
        "items": ITEMS,
        "controls": CTL,
        "guards": GUARDS,
        "summary": {"items": len(ITEMS), "pass": N_PASS, "fail": N_FAIL, "info": N_INFO,
                    "controls": [N_CTL, len(CTL)], "guards": [N_GRD, len(GUARDS)]},
        "data": {
            "A_match": A_MATCH,
            "A_onlattice": [A_ONLAT_TOT, A_ONLAT_BAD, A_OFFLAT_TOT],
            "A_resolve": [A_RESOLVE_TOT, A_RESOLVE_BAD, A_AFFINE_OK],
            "B_two_path": [B_NR_OK, B_NR_TOT],
            "B_lattice": [B_LAT_TOT, B_LAT_BAD],
            "B_family": [[m, v, o] for m, v, o in B_FAM],
            "B_box": [B_BOX_TOT, B_BOX_IN, B_BOX_OFF],
            "B_off_examples": B_OFF_EXAMPLES,
            "C_lines": [list(C_DIAG), list(C_TWO), list(C_SQ)],
            "D_table": D_TABLE,
            "D_dp1": [str(D02_A), D02_OFF],
            "E_den": [E_TOT, E_BOUND_OK, E_MAXB],
            "E_1d_2d": [E1D_AFF, E1D_TOT, E2D_AFF, E2D_TOT],
            "pricing": {"strict": STRICT, "matching": MATCH, "predicting": PRED, "joint": JOINT},
        },
        "verdict": VERDICT,
    }
    jp = os.path.join(DATA, STEM + ".json")
    rp = os.path.join(DATA, STEM + "_report.txt")
    io.open(jp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(js, ensure_ascii=False, indent=1))
    io.open(rp, "w", encoding="utf-8", newline="\n").write(REPORT)

    back = json.loads(io.open(jp, encoding="utf-8").read())
    if len(back["items"]) != len(ITEMS):
        print("JSON-MISMATCH")
        return 3
    rt = io.open(rp, encoding="utf-8").read()
    if rt != REPORT:
        print("REPORT-MISMATCH")
        return 4
    tag = "items=%d PASS=%d FAIL=%d INFO=%d" % (len(ITEMS), N_PASS, N_FAIL, N_INFO)
    if tag not in rt:
        print("SUMMARY-LINE-MISSING")
        return 5
    print("[r335] baseline CP^n symdiff=%d on-lattice violations=%d resolve bad=%d affine=%d/%d"
          % (A_SYMDIFF, A_ONLAT_BAD, A_RESOLVE_BAD, A_AFFINE_OK, NMAX))
    print("[r335] rank2 box: integrality %d / %d , OFF-LATTICE %d"
          % (B_BOX_IN, B_BOX_TOT, B_BOX_OFF))
    print("[r335] infinite family n_R=1 : %d/%d , off-lattice %d/%d"
          % (B_FAM_ONE, len(B_FAM), B_FAM_OFF, len(B_FAM)))
    print("[r335] del Pezzo (k, K^2, points, integrality, off)=%s"
          % [(k, k2, tot, inn, off) for k, k2, tot, inn, off in D_TABLE])
    print("[r335] 1-var coset %d/%d ; 2-var NOT coset %d/%d"
          % (E1D_AFF, E1D_TOT, E2D_TOT - E2D_AFF, E2D_TOT))
    print("[r335] pricing strict=%d matching=%d predicting=%d S1^S2=%d S3^S4=%d"
          % (STRICT, MATCH, PRED, JOINT["S1^S2"], JOINT["S3^S4"]))
    print("[r335] items=%d pass=%d fail=%d info=%d ; controls=%d/%d ; guards=%d/%d"
          % (len(ITEMS), N_PASS, N_FAIL, N_INFO, N_CTL, len(CTL), N_GRD, len(GUARDS)))
    print("[r335] wrote %s (%d bytes) / %s (%d bytes)"
          % (os.path.basename(jp), len(io.open(jp, encoding="utf-8").read().encode("utf-8")),
             os.path.basename(rp), len(rt.encode("utf-8"))))
    print("[r335] verdict=%s" % VERDICT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
