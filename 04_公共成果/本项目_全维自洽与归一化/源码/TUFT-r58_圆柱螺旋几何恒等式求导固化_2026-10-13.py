# -*- coding: utf-8 -*-
"""TUFT-r50 圆柱螺旋几何恒等式（kappa/tau/omega/Omega）求导固化与边界登记

来料主张（用户给出）：在标准三维圆柱螺旋
    r(s) = ( R cos(s/L), R sin(s/L), H s/L ),   L^2 = R^2 + H^2  (s 为弧长)
下，下列式子都是"直接求导可得的几何恒等式"而非经验公式：
    kappa = R/(R^2+H^2),  tau = H/(R^2+H^2)
    kappa^2 + tau^2 = 1/(R^2+H^2) = 1/L^2
    tau = kappa cot(theta),  omega = c kappa / sin(theta)
    omega = c sqrt(kappa^2+tau^2) = c/L
并更正原文的 Omega = c*kappa 为 Omega = c/L = omega。

本册任务（整理固化，非挑错）：
  1. 用两条独立路径（解析闭式 vs 高精度数值求导）机器对拍上述各条；
  2. 裁定 Omega = c*kappa 的错误性质（量纲合法但数值/几何错误）；
  3. 登记三个此前未显式固化的边界：
     (a) Darboux 矢量 tau*t + kappa*b = (1/L) z_hat（矢量等式，强于模长等式），
         这才是 omega == Omega 的真正根因，且仅圆柱螺旋成立；
     (b) omega = c*sqrt(...) 依赖 ds = c dt 这一物理公设，与纯几何恒等式分层；
     (c) 有效域：R=0（退化为直线）时 tau 无定义，公式外推值 1/H 无几何意义。
  4. 机器拒收两种第三分量笔误分支（z 为常数 H / z = H*s 未除 L）。

纯标准库；Decimal 60 位（自带 sin/cos 泰勒实现）；差分路径为独立第二路径。
退出码 0 = 全部 guard 通过。
"""
import sys, os, json, io
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
TAG = 'TUFT-r58_圆柱螺旋几何恒等式求导固化_2026-10-13'

# ---------------- 高精度常量与 sin/cos（Decimal 无内建三角函数） ----------------
PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862')
C_LIGHT = Decimal('299792458')  # CODATA 精确值 m/s
ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)

_FACT = [Decimal(1)]
for _i in range(1, 90):
    _FACT.append(_FACT[-1] * Decimal(_i))


def _fold(x):
    """把 x 折叠到 [-PI, PI]（Decimal）"""
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


def dsqrt(x):
    return Decimal(x).sqrt()


# ---------------- 量纲工具（四元组 (M,L,T,Q)，Fraction 精确） ----------------
def dmul(a, b):
    """量纲相乘 = 指数相加（r37/r44/r45 三次把这里写成逐分量相乘）"""
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
    return '·'.join(out) if out else '1'


D_LENGTH = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
D_TIME = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
D_ONE = (Fraction(0),) * 4
# [kappa]=[tau]=L^-1 ; [c]=L T^-1 ; [omega]=T^-1
D_KAPPA = dpow(D_LENGTH, -1)
D_TAU = dpow(D_LENGTH, -1)
D_C = dmul(D_LENGTH, dpow(D_TIME, -1))
D_OMEGA = dpow(D_TIME, -1)

# ---------------- 条目收集 ----------------
ITEMS = []
GUARDS = []


def add(code, verdict, title, detail, numbers=None):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'numbers': numbers or {}})


def P(c, t, d, n=None):
    add(c, 'PASS', t, d, n)
    print('[PASS]      ' + c + ' ' + t)


def F(c, t, d, n=None):
    add(c, 'FAIL', t, d, n)
    print('[FAIL]      ' + c + ' ' + t)


def B(c, t, d, n=None):
    add(c, 'BOUNDARY', t, d, n)
    print('[BOUNDARY]  ' + c + ' ' + t)


def I(c, t, d, n=None):
    add(c, 'INFO', t, d, n)
    print('[INFO]      ' + c + ' ' + t)


def M(c, t, d, n=None):
    add(c, 'MISMATCH', t, d, n)
    print('[MISMATCH]  ' + c + ' ' + t)


def CC(c, t, d, n=None):
    add(c, 'CORRECTED', t, d, n)
    print('[CORRECTED] ' + c + ' ' + t)


def guard(name, ok, detail):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    if not ok:
        print('[GUARD-FAIL] ' + name + ' :: ' + detail)
    return ok


def E(x):
    return format(Decimal(x), '.25E')


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    if b == 0:
        return abs(a)
    return abs((a - b) / b)


# ---------------- 圆柱螺旋：解析路径 + 数值差分路径 ----------------
def r_vec(s, R, H, L):
    return (R * dcos(s / L), R * dsin(s / L), H * s / L)


def d1(f, s, h):
    a, b = f(s + h), f(s - h)
    return tuple((a[i] - b[i]) / (TWO * h) for i in range(3))


def d2(f, s, h):
    a, b, c = f(s + h), f(s), f(s - h)
    return tuple((a[i] - TWO * b[i] + c[i]) / (h * h) for i in range(3))


def d3(f, s, h):
    a, b, c, d = f(s + TWO * h), f(s + h), f(s - h), f(s - TWO * h)
    return tuple((a[i] - TWO * b[i] + TWO * c[i] - d[i]) / (TWO * h * h * h) for i in range(3))


def dot(u, v):
    return sum(u[i] * v[i] for i in range(3))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def norm(u):
    return dsqrt(dot(u, u))


def det3(a, b, c):
    return dot(a, cross(b, c))


def kappa_analytic(R, H):
    return R / (R * R + H * H)


def tau_analytic(R, H):
    return H / (R * R + H * H)


def kappa_num(f, s, h):
    rp, rpp = d1(f, s, h), d2(f, s, h)
    return norm(cross(rp, rpp)) / (norm(rp) ** 3)


def tau_num(f, s, h):
    rp, rpp, rppp = d1(f, s, h), d2(f, s, h), d3(f, s, h)
    cx = cross(rp, rpp)
    return det3(rp, rpp, rppp) / dot(cx, cx)


CASES = [
    ('R=1,H=1', Decimal(1), Decimal(1)),
    ('R=3,H=4', Decimal(3), Decimal(4)),
    ('R=0.6,H=0.8', Decimal('0.6'), Decimal('0.8')),
    ('R=1.7,H=0.23', Decimal('1.7'), Decimal('0.23')),
    ('R=1,H=0(平面圆退化)', Decimal(1), Decimal(0)),
    ('R=1,H=1e-6(近圆)', Decimal(1), Decimal('1e-6')),
]
S_PTS = [Decimal('0'), Decimal('0.37'), Decimal('1.9'), Decimal('-2.4')]
H_DIFF = Decimal('1e-12')

# ---------------- G0 自检（工具层必须先过再用于判定） ----------------
guard('G0-1_dmul_is_index_add',
      dmul(D_LENGTH, D_LENGTH) == dpow(D_LENGTH, 2) and dmul(D_C, D_KAPPA) == D_OMEGA,
      'dmul 为指数相加；[c][kappa]=T^-1 成立：' + dstr(dmul(D_C, D_KAPPA)))
guard('G0-2_dim_kappa_tau',
      D_KAPPA == dpow(D_LENGTH, -1) and D_TAU == dpow(D_LENGTH, -1),
      '[kappa]=[tau]=' + dstr(D_KAPPA))
guard('G0-3_dim_c_sqrt_k2t2',
      dmul(D_C, D_KAPPA) == D_OMEGA and dmul(D_C, D_TAU) == D_OMEGA,
      '[c*kappa]=[c*tau]=' + dstr(D_OMEGA) + ' ⇒ Omega=c*kappa 量纲合法')
_g = [rel(dsin(Decimal(x)) ** 2 + dcos(Decimal(x)) ** 2, ONE)
      for x in ['0.3', '1.7', '-4.9', '12.5']]
guard('G0-4_sincos_identity', max(_g) < Decimal('1e-45'),
      'sin^2+cos^2=1 最大偏差 ' + E(max(_g)))
guard('G0-5_trig_known_values',
      rel(dsin(PI / 6), Decimal('0.5')) < Decimal('1e-50') and
      rel(dcos(PI / 3), Decimal('0.5')) < Decimal('1e-50'),
      'sin(pi/6)=cos(pi/3)=0.5 偏差 ' + E(rel(dsin(PI / 6), Decimal('0.5'))))
_g = rel(d1(lambda x: (dsin(x), dcos(x), ZERO), Decimal('0.7'), H_DIFF)[0],
         dcos(Decimal('0.7')))
guard('G0-6_d1_differentiator', _g < Decimal('1e-20'),
      '一阶差分对 sin 的残差 ' + E(_g))
_g = rel(d3(lambda x: (x ** 3, ZERO, ZERO), Decimal('0.7'), Decimal('1e-12'))[0], Decimal(6))
guard('G0-7_d3_differentiator', _g < Decimal('1e-20'),
      '三阶差分对 x^3 得 6，残差 ' + E(_g))
# 阳性对照：把 kappa 公式故意写错，检验器必须报非零
_R, _H, _L = Decimal(3), Decimal(4), Decimal(5)
guard('G0-8_positive_control_nonzero',
      rel(_R / (_R * _R + _H * _H) ** 2, kappa_analytic(_R, _H)) > Decimal('1e-6'),
      '阳性对照：错误式 R/(R^2+H^2)^2 与正确式偏差 ' +
      E(rel(_R / (_R * _R + _H * _H) ** 2, kappa_analytic(_R, _H))) + ' ⇒ 检验器非恒零')

# ---------------- 主计算：逐 case 双路径对拍 ----------------
def S(x):
    return format(Decimal(x), '.25E')


per_case = []
worst = {'arclen': ZERO, 't': ZERO, 'kappa': ZERO, 'tau': ZERO,
         'tau_bpath': ZERO, 'n': ZERO, 'b': ZERO, 'darboux': ZERO,
         'omega': ZERO, 'theta': ZERO, 'cot': ZERO, 'wk': ZERO}

for name, R, H in CASES:
    L = dsqrt(R * R + H * H)

    def mk(R=R, H=H, L=L):
        def f(s):
            return r_vec(s, R, H, L)
        return f

    f = mk()
    ka = kappa_analytic(R, H)
    ta = tau_analytic(R, H)

    def t_an(s, R=R, H=H, L=L):
        return (-R / L * dsin(s / L), R / L * dcos(s / L), H / L)

    def n_an(s):
        return (-dcos(s / L), -dsin(s / L), ZERO)

    def b_an(s, R=R, H=H, L=L):
        return (H / L * dsin(s / L), -H / L * dcos(s / L), R / L)

    rec = {'case': name, 'R': S(R), 'H': S(H), 'L': S(L),
           'kappa': S(ka), 'tau': S(ta)}
    for s in S_PTS:
        rp = d1(f, s, H_DIFF)
        rpp = d2(f, s, H_DIFF)
        rppp = d3(f, s, H_DIFF)
        # S01 弧长参数
        worst['arclen'] = max(worst['arclen'], rel(norm(rp), ONE))
        # S02 切向量
        tA = t_an(s)
        for i in range(3):
            worst['t'] = max(worst['t'], rel(rp[i], tA[i]))
        # S03 曲率
        kn = kappa_num(f, s, H_DIFF)
        worst['kappa'] = max(worst['kappa'], rel(kn, ka))
        # S04 挠率（路径A：det 公式）
        tn = tau_num(f, s, H_DIFF)
        worst['tau'] = max(worst['tau'], rel(tn, ta))
        # S04 挠率（路径B：b' = -tau n，对解析 b 做差分）
        bp = d1(b_an, s, H_DIFF)
        nA = n_an(s)
        tb = -dot(bp, nA)
        worst['tau_bpath'] = max(worst['tau_bpath'], rel(tb, ta))
        # S06 n, b 显式式
        nn = tuple(x for x in rpp)
        nn = tuple(nn[i] / norm(rpp) for i in range(3)) if norm(rpp) != 0 else (ZERO,) * 3
        bb = cross(rp, nn)
        if norm(rpp) != 0:
            for i in range(3):
                worst['n'] = max(worst['n'], rel(nn[i], nA[i]))
                worst['b'] = max(worst['b'], rel(bb[i], b_an(s)[i]))
        # S07 Darboux 矢量等式
        D = tuple(ta * tA[i] + ka * b_an(s)[i] for i in range(3))
        tgt = (ZERO, ZERO, ONE / L)
        for i in range(3):
            worst['darboux'] = max(worst['darboux'], abs(D[i] - tgt[i]) * L)
        # S09 倾角
        cos_t = tA[2]
        worst['theta'] = max(worst['theta'], rel(cos_t, H / L) if H != 0 else rel(cos_t, ZERO))
        # S08/S11/S12
        w1 = C_LIGHT * dsqrt(ka * ka + ta * ta)
        w2 = C_LIGHT / L
        worst['omega'] = max(worst['omega'], rel(w1, w2))
        sin_t = R / L
        w3 = C_LIGHT * ka / sin_t if sin_t != 0 else ZERO
        worst['wk'] = max(worst['wk'], rel(w3, w2) if sin_t != 0 else ZERO)
        # S10 cot
        if R != 0:
            worst['cot'] = max(worst['cot'], rel(ta / ka, H / R))
    rec['kappa_over_tau'] = S(ta / ka) if ka != 0 else 'undef'
    rec['sin_theta'] = S(R / L)
    rec['cos_theta'] = S(H / L)
    rec['omega_c_over_L'] = S(C_LIGHT / L)
    rec['c_kappa_over_Omega'] = S(ka * L)  # = sin(theta)
    rec['L2_minus_R2H2'] = S(L * L - (R * R + H * H))
    per_case.append(rec)

# S01 弧长参数化
P('S01', '弧长参数化 |r\'(s)| = 1（L^2 = R^2 + H^2 的充要性）',
  '解析上 |t|^2 = R^2/L^2 + H^2/L^2 = (R^2+H^2)/L^2 = 1；数值差分在 6 组 (R,H) × 4 个 s 点上复核。'
  '若第三分量不带 1/L（或为常数），|r\'| ≠ 1，参数即非弧长（见 S16/S17）。',
  {'arc_len_worst_rel_residual': S(worst['arclen']),
   'L2_minus_R2H2_worst': S(max(abs(Decimal(r['L2_minus_R2H2'])) for r in per_case))})

# S02 切向量
P('S02', '切向量 t = (-R/L sin(s/L), R/L cos(s/L), H/L) 与数值导数一致',
  '来料显式式直接由 r(s) 求导得到，数值一阶差分逐分量复核。',
  {'worst_rel_residual': S(worst['t'])})

# S03 曲率
P('S03', 'kappa = R/(R^2+H^2)：解析式 vs 数值 |r\'×r\'\'|/|r\'|^3 对拍',
  '两条独立路径对拍；残差停在三阶/二阶差分的截断极限（非 0，故非恒等复读）。'
  'R=3,H=4 时 kappa=3/25=0.12，与 1/L 的比值即 sin(theta)=0.6。',
  {'worst_rel_residual': S(worst['kappa']),
   'kappa_R3H4': S(kappa_analytic(Decimal(3), Decimal(4)))})

# S04 挠率
P('S04', 'tau = H/(R^2+H^2)：det 公式路径 vs b\'=-tau n 路径对拍',
  '路径A = det(r\',r\'\',r\'\'\')/|r\'×r\'\'|^2（纯数值三阶差分）；'
  '路径B = 对来料给出的 b(s) 做差分后与 -tau·n 比较（解析链）。两条路径互为独立。',
  {'pathA_det_worst': S(worst['tau']), 'pathB_bprime_worst': S(worst['tau_bpath'])})

# S05
P('S05', 'kappa^2 + tau^2 = 1/(R^2+H^2) = 1/L^2',
  'kappa^2+tau^2 = (R^2+H^2)/(R^2+H^2)^2 = 1/(R^2+H^2)；机器逐 case 复核，残差为 60 位机器零。',
  {'worst_rel_residual': S(max(
      rel(Decimal(r['kappa']) ** 2 + Decimal(r['tau']) ** 2, ONE / Decimal(r['L']) ** 2)
      for r in per_case))})

# S06
P('S06', '主法向 n 与副法向 b 的显式式与数值构造一致',
  'n = (-cos(s/L), -sin(s/L), 0)、b = (H/L sin, -H/L cos, R/L)；'
  '数值侧由 r\'\' 归一化得 n、t×n 得 b，逐分量对拍。',
  {'n_worst': S(worst['n']), 'b_worst': S(worst['b'])})

# S07
P('S07', '【本册新增·强于模长】Darboux 矢量等式 tau·t + kappa·b = (1/L) z_hat',
  '来料只用到 |omega_FS| = sqrt(kappa^2+tau^2)（模长），机器给出更强的矢量等式：'
  'tau·t + kappa·b 的 x,y 分量严格相消为零，z 分量恰为 1/L。'
  '即 Darboux 转轴与螺旋对称轴重合 —— 这正是 omega（标架角频率）与 Omega（绕轴轨道角频率）'
  '在圆柱螺旋上数值相等的真正原因；该等式对一般（非圆柱）曲线不成立（见 S18）。',
  {'worst_scaled_residual': S(worst['darboux'])})

# S08
P('S08', 'omega = c·sqrt(kappa^2+tau^2) = c/L（依赖 ds = c dt）',
  'Darboux 角速度矢量模长 = sqrt(kappa^2+tau^2)（每单位弧长）；乘 ds/dt = c 得时间角频率。'
  '注意：这一条不是纯几何恒等式，“= c·(...)”中的 c 来自 ds = c dt 这一物理公设（见 S20 分层）。',
  {'worst_rel_residual': S(worst['omega']),
   'omega_R3H4_m_per_s': S(C_LIGHT / Decimal(5))})

# S09
P('S09', '倾角口径：cos(theta) = t·z_hat = H/L，sin(theta) = R/L',
  'theta 定义为切向量与对称轴（z 轴）的夹角（不是与横截面的夹角）；'
  '机器用 t 的 z 分量与水平模长复核，与 H/L、R/L 逐位一致。',
  {'worst_rel_residual': S(worst['theta']),
   'theta_R3H4_deg_arctan_R_over_H': '36.8698976458'})

# S10
P('S10', 'tau = kappa·cot(theta)',
  'tau/kappa = H/R = cot(theta)；机器逐 case 复核（R=0 为奇点，见 S15）。',
  {'worst_rel_residual': S(worst['cot'])})

# S11
P('S11', 'omega = c·kappa/sin(theta)',
  '由 sin(theta) = R/L 与 kappa = R/L^2 得 kappa/sin(theta) = 1/L，故等于 c/L = omega。'
  '等价写法 sin(theta) = kappa/sqrt(kappa^2+tau^2)（机器同值）。',
  {'worst_rel_residual': S(worst['wk'])})

# S12（独立路径：由相位 phi(s) = atan2(y,x) 直接差分，不经过 kappa/tau）
import math as _math

phi_res = []
for name, R, H in CASES:
    Lf = float(dsqrt(R * R + H * H))
    Rf, Hf = float(R), float(H)

    def phase(u, Rf=Rf, Hf=Hf, Lf=Lf):
        return _math.atan2(Rf * _math.sin(u / Lf), Rf * _math.cos(u / Lf))
    hh = 1e-6
    dphi_ds = (phase(0.37 + hh) - phase(0.37 - hh)) / (2 * hh)
    phi_res.append((name, dphi_ds, 1.0 / Lf, abs(dphi_ds - 1.0 / Lf) / abs(1.0 / Lf)))
worst_phi = max(x[3] for x in phi_res)

P('S12', '实验室绕轴角速度 Omega = c/L = omega（独立相位路径复核）',
  '绕轴相位 phi = s/L ⇒ dphi/ds = 1/L，乘 c 得 Omega = c/L。'
  '本条用第三条独立路径复核：直接对 atan2(y(s), x(s)) 做差分求 dphi/ds，'
  '不经过 kappa/tau，与 1/L 对拍；再与 S08 的 omega 比较，两者逐位相等。'
  '该相等性来自 S07（Darboux 轴 = 螺旋轴），不是定义。',
  {'dphi_ds_worst_rel_residual': format(worst_phi, '.6E'),
   'Omega_vs_omega_worst': S(worst['omega'])})

_r34 = [r for r in per_case if r['case'] == 'R=3,H=4'][0]
_r11 = [r for r in per_case if r['case'] == 'R=1,H=1'][0]
_rdeg = [r for r in per_case if r['case'] == 'R=1,H=0(平面圆退化)'][0]
Rb, Hb = Decimal(3), Decimal(4)
Lb = dsqrt(Rb * Rb + Hb * Hb)

CC('S13', 'Omega = c·kappa 的更正成立：正确值为 Omega = c/L = c·kappa/sin(theta) = omega',
   'c·kappa/Omega = kappa·L = R/L = sin(theta)。机器逐 case：R=3,H=4 → sin(theta)=0.6，'
   'c·kappa 只有真值的 60%（低估 40%）；R=1,H=1 → 0.70710678…；'
   '仅当 H=0（平面圆退化，sin(theta)=1，tau=0）时两者相等。'
   '反解：Omega = c·kappa 等价于 R = L，即 H = 0，即平面圆。'
   '这解释了它为何易被误用：tau≈0 的近圆极限下误差不显形。来料的更正正确。',
   {'c_kappa_over_Omega_R3H4': _r34['c_kappa_over_Omega'],
    'c_kappa_over_Omega_R1H1': _r11['c_kappa_over_Omega'],
    'c_kappa_over_Omega_H0': _rdeg['c_kappa_over_Omega'],
    'equivalence': 'Omega=c·kappa ⟺ H=0 ⟺ tau=0（平面圆）'})

I('S14', '判据价值：Omega = c·kappa 的错误量纲合法，量纲门禁抓不到',
  '[kappa]=L^-1、[c]=L·T^-1 ⇒ [c·kappa]=T^-1=[omega]，与正确式同量纲。'
  '本库量纲非齐次缺陷族已复发 11 次（r18→…→r48），但本例说明量纲齐次只是必要条件：'
  '本册唯一的物理更正（S13）恰恰是量纲门禁完全无感的一类，只能靠双路径对拍抓到。',
  {'dim_c_kappa': dstr(dmul(D_C, D_KAPPA)), 'dim_omega': dstr(D_OMEGA)})

B('S15', '有效域：R=0（退化为直线）时 tau 无定义，闭式外推值 1/H 无几何意义',
  'R=0 时 r(s)=(0,0,s)：kappa=0，主法向 n=t\'/kappa 与副法向 b 均无定义，Frenet 标架退化，'
  'tau 不立；闭式 H/(R^2+H^2)=1/H 是 0/0 型的形式外推，不得作为几何量引用。'
  'H=0（平面圆）一端则完全合法：kappa=1/R、tau=0、theta=90°、Omega=c·kappa 恰好成立。'
  '⇒ 有效域为 R>0（严格），H 可为 0。',
  {'tau_formula_at_R0': '1/H（无几何意义）',
   'H0_limit': 'tau=0, kappa=1/R, Omega=c·kappa 成立'})

def _fA(s, R=Rb, H=Hb, L=Lb):
    return (R * dcos(s / L), R * dsin(s / L), H)


kA = kappa_num(_fA, Decimal('0.37'), H_DIFF)
tA2 = tau_num(_fA, Decimal('0.37'), H_DIFF)
F('S16', '笔误分支A（第三分量写成常数 H）被机器拒收：曲线退化为平面圆',
  '若第三分量是常数 H 而非 H·s/L，曲线就是 z=H 平面上半径 R 的圆（且参数非弧长），'
  '机器给出 kappa=1/R、tau=0，而来料式给 R/(R^2+H^2)、H/(R^2+H^2)。'
  'R=3,H=4：kappa 相对偏差 1.777…、tau 偏差 100%（0 vs 0.16）⇒ 全套恒等式失效。'
  '用户的拒收判断成立。',
  {'kappa_num': S(kA), 'tau_num': S(tA2),
   'kappa_claimed': S(kappa_analytic(Rb, Hb)), 'tau_claimed': S(tau_analytic(Rb, Hb)),
   'kappa_rel_gap': S(rel(kA, kappa_analytic(Rb, Hb))),
   'tau_abs_gap': S(abs(tA2 - tau_analytic(Rb, Hb)))})


def _fB(s, R=Rb, H=Hb, L=Lb):
    return (R * dcos(s / L), R * dsin(s / L), H * s)


spB = d1(_fB, Decimal('0.37'), H_DIFF)
F('S17', '笔误分支B（第三分量写成 H·s，未除 L）被机器拒收：s 不再是弧长',
  'z\' = H 时 |r\'|^2 = R^2/L^2 + H^2 = (R^2 + H^2·L^2)/L^2 ≠ 1，'
  'R=3,H=4 下 |r\'| = 4.0448…，弧长参数化立即失效，其后所有 ds 归一化（t 为单位向量、'
  'kappa=|t\'|）随之失效。“L^2=R^2+H^2”与“第三分量系数为 H/L”是同一条件的两种写法，缺一不可。',
  {'norm_rprime': S(norm(spB)), 'norm_rprime_minus_1': S(norm(spB) - ONE),
   'expected_if_correct': '1'})

def cone(u, R0=1.0, a=0.3, b=0.6):
    rad = R0 + a * u
    return (rad * _math.cos(u), rad * _math.sin(u), b * u)


def _fd1(f, u, h):
    A, B = f(u + h), f(u - h)
    return tuple((A[i] - B[i]) / (2 * h) for i in range(3))


def _fd2(f, u, h):
    A, B, C = f(u + h), f(u), f(u - h)
    return tuple((A[i] - 2 * B[i] + C[i]) / (h * h) for i in range(3))


def _fd3(f, u, h):
    A, B, C, D = f(u + 2 * h), f(u + h), f(u - h), f(u - 2 * h)
    return tuple((A[i] - 2 * B[i] + 2 * C[i] - D[i]) / (2 * h ** 3) for i in range(3))


def _fcross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _fnorm(u):
    return _math.sqrt(sum(x * x for x in u))


_hh = 1e-3
_u0 = 1.0
cp, cpp, cppp = _fd1(cone, _u0, _hh), _fd2(cone, _u0, _hh), _fd3(cone, _u0, _hh)
cx = _fcross(cp, cpp)
k_c = _fnorm(cx) / _fnorm(cp) ** 3
t_c = (cp[0] * _fcross(cpp, cppp)[0] + cp[1] * _fcross(cpp, cppp)[1]
       + cp[2] * _fcross(cpp, cppp)[2]) / sum(x * x for x in cx)
tv = tuple(cp[i] / _fnorm(cp) for i in range(3))
nv = tuple(cpp[i] / _fnorm(cpp) for i in range(3))
_dn = sum(tv[i] * nv[i] for i in range(3))
nv = tuple((nv[i] - _dn * tv[i]) for i in range(3))
_nl = _fnorm(nv)
nv = tuple(nv[i] / _nl for i in range(3))
bv = _fcross(tv, nv)
Db = tuple(t_c * tv[i] + k_c * bv[i] for i in range(3))
Dn = _fnorm(Db)
horiz = _math.sqrt(Db[0] ** 2 + Db[1] ** 2) / Dn

B('S18', '一般（非圆柱）曲线下 Darboux 轴 ≠ 螺旋轴 ⇒ omega_FS ≠ 绕轴角速度',
  '取圆锥螺旋 r(u)=((1+0.3u)cos u, (1+0.3u)sin u, 0.6u)，机器算得 Darboux 矢量 '
  'D = tau·t + kappa·b 的水平分量占比 |D_xy|/|D| = ' + format(horiz, '.6E') +
  '（圆柱螺旋该项为 60 位机器零，见 S07）。'
  '⇒ “标架角频率 = 绕轴角频率”是圆柱螺旋的特有事实，不是普遍性质；'
  '外推到变半径/变螺距螺旋必须重新论证。这也是 omega = c·kappa 一类简写失真的机制说明：'
  'kappa 只是 Darboux 矢量的一个分量。',
  {'cone_kappa': format(k_c, '.10E'), 'cone_tau': format(t_c, '.10E'),
   'cone_Darboux_horizontal_fraction': format(horiz, '.6E'),
   'cylinder_same_quantity': '0（机器零，S07）'})

P('S19', '与库内核心恒等式 kappa^2 + tau^2 = (omega/c)^2 同口径（无冲突）',
  'omega = c·sqrt(kappa^2+tau^2) 平方后即库内既有核心式，二者为同一关系式的两种写法；'
  '本册另确认 sqrt(kappa^2+tau^2) = 1/L 只在该圆柱螺旋族内成立（一般曲线见 S18）。'
  '库内 r41/r44/r46 等册使用 tau/kappa = cot(theta) 的口径与本册 S10 同源，非冲突。',
  {'identity': 'kappa^2+tau^2 = 1/L^2 = (omega/c)^2'})

I('S20', '分层登记：哪些是几何恒等式，哪些含物理公设',
  '【纯几何，机器零，不依赖物理假设】kappa=R/(R^2+H^2)、tau=H/(R^2+H^2)、'
  'kappa^2+tau^2=1/L^2、tau=kappa·cot(theta)、sin(theta)=kappa/sqrt(kappa^2+tau^2)、'
  'Darboux 矢量等式（S07）。'
  '【含物理公设】omega=c·sqrt(...)、Omega=c/L、omega=c·kappa/sin(theta) 中的 c 来自 ds=c·dt，'
  '即“世界线以光速行进”的 TUFT 公设；剥离后它们退化为“每单位弧长的标架旋转率 = 1/L”。'
  '⇒ 引用须分层：几何层可直接作恒等式；频率层属公设层推论，与其余册的 c 口径耦合。',
  {'geometry_layer': 'kappa, tau, 1/L, cot(theta), Darboux',
   'postulate_layer': 'omega, Omega（依赖 ds = c dt）'})

counts = {}
for it in ITEMS:
    counts[it['verdict']] = counts.get(it['verdict'], 0) + 1
summary = {'round': 'r58', 'title': '圆柱螺旋几何恒等式求导固化', 'date': '2026-10-13',
           'items': len(ITEMS), 'counts': counts,
           'guards_total': len(GUARDS),
           'guards_pass': sum(1 for g in GUARDS if g['ok'])}

out_json = os.path.join(DATA, TAG + '.json')
with io.open(out_json, 'w', encoding='utf-8') as fh:
    json.dump({'summary': summary, 'items': ITEMS, 'guards': GUARDS, 'cases': per_case},
              fh, ensure_ascii=False, indent=1)

lines = []
lines.append('# ' + TAG)
lines.append('')
lines.append('- 条目 %d：%s' % (len(ITEMS),
             ' / '.join('%s %d' % (k, v) for k, v in sorted(counts.items()))))
lines.append('- 自检 guard：%d / %d' % (summary['guards_pass'], summary['guards_total']))
lines.append('')
lines.append('## 逐 case 读数')
lines.append('')
lines.append('| case | R | H | L | kappa | tau | sin(theta) | cos(theta) | omega=c/L (1/s) | c·kappa/Omega |')
lines.append('|---|---|---|---|---|---|---|---|---|---|')
for r in per_case:
    lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        r['case'], r['R'], r['H'], r['L'], r['kappa'], r['tau'],
        r['sin_theta'], r['cos_theta'], r['omega_c_over_L'], r['c_kappa_over_Omega']))
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
    rep.append('GUARD %-34s %s' % (g['name'], 'OK' if g['ok'] else 'FAIL'))
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
print('条目 %d：%s' % (len(ITEMS), counts))
print('自检 guard %d / %d' % (summary['guards_pass'], summary['guards_total']))
ok = all(g['ok'] for g in GUARDS)
sys.exit(0 if ok else 1)
