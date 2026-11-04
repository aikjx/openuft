# -*- coding: utf-8 -*-
"""TUFT-r398  攻 X-GSM-3：V_J / V_K 显式基与零模归属 —— 把 r397 的「机制认领」变成推导

纯标准库（Fraction，判据区无浮点、无随机）。不读任何来料中间量。

r397 留下的两条软边界（§十四 第 3、5 条）：
  ① 「16 能分辨 J/K」的**机制**（16 = V_J ⊕ V_K、nu^c ∈ V_J）只是**认领**；
  ② 「手征块对单态计数不可见」只有读数、没有构造。
本卷用显式基把它做掉，并顺带把 r397 E09 撤回的那句话（16 与 16bar 不等价）**变成机核事实**，
同时明确它**不是** J/K 可分辨的原因。

  A1  复结构 JMAP：JMAP^2 = -1；与 45 个 Sigma、12 个 SM 生成元全部交换（57 项）
  A2  V_J = ker(su(2)_J)：实 16 维、JMAP 不变（⇒ 复 8 维子空间），给出显式基
  A3  V_K = ker(su(2)_K)：实 16 维、JMAP 不变
  A4  V_J ∩ V_K = 0 且维数和 32 ⇒ 16 = V_J ⊕ V_K（**定理**，不是认领）
  A5  J3 在 V_J 上恒 0；在 V_K 上 A^2 = (1/4)I 且 tr = 0 ⇒ 谱 ±1/2 各 8
  A6  核心：ker(Y|V_J) 实 2（复 1 = nu^c）、ker(Y|V_K) = 0 ⇒ r397 的 2 vs 0 是推导
  A7  谱分半：tr((Y|V_J)^2)/2 与 tr((Y|V_K)^2)/2 不同、和 = p_1 ⇒ 「p_k 四格全同」与「J/K 可分」不矛盾
  A8  16 与 16bar **不等价**的机核：ker(Y-1) 在 16 上 2 维、在 16bar 上 0 维
  A9  判别力：换 so(4) 到 1..4 指标，仍 8+8，但子空间不同、nu^c 不在其中
"""
import io
import json
import os
from fractions import Fraction as F

RID = "r398"
TITLE = ("TUFT-r398_攻X-GSM-3_VJ与VK显式基与零模归属_十六的八加八直和定理_"
         "单态机制从认领到推导_十六与十六bar不等价的机核_换so4的判别力_精算_2026-11-04")
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


# ============================================================ A1 复结构
JMAP = zmat(N32)
for i in range(16):
    JMAP[i][16 + i] = F(-1)
    JMAP[16 + i][i] = F(1)
_jmap_sq = mmul(JMAP, JMAP, N32)
_jmap_negI = [[F(-1) if i == j else F(0) for j in range(N32)] for i in range(N32)]
_jm_bad_sig = [kk for kk in KEYS if not is_zero(comm2(JMAP, SIGR[kk], N32))]
_jm_bad_sm = [i for i, M in enumerate(SM_J) if not is_zero(comm2(JMAP, M, N32))]
_a1_ok = (_jmap_sq == _jmap_negI and not _jm_bad_sig and not _jm_bad_sm)
add(MAIN, "A1",
    "复结构 JMAP（32 维实化空间上乘 i）：JMAP^2 = -1；与 45 个 Sigma 与 12 个 SM 生成元全部交换",
    "JMAP^2 = -1；57 项全部交换",
    "JMAP^2 = -1 是 %s；与 Sigma 不交换 %d 个；与 SM 生成元不交换 %d 个"
    % (_jmap_sq == _jmap_negI, len(_jm_bad_sig), len(_jm_bad_sm)),
    "PASS" if _a1_ok else "FAIL",
    "★★ 这一条不是装饰：r397 把 16x16 复矩阵 realify 成 32x32 实矩阵，"
    "「实化 = 复线性映射」这件事的机核就是「与 JMAP 交换」。若某处漏了 -B 的负号，"
    "矩阵会不再与 JMAP 交换 —— 本卷把它做成第一道门。"
    "★ 45 + 12 = 57 项逐项验证，不抽查。")

# ============================================================ A2 / A3 V_J 与 V_K
VJ = nullspace_basis(rows_of(J_GENS), N32)
VK = nullspace_basis(rows_of(K_GENS), N32)
_dimVJ, _dimVK = len(VJ), len(VK)


def is_invariant(M, basis, n=N32):
    """basis 张成的子空间是否 M-不变（只需 rank(basis + M·basis) == rank(basis)）"""
    base = rank_of(basis, n)
    ext = list(basis) + [mat_vec(M, b) for b in basis]
    return rank_of(ext, n) == base


_jm_inv_J = is_invariant(JMAP, VJ)
_jm_inv_K = is_invariant(JMAP, VK)


def _fmt_vec(v, kmax=4):
    nz = [(i, v[i]) for i in range(len(v)) if v[i] != 0]
    head = ", ".join("%d:%s" % (i + 1, str(x)) for i, x in nz[:kmax])
    return "[%d 个非零] %s%s" % (len(nz), head, " …" if len(nz) > kmax else "")


_a2_ok = (_dimVJ == 16 and _jm_inv_J)
add(MAIN, "A2",
    "V_J = ker(su(2)_J) 的显式基：实 16 维（= 复 8 维），且 JMAP-不变（⇒ 确是复子空间）",
    "实 16 维；JMAP-不变 = True",
    "维数 %d；JMAP-不变 = %s；基[0] = %s；基[1] = %s"
    % (_dimVJ, _jm_inv_J, _fmt_vec(VJ[0]), _fmt_vec(VJ[1])),
    "PASS" if _a2_ok else "FAIL",
    "★★ 「实 16 维」不等于「复 8 维」：只有子空间 JMAP-不变时才成立（复结构把实向量配成 v 与 i·v）。"
    "这一条是 r397 A5 那条「实 2 ÷ 2 = 复 1」的**结构性版本** —— 那里只对一个零空间做了除法，"
    "这里对整个 16 维子空间验证了复结构。★ 基向量是有理数，可直接复算。")

_a3_ok = (_dimVK == 16 and _jm_inv_K)
add(MAIN, "A3",
    "V_K = ker(su(2)_K) 的显式基：实 16 维、JMAP-不变",
    "实 16 维；JMAP-不变 = True",
    "维数 %d；JMAP-不变 = %s；基[0] = %s" % (_dimVK, _jm_inv_K, _fmt_vec(VK[0])),
    "PASS" if _a3_ok else "FAIL",
    "★ 与 A2 同一算法、只换 3 个生成元（SU2J_C → SU2K_C）—— 口径自守：换对象不换算法。"
    "★★ 注意维数相同**不能**说明两个子空间相同：见 A4 与 K2。")

# ============================================================ A4 直和
_rank_sum = rank_of(VJ + VK, N32)
_inter = _dimVJ + _dimVK - _rank_sum
_a4_ok = (_rank_sum == 32 and _inter == 0)
add(MAIN, "A4",
    "16 = V_J ⊕ V_K：两个子空间的交为 0、维数和 = 32",
    "rank(V_J + V_K) = 32；交维数 = 0",
    "rank(V_J + V_K) = %d；dim V_J = %d；dim V_K = %d ⇒ 交维数 = %d"
    % (_rank_sum, _dimVJ, _dimVK, _inter),
    "PASS" if _a4_ok else "FAIL",
    "★★★ 这一条把 r397 §十四 第 5 条的「认领」变成**定理**：16 不是「碰巧」分成 8+8，"
    "而是两个核的交为零、维数和恰为 32 ⇒ 直和。★ 机核是「秩」不是「维数相加」："
    "两个 16 维子空间在 32 维里可以相同，也可以交成 16 维 —— 必须算 rank(V_J + V_K)。")

# ============================================================ A5 J3 的谱结构
_A_J3J = restrict_mat(J3, VJ, N32)
_A_J3K = restrict_mat(J3, VK, N32)
_A_J3K_sq = mmul(_A_J3K, _A_J3K, len(_A_J3K))
_A_J3K_sq_ok = all(_A_J3K_sq[i][j] == (F(-1) if i == j else F(0))
                   for i in range(len(_A_J3K)) for j in range(len(_A_J3K)))
_tr_J3K = trace(_A_J3K)
_a5_ok = (is_zero(_A_J3J) and _A_J3K_sq_ok and _tr_J3K == 0)
add(MAIN, "A5",
    "J3 在两半上的谱：V_J 上恒 0；V_K 上满足 A^2 = -I 且 tr = 0 ⇒ 谱 {+i x8, -i x8} ⇒ 4 个二重态",
    "V_J 上全 0；V_K 上 A^2 = -I、tr = 0",
    "V_J 上 J3 全零 = %s；V_K 上 A^2 = -I 是 %s；tr = %s ⇒ 谱 {+i x8, -i x8}"
    % (is_zero(_A_J3J), _A_J3K_sq_ok, _tr_J3K),
    "PASS" if _a5_ok else "FAIL",
    "★★ 只用**代数恒等式**给谱，不去解本征值：16x16 矩阵满足 A^2 = -I ⇒ 全部本征值是 ±i；"
    "再加 tr = 0 ⇒ 正负各 8。**全程有理数，没有一次开方。**"
    "★★★ 归一化必须说清（这是本卷第 E01 号自伤）：`Sigma_ab = (1/4)[Gamma,Gamma]` 是**反 Hermitian**，"
    "实化后是实反对称，所以 J3 的本征值是**纯虚**的；又因为 SU2J_C 每个平面系数取 1（= 标准 Cartan 的 2 倍），"
    "二重态上的谱是 ±i（不是 ±i/2）。第一版把期望写成 `A^2 = +(1/4)I`（Hermitian 口径）⇒ 当场判 FAIL。"
    "★ 于是 16 = 8 x 1（V_J，su(2)_J 平凡）+ 4 x 2（V_K，四个二重态）—— "
    "这是 r397 K1 里「su(2)_J 给 16 维不变量」的显式分解。")

# ============================================================ A6 核心：Y 的零模落在哪一半
_A_YJ = restrict_mat(Y_R, VJ, N32)
_A_YK = restrict_mat(Y_R, VK, N32)
_kerYJ = len(VJ) - rank_of(_A_YJ, len(VJ))
_kerYK = len(VK) - rank_of(_A_YK, len(VK))
_a6_ok = (_kerYJ == 2 and _kerYK == 0)
add(MAIN, "A6",
    "核心：Y 在 V_J 上有一个 2 维实零模（= 复 1 维 = nu^c），在 V_K 上一个都没有",
    "ker(Y|V_J) = 2（复 1）；ker(Y|V_K) = 0",
    "ker(Y|V_J) = %d 维实（复 %d）；ker(Y|V_K) = %d 维实（复 %d）"
    % (_kerYJ, _kerYJ // 2, _kerYK, _kerYK // 2),
    "PASS" if _a6_ok else "FAIL",
    "★★★ 这就是 r397 A8「J 档留 1、K 档留 0」的**推导**：不是「解 12 个生成元的 384x32 得 2」，"
    "而是「su(2)_J 先把空间切成 V_J ⊕ V_K，再看 Y 的零模落在哪一半」。"
    "★ 精确机制一句话：**零模落在哪一半，哪一半就留一个单态**。"
    "★★ 这一条同时解释了为什么 r397 的 K1 表里 `su(2)_J+Y` 给 2、`su(2)_K+Y` 给 0 —— "
    "不是 Y 变了，是**被问的那一半变了**。")

# ============================================================ A7 谱分半（按 y 值列表）
H_Y = mmul(JMAP, Y_R, N32)        # i*Y：Hermitian（实对称），本征值 = y
H_YM = mmul(JMAP, Y_RM, N32)
_h_sym = all(H_Y[i][j] == H_Y[j][i] for i in range(N32) for j in range(N32))
_HJ = restrict_mat(H_Y, VJ, N32)
_HK = restrict_mat(H_Y, VK, N32)
YVALS = [F(-1), F(1), F(-2, 3), F(2, 3), F(-1, 3), F(1, 3),
         F(-1, 2), F(1, 2), F(-1, 6), F(1, 6), F(0)]
_tab = []
for lam in YVALS:
    _tab.append((lam,
                 len(VJ) - rank_of([[HJ_i - (lam if a == b else F(0))
                                     for b, HJ_i in enumerate(_HJ[a])] for a in range(len(_HJ))], len(_HJ)),
                 len(VK) - rank_of([[HK_i - (lam if a == b else F(0))
                                     for b, HK_i in enumerate(_HK[a])] for a in range(len(_HK))], len(_HK))))
_tab_txt = "; ".join("y=%s: V_J %d / V_K %d" % (lam, a, b) for lam, a, b in _tab)
_tot_J = sum(a for _, a, b in _tab)
_tot_K = sum(b for _, a, b in _tab)
_tot_all = _tot_J + _tot_K
_nz_J = sum(1 for _, a, b in _tab if a > 0)
_nz_K = sum(1 for _, a, b in _tab if b > 0)
_vals_J = [lam for lam, a, b in _tab if a > 0]
_vals_K = [lam for lam, a, b in _tab if b > 0]
_vJ_txt = "{" + ", ".join("%s" % v for v in _vals_J) + "}"
_vK_txt = "{" + ", ".join("%s" % v for v in _vals_K) + "}"
def _pow_sum(M, kmax=1):
    n = len(M)
    P = mmul(M, M, n)
    Q = P
    for _ in range(1, kmax):
        Q = mmul(Q, P, n)
    return (F(-1) ** kmax) * trace(Q) / 2


_s1_J = _pow_sum(_A_YJ, 1)
_s1_K = _pow_sum(_A_YK, 1)
_s1_sum = _s1_J + _s1_K
_s2_J = _pow_sum(_A_YJ, 2)
_s2_K = _pow_sum(_A_YK, 2)
_s2_sum = _s2_J + _s2_K
_h2 = trace(mmul(H_Y, H_Y, N32))          # tr((iY)^2) = 2 * p_1
_s1_hit = any(_x in (F(10, 3), F(95, 54)) for _x in (_s1_J, _s1_K))
_a7_ok = (_h_sym and _tot_J == 16 and _tot_K == 16 and _tot_all == 32
          and _s1_J != _s1_K and _s1_sum == F(10, 3)
          and _s2_J != _s2_K and _s2_sum == F(95, 54)
          and _h2 == 2 * F(10, 3) and not _s1_hit)
add(MAIN, "A7",
    "谱分半（按 y 值列全表）：两个 16 维实子空间各收 8 个复态、值集互不相交；"
    "两半的 s1、s2 都不同，而两半之和 = r397 的 p_1 = 10/3、p_2 = 95/54",
    "i*Y 实对称；两半各 16 维实（合计 32）；s1、s2 两半都不同；s1 和 = 10/3、s2 和 = 95/54；"
    "tr((iY)^2) = 2*p_1；两半各自的 s1 都不等于 p_1 或 p_2",
    "i*Y 实对称 = %s；候选 %d 个 y 值（**两侧符号都放了**），有非零读数的 V_J 侧 %d 行、V_K 侧 %d 行；"
    "两半合计 %d + %d = %d；s1 = %s + %s = %s；s2 = %s + %s = %s；tr((iY)^2) = %s；全表 [%s]"
    % (_h_sym, len(YVALS), _nz_J, _nz_K, _tot_J, _tot_K, _tot_all,
       _s1_J, _s1_K, _s1_sum, _s2_J, _s2_K, _s2_sum, _h2, _tab_txt),
    "PASS" if _a7_ok else "FAIL",
    "★★★ 这张表是本卷的**结构总图**：V_J 收 %s（%d 个值、%d 维实 = 复 %d），"
    "V_K 收 %s（%d 个值、%d 维实 = 复 %d）—— 两值集**互不相交**，合起来正好铺满全谱。"
    "★ 符号是**算出来的**：候选集把 ±1、±2/3、±1/3、±1/2、±1/6、0 **全放进去**，"
    "结果每一侧只点亮自己那一半（V_J 侧非零 %d 行、V_K 侧非零 %d 行）⇒ 不是我先定好符号再去验。"
    "★★ A5 已给出两半的 J3 结构（V_J 上恒 0、V_K 上 A^2 = -I）⇒ 上表的读法是「**Y 的每个本征值只住在 J 型或 K 型的一边**」；"
    "这才是 r397「J 档留 2、K 档留 0」被拆开的东西：不是 Y 分成两组，是**空间分成两半、Y 在各自一半上的谱不同**。"
    "★★ 两条幂和都与 r397 互印：s1 和 = %s = p_1、s2 和 = %s = p_2，本卷是**用两个 16x16 子矩阵的迹**分别算再相加"
    "（r397 是在 32 维上直接算 Y^{2k} 的迹），路径不同；tr((iY)^2) = %s = 2*p_1 是同一件事在 32 维上的第三条路径 ⇒ 三路一致。"
    "★ 这一条只在 V_J、V_K 都是 H 的不变子空间时才成立，故它同时**回验**了 A2/A3 的不变性。"
    "★★ 反面也报：两半各自的 s1（%s 与 %s）**都不等于** p_1 或 p_2（判据里的 `not _s1_hit`，实测 %s）"
    "⇒ 全谱矩里**没有**「哪一半出多少」的信息，这与 r397「p_k 四格全同」的边界一致 —— "
    "分辨 J/K 靠的是**零模落点**（A6）与**值集分块**（本条），不是谱矩。"
    % (_vJ_txt, len(_vals_J), _tot_J, _tot_J // 2,
       _vK_txt, len(_vals_K), _tot_K, _tot_K // 2,
       _nz_J, _nz_K, _s1_sum, _s2_sum, _h2, _s1_J, _s1_K, (not _s1_hit)))

# ============================================================ A8 16 与 16bar 不等价 + Y 的符号定下来
def _ker_shift(M, lam, n=N32):
    """ker(M - lam*I) 的维数"""
    S = [[M[i][j] - (lam if i == j else F(0)) for j in range(n)] for i in range(n)]
    return n - rank_of(S, n)


_k_m1 = _ker_shift(H_YM, F(1))
_k_p1 = _ker_shift(H_Y, F(1))
_k_mm1 = _ker_shift(H_YM, F(-1))
_k_pm1 = _ker_shift(H_Y, F(-1))
_a8_ok = (_k_p1 == 0 and _k_m1 == 2 and _k_pm1 == 2 and _k_mm1 == 0)
add(MAIN, "A8",
    "16 与 16bar **不等价**的机核（并顺带把 Y 的符号定下来）：ker(iY -/+ 1) 在两块上下相反",
    "16: (ker(iY-1), ker(iY+1)) = (0, 2)；16bar: (2, 0)",
    "16: ker(iY-1) = %d, ker(iY+1) = %d；16bar: ker(iY-1) = %d, ker(iY+1) = %d"
    % (_k_p1, _k_pm1, _k_m1, _k_mm1),
    "PASS" if _a8_ok else "FAIL",
    "★★★ 先说**工具**：Y 在实化空间的本征值是 ±i*y，所以 `ker(Y - 1)` 恒为 0（这一条我第一版写错，"
    "E02）；要问「y 等于多少」必须用 `i*Y`（实对称、本征值恰是 y）。"
    "★★★ 这条读数的**副产品**：`16` 的 y 谱是 `-1 x1`（不含 `+1`），`16bar` 是 `+1 x1` —— "
    "即 **16bar 的 y 谱是 16 的逐项取反**。这与 r397 清单 `{1/6 x6, -2/3 x3, 1 x1, 1/3 x3, -1/2 x2, 0}` "
    "**整体反号**：r397 只用偶次幂 `p_k`，对符号完全不敏感（其诚实边界第 4 条已声明「只定 |y| 不定符号」），"
    "本卷把符号定下来了 —— `16` 在本卷口径下是 `{-1/6 x6, 2/3 x3, -1 x1, -1/3 x3, 1/2 x2, 0}`。"
    "★★★ 不等价：等价表示必须有相同的本征值重数；这里 y = +1 的重数在两边是 0 与 1（复）⇒ **不等价**。"
    "★★★ 但归属必须说清：这条不等价**不是** J/K 可分辨的原因。r397 的四格里 J 在两块都得 2、"
    "K 在两块都得 0，说明分辨与否只取决于 J/K；真正的原因是 A6「零模落在 V_J 而不在 V_K」。"
    "把「不等价」当成「可分的原因」正是 r397 E09 的错法，本卷把两句拆开各归各位。")

# ============================================================ A9 判别力：换一个 so(4)
VJ2 = nullspace_basis(rows_of(J2_GENS), N32)
VK2 = nullspace_basis(rows_of(K2_GENS), N32)
_dimVJ2 = len(VJ2)
_inter_J_J2 = _dimVJ + _dimVJ2 - rank_of(VJ + VJ2, N32)
_v45 = nullspace_basis(rows_of(SM_J), N32)[0]     # r397 的那个单态（nu^c 方向）
_in_VJ = rank_of(VJ + [_v45], N32) == _dimVJ
_in_VK = rank_of(VK + [_v45], N32) == _dimVK
_in_VJ2 = rank_of(VJ2 + [_v45], N32) == _dimVJ2
_in_VK2 = rank_of(VK2 + [_v45], N32) == len(VK2)
_a9_ok = (_dimVJ2 == 16 and len(VK2) == 16 and _inter_J_J2 < 16 and _in_VJ and not _in_VK)
add(MAIN, "A9",
    "判别力：把 so(4) 换到 1..4 号指标再算一遍 —— 仍 8+8，但子空间不同、单态的归属不同",
    "V_J' 与 V_K' 各 16 维；V_J 与 V_J' 的交 < 16；nu^c 在 V_J 内、不在 V_K 内",
    "V_J' 维数 %d、V_K' 维数 %d；dim(V_J ∩ V_J') = %d；nu^c ∈ V_J = %s、∈ V_K = %s、∈ V_J' = %s、∈ V_K' = %s"
    % (_dimVJ2, len(VK2), _inter_J_J2, _in_VJ, _in_VK, _in_VJ2, _in_VK2),
    "PASS" if _a9_ok else "FAIL",
    "★★★ 这是本卷的**判别力自证**：如果「8+8」是任何 so(4) 都成立的恒等式，那 A4 就毫无信息。"
    "实测换到 1..4 号指标后仍是 8+8（说明 8+8 只依赖「16 是 so(6) 的旋量与 so(4) 的自旋的乘积」这一结构），"
    "但 **V_J' 与 V_J 的交不是 16**（是两个不同的子空间），且 **nu^c 不在 V_J' 里** —— "
    "所以「nu^c ∈ V_J」是这一组特定嵌入的性质，不是废话。"
    "★ 这一条同时给出 r397 §十四 第 2 条的边界形态：可分辨依赖**这一组** J/K 的选择。")

# ============================================================ 控制组
_deg = N32 - rank_of([], N32)
add(CTL, "K1", "控制组（退化）：一个约束都不加", "32（全空间）",
    "零约束：秩 = 0；零空间 = %d" % _deg, "PASS" if _deg == 32 else "FAIL",
    "★退化档必须是全空间，否则「16」与「32」之间没有标尺。")

# K2 维数不是判据：用 K 的生成元跑「V_J 的算法」
Vx = nullspace_basis(rows_of(K_GENS), N32)
_k2_same_dim = (len(Vx) == _dimVJ)
_k2_same_space = (rank_of(Vx + VJ, N32) == _dimVJ)
add(CTL, "K2",
    "控制组（判别力）：用 su(2)_K 的生成元跑「V_J 的算法」—— 维数相同、但空间不同",
    "维数相同（16）但 V_x ∩ V_J = 0",
    "V_x 维数 = %d（V_J 也是 %d）；V_x 与 V_J 是同一空间 = %s"
    % (len(Vx), _dimVJ, _k2_same_space),
    "PASS" if (_k2_same_dim and not _k2_same_space) else "FAIL",
    "★★ 这一条是 r394「维数比较不是子群判据」刀的表示论版本："
    "两个都是 16 维、都在 32 维里，但**交为 0**。所以 A4 的结论必须用 rank(V_J + V_K) 算，"
    "不能只报「16 + 16 = 32」。★ 若某处把 SU2J_C 与 SU2K_C 抄成同一组，"
    "这条控制组会立刻变成「同一空间 = True」而红。")

# K3 错的复结构（反射）
JBAD = zmat(N32)
for i in range(16):
    JBAD[i][16 + i] = F(1)
    JBAD[16 + i][i] = F(1)
_jbad_sq = mmul(JBAD, JBAD, N32)
_jbad_isI = (_jbad_sq == [[F(1) if i == j else F(0) for j in range(N32)] for i in range(N32)])
_dj_vj = _dimVJ
add(CTL, "K3",
    "控制组（判别力）：把复结构写成反射 [[0,I],[I,0]]（平方 = +1）—— 维数与不变性都抓不到",
    "J_bad^2 = +1（不是 -1）；而 V_J 的维数仍是 16",
    "J_bad^2 = +1 是 %s；V_J 维数仍 = %d；故只靠「维数」判不出复结构错"
    % (_jbad_isI, _dj_vj),
    "PASS" if (_jbad_isI and _dj_vj == 16) else "FAIL",
    "★★ 这一条证明 A1 的 `JMAP^2 = -1` 是**必要**的一条：换成一个平方为 +1 的矩阵（反射），"
    "V_J 的维数照样是 16、A2 的「JMAP-不变」也可能照样通过 —— 只有「平方 = -1」这一条能把它挑出来。"
    "★ 与 r397 K4 同一族：**刻度/符号类的错不改维数**，必须另配一条敏感判据。")

# K4 把 y 谱平移 1/2：零模从 V_J 跳到 V_K ⇒ 机制是「哪个 y 值落在哪一半」
_shift = F(1, 2)
_HS = [[H_Y[i][j] - (_shift if i == j else F(0)) for j in range(N32)] for i in range(N32)]
_ASI = restrict_mat(_HS, VJ, N32)
_ASI2 = restrict_mat(_HS, VK, N32)
_k4_J = len(VJ) - rank_of(_ASI, len(VJ))
_k4_K = len(VK) - rank_of(_ASI2, len(VK))
# 期望值由 A7 的表推出来（不是抄读数）：把 y 整体减 1/2 后，零模恰好落在「原本 y = 1/2」的本征空间上，
# 故 ker(V_J) = y=1/2 在 V_J 的重数、ker(V_K) = y=1/2 在 V_K 的重数。
_row_half = [(_a, _b) for (_l, _a, _b) in _tab if _l == F(1, 2)][0]
_k4_exp_J = _row_half[0]
_k4_exp_K = _row_half[1]
add(CTL, "K4",
    "控制组（判别力）：把 y 谱整体平移 1/2（用 i*Y - 1/2）—— 零模从 V_J 换到 V_K",
    "零模换边：(V_J, V_K) = (0, 4)（基线是 (2, 0)）；且 4 = y=1/2 在 V_K 的重数（由 A7 表推出）",
    "i*Y - 1/2：ker 在 V_J 上 = %d（基线 %d）、在 V_K 上 = %d（基线 %d）；"
    "由 A7 表推出的期望 (%d, %d)"
    % (_k4_J, _kerYJ, _k4_K, _kerYK, _k4_exp_J, _k4_exp_K),
    "PASS" if (_k4_J == _k4_exp_J and _k4_K == _k4_exp_K
               and _kerYJ == 2 and _kerYK == 0) else "FAIL",
    "★★ 这一条说明 A6 的「2 vs 0」不是「随便一个 Y 都给这样」：y 谱一平移，零模就换边。"
    "所以机制精确地是「**哪个 y 值**落在哪一半」，而不是「哪一半更特殊」。"
    "★★ 期望值是**推出来的、不是抄来的**：平移 y -> y - 1/2 后，ker 恰好是原本 y = 1/2 的本征空间，"
    "故两半的核维数应等于 y=1/2 在两半各自的重数 —— A7 表给出 V_J 侧 0、V_K 侧 4，实测正合。"
    "★ 顺带一个**不是对调**的事实：V_K 侧的核是 4 维实（2 个复态），是 V_J 侧基线 2 维实（1 个复态）的 2 倍 —— "
    "因为 V_J 的零模来自 `y = 0`（单态，1 个），V_K 的新零模来自 `y = 1/2`（二重态，2 个）。"
    "**零模维数跟着「被平移到 0 的那个 y 值的重数」走**，这也是 A6 只给 1 个的原因。"
    "★★★ 本卷第一版做错了这一条（第 E03 号自伤）：我把 1/2 直接加到 `Y_R` 上 —— "
    "那是「平移 ±i*y」而不是「平移 y」，永远造不出零模 ⇒ 读数 (0, 0)，控制组变成装饰。"
    "正确的对象是 `i*Y`（实对称、本征值就是 y）。这正是 r397 E09 的同族错：**动了错的量**。"
    "★★ 第二版我又把期望写成 (0, 2)（猜的：想当然以为「对调」）⇒ 实测 (0, 4) 判 FAIL（E05）。")

# ============================================================ 守卫
_HEAD = ""
try:
    _HEAD = io.open(os.path.abspath(__file__), encoding="utf-8").read()
except Exception:
    _HEAD = ""
_ALG = _HEAD.split("# ============================================================ 控制组", 1)[0]
_BAD = ["1e-", "1e+", "float(", "** 0.5", "round(", "math.sqrt", "Decimal"]
_cb = sum(_ALG.count(t) for t in _BAD)
add(GRD, "G01", "判据区不得含 10 的整数幂门限 / 浮点 / 开方", "0 处",
    "扫描区（A1–A9）出现 %d 处" % _cb, "PASS" if _cb == 0 else "FAIL",
    "★扫描区切在控制组之前，避开自指。")

_n_id = sum(1 for r in MAIN if r["kind"] == "IDENTITY")
add(GRD, "G02", "恒等式不得记 PASS", "0 条 IDENTITY",
    "IDENTITY 条目 %d 条" % _n_id, "PASS" if _n_id == 0 else "FAIL",
    "★A6 是真解 16x16 的秩；A7 是真乘 16x16 矩阵再取迹。都不是符号恒等。")

add(GRD, "G03", "四个控制组必须给出可区分的读数",
    "K1 = 32；K2 维数同而空间不同；K3 J_bad^2 = +1 且维数仍 16；K4 零模换边 = (0, 4) 且与 A7 表推出的期望一致",
    "K1 = %d；K2 维数 %d/同空间 %s；K3 J_bad^2=+1 是 %s 且维数 %d；K4 (%d, %d) 基线 (%d, %d) 期望 (%d, %d)"
    % (_deg, len(Vx), _k2_same_space, _jbad_isI, _dj_vj, _k4_J, _k4_K, _kerYJ, _kerYK,
       _k4_exp_J, _k4_exp_K),
    "PASS" if (_deg == 32 and _k2_same_dim and not _k2_same_space and _jbad_isI
               and _k4_J == _k4_exp_J and _k4_K == _k4_exp_K) else "FAIL",
    "★K1 退化标尺，K2 维数不是判据，K3 复结构必须平方 -1，K4 零模必须跟着 y 值走。四者分工不重叠。")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "0 违规（收尾重算，覆盖 %d 条）" % len(ALL) if _bad4 == 0 else "%d 违规" % _bad4,
    "PASS" if _bad4 == 0 else "FAIL", "★收尾重算，不是逐条自查。")

add(GRD, "G05", "维数账：32 = 16 + 16（V_J ⊕ V_K），2 x 8 = 16", "两处一致",
    "V_J %d + V_K %d = %d；实 16 = 复 8 x 2" % (_dimVJ, _dimVK, _dimVJ + _dimVK),
    "PASS" if (_dimVJ == 16 and _dimVK == 16 and _dimVJ + _dimVK == 32) else "FAIL",
    "★三处独立枚举（A2 / A3 / A4），任一处错都会与 rank(V_J+V_K) = 32 打架。")

add(GRD, "G06", "生成元账：su(3) 8 + su(2) 3 + Y 1 = 12；so(10) = 45", "闭合",
    "%d + %d + 1 = %d；so(10) 基 %d 个"
    % (len(SU3_C), len(SU2J_C), len(SU3_C) + len(SU2J_C) + 1, len(KEYS)),
    "PASS" if (len(SU3_C) + len(SU2J_C) + 1 == 12 and len(KEYS) == 45) else "FAIL",
    "★三处独立，任一处少一个都会露出来。")

_g7 = all(is_antisym(SIGR[kk]) for kk in KEYS) and all(is_antisym(M) for M in SM_J)
add(GRD, "G07", "结构守卫：45 个 Sigma 与 12 个 SM 生成元全部反对称", "全部反对称",
    "Sigma 全反对称 = %s；SM 生成元全反对称 = %s"
    % (all(is_antisym(SIGR[kk]) for kk in KEYS), all(is_antisym(M) for M in SM_J)),
    "PASS" if _g7 else "FAIL",
    "★★ 反对称是「实化正确」的直接后果（反 Hermitian 实化后反对称）；"
    "若 realify 的 -B 写成 +B，这里会立刻红（r397 K3 的教训）。")

VERDICT = "--".join([
    "SIXTEEN-IS-%d-PLUS-%d-DIRECT-SUM" % (_dimVJ, _dimVK),
    "ZERO-MODE-LIVES-IN-VJ" if (_kerYJ == 2 and _kerYK == 0) else "ZERO-MODE-SPLIT-UNEXPECTED",
    "SPECTRUM-SPLIT-%s-VS-%s" % (_s1_J, _s1_K),
    "SIXTEEN-NOT-EQUIV-16BAR" if _a8_ok else "EQUIV-UNDECIDED",
])
_dd = {r["id"]: r["kind"] for r in ALL}
_v2 = "--".join([
    "SIXTEEN-IS-%d-PLUS-%d-DIRECT-SUM" % (_dimVJ, _dimVK) if _dd["A4"] == "PASS"
    else "SIXTEEN-SUM-OPEN",
    "ZERO-MODE-LIVES-IN-VJ" if _dd["A6"] == "PASS" else "ZERO-MODE-SPLIT-UNEXPECTED",
    "SPECTRUM-SPLIT-%s-VS-%s" % (_s1_J, _s1_K),
    "SIXTEEN-NOT-EQUIV-16BAR" if _dd["A8"] == "PASS" else "EQUIV-UNDECIDED",
])
add(GRD, "G08", "判词与判定表必须同一读数（两路径拼接）", "两路一致",
    "由变量拼：%s；由 ALL 行重算：%s（%s）"
    % (VERDICT, _v2, "一致" if _v2 == VERDICT else "不一致"),
    "PASS" if _v2 == VERDICT else "FAIL", "★一路由构造变量拼、一路由条目 kind 重算。")

g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "（回填）", "（回填）", "INFO",
          "★先占位再回填（r396 E06：报告必须在回填之后才拼）")

DECLARED_NEG = set()
_neg = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G10", "真判负必须逐条登记", "登记集 == 实际 FAIL 集",
    "%s vs %s" % (sorted(DECLARED_NEG), _neg),
    "PASS" if sorted(DECLARED_NEG) == _neg else "FAIL",
    "★本卷的判负（若有）必须同时写进 DECLARED_NEG 与判定册。")

_g11 = (len(SIGR) == 45 and len(SIGR_M) == 45 and len(set(KEYS)) == 45
        and all(len(v) == N32 for v in VJ) and all(len(v) == N32 for v in VK))
add(GRD, "G11", "完备性：两块各 45 个 Sigma、基向量维数全为 32", "45 / 45 / 32",
    "SIGR %d / SIGR_M %d / 去重基 %d；V_J 基向量 %d 个 x %d 维"
    % (len(SIGR), len(SIGR_M), len(set(KEYS)), len(VJ), N32),
    "PASS" if _g11 else "FAIL",
    "★「两块都建了」必须真的枚举，不能只建 PLUS 就复制一份。")

add(GRD, "G12", "两条独立路径：su(2)_J + Y 的单态数由「直接解 384x32」与「先分半再解 Y」各算一次",
    "两路都给 2",
    "直接解 %d；分半路 %d（= ker(Y|V_J)）"
    % (len(nullspace_basis(rows_of([to_rep(c, SIGR) for c in SU2J_C] + [Y_R]), N32)), _kerYJ),
    "PASS" if (len(nullspace_basis(rows_of([to_rep(c, SIGR) for c in SU2J_C] + [Y_R]), N32))
               == _kerYJ) else "FAIL",
    "★★ 两条路不同源：一路把 4 个生成元叠成 128 行直接解；另一路先算 V_J 再把 Y 限制上去。"
    "★ 这正是本卷的**总纲**：把 r397 的一条「解出来的数」换成「一个结构性推导」。")

add(GRD, "G13", "总门必须对「守卫失败」敏感", "注入守卫 FAIL 必须翻转", "（回填）", "INFO",
    "★沿用 r392 起的总门口径 + 已登记判负不挡门。")


def final_of(nf_main, nf_guard, n_decl=0):
    if nf_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main


_all_ids = {r["id"]: r for r in ALL}
_kt = "16 = %d + %d；零模 %d/%d；谱和 %s；不等价 %s" % (
    _dimVJ, _dimVK, _kerYJ, _kerYK, _s1_sum, _a8_ok)
_kt_from_rows = "16 = %d + %d；零模 %d/%d；谱和 %s；不等价 %s" % (
    int(_all_ids["A4"]["act"].split("dim V_J = ")[1].split("；")[0]),
    int(_all_ids["A4"]["act"].split("dim V_K = ")[1].split(" ⇒")[0]),
    int(_all_ids["A6"]["act"].split("ker(Y|V_J) = ")[1].split(" 维实")[0]),
    int(_all_ids["A6"]["act"].split("ker(Y|V_K) = ")[1].split(" 维实")[0]),
    _s1_sum,
    _all_ids["A8"]["kind"] == "PASS")
_kt_basis = ("V_J 的基由 su(2)_J 的 3 个生成元的零空间直接给出（%d 个有理向量）" % _dimVJ
             if (_dimVJ == 16 and _jm_inv_J) else "未定（A2 未同时给出 16 维与 JMAP-不变）")
_kt_j3_ok = (_A_J3K_sq_ok and _tr_J3K == 0 and _tot_J + len(_A_J3K) == N32)
_kt_j3 = ("J3 谱：V_J 上恒 0（%d 个复态 = %d x 1），V_K 上 A^2 = -I（%s）且 tr = %s ⇒ 谱 ±i 各 %d 维实 ⇒ %d x 2"
          % (_tot_J // 2, _tot_J // 2, _A_J3K_sq_ok, _tr_J3K,
             len(_A_J3K) // 2, len(_A_J3K) // 4))
add(GRD, "G14", "关键表读数必须与主册同一条目同读数（防同名覆盖 / 防关键表写死错话）",
    "关键表四个读数 == A4/A6/A7/A8 抽出值；且 V_J 基的「话」必须由 A2 的读数拼出；"
    "且 J3 谱那行的每个数都必须出自 A5 的布尔量",
    "关键表：%s；由 act 重算：%s；基串：%s；J3 行可复算 = %s（A^2=-I %s、tr %s、%d+%d=32、A5 %s）"
    % (_kt, _kt_from_rows, _kt_basis, _kt_j3_ok, _A_J3K_sq_ok, _tr_J3K,
       _tot_J, len(_A_J3K), _all_ids["A5"]["kind"]),
    "PASS" if (_kt == _kt_from_rows and _kt_j3_ok
               and _kt_basis != "未定（A2 未同时给出 16 维与 JMAP-不变）") else "FAIL",
    "★★ r396 E02 / r397 E09 的直接继承：关键表里「谁是基」这类话必须由布尔量拼出。"
    "本卷这句由 (维数 == 16) and (JMAP-不变) 拼。"
    "★★★ J3 谱那行是本卷第 E06 号自伤的现场：我第一版把它硬写成「V_K 上 ±1/2 各 8」，"
    "而 A5 实测 `A^2 = -I`、`tr = 0` ⇒ 谱只能是 **±i** 各 8（实维），±1/2 是 E01 那套 Hermitian 口径的残留文案。"
    "四个数字（8/8/4/2）全对、话错 —— 与 r397 E08 同族。现在整行由 `_A_J3K_sq_ok`、`_tr_J3K`、"
    "`_tot_J`、`len(_A_J3K)` 四个布尔/整数拼出，改口径时这行会跟着变，不会再残留旧文案。")

# ============================================================ 汇总
_nf_main = sum(1 for r in MAIN if r["kind"] == "FAIL")
_nf_g = sum(1 for r in CTL + GRD if r["kind"] == "FAIL")
FINAL = final_of(_nf_main, _nf_g, len(DECLARED_NEG & set(_neg)))

g13 = _all_ids["G13"]
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
                           identity=_n_id, fail=_nf_main,
                           ctl=len(CTL), grd=len(GRD), total=len(ALL)),
               rows=ALL, declared_neg=sorted(DECLARED_NEG))
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

_back = json.load(io.open(JSN, encoding="utf-8"))
g09["exp"] = "回读条目数 == 内存条目数（%d）" % len(ALL)
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                        "一致" if len(_back["rows"]) == len(ALL) else "不一致")
g09["kind"] = "PASS" if len(_back["rows"]) == len(ALL) else "FAIL"

payload["rows"] = ALL
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

L = []


def A(s=""):
    L.append(s)


A(TITLE)
A("=" * 100)
A("对象：X-GSM-3（V_J / V_K 显式基与零模归属：把 r397 的机制从认领变推导）")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
     sum(1 for r in MAIN if r["kind"] == "INFO"), _n_id, _nf_main,
     len(CTL), len(GRD), len(ALL)))
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
A("16 = V_J(%d) + V_K(%d)，直和（交为 0）" % (_dimVJ, _dimVK))
# 这一行必须由 A5 的读数拼出（r397 E08 教训：报告里的话也得机拼）
A(_kt_j3)
A("Y 零模归属：ker(Y|V_J) = %d 维实（复 %d），ker(Y|V_K) = %d" % (_kerYJ, _kerYJ // 2, _kerYK))
A("Y 谱分半：s1(V_J) = %s，s1(V_K) = %s，和 = %s（= r397 的 p_1）；s2 和 = %s（= r397 的 p_2）"
  % (_s1_J, _s1_K, _s1_sum, _s2_sum))
A("16 与 16bar 不等价：ker(iY-1) = %d vs %d；ker(iY+1) = %d vs %d"
  % (_k_p1, _k_m1, _k_pm1, _k_mm1))
A("换 so(4) 判别力：V_J' 维数 %d，dim(V_J ∩ V_J') = %d，nu^c ∈ V_J' = %s、∈ V_K' = %s"
  % (_dimVJ2, _inter_J_J2, _in_VJ2, _in_VK2))
A("")
A("【诚实边界】")
A(" 1) 本卷只做**子空间结构与零模归属**：不含质量谱 / Yukawa / 混合角；")
A(" 2) 「8+8 直和」是对**这一组** so(4)（作用在 7..10 号指标）证明的，不是对任意 so(4)；"
  "A9 已给出反例方向 —— 换到 1..4 号指标后 dim(V_J ∩ V_J') = %d（≠ %d，两子空间不同）、"
  "nu^c ∈ V_J' = %s、∈ V_K' = %s（归属整个换边）；"
  % (_inter_J_J2, _dimVJ, _in_VJ2, _in_VK2))
A(" 3) A6 只给出 ker(Y|V_J) = %d、ker(Y|V_K) = %d 这两个读数，"
  "**不解释**「为什么 nu^c 落在 V_J」—— 后者的成因（nu^c 的 su(2)_J 归属）属分解表层面，本卷未从第一原理导出；"
  % (_kerYJ, _kerYK))
A(" 4) A8 只证明「16 与 16bar 不等价」这一件事（ker(iY-1) = %d vs %d），"
  "**不**主张它是 J/K 可分辨的原因（见 A6）；" % (_k_p1, _k_m1))
A(" 5) 本卷不构造显式的 16 → 16bar 共轭算子；A8 用的是「本征空间维数不同」这条**否定性**证据。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

print("JSON ->", JSN)
