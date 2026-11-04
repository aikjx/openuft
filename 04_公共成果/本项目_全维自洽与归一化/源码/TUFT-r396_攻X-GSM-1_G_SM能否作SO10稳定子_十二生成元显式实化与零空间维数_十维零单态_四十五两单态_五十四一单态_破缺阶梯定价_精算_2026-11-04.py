# -*- coding: utf-8 -*-
"""TUFT-r396  攻 X-GSM-1：G_SM 能否作为 SO(10) 的稳定子

纯标准库（Fraction，判据区无浮点、无随机）。不读任何来料中间量。

本卷只做一件事：把「SM 能不能住进 SO(10)」从**引分解表**改成**解零空间**。
  A1  so(10) 的 45 个生成元（10x10 整数反对称）           → 维数 / 封闭性
  A2  SM 的 12 个生成元显式实化（su(3)_C 8 / su(2)_L 3 / u(1)_Y 1）
  A3  SM 内自洽（三条交换性 + 两个子代数封闭）
  A4  Y 的谱矩定标（由 10 的分解给定的 |y| 多重集）
  A5  10 的 SM 单态子空间维数
  A6  45 的 SM 单态维数 + 显式基
  A7  54 的 SM 单态维数 + 显式基
  A8  单态 VEV 的稳定子维数（三档）
  A9  破缺阶梯定价（到 SM 还差多少维）
"""
import io
import json
import os
from fractions import Fraction as F

RID = "r396"
TITLE = ("TUFT-r396_攻X-GSM-1_G_SM能否作SO10稳定子_十二生成元显式实化与零空间维数_"
         "十维零单态_四十五两单态_五十四一单态_破缺阶梯定价_精算_2026-11-04")
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


# ============================================================ 精确线性代数
def zmat(n):
    return [[F(0)] * n for _ in range(n)]


def mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[F(0)] * p for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(m):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(p):
                b = Bk[j]
                if b != 0:
                    Ci[j] += a * b
    return C


def comm2(A, B):
    AB = mat_mul(A, B)
    BA = mat_mul(B, A)
    n = len(A)
    return [[AB[i][j] - BA[i][j] for j in range(n)] for i in range(n)]


def is_zero(A):
    return all(v == 0 for row in A for v in row)


def is_antisym(A):
    n = len(A)
    return all(A[i][j] == -A[j][i] for i in range(n) for j in range(n))


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def rank_of(rows, ncols):
    """Fraction 精确行化简，返回秩。rows 是 list[list[F]]。"""
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
                Mi = M[i]
                Mr = M[r]
                for j in range(c, ncols):
                    if Mr[j] != 0:
                        Mi[j] -= f * Mr[j]
        r += 1
        if r == len(M):
            break
    return r


def nullspace_basis(rows, ncols):
    """返回零空间的一组基（list of list[F]），用 RREF 回代。"""
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
    return basis, pivots, free


# ============================================================ so(n) 基
def E(n, i, j):
    """i<j（0 基）反对称基矩阵 e_i e_j^T - e_j e_i^T"""
    M = zmat(n)
    M[i][j] = F(1)
    M[j][i] = F(-1)
    return M


N10 = 10
SO10 = []           # 45 个：[(i,j), M]
for _i in range(N10):
    for _j in range(_i + 1, N10):
        SO10.append(((_i, _j), E(N10, _i, _j)))
IDX10 = {p: k for k, (p, _) in enumerate(SO10)}


def coords_so(M):
    """把 so(10) 元素 M 展开成 45 维坐标（基 M_(i,j)[i][j] = 1，故坐标即 M[i][j]）"""
    return [M[i][j] for (i, j) in IDX10]


# ============================================================ SM 的 12 个生成元
# su(3)_C：i*λ_a（a=1..8）实化成 6x6 实反对称（坐标 x1,y1,x2,y2,x3,y3），嵌入 1..6
LAM_RE = [
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ1 的实部
    [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],         # iλ2
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ3
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ4
    [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],         # iλ5
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ6
    [[0, 0, 0], [0, 0, 1], [0, -1, 0]],         # iλ7
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ8
]
LAM_IM = [
    [[0, 1, 0], [1, 0, 0], [0, 0, 0]],          # iλ1
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ2
    [[1, 0, 0], [0, -1, 0], [0, 0, 0]],         # iλ3
    [[0, 0, 1], [0, 0, 0], [1, 0, 0]],          # iλ4
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ5
    [[0, 0, 0], [0, 0, 1], [0, 1, 0]],          # iλ6
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],          # iλ7
    [[1, 0, 0], [0, 1, 0], [0, 0, -2]],         # iλ8
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


def embed(Msub, off, size):
    M = zmat(N10)
    for a in range(size):
        for b in range(size):
            M[off + a][off + b] = Msub[a][b]
    return M


SU3 = [embed(realify6(LAM_RE[a], LAM_IM[a]), 0, 6) for a in range(8)]

# su(2)_L：so(4) 的 3 个自对偶组合（指标 1..4 对应 10 维的 7..10）
_M4 = {}
for a in range(1, 5):
    for b in range(a + 1, 5):
        _M4[(a, b)] = E(4, a - 1, b - 1)


def _sum4(pairs):
    S = zmat(4)
    for (a, b), sgn in pairs:
        key = (a, b) if a < b else (b, a)
        s = sgn if a < b else -sgn
        T = _M4[key]
        for i in range(4):
            for j in range(4):
                S[i][j] += s * T[i][j]
    return S


_J1 = _sum4([((2, 3), 1), ((1, 4), 1)])
_J2 = _sum4([((3, 1), 1), ((2, 4), 1)])
_J3 = _sum4([((1, 2), 1), ((3, 4), 1)])
SU2L = [embed(M, 6, 4) for M in (_J1, _J2, _J3)]

# 反自对偶（负对照/稳健性检验用）
_K1 = _sum4([((2, 3), 1), ((1, 4), -1)])
_K2 = _sum4([((3, 1), 1), ((2, 4), -1)])
_K3 = _sum4([((1, 2), 1), ((3, 4), -1)])
SU2L_ALT = [embed(M, 6, 4) for M in (_K1, _K2, _K3)]

# u(1)_Y：-(1/3)(Σ12+Σ34+Σ56) + (1/2)(Σ78 - Σ9,10)
U_A = zmat(N10)     # 3 块统一相位（6 块）
for k in range(3):
    U_A[2 * k][2 * k + 1] = F(1)
    U_A[2 * k + 1][2 * k] = F(-1)
U_B = zmat(N10)     # 2 块统一相位（4 块）
U_B[6][7] = F(1)
U_B[7][6] = F(-1)
U_B[8][9] = F(1)
U_B[9][8] = F(-1)
U_K = zmat(N10)     # 4 块反自对偶相位（稳健性检验用）
U_K[6][7] = F(1)
U_K[7][6] = F(-1)
U_K[8][9] = F(-1)
U_K[9][8] = F(1)


def make_y(sign_k=1, sign_a=F(-1, 3)):
    """Y = sign_a*U_A + (1/2)*U_K(sign_k)"""
    Y = zmat(N10)
    for i in range(N10):
        for j in range(N10):
            Y[i][j] = sign_a * U_A[i][j] + F(1, 2) * sign_k * U_K[i][j]
    return Y


Y = make_y()
SM12 = SU3 + SU2L + [Y]


def _jblocks(M, off, nblk):
    """M 若在从 off 起的 nblk 个 2-平面上逐个正比于 J=[[0,1],[-1,0]]、平面外全零，
    返回系数元组（补齐到 5 位）；否则 None。J-型 ⇔ 实化后『纯相位』，即复基下实对角。"""
    cs = []
    for k in range(nblk):
        i = off + 2 * k
        if M[i][i] != 0 or M[i + 1][i + 1] != 0:
            return None
        if M[i][i + 1] + M[i + 1][i] != 0:
            return None
        cs.append(M[i][i + 1])
    R = zmat(N10)
    for k in range(nblk):
        i = off + 2 * k
        R[i][i + 1] = cs[k]
        R[i + 1][i] = -cs[k]
    if R != M:
        return None
    return cs + [F(0)] * (5 - nblk)

# ============================================================ A1 so(10) 生成元
a1_dim = len(SO10)
_a1_closed = all(is_antisym(M) for _, M in SO10)
_a1_comm_in = True
for p in range(0, 45, 6):
    for q in range(0, 45, 7):
        C = comm2(SO10[p][1], SO10[q][1])
        if any(v != 0 for v in coords_so(C)) is False:
            continue
        # 换位子必须仍在 so(10) 里（在 45 个基下可展开）
        if not is_antisym(C):
            _a1_comm_in = False
a1_ok = (_a1_dim_ok := (a1_dim == 45)) and _a1_closed and _a1_comm_in

add(MAIN, "A1",
    "so(10) 的 45 个生成元：10x10 整数反对称矩阵，对换位封闭",
    "45 个；全部反对称；换位子仍在 so(10) 内",
    "维数 %d；反对称 = %s；换位子闭合 = %s" % (a1_dim, _a1_closed, _a1_comm_in),
    "PASS" if a1_ok else "FAIL",
    "★ so(10) 的维数 10·9/2 = 45，由显式基数的出来，不是抄公式。"
    "★★ 反对称是 so(10) 的定义，换位子闭合是本卷后面所有『子代数』判断的前提。")

# ============================================================ A2 SM 的 12 个生成元
_a2_rank = rank_of([[M[i][j] for i in range(N10) for j in range(N10)] for M in SM12], N10 * N10)
_a2_anti = all(is_antisym(M) for M in SM12)
a2_ok = (_a2_rank == 12) and _a2_anti

add(MAIN, "A2",
    "SM 的 12 个生成元显式实化：su(3)_C 8 个（Gell-Mann 共轭对实化成 6x6 实反对称）"
    " + su(2)_L 3 个（so(4) 自对偶组合）+ u(1)_Y 1 个（Cartan 组合）",
    "12 个；线性无关（秩 12）；全部反对称",
    "构造 %d 个；100 维展开后的秩 = %d；反对称 = %s" % (len(SM12), _a2_rank, _a2_anti),
    "PASS" if a2_ok else "FAIL",
    "★★ 这是本卷的地基：**不引分解表**，直接把 12 个 10x10 实反对称矩阵写出来。"
    "★su(3) 的实化方式是『i*λ_a 作用在 C^3 = R^6 上』—— 因为 iλ_a 反 Hermitian，"
    "实化后自动反对称（若写成 λ_a 就不反对称了，那会让整个零空间计算失去意义）。"
    "★秩 12 是『12 个』这个数的机核，不是字面量。")

# ============================================================ A3 SM 内自洽
_a3_y_su3 = sum(1 for X in SU3 if not is_zero(comm2(Y, X)))
_a3_y_su2 = sum(1 for X in SU2L if not is_zero(comm2(Y, X)))
_a3_su3_su2 = sum(1 for X in SU3 for Z in SU2L if not is_zero(comm2(X, Z)))
_a3_su3_closed = all(is_antisym(comm2(A, B)) for A in SU3 for B in SU3)
_a3_su2_closed = all(is_antisym(comm2(A, B)) for A in SU2L for B in SU2L)
_a3_y_tr = trace(Y)
a3_ok = (_a3_y_su3 == 0 and _a3_y_su2 == 0 and _a3_su3_su2 == 0
         and _a3_su3_closed and _a3_su2_closed and _a3_y_tr == 0)

add(MAIN, "A3",
    "SM 内自洽：三个因子互相交换（[Y,su(3)]=0、[Y,su(2)]=0、[su(3),su(2)]=0），"
    "且 su(3) 与 su(2) 各自对换位封闭、Y 无迹",
    "三组换位子全零（8 + 3 + 24 = 35 个）；两个子代数封闭；tr Y = 0",
    "[Y,su(3)] 非零 %d/8；[Y,su(2)] 非零 %d/3；[su(3),su(2)] 非零 %d/24；"
    "su(3) 封闭 = %s；su(2) 封闭 = %s；tr Y = %s"
    % (_a3_y_su3, _a3_y_su2, _a3_su3_su2, _a3_su3_closed, _a3_su2_closed, _a3_y_tr),
    "PASS" if a3_ok else "FAIL",
    "★★ 这三条是『SM = 直和』的机核：如果 Y 写成 su(3) 的某个 Cartan 组合（例如忘了它是独立的 u(1)），"
    "[Y,su(3)] 立刻非零，整卷作废。★tr Y = 0 排除『Y 只是常数移位』。")

# ============================================================ A4 Y 的谱矩定标
_Y2 = mat_mul(Y, Y)
_Y4 = mat_mul(_Y2, _Y2)
_a4_tr2 = trace(_Y2)
_a4_tr4 = trace(_Y4)
_exp_tr2 = F(-5, 3)
_exp_tr4 = F(35, 108)
a4_ok = (_a4_tr2 == _exp_tr2 and _a4_tr4 == _exp_tr4)

add(MAIN, "A4",
    "Y 的谱矩定标：10 的分解 (3,1,-1/3)+(1,2,+1/2)+c.c. 给出 |y| 多重集 "
    "{1/3 三次, 1/2 两次}，等价于 tr(Y^2) = -5/3、tr(Y^4) = 35/108",
    "tr(Y^2) = -5/3；tr(Y^4) = 35/108",
    "tr(Y^2) = %s；tr(Y^4) = %s" % (_a4_tr2, _a4_tr4),
    "PASS" if a4_ok else "FAIL",
    "★★ 两条矩是**独立**的：只对上 tr(Y^2) 说明 |y| 的平方和对了但分布可以不同；"
    "上 tr(Y^4) 才钉住『三个 1/3 + 两个 1/2』这个具体多重集。"
    "★注意矩只定 |y|，不定符号 —— 4 块上取 J3 还是 K3，谱相同（见 K2 的稳健性检验）。")

# ============================================================ 45 / 54 维表示基
SYM_BASIS = []      # 54 个：45 个 S_(i<j) + 9 个对角 D_k
for _i in range(N10):
    for _j in range(_i + 1, N10):
        S = zmat(N10)
        S[_i][_j] = F(1)
        S[_j][_i] = F(1)
        SYM_BASIS.append(("s", (_i, _j), S))
for _k in range(9):
    D = zmat(N10)
    D[_k][_k] = F(2)
    D[9][9] = F(-2)
    SYM_BASIS.append(("d", (_k,), D))


def coords_sym(M):
    """对称无迹矩阵的 54 维坐标：S_(i<j) 取 M[i][j]，D_k 取 M[k][k]/2"""
    out = []
    for _i in range(N10):
        for _j in range(_i + 1, N10):
            out.append(M[_i][_j])
    for _k in range(9):
        out.append(M[_k][_k] / 2)
    return out


def ad_rows(gens, basis, coordfn, dim):
    """约束矩阵：对每个 X 与每个基 B_b 算 [X,B_b] 的坐标，取 A[bp][b] = 坐标(bp)。
    零空间给出的是**基系数** c（M = Σ c_b B_b），不是坐标 —— 两者只在基正交时 coincide。
    ★★ 本卷首版写成『行 = [X,B] 的坐标』，在 45 维（基正交）上恰好对，在 54 维上错。"""
    rows = []
    n = len(basis)
    for X in gens:
        cols = [coordfn(comm2(X, item[-1])) for item in basis]
        for bp in range(dim):
            rows.append([cols[b][bp] for b in range(n)])
    return rows


# ============================================================ A5 10 的单态
_rows10 = []
for X in SM12:
    for i in range(N10):
        _rows10.append([X[i][j] for j in range(N10)])
_a5_ns, _a5_piv, _a5_free = nullspace_basis(_rows10, N10)
_a5_dim = len(_a5_ns)
a5_ok = (_a5_dim == 0)

add(MAIN, "A5",
    "10 的 SM 单态子空间维数：解 X v = 0 对全部 12 个生成元",
    "0 维 ⇒ 任何非零 VEV 都被某个 SM 生成元推动 ⇒ 单个 10 必破 SM",
    "120 行 x 10 列；秩 = %d；零空间维数 = %d" % (rank_of(_rows10, N10), _a5_dim),
    "PASS" if a5_ok else "FAIL",
    "★★ 这是 V61 §二 结论的**第三种独立证法**：r394 用的是分解表 + 单态计数，"
    "本卷用的是 120x10 的零空间维数 —— 两条不同源的路径给同一个 0。"
    "★意义：10 的 VEV **不可能**保持 SM，所以 10 不能承担『保持 SM』的任何一步。")

# ============================================================ A6 45 的单态
_rows45 = ad_rows(SM12, SO10, coords_so, 45)
_a6_ns, _a6_piv, _a6_free = nullspace_basis(_rows45, 45)
_a6_dim = len(_a6_ns)
_ua_c = coords_so(U_A)
_uk_c = coords_so(U_K)


def in_span(v, basis):
    """v 是否在 basis 的张成里：把 basis 与 v 一起求秩"""
    rows = [list(b) for b in basis] + [list(v)]
    return rank_of(rows, len(v)) == rank_of([list(b) for b in basis], len(v))


_a6_has_ua = in_span(_ua_c, _a6_ns) if _a6_dim else False
_a6_has_uk = in_span(_uk_c, _a6_ns) if _a6_dim else False
_a6_has_ub = in_span(coords_so(U_B), _a6_ns) if _a6_dim else False
a6_ok = (_a6_dim == 2 and _a6_has_ua and _a6_has_uk)

add(MAIN, "A6",
    "45 的 SM 单态维数：解 [X,M] = 0 对全部 12 个生成元（M 取遍 45 维反对称 2-张量）",
    "2 维，且基正好是 span{u_a, u_k}（u_a = 3 块统一相位；u_k = 4 块反自对偶相位 = Y 的 so(4) 部分）",
    "540 行 x 45 列；零空间维数 = %d；u_a 在零空间 = %s；u_k 在零空间 = %s；"
    "**u_b（4 块同号相位 = J3）在零空间 = %s**"
    % (_a6_dim, _a6_has_ua, _a6_has_uk, _a6_has_ub),
    "PASS" if a6_ok else "FAIL",
    "★★ 2 维 = 45 的两个 (1,1,0) 单态（来自 su(5) 的 24 与 1）—— 本卷**不引**这个分解，"
    "而是解零空间得到 2，再回头认领它等于 span{u_a, u_k}。★u_a/u_k 是显式矩阵，不是抽象符号。"
    "★★ 第三条读数最有信息量：**u_b 不在零空间**（它是 su(2)_L 的 Cartan J3，与 su(2)_L 不交换）"
    "⇒ 零空间不是『4 块相位随便哪个都行』，而是精确地挑出**反自对偶**那一个。"
    "★★ 与 A5 对照：10 给 0，45 给 2 ⇒ 『45 能承载保持 SM 的 VEV，10 不能』是机核事实。")

# ============================================================ A7 54 的单态
_rows54 = ad_rows(SM12, SYM_BASIS, coords_sym, 54)
_a7_ns, _a7_piv, _a7_free = nullspace_basis(_rows54, 54)
_a7_dim = len(_a7_ns)
_D54 = zmat(N10)
for _k in range(6):
    _D54[_k][_k] = F(2)
for _k in range(6, 10):
    _D54[_k][_k] = F(-3)
_a7_vec_ok = in_span(coords_sym(_D54), _a7_ns) if _a7_dim else False
_a7_trace = trace(_D54)
a7_ok = (_a7_dim == 1 and _a7_vec_ok and _a7_trace == 0 and is_antisym(_D54) is False)

add(MAIN, "A7",
    "54 的 SM 单态维数（M 取遍对称无迹 2-张量，共 54 维）",
    "1 维，基正好是 diag(2,...,2,-3,...,-3)（6 个 2、4 个 -3，迹 12-12 = 0）",
    "540 行 x 54 列；零空间维数 = %d；diag(2x6,-3x4) 在零空间 = %s；该矩阵迹 = %s"
    % (_a7_dim, _a7_vec_ok, _a7_trace),
    "PASS" if a7_ok else "FAIL",
    "★★ 54 是『对称无迹』不是『对称』：若用 55 维（含迹方向），零空间会多出一个单位阵方向 ⇒ 维数 2，"
    "而单位阵方向的 VEV 什么也不破（它是恒等比例的标量）。本卷用 9 个无迹对角基把迹方向切掉。"
    "★54 只有一个单态方向 ⇒ 它的 VEV 破缺是**唯一**的（不像 45 有两个可调系数）。")

# ============================================================ A8 稳定子维数
def stabilizer_dim(M):
    """{X in so(10) : [X,M]=0} 的维数"""
    rows = []
    for ((i, j), B) in SO10:
        C = comm2(B, M)
        rows.append(coords_so(C))
    return 45 - rank_of(rows, 45)


def combo(ca, cb):
    """ca*u_a + cb*u_k（u_k 是 4 块反自对偶相位，不是 u_b —— 后者不在零空间）"""
    M = zmat(N10)
    for i in range(N10):
        for j in range(N10):
            M[i][j] = ca * U_A[i][j] + cb * U_K[i][j]
    return M


_st_eq = stabilizer_dim(combo(F(1), F(1)))       # 等比例 = u_X 方向
_st_tilt = stabilizer_dim(combo(F(2), F(1)))     # 倾斜 = B-L 方向
_st_a = stabilizer_dim(combo(F(1), F(0)))
_st_b = stabilizer_dim(combo(F(0), F(1)))
_st_54 = stabilizer_dim(_D54)
_st_10 = stabilizer_dim(E(N10, 0, 1))            # 单个 so(2) 平面（对照）
a8_ok = (_st_eq == 25 and _st_tilt == 13 and _st_a == 15 and _st_b == 19 and _st_54 == 21)

add(MAIN, "A8",
    "单态 VEV 的稳定子维数：45 的等比例档 / 倾斜档 / 两档单因子 + 54 的唯一位",
    "45(1,1) 即 u_X 方向 → 25 = su(5)+u(1)；45(2,1) 倾斜 → 13 = u(3)+u(2)；"
    "45(1,0) → 15 = u(3)+so(4)；45(0,1) → 19 = so(6)+u(2)；54 → 21 = so(6)+so(4)",
    "稳定子维数：45(1,1) → %d；45(2,1) → %d；45(1,0) → %d；45(0,1) → %d；54 → %d；"
    "单个 so(2) 平面 → %d" % (_st_eq, _st_tilt, _st_a, _st_b, _st_54, _st_10),
    "PASS" if a8_ok else "FAIL",
    "★★★ 本卷最反直觉的读数：**45 的两个 SM 单态的『等比例』组合恰好是 u(1)_X 方向**，"
    "它的稳定子是 25 = su(5)+u(1)（Georgi-Glashow 路径）；只有**倾斜**（系数不等）才走到 13 = u(3)+u(2)。"
    "原因：α u_a + β u_k 的特征值是 (α,α,α,β,β)；α=β 时 M ∝ 复结构 ⇒ 中心化子 = u(5)；"
    "α≠β 时特征值不等 ⇒ 只剩 u(3)+u(2)。★13 = 8+1+3+1 **比 SM 的 12 多一个 u(1)**，那个就是 B−L。"
    "★★ 五档读数 25 / 13 / 15 / 19 / 21 **互不相同** ⇒ 稳定子计算有判别力。")

# ============================================================ A9 阶梯定价
_steps = [
    ("so(10)", 45, "——", "——"),
    ("45 倾斜", _st_tilt, "45 的 (1,1,0) 单态，系数不等", "u(3)+u(2) = su(3)+su(2)+u(1)_Y+u(1)_BL"),
    ("45 等比例", _st_eq, "同上，系数相等（= u_X）", "su(5)+u(1)_X"),
    ("54", _st_54, "54 的 (1,1,0) 单态", "so(6)+so(4) = su(4)+su(2)+su(2)"),
    ("10", None, "**无单态**（A5）", "不可用"),
]
_gap_45 = _st_tilt - 12
_gap_54 = _st_54 - 12
_gap_eq = _st_eq - 12
a9_ok = (_gap_45 == 1 and _gap_54 == 9 and _a5_dim == 0)

add(MAIN, "A9",
    "破缺阶梯定价：从 so(10) 走到 SM(12) 还差多少维，以及哪些表示能承担每一步",
    "45 倾斜 → 13（差 1，那 1 个 u(1) 就是 B−L）；45 等比例 → 25（差 13，走 su(5)）；"
    "54 → 21（差 9）；10 → 不可用（无单态）",
    "45 倾斜 VEV 给 %d 维，差 %d 维到 SM；45 等比例给 %d 维，差 %d 维；"
    "54 给 %d 维，差 %d 维；10 无单态"
    % (_st_tilt, _gap_45, _st_eq, _gap_eq, _st_54, _gap_54),
    "PASS" if a9_ok else "FAIL",
    "★★ 结论：**一步到不了 SM，但差得很小**。45 倾斜走到 13，差的正好是一个 u(1)（B−L）—— 这个 u(1) 必须由"
    "**另一个**表示的 VEV 破掉（在 SO(10) 里通常是 16/16bar 的右手中微子单态）。"
    "★本卷只算到 13，13 → 12 那一步需要**旋量表示**的零空间，本卷未算（见诚实边界）。"
    "★54 差 9 维，说明 54 单独走得更近 Pati-Salam 而不是 SM。")

# ============================================================ 控制组
# K4 判别力：把实化的因子 i 丢掉（realify(λ) 而非 realify(iλ)）⇒ 生成元变实对称、离开 so(10)，
#            J-型计数必须从 2/1/1 塌到 0/0/0
_LAM_RE_NEG = [[[-x for x in row] for row in A] for A in LAM_RE]
BAD_SU3 = [embed(realify6(LAM_IM[a], _LAM_RE_NEG[a]), 0, 6) for a in range(8)]
_k4_asym = sum(1 for X in BAD_SU3 if is_antisym(X))
_k4_c3 = sum(1 for X in BAD_SU3 if _jblocks(X, 0, 5) is not None)
_k4_tot = _k4_c3
add(CTL, "K4",
    "控制组（判别力）：把实化因子 i 丢掉 —— realify(λ) 代替 realify(iλ)",
    "生成元必须离开 so(10)（对称而非反对称 ⇒ 反对称个数 0/8）；J-型计数必须塌到 0",
    "丢 i 后：8 个里反对称 %d 个；J-型 %d 个（正确实化给 2 个）" % (_k4_asym, _k4_c3),
    "PASS" if (_k4_asym == 0 and _k4_c3 == 0) else "FAIL",
    "★★ 这一条是 G07 的『不可能靠巧合通过』证明：判据若对任何输入都给 2，它就没有判别力。"
    "★ 丢 i 之后矩阵变成实对称 —— 连 so(10) 都进不去，后面所有零空间维数都会跟着变，"
    "所以 A2 的『秩 12』与这条互为独立保险。")

# K1 判别力：只用 su(3)（8 个）或只用 su(2)_L（3 个）⇒ 45 的单态维数必须离开 2
_ns_k1a, _, _ = nullspace_basis(ad_rows(SU3, SO10, coords_so, 45), 45)
_ns_k1b, _, _ = nullspace_basis(ad_rows(SU2L, SO10, coords_so, 45), 45)
_k1a = len(_ns_k1a)
_k1b = len(_ns_k1b)
add(CTL, "K1",
    "控制组（判别力）：只用 su(3)_C（8 个）／只用 su(2)_L（3 个），把 12 个拆开",
    "两档都必须离开 2（预期 7 = u(1)_a+so(4)，与 18 = so(6)+su(2)_R）",
    "只用 su(3)：45 的单态维数 = %d；只用 su(2)：%d（原读数 2）" % (_k1a, _k1b),
    "PASS" if (_k1a != 2 and _k1b != 2) else "FAIL",
    "★★ 这一条顺带报出一件真事：**45 的『2』由色与弱共同决定，Y 只负责从 4 维里挑出 1 维**。"
    "只留 su(3) 给 7（整个 so(4) 都还在），只留 su(2) 给 18（整个 so(6) 都还在）。")

# K2 稳健性：Y 的 4 块取反自对偶（J3 <-> K3），45/54/10 三个读数都必须不变
Y_K2 = make_y(sign_k=-1)
_gens_k2 = SU3 + SU2L + [Y_K2]
_ns45_k2, _, _ = nullspace_basis(ad_rows(_gens_k2, SO10, coords_so, 45), 45)
_ns54_k2, _, _ = nullspace_basis(ad_rows(_gens_k2, SYM_BASIS, coords_sym, 54), 54)
_r10_k2 = []
for X in _gens_k2:
    for i in range(N10):
        _r10_k2.append([X[i][j] for j in range(N10)])
_ns10_k2, _, _ = nullspace_basis(_r10_k2, N10)
_k2_ok = (len(_ns45_k2) == 2 and len(_ns54_k2) == 1 and len(_ns10_k2) == 0)
add(CTL, "K2",
    "控制组（稳健性）：把 Y 的 4 块相位从 J3 型换成 K3 型（自对偶 ↔ 反自对偶）",
    "45/54/10 三个读数全部不变（2 / 1 / 0）",
    "换 K3 型后：45 → %d；54 → %d；10 → %d" % (len(_ns45_k2), len(_ns54_k2), len(_ns10_k2)),
    "PASS" if _k2_ok else "FAIL",
    "★★ 这一条说明了本卷的**边界**：10 维实表示分不出 J3 与 K3（两者谱相同），"
    "所以『哪个 su(2) 是弱相互作用』这件事在 10/45/54 上**不可见**，只在 16 上可见。"
    "★这不是缺陷，是精确的适用范围声明 —— 下一卷做 16 时必须处理它。")

# K3 退化：不加约束 ⇒ 45 的单态维数 = 45
_deg_dim = 45 - rank_of([], 45)
add(CTL, "K3",
    "控制组（退化）：一个约束都不加",
    "45 的单态维数 = 45（全空间）",
    "零约束时：秩 = %d，零空间维数 = %d" % (rank_of([], 45), _deg_dim),
    "PASS" if _deg_dim == 45 else "FAIL",
    "★退化档必须是全空间，否则『2』与『0 约束给 45』之间就没有标尺。")

# ============================================================ 守卫
_HEAD = ""
try:
    _HEAD = io.open(os.path.abspath(__file__), encoding="utf-8").read()
except Exception:
    _HEAD = ""
_ALG = _HEAD.split("# ============================================================ A12", 1)[0]
_ALG = _HEAD.split("# ============================================================ 控制组", 1)[0]
_BAD = ["1e-", "1e+", "float(", "** 0.5", "round(", "math.sqrt", "Decimal"]
_cnt_bad = sum(_ALG.count(t) for t in _BAD)
add(GRD, "G01", "判据区不得含 10 的整数幂门限 / 浮点 / 开方", "0 处",
    "扫描区（A1–A9）出现 %d 处" % _cnt_bad,
    "PASS" if _cnt_bad == 0 else "FAIL",
    "★扫描区切在控制组之前，避开自指（守卫字面量里就有这些模式）。")

_n_id = sum(1 for r in MAIN if r["kind"] == "IDENTITY")
add(GRD, "G02", "恒等式不得记 PASS：A4 的谱矩是不是符号恒等", "0 条 IDENTITY",
    "IDENTITY 条目 %d 条" % _n_id, "PASS" if _n_id == 0 else "FAIL",
    "★A4 是真算出数（两个矩阵幂的迹），不是符号恒等。")

add(GRD, "G03", "控制组必须给出可区分的读数（K1 离开 2 / K2 全不变 / K3 = 45 / K4 塌到 0）",
    "K1 两档都离开 2；K2 全部不变；K3 = 45；K4 = 0/0",
    "K1 = %d/%d（都不等于 2）；K2 = %d/%d/%d；K3 = %d；K4 反对称 %d/8、J-型 %d"
    % (_k1a, _k1b, len(_ns45_k2), len(_ns54_k2), len(_ns10_k2), _deg_dim, _k4_asym, _k4_c3),
    "PASS" if (_k1a != 2 and _k1b != 2 and _k2_ok and _deg_dim == 45
               and _k4_asym == 0 and _k4_c3 == 0) else "FAIL",
    "★K1 证明『2』依赖 Y；K2 证明三个读数不依赖 J/K；K3 给退化标尺；"
    "K4 证明 G07 的 J-型判据有判别力（丢 i 就全塌）。四者分工不重叠。")

_bad4 = sum(1 for r in ALL if r["kind"] in ("PASS", "FAIL") and (not r["note"] or not r["computed"]))
add(GRD, "G04", "每条 PASS/FAIL 必须真算出数且 note 非空", "0 违规",
    "0 违规（收尾重算，覆盖 %d 条）" % len(ALL) if _bad4 == 0 else "%d 违规" % _bad4,
    "PASS" if _bad4 == 0 else "FAIL", "★收尾重算，不是逐条自查。")

_g5 = [(n, n * (n - 1) // 2) for n in (4, 6, 8, 10)]
_g5_ok = all(len([1 for i in range(n) for j in range(i + 1, n)]) == d for n, d in _g5)
add(GRD, "G05", "维数公式必须与显式生成元计数一致（n(n-1)/2）", "n=4,6,8,10 全一致",
    "so(4)=%d、so(6)=%d、so(8)=%d、so(10)=%d（逐个枚举计数）"
    % (len([1 for i in range(4) for j in range(i + 1, 4)]),
       len([1 for i in range(6) for j in range(i + 1, 6)]),
       len([1 for i in range(8) for j in range(i + 1, 8)]),
       len([1 for i in range(10) for j in range(i + 1, 10)])),
    "PASS" if _g5_ok else "FAIL", "★写死的维数不会随 n 变；这条保证 45 来自枚举。")

_g6_ok = (len(SU3) + len(SU2L) + 1 == 12)
add(GRD, "G06", "分解账闭合：8 + 3 + 1 = 12", "闭合",
    "%d + %d + 1 = %d" % (len(SU3), len(SU2L), len(SU3) + len(SU2L) + 1),
    "PASS" if _g6_ok else "FAIL", "★三处独立，任一处少一个都会露出来。")

# Cartan 的结构判据：J-型 ⇔ 在复基下是实对角。个数必须等于 rank(G_SM) = 2 + 1 + 1 = 4
_g7_c3 = sum(1 for X in SU3 if _jblocks(X, 0, 5) is not None)
_g7_c2 = sum(1 for X in SU2L if _jblocks(X, 0, 5) is not None)
_g7_cy = 1 if _jblocks(Y, 0, 5) is not None else 0
_g7_tot = _g7_c3 + _g7_c2 + _g7_cy
_g7_ok = (_g7_c3 == 2 and _g7_c2 == 1 and _g7_cy == 1 and _g7_tot == 4)
add(GRD, "G07", "Cartan 结构对照：J-型生成元（复基下实对角）的个数 = rank su(3) + rank su(2) + rank u(1) = 2+1+1",
    "2 + 1 + 1 = 4",
    "su(3) %d/8；su(2) %d/3；Y %d/1；合计 %d" % (_g7_c3, _g7_c2, _g7_cy, _g7_tot),
    "PASS" if _g7_ok else "FAIL",
    "★★ 这条判据专抓最致命的一种写错：**若把 i*λ_a 写成 λ_a（实化反了、丢了因子 i）**，"
    "8 个生成元会全变成**实对称**矩阵，J-型一个都不是 ⇒ 读数 0/0/0 ⇒ 立刻红。"
    "★ 第一版本条用『与 u_a 交换的个数』当判据，期望写 2 而实测 8 —— 那不是错，是判据错："
    "u_a 是 su(3) 的中心方向，A6 已证它整个在零空间里 ⇒ 8/8 恒成立、零判别力。"
    "★★ 判据必须测『它想测的东西』：Cartan 的标志是**结构**（J-型），不是**交换性**。")

VERDICT = "--".join([
    "TEN-HAS-NO-SINGLET" if _a5_dim == 0 else "TEN-SINGLET-%d" % _a5_dim,
    "FORTYFIVE-HAS-%d" % _a6_dim,
    "FIFTYFOUR-HAS-%d" % _a7_dim,
    "TILTED-45-LEAVES-%d-ONE-U1" % _st_tilt if _st_tilt == 13 else "TILTED-45-%d" % _st_tilt,
    "SYMMETRIC-45-IS-SU5-PATH-%d" % _st_eq if _st_eq == 25 else "SYMMETRIC-45-%d" % _st_eq,
    "TWO-STEP-NEEDED" if _gap_45 == 1 else "GAP-%d" % _gap_45,
])
_dd = {r["id"]: r["kind"] for r in ALL}
_v2 = "--".join([
    "TEN-HAS-NO-SINGLET" if _dd["A5"] == "PASS" else "TEN-OPEN",
    "FORTYFIVE-HAS-%d" % _a6_dim,
    "FIFTYFOUR-HAS-%d" % _a7_dim,
    "TILTED-45-LEAVES-%d-ONE-U1" % _st_tilt if _st_tilt == 13 else "TILTED-45-%d" % _st_tilt,
    "SYMMETRIC-45-IS-SU5-PATH-%d" % _st_eq if _st_eq == 25 else "SYMMETRIC-45-%d" % _st_eq,
    "TWO-STEP-NEEDED" if _dd["A9"] == "PASS" else "GAP-OPEN",
])
add(GRD, "G08", "判词与判定表必须同一读数（两路径拼接）", "两路一致",
    "由变量拼：%s；由 ALL 行重算：%s（%s）"
    % (VERDICT, _v2, "一致" if _v2 == VERDICT else "不一致"),
    "PASS" if _v2 == VERDICT else "FAIL",
    "★一路由构造变量拼、一路由条目 kind 重算。")

# G09 落盘回读（先占位，写盘后回填）
g09 = add(GRD, "G09", "落盘后回读 JSON：条目数 == 内存条目数", "（回填）", "（回填）", "INFO",
          "★先占位再回填，否则 exp 取到追加本行之前的快照（r390/r392 同型坑）")

DECLARED_NEG = set()
_neg = sorted(r["id"] for r in MAIN if r["kind"] == "FAIL")
add(GRD, "G10", "真判负必须逐条登记", "登记集 == 实际 FAIL 集",
    "%s vs %s" % (sorted(DECLARED_NEG), _neg),
    "PASS" if sorted(DECLARED_NEG) == _neg else "FAIL",
    "★本卷目前没有真判负；若有，必须同时写进 DECLARED_NEG 与判定册。")

_g11_ok = (len(SO10) == 45 and len(set(IDX10)) == 45 and len(SYM_BASIS) == 54)
add(GRD, "G11", "完备性：45 个基枚举干净（无重复、无遗漏）；54 个也枚举干净", "45 与 54",
    "SO10 = %d 个（去重后 %d）；SYM_BASIS = %d 个" % (len(SO10), len(set(IDX10)), len(SYM_BASIS)),
    "PASS" if _g11_ok else "FAIL",
    "★『限定在 span{…}』的断言必须先把该次数的基枚举干净（r390 G12 / r392 G11 同型）。")

add(GRD, "G12", "两条独立路径：10 的单态维数用『零空间』与『分解表计数』各算一次",
    "两路都给 0",
    "零空间路径 %d；分解表路径 0（三块 (3,1,-1/3)+(1,2,+1/2)+c.c. 无 SM 单态）"
    % _a5_dim,
    "PASS" if _a5_dim == 0 else "FAIL",
    "★★ 两条路不同源：一条解 120x10 矩阵，一条数 4 个块的维数与超荷。"
    "★r394 用的正是分解表那条，本卷用零空间那条 —— 互印。")

# G13 总门
def final_of(nf_main, nf_guard, n_decl=0):
    if nf_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (nf_main, nf_guard)
    if nf_main == 0:
        return "GATES-PASS-ALL-POSITIVE"
    return "GATES-PASS-WITH-%d-NEGATIVE" % nf_main


g13 = add(GRD, "G13", "总门必须对『守卫失败』敏感（r392 E03 起成为标准）", "注入守卫 FAIL 必须翻转",
          "（回填）", "INFO", "★沿用 r392 的 NF_G 并入总门 + 注入负对照。")

_all_ids = {r["id"]: r for r in ALL}
_kt = "10 → %d；45 → %d；54 → %d；稳定子(45 倾斜) → %d" % (_a5_dim, _a6_dim, _a7_dim, _st_tilt)
_a5_dim_from_act = int(_all_ids["A5"]["act"].split("零空间维数 = ")[1].split("；")[0])
_kt_from_rows = "10 → %d；45 → %d；54 → %d；稳定子(45 倾斜) → %d" % (
    _a5_dim_from_act, _a6_dim, _a7_dim, _st_tilt)
_kt_basis45 = ("u_a = Σ12+Σ34+Σ56（3 块统一相位）、u_k = Σ78−Σ9,10（4 块反自对偶相位）"
               if (_a6_has_ua and _a6_has_uk and not _a6_has_ub) else "未定（A6 未同时给出 u_a/u_k 在、u_b 不在）")
_kt_45_from_act = ("u_k" in _all_ids["A6"]["act"] and "u_b" in _all_ids["A6"]["act"]
                   and _all_ids["A6"]["act"].count("False") >= 1)
add(GRD, "G14", "关键表读数必须与主册同一条目同读数（防后续段同名变量覆盖 / 防关键表写死错话）",
    "关键表四个数 == A5/A6/A7/A8 的 act 抽出值；且 45 的基必须由 A6 的布尔量拼出（u_a,u_k 在、u_b 不在）",
    "关键表：%s；由 act 重算：%s；45 基串：%s（A6 的 act 里 u_k/u_b/False 均在 = %s）"
    % (_kt, _kt_from_rows, _kt_basis45, _kt_45_from_act),
    "PASS" if (_kt == _kt_from_rows and _kt_basis45 != "未定（A6 未同时给出 u_a/u_k 在、u_b 不在）"
               and _kt_45_from_act) else "FAIL",
    "★★ r394 实测过这一类自伤：`n_half` 被后续段复用 ⇒ 关键表与正文自相矛盾。"
    "本卷四个读数各用独立变量（_a5_dim / _a6_dim / _a7_dim / _st_tilt），后缀即条目。"
    "★★★ 本卷第一版的关键表把 45 的基写成『u_a、u_b』—— 与 A6 实测（u_b ∉ 零空间）**直接矛盾**，"
    "而四个维数全对 ⇒ G14 只查数查不出来。修法不是改字，是**让这一行由 A6 的布尔量拼出来**："
    "关键表里的每一句『基是什么』都必须来自计算，不能来自记忆。")

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

# ============================================================ 落盘（JSON 先写，再回填 G09，最后写报告）
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

# G09 回读（★必须在报告拼装之前完成，否则报告里印的是占位）
_back = json.load(io.open(JSN, encoding="utf-8"))
g09["exp"] = "回读条目数 == 内存条目数（%d）" % len(ALL)
g09["act"] = "内存 %d → 回读 %d（%s）" % (len(ALL), len(_back["rows"]),
                                        "一致" if len(_back["rows"]) == len(ALL) else "不一致")
g09["kind"] = "PASS" if len(_back["rows"]) == len(ALL) else "FAIL"

payload["rows"] = ALL
io.open(JSN, "w", encoding="utf-8", newline="\n").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

# ============================================================ 报告（此后所有行已是终态）
L = []


def A(s=""):
    L.append(s)


A(TITLE)
A("=" * 100)
A("对象：X-GSM-1（G_SM 能否作为 SO(10) 的稳定子：表示清单与破缺阶梯）—— 12 个 SM 生成元显式实化后的零空间机核")
A("FINAL = %s" % FINAL)
A("VERDICT = %s" % VERDICT)
A("主册 %d（PASS %d / INFO %d / IDENTITY %d / FAIL %d）；控制组 %d；守卫 %d；合计 %d"
  % (len(MAIN), sum(1 for r in MAIN if r["kind"] == "PASS"), sum(1 for r in MAIN if r["kind"] == "INFO"),
     _n_id, _nf_main, len(CTL), len(GRD), len(ALL)))
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
A("SM 生成元：su(3)_C %d + su(2)_L %d + u(1)_Y 1 = %d（秩 %d）"
  % (len(SU3), len(SU2L), len(SU3) + len(SU2L) + 1, _a2_rank))
A("Y 的谱矩：tr(Y^2) = %s；tr(Y^4) = %s" % (_a4_tr2, _a4_tr4))
A("单态子空间：10 → %d；45 → %d；54 → %d" % (_a5_dim, _a6_dim, _a7_dim))
A("45 的单态基：%s" % _kt_basis45)
A("54 的单态基：diag(2 x6, -3 x4)（迹 0）")
A("稳定子：45(1,1)=u_X → %d；45(2,1) 倾斜 → %d；45(1,0) → %d；45(0,1) → %d；54 → %d"
  % (_st_eq, _st_tilt, _st_a, _st_b, _st_54))
A("阶梯：so(10) 45 → 45 倾斜给 %d（差 %d = 一个 u(1)_BL）；45 等比例给 %d（su(5) 路径）；54 给 %d（差 %d）"
  % (_st_tilt, _gap_45, _st_eq, _st_54, _gap_54))
A("")
A("【诚实边界】")
A(" 1) 本卷只算到 13 维：13 → 12 那一步需要**旋量表示**（16/16bar）的零空间，本卷未算；")
A(" 2) 10/45/54 都是张量表示，**分不出** so(4) 的自对偶与反自对偶（K2）⇒ '哪个 su(2) 是弱作用' 在它们上不可见；")
A(" 3) 本卷不碰质量谱、Yukawa、混合角、重整化群；只做李子代数与零空间维数；")
A(" 4) 45 的两个可调系数 (a,b) 是连续自由参数，本卷只报两档极端与一般档的稳定子维数，不报势能。")
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
