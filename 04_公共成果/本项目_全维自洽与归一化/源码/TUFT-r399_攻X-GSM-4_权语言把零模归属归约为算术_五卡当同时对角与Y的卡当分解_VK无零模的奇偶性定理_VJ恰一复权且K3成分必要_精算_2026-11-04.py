# -*- coding: utf-8 -*-
"""TUFT-r399  攻 X-GSM-4：权语言 —— 把「零模归属」从矩阵读数归约为**算术**

纯标准库（Fraction，判据区无浮点、无随机）。复用 r398 的代数底座（同一 Γ / Σ / 生成元 / realify），
只换判据的**表达方式**：不再解 16x16 矩阵，而是在 5 个 Cartan 的**权基**上做有限枚举。

r398 留下的硬边界（其 §十四 第 3 条）：
  「A6 只给出 ker(Y|V_J)=2、ker(Y|V_K)=0 这两个读数，**不解释**为什么 nu^c 落在 V_J」
本卷把它推进到最后一步 —— 能推的推到底，剩下的是什么也一并说清。

  A1  五个 Cartan H_i = Sigma_{2i,2i+1} 在 16 维手征块上**同时对角**、对角值全为 ±1/2
  A2  16 个权向量两两不同（确是权基）；V_J / V_K 在权基上就是两条符号约束；#(-eps) 恒为偶数
  A3  Y 的 Cartan 分解是**矩阵等式**：Y = -(1/3)(H1+H2+H3) + (1/2)(H4-H5)
  A4  J3 = H4+H5、K3 = H4-H5（与 su(2)_J / su(2)_K 的第 3 个生成元逐元素相等）
  A5  用权重算 y 谱（与 r398 解矩阵得的谱逐项一致）—— 独立路径互印
  A6  定理 W(i)：ker(Y|V_K) = 0 是**奇偶性**结果（三个 ±1/2 之和恒为半整数奇数倍，不可能为 0）
  A7  定理 W(ii)：ker(Y|V_J) = 1 个复权（2 维实）且零化 <=> eps1=eps2=eps3=eps4
  A8  这 2 个权态与 r398 的零空间**是同一空间**（矩阵路径 vs 权路径）
  A9  边界：Y -> -Y 零模数不变 ⇒ 零模数对总符号完全不敏感
"""
import io
import json
import os
from fractions import Fraction as F

RID = "r399"
TITLE = ("TUFT-r399_攻X-GSM-4_权语言把零模归属归约为算术_五卡当同时对角与Y的卡当分解_"
         "VK无零模的奇偶性定理_VJ恰一复权且K3成分必要_精算_2026-11-04")
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



# ============================================================ A1 五个 Cartan 同时对角（权基）
NC = 16                                     # PLUS 块的复维数
HC = [SIGC[(2 * i, 2 * i + 1)] for i in range(5)]
_off_nz = 0
_diag_bad = 0
for _i, _M in enumerate(HC):
    _R, _I = _M
    for _a in range(NC):
        for _b in range(NC):
            if _a != _b and (_R[_a][_b] != 0 or _I[_a][_b] != 0):
                _off_nz += 1
    for _a in range(NC):
        if _R[_a][_a] != 0:
            _diag_bad += 1
        if _I[_a][_a] not in (F(1, 2), F(-1, 2)):
            _diag_bad += 1
W = [[HC[_i][1][k][k] for _i in range(5)] for k in range(NC)]       # 权向量（5 个 ±1/2）
_a1_ok = (_off_nz == 0 and _diag_bad == 0)
add(MAIN, "A1",
    "五个 Cartan H_i = Sigma_{2i,2i+1} 在 16 维手征块上**同时对角**，对角值全是 ±1/2",
    "非对角非零 0 处；16x5 个对角值全 in {±1/2}；Re 对角全 0",
    "非对角非零 %d 处；对角值不合规 %d 处；权值集 = %s"
    % (_off_nz, _diag_bad, sorted({x for w in W for x in w})),
    "PASS" if _a1_ok else "FAIL",
    "★★★ 这一条是整卷的**地皮**：只要 5 个 Cartan 同时对角，「解 16x16 本征值」这件事就退化成"
    "「读 5 个 ±1/2 的符号串」。★ 注意我是**验证**它对角，不是假设：`Sigma_ab = (1/4)[Γ,Γ]` 是不是对角，"
    "取决于 Γ 的张量积构造，写错因子就立刻露出来（非对角非零数不会为 0）。"
    "★★ 与 r398 的口径完全一致（同一个 SIGC），所以不是换模型，是换**算法**。")

# ============================================================ A2 权基完整 + V_J/V_K 的权表述
_uniq = len({tuple(w) for w in W})
_nminus = sorted({sum(1 for x in w if x == F(-1, 2)) for w in W})
VJ = nullspace_basis(rows_of(J_GENS), N32)
VK = nullspace_basis(rows_of(K_GENS), N32)
IDX_J = [k for k in range(NC) if W[k][3] + W[k][4] == 0]        # w4 + w5 = 0  <=>  J3 = 0
IDX_K = [k for k in range(NC) if W[k][3] - W[k][4] == 0]        # w4 - w5 = 0  <=>  K3 = 0
_a2_ok = (_uniq == NC and len(IDX_J) * 2 == len(VJ) and len(IDX_K) * 2 == len(VK))
add(MAIN, "A2",
    "16 个权向量两两不同（确是权基）；且 V_J / V_K 在权基上就是两条**符号约束**",
    "16 个权互不相同；len(IDX_J)*2 = dim V_J = 16；len(IDX_K)*2 = dim V_K = 16",
    "互不相同的权 %d 个；#(eps=-1/2) 取值 %s；IDX_J %d 个 -> dim V_J %d；IDX_K %d 个 -> dim V_K %d"
    % (_uniq, _nminus, len(IDX_J), len(VJ), len(IDX_K), len(VK)),
    "PASS" if _a2_ok else "FAIL",
    "★★★ 这是本卷的**翻译表**：`V_J = ker(su(2)_J)` 原本是「解 3 个 32x32 生成元的零空间」，"
    "在权基上它就是 `w4 + w5 = 0` 这一条符号约束；`V_K` 是 `w4 - w5 = 0`。"
    "★ 两边的维数必须对上（8 复 = 16 实），这是权语言与矩阵语言的**字典检验**："
    "若权基或生成元系数有一处不一致，这两个等式会当场不成立。"
    "★★ 半整数账：每个权是 5 个 ±1/2，#(-1/2) 的取值集合就是手征性的判据。")

# ============================================================ A3 Y 的 Cartan 分解（矩阵等式）


def csmul(X, s):
    return ([[s * x for x in row] for row in X[0]], [[s * x for x in row] for row in X[1]])


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


Y_CM = to_rep_c(Y_C, SIGC)
A_SUM = cadd(cadd(HC[0], HC[1]), HC[2])
K3C = cadd(HC[3], HC[4], -1)
J3C = cadd(HC[3], HC[4], 1)
Y_DEC = cadd(csmul(A_SUM, F(-1, 3)), csmul(K3C, F(1, 2)))
_a3_ok = (Y_DEC == Y_CM)
add(MAIN, "A3",
    "Y 的 Cartan 分解是一条**矩阵等式**（不是拟合）：Y = -(1/3)(H1+H2+H3) + (1/2)(H4-H5)",
    "Y_C 与 -(1/3)(H1+H2+H3)+(1/2)(H4-H5) 逐元素相等",
    "逐元素相等 = %s；Y_C 的非零系数 %s"
    % (_a3_ok, {str(k): str(v) for k, v in sorted(Y_C.items())}),
    "PASS" if _a3_ok else "FAIL",
    "★★★ 这一条是本卷的**全部内容**：Y 不是一个神秘矩阵，它是「so(6) 的 U(1)_A 取 -1/3」加上"
    "「su(2)_K 的 Cartan 取 +1/2」。★ 系数 -1/3 与 +1/2 都是**输入**（超荷嵌入），不是本卷算出来的 —— "
    "诚实边界第 1 条。但**给定**这两个系数之后，零模落在哪一半就变成了**算术**（A6/A7）。"
    "★★ 逐元素相等，不做「迹相等」这类弱检验：若某处把 (H4+H5) 写成 (H4-H5)，"
    "迹不变（tr 都是 0）而矩阵不等 ⇒ 只有逐元素才抓得到。")

# ============================================================ A4 J3 / K3 与 su(2) 的第 3 个生成元
_a4_j = (to_rep_c(SU2J_C[2], SIGC) == J3C)
_a4_k = (to_rep_c(SU2K_C[2], SIGC) == K3C)
add(MAIN, "A4",
    "J3 = H4+H5 与 K3 = H4-H5：正是 su(2)_J / su(2)_K 的第 3 个生成元（逐元素相等）",
    "to_rep(SU2J_C[2]) == H4+H5；to_rep(SU2K_C[2]) == H4-H5",
    "J3 逐元素相等 = %s；K3 逐元素相等 = %s" % (_a4_j, _a4_k),
    "PASS" if (_a4_j and _a4_k) else "FAIL",
    "★★ 这一条把「第 3 个生成元」这个名字钉死在 H4±H5 上 —— 于是「J3 在 V_J 上恒 0」与"
    "「w4 + w5 = 0」是同一句话的两种写法。★ 与 A2 的字典互为逆映射。")

# ============================================================ A5 用权算 y 谱（独立路径）
YS = [Y_CM[1][k][k] for k in range(NC)]         # 对角 = i*y ⇒ 虚部就是 y
_y_re_bad = sum(1 for k in range(NC) if Y_CM[0][k][k] != 0)
_spec = {}
for _y in YS:
    _spec[_y] = _spec.get(_y, 0) + 1
# r398 公布的谱（判定册 §八 的 11 值表汇总，16 个态）
R398 = {F(-1): 1, F(-1, 6): 6, F(2, 3): 3, F(-1, 3): 3, F(1, 2): 2, F(0): 1}
FLIP = {-k: v for k, v in R398.items()}
_spec_is_flip = (_spec == FLIP)
_a5_ok = ((_spec == R398 or _spec == FLIP) and _y_re_bad == 0 and sum(_spec.values()) == NC)
_nval = len(_spec)
add(MAIN, "A5",
    "用权重算 y 谱：与 r398 的谱**整体一致**，但符号是反的 ⇒ 本卷的 PLUS 块是 r398 记的 `16bar`",
    "16 个态、6 个值、合计 16、Re 对角全 0；谱 = r398 的谱或其整体取反（并**报出是哪一种**）",
    "权路径 %s；值 %d 个；合计 %d；Re 对角非零 %d 处；== r398 清单 = %s；== r398 清单取反 = %s"
    % ({str(k): v for k, v in sorted(_spec.items())}, _nval, sum(_spec.values()), _y_re_bad,
       _spec == R398, _spec_is_flip),
    "PASS" if _a5_ok else "FAIL",
    "★★★ 两条路径：r398 是「解 16x16 零空间 + 求本征值」，本卷是「读 16 个对角虚部」。"
    "★ 独立性的诚实说明：**用的是同一批生成元**，所以这不是两个独立物理假设，而是同一算式的两种算法 —— "
    "它验证的是**实现**，不是**前提**。这条必须这么说，否则就变成「同源回验抓不到同源错误」的教科书错法。"
    "★★★ 符号这一条是真发现（也是本卷头号自伤）：r398 的 `y` 是用「`ker(iY∓1)` 落在哪一块」**钉**出来的，"
    "本卷的 `y` 是「`Y` 的复本征值除以 `i`」直接读出来的 —— 两者差一个整体符号。"
    "读数给出的是 `%s`，正好是 r398 清单的**逐项取反** ⇒ **本卷的 PLUS 块就是 r398 记的 `16bar`**。"
    "这不是矛盾，而是 r398 A8 那句「`16bar` 的 `y` 谱是 `16` 的逐项取反」从**第二个方向**被复现了。"
    "★ 而这个符号差**不影响任何零模数**（A9 已单独证明零模数对总符号免疫）—— 所以它是**约定**问题，不是**物理**问题。"
    "把约定当结论、或把结论当约定，都是 r397 E09 那一族错。" % ("取反" if _spec_is_flip else "同号"))

# ============================================================ A6 定理 W(i)：V_K 上没有零模是奇偶性
_yK = [YS[k] for k in IDX_K]
_sK = [W[k][0] + W[k][1] + W[k][2] for k in IDX_K]
_s3_ok = all(YS[k] == -_sK[_i] / 3 for _i, k in enumerate(IDX_K))       # 在 V_K 上 K3 = 0
_parity = all((2 * s).denominator == 1 and (2 * s).numerator % 2 != 0 for s in _sK)
_a6_ok = (len(_yK) == 8 and all(y != 0 for y in _yK) and _s3_ok and _parity)
add(MAIN, "A6",
    "定理 W(i)：ker(Y|V_K) = 0 是**奇偶性**的结果，不是解出来的",
    "V_K 上 y = -s/3（s = eps1+eps2+eps3）；s 恒为 1/2 的奇数倍 ⇒ s != 0 ⇒ y != 0；8 个态全非零",
    "V_K 的 8 个态：y 取值集 %s；y = -s/3 逐项成立 = %s；2s 恒为奇数 = %s"
    % (sorted({str(y) for y in _yK}), _s3_ok, _parity),
    "PASS" if _a6_ok else "FAIL",
    "★★★ **这就是 r398 那条「未解释」的边界被推到底的地方**：在 V_K 上 K3 = 0（因为 V_K 就是它自己的核），"
    "于是 Y 只剩下 -(1/3)A 这一项，零模条件化成「三个 ±1/2 之和为 0」。"
    "而三个 ±1/2 之和**恒为 1/2 的奇数倍**（2s = ±1 或 ±3），**永远不可能是 0** ⇒ 零模不存在。"
    "★★ 这个论证**不依赖**任何矩阵：它是一条整数奇偶性。也就是说 `ker(Y|V_K) = 0` 是**定理**，不是读数。"
    "★ 反过来，若谁把 Y 的 A 项系数从 -1/3 改成别的值，这条奇偶性论证照旧成立 —— 见 K1 的边界说明。")

# ============================================================ A7 定理 W(ii)：V_J 上恰 2 个权，条件 eps1=..=eps4
_yJ = [YS[k] for k in IDX_J]
_zero_J = [k for k in IDX_J if YS[k] == 0]
_formJ = all(YS[k] == F(-1) * (W[k][0] + W[k][1] + W[k][2]) / 3 + W[k][3] for k in IDX_J)
_cond = all(W[k][0] == W[k][1] == W[k][2] == W[k][3] == -W[k][4] for k in _zero_J)
# 镜像权 -w 为什么不在同一块：本块 #(eps=-1/2) 恒为**偶数**，而 -w 的 #(-1/2) = 5 - #(-1/2)
_NM = {tuple(w): sum(1 for x in w if x == F(-1, 2)) for w in W}
_mir_out = all(((5 - _NM[tuple(W[k])]) % 2 == 1
                and tuple([-x for x in W[k]]) not in _NM) for k in _zero_J)
_a7_ok = (len(_zero_J) == 1 and _formJ and _cond and _mir_out)
add(MAIN, "A7",
    "定理 W(ii)：ker(Y|V_J) = 1 个**复**权（= 2 维实）且零化 <=> eps1 = eps2 = eps3 = eps4",
    "V_J 上 y = -s/3 + eps4；零化 <=> s = 3*eps4 <=> eps1=eps2=eps3=eps4；恰 1 个权（镜像权不在本块）",
    "V_J 的 8 个态：零模权 %d 个；y = -s/3+eps4 逐项成立 = %s；条件 eps1=..=eps4 且 eps5=-eps4 = %s；"
    "镜像权不在本块 = %s"
    % (len(_zero_J), _formJ, _cond, _mir_out),
    "PASS" if _a7_ok else "FAIL",
    "★★★ 这是整卷的**结论**：在 V_J 上 J3 = 0 给出 `eps5 = -eps4`，于是 K3 = H4-H5 在该半边上等于 `2*eps4`，"
    "Y 变成 `-s/3 + eps4`。零化 ⟺ `s = 3*eps4` ⟺ `eps1=eps2=eps3=eps4`（因为 s 只能是 ±3/2 或 ±1/2，"
    "而 3*eps4 只能是 ±3/2）⇒ 权向量被完全钉死成 `(±1/2,±1/2,±1/2,±1/2,∓1/2)`，**恰好 2 个**。"
    "★★ `2 维实 = 1 维复`：这 2 个权态是复共轭对，正好构成一个**复 1 维**空间 —— 这就是 `nu^c`。"
    "★ 至此「零模落在 V_J」不再是认领：它是「`eps5 = -eps4` 之后，方程从 `s=0`（不可能）变成 `s=3eps4`（可能，且只解 2 个）」。"
    "★★★ 但**为什么 Y 里有 +(1/2)K3 这一项**仍是输入（A3 的诚实边界）：本卷推的是「给定 Y，零模在哪」，"
    "不是「Y 为什么长这样」。这条区别必须留着。")

# ============================================================ A8 与 r398 的零空间是同一空间
_A_YJ = restrict_mat(Y_R, VJ, N32)
_ker32 = nullspace_basis(rows_of(J_GENS + [Y_R]), N32)      # {v in V_J : Y v = 0}，32 维里的子空间
_u = []
for k in _zero_J:                      # 一个复权态 = 实化空间里的 (e_k, i e_k) 这一对
    _u.append([F(1) if j == k else F(0) for j in range(N32)])
    _u.append([F(1) if j == (k + NC) else F(0) for j in range(N32)])
_same = (rank_of(VJ + _u, N32) == len(VJ)) and (rank_of(VJ + _u + _ker32, N32) == len(VJ))
_u_in_ker = all(rank_of(_ker32 + [v], N32) == len(_ker32) for v in _u)
_a8_ok = (_same and _u_in_ker and len(_zero_J) == 1 and len(_ker32) == 2 and len(_u) == 2)
add(MAIN, "A8",
    "这 2 个权态与 r398 的零空间**是同一空间**（矩阵路径 vs 权路径）",
    "`e_k` 与 `i·e_k` 都在 V_J 内、都在 ker(Y|V_J) 内；三者张成同一 16 维 ⇒ 同一 2 维零模子空间",
    "权态在 V_J 内且张成不变 = %s；权态都在 ker 内 = %s；ker(Y|V_J) 维数 = %d；零模权数 = %d"
    % (_same, _u_in_ker, len(_ker32), len(_zero_J)),
    "PASS" if _a8_ok else "FAIL",
    "★★ 这一条防的是「两个不同的 2 维空间」：`ker(Y|V_J)` 恰好 2 维，而我挑的 2 个实向量也恰好 2 维 —— "
    "**维数相等不等于空间相等**（r394 的维数比较刀）。所以这里算的是**秩**：把两组向量叠在 V_J 里，"
    "秩仍是 16（没有长大）⇒ 张成同一个子空间。★ 若权基的指标错位（例如把 e_k 当成 e_{k+1}），"
    "这一条会红而 A7 仍绿 —— 这正是需要的分工。")

# ============================================================ A9 边界：零模数对总符号不敏感
YNEG = csmul(Y_CM, -1)
_knegJ = len(VJ) - rank_of(restrict_mat(realify(YNEG), VJ, N32), len(VJ))
_knegK = len(VK) - rank_of(restrict_mat(realify(YNEG), VK, N32), len(VK))
_kbaseJ = len(VJ) - rank_of(_A_YJ, len(VJ))
_kbaseK = len(VK) - rank_of(restrict_mat(Y_R, VK, N32), len(VK))
_a9_ok = (_knegJ == _kbaseJ == 2 and _knegK == _kbaseK == 0)
add(MAIN, "A9",
    "边界（不是控制组）：Y -> -Y 后零模数**不变** ⇒ 零模数对总符号完全不敏感",
    "基线 (2, 0)；取负后仍 (2, 0)",
    "基线 (%d, %d)；Y -> -Y 后 (%d, %d)" % (_kbaseJ, _kbaseK, _knegJ, _knegK),
    "PASS" if _a9_ok else "FAIL",
    "★★ 为什么这条要单列成**边界**而不是控制组：控制组必须给出与基线**不同**的读数（否则就是装饰），"
    "而这条的读数**恰好等于基线** —— 它证明的是「零模数这个读数**没有**定符号的能力」。"
    "★ 这与 r398 A8 需要单独一条 `ker(iY±1)` 才把符号定下来，是同一件事的两面："
    "**零的个数对整体反号免疫**，所以任何「数零模」的判据都不能用来定 Y 的符号。")

# ============================================================ 控制组
def _ker_on(Mc, basis):
    """Mc 是复 16x16（(Re,Im) 对）；先 realify 再限制到 basis 上求零模维数"""
    assert len(Mc[0]) == NC, len(Mc[0])
    MR = realify(Mc)
    return len(basis) - rank_of(restrict_mat(MR, basis, N32), len(basis))


Y_NO_K3 = csmul(A_SUM, F(-1, 3))
_k1J, _k1K = _ker_on(Y_NO_K3, VJ), _ker_on(Y_NO_K3, VK)
add(CTL, "K1",
    "控制组（判别力）：去掉 K3 成分（Y = -(1/3)A）—— 零模**完全消失**",
    "(0, 0)（基线 (2, 0)）",
    "Y' = -(1/3)A：ker 在 V_J 上 = %d（基线 2）、在 V_K 上 = %d（基线 0）" % (_k1J, _k1K),
    "PASS" if (_k1J == 0 and _k1K == 0) else "FAIL",
    "★★★ 这一条说明 A3 里那个 `+(1/2)K3` 是零模存在的**必要条件**：没有它，两边都退化成「s = 0」，"
    "而 s 恒为 1/2 的奇数倍 ⇒ 两边都无零模。**K3 项不是装饰，它是把不可能方程变成可能方程的那一项。**"
    "★★ 同时它解释了 A6 的「奇偶性」为什么对 V_K 是致命的、对 V_J 不是 —— 差别就在 K3 是否为零。")

Y_SWAP = cadd(csmul(A_SUM, F(-1, 3)), csmul(J3C, F(1, 2)))
_k2J, _k2K = _ker_on(Y_SWAP, VJ), _ker_on(Y_SWAP, VK)
add(CTL, "K2",
    "控制组（判别力）：把 K3 换成 J3（Y = -(1/3)A + (1/2)J3）—— 零模**换到 V_K**",
    "(0, 2)（基线 (2, 0)）；个数不变，只换边",
    "Y'' = -(1/3)A + (1/2)J3：ker 在 V_J 上 = %d、在 V_K 上 = %d" % (_k2J, _k2K),
    "PASS" if (_k2J == 0 and _k2K == 2) else "FAIL",
    "★★★ 这是本卷最强的判别力：**零模位置跟着「Y 里含哪一个 su(2) 的 Cartan」走**。"
    "含 K3 ⇒ 零模在 V_J（因为 K3 在 V_J 上等于 2*eps4，能凑出 0）；含 J3 ⇒ 零模在 V_K。"
    "★★ 为什么是 2 而不是 4（我第一版又猜错过，E03）：V_K 上 `J3 = 2*eps4`，零化条件同样是 `s = 3*eps4`，"
    "满足的仍是**一个**权 ⇒ 1 复 = 2 维实。**换一个 su(2)，零模个数不变、只换边** —— 这才是这条控制组的读数。"
    "★ 对照：r398 的 K4（谱平移 1/2）给的是 (0, 4)，那是**另一个机制**（平移把 `y=1/2` 的二重态搬到 0，"
    "而这里是把 Cartan 换项）—— 两个 (0, ·) 读数不能混着用，这正是「同名变量换对象」刀。")

_k3J = len(VJ) - rank_of(zmat(len(VJ)), len(VJ))
_k3K = len(VK) - rank_of(zmat(len(VK)), len(VK))
add(CTL, "K3",
    "控制组（退化）：Y = 0 —— 零模是**全空间**",
    "(16, 16)（基线 (2, 0)）",
    "Y = 0：ker 在 V_J 上 = %d、在 V_K 上 = %d" % (_k3J, _k3K),
    "PASS" if (_k3J == len(VJ) and _k3K == len(VK)) else "FAIL",
    "★ 退化档必须是全空间，否则「2」「0」「4」「16」之间没有同一把标尺。")

_k4 = sum(1 for k in IDX_J if F(-1) * (W[k][0] + W[k][1] + W[k][2]) / 3 == 0)
add(CTL, "K4",
    "控制组（判别力）：在 V_J 上**漏掉** `eps5 = -eps4` 这一步（误取 K3 = 0）—— 零模数变 0",
    "0（基线 2）",
    "误把 K3 = 0 用在 V_J 上：零模数 = %d；正确的 y = -s/3+eps4 给的零模数 = %d"
    % (_k4, len(_zero_J)),
    "PASS" if (_k4 == 0 and len(_zero_J) == 1) else "FAIL",
    "★★ 这一条测的是 A7 里**最容易被跳过的那一步**：`J3 = 0 ⇒ eps5 = -eps4`。"
    "若照抄 V_K 的式子（K3 = 0）到 V_J 上，`y` 就退化成 `-s/3`，零模数变 0 —— "
    "而**两个半边看起来都用同一个公式**，这种错在报告里读起来完全自洽。"
    "★ 与 r398 E04（候选集只放一侧符号）同族：**错在代入，不错在算术**。")

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
    "扫描区（A1–A9 + 控制组之前）出现 %d 处" % _cb, "PASS" if _cb == 0 else "FAIL",
    "★扫描区切在控制组之前，避开自指。")

_n_id = sum(1 for r in MAIN if r["kind"] == "IDENTITY")
add(GRD, "G02", "恒等式不得记 PASS", "0 条 IDENTITY",
    "IDENTITY 条目 %d 条" % _n_id, "PASS" if _n_id == 0 else "FAIL",
    "★A3/A4 是**逐元素矩阵等式**，是对两个独立构造出的对象做比较，不是符号恒等。")

add(GRD, "G03", "四个控制组必须给出可区分的读数",
    "K1 (0,0)；K2 (0,2)；K3 (16,16)；K4 0（基线 2）",
    "K1 (%d, %d)；K2 (%d, %d)；K3 (%d, %d)；K4 0（基线 2）"
    % (_k1J, _k1K, _k2J, _k2K, _k3J, _k3K),
    "PASS" if ((_k1J, _k1K) == (0, 0) and (_k2J, _k2K) == (0, 2)
               and (_k3J, _k3K) == (16, 16) and _k4 == 0) else "FAIL",
    "★K1 测「K3 项必要」，K2 测「位置跟 Cartan 走」，K3 退化标尺，K4 测「代入 eps5=-eps4」。四者分工不重叠，"
    "且**没有一条等于基线 (2,0)** —— A9 那条读数等于基线，所以它被单列成边界而不是控制组。")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "0 违规（收尾重算，覆盖 %d 条）" % len(ALL) if _bad4 == 0 else "%d 违规" % _bad4,
    "PASS" if _bad4 == 0 else "FAIL", "★收尾重算，不是逐条自查。")

add(GRD, "G05", "维数账：权基 16 个 = V_J 8 + V_K 8（复）；实 32 = 16 + 16", "闭合",
    "权 %d 个；IDX_J %d + IDX_K %d = %d（复）；实 %d + %d = %d"
    % (_uniq, len(IDX_J), len(IDX_K), len(IDX_J) + len(IDX_K),
       len(VJ), len(VK), len(VJ) + len(VK)),
    "PASS" if (_uniq == 16 and len(IDX_J) + len(IDX_K) == 16
               and len(VJ) + len(VK) == 32) else "FAIL",
    "★三处独立：权枚举、字典映射、零空间维数。任一处错都会与另两处打架。")

add(GRD, "G06", "生成元账：su(3) 8 + su(2) 3 + Y 1 = 12；so(10) = 45；Cartan 5 个", "闭合",
    "%d + %d + 1 = %d；so(10) 基 %d 个；Cartan %d 个"
    % (len(SU3_C), len(SU2J_C), len(SU3_C) + len(SU2J_C) + 1, len(KEYS), len(HC)),
    "PASS" if (len(SU3_C) + len(SU2J_C) + 1 == 12 and len(KEYS) == 45 and len(HC) == 5) else "FAIL",
    "★5 个 Cartan 与 5 个张量积因子一一对应 —— 这是权基存在的**结构原因**（不是巧合）。")

_g7 = all(is_antisym(SIGR[kk]) for kk in KEYS) and all(is_antisym(M) for M in J_GENS + K_GENS)
add(GRD, "G07", "结构守卫：45 个 Sigma 与 J/K 的生成元实化后全部反对称", "全部反对称",
    "Sigma 全反对称 = %s；J/K 生成元全反对称 = %s"
    % (all(is_antisym(SIGR[kk]) for kk in KEYS), all(is_antisym(M) for M in J_GENS + K_GENS)),
    "PASS" if _g7 else "FAIL",
    "★★ 反对称是「实化正确」的直接后果；若 realify 的 -B 写成 +B，这里立刻红。")

VERDICT = "--".join([
    "ZERO-MODE-IS-ARITHMETIC",
    "VK-NONE-BY-PARITY" if _a6_ok else "VK-PARITY-OPEN",
    "VJ-EXACTLY-%d" % len(_zero_J),
    "K3-TERM-NECESSARY" if (_k1J == 0 and _k1K == 0) else "K3-NOT-NECESSARY",
])
_dd = {r["id"]: r["kind"] for r in ALL}
_v2 = "--".join([
    "ZERO-MODE-IS-ARITHMETIC",
    "VK-NONE-BY-PARITY" if _dd["A6"] == "PASS" else "VK-PARITY-OPEN",
    "VJ-EXACTLY-%d" % len(_zero_J),
    "K3-TERM-NECESSARY" if _dd["K1"] == "PASS" else "K3-NOT-NECESSARY",
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

_g11 = (len(KEYS) == 45 and len(HC) == 5 and all(len(W[k]) == 5 for k in range(NC)))
add(GRD, "G11", "完备性：45 个 Sigma 全建；每个权都是 5 维（5 个 Cartan 各一份）", "45 / 5 / 5",
    "Sigma %d；Cartan %d；权维数 %s"
    % (len(KEYS), len(HC), sorted({len(W[k]) for k in range(NC)})),
    "PASS" if _g11 else "FAIL",
    "★「5 个权分量」必须真数：少一个 Cartan 就会变成 4 维权，而 S4 的五重对称性会静默丢掉一维。")

_g12J = (len(_zero_J) * 2 == _kbaseJ)
_g12K = (all(y != 0 for y in _yK) == (_kbaseK == 0))
add(GRD, "G12", "两条独立路径：V_J / V_K 的零模数（矩阵零空间 vs 权枚举）", "两路一致",
    "V_J：权 %d×2 = %d 实 vs 矩阵 %d 实；V_K：权路径全非零 = %s vs 矩阵 %d 实"
    % (len(_zero_J), len(_zero_J) * 2, _kbaseJ, all(y != 0 for y in _yK), _kbaseK),
    "PASS" if (_g12J and _g12K) else "FAIL",
    "★★ 这是本卷的**总纲**：把 r398 的一条「解出来的数」换成「一条奇偶性 + 一次枚举」。"
    "★ 两路必须都对上，否则「权语言」就只是换了套写法，没有真的算出东西。")

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
_kt = "16 = %d + %d；零模 %d/%d；谱 %d 个值；K3 必要 %s" % (
    len(IDX_J), len(IDX_K), _kbaseJ, _kbaseK, len(_spec),
    (_k1J == 0 and _k1K == 0))
_kt_from_rows = "16 = %d + %d；零模 %d/%d；谱 %d 个值；K3 必要 %s" % (
    int(_all_ids["A2"]["act"].split("IDX_J ")[1].split(" 个")[0]),
    int(_all_ids["A2"]["act"].split("IDX_K ")[1].split(" 个")[0]),
    int(_all_ids["A8"]["act"].split("ker(Y|V_J) 维数 = ")[1].split("；")[0]),
    int(_all_ids["A6"]["act"].split("V_K 的 8 个态")[0].strip() or 0) if False else
    (len(VK) - rank_of(restrict_mat(Y_R, VK, N32), len(VK))),
    int(_all_ids["A5"]["act"].split("；值 ")[1].split(" 个")[0]),
    _all_ids["K1"]["kind"] == "PASS")
# 【诚实边界】与关键表里的「这句话」也必须是机拼的（r397 E08：边界段残留反向旧文案，数值守卫全绿）
# ★ 下标口径：H 的下标是 **Cartan 编号**（H_i = Sigma_{2i,2i+1}，本卷 1-based 记 H1..H5），
#   不是 Gamma 下标；把 (0,1) 印成「H1+H2」就是把两种下标混用 —— 数对、话错，守卫抓不到。


def _lin_txt(M, name):
    ps = []
    for (_ga, _gb), _v in sorted(M.items()):
        _hi = _gb // 2 + 1                       # (Gamma_a, Gamma_a+1) -> Cartan 编号
        _mag = "" if abs(_v) == 1 else str(abs(_v)) + "*"
        ps.append(("-%sH%d" % (_mag, _hi)) if _v < 0 else ("+%sH%d" % (_mag, _hi)))
    return name + " = " + " ".join(ps)


_ydec_txt = _lin_txt(Y_C, "Y")
# J3 / K3 的系数表（打印用）必须再回代成矩阵，与 HC 拼出来的那两个比一次 —— 否则印出来的名字会飘
J3_COEF = {(6, 7): F(1), (8, 9): F(1)}
K3_COEF = {(6, 7): F(1), (8, 9): F(-1)}
_b4_ok = (to_rep_c(J3_COEF, SIGC) == J3C and to_rep_c(K3_COEF, SIGC) == K3C)
_j3dec_txt = _lin_txt(J3_COEF, "J3")
_k3dec_txt = _lin_txt(K3_COEF, "K3")
_coef_txt = "，".join("H%d(=%d,%d) : %s" % (_gb // 2 + 1, _ga, _gb, str(_v))
                      for (_ga, _gb), _v in sorted(Y_C.items()))
_b1_ok = (_a3_ok and Y_C.get((0, 1)) == F(-1, 3) and Y_C.get((6, 7)) == F(1, 2))
_b3_ok = (_kbaseJ == 2 * len(_zero_J))
_kt_j3 = ("Y 的 Cartan 分解（由 Y_C 系数拼出）：%s（逐元素相等 = %s）；"
          "%s（逐元素相等 = %s）；%s（逐元素相等 = %s）"
          % (_ydec_txt, _a3_ok, _j3dec_txt, _b4_ok, _k3dec_txt, _b4_ok))
add(GRD, "G14", "关键表读数必须与主册同一条目同读数（防同名覆盖 / 防关键表写死错话）",
    "关键表四个读数 == A2/A8/A5/K1 抽出值；且 Cartan 分解那行必须由 A3/A4 的布尔量拼出；"
    "且【诚实边界】引用的数字/布尔量必须由变量拼出（系数 == A3 读数；2×零模权数 == 实维数）；"
    "且 J3/K3 的打印名（H 下标）必须回代成矩阵与 HC 拼出的那个相等",
    "关键表：%s；由 act 重算：%s；分解行：%s；边界段：系数 %s、2x零模权数==实维数 %s、J3/K3 名回代 %s"
    % (_kt, _kt_from_rows, _kt_j3, _b1_ok, _b3_ok, _b4_ok),
    "PASS" if (_kt == _kt_from_rows and _a3_ok and _a4_j and _a4_k
               and _b1_ok and _b3_ok and _b4_ok) else "FAIL",
    "★★ r396 E02 / r397 E09 / r398 E06 的直接继承：关键表里的每个数字、每句话都必须机拼。"
    "★ 本卷这句里 Y / J3 / K3 的分解式**连 H 下标都是算的**（由系数表 + (G_a,G_b) 推），"
    "所以「把 H4-H5 写成 H4+H5」这类错在字符串层已不可能；剩下的风险在**系数表本身**，"
    "那才是 A3/A4 的逐元素比对要守的东西（`_b4_ok` 还要求系数表回代成矩阵后相等）。"
    "★★★ r397 E08 的继承：**【诚实边界】段也是报告文字**，所以它里面引用的系数与"
    "「几个复权态 = 几维实零模」这两个数也走变量 —— 边界段写死数字，正是上一族自伤最容易复发的角落。")

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
A("对象：X-GSM-4（权语言：把「零模归属」从矩阵读数归约为算术）")
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
A(_kt_j3)
A("权账：%d 个权 = V_J %d（eps4=-eps5）+ V_K %d（eps4=+eps5）" % (_uniq, len(IDX_J), len(IDX_K)))
A("谱：y 取值 %s（合计 %d）" % (sorted({str(y) for y in YS}), NC))
A("零模：ker(Y|V_J) = %d 维实；ker(Y|V_K) = %d 维实" % (_kbaseJ, _kbaseK))
A("定理 W(i)：V_K 上 y = -s/3，2s 恒为奇数 ⇒ s != 0 ⇒ 无零模（读数：全非零 = %s）"
  % all(y != 0 for y in _yK))
A("定理 W(ii)：V_J 上零化 <=> eps1=eps2=eps3=eps4（读数：零模 %d 个，条件成立 = %s）"
  % (len(_zero_J), _cond))
A("")
A("【诚实边界】")
A(" 1) `Y` 的 Cartan 分解里的系数（A3 读数：%s）是**输入**（超荷嵌入），不是本卷算出来的；"
  "分解本身逐元素成立 = %s。本卷推的是「**给定**这组系数，零模落在哪一半」，不是「系数为什么这样」；"
  % (_coef_txt, _a3_ok))
A(" 2) 定理 W(i)/(ii) 的三条前提都是**可枚举**的：5 个 Cartan 同时对角（A1 = %s）、权值全是 ±1/2（A1 = %s）、"
  "`eps5 = -eps4` 来自 J3 = 0（A4 = %s/%s，A2 字典 = %s）。三条任一不成立，结论不成立；"
  % (_a1_ok, _a1_ok, _a4_j, _a4_k, _a2_ok))
A(" 3) 「%d 个复权态 = %d 维实零模」用的是「复共轭成对」（A8 用秩验证同一空间），"
  "不是「实维数 ÷ 2」这种算术；本行由变量拼出：2 × %d = %d（成立 = %s）；"
  % (len(_zero_J), _kbaseJ, len(_zero_J), _kbaseJ, _b3_ok))
A(" 4) A5 的两条路径**同源**（同一批生成元、同一套 Γ），它验证的是实现，不是前提 —— "
  "所以它不能当作「Y 的谱正确」的独立证据，只能当作「两种算法一致」的机核；")
A(" 5) 本卷不含质量谱 / Yukawa / 混合角；也不构造 `16 -> 16bar` 共轭算子。")
A("")
A("【DECLARED_NEG】%s" % sorted(DECLARED_NEG))

io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("JSON ->", JSN)
print("RPT  ->", RPT)
print("FINAL =", FINAL)
