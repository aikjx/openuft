# -*- coding: utf-8 -*-
"""r116｜ROOT·空间光速螺旋实验室：光子以空间光速移动时「内部是否仍在运行」——全情形穷举判决 + 传统数据精算对照

攻击对象 = 一个命题（不是一份来料）：
    P =「光子在空间以光速 c 移动的同时，其内部还在运行（振荡/自转/螺旋/循环/内禀时钟）」

本册把 P 拆成三维情形空间并做笛卡尔积穷举（6 载体 × 3 时间标度 × 2 速率预算 = 36 格），
逐格给出机器判决；再对每一格做可算定价（光速预算 / 转动惯量定理 / 固有时 / 偏振 / OAM / 质量上限），
最后与传统物理（Maxwell、光子 m=0、helicity、E=hnu、多普勒、结构光实验）逐条对照，
并用 5 套方法论立场做稳健性矩阵（结论是否随立场漂移）。

纪律：纯标准库；Decimal 60 位；量纲用 Fraction 四元组 (M,L,T,Q)；
量纲工具本身先过守卫再用于对外判定（本库 r37/r44/r59 教训）；不自推新物理；不改任何既有产物字节。
"""
from __future__ import print_function
import sys
import os
import io
import json
from decimal import Decimal as Dc, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, '源码')
DATA = os.path.join(BASE, '数据')
if not os.path.isdir(DATA):
    os.makedirs(DATA)

ROUND = 'r116'
TAG = '光子内部运行全情形判决与传统对照'
STAMP = '2026-10-20'

# ---------------------------------------------------------------- 量纲工具
# 四元组 (M, L, T, Q)：质量、长度、时间、电荷


def dmul(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dpow(a, n):
    n = int(n)
    return tuple(a[i] * n for i in range(4))


def dstr(a):
    out = []
    sym = ['M', 'L', 'T', 'Q']
    for i in range(4):
        v = a[i]
        if v == 0:
            continue
        out.append(sym[i] + ('^' + str(v) if v != 1 else ''))
    return '·'.join(out) if out else '1'


def deq(a, b):
    return tuple(a) == tuple(b)


REG = {}


def reg(name, dim):
    REG[name] = tuple(dim)
    return REG[name]


D_M = (1, 0, 0, 0)
D_L = (0, 1, 0, 0)
D_T = (0, 0, 1, 0)
D_Q = (0, 0, 0, 1)
D_1 = (0, 0, 0, 0)

# 基本量纲登记（逐个由定义式反锁，不用记忆）
reg('c', ddiv(D_L, D_T))                       # [c] = L T^-1
reg('hbar', dmul(dmul(D_M, dpow(D_L, 2)), ddiv(D_1, D_T)))   # [hbar]=M L^2 T^-1 (E·t)
reg('e', D_Q)
reg('m_e', D_M)
reg('eps0', ddiv(dmul(dpow(D_Q, 2), dpow(D_T, 2)), dmul(dmul(D_M, dpow(D_L, 3)), D_1)))
# 由库仑 F = q^2/(4 pi eps0 r^2)：[eps0] = Q^2 T^2 M^-1 L^-3
reg('kappa', ddiv(D_1, D_L))                   # 曲率
reg('tau', ddiv(D_1, D_L))                     # 挠率
reg('omega', ddiv(D_1, D_T))                   # 角频率
reg('lambda', D_L)

# ---------------------------------------------------------------- 常数（CODATA，标明来源不自推）
PI = Dc('3.14159265358979323846264338327950288419716939937510582097494')
C = Dc('299792458')                       # 定义值，精确
H_BAR = Dc('1.05457181764615639126242800330238374081392527458568e-34')
QBAR = H_BAR
M_E = Dc('9.10938371392808368442978913608078763743833076766321e-31')
ALPHA = Dc('7.29735256429999999999999999999999999999999999999999e-3')
LAMBDA_OPT = Dc('500e-9')                 # 实验室可见光代表波长（人工锚 [C]）

# 派生（现算，不硬编码）
LAM_C = QBAR / (M_E * C)                  # 电子约化康普顿波长
OMEGA_OPT = 2 * PI * C / LAMBDA_OPT       # 对应角频率
NU_OPT = C / LAMBDA_OPT
H_HEL = LAMBDA_OPT / (2 * PI)             # 圆柱螺旋：一周期前进一个波长 ⇒ 2πH = λ

# ---------------------------------------------------------------- 条目系统
ENTRIES = []
GUARDS = []


def add(code, verdict, title, detail):
    ENTRIES.append({'code': code, 'verdict': verdict, 'title': title, 'detail': detail})


def P_(code, t, d):
    add(code, 'PASS', t, d)


def F_(code, t, d):
    add(code, 'FAIL', t, d)


def B_(code, t, d):
    add(code, 'BOUNDARY', t, d)


def I_(code, t, d):
    add(code, 'INFO', t, d)


def C_(code, t, d):
    add(code, 'CORRECTED', t, d)


def guard(name, cond, note):
    GUARDS.append({'name': name, 'ok': bool(cond), 'note': note})
    return bool(cond)


def fv(x, n=25):
    """定点科学计数法输出（Decimal 高位数下 quantize 会抛 InvalidOperation）"""
    try:
        return format(Dc(x), '.' + str(n) + 'E')
    except Exception:
        return str(x)


def rel(a, b):
    """相对偏差 |a-b|/|b|"""
    b = Dc(b)
    if b == 0:
        return Dc('Infinity')
    return abs(Dc(a) - b) / abs(b)


# ---------------------------------------------------------------- 守卫（量纲工具自检，先于对外判定）
guard('G0-1 dim_mul_c_hbar', deq(dmul(REG['c'], REG['hbar']), (1, 3, -2, 0)),
      '[c*hbar] = M L^3 T^-2')
guard('G0-2 eps0_from_coulomb',
      deq(dmul(REG['eps0'], dpow(D_L, 2)), ddiv(dmul(dpow(D_Q, 2), dpow(D_T, 2)), dmul(D_M, dpow(D_L, 1)))),
      'eps0*r^2 = Q^2 T^2 / (M L)')
guard('G0-3 hbar_over_mc_is_length', deq(ddiv(REG['hbar'], dmul(REG['m_e'], REG['c'])), D_L),
      '[hbar/(m c)] = L')
guard('G0-4 kappa_sq_plus_tau_sq',
      deq(dpow(REG['kappa'], 2), ddiv(dpow(REG['omega'], 2), dpow(REG['c'], 2))),
      '[kappa^2] = [omega^2/c^2] = L^-2')
guard('G0-5 omega_dim', deq(REG['omega'], (0, 0, -1, 0)), '[omega] = T^-1')
guard('G0-6 lam_c_value', rel(LAM_C, Dc('3.8615926e-13')) < Dc('1e-6'),
      'lambda_C(e) 复算 ' + fv(LAM_C) + ' m 落在 3.8616e-13 附近')
guard('G0-7 alpha_lt_1', Dc('0') < ALPHA < Dc('1'), 'alpha = ' + fv(ALPHA))
guard('G0-8 helix_H_pos', H_HEL > 0 and rel(2 * PI * H_HEL, LAMBDA_OPT) < Dc('1e-50'),
      '2*pi*H = lambda 残差机器零')

# ================================================================ A 段：情形空间穷举（6×3×2 = 36 格）
# 维度 A：什么在「运行」（载体层）
CARRIERS = [
    # id, 名称, 是否需要静质量 m>0, 是否属场层, 说明
    ('A1', '光子沿螺旋空间轨迹前进（轨迹层）', False, False, 'κ=R/L², τ=H/L², 切向速率 c'),
    ('A2', '光子自身自转（刚体转动层）', True, False, '需转动惯量 I=a·m·R²'),
    ('A3', '场矢量在横向平面内旋转（偏振层）', False, True, '圆偏振 E 以 ω 旋转'),
    ('A4', '场能量在横向做环流（坡印廷涡旋/OAM）', False, True, 'S 有方位角分量，能流线螺旋'),
    ('A5', '光子有内部结构/组分相互运动（亚结构层）', True, False, '需可定域的内部中心'),
    ('A6', '光子携带内禀时钟（固有时层）', False, False, '内部周期数 N=Δτ·ν'),
]
# 维度 B：「运行」的时间标度参照
CLOCKS = [
    ('B1', '以光子自身固有时计（dτ）'),
    ('B2', '以实验室坐标时计（dt）'),
    ('B3', '以光源共动时计'),
]
# 维度 C：内部运行与外禀平动的速率预算关系
BUDGETS = [
    ('C1', '内部运行占用平动预算（总切向速率 = c）'),
    ('C2', '内部运行不占预算（额外叠加）'),
]

CELLS = []


def cell_metric(a, b, c):
    """每格给出至少一个可算读数（Decimal 现算，不硬编码）"""
    if a == 'A1':
        # v_z/c = H/L = cosθ；取 R=H 的代表构型（最"像螺旋"的一格）
        r = H_HEL
        h = H_HEL
        L = (r * r + h * h).sqrt()
        return ('v_z/c(R=H)', h / L)
    if a == 'A2':
        # 自转模型的赤道速度（见 B 段定理）：v_eq/c = 1/sqrt(a_shape)，取实心球 a=2/5
        a_sh = Dc('0.4')
        return ('v_eq/c(实心球)', Dc(1) / a_sh.sqrt())
    if a == 'A3':
        return ('偏振旋转角频率/s^-1', OMEGA_OPT)
    if a == 'A4':
        # 坡印廷倾角上界：1-cosα ≤ α²/2，α = lλ/(2πr)，取 l=1, r=10 μm
        r_beam = Dc('1e-5')
        alp = LAMBDA_OPT / (2 * PI * r_beam)
        return ('1-cosα 上界(l=1,r=10μm)', alp * alp / 2)
    if a == 'A5':
        return ('可定域内部中心', Dc('nan'))
    # A6
    return ('内部周期数 N=Δτ·ν', Dc(0))


def judge(a, b, c):
    """逐格判决。规则按依赖顺序，命中即返回（规则编号写进 reason）"""
    if a == 'A2' or a == 'A5':
        if a == 'A2':
            return ('FAIL', 'R1-需静质量',
                    '自转需转动惯量 I=a·m·R²，光子 m=0 ⇒ I=0；且 m_γ 上限（PDG 量级 1e-18 eV）不容')
        return ('BOUNDARY', 'R8-不可判定',
                'm=0 且自旋>0 的粒子无 Newton–Wigner 位置算符，「内部」无定域中心可定义')
    if b == 'B1':
        return ('FAIL', 'R2-固有时为零',
                '类光世界线 ds²=0 ⇒ Δτ≡0 ⇒ 任何有限 ν 下内部周期数 N=Δτ·ν=0（不是「走得慢」，是恒零）')
    if a == 'A6':
        return ('FAIL', 'R9-非内禀',
                '「内禀时钟」要求与参考系无关；B2/B3 下 N=Δt·ν 随观测者变（多普勒）⇒ 与「内禀」定义直接冲突')
    if a == 'A1':
        if c == 'C1':
            return ('FAIL', 'R3-光速预算',
                    '沿非退化螺旋以切向速率 c 前进 ⇒ 轴向推进 v_z=c·H/L<c，被真空光速预算压到 R≤1.1e-16 m（见 B1）')
        return ('FAIL', 'R4-超光速', '不占预算则切向速率 > c ⇒ 与 v=c 公设自斥')
    if a == 'A3':
        if c == 'C1':
            return ('FAIL', 'R6-占预算则减速', '偏振旋转若占用平动预算 ⇒ v_z<c，与圆偏振沿 z 以 c 传播冲突')
        return ('PASS', 'R5-场层成立', '场矢量旋转不占平动预算、与 Maxwell 完全一致；代价=零新增（见 D1）')
    if a == 'A4':
        if c == 'C1':
            return ('BOUNDARY', 'R7-条件成立',
                    '真实现象（结构光坡印廷螺旋）；但属光束横模属性，减速量 ≤α²/2 随束宽消失')
        return ('FAIL', 'R4-超光速', '不占预算 ⇒ 能流速率 > c')
    return ('BOUNDARY', 'R0-未覆盖', '')


for _a in CARRIERS:
    for _b in CLOCKS:
        for _c in BUDGETS:
            v, k, note = judge(_a[0], _b[0], _c[0])
            mk, mv = cell_metric(_a[0], _b[0], _c[0])
            CELLS.append({'carrier': _a[0], 'carrier_name': _a[1], 'clock': _b[0],
                          'budget': _c[0], 'verdict': v, 'rule': k, 'note': note,
                          'metric_key': mk, 'metric_val': (None if mv != mv else fv(mv))})

VC = {}
for _x in CELLS:
    VC[_x['verdict']] = VC.get(_x['verdict'], 0) + 1
# 按载体聚合：只看「是否存在任何一格存活」
SURV = {}
for _a in CARRIERS:
    vs = set(x['verdict'] for x in CELLS if x['carrier'] == _a[0])
    if 'PASS' in vs:
        SURV[_a[0]] = 'PASS'
    elif 'BOUNDARY' in vs:
        SURV[_a[0]] = 'BOUNDARY'
    else:
        SURV[_a[0]] = 'FAIL'

guard('G-A1 cell_count', len(CELLS) == 36, '情形格数 6*3*2 = ' + str(len(CELLS)))
guard('G-A2 verdict_sum', sum(VC.values()) == 36, '判决总数守恒 ' + str(VC))
guard('G-A3 a1_all_fail', SURV['A1'] == 'FAIL', 'A1 轨迹螺旋六格全 FAIL')
guard('G-A4 a2_all_fail', SURV['A2'] == 'FAIL', 'A2 自转六格全 FAIL')
guard('G-A5 a6_all_fail', SURV['A6'] == 'FAIL', 'A6 内禀时钟六格全 FAIL')

F_('A01', '情形空间闭合：36 格全部给出判决',
   '载体 6（A1 轨迹螺旋 / A2 自转 / A3 偏振场旋转 / A4 坡印廷涡旋 / A5 亚结构 / A6 内禀时钟）× 时间标度 3（B1 固有时 / B2 坐标时 / B3 光源时）× 速率预算 2（C1 占预算 / C2 不占预算）= **36 格**，无一格留空；'
   '判决分布 ' + str(VC) + '。')

F_('A02', '★A1 轨迹螺旋：六格全 FAIL（两条互斥的路都被堵死）',
   'C1（占预算）⇒ v_z=c·H/L<c，与真空光速预算冲突（见 B1，R≤' + fv(Dc('1.1254e-16')) + ' m）；'
   'C2（不占预算）⇒ 切向速率超过 c ⇒ 与「光子以 c 运动」自斥。'
   '两条路互斥且穷尽 ⇒ **A1 无存活格**。B1 参照下更是双重失败（Δτ≡0，连「走了多久」都无定义）。')

F_('A03', '★A2 自转：需静质量，与光子 m=0 及 m_γ 上限互斥',
   '转动角动量 S=I·ω、I=a·m·R² ⇒ m=0 时 I=0 ⇒ 无法承载 ħ；以等效质量 m_eff=ħω/c² 顶替则触发 B2 的超光速定理。'
   '六格全 FAIL（其中 B1 参照另加「Δτ=0」一重）。')

P_('A04', '★A3 偏振场旋转：唯一在 C2 下成立的格（但代价是零新增）',
   '圆偏振 E=E₀(cos(kz−ωt), sin(kz−ωt), 0)：场矢量以角频率 ω=' + fv(OMEGA_OPT) + ' s⁻¹ 旋转，'
   '而能流 S∝ẑ、E·ẑ≡0 ⇒ 旋转不占平动预算、v_z=c 不变 ⇒ **2 格 PASS**（B2/B3 参照 × C2 不占预算；'
   '其余 4 格分别死于 B1 固有时与 C1 占预算）。'
   '代价：这与 Maxwell 圆偏振**逐字相同**，不产生任何新物理（D1 判定为恒等复读）。')

B_('A05', 'A4 坡印廷涡旋：真实现象，但只在「光束模式」层成立',
   '结构光（携 OAM 的 LG/Bessel 束）能流线确为螺旋，轴向能流 v_z=c·cosα，减速量 ≤α²/2；'
   '取 l=1、r=10 μm ⇒ 1−cosα ≤ ' + fv((LAMBDA_OPT / (2 * PI * Dc('1e-5'))) ** 2 / 2) + '。'
   '属**横模结构**不是单光子内部属性，且随束宽增大 α→0 而消失 ⇒ BOUNDARY。')

B_('A06', 'A5 亚结构：不可判定（不是通过，也不是失败）',
   'm=0 且自旋>0 的粒子不存在 Newton–Wigner 位置算符，「光子内部」缺乏定域中心 ⇒ '
   '「内部是否有组分在动」在本框架内**无定义**，机器不给 PASS 也不给 FAIL。')

F_('A07', '★A6 内禀时钟：三格全 FAIL，且两种参照下理由不同',
   'B1（固有时）⇒ Δτ≡0 ⇒ N=Δτ·ν=0，时钟读数恒零；B2/B3 ⇒ N=Δt·ν 随观测者变（多普勒）⇒ 与「内禀」二字直接矛盾。'
   '⇒ **光子没有内禀时钟**这一结论不依赖参考系选择。')

def helix_budget(delta):
    d = Dc(delta)
    ratio = (Dc(1) / ((Dc(1) - d) ** 2) - Dc(1)).sqrt()   # R/H 上界
    r_max = H_HEL * ratio
    L = (H_HEL ** 2 + r_max ** 2).sqrt()
    return ratio, r_max, Dc(1) / (r_max / (L ** 2))       # ratio, R_max, 曲率半径 1/κ


BUDGET_ROWS = []
for _dl in ['1e-3', '1e-6', '1e-9', '1e-15', '1e-18']:
    _ra, _rm, _rd = helix_budget(_dl)
    BUDGET_ROWS.append({'delta': _dl, 'R_over_H': fv(_ra), 'R_max_m': fv(_rm),
                        'R_max_over_lambdaC': fv(_rm / LAM_C),
                        'curvature_radius_m': fv(_rd),
                        'curv_radius_over_lambda': fv(_rd / LAMBDA_OPT)})

_ratio18, _rmax18, _rad18 = helix_budget('1e-18')

guard('G-B1 budget_monotone',
      all(Dc(BUDGET_ROWS[i + 1]['R_max_m']) < Dc(BUDGET_ROWS[i]['R_max_m']) for i in range(4)),
      'δ 越严 R_max 越小')
guard('G-B2 small_delta_limit', rel(_ratio18, (Dc(2) * Dc('1e-18')).sqrt()) < Dc('1e-9'),
      '小 δ 极限 R/H → sqrt(2δ) = ' + fv(_ratio18))
guard('G-B3 degenerates_to_line', _rad18 / LAMBDA_OPT > Dc('1e7'),
      'δ=1e-18 曲率半径/波长 = ' + fv(_rad18 / LAMBDA_OPT))

F_('B01', '★光速预算定理：观测把螺旋半径压到 λ_C 的万分之三以下',
   '沿圆柱螺旋以切向速率 c 前进 ⇒ 轴向 v_z=c·H/√(H²+R²) < c。要求 |1−v_z/c|≤δ ⇒ R/H≤√(1/(1−δ)²−1)≈√(2δ)。'
   '取 λ=500 nm（H=λ/2π=' + fv(H_HEL) + ' m）：δ=1e-3 ⇒ R≤' + BUDGET_ROWS[0]['R_max_m'] +
   ' m；δ=1e-18（现代洛伦兹/真空光速检验量级）⇒ R≤**' + fv(_rmax18) + ' m**，仅为电子约化康普顿波长 ' +
   fv(LAM_C) + ' m 的 ' + fv(_rmax18 / LAM_C) + ' 倍；曲率半径 1/κ=**' + fv(_rad18) +
   ' m**，是波长的 ' + fv(_rad18 / LAMBDA_OPT) + ' 倍 ⇒ **轨迹必然是直线**。')

SHAPES = [('实心球 a=2/5', Dc('0.4')), ('圆盘/柱 a=1/2', Dc('0.5')),
          ('薄球壳 a=2/3', Dc(2) / Dc(3)), ('薄环 a=1', Dc(1))]
SPIN_ROWS = []
SPIN_RAW = []
for _nm, _a in SHAPES:
    v_eq = Dc(1) / _a.sqrt()
    SPIN_RAW.append(v_eq)
    SPIN_ROWS.append({'shape': _nm, 'v_eq_over_c': fv(v_eq),
                      'R_required_m': fv(C / (OMEGA_OPT * _a.sqrt())),
                      'R_req_over_R_max': fv((C / (OMEGA_OPT * _a.sqrt())) / _rmax18)})

guard('G-B4 spin_theorem', rel(SPIN_RAW[0], Dc(1) / Dc('0.4').sqrt()) < Dc('1e-50'),
      '自转定理 v_eq/c = 1/sqrt(a) 不依赖 λ（用原始 Decimal 比对，不用 25 位格式化串）')
guard('G-B5 spin_superluminal', Dc(SPIN_ROWS[0]['v_eq_over_c']) > 1,
      'a<1 刚体必超光速（实心球 ' + SPIN_ROWS[0]['v_eq_over_c'] + ' c）')

F_('B02', '★自转载荷定理（与半径/波长无关）：任何 a<1 的刚体自转光子必然赤道超光速',
   'S=Iω=ħ、I=a·m·R²，以等效质量 m_eff=ħω/c² 顶替 ⇒ R=c/(ω√a)、赤道速度 v_eq=ωR=**c/√a**（R 与 ω 全部约掉）。'
   '实心球 ⇒ ' + SPIN_ROWS[0]['v_eq_over_c'] + ' c（超光速 ' +
   fv((Dc(SPIN_ROWS[0]['v_eq_over_c']) - 1) * 100) + '%）；盘 ⇒ ' + SPIN_ROWS[1]['v_eq_over_c'] +
   ' c；薄环 a=1 恰给 v_eq=c（但环上无质量可束缚）。叠加 B1：薄环要求 R=' + SPIN_ROWS[3]['R_required_m'] +
   ' m，光速预算只允许 R≤' + fv(_rmax18) + ' m，超出 **' + SPIN_ROWS[3]['R_req_over_R_max'] + ' 倍** ⇒ 双杀。')

DOPPLER_ROWS = []
for _b in ['0.1', '0.5', '0.9']:
    _bt = Dc(_b)
    _fac = ((Dc(1) + _bt) / (Dc(1) - _bt)).sqrt()
    DOPPLER_ROWS.append({'beta': _b, 'shift_factor': fv(_fac),
                         'lambda_obs_nm': fv(LAMBDA_OPT * _fac * Dc('1e9'))})

_bt = Dc('0.9')
_gam = Dc(1) / (Dc(1) - _bt ** 2).sqrt()
_E = _gam * M_E * C ** 2
_p = _gam * M_E * (_bt * C)
_inv = (_E ** 2 - (_p * C) ** 2).sqrt()
INV_RESID = rel(_inv, M_E * C ** 2)

guard('G-B6 electron_invariant', INV_RESID < Dc('1e-50'), '电子不变量残差 ' + fv(INV_RESID))
guard('G-B7 doppler_ordered', Dc(DOPPLER_ROWS[2]['shift_factor']) > Dc(DOPPLER_ROWS[0]['shift_factor']),
      '红移因子随 β 单调增')

F_('B03', '★内禀性判据：光子的 ω 随参考系变，电子的 m_e 不变 ⇒ ω 不是内禀属性',
   '多普勒 λ′=λ√((1+β)/(1−β))（源 500 nm）：β=0.1 ⇒ ' + DOPPLER_ROWS[0]['lambda_obs_nm'] +
   ' nm；β=0.5 ⇒ ' + DOPPLER_ROWS[1]['lambda_obs_nm'] + ' nm；β=0.9 ⇒ ' + DOPPLER_ROWS[2]['lambda_obs_nm'] +
   ' nm。对照电子：β=0.9 时 √(E²−p²c²)=' + fv(_inv) + ' J 与 m_ec²=' + fv(M_E * C ** 2) +
   ' J 相对残差 ' + fv(INV_RESID) + ' —— 不变质量是洛伦兹标量，而频率不是。'
   '⇒ 把光子的 ω 称作「内部运行速率」等于把关系量当内禀量。')

SAMP = [(1, 0), (0, 1), (-1, 0), (0, -1)]        # (cosφ, sinφ) 在 φ=0, π/2, π, 3π/2 的精确值
POL_NORM = all(abs(Dc(c) ** 2 + Dc(s) ** 2 - 1) == 0 for c, s in SAMP)
guard('G-B8 pol_norm_const', POL_NORM, '圆偏振 |E| 恒定（sin²+cos²=1 精确成立，未用数值三角）')

OMEGA_HELIX = C / (LAMBDA_OPT / (2 * PI))
RES_OMEGA = rel(OMEGA_HELIX, OMEGA_OPT)
OMEGA_HELIX_2 = C / (2 * LAMBDA_OPT / (2 * PI))
RES_OMEGA_2 = rel(OMEGA_HELIX_2, OMEGA_OPT)

guard('G-B9 omega_identity', RES_OMEGA < Dc('1e-50'), 'L=λ/2π 时 Ω 与 ω 残差 ' + fv(RES_OMEGA))
guard('G-B10 omega_not_free', RES_OMEGA_2 > Dc('0.4'), 'L 改为 2λ/2π 时偏差 ' + fv(RES_OMEGA_2))

C_('B04', '★「螺旋角频率 = 光子频率」是反解定义而非推导',
   'Ω=c/L 与 ω=2πc/λ 相等的充要条件是 L=λ/2π（机器残差 ' + fv(RES_OMEGA) + '）。'
   '换参检验：L 取 2λ/2π（每两周期前进一个波长）⇒ Ω 相对 ω 偏差 ' + fv(RES_OMEGA_2) +
   ' ⇒ L 是被 E=ħω 反解锁定的，该式信息量等价于「每周期前进一个波长」这句几何声明，零新增。')

OAM_ROWS = []
for _r in ['1e-3', '1e-5', '1e-6']:
    _rr = Dc(_r)
    _alp = LAMBDA_OPT / (2 * PI * _rr)                    # tanα ≈ α = lλ/(2πr)，l=1
    OAM_ROWS.append({'r_m': _r, 'alpha_rad': fv(_alp), 'slowdown_upper': fv(_alp * _alp / 2)})

guard('G-B11 oam_monotone',
      Dc(OAM_ROWS[2]['slowdown_upper']) > Dc(OAM_ROWS[0]['slowdown_upper']),
      '束宽越小减速上界越大')
guard('G-B12 oam_vanishes', Dc(OAM_ROWS[0]['slowdown_upper']) < Dc('1e-8'),
      'r=1mm 时减速上界 ' + OAM_ROWS[0]['slowdown_upper'] + ' ⇒ 宏观束宽下效应消失')

B_('B05', 'OAM/坡印廷涡旋：唯一真实的「能流螺旋」，但它是光束横模属性',
   '携轨道角动量的结构光其坡印廷矢量含方位角分量，能流线确为螺旋；倾角 α=lλ/(2πr)，'
   '轴向减速 1−cosα ≤ α²/2（不等式界，无需数值三角）：r=1 mm ⇒ ≤' + OAM_ROWS[0]['slowdown_upper'] +
   '；r=10 μm ⇒ ≤' + OAM_ROWS[1]['slowdown_upper'] + '；r=1 μm ⇒ ≤' + OAM_ROWS[2]['slowdown_upper'] + '。'
   '⇒ 效应随束宽平方反比消失，且属**模式**属性（同一束内所有光子共享），不是单个光子的内部运行。'
   '外部锚：Giovannini 等 2015 实测结构光慢于 c（量级 1e-5 级）与本量级相容，'
   '具体数值**待官方原文核对**（标 needs_official_confirmation，本册不以该数值作判据）。')

MGAM_EV = Dc('1e-18')            # PDG 量级的光子静质量上限（[C] 人工锚，只作量级参照）
MASS_ROWS = []
for _EeV in ['1', '1e-6']:
    _x = MGAM_EV / Dc(_EeV)      # m_γc²/E
    MASS_ROWS.append({'E_eV': _EeV, 'x': fv(_x), 'slowdown': fv(_x * _x / 2)})

guard('G-B13 mass_unmeasurable', Dc(MASS_ROWS[1]['slowdown']) < Dc('1e-20'),
      'E=1e-6 eV 时减速 ' + MASS_ROWS[1]['slowdown'] + ' ⇒ 即便取上限也不可测')

I_('B06', '光子静质量上限与「内部运行」无因果关系（两侧都不支持）',
   '若 m_γ>0 ⇒ v/c=√(1−(m_γc²/E)²)，减速 ≈(m_γc²/E)²/2：m_γc²=1e-18 eV、E=1 eV ⇒ ' + MASS_ROWS[0]['slowdown'] +
   '；E=1e-6 eV ⇒ ' + MASS_ROWS[1]['slowdown'] + '。'
   '⇒ 一方面质量上限的存在推不出任何内部周期；另一方面「内部运行」也并不要求 m_γ>0。两者无因果链，不得互引为证据。')

# ================================================================ C 段：与传统物理逐条精算对照
K_OPT = 2 * PI / LAMBDA_OPT
E_PHOTON = QBAR * OMEGA_OPT
P_PHOTON = QBAR * K_OPT
RES_EP = rel(E_PHOTON / (P_PHOTON * C), Dc(1))

guard('G-C1 massless_dispersion', RES_EP < Dc('1e-50'), 'E/(pc) = ω/(kc) 残差 ' + fv(RES_EP))

P_('C01', '传统支 1（Maxwell 平面波）通过，且它已穷尽「内部运行」所有成立的含义',
   '真空无源 Maxwell 的解就是横波 E⊥k、B⊥k、E⊥B；场分量以 ω 振荡（' + fv(OMEGA_OPT) + ' s⁻¹），'
   '但这是**场的**振荡，与「光子有个内部在跑」是两层命题。本册 36 格里唯一 PASS 的 A3（场矢量旋转）'
   '正是 Maxwell 圆偏振 ⇒ 与教科书逐字相同，零新增。')

P_('C02', '传统支 2（E=ħω, p=ħk ⇒ E=pc）机器零',
   'E/(pc)=ω/(kc)，k=2π/λ ⇒ 比值 ' + fv(E_PHOTON / (P_PHOTON * C)) + '，残差 ' + fv(RES_EP) +
   ' ⇒ 无静质量、速率恰为 c；任何「内部运行占用平动预算」的模型都会把该比值推离 1（B1 已定价）。')

P_('C03', '传统支 3（m=0 自旋 1 ⇒ 只有 helicity ±1 两态）结构性排除「自转」叙事',
   '有质量自旋 1 粒子有 2s+1=3 个投影态；m=0 的小群退化为 E(2) ⇒ 纵向投影被规范消去，'
   '物理光子只剩 ±1 **两态**。机器计数：3 vs 2，差 1。'
   '「光子内部在自转」隐含 3 个取向（含 0 投影），与横向两偏振直接互斥 ⇒ A2 在结构层再死一次。')

P_('C04', '传统支 4（类光 ds²=0 ⇒ 无固有时）与 A6/B1 完全同向',
   '类光世界线的固有时微元恒零 ⇒ 不能为光子定义「内部经历的时间」。'
   '本册 B1 参照下的 12 格（6 载体 × 2 预算）全部因此 FAIL，与传统结论一致。')

C_('C05', '传统支 5（真空无双折射、无色散）：继承 r53 E05，本册不重判',
   '真空中两偏振同速、无旋光，r53 已用真平面波残差 4.04e-12/1.98e-11 判定；'
   '本册只继承，不重复裁定，也不把它计入本册新增条目。')

COMPARE = [
    ('内部运行 = 沿螺旋轨迹前进', 'null 测地线（直线）', 'B01：R≤1.1e-16 m、曲率半径≥56 m', 'FAIL', '被光速预算排除'),
    ('内部运行 = 自转', 'helicity ±1，无静止系', 'B02：v_eq=c/√a ≥ 1.41c', 'FAIL', '超光速 + 态数互斥'),
    ('内部运行 = 内禀时钟', 'ds²=0，无固有时', 'A07：N=Δτ·ν≡0', 'FAIL', '时钟读数恒零'),
    ('内部运行 = 内部频率 ω', 'E=ħω（关系量，随观测者变）', 'B03：多普勒 500→2179 nm', 'FAIL', '关系量被当内禀量'),
    ('内部运行 = 场矢量旋转', '圆偏振（Maxwell）', 'B04：Ω≡ω，残差 ' + fv(RES_OMEGA), 'PASS', '成立但零新增'),
    ('内部运行 = 能流环流', 'OAM 结构光坡印廷螺旋', 'B05：减速 ≤α²/2 且随束宽消失', 'BOUNDARY', '真实现象，属模式层'),
    ('内部运行 = 亚结构', '无定域位置算符', 'A06：不可定义', 'BOUNDARY', '不可判定，非通过'),
]

C_('C06', '★对照总表：七种「内部运行」定义逐一比价，无一给出新物理',
   '机器比对结果 ' + str([x[3] for x in COMPARE]) + '。三条 PASS/BOUNDARY 的读法分别是：'
   '「场矢量旋转」= Maxwell 圆偏振（零新增）、「能流环流」= 结构光横模（模式层，非单光子）、'
   '「亚结构」= 不可判定。⇒ **「光子内部还在运行」这一命题没有任何一种读法能同时满足「成立」与「新增」。**')

# ================================================================ D 段：五套方法论立场 × 六种载体 的稳健性矩阵
# （对应本库「最伟大的科学家处理模式」：多套自洽判据集交叉，看结论是否随判据集漂移）
_R = H_HEL
_HH = H_HEL
_LL = (_R ** 2 + _HH ** 2).sqrt()
_KAPPA = _R / (_LL ** 2)
_TAU = _HH / (_LL ** 2)
_OMH = C / _LL
RES_TRIAD = rel(_KAPPA ** 2 + _TAU ** 2, (_OMH / C) ** 2)

guard('G-D1 triad_identity', RES_TRIAD < Dc('1e-50'),
      '螺旋几何恒等式 κ²+τ²=(ω/c)² 残差 ' + fv(RES_TRIAD) + ' ⇒ 几何主义下 A1 确实自洽')

STANCES = [
    ('S1 严格观测主义', '只认可测量：光速预算、多普勒、偏振、m_γ 上限'),
    ('S2 结构/对称性主义', '只认洛伦兹协变与类光结构：ds²=0、小群 E(2)、不变量'),
    ('S3 几何主义', '只要求螺旋几何自洽：κ²+τ²=(ω/c)² 等恒等式成立'),
    ('S4 场论主义', '只认 Maxwell/QFT 可观测量与算符'),
    ('S5 构造主义', '要求可构造机制 + 可证伪预言'),
]
MATRIX = {
    ('S1', 'A1'): ('FAIL', '光速预算把 R 压到 ' + fv(_rmax18) + ' m'),
    ('S2', 'A1'): ('FAIL', '平直时空 null 测地线曲率为 0（继承 r54 N19）'),
    ('S3', 'A1'): ('PASS', '几何恒等式残差 ' + fv(RES_TRIAD) + '（自洽）'),
    ('S4', 'A1'): ('FAIL', 'Maxwell 真空解无螺旋轨迹'),
    ('S5', 'A1'): ('FAIL', 'R 上界不可测 ⇒ 无可证伪预言'),
    ('S1', 'A2'): ('FAIL', 'v_eq=c/√a ≥ 1.41c'),
    ('S2', 'A2'): ('FAIL', 'm=0 ⇒ helicity ±1 两态，无 3 投影'),
    ('S3', 'A2'): ('FAIL', '自转无几何必然性，且需 m>0'),
    ('S4', 'A2'): ('FAIL', '无静止系可定义自转'),
    ('S5', 'A2'): ('FAIL', '无构造'),
    ('S1', 'A3'): ('PASS', '偏振可直接测量'),
    ('S2', 'A3'): ('PASS', '与横波协变结构一致'),
    ('S3', 'A3'): ('NA', '非几何命题'),
    ('S4', 'A3'): ('PASS', 'Maxwell 圆偏振'),
    ('S5', 'A3'): ('PASS', '可构造可证伪，但零新增'),
    ('S1', 'A4'): ('PASS', '结构光减速可测（上界 α²/2）'),
    ('S2', 'A4'): ('PASS', '能流螺旋协变成立'),
    ('S3', 'A4'): ('BOUNDARY', '倾角依赖束宽，非内禀几何'),
    ('S4', 'A4'): ('PASS', 'OAM 是横模解'),
    ('S5', 'A4'): ('PASS', '可构造（LG/Bessel 束）'),
    ('S1', 'A5'): ('BOUNDARY', '无观测量可判定'),
    ('S2', 'A5'): ('BOUNDARY', '无定域中心（无位置算符）'),
    ('S3', 'A5'): ('NA', '非几何命题'),
    ('S4', 'A5'): ('BOUNDARY', '无定义'),
    ('S5', 'A5'): ('BOUNDARY', '不可构造'),
    ('S1', 'A6'): ('FAIL', '多普勒：N 随观测者变'),
    ('S2', 'A6'): ('FAIL', 'ds²=0 ⇒ Δτ≡0'),
    ('S3', 'A6'): ('FAIL', '类光曲线无 Frenet 弧长参数（继承 r56 C13）'),
    ('S4', 'A6'): ('FAIL', '无固有时算符'),
    ('S5', 'A6'): ('FAIL', '不可构造'),
}

ROBUST = {}
for _a in CARRIERS:
    vs = [MATRIX[(s[0].split()[0], _a[0])][0] for s in STANCES]
    vs2 = [v for v in vs if v != 'NA']
    ROBUST[_a[0]] = {'votes': vs, 'stable': len(set(vs2)) == 1, 'summary': dict((v, vs2.count(v)) for v in set(vs2))}

guard('G-D2 matrix_complete', len(MATRIX) == 30, '矩阵 5*6 = ' + str(len(MATRIX)))
guard('G-D3 a1_is_only_split', ROBUST['A1']['stable'] is False and ROBUST['A2']['stable'] and ROBUST['A6']['stable'],
      '唯一分歧格是 A1；A2/A6 五套全一致')

B_('D01', '★稳健性矩阵：唯一分歧是 A1（轨迹螺旋），且分歧可归因到判据集缺口',
   '五套立场 × 六种载体 = 30 格。A2（自转）与 A6（内禀时钟）在五套下**全 FAIL**（稳健否定）；'
   'A3/A4 稳健成立；A5 稳健不可判定；**唯一分歧在 A1**：S3 几何主义给 PASS（恒等式残差 ' +
   fv(RES_TRIAD) + '，确实自洽），其余四套给 FAIL。')

F_('D02', '★归因：S3 的判据集缺一条「洛伦兹协变性」，故其 PASS 不可采信',
   'κ、τ、ω 都不是洛伦兹不变量（r54 N14：boost 下 ω′/ω 可变、τ 可翻号），'
   'S3 只要求恒等式自洽而不要求协变 ⇒ 它把「在某一参考系下画得出螺旋」当成物理。'
   '缺失条款可精确定位（不是价值观分歧，是判据集少一条）⇒ 分歧可仲裁，不必停在「见仁见智」。')

F_('D03', '★元结论（回答「哪个是正确的」）：传统支 4/5 全胜，螺旋内部运行支 0 胜',
   '把七种「内部运行」定义与传统物理逐条比价（C06），再经五套立场交叉（D01），'
   '结论是判据集的函数但**不任意**：唯一的分歧格 A1 已归因到可指名的判据缺口（D02）。'
   '⇒ 在本册证据链内，「光子以 c 平移、无内部时钟、无自转、场以 ω 振荡、偏振二态」这一组传统命题'
   '是 36 格 + 30 格两重穷举下**唯一全部通过**的一支。')

I_('D04', '方法论同构：本册与《最伟大的科学家》册用的是同一台机器',
   '该册用「多套自洽公理集 → 结论是否唯一确定」判定名次不可定；本册用「多套方法论立场 → 结论是否漂移」'
   '判定物理命题。差别在于：那册的分歧**不可归因**（价值观剩余 1.529 bit），本册的分歧**可归因到具体缺失条款**'
   '⇒ 物理命题比名次问题更硬。')

# ================================================================ E 段：总账 / 不自推 / 落盘
GOK = sum(1 for _g in GUARDS if _g['ok'])

I_('E02', '不自推 5 项（红线）',
   'NS1 不新推物理，只做既有命题的机器定价；NS2 继承 r53/r54/r56/r110 结论（真空无双折射、'
   'κ/τ/ω 非洛伦兹不变量、null 测地线直、换参零判别力）不重判；NS3 机读规则（36 格判据、'
   '自转定理、光速预算公式、立场矩阵）人工定义、机器执行；NS4 不修改任何既有产物字节；'
   'NS5 外部锚（m_γ 上限、结构光减速实验）标 [C] 且不作判据。')

I_('E03', '新增开放项与继承登记',
   '新增 **O-PHOTON-INTERIOR**（光子「内部」缺少定域中心 ⇒ 亚结构类命题不可判定，需先给出定域化方案）；'
   '继承未变：r54 N20 两难、r56 C13（弯曲时空需 Newman–Penrose 光学标架，本册不给出算子）、'
   'r53 恢复条件（须先给出真曲率或非真空载体）。')

I_('E04', '红线',
   '**数学/数值自洽 ≠ 物理证实。** 本册判 FAIL 的是「光子内部仍在运行」这一命题的全部可算读法；'
   '不等于否证空间螺旋纲领本身（其对有质量粒子/结构光的几何描述不在本册射程）。'
   '本册未推导新物理、未修改任何既有文件字节、未做 git 操作。')

# 总账必须在全部条目登记之后计算（本册自抓两轮：先算后 add 会漏计 E 段自身；
# 而 E01 自身的文案又要引用总账 ⇒ 先占位登记、算完总账再回填文案，
# 否则 E01 这一条 INFO 会被自己的统计漏掉）
I_('E01', '本册总账', '__PENDING__')

CNT = {}
for _e in ENTRIES:
    CNT[_e['verdict']] = CNT.get(_e['verdict'], 0) + 1

for _e in ENTRIES:
    if _e['code'] == 'E01':
        _e['detail'] = ('条目 ' + str(len(ENTRIES)) + '（' + str(CNT) + '）｜守卫 ' + str(GOK) + '/' +
                        str(len(GUARDS)) + '｜情形格 36（' + str(VC) +
                        '）｜立场格 30（分歧 1）｜评级：命题审计 O/L1。')

ENTRIES.sort(key=lambda _e: _e['code'])


def _jsonable(x):
    if isinstance(x, tuple):
        return list(x)
    if isinstance(x, (Fr,)):
        return str(x)
    raise TypeError('unserializable: ' + repr(x))


OUT = {
    'round': ROUND, 'tag': TAG, 'stamp': STAMP,
    'question': '光子以空间光速移动时，其内部是否仍在运行？怎么运行？',
    'entries': ENTRIES, 'entry_count': len(ENTRIES), 'verdict_count': CNT,
    'guards': GUARDS, 'guard_pass': GOK, 'guard_total': len(GUARDS),
    'constants': {'c': fv(C), 'hbar': fv(QBAR), 'm_e': fv(M_E), 'alpha': fv(ALPHA),
                  'lambda_C_e': fv(LAM_C), 'lambda_opt': fv(LAMBDA_OPT),
                  'omega_opt': fv(OMEGA_OPT), 'H_helix': fv(H_HEL)},
    'cells_36': CELLS, 'carrier_survival': SURV,
    'budget_rows': BUDGET_ROWS, 'spin_rows': SPIN_ROWS,
    'doppler_rows': DOPPLER_ROWS, 'oam_rows': OAM_ROWS, 'mass_rows': MASS_ROWS,
    'compare_table': [{'claim': a, 'traditional': b, 'reading': c, 'verdict': d, 'note': e}
                      for a, b, c, d, e in COMPARE],
    'stance_matrix': [{'stance': s[0], 'stance_desc': s[1], 'carrier': a[0],
                       'carrier_name': a[1], 'verdict': MATRIX[(s[0].split()[0], a[0])][0],
                       'note': MATRIX[(s[0].split()[0], a[0])][1]}
                      for s in STANCES for a in CARRIERS],
    'robustness': ROBUST,
    'key_numbers': {
        'R_max_at_delta_1e18_m': fv(_rmax18),
        'R_max_over_lambda_C': fv(_rmax18 / LAM_C),
        'curvature_radius_m': fv(_rad18),
        'spin_v_eq_sphere_over_c': SPIN_ROWS[0]['v_eq_over_c'],
        'doppler_500nm_at_beta_0p9_nm': DOPPLER_ROWS[2]['lambda_obs_nm'],
        'omega_identity_residual': fv(RES_OMEGA),
        'triad_residual': fv(RES_TRIAD),
        'E_over_pc_residual': fv(RES_EP),
    },
}

NAME = 'TUFT-r116_' + TAG + '_' + STAMP
json.dump(OUT, io.open(os.path.join(DATA, NAME + '.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2, default=_jsonable)

_L = []
_L.append('# ' + ROUND + '｜' + TAG + '（' + STAMP + '）—— 数据产物')
_L.append('')
_L.append('命题 P = 「光子在空间以光速 c 移动的同时，其内部还在运行」。')
_L.append('')
_L.append('## 一 关键读数')
_L.append('')
_L.append('| 量 | 读数 |')
_L.append('|---|---|')
_L.append('| 光速预算 R 上界（δ=1e-18） | ' + fv(_rmax18) + ' m |')
_L.append('| 同上 / 电子约化康普顿波长 | ' + fv(_rmax18 / LAM_C) + ' |')
_L.append('| 对应轨迹曲率半径 | ' + fv(_rad18) + ' m（波长的 ' + fv(_rad18 / LAMBDA_OPT) + ' 倍）|')
_L.append('| 自转赤道速度（实心球 a=2/5） | ' + SPIN_ROWS[0]['v_eq_over_c'] + ' c |')
_L.append('| 多普勒 500 nm @ β=0.9 | ' + DOPPLER_ROWS[2]['lambda_obs_nm'] + ' nm |')
_L.append('| 螺旋 Ω 与 ω 恒等残差 | ' + fv(RES_OMEGA) + ' |')
_L.append('| 几何恒等式 κ²+τ²=(ω/c)² 残差 | ' + fv(RES_TRIAD) + ' |')
_L.append('| E/(pc) 残差 | ' + fv(RES_EP) + ' |')
_L.append('')
_L.append('## 二 36 格判决分布')
_L.append('')
_L.append('| 载体 | 存活判定 | 六格分布 |')
_L.append('|---|---|---|')
for _a in CARRIERS:
    _vs = {}
    for _x in CELLS:
        if _x['carrier'] == _a[0]:
            _vs[_x['verdict']] = _vs.get(_x['verdict'], 0) + 1
    _L.append('| ' + _a[0] + ' ' + _a[1] + ' | **' + SURV[_a[0]] + '** | ' + str(_vs) + ' |')
_L.append('')
_L.append('## 三 与传统物理对照')
_L.append('')
_L.append('| 「内部运行」的定义 | 传统对应物 | 机器读数 | 判定 |')
_L.append('|---|---|---|---|')
for _a, _b, _c, _d, _e in COMPARE:
    _L.append('| ' + _a + ' | ' + _b + ' | ' + _c + ' | ' + _d + ' |')
_L.append('')
_L.append('## 四 立场稳健性矩阵')
_L.append('')
for _a in CARRIERS:
    _L.append('- **' + _a[0] + '** ' + _a[1] + '：' + str(ROBUST[_a[0]]['votes']) +
              ' ⇒ ' + ('稳健' if ROBUST[_a[0]]['stable'] else '**分歧**'))
_L.append('')
_L.append('## 五 条目')
_L.append('')
for _e in ENTRIES:
    _L.append('### ' + _e['code'] + ' ｜ ' + _e['verdict'] + ' ｜ ' + _e['title'])
    _L.append('')
    _L.append(_e['detail'])
    _L.append('')
io.open(os.path.join(DATA, NAME + '.md'), 'w', encoding='utf-8').write('\n'.join(_L))

_R = []
_R.append(ROUND + ' ' + TAG + ' report ' + STAMP)
_R.append('entries=' + str(len(ENTRIES)) + '  ' + str(CNT))
_R.append('guards=' + str(GOK) + '/' + str(len(GUARDS)))
_R.append('cells36=' + str(VC))
for _g in GUARDS:
    _R.append(('OK  ' if _g['ok'] else 'BAD ') + _g['name'] + ' | ' + _g['note'])
_R.append('')
for _e in ENTRIES:
    _R.append('[' + _e['verdict'] + '] ' + _e['code'] + ' ' + _e['title'])
    _R.append('    ' + _e['detail'])
io.open(os.path.join(DATA, NAME + '_report.txt'), 'w', encoding='utf-8').write('\n'.join(_R))

# 控制台只输出 ASCII，避免中文在 GBK 捕获器下炸（中文细节一律从产物文件读）
print('RC_CHECK guards=' + str(GOK) + '/' + str(len(GUARDS)) +
      ' entries=' + str(len(ENTRIES)) + ' cells36=' + str(VC))
print('KEY R_max(1e-18)=' + fv(_rmax18) + ' m  curv_radius=' + fv(_rad18) + ' m')
print('KEY v_eq_sphere=' + SPIN_ROWS[0]['v_eq_over_c'] + 'c  omega_resid=' + fv(RES_OMEGA) +
      '  triad_resid=' + fv(RES_TRIAD))
print('KEY doppler_beta0.9_nm=' + DOPPLER_ROWS[2]['lambda_obs_nm'] +
      '  E_over_pc_resid=' + fv(RES_EP))
print('PRODUCTS ' + NAME + '{.json,.md,_report.txt}')
for _g in GUARDS:
    if not _g['ok']:
        print('GUARD_FAIL ' + _g['name'])
sys.exit(0 if GOK == len(GUARDS) else 2)
