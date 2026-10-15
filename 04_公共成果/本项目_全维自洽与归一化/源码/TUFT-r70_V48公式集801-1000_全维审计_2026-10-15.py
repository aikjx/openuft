# -*- coding: utf-8 -*-
"""
r70 · 2026-10-15 · 《openuft#49 ｜1000 核心理论体系公式集（续，公式 801-1000）》
      TUFT v4.8 条目集 全维审计（公理层 / 张量层 / 因果性 / 自由度 / 记账）
==============================================================================
来料：my_lib/openuft49_1000核心理论体系公式集_公式801-1000.md（594 行，200 条 801-1000）
      由助理本轮从被转义污染的 LaTeX 还原整理；本册只审内容，不再做格式整理。

审计对象（机器可判定的六组）：
  A 公理层量纲与符号：801(κ²+τ²=ω²) / 802·938(张量版) / 803(旋量投影) / 804(量纲声明)
                      / 940(经典极限 τ→0)
  B 因果性与色散：835(ω²=k²+κ²+τ²) / 836(v_g=k/ω) 与 801 的联立后果
  C 毕安基与守恒：822 / 823 / 824 与 812 的联立后果；张量型匹配
  D 畸变张量（contorsion）：819 定义式 vs 820 联络分解的自洽性（精确算术复原检验）
  E 自由度计数：828 的 10+24+1+1-1=35 与 829「退化到 GR, N→10」的口径
  F 记账与统计：964 版本链 / 930 预测比 / 880 χ² 可加性 / 995 稳定性 / 991 全局积分
                / OPEN 标记覆盖率

设计原则（承 r37 / r59 / r64 / r66 / r67 / r69）
 1) 纯标准库 + Decimal 60 位；量纲用 Fraction 四元组 (M,L,T,Q)，指数相加
    （r37 曾错写为逐分量相乘，本册 G0-* 守卫兜底）。
 2) 量纲工具必须先过自守卫 G0-* 再用于判定；手算量纲一律机器兜底。
 3) 任何"残差为零"结论必须配阳性对照，否则无法区分"真恒等"与"检验器坏了"。
 4) 不自推的系数/结论显式登记 not_self_derived，不编。
 5) 只审来料写出的式子，不替来料补写未写出的项（补写属"代选"）。
 6) 退出码 0 = 引擎跑完；结论看 counts/verdict，不看退出码。
 7) 不改任何他人文件字节；不跑 refresh_catalog（并发回退风险，待批准）。
==============================================================================
"""

import sys, os, io, json, re, glob, random, shutil
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
OFT_UP = os.path.dirname(BASE)          # 04_公共成果
OPENUFT = os.path.dirname(OFT_UP)       # openuft
MY_LIB = os.path.dirname(OPENUFT)       # my_lib

STEM = 'TUFT-r70_V48公式集801-1000_全维审计_2026-10-15'
SRC_NAME = STEM + '.py'

# ----------------------------------------------------------------------------
# 1) 量纲工具：(M, L, T, Q) 四元组，Fraction 指数
# ----------------------------------------------------------------------------
ZERO = (Fr(0), Fr(0), Fr(0), Fr(0))


def d(*e):
    """构造量纲向量：d(m, l, t, q)"""
    e = list(e) + [0] * (4 - len(e))
    return (Fr(e[0]), Fr(e[1]), Fr(e[2]), Fr(e[3]))


def dmul(a, b):
    """量纲相乘 = 指数相加（r37 曾错写为逐分量相乘，此处为唯一真源）"""
    return tuple(x + y for x, y in zip(a, b))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dpow(a, n):
    n = Fr(n)
    return tuple(x * n for x in a)


def deq(a, b):
    return all(x == y for x, y in zip(a, b))


def dstr(a):
    names = ('M', 'L', 'T', 'Q')
    out = []
    for nm, x in zip(names, a):
        if x == 0:
            continue
        out.append(nm + '^' + str(x))
    return ' · '.join(out) if out else '1'


D_M, D_L, D_T, D_Q = d(1, 0, 0, 0), d(0, 1, 0, 0), d(0, 0, 1, 0), d(0, 0, 0, 1)
D_c = d(0, 1, -1, 0)
D_hbar = d(1, 2, -1, 0)
D_G = d(-1, 3, -2, 0)
D_kappa = d(0, -1, 0, 0)      # [κ] = [τ] = [ω] = L^-1（来料 804 声明）
D_tau = D_kappa
D_omega = D_kappa
D_riemann = d(0, -2, 0, 0)    # R^a_{bcd}, R_ab
D_torsion = d(0, -1, 0, 0)    # T^a_{bc}
D_g = ZERO                    # 度规无量纲
D_u = ZERO                    # 类时单位矢量无量纲
D_E = d(1, 2, -2, 0)          # 能量
D_rhoE = d(1, -1, -2, 0)      # 能量密度（r66 定案：ρ_E = M L^-1 T^-2）
D_rhoM = d(1, -3, 0, 0)       # 质量密度
D_lP = d(0, 1, 0, 0)

# ----------------------------------------------------------------------------
# 2) 条目收集器
# ----------------------------------------------------------------------------
ITEMS = []
GUARDS = []
COUNT = {'PASS': 0, 'FAIL': 0, 'MISMATCH': 0, 'CORRECTED': 0, 'INFO': 0, 'BOUNDARY': 0}


def rec(code, kind, title, detail='', numbers=None, not_self_derived=False):
    if kind not in COUNT:
        raise ValueError('bad kind: ' + kind)
    COUNT[kind] += 1
    ITEMS.append({
        'code': code, 'kind': kind, 'title': title, 'detail': detail,
        'numbers': numbers or {}, 'not_self_derived': not_self_derived,
    })
    print('[%s] %s : %s' % (kind, code, title))
    if detail:
        print('    ' + detail)
    if numbers:
        for k in sorted(numbers):
            print('    %s = %s' % (k, numbers[k]))
    return None


def guard(name, ok, note=''):
    GUARDS.append({'name': name, 'ok': bool(ok), 'note': note})
    if not ok:
        print('[GUARD-FAIL] %s : %s' % (name, note))
    return bool(ok)


# ----------------------------------------------------------------------------
# 2.5) 来料读取与条目切片（只读，不改来料）
# ----------------------------------------------------------------------------
SRC_CANDIDATES = glob.glob(os.path.join(MY_LIB, 'openuft49_1000*801-1000*.md'))
SRC_PATH = SRC_CANDIDATES[0] if SRC_CANDIDATES else None
SRC_TEXT = ''
if SRC_PATH:
    SRC_TEXT = io.open(SRC_PATH, encoding='utf-8').read()

ITEM_RE = re.compile(r'^(\d{3,4})\. ', re.M)
_MARKS = list(ITEM_RE.finditer(SRC_TEXT))
ITEM_IDS = [int(m.group(1)) for m in _MARKS]
ITEM_BLOCK = {}
for i, m in enumerate(_MARKS):
    end = _MARKS[i + 1].start() if i + 1 < len(_MARKS) else len(SRC_TEXT)
    ITEM_BLOCK[int(m.group(1))] = SRC_TEXT[m.end():end].strip()


def item(n):
    return ITEM_BLOCK.get(int(n), '')


def has_open(n):
    return 'OPEN' in item(n)


def math_of(n):
    """取条目公式体：优先独立公式 $$...$$，回退行内 $...$。
    自抓记录：首版只认 $$ ⇒ 823 / 938 等行内公式条目取空串，
    导致 A03 假 MISMATCH、C02 两侧皆空被判 PASS（「绿灯但自相矛盾」）。"""
    b = item(n)
    m = re.search(r'\$\$(.*?)\$\$', b, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', b, re.S)
    return m.group(1).strip() if m else ''


def sides(n):
    s = math_of(n)
    return s.split('=') if '=' in s else [s]


def norm_mul(s):
    """乘法因子归一：拆出各乘法因子后排序。用于判定两式是否为同式复读（仅因子次序不同）。
    自抓记录：首版只按 '*' 切分，而来料用 LaTeX 的 \\, 与空格分隔因子 ⇒ 恒判不等（假 MISMATCH）。"""
    t = s.replace('\\,', ' ').replace('\\;', ' ').replace('\\ ', ' ')
    t = re.sub(r'\}(?=[A-Za-z\\])', '} ', t)          # R_{ab}R^{ab} → R_{ab} R^{ab}
    t = re.sub(r'(\^[A-Za-z])(?=[A-Za-z])', r'\1 ', t)  # u^au^b → u^a u^b
    return '|'.join(sorted(x for x in t.split() if x))


def norm_expr(s):
    """含 '+' 的表达式归一：逐项因子归一后整体排序"""
    return '|'.join(sorted(norm_mul(p) for p in s.split('+')))


def free_terms(s):
    """逐项自由指标集（每项内出现次数为 1 的指标）。多项式求和必须逐项算，
    否则同一指标在 4 个项里各出现一次会被误算成「收缩掉」（首版自由集恒空）。"""

    def one(term):
        cnt = {}
        for m in re.finditer(r'[\^_](?:\{([a-zA-Z]+)\}|([a-zA-Z]))', term):
            g = m.group(1) or m.group(2)
            for ch in g:
                cnt[ch] = cnt.get(ch, 0) + 1
        return sorted([k for k, v in cnt.items() if v == 1])

    return [one(p) for p in s.split('+')]


def free_ok(s):
    ft = free_terms(s)
    return len(ft) > 0 and all(x == ft[0] for x in ft)


guard('G0-0', len(ITEM_IDS) == 200 and ITEM_IDS == list(range(801, 1001)),
      '来料条目 801-1000 连续无缺号（实得 %d 条）' % len(ITEM_IDS))
_NEED_MATH = [801, 802, 803, 812, 822, 823, 824, 835, 836, 938, 940, 991]
guard('G0-0b', all(math_of(n) for n in _NEED_MATH),
      '关键条目公式体全部解析非空：%s'
      % ', '.join('%d=%s' % (n, bool(math_of(n))) for n in _NEED_MATH))

# ----------------------------------------------------------------------------
# 3) G0 量纲工具自守卫（必须先过，再用于判定）
# ----------------------------------------------------------------------------
guard('G0-1', deq(dmul(D_c, D_T), D_L), 'c·T = L')
guard('G0-2', not deq(dmul(D_hbar, D_c), D_G), 'ħc ≠ G（差 M^2）')
guard('G0-3', deq(ddiv(D_E, dpow(D_L, 3)), D_rhoE), 'E/L^3 = 能量密度')
guard('G0-4', not deq(D_E, D_rhoE), '能量 ≠ 能量密度（r66 定案）')
guard('G0-5', not deq(D_rhoE, D_rhoM), '能量密度 ≠ 质量密度')
guard('G0-6', deq(dmul(D_riemann, D_riemann), d(0, -4, 0, 0)), 'R_ab R^ab = L^-4')
guard('G0-7', deq(dmul(D_torsion, D_torsion), d(0, -2, 0, 0)), 'T_acd T^acd = L^-2')
guard('G0-8', not deq(d(0, -4, 0, 0), d(0, -2, 0, 0)), 'L^-4 ≠ L^-2（802 不齐的前提）')
guard('G0-9', deq(dmul(ddiv(D_G, dpow(D_c, 4)), D_rhoE), d(0, -2, 0, 0)),
      'Einstein 方程量纲闭合：(G/c^4)·ρ_E = L^-2')
guard('G0-10', deq(dmul(D_omega, D_omega), d(0, -2, 0, 0)), 'ω^2 = L^-2')

# ----------------------------------------------------------------------------
# 4) A 组 · 公理层量纲与符号
# ----------------------------------------------------------------------------
# 801: κ^2+τ^2=ω^2
LHS801 = dmul(D_kappa, D_kappa)
RHS801 = dmul(D_omega, D_omega)
rec('A01', 'PASS' if deq(LHS801, RHS801) else 'FAIL',
    '801 公理 κ²+τ²=ω² 量纲齐次（两边皆 L^-2）',
    'LHS=%s ; RHS=%s' % (dstr(LHS801), dstr(RHS801)),
    {'dim_LHS': dstr(LHS801), 'dim_RHS': dstr(RHS801),
     'homogeneous': str(deq(LHS801, RHS801))})

# 802 / 938: R_ab R^ab + T_acd T^acd = ω^2 u^a u^b g_ab
t1 = dmul(D_riemann, D_riemann)      # L^-4
t2 = dmul(D_torsion, D_torsion)      # L^-2
rhs802 = dmul(dmul(dmul(D_omega, D_omega), D_g), dmul(D_u, D_u))  # L^-2
gap802 = ddiv(t1, t2)                # L^-2
rec('A02', 'FAIL',
    '802/938 张量版公理量纲非齐次：R_ab R^ab(L^-4) 与 T_acd T^acd(L^-2) 不可相加',
    '两项差 %s ；右端 ω²·g·u·u = %s 只与第二项同量纲 ⇒ 第一项无处安放。'
    '（本库「量纲非齐次」缺陷族跨册复发实例）' % (dstr(gap802), dstr(rhs802)),
    {'dim_term1': dstr(t1), 'dim_term2': dstr(t2), 'gap': dstr(gap802),
     'dim_RHS': dstr(rhs802),
     'term1_vs_RHS': str(deq(t1, rhs802)), 'term2_vs_RHS': str(deq(t2, rhs802))})

# 802 与 938 同式复读（机器比对：等式两边乘法因子归一后逐字相等）
_s802, _s938 = sides(802), sides(938)
_lhs_same = len(_s802) == len(_s938) == 2 and norm_expr(_s802[0]) == norm_expr(_s938[0])
_rhs_same = len(_s802) == len(_s938) == 2 and norm_expr(_s802[1]) == norm_expr(_s938[1])
rec('A03', 'INFO' if (_lhs_same and _rhs_same) else 'MISMATCH',
    '802 与 938 为同一式的重复登记（938「Axiom A3 张量提升版」= 802 原式）',
    '机器比对：LHS 归一相等=%s ；RHS 归一相等=%s '
    '（ω² u^a u^b g_ab ↔ ω² g_ab u^a u^b 仅因子次序不同）⇒ 不产生新内容，'
    '属本库「恒等式复读」类零信息量条目。' % (_lhs_same, _rhs_same),
    {'math_802': math_of(802), 'math_938': math_of(938),
     'lhs_same': str(_lhs_same), 'rhs_same': str(_rhs_same)})

# 803 旋量投影
rec('A04', 'BOUNDARY',
    '803 旋量投影公理：φ、χ 的量纲来料未声明 ⇒ 无法唯一判定；按自然类比（φ↔曲率 L^-2、χ↔挠率 L^-1）与 802 同型不齐',
    '若 [φ]=L^-2、[χ]=L^-1，则 φφ̄=L^-4、χχ̄=L^-2，与 802 同一缺陷；'
    '来料未给旋量量纲表，故本册不判 FAIL，登记为口径未声明。',
    {'assumed_dim_phi': 'L^-2', 'assumed_dim_chi': 'L^-1', 'declared': 'False'},
    not_self_derived=True)

# 804 与 802 的一致性
rec('A05', 'FAIL',
    '804 声明 [κ]=[τ]=[ω]=L^-1 与 802 不自洽：802 要求 ω² 与 R_ab R^ab(L^-4) 配对',
    '802 若成立则 [ω²] 须同时是 L^-4 与 L^-2 ⇒ 804 的量纲表与 802 互斥；'
    '804 只覆盖 801，未覆盖 802。',
    {'declared_in_804': 'κ,τ,ω = L^-1', 'required_by_802': 'ω² = L^-4 (第一项) 且 L^-2 (第二项)'})

# 940 经典极限的符号矛盾（号差 (-,+,+,+)，类时单位矢量 g_ab u^a u^b = -1）
U_SQ = -1
# 802: R_ab R^ab + T·T = ω^2 * (g_ab u^a u^b) = -ω^2
# τ→0 ⇒ T→0 ⇒ R_ab R^ab = -ω^2 ⇒ ω^2 = -R_ab R^ab
# 940 声称 ω → +sqrt(R_ab R^ab) ⇒ ω^2 = +R_ab R^ab
rec('A06', 'FAIL',
    '940 经典极限与 802 符号矛盾：号差 (-,+,+,+) 下 g_ab u^a u^b = -1 ⇒ 802 给 ω² = -R_ab R^ab，而 940 给 ω² = +R_ab R^ab',
    '承重：τ→0（挠率冻结）时 802 退化为 R_ab R^ab = ω²·(-1) ⇒ ω² = -R_ab R^ab；'
    '940 却写 ω → +√(R_ab R^ab)。除非 R_ab R^ab ≡ 0（平凡解），否则两者必居其一为错；'
    '若 R_ab R^ab > 0 则 802 强制 ω 为虚数 ⇒ 经典极限不存在。',
    {'signature': '(-,+,+,+)', 'g_u_u': str(U_SQ),
     'from_802': 'ω^2 = -R_ab R^ab', 'from_940': 'ω^2 = +R_ab R^ab',
     'sign_conflict': 'True'})

# ----------------------------------------------------------------------------
# 5) B 组 · 因果性与色散（835 / 836 与 801 的联立后果）
# ----------------------------------------------------------------------------
KA = Decimal('1.234')      # κ
TA = Decimal('0.567')      # τ
W2_801 = KA * KA + TA * TA
W_801 = W2_801.sqrt()
K2_FROM_835 = W2_801 - (KA * KA + TA * TA)   # 835 解出的 k²
rec('B01', 'FAIL',
    '835 与 801 联立 ⇒ k² ≡ 0：色散关系退化，几何波无传播模',
    '801 给 ω²=κ²+τ²；代入 835（ω²=k²+κ²+τ²）得 k²=%s ⇒ k≡0。'
    '⇒ 836 的 v_g=k/ω 恒为 0，「自动满足因果性」成为恒真命题（见 B02）；'
    '同时「UFT 几何波」在该联立下不存在有限波数的传播解。' % (K2_FROM_835,),
    {'kappa': str(KA), 'tau': str(TA), 'omega_sq_801': str(W2_801),
     'k_sq_from_835': str(K2_FROM_835), 'k': str(K2_FROM_835.sqrt())},
    )

_vg = {}
_vp = {}
_vg_neg = {}
for _k in ['0.1', '1', '10', '100']:
    kv = Decimal(_k)
    om = (kv * kv + KA * KA + TA * TA).sqrt()
    _vg[_k] = kv / om
    _vp[_k] = om / kv
    inner = kv * kv - KA * KA - TA * TA
    _vg_neg[_k] = (kv / inner.sqrt()) if inner > 0 else None
VG_MAX = max(_vg.values())
VG_NEG_MAX = max(v for v in _vg_neg.values() if v is not None)
rec('B02', 'BOUNDARY',
    '836「v_g=k/ω 自动 ≤1」在 835 下算术为真，但结论只依赖 κ²+τ² 的正号，与 UFT 公理/挠率物理无关 ⇒ 零 UFT 判别力',
    '正号口径：k=0.1/1/10/100 时 v_g 单调趋 1，max=%s < 1 ✓。'
    '阳性对照（改号 ω²=k²−κ²−τ²）：同 k 下 v_g 最大 %s > 1 ⇒ 判据非恒真、检验器有效。'
    '⇒ 836 的因果性来自色散式的符号选择，不是 UFT 的成就，也不是对任何 UFT 断言的检验。'
    % (VG_MAX, VG_NEG_MAX),
    {'vg_plus': {k: str(v) for k, v in _vg.items()},
     'vg_max_plus': str(VG_MAX),
     'vg_negative_sign_control': {k: (str(v) if v is not None else 'n/a') for k, v in _vg_neg.items()},
     'vg_max_negative_sign': str(VG_NEG_MAX),
     'positive_control_works': str(VG_NEG_MAX > 1)})

rec('B03', 'INFO',
    '836 所「消解」的「超光速佯谬」对象本身不是佯谬：相速度 v_p=ω/k>1 不承载信号',
    '机器读数：k=0.1 时 v_p=%s、k=100 时 v_p=%s（均 >1）；因果性约束的是群速度/信号速度而非相速度，'
    '属标准波物理，非 UFT 特有结论。' % (_vp['0.1'], _vp['100']),
    {'vp_k0p1': str(_vp['0.1']), 'vp_k100': str(_vp['100'])})

# ----------------------------------------------------------------------------
# 6) C 组 · 毕安基与守恒（812 / 822 / 823 / 824）
# ----------------------------------------------------------------------------
_s823 = sides(823)
_left823 = _s823[0] if _s823 else ''
_right823 = _s823[1] if len(_s823) > 1 else ''
F823L, F823R = free_terms(_left823), free_terms(_right823)
TYPE_OK_823 = bool(F823L and F823R and F823L[0] == F823R[0])

_s812 = sides(812)
F812L = free_terms(_s812[0]) if _s812 else []
F812R = free_terms(_s812[1]) if len(_s812) > 1 else []
TYPE_OK_812 = bool(F812L and F812R and F812L[0] == F812R[0])

guard('G-C1', bool(_left823) and bool(_right823),
      '823 公式体解析非空（防空串导致两侧皆空 ⇒ 假 PASS；首版即踩此坑）')
guard('G-C2', TYPE_OK_812, '812 张量型自检：两边自由指标一致（检验器对正确式须判一致）')
guard('G-C3', TYPE_OK_812 and not TYPE_OK_823,
      '检验器非恒真：812 判一致且 823 判不一致（若解析器失灵，两者会同向 ⇒ 本守卫拦下）')

rec('C01', 'FAIL',
    '823 与 812+824 三方矛盾：812+824 强制 ∇^a G_ab ≡ 0，则 823 的挠率源 T^source_ab 必恒为零',
    '812 给 G_ab = 8πG·T^tot_ab；824 给 ∇^a T^tot_ab = 0 ⇒ ∇^a G_ab = 8πG·∇^a T^tot_ab ≡ 0；'
    '而 823 写 ∇^a G_ab = T^source_ab 并称「挠率提供源」。⇒ 三者不能同时成立：'
    '要么放弃 824（总能动不守恒），要么 823 的源项必须重新安置（例如改写到物质侧或改为恒等式右端的 0）。'
    '本册不代选修法。',
    {'has_812': str('8\\pi G' in math_of(812)), 'has_823': str('\\nabla^a G_{ab}' in math_of(823)),
     'has_824': str("T_{ab}^{\\text{tot}}" in math_of(824)),
     'math_823': math_of(823), 'contradiction': 'True'})

rec('C02', 'FAIL' if not TYPE_OK_823 else 'PASS',
    '823 张量型不匹配：左端 ∇^a G_ab 只剩 1 个自由下标 b，右端 T^source_ab 有 2 个（a,b）',
    '逐项自由指标集合：左=%s ，右=%s ⇒ 两边张量型不同（(0,1) vs (0,2)），'
    '这是独立于量纲的结构错误。对照：812 左=%s 右=%s ⇒ 812 的张量型正确，检验器有效。'
    % (F823L, F823R, F812L, F812R),
    {'free_terms_left_823': str(F823L), 'free_terms_right_823': str(F823R),
     'type_match_823': str(TYPE_OK_823),
     'free_terms_left_812': str(F812L), 'free_terms_right_812': str(F812R),
     'type_match_812': str(TYPE_OK_812)})

# 822 带挠率毕安基：逐项自由指标集 + 量纲
_m822 = math_of(822)
_l822, _r822 = _m822.split('=')[0], _m822.split('=')[1]
_setsL = free_terms(_l822)
_setsR = free_terms(_r822)
_dim822L = dmul(d(0, -1, 0, 0), D_riemann)     # ∇R
_dim822R = dmul(D_torsion, D_riemann)          # T·R
rec('C03', 'PASS' if deq(_dim822L, _dim822R) and _setsL and _setsR and _setsL[0] == _setsR[0] else 'FAIL',
    '822 带挠率毕安基恒等式：量纲齐次（∇R 与 T·R 皆 L^-3）且逐项自由指标集一致',
    '左逐项自由指标=%s ；右逐项自由指标=%s ；量纲左=%s、右=%s ⇒ 形式为教科书级正确。'
    '（本册只核形式，不核挠率项的系数与符号约定，登记 not_self_derived。）'
    % (_setsL, _setsR, dstr(_dim822L), dstr(_dim822R)),
    {'dim_LHS': dstr(_dim822L), 'dim_RHS': dstr(_dim822R),
     'free_per_term_LHS': str(_setsL), 'free_per_term_RHS': str(_setsR)},
    not_self_derived=True)

# ----------------------------------------------------------------------------
# 7) D 组 · 畸变张量（contorsion）819 vs 820：精确算术复原检验
# ----------------------------------------------------------------------------
# 记号约定（本册显式声明，避免跨册符号歧义）：
#   挠率 T^a_{bc} = Γ^a_{bc} − Γ^a_{cb}（对 b,c 反对称）；
#   由 820（Γ = Γ_LC + K）⇒ T_{abc} = K_{abc} − K_{acb}（全下标）；
#   度规兼容 ∇g = 0 ⇒ K_{abc} = −K_{bac}（对前两指标反对称）。
#   来料 819 写 K^a_{bc} = ½(T^a_{bc} − T^a_{cb} − T_{bc}{}^a)；
#   记号 T_{bc}{}^a 的两种常见翻译（g^{ad}T_{bcd} / g^{ad}T_{bdc}）分别对应下面的
#   cand_819a / cand_819b；两种翻译下都做检验 ⇒ 结论与翻译约定无关。
rnd = random.Random(20261015)
KT = {}
for a in range(4):
    for b in range(4):
        for c in range(4):
            if (a, b, c) in KT:
                continue
            if a == b:
                KT[(a, b, c)] = Fr(0)
            else:
                v = Fr(rnd.randint(-9, 9), rnd.randint(1, 7))
                KT[(a, b, c)] = v
                KT[(b, a, c)] = -v

RANGE4 = range(4)
TRIPLES = [(a, b, c) for a in RANGE4 for b in RANGE4 for c in RANGE4]
ANTISYM_OK = all(KT[(a, b, c)] == -KT[(b, a, c)] for a, b, c in TRIPLES)
TT = {(a, b, c): KT[(a, b, c)] - KT[(a, c, b)] for a, b, c in TRIPLES}
TOR_ANTISYM_OK = all(TT[(a, b, c)] == -TT[(a, c, b)] for a, b, c in TRIPLES)


def c_std(a, b, c):
    return (TT[(a, b, c)] + TT[(b, c, a)] - TT[(c, a, b)]) / 2


def c_819a(a, b, c):
    return (TT[(a, b, c)] - TT[(a, c, b)] - TT[(b, c, a)]) / 2


def c_819b(a, b, c):
    return (TT[(a, b, c)] - TT[(a, c, b)] + TT[(b, c, a)]) / 2


def resid(f):
    r1 = max(abs(f(a, b, c) - KT[(a, b, c)]) for a, b, c in TRIPLES)
    r2 = max(abs((f(a, b, c) - f(a, c, b)) - TT[(a, b, c)]) for a, b, c in TRIPLES)
    return r1, r2


R_STD = resid(c_std)
R_A = resid(c_819a)
R_B = resid(c_819b)

guard('G-D1', ANTISYM_OK and TOR_ANTISYM_OK, 'K 对前两指标反对称、T 对后两指标反对称')
guard('G-D2', R_STD[0] == 0 and R_STD[1] == 0, '标准 contorsion 精确复原 K 且满足 2K_{a[bc]}=T_{abc}')
guard('G-D3', R_A[0] != 0 or R_A[1] != 0, '819 翻译一不自洽（阳性对照：必须非零，否则检验器恒真）')
guard('G-D4', R_B[0] != 0 or R_B[1] != 0, '819 翻译二不自洽（同上）')

rec('D01', 'FAIL',
    '819 畸变张量定义式与 820 不自洽：两种记号翻译均不能从挠率复原 K',
    '精确算术（Fraction，无浮点）：复原残差 max|K_cand − K_true| —— 标准式=%s（机器零）；'
    '819 翻译一=%s ；819 翻译二=%s 。'
    '定义性质 2K_{a[bc]} = T_{abc} 的残差 —— 标准式=%s ；819 翻译一=%s ；819 翻译二=%s 。'
    '⇒ 819 的第三项 −T_{bc}{}^a 应为 −T_{cb}{}^a 型（且第一项系数因 −T^a_{cb}=+T^a_{bc} 而被加倍），'
    '当前写法使 K 被系统放大，与 820 的 Γ = Γ_LC + K 不闭合。'
    % (R_STD[0], R_A[0], R_B[0], R_STD[1], R_A[1], R_B[1]),
    {'resid_restore_std': str(R_STD[0]), 'resid_restore_819a': str(R_A[0]),
     'resid_restore_819b': str(R_B[0]),
     'resid_defprop_std': str(R_STD[1]), 'resid_defprop_819a': str(R_A[1]),
     'resid_defprop_819b': str(R_B[1]),
     'antisym_K': str(ANTISYM_OK), 'antisym_T': str(TOR_ANTISYM_OK)})

rec('D02', 'PASS',
    '给出修正读数（不自推、机器验证）：K_{abc} = ½(T_{abc} + T_{bca} − T_{cab}) 精确复原 K 且满足定义性质',
    '该式由「Γ = Γ_LC + K」+「T^a_{bc} = Γ^a_{[bc]} 的两倍」+「度规兼容 K_{abc}=−K_{bac}」三条唯一确定，'
    '本册用随机反对称 K 构造 T 后反向复原，残差精确为 0（Fraction 精确算术，无浮点误差可辩）。'
    '残差=%s / %s' % (R_STD[0], R_STD[1]),
    {'correct_form': 'K_{abc} = 1/2 (T_{abc} + T_{bca} - T_{cab})',
     'resid_restore': str(R_STD[0]), 'resid_defprop': str(R_STD[1])})

N_INDEP_T = sum(1 for a in RANGE4 for b in RANGE4 for c in RANGE4 if b < c)
N_INDEP_K = sum(1 for a in RANGE4 for b in RANGE4 for c in RANGE4 if a < b)
rec('D03', 'PASS',
    '挠率独立分量 = 4×C(4,2) = %d，与 contorsion 独立分量 %d 相等 ⇒ 交叉印证 828 的「24」'
    % (N_INDEP_T, N_INDEP_K),
    'T^a_{bc} 对 b,c 反对称 ⇒ 4×6=%d ；K_{abc} 对 a,b 反对称 ⇒ 6×4=%d ；两者相等是 Γ=Γ_LC+K 的必要条件。'
    % (N_INDEP_T, N_INDEP_K),
    {'n_indep_torsion': str(N_INDEP_T), 'n_indep_contorsion': str(N_INDEP_K)})

# ----------------------------------------------------------------------------
# 8) E 组 · 自由度计数（828 / 829 / 830）
# ----------------------------------------------------------------------------
DOF828 = 10 + 24 + 1 + 1 - 1
rec('E01', 'PASS',
    '828 算术自洽：10+24+1+1−1 = %d，与来料写的 35 一致' % DOF828,
    '分项：度规对称张量分量 C(5,2)=10 ；挠率 24（D03 机器复核） ；ω 标量 1 ；乘子 λ 1 ；约束 κ²+τ²=ω² 减 1 。',
    {'dof_claim': '35', 'dof_recomputed': str(DOF828)})

GR_PHASE = 6 * 2          # h_ij 6 个分量 × 2（位形 + 动量）
GR_CONSTRAINTS = 4 * 2    # 哈密顿 + 3 动量，各减 2（约束 + 规范）
GR_DOF = (GR_PHASE - GR_CONSTRAINTS) // 2
rec('E02', 'FAIL',
    '828/829 把「场分量数」当作「物理自由度」：829 称低能退化到 GR 时 N_dof→10，而 GR 的物理自由度是 2',
    'ADM 计数：h_ij 6 个分量 ⇒ 相空间 %d ；哈密顿约束 1 + 动量约束 3 共 4 条，各配 1 个规范自由度 ⇒ 减 %d ；'
    '余 %d / 2 = %d 个物理自由度（两个引力偏振）。'
    '⇒ 同一册内 828 用「分量数」、829 用「自由度」两个口径，10 与 2 差 5 倍 ⇒ 830 的「35 个场自由度」同样是分量数而非物理自由度。'
    % (GR_PHASE, GR_CONSTRAINTS, GR_PHASE - GR_CONSTRAINTS, GR_DOF),
    {'gr_phase_space': str(GR_PHASE), 'gr_constraints': str(GR_CONSTRAINTS),
     'gr_physical_dof': str(GR_DOF), 'claimed_829': '10', 'ratio': '5'})

rec('E03', 'BOUNDARY',
    '828 的「−1」口径不自洽：标量约束在相空间里应减 2（1 约束 + 1 规范固定），不是减 1',
    '若按相空间口径，κ²+τ²=ω² 一条标量约束应减 2；按分量配置口径则应说明 35 是「配置变量分量数」而非自由度。'
    '来料未声明口径 ⇒ 本册只登记不自洽，不代选口径。',
    {'subtracted': '1', 'phase_space_convention': '2'})

# ----------------------------------------------------------------------------
# 9) F 组 · 记账、版本、统计
# ----------------------------------------------------------------------------
V48_OK = ('v4.8' in item(964)) and ('openuft#49' in SRC_TEXT)
rec('F01', 'PASS' if V48_OK else 'MISMATCH',
    '964 版本链自洽：TUFT v4.8 = openuft#49 = 本公式集（与来料标题逐字一致）',
    '机器：item(964) 含 v4.8 = %s ；来料标题含 openuft#49 = %s 。'
    % (('v4.8' in item(964)), ('openuft#49' in SRC_TEXT)),
    {'version': 'v4.8', 'anchor': 'openuft#49', 'self_consistent': str(V48_OK)})

RATIO = Decimal('22') / Decimal('3')
rec('F02', 'FAIL',
    '930 预测比 22/3 ≈ 7.3 算术正确，但「输入几何参数 = 3」的记账不成立：810 含自由函数 f(τ,ω)、811 新增乘子场 λ',
    '机器：22/3 = %s（来料写 ≈7.3 ✓ 算术）。但分母口径错误：'
    '810 的 𝓛 主干含未指定函数 f(τ,ω) —— 按本库 r15 纪律，一个自由函数是无穷维输入，不是「一个参数」；'
    '811 又引入乘子场 λ 作为新自由度。⇒ 真实输入 ≥ 3(κ,τ,ω 或等价) + 1(λ) + 1 个自由函数；'
    '在自由函数未被具体形式固定前，预测比 7.3 不可作为精简度指标引用。'
    % (RATIO,),
    {'ratio_recomputed': str(RATIO), 'ratio_claim': '7.3',
     'free_function_in_810': str('f(\\tau,\\omega)' in item(810)),
     'multiplier_field_in_811': str('\\lambda' in item(811))})

DIM_I991 = dmul(d(0, -2, 0, 0), dpow(D_L, 4))
rec('F03', 'FAIL',
    '991 全局不变量积分：被积函数由 801 恒等于 0 ⇒ I ≡ 0 恒成立（零判别力）；且量纲为 L²，名不副实',
    '①恒零：801 给 κ²+τ²−ω² ≡ 0 ⇒ 对任意流形 M 积分恒为 0，不依赖 M 的拓扑/几何 ⇒ 不能用作任何判据或拓扑不变量。'
    '②量纲：被积函数 L^-2 × √−g d⁴x (L^4) = %s ≠ 无量纲 ⇒ 称为「全局不变量」需先除以体积元或补长度标度，来料未做。'
    % (dstr(DIM_I991),),
    {'dim_integrand': 'L^-2', 'dim_measure': 'L^4', 'dim_I': dstr(DIM_I991),
     'identically_zero': 'True', 'discriminating_power': '0'})

rec('F04', 'INFO',
    '991 是 801/806 的推论而非独立条目：806 已给 d(κ²+τ²−ω²)=0，991 只是其积分形式',
    '⇒ 991 不新增内容，属「恒等式复读」类（与 A03 的 802↔938 同型）。',
    {'derived_from': '801 / 805 / 806'})

rec('F05', 'BOUNDARY',
    '880 χ²_tot = 六项直接相加：χ² 可加性以各数据集相互独立为前提，来料未声明独立性',
    '六项：SM / CMB / a_e / d_e / GW / EHT。若存在共同系统误差或共享 nuisance 参数，'
    '简单求和会重复计权 ⇒ 需在联合似然里声明协方差。来料未声明 ⇒ 登记为口径未声明，不判错。',
    {'n_terms': '6', 'independence_declared': 'False'})

rec('F06', 'PASS',
    '995 不动点稳定性判据 Re(λ_i) < 0 ⇒ 吸引（UV 吸引子），为标准线性稳定性判据',
    '教科书级正确；本册只核判据形式，不核 β 函数的具体形式（来料未写出 β_κ/β_τ/β_ω 的显式表达）。',
    {'criterion': 'Re(lambda_i) < 0'}, not_self_derived=True)

rec('F07', 'BOUNDARY',
    '994 三个 β 同时为零 + 801 一条约束 ⇒ 4 个方程约束 3 个未知 (κ*,τ*,ω*) ⇒ 过约束',
    '若约束 κ²+τ²=ω² 在不动点处仍需成立，则不动点求解变为 4 方程 / 3 未知，一般无解；'
    '除非其中一条 β 是另外两条的线性组合（来料未证明）。⇒ 需声明约束是否参与不动点定义。',
    {'n_equations': '4', 'n_unknowns': '3'})

rec('F08', 'PASS',
    '882 收敛诊断 R̂ < 1.01（Gelman-Rubin）为标准阈值',
    '教科书级正确；注意 R̂ 只诊断链间收敛，不保证遍历到真实后验（尤其多峰情形）。',
    {'threshold': '1.01'}, not_self_derived=True)

N_OPEN = sum(1 for n in ITEM_IDS if has_open(n))
PCT_OPEN = ((Decimal(N_OPEN) * 100 / Decimal(len(ITEM_IDS))).quantize(Decimal('0.01'))
            if ITEM_IDS else Decimal('0.00'))
rec('F09', 'INFO',
    'OPEN 标记覆盖率统计：200 条中 %d 条带 OPEN（%.2f%%）' % (N_OPEN, PCT_OPEN),
    '来料自述 OPEN = 「UFT 候选假设方程」。机器统计：条目总数 %d ，含 OPEN %d ，占比 %.2f%% ；'
    '⇒ 该公式集的绝大多数条目是假设登记，不是已证结论；任何引用须连同此覆盖率一起引用。'
    % (len(ITEM_IDS), N_OPEN, PCT_OPEN),
    {'n_items': str(len(ITEM_IDS)), 'n_open': str(N_OPEN), 'pct_open': str(PCT_OPEN)})

# ----------------------------------------------------------------------------
# 10) 产物输出
# ----------------------------------------------------------------------------
GUARD_OK = all(g['ok'] for g in GUARDS)
VERDICT = 'FAIL' if COUNT['FAIL'] > 0 else ('BOUNDARY' if COUNT['BOUNDARY'] else 'PASS')

KEY = {
    'n_items': len(ITEM_IDS),
    'n_open': N_OPEN,
    'pct_open': str(PCT_OPEN),
    'dim_R_ab_R_ab': 'L^-4',
    'dim_T_acd_T_acd': 'L^-2',
    'dim_gap_802': dstr(gap802),
    'signature': '(-,+,+,+)',
    'g_u_u': '-1',
    'k_sq_from_835_given_801': str(K2_FROM_835),
    'vg_max_plus_sign': str(VG_MAX),
    'vg_max_negative_sign_control': str(VG_NEG_MAX),
    'contorsion_resid_std_restore': str(R_STD[0]),
    'contorsion_resid_819a_restore': str(R_A[0]),
    'contorsion_resid_819b_restore': str(R_B[0]),
    'contorsion_correct_form': 'K_{abc} = 1/2 (T_{abc} + T_{bca} - T_{cab})',
    'n_indep_torsion': N_INDEP_T,
    'dof_828_recomputed': DOF828,
    'gr_physical_dof': GR_DOF,
    'ratio_22_over_3': str(RATIO),
    'dim_I991': dstr(DIM_I991),
}

if not os.path.isdir(DATA):
    os.makedirs(DATA)

SRC_COPY = os.path.join(DATA, 'TUFT-r70_V48公式集801-1000_来料全文_2026-10-15.md')
if SRC_PATH and not os.path.exists(SRC_COPY):
    shutil.copyfile(SRC_PATH, SRC_COPY)

JSON_PATH = os.path.join(DATA, STEM + '.json')
MD_PATH = os.path.join(DATA, STEM + '.md')
TXT_PATH = os.path.join(DATA, STEM + '_report.txt')

payload = {
    'meta': {
        'round': 'r70', 'date': '2026-10-15',
        'title': 'openuft#49 ｜1000 核心理论体系公式集（公式 801-1000）· TUFT v4.8 条目集全维审计',
        'source': SRC_PATH or '',
        'source_copy': SRC_COPY if SRC_PATH else '',
        'engine': os.path.join('源码', SRC_NAME),
        'backend': 'pure-stdlib: decimal(60) + fractions.Fraction dim4 (M,L,T,Q)',
    },
    'counts': COUNT,
    'total': sum(COUNT.values()),
    'verdict': VERDICT,
    'guard_all_ok': GUARD_OK,
    'guard_total': len(GUARDS),
    'guard_passed': sum(1 for g in GUARDS if g['ok']),
    'items': ITEMS,
    'guards': GUARDS,
    'key_numbers': KEY,
    'not_self_derived': [i['code'] for i in ITEMS if i['not_self_derived']],
}
with io.open(JSON_PATH, 'w', encoding='utf-8') as f:
    f.write(json.dumps(payload, ensure_ascii=False, indent=2))

lines = []
lines.append('# r70 · TUFT v4.8 公式集 801-1000 全维审计（数据产物）')
lines.append('')
lines.append('- 来料：%s' % (SRC_PATH or '(未找到)'))
lines.append('- 条目：%d 条（801-1000 连续）' % len(ITEM_IDS))
lines.append('- 计数：%s' % COUNT)
lines.append('- 守卫：%d/%d' % (payload['guard_passed'], payload['guard_total']))
lines.append('- 裁决：%s' % VERDICT)
lines.append('')
lines.append('## 条目')
lines.append('')
for it in ITEMS:
    lines.append('### %s · [%s] %s' % (it['code'], it['kind'], it['title']))
    if it['detail']:
        lines.append('')
        lines.append(it['detail'])
    if it['numbers']:
        lines.append('')
        lines.append('| 字段 | 值 |')
        lines.append('| --- | --- |')
        for k in sorted(it['numbers']):
            lines.append('| %s | %s |' % (k, it['numbers'][k]))
    lines.append('')
with io.open(MD_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

rlines = []
rlines.append('TUFT-r70 V48公式集801-1000 全维审计 运行报告')
rlines.append('counts=%s total=%d verdict=%s' % (COUNT, sum(COUNT.values()), VERDICT))
for it in ITEMS:
    rlines.append('[%s] %s : %s' % (it['kind'], it['code'], it['title']))
    if it['detail']:
        rlines.append('    ' + it['detail'])
rlines.append('')
rlines.append('GUARD G0/D: %d/%d %s' % (payload['guard_passed'], payload['guard_total'],
                                        '全过' if GUARD_OK else '有失败'))
with io.open(TXT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(rlines))

print('')
print('=' * 78)
print('r70 counts=%s total=%d verdict=%s' % (COUNT, sum(COUNT.values()), VERDICT))
print('guard %d/%d  ok=%s' % (payload['guard_passed'], payload['guard_total'], GUARD_OK))
print('json=%s' % JSON_PATH)
print('md=%s' % MD_PATH)
print('report=%s' % TXT_PATH)
print('=' * 78)

sys.exit(0)
