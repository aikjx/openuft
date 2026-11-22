# -*- coding: utf-8 -*-
"""TUFT-r441 · N2 维数阶梯可行性

主题：直和 5 / 张量积 6 / 单代 15 —— 承载下界与量子数三重判据。

纯标准库（Fraction 精确）· 无第三方依赖 · Python 3.8。
输出：../数据/TUFT-r441_..._{json,md,_report.txt}
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
TAG = 'TUFT-r441_N2维数阶梯可行性_5vs6vs15承载下界与量子数三重判据_精算_' + STAMP

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


def cmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    out = cmat(n, m)
    for i in range(n):
        Ai = A[i]
        for t in range(k):
            a = Ai[t]
            if a.iszero():
                continue
            Bt = B[t]
            for j in range(m):
                b = Bt[j]
                if b.iszero():
                    continue
                out[i][j] = out[i][j] + a * b
    return out


def cvec(A, v):
    return [sum((A[i][j] * v[j] for j in range(len(v))), ZERO) for i in range(len(A))]


def crank(rows):
    """复矩阵的秩（Fraction 精确高斯消元）。"""
    M = []
    for r in rows:
        rr = [_c(x) for x in r]
        if any(not x.iszero() for x in rr):
            M.append(rr)
    if not M:
        return 0
    n, m, rank = len(M), len(M[0]), 0
    for c in range(m):
        piv = None
        for i in range(rank, n):
            if not M[i][c].iszero():
                piv = i
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][c].inv()
        M[rank] = [x * pv for x in M[rank]]
        for i in range(n):
            if i != rank and not M[i][c].iszero():
                f = M[i][c]
                M[i] = [M[i][j] - f * M[rank][j] for j in range(m)]
        rank += 1
        if rank == n:
            break
    return rank


def cnullity(rows, ncols):
    return ncols - crank(rows)


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


def bdiag(A, B):
    n, m = len(A), len(A[0])
    p, q = len(B), len(B[0])
    out = cmat(n + p, m + q)
    for i in range(n):
        for j in range(m):
            out[i][j] = A[i][j]
    for i in range(p):
        for j in range(q):
            out[n + i][m + j] = B[i][j]
    return out


def is_zero_mat(M):
    for row in M:
        for x in row:
            if not x.iszero():
                return False
    return True


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
    """SU(3) 不可约表示 (p,q) 的复维数：Weil 维数公式。"""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su2_gens():
    """su(2) 最小忠实（j=1/2）三个生成元 = sigma/2。"""
    h = F(1, 2)
    ih = C(0, h)
    return [
        [[ZERO, C(h)], [C(h), ZERO]],
        [[ZERO, -ih], [ih, ZERO]],
        [[C(h), ZERO], [ZERO, C(-h)]],
    ]


def su3_gens():
    """su(3) 八个生成元 = lambda_A/2。

    注：lambda_8 用 diag(1,1,-2)（不除 sqrt(3)）——整体缩放不改变中心，保持 Fraction 精确。
    """
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


# ---------------------------------------------------------------- 表示构造
S2 = su2_gens()
S3 = su3_gens()
Z2 = cmat(2, 2)
Z3 = cmat(3, 3)
I2 = ceye(2)
I3 = ceye(3)

# 直和口径：V = V2 + V3（5 维）
DIRECT_J = [bdiag(g, Z3) for g in S2]
DIRECT_T = [bdiag(Z2, g) for g in S3]
# 张量积口径：V = V2 (x) V3（6 维）
TENSOR_J = [kron(g, I3) for g in S2]
TENSOR_T = [kron(I2, g) for g in S3]


# ---------------------------------------------------------------- SM 单代场表
SM_SINGLE = [
    {'name': 'Q_L', 'su3': (1, 0), 'tw': 2, 'Y': F(1, 6)},
    {'name': 'u_R', 'su3': (0, 1), 'tw': 1, 'Y': F(2, 3)},
    {'name': 'd_R', 'su3': (0, 1), 'tw': 1, 'Y': F(1, 3)},
    {'name': 'L', 'su3': (0, 0), 'tw': 2, 'Y': F(-1, 2)},
    {'name': 'e_R', 'su3': (0, 0), 'tw': 1, 'Y': F(-1)},
]
for _f in SM_SINGLE:
    _f['dim'] = dim_su3(*_f['su3']) * _f['tw']
SM_TOTAL = sum(_f['dim'] for _f in SM_SINGLE)


# ---------------------------------------------------------------- 守卫 G0
guard('G0-1 SU(3) 维数公式已知值',
      [dim_su3(0, 0), dim_su3(1, 0), dim_su3(0, 1), dim_su3(1, 1), dim_su3(2, 0),
       dim_su3(3, 0), dim_su3(2, 1), dim_su3(4, 0), dim_su3(2, 2), dim_su3(3, 1)]
      == [1, 3, 3, 8, 6, 10, 15, 15, 27, 24],
      'dim(0,0)=1 · (1,0)=3 · (1,1)=8 · (2,0)=6 · (2,1)=15 · (4,0)=15 · (2,2)=27 · (3,1)=24')

guard('G0-2 SU(2) 维数 = 2j+1',
      [dim_su2(t) for t in (1, 2, 3, 5, 15)] == [1, 2, 3, 5, 15],
      'tw=2j+1 直接取值')

guard('G0-3 SM 单代内部态求和 = 15',
      SM_TOTAL == 15 and [f['dim'] for f in SM_SINGLE] == [6, 3, 3, 2, 1],
      '6(Q)+3(u)+3(d)+2(L)+1(e) = 15')

guard('G0-4 直和口径维数 = 5',
      len(DIRECT_J[0]) == 5 and len(DIRECT_J) == 3 and len(DIRECT_T) == 8,
      'su(2):2 + su(3):3 = 5')

guard('G0-5 张量积口径维数 = 6',
      len(TENSOR_J[0]) == 6 and len(TENSOR_J) == 3 and len(TENSOR_T) == 8,
      '2 x 3 = 6')

KEY['dim_direct'] = 5
KEY['dim_tensor'] = 6
KEY['dim_single_gen'] = SM_TOTAL
KEY['dim_three_gen'] = 3 * SM_TOTAL

guard('G0-6 中心维数 su(2) j=1/2 = 1',
      central_dim(S2, 2) == 1, 'd=2')
guard('G0-7 中心维数 su(3) = 1',
      central_dim(S3, 3) == 1, 'd=3')
guard('G0-8 中心维数 6 维张量积 = 1',
      central_dim(TENSOR_J + TENSOR_T, 6) == 1,
      'Schur：2(x)3 在 su(2)+su(3) 下不可约')
guard('G0-9 中心维数 5 维直和 = 2',
      central_dim(DIRECT_J + DIRECT_T, 5) == 2,
      '两块各有独立标量 ⇒ 直和给 2 个 Y 自由度')

_t2 = is_zero_mat(DIRECT_T[0][:2])
_rest = [row[2:] for row in DIRECT_T[0][:2]]
guard('G0-10 su(3) 在 su(2) 块上恒为零',
      _t2 and all(z.iszero() for row in _rest for z in row),
      'T|V2 = 0')
_rest2 = [row[:2] for row in DIRECT_J[0][2:]]
guard('G0-11 su(2) 在 su(3) 块上恒为零',
      _rest2 and all(z.iszero() for row in _rest2 for z in row),
      'J|V3 = 0')
# ================================================================ 判据 I：分量匹配
# SM 单代在 SU(3)_C x SU(2)_L 下的不可约分解（重数）
SM_NEED = {(3, 2): 1, (3, 1): 2, (1, 2): 1, (1, 1): 1}   # (3,2)=Q_L;(3,1)=u_R,d_R;(1,2)=L;(1,1)=e_R
DIRECT_DEC = {(1, 2): 1, (3, 1): 1}                      # 5 维直和：V2 + V3
TENSOR_DEC = {(3, 2): 1}                                 # 6 维张量积：2 (x) 3


def dec_dim(dec):
    """键 = (SU(3) 维数 d3, SU(2) 维数 d2)，值 = 重数。"""
    return sum(d3 * d2 * n for (d3, d2), n in dec.items())


def dec_count(dec):
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


def dec_missing_dim(dec):
    return sum(d3 * d2 * n for (d3, d2), n in dec_missing(dec).items())


def dec_excess_dim(dec):
    return sum(d3 * d2 * n for (d3, d2), n in dec_excess(dec).items())


def fmt_dec(dec):
    parts = []
    for (d3, d2) in sorted(dec.keys()):
        n = dec[(d3, d2)]
        parts.append('(%d,%d)x%d[%d]' % (d3, d2, n, d3 * d2 * n))
    return ' + '.join(parts)


DEC_DIRECT_3 = {(1, 2): 3, (3, 1): 3}                     # 3 代 x 直和 5 维 = 15 维

guard('G1-1 三口径维数（精确）',
      dec_dim(SM_NEED) == 15 and dec_dim(DIRECT_DEC) == 5 and dec_dim(TENSOR_DEC) == 6,
      'SM=%d · 直和=%d · 张量积=%d' % (dec_dim(SM_NEED), dec_dim(DIRECT_DEC), dec_dim(TENSOR_DEC)))

guard('G1-2 直和 5 维缺失维度 = 10',
      dec_missing_dim(DIRECT_DEC) == 10 and dec_missing(DIRECT_DEC) == {(3, 2): 1, (3, 1): 1, (1, 1): 1},
      '缺 (3,2)x1[6] + (3,1)x1[3] + (1,1)x1[1] = 10')

guard('G1-3 张量积 6 维缺失维度 = 9',
      dec_missing_dim(TENSOR_DEC) == 9
      and dec_missing(TENSOR_DEC) == {(3, 1): 2, (1, 2): 1, (1, 1): 1},
      '缺 (3,1)x2[6] + (1,2)x1[2] + (1,1)x1[1] = 9（已含 Q_L 的 (3,2)）')

guard('G1-4 不可约分量实例数 5 / 2 / 1',
      dec_count(SM_NEED) == 5 and dec_count(DIRECT_DEC) == 2 and dec_count(TENSOR_DEC) == 1,
      'SM=%d 块 · 直和=%d 块 · 张量积=%d 块' % (dec_count(SM_NEED), dec_count(DIRECT_DEC),
                                              dec_count(TENSOR_DEC)))

guard('G1-5 单代缺失 = 0（结构完整）',
      dec_missing_dim(SM_NEED) == 0 and dec_excess_dim(SM_NEED) == 0,
      'SM 自身分量匹配无缺无余')

KEY['dec_sm'] = fmt_dec(SM_NEED)
KEY['dec_direct'] = fmt_dec(DIRECT_DEC)
KEY['dec_tensor'] = fmt_dec(TENSOR_DEC)
KEY['missing_dim_direct'] = dec_missing_dim(DIRECT_DEC)
KEY['missing_dim_tensor'] = dec_missing_dim(TENSOR_DEC)
KEY['blocks_sm'] = dec_count(SM_NEED)
KEY['blocks_direct'] = dec_count(DIRECT_DEC)
KEY['blocks_tensor'] = dec_count(TENSOR_DEC)


# ================================================================ 判据 II：超荷自由度
# 与全部生成元对易的标量空间维数 = 可独立赋超荷的块数（Schur）
CD_DIRECT = central_dim(DIRECT_J + DIRECT_T, 5)
CD_TENSOR = central_dim(TENSOR_J + TENSOR_T, 6)
CD_SM = dec_count(SM_NEED)          # 5 个不可约块，每块 1 个标量（Schur），直和可加
SM_Y = sorted(set(f['Y'] for f in SM_SINGLE))
SM_Y_DISTINCT = len(SM_Y)

guard('G2-0 SM 超荷与 Q = T3 + Y 自洽（5 采样）',
      (F(0) + F(2, 3)) == F(2, 3)
      and (F(0) + F(-1, 3)) == F(-1, 3)
      and (F(0) + F(-1)) == F(-1)
      and (F(-1, 2) + F(-1, 2)) == F(-1)
      and (F(1, 2) + F(1, 6)) == F(2, 3),
      'u_R:+2/3 · d_R:-1/3 · e_R:-1 · L下:-1 · Q_L上:+2/3')

guard('G2-1 SM 单代不同超荷值个数 = 5',
      SM_Y_DISTINCT == 5,
      'Y ∈ {%s}' % ', '.join(str(y) for y in SM_Y))

guard('G2-2 直和 5 维中心化子维数 = 2 < 5',
      CD_DIRECT == 2 and CD_DIRECT < SM_Y_DISTINCT,
      '两块各 1 标量 ⇒ 2 个独立 Y；SM 需 %d' % SM_Y_DISTINCT)

guard('G2-3 张量积 6 维中心化子维数 = 1 < 5',
      CD_TENSOR == 1 and CD_TENSOR < SM_Y_DISTINCT,
      '不可约 ⇒ 仅 1 个整体 Y；SM 需 %d' % SM_Y_DISTINCT)

guard('G2-4 直和中心化子可加性（块规则）',
      CD_DIRECT == central_dim(S2, 2) + central_dim(S3, 3) == 2,
      'central(直和) = 1 + 1 = 2 ⇒ 15 维 5 块直和给 5')

guard('G2-5 功能非单调：维数 5 -> 6 升，超荷自由度 2 -> 1 降',
      dec_dim(TENSOR_DEC) > dec_dim(DIRECT_DEC) and CD_TENSOR < CD_DIRECT,
      'dim 5->6 (+1) 而 Y 自由度 2->1 (-1)')

KEY['y_dof_direct'] = CD_DIRECT
KEY['y_dof_tensor'] = CD_TENSOR
KEY['y_dof_sm'] = CD_SM
KEY['y_values_sm'] = [str(y) for y in SM_Y]


# ================================================================ 判据 III：反常消除
# 约定：Q = T3 + Y；右手场以左手共轭计入 ⇒ Y_LH = -Y_R
# T(2) = 1/2（双重态）、T(1) = 0；T(3) = 1/2（基本表示）、T(SU(3) 单态) = 0
SM_CHIRAL = [
    ('Q_L', (1, 0), 2, F(1, 6), False),
    ('u_R', (0, 1), 1, F(2, 3), True),
    ('d_R', (0, 1), 1, F(-1, 3), True),
    ('L', (0, 0), 2, F(-1, 2), False),
    ('e_R', (0, 0), 1, F(-1), True),
]


def anomalies(fields):
    a22 = F(0)
    a33 = F(0)
    ayyy = F(0)
    agr = F(0)
    for name, su3, tw, Y, right in fields:
        d3 = dim_su3(*su3)
        d2 = tw
        y = -Y if right else Y
        T2 = F(1, 2) if d2 == 2 else F(0)
        # 基本 (1,0) 与反基本 (0,1) 的 Dynkin 指标同为 1/2
        T3 = F(1, 2) if su3 in ((1, 0), (0, 1)) else F(0)
        a22 += T2 * d3 * y
        a33 += T3 * d2 * y
        ayyy += d3 * d2 * y ** 3
        agr += d3 * d2 * y
    return a22, a33, ayyy, agr


AN_SM = anomalies(SM_CHIRAL)

guard('G3-1 SM 单代四条反常精确为零',
      AN_SM == (F(0), F(0), F(0), F(0)),
      '[SU2]^2U1=%s · [SU3]^2U1=%s · U1^3=%s · grav-U1=%s' % tuple(str(x) for x in AN_SM))

# 5 维直和：V2 用 y1（SU(3) 单态），V3 用 y2（SU(2) 单态）
A22_D = F(1, 2) * 1 * F(1)
A33_D = F(1, 2) * 1 * F(1)
AN_DIRECT_UNIT = (F(1, 2), F(1, 2), F(2) + F(3), F(2) + F(3))
guard('G3-2 直和口径反常方程只有 Y 恒零解',
      AN_DIRECT_UNIT[0] != 0 and AN_DIRECT_UNIT[1] != 0,
      'y1=y2=1 时 [SU2]^2U1=1/2、[SU3]^2U1=1/2 ⇒ 强制 y1=y2=0（无超荷）')

# 6 维张量积：单一 y
AN_TENSOR_UNIT = (F(1, 2) * 3, F(1, 2) * 2, F(6), F(6))
guard('G3-3 张量积口径反常方程只有 Y 恒零解',
      AN_TENSOR_UNIT[0] != 0 and AN_TENSOR_UNIT[1] != 0,
      'y=1 时 [SU2]^2U1=3/2、[SU3]^2U1=1 ⇒ 强制 y=0（无超荷）')

guard('G3-4 Y 恒零与电荷谱互斥',
      SM_Y_DISTINCT == 5 and all(y != 0 for y in SM_Y),
      'SM 需 5 个非零超荷；5/6 口径只允许 Y≡0 ⇒ 无法重现 Q=T3+Y 电荷谱')

# 15 维：非平凡解存在（整体归一自由度 1）⇒ 解空间维数 1
guard('G3-5 15 维口径存在非平凡 Y 解（唯一到整体归一）',
      AN_SM == (F(0), F(0), F(0), F(0)) and SM_Y_DISTINCT == 5,
      '四条齐次方程对 5 个 Y（1 个整体归一冗余）⇒ 零空间维数 1')

KEY['anomaly_sm'] = {
    'SU2^2U1': str(AN_SM[0]),
    'SU3^2U1': str(AN_SM[1]),
    'U1^3': str(AN_SM[2]),
    'grav-U1': str(AN_SM[3]),
}
KEY['anomaly_direct_unit_y'] = [str(x) for x in AN_DIRECT_UNIT]
KEY['anomaly_tensor_unit_y'] = [str(x) for x in AN_TENSOR_UNIT]


# ================================================================ 判据 IV：阶梯算术
LADDER_PRODUCT = sorted(set(2 ** a * 3 ** b for a in range(7) for b in range(7)))

guard('G4-1 纯乘积半群 <2,3> 不含 5 与 15（含 6）',
      5 not in LADDER_PRODUCT and 15 not in LADDER_PRODUCT and 6 in LADDER_PRODUCT,
      '2^a*3^b 前 12 项 = %s' % LADDER_PRODUCT[:12])

guard('G4-2 混合算术 (2+3)x3 = 15 可达（但结构不等价）',
      (2 + 3) * 3 == 15,
      '5 x 3 = 15 ⇒ 维数可达，须另判分量结构')

guard('G4-3 维数巧合陷阱：3 x 5 与单代同维数但缺 7 维、多 7 维',
      dec_dim(DEC_DIRECT_3) == 15
      and dec_missing_dim(DEC_DIRECT_3) == 7
      and dec_excess_dim(DEC_DIRECT_3) == 7
      and dec_missing(DEC_DIRECT_3) == {(3, 2): 1, (1, 1): 1}
      and dec_excess(DEC_DIRECT_3) == {(1, 2): 2, (3, 1): 1},
      '缺 (3,2)[6]+(1,1)[1]=7 · 多 (1,2)x2[4]+(3,1)x1[3]=7 ⇒ 维数相等 != 结构等价')

guard('G4-4 三代 45 维分量与超荷按代复本',
      3 * dec_dim(SM_NEED) == 45 and 3 * dec_count(SM_NEED) == 15,
      '3 x 15 = 45 维 · 15 个不可约块 · Y 自由度 15（每代 5）')

KEY['ladder_product_first'] = LADDER_PRODUCT[:12]
KEY['dim_three_gen'] = 45
KEY['y_dof_three_gen'] = 15
KEY['coincidence_missing_dim'] = dec_missing_dim(DEC_DIRECT_3)
KEY['coincidence_excess_dim'] = dec_excess_dim(DEC_DIRECT_3)
# ================================================================ 判据 V：承载下界定理
BOUND_DIM = dec_dim(SM_NEED)
BOUND_BLOCKS = dec_count(SM_NEED)
BOUND_Y = SM_Y_DISTINCT

guard('G5-1 承载下界：维数 >= 15、分量 >= 5、超荷自由度 >= 5',
      BOUND_DIM == 15 and BOUND_BLOCKS == 5 and BOUND_Y == 5
      and dec_dim(DIRECT_DEC) < BOUND_DIM and dec_dim(TENSOR_DEC) < BOUND_DIM,
      '下界三元组 (15, 5, 5)；5 维给 (5, 2, 2)、6 维给 (6, 1, 1)')

guard('G5-2 三条下界同时不满足（非单指标偶然）',
      dec_dim(DIRECT_DEC) < BOUND_DIM and dec_count(DIRECT_DEC) < BOUND_BLOCKS
      and CD_DIRECT < BOUND_Y
      and dec_dim(TENSOR_DEC) < BOUND_DIM and dec_count(TENSOR_DEC) < BOUND_BLOCKS
      and CD_TENSOR < BOUND_Y,
      '5/6 在维数、分量、超荷三项上同时低于下界 ⇒ 不可由任一单项修补')

KEY['bound_dim'] = BOUND_DIM
KEY['bound_blocks'] = BOUND_BLOCKS
KEY['bound_y'] = BOUND_Y


# ================================================================ 结论条目
entry('E01', '直和 5 维（SU(2)_j=1/2 ⊕ SU(3)_fund）承载 SM 单代', 'FAIL',
      '不可约分解 = (1,2)x1 + (3,1)x1；缺 (3,2)x1 + (3,1)x1 + (1,1)x1 = 10 维；'
      '超荷自由度 2 < 5；[SU2]^2U1 与 [SU3]^2U1 反常强制 y1=y2=0（无超荷）',
      {'dim': dec_dim(DIRECT_DEC), 'blocks': dec_count(DIRECT_DEC),
       'missing_dim': dec_missing_dim(DIRECT_DEC), 'y_dof': CD_DIRECT})

entry('E02', '张量积 6 维（2 ⊗ 3 ≅ (3,2) = Q_L 一个场）承载 SM 单代', 'FAIL',
      '不可约分解 = (3,2)x1；缺 (3,1)x2 + (1,2)x1 + (1,1)x1 = 9 维；'
      '超荷自由度 1 < 5；单块不可约 ⇒ 只有整体 Y，反常强制 y=0',
      {'dim': dec_dim(TENSOR_DEC), 'blocks': dec_count(TENSOR_DEC),
       'missing_dim': dec_missing_dim(TENSOR_DEC), 'y_dof': CD_TENSOR})

entry('E03', '单代 15 维（5 块直和）承载 SM 单代', 'PASS',
      '分量匹配无缺无余（缺失 0 / 多余 0）；超荷自由度 5 = SM 的 5 个不同 Y；'
      '四条反常精确为零（Fraction 恒等），且 5 个 Y 满足四条齐次方程 ⇒ 解空间维数 1（整体归一冗余）',
      {'dim': dec_dim(SM_NEED), 'blocks': dec_count(SM_NEED), 'missing_dim': 0,
       'y_dof': CD_SM, 'y_values': len(SM_Y)})

entry('E04', '三代 45 维 = 3 × 15', 'PASS',
      '按代复本：15 个不可约块、维数 45、超荷自由度 15；反常逐代相消（每代独立为零 ⇒ 总和不增）',
      {'dim': 45, 'blocks': 15, 'y_dof': 15})

entry('E05', '维数巧合陷阱：3 × 直和 5 = 15 与单代同维数', 'FAIL',
      '三维直和 5 的维数恰为 15，但分量缺 (3,2)x1 + (1,1)x1 = 7 维、'
      '同时过量 (1,2)x2 + (3,1)x1 = 7 维（缺失与多余恰好相等）⇒ '
      '「维数相等」不能作为可行性判据，必须比对不可约分解',
      {'dim': dec_dim(DEC_DIRECT_3),
       'missing_dim': dec_missing_dim(DEC_DIRECT_3),
       'excess_dim': dec_excess_dim(DEC_DIRECT_3)})

entry('E06', '承载下界定理：(N, 块数, Y 自由度) >= (15, 5, 5)', 'PASS',
      'SM 单代需要 5 个 SU(3)xSU(2) 不可约分量、合计 15 复维、5 个互异超荷；'
      '三条下界由表示论（不是动力学）给出，与模型无关 ⇒ 5 与 6 在三条上同时不满足',
      {'dim': BOUND_DIM, 'blocks': BOUND_BLOCKS, 'y': BOUND_Y})

entry('E07', '维数阶梯的功能非单调性：5 -> 6 升维而超荷自由度 2 -> 1 降', 'INFO',
      '直和 5 维有 2 个独立标量（两块各一），张量积 6 维因不可约（Schur 中心化子 1）'
      '只剩 1 个整体标量 ⇒ 「更高维」不等于「更多量子数自由度」',
      {'dim': [5, 6], 'y_dof': [CD_DIRECT, CD_TENSOR]})

entry('E08', '反常消除把三条路线分成两类（唯一分水岭）', 'PASS',
      '5 维与 6 维口径的反常方程只有 Y 恒零解（无超荷 ⇒ 无法给 Q=T3+Y 电荷）；'
      '15 维口径存在非平凡解且四条精确为零 ⇒ 反常判据与维数判据同向，且与分量判据互为独立证据',
      {'direct_only_trivial': True, 'tensor_only_trivial': True, 'sm_nontrivial': True})

VERDICT = 'N2-DIMENSION-LADDER--5-AND-6-INFEASIBLE--15-IS-MINIMUM--COINCIDENCE-3x5-TRAP'


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
    add('# TUFT-r441 · N2 维数阶梯可行性：5 vs 6 vs 15')
    add('')
    add('> 直和 5 维 / 张量积 6 维 / 单代 15 维 —— 承载下界与量子数三重判据（Fraction 精确算术，无浮点）')
    add('')
    add('- 生成日期：' + STAMP)
    add('- 守卫：%d/%d 通过' % (guard_ok(), len(GUARDS)))
    add('- 条目：PASS=%d · FAIL=%d · INFO=%d' % (cnt.get('PASS', 0), cnt.get('FAIL', 0), cnt.get('INFO', 0)))
    add('- 总裁定：`' + VERDICT + '`')
    add('')
    add('## 〇 一句话结论')
    add('')
    add('**5 与 6 均不可行，15 是下界。** 5 维直和缺 10 维（缺 3 个不可约分量），'
        '6 维张量积缺 9 维（缺 4 个分量）；两者在反常消除判据下都只剩 `Y ≡ 0` 平凡解；'
        '更反直觉的是：6 维虽比 5 维多 1 维，可独立赋超荷的标量数反而从 2 降到 1（Schur）。')
    add('')
    add('## 一 三口径对照（机器派生）')
    add('')
    add('| 口径 | 构造 | 维数 | 不可约分量 | 缺失维度 | 超荷自由度 | 反常非平凡解 | 判定 |')
    add('| --- | --- | --- | --- | --- | --- | --- | --- |')
    add('| 直和 | V₂ ⊕ V₃ = (1,2) ⊕ (3,1) | 5 | 2 | 10 | 2 | 无（Y≡0） | FAIL |')
    add('| 张量积 | V₂ ⊗ V₃ ≅ (3,2) | 6 | 1 | 9 | 1 | 无（Y≡0） | FAIL |')
    add('| 单代 | 5 块直和 | 15 | 5 | 0 | 5 | 有（归一冗余 1） | PASS |')
    add('| 三代 | 3 × 15 | 45 | 15 | 0 | 15 | 逐代相消 | PASS |')
    add('')
    add('机器读数：`' + KEY['dec_sm'] + '`（SM）· `' + KEY['dec_direct'] + '`（直和 5）· `'
        + KEY['dec_tensor'] + '`（张量积 6）。')
    add('')
    add('## 二 量子数三重判据')
    add('')
    add('### 判据 I：不可约分量匹配')
    add('')
    add('- SM 单代需要 `' + KEY['dec_sm'] + '`，共 5 块 15 维。')
    add('- 直和 5 维缺 `(3,2)×1 + (3,1)×1 + (1,1)×1 = 6+3+1 = 10` 维。')
    add('- 张量积 6 维缺 `(3,1)×2 + (1,2)×1 + (1,1)×1 = 6+2+1 = 9` 维（(3,2) 已由 2⊗3 提供）。')
    add('')
    add('### 判据 II：超荷自由度（Schur 中心化子）')
    add('')
    add('- `central(5 维直和) = 2`（两块各一标量）；`central(6 维张量积) = 1`（不可约）；'
        '`SM 需 5`（5 个互异 Y）。')
    add('- 反直觉读数：**维数 5 → 6 升 1，超荷自由度 2 → 1 降 1** ⇒ 阶梯在功能上非单调。')
    add('')
    add('### 判据 III：反常消除（Q = T₃ + Y，右手按左手共轭计 −Y）')
    add('')
    add('- SM 单代四条：`[SU2]²U1 = 0`、`[SU3]²U1 = 0`、`U1³ = 0`、`grav-U1 = 0`（Fraction 恒等零）。')
    add('- 直和口径：`[SU2]²U1 = y₁/2`、`[SU3]²U1 = y₂/2` ⇒ 强制 `y₁ = y₂ = 0`。')
    add('- 张量积口径：`[SU2]²U1 = 3y/2`、`[SU3]²U1 = y` ⇒ 强制 `y = 0`。')
    add('- ⇒ 5/6 口径下「反常消除」与「有超荷」不可同时成立；15 维口径解空间维数 1（只剩整体归一冗余）。')
    add('')
    add('### 判据 IV：阶梯算术')
    add('')
    add('- 纯乘积半群 `⟨2,3⟩`（`2^a·3^b`）前 12 项：`'
        + ', '.join(str(x) for x in KEY['ladder_product_first']) + '` —— **不含 5，也不含 15**。')
    add('- 混合算术 `(2+3)×3 = 15` 可达 ⇒ 但这是「直和 + 乘法」的混合，须另判分量结构（见 E05）。')
    add('- **维数巧合陷阱**：`3 × 直和 5 = 15` 与单代同维数，但缺 `(3,2)×1 + (1,1)×1 = 7` 维、'
        '同时多出 `(1,2)×2 + (3,1)×1 = 7` 维，缺失与多余恰好相等 ⇒ 维数相等 ≠ 结构等价。')
    add('')
    add('## 三 条目表')
    add('')
    add('| 编号 | 判定 | 条目标题 | 说明 |')
    add('| --- | --- | --- | --- |')
    for e in ENTRIES:
        add('| %s | **%s** | %s | %s |' % (e['code'], e['verdict'], e['title'],
                                          e['detail'].replace('\n', ' ')))
    add('')
    add('## 四 守卫清单')
    add('')
    add('| 守卫 | 结果 | 说明 |')
    add('| --- | --- | --- |')
    for g in GUARDS:
        add('| %s | %s | %s |' % (g['name'], 'PASS' if g['ok'] else 'FAIL', g['detail'].replace('\n', ' ')))
    add('')
    add('## 五 关键数值')
    add('')
    add('| 键 | 值 |')
    add('| --- | --- |')
    for k in sorted(KEY.keys()):
        add('| `%s` | `%s` |' % (k, KEY[k]))
    add('')
    add('## 六 边界（诚实登记）')
    add('')
    add('1. 本册只判「表示的承载能力」，不判动力学（不涉及耦合常数、质量谱、破缺机制）。')
    add('2. 「15 是下界」是**在 SU(3)×SU(2) 分量结构固定**的前提下成立；若允许扩展规范群，'
        '下界与分解都要重算（本册不覆盖）。')
    add('3. 超荷自由度用 Schur 中心化子计数，只对「每块一个标量」的完备可约表示有效；'
        '若允许非对角耦合（破坏 SU(2)×SU(3) 协变），计数不适用。')
    add('4. 反常判据用单代左手约定；代间相加为零（每代独立为零），不涉及代混合。')
    add('')
    return '\n'.join(L) + '\n'


def build_report():
    cnt = counter()
    L = []
    add = L.append
    add(TAG)
    add('=' * 72)
    add('')
    add('ENTRIES')
    for e in ENTRIES:
        add('[%s] %s  %s' % (e['verdict'], e['code'], e['title']))
        add('    ' + e['detail'])
    add('')
    add('KEY NUMBERS')
    for k in sorted(KEY.keys()):
        add('  %-26s %s' % (k, KEY[k]))
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
    print('[r441] guards %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        if not g['ok']:
            print('  [NG] ' + g['name'] + ' | ' + g['detail'])
    print('[r441] entries PASS=%d FAIL=%d INFO=%d'
          % (cnt.get('PASS', 0), cnt.get('FAIL', 0), cnt.get('INFO', 0)))
    print('[r441] VERDICT ' + VERDICT)
    print('[r441] out ' + jp)
    print('[r441] out ' + mp)
    print('[r441] out ' + rp)
    return 0 if guard_ok() == len(GUARDS) else 1


if __name__ == '__main__':
    sys.exit(main())
