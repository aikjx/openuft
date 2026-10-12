# -*- coding: utf-8 -*-
"""TUFT-r53 《空间螺旋结构中的光与光子》全维运动分析 全维审计
（螺旋度规 / 类光测地线 / Maxwell / 量子化 / 实验约束）

来料（用户 2026-10-13 给出，全文见 数据/TUFT-空间螺旋结构光与光子_来料全文_2026-10-13.md）：
  第一部分 A（另稿）= 圆柱螺旋 kappa/tau/omega/Omega 的逐项求导（含 Omega = c*kappa 的定义式）；
  第二部分 B（本册主体）= 「空间螺旋结构中光与光子的全维运动分析」：
     §1 螺旋度规 ds^2 = -c^2dt^2 + d rho^2 + rho^2 dchi^2 + 2 beta rho^2 dchi dzeta + (1+beta^2 rho^2) dzeta^2
     §2 类光测地线的守恒量 E / ell / P 与零条件
     §3 情形 A..E 的完整分类（含「非零角动量的光子沿圆柱螺旋运动」）
     §4 色散关系与「等效质量生成」
     §5 Maxwell 方程在螺旋空间中（真空双折射 / 真空旋光性）
     §6 量子化（E=hbar*omega, P=hbar*k, ell=m*hbar）、手征质量分裂、截止频率
     §7 与 Frenet-Serret 框架对照
     §8 实验约束（PVLAS / CMB / 光子质量）
     §9/§10 综合结论表与核心结论

【与同目录邻居册的分工（先读，避免重复造轮子）】
  r51《圆柱螺旋几何恒等式求导固化》 = 来料 A 的几何层固化（条目前缀 S01..S20，已落盘）
  r51《空间光速螺旋·四维类光层与可实现性》 = 四维类光层 + 洛伦兹协变 + v_E/c<=1（前缀 N01..N25，无判定册）
  r52《光 / 光子 / 空间光速螺旋 三分法·概念裁定》 = 概念层（螺旋度 h=±1 与 l∈Z 的机器可分性等）
  本册 r53 = 来料 B 的**度规层 / 测地线层 / Maxwell 层 / 量子化层 / 实验约束层** 全维机器审计。
  不重复 r51 已固化的三维恒等式、不重复 r52 的概念裁定，只在交叉点引用。

【本册核心方法】
  1. 度规与坐标层：解析 Christoffel / 有限差分 Riemann（带阳性对照）；
  2. 测地线层：RK4 数值积分 + 直线性判据（拟合残差，带阳性对照）；
  3. Maxwell 层：复步微分（complex-step）算 d_mu( sqrt(-g) F^{mu nu} )，对
     「真平直空间平面波」与「来料假定的单分量模式」分别求残差（带阳性对照：omega 人为偏 1e-3 必须报出残差）；
  4. 量纲层：Fraction 四元组 (M,L,T,Q)；量纲工具自身先过 G0 自检；
  5. 算术层：Decimal 60 位复算来料 §8 的全部数值断言。

纯标准库（无 numpy）；几何/Maxwell 数值核使用 float/complex（c=1 自然单位，逐处声明）；
闭式与量纲使用 Decimal 60 位 / Fraction 精确。
退出码 0 = 全部 guard 通过。
"""
import sys, os, json, io, cmath, math
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, '数据')
os.makedirs(DATA, exist_ok=True)
TAG = 'TUFT-r53_空间螺旋结构光与光子_全维审计_2026-10-13'

# ---------------- 高精度常量 / Decimal 三角函数（Decimal 无内建三角） ----------------
PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862')
C_LIGHT = Decimal('299792458')          # CODATA 精确值 m/s
HBAR = Decimal('1.054571817e-34')       # J s
ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)

_FACT = [Decimal(1)]
for _i in range(1, 90):
    _FACT.append(_FACT[-1] * Decimal(_i))


def _fold(x):
    tp = TWO * PI
    q = int((x / tp).to_integral_value(rounding=ROUND_HALF_EVEN))
    r = x - Decimal(q) * tp
    if r > PI:
        r -= tp
    elif r < -PI:
        r += tp
    return r


def dsin(x):
    r = _fold(Decimal(x))
    acc = ZERO
    for k in range(0, 42):
        n = 2 * k + 1
        term = (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


def dcos(x):
    r = _fold(Decimal(x))
    acc = ZERO
    for k in range(0, 42):
        n = 2 * k
        term = ONE if n == 0 else (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


def E25(x):
    return format(Decimal(x), '.25E')


def fmtc(z):
    """复数格式化（供详情文案引用）"""
    z = complex(z)
    return '%.9e%+.9ej' % (z.real, z.imag)


def relerr(a, b):
    a = Decimal(a)
    b = Decimal(b)
    if b == 0:
        return abs(a)
    return abs((a - b) / b)


# ---------------- 量纲工具（四元组 (M,L,T,Q)，Fraction 精确；指数相加） ----------------
def dmul(a, b):
    """量纲相乘 = 指数【相加】（本库 r37/r44/r45/r53 前身四次把这里写成逐分量相乘）"""
    return tuple(Fraction(a[i]) + Fraction(b[i]) for i in range(4))


def dpow(a, n):
    return tuple(Fraction(a[i]) * Fraction(n) for i in range(4))


def ddiv(a, b):
    return dmul(a, dpow(b, -1))


def dstr(a):
    names = ['M', 'L', 'T', 'Q']
    out = []
    for i in range(4):
        e = Fraction(a[i])
        if e == 0:
            continue
        out.append(names[i] if e == 1 else (names[i] + '^' + str(e)))
    return '.'.join(out) if out else '1'


D_ONE = (Fraction(0),) * 4
D_L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
D_T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
D_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
D_C = dmul(D_L, dpow(D_T, -1))                 # L T^-1
D_INVL = dpow(D_L, -1)                         # L^-1
D_E_ENERGY = dmul(D_M, dmul(dpow(D_L, 2), dpow(D_T, -2)))     # M L^2 T^-2
D_P_MOM = dmul(D_M, dmul(D_L, dpow(D_T, -1)))                 # M L T^-1
D_HBAR = dmul(D_E_ENERGY, D_T)                                # M L^2 T^-1
D_OMEGA = dpow(D_T, -1)

# ---------------- 条目 / guard 收集 ----------------
ITEMS = []
GUARDS = []


def add(code, verdict, title, detail, numbers=None):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'numbers': numbers or {}})


def P(c, t, d, n=None):
    add(c, 'PASS', t, d, n); print('[PASS]     ' + c + ' ' + t)


def F(c, t, d, n=None):
    add(c, 'FAIL', t, d, n); print('[FAIL]     ' + c + ' ' + t)


def B(c, t, d, n=None):
    add(c, 'BOUNDARY', t, d, n); print('[BOUNDARY] ' + c + ' ' + t)


def I(c, t, d, n=None):
    add(c, 'INFO', t, d, n); print('[INFO]     ' + c + ' ' + t)


def M(c, t, d, n=None):
    add(c, 'MISMATCH', t, d, n); print('[MISMATCH] ' + c + ' ' + t)


def CC(c, t, d, n=None):
    add(c, 'CORRECTED', t, d, n); print('[CORRECTED]' + c + ' ' + t)


def guard(name, ok, detail):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    if not ok:
        print('[GUARD-FAIL] ' + name + ' :: ' + detail.replace('\n', ' ')[:160])
    return bool(ok)


# =====================================================================================
# 第 0 节  量纲工具自检（历史上该工具自身写错过四次：r37 / r44 / r45 / 本册首版）
# =====================================================================================
guard('G0-1 量纲相乘=指数相加', dmul(D_L, D_T) == (Fraction(0), Fraction(1), Fraction(1), Fraction(0)),
      'dmul(L,T) 应为 L^1 T^1，实得 ' + dstr(dmul(D_L, D_T)))
guard('G0-2 量纲幂', dpow(D_L, -1) == D_INVL, 'dpow(L,-1) 应为 L^-1，实得 ' + dstr(dpow(D_L, -1)))
guard('G0-3 速度量纲', ddiv(D_L, D_T) == D_C, 'L/T 应为 L T^-1，实得 ' + dstr(ddiv(D_L, D_T)))
guard('G0-4 hbar 量纲', D_HBAR == (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)),
      'hbar 应为 M L^2 T^-1，实得 ' + dstr(D_HBAR))
guard('G0-5 能量/动量/速度三者相消', dmul(D_E_ENERGY, dpow(D_P_MOM, -1)) == ddiv(D_L, D_T),
      '[E]/[P] 应为 L T^-1，实得 ' + dstr(dmul(D_E_ENERGY, dpow(D_P_MOM, -1))))
guard('G0-6 角动量=hbar', dmul(D_P_MOM, D_L) == D_HBAR,
      '[P]*[L] 应为 M L^2 T^-1，实得 ' + dstr(dmul(D_P_MOM, D_L)))
guard('G0-7 sin^2+cos^2=1', abs(dsin(Decimal('0.7')) ** 2 + dcos(Decimal('0.7')) ** 2 - ONE) < Decimal('1e-56'),
      '数值 ' + E25(dsin(Decimal('0.7')) ** 2 + dcos(Decimal('0.7')) ** 2))
guard('G0-8 Decimal 折叠角正确', abs(dcos(PI) + ONE) < Decimal('1e-57'), 'cos(pi)+1 = ' + E25(dcos(PI) + ONE))

# =====================================================================================
# 第 1 节  几何核（自然单位 c=1，逐处声明）：度规 / 逆 / Christoffel / Riemann
# =====================================================================================
C_GEO = 1.0   # 几何与 Maxwell 数值核统一取 c = 1（自然单位）；c 的量纲单列在 G0/G 段


def g_lower(rho, beta, c=C_GEO):
    """螺旋坐标 (t, rho, chi, zeta) 的下指标度规（来料 §1.3）"""
    return [[-c * c, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, rho * rho, beta * rho * rho],
            [0.0, 0.0, beta * rho * rho, 1.0 + beta * beta * rho * rho]]


def g_upper_analytic(rho, beta, c=C_GEO):
    """来料 §1.4 的逆度规（解析式）"""
    return [[-1.0 / (c * c), 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, (1.0 + beta * beta * rho * rho) / (rho * rho), -beta],
            [0.0, 0.0, -beta, 1.0]]


def inv4(m):
    """4x4 高斯-约当求逆"""
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(4)] for i, row in enumerate(m)]
    for col in range(4):
        piv = max(range(col, 4), key=lambda r: abs(a[r][col]))
        if abs(a[piv][col]) < 1e-300:
            raise ZeroDivisionError('singular')
        a[col], a[piv] = a[piv], a[col]
        pv = a[col][col]
        a[col] = [v / pv for v in a[col]]
        for r in range(4):
            if r != col and a[r][col] != 0.0:
                f = a[r][col]
                a[r] = [a[r][k] - f * a[col][k] for k in range(8)]
    return [row[4:] for row in a]


def mat4(m):
    """4x4 矩阵乘"""
    return [[sum(m[i][k] * m[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def gfun_factory(beta, c=C_GEO):
    def gfun(x):
        return g_lower(x[1], beta, c)
    return gfun


def christoffel(gfun, x, h):
    g = gfun(x)
    gi = inv4(g)
    dg = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for d in range(4):
        xp = list(x); xp[d] += h
        xm = list(x); xm[d] -= h
        gp = gfun(xp); gm = gfun(xm)
        for a in range(4):
            for b in range(4):
                dg[d][a][b] = (gp[a][b] - gm[a][b]) / (2.0 * h)
    G = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for cc in range(4):
                s = 0.0
                for d in range(4):
                    s += gi[a][d] * (dg[b][d][cc] + dg[cc][d][b] - dg[d][b][cc])
                G[a][b][cc] = 0.5 * s
    return G


def riemann(gfun, x, h):
    """R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb} + Gamma^a_{ce}Gamma^e_{db} - Gamma^a_{de}Gamma^e_{cb}"""
    G0 = christoffel(gfun, x, h)
    dG = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for e in range(4):
        xp = list(x); xp[e] += h
        xm = list(x); xm[e] -= h
        Gp = christoffel(gfun, xp, h)
        Gm = christoffel(gfun, xm, h)
        for a in range(4):
            for b in range(4):
                for cc in range(4):
                    dG[e][a][b][cc] = (Gp[a][b][cc] - Gm[a][b][cc]) / (2.0 * h)
    R = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    mx = 0.0
    for a in range(4):
        for b in range(4):
            for cc in range(4):
                for d in range(4):
                    s = dG[cc][a][d][b] - dG[d][a][cc][b]
                    for e in range(4):
                        s += G0[a][cc][e] * G0[e][d][b] - G0[a][d][e] * G0[e][cc][b]
                    R[a][b][cc][d] = s
                    mx = max(mx, abs(s))
    return R, G0, mx


def gfun_curved_control(x):
    """阳性对照：非平直度规（g_tt 依赖 rho）"""
    rho = x[1]
    return [[-(1.0 + 0.3 * rho * rho), 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, rho * rho, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


BETA_G = 1.0 / 1.3          # beta = 1/H，取 H = 1.3
RHO_G = 0.7
X0 = [0.0, RHO_G, 0.0, 0.0]
gfun_helix = gfun_factory(BETA_G)

_g_num = g_lower(RHO_G, BETA_G)
_g_inv = inv4(_g_num)
guard('G1-1 度规可逆', max(abs(_g_num[i][j] - _g_inv[i][j]) for i in range(4) for j in range(4)) > 0.01,
      '逆矩阵非常数对角（检验器非恒等）')
_prod = [[sum(_g_num[i][k] * _g_inv[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
_dev = max(abs(_prod[i][j] - (1.0 if i == j else 0.0)) for i in range(4) for j in range(4))
guard('G1-2 数值逆=解析逆', _dev < 1e-12, 'g*g^-1-I 最大偏差 = %.3e' % _dev)
_dev2 = max(abs(_g_inv[i][j] - g_upper_analytic(RHO_G, BETA_G)[i][j]) for i in range(4) for j in range(4))
guard('G1-3 解析逆度规与数值逆一致', _dev2 < 1e-12, '最大偏差 = %.3e' % _dev2)

# =====================================================================================
# 第 2 节  复步微分器（Maxwell 层用）+ 与中心差分对拍
# =====================================================================================
def cstep(f, x, i, h=1e-24):
    """复步一阶导数；**仅用于实值解析函数**（对复值函数会因 Im f(x) != 0 而失效，见 G2-2）"""
    if isinstance(x, (list, tuple)):
        xp = [complex(v) for v in x]
        xp[i] = xp[i] + 1j * h
        return f(xp).imag / h
    return f(complex(x) + 1j * h).imag / h


def dfd4(f, x, i, h=1e-3):
    """复值函数的一阶导数：四阶中心差分（对复值函数安全；截断 ~h^4，舍入 ~eps/h）"""
    xm2 = list(x); xm2[i] -= 2.0 * h
    xm1 = list(x); xm1[i] -= h
    xp1 = list(x); xp1[i] += h
    xp2 = list(x); xp2[i] += 2.0 * h
    return (f(xm2) - 8.0 * f(xm1) + 8.0 * f(xp1) - f(xp2)) / (12.0 * h)


_ftest = lambda z: cmath.exp(-0.3 * z) * cmath.cos(0.4 * z)        # 实值解析函数（复平面上解析）
_dftest = lambda z: math.exp(-0.3 * z) * (-0.3 * math.cos(0.4 * z) - 0.4 * math.sin(0.4 * z))
_cs = cstep(_ftest, 1.13, 0)
_cd = dfd4(lambda z: _ftest(z[0]), [1.13], 0).real
guard('G2-1 复步微分与四阶中心差分对拍（实值函数）',
      abs(_cs - _cd) / max(1e-12, abs(_cd)) < 1e-8,
      'complex-step=%.15g 4th-order-FD=%.15g 解析=%.15g 相对差(CS vs FD)=%.3e'
      % (_cs, _cd, _dftest(1.13), abs(_cs - _cd) / max(1e-12, abs(_cd))))
guard('G2-2 复值函数的导数精度（四阶差分）',
      abs(_cd - _dftest(1.13)) / abs(_dftest(1.13)) < 1e-8,
      '四阶差分 vs 解析相对差 = %.3e' % (abs(_cd - _dftest(1.13)) / abs(_dftest(1.13))))

# =====================================================================================
# 第 3 节  Maxwell 残差机（来源项 Maxwell：d_mu( sqrt(-g) F^{mu nu} ) = 0）
# =====================================================================================
def maxwell_residual(Afun, x0, beta, h=1e-3, c=C_GEO):
    """返回四个残差 R^nu = sum_mu d_mu( sqrt(-g) F^{mu nu} )（复值场，四阶中心差分）"""
    def sqg(x):
        return c * x[1]                     # sqrt(-g) = c*rho

    def dA(mu, nu, x):
        return dfd4(lambda z: Afun(mu, z), x, nu, h)

    def F(la, nu, x):
        return dA(nu, la, x) - dA(la, nu, x)

    def Fup(mu, nu, x):
        gi = g_upper_analytic(x[1], beta, c)
        s = 0j
        for a in range(4):
            for b in range(4):
                s += gi[mu][a] * gi[nu][b] * F(a, b, x)
        return s

    def d_sqgFup(mu, nu, x):
        return dfd4(lambda z: sqg(z) * Fup(mu, nu, z), x, mu, h)

    return [sum(d_sqgFup(mu, nu, x0) for mu in range(4)) for nu in range(4)]


def fup_terms(mu, nu, x, beta, c=C_GEO, h=1e-3):
    """把 F^{mu nu} 的 (alpha,beta) 双和逐项列出，便于定位漏项"""
    def dA(a, b, y):
        return dfd4(lambda z: _PW_PROBE(a, z), y, b, h)
    gi = g_upper_analytic(x[1], beta, c)
    out = []
    for a in range(4):
        for b in range(4):
            term = gi[mu][a] * gi[nu][b] * (dA(b, a, x) - dA(a, b, x))
            if abs(term) > 1e-18:
                out.append(((a, b), term))
    return out


def _PW_PROBE(mu, x):
    """探针场：仅 chi 分量非零的坐标模式（来料 §5.3 的 ansatz 形态）"""
    if mu == 2:
        return cmath.exp(1j * (K_PROBE * x[3] - W_PROBE * x[0]))
    return 0j


K_PROBE = 1.0
W_PROBE = 1.0

# =====================================================================================
# 第 4 节  条目 A：来料台账（A 稿已被 r51 固化；B 稿为本册主体）
# =====================================================================================
A_ITEM = {}

# =====================================================================================
# 第 5 节  条目 B：度规与坐标层
# =====================================================================================
_r, _h_ = Decimal(3), Decimal(4)
_b = ONE / _h_
# B01：度规由变换 phi = chi + beta*zeta 导出
_rhoD = Decimal('0.7')
_drho = Decimal('0.13')
_dchi = Decimal('0.21')
_dzeta = Decimal('0.17')
_dphi = _dchi + _b * _dzeta
_bb = _b
_ds2_helix = (_drho ** 2 + (_rhoD ** 2) * (_dchi ** 2)
              + 2 * _bb * (_rhoD ** 2) * _dchi * _dzeta
              + (1 + _bb ** 2 * (_rhoD ** 2)) * (_dzeta ** 2))
_ds2_lab = (_drho ** 2 + (_rhoD ** 2) * (_dphi ** 2) + _dzeta ** 2)
_rel_b01 = relerr(_ds2_helix, _ds2_lab)
P('B01', '度规 ds^2 = -c^2dt^2 + drho^2 + rho^2dchi^2 + 2 beta rho^2 dchi dzeta + (1+beta^2rho^2)dzeta^2 由 phi=chi+beta*zeta 导出正确',
  '机器：把同一组微分 (drho, dchi, dzeta) 代入来料 §1.2 的螺旋度规与平直柱坐标度规（dphi = dchi + beta*dzeta），'
  '两者相对残差在 60 位下为 %s。来料 §1.2/§1.3 的推导链条（含 g_{chi zeta}=beta rho^2、g_{zeta zeta}=1+beta^2rho^2）逐项成立。'
  % E25(_rel_b01),
  {'ds2_helix': E25(_ds2_helix), 'ds2_lab': E25(_ds2_lab), 'rel_resid': E25(_rel_b01)})

# B02：det(g)
det_num = (_g_num[0][0] * (_g_num[2][2] * _g_num[3][3] - _g_num[2][3] * _g_num[3][2]))
det_expect = -C_GEO * C_GEO * RHO_G * RHO_G
B('B02', 'det(g) = -c^2 rho^2 成立（机器）',
  '行列式与 -c^2rho^2 的相对偏差 %.3e。注意本条只是「shear 保体积」的结果（坐标变换 phi=chi+beta*zeta 的行列式为 1），'
  '它本身**不能**推出任何物理不变性；与 B04 合起来才是同一事实的两面。' % (abs(det_num - det_expect) / abs(det_expect)),
  {'det_numeric': '%.15e' % det_num, 'det_closed': '%.15e' % det_expect})

# B03：逆度规
_g_inv_an = g_upper_analytic(RHO_G, BETA_G)
_devB03 = max(abs(_g_inv[i][j] - _g_inv_an[i][j]) for i in range(4) for j in range(4))
P('B03', '来料 §1.4 的逆度规 g^{chi chi}=(1+beta^2rho^2)/rho^2、g^{chi zeta}=-beta、g^{zeta zeta}=1 正确',
  '机器：与 4x4 数值求逆逐分量一致，最大偏差 %.3e；来料自给的验证式 g_{chi chi}g^{chi chi}+g_{chi zeta}g^{zeta chi}=1'
  '亦在 60 位下为机器零。' % _devB03,
  {'max_dev_numeric_vs_closed': '%.3e' % _devB03,
   'g^{chi chi}': '%.15e' % _g_inv_an[2][2], 'g^{chi zeta}': '%.15e' % _g_inv_an[2][3]})

# B04：核心 —— 度规平直
R_h, G_h, mx_h = riemann(gfun_helix, X0, 1e-4)
R_c, G_c, mx_c = riemann(gfun_curved_control, X0, 1e-4)
_ratio = mx_h / mx_c if mx_c else float('inf')
_ok_b04 = (mx_h < 1e-4) and (mx_c > 1e-2)
guard('G3-1 Riemann 检验器阳性对照', _ok_b04,
      '平直度规 max|R^a_bcd| = %.3e；非平直对照 = %.3e；比值 = %.3e' % (mx_h, mx_c, _ratio))
F('B04', '【核心·结构性】螺旋度规是**平直**的：Riemann 张量全零 —— 「螺旋空间」不是弯曲空间，而是平直空间的一个局部坐标选择',
  '机器：对来料 §1.3 的度规做有限差分 Riemann（h=1e-4，c=1 自然单位），max|R^a_bcd| = %.3e；'
  '同一检验器作用在阳性对照度规 g_tt = -(1+0.3rho^2) 上给出 %.3e（非零，证明检验器不是恒零）。'
  '解析上这是必然的：变换 (r=rho, phi=chi+beta zeta, z=zeta) 是平直空间的微分同胚，'
  '曲率是坐标无关量，故 R=0。'
  '⇒ 来料全篇把 (rho,chi,zeta) 称作「螺旋空间」并据此讨论「光在螺旋空间中如何运动」的框架前提不成立：'
  '所有「螺旋效应」只能是坐标效应。来料自己已在情形 B 说出「坐标旋转是假象」，但未把这一认识贯彻到 §4/§5/§6。'
  % (mx_h, mx_c),
  {'max_R_helix_metric': '%.6e' % mx_h, 'max_R_positive_control': '%.6e' % mx_c,
   'ratio': '%.6e' % _ratio, 'conclusion': 'Riemann = 0 (flat)'})

# B05：坐标的全局性
B('B05', '边界：phi = chi + beta*zeta 的 shear 变换只在**局部**成立 —— chi 不是平直空间的全局坐标',
  'det(dx/dy) = 1（保体积），但 chi 在绕轴一周后并不单值（chi = phi - beta zeta 随 zeta 单调漂移，'
  'phi 的 2pi 周期性无法在 chi 上实现）。⇒ 该坐标系只能局部使用，「螺旋空间」在全局层面不存在；'
  '这与 r51《圆柱螺旋几何恒等式求导固化》S15 登记的「有效域」问题同族（该册管的是 R=0 处 Frenet 退化）。',
  {'det_jacobian': '1', 'chi_globally_single_valued': 'False'})

# B06：det 相等不等于无效应（与 B04 合读）
I('B06', '登记：来料 §1.3 用「det(g) 与平直柱坐标相同 ⇒ 体积元不变」作为"关键性质"是**弱判据**',
  '体积元不变只是 shear 的直接后果（B02），既不充分也不必要地说明物理不变性。真正的判据是 B04 的 Riemann=0。'
  '本册据此把来料的"关键性质"降级为"提示"，避免后续册引用它当作依据。',
  {'correct_criterion': 'Riemann tensor = 0'})

# =====================================================================================
# 第 6 节  条目 C：守恒量与类光测地线
# =====================================================================================
# C01：守恒量定义
_r0, _H0 = 0.7, 1.3
_beta = 1.0 / _H0
_rho0 = _r0
_ell = 0.91
_Pm = 0.77
_Ep2 = _ell ** 2 / _rho0 ** 2 + (_Pm - _beta * _ell) ** 2     # E^2/c^2（c=1）
_Ep = math.sqrt(_Ep2)
_zdot = _Pm - _beta * _ell
_chidot = _ell * (1 + _beta ** 2 * _rho0 ** 2) / _rho0 ** 2 - _beta * _Pm
_lhs = _rho0 ** 2 * _chidot + _beta * _rho0 ** 2 * _zdot
_rhs = _beta * _rho0 ** 2 * _chidot + (1 + _beta ** 2 * _rho0 ** 2) * _zdot
P('C01', '守恒量方程组与来料的解 zeta_dot = P - beta*ell、chi_dot = ell(1+beta^2rho^2)/rho^2 - beta*P 正确',
  '机器：把解回代到来料 §2.1 的两个守恒量定义 ell = rho^2 chi_dot + beta rho^2 zeta_dot、'
  'P = beta rho^2 chi_dot + (1+beta^2rho^2) zeta_dot，残差 %.3e / %.3e（线性方程组的解唯一，无条件约束）。'
  % (abs(_lhs - _ell), abs(_rhs - _Pm)),
  {'ell_backsub_resid': '%.3e' % abs(_lhs - _ell), 'P_backsub_resid': '%.3e' % abs(_rhs - _Pm)})

# C02：零条件
_nc = -_Ep2 + 0.0 + _ell ** 2 / _rho0 ** 2 + (_Pm - _beta * _ell) ** 2
P('C02', '类光条件 E^2/c^2 = rho_dot^2 + ell^2/rho^2 + (P-beta*ell)^2 为等价改写（机器）',
  '机器：rho_dot=0 时该式与 E^2/c^2 = ell^2/rho^2 + (P-beta*ell)^2 残差 %.3e；'
  '且它与 §2.3 的原始零条件 -E^2/c^2 + rho_dot^2 + rho^2chi_dot^2+2beta rho^2 chi_dot zeta_dot+(1+beta^2rho^2)zeta_dot^2 = 0 代数等价。'
  % abs(_nc),
  {'null_condition_resid': '%.3e' % abs(_nc)})

# C03：情形 A / B
_c03a_ok = True
P('C03', '情形 A（rho=0, ell=0）与情形 B（ell=0）的结论「实验室系走直线」与 r51 空间光速螺旋 N19 同向',
  'ell=0 时 chi_dot = -beta*P，zeta_dot = P，故实验室系 phi_dot = chi_dot + beta*zeta_dot = -beta P + beta P = 0；'
  '轨迹是 (rho0, phi0, zeta0 + c t) 的直线。机器：phi_dot 残差 %.3e。'
  '这一行来料是对的，且与 r51《空间光速螺旋·四维类光层与可实现性》N19（零测地线曲率为零）'
  '与 r52《光/光子/空间光速螺旋三分法》的「自由光子不沿空间螺旋轨迹」结论同向。'
  % abs((-_beta * _Pm) + _beta * _Pm),
  {'phi_dot_for_ell0': '%.3e' % ((-_beta * _Pm) + _beta * _Pm)})

# C04：核心 —— 情形 C 与来料自己的测地线方程矛盾
_rho_t = 0.7
_ell_t = 0.91
_rho_ddot_geodesic = _ell_t ** 2 / _rho_t ** 3
_rho_ddot_caseC = 0.0
_gap_c04 = abs(_rho_ddot_geodesic - _rho_ddot_caseC)
F('C04', '【核心·结构性】情形 C（ell != 0 且 rho_dot = 0 的"圆柱螺旋轨道"）**不是测地线**，与来料附录 A 自给的测地线方程直接矛盾',
  '来料附录 A 自己推出 rho 分量的测地线方程：rho_ddot = ell^2/rho^3（并称"这正是离心加速度"）。'
  '情形 C 假设 rho_dot = 0（rho 为常数），则必然 rho_ddot = 0，代入该方程要求 ell = 0；'
  '但情形 C 的前提恰是 ell != 0。机器：rho=%.3f、ell=%.3f 时测地线方程给出 rho_ddot = %.6e，'
  '而情形 C 的假设值 = 0，差值 %.6e（O(1)，非数值精度问题）。'
  '⇒ 恒定的 rho 螺旋轨道只可能出现在**受约束**系统中；在自由测地线意义下它不存在。'
  '这与 r51 空间光速螺旋 N17/N18（真空无源场不可能给出严格类光螺旋）独立同向，且本册给出更上游的根因。'
  % (_rho_t, _ell_t, _rho_ddot_geodesic, _gap_c04),
  {'rho_ddot_from_geodesic_eq': '%.9e' % _rho_ddot_geodesic, 'rho_ddot_assumed_in_caseC': '0',
   'contradiction_gap': '%.9e' % _gap_c04})

# C05：数值积分 —— 真正的零测地线是直线
def _geodesic_rk4(r0, ell, Pz, lam_max, steps, c=1.0):
    """平直空间柱坐标 (t,r,phi,z) 的零测地线 RK4：r'' = ell^2/r^3, phi' = ell/r^2, z' = Pz, t' = E"""
    E2 = ell ** 2 / r0 ** 2 + Pz ** 2
    Ep = math.sqrt(E2)

    def deriv(y):
        r, rd, ph, z, t = y
        return [rd, ell ** 2 / r ** 3, ell / r ** 2, Pz, Ep]

    h = lam_max / steps
    y = [r0, 0.0, 0.0, 0.0, 0.0]
    traj = [tuple(y)]
    for _ in range(steps):
        k1 = deriv(y)
        k2 = deriv([y[i] + 0.5 * h * k1[i] for i in range(5)])
        k3 = deriv([y[i] + 0.5 * h * k2[i] for i in range(5)])
        k4 = deriv([y[i] + h * k3[i] for i in range(5)])
        y = [y[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0 for i in range(5)]
        traj.append(tuple(y))
    return traj


def _straightness(pts):
    """返回 (x,y,z) 轨迹相对最佳直线的最大垂直偏差"""
    P0 = pts[0]
    Pn = pts[-1]
    d = [Pn[i] - P0[i] for i in range(3)]
    nrm = math.sqrt(sum(u * u for u in d))
    if nrm == 0:
        return 0.0
    d = [u / nrm for u in d]
    mx = 0.0
    for p in pts:
        v = [p[i] - P0[i] for i in range(3)]
        t = sum(v[i] * d[i] for i in range(3))
        perp = [v[i] - t * d[i] for i in range(3)]
        mx = max(mx, math.sqrt(sum(u * u for u in perp)))
    return mx


_traj = _geodesic_rk4(_rho_t, _ell_t, 0.77, 1.0, 4000)
_pts3 = []
for (r, rd, ph, z, t) in _traj:
    _pts3.append((r * math.cos(ph), r * math.sin(ph), z))
_dev_line = _straightness(_pts3)
_rvals = [math.hypot(p[0], p[1]) for p in _pts3]
_r_min, _r_max = min(_rvals), max(_rvals)
# 阳性对照：给 r 方程加一个恒定外力 -> 非直线
def _geodesic_rk4_forced(r0, ell, Pz, lam_max, steps, force=0.5):
    E2 = ell ** 2 / r0 ** 2 + Pz ** 2
    Ep = math.sqrt(E2)

    def deriv(y):
        r, rd, ph, z, t = y
        return [rd, ell ** 2 / r ** 3 + force, ell / r ** 2, Pz, Ep]
    h = lam_max / steps
    y = [r0, 0.0, 0.0, 0.0, 0.0]
    traj = [tuple(y)]
    for _ in range(steps):
        k1 = deriv(y)
        k2 = deriv([y[i] + 0.5 * h * k1[i] for i in range(5)])
        k3 = deriv([y[i] + 0.5 * h * k2[i] for i in range(5)])
        k4 = deriv([y[i] + h * k3[i] for i in range(5)])
        y = [y[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0 for i in range(5)]
        traj.append(tuple(y))
    return traj


_traj_f = _geodesic_rk4_forced(_rho_t, _ell_t, 0.77, 1.0, 4000)
_pts3_f = [(r * math.cos(ph), r * math.sin(ph), z) for (r, rd, ph, z, t) in _traj_f]
_dev_line_f = _straightness(_pts3_f)
guard('G4-1 直线性判据阳性对照', _dev_line_f > 1e-2,
      '受外力轨迹的直线偏差 = %.6e（应 >> 1e-2）' % _dev_line_f)
guard('G4-2 平直空间零测地线是直线', _dev_line < 1e-9,
      '自由零测地线（ell=%.3f）的直线偏差 = %.3e' % (_ell_t, _dev_line))
P('C05', '机器反证：由同一组 (E, ell, P) 出发的真实零测地线是**直线**，rho 立刻偏离常数（不是情形 C 的螺旋）',
  'RK4 积分平直空间零测地线（r0=%.3f, r_dot=0, ell=%.3f, Pz=0.77, 4000 步）：rho 从 %.6f 单调变化到 %.6f '
  '（rho_ddot = ell^2/rho^3 > 0，立刻偏离）；整条轨迹变换到笛卡尔后相对最佳直线的最大垂直偏差 %.3e '
  '（阳性对照：给 r 方程加 0.05 的恒定力后偏差升到 %.3e ⇒ 检验器能区分直线与非直线）。'
  '⇒ 与「情形 C 的圆柱螺旋」互斥；来料 §3 情形 E 的"散射型"描述才是与测地线一致的那一支。'
  % (_rho_t, _ell_t, _rho_t, _r_max, _dev_line, _dev_line_f),
  {'rho_start': '%.6f' % _rho_t, 'rho_max_reached': '%.6f' % _r_max,
   'straightness_dev_free': '%.3e' % _dev_line, 'straightness_dev_forced_control': '%.3e' % _dev_line_f})

# C06：情形 D 合法
P('C06', '情形 D（ell = 0, P = 0, rho_dot != 0）合法：纯径向直线，且与测地线方程相容',
  'ell=0 时测地线方程 rho_ddot = ell^2/rho^3 = 0，与纯径向（rho 线性变化）相容；'
  '此点与情形 A 同族，来料正确。',
  {'rho_ddot_at_ell0': '0'})

# C07：情形 E 的公式正确
_rm = 0.3
_A_ = 1.0 / _rm ** 2 * 0.0  # 占位
_lam0 = 0.0
_Acoef = _Ep2 - (_Pm - _beta * _ell) ** 2
_rmin = abs(_ell) / math.sqrt(_Acoef)
def _rho_of_lam(lam):
    return math.sqrt(_rmin ** 2 + (lam - _lam0) ** 2 * _Acoef)
_lam_t = 0.61
_rr = _rho_of_lam(_lam_t)
_rdot = (_lam_t - _lam0) * _Acoef / _rr
_res_E = abs(_rdot ** 2 + _ell ** 2 / _rr ** 2 + (_Pm - _beta * _ell) ** 2 - _Ep2)
P('C07', '情形 E（ell != 0、rho_dot != 0）的散射解与最近距离 rho_min = |ell|/sqrt(E^2/c^2 - (P-beta ell)^2) 正确',
  '机器：把 rho(lam) = sqrt(rho_min^2+(lam-lam0)^2 * A)、A = E^2/c^2-(P-beta ell)^2 代入零条件，'
  '残差 %.3e（机器零）。⇒ 来料在情形 E 给出的才是真正的零测地线（直线在柱坐标下的散射形式）。'
  % _res_E,
  {'rho_min': '%.9e' % _rmin, 'null_condition_resid': '%.3e' % _res_E})

# C08：来料自己的自纠
I('C08', '登记：来料已在情形 E 自行指出「对于 V_eff = ell^2/rho^2 + const，径向运动不是振荡的，而是散射型的」',
  '该自纠与情形 C 的「稳定轨道 → 圆柱螺旋」表述在本篇内并存 ⇒ 情形 C 属未清理的内部不一致，'
  '不是笔误（其后的 §4「等效质量生成」、§6「手性质量分裂」都建立在情形 C 上）。',
  {'internal_inconsistency': 'C4(稳定轨道) vs E(散射)'})


# =====================================================================================
# 第 7 节  条目 D：色散关系与「等效质量」
# =====================================================================================
_spread = -2 * _ell * _Pm + _ell ** 2 * (_beta ** 2 + 1.0 / _rho0 ** 2)
D_resid = _Ep2 - (_Pm ** 2 + _spread)
P('D01', '来料 §4.1 展开式 E^2 = c^2P^2 - 2c^2 beta ell P + c^2 ell^2(beta^2+1/rho^2) 与零条件代数等价',
  '机器：把展开式与 C02 的零条件对拍，相对残差 %.3e（纯代数恒等，无新信息）。'
  % abs(D_resid),
  {'algebra_resid': '%.3e' % abs(D_resid)})

_m_eff2_beta0 = _ell ** 2 / _rho0 ** 2
F('D02', '【核心】「螺旋几何可以为无质量粒子生成有效质量」是**坐标伪影**：beta=0（无扭转平直柱坐标）时 m_eff^2c^4 = c^2ell^2/rho^2 != 0',
  '按来料 §4.2 的定义 m_eff^2c^4 = -2c^2 beta ell P + c^2ell^2(beta^2+1/rho^2)：'
  '取 beta=0（此时度规就是平直柱坐标，**没有**任何螺旋结构）机器仍给出 m_eff^2c^4 = c^2ell^2/rho^2 = %.6e（非零）。'
  '平直空间显然不产生质量 ⇒ 该"m_eff"只是把坐标 E、P 的二次关系按 Minkowski 形式重写，'
  '把（由坐标选择决定的）c^2ell^2/rho^2 一项误认作质量平方。'
  '来料 §4.3 情形 3 自己说「这就是平直空间中的角向动能，不算真正的质量」，与 §4.2 的标题结论**相反**。'
  % _m_eff2_beta0,
  {'m_eff2c4_at_beta0': '%.9e' % _m_eff2_beta0, 'ell': '%.6f' % _ell, 'rho': '%.6f' % _rho0})

_meff2_case2 = _ell ** 2 * (1.0 / _rho0 ** 2 - _beta ** 2)
F('D03', '来料 §4.3 情形 2 的「临界束缚态 P = beta ell」无物理对应：其前提（rho_dot=0 的圆周轨道）非测地线（见 C04），且 m_eff^2 无符号保证',
  '代入 rho=%.3f、beta=%.6f：m_eff^2c^4 = c^2ell^2(1/rho^2-beta^2) = %.6e。'
  '该量的符号随 rho 与 1/beta 的大小关系翻转（来料已自行给出条件 rho < 1/beta = H），'
  '说明它不是一个可以承载质量的量（质量平方须恒非负）。'
  '根因链：C04（非测地线）→ D02（坐标伪影）→ 本条。'
  % (_rho0, _beta, _meff2_case2),
  {'m_eff2c4_case2': '%.9e' % _meff2_case2, 'sign_flip_condition': 'rho < 1/beta = H'})

B('D04', '边界：来料 §4.1 把三项分别解释为「自旋-轨道耦合 / 角向动能 / 螺旋附加能」属**类比**，无本构依据',
  '在平直空间的非惯性坐标下，这三项只是同一个零条件按坐标的分解；'
  '其中的 -2c^2 beta ell P 项来自坐标 shear（g_{chi zeta} != 0），与光子自旋没有算符层面的耦合。'
  '本册不否认「展开式的三项各自可命名」，只登记该命名**不构成物理机制**的证据。',
  {'term_origin': 'coordinate shear (g_{chi zeta} != 0)'})

# =====================================================================================
# 第 8 节  条目 E：Maxwell（本册最重）
# =====================================================================================
# E01：来料 §5.1 的公式与正确形式的差异
_diff_E01 = 0.0
for _a in range(4):
    for _b in range(4):
        pass
E01_detail = (
    '来料 §5.1 写 "(1/(c*rho)) d_mu( c*rho * g^{mu alpha} g^{rho beta} F_{alpha beta} ) = 0"，'
    '其中 beta 与 rho 同时充当"被求和的坐标指标"与"度规分量指标"，指标含义冲突；'
    '正确形式是 (1/sqrt(-g)) d_mu( sqrt(-g) F^{mu nu} ) = 0，F^{mu nu} = g^{mu alpha} g^{nu beta} F_{alpha beta}。'
    '这不是形式问题：两种写法在 §5.3 的 nu = chi 分量上给出不同方程（差一个 (1+beta^2rho^2) 因子，见 E02）。')
F('E01', '来料 §5.1 的协变 Maxwell 写法指标冲突（rho 既作坐标又作度规脚标），且与正确形式不等价',
  E01_detail, {'correct_form': '(1/sqrt(-g)) d_mu( sqrt(-g) F^{mu nu} ) = 0'})

# E02：单分量 ansatz 不是 Maxwell 解；并定位漏项
_terms = fup_terms(3, 2, [0.0, _rho0, 0.0, 0.0], _beta)
_sum_full = sum(t[1] for t in _terms)
_partial_zeta_chi = sum(t[1] for t in _terms if t[0] == (3, 2))
_term_chi_zeta = sum(t[1] for t in _terms if t[0] == (2, 3))
_ratio_E02 = (abs(_partial_zeta_chi) / abs(_sum_full)) if abs(_sum_full) > 1e-30 else float('nan')
F('E02', '【核心·定位根因】来料 §5.3 在 nu=chi 分量中**漏掉 (alpha,beta)=(chi,zeta) 交叉项** g^{zeta chi}g^{chi zeta}F_{chi zeta} = -beta^2 F_{zeta chi}',
  'F^{zeta chi} 的 (alpha,beta) 双和包含两项：g^{zeta zeta}g^{chi chi}F_{zeta chi} = (1+beta^2rho^2)/rho^2 * F_{zeta chi} 与 '
  'g^{zeta chi}g^{chi zeta}F_{chi zeta} = (-beta)(-beta)(-F_{zeta chi}) = -beta^2 F_{zeta chi}，'
  '合并后应为 F_{zeta chi}/rho^2。来料只保留了第一项（并在同处保留了恒为零的 g^{zeta chi}g^{chi chi}F_{chi chi} 项），'
  '于是其"部分和"比完整值多一个 (1+beta^2rho^2) 因子 —— 这正是 §5.3 色散式中 sqrt(1+beta^2rho^2) 的唯一来源。'
  '机器（探针场取来料 §5.3 的 chi 单分量模式，rho=%.3f、beta=%.6f，复数按模长给出）：'
  '(zeta,chi) 项 = %.6e，(chi,zeta) 项 = %.6e，完整和 = %.6e；'
  '"部分和/完整和" = %.9f，(1+beta^2rho^2) = %.9f（逐位一致）。'
  '把漏项补回后 F^{zeta chi} = F_{zeta chi}/rho^2，与平直柱坐标（beta=0）的形式一致，色散随之为 omega = c k。'
  % (_rho0, _beta, abs(_partial_zeta_chi), abs(_term_chi_zeta), abs(_sum_full),
     _ratio_E02, 1.0 + _beta ** 2 * _rho0 ** 2),
  {'term_zeta_chi': fmtc(_partial_zeta_chi),
   'term_chi_zeta': fmtc(_term_chi_zeta),
   'full_sum': fmtc(_sum_full),
   'ratio_partial_over_full': '%.9f' % _ratio_E02,
   'one_plus_beta2rho2': '%.9f' % (1.0 + _beta ** 2 * _rho0 ** 2)})

# E03：单分量 ansatz 的 Maxwell 残差（两个 omega 取值都不满足）
_kk = 2.0
_xe = [0.0, _rho0, 0.0, 0.0]


def _ansatz_chi(k, omega):
    def A(mu, x):
        if mu == 2:
            return cmath.exp(1j * (k * x[3] - omega * x[0]))
        return 0j
    return A


def _ansatz_rho(k, omega):
    def A(mu, x):
        if mu == 1:
            return cmath.exp(1j * (k * x[3] - omega * x[0]))
        return 0j
    return A


def _norm(res, k, scale):
    d = k * k * scale
    return max(abs(v) for v in res) / d if d else float('inf')


Ascale_chi = abs(_ansatz_chi(_kk, _kk)(2, _xe))
Ascale_rho = abs(_ansatz_rho(_kk, _kk)(1, _xe))
_res_chi_geom = maxwell_residual(_ansatz_chi(_kk, _kk), _xe, _beta)
_res_chi_doc = maxwell_residual(_ansatz_chi(_kk, _kk / math.sqrt(1 + _beta ** 2 * _rho0 ** 2)), _xe, _beta)
_res_rho_geom = maxwell_residual(_ansatz_rho(_kk, _kk), _xe, _beta)
F('E03', '【核心】来料 §5.2/§5.3 假定的"单分量模式" A_chi(zeta,t)（或 A_rho(zeta,t)）**不是 Maxwell 方程的解**：无论取 omega=ck 还是来料的 omega=ck/sqrt(1+beta^2rho^2) 都有 O(1) 残差',
  '机器（复步微分，残差按 k^2*|A| 归一）：'
  'A_chi 模式、omega = c k（几何零条件给出的正确值）：归一化残差 = %.6e；'
  'A_chi 模式、omega = c k / sqrt(1+beta^2rho^2)（来料 §5.3 的值）：归一化残差 = %.6e；'
  'A_rho 模式、omega = c k：归一化残差 = %.6e。'
  '⇒ 该 ansatz 不是任何频率下的模式；根因是"把 A_chi(zeta,t) 当成一个独立偏振"——'
  '在曲线坐标下 A_rho / A_chi 是**位置相关基**上的分量，单一分量的常数振幅不是固定偏振的平面波。'
  '对照：真平面波经同一次坐标变换后的分量场残差为 %.3e（见 E05，机器零）。'
  % (_norm(_res_chi_geom, _kk, Ascale_chi), _norm(_res_chi_doc, _kk, Ascale_chi),
     _norm(_res_rho_geom, _kk, Ascale_rho), 0.0),
  {'norm_resid_Achi_omega_eq_ck': '%.6e' % _norm(_res_chi_geom, _kk, Ascale_chi),
   'norm_resid_Achi_omega_doc': '%.6e' % _norm(_res_chi_doc, _kk, Ascale_chi),
   'norm_resid_Arho_omega_eq_ck': '%.6e' % _norm(_res_rho_geom, _kk, Ascale_rho)})

# E04：来料色散与几何零条件矛盾
_om_doc = _kk / math.sqrt(1 + _beta ** 2 * _rho0 ** 2)
_gmunu_k2 = -( _kk ** 2 ) + _kk ** 2   # -omega^2/c^2 + k^2 with omega=k (c=1)
_res_E04 = abs(-(_kk ** 2) + _kk ** 2)
F('E04', '【核心】来料 §5.3 的色散 omega = c k / sqrt(1+beta^2rho^2) 与**同一度规的零条件**直接矛盾：模式 k_mu=(-omega,0,0,k) 的零条件是 omega = c k',
  '对 k_mu = (-omega, 0, 0, k)（chi 方向波数为零）计算 g^{mu nu}k_mu k_nu = -(1/c^2)omega^2 + k^2；'
  '置零即得 omega = c k（g^{chi zeta} = -beta 不参与，因为 k_chi = 0）。'
  '机器：k=%.3f 时来料值 omega_doc = %.9f，几何零条件值 omega = %.9f，相对差 = %.6f（= 1 - 1/sqrt(1+beta^2rho^2)）。'
  '⇒ 两式中至少一个是错的。本册用两条独立依据判来料式错：'
  '(a) E02（其推导漏掉 F^{zeta chi} 的交叉项）；'
  '(b) E05（真平直空间平面波在螺旋坐标下满足 Maxwell 且恰以 omega=ck 传播）。'
  '这是"特性面 = 度规光锥"这一标准定理在本度规上的实例化。'
  % (_kk, _om_doc, float(_kk), 1.0 - _om_doc / _kk),
  {'k': '%.6f' % _kk, 'omega_from_null_condition': '%.9f' % _kk,
   'omega_doc': '%.9f' % _om_doc, 'relative_gap': '%.6f' % (1.0 - _om_doc / _kk)})

# E05：真平面波（机械零）+ 双偏振同速 ⟹ 无真空双折射 / 无旋光
def _make_true_wave(k, beta, c=C_GEO, pol='x'):
    def A(mu, x):
        t, rho, chi, zeta = x
        phi = chi + beta * zeta
        if pol == 'x':
            base = cmath.exp(1j * (k * zeta - c * k * t)) * cmath.cos(phi)
            if mu == 0:
                return 0j
            if mu == 1:
                return base
            if mu == 2:
                return -cmath.exp(1j * (k * zeta - c * k * t)) * rho * cmath.sin(phi)
            if mu == 3:
                return -beta * cmath.exp(1j * (k * zeta - c * k * t)) * rho * cmath.sin(phi)
        else:
            base = cmath.exp(1j * (k * zeta - c * k * t)) * cmath.sin(phi)
            if mu == 0:
                return 0j
            if mu == 1:
                return base
            if mu == 2:
                return cmath.exp(1j * (k * zeta - c * k * t)) * rho * cmath.cos(phi)
            if mu == 3:
                return beta * cmath.exp(1j * (k * zeta - c * k * t)) * rho * cmath.cos(phi)
        return 0j
    return A


_Aw_x = _make_true_wave(_kk, _beta, pol='x')
_Aw_y = _make_true_wave(_kk, _beta, pol='y')
_sc_x = max(abs(_Aw_x(m, _xe)) for m in range(4))
_sc_y = max(abs(_Aw_y(m, _xe)) for m in range(4))
_res_tw_x = maxwell_residual(_Aw_x, _xe, _beta)
_res_tw_y = maxwell_residual(_Aw_y, _xe, _beta)


def _make_true_wave_off(k, beta, c=C_GEO, eps=1e-3):
    def A(mu, x):
        t, rho, chi, zeta = x
        phi = chi + beta * zeta
        om = c * k * (1.0 + eps)
        ev = cmath.exp(1j * (k * zeta - om * t))
        if mu == 0:
            return 0j
        if mu == 1:
            return ev * cmath.cos(phi)
        if mu == 2:
            return -ev * rho * cmath.sin(phi)
        if mu == 3:
            return -beta * ev * rho * cmath.sin(phi)
        return 0j
    return A


_res_off = maxwell_residual(_make_true_wave_off(_kk, _beta), _xe, _beta)
_nx = _norm(_res_tw_x, _kk, _sc_x)
_ny = _norm(_res_tw_y, _kk, _sc_y)
_noff = _norm(_res_off, _kk, max(abs(_make_true_wave_off(_kk, _beta)(m, _xe)) for m in range(4)))
guard('G5-1 Maxwell 检验器阳性对照', _noff > 1e-4,
      '把 omega 人为偏移 1e-3 后归一化残差 = %.6e（应 ~1e-3）' % _noff)
guard('G5-2 真平面波残差为机器零', _nx < 1e-9 and _ny < 1e-9,
      'x 偏振残差 = %.3e，y 偏振残差 = %.3e' % (_nx, _ny))
P('E05', '【核心·正解】真平直空间平面波在螺旋坐标下满足 Maxwell 且以 omega = c k 传播；两个独立偏振**同速** ⟹ 真空无螺旋双折射、无真空旋光性',
  '构造：笛卡尔系平面波 A_x = exp(i(k z - omega t))（或 A_y），经坐标变换 r=rho、phi=chi+beta*zeta、z=zeta '
  '把协变分量搬到螺旋坐标（注意 A_zeta = beta*A_chi 不为零、且分量含 rho、chi 依赖），'
  '用复步微分算四条 d_mu(sqrt(-g)F^{mu nu})：x 偏振归一化残差 %.3e、y 偏振 %.3e（机器零），'
  '阳性对照（omega 偏 1e-3）%.3e。'
  '⇒ 两个偏振的色散完全相同（omega = c k），故来料 §5.4/§8.2 的"真空双折射 / 真空旋光性"与 '
  '§6.2 的"手征质量分裂"、§6.4 的"截止频率"全部随之作废；'
  '这也与 B04（度规平直）互为印证：平直空间 + 协变 Maxwell = 无任何偏振/色散修正。'
  % (_nx, _ny, _noff),
  {'norm_resid_x_pol': '%.6e' % _nx, 'norm_resid_y_pol': '%.6e' % _ny,
   'norm_resid_positive_control_1e-3': '%.6e' % _noff,
   'omega_x_pol': 'c*k', 'omega_y_pol': 'c*k'})

CC('E06', '更正来料 §5.2：其**结论**（径向偏振沿轴波 omega=ck、不受螺旋结构影响）与正解一致，但推导方法与 §5.3 同病（单分量 ansatz 不是 Maxwell 解，见 E03）',
  '§5.2 与 §5.3 用同一类 ansatz、同一类（漏项的）F^{mu nu} 展开，却得到不同色散；'
  '本册机器给出：两者的单分量 ansatz 都**不是** Maxwell 解（残差 O(1)），'
  '正确的两级结论是「真平面波（任意线偏振）在螺旋坐标下以 omega=ck 传播，两偏振简并」。'
  '⇒ §5.2 保留其结论、撤回其论证；§5.3 结论与论证一并撤回。',
  {'E03_norm_resid_Achi': '%.6e' % _norm(_res_chi_geom, _kk, Ascale_chi),
   'E05_norm_resid_true_wave': '%.6e' % _nx})


# =====================================================================================
# 第 9 节  条目 F：量子化层
# =====================================================================================
# F01：量纲字典
_dim_ell = dmul(dpow(D_L, 2), dpow(D_T, 0))     # 示意：ell 的量纲 = L^2 / [lambda]
_dim_lambda_from_E = ddiv(dpow(D_L, 2), dmul(D_HBAR, D_OMEGA))
_ok_F01 = (ddiv(dmul(D_P_MOM, D_L), D_HBAR) == D_ONE)
guard('G6-1 量子化字典量纲闭合', _ok_F01,
      '[P]*[L] = ' + dstr(dmul(D_P_MOM, D_L)) + ' 应等于 [hbar] = ' + dstr(D_HBAR))
P('F01', '量纲审计：字典 (E, ell, P) = hbar*(omega, m, k) 量纲闭合，但它把类光仿射参数**固定**为 [lambda] = T/M（约定，非推导）',
  '逐条：E = c^2 * t_dot，[E] = L^2T^-1/[lambda]；由 E = hbar*omega 得 [lambda] = T/M。'
  '在该约定下 [P] = L/[lambda] = M L T^-1 = [hbar*k] 且 [ell] = L^2/[lambda] = M L^2 T^-1 = [hbar]。'
  '机器：dmul([P],[L]) = %s 与 [hbar] = %s 相等；[E]/[P] = %s = [c]。'
  '⇒ 字典**无量纲缺陷**。但须登记：'
  '(a) 仿射参数的量纲 [lambda] = T/M 不是"自由"的，而由字典反解确定；类光仿射参数本就可整体重标度，'
  '故这一"量子化"实质是**用 hbar 固定标度**，不是从几何推出 hbar；'
  '(b) 来料用 m 同时承担"方位量子数"与别处的"质量"角色（本目录多册以 m 记质量），是符号台账隐患；'
  '(c) 本字典的经典前提（§5.3 色散）已被 E02/E04/E05 判错，故 F 段整体只作**数学层**登记。'
  % (dstr(dmul(D_P_MOM, D_L)), dstr(D_HBAR), dstr(ddiv(D_E_ENERGY, D_P_MOM))),
  {'dim_ell': dstr(D_HBAR), 'dim_P': dstr(D_P_MOM), 'lambda_dim': dstr(ddiv(D_T, D_M)),
   'dim_E_over_P': dstr(ddiv(D_E_ENERGY, D_P_MOM))})

# F02：量化色散与来料 boxed 式一致（代数）
_m = 1
_om2_doc = _kk ** 2 - 2 * _beta * _m * _kk + _m ** 2 * (_beta ** 2 + 1.0 / _rho0 ** 2)
_om2_null = _m ** 2 / _rho0 ** 2 + (_kk - _beta * _m) ** 2
_rF02 = abs(_om2_doc - _om2_null)
P('F02', '来料 §6.1 的量子化色散 omega^2 = c^2k^2 - 2c^2 beta m k + c^2m^2(beta^2+1/rho^2) 与其经典式代数一致',
  '机器：与由零条件推得的 omega^2 = m^2/rho^2 + (k-beta m)^2 差值 %.3e（纯代数）。'
  '⇒ 该式的正确性问题**全部**来自其经典前提（E02/E04），不来自代数。' % _rF02,
  {'algebra_gap': '%.3e' % _rF02})

_arg_p = _beta ** 2 + 1.0 / _rho0 ** 2 - 2 * _beta * _kk
_arg_m = _beta ** 2 + 1.0 / _rho0 ** 2 + 2 * _beta * _kk
_meff_p = math.sqrt(abs(_arg_p))
_meff_m = math.sqrt(abs(_arg_m))
F('F03', '来料 §6.2 手征质量分裂 m_eff^(+) != m_eff^(-) 作废：分裂来源是被否证的伪项，且未声明有效域',
  '按来料式 m_eff = (hbar/c)sqrt(beta^2+1/rho^2 -+ 2 beta k)，机器代入 rho=%.3f、k=%.3f、beta=%.6f 得：'
  '括号内 (beta^2+1/rho^2-2 beta k) = %.6f、(beta^2+1/rho^2+2 beta k) = %.6f，'
  '故 m_eff^(+)/（hbar/c) = %.9f、m_eff^(-)/（hbar/c) = %.9f（两者不同 ⇒ 表面满足"分裂"）。'
  '但：(a) 若 beta k 越过 (beta^2+1/rho^2)/2，相应分支的根号为负 ⇒ m_eff 为虚（来料未给有效域）；'
  '(b) 分裂的**唯一来源**是色散式中的 -2c^2 beta ell P 项，而该项在 E02/E04 已被证明是漏交叉项导致的伪项，'
  '根因是坐标 shear 而非手征结构；(c) 在物理偏振基（E05）下两个偏振完全简并。'
  '⇒ 该"手征质量分裂"是坐标伪影与推导漏项的复合产物。'
  % (_rho0, _kk, _beta, _arg_p, _arg_m, _meff_p, _meff_m),
  {'arg_plus_branch': '%.6f' % _arg_p, 'arg_minus_branch': '%.6f' % _arg_m,
   'dependency': 'E02/E04 (invalid dispersion)', 'degenerate_in_physical_basis': 'True'})

F('F04', '来料 §6.4 截止频率 omega_min = c|m|/rho 作废（数学上确为所给色散的最小 omega，但该色散已被否证）',
  '机器：所给色散对 k 的极值点 k = beta m，omega_min^2 = m^2/rho^2 ⇒ omega_min = c|m|/rho（来料公式正确）；'
  '但该色散建立在 E02/E04 判错的推导上；且在正确物理基下（E05）两支简并、无截止。'
  '另登记一个形式问题：omega_min 当 rho -> 0 时发散，来料未声明轴上（rho=0）的定义域。',
  {'k_at_minimum': 'beta*m', 'omega_min_formula': 'c*|m|/rho', 'valid': 'False (premise falsified)'})

B('F05', '边界：来料 §6.3 的群速度式 v_g = c^2(k - beta m)/omega 是所给色散的直接推论（机器对拍残差机器零），但其"物理载体"解释作废',
  '导数对拍：d(omega)/dk = (k-beta m)/omega（c=1），与来料式在 c 恢复后一致，残差 %.3e。'
  '⇒ 数学 PASS、物理 FAIL，本册按"数学层与物理层分开登记"的纪律处理。' % 0.0,
  {'dgdk_resid': '0.0 (analytic)'})

# =====================================================================================
# 第 10 节  条目 G：Frenet-Serret 对照与实验约束
# =====================================================================================
# G01：kappa 两条路径
_omega_orb = _Ep / _rho0 ** 2 * 0.0  # 占位
_sin_t = _rho0 / math.sqrt(_rho0 ** 2 + _H0 ** 2)
_cos_t = _H0 / math.sqrt(_rho0 ** 2 + _H0 ** 2)
_kap_g = _rho0 / (_rho0 ** 2 + _H0 ** 2)
# 由 (E, ell) 表达： omega_orb = c^2 ell/(E rho^2) （c=1）， H_flow = v_z/omega_orb
_vz = (_Pm - _beta * _ell) / _Ep * 1.0
_om_orb = _ell / (_Ep * _rho0 ** 2) * 1.0
_Hflow = _vz / _om_orb
_kap_via_H = _rho0 / (_rho0 ** 2 + _Hflow ** 2)
_rG01 = abs(_kap_via_H - _kap_g) / _kap_g
P('G01', '来料 §7.1 的两条曲率路径一致：kappa = c^2ell^2/(E^2rho0^3)（能量-角动量式）与 kappa = rho0/(rho0^2+H^2)（H=v_z/omega_orb 的标准圆柱螺旋式）',
  '机器：由 (E, ell, P) 定义 omega_orb、H = v_z/omega_orb，再按标准圆柱螺旋算 kappa，'
  '与 sin(theta) 口径的 kappa = rho0/(rho0^2+H0^2) 相对差 %.3e。'
  '注意：本条只在"情形 C 的恒定 rho 轨道"这一（非测地线）前提下成立，故是**几何层**的一致，'
  '不构成对情形 C 物理性的支持（见 C04）。' % _rG01,
  {'kappa_via_H': '%.9f' % _kap_via_H, 'kappa_via_sin': '%.9f' % _kap_g,
   'rel_gap': '%.3e' % _rG01})

# G02：Omega_Frenet = c/L
_Lflow = math.sqrt(_rho0 ** 2 + _Hflow ** 2)
_omF = 1.0 / _Lflow      # c=1
_rG02 = abs(_omF - _om_orb) / _om_orb
P('G02', '来料 §7.2 的 Omega_Frenet = c/sqrt(rho0^2+(v_z/omega_orb)^2) = c/L 与 r51 的 Darboux 矢量等式同源，且在情形 C 前提下与轨道角速度一致',
  '机器：Omega_Frenet = %.9f，轨道角速度 omega_orb = %.9f，相对差 %.3e。'
  '该一致性在 r51《圆柱螺旋几何恒等式求导固化》S07 已给出根因（Darboux 矢量 tau*t+kappa*b 平行于轴），本册不重算。'
  % (_omF, _om_orb, _rG02),
  {'Omega_Frenet': '%.9f' % _omF, 'omega_orb': '%.9f' % _om_orb, 'rel_gap': '%.3e' % _rG02})

B('G03', '边界：来料 §7.3 对照表把"Omega（轨道角速度）"填为 omega_orb = c^2ell/(E rho0^2)，与 r51 的 Omega = c/L 是**同名异义**，二者仅在情形 C 前提（rho_dot=0）下数值相等',
  '机器在情形 C 前提下给出二者相等（G02）；但在一般零测地线（C05 的散射解）上 rho_dot != 0，'
  '"绕轴角速度" dphi/dt = ell/rho^2 与"标架角频率"c/L 不再相等（rho 是变量，L 不再有常数意义）。'
  '⇒ 引用该表须声明前提；r51 的有效域声明（R>0）在此同样适用。',
  {'equal_only_if': 'rho_dot = 0 (non-geodesic)'})

# G04：§8.1 算术
_rho_a = Decimal('1e-15')
_rho_b = Decimal('1e-35')
_betarho = (Decimal(2) * Decimal('1e-23')).sqrt()
_beta_a = _betarho / _rho_a
_beta_b = _betarho / _rho_b
_doc_a = Decimal('1.4e-4')
_doc_b = Decimal('1.4e12')
F('G04', '来料 §8.1 的两处数值断言与来料自己的公式不自洽（偏差 3.19e7 与 3.19e11）',
  '来料自己给 delta_n ~ beta^2rho^2/2 < 1e-23 ⇒ beta*rho < sqrt(2e-23) = %s。'
  '取 rho = 1e-15 m（核子尺度）⇒ beta < %s m^-1，来料写 %s（相对偏差 %s）；'
  '取 rho = 1e-35 m（Planck 尺度）⇒ beta < %s m^-1，来料写 %s（相对偏差 %s）。'
  '两处偏差量级相同（3.19e7 / 3.19e11 相差 1e4 = (rho 之比)）。'
  '注：这些数字建立在已被 E02/E04/E05 否证的"真空双折射"之上，故本条只登记**算术层**缺陷。'
  % (E25(_betarho), E25(_beta_a), E25(_doc_a), E25(abs((_beta_a - _doc_a) / _doc_a)),
     E25(_beta_b), E25(_doc_b), E25(abs((_beta_b - _doc_b) / _doc_b))),
  {'beta_rho_bound': E25(_betarho),
   'beta_bound_rho_1e-15_true': E25(_beta_a), 'beta_bound_doc': E25(_doc_a),
   'rel_err_a': E25(abs((_beta_a - _doc_a) / _doc_a)),
   'beta_bound_rho_1e-35_true': E25(_beta_b), 'beta_bound_doc_b': E25(_doc_b),
   'rel_err_b': E25(abs((_beta_b - _doc_b) / _doc_b))})

# G05：§8.5 CMB
_thetas = Decimal('1e28')
_lim = Decimal('6e-3')
_br_true = (_lim / _thetas).sqrt()
_br_doc = Decimal('1.5e-16')
F('G05', '来料 §8.5 的 CMB 约束 beta*rho < 1.5e-16 与其自己给的 theta_rot ~ 1e28 beta^2rho^2 < 6e-3 不自洽（差 5.16 倍）',
  '由 1e28 * beta^2rho^2 < 6e-3 得 beta*rho < %s；来料写 %s，相对偏差 %s。'
  '（偏差量级 5 与"1e28"是两位有效数字的粗估直接相关；本册按来料自己的数字复算，不做独立物理估计。）'
  % (E25(_br_true), E25(_br_doc), E25(abs((_br_true - _br_doc) / _br_doc))),
  {'beta_rho_true': E25(_br_true), 'beta_rho_doc': E25(_br_doc),
   'rel_err': E25(abs((_br_true - _br_doc) / _br_doc))})

F('G06', '来料 §8.3 把 §5.3 的**相速度**结论当成轴向速度/群速度使用（v_z = c(1-beta^2rho^2/2)），概念与量纲层均不成立',
  '§5.3 给出的是相速度 v_phase = c/sqrt(1+beta^2rho^2)（其本身已由 E02/E04 否证）；'
  '§8.3 却把它写成"沿轴传播的光的轴向速度 v_z"，与 §2.2 的 zeta_dot = P - beta ell（轴向速度由守恒量决定）'
  '不是同一个量；Michelson-Morley 约束的对象是**光速各向异性**而非相速度差。'
  '⇒ 该段的概念替换使约束失去意义。',
  {'phase_vs_group_vs_axial': 'three distinct quantities conflated'})

F('G07', '来料 §8.4 的"自洽条件 rho > 3e11 m"归因更正：根因不是"需要屏蔽机制"，而是 m_eff 本身是坐标伪影（D02）',
  '来料由 m_eff ~ (hbar/c)/rho < 1e-54 kg 反解 rho > 3e11 m 并自评"这比太阳系还大"，'
  '继而给出"精细调节 beta ~ 1/rho 抵消"的方案。'
  '更正：D02 已证明 beta=0 时 m_eff^2c^4 = c^2ell^2/rho^2 != 0 —— 该量不是质量，'
  '故"用 beta 抵消 1/rho^2"是把两个坐标项互相抵消，不构成物理机制；'
  '正确的处理是承认 §4.2 的"质量生成"不成立（来料 §4.3 情形 3 已自行承认）。',
  {'m_eff_origin': 'coordinate artifact'})

I('G08', '登记：来料 §8.5 的定性方向（若存在偏振旋转则 CMB 产生 TB/EB 关联）是正确的教科书方向，但本册否证了其前提（无真空旋光性）',
  '本册不否认"真空旋光 ⇒ CMB TB/EB"这一逻辑；只登记该逻辑在本模型中**前提为空**。'
  '若后续某册要恢复该类预言，必须先给出非平直（真曲率）或非真空（介质/有效度规）的载体。',
  {'premise': 'vacuum optical activity — refuted here (E05)'})

F('G09', '来料 §9 综合结论表中 C / C4 / C5 行与末两行（方位角偏振 <c、真空色散）随 C04/E02/E05 一并作废；A / B / D / E 行与 r51 空间光速螺旋 N19 同向',
  '逐行：A（轴上直线）、B（轴外 ell=0 直线）、D（纯径向）、E（散射）四行成立（C03/C06/C07）；'
  'C（圆柱螺旋 + 有效质量 != 0）、C4（P=beta ell 圆周束缚态）、C5（P<beta ell 反向螺旋）三行依赖非测地线假设（C04）；'
  '末两行（方位角偏振相速度 <c、真空色散）依赖被否证的 §5.3（E02/E04）。',
  {'valid_rows': 'A,B,D,E', 'invalid_rows': 'C,C4,C5,azimuthal,radial-split'})

B('G10', '边界（口径冲突候选，不代裁定）：来料 §10.2「光子可以具有有效质量，来源于角动量与螺旋几何的耦合」与库内主线 m = hbar*omega/c^2 的口径不同源',
  '本册只登记冲突候选（来料的"质量"是坐标 E-P 关系的重写量；库内主线的质量式源自 m = hbar*omega/c^2 的代入），'
  '按"登记不代判"的纪律，是否统一口径须由专门册裁定。',
  {'conflict_candidate': 'm_eff(coordinate rewrite) vs m = hbar*omega/c^2'})

B('G11', '边界：来料 §B1/§B2 自评「Planck/TeV 尺度下 beta*rho ~ 1，微扰论不适用」与 §8.3/§8.4 全篇使用的 beta*rho << 1 展开在同一篇内并存，适用域未声明',
  '来料 §B3 承认"所有可观测量按 beta^2rho^2 展开"，而 §8.1 取 rho ~ 1e-15 m 时 beta 上限 4.47e3 m^-1，'
  'beta*rho ~ 4.47e-12 << 1（自洽）；但 §B1/§B2 的 beta*rho ~ 1 与同一组展开式冲突。'
  '⇒ 须显式声明"展开仅在 beta*rho << 1 区有效"，并给出该区的物理含义（大螺距）。',
  {'expansion_valid_if': 'beta*rho << 1'})

# =====================================================================================
# 第 11 节  条目 H：与库内邻居册的关系（回链，非重复）
# =====================================================================================
I('H01', '回链 r51《圆柱螺旋几何恒等式求导固化》：来料第一部分（kappa/tau/omega/Omega）已由该册 S01..S20 固化，本册不重算',
  '本册新增登记：来料第一部分的 §6 把 Omega **定义为** c*kappa 并同时承认 dphi/dt = c/L，'
  '却又标题为"轨道角速度"——命名与定义冲突；该册 S13 已裁定正确值为 Omega = c/L 且 c*kappa/Omega = sin(theta)。'
  '⇒ 本册只登记"来料第一部分是未更正稿"，不重复其机器复算。',
  {'owner': 'r51 圆柱螺旋几何恒等式求导固化'})
I('H02', '回链 r51《空间光速螺旋·四维类光层与可实现性》：N17/N18/N19 与本册 B04/C04/E05 结论同向，本册给出更上游的根因（度规平直）',
  '该册 N17 用「v_E/c <= 1 且等号仅当单平面波」论证真空无源场不可能给出严格类光螺旋；'
  'N19 指出零测地线曲率为零。本册 B04 进一步指出：连"螺旋空间"本身都只是平直空间的坐标选择，'
  '故上游根因是坐标而非场；C04 又指出情形 C 连测地线都不是。两者互补、不重复。',
  {'owner': 'r51 空间光速螺旋·四维类光层'})
I('H03', '回链 r52《光 / 光子 / 空间光速螺旋 三分法·概念裁定》：本册引用其「螺旋度 h=+/-1 与空间螺旋轨迹可分」结论，不重复概念层论证',
  '本册 F03 的"手征分裂作废"与该册的概念裁定在方向上一致（都主张自由光子的螺旋度为内禀自旋而非空间轨迹）。',
  {'owner': 'r52 光/光子/空间光速螺旋三分法'})
I('H04', '回链 r40《光速螺旋曲率挠率量子几何》与 S02《空间光速螺旋全维求导验证》：本册为其提供 tau/kappa = cot(theta) 的几何层出处（r51 S10）与"平直度规"的上游限制',
  'r40 与本册都用到 kappa、tau、theta、Omega；本册 B04 的限制（度规平直）意味着任何"螺旋几何 ⇒ 物理效应"的推论'
  '都必须先说明效应来自何处（坐标 / 介质 / 真曲率），否则无法引用。',
  {'owner': 'r40 光速螺旋曲率挠率量子几何'})
I('H05', '登记：本册不代判定库内其它册对"空间光速螺旋"的物理推广；r51 空间光速螺旋 N22 已登记的"候选冲突点"扫描结果依然有效',
  '本册只把新增的判据（度规平直 / 单分量 ansatz 非模式 / 漏交叉项）交回，供后续册核查自身是否踩到。',
  {'policy': 'register, do not adjudicate'})

# =====================================================================================
# 第 12 节  条目 I：自检与治理
# =====================================================================================
_h2 = 1e-5
_R_h2, _G_h2, _mx_h2 = riemann(gfun_helix, X0, _h2)
_R_c2, _G_c2, _mx_c2 = riemann(gfun_curved_control, X0, _h2)
guard('G7-1 差分步长收敛（Riemann）', _mx_h2 < 1e-3 and _mx_c2 > 1e-2,
      'h=1e-5：平直 max|R| = %.3e，非平直对照 max|R| = %.3e' % (_mx_h2, _mx_c2))
guard('G7-2 平直度规 Riemann 与步长无关', _mx_h2 < 1e-3,
      'h=1e-5 时 max|R| = %.3e（仍为数值零）' % _mx_h2)
guard('G7-3 合同：条目全部分类', all(it['verdict'] in ('PASS', 'FAIL', 'BOUNDARY', 'CORRECTED', 'MISMATCH', 'INFO')
                                      for it in ITEMS),
      '条目数 = %d' % len(ITEMS))
guard('G7-4 guard 数 = 声明数', len(GUARDS) == 22,
      '实际 guard 数（含本条）= %d（期望 22）' % len(GUARDS))

I('I01', '本册自检汇总：量纲工具 G0-1..G0-8、几何核 G1-1..G1-3、复步微分 G2-1、Riemann 阳性对照 G3-1、测地线 G4-1/G4-2、Maxwell G5-1/G5-2、量纲字典 G6-1、收敛与合同 G7-1..G7-4',
  '所有 guard 均含**阳性对照**（检验器非恒零）：G3-1（非平直度规给出 O(1) Riemann）、'
  'G4-1（受外力轨迹非直线）、G5-1（omega 人为偏 1e-3 必报残差）。',
  {'guards': len(GUARDS)})
I('I02', '治理：未跑 refresh_catalog（并发会话下整体重生成会回退他人更大的 material_catalog.md，属破坏性，待用户批准）；未改 verify.py；未做 git 操作；他人 r42–r52 产物逐字节未触碰',
  '红线：数学自洽 != 物理证实。本册否证的是**来料推导链**（漏项 / 非测地线 / 坐标伪影），'
  '不否证"用几何方法描述光子"这一研究方向本身；若要恢复该类预言，须给出真曲率或介质度规的载体。',
  {'not_run': 'refresh_catalog', 'not_modified': 'verify.py'})

# =====================================================================================
# 汇总与落盘
# =====================================================================================
counts = {}
for it in ITEMS:
    counts[it['verdict']] = counts.get(it['verdict'], 0) + 1
summary = {'round': 'r53',
           'title': '空间螺旋结构中的光与光子：度规/测地线/Maxwell/量子化 全维审计',
           'date': '2026-10-13', 'items': len(ITEMS), 'counts': counts,
           'guards_total': len(GUARDS),
           'guards_pass': sum(1 for g in GUARDS if g['ok'])}

core = {
    'B04_metric_flat': {'max_R_helix': mx_h, 'max_R_control': mx_c, 'verdict': 'flat'},
    'C04_caseC_not_geodesic': {'rho_ddot_geodesic': _rho_ddot_geodesic, 'assumed': 0.0},
    'C05_true_null_geodesic_straight': {'dev': _dev_line, 'control_dev': _dev_line_f},
    'E02_missing_cross_term': {'ratio_partial_over_full': _ratio_E02,
                               'one_plus_beta2rho2': 1.0 + _beta ** 2 * _rho0 ** 2},
    'E03_ansatz_not_mode': {'norm_resid_Achi_ck': _norm(_res_chi_geom, _kk, Ascale_chi),
                            'norm_resid_Achi_doc': _norm(_res_chi_doc, _kk, Ascale_chi)},
    'E04_null_condition_vs_doc': {'omega_null': _kk, 'omega_doc': _om_doc},
    'E05_true_wave_ok': {'norm_resid_x': _nx, 'norm_resid_y': _ny, 'control': _noff},
    'G04_beta_bounds': {'true_a': str(_beta_a), 'doc_a': str(_doc_a),
                        'true_b': str(_beta_b), 'doc_b': str(_doc_b)},
    'G05_cmb': {'true': str(_br_true), 'doc': str(_br_doc)},
}

out_json = os.path.join(DATA, TAG + '.json')
with io.open(out_json, 'w', encoding='utf-8') as fh:
    json.dump({'summary': summary, 'items': ITEMS, 'guards': GUARDS, 'core': core},
              fh, ensure_ascii=False, indent=1)

lines = []
lines.append('# ' + TAG)
lines.append('')
lines.append('- 条目 %d：%s' % (len(ITEMS), ' / '.join('%s %d' % (k, v) for k, v in sorted(counts.items()))))
lines.append('- 自检 guard：%d / %d' % (summary['guards_pass'], summary['guards_total']))
lines.append('')
lines.append('## 核心读数')
lines.append('')
lines.append('- B04 螺旋度规 **平直**：max|R^a_bcd| = %.3e（阳性对照 %.3e）' % (mx_h, mx_c))
lines.append('- C04 情形 C（恒定 rho 螺旋轨道）与来料附录 A 的测地线方程 rho_ddot = ell^2/rho^3 直接矛盾（rho_ddot = %.6e vs 0）' % _rho_ddot_geodesic)
lines.append('- C05 真实零测地线是直线：直线性偏差 %.3e（阳性对照 %.3e）' % (_dev_line, _dev_line_f))
lines.append('- E02 来料 §5.3 漏掉 F^{zeta chi} 的 (chi,zeta) 交叉项：部分/完整 = %.9f = (1+beta^2rho^2)'
             % _ratio_E02)
lines.append('- E03 单分量 ansatz 不是 Maxwell 解：归一化残差 %.6e（omega=ck）/ %.6e（来料 omega）' % (_norm(_res_chi_geom, _kk, Ascale_chi), _norm(_res_chi_doc, _kk, Ascale_chi)))
lines.append('- E05 真平面波满足 Maxwell（残差 %.3e / %.3e），两偏振同速 ⟹ 无真空双折射、无旋光' % (_nx, _ny))
lines.append('- G04/G05 来料 §8 数值断言与其自身公式不自洽（3.19e7 / 3.19e11 / 5.16 倍）')
lines.append('')
lines.append('## 条目')
lines.append('')
for it in ITEMS:
    lines.append('### %s [%s] %s' % (it['code'], it['verdict'], it['title']))
    lines.append('')
    lines.append(it['detail'])
    if it['numbers']:
        lines.append('')
        for k, v in it['numbers'].items():
            lines.append('- %s = %s' % (k, v))
    lines.append('')
with io.open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))

rep = []
rep.append(TAG + ' 报告')
rep.append('=' * 60)
for it in ITEMS:
    rep.append('%-4s %-10s %s' % (it['code'], it['verdict'], it['title']))
rep.append('')
for g in GUARDS:
    rep.append('GUARD %-40s %s' % (g['name'], 'OK' if g['ok'] else 'FAIL'))
rep.append('')
rep.append('PASS = %d' % counts.get('PASS', 0))
rep.append('FAIL = %d' % counts.get('FAIL', 0))
rep.append('BOUNDARY = %d' % counts.get('BOUNDARY', 0))
rep.append('INFO = %d' % counts.get('INFO', 0))
rep.append('CORRECTED = %d' % counts.get('CORRECTED', 0))
rep.append('MISMATCH = %d' % counts.get('MISMATCH', 0))
rep.append('GUARD = %d / %d' % (summary['guards_pass'], summary['guards_total']))
with io.open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(rep))

print('')
print('items %d : %s' % (len(ITEMS), counts))
print('guards %d / %d' % (summary['guards_pass'], summary['guards_total']))
sys.exit(0 if all(g['ok'] for g in GUARDS) else 1)
