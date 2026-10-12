# -*- coding: utf-8 -*-
"""
TUFT-V4.8 修订版 §4.2 稳态基态条件与光速螺旋几何自洽性 · 全维审计
r49 · 2026-10-12

来料：《TUFT-V4.8｜修订版 4.2 稳态基态条件与光速螺旋几何自洽性》+《4.3 稳态质量隐式关系（同步更新）》
自称全部修正：圆柱螺旋参数化、Frenet-Serret 逗号笔误、Omega 错误定义、
作用量/哈密顿/边界条件全套量纲重构、区分两套积分约定、势能项标注为罚约束、清除逗号排版错误。

本册定位（分工声明，零重复）：
  r45 审 V4.5 变分导出链（无源 + 衰减边界 => kappa≡0 => 无粒子）
  r46 审 V4.8 子分支B（加源 + 边界项，R_c 导出）
  r47 审 V4.8-4.3 稳态质量隐式关系与 m_max（旧版 8π 系数）
  r48 审 V4.7 分支2 格林函数解与自能重算
  本册审【修订版 4.2 稳态基态条件 + 螺旋几何自洽性】，并对 4.3（4π 系数版）做回归复算。
  本册新增的两条结构判据此前无人登记：
    (1) 罚约束 V_constraint 不能豁免量纲齐次性（与动能项在同一被积式内相加减）
    (2) 条件2（V=0）=> kappa 被钉为常数 => 自能恒零 => 条件6（能量极小）无解
       => §4.2 条件集与 §4.3 质量链在同一构型下互斥（本册承重二难）

工具：mpmath 1.3.0（dps=80）+ Fraction 四元组量纲 (M,L,T,Q)
纪律：量纲工具先过 guard 再用于判定；所有断言与文案同取向互锁。
"""

import os
import sys
import json
import io
from fractions import Fraction as F

import mpmath as mp

mp.mp.dps = 80

ROUND = 'r49'
DATE = '2026-10-12'
TAG = 'TUFT-r49_V48修订版42稳态基态与螺旋几何_全维审计_2026-10-12'
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SELF_DIR)
OUTDIR = os.path.join(BASE, '数据')

# ---------------------------------------------------------------- 量纲工具
# 四元组 (M, L, T, Q)：质量、长度、时间、电荷
ZERO = (F(0), F(0), F(0), F(0))
DIM_NAMES = ('M', 'L', 'T', 'Q')


def dmul(a, b):
    """量纲相乘 = 指数相加（r37/r44/r45/r48 四次同族事故点，必须 guard）"""
    return tuple(x + y for x, y in zip(a, b))


def dpow(a, n):
    n = F(n)
    return tuple(x * n for x in a)


def ddiv(a, b):
    return dmul(a, dpow(b, F(-1)))


def dstr(a):
    out = []
    for nm, v in zip(DIM_NAMES, a):
        if v == 0:
            continue
        out.append(nm if v == 1 else (nm + '^' + str(v)))
    return '·'.join(out) if out else '1'


D_M = (F(1), F(0), F(0), F(0))
D_L = (F(0), F(1), F(0), F(0))
D_T = (F(0), F(0), F(1), F(0))
D_Q = (F(0), F(0), F(0), F(1))
D_NONE = ZERO


def dim_of(power_map):
    """由 {基础量纲: 指数} 构造量纲"""
    d = ZERO
    for base, n in power_map.items():
        d = dmul(d, dpow(base, n))
    return d


# ---------------------------------------------------------------- 输出格式
def fx(x, nd=26):
    """强制科学计数法字符串（与库内 r 序列读数口径一致，26 位有效数字）"""
    x = mp.mpf(x)
    if x == 0:
        return '0.' + '0' * (nd - 1) + 'E+00'
    ex = int(mp.floor(mp.log10(abs(x))))
    mant = x / mp.mpf(10) ** ex
    s = mp.nstr(mant, nd, strip_zeros=False)
    if 'e' in s:
        s = s.split('e')[0]
    if s.startswith('10'):          # 末位进位跨过 10 的情形
        mant = mant / 10
        ex += 1
        s = mp.nstr(mant, nd, strip_zeros=False).split('e')[0]
    return s + 'E' + ('-' if ex < 0 else '+') + str(abs(ex)).rjust(2, '0')


def rel(a, b):
    """相对偏差"""
    a = mp.mpf(a)
    b = mp.mpf(b)
    if a == 0 and b == 0:
        return mp.mpf('0')
    den = max(abs(a), abs(b))
    return abs(a - b) / den


# ---------------------------------------------------------------- 常数（CODATA 2018 / PDG，与来料代码同源）
c = mp.mpf('299792458')
hbar = mp.mpf('1.0545718176461565e-34')
e_ch = mp.mpf('1.602176634e-19')
m_e = mp.mpf('9.1093837015e-31')
m_mu = mp.mpf('1.883531627e-28')
m_tau = mp.mpf('3.16754e-27')
l_P = mp.mpf('1.616255078e-35')
G_exp = mp.mpf('6.67430e-11')
pi = mp.pi

# 来料代码口径的磁矩残差
A_E_QED = mp.mpf('1.15965218128e-3')
A_E_EXP = mp.mpf('1.15965218059e-3')
A_MU_QED = mp.mpf('1.16591810e-3')
A_MU_EXP = mp.mpf('1.16592040e-3')
SIG_E_CODE = mp.mpf('1e-12')
SIG_MU_CODE = mp.mpf('4e-7')
SIG_G_REL_CODE = mp.mpf('1e-5')
# 真实不确定度档（r44 口径，显式登记来源）
SIG_E_REAL = mp.mpf('2.8e-14')
SIG_MU_REAL = mp.mpf('5.2e-10')
SIG_G_REL_REAL = mp.mpf('2.2e-5')

D_E = A_E_EXP - A_E_QED
D_MU = A_MU_EXP - A_MU_QED

M_P_KG = hbar / (l_P * c)
M_P_GEV = mp.mpf('1.22089e19')

# ---------------------------------------------------------------- 条目记录
ENTRIES = []
GUARDS = []


def _rec(vid, verdict, claim, reading):
    ENTRIES.append({'id': vid, 'verdict': verdict, 'claim': claim, 'reading': reading})


def P_(vid, claim, reading):
    _rec(vid, 'PASS', claim, reading)


def F_(vid, claim, reading):
    _rec(vid, 'FAIL', claim, reading)


def B_(vid, claim, reading):
    _rec(vid, 'BOUNDARY', claim, reading)


def I_(vid, claim, reading):
    _rec(vid, 'INFO', claim, reading)


def C_(vid, claim, reading):
    _rec(vid, 'CORRECTED', claim, reading)


def M_(vid, claim, reading):
    _rec(vid, 'MISMATCH', claim, reading)


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'detail': str(detail)})


# ================================================================ G0 量纲工具自检（先过 guard 再用于判定）
guard('g01_dmul_is_add_not_mul',
      dmul(D_L, D_L) == (F(0), F(2), F(0), F(0)),
      dstr(dmul(D_L, D_L)))
guard('g02_dpow_negative',
      dpow(D_L, -1) == (F(0), F(-1), F(0), F(0)),
      dstr(dpow(D_L, -1)))
guard('g03_dstr_negative_renders_caret',
      dstr(dpow(D_L, -1)) == 'L^-1', dstr(dpow(D_L, -1)))
guard('g04_fx_digits', len(fx(mp.mpf('1.5')).split('E')[0].replace('.', '')) >= 26,
      fx(mp.mpf('1.5')))
guard('g05_hbar_dim', dim_of({D_M: 1, D_L: 2, D_T: -1}) == (F(1), F(2), F(-1), F(0)),
      dstr(dim_of({D_M: 1, D_L: 2, D_T: -1})))
guard('g06_c_dim', dim_of({D_L: 1, D_T: -1}) == (F(0), F(1), F(-1), F(0)),
      dstr(dim_of({D_L: 1, D_T: -1})))
guard('g07_G_dim', dim_of({D_M: -1, D_L: 3, D_T: -2}) == (F(-1), F(3), F(-2), F(0)),
      dstr(dim_of({D_M: -1, D_L: 3, D_T: -2})))

# ================================================================ A 段 · 4.2.1 螺旋几何
# 来料参数化： r(s) = (R cos(s/L), R sin(s/L), H s/L),  L = sqrt(R^2+H^2)
R_HEL = mp.mpf('0.3')
H_HEL = mp.mpf('0.7')
L_HEL = mp.sqrt(R_HEL ** 2 + H_HEL ** 2)
SIN_TH_GEO = R_HEL / L_HEL
COS_TH_GEO = H_HEL / L_HEL
HH = mp.mpf('1e-16')          # 有限差分步长：最优 h^5 ≈ eps(dps=80) ⇒ 截断与舍入均 ~1e-32


def r_vec(s):
    u = s / L_HEL
    return [R_HEL * mp.cos(u), R_HEL * mp.sin(u), H_HEL * u]


def t_ana(s):
    u = s / L_HEL
    return [-(R_HEL / L_HEL) * mp.sin(u), (R_HEL / L_HEL) * mp.cos(u), H_HEL / L_HEL]


def n_ana(s):
    u = s / L_HEL
    return [-mp.cos(u), -mp.sin(u), mp.mpf('0')]


def b_ana(s):
    u = s / L_HEL
    return [(H_HEL / L_HEL) * mp.sin(u), -(H_HEL / L_HEL) * mp.cos(u), R_HEL / L_HEL]


def _sub(a, b):
    return [x - y for x, y in zip(a, b)]


def _add(a, b):
    return [x + y for x, y in zip(a, b)]


def _sc(k, a):
    return [k * x for x in a]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _norm(a):
    return mp.sqrt(_dot(a, a))


def d1(f, s, h=HH):
    """中心差分一阶导"""
    return _sc(1 / (2 * h), _sub(f(s + h), f(s - h)))


def t_num_of(s):
    return d1(r_vec, s)


def dt_num_of(s):
    return d1(t_num_of, s)


def kap_num_of(s):
    return _norm(dt_num_of(s))


def n_num_of(s):
    return _sc(1 / kap_num_of(s), dt_num_of(s))


def b_num_of(s):
    return _cross(t_num_of(s), n_num_of(s))


S0 = mp.mpf('0.4')

# A-01 弧长参数化
speed_num = _norm(d1(r_vec, S0))
res_speed = rel(speed_num, mp.mpf('1'))
P_('V01', '弧长参数化 |r\'(s)|=1 严格成立（来料自称「圆柱螺旋参数化」已修正）',
   '机器中心差分 |r\'(s)| = %s，相对 1 的偏差 %s（R=%s, H=%s）'
   % (fx(speed_num), fx(res_speed), fx(R_HEL), fx(H_HEL)))
guard('g08_arclength_unit_speed', res_speed < mp.mpf('1e-30'), fx(res_speed))

# A-02/03 曲率挠率：解析式 vs Frenet 定义式（差分双路径）
kap_ana = R_HEL / L_HEL ** 2
tau_ana = H_HEL / L_HEL ** 2
dt_num = dt_num_of(S0)
kap_num = kap_num_of(S0)
n_num = n_num_of(S0)
b_num = b_num_of(S0)
db_num = d1(b_num_of, S0)
tau_num = -_dot(db_num, n_num)
res_kap = rel(kap_num, kap_ana)
res_tau = rel(tau_num, tau_ana)
P_('V02', 'kappa = R/L^2、tau = H/L^2 与 Frenet 定义式一致（双路径：解析式 vs 数值差分）',
   'kappa 解析 %s / 差分 %s，相对偏差 %s；tau 解析 %s / 差分 %s，相对偏差 %s'
   % (fx(kap_ana), fx(kap_num), fx(res_kap), fx(tau_ana), fx(tau_num), fx(res_tau)))
guard('g09_kappa_matches_analytic', res_kap < mp.mpf('1e-25'), fx(res_kap))
guard('g10_tau_matches_analytic', res_tau < mp.mpf('1e-25'), fx(res_tau))

# A-04 恒等式 kappa^2+tau^2 = 1/L^2
lhs_id = kap_ana ** 2 + tau_ana ** 2
rhs_id = 1 / L_HEL ** 2
res_id = rel(lhs_id, rhs_id)
P_('V03', '几何恒等式 kappa^2 + tau^2 = 1/L^2 成立',
   '左 %s，右 %s，相对偏差 %s' % (fx(lhs_id), fx(rhs_id), fx(res_id)))

# A-05 耦合公理 tau = kappa cot(theta) 与 sin=R/L, cos=H/L 自洽
cot_geo = tau_ana / kap_ana
cot_from_theta = COS_TH_GEO / SIN_TH_GEO
res_cot = rel(cot_geo, cot_from_theta)
P_('V04', '耦合公理 tau = kappa·cot(theta) 与 sin(theta)=R/L、cos(theta)=H/L 自洽',
   'tau/kappa = %s，cos/sin = %s，相对偏差 %s' % (fx(cot_geo), fx(cot_from_theta), fx(res_cot)))

# A-06 【修订核心】Omega = c/L 与 omega = c sqrt(kappa^2+tau^2) 数值相等
#   omega：Frenet 标架绕 Darboux 轴 D = tau·t + kappa·b 的旋转速率 |D|，乘 ds/dt = c
D_vec = _add(_sc(tau_ana, t_ana(S0)), _sc(kap_ana, b_ana(S0)))
D_mod = _norm(D_vec)
omega_num = c * D_mod
# Darboux 关系 dt/ds = D x t（三条）数值检验
chk_t = _sub(_cross(D_vec, t_ana(S0)), dt_num)
chk_n = _sub(_cross(D_vec, n_ana(S0)), d1(n_ana, S0))
chk_b = _sub(_cross(D_vec, b_ana(S0)), d1(b_ana, S0))
err_darboux = max(_norm(chk_t), _norm(chk_n), _norm(chk_b))
# Omega：方位角 phi = atan2(y,x) 对 t 的导数
def phi_of(s):
    return mp.atan2(r_vec(s)[1], r_vec(s)[0])


dphi_ds = (phi_of(S0 + HH) - phi_of(S0 - HH)) / (2 * HH)
omega_ana = c / L_HEL
res_omega = rel(omega_num, omega_ana)
res_Omega = rel(c * dphi_ds, omega_ana)
res_eq = rel(omega_num, c * dphi_ds)
P_('V05', '【修订核心·真修好】Omega（实验室系轨道角速度）与 omega（Frenet 标架内禀旋转频率）数值相等，'
          '且均 = c/L',
   'Darboux 轴模 |D| = %s = 1/L（偏差 %s）；omega = c|D| = %s；Omega = c·dphi/ds = %s；'
   '解析 c/L = %s；omega 相对偏差 %s、Omega 相对偏差 %s、二者互差 %s。'
   'Darboux 三条恒等式 (dt,dn,db) 最大残差 %s（阳性对照：把 D 置零后残差 = |dt/ds| = %s，检验器非恒零）'
   % (fx(D_mod), fx(rel(D_mod, 1 / L_HEL)), fx(omega_num), fx(c * dphi_ds), fx(omega_ana),
      fx(res_omega), fx(res_Omega), fx(res_eq), fx(err_darboux), fx(_norm(dt_num))))
guard('g11_darboux_mod_equals_inv_L', rel(D_mod, 1 / L_HEL) < mp.mpf('1e-30'),
      fx(rel(D_mod, 1 / L_HEL)))
guard('g12_darboux_reproduces_frame_derivatives', err_darboux < mp.mpf('1e-25'), fx(err_darboux))
guard('g13_omega_equals_Omega', res_eq < mp.mpf('1e-25'), fx(res_eq))
guard('g14_positive_control_darboux_nonzero', _norm(dt_num) > mp.mpf('1e-10'), fx(_norm(dt_num)))

# A-07 旧式 Omega = c·kappa 的偏差
ratio_old = (c * kap_ana) / (c / L_HEL)
C_('V06', '旧式 Omega = c·kappa 与修正式 Omega = c/L 的关系',
   '机器比值 (c·kappa)/(c/L) = R/L = sin(theta) = %s，与 sin(theta) 相对偏差 %s'
   ' ⇒ 旧式恒偏小 sin(theta) 倍，仅当 H=0（tau=0，退化为纯圆）时相等；含挠率时旧式必错。'
   '本条确认「Omega 错误定义」这一项修订**成立**'
   % (fx(ratio_old), fx(rel(ratio_old, SIN_TH_GEO))))

# A-08 omega = c·kappa/sin(theta) 恒等
res_om2 = rel(c * kap_ana / SIN_TH_GEO, omega_ana)
P_('V07', 'omega = c·kappa/sin(theta) 与 c·sqrt(kappa^2+tau^2) 恒等',
   '相对偏差 %s' % fx(res_om2))

# A-09 「类光」口径
B_('V08', '「类光圆柱螺旋」：s = c·t 即空间速率 |dr/dt| = c',
   '在 3+1 时空下该世界线确为零测（null），术语自洽；但同一构型又赋予静质量 m，'
   '「以 c 运动的局域螺旋 + 非零静质量」属 TUFT 公设层张力（v_local = c），非本册新发现，仅登记边界')

# A-10 theta 普适常数 ⇒ tau/kappa 全域恒定
I_('V09', '「theta 是 TUFT 普适常数，不随粒子种类改变」',
   '由 tau = kappa·cot(theta) ⇒ tau/kappa = cot(theta) 对所有粒子取同一值'
   ' ⇒ 挠率不是独立自由度（r41 R15「theta 常数 ⇒ tau/kappa 全域恒定，tau 仍被奴役」同族）。'
   '本册几何算例 cot(theta) = %s' % fx(cot_geo))

# ================================================================ B 段 · 4.2.2 作用量与量纲重构
D_S = dim_of({D_M: 1, D_L: 2, D_T: -1})                 # [S] = J·s
D_LAG = ddiv(D_S, dpow(D_L, 4))                          # [L] = [S]/L^4 （x^0 = c t）
D_KAPPA = dpow(D_L, -1)
D_GRAD4 = dpow(D_L, -1)                                  # d/dx^0 也是 L^-1
D_OMEGA = dpow(D_T, -1)

# B-01 作用量约定
guard('g15_lag_density_dim', D_LAG == (F(1), F(-2), F(-1), F(0)), dstr(D_LAG))
P_('V10', '约定 S = ∫d^4x √-g ℒ（x^0 = c·t）下，[d^4x] = L^4，[ℒ] = J·s/m^4',
   '机器 [S] = %s，[ℒ] = %s ✓ 与来料自述「J·s/m^4」一致（J·s·m^-4 = M·L^-2·T^-1 逐项核对通过）'
   % (dstr(D_S), dstr(D_LAG)))

# B-02 动能项（修订核心）
D_KIN_NEW = dmul(dim_of({D_M: 1, D_L: 2, D_T: -1}), dpow(dmul(D_GRAD4, D_KAPPA), 2))
D_KIN_OLD = dmul(ddiv(dim_of({D_M: 1, D_L: 2, D_T: -1}), dim_of({D_L: 1, D_T: -1})),
                 dpow(dmul(D_GRAD4, D_KAPPA), 2))
ok_kin = (D_KIN_NEW == D_LAG)
gap_old_lag = ddiv(D_LAG, D_KIN_OLD)
P_('V11', '【修订核心·真修好】动能项 (ħ/2)·g^{μν}∇_μκ∇_νκ 量纲 = [ℒ]',
   '机器 [(ħ/2)(∇κ)^2] = %s = [ℒ] = %s ✓。旧系数 ħ/(2c) 给 %s，对 [ℒ] 缺口 %s（= c）；'
   '（r46 B01 记的缺口 c^2 是拿它当**能量密度**比，本修订版已改称拉氏密度，故缺口为 c —— 两种读法都判旧式错）'
   % (dstr(D_KIN_NEW), dstr(D_LAG), dstr(D_KIN_OLD), dstr(gap_old_lag)))
guard('g16_kinetic_term_is_homogeneous', ok_kin, dstr(D_KIN_NEW))

# B-03 罚约束项量纲【本册承重】
D_BRACKET = dmul(dpow(dim_of({D_L: 1, D_T: -1}), 2), dpow(D_KAPPA, 2))   # [c^2 kappa^2] = T^-2
D_VCON = dpow(D_BRACKET, 2)                                              # V = 1/2 (bracket)^2
gap_V = ddiv(D_LAG, D_VCON)
F_('V12', 'V_constraint = 1/2·(c^2κ^2/sin^2θ − ω^2)^2 被标注为「罚约束项，量纲不必匹配拉氏密度」',
   '**罚函数不能豁免量纲齐次性**：它与动能项写在**同一个被积式**内做加减（ℒ = ħ/2(∇κ)^2 − V），'
   '相加减的两项必须同量纲，否则作用量本身量纲不齐、变分无定义。'
   '机器 [V] = %s（括号 c^2κ^2 与 ω^2 同量纲 T^-2 ✓ 内部自洽），而 [ℒ] = %s，缺口 %s。'
   '正确做法是乘**带量纲的拉格朗日乘子** λ(x)·(c^2κ^2/sin^2θ − ω^2)，[λ] = %s。'
   '（本册第 12 次「量纲非齐次」复发）'
   % (dstr(D_VCON), dstr(D_LAG), dstr(gap_V), dstr(gap_V)))
guard('g17_Vconstraint_dim_is_T_minus_4', D_VCON == (F(0), F(0), F(-4), F(0)), dstr(D_VCON))
guard('g18_Vconstraint_mismatch_is_nonzero', gap_V != D_NONE, dstr(gap_V))

# B-04 欧拉-拉格朗日方程量纲
D_EL_LHS = dmul(dim_of({D_M: 1, D_L: 2, D_T: -1}), dpow(D_GRAD4, 2))   # hbar * nabla^2 * kappa
D_EL_LHS = dmul(D_EL_LHS, D_KAPPA)
D_EL_RHS = ddiv(D_VCON, D_KAPPA)                                       # dV/dkappa
gap_EL = ddiv(D_EL_LHS, D_EL_RHS)
F_('V13', '体域欧拉–拉格朗日方程 ħ∇^2κ = −dV_constraint/dκ + J_κ 量纲齐次',
   '机器 [ħ∇^2κ] = %s，[dV/dκ] = %s，缺口 %s ⇒ 该场方程**量纲不成立**（是 V12 的直接后果）。'
   '若 V 换成 λ·(c^2κ^2/sin^2θ − ω^2)，则 [dV/dκ] = %s 与左端一致'
   % (dstr(D_EL_LHS), dstr(D_EL_RHS), dstr(gap_EL),
      dstr(ddiv(dmul(gap_V, D_VCON), D_KAPPA))))
guard('g19_EL_inhomogeneous', gap_EL != D_NONE, dstr(gap_EL))

# B-05 度规签名未声明 ⇒ 拉氏与哈密顿的符号相容性二分支
def H_grad_coeff(sig):
    """sig=+1 → (+,−,−,−)；sig=−1 → (−,+,+,+)。返回哈密顿密度中 |∇κ|^2 的系数"""
    g00 = mp.mpf(sig)
    gsp = mp.mpf(-sig)
    A3 = c * (hbar / 2) * g00 / c ** 2        # L3 中 kdot^2 的系数
    B_grad = c * (hbar / 2) * gsp             # L3 中 |grad kappa|^2 的系数
    return -B_grad                            # H = pi*kdot - L3 ⇒ 梯度项系数取负


hg_plus = H_grad_coeff(1)
hg_minus = H_grad_coeff(-1)
B_('V14', 'ℒ = +(ħ/2)g^{μν}∇_μκ∇_νκ − V 与 ℋ = +(ħc/2)|∇κ|^2 的符号相容性',
   '来料**未声明度规签名**，而 √-g 在两种签名下都成立，无法据此判定。机器两分支：'
   '(+,−,−,−) 下 ℋ 梯度项系数 = %s（= +ħc/2 ✓ 与来料一致）；'
   '(−,+,+,+) 下 = %s（负号 ⇒ 梯度能为负、哈密顿无下界、无稳定基态）。'
   '⇒ 该自洽性**依赖一个未声明的约定**，标 BOUNDARY 不代选'
   % (fx(hg_plus), fx(hg_minus)))
guard('g20_signature_plus_branch_matches_claim', hg_plus == hbar * c / 2, fx(hg_plus))
guard('g21_signature_minus_branch_is_negative', hg_minus == -hbar * c / 2, fx(hg_minus))

# B-06 哈密顿密度与两套系数约定
D_GRAD3_KAPPA = dmul(dpow(D_L, -1), D_KAPPA)      # 空间梯度 [∇κ] = L^-2
D_HAM = dmul(dim_of({D_M: 1, D_L: 3, D_T: -2}), dpow(D_GRAD3_KAPPA, 2))
D_L3 = dmul(D_LAG, dim_of({D_L: 1, D_T: -1}))
P_('V15', '【修订核心·真修好】ℋ_spiral = (ħc/2)|∇κ|^2 量纲 = 能量密度；且「两套系数约定」说明正确',
   '机器 [(ħc/2)|∇κ|^2] = %s = J/m^3 ✓；[ℒ_3] = [cℒ] = %s，与 [ℋ] 同 ✓；'
   '两套系数之比 (ħc/2)/(ħ/2) = c = %s 恰为 ∫d^4x = ∫dt d^3x·c 的换算因子'
   ' ⇒ 「四维用 ħ/2、3+1 用 ħc/2」这条修订**成立**（旧 ħ/(2c) 全部删除亦正确）'
   % (dstr(D_HAM), dstr(D_L3), fx(c)))
guard('g22_hamiltonian_is_energy_density', D_HAM == (F(1), F(-1), F(-2), F(0)), dstr(D_HAM))

# B-07 自能积分
D_USELF_INT = dmul(dpow(D_L, 3), D_HAM)
P_('V16', '自能积分 U_self = ∫d^3x √g ℋ_spiral 量纲为能量',
   '机器 [d^3x·ℋ] = %s = M·L^2·T^-2 = J ✓' % dstr(D_USELF_INT))
guard('g23_uself_integral_is_energy', D_USELF_INT == (F(1), F(2), F(-2), F(0)), dstr(D_USELF_INT))

# B-08 边界平衡式量纲
D_SIGMA = dim_of({D_M: 1, D_T: -2})          # 表面能密度 J/m^2
D_KCURV = dpow(D_L, -1)
D_BC_L = D_HAM
D_BC_R = dmul(D_SIGMA, D_KCURV)
P_('V17', '【修订核心·真修好】边界力学平衡 (ħc/2)(∇κ)^2|_{∂Ω} = σ·K 量纲齐次',
   '左 %s，右（σ = 表面能密度 J/m^2 = %s，K = %s）%s ⇒ 相等 ✓。'
   '（r46 B03 判旧系数 ħ/(2c) 两种 σ 口径都不齐，本次改用 ħc/2 后闭合）'
   % (dstr(D_BC_L), dstr(D_SIGMA), dstr(D_KCURV), dstr(D_BC_R)))
guard('g24_boundary_balance_homogeneous', D_BC_L == D_BC_R, dstr(D_BC_R))

# B-09 但「边界变分」给出的不是能量密度
B_('V18', '条件 4 声称由「边界变分驻定」得到 (ħc/2)(∇κ)^2|_{∂Ω} = σK',
   '对 ∫d^3x (ħc/2)|∇κ|^2 做变分，边界项是 (ħc)·∂_nκ·δκ（一阶、含法向导数、线性于 κ），'
   '而 (ħc/2)(∇κ)^2 是**能量密度**（二阶、平方）⇒ 二者是不同对象。'
   '量纲虽齐次（V17），但「由边界变分驻定推出」这一步**推导链断裂**；'
   '写成 Young–Laplace 型「内压 = σK」是另一套物理，不能由同一变分同时给出')

# ---------------------------------------------------------------- B 段承重：稳态基态二难
# 条件2：V=0 且 dV/dκ=0  ⇒  c^2κ^2/sin^2θ = ω^2  ⇒  |κ| = ω sinθ / c = 常数（ω、θ 均为全局常数）
F_('V19', '【本册承重·二难】引理 4.1 条件 2（V_constraint = 0）与 §4.3 质量链可否同时成立',
   '条件 2 给 c^2κ^2/sin^2θ = ω^2 ⇒ |κ| ≡ ω·sinθ/c = **常数**（ω 与 θ 都是来料声明的全局常数，'
   '见注记 2「θ 是 TUFT 普适常数」）。于是 ∇κ ≡ 0 ⇒ ℋ_spiral ≡ 0 ⇒ **U_self ≡ 0** ⇒ '
   '总静能 E = ħcκ_0/sinθ 对 κ_0 **线性**，dE/dκ_0 = ħc/sinθ ≠ 0 ⇒ **条件 6（能量极小）无解**'
   ' ⇒ m_max 与「稳态存在的能量阈值」不存在。'
   '反向：若要 U_self ≠ 0 就必须 ∇κ ≠ 0，即 κ 非常数，即 V_constraint ≠ 0，**违反条件 2**'
   ' ⇒ 不是稳态基态。**§4.2 的条件集与 §4.3 的质量链在同一构型下互斥**（二难，非缺推导）')
F_('V20', '（二难后果·边界）条件 2 下边界力学平衡条件退化',
   '∇κ ≡ 0 ⇒ 条件 4 左端 = 0 ⇒ σ·K = 0；球面边界 K = 2/R_c ≠ 0 ⇒ σ ≡ 0'
   ' ⇒ 边界条件退化为恒等式 0 = 0，**不再构成约束**，「局域粒子包稳定」的力学平衡机制随之消失')
F_('V21', '（二难后果·源）条件 2 与条件 1 在源区直接矛盾',
   'κ 为常数 ⇒ ∇^2κ = 0 ⇒ 由条件 1 的场方程（约束面上 dV/dκ = 0）得 J_κ ≡ 0，'
   '与「源内部（螺旋世界线邻域）J_κ ≠ 0」直接冲突 ⇒ **引理 4.1 的六条方程组在有源区无解**；'
   'J_κ ≡ 0 则回到 r45 T34「无源 ⇒ 无粒子」')
I_('V22', '条件 2 写的两条（V = 0 与 dV/dκ = 0）是否独立',
   '机器代数：dV/dκ = 2(c^2κ^2/sin^2θ − ω^2)·(2c^2κ/sin^2θ)，V = 0 已蕴含括号为 0'
   ' ⇒ dV/dκ = 0 自动成立 ⇒ **实际只有 1 条独立约束**，不是 2 条')
C_('V23', '选项 5「把罚约束改写为拉格朗日乘子形式，消除罚函数，重构变分框架」能否解困',
   '**修量纲、不修二难**：改写成 λ(x)·(c^2κ^2/sin^2θ − ω^2) 后 [λ] = %s，量纲齐次（V12/V13 解除）；'
   '但约束方程 C(κ) = 0 的形式不变，**仍把 κ 钉成常数** ⇒ V19 的二难原封不动。'
   '唯一已知出口是让 ω 成为**场/局部量** ω(x)（此时 κ(x) = ω(x)sinθ/c 可非常数），'
   '这正是 r41 的 M4（ω 独立演化）—— 与 r41 R35「冗余解除需 M4 ∧ M2-c 同时成立」同源'
   % dstr(gap_V))

# ================================================================ C 段 · 4.3 稳态质量隐式关系（回归复算，对照 r46/r47）
# 来料（本修订版）系数： alpha = hbar/(c sinθ)、beta_U = pi·hbar·l_P/c^3、U_self = pi·hbar·l_P·kappa^2/c
alpha = lambda th: hbar / (c * mp.sin(th))
beta_U = pi * hbar * l_P / c ** 3            # 来料
beta_U_c = pi * hbar * l_P / c               # 最小修正（补回 c^2）
TH = pi / 2                                   # sinθ = 1（拟合驱动的最坏/最紧情形：kappa_crit 最小）


def kappa_roots(m, th=TH, b=None):
    """解 alpha·k − b·k^2 = m 的两根（数值稳定形式）"""
    b = beta_U if b is None else b
    a = alpha(th)
    disc = a * a - 4 * b * m
    sq = mp.sqrt(disc)
    k_minus = 2 * m / (a + sq)
    k_plus = (a + sq) / (2 * b)
    return k_minus, k_plus, disc


K_E, K_E_PLUS, DISC_E = kappa_roots(m_e)
K_MU, K_MU_PLUS, _ = kappa_roots(m_mu)
K_TAU, K_TAU_PLUS, _ = kappa_roots(m_tau)

# Vieta 自检
a0 = alpha(TH)
guard('g25_vieta_sum', rel(K_E + K_E_PLUS, a0 / beta_U) < mp.mpf('1e-40'),
      fx(rel(K_E + K_E_PLUS, a0 / beta_U)))
guard('g26_vieta_prod', rel(K_E * K_E_PLUS, m_e / beta_U) < mp.mpf('1e-40'),
      fx(rel(K_E * K_E_PLUS, m_e / beta_U)))

# C-01 R_c 量纲（回归 r47 W01）
D_RC_IN = ddiv(dmul(D_KAPPA, dpow(D_L, 2)), dim_of({D_L: 1, D_T: -1}))     # [kappa·l_P^2/c] = T
D_RC = dpow(D_RC_IN, F(2, 3))
F_('V24', 'R_c(κ_0) = ((κ_0·l_P^2)/(√2·c))^{2/3} 是长度',
   '机器 [κ_0 l_P^2/c] = %s，取 2/3 次幂得 [R_c] = %s ≠ L。式中含 /c 使 T 指数恒非零'
   ' ⇒ **该「地基式」量纲破缺，且任何 κ_0 量纲都救不回纯长度**。'
   'r47 W01 已对旧版判同一 FAIL ⇒ **本修订版未修此项**' % (dstr(D_RC_IN), dstr(D_RC)))
guard('g27_Rc_is_not_length', D_RC != D_L, dstr(D_RC))

# C-02 r46 修正式（本册交叉印证，不重新发明）
D_RC_FIX_IN = dmul(D_KAPPA, dpow(D_L, F(5, 2)))
D_RC_FIX = dpow(D_RC_FIX_IN, F(2, 3))
kappa_min = mp.sqrt(2) / l_P      # R_c = l_P 对应的 κ（由修正式反解）
P_('V25', '（继承 r46 B08 / r47 W03）修正式 R_c = (κ_0·l_P^{5/2}/√2)^{2/3} 量纲为长度',
   '机器 [κ_0 l_P^{5/2}] = %s，^(2/3) → %s = L ✓（本册不重新发明，仅交叉印证）。'
   '由 R_c = l_P 反解得 κ_min = √2/l_P = %s m^-1' % (dstr(D_RC_FIX_IN), dstr(D_RC_FIX), fx(kappa_min)))
guard('g28_Rc_fixed_is_length', D_RC_FIX == D_L, dstr(D_RC_FIX))

# C-03 U_self 量纲（回归 r47 W04）
D_USELF = dmul(ddiv(dmul(dim_of({D_M: 1, D_L: 2, D_T: -1}), D_L), dim_of({D_L: 1, D_T: -1})),
               dpow(D_KAPPA, 2))
gap_uself = ddiv(dim_of({D_M: 1, D_L: 2, D_T: -2}), D_USELF)
F_('V26', 'U_self = (π·ħ·l_P/c)·κ_0^2 是能量（来料自带「✅ 量纲核验」）',
   '机器 [ħ·l_P/c] = M·L^2（来料这一步写对了），乘 κ_0^2 (L^-2) 得 [U_self] = %s = **质量**，非 J；'
   '缺口 %s = c^2。来料核验段「J·s^2 乘 m^-2 = J」**漏掉了 s^2**（J·s^2·m^-2 = kg·m^2·m^-2 = kg）'
   ' ⇒ 自证错误；r47 W04 对旧版同一判 FAIL ⇒ **本修订版未修此项**'
   % (dstr(D_USELF), dstr(gap_uself)))
guard('g29_uself_dim_is_mass_not_energy', D_USELF == (F(1), F(0), F(0), F(0)), dstr(D_USELF))
guard('g30_uself_gap_is_c2', gap_uself == (F(0), F(2), F(-2), F(0)), dstr(gap_uself))

# C-04 最小修法穷举
hits = []
for ai in range(-3, 4):
    for bi in range(-3, 4):
        for di in range(-3, 4):
            d = dmul(dmul(dpow(dim_of({D_M: 1, D_L: 2, D_T: -1}), ai),
                          dpow(dim_of({D_L: 1, D_T: -1}), bi)),
                     dpow(D_L, di))
            d = dmul(d, dpow(D_KAPPA, 2))
            if d == (F(1), F(2), F(-2), F(0)):
                hits.append((ai, bi, di))
P_('V27', '（本册）量纲最小修法穷举：U_self ∝ ħ^a c^b l_P^d κ_0^2 且要求 [U] = 能量',
   'a,b,d ∈ [−3,3] 共 343 组，命中 %d 组：%s ⇒ 唯一解 U_self ∝ ħ·c·l_P·κ_0^2；'
   '与来料 (π ħ l_P/c) 恰差一个 c^2 ⇒ **同一个 c^2 记账错误**（与 r47 W09 同点）'
   % (len(hits), hits))
guard('g31_uself_minimal_fix_unique', hits == [(1, 1, 1)], str(hits))

# C-05 alpha / beta_U
D_ALPHA = ddiv(dim_of({D_M: 1, D_L: 2, D_T: -1}), dim_of({D_L: 1, D_T: -1}))
D_BETA = ddiv(dmul(dim_of({D_M: 1, D_L: 2, D_T: -1}), D_L), dpow(dim_of({D_L: 1, D_T: -1}), 3))
D_BETA_K2 = dmul(D_BETA, dpow(D_KAPPA, 2))
F_('V28', 'm(κ_0) = α·κ_0 − β_U·κ_0^2 两项同为质量（来料称「量纲完全自洽」）',
   '[α] = %s，[α·κ_0] = %s ✓ 是质量；[β_U] = %s，[β_U·κ_0^2] = %s ≠ M，缺口 %s = c^2'
   ' ⇒ 第二项须乘 c^2 才是质量 ⇒ **修订版未修好量纲**' %
   (dstr(D_ALPHA), dstr(dmul(D_ALPHA, D_KAPPA)), dstr(D_BETA), dstr(D_BETA_K2),
    dstr(ddiv(D_M, D_BETA_K2))))
guard('g32_alpha_kappa_is_mass', dmul(D_ALPHA, D_KAPPA) == (F(1), F(0), F(0), F(0)),
      dstr(dmul(D_ALPHA, D_KAPPA)))
guard('g33_beta_term_not_mass', D_BETA_K2 != (F(1), F(0), F(0), F(0)), dstr(D_BETA_K2))

# C-06 极值代数（数值对拍）
aa, bb = mp.mpf('1.7'), mp.mpf('2.3')
k_crit_num = aa / (2 * bb)
m_max_direct = aa * k_crit_num - bb * k_crit_num ** 2
m_max_closed = aa ** 2 / (4 * bb)
res_alg = rel(m_max_direct, m_max_closed)
P_('V29', '极值代数 κ_crit = α/(2β_U)、m_max = α^2/(4β_U) 自洽',
   '数值对拍（α=1.7, β_U=2.3）：直接代入 %s vs 闭式 %s，相对偏差 %s ⇒ 代数逐项正确，'
   '失效仅在量纲与上游幂次' % (fx(m_max_direct), fx(m_max_closed), fx(res_alg)))
guard('g34_extremum_algebra', res_alg < mp.mpf('1e-50'), fx(res_alg))

# C-07 4.3.2 与 4.3.4 的 c^2 冲突
m_max_432 = hbar * c / (4 * pi * l_P)                 # 来料 4.3.2（sinθ=1）
m_max_434 = M_P_KG / (4 * pi)                          # 来料 4.3.4（sinθ=1）
ratio_432_434 = m_max_432 / m_max_434
D_MMAX432 = ddiv(dmul(dim_of({D_M: 1, D_L: 2, D_T: -1}), dim_of({D_L: 1, D_T: -1})), D_L)
M_('V30', 'm_max = ħc/(4π l_P sin^2θ)（4.3.2）与 m_max = m_P/(4π sin^2θ)（4.3.4）一致',
   '机器 [4.3.2] = %s = **能量**；[4.3.4] = M = 质量 ✓；两式数值比 = %s = c^2'
   ' ⇒ 同一册内两处相差 c^2；4.3.2→4.3.4 的推导把 ħc/l_P 写成 m_P c^2 后**凭空插入一个式中并不存在的 /c^2**'
   '（r47 W10 对旧版同型）' % (dstr(D_MMAX432), fx(ratio_432_434)))
guard('g35_mmax_432_is_energy', D_MMAX432 == (F(1), F(2), F(-2), F(0)), dstr(D_MMAX432))
guard('g36_mmax_ratio_is_c2', rel(ratio_432_434, c ** 2) < mp.mpf('1e-40'), fx(ratio_432_434))

# C-08 修正链（补 c^2）后与 4.3.4 逐位一致
m_max_corr = a0 ** 2 / (4 * beta_U_c)
res_corr = rel(m_max_corr, m_max_434)
C_('V31', '（本册）补回 c^2 后的自洽链：β_U* = πħl_P/c、m_max* = α^2/(4β_U*) = m_P/(4π sin^2θ)',
   '机器 m_max* = %s kg，与来料 4.3.4 的 %s kg 相对偏差 %s ⇒ **4.3.4 才是量纲正确的那一支**，'
   '4.3.2 漏了 c^2。化为能标：m_max* = %s GeV = %s × m_τ'
   % (fx(m_max_corr), fx(m_max_434), fx(res_corr),
      fx(m_max_corr / m_e * mp.mpf('0.51099895') / 1000), fx(m_max_corr / m_tau)))
guard('g37_corrected_mmax_equals_434', res_corr < mp.mpf('1e-40'), fx(res_corr))

# C-09 定义域与稳态域是否相交（回归 r47 W14/W16，本册为 4π 版）
k_crit_c = a0 / (2 * beta_U_c)
ratio_dom = k_crit_c / kappa_min
rc_at_kcrit = (k_crit_c * l_P ** mp.mpf('2.5') / mp.sqrt(2)) ** (mp.mpf(2) / 3)
rc_ratio = rc_at_kcrit / l_P
F_('V32', '稳态域（κ ≤ κ_crit）与定义域（R_c ≥ l_P，即 κ ≥ κ_min = √2/l_P）是否相交',
   '机器 κ_crit* = %s m^-1，κ_min = %s m^-1 ⇒ **κ_crit*/κ_min = %s < 1 ⇒ 两域不相交（空集）**；'
   'R_c(κ_crit*)/l_P = %s < 1 同样自证。'
   '对照 r47（旧版 8π 系数）比值 = 5.627e-2，本修订版 4π 系数把比值改善到 %s，**改善倍数 2.00，但仍 < 1**'
   ' ⇒ 修订把矛盾缩小了一半，未解除' % (fx(k_crit_c), fx(kappa_min), fx(ratio_dom), fx(rc_ratio), fx(ratio_dom)))
guard('g38_empty_set_strict', ratio_dom < 1, fx(ratio_dom))
guard('g39_improvement_factor_two', rel(ratio_dom / mp.mpf('5.627e-2'), mp.mpf('2')) < mp.mpf('1e-2'),
      fx(ratio_dom / mp.mpf('5.627e-2')))

# C-10 「τ 子接近临界曲率、三次项显著」是否成立
frac_tau = K_TAU / k_crit_c
frac_e = K_E / k_crit_c
frac_tau_raw = K_TAU / (a0 / (2 * beta_U))
F_('V33', '§4.3.3「轻粒子二次项主导；接近临界曲率的 τ 子三次项贡献显著、抵消二次项」',
   '机器 κ_τ = %s m^-1，κ_crit* = %s m^-1 ⇒ κ_τ/κ_crit* = %s（电子 %s）；'
   '取来料自身（未修）链则 κ_τ/κ_crit = %s。'
   '二次项相对线性项 = κ/(2κ_crit) ⇒ τ 子也只有 %s 量级 ⇒ **不存在「三次项显著抵消」的参数域**，'
   '该二分是来料的定性想象，数值上差 19~35 个量级' % (fx(K_TAU), fx(k_crit_c), fx(frac_tau),
                                          fx(frac_e), fx(frac_tau_raw), fx(frac_tau / 2)))
guard('g40_tau_far_from_critical', frac_tau < mp.mpf('1e-15'), fx(frac_tau))

# C-11 「θ 趋近 π/2 ⇒ sin^2θ 为极小值」方向
mmax_over_mtau = m_max_corr / m_tau
sin2_needed = (M_P_KG / (4 * pi)) / m_tau
B_('V34', '§4.3.4「要求 m_max > m_τ ⇒ 约束 sin^2θ 为极小值，θ 趋近 π/2，自洽」',
   '**方向写反**：θ → π/2 ⇒ sinθ → 1 ⇒ sin^2θ 取**最大值**而非极小值；'
   '且该约束根本不激活——要使 m_max = m_P/(4π sin^2θ) ≤ m_τ 需 sin^2θ ≥ %s ≫ 1，'
   '而 sin^2θ ≤ 1 恒成立 ⇒ m_max/m_τ ≥ %s ≫ 1 对**任意** θ 都成立'
   ' ⇒ 「自洽」论证不成立，且 m_max 是**恒真空洞、零筛选力**（r47 W20/W21 同族）'
   % (fx(sin2_needed), fx(mmax_over_mtau)))
guard('g41_mmax_zero_screening', mmax_over_mtau > mp.mpf('1e15'), fx(mmax_over_mtau))

# ================================================================ D 段 · 反常磁矩、χ^2 与代码
coef_a = 3 * c / (4 * e_ch * hbar)


def a_tuft(m, kappa, delta):
    """来料 a_TUFT = −3c·cotθ/(4eħ)·m·κ，cotθ = tan(π/2−θ) = tan δ"""
    return -coef_a * mp.tan(delta) * m * kappa


D_A_TUFT = ddiv(dmul(dim_of({D_L: 1, D_T: -1}), dmul(D_M, D_KAPPA)),
                dmul(D_Q, dim_of({D_M: 1, D_L: 2, D_T: -1})))
F_('V35', 'a_TUFT = −(3c·cotθ)/(4eħ)·m·κ_0 是无量纲反常磁矩',
   '机器 [a_TUFT] = %s ≠ 1（反常磁矩须无量纲）；补齐因子须 L^2·Q。'
   '在 {ħ,c,e,m,l_P} 的 ±3 次幂穷举中命中见下条 ⇒ r45 T25 / r46 B11 同族**第 3 次复发**'
   % dstr(D_A_TUFT))
guard('g42_a_tuft_not_dimensionless', D_A_TUFT != D_NONE, dstr(D_A_TUFT))

fix_hits = []
bases = [('hbar', dim_of({D_M: 1, D_L: 2, D_T: -1})), ('c', dim_of({D_L: 1, D_T: -1})),
         ('e', D_Q), ('m', D_M), ('lP', D_L)]
need = ddiv(D_NONE, D_A_TUFT)
for i1 in range(-3, 4):
    for i2 in range(-3, 4):
        for i3 in range(-3, 4):
            for i4 in range(-3, 4):
                for i5 in range(-3, 4):
                    d = dmul(dmul(dmul(dmul(dpow(bases[0][1], i1), dpow(bases[1][1], i2)),
                                       dpow(bases[2][1], i3)), dpow(bases[3][1], i4)),
                             dpow(bases[4][1], i5))
                    if d == need:
                        fix_hits.append((i1, i2, i3, i4, i5))
I_('V36', '（承 V35）a_TUFT 的补齐因子穷举（ħ^i1 c^i2 e^i3 m^i4 l_P^i5，各 ∈ [−3,3]）',
   '目标量纲 %s，共 7^5 = 16807 组，命中 %d 组：%s'
   ' ⇒ 最简解是乘 e·l_P^2（电荷×面积），无物理来源；含 ħ 的解需 m^-1 或 c^-1，'
   '同样不是任何 TUFT 已声明结构 ⇒ **框架内无自然补齐**' % (dstr(need), len(fix_hits), fix_hits[:6]))

# D-03 比值判据（对量纲缺陷免疫）
delta_star = abs(D_E) / (coef_a * m_e * K_E)
a_mu_at_ds = -coef_a * delta_star * m_mu * K_MU
ratio_amu_ae = a_mu_at_ds / D_E
ratio_mass_sq = (m_mu / m_e) ** 2
sign_opposite = (a_mu_at_ds < 0) and (D_MU > 0)
F_('V37', 'a_TUFT 能否同时容纳电子与缪子的 g−2 残差（“打破 m^2”是否成立）',
   '拟合电子（Δa_e = %s）需 δ* = %s rad；此时 a_μ 预言 = %s，而实验残差 Δa_μ = %s'
   ' ⇒ **符号相反**（a_TUFT 对 δ>0 恒负、而缪子残差为正），量级差 %s 倍。'
   '比值 |a_μ/a_e| = %s 与 (m_μ/m_e)^2 = %s 相对偏差 %s ⇒ 因函数形式锁定 a ∝ m·κ 且 κ ∝ m，'
   '任何与 m 无关的补齐系数在比值中消去 ⇒ **该证伪对量纲缺陷免疫**（r42 N02/N03、r46 B26 同值）'
   % (fx(D_E), fx(delta_star), fx(a_mu_at_ds), fx(D_MU), fx(abs(a_mu_at_ds / D_MU)),
      fx(abs(ratio_amu_ae)), fx(ratio_mass_sq), fx(rel(abs(ratio_amu_ae), ratio_mass_sq))))
guard('g43_ratio_equals_mass_squared', rel(abs(ratio_amu_ae), ratio_mass_sq) < mp.mpf('1e-30'),
      fx(rel(abs(ratio_amu_ae), ratio_mass_sq)))
guard('g44_sign_opposite_assert_matches_text', sign_opposite is True, str(sign_opposite))

# D-04 G_th 恒等式复读
G_th0 = c ** 3 * l_P ** 2 / hbar
res_G = rel(G_th0, G_exp)
D_GTH = ddiv(dmul(dpow(dim_of({D_L: 1, D_T: -1}), 3), dpow(D_L, 2)),
             dim_of({D_M: 1, D_L: 2, D_T: -1}))
P_('V38', 'G_th = c^3 l_P^2/(ħ sinθ) 量纲为 G',
   '机器 [G_th] = %s = [G] ✓（这一项量纲正确）' % dstr(D_GTH))
guard('g45_Gth_dim_ok', D_GTH == (F(-1), F(3), F(-2), F(0)), dstr(D_GTH))
I_('V39', 'G_th 是否为新预言',
   'l_P^2 ≡ ħG/c^3 ⇒ G_th(sinθ=1) = %s 与 G_exp = %s 相对偏差 %s（标称 CODATA 位数内的机器零）'
   ' ⇒ **恒等式复读**（r40/r41 M1/r44/r46 B40 同族，本库第 11 次）；'
   '且 δ~1e-40 时 1/sinθ − 1 ~ 1e-80，低于 60~80 位有效位 ⇒ **χ_G 对 θ 零判别力**'
   % (fx(G_th0), fx(G_exp), fx(res_G)))

# D-05 先验盒与最优解是否相交（选项 1 可否执行）
PRIOR_LO = mp.mpf('1e-48')
PRIOR_HI = mp.mpf('1e-40')
a_e_at_lo = -coef_a * PRIOR_LO * m_e * K_E
a_e_at_hi = -coef_a * PRIOR_HI * m_e * K_E
F_('V40', '选项 1（运行 dynesty 嵌套采样扫 θ）执行前可否成立',
   'ptform 给 δ ∈ [%s, %s]；而使 a_TUFT 落进电子残差需 δ* = %s rad，落在盒**下方 8 个量级**。'
   '盒内 |a_TUFT(e)| ∈ [%s, %s]，比 |Δa_e| = %s 大 %s ~ %s 倍'
   ' ⇒ χ^2 在整个先验盒内单调下降、最小值落在人为下边界 δ = 1e-48 处'
   ' ⇒ **运行 dynesty 只能得到先验边界上的伪极小，不是数据驱动的最优 θ**（r47 W23/W28、r48 D06 同族）'
   % (fx(PRIOR_LO), fx(PRIOR_HI), fx(delta_star), fx(abs(a_e_at_lo)), fx(abs(a_e_at_hi)),
      fx(abs(D_E)), fx(abs(a_e_at_lo / D_E)), fx(abs(a_e_at_hi / D_E))))
guard('g46_delta_star_below_prior_box', delta_star < PRIOR_LO, fx(delta_star))

# D-06 χ^2 两档（判决支点：结论依赖未声明的 σ）
def chi2_of(delta, sig_e, sig_mu, sig_g_rel):
    ae = -coef_a * mp.tan(delta) * m_e * K_E
    amu = -coef_a * mp.tan(delta) * m_mu * K_MU
    gth = c ** 3 * l_P ** 2 / (hbar * mp.sin(pi / 2 - delta))
    return (((A_E_QED + ae) - A_E_EXP) / sig_e) ** 2 + \
           (((A_MU_QED + amu) - A_MU_EXP) / sig_mu) ** 2 + \
           ((gth - G_exp) / (G_exp * sig_g_rel)) ** 2


# 在 t = delta/delta_star 上扫描求最小
def chi2_min(sig_e, sig_mu, sig_g_rel):
    """在 t = delta/delta_star ∈ [-5, 5] 上粗扫 + 三分法细化（扫描区间必须覆盖真最小点）"""
    best = (mp.inf, None)
    t = mp.mpf('-5')
    step = mp.mpf('0.002')
    while t <= mp.mpf('5'):
        v = chi2_of(t * delta_star, sig_e, sig_mu, sig_g_rel)
        if v < best[0]:
            best = (v, t)
        t += step
    lo, hi = best[1] - step, best[1] + step
    for _ in range(80):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if chi2_of(m1 * delta_star, sig_e, sig_mu, sig_g_rel) < chi2_of(m2 * delta_star, sig_e, sig_mu, sig_g_rel):
            hi = m2
        else:
            lo = m1
    tm = (lo + hi) / 2
    return chi2_of(tm * delta_star, sig_e, sig_mu, sig_g_rel), tm


chi2_code, t_code = chi2_min(SIG_E_CODE, SIG_MU_CODE, SIG_G_REL_CODE)
chi2_real, t_real = chi2_min(SIG_E_REAL, SIG_MU_REAL, SIG_G_REL_REAL)
chi2_code_at_ds = chi2_of(delta_star, SIG_E_CODE, SIG_MU_CODE, SIG_G_REL_CODE)
chi2_real_at_ds = chi2_of(delta_star, SIG_E_REAL, SIG_MU_REAL, SIG_G_REL_REAL)
M_('V41', 'χ^2 的判决强度（来料代码 σ 档 vs 真实 σ 档）',
   '来料档（σ_e=1e-12, σ_μ=4e-7, σ_G/G=1e-5）：χ^2_min = %s（t = %s），**不失配**；'
   '真实档（σ_e=2.8e-14, σ_μ=5.2e-10, σ_G/G=2.2e-5，口径取自 r44）：χ^2_min = %s（t = %s），**强失配**。'
   '在 δ = δ* 处两档分别为 %s 与 %s。'
   ' ⇒ **同一模型在两种 σ 口径下结论相反**，与 r44「判决支点」同型：'
   '「被实验排除」的强度不能用未声明的 σ 换算；本册不代选，只把 σ 口径显式登记为判据的一部分'
   % (fx(chi2_code), fx(t_code), fx(chi2_real), fx(t_real),
      fx(chi2_code_at_ds), fx(chi2_real_at_ds)))
guard('g47_chi2_two_tier_orders_apart',
      (chi2_code < mp.mpf('1')) and (chi2_real > mp.mpf('100')),
      '%s vs %s' % (fx(chi2_code), fx(chi2_real)))
guard('g48_fx_forces_scientific', 'E' in fx(c ** 2) and abs(mp.mpf(fx(c ** 2)) - c ** 2) < mp.mpf('1'),
      fx(c ** 2))
guard('g49_chi2_min_is_interior_not_boundary',
      abs(t_code) < mp.mpf('4.5') and abs(t_real) < mp.mpf('4.5'),
      't_code=%s t_real=%s' % (fx(t_code), fx(t_real)))

# D-07 θ → π/2 ⇒ 挠率归零
I_('V42', '拟合/相容性把 θ 推向 π/2 的后果',
   '两档约束分开读：①G 通道只要求 sinθ ≈ 1 ⇒ δ ≲ %s rad ⇒ τ/κ = cotθ ≤ %s（很小但非零）；'
   '②而一旦同时要求 a_TUFT 拟合电子残差，δ 必须降到 δ* = %s ⇒ τ/κ ≈ %s ⇒ **挠率实质归零**。'
   ' ⇒ 本修订版的核心卖点「含挠率的螺旋」在它自己的拟合最优点上消失'
   '（r40「三条关系联立只能在 τ=0 的纯圆上相容」同族）'
   % (fx(mp.sqrt(2 * res_G)), fx(mp.sqrt(2 * res_G)), fx(delta_star), fx(delta_star)))

# D-08 代码分支未指定
def kappa_code(m, th=TH):
    """原样执行来料代码：mp.findroot(f, 1e34)"""

    def f(k):
        return (hbar * c * k / mp.sin(th) - (pi * hbar * l_P / c) * k ** 2) / (c ** 2) - m

    try:
        return mp.findroot(f, mp.mpf('1e34'))
    except Exception as ex:
        return None


kc_e = kappa_code(m_e)
kc_mu = kappa_code(m_mu)
kc_tau = kappa_code(m_tau)
branch_note = ''
if kc_e is not None:
    branch_note = 'findroot 落点与小根相对偏差 %s；与大根相对偏差 %s' % (
        fx(rel(kc_e, K_E)), fx(rel(kc_e, K_E_PLUS)))
B_('V43', '来料代码 kappa(m) = mp.findroot(f, 1e34) 的分支选择',
   'm(κ) = ακ − β_Uκ^2 是开口向下的抛物线，给定 m 有**两个**根：'
   '电子 κ_- = %s、κ_+ = %s（相差 %s 倍），缪子、τ 同理。'
   '代码固定起点 1e34 且未声明取哪一支：机器实测 e/μ/τ 落点 = %s / %s / %s；%s。'
   '当前落点恰为小根（物理支），但**这是数值偶然而非声明**；'
   '若落到大根，a_TUFT 会放大 %s 倍 ⇒ 结果不可复现，须显式声明分支'
   % (fx(K_E), fx(K_E_PLUS), fx(K_E_PLUS / K_E), fx(kc_e), fx(kc_mu), fx(kc_tau),
      branch_note, fx(K_E_PLUS / K_E)))

# D-09 外部输入账
I_('V44', '外部输入账（Ω5：自由常数 ≤ 1）',
   '本修订版显式/隐式引入：{θ（普适倾角）}、{l_P（紫外截断，且 l_P^2 ≡ ħG_exp/c^3 把 G 直接注入）}、'
   '{σ（边界表面能密度，未给第一性表达式）}、{ω（约束里的角频率，作为给定常数）}、'
   '{κ_0 的两根取值约定} ⇒ **外部输入 ≥ 4**，与 r46 B35「≥3」、r45 T33 同族 ⇒ 撞 Ω5')

# ================================================================ 汇总与落盘
ORDER = ['PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED', 'MISMATCH']
counts = {k: sum(1 for x in ENTRIES if x['verdict'] == k) for k in ORDER}
guard_ok = sum(1 for g in GUARDS if g['ok'])
guard_all = len(GUARDS)

KEY = {
    'helix_R': fx(R_HEL), 'helix_H': fx(H_HEL), 'helix_L': fx(L_HEL),
    'sin_theta_geo': fx(SIN_TH_GEO), 'cot_theta_geo': fx(cot_geo),
    'omega_eq_Omega_resid': fx(res_eq),
    'old_Omega_over_new': fx(ratio_old),
    'dim_lag_density': dstr(D_LAG),
    'dim_V_constraint': dstr(D_VCON),
    'dim_gap_V_vs_L': dstr(gap_V),
    'dim_EL_lhs': dstr(D_EL_LHS), 'dim_EL_rhs': dstr(D_EL_RHS), 'dim_EL_gap': dstr(gap_EL),
    'dim_H_spiral': dstr(D_HAM),
    'H_grad_coeff_signature_plus': fx(hg_plus), 'H_grad_coeff_signature_minus': fx(hg_minus),
    'dim_U_self_lailiao': dstr(D_USELF), 'c2_gap': fx(c ** 2),
    'dim_a_tuft': dstr(D_A_TUFT),
    'kappa_e': fx(K_E), 'kappa_mu': fx(K_MU), 'kappa_tau': fx(K_TAU),
    'kappa_e_plus_branch': fx(K_E_PLUS), 'branch_ratio': fx(K_E_PLUS / K_E),
    'kappa_crit_corrected': fx(k_crit_c), 'kappa_min_sqrt2_over_lP': fx(kappa_min),
    'domain_ratio_kcrit_over_kmin': fx(ratio_dom),
    'r47_domain_ratio_old': '5.6269769759819129347199949E-2',
    'improvement_factor': fx(ratio_dom / mp.mpf('5.6269769759819129347199949E-2')),
    'Rc_at_kcrit_over_lP': fx(rc_ratio),
    'tau_over_kcrit': fx(frac_tau), 'tau_over_kcrit_raw_chain': fx(frac_tau_raw),
    'm_max_432_energy_J': fx(m_max_432), 'm_max_434_mass_kg': fx(m_max_434),
    'm_max_ratio_is_c2': fx(ratio_432_434),
    'm_max_corrected_kg': fx(m_max_corr), 'm_max_over_m_tau': fx(mmax_over_mtau),
    'delta_star': fx(delta_star),
    'a_mu_at_delta_star': fx(a_mu_at_ds), 'Delta_a_mu': fx(D_MU), 'Delta_a_e': fx(D_E),
    'a_mu_over_a_e': fx(abs(ratio_amu_ae)), 'mass_ratio_squared': fx(ratio_mass_sq),
    'sign_mismatch_factor': fx(abs(a_mu_at_ds / D_MU)),
    'G_th0': fx(G_th0), 'G_exp': fx(G_exp), 'G_rel_resid': fx(res_G),
    'prior_lo': fx(PRIOR_LO), 'prior_hi': fx(PRIOR_HI),
    'a_e_at_prior_lo': fx(abs(a_e_at_lo)), 'a_e_at_prior_hi': fx(abs(a_e_at_hi)),
    'chi2_min_code_sigma': fx(chi2_code), 'chi2_t_code': fx(t_code),
    'chi2_min_real_sigma': fx(chi2_real), 'chi2_t_real': fx(t_real),
    'chi2_at_delta_star_code': fx(chi2_code_at_ds), 'chi2_at_delta_star_real': fx(chi2_real_at_ds),
    'm_P_kg': fx(M_P_KG), 'm_P_GeV': fx(M_P_GEV),
    'findroot_e': fx(kc_e) if kc_e is not None else 'N/A',
    'findroot_mu': fx(kc_mu) if kc_mu is not None else 'N/A',
    'findroot_tau': fx(kc_tau) if kc_tau is not None else 'N/A',
}

if not os.path.isdir(OUTDIR):
    os.makedirs(OUTDIR)

# ---- JSON
payload = {
    'round': ROUND, 'date': DATE, 'tag': TAG,
    'target': 'TUFT-V4.8 修订版 §4.2 稳态基态条件与光速螺旋几何自洽性 + §4.3 稳态质量隐式关系（4π 版）',
    'entries': ENTRIES, 'counts': counts, 'total': len(ENTRIES),
    'guards': GUARDS, 'guard_ok': guard_ok, 'guard_total': guard_all,
    'key_numbers': KEY,
}
with io.open(os.path.join(OUTDIR, TAG + '.json'), 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(payload, ensure_ascii=False, indent=2))

# ---- MD
lines = []
lines.append('# %s · %s 全维审计 · 机器读数' % (ROUND, DATE))
lines.append('')
lines.append('- 来料：《TUFT-V4.8｜修订版 4.2 稳态基态条件与光速螺旋几何自洽性》+《4.3 稳态质量隐式关系（同步更新）》')
lines.append('- 条目：%d（%s）' % (len(ENTRIES), ' / '.join('%s %d' % (k, counts[k]) for k in ORDER if counts[k])))
lines.append('- 自检 guard：%d/%d' % (guard_ok, guard_all))
lines.append('')
lines.append('## 逐条读数')
lines.append('')
lines.append('| id | 判定 | 声称 | 机器读数 |')
lines.append('|---|---|---|---|')
for x in ENTRIES:
    lines.append('| %s | %s | %s | %s |' % (x['id'], x['verdict'],
                                            x['claim'].replace('|', '\\|'),
                                            x['reading'].replace('|', '\\|')))
lines.append('')
lines.append('## 关键数值')
lines.append('')
for k in sorted(KEY):
    lines.append('- %s = %s' % (k, KEY[k]))
lines.append('')
lines.append('## 自检 guard')
lines.append('')
for g in GUARDS:
    lines.append('- %s g_%s：%s' % ('PASS' if g['ok'] else 'FAIL', g['name'], g['detail']))
lines.append('')
with io.open(os.path.join(OUTDIR, TAG + '.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))

# ---- TXT
txt = []
txt.append('TUFT-V4.8 修订版 §4.2/§4.3 全维审计 · %s · %s' % (ROUND, DATE))
txt.append('条目 %d（%s）' % (len(ENTRIES), ' / '.join('%s=%d' % (k, counts[k]) for k in ORDER if counts[k])))
txt.append('自检 guard %d/%d' % (guard_ok, guard_all))
txt.append('')
for x in ENTRIES:
    txt.append('[%s] %s' % (x['verdict'], x['id']))
    txt.append('  声称: %s' % x['claim'])
    txt.append('  读数: %s' % x['reading'])
txt.append('')
for g in GUARDS:
    txt.append('GUARD %s %s %s' % ('PASS' if g['ok'] else 'FAIL', g['name'], g['detail']))
with io.open(os.path.join(OUTDIR, TAG + '_report.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(txt))

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
print('条目 %d（%s）' % (len(ENTRIES), ' / '.join('%s=%d' % (k, counts[k]) for k in ORDER if counts[k])))
print('自检 guard %d/%d' % (guard_ok, guard_all))
for g in GUARDS:
    if not g['ok']:
        print('GUARD FAIL: %s %s' % (g['name'], g['detail']))
sys.exit(0 if guard_ok == guard_all else 1)
