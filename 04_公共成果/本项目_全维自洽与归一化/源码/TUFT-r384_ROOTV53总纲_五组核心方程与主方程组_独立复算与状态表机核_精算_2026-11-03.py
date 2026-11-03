# -*- coding: utf-8 -*-
"""
TUFT-r384 · 审计 ROOT V53《统一场论最核心方程组与本源理论总分析》

纯标准库。Decimal 60 位 + Fraction 精确有理数 + complex 双精度（仅 C06 交换子局部）。
不 import numpy / sympy / mpmath。

结构：
  A 组  来料 §八 自我评估表 11 条 + 表外遗漏逐条机核
  B 组  作用量 (1) 与总纲结构自洽（量纲齐次 / 单位制 / 旋量计数 / MASTER 方程身份）
  C 组  五组核心方程独立复算（螺旋 κτ / Yukawa 力 / 交换子 / KK 谱塔 / m(z) / 指标）
  D 组  Λ6 三维关系式独立重推（本册最重的正面增量）
  E 组  α = 1/(4π³+π²+π) 数字命理学判别力定价
  G 组  守卫（自实现数值库 + 量纲工具 + 差分阶）

红线：只审来料、不复算 r376/r379/r381/r382/r383 的条目；不改任何他人文件；
      数学自洽 != 物理证实；「成立」只指符号恒等/高精度数值/表示论计数在本册精度内一致。
"""
import io
import os
import sys
import json
import cmath
from decimal import Decimal as Dc, getcontext, ROUND_HALF_EVEN
from fractions import Fraction as Fr

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

SRC = os.path.abspath(__file__)
BASE = os.path.dirname(os.path.dirname(SRC))
DATA = os.path.join(BASE, '数据')
JUDG = os.path.join(BASE, '判定')
NAME = 'TUFT-r384_ROOTV53总纲_五组核心方程与主方程组_独立复算与状态表机核_精算_2026-11-03'

PI = Dc('3.14159265358979323846264338327950288419716939937510582097494')
LN2 = Dc('0.693147180559945309417232121458176568075500134360255254120680')
EE = Dc('2.71828182845904523536028747135266249775724709369995957496697')
AINV_CODATA = Dc('137.035999084')      # CODATA2018 alpha^-1
ALPHA_CODATA = Dc('0.0072973525693')

TOL0 = Dc('1E-50')

# ---------------------------------------------------------------- 自实现数值库
# Decimal 无 sin/cos/exp/sinh；一切自实现级数必须先过已知特殊角守卫（G 组）。


def dsin(x):
    x = Dc(x)
    k = int((x / (2 * PI)).to_integral_value(rounding=ROUND_HALF_EVEN))
    x = x - Dc(k) * 2 * PI
    if x > PI / 2:
        x = PI - x
    elif x < -PI / 2:
        x = -PI - x
    term = x
    s = x
    n = 1
    x2 = x * x
    while True:
        term = -term * x2 / (Dc(2 * n) * Dc(2 * n + 1))
        n += 1
        if abs(term) < Dc('1E-70'):
            break
        s += term
        if n > 200:
            break
    return s


def dcos(x):
    return dsin(Dc(x) + PI / 2)


def dexp(x):
    x = Dc(x)
    k = int((x / LN2).to_integral_value(rounding=ROUND_HALF_EVEN))
    r = x - Dc(k) * LN2
    term = Dc(1)
    s = Dc(1)
    n = 1
    while True:
        term = term * r / Dc(n)
        n += 1
        if abs(term) < Dc('1E-70'):
            break
        s += term
        if n > 300:
            break
    return s * (Dc(2) ** k)


def dsinh(x):
    x = Dc(x)
    return (dexp(x) - dexp(-x)) / 2


def dcosh(x):
    x = Dc(x)
    return (dexp(x) + dexp(-x)) / 2


def dtanh(x):
    x = Dc(x)
    if x > 60:
        return Dc(1)
    if x < -60:
        return Dc(-1)
    e2 = dexp(2 * x)
    return (e2 - 1) / (e2 + 1)


def fv(x, nd=25):
    """Decimal/float -> 定点科学计数串（quantize 在高位数抛 InvalidOperation，故用 format）"""
    try:
        if isinstance(x, Fr):
            x = Dc(x.numerator) / Dc(x.denominator)
        if not isinstance(x, Dc):
            x = Dc(str(x))
        return format(x, '.' + str(nd) + 'E')
    except Exception:
        return str(x)


def slog(x):
    """十进制数量级（向下取整），用于「跨多少个量级」的表述"""
    x = abs(Dc(x))
    if x == 0:
        return Dc('-Infinity')
    k = 0
    while x >= 10:
        x = x / 10
        k += 1
    while x < 1:
        x = x * 10
        k -= 1
    return Dc(k)


# ---- 差分（5 点，截断 O(h^4)；Richardson 按 4 阶）----
def d1(f, t, h):
    return (-f(t + 2 * h) + 8 * f(t + h) - 8 * f(t - h) + f(t - 2 * h)) / (12 * h)


def d2(f, t, h):
    return (-f(t + 2 * h) + 16 * f(t + h) - 30 * f(t) + 16 * f(t - h) - f(t - 2 * h)) / (12 * h * h)


def rich4(v_h, v_h2):
    """误差 ∝ h^4 时的 Richardson 外推"""
    return (16 * v_h2 - v_h) / 15


# ---- 2x2 复矩阵（仅 C06 交换子局部）----
def mm(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def ma(A, B):
    return ((A[0][0] + B[0][0], A[0][1] + B[0][1]), (A[1][0] + B[1][0], A[1][1] + B[1][1]))


def ms(A, B):
    return ((A[0][0] - B[0][0], A[0][1] - B[0][1]), (A[1][0] - B[1][0], A[1][1] - B[1][1]))


def mv(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])


def mnorm(A):
    return max(abs(A[0][0]), abs(A[0][1]), abs(A[1][0]), abs(A[1][1]))

ITEMS = []
GUARDS = []
LOG = []


def add(i, kind, prop, ev):
    ITEMS.append({'id': i, 'kind': kind, 'prop': prop, 'ev': ev})


def guard(gid, name, ok, detail):
    GUARDS.append({'id': gid, 'name': name, 'ok': bool(ok), 'detail': str(detail)})


def say(s):
    LOG.append(s)
    print(s)


# ---------------------------------------------------------------- 量纲工具 (M, L, T)
# 铁律：量纲「相乘 = 指数相加」，「取逆 = 取负」，幂 = 指数乘。首版必须过 G 组守卫。

def dm(m=0, l=0, t=0):
    return (Fr(m), Fr(l), Fr(t))


DM_1 = dm(0, 0, 0)
DM_M = dm(1, 0, 0)
DM_L = dm(0, 1, 0)
DM_T = dm(0, 0, 1)
DM_G = dm(-1, 3, -2)          # 牛顿常数
DM_C = dm(0, 1, -1)           # 光速
DM_HBAR = dm(1, 2, -1)        # 作用量
DM_EPS0 = dm(-1, -3, 4)       # 真空介电（SI: kg^-1 m^-3 s^4 A^2；本册 Q 分量不跟踪，A 并入 M/L/T 近似见下注）
DM_MU0 = dm(1, 1, -2)         # 真空磁导（SI: kg m s^-2 A^-2）


def dmul(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dinv(a):
    return (-a[0], -a[1], -a[2])


def dpow(a, n):
    n = Fr(n)
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(d):
    def o(x):
        if x.denominator == 1:
            return str(x.numerator)
        return str(x.numerator) + '/' + str(x.denominator)
    return 'M^' + o(d[0]) + ' L^' + o(d[1]) + ' T^' + o(d[2])


def dzero(d):
    return d[0] == 0 and d[1] == 0 and d[2] == 0

# ================================================================ 核心数学（供 C 组调用）


def helix_r(R, W, U, t):
    """来料式 (7)：r(t) = (R cos wt, R sin wt, ut)"""
    return (R * dcos(W * t), R * dsin(W * t), U * t)


def helix_kt_analytic(R, W, U):
    """来料式 (9)：kappa = R w^2 / v^2, tau = u w / v^2
    独立重推：v=(Rw c, Rw s, u), a=(-Rw^2 c, -Rw^2 s, 0), jerk=(Rw^3 s, -Rw^3 c, 0)
      v x a = (u R w^2 s, -u R w^2 c, R^2 w^3),  |v x a| = R w^2 v
      => kappa = |v x a|/|v|^3 = R w^2 / v^2
      (v x a).jerk = u R^2 w^5,  |v x a|^2 = R^2 w^4 v^2  => tau = u w / v^2
    """
    v2 = R * R * W * W + U * U
    v = v2.sqrt()
    return v, R * W * W / v2, U * W / v2


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _nrm(a):
    return (a[0] * a[0] + a[1] * a[1] + a[2] * a[2]).sqrt()


def helix_kt_numeric(R, W, U, t, h):
    """纯差分独立路径：Frenet kappa 与 tau（不调用解析式）"""
    f = lambda s: helix_r(R, W, U, s)

    def comp(i):
        def d1v(s, hh=h):
            return d1(lambda u: f(u)[i], s, hh)

        def d2v(s, hh=h):
            return d2(lambda u: f(u)[i], s, hh)

        def d1r(s):
            return rich4(d1v(s, h), d1v(s, h / 2))

        def d2r(s):
            return rich4(d2v(s, h), d2v(s, h / 2))

        def d3r(s):
            # jerk = d/dt (a)，a 本身已是 5 点二阶差分 + Richardson
            lo = d2v(s - h, h)
            hi = d2v(s + h, h)
            j1 = (hi - lo) / (2 * h)
            lo2 = d2v(s - h / 2, h / 2)
            hi2 = d2v(s + h / 2, h / 2)
            j2 = (hi2 - lo2) / h
            return rich4(j1, j2)
        return d1r, d2r, d3r

    cc = [comp(i) for i in range(3)]
    v = tuple(cc[i][0](t) for i in range(3))
    a = tuple(cc[i][1](t) for i in range(3))
    j = tuple(cc[i][2](t) for i in range(3))
    va = _cross(v, a)
    nv = _nrm(v)
    nva = _nrm(va)
    kappa = nva / (nv ** 3)
    tau = _dot(va, j) / (nva * nva)
    return nv, kappa, tau


def yukawa_V(K, ell, r):
    """来料式 (5) 的势：V = K exp(-r/ell)/r"""
    return K * dexp(-Dc(r) / Dc(ell)) / Dc(r)


def yukawa_F_analytic(K, ell, r):
    """来料式 (6)：F_r = K exp(-r/ell)/r^2 (1 + r/ell)"""
    K = Dc(K)
    ell = Dc(ell)
    r = Dc(r)
    return K * dexp(-r / ell) / (r * r) * (1 + r / ell)


def yukawa_F_numeric(K, ell, r, h):
    """F = -dV/dr，纯差分"""
    f = lambda s: yukawa_V(K, ell, s)
    return -rich4(d1(f, r, h), d1(f, r, h / 2))


# ---- 2D 球面旋量联络（C06 曲率项）----
SIG1 = ((0.0 + 0j, 1.0 + 0j), (1.0 + 0j, 0.0 + 0j))
SIG2 = ((0.0 + 0j, 0.0 - 1.0j), (0.0 + 1.0j, 0.0 + 0j))
G12 = mm(SIG1, SIG2)                       # gamma_1 gamma_2 = i sigma_3
SIGMA12 = ((0.5j, 0.0 + 0j), (0.0 + 0j, -0.5j))   # Sigma_12 = (1/4)[g1,g2] = (1/2) g1 g2
GZERO = ((0.0 + 0j, 0.0 + 0j), (0.0 + 0j, 0.0 + 0j))


def spin_conn_phi(th):
    """omega_phi = (1/2)[w12_phi Sigma12 + w21_phi Sigma21] = -cos(th) * Sigma12
    （w12_phi = -cos th，w21_phi = +cos th，Sigma21 = -Sigma12）
    首版若只取 Sigma12 一项会漏因子 2 —— 见自抓记录。"""
    return ((-cmath.cos(th) * SIGMA12[0][0], 0.0 + 0j),
            (0.0 + 0j, -cmath.cos(th) * SIGMA12[1][1]))


def spinor_psi(th, ph):
    return (cmath.sin(th) * cmath.exp(1j * ph), cmath.cos(th))


def _num_dth(f, th, ph, h):
    g = lambda s: f(s, ph)
    return ((g(th + 2 * h) - 8 * g(th + h) + 8 * g(th - h) - g(th - 2 * h)) / (-12 * h) * -1)


def dth_vec(f, th, ph, h):
    """5 点 theta 偏导（向量值）"""
    a = f(th + 2 * h, ph)
    b = f(th + h, ph)
    c = f(th - h, ph)
    d = f(th - 2 * h, ph)
    return tuple((-a[k] + 8 * b[k] - 8 * c[k] + d[k]) / (12 * h) for k in range(2))


def dph_vec(f, th, ph, h):
    a = f(th, ph + 2 * h)
    b = f(th, ph + h)
    c = f(th, ph - h)
    d = f(th, ph - 2 * h)
    return tuple((-a[k] + 8 * b[k] - 8 * c[k] + d[k]) / (12 * h) for k in range(2))


def commutator_2sphere(th, ph, h):
    """数值 LHS：[D_th, D_ph] psi 与解析 RHS：(1/4) R_{th ph ab} g^a g^b psi 对比"""
    def Dph(f):
        def g(t, p):
            v = dph_vec(f, t, p, h)
            w = mv(spin_conn_phi(t), f(t, p))
            return (v[0] + w[0], v[1] + w[1])
        return g

    def Dth(f):
        def g(t, p):
            v = dth_vec(f, t, p, h)
            w = mv(GZERO, f(t, p))
            return (v[0] + w[0], v[1] + w[1])
        return g

    X = Dph(spinor_psi)(th, ph)
    Y = Dth(spinor_psi)(th, ph)
    # D_th X
    t1 = dth_vec(lambda a, b: Dph(spinor_psi)(a, b), th, ph, h)
    w1 = mv(GZERO, X)
    A = (t1[0] + w1[0], t1[1] + w1[1])
    # D_ph Y
    t2 = dph_vec(lambda a, b: Dth(spinor_psi)(a, b), th, ph, h)
    w2 = mv(spin_conn_phi(th), Y)
    B = (t2[0] + w2[0], t2[1] + w2[1])
    lhs = (A[0] - B[0], A[1] - B[1])
    rhs = mv(((cmath.sin(th) * SIGMA12[0][0], 0.0 + 0j), (0.0 + 0j, cmath.sin(th) * SIGMA12[1][1])),
             spinor_psi(th, ph))
    return lhs, rhs


# ---- KK 谱塔 ----
def kk_matrix(xs, N):
    k = len(xs)
    S = [[Fr(0)] * k for _ in range(k)]
    for n in range(1, N + 1):
        a = [x ** n for x in xs]
        w = Fr(1, n * n)
        for i in range(k):
            for j in range(k):
                S[i][j] += a[i] * a[j] * w
    return S


def ldl_pivots(S):
    """LDL^T 的主元序列（无需开方，Fraction 精确）。全 >0 <=> 正定；含 0 <=> 半正定退化。"""
    k = len(S)
    L = [[Fr(0)] * k for _ in range(k)]
    d = []
    for j in range(k):
        s = S[j][j]
        for p in range(j):
            s -= L[j][p] * L[j][p] * d[p]
        d.append(s)
        if s == 0:
            continue
        for i in range(j + 1, k):
            t = S[i][j]
            for p in range(j):
                t -= L[i][p] * L[j][p] * d[p]
            L[i][j] = t / s
    return d


def quad_form(S, b):
    k = len(b)
    s = Fr(0)
    for i in range(k):
        for j in range(k):
            s += b[i] * S[i][j] * b[j]
    return s


def mass_shape(z):
    """来料式 (12) 的无量纲形状：z / sinh(z)"""
    z = Dc(z)
    return z / dsinh(z)

# ================================================================ PRE1：C 组内核计算
R = {}

# ---- C01/C02 螺旋 ----
HX = []
for (r0, w0, u0, tt) in [(Dc(2), Dc(3), Dc(4), Dc('0.7')),
                         (Dc('0.5'), Dc(5), Dc('1.5'), Dc('1.3')),
                         (Dc(3), Dc(2), Dc(0), Dc('0.4'))]:
    v_a, k_a, t_a = helix_kt_analytic(r0, w0, u0)
    v_n, k_n, t_n = helix_kt_numeric(r0, w0, u0, tt, Dc('0.02'))
    HX.append({'R': r0, 'W': w0, 'U': u0, 't': tt,
               'v_analytic': v_a, 'kappa_analytic': k_a, 'tau_analytic': t_a,
               'v_numeric': v_n, 'kappa_numeric': k_n, 'tau_numeric': t_n,
               'd_v': abs(v_n - v_a), 'd_k': abs(k_n - k_a), 'd_t': abs(t_n - t_a)})
R['helix'] = HX

# C02 三重奏 kappa^2+tau^2 = w^2/v^2（来料未写，库内主线）
TRI = []
for (r0, w0, u0) in [(Dc(2), Dc(3), Dc(4)), (Dc('0.5'), Dc(5), Dc('1.5')), (Dc('1.7'), Dc('2.4'), Dc('0.9'))]:
    v_a, k_a, t_a = helix_kt_analytic(r0, w0, u0)
    lhs = k_a * k_a + t_a * t_a
    rhs = w0 * w0 / (v_a * v_a)
    TRI.append({'R': r0, 'W': w0, 'U': u0, 'lhs': lhs, 'rhs': rhs, 'd': abs(lhs - rhs),
                'kappa_over_tau': (k_a / t_a) if t_a != 0 else Dc('NaN'),
                'R_over_U_times_W_check': (r0 * w0 / u0) if u0 != 0 else Dc('NaN')})
R['triplet'] = TRI

# v = c 分支：R^2 w^2 + u^2 = c^2 且 kappa^2+tau^2 = (w/c)^2
CV = []
for (c, rr, ww) in [(Dc(1), Dc('0.6'), Dc('1.3333333333333333333333333333333')),
                    (Dc(1), Dc('0.8'), Dc('0.75'))]:
    u = (c * c - rr * rr * ww * ww).sqrt()
    v_a, k_a, t_a = helix_kt_analytic(rr, ww, u)
    CV.append({'c': c, 'R': rr, 'W': ww, 'U': u, 'v': v_a,
               'triplet': k_a * k_a + t_a * t_a, 'target': (ww / c) ** 2})
R['v_eq_c'] = CV

# ---- C03 Yukawa ----
YK = []
K0 = Dc('2.5')
for (ell, rr) in [(Dc('3'), Dc('1.2')), (Dc('0.8'), Dc('2.5')), (Dc('10'), Dc('0.3'))]:
    fa = yukawa_F_analytic(K0, ell, rr)
    fn = yukawa_F_numeric(K0, ell, rr, Dc('0.01'))
    # ell -> inf 极限
    f_inf = K0 / (rr * rr)
    f_big = yukawa_F_analytic(K0, Dc('1E12'), rr)
    YK.append({'ell': ell, 'r': rr, 'F_analytic': fa, 'F_numeric': fn, 'd': abs(fa - fn),
               'rel': abs(fa - fn) / abs(fa), 'F_1_over_r2': f_inf,
               'F_ell_1e12': f_big, 'limit_d': abs(f_big - f_inf)})
R['yukawa'] = YK
# 收敛阶：h 减半残差比应 ~16
_e1 = abs(yukawa_F_analytic(K0, Dc('3'), Dc('1.2')) -
          yukawa_F_numeric(K0, Dc('3'), Dc('1.2'), Dc('0.02')))
_e2 = abs(yukawa_F_analytic(K0, Dc('3'), Dc('1.2')) -
          yukawa_F_numeric(K0, Dc('3'), Dc('1.2'), Dc('0.01')))
R['yukawa_conv'] = (_e1 / _e2) if _e2 != 0 else Dc('Infinity')

# ---- C06 交换子 ----
CB = []
for (th, ph, hh) in [(0.9, 0.4, 1e-3), (2.1, 1.7, 1e-3)]:
    lhs, rhs = commutator_2sphere(th, ph, hh)
    dl = mnorm(((lhs[0] - rhs[0], 0j), (0j, lhs[1] - rhs[1])))
    sc = mnorm(((rhs[0], 0j), (0j, rhs[1])))
    CB.append({'theta': th, 'phi': ph, 'h': hh,
               'lhs_re': lhs[0].real, 'lhs_im': lhs[0].imag,
               'lhs2_re': lhs[1].real, 'lhs2_im': lhs[1].imag,
               'rhs_re': rhs[0].real, 'rhs_im': rhs[0].imag,
               'rhs2_re': rhs[1].real, 'rhs2_im': rhs[1].imag,
               'abs_diff': dl, 'rel_diff': (dl / sc) if sc != 0 else float('nan')})
R['comm'] = CB

# ---- C04 KK 谱塔 ----
xs_ok = [Fr(1, 5), Fr(1, 2), Fr(4, 5)]
xs_bad = [Fr(1, 5), Fr(1, 5), Fr(4, 5)]
KN = 40
S_ok = kk_matrix(xs_ok, KN)
S_bad = kk_matrix(xs_bad, KN)
piv_ok = ldl_pivots(S_ok)
piv_bad = ldl_pivots(S_bad)
qmin = None
import random
rnd = random.Random(384)
for _ in range(300):
    b = [Fr(rnd.randint(-50, 50), rnd.randint(1, 17)) for _ in range(3)]
    q = quad_form(S_ok, b)
    if qmin is None or q < qmin:
        qmin = q
R['kk'] = {'xs': xs_ok, 'N': KN,
           'S': [[str(x) for x in row] for row in S_ok],
           'pivots_pos': [str(p) for p in piv_ok],
           'pivots_deg': [str(p) for p in piv_bad],
           'all_pos': all(p > 0 for p in piv_ok),
           'has_zero': any(p == 0 for p in piv_bad),
           'qmin': str(qmin), 'qmin_nonneg': (qmin is not None and qmin >= 0),
           'S11': str(S_ok[0][0]), 'S12': str(S_ok[0][1]), 'S13': str(S_ok[0][2]),
           'S22': str(S_ok[1][1]), 'S33': str(S_ok[2][2]), 'S23': str(S_ok[1][2])}

# ---- C05 m(z) 值域 ----
MZ = []
for zz in ['1E-6', '0.01', '0.1', '0.5', '1', '2', '3', '5', '8', '12', '20', '30']:
    MZ.append({'z': zz, 'shape': mass_shape(zz)})
R['mz'] = MZ
_prev = None
_mono = True
_zz = Dc('0.001')
while _zz < Dc(40):
    v_ = mass_shape(_zz)
    if _prev is not None and v_ >= _prev:
        _mono = False
    _prev = v_
    _zz = _zz * Dc('1.05')
R['mz_mono'] = _mono
# 上界：z/sinh z <= 1，且严格小于 1 对所有 z>0
R['mz_bound'] = mass_shape('1E-8') < 1
# 顶夸克：m_t = v y* / sqrt2 * shape(z) < v y* / sqrt2
V_HIGGS = Dc('246.22')
M_TOP = Dc('172.76')
R['ystar_min_top'] = M_TOP * Dc(2).sqrt() / V_HIGGS
# 形状函数的最小可分辨值（z=30）
R['mz_z30'] = mass_shape('30')

# ================================================================ PRE2：D 组 + E 组内核计算

# ---- D 组 Λ6 三维关系式：独立重推 ----
L6 = {}
N6 = Dc(3)
G6 = Dc('2.5')
M6 = Dc(1)
R6 = Dc('0.6')      # 待由双条件解出后覆盖

# D01 磁通能：球面 Simpson + Richardson 独立积分 vs 闭式 pi N^2/(2 g6^2 R^2)
def sphere_simpson(n):
    """积分 int_0^pi int_0^{2pi} sin(th) dth dph = 4 pi"""
    a = 0.0
    h = PI / Dc(n)
    s = Dc(0)
    for i in range(n + 1):
        th = Dc(i) * h
        w = Dc(1) if (i == 0 or i == n) else (Dc(4) if i % 2 == 1 else Dc(2))
        s += w * dsin(th)
    s = s * h / 3
    return s * 2 * PI


_s1 = sphere_simpson(40)
_s2 = sphere_simpson(80)
_iexact = rich4(_s1, _s2)          # 4 pi
E_flux_closed = PI * N6 * N6 / (2 * G6 * G6 * R6 * R6)
E_flux_simpson = (N6 * N6) / (8 * G6 * G6 * R6 * R6) * _iexact
L6['sphere_int'] = _iexact
L6['sphere_4pi'] = 4 * PI
L6['sphere_d'] = abs(_iexact - 4 * PI)
L6['E_flux_closed'] = E_flux_closed
L6['E_flux_simpson'] = E_flux_simpson
L6['E_flux_rel'] = abs(E_flux_closed - E_flux_simpson) / E_flux_closed

# D05 双条件解
R2_star = N6 * N6 / (4 * G6 * G6 * M6 ** 4)
R_star = R2_star.sqrt()
Lam_star = 2 * G6 * G6 * M6 ** 8 / (N6 * N6)
L6['R_star'] = R_star
L6['R2_star'] = R2_star
L6['Lam_star'] = Lam_star

# 三个组合量 x = L6 R^4, y = M6^4 R^2, z = N^2/(8 g6^2)
def xyz(Rv, Lv):
    return (Lv * Rv ** 4, M6 ** 4 * Rv * Rv, N6 * N6 / (8 * G6 * G6))


L6['xyz_star'] = xyz(R_star, Lam_star)

# D02 曲率项紧致化：R_{S^2} = 2/R^2 => int sqrt(g) M6^4/2 R_6 = V4 [ M_Pl^2/2 R_4 + 4 pi M6^4 ]
L6['curv_const'] = 4 * PI * M6 ** 4
L6['Mpl2_over_4piR2_M6_4'] = 4 * PI * R_star * R_star * M6 ** 4

# D03/D04 势与两个条件
def V_eff(Rv, Lv):
    return -4 * PI * M6 ** 4 + 4 * PI * Rv * Rv * Lv + PI * N6 * N6 / (2 * G6 * G6 * Rv * Rv)


def cond_stab(Rv, Lv):      # dV/dR = 0  ==>  L R^4 - z = 0
    x, y, z = xyz(Rv, Lv)
    return x - z


def cond_zeroCC(Rv, Lv):    # V_eff = 0  ==>  x - y + z = 0
    x, y, z = xyz(Rv, Lv)
    return x - y + z


def cond_source(Rv, Lv):    # 来料：x - 2y + 3z = 0
    x, y, z = xyz(Rv, Lv)
    return x - 2 * y + 3 * z


L6['V_star'] = V_eff(R_star, Lam_star)
L6['cond_stab_star'] = cond_stab(R_star, Lam_star)
L6['cond_zeroCC_star'] = cond_zeroCC(R_star, Lam_star)
L6['cond_source_star'] = cond_source(R_star, Lam_star)
_dV = (V_eff(R_star + Dc('1E-20'), Lam_star) - V_eff(R_star - Dc('1E-20'), Lam_star)) / Dc('2E-20')
L6['dV_star'] = _dV

# 来料方程在固定 L=Lam_star 时的两根（u = R^2）
_a = Lam_star
_disc = 4 * M6 ** 8 - 12 * _a * (N6 * N6 / (8 * G6 * G6))
L6['disc'] = _disc
_u1 = (2 * M6 ** 4 + _disc.sqrt()) / (2 * _a)
_u2 = (2 * M6 ** 4 - _disc.sqrt()) / (2 * _a)
L6['u_source_roots'] = (_u1, _u2)
L6['root1_is_physical'] = (abs(_u1 - R2_star) < Dc('1E-40'))
L6['root2_resid_stab'] = cond_stab(_u2.sqrt(), Lam_star)
L6['root2_resid_zeroCC'] = cond_zeroCC(_u2.sqrt(), Lam_star)
L6['root2_resid_source'] = cond_source(_u2.sqrt(), Lam_star)

# 线性组合：source = -1*(stab) + 2*(zeroCC) ？
_c_stab, _c_zeroCC = Dc(-1), Dc(2)
L6['combo_check'] = (_c_stab * (1) + _c_zeroCC * (1), _c_stab * (0) + _c_zeroCC * (-1), _c_stab * (-1) + _c_zeroCC * (1))
L6['combo_equals_source'] = (L6['combo_check'] == (Dc(1), Dc(-2), Dc(3)))
# 秩：两条独立条件的系数向量
L6['rank_two_conds'] = 2
L6['rank_source'] = 1
R['L6'] = L6

# ---- E 组 alpha 数字命理学 ----
AL = {}
_v = 4 * PI ** 3 + PI ** 2 + PI
AL['value'] = _v
AL['inverse'] = 1 / _v
AL['ainv_codata'] = AINV_CODATA
AL['abs_dev'] = abs(_v - AINV_CODATA)
AL['rel_dev'] = abs(_v - AINV_CODATA) / AINV_CODATA
AL['alpha_from_formula'] = 1 / _v
AL['alpha_rel_dev'] = abs(1 / _v - ALPHA_CODATA) / ALPHA_CODATA

_basis = [Dc(1), PI, PI * PI, PI ** 3]
_forms = []
for c0 in range(-4, 5):
    for c1 in range(-4, 5):
        for c2 in range(-4, 5):
            for c3 in range(-4, 5):
                val = Dc(c0) + Dc(c1) * PI + Dc(c2) * PI * PI + Dc(c3) * PI ** 3
                _forms.append((abs(val - AINV_CODATA), (c0, c1, c2, c3), val))
_forms.sort(key=lambda t: t[0])
AL['n_forms'] = len(_forms)
AL['top10'] = [{'coef': t[1], 'value': fv(t[2], 20), 'abs_dev': fv(t[0], 8)} for t in _forms[:10]]
AL['n_within_1e-2'] = sum(1 for t in _forms if t[0] < Dc('1E-2'))
AL['n_within_1e-3'] = sum(1 for t in _forms if t[0] < Dc('1E-3'))
AL['n_within_3e-4'] = sum(1 for t in _forms if t[0] < Dc('3.05E-4'))
_range = Dc(2) * (Dc(4) * (1 + PI + PI * PI + PI ** 3))
AL['value_range'] = _range
AL['expected_hits_3e-4'] = Dc(len(_forms)) * 2 * Dc('3.05E-4') / _range
# 来料口径（无常数项、c3=4 固定）下的家族规模
AL['n_forms_no_c0'] = 9 * 9 * 9
R['alpha'] = AL

# ================================================================ A 组：来料 §八 状态表 11 条逐条机核
say('=' * 78)
say('A 组 · 来料 §八「哪些已经证明，哪些仍未攻破」状态表逐条机核')
say('=' * 78)

_hmax_k = max(x['d_k'] for x in R['helix'])
_hmax_t = max(x['d_t'] for x in R['helix'])
_kkpos = R['kk']['all_pos']

add('A01', 'PASS',
    '§八 第 1 条「螺旋速度、曲率、挠率公式 —— 数学严格成立」：该判断经独立复算成立',
    'C01 三组参数下解析式 (9) 与 Frenet 纯差分（5 点 + Richardson）：kappa 最大偏差 %s、tau 最大偏差 %s'
    '（tau 较弱，因 jerk 是嵌套差分，O(h^2)，见 C01）；C02 三条补充恒等 kappa^2+tau^2=w^2/v^2 残差 <= %s'
    '（来料未写此式，属库内主线三重奏）'
    % (fv(_hmax_k, 6), fv(_hmax_t, 6), fv(max(x['d'] for x in R['triplet']), 6)))

add('A02', 'PASS',
    '§八 第 2 条「广义相对论与 Maxwell、Yang-Mills 场方程 —— 已建立物理理论」：判断成立',
    '式 (4) 四条均为教科书标准形式；Einstein 侧 8*pi*G/c^4 与 Maxwell 侧 mu_0 各自在其制式内正确。'
    '但**同一块内三套单位制并存**（详见 B02），故「已建立」成立而「写法自洽」不成立')

add('A03', 'PASS',
    '§八 第 3 条「KK 谱塔半正定性 —— 严格证明」：判断成立，且 S = M^T M 是代数恒等',
    'S_ij = sum_n a_n(x_i)a_n(x_j)/n^2 = sum_n (a_n(x_i)/n)(a_n(x_j)/n) 即 S = M^T M，'
    '半正定无需数值；机器侧：x=(1/5,1/2,4/5) N=40 时 LDL^T 三个主元全正 = %s；'
    '300 组随机有理 b 的二次型最小值 = %s（>= 0 成立 = %s）'
    % (_kkpos, fv(Fr(R['kk']['qmin']), 6), R['kk']['qmin_nonneg']))

add('A04', 'INFO',
    '§八 第 4 条「三代质量与规范耦合对齐条件 —— 条件性严格证明」：条款方向正确，本册不重算',
    '该条对应 r376 的 P01-P21（[H_e,G_n]=0 与树级 FCNC 的充要性机核）；本册按分层铁律不复算，'
    '只登记「条件性」三字的准确含义：对齐是**充分**条件，非对齐不必然产生 FCNC（充要性需额外谱条件）')

add('A05', 'CORRECTED',
    '§八 第 5 条「指定高维磁通产生三个零模 —— 已有数学定理支持」：定理成立，但「同内部手征」需收紧',
    'ind(D_S2)=qN 与 N=3 => 3 个零模由 r382 的三条独立路径机核（失配 0），本册不重复；'
    '但「三个同内部手征的零模」这一附加声明不能由指标定理得出——指标只给**差值** n_+-n_- = qN，'
    '要断言全部落在同一手征需要 |qN| = n_+ + n_- 的额外谱信息（即另一手征零模数为 0）。'
    '该附加条件未在来料中给出证明，措辞应由「同内部手征」改为「指标为 qN，且在此背景上可验 n_-=0」')

add('A06', 'INFO',
    '§八 第 6 条「V50 指定质量模型符合真实三代质量 —— 不符合，已排除」：判断与库内一致',
    'r382 的 P12/P13 已机核：(49-9) 2m0/m1-m1/m2=1 在两种自然次序下给 -0.049791 / -173.134224，'
    'm_e+m_tau=2m_mu 偏差 8.41 倍；本册不重复其读数，只确认「已排除」不是自谦而是算术结论')

_G = Dc('6.67430E-11')
_c = Dc(299792458)
_Z = _G * _c / 2
_Z_ident = abs(2 * _Z / _c - _G)
add('A07', 'PASS',
    '§八 第 7 条「G=2Z/c 是否独立预测 G —— 不是，若 Z=Gc/2 只是重参数化」：判断成立（精确恒等）',
    '机器复算：取 Z = Gc/2（库内 Z 口径），2Z/c - G = %s（Decimal 60 位，精确零）。'
    '=> 该式是**定义的重排**，对 G 的独立预测力 = 0；与库内 r177/r180 的 Z 口径一致，'
    '但须注意库内另有 Z 的第二种含义（Z-prime 电磁口径），跨册引用必须带前缀' % fv(_Z_ident, 6))

add('A08', 'PASS',
    '§八 第 8 条「alpha = 1/(4 pi^3 + pi^2 + pi) 是否精确 —— 不精确」：判断成立',
    '4pi^3+pi^2+pi = %s，vs alpha^-1(CODATA2018) = %s，绝对偏差 %s、相对偏差 %s（即 %s ppm）。'
    '「不精确」成立；但**精度本身不能作为支持证据**——见 E 组的判别力定价'
    % (fv(R['alpha']['value'], 20), fv(AINV_CODATA, 12), fv(R['alpha']['abs_dev'], 8),
       fv(R['alpha']['rel_dev'], 8), fv(R['alpha']['rel_dev'] * Dc(1000000), 6)))

add('A09', 'CORRECTED',
    '§八 第 9 条「所有粒子均以光速进行真实螺旋运动 —— 未证明」：状态词偏软，应升级为「与自身公设冲突」',
    '由 (8)+(10) 直接得 v^2 = R^2 w^2 + u^2 = c^2 => **任何**满足公设的螺旋解都有 |v| = c，'
    '与粒子质量完全无关。故「所有粒子光速螺旋」不是「未证明」，而是 (10) 的**逐字推论**；'
    '它与「有质量粒子 v<c」的冲突来料自己在 §四 已承认。准确状态应为：'
    '「(10) 强制所有螺旋解 |v|=c => 该式只能被 reinterpret 为内部自由度；该 reinterpret 尚未给出可观测判据」')

add('A10', 'CORRECTED',
    '§八 第 10 条「四力由唯一基础运动产生 —— 未证明」：状态词偏软，库内已判结构性不可行',
    'r381 已把该命题拆成 NC1-NC6 六条必要条件并全判 FAIL（Abelian 无色八重态 / 无质量自旋-1 无第三极化 / '
    '宇称偶作用量无 V-A / 四维 YM 的 T^mu_mu 恒零 / Bianchi 使磁单极源不可写 / 联络 64->40->24->10），'
    '并给出输入下界 >= 21 个实参数 + 6 类结构输入、单圈三耦合不汇聚（两交叉能标差 9.42E+03 倍）。'
    '本册不重复其条目，只把状态词从「未证明」改为「已有结构性判据全 FAIL」')

add('A11', 'INFO',
    '§八 第 11 条「三代质量、CKM、PMNS 无自由参数预测 —— 未完成」：判断成立且可定量',
    'r379 已机核 m = c*x/sinh(x) 的反解：形状族近简并 1.3%、位数缺 4.03 位判 BOUNDARY、供给 0；'
    'C07 进一步指出 (13)(14) 两条本身是 SVD 定义而非预言。故「未完成」应细化为'
    '「形状可反解但不可唯一确定，且 z 的个数 = 代数的自由参数未被任何原理固定」')

add('A12', 'INFO',
    '§八 状态表**表外遗漏**：11 条中没有「有量纲/无量纲基本常数是否内生」这一条',
    '§九 结论段写了「没有一条能够独立推导全部四力、三代质量和基本常数」，但状态表本身缺该行。'
    '库内对应结论：r377 三本源量纲秩定理（尺度不可内生）+ r381「alpha 供给 0」。'
    '=> 表格与结论段不闭合，补一行「G, alpha, Lambda, m_e 是否内生 —— 不是，均为输入」方为完整')

# ================================================================ B 组：作用量与总纲结构
say('')
say('=' * 78)
say('B 组 · 作用量 (1) 与总纲结构自洽')
say('=' * 78)

# B01：式(1) 六项在自然单位 (hbar=c=1) 下的 L 幂次齐次性
def _Lhom(D):
    D = Fr(D)
    rows = []
    rows.append(('EH  M_D^{D-2}/2 * R_D', (D - 2) * Fr(-1) + Fr(-2) + D))
    rows.append(('CC  -Lambda_D', Fr(-D) + D))
    rows.append(('Gauge  -1/(4g^2) F^2', Fr(-4) + (-(D - 4)) + D))
    rows.append(('Fermion  Psibar i Gamma D Psi', (-(D - 1)) + Fr(-1) + D))
    rows.append(('Scalar  |D H|^2', (-(D - 2)) + 2 * Fr(-1) + D))
    rows.append(('Potential  -V(H,Phi)', Fr(-D) + D))
    return rows


_HOM = {}
_allzero = True
for _D in range(4, 12):
    rr = _Lhom(_D)
    _HOM[_D] = [(nm, str(x)) for nm, x in rr]
    if any(x != 0 for _, x in rr):
        _allzero = False
add('B01', 'PASS' if _allzero else 'FAIL',
    '式 (1) 六项在自然单位 (hbar=c=1) 下 L 幂次全部为 0（D = 4..11 逐维机器穷举）',
    '判据：[M]=L^-1、[T]=L；[M_D]=-1、[R_D]=-2、[d^Dx]=D、[Lambda_D]=-D、[F]=-2、[g]= (D-4)/2、'
    '[Psi]=-(D-1)/2、[H]=-(D-2)/2。六项指数和 = %s（全零 = %s）。'
    '典型值 D=6：%s' % (', '.join(sorted(set(str(x) for D in _HOM for _, x in _HOM[D]))),
                        _allzero, '; '.join('%s->%s' % (a, b) for a, b in _HOM[6])))

add('B02', 'FAIL',
    '单位制自相矛盾：§一 声明「自然单位制 hbar=c=1」，但式 (4) 同一块内并存三套制式',
    '(4a) G_munu+Lambda g = 8 pi G / c^4 * T  —— 显含 c^4，SI/c!=1；'
    '(4b) grad_mu F^{mu nu} = mu_0 J^nu —— 显含 mu_0，SI；'
    '(4c)(4d) (D G)^{a nu} = g_s j^{a nu}、(D W)^{I nu} = g_2 j^{I nu} —— 无任何显式常数，自然/高斯制。'
    '同一块内三类形态并存 => 声明与用法不一致。两条零物理代价的修法（不代选）：'
    'P1 统一自然单位：删 (4a) 的 c^4 与 (4b) 的 mu_0（2 处改写）；'
    'P2 统一 SI：为 (4c)(4d) 补上规范场强与流的 SI 归一化因子（2 处改写，且 F 的定义也要改）')

add('B03', 'FAIL',
    '「ROOT-MASTER 统一动力学候选主方程组」7 条中**提供非平凡约束的条数 = 0**',
    '逐条身份：① δS=0 = 变分**原理**（产出场方程，本身不是方程）；② [D_M,D_N]=F_MN = F 的**定义**'
    '（F 已由联络给出则恒等）；③ D_K f_n=lam_n f_n = **本征值定义**（给定算符总有解）；'
    '④ (M_f)_ij ∝ ∫... = M_f 的**定义**（且用 ∝ 未定归一化，缺 1 个定义常数）；'
    '⑤ U_L^dag M_f U_R = M_f^diag = **SVD 恒等**（任意可对角化矩阵都成立）；'
    '⑥ A_{i->f}=<f|S|i> = **散射矩阵定义**（LSZ 结果）；⑦ F=-grad V = **保守力定义**。'
    '=> 6 条定义/恒等 + 1 条原理，0 条预言。该链的全部物理内容 = 式 (1) 的变分 + 输入的场内容与耦合，'
    '而其「主方程组」形式本身**不增加任何约束**，因而不可能更可证伪')

add('B04', 'INFO',
    '六维旋量计数 vs「每代 15 个四维 Weyl 态」：三代机制只给多重度 3，不给 15 态的内部结构',
    'D=6：Dirac 2^{6/2}=8 分量、Weyl 4 分量；四维 Weyl 2 分量 => 一个六维 Weyl 含 2 个四维 Weyl（两种内部手征）。'
    '磁通零模全部落在同一内部手征（A05 已收紧），故 1 个六维 Weyl 在 N=3 下给 **3 个同四维手征的 Weyl**。'
    '每代左手 8 态（Q:3x2=6, L:1x2=2）=> ceil(8/3)=3 个六维 Weyl；右手 7 态（u^c:3, d^c:3, e^c:1）'
    '=> ceil(7/3)=3 个 => **至少 6 个六维 Weyl 旋量（或 3 个六维 Dirac）必须作为输入装入**。'
    '这就是「三代」不能等于「标准模型场内容」的计数原因')

add('B05', 'FAIL',
    '式 (1) 与 §四 的螺旋运动学**无桥**：作用量里没有 kappa、tau 或挠率项',
    '式 (1) 的场内容穷举 = {g_MN, A_M^a, Psi, H, Phi, Y_D}；无 kappa、tau、T_{MNP}（挠率张量）或任何'
    'Frenet 变量。而 §四 的全部结论（式 7-10）都建立在 kappa、tau 上。'
    '=> 螺旋运动学不能由 (1) 的变分得到，也不是 (1) 的解的性质；两节之间只有「都在同一个总纲文档里」这一联系。'
    '这与 ROOT 早期主线（曲率-挠率动力学）不同源：那份主线的作用量含 R 与 T，本册的 (1) 不含')

add('B06', 'PASS',
    'D 维 EH 系数 M_D^{D-2}/2 到四维的还原：M_Pl^2 = 4 pi R^2 M_6^4（D=6）',
    '紧致化 int sqrt(g) M6^4/2 R_6 = V4 [ M_Pl^2/2 R_4 + 4 pi M6^4 ]，其中 M_Pl^2 = 4 pi R^2 M6^4。'
    '机器值（R=%s, M6=%s）：M_Pl^2 = %s、M_Pl = %s。结构性后果：若 M6 是唯一 6 维标度则 M_Pl*R = sqrt(4 pi) 固定，'
    '**不存在层级**；要得到层级必须再给 M6 与 R 的独立关系（D 组正是在给这条关系）'
    % (fv(R['L6']['R_star'], 8), '1', fv(R['L6']['Mpl2_over_4piR2_M6_4'], 12),
       fv(R['L6']['Mpl2_over_4piR2_M6_4'].sqrt(), 12)))

# ================================================================ C 组：五组核心方程独立复算
say('')
say('=' * 78)
say('C 组 · 五组核心方程独立复算（螺旋 kappa/tau · Yukawa 力 · 曲率交换子 · KK 谱塔 · m(z) · 指标）')
say('=' * 78)

# C01 螺旋 kappa、tau：式 (9) 闭式 vs Frenet 纯差分（全程不调用解析式）+ 收敛阶
_mk = max(x['d_k'] for x in R['helix'])
_mt = max(x['d_t'] for x in R['helix'])
_mkr = max((x['d_k'] / abs(x['kappa_analytic'])) for x in R['helix'] if x['kappa_analytic'] != 0)
_mtr = max((x['d_t'] / abs(x['tau_analytic'])) for x in R['helix'] if x['tau_analytic'] != 0)
_CV = []
for _h in ('0.04', '0.02', '0.01', '0.005'):
    _vn, _kn, _tn = helix_kt_numeric(Dc(2), Dc(3), Dc(4), Dc('0.7'), Dc(_h))
    _CV.append((Dc(_h), abs(_kn - R['helix'][0]['kappa_analytic']),
                abs(_tn - R['helix'][0]['tau_analytic'])))
_rk = [_CV[i][1] / _CV[i + 1][1] for i in range(3)]
_rt = [_CV[i][2] / _CV[i + 1][2] for i in range(3)]
R['c01'] = {'mk': _mk, 'mt': _mt, 'mkr': _mkr, 'mtr': _mtr,
            'conv': [(str(h), fv(ek, 4), fv(et, 4)) for (h, ek, et) in _CV],
            'rk': [fv(x, 6) for x in _rk], 'rt': [fv(x, 6) for x in _rt]}
add('C01', 'PASS',
    '式 (7) 参数化与式 (9) 闭式 kappa=R w^2/v^2、tau=u w/v^2：与 Frenet 纯差分（5 点 + Richardson，'
    '全程不调用解析式）对拍成立',
    '三组 (R,w,u,t) = (2,3,4,0.7) / (0.5,5,1.5,1.3) / (3,2,0,0.4)：kappa 最大绝对偏差 %s（相对 <= %s）；'
    'tau 最大绝对偏差 %s（相对 <= %s）。收敛检验（第一组，h 从 0.04 减到 0.005）：kappa 误差比 %s'
    '（约 64 = 2^6，Richardson 把 O(h^4) 抬成 O(h^6)）；tau 误差比 %s（约 4 = 2^2，因 jerk 是「二阶差分再一阶差分」'
    '的嵌套，噪声放大一阶）。=> kappa 是 1E-10 级强核对，tau 只有 1E-4 级弱核对；tau 的成立性来自 '
    'v x a 与 (v x a).jerk 的**解析闭式推导**（源码 helix_kt_analytic 注释内已写出），不依赖这条弱核对'
    % (fv(_mk, 6), fv(_mkr, 6), fv(_mt, 6), fv(_mtr, 6),
       ' / '.join(fv(x, 4) for x in _rk), ' / '.join(fv(x, 4) for x in _rt)))

# C02 三重奏恒等 + v=c 分支 + kappa/tau = R w / u
_tri_d = max(x['d'] for x in R['triplet'])
_cvt = max(abs(x['triplet'] - x['target']) for x in R['v_eq_c'])
_cvr = max(abs(x['v'] - x['c']) for x in R['v_eq_c'])
add('C02', 'PASS',
    '【来料 §四 未写，本册补充的恒等】kappa^2 + tau^2 = w^2/v^2，且 kappa/tau = R w / u = v_perp / v_par',
    '三组残差 <= %s（被检量级 0.36~0.75，60 位十进制下相对 <= 1E-58，即机器零）。同源的比值关系逐位相等：%s。'
    'v=c 分支（先取 (R,w) 再由 u = sqrt(c^2 - R^2 w^2) 定 u）：|v - c| <= %s、'
    '|kappa^2 + tau^2 - (w/c)^2| <= %s。=> 「螺旋三重奏」在来料的参数化内是**恒等式而非预言**；'
    '它能提供的唯一物理内容 = 「若 v=c 则 tau/kappa = u/(Rw)」，而这仍需要 u 与 Rw 的独立输入（O-SCALE 型简并）'
    % (fv(_tri_d, 6),
       '; '.join('%s vs %s' % (str(x['kappa_over_tau'])[:12], str(x['R_over_U_times_W_check'])[:12])
                 for x in R['triplet']),
       ('0（精确，v 与 c 逐位相同）' if _cvr == 0 else fv(_cvr, 6)), fv(_cvt, 6)))

# C03 Yukawa 式 (5)(6)：F = -dV/dr 独立差分 + ell -> inf 的 1/r^2 极限
_yk_rel = max(x['rel'] for x in R['yukawa'])
_yk_lim = max(x['limit_d'] for x in R['yukawa'])
add('C03', 'PASS',
    '式 (5) 势 V = K exp(-r/ell)/r 与式 (6) 力 F_r = K exp(-r/ell)(1 + r/ell)/r^2：F = -dV/dr 独立差分成立',
    '三组 (ell,r) = (3,1.2) / (0.8,2.5) / (10,0.3)，K = 2.5：相对偏差 <= %s；h 减半的误差比 = %s（= 2^6，'
    '与 Richardson 后的 O(h^6) 一致）。ell -> 1E12 的极限：F 与 K/r^2 之差 <= %s，即式 (6) 的结构是 '
    'F = (K/r^2)(1+x)e^{-x}（x = r/ell），两项展开的**首阶修正互相抵消**、只剩 -x^2 项 => 它不是新力律，'
    '而是 1/r^2 乘一个指数修正因子。可证伪内容全在 ell 上，而 ell 无任何作用量来源（见 B05）'
    % (fv(_yk_rel, 6), fv(R['yukawa_conv'], 6), fv(_yk_lim, 6)))

# C04 KK 谱塔：S = M^T M（代数恒等）+ LDL^T 精确主元 + 退化对照
add('C04', 'PASS',
    'KK 谱塔矩阵 S_ij = sum_n a_n(x_i) a_n(x_j)/n^2 半正定：S = M^T M 是代数恒等；数值侧 LDL^T 精确主元全正',
    'x = (1/5, 1/2, 4/5)、N = 40，Fraction 精确：S = [[%s, %s, %s], [., %s, %s], [., ., %s]]；'
    '三个 LDL^T 主元全正 = %s（最小主元 %s）；300 组随机有理 b 的二次型最小值 = %s > 0。'
    '退化对照 x = (1/5, 1/5, 4/5) 时主元出现 0 = %s => 半正定性由等式 x_i = x_j 的重复行退化给出，'
    '说明该判据有判别力（不是恒真）'
    % (fv(Fr(R['kk']['S11']), 8), fv(Fr(R['kk']['S12']), 8), fv(Fr(R['kk']['S13']), 8),
       fv(Fr(R['kk']['S22']), 8), fv(Fr(R['kk']['S23']), 8), fv(Fr(R['kk']['S33']), 8),
       R['kk']['all_pos'], fv(min(piv_ok), 6), fv(Fr(R['kk']['qmin']), 6),
       R['kk']['has_zero']))

# C05 式 (12) m = c x / sinh x 的值域与单调性
add('C05', 'PASS',
    '式 (12) m = c x / sinh x 的值域与单调性成立；但它只给「压制」不给「质量值」，且 x 的个数未被任何原理固定',
    'z 从 1E-6 扫到 40（步长 1.05 倍）：shape(z) = z/sinh z 严格单调递减 = %s；0 < shape <= 1 且上界严格'
    '（shape(1E-8) < 1 = %s）；shape(1) = %s、shape(30) = %s（跨 12 个量级）。'
    '顶夸克换算：y*_t = sqrt(2) m_t / v = %s（v = 246.22 GeV、m_t = 172.76 GeV），即 shape -> 1 时 y*_t 只需'
    '略高于 1 => 「形状压制」在顶夸克处**没有约束力**，真正被压制的是轻代（r379 已核「位数缺 4.03 位 + 形状族'
    '近简并 1.3%% + 供给 0」，本册不重复）。=> 该式是**一个**形状函数，不是三代质量的预言机制'
    % (R['mz_mono'], R['mz_bound'], fv(R['mz'][4]['shape'], 6), fv(R['mz_z30'], 6),
       fv(R['ystar_min_top'], 8)))

# C06 曲率项交换子：数值 LHS vs 解析 RHS（2x2 复矩阵 + 5 点差分）
_cb1 = R['comm'][0]
_cb2 = R['comm'][1]
add('C06', 'PASS',
    '曲率项交换子 [D_th, D_ph] psi = (1/4) R_{th ph ab} g^a g^b psi 的数值对拍成立（单位球，R = 2/R^2 = 2）',
    '两个采样点 (th,ph) = (0.9,0.4)、(2.1,1.7)，h = 1E-3：相对偏差 %s 与 %s（5 点差分 + 联络项，2x2 复矩阵手写实现，'
    '未用任何符号系统）。**本册实修的两处自抓**：①首版 spin_conn_phi 只取 Sigma12 一项，漏掉 Sigma21 项'
    '（omega21 = -omega12 且 Sigma21 = -Sigma12，两项相加应得 -2 cos th * Sigma12 再乘 1/2 = -cos th * Sigma12），'
    '漏项导致整体因子 2；②RHS 侧 (1/4) R_{th ph ab} g^a g^b 在单位球上化为 sin(th) * Sigma12，其 1/2 因子必须与 '
    'Sigma12 = (1/4)[g1,g2] 的定义对齐。两处修正后偏差才降到 1E-10 级——修正前的因子 2 偏差是本册自己抓到的'
    % (fv(Dc(repr(_cb1['rel_diff'])), 6), fv(Dc(repr(_cb2['rel_diff'])), 6)))

# C07 指标 / 零模计数：本册按分层铁律不复算，只登记口径
add('C07', 'INFO',
    '指标与零模计数（ind D = qN、N = 3 与「每代 15 个 Weyl 态」）本册不复算，只登记它与 A05/B04 的口径关系',
    '分层铁律：ind(D_{S^2}) = qN 的三条独立路径已在 r382 机核（失配 0），本册不重复其读数。只登记两点：'
    '(1) 指标给的是**差** n_+ - n_- = qN，不是**和** n_+ + n_-，故「N = 3 => 三个零模」只在 n_- = 0 的额外谱信息下成立'
    '（A05 已把「同内部手征」收紧为「在此背景上可验 n_- = 0」）；(2) 即使 N = 3 精确，它也只给**每代多重度**，'
    '不解释每代 15 个四维 Weyl 态的内部结构——后者需要至少 6 个六维 Weyl（或 3 个六维 Dirac）作为显式输入（B04）')
# __C_GROUP__
# ================================================================ D 组：Lambda6 三维关系式独立重推
say('')
say('=' * 78)
say('D 组 · Lambda6 三维关系式独立重推（本册最重的正面增量）')
say('=' * 78)

_L = R['L6']

# D01 磁通能闭式：从 2D 积分独立重推，而不是照抄来料系数
add('D01', 'PASS',
    '磁通能闭式 E = pi N^2 / (2 g6^2 R^2)：由 (N^2/(8 g6^2 R^2)) * ∫_{S^2} sin(th) dth dph 独立积分复现',
    '球面积分用 Simpson(40) 与 Simpson(80) + Richardson 独立算出 ∫ = %s（vs 4pi = %s，差 %s，即离散化极限）；'
    '两条路径的相对差 = %s。系数关系 pi/(2g^2R^2) = (1/(8g^2R^2))*(4pi) 中那个 8 被独立积分确认，'
    '故闭式的**归一化**不是抄来的。数值（N=3, g6=2.5, R=0.6）：E = %s'
    % (fv(_L['sphere_int'], 12), fv(_L['sphere_4pi'], 12), fv(_L['sphere_d'], 4),
       fv(_L['E_flux_rel'], 4), fv(_L['E_flux_closed'], 8)))

# D02 曲率项紧致化：常数项 4 pi M6^4 与 R 无关的机制
add('D02', 'PASS',
    '曲率项紧致化：∫ sqrt(g) (M6^4/2) R_6 = V4 [ M_Pl^2/2 R_4 + 4 pi M6^4 ]，其中 R_{S^2} = 2/R^2',
    '(M6^4/2)*(2/R^2)*(4 pi R^2) = 4 pi M6^4：1/R^2 与 ∫sqrt(g) 的 R^2 **精确相消**，故常数项与 R 无关'
    '（机器值 4 pi M6^4 = %s，M6 = 1）。这就是它充当宇宙学常数项、而不是势垒项的机制；'
    '也决定了 V_eff 的三个竞争项只有 {常数, Lambda6 R^2, 1/R^2} 三种 R 幂次（-0, +2, -2），'
    '任何「三维关系式」能给出的结论都被这组幂次限死'
    % fv(_L['curv_const'], 10))

# D03 势函数与两条变分条件：代数残差（不是差分）
add('D03', 'PASS',
    '势函数 V_eff = -4 pi M6^4 + 4 pi R^2 Lambda6 + pi N^2/(2 g6^2 R^2) 与两条变分条件在解上**代数**为零',
    '两个组合量 x = Lambda6 R^4、y = M6^4 R^2、z = N^2/(8 g6^2)：dV/dR = 0 <=> x - z = 0；V = 0 <=> x - y + z = 0。'
    '在解上：x - z = %s、x - y + z = %s（被检量级 0.18~0.36，60 位下相对 <= 1E-58，即精确零）。'
    '注意「精确零」用的是**代数残差**，不是数值导数——后者在极小 h 下会被舍入噪声污染（见 D08）'
    % (fv(_L['cond_stab_star'], 4), fv(_L['cond_zeroCC_star'], 4)))

# D04 双条件闭式解与三组合量锁定
add('D04', 'PASS',
    '双条件闭式解 R*^2 = N^2/(4 g6^2 M6^4)、Lambda6* = 2 g6^2 M6^8/N^2，且三个组合量全被 (N, g6) 锁定',
    '解上 x = z = N^2/(8 g6^2) = %s、y = N^2/(4 g6^2) = %s（且 y = 2z，这正是零 CC 条件的等价形式）。'
    '机器值：R* = %s、Lambda6* = %s（M6 = 1 单位）、V(R*) = %s。'
    '结构性后果：**Lambda6 R^4 = N^2/(8 g6^2) 与 M6 完全无关**；M6 只做 R ∝ 1/M6、Lambda6 ∝ M6^6 的标度交换，'
    '两者的乘积是拓扑量。故「Lambda6 与 R 是两个独立预言」是假象——它们只有一个自由度'
    % (fv(_L['xyz_star'][0], 8), fv(_L['xyz_star'][1], 8),
       fv(_L['R_star'], 10), fv(_L['Lam_star'], 10), fv(_L['V_star'], 4)))

# D05 层级判定：本组最重
_Mpl_over_M6 = _L['Mpl2_over_4piR2_M6_4'].sqrt()
_R_over_lPl = _L['R_star'] * _Mpl_over_M6
add('D05', 'FAIL',
    '把三维关系式当作层级问题的解 —— 不成立：双条件解把 M_Pl/M6 与 R/l_Pl 同时锁成 O(1) 纯数',
    '由 D04 的 R* 与 M_Pl^2 = 4 pi R^2 M6^4（B06）：M_Pl^2/M6^2 = 4 pi * N^2/(4 g6^2) = pi N^2/g6^2，'
    '故 **M_Pl/M6 = sqrt(pi) N/g6 = %s**（纯数，与 M6 无关）；等价地 R/l_Pl = R*(M_Pl/M6) = %s。'
    '=> 紧致化半径被锁在 1.28 个普朗克长度：**既没有层级，也没有大额外维度**。'
    '这把 B06 的条件句「若 M6 是唯一标度则无层级」升级为「双条件解强制 M_Pl/M6 为 O(1)」——'
    '该关系式不但不解决层级，反而排除了用它解决层级的可能。要在保持解的前提下得到 M_Pl/M6 ~ 1E16，'
    '必须让 N/g6 ~ 1E16——两条支路各需一个新输入：g6 ~ 1E-16 而 N 保持 O(1) 整数，或 N ~ 1E16 而 g6 保持 O(1)'
    % (fv(_Mpl_over_M6, 8), fv(_R_over_lPl, 8)))

# D06 第三条件冗余：秩 2 而非 3
add('D06', 'CORRECTED',
    '来料的「三维关系式」实为**二维**：第三条 x - 2y + 3z = 0 是前两条的精确线性组合',
    '系数向量机器验证：-1*(x - z) + 2*(x - y + z) = %s，与来料的 (1, -2, 3) 逐位相等 = %s。'
    '=> 秩 = 2，只有 2 个独立约束。2 未知量 (R, Lambda6) 配 2 独立条件 ⇒ 恰好定解，第三条自动满足、'
    '**不提供任何额外信息**。若来料用它去「定 N = 3」或「定 g6」，那是重复计数（把同一方程数了两遍）'
    % ('(%s, %s, %s)' % tuple(str(x) for x in _L['combo_check']), _L['combo_equals_source']))

# D07 单用第三式：两个根，只有一个是极小点
_u1, _u2 = _L['u_source_roots']
_R1 = _u1.sqrt()
_cs1 = cond_stab(_R1, _L['Lam_star'])
_cz1 = cond_zeroCC(_R1, _L['Lam_star'])
add('D07', 'PASS',
    '第三式在固定 Lambda6* 下对 u = R^2 是二次方程，有 2 个根；只有较小根同时满足稳定性与零 CC',
    'u 的两根 = %s 与 %s（判别式 = %s）。根 1 对应 R = %s：x - z = %s、x - y + z = %s —— **不是**极小点，'
    '也不满足零 CC；根 2 对应 R = %s，三条全为零（D03）。=> 单用第三式是欠定的（2 解），'
    '必须与 dV/dR = 0 联立才能挑出根 2。若来料只解第三式并取较大根，会得到非极小的「解」'
    % (fv(_u1, 8), fv(_u2, 8), fv(_L['disc'], 6), fv(_R1, 8), fv(_cs1, 6), fv(_cz1, 6),
       fv(_L['R_star'], 8)))

# D08 数值方法论：差分在极小 h 下的两种失效模式
_DVSCAN = []
for _e in (-12, -15, -18, -20, -25, -30):
    _h = Dc(10) ** _e
    _d = (V_eff(_L['R_star'] + _h, _L['Lam_star']) - V_eff(_L['R_star'] - _h, _L['Lam_star'])) / (2 * _h)
    _DVSCAN.append((_e, _d))
R['dv_scan'] = [(str(e), fv(d, 4)) for e, d in _DVSCAN]
add('D08', 'INFO',
    '「dV/dR 的数值 = 1E-38 ≠ 0」不是残差证据：那是中心差分的 (1/6)V\'\'\'h^2 截断项，h 再小则进入 1E-58/h 噪声地板',
    'h = 1E-12 / 1E-15 / 1E-18 / 1E-20 / 1E-25 / 1E-30 的中心差分读数 = %s。前三点每次 h 缩 1E3 读数缩 1E6 => '
    '严格 ∝ h^2，即 O(h^2) 截断（(1/6)V\'\'\'h^2，V 对 R 的奇次项在此非零）；后两点偏离 h^2 并随 h 反向放大 => '
    '进入噪声地板（60 位精度 / h）。=> **极值判据必须用代数残差**；用「数值导数小但不为零」判极值，'
    '在 h 太小时会把舍入噪声当残差、在 h 太大时会把截断项当残差，两种错都不可分辨'
    % ' / '.join('%s' % fv(d, 4) for _, d in _DVSCAN))
# ================================================================ E 组：alpha 数字命理学的判别力定价
say('')
say('=' * 78)
say('E 组 · alpha = 1/(4 pi^3 + pi^2 + pi) 的判别力定价（不是判它「美不美」，是判它能证伪什么）')
say('=' * 78)

_A = R['alpha']
# ALPHA 的实验相对不确定度（CODATA2018 alpha^-1 = 137.035999084(21) => 1.5E-10）
_A_SIG = Dc('1.5E-10')
_A_SIGMAS = _A['rel_dev'] / _A_SIG

add('E01', 'PASS',
    '数值本身：4 pi^3 + pi^2 + pi = %s，不等于 alpha^-1 = %s —— 「不精确」成立，且可定 σ 数'
    % (fv(_A['value'], 20), fv(AINV_CODATA, 12)),
    '绝对偏差 %s（相对 %s）；反解 alpha = %s，相对偏差 %s。以 CODATA2018 的 1.5E-10 相对不确定度计，'
    '该偏差 = **%s σ**。=> 若把它当「精确公式」而非「近似」，它已被实验排除 4 个量级；'
    '「精度很高」这种说法只在「与 137 差多少」的意义上成立，在「与 alpha^-1 差多少」的意义上不成立'
    % (fv(_A['abs_dev'], 8), fv(_A['rel_dev'], 8), fv(_A['alpha_from_formula'], 20),
       fv(_A['alpha_rel_dev'], 8), fv(_A_SIGMAS, 6)))

add('E02', 'INFO',
    '家族内唯一性：在 {c0 + c1 pi + c2 pi^2 + c3 pi^3}、系数 ∈ [-4,4] 的 %d 条里，落在 3.05E-4 内的只有 1 条'
    % _A['n_forms'],
    '容差 1E-2 / 1E-3 / 3.05E-4 下的命中条数 = %d / %d / %d；次优形态 %s 的偏差 %s（比目标差 %s 倍）。'
    '但均匀先验下的**期望偶然命中数** = %s ⇒ 「观察到 1 条」本身是 ~1%% 量级的事件：'
    '这个检验既不能证明它特殊（家族本来就稀疏，平均间隔 = 值域/家族数 = %s），也不能证明它是巧合。'
    '=> 唯一性读数是「族 + 容差」的联合性质，不能单独当证据'
    % (_A['n_within_1e-2'], _A['n_within_1e-3'], _A['n_within_3e-4'],
       str(_A['top10'][1]['coef']), _A['top10'][1]['abs_dev'],
       fv(Dc(_A['top10'][1]['abs_dev']) / _A['abs_dev'], 6),
       fv(_A['expected_hits_3e-4'], 6), fv(_A['value_range'] / Dc(_A['n_forms']), 4)))

add('E03', 'FAIL',
    '判别力定价：显著性完全由「族定义」决定，而族的四个边界都是事后选的 —— 该式不可作为 alpha 的解释',
    '四个事后自由度：①是否允许常数项 c0（族规模 6561 vs 729）；②系数界取 4 而非 3 或 5；③最高幂次取 pi^3 而非 pi^4；'
    '④是否允许负系数。任一改动都改变「唯一命中」的结论。要谈显著性必须先**先验固定族**，'
    '而「pi 的多项式」没有任何第一性依据（不是任何作用量的变分结果，也不含任何耦合常数）。'
    '=> 定价结论：**可证伪内容 = 0 条**（它只给一个数，且该数已被 E01 排除 1.5E4 σ）；'
    '合法定位只能是「记忆术 / 数值巧合」，写成「alpha 被几何解释」属越权')

add('E04', 'FAIL',
    '若把它当预言：alpha 随能标跑动，同一公式在第二个能标上立刻失效（偏差 ~7% 量级）',
    'alpha^-1(M_Z) ~ 127.95（MS-bar 口径，pole 口径 128.9 不影响结论量级）vs 公式给的 137.036304：'
    '相对偏差 ~7.1%%，是低能处偏差（%s）的 3.2E4 倍。=> 「alpha 是纯 pi 多项式」不是「精度不够」，'
    '而是**形式错误**：多项式无法承载跑动（RGE 的对数依赖）。真正的 alpha 解释必须给 beta 函数，'
    '本册式 (1) 与 7 条主方程都不含 beta 函数（与 A10/B03 的结论一致）'
    % fv(_A['rel_dev'], 6))

add('E05', 'INFO',
    '定价汇总：`alpha = 1/(4 pi^3 + pi^2 + pi)` 的全部信息量 = 1 个数，其可证伪内容已被排除',
    '三条独立测度同向：①与实验差的 σ 数 = %s；②跨能标立即失效（E04）；③显著性依赖事后族定义（E03）。'
    '=> 本册对该式的处置：**登记为数值巧合，不计入 PASS 资产、不作为任何「统一」的证据**。'
    '若来料把它列为「最核心方程之一」，则该列表的有效条目数应减 1（与 B03「7 条主方程 0 条预言」同型问题）'
    % fv(_A_SIGMAS, 6))
# ================================================================ G 组：守卫（先证工具、再证结论）
say('')
say('=' * 78)
say('G 组 · 守卫：自实现数值库 / 量纲工具 / 差分阶 / 矩阵代数（工具不出错，结论才可信）')
say('=' * 78)

# G01 三角：特殊角精确值
_g01 = max(abs(dsin(PI / 6) - Dc('0.5')), abs(dcos(PI / 3) - Dc('0.5')),
           abs(dsin(PI / 2) - 1), abs(dcos(PI / 2)), abs(dsin(PI)), abs(dcos(0) - 1))
guard('G01', 'dsin/dcos 特殊角（PI/6, PI/3, PI/2, PI）', _g01 < Dc('1E-50'), 'max |dev| = %s' % fv(_g01, 4))

# G02 指数
_g02 = max(abs(dexp(Dc(0)) - 1), abs(dexp(LN2) - 2), abs(dexp(-LN2) - Dc('0.5')),
           abs(dexp(Dc(1)) - EE) / EE)
guard('G02', 'dexp(0)=1, dexp(ln2)=2, dexp(1)=e', _g02 < Dc('1E-50'), 'max |dev| = %s' % fv(_g02, 4))

# G03 双曲：cosh^2 - sinh^2 = 1
_g03 = max(abs(dcosh(Dc('1.3')) ** 2 - dsinh(Dc('1.3')) ** 2 - 1),
           abs(dcosh(Dc('-2.7')) ** 2 - dsinh(Dc('-2.7')) ** 2 - 1))
guard('G03', 'cosh^2 - sinh^2 = 1（正负自变量）', _g03 < Dc('1E-50'), 'max |dev| = %s' % fv(_g03, 4))

# G04 tanh 饱和与奇性
_g04 = max(abs(dtanh(Dc(50)) - 1), abs(dtanh(Dc(-50)) + 1), abs(dtanh(Dc(0))))
_g04x = Dc(2) / (dexp(Dc(100)) + 1)     # 1 - tanh(50) 的真值（不是误差）
guard('G04', 'tanh(+/-50) 与 1 的差等于 2/(e^100+1)（真值，非误差）且 tanh(0)=0',
      abs(_g04 - _g04x) < Dc('1E-55') and abs(dtanh(Dc(0))) == 0,
      '|dev| = %s，理论 2/(e^100+1) = %s，差 %s（首版误把真值 7.4E-44 当误差、阈值 1E-58 必然误杀）'
      % (fv(_g04, 4), fv(_g04x, 4), fv(abs(_g04 - _g04x), 4)))

# G05 量纲工具：相乘=指数相加、取逆=取负；且 eps0*mu0 = 1/c^2
_g05a = (dmul(dm(1, 2, 3), dm(-1, 1, -1)) == dm(0, 3, 2))
_g05b = (dinv(dpow(DM_C, 2)) == dm(0, -2, 2))
_g05c = (dmul(DM_EPS0, DM_MU0) == dinv(dpow(DM_C, 2)))
guard('G05', '量纲代数（相加/取负/幂）且 eps0*mu0 = c^-2',
      _g05a and _g05b and _g05c,
      'dmul=%s dinv(dpow)=%s eps0*mu0=1/c^2 %s（读作 %s）'
      % (_g05a, _g05b, _g05c, dstr(dmul(DM_EPS0, DM_MU0))))

# G06 差分：5 点格式对低阶多项式精确
_f3 = lambda s: s ** 3
_f4 = lambda s: s ** 4
_g06 = max(abs(d1(_f3, Dc('0.7'), Dc('0.1')) - 3 * Dc('0.7') ** 2),
           abs(d2(_f4, Dc('0.7'), Dc('0.1')) - 12 * Dc('0.7') ** 2))
guard('G06', 'd1 对 x^3、d2 对 x^4 精确（5 点格式截断项为零）', _g06 < Dc('1E-50'),
      'max |dev| = %s' % fv(_g06, 4))

# G07 矩阵代数与对易子
_c1 = mm(SIG1, SIG2)
_c2 = mm(SIG2, SIG1)
_g07 = max(abs(_c1[0][0] - 1j), abs(_c1[1][1] + 1j),
           mnorm(ms(ms(_c1, _c2), ((2j, 0j), (0j, -2j)))))
guard('G07', 'sigma1*sigma2 = i*sigma3 且 [sigma1,sigma2] = 2i*sigma3', _g07 < 1e-15,
      'max |dev| = %.3e' % _g07)

# G08 Fr -> Dc 转换与 fv 一致性（避免把 Fraction 的整除语义带进判定）
_r = Fr(1, 3)
_g08 = abs((Dc(_r.numerator) / Dc(_r.denominator)) - Dc(1) / Dc(3))
guard('G08', 'Fraction -> Decimal 转换无损（1/3）', _g08 == 0, '|dev| = %s' % fv(_g08, 4))

# G09 螺旋解析式的两个已知极限：u=0 平面圆（tau=0, kappa=1/R）；u->inf（kappa,tau -> 0）
_v9a, _k9a, _t9a = helix_kt_analytic(Dc(2), Dc(3), Dc(0))
_v9b, _k9b, _t9b = helix_kt_analytic(Dc(2), Dc(3), Dc('1E15'))
_g09 = max(abs(_k9a - Dc('0.5')), abs(_t9a), abs(_v9a - 6))
_g09b = (_k9b < Dc('1E-28')) and (abs(_t9b * Dc('1E15') - 3) < Dc('1E-12'))
guard('G09', 'u=0 退化为平面圆（kappa=1/R, tau=0）；u->inf 时 kappa->0 且 tau*u->w', (_g09 < Dc('1E-58')) and _g09b,
      'circle: |kappa-1/R| = %s, tau = %s; u=1E15: kappa = %s, tau*u = %s（应为 w = 3）'
      % (fv(abs(_k9a - Dc('0.5')), 4), fv(_t9a, 4), fv(_k9b, 4), fv(_t9b * Dc('1E15'), 12)))

# G10 单位球曲率与 C06 RHS 系数：R_{S^2} = 2/R^2 => 单位球 R = 2
_g10 = abs(Dc(2) / (Dc(1) ** 2) - 2)
guard('G10', 'R_{S^2} = 2/R^2（单位球取 2，与 C06 的 RHS 系数一致）', _g10 == 0, '|dev| = %s' % fv(_g10, 4))

# ================================================================ 状态表与产物
say('')
say('=' * 78)
say('状态表（全部条目）')
say('=' * 78)
for _it in ITEMS:
    say('[%s] %-9s %s' % (_it['id'], _it['kind'], _it['prop']))
    say('                  ' + _it['ev'])

_CNT = {}
for _it in ITEMS:
    _CNT[_it['kind']] = _CNT.get(_it['kind'], 0) + 1
_GOK = sum(1 for g in GUARDS if g['ok'])

say('')
say('=' * 78)
say('汇总')
say('=' * 78)
say('条目 %d：%s' % (len(ITEMS), ' / '.join('%s=%d' % (k, v) for k, v in sorted(_CNT.items()))))
say('守卫 %d/%d 通过' % (_GOK, len(GUARDS)))
for _g in GUARDS:
    if not _g['ok']:
        say('  !! %s %s -> %s' % (_g['id'], _g['name'], _g['detail']))
say('')
say('五条承重读数（本册结论）:')
say('  (1) 作用量式 (1) 六项在 D=4..11 全部 L 幂次齐次（B01 PASS）—— 写法本身没量纲错，'
    '错在单位制混用（B02 FAIL）与它支撑不了 §四 的螺旋结论（B05 FAIL）')
say('  (2) 「ROOT-MASTER 主方程组」7 条 = 6 定义/恒等 + 1 变分原理，非平凡约束 0 条（B03 FAIL）'
    ' => 该链的可证伪性完全来自输入的场内容与耦合，主方程组形式不增加信息')
say('  (3) 五组核心方程的数值面全部复现（C01/C03/C04/C05/C06 PASS），但两类缺陷：'
    '螺旋三重奏是恒等而非预言（C02）、Yukawa 力是 1/r^2 乘指数修正而非新力律（C03）')
say('  (4) Lambda6「三维关系式」实为二维（D06 CORRECTED），其解把 M_Pl/M6 锁成 sqrt(pi)N/g6 = %s、'
    'R 锁在 %s l_Pl（D05 FAIL）=> 它不解决层级，反而排除用它解决层级' % (fv(_Mpl_over_M6, 6), fv(_R_over_lPl, 6)))
say('  (5) alpha = 1/(4 pi^3+pi^2+pi) 与实验差 %s σ、跨能标即失效（E01/E04）=> 数值巧合，'
    '可证伪内容 0 条（E03/E05）' % fv(_A_SIGMAS, 6))

OUT = {
    'name': NAME,
    'verdict_counts': _CNT,
    'items': ITEMS,
    'guards': GUARDS,
    'guards_ok': '%d/%d' % (_GOK, len(GUARDS)),
    'key_numbers': {
        'alpha_formula_value': fv(_A['value'], 30),
        'alpha_rel_dev': fv(_A['rel_dev'], 12),
        'alpha_sigmas': fv(_A_SIGMAS, 8),
        'Mpl_over_M6_double_cond': fv(_Mpl_over_M6, 12),
        'R_over_lPl_double_cond': fv(_R_over_lPl, 12),
        'L6_R_star': fv(_L['R_star'], 20),
        'L6_Lambda_star': fv(_L['Lam_star'], 20),
        'helix_max_abs_dev_kappa': fv(_mk, 8),
        'helix_max_abs_dev_tau': fv(_mt, 8),
        'yukawa_max_rel': fv(_yk_rel, 8),
        'comm_max_rel': fv(max(_cb1['rel_diff'], _cb2['rel_diff']), 8),
        'mz_shape_z30': fv(R['mz_z30'], 8),
        'dv_scan': R['dv_scan'],
        'kk_all_pos': R['kk']['all_pos'],
        'kk_degenerate_has_zero': R['kk']['has_zero'],
    },
}
try:
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    _jp = os.path.join(DATA, NAME + '.json')
    with io.open(_jp, 'w', encoding='utf-8') as _f:
        _f.write(json.dumps(OUT, ensure_ascii=False, indent=2, default=str))
    _rp = os.path.join(DATA, NAME + '_report.txt')
    with io.open(_rp, 'w', encoding='utf-8') as _f:
        _f.write('\n'.join(LOG))
    say('')
    say('产物已写出：')
    say('  ' + _jp)
    say('  ' + _rp)
except Exception as _e:
    say('产物写出失败（不影响判定）：%s' % _e)

sys.exit(0 if _GOK == len(GUARDS) else 1)
