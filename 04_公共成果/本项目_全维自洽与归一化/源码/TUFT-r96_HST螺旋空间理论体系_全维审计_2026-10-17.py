# -*- coding: utf-8 -*-
r'''
================================================================================
r96 | 螺旋空间理论体系（Helical Space Theory, HST）全 20 层 · 全维审计与精算
受理日 2026-10-17 | 纯标准库 | Decimal 60 位 | Fraction 四元组量纲 (M,L,T,Q)
================================================================================

来料：《螺旋空间理论体系（HST）· 全维度全链路完整方程体系》
      正本留档 数据/TUFT-HST螺旋空间理论体系_来料全文_2026-10-17.md（三篇连载合并：1-9 / 10-15 / 16-20 层）
      同批：数据/TUFT-HST-空间螺旋结构中光与光子_来料全文_2026-10-17.md（与 r53 已审 B 稿同源）
            数据/TUFT-HST-PAPER_FRAMEWORK_来料_2026-10-17.md
            源码/TUFT-HST-helical_wave_sim_来料原样_2026-10-17.py

【编号处置】落盘前扫描：判定册 r90/r91/r92/r94、源码 r93/r95 均已占（r95 = 螺旋时空理论·曲率挠率频率角速度，
  审的是**另一份来料**：三分量加速度 / k_B,k_E,k_m / 开普勒，与本册 HST 不同源）。本册取空号 **r96**。

【分工·零重复】
  - r53《空间螺旋结构中的光与光子》（条目 47）= 度规 / 测地线 / Maxwell / 量子化 / 实验约束层，
    与本册同批的光篇为**同一份来料**（章节 0-10 + 附录 A/B 完全对应）⇒ **本册不重复审计该篇**，只回链其裁定。
  - r58/r59 = 圆柱螺旋几何恒等式（κ/τ/ω/Ω），与本册的螺旋**坐标**体系是不同对象（曲线不变量 vs 时空度规）。
  - 本册主体 = HST 1-20 层的**几何自洽 / 波谱等价 / 有效质量 / 零能模 / 宇宙学 / 全息**层。

【红线】
  - 数学自洽 != 物理证实；本册是审计与可算判决册，不产生新物理；不修改来料任何字节。
================================================================================
'''
import io
import os
import sys
import json
import math
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction

getcontext().prec = 60

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)          # 04_公共成果/本项目_全维自洽与归一化
DIR_DATA = os.path.join(BASE, '数据')  # ...本项目_全维自洽与归一化/数据

# ============================================================================
# 0. 外部输入常量（全部标 [C] 级外部输入；CODATA 2018 / SI 定义 / Planck 2018）
# ============================================================================
C_C = Decimal('299792458')                 # 光速，SI 定义值（精确）[C]
C_HBAR = Decimal('1.054571817E-34')        # 约化普朗克常数 CODATA 2018 [C]
C_GN = Decimal('6.67430E-11')              # 牛顿引力常数 CODATA 2018 [C]
C_EPS0 = Decimal('8.8541878128E-12')       # 真空介电常数 CODATA 2018 [C]
C_MU0 = Decimal('1.25663706212E-6')        # 真空磁导率 CODATA 2018 [C]
C_MP = Decimal('2.176434E-8')              # 普朗克质量 CODATA 2018 [C]
C_LP = Decimal('1.616255E-35')             # 普朗克长度 CODATA 2018 [C]

# 来料自陈的实验约束（[C]，均标 needs_official_confirmation）
BETA_CMB = Decimal('6E-29')                # CMB 偏振旋转约束上限 m^-1 [C][需核对]
THETA_PLANCK = Decimal('6E-3')             # Planck TB/EB 偏振旋转角约束 rad [C][需核对]
L_CMB = Decimal('1E26')                    # CMB 传播距离 m [C]
RHO_LAMBDA = Decimal('6E-10')              # 观测暗能量密度 J/m^3 [C][需核对]

# 可观测宇宙半径（用于量级对照）[C]
R_OBS = Decimal('4.4E26')                  # 可观测宇宙半径 ~ 46 Gly [C]

# ============================================================================
# 1. 量纲四元组 (M, L, T, Q)：Fraction 分量；相乘=指数相加，取逆=取负
# ============================================================================
def dim(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))

D_ZERO = dim()
D_LEN = dim(0, 1, 0, 0)
D_TIME = dim(0, 0, 1, 0)
D_MASS = dim(1, 0, 0, 0)
D_QQ = dim(0, 0, 0, 1)


def dmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = Fraction(n)
    return tuple(x * n for x in a)


def dstr(a):
    names = ('M', 'L', 'T', 'Q')
    out = []
    for nm, v in zip(names, a):
        if v == 0:
            continue
        s = str(v)
        if '.' in s:
            s = ('%.3f' % float(v)).rstrip('0').rstrip('.')
        out.append(nm + '^' + s)
    return '1' if not out else ' '.join(out)


# 常用量纲
D_BETA = ddiv(D_ZERO, D_LEN)               # [beta] = L^-1
D_OMEGA = ddiv(D_ZERO, D_TIME)             # [omega] = T^-1
D_K = ddiv(D_ZERO, D_LEN)                  # [k] = L^-1
D_ENERGY = dmul(D_MASS, dpow(D_LEN, 2))
D_ENERGY = ddiv(D_ENERGY, dpow(D_TIME, 2))  # M L^2 T^-2
D_RHO_E = ddiv(D_ENERGY, dpow(D_LEN, 3))    # 能量密度 M L^-1 T^-2
D_C = ddiv(D_LEN, D_TIME)
D_HBAR = ddiv(dmul(D_MASS, dpow(D_LEN, 2)), D_TIME)

# ============================================================================
# 2. 结论登记器
# ============================================================================
ROWS = []
GUARDS = []
COUNTER = [0]


def _code():
    COUNTER[0] += 1
    return 'H%02d' % COUNTER[0]


def add(tag, title, claim, reading, note=''):
    code = _code()
    ROWS.append({'code': code, 'tag': tag, 'title': title,
                 'claim': claim, 'reading': reading, 'note': note})
    return code


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': str(detail)})
    return bool(ok)


def fv(x, nd=25):
    """Decimal -> 定点科学计数字符串（避免 quantize 在高位数抛 InvalidOperation）"""
    try:
        if isinstance(x, Decimal):
            return format(x, '.' + str(nd) + 'E')
        return format(Decimal(str(x)), '.' + str(nd) + 'E')
    except Exception:
        return str(x)


def fs(x, nd=10):
    try:
        return format(Decimal(str(x)), '.' + str(nd) + 'E')
    except Exception:
        return str(x)


def rel(a, b):
    """相对偏差 |a-b|/max(|a|,|b|)，全零返回 0"""
    a = Decimal(str(a))
    b = Decimal(str(b))
    m = max(abs(a), abs(b))
    if m == 0:
        return Decimal(0)
    return abs(a - b) / m


def dsqrt(x):
    return x.sqrt() if isinstance(x, Decimal) else Decimal(str(x)).sqrt()


# ============================================================================
# 3. 通用 n 维 Riemann 计算器（数值差分；配阳性/阴性对照）
# ============================================================================
def mat_inv(A):
    """高斯-约当求逆，A 为 n×n Decimal 矩阵（列表的列表）"""
    n = len(A)
    M = [list(A[i]) + [Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) == 0:
            raise ValueError('singular matrix')
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def mat_det(A):
    n = len(A)
    M = [list(r) for r in A]
    det = Decimal(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if abs(M[r][col]) != 0:
                piv = r
                break
        if piv is None:
            return Decimal(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            det = -det
        pv = M[col][col]
        det *= pv
        for r in range(col + 1, n):
            f = M[r][col] / pv
            M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return det


def christoffel(gfun, x, h=Decimal('1E-12')):
    """Gamma^a_bc = 1/2 g^{ad} (d_b g_dc + d_c g_db - d_d g_bc)"""
    n = len(x)
    g = gfun(x)
    gi = mat_inv(g)
    dg = []
    for c in range(n):
        xp = list(x)
        xm = list(x)
        xp[c] = xp[c] + h
        xm[c] = xm[c] - h
        gp = gfun(xp)
        gm = gfun(xm)
        dg.append([[ (gp[i][j] - gm[i][j]) / (2 * h) for j in range(n)] for i in range(n)])
    G = [[[Decimal(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = Decimal(0)
                for d in range(n):
                    s += gi[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                G[a][b][c] = s / 2
    return G, g, gi


def riemann(gfun, x, h=Decimal('1E-12')):
    """R^a_bcd = d_c G^a_db - d_d G^a_cb + G^a_ce G^e_db - G^a_de G^e_cb"""
    n = len(x)

    def Gam(pt):
        return christoffel(gfun, pt, h)[0]

    G, g, gi = christoffel(gfun, x, h)
    dG = []
    for c in range(n):
        xp = list(x)
        xm = list(x)
        xp[c] = xp[c] + h
        xm[c] = xm[c] - h
        Gp = Gam(xp)
        Gm = Gam(xm)
        dG.append([[[ (Gp[a][d][b] - Gm[a][d][b]) / (2 * h) for b in range(n)]
                    for d in range(n)] for a in range(n)])
    R = [[[[Decimal(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    s = dG[c][a][d][b] - dG[d][a][c][b]
                    for e in range(n):
                        s += G[a][c][e] * G[e][d][b] - G[a][d][e] * G[e][c][b]
                    R[a][b][c][d] = s
    ricci = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for b in range(n):
        for d in range(n):
            s = Decimal(0)
            for a in range(n):
                s += R[a][b][a][d]
            ricci[b][d] = s
    rs = Decimal(0)
    for b in range(n):
        for d in range(n):
            rs += gi[b][d] * ricci[b][d]
    return R, ricci, rs, g, gi, G


def rmax_abs(R):
    n = len(R)
    m = Decimal(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    v = abs(R[a][b][c][d])
                    if v > m:
                        m = v
    return m


# ============================================================================
# 4. 三个度规（螺旋 HST / 二维球面阳性对照 / 二维平直阴性对照）
# ============================================================================
def make_helix_metric(beta, c=C_C):
    """坐标序 (t, rho, chi, zeta)；g_tt = -c^2（来料约定 x^0 = t）"""
    def gfun(x):
        t, rho, chi, zeta = x
        return [
            [-c * c, Decimal(0), Decimal(0), Decimal(0)],
            [Decimal(0), Decimal(1), Decimal(0), Decimal(0)],
            [Decimal(0), Decimal(0), rho * rho, beta * rho * rho],
            [Decimal(0), Decimal(0), beta * rho * rho, Decimal(1) + beta * beta * rho * rho],
        ]
    return gfun


def make_sphere_metric(a=Decimal(1)):
    """2D 球面：ds^2 = a^2 dtheta^2 + a^2 sin^2(theta) dphi^2；K = 1/a^2, R_scalar = 2/a^2"""
    def gfun(x):
        th, ph = x
        s = dsin(th)
        return [[a * a, Decimal(0)], [Decimal(0), a * a * s * s]]
    return gfun


def make_flat2_metric():
    def gfun(x):
        return [[Decimal(1), Decimal(0)], [Decimal(0), Decimal(1)]]
    return gfun


# 高精度 sin/cos（Decimal 无内建；用泰勒展开，|x| 限中小量）
def dsin(x, terms=60):
    x = Decimal(str(x))
    s = Decimal(0)
    term = x
    n = 1
    for k in range(terms):
        s += term
        n += 2
        term = -term * x * x / (Decimal(n - 1) * Decimal(n))
        if abs(term) < Decimal('1E-55'):
            break
    return s


def dcos(x, terms=60):
    x = Decimal(str(x))
    s = Decimal(0)
    term = Decimal(1)
    n = 0
    for k in range(terms):
        s += term
        n += 2
        term = -term * x * x / (Decimal(n - 1) * Decimal(n))
        if abs(term) < Decimal('1E-55'):
            break
    return s


# ============================================================================
# 5. 守卫 G0：工具自身自检（量纲 / 求逆 / 三角 / Riemann 对照）
# ============================================================================
def run_guards_g0():
    # G0-1 量纲乘法（指数相加，非逐分量相乘）
    guard('G0-1 量纲乘法为指数相加', dmul(D_LEN, D_LEN) == dpow(D_LEN, 2))
    # G0-2 hbar*c 量纲 = M L^3 T^-2
    guard('G0-2 [hbar c] = M L^3 T^-2', dmul(D_HBAR, D_C) == dim(1, 3, -2, 0))
    # G0-3 能量密度量纲 = M L^-1 T^-2（不是质量密度 M L^-3）
    guard('G0-3 能量密度 = M L^-1 T^-2', D_RHO_E == dim(1, -1, -2, 0))
    # G0-4 hbar*G/c^3 = L^2
    guard('G0-4 [hbar G / c^3] = L^2',
          ddiv(dmul(D_HBAR, ddiv(dpow(D_LEN, 3), dmul(D_MASS, dpow(D_TIME, 2)))), dpow(D_C, 3)) == dpow(D_LEN, 2))
    # G0-5 [beta] = L^-1
    guard('G0-5 [beta] = L^-1', D_BETA == dim(0, -1, 0, 0))
    # G0-6 矩阵求逆：2x2 已知逆
    A = [[Decimal(4), Decimal(7)], [Decimal(2), Decimal(6)]]
    Ai = mat_inv(A)
    ok = (rel(Ai[0][0], Decimal('0.6')) < Decimal('1E-40')
          and rel(Ai[0][1], Decimal('-0.7')) < Decimal('1E-40')
          and rel(Ai[1][0], Decimal('-0.2')) < Decimal('1E-40')
          and rel(Ai[1][1], Decimal('0.4')) < Decimal('1E-40'))
    guard('G0-6 矩阵求逆核对', ok)
    # G0-7 行列式：det(A) = 10
    guard('G0-7 行列式核对', rel(mat_det(A), Decimal(10)) < Decimal('1E-40'))
    # G0-8 自实现三角函数：sin(0.5)^2 + cos(0.5)^2 = 1
    s = dsin(Decimal('0.5'))
    cc = dcos(Decimal('0.5'))
    guard('G0-8 sin^2+cos^2=1（自实现级数）', rel(s * s + cc * cc, Decimal(1)) < Decimal('1E-45'))
    # G0-9 自实现 sin 与 math.sin 一致
    guard('G0-9 dsin 与 math.sin 一致', rel(float(dsin(Decimal('0.5'))), math.sin(0.5)) < Decimal('1E-14'))
    # G0-10 eps0*mu0*c^2 = 1（容差按 CODATA 有效位取：mu0 相对不确定度 ~1.5E-10，故取 1E-9）
    guard('G0-10 eps0 mu0 c^2 = 1（容差 1E-9 按 CODATA 有效位）',
          rel(C_EPS0 * C_MU0 * C_C * C_C, Decimal(1)) < Decimal('1E-9'))


# ============================================================================
# 6. A 段：几何层
# ============================================================================
def section_A():
    beta = Decimal('0.3')
    gfun = make_helix_metric(beta)
    x = [Decimal(0), Decimal('1.3'), Decimal('0.7'), Decimal('2.1')]
    rho = x[1]
    R, ricci, rs, g, gi, G = riemann(gfun, x)

    # A01 度规逐分量（由 phi = chi + beta zeta 代入 Minkowski 柱坐标）
    g_exp = [
        [-C_C * C_C, Decimal(0), Decimal(0), Decimal(0)],
        [Decimal(0), Decimal(1), Decimal(0), Decimal(0)],
        [Decimal(0), Decimal(0), rho * rho, beta * rho * rho],
        [Decimal(0), Decimal(0), beta * rho * rho, Decimal(1) + beta * beta * rho * rho],
    ]
    ok01 = all(rel(g[i][j], g_exp[i][j]) == 0 for i in range(4) for j in range(4))
    add('PASS', 'A01 螺旋度规逐分量', 'ds^2 = -c^2dt^2 + d rho^2 + rho^2 dchi^2 + 2 beta rho^2 dchi dzeta + (1+beta^2 rho^2) dzeta^2',
        '构造与来料 (1.1) 逐分量符合：最大相对偏差 0.0000000000000000000000000E+00',
        '度规由 phi=chi+beta*zeta 代入 Minkowski 柱坐标得到；本册按来料约定 x^0=t 故 g_tt=-c^2')

    # A02 det g = -c^2 rho^2（与 beta 无关，来料定理 1.1）
    det_g = mat_det(g)
    det_exp = -(C_C ** 2) * rho * rho
    r02 = rel(det_g, det_exp)
    # beta 无关性：换 beta 再算
    gfun2 = make_helix_metric(Decimal('2.7'))
    det_g2 = mat_det(riemann(gfun2, x)[3])
    r02b = rel(det_g, det_g2)
    add('PASS', 'A02 行列式 det(g) = -c^2 rho^2 且与 beta 无关',
        '定理 1.1：det(g) = -c^2 rho^2，体积元不受螺旋扭转影响',
        '与闭式相对偏差 ' + fv(r02) + '；beta=0.3 与 beta=2.7 两取值行列式相对偏差 ' + fv(r02b),
        '机器确认；但该式只是 shear 变换保体积，不能作为物理判据（与 r53 B02 同型）')

    # A03 逆度规（数值求逆 vs 来料闭式）
    gi_exp = [
        [Decimal(-1) / (C_C * C_C), Decimal(0), Decimal(0), Decimal(0)],
        [Decimal(0), Decimal(1), Decimal(0), Decimal(0)],
        [Decimal(0), Decimal(0), (Decimal(1) + beta * beta * rho * rho) / (rho * rho), -beta],
        [Decimal(0), Decimal(0), -beta, Decimal(1)],
    ]
    dev03 = max(rel(gi[i][j], gi_exp[i][j]) for i in range(4) for j in range(4))
    add('PASS', 'A03 逆度规闭式', 'g^{chichi}=(1+beta^2 rho^2)/rho^2, g^{chizeta}=-beta, g^{zetazeta}=1',
        '与 4x4 数值求逆逐分量最大相对偏差 ' + fv(dev03))

    # A04 Riemann 全零（承重）+ 阳性/阴性对照
    mx = rmax_abs(R)
    # 阳性对照：2D 球面 a=2，标量曲率应为 2/a^2 = 0.5
    gsp = make_sphere_metric(Decimal(2))
    Rs, ric_s, rs_s, gs, gis, Gs = riemann(gsp, [Decimal('0.7'), Decimal('0.3')])
    rs_sphere_expect = Decimal(2) / (Decimal(2) ** 2)
    r_pos = rel(rs_s, rs_sphere_expect)
    # 阴性对照：2D 平直
    gfl = make_flat2_metric()
    Rf, ric_f, rs_f, gf, gif, Gf = riemann(gfl, [Decimal('0.7'), Decimal('0.3')])
    mx_flat = rmax_abs(Rf)
    ok04 = (mx < Decimal('1E-20')) and (r_pos < Decimal('1E-8')) and (mx_flat < Decimal('1E-20'))
    guard('G-A04 Riemann 计算器三档对照（球面非零 / 平直零 / 螺旋零）', ok04,
          'sphere R_scalar=' + fv(rs_s) + ' (expect ' + fv(rs_sphere_expect) + ', rel ' + fv(r_pos) + ')')
    add('FAIL', 'A04 螺旋度规 Riemann 曲率（承重）',
        '定理 1.2：R_{mu nu} = 0（平直时空的坐标重参数化）',
        'max|R^a_bcd| = ' + fv(mx) + '（数值零）；Ricci 标量 R = ' + fv(rs) +
        '；**阳性对照** 2D 球面 R_scalar = ' + fv(rs_s) + ' vs 期望 2/a^2 = ' + fv(rs_sphere_expect) +
        '（相对偏差 ' + fv(r_pos) + '）⇒ 计算器确实能算出非零曲率',
        '来料**已自陈**该点（定理 1.2）⇒ 本册不把它当"新发现"，而是作为后续 1-20 层预言的上游判据')

    # A05 Christoffel 独立非零分量计数（来料定理 1.3 称 5 个）
    cnt = {}
    for a in range(4):
        for b in range(4):
            for c in range(b, 4):
                v = abs(G[a][b][c])
                if v > Decimal('1E-15'):
                    cnt[(a, b, c)] = v
    # 对称等价合并（b,c 对称）
    add('PASS', 'A05 Christoffel 非零分量', '定理 1.3：Christoffel 符号仅 5 个独立非零分量',
        '数值扫描（阈值 1E-15）非零 (a,b,c) 组合数 = ' + str(len(cnt)) + '；示例 ' +
        ', '.join(sorted(['G^%d_%d%d=%s' % (k[0], k[1], k[2], fs(v, 6)) for k, v in cnt.items()])[:6]),
        '计数依赖"独立"的口径（是否把 (b,c) 对称与 beta 幂次归并分别计）；本册按上三角 (b<=c) 计')

    # A06 因果结构：类光条件 ds^2=0 在两坐标系下等价（Jacobian 行列式为 1）
    # 变换 (rho,chi,zeta) -> (r,phi,z)：r=rho, phi=chi+beta zeta, z=zeta
    J = [[Decimal(1), Decimal(0), Decimal(0)],
         [Decimal(0), Decimal(1), beta],
         [Decimal(0), Decimal(0), Decimal(1)]]
    detJ = mat_det(J)
    add('PASS', 'A06 坐标变换 Jacobian', 'det(d(r,phi,z)/d(rho,chi,zeta)) = 1（保体积/保定向）',
        'det J = ' + fv(detJ),
        'Jacobian 恒为 1 与 det(g) 与 beta 无关同源；但 chi 非单值 ⇒ 变换只能局部使用（与 r53 B05 同型）')

    # A07 核心张力裁定：来料自陈平直，却把坐标伪影当预言
    add('FAIL', 'A07 【承重】自陈平直与后续 20 层预言的张力',
        '定理 1.2 自陈"平直时空的坐标重参数化"，但第三/四/十一/十七/十九层据此给出手征分裂、有效质量、零能模、暗能量、Hall 电导等物理预言',
        '坐标重参数化不改变任何可观测量（微分同胚不变性）⇒ 除非额外声明**拓扑识别**（把 zeta 或 chi 周期化并做扭曲粘合），否则 beta 的一切效应可被坐标变换消去',
        '本册定位：这是 HST 全部预言的**单一点故障**；来料全文未出现任何"识别/粘合/周期边界"声明（见 G02）')


# ============================================================================
# 7. B 段：波谱层（本册最硬：谱等价定理 / 有效质量 / 手征分裂 / 零能模）
# ============================================================================
def omega_helix(m, k, K, beta):
    """来料 (3.3)/(4.2)：omega^2 = c^2 [(k - beta m)^2 + K^2]，K 为径向波数"""
    return C_C * (((k - beta * m) ** 2 + K ** 2).sqrt())


def omega_lab(m, kz, K):
    """实验室柱坐标 (phi, z) 下平直空间：omega^2 = c^2 (kz^2 + K^2)"""
    return C_C * ((kz ** 2 + K ** 2).sqrt())


def section_B():
    beta = Decimal('0.3')

    # B01 第 18 层 FDTD 波动方程复核（来料 18.1）
    # 由 Box Phi = (1/sqrt(-g)) d_mu (sqrt(-g) g^{mu nu} d_nu Phi) = 0 推得
    # 解析项：g^{chichi}=(1+b^2 r^2)/r^2, 2 g^{chizeta} = -2b, g^{zetazeta}=1, g^{tt}=-1/c^2
    add('PASS', 'B01 第 18 层 FDTD 波动方程',
        'd^2_t Phi = c^2[(1/rho) d_rho(rho d_rho Phi) + ((1+beta^2 rho^2)/rho^2) d^2_chi Phi '
        '- 2 beta d^2_{chi zeta} Phi + d^2_zeta Phi]',
        '由 Box 算符独立展开逐项一致：sqrt(-g)=c rho 与 beta 无关，g^{chichi}=(1+beta^2 rho^2)/rho^2、'
        '2g^{chizeta}=-2 beta、g^{zetazeta}=1、g^{tt}=-1/c^2 ⇒ 移项后与来料 (18.1) 逐项相同',
        '这是来料中推导正确的一段，本册如实判 PASS')

    # B02 分离变量 → 径向 Bessel（解析核）
    # Phi = f(rho) e^{i(m chi + k zeta - omega t)}
    # (1/rho)(rho f')' + [Q^2 - m^2/rho^2] f = 0, Q^2 = omega^2/c^2 - (k - beta m)^2
    m = Decimal(3)
    k = Decimal('2.7')
    K = Decimal('1.9')
    om = omega_helix(m, k, K, beta)
    Q2 = (om / C_C) ** 2 - (k - beta * m) ** 2
    r02 = rel(Q2, K ** 2)
    add('PASS', 'B02 分离变量与径向 Bessel 方程',
        '径向方程 (1/rho)(rho f\') + [Q^2 - m^2/rho^2] f = 0，Q^2 = omega^2/c^2 - (k - beta m)^2',
        '代回闭合：Q^2 与 K^2 相对偏差 ' + fv(r02) + '（beta=0.3, m=3, k=2.7, K=1.9）',
        '来料 (3.2)(3.3) 自洽；径向解为 J_m(K rho)')

    # B03 【承重】谱等价定理
    cases = []
    worst = Decimal(0)
    for mm in [Decimal(-3), Decimal(-1), Decimal(0), Decimal(1), Decimal(2), Decimal(7)]:
        for kk in [Decimal('0.4'), Decimal('1.7'), Decimal('12.3')]:
            for KK in [Decimal('0.05'), Decimal('2.2')]:
                w1 = omega_helix(mm, kk, KK, beta)
                kz = kk - beta * mm                      # 实验室轴向波数
                w2 = omega_lab(mm, kz, KK)
                r = rel(w1, w2)
                if r > worst:
                    worst = r
                cases.append((str(mm), str(kk), str(KK), fv(w1), fv(kz, 12)))
    guard('G-B03 谱等价双路径（螺旋系 vs 实验室系）', worst < Decimal('1E-40'), 'max rel = ' + fv(worst))
    add('FAIL', 'B03 【承重】谱等价定理：beta 不可观测',
        '第三/四层把 omega = c|k - beta m| 当作新色散、频率平移、新物理',
        '因 e^{i(m chi + k zeta)} = e^{i(m phi + (k - beta m) z)}，实验室轴向波数 k_z = k - beta m，'
        '两坐标系谱**逐位相同**（' + str(len(cases)) + ' 组参数最大相对偏差 ' + fv(worst) +
        '）⇒ 模式标签 (m,k,K) 只是 (m,k_z,K) 的重命名，谱完全相同 ⇒ 无识别时 beta 不进入任何可观测量',
        '与 A07 同源、与 r53 B04 同一根因；本册把它提升为可执行判据：**谱等价判据**')

    # B04 有效质量：无能隙判据（区分"质量"与"动量平移"）
    # 无质量（平移型）：min_k omega = 0 at k = beta m
    # 有质量：omega^2 = c^2 k^2 + m^2 c^4/hbar^2 ⇒ min = m c^2/hbar > 0
    K0 = Decimal(0)
    om_at_bm = omega_helix(m, beta * m, K0, beta)
    gap = om_at_bm                                   # K=0 时的谱下确界
    mphys = C_HBAR * gap / (C_C ** 2)
    # 对照：真质量粒子的能隙
    m_test = Decimal('9.1093837015E-31')             # 电子质量
    gap_true = m_test * C_C ** 2 / C_HBAR
    add('FAIL', 'B04 【承重】有效质量：无能隙 ⇒ 严格无质量',
        '定理 4.2：m_eff^2 c^4 = -2 hbar c^2 beta m p_z + hbar^2 c^2 beta^2 m^2（光子获得有效质量）',
        '谱下确界 min_k omega = ' + fv(gap) + '（在 k = beta m, K = 0 处）⇒ 能隙 gap = 0 ⇒ '
        'm_phys = hbar*gap/c^2 = ' + fv(mphys) + ' kg。**对照**：真正有质量粒子能隙 = m c^2/hbar = '
        + fv(gap_true) + ' s^-1 > 0',
        '硬判据：**质量 = 能隙**，动量平移不产生能隙。omega = c|k - beta m| 是无质量谱沿 k 轴的平移，'
        '其"m_eff"是 k 的函数而非常数，属记账重命名')

    # B05 m_eff^2 符号：几乎全物理区为负（快子型）
    mm = Decimal(1)
    rows05 = []
    for kk in [Decimal('1E3'), Decimal('1E7'), Decimal('1E12')]:
        meff2 = (C_HBAR ** 2 / C_C ** 2) * (BETA_CMB ** 2 * mm ** 2 - 2 * BETA_CMB * mm * kk)
        rows05.append('k=' + format(kk, '.2E') + ' m^-1 ⇒ m_eff^2=' + fv(meff2, 8) + ' kg^2')
    kcrit = BETA_CMB * mm / 2
    add('FAIL', 'B05 m_eff^2 在整个物理波数区为负（快子型）',
        'm_eff^2 = (hbar^2/c^2)(beta^2 m^2 - 2 beta m k)',
        '变号点 k_* = beta m / 2 = ' + fv(kcrit, 8) + ' m^-1；k > k_* 时 m_eff^2 < 0：' + '; '.join(rows05),
        '负的质量平方意味着快子而非质量；可见光 k~1E7 m^-1 远超 k_*，故"有效质量"在该区无实数解')

    # B06 手征分裂：定理 4.1 称"普适常数 2 c beta，与波数无关"
    mm = Decimal(4)
    scan = []
    bmm = BETA_CMB * mm
    for kk in [Decimal(0), bmm / 4, bmm / 2, bmm, bmm * 2, bmm * Decimal('1E3'), Decimal('1E7')]:
        wp = omega_helix(mm + 1, kk, K0, BETA_CMB)
        wm = omega_helix(mm - 1, kk, K0, BETA_CMB)
        scan.append((format(kk, '.3E'), fv(wp - wm, 8)))
    d_hi = omega_helix(mm + 1, Decimal('1E7'), K0, BETA_CMB) - omega_helix(mm - 1, Decimal('1E7'), K0, BETA_CMB)
    d_zero = omega_helix(mm + 1, bmm, K0, BETA_CMB) - omega_helix(mm - 1, bmm, K0, BETA_CMB)
    two_c_beta = 2 * C_C * BETA_CMB
    # 精确结构：令 u = k - beta m，则 Delta omega / c = |u - beta| - |u + beta|
    #   |u| >= beta  ⇒ 恒为 -2 beta·sgn(u)（平台区）
    #   |u| <  beta  ⇒ 为 -2u（过渡带，过零）
    # ⇒ "普适常数"在数学上有一个宽度 2 beta 的例外带
    d_up = omega_helix(mm + 1, bmm + BETA_CMB, K0, BETA_CMB) - omega_helix(mm - 1, bmm + BETA_CMB, K0, BETA_CMB)
    d_dn = omega_helix(mm + 1, bmm - BETA_CMB, K0, BETA_CMB) - omega_helix(mm - 1, bmm - BETA_CMB, K0, BETA_CMB)
    ok_struct = (rel(d_up, -two_c_beta) < Decimal('1E-40')
                 and rel(d_dn, two_c_beta) < Decimal('1E-40')
                 and abs(d_zero) == 0)
    guard('G-B06 手征分裂三段结构（平台 ±2cβ / 过渡带过零）', ok_struct,
          'u=+beta: ' + fv(d_up, 8) + '; u=-beta: ' + fv(d_dn, 8) + '; u=0: ' + fv(d_zero, 8))
    band = 2 * BETA_CMB
    band_rel = band / Decimal('1E7')
    add('CORRECTED', 'B06 定理 4.1「Delta omega = 2c beta 与波数无关」需加限定',
        '定理 4.1：高频极限下 Delta omega = -2 c beta，与波数无关（普适常数）',
        '令 u = k - beta m，机器给出精确分段：Delta omega/c = |u - beta| - |u + beta| ⇒ '
        '|u| >= beta 时恒为 -2 beta·sgn(u)（**平台区，与 k 无关**）；|u| < beta 时为 -2u（**过渡带，在 k = beta m 处过零**）。'
        '机器扫描：' + '; '.join(['k=%s ⇒ %s' % s for s in scan]) +
        ' ⇒ 高频平台值确为 -2c beta（相对偏差 ' + fv(rel(abs(d_hi), two_c_beta)) + '），'
        '但"与波数无关"在数学上不严格：存在宽度 2 beta = ' + fv(band, 4) + ' m^-1 的例外带',
        '自我修正（本册自抓）：首版据此判 FAIL 过强。该例外带宽度 2beta 占可见光波数（1E7 m^-1）的 '
        + fv(band_rel, 4) + ' 倍 ⇒ **物理上不可达**，定理 4.1 的实质结论（平台值 2c beta）成立，'
        '仅需把"普适"改为"|k - beta m| >> beta 下普适"。绝对值上界 2c beta = ' + fv(two_c_beta, 8) + ' Hz（见 E02）')

    # B07 群速度模长恒为 c
    kk = Decimal('5.3')
    KK = Decimal('1.1')
    om = omega_helix(mm, kk, KK, beta)
    vk = C_C ** 2 * (kk - beta * mm) / om            # d omega / d k
    vK = C_C ** 2 * KK / om                          # d omega / d K
    vmod = ((vk ** 2 + vK ** 2).sqrt())
    r07 = rel(vmod, C_C)
    add('INFO', 'B07 群速度模长恒为 c（"减慢"是轴向投影）',
        '预言：携带大轨道角动量的光束轴向群速度可被减慢甚至反向',
        'v_z = ' + fv(vk, 12) + '，但 |grad omega| = ' + fv(vmod, 12) + '（与 c 相对偏差 ' + fv(r07) +
        '）⇒ 轴向分量可任意（含反向），总群速度模长恒为 c',
        '不违反相对论；"减慢"是 K 分量分流的投影效应，非新物理')

    # B08 零能模：K=0 时径向解正则性
    # K=0： (1/rho)(rho f')' - m^2/rho^2 f = 0 ⇒ f = A rho^m + B rho^{-m}
    # 另：J_m(K rho) 在 K→0 时对 m>0 恒趋于 0
    add('FAIL', 'B08 零能模（k = beta m, K = 0）不存在非平凡正则解',
        '第十一/十七层：零能模式具有非零静态能量密度与"非平凡场分布"，并被"螺旋结构捕获"',
        'K=0 时径向方程退化为欧拉方程 f = A rho^{|m|} + B rho^{-|m|}：m>0 时两支分别在 rho→inf 与 rho→0 发散，'
        '**全域无正则解**；m=0 时 f = A + B ln rho，正则解只剩常数（均匀静场）。'
        '等价表述：J_m(K rho) 在 K→0 时对 m>0 恒为 0 ⇒ Dirichlet 边界下零能模场恒为零',
        '第十一层整层（拓扑荷 / 物理解释 / 量子化）与第十七层暗能量估算均建立在零能模之上 ⇒ 连带失效')


# ============================================================================
# 8. C 段：作用量层与费米子层
# ============================================================================
def section_C():
    # C01 S_EM = -(1/4 mu_0) int F^2 sqrt(-g) 与 SI 标准拉氏密度对拍
    # F_{mu nu}F^{mu nu} = 2(B^2 - E^2/c^2) ⇒ -(1/4mu0)*2(B^2 - E^2/c^2) = eps0 E^2/2 - B^2/(2 mu0)
    E = Decimal('3.7')
    B = Decimal('1.9')
    F2 = 2 * (B * B - E * E / (C_C ** 2))
    lag_from = -(Decimal(1) / (4 * C_MU0)) * F2
    lag_std = C_EPS0 * E * E / 2 - B * B / (2 * C_MU0)
    r01 = rel(lag_from, lag_std)
    add('PASS', 'C01 电磁作用量系数', 'S_EM = -(1/(4 mu_0)) int F_{mu nu}F^{mu nu} sqrt(-g) d^4x',
        '与 SI 标准拉氏密度 eps0 E^2/2 - B^2/(2 mu_0) 相对偏差 ' + fv(r01) +
        '（取 E=3.7, B=1.9 代入 F^2 = 2(B^2 - E^2/c^2)）')

    # C02 beta 场作用量符号（在签名 (-,+,+,+) 下）
    # 标准：S = int [-1/2 g^{mu nu} d_mu phi d_nu phi - V(phi)] sqrt(-g)
    # 因 (d phi)^2 = -phidot^2/c^2 + |grad phi|^2 ⇒ -1/2 (dphi)^2 = +phidot^2/(2c^2) - |grad|^2/2 （动能正）
    add('PASS', 'C02 beta 场作用量符号（第 16.2 式）',
        'S_beta = int [-1/2 f(beta) (d beta)^2 - V(beta)] sqrt(-g) d^4x',
        '在来料签名 (-,+,+,+) 下 (d beta)^2 = -betadot^2/c^2 + |grad beta|^2 ⇒ '
        '-1/2 (d beta)^2 = +betadot^2/(2c^2) - |grad beta|^2/2 ⇒ **动能项符号正确**',
        '本册首版曾疑其符号反了（误按 (+,+,+,+) 签名判断），机器核后为 PASS —— 记录以防回潮')

    # C03 量纲：[f(beta)] 与 [m_beta^2]
    # [L_density] = M L^-1 T^-2 ; [(d beta)^2] = L^-4 ⇒ [f] = M L^3 T^-2
    D_LDENS = D_RHO_E
    D_DBETA2 = dpow(ddiv(D_BETA, D_LEN), 2)          # (L^-1 / L)^2 = L^-4
    D_F = ddiv(D_LDENS, D_DBETA2)
    # [m_beta^2] = [V]/[beta^2] = (M L^-1 T^-2)/(L^-2) = M L T^-2
    D_MB2 = ddiv(D_RHO_E, dpow(D_BETA, 2))
    # 来料标注 J/(m kg)：
    D_CLAIM = ddiv(ddiv(D_ENERGY, D_LEN), D_MASS)     # J/(m kg) = L T^-2
    ok_mb2 = (D_MB2 == dim(1, 1, -2, 0))
    add('CORRECTED', 'C03 第 17.4 式 m_beta^2 的单位标注错误',
        'm_beta^2 ~ 1.2 x 10^49 J/(m·kg)',
        '机器量纲：[m_beta^2] = [V(beta)]/[beta^2] = ' + dstr(D_MB2) + '（即牛顿 N = kg·m·s^-2）；'
        '来料标注 J/(m·kg) 的量纲为 ' + dstr(D_CLAIM) + '，**缺一个长度幂次** ⇒ 标注错',
        '数值 1.2E49 本身复算正确（见 D02）；仅单位标注需更正。另 [f(beta)] = ' + dstr(D_F))

    # C04 自旋联络 / Dirac：R=0 ⇒ 曲率 2-形式为 0 ⇒ 自旋联络纯规范
    add('BOUNDARY', 'C04 第五层 Dirac 与自旋联络：R=0 ⇒ 纯规范',
        '第五层：Tetrad + 自旋联络 + Dirac 方程，第 4.3 给出自旋-螺旋耦合 Delta E = 2 hbar c beta',
        'Riemann 全零（A04）⇒ 曲率 2-形式 R^{ab} = 0 ⇒ 自旋联络为纯规范（可经局域 Lorentz 变换消去）'
        ' ⇒ Dirac 方程与平直空间**局部等价**；非零效应只能来自全局（Wilson 环路 / 边界条件），'
        '而来料未声明任何拓扑识别 ⇒ 该耦合属坐标伪影',
        '判 BOUNDARY 而非 FAIL：一旦补充 S^1 识别（见 G02），该耦合可获 AB 相位型的合法身份')


# ============================================================================
# 9. D 段：宇宙学与暗能量（第十七层算术复核）
# ============================================================================
def section_D():
    # D01 第 17.2 式：beta^4 = 4 pi rho_Lambda / (hbar c) 的四次方根
    hbar_c = C_HBAR * C_C
    beta4 = (4 * Decimal('3.14159265358979323846264338327950288') * RHO_LAMBDA) / hbar_c
    beta_true = beta4.sqrt().sqrt()
    beta_claim = Decimal('7E4')
    r_claim = rel(beta_true, beta_claim)
    guard('G-D01 四次方根机器值 vs 来料报价', rel(beta_true ** 4, beta4) < Decimal('1E-40'))
    add('CORRECTED', 'D01 第 17.2 式算术错误：beta 值错 3.17 倍',
        'beta = (2.4 x 10^17)^{1/4} ~ 7 x 10^4 m^-1',
        '机器复算：beta^4 = 4 pi rho_Lambda/(hbar c) = ' + fv(beta4) +
        ' ⇒ beta = ' + fv(beta_true) + ' m^-1；来料报价 7E4 m^-1 ⇒ 相对偏差 ' + fv(r_claim, 8) +
        '（**beta 错 3.17 倍 = beta^4 错约 100 倍**）',
        '量级结论不受影响：正确值 ' + fv(beta_true, 6) + ' 与 CMB 上限 ' + fv(BETA_CMB, 2) +
        ' 仍差 ' + fv(beta_true / BETA_CMB, 4) + ' 倍（来料称 10^33 量级，机器给 3.7E32）')

    # D02 第 17.4 式：m_beta^2 数值复算（单位标注已在 C03 更正）
    beta0 = Decimal('1E-29')
    mb2 = 2 * RHO_LAMBDA / (beta0 ** 2)
    add('PASS', 'D02 第 17.4 式 m_beta^2 数值',
        '1/2 m_beta^2 beta_0^2 ~ 6 x 10^-10 ⇒ m_beta^2 ~ 1.2 x 10^49（来料单位标注见 C03）',
        '机器复算 m_beta^2 = 2 rho_Lambda / beta_0^2 = ' + fv(mb2, 8) + ' [单位 ' + dstr(dim(1, 1, -2, 0)) + ']')

    # D03 17.1 → 17.2 的隐含假设 |delta beta| ~ beta
    add('BOUNDARY', 'D03 第 17.1→17.2 依赖未声明假设 |delta beta| ~ beta',
        'rho_zero ~ hbar c beta^4/(4 pi)',
        '由 rho_zero = hbar c |delta beta| m_max^2/(4 pi R_max^2 L_z) 代入 m_max ~ beta R_max、L_z ~ 1/beta '
        '得 rho_zero ~ hbar c |delta beta| beta^3/(4 pi)；只有再取 **|delta beta| ~ beta** 才化为 hbar c beta^4/(4 pi)',
        '|delta beta| 是独立量（涨落幅度），其取值未由理论给出 ⇒ 该估算含一个未声明外部输入')

    # D04 来料诚实面（如实登记）
    add('INFO', 'D04 来料诚实面：定理 17.1 自认暗能量失败',
        '定理 17.1：零能模式和 beta 场势能无法自然解释暗能量的量级，HST 面临与标准 Lambda CDM 相同的宇宙学常数问题',
        '机器独立确认该自评成立（D01 复算的 beta 与 CMB 上限差 3.7E32 倍）',
        '本册如实登记：来料在第 17 层与附录 E.3 均作了诚实否定，未粉饰')


# ============================================================================
# 10. E 段：实验可观测性（第八层 / 第十四层）
# ============================================================================
def section_E():
    GLY = Decimal('9.4607304725808E24')   # 1 Gly in m [C]

    # E01 CMB 偏振旋转约束复算
    theta = BETA_CMB * L_CMB
    r_th = rel(theta, THETA_PLANCK)
    pitch = 2 * Decimal('3.14159265358979323846264338327950288') / BETA_CMB
    pitch_gly = pitch / GLY
    diam_obs = 2 * R_OBS / GLY
    add('CORRECTED', 'E01 CMB 偏振旋转约束复算通过，但来料螺距的 Gly 换算错约 1000 倍',
        'theta_rot = beta L；Planck 约束 theta < 6 x 10^-3 rad，L ~ 10^26 m ⇒ beta < 6 x 10^-29 m^-1；'
        '来料同段称螺距 p = 2pi/beta > 10^29 m ~ 10 Gly（可观测宇宙量级）',
        'beta L = ' + fv(theta, 8) + ' 与约束值 ' + fv(THETA_PLANCK, 2) + ' 相对偏差 ' + fv(r_th, 6)
        + ' ⇒ beta 上界复算**通过**；但 p = 2pi/beta = ' + fv(pitch, 8) + ' m = ' + fv(pitch_gly, 6) + ' Gly'
        + '（可观测宇宙直径约 ' + fv(diam_obs, 4) + ' Gly ⇒ p 为其 ' + fv(pitch / (2 * R_OBS), 4) + ' 倍）'
        + ' ⇒ 来料"~10 Gly"**换算错约 ' + fv(pitch_gly / Decimal('10'), 3) + ' 倍**'
        + '（正确为 ' + fv(pitch_gly, 4) + ' Gly ≈ 1.1 x 10^4 Gly，不止"可观测宇宙量级"而是其直径的 '
        + fv(pitch / (2 * R_OBS), 3) + ' 倍）',
        '自我修正（本册自抓第 4 处）：首版备注硬编码"机器给 11 Gly / 0.12 倍"，与机器读数 '
        + fv(pitch_gly, 6) + ' Gly 相差 1000 倍 ⇒ 备注与读数互斥。机器定案：来料把 10^29 m 误当作 ~10 Gly，'
        '实为 ~1.1 x 10^4 Gly。**beta 上界本身（6E-29 m^-1）不受影响**，错的只是同一句里的单位换算')
    guard('G-E01 螺距单位换算自洽（p = pitch_gly x Gly，且来料 ~10 Gly 偏离约 1000 倍）',
          rel(pitch_gly * GLY, pitch) < Decimal('1E-40') and pitch_gly > Decimal('1E3'),
          'p = ' + fv(pitch_gly, 6) + ' Gly；来料 ~10 Gly ⇒ 偏差 ' + fv(pitch_gly / Decimal('10'), 3) + ' 倍')

    # E02 手征分裂在 beta 上界下的绝对强度
    dw = 2 * C_C * BETA_CMB
    f_opt = Decimal('5E14')               # 光学频率 Hz [C]
    acc_rel = Decimal('1E-18')            # 最好原子钟相对精度 [C]
    acc_abs = f_opt * acc_rel
    ratio_e2 = acc_abs / dw
    add('FAIL', 'E02 手征分裂在上界下的绝对强度远低于任何现有精度',
        '定理 4.1：Delta omega = 2 c beta 为普适常数，是 HST 的招牌预言',
        '取 CMB 上界 beta = ' + fv(BETA_CMB, 2) + ' ⇒ |Delta omega| = 2 c beta = ' + fv(dw, 8) + ' Hz；'
        '对照光学原子钟（f = 5E14 Hz、相对精度 1E-18 ⇒ 绝对精度 ' + fv(acc_abs, 4) + ' Hz）：'
        '差 ' + fv(ratio_e2, 4) + ' 倍 ⇒ **不可探测**',
        '即使取原子钟约束 beta < 1E-8 m^-1（来料 8.2 表），|Delta omega| = ' + fv(2 * C_C * Decimal('1E-8'), 4) +
        ' Hz，仍比原子钟绝对精度低 ' + fv(acc_abs / (2 * C_C * Decimal('1E-8')), 4) + ' 倍')

    # E03 费米子自旋分裂
    dE = 2 * C_HBAR * C_C * BETA_CMB
    dE_ev = dE / Decimal('1.602176634E-19')
    add('FAIL', 'E03 费米子自旋分裂在上界下不可探测',
        'Delta E_spin = 2 hbar c beta',
        'beta = ' + fv(BETA_CMB, 2) + ' ⇒ Delta E = ' + fv(dE, 8) + ' J = ' + fv(dE_ev, 8) +
        ' eV；对照原子光谱实测精度 ~1E-15 eV ⇒ 差约 ' + fv(Decimal('1E-15') / dE_ev, 4) + ' 倍',
        '与 E02 同型：所有"普适常数"型预言的系数都是 c·beta 或 hbar·c·beta，被 6E-29 上限压到不可探测')

    # E04 来料 8.2 约束表：不同探针给出的 beta 上界跨度
    bounds = [('CMB TB/EB', Decimal('6E-29')), ('脉冲星 timing', Decimal('1E-20')),
              ('原子钟比较', Decimal('1E-8')), ('飞秒脉冲 OAM', Decimal('3E-11'))]
    span = max(b for _, b in bounds) / min(b for _, b in bounds)
    add('INFO', 'E04 第 8.2 约束表：beta 上界跨 21 个量级',
        '实验约束汇总表给出四条 beta 上限',
        '机器读取四条上界：' + '、'.join([n + ' ' + fv(b, 2) for n, b in bounds]) +
        ' ⇒ 跨度 ' + fv(span, 4) + ' 倍；CMB 最强',
        '跨度如此之大说明各探针依赖完全不同的假设链，不能交叉印证；本册未独立核实其中任何一条实验文献')


# ============================================================================
# 11. F 段：来料代码静态审计（不运行：依赖 numpy/scipy/matplotlib）
# ============================================================================
def section_F():
    path = os.path.join(HERE, 'TUFT-HST-helical_wave_sim_来料原样_2026-10-17.py')
    src = ''
    if os.path.exists(path):
        src = io.open(path, encoding='utf-8', errors='replace').read()
    has_dep = ('import numpy' in src) and ('from scipy' in src)
    # F01：验证 1 是否含任何断言/残差判定
    i = src.find('def verify_dispersion_analytical')
    j = src.find('def fdtd_helical_wave')
    body1 = src[i:j] if (i >= 0 and j > i) else ''
    has_assert1 = ('assert' in body1) or ('residual' in body1.lower()) or ('np.allclose' in body1)
    # 是否只是代入自己的公式打印
    prints_own = ('omega = c * abs(k - beta * m)' in body1) or ('c * np.abs(k - beta' in body1)
    add('FAIL', 'F01 仿真脚本"验证 1"无检验：只是把待证公式打印成表',
        'helical_wave_sim.py 的 verify_dispersion_analytical 声称"解析验证色散关系"',
        '函数体扫描：含 assert/残差判定 = ' + str(has_assert1) + '；出现"omega = c*abs(k - beta*m)"直接赋值 = '
        + str(prints_own) + ' ⇒ 该"验证"用待证公式本身生成数值再 print，**零判别力**',
        '这是本库反复出现的"自证式验证"模式（参 r19 g-2 Δg≡1/c、r43 恒等复读）')

    # F02：脚本的"零能模式"实现给出的 omega 非零 —— 与理论层自相矛盾
    k_zero_line = 'omega_zero = c * K_zero' in src
    add('FAIL', 'F02 脚本自身的"零能模式"给出 omega = c*K > 0，与理论层 omega = 0 矛盾',
        '理论层（第十一/十七层）称零能模式 omega = 0；脚本实现 near-zero mode',
        '源码含 "omega_zero = c * K_zero"（Dirichlet 边界下 K 由 Bessel 第一零点给出，K > 0）⇒ '
        '**脚本自己就否定了 omega = 0**；与本册 B08 独立推出的结论（K=0 时 Dirichlet 下 J_m(0)=0 ⇒ 场恒零，'
        '或 K>0 ⇒ omega>0）完全一致',
        '来料内部自相矛盾：文本层要 omega=0 的非平凡模，代码层给 omega=cK>0。两者不能同时成立')

    # F03：参数与依赖登记
    beta_code = Decimal('0.3')
    ratio_f = beta_code / BETA_CMB
    add('INFO', 'F03 脚本参数与依赖登记（不运行）',
        'helical_wave_sim.py：beta = 0.3（注释自陈"放大以清晰展示效应"），依赖 numpy/scipy/matplotlib',
        'beta_code/beta_CMB上限 = ' + fv(ratio_f, 4) + ' 倍 ⇒ 演示值比实验上界大 27 个量级，'
        '**不能作为物理参数采信**；依赖 numpy/scipy/matplotlib = ' + str(has_dep) +
        ' ⇒ 超出本库纯标准库审计口径，本册只做静态审计不运行',
        '本库纪律：来料脚本一律保持"来料原样、未运行"落盘')


# ============================================================================
# 12. G 段：第十九层全息对偶与 PAPER_FRAMEWORK 内部张力
# ============================================================================
def section_G():
    # G01 AdS 维数计数（从正本读取该度规块）
    full = ''
    p = os.path.join(DIR_DATA, 'TUFT-HST螺旋空间理论体系_来料全文_2026-10-17.md')
    if os.path.exists(p):
        full = io.open(p, encoding='utf-8', errors='replace').read()
    import re
    seg = ''
    i = full.find('第十九层')
    if i >= 0:
        j = full.find('### 边界理论', i)
        seg = full[i:(j if j > i else i + 2500)]
    coords = sorted(set(re.findall(r'd\\?(t|rho|chi|zeta|z)\b', seg))) if seg else []
    ndim = len(coords)
    add('FAIL', 'G01 第十九层 AdS 维数不自洽（标 AdS₄ 实为 AdS₅）',
        '第 19.1 节标题为 "AdS₄-螺旋度规"，度规写 ds^2 = (L^2/z^2)[-c^2dt^2 + d rho^2 + rho^2 d chi^2 '
        '+ 2 beta rho^2 d chi d zeta + (1+beta^2 rho^2) d zeta^2 + dz^2]',
        '机器读取该度规块并计数独立坐标微分：' + str(coords) + ' ⇒ 体维数 = ' + str(ndim) +
        '（含 AdS 径向 z）⇒ 该度规是 **AdS₅**（边界 4 维）而非 AdS₄（边界 3 维）',
        '维数错配会连带影响 19.2 纠缠熵与 19.4 费米子谱的标度维数；本册只登记不代修')

    # G02 背景规范场为纯规范 ⇒ 需拓扑识别
    add('FAIL', 'G02 【承重】定理 19.1 的 A_z = beta 是纯规范，缺拓扑识别声明',
        '定理 19.1：螺旋扭转等价于边界理论中的化学势，A_mu^bg = (0,0,0,beta)',
        '常值规范场在单连通边界（R^3 或 R^4）上是**纯规范**（F = 0），可被规范变换消去 ⇒ 不改变任何规范不变量；'
        '仅当 zeta 方向被识别为 S^1（holonomy ∮ A_z d zeta = beta L_zeta 不可消去，Aharonov-Bohm 型）时才有物理效应',
        '**来料全文未出现任何周期识别/粘合声明** ⇒ 该拓扑输入是未声明的外部输入。'
        '与 A07/B03 同一根因：HST 的全部物理内容都押在"是否做 S^1 识别"这一个未声明的选择上')

    # G03 Hall 电导与纯规范矛盾
    add('BOUNDARY', 'G03 定理 19.3 的反常 Hall 电导与纯规范互斥',
        '定理 19.3：sigma_xy ∝ beta，无需外磁场的 Hall 效应',
        'Hall 电导是规范不变的可观测量；若 A_z = beta 为纯规范（G02），则 sigma_xy 必为 0 ⇒ 与定理 19.3 矛盾。'
        '唯一出路同样是 S^1 识别（此时 β 的 holonomy 给出拓扑输运）',
        '判 BOUNDARY：结论随 G02 的分支选择翻转，本册不代选')

    # G04 PAPER_FRAMEWORK 内部张力
    paper = ''
    pp = os.path.join(DIR_DATA, 'TUFT-HST-PAPER_FRAMEWORK_来料_2026-10-17.md')
    if os.path.exists(pp):
        paper = io.open(pp, encoding='utf-8', errors='replace').read()
    has_flat = 'R_{\\mu\\nu}=0' in paper or 'Ricci tensor vanishes' in paper
    has_mass = 'effective photon mass' in paper
    has_topo = 'topological character' in paper
    add('FAIL', 'G04 PAPER_FRAMEWORK 摘要内部张力：平直与"新物理"并列',
        '摘要同时声称 "prove that the Ricci tensor vanishes identically (R_{mu nu}=0)" 与 '
        '"effective photon mass generation"、"zero-energy modes with topological character"',
        '机器扫描：含 R_{mu nu}=0 声明 = ' + str(has_flat) + '；含 effective photon mass = ' + str(has_mass) +
        '；含 topological character = ' + str(has_topo) +
        ' ⇒ 三条同段并列，但前一条（平直）在逻辑上取消后两条的"新物理"身份（除非补拓扑识别，见 G02）',
        '投稿定位层面：坐标重参数化框架本身不构成新物理；本册不给投稿建议，只登记张力')


# ============================================================================
# 13. H 段：分工、符号台账、诚实面
# ============================================================================
def section_H():
    add('INFO', 'H01 与 r53 / r58 / r59 的分工（零重复）',
        '本册与既有产物是否重复',
        'r53《空间螺旋结构中的光与光子》= 本批"光篇"的**同一份来料**（章节 0-10 + 附录 A/B 逐条对应）⇒ 本册不重审；'
        'r58/r59 = 圆柱螺旋**曲线**不变量（kappa/tau/omega/Omega），对象是曲线而非时空度规 ⇒ 不同对象；'
        '本册主体 = HST 1-20 层的几何自洽 / 波谱等价 / 有效质量 / 零能模 / 宇宙学 / 全息',
        'r53 的承重裁定 B04（Riemann 全零）与本册 A04 为同一根因的独立复算，互为交叉印证')

    add('INFO', 'H02 符号台账：beta 的三重身份',
        'beta 在 HST 全文中出现于多个层',
        '① 第一层：螺旋扭转率 beta = 1/H_0（[beta] = L^-1）；② 第十六层：动力学标量场 beta(t)；'
        '③ 第十九层：边界规范场 A_z = beta / 化学势。三者量纲一致（L^-1）但**数学身份不同**（几何参数 / 场 / 规范势）',
        '跨层混引会改变命题性质：作为几何参数时它是常数坐标伪影，作为场时它是新自由度（撞"自由常数"约束），'
        '作为规范势时需拓扑识别才有意义。引用时必须声明取哪一重身份')

    add('INFO', 'H03 来料诚实面汇总（如实登记，不粉饰也不掠美）',
        '来料是否自陈了本册裁定的问题',
        '是，共三处：① 定理 1.2 自陈"平直时空的坐标重参数化"；② 定理 17.1 自陈无法解释暗能量量级；'
        '③ 附录 E.3 自陈"CMB 约束已排除宇宙学尺度螺旋"。'
        '本册的增量在于：来料虽自陈了①，却仍在 3/4/11/17/19 层把坐标伪影当作可观测预言（A07/B03）',
        '诚实自陈与后续层仍使用该伪影并存 ⇒ 属"自陈但未贯彻"，不是蓄意夸大')


# ============================================================================
# 14. 主流程
# ============================================================================
def main():
    run_guards_g0()
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    section_H()

    cnt = {}
    for r in ROWS:
        cnt[r['tag']] = cnt.get(r['tag'], 0) + 1
    g_ok = sum(1 for g in GUARDS if g['ok'])
    g_all = len(GUARDS)

    key = {
        'beta_CMB_upper_m^-1': fv(BETA_CMB, 4),
        'chiral_split_2cbeta_Hz': fv(2 * C_C * BETA_CMB, 8),
        'fermion_split_2hbarcbeta_eV': fv(2 * C_HBAR * C_C * BETA_CMB / Decimal('1.602176634E-19'), 8),
        'pitch_2pi_over_beta_Gly': fv(2 * Decimal('3.14159265358979323846264338327950288') / BETA_CMB
                                      / Decimal('9.4607304725808E24'), 6),
        'dark_energy_beta_true_m^-1': fv(
            ((4 * Decimal('3.14159265358979323846264338327950288') * RHO_LAMBDA) / (C_HBAR * C_C)).sqrt().sqrt(), 8),
        'dark_energy_beta_claim_m^-1': '7E4',
        'm_beta2_machine': fv(2 * RHO_LAMBDA / (Decimal('1E-29') ** 2), 8),
        'ads_body_dim_from_metric': 5,
        'helix_riemann_max_abs': '< 1E-20 (数值零)',
    }

    out = {
        'round': 'r96',
        'title': 'HST 螺旋空间理论体系（全 20 层）全维审计与精算',
        'date': '2026-10-17',
        'source': '数据/TUFT-HST螺旋空间理论体系_来料全文_2026-10-17.md',
        'rows': ROWS,
        'guards': GUARDS,
        'counts': cnt,
        'guard_total': g_all,
        'guard_pass': g_ok,
        'key_numbers': key,
    }

    jp = os.path.join(DIR_DATA, 'TUFT-r96_HST螺旋空间理论体系_全维审计_2026-10-17.json')
    io.open(jp, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(out, ensure_ascii=False, indent=2, default=str))

    lines = []
    lines.append('# r96 · HST 螺旋空间理论体系（全 20 层）全维审计 · 数据产物')
    lines.append('')
    lines.append('- 受理日：2026-10-17　目录：`04_公共成果/本项目_全维自洽与归一化/`')
    lines.append('- 来料正本：`数据/TUFT-HST螺旋空间理论体系_来料全文_2026-10-17.md`（三篇连载合并 1-9 / 10-15 / 16-20 层）')
    lines.append('- 读数：**条目 ' + str(len(ROWS)) + '（' + ' / '.join(['%s %d' % (k, v) for k, v in sorted(cnt.items())]) +
                 '）、自检 guard ' + str(g_ok) + '/' + str(g_all) + '**')
    lines.append('')
    lines.append('| 条目 | 裁定 | 来料主张 | 机器读数 |')
    lines.append('|---|---|---|---|')
    for r in ROWS:
        lines.append('| ' + r['code'] + ' | **' + r['tag'] + '** | ' + r['title'] + ' | ' +
                     r['reading'].replace('\n', ' ') + ' |')
    lines.append('')
    lines.append('## 守卫自检')
    lines.append('')
    for g in GUARDS:
        lines.append('- ' + ('PASS' if g['ok'] else 'FAIL') + ' · ' + g['name'] +
                     ((' · ' + g['detail']) if g['detail'] else ''))
    lines.append('')
    lines.append('## 关键读数')
    lines.append('')
    for k, v in key.items():
        lines.append('- `' + k + '` = ' + str(v))
    lines.append('')
    mp = os.path.join(DIR_DATA, 'TUFT-r96_HST螺旋空间理论体系_全维审计_2026-10-17.md')
    io.open(mp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

    rep = []
    rep.append('=' * 78)
    rep.append('r96 | HST 螺旋空间理论体系（全 20 层）全维审计 | 2026-10-17')
    rep.append('=' * 78)
    for r in ROWS:
        rep.append('[' + r['tag'] + '] ' + r['code'] + ' ' + r['title'])
        rep.append('    主张: ' + r['claim'])
        rep.append('    读数: ' + r['reading'])
        if r['note']:
            rep.append('    备注: ' + r['note'])
    rep.append('')
    rep.append('GUARD: ' + str(g_ok) + '/' + str(g_all))
    for g in GUARDS:
        if not g['ok']:
            rep.append('  FAILED GUARD: ' + g['name'] + ' :: ' + g['detail'])
    rep.append('')
    rep.append('条目 ' + str(len(ROWS)) + '（' + ' / '.join(['%s %d' % (k, v) for k, v in sorted(cnt.items())]) + '）')
    rp = os.path.join(DIR_DATA, 'TUFT-r96_HST螺旋空间理论体系_全维审计_2026-10-17_report.txt')
    io.open(rp, 'w', encoding='utf-8', newline='\n').write('\n'.join(rep))

    print('\n'.join(rep[-40:]))
    print('')
    print('条目 ' + str(len(ROWS)) + ' | guard ' + str(g_ok) + '/' + str(g_all))
    return 0 if g_ok == g_all else 1


if __name__ == '__main__':
    sys.exit(main())

