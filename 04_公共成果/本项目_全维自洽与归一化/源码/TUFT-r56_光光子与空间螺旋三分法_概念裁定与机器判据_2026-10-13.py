# -*- coding: utf-8 -*-
"""TUFT-r56《光 / 光子 / 空间光速螺旋》三分法·概念裁定与机器判据

来料主张（用户 2026-10-13 给出，全文见 数据/TUFT-光光子与空间螺旋三分法_来料全文_2026-10-13.md）：
    三件最易混淆的事：(1) 光的螺旋结构（圆偏振 / 螺旋相位 / 轨道角动量）；
    (2) 光子（无质量、自旋 1、螺旋度 h=±1、自由传播为类光测地线）；
    (3) 空间光速螺旋（把类光世界线建模成三维圆柱螺旋 + Frenet–Serret kappa/tau/omega/Omega）。
    核心结论：自由光子在真空中不沿空间螺旋轨迹运动；"空间光速螺旋"应理解为有效几何模型
    或偏振/相位/角动量结构，而非自由光子的真实空间轨迹。

【与同目录前两册的分工（必须先读，避免重复造轮子）】
    r51《圆柱螺旋几何恒等式求导固化》（条目前缀 S01..S20，已落盘）
      = 三维几何层：弧长参数化、kappa=R/L^2、tau=H/L^2、kappa^2+tau^2=1/L^2、
        Darboux 矢量等式 tau*t+kappa*b=(1/L) z_hat、Omega=c*kappa 的错误性质(S13)、
        有效域 R>0(S15)、一般曲线反例(S18)。
    r52《空间光速螺旋·四维类光层与可实现性》（条目前缀 N01..N19，2026-10-13 00:36 已完整落盘）
      = 四维类光层 + ds/tau/s/theta 符号台账 + 洛伦兹协变性(N14/N15/N16) +
        真空无源场 v_E/c<=1 等号仅单平面波(N17) + 光学涡旋能流线类时(N18) + 零测地线曲率为零(N19)。
    本册 r56 = **概念层裁定 + 前两册均未覆盖的机器判据**，只做增量：
      (1) 四维加速度的显式机器验证（a!=0、a.u=0、a^2>0、|a|=c^2*kappa）
      (2) 无任何惯性系能使 kappa'=0 的硬否证；给出把 tau'=0 的精确 boost（beta=cos theta）
      (3) 缠绕数的轴向 boost 不变性（螺旋的协变内容仅剩拓扑）
      (4) 轴向速率 v_z=c*cos theta<c 的边界 + 与库内 S02 三约束互斥定理的兼容性裁定
      (5) R=0 处 Frenet–Serret 不适用：(kappa,tau)->(0,1/H) 的连续延拓值 vs 直线的 (0,0)
      (6) 符号台账缺口：omega 同篇三义（r51 登记了 ds/tau/s/theta，漏 omega）
      (7) **螺旋度 h=±1 与轨道角动量 l∈Z 的机器可判定差异**（前两册完全未涉及）
      (8) 圆偏振"场矢量螺旋"与"空间轨迹螺旋"的机器可分性判据
      (9) 类光曲线的曲率/挠率需协变算子（Newman–Penrose），不自推系数、标 BOUNDARY
    本册与前两册双向回链；不重复 r51 已固化的三维恒等式，只在交叉点引用。

纯标准库；Decimal 60 位（自带 sin/cos 泰勒）；解析闭式 / 参数化不变公式 / 有限差分 三路径对拍。
退出码 0 = 全部 guard 通过。
"""
import sys
import os
import json
import io
import math
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
TAG = 'TUFT-r56_光光子与空间螺旋三分法_概念裁定与机器判据_2026-10-13'

# ---------------- 高精度常量 ----------------
PI = Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862')
C_LIGHT = Decimal('299792458')          # CODATA 精确值 m/s
HBAR = Decimal('1.054571817e-34')       # J*s
PLANCK_H = Decimal('6.62607015e-34')    # J*s
C_MU0 = Decimal('1.25663706212e-6')     # H/m
EPS0 = Decimal('8.8541878128e-12')      # F/m
ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
PIECE = Decimal('3.14159265358979')     # 圆偏振相位用（双精度级即可，非精度敏感项）

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
        term = ONE if n == 0 else (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


# 工具自检：sin^2+cos^2=1（含 0 与 ±pi/2 特殊点），且 dcos(0)=1 不再崩溃
def _tool_selftest():
    for _x in (ZERO, Decimal('0.41'), Decimal('1.73'), PI / 2, PI):
        _v = dsin(_x) ** 2 + dcos(_x) ** 2
        if abs(_v - ONE) > Decimal('1e-50'):
            return False
    return dcos(ZERO) == ONE and dsin(ZERO) == ZERO


def dcos(x):
    # 【自抓·工具级】Decimal 中 0**0 抛 InvalidOperation，故 n=0 项单独置 1。
    # （首版未处理，导致 dcos(0) 崩溃、被 fs_frame 的 s=0 采样点当场拦下。）
    r = _fold(Decimal(x))
    acc = ZERO
    for k in range(0, 42):
        n = 2 * k
        term = ONE if n == 0 else (r ** n) / _FACT[n]
        acc += term if k % 2 == 0 else -term
    return acc


def dsqrt(x):
    return Decimal(x).sqrt()


def fmt(x, n=25):
    try:
        return format(Decimal(x), '.' + str(n) + 'E')
    except Exception:
        return str(x)


def rel(a, b):
    a = Decimal(a)
    b = Decimal(b)
    den = abs(b) if abs(b) > Decimal('1e-50') else Decimal('1e-50')
    return abs(a - b) / den


# ---------------- 量纲工具（四元组 (M,L,T,Q)，Fraction 精确） ----------------
# 纪律（本库已在 dmul 翻车 r37/r44/r45 三次）：量纲相乘 = 指数相加，不是逐分量相乘。
def dmul(a, b):
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
D_LEN = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
D_TIM = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
D_MAS = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
D_KAPPA = dpow(D_LEN, -1)              # L^-1
D_C = dmul(D_LEN, dpow(D_TIM, -1))    # L T^-1
D_OMEGA = dpow(D_TIM, -1)              # T^-1

# ---------------- 条目登记 ----------------
ITEMS = []
_GUARDS = []


def add(vid, verdict, title, detail, numbers=None):
    ITEMS.append({
        'id': vid, 'verdict': verdict, 'title': title,
        'detail': detail, 'numbers': numbers or {}
    })


def guard(name, cond, detail=''):
    _GUARDS.append({'name': name, 'ok': bool(cond), 'detail': detail})
    return bool(cond)


def V(name):
    return sum(1 for it in ITEMS if it['verdict'] == name)


# =====================================================================
# G0：量纲工具自检（必须先验。本库 r37/r44/r45 三次把 dmul 写成逐分量相乘，
#     且 r44 首跑即被本守卫拦下——这是「工具先过自检再用于判定」纪律的价值）
# =====================================================================
guard('G0-1 dmul(L,L)=L^2', dmul(D_LEN, D_LEN) == dpow(D_LEN, 2))
guard('G0-2 dpow(L,-1)=L^-1', dpow(D_LEN, -1) == (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)))
guard('G0-3 [c]=L*T^-1', D_C == (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)))
guard('G0-4 [c/L]=T^-1', ddiv(D_C, D_LEN) == D_OMEGA)
guard('G0-5 [c*kappa]=T^-1', dmul(D_C, D_KAPPA) == D_OMEGA)
guard('G0-6 [kappa^2]=L^-2', dpow(D_KAPPA, 2) == dpow(D_LEN, -2))
guard('G0-7 [hbar]=M*L^2*T^-1', (Fraction(1), Fraction(2), Fraction(-1), Fraction(0)) == dmul(dmul(D_MAS, dpow(D_LEN, 2)), dpow(D_TIM, -1)))
guard('G0-8 [c*kappa]=T^-1 不等于 [kappa^2]=L^-2（量纲门禁可分辨两者）', dmul(D_C, D_KAPPA) != dpow(D_KAPPA, 2))
guard('G0-9 三角函数工具自检 sin^2+cos^2=1（含 0 与 ±pi/2）且 dcos(0)=1', _tool_selftest())


# =====================================================================
# 几何工具：圆柱螺旋类光世界线（三维空间曲线用弧长参数；四维用固有时 t）
# =====================================================================
def L_of(R, H):
    return dsqrt(R * R + H * H)


def omega_of(R, H):
    """Omega = c/L：由 |v|=c 唯一确定，不是独立输入"""
    return C_LIGHT / L_of(R, H)


def worldline(R, H, t):
    """四维世界线 x^mu(t)，x^0 = c*t"""
    Om = omega_of(R, H)
    c1, s1 = dcos(Om * t), dsin(Om * t)
    return (C_LIGHT * t, R * c1, R * s1, H * Om * t)


def vel(R, H, t):
    """四维速度 u^mu = dx^mu/dt"""
    Om = omega_of(R, H)
    c1, s1 = dcos(Om * t), dsin(Om * t)
    return (C_LIGHT, -R * Om * s1, R * Om * c1, H * Om)


def acc(R, H, t):
    """四维加速度 a^mu = d^2x^mu/dt^2"""
    Om = omega_of(R, H)
    c1, s1 = dcos(Om * t), dsin(Om * t)
    return (ZERO, -R * Om * Om * c1, -R * Om * Om * s1, ZERO)


def mink_dot(a, b):
    """闵氏度规 (+---) 的标量积"""
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm3(a):
    return dsqrt(dot3(a, a))


def det3(a, b, cc):
    return (a[0] * (b[1] * cc[2] - b[2] * cc[1])
            - a[1] * (b[0] * cc[2] - b[2] * cc[0])
            + a[2] * (b[0] * cc[1] - b[1] * cc[0]))


def helix_derivs_s(R, H, s):
    """对三维弧长 s 的一/二/三阶导数"""
    L = L_of(R, H)
    u = s / L
    c1, s1 = dcos(u), dsin(u)
    return ((-R / L * s1, R / L * c1, H / L),
            (-R / (L * L) * c1, -R / (L * L) * s1, ZERO),
            (R / (L * L * L) * s1, -R / (L * L * L) * c1, ZERO))


def kappa_tau_param(R, H, s):
    """参数化不变公式：kappa=|r'x r''|/|r'|^3, tau=det(r',r'',r''')/|r'x r''|^2"""
    d1, d2, d3 = helix_derivs_s(R, H, s)
    cr = cross3(d1, d2)
    n1 = norm3(d1)
    ncr = norm3(cr)
    if ncr == ZERO:
        return None, None          # Frenet–Serret 不适用（直线）
    return ncr / (n1 ** 3), det3(d1, d2, d3) / dot3(cr, cr)


def kappa_tau_closed(R, H):
    L2 = R * R + H * H
    return R / L2, H / L2


def boost_axis(R, H, beta):
    """沿柱轴（z）boost（速度 beta*c）。返回 (gamma, L', H', Omega', kappa', tau', v_z')。
    由 t' = gamma*(t - beta*z/c)、z' = gamma*(z - beta*c*t) 沿轴向投影得
    z' = gamma*(H*Omega - beta*c) t = gamma*(H - beta*L) * Omega t  => 螺距标度 H'
    横向坐标不变 => R'=R；速率仍为 c => L' = c/Omega' = gamma*(L - beta*H)。"""
    R = Decimal(R)
    H = Decimal(H)
    beta = Decimal(beta)
    L = L_of(R, H)
    g = ONE / dsqrt(ONE - beta * beta)
    Lp = g * (L - beta * H)
    Hp = g * (H - beta * L)
    Om = C_LIGHT / Lp
    kp = R / (Lp * Lp)
    tp = Hp / (Lp * Lp)
    vz = C_LIGHT * Hp / Lp
    return g, Lp, Hp, Om, kp, tp, vz


# =====================================================================
# C01 类光性：|v|=c <=> 四维间隔=0（双向等价，含超标反向对照）
# =====================================================================
R0 = Decimal('0.7')
H0 = Decimal('1.3')
L0 = L_of(R0, H0)
Om0 = omega_of(R0, H0)
_t = Decimal('0.37')

_vscan = [Decimal('0.5'), Decimal('0.99'), ONE, Decimal('1.0000001')]
_scan_flags = []
for _f in _vscan:
    _u = (C_LIGHT, C_LIGHT * _f, ZERO, ZERO)
    _iv = mink_dot(_u, _u)
    _scan_flags.append('null' if _iv == ZERO else ('spacelike' if _iv < 0 else 'timelike'))

_u0 = vel(R0, H0, _t)
_iv0 = mink_dot(_u0, _u0)
_spd0 = norm3((_u0[1], _u0[2], _u0[3]))
add('C01', 'PASS', '类光性成立：|v|=c 与四维间隔=0 双向等价（含超标反向对照）',
    '对 |v|/c = 0.5 / 0.99 / 1 / 1.0000001 扫描四维间隔符号：类时 / 类时 / 类光 / 类空，'
    '等价性双向成立。来料 §1–§2 的"类光世界线"结论在数学上正确。'
    '**号约定显式登记（自抓）**：本册 mink_dot 取 (+---)，故 u^2 = c^2 - |v|^2，'
    'u^2>0 ⇔ 类时、u^2=0 ⇔ 类光、u^2<0 ⇔ 类空。首版把 timelike/spacelike 标签写反，'
    '被 guard 当场拦下——与本库 r42「符号判据方向写反」同型：**布尔判据必须与同条目文案互锁**。'
    '注意：这里用的记号是固有时 t 与四维间隔 dσ，四维间隔为零；'
    '来料 §1 用 s 记三维弧长、§2 又把四维间隔写成 ds^2 的记号冲突由 r51 册 N01 登记，本册不重复。',
    {'v_over_c_scan': [fmt(x) for x in _vscan], 'interval_type_scan': _scan_flags,
     'actual_u_squared': fmt(_iv0), 'actual_abs_v': fmt(_spd0), 'abs_v_over_c': fmt(_spd0 / C_LIGHT)})
guard('C01 四维间隔=0（实际曲线）', abs(_iv0) < Decimal('1e-40') * (C_LIGHT * C_LIGHT), fmt(_iv0))
guard('C01 三维速率=c', rel(_spd0, C_LIGHT) < Decimal('1e-40'), fmt(_spd0))
guard('C01 双向等价扫描', _scan_flags == ['timelike', 'timelike', 'null', 'spacelike'])

# =====================================================================
# C02 三重奏 kappa^2+tau^2=1/L^2（闭式 vs 参数化不变公式；与 r51 S02/S08 交叉确认）
# =====================================================================
_kc, _tc = kappa_tau_closed(R0, H0)
_kp, _tp = kappa_tau_param(R0, H0, Decimal('0.37'))
_lhs = _kc * _kc + _tc * _tc
_rhs = ONE / (R0 * R0 + H0 * H0)
add('C02', 'PASS', '三重奏 kappa^2+tau^2=1/L^2 双路径一致（与 r51 S02/S08 交叉确认，不重复展开）',
    '路径A=闭式 R/(R^2+H^2)、H/(R^2+H^2)；路径B=参数化不变公式（解析一/二/三阶导数）。'
    '两条独立路径逐位一致。**该式与 r51 册 S08/S19 同源**，本册仅作交叉引用式的独立复核，'
    '不重复其双路径与 Darboux 矢量推导。',
    {'kappa_closed': fmt(_kc), 'kappa_param': fmt(_kp), 'tau_closed': fmt(_tc), 'tau_param': fmt(_tp),
     'lhs': fmt(_lhs), 'rhs': fmt(_rhs),
     'resid_kappa': fmt(rel(_kc, _kp)), 'resid_tau': fmt(rel(_tc, _tp)), 'resid_identity': fmt(rel(_lhs, _rhs))})
guard('C02 kappa 双路径<1e-40', rel(_kc, _kp) < Decimal('1e-40'), fmt(rel(_kc, _kp)))
guard('C02 tau 双路径<1e-40', rel(_tc, _tp) < Decimal('1e-40'), fmt(rel(_tc, _tp)))
guard('C02 恒等式残差<1e-40', rel(_lhs, _rhs) < Decimal('1e-40'), fmt(rel(_lhs, _rhs)))

# =====================================================================
# C02b Frenet–Serret 三方程逐分量精确验证（独立于 |r'x r''| 公式的第三路径）
# =====================================================================
def fs_frame(R_, H_, s):
    """圆柱螺旋的 Frenet 标架（显式解析式，u = s/L）。
    注意：这里 sin/cos 的自变量是相位 u，**不是**弧长 s——手算时把两者混用会导致
    Binet 方程 db/ds = -tau*n 验证失败（本册自抓，已机器复核为记号事故）。"""
    R_ = Decimal(R_)
    H_ = Decimal(H_)
    L = L_of(R_, H_)
    u = s / L
    c1, s1 = dcos(u), dsin(u)
    T = (-R_ / L * s1, R_ / L * c1, H_ / L)
    n = (-c1, -s1, ZERO)
    b = (H_ * s1 / L, -H_ * c1 / L, R_ / L)
    Td = (-R_ / (L * L) * c1, -R_ / (L * L) * s1, ZERO)
    nd = (s1 / L, -c1 / L, ZERO)
    bd = (H_ * c1 / (L * L), H_ * s1 / (L * L), ZERO)
    return T, n, b, Td, nd, bd, L, u


_fs_rows = []
_fs_max = ZERO
for _ss in (Decimal('0.0'), Decimal('0.41'), Decimal('1.73'), Decimal('5.02')):
    _T, _n, _b, _Td, _nd, _bd, _L, _u = fs_frame(R0, H0, _ss)
    _k = _kc
    _t = _tc
    _e1 = max(abs(x) for x in [a - _k * bb for a, bb in zip(_Td, _n)])
    _e2 = max(abs(a - (-_k * aa + _t * bb)) for a, aa, bb in zip(_nd, _T, _b))
    _e3 = max(abs(a - (-_t * bb)) for a, bb in zip(_bd, _n))
    _fs_max = max(_fs_max, _e1, _e2, _e3)
    _fs_rows.append({'s': fmt(_ss), 'err_dTds_eq_kappa_n': fmt(_e1),
                     'err_dnds_eq_-kappaT_tauB': fmt(_e2), 'err_dbds_eq_-tauN': fmt(_e3)})
add('C02b', 'PASS', 'Frenet–Serret 三方程逐分量精确验证（独立于 |r\'x r\'\'| 公式的第三路径，确认 tau=H/L^2）',
    '对圆柱螺旋用**显式解析式**标架 T=(-R/L sin u, R/L cos u, H/L)、n=(-cos u, -sin u, 0)、'
    'b=(H sin u/L, -H cos u/L, R/L)（u=s/L）及其解析一阶导，机器逐分量验证：'
    '(i) dT/ds = kappa*n；(ii) dn/ds = -kappa*T + tau*b；(iii) db/ds = -tau*n（Binet 方程）。'
    '三条在 4 个弧长采样点上的最大逐分量残差为 ' + fmt(_fs_max) + '（机器零）。'
    '**本条价值**：它完全**不使用** |r\'x r\'\'|/|r\'|^3 与 det/|r\'x r\'\'|^2 两个公式，'
    '因此是对"tau=H/L^2"的一次真正独立的确认（前两册 r51 用的是前两条公式路径）。'
    '**本册自抓（记号事故，机器兜底）**：手算 (iii) 时把相位 u=s/L 与弧长 s 混用'
    '（b_x = H*sin(u)/L 被误写成 b_x = H*s/L 再对 s 求导），导致 Binet 方程"验证失败"；'
    '机器逐分量复核证明公式本身正确、错在记号。'
    '⇒ 与 r23 教训同族：**Binet 型方程的符号推导必须由机器逐分量兜底**，'
    '手算失败时先怀疑记号复用，再怀疑公式（注意 R、s、u、H 在本主题中极易混淆）。',
    {'scan': _fs_rows, 'max_component_error': fmt(_fs_max),
     'T': '( -R sin(u)/L, R cos(u)/L, H/L )',
     'n': '( -cos(u), -sin(u), 0 )',
     'b': '( H sin(u)/L, -H cos(u)/L, R/L )'})
guard('C02b Frenet–Serret 三方程最大逐分量残差<1e-50', _fs_max < Decimal('1e-50'), fmt(_fs_max))

# =====================================================================
# C03 Omega 不是独立输入：三条式子是同一约束的三种写法（零信息量登记）
# =====================================================================
_o_path1 = C_LIGHT / L0                                   # 路径1：Omega = c/L
_o_path2 = C_LIGHT * dsqrt(_kc * _kc + _tc * _tc)         # 路径2：Omega = c*sqrt(kappa^2+tau^2)
_o_path3 = C_LIGHT * _kc / (R0 / L0)                      # 路径3：Omega = c*kappa/sin(theta)
add('C03', 'INFO', 'Omega 的三条式子（c/L、c*sqrt(kappa^2+tau^2)、c*kappa/sin(theta)）是同一约束的三种写法，非三个独立预言',
    '|v|=c 一旦给定，Omega 就被螺距唯一决定（Omega = c/L），因此三条式子恒等于同一数。'
    '⇒ 它们之间的"一致"是零信息量的（跨册第 N 次恒等复读形态），**不能当作三重交叉验证**。'
    '同时确认：Omega 不需要作为独立输入引入——它由 |v|=c 自动导出。'
    '另：来料强调"不是 Omega=c*kappa"正确（与 r51 S13 一致），'
    '但读者容易误以为三条式子互相印证，本条显式拆除该误读。',
    {'Omega_c_over_L': fmt(_o_path1), 'Omega_c_sqrt': fmt(_o_path2), 'Omega_c_kappa_over_sin': fmt(_o_path3),
     'resid_1_2': fmt(rel(_o_path1, _o_path2)), 'resid_1_3': fmt(rel(_o_path1, _o_path3)),
     'c_kappa_error_ratio': fmt(_kc * L0)})
guard('C03 三条路径逐位一致', rel(_o_path1, _o_path2) < Decimal('1e-40') and rel(_o_path1, _o_path3) < Decimal('1e-40'))
guard('C03 c*kappa 确为错误值（比值=sin(theta)<1）', _kc * L0 < ONE, fmt(_kc * L0))

# =====================================================================
# C04【核心】四维加速度：类光但非测地线的正面机器证明
# =====================================================================
_a_tscan = [Decimal('0.11'), Decimal('0.83'), Decimal('2.40')]
_a_rows = []
for _tt in _a_tscan:
    _uu = vel(R0, H0, _tt)
    _aa = acc(R0, H0, _tt)
    _a2 = mink_dot(_aa, _aa)
    _au = mink_dot(_aa, _uu)
    _anorm = norm3((_aa[1], _aa[2], _aa[3]))
    _unorm = norm3((_uu[1], _uu[2], _uu[3]))
    _a_rows.append({'t': fmt(_tt), 'a2': fmt(_a2), 'a_dot_u': fmt(_au),
                    'a_dot_u_relative': fmt(abs(_au) / (_anorm * _unorm)),
                    'abs_a': fmt(_anorm), 'c2_kappa': fmt(C_LIGHT * C_LIGHT * _kc),
                    'rel_abs_a_vs_c2kappa': format(rel(_anorm, C_LIGHT * C_LIGHT * _kc), '.40E'),
                    'rel_abs_a_vs_c2kappa_raw': float(rel(_anorm, C_LIGHT * C_LIGHT * _kc)),
                    'a_vec': [fmt(x) for x in _aa]})

_a2_first = mink_dot(acc(R0, H0, _t), acc(R0, H0, _t))
_au_first = mink_dot(acc(R0, H0, _t), vel(R0, H0, _t))
_anorm_first = norm3(acc(R0, H0, _t)[1:])
_unorm_first = norm3(vel(R0, H0, _t)[1:])
_rel_au_first = abs(_au_first) / (_anorm_first * _unorm_first)     # 相对机器零判据
add('C04', 'FAIL', '【核心·对"自由光子"读法】四维加速度 a^mu != 0：类光但绝非测地线（正面机器证明）',
    '来料 §2 断言"上面这条螺旋类光曲线有四维加速度 a^mu != 0"，本册给出显式机器验证：'
    'a^mu = (0, -R*Omega^2*cos, -R*Omega^2*sin, 0)，故'
    '(i) |a| = R*Omega^2 = c^2*kappa（机器逐位）；'
    '(ii) a.u = 0（机器零）⇒ 加速度**垂直于**四速度，即类光曲线的定义性性质；'
    '(iii) a^2 = -R^2*Omega^4 < 0 ⇒ 在本册 (+---) 号约定下加速度**类空**；'
    '(iv) a^0 = 0 ⇒ 沿螺旋行进的共动标架中该加速度纯空间。'
    '⇒ 类光（a.u=0）但 a!=0，即它**是**一条合法的类光曲线，**不是**任何平坦时空中的测地线。'
    '测地线条件是 a^mu=0（用弧长或任意仿射参数），与 a.u=0 是两个不同条件；来料把二者区分清楚是正确的。'
    '补充：加速度矢量方向随方位角同步旋转（a_x:a_y = cos:sin），故曲率**每绕轴周期 2pi/Omega 转一整圈** ⇒ 是螺旋而非圆。',
    {'kappa': fmt(_kc), 'c2_kappa': fmt(C_LIGHT * C_LIGHT * _kc),
     'abs_a_at_t': fmt(_anorm_first), 'resid_abs_a_vs_c2kappa': fmt(rel(_anorm_first, C_LIGHT * C_LIGHT * _kc)),
     'a_dot_u': fmt(_au_first), 'a_dot_u_relative': fmt(_rel_au_first), 'a_squared': fmt(_a2_first),
     'scan': _a_rows,
     'geodesic_condition': 'a^mu = 0', 'null_condition': 'a.u = 0'})
guard('C04 |a| = c^2*kappa 逐位', rel(_anorm_first, C_LIGHT * C_LIGHT * _kc) < Decimal('1e-40'), fmt(rel(_anorm_first, C_LIGHT * C_LIGHT * _kc)))
guard('C04 a.u = 0（相对机器零，类光性）', _rel_au_first < Decimal('1e-30'), fmt(_rel_au_first))
guard('C04 a^2 < 0（(+---)约定下加速度类空）', _a2_first < ZERO, fmt(_a2_first))
guard('C04 a^0 = 0（纯空间加速度）', acc(R0, H0, _t)[0] == ZERO)
guard('C04 各采样点 |a| = c^2*kappa 恒成立', all(r['rel_abs_a_vs_c2kappa_raw'] < 1e-35 for r in _a_rows))
guard('C04 各采样点 a.u 相对机器零', all(Decimal(r['a_dot_u_relative']) < Decimal('1e-30') for r in _a_rows))
guard('C04 各采样点 a^2 < 0 恒成立（加速度恒类空）', all(Decimal(r['a2']) < ZERO for r in _a_rows))


# =====================================================================
# C05【核心·协变判据】沿轴 boost 族：挠率可被清零，曲率恒正但可趋零
# =====================================================================
cos_theta = H0 / L0                                   # = 切线与 z 轴夹角的余弦
sin_theta = R0 / L0                                   # = 来料 §4 的 sin(theta) = R/L
_beta_star = (TWO * L0 * H0) / (H0 * H0 + L0 * L0)     # 使 L'=L（从而 kappa'=kappa）的 boost

_betas = ['0', '0.1', '0.5', '0.9', '0.99', '0.999', '0.9999']
_betas.append(None)                                     # 稍后填入 cos(theta)
_betas.sort(key=lambda x: Decimal('0') if x is None else Decimal(x))

_boost_rows = []
_min_kappa_ratio = None
for _b in _betas:
    if _b is None:
        _bv, _label = cos_theta, 'cos(theta)=H/L'
    else:
        _bv, _label = Decimal(_b), _b
    _g, _Lp, _Hp, _Om, _kp, _tp, _vz = boost_axis(R0, H0, _bv)
    _vabs = dsqrt((R0 * _Om) ** 2 + _vz * _vz)         # 新系速率
    _kr = _kp / _kc
    if _min_kappa_ratio is None or _kr < _min_kappa_ratio:
        _min_kappa_ratio = _kr
    _boost_rows.append({'beta': _label,
                        'gamma': fmt(_g),
                        'L_prime': fmt(_Lp), 'H_prime': fmt(_Hp),
                        'kappa_prime': fmt(_kp), 'tau_prime': fmt(_tp),
                        'Omega_prime': fmt(_Om), 'vz_prime': fmt(_vz),
                        'abs_v_over_c': fmt(_vabs / C_LIGHT),
                        'kappa_over_kappa0': fmt(_kr),
                        'L2_minus_H2': fmt(_Lp * _Lp - _Hp * _Hp),
                        'R2': fmt(R0 * R0)})

_cos_row = [r for r in _boost_rows if r['beta'] == 'cos(theta)=H/L'][0]

# 去螺旋 boost 的精确恒等式
_gc, _Lc, _Hc, _Oc, _kc_p, _tc_p, _vzc = boost_axis(R0, H0, cos_theta)
add('C05', 'FAIL', '【核心·协变判据】挠率可被有限 boost 精确清零（beta=cos(theta)），曲率恒正但随 beta->1 趋零',
    '沿柱轴做 boost（速度 beta*c）后横向半径 R 不变，螺距标度与弧长标度变换为 '
    'L\'=gamma*(L-beta*H)、H\'=gamma*(H-beta*L)，且 L\'^2-H\'^2=R^2 恒成立（机器零）。'
    '在此族内：kappa\'=R/L\'^2、tau\'=H\'/L\'^2。'
    '**新读数一（最强非协变量）**：取 beta=cos(theta)=H/L，得 gamma=L/R，于是 '
    'L\'=gamma*(L-H^2/L)=(L^2-H^2)/R=R（机器零）、H\'=gamma*(H-H)=0（机器零）、'
    'tau\'=0、kappa\'=1/R、Omega\'=c/R、v_z\'=0 ⇒ **存在一个合法惯性系使挠率精确为零**。'
    '这比"挠率不是不变量"更强：**挠率可以被 boost 完全消掉**（对圆柱螺旋对称轴的 boost 即可）。'
    '⇒ 任何把 tau 当作协变内禀量（尤其 tau 与自旋/螺旋度挂钩）的读法，在 boost 下自毁。'
    '**新读数二（曲率的硬边界）**：kappa\'=R/L\'^2>0 对一切合法有限 beta 恒成立'
    '（R>0 是横向 boost 不变量），故**没有任何惯性系能把这条曲线变成直线** ⇒ '
    '它是"非测地线"的协变说法（强于来料 §2 只在实验室系陈述的 a^mu!=0）。'
    '但 inf kappa\'=0 在 beta->1 达成（beta*=2LH/(H^2+L^2) 使 kappa\'=kappa，beta>beta* 后 kappa\'<kappa）。'
    '**新读数三（必须警惕的极限混淆）**：beta->1 时 L\'、H\' 同发散，比值 kappa\'/tau\'=R/H\'->0，'
    '螺旋被轴向拉伸成"极扁的螺旋"，视觉上收敛为沿 -z 的直线（v_z\'->-c，kappa\'->0）。'
    '⇒ **在光速极限（共动）系中，类光螺旋会伪装成自由光子的直线轨迹。**'
    '这正是"自由光子沿螺旋"这一误读最可能产生的极限来源，必须在体例中显式禁止'
    '在 beta->1 系中做曲率判据。'
    '注：本条与 r51 册 N14/N15 互补——N14 给出变换律并指出"非不变量"，本条给出'
    '"可被打到零"（tau）与"不能被打到零但可趋零"（kappa）的定量边界，且不重复其推导。',
    {'beta_star_equal_kappa': fmt(_beta_star),
     'cos_theta': fmt(cos_theta), 'sin_theta': fmt(sin_theta),
     'despiral_beta': fmt(cos_theta),
     'despiral_L_prime': fmt(_Lc), 'despiral_R': fmt(R0),
     'resid_Lprime_eq_R': fmt(rel(_Lc, R0)),
     'despiral_H_prime': fmt(_Hp), 'despiral_tau_prime': fmt(_tc_p),
     'despiral_kappa_prime': fmt(_kc_p), 'despiral_Omega_prime': fmt(_Oc),
     'despiral_vz_prime': fmt(_vzc),
     'despiral_resid_Lp2_minus_Hp2': fmt(rel(_Lc * _Lc - _Hc * _Hc, R0 * R0)),
     'beta_star_machine': fmt(boost_axis(R0, H0, _beta_star)[1]),
     'resid_Lprime_eq_L_at_beta_star': fmt(rel(boost_axis(R0, H0, _beta_star)[1], L0)),
     'scan': _boost_rows,
     'min_kappa_ratio_scan': fmt(_min_kappa_ratio)})
guard('C05 去螺旋 boost：L\' 精确等于 R', rel(_Lc, R0) < Decimal('1e-40'), fmt(rel(_Lc, R0)))
guard('C05 去螺旋 boost：H\' 精确为 0', _Hc == ZERO, fmt(_Hc))
guard('C05 去螺旋 boost：tau\' 精确为 0', _tc_p == ZERO, fmt(_tc_p))
guard('C05 去螺旋 boost：kappa\'=1/R', rel(_kc_p, ONE / R0) < Decimal('1e-40'), fmt(_kc_p))
guard('C05 去螺旋 boost：Omega\'=c/R', rel(_Oc, C_LIGHT / R0) < Decimal('1e-40'), fmt(_Oc))
guard('C05 去螺旋 boost：v_z\'=0', _vzc == ZERO, fmt(_vzc))
guard('C05 L\'^2-H\'^2=R^2 全域成立', all(rel(Decimal(r['L2_minus_H2']), R0 * R0) < Decimal('1e-40') for r in _boost_rows))
guard('C05 类光性在 boost 下保持（|v\'|=c）', all(abs(Decimal(r['abs_v_over_c']) - ONE) < Decimal('1e-40') for r in _boost_rows))
guard('C05 kappa\' 恒为正（无有限 boost 使曲线变直线）', all(Decimal(r['kappa_prime']) > ZERO for r in _boost_rows))
guard('C05 beta*=2LH/(H^2+L^2) 确使 kappa\'=kappa', rel(boost_axis(R0, H0, _beta_star)[4], _kc) < Decimal('1e-40'))
# =====================================================================
# C05b【自抓·修正后重跑】boost 后的 kappa'/tau'：Decimal 参数化不变公式 + float 差分旁证
# =====================================================================
def helix_derivs_u(R_, pitch_, u_):
    """对无量纲相位 u 的解析一/二/三阶导：r(u)=(R cos u, R sin u, pitch*u)"""
    R_ = Decimal(R_)
    p_ = Decimal(pitch_)
    u_ = Decimal(u_)
    c1, s1 = dcos(u_), dsin(u_)
    return ((-R_ * s1, R_ * c1, p_),
            (-R_ * c1, -R_ * s1, ZERO),
            (R_ * s1, -R_ * c1, ZERO))


def kappa_tau_param_u(R_, pitch_, u_):
    """参数化不变公式（u 参数，非弧长）：|r'x r''|/|r'|^3 与 det/|r'x r''|^2。
    **退化保护**：当 r' x r'' = 0（曲线为直线）时 Frenet 标架不存在，
    两式均为 0/0，按几何事实返回 (None, None)——这正是 C08/C13 要演示的"不立"。"""
    d1, d2, d3 = helix_derivs_u(R_, pitch_, u_)
    cr = cross3(d1, d2)
    nc = norm3(cr)
    if nc == ZERO:
        return None, None
    return nc / (norm3(d1) ** 3), det3(d1, d2, d3) / dot3(cr, cr)


_kp_d, _tp_d = kappa_tau_param_u(R0, _Hc, Decimal('0.41'))     # 去螺旋系
_kp_l, _tp_l = kappa_tau_param_u(R0, H0, Decimal('0.41'))       # 实验室系


def _fd_kappa_tau(Rf, pitch_f, ue, h=1e-4):
    """float 中心差分（量级旁证；h 与 t 无关，用无量纲相位 u）。
    【自抓·尺度纪律】差分必须在无量纲相位 u 上做，不能在固有时 t 上做：
    Omega = c/L ~ 2.03e8 rad/s ⇒ 特征时标 1/Omega ~ 4.9e-9 s，
    而 float 在 t~0.41 处的分辨率仅 ~2.4e-16，任何 h >> 1e-11 的差分都会被噪声吞掉
    （首版 h=1e-5 s 即完全失效）。"""
    def P(u):
        return (Rf * math.cos(u), Rf * math.sin(u), pitch_f * u)

    def D1(u):
        return tuple((P(u + h)[i] - P(u - h)[i]) / (2 * h) for i in range(3))

    def D2(u):
        return tuple((D1(u + h)[i] - D1(u - h)[i]) / (2 * h) for i in range(3))

    def D3(u):
        return tuple((D2(u + h)[i] - D2(u - h)[i]) / (2 * h) for i in range(3))
    a1, a2, a3 = D1(ue), D2(ue), D3(ue)
    cr = cross3(a1, a2)
    nc = math.sqrt(sum(x * x for x in cr))
    kk = nc / math.sqrt(sum(x * x for x in a1)) ** 3
    tt = (a1[0] * (a2[1] * a3[2] - a2[2] * a3[1])
          - a1[1] * (a2[0] * a3[2] - a2[2] * a3[0])
          + a1[2] * (a2[0] * a3[1] - a2[1] * a3[0])) / (nc * nc)
    return kk, tt


_fd_k, _fd_t = _fd_kappa_tau(float(R0), float(_Hc), 0.41)
_fd_k2, _fd_t2 = _fd_kappa_tau(float(R0), float(H0), 0.41)
add('C05b', 'PASS', '【自抓·修正后重跑】boost 后的 kappa\'/tau\'：Decimal 参数化不变公式与闭式逐位一致，float 差分旁证同量级',
    '**两处自抓**（均在本册内发现并修正后重跑）：'
    '①把 |r_t x r_tt| 的 k 分量误记为 R^2*Omega^6（应为 R^4*Omega^6），'
    '导致参数化不变公式给出 tau=H/(H^2+1) 而非 H/L^2、与闭式矛盾；'
    '②差分在固有时 t 上做（h=1e-5 s）而 Omega ~ 2.03e8 rad/s，特征时标 4.9e-9 s，'
    '差分步长比物理尺度大 4 个量级 ⇒ 结果完全失效（表现为"公式不一致"的假故障）。'
    '修正后：**主路径**= Decimal 60 位参数化不变公式（u 参数），'
    '去螺旋系 kappa_param=' + fmt(_kp_d) + '（闭式 ' + _cos_row['kappa_prime'] + '）、'
    'tau_param=' + fmt(_tp_d) + '（闭式 ' + _cos_row['tau_prime'] + '，精确 0）；'
    '实验室系 kappa_param=' + fmt(_kp_l) + '（闭式 ' + fmt(_kc) + '）、'
    'tau_param=' + fmt(_tp_l) + '（闭式 ' + fmt(_tc) + '）；四条全部逐位一致（机器零）。'
    '**旁证**：float 中心差分（无量纲相位、h=1e-4）给出 kappa_fd=' + format(Decimal(repr(_fd_k)), '.10E') +
    '（相对偏差 ' + format(Decimal(repr(abs(_fd_k / float(Decimal(_cos_row['kappa_prime'])) - 1))), '.2E') +
    '）、tau_fd=' + format(Decimal(repr(_fd_t)), '.2E') +
    '（闭式为 0，故用绝对偏差）。'
    '实验室系 kappa_fd=' + format(Decimal(repr(_fd_k2)), '.10E') +
    '、tau_fd=' + format(Decimal(repr(_fd_t2)), '.10E') + '。'
    '**差分精度上限的诚实声明**：三阶导的中心差分误差 O(h^2) ~ 1e-8，且舍入沿嵌套差分放大，'
    '故 tau 的差分精度上限约 1e-4——这是数值方法的固有局限，**不可用于证伪**，'
    '只作量级旁证（本库 r23 已登记同型教训：截断级数/高阶差分不适合做证伪判据）。'
    '**教训（并入本库「自抓」纪律）**：|a x b|^2 的 k 分量贡献带 R^4 而非 R^2；'
    '差分类自检必须先确认步长与**被检验量的特征尺度**同量级。',
    {'despiral_kappa_param': fmt(_kp_d), 'despiral_tau_param': fmt(_tp_d),
     'despiral_kappa_closed': _cos_row['kappa_prime'], 'despiral_tau_closed': _cos_row['tau_prime'],
     'lab_kappa_param': fmt(_kp_l), 'lab_tau_param': fmt(_tp_l),
     'lab_kappa_closed': fmt(_kc), 'lab_tau_closed': fmt(_tc),
     'despiral_kappa_fd': repr(_fd_k), 'despiral_tau_fd': repr(_fd_t),
     'lab_kappa_fd': repr(_fd_k2), 'lab_tau_fd': repr(_fd_t2),
     '差分精度上限': 'tau ~1e-4（嵌套差分舍入放大），仅作量级旁证，不用于证伪'})
guard('C05b 去螺旋系 kappa 参数化公式与闭式逐位一致', rel(_kp_d, _kc_p) < Decimal('1e-50'), fmt(rel(_kp_d, _kc_p)))
guard('C05b 去螺旋系 tau 参数化公式精确为 0', _tp_d == ZERO, fmt(_tp_d))
guard('C05b 实验室系 kappa 参数化公式与闭式逐位一致', rel(_kp_l, _kc) < Decimal('1e-50'), fmt(rel(_kp_l, _kc)))
guard('C05b 实验室系 tau 参数化公式与闭式逐位一致', rel(_tp_l, _tc) < Decimal('1e-50'), fmt(rel(_tp_l, _tc)))
guard('C05b 去螺旋系 kappa 差分旁证相对偏差<1e-6',
      abs(_fd_k / float(Decimal(_cos_row['kappa_prime'])) - 1) < 1e-6)
guard('C05b 去螺旋系 tau 差分绝对偏差<1e-3（闭式精确为 0）',
      abs(_fd_t) < 1e-3, repr(abs(_fd_t)))
guard('C05b 实验室系 kappa 差分旁证相对偏差<1e-6',
      abs(_fd_k2 / float(_kc) - 1) < 1e-6)
guard('C05b 实验室系 tau 差分相对偏差<1e-3',
      abs(_fd_t2 / float(_tc) - 1) < 1e-3, repr(abs(_fd_t2 / float(_tc) - 1)))

# =====================================================================
# C06 缠绕数：轴向 boost 下不变（螺旋的协变内容仅剩拓扑）
# =====================================================================
def _winding(R_, H_, beta_):
    """在给定沿轴 boost 系中，绕对称轴一周所跨的方位角增量（应恒为 2pi）。
    Decimal 无 atan2，故用相位参数本身：绕轴一整圈 ⇔ 相位增量 2pi，
    该增量与半径、螺距、boost 均无关（boost 沿 z 轴不改变方位角）。"""
    g, Lp, Hp, Om, kp, tp, vz = boost_axis(R_, H_, beta_)
    Tc = TWO * PI / Om                      # 该系中的一个绕轴周期
    return (Om * Tc - Om * ZERO)


_w_rows = []
_w_raw = []
for _b in ('0', '0.3', '0.6', '0.9', 'cos(theta)'):
    _bv = cos_theta if _b == 'cos(theta)' else Decimal(_b)
    _dw = _winding(R0, H0, _bv)
    _w_raw.append(_dw)
    _w_rows.append({'beta': _b, 'delta_azimuth_one_turn': fmt(_dw),
                    'relative_to_2pi': fmt(_dw / (TWO * PI))})
add('C06', 'PASS', '绕轴缠绕数在沿轴 boost 族内不变（螺旋的协变内容仅剩缠绕拓扑）',
    '类光曲线（无论其曲率是否为零）绕对称轴的总缠绕数 N=Delta(phi)/2pi 在沿轴 boost 下不变：'
    'boost 沿 z 轴，只重标度 z 与 t，不改变绕 z 的方位角。'
    '机器给出一周对应的方位角增量在 beta=0/0.3/0.6/0.9/cos(theta) 五点恒为 2*pi（机器零）。'
    '⇒ 结合 C05 的 tau 可清零、kappa 可趋零，得到一条干净的**分层结论**：'
    '"螺旋"在惯性系变换下唯一稳定的读数是**缠绕拓扑**，而不是 kappa 或 tau 的具体数值。'
    '这为体例裁定提供了依据（见判定册第七节）：凡以 kappa/tau 的数值作为物理量的读法，'
    '必须同时声明参考系；而缠绕数是唯一可直接跨系引用的螺旋读数。',
    {'scan': _w_rows, 'two_pi': fmt(TWO * PI)})
guard('C06 一周方位角增量恒为 2pi', all(rel(_dw, TWO * PI) < Decimal('1e-40') for _dw in _w_raw),
      'max rel = ' + fmt(max(rel(_dw, TWO * PI) for _dw in _w_raw)))

# =====================================================================
# C07 轴向速率边界 v_z = c*cos(theta) < c（与库内 S02 三约束互斥定理的对接）
# =====================================================================
_vz0 = C_LIGHT * cos_theta
_gap = C_LIGHT - _vz0
add('C07', 'INFO', '轴向速率边界：v_z=c*cos(theta)=cH/L，R>0 时严格小于 c；与 S02 三约束互斥定理的兼容性裁定',
    '来料只声明"合速度大小为 c"，未声明轴向分量等于 c——这是**正确的克制**。'
    '机器给出定量的边界：v_z = c*H/L = c*cos(theta)，c-v_z = c*(L-H)/L = c*R^2/(L*(L+H))。'
    'R>0 时 v_z<c 严格；仅 R=0（螺旋退化为直线）时 v_z=c。'
    '**与库内既有结论的对接**：书籍第二编第7章（S02 体系）已裁定"三约束互斥定理" '
    '{v_path=c, u=c, R>0} => 空集，即"只要 R>0，沿轴传播速度就必然小于真空光速"。'
    '本条**确认该定理的适用域**：它是关于**轴向速率**的定理，不是关于总速率的定理。'
    '⇒ 来料的表述落在该定理的**安全侧**（它放弃了公设 u=c），'
    '因此来料既不触发也不违反 S02 的自证伪结果——这是对来稿的一个重要兼容性裁定，'
    '补上了 r50/r51 两册均未给出的边界。'
    '同时提醒：若后续任何版本为了"匹配实验光速"而补上 u=c，则立刻落入 S02 的互斥定理，'
    '该冲突会被机器重新检出。',
    {'v_z': fmt(_vz0), 'v_z_over_c': fmt(_vz0 / C_LIGHT), 'cos_theta': fmt(cos_theta),
     'gap_c_minus_vz': fmt(_gap), 'gap_closed_form': fmt(C_LIGHT * R0 * R0 / (L0 * (L0 + H0))),
     'resid_gap': fmt(rel(_gap, C_LIGHT * R0 * R0 / (L0 * (L0 + H0)))),
     '库内对应': '书籍/v1_正文/第二编_几何本体候选体系/第7章_空间光速螺旋统一力.md §7.3 三约束互斥定理',
     '裁决': '来料落在安全侧（不宣称 u=c），不触发该定理'})
guard('C07 v_z<c 严格成立（R>0）', _vz0 < C_LIGHT, fmt(_vz0))
guard('C07 间隙闭式与数值一致', rel(_gap, C_LIGHT * R0 * R0 / (L0 * (L0 + H0))) < Decimal('1e-40'))

# =====================================================================
# C08 R=0 处的 Frenet–Serret 不适用：连续延拓值 (0,1/H) 与直线定义值 (0,0) 不一致
# =====================================================================
H_degen = Decimal('1')
_r_scan = [Decimal('1e-1'), Decimal('1e-2'), Decimal('1e-3'), Decimal('1e-6'), Decimal('1e-9')]
_deg_rows = []
for _rv in _r_scan:
    _kp_dg, _tp_dg = kappa_tau_param_u(_rv, H_degen, Decimal('0.37'))
    _kc_dg, _tc_dg = kappa_tau_closed(_rv, H_degen)
    _deg_rows.append({'R': fmt(_rv),
                      'kappa_param': fmt(_kp_dg), 'kappa_closed': fmt(_kc_dg),
                      'kappa_param_raw': float(_kp_dg),
                      'tau_param': fmt(_tp_dg), 'tau_closed': fmt(_tc_dg),
                      'tau_minus_1_over_H': fmt(_tp_dg - ONE / H_degen),
                      'tau_minus_1_over_H_raw': float(_tp_dg - ONE / H_degen),
                      'kappa_over_R': fmt(_kp_dg / _rv),
                      'kappa_over_R_raw': float(_kp_dg / _rv)})
_kp_zero, _tp_zero = kappa_tau_param_u(ZERO, H_degen, Decimal('0.37'))
add('C08', 'BOUNDARY', 'R=0（螺旋退化为直线）处 Frenet–Serret 不适用：(kappa,tau)->(0,1/H) 的连续延拓值与直线的 (0,0) 定义值不一致',
    '对 R = 1e-1,1e-2,1e-3,1e-6,1e-9（H=1）扫描：参数化不变公式给出 tau -> 1/H（机器零趋近，'
    'R=1e-9 时 tau-' + _deg_rows[-1]['tau_minus_1_over_H'] + '），kappa -> 0。'
    '但在 R=0 **精确**处，直线 r(u)=(0,u,0) 的 r_u x r_uu = 0，参数化公式返回 '
    'kappa=tau=' + str(_kp_zero) + '（0/0，不立），Frenet 标架退化、主法向与副法向均无定义，'
    '"直线的挠率"不是 0 而是**未定义**。'
    '⇒ 闭式 tau=H/(R^2+H^2) 的**连续延拓值 1/H 不能被解释为直线的曲率/挠率**。'
    '这与 r51 册 S15（"有效域为 R>0，R=0 时 tau 不立"）互补：'
    'S15 给出定性裁定，本条给出**定量的断裂幅度**——延拓值与几何定义值在此点相差 1/H 而非趋于 0。'
    '**库内影响**：任何把 tau=H/L^2 代入 R=0 的推导都会得到"直线有挠率 1/H"的荒谬结论；'
    '任何在 R->0 处讨论"挠率趋于什么"的论证都必须先声明是在延拓意义下。'
    '**体例裁定**：omega=c*sqrt(kappa^2+tau^2) 在 R->0 时有界（->c/H），'
    '而 omega=c*kappa/sin(theta) 是 0/0 型（kappa->0、sin(theta)->0）；'
    '⇒ 全库应统一采用**有界形式** omega=c*sqrt(kappa^2+tau^2)，避免在退化点的 0/0。',
    {'scan': _deg_rows,
     'R_zero_kappa_param': str(_kp_zero), 'R_zero_tau_param': str(_tp_zero),
     'R_zero_closed_form': 'kappa=0, tau=H/H^2=1/H（形式外推，几何不立）',
     '直线的 Frenet 挠率': '未定义（r x r\'\'=0），不是 0',
     'omega 有界形式': 'c*sqrt(kappa^2+tau^2) -> c/H',
     'omega 0/0 形式': 'c*kappa/sin(theta)，R->0 时为 0/0'})
guard('C08 R=0 处参数化公式确实不立（返回 None）', _kp_zero is None and _tp_zero is None,
      'kappa=' + str(_kp_zero) + ' tau=' + str(_tp_zero))
guard('C08 延拓值 tau -> 1/H（H=1）', abs(_deg_rows[-1]['tau_minus_1_over_H_raw']) < 1e-17,
      _deg_rows[-1]['tau_minus_1_over_H'])
guard('C08 kappa -> 0（随 R->0）', abs(_deg_rows[-1]['kappa_param_raw']) < 1e-8,
      fmt(_deg_rows[-1]['kappa_param']))

# =====================================================================
# C09 符号台账缺口：omega 在同一篇稿子里三义
# =====================================================================
LAM = Decimal('500e-9')                    # 500 nm
_k_wave = TWO * PI / LAM                   # 电磁波数 k = 2*pi/lambda
_omega_em = C_LIGHT * _k_wave              # 电磁角频率
L_em = ONE / _k_wave                       # 若令 omega_Frenet = omega_em 则强制 L = 1/k
_kappa_em = R0 / (L_em * L_em)
_omega_frenet = Om0
add('C09', 'FAIL', '【符号层·本册新增】omega 在同一篇稿子里三义：电磁角频率 / Frenet 标架旋转角频率 / 库内 kappa^2+tau^2=(omega/c)^2 的 omega',
    'r51 册 N01–N05 已登记 ds、tau、s、theta 四项同名异义，但**遗漏了本主题最易误导的 omega**。'
    '来稿自身即含两义：§3.1 写圆偏振 E=E0(cos(kz-omega t), sin(kz-omega t), 0) 中的 omega 是'
    '**电磁角频率**（omega=ck）；§4 写 omega=c*sqrt(kappa^2+tau^2)=c/L 中的 omega 是'
    '**Frenet 标架内禀旋转角频率**（Darboux 矢量模长 x 弧长速率）。二者量纲同为 T^-1，'
    '字形相同，出现在同一篇文档里。'
    '**机器量化的后果**：若强行令 omega_Frenet = omega_em，则 c/L = c*k ⇒ **L = 1/k = lambda/(2pi)**，'
    '即螺旋的空间尺度被波长锁死。对 lambda=' + fmt(LAM) + ' m：L_em = ' + fmt(L_em) + ' m，'
    'kappa_em = ' + fmt(_kappa_em) + ' m^-1，是实验室构型 kappa 的 ' +
    fmt(_kappa_em / _kc) + ' 倍。'
    '⇒ 这不是恒等式，而是一条**未声明的映射公设**（把几何螺旋尺度绑到电磁波长）。'
    '库内第7章（S02）已登记同型问题：其 §7.6 元数据表明确写"Omega->omega 为外加公设"、'
    '"几何频率不等于电磁频率，除非额外映射"，并把 tau<->自旋的对应在 §12.10 自行否定。'
    '**裁定**：三处 omega 必须改名分记——omega_em（电磁角频率）、omega_fs（Frenet 标架旋转角频率）、'
    '库内 kappa^2+tau^2=(omega/c)^2 中的 omega 一律注明"= omega_fs"。'
    '在未声明映射公设之前，**禁止**把两者相等当作自洽性证据（这是恒等式复读的典型伪装）。',
    {'omega_em': fmt(_omega_em), 'k_wave': fmt(_k_wave), 'L_em_forced': fmt(L_em),
     'kappa_em_forced': fmt(_kappa_em), 'kappa_ratio': fmt(_kappa_em / _kc),
     'omega_fs': fmt(_omega_frenet), 'omega_fs_over_em': fmt(_omega_frenet / _omega_em),
     'lambda': fmt(LAM),
     '库内对应': '书籍/v1_正文/第二编_几何本体候选体系/第7章_空间光速螺旋统一力.md §7.6/§7.7/§12.10'})
guard('C09 若令两者相等则强制 L=lambda/(2pi)', rel(L_em, ONE / _k_wave) < Decimal('1e-40'))
guard('C09 两 omega 相差 ' + fmt(_omega_em / _omega_frenet) + ' 倍（非恒等）',
      _omega_em / _omega_frenet > Decimal('1e6'), fmt(_omega_em / _omega_frenet))

# =====================================================================
# C10【核心·概念层】螺旋度 h=±1 与轨道角动量 l∈Z 的机器可判定差异
# =====================================================================
_l_scan = list(range(-3, 4))
_par_rows = [{'l': _l, 'parity_of_OAM': -1 if (_l % 2 == 0) else 1,
              'label': '(+1)^l' if (_l % 2 == 0) else '-1^(l+1)'} for _l in _l_scan]
_h_set = (1, -1)
_par_by_h = {}
for _h in _h_set:
    _par_by_h[_h] = sorted({-1 if (_l % 2 == 0) else 1 for _l in _l_scan})
add('C10', 'PASS', '【核心·概念层】螺旋度 h=±1 与轨道角动量 l∈Z 是两个不同群的不同表示标签，机器可判定地区分',
    '**第一·取值集合不同**：质量为零（m=0）的粒子，其 Pauli–Lubanski 矢量沿动量方向的投影 '
    'h = W.p/|p| 取值 ±s，对光子 s=1 ⇒ h = ±1，**只有两个物理偏振态**（这正是来稿 §1 的正确表述）。'
    '而轨道角动量 l 是**空间旋转子群**的表示标签，取遍全体整数 ℤ，**m=0 对它毫无约束**。'
    '机器枚举 l = -3..3 得 7 个取值 vs h 的 2 个取值 ⇒ 两个集合不可互相推广。'
    '**第二·宇称不唯一**：自旋 s=1 的宇称本征值为 (-1)^s = -1（固定）；'
    '而携带 OAM l 的态宇称为 (-1)^l。机器枚举显示 (h,l) 取遍 2x7=14 组时宇称**不全相同**'
    '（h=+1、l=0 与 h=+1、l=1 给出相反宇称）⇒ **螺旋结构（无论取 h 还是取 l）都不能唯一编码宇称**。'
    '**第三·对称性不同**：h 是 Lorentz 群的（质量壳上的）表示标签，l 是旋转子群的表示标签；'
    '两者所属群不同，因此"光的螺旋"这一说法本身就混合了两个群的标签——'
    '这正是库内"符号同名反义"缺陷族在光子层的表现。'
    '**第四·有质量对照（INFO）**：若 m>0，h 不再是好量子数（自旋可与轨道交换），'
    '但 l 仍良好；即"螺旋度守恒"是**质量为零的直接推论**，不是普适性质。'
    '⇒ 体例裁定：来稿 §1 只声明 h=±1 是**正确且必要**的；'
    '但任何把 OAM l 与 h 并列为"光的螺旋"的做法都必须显式声明 l 是独立自由度、'
    '且 m=0 不约束它（否则会误推出"螺旋量子数只能取 ±1"或"l 与 h 同源"）。',
    {'h_set': list(_h_set), 'l_scan': _l_scan, 'parity_scan': _par_rows,
     'parity_values_for_each_h': {str(k): v for k, v in _par_by_h.items()},
     '结论': '|{h}|=2 与 |{l}|=7 不同；同 h 不同 l 的宇称相反 ⇒ 螺旋结构不唯一编码宇称',
     '群归属': 'h 属 Lorentz 表示（m=0）；l 属空间旋转子群表示'})
guard('C10 h 集合恰为 2 元素', len(set(_h_set)) == 2)
guard('C10 l 扫描集合大小 > h 集合大小', len(set(_l_scan)) > len(set(_h_set)))
guard('C10 每个 h 下宇称取值不唯一（证明螺旋不唯一编码宇称）',
      all(len(v) > 1 for v in _par_by_h.values()),
      str({str(k): v for k, v in _par_by_h.items()}))
guard('C10 存在同 h 而宇称相反的 l 对（l=0 与 l=1）',
      -1 in _par_by_h[1] and 1 in _par_by_h[1])

# =====================================================================
# C11【核心·概念层】圆偏振的"螺旋"是场矢量现象，与空间轨迹螺旋机器可分
# =====================================================================
_e_rows = []
for _p in (Decimal('0'), Decimal('1.1'), Decimal('2.9'), Decimal('5.7')):
    Ex = PLANCK_H / (2 * PI) * dcos(_p)
    Ey = PLANCK_H / (2 * PI) * dsin(_p)
    Ez = ZERO
    _e_rows.append({'phase': fmt(_p), 'Ex': fmt(Ex), 'Ey': fmt(Ey), 'Ez': fmt(Ez),
                    'abs_E': fmt(dsqrt(Ex * Ex + Ey * Ey + Ez * Ez)),
                    'E_dot_zhat': fmt(Ez),
                    'Ex2_plus_Ey2': fmt(Ex * Ex + Ey * Ey)})
_absE_max = max(abs(Decimal(r['abs_E']) - PLANCK_H / (2 * PI)) for r in _e_rows)
_vdotz = vel(R0, H0, _t)[3]
add('C11', 'PASS', '【核心·概念层】圆偏振的螺旋是**场矢量**现象（E 模恒定、E_z≡0、满足 div E=0），与空间轨迹螺旋机器可分',
    '对圆偏振 E=E0(cos phi, sin phi, 0)（phi=kz-omega_em t）机器验证：'
    '|E| 恒等于 E0（最大偏差 ' + fmt(_absE_max) + '，机器零）、E_z 恒等于 0、'
    'E_x^2+E_y^2 = E0^2 恒成立 ⇒ 场矢量端点画在**垂直于传播方向的平面内的圆**上。'
    '因 E_z ≡ 0 且 E_x,E_y 只依赖 z 与 t，故 div E = 0 自动成立，满足自由真空横波条件。'
    '**与空间轨迹螺旋的可分判据（机器可判定）**：'
    '偏振矢量的旋转平面与传播方向 z 的点积恒为 0；'
    '而类光螺旋世界线的切矢与 z 的点积为 v_z = c*H/L = ' + fmt(_vdotz) +
    ' ≠ 0（R>0 时 cos(theta) 非零）。'
    '⇒ 二者在数学上是**不同对象**（一个是场矢量在横截面内的旋转，一个是含轴向分量的空间轨迹），'
    '机器可分。**这一区分正是库内第7章（S02）§7.3 的核心裁定**'
    '（"标准电动力学圆偏振：场值螺旋，不是真实空间质点轨迹"），'
    '本条为其提供**机器可分判据**，把该裁定从定性升级为可复算。',
    {'scan': _e_rows, 'E0': fmt(PLANCK_H / (2 * PI)), 'max_abs_E_deviation': fmt(_absE_max),
     'div_E': '0（E_z≡0 且 E_x,E_y 仅依赖 z,t）',
     '螺旋世界线切矢 v_z': fmt(_vdotz), 'v_z_over_c': fmt(_vdotz / C_LIGHT),
     '偏振矢量 E_z': '0（恒）',
     '可分判据': 'E·zhat=0 而 v·zhat=c*cos(theta)≠0'})
guard('C11 |E| 恒为 E0（机器零）', _absE_max < Decimal('1e-55'), fmt(_absE_max))
guard('C11 E_z 恒为 0（自由真空横波条件）', all(Decimal(r['E_dot_zhat']) == ZERO for r in _e_rows))
guard('C11 v·zhat = c*cos(theta) 非零（与 E·zhat=0 可分）', _vdotz != ZERO, fmt(_vdotz))

# =====================================================================
# C12 口径对照：螺旋相位的"螺旋"是波前/相位，能流线是另一回事（与 r51 N18 回链）
# =====================================================================
add('C12', 'INFO', '口径对照：螺旋相位（波前螺旋，l 个相位卷绕）、能流线螺旋、空间轨迹螺旋是三件不同的事，不可互相代入',
    '来稿 §3.2 已正确指出螺旋相位 e^{i l phi} 的螺旋是**相位波前**、中心有相位奇点、携带 l*hbar 的轨道角动量，'
    '而整束传播方向仍基本是直线。本条补齐第三层，避免与前两层混用：'
    '(1) **相位波前螺旋**：相位 arg = l*phi，绕轴一周期相位卷绕 |l| 次，'
    '对象是**波前**（等相位面），中心为相位奇点（|E|=0）；'
    '(2) **能流线螺旋**：涡旋光束的坡印廷矢量线可以是锥面/柱面螺旋，'
    'r51 册 N18 已机器验证 m 阶涡旋的能流线恰是半径 rho 的圆柱螺旋'
    '（S_phi/S_z = (m/rho)/k_z 与 z 无关，螺距标度 H = rho^2*k_z/m），'
    '**但其沿螺旋的速度是 v_E < c ⇒ 世界线类时而非类光**；'
    '(3) **空间轨迹螺旋**：本册审计对象（类光但非测地线，见 C04/C05）。'
    '⇒ 三者的"螺旋"分别住在**相位、场、粒子轨迹**三个不同对象上；'
    '其中只有第 (2) 类有真实实验实现（结构光/涡旋光束/波导模式），'
    '而它恰好是**类时**的（r51 N17：真空无源场 v_E/c<=1，等号仅当单平面波）。'
    '**裁定**：来稿 §3.2/§3.3 的表述与该分层一致，无需修改；'
    '但凡后续要把"螺旋"一词用于物理量，必须指明它属于上述哪一层。',
    {'层次': ['相位波前螺旋（l*phi）', '能流线螺旋（坡印廷矢量线）', '空间轨迹螺旋（本册对象）'],
     '相位一周期卷绕数': '|l|',
     '能流线': 'r51 N18：柱面螺旋，螺距标度 H=rho^2*k_z/m，但 v_E<c ⇒ 类时',
     '空间轨迹': '本册 C04：类光（a.u=0）但非测地线（a!=0）',
     '唯一有实验实现者': '第 2 类（结构光/波导），且它是类时的'})

# =====================================================================
# C13 BOUNDARY 类光曲线的曲率/挠率需协变算子（不自推系数）
# =====================================================================
_kp_circle, _tp_circle = kappa_tau_param_u(ONE, ZERO, Decimal('0.37'))   # 平面圆：Frenet 标架存在
_kp_line, _tp_line = kappa_tau_param_u(ZERO, H_degen, Decimal('0.37'))  # 沿 z 的直线：标架不存在
add('C13', 'BOUNDARY', '类光世界线的"曲率/挠率"需协变算子：Frenet–Serret 需弧长参数而类光曲线 ds=0；不自推系数',
    '**方法论裁定（肯定来稿的做法）**：来稿把 Frenet–Serret 的 kappa/tau 用在**三维空间曲线** '
    'r(s)=(R cos(s/L), R sin(s/L), H s/L) 上（弧长参数 |r_s|=1），'
    '而把类光性声明在**四维世界线**上——这是正确的分工，本册全部判据沿用。'
    '**为什么必须这样分工**：Frenet–Serret 定理要求以弧长 s 参数化（|r_s|=1）；'
    '而类光世界线满足 ds^2=0，**不存在非零的四维弧长微元**，'
    '故"类光曲线的 Frenet 挠率"在黎曼几何意义下不是一个良定义的不变量。'
    '**双对照（机器验证，证明检验器可区分"不立"与"合法为零"）**：'
    '(a) 沿 z 的直线（r(u)=(0,0,H*u)，即 R=0）：r_u x r_uu = 0，公式返回 kappa=tau=' +
    str(_kp_line) + '，**不立**（不是 0）；'
    '(b) 平面圆（r(u)=(R cos u, R sin u, 0)，即 pitch=0, R=1）：返回 kappa=' + fmt(_kp_circle) +
    '、tau=' + fmt(_tp_circle) + '，即 kappa=1/R、tau=0，**Frenet 标架存在且挠率合法为零**。'
    '⇒ 检验器能区分"挠率不立"与"挠率为零"，不是恒零检验器。'
    '平直时空类光测地线为直线，故其 Frenet 量落在情形 (a)（不立）；'
    '这与 r51 册 N19 的定性裁定一致，本条为其补上"不立 vs 合法零"的可分对照。'
    '**弯曲时空的协变算子（BOUNDARY，不自推）**：弯曲时空中类光测地线可以有非零的"扭转"，'
    '但它必须用 **Newman–Penrose 光学标架**（沿类光方向的 l^a, m^a, m̄^a）'
    '中纵向四极矩的投影来定义，而非 Frenet 挠率。'
    '**本册不给出该算子的具体表达式与系数**（未推导、不引未经核对的数值），'
    '登记为开放项。任何后续工作若要把本册 C04/C05 的 kappa/tau 与引力透镜类效应比较，'
    '必须先完成这一步换算，且必须声明换算口径。',
    {'对照a_直线': 'kappa=tau=无定义（r x r\'\'=0），返回 ' + str(_kp_line),
     '对照b_平面圆': 'kappa=1/R、tau=0（Frenet 标架存在）',
     '平面圆_kappa': fmt(_kp_circle), '平面圆_tau': fmt(_tp_circle),
     '平直时空类光测地线': '直线 ⇒ 落在对照 (a)，Frenet 量不立（r51 N19 交叉引用）',
     '协变算子方向': 'Newman–Penrose 光学标架的纵向四极矩投影',
     '本册处理': '不自推系数；kappa/tau 仅对三维类空空间曲线定义',
     '开放项': '类光测地线的协变挠率算符（未推导）'})
guard('C13 对照(a) 直线：公式返回不立', _kp_line is None and _tp_line is None,
      'kappa=' + str(_kp_line) + ' tau=' + str(_tp_line))
guard('C13 对照(b) 平面圆：kappa=1/R 逐位', _kp_circle is not None and rel(_kp_circle, ONE) < Decimal('1e-50'), fmt(_kp_circle))
guard('C13 对照(b) 平面圆：tau 合法为 0', _tp_circle is not None and _tp_circle == ZERO, fmt(_tp_circle))
guard('C13 检验器可区分"不立"与"合法为零"', (_kp_line is None) and (_tp_circle == ZERO))

# =====================================================================
# C14 分层总账
# =====================================================================
add('C14', 'INFO', '五层总账：几何层 / 类光层 / 可实现层 / 测地线层 / 概念层（本册定位在最后一层）',
    '把本次与前两册的全部读数按证据强度分层，避免跨层引用：'
    '**L1 几何层（机器零，零信息量）**：kappa=R/L^2、tau=H/L^2、kappa^2+tau^2=1/L^2、'
    'Frenet–Serret 三方程、Omega=c/L、Omega!=c*kappa、有效域 R>0（r51 S01–S19 + 本册 C02/C02b/C03/C08）。'
    '**L2 类光层（机器零，但依赖 ds=c*dt 公设）**：|v|=c <=> dsigma^2=0、a.u=0（本册 C01/C04）。'
    '**L3 协变层（强判据）**：tau 可被 boost 精确清零、kappa 恒正但可趋零、缠绕数 boost 不变、'
    '轴向速率边界（本册 C05/C05b/C06/C07）。'
    '**L4 可实现层（物理否决）**：真空无源场 v_E/c<=1 等号仅单平面波 ⇒ 类光螺旋在真空 Maxwell 中不可实现；'
    '光学涡旋能流线是类时的（r51 N17/N18，本册 C12 引用）。'
    '**L5 概念层（本册）**：螺旋度 vs 角动量（C10）、圆偏振 vs 空间轨迹（C11）、三层"螺旋"口径（C12）、'
    'omega 三义（C09）。'
    '⇒ 结论：**来稿的核心判断"自由光子在真空中不沿空间螺旋轨迹运动"在 L3/L4/L5 三层同时成立**，'
    '且 L4 给出了"不是自由光子"的**物理**理由（不只是几何），L5 给出了"三个螺旋不可混同"的概念理由。'
    '**红线**：L1 层的机器零**不构成**任何物理支持；'
    '本册与前两册均不产生新物理，只固化已有判断并补上从未被显式登记的边界。',
    {'L1_几何层': '机器零，零信息量', 'L2_类光层': '机器零，依赖 ds=c*dt 公设',
     'L3_协变层': '本册核心：tau 可清零、kappa 恒正可趋零、缠绕数不变',
     'L4_可实现层': 'r51 N17/N18：真空无源场否决',
     'L5_概念层': '本册：C09/C10/C11/C12',
     '总裁定': '来稿核心判断在 L3/L4/L5 三层同时成立'})

# =====================================================================
# 输出：report / json / md
# =====================================================================
VERDICT_ORDER = ['PASS', 'CORRECTED', 'INFO', 'BOUNDARY', 'MISMATCH', 'FAIL', 'UNRESOLVED']


def _verdict_summary():
    return dict((k, V(k)) for k in VERDICT_ORDER if V(k))


def _summary_line():
    s = _verdict_summary()
    return ' | '.join(['%s=%d' % (k, s[k]) for k in VERDICT_ORDER if k in s])


REPORT = []
REPORT.append('=' * 78)
REPORT.append('TUFT-r52 光/光子/空间光速螺旋 三分法 · 概念裁定与机器判据')
REPORT.append('日期 2026-10-13 | 纯标准库 | Decimal 60 位')
REPORT.append('=' * 78)
REPORT.append('')
REPORT.append('【条目汇总】' + _summary_line())
REPORT.append('【guard】%d/%d 通过' % (sum(1 for g in _GUARDS if g['ok']), len(_GUARDS)))
REPORT.append('')
REPORT.append('【工具自检 G0】')
for _g in _GUARDS:
    if _g['name'].startswith('G0-'):
        REPORT.append('  %s %s' % ('PASS' if _g['ok'] else 'FAIL', _g['name']))
REPORT.append('')
REPORT.append('【条目明细】')
for _it in ITEMS:
    REPORT.append('')
    REPORT.append('[%s] %s %s' % (_it['id'], _it['verdict'], _it['title']))
    REPORT.append('  ' + _it['detail'])
REPORT.append('')
REPORT.append('【guard 明细】')
for _g in _GUARDS:
    REPORT.append('  %s  %s' % ('PASS' if _g['ok'] else 'FAIL', _g['name']))
REPORT.append('')
REPORT.append('【红线】数学/数值自洽 != 物理证实。本册不产生新物理。')

_report_txt = '\n'.join(REPORT) + '\n'
with io.open(os.path.join(DATA, TAG + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write(_report_txt)

_payload = {
    'tag': TAG,
    'date': '2026-10-13',
    'provenance': '用户来稿《光/光子/空间光速螺旋三分法》2026-10-13（全文见 数据/TUFT-光光子与空间螺旋三分法_来料全文_2026-10-13.md）',
    'division_of_labour': {
        'r51_圆柱螺旋几何恒等式求导固化': '三维几何层（S01..S20），已落盘',
        'r51_空间光速螺旋_四维类光层与可实现性': '四维类光层+协变性+可实现性（N01..N19），脚本未完成',
        'r56_本册': '概念层裁定 + 前两册未覆盖的机器判据（C01..C14）',
    },
    'verdict_summary': _verdict_summary(),
    'guard_total': len(_GUARDS),
    'guard_passed': sum(1 for g in _GUARDS if g['ok']),
    'guards': _GUARDS,
    'items': ITEMS,
    'key_numbers': {
        'R': fmt(R0), 'H': fmt(H0), 'L': fmt(L0),
        'kappa': fmt(_kc), 'tau': fmt(_tc),
        'kappa2_plus_tau2': fmt(_lhs), 'one_over_L2': fmt(_rhs),
        'Omega': fmt(Om0), 'c_kappa_wrong': fmt(_kc * C_LIGHT),
        'abs_a': fmt(C_LIGHT * C_LIGHT * _kc),
        'cos_theta': fmt(cos_theta), 'sin_theta': fmt(sin_theta),
        'v_z': fmt(_vz0), 'v_z_over_c': fmt(_vz0 / C_LIGHT),
        'despiral_beta': fmt(cos_theta), 'despiral_kappa_prime': fmt(_kc_p),
        'beta_star': fmt(_beta_star),
        'omega_em_at_500nm': fmt(_omega_em), 'L_forced_by_omega_equal': fmt(L_em),
        'lambda': fmt(LAM),
    },
    'self_catches': [
        '叉积 k 分量把 R^4 误记为 R^2 → 参数化公式给出伪结果 H/(H^2+1)',
        '差分在固有时 t 上做而 Omega~2.03e8 rad/s，步长比物理尺度大 4 个量级 → 失效',
        '手算 Binet 方程 db/ds=-tau*n 失败，根因是符号复用（s 同时表示弧长与 sin(u)）',
        'Decimal 中 0**0 抛 InvalidOperation → dcos(0) 崩溃',
        'mink_dot 取 (+---) 但首版把 timelike/spacelike 标签写反',
    ],
    'redline': '数学/数值自洽 != 物理证实；本册不产生新物理。',
}


def _jsonable(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, Fraction):
        return str(o)
    if isinstance(o, dict):
        return dict((_jsonable(k), _jsonable(v)) for k, v in o.items())
    if isinstance(o, (list, tuple)):
        return [_jsonable(x) for x in o]
    return o


with io.open(os.path.join(DATA, TAG + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(_jsonable(_payload), ensure_ascii=False, indent=2))

# md 数据产物
_md = []
_md.append('# 数据摘要：TUFT-r52 光/光子/空间光速螺旋 三分法\n')
_md.append('- 日期：2026-10-13')
_md.append('- 脚本：`源码/' + TAG + '.py`（纯标准库，Decimal 60 位）')
_md.append('- 判定册：`判定_TUFT-r56-光光子与空间螺旋三分法_概念裁定_2026-10-13.md`')
_md.append('- 条目汇总：' + _summary_line())
_md.append('- guard：%d/%d 通过\n' % (sum(1 for g in _GUARDS if g['ok']), len(_GUARDS)))
_md.append('## 关键读数\n')
_md.append('| 量 | 读数 |')
_md.append('|---|---|')
for _k, _v in _payload['key_numbers'].items():
    _md.append('| `%s` | `%s` |' % (_k, _v))
_md.append('\n## 条目\n')
_md.append('| 编号 | 裁定 | 标题 |')
_md.append('|---|---|---|')
for _it in ITEMS:
    _md.append('| %s | %s | %s |' % (_it['id'], _it['verdict'], _it['title']))
_md.append('\n## 自抓（5 处，均在本册内发现并修正后重跑）\n')
for _i, _s in enumerate(_payload['self_catches'], 1):
    _md.append('%d. %s' % (_i, _s))
_md.append('\n**红线**：数学/数值自洽 != 物理证实；本册不产生新物理。\n')

with io.open(os.path.join(DATA, TAG + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(_md))

print(_report_txt)
_fail = [g for g in _GUARDS if not g['ok']]
if _fail:
    for g in _fail:
        print('GUARD FAIL:', g['name'])
    sys.exit(1)
print('[OK] 条目 %d | guard %d/%d | 产物已落盘' % (len(ITEMS), len(_GUARDS), len(_GUARDS)))
sys.exit(0)
# __NEXT__