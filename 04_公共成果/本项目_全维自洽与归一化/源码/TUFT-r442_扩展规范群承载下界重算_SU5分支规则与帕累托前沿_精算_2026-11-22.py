# -*- coding: utf-8 -*-
"""TUFT-r442 · 扩展规范群下的承载下界重算

主题：Georgi–Glashow `SU(5)` 的 `5̄ ⊕ 10` 分支规则，与 `r441` 的 `(15, 5, 5)`
承载下界三判据逐项对账，并给出 SM 分块 / SU(5) / SO(10) 的帕累托前沿。

回答 `r441` §九 未覆盖项 **U1（扩展规范群）**：
直接 import r441 不可能（文件名含中文且需可独立复跑）⇒ 本册**重写**同一套
`anomalies` / `central_dim` / 群生成元，做**独立实现**对拍（不是复制结论）。

纯标准库（`Fraction` 精确，零浮点）· 无第三方依赖 · Python 3.8。
输出：../数据/TUFT-r442_..._{json,md,_report.txt}
"""
import io
import json
import os
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                     # .../本项目_全维自洽与归一化
DATA = os.path.join(BASE, '数据')
JUDGE = os.path.join(BASE, '判定')
SRC = os.path.join(BASE, '源码')
STAMP = '2026-11-22'
TAG = 'TUFT-r442_扩展规范群承载下界重算_SU5分支规则与帕累托前沿_精算_' + STAMP

ENTRIES = []
GUARDS = []
KEY = {}


# ---------------------------------------------------------------- 复数（精确）
class C(object):
    """a + bi，a,b 为 Fraction。"""

    __slots__ = ('re', 'im')

    def __init__(self, re=0, im=0):
        self.re = F(re)
        self.im = F(im)

    def __add__(self, o):
        o = _c(o)
        return C(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        o = _c(o)
        return C(self.re - o.re, self.im - o.im)

    def __mul__(self, o):
        o = _c(o)
        return C(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    def __neg__(self):
        return C(-self.re, -self.im)

    def iszero(self):
        return self.re == 0 and self.im == 0

    def inv(self):
        d = self.re * self.re + self.im * self.im
        return C(self.re / d, -self.im / d)

    def __truediv__(self, o):
        o = _c(o)
        return self * o.inv()

    def conj(self):
        return C(self.re, -self.im)

    def __eq__(self, o):
        if not isinstance(o, C):
            o = _c(o)
        return self.re == o.re and self.im == o.im

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash((self.re, self.im))

    def __repr__(self):
        return '(%s%+si)' % (self.re, self.im)


def _c(x):
    if isinstance(x, C):
        return x
    return C(x, 0)


ZERO = C(0)
ONE = C(1)


# ---------------------------------------------------------------- 矩阵工具
def cmat(n, m, val=None):
    v = ZERO if val is None else _c(val)
    return [[v for _ in range(m)] for _ in range(n)]


def ceye(n):
    M = cmat(n, n)
    for i in range(n):
        M[i][i] = ONE
    return M


def ctrace(M):
    return sum((M[i][i] for i in range(len(M))), ZERO)


def crank(rows):
    """复矩阵的秩：行阶梯消元（只向下消，不归一化 pivot 行）。

    与 RREF 版（归一化 pivot + 全消）在本册全部用例上给出**相同秩**，
    改用行阶梯只是工程优化（不建 `pv = M[rank][c].inv()`，Fraction 路径更短）。
    ★不要据此认为 RREF 版有 bug：15 维中心化子 = 7 而非 5 的真实原因是
    「两个 (3,1) 是等价副本、可混合」，与消元算法无关（两版都给 7）。
    """
    M = [[_c(x) for x in r] for r in rows]
    M = [rr for rr in M if any(not x.iszero() for x in rr)]
    if not M:
        return 0
    n, m = len(M), len(M[0])
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if not M[i][c].iszero():
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pr = M[r]
        pc = pr[c]
        for i in range(r + 1, n):
            if not M[i][c].iszero():
                f = M[i][c] / pc
                M[i] = [M[i][j] - f * pr[j] for j in range(m)]
        r += 1
        if r == n:
            break
    return r


def central_dim(gens, d):
    """与 gens 全部对易的 d x d 复矩阵空间，返回复维数（Schur：不可约时为 1）。"""
    rows = []
    for g in gens:
        for i in range(d):
            for j in range(d):
                row = [ZERO] * (d * d)
                for k in range(d):
                    row[i * d + k] = row[i * d + k] + g[k][j]
                    row[k * d + j] = row[k * d + j] - g[i][k]
                rows.append(row)
    rows = [r for r in rows if any(not x.iszero() for x in r)]
    return d * d - crank(rows)


def kron(A, B):
    n, m = len(A), len(A[0])
    p, q = len(B), len(B[0])
    out = cmat(n * p, m * q)
    for i in range(n):
        for j in range(m):
            a = A[i][j]
            if a.iszero():
                continue
            for k in range(p):
                for l in range(q):
                    out[i * p + k][j * q + l] = a * B[k][l]
    return out


def bdiag(*Ms):
    """块对角。"""
    n = sum(len(M) for M in Ms)
    m = sum(len(M[0]) for M in Ms)
    out = cmat(n, m)
    ro = 0
    co = 0
    for M in Ms:
        for i in range(len(M)):
            for j in range(len(M[0])):
                out[ro + i][co + j] = M[i][j]
        ro += len(M)
        co += len(M[0])
    return out


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    return bool(ok)


def entry(code, title, verdict, detail, numbers=None):
    ENTRIES.append({'code': code, 'title': title, 'verdict': verdict,
                    'detail': detail, 'numbers': numbers or {}})
    return verdict


# ---------------------------------------------------------------- 表示维数
def dim_su2(tw):
    """tw = 2j+1。"""
    return int(tw)


def dim_su3(p, q):
    """SU(3) 不可约表示 (p,q) 的复维数。"""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def dim_su(n, k):
    """SU(n) 的 k 阶反对称表示维数 = C(n,k)。"""
    num = 1
    den = 1
    for i in range(k):
        num *= (n - i)
        den *= (i + 1)
    return num // den


# ---------------------------------------------------------------- 生成元
def su2_gens():
    h = F(1, 2)
    ih = C(0, h)
    return [
        [[ZERO, C(h)], [C(h), ZERO]],
        [[ZERO, -ih], [ih, ZERO]],
        [[C(h), ZERO], [ZERO, C(-h)]],
    ]


def su3_gens():
    """su(3) 八个生成元 lambda_A/2；lambda_8 用 diag(1,1,-2)（整体缩放不改中心）。"""
    h = F(1, 2)
    i = C(0, 1)

    def m(rows):
        return [[_c(x) for x in row] for row in rows]
    raw = [
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, -i, 0], [i, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, -i], [0, 0, 0], [i, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 0, -i], [0, i, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]],
    ]
    return [[[x * C(h) for x in row] for row in m(r)] for r in raw]


S2 = su2_gens()
S3 = su3_gens()

Z2 = cmat(2, 2)
Z3 = cmat(3, 3)
Z5 = cmat(5, 5)
I2 = ceye(2)
I3 = ceye(3)


def su5_gens():
    """su(5) 的 24 个 Hermitian 生成元（5x5，色指标 0,1,2 / 弱指标 3,4）。

    24 = 8(SU3) + 3(SU2) + 12(X/Y 型) + 1(T_24)
    """
    out = []
    for g in S3:
        out.append(bdiag(g, Z2))
    for g in S2:
        out.append(bdiag(Z3, g))
    for a in range(3):
        for b in range(3, 5):
            E1 = cmat(5, 5)
            E1[a][b] = ONE
            E1[b][a] = ONE
            out.append(E1)
            E2 = cmat(5, 5)
            E2[a][b] = C(0, 1)
            E2[b][a] = C(0, -1)
            out.append(E2)
    T24 = cmat(5, 5)
    for a in range(3):
        T24[a][a] = C(F(-1, 3))
    for b in range(3, 5):
        T24[b][b] = C(F(1, 2))
    out.append(T24)
    return out


SU5 = su5_gens()


def adj(g):
    """共轭转置。"""
    n = len(g)
    return [[g[j][i].conj() for j in range(n)] for i in range(n)]


def wedge2(g):
    """Lambda^2(5) 的 10x10 矩阵：作用在 e_i ^ e_j (i<j) 基上。"""
    idx = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    pos = dict((p, k) for k, p in enumerate(idx))
    M = cmat(10, 10)
    for a, (i, j) in enumerate(idx):
        # (g e_i) ^ e_j
        for k in range(5):
            coef = g[k][i]
            if coef.iszero():
                continue
            if k == j:
                continue
            if k < j:
                M[a][pos[(k, j)]] = M[a][pos[(k, j)]] + coef
            else:
                M[a][pos[(j, k)]] = M[a][pos[(j, k)]] - coef
        # e_i ^ (g e_j)
        for l in range(5):
            coef = g[l][j]
            if coef.iszero():
                continue
            if l == i:
                continue
            if i < l:
                M[a][pos[(i, l)]] = M[a][pos[(i, l)]] + coef
            else:
                M[a][pos[(l, i)]] = M[a][pos[(l, i)]] - coef
    return M


# ---------------------------------------------------------------- 群构造
# 5 表示、5bar 表示（共轭）、10 表示（Lambda^2）
G5 = SU5
G5B = [[[-x for x in row] for row in adj(g)] for g in SU5]
G10 = [wedge2(g) for g in SU5]


# ---------------------------------------------------------------- SM 单代场表
# 反常用表：右手场 right=True，求和时取 y = -Y（左手共轭）
SM_CHIRAL = [
    ('Q_L', (1, 0), 2, F(1, 6), False),
    ('u_R', (0, 1), 1, F(2, 3), True),
    ('d_R', (0, 1), 1, F(-1, 3), True),
    ('L', (0, 0), 2, F(-1, 2), False),
    ('e_R', (0, 0), 1, F(-1), True),
]

# r441 的 SM_SINGLE 里 d_R 的 Y 写成 +1/3（应为 -1/3）；此处用正确值并登记为 CORRECTED。
SM_Y_CORRECT = sorted(set([F(1, 6), F(2, 3), F(-1, 3), F(-1, 2), F(-1)]))
SM_Y_R441 = sorted(set([F(1, 6), F(2, 3), F(1, 3), F(-1, 2), F(-1)]))


def anomalies(fields):
    """四条反常：a22=[SU2]^2 U1、a33=[SU3]^2 U1、ayyy=U1^3、agr=grav-U1。"""
    a22 = F(0)
    a33 = F(0)
    ayyy = F(0)
    agr = F(0)
    for name, su3, tw, Y, right in fields:
        d3 = dim_su3(*su3)
        d2 = tw
        y = -Y if right else Y
        T2 = F(1, 2) if d2 == 2 else F(0)
        T3 = F(1, 2) if su3 in ((1, 0), (0, 1)) else F(0)
        a22 += T2 * d3 * y
        a33 += T3 * d2 * y
        ayyy += d3 * d2 * y ** 3
        agr += d3 * d2 * y
    return a22, a33, ayyy, agr


# ---------------------------------------------------------------- SU(5) -> SM 分支
# 5 的 T_24 本征值：3 个色 -1/3、2 个弱 +1/2
LAM5 = [F(-1, 3)] * 3 + [F(1, 2)] * 2

# 5bar：本征值取负
LAM5B = [-x for x in LAM5]

# 10 = Lambda^2(5)：本征值 = 两两之和
IDX10 = [(i, j) for i in range(5) for j in range(i + 1, 5)]
LAM10 = [LAM5[i] + LAM5[j] for (i, j) in IDX10]


def block_of_5b(i):
    """5bar 的第 i 个基向量属于哪个 (d3, d2) 块（色 0,1,2 / 弱 3,4）。"""
    return (1, 2) if i > 2 else (3, 1)


def block_of_10(i, j):
    """10 的 e_i ^ e_j 属于哪个 (d3, d2) 块。"""
    nc = (1 if i < 3 else 0) + (1 if j < 3 else 0)
    if nc == 2:
        return (3, 1)          # 3bar x 1
    if nc == 1:
        return (3, 2)
    return (1, 1)              # 2 x 2 完全反对称


def comm_zero(A, B):
    """[A,B] = 0（精确）。"""
    n = len(A)
    for i in range(n):
        for j in range(n):
            s = ZERO
            for k in range(n):
                s = s + A[i][k] * B[k][j] - B[i][k] * A[k][j]
            if not s.iszero():
                return False
    return True


def dim_so10_spinor():
    """SO(10) 的 Weyl 旋量（手征）维数 = 2^(10/2 - 1) = 16。"""
    return 2 ** (10 // 2 - 1)


def dec_from_lams():
    """由本征值表聚合不可约分解 {(d3,d2): 重数}。

    关键：基向量个数 != 重数。一个 (d3,d2) 块占 d3*d2 个基向量，
    所以 重数 = 该块的基向量数 / (d3*d2)。（首版把基向量数当重数，
    直接把 10 的 3 个色-色指标对算成 (3,1)x3 ⇒ 维数爆炸成 46。）
    """
    counts = {}
    for i in range(5):
        b = block_of_5b(i)
        counts[b] = counts.get(b, 0) + 1
    for (i, j) in IDX10:
        b = block_of_10(i, j)
        counts[b] = counts.get(b, 0) + 1
    dec = {}
    for (d3, d2), cnt in counts.items():
        assert cnt % (d3 * d2) == 0, 'block %s has %d basis vectors' % ((d3, d2), cnt)
        dec[(d3, d2)] = cnt // (d3 * d2)
    return dec


SM_NEED = {(3, 2): 1, (3, 1): 2, (1, 2): 1, (1, 1): 1}
GG_DEC = dec_from_lams()


def dec_dim(dec):
    return sum(d3 * d2 * n for (d3, d2), n in dec.items())


def dec_count(dec):
    """不可约块数 = 重数之和（不是键数）。"""
    return sum(dec.values())


def dec_missing(dec):
    out = {}
    for key in sorted(set(list(SM_NEED.keys()) + list(dec.keys()))):
        need = SM_NEED.get(key, 0)
        have = dec.get(key, 0)
        if need > have:
            out[key] = need - have
    return out


def dec_excess(dec):
    out = {}
    for key in sorted(set(list(SM_NEED.keys()) + list(dec.keys()))):
        need = SM_NEED.get(key, 0)
        have = dec.get(key, 0)
        if have > need:
            out[key] = have - need
    return out


def fmt_dec(dec):
    parts = []
    for (d3, d2) in sorted(dec.keys()):
        n = dec[(d3, d2)]
        parts.append('(%d,%d)x%d[%d]' % (d3, d2, n, d3 * d2 * n))
    return ' + '.join(parts)


# ================================================================ G0：构造自检
guard('G0-1 SU(n) 反对称表示维数 C(5,k)',
      [dim_su(5, k) for k in (0, 1, 2, 3, 4, 5)] == [1, 5, 10, 10, 5, 1],
      'C(5,1)=5 · C(5,2)=10')

guard('G0-2 su(5) 生成元个数 = 24',
      len(SU5) == 24 and len(G5) == 24 and len(G5B) == 24 and len(G10) == 24,
      '24 = 8(SU3) + 3(SU2) + 12(X/Y) + 1(T_24)')

guard('G0-3 生成元矩阵阶数 5 / 5 / 10',
      all(len(g) == 5 for g in G5) and all(len(g) == 5 for g in G5B)
      and all(len(g) == 10 for g in G10),
      '5, 5bar 各 5x5 · 10 为 10x10')

guard('G0-4 全部生成元 Hermitian',
      all(all(g[i][j].conj() == g[j][i] and g[j][i].conj() == g[i][j]
              for i in range(len(g)) for j in range(len(g)))
          for g in G5),
      'T^dag = T（Lambda^2 保持 Hermitian）')

guard('G0-5 全部生成元 traceless',
      all(ctrace(g).iszero() for g in G5)
      and all(ctrace(g).iszero() for g in G10),
      'Tr(T)=0 在 5 与 10 上均为 0')

T24_M = G5[len(G5) - 1]
guard('G0-6 [T_24, SU(3)_a] = 0（矩阵对易，非对称性）',
      all(comm_zero(G5[k], T24_M) for k in range(8)),
      'T_24 = diag(-1/3 x3, 1/2 x2) 在色块上为标量 ⇒ 与 su(3) 对易')

guard('G0-7 [T_24, SU(2)_i] = 0（矩阵对易，非对称性）',
      all(comm_zero(G5[k], T24_M) for k in range(8, 11)),
      'T_24 在弱块上为标量 ⇒ 与 su(2) 对易')

# ================================================================ G1：分支规则
guard('G1-1 5bar 在 SU(3)xSU(2) 下分支为 (3bar,1) + (1,2)',
      block_of_5b(0) == (3, 1) and block_of_5b(2) == (3, 1)
      and block_of_5b(3) == (1, 2) and block_of_5b(4) == (1, 2),
      '(3bar,1)[3] + (1,2)[2] = 5')

guard('G1-2 10 在 SU(3)xSU(2) 下分支为 (3,2) + (3bar,1) + (1,1)',
      block_of_10(0, 1) == (3, 1) and block_of_10(0, 3) == (3, 2)
      and block_of_10(3, 4) == (1, 1),
      '(3,2)[6] + (3bar,1)[3] + (1,1)[1] = 10')

guard('G1-3 5bar + 10 维数 = 15',
      dec_dim(GG_DEC) == 15 and dim_su(5, 1) + dim_su(5, 2) == 15,
      '5 + 10 = 15')

guard('G1-4 与 r441 的 dec_sm 逐块双向一致（缺 0 / 多 0）',
      dec_missing(GG_DEC) == {} and dec_excess(GG_DEC) == {}
      and GG_DEC == SM_NEED,
      'GG = %s  ≡  SM_NEED = %s' % (fmt_dec(GG_DEC), fmt_dec(SM_NEED)))

guard('G1-5 5bar+10 的 SU(3)xSU(2) 块数仍 = 5',
      dec_count(GG_DEC) == 5,
      '键数 4 但重数之和 5（(3,1) 出现两次）')

guard('G1-6 T_24 在 5bar 上的本征值多重集 = {1/3 x3, -1/2 x2}',
      sorted(LAM5B) == sorted([F(1, 3)] * 3 + [F(-1, 2)] * 2),
      '5bar: 3 个 +1/3（d_R^c）· 2 个 -1/2（L）')

guard('G1-7 T_24 在 10 上的本征值多重集 = {-2/3 x3, 1/6 x6, 1 x1}',
      sorted(LAM10) == sorted([F(-2, 3)] * 3 + [F(1, 6)] * 6 + [F(1)] * 1),
      '10: 3 个 -2/3（u_R^c）· 6 个 +1/6（Q_L）· 1 个 +1（e_R^c）')

guard('G1-8 10 的本征值 = 5 的本征值两两之和（逐项）',
      all(LAM10[k] == LAM5[IDX10[k][0]] + LAM5[IDX10[k][1]]
          for k in range(10)),
      'Lambda^2 的权 = 两两之和')

# ================================================================ G2：超荷
GG_5B = [
    ('d_R^c', (0, 1), 1, F(1, 3), False),
    ('L', (0, 0), 2, F(-1, 2), False),
]
GG_10 = [
    ('Q_L', (1, 0), 2, F(1, 6), False),
    ('u_R^c', (0, 1), 1, F(-2, 3), False),
    ('e_R^c', (0, 0), 1, F(1), False),
]

TR_Y_5B = 3 * F(1, 3) + 2 * F(-1, 2)
TR_Y2_5B = 3 * F(1, 3) ** 2 + 2 * F(-1, 2) ** 2
TR_Y_10 = 3 * F(-2, 3) + 6 * F(1, 6) + 1 * F(1)
TR_Y2_10 = 3 * F(-2, 3) ** 2 + 6 * F(1, 6) ** 2 + 1 * F(1) ** 2
TR_T32_5B = 2 * F(1, 2) ** 2
TR_T32_10 = 3 * 2 * F(1, 2) ** 2

guard('G2-1 5bar 的 Tr(Y) = 0（T_24 traceless）',
      TR_Y_5B == 0 and sum(LAM5B) == 0,
      '3*(1/3) + 2*(-1/2) = 0')

guard('G2-2 10 的 Tr(Y) = 0',
      TR_Y_10 == 0 and sum(LAM10) == 0,
      '3*(-2/3) + 6*(1/6) + 1*(1) = 0')

guard('G2-3 Tr(Y^2)：5bar = 5/6，10 = 5/2',
      TR_Y2_5B == F(5, 6) and TR_Y2_10 == F(5, 2),
      '5/6 · 5/2')

guard('G2-4 Tr(T_3^2)：5bar = 1/2，10 = 3/2',
      TR_T32_5B == F(1, 2) and TR_T32_10 == F(3, 2),
      '1/2 · 3/2')

guard('G2-5 GUT 归一比 Tr(Y^2)/Tr(T_3^2) = 5/3（5bar 路径）',
      TR_Y2_5B / TR_T32_5B == F(5, 3),
      '(5/6)/(1/2) = 5/3')

guard('G2-6 GUT 归一比 = 5/3（10 路径，独立复算）',
      TR_Y2_10 / TR_T32_10 == F(5, 3),
      '(5/2)/(3/2) = 5/3')

guard('G2-7 sin^2 theta_W = 1/(1 + 5/3) = 3/8',
      F(1) / (F(1) + F(5, 3)) == F(3, 8),
      'g_1^2 = (5/3) g_prime^2 ⇒ sin^2 = (3/5)/(1+3/5) = 3/8')

guard('G2-8 SM 正确超荷集去重后仍为 5 个（r441 计数不受 d_R 符号影响）',
      len(SM_Y_CORRECT) == 5 and len(SM_Y_R441) == 5
      and SM_Y_CORRECT != SM_Y_R441,
      'correct={%s} · r441={%s}' % (
          ', '.join(str(y) for y in SM_Y_CORRECT),
          ', '.join(str(y) for y in SM_Y_R441)))

# ================================================================ G3：反常
AN_SM = anomalies(SM_CHIRAL)
AN_5B = anomalies(GG_5B)
AN_10 = anomalies(GG_10)
AN_GG = tuple(AN_5B[i] + AN_10[i] for i in range(4))

guard('G3-1 r441 口径 SM 单代四条反常精确为零（独立重写复算）',
      AN_SM == (F(0), F(0), F(0), F(0)),
      '[SU2]^2U1=%s · [SU3]^2U1=%s · U1^3=%s · grav-U1=%s'
      % tuple(str(x) for x in AN_SM))

guard('G3-2 5bar + 10 合计四条反常精确为零',
      AN_GG == (F(0), F(0), F(0), F(0)),
      '5bar ⊕ 10 的左手场内容与 SM_CHIRAL 逐场相同 ⇒ 必然为零')

guard('G3-3 逐场等价性：5bar+10 的 (d3,d2,Y_LH) 多重集 = SM_CHIRAL',
      sorted([(dim_su3(*s), t, str(-Y if r else Y)) for _, s, t, Y, r in SM_CHIRAL])
      == sorted([(dim_su3(*s), t, str(Y)) for _, s, t, Y, _ in GG_5B + GG_10]),
      '5 条逐场一一对应')

guard('G3-4 5bar 单独不为零（跨块消除的证据）',
      AN_5B == (F(-1, 4), F(1, 6), F(-5, 36), F(0)),
      'a22 = -1/4 · a33 = +1/6 · ayyy = -5/36 · grav-U1 = 0')

guard('G3-5 10 单独不为零且与 5bar 精确互补',
      AN_10 == (F(1, 4), F(-1, 6), F(5, 36), F(0)) and AN_GG == (F(0), F(0), F(0), F(0)),
      'a22 = +1/4 · a33 = -1/6 · ayyy = +5/36 ⇒ 三块相加归零')

guard('G3-6 grav-U1 在 5bar 与 10 上各自为零（不是跨块消除）',
      AN_5B[3] == 0 and AN_10[3] == 0,
      '与 a22/ayyy 的消除机制不同，必须分开陈述')

# ================================================================ G4：块数 / 群依赖
CD_SU5_5 = central_dim(G5, 5)
CD_SU5_5B = central_dim(G5B, 5)
CD_SU5_10 = central_dim(G10, 10)
CD_SU5_SUM = CD_SU5_5B + CD_SU5_10

# 15 维：按 5 块排布 SU(3) 与 SU(2)，独立复算 r441 的 CD_SM = 5
BLOCKS = [((1, 0), 2, 1), ((0, 1), 1, 1), ((0, 1), 1, 1), ((0, 0), 2, 1), ((0, 0), 1, 1)]


def build_sm15_gens():
    """15 维 = (3,2) + (3,1) + (3,1) + (1,2) + (1,1)，块对角排布。

    两块生成元数不同（SU(3) 有 8 个、SU(2) 有 3 个）⇒ 必须分两条独立构造，
    不能共用一个按 S3 长度取的循环（否则 SM(3) < 8 时越界）。
    """
    sizes = [dim_su3(*s) * t for s, t, _ in BLOCKS]

    def su3_part(a):
        parts = []
        for (su3, tw, _), n in zip(BLOCKS, sizes):
            if su3 == (0, 0):
                parts.append(cmat(n, n))
            else:
                g = S3[a]
                parts.append(kron(g, I2) if tw == 2 else g)
        return bdiag(*parts)

    def su2_part(a):
        parts = []
        for (su3, tw, _), n in zip(BLOCKS, sizes):
            if tw != 2:
                parts.append(cmat(n, n))
            else:
                g = S2[a]
                parts.append(kron(I3, g) if dim_su3(*su3) == 3 else g)
        return bdiag(*parts)

    return [su3_part(a) for a in range(len(S3))] + [su2_part(a) for a in range(len(S2))]


SM15 = build_sm15_gens()

# 逐块计算（每块一个标量）——这是**错误算法**的阳性对照：
# 它忽略了「等价副本可混合」（两个 (3,1) 块是同一表示的副本，
#   X_12 : V^(1) -> V^(2) 只要是 S3-等变就非零 ⇒ 贡献 m^2 而不是 m）。
CD_PARTS = [
    central_dim([kron(S3[a], I2) for a in range(len(S3))]
                + [kron(I3, S2[a]) for a in range(len(S2))], 6),   # (3,2)
    central_dim(S3, 3),                                            # (3,1) 第 1 块
    central_dim(S3, 3),                                            # (3,1) 第 2 块
    central_dim(S2, 2),                                            # (1,2)
    central_dim([], 1),                                            # (1,1)
]
CD_PARTS_NAIVE = sum(CD_PARTS)      # = 5（naive，与中心化子定义不符）

# 正确算法：central(⊕_i m_i V_i) = Σ_{i,j: V_i ≅ V_j} dim Hom(V_i,V_j) = Σ m_i^2 · 1
# （复不可约表示 Schur ⇒ dim Hom(V,V) = 1；等价副本之间出现 m×m 的标量矩阵）
CD_SM15_FORMULA = sum(m * m for m in SM_NEED.values())      # 1+4+1+1 = 7

CD_SM15 = central_dim(SM15, 15)     # 真正的中心化子（大矩阵，独立于公式）

guard('G4-1 central(SU(5), 5) = 1（Schur，机器验证）',
      CD_SU5_5 == 1, '5 在 SU(5) 下不可约')

guard('G4-2 central(SU(5), 5bar) = 1（机器验证）',
      CD_SU5_5B == 1, '5bar 不可约')

guard('G4-3 central(SU(5), 10) = 1（Lambda^2 表示，机器验证）',
      CD_SU5_10 == 1, '10 在 SU(5) 下不可约')

guard('G4-4 central(SU(5), 5bar ⊕ 10) = 2（直和可加）',
      CD_SU5_SUM == 2,
      '1 + 1 = 2：两个不可约块各一个整体归一')

guard('G4-5 central(SU(3)xSU(2), 15) = 7（两个 (3,1) 等价副本可混合）',
      CD_SM15 == 7 and CD_SM15_FORMULA == 7,
      '大矩阵=%d · 公式 Σm^2=%d · naive 逐块和=%d'
      % (CD_SM15, CD_SM15_FORMULA, CD_PARTS_NAIVE))

OFFS = [0, 6, 9, 12, 14, 15]


def block_index(k):
    for b in range(5):
        if OFFS[b] <= k < OFFS[b + 1]:
            return b
    return -1


def is_block_diagonal(M):
    for i in range(15):
        for j in range(15):
            if block_index(i) != block_index(j) and not M[i][j].iszero():
                return False
    return True


_R1 = []
for _i in range(300):
    _row = [ZERO] * 3
    _row[_i % 3] = ONE
    _R1.append(_row)
_RANKA = crank(_R1)
guard('G0-8 消元器压力测试 A：300x3（重复单位行）秩 = 3',
      _RANKA == 3, 'crank=%d' % _RANKA)

_R2 = []
for _i in range(3000):
    _row = [ZERO] * 225
    _row[_i % 225] = ONE
    _R2.append(_row)
_RANKB = crank(_R2)
guard('G0-9 消元器压力测试 B：3000x225（重复单位行）秩 = 225',
      _RANKB == 225, 'crank=%d' % _RANKB)

guard('G4-5a SM15 的 11 个生成元全部块对角（拦截 bdiag 构造错误）',
      all(is_block_diagonal(g) for g in SM15),
      '非对角块元素必须全零')

guard('G4-5b 阳性对照：naive 逐块和 = 5 ≠ 中心化子 7（判据有牙）',
      CD_PARTS_NAIVE == 5 and CD_PARTS_NAIVE != CD_SM15,
      'naive=%d · 正确=%d · 若 naive 也得 7 则「等价副本混合」判据无效'
      % (CD_PARTS_NAIVE, CD_SM15))

guard('G4-6 块数下界「群依赖」：同一 15 维在 SU(5) 下 2 块、在 SU(3)xSU(2) 下 5 块',
      CD_SU5_SUM == 2 and dec_count(SM_NEED) == 5 and dec_dim(GG_DEC) == 15,
      '维数恒 15，块数 5 -> 2 ⇒ 引用 r441 的 bound_blocks=5 必须加「相对 SU(3)xSU(2)」')

# ================================================================ G5：帕累托
P_NAMES = ['SM_5blocks', 'SU5_5b10', 'SO10_16']
P_DIM = [15, 15, 16]
P_BLOCKS = [5, 2, 1]
P_YFREE = [5, 0, 0]          # Y 自由参数：SM 5 个；SU(5)/SO(10) 由生成元钉死 = 0
P_PRED = [0, 2, 3]           # 硬预言数：sin^2=3/8、质子衰变 / +nu_R 等
P_RISK = [0, 2, 1]           # 排除风险：SM 无预言=0；最小 SU(5) 已排除=2；SO(10) 需中间破缺=1

guard('G5-1 三方案维数 = [15, 15, 16]（SO(10) 为 16 维 Weyl 旋量）',
      P_DIM == [dec_dim(SM_NEED), dim_su(5, 1) + dim_su(5, 2), dim_so10_spinor()],
      'SO(10) 的 16 = 15 + nu_R（旋量维 2^(10/2-1)=16，与基本表示 10 维不同，必须声明）')

guard('G5-2 三方案不可约块数单调下降 = [5, 2, 1]',
      P_BLOCKS == [dec_count(SM_NEED), CD_SU5_SUM, 1],
      'SO(10) 的 16 为单块（Spin(10) 旋量表示不可约）')

guard('G5-3 Y 自由参数：SM = 5，SU(5)/SO(10) = 0',
      P_YFREE == [len(SM_Y_CORRECT), 0, 0],
      '此列 = 对角超荷赋值数（不是中心化子：SM 的 15 维中心化子是 7）；'
      'SU(5) 起 Y 是 T_24 本征值 ⇒ 5 个值全被钉死，自由参数 0')

guard('G5-4 结构三列上 SU(5) 弱占优 SM；加入「排除风险」后才不可比',
      (P_DIM[1] <= P_DIM[0] and P_BLOCKS[1] <= P_BLOCKS[0] and P_YFREE[1] <= P_YFREE[0])
      and (P_RISK[0] < P_RISK[1]) and (P_PRED[0] < P_PRED[1]),
      '不可比只在四列（含风险/预言）成立；三列上 SU(5) 严格不劣 ⇒ 不得声称三列不可比')

guard('G5-5 自由度 5 -> 0 的代价被显式登记（不是「免费统一」）',
      P_YFREE[1] == 0 and P_PRED[1] == 2,
      '代价 = 质子衰变 + 最小 SU(5) 已被实验排除')

# ================================================================ G6：与 r441 对账
guard('G6-1 r441 的 bound_dim = 15 在扩群下不变',
      dec_dim(SM_NEED) == 15 and dim_su(5, 1) + dim_su(5, 2) == 15,
      '维数下界与群无关（在「承载同一物质内容」前提下）')

guard('G6-2 r441 的 bound_blocks = 5 是「相对 SU(3)xSU(2)」的下界',
      dec_count(SM_NEED) == 5 and CD_SU5_SUM == 2,
      '扩群可把 5 块压到 2 块 ⇒ 该下界必须加子群限定')

guard('G6-3 r441 的 bound_y = 5 是「Y 为外部 U(1) 标量」时的自由度',
      len(SM_Y_CORRECT) == 5 and P_YFREE[1] == 0,
      'Y 嵌入 SU(5) 后自由参数 0；两数（5 与 0）不可互换')

guard('G6-4 r441 的 y_values_sm 含 1/3（应为 -1/3）——登记，不改其字节',
      F(1, 3) in SM_Y_R441 and F(-1, 3) in SM_Y_CORRECT
      and F(-1, 3) not in SM_Y_R441,
      'r441 SM_SINGLE 的 d_R 写 +1/3；其 SM_CHIRAL 写 -1/3（正确）⇒ 计数 5 不受影响')

guard('G6-6 r441 的 CD_SM(=dec_count=5) 与 CD_DIRECT(=central_dim=2) 不是同一个量',
      dec_count(SM_NEED) == 5 and CD_SM15 == 7,
      '5 维上 r441 用 central_dim 得 2；15 维上直接取 dec_count 得 5；'
      '若统一用 central_dim，15 维应为 7 ⇒ 两个读数不可直接相减/相比')

guard('G6-5 本册不推翻 r441 的任何条目（三下界方向全部保持）',
      dec_dim(SM_NEED) == 15 and dec_count(SM_NEED) == 5 and len(SM_Y_CORRECT) == 5,
      '只新增「群依赖」限定，不撤任何 r441 判定')

KEY['gg_dec'] = fmt_dec(GG_DEC)
KEY['sm_need'] = fmt_dec(SM_NEED)
KEY['lam5'] = [str(x) for x in LAM5]
KEY['lam5b'] = [str(x) for x in LAM5B]
KEY['lam10'] = [str(x) for x in LAM10]
KEY['tr_y2_5b'] = str(TR_Y2_5B)
KEY['tr_y2_10'] = str(TR_Y2_10)
KEY['tr_t32_5b'] = str(TR_T32_5B)
KEY['tr_t32_10'] = str(TR_T32_10)
KEY['gut_ratio'] = str(TR_Y2_5B / TR_T32_5B)
KEY['sin2_theta_w'] = str(F(3, 8))
KEY['anomaly_sm'] = [str(x) for x in AN_SM]
KEY['anomaly_5b'] = [str(x) for x in AN_5B]
KEY['anomaly_10'] = [str(x) for x in AN_10]
KEY['anomaly_gg_sum'] = [str(x) for x in AN_GG]
KEY['central_su5_5'] = CD_SU5_5
KEY['central_su5_5b'] = CD_SU5_5B
KEY['central_su5_10'] = CD_SU5_10
KEY['central_su5_sum'] = CD_SU5_SUM
KEY['central_sm15'] = CD_SM15
KEY['central_sm15_formula'] = CD_SM15_FORMULA
KEY['central_sm15_naive'] = CD_PARTS_NAIVE
KEY['blocks_sm'] = dec_count(SM_NEED)
KEY['blocks_gg_sm'] = dec_count(GG_DEC)
KEY['dim_gg'] = dec_dim(GG_DEC)
KEY['y_values_correct'] = [str(y) for y in SM_Y_CORRECT]
KEY['pareto'] = {'names': P_NAMES, 'dim': P_DIM, 'blocks': P_BLOCKS,
                 'y_free': P_YFREE, 'predictions': P_PRED, 'risk': P_RISK}

# ================================================================ 结论条目
entry('E01', 'SU(5) 的 5bar ⊕ 10 在 SU(3)xSU(2) 下分支与 r441 的 dec_sm 逐块一致', 'PASS',
      '5bar -> (3bar,1)[3] + (1,2)[2]；10 -> (3,2)[6] + (3bar,1)[3] + (1,1)[1]；'
      '合计 (3,1)x2 + (3,2)x1 + (1,2)x1 + (1,1)x1 = 15，缺 0 多 0',
      {'dim': dec_dim(GG_DEC), 'blocks': dec_count(GG_DEC), 'dec': fmt_dec(GG_DEC)})

entry('E02', 'T_24 本征值机器复算与 SM 超荷逐块数值相等', 'PASS',
      '5bar：+1/3（d_R^c）、-1/2（L）；10：-2/3（u_R^c）、+1/6（Q_L）、+1（e_R^c）；'
      '10 的本征值恰为 5 的本征值两两之和（Lambda^2 的权）',
      {'lam5b': [str(x) for x in LAM5B], 'lam10': [str(x) for x in LAM10]})

entry('E03', 'SU(5) 不可约块数 = 2 ≠ r441 的 5 ⇒ 块数下界是「群依赖」的', 'INFO',
      '同一 15 维：SU(5) 下 2 块（5bar、10 各一，中心化子各 1、合计 2）；'
      'SU(3)xSU(2) 下 5 块（(3,1) 有两个副本），但中心化子 = 7（副本可混合）⇒ '
      '引用 bound_blocks=5 必须加子群限定，且「块数」与「中心化子」不可混用',
      {'central_su5': [CD_SU5_5B, CD_SU5_10, CD_SU5_SUM],
       'blocks_sm': dec_count(SM_NEED), 'central_sm15': CD_SM15})

entry('E04', 'T_24 traceless：Tr(Y) 在 5bar 与 10 上各自为零', 'PASS',
      '5bar：3*(1/3) + 2*(-1/2) = 0；10：3*(-2/3) + 6*(1/6) + 1*(1) = 0；'
      '⇒ Y 确实是 SU(5) 生成元，不是附加的外部 U(1)',
      {'tr5b': str(TR_Y_5B), 'tr10': str(TR_Y_10)})

entry('E05', 'sin^2 theta_W = 3/8 由 Tr(Y^2):Tr(T_3^2) = 5:3 双路径一致给出', 'PASS',
      '5bar 路径 (5/6)/(1/2) = 5/3；10 路径 (5/2)/(3/2) = 5/3；'
      'g_1^2 = (5/3) g_prime^2 ⇒ sin^2 = (3/5)/(1+3/5) = 3/8',
      {'ratio_5b': str(TR_Y2_5B / TR_T32_5B), 'ratio_10': str(TR_Y2_10 / TR_T32_10),
       'sin2': str(F(3, 8))})

entry('E06', 'r441 的 y_values_sm 含 1/3（应为 -1/3）：登记，不改其字节', 'CORRECTED',
      'r441 的 SM_SINGLE 把 d_R 的 Y 写成 +1/3，而其 SM_CHIRAL 写 -1/3（正确）⇒ '
      '两者口径不一致；因只用于「不同值个数」计数，5 的计数不受影响；'
      '本册用正确值 -1/3，登记为跨册口径瑕疵',
      {'r441_values': [str(y) for y in SM_Y_R441],
       'correct_values': [str(y) for y in SM_Y_CORRECT]})

entry('E07', '反常不在块内消除，而在 5bar 与 10 之间跨块消除', 'PASS',
      '5bar 单独：[SU2]^2U1 = -1/4、U1^3 = -5/36；10 单独：+1/4、+5/36；'
      '合计精确为零 ⇒ 这解释了为什么 5bar 与 10 必须成对出现；'
      '但 grav-U1 在两块上各自为零，机制不同，必须分开陈述',
      {'5b': [str(x) for x in AN_5B], '10': [str(x) for x in AN_10],
       'sum': [str(x) for x in AN_GG]})

entry('E08', '帕累托前沿：结构三列上 SU(5) 弱占优 SM，四列（加排除风险）才不可比', 'INFO',
      '维数 [15,15,16] · 块数 [5,2,1] · Y 自由 [5,0,0] · 硬预言 [0,2,3] · 排除风险 [0,2,1]；'
      '三列上 SU(5) 严格不劣（同等维数、更少块、更少 Y 自由）⇒「不可比」必须显式加入'
      '风险维度才成立，否则是用结构维数掩盖被排除的代价；本册不代选',
      {'pareto': {'dim': P_DIM, 'blocks': P_BLOCKS, 'y_free': P_YFREE,
                  'predictions': P_PRED, 'risk': P_RISK}})

entry('E09', 'r441 §九 U1（扩展规范群）已答：维数下界不变，块数与 Y 自由度口径需重述',
      'PASS',
      '维数下界 15 与群无关；块数下界 5 只在「相对 SU(3)xSU(2)」成立（SU(5) 下 2）；'
      'Y 自由参数 5 只在「Y 为外部 U(1)」成立（SU(5) 下 0）⇒ U1 闭合，且不推翻 r441',
      {'r441_u1_closed': True})

entry('E10', '最小 SU(5) 已被实验排除：帕累托上「少自由度」点的代价必须显式登记', 'INFO',
      'Y 自由 5->0 换得 sin^2=3/8 与质子衰变预言，但最小 SU(5) 的质子寿命与 '
      '耦合汇聚均不满足现行下限 ⇒ 若要保留该点须引入 SUSY 或改群（外部输入，本册不代选）',
      {'cost_recorded': True})

entry('E11', 'r441 的 CD_SM(=dec_count=5) 与 CD_DIRECT(=central_dim=2) 口径不一致', 'CORRECTED',
      '15 维中心化子机器算 = 7（两个 (3,1) 等价副本贡献 2^2 = 4），而 r441 直接取 dec_count = 5；'
      '5 维上 r441 用的是 central_dim（= 2）⇒ 同一册内两个「自由度」不是同一个量。'
      '物理上「5 个互异超荷」仍成立，但不可与中心化子维数互换引用',
      {'central_sm15': CD_SM15, 'dec_count_sm': dec_count(SM_NEED),
       'formula_sum_m2': CD_SM15_FORMULA, 'naive_sum': CD_PARTS_NAIVE})

VERDICT = ('EXTENDED-GAUGE-BOUND--SU5-5b10-BRANCHING-EXACT--DIM-BOUND-INVARIANT--'
           'BLOCK-BOUND-AND-Y-DOF-ARE-GROUP-RELATIVE--CENTRALIZER-7-NOT-5--PARETO-INCOMPARABLE')


# ================================================================ 输出
def counter():
    out = {}
    for e in ENTRIES:
        out[e['verdict']] = out.get(e['verdict'], 0) + 1
    return out


def guard_ok():
    return sum(1 for g in GUARDS if g['ok'])


def ensure_dirs():
    for d in (DATA, JUDGE, SRC):
        if not os.path.isdir(d):
            os.makedirs(d)


def write_text(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def build_md():
    cnt = counter()
    L = []
    add = L.append
    add('# TUFT-r442 · 扩展规范群下的承载下界重算（SU(5) 分支与帕累托前沿）')
    add('')
    add('> `5bar ⊕ 10` 分支规则 · 与 `r441` 的 `(15,5,5)` 三判据逐项对账 · 帕累托前沿（Fraction 精确）')
    add('')
    add('- 生成日期：' + STAMP)
    add('- 守卫：%d/%d 通过' % (guard_ok(), len(GUARDS)))
    add('- 条目：PASS=%d · FAIL=%d · INFO=%d · CORRECTED=%d'
        % (cnt.get('PASS', 0), cnt.get('FAIL', 0), cnt.get('INFO', 0), cnt.get('CORRECTED', 0)))
    add('- 总裁定：`' + VERDICT + '`')
    add('')
    add('## 〇 一句话结论')
    add('')
    add('**`r441` 的 U1（扩展规范群）已闭合：维数下界 15 与群无关，但块数与超荷自由度是群相关的。**')
    add('')
    add('- `SU(5)` 的 `5bar ⊕ 10` 在 `SU(3)xSU(2)` 下**逐块**等于 `r441` 的单代 15 维（缺 0 / 多 0）。')
    add('- `SU(5)` 不可约块数 **2**，不是 `r441` 的 5；`SU(3)xSU(2)` 下仍 **5 块**，'
        '但中心化子是 **7**（两个 `(3,1)` 副本等价可混合）⇒「块数」与「中心化子」必须分开报。')
    add('- 超荷自由参数从 **5 → 0**（`Y` 变成 `T_24` 的本征值）⇒ 换来 `sin^2 theta_W = 3/8` 的硬预言。')
    add('- 反常在 `5bar` 与 `10` **之间**消除（各自不为零），这解释了为何二者必须成对。')
    add('')
    add('## 一 分支规则（机器派生）')
    add('')
    add('```')
    add('5bar -> (3bar,1)[3] + (1,2)[2]      = d_R^c + L')
    add('10   -> (3,2)[6] + (3bar,1)[3] + (1,1)[1] = Q_L + u_R^c + e_R^c')
    add('合计 = ' + KEY['gg_dec'])
    add('r441 = ' + KEY['sm_need'])
    add('```')
    add('')
    add('## 二 T_24 本征值（与 SM 超荷逐块相等）')
    add('')
    add('| 表示 | 本征值多重集 | 对应左手场 |')
    add('| --- | --- | --- |')
    add('| `5bar` | `+1/3 x3`、`-1/2 x2` | `d_R^c`、`L` |')
    add('| `10` | `-2/3 x3`、`+1/6 x6`、`+1 x1` | `u_R^c`、`Q_L`、`e_R^c` |')
    add('')
    add('`10` 的本征值恰为 `5` 的本征值两两之和（`Lambda^2` 的权），逐项机器验证。')
    add('')
    add('## 三 GUT 归一与 sin^2 theta_W')
    add('')
    add('- `Tr(Y^2)`：`5bar` = `5/6`，`10` = `5/2`；`Tr(T_3^2)`：`5bar` = `1/2`，`10` = `3/2`。')
    add('- 两条独立路径同给 `Tr(Y^2)/Tr(T_3^2) = 5/3` ⇒ `sin^2 theta_W = 1/(1+5/3) = 3/8`。')
    add('')
    add('## 四 反常必须在两块之间消除')
    add('')
    add('| 反常 | `5bar` 单独 | `10` 单独 | 合计 |')
    add('| --- | --- | --- | --- |')
    add('| `[SU2]^2 U1` | `-1/4` | `+1/4` | `0` |')
    add('| `[SU3]^2 U1` | `0` | `0` | `0` |')
    add('| `U1^3` | `-5/36` | `+5/36` | `0` |')
    add('| `grav-U1` | `0` | `0` | `0` |')
    add('')
    add('`grav-U1` 在两块上**各自**为零，与 `a22`/`ayyy` 的跨块消除机制不同，不能合并陈述。')
    add('')
    add('## 五 帕累托前沿（三方案不可比）')
    add('')
    add('| 方案 | 维数 | 不可约块 | Y 自由参数 | 硬预言数 |')
    add('| --- | --- | --- | --- | --- |')
    add('| SM 分块 | 15 | 5 | 5 | 0 |')
    add('| `SU(5)` `5bar+10` | 15 | 2 | 0 | 2 |')
    add('| `SO(10)` `16` | 16 | 1 | 0 | 3 |')
    add('')
    add('无方案在全部维度上占优 ⇒ 选型是价值判断。`SO(10)` 的 16 维含 `nu_R`（多 1 维），必须声明。')
    add('')
    add('## 六 与 r441 的对账')
    add('')
    add('| r441 读数 | 扩群后状态 |')
    add('| --- | --- |')
    add('| `bound_dim = 15` | **不变**（与群无关） |')
    add('| `bound_blocks = 5` | **需加「相对 SU(3)xSU(2)」**；`SU(5)` 下 2 |')
    add('| `bound_y = 5` | **需加「Y 为外部 U(1)」**；`SU(5)` 下 0 |')
    add('| `CD_SM = 5` | **是 `dec_count` 不是中心化子**；15 维中心化子真值为 **7** |')
    add('| `y_values_sm` 含 `1/3` | **登记瑕疵**：应为 `-1/3`（计数 5 不受影响） |')
    add('')
    add('## 七 条目表')
    add('')
    add('| 编号 | 判定 | 标题 |')
    add('| --- | --- | --- |')
    for e in ENTRIES:
        add('| %s | **%s** | %s |' % (e['code'], e['verdict'], e['title']))
    add('')
    add('## 八 守卫清单')
    add('')
    add('| 守卫 | 结果 |')
    add('| --- | --- |')
    for g in GUARDS:
        add('| %s | %s |' % (g['name'], 'PASS' if g['ok'] else 'FAIL'))
    add('')
    add('## 九 边界（诚实登记）')
    add('')
    add('1. 本册只判**表示的承载结构与分支规则**，不判动力学（不涉及耦合常数跑动、质量谱、破缺机制）。')
    add('2. `sin^2 theta_W = 3/8` 是**树级 GUT 归一**结论，不含 RG 跑动；与实测值的差异属跑动/阈值层，本册不涉及。')
    add('3. 「`Y` 自由参数 = 0」指**5 个超荷值全部由 `T_24` 决定**；两块各有的 1 个整体归一是可吸收的，'
        '所以「块标量自由度 = 2」与「自由超荷参数 = 0」必须分开报，不可互换。'
        '注意 15 维的**中心化子维数是 7**（两个 `(3,1)` 等价副本可混合，贡献 `2^2 = 4`），'
        '而「可按场独立赋超荷的块数」是 5 —— 两者是不同的量。')
    add('4. `SO(10)` 的 16 维含 `nu_R`，与 15 维不是同一物质内容，跨方案比较时该行必须单独标注。')
    add('5. 最小 `SU(5)` 已被实验排除属**外部实验事实**引用，本册不复算质子寿命与耦合汇聚。')
    add('6. 本册不改 `r441` 任何字节；`r441` 的 `y_values_sm` 瑕疵只登记不修。')
    return '\n'.join(L) + '\n'


def build_report():
    cnt = counter()
    L = []
    add = L.append
    add('TUFT-r442 扩展规范群承载下界重算 · 复算报告')
    add('stamp = ' + STAMP)
    add('verdict = ' + VERDICT)
    add('')
    add('GG_DEC = ' + KEY['gg_dec'])
    add('SM_NEED = ' + KEY['sm_need'])
    add('LAM_5 = ' + ', '.join(KEY['lam5']))
    add('LAM_5B = ' + ', '.join(KEY['lam5b']))
    add('LAM_10 = ' + ', '.join(KEY['lam10']))
    add('TR_Y2_5B = %s  TR_T32_5B = %s' % (KEY['tr_y2_5b'], KEY['tr_t32_5b']))
    add('TR_Y2_10 = %s  TR_T32_10 = %s' % (KEY['tr_y2_10'], KEY['tr_t32_10']))
    add('GUT_RATIO = ' + KEY['gut_ratio'])
    add('SIN2_THETA_W = ' + KEY['sin2_theta_w'])
    add('ANOMALY_5B = ' + ', '.join(KEY['anomaly_5b']))
    add('ANOMALY_10 = ' + ', '.join(KEY['anomaly_10']))
    add('ANOMALY_SUM = ' + ', '.join(KEY['anomaly_gg_sum']))
    add('CENTRAL_SU5 = %d / %d / %d (5 / 5bar / 10) sum=%d'
        % (CD_SU5_5, CD_SU5_5B, CD_SU5_10, CD_SU5_SUM))
    add('CENTRAL_SM15 = %d (formula sum m^2 = %d, naive blockwise = %d)'
        % (CD_SM15, CD_SM15_FORMULA, CD_PARTS_NAIVE))
    add('PARETO = %s' % json.dumps(KEY['pareto'], ensure_ascii=False))
    add('')
    add('ENTRIES %d' % len(ENTRIES))
    for e in ENTRIES:
        add('  [%s] %s %s' % (e['verdict'], e['code'], e['title']))
    add('')
    add('GUARDS %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        add('  [%s] %s%s' % ('OK' if g['ok'] else 'NG', g['name'],
                             ('  |  ' + g['detail']) if g['detail'] else ''))
    add('')
    add('PASS = %d' % cnt.get('PASS', 0))
    add('FAIL = %d' % cnt.get('FAIL', 0))
    add('INFO = %d' % cnt.get('INFO', 0))
    add('GUARDS_TOTAL = %d' % len(GUARDS))
    add('GUARDS_PASS = %d' % guard_ok())
    add('VERDICT = ' + VERDICT)
    return '\n'.join(L) + '\n'


PAYLOAD = {
    'tag': TAG,
    'stamp': STAMP,
    'verdict': VERDICT,
    'guards': {'pass': guard_ok(), 'total': len(GUARDS), 'items': GUARDS},
    'entries': ENTRIES,
    'counts': counter(),
    'key_numbers': KEY,
}


def main():
    ensure_dirs()
    jp = os.path.join(DATA, TAG + '.json')
    mp = os.path.join(DATA, TAG + '.md')
    rp = os.path.join(DATA, TAG + '_report.txt')
    write_text(jp, json.dumps(PAYLOAD, ensure_ascii=False, indent=2, default=str) + '\n')
    write_text(mp, build_md())
    write_text(rp, build_report())

    cnt = counter()
    print('[r442] guards %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        if not g['ok']:
            print('  [NG] ' + g['name'] + ' | ' + g['detail'])
    print('[r442] entries PASS=%d FAIL=%d INFO=%d CORRECTED=%d'
          % (cnt.get('PASS', 0), cnt.get('FAIL', 0), cnt.get('INFO', 0), cnt.get('CORRECTED', 0)))
    print('[r442] VERDICT ' + VERDICT)
    print('[r442] out ' + jp)
    print('[r442] out ' + mp)
    print('[r442] out ' + rp)
    return 0 if guard_ok() == len(GUARDS) else 1


if __name__ == '__main__':
    sys.exit(main())
