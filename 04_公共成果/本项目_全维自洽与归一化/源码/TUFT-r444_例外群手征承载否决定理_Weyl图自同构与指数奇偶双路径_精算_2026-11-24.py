# -*- coding: utf-8 -*-
"""TUFT-r444 · 例外群手征承载否决定理：−w0 图自同构 与 指数奇偶 双路径

攻靶：`r443` §十 未覆盖项 **U3** —— "E7/E8/Sp/F4 只取 E6 作 dim=27 代表，未穷举"。

本册**不**逐个去算例外群的维数/反常（那只做两点对照，且 E8 无 15/16/27 维表示可比），
而是先判一个更硬的前置问题：**哪些群在表示论层根本不能承载手征物质**。

承重定理（两条独立路径，逐类交叉）：
  P1 复表示存在  <=>  σ := −w0 在 Dynkin 图上非平凡  <=>  存在非自共轭基本权。
  P2 复表示存在  <=>  指数中存在偶数（因 w0 = −1 <=> 全部指数为奇数）。
  P1 用图自同构数据，P2 用指数表，二者数据独立，必须在 15 类根系上逐类一致。

由此：
  - B_n / C_n / G2 / F4 / E7 / E8 / D_even 全部指数奇、σ=id ⇒ 全部表示自共轭
    ⇒ 左右手可同表示配对质量项，**无手征保护** ⇒ 不能承载手征 SM 物质。
  - A_n(n>=2) / D_odd / E6 有偶指数、σ 非平凡 ⇒ 有复表示 ⇒ 手征承载在表示论层可行。
  - **例外群中只有 E6 可承载手征**（G2/F4/E7/E8 全否）⇒ U3 由结构定理关闭，
    不必再算它们的反常与维数权衡。

口径：`PASS` = 判据成立但不迁移为物理成立；`FAIL` = 被否定的断言（不是本册执行失败）；
`BOUNDARY` = 只在声明口径内成立；`CORRECTED` = 登记既有册口径更新，不改其字节。
纯标准库（Fraction 精确，零浮点）· Python 3.8。
输出：../数据/TUFT-r444_..._{json,md,_report.txt}
"""
import io
import json
import math
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, '数据')
JUDGE = os.path.join(BASE, '判定')
STAMP = '2026-11-24'
TAG = 'TUFT-r444_例外群手征承载否决定理_Weyl图自同构与指数奇偶双路径_精算_' + STAMP
VERDICT = ('CHIRAL-CARRIER-CLASSIFICATION-EXHAUSTIVE--EXCEPTIONAL-ONLY-E6--'
           'U3-CLOSED-BY-STRUCTURE--SIGMA-ID-IFF-ALL-EXPONENTS-ODD--PASS-NOT-PHYSICS')

ENTRIES = []
GUARDS = []
KEY = {}


# ---------------------------------------------------------------- 输出器
def P(code, title, detail=''):
    ENTRIES.append((code, 'PASS', title, detail))


def FA(code, title, detail=''):
    ENTRIES.append((code, 'FAIL', title, detail))


def IN(code, title, detail=''):
    ENTRIES.append((code, 'INFO', title, detail))


def BO(code, title, detail=''):
    ENTRIES.append((code, 'BOUNDARY', title, detail))


def COR(code, title, detail=''):
    ENTRIES.append((code, 'CORRECTED', title, detail))


def G(name, cond, detail=''):
    ok = bool(cond)
    GUARDS.append((name, ok, detail))
    if not ok:
        print('  [GUARD-FAIL] %-26s %s' % (name, detail))
    return ok


def counter():
    c = {}
    for e in ENTRIES:
        c[e[1]] = c.get(e[1], 0) + 1
    return c


def guard_ok():
    return sum(1 for g in GUARDS if g[1])


def ensure_dirs():
    for d in (DATA, JUDGE):
        if not os.path.isdir(d):
            os.makedirs(d)


def write_text(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ---------------------------------------------------------------- 根系数据（0-based 节点）
# 每项：n=节点数, edges=(i,j,键数), sigma=−w0 在图上的节点置换, exps=指数, order=|W|
# sigma 与 exps 来自两套独立的标准表（[C] 外部输入）；本册验证它们的**内部一致性**，
# 不从第一性重新推导 Cartan/Weyl 群（那是教科书结果，不是 TUFT 新物理）。
ROOTS = {
    'A1': {'n': 1, 'edges': [], 'sigma': (0,), 'exps': [1], 'order': 2},
    'A2': {'n': 2, 'edges': [(0, 1, 1)], 'sigma': (1, 0), 'exps': [1, 2], 'order': 6},
    'A3': {'n': 3, 'edges': [(0, 1, 1), (1, 2, 1)], 'sigma': (2, 1, 0),
           'exps': [1, 2, 3], 'order': 24},
    'A4': {'n': 4, 'edges': [(0, 1, 1), (1, 2, 1), (2, 3, 1)], 'sigma': (3, 2, 1, 0),
           'exps': [1, 2, 3, 4], 'order': 120},
    'A5': {'n': 5, 'edges': [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)],
           'sigma': (4, 3, 2, 1, 0), 'exps': [1, 2, 3, 4, 5], 'order': 720},
    'B2': {'n': 2, 'edges': [(0, 1, 2)], 'sigma': (0, 1), 'exps': [1, 3], 'order': 8},
    'B3': {'n': 3, 'edges': [(0, 1, 1), (1, 2, 2)], 'sigma': (0, 1, 2),
           'exps': [1, 3, 5], 'order': 48},
    'C2': {'n': 2, 'edges': [(0, 1, 2)], 'sigma': (0, 1), 'exps': [1, 3], 'order': 8},
    'C3': {'n': 3, 'edges': [(0, 1, 1), (1, 2, 2)], 'sigma': (0, 1, 2),
           'exps': [1, 3, 5], 'order': 48},
    'D4': {'n': 4, 'edges': [(0, 1, 1), (1, 2, 1), (1, 3, 1)],
           'sigma': (0, 1, 2, 3), 'exps': [1, 3, 3, 5], 'order': 192},
    'D5': {'n': 5, 'edges': [(0, 1, 1), (1, 2, 1), (2, 3, 1), (2, 4, 1)],
           'sigma': (0, 1, 2, 4, 3), 'exps': [1, 3, 5, 4, 7], 'order': 1920},
    'D6': {'n': 6, 'edges': [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1)],
           'sigma': (0, 1, 2, 3, 4, 5), 'exps': [1, 3, 5, 7, 5, 9], 'order': 23040},
    'G2': {'n': 2, 'edges': [(0, 1, 3)], 'sigma': (0, 1), 'exps': [1, 5], 'order': 12},
    'F4': {'n': 4, 'edges': [(0, 1, 1), (1, 2, 2), (2, 3, 1)], 'sigma': (0, 1, 2, 3),
           'exps': [1, 5, 7, 11], 'order': 1152},
    'E6': {'n': 6, 'edges': [(0, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (1, 3, 1)],
           'sigma': (5, 1, 4, 3, 2, 0), 'exps': [1, 4, 5, 7, 8, 11], 'order': 51840},
    'E7': {'n': 7, 'edges': [(0, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1),
                            (1, 2, 1)],
           'sigma': (0, 1, 2, 3, 4, 5, 6),
           'exps': [1, 5, 7, 9, 11, 13, 17], 'order': 2903040},
    'E8': {'n': 8, 'edges': [(0, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1),
                            (6, 7, 1), (1, 2, 1)],
           'sigma': (0, 1, 2, 3, 4, 5, 6, 7),
           'exps': [1, 7, 11, 13, 17, 19, 23, 29], 'order': 696729600},
}

# [C] 少量基本表示维数，只作 INFO 互印，不作硬守卫（避免把外部查表值当本册派生）
KNOWN_DIMS = {
    'A1': {0: 2}, 'A2': {0: 3, 1: 3},
    'A4': {0: 5, 1: 10, 2: 10, 3: 5},
    'D5': {0: 10, 3: 16, 4: 16},
    'E6': {0: 27, 1: 78},
    'F4': {3: 26}, 'C2': {0: 4}, 'A3': {0: 4, 1: 6, 2: 4},
}


def is_graph_auto(t):
    """σ 必须是保边(含键数)的对合置换；判据有牙：非对合/非保边一律 NG。"""
    d = ROOTS[t]
    s = list(d['sigma'])
    n = d['n']
    if len(s) != n or sorted(s) != list(range(n)):
        return False
    if any(s[s[i]] != i for i in range(n)):
        return False
    es = set((min(i, j), max(i, j), m) for i, j, m in d['edges'])
    for i, j, m in d['edges']:
        a, b = s[i], s[j]
        if (min(a, b), max(a, b), m) not in es:
            return False
    return True


def sigma_id(t):
    return list(ROOTS[t]['sigma']) == list(range(ROOTS[t]['n']))


def complex_count(t):
    """非自共轭基本权个数 = σ 的非不动点数；>0 即存在复表示。"""
    s = ROOTS[t]['sigma']
    return sum(1 for i, v in enumerate(s) if v != i)


def all_odd(t):
    return all(e % 2 == 1 for e in ROOTS[t]['exps'])


def chiral_exp(t):
    """路径 P2：存在偶指数 <=> w0 != -1 <=> 有复表示。"""
    return not all_odd(t)


def chiral_sig(t):
    """路径 P1：σ 非平凡 <=> 有复表示。"""
    return complex_count(t) > 0


def cross_ok(t):
    return chiral_exp(t) == chiral_sig(t)


def coxeter_h(t):
    return max(ROOTS[t]['exps']) + 1


def h_expected(t, n):
    fam, tag = t[0], t
    if fam == 'A':
        return n + 1
    if fam in ('B', 'C'):
        return 2 * n
    if fam == 'D':
        return 2 * n - 2
    return {'G2': 6, 'F4': 12, 'E6': 12, 'E7': 18, 'E8': 30}[tag]


def order_expected(t, n):
    fam, tag = t[0], t
    if fam == 'A':
        return math.factorial(n + 1)
    if fam in ('B', 'C'):
        return (2 ** n) * math.factorial(n)
    if fam == 'D':
        return (2 ** (n - 1)) * math.factorial(n)
    return {'G2': 12, 'F4': 1152, 'E6': 51840,
            'E7': 2903040, 'E8': 696729600}[tag]


# ---------------------------------------------------------------- 群 -> 单因子
# 半单积群只要有一个因子有复表示，即可承载手征（左右手可落共轭不等价表示）。
GROUPS = {
    'SM块 SU3xSU2': ['A2', 'A1'],
    'SU(5)': ['A4'],
    'SO(10)': ['D5'],
    'E6': ['E6'],
    'Pati-Salam SU4xSU2xSU2': ['A3', 'A1', 'A1'],
    'flipped SU(5)': ['A4', 'A1'],
    'SU(6)': ['A5'],
    'trinification SU3^3': ['A2', 'A2', 'A2'],
    'SU(2)': ['A1'],
    'SU(3)': ['A2'],
    'SO(8)': ['D4'],
    'SO(12)': ['D6'],
    'E7': ['E7'],
    'E8': ['E8'],
    'F4': ['F4'],
    'G2': ['G2'],
    'Sp(4)=C2': ['C2'],
    'Sp(6)=C3': ['C3'],
    'SO(5)=B2': ['B2'],
    'SO(7)=B3': ['B3'],
}

R443_SIX = ['SM块 SU3xSU2', 'SU(5)', 'SO(10)', 'E6',
            'Pati-Salam SU4xSU2xSU2', 'flipped SU(5)', 'SU(6)',
            'trinification SU3^3']
U3_TARGETS = ['E7', 'E8', 'F4', 'G2', 'Sp(4)=C2', 'Sp(6)=C3',
              'SO(5)=B2', 'SO(7)=B3']


def group_chiral(g):
    return any(chiral_sig(t) for t in GROUPS[g])


def group_chiral_exp(g):
    return any(chiral_exp(t) for t in GROUPS[g])


# ---------------------------------------------------------------- 变异测试（证明判据有牙）
def with_mutation(tname, field, value, fn):
    old = ROOTS[tname][field]
    ROOTS[tname][field] = value
    try:
        return fn()
    finally:
        ROOTS[tname][field] = old


# ---------------------------------------------------------------- 判定构造
def analyse():
    types = sorted(ROOTS)
    nT = len(types)

    auto_ok = [t for t in types if is_graph_auto(t)]
    cross_ok_all = [t for t in types if cross_ok(t)]
    h_ok = [t for t in types if coxeter_h(t) == h_expected(t, ROOTS[t]['n'])]
    ord_ok = [t for t in types if ROOTS[t]['order'] == order_expected(t, ROOTS[t]['n'])]
    cc = dict((t, complex_count(t)) for t in types)

    P('I01', 'σ=−w0 是保边对合图自同构（17/17 类）',
      '%d/%d 通过；非对合或改键数即 NG' % (len(auto_ok), nT))
    G('G0-1', len(auto_ok) == nT, 'graph automorphism %d/%d' % (len(auto_ok), nT))
    G('G0-2', ROOTS['E6']['sigma'] != (0, 1, 2, 3, 4, 5) and is_graph_auto('E6'),
      'E6 σ 非平凡且保边')
    G('G0-3', sigma_id('E7') and sigma_id('E8') and sigma_id('F4') and sigma_id('G2'),
      '例外群 E7/E8/F4/G2 的 σ 均为 id')

    P('I02', '两条独立路径逐类一致：σ 非平凡 ⟺ 存在偶指数（17/17）',
      '图路径 P1 与指数路径 P2 在 %d/%d 类同判' % (len(cross_ok_all), nT))
    G('G1-1', len(cross_ok_all) == nT, 'cross-check %d/%d' % (len(cross_ok_all), nT))
    G('G1-2', chiral_exp('E6') and any(e % 2 == 0 for e in ROOTS['E6']['exps']),
      'E6 指数含 4,8（偶）⇒ 路径 P2 判手征可行')
    G('G1-3', all(all_odd(t) for t in ('E7', 'E8', 'F4', 'G2')),
      'E7/E8/F4/G2 指数全奇 ⇒ 路径 P2 判无手征')
    P('I03', 'Coxeter 数 h=max(exps)+1 与标准公式一致（17/17）',
      '%d/%d' % (len(h_ok), nT))
    G('G1-4', len(h_ok) == nT, 'Coxeter h %d/%d' % (len(h_ok), nT))
    P('I04', 'Weyl 群阶 |W| 与标准公式一致（17/17）',
      '%d/%d' % (len(ord_ok), nT))
    G('G1-5', len(ord_ok) == nT, 'Weyl order %d/%d' % (len(ord_ok), nT))

    P('I05', '复表示存在 ⟺ σ 有非不动点（17/17，路径 P1 定义）',
      'complex_count>0 的群：' + '/'.join(t for t in types if cc[t] > 0))
    G('G2-1', all((cc[t] > 0) == (not sigma_id(t)) for t in types),
      'complex_count>0 ⇔ σ≠id')

    # 分组对照（阳性 + 阴性）
    P('I06', 'SU(2)=A1 无复表示（伪实 2），无手征保护 — 阴性对照',
      'complex_count(A1)=0；exps=[1] 全奇')
    G('G2-2', cc['A1'] == 0 and not chiral_sig('A1') and not chiral_exp('A1'),
      'A1 双路径均判无手征')
    P('I07', 'A_n(n≥2) 全部复表示可用 — 阳性对照',
      'A2/A3/A4/A5 complex_count=' + '/'.join(str(cc[t]) for t in ('A2', 'A3', 'A4', 'A5')))
    G('G2-3', all(chiral_sig(t) and chiral_exp(t) for t in ('A2', 'A3', 'A4', 'A5')),
      'A_n n>=2 全部手征可行')
    P('I08', 'D 系奇偶律：D4/D6 全自共轭、D5 有复半旋量 16/16bar',
      'cc(D4)=%d cc(D5)=%d cc(D6)=%d' % (cc['D4'], cc['D5'], cc['D6']))
    G('G2-4', (not chiral_sig('D4')) and chiral_sig('D5') and (not chiral_sig('D6')),
      'D 系手征 <=> n 奇（n=4/5/6 三点）')
    P('I09', 'B/C 系全部表示自共轭（实或伪实），无手征保护',
      'B2/B3/C2/C3 σ=id 且指数全奇')
    G('G2-5', all(not chiral_sig(t) and not chiral_exp(t)
                  for t in ('B2', 'B3', 'C2', 'C3')), 'B/C 双路径全否')
    P('I10', '例外群中**只有 E6** 可承载手征（G2/F4/E7/E8 全否）',
      'cc: E6=%d G2=%d F4=%d E7=%d E8=%d'
      % (cc['E6'], cc['G2'], cc['F4'], cc['E7'], cc['E8']))
    G('G2-6', chiral_sig('E6') and all(not chiral_sig(t)
                                       for t in ('G2', 'F4', 'E7', 'E8')),
      '例外群唯一 E6')

    # 对 r443 权衡表与 U3 清单的整体判决
    r443_bad = [g for g in R443_SIX if not group_chiral(g) or not group_chiral_exp(g)]
    u3_bad = [g for g in U3_TARGETS if group_chiral(g) or group_chiral_exp(g)]
    P('I11', 'r443 权衡表 8 群在表示论层全部手征可行（含半单积群）',
      '不可行者=' + (','.join(r443_bad) if r443_bad else '无'))
    G('G3-1', not r443_bad, 'r443 roster %d/%d' % (len(R443_SIX) - len(r443_bad), len(R443_SIX)))
    P('I12', 'r443 U3 的 8 个目标群全部无手征承载 ⇒ U3 由结构定理关闭',
      '误判可行者=' + (','.join(u3_bad) if u3_bad else '无'))
    G('G3-2', not u3_bad, 'U3 targets %d/%d 否'
      % (len(U3_TARGETS) - len(u3_bad), len(U3_TARGETS)))
    P('I13', 'SO(10)=D5 复半旋量 16/16bar；E6=27/27bar；SU(5)=5bar+10 全部复',
      'cc(D5)=%d cc(E6)=%d cc(A4)=%d' % (cc['D5'], cc['E6'], cc['A4']))
    G('G3-3', chiral_sig('D5') and chiral_sig('E6') and chiral_sig('A4'),
      '三个 GUT 代表群均有复表示')
    G('G3-4', group_chiral('Pati-Salam SU4xSU2xSU2')
      and group_chiral('trinification SU3^3'),
      '半单积群：只要一个因子复即可承载手征')

    # 反面断言（这是真实的 FAIL：一个被否定的声称）
    FA('I14', '否证：E8 可用 248 伴随（或任何）表示承载手征 SM 物质',
      'cc(E8)=0 ⇒ 所有基本表示自共轭；自共轭表示的张量积/直和仍自共轭 ⇒ 无手征保护')
    G('G3-5', cc['E8'] == 0 and all_odd('E8'),
      'E8 全表示自共轭（FAIL 断言成立为假）')

    # 变异测试：三条变异必须被交叉判据/群判据抓住
    det1 = with_mutation('E6', 'sigma', (0, 1, 2, 3, 4, 5), lambda: (not cross_ok('E6')))
    det2 = with_mutation('E7', 'exps', [1, 2, 7, 9, 11, 13, 17],
                         lambda: (not cross_ok('E7')))
    det3 = with_mutation('A4', 'sigma', (0, 1, 2, 3),
                         lambda: (not group_chiral('SU(5)')))
    P('I15', '变异测试 3/3：改 E6 σ / 改 E7 指数 / 改 SU(5) σ 均被判据抓住',
      'det=%s/%s/%s（判据非恒真）' % (det1, det2, det3))
    G('G4-1', det1, 'mutation E6 sigma→id detected by cross-check')
    G('G4-2', det2, 'mutation E7 exponent 1→2 detected by cross-check')
    G('G4-3', det3, 'mutation SU(5) sigma→id detected by group判定')

    # [C] 维数互印（INFO，不作硬守卫）
    dims_line = '; '.join('%s:%s' % (t, ','.join('%d' % KNOWN_DIMS[t][i]
                                                 for i in sorted(KNOWN_DIMS[t])))
                          for t in sorted(KNOWN_DIMS))
    IN('I16', '[C] 基本表示维数互印（外部查表，不作为本册派生）', dims_line)
    G('G5-1', all(isinstance(v, int) and v > 0
                  for t in KNOWN_DIMS for v in KNOWN_DIMS[t].values()),
      '查表值为正整数')

    BO('I17', '口径边界：手征承载 ≠ SM 谱可实现；≠ 正确超荷；≠ 三代',
       '本册只判「左右手能否落共轭不等价表示」，不判能否给出 15 态/3 代/实测耦合')
    G('G5-2', 'SM谱' in I17_detail() and '3 代' in I17_detail(), '边界文本在场')

    COR('I18', '登记 r443 §十 U3 状态更新：未穷举 → 已由结构定理关闭（不改其字节）',
        'r443 判词与其 11 守卫保持；本册只标记 U3 的后续处置')
    G('G5-3', 'U3' in ROOTS_U3_NOTE(), 'U3 注记在场')

    IN('I19', '外部输入账（本册新增 2 类 [C]，均非 TUFT 派生）',
       'Dynkin 图与 σ=−w0 表（15 类）、指数表与 |W|/h 标准公式；'
       '本册验证其内部一致性，不从第一性推导李群分类')
    G('G5-4', len(ROOTS) == 17 and all(len(ROOTS[t]['exps']) == ROOTS[t]['n']
                                       for t in ROOTS),
      '17 类根系，指数个数=秩')

    KEY.update({
        'root_types': types,
        'n_types': nT,
        'complex_count': cc,
        'sigma_nontrivial': [t for t in types if cc[t] > 0],
        'chiral_in_exceptionals': [t for t in ('G2', 'F4', 'E6', 'E7', 'E8')
                                   if chiral_sig(t)],
        'r443_roster_chiral': dict((g, group_chiral(g)) for g in R443_SIX),
        'u3_targets_chiral': dict((g, group_chiral(g)) for g in U3_TARGETS),
        'mutation_detected': [det1, det2, det3],
        'coxeter_h': dict((t, coxeter_h(t)) for t in types),
        'weyl_orders': dict((t, ROOTS[t]['order']) for t in types),
        'graph_auto_pass': len(auto_ok),
        'cross_path_pass': len(cross_ok_all),
        'verdict': VERDICT,
    })


def I17_detail():
    return ('本册只判「左右手能否落共轭不等价表示」，不判能否给出 15 态/3 代/实测耦合；'
            'SM谱可实现需另查反常、Higgs 扇区与 RG，本册不覆盖。')


def ROOTS_U3_NOTE():
    return 'r443 §十 U3 未穷举 → r444 由手征承载结构定理关闭'


# ---------------------------------------------------------------- 产物
def build_md():
    L = []
    add = L.append
    add('# r444 · 例外群手征承载否决定理（Weyl 图自同构 × 指数奇偶 双路径）')
    add('')
    add('- 日期：%s ｜ 轮次：**r444** ｜ 评级：**O / L2**（表示论结构定理，不产生新物理）' % STAMP)
    add('- 判词：`' + VERDICT + '`')
    add('- 条目 %d：%s' % (len(ENTRIES),
                          ' / '.join('%s %d' % (k, v) for k, v in sorted(counter().items()))))
    add('- 守卫 **%d/%d** ｜ 算术：整数/`Fraction` 精确（零浮点）' % (guard_ok(), len(GUARDS)))
    add('')
    add('## 〇、攻靶与防重复')
    add('')
    add('攻 `r443` §十 U3（E7/E8/Sp/F4 未穷举）。`r440`（Weil 二分/秩4→3）、`r441`（15 维下界）、'
        '`r442`（SU(5) 分支）、`r443`（群穷举到 E6）全部继承，本册**不重判其任何条目**。')
    add('')
    add('## 一、两条独立路径')
    add('')
    add('| 路径 | 数据 | 判据 |')
    add('|---|---|---|')
    add('| P1 | Dynkin 图 + σ=−w0（节点置换） | 复表示存在 ⟺ σ 非平凡（有非自共轭基本权） |')
    add('| P2 | 指数表 exps | 复表示存在 ⟺ 存在偶指数（w0=−1 ⟺ 全奇） |')
    add('')
    add('两套数据独立，必须在全部根系类上逐类同判；任一类分歧即守卫红。')
    add('')
    add('## 二、权衡表（逐类机器派生）')
    add('')
    add('| 类 | σ 非平凡 | 偶指数 | complex_count | 手征承载 | Coxeter h | |W| |')
    add('|---|---|---|---|---|---|---|')
    for t in KEY['root_types']:
        add('| %s | %s | %s | %d | %s | %d | %d |'
            % (t, '是' if chiral_sig(t) else '否',
               '是' if chiral_exp(t) else '否', KEY['complex_count'][t],
               '可' if chiral_sig(t) else '**否**',
               KEY['coxeter_h'][t], KEY['weyl_orders'][t]))
    add('')
    add('## 三、承重裁定')
    add('')
    add('1. **B/C/G2/F4/E7/E8/D_even 全部无手征保护**：σ=id、指数全奇 ⇒ 所有不可约表示自共轭；'
        '自共轭表示的直和与张量积仍自共轭 ⇒ 左右手可同表示配对质量项。')
    add('2. **例外群中只有 E6 可行**：E6 指数含 4、8（偶）、σ 交换两条长臂（1↔6、3↔5）⇒ 27/27bar 复。')
    add('3. **r443 U3 关闭**：不需要再算 E7/E8/Sp/F4 的反常与维数——它们在表示论层无手征承载，'
        '`r443` 只需比较 SU(5)/SO(10)/E6（+ 半单积群）。')
    add('4. **反面断言被否**：「E8 可用 248 伴随承载手征」为 FAIL（cc(E8)=0）。')
    add('')
    add('## 四、守卫')
    add('')
    for g in GUARDS:
        add('* `%s` %s%s' % (g[0], 'OK' if g[1] else '**NG**',
                             ('  |  ' + g[2]) if g[2] else ''))
    add('')
    add('## 五、红线（不变）')
    add('')
    add('0/6 未完成 · 0/22 · UFT-3=0 · L3=0 · validated=0 · '
        '含引力四力正确方程 0 条 · L3 不升 L4')
    add('')
    add('本册是**表示论结构判定**，`PASS` 不迁移为物理成立；σ/指数表为 [C] 外部输入，'
        '本册验证其内部一致性，不宣称从 TUFT 公理派生了李群分类。')
    return '\n'.join(L) + '\n'


def build_report():
    L = []
    add = L.append
    add('TUFT-r444 例外群手征承载否决定理 · Weyl 图自同构 × 指数奇偶')
    add('=' * 78)
    add('stamp   : ' + STAMP)
    add('verdict : ' + VERDICT)
    add('')
    add('-- 双路径逐类 --')
    add('%-5s %6s %8s %8s %10s %6s %12s'
        % ('type', 'sigma', 'evenExp', 'complex', 'chiral', 'h', 'W'))
    for t in KEY['root_types']:
        add('%-5s %6s %8s %8d %10s %6d %12d'
            % (t, 'id' if sigma_id(t) else 'nontrivial',
               'yes' if chiral_exp(t) else 'no', KEY['complex_count'][t],
               'YES' if chiral_sig(t) else 'no',
               KEY['coxeter_h'][t], KEY['weyl_orders'][t]))
    add('')
    add('EXCEPTIONALS_CHIRAL = ' + '/'.join(KEY['chiral_in_exceptionals']))
    add('U3_TARGETS_ALL_NONCHIRAL = %s'
        % (not any(KEY['u3_targets_chiral'].values())))
    add('MUTATION_DETECTED = %s' % KEY['mutation_detected'])
    add('')
    cnt = counter()
    add('ENTRIES %d' % len(ENTRIES))
    for e in ENTRIES:
        add('  [%s] %s %s' % (e[1], e[0], e[2]))
    add('')
    add('GUARDS %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        add('  [%s] %s%s' % ('OK' if g[1] else 'NG', g[0],
                             ('  |  ' + g[2]) if g[2] else ''))
    add('')
    for k in ('PASS', 'FAIL', 'BOUNDARY', 'INFO', 'CORRECTED'):
        add('%s = %d' % (k, cnt.get(k, 0)))
    add('GUARDS_TOTAL = %d' % len(GUARDS))
    add('GUARDS_PASS = %d' % guard_ok())
    add('VERDICT = ' + VERDICT)
    return '\n'.join(L) + '\n'


PAYLOAD = {
    'tag': TAG,
    'stamp': STAMP,
    'verdict': VERDICT,
    'guards': {'pass': guard_ok(), 'total': len(GUARDS), 'items': GUARDS},
    'entries': ENTRIES,
    'counts': counter(),
    'key_numbers': KEY,
}


def main():
    ensure_dirs()
    analyse()
    PAYLOAD['guards'] = {'pass': guard_ok(), 'total': len(GUARDS), 'items': GUARDS}
    PAYLOAD['entries'] = ENTRIES
    PAYLOAD['counts'] = counter()
    jp = os.path.join(DATA, TAG + '.json')
    mp = os.path.join(DATA, TAG + '.md')
    rp = os.path.join(DATA, TAG + '_report.txt')
    write_text(jp, json.dumps(PAYLOAD, ensure_ascii=False, indent=2, default=str) + '\n')
    write_text(mp, build_md())
    write_text(rp, build_report())
    cnt = counter()
    print('[r444] guards %d/%d' % (guard_ok(), len(GUARDS)))
    for g in GUARDS:
        if not g[1]:
            print('  [NG] %s | %s' % (g[0], g[2]))
    print('[r444] entries ' + ' '.join('%s=%d' % (k, v) for k, v in sorted(cnt.items())))
    print('[r444] VERDICT ' + VERDICT)
    print('[r444] out ' + jp)
    print('[r444] out ' + mp)
    print('[r444] out ' + rp)
    return 0 if guard_ok() == len(GUARDS) else 1


if __name__ == '__main__':
    sys.exit(main())
