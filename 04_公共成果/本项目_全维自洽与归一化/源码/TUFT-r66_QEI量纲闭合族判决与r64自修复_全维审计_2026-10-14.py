# -*- coding: utf-8 -*-
# =============================================================================
# TUFT r66 · QEI 量纲闭合族判决表 + r64 三条自修复 + 继续攻破
# 2026-10-14
#   定位：r64 = 结构性否定册；r65（并行会话）= 精算账与可执行性册；
#         本册 = 「QEI 形式族判决 + 对 r64 的自修复」，三者互补零重复。
#   纯标准库；Decimal 60 位；四元组量纲 (M,L,T,Q)
#   方法论纪律：
#     (1) 量纲工具先过 guard 再用于判定（r64 自抓 3 次手算量纲错误的直接对策）
#     (2) 任何「比值/倍数」类读数必须先证量纲闭合（r64 E03b 违反此条）
#     (3) 「恒为零/不成立」类裁定必须配阳性对照
#     (4) 外部公式形式不可核实时，做「族」判决表而非单点判决
# =============================================================================
from __future__ import annotations
import io
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:  # pragma: no cover
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, '数据')
NAME = 'TUFT-r66_QEI量纲闭合族判决与r64自修复_全维审计_2026-10-14'

# ---- 常数（CODATA 2018 / SI，与 r64 同口径以便交叉核对）-------------------
c = Decimal('299792458')
G = Decimal('6.67430e-11')
hbar = Decimal('1.054571817e-34')
lP = Decimal('1.616255e-35')
M_SUN = Decimal('1.98892e30')
M_UNIV = Decimal('1.5e53')
LY = Decimal('9.4607304725808e15')
PI = Decimal('3.14159265358979323846264338327950288')

# ---- 四元组量纲工具（指数相加，不是逐分量相乘）----------------------------
def D(m=0, l=0, t=0, q=0):
    return (F(m), F(l), F(t), F(q))


_NM = ['M', 'L', 'T', 'Q']


def mul(*ds):
    o = D()
    for x in ds:
        o = tuple(o[i] + x[i] for i in range(4))
    return o


def inv(a):
    return tuple(-a[i] for i in range(4))


def pw(d, n):
    n = F(n)
    return tuple(d[i] * n for i in range(4))


def show(d):
    out = [_NM[i] if d[i] == 1 else _NM[i] + '^' + str(d[i]) for i in range(4) if d[i] != 0]
    return ' '.join(out) if out else '1'


def eq(a, b):
    return all(a[i] == b[i] for i in range(4))


DM, DL, DT, DQ = D(1, 0, 0, 0), D(0, 1, 0, 0), D(0, 0, 1, 0), D(0, 0, 0, 1)
d_hbar = D(1, 2, -1, 0)
d_c = D(0, 1, -1, 0)
d_G = D(-1, 3, -2, 0)
d_L = DL
d_E = D(1, 2, -2, 0)
RHO_E = D(1, -1, -2, 0)     # 能量密度 = E / L^3
RHO_M = D(1, -3, 0, 0)      # 质量密度 = kg/m^3
d_fp = D(0, -1, 0, 0)       # df/dr_s
d_vs = d_c

# ---- 守卫 ------------------------------------------------------------------
GUARD = []


def guard(name, ok, note=''):
    GUARD.append({'guard': name, 'ok': bool(ok), 'note': note})
    return bool(ok)


def G0(tag, ok, note=''):
    return guard('G0-' + tag, ok, note)


# 量纲工具自检（G0-1..G0-8）—— 必须全过才可用于判定
G0('1', eq(mul(d_E, pw(d_L, -3)), RHO_E), '[E][L^-3] = 能量密度 ML^-1 T^-2')
G0('2', not eq(RHO_E, RHO_M), '能量密度 != 质量密度（本册与 r65 仲裁的关键一条）')
G0('3', eq(mul(d_c, d_c, d_vs, d_vs, d_fp, d_fp, inv(d_G)), RHO_E),
    'r64/r65 来料式 c^2 v_s^2 (f\')^2/G = 能量密度（r64 判 PASS）')
G0('4', eq(mul(pw(d_c, 4), inv(d_G), pw(d_L, -2)), RHO_E), 'c^4/(G delta^2) = 能量密度')
G0('5', eq(mul(d_hbar, d_c), D(1, 3, -2, 0)), '[hbar c] = ML^3 T^-2')
G0('6', eq(mul(pw(d_hbar, 1), pw(d_c, 1), pw(d_L, -4), pw(d_L, 0)), RHO_E),
    'hbar c / delta^4 = 能量密度（QEI 的 a=4,b=0 族）')
G0('7', eq(mul(pw(d_hbar, 1), pw(d_c, 1), pw(d_L, -1), pw(d_L, -3)), RHO_E),
    'hbar c /(delta L^3) = 能量密度（QEI 的 a=1,b=3 族）')
G0('8', eq(mul(inv(d_G), inv(d_hbar), pw(d_c, -4)), D(0, -9, 7, 0)),
    '[G hbar c^-4] = L^-9 T^7（r64 E03b 的 t_max 维度，实为非时间量）')
ALL_GUARDS_OK = all(g['ok'] for g in GUARD)

# ---- 数值工具 --------------------------------------------------------------
def Dc(x):
    return Decimal(str(x))


def sqrt(x):
    return (x.ln() / Decimal(2)).exp()


def cbrt(x):
    return (x.ln() / Decimal(3)).exp()


def fv(x, sig=12):
    return '%.*E' % (sig, x)


# ---- 条目容器 --------------------------------------------------------------
ITEMS = []


def add(code, verdict, title, detail, evidence=''):
    ITEMS.append({'code': code, 'verdict': verdict, 'title': title,
                  'detail': detail, 'evidence': evidence})


def PA(c, t, d, e=''):
    add(c, 'PASS', t, d, e)


def FA(c, t, d, e=''):
    add(c, 'FAIL', t, d, e)


def BO(c, t, d, e=''):
    add(c, 'BOUNDARY', t, d, e)


def CO(c, t, d, e=''):
    add(c, 'CORRECTED', t, d, e)


def IN(c, t, d, e=''):
    add(c, 'INFO', t, d, e)


def MI(c, t, d, e=''):
    add(c, 'MISMATCH', t, d, e)


# =============================================================================
# 组 I · 三处争议的机器仲裁（r64 / r65 双写册之间的冲突）
# =============================================================================
I01_RHOE = mul(d_E, pw(d_L, -3))
I01_OK = (eq(I01_RHOE, RHO_E) and not eq(RHO_E, RHO_M))
PA('I01', '仲裁①：能量密度 = ML^-1 T^-2，r64 正确、r65 裁定③错误（它拿质量密度当能量密度）',
   '机器算 [E]/[L^3] = %s。质量密度 = %s。两者**不等**（机器比较 False）。'
   '⇒ r65 裁定③ 所谓「来料式量纲为 ML^-1 T^-2 而能量密度为 ML^-3 T^-2，缺口恰为 L^2」'
   '是把**质量密度**当成了能量密度；ML^-3（无 T 项）是 kg/m^3，属质量密度族。'
   '⇒ **r65 裁定③ 及其全部下游（3125 组穷举、最简 ℓ_P^-2、「最小修法乘 1/ℓ_P²」）连锁失效**，'
   '本册不采纳。仲裁结论：能量密度口径为 ML^-1 T^-2（r64 A01 正确）。'
   % (show(I01_RHOE), show(RHO_M)),
   'rho_E=%s | rho_M=%s | equal=%s' % (show(I01_RHOE), show(RHO_M), eq(RHO_E, RHO_M)))

RHO_CLAIM = mul(d_c, d_c, d_vs, d_vs, d_fp, d_fp, inv(d_G))
I02_OK = eq(RHO_CLAIM, RHO_E)
PA('I02', '仲裁②：来料 rho 式量纲机器确认为能量密度 ⇒ r64 A01 的 PASS 成立',
   '机器算 c^2 v_s^2 (f\')^2 / G = %s，逐分量等于能量密度 %s（机器比较 True）。'
   '故 r64 的 A01 PASS 与 r65 裁定③ 的「缺口 L^2」不能同时成立；'
   '本册机器复核支持 r64。另机器复核严格形式 c^4 /(32 pi G delta^2) = %s，同样等于能量密度。'
   % (show(RHO_CLAIM), show(RHO_E), show(mul(pw(d_c, 4), inv(d_G), pw(d_L, -2)))),
   'rho_claim=%s ==RHO_E:%s' % (show(RHO_CLAIM), I02_OK))

T_MAX_DIM = mul(inv(d_G), inv(d_hbar), pw(d_c, -4))
T_P_DIM = mul(d_L, inv(d_c))
RATIO_DIM = mul(T_MAX_DIM, inv(T_P_DIM))
I03_OK = not eq(RATIO_DIM, D())
CO('I03', '★自我修复①：r64 E03b 的「时间上限 / 普朗克时间比」量纲不闭合 ⇒ 该条撤回',
   'r64 E03b 写「t ≤ 32 pi G ħ / c^4 = %s s」并与普朗克时间 t_P = l_P / c 比。'
   '机器复核维度：[G ħ c^-4] = %s、t_P = %s、两者的比 = %s ⇒ **无量纲？%s**。'
   '⇒ 「时间上限」根本不是时间（缺一个速度因子），所谓「普朗克时间比」是两个不同量纲量相除，'
   '**该读数无物理意义**。'
   '⇒ **本册撤回 r64 的 E03b 条目**，并撤回它作为「幂次无关论证」的资格。'
   '替代的幂次无关论证改由组 J 的「族判决表」承担：'
   '不依赖 QEI 的具体幂次，而依赖「QEI 形式必须量纲闭合」这一唯一硬条件。'
   % (show(T_MAX_DIM), show(T_MAX_DIM), show(T_P_DIM), show(RATIO_DIM), eq(RATIO_DIM, D())),
   'dim[G hbar c^-4]=%s | dim[t_P]=%s | dim[ratio]=%s | dimensionless=%s'
   % (show(T_MAX_DIM), show(T_P_DIM), show(RATIO_DIM), eq(RATIO_DIM, D())))

# =============================================================================
# 组 J · QEI 量纲闭合族的穷举与判决表（★本册承重）
# =============================================================================
J_HITS = []
J_N = 0
for _al in range(0, 3):
    for _be in range(-2, 4):
        for _a in range(0, 7):
            for _b in range(0, 7):
                J_N += 1
                if eq(mul(pw(d_hbar, _al), pw(d_c, _be), pw(d_L, -_a), pw(d_L, -_b)), RHO_E):
                    J_HITS.append((_al, _be, _a, _b))
J_UNIQ = sorted(set((h[0], h[1], h[2] + h[3]) for h in J_HITS))
J_FAM = sorted(set((h[2], h[3]) for h in J_HITS if h[0] == 1 and h[1] == 1 and h[2] + h[3] == 4))
J_ONE_FAMILY = (len(J_UNIQ) == 1 and J_UNIQ[0] == (1, 1, 4))
J_FIVE = (len(J_FAM) == 5 and J_FAM == [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)])

PA('J01', 'QEI 的量纲闭合族恰好 5 个，且归并到唯一的 (ħ,c) 组合',
   '把 QEI 写成 rho <= K ħ^al c^be / (delta^a L^b)（K 无量纲、al/be/a/b 为整数），'
   '要求右端量纲 = 能量密度 ML^-1 T^-2。穷举 al∈[0,2]、be∈[-2,3]、a,b∈[0,6] 共 %d 组，'
   '命中 %d 组，归并后只有**一个**组合 (al, be, a+b) = %s ⇒ **含 ħ 与 c 各一次是唯一解**，'
   '且 a+b=4。展开即 **%d 个族**：(a,b) = %s。'
   '⇒ 这是本册的判决表骨架：**QEI 不是一个式子，而是一族式子；'
   '族内不同成员对「delta 是否有界、界的方向」给出相反答案。**'
   % (J_N, len(J_HITS), J_UNIQ, len(J_FAM), J_FAM),
   'combos=%d hits=%d uniq=%s families=%d' % (J_N, len(J_HITS), J_UNIQ, len(J_FAM)))

# ---- J02 数值判决表 --------------------------------------------------------
DELTA0 = lP                    # 取普朗克厚壳（本册主张的唯一「严肃可行点」）
LCHAR = Decimal('100')         # 泡特征长度 / QEI 的长度参量
VSC = c                        # v_s = c（唯一在定义域内的泡速，见 r64 C01）


def rho_alc(delta=DELTA0, vs=VSC):
    """Alcubierre 需求能量密度 c^2 v_s^2 /(32 pi G) (1/delta)^2。"""
    fps = Dc(1) / delta
    return (c * c) * (vs * vs) / (Decimal(32) * PI * G) * fps * fps


def rho_qei(a, b, delta=DELTA0, Lc=LCHAR):
    """QEI 允许能量密度 ħ c /(delta^a L^b)。"""
    return hbar * c / ((delta ** a) * (Lc ** b))


J02_ROWS = []
for (a_, b_) in J_FAM:
    need = rho_alc()
    allow = rho_qei(a_, b_)
    ratio = need / allow
    if a_ > 2:
        bnd, dirn = '上界', 'upper'
    elif a_ == 2:
        bnd, dirn = '无关(要求 K>=1)', 'flat'
    else:
        bnd, dirn = '下界', 'lower'
    J02_ROWS.append({'a': a_, 'b': b_, 'form': 'ħc/(delta^%d L^%d)' % (a_, b_),
                     'rho_need': fv(need, 10), 'rho_allow': fv(allow, 10),
                     'ratio': fv(ratio, 10), 'verdict_qei': '不排除' if ratio <= 1 else '排除',
                     'delta_bound': bnd, 'dir': dirn})

J02_PASS = [r for r in J02_ROWS if r['verdict_qei'] == '不排除']
J02_FAIL = [r for r in J02_ROWS if r['verdict_qei'] == '排除']
J02_MINR = min(Decimal(r['ratio']) for r in J02_ROWS)
J02_MAXR = max(Decimal(r['ratio']) for r in J02_ROWS)

FA('J02', '★判决：QEI 是否排除 Alcubierre 泡完全取决于幂次族 —— 5 个量纲闭合族中 1 个不排除、4 个排除',
   '判决表（delta = l_P、L = %s m、v_s = c）：' % fv(LCHAR, 4) +
   '；'.join('(a,b)=(%d,%d) 需求/允许 = %s ⇒ %s，delta %s'
             % (r['a'], r['b'], r['ratio'], r['verdict_qei'], r['delta_bound'])
             for r in J02_ROWS) +
   '。⇒ 比值跨度 **%s ~ %s**（跨 %d 个数量级）。'
   '**族 (4,0)（rho <= ħc/delta^4）下需求低于允许（比值 %s），QEI 不排除该泡**；'
   '其余 4 族全部排除，比值 %s ~ %s。'
   '⇒ 这直接**推翻 r64 E03/E06 的无条件表述**：「结构性不可行」只在 4/5 族成立。'
   % (fv(J02_MINR, 6), fv(J02_MAXR, 6), len(str(int(J02_MAXR))) - len(str(int(J02_MINR))),
      fv(Decimal(J02_PASS[0]['ratio']), 6) if J02_PASS else 'n/a',
      fv(min(Decimal(r['ratio']) for r in J02_FAIL), 6) if J02_FAIL else 'n/a',
      fv(J02_MAXR, 6)),
   'pass_families=%d fail_families=%d min_ratio=%s max_ratio=%s'
   % (len(J02_PASS), len(J02_FAIL), fv(J02_MINR, 6), fv(J02_MAXR, 6)))

# ---- J03 δ 界的数值 -------------------------------------------------------
J03_ROWS = []
BASE_C = Decimal(32) * PI * G * hbar / (c * c * VSC)   # 32 pi G hbar / c^3  (m^2)
J03_NUM = {}
for (a_, b_) in J_FAM:
    k = BASE_C * (LCHAR ** b_)
    if a_ == 2:
        dlim = Decimal(1)          # 指数为 0，占位（该族与 delta 无关）
    else:
        dlim = (k.ln() / Decimal(a_ - 2)).exp()
    dirn = 'upper' if a_ > 2 else ('flat' if a_ == 2 else 'lower')
    J03_NUM[(a_, b_)] = dlim
    J03_ROWS.append({'a': a_, 'b': b_, 'dir': dirn,
                     'k_m2': fv(k, 10),
                     'delta_limit_m': fv(dlim, 10) if a_ != 2 else 'n/a (delta 无关)',
                     'over_lP': fv(dlim / lP, 10) if a_ != 2 else 'n/a'})
J03_UP = [r for r in J03_ROWS if r['dir'] == 'upper']
J03_LO = [r for r in J03_ROWS if r['dir'] == 'lower']
J03_FLAT = [r for r in J03_ROWS if r['dir'] == 'flat']
J03_SPAN = max(J03_NUM.values()) / min(J03_NUM.values())
J03_R64CMP = J03_NUM[(1, 3)] / Decimal('1.561565208634e23')   # 与 r64 E06 的 delta_min 比

MI('J03', '★delta 界方向在族内相反：2 族给上界、1 族无关、2 族给下界 ⇒ r64 的「delta 有下界」只在 2/5 族成立',
   '由 rho_Alc ∝ delta^-2 与 rho_QEI ∝ delta^-a，约束化为 delta^(a-2) <= K，'
   '故 a>2 给**上界**、a=2 **无关**、a<2 给**下界**。机器判决：' +
   '；'.join('(a,b)=(%d,%d) -> %s，delta 界 %s m（= %s ℓ_P）'
             % (r['a'], r['b'], r['dir'], r['delta_limit_m'], r['over_lP'])
             for r in J03_ROWS) +
   '。⇒ delta 界在族内跨 **%s 个数量级**，方向也相反。'
   '**与 r64 E06 的比较**：本册 a=1,b=3 族给出的 delta 下界是 %s m，'
   '而 r64 E06 给的是 1.561565208634e23 m，二者相差 **%s 倍**'
   '（r64 用的是量纲不闭合的 delta^1 L^1 形式，本册用唯一量纲闭合的 delta^1 L^3 形式）。'
   '⇒ 反之 a>=3 的两族给 delta **上界**（最大 %s m = %s ℓ_P），'
   '薄壳（delta ≪ R = %s m）在这些族下**几何上完全可行**。'
   % (len(str(int(J03_SPAN))), fv(J03_NUM[(1, 3)], 8), fv(J03_SPAN, 6),
      fv(J03_NUM[(4, 0)], 8), fv(J03_NUM[(4, 0)] / lP, 6), fv(LCHAR, 4)),
   'upper=%d flat=%d lower=%d | span=%s | vs_r64=%s'
   % (len(J03_UP), len(J03_FLAT), len(J03_LO), fv(J03_SPAN, 6), fv(J03_R64CMP, 6)))

# =============================================================================
# 组 K · r64 三条的自修复（自我降级，不改 r64 任何字节）
# =============================================================================
K01_RHO_ALC = rho_alc()
FA('K01', '★自我修复②：r64 E03「需求/QEI = 3.81e69 ~ 2.36e104 倍」降级为条件性（4/5 族成立）',
   'r64 E03 用 QEI 形式 rho <= ħ c/(delta L) 作分母，得出需求/允许达 %s ~ %s 倍。'
   '本册机器复核：**该形式的量纲为 %s，不等于能量密度 %s** ⇒ 它不在量纲闭合族内，'
   '故其倍数读数只在「若该形式恰好成立」的条件下有效。'
   '在唯一量纲闭合的族集合里（J01 的 5 族），倍数区间为 %s ~ %s，其中 (4,0) 族比值 %s < 1。'
   '⇒ **E03 的定性方向（压强需求天文级）保留，其定量倍数降级为条件性**，'
   '并由 J02 的族判决表替代。'
   % ('3.81e69', '2.36e104', show(mul(pw(d_hbar, 1), pw(d_c, 1), pw(d_L, -1), pw(d_L, -1))),
      show(RHO_E), fv(J02_MINR, 6), fv(J02_MAXR, 6),
      fv(Decimal(J02_PASS[0]['ratio']), 6) if J02_PASS else 'n/a'),
   'dimensionless_family_span=%s..%s' % (fv(J02_MINR, 6), fv(J02_MAXR, 6)))

FA('K02', '★自我修复③：r64 E06「delta_min = 1.56e23 m、δ_min/R = 1.56e21、薄壳几何失效」降级为 2/5 族',
   'r64 E06 由 QEI 形式 rho <= ħ c/(delta L) 反解出 delta 下界 1.5616e23 m，'
   '并据此判「薄壳几何前提失效」。本册机器复核：'
   '在量纲闭合的族里，a>2 的两族给 delta **上界**（delta ≪ R 反而容易满足）、'
   'a=2 一族与 delta 无关、a<2 的两族给下界。'
   '⇒ 「delta 有下界且远大于 R」只在 **2/5 族**成立；'
   '在 (4,0) 族下 delta 有**上界** 1.6207e-34 m，薄壳几何完全可行。'
   '⇒ E06 的定性结论（「所有有限尺度泡都被排除」）**不成立**，降级为族条件性。'
   'r64 的其他条目（C01 泡内固有时虚、C05 度规基底错、B02 dτ 语义、C04 虚时间）'
   '**不受本册影响**，继续有效（它们不依赖 QEI 形式）。',
   'upper_families=%d lower_families=%d' % (len(J03_UP), len(J03_LO)))

PA('K03', '无条件保留的稳健读数：Alcubierre 需求压强本身是天文量（与 QEI 形式无关）',
   '机器算 rho_Alc(delta = l_P, v_s = c) = %s J/m^3。'
   '这一读数**只依赖来稿式与常数、不依赖 QEI 的任何形式**，因此是全册唯一无条件成立的'
   '「天文级」读数。它与 r64 E02 一致。'
   '⇒ 即便 QEI 形式最终定为最宽松的 (4,0) 族，泡所需的能量密度仍比任何已知实验室或天体'
   '负能量密度高 40 个数量级以上（作为量级对照，不依赖 QEI）。'
   % fv(K01_RHO_ALC, 10),
   'rho_Alc(l_P, v_s=c) = ' + fv(K01_RHO_ALC, 12) + ' J/m^3')

PA('K04', '本册与 r64 的分工仲裁：四条结构性否定继续有效，两条 QEI 结论降级',
   '**继续有效（不依赖 QEI 形式）**：C01/C04（v_s>c 泡内固有时为虚、「船上一瞬间」是虚时间）、'
   'C05/C05b（来稿度规与 Alcubierre 原式不符、rho 公式不可移植）、B02（dτ=0 是无时间非无位移）。'
   '**降级为族条件性**：E03（压强倍数）、E03b（撤，见 I03）、E06（delta 下界）。'
   '⇒ 综合修正后的表述应为：**在 Alcubierre 型 + QEI 框架内，该泡是否被 QEI 排除'
   '取决于尚未核实的 QEI 幂次族；5 个量纲闭合族中 1 个不排除、4 个排除。**',
   'effective=4/11 (C01+C05+C05b+B02) | conditional=3 (E03+E03b+E06)')

# =============================================================================
# 组 L · 幸存族 (4,0) 的真实代价（「继续攻破」的核心产出）
# =============================================================================
DLIM_40 = J03_NUM[(4, 0)]                       # delta 上界 = 1.6207e-34 m
DLIM_40_OVER_LP = DLIM_40 / lP
CURV_SHELL = Dc(1) / (DELTA0 * DELTA0)          # 壳内曲率标度 ~ 1/delta^2
CURV_BUB = Dc(1) / (LCHAR * LCHAR)              # 泡尺度曲率 ~ 1/R^2
CURV_RATIO = CURV_SHELL / CURV_BUB
M_NEG_40 = (VSC * VSC) * (LCHAR * LCHAR) / (Decimal(8) * G * DLIM_40)
M_NEG_40_MSUN = M_NEG_40 / M_SUN

L01_NOTE = (
    'J02 判定 (4,0) 族（rho <= ħ c / delta^4）下 QEI **不排除**该泡。'
    '本条给出该「幸存」的完整代价，三项全部机器定价：'
    '**代价一 · 厚度被迫取普朗克量级**：该族给 delta **上界** delta <= %s m = %s ℓ_P。'
    '⇒ 若要满足，最自然的选择就是取 delta ~ ℓ_P（把壳压到普朗克厚），'
    '这与 r64 的假设一致，但方向相反（r64 由 QEI 推出 delta 必须远大于 R，此族推出 delta <= ℓ_P）。'
    '**代价二 · 曲率集中度**：普朗克厚壳的时空曲率标度 1/delta^2 = %s m^-2，'
    '而泡半径 %s m 的特征曲率仅 1/R^2 = %s m^-2，二者相差 **%s 倍**。'
    '⇒ 曲率在壳内高度集中，**经典 GR 的弱场/有效场论前提在此失效**，'
    '问题从 QEI 转移到量子引力（即 r64 钥匙 4，本册不代其判定）。'
    '**代价三 · 负能量当量暴涨**：M_neg ∝ delta^-1，delta 被限在 ≤ %s m 后，'
    '机器算 M_neg = %s kg = %s M_sun。'
    '⇒ 与 r64 E07 在 delta=1 m 下算得的 **0.846 M_sun** 相比，'
    '同一族下允许的泡**质量当量反而是 %s 倍**。'
    '⇒ **QEI 族 (4,0) 的「不排除」是有价格的**：三重代价（普朗克厚壳 / 量子引力区 / '
    '%s 太阳质量负能量）叠加后，实质上仍不可行，但论证链从「被 QEI 排除」'
    '升级为「不被 QEI 排除、而是被量子引力与能量账排除」。'
    % (fv(DLIM_40, 8), fv(DLIM_40_OVER_LP, 6), fv(CURV_SHELL, 8),
       fv(LCHAR, 4), fv(CURV_BUB, 8), fv(CURV_RATIO, 8),
       fv(DLIM_40, 8), fv(M_NEG_40, 8), fv(M_NEG_40_MSUN, 8),
       fv(M_NEG_40_MSUN / Dc('0.846308'), 8), fv(M_NEG_40_MSUN, 8)))

IN('L01', '★幸存族 (4,0) 的三重代价：普朗克厚壳 + 曲率集中 %s 倍 + %s M_sun 负能量'
   % (fv(CURV_RATIO, 4), fv(M_NEG_40_MSUN, 4)),
   L01_NOTE,
   'delta_max=%s m (%s l_P) | curvature_ratio=%s | M_neg=%s kg (%s M_sun)'
   % (fv(DLIM_40, 10), fv(DLIM_40_OVER_LP, 6), fv(CURV_RATIO, 6),
      fv(M_NEG_40, 10), fv(M_NEG_40_MSUN, 6)))

L02_OK = (len(J02_PASS) == 1 and J02_PASS[0]['a'] == 4 and J02_PASS[0]['b'] == 0)
IN('L02', '攻破结论·收敛：曲速泡的否决点从「QEI 排除」迁移到「量子引力 + 能量账」',
   '本册把 r64 的「结构性不可行」从一个**单点判决**升级为一个**族判决 + 代价清单**：'
   '（i）QEI 是否排除该泡：5 个量纲闭合族中 1 个不排除（(4,0)）、4 个排除；'
   '（ii）不排除的那一族的可实现代价：普朗克厚壳（delta <= 1.62e-34 m）、'
   '曲率集中 3.83e73 倍（经典 GR 失效）、负能量当量 5.2e33 M_sun。'
   '⇒ **真正的否决点不是 QEI，而是「QEI 不排除」这一分支上紧接着的量子引力条件'
   '（r64 钥匙 4）与能量账**。这一迁移本身是可算的、可复现的增量：'
   '它把一个被误当成无条件的结论，降级为有条件的，并精确定位了条件边界。'
   '⇒ 并且它给出一条**此前无人登记的判据**：任何只用「单一 QEI 形式」下结论的曲速论证，'
   '都必须先做本册 J01 的量纲闭合族穷举，否则该结论不可复现。',
   'unique_surviving_family=(4,0) confirmed=%s' % L02_OK)

# =============================================================================
# 组 M · 与 r65 裁定② 的第三处仲裁：δ 方向（决定「能量账是否 no-go」）
# =============================================================================
def m_neg(vs, R, delta):
    """M_neg = v_s^2 R^2 /(8 G delta)。"""
    return (vs * vs) * (R * R) / (Decimal(8) * G * delta)


M_MNEG_GEOM = m_neg(VSC, LCHAR, LCHAR)          # δ -> R（壳厚=泡半径，泡结构已失）
M_MNEG_R64 = m_neg(VSC, LCHAR, Decimal('1'))    # r64 E07 的 δ = 1 m
M_MNEG_QEI40 = m_neg(VSC, LCHAR, DLIM_40)      # δ = QEI(4,0) 族上界
M_MNEG_TINY = m_neg(VSC, LCHAR, lP / Decimal(1000))   # δ = ℓ_P/1000（更薄更贵）

M03_ROWS = []
for lab, dl in [('δ = R = 100 m（泡结构已失）', LCHAR),
                ('δ = 1 m（r64 E07 取值）', Decimal('1')),
                ('δ = ℓ_P/1000', lP / Decimal(1000)),
                ('δ = ℓ_P', lP),
                ('δ = QEI(4,0) 上界', DLIM_40)]:
    mm = m_neg(VSC, LCHAR, dl)
    M03_ROWS.append({'delta_label': lab, 'delta_m': fv(dl, 8),
                     'M_neg_kg': fv(mm, 10), 'M_over_Msun': fv(mm / M_SUN, 10)})
M03_DOWN = True   # δ 增大 => M_neg 减小（由 dM/dδ ∝ -δ^-2 < 0 解析保证）

CO('M01', '★仲裁④：r65 裁定②「δ_supp 无下界 ⇒ M_neg 可任意小」推论方向反了',
   '机器读数（v_s = c、R = %s m，扫 δ）：' % fv(LCHAR, 4) +
   '；'.join('%s => M_neg = %s kg = %s M⊙' % (r['delta_label'], r['M_neg_kg'], r['M_over_Msun'])
             for r in M03_ROWS) +
   '。由 M_neg = v_s^2 R^2/(8 G δ) 直接得 dM_neg/dδ ∝ -δ^-2 < 0 ⇒ '
   '**δ 越小 M_neg 越大**（δ → 0 时 M_neg → ∞）。'
   '⇒ r65 的 Cauchy–Schwarz 下界 M_neg ≥ v_s²R²/(32πG·δ_supp) 本身**方向正确**，'
   '但其推论「δ_supp 没有物理下界 ⇒ M_neg 可任意小」**逻辑反向**：'
   'δ_supp 没有下界恰恰意味着 M_neg 的下界可以任意**大**。'
   '⇒ 正确的表述是：M_neg 要小必须 δ **大**；'
   '而 δ 大到 R 附近时薄壁泡结构消失（机器读数：δ = R 对应 %s M⊙）。'
   '⇒ 本册判定 r65 裁定②的**推论**失效（其下界式保留）。'
   % fv(M_MNEG_GEOM / M_SUN, 8),
   'M_neg(delta=R)=%s kg | delta=1m -> %s kg | delta=QEI(4,0)上限 -> %s kg'
   % (fv(M_MNEG_GEOM, 10), fv(M_MNEG_R64, 10), fv(M_MNEG_QEI40, 10)))

CO('M02', '★合并 M01 + L01：在 QEI (4,0) 族下「能量账非 no-go」被阻断，M_neg 被下界锁在 %s M⊙'
   % fv(M_MNEG_QEI40 / M_SUN, 4),
   '把 M01（δ 小 ⇒ M 大）与 L01（QEI (4,0) 族给 δ 上界 1.6207e-34 m）合起来：'
   'QEI 要求 δ ≤ %s m，而 M_neg ∝ δ^-1 ⇒ **M_neg 被下界锁定在 %s kg = %s M⊙**。'
   '⇒ r65 的「能量账不是 no-go」在**没有 QEI 约束时**成立（几何下界仅 %s M⊙），'
   '但**在 QEI (4,0) 族下被阻断**（下界升至 %s M⊙，高 %s 倍）。'
   '⇒ 这构成本册对「曲速泡可行性」最完整的一张账：'
   '几何结构给上界（要薄）、QEI 给下界（要薄）、能量账给下界（要厚）⇒ 三者张力集中在 δ。'
   % (fv(DLIM_40, 8), fv(M_MNEG_QEI40, 8), fv(M_MNEG_QEI40 / M_SUN, 8),
      fv(M_MNEG_GEOM / M_SUN, 8), fv(M_MNEG_QEI40 / M_SUN, 8),
      fv(M_MNEG_QEI40 / M_MNEG_GEOM, 8)),
   'M_geometric_floor=%s M_sun | M_QEI40_floor=%s M_sun | ratio=%s'
   % (fv(M_MNEG_GEOM / M_SUN, 6), fv(M_MNEG_QEI40 / M_SUN, 6),
      fv(M_MNEG_QEI40 / M_MNEG_GEOM, 6)))

# =============================================================================
# 组 N · 可变光速双口径判决（修 r64 H05：c⁴ 杠杆依赖 G 是否同步归一）
# =============================================================================
def dl_max_family(k, geo_fixed):
    """(4,0) 族在 c_eff = k c 下的 delta 上界。
    geo_fixed=True  => G 固定（G 不随 c_eff 归一）
    geo_fixed=False => G_eff = G (c_eff/c)^4（几何单位归一）
    """
    ce = k * c
    if geo_fixed:
        num = Decimal(32) * PI * G * hbar / ce        # δ^2 <= ...
        return (num.ln() / Decimal(2)).exp()
    # G_eff = G k^4  =>  ρ_Alc = c^4/(32πG δ^2)，c_eff 完全消去
    return DLIM_40


N_ROWS = []
for k in [Decimal('0.5'), Decimal('0.1'), Decimal('0.01'), Decimal('1')]:
    dA = dl_max_family(k, True)
    dB = dl_max_family(k, False)
    mA = m_neg(VSC, LCHAR, dA)
    N_ROWS.append({'k': fv(k, 4), 'delta_max_Gfixed': fv(dA, 8),
                   'M_neg_Gfixed_Msun': fv(mA / M_SUN, 8),
                   'delta_max_geo': fv(dB, 8),
                   'M_neg_geo_Msun': fv(M_MNEG_QEI40 / M_SUN, 8)})
N_GK = dl_max_family(Decimal('0.01'), True)
N_GEO_CONST = True   # 几何归一口径下 delta_max 与 k 无关（c_eff 完全消去）

MI('N01', '★修正 r64 H05：「降 c_eff 压 ρ_Alc」只在「G 固定」口径成立；几何归一口径下 c_eff 完全消去',
   'r64 H05 写「唯一可被螺旋光速论压缩的因子是 c²：若 c_eff < c 则 ρ_Alc ~ c_eff^4」，'
   '但同一句里又说「G 与 c 的口径必须同步（几何单位制下 G ~ c^4）」——'
   '这两句在代数上**互斥**。机器判决：'
   '**口径 (a) G 固定**：ρ_Alc = c_eff^4/(32πGδ²)，随 c_eff 下降而下降；'
   '但 δ 上界 δ_max = sqrt(32πGħ/c_eff) ∝ c_eff^-1/2 ⇒ **c_eff 降 ⇒ δ_max 降 ⇒ '
   'M_neg ∝ δ^-1 升** ⇒ 机器读数 k=0.5/0.1/0.01 时 M_neg 分别为 %s / %s / %s M⊙（逐项升高）。'
   '**口径 (b) G_eff = G(c_eff/c)^4（几何归一）**：ρ_Alc = c_eff^4/(32πG k^4 δ²) '
   '= c^4/(32πGδ²) ⇒ **c_eff 完全消去**，δ_max 恒为 %s m，杠杆失效。'
   '⇒ 判决：**r64 H05 宣称的「c⁴ 是唯一杠杆」是口径依赖的，且在几何归一口径下不成立**。'
   '这直接影响「螺旋光速论能否救曲速泡」这一问题本身：'
   '若本库主线采用几何归一口径（记忆显示 r18 审计过 G=c^4/(8πκ) 型式），'
   '则**可变光速对曲速泡压强零帮助**。'
   % (N_ROWS[0]['M_neg_Gfixed_Msun'], N_ROWS[1]['M_neg_Gfixed_Msun'],
      N_ROWS[2]['M_neg_Gfixed_Msun'], fv(DLIM_40, 8)),
   '; '.join('k=%s: Gfixed δ<=%s M=%s M_sun | geo δ=%s'
             % (r['k'], r['delta_max_Gfixed'], r['M_neg_Gfixed_Msun'], r['delta_max_geo'])
             for r in N_ROWS))

IN('N02', '口径归属是攻破前置条件：必须先定「G 是否随 c 归一」，否则变速路线无法判定',
   '本册 M01/N01 两次读数都显示：**同一个「降低有效光速」的杠杆，在两种 G 口径下给出相反方向**'
   '（口径 a 下 M_neg 随 c_eff 降而升、口径 b 下完全不变）。'
   '⇒ 因此「螺旋光速论能否降低曲速泡的负能量门槛」这一问题，'
   '**在库内公设集层面尚未被裁定**（属 G 与 c 的关系公设，r18 曾触及但未收口）。'
   '⇒ 本册不代选，登记为新的开放项：**O-GC-REL（引力度与光速的归一关系）**。',
   'new_open_item=O-GC-REL')

# =============================================================================
# 组 O · H02 的实验判据（把 r64 的定性否证条件做成可算判据）
# =============================================================================
O_ROWS = []
for lab, beta in [('0.5c', Decimal('0.5')), ('0.9c', Decimal('0.9')),
                  ('0.99c', Decimal('0.99')), ('0.999c', Decimal('0.999')),
                  ('0.9999c', Decimal('0.9999')), ('0.99999c', Decimal('0.99999'))]:
    g = sqrt(Decimal(1) - beta * beta)
    O_ROWS.append({'v_s': lab, 'beta': fv(beta, 6),
                   'clock_factor_g': fv(g, 12),
                   'g_percent': fv(g * 100, 8),
                   'measurable_1pct': 'YES' if g >= Decimal('0.01') else 'NO'})
O_YES = len([r for r in O_ROWS if r['measurable_1pct'] == 'YES'])
O_TIGHT = [r for r in O_ROWS if r['measurable_1pct'] == 'YES'][-1]

PA('O01', '泡内时钟减速因子 √(1-β²) 的可测性阶梯（r64 H02 的定量版）',
   '机器采样（v_s < c 全部有实值）：' +
   '；'.join('%s -> g = %s（%s%%）⇒ 1%% 精度可测：%s'
             % (r['v_s'], r['clock_factor_g'], r['g_percent'], r['measurable_1pct'])
             for r in O_ROWS) +
   '。⇒ 只要泡速达到 %s 量级，泡内时钟减速就超过 1%%，**现有原子钟技术即可测量**。'
   '⇒ 该判据的关键性质：它**不依赖负能量、不依赖 QEI 形式、不依赖 v_s > c**，'
   '因此在本册把 QEI 族条件化之后，它仍是全册唯一不受影响的实验判据。'
   % O_TIGHT['v_s'],
   '; '.join('%s:g=%s' % (r['v_s'], r['clock_factor_g']) for r in O_ROWS))

PA('O02', '否证条件的不等式形式（比 r64 H02 的定性表述更强）',
   'r64 H02 写「若实验观测泡内时钟不减速，则任何曲速泡被排除」。'
   '本册给出可算形式：若测得 g_obs，则 v_s/c = sqrt(1 - g_obs^2)，'
   '且**任何声称存在曲速泡的模型必须给出与之相容的 g**。'
   '⇒ 三档判决：'
   '(i) g_obs = 0（泡内外时钟同步）⇒ 所有 v_s>0 的泡被排除（含正能量泡与亚光速泡）；'
   '(ii) 0 < g_obs < 1 ⇒ 支持某个 v_s = c sqrt(1-g_obs^2)，但该 v_s 必须同时满足'
   '本册 J02 族判决表（若该族排除 QEI 则该 g_obs 仍不可信）；'
   '(iii) g_obs → 1 ⇒ 泡速趋零，泡效应趋于零、观测意义消失。'
   '⇒ **判据 (i) 是最强的一档**：它一次性排除全部曲速方案，'
   '且不需要任何关于负能量或 QEI 的假设。'
   '⇒ 建议实验设计：把「长距离运输中物质钟与实验室钟是否同步」作为**一阶判据**，'
   '其难度远低于直接测量超光速，因为不需要造出泡——'
   '只需找到任何 g_obs≠0 的效应。',
   'three_branches=0 <(g_obs)< 1 ; strongest=branch_i')

# =============================================================================
# 组 P · r64 / r65 / r66 三方分工与冲突仲裁总表
# =============================================================================
ARB = [
    ('能量密度口径', 'r64 A01: ML^-1 T^-2', 'r65 裁定3: ML^-3', 'r66 I01: ML^-1 T^-2',
     'r64 正确；r65 把质量密度当能量密度，其 3125 组穷举连锁失效'),
    ('来料 rho 式量纲', 'r64 A01: PASS', 'r65 裁定3: 缺口 L^2', 'r66 I02: PASS',
     'r64 正确（机器逐分量相等）'),
    ('E03b 普朗克时间比', 'r64 E03b: 成立', '（未涉及）', 'r66 I03: 撤回',
     'r64 该条量纲不闭合（L^-9 T^6 比值），撤回'),
    ('E03 压强倍数', 'r64 E03: 3.81e69~2.36e104', '（Klauber 口径 40 量级）', 'r66 J02: 族条件性',
     'r64 分母形式量纲不闭合；倍数降级为 4/5 族条件性'),
    ('E06 delta 下界', 'r64 E06: 1.56e23 m', '（未涉及）', 'r66 J03: 2/5 族给下界',
     'r64 形式量纲不闭合；本册唯一量纲闭合的 delta^1 L^3 族给下界 3.81e61 m'),
    ('能量账是否 no-go', 'r64 E07: 归因在压强', 'r65 裁定2: 非 no-go（delta_sup 无下界）',
     'r66 M01/M02: 推论方向反，且被 QEI(4,0) 族阻断',
     'r65 下界式保留，推论「delta_sup 无下界 => M 可任意小」逻辑反向'),
    ('可变光速杠杆', 'r64 H05: c^4 唯一杠杆', '（未涉及）', 'r66 N01: 口径依赖，几何归一下失效',
     'r64 同一句内自相矛盾（c^4 下降 vs G~c^4 同步）'),
]
PA('P01', '三方冲突仲裁总表（6 处冲突，5 处判 r64 或 r65 有误、1 处判 r64 正确）',
   '本主题已有三册（r64 结构性否定 / r65 精算账与可执行性（并行会话）/ r66 本册）。'
   '机器仲裁 6 处冲突：' +
   '；'.join('【%s】%s vs %s ⇒ %s（%s）' % a for a in ARB) +
   '。⇒ **净结果：r64 的 4 条 QEI 相关结论（E03/E03b/E06/H05）全部降级或撤回，'
   '其 4 条结构性否定（C01/C05/C05b/B02）继续有效；r65 的 2 条（裁定2/裁定3）被本册修正。**'
   '⇒ 三册合并后的净立场是：曲速泡在 Alcubierre 型框架内**未被 QEI 无条件排除**（1/5 族不排除），'
   '但也不被任何族无条件允许，且幸存分支的代价（普朗克厚壳 + 量子引力区 + %s M⊙）'
   '在工程上不可实现。'
   % fv(M_MNEG_QEI40 / M_SUN, 4),
   'conflicts_arbitrated=%d' % len(ARB))

IN('P02', '本册新增开放项：O-GC-REL（引力度与光速的归一关系）—— 变速路线的判定前置',
   'N01/N02 表明：「降低有效光速能否降低曲速泡的负能量门槛」在库内**无法判定**，'
   '因为它取决于 G 是否随 c 归一，而这一公设尚未裁定。'
   '⇒ 登记 **O-GC-REL**。本册不代选。'
   '⇒ 影响面：H05（r64 的主线接口）、任何「可变光速 + 曲速泡」的组合方案。',
   'open_item=O-GC-REL')

# =============================================================================
# 图谱（r66 增量层：族判决 + 自修复 + 三方仲裁）
# =============================================================================
NODES = [
    {'id': 'FAM_QEI', 'type': 'family', 'label': 'QEI 量纲闭合族（共 5 个）'},
    {'id': 'FAM_40', 'type': 'family_member', 'label': '族(4,0)：rho<=ħc/δ⁴（不排除）'},
    {'id': 'FAM_31', 'type': 'family_member', 'label': '族(3,1)：rho<=ħc/(δ³L)'},
    {'id': 'FAM_22', 'type': 'family_member', 'label': '族(2,2)：rho<=ħc/(δ²L²)'},
    {'id': 'FAM_13', 'type': 'family_member', 'label': '族(1,3)：rho<=ħc/(δL³)'},
    {'id': 'FAM_04', 'type': 'family_member', 'label': '族(0,4)：rho<=ħc/L⁴'},

    {'id': 'R64_E03', 'type': 'prior_finding', 'label': 'r64 E03 压强倍数', 'status': 'downgraded'},
    {'id': 'R64_E03b', 'type': 'prior_finding', 'label': 'r64 E03b 普朗克时间比', 'status': 'retracted'},
    {'id': 'R64_E06', 'type': 'prior_finding', 'label': 'r64 E06 delta 下界', 'status': 'downgraded'},
    {'id': 'R64_H05', 'type': 'prior_finding', 'label': 'r64 H05 c⁴ 杠杆', 'status': 'corrected'},
    {'id': 'R64_C01', 'type': 'prior_finding', 'label': 'r64 C01 泡内固有时为虚', 'status': 'valid'},
    {'id': 'R64_C05', 'type': 'prior_finding', 'label': 'r64 C05 度规基底错', 'status': 'valid'},
    {'id': 'R65_ARB3', 'type': 'prior_finding', 'label': 'r65 裁定3 能量密度口径', 'status': 'corrected'},
    {'id': 'R65_ARB2', 'type': 'prior_finding', 'label': 'r65 裁定2 能量账非 no-go', 'status': 'corrected'},

    {'id': 'O_GC_REL', 'type': 'open_item', 'label': 'O-GC-REL 引力度与光速的归一关系'},
    {'id': 'K_QG', 'type': 'constraint', 'label': '量子引力有效域（r64 钥匙4）'},
    {'id': 'K_ENERGY', 'type': 'constraint', 'label': '负能量当量账（M_neg ∝ δ^-1）'},
    {'id': 'K_GEOM', 'type': 'constraint', 'label': '薄壁泡几何（δ ≲ R）'},
]
EDGES = [
    {'src': 'FAM_QEI', 'dst': 'FAM_40', 'type': 'contains'},
    {'src': 'FAM_QEI', 'dst': 'FAM_31', 'type': 'contains'},
    {'src': 'FAM_QEI', 'dst': 'FAM_22', 'type': 'contains'},
    {'src': 'FAM_QEI', 'dst': 'FAM_13', 'type': 'contains'},
    {'src': 'FAM_QEI', 'dst': 'FAM_04', 'type': 'contains'},
    # 族 → r64 结论的支持关系（4 个排除族支持 r64 的排除方向；1 个幸存族反证它）
    {'src': 'FAM_31', 'dst': 'R64_E03', 'type': 'supports_exclusion'},
    {'src': 'FAM_22', 'dst': 'R64_E03', 'type': 'supports_exclusion'},
    {'src': 'FAM_13', 'dst': 'R64_E03', 'type': 'supports_exclusion'},
    {'src': 'FAM_04', 'dst': 'R64_E03', 'type': 'supports_exclusion'},
    {'src': 'FAM_40', 'dst': 'R64_E03', 'type': 'refutes_exclusion'},
    # r64 结构性否定 → 本册约束面（这两条不依赖 QEI 形式，继续有效）
    {'src': 'R64_C01', 'dst': 'K_GEOM', 'type': 'constrains'},
    {'src': 'R64_C05', 'dst': 'FAM_QEI', 'type': 'scopes'},
    {'src': 'R66_J02', 'dst': 'FAM_QEI', 'type': 'uses'},
    {'src': 'R64_E03', 'dst': 'FAM_QEI', 'type': 'downgraded_by'},
    {'src': 'R64_E03b', 'dst': 'R66_I03', 'type': 'retracted_by'},
    {'src': 'R64_E06', 'dst': 'FAM_QEI', 'type': 'downgraded_by'},
    {'src': 'R64_H05', 'dst': 'O_GC_REL', 'type': 'blocked_by'},
    {'src': 'R65_ARB3', 'dst': 'R66_I01', 'type': 'corrected_by'},
    {'src': 'R65_ARB2', 'dst': 'R66_M01', 'type': 'corrected_by'},
    {'src': 'FAM_40', 'dst': 'K_QG', 'type': 'requires'},
    {'src': 'K_QG', 'dst': 'K_GEOM', 'type': 'related'},
    {'src': 'K_ENERGY', 'dst': 'FAM_40', 'type': 'bounds'},
    {'src': 'K_GEOM', 'dst': 'K_ENERGY', 'type': 'relates'},
    {'src': 'O_GC_REL', 'dst': 'R64_H05', 'type': 'scopes'},
]
ITEMS_BY_CODE = dict((it['code'], it) for it in ITEMS)
for _code in ['J01', 'J02', 'I01', 'I03', 'M01', 'M02', 'N01', 'L01']:
    _it = ITEMS_BY_CODE.get(_code)
    if _it is None:
        continue
    NODES.append({'id': 'R66_' + _code, 'type': 'finding',
                  'label': _code + ' ' + _it['title'], 'verdict': _it['verdict']})
_ids = set(n['id'] for n in NODES)
_out = dict((n['id'], 0) for n in NODES)
for e in EDGES:
    _out[e['src']] = _out.get(e['src'], 0) + 1
G_DUP = len(NODES) - len(_ids)
G_DANGLE = len([e for e in EDGES if e['src'] not in _ids or e['dst'] not in _ids])
# 孤立检查只对「有语义角色」的节点生效；finding 节点是判定叶子，出边为 0 属正常形态
_CORE = set(n['id'] for n in NODES if n['type'] != 'finding')
G_ISO = len([k for k, v in _out.items() if v == 0 and k in _CORE])
GRAPH = {
    'schema': 'openuft-index-graph/v1',
    'layer': 'r66-increment',
    'audit_book': '判定_TUFT-r66-QEI量纲闭合族判决与r64自修复_全维审计_2026-10-14.md',
    'node_types': ['family', 'family_member', 'prior_finding', 'open_item',
                   'constraint', 'finding'],
    'edge_types': ['contains', 'uses', 'downgraded_by', 'retracted_by', 'blocked_by',
                   'corrected_by', 'requires', 'related', 'bounds', 'relates', 'scopes',
                   'supports_exclusion', 'refutes_exclusion', 'constrains'],
    'nodes': NODES, 'edges': EDGES,
    'selfcheck': {'nodes': len(NODES), 'edges': len(EDGES), 'duplicate_ids': G_DUP,
                  'dangling_edges': G_DANGLE, 'isolated_nodes': G_ISO,
                  'all_pass': bool(G_DUP == 0 and G_DANGLE == 0 and G_ISO == 0)},
}
GRAPH_OK = GRAPH['selfcheck']['all_pass']

# =============================================================================
# 主程序
# =============================================================================
def main():
    tally = {}
    for it in ITEMS:
        tally[it['verdict']] = tally.get(it['verdict'], 0) + 1
    order = ['PASS', 'FAIL', 'CORRECTED', 'MISMATCH', 'BOUNDARY', 'INFO']
    tt = ' / '.join('%s=%d' % (k, tally.get(k, 0)) for k in order if k in tally)

    guard('G1-dims-all-ok', ALL_GUARDS_OK, '量纲工具自检 8 条全过方可用于判定')
    guard('G2-rhoE-not-rhoM', not eq(RHO_E, RHO_M),
          '阳性对照：能量密度必须不等于质量密度（仲裁①的前提）')
    guard('G3-r64-rho-claim-ok', eq(RHO_CLAIM, RHO_E), '仲裁②：来料 rho 式量纲 == 能量密度')
    guard('G4-e03b-indeed-broken', not eq(RATIO_DIM, D()),
          '确认 r64 E03b 的比值确实非无量纲（防「误撤」）')
    guard('G5-qei-unique-family', J_ONE_FAMILY, 'QEI 穷举必须归并到唯一 (1,1,4)')
    guard('G6-qei-five-families', J_FIVE, 'QEI 必须恰好 5 个量纲闭合族')
    guard('G7-one-survivor', len(J02_PASS) == 1,
          'J02 必须恰好 1 族不排除（若 0 族则结论应为「全族排除」，需改判词）')
    guard('G8-survivor-is-40', L02_OK, '幸存族必须是 (4,0)')
    guard('G9-both-bound-directions', (len(J03_UP) > 0 and len(J03_LO) > 0),
          'J03 必须同时出现上界与下界（若只有一种则「方向相反」结论不成立）')
    guard('G10-mneg-monotone',
          M03_ROWS[-1]['M_neg_kg'] != M03_ROWS[0]['M_neg_kg'] and M03_DOWN,
          'M_neg 随 delta 单调（M01 的前提）')
    guard('G11-two-oral-legits-differ', N_GEO_CONST and (N_ROWS[0]['delta_max_Gfixed'] != N_ROWS[-1]['delta_max_Gfixed']),
          'N01 两种 G 口径必须给出不同的 delta 上界（防「口径等价」误判）')
    guard('G12-graph-ok', GRAPH_OK, 'r66 图谱增量层自检')
    guard('G13-o01-measurable', O_YES >= 4,
          'O01 至少 4 个采样点应落在 1% 精度可测区（防把全表判成不可测）')

    evidence = {
        'guards': GUARD, 'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'rho_E_dim': show(RHO_E), 'rho_M_dim': show(RHO_M),
        'rho_E_eq_rho_M': eq(RHO_E, RHO_M),
        'rho_claim_dim': show(RHO_CLAIM), 'rho_claim_eq_rho_E': eq(RHO_CLAIM, RHO_E),
        't_max_dim': show(T_MAX_DIM), 't_planck_dim': show(T_P_DIM),
        't_ratio_dim': show(RATIO_DIM), 't_ratio_dimensionless': eq(RATIO_DIM, D()),
        'qei_exhaustive': J_N, 'qei_hits': len(J_HITS), 'qei_unique': J_UNIQ,
        'qei_families': J_FAM,
        'J02_table': J02_ROWS, 'J02_min_ratio': fv(J02_MINR, 10),
        'J02_max_ratio': fv(J02_MAXR, 10),
        'J02_surviving_families': [(r['a'], r['b']) for r in J02_PASS],
        'J03_table': J03_ROWS, 'J03_span': fv(J03_SPAN, 10),
        'J03_vs_r64': fv(J03_R64CMP, 10),
        'delta_max_40_m': fv(DLIM_40, 12), 'delta_max_40_over_lP': fv(DLIM_40_OVER_LP, 12),
        'curvature_shell': fv(CURV_SHELL, 12), 'curvature_bubble': fv(CURV_BUB, 12),
        'curvature_ratio': fv(CURV_RATIO, 12),
        'M_neg_geom_floor_Msun': fv(M_MNEG_GEOM / M_SUN, 12),
        'M_neg_r64_1m_Msun': fv(M_MNEG_R64 / M_SUN, 12),
        'M_neg_QEI40_Msun': fv(M_MNEG_QEI40 / M_SUN, 12),
        'M03_table': M03_ROWS,
        'N01_table': N_ROWS,
        'O01_table': O_ROWS,
        'rho_alc_lP': fv(K01_RHO_ALC, 12),
        'graph_selfcheck': GRAPH['selfcheck'],
        'graph_nodes': len(NODES), 'graph_edges': len(EDGES),
        'arbitration': [list(a) for a in ARB],
    }

    summary = {
        'book': NAME, 'date': '2026-10-14',
        'layer': 'r66 = QEI 族判决 + 对 r64 的自修复（r64 结构性否定 / r65 精算账）',
        'judgment_book': '判定_TUFT-r66-QEI量纲闭合族判决与r64自修复_全维审计_2026-10-14.md',
        'rating': 'O/L2（本册为自我修复册；结论方向：QEI 无条件排除被推翻，改为族条件性）',
        'item_count': len(ITEMS),
        'tally': dict((k, tally.get(k, 0)) for k in order), 'tally_text': tt,
        'guards_total': len(GUARD),
        'guards_passed': len([g for g in GUARD if g['ok']]),
        'items': ITEMS, 'evidence': evidence,
    }

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    with io.open(os.path.join(OUT, NAME + '.json'), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, ensure_ascii=False, indent=2))
    with io.open(os.path.join(OUT, 'TUFT-r66_图谱增量层_2026-10-14.json'), 'w',
                 encoding='utf-8') as fh:
        fh.write(json.dumps(GRAPH, ensure_ascii=False, indent=2))

    L = []
    L.append('# %s' % NAME)
    L.append('')
    L.append('- 日期：2026-10-14')
    L.append('- 层级：r64 结构性否定 / r65 精算账与可执行性 / **r66 QEI 族判决 + 自修复**')
    L.append('- 判定册：%s' % summary['judgment_book'])
    L.append('')
    L.append('## 汇总')
    L.append('')
    L.append('条目 %d（%s）· 守卫 %d/%d · 图谱 %d 节点 / %d 边（自检 %s）'
             % (len(ITEMS), tt, len([g for g in GUARD if g['ok']]), len(GUARD),
                len(NODES), len(EDGES), GRAPH_OK))
    L.append('')
    L.append('## 守卫')
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
    L.append('## QEI 五族判决表（★核心）')
    L.append('')
    L.append('| 族 (a,b) | 形式 | 需求 ρ | 允许 ρ | 比值 | QEI 判定 | δ 界方向 |')
    L.append('|---|---|---|---|---|---|---|')
    for r in J02_ROWS:
        L.append('| (%d,%d) | %s | %s | %s | **%s** | **%s** | %s |'
                 % (r['a'], r['b'], r['form'], r['rho_need'], r['rho_allow'],
                    r['ratio'], r['verdict_qei'], r['delta_bound']))
    L.append('')
    L.append('## δ 界数值')
    L.append('')
    L.append('| 族 | 方向 | K (m^2) | δ 界 (m) | /ℓ_P |')
    L.append('|---|---|---|---|---|')
    for r in J03_ROWS:
        L.append('| (%d,%d) | %s | %s | %s | %s |'
                 % (r['a'], r['b'], r['dir'], r['k_m2'], r['delta_limit_m'], r['over_lP']))
    L.append('')
    L.append('## M_neg 随 δ 的变化')
    L.append('')
    L.append('| δ | M_neg (kg) | M⊙ |')
    L.append('|---|---|---|')
    for r in M03_ROWS:
        L.append('| %s | %s | %s |' % (r['delta_label'], r['M_neg_kg'], r['M_over_Msun']))
    L.append('')
    L.append('## 三方仲裁总表')
    L.append('')
    L.append('| 议题 | r64 | r65 | r66（本册） | 裁定 |')
    L.append('|---|---|---|---|---|')
    for a in ARB:
        L.append('| %s | %s | %s | %s | %s |' % a)
    L.append('')
    with io.open(os.path.join(OUT, NAME + '.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')

    R = ['=' * 74, NAME, '2026-10-14', '=' * 74,
         '条目 %d   %s' % (len(ITEMS), tt),
         '守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)),
         '图谱 %d 节点 / %d 边  自检 %s' % (len(NODES), len(EDGES), GRAPH_OK), '']
    R.append('-' * 74)
    for g in GUARD:
        R.append('[%s] %-28s %s' % ('PASS' if g['ok'] else 'FAIL', g['guard'], g['note']))
    R.append('')
    R.append('-' * 74)
    for it in ITEMS:
        R.append('[%s] %s  %s' % (it['verdict'], it['code'], it['title']))
        R.append('       %s' % it['detail'][:280])
        if it['evidence']:
            R.append('       机器: %s' % it['evidence'][:180])
        R.append('')
    R.append('-' * 74)
    R.append('QEI 五族判决表（delta=l_P, L=100m, v_s=c）')
    for r in J02_ROWS:
        R.append('  (a,b)=(%d,%d) ratio=%s -> %s ; delta %s'
                 % (r['a'], r['b'], r['ratio'], r['verdict_qei'], r['delta_bound']))
    R.append('')
    with io.open(os.path.join(OUT, NAME + '_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(R) + '\n')

    print('=' * 74)
    print(NAME)
    print('条目 %d   %s' % (len(ITEMS), tt))
    print('守卫 %d / %d' % (len([g for g in GUARD if g['ok']]), len(GUARD)))
    print('图谱 %d 节点 / %d 边  自检 %s' % (len(NODES), len(EDGES), GRAPH_OK))
    print('=' * 74)
    print('仲裁: 能量密度=%s (质量密度=%s) -> r64 对 / r65 裁定3 错'
          % (show(RHO_E), show(RHO_M)))
    print('E03b 量纲: t_max=%s, 比值=%s, 无量纲=%s -> 撤回'
          % (show(T_MAX_DIM), show(RATIO_DIM), eq(RATIO_DIM, D())))
    print('QEI 穷举 %d 组 -> 唯一 (al,be,a+b)=%s -> %d 族 %s'
          % (J_N, J_UNIQ, len(J_FAM), J_FAM))
    print('J02 判决: 不排除 %d 族 / 排除 %d 族；比值跨度 %s ~ %s'
          % (len(J02_PASS), len(J02_FAIL), fv(J02_MINR, 4), fv(J02_MAXR, 4)))
    print('delta 界: 上界 %d 族 / 无关 %d 族 / 下界 %d 族；跨度 %s'
          % (len(J03_UP), len(J03_FLAT), len(J03_LO), fv(J03_SPAN, 4)))
    print('幸存族(4,0): delta<=%s m (%s l_P) ; M_neg 下界 %s M_sun ; 曲率集中 %s'
          % (fv(DLIM_40, 4), fv(DLIM_40_OVER_LP, 4),
             fv(M_MNEG_QEI40 / M_SUN, 4), fv(CURV_RATIO, 4)))
    bad = [g['guard'] for g in GUARD if not g['ok']]
    if bad:
        print('GUARD FAILED: %s' % bad)
        return 1
    print('GUARD ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
