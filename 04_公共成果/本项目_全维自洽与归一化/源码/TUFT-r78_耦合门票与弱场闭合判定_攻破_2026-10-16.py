# -*- coding: utf-8 -*-
"""TUFT r76：V4.8 修正最小模型的耦合门票与弱场可检验性闭合判定（攻破）

纯标准库：Decimal(60) + Fraction 三元组量纲 (M,L,T)。
受理：r69->r71->r73->r74 修正后的最小作用量；疑问=它到底能不能给出引力。
"""
import json
import os
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60

class Dim(object):
    """(M, L, T) 指数三元组。相乘=指数相加；异构相加抛 TypeError。"""

    def __init__(self, m=0, l=0, t=0):
        self.v = (F(m), F(l), F(t))

    def __repr__(self):
        return 'Dim%s' % (str(tuple(str(x) for x in self.v)),)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __pow__(self, e):
        e = F(e)
        return Dim(*[x * e for x in self.v])

    def __eq__(self, o):
        return tuple(self.v) == tuple(o.v)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash(tuple(self.v))

    def is_dimless(self):
        return all(x == 0 for x in self.v)


def dstr(d):
    parts = []
    for x, s in zip(d.v, ('M', 'L', 'T')):
        if x == 0:
            continue
        parts.append('%s^%s' % (s, str(x)))
    return '1' if not parts else ' '.join(parts)


D_M = Dim(1, 0, 0)
D_L = Dim(0, 1, 0)
D_T = Dim(0, 0, 1)
D_NONE = Dim(0, 0, 0)

C_BASE = {
    'hbar': D_M * D_L ** 2 / D_T,
    'c': D_L / D_T,
    'G': D_L ** 3 / (D_M * D_T ** 2),
}


def enum_dim(base, target, lo=-4, hi=4, step=F(1)):
    """在 base 上穷举满足 target 的幂次组合。step=1/2 允许半整数幂。"""
    names = sorted(base.keys())
    out = []

    def rec(i, cur):
        if i == len(names):
            if cur == target:
                out.append(dict((n, memo[n]) for n in names))
            return
        e = F(lo)
        two = step
        while e <= F(hi):
            memo[names[i]] = e
            rec(i + 1, cur * base[names[i]] ** e)
            e += two

    memo = {}
    rec(0, D_NONE)
    return out


def fmt_sol(sol):
    ks = [k for k in sorted(sol.keys()) if sol[k] != 0]
    if not ks:
        return '1'
    return ' * '.join('%s^%s' % (k, str(sol[k])) for k in ks)


def Dc(x):
    return Decimal(str(x))


def rel(a, b):
    """相对偏差。"""
    a = Dc(a)
    b = Dc(b)
    if b == 0:
        return abs(a)
    return abs(a - b) / abs(b)


# ---------------- CODATA 锚点（外部输入，非第一性导出，登记为 NS） ----------------
HBAR = Dc('1.054571817e-34')          # J*s
C_LIT = Dc('299792458')               # m/s
G_LIT = Dc('6.67430e-11')             # m^3 kg^-1 s^-2
LP_LIT = Dc('1.616255e-35')           # m（CODATA 2018 字面值）

HBAR_C = HBAR * C_LIT
LP_CALC = (HBAR * G_LIT / (C_LIT ** 3)).sqrt()
L_P = LP_CALC


def fv(x, n=25):
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return 'NaN'


def fs(x, n=6):
    try:
        return format(Dc(x), '.%dE' % n)
    except Exception:
        return 'NaN'


E_DENS = D_M * D_L ** -1 * D_T ** -2
ENERGY = D_M * D_L ** 2 * D_T ** -2
FORCE = D_M * D_L * D_T ** -2
D_KAPPA = D_L ** -1
D_TRACE = E_DENS

PI60 = Decimal('3.14159265358979323846264338327950288419716939937510582097494')
FOURPI = PI60 * 4
SQRT_4PI = (FOURPI).sqrt()
K_STATIC = HBAR_C
C_REQ = SQRT_4PI * L_P

GUARDS = []


def G(tag, cond, detail=''):
    GUARDS.append((tag, bool(cond), detail))
    return bool(cond)


G('G0-1 [G]', D_L ** 3 / (D_M * D_T ** 2) == C_BASE['G'], dstr(C_BASE['G']))
G('G0-2 [hbar]', D_M * D_L ** 2 / D_T == C_BASE['hbar'], dstr(C_BASE['hbar']))
G('G0-3 [c]', D_L / D_T == C_BASE['c'], dstr(C_BASE['c']))
G('G0-4 能量密度', E_DENS == ENERGY / D_L ** 3, dstr(E_DENS))
G('G0-5 力 != 能量', FORCE != ENERGY, '%s vs %s' % (dstr(FORCE), dstr(ENERGY)))
G('G0-6 [hbar c]', C_BASE['hbar'] * C_BASE['c'] == D_M * D_L ** 3 * D_T ** -2,
  dstr(C_BASE['hbar'] * C_BASE['c']))
G('G0-7 l_P^2', C_BASE['hbar'] * C_BASE['G'] * C_BASE['c'] ** -3 == D_L ** 2,
  dstr(C_BASE['hbar'] * C_BASE['G'] * C_BASE['c'] ** -3))

try:
    D_L + D_T
    G('G0-8 异构相加须抛错', False, '未抛 TypeError')
except TypeError:
    G('G0-8 异构相加须抛错', True, 'TypeError 已抛出')

LP_REL = rel(LP_CALC, LP_LIT)
G('G0-9 l_P 计算 vs 字面', LP_REL < Decimal('1e-4'), 'rel=%s' % fs(LP_REL))

KIN = C_BASE['hbar'] * C_BASE['c'] * D_KAPPA ** 2 * D_L ** -2
G('G0-10 [(hbar c/2)(grad kappa)^2] = 能量密度', KIN == E_DENS, dstr(KIN))

C1_DIM = E_DENS / (D_KAPPA * D_TRACE)
G('G0-11 [C_1] = L', C1_DIM == D_L, dstr(C1_DIM))
G('G0-12 [C_n] = L^n', E_DENS / (D_KAPPA ** 3 * D_TRACE) == D_L ** 3, dstr(D_L ** 3))

SOL_INT_L = enum_dim(C_BASE, D_L, -4, 4, F(1))
SOL_HALF_L = enum_dim(C_BASE, D_L, -4, 4, F(1, 2))
SOL_INT_HBAR = enum_dim(C_BASE, C_BASE['hbar'], -4, 4, F(1))
SOL_INT_HBARC = enum_dim(C_BASE, C_BASE['hbar'] * C_BASE['c'], -4, 4, F(1))
SOL_INT_L2 = enum_dim(C_BASE, D_L ** 2, -4, 4, F(1))

G('G0-13 整数幂 target=L 命中 0', len(SOL_INT_L) == 0, 'hits=%d' % len(SOL_INT_L))
G('G0-14 半幂 target=L 命中 1', len(SOL_HALF_L) == 1, 'hits=%d' % len(SOL_HALF_L))
G('G0-15 阳性对照 [hbar] 非空', len(SOL_INT_HBAR) >= 1, 'hits=%d' % len(SOL_INT_HBAR))
G('G0-16 阳性对照 [hbar c] 非空', len(SOL_INT_HBARC) >= 1, 'hits=%d' % len(SOL_INT_HBARC))
G('G0-17 阳性对照 L^2 非空', len(SOL_INT_L2) >= 1, 'hits=%d' % len(SOL_INT_L2))
LP_SOL = SOL_HALF_L[0] if SOL_HALF_L else None
G('G0-18 半幂唯一解 sqrt(hbar G/c^3)',
  LP_SOL == {'hbar': F(1, 2), 'c': F(-3, 2), 'G': F(1, 2)},
  fmt_sol(LP_SOL) if LP_SOL else 'none')

G_EFF = (C_REQ ** 2) * (C_LIT ** 3) / (FOURPI * HBAR)
G_REL = rel(G_EFF, G_LIT)
G('G0-19 G_eff==G（xi=sqrt(4pi)）', G_REL < Decimal('1e-45'), 'rel=%s' % fs(G_REL))

ELL_REQ = (FOURPI * HBAR * G_LIT / (C_LIT ** 3)).sqrt()
G('G0-20 新长度被观测唯一锁定', rel(ELL_REQ, C_REQ) < Decimal('1e-45'),
  'rel=%s' % fs(rel(ELL_REQ, C_REQ)))
G('G0-21 C_req/l_P = sqrt(4pi)', rel(C_REQ / L_P, SQRT_4PI) < Decimal('1e-45'),
  'ratio=%s' % fs(C_REQ / L_P))
G_EFF_DIM = (D_L ** 2) * (D_L / D_T) ** 3 / (D_M * D_L ** 2 / D_T)
G('G0-22 G_eff 量纲 = [G]', C_BASE['G'] == G_EFF_DIM, dstr(G_EFF_DIM))

GAP_ORIG = E_DENS / ((C_BASE['hbar'] / C_BASE['c']) * D_KAPPA ** 2 * D_L ** -2)
G('G0-23 原式 hbar/(2c) 缺口 = c^2', GAP_ORIG == D_L ** 2 * D_T ** -2, dstr(GAP_ORIG))
BAD = (C_BASE['hbar'] * C_BASE['c'] / (D_L ** 2)) * D_KAPPA ** 2 * D_L ** -2
G('G0-24 hbar c/l_0^2 版仍差 L^2', E_DENS / BAD == D_L ** 2, dstr(E_DENS / BAD))
KN = HBAR_C / (L_P ** 2)
G('G0-25 hbar c/l_P^2 == c^4/G', rel(KN, C_LIT ** 4 / G_LIT) < Decimal('1e-45'),
  'rel=%s' % fs(rel(KN, C_LIT ** 4 / G_LIT)))

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
INC = os.path.join(DATA, 'TUFT-r70_V48公式集801-1000_来料全文_2026-10-15.md')

INC_TEXT = ''
INC_OK = False
if os.path.isfile(INC):
    INC_TEXT = open(INC, encoding='utf-8', errors='replace').read()
    INC_OK = True

TOK_MISS = ['牛顿', 'Newton', '弱场', '源项', 'J_\\kappa']
TOK_CTRL = ['引力', '挠率']
CNT_MISS = dict((k, INC_TEXT.count(k)) for k in TOK_MISS)
CNT_CTRL = dict((k, INC_TEXT.count(k)) for k in TOK_CTRL)

G('G0-26 来料正本可读', INC_OK and len(INC_TEXT) > 1000, 'len=%d' % len(INC_TEXT))
G('G0-27 阳性对照计数非恒零', sum(CNT_CTRL.values()) > 0, str(CNT_CTRL))
G('G0-28 缺失项计数为 0', sum(CNT_MISS.values()) == 0, str(CNT_MISS))

ITEMS = []


def IT(code, kind, title, detail):
    ITEMS.append({'id': code, 'kind': kind, 'title': title, 'detail': detail})


def P(code, title, detail):
    IT(code, 'PASS', title, detail)


def F_(code, title, detail):
    IT(code, 'FAIL', title, detail)


def B(code, title, detail):
    IT(code, 'BOUNDARY', title, detail)


def I(code, title, detail):
    IT(code, 'INFO', title, detail)


def M(code, title, detail):
    IT(code, 'MISMATCH', title, detail)

I('I01', '受理事实：801-1000 正本内无牛顿极限、无弱场、无源项、无 J_kappa',
  '机器计数 %s，阳性对照 %s；全集唯一涉及能动张量的是 824 号「nabla^a T_ab^tot = 0」。'
  % (str(CNT_MISS), str(CNT_CTRL)))

F_('I02', '耦合门票缺失：kappa 与物质之间无任何耦合项',
  '一个场要「给出引力」必须先有与 T_{mu nu} 的耦合项；该集合只有 824 的守恒律，'
  '没有耦合项、没有弱场展开、没有牛顿极限定理。这是「未完成统一场论」最直接的一条证据。')

P('I03', '最小耦合项的量纲定价：线性耦合系数 [C_1] = L',
  ('要求 [L_int] = 能量密度 %s、[kappa] = %s、[T] = %s，则线性耦合 -C_1 kappa T 的 '
   '[C_1] = %s；一般 -C_n kappa^n T 给 [C_n] = L^n。'
   % (dstr(E_DENS), dstr(D_KAPPA), dstr(D_TRACE), dstr(C1_DIM))))

F_('I04', '耦合系数排除定理：{hbar, c, G} 整数幂构造不出长度，半幂唯一解就是 l_P',
  ('整数幂穷举（幂域 [-4,4]，共 729 组）命中 %d 组；允许半幂后唯一解 %s，即 sqrt(hbar G / c^3) = l_P。'
   '⇒ 耦合系数只能是一个长度，而框架内唯一的长度由 G 通过 l_P 提供 ⇒ 必须输入 G。'
   % (len(SOL_INT_L), fmt_sol(LP_SOL))))

B('I05', '复现牛顿 G 是重排而非预言：C_req = sqrt(4pi) l_P，代回 G_eff 与 G 机器零',
  ('G_eff = C^2 c^3 / (4 pi hbar)；取 C = C_req = %s m，得 G_eff = %s，与 CODATA G = %s '
   '相对偏差 %s（机器零）。但 l_P^2 = hbar G / c^3 ⇒ G 是输入不是输出，属「普朗克锚定循环」同族。'
   % (fv(C_REQ), fv(G_EFF), fv(G_LIT), fv(G_REL))))

B('I06', '若改用「新基本长度」ell，观测把它唯一锁定为 sqrt(4pi) l_P：自由度 0、预测力 0',
  ('由 G_eff = G 反解 ell = sqrt(4 pi hbar G / c^3) = sqrt(4 pi) l_P = %s m，与 C_req 相对偏差 %s。'
   '⇒ 新常数不带来任何自由度（被实验唯一确定），但也不带来任何预测（G 仍是外部输入）；'
   '其中的 sqrt(4 pi) 是格林函数归一化约定，非物理常数。'
   % (fv(ELL_REQ), fv(rel(ELL_REQ, C_REQ)))))

GAMMA_SCALAR = Decimal('-1')
CASSINI_LIM = Decimal('2.3e-5')
GAMMA_GAP = abs(GAMMA_SCALAR - Decimal('1'))
CASSINI_RATIO = GAMMA_GAP / CASSINI_LIM
DEFL_GR = Decimal('1.75')
DEFL_SCALAR = Decimal('0')
G('G0-29 纯标量超 Cassini 限 4 个量级以上', CASSINI_RATIO > Decimal('1e4'),
  'ratio=%s' % fs(CASSINI_RATIO))

D07 = ('单标量只与 T 的迹耦合，电磁场 T^mu_mu = 0 ⇒ PPN gamma = %s ⇒ 零偏折'
       '（(1+gamma)/2 x 1.75 角秒 = %s 角秒），而 GR/实测为 %s 角秒；|gamma - 1| = %s，'
       'Cassini 限 %s ⇒ 超 %s 倍。'
       '（Cassini 限与 1.75 角秒为外部实验事实，登记为 NS，不自推）')
D07 = D07 % (str(GAMMA_SCALAR), str(DEFL_SCALAR), str(DEFL_GR),
             str(GAMMA_GAP), str(CASSINI_LIM), fs(CASSINI_RATIO))
F_('I07', '纯标量中介被光线偏折排除：PPN gamma = -1，超 Cassini 限 %s 倍'
  % fs(CASSINI_RATIO), D07)

B('I08', '力的方向在集合内未定义：耦合项的符号与整体归一化均未声明',
  '两条号差约定下 T 的迹反号（(-,+,+,+) 给 T = -eps，(+,-,-,-) 给 T = +eps），'
  '而 801-1000 既未写 L_int 的形式也未写其符号；'
  '⇒ 即使按本册补上系数，吸引还是排斥仍是未声明输入。'
  '（同 r72 号差、r73 测度约定型的「口径缺失」，不代判哪一支）')

F_('I09', '三条出路在 Omega5 内无一闭合（本册承重裁定）',
  'W1 把 kappa,tau 降为度规派生量（退化为 GR）：新常数 0，但框架失去本原性，相对 GR 零新增内容；'
  'W2 保留 kappa 传播并加张量扇区（标量-张量）：要过 Cassini 必须屏蔽，屏蔽机制需 +1 个自由函数'
  '（按 r15 口径，函数比常数更贵，直接撞 Omega5，且并入 r72 已记的 >=3 常数账）；'
  'W3 保持纯标量：已被 I07 排除。⇒ 「给出引力」这一步在当前公设集内没有零代价解。')

I('I10', '非线性耦合族同样要输入 G：kappa^n T 的系数 [C_n] = L^n，每升一阶多一个 l_P 幂',
  'n = 1 需 L、n = 2 需 L^2 = l_P^2 = hbar G / c^3、n = 3 需 L^3 = l_P^3 = (hbar G / c^3)^{3/2}；'
  '阶数越高，G 的幂次越高，循环自洽的依赖越强，且不改变「无耦合项」这一原始缺口。')

P('I11', '独立引擎复现 r73 三条核心读数（交叉印证，非引用）',
  ('原式 hbar/(2c) 的缺口 = %s（不是 [s^-2]）；来料修正 hbar c / l_0^2 版仍差 %s；'
   'hbar c / l_P^2 与 c^4/G 逐位同源（相对偏差 %s）。三条均由本册独立引擎重算得到。'
   % (dstr(GAP_ORIG), dstr(E_DENS / BAD), fv(rel(KN, C_LIT ** 4 / G_LIT)))))

I('I12', '精度与口径登记：l_P 计算值 %s m 与 CODATA 字面值 %s m 相对偏差 %s',
  ('l_P 计算值 = %s m，CODATA 字面值 = %s m，相对偏差 = %s。'
   '该偏差来自输入常数（G 只有 6 位有效数字）而非判据；本册所有判定均取相对判据，'
   '不把该量级的差异当作物理结论。' % (fv(LP_CALC), fv(LP_LIT), fv(LP_REL))))

P('I13', '阳性对照组汇总（证明各判据非恒真/非恒零）',
  ('计数判据：%s 非零 ⇒ 计数器工作；穷举判据：target=[hbar] 命中 %d、[hbar c] 命中 %d、'
   'L^2 命中 %d 而 L 整数幂命中 %d ⇒ 穷举器有分辨力；'
   '符号判据：力 != 能量、异构相加抛 TypeError ⇒ 量纲工具自守有效。'
   % (str(CNT_CTRL), len(SOL_INT_HBAR), len(SOL_INT_HBARC), len(SOL_INT_L2), len(SOL_INT_L))))

KEY = {
    'l_p_calc_m': fv(LP_CALC),
    'l_p_literal_m': fv(LP_LIT),
    'l_p_rel_dev': fv(LP_REL),
    'c_req_m': fv(C_REQ),
    'ell_req_m': fv(ELL_REQ),
    'sqrt_4pi': fv(SQRT_4PI),
    'g_eff': fv(G_EFF),
    'g_literal': fv(G_LIT),
    'g_eff_rel_dev': fv(G_REL),
    'hbc_over_lp2': fv(KN),
    'c4_over_G': fv(C_LIT ** 4 / G_LIT),
    'enum_int_len_hits': len(SOL_INT_L),
    'enum_half_len_hits': len(SOL_HALF_L),
    'enum_half_len_solution': fmt_sol(LP_SOL),
    'enum_hbar_hits': len(SOL_INT_HBAR),
    'enum_hbarc_hits': len(SOL_INT_HBARC),
    'enum_l2_hits': len(SOL_INT_L2),
    'dim_c1': dstr(C1_DIM),
    'dim_gap_orig': dstr(GAP_ORIG),
    'dim_gap_hbarc_over_l02': dstr(E_DENS / BAD),
    'ppn_gamma_scalar': str(GAMMA_SCALAR),
    'cassini_limit': str(CASSINI_LIM),
    'cassini_excess_factor': fs(CASSINI_RATIO),
    'deflection_scalar_arcsec': str(DEFL_SCALAR),
    'deflection_gr_arcsec': str(DEFL_GR),
    'incoming_missing_counts': CNT_MISS,
    'incoming_control_counts': CNT_CTRL,
}

NS = [
    'NS1：Cassini 的 |gamma-1| < 2.3e-5 限与太阳临边 1.75 角秒偏折为外部实验事实，本册引用不自推。',
    'NS2：PPN gamma = -1 属纯标量（Nordstrom 型）引力的教科书结论，本册引用不自推。',
    'NS3：kappa 与 T_{mu nu} 的耦合形式为本册为定价而构造的最小候选，来料原文未给出，不自推其物理意图。',
    'NS4：CODATA 的 hbar / c / G / l_P 为实验测量值，非第一性导出。',
    'NS5：屏蔽机制（chameleon / Vainshtein）是否能在标量-张量中救回 gamma=1，本册只记代价不建模。',
]

NAME = 'TUFT-r78_耦合门票与弱场闭合判定_攻破_2026-10-16'


def tally():
    d = {}
    for it in ITEMS:
        d[it['kind']] = d.get(it['kind'], 0) + 1
    return d


def main():
    cnt = tally()
    guard_ok = all(x[1] for x in GUARDS)
    guard_n = len(GUARDS)
    guard_pass = sum(1 for x in GUARDS if x[1])
    verdict = 'FAIL' if cnt.get('FAIL', 0) > 0 else 'PASS'

    payload = {
        'round': 'r78',
        'date': '2026-10-16',
        'topic': 'V4.8 修正最小模型的耦合门票与弱场可检验性闭合判定',
        'items': ITEMS,
        'counts': cnt,
        'total': len(ITEMS),
        'verdict': verdict,
        'guards': [{'tag': t, 'ok': ok, 'detail': d} for t, ok, d in GUARDS],
        'guard_all_ok': guard_ok,
        'guard_total': guard_n,
        'guard_pass': guard_pass,
        'key_numbers': KEY,
        'not_self_derived': NS,
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    jp = os.path.join(DATA, NAME + '.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    lines = []
    lines.append('# ' + NAME)
    lines.append('')
    lines.append('- 条目 %d：%s' % (len(ITEMS), ' / '.join(
        '%s %d' % (k, cnt[k]) for k in sorted(cnt.keys()))))
    lines.append('- verdict: %s · 守卫 %d/%d' % (verdict, guard_pass, guard_n))
    lines.append('')
    for it in ITEMS:
        lines.append('## %s · %s · %s' % (it['id'], it['kind'], it['title']))
        lines.append('')
        lines.append(it['detail'])
        lines.append('')
    lines.append('## 数值档案')
    lines.append('')
    for k in sorted(KEY.keys()):
        lines.append('- %s = %s' % (k, str(KEY[k])))
    lines.append('')
    lines.append('## 不自推')
    lines.append('')
    for s in NS:
        lines.append('- ' + s)
    lines.append('')
    mp = os.path.join(DATA, NAME + '.md')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    rep = []
    rep.append('TUFT r76 report')
    rep.append('items=%d %s' % (len(ITEMS), cnt))
    rep.append('guards=%d/%d ok=%s' % (guard_pass, guard_n, guard_ok))
    rep.append('verdict=%s' % verdict)
    for t, ok, d in GUARDS:
        rep.append('%s %s | %s' % ('OK ' if ok else 'BAD', t, d))
    rp = os.path.join(DATA, NAME + '_report.txt')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rep) + '\n')

    print('items=%d %s' % (len(ITEMS), cnt))
    print('guards=%d/%d' % (guard_pass, guard_n))
    print('verdict=%s' % verdict)
    print('C_req=%s m' % fv(C_REQ))
    print('G_eff=%s rel=%s' % (fv(G_EFF), fv(G_REL)))
    print('cassini_excess=%s' % fs(CASSINI_RATIO))
    return 0 if guard_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

B('I08', '力的方向在当前集合内未定义：耦合符号与整体归一化均未声明',
  '两条号差约定下 T 的迹反号（(-,+,+,+) 给 T = -eps，(+,-,-,-) 给 T = +eps），'
  '而 801-1000 既未写 L_int 的形式也未写其符号 ⇒ 即使按本册补上系数，'
  '吸引还是排斥仍是一个未声明输入（同 r72 号差、r73 测度约定型的「口径缺失」）。')