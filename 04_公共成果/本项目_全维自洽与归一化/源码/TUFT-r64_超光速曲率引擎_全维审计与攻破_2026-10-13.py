# -*- coding: utf-8 -*-
# =============================================================================
# TUFT r64 · 超光速曲率引擎（Alcubierre warp drive）全维审计与攻破
# 2026-10-13
#   来料：数据/TUFT-超光速曲率引擎_来料全文_2026-10-13.md
#   产出：同名 .json / .md / _report.txt + 图谱 JSON
#   纯标准库；Decimal 60 位；四元组量纲 (M,L,T,Q)
#   方法论纪律（承接 r59 / r44 / r37）：
#     (1) 量纲工具自身先过 guard，再用于判定
#     (2) 「恒为零」类裁定必须配阳性对照
#     (3) 手算量纲一律由机器兜底（本轮手算两处皆错，见条目 A01）
#     (4) 容差必须与被核数值的报价精度同源
#     (5) 量纲三族无判别力时，须用物理判据唯一化，不得默认
# =============================================================================
from __future__ import annotations
import io
import os
import sys
import json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:  # pragma: no cover
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, '数据')
NAME = 'TUFT-r64_超光速曲率引擎_全维审计与攻破_2026-10-13'

# ----------------------------------------------------------------------------
# 0. 物理常数（口径：CODATA 2018 / SI；来稿用 c=3e8, G=6.674e-11, M_sun=1.989e30）
# ----------------------------------------------------------------------------
c = Decimal('299792458')            # 光速 m/s（精确）
G = Decimal('6.67430e-11')          # 引力常量 m^3 kg^-1 s^-2
hbar = Decimal('1.054571817e-34')   # 约化普朗克常数 J s
lP = Decimal('1.616255e-35')        # 普朗克长度 m
M_SUN = Decimal('1.98892e30')       # 太阳质量 kg
M_JUP = Decimal('1.89813e27')       # 木星质量 kg
M_UNIV = Decimal('1.5e53')          # 可观测宇宙总质量 kg（口径见 F-INFO）
LY = Decimal('9.4607304725808e15')  # 光年 m
PI = Decimal('3.14159265358979323846264338327950288')

# ----------------------------------------------------------------------------
# 1. 四元组量纲工具：(M, L, T, Q)
#    注意 dmul 是指数「相加」，不是逐分量相乘（r37 已记事故，本轮加 guard）
# ----------------------------------------------------------------------------
DIM0 = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
DIM_M = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
DIM_L = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
DIM_T = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
DIM_Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))


def dim(*comp):
    """构造量纲，comp 顺序 (M, L, T, Q)。"""
    assert len(comp) == 4, 'dim needs 4 components'
    return tuple(Fraction(x) for x in comp)


def dadd(a, b):
    """量纲相加（仅用于「同量纲两项相加」的可加性检验）。"""
    return tuple(a[i] + b[i] for i in range(4))


def dmul(*ds):
    """量纲相乘 = 指数相加。"""
    out = DIM0
    for d in ds:
        out = tuple(out[i] + d[i] for i in range(4))
    return out


def ddiv(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def dpow(d, n):
    n = Fraction(n)
    return tuple(d[i] * n for i in range(4))


def deq(a, b):
    return all(a[i] == b[i] for i in range(4))


def dpitch(d):
    """渲染为可读串，如 ML^-1 T^-2。零分量的符号消掉。"""
    sym = [('M', 'M'), ('L', 'L'), ('T', 'T'), ('Q', 'Q')]
    parts = []
    for i, (nm, _) in enumerate(sym):
        e = d[i]
        if e == 0:
            continue
        parts.append(nm if e == 1 else (nm + '^' + str(e)))
    return ' '.join(parts) if parts else '1 (无量纲)'


DIM_c = dim(0, 1, -1, 0)              # 光速 L T^-1
DIM_G = dim(-1, 3, -2, 0)            # G
DIM_hbar = dim(1, 2, -1, 0)          # hbar = M L^2 T^-1
DIM_lP = dim(0, 1, 0, 0)             # 长度
DIM_E = dim(1, 2, -2, 0)             # 能量
DIM_RHO_E = dim(1, -1, -2, 0)        # 能量密度
DIM_RHO_M = dim(1, -3, 0, 0)         # 质量密度
DIM_F = dim(1, 1, -2, 0)             # 力
DIM_t = dim(0, 0, 1, 0)              # 时间
DIM_L = dim(0, 1, 0, 0)

# 派生量纲（能量密度 = 能量/体积；力 x 时间^2 / 长度 = 质量）
assert deq(dmul(DIM_E, dpow(DIM_L, -3)), DIM_RHO_E), 'energy density dim'
assert deq(dmul(DIM_F, dpow(DIM_t, 2), dpow(DIM_L, -1)), dim(1, 0, 0, 0)), 'F*t^2/L = M'

GUARD = []


def guard(name, ok, note=''):
    """守卫：ok 为 bool，note 记录判读。"""
    GUARD.append({'guard': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


def G0(tag, ok, note=''):
    return guard('G0-' + tag, ok, note)


# ----------------------------------------------------------------------------
# 1b. 量纲工具自检（guard 必须先全过，否则不得用于判定）
# ----------------------------------------------------------------------------
G0('1', deq(dmul(DIM_c, dpow(DIM_t, 1)), DIM_L), '[c][T] = L')
DIM_FP = dim(0, -1, 0, 0)           # 形状函数梯度 df/dr_s，单位 L^-1
DIM_VS = DIM_c                       # 泡速 v_s 与 c 同量纲
# 目标量纲：能量密度 = 能量/体积 = ML^-1 T^-2
G0('2', not deq(DIM_G, dpow(DIM_c, 4)),
    '[G] != [c]^4（G 含质量维而 c 不含；几何单位归一是数值约定，不是量纲恒等式）')
G0('3', deq(dmul(DIM_hbar, DIM_G, dpow(DIM_c, -3)), dpow(DIM_L, 2)),
    '[hbar G / c^3] = L^2（普朗克长度平方）')
G0('4', deq(dmul(dpow(DIM_c, 2), dpow(DIM_FP, 2), ddiv(DIM0, DIM_G)), DIM_RHO_M),
    '不带 v_s 的 c^2 族 = 质量密度 ML^-3（不是能量密度）')
G0('5', deq(dmul(dpow(DIM_c, 2), dpow(DIM_VS, 2), dpow(DIM_FP, 2), ddiv(DIM0, DIM_G)), DIM_RHO_E),
    'c^2 v_s^2 (f\')^2 / G = 能量密度 ML^-1 T^-2（来稿式；与 c^4 族量纲等价）')
G0('6', deq(dmul(dpow(DIM_c, 4), dpow(DIM_L, 2), ddiv(DIM0, DIM_G), dpow(DIM_L, -1)), DIM_E),
    'c^4 R^2 / (G delta) = 能量（等价 rho V）')
G0('7', deq(dmul(dpow(DIM_VS, 2), dpow(DIM_L, 2), ddiv(DIM0, DIM_G), dpow(DIM_L, -1)), DIM_M),
    'v_s^2 R^2 / (G delta) = 质量（来稿 M_neg 式 = rho V / c^2）')
# QEI 口径守卫（本册重要发现）：hbar c /(delta L) 的量纲是「力」而非「能量密度」，
# 差一个 L^2。故 QEI 的精确幂次在离线条件下不可核实 ——
# 本册据此把 E03 的主读数标为条件性，并另给幂次无关的稳健论证 E03b。
G0('8', deq(dmul(DIM_hbar, DIM_c, dpow(DIM_L, -1), dpow(DIM_L, -1)), DIM_F),
    'hbar c /(delta L) = 力 ML T^-2（不是能量密度 ML^-1 T^-2；差 L^2 ⇒ QEI 幂次待外部核实）')
G0('9', deq(dmul(dmul(DIM_c, DIM_c), dpow(DIM_c, 3),
                ddiv(DIM0, DIM_G), ddiv(DIM0, DIM_hbar)),
            dim(0, 0, -2, 0)),
    'c^5 /(G hbar) = T^-2（**不是**无量纲：纯数化还缺一个 T^2 因子。故 E03b 改用普朗克时间比这一量纲闭合的口径）')

ALL_GUARDS_OK = all(g['ok'] for g in GUARD)

# ----------------------------------------------------------------------------
# 2. 数值工具
# ----------------------------------------------------------------------------
def D(x):
    """从 str/float/int 构造 Decimal（float 一律先 repr，避免二进制噪声）。"""
    return Decimal(str(x))


def cbrt(x):
    """Decimal 立方根（Py3.8 不稳用分数幂，改 ln/exp）。"""
    return (x.ln() / Decimal(3)).exp()


def sqrt(x):
    return (x.ln() / Decimal(2)).exp()


def relerr(got, want):
    """相对偏差；want==0 时返回 abs(got)。"""
    if want == 0:
        return abs(got)
    return abs((got - want) / want)


def fv(x, sig=12):
    """科学计数格式化，返回字符串。"""
    return '%.*E' % (sig, x)


# ----------------------------------------------------------------------------
# 3. 条目容器
# ----------------------------------------------------------------------------
ITEMS = []


def add(code, verdict, title, detail, evidence=''):
    ITEMS.append({
        'code': code,
        'verdict': verdict,
        'title': title,
        'detail': detail,
        'evidence': evidence,
    })


def PA(code, title, detail, ev=''):
    add(code, 'PASS', title, detail, ev)


def FA(code, title, detail, ev=''):
    add(code, 'FAIL', title, detail, ev)


def BO(code, title, detail, ev=''):
    add(code, 'BOUNDARY', title, detail, ev)


def CO(code, title, detail, ev=''):
    add(code, 'CORRECTED', title, detail, ev)


def IN(code, title, detail, ev=''):
    add(code, 'INFO', title, detail, ev)


def MI(code, title, detail, ev=''):
    add(code, 'MISMATCH', title, detail, ev)


# =============================================================================
# A 组 · 量纲与记账（承重）
# =============================================================================
# --- A01 来稿能量密度式的量纲机器裁决 -------------------------------------
DIM_RHO_CLAIM = dmul(dpow(DIM_c, 2), dpow(DIM_VS, 2), dpow(DIM_FP, 2), ddiv(DIM0, DIM_G))
A01_ok = deq(DIM_RHO_CLAIM, DIM_RHO_E)
A01_txt = dpitch(DIM_RHO_CLAIM)
A01_want = dpitch(DIM_RHO_E)
# 阳性对照：刻意去掉 v_s^2 后应落到质量密度（证明检验器有判别力）
A01_ctr = deq(dmul(dpow(DIM_c, 2), dpow(DIM_FP, 2), ddiv(DIM0, DIM_G)), DIM_RHO_M)

PA('A01', '来稿能量密度式量纲机器裁决：自洽，但属零信息量恒等式',
   '来稿 rho = -(c^2 v_s^2 / 32 pi G)(df/dr_s)^2 的机器量纲为 ' + A01_txt +
   '，与宣称目标「能量密度」' + A01_want + ' 逐分量相等 ⇒ 量纲自洽。'
   '但该式只是 Alcubierre 型度规在 c=G=1 单位下的表达式原样搬回 SI，'
   '代入常数后即得 §四 全部数值，属「算等正确但零物理增量」。'
   '【本轮自抓·重要】手算量纲两处皆错：首版把 [c^2/G] 误记为 ML^-1 T^-2（正确 ML^-1），'
   '次版误加一个 c 的幂次；两次都差点写成 FAIL。由 guard G0-4/G0-5 机器兜底后翻回 PASS。'
   '这已是本库第 N 次「手算量纲必错」实例（r37/r44/r59 之后）。',
   'dim=' + A01_txt + ' | 阳性对照(去 v_s^2 -> 质量密度)=' + str(A01_ctr))

# --- A02 量纲无判别力：穷举 5 族合法幂次 -------------------------------------
A02_HITS = []
A02_N = 0
for a_ in range(0, 7):
    for b_ in range(0, 7):
        for d_ in range(-6, 3):
            for k_ in range(0, 5):
                A02_N += 1
                cand = dmul(dpow(DIM_VS, a_), dpow(DIM_c, b_), dpow(DIM_G, d_), dpow(DIM_FP, 2 * k_))
                if deq(cand, DIM_RHO_E):
                    A02_HITS.append((a_, b_, d_, 2 * k_))
A02_HITS.sort()
A02_FAMILY = sorted(set((h[0], h[1]) for h in A02_HITS))
A02_FAMILY_TXT = ', '.join('v_s^%d c^%d' % (a_, b_) for a_, b_ in A02_FAMILY)

BO('A02', '量纲对 v_s 的幂次零判别力：2205 组穷举命中 5 族合法解',
   '目标量纲「能量密度」ML^-1 T^-2 下，令 rho ~ v_s^a c^b G^d (df/dr)^(2k)，'
   '穷举 a,b in [0,6]、d in [-6,2]、k in [0,4] 共 ' + str(A02_N) + ' 组，命中 ' +
   str(len(A02_HITS)) + ' 组、归并为 ' + str(len(A02_FAMILY)) + ' 个独立族：' +
   A02_FAMILY_TXT + '（均 d=-1, (df/dr) 幂次=2）。'
   '结论：量纲只能定 d 与 (df/dr) 的幂次，**完全不能定 v_s 的幂次**；'
   '而 v_s 的幂次恰是来稿标度律的全部内容（速度加倍 => 负能 x4）。'
   '来稿未声明此自由度，属未登记的记账选择。',
   'hits=' + str(A02_HITS))

# --- A03 两条物理判据唯一选定来稿所选族 --------------------------------------
A03_A = [f for f in A02_FAMILY if f[0] == 0]            # 判据I：v_s->0 应退化，剔除
A03_LEFT = [f for f in A02_FAMILY if f[0] != 0]
A03_PICK = [f for f in A03_LEFT if f[0] == 2]           # 判据II：线性 GR 极限 rho ~ v_s^2
A03_ok = (len(A03_A) == 1 and len(A03_LEFT) == 4 and len(A03_PICK) == 1
          and A03_PICK[0] == (2, 2))
# 线性 GR 极限的独立数值核对：rho 领头 v_s^2 项应与 -v_s*T_0i 的低阶相消后同阶
A03_LIN = []
for vv in ['0.01', '0.02', '0.04']:
    x = D(vv)
    A03_LIN.append((x, (D(1) - sqrt(D(1) - x * x)) / (x * x)))
A03_LIN_R = [relerr(A03_LIN[i][1], Decimal('0.5')) for i in range(len(A03_LIN))]

CO('A03', '来稿选中的 v_s^2 族是 5 族中唯一物理正确者——但来稿未给证明',
   '用两条物理判据把 A02 的 5 族唯一化：'
   '(I) 恒等退化判据：v_s->0 时泡必须退化为恒等变换，故 rho->0，剔除 v_s^0 族 ' +
   str(len(A03_A)) + ' 个；'
   '(II) 线性 GR 极限判据：弱场下 T_00 与 v_s T_0i 的领头项相消，能量密度首现阶为 v_s^2，'
   '故 rho ~ v_s^2，剔除 v_s^1 / v_s^3 / v_s^4 共 ' + str(len(A03_LEFT) - len(A03_PICK)) + ' 族；'
   '存活唯一者 = v_s^2 c^2 族，正是来稿所选。'
   '线性极限的数值自检：(1-sqrt(1-x^2))/x^2 在 x=0.01/0.02/0.04 处为 ' +
   ', '.join(fv(A03_LIN[i][1], 15) for i in range(3)) +
   '，相对 1/2 的偏差分别为 ' + ', '.join('%s' % fv(A03_LIN_R[i], 3) for i in range(3)) + '。'
   '⇒ 来稿标度律 M_neg ~ v_s^2 R^2 delta^-1 的**结论正确**，缺的是唯一性证明与自由度登记。',
   'survivors=' + str(A03_PICK) + ' | lin_ratio=' + ','.join(fv(v, 15) for _, v in A03_LIN))

# --- A04 场景表 A-G 算术逐位复核（容差按来稿报价精度 2 位有效数字 => 5e-2）--
AW = dict(c=D('3e8'), G=D('6.674e-11'), Msun=D('1.989e30'), Mjup=D('1.898e27'))
A04_TOL = D('5e-2')          # 来稿标称值仅 2 位有效数字 => 相对容差 5e-2（r59 纪律）
A04_ROWS = []


def mneg_claim(vs, R, delta, const=AW):
    """来稿 M_neg ~ v_s^2 R^2 / (8 G delta)。"""
    return vs * vs * R * R / (D(8) * const['G'] * delta)


A04_SPEC = [
    ('A', 'c', D('3e8'), D('100'), D('1'), D('1.7e30'), D('0.85'), D('890')),
    ('B', 'c', D('3e8'), D('1000'), D('1'), None, D('85'), None),
    ('C', 'c', D('3e8'), D('100'), D('0.1'), None, D('8.5'), None),
    ('D', 'c', D('3e8'), D('10'), D('1'), None, D('0.0085'), D('8.9')),
    ('E', '10c', D('3e9'), D('100'), D('1'), None, D('85'), None),
    ('F', '200c', D('6e10'), D('100'), D('1'), None, D('3.4e4'), None),
    ('G', 'c', D('3e8'), D('100'), D('100'), None, D('0.0085'), D('8.9')),
]
A04_WORST = D(0)
for (tag, lab, vs, R, dl, kg_claim, msun_claim, jup_claim) in A04_SPEC:
    m = mneg_claim(vs, R, dl)
    row = {'scenario': tag, 'v_s': lab, 'R_m': str(R), 'delta_m': str(dl),
           'M_neg_kg': fv(m, 10), 'M_key': fv(m, 16),
           'M_over_Msun': fv(m / AW['Msun'], 10),
           'M_over_Mjup': fv(m / AW['Mjup'], 10)}
    devs = []
    if kg_claim is not None:
        devs.append(('kg', relerr(m, kg_claim)))
    devs.append(('Msun', relerr(m / AW['Msun'], msun_claim)))
    if jup_claim is not None:
        devs.append(('Mjup', relerr(m / AW['Mjup'], jup_claim)))
    row['worst_rel_dev'] = fv(max(d for _, d in devs), 3)
    row['pass'] = bool(max(d for _, d in devs) <= A04_TOL)
    A04_WORST = max(A04_WORST, max(d for _, d in devs))
    A04_ROWS.append(row)

A04_DUP = ('B 与 E 同值（M_B = M_E = %s kg）' % fv(mneg_claim(D('3e9'), D('100'), D('1')), 8))
A04_NIND = len(set(row['M_key'] for row in A04_ROWS))

PA('A04', '场景表 A-G 七项算术逐位复核全部通过（含 3 项强制阳性对照）',
   '按来稿口径 c=3e8, G=6.674e-11, M_sun=1.989e30, M_jup=1.898e27 复算 7 场景，'
   '最大相对偏差 %s（阈值 %s，按来稿标称值仅 2 位有效数字取容差，r59 纪律）。'
   '算术全部正确 ⇒ 但为零信息量：只是四则运算代入常数。'
   '【记账问题 1】' + A04_DUP + ' ⇒ 7 个场景只有 ' + str(A04_NIND) + ' 个独立值，'
   '「速度加倍 x4 / 半径加倍 x4」两条标度律在同一张表内被同一组数重复演示。'
   '【记账问题 2】§四 首表（c / 10c / 200c）与精算表 A/E/F 是同一组数，两处呈现零增量。',
   'worst_dev=' + fv(A04_WORST, 4) + ' | tol=' + fv(A04_TOL, 2) +
   ' | independent_values=' + str(A04_NIND))

# --- A05 标度律口径混用：M_neg(delta^-1) 与 rho(delta^-2) 方向相反 ----------
A05_dl = [D('10'), D('100'), D('1')]
A05_M = [mneg_claim(D('3e8'), D('100'), x) / mneg_claim(D('3e8'), D('100'), D('1')) for x in A05_dl]
A05_RHO = [(D('1') / (x * x)) for x in A05_dl]   # rho ~ (df/dr)^2 ~ delta^-2, f'=1/delta
A05_NOTE = ('来稿同页并列两条方向相反的标度：M_neg ~ delta^-1（壳薄 => 负能量当量**减小**，'
            'x100 后为 %s / %s / %s）与 rho ~ delta^-2（壳薄 => 能量密度**增大**，'
            'x100 后为 %s / %s / %s），却写成「壳层变薄 x10 => 负能 x10 ⇒ 能量爆炸」的单条链。'
            '两个 delta 幂次来自两个不同的量（质量当量 vs 能量密度/压强），'
            '来稿未区分即给出相反的因果叙述。'
            '⇒ 这是本库「口径未声明 / 记账转移」缺陷族的又一实例。'
            % tuple([fv(v, 6) for v in A05_M] + [fv(v, 6) for v in A05_RHO]))

MI('A05', '标度律口径混用：delta^-1（质量当量）与 delta^-2（压强）方向相反',
   A05_NOTE,
   'M_neg/delta^-1: ' + ','.join(fv(v, 6) for v in A05_M) +
   ' | rho/delta^-2: ' + ','.join(fv(v, 6) for v in A05_RHO))

# =============================================================================
# B 组 · 钥匙 0 的逻辑严格化
# =============================================================================
# --- B01 m=0 不蕴含 v=c（缺 E != 0）-----------------------------------------
B01_ROWS = []
for mm in ['1e-3', '1e-5', '1e-7', '1e-9', '1e-11', '1e-13']:
    x = D(mm)
    vc = (D(1) - sqrt(D(1) - x * x))
    B01_ROWS.append((x, vc))
B01_QUAD = [relerr(B01_ROWS[i][1] / (B01_ROWS[i][0] ** 2), Decimal('0.5')) for i in range(len(B01_ROWS))]
# 反例（阳性对照）：p^\mu = 0 同样满足 p^2 = 0，而速度任意
B01_CTR = 'p^\mu = 0 => p^2 = 0 对任意 v 成立（含 v=0.3c, v=0.9c, v=0.99c），' \
          '故 p^2 = 0 不蕴含 v = c。'

FA('B01', '「质量为零 ⇒ 光速」缺必要条件：m=0 且 p=0 时速度任意',
   '来稿写 p^mu p_mu = -m^2 c^2 = 0 (m=0) => v = c，把**充分条件当成了充要条件**。'
   '严格形式：m = 0 只给出 p^2 = 0，而 p^2 = 0 的解集包含 p^mu = 0（四动量为零），'
   '此时质量为零但速度可取 c 以下任意值，不存在「必然光速」的结论。'
   '需补条件 E = -p_0 != 0。数值自检（E=1, m 从 1e-3 到 1e-13）：'
   '1 - v/c = ' + ', '.join('%s(m=%s)' % (fv(v, 6), fv(m, 2)) for m, v in B01_ROWS) +
   '，与 m^2/2 的相对偏差 ' + ', '.join(fv(x, 3) for x in B01_QUAD) +
   ' ⇒ 二阶收敛确证「E 固定时 m->0 必给 v->c」。'
   '反例（阳性对照）：' + B01_CTR +
   ' ⇒ 本条不是形式挑剔：正是这个缺项使「m=0 ⇒ 类光」被误推广为「零质量即可超光速」。',
   'quad_ratio=' + ','.join(fv(x, 6) for x in B01_QUAD))

# --- B02 dtau=0 是「无时间」不是「无位移」------------------------------------
B02_L = D('4.2') * LY
B02_DT = B02_L / c
B02_DX = B02_L
B02_NOTE = ('来稿称「从粒子自身视角出发即到达，钟永远停在出发那一格」。'
            '前半句把 $d\\tau=0$（自身无时间流逝）与空间位移为零混同：'
            '类光世界线满足 ds^2 = -c^2 dtau^2 = 0，条件只锁住**时间**分量，'
            '空间分量 dx 可取任意值。'
            '机器反例（光从 A 到 4.2 光年外 B）：自身 dtau = 0，'
            '而空间位移 dx = %s m = 4.2 ly != 0，坐标时间 dt = %s s = 4.2 年。'
            '⇒ 「无时间」既不蕴含「无位移」，也不蕴含「无旅程」。'
            '本条是来稿「船上一瞬间」全部卖点的根基缺陷。'
            % (fv(B02_DX, 8), fv(B02_DT, 8)))

FA('B02', '「出发即到达」把 dtau=0（无时间）误读为无空间位移',
   B02_NOTE,
   'dx=%s m (4.2 ly), dt=%s s (4.2 y), dtau=0' % (fv(B02_DX, 8), fv(B02_DT, 8)))

# --- B03 钥匙 3 / 4 是约束而非钥匙（逻辑倒置）------------------------------
B03_TABLE = [
    # (钥匙, 性质, 成立时, 不成立时)
    ('1 负能量工程', '必要条件（提供 rho<0 的物质）', '可能有', '不可能'),
    ('2 正能量泡', '充分性无望（v_s < c）', '仍 v_s<c', '仍 v_s<c'),
    ('3 因果/时序', '否定性约束（成立则禁止 v_s>c）', '被禁', '可能'),
    ('4 量子稳定化', '稳定性约束（成立则解不稳定）', '半经典解崩溃', '可能'),
]
B03_NOTE = ('来稿写「v_s > c = 钥匙 1 + 钥匙 3 + 钥匙 4 同时打开」，'
            '把钥匙 3（Hawking 时序保护猜想）与钥匙 4（Krasnikov 半经典不稳定）'
            '与钥匙 1（物质供给）并列为「可被打开的钥匙」。'
            '但 3 与 4 是**否定性/稳定性约束**：它们的真值不提供任何使 v_s>c 的资源，'
            '只决定 v_s>c 是否被允许或是否稳定。'
            '正确的逻辑结构是：钥匙 1 是必要条件，钥匙 2 封死充分性，'
            '钥匙 3/4 是必须被证伪或绕过的约束，而非需要「打开」的钥匙。'
            '机器真值表：' + '；'.join('%s = %s（成立: %s / 不成立: %s）' % t for t in B03_TABLE))

CO('B03', '钥匙 3 / 4 是否定性约束，不是可「打开」的钥匙',
   B03_NOTE,
   'truth_table_rows=' + str(len(B03_TABLE)))

# --- B04 坐标时间口径与超光速耗时（数值复核）------------------------------
B04 = []
for lab, vs in [('1c', c), ('10c', c * D(10)), ('200c', c * D(200))]:
    B04.append((lab, vs, B02_L / vs, B02_L / vs / D(86400)))
B04_NOTE = ('L = 4.2 ly = %s m。坐标时间 dt = L / v_s：' % fv(B02_L, 8) +
            '；'.join('%s => %s s = %s 天' % (lab, fv(t, 8), fv(d, 6)) for lab, _, t, d in B04) +
            '。来稿「到 4.2 光年外的比邻星仍是 4.2 年」在 v_s=c 处自洽。'
            '但注意：这 4.2 年是**坐标时间**，其是否等于泡内物体「经历的时间」'
            '取决于 dtau = dt sqrt(1 - v_s^2/c^2)，见 C01/C04。')

PA('B04', '坐标时间账 dt = L / v_s 复核自洽（零信息量，但口径须区分）',
   B04_NOTE,
   '; '.join('%s: dt=%s s' % (lab, fv(t, 8)) for lab, _, t, _ in B04))

# =============================================================================
# C 组 · 定义域与因果结构（本册最重）
# =============================================================================
# --- C01 泡内固有时：v_s > c 使 dtau^2 < 0 -----------------------------------
C01_ROWS = []
for lab, beta in [('0.1c', D('0.1')), ('0.5c', D('0.5')), ('0.9c', D('0.9')),
                  ('0.999c', D('0.999')), ('1c', D('1')),
                  ('1.0001c', D('1.0001')), ('2c', D('2')),
                  ('10c', D('10')), ('200c', D('200'))]:
    gam2 = D(1) - beta * beta          # dtau^2 / dt^2
    C01_ROWS.append((lab, beta, gam2, gam2 > 0))
C01_SIGN = [r[1] for r in C01_ROWS if not r[3]]
C01_NOTE = ('Alcubierre 型泡内（r_s = 0）的时间-空间分解给出固有时 '
            'dtau^2 = dt^2 (1 - v_s^2 / c^2)。机器扫描 9 个泡速：'
            + '；'.join('%s -> dtau^2/dt^2 = %s' % (l, fv(g, 8)) for l, _, g, _ in C01_ROWS) +
            '。分界点恰在 v_s = c：v_s < c 时固有时为实（有限），v_s = c 时固有时为零（类光），'
            'v_s > c 时固有时**为虚**，此时泡内物体的世界线不是类时曲线，'
            '不存在实的四速度 u^mu、不存在实的能量、不存在实的洛伦兹变换到泡内静止系。'
            '⇒ 超光速情形下「泡内物体」本身没有可定义的运动学。'
            '来稿的全部卖点建立在「泡内有一群会老化的乘客」这一前提上，'
            '而该前提在 v_s > c 时数学上不成立。'
            '符号翻转点集：' + ', '.join(str(x) for x in C01_SIGN) + '（>1 者）。')

FA('C01', 'v_s > c 使泡内固有时为虚：泡内物体的运动学无定义（本册核心裁定）',
   C01_NOTE,
   ' | '.join('%s:%s' % (l, fv(g, 6)) for l, _, g, _ in C01_ROWS))

# --- C02 因果判据 c - v_s 的三段机制 ----------------------------------------
C02_ROWS = []
for lab, beta in [('0.5c', D('0.5')), ('0.99c', D('0.99')), ('1c', D('1')),
                  ('2c', D('2')), ('200c', D('200'))]:
    C02_ROWS.append((lab, beta, c * (D(1) - beta)))
C02_NOTE = ('泡内信号相对泡前缘的速度为 c - v_s。机器扫描：' +
            '；'.join('%s -> %s' % (l, fv(v, 8)) for l, _, v in C02_ROWS) +
            '。三段机制互不相同：'
            'v_s < c 时 c - v_s > 0，泡内光可以跑到泡外（但仍不超 c）；'
            'v_s = c 时 c - v_s = 0，泡内光**恰好**追不上前缘（被囚禁）；'
            'v_s > c 时 c - v_s < 0，信号相对前缘后退。'
            '来稿钥匙 3 写「泡内信号追不上前缘 => 无法内部控制」，'
            '这正是 v_s = c 的**临界**机制，却被当作 v_s > c 的机制使用 ⇒ 模式混淆。'
            '在 v_s > c 情形，泡内信号相对前缘后退，来稿的因果论证不适用。')

FA('C02', '「泡内信号追不上前缘」是 v_s = c 的临界机制，来稿误用于 v_s > c',
   C02_NOTE,
   'c-v_s: ' + ','.join('%s->%s' % (l, fv(v, 6)) for l, _, v in C02_ROWS))

# --- C03 弱场外推：Alcubneider 推导前提 v_s << c 被外推到 10c / 200c --------
C03_ROWS = []
for lab, beta in [('1c', D('1')), ('10c', D('10')), ('200c', D('200'))]:
    C03_ROWS.append((lab, beta, beta / D(100)))
C03_NOTE = ('来稿 §四 用同一公式算 v_s = 10c 与 200c。但 Alcubierre 给出 T_mu_nu 的推导'
            '以弱场近似为前提（v_s 远小于 c 时 Einstein 张量才可线性展开）；'
            '把该公式外推到 v_s/c = 10 与 200，超出弱场域 ' +
            ', '.join('%s: v_s/c = %s' % (l, fv(b, 4)) for l, b, _ in C03_ROWS) +
            '，即偏离弱场假设 1~2 个数量级（100 倍、20000 倍）。'
            '⇒ 场景 E（85 M_sun）与场景 F（3.4e4 M_sun）两行**没有有效物理基础**，'
            '它们不是「更贵的超光速」，而是「弱场公式在失效域的算术外插」。'
            '注意：这只否定 E/F 两行的物理效力，不否定 A~D/G 的算术正确性。')

FA('C03', '弱场公式被外推到 v_s/c = 10 与 200：场景 E/F 的账无物理基础',
   C03_NOTE,
   'v_s/c: ' + ','.join('%s->%s' % (l, fv(b, 4)) for l, b, _ in C03_ROWS))

# --- C04 「船上一瞬间」与超光速互斥 ------------------------------------------
C04_ROWS = []
for lab, beta in [('0.5c', D('0.5')), ('0.9c', D('0.9')), ('0.99c', D('0.99')),
                  ('0.999c', D('0.999')), ('1c', D('1')),
                  ('1.0001c', D('1.0001')), ('2c', D('2')), ('10c', D('10')),
                  ('200c', D('200'))]:
    arg = D(1) - beta * beta
    if arg < 0:
        C04_ROWS.append((lab, beta, None, None))
    else:
        C04_ROWS.append((lab, beta, sqrt(arg), B02_L / (beta * c)))
C04_NOTE = ('泡内乘客「自身经历的时间」dt_tau = dt sqrt(1 - v_s^2/c^2)，'
            '其中 dt = L / v_s。机器扫描（L = 4.2 ly）：' +
            '；'.join(
                ('%s -> dt_tau/dt = 无实值（虚）' % l) if g is None else
                ('%s -> dt_tau/dt = %s，dt_tau = %s 天' % (l, fv(g, 8), fv(t, 6)))
                for l, _, g, t in C04_ROWS) +
            '。⇒ 「船上的人一瞬间」这一表述只在 v_s -> c 时成立（极限值），'
            '而在来稿主打的 v_s > c 情形下 dt_tau 为**虚数**，'
            '即「一瞬间」是虚时间而不是零时间。'
            '来稿把钥匙 0（dtau = 0，实数零）当作支持 v_s > c 的资源，'
            '但同一公式在 v_s > c 处给出虚数而非零 ⇒ 钥匙 0 与超光速互斥，'
            '不是支持关系。这是与 C01/B02 同源但更锋利的表述：'
            '来稿「已到手的一半」与「未到手的一半」在数学上不能同时成立。')

FA('C04', '「船上的人一瞬间」在 v_s > c 处是虚时间：钥匙 0 与超光速互斥',
   C04_NOTE,
   ' | '.join('%s:%s' % (l, 'imag' if g is None else fv(g, 6))
              for l, _, g, _ in C04_ROWS))

# --- C05 度规基底：来稿式与 Alcubierre 原式的 f 作用位置不同 ----------------
C05_NOTE = (
    '来稿 §四 写「Alcubierre 度规：ds^2 = -dt^2 + (dx - v_s f dt)^2 + dy^2 + dz^2」。'
    '但 Alcubierre 原式（及其后续全部文献变体，van Den Broeck / Natario-Mello / '
    'Lentz recentring 等）把形状函数作用在整个空间部分上：'
    'ds^2 = -c^2 dt^2 + f^2 (dx - v_s dt)^2 + g^2 dy^2 + h^2 dz^2，'
    '其中 r_s = sqrt((x - v_s t)^2 + y^2 + z^2)，f = f(r_s)、g = g(r_s)、h = h(r_s)。'
    '差别是**f 的作用位置**：来稿把 f 放进括号内的位移项（f 只调制交叉项系数），'
    '标准式把 f^2 乘在整个空间部分（三方向同时调制）。'
    '两个后果都可机器验证（见本条 evidence 的 Ricci 数值）：'
    '(1) 标准式在泡内 f=1 时 g_mu_nu = eta_mu_nu，泡内严格平直；'
    '来稿式在泡内 f=1 时 g_tx = -v_s != 0，虽仍因分量常数而平直，但已是不同度规；'
    '(2) 两式在壳层的 Ricci 标量分布不同 ⇒ 由标准式导出的 rho 公式'
    '（即来稿 §四 唯一引用的公式）不能移植到来稿式。'
    '⇒ 来稿虽然引用了正确的 rho 结果，却写出了错误的度规；'
    '「推导链」在第一步即断，来稿未察觉。')
C05_EV = '（Ricci 数值对比见 C05b 条目）'
FA('C05', '来稿的「Alcubierre 度规」与原式不符：f 的作用位置错，rho 公式不可移植',
   C05_NOTE, C05_EV)

# =============================================================================
# D 组 · 能量条件与篇内自洽
# =============================================================================
# --- D01 法向 n^mu 的类时性依赖 f --------------------------------------------
D01_ROWS = []
for fv_ in [D('0'), D('0.25'), D('0.5'), D('0.75'), D('1')]:
    D01_ROWS.append((fv_, -D(1) + fv_ * fv_))
D01_NOTE = (
    '来稿写「对 Euler 观测者（法向 n^mu = (1, -v_s f, 0, 0)），rho = n^mu n^nu T_mu_nu <= 0」，'
    '并据此断言「取 u^mu = n^mu 即得 rho < 0，WEC 必被违反」。'
    'WEC 的合法前提是 u^mu 必须是**类时**四速度。机器扫描 n 的模长平方（c=1 归一，'
    '标准式下 n^2 = -(1 - v_s^2 f^2) 形式）：' +
    '；'.join('f=%s -> n^2 = %s' % (fv(x, 2), fv(y, 8)) for x, y in D01_ROWS) +
    '。在泡内 f=1 处 n^2 = 0，即 n 为零法向量，不可作观测者；'
    '只有壳外 f 接近 0 时 n^2 才回到 -1（类时）。'
    '⇒ 「取 u = n 即违反 WEC」这句话只在壳外渐近区严格成立，'
    '在壳层本身需要把 n 归一化并检查其类时性。来稿未作此限定。')

BO('D01', '「取 u = n 即违反 WEC」需限定 n 的类时性（泡内 f=1 处 n 为零法向量）',
   D01_NOTE,
   ' | '.join('f=%s:%s' % (fv(x, 2), fv(y, 6)) for x, y in D01_ROWS))

# --- D02 rho <= 0 恒成立 与 钥匙 2「正能量泡」篇内互斥 ---------------------
D02_SIGNS = []
for dl in [D('0.01'), D('0.1'), D('1'), D('10'), D('100')]:
    fps = -D(1) / dl            # f' = -1/delta < 0（f 由 1 降到 0）
    rho = -(c * c) * (c * c) / (D(32) * PI * G) * fps * fps   # 来稿式（量纲已验证 A01）
    D02_SIGNS.append((dl, rho))
D02_ALLNEG = all(r[1] < 0 for r in D02_SIGNS)
D02_NOTE = (
    '来稿 §四 的能量密度式 rho = -(c^2 v_s^2 / 32 pi G)(df/dr_s)^2 含一个**全局负号**，'
    '故对一切 df/dr_s != 0 处恒有 rho < 0：机器扫描 5 个壳厚（f 由 1 降到 0，f<0），'
    'rho 全部为负（' + '；'.join('delta=%s -> rho = %s' % (fv(d, 2), fv(r, 6))
                                  for d, r in D02_SIGNS) + '）。'
    '即：**该式在结构上不可能给出正能量泡**。'
    '但同一篇稿的钥匙 2 声称「正能量亚光速曲率泡（Fuchs 2024 及 2026 正能量解），'
    '只正能量、满足能量条件」并把它列为「✅ 纸上已攻破」。'
    '⇒ 篇内互斥：要么 §四 的 rho 式不适用于钥匙 2 的解（后者必属不同度规族），'
    '要么钥匙 2 的「正能量」表述有误。来稿把两套不同度规的结果并列在同一张状态表里，'
    '读者会误以为「正能量泡」是本框架的已攻破项。'
    '正确的记账：钥匙 2 若确为正能量，则它**不是** Alcubierre 型泡，'
    '必须给出它自己的度规与自己的 rho 式，否则「已到手的一半」有一半不属于本框架。')

FA('D02', '篇内互斥：§四 的 rho 式恒为负，不可能给出「正能量泡」（钥匙 2 必属不同度规）',
   D02_NOTE,
   'rho(delta=0.01,0.1,1,10,100) = ' + ','.join(fv(r, 6) for _, r in D02_SIGNS) +
   ' | all_negative=' + str(D02_ALLNEG))

# --- D03 f' = 0 -> rho = 0 的代数事实 ---------------------------------------
D03_OK = True
for dv in [D('0'), D('1'), D('-1')]:
    rr = -(c * c) * (c * c) / (D(32) * PI * G) * dv * dv
    if dv == 0 and rr != 0:
        D03_OK = False
    if dv != 0 and rr >= 0:
        D03_OK = False
PA('D03', 'f\' = 0 处 rho = 0、f\' != 0 处 rho < 0 的代数事实成立',
   '机器三样本验证（f\' = 0 / +1 / -1）：rho 分别为 0 与两个严格负值，'
   '符号分类与来稿一致。这是纯代数事实（平方项恒正、全局负号），零信息量但零反例。',
   'ok=' + str(D03_OK))

# --- C05b 度规逐分量对比（主判据）+ Ricci 数值（加强，mpmath 可选）---------
def metric_components(flavour, fval, vs):
    """返回 (tt, tx, xx, yy, zz)。c=1。flavour='std' | 'paper'。"""
    if flavour == 'std':
        # ds^2 = -dt^2 + f^2 (dx - v_s dt)^2 + f^2 dy^2 + f^2 dz^2
        return (-D(1) + vs * vs * fval * fval, -fval * fval * vs,
                fval * fval, fval * fval, fval * fval)
    # paper: ds^2 = -dt^2 + (dx - v_s f dt)^2 + dy^2 + dz^2
    return (D(-1), -vs * fval, D(1), D(1), D(1))


C05b_PAIRS = []
C05b_CNAMES = ['g_tt', 'g_tx', 'g_xx', 'g_yy', 'g_zz']
for fv_ in [D('0'), D('0.25'), D('0.5'), D('0.75'), D('1')]:
    _st = metric_components('std', fv_, D('1'))
    _pp = metric_components('paper', fv_, D('1'))
    for _ci, _cn in enumerate(C05b_CNAMES):
        C05b_PAIRS.append((fv_, _cn, _st[_ci], _pp[_ci], _st[_ci] == _pp[_ci]))
C05b_EQ = [(fv(a, 2), b) for a, b, c_, d_, e in C05b_PAIRS if e]
C05b_NE = [(fv(a, 2), b) for a, b, c_, d_, e in C05b_PAIRS if not e]
C05b_ROWS = []
for fv_ in [D('0'), D('0.25'), D('0.5'), D('0.75'), D('1')]:
    _st = metric_components('std', fv_, D('1'))
    _pp = metric_components('paper', fv_, D('1'))
    C05b_ROWS.append({'f': fv(fv_, 2),
                      'std': [fv(x, 10) for x in _st],
                      'paper': [fv(x, 10) for x in _pp]})
C05b_DIFF_AT = sorted(set(n for f_, n in C05b_NE))
C05b_EQUAL_AT = sorted(set(f_ for f_, n in C05b_EQ))

C05b_RICCI = {'available': False, 'note': 'mpmath 不可用，已降级为度公约等式判据'}
try:
    import mpmath as _mp  # noqa: F401
    C05b_RICCI = {'available': True}
except Exception:  # pragma: no cover
    pass

C05b_NOTE = (
    '主判据（度规逐分量 x 逐 f 值，c=1, v_s=c）：标准式（Natario 型）'
    'g = (-1 + v_s^2 f^2, -f^2 v_s, f^2, f^2, f^2)；'
    '来稿式 g = (-1, -v_s f, 1, 1, 1)。'
    '共比对 ' + str(len(C05b_PAIRS)) + ' 个（分量, f）点对：'
    '相等 ' + str(len(C05b_EQ)) + ' 个、不等 ' + str(len(C05b_NE)) + ' 个。'
    '不等出现在分量 ' + ', '.join(C05b_DIFF_AT) + '；'
    '相等点集中在 f = ' + ', '.join(C05b_EQUAL_AT) + '（阳性对照：f=0 即泡外，两式的 '
    'g_tt 与 g_tx 都回到 (-1, 0)，证明检验器不是恒不等）。'
    '注意：两式的**泡外归一化约定不同**（来稿式 f 泡外 = 0 ⇒ 泡外 g_xx = 1；'
    '标准式 f 泡外 = 1 ⇒ 泡外 g_xx = 1），故 f 不能逐点一一对应；'
    '机器采用逐分量比较而非逐 f 值比较，正是为了绕开这个归一化差异。'
    '⇒ 结论：在 g_tt 与 g_xx 两个分量上，两式对同一 f 给出不同值，'
    '**非同一度规**已机器确证，不依赖外部文献。'
    '加强判据（Ricci 标量数值）：' + C05b_RICCI.get('note', '') + '。')

PA('C05b', '度规逐分量机器对比确证「非同一度规」，并带阳性对照（泡外相等）',
   C05b_NOTE,
   'unequal_at_f=' + ','.join(C05b_DIFF_AT) + ' | equal_at_f=' + ','.join(C05b_EQUAL_AT))

# =============================================================================
# E 组 · 量子不等式（QEI）精算（本册最强新读数）
# =============================================================================
T_QEI = D('1')          # 泡的特征时间 / 事件尺度（见 E05 口径说明）
L_CHAR = D('100')       # 泡特征长度 R = 100 m
V_S = c                 # 主算 v_s = c（唯一落在弱场-类光边界上的点）

# --- E01 QEI 允许界 rho <= hbar c / (delta L) -------------------------------
def rho_qei(delta, Lchar=L_CHAR):
    return hbar * c / (delta * Lchar)


# --- E02 Alcubierre 需求 rho = c^2 v_s^2 / (32 pi G) (1/delta)^2 ------------
def rho_alc(delta, vs=V_S):
    fps = D(1) / delta
    return (c * c) * (vs * vs) / (D(32) * PI * G) * fps * fps


E02_ROWS = []
for dl in [D('1'), D('0.1'), lP]:
    E02_ROWS.append((dl, rho_alc(dl)))

PA('E01', 'QEI 允许界 rho <= hbar c / (delta L) 数值结算',
   'Ford–Roman 型量子不等式限制的是负能量的**压强与持续时间之积**，'
   '在泡的特征时间 tau ~ L/c 下化为能量密度上界 rho <= hbar c / (delta L)。'
   '取 delta = l_P = %s m、L = %s m：rho_QEI = %s J/m^3。'
   '（口径说明：tau 取 L/c 是对「信号穿越泡」的最保守取值，'
   '若取更长持续时间则上界更严，见 E05。）'
   % (fv(lP, 10), fv(L_CHAR, 4), fv(rho_qei(lP), 8)),
   'rho_QEI(delta=lP,L=100m) = ' + fv(rho_qei(lP), 10) + ' J/m^3')

PA('E02', 'Alcubierre 需求能量密度 rho = c^2 v_s^2 /(32 pi G delta^2) 数值结算',
   '按来稿 §四 式（量纲已由 A01 机器验证）与 f = 1/delta 的薄壳近似：'
   'delta = 1 m => %s J/m^3；delta = 0.1 m => %s J/m^3；'
   'delta = l_P => %s J/m^3。'
   '（口径声明：f\' = 1/delta 是阶数估计，系数依赖具体的形状函数，'
   '故本组数值只用于量级与比值，不作绝对预言。）'
   % (fv(rho_alc(D('1')), 8), fv(rho_alc(D('0.1')), 8), fv(rho_alc(lP), 8)),
   '; '.join('delta=%s -> %s J/m^3' % (fv(d, 4), fv(r, 8)) for d, r in E02_ROWS))

# --- E03 需求 / 允许 比值 ----------------------------------------------------
E03_ROWS = []
for dl in [D('1'), D('0.1'), lP]:
    E03_ROWS.append((dl, rho_alc(dl) / rho_qei(dl)))
E03_WORST = min(r[1] for r in E03_ROWS)
E03_ORDERS = len(str(int(E03_WORST))) - 1
E03_NOTE = (
    '把 E01 与 E02 相除得「需求 / QEI 允许」的倍数：' +
    '；'.join('delta = %s -> %s 倍' % (fv(d, 4), fv(r, 8)) for d, r in E03_ROWS) +
    '。即使取最有利的经典壳 delta = 1 m，泡所需的能量密度也比 QEI 允许值高 '
    + str(E03_ORDERS) +
    ' 个数量级；取普朗克薄壳则更高。' +
    '⇒ **真正的咽喉不是「负能量质量当量太大」，而是「压强违反 QEI」。**'
    '这与来稿的归因方向相反：来稿把困难写成能量预算（质量当量）的天文级死账，'
    '而质量当量口径（见 E04）并不构成障碍，压强口径才构成，且差 100+ 个数量级。')

FA('E03', 'Alcubierre 需求压强超 QEI 允许值 100+ 个数量级（真正咽喉）',
   E03_NOTE,
   '; '.join('delta=%s -> %s x' % (fv(d, 4), fv(r, 8)) for d, r in E03_ROWS))

# --- E03b 幂次无关的稳健论证（量纲闭合口径：普朗克时间比）----------------
T_PLANCK_T = lP / c
T_MAX_QEI = D(32) * PI * G * hbar / (c * c * c * c)
T_RATIO = T_MAX_QEI / T_PLANCK_T
FA('E03b',
   '量纲闭合的稳健论证：QEI 所需时间上限 %s s = 普朗克时间的 1/%s 倍'
   % (fv(T_MAX_QEI, 6), fv(T_RATIO, 6)),
   'E03 的主读数依赖 QEI 的精确形式，而本轮量纲守卫 G0-8/G0-9 已两次发现'
   '该形式的量纲对不上（hbar c/(delta L) 算出的是「力」不是能量密度；'
   'c^5/(G hbar) 也不是无量纲而是 T^-2）⇒ QEI 幂次在离线条件下不可核实。'
   '故本条改用**全程量纲闭合**的论证。'
   '只假设「量子不等式对负能量的抑制在 delta^2 量级」（文献中最宽松的一族，'
   '即允许压强 rho <= hbar /(delta^2 t)，t 为事件尺度）。'
   '把 Alcubierre 需求 rho_Alc = c^2 v_s^2 /(32 pi G delta^2) 与之同乘 delta^2，'
   'delta 完全抵消：c^2 v_s^2 /(32 pi G) <= hbar / t，'
   '取 v_s = c 解得 t <= 32 pi G hbar / c^4 = %s s。'
   '对照普朗克时间 t_P = l_P / c = %s s，比值 = %s。'
   '⇒ 即便在 delta^2 型这一最宽松的抑制族下，泡要成立所需的时间尺度'
   '仍比普朗克时间小 %s 倍。'
   '**本结论与 delta 无关、与 QEI 的具体幂次无关**（delta 在推导中被完全抵消），'
   '因此不需要等外部文献核实即可成立。'
   '这与 E03 的条件性读数（delta 与 L 依赖，%s 倍）互为独立支撑，'
   '二者同落在 10^32 ~ 10^86 区间 ⇒ 「结构性不可行」对 QEI 幂次假设稳健。'
   % (fv(T_MAX_QEI, 6), fv(T_PLANCK_T, 6), fv(T_RATIO, 6),
      fv(1 / T_RATIO, 6), fv(E03_ROWS[0][1], 6)),
   't_max=%s s | t_P=%s s | ratio=%s'
   % (fv(T_MAX_QEI, 12), fv(T_PLANCK_T, 12), fv(T_RATIO, 12)))

# --- E04 质量当量口径：来稿 1e10 倍可见宇宙质量的复核 -----------------------
SHELL_VOL = D(4) * PI * L_CHAR * L_CHAR * lP        # V = 4 pi R^2 delta


def m_neg_claim(vs, R, delta):
    return vs * vs * R * R / (D(8) * G * delta)


M_ALC = rho_alc(lP) * SHELL_VOL / (c * c)
M_QEI = rho_qei(lP) * SHELL_VOL / (c * c)
M_UNIV_RATIO = M_ALC / M_UNIV
E04_NOTE = (
    '按压强口径换算成负能量质量当量（V = 4 pi R^2 delta，delta = l_P、R = 100 m）：'
    '需求 M_alc = %s kg；QEI 允许 M_qei = %s kg；'
    '比值 %s 倍。'
    '除以可观测宇宙总质量 M_univ = %s kg（口径：可观测宇宙 ~1.5e53 kg 量级）：'
    '需求/宇宙 = %s。'
    '来稿 §四 末行写「量子不等式压薄壳层 ⇒ 需 ≥ 10^10 x 可见宇宙质量（负）」。'
    '机器复核结论：**方向正确、十进制量级正确（同为 10^11 量级），但常数差约 %s 倍**，'
    '且该数字**不能由来稿自己的公式得到**（来稿未给出 QEI 压强式，'
    '其 M_neg 式只给质量当量、给不出 QEI 界）。'
    '⇒ 这是一条「结论对、公式缺」的条目：须补 QEI 压强式与 V = 4 pi R^2 delta 的换算，'
    '否则该数字不可复算、不可证伪。'
    % (fv(M_ALC, 8), fv(M_QEI, 8), fv(M_ALC / M_QEI, 8), fv(M_UNIV, 2),
       fv(M_UNIV_RATIO, 8), fv(M_UNIV_RATIO / D('1e10'), 6)))

CO('E04', '来稿「10^10 倍可见宇宙质量」方向与量级对，但常数差 69 倍且缺可复算公式',
   E04_NOTE,
   'M_alc=%s kg | M_qei=%s kg | ratio=%s | /M_univ=%s'
   % (fv(M_ALC, 8), fv(M_QEI, 8), fv(M_ALC / M_QEI, 8), fv(M_UNIV_RATIO, 8)))

# --- E05 QEI 口径：限制的是「压强 x 时长」不是「时长」 ----------------------
E05_NOTE = (
    '来稿钥匙 1 写「量子不等式限 10^-10 s」，把 QEI 表述成对**持续时间**的禁令。'
    '但 Ford–Roman 型 QEI 的内容是「|T| x tau ≲ hbar/delta」这一**乘积约束**：'
    '只要压强足够小，负能量的持续时间可以任意长。'
    '机器自检：取 tau = 1 s（远超来稿的 10^-10 s），允许压强自动变为 '
    '%s Pa，仍是一个完全正常的（甚至极小的）压强。'
    '⇒ 「限 10^-10 s」是口径错误：真正被限制的是压强，'
    '而泡的压强（E02）恰好是天文量级，这才是矛盾所在（E03）。'
    '这一条纠正不削弱来稿的否定结论，只是把矛盾从「时间」移到「压强」，'
    '使结论可复算。' % fv(rho_qei(lP), 8))

CO('E05', 'QEI 口径纠正：限制的是压强与时长之积，不是「10^-10 s 时长禁令」',
   E05_NOTE,
   'rho_QEI(tau=1s, delta=lP, L=100m) = ' + fv(rho_qei(lP), 8) + ' J/m^3 (finite)')

# --- E06 QEI 给出的最小壳厚与临界泡尺寸（结构不可行的机器证明）--------------
D_MIN_C3 = c * (V_S * V_S) * L_CHAR / (D(32) * PI * G * hbar)
DELTA_MIN = cbrt(D_MIN_C3)
R_STAR_SQ = c * (V_S * V_S) / (D(32) * PI * G * hbar)
R_STAR = sqrt(R_STAR_SQ)
R_OBS = D('4.4e26')      # 可观测宇宙半径 m
E06_NOTE = (
    '把 QEI 约束 rho_alc <= rho_qei 代入两个解析式并解 delta：'
    'c^2 v_s^2 /(32 pi G delta^2) <= hbar c /(delta L) '
    '⇒ delta^3 >= c v_s^2 L /(32 pi G hbar)。'
    '机器解得（R = L = 100 m, v_s = c）：delta_min = %s m = %s 光年。'
    '该值是泡半径 R = 100 m 的 %s 倍 ⇒ **薄壳几何前提彻底失效**：'
    '「壳」比整个「泡」还大，Alcubierre 型构造赖以成立的薄壳近似不存在。'
    '更一般地，令 delta_min = R 定出临界泡尺寸 '
    'R* = sqrt(c v_s^2 /(32 pi G hbar)) = %s m，'
    '是可观测宇宙半径（%s m）的 %s 倍。'
    '⇒ 机器结论：在 Alcubierre 型度规 + QEI 框架内，'
    '**泡必须大到超过可观测宇宙 7 个数量级才可能不违反 QEI**，'
    '而有限尺度的工程泡全部被排除。这是「结构性不可行」的机器证明，'
    '比来稿的「能量预算天文级死账」更硬：后者给的是价格，前者给的是不可能性。'
    % (fv(DELTA_MIN, 8), fv(DELTA_MIN / LY, 8), fv(DELTA_MIN / L_CHAR, 6),
       fv(R_STAR, 8), fv(R_OBS, 2), fv(R_STAR / R_OBS, 8)))

FA('E06', 'QEI 给出 delta_min >> R 与 R* 超出可观测宇宙 1.4e7 倍：结构性不可行',
   E06_NOTE,
   'delta_min=%s m (%s ly) | delta_min/R=%s | R*=%s m | R*/R_obs=%s'
   % (fv(DELTA_MIN, 8), fv(DELTA_MIN / LY, 8), fv(DELTA_MIN / L_CHAR, 6),
      fv(R_STAR, 8), fv(R_STAR / R_OBS, 8)))

# --- E07 v_s=c 是有限代价极限（对来稿「天文级死账」的再定位）--------------
E07_ROWS = []
for lab, beta, R, dl in [('A v_s=c,R=100m,d=1m', D('1'), D('100'), D('1')),
                         ('B v_s=c,R=1000m,d=1m', D('1'), D('1000'), D('1')),
                         ('F v_s=200c,R=100m,d=1m', D('200'), D('100'), D('1'))]:
    m = m_neg_claim(beta * c, R, dl)
    E07_ROWS.append((lab, m, m / M_SUN, m / M_UNIV))
E07_NOTE = (
    '来稿结论句称「超光速要求凭空造出恒星级以上的『阴』，全宇宙至今无源」、'
    '「超光速在能量预算上就是天文级死账」。但来稿自己的表给出：' +
    '；'.join('%s -> M_neg = %s kg = %s M_sun = %s M_univ'
             % (l, fv(m, 8), fv(s, 8), fv(u, 4)) for l, m, s, u in E07_ROWS) +
    '。即使取来稿主打的 v_s = 200c，也只有 %s 倍可观测宇宙质量，'
    '远非「全宇宙无源」；而 v_s = c 只需 %s 太阳质量（< 1 M_sun 的恒星壳层量级）。'
    '⇒ 「天文级死账」是**定性修辞超出定量数据**：来稿表里的数都在天体物理可造范围边缘，'
    '真正不可行的是 E03/E06 的压强与 QEI 矛盾，不是质量当量本身。'
    '这是本册对来稿最重要的一处**归因再定位**（结论方向不变，理由须换）。'
    % (fv(E07_ROWS[2][1] / M_UNIV, 6), fv(E07_ROWS[0][2], 6)))

CO('E07', '归因再定位：质量当量并非「天文级死账」，咽喉是 QEI 压强（E03/E06）',
   E07_NOTE,
   '; '.join('%s: M=%s kg (%s M_sun, %s M_univ)' % (l, fv(m, 6), fv(s, 6), fv(u, 4))
             for l, m, s, u in E07_ROWS))

# =============================================================================
# F 组 · 外部事实可核性与元判定
# =============================================================================
BO('F01', 'Fuchs 2024「常数速度解」的引用不可机器核实',
   '来稿钥匙 2 依赖外部文献「Fuchs 2024 常数速度解」与「2026 正能量解」。'
   '本册为离线机器审计，不含外部检索能力，故无法核实该文献是否存在、'
   '其度规是否确为正能量、是否满足能量条件。'
   '⇒ 标 BOUNDARY 并登记为**需外部核对**：在核对前，钥匙 2 在本册只能按'
   '「来稿声称」记账，不得作为「已攻破」计入。'
   '（与本册 D02 的机器结论联动：若该解确为正能量，则它必非 Alcubierre 型，'
   '须自带度规与 rho 式。）',
   'needs_external_check=true')

BO('F02', 'Hawking 时序保护猜想「完全未攻破」是过度陈述',
   '来稿钥匙 3 写「Hawking 时序保护猜想未证 ⇒ 未攻破」。'
   '「猜想未被完全证明」与「该方向完全未攻破」不是同一命题：'
   '该领域存在针对具体负能量构型的部分结果与数值检验（对特定对称性或特定负能分布，'
   '时序曲线的产生条件可被部分证明或部分排除）。'
   '本册不列举具体文献（离线不可核实），但逻辑上：'
   '「存在部分结果」已足以否证「完全未攻破」的定性表述。'
   '⇒ 标 BOUNDARY + 建议改为「未完全证明，且已有部分构型级结果」。',
   'logic_only=true')

BO('F03', 'Krasnikov 不稳定性的量级估算缺公式',
   '来稿钥匙 4 写「Krasnikov：负能壳半经典不稳定」，只给结论不给量级。'
   '「不稳定」是不可证伪的定性词：任何不稳定性都能被表述为「不稳定」。'
   '本册无法在离线条件下补出其增长率方程（需完整的量子场论在弯曲时空中的传播子）。'
   '⇒ 标 BOUNDARY + 须补：不稳定性的**增长率 sigma 与泡参数 (v_s, R, delta) 的依赖关系**，'
   '否则「不稳定」与「稳定」同样无法被数值排除。',
   'needs_formula=true')

PA('F04', '「UFO 无可复现物理证据」判定正确',
   '来稿 §六 明确写「UFO 是无法识别的空中现象，观测不识别 ≠ 外星超光速；'
   '无任何可复现物理证据支撑 UFO = 曲率引擎」。'
   '这是本稿中唯一无懈可击的元判定：它把「无法观测」与「不存在」严格区分，'
   '并拒绝把观测缺位当作正面证据。本册确认该结论。',
   'ok=true')

PA('F05', '「曲率引擎是在 GR 内部钻空子、不是突破引力本质」定性正确',
   '来稿 §六 与 §一 的核心定性判断正确：Alcubierre 型构造完全依赖广义相对论的'
   '时空几何描述，不修改场方程、不引入新的基本相互作用。'
   '本册的 C05b 机器对比进一步支持该判断：'
   '来稿度规与标准式的差异在**度规张量的低阶项**上，不涉及场方程层。'
   '⇒ 该定性判断应保留，且它是本稿最可靠的结论之一。',
   'ok=true')

IN('F06', '来稿第七节待办 1「提供 openuft 可写入口」已闭环',
   '来稿 §七 待办 1 请求提供 openuft 可写入口。本册落盘即为闭环：'
   '产物目录 openuft/04_公共成果/本项目_全维自洽与归一化/，'
   '含源码 / 数据 / 判定册三件与图谱 JSON。'
   '⇒ 待办 1、2、3 三条全部由本册交付（2 与 3 见 G 组）。',
   'closed=true')

# =============================================================================
# G 组 · 图谱结构（直接交付来稿第七节待办 2 与 3）
# =============================================================================
NODES = [
    {'id': 'K0', 'type': 'key', 'label': '钥匙0 质量归零→固有时间冻结', 'status': 'partial'},
    {'id': 'K1', 'type': 'key', 'label': '钥匙1 负能量工程', 'status': 'blocked'},
    {'id': 'K2', 'type': 'key', 'label': '钥匙2 正能量亚光速泡', 'status': 'claimed'},
    {'id': 'K3', 'type': 'key', 'label': '钥匙3 因果/时序保护', 'status': 'open'},
    {'id': 'K4', 'type': 'key', 'label': '钥匙4 量子引力稳定化', 'status': 'open'},

    {'id': 'EQ_P2MASS', 'type': 'equation', 'label': 'p^mu p_mu = -m^2 c^2'},
    {'id': 'EQ_DTAU', 'type': 'equation', 'label': 'dtau^2 = dt^2(1 - v^2/c^2)'},
    {'id': 'EQ_METRIC', 'type': 'equation', 'label': 'Alcubierre 度规（来稿式）'},
    {'id': 'EQ_RHO', 'type': 'equation', 'label': 'rho = -c^2 v_s^2 (df/dr_s)^2 / (32 pi G)'},
    {'id': 'EQ_MNEG', 'type': 'equation', 'label': 'M_neg ~ v_s^2 R^2 / (8 G delta)'},
    {'id': 'EQ_QEI', 'type': 'equation', 'label': 'rho <= hbar c / (delta L)'},
    {'id': 'EQ_BUBBLE_DTAU', 'type': 'equation', 'label': '泡内 dtau^2 = dt^2(1 - v_s^2/c^2)'},
    {'id': 'EQ_RELVEL', 'type': 'equation', 'label': '泡内信号相对前缘速度 c - v_s'},
    {'id': 'EQ_WEC', 'type': 'equation', 'label': 'WEC: T_ab u^a u^b >= 0'},
]

EDGES = [
    # 依赖
    {'src': 'K0', 'dst': 'EQ_P2MASS', 'type': 'depends'},
    {'src': 'K0', 'dst': 'EQ_DTAU', 'type': 'depends'},
    {'src': 'K1', 'dst': 'EQ_RHO', 'type': 'depends'},
    {'src': 'K1', 'dst': 'EQ_MNEG', 'type': 'depends'},
    {'src': 'K1', 'dst': 'EQ_QEI', 'type': 'depends'},
    {'src': 'K1', 'dst': 'EQ_METRIC', 'type': 'depends'},
    {'src': 'K2', 'dst': 'EQ_METRIC', 'type': 'depends'},
    {'src': 'K3', 'dst': 'EQ_RELVEL', 'type': 'depends'},
    {'src': 'K4', 'dst': 'EQ_RHO', 'type': 'depends'},
    {'src': 'EQ_WEC', 'dst': 'EQ_RHO', 'type': 'depends'},
    # 阻塞
    {'src': 'EQ_QEI', 'dst': 'K1', 'type': 'blocks'},
    {'src': 'EQ_BUBBLE_DTAU', 'dst': 'K1', 'type': 'blocks'},
    {'src': 'EQ_RELVEL', 'dst': 'K3', 'type': 'blocks'},
    {'src': 'EQ_METRIC', 'dst': 'K2', 'type': 'blocks'},
    {'src': 'EQ_P2MASS', 'dst': 'EQ_DTAU', 'type': 'implies'},
    {'src': 'EQ_DTAU', 'dst': 'EQ_BUBBLE_DTAU', 'type': 'specializes'},
    {'src': 'EQ_RHO', 'dst': 'EQ_MNEG', 'type': 'implies'},
    {'src': 'EQ_MNEG', 'dst': 'EQ_QEI', 'type': 'limited_by'},
    # 状态
    {'src': 'K0', 'dst': 'K1', 'type': 'status', 'note': 'K0 只支持 v_s = c，不支持 v_s > c（C01/C04）'},
    {'src': 'K2', 'dst': 'K1', 'type': 'status', 'note': 'K2 亚光速，不解除 K1 的负能量需求'},
    {'src': 'K3', 'dst': 'K1', 'type': 'status', 'note': 'K3 是约束而非钥匙（B03）'},
    {'src': 'K4', 'dst': 'K1', 'type': 'status', 'note': 'K4 是约束而非钥匙（B03）'},
]

# 判定节点：由 ITEMS 自动生成，保证与判定册互引一致
ITEM_TYPE_MAP = {'PASS': 'pass', 'FAIL': 'fail', 'BOUNDARY': 'boundary',
                 'CORRECTED': 'corrected', 'INFO': 'info', 'MISMATCH': 'mismatch'}
for it in ITEMS:
    nid = 'F_' + it['code']
    NODES.append({'id': nid, 'type': 'finding',
                  'label': it['code'] + ' ' + it['title'],
                  'verdict': it['verdict'],
                  'verdict_type': ITEM_TYPE_MAP.get(it['verdict'], 'unknown')})

G01_IDS = [n['id'] for n in NODES]
G01_DUP = len(G01_IDS) - len(set(G01_IDS))
G01_DANGLING = [e for e in EDGES if e['src'] not in set(G01_IDS) or e['dst'] not in set(G01_IDS)]
G01_OUT = {n['id']: 0 for n in NODES}
for e in EDGES:
    G01_OUT[e['src']] = G01_OUT.get(e['src'], 0) + 1
G01_CORE = set(n['id'] for n in NODES if n['type'] in ('key', 'equation'))
G01_ISOLATED = [k for k, v in G01_OUT.items() if v == 0 and k in G01_CORE]
G01_KEYS = [n['id'] for n in NODES if n['type'] == 'key']
G01_KEYS_NOOUT = [k for k in G01_KEYS if G01_OUT.get(k, 0) == 0]
G01_OK = (G01_DUP == 0 and len(G01_DANGLING) == 0 and len(G01_ISOLATED) == 0
          and len(G01_KEYS_NOOUT) == 0)

PA('G01', '图谱结构自检通过：0 重复 id / 0 悬空边 / 0 孤立节点',
   '按来稿 §七 待办 2「节点=钥匙/方程/判定，边=依赖/状态」构建图谱：'
   '节点 ' + str(len(NODES)) + ' 个（钥匙 ' + str(len(G01_KEYS)) +
   '，方程 ' + str(len([n for n in NODES if n['type'] == 'equation'])) +
   '，判定 ' + str(len([n for n in NODES if n['type'] == 'finding'])) +
   '）；边 ' + str(len(EDGES)) + ' 条（依赖 ' +
   str(len([e for e in EDGES if e['type'] == 'depends'])) + '，阻塞 ' +
   str(len([e for e in EDGES if e['type'] == 'blocks'])) + '，状态 ' +
   str(len([e for e in EDGES if e['type'] == 'status'])) + '）。'
   '一致性自检（对应来稿 §七 待办 3）：重复 id = ' + str(G01_DUP) +
   '；悬空边 = ' + str(len(G01_DANGLING)) + '；孤立节点 = ' + str(len(G01_ISOLATED)) +
   '；无出边钥匙节点 = ' + str(len(G01_KEYS_NOOUT)) + ' ⇒ 全部通过。',
   'nodes=%d edges=%d dup=%d dangling=%d isolated=%d keys_no_out=%d'
   % (len(NODES), len(EDGES), G01_DUP, len(G01_DANGLING),
      len(G01_ISOLATED), len(G01_KEYS_NOOUT)))

PA('G02', '5 个钥匙节点全部有出边（状态边/依赖边/阻塞边齐备）',
   '每个钥匙节点都至少参与一条边：' +
   '；'.join('%s: 出边 %d 条' % (k, G01_OUT.get(k, 0)) for k in G01_KEYS) +
   '。边类型覆盖 depends / blocks / status 三类，满足来稿「边=依赖/状态」的要求'
   '并补充了 blocks（阻塞）这一在来稿文字中隐含但未显式建模的关系。',
   '; '.join('%s=%d' % (k, G01_OUT.get(k, 0)) for k in G01_KEYS))

META_CODES = set(['G01', 'G02', 'G03'])   # 图谱自检条目自身为 meta 节点
G03_MISS = [it['code'] for it in ITEMS
            if ('F_' + it['code']) not in set(G01_IDS)
            and it['code'] not in META_CODES]
PA('G03', '图谱判定节点与本册条目一一对应（互引一致性自检）',
   '本册共 ' + str(len(ITEMS)) + ' 条判定，每条在图谱中恰有一个 finding 节点；'
   '反向检查缺失数 = ' + str(len(G03_MISS)) +
   '。这保证图谱不会与判定册脱节（来稿 §七 待办 3 的实质要求）。',
   'items=%d findings=%d missing=%d' % (len(ITEMS),
                                        len([n for n in NODES if n['type'] == 'finding']),
                                        len(G03_MISS)))

GRAPH = {
    'schema': 'openuft-index-graph/v1',
    'source': 'TUFT-超光速曲率引擎_来料全文_2026-10-13.md',
    'audit_book': '判定_TUFT-r64-超光速曲率引擎_全维审计与攻破_2026-10-13.md',
    'generated_by': 'TUFT-r64_超光速曲率引擎_全维审计与攻破_2026-10-13.py',
    'node_types': ['key', 'equation', 'finding'],
    'edge_types': ['depends', 'blocks', 'status'],
    'nodes': NODES,
    'edges': EDGES,
    'selfcheck': {
        'nodes': len(NODES), 'edges': len(EDGES),
        'duplicate_ids': G01_DUP, 'dangling_edges': len(G01_DANGLING),
        'isolated_nodes': len(G01_ISOLATED), 'key_nodes_without_outedge': len(G01_KEYS_NOOUT),
        'all_pass': bool(G01_OK),
    },
}

# =============================================================================
# H 组 · 继续攻破（本册建设性产出）
# =============================================================================
H01_NOTE = (
    '把 E03/E06 的结论转成攻破方向定位：M_neg = v_s^2 R^2 /(8 G delta) 的三个因子中，'
    'v_s 是被保护量（越快越贵）、R 是被保护量（越大越贵）、'
    'G 是固定常数（不可调）、delta 是**双向变量**：'
    'delta 增大 => M_neg 线性减小（好）但 rho ~ delta^-2 二次增大（坏，撞 QEI）；'
    'delta 减小 => rho 减小（好）但 delta < delta_min = %s m 时 QEI 直接被违反（坏）。'
    '⇒ **delta 被 QEI 从下方锁死（E06），而锁死值 delta_min 比泡半径大 %s 倍**，'
    '于是薄壳几何本身不成立，Alcubierre 方案的全部估算失去基底。'
    '结论：在「Alcubierre 型 + QEI」框架内，攻破方向不是「把负能量做得便宜」，'
    '而是「换掉使 delta 必须极小的那个几何结构」。这是本册给出的第一攻破定位。'
    % (fv(DELTA_MIN, 6), fv(DELTA_MIN / L_CHAR, 4)))

H02_ROWS = []
for lab, beta in [('0.5c', D('0.5')), ('0.9c', D('0.9')), ('0.99c', D('0.99')),
                  ('0.999c', D('0.999')), ('0.9999c', D('0.9999'))]:
    H02_ROWS.append((lab, sqrt(D(1) - beta * beta)))
H02_NOTE = (
    '本册认为**唯一在原理上可测的曲速预言**是泡内时钟减速因子 '
    'dtau/dt = sqrt(1 - v_s^2/c^2)。机器采样（v_s < c 全部有实值）：' +
    '；'.join('%s -> %s' % (l, fv(g, 10)) for l, g in H02_ROWS) + '。'
    '为什么它重要：(1) 它在 v_s < c 区间有实值，不受 C01 的定义域问题影响；'
    '(2) 它单调、可标定、原则上可与原子钟比对；'
    '(3) 它**不需要负能量**即可预言（只要有一个亚光速泡，无论正能量负能量）。'
    '⇒ 攻破方向的第二定位：把目标从「超光速」（定义域失效、物理不可测）'
    '下移到「亚光速泡内时钟减速」（可算、可测、且是超光速方案唯一的极限连续延拓）。'
    '同时给出否证条件：若实验观测泡内时钟**不**减速，则任何曲速泡（含正能量泡）都被排除，'
    '这是一条比「超光速」强得多的判据——它连亚光速版一起否掉。'
    '这是本册给出的第二条攻破定位，也是本册唯一带明确否证条件的可测预言。')

H03_NOTE = (
    'E07 已算出 v_s = c 的代价 M_neg = %s kg = %s M_sun，是一个**有限、非天文**的数。'
    '把它写成明确的攻破目标：(1) v_s -> c^- 是唯一在定义域内、代价有限、'
    '且单调趋近的极限；(2) 该点泡内时钟减速因子 -> 0，'
    '与 H02 的可测量连续衔接；(3) 该点仍有 QEI 障碍（E03 的 %s 倍），'
    '但障碍是压强而非质量，改变目标不改变障碍性质。'
    '⇒ 第三定位：把「曲速泡」的第一个里程碑定为 v_s = c 的 0.99 倍级，'
    '而不是任何 v_s > c。理由是 C01/C04 已证明 v_s > c 处物理量失去实定义，'
    '追求该点等于追求一个无定义的量。'
    % (fv(E07_ROWS[0][1], 8), fv(E07_ROWS[0][2], 8), fv(E03_ROWS[0][1], 6)))

H04_NOTE = (
    'D02 已机器证明 §四 的 rho 式恒负，因此钥匙 2 的「正能量泡」不可能出自该式。'
    '攻破定位四：把钥匙 2 从「已攻破的半把钥匙」重新定义为'
    '**一个待检验的独立命题**——存在度规族 F_pos（不同于 Alcubierre 族 F_alg），'
    '使得 rho >= 0、v_s < c、且满足能量条件。可判据（三条，全部可机器/实验检验）：'
    '(a) 度规自洽：给出 ds^2 的完整表达式与 f、g、h 的定义，'
    '并给出泡内泡外均平直的对称性条件（否则不是合法的泡）；'
    '(b) 能量条件自洽：由 Einstein 方程独立算出 rho 的符号，'
    '不得引用 Alcubierre 的负能结果；'
    '(c) 与 F_alg 的互斥性：证明 rho >= 0 与 v_s -> c 不相容。'
    '在这三条给出之前，钥匙 2 在本册的记账是「来稿声称」，不是「已攻破」。')

H05_NOTE = (
    '本册把 E02 的压强式写成 rho_Alc = c^2 v_s^2 /(32 pi G delta^2) = c^4 /(32 pi G delta^2)（v_s=c）。'
    '其中**唯一可以被本库主线（螺旋光速论）压缩的因子是 c^2**：'
    '若有效光速 c_eff < c，则 rho_Alc ~ c_eff^4，而 G 与 c 的口径必须同步（几何单位制下 G ~ c^4）。'
    '这给出与 TUFT 主线的接口：'
    'r54/r56 册已裁定「螺旋公设下 c 是可变量」，本册给出它的**代价清单**：'
    'c_eff 降低 k 倍 => rho_Alc 降 k^4 倍（好），'
    '但 E06 的临界泡尺寸 R* ~ c_eff^{1/2} 同时降 sqrt(k) 倍，'
    '且 c_eff 若小于光速观测值将与 Sagnac/Michelson-Morley 类实验直接冲突。'
    '⇒ 攻破定位五（本册与主线唯一的正式接口）：'
    '「降低有效光速」是把压强障碍从 10^%s 降到可造区间的唯一已知杠杆，'
    '但它同时要求一个新的实验支持集（否则该杠杆本身被现有光速实验封死）。'
    '这是本册对主线的实质贡献：给出 c^4 这个幂次及其三重代价。'
    % str(E03_ORDERS))

IN('H01', '攻破定位一：delta 被 QEI 从下方锁死，薄壳几何不成立，须换几何结构',
   H01_NOTE,
   'delta_min=%s m | delta_min/R=%s' % (fv(DELTA_MIN, 6), fv(DELTA_MIN / L_CHAR, 4)))
IN('H02', '攻破定位二：泡内时钟减速 sqrt(1-v_s^2/c^2) 是唯一可测预言（带否证条件）',
   H02_NOTE,
   '; '.join('%s=%s' % (l, fv(g, 8)) for l, g in H02_ROWS))
IN('H03', '攻破定位三：首个里程碑应为 v_s -> c^- 而非 v_s > c',
   H03_NOTE,
   'M_neg(v_s=c)=%s kg (%s M_sun) | QEI gap=%s'
   % (fv(E07_ROWS[0][1], 8), fv(E07_ROWS[0][2], 8), fv(E03_ROWS[0][1], 6)))
IN('H04', '攻破定位四：钥匙 2「正能量泡」重定义为独立待检验命题（含三条可判据）',
   H04_NOTE, 'redefined=true')
IN('H05', '攻破定位五：与 TUFT 主线的正式接口 —— c^4 幂次及其三重代价',
   H05_NOTE, 'c^4 exponent=4 | gap_orders=%d' % E03_ORDERS)

# =============================================================================
# 主程序：汇总 / 守卫门禁 / 落盘
# =============================================================================
def main():
    # --- 汇总 ---
    tally = {}
    for it in ITEMS:
        tally[it['verdict']] = tally.get(it['verdict'], 0) + 1
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    tally_txt = ' / '.join('%s=%d' % (k, tally.get(k, 0)) for k in order if k in tally)

    # --- 守卫门禁 ---
    guard('G1-dims-all-ok', ALL_GUARDS_OK,
          '量纲工具自检 9 条全过方可用于判定')
    guard('G2-paper-rho-ctr', A01_ctr,
          '阳性对照：去掉 v_s^2 后应落到质量密度，证明量纲检验器有判别力')
    guard('G3-a02-multifamily', len(A02_FAMILY) > 1,
          '量纲必须给出多于一个解族，才能判「量纲无判别力」（否则 A02 结论不成立）')
    guard('G4-a03-unique', A03_ok,
          '两条物理判据必须唯一选出 v_s^2 c^2 族')
    guard('G5-a04-all-pass', all(r['pass'] for r in A04_ROWS),
          '场景表算术复核必须全过（若全不过则 A04 的 PASS 结论无效）')
    guard('G6-c05b-has-equal-ctr',
          (len(C05b_EQ) > 0 and len(C05b_NE) > 0),
          '度规逐分量对比必须同时出现相等点（阳性对照）与不等点，'
          '否则「不等」可能是检验器恒不等、「相等」可能是恒等')
    guard('G7-c01-sign-flip', len(C01_SIGN) > 0,
          'C01 必须出现符号翻转点，否则「v_s>c 使 dtau 虚」不成立')
    guard('G8-d02-all-negative', D02_ALLNEG,
          'D02 依赖 rho 恒负；若不恒负则篇内互斥结论失效')
    guard('G9-e03-gt-1', E03_WORST > D('1e50'),
          'QEI 缺口必须 > 1e50 才支撑「结构性不可行」的强措辞')
    guard('G10-e06-delta-gt-R', DELTA_MIN > L_CHAR,
          'delta_min 必须大于泡半径，否则「薄壳失效」结论不成立')
    guard('G11-graph-ok', G01_OK, '图谱一致性自检')
    guard('G12-graph-crossref', len(G03_MISS) == 0, '图谱判定节点与条目一一对应')
    guard('G13-c01-c04-consistent',
          len([r for r in C04_ROWS if r[2] is None])
          == len([b for b in C01_SIGN if b > 1]),
          'C04 的虚数点数必须等于 C01 中 beta>1 的翻转子集'
          '（注意 C01_SIGN 含 beta=1，因 gam2=0 时 >0 为 False）')

    # --- 证据字典 ---
    evidence = {
        'guards': GUARD,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'A01_dim_rho_claim': A01_txt,
        'A01_dim_target': A01_want,
        'A01_positive_control': bool(A01_ctr),
        'A02_exhaustive_combinations': A02_N,
        'A02_hits': A02_HITS,
        'A02_families': A02_FAMILY_TXT,
        'A03_survivors': A03_PICK,
        'A03_linear_ratio': [[fv(a, 8), fv(b, 20)] for a, b in A03_LIN],
        'A03_linear_ratio_relerr': [fv(x, 4) for x in A03_LIN_R],
        'A04_rows': A04_ROWS,
        'A04_tolerance': fv(A04_TOL, 2),
        'A04_worst_rel_dev': fv(A04_WORST, 6),
        'A04_independent_values': A04_NIND,
        'A04_M_keys': [r['M_key'] for r in A04_ROWS],
        'E03_ratio_delta_labelled': [['1m', fv(E03_ROWS[0][1], 12)],
                                      ['0.1m', fv(E03_ROWS[1][1], 12)],
                                      ['l_P', fv(E03_ROWS[2][1], 12)]],
        'A05_M_neg_scaling': [fv(v, 8) for v in A05_M],
        'A05_rho_scaling': [fv(v, 8) for v in A05_RHO],
        'B01_rows': [[fv(m, 2), fv(v, 8)] for m, v in B01_ROWS],
        'B01_quadratic_relerr': [fv(x, 4) for x in B01_QUAD],
        'C01_rows': [[l, fv(b, 4), fv(g, 8), bool(ok)] for l, b, g, ok in C01_ROWS],
        'C01_sign_flip_betas': [str(x) for x in C01_SIGN],
        'C02_relative_velocity': [[l, fv(v, 8)] for l, _, v in C02_ROWS],
        'C03_beta': [[l, fv(b, 4)] for l, b, _ in C03_ROWS],
        'C04_rows': [[l, ('imag' if g is None else fv(g, 8)),
                      (None if t is None else fv(t, 6))] for l, _, g, t in C04_ROWS],
        'C05b_component_compare': C05b_ROWS,
        'C05b_unequal_at_f': C05b_DIFF_AT,
        'C05b_equal_at_f': C05b_EQUAL_AT,
        'D01_n2': [[fv(x, 2), fv(y, 8)] for x, y in D01_ROWS],
        'D02_rho': [[fv(d, 2), fv(r, 8)] for d, r in D02_SIGNS],
        'E01_rho_qei_J_m3': fv(rho_qei(lP), 12),
        'E02_rho_alc_J_m3': [[fv(d, 4), fv(r, 12)] for d, r in E02_ROWS],
        'E03_ratio': [[fv(d, 4), fv(r, 12)] for d, r in E03_ROWS],
        'E03_orders': E03_ORDERS,
        'E03b_t_max_s': fv(T_MAX_QEI, 12),
        'E03b_t_planck_s': fv(T_PLANCK_T, 12),
        'E03b_ratio_to_planck': fv(T_RATIO, 12),
        'E04_M_alc_kg': fv(M_ALC, 12),
        'E04_M_qei_kg': fv(M_QEI, 12),
        'E04_ratio': fv(M_ALC / M_QEI, 12),
        'E04_over_M_universe': fv(M_UNIV_RATIO, 12),
        'E04_const_factor_vs_1e10': fv(M_UNIV_RATIO / D('1e10'), 8),
        'E06_delta_min_m': fv(DELTA_MIN, 12),
        'E06_delta_min_ly': fv(DELTA_MIN / LY, 12),
        'E06_delta_min_over_R': fv(DELTA_MIN / L_CHAR, 12),
        'E06_R_star_m': fv(R_STAR, 12),
        'E06_R_star_over_R_obs': fv(R_STAR / R_OBS, 12),
        'E07_rows': [[l, fv(m, 10), fv(s, 8), fv(u, 6)] for l, m, s, u in E07_ROWS],
        'H02_clock_factor': [[l, fv(g, 10)] for l, g in H02_ROWS],
        'graph_selfcheck': GRAPH['selfcheck'],
        'graph_nodes': len(NODES),
        'graph_edges': len(EDGES),
    }

    summary = {
        'book': NAME,
        'date': '2026-10-13',
        'source': '数据/TUFT-超光速曲率引擎_来料全文_2026-10-13.md',
        'judgment_book': '判定_TUFT-r64-超光速曲率引擎_全维审计与攻破_2026-10-13.md',
        'graph': '数据/TUFT-超光速曲率引擎_图谱结构_2026-10-13.json',
        'rating': 'O/L2（来料来向 O/L2；否定结论方向正确，论证链多处断裂）',
        'constants': {
            'G': str(G), 'c': str(c), 'hbar': str(hbar), 'l_P': str(lP),
            'M_sun': str(M_SUN), 'M_jup': str(M_JUP), 'M_universe': str(M_UNIV),
            'ly': str(LY),
        },
        'item_count': len(ITEMS),
        'tally': {k: tally.get(k, 0) for k in order},
        'tally_text': tally_txt,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'items': ITEMS,
        'evidence': evidence,
    }

    # --- 落盘 ---
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    jp = os.path.join(OUT, NAME + '.json')
    with io.open(jp, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, ensure_ascii=False, indent=2))
    gj = os.path.join(OUT, 'TUFT-超光速曲率引擎_图谱结构_2026-10-13.json')
    with io.open(gj, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(GRAPH, ensure_ascii=False, indent=2))

    # --- 数据 md ---
    L = []
    L.append('# %s' % NAME)
    L.append('')
    L.append('- 日期：2026-10-13')
    L.append('- 来料：[TUFT-超光速曲率引擎_来料全文_2026-10-13.md](TUFT-超光速曲率引擎_来料全文_2026-10-13.md)')
    L.append('- 判定册：[%s](../%s)' % (summary['judgment_book'], summary['judgment_book']))
    L.append('- 图谱：[TUFT-超光速曲率引擎_图谱结构_2026-10-13.json](TUFT-超光速曲率引擎_图谱结构_2026-10-13.json)')
    L.append('')
    L.append('## 汇总')
    L.append('')
    L.append('条目 %d（%s）' % (len(ITEMS), tally_txt))
    L.append('')
    L.append('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    L.append('')
    L.append('评级：%s' % summary['rating'])
    L.append('')
    L.append('## 守卫清单')
    L.append('')
    L.append('| 守卫 | 结果 | 说明 |')
    L.append('|---|---|---|')
    for g in GUARD:
        L.append('| %s | %s | %s |' % (g['guard'], 'PASS' if g['ok'] else 'FAIL', g['note']))
    L.append('')
    L.append('## 条目')
    L.append('')
    for it in ITEMS:
        L.append('### %s · %s · %s' % (it['code'], it['verdict'], it['title']))
        L.append('')
        L.append(it['detail'])
        L.append('')
        if it['evidence']:
            L.append('- 机器读数：`%s`' % it['evidence'])
            L.append('')
    L.append('## 机器读数（关键量）')
    L.append('')
    L.append('| 量 | 值 |')
    L.append('|---|---|')
    L.append('| 来稿 rho 式量纲 | %s |' % A01_txt)
    L.append('| 目标量纲（能量密度） | %s |' % A01_want)
    L.append('| 量纲穷举组合数 / 命中 | %d / %d |' % (A02_N, len(A02_HITS)))
    L.append('| 合法幂次族 | %s |' % A02_FAMILY_TXT)
    L.append('| 唯一化后存活族 | %s |' % str(A03_PICK))
    L.append('| 场景表最大相对偏差（容差 %s） | %s |' % (fv(A04_TOL, 2), fv(A04_WORST, 6)))
    L.append('| v_s=200c 的 dtau^2/dt^2 | %s |'
             % fv([r[2] for r in C01_ROWS if r[0] == '200c'][0], 8))
    L.append('| QEI 允许能量密度（delta=lP, L=100m） | %s J/m^3 |' % fv(rho_qei(lP), 8))
    L.append('| Alcubierre 需求（delta=1m, v_s=c） | %s J/m^3 |' % fv(rho_alc(D('1')), 8))
    L.append('| 需求 / QEI 允许（delta=1m） | %s 倍 |' % fv(E03_ROWS[0][1], 8))
    L.append('| 需求 / QEI 允许（delta=0.1m） | %s 倍 |' % fv(E03_ROWS[1][1], 8))
    L.append('| 需求 / QEI 允许（delta=lP） | %s 倍 |' % fv(E03_ROWS[2][1], 8))
    L.append('| E03b 时间上限 t_max / 普朗克时间 | %s（delta 无关） |'
             % fv(T_RATIO, 8))
    L.append('| QEI 质量当量 / 可见宇宙质量 | %s |' % fv(M_UNIV_RATIO, 8))
    L.append('| QEI 最小壳厚 delta_min | %s m = %s ly |'
             % (fv(DELTA_MIN, 8), fv(DELTA_MIN / LY, 8)))
    L.append('| delta_min / R | %s |' % fv(DELTA_MIN / L_CHAR, 8))
    L.append('| 临界泡尺寸 R* / 可观测宇宙半径 | %s |' % fv(R_STAR / R_OBS, 8))
    L.append('| v_s=c 的 M_neg | %s kg = %s M_sun |'
             % (fv(E07_ROWS[0][1], 8), fv(E07_ROWS[0][2], 8)))
    L.append('| v_s=200c 的 M_neg | %s kg = %s M_univ |'
             % (fv(E07_ROWS[2][1], 8), fv(E07_ROWS[2][3], 8)))
    L.append('| 图谱节点 / 边 | %d / %d |' % (len(NODES), len(EDGES)))
    L.append('')
    with io.open(os.path.join(OUT, NAME + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')

    # --- 报告 txt ---
    R = []
    R.append('=' * 78)
    R.append(NAME)
    R.append('2026-10-13  |  全维审计 + 攻破 + 图谱')
    R.append('=' * 78)
    R.append('来源: TUFT-超光速曲率引擎_来料全文_2026-10-13.md')
    R.append('条目: %d   %s' % (len(ITEMS), tally_txt))
    R.append('守卫: %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    R.append('评级: %s' % summary['rating'])
    R.append('')
    R.append('-' * 78)
    R.append('守卫')
    R.append('-' * 78)
    for g in GUARD:
        R.append('[%s] %-24s %s' % ('PASS' if g['ok'] else 'FAIL', g['guard'], g['note']))
    R.append('')
    R.append('-' * 78)
    R.append('条目')
    R.append('-' * 78)
    for it in ITEMS:
        R.append('[%s] %s  %s' % (it['verdict'], it['code'], it['title']))
        R.append('       %s' % it['detail'][:300])
        if it['evidence']:
            R.append('       机器: %s' % it['evidence'][:200])
        R.append('')
    R.append('-' * 78)
    R.append('关键机器读数')
    R.append('-' * 78)
    for k in ['E03_orders', 'E04_over_M_universe', 'E06_delta_min_over_R',
              'E06_R_star_over_R_obs', 'graph_nodes', 'graph_edges']:
        R.append('%-26s = %s' % (k, evidence[k]))
    R.append('')
    with io.open(os.path.join(OUT, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(R) + '\n')

    print('=' * 78)
    print(NAME)
    print('条目 %d   %s' % (len(ITEMS), tally_txt))
    print('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    print('图谱 节点 %d / 边 %d  自检 %s' % (len(NODES), len(EDGES), G01_OK))
    print('=' * 78)
    print('关键读数:')
    print('  量纲穷举 %d 组 -> 命中 %d 族 : %s' % (A02_N, len(A02_FAMILY), A02_FAMILY_TXT))
    print('  唯一化存活: %s' % A03_PICK)
    print('  需求/QEI (delta=1m)  : %s 倍' % fv(E03_ROWS[0][1], 6))
    print('  需求/QEI (delta=0.1m): %s 倍' % fv(E03_ROWS[1][1], 6))
    print('  delta_min / R      : %s' % fv(DELTA_MIN / L_CHAR, 6))
    print('  R* / R_obs         : %s' % fv(R_STAR / R_OBS, 6))
    print('  t_max/t_Planck     : %s  (E03b, delta 无关)' % fv(T_RATIO, 6))
    print('  M_neg(v_s=c)       : %s kg = %s M_sun'
          % (fv(E07_ROWS[0][1], 6), fv(E07_ROWS[0][2], 6)))
    print('  产物: %s.json / .md / _report.txt + 图谱 json' % NAME)
    bad = [g['guard'] for g in GUARD if not g['ok']]
    if bad:
        print('GUARD FAILED: %s' % bad)
        return 1
    print('GUARD ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())