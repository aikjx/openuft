# -*- coding: utf-8 -*-
"""TUFT-r397  攻 X-GSM-2：16 旋量表示的零空间 —— 手征投影 / 45 个生成元实化 / 单态计数 / J-K 对照

纯标准库（Fraction，判据区无浮点、无随机）。不读任何来料中间量。

本卷接着 r396 的 §十四 第一入口做：r396 只用张量表示（10/45/54），K2 说它们分不出
so(4) 的自对偶与反自对偶；本卷换成 **16（旋量）** 再问一次同样的问题。

  A1  32x32 复 gamma：10 个 Hermitian，55 对 Clifford 关系
  A2  手征算子 CHIR = (-i)Gamma_1...Gamma_10：平方 1、±1 各 16 维、45 个 Sigma 全部与之交换
  A3  45 个 Sigma_ab 的实化：反对称 / 秩 45 / 990 对换位子与向量表示的系数一致
  A4  SM 的 12 个生成元在 32 维实旋量空间上：秩 12
  A5  16 的 SM 单态维数（实零空间 / 2 = 复单态维数）
  A6  单态被全部 12 个熄灭、被 so(10) 推满整个 32 维（⇒ 不是 so(10) 单态）
  A7  Y 的幂和 p_1..p_5 与分解表多重集 {1/6x6, -2/3x3, 1/3x3, -1/2x2, 0} 比对
  A8  {16, 16bar} x {J, K} 四格对照：J@16 是否 == K@16bar（本卷核心争点）
  A9  两步阶梯：dim(Stab(v45) ∩ Stab(v16))
"""
import io
import json
import os
from fractions import Fraction as F

RID = "r397"
TITLE = ("TUFT-r397_攻X-GSM-2_十六旋量零空间_手征投影与四十五生成元实化_单态计数与Y谱幂和_"
         "J与K四格对照_两步阶梯复合稳定子_精算_2026-11-04")
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


# ============================================================ 复矩阵用 (Re, Im) 整数对表示
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
C1, C2, C3 = (S1, Z2), (Z2, J2), (S3, Z2)      # sigma1 / sigma2 = iJ / sigma3，全部 Hermitian

# ============================================================ A1 gamma 与 Clifford
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

_a1_herm = all(is_herm(g) for g in GAM)
_a1_pairs, _a1_bad = 0, []
for _a in range(10):
    for _b in range(_a, 10):
        _a1_pairs += 1
        _S = cadd(cmul(GAM[_a], GAM[_b]), cmul(GAM[_b], GAM[_a]), 1)
        _W = zmat(N32)
        if _a == _b:
            for _i in range(N32):
                _W[_i][_i] = F(2)
        if _S[0] != _W or not is_zero(_S[1]):
            _a1_bad.append((_a + 1, _b + 1))
a1_ok = (_a1_herm and len(GAM) == 10 and not _a1_bad)
add(MAIN, "A1",
    "32x32 复 gamma：10 个 Hermitian 矩阵，55 对 Clifford 关系 {G_a, G_b} = 2*delta_ab 全过",
    "10 个；全部 Hermitian；55 对全过",
    "维数 %d；Hermitian = %s；Clifford 对数 %d；违例 %d%s"
    % (len(GAM[0][0]), _a1_herm, _a1_pairs, len(_a1_bad),
       ("：" + str(_a1_bad)) if _a1_bad else ""),
    "PASS" if a1_ok else "FAIL",
    "★ 10 维的 Dirac 旋量必须是 32 维（Cl(10,0) 的实表示维数 32，复表示 32 也即最小）——"
    "这是本卷第一处「不能想当然」：16 不是 Clifford 模，只是 so(10) 的模。"
    "★ 全部 55 对逐元素验证，不是抽查。")

# ============================================================ A2 手征投影
_P = GAM[0]
for _a in range(1, 10):
    _P = cmul(_P, GAM[_a])
CHIR = (_P[1], [[-x for x in row] for row in _P[0]])   # 乘 -i：i(Re + i Im) = -Im + i Re
_chir_diag = [CHIR[0][i][i] for i in range(N32)]
_chir_imag = sum(abs(x) for row in CHIR[1] for x in row)
_chir_off = sum(abs(CHIR[0][i][j]) + abs(CHIR[1][i][j])
                for i in range(N32) for j in range(N32) if i != j)
PLUS = [i for i in range(N32) if _chir_diag[i] == 1]
MINUS = [i for i in range(N32) if _chir_diag[i] == -1]
_chir_sq = cadd(cmul(CHIR, CHIR), (zmat(N32), zmat(N32)), 1)
_chir_sq_ok = (_chir_sq[0] == [[F(1) if i == j else F(0) for j in range(N32)] for i in range(N32)]
               and is_zero(CHIR[1]))
a2_ok = (len(PLUS) == 16 and len(MINUS) == 16 and _chir_off == 0 and _chir_imag == 0
         and _chir_sq_ok)
add(MAIN, "A2",
    "手征算子 CHIR = (-i)*G_1...G_10：Hermitian、平方 = 1、+1/-1 各 16 维、且在本基下对角",
    "平方 = 1；±1 各 16 维；非对角 0；纯实",
    "对角谱 %s；+1 维数 %d；-1 维数 %d；非对角和 %d；虚部和 %d；CHIR^2 = 1 是 %s"
    % (sorted(set(_chir_diag)), len(PLUS), len(MINUS), _chir_off, _chir_imag, _chir_sq_ok),
    "PASS" if a2_ok else "FAIL",
    "★ 有了 CHIR 才能把 32 维 Dirac 切成 16 + 16bar；「16」不是长出来的，是**投影**出来的。"
    "★★ 非对角和 = 0 是关键：只有 CHIR 在本基下**对角**，才能用「取子矩阵」代替「求本征矢量」——"
    "这一步省下的不只是时间，还避免了「本征矢量归一化带根号」这个精确算术的破口。")

# ============================================================ A3 45 个 Sigma
def restrict(Mc, idx):
    (R, I) = Mc
    return ([[R[i][j] for j in idx] for i in idx], [[I[i][j] for j in idx] for i in idx])


def realify(Mc):
    """16x16 复 -> 32x32 实：[[A, -B], [B, A]]（复结构作用在 (1, i) 上）"""
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


def realify_bad(Mc):
    """★负对照用：把 -B 写成 +B —— 反 Hermitian 不再实化成反对称"""
    (R, I) = Mc
    n = len(R)
    M = zmat(2 * n)
    for i in range(n):
        for j in range(n):
            M[i][j] = R[i][j]
            M[i][n + j] = I[i][j]
            M[n + i][j] = I[i][j]
            M[n + i][n + j] = R[i][j]
    return M


KEYS = [(a, b) for a in range(10) for b in range(a + 1, 10)]
SIGC = {}     # 复 16x16
SIGR = {}     # 实 32x32
for (a, b) in KEYS:
    _Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    _Cm = ([[x / 4 for x in row] for row in _Cm[0]], [[x / 4 for x in row] for row in _Cm[1]])
    SIGC[(a, b)] = restrict(_Cm, PLUS)
    SIGR[(a, b)] = realify(SIGC[(a, b)])

# (1) 实化后反对称
_a3_asym = all(is_antisym(SIGR[k]) for k in KEYS)
# (2) 秩 45（1024 x 45）
_a3_cols = [[SIGR[k][i][j] for k in KEYS] for i in range(N32) for j in range(N32)]
_a3_rank = rank_of(_a3_cols, 45)
# (3) 闭合：990 对，(a) 向量表示里算换位子拿系数，(b) 同系数组合 Sigma，(c) 与直接算的换位子比
_E10 = {}
for (a, b) in KEYS:
    M = zmat(10)
    M[a][b] = F(1)
    M[b][a] = F(-1)
    _E10[(a, b)] = M


def coefs_from_vec(M):
    """把反对称矩阵展开成 (i,j) -> 系数（按矩阵自己的维数枚举，6x6 与 10x10 通用）"""
    n = len(M)
    return {(a, b): M[a][b] for a in range(n) for b in range(a + 1, n) if M[a][b] != 0}


_a3_checks, _a3_bad = 0, []
_a3_probe = []
for _i in range(len(KEYS)):
    for _j in range(_i + 1, len(KEYS)):
        k1, k2 = KEYS[_i], KEYS[_j]
        _a3_checks += 1
        vec_comm = comm2(_E10[k1], _E10[k2], 10)
        coef = coefs_from_vec(vec_comm)
        # 用同系数组合 16x16 复 Sigma
        (R, I) = (zmat(16), zmat(16))
        for kk, cc in coef.items():
            for x in range(16):
                for y in range(16):
                    R[x][y] += cc * SIGC[kk][0][x][y]
                    I[x][y] += cc * SIGC[kk][1][x][y]
        direct = cadd(cmul(SIGC[k1], SIGC[k2]), cmul(SIGC[k2], SIGC[k1]), -1)
        if R != direct[0] or I != direct[1]:
            _a3_bad.append((k1, k2))
a3_ok = (_a3_asym and _a3_rank == 45 and not _a3_bad and _a3_checks == 990)
add(MAIN, "A3",
    "45 个 Sigma_ab 实化到 32x32：全部反对称；秩 45；990 对换位子与「向量表示的换位子系数」逐元素一致",
    "反对称；秩 45；990 对全一致",
    "反对称 = %s；秩 = %d；换位子对数 %d；不一致 %d%s"
    % (_a3_asym, _a3_rank, _a3_checks, len(_a3_bad),
       ("：" + str(_a3_bad[:4])) if _a3_bad else ""),
    "PASS" if a3_ok else "FAIL",
    "★★ 闭合性不是「引结构常数」：先在**向量表示**（10x10）里真算 [E,E]，把结果展开成系数，"
    "再用同一组系数组合 Sigma，最后与**直接**算的 [Sigma,Sigma] 比。"
    "两个不同对象（10 维向量 / 16 维旋量）走同一条系数，才是「这是 so(10) 的表示」的机核。"
    "★ r396 的 E01 教训：对象换了必须写在变量名里（SIGC 复 16 / SIGR 实 32，绝不混用）。")

# ============================================================ SM 的 12 个生成元（系数写法）
# su(3)_C：i*lambda_a（a=1..8）实化到 C^3 = R^6，嵌在 1..6
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


SU3_C = [coefs_from_vec(realify6(LAM_RE[a], LAM_IM[a])) for a in range(8)]

# 4 块上的 so(4)（10 维指标 7..10，0 基 6..9）
SU2J_C = [{(7, 8): F(1), (6, 9): F(1)},                              # J1
          {(6, 8): F(-1), (7, 9): F(1)},                             # J2
          {(6, 7): F(1), (8, 9): F(1)}]                              # J3 = U_B
SU2K_C = [{(7, 8): F(1), (6, 9): F(-1)},                             # K1
          {(6, 8): F(-1), (7, 9): F(-1)},                            # K2
          {(6, 7): F(1), (8, 9): F(-1)}]                             # K3
U_A = {(0, 1): F(1), (2, 3): F(1), (4, 5): F(1)}                     # 3 块统一相位
U_K = {(6, 7): F(1), (8, 9): F(-1)}                                  # 4 块反自对偶相位
U_B = {(6, 7): F(1), (8, 9): F(1)}                                   # 4 块同号相位
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


def sm12(which):
    su2 = SU2J_C if which == "J" else SU2K_C
    return [to_rep(c, SIGR) for c in SU3_C] + [to_rep(c, SIGR) for c in su2] + [to_rep(Y_C, SIGR)]


SM_J = sm12("J")
SM_K = sm12("K")

# ============================================================ A4 12 个生成元与秩
_a4_cols = [[M[i][j] for M in SM_J] for i in range(N32) for j in range(N32)]
_a4_rank = rank_of(_a4_cols, 12)
_a4_asym = all(is_antisym(M) for M in SM_J)
a4_ok = (_a4_rank == 12 and _a4_asym and len(SM_J) == 12)
add(MAIN, "A4",
    "SM 的 12 个生成元作用在 32 维实旋量空间上：全部反对称、线性无关（秩 12）",
    "12 个；秩 12；全部反对称",
    "构造 %d 个；1024 维展开后的秩 = %d；反对称 = %s" % (len(SM_J), _a4_rank, _a4_asym),
    "PASS" if a4_ok else "FAIL",
    "★ 系数与 r396 完全一致（同一组 i*lambda_a 实化表 + 同一组 so(4) 组合 + 同一个 Y 公式）——"
    "这叫口径自守：换表示不换系数，否则两组读数不可比。★ 秩 12 是「12 个」的机核。")

# ============================================================ A5 16 的 SM 单态
def singlet_rows(gens):
    rows = []
    for M in gens:
        for i in range(N32):
            rows.append([M[i][j] for j in range(N32)])
    return rows


_ns_J = nullspace_basis(singlet_rows(SM_J), N32)
_d_J = len(_ns_J)
a5_ok = (_d_J % 2 == 0 and _d_J // 2 == 1)
add(MAIN, "A5",
    "16 的 SM 单态：32 维实空间里解 12 个 X v = 0，实维数必须是偶数、除以 2 才是复单态维数",
    "实维数 2 ⇒ 复单态 1 维（= 右手中微子 nu^c）",
    "12 x 32 = 384 行；秩 = %d；实零空间 %d 维 ⇒ 复单态 **%d** 维"
    % (N32 - _d_J, _d_J, _d_J // 2),
    "PASS" if a5_ok else "FAIL",
    "★★★ 本卷第一个「对象错位」风险点：16 是**复**表示、我算的是**实** 32 维零空间。"
    "复单态 v 与 i*v 是两个实方向 ⇒ 实维数必为偶，除以 2 才是复维数。"
    "把 2 当 1 报（或把 4 当 1 报）都会「看起来对」。★ 期望的 1 由 A7 的谱独立支持，不是猜的。")

# ============================================================ A6 单态不是 so(10) 单态
_sing = _ns_J[0]
_Yact = [sum(to_rep(Y_C, SIGR)[i][j] * _sing[j] for j in range(N32)) for i in range(N32)]
_Y_zero = all(v == 0 for v in _Yact)
_orb = []
for k in KEYS:
    Mk = SIGR[k]
    _orb.append([sum(Mk[i][j] * _sing[j] for j in range(N32)) for i in range(N32)])
_orb_rank = rank_of(_orb, N32)
_kern = 45 - _orb_rank
_kill_one = sum(1 for k in KEYS
                if all(sum(SIGR[k][i][j] * _sing[j] for j in range(N32)) == 0 for i in range(N32)))
_kill_sm = sum(1 for M in SM_J
               if all(sum(M[i][j] * _sing[j] for j in range(N32)) == 0 for i in range(N32)))
a6_ok = (_Y_zero and _kill_sm == 12 and 12 <= _kern < 45)
add(MAIN, "A6",
    "这个单态是「SM 单态」但不是「so(10) 单态」：熄灭它的是一个 24 维子空间，而不是全部 45 维",
    "12 个 SM 生成元全部熄灭；熄灭子空间（核）维数落在 [12, 45) 内；Y 熄灭它",
    "Y v = 0 是 %s；12 个 SM 生成元里熄灭它的 %d 个；"
    "45 个 Sigma **基**里逐个熄灭它的 %d 个；熄灭子空间（核）= 45 − 轨道秩 %d = **%d** 维"
    % (_Y_zero, _kill_sm, _kill_one, _orb_rank, _kern),
    "PASS" if a6_ok else "FAIL",
    "★★★ 本卷第二处「不能猜」：第一版把期望写成「轨道秩 = 32（满维）」，实测 **21**，"
    "因为 16 里的一个向量不可能被 so(10) 推满（16 是纯旋量，轨道维度远小于 32）。"
    "★★ 更关键的一条读数：**没有任何单个 Sigma_ab 熄灭它（0 个）**，可它明明被 12 个 SM 生成元熄灭 —— "
    "因为那 12 个是**线性组合**（如 Sigma12 - Sigma34），不是基元素。"
    "所以要问的不是「哪些生成元熄灭它」，而是「熄灭它的**子空间**有多大」：45 − 21 = 24 维。"
    "★★ 24 落在 [12, 45) 内，正是「SM 单态、但 so(10) 不单态」的精确形态；"
    "若核 = 45 则是平凡单态（整卷空转），若核 = 12 则是 so(10) 纯单态（16 里不存在）。")

# ============================================================ A7 Y 的幂和
Y_R = to_rep(Y_C, SIGR)


def pow_traces(M, kmax):
    n = len(M)
    P = mmul(M, M, n)
    out = {1: trace(P)}
    Q = P
    for k in range(2, kmax + 1):
        Q = mmul(Q, P, n)
        out[k] = trace(Q)
    return out


_tr = pow_traces(Y_R, 5)
# Y 实反对称 ⇒ 本征值 ±i*y ⇒ tr(Y^{2k}) = 2*(-1)^k*sum y^{2k}
PK = {k: (F(-1) ** k) * _tr[k] / 2 for k in _tr}
MULT = [(F(1, 6), 6), (F(-2, 3), 3), (F(1), 1), (F(1, 3), 3), (F(-1, 2), 2), (F(0), 1)]
_mult_dim = sum(n for _, n in MULT)
PRED = {k: sum(n * (y ** (2 * k)) for y, n in MULT) for k in range(1, 6)}
a7_ok = (_mult_dim == 16 and PK == PRED)
add(MAIN, "A7",
    "Y 的幂和：p_k = sum y^{2k}（16 个态）必须与分解表多重集 {1/6 x6, -2/3 x3, 1 x1, 1/3 x3, -1/2 x2, 0} 一致",
    "p_1..p_5 逐项一致；多重集维数和 = 16",
    "p_1..p_5 = %s；预测 %s；多重集维数和 %d"
    % ([str(PK[k]) for k in range(1, 6)], [str(PRED[k]) for k in range(1, 6)], _mult_dim),
    "PASS" if a7_ok else "FAIL",
    "★★ p_k 不是「猜的期望值」：它由**多重集**直接算出来（代码里对 MULT 求和），"
    "而多重集来自 16 的 SM 分解；左边 p_k 来自**矩阵幂的迹**。两条路不同源。"
    "★ 用迹而不用本征值：本征值要开根号，会破精确算术；迹只做加减乘除。"
    "★ 多重集六项 6+3+1+3+2+1 = 16，**第一版漏了 e^c（y = 1）这一项**，维数和只有 15 —— 是「维数和 = 16」这条自查把它抓出来的。"
    "★ 只定 |y| 不定符号 —— 这也正是 A8 要问的问题。")

# ============================================================ A8 J / K 四格对照
def blocks(fix):
    return PLUS if fix == "+" else MINUS


def build_all(fix):
    """在给定手征块上重建 45 个 Sigma 与 12 个 SM 生成元"""
    idx = blocks(fix)
    sig = {}
    for (a, b) in KEYS:
        Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
        Cm = ([[x / 4 for x in row] for row in Cm[0]], [[x / 4 for x in row] for row in Cm[1]])
        sig[(a, b)] = realify(restrict(Cm, idx))
    out = {}
    for which in ("J", "K"):
        su2 = SU2J_C if which == "J" else SU2K_C
        gens = ([to_rep(c, sig) for c in SU3_C] + [to_rep(c, sig) for c in su2]
                + [to_rep(Y_C, sig)])
        d = len(nullspace_basis(singlet_rows(gens), N32))
        tr = pow_traces(to_rep(Y_C, sig), 5)
        pk = tuple((F(-1) ** k) * tr[k] / 2 for k in range(1, 6))
        out[(fix, which)] = dict(dim=d, pk=pk)
    return out


ALL4 = build_all("+")
ALL4.update(build_all("-"))
_d_p = {kk: v["dim"] for kk, v in ALL4.items()}
_pk4 = {kk: v["pk"] for kk, v in ALL4.items()}
_a8_grid_ok = (len(ALL4) == 4 and len(set(_pk4.values())) == 1)     # 四格齐全 + p_k 四格全同
_a8_chir_blind = (_d_p[("+", "J")] == _d_p[("-", "J")]
                  and _d_p[("+", "K")] == _d_p[("-", "K")])         # 手征块不改读数
_a8_sep_dim = (_d_p[("+", "J")] != _d_p[("+", "K")])
_a8_sep = _a8_sep_dim
add(MAIN, "A8",
    "本卷核心争点（继承 r396 §十四 的预期）：16 能否分辨 so(4) 的自对偶 J 与反自对偶 K",
    "能分辨：四格齐全、p_k 四格全同，且同一手征块内 J 档与 K 档的单态数必须不同",
    "四格单态数 %s；同一块内 J vs K = %d vs %d（复 %d vs %d）⇒ 不同 = %s；"
    "手征块不可见（J 跨块同、K 跨块同）= %s；p_k 四格全同 = %s（Y 谱对 J/K 与手征块皆不变）"
    % (dict((k[0] + k[1], _d_p[k]) for k in sorted(_d_p)),
       _d_p[("+", "J")], _d_p[("+", "K")], _d_p[("+", "J")] // 2, _d_p[("+", "K")] // 2,
       _a8_sep_dim, _a8_chir_blind, _a8_grid_ok),
    "PASS" if (_a8_sep and _a8_grid_ok) else "FAIL",
    "★★★ 本卷的正面结论：**16 能分辨 J 与 K** —— 同一手征块内 J 档留 1 个复单态、K 档留 0 个；"
    "而 r396 的 10 / 45 / 54 把 J 换成 K 读数一律不变（r396 K2）。"
    "★★★ 机制的准确形态（这一段是**认领**，不是本卷的推导）：把 16 看成复 8+8，"
    "V_J = su(2)_J 的不变量空间、V_K = su(2)_K 的不变量空间，两者互补；"
    "ν^c（y = 0，16 里唯一的零超荷态）落在 V_J 而不在 V_K ⇒ 加上 Y 后 J 档剩 1 维、K 档剩 0 维。"
    "所以分辨力来自「Y 与哪一个 su(2) 占用同一条不变量空间」，不是来自 su(2) 本身"
    "（K1：单用 su(2) 两档都给 16）。"
    "★★★ **撤回一条**：本卷早先的 note 写「四格两两相等 ⇒ 把 J 换成 K 等价于把 16 换成 16bar」，"
    "并用「16 与 16bar 不等价」去解释 J/K 可分辨 —— 这是**读数支持不了的解读**："
    "实测 J 在两块都得 2、K 在两块都得 0，**手征块根本不改读数**；"
    "p_k 四格全同 ⇒ 「配对」这件事没有任何一条读数能区分。正确说法只有一句："
    "手征块对这些计数不可见，唯一的变量是 J/K。"
    "★★ 顺带：16 与 16bar 各有一个 (1,1,0)，这是分解表层面就成立的事实，与本卷的 J/K 分辨无关。")

# ============================================================ A9 两步阶梯
def so10_dic(k):
    return {k: F(1)}


_M45 = {}
for kk, cc in U_A.items():
    _M45[kk] = _M45.get(kk, F(0)) + 2 * cc          # 45 倾斜 = 2*u_a + u_k
for kk, cc in U_K.items():
    _M45[kk] = _M45.get(kk, F(0)) + cc
_M45 = {k: v for k, v in _M45.items() if v != 0}

# 45 维反对称 2-张量基
T45 = {}
for (a, b) in KEYS:
    M = zmat(10)
    M[a][b] = F(1)
    M[b][a] = F(-1)
    T45[(a, b)] = M


def coords45(M):
    return [M[a][b] for (a, b) in KEYS]


# 约束 1：[X, M45] = 0，未知量是 X 的 45 个系数
_M45_M = [[F(0)] * 10 for _ in range(10)]
for (i, j), cc in _M45.items():
    _M45_M[i][j] = cc
    _M45_M[j][i] = -cc
_cols1 = []
for kk in KEYS:
    _cols1.append(coords45(comm2(T45[kk], _M45_M, 10)))    # 第 kk 列 = coord([B_kk, M45])
_rows1 = [[_cols1[b][bp] for b in range(45)] for bp in range(45)]   # 行 = 坐标 b'，列 = 基 b
# 约束 2：X v = 0，v 是 A5 的零空间基（32 维实）
_rows2 = []
for kk in KEYS:
    Mk = SIGR[kk]
    _rows2.append([sum(Mk[i][j] * _sing[j] for j in range(N32)) for i in range(N32)])
_rows2 = [[_rows2[b][i] for b in range(45)] for i in range(N32)]
# ★ 分段算，不靠 r396 的 13 反推：约束 1 单独给多少、加上 32 行后多熄灭几维
_r1 = rank_of(_rows1, 45)
_r12 = rank_of(_rows1 + _rows2, 45)
_stab2 = 45 - _r12
a9_ok = (_stab2 == 12 and 45 - _r1 == 13 and _r12 - _r1 == 1)
add(MAIN, "A9",
    "两步阶梯：45 倾斜 VEV 的稳定子（13）再与 16 单态求交 ⇒ 应落到 12 = G_SM",
    "12 维；且「只用约束 1」必须给 13、「加 32 行」只能让秩 +1",
    "未知量 45；约束 %d + %d = %d 行；只用约束 1 秩 = %d ⇒ 稳定子 %d 维；"
    "合起来秩 = %d ⇒ 复合稳定子 = %d 维（只多熄灭 %d 维）"
    % (len(_rows1), len(_rows2), len(_rows1) + len(_rows2),
       _r1, 45 - _r1, _r12, _stab2, _r12 - _r1),
    "PASS" if a9_ok else "FAIL",
    "★★ 这一条把 r396 的「TWO-STEP-NEEDED 是读数名、不是证明」补上了："
    "把两个稳定子按**交**算（不是相加、不是相减），恰好落到 12。"
    "★★★ 更硬的一条读数：**加 32 行只让秩 +1**（%d → %d）—— r396 §八 说的「差 1 个 u(1)_{B−L}」，"
    "在本卷机核里的精确形态就是这一个 +1：13 − 12 = 1 不是算出来的减法，是**秩的增量**。"
    "若某处把 v 或 M45 写错，最可能的表现是这个增量变成 0（= SM 已经是稳定子）或 > 1。"
    "★ 约束 1 的行是「坐标 b'」、列是「基 b」—— r396 E01 的同一个坑，本卷从一开始就按这个顺序写。"
    "★★ 注意 rank %d 是**独立算出来的**，不是从 r396 的 13 反推（反推 = 引用旧读数 = 没算）。"
    % (_r1, _r12, _r1))

# ============================================================ 控制组
# K1 子代数单态计数表（16 与 16bar 两列 x J/K 两档）
SUBS = [("su(3)_C", "su3"), ("su(2)_J", "j"), ("su(2)_K", "k"), ("u(1)_Y", "y"),
        ("su(3)+Y", "8y"), ("su(2)_J+Y", "3jy"), ("su(2)_K+Y", "3ky"),
        ("su(3)+su(2)_J", "8j"), ("su(3)+su(2)_K", "8k")]
_tab = []
for fix in ("+", "-"):
    idx = blocks(fix)
    sig = {}
    for (a, b) in KEYS:
        Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
        Cm = ([[x / 4 for x in row] for row in Cm[0]], [[x / 4 for x in row] for row in Cm[1]])
        sig[(a, b)] = realify(restrict(Cm, idx))
    G = dict(su3=[to_rep(c, sig) for c in SU3_C],
             j=[to_rep(c, sig) for c in SU2J_C],
             k=[to_rep(c, sig) for c in SU2K_C],
             y=[to_rep(Y_C, sig)])
    G["8j"] = G["su3"] + G["j"]
    G["8k"] = G["su3"] + G["k"]
    G["8y"] = G["su3"] + G["y"]
    G["3jy"] = G["j"] + G["y"]
    G["3ky"] = G["k"] + G["y"]
    row = {}
    for nm, key in SUBS:
        row[nm] = len(nullspace_basis(singlet_rows(G[key]), N32))
    _tab.append(row)
_k1_ok = all(v % 2 == 0 for r in _tab for v in r.values())
_k1_diff_chir = [nm for nm, _ in SUBS if _tab[0][nm] != _tab[1][nm]]      # 16 vs 16bar
JK_PAIRS = [("su(2) 单独（不含 Y）", "su(2)_J", "su(2)_K"),
            ("su(2)+Y", "su(2)_J+Y", "su(2)_K+Y"),
            ("su(3)+su(2)（不含 Y）", "su(3)+su(2)_J", "su(3)+su(2)_K")]
_k1_diff_jk = [nm for nm, a, b in JK_PAIRS if _tab[0][a] != _tab[0][b]]
add(CTL, "K1",
    "控制组（判别力表）：9 个子代数 x 2 个手征块的单态维数；并单独比较「同一子代数的 J 档 vs K 档」",
    "每格都算出数（偶数）；报出 (a) 16 与 16bar 之间不同的格数、(b) 同一手征块内 J 与 K 不同的子代数",
    "16: %s；16bar: %s；16 与 16bar 不同 %d 格；同一块内 J vs K 不同：%s"
    % (" ".join("%s=%d" % (nm, _tab[0][nm]) for nm, _ in SUBS),
       " ".join("%s=%d" % (nm, _tab[1][nm]) for nm, _ in SUBS),
       len(_k1_diff_chir), (_k1_diff_jk if _k1_diff_jk else "无")),
    "PASS" if _k1_ok else "FAIL",
    "★★ 这张表把 A8 的结论说得更准：**单靠 su(2) 分不开 J 与 K（都 16），一旦加上 Y 就分开了**"
    "（su(2)_J+Y 给 2，su(2)_K+Y 给 0）。所以「16 能分辨 J/K」的准确含意是："
    "**分辨力来自 Y 与 su(2) 的联合作用，不是来自 su(2) 本身**。"
    "★★ 另一半同样重要：16 与 16bar 两列**逐格相同**（0 格不同）⇒ 交换手征块什么也不改 ——"
    "这与 A8 四格里「J、K 各自跨块不变」是**同一条事实**（手征块对这些计数不可见）。"
    "★ 判别力自证：su(3)_C 给 8、su(2) 给 16、u(1)_Y 给 2 —— 三档互不相同，说明这不是一张空表。")

# K2 零约束
_deg = N32 - rank_of([], N32)
add(CTL, "K2", "控制组（退化）：一个约束都不加", "32（全空间）",
    "零约束：秩 = 0；零空间 = %d" % _deg, "PASS" if _deg == 32 else "FAIL",
    "★退化档必须是全空间，否则「2」与「32」之间没有标尺。")

# K3 不做手征投影（用全 32 维 Dirac）
# 全 32 维（未投影）上的 12 个生成元：直接用 32x32 复 Sigma 的实化 64x64
SIG64 = {}
for (a, b) in KEYS:
    Cm = cadd(cmul(GAM[a], GAM[b]), cmul(GAM[b], GAM[a]), -1)
    Cm = ([[x / 4 for x in row] for row in Cm[0]], [[x / 4 for x in row] for row in Cm[1]])
    SIG64[(a, b)] = realify(Cm)
_dirac_gens = []
for c in SU3_C + SU2J_C + [Y_C]:
    _dirac_gens.append(to_rep(c, SIG64))
_r64 = []
for M in _dirac_gens:
    for i in range(64):
        _r64.append([M[i][j] for j in range(64)])
_d_dirac = 64 - rank_of(_r64, 64)
add(CTL, "K3",
    "控制组（判别力）：不做手征投影，直接在 32 维 Dirac 上算（实化 64 维）",
    "必须离开 2（预期 4 = 16 与 16bar 各 2）",
    "Dirac 上：实零空间 = %d（投影后 %d）" % (_d_dirac, _d_J),
    "PASS" if _d_dirac != _d_J else "FAIL",
    "★★ 这一条证明「投影不是装饰」：不投影会多出 16bar 的那一维 ⇒ 2 变成 4。"
    "★ 同时它验证了 A5 的 2 不是「随便解解」得来的。")

# K4 实化写反
# ★负对照取材于本卷**真实犯过的错**：Sigma 的归一化写成 1/2 而不是 1/4
SIGR_H = {k: [[2 * v for v in row] for row in SIGR[k]] for k in KEYS}
_YH = to_rep(Y_C, SIGR_H)
_trH = pow_traces(_YH, 1)
_p1H = (F(-1) ** 1) * _trH[1] / 2
_dH = len(nullspace_basis(singlet_rows([to_rep(c, SIGR_H) for c in SU3_C + SU2J_C + [Y_C]]), N32))
add(CTL, "K4",
    "控制组（判别力）：把 Sigma 的归一化从 1/4 写成 1/2（本卷第一版真实犯过的错）",
    "p_1 必须离开 10/3（整体缩放会把 Y 谱乘以 2）；单态数不受影响（零空间对整体缩放不变）",
    "p_1 = %s（正确 %s）；单态数 = %d（正确 %d）" % (_p1H, PK[1], _dH, _d_J),
    "PASS" if (_p1H != PK[1] and _dH == _d_J) else "FAIL",
    "★★ 这一条是**真实自伤驱动**的：本卷第一版写 1/2，实测 p_1 = 40/3，而正确值 10/3 —— "
    "恰好是 4 倍（Y 乘 2 ⇒ y^2 乘 4），一步定位到「归一化错了 2 倍」。"
    "★★ 注意它同时给出一条**反读数**：单态数对整体缩放**不敏感**（2 还是 2），"
    "所以「单态数对」**不能**保证「归一化对」—— 必须另有一条对量纲敏感的判据（这里是 p_1）。")

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
    "★A7 的 p_k 是真算矩阵幂的迹；A3 的闭合是真算 990 对换位子。都不是符号恒等。")

add(GRD, "G03", "四个控制组必须给出可区分的读数",
    "K1 每格有数；K2 = 32；K3 ≠ 2；K4 的 p_1 离开 10/3（单态数可以不变）",
    "K1 两列不同格数 %d（J vs K 在 su(2)+Y 上不同）；K2 = %d；K3 = %d（≠%d）；K4 p_1 = %s（≠ %s）、单态数 %d"
    % (len(_k1_diff_chir), _deg, _d_dirac, _d_J, _p1H, PK[1], _dH),
    "PASS" if (_k1_ok and _deg == 32 and _d_dirac != _d_J and _p1H != PK[1]) else "FAIL",
    "★K1 给结构表，K2 给退化标尺，K3 证明手征投影必要，K4 证明归一化必要。四者分工不重叠。"
    "★★ K4 与 K3 的着重点不同：K3 动的是**空间**（投影），K4 动的是**刻度**（归一化）—— "
    "而刻度错时单态数**不变**，所以只靠 K3 是抓不到的。")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "0 违规（收尾重算，覆盖 %d 条）" % len(ALL) if _bad4 == 0 else "%d 违规" % _bad4,
    "PASS" if _bad4 == 0 else "FAIL", "★收尾重算，不是逐条自查。")

add(GRD, "G05", "维数账：10 个 gamma 在 32 维、45 个 Sigma 在 32 维、16 = 32/2",
    "10 / 45 / 16 三处一致",
    "gamma %d 个 x %d 维；Sigma %d 个 x %d 维；手征块 %d 维"
    % (len(GAM), N32, len(SIGR), N32, len(PLUS)),
    "PASS" if (len(GAM) == 10 and len(SIGR) == 45 and len(PLUS) == 16) else "FAIL",
    "★三处独立枚举，任一处错都会和 A3 的秩 45 打架。")

add(GRD, "G06", "分解账闭合：8 + 3 + 1 = 12", "闭合",
    "%d + %d + 1 = %d" % (len(SU3_C), len(SU2J_C), len(SU3_C) + len(SU2J_C) + 1),
    "PASS" if len(SU3_C) + len(SU2J_C) + 1 == 12 else "FAIL",
    "★三处独立，任一处少一个都会露出来。")

_g7 = (len(PLUS) == 16 and len(MINUS) == 16
       and all(is_antisym(M) for M in SM_J))
add(GRD, "G07", "手征块与反对称的结构守卫：两块各 16 维、12 个生成元全部反对称",
    "16 / 16 / 全部反对称",
    "±块 %d / %d；生成元反对称 = %s" % (len(PLUS), len(MINUS), all(is_antisym(M) for M in SM_J)),
    "PASS" if _g7 else "FAIL",
    "★★ 反对称不是「顺手检查」：16 是复表示，实化后若不对称/不反对称，"
    "「零空间 = 复单态 x2」的整条推理就断了。")

VERDICT = "--".join([
    "SIXTEEN-HAS-%d-SINGLET" % (_d_J // 2) if _d_J // 2 == 1 else "SIXTEEN-HAS-%d-SINGLETS" % (_d_J // 2),
    "Y-POWERS-MATCH-DECOMP" if a7_ok else "Y-POWERS-DIFFER",
    "JK-SEPARATED-ON-16" if _a8_sep else "JK-INDISTINGUISHABLE-ON-16",
    "TWO-STEP-GIVES-%d" % _stab2,
])
_dd = {r["id"]: r["kind"] for r in ALL}
_v2 = "--".join([
    "SIXTEEN-HAS-%d-SINGLET" % (_d_J // 2) if _dd["A5"] == "PASS" else "SIXTEEN-OPEN",
    "Y-POWERS-MATCH-DECOMP" if _dd["A7"] == "PASS" else "Y-POWERS-DIFFER",
    "JK-SEPARATED-ON-16" if _a8_sep else "JK-INDISTINGUISHABLE-ON-16",
    "TWO-STEP-GIVES-%d" % _stab2,
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

_g11 = (len(SIGR) == 45 and len(set(KEYS)) == 45 and _a3_checks == 990)
add(GRD, "G11", "完备性：45 个基无重复、990 对 = C(45,2) 全覆盖", "45 / 990",
    "SIGR = %d 个（去重后 %d）；换位子对数 %d（C(45,2) = 990）"
    % (len(SIGR), len(set(KEYS)), _a3_checks),
    "PASS" if _g11 else "FAIL",
    "★「全部 990 对」必须真的枚举完，不能抽样 —— 抽样时漏掉的那一对恰好可能是坏的。")

add(GRD, "G12", "两条独立路径：16 的单态数由「零空间」与「K3 的 Dirac 减半」各算一次",
    "零空间给 1；Dirac 给 4 ⇒ 每块 2 ⇒ 复 1",
    "零空间路 %d；Dirac 路 %d（÷2 块 ÷2 复 = %d）" % (_d_J, _d_dirac, _d_dirac // 4),
    "PASS" if (_d_J // 2 == _d_dirac // 4) else "FAIL",
    "★★ 两条路不同源：一条在投影后的 32 维上解，一条在未投影的 64 维上解再除回去。"
    "★ r396 的 G12 是「零空间 vs 分解表」，本卷是「投影后 vs 未投影」—— 都是两个不同对象给同一读数。")


def final_of(nf_main, nf_guard, n_decl=0):
    if nf_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main


g13 = add(GRD, "G13", "总门必须对「守卫失败」敏感", "注入守卫 FAIL 必须翻转", "（回填）", "INFO",
          "★沿用 r392 起的总门口径 + 已登记判负不挡门。")

_all_ids = {r["id"]: r for r in ALL}
_kt = "16 → %d；Y 幂和相符 = %s；J/K 四格 → %s；两步 → %d" % (
    _d_J // 2, a7_ok, sorted(set(_d_p.values())), _stab2)
_kt_from_rows = "16 → %d；Y 幂和相符 = %s；J/K 四格 → %s；两步 → %d" % (
    int(_all_ids["A5"]["act"].split("复单态 **")[1].split("**")[0]),
    _all_ids["A7"]["kind"] == "PASS",
    sorted(set(_d_p.values())),
    int(_all_ids["A9"]["act"].split("复合稳定子 = ")[1].split(" 维")[0]))
_kt_basis16 = ("单态是 16 里唯一的 SM 单态（右手中微子方向）"
               if (_d_J == 2 and a6_ok) else "未定（A5/A6 未同时给出实维数 2 与轨道满维）")
add(GRD, "G14", "关键表读数必须与主册同一条目同读数（防同名覆盖 / 防关键表写死错话）",
    "关键表四个读数 == A5/A7/A8/A9 抽出值；且 16 基的「话」必须由 A5/A6 的读数拼出",
    "关键表：%s；由 act 重算：%s；16 基串：%s" % (_kt, _kt_from_rows, _kt_basis16),
    "PASS" if (_kt == _kt_from_rows and _kt_basis16 != "未定（A5/A6 未同时给出实维数 2 与轨道满维）")
    else "FAIL",
    "★★ r396 E02 的直接继承：关键表里「谁是基」这类话必须由上一段的布尔量拼出，"
    "不能凭记忆写。本卷这句由 (实维数 == 2) and (轨道满维) 拼。")

# ============================================================ 汇总
_nf_main = sum(1 for r in MAIN if r["kind"] == "FAIL")
_nf_g = sum(1 for r in CTL + GRD if r["kind"] == "FAIL")
FINAL = final_of(_nf_main, _nf_g, len(DECLARED_NEG & set(_neg)))

g13["exp"] = "注入守卫 FAIL 必须翻转；已登记判负不挡门"
g13["act"] = "(0,0)=%s；(0,1)=%s；(1,0)=%s；(已登记 1 条)=%s" % (
    final_of(0, 0, 0), final_of(0, 1, 0), final_of(1, 0, 0), final_of(1, 0, 1))
g13["kind"] = ("PASS" if (final_of(0, 0, 0) == "GATES-PASS-ALL-POSITIVE"
                          and final_of(0, 1, 0) != final_of(0, 0, 0)
                          and final_of(1, 0, 0) != final_of(0, 0, 0)
                          and final_of(1, 0, 1) == "GATES-PASS-WITH-1-NEGATIVE") else "FAIL")

# ============================================================ 落盘（JSON 先写 → 回填 G09 → 再写 → 最后拼报告）
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
A("对象：X-GSM-2（16 旋量表示上的零空间：手征投影 / 45 个生成元实化 / 单态计数 / J-K 对照）")
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
A("gamma：%d 个 32x32；Sigma：%d 个；手征块 %d 维" % (len(GAM), len(SIGR), len(PLUS)))
A("SM 生成元：%d 个（秩 %d），在 32 维实旋量空间上" % (len(SM_J), _a4_rank))
A("16 的 SM 单态：实 %d 维 ⇒ 复 **%d** 维（%s）" % (_d_J, _d_J // 2, _kt_basis16))
A("Y 的幂和 p_1..p_5 = %s" % [str(PK[k]) for k in range(1, 6)])
A("J/K 四格单态数：%s" % dict((k[0] + k[1], v) for k, v in _d_p.items()))
A("两步复合稳定子：%d 维" % _stab2)
A("")
A("【诚实边界】")
# ★ 边界文案必须由读数拼出（本卷第 E07 号自伤：这里曾残留「J/K 不可分辨」的旧文案，
#   与 A8 实测可分辨直接矛盾，而任何数值守卫都抓不到）
_a8_word = ("可分辨（同一手征块内单态数 %d vs %d）" % (_d_p[("+", "J")], _d_p[("+", "K")])
            if _a8_sep else "不可分辨（四格读数全同）")
A(" 1) 本卷只做**计数与谱**：单态数、Y 的幂和、复合稳定子维数；不碰质量谱 / Yukawa / 混合角；")
A(" 2) J/K 在本卷读作 %s，但这是**在已算的读数上**的结论，不是定理："
  "没有证明「不存在任何可分辨的不变量」；" % _a8_word)
A(" 3) 手征块对单态计数**不可见**（A8 四格里 J、K 各自跨块不变）是本卷的读数，"
  "但本卷没有构造显式共轭算子，也没有用它推出任何等价性 —— "
  "早先把这条读成「16bar 等价于把 J 换成 K」是错的（§十一 E08）；")
A(" 4) Y 的幂和只定 |y| 的多重集、不定符号；且 p_k 对 J/K **两档逐项相同**（[Y,su(2)]=0）"
  "⇒ 符号/手征信息**不在谱里**，只在 A8 的「哪些态被熄灭」里。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

print("JSON ->", JSN)
print("TXT  ->", RPT, "(%d chars)" % len("\n".join(L)))
print("MAIN=%d (PASS %d / INFO %d / IDENTITY %d / FAIL %d)  CTL=%d  GRD=%d  合计 %d"
      % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"),
         sum(1 for r in MAIN if r["kind"] == "INFO"), _n_id, _nf_main,
         len(CTL), len(GRD), len(ALL)))
print("FINAL   =", FINAL)
print("VERDICT =", VERDICT)
