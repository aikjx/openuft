# -*- coding: utf-8 -*-
"""TUFT-r401  攻 X-GSM-6：编号层与宇称类 —— 16 与 16bar 的一比特分离

纯标准库（Fraction，判据区无浮点、无随机）。复用 r399/r400 的代数底座（同一 Γ / Σ / 生成元 / realify）。

r400 留下的硬边界（其 `_report` 的【诚实边界】第 3 条与 A10）：
  「SM 电荷表对 q -> -q 免疫 ⇒ 任何只用电荷谱的判据都无法区分 16 与 16bar」
本卷问：把这层边界拆开 —— 分不开的结构原因是什么？分开的最小充分输入是什么？

  A1  两个宇称类：32 个旋量权 = 偶类（手征 +1 块，#(−1/2)∈{0,2,4}，重数 = C(5,k)）
      ∪ 奇类（手征 −1 块，{1,3,5}）；不相交、并 = 全部 32 个 (±1/2)^5；
      奇类权集 == −偶类权集（共轭互换两类）；两类最高权不同 ⇒ 作为 so(10) 表示不等价
  A2  折叠机制：对线性 χ，multiset(χ|奇类) = −multiset(χ|偶类)；Q 在两类都折出 SM 表（免疫的机制）
  A3  主判定：Q 表自共轭 ⇒ 分不开；y 表非自共轭 ⇒ 分得开（偶类 == SM 超荷表，奇类 == 其取反）
      ⇒ SM 一代住在偶类
  A4  一比特·表述一：e 态 (T3L,y)=(−1/2,−1/2) 在偶类恰 1 态、在奇类 0 态 ⇒ 两个数已定类
  A5  一比特·表述二：y=0 单态的 B-L 在偶类 = +1（ν^c）、在奇类 = −1（ν）
      —— 「哪个 y=0 单态叫 ν^c」就是那层编号
  A6  一比特·表述三：双扇区（K3=0）Q 多重集两类互为取反且非自共轭 ⇒ 扇区分辨的电荷表已含该比特
  A7  下界：|y| 幅值表两类全同 ⇒ 0 比特不够；全网格 4 解恰按 λ_A 符号分成「SM 表 / −SM 表」两支
      （λ_K 那支不改 y 表）⇒ 歧义恰为 Z2，一比特是下界也是上界
  A8  r400 张力显式化：SM 扇区表 ⇒ λ_A = −1/3；共轭扇区表 ⇒ +1/3；
      SM 扇区表本身非自共轭 ⇒ r400 A5 的「唯一」是在「给定 SM 扇区指认」下的唯一
  A9  对称稳定性：eps4<->eps5（r400 A8 的编号约定）不换类、不翻比特；共轭翻一切 ⇒ 判别力双向验证
  A10 共轭完成自洽：在奇类上用 −Y 折叠 ⇒ y 表 == SM 超荷表、Q 表 == SM 电荷表
      —— 「奇类 + 共轭嵌入」与「偶类 + SM 嵌入」在电荷/幅值层不可区分（边界的另一半）
"""
import ast
import io
import json
import math
import os
from fractions import Fraction as F

RID = "r401"
TITLE = ("TUFT-r401_攻X-GSM-6_编号层与宇称类_16与16bar的一比特分离_"
         "电荷表分不开的结构原因_最小充分输入是一个态的超荷符号_"
         "共轭互换宇称类_y0单态是折叠不动点_r400扇区输入已选支_精算_2026-11-05")
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




# ============================================================ 奇类（MINUS 块）的权：从 Σ 的虚部对角读
SIGC_M = {}
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    _Cm = ([[x / 4 for x in row] for row in _Cm[0]], [[x / 4 for x in row] for row in _Cm[1]])
    SIGC_M[(a, b)] = restrict(_Cm, MINUS)
HC_M = [SIGC_M[(2 * i, 2 * i + 1)] for i in range(5)]
WM = [[HC_M[i][1][k][k] for i in range(5)] for k in range(NC)]
assert all(HC_M[i][0][k][k] == 0 for i in range(5) for k in range(NC)), "奇类 Cartan 实部非零"


def _nm(w):
    return sum(1 for x in w if x < 0)


def _ftp(w):
    return "(" + ",".join(str(x) for x in w) + ")"


WPt = [tuple(w) for w in W]
WMt = [tuple(w) for w in WM]

# ============================================================ 折叠与两张 SM 表
_COEF_A = F(-1, 3)
_COEF_K = F(1, 2)


def _fold(ws):
    A = [w[0] + w[1] + w[2] for w in ws]
    TL = [(w[3] + w[4]) / 2 for w in ws]
    K3 = [w[3] - w[4] for w in ws]
    Q = [TL[i] + _COEF_A * A[i] + _COEF_K * K3[i] for i in range(len(ws))]
    y = [_COEF_A * A[i] + _COEF_K * K3[i] for i in range(len(ws))]
    BL = [F(-2, 3) * A[i] for i in range(len(ws))]
    return A, TL, K3, Q, y, BL


A_P, TL_P, K_P, Q_P, y_P, BL_P = _fold(WPt)
A_M, TL_M, K_M, Q_M, y_M, BL_M = _fold(WMt)
SM_Q = {F(2, 3): 3, F(-1, 3): 3, F(-2, 3): 3, F(1, 3): 3, F(0): 2, F(-1): 1, F(1): 1}
SM_Y = {F(1, 6): 6, F(-2, 3): 3, F(1, 3): 3, F(-1, 2): 2, F(1): 1, F(0): 1}
NSM_Y = {-k: v for k, v in SM_Y.items()}
NSM_Q = {-k: v for k, v in SM_Q.items()}
_Q_PN = cnt([-q for q in Q_P])
_y_PN = cnt([-q for q in y_P])
_GRID = [F(k, 12) for k in range(-24, 25)]

# ============================================================ A1 两个宇称类
_PAR_P = cnt([_nm(w) for w in WPt])
_PAR_M = cnt([_nm(w) for w in WMt])
_EXP_PP = {k: math.comb(5, k) for k in (0, 2, 4)}
_EXP_PM = {k: math.comb(5, k) for k in (1, 3, 5)}
_ALLC = set(tuple(F(1, 2) if (i >> k) & 1 == 0 else F(-1, 2) for k in range(5))
            for i in range(32))
_NEGP = {tuple(-x for x in w) for w in WPt}
_HW_P, _HW_M = max(WPt), max(WMt)
_a1_ok = (_PAR_P == _EXP_PP and _PAR_M == _EXP_PM
          and not (set(WPt) & set(WMt)) and set(WPt) | set(WMt) == _ALLC
          and set(WMt) == _NEGP and _HW_P != _HW_M
          and len(set(WPt)) == NC and len(set(WMt)) == NC)
add(MAIN, "A1",
    "32 个旋量权分成两个宇称类：偶类（手征 +1 块）#(−1/2) 取值集 {0,2,4}、重数等于二项式 C(5,k)；"
    "奇类（手征 −1 块）{1,3,5}；两类不相交、并 = 全部 32 个 (±1/2)^5；"
    "奇类权集 == −偶类权集（共轭互换两类）；两类最高权不同 ⇒ 作为 so(10) 表示不等价",
    "偶类重数 {0:1, 2:10, 4:5}、奇类 {1:5, 3:10, 5:1}；并集 == 32 组合；奇类 == −偶类；"
    "偶类最高权 (1/2,1/2,1/2,1/2,1/2) != 奇类最高权 (1/2,1/2,1/2,1/2,-1/2)",
    "偶类重数 %s；奇类重数 %s；不相交 = %s；并集 = %d/32（全组合 = %s）；奇类==−偶类 = %s；"
    "最高权 %s vs %s（不同 = %s）"
    % (ctr_txt(_PAR_P), ctr_txt(_PAR_M), not (set(WPt) & set(WMt)),
       len(set(WPt) | set(WMt)), set(WPt) | set(WMt) == _ALLC, set(WMt) == _NEGP,
       _ftp(_HW_P), _ftp(_HW_M), _HW_P != _HW_M),
    "PASS" if _a1_ok else "FAIL",
    "★★★ 这是本卷的地皮，而且每半都有独立来源：重数由组合计数 C(5,k) 预答、由矩阵对角实测，"
    "两路在 A1 里相遇；「奇类 == −偶类」也是矩阵层读出的（HC_M 从 MINUS 块 Sigma 的虚部对角来，"
    "不是从 −W 反推 —— G12 会拿两条路互印）。"
    "★ 最高权不同 ⇒ 两类是 so(10) 的**不等价**不可约表示，这就是「16 与 16bar 不同」的权层判定。"
    "★★ 但「谁叫 16 谁叫 16bar」是**命名约定**（依赖 Gamma 的编号）：本卷断言的是"
    "「两类不等价、SM 一代住偶类」，不断言「偶类」这个名字。与 r399 勘误、r400 A9 口径一致。")

# ============================================================ A2 折叠机制
_a2_ok = (cnt(Q_M) == _Q_PN and cnt(y_M) == _y_PN
          and cnt(Q_P) == SM_Q and cnt(Q_M) == SM_Q)
add(MAIN, "A2",
    "折叠机制：对线性 chi（A / T3L / K3 的任意有理组合），multiset(chi|奇类) = −multiset(chi|偶类)；"
    "对 chi = Q 再因 SM 电荷表自共轭 ⇒ 两类折出同一张表（r400 A10 免疫的结构原因）",
    "cnt(Q|奇) == cnt(−Q|偶) 且 cnt(y|奇) == cnt(−y|偶)；且 cnt(Q|偶) == cnt(Q|奇) == SM 电荷表（16 项）",
    "Q：奇==−偶 %s；y：奇==−偶 %s；Q|偶==SM_Q %s；Q|奇==SM_Q %s"
    % (cnt(Q_M) == _Q_PN, cnt(y_M) == _y_PN, cnt(Q_P) == SM_Q, cnt(Q_M) == SM_Q),
    "PASS" if _a2_ok else "FAIL",
    "★★ 这条一半是结构（chi 线性 + 奇类=−偶类 ⇒ 逐类取反），一半是实测："
    "Q|奇类 == SM_Q 是从 MINUS 块的矩阵对角折出来的，不是从「−偶类」反推的 —— "
    "在 A1 把矩阵层数据读进来之前，「两类折出同一张电荷表」只是一个待验断言。"
    "★ 免疫的机制到此说清：Q 折叠对共轭免疫，等价于 SM_Q 自共轭 —— 这不是 Q 的性质，"
    "是**那张表**的性质（A3 会把 y 表拿来做对照）。")

# ============================================================ A3 主判定
_yP_eq = cnt(y_P) == SM_Y
_yM_eq = cnt(y_M) == SM_Y
_yM_neg = cnt(y_M) == NSM_Y
_qsym = SM_Q == NSM_Q
_ysym = SM_Y == NSM_Y
_a3_ok = (_yP_eq and (not _yM_eq) and _yM_neg and _qsym and (not _ysym)
          and cnt(Q_P) == SM_Q and cnt(Q_M) == SM_Q)
add(MAIN, "A3",
    "主判定：Q 表自共轭 ⇒ 电荷判据分不开两类；y 表非自共轭 ⇒ 超荷判据分得开"
    "（偶类 == SM 超荷表，奇类 == 其逐项取反）⇒ SM 一代住在偶类",
    "SM_Q == −SM_Q（True，分不开）；SM_Y == −SM_Y（False，分得开）；"
    "cnt(y|偶) == SM_Y（True）；cnt(y|奇) == SM_Y（False）且 == −SM_Y（True）",
    "Q 表自共轭 = %s；y 表自共轭 = %s；y|偶 == SM_Y = %s；y|奇 == SM_Y = %s；y|奇 == −SM_Y = %s；"
    "Q|偶 = %s；Q|奇 = %s；y|偶 = %s；y|奇 = %s"
    % (_qsym, _ysym, _yP_eq, _yM_eq, _yM_neg,
       ctr_txt(cnt(Q_P)), ctr_txt(cnt(Q_M)), ctr_txt(cnt(y_P)), ctr_txt(cnt(y_M))),
    "PASS" if _a3_ok else "FAIL",
    "★★★ 同一套折叠、同一个线性机制，Q 分不开而 y 分得开 —— 差别只在**表自己的对称性**："
    "SM_Q 的 7 个值在取反下配对闭合，SM_Y 的 6 个值不闭合（取反后只剩 0 一个公共值）。"
    "★ 判定方向：SM_Y 是外部物理输入（16 项），偶类的 y 表与它相等、奇类的与它取反相等 "
    "⇒ SM 一代住偶类。这是 r400 A9 那条校正的补全：r400 只说了「本卷 y = SM 表」，"
    "本卷说明这恰好就是「住在哪一类」的判据。")

# ============================================================ A4 一比特·表述一（e 态）
_eP = [i for i in range(NC) if TL_P[i] == F(-1, 2) and y_P[i] == F(-1, 2)]
_eM = [i for i in range(NC) if TL_M[i] == F(-1, 2) and y_M[i] == F(-1, 2)]
_a4_ok = (len(_eP) == 1 and len(_eM) == 0 and _nm(WPt[_eP[0]]) % 2 == 0)
add(MAIN, "A4",
    "一比特·表述一：e 态的两个数 (T3L, y) = (−1/2, −1/2) 已经定类 —— "
    "它在偶类恰 1 态、在奇类 0 态",
    "偶类 1 态（权 (1/2,1/2,1/2,−1/2,−1/2)，#(−1/2) = 2 偶）；奇类 0 态（−SM_Y 不含 −1/2）",
    "偶类 %d 态（权 %s，#(−1/2)=%d）；奇类 %d 态"
    % (len(_eP), _ftp(WPt[_eP[0]]) if _eP else None, _nm(WPt[_eP[0]]) if _eP else -1, len(_eM)),
    "PASS" if _a4_ok else "FAIL",
    "★★ 这是最小充分输入的**单点版**：不需要整张 16 项表，一个非零 y 双态的两个数 (T3L, y) 就够。"
    "机制：双态 K3 = 0 ⇒ (T3L, y) 定 A ⇒ 定整个权 ⇒ 定宇称类。"
    "★ exp 的「奇类 0 态」是从外部表推的（−SM_Y 里没有 −1/2），act 是从矩阵对角折的 —— 两路独立。"
    "★★ 为什么必须是非零 y 的双态：K4 会给反例 —— y = 0 单态的 (T3L,y) = (0,0) 在两类各有一态，"
    "是折叠的不动点。")

# ============================================================ A5 一比特·表述二（nu^c）
_nuP = [i for i in range(NC) if y_P[i] == 0 and K_P[i] != 0]
_nuM = [i for i in range(NC) if y_M[i] == 0 and K_M[i] != 0]
_a5_ok = (len(_nuP) == 1 and len(_nuM) == 1
          and BL_P[_nuP[0]] == F(1) and BL_M[_nuM[0]] == F(-1)
          and _nm(WPt[_nuP[0]]) == 4 and _nm(WMt[_nuM[0]]) == 1)
add(MAIN, "A5",
    "一比特·表述二：y = 0 的单态在偶类 B-L = +1（nu^c）、在奇类 = −1（nu）——"
    "「哪个 y = 0 单态叫 nu^c」就是 r400 说的那层编号，它是一比特",
    "偶类 y = 0 单态恰 1 个、B-L = +1（落在 SM 的 B-L 表 {1:2} 那两格，r400 A2 读数）；"
    "奇类恰 1 个、B-L = −1；两态权互为取反",
    "偶类 %d 态 B-L = %s（权 %s，#(−1/2)=%d）；奇类 %d 态 B-L = %s（权 %s，#(−1/2)=%d）"
    % (len(_nuP), BL_P[_nuP[0]] if _nuP else None, _ftp(WPt[_nuP[0]]) if _nuP else None,
       _nm(WPt[_nuP[0]]) if _nuP else -1,
       len(_nuM), BL_M[_nuM[0]] if _nuM else None, _ftp(WMt[_nuM[0]]) if _nuM else None,
       _nm(WMt[_nuM[0]]) if _nuM else -1),
    "PASS" if _a5_ok else "FAIL",
    "★★★ 这是「编号层」这个名字的来源：SM 里 nu^c 的 B-L = +1（与 e^c 同占 {1:2} 那两格），"
    "共轭把这一格送到 −1（nu）。两个态在电荷/超荷层**完全同配**（K4：T3L = y = 0，两类各一），"
    "分开它们必须用 B-L —— 也就是必须用「哪个态叫 nu」这层名字。"
    "★ r400 A10 说的「引入费米子编号」在权语言里就是这一个比特，不是更多。")

# ============================================================ A6 一比特·表述三（扇区表）
_dzP = cnt([Q_P[i] for i in range(NC) if K_P[i] == 0])
_dzM = cnt([Q_M[i] for i in range(NC) if K_M[i] == 0])
_sect_n = (len([i for i in range(NC) if K_P[i] == 0]), len([i for i in range(NC) if K_M[i] == 0]))
_sect_inv = all(((w[3] - w[4]) == 0) == ((w[4] - w[3]) == 0) for w in WPt)
_dzP_neg = {-k: v for k, v in _dzP.items()}
_a6_ok = (_sect_n == (8, 8) and _dzM == _dzP_neg
          and _dzP != _dzP_neg and _sect_inv
          and sum(_dzP.values()) == 8 and sum(_dzM.values()) == 8)
add(MAIN, "A6",
    "一比特·表述三：双扇区（K3 = 0 的 8 态）的 Q 多重集在两类互为取反且非自共轭 ——"
    "扇区分辨的电荷表已经装着这个比特（这正是 r400 A5 用的输入）",
    "偶类双扇区表 {-1:1, -1/3:3, 0:1, 2/3:3}；奇类 {-2/3:3, 0:1, 1/3:3, 1:1}（= 逐项取反）；"
    "偶类表 != 其取反；K3 = 0 在取反下不变（扇区不换）",
    "偶类双扇区 %s；奇类双扇区 %s；互为取反 = %s；偶类表自共轭 = %s；扇区数 %s；K3=0 取反不变 = %s"
    % (ctr_txt(_dzP), ctr_txt(_dzM), _dzM == _dzP_neg,
       _dzP == _dzP_neg, _sect_n, _sect_inv),
    "PASS" if _a6_ok else "FAIL",
    "★ 总表（A3）对称而**扇区表**不对称 —— 把同一张电荷表按扇区切开，比特就露出来了。"
    "★★ 这条直接接 r400 A5：它用的正是扇区分辨的子表，所以 r400 的「lambda_A 唯一」"
    "其实是在已经选支的输入下给的（A8 显式化）。"
    "★ 机制：共轭保扇区（K3 -> −K3 不动 0），所以扇区表逐扇区取反，"
    "而子表 {−1, −1/3, 0, 2/3} 在取反下不闭合。")

# ============================================================ A7 下界（0 比特不够）与 4 解分类
_absyP = cnt([abs(x) for x in y_P])
_absyM = cnt([abs(x) for x in y_M])
_absqP = cnt([abs(x) for x in Q_P])
_absqM = cnt([abs(x) for x in Q_M])
_full = []
for la in _GRID:
    for lk in _GRID:
        if la == 0 and lk == 0:
            continue
        if cnt([TL_P[i] + la * A_P[i] + lk * K_P[i] for i in range(NC)]) == SM_Q:
            _full.append((la, lk))
_part = {}
for (la, lk) in _full:
    _yt = cnt([la * A_P[i] + lk * K_P[i] for i in range(NC)])
    _part[(la, lk)] = "SM" if _yt == SM_Y else ("NEG" if _yt == NSM_Y else "?")
_part_ok = all(_part[(la, lk)] == ("SM" if la < 0 else "NEG") for (la, lk) in _full)
_a7_ok = (_absyP == _absyM and _absqP == _absqM and len(_full) == 4 and _part_ok
          and len([1 for (la, lk) in _full if la < 0]) == 2
          and all(v != "?" for v in _part.values()))
add(MAIN, "A7",
    "下界：幅值表 |y| 与 |Q| 两类全同 ⇒ 0 比特（只用幅值或电荷的任何判据）分不开；"
    "全网格 4 解恰按 lambda_A 符号分成两支（lambda_A < 0 的两解给 SM 表、> 0 的两解给 −SM 表，"
    "lambda_K 那支不改变 y 表）⇒ 歧义恰为 Z2，一比特既是下界又是上界",
    "|y| 两类同表（16 项）；|Q| 两类同表；4 解分类只依赖 lambda_A 符号；两支各 2 解；无“?”项",
    "|y| 同 = %s（%s）；|Q| 同 = %s；4 解 = %s；分类 %s；按 lambda_A 分支正确 = %s"
    % (_absyP == _absyM, ctr_txt(_absyP), _absqP == _absqM,
       [(str(a), str(b)) for (a, b) in _full],
       {("%s,%s" % (a, b)): _part[(a, b)] for (a, b) in _full}, _part_ok),
    "PASS" if _a7_ok else "FAIL",
    "★★★ 这条把「最小」钉死在两头：**充分**由 A4/A5/A6 给（一比特够），"
    "**必要**由本条给（0 比特不够 —— 幅值运算与取反对易，任何只看幅值的判据对共轭盲）。"
    "★ 4 解 = Z2(lambda_A = 共轭) x Z2(lambda_K = eps4<->eps5)，其中只有 lambda_A 那支翻 y 表 —— "
    "也就是说 r400 全网格的 4 解里，翻类的只有一半，另一半连类都不翻（r400 A8 已证它是编号）。"
    "G11 机核这个分类。")

# ============================================================ A8 r400 张力显式化
_ZI = [i for i in range(NC) if K_P[i] == 0]
_solA_SM = [la for la in _GRID if la != 0 and cnt([TL_P[i] + la * A_P[i] for i in _ZI]) == _dzP]
_solA_CJ = [la for la in _GRID if la != 0 and cnt([TL_P[i] + la * A_P[i] for i in _ZI]) == _dzP_neg]
_a8_ok = (_solA_SM == [F(-1, 3)] and _solA_CJ == [F(1, 3)] and _dzP != _dzP_neg)
add(MAIN, "A8",
    "r400 张力显式化：用 SM 扇区表解 ⇒ lambda_A = −1/3（唯一）；换成共轭扇区表 ⇒ lambda_A = +1/3"
    "（唯一）。SM 扇区表本身非自共轭 ⇒ r400 A5 的「唯一」是在「给定 SM 扇区指认」下的唯一，"
    "那个指认已经选了 16 这一支",
    "SM 扇区表解 = [−1/3]；共轭扇区表解 = [+1/3]；SM 扇区表 == 其取反 = False",
    "SM 扇区表解 lambda_A = %s；共轭扇区表解 lambda_A = %s；SM 扇区表自共轭 = %s"
    % ([str(x) for x in _solA_SM], [str(x) for x in _solA_CJ], _dzP == _dzP_neg),
    "PASS" if _a8_ok else "FAIL",
    "★★ 这是本卷对 r400 的**诚实记账**，不是勘误：r400 的读数全对，"
    "但「lambda_A 唯一」这句话的适用范围要写明 —— 输入（扇区分辨电荷表）非自共轭，"
    "已经把共轭支排除在解空间外。"
    "★ 换成对称输入（只给总表）就回到 4 解（A7）；把输入换成共轭扇区表，唯一解翻到 +1/3 —— "
    "三种输入、三种解集，正好把「哪些是算的、哪些是指认的」摆在同一张桌上。"
    "★★ r400 文件不动：读数不变，只是本卷把那层指认显式化（与 r400 对 r399 的处理方式一致）。")

# ============================================================ A9 对称稳定性
def _sw(w):
    return (w[0], w[1], w[2], w[4], w[3])


_eps45_closed = {tuple(_sw(w)) for w in WPt} == set(WPt)
_eps45_class = all(_nm(_sw(w)) == _nm(w) for w in WPt)
_eps45_BLnu = all(F(-2, 3) * (_sw(w)[0] + _sw(w)[1] + _sw(w)[2])
                  == F(-2, 3) * (w[0] + w[1] + w[2]) for w in WPt)
_conj_flip = (BL_M[_nuM[0]] == -BL_P[_nuP[0]] and set(WMt) == _NEGP)
_a9_ok = (_eps45_closed and _eps45_class and _eps45_BLnu and _conj_flip)
add(MAIN, "A9",
    "对称稳定性（判别力双向验证）：eps4<->eps5（r400 A8 的编号约定）在偶类内闭环、不换宇称类、"
    "不翻 nu^c 的 B-L ⇒ 不翻比特；共轭（w -> −w）换类、翻 B-L ⇒ 翻比特",
    "eps4<->eps5：偶类闭环 16/16、#(−1/2) 不变、nu^c 的 B-L 不变；共轭：奇类 == −偶类、B-L 翻号",
    "eps45 闭环 = %s；不换类 = %s；保 nu^c 的 B-L = %s；共轭翻 B-L = %s（%s -> %s）"
    % (_eps45_closed, _eps45_class, _eps45_BLnu, _conj_flip, BL_P[_nuP[0]], BL_M[_nuM[0]]),
    "PASS" if _a9_ok else "FAIL",
    "★★ 一个判据要测它想测的东西：本卷的比特必须**对编号约定稳定**（eps4<->eps5 是 r400 A8 "
    "证过的权集对称；它若翻比特，比特就成了约定而不是物理）、**对共轭敏感**（它若不翻，就没有判别力）。"
    "两头都是算的，缺一头这个比特都不成立。"
    "★ 这正是「判据要测结构不测交换性」与「正负双对照」两条老纪律的合用。")

# ============================================================ A10 共轭完成自洽（边界）
_yc_M = [-x for x in y_M]
_Qc_M = [TL_M[i] - y_M[i] for i in range(NC)]
_a10_ok = (cnt(_yc_M) == SM_Y and cnt(_Qc_M) == SM_Q)
add(MAIN, "A10",
    "边界的另一半：在奇类上用 −Y 折叠，y 表 == SM 超荷表、Q 表 == SM 电荷表 ——"
    "「奇类 + 共轭嵌入」与「偶类 + SM 嵌入」在电荷/幅值层**完全不可区分**；"
    "分得开的只有宇称类（一比特）",
    "−y|奇 == SM_Y（True）；(T3L − y)|奇 == SM_Q（True）⇒ 两个自洽完成并存",
    "−y|奇 == SM_Y = %s；(T3L−y)|奇 == SM_Q = %s"
    % (cnt(_yc_M) == SM_Y, cnt(_Qc_M) == SM_Q),
    "PASS" if _a10_ok else "FAIL",
    "★★ 这条与 A7 是同一枚硬币的两面：A7 说 0 比特分不开（不存在更小的输入），"
    "本条说分不开的那个**另一个世界真的存在**（奇类上装 −Y，一切电荷/超荷读数与 SM 相同）。"
    "★ 所以「SM 一代住偶类」不是电荷层的胜利，是**一比特物理输入**（SM_Y 的符号结构）的胜利 —— "
    "这正是本卷对 r400 A10 的回答：边界不在电荷层关闭，在编号层关闭。"
    "★★ 本卷到此为止：不构造矩阵层共轭算子、不含质量谱 / Yukawa / 混合角；"
    "独有预言 0、不占度（度数链维持 36，r264 止）。")

# ============================================================ 控制组
_k1 = (_absyP == _absyM, _absyP == SM_Y)
add(CTL, "K1",
    "控制组（丢符号）：用 |y| 幅值表当分离判据",
    "(两类同表 True, == SM_Y False) —— 幅值表既分不开两类、也不是 SM 表",
    "两类同表 = %s；== SM_Y = %s" % _k1,
    "PASS" if _k1 == (True, False) else "FAIL",
    "★ 两个读数都有用：第一个说明幅值层无判别力（A7 下界的实感版），"
    "第二个说明幅值表连「对的那张表」都不是 —— 丢符号丢的不只是类的信息，还有表本身。")
_k2 = (cnt(Q_P) == cnt(Q_M), cnt(Q_P) == SM_Q)
add(CTL, "K2",
    "控制组（丢扇区）：用总 Q 多重集当分离判据（r400 A6 的输入）",
    "(两类同表 True, == SM_Q True) —— 总表分不开，但它确实是 SM 的表",
    "两类同表 = %s；== SM_Q = %s" % _k2,
    "PASS" if _k2 == (True, True) else "FAIL",
    "★ 与 K1 对照着读：总 Q 表**是**正确的物理表却**没有**判别力 —— "
    "「表对」与「分得开」是两件事（r397 A8「谱同而核不同」的族裔）。")
_wm_bad = list(WMt)
_wm_bad[0] = WPt[3]
_sb = set(_wm_bad)
_k3 = (len(set(WPt) & _sb), len(set(WPt) | _sb), _sb == _NEGP)
add(CTL, "K3",
    "控制组（污染类）：把奇类权集的一个权换成偶类的 ⇒ A1 的三条结构断言全红",
    "(相交 1, 并 31, == −偶类 False) —— 判别力：A1 不是恒绿",
    "相交 %d；并集 %d；== −偶类 = %s" % _k3,
    "PASS" if _k3 == (1, 31, False) else "FAIL",
    "★ 一个 100% 通过的谓词判别力为 0：A1 的「不相交 / 并 = 32 / 互为取反」必须能被一个污染实例打红，"
    "否则它只是在复述定义。")
_fpP = [i for i in range(NC) if TL_P[i] == 0 and y_P[i] == 0]
_fpM = [i for i in range(NC) if TL_M[i] == 0 and y_M[i] == 0]
_k4 = (len(_fpP), len(_fpM), BL_P[_fpP[0]], BL_M[_fpM[0]])
add(CTL, "K4",
    "控制组（折叠不动点）：(T3L, y) = (0, 0) 的态在两类**各有一个** —— 电荷/超荷层对此完全无判别力",
    "(偶类 1, 奇类 1, B-L +1, B-L −1) —— 必须加 B-L 才分开",
    "偶类 %d 态；奇类 %d 态；B-L = (%s, %s)" % _k4,
    "PASS" if _k4 == (1, 1, F(1), F(-1)) else "FAIL",
    "★★★ 这就是 nu^c / nu 那一对：它们是折叠的不动点（0 = −0），"
    "所以「哪个 y = 0 单态叫 nu^c」**不可能**由任何 (T3L, y) 数据回答 —— "
    "A4 那条最小输入必须用非零 y 的态（或像 A5 那样加 B-L），这不是实现细节，是结构限制。")

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

_readings = [_k1, _k2, _k3, _k4]
_k4s = "(%d, %d, %s, %s)" % _k4
add(GRD, "G03", "四个控制组必须两两给出不同读数", "4 个不同读数",
    "K1 %s；K2 %s；K3 %s；K4 %s（%d 个不同）"
    % (_k1, _k2, _k3, _k4s, len(set(_readings))),
    "PASS" if len(set(_readings)) == 4 else "FAIL",
    "★ K1/K2 都是「分不开」型负控，读数必须靠第二个分量分开；K3/K4 靠结构分开。")

add(GRD, "G04", "每条都有非空 note 且 computed", "0 违规",
    "%d 违规（覆盖 %d 条）" % (sum(1 for r in ALL if not r["note"] or not r["computed"]), len(ALL)),
    "PASS" if all(r["note"] and r["computed"] for r in ALL) else "FAIL",
    "★ 收尾整表重扫。")

TR_P = [(w[3] - w[4]) / 2 for w in WPt]
TR_M = [(w[3] - w[4]) / 2 for w in WMt]
_g5 = (len(WPt) == 16 and len(WMt) == 16 and not (set(WPt) & set(WMt))
       and len([1 for i in range(NC) if K_P[i] == 0]) == 8
       and len([1 for i in range(NC) if K_M[i] == 0]) == 8
       and all(not (TL_P[i] != 0 and TR_P[i] != 0) for i in range(NC))
       and all(not (TL_M[i] != 0 and TR_M[i] != 0) for i in range(NC)))
add(GRD, "G05", "维数账：两类各 16、互不相交；两类的双扇区各 8+8；两类都没有态同时带 T3L 与 T3R",
    "闭合",
    "两类 %d/%d；双扇区 %d+%d / %d+%d；同时非零 %d+%d"
    % (len(WPt), len(WMt),
       len([1 for i in range(NC) if K_P[i] == 0]), len([1 for i in range(NC) if K_P[i] != 0]),
       len([1 for i in range(NC) if K_M[i] == 0]), len([1 for i in range(NC) if K_M[i] != 0]),
       len([1 for i in range(NC) if TL_P[i] != 0 and TR_P[i] != 0]),
       len([1 for i in range(NC) if TL_M[i] != 0 and TR_M[i] != 0])),
    "PASS" if _g5 else "FAIL",
    "★ 账要在**两类**上各做一遍：A5/A6 的结论在奇类上同样用（奇类也有 8+8 的扇区），"
    "只查偶类会漏掉一半的世界。")

_g6 = (sum(SM_Q.values()) == NC and sum(SM_Y.values()) == NC and sum(NSM_Y.values()) == NC
       and sum(_dzP.values()) == 8 and sum(_dzM.values()) == 8)
add(GRD, "G06", "表闭合：SM_Q / SM_Y / −SM_Y 各 16 项；双扇区表各 8 项", "16/16/16 与 8/8",
    "SM_Q %d；SM_Y %d；−SM_Y %d；dz|偶 %d；dz|奇 %d"
    % (sum(SM_Q.values()), sum(SM_Y.values()), sum(NSM_Y.values()),
       sum(_dzP.values()), sum(_dzM.values())),
    "PASS" if _g6 else "FAIL",
    "★ 少一项就说明某个扇区被漏掉，而扇区分解会静默成立。")

_g7 = (len(KEYS) == 45 and len(HC) == 5 and len(HC_M) == 5
       and all(len(w) == 5 for w in W) and all(len(w) == 5 for w in WM)
       and all(abs(x) == F(1, 2) for w in W for x in w)
       and all(abs(x) == F(1, 2) for w in WM for x in w)
       and all(HC[i][0][k][k] == 0 for i in range(5) for k in range(NC))
       and all(HC_M[i][0][k][k] == 0 for i in range(5) for k in range(NC)))
add(GRD, "G07", "完备性：45 个 Sigma、两块各 5 个 Cartan、权全 5 维 ±1/2、两块 Cartan 实部对角全 0",
    "45 / 5+5 / 5 / 实部 0",
    "Sigma %d；Cartan %d+%d；权维 %s；|权元| = %s；实部全零 = %s"
    % (len(KEYS), len(HC), len(HC_M), sorted({len(w) for w in W} | {len(w) for w in WM}),
       sorted({str(abs(x)) for w in W for x in w} | {str(abs(x)) for w in WM for x in w}),
       all(HC[i][0][k][k] == 0 for i in range(5) for k in range(NC))
       and all(HC_M[i][0][k][k] == 0 for i in range(5) for k in range(NC))),
    "PASS" if _g7 else "FAIL",
    "★ 奇类权是从 MINUS 块 Sigma 的**虚部**对角读的（与偶类同口径），实部必须全零 —— "
    "否则「权」这个读法本身不成立（r399 的老守卫，本卷在两块上各跑一遍）。")

VERDICT = "--".join([
    "TWO-PARITY-CLASSES" if _a1_ok else "CLASS-STRUCTURE-BROKEN",
    "Q-FOLD-CONJUGATION-IMMUNE" if _a2_ok else "Q-FOLD-SENSITIVE",
    "Y-SEPARATES-THE-TWO" if _a3_ok else "Y-CANNOT-SEPARATE",
    "ONE-BIT-SUFFICIENT-3-WAYS" if (_a4_ok and _a5_ok and _a6_ok) else "ONE-BIT-OPEN",
    "ZERO-BIT-INSUFFICIENT" if _a7_ok else "ZERO-BIT-MIGHT-SUFFICE",
    "R400-A5-INPUT-CHOSE-BRANCH" if _a8_ok else "R400-A5-NEUTRAL-INPUT",
    "BIT-STABLE-UNDER-EPS45" if _a9_ok else "BIT-CONVENTION-DEPENDENT",
    "CONJUGATE-COMPLETION-CONSISTENT" if _a10_ok else "CONJUGATE-COMPLETION-BROKEN",
])
add(GRD, "G08", "判词与判定表必须同一读数（两路径拼接）", "两路一致",
    "由变量拼：%s" % VERDICT,
    "PASS" if (_a1_ok and _a2_ok and _a3_ok and _a4_ok and _a5_ok and _a6_ok
               and _a7_ok and _a8_ok and _a9_ok and _a10_ok) else "FAIL",
    "★ 判词每一段由一个布尔量决定，不写字面量。")

g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "（回填）", "（回填）", "INFO",
          "★ 先占位再回填（r396 E06：报告必须在回填之后才拼）")

DECLARED_NEG = set()
_neg_fail = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G10", "真判负必须逐条登记", "登记集 == 实际 FAIL 集",
    "%s vs %s" % (sorted(DECLARED_NEG), _neg_fail),
    "PASS" if sorted(DECLARED_NEG) == _neg_fail else "FAIL",
    "★ 本卷若无判负，登记集为空。")

_EXP4 = {(F(-1, 3), F(1, 2)), (F(-1, 3), F(-1, 2)),
         (F(1, 3), F(1, 2)), (F(1, 3), F(-1, 2))}
_g11 = (len(_full) == 4 and _part_ok
        and all(_part[(la, lk)] == ("SM" if la == F(-1, 3) else "NEG") for (la, lk) in _full)
        and set(_full) == _EXP4
        and len({lk for (la, lk) in _full if la == F(-1, 3)}) == 2)
add(GRD, "G11", "主关系：4 解 = Z2(lambda_A = 共轭) x Z2(lambda_K = eps45)，只有 lambda_A 支翻 y 表",
    "4 解 = {±1/3} x {±1/2}（r400 A6 读数反抄）；分类只依赖 lambda_A；lambda_A = −1/3 支内两解同表",
    "分类 %s；按 lambda_A 分支正确 = %s；−1/3 支内 lambda_K 取值 %s；解集 == 反抄值 %s"
    % ({("%s,%s" % (a, b)): _part[(a, b)] for (a, b) in _full}, _part_ok,
       sorted({lk for (la, lk) in _full if la == F(-1, 3)}), set(_full) == _EXP4),
    "PASS" if _g11 else "FAIL",
    "★★★ 这是本卷的总纲机核：r400 给了 4 解，本卷给**每一个解**定类 —— "
    "翻 y 表的恰是 lambda_A 那支（共轭），lambda_K 那支（eps4<->eps5）连表都不换。"
    "★ 期望解集反抄自 r400 report 的 A6 读数（另一卷的独立路径），不在本卷内自证。")

_g12 = (sorted(WMt) == sorted([tuple(-x for x in w) for w in W])
        and cnt(y_M) == cnt([-y_P[i] for i in range(NC)]))
add(GRD, "G12", "两路拼关键量：奇类权（矩阵对角路）== −偶类权（集合取反路）；"
    "y|奇（从 WM 折）== −y|偶（从 W 折再取反）", "两路一致",
    "权：%s；y：%s" % (sorted(WMt) == sorted([tuple(-x for x in w) for w in W]),
                     cnt(y_M) == cnt([-y_P[i] for i in range(NC)])),
    "PASS" if _g12 else "FAIL",
    "★ 一条从 MINUS 块 Sigma 的对角读，一条从 PLUS 权取反 —— 两条路在 A1/A2 之后再次互印，"
    "「奇类 == −偶类」不再依赖任何单一路径。")

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


# ---- G14 关键表：两路机拼（左 = 缓存变量；右 = 现场重算，不引用缓存）
_FORM1 = ("两类：偶类 #(−1/2) 重数 %s；奇类重数 %s；奇类==−偶类 = %s；最高权 %s vs %s（不等 = %s）")
_FORM2 = "折叠：Q|偶 == Q|奇 == SM_Q = %s；y|偶 == SM_Y = %s；y|奇 == −SM_Y = %s"
_FORM3 = "一比特三表述：e 态 (偶 %d / 奇 %d)；nu^c 的 B-L (%s, %s)；双扇区表自共轭 = %s"
_FORM4 = "下界与完成：|y| 两类同 = %s；4 解按 lambda_A 分支 = %s；共轭完成自洽 = %s"

_KT1 = _FORM1 % (ctr_txt(_PAR_P), ctr_txt(_PAR_M), set(WMt) == _NEGP,
                 _ftp(_HW_P), _ftp(_HW_M), _HW_P != _HW_M)
_KT2 = _FORM2 % (cnt(Q_P) == SM_Q and cnt(Q_M) == SM_Q, _yP_eq, _yM_neg)
_KT3 = _FORM3 % (len(_eP), len(_eM), BL_P[_nuP[0]], BL_M[_nuM[0]], _dzP == _dzP_neg)
_KT4 = _FORM4 % (_absyP == _absyM, _part_ok, _a10_ok)

# —— 右路：一切从原始数据现场重算（不引用 _PAR_/_dzP/_full 等缓存）
_r_WP = [tuple(v) for v in W]
_r_WM = [tuple(HC_M[i][1][k][k] for i in range(5)) for k in range(NC)]
_r_mP = cnt([sum(1 for x in w if x < 0) for w in _r_WP])
_r_mM = cnt([sum(1 for x in w if x < 0) for w in _r_WM])
_r_hwP = max(_r_WP)
_r_hwM = max(_r_WM)
_r_fold = lambda ws: ([w[0] + w[1] + w[2] for w in ws],
                      [(w[3] + w[4]) / 2 for w in ws],
                      [w[3] - w[4] for w in ws])
_r_AP, _r_TLP, _r_KP = _r_fold(_r_WP)
_r_AM, _r_TLM, _r_KM = _r_fold(_r_WM)
_r_QP = [_r_TLP[i] + F(-1, 3) * _r_AP[i] + F(1, 2) * _r_KP[i] for i in range(NC)]
_r_QM = [_r_TLM[i] + F(-1, 3) * _r_AM[i] + F(1, 2) * _r_KM[i] for i in range(NC)]
_r_yP = [F(-1, 3) * _r_AP[i] + F(1, 2) * _r_KP[i] for i in range(NC)]
_r_yM = [F(-1, 3) * _r_AM[i] + F(1, 2) * _r_KM[i] for i in range(NC)]
_r_eP = [i for i in range(NC) if _r_TLP[i] == F(-1, 2) and _r_yP[i] == F(-1, 2)]
_r_eM = [i for i in range(NC) if _r_TLM[i] == F(-1, 2) and _r_yM[i] == F(-1, 2)]
_r_nP = [i for i in range(NC) if _r_yP[i] == 0 and _r_KP[i] != 0]
_r_nM = [i for i in range(NC) if _r_yM[i] == 0 and _r_KM[i] != 0]
_r_dzP = cnt([_r_QP[i] for i in range(NC) if _r_KP[i] == 0])
_r_dzM = cnt([_r_QM[i] for i in range(NC) if _r_KM[i] == 0])
_r_abs = cnt([abs(x) for x in _r_yP]) == cnt([abs(x) for x in _r_yM])
_r_full = [(a, b) for a in [F(k, 12) for k in range(-24, 25)]
           for b in [F(k, 12) for k in range(-24, 25)] if (a, b) != (0, 0)
           and cnt([_r_TLP[i] + a * _r_AP[i] + b * _r_KP[i] for i in range(NC)]) == SM_Q]
_r_partok = all((cnt([a * _r_AP[i] + b * _r_KP[i] for i in range(NC)]) == SM_Y) == (a < 0)
                for (a, b) in _r_full)
_r_conj = (cnt([-x for x in _r_yM]) == SM_Y and
           cnt([_r_TLM[i] - _r_yM[i] for i in range(NC)]) == SM_Q)

_KT1r = _FORM1 % (ctr_txt(_r_mP), ctr_txt(_r_mM), set(_r_WM) == {tuple(-x for x in w) for w in _r_WP},
                  _ftp(_r_hwP), _ftp(_r_hwM), _r_hwP != _r_hwM)
_KT2r = _FORM2 % (cnt(_r_QP) == SM_Q and cnt(_r_QM) == SM_Q,
                  cnt(_r_yP) == SM_Y, cnt(_r_yM) == NSM_Y)
_KT3r = _FORM3 % (len(_r_eP), len(_r_eM),
                  F(-2, 3) * _r_AP[_r_nP[0]], F(-2, 3) * _r_AM[_r_nM[0]],
                  _r_dzP == {-k: v for k, v in _r_dzP.items()})
_KT4r = _FORM4 % (_r_abs, _r_partok, _r_conj)

_kt_all = " || ".join([_KT1, _KT2, _KT3, _KT4])
_kt_re = " || ".join([_KT1r, _KT2r, _KT3r, _KT4r])
add(GRD, "G14", "关键表每一句都必须由变量拼出，且两条独立路径（缓存变量 / 现场重算）字面相等",
    "两路字面相等",
    "左路：%s || 右路：%s || 相等 = %s" % (_kt_all, _kt_re, _kt_all == _kt_re),
    "PASS" if (_kt_all == _kt_re and _a2_ok and _a3_ok and _a6_ok and _a7_ok and _a10_ok) else "FAIL",
    "★★ r396 E02 / r397 E09 / r398 E06 / r399 E07 的第六次继承：关键表**每一句都由变量拼**。"
    "★ 这里多一层：右路完全不引用缓存，从 W / WM 原始数据重折一遍 —— "
    "「关键表写对」不再依赖任何记忆，也不依赖左路的中间量。")

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
               rows=ALL, declared_neg=sorted(DECLARED_NEG))
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
A("对象：X-GSM-6（编号层与宇称类：16 与 16bar 的一比特分离）")
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
A("读数：偶类重数 %s；奇类重数 %s；Q 表自共轭 %s；y|偶==SM %s；y|奇==−SM %s；"
  "e 态 %d/%d；nu^c 的 B-L (%s, %s)；|y| 两类同 %s；4 解分类 %s；共轭完成 %s"
  % (ctr_txt(_PAR_P), ctr_txt(_PAR_M), _qsym, _yP_eq, _yM_neg,
     len(_eP), len(_eM), BL_P[_nuP[0]], BL_M[_nuM[0]], _absyP == _absyM, _part_ok, _a10_ok))
A("")
A("【诚实边界】")
A(" 1) 「一比特」本身是**物理输入**：A5 的 nu^c 的 B-L = %s（等价的 A4：e 态 (T3L,y) = (−1/2,−1/2) 定出的权是 %s）。"
  "本卷证明的是这一比特**必要且充分**（必要 = A7 的 |y| 两路同表，充分 = A4/A5/A6 三表述），"
  "不是「没有输入」；"
  % (BL_P[_nuP[0]], _ftp(WPt[_eP[0]])))
A(" 2) 本卷全部在**权层**：不构造 16 <-> 16bar 的矩阵层共轭算子，也不在矩阵层验证表示不等价"
  "（不等价由最高权判定：%s vs %s）。谁叫 16 谁叫 16bar 是命名约定，本卷只断言「两类不等价、"
  "SM 一代住偶类（手征 +1 块）」；" % (_ftp(_HW_P), _ftp(_HW_M)))
A(" 3) r400 A5 的唯一性重读：其扇区输入已选支（A8 读数：SM 扇区表给 %s、共轭扇区表给 %s）。"
  "r400 文件不动、读数不改，本卷只把那层指认显式化；"
  % ([str(x) for x in _solA_SM], [str(x) for x in _solA_CJ]))
A(" 4) nu^c / nu 是折叠的不动点（K4 读数：两类各 %d 态，(T3L,y) 都是 (0,0)，B-L 为 %s / %s）"
  "⇒ 分开这一对**必须**用 B-L，也就是命名。这就是「编号层」这个名字的精确含义；"
  % (_k4[0], BL_P[_fpP[0]], BL_M[_fpM[0]]))
A(" 5) 「分离」不产生新预言：本卷给出的是**类的判定**，独有预言 0、不占度（度数链维持 36，r264 止）；")
A(" 6) 本卷不含质量谱 / Yukawa / 混合角，也不构造 16 x 16 x 126bar 型不变量 —— "
  "「一比特分开了类」不等于「类上的动力学被定下」。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("JSON ->", JSN)
print("RPT  ->", RPT)
print("FINAL =", FINAL)
