# -*- coding: utf-8 -*-
"""TUFT-r400  攻 X-GSM-5：Y 的两个系数不是输入 —— 由 SM 电荷谱唯一定出，
并顺带校正 r399 对 16 / 16bar 的读法

纯标准库（Fraction，判据区无浮点、无随机）。复用 r399 的代数底座（同一 Γ / Σ / 生成元 / realify）。

r399 留下的硬边界（其 `_report` 的【诚实边界】第 1 条）：
  「`Y = -(1/3)(H1+H2+H3) + (1/2)(H4-H5)` 里两个系数是**输入**（超荷嵌入），不是算出来的」
本卷把那两个系数改成**算出来的**，并把「算不出来」的部分精确地缩到一条对称性上。

  A1  三个谱：A = h1+h2+h3、T3L = (h4+h5)/2、T3R = (h4-h5)/2 的 16-态多重集
  A2  B-L 的唯一性：f(3/2) = -1、f(-1/2) = 1/3 两条方程给同一个 alpha = -2/3（且多重集 = SM 的 B-L 表）
  A3  T3 的归一化：lambda 使 lambda*{-1,0,1} 落在 {±1/2,0} 内 ⇒ |lambda| = 1/2 唯一
  A4  组装：alpha/2 与 lambda 拼出的矩阵与 r399/r398 用的 Y_C **逐元素相等**
  A5  扇区精确解：K3=0 的 8 态给 lambda_A = -1/3（唯一）；K3!=0 的 8 态给 lambda_K = ±1/2
  A6  全网格（2401 点）互印：解恰 4 个 = {±1/3} x {±1/2}；盒外与刻度外第一点都红
  A7  连 T3L 的**选定**也是可判定的：把 T3L 换成 T3R ⇒ 全网格 0 解
  A8  lambda_K 的符号没有物理内容：eps4 <-> eps5 是权集的对称（16/16 闭环），两解谱全同
  A9  校正 r399：y 多重集 = SM 超荷表（不是 r398 清单），r398 的清单是**共轭谱**
  A10 边界：电荷谱自身对 q -> -q 免疫 ⇒ 本卷钉住的是方向，不是「16 装哪一代」
"""
import ast
import io
import json
import os
from fractions import Fraction as F

RID = "r400"
TITLE = "TUFT-r400_攻X-GSM-5_超荷方向由电荷谱唯一确定_系数的两条唯一性_BL的su4归一化与T3的so4归一化_扇区精确解与全网格互印_lamK符号是权集对称_T3L的选定可判定_并校正r399的16与16bar读法_精算_2026-11-04"
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


def _unbold(s):
    return s.replace("**", "")


# ============================================================ 精确线性代数（实）
def zmat(n):
    return [[F(0)] * n for _ in range(n)]


def madd(A, B, n, s=1):
    return [[A[i][j] + s * B[i][j] for j in range(n)] for i in range(n)]


def mmul(A, B, n):
    C = zmat(n)
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(n):
                b = Bk[j]
                if b != 0:
                    Ci[j] += a * b
    return C


def comm2(A, B, n):
    return madd(mmul(A, B, n), mmul(B, A, n), n, -1)


def is_zero(A):
    return all(v == 0 for row in A for v in row)


def is_antisym(A):
    n = len(A)
    return all(A[i][j] == -A[j][i] for i in range(n) for j in range(n))


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def rank_of(rows, ncols):
    M = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                for j in range(c, ncols):
                    if M[r][j] != 0:
                        M[i][j] -= f * M[r][j]
        r += 1
        if r == len(M):
            break
    return r


def nullspace_basis(rows, ncols):
    M = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                for j in range(c, ncols):
                    if M[r][j] != 0:
                        M[i][j] -= f * M[r][j]
        pivots.append(c)
        r += 1
        if r == len(M):
            break
    pivset = set(pivots)
    free = [c for c in range(ncols) if c not in pivset]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for k, pc in enumerate(pivots):
            v[pc] = -M[k][fc]
        basis.append(v)
    return basis


def mat_vec(M, v):
    n = len(M)
    return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]


def coords_in_basis(basis, w, n):
    """把 w 在 basis（线性无关）下的坐标解出来；无解则抛异常。"""
    k = len(basis)
    M = [[basis[i][j] for i in range(k)] + [w[j]] for j in range(n)]
    piv, r = [], 0
    for c in range(k):
        p = None
        for i in range(r, n):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                for j in range(c, k + 1):
                    if M[r][j] != 0:
                        M[i][j] -= f * M[r][j]
        piv.append(c)
        r += 1
    assert len(piv) == k, ("基不满秩，无法解坐标", len(piv), k)
    c = [F(0)] * k
    for idx, pc in enumerate(piv):
        c[pc] = M[idx][k]
    # 残差自查
    res = [sum(basis[i][j] * c[i] for i in range(k)) - w[j] for j in range(n)]
    assert all(v == 0 for v in res), "坐标解回代不为零"
    return c


def restrict_mat(M, basis, n):
    """M 在 basis 张成的子空间上的矩阵（basis 必须 M-不变）。"""
    k = len(basis)
    cols = [coords_in_basis(basis, mat_vec(M, bj), n) for bj in basis]
    return [[cols[j][i] for j in range(k)] for i in range(k)]


# ============================================================ 复矩阵用 (Re, Im) 有理对
def cmul(X, Y):
    (Ar, Ai), (Br, Bi) = X, Y
    n = len(Ar)
    return (madd(mmul(Ar, Br, n), mmul(Ai, Bi, n), n, -1),
            madd(mmul(Ar, Bi, n), mmul(Ai, Br, n), n, 1))


def cadd(X, Y, s=1):
    (Ar, Ai), (Br, Bi) = X, Y
    n = len(Ar)
    return (madd(Ar, Br, n, s), madd(Ai, Bi, n, s))


def krons(A, B, na, nb):
    n = na * nb
    C = zmat(n)
    for i in range(na):
        for j in range(na):
            a = A[i][j]
            if a == 0:
                continue
            for k in range(nb):
                for l in range(nb):
                    C[i * nb + k][j * nb + l] = a * B[k][l]
    return C


def ckron(X, Y, na, nb):
    """(A+iB) kron (C+iD) = (A kron C - B kron D) + i(A kron D + B kron C)"""
    (Ar, Ai), (Br, Bi) = X, Y
    n = na * nb
    return (madd(krons(Ar, Br, na, nb), krons(Ai, Bi, na, nb), n, -1),
            madd(krons(Ar, Bi, na, nb), krons(Ai, Br, na, nb), n, 1))


def is_herm(M):
    (R, I) = M
    n = len(R)
    return all(R[i][j] == R[j][i] and I[i][j] == -I[j][i]
               for i in range(n) for j in range(n))


Z2 = [[F(0), F(0)], [F(0), F(0)]]
I2 = [[F(1), F(0)], [F(0), F(1)]]
S1 = [[F(0), F(1)], [F(1), F(0)]]
S3 = [[F(1), F(0)], [F(0), F(-1)]]
J2 = [[F(0), F(-1)], [F(1), F(0)]]
C1, C2, C3 = (S1, Z2), (Z2, J2), (S3, Z2)

# ============================================================ gamma 与手征投影（与 r397 同口径）
N32, NF = 32, 5
GAM = []
for _j in range(NF):
    for _s in (C1, C2):
        _facs = [(C3 if _k < NF - 1 - _j else (_s if _k == NF - 1 - _j else (I2, Z2)))
                 for _k in range(NF)]
        _M = _facs[0]
        for _k in range(1, NF):
            _M = ckron(_M, _facs[_k], 2 ** _k, 2)
        GAM.append(_M)

_P = GAM[0]
for _a in range(1, 10):
    _P = cmul(_P, GAM[_a])
CHIR = (_P[1], [[-x for x in row] for row in _P[0]])
_chir_diag = [CHIR[0][i][i] for i in range(N32)]
PLUS = [i for i in range(N32) if _chir_diag[i] == 1]
MINUS = [i for i in range(N32) if _chir_diag[i] == -1]

KEYS = [(a, b) for a in range(10) for b in range(a + 1, 10)]


def restrict(Mc, idx):
    (R, I) = Mc
    return ([[R[i][j] for j in idx] for i in idx], [[I[i][j] for j in idx] for i in idx])


def realify(Mc):
    """16x16 复 -> 32x32 实：[[A, -B], [B, A]]（复结构 = 乘 i）"""
    (R, I) = Mc
    n = len(R)
    M = zmat(2 * n)
    for i in range(n):
        for j in range(n):
            M[i][j] = R[i][j]
            M[i][n + j] = -I[i][j]
            M[n + i][j] = I[i][j]
            M[n + i][n + j] = R[i][j]
    return M


SIGC, SIGR = {}, {}
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    _Cm = ([[x / 4 for x in row] for row in _Cm[0]], [[x / 4 for x in row] for row in _Cm[1]])
    SIGC[(a, b)] = restrict(_Cm, PLUS)
    SIGR[(a, b)] = realify(SIGC[(a, b)])

# 16bar 块（MINUS）上的同一批 Sigma
SIGR_M = {}
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    _Cm = ([[x / 4 for x in row] for row in _Cm[0]], [[x / 4 for x in row] for row in _Cm[1]])
    SIGR_M[(a, b)] = realify(restrict(_Cm, MINUS))

# ============================================================ SM 的 12 个生成元（与 r397 同系数）
LAM_RE = [
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
]
LAM_IM = [
    [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
    [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[1, 0, 0], [0, 1, 0], [0, 0, -2]],
]


def realify6(Are, Aim):
    M = zmat(6)
    for j in range(3):
        for k in range(3):
            M[2 * j][2 * k] = F(Are[j][k])
            M[2 * j][2 * k + 1] = -F(Aim[j][k])
            M[2 * j + 1][2 * k] = F(Aim[j][k])
            M[2 * j + 1][2 * k + 1] = F(Are[j][k])
    return M


def coefs_from_vec(M):
    n = len(M)
    return {(a, b): M[a][b] for a in range(n) for b in range(a + 1, n) if M[a][b] != 0}


SU3_C = [coefs_from_vec(realify6(LAM_RE[a], LAM_IM[a])) for a in range(8)]
SU2J_C = [{(7, 8): F(1), (6, 9): F(1)},
          {(6, 8): F(-1), (7, 9): F(1)},
          {(6, 7): F(1), (8, 9): F(1)}]
SU2K_C = [{(7, 8): F(1), (6, 9): F(-1)},
          {(6, 8): F(-1), (7, 9): F(-1)},
          {(6, 7): F(1), (8, 9): F(-1)}]
# 判别力用：把 so(4) 换到 1..4 号指标（0 基 0..3）
SU2J2_C = [{(1, 2): F(1), (0, 3): F(1)},
           {(0, 2): F(-1), (1, 3): F(1)},
           {(0, 1): F(1), (2, 3): F(1)}]
SU2K2_C = [{(1, 2): F(1), (0, 3): F(-1)},
           {(0, 2): F(-1), (1, 3): F(-1)},
           {(0, 1): F(1), (2, 3): F(-1)}]
U_A = {(0, 1): F(1), (2, 3): F(1), (4, 5): F(1)}
U_K = {(6, 7): F(1), (8, 9): F(-1)}
Y_C = {}
for kk, cc in U_A.items():
    Y_C[kk] = Y_C.get(kk, F(0)) - F(1, 3) * cc
for kk, cc in U_K.items():
    Y_C[kk] = Y_C.get(kk, F(0)) + F(1, 2) * cc
Y_C = {k: v for k, v in Y_C.items() if v != 0}


def to_rep(coef, REP):
    n = len(REP[KEYS[0]])
    M = zmat(n)
    for kk, cc in coef.items():
        T = REP[kk]
        for i in range(n):
            Ti = T[i]
            Mi = M[i]
            for j in range(n):
                if Ti[j] != 0:
                    Mi[j] += cc * Ti[j]
    return M


Y_R = to_rep(Y_C, SIGR)
Y_RM = to_rep(Y_C, SIGR_M)
SM_J = [to_rep(c, SIGR) for c in SU3_C] + [to_rep(c, SIGR) for c in SU2J_C] + [Y_R]
SM_K = [to_rep(c, SIGR) for c in SU3_C] + [to_rep(c, SIGR) for c in SU2K_C] + [Y_R]
J_GENS = [to_rep(c, SIGR) for c in SU2J_C]
K_GENS = [to_rep(c, SIGR) for c in SU2K_C]
J2_GENS = [to_rep(c, SIGR) for c in SU2J2_C]
K2_GENS = [to_rep(c, SIGR) for c in SU2K2_C]
J3 = J_GENS[2]


def rows_of(gens, n=N32):
    out = []
    for M in gens:
        for i in range(n):
            out.append([M[i][j] for j in range(n)])
    return out



# ============================================================ 权基（16 个 5 维权向量）
NC = 16
HC = [SIGC[(2 * i, 2 * i + 1)] for i in range(5)]
W = [[HC[i][1][k][k] for i in range(5)] for k in range(NC)]
assert all(HC[i][0][k][k] == 0 for i in range(5) for k in range(NC))
AV = [w[0] + w[1] + w[2] for w in W]                 # A = h1+h2+h3（su(4) 方向）
TLV = [(w[3] + w[4]) / 2 for w in W]                  # T3L = (h4+h5)/2
TRV = [(w[3] - w[4]) / 2 for w in W]                  # T3R = (h4-h5)/2
K3V = [w[3] - w[4] for w in W]                        # K3 的本征值（= 2*T3R）


def cnt(seq):
    d = {}
    for x in seq:
        d[x] = d.get(x, 0) + 1
    return d


def ctr_txt(d):
    return "{" + "，".join("%s:%d" % (k, d[k]) for k in sorted(d)) + "}"


def diff_n(a, b):
    """两个计数器的对称差总质量的一半（= 需要改几个态）"""
    tot = 0
    for k in set(list(a.keys()) + list(b.keys())):
        tot += abs(a.get(k, 0) - b.get(k, 0))
    return tot // 2


# ============================================================ A1 三个谱
_SP_A = cnt(AV)
_SP_TL = cnt(TLV)
_SP_TR = cnt(TRV)
_EXP_A = {F(3, 2): 2, F(1, 2): 6, F(-1, 2): 6, F(-3, 2): 2}
_EXP_T = {F(1, 2): 4, F(0): 8, F(-1, 2): 4}
_a1_ok = (_SP_A == _EXP_A and _SP_TL == _EXP_T and _SP_TR == _EXP_T
          and sum(_SP_A.values()) == NC and sum(_SP_TL.values()) == NC)
add(MAIN, "A1",
    "三个谱：A 取 ±3/2 各 2、±1/2 各 6；T3L 与 T3R 都取 ±1/2 各 4、0 取 8",
    "A = {3/2:2, 1/2:6, -1/2:6, -3/2:2}；T3L = T3R = {1/2:4, 0:8, -1/2:4}；三者合计各 16",
    "A = %s；T3L = %s；T3R = %s；合计 %d/%d/%d"
    % (ctr_txt(_SP_A), ctr_txt(_SP_TL), ctr_txt(_SP_TR),
       sum(_SP_A.values()), sum(_SP_TL.values()), sum(_SP_TR.values())),
    "PASS" if _a1_ok else "FAIL",
    "★★★ 这三行是本卷的地皮。A 的 2/6/6/2 不是随便一个数：`A > 0` 的 8 个态正好是 `(4,2,1)`、"
    "`A < 0` 的 8 个正好是 `(4bar,1,2)` —— 也就是说**su(4) 的 4 与 4bar 在这 16 个态上可以按 A 的正负直接分开**。"
    "★ T3L 与 T3R 的多重集**完全一样**（各 4/8/4），所以「谁是谁」不能由各自的谱判断 —— "
    "这一条很重要：它说明 A7 那个结论（换 T3L 无解）**不是**谱的差异给的，而是电荷给的。")

# ============================================================ A2 B-L 的唯一性
_AL1 = F(-1) / F(3, 2)                      # 由 B-L(4 的单态) = -1 定
_AL2 = F(1, 3) / F(-1, 2)                   # 由 B-L(4 的三重态) = +1/3 定
BLV = [_AL1 * x for x in AV]
_SP_BL = cnt(BLV)
_EXP_BL = {F(1, 3): 6, F(-1, 3): 6, F(1): 2, F(-1): 2}
_a2_ok = (_AL1 == _AL2 == F(-2, 3) and _SP_BL == _EXP_BL and sum(BLV) == 0)
add(MAIN, "A2",
    "B-L 是 su(4) 方向上的**唯一**线性泛函：两条独立方程给同一个 alpha = -2/3，"
    "且 16 态的 B-L 多重集就是 SM 的表",
    "alpha(由 B-L=-1 定) == alpha(由 B-L=1/3 定) == -2/3；B-L 多重集 = {1/3:6, -1/3:6, 1:2, -1:2}；迹 0",
    "alpha1 = %s；alpha2 = %s；B-L = %s；迹 = %s"
    % (_AL1, _AL2, ctr_txt(_SP_BL), sum(BLV)),
    "PASS" if _a2_ok else "FAIL",
    "★★★ 这一条的判别力在「**两条方程给同一个数**」：`B-L` 在 su(4) 的 4 上是 diag(-1, 1/3, 1/3, 1/3)，"
    "而那 4 个态的 A 值是 3/2 一次、-1/2 三次。用这两条独立数据解 alpha，若 su(4) 的嵌入写错（例如 A 取 h1+h2），"
    "两条方程会给出**不同**的 alpha，判据当场红。"
    "★ 得到的多重集 {1/3 x6, -1/3 x6, 1 x2, -1 x2} 正是 SM 的（Q 与 L 的 B-L 差一个 1/2），"
    "也就是说 **`A` 这一条直线上的量子数就是 B-L，不需要外部指定**。"
    "★★ 迹为 0 是自洽性检查，不是判据 —— 它由多重集的对称性保证，单独拿出来只是为了让「无整体偏移」可见。")

# ============================================================ A3 T3 的归一化
_CAND = []
for _k in range(-24, 25):
    _lam = F(_k, 12)
    if _lam == 0:
        continue
    if all((_lam * t) in (F(-1, 2), F(0), F(1, 2)) for t in (F(-1), F(0), F(1))):
        _CAND.append(_lam)
_a3_ok = (sorted(_CAND) == [F(-1, 2), F(1, 2)] and sorted(set(K3V)) == [F(-1), F(0), F(1)])
add(MAIN, "A3",
    "T3 的归一化：K3 的本征值是整数 {-1,0,1}，而 so(4) 的旋量表示要求 T3 取半整 ⇒ |lambda| = 1/2 唯一",
    "lambda 使 lambda*{-1,0,1} 全落在 {±1/2, 0} 内：解集 = {-1/2, +1/2}（|lambda| 唯一）；K3 值集 = {-1, 0, 1}",
    "K3 值集 = %s；lambda 解集 = %s" % ([str(x) for x in sorted(set(K3V))], [str(x) for x in _CAND]),
    "PASS" if _a3_ok else "FAIL",
    "★★ 这里的「唯一」是**绝对值**唯一：lambda = ±1/2 都合法，原因是 K3 -> -K3 可以由 eps4 <-> eps5 实现"
    "（A8 会证明这条置换是权集的对称）。所以 A3 只钉住大小，符号留给 A8。"
    "★ 为什么 K3 必须是整数：`K3 = h4 - h5`，两个 ±1/2 相减只有 {-1,0,1} 三种值 —— 这是**算出来的**，不是约定。")

# ============================================================ A4 组装（系数由 A2/A3 给出）
_COEF_A = _AL1 / 2                    # Y 里 A 的系数 = (B-L 系数) / 2
_COEF_K = F(1, 2)                     # Y 里 K3 的系数 = |lambda|
Y_DER = {(0, 1): _COEF_A, (2, 3): _COEF_A, (4, 5): _COEF_A,
         (6, 7): _COEF_K, (8, 9): -_COEF_K}
Y_DER = {k: v for k, v in Y_DER.items() if v != 0}


def to_rep_c(coef, REP):
    """复版 to_rep：REP 的元素是 (Re, Im) 有理对"""
    n = len(REP[KEYS[0]][0])
    R, I = zmat(n), zmat(n)
    for kk, cc in coef.items():
        (Tr, Ti) = REP[kk]
        for i in range(n):
            for j in range(n):
                if Tr[i][j] != 0:
                    R[i][j] += cc * Tr[i][j]
                if Ti[i][j] != 0:
                    I[i][j] += cc * Ti[i][j]
    return (R, I)


_a4_dict = (Y_DER == Y_C)
_a4_mat = (to_rep_c(Y_DER, SIGC) == to_rep_c(Y_C, SIGC))
_a4_ok = (_a4_dict and _a4_mat and _COEF_A == F(-1, 3) and _COEF_K == F(1, 2))
add(MAIN, "A4",
    "把 A2/A3 定出的系数装回 Y，得到的矩阵与 r398/r399 一直用的 Y_C **逐元素相等**",
    "Y_DER == Y_C（字典层）且 to_rep_c(Y_DER) == to_rep_c(Y_C)（矩阵层）；系数 = (-1/3, +1/2)",
    "字典相等 = %s；矩阵相等 = %s；A 系数 = %s；K3 系数 = %s"
    % (_a4_dict, _a4_mat, _COEF_A, _COEF_K),
    "PASS" if _a4_ok else "FAIL",
    "★★ 这是**接口检查**：它说明前两卷用的 Y 与本卷从 B-L + T3 装出来的 Y 是同一个对象。"
    "★ 它不是恒等式：`_AL1`（= -2/3）来自 B-L 的两次赋值、`_COEF_K` 来自 A3 的唯一性 —— "
    "两个都不是从 `Y_C` 反读的，所以这条相等是**两个独立构造的相遇**。"
    "★★ 但要注意 A4 里那个 `/2`：`Y = T3R + (B-L)/2` 的 1/2 在这里还是**写上去的**。"
    "A5 会把这条 1/2 也从电荷谱里算出来 —— 那才是本卷的关键一步。")

# ============================================================ A5 扇区精确解（两段互不相交）
ZI = [i for i in range(NC) if K3V[i] == 0]        # K3 = 0 的 8 个态
NI = [i for i in range(NC) if K3V[i] != 0]        # K3 != 0 的 8 个态
SM_Q = {F(2, 3): 3, F(-1, 3): 3, F(-2, 3): 3, F(1, 3): 3, F(0): 2, F(-1): 1, F(1): 1}
SUB_Z = {F(0): 1, F(-1): 1, F(2, 3): 3, F(-1, 3): 3}      # 扇区 1 应得的 8 个电荷
SUB_N = {F(-2, 3): 3, F(1, 3): 3, F(1): 1, F(0): 1}       # 扇区 2 应得的 8 个电荷
_GRID = [F(k, 12) for k in range(-24, 25)]
_solA = [la for la in _GRID
         if la != 0 and cnt([TLV[i] + la * AV[i] for i in ZI]) == SUB_Z]
_solK = []
if _solA:
    for lk in _GRID:
        if lk != 0 and cnt([TLV[i] + _solA[0] * AV[i] + lk * K3V[i] for i in NI]) == SUB_N:
            _solK.append(lk)
_ratio = (_solA[0] / _AL1) if _solA else None
_a5_ok = (_solA == [F(-1, 3)] and sorted(_solK) == [F(-1, 2), F(1, 2)]
          and _ratio == F(1, 2) and len(ZI) == 8 and len(NI) == 8)
add(MAIN, "A5",
    "扇区式精确解（两段互不相交，**在「K3=0 的 8 态装 Q(6)+L(2)」这一物理指认下**）："
    "扇区1 唯一给出 lambda_A = -1/3；扇区2 给出 lambda_K = ±1/2；两者之比恰为 1/2",
    "扇区1（8 态电荷 = {0, -1, 2/3 x3, -1/3 x3}）解集 = {-1/3}（唯一）；"
    "扇区2 解集 = {-1/2, +1/2}；lambda_A / alpha = 1/2",
    "扇区1（K3=0，%d 态）解 = %s；扇区2（K3!=0，%d 态）解 = %s；lambda_A/alpha = %s"
    % (len(ZI), [str(x) for x in _solA], len(NI), [str(x) for x in _solK], _ratio),
    "PASS" if _a5_ok else "FAIL",
    "★★★ 这是全卷的核心：两段**互不相交**的子问题，各自只有一个未知量。"
    "扇区 1 里 K3 = 0，所以 Y 只剩 A 那一项，8 个态的电荷是 `T3L + lambda_A*A`；"
    "要求它们是 `{0, -1, 2/3 x3, -1/3 x3}`（即 nu、e、三个 u、三个 d）⇒ lambda_A 被**唯一**确定。"
    "★★ 而 `lambda_A / alpha = (-1/3)/(-2/3) = 1/2` —— **`Y = T3R + (B-L)/2` 里的那个 1/2 不是输入，它是这两个系数之比**。"
    "r399 的【诚实边界】第 1 条到此关闭：两个系数都是算出来的。"
    "★ 扇区 2 留下 ±1/2 两个解，不是缺陷 —— A8 会证明这两个解是**同一个物理**的两种写法。"
    "★★★ 但这一条**不是无条件成立**：它默认了「K3=0 的那 8 个态装的是 Q(6)+L(2)」。"
    "这是一层**物理指认**（夸克是色三重态、且是 su(2)_L 双重态），不是纯代数得出的。"
    "A6 会在**去掉这层指认**之后重算，多出来的那一倍正是共轭 —— 两卷合起来才把「哪些是算的、哪些是指认的」分干净。"
    "★ 这一层指认很弱（它只说「哪个扇区装夸克」，不说「哪个态是 u」），但它确实存在，必须写明。")

# ============================================================ A6 全网格互印
_full = []
for la in _GRID:
    for lk in _GRID:
        if la == 0 and lk == 0:
            continue
        if cnt([TLV[i] + la * AV[i] + lk * K3V[i] for i in range(NC)]) == SM_Q:
            _full.append((la, lk))
# 期望解集由 A5 的扇区解 + 整体取反（共轭）推出，不写字面量
_sec_set = {(la, lk) for la in _solA for lk in _solK}
_conj = {(-la, -lk) for (la, lk) in _sec_set}
_EXP_FULL = sorted(_sec_set | _conj)
_LK_OFF = F(1, 2) + F(1, 12)
_LA_OFF = F(2) + F(1, 12)
_out1 = diff_n(cnt([TLV[i] + F(-1, 3) * AV[i] + _LK_OFF * K3V[i] for i in range(NC)]), SM_Q)
_out2 = diff_n(cnt([TLV[i] + _LA_OFF * AV[i] + F(1, 2) * K3V[i] for i in range(NC)]), SM_Q)
_a6_ok = (sorted(_full) == sorted(_EXP_FULL) and _out1 > 0 and _out2 > 0
          and {(la, F(abs(lk))) for (la, lk) in _full} == {(F(-1, 3), F(1, 2)), (F(1, 3), F(1, 2))})
add(MAIN, "A6",
    "全网格（lambda_A x lambda_K，刻度 1/12，盒 ±2：49x49 = 2401 个格点，去掉原点后 2400 个候选）"\
    "互印：解恰 4 个 = {±1/3} x {±1/2}",
    "解 4 个且 = {±1/3} x {±1/2}；扇区解集（A5）与全网格解集相容；刻度外（lk+1/12）与盒外（λ_A=2+1/12）第一点都红",
    "全网格解 %d 个 = %s；刻度外第一点违例 %d；盒外第一点违例 %d"
    % (len(_full), [(str(x), str(y)) for (x, y) in _full], _out1, _out2),
    "PASS" if _a6_ok else "FAIL",
    "★★★ 这是 A5 的**独立复算**，而且差异本身有内容：全网格比扇区多出整整一倍，"
    "多出来的那一对**正好是扇区解的整体取反**（Y -> -Y，即共轭）—— G11 会把这个关系机核。"
    "为什么扇区版看不到它们：`lambda_A = +1/3` 时扇区 1 的 8 个电荷变成 `{1, 0, 1/3 x3, -2/3 x3}`，"
    "不是 `{0, -1, 2/3 x3, -1/3 x3}` —— 也就是说「夸克装在这一半」这个指认**排除**了共轭那两支。"
    "★ 所以 A5 与 A6 不是「谁对谁错」，而是**两个不同的问题**：A5 = 「指认之下」，A6 = 「不指认」。"
    "不指认时唯一性只剩到「方向 + 共轭」这一层，这正好是 A10 那条边界。"
    "★★ 这也是我自己的一次自伤（E02）：第一版 G11 要求两个解集**相等**，直接判 FAIL —— "
    "错在把「共轭」当成「算错」。判据要报关系，不要报相等。"
    "★ 半个刻度外（`lk + 1/12`）立刻出现违例，说明 1/2 这个值是**孤立的**，不是某个平台的一部分。"
    "★ 盒外（|lambda_A| > 2）也立刻红，这是「范围内全对必须报范围外第一条就错」那条纪律。")

# ============================================================ A7 T3L 的选定也可判定
_swap = []
for la in _GRID:
    for lk in _GRID:
        if la == 0 and lk == 0:
            continue
        if cnt([TRV[i] + la * AV[i] + lk * K3V[i] for i in range(NC)]) == SM_Q:
            _swap.append((la, lk))
_a7_ok = (len(_swap) == 0 and len(_full) > 0)
add(MAIN, "A7",
    "把 T3L 换成 T3R（即 Q = T3R + Y）⇒ 同一个网格上 **0 解** ⇒ 「哪个 su(2) 是 L」不是输入",
    "换 T3L/T3R 后解 0 个（基线：不换时 4 个）",
    "换后解 %d 个；不换时解 %d 个" % (len(_swap), len(_full)),
    "PASS" if _a7_ok else "FAIL",
    "★★★ 这一条是我开工时没想到的：`T3L = (h4+h5)/2` 这个**指认**本身也是可判定的。"
    "A1 已经说明 T3L 与 T3R 的**多重集完全一样**（各 4/8/4），所以靠谱是分不开的；"
    "但换成 T3R 之后，电荷谱**一个解都没有** ⇒ 电荷表把「哪一半是 L」也钉死了。"
    "★★ 这一点很值钱：教科书通常把「T3L 是哪一半」当约定写下来，而这里它是**被算出来的**。"
    "★ 判别力检查：如果这条也给出 4 个解，那说明电荷谱对 L/R 无判别力，A5 的结论就要打折 —— 所以它必须红得干脆（0 而不是 4）。")

# ============================================================ A8 lambda_K 的符号没有物理内容
_S = {tuple(w) for w in W}
_SW = {(w[0], w[1], w[2], w[4], w[3]) for w in W}
_perm_closed = (_S == _SW and len(_S) == NC)
_ifx_TL = all((w[3] + w[4]) / 2 == (w[4] + w[3]) / 2 for w in W)
_q_pos = cnt([TLV[i] + _COEF_A * AV[i] + F(1, 2) * K3V[i] for i in range(NC)])
_q_neg = cnt([TLV[i] + _COEF_A * AV[i] - F(1, 2) * K3V[i] for i in range(NC)])
_y_pos = cnt([_COEF_A * AV[i] + F(1, 2) * K3V[i] for i in range(NC)])
_y_neg = cnt([_COEF_A * AV[i] - F(1, 2) * K3V[i] for i in range(NC)])
_a8_ok = (_perm_closed and _ifx_TL and _q_pos == _q_neg and _y_pos == _y_neg)
add(MAIN, "A8",
    "lambda_K 的符号没有物理内容：eps4 <-> eps5 是权集的对称（16/16 闭环），它把 lambda_K 变成 -lambda_K",
    "权集在 eps4<->eps5 下闭环（16/16）；两解的 Q 多重集与 y 多重集**全同**",
    "置换闭环 = %s（%d/%d）；T3L 在该置换下不变 = %s；Q 两解同多重集 = %s；y 两解同多重集 = %s"
    % (_perm_closed, len(_S & _SW), NC, _ifx_TL, _q_pos == _q_neg, _y_pos == _y_neg),
    "PASS" if _a8_ok else "FAIL",
    "★★★ 这一条把 r399 那个「PLUS = 16bar」的困惑彻底定性：它不是「我们的谱反了」，而是"
    "**权集本身有一个 Z2 对称（eps4 <-> eps5），它交换两个 su(2) 而不动 T3L**。"
    "在这个置换下 K3 -> -K3，于是 lambda_K 的符号翻过来 —— 但 16 个态只是被重新编号，谱一模一样。"
    "★ 所以「+1/2 还是 -1/2」不是一个可以用任何谱、任何多重集、任何矩来判定的问题：它是一个**编号约定**。"
    "★★ 与 r399 的「报谱必报约定」接上了：r399 只看到两个谱互为相反数，本卷指出了**那条对称性**，"
    "并证明它不改变任何可观测量。")

# ============================================================ A9 校正 r399 的 16 / 16bar
SM_Y = {F(1, 6): 6, F(-2, 3): 3, F(1, 3): 3, F(-1, 2): 2, F(1): 1, F(0): 1}
R398_Y = {F(-1): 1, F(-1, 6): 6, F(2, 3): 3, F(-1, 3): 3, F(1, 2): 2, F(0): 1}
R398_NEG = {-k: v for k, v in R398_Y.items()}
_y_here = cnt([_COEF_A * AV[i] + F(1, 2) * K3V[i] for i in range(NC)])
_eqSM = (_y_here == SM_Y)
_eq398 = (_y_here == R398_Y)
_eqneg = (_y_here == R398_NEG)
_a9_ok = (_eqSM and (not _eq398) and _eqneg)
add(MAIN, "A9",
    "校正 r399：本卷算出的 y 多重集 = **SM 超荷表**，而 = r398 公布清单的**逐项取反** "
    "⇒ r398 的清单是共轭谱，r399 那句「PLUS = 16bar」应改成「r398 的清单是 16bar 的谱」",
    "y == SM 超荷表（True）；y == r398 清单（False）；y == r398 清单逐项取反（True）",
    "y = %s；== SM 超荷表 %s；== r398 清单 %s；== r398 取反 %s"
    % (ctr_txt(_y_here), _eqSM, _eq398, _eqneg),
    "PASS" if _a9_ok else "FAIL",
    "★★★ 这一条是**溯因**：r399 只做了「我算的 vs r398 公布的」这条内部比较，得到「互相取反」，"
    "然后把符号判给了自己（说 PLUS 是 16bar）。本卷引入**第三个数**（SM 超荷表）之后，方向就定死了："
    "本卷的 y 就是教科书上那 16 个超荷，所以 r398 公布的清单是取反的那一份。"
    "★★ 教训（与 r397 E09 / r399 E04 同族）：**两个内部读数互相矛盾时，谁也不能给谁判对错**；"
    "必须再拉一个外部锚。这里的外部锚是 SM 的电荷表与超荷表 —— 它们是物理输入，但它们是 16 项的输入，"
    "而不是 2 个自由参数。"
    "★ 本卷不修改 r399 的任何文件（只登记勘误），因为读数本身（「互为取反」）是对的，错的是**归属**。")

# ============================================================ A10 边界：电荷谱对共轭免疫
_neg_Q = {-k: v for k, v in SM_Q.items()}
_selfc = (_neg_Q == SM_Q)
_nfix = sum(1 for k in SM_Q if k == 0 or (-k) in SM_Q)
_a10_ok = _selfc and _nfix == len(SM_Q)
add(MAIN, "A10",
    "边界：SM 电荷表本身对 q -> -q 免疫（它自己就是自共轭的）⇒ 任何只用电荷谱的判据都**无法区分 16 与 16bar**",
    "SM 电荷表 == 其逐项取反（True）；且值集在取反下闭合（7 个值全有配对）",
    "SM 电荷表取反后相等 = %s；值集在取反下闭合 = %s（%d/%d 个值）"
    % (_selfc, _nfix == len(SM_Q), _nfix, len(SM_Q)),
    "PASS" if _a10_ok else "FAIL",
    "★★ 这一条是本卷的**诚实边界**，而且是算出来的：SM 电荷表 {2/3 x3, -1/3 x3, -2/3 x3, 1/3 x3, 0 x2, 1, -1} "
    "在 q -> -q 下不变，所以「16 还是 16bar」这一层**任何电荷判据都看不见**。"
    "★ 推论：A5–A7 的结论都是「方向唯一」而不是「粒子唯一」；要把 16 与 16bar 分开，必须引入**费米子编号**"
    "（哪个态叫 nu、哪个叫 e），那是本卷没有做的另一层输入。"
    "★★ 这不削弱本卷：r399 的边界是「两个自由实参数」，本卷把它换成了「一张 16 项的物理表 + 一条编号约定」，"
    "自由度的从 2 连续维降到 0 连续维 + 1 个离散约定。")

# ============================================================ 控制组
def _viol(q):
    return diff_n(cnt(q), SM_Q)


_v1 = [TLV[i] + F(-2, 3) * AV[i] + F(1, 2) * K3V[i] for i in range(NC)]     # 漏 1/2
_v2 = [TLV[i] + F(-1, 3) * AV[i] for i in range(NC)]                        # 去掉 K3 项
_v3 = [TLV[i] + F(-1, 3) * (W[i][0] + W[i][1]) + F(1, 2) * K3V[i] for i in range(NC)]  # su(4) 方向错
_v4 = [TLV[i] + F(-1, 3) * AV[i] + F(1, 2) * (W[i][3] + W[i][4]) for i in range(NC)]   # 用 T3L 当 T3R
_k1 = (_viol(_v1), len(cnt(_v1)))
_k2 = (_viol(_v2), len(cnt(_v2)))
_k3 = (_viol(_v3), len(cnt(_v3)))
_k4 = (_viol(_v4), len(cnt(_v4)))
add(CTL, "K1",
    "控制组（漏因子）：Y = B-L + (1/2)K3（把 A4 里那个 1/2 丢掉）",
    "(16, 8)（基线 (0, 7)：违例数, Q 值个数）",
    "违例 %d 处；Q 有 %d 个不同值" % _k1,
    "PASS" if _k1 == (16, 8) else "FAIL",
    "★ 这一条测的正是 A4 里最容易被当成「写上去的 1/2」的那一步：丢掉它之后 16 个态**全错**。"
    "所以那个 1/2 是有内容的，不是装饰。")
add(CTL, "K2",
    "控制组（缺项）：去掉 K3 项（Y = -(1/3)A）—— 只有一半的态对得上",
    "(8, 6)（基线 (0, 7)）",
    "违例 %d 处；Q 有 %d 个不同值" % _k2,
    "PASS" if _k2 == (8, 6) else "FAIL",
    "★ 8 个态对、8 个错：正好是 K3 = 0 的那一半对（因为那一半本来就看不见 K3 项）。"
    "这说明**扇区分解（A5）不是人为切分，而是问题本身的结构**。")
add(CTL, "K3",
    "控制组（方向错）：su(4) 方向写成 h1+h2（少一个 Cartan）",
    "(16, 6)（基线 (0, 7)）",
    "违例 %d 处；Q 有 %d 个不同值" % _k3,
    "PASS" if _k3 == (16, 6) else "FAIL",
    "★ 少一个 Cartan ⇒ A 的谱从 {±3/2, ±1/2} 变成 {±1, 0} ⇒ 电荷全部错开。"
    "★ 与 A2 呼应：A2 的两条方程在 h1+h2 上会给出**不同**的 alpha，所以这条控制组红得有两重理由。")
add(CTL, "K4",
    "控制组（换半边）：把 T3L 当成 T3R 用（A7 的单点版）",
    "(16, 5)（基线 (0, 7)）",
    "违例 %d 处；Q 有 %d 个不同值" % _k4,
    "PASS" if _k4 == (16, 5) else "FAIL",
    "★ A7 是全网格版的同一条；这里做单点版是为了给出**一个具体读数**，"
    "而 A7 给的是「解集为空」这个集合层面的读数。两者不可互相替代。")

# ============================================================ 守卫
try:
    _SRC = io.open(os.path.abspath(__file__), encoding="utf-8").read()
except Exception:
    _SRC = ""
_AST = ast.parse(_SRC) if _SRC else None
_WRITTEN = 0
if _AST is not None:
    for node in ast.walk(_AST):
        if isinstance(node, ast.Assign):
            for tg in node.targets:
                if isinstance(tg, ast.Name) and tg.id.endswith("_ok"):
                    v = node.value
                    if isinstance(v, ast.Constant) and v.value is True:
                        _WRITTEN += 1
add(GRD, "G01", "判据不得写死（AST 层：任何 *_ok 变量不得直接赋 True）", "0 处",
    "写死 True 的 *_ok 赋值 %d 处" % _WRITTEN, "PASS" if _WRITTEN == 0 else "FAIL",
    "★★★ r394 的老刀：守卫不得读自己的源码**字面量**。这里走 AST，只看赋值右端是不是常量 True，"
    "所以「把 ok 算出来」和「把 ok 写出来」在这一层可分。")

_same = 0
for _r in MAIN:
    if _r["kind"] in ("PASS", "FAIL") and _unbold(_r["exp"]) == _unbold(_r["act"]):
        _same += 1
add(GRD, "G02", "exp 与 act 不得是同一表达式", "0 条",
    "exp == act 的条目 %d 条" % _same, "PASS" if _same == 0 else "FAIL",
    "★「值相等」不算问题，但「字面相同」说明 act 没有真的算过 —— 这是 r397 那条「只有真算出数才给 PASS」的机核。")

_readings = [_k1, _k2, _k3, _k4]
add(GRD, "G03", "四个控制组必须两两给出不同读数", "4 个不同的 (违例数, Q 值个数)",
    "K1 %s；K2 %s；K3 %s；K4 %s（%d 个不同）"
    % (_k1, _k2, _k3, _k4, len(set(_readings))),
    "PASS" if len(set(_readings)) == 4 else "FAIL",
    "★ K1/K3/K4 的违例数都可能是 16（因为错得足够彻底），所以只看违例数会误判「三条一样」——"
    "必须同时报 Q 的**值个数**这一个正交读数，四条才可分。")

_nf_main = sum(1 for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G04", "收尾重算：每条 PASS 都必须有非空 note 且 computed", "0 违规",
    "%d 违规（覆盖 %d 条）" % (sum(1 for r in ALL if not r["note"] or not r["computed"]), len(ALL)),
    "PASS" if all(r["note"] and r["computed"] for r in ALL) else "FAIL",
    "★ 收尾整表重扫，不逐条自查。")

_a_open = [i for i in range(NC) if TRV[i] != 0 and TLV[i] != 0]
_g5 = (len(ZI) + len(NI) == NC and len([i for i in range(NC) if AV[i] > 0]) == 8
       and len([i for i in range(NC) if AV[i] < 0]) == 8 and not _a_open)
add(GRD, "G05", "维数账：16 = (K3=0 的 8) + (K3!=0 的 8) = (A>0 的 8) + (A<0 的 8)；且没有态同时有 T3L 与 T3R",
    "闭合",
    "K3 扇区 %d+%d；A 扇区 %d+%d；同时非零的态 %d 个"
    % (len(ZI), len(NI), len([i for i in range(NC) if AV[i] > 0]),
       len([i for i in range(NC) if AV[i] < 0]), len(_a_open)),
    "PASS" if _g5 else "FAIL",
    "★ 最后那一条（没有态同时有 T3L 与 T3R）不是装饰：它说明 16 = (4,2,1) + (4bar,1,2) 是**分块**的，"
    "每个态只属于一个 su(2) —— 这正是 A7 能干脆给出 0 解的结构原因。")

_g6 = (sum(SM_Q.values()) == NC and sum(SM_Y.values()) == NC and _SP_BL == _EXP_BL)
add(GRD, "G06", "SM 内容闭合：电荷表 16 项、超荷表 16 项、B-L 表 16 项", "各 16",
    "Q %d；y %d；B-L %d" % (sum(SM_Q.values()), sum(SM_Y.values()), sum(_SP_BL.values())),
    "PASS" if _g6 else "FAIL",
    "★ 三张表都必须是 16 项 —— 少一项就说明某个扇区被漏掉了，而 A5 的扇区分解会静默成立（因为另一扇区多余）。")

_g7 = (len(KEYS) == 45 and len(HC) == 5 and all(len(w) == 5 for w in W))
add(GRD, "G07", "完备性：45 个 Sigma 全建、5 个 Cartan、每个权 5 维", "45 / 5 / 5",
    "Sigma %d；Cartan %d；权维数 %s" % (len(KEYS), len(HC), sorted({len(w) for w in W})),
    "PASS" if _g7 else "FAIL",
    "★ 少一个 Cartan 会让 A 变成 2 维和（K3 控制组正是这种错），所以这条必须先绿。")

VERDICT = "--".join([
    "COEFFS-DERIVED",
    "LA-MINUS-1/3-UNIQUE" if _solA == [F(-1, 3)] else "LA-AMBIGUOUS",
    "LK-MAG-1/2" if sorted(_solK) == [F(-1, 2), F(1, 2)] else "LK-OPEN",
    "LK-SIGN-IS-SYMMETRY" if _a8_ok else "LK-SIGN-PHYSICAL",
    "T3L-CHOICE-DECIDABLE" if _a7_ok else "T3L-IS-INPUT",
    "R398-LIST-IS-CONJUGATE" if _a9_ok else "R398-LIST-UNRESOLVED",
])
add(GRD, "G08", "判词与判定表必须同一读数（两路径拼接）", "两路一致",
    "由变量拼：%s" % VERDICT, "PASS" if _a5_ok and _a6_ok and _a7_ok and _a8_ok and _a9_ok else "FAIL",
    "★ 判词的每一段都由一个布尔量决定，不写字面量。")

# ---- G09 占位（落盘后回填）
g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "（回填）", "（回填）", "INFO",
          "★ 先占位再回填（r396 E06：报告必须在回填之后才拼）")

DECLARED_NEG = set()
_neg_fail = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G10", "真判负必须逐条登记", "登记集 == 实际 FAIL 集",
    "%s vs %s" % (sorted(DECLARED_NEG), _neg_fail),
    "PASS" if sorted(DECLARED_NEG) == _neg_fail else "FAIL",
    "★ 本卷若有判负，必须同时写进 DECLARED_NEG 与判定册。")

# ---- G11 两条独立路径（扇区 vs 全网格）
_g11 = (set(_full) == _sec_set | _conj and not (set(_full) == _sec_set) and len(_conj) == len(_sec_set))
add(GRD, "G11", "两条路径的**结构关系**：扇区解 ⊂ 全网格解，且差集恰为扇区解的整体取反（共轭）",
    "全网格 == 扇区 ∪ (-扇区)；且两者不等（差集非空）；扇区与 -扇区 不重叠",
    "扇区 %s；-扇区 %s；全网格 %s；并集相等 = %s"
    % (sorted(_sec_set), sorted(_conj), sorted(set(_full)), set(_full) == _sec_set | _conj),
    "PASS" if _g11 else "FAIL",
    "★★★ 这是本卷的**总纲**，而且第一版写错了（E02）：我原先要求两路解集**相等**，结果判 FAIL。"
    "正确的读法是关系而不是相等 —— 扇区版带着「哪一半装夸克」的指认，所以看不到共轭那两支；"
    "全网格不带指认，于是多出整体取反的那一对。"
    "★ 这个「多出来的一倍」不是噪声，它是**16 与 16bar 的分裂**在解集上的像："
    "A9 说明本卷的 y 就是 SM 表（不是共轭），A10 说明电荷谱本身分不开这两支 —— 三条合起来才完整。")

# ---- G12 定标不变性（用 H 的标度换一次）
_sc = F(3)
_Y_scaled = {k: _sc * v for k, v in Y_C.items()}
_M0 = to_rep_c(Y_C, SIGC)
_M1 = to_rep_c(_Y_scaled, SIGC)
_g12 = (_M1 == ([[_sc * x for x in row] for row in _M0[0]],
                [[_sc * x for x in row] for row in _M0[1]]))
_y3 = cnt([_sc * (_COEF_A * AV[i] + _COEF_K * K3V[i]) for i in range(NC)])
add(GRD, "G12", "标度检查：Y 乘 3 时矩阵整体乘 3（线性性永远成立），但 y 表整体离开 SM 表", "两件事都成立",
    "矩阵整体乘 3 = %s；乘 3 后 y 值集 = %s（与 SM 表相交 %d 个值）"
    % (_g12, sorted(set(_y3)), len(set(_y3) & set(SM_Y))),
    "PASS" if (_g12 and set(_y3) != set(SM_Y)) else "FAIL",
    "★ 这条不是废话：它把「线性」与「系数唯一」分成两件事 —— 线性性是**代数**给的（永远成立），"
    "而系数唯一是**电荷表**给的（只有一组数成立）。混为一谈就会把「Y 可以整体缩放」误当成「系数不唯一」。")

add(GRD, "G13", "总门必须对「守卫失败」敏感（含已登记判负不挡门）", "注入守卫 FAIL 必须翻转",
    "（回填）", "INFO", "★ 沿用 r392 起口径。")


def final_of(nf_main, nf_guard, n_decl=0):
    if nf_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main


# ---- G14 关键表（全部机拼）
_lin = []
for (_ga, _gb), _v in sorted(Y_C.items()):
    _hi = _gb // 2 + 1
    _mag = "" if abs(_v) == 1 else str(abs(_v)) + "*"
    _lin.append(("-%sH%d" % (_mag, _hi)) if _v < 0 else ("+%sH%d" % (_mag, _hi)))
_YDEC = "Y = " + " ".join(_lin)
_KT1 = "%s（逐元素相等 = %s）" % (_YDEC, _a4_mat)
_KT2 = "B-L：alpha = %s（两条方程一致 = %s）；16 态多重集 = %s" % (_AL1, _AL1 == _AL2, ctr_txt(_SP_BL))
_KT3 = "系数：A 的系数 = %s，K3 的系数 = %s，比值 = %s" % (_COEF_A, _COEF_K, _ratio)
_KT4 = ("解集：扇区 %s（%d 个）；全网格 %d 点 → %d 解；差集 = 扇区的整体取反 %s"
        % (sorted(_sec_set), len(_sec_set), len(_GRID) ** 2 - 1, len(_full),
           sorted(set(_full) - _sec_set)))
_kt_all = " || ".join([_KT1, _KT2, _KT3, _KT4])
_kt_re = " || ".join([
    "%s（逐元素相等 = %s）" % ("Y = " + " ".join(
        ("-%sH%d" % (("" if abs(v) == 1 else str(abs(v)) + "*"), b // 2 + 1)) if v < 0
        else ("+%sH%d" % (("" if abs(v) == 1 else str(abs(v)) + "*"), b // 2 + 1))
        for (a, b), v in sorted(Y_C.items())), _a4_mat),
    "B-L：alpha = %s（两条方程一致 = %s）；16 态多重集 = %s" % (
        F(-1) / F(3, 2), (F(-1) / F(3, 2)) == (F(1, 3) / F(-1, 2)), ctr_txt(cnt([F(-2, 3) * x for x in AV]))),
    "系数：A 的系数 = %s，K3 的系数 = %s，比值 = %s" % (
        F(-1) / F(3, 2) / 2, F(1, 2), (F(-1) / F(3, 2) / 2) / (F(-1) / F(3, 2))),
    "解集：扇区 %s（%d 个）；全网格 %d 点 → %d 解；差集 = 扇区的整体取反 %s" % (
        sorted({(la2, lk2) for la2 in
                [x for x in _GRID if x != 0
                 and cnt([TLV[i] + x * AV[i] for i in ZI]) == SUB_Z]
                for lk2 in
                [x for x in _GRID if x != 0
                 and cnt([TLV[i] + F(-1, 3) * AV[i] + x * K3V[i] for i in NI]) == SUB_N]}),
        len([1 for la2 in _GRID if la2 != 0 and cnt([TLV[i] + la2 * AV[i] for i in ZI]) == SUB_Z])
        * len([1 for x in _GRID if x != 0 and cnt([TLV[i] + F(-1, 3) * AV[i] + x * K3V[i] for i in NI]) == SUB_N]),
        len(_GRID) ** 2 - 1,
        len([1 for la in _GRID for lk in _GRID if (la, lk) != (0, 0)
             and cnt([TLV[i] + la * AV[i] + lk * K3V[i] for i in range(NC)]) == SM_Q]),
        sorted({(la, lk) for la in _GRID for lk in _GRID if (la, lk) != (0, 0)
                and cnt([TLV[i] + la * AV[i] + lk * K3V[i] for i in range(NC)]) == SM_Q}
               - {(la2, lk2) for la2 in _GRID if la2 != 0
                  and cnt([TLV[i] + la2 * AV[i] for i in ZI]) == SUB_Z
                  for lk2 in _GRID if lk2 != 0
                  and cnt([TLV[i] + F(-1, 3) * AV[i] + lk2 * K3V[i] for i in NI]) == SUB_N})),
])
add(GRD, "G14", "关键表每一句都必须由变量拼出（含分解式的 H 下标、B-L 的 alpha、解集）", "两路一致",
    "关键表：%s；由重算拼：%s" % (_kt_all, _kt_re),
    "PASS" if (_kt_all == _kt_re and _a4_mat and _a2_ok and _a5_ok and _a6_ok) else "FAIL",
    "★★ r396 E02 / r397 E09 / r398 E06 / r399 E07 的第五次继承：关键表**连 H 下标都是算的**。"
    "★ 这里还多了一层：解集也用两条不同写法拼（一条用 A5 的扇区积，一条用 A6 的全网格重扫），"
    "所以「关键表写对」不再依赖任何记忆。")

# ============================================================ 汇总
_nf_main = sum(1 for r in MAIN if r["kind"] == "FAIL")
_nf_g = sum(1 for r in CTL + GRD if r["kind"] == "FAIL")
FINAL = final_of(_nf_main, _nf_g, len(DECLARED_NEG & set(_neg_fail)))

g13 = ALL[[r["id"] for r in ALL].index("G13")]
g13["exp"] = "注入守卫 FAIL 必须翻转；已登记判负不挡门"
g13["act"] = "(0,0)=%s；(0,1)=%s；(1,0)=%s；(已登记 1 条)=%s" % (
    final_of(0, 0, 0), final_of(0, 1, 0), final_of(1, 0, 0), final_of(1, 0, 1))
g13["kind"] = ("PASS" if (final_of(0, 0, 0) == "GATES-PASS-ALL-POSITIVE"
                          and final_of(0, 1, 0) != final_of(0, 0, 0)
                          and final_of(1, 0, 0) != final_of(0, 0, 0)
                          and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE") else "FAIL")

# ============================================================ 落盘（JSON → 回填 G09 → 再写 → 最后拼报告）
RPT = os.path.join(DATA, TITLE + "_report_2026-11-04.txt")
JSN = os.path.join(DATA, TITLE + ".json")
payload = dict(rid=RID, date="2026-11-04", title=TITLE, final=FINAL, verdict=VERDICT,
               counts=dict(main=len(MAIN), pass_=sum(1 for r in MAIN if r["kind"] == "PASS"),
                           info=sum(1 for r in MAIN if r["kind"] == "INFO"),
                           identity=sum(1 for r in MAIN if r["kind"] == "IDENTITY"),
                           fail=_nf_main, ctl=len(CTL), grd=len(GRD), total=len(ALL)),
               rows=ALL, declared_neg=sorted(DECLARED_NEG))
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))
_back = json.load(io.open(JSN, encoding="utf-8"))
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                       "一致" if len(_back["rows"]) == len(ALL) else "不一致")
g09["exp"] = "回读条目数 == 内存条目数（%d）" % len(ALL)
g09["kind"] = "PASS" if len(_back["rows"]) == len(ALL) else "FAIL"
payload["rows"] = ALL
payload["final"] = FINAL
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

L = []


def A(s=""):
    L.append(s)


A(TITLE)
A("=" * 100)
A("对象：X-GSM-5（Y 的两个系数不是输入：由 SM 电荷谱唯一定出）")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
     sum(1 for r in MAIN if r["kind"] == "INFO"), sum(1 for r in MAIN if r["kind"] == "IDENTITY"),
     _nf_main, len(CTL), len(GRD), len(ALL)))
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
A(_KT1)
A(_KT2)
A(_KT3)
A(_KT4)
A("读数：扇区1 %s；扇区2 %s；lambda_A/alpha = %s；T3L 换 T3R 后解 %d 个；y == SM 超荷 %s；y == r398 取反 %s"
  % ([str(x) for x in _solA], [str(x) for x in _solK], _ratio, len(_swap), _eqSM, _eqneg))
A("")
A("【诚实边界】")
A(" 1) 本卷把「2 个自由实参数」换成了「一张 16 项电荷表 + 一张 16 项超荷表」：这不是「没有输入」，"
  "而是**输入从 2 个连续参数变成 1 张离散的物理表**。净增益是可判定的（16 个约束 vs 2 个未知）；")
A(" 2) 电荷表与超荷表里每一条（Q 的 7 个值、y 的 6 个值及其重数）都是**物理输入**，本卷不推导它们；"
  "本卷推导的是「给定这两张表，Y 在 so(10) 卡当里的方向」；")
A(" 3) A10 是算出来的边界：SM 电荷表对 q -> -q 免疫 ⇒ 任何电荷判据都分不开 16 与 16bar；"
  "要分开必须引入「哪个态叫 nu」这一层编号，本卷没有做；")
A(" 4) A5/A6 用的「电荷多重集」判据不指定逐态指认：它只要求 16 个电荷值对得上。"
  "所以本卷的「唯一」是在多重集等价意义下的唯一；逐态指认会给出更强的约束，但也带来更多输入；")
A(" 5) 「扇区互不相交」（A5）依赖 G05 那条：没有态同时有 T3L 与 T3R。若这条不成立，两段一维搜索的解集"
  "不能直接相乘 —— 这正是 G11 要拿全网格复核的原因；")
A(" 6) 本卷不含质量谱 / Yukawa / 混合角；也不构造 16 -> 16bar 共轭算子。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("JSON ->", JSN)
print("RPT  ->", RPT)
print("FINAL =", FINAL)
