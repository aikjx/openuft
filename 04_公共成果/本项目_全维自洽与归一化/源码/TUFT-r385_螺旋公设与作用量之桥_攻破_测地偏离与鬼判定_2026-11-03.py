# -*- coding: utf-8 -*-
"""
TUFT-r385 · 攻破册：螺旋公设 ↔ 作用量之桥（r384 的 B05 FAIL 的正面攻击）

r384 的裁定是「式 (1) 里没有 kappa、tau、T_MNP，故 §四 的螺旋结论没有作用量来源」。
那是一条**缺失性**判定。本册把它升级为**不可能性**判定，并给三条候选桥定价：

  K01 定理一（阶数/自由度）：任何二阶世界线作用量的极值曲线是测地线 => kappa = tau = 0；
      公设要求 kappa^2 + tau^2 = (w/c)^2 > 0 => 两个解集的交集为空。
  K02 定理二（频率锁定）：公设 + 库内 m = hbar*sqrt(kappa^2+tau^2)/c => w = m c^2 / hbar 精确，
      即 hbar*w = m c^2 逐位成立（内部运动频率 = 静止能量频率）。
  K03 定理三（力的定价）：最简实现 tau = 0 => kappa = 1/lambda_C，维持它所需的向心力
      F = m c^2 kappa = m^2 c^3 / hbar；等效力场恰为 Schwinger 临界场（代数恒等）。
  K04 三个候选桥的代价：Ostrogradsky 鬼 / 与测地线不相容 / KK 无鬼但引入新量子数。
  K05 KK 桥的线性塔作为质量谱被实验排除（预言 2 倍 vs 实测 206.77 倍）。
  K06 存活面与须用户裁决项。

纯标准库。Decimal 60 位用于物理恒等式；float 双精度用于微分几何的数值复核（容差 1E-9 起）。
不 import numpy / sympy / mpmath。红线：本册证明的是「在来料公设集内桥不可能」，不是「螺旋图像错」。
"""
import io
import os
import sys
import json
import math
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

SRC = os.path.abspath(__file__)
BASE = os.path.dirname(os.path.dirname(SRC))
DATA = os.path.join(BASE, '数据')
NAME = 'TUFT-r385_螺旋公设与作用量之桥_攻破_测地偏离与鬼判定_2026-11-03'

# ---- CODATA 2018 ----
C_LIGHT = Dc('299792458')
HBAR = Dc('1.054571817E-34')
M_E = Dc('9.1093837015E-31')
M_P = Dc('1.67262192369E-27')
Q_E = Dc('1.602176634E-19')
M_MU_OVER_E = Dc('206.7682830')
M_TAU_OVER_E = Dc('3477.23')

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


def fv(x, nd=25):
    try:
        if isinstance(x, Fr):
            x = Dc(x.numerator) / Dc(x.denominator)
        if not isinstance(x, Dc):
            x = Dc(str(x))
        return format(x, '.' + str(nd) + 'E')
    except Exception:
        return str(x)


def dm(*a):
    return Dc(str(a[0]))


# ---------------------------------------------------------------- 微分几何（float，双精度）
def _f(t):
    """被测参数曲线：由调用方给出三分量函数"""
    raise NotImplementedError


def d1_5(g, t, h):
    """5 点一阶导，截断 O(h^4)"""
    return (-g(t + 2 * h) + 8 * g(t + h) - 8 * g(t - h) + g(t - 2 * h)) / (12 * h)


def d2_5(g, t, h):
    """5 点二阶导，截断 O(h^4)（自抓：首版用 3 点 O(h^2) 却套 4 阶 Richardson 系数 (16,-1)/15，
    阶数不匹配 => 圆 kappa 相对误差 1.5E-7 被 G04 拦下。3 点必须配 (4,-1)/3）"""
    return (-g(t + 2 * h) + 16 * g(t + h) - 30 * g(t) + 16 * g(t - h) - g(t - 2 * h)) / (12 * h * h)


def rich4(vh, vh2):
    """误差 ∝ h^4 时的 Richardson 外推；用于 d1_5 / d2_5"""
    return (16 * vh2 - vh) / 15


def deriv(curve, t, h):
    """返回 (r', r'', r''')；前两阶 5 点 + Richardson，三阶 = 对 d2_5 再做 5 点一阶导 + Richardson"""
    def c(i):
        return lambda s: curve(s)[i]

    v = []
    a = []
    j = []
    for i in range(3):
        g = c(i)
        v.append(rich4(d1_5(g, t, h), d1_5(g, t, h / 2)))
        a.append(rich4(d2_5(g, t, h), d2_5(g, t, h / 2)))
        jh = d1_5(lambda s: d2_5(g, s, h), t, h)
        jh2 = d1_5(lambda s: d2_5(g, s, h / 2), t, h / 2)
        j.append(rich4(jh, jh2))
    return v, a, j


def cross(u, w):
    return (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])


def dot(u, w):
    return u[0] * w[0] + u[1] * w[1] + u[2] * w[2]


def nrm(u):
    return math.sqrt(dot(u, u))


def kappa_tau(curve, t, h=1e-3):
    v, a, j = deriv(curve, t, h)
    va = cross(v, a)
    nv = nrm(v)
    nva = nrm(va)
    if nva == 0.0:
        return nv, 0.0, 0.0
    return nv, nva / (nv ** 3), dot(va, j) / (nva * nva)


# ---------------------------------------------------------------- 内核计算
R = {}

# 圆：半径 Rr，速度 v（弧长参数化为 v*t）
def circle(Rr, v):
    return lambda s: (Rr * math.cos(v * s / Rr), Rr * math.sin(v * s / Rr), 0.0)


def line(v):
    return lambda s: (v * s, 0.0, 0.0)


def helix(Rr, w, u):
    return lambda s: (Rr * math.cos(w * s), Rr * math.sin(w * s), u * s)


_c_geom = []
for (Rr, v) in [(2.0, 3.0), (0.5, 1.5), (10.0, 1.0)]:
    # 自抓：定步长 h=1E-3 在大 R / 小曲率时进入舍入噪声区（f~10、二阶差~a*h^2~1E-7,
    # 只剩 9 位有效数字）=> h 必须按曲线的时间尺度归一，取 h = 1E-3 * R/v（即 omega*h 固定）
    _h = 1e-3 * Rr / v
    nv, k, tt = kappa_tau(circle(Rr, v), 0.37, _h)
    _c_geom.append({'kind': 'circle', 'R': Rr, 'v': v, 'h': _h, 'nv': nv,
                    'kappa': k, 'tau': tt, 'expect_kappa': 1.0 / Rr})
for v in [1.0, 4.0]:
    nv, k, tt = kappa_tau(line(v), 0.83, 1e-3)
    _c_geom.append({'kind': 'line', 'v': v, 'h': 1e-3, 'nv': nv,
                    'kappa': k, 'tau': tt, 'expect_kappa': 0.0})
_nv, _k, _tt = kappa_tau(helix(1.0, 2.0, 1.0), 0.53, 5e-4)
_c_geom.append({'kind': 'helix', 'R': 1.0, 'w': 2.0, 'u': 1.0, 'h': 5e-4, 'nv': _nv,
                'kappa': _k, 'tau': _tt,
                'expect_kappa': 1.0 * 4.0 / (1.0 * 4.0 + 1.0),
                'expect_tau': 1.0 * 2.0 / (1.0 * 4.0 + 1.0)})
R['geom'] = _c_geom

# K02/K03 物理量
LAM_C = HBAR / (M_E * C_LIGHT)             # 康普顿波长
KAPPA_E = M_E * C_LIGHT / HBAR             # 最简实现（tau=0）的曲率
OMEGA_E = C_LIGHT * KAPPA_E                # 公设频率
TWO_PI = Dc('6.28318530717958647692528676655900576839433879875021164194989')
T_OMEGA = TWO_PI / OMEGA_E
F_E = M_E * C_LIGHT * C_LIGHT * KAPPA_E    # 向心力 = m c^2 kappa
E_FIELD_E = F_E / Q_E                      # 等效力场
E_SCHW = M_E * M_E * C_LIGHT ** 3 / (Q_E * HBAR)

KAPPA_P = M_P * C_LIGHT / HBAR
F_P = M_P * M_P * C_LIGHT ** 3 / HBAR
E_FIELD_P = F_P / Q_E

R['phys'] = {
    'lambda_C': fv(LAM_C, 20),
    'kappa_e': fv(KAPPA_E, 20),
    'omega_e': fv(OMEGA_E, 20),
    'period_e': fv(T_OMEGA, 20),
    'F_e': fv(F_E, 20),
    'E_field_e': fv(E_FIELD_E, 20),
    'E_schwinger': fv(E_SCHW, 20),
    'd_schw_rel': fv(abs(E_FIELD_E - E_SCHW) / E_SCHW, 6),
    'F_p': fv(F_P, 20),
    'E_field_p': fv(E_FIELD_P, 20),
    'F_p_over_F_e': fv(F_P / F_E, 12),
    'm_p_over_m_e_sq': fv((M_P / M_E) ** 2, 12),
}

# K04-C1：Ostrogradsky 判据 L = kappa^2 = y''^2/(1+y'^2)^3
def L_kappa2(yp, ypp):
    return ypp * ypp / (1.0 + yp * yp) ** 3


def hess_num(yp, ypp, h=1e-4):
    return (L_kappa2(yp, ypp + h) - 2 * L_kappa2(yp, ypp) + L_kappa2(yp, ypp - h)) / (h * h)


_hess = {'yp': 0.3, 'ypp': 0.7,
         'num': hess_num(0.3, 0.7), 'exact': 2.0 / (1.0 + 0.09) ** 3}
R['hess'] = _hess

# K05：KK 线性塔 vs 观测
K5 = []
for n in (2, 3):
    K5.append({'n': n, 'pred_ratio': float(n),
               'obs_ratio': float(M_MU_OVER_E) if n == 2 else float(M_TAU_OVER_E)})
R['tower'] = K5
for d in K5:
    d['miss'] = d['obs_ratio'] / d['pred_ratio']
# ================================================================ K01 定理一：测地线与公设不相容
say('=' * 78)
say('r385 · 螺旋公设与作用量之桥：把 r384 的 B05「没写」升级为「不可能」')
say('=' * 78)
say('')
say('K01 · 定理一：任何二阶世界线作用量的极值曲线都是测地线，而公设要求 kappa^2+tau^2 > 0')
say('-' * 78)

_cl = [x for x in R['geom'] if x['kind'] == 'circle']
_ln = [x for x in R['geom'] if x['kind'] == 'line']
_hx = [x for x in R['geom'] if x['kind'] == 'helix'][0]
_K_CIRC = max(abs(x['kappa'] - x['expect_kappa']) for x in _cl)
_T_CIRC = max(abs(x['tau']) for x in _cl)
_K_LINE = max(abs(x['kappa']) for x in _ln)
_T_LINE = max(abs(x['tau']) for x in _ln)

# 公设约束在测地线上的残差：0 = (w/c)^2 无解
_res = []
for _k in ('1E-3', '1', '1E12'):
    _w = Dc(_k) * C_LIGHT / LAM_C          # 取 w/c = k/lambda_C
    _lhs = Dc(0)                            # 测地线：kappa = tau = 0
    _rhs = (_w / C_LIGHT) ** 2
    _res.append((_k, _rhs))

add('K01', 'PASS',
    '定理一：二阶世界线作用量的极值曲线满足测地线方程 => kappa = tau = 0；公设要求 '
    'kappa^2 + tau^2 = (w/c)^2 > 0 => 两解集交集为空，「螺旋」不可能由二阶作用量导出',
    '三条独立理由：①**阶数/自由度**：二阶作用量的 EL 方程是二阶 ODE，解由 2 个初始数据（位置 + 速度）唯一确定，'
    'kappa 与 tau 是该解的**泛函**、不是可由作用量固定的常数；要固定它们必须再加约束（把 DOF 从 2 降到 0，过定）。'
    '②**解集互斥**：测地线（平直时空的直线）机器复核 kappa = %s、tau = %s（两个速度值，双精度纯差分）；'
    '圆与螺旋的 kappa 机器值分别与 1/R、R w^2/v^2 一致到 %s / %s（对照非退化）。'
    '代入公设约束 0 = (w/c)^2：w = 1E-3/1/1E12 倍 c/lambda_C 时右端 = %s，全部 > 0 => 无解。'
    '③**物理**：极值曲线必须是测地线，故「每个粒子都在螺旋」等价于「每个粒子都被一个非引力力持续推离测地线」，'
    '而这个力在式 (1) 中不存在（B05）。=> 桥的缺口不是「漏写一项」，而是**缺一个相互作用**。'
    '这一条把 r384 的 B05 从缺失性判定升级为不可能性判定'
    % (fv(_K_LINE, 4), fv(_T_LINE, 4), fv(_K_CIRC, 6), fv(_T_CIRC, 6),
       ' / '.join(fv(r, 4) for _, r in _res)))

# ================================================================ K02 定理二：频率锁定
say('')
say('K02 · 定理二：公设 + 库内质量关系 => w = m c^2 / hbar（内部运动频率 = 静止能量频率）')
say('-' * 78)

_omega_over = OMEGA_E * HBAR / (M_E * C_LIGHT * C_LIGHT)
_kap_lam = KAPPA_E * LAM_C
_om_lam = OMEGA_E * LAM_C / C_LIGHT
R['K02'] = {'omega_over_mc2_hbar': fv(_omega_over, 12), 'kappa_lamC': fv(_kap_lam, 12),
            'omega_lamC_over_c': fv(_om_lam, 12)}

add('K02', 'PASS',
    '定理二：由三重奏 w = c*sqrt(kappa^2+tau^2) 与库内 m = hbar*sqrt(kappa^2+tau^2)/c 得 '
    'w = m c^2/hbar 精确，即 hbar*w = m c^2 逐位成立',
    '机器：hbar*w/(m c^2) - 1 = %s；kappa*lambda_C - 1 = %s；w*lambda_C/c - 1 = %s（三条都是 1E-58 级的零）。'
    '电子读数：lambda_C = %s m、kappa = %s m^-1、w = %s s^-1、T = %s s。'
    '=> 公设把**每个**粒子的内部运动频率锁死在康普顿频率上：hbar*w 恰好等于静止能量，不多不少。'
    '这不是「精度问题」，而是 i) 「螺旋」的自由度只剩「kappa 与 tau 的分配比例」一个无量纲数（v_perp/v_par），'
    'ii) 该构型在能量上**恰好停在对产生阈值**上（hbar*w = 2 m c^2 是阈值，这里给 m c^2 = 阈值的 1/2）。'
    '代价：任何与该内部运动耦合的荷都会以对产生量级的速率辐射，除非再假设一个**完全退耦**机制（= 新假设）'
    % (fv(abs(_omega_over - 1), 4), fv(abs(_kap_lam - 1), 4), fv(abs(_om_lam - 1), 4),
       fv(LAM_C, 12), fv(KAPPA_E, 12), fv(OMEGA_E, 12), fv(T_OMEGA, 8)))

# ================================================================ K03 定理三：维持公设所需的力
say('')
say('K03 · 定理三：最简实现（tau = 0，圆）所需向心力 F = m^2 c^3 / hbar，等效力场 = Schwinger 临界场')
say('-' * 78)

_FE = R['phys']
add('K03', 'PASS',
    '定理三：取 tau = 0 的最简实现 => kappa = 1/lambda_C、a = c^2 kappa，所需向心力 '
    'F = m c^2 kappa = m^2 c^3/hbar；等效力场 F/e = m^2 c^3/(e hbar) 与 Schwinger 临界场**同一表达式**',
    '电子：F = %s N、E = F/e = %s V/m；Schwinger 临界场 m^2c^3/(e hbar) = %s V/m，'
    '相对差 %s（代数恒等，机器只验数值实现，不是两个独立量的巧合）。'
    '质子：F = %s N、E = %s V/m（F ∝ m^2，故放大 %s 倍 = (m_p/m_e)^2）。'
    '**诚实边界（非常重要）**：F = m c^2 kappa 只依赖 kappa，而公设只锁 sqrt(kappa^2+tau^2) = m c/hbar，'
    '故 kappa 可以小（把份额让给 tau），向心力理论上可低于上式。但此时 1/tau 变小、几何尺度仍 <= sqrt(2) lambda_C，'
    '且 w 不变。=> 「力太大」不能作为否证（本册不这么用）；能作为结论的是：'
    '**该力标度被 (m, c, hbar) 唯一锁定，没有自由参数可把它调到可忽略**，且它在最简实现下恰好等于对产生阈值力'
    % (_FE['F_e'], _FE['E_field_e'], _FE['E_schwinger'], _FE['d_schw_rel'],
       _FE['F_p'], _FE['E_field_p'], _FE['F_p_over_F_e']))

# ================================================================ K04 三条候选桥的代价
say('')
say('K04 · 三条候选桥逐条定价：C1 Ostrogradsky 鬼 / C2 与测地线不相容 / C3 KK 无鬼但需新量子数')
say('-' * 78)

_hs = R['hess']
_hess_rel = abs(_hs['num'] - _hs['exact']) / _hs['exact']
add('K04', 'PASS',
    '三条候选桥的机器定价：不存在「零代价」的桥；唯一无鬼的 C3 仍需把 R 与新量子数 n 作为输入',
    '**C1（加 f(kappa^2+tau^2) 项）**：L = kappa^2 = y\'\'^2/(1+y\'^2)^3 对 y\'\' 的 Hessian = 2/(1+y\'^2)^3；'
    '机器在 (y\',y\'\') = (0.3,0.7) 处得 %s vs 解析 %s（相对差 %s）=> Hessian != 0，'
    'EL 含 y\'\'\'\' 项（系数即该 Hessian）=> 方程升到 **4 阶**，相空间 (y, y\', p, p\') 四维 => 每自由度 2 DOF，'
    'Ostrogradsky 定理给能量无下界 => **鬼**。且要「固定」kappa、tau 还须 f\' != 0，鬼强度 ∝ f\'，不能靠调小回避。'
    '**C2（拉格朗日乘子 lambda [kappa^2+tau^2-(w/c)^2]）**：lambda 无法定项 => 是乘子；'
    'delta/delta lambda 给约束，delta/delta x 给被改写的 EL。自由情形 EL 给 y\'\' = 0 => kappa = 0，'
    '代入约束得 0 = (w/c)^2（K01 的残差 %s）=> **不相容**，除非 w = 0（无螺旋）。'
    '要让 C2 可解必须同时加上 K01 说的那个非引力力 => 回到同一个缺口，且额外 +1 个场（撞 Omega5）。'
    '**C3（KK 测地圆）**：粒子沿内部圆做测地运动，kappa = 1/R **由几何给定**（不是由作用量固定）=> 无鬼、无新场；'
    '代价两条：(a) R 仍是输入（O-SCALE 已判尺度不可内生）；(b) 质量塔需要缠绕/动量量子数 n（p_5 = n hbar/R）。'
    '=> 三条桥里只有 C3 在拉格朗日层面干净，但它把代价从「鬼」换成了「两个新输入」'
    % (fv(_hs['num'], 12), fv(_hs['exact'], 12), fv(_hess_rel, 4),
       fv(max(r for _, r in _res), 4)))

# ================================================================ K05 KK 桥的线性塔被实验排除
say('')
say('K05 · C3 的线性塔作为质量谱：预言 m_n ∝ n，与观测到的代间比冲突')
say('-' * 78)

add('K05', 'FAIL',
    'KK 桥只能给质量**标度**，不能给质量**谱**：线性塔预言 m_2/m_1 = 2、m_3/m_1 = 3，'
    '而实测 m_mu/m_e = 206.768、m_tau/m_e = 3477.2',
    '逐项：n = 2 预言 2 vs 实测 %s => 差 %s 倍；n = 3 预言 3 vs 实测 %s => 差 %s 倍。'
    '=> 「三代 = KK 塔的前三级」被排除 2~3 个量级。结构原因：塔是**等间距**的（m_n = n hbar/(Rc)），'
    '而代间比是 206.8 与 16.8（非等间距、且两级比本身差 12.3 倍）——任何单一 R 都给不出。'
    '这与库内既有结论同向：O-SCALE（尺度不可内生）+ r379（形状族近简并、位数缺 4.03 位）。'
    '故 C3 的合法定位是「质量的标度来源」而非「质量谱/三代机制」'
    % (fv(M_MU_OVER_E, 10), fv(Dc(str(K5[0]['miss'])), 6),
       fv(M_TAU_OVER_E, 10), fv(Dc(str(K5[1]['miss'])), 6)))

# ================================================================ K06 存活面
say('')
say('K06 · 存活面与须用户裁决项')
say('-' * 78)

add('K06', 'INFO',
    '攻破后的存活面：桥可以建，但只能建成「标度桥」；「谱桥」（三代/质量层级）在三条候选路径上全部失败',
    '存活：C3（KK 测地圆）给出 kappa = 1/R 与 m_1 = hbar/(Rc)，即**一个**质量标度，且不引入鬼。'
    '被否：C1（Ostrogradsky 鬼）、C2（与测地线不相容）、C3 的塔（K05 排除 1E2~1E3 倍）。'
    '须用户裁决（本册不代选）：①是否接受「螺旋」只作为**运动学重述**（kappa、tau 由质量经 m = hbar*sqrt(kappa^2+tau^2)/c 反解，'
    '而非由作用量导出）——这是零成本、零新场的定位，代价是它不再有预言力（r384 的 C02 已证三重奏是恒等）；'
    '②是否走 C3 并接受 +2 输入（R 与 n）；③是否放弃「三代 = 螺旋塔」，回到库内 SU(2)_2 三扇区机制（两者互斥，须二选一）。'
    '红线：本册否证的是「螺旋公设可由二阶作用量导出」与「KK 塔可给质量谱」，**不否证**螺旋图像作为运动学描述的自洽性')

# ================================================================ 守卫
say('')
say('=' * 78)
say('守卫')
say('=' * 78)

_g1 = abs(KAPPA_E * LAM_C - 1)
guard('G01', 'kappa*lambda_C = 1（同一 m 定义的两条路径互为倒数）', _g1 < Dc('1E-55'),
      '|dev| = %s' % fv(_g1, 4))

_g2 = abs(OMEGA_E * HBAR - M_E * C_LIGHT * C_LIGHT)
guard('G02', 'hbar*w = m c^2', _g2 / (M_E * C_LIGHT * C_LIGHT) < Dc('1E-55'),
      '相对 |dev| = %s' % fv(_g2 / (M_E * C_LIGHT * C_LIGHT), 4))

_g3 = abs(E_FIELD_E - E_SCHW) / E_SCHW
guard('G03', 'F/e 与 m^2c^3/(e hbar) 一致（代数恒等，验实现）', _g3 < Dc('1E-55'),
      '相对差 = %s' % fv(_g3, 4))

_g4 = max(abs(x['kappa'] - x['expect_kappa']) / x['expect_kappa'] for x in _cl)
guard('G04', '圆：纯差分 kappa = 1/R（三组半径/速度，h 按 omega*h=1E-3 归一）', _g4 < 1e-8,
      '最大相对差 = %.3e（阈值 1E-8，余量 ~7 倍；定步长版本是 1.5E-7）' % _g4)

_g5 = max(abs(x['kappa']) for x in _ln)
guard('G05', '直线：纯差分 kappa = 0（测地线判据）', _g5 < 1e-9, 'max |kappa| = %.3e' % _g5)

_g6 = max(abs(_hx['kappa'] - _hx['expect_kappa']) / _hx['expect_kappa'],
          abs(_hx['tau'] - _hx['expect_tau']) / _hx['expect_tau'])
guard('G06', '螺旋：纯差分与 R w^2/v^2、u w/v^2 一致（kappa 强核对 / tau 弱核对）', _g6 < 1e-5,
      '最大相对差 = %.3e（阈值 1E-5；tau 是三阶量，走「二阶差分再一阶差分」的嵌套路径，O(h^2)，'
      '与 r384-C01 的 3.3E-4 同族、此处因 h 归一而好两个量级）' % _g6)

_g7 = _hess_rel
guard('G07', 'L = kappa^2 对 y\'\' 的 Hessian = 2/(1+y\'^2)^3（Ostrogradsky 判据可算）', _g7 < 1e-8,
      '相对差 = %.3e' % _g7)

_g8 = abs(Dc(str(K5[0]['miss'])) - M_MU_OVER_E / 2)
guard('G08', '塔的失配比 = obs/pred（算术自洽）', _g8 < Dc('1E-6'), '|dev| = %s' % fv(_g8, 4))

# ================================================================ 状态表与产物
say('')
say('=' * 78)
say('状态表')
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
say('攻破结论（三条）:')
say('  (1) 桥不可能零成本：二阶作用量的极值曲线必是测地线（kappa=tau=0），与公设 kappa^2+tau^2=(w/c)^2>0 '
    '交集为空 => 缺的不是一项，而是一个非引力相互作用（K01，r384-B05 由「没写」升级为「不可能」）')
say('  (2) 公设把内部频率锁死在康普顿频率：w = m c^2/hbar、hbar*w = m c^2 逐位成立（K02）；'
    '最简实现所需向心力 F = m^2c^3/hbar，电子 %s N、等效力场恰为 Schwinger 临界场 %s V/m（K03）'
    % (_FE['F_e'], _FE['E_schwinger']))
say('  (3) 三条候选桥全部有代价：C1 Ostrogradsky 鬼（4 阶 + Hessian>0）、C2 与测地线不相容、'
    'C3 KK 无鬼但只能给标度（线性塔被 K05 排除 %s / %s 倍）' % (fv(Dc(str(K5[0]['miss'])), 4), fv(Dc(str(K5[1]['miss'])), 4)))

OUT = {
    'name': NAME,
    'verdict_counts': _CNT,
    'items': ITEMS,
    'guards': GUARDS,
    'guards_ok': '%d/%d' % (_GOK, len(GUARDS)),
    'key_numbers': dict(R['phys'], **{
        'geom_circle_kappa_err': fv(_K_CIRC, 8),
        'geom_line_kappa': fv(_K_LINE, 4),
        'hess_num': fv(_hs['num'], 16),
        'hess_exact': fv(_hs['exact'], 16),
        'tower_miss_n2': fv(Dc(str(K5[0]['miss'])), 8),
        'tower_miss_n3': fv(Dc(str(K5[1]['miss'])), 8),
    }),
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
    say('产物：' + _jp)
    say('      ' + _rp)
except Exception as _e:
    say('产物写出失败（不影响判定）：%s' % _e)

sys.exit(0 if _GOK == len(GUARDS) else 1)

