# -*- coding: utf-8 -*-
"""TUFT-r402  攻 X-GSM-7：矩阵层共轭 —— B 实现 16bar = B·conj(16)·B^{-1}，B 恰为 Gamma 奇位积

纯标准库（Fraction，判据区无浮点、无随机）。复用 r400 的代数底座（同一 Gamma / Sigma / realify）。

r401 留下的硬边界（其 `_report` 的【诚实边界】第 2 条）：
  「本卷全部在权层：不构造 16 <-> 16bar 的矩阵层共轭算子，也不在矩阵层验证表示不等价」
本卷把这一层补上 —— 矩阵层的三个独立判据 + 共轭算子的显式构造与它的 Clifford 出处。

  A1  前提复核：两类权不相交、奇类 == −偶类、match 双射（r401 A1 读数反抄 + 本卷矩阵路互印）
  A2  Hom 双向为零：Hom(16,16bar) 与 Hom(16bar,16) 的 Cartan 支撑都是 0
      —— 矩阵层不等价的权层机制：宇称账（偶 {0,2,4} / 奇 {1,3,5}，同权须同宇称）
  A3  Hom(16,16) = 标量：交换子两步直解（Cartan 消元 -> 对角；非对角方程 -> 全等）
      —— 复维 1 = Schur；16 不可约的计算判据
  A4  Dirac 系统（16 x 16bar 不变量空间）：全复数 1280 行，解空间实维 2 = 复维 1；
      T0 实向量全 ±1；conj(rhoM) 的权 == PLUS 权（同构 16 的矩阵对角直读）⇒ 方程即 Hom(16,16)
  A5  反 Hermitian 桥：rho^T == −conj(rho)；两块各 45/45；
      独立路 = Gamma 的 epsilon 账（10 个 Gamma 逐个验证 G^T == conj(G)，全 +1）
  A6  B = T0^T 主判定：rhoM·B == B·conj(rhoP) 违例 0/45（A4 取转置 + A5 的桥）；
      B·B^T == I（B 正交，B^{-1} = B^T）；实化秩 32
  A7  B 的权层结构与 t_j 闭式：列 j 支撑恰在 match[j]、值 = t_j；
      t_j == sign(w1·w3·w5)（闭式来自权，T0 来自 nullspace —— 两路）
  A8  B 恰为 Gamma 奇位积：P* = [[0,B^{-1}],[B,0]] 嵌入 32 维后 P*·sig + sig^T·P* 违例 0/45
      （32 维 Dirac 表示自共轭的显式实现）；P* 与 Gamma_0·Gamma_2·Gamma_4·Gamma_6·Gamma_8
      （mask 341）逐元相等；换块 Gamma 乘积 512 个中恰 2 个满足（341 与 682 = 偶位积，
      块标量 (−i, +i) 独立）；Gamma 权作用表：每个 Gamma 翻恰一个权位、16 个非零元
  A9  二次不变量账：16 x 16 与 16bar x 16bar 的 Cartan 支撑均 0（无 Majorana 二次项）；
      16 x 16bar 支撑 = 16 = match 对、解空间复维 1（与 A4 同一对象，同源不另计）—— Dirac 项唯一
"""
import ast
import io
import json
import os
from fractions import Fraction as F

RID = "r402"
TITLE = ("TUFT-r402_攻X-GSM-7_矩阵层共轭_16bar等于B共轭B逆的显式实现_"
         "B恰为Gamma奇位积_Hom双向为零_Dirac项唯一且无Majorana二次项_"
         "tj闭式signw1w3w5_精算_2026-11-05")
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


def _ftp(t):
    return "(" + ",".join(str(x) for x in t) + ")"


def _ftv(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def _fcp(lam):
    (re, im) = lam
    if im == 0:
        return str(re)
    if re == 0:
        return "%s*i" % str(im)
    return "%s%si" % (str(re), "+" if im > 0 else "")

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




# ============================================================ 复矩阵工具（本卷新增）
def cT(M):
    (R, I) = M
    n = len(R)
    return ([[R[j][i] for j in range(n)] for i in range(n)],
            [[I[j][i] for j in range(n)] for i in range(n)])


def cbar(M):
    return (M[0], [[-x for x in row] for row in M[1]])


def czero(M):
    return all(M[0][i][j] == 0 and M[1][i][j] == 0
               for i in range(len(M[0])) for j in range(len(M[0])))


def cmulS(A, s):
    return ([[s * x for x in row] for row in A[0]], [[s * x for x in row] for row in A[1]])


def ceye(n):
    return ([[F(1) if i == j else F(0) for j in range(n)] for i in range(n)],
            [[F(0)] * n for _ in range(n)])


def sgn(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


# ============================================================ 32 维全模与 16bar 块的 Sigma
SIG32 = {}
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    SIG32[(a, b)] = ([[x / 4 for x in row] for row in _Cm[0]],
                     [[x / 4 for x in row] for row in _Cm[1]])
SIGC_M = {}
for (a, b) in KEYS:
    SIGC_M[(a, b)] = restrict(SIG32[(a, b)], MINUS)

WP = [tuple(w) for w in W]
HC_M = [SIGC_M[(2 * i, 2 * i + 1)] for i in range(5)]
WM = [tuple(HC_M[i][1][k][k] for i in range(5)) for k in range(NC)]

# ============================================================ 权配对（w- == −w+ 的双射）
match = {}
match_unique = True
for j in range(NC):
    neg = tuple(-x for x in WP[j])
    hit = [k for k in range(NC) if WM[k] == neg]
    if len(hit) != 1:
        match_unique = False
        hit = hit[:1]
    match[j] = hit[0] if hit else -1
match_bijective = match_unique and len(set(match.values())) == NC and -1 not in set(match.values())

# ============================================================ 全复数 Dirac 系统
# 未知 t_l = a_l + i*b_l（32 个实未知量，变量序 a_0..a_15, b_0..b_15）
# 方程：rhoP·T + T·(rhoM)^T == 0，T[l][k] = t_l * delta(k, match[l])
rows_d = []
for kk in KEYS:
    (Rp, Ip) = SIGC[kk]
    (Rm, Im) = SIGC_M[kk]
    for j in range(NC):
        for k in range(NC):
            lstar = [l for l in range(NC) if match[l] == k]
            cre = [F(0)] * (2 * NC)
            cim = [F(0)] * (2 * NC)
            if lstar:
                l = lstar[0]
                cre[l] += Rp[j][l]
                cim[l] += Ip[j][l]
                cre[NC + l] += -Ip[j][l]
                cim[NC + l] += Rp[j][l]
            cre[j] += Rm[k][match[j]]
            cim[j] += Im[k][match[j]]
            cre[NC + j] += -Im[k][match[j]]
            cim[NC + j] += Rm[k][match[j]]
            if any(x != 0 for x in cre):
                rows_d.append(cre)
            if any(x != 0 for x in cim):
                rows_d.append(cim)
rows_d = [r for r in rows_d if any(x != 0 for x in r)]
ns_d = nullspace_basis(rows_d, 2 * NC)

T0 = None
for _v in ns_d:
    if all(x == 0 for x in _v[NC:]) and any(x != 0 for x in _v[:NC]):
        T0 = list(_v[:NC])
        break
T0_real = T0 is not None


def Tmat(t):
    R = [[F(0)] * NC for _ in range(NC)]
    I = [[F(0)] * NC for _ in range(NC)]
    for j in range(NC):
        R[j][match[j]] = t[j]
    return (R, I)


TM = Tmat(T0) if T0_real else Tmat([F(0)] * NC)
B = cT(TM)

# A4 直接验证路：rhoP·T + T·(rhoM)^T 逐对
bad_T = 0
for kk in KEYS:
    if not czero(cadd(cmul(SIGC[kk], TM), cmul(TM, cT(SIGC_M[kk])))):
        bad_T += 1

# A6 主判定：rhoM·B == B·conj(rhoP) 逐对
bad_B = 0
for kk in KEYS:
    if not czero(cadd(cmul(SIGC_M[kk], B), cmul(B, cbar(SIGC[kk])), -1)):
        bad_B += 1

# K2 负控：去 conj（rhoM·B == B·rhoP）
bad_Bnc = 0
for kk in KEYS:
    if not czero(cadd(cmul(SIGC_M[kk], B), cmul(B, SIGC[kk]), -1)):
        bad_Bnc += 1

# B 正交与秩
BBt_ok = czero(cadd(cmul(B, cT(B)), ceye(NC), -1))
Brank = rank_of([r[:] for r in realify(B)], 32)

# ============================================================ epsilon 账与反 Hermitian
eps = []
for a in range(10):
    if czero(cadd(cT(GAM[a]), cbar(GAM[a]))):
        eps.append(-1)
    elif czero(cadd(cT(GAM[a]), cbar(GAM[a]), -1)):
        eps.append(1)
    else:
        eps.append(0)
eps_pairs = sum(1 for (a, b) in KEYS if eps[a] * eps[b] == 1)


def anti_herm_count(REP):
    n = 0
    for kk in KEYS:
        (Rr, Ii) = REP[kk]
        ok = all(Rr[i][j] == -Rr[j][i] and Ii[i][j] == Ii[j][i]
                 for i in range(NC) for j in range(NC))
        if ok:
            n += 1
    return n


ahP = anti_herm_count(SIGC)
ahM = anti_herm_count(SIGC_M)

# ============================================================ 交换子两步直解（Hom(16,16)）
# 一步：Cartan 消元 —— [X, H_m] == 0 且权互异 ⇒ X 支撑只能在同权位（= 对角）
sup_comm = [(i, j) for i in range(NC) for j in range(NC)
            if all(W[i][m] == W[j][m] for m in range(5))]
# 二步：对角 X = diag(x_j)，非对角非零元给方程 x_i == x_j（复 ⇒ 实虚两行）
rows_c = []
for kk in KEYS:
    (Rr, Ii) = SIGC[kk]
    for i in range(NC):
        for j in range(i + 1, NC):
            if Rr[i][j] != 0 or Ii[i][j] != 0 or Rr[j][i] != 0 or Ii[j][i] != 0:
                r1 = [F(0)] * (2 * NC)
                r1[i] = F(1)
                r1[j] = F(-1)
                r2 = [F(0)] * (2 * NC)
                r2[NC + i] = F(1)
                r2[NC + j] = F(-1)
                rows_c.append(r1)
                rows_c.append(r2)
rows_c = [list(r) for r in {tuple(r) for r in rows_c}]
ns_c = nullspace_basis(rows_c, 2 * NC)

# 连通分量（同一边界数据的图路读数）
_par = list(range(NC))


def _find(x):
    while _par[x] != x:
        _par[x] = _par[_par[x]]
        x = _par[x]
    return x


for kk in KEYS:
    (Rr, Ii) = SIGC[kk]
    for i in range(NC):
        for j in range(i + 1, NC):
            if Rr[i][j] != 0 or Ii[i][j] != 0 or Rr[j][i] != 0 or Ii[j][i] != 0:
                _a, _b = _find(i), _find(j)
                if _a != _b:
                    _par[_a] = _b
comps = len({_find(i) for i in range(NC)})

# ============================================================ Hom 支撑（双向）与二次不变量支撑
sup_pm = [(j, k) for j in range(NC) for k in range(NC) if WP[j] == WM[k]]
sup_mp = [(j, k) for j in range(NC) for k in range(NC) if WM[j] == WP[k]]
sup_pp = [(j, k) for j in range(NC) for k in range(NC)
          if tuple(-x for x in WP[j]) == WP[k]]
sup_mm = [(j, k) for j in range(NC) for k in range(NC)
          if tuple(-x for x in WM[j]) == WM[k]]
sup_pm_inv = [(j, k) for j in range(NC) for k in range(NC)
              if WM[k] == tuple(-x for x in WP[j])]

# ============================================================ Gamma 权作用表
wdiff = {}
wnz = {}
for a in range(10):
    rel = set()
    n = 0
    (R, I) = GAM[a]
    for pi in range(NC):
        for mi in range(NC):
            if R[MINUS[mi]][PLUS[pi]] != 0 or I[MINUS[mi]][PLUS[pi]] != 0:
                rel.add(tuple(WM[mi][t] - WP[pi][t] for t in range(5)))
                n += 1
    wdiff[a] = sorted(rel)
    wnz[a] = n

# ============================================================ Gamma 乘积表（DP）与三组搜索
P = [None] * 1024
P[0] = ceye(32)
for mask in range(1, 1024):
    hb = mask.bit_length() - 1
    P[mask] = cmul(P[mask ^ (1 << hb)], GAM[hb])

cTSIG = {kk: cT(SIG32[kk]) for kk in KEYS}
cTSIGC = {kk: cT(SIGC[kk]) for kk in KEYS}


def block_offdiag(Pm):
    (R, I) = Pm
    for j in PLUS:
        for m in PLUS:
            if R[m][j] != 0 or I[m][j] != 0:
                return False
    for j in MINUS:
        for m in MINUS:
            if R[m][j] != 0 or I[m][j] != 0:
                return False
    return True


def block_keep(Pm):
    (R, I) = Pm
    for j in PLUS:
        for m in MINUS:
            if R[m][j] != 0 or I[m][j] != 0:
                return False
    for j in MINUS:
        for m in PLUS:
            if R[m][j] != 0 or I[m][j] != 0:
                return False
    return True


cands_swap = [m for m in range(1024) if m and block_offdiag(P[m])]
cands_keep = [m for m in range(1024) if m and block_keep(P[m])]
_kk0 = KEYS[0]

hits_neg = []
for m in cands_swap:
    if not czero(cadd(cmul(P[m], SIG32[_kk0]), cmul(cTSIG[_kk0], P[m]))):
        continue
    if all(czero(cadd(cmul(P[m], SIG32[kk]), cmul(cTSIG[kk], P[m]))) for kk in KEYS):
        hits_neg.append(m)

hits_pos = []
for m in cands_swap:
    if not czero(cadd(cmul(P[m], SIG32[_kk0]), cmulS(cmul(cTSIG[_kk0], P[m]), -1))):
        continue
    if all(czero(cadd(cmul(P[m], SIG32[kk]), cmulS(cmul(cTSIG[kk], P[m]), -1)))
           for kk in KEYS):
        hits_pos.append(m)

hits_keep = []
for m in cands_keep:
    PP = restrict(P[m], PLUS)
    for sg in (1, -1):
        if all(czero(cadd(cmul(PP, SIGC[kk]), cmulS(cmul(cTSIGC[kk], PP), sg)))
               for kk in KEYS):
            hits_keep.append(m)
            break

per_pair_pass = 0
for m in cands_keep:
    PP = restrict(P[m], PLUS)
    ok = True
    for kk in KEYS:
        if not any(czero(cadd(cmul(PP, SIGC[kk]), cmulS(cmul(cTSIGC[kk], PP), sg)))
                   for sg in (1, -1)):
            ok = False
            break
    if ok:
        per_pair_pass += 1

# ============================================================ P* 的 32 维嵌入与 Gamma 奇位积
def embed_offdiag(PMblock, MMblock):
    R = [[F(0)] * 32 for _ in range(32)]
    I = [[F(0)] * 32 for _ in range(32)]
    for a in range(NC):
        for b in range(NC):
            R[PLUS[a]][MINUS[b]] = PMblock[0][a][b]
            I[PLUS[a]][MINUS[b]] = PMblock[1][a][b]
            R[MINUS[a]][PLUS[b]] = MMblock[0][a][b]
            I[MINUS[a]][PLUS[b]] = MMblock[1][a][b]
    return (R, I)


Pstar = embed_offdiag(TM, B)
bad_Pstar = 0
for kk in KEYS:
    if not czero(cadd(cmul(Pstar, SIG32[kk]), cmul(cTSIG[kk], Pstar))):
        bad_Pstar += 1
bad_Pstar_pos = 0
for kk in KEYS:
    if not czero(cadd(cmul(Pstar, SIG32[kk]), cmulS(cmul(cTSIG[kk], Pstar), -1))):
        bad_Pstar_pos += 1

eq_masks = [m for m in range(1024) if czero(cadd(P[m], Pstar, -1))]


def scalar_ratio(A, Bm):
    lam = None
    n = len(A[0])
    for i in range(n):
        for j in range(n):
            if A[0][i][j] != 0 or A[1][i][j] != 0:
                br, bi = Bm[0][i][j], Bm[1][i][j]
                if br == 0 and bi == 0:
                    return None
                ar, ai = A[0][i][j], A[1][i][j]
                den = br * br + bi * bi
                lam = ((ar * br + ai * bi) / den, (ai * br - ar * bi) / den)
                break
        if lam is not None:
            break
    if lam is None:
        return (F(0), F(0)) if czero(A) else None
    (lr, li) = lam
    for i in range(n):
        for j in range(n):
            ar, ai = A[0][i][j], A[1][i][j]
            br, bi = Bm[0][i][j], Bm[1][i][j]
            xr = lr * br - li * bi
            xi = lr * bi + li * br
            if ar != xr or ai != xi:
                return None
    return lam


def blocks_of(Pm):
    (R, I) = Pm
    P12 = ([[R[PLUS[a]][MINUS[b]] for b in range(NC)] for a in range(NC)],
           [[I[PLUS[a]][MINUS[b]] for b in range(NC)] for a in range(NC)])
    P21 = ([[R[MINUS[a]][PLUS[b]] for b in range(NC)] for a in range(NC)],
           [[I[MINUS[a]][PLUS[b]] for b in range(NC)] for a in range(NC)])
    return (P12, P21)


blk_scal = {}
for m in hits_neg:
    (P12, P21) = blocks_of(P[m])
    blk_scal[m] = (scalar_ratio(P12, TM), scalar_ratio(P21, B))

# DP 完整性抽查：直接乘积 vs DP 表
def direct_prod(bits):
    M = ceye(32)
    for a in bits:
        M = cmul(M, GAM[a])
    return M


dp_check = {}
for (m, bits) in ((341, [0, 2, 4, 6, 8]), (682, [1, 3, 5, 7, 9]),
                  (7, [0, 1, 2]), (0, [])):
    dp_check[m] = czero(cadd(P[m], direct_prod(bits), -1))

# ============================================================ A1 前提复核
_a1_inter = len(set(WP) & set(WM))
_a1_neg = set(WM) == {tuple(-x for x in w) for w in WP}
_a1_ok = (_a1_inter == 0 and _a1_neg and match_bijective)
add(MAIN, "A1", "前提复核：两类权不相交、奇类 == −偶类、match 双射",
    "相交 0；集合取反相等 True；match 双射 True（r401 A1 读数反抄：偶 {0,2,4} / 奇 {1,3,5} 不相交且互为取反）",
    "相交 %d；奇类==−偶类 %s；match 双射 %s" % (_a1_inter, _a1_neg, match_bijective),
    "PASS" if _a1_ok else "FAIL",
    "★ r401 的宇称类结论在本卷的矩阵底座上重立：WM 从 MINUS 块 Sigma 的虚部对角读（与 WP 同口径），"
    "match[j] = 唯一使 WM[k] == −WP[j] 的 k —— B 的列支撑将由它决定（A7）。")

# ============================================================ A2 Hom 双向为零
parP = cnt([sum(1 for x in w if x < 0) for w in WP])
parM = cnt([sum(1 for x in w if x < 0) for w in WM])
_a2_ok = (len(sup_pm) == 0 and len(sup_mp) == 0
          and sorted(parP.items()) == [(0, 1), (2, 10), (4, 5)]
          and sorted(parM.items()) == [(1, 5), (3, 10), (5, 1)])
add(MAIN, "A2", "Hom 双向为零：Hom(16,16bar) 与 Hom(16bar,16) 的 Cartan 支撑都是 0",
    "双向支撑 0/0 —— 宇称账：偶类 #(−1/2) 重数 {0:1，2:10，4:5}、奇类 {1:5，3:10，5:1}（= C(5,k)），"
    "同权须同宇称 ⇒ 双向都配不上对",
    "Hom(16,16bar) 支撑 %d；Hom(16bar,16) 支撑 %d；宇称账 偶 %s / 奇 %s"
    % (len(sup_pm), len(sup_mp), ctr_txt(parP), ctr_txt(parM)),
    "PASS" if _a2_ok else "FAIL",
    "★★ 矩阵层不等价的第一判据：交缠算子 C 须与 5 个 Cartan 同时对易 ⇒ 支撑只能在同权位；"
    "两条独立的计算路（逐对枚举 vs 宇称重数账）都给 0。r401 权层「两类不等价」的矩阵层机制。")

# ============================================================ A3 Hom(16,16) = 标量
_a3_ok = (len(sup_comm) == NC and len(ns_c) == 2 and comps == 1)
add(MAIN, "A3", "Hom(16,16) = 标量：交换子两步直解（16 不可约的计算判据）",
    "支撑 = 对角 16 位；非对角方程 nullspace 实维 2（= 复 1）—— 由 r397 的 55 对全量枚举已证 "
    "Cl(10,0) 手征块不可约 ⇒ Schur ⇒ 交换子 = 标量；恒等给出下界 1",
    "Cartan 消元后支撑 %d 位（== 对角 %s）；nullspace 实维 %d；连通分量 %d"
    % (len(sup_comm), len(sup_comm) == NC, len(ns_c), comps),
    "PASS" if _a3_ok else "FAIL",
    "★ 两步直解：一步用 [X,H_m]=0 + 权互异把支撑削到对角（同权位枚举）；二步用 45 个 Sigma 的"
    "非对角非零元给 x_i==x_j 方程再解。★ 连通分量 1 是同一边界数据的图路读数 —— "
    "「矩阵看着对」不等于「不可约」，交换子平凡才是计算判据（r397 老刀的复层版）。")

# ============================================================ A4 Dirac 系统
_conjM_w = {tuple(-x for x in w) for w in WM}
_a4_wpath = _conjM_w == set(WP)
_a4_t0pm1 = T0_real and sorted(set(T0)) == [F(-1), F(1)]
_a4_ok = (len(rows_d) == 1280 and len(ns_d) == 2 and _a4_t0pm1 and bad_T == 0
          and _a4_wpath)
add(MAIN, "A4", "Dirac 系统：16 x 16bar 不变量空间复维 1，T0 全 ±1 且直接验证 0/45",
    "行 1280；nullspace 实维 2（= 复 1）—— conj(rhoM) 的权 == −(MINUS 权) == PLUS 权（矩阵对角共轭直读）"
    "⇒ Dirac 方程即 Hom(16,16) 的方程 ⇒ A3 的标量；T0 实支直接验证违例 0/45",
    "行 %d；nullspace 实维 %d；T0 全 ±1 = %s；rhoP·T + T·(rhoM)^T 违例 %d/45；"
    "conj(rhoM) 权 == PLUS 权 = %s"
    % (len(rows_d), len(ns_d), _a4_t0pm1, bad_T, _a4_wpath),
    "PASS" if _a4_ok else "FAIL",
    "★★ 全复数系统：未知 t_l = a_l + i·b_l（32 实未知量），每复方程拆实虚两行。"
    "★ r402 设计期的自伤记录：第一版只建了矩阵实部（虚部 Cartan 对角被丢），维数侥幸 —— "
    "本卷以全复数版为准。★ T0 = " + _ftv(T0) + "；与 nullspace 另一支（纯虚支）张成解空间。")

# ============================================================ A5 反 Hermitian 桥
_a5_ok = (eps == [1] * 10 and eps_pairs == 45 and ahP == 45 and ahM == 45)
add(MAIN, "A5", "反 Hermitian 桥：rho^T == −conj(rho)，两块各 45/45（epsilon 账独立路）",
    "epsilon 表全 +1（10 个 Gamma 逐个验证 G^T == conj(G)）⇒ eps_a·eps_b == +1 恰 45/45"
    "⇒ sigma_ab^T == −eps_a·eps_b·conj(sigma_ab) == −conj(sigma_ab)（结构预期 45+45）",
    "epsilon 表 %s；eps_a*eps_b==+1 对 %d/45；PLUS 反 Hermitian %d/45；MINUS %d/45"
    % (_ftv(eps), eps_pairs, ahP, ahM),
    "PASS" if _a5_ok else "FAIL",
    "★ 独立路从 Gamma 层组合：sigma = [Ga,Gb]/4 的转置由 Ga^T = eps_a·conj(Ga) 逐对拼出，"
    "不逐个复述 Sigma 的对称性。这条桥把 A4 的 Dirac 条件转置成 A6 的 B 共轭关系。")

# ============================================================ A6 B 主判定
_a6_ok = (bad_B == 0 and BBt_ok and Brank == 32)
add(MAIN, "A6", "B = T0^T 主判定：rhoM·B == B·conj(rhoP) 违例 0/45；B 正交；实化秩 32",
    "0/45 —— A4 的 0/45 取转置（T^T·rhoP^T + rhoM·T^T = 0）再用 A5 的 rhoP^T == −conj(rhoP)；"
    "B·B^T == I 与秩 32（16 复 = 32 实满秩）",
    "rhoM·B == B·conj(rhoP) 违例 %d/45；B·B^T == I = %s；实化秩 %d"
    % (bad_B, BBt_ok, Brank),
    "PASS" if _a6_ok else "FAIL",
    "★★★ 这就是 16bar == B·conj(16)·B^{-1} 的显式矩阵实现（B 可逆由正交性给出，B^{-1} = B^T = T0 矩阵）。"
    "r401 边界第 2 条（不构造矩阵层共轭算子）在本卷闭合。")

# ============================================================ A7 B 的权层结构与 t_j 闭式
_col_ok = all(all((B[0][m][j] == 0 and B[1][m][j] == 0) or m == match[j]
                  for m in range(NC)) for j in range(NC))
_val_ok = all(B[0][match[j]][j] == T0[j] and B[1][match[j]][j] == 0 for j in range(NC))
_mw_ok = all(WM[match[j]] == tuple(-x for x in WP[j]) for j in range(NC))
_tf = [sgn(w[0] * w[2] * w[4]) for w in WP]
_tform_ok = _tf == [int(x) for x in T0]
_a7_ok = (_col_ok and _val_ok and _mw_ok and _tform_ok)
add(MAIN, "A7", "B 的权层结构与 t_j 闭式：列 j 支撑恰在 match[j]、值 = t_j；t_j == sign(w1·w3·w5)",
    "支撑/取值/权配对全闭合；闭式 sign(w1·w3·w5)（来自权）== T0（来自 nullspace）—— 两路独立",
    "列支撑 == match %s；值 == t_j %s；WM[match[j]] == −WP[j] %d/16；"
    "闭式匹配 = %s（t_j = %s）"
    % (_col_ok, _val_ok, sum(1 for j in range(NC)
                             if WM[match[j]] == tuple(-x for x in WP[j])),
       _tform_ok, _ftv(_tf)),
    "PASS" if _a7_ok else "FAIL",
    "★ B 把 w-权向量送到 t_j·(−w)-权向量 —— 矩阵层的共轭在权层就是 r401 的「共轭互换宇称类」。"
    "★ 闭式只含 w1·w3·w5（不含 w2·w4）：为何 Gamma_2、Gamma_6 的符号贡献与权无关，本卷未单独推导（诚实边界第 3 条）。")

# ============================================================ A8 B 恰为 Gamma 奇位积
_a8_ok = (bad_Pstar == 0 and bad_Pstar_pos == 45 and eq_masks == [341]
          and hits_neg == [341, 682] and hits_pos == []
          and dp_check.get(341) and dp_check.get(682))
add(MAIN, "A8", "B 恰为 Gamma 奇位积：P* == Gamma_0·Gamma_2·Gamma_4·Gamma_6·Gamma_8（mask 341）逐元相等",
    "P*·sig + sig^T·P* 违例 0/45（32 维 Dirac 表示自共轭的显式实现）；换块 Gamma 乘积 512 个中"
    "恰 2 个满足该方程（341 与 682，块标量独立）；+号对照 45/45 非零 —— 由 Gamma 权作用表"
    "（每个 Gamma 翻恰一个权位）奇位积翻全部 5 位 ⇒ 支撑 == match（权路），矩阵路为 45 对直验",
    "P*·sig + sig^T·P* 违例 %d/45；+号对照 %d/45；P* == Gamma 乘积的 mask = %s（1024 全扫）；"
    "换块方程命中 = %s；+号命中 = %s；682 块标量 (lam1,lam2) = (%s, %s)"
    % (bad_Pstar, bad_Pstar_pos, eq_masks, hits_neg, hits_pos,
       _fcp(blk_scal[682][0]) if 682 in blk_scal else "NA",
       _fcp(blk_scal[682][1]) if 682 in blk_scal else "NA"),
    "PASS" if _a8_ok else "FAIL",
    "★★★ 本卷主结果：共轭算子不是「必须按权配对另行构造」的外来对象 —— 它就是 Clifford 代数里"
    "奇位 Gamma 积的换块作用（P* 与 mask 341 逐元相等，lam = 1）。682 = 偶位积 Gamma_1·3·5·7·9，"
    "块标量 (−i, +i) 独立 —— 解空间两个复方向的显式代表。★ 设计期自伤记录：第一版搜索方程"
    "把右端的 P 丢了（P·sig == sig^T），0 命中被误读为负结果 —— 方程写错时「没找到」不是「不存在」。")

# ============================================================ A9 二次不变量账
_a9_ok = (len(sup_pp) == 0 and len(sup_mm) == 0 and len(sup_pm_inv) == NC)
add(MAIN, "A9", "二次不变量账：16 x 16 与 16bar x 16bar 支撑均 0；16 x 16bar 支撑 = 16 = match 对",
    "0/0 与 16 —— 宇称账：−(偶) = 奇 ∉ 偶、−(奇) = 偶 ∉ 奇 ⇒ 同类张量积无零权和；"
    "异类的零权和恰由 match 双射给出（A1）",
    "16x16 支撑 %d；16barx16bar 支撑 %d；16x16bar 支撑 %d（== match 对 %s）；"
    "其解空间复维 = %d（A4 同一对象，同源不另计）"
    % (len(sup_pp), len(sup_mm), len(sup_pm_inv), len(sup_pm_inv) == NC, len(ns_d) // 2),
    "PASS" if _a9_ok else "FAIL",
    "★ 物理读法：V 上无非退化不变双线性（Hom(16,16bar) = 0 的张量读法）⇒ 单个 16 无 Majorana "
    "二次项（nu^c·nu^c 型需 126bar 三线性）；16 x 16bar 的不变量复维 1 = Dirac 质量项唯一。"
    "★ 与 A4 是同一个线性系统的两种读法 —— 已在 act 中显式标注同源，不得当作两次独立确认。")

# ============================================================ 控制组
rows_k1 = []
for kk in KEYS:
    (Rp, Ip) = SIGC[kk]
    (Rm, Im) = SIGC[kk]
    for j in range(NC):
        for k in range(NC):
            lstar = [l for l in range(NC) if match[l] == k]
            cre = [F(0)] * (2 * NC)
            cim = [F(0)] * (2 * NC)
            if lstar:
                l = lstar[0]
                cre[l] += Rp[j][l]
                cim[l] += Ip[j][l]
                cre[NC + l] += -Ip[j][l]
                cim[NC + l] += Rp[j][l]
            cre[j] += Rm[k][match[j]]
            cim[j] += Im[k][match[j]]
            cre[NC + j] += -Im[k][match[j]]
            cim[NC + j] += Rm[k][match[j]]
            if any(x != 0 for x in cre):
                rows_k1.append(cre)
            if any(x != 0 for x in cim):
                rows_k1.append(cim)
rows_k1 = [r for r in rows_k1 if any(x != 0 for x in r)]
ns_k1 = nullspace_basis(rows_k1, 2 * NC)
_k1 = (len(rows_k1), len(ns_k1))
add(CTL, "K1",
    "控制组（污染表示）：同式 Dirac 系统但两块都用 rhoP",
    "解空间实维 0 —— 换错表示 ⇒ 解坍缩（若仍 2 则 A4 的维数是系统形状的产物而非表示的产物）；"
    "行数是污染支撑稀疏性的副产品，如实报、不作预期",
    "(行 %d, 解空间实维 %d)（对照 A4 的 (1280, 2)）" % _k1,
    "PASS" if _k1[1] == 0 else "FAIL",
    "★ A4 的判别力对照：系统逐字符同形，只把第二个表示换掉，解从 2 维坍到 0 维 —— "
    "「复维 1」读的是表示（16 对 16bar），不是方程的形状。污染版行数 %d 与 A4 的 1280 不同，"
    "本身即支撑错位的读数。" % _k1[0])
_k2 = (bad_Bnc, bad_B)
add(CTL, "K2",
    "控制组（去共轭）：rhoM·B == B·rhoP（无 conj）",
    "非零（conj 不可去）；带 conj 侧 0（A6 反抄）—— 两侧读数必须不同",
    "去 conj 违例 %d/45；带 conj 违例 %d/45" % _k2,
    "PASS" if (_k2[0] != 0 and _k2[1] == 0) else "FAIL",
    "★ 有趣的中间读数：45 对中恰 %d 对在去掉 conj 后仍成立（偶然同解），"
    "但只要有一对不成立，conj 就是必要的 —— 负控报「非零」不报「全非零」。" % (45 - _k2[0]))
_k3 = (len(hits_keep), per_pair_pass)
add(CTL, "K3",
    "控制组（块保持同号）：C = P|_PLUS 满足 C·rhoP == ±(rhoP)^T·C（全 45 对同一符号）",
    "(0, 511) —— 同号 0（由 Hom(16,16bar)=0：C·rhoP == conj(rhoP)·C 型方程无非零可逆解）；"
    "逐对各自换号 511（Gamma 乘积在权基下是单项式矩阵，逐对符号总可配）",
    "45 对同号命中 %d/%d；逐对换号通过 %d/%d" % (_k3[0], len(cands_keep), _k3[1], len(cands_keep)),
    "PASS" if _k3 == (0, 511) else "FAIL",
    "★★ 本卷设计期的实感刀：第一版对照允许逐对各自换号，511/511 全过 —— 空转。"
    "「同号」才是缠绕条件；「逐对可配」是单项式结构的平凡副产品。两个读数都要报，"
    "否则会以为对照做过了。")


def _nmin3(w):
    return sum(1 for x in w[:3] if x < 0)


_tfalse = {
    "(-1)^{#minus前3}": [(-1) ** _nmin3(w) for w in WP],
    "(-1)^{#minus全部}": [(-1) ** sum(1 for x in w if x < 0) for w in WP],
    "sign(w4*w5)": [sgn(w[3] * w[4]) for w in WP],
    "sign(w1*w2*w3)": [sgn(w[0] * w[1] * w[2]) for w in WP],
}
_k4 = ([int(x) for x in T0], {nm: (v == [int(x) for x in T0]) for nm, v in _tfalse.items()})
add(CTL, "K4",
    "控制组（闭式负候选）：t_j 的四个错闭式",
    "真闭式 sign(w1*w3*w5) True；四个负候选全 False —— 判别力两侧都有",
    "真闭式匹配 = %s；负候选匹配 = %s" % (_tform_ok, _k4[1]),
    "PASS" if (_tform_ok and not any(_k4[1].values())) else "FAIL",
    "★ 若任何负候选也匹配，A7 的闭式就没有判别力（一个 100% 通过的谓词判别力为 0）。")

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
    "★★★ r394 的老刀：守卫不得读自己的源码字面量，走 AST 只看赋值右端是否常量 True。")

_same = 0
for _r in MAIN:
    if _r["kind"] in ("PASS", "FAIL") and _unbold(_r["exp"]) == _unbold(_r["act"]):
        _same += 1
add(GRD, "G02", "exp 与 act 不得是同一表达式", "0 条",
    "exp == act 的条目 %d 条" % _same, "PASS" if _same == 0 else "FAIL",
    "★「值相等」不算问题，「字面相同」说明 act 没有真的算过。")

_readings = [_k1, _k2, _k3, (1 if _tform_ok else 0, sum(1 for v in _k4[1].values() if v))]
add(GRD, "G03", "四个控制组必须两两给出不同读数", "4 个不同读数",
    "K1 %s；K2 %s；K3 %s；K4 (真闭式 %d, 负候选命中 %d)（%d 个不同）"
    % (_k1, _k2, _k3, _readings[3][0], _readings[3][1], len(set(_readings))),
    "PASS" if len(set(_readings)) == 4 else "FAIL",
    "★ K1/K3 都是「坍缩型」负控，靠第二个分量分开；K2/K4 靠结构分开。")

add(GRD, "G04", "每条都有非空 note 且 computed", "0 违规",
    "%d 违规（覆盖 %d 条）" % (sum(1 for r in ALL if not r["note"] or not r["computed"]), len(ALL)),
    "PASS" if all(r["note"] and r["computed"] for r in ALL) else "FAIL",
    "★ 收尾整表重扫。")

_g5 = (len(KEYS) == 45 and len(HC) == 5 and len(HC_M) == 5
       and len(WP) == 16 and len(WM) == 16
       and all(abs(x) == F(1, 2) for w in WP for x in w)
       and all(abs(x) == F(1, 2) for w in WM for x in w)
       and len(PLUS) == 16 and len(MINUS) == 16 and len(set(PLUS) | set(MINUS)) == 32
       and match_bijective and all(dp_check.values()))
add(GRD, "G05", "维数账：45 个 Sigma、5+5 Cartan、两类各 16 权全 ±1/2、match 双射、Gamma 乘积表 DP 抽查",
    "45 / 5+5 / 16+16 / 双射 / DP 抽查 4 个全对",
    "Sigma %d；Cartan %d+%d；权 %d+%d 全 ±1/2 = %s；match 双射 %s；DP 抽查 %s"
    % (len(KEYS), len(HC), len(HC_M), len(WP), len(WM),
       all(abs(x) == F(1, 2) for w in WP for x in w)
       and all(abs(x) == F(1, 2) for w in WM for x in w),
       match_bijective, dp_check),
    "PASS" if _g5 else "FAIL",
    "★ DP 抽查：mask 341 / 682 / 7 / 0 与直接升序乘积逐元相等 —— 乘积表不是凭记忆拼的。")

_wd_ok = all(
    len(wdiff[a]) == 2 and wdiff[a][0] == tuple(-x for x in wdiff[a][1])
    and [t for t in range(5) if wdiff[a][0][t] != 0] == [a // 2]
    and abs(wdiff[a][0][a // 2]) == 1 and wnz[a] == 16
    for a in range(10))
_g6 = (len(cands_swap) == 512 and len(cands_keep) == 511
       and len(cands_swap) + len(cands_keep) + 1 == 1024 and _wd_ok)
add(GRD, "G06", "分类账：1024 个 mask = 换块 512 + 块保持 511 + 空 1；每个 Gamma 权差恰 ±e_{a//2} 且 16 非零元",
    "512 + 511 + 1 = 1024；权差表全对",
    "换块 %d；块保持 %d；空 1；和 = %d；权差表全对 = %s"
    % (len(cands_swap), len(cands_keep),
       len(cands_swap) + len(cands_keep) + 1, _wd_ok),
    "PASS" if _g6 else "FAIL",
    "★ 少一个 mask 就说明 DP 表有洞；权差表错一位，A8 的 Gamma 奇位积解释就失去地基。")

_g7 = (all(HC_M[i][0][k][k] == 0 for i in range(5) for k in range(NC))
       and all(HC[i][0][k][k] == 0 for i in range(5) for k in range(NC))
       and all(HC_M[i][1][k][k] == WM[k][i] for i in range(5) for k in range(NC))
       and all(HC[i][1][k][k] == WP[k][i] for i in range(5) for k in range(NC)))
add(GRD, "G07", "权读法守卫：两块 Cartan 实部对角全 0、虚部对角 == 权（r399 老守卫，两块各跑）",
    "两块全闭合",
    "MINUS 实部全零 = %s；虚部 == 权 = %s（PLUS 同口径由 setup 断言 + 本卷复验）"
    % (all(HC_M[i][0][k][k] == 0 for i in range(5) for k in range(NC)),
       all(HC_M[i][1][k][k] == WM[k][i] for i in range(5) for k in range(NC))),
    "PASS" if _g7 else "FAIL",
    "★ 「权」这个读法本身要守卫：对角元若混入实部，后续所有支撑账都会静默错位。")

VERDICT = "--".join([
    "HOM-BOTH-DIRECTIONS-ZERO" if _a2_ok else "HOM-NONZERO",
    "COMMUTANT-SCALAR-IRREDUCIBLE" if _a3_ok else "COMMUTANT-NONSCALAR",
    "DIRAC-INVARIANT-COMPLEX-DIM-1" if _a4_ok else "DIRAC-DIM-WRONG",
    "ANTIHERMITIAN-BRIDGE-90-OF-90" if _a5_ok else "ANTIHERMITIAN-BROKEN",
    "B-CONJUGATION-EXACT-45-OF-45" if _a6_ok else "B-CONJUGATION-FAILS",
    "TJ-CLOSED-FORM-SIGN-W1W3W5" if _a7_ok else "TJ-NO-CLOSED-FORM",
    "B-IS-GAMMA-ODD-PRODUCT-MASK341" if _a8_ok else "B-NOT-GAMMA-PRODUCT",
    "NO-MAJORANA-QUADRATIC-DIRAC-UNIQUE" if _a9_ok else "QUADRATIC-ACCOUNT-BROKEN",
])
add(GRD, "G08", "判词与判定表必须同一读数（两路径拼接）", "两路一致",
    "由变量拼：%s" % VERDICT,
    "PASS" if (_a1_ok and _a2_ok and _a3_ok and _a4_ok and _a5_ok
               and _a6_ok and _a7_ok and _a8_ok and _a9_ok) else "FAIL",
    "★ 判词每一段由一个布尔量决定，不写字面量。")

g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "（回填）", "（回填）", "INFO",
          "★ 先占位再回填（r396 E06：报告必须在回填之后才拼）")

DECLARED_NEG = set()
_neg_fail = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G10", "真判负必须逐条登记", "登记集 == 实际 FAIL 集",
    "%s vs %s" % (sorted(DECLARED_NEG), _neg_fail),
    "PASS" if sorted(DECLARED_NEG) == _neg_fail else "FAIL",
    "★ 本卷若无判负，登记集为空。")

_g11 = (bad_B == 0 and BBt_ok and Brank == 32 and len(ns_d) == 2
        and len(sup_pm) == 0 and len(sup_mp) == 0 and len(ns_c) == 2 and comps == 1
        and len(sup_pp) == 0 and len(sup_mm) == 0 and len(sup_pm_inv) == 16
        and eq_masks == [341] and hits_neg == [341, 682] and hits_pos == []
        and bad_Pstar == 0 and bad_Pstar_pos == 45 and _tform_ok)
add(GRD, "G11", "主关系机核：Hom 双向 0 + 交换子标量 + Dirac 复维 1 + B 共轭 0/45 + B == Gamma 奇位积 + 二次账",
    "全部主读数同真",
    "B 关系 %d；正交 %s；秩 %d；ns_d %d；sup %d/%d；ns_c %d；comps %d；"
    "二次 %d/%d/%d；mask %s；命中 %s/%s；P* %d/%d"
    % (bad_B, BBt_ok, Brank, len(ns_d), len(sup_pm), len(sup_mp), len(ns_c), comps,
       len(sup_pp), len(sup_mm), len(sup_pm_inv), eq_masks, hits_neg, hits_pos,
       bad_Pstar, bad_Pstar_pos),
    "PASS" if _g11 else "FAIL",
    "★★★ 本卷总纲机核：把九条主判据的核心读数拼成一个布尔 —— 任何一条塌了总门就红。")

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

# ============================================================ 右路：现场重算（不引用任何左路缓存）
_r_sig32 = {}
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    _r_sig32[(a, b)] = ([[x / 4 for x in row] for row in _Cm[0]],
                        [[x / 4 for x in row] for row in _Cm[1]])
_r_sigp = {kk: restrict(_r_sig32[kk], PLUS) for kk in KEYS}
_r_sigm = {kk: restrict(_r_sig32[kk], MINUS) for kk in KEYS}
_r_wp = [tuple(_r_sigp[(2 * i, 2 * i + 1)][1][k][k] for i in range(5)) for k in range(NC)]
_r_wm = [tuple(_r_sigm[(2 * i, 2 * i + 1)][1][k][k] for i in range(5)) for k in range(NC)]
# match 右路：从 MINUS 侧反着建（左路从 PLUS 侧建）
_r_match = {}
for k in range(NC):
    hit = [j for j in range(NC) if _r_wp[j] == tuple(-x for x in _r_wm[k])]
    _r_match[k] = hit[0] if len(hit) == 1 else -1
_r_minv = {j: k for k, j in _r_match.items()}

# Dirac 右路：T0 用闭式当 ansatz（不解 nullspace），再代入验证全部方程
_r_t0 = [sgn(w[0] * w[2] * w[4]) for w in _r_wp]
_r_rows = []
for kk in KEYS:
    (Rp, Ip) = _r_sigp[kk]
    (Rm, Im) = _r_sigm[kk]
    for j in range(NC):
        for k in range(NC):
            lstar = [l for l in range(NC) if _r_minv[l] == k]
            cre = [F(0)] * (2 * NC)
            cim = [F(0)] * (2 * NC)
            if lstar:
                l = lstar[0]
                cre[l] += Rp[j][l]
                cim[l] += Ip[j][l]
                cre[NC + l] += -Ip[j][l]
                cim[NC + l] += Rp[j][l]
            cre[j] += Rm[k][_r_minv[j]]
            cim[j] += Im[k][_r_minv[j]]
            cre[NC + j] += -Im[k][_r_minv[j]]
            cim[NC + j] += Rm[k][_r_minv[j]]
            if any(x != 0 for x in cre):
                _r_rows.append(cre)
            if any(x != 0 for x in cim):
                _r_rows.append(cim)
_r_rows = [r for r in _r_rows if any(x != 0 for x in r)]
_r_sub_bad = sum(1 for row in _r_rows
                 if sum(row[l] * _r_t0[l] for l in range(NC)) != 0)
_r_dim_d = 2 * NC - rank_of([r[:] for r in _r_rows], 2 * NC)

_r_TM = ([[F(0)] * NC for _ in range(NC)], [[F(0)] * NC for _ in range(NC)])
for j in range(NC):
    _r_TM[0][j][_r_minv[j]] = _r_t0[j]
_r_B = cT(_r_TM)
_r_badB = 0
for kk in KEYS:
    if not czero(cadd(cmul(_r_sigm[kk], _r_B), cmul(_r_B, cbar(_r_sigp[kk])), -1)):
        _r_badB += 1
_r_BBt = czero(cadd(cmul(_r_B, cT(_r_B)), ceye(NC), -1))
_r_Brank = rank_of([r[:] for r in realify(_r_B)], 32)

# 交换子右路：秩 + 全 1 向量代入（不建 nullspace 基）
_r_rowsc = []
for kk in KEYS:
    (Rr, Ii) = _r_sigp[kk]
    for i in range(NC):
        for j in range(i + 1, NC):
            if Rr[i][j] != 0 or Ii[i][j] != 0 or Rr[j][i] != 0 or Ii[j][i] != 0:
                r1 = [F(0)] * (2 * NC)
                r1[i] = F(1)
                r1[j] = F(-1)
                r2 = [F(0)] * (2 * NC)
                r2[NC + i] = F(1)
                r2[NC + j] = F(-1)
                _r_rowsc.append(r1)
                _r_rowsc.append(r2)
_r_rowsc = [list(r) for r in {tuple(r) for r in _r_rowsc}]
_r_dim_c = 2 * NC - rank_of([r[:] for r in _r_rowsc], 2 * NC)
_r_one_bad = sum(1 for row in _r_rowsc if sum(row) != 0)

_r_sup_pm = sum(1 for j in range(NC) for k in range(NC) if _r_wp[j] == _r_wm[k])
_r_sup_mp = sum(1 for j in range(NC) for k in range(NC) if _r_wm[j] == _r_wp[k])
_r_sup_pp = sum(1 for j in range(NC) for k in range(NC)
                if tuple(-x for x in _r_wp[j]) == _r_wp[k])
_r_sup_mm = sum(1 for j in range(NC) for k in range(NC)
                if tuple(-x for x in _r_wm[j]) == _r_wm[k])
_r_sup_inv = sum(1 for j in range(NC) for k in range(NC)
                 if _r_wm[k] == tuple(-x for x in _r_wp[j]))

# Gamma 乘积表与搜索右路（全量重建）
_r_P = [None] * 1024
_r_P[0] = ceye(32)
for mask in range(1, 1024):
    hb = mask.bit_length() - 1
    _r_P[mask] = cmul(_r_P[mask ^ (1 << hb)], GAM[hb])
_r_cTS = {kk: cT(_r_sig32[kk]) for kk in KEYS}


def _r_bswap(Pm):
    (R, I) = Pm
    return all(R[m][j] == 0 and I[m][j] == 0
               for j in PLUS for m in PLUS) and \
           all(R[m][j] == 0 and I[m][j] == 0
               for j in MINUS for m in MINUS)


_r_swap = [m for m in range(1024) if m and _r_bswap(_r_P[m])]
_r_hits = []
for m in _r_swap:
    ok = all(czero(cadd(cmul(_r_P[m], _r_sig32[kk]), cmul(_r_cTS[kk], _r_P[m])))
             for kk in KEYS)
    if ok:
        _r_hits.append(m)
_r_hits_pos = []
for m in _r_swap:
    ok = all(czero(cadd(cmul(_r_P[m], _r_sig32[kk]),
                        cmulS(cmul(_r_cTS[kk], _r_P[m]), -1))) for kk in KEYS)
    if ok:
        _r_hits_pos.append(m)
_r_Pstar = embed_offdiag(_r_TM, _r_B)
_r_badP = 0
for kk in KEYS:
    if not czero(cadd(cmul(_r_Pstar, _r_sig32[kk]), cmul(_r_cTS[kk], _r_Pstar))):
        _r_badP += 1
_r_badPpos = 0
for kk in KEYS:
    if not czero(cadd(cmul(_r_Pstar, _r_sig32[kk]),
                      cmulS(cmul(_r_cTS[kk], _r_Pstar), -1))):
        _r_badPpos += 1
_r_eq = [m for m in range(1024) if czero(cadd(_r_P[m], _r_Pstar, -1))]
_r_l1 = scalar_ratio(blocks_of(_r_P[682])[0], _r_TM)
_r_l2 = scalar_ratio(blocks_of(_r_P[682])[1], _r_B)

_g12 = (all(_r_match[match[j]] == j for j in range(NC))
        and _r_t0 == [int(x) for x in T0]
        and _r_sub_bad == 0 and _r_dim_d == len(ns_d)
        and _r_badB == bad_B and _r_BBt == BBt_ok and _r_Brank == Brank
        and _r_dim_c == len(ns_c) and _r_one_bad == 0
        and _r_sup_pm == len(sup_pm) and _r_sup_mp == len(sup_mp)
        and _r_sup_pp == len(sup_pp) and _r_sup_mm == len(sup_mm)
        and _r_sup_inv == len(sup_pm_inv)
        and _r_hits == hits_neg and _r_hits_pos == hits_pos
        and _r_badP == bad_Pstar and _r_badPpos == bad_Pstar_pos
        and _r_eq == eq_masks
        and rank_of([r[:] for r in rows_d], 2 * NC) + len(ns_d) == 2 * NC)
add(GRD, "G12", "两路拼关键量：match 两向 / T0 两路（nullspace vs 闭式代入）/"
    "维数两路（nullspace vs 秩+零化度）/ B 关系与 Gamma 实现全量重算", "两路全一致",
    "match 反建 %s；T0 闭式代入违例 %d（维 %d vs %d）；B %d/%d；正交 %s/%s；秩 %d/%d；"
    "交换子 %d/%d（全 1 代入 %d）；支撑 %d/%d/%d/%d/%d；命中 %s/%s；P* %d/%d；相等 %s"
    % (all(_r_match[match[j]] == j for j in range(NC)), _r_sub_bad, _r_dim_d, len(ns_d),
       _r_badB, bad_B, _r_BBt, BBt_ok, _r_Brank, Brank,
       _r_dim_c, len(ns_c), _r_one_bad,
       _r_sup_pm, _r_sup_mp, _r_sup_pp, _r_sup_mm, _r_sup_inv,
       _r_hits, _r_hits_pos, _r_badP, _r_badPpos, _r_eq),
    "PASS" if _g12 else "FAIL",
    "★★ 右路的三个真不同路：match 从 MINUS 侧反建；T0 不解方程、拿闭式当 ansatz 代入全部 %d 行；"
    "维数用秩+零化度而不是 nullspace 基。左路任何一处缓存污染都会在这里现形。" % len(_r_rows))

# ============================================================ G14 关键表两路机拼
_FORM1 = "三重判定：Hom 支撑 %d+%d；交换子实维 %d；Dirac 行 %d / 实维 %d"
_FORM2 = "B：违例 %d/45；B·B^T == I = %s；秩 %d；t_j 闭式匹配 %s"
_FORM3 = "Gamma 实现：P* 违例 %d/45；+号 %d/45；相等 mask %s；换块命中 %s；682 标量 (%s, %s)"
_FORM4 = "二次账：16x16 %d；16barx16bar %d；16x16bar %d（复维 %d）"

_KT1 = _FORM1 % (len(sup_pm), len(sup_mp), len(ns_c), len(rows_d), len(ns_d))
_KT2 = _FORM2 % (bad_B, BBt_ok, Brank, _tform_ok)
_KT3 = _FORM3 % (bad_Pstar, bad_Pstar_pos, eq_masks, hits_neg,
                 _fcp(blk_scal[682][0]) if 682 in blk_scal else "NA",
                 _fcp(blk_scal[682][1]) if 682 in blk_scal else "NA")
_KT4 = _FORM4 % (len(sup_pp), len(sup_mm), len(sup_pm_inv), len(ns_d) // 2)
_r_KT1 = _FORM1 % (_r_sup_pm, _r_sup_mp, _r_dim_c, len(_r_rows), _r_dim_d)
_r_KT2 = _FORM2 % (_r_badB, _r_BBt, _r_Brank, _r_t0 == [int(x) for x in T0])
_r_KT3 = _FORM3 % (_r_badP, _r_badPpos, _r_eq, _r_hits, _fcp(_r_l1), _fcp(_r_l2))
_r_KT4 = _FORM4 % (_r_sup_pp, _r_sup_mm, _r_sup_inv, _r_dim_d // 2)

_kt_all = " || ".join([_KT1, _KT2, _KT3, _KT4])
_kt_re = " || ".join([_r_KT1, _r_KT2, _r_KT3, _r_KT4])
add(GRD, "G14", "关键表每一句都必须由变量拼出，且两条独立路径（缓存变量 / 现场重算）字面相等",
    "两路字面相等",
    "左路：%s || 右路：%s || 相等 = %s" % (_kt_all, _kt_re, _kt_all == _kt_re),
    "PASS" if (_kt_all == _kt_re and _a4_ok and _a6_ok and _a7_ok and _a8_ok) else "FAIL",
    "★★ r396 E02 / r397 E09 / r398 E06 / r399 E07 / r401 G14 的第七次继承：关键表每一句由变量拼。"
    "★ 右路 T0 来自闭式 ansatz、维数来自秩 —— 与左路在算法上真不同。")

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

# ============================================================ 落盘（JSON -> 回填 G09 -> 再写 -> 最后拼报告）
RPT = os.path.join(DATA, TITLE + "_report_2026-11-05.txt")
JSN = os.path.join(DATA, TITLE + ".json")
payload = dict(rid=RID, date="2026-11-05", title=TITLE, final=FINAL, verdict=VERDICT,
               counts=dict(main=len(MAIN), pass_=sum(1 for r in MAIN if r["kind"] == "PASS"),
                           info=sum(1 for r in MAIN if r["kind"] == "INFO"),
                           identity=sum(1 for r in MAIN if r["kind"] == "IDENTITY"),
                           fail=_nf_main, ctl=len(CTL), grd=len(GRD), total=len(ALL)),
               rows=ALL, declared_neg=sorted(DECLARED_NEG),
               key_tables=[_KT1, _KT2, _KT3, _KT4],
               readings=dict(sup_pm=len(sup_pm), sup_mp=len(sup_mp), ns_c=len(ns_c),
                             comps=comps, rows_d=len(rows_d), ns_d=len(ns_d),
                             t0=[str(x) for x in T0], bad_T=bad_T, ahP=ahP, ahM=ahM,
                             bad_B=bad_B, bad_Bnc=bad_Bnc, BBt_ok=str(BBt_ok),
                             Brank=Brank, tform=str(_tform_ok),
                             tf=[str(x) for x in _tf],
                             bad_Pstar=bad_Pstar, bad_Pstar_pos=bad_Pstar_pos,
                             eq_masks=eq_masks, hits_neg=hits_neg, hits_pos=hits_pos,
                             lam682=([_fcp(blk_scal[682][0]), _fcp(blk_scal[682][1])]
                                     if 682 in blk_scal else []),
                             sup_pp=len(sup_pp), sup_mm=len(sup_mm),
                             sup_pm_inv=len(sup_pm_inv), ns_k1=len(ns_k1),
                             hits_keep=len(hits_keep), per_pair=per_pair_pass,
                             wdiff=[[str(t) for t in wdiff[a]] for a in range(10)],
                             match=[match[j] for j in range(NC)],
                             wp=[[str(x) for x in w] for w in WP],
                             wm=[[str(x) for x in w] for w in WM]))
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))
_back = json.load(io.open(JSN, encoding="utf-8"))
g09["exp"] = "回读条目数 == 内存条目数（%d）" % len(ALL)
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                       "一致" if len(_back["rows"]) == len(ALL) else "不一致")
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
A("对象：X-GSM-7（矩阵层共轭：16bar == B·conj(16)·B^{-1} 的显式实现，B 恰为 Gamma 奇位积）")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
     sum(1 for r in MAIN if r["kind"] == "INFO"),
     sum(1 for r in MAIN if r["kind"] == "IDENTITY"),
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
A("读数：Hom %d+%d；交换子实维 %d（分量 %d）；Dirac %d 行实维 %d；反 Hermitian %d+%d；"
  "B 违例 %d、正交 %s、秩 %d；t_j 闭式 %s；P* %d/45（+号 %d/45）；相等 mask %s；"
  "换块命中 %s；二次账 %d/%d/%d"
  % (len(sup_pm), len(sup_mp), len(ns_c), comps, len(rows_d), len(ns_d), ahP, ahM,
     bad_B, BBt_ok, Brank, _tform_ok, bad_Pstar, bad_Pstar_pos, eq_masks, hits_neg,
     len(sup_pp), len(sup_mm), len(sup_pm_inv)))
A("")
A("【诚实边界】")
A(" 1) 本卷读数绑定 r397 起的同一 Gamma 口径（C1/C2/C3 张量积序与相位约定）：mask %s 与 t_j 闭式的"
  "**形状**依赖该构造；Hom 双向 0、交换子标量、Dirac 复维 1、无 Majorana 二次是表示层不变量"
  "（换基不变）。换 Gamma 相位后逐元相等会变成别的标量倍（本卷口径下 lam = %s）；"
  % (eq_masks, _fcp(blk_scal[341][1]) if 341 in blk_scal else "1"))
A(" 2) t_j = sign(w1·w3·w5) 为何不含 w2、w4：Gamma_2、Gamma_6（第二因子）的符号贡献"
  "与权无关这一步**未单独推导** —— 闭式以三重读数记录（nullspace 匹配 / mask %s 逐元相等 / "
  "右路闭式 ansatz 代入全部 %d 行零违例）；"
  % (eq_masks, len(_r_rows)))
A(" 3) 32 维自共轭（P*·sig + sig^T·P* = 0 违例 %d/45）与 16 ≠ 16bar **不矛盾**：P* 联系的是两个"
  "**块之间**（16 ⊕ 16bar 整体自共轭），块内的 Hom 双向 0 才是不等价；r401 的「一比特」在矩阵层"
  "即：B 的作用方向（PLUS -> MINUS）取哪一边；" % bad_Pstar)
A(" 4) 同源账：A9 的 16x16bar 解空间与 A4 是**同一个线性系统**（act 内已标注，不得当两次独立确认）；"
  "K1 的 (%d, %d) 是污染支撑控制（第二个表示换错），不是 16⊗16 系统的维数（后者支撑 = %d）；"
  % (_k1[0], _k1[1], len(sup_pp)))
A(" 5) 物理读法边界：Dirac 项唯一 / 无 Majorana 二次项是**表示论读法**；质量数值、Yukawa、混合角、"
  "126bar 三线性不在本卷 —— 「二次项被禁」不等于「质量谱被定下」；")
A(" 6) 独有预言 0、不占度（度数链维持 36，r264 止）：本卷是 r401 权层结论（两类不等价、SM 住偶类）"
  "的矩阵层实现与判据，审计册不产新物理。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("JSON ->", JSN)
print("RPT  ->", RPT)
print("FINAL =", FINAL)
