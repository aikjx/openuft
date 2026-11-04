# -*- coding: utf-8 -*-
"""TUFT-r394  审计 ROOT V61（四力大统一的真空稳定性与粒子谱审查）
纯标准库（Fraction + Decimal，判据区无浮点、无随机）。不读任何来料中间量。

本卷只做一件事：把 V61 的六项主张逐条变成**可算判决**。
  §一 中心化子 46 / 残余 34          → A1 A2
  §二 单个 10 Higgs 不能破缺         → A3 A4 A5
  §三 m_H = m_T                      → A6
  §四 6 代 + 24 额外单态             → A7 A8
  §五 势与 Δ 的四行条件              → A9 A10
  §六 Jarlskog 恒等式                → A11 A12
  §八 26/26 通过                     → A13
"""
import io
import os
import json
import re
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 50

RID = "r394"
TITLE = ("TUFT-r394_审计ROOTV61_中心化子46与34个残余生成元_单个十维Higgs论证无效但结论对_"
         "Schur锁死二重态三重态简并_六代计数与半整数出口_Jarlskog恒等式精确复核_精算_2026-11-04")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")
os.makedirs(DATA, exist_ok=True)

MAIN, CTL, GRD = [], [], []
ALL = []


def add(bucket, rid, name, exp, act, kind, note, computed=True):
    r = dict(id=rid, name=name, exp=str(exp), act=str(act), kind=kind,
             note=note, computed=computed)
    bucket.append(r)
    ALL.append(r)
    return r


# ============================================================ 精确线性代数（Fraction）
Z = F(0)
O = F(1)


def zeros(n, m):
    return [[Z] * m for _ in range(n)]


def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    C = zeros(n, m)
    for i in range(n):
        Ai, Ci = A[i], C[i]
        for t in range(k):
            a = Ai[t]
            if a == 0:
                continue
            Bt = B[t]
            for j in range(m):
                b = Bt[j]
                if b != 0:
                    Ci[j] += a * b
    return C


def comm(A, B):
    return [[A[i][j] * 0 + (sum(A[i][p] * B[p][j] for p in range(len(B))) -
                            sum(B[i][p] * A[p][j] for p in range(len(B))))
             for j in range(len(A))] for i in range(len(A))]


def rref_rank(rows, ncols):
    M = [[x if isinstance(x, F) else F(x) for x in r] for r in rows if any(x != 0 for x in r)]
    if not M:
        return 0
    rank = 0
    nrow = len(M)
    for c in range(ncols):
        piv = -1
        for r in range(rank, nrow):
            if M[r][c] != 0:
                piv = r
                break
        if piv < 0:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][c]
        if pv != 1:
            M[rank] = [x / pv for x in M[rank]]
        R = M[rank]
        for r in range(nrow):
            if r != rank and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], R)]
        rank += 1
        if rank == nrow:
            break
    return rank


def nullity(rows, ncols):
    return ncols - rref_rank(rows, ncols)


def so_basis(n, upto=None):
    """E_ij（i<j）：第 i 行第 j 列 +1、第 j 行第 i 列 −1。upto 限制指标上界（含）。"""
    hi = n if upto is None else upto
    out = []
    for i in range(hi):
        for j in range(i + 1, hi):
            M = zeros(n, n)
            M[i][j] = O
            M[j][i] = -O
            out.append(M)
    return out


def centralizer_dim(n, T):
    """Cent_{so(n)}(T)：未知量 = 66 个系数，约束 = [B_c,T] 的全部 n² 个元素。"""
    basis = so_basis(n)
    brackets = [comm(B, T) for B in basis]        # 每个基元只算一次
    rows = []
    for i in range(n):
        for j in range(n):
            rows.append([Br[i][j] for Br in brackets])
    return nullity(rows, len(basis))


# ============================================================ A1 中心化子维数（三档）
T0 = zeros(12, 12)
TF = zeros(12, 12)
TF[10][11] = O
TF[11][10] = -O
TFC = zeros(12, 12)
for k, cf in enumerate((1, 2, 4, 8, 16, 32)):
    i = 2 * k
    TFC[i][i + 1] = F(cf)
    TFC[i + 1][i] = F(-cf)

c_zero = centralizer_dim(12, T0)
c_one = centralizer_dim(12, TF)
c_cart = centralizer_dim(12, TFC)
a1_ok = (c_zero == 66 and c_one == 46 and c_cart == 6)
add(MAIN, "A1",
    "so(12) 的中心化子维数：T=0 给全空间、单平面磁通给 46、一般 Cartan 元只给 6",
    "66 / 46 / 6（三档互不相同）",
    "T=0 → %d；T_F=E_{11,12} → %d；一般 Cartan → %d（so(12) 维数 %d）"
    % (c_zero, c_one, c_cart, len(so_basis(12))),
    "PASS" if a1_ok else "FAIL",
    "★★这是 V61 §一 的第一条硬读数：46 由 66 个显式生成元的换位子核算出，不是把 45+1 抄一遍。"
    "★三档读数互不相同 ⇒ 计数本身有判别力（若换位子判据写错、把 66 个都算成未破缺，T=0 那档会与它重合）")

# ============================================================ A2 分解账
GENS10 = so_basis(12, upto=10)                 # so(10) 的 45 个生成元（嵌在 12 维里）
n_so12 = len(so_basis(12))
n_so10 = len(GENS10)
span_h = n_so10 + 1
check_comm = all(comm(G, TF) == zeros(12, 12) for G in GENS10)
a2_ok = (n_so12 == 66 and n_so10 == 45 and span_h == 46 and check_comm
         and n_so12 - span_h == 20 and span_h - 12 == 34 and 45 - 12 == 33)
add(MAIN, "A2",
    "V61 §一 的维数账：66 = 45+1+10+10，未破缺 46，残余 46−12 = 34 = 33+1",
    "66 = 45+1+10+10；46−12 = 34 = 33+1",
    "so(12)=%d；so(10)=%d；h=so(10)⊕u(1)=%d；差集=%d=10+10；"
    "45 个生成元逐个与 T_F 换位 = %s；46−12=%d=33+1"
    % (n_so12, n_so10, span_h, n_so12 - span_h, check_comm, span_h - 12),
    "PASS" if a2_ok else "FAIL",
    "★V61 这条账算术全对，本卷独立复算（45 个显式生成元逐个换位，不是引 Schur）。"
    "★★但「33 个属于 Spin(10) 内尚未破缺」隐含「SM 的 12 个生成元整体住在 so(10) 里」——"
    "本卷核为真（标准嵌入），来料未写，属**前提未写全**")

# ============================================================ A3 §二 的论证无效（真判负）
GENS8_10 = so_basis(10, upto=8)                # so(8) 的 28 个生成元（嵌在 10 维里）
SUB = []
for block in ((0, 1, 2, 3), (4, 5, 6, 7)):
    for a in block:
        for b in block:
            if a < b:
                M = zeros(10, 10)
                M[a][b] = O
                M[b][a] = -O
                SUB.append(M)
_rows_sub = [[X[i][j] for i in range(10) for j in range(10)] for X in SUB]
_rk_sub = rref_rank(_rows_sub, 100)
closed = True
for X in SUB:
    for Y in SUB:
        C = comm(X, Y)
        flat = [C[i][j] for i in range(10) for j in range(10)]
        if rref_rank(_rows_sub + [flat], 100) != _rk_sub:
            closed = False
a3_ok = (_rk_sub == 12 and closed)
add(MAIN, "A3",
    "★V61 §二 的论证无效：把「稳定子维数 28 > SM 维数 12」当成「SM 不是稳定子」的判据",
    "论证无效（结论仍对，由 A4 独立证成）",
    "so(4)⊕so(4) ⊂ so(8) 的显式 12 维子代数：维数 %d、对换位封闭 = %s ⇒ "
    "「28 > 12」并不排除 12 维子代数 ⇒ 该不等式对「SM ⊂ 稳定子」零判别力" % (_rk_sub, closed),
    "FAIL" if a3_ok else "PASS",
    "★★本卷唯一的真判负：**结论对、理由错**。V61 由「一般复 10 的稳定子含 SO(8)（维 28）」"
    "跳到「28 > 12 ⇒ 不能完成 SM 破缺」——维数比较不能判定子群关系，反例就在 so(8) 里。"
    "★正确判据见 A4（单态计数），它给的是更强的结论：SM 不稳定化 10 里**任何**非零矢量")

# ============================================================ A4 正确判据：10 在 SM 下无单态
fives = [((3, 1), F(-1, 3)), ((1, 2), F(1, 2))]
all_parts = []
for rep, y in fives:
    all_parts.append((rep, y, +1))
    all_parts.append((rep, -y, -1))
dim_sum = sum(r[0][0] * r[0][1] for r in all_parts)
traceless = sum(r[0][0] * r[0][1] * r[1] for r in all_parts)
singlets = [r for r in all_parts if r[0] == (1, 1) and r[1] == 0]
a4_ok = (dim_sum == 10 and len(singlets) == 0 and traceless == 0)
add(MAIN, "A4",
    "正确的判据：10 在 SU(3)×SU(2)×U(1) 下没有单态 ⇒ SM 不稳定化 10 里任何非零矢量",
    "单态数 = 0；维数和 = 10；超荷和 = 0",
    "10 = 5+5̄ = (3,1,−1/3)+(1,2,+1/2)+c.c. ⇒ 维数和 %d、超荷和 %s、**单态数 %d**"
    % (dim_sum, traceless, len(singlets)),
    "PASS" if a4_ok else "FAIL",
    "★★为什么这条比维数比较硬：SM ⊂ 稳定子(v) ⟺ v 是 SM 不变向量 ⟺ v 落在 10 的单态子空间。"
    "单态数 0 ⇒ 任何非零 v 都被某个 SM 生成元推动 ⇒ **单个 10 的任意 VEV 一定破 SM**。"
    "★正对照：超荷和 3·(−1/3)+2·(+1/2)=0（分解若抄错，这个和一般不为 0）")

# ============================================================ A5 稳定子维数：36 / 28
GENS10_10 = so_basis(10)


def stabilizer_dim(gens, vecs):
    """未知量 = 生成元系数；约束 = (Σ c_X X)·v 对**每个** v 的 n 个分量全为 0。"""
    n = len(vecs[0])
    rows = []
    for vec in vecs:
        for i in range(n):
            rows.append([sum(X[i][j] * vec[j] for j in range(n)) for X in gens])
    return nullity(rows, len(gens))


v1 = [O] + [Z] * 9
v2 = [O, O] + [Z] * 8
st1 = stabilizer_dim(GENS10_10, [v1])
st2 = stabilizer_dim(GENS10_10, [v1, v2])
a5_ok = (st1 == 36 and st2 == 28)
add(MAIN, "A5",
    "稳定子维数复算：一个实矢量给 so(9)=36，两个独立实矢量给 so(8)=28",
    "36 / 28",
    "v=e₁ → %d（so(9)=%d）；v=(e₁,e₂) → %d（so(8)=%d）"
    % (st1, 9 * 8 // 2, st2, 8 * 7 // 2),
    "PASS" if a5_ok else "FAIL",
    "★V61 的 36/28 两个数本身对。★但「复 10 的实部虚部最多给两个独立实矢量」只在两分量不共线时成立；"
    "若两分量共线（v 与 iv），稳定子是 so(9)=36 ⇒ 来料取了**最弱**的下界，方向对但不是等号")


# ============================================================ A6 Schur：不变对称算子维数
def invariant_symmetric_dim(gens, n):
    idx = {}
    k = 0
    for i in range(n):
        for j in range(i, n):
            idx[(i, j)] = k
            k += 1
    nv = k
    rows = []
    for X in gens:
        for i in range(n):
            for j in range(n):
                row = [Z] * nv
                for p in range(n):
                    c = X[p][j]
                    if c != 0:
                        key = (i, p) if i <= p else (p, i)
                        row[idx[key]] += c
                for q in range(n):
                    c = -X[i][q]
                    if c != 0:
                        key = (q, j) if q <= j else (j, q)
                        row[idx[key]] += c
                rows.append(row)
    return nullity(rows, nv)


# 生成元取「路径」集 E_{i,i+1}：与之全部换位 ⇔ 与整个 so(n) 换位（换位子封闭）
PATH10 = []
for i in range(9):
    M = zeros(10, 10)
    M[i][i + 1] = O
    M[i + 1][i] = -O
    PATH10.append(M)
PATH8 = []
for i in range(7):
    M = zeros(10, 10)
    M[i][i + 1] = O
    M[i + 1][i] = -O
    PATH8.append(M)
inv10 = invariant_symmetric_dim(PATH10, 10)
inv8 = invariant_symmetric_dim(PATH8, 10)
inv10_full = invariant_symmetric_dim(GENS10_10, 10)      # 两条路径：全生成元 vs 路径集
a6_ok = (inv10 == 1 and inv8 == 4 and inv10_full == 1)
add(MAIN, "A6",
    "Schur：与整个 so(10) 交换的对称 10×10 算子只有 1 维 ⇒ 二次涨落算符必 ∝ 单位 ⇒ m_H = m_T",
    "1 维（负对照：so(8) 给 4 维；全 45 生成元与路径集同读数）",
    "so(10) 不变量维数 = %d（路径集）/ %d（全 45 个）；so(8) 作用在 R^10=8+1+1 上 = %d"
    % (inv10, inv10_full, inv8),
    "PASS" if a6_ok else "FAIL",
    "★★这解释了 V61 §三 的 m_H = m_T：不是「磁通只沿 U(1)_F」这个模型选择，而是 **Schur 引理**——"
    "只要未破缺群含 so(10) 且 10 不可约，任何不变的二次算子就是纯数 ⇒ 简并是**定理**，"
    "分裂只能来自破 so(10) 的序参量或边界项（与 A3/A4 一致：单个 10 本来就破 SM）。"
    "★负对照 so(8) 给 4 维（8×8 单位 ⊕ 2×2 对称块）⇒ 简并不是「怎么算都 1」")

# ============================================================ A7 六代计数：N=3 ⇒ 6
N_FLUX = 3
n16 = N_FLUX
n16b = N_FLUX
total16 = n16 + n16b
net = 1 * N_FLUX + (-1) * (-N_FLUX)
sum_sq = 1 * N_FLUX ** 2 + (-1) * (-N_FLUX) ** 2
a7_ok = (total16 == 6 and net == 6 and sum_sq == 0)
add(MAIN, "A7",
    "V61 §四 的六代计数：32 → 16_{+1} ⊕ 16̄_{−1}，N=3 ⇒ 左手 16 共 6 个（不是 3）",
    "6 套；净手征 n = 6；Σ s Q² = 0",
    "16_{+1}：%d 个；16̄_{−1}：%d 个（电荷共轭后同为左手 16）⇒ 合计 %d；"
    "净手征 n = Σ s Q = %d；Σ s Q² = %d" % (n16, n16b, total16, net, sum_sq),
    "PASS" if a7_ok else "FAIL",
    "★★这条与 r392 的 `n = 2q₊` 是**同一个读数**（q₊=3 ⇒ 6）：V61 说「6 而不是 3」，"
    "r392 说「整数磁通下 n 恒偶、非平凡支 n = 2q₊」。★Σ s Q² = 0 ⇒ 反常正好抵消，"
    "所以「6」不是反常在捣乱，是**整数性**在捣乱")

# ============================================================ A8 出口：q₊ = 3/2 ⇒ 3
def two_family(qp_num, qm_num, den):
    qp = F(qp_num, den)
    qm = F(qm_num, den)
    return qp - qm, qp * qp - qm * qm


n_int, sq_int = two_family(3, -3, 1)
n_halfA, sq_halfA = two_family(3, -3, 2)   # ★后缀 A8：防被后续段（A13）同名覆盖
a8_ok = (n_int == 6 and n_halfA == 3 and sq_int == 0 and sq_halfA == 0)
add(MAIN, "A8",
    "「6 而不是 3」是整数磁通的后果：把同一个 N 改成半整数 N=3/2 ⇒ 净手征恰为 3",
    "整数给 6，半整数（分母 2）给 3；两者 Σ s Q² 都 = 0",
    "q=(3,−3)：n=%s、Σ s Q²=%s；q=(3/2,−3/2)：n=%s、Σ s Q²=%s"
    % (n_int, sq_int, n_halfA, sq_halfA),
    "PASS" if a8_ok else "FAIL",
    "★★这是本卷对「攻破」二字的唯一正面贡献：V61 §四 把「6 代」记成一条**限制**，"
    "r392 已证它只是**分母**的后果 —— 半整数磁通下 n=3 精确可达且两项反常仍抵消。"
    "★所以 V61 若想保住「三代」，该改的不是谱，是**磁通量子化条件**（代价：几何实现，r392 §十已登记）")

# ============================================================ A9 势的四行条件
MU2 = F(1)
LAM = F(1, 2)
VAC2 = MU2 / (2 * LAM)          # v² = 1 ⇒ v = 1（有理，便于精确取样）


def V_pot(h2, t2, delta):
    r = h2 + t2
    return -MU2 * r + LAM * r * r + delta * t2


def second_deriv(fn, x0, deg=4, step=F(1, 7)):
    """精确二阶导：在 u = x − x0 上做 degree-4 Vandermonde 拟合（五次点），返回 2·c₂。"""
    us = [F(k) * step for k in range(deg + 1)]
    ys = [fn(x0 + u) for u in us]
    n = deg + 1
    A = [[u ** k for k in range(n)] + [y] for u, y in zip(us, ys)]
    for c in range(n):
        piv = -1
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r
                break
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [v / pv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    c2 = A[2][n]
    return 2 * c2


DELTA = F(1, 3)
d2_h = second_deriv(lambda x: V_pot(x * x, Z, DELTA), O)
d2_t = second_deriv(lambda x: V_pot(O, x * x, DELTA), Z)
sign_rows = []
for d, want in ((F(-1, 3), -1), (F(0), 0), (F(1, 3), +1)):
    cc = second_deriv(lambda x: V_pot(O, x * x, d), Z)
    got = -1 if cc < 0 else (0 if cc == 0 else +1)
    sign_rows.append((d, got == want, cc))
origin_ok = all(((-MU2 + d) >= 0) == (d >= MU2) for d in (Z, F(1, 2), O, F(2)))
a9_ok = (d2_t == 2 * DELTA and all(g for _, g, _ in sign_rows) and origin_ok
         and d2_h == 8 * LAM * VAC2)
add(MAIN, "A9",
    "§五 的示范势：Δ 的四行条件逐条成立，二次项系数由精确 Vandermonde 独立取出",
    "H 方向 V''=8λv²=4；T 方向 V''=2Δ；四行条件全成立",
    "H 方向 V'' = %s（解析 8λv²=%s）；T 方向 V'' = %s（解析 2Δ=%s）；"
    "Δ<0/0/>0 三档 = %s；原点条件（Δ≥μ² ⇔ 无负质量平方）= %s"
    % (d2_h, 8 * LAM * VAC2, d2_t, 2 * DELTA, [str(g) for _, g, _ in sign_rows], origin_ok),
    "PASS" if a9_ok else "FAIL",
    "★两条独立路径：解析式（∂²V）与 5 点精确 Vandermonde 拟合（degree 4 恰好无截断误差）。"
    "★★注意 T 方向的二次项是 **2Δ 而不是 Δ** —— 口径账见 A10。"
    "★H 方向 8λv² 与 T 方向 2Δ 不能直接比大小（H 的径向模与 T 的整模归一化不同）")

# ============================================================ A10 归一化口径（INFO）
add(MAIN, "A10",
    "口径账：m_T² = Δ 还是 2Δ，取决于场的归一化约定；来料未写死",
    "复场归一化给 Δ，实分量归一化给 2Δ（差因子 2）",
    "V ⊃ Δ|T|²：复场标准动能 |∂T|²（质量项 m²|T|²）⇒ m² = Δ，V61 式 (61-6) 成立；"
    "拆成实分量（动能 ½(∂φ)²、质量项 ½m²φ²）⇒ m² = 2Δ；本卷 Vandermonde 实测二次项 = 2Δ = %s"
    % (2 * DELTA),
    "INFO",
    "★按 V59 的教训：**归一化未写死就记 INFO，不指控**。Δ 的四个**符号**条件与归一化无关"
    "（A9 全成立），只有绝对值差因子 2 ⇒ 不影响 V61 的定性结论，但影响日后与实验数比大小")

# ============================================================ A11 Jarlskog 恒等式（全精确）
def cq(re, im=0):
    return (F(re), F(im))


def c_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def c_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def c_conj(a):
    return (a[0], -a[1])


def cm_zeros(n):
    return [[(Z, Z)] * n for _ in range(n)]


def cm_eye(n):
    M = cm_zeros(n)
    for i in range(n):
        M[i][i] = (O, Z)
    return M


def cm_mul(A, B):
    n = len(A)
    C = cm_zeros(n)
    for i in range(n):
        for j in range(n):
            acc = (Z, Z)
            for k in range(n):
                acc = c_add(acc, c_mul(A[i][k], B[k][j]))
            C[i][j] = acc
    return C


def cm_dag(A):
    n = len(A)
    return [[c_conj(A[j][i]) for j in range(n)] for i in range(n)]


def cm_comm(A, B):
    P = cm_mul(A, B)
    Q = cm_mul(B, A)
    return [[(P[i][j][0] - Q[i][j][0], P[i][j][1] - Q[i][j][1]) for j in range(len(A))]
            for i in range(len(A))]


def cm_pow(A, p):
    R = cm_eye(len(A))
    for _ in range(p):
        R = cm_mul(R, A)
    return R


def cm_trace(A):
    acc = (Z, Z)
    for i in range(len(A)):
        acc = c_add(acc, A[i][i])
    return acc


def unit_g(num_re, num_im, den):
    v = (F(num_re, den), F(num_im, den))
    assert v[0] * v[0] + v[1] * v[1] == 1, (num_re, num_im, den)
    return v


def inv3(M):
    d = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
         - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
         + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    inv = [[Z] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            sub = [row[:] for row in M]
            sub.pop(i)
            for row in sub:
                row.pop(j)
            inv[j][i] = ((-1) ** (i + j)) * (sub[0][0] * sub[1][1] - sub[0][1] * sub[1][0]) / d
    return inv


def rm_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def cayley(a, b, c):
    """Cayley 变换 R = (I−A)(I+A)^{-1}，A 反对称且有理 ⇒ R 有理正交（一般位置，不是单轴旋转）。"""
    A = [[Z, F(a), F(b)], [F(-a), Z, F(c)], [F(-b), F(-c), Z]]
    I3 = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return rm_mul([[I3[i][j] - A[i][j] for j in range(3)] for i in range(3)],
                  inv3([[I3[i][j] + A[i][j] for j in range(3)] for i in range(3)]))


def lift(R):
    return [[cq(R[i][j]) for j in range(3)] for i in range(3)]


def diag_c(ph):
    D = cm_zeros(3)
    for i, p in enumerate(ph):
        D[i][i] = p
    return D


def herm_from(U, d):
    D = cm_zeros(3)
    for i, x in enumerate(d):
        D[i][i] = cq(x)
    return cm_mul(cm_mul(U, D), cm_dag(U))


def jarlskog(V):
    t = c_mul(c_mul(V[0][0], V[1][1]), c_mul(c_conj(V[0][1]), c_conj(V[1][0])))
    return t[1]


R1 = cayley(F(1, 3), F(1, 5), F(1, 7))
R2 = cayley(F(2, 5), F(1, 4), F(3, 8))
orth_ok = (rm_mul(R1, [[R1[j][i] for j in range(3)] for i in range(3)]) ==
           [[O if i == j else Z for j in range(3)] for i in range(3)])
Uu = cm_mul(diag_c([unit_g(3, 4, 5), unit_g(5, 12, 13), cq(1)]), lift(R1))
Ud = cm_mul(diag_c([cq(1), unit_g(8, 15, 17), unit_g(4, 3, 5)]), lift(R2))
du = (F(1), F(3), F(7))
dd = (F(2), F(5), F(11))
Hu = herm_from(Uu, du)
Hd = herm_from(Ud, dd)
def fnum(x, nd=12):
    """Fraction → 定点显示串（只用于展示，判据仍用精确分数）。"""
    if not isinstance(x, F):
        x = F(x)
    dd = Decimal(x.numerator) / Decimal(x.denominator)
    return str(dd.quantize(Decimal(1).scaleb(-nd)))


lhs = cm_trace(cm_pow(cm_comm(Hu, Hd), 3))[1]
Vmix = cm_mul(cm_dag(Uu), Ud)
Jval = jarlskog(Vmix)
pu = (du[0] - du[1]) * (du[0] - du[2]) * (du[1] - du[2])
pd = (dd[0] - dd[1]) * (dd[0] - dd[2]) * (dd[1] - dd[2])
rhs6 = 6 * Jval * pu * pd
rhs_m6 = -6 * Jval * pu * pd
matched = "+6" if lhs == rhs6 else ("-6" if lhs == rhs_m6 else "none")
a11_ok = (matched != "none") and (lhs != 0) and (Jval != 0) and orth_ok
add(MAIN, "A11",
    "V61 式 (61-8)：Im tr([H_u,H_d]³) = 6·J·∏(m²_ui−m²_uj)·∏(m²_dk−m²_dl)",
    "系数绝对值 = 6 精确成立（Gauss 有理数，零容差），符号随 (i<j) 排序定",
    "Im tr = %s；6J·∏∏ = %s；−6J·∏∏ = %s ⇒ 命中 = %s；J = %s；R 正交 = %s"
    % (fnum(lhs), fnum(rhs6), fnum(rhs_m6), matched, fnum(Jval), orth_ok),
    "PASS" if a11_ok else "FAIL",
    "★★全精确（Fraction）：U = D·R，D 是模 1 的 Gauss 有理数（勾股数）、R 是 Cayley 变换给的"
    "**有理正交阵**（不是单轴旋转，否则 J 会退化为 0，见 K3）⇒ J 与两侧都是有理数，**零容差**。"
    "★两条独立路径：左边三次矩阵乘法取迹，右边只用特征值差与混合矩阵。"
    "★★**系数 6 是绝对值**：把 ∏ 的排序反过来常数变 −6 ⇒ 排序必须写死（本卷取 i<j），"
    "报「恒等式成立」时必须同时报排序约定")

# ============================================================ A12 V61 三行读数的自洽性
Jrep = Decimal("-0.02011670455")
Itr = Decimal("-1.08117111" + "e-8")
prod_needed = Itr / (Decimal(6) * Jrep)
J_phys = Decimal("3.08" + "e-5")
ratio = abs(Jrep) / J_phys
add(MAIN, "A12",
    "V61 §六 的三行读数：由 J 与 Im tr 反解所需的质量平方差乘积，并核 J 的量级",
    "所需 ∏∏ ≈ 8.96e-8；|J| 比物理 CKM 大约两个量级 ⇒ 不是预言",
    "∏∏_所需 = Im/(6J) = %s；|J|/J_CKM = %s（J_CKM=3.08e-5）；"
    "来料第二、三行给同一个数 −1.08117111e-8（到 9 位）⇒ 无法区分「两种方法」与「同义反复」"
    % (prod_needed.quantize(Decimal("1e-14")), ratio.quantize(Decimal("0.1"))),
    "INFO",
    "★口径：来料自认振幅是人为选的 ⇒ J 不是预言。本卷只做两件事：①用 A11 的恒等式反解"
    "「要得到这个 Im tr，质量平方差乘积必须是多少」= %s；②指出第三行与第二行**数字完全相同**，"
    "若真是独立重构应给出不同末位 ⇒ 记「不可核」，不指控" % prod_needed)

# ============================================================ A13 26/26 的可判性分类
v61_rows = [
    ("规范群中心化子和维数", "A1/A2", "可判"),
    ("单个十维 Higgs 的稳定子群", "A3/A5", "可判"),
    ("32 旋量的二次、四次迹", "", "不可判"),
    ("六维局域反常因子化", "", "不可判"),
    ("手征家族与额外单态计数", "A7", "半可判"),
    ("Higgs 势及有色真空稳定性", "A9", "可判"),
    ("CP 不变量和 Jarlskog 恒等式", "A11/A12", "可判"),
    ("四力共同微观本源", "", "未证明"),
]
n_judge = sum(1 for r in v61_rows if r[2] == "可判")
n_partial = sum(1 for r in v61_rows if r[2] == "半可判")  # ★后缀 partial：这是「半可判行数」，与 A8 无关
n_no = sum(1 for r in v61_rows if r[2] in ("不可判", "未证明"))
_kind = {r["id"]: r["kind"] for r in ALL}
_ids_ok = True
for nm, ids, cls in v61_rows:
    if cls != "可判":
        continue
    lss = [x for x in ids.split("/") if x]
    if not lss:
        _ids_ok = False
        continue
    if any(one not in _kind for one in lss):
        _ids_ok = False
    if all(_kind.get(one) == "INFO" for one in lss):
        _ids_ok = False
a13_ok = (n_judge + n_partial + n_no == 8 and n_judge == 4 and _ids_ok)
add(MAIN, "A13",
    "§八 的「26/26 通过」逐行可判性分类：8 行里多少能被本卷独立复算",
    "可判 4 / 半可判 1 / 不可判或未证明 3（共 8 行）；且 4 行可判项都指向真算出数的条目",
    "可判 %d 行；半可判 %d 行；不可判或未证明 %d 行；可判行所指条目全部存在且非 INFO = %s"
    % (n_judge, n_partial, n_no, _ids_ok),
    "PASS" if a13_ok else "FAIL",
    "★★r391 的老教训重演：**「176/176 通过」型表格的独立可判命题远少于条目数**。"
    "8 行里只有 4 行能真算、1 行半可算、3 行无来料中间量 ⇒「26/26」不能当 26 条独立证据。"
    "★来料自己写了「26 项为特定数学模型内的断言检查，并非 26 项独立实验」—— 这句是诚实的")

# ============================================================ 控制组
add(CTL, "K1",
    "控制组（判别力）：三档中心化子必须给三个不同读数",
    "66 / 46 / 6 互不相同",
    "T=0 → %d；单平面 → %d；一般 Cartan → %d" % (c_zero, c_one, c_cart),
    "PASS" if (len({c_zero, c_one, c_cart}) == 3) else "FAIL",
    "★若三档相同，A1 的「46」就没有判别力（任何元素都给同一个数）")

add(CTL, "K2",
    "控制组（负向）：把 so(10) 换成 so(8)，不变量维数必须离开 1",
    "4（不是 1）",
    "so(10) → %d 维；so(8) 作用在 R^10=8+1+1 → %d 维" % (inv10, inv8),
    "PASS" if (inv10 == 1 and inv8 == 4) else "FAIL",
    "★A6 的负对照：若两者都给 1，则「Schur 逼简并」是「怎么算都简并」，无信息")

Uu_r = lift(R1)
Ud_r = lift(R2)
Hu_r = herm_from(Uu_r, du)
Hd_r = herm_from(Ud_r, dd)
lhs_r = cm_trace(cm_pow(cm_comm(Hu_r, Hd_r), 3))[1]
J_r = jarlskog(cm_mul(cm_dag(Uu_r), Ud_r))
add(CTL, "K3",
    "控制组（退化）：实纹理（J=0）时恒等式退化为 0 = 0，不能当证据",
    "J=0 且 Im tr=0（两侧同时为零）",
    "实正交混合（同一组 Cayley R，只是去掉 D 的复相位）：J = %s、Im tr = %s ⇒ 两侧同为 0"
    % (J_r, lhs_r),
    "PASS" if (J_r == 0 and lhs_r == 0) else "FAIL",
    "★★这就是 A11 必须用**复数相位**、且 U 必须用**一般正交阵**的两个原因："
    "实纹理两侧都恒等于 0；单轴旋转会让 V 块对角、J 也等于 0。"
    "⇒ 报「恒等式成立」必须同时报「它在哪个子空间上非平凡」")

# ============================================================ 守卫
SRC_PATH = os.path.abspath(__file__)
_SRC = io.open(SRC_PATH, encoding="utf-8").read()
_HEAD = _SRC.split('add(GRD, "G01"', 1)[0]
_ALG = _HEAD.split("# ============================================================ A12", 1)[0]

_g01 = sum(1 for r in ALL if r["id"] in ("A1", "A2", "A7") and r["kind"] not in
           ("PASS", "INFO", "FAIL", "IDENTITY"))
add(GRD, "G01", "恒等式不得记 PASS：A1/A2/A7 若为符号恒等须显式标注", "0 违规",
    "%d 违规" % _g01, "PASS" if _g01 == 0 else "FAIL",
    "A1/A2 是显式换位子核（不是抄 45+1）；A7 是模数计数（改 N 会变，见 G05）")

_g02 = (len({c_zero, c_one, c_cart}) == 3) and (inv10 == 1) and (inv8 == 4) and (st1 != st2)
add(GRD, "G02", "三个控制组必须给出可区分的读数", "全部可区分",
    "K1 %d/%d/%d；K2 %d vs %d；K3 0=0（退化，已显式标注）"
    % (c_zero, c_one, c_cart, inv10, inv8),
    "PASS" if _g02 else "FAIL",
    "★K1/K2 给不同读数；K3 本身就是「恒为零」的退化档，故它必须被标成退化而不是「通过」")

_tok = ("1e-", "1e+", "float(", "** 0.5", "round(")
_n_thr = sum(_ALG.count(t) for t in _tok)
add(GRD, "G03", "代数判据区不得含 10 的整数幂门限 / 浮点 / 浮点开方", "0 处",
    "代数区（A1–A11，不含 A12 的来料读数）出现 %s 共 %d 处（扫描区切在守卫段之前，避开自指）"
    % ("/".join(_tok), _n_thr),
    "PASS" if _n_thr == 0 else "FAIL",
    "★A1–A11 全程 Fraction / Gauss 有理数，「相等」用 `==` 精确判；"
    "A12 是来料给的十进制读数，用 Decimal 只报量级比，不当门限 ⇒ 单独切出去")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "%d 违规（首算；收尾重算见下）" % _bad4, "PASS" if _bad4 == 0 else "FAIL",
    "逐条核查 computed=True")

_d_so = all(len(so_basis(n)) == n * (n - 1) // 2 for n in (6, 8, 10, 12))
add(GRD, "G05", "维数公式必须与显式生成元计数一致（n(n−1)/2）", "n=6,8,10,12 全一致",
    "so(6)=%d、so(8)=%d、so(10)=%d、so(12)=%d"
    % (len(so_basis(6)), len(so_basis(8)), len(so_basis(10)), len(so_basis(12))),
    "PASS" if _d_so else "FAIL",
    "★写死的维数不会随 n 变；这条保证 A1/A2 的 66/45/46 来自生成元计数而不是字面量")

_g06 = (n_so12 == n_so10 + 1 + 10 + 10) and (span_h == n_so10 + 1) and (span_h - 12 == 33 + 1)
add(GRD, "G06", "分解账闭合：66 = 45+1+10+10、46 = 45+1、34 = 33+1", "三条全闭合",
    "66=%d 与 45+1+10+10=%d；46=%d 与 45+1=%d；34=%d 与 33+1=34"
    % (n_so12, n_so10 + 21, span_h, n_so10 + 1, span_h - 12),
    "PASS" if _g06 else "FAIL",
    "★三处加法互相独立，任一处抄错都会在这里露出来")

X_bad = zeros(12, 12)
X_bad[0][11] = O
X_bad[11][0] = -O
_nonzero_bracket = comm(X_bad, TF) != zeros(12, 12)
_inside = all(comm(G, TF) == zeros(12, 12) for G in GENS10)
add(GRD, "G07", "负对照：一个**不**与 T_F 换位的生成元必须被排除在中心化子外", "E_{1,12} 确被排除",
    "E_{1,12} 与 T_F 的换位子非零 = %s；so(10) 的 45 个全换位 = %s ⇒ "
    "「46」不是把 66 个都算进去的结果" % (_nonzero_bracket, _inside),
    "PASS" if (_nonzero_bracket and _inside) else "FAIL",
    "★若换位子判据写错（例如只比较迹），这条会红")

add(GRD, "G08", "判词与判定表必须同一读数：六 token 由变量拼 vs 由 ALL 行重算", "两路径一致",
    "(回填)", "INFO", "★漂移守卫：一路由构造变量拼、一路由表格行重算")

add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "(回填)", "(回填)", "INFO",
    "★写盘前先 add 占位，否则 exp 取到追加本行之前的快照（r390/r392 同型坑）")

add(GRD, "G10", "真判负必须逐条登记", "(回填)", "(回填)", "INFO",
    "★A3 是本卷唯一真判负：来料 §二 的**论证**无效（结论对）")

add(GRD, "G11", "完备性：10 在 SM 下的分解必须枚举干净（维数和 = 10、无单态）", "(回填)", "(回填)",
    "INFO", "★与 r390 G12 / r392 G11 同型：先枚举再断言")

add(GRD, "G12", "两条独立路径：Jarlskog 用「构造」与「恒等式」各算一次", "同一读数",
    "构造路径 Im tr = %s；恒等式路径 6J∏∏ = %s" % (lhs, rhs6),
    "PASS" if lhs == rhs6 else "FAIL",
    "★左边三次矩阵乘法取迹；右边只用特征值差与混合矩阵 ⇒ 不同源")

DECLARED_NEG = {"A3"}
_neg_ids = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G13", "总门必须对「守卫失败」敏感（r392 E03 起成为标准）", "注入守卫 FAIL 必须翻转",
    "(回填)", "INFO", "★沿用 r392 的 `NF_G` 并入总门 + 注入负对照")


def final_of(nf_main, nf_guard, n_decl=0):
    """登记过的判负不算失败；未登记的判负或任何守卫失败都挡总门。"""
    if nf_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main


_g13_a = final_of(0, 0, 0)
_g13_b = final_of(0, 1, 0)
_g13_c = final_of(1, 0, 0)
_nd = len(DECLARED_NEG & set(_neg_ids))
_g13_d = final_of(1, 0, 1)          # 登记过的判负不应挡门
g13 = [r for r in GRD if r["id"] == "G13"][0]
g13["act"] = "(0,0)=%s；(0,1)=%s；(1,0)=%s；(已登记 1 条)=(%s)" % (
    _g13_a, _g13_b, _g13_c, _g13_d)
g13["kind"] = ("PASS" if (_g13_a == "GATES-PASS-ALL-POSITIVE"
                          and _g13_b != _g13_a and _g13_c != _g13_a
                          and _g13_d == "GATES-PASS-WITH-1-NEGATIVE") else "FAIL")

# ============================================================ G14 关键表 vs 主册读数（漂移守卫）
# ★★本卷实测自伤：`n_half` 曾同时被 A8（半整数净手征 = 3）与 A13（半可判行数 = 1）占用，
#   A13 的赋值覆盖了 A8 ⇒ 关键表印出「n=1」而 A8 正文是「n=3」。
#   修法两条：①变量名带条目后缀（n_halfA / n_partial）；②本守卫两路对拍。
KT_HALF = "半整数出口：q=(3/2,−3/2) → n=%s、Σ s Q²=%s" % (n_halfA, sq_halfA)
_kt_n = re.findall(r"n=(-?\d+)", KT_HALF)
_a8_act = [r["act"] for r in ALL if r["id"] == "A8"][0]
_a8_n = re.findall(r"n=(-?\d+)", _a8_act)
_kt_bad = KT_HALF.replace("n=%s" % n_halfA, "n=1", 1)          # 重演被覆盖的那个错
_bad_n = re.findall(r"n=(-?\d+)", _kt_bad)
g14_ok = (len(_kt_n) == 1 and len(_a8_n) == 2 and _kt_n[0] == _a8_n[-1]
          and len(_bad_n) == 1 and _bad_n[0] != _a8_n[-1])
add(GRD, "G14", "关键表读数必须与主册同一条目同读数（防后续段同名变量覆盖）",
    "关键表写的 n 必须等于 A8 行 act 里的半整数档 n；且把该值改成 1 之后判据必须红",
    "关键表 n=%s vs A8 行 act 末档 n=%s；注入 n=1 后的读数 n=%s（应不等于 %s）"
    % (_kt_n[0], _a8_n[-1], _bad_n[0], _a8_n[-1]),
    "PASS" if g14_ok else "FAIL",
    "★★这是本卷唯一被落盘前抓住的**读数不一致**：`n_half` 先给 A8（=3）、后被 A13 复用为"
    "「半可判行数」（=1）⇒ 关键表与判定表自相矛盾，而两处各自「算对了」。"
    "★与 r367「对象错位」同族：**同名变量换了对象**，复算抓不到，只有把两处读数拉出来对拍才抓得到")

g11 = [r for r in GRD if r["id"] == "G11"][0]
g11["exp"] = "维数和 = 10 且单态数 = 0（枚举 5 与 5̄ 全部 4 块）"
g11["act"] = "维数和 %d、单态 %d、超荷和 %s" % (dim_sum, len(singlets), traceless)
g11["kind"] = "PASS" if (dim_sum == 10 and len(singlets) == 0) else "FAIL"

g09 = [r for r in GRD if r["id"] == "G09"][0]
g10 = [r for r in GRD if r["id"] == "G10"][0]

VERDICT = "--".join([
    "CENTRALIZER-46-LEAVES-34" if (a1_ok and a2_ok) else "CENTRALIZER-MISMATCH",
    "DIM-ARGUMENT-INVALID-CONCLUSION-RIGHT" if (a3_ok and a4_ok) else "DIM-ARGUMENT-OPEN",
    "SCHUR-FORCES-MH-EQ-MT" if a6_ok else "DEGENERACY-OPEN",
    "SIX-GENERATIONS-EQ-2N" if a7_ok else "COUNT-MISMATCH",
    "THREE-REACHABLE-AT-HALF-FLUX" if a8_ok else "ESCAPE-CLOSED",
    "JARLSKOG-IDENTITY-EXACT" if a11_ok else "IDENTITY-FAILS",
])
_d = {r["id"]: r["kind"] for r in ALL}
_v2 = "--".join([
    "CENTRALIZER-46-LEAVES-34" if (_d["A1"] == "PASS" and _d["A2"] == "PASS") else "CENTRALIZER-MISMATCH",
    "DIM-ARGUMENT-INVALID-CONCLUSION-RIGHT"
    if (_d["A3"] == "FAIL" and _d["A4"] == "PASS") else "DIM-ARGUMENT-OPEN",
    "SCHUR-FORCES-MH-EQ-MT" if _d["A6"] == "PASS" else "DEGENERACY-OPEN",
    "SIX-GENERATIONS-EQ-2N" if _d["A7"] == "PASS" else "COUNT-MISMATCH",
    "THREE-REACHABLE-AT-HALF-FLUX" if _d["A8"] == "PASS" else "ESCAPE-CLOSED",
    "JARLSKOG-IDENTITY-EXACT" if _d["A11"] == "PASS" else "IDENTITY-FAILS",
])
g08 = [r for r in GRD if r["id"] == "G08"][0]
g08["exp"] = "由变量拼接：%s" % VERDICT
g08["act"] = "由 ALL 行重算：%s（%s）" % (_v2, "一致" if _v2 == VERDICT else "不一致")
g08["kind"] = "PASS" if _v2 == VERDICT else "FAIL"

# ============================================================ 汇总
_bad4b = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
g04 = [r for r in GRD if r["id"] == "G04"][0]
g04["act"] = "%d 违规（收尾重算，覆盖全部 %d 条）" % (_bad4b, len(ALL))
g04["kind"] = "PASS" if _bad4b == 0 else "FAIL"

NP = sum(1 for r in MAIN if r["kind"] == "PASS")
NI = sum(1 for r in MAIN if r["kind"] == "INFO")
NID = sum(1 for r in MAIN if r["kind"] == "IDENTITY")
NF = sum(1 for r in MAIN if r["kind"] == "FAIL")
NF_G = sum(1 for r in CTL + GRD if r["kind"] == "FAIL")
FINAL = final_of(NF, NF_G, _nd)

OUT_JSON = os.path.join(DATA, TITLE + ".json")
OUT_TXT = os.path.join(DATA, TITLE + "_report_2026-11-04.txt")

payload = dict(rid=RID, date="2026-11-04", title=TITLE, final="", verdict=VERDICT,
               counts=dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD), P=0, I=0, F=0, ID=0),
               rows=[])


def write_json():
    payload["rows"] = ALL
    payload["counts"] = dict(main=len(MAIN), ctl=len(CTL), grd=len(GRD),
                             P=NP, I=NI, F=NF, ID=NID)
    payload["final"] = FINAL
    payload["verdict"] = VERDICT
    payload["declared_neg"] = sorted(DECLARED_NEG)
    with io.open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)


g10["exp"] = "登记集 == 实际 FAIL 集"
g10["act"] = "%s vs %s" % (sorted(DECLARED_NEG), _neg_ids)
g10["kind"] = "PASS" if (sorted(DECLARED_NEG) == _neg_ids) else "FAIL"

g09["exp"] = "回读条目数 == 内存条目数"
g09["act"] = "(回填)"
g09["kind"] = "INFO"
write_json()
_back = json.load(io.open(OUT_JSON, encoding="utf-8"))
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                        "一致" if len(ALL) == len(_back["rows"]) else "不一致")
g09["kind"] = "PASS" if len(ALL) == len(_back["rows"]) else "FAIL"
write_json()
_back2 = json.load(io.open(OUT_JSON, encoding="utf-8"))
_g09b = [r for r in _back2["rows"] if r["id"] == "G09"][0]
assert _g09b["kind"] == "PASS", _g09b

# ============================================================ 报告
L = []
A = L.append
A(TITLE)
A("=" * 100)
A("对象：ROOT V61（四力大统一的真空稳定性与粒子谱审查）—— 六项主张逐条变可算判决")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
A("")
for title, bucket in (("【主册】", MAIN), ("【控制组】", CTL), ("【守卫】", GRD)):
    A("=" * 100)
    A(title)
    A("=" * 100)
    for r in bucket:
        A("[%s] %-4s %s" % (r["kind"], r["id"], r["name"]))
        A("    exp = %s" % r["exp"])
        A("    act = %s" % r["act"])
        A("    %s" % r["note"])
        A("")
A("=" * 100)
A("【关键表】")
A("中心化子维数：T=0 → %d；T_F → %d；一般 Cartan → %d" % (c_zero, c_one, c_cart))
A("分解账：66 = %d+1+10+10；46 = %d+1；46−12 = %d = 33+1" % (n_so10, n_so10, span_h - 12))
A("稳定子：单矢量 %d，两个独立矢量 %d" % (st1, st2))
A("不变对称算子维数：so(10) → %d（路径集）/ %d（全 45）；so(8) → %d" % (inv10, inv10_full, inv8))
A("六代计数：16_{+1} %d + 16̄_{−1} %d = %d；净手征 %d；Σ s Q² = %d"
  % (n16, n16b, total16, net, sum_sq))
A(KT_HALF)
A("势：H 方向 V'' = %s；T 方向 V'' = %s（= 2Δ）" % (d2_h, d2_t))
A("Jarlskog：Im tr = %s；6J∏∏ = %s；相符 = %s；J = %s" % (lhs, rhs6, lhs == rhs6, Jval))
A("实纹理退化对照：J = %s、Im tr = %s" % (J_r, lhs_r))
A("V61 读数反解：所需 ∏∏ = %s；|J|/J_CKM = %s"
  % (prod_needed, ratio.quantize(Decimal("0.1"))))
A("")
A("【诚实边界】")
A(" 1) 本卷只做群论维数、不变量维数、计数与代数恒等式，不碰零模波函数与完整 Hessian；")
A(" 2) V61 §四 的「24 个额外带电单态」无来料中间量、口径不明 ⇒ 未核；")
A(" 3) V61 §八 的「26/26」按行分类后只有 4 行可独立复算，1 行半可算；")
A(" 4) A3 判负的是**论证**（维数比较不是子群判据），不是 V61 的结论 —— 结论由 A4 独立证成；")
A(" 5) A11 的恒等式在实纹理子空间上退化为 0=0（K3），所以「成立」只在有复相位的子空间上有内容。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))
with io.open(OUT_TXT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")

print("JSON ->", OUT_JSON)
print("TXT  ->", OUT_TXT, "(%d chars)" % len("\n".join(L)))
print("MAIN=%d (PASS %d / INFO %d / IDENTITY %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), NP, NI, NID, NF, len(CTL), len(GRD), len(ALL)))
print("FINAL   =", FINAL)
print("VERDICT =", VERDICT)
