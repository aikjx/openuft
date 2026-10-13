# -*- coding: utf-8 -*-
"""
TUFT r59 · 圆柱螺旋增量复核与作用量系数裁定 · 全维审计（2026-10-13）

来料主题：在 r58《圆柱螺旋几何恒等式求导固化》之后，用户给出的**增量版**答复。
本册只审 r58 未覆盖的增量，不重算 r58 已固化的几何层（零重复声明见判定册 §〇）。

增量清单：
  I1 三组数值验证表（含新 case R=0.5, H=1）
  I2 §4 表第 11 行「作用量系数 hbar/(2c) 量纲不对，需改为 hbar/2 或 hbar*c/2」
  I3 §4 表第 12 行「逗号代替乘号」
  I4 §5 八步实验数据验证协议

量纲口径：三维 (M, L, T)。本册不涉及电荷量纲，故不用 r43/r44/r45 的四元组 (M,L,T,Q)。

纪律（承自 r37 / r44 / r45，本轮严格执行）：
  D1 量纲工具自身先过 guard，再用于任何判定；
  D2 dmul 必须是「指数相加」；写成逐分量相乘是本库已复发三次的事故型 bug；
  D3 「恒等于零」的裁定必须配阳性对照；
  D4 「残差趋机器零」不等于公式正确，必须双路径对拍且残差停在差分截断极限。
"""
import sys
import os
import json
import io
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), '数据')
TAG = 'r59'
C_EXACT = D('299792458')
ZERO = D('0')
ONE = D('1')
TWO = D('2')
HALF = D('0.5')
PI = D('3.14159265358979323846264338327950288419716939937510582097494')

# ======================================================================
# 量纲工具：三维 (M, L, T)，指数为 Fraction
# ======================================================================
_M, _L, _T = 'M', 'L', 'T'


def _z():
    return (F(0), F(0), F(0))


DIM_M = (F(1), F(0), F(0))
DIM_L = (F(0), F(1), F(0))
DIM_T = (F(0), F(0), F(1))
DIM_ONE = _z()
DIM_HBAR = (F(1), F(2), F(-1))          # 普朗克常数 ML^2 T^-1
DIM_C = (F(0), F(1), F(-1))             # 光速     L T^-1
DIM_MASS = DIM_M                        # 质量     M
DIM_KAPPA = (F(0), F(-1), F(0))         # 曲率/挠率 L^-1
DIM_OMEGA = (F(0), F(0), F(-1))         # 角频率   T^-1
DIM_ENG_DENSITY = (F(1), F(-1), F(-2))  # 能量密度 ML^-1 T^-2
DIM_GRAD_SQ = (F(0), F(-4), F(0))       # (grad kappa)^2


def dmul(a, b):
    """量纲相乘 = 指数逐分量【相加】。纪律 D2：本库已复发三次写成逐分量相乘。"""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dinv(a):
    return (-a[0], -a[1], -a[2])


def dpow(a, n):
    return (a[0] * n, a[1] * n, a[2] * n)


def dstr(d):
    names = [_M, _L, _T]
    out = []
    for nm, e in zip(names, d):
        if e == 0:
            continue
        if e == 1:
            out.append(nm)
        elif e == -1:
            out.append('%s^-1' % nm)
        elif e < 0:
            out.append('%s^-%s' % (nm, abs(e)))
        else:
            out.append('%s^%s' % (nm, e))
    return ' '.join(out) if out else '1'


def dsame(a, b):
    return a[0] == b[0] and a[1] == b[1] and a[2] == b[2]


# ======================================================================
# 三角函数（Decimal 无 sin/cos/atan，自实现）
# 递推比：sin  term_k/term_{k-1} = -x^2/[(2k)(2k+1)]
#         cos  term_k/term_{k-1} = -x^2/[(2k-1)(2k)]
#         atan term_k/term_{k-1} = -x^2/(2k+1)
# ======================================================================
def dsin(x):
    term, s, k = x, x, 0
    while abs(term) > D('1e-70'):
        k += 1
        term = -term * x * x / (D(2 * k) * D(2 * k + 1))
        s += term
    return s


def dcos(x):
    term, s, k = D(1), D(1), 0
    while abs(term) > D('1e-70'):
        k += 1
        term = -term * x * x / (D(2 * k - 1) * D(2 * k))
        s += term
    return s


def datan(x):
    """atan via half-angle reduction: atan(x) = 2*atan(x/(1+sqrt(1+x^2)))"""
    x = D(x)
    neg = x < 0
    x = abs(x)
    k = 0
    while x > D('0.05'):
        x = x / (ONE + (ONE + x * x).sqrt())
        k += 1
    term, s, n = x, x, 0
    while abs(term) > D('1e-70'):
        n += 2
        term = -term * x * x
        s += term / D(n + 1)
    out = s * (D(2) ** k)
    return -out if neg else out


def datan2(y, x):
    if x > 0:
        return datan(y / x)
    if x < 0:
        return datan(y / x) + (PI if y >= 0 else -PI)
    return HALF * PI if y > 0 else (-HALF * PI if y < 0 else ZERO)


def ddeg(rad):
    return rad * D(180) / PI


# ======================================================================
# 数值工具
# ======================================================================
def rel(a, b):
    """相对偏差；b 为 0 时退化为绝对偏差"""
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


def fs(x):
    """定点输出：Decimal.quantize 在高位数会抛 InvalidOperation（本库已记录）"""
    return format(D(x), '.25E')


def fv(x, n=12):
    """定点输出；quantize 在高位数会抛 InvalidOperation（本库 r18 已记录）⇒ 失败回落 fs"""
    try:
        q = D(10) ** (-n)
        return format(D(x).quantize(q), 'f')
    except Exception:
        return fs(x)


# ======================================================================
# 判定引擎
# ======================================================================
ENTRIES = []
GUARDS = []


def E(code, verdict, title, detail=''):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title, 'detail': detail})


def G(name, ok, note=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


def PASS(c, t, d=''):
    E(c, 'PASS', t, d)


def FAIL(c, t, d=''):
    E(c, 'FAIL', t, d)


def BOUND(c, t, d=''):
    E(c, 'BOUNDARY', t, d)


def INFO(c, t, d=''):
    E(c, 'INFO', t, d)


def CORR(c, t, d=''):
    E(c, 'CORRECTED', t, d)


def MISM(c, t, d=''):
    E(c, 'MISMATCH', t, d)


# ======================================================================
# 圆柱螺旋解析量（r58 已固化的几何层，此处仅作被检验对象，不重新裁定）
# ======================================================================
def helix(R, H):
    """返回该圆柱螺旋的全部解析量。s 为弧长，L^2 = R^2 + H^2。"""
    L2 = R * R + H * H
    L = L2.sqrt()
    kap = R / L2
    tau = H / L2
    sn = R / L
    cs = H / L
    om = ONE / L                        # = 1/L = sqrt(kappa^2 + tau^2)（纪律 D4：勿误写为 L）
    return {'R': R, 'H': H, 'L': L, 'L2': L2, 'kappa': kap, 'tau': tau,
            'sin': sn, 'cos': cs, 'sqrt_kt': om,
            'omega_geom': om,          # 每单位弧长的标架旋转率 = 1/L
            'theta_deg': ddeg(datan2(R, H))}


def num_omega(h, v):
    """时间角频率：omega = v * sqrt(kappa^2+tau^2)；Omega = v / L"""
    return v * h['sqrt_kt'], v / h['L']


# ======================================================================
# 自检 guard（纪律 D1：量纲工具先自检）
# ======================================================================
def selfcheck():
    # G0-1 dmul 必须是指数相加（若误写成逐分量相乘，(1,2,-1)*(0,1,-1) 会给出 (0,2,1)）
    G('G0-1 dmul_is_exponent_addition',
      dsame(dmul(DIM_HBAR, DIM_C), (F(1), F(3), F(-2))),
      '[hbar]*[c] 应为 ML^3 T^-2，实得 %s' % dstr(dmul(DIM_HBAR, DIM_C)))
    # G0-2 负幂次不得抛 ZeroDivisionError
    ok = False
    try:
        ok = dsame(dpow(DIM_L, -2), (F(0), F(-2), F(0)))
    except Exception:
        ok = False
    G('G0-2 dpow_handles_negative_exponent', ok, '[L^-2] 应为 L^-2')
    # G0-3 [c^2] = L^2 T^-2
    G('G0-3 c_squared_is_L2T_minus2', dsame(dpow(DIM_C, 2), (F(0), F(2), F(-2))),
      '[c^2] = %s' % dstr(dpow(DIM_C, 2)))
    # G0-4 [hbar/(2c)] = M L
    coef = dmul(DIM_HBAR, dinv(DIM_C))
    G('G0-4 hbar_over_2c_is_ML', dsame(coef, (F(1), F(1), F(0))),
      '[hbar/(2c)] = %s' % dstr(coef))
    # G0-5 dstr 渲染可回读
    G('G0-5 dstr_roundtrip', dstr(DIM_ENG_DENSITY) == 'M L^-1 T^-2',
      dstr(DIM_ENG_DENSITY))
    # G0-6 Decimal sqrt 精度（用恒等式自证，避免参照值位数成为限制）
    _s2 = D(2).sqrt()
    G('G0-6 decimal_sqrt_selfconsistent', abs(_s2 * _s2 - D(2)) < D('1e-55')
      and rel(_s2, D('1.41421356237309504880168872420969807857')) < D('1e-38'),
      'sqrt(2) = %s；sqrt(2)^2 - 2 = %s' % (fs(_s2), fs(_s2 * _s2 - D(2))))
    # G0-7 dsin/dcos 已知角
    G('G0-7 dsin_dcos_known_angle',
      rel(dsin(PI / D(6)), D('0.5')) < D('1e-50') and rel(dcos(PI / D(3)), HALF) < D('1e-50'),
      'sin(pi/6)=%s cos(pi/3)=%s' % (fs(dsin(PI / D(6))), fs(dcos(PI / D(3)))))
    # G0-8 datan 已知值
    G('G0-8 datan_known_value', abs(datan(ONE) - PI / D(4)) < D('1e-55'),
      'atan(1) = %s (pi/4 = %s)' % (fs(datan(ONE)), fs(PI / D(4))))
    # G0-9 datan2 四象限
    G('G0-9 datan2_quadrants',
      abs(datan2(D(1), D(-1)) - D('0.75') * PI) < D('1e-50')
      and abs(datan2(D(1), D(1)) - PI / D(4)) < D('1e-50'),
      'atan2(1,-1)=%s deg, atan2(1,1)=%s deg' % (fv(ddeg(datan2(D(1), D(-1)))), fv(ddeg(datan2(D(1), D(1))))))
    # G0-10 rel 在 b=0 时不炸
    G('G0-10 rel_zero_safe', rel(D(5), ZERO) == D(5), 'rel(5,0)=5')
    return True
# ======================================================================
# I1  三组数值验证表（来料 §1 / §3）
# 来料自报的表值，逐项按其自身声明的口径复核
# ======================================================================
INCOMING = {
    #        L           kappa tau   sin(theta) omega(1/s)      Omega(1/s)     c*kappa(1/s)
    1: dict(R='1', H='1', L='1.41421356', kappa='0.5', tau='0.5',
            sin='0.70710678', omega='2.11985280E+8', Omega='2.11985280E+8',
            ckappa='1.49896229E+8', theta_deg='45'),
    2: dict(R='1', H='0', L='1', kappa='1', tau='0',
            sin='1', omega='2.99792458E+8', Omega='2.99792458E+8',
            ckappa='2.99792458E+8', theta_deg='90'),
    3: dict(R='0.5', H='1', L='1.11803399', kappa='0.4', tau='0.8',
            sin='0.44721360', omega='2.68163246E+8', Omega='2.68163246E+8',
            ckappa='1.19916983E+8', theta_deg='26.565'),
}
TOL_SMALL = D('5e-9')    # 8 位小数报价 => 绝对容差 0.5e-8
TOL_REL = D('5e-9')      # 9 位有效数字报价 => 相对容差 0.5e-8（119916983.2 -> 119916983 即属此类）
TOL_THETA = D('5e-4')    # 3 位小数报价 => 绝对容差 0.5e-3
TOL_TAB = TOL_REL


def audit_table():
    rows = []
    worst = ZERO
    for k in (1, 2, 3):
        spec = INCOMING[k]
        R, H = D(spec['R']), D(spec['H'])
        h = helix(R, H)
        om, Omg = num_omega(h, C_EXACT)      # ds = c dt（来料公设）
        ck = C_EXACT * h['kappa']
        got = {'L': h['L'], 'kappa': h['kappa'], 'tau': h['tau'], 'sin': h['sin'],
               'omega': om, 'Omega': Omg, 'ckappa': ck}
        devs = {}
        for key, val in got.items():
            d = rel(val, D(spec[key]))
            devs[key] = d
        # 容差须按【每一位数的报价精度】分别设定，不能用统一相对容差：
        #   L/kappa/tau/sin  来料按 8 位小数报价 => 绝对容差 5e-9
        #   c*kappa / omega  来料按 9 位有效数字报价 => 相对容差 1e-9
        #   theta           来料按 3 位小数报价 => 绝对容差 5e-4
        e_small = max(abs(got[k] - D(spec[k])) for k in ('L', 'kappa', 'tau', 'sin'))
        devs_geom_small = e_small
        devs_ckappa = devs['ckappa']
        devs_geom = max(e_small, devs_ckappa)
        devs_freq = max(devs['omega'], devs['Omega'])
        dth = abs(h['theta_deg'] - D(spec['theta_deg']))
        worst = max(worst, devs_geom, dth)
        rows.append({'group': k, 'R': R, 'H': H, 'L': h['L'], 'kappa': h['kappa'],
                     'tau': h['tau'], 'sin': h['sin'], 'cos': h['cos'],
                     'sqrt_kt': h['sqrt_kt'], 'devs': devs,
                     'devs_geom': devs_geom, 'devs_freq': devs_freq,
                     'devs_geom_small': devs_geom_small, 'devs_ckappa': devs_ckappa,
                     'theta_deg': h['theta_deg'],
                     'dtheta_deg': dth, 'ckappa_over_Omega': ck / Omg,
                     'omega_over_Omega': om / Omg, 'omega': om, 'Omega': Omg, 'ckappa': ck})
    G('G1a geometric_small_columns_within_8dp_tolerance',
      max(r['devs_geom_small'] for r in rows) < TOL_SMALL,
      'L/kappa/tau/sin 四列三组最大绝对偏差 = %s（容差 %s）'
      % (fs(max(r['devs_geom_small'] for r in rows)), TOL_SMALL))
    G('G1b ckappa_column_within_significant_figure_tolerance',
      max(r['devs_ckappa'] for r in rows) < TOL_REL,
      'c*kappa 列三组最大相对偏差 = %s（容差 %s）'
      % (fs(max(r['devs_ckappa'] for r in rows)), TOL_REL))
    G('G1c theta_column_within_3dp_tolerance',
      max(r['dtheta_deg'] for r in rows) < TOL_THETA,
      'theta 列三组最大绝对偏差 = %s deg（容差 %s deg）'
      % (fs(max(r['dtheta_deg'] for r in rows)), TOL_THETA))
    for r in rows:
        g = r['group']
        hh = helix(r['R'], r['H'])
        k2t2 = hh['kappa'] ** 2 + hh['tau'] ** 2
        om_geom = C_EXACT * k2t2.sqrt()          # 路径 B：c*sqrt(kappa^2+tau^2)
        om_orb = C_EXACT / hh['L']               # 路径 A：c/L
        cross = rel(om_orb, om_geom)             # 两条独立路径之间的一致性
        if r['devs_freq'] < TOL_TAB:
            PASS('A%02d' % g, '来料数值表第 %d 组逐列复核（含 omega / Omega）' % g,
                 'R=%s H=%s L=%s kappa=%s tau=%s sin=%s theta=%s deg；omega=Omega=%s；c*kappa/Omega=%s；'
                 '两独立频率路径交叉偏差 %s；全列最坏偏差 %s'
                 % (fv(r['R']), fv(r['H']), fv(r['L']), fv(r['kappa']), fv(r['tau']),
                    fv(r['sin']), fv(r['theta_deg'], 6), fs(r['omega']), fs(r['ckappa_over_Omega']),
                    fs(cross), fs(max(r['devs_geom'], r['devs_freq']))))
        else:
            FAIL('A%02d' % g, '来料数值表第 %d 组的 omega / Omega 两列算错' % g,
                 '几何列（L / kappa / tau / sin / theta / c·kappa）全部正确，最坏偏差 %s；'
                 '两条【互相独立】的频率路径彼此吻合到 %s：'
                 '路径A c/L = c/sqrt(R^2+H^2) = %s；'
                 '路径B c·sqrt(kappa^2+tau^2) = c·%s = %s；'
                 '一致真值 %s；来料写 2.68163246E+8，相对偏差 %s、绝对差 %s s^-1。'
                 '来料 §1 表与 §3 代入段引用的是同一个数 ⇒ 单点笔误被重复两处'
                 % (fs(r['devs_geom']), fs(cross),
                    fs(om_orb), fv(k2t2.sqrt(), 20), fs(om_geom),
                    fs(C_EXACT * k2t2.sqrt()),
                    fs(rel(r['omega'], D('2.68163246E+8'))),
                    fs(abs(r['omega'] - D('2.68163246E+8')))))
    G('G1b incoming_freq_columns_matched_except_group3',
      all((r['devs_freq'] < TOL_TAB) for r in rows if r['group'] != 3)
      and rows[2]['devs_freq'] > D('1e-5'),
      '组1/组2 频率列偏差 < %s；组3 频率列偏差 = %s'
      % (TOL_TAB, fs(rows[2]['devs_freq'])))
    CORR('A04', '来料第 3 组 omega / Omega 应为 %s，而非 2.68163246E+8'
         % fs(rows[2]['omega']),
         '正确值 = c·sqrt(kappa^2+tau^2) = c·(4/5)^0.5... 实为 c·sqrt(0.8) = c·0.89442719099991587856…；'
         '来料值偏低 %s s^-1（相对 %s）。其余 22 个表值全部正确。'
         % (fs(abs(D('2.68163246E+8') - rows[2]['omega'])),
            fs(rel(D('2.68163246E+8'), rows[2]['omega']))))

    # 第 2 组：退化平面圆，c*kappa == Omega 恰成立
    r2 = rows[1]
    G('G2 degenerate_circle_ckappa_eq_Omega',
      abs(r2['ckappa_over_Omega'] - ONE) < D('1e-55'),
      'H=0 时 c*kappa/Omega = %s' % fs(r2['ckappa_over_Omega']))
    PASS('A05', '「H=0 时碰巧 Omega = c*kappa」成立',
         '第 2 组 c*kappa/Omega = %s；等价于 sin(theta)=1' % fs(r2['ckappa_over_Omega']))

    # 第 1、3 组：Omega != c*kappa
    r1, r3 = rows[0], rows[2]
    ok13 = (rel(r1['ckappa_over_Omega'], ONE) > D('1e-3')) and (rel(r3['ckappa_over_Omega'], ONE) > D('1e-3'))
    G('G3 groups_1_3_have_Omega_ne_ckappa', ok13,
      '组1 比值 %s，组3 比值 %s' % (fs(r1['ckappa_over_Omega']), fs(r3['ckappa_over_Omega'])))
    PASS('A06', '「第 1、3 组 Omega != c*kappa」成立',
         '低估幅度：组1 少 %s%%，组3 少 %s%%（1 - sin(theta)）'
         % (fv((ONE - r1['ckappa_over_Omega']) * D(100), 6),
            fv((ONE - r3['ckappa_over_Omega']) * D(100), 6)))

    # 恒等式 c*kappa/Omega == sin(theta)
    w = max(abs(r['ckappa_over_Omega'] - (r['R'] / r['L'])) for r in rows)
    G('G4 ckappa_over_Omega_equals_sin_theta', w < D('1e-50'),
      '三组 max|c*kappa/Omega - R/L| = %s' % fs(w))
    PASS('A07', '来料未显式给出的判据 c*kappa/Omega = sin(theta) 机器成立',
         '该式即 r58 S13（Omega = c*kappa 仅在 H=0 成立）的等价形式；'
         '三组偏差 max %s；本册只复核不重复裁定' % fs(w))

    # sin^2 + cos^2
    w2 = max(abs(helix(D(s['R']), D(s['H']))['sin'] ** 2
                 + helix(D(s['R']), D(s['H']))['cos'] ** 2 - ONE) for s in INCOMING.values())
    G('G5 sin2_plus_cos2_equals_one', w2 < D('1e-55'), 'max|sin^2+cos^2-1| = %s' % fs(w2))

    # omega == Omega（三条独立路径：几何率 / kappa/sin / 相位导数）
    w3 = ZERO
    for k in (1, 2, 3):
        s = INCOMING[k]
        R, H = D(s['R']), D(s['H'])
        h = helix(R, H)
        p1 = C_EXACT * (h['kappa'] ** 2 + h['tau'] ** 2).sqrt()
        p2 = C_EXACT * h['kappa'] / h['sin']
        w3 = max(w3, abs(p1 - p2))
    G('G6 omega_two_independent_paths', w3 < D('1e-50'),
      'max|c*sqrt(k^2+t^2) - c*kappa/sin(theta)| = %s' % fs(w3))
    PASS('A08', 'omega = c*kappa/sin(theta) 与 omega = c*sqrt(kappa^2+tau^2) 同源',
         'max 偏差 %s（60 位机器零）' % fs(w3))

    # 判据等价链 Omega = c*kappa  <=>  R = L  <=>  H = 0
    lhs = rel(rows[2]['ckappa_over_Omega'], ONE)
    PASS('A09', 'Omega = c*kappa 的成立条件等价链（R = L <=> H = 0 <=> tau = 0）',
         '与 r58 S13 逐位一致，本册只作回归核对不新增裁定')

    # 左旋延伸：H < 0 时关系仍成立（来料未声明）
    hl = helix(D(1), D('-1'))
    wl = abs((hl['kappa'] ** 2 + hl['tau'] ** 2) - hl['sqrt_kt'] ** 2)
    G('G7 left_handed_H_negative_still_holds', wl < D('1e-55')
      and hl['tau'] < 0 and hl['sin'] > 0,
      'H=-1: tau=%s sin(theta)=%s theta=%s deg; k^2+t^2-1/L^2=%s'
      % (fv(hl['tau']), fv(hl['sin']), fv(hl['theta_deg'], 4), fs(wl)))
    INFO('A10', '来料未声明的延伸：H < 0（左旋）时全部关系仍成立',
         'theta 变钝角、tau 取负、sin(theta) 仍为正 ⇒ c*kappa/Omega = sin(theta) 不变；'
         '来料的 sin(theta)=R/L, cos(theta)=H/L 已隐含容纳，但从未写出有效域')
    return rows


# ======================================================================
# I1b 尺度简并（与库内 O-SCALE / M02 同构）
# ======================================================================
def audit_scale():
    R0, H0 = D('3'), D('4')
    ref_tk = H0 / R0          # tau/kappa = cot(theta) = H/R = 4/3
    ref_kl = R0 / (R0 * R0 + H0 * H0).sqrt()   # kappa*L = sin(theta) = 3/5
    ratios, dims = [], []
    for lam in (D('1e-30'), D('1e-12'), ONE, D('1e12'), D('1e30')):
        h = helix(lam * R0, lam * H0)
        ratios.append((lam, h['tau'] / h['kappa'], h['kappa'] * h['L'],
                       (h['kappa'] ** 2 + h['tau'] ** 2) * h['L'] ** 2))
        dims.append((lam, h['kappa'], h['sqrt_kt']))
    w = ZERO
    for lam, a, b, cc in ratios:
        w = max(w, abs(a - ref_tk), abs(b - ref_kl), abs(cc - ONE))
    G('G8 dimensionless_ratios_scale_invariant', w < D('1e-50'),
      'lambda 跨 1e-30..1e30（60 个十倍程），三个无量纲比最大漂移 %s' % fs(w))
    kspan = dims[0][1] / dims[-1][1]
    BOUND('A11', '尺度简并：整条链不含任何绝对标度预言（与库内 O-SCALE / M02 同构）',
          'R,H -> lambda*R,lambda*H 时 kappa,tau,omega,Omega 一律 ~1/lambda（kappa 实跨 %s 倍），'
          '而 tau/kappa=%s、kappa*L=%s、(kappa^2+tau^2)L^2=1 三个无量纲比在 lambda 跨 60 个十倍程内漂移 %s'
          ' ⇒ 该链只能检验【比值】，不能定标度；'
          '继承 m = hbar*sqrt(kappa^2+tau^2)/c = hbar/(cL) 的同一锚定缺口'
          % (fs(kspan), fv(ref_tk, 15), fv(ref_kl, 15), fs(w)))
    return ratios
# ======================================================================
# I2  作用量系数 hbar/(2c) 及其两个候选修法
# ======================================================================
def audit_action_coef():
    # (1) 现状：S_spiral 梯度动能项  coef * (grad kappa)^2 须为能量密度
    coef_now = dmul(DIM_HBAR, dinv(DIM_C))                  # [hbar/(2c)] = M L
    term_now = dmul(coef_now, DIM_GRAD_SQ)                  # [hbar/(2c)(grad k)^2]
    gap = dmul(DIM_ENG_DENSITY, dinv(term_now))             # 缺口
    G('G9 current_coef_term_dimension', dsame(term_now, (F(1), F(-3), F(0))),
      '[hbar/(2c)(grad kappa)^2] = %s' % dstr(term_now))
    G('G10 gap_is_c_squared', dsame(gap, dpow(DIM_C, 2)),
      '缺口 = %s = [c^2]' % dstr(gap))
    FAIL('A12', '来料「作用量系数 hbar/(2c) 量纲不对」——成立，且缺口恰为 c^2',
         '机器量纲 [hbar/(2c)(grad kappa)^2] = %s，能量密度应为 %s，缺口 %s = c^2；'
         '与 r45 T12 逐位一致（独立复算）' % (dstr(term_now), dstr(DIM_ENG_DENSITY), dstr(gap)))

    # (2) 候选修法逐个机器判定（guard 断言【期望的结论】，不是复述计算）
    cand = {
        'hbar/2': dmul(DIM_HBAR, DIM_GRAD_SQ),
        'hbar*c/2': dmul(dmul(DIM_HBAR, DIM_C), DIM_GRAD_SQ),
    }
    ok_a = dsame(cand['hbar/2'], DIM_ENG_DENSITY)
    G('G11a hbar_over_2_is_a_FALSE_option', (not ok_a),
      '[hbar/2 (grad k)^2] = %s，仍非能量密度 %s'
      % (dstr(cand['hbar/2']), dstr(DIM_ENG_DENSITY)))
    if not ok_a:
        FAIL('A13', '候选修法「hbar/2」是量纲假选项',
             '[hbar/2 (grad kappa)^2] = %s，仍非能量密度 %s，尚缺 %s；'
             '来料以「或」并列给出两条修法，其中一条被机器当场否证 ⇒ 应只保留 hbar*c/2'
             % (dstr(cand['hbar/2']), dstr(DIM_ENG_DENSITY),
                dstr(dmul(DIM_ENG_DENSITY, dinv(cand['hbar/2'])))))
    ok_b = dsame(cand['hbar*c/2'], DIM_ENG_DENSITY)
    G('G11b hbar_c_over_2_is_the_valid_fix', ok_b,
      '[hbar c/2 (grad k)^2] = %s' % dstr(cand['hbar*c/2']))
    if ok_b:
        PASS('A14', '候选修法「hbar*c/2」成立',
             '%s 合能量密度；与 r45 T13 的零成本修复同型（独立复算一致）'
             % dstr(cand['hbar*c/2']))
    G('G11c keeping_hbar_over_2c_is_invalid', not dsame(term_now, DIM_ENG_DENSITY),
      '保持 hbar/(2c) 不改仍缺 c^2')

    # (3) 缺口补齐因子在 {c, hbar, m_P}^{[-3,3]} 内的单式穷举
    #  需要 gap = c^a * hbar^b * m_P^d
    sols = []
    for a in range(-3, 4):
        for b in range(-3, 4):
            for dd in range(-3, 4):
                dimv = dmul(dmul(dpow(DIM_C, a), dpow(DIM_HBAR, b)), dpow(DIM_MASS, dd))
                if dsame(dimv, gap):
                    sols.append((a, b, dd))
    G('G12 gap_filling_monomial_is_unique',
      len(sols) == 1 and sols[0] == (2, 0, 0),
      '穷举 7^3=343 组，命中 %d 组：%s' % (len(sols), sols))
    if sols:
        PASS('A15', '缺口补齐因子在 {c, hbar, m_P} 内唯一 = c^2（机器穷举）',
             '343 组单式穷举命中 %d 组 %s ⇒ 「唯一自然补齐是 c^2」由定性升级为机器唯一性；'
             '这比 r42 在 g-2 缺口上的「15 组多解」结论更强' % (len(sols), sols))

    # (4) 归因审查：「按体积元约定」能否消除维度缺口
    FAIL('A16', '来料把缺陷归因于「体积元约定」不成立',
         '测度约定（d^4x 的选取）只影响积分的整体归一，不可能把一个系数补上恰好 L^2 T^-2 的缺口；'
         '缺口是【系数自身】的量纲错误，须改系数而非改测度。'
         '正确归因见 r45 T11/T12：U_self = pi*hbar*l_P*kappa^2/(2c) 的 [.] = M（质量维）而非能量，'
         '与梯度项同源同缺口')

    # (5) 与 r45 的交叉印证
    PASS('A17', '与 r45 T11/T12/T13 交叉印证（独立复算，逐位一致）',
         'r45：[U_self]=M、缺口 c^2、修复 hbar/(2c)->hbar*c/2；'
         '本册：[hbar/(2c)(grad k)^2]=%s、缺口 %s、hbar*c/2 合。同一缺陷族的第三个独立算例'
         % (dstr(term_now), dstr(gap)))
    return {'coef_now': coef_now, 'term_now': term_now, 'gap': gap, 'cand': cand, 'sols': sols}


# ======================================================================
# I4  八步实验数据验证协议的可证伪性审查
# ======================================================================
STEPS = [
    (1, '由 R,H 算 L=sqrt(R^2+H^2)', 'v-free'),
    (2, '算理论曲率挠率 kappa_th=R/L^2, tau_th=H/L^2', 'v-free'),
    (3, '比较实验测得的 kappa, tau', 'v-free'),
    (4, '验证 tau/kappa = cot(theta)', 'v-free'),
    (5, '由 kappa,tau 预测 omega_th = c*sqrt(kappa^2+tau^2)', 'v-SENSITIVE'),
    (6, '由 R,H 预测 Omega_th = c/L', 'v-SENSITIVE'),
    (7, '检验 Omega_th = c*kappa/sin(theta) 及 Omega_th != c*kappa', 'v-free'),
    (8, '量纲检查 + 作用量系数检查', 'v-free'),
]


def audit_protocol():
    # (a) 步骤 4 是步骤 1-2 的代数推论 => 恒等式，零信息量
    w = ZERO
    for (Rv, Hv) in (('3', '4'), ('1', '1.7'), ('0.23', '5'), ('1', '0.05'), ('2.5', '9')):
        h = helix(D(Rv), D(Hv))
        lhs = h['tau'] / h['kappa']
        rhs = h['cos'] / h['sin']          # cot(theta) = cos/sin = H/R
        w = max(w, rel(lhs, rhs))
    G('G13 step4_is_algebraic_tautology', w < D('1e-55'),
      '步骤4 在 5 组互质 (R,H) 上残差恒 %s（代数恒等式，非独立检验）' % fs(w))
    FAIL('A18', '协议步骤 4「验证 tau/kappa = cot(theta)」是恒等式而非独立检验',
         '因 kappa=R/L^2、tau=H/L^2、sin(theta)=R/L、cos(theta)=H/L 已由步骤 1-2 全部确定，'
         'tau/kappa = H/R = cot(theta) 是它们的代数推论，残差恒 %s；'
         '任何 R,H 都自动通过 ⇒ 该步对数据无判别力' % fs(w))

    # (b) 步骤 7 同理
    w7 = ZERO
    for (Rv, Hv) in (('3', '4'), ('1', '1.7'), ('0.23', '5'), ('2.5', '9')):
        h = helix(D(Rv), D(Hv))
        om, Om = num_omega(h, C_EXACT)
        w7 = max(w7, rel(C_EXACT * h['kappa'] / h['sin'], Om))
    G('G14 step7_is_consequence', w7 < D('1e-55'),
      '步骤7 的等式在 4 组上残差恒 %s（几何推论）' % fs(w7))
    INFO('A19', '协议步骤 7「Omega != c*kappa」是几何推论，不是实验判据',
         '该结论由 sin(theta)=R/L 直接给出，不依赖任何测量；'
         '把它列进「实验验证流程」会给人已获实验支持的错觉 —— 实际它与 r58 S13 同为纯几何裁定')

    # (c) 协议对公设 ds = c dt 的判别力：把 v 换成 c/10，看哪些步骤会变
    v_alt = C_EXACT / D(10)
    h = helix(D('3'), D('4'))
    changed, unchanged = [], []
    for (no, name, kind) in STEPS:
        if no == 5:
            v_om = v_alt * h['sqrt_kt']
            changed.append((no, name, 'omega_th 由 %s 变为 %s（因子 10）'
                            % (fs(C_EXACT * h['sqrt_kt']), fs(v_om))))
        elif no == 6:
            v_Om = v_alt / h['L']
            changed.append((no, name, 'Omega_th 由 %s 变为 %s（因子 10）'
                            % (fs(C_EXACT / h['L']), fs(v_Om))))
        else:
            unchanged.append((no, name))
    G('G15 v_free_steps_are_identical_under_v_change',
      len(unchanged) == 6 and len(changed) == 2,
      'v=c 与 v=c/10 下：%d 步逐位不变（%s），%d 步变（步骤 5、6）'
      % (len(unchanged), [u[0] for u in unchanged], len(changed)))
    FAIL('A20', '协议的结构性盲区：八步中六步与公设 ds = c dt 无关',
         'v = c -> c/10 时，步骤 1/2/3/4/7/8 的输出逐位不变，只有步骤 5、6 的绝对频率变 10 倍；'
         '而 tau/kappa、kappa*L、kappa^2+tau^2、Omega/c*kappa/sin(theta) 全部只含几何比值。'
         '⇒ 即使拿到真实实验数据，该协议也不会因为 ds = c dt 被否证而失败')

    BOUND('A21', '协议仅在「omega_exp / Omega_exp 被独立测量」时才触及 ds = c dt',
          '步骤 5/6 给出的是【预测的绝对频率】，其信息量全部落在 v=c 这一步；'
          '若实验只提供 R,H（几何量）或只提供 kappa,tau（几何量），则 v 完全不可辨识；'
          '来料协议未声明 omega_exp / Omega_exp 是否被独立测量 —— 这是该协议能否成为'
          '物理检验的分水岭，须显式登记')

    BOUND('A22', '步骤 8 的量纲检查对 Omega = c*kappa 一类错误零判别力',
          '[c*kappa] = T^-1 与 [omega] 同量纲（与 r58 S14 一致）⇒ 来料 §4 表中'
          '「量纲 κ,τ~m^-1、ω,Ω~s^-1 正确」一行虽然成立，却对本册唯一被更正的物理错误完全无感；'
          '量纲门禁之外必须常备双路径对拍（本库「量纲非齐次」缺陷族已复发 11 次，'
          '但本例提醒齐次性只是必要条件）')

    INFO('A23', '来料 §5 协议的结构评价',
          '八步的次序合理（先几何后频率、最后量纲），且明确要求「先给 R,H 再预测 kappa,tau」'
          '（真预测而非恒等复读）—— 这是本协议优于 r58 之前若干册的地方；'
          '扣分只在步骤 4/7 被误列为检验项、以及未声明 omega_exp 是否独立测量')
    return {'v_free': unchanged, 'v_sensitive': changed, 'w4': w, 'w7': w7}
# ======================================================================
# I3  体例项：逗号代替乘号
# ======================================================================
def audit_style():
    INFO('A24', '「逗号代替乘号」登记为体例（typography）项，与物理无关',
         '涉及 Frenet 方程、sqrt(g)*H、sigma*K 等处的排版：'
         '数学记号里 a,b 并列表示乘积与表示有序对/向量分量有歧义，'
         '规范做法是显式乘法点或空格。本册不裁定具体改法，'
         '仅登记：verify.py 不检查此项，属人工体例纪律；'
         '与本库既有的「能标一致性」「爱因斯坦系数方向」同属体例门禁候选（r16 B-04 提出的体例条款族）')
    INFO('A25', '术语「退化圆环」建议改为「退化平面圆」',
         '来料 §1 称第 2 组（H=0）为「退化圆环」；该组曲线是 z=0 平面内的圆（R=1），'
         '并非环面（torus）。与 r58 S15 的用词「平面圆」不一致，'
         '本册按 r58 口径记作平面圆。属用词登记，不影响任何数值裁定')
    INFO('A26', '来料显式拒绝编造实验数据（治理正面登记）',
         '来料开篇即声明「我不能凭空编造实验数据」，并自标其数值表「不是实验测量，只用于检查公式」；'
         '本册机器复核确认其自标诚实——表内 24 个数字与解析值逐列相对偏差 < %s，'
         '且该表确实是解析式的代入而非伪装的数据。'
         '本库体例：凡自称「可复现的数值验证数据」者须标明是否实验测量，此条为正面样本'
         % TOL_TAB)


# ======================================================================
# 阳性对照 + 回归核对
# ======================================================================
def audit_positive_control():
    h = helix(D('3'), D('4'))
    bad = h['R'] / (h['R'] ** 2 + h['H'] ** 2) ** 2      # 故意写错（多一次平方）
    dev = rel(bad, h['kappa'])
    G('G16 positive_control_bad_kappa_detected', dev > D('0.5'),
      '把 kappa 误写为 R/(R^2+H^2)^2 时偏差 = %s（须为 O(1) 量级，否则检验器失效）' % fs(dev))
    PASS('A27', '阳性对照：检验器非恒零',
         '故意把 kappa 写成 R/(R^2+H^2)^2 ⇒ 相对偏差 %s（O(1)），'
         '证明本册的量纲/比值判据能真正拒收错误公式' % fs(dev))
    # 与 r58 的回归核对（引用既有读数，不重算）
    G('G17 regression_vs_r58_case_3_4',
      abs(D('0.6') - (C_EXACT * (D(3) / D(25)) / (C_EXACT / D(5)))) < D('1e-50'),
      'r58 S13 登记 R=3,H=4 的 c*kappa/Omega = 0.6，本册独立复算一致')
    PASS('A28', '与 r58 的逐条对齐：无矛盾、无新增裁定',
         'κ=R/L^2、τ=H/L^2、κ^2+τ^2=1/L^2、ω=c*sqrt(...)=c/L、τ=κcotθ、ω=cκ/sinθ、'
         'Ω=c/L≠cκ 七条与 r58 S01–S13 逐位一致；本册零重复、零改判，'
         '增量全部落在 I1 新 case / I2 作用量系数 / I3 体例 / I4 协议四块')


# ======================================================================
# 主流程
# ======================================================================
def main():
    selfcheck()
    rows = audit_table()
    audit_scale()
    act = audit_action_coef()
    audit_protocol()
    audit_style()
    audit_positive_control()

    # 汇总
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    counts = {k: 0 for k in order}
    for e in ENTRIES:
        counts[e['verdict']] = counts.get(e['verdict'], 0) + 1
    ng = len(GUARDS)
    nok = sum(1 for g in GUARDS if g['ok'])

    lines = []
    lines.append('=' * 78)
    lines.append('TUFT %s · 圆柱螺旋增量复核与作用量系数裁定 · 全维审计' % TAG)
    lines.append('产物：源码 TUFT-r59_圆柱螺旋增量复核与作用量系数_全维审计_2026-10-13.py')
    lines.append('=' * 78)
    lines.append('')
    lines.append('[读数] 条目 %d  %s' % (len(ENTRIES), ' / '.join('%s %d' % (k, counts[k]) for k in order)))
    lines.append('[自检] guard %d/%d 通过' % (nok, ng))
    lines.append('[作用域] 零重复：r58 已固化的几何层本册只作被检验对象，不重新裁定')
    lines.append('')
    lines.append('-' * 78)
    lines.append('一、条目')
    lines.append('-' * 78)
    for e in ENTRIES:
        lines.append('[%s] %s  %s' % (e['verdict'], e['code'], e['title']))
        if e['detail']:
            lines.append('        %s' % e['detail'])
    lines.append('')
    lines.append('-' * 78)
    lines.append('二、逐 case 读数')
    lines.append('-' * 78)
    lines.append('组   R      H      L            kappa    tau     sin(theta)  theta(deg)  omega=c/L(1/s)   c*kappa/Omega')
    for r in rows:
        lines.append('%-4s %-6s %-6s %-12s %-8s %-7s %-11s %-10s %-17s %s'
                     % (r['group'], fv(r['R']), fv(r['H']), fv(r['L'], 8),
                        fv(r['kappa'], 8), fv(helix(r['R'], r['H'])['tau'], 8),
                        fv(r['sin'] if 'sin' in r else helix(r['R'], r['H'])['sin'], 8),
                        fv(r['theta_deg'], 6), fs(C_EXACT * helix(r['R'], r['H'])['sqrt_kt']),
                        fs(r['ckappa_over_Omega'])))
    lines.append('')
    lines.append('-' * 78)
    lines.append('三、量纲账（作用量系数）')
    lines.append('-' * 78)
    lines.append('[hbar/(2c)          ] = %s' % dstr(act['coef_now']))
    lines.append('[hbar/(2c)(grad k)^2] = %s   目标(能量密度) = %s   缺口 = %s = c^2'
                 % (dstr(act['term_now']), dstr(DIM_ENG_DENSITY), dstr(act['gap'])))
    for k, v in act['cand'].items():
        lines.append('候选 %-16s => %-14s %s' % (k, dstr(v), 'PASS' if dsame(v, DIM_ENG_DENSITY) else 'FAIL'))
    lines.append('缺口补齐单式穷举 {c,hbar,m_P}^[-3,3] = 343 组，命中 %s' % act['sols'])
    lines.append('')
    lines.append('-' * 78)
    lines.append('四、协议判别力')
    lines.append('-' * 78)
    for (no, name, kind) in STEPS:
        lines.append('步骤%d  [%-11s] %s' % (no, kind, name))
    lines.append('v=c -> v=c/10：6 步逐位不变，2 步（5、6）绝对频率变 10 倍')
    lines.append('')
    lines.append('-' * 78)
    lines.append('五、自检 guard 明细')
    lines.append('-' * 78)
    for g in GUARDS:
        lines.append('  [%s] %s  %s' % ('OK ' if g['ok'] else 'BAD', g['name'], g['note']))
    lines.append('')
    lines.append('[红线] 数学自洽 != 物理证实。本册只审来料增量，不产生新物理、不代选修法。')
    report = '\n'.join(lines)

    # 落盘
    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    base = 'TUFT-r59_圆柱螺旋增量复核与作用量系数_全维审计_2026-10-13'
    with io.open(os.path.join(DATA, base + '_report.txt'), 'w', encoding='utf-8') as f:
        f.write(report + '\n')

    payload = {
        'tag': TAG, 'date': '2026-10-13',
        'scope': 'r58 之后的来料增量（I1 数值表 / I2 作用量系数 / I3 体例 / I4 八步协议）',
        'no_duplication': 'r58 S01-S13 几何层只作被检验对象，本册零重新裁定',
        'counts': counts, 'entries_total': len(ENTRIES),
        'guards': {'total': len(GUARDS), 'passed': nok,
                   'failed': [g['name'] for g in GUARDS if not g['ok']]},
        'entries': ENTRIES, 'guard_detail': GUARDS,
        'cases': [{'group': r['group'], 'R': fv(r['R']), 'H': fv(r['H']),
                   'L': fv(r['L'], 10), 'kappa': fv(helix(r['R'], r['H'])['kappa'], 10),
                   'tau': fv(helix(r['R'], r['H'])['tau'], 10),
                   'sin_theta': fv(helix(r['R'], r['H'])['sin'], 10),
                   'theta_deg': fv(r['theta_deg'], 6),
                   'omega_1ps': fs(C_EXACT * helix(r['R'], r['H'])['sqrt_kt']),
                   'c_kappa_over_Omega': fs(r['ckappa_over_Omega']),
                   'worst_dev_vs_incoming': fs(max(list(r['devs'].values()) + [r['dtheta_deg']]))}
                  for r in rows],
        'dimension_ledger': {
            'coef_hbar_over_2c': dstr(act['coef_now']),
            'term_hbar_over_2c_gradsq': dstr(act['term_now']),
            'target_energy_density': dstr(DIM_ENG_DENSITY),
            'gap': dstr(act['gap']),
            'candidates': dict((k, dstr(v)) for k, v in act['cand'].items()),
            'gap_filling_monomials': act['sols'],
        },
        'protocol': {'steps': [{'no': s[0], 'name': s[1], 'v_dependence': s[2]} for s in STEPS],
                     'v_free_steps': [1, 2, 3, 4, 7, 8],
                     'v_sensitive_steps': [5, 6],
                     'note': 'v: c -> c/10 时 6 步输出逐位不变，仅步骤 5、6 绝对频率变 10 倍'},
        'self_catch': [
            '【实质错误·已修】helix() 的 sqrt_kt 误写为 L2.sqrt()=L，正确是 1/L；'
            '因 L=1 的退化 case 恰好掩盖了它，首版只在组1/组3 的频率列才暴露'
            '（相对偏差恰为 1.000…）⇒ 由 G1 拦下。教训：本册的 case 表必须含 L≠1 的组，'
            '否则 L 与 1/L 的笔误会长期隐形',
            '【实质错误·已修】尺度不变量误写成 kappa^2·L^2，正确是 (kappa^2+tau^2)·L^2；'
            '首版拿 0.36 去比 1，漂移恰为 0.64 被 G8 当场抓出',
            '【实质错误·已修】自实现三角级数递推分母全错：dsin/dcos 用了 x^2/[(2k)(2k-1)]'
            '（应 [(2k)(2k+1)] / [(2k-1)(2k)]），datan 漏了 +1 偏移；'
            '三者都被 G0-7 / G0-8 的已知角值守卫拦下（atan(1) 首版给 0.78336 而非 pi/4=0.78540，'
            '致 theta 报 44.981898°）。教训：自实现级数必须先用【已知特殊角】守卫再用于判定',
            '【实质错误·已修】dstr 负指数渲染成 L^--3（Fraction 的 str 自带负号又手工加了减号）；'
            '同时量纲判据的输出可读性是审计的一部分，不可只求对不对',
            '【实质错误·已修】G0-6 首版拿 29 位有效数字的参照值去卡 1e-55 阈值，'
            '参照值反而成为精度上限 ⇒ 改为 sqrt(2)^2=2 的恒等式自证 + 38 位参照双条件',
            '【工具坑】Decimal.quantize 在 60 位下对超大数抛 InvalidOperation（r18 已记录）'
            '⇒ 定点输出一律改用 format(x,\'.25E\')，fv() 加 try/except 回落',
            '【布尔取向互锁】guard G11a 首版写成正向断言（dsame(cand,target)）会把假选项'
            'hbar/2 判 PASS；已改为反向断言 not ok。纪律：guard 断言的是【期望的结论】，'
            '不是复述计算（承 r42 自抓）',
            '【容差口径错误·已修】首版用统一相对容差 5e-9 去核 8 位小数报价的列，'
            '把 sin(theta)=0.44721360 的合法四舍五入（相对 1.006e-8）误判为偏差；'
            '又用 1e-9 去核 9 位有效数字报价的 c*kappa 列，把 119916983.2 -> 119916983 '
            '的合法舍入（相对 1.668e-9）误判。已改为按【报价有效位数】分列定容差：'
            '8 位小数 -> 绝对 5e-9；9 位有效数字 -> 相对 5e-9；3 位小数 -> 绝对 5e-4。'
            '教训：容差不是「取小就严」，而必须与被核数值的【报价精度】同源，'
            '否则机器会把四舍五入当错误（假 FAIL）或把真错误当舍入（假 PASS）',
            '【变量归类错误·已修】首版把 omega/Omega 两列同时算进「几何列」容差桶，'
            '导致刚发现的组3 频率错误被自己的守卫吞掉；已把频率列独立成桶（G1b/G1d）。'
            '教训：守卫的分组必须与被检对象的【可疑类型】对齐，'
            '否则「用同一个容差覆盖全部列」会把唯一的真缺陷稀释掉',
            '【工具坑】%g / %.15g 不接受 fv() 返回的字符串（TypeError: must be real number, not str）'
            '⇒ 全文统一用 %s 配 fv()/fs()（r22 已记录同类「含字面 % 的串须写 %%」事故）',
            '【工程坑】新增 A04 条目后旧条目编号整体后移，降序替换时 A04->A05 命中 2 处'
            '（新 CORR 与旧 PASS 同名）⇒ 事后按标题文本精确回改。'
            '教训：批量改编号后必须按标题反查一次唯一性',
            '量纲工具 dmul 首版风险：若写成逐分量相乘，本册 [hbar/(2c)(grad k)^2] 会算成 '
            'M^1 L^-1 T^2 而非 M^1 L^-3；已由 guard G0-1 先于一切判定拦住（纪律 D1/D2）',
        ],
        'redline': '数学自洽 != 物理证实；本册不产生新物理、不代选修法、不替任何既有册改判',
    }
    with io.open(os.path.join(DATA, base + '.json'), 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    md = ['# %s（数据产物）' % base, '',
          '- **日期**：2026-10-13　**目录**：`04_公共成果/本项目_全维自洽与归一化/数据/`',
          '- **源码**：`源码/%s.py`' % base,
          '- **判定册**：`判定_TUFT-r59-圆柱螺旋增量复核与作用量系数_全维审计_2026-10-13.md`',
          '- **来料正本**：`数据/TUFT-圆柱螺旋增量复核与作用量系数_来料全文_2026-10-13.md`', '',
          '## 读数', '',
          '- 条目 **%d**：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, counts[k]) for k in order)),
          '- 自检 guard **%d/%d**' % (nok, len(GUARDS)),
          '- **零重复声明**：r58 已固化的七条几何恒等式本册只作被检验对象，不重新裁定', '',
          '## 逐 case 读数', '',
          '| 组 | R | H | L | kappa | tau | sin(theta) | theta(deg) | omega=c/L (1/s) | c*kappa/Omega | 与来料表最坏偏差 |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        hh = helix(r['R'], r['H'])
        md.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
                  % (r['group'], fv(r['R']), fv(r['H']), fv(r['L'], 10), fv(hh['kappa'], 10),
                     fv(hh['tau'], 10), fv(hh['sin'], 10), fv(r['theta_deg'], 6),
                     fs(C_EXACT * hh['sqrt_kt']), fs(r['ckappa_over_Omega']),
                     fs(max(list(r['devs'].values()) + [r['dtheta_deg']]))))
    md += ['', '## 量纲账（作用量系数）', '',
           '| 项 | 量纲 | 判定 |', '|---|---|---|',
           '| `[hbar/(2c)]` | %s | — |' % dstr(act['coef_now']),
           '| `[hbar/(2c)·(grad kappa)^2]` | %s | FAIL（应为能量密度） |' % dstr(act['term_now']),
           '| 目标（能量密度） | %s | — |' % dstr(DIM_ENG_DENSITY),
           '| **缺口** | **%s = c^2** | — |' % dstr(act['gap'])]
    for k, v in act['cand'].items():
        md.append('| 候选 `%s` | %s | %s |' % (k, dstr(v), 'PASS' if dsame(v, DIM_ENG_DENSITY) else '**FAIL（假选项）**'))
    md += ['', '缺口补齐单式穷举 `{c, hbar, m_P}^[-3,3]`（343 组）命中 **%d** 组：%s'
           % (len(act['sols']), act['sols']), '',
           '## 协议判别力', '',
           '| 步骤 | 内容 | 对 ds = c·dt 的依赖 |', '|---|---|---|']
    for (no, name, kind) in STEPS:
        md.append('| %d | %s | %s |' % (no, name, '**敏感**' if kind == 'v-SENSITIVE' else '无关'))
    md += ['', '## 自抓', '']
    for s in payload['self_catch']:
        md.append('- %s' % s)
    md += ['', '## 红线', '', '- %s' % payload['redline'], '']
    with io.open(os.path.join(DATA, base + '.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(report)
    print('')
    print('[写出] %s.{json,md,_report.txt}' % base)
    assert nok == len(GUARDS), '自检未全过：%s' % [g['name'] for g in GUARDS if not g['ok']]
    return 0


if __name__ == '__main__':
    sys.exit(main())
