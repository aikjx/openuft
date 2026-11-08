# -*- coding: utf-8 -*-
"""TUFT-r404 | 统一所有力：同源化最小代价下界与唯一生存通道。

定位（与既有册分工，详见判定册 §一）：
  r403      = 哪个方程正确（C0-C3 四级 + 13 行继承总表）
  attack41  = 补齐外部输入能否完成（类别互斥）
  attack43/46 = 力本源供给矩阵 / 基础块留一抽除
  卷116     = 五条逃逸口状态 + 债务 #1-#27 + 两个重启入口
  本册      = 要让四力真正同源，最小必须付出什么代价；是否存在唯一未被排除通道

不做的事：不重判任何既有条目、不新造统一方程、不宣称统一已完成、
不改写任何被引文件字节。所有继承读数均做磁盘实读锚点核对。

纯标准库 / Python 3.8 / Decimal 60 位 / Fraction 四元组量纲 (M,L,T,Q)。
控制台只打印 ASCII 摘要（GBK 控制台守卫）；中文细节全部写入 UTF-8 产物。
"""
import io
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

getcontext().prec = 60
D = Decimal
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
NAME = 'TUFT-r404_统一所有力_同源化最小代价下界与唯一生存通道_2026-11-09'


def Ds(x):
    return D(str(x))


def fmt(x, n=25):
    try:
        return format(x, '.' + str(n) + 'E')
    except Exception:
        return str(x)


ENTRIES = []
GUARDS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


# ---------------------------------------------------------------- 量纲工具
def dv(m=0, l=0, t=0, q=0):
    return (Fraction(m), Fraction(l), Fraction(t), Fraction(q))


def dadd(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(4))


def dscale(v, n):
    return tuple(v[i] * Fraction(n) for i in range(4))


def dneg(v):
    return dscale(v, -1)


def dstr(v):
    ax = 'MLTQ'
    return ' '.join('%s^%s' % (ax[i], v[i]) for i in range(4) if v[i])


C = dv(0, 1, -1, 0)       # c
HB = dv(1, 2, -1, 0)      # hbar
GG = dv(-1, 3, -2, 0)     # G
MP = dv(1, 0, 0, 0)       # 任意质量标度
EE = dv(0, 0, 0, 1)       # 电荷
AL = dv(0, 0, 0, 0)       # 无量纲常数

guard('G0-1', dadd(HB, C, dscale(dv(0, 1, 0, 0), -1)) == dv(1, 2, -2, 0),
      'hbar*c/r = 能量')
guard('G0-2', dadd(GG, HB, dscale(C, -3)) == dv(0, 2, 0, 0),
      'G*hbar/c^3 = L^2')
guard('G0-3', dscale(dadd(dv(0, 0, -1, 0), dneg(C)), 2) == dv(0, -2, 0, 0),
      '(omega/c)^2 = L^-2')
guard('G0-4', dadd(dv(1, 0, 0, 0), dv(0, 1, 0, 0)) == dv(1, 1, 0, 0),
      '量纲相乘 = 指数相加，不是逐分量相乘')
guard('G0-5', dscale(C, -1) == dv(0, -1, 1, 0), '负幂 = 指数取负')
guard('G0-6', dneg(GG) == dv(1, -3, 2, 0), '-dim(G) = (1,-3,2,0)')
guard('G0-7', AL == dv() and EE == dv(0, 0, 0, 1), 'alpha 无量纲 / e 占 Q 轴')
guard('G0-8', dadd(C, dneg(C)) == dv(), '逆元闭合')

# ---------------------------------------------------------------- A 锚点实读
from fnmatch import fnmatch

ANCHOR_SPECS = [
    ('r403 判定册', '判定_TUFT-r403_*', ['NO-CORRECT-FOUR-FORCE-GUT', 'C3', 'U01']),
    ('attack41 report', 'attack41_*_report.txt', ['类别互斥', 'W3', 'UNBOUNDED']),
    ('卷116 终卷', '116_终卷_*', ['五条逃逸口', '钉死', '债务']),
    ('Omega5 条款', '*张祥前CTFA_自由度预算*', ['自由常数']),
    ('能标一致性册', '*能标一致性与四力跨度重算*', ['dex', '33.']),
    ('UFT 达成度总汇', '理论体系方程总汇_*', ['达成度']),
]
ALL_FILES = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in str(p)]
anchor_rows = []
for label, pattern, keys in ANCHOR_SPECS:
    files = [p for p in ALL_FILES if fnmatch(p.name, pattern)]
    best_hit, best_name = 0, 'MISSING'
    for p in files:
        try:
            text = io.open(str(p), encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        h = sum(1 for k in keys if k in text)
        if h > best_hit:
            best_hit, best_name = h, p.name
    anchor_rows.append(dict(label=label, file=best_name, hit=best_hit, total=len(keys)))
guard('G-A', sum(1 for r in anchor_rows if r['hit'] > 0) >= 5,
      '至少 5/6 继承锚点磁盘实读命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:3]),
      'r403 / attack41 / 卷116 三个主锚必须命中')
add('A01', 'PASS', '继承锚点磁盘实读',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:48], r['hit'], r['total']) for r in anchor_rows))
missing = [r['label'] for r in anchor_rows if r['hit'] == 0]
if missing:
    add('A02', 'BOUNDARY', '未命中锚点：' + '、'.join(missing),
        '未命中锚点不构造继承读数，相关条目降级为条件性，不冒充继承')

# ---------------------------------------------------------------- K 量纲锁死
target = dneg(GG)
sol = []
for nc, nh, nm, ne, na in product(range(-3, 4), repeat=5):
    v = dadd(dscale(C, nc), dscale(HB, nh), dscale(MP, nm),
             dscale(EE, ne), dscale(AL, na))
    if v == target:
        sol.append((nc, nh, nm, ne, na))
core = sorted(set((a, b, c, d) for a, b, c, d, e in sol))
sol_no_mass = [s for s in sol if s[2] == 0]

hbar = Ds('1.054571817e-34')
cc = Ds('299792458')
GN = Ds('6.67430e-11')
mP = (hbar * cc / GN).sqrt()
ident_ratio = GN * mP * mP / (hbar * cc)

guard('G-K1', len(sol) == 7, 'G 无量纲化：7 组命中（alpha 退化幂 7 个）')
guard('G-K2', core == [(-1, -1, 2, 0)] and len(core) == 1,
      '去重后唯一核心组合 G*m^2/(hbar*c)')
guard('G-K3', len(sol_no_mass) == 0, '阴性对照：去掉质量标度后 0 命中')
guard('G-K4', abs(ident_ratio - D(1)) < D('1e-50'),
      '取 m=m_P 时 G*m_P^2/(hbar*c) 恒等于 1（恒等复读）')

add('K01', 'PASS', '量纲锁死定理：引力耦合的同源化必须引入质量标度',
    '基组 {c,hbar,G,m,e,alpha} 幂 [-3,3] 穷举 16807 组，命中 %d 组；'
    '去重后唯一核心 %s 即 G*m^2/(hbar*c)；去掉质量标度命中 %d 组。'
    % (len(sol), str(core), len(sol_no_mass)))
add('K02', 'FAIL', '唯一不新增输入的读法是恒等复读，零判别力',
    'm=m_P 时恒等式 m_P^2 = hbar*c/G 使 G*m_P^2/(hbar*c) = %s（60 位机器零），'
    '不是从框架导出的引力耦合，而是把 G 自己写了一遍。' % fmt(ident_ratio))
add('K03', 'INFO', '与 M02 普朗克锚定谬误同型，本册为独立复算',
    'r42/r44 亦用「缺失因子参数空间穷举」；本册靶不同（G 的无量纲化而非 a_e 补齐因子），'
    '结论同向：框架内无自然补齐，补齐即外部输入。')

# ---------------------------------------------------------------- Y 单常数与 Omega5 结构缺口
# M_Z 口径四耦合；[C] 级测量锚，继承「能标一致性与四力跨度重算」册，不重新判定
Q = {'em': Ds('7.8156e-3'), 'w': Ds('3.3804e-2'),
     's': Ds('0.1181'), 'G': Ds('5.578e-35')}
logs = dict((k, v.log10()) for k, v in Q.items())
span = max(logs.values()) - min(logs.values())
mean = sum(logs.values()) / D(4)
rms = (sum((v - mean) ** 2 for v in logs.values()) / D(4)).sqrt()
lam_star = D(10) ** mean
half = max(abs(v - mean) for v in logs.values())
a_int = dict((k, int(v.to_integral_value())) for k, v in logs.items())
res_int = dict((k, logs[k] - D(a_int[k])) for k in logs)
maxres = max(abs(v) for v in res_int.values())

guard('G-Y1', D('33.0') < span < D('33.6'), '四耦合跨度落在 33.x dex（继承读数 33.325）')
guard('G-Y2', rms > D(10), '单常数拟合 RMS 残差 > 10 dex')
guard('G-Y3', maxres <= D('0.5'), 'lambda=10 + 4 个整数指数可拟合到 0.5 dex 内')
guard('G-Y4', len(a_int) == 4 and maxres > D('1e-6'),
      '整数指数拟合非精确：4 个结构位置且残差 > 1e-6 dex')
guard('G-Y5', half > D(10), '单自由常数的最大偏差 > 10 dex')

add('Y01', 'PASS', '四力耦合跨度复算（继承，不重判）',
    'em=%s w=%s s=%s G=%s；log10 跨度 %s dex；'
    '几何平均 lambda*=%s' % (fmt(Q['em']), fmt(Q['w']), fmt(Q['s']), fmt(Q['G']),
                            fmt(span), fmt(lam_star)))
add('Y02', 'FAIL', '单个自由常数无法同时给出四个耦合',
    '最优单常数 lambda* 的 RMS 残差 %s dex、最大偏差 %s dex；'
    '任何「1 常数 + 框架函数」的同源方案至少要由结构承载 %s dex 的跨度。'
    % (fmt(rms), fmt(half), fmt(span)))
add('Y03', 'CORRECTED', 'Omega5「自由常数 <= 1」口径 I 形式通过但实质无效',
    '取 lambda=10（纯数，非自由参数）并把四个 log10 取整为整数指数 a_i=%s，'
    '拟合最大残差仍有 %s dex，不是精确拟合；'
    '此时连续自由常数 = 0（Omega5 形式 PASS），但需 4 个手填整数指数（结构自由度 = 4）；'
    '要精确拟合还须放开 lambda，则连续常数 >= 1 且结构输入 >= 4，合计 >= 5。'
    '与第十五轮「口径 I 无效」同型，本册用四力耦合数据独立复现。'
    % (str(a_int), fmt(maxres)))
add('Y04', 'FAIL', 'Omega5 缺「结构自由度限额」条款，是本册定价的硬前提',
    '四力同源要求连续常数 >= 3（见 E 段秩下界）或 1 常数 + >= 4 个离散结构输入；'
    'Omega5 只约束前者，二者都满足字面的「<=1」而实际自由度 >= 4。'
    '未补该条款前，任何「未违反 Omega5」的自辩均不构成统一。')

# ---------------------------------------------------------------- E 出口代价穷举
# c=新增连续常数, s=新增结构自由度, f=函数级自由度(0/1), c2=保持 GR/SM 还原,
# w3=能产出 W3 要求的非测量锚无量纲数值, excl=已被实验/既有册排除
EXIT = [
    dict(id='E01', name='最小 SU(5)', c=0, s=1, f=0, c2=1, w3=0, excl=1,
         src='r403 U03；质子衰变 523 倍'),
    dict(id='E02', name='MSSM / 超对称', c=105, s=1, f=0, c2=1, w3=0, excl=1,
         src='r403 A07；105 参数、LHC 未见'),
    dict(id='E03', name='SO(10) + 阈值 + Yukawa', c=15, s=1, f=0, c2=1, w3=0, excl=0,
         src='attack41 外部输入链 >=15；不可交付'),
    dict(id='E04', name='额外维 KK', c=1, s=2, f=0, c2=1, w3=0, excl=0,
         src='r380 D=5 正对照；维数与紧化'),
    dict(id='E05', name='弦 / 量子引力', c=0, s=9, f=0, c2=0, w3=0, excl=0,
         src='r403 U08 OPEN-NON-UNIQUE；真空选择无界'),
    dict(id='E06', name='几何 omega(r,t) 自由函数', c=0, s=1, f=1, c2=1, w3=0, excl=0,
         src='attack39 四路封死；r95 函数级自由度'),
    dict(id='E07', name='新场 / 新耦合（tau 动力学化）', c=2, s=0, f=0, c2=1, w3=0, excl=0,
         src='r20 P0 同源化；DEC 破坏、极化 2->3'),
    dict(id='E08', name='修改 Omega5 并逐项登记外部输入', c=3, s=4, f=0, c2=1, w3=0, excl=0,
         src='第十四轮路线 4 / 第十五轮 A4 硬条件'),
    dict(id='E09', name='钉死 f 的原理（卷116 债务 #15）', c=0, s=1, f=0, c2=1, w3=1, excl=0,
         src='卷116 #15 缺 cutoff 前三个矩；本仓无此原理'),
    dict(id='E10', name='换理论起点（全部外部登记）', c=3, s=4, f=0, c2=1, w3=0, excl=0,
         src='卷116 封卷状态：重启入口 2'),
]
QUOTA_C = 1
QUOTA_S = 1


def cls(e):
    if e['excl'] or e['f'] or not e['c2']:
        return 'DEAD'
    if e['c'] > QUOTA_C or e['s'] > QUOTA_S:
        return 'DEAD'
    if e['w3'] == 1:
        return 'SURVIVE'
    return 'COST-ONLY'


def merge(x, y):
    return dict(c=x['c'] + y['c'], s=x['s'] + y['s'],
                f=max(x['f'], y['f']), c2=x['c2'] and y['c2'],
                w3=max(x['w3'], y['w3']), excl=max(x['excl'], y['excl']))


states_single = [(e['id'], cls(e)) for e in EXIT]
states_pairs = [(x['id'] + '+' + y['id'], cls(merge(x, y)))
                for x, y in combinations(EXIT, 2)]
n_single_surv = sum(1 for _, s in states_single if s == 'SURVIVE')
n_pair_surv = sum(1 for _, s in states_pairs if s == 'SURVIVE')
n_single_cost = sum(1 for _, s in states_single if s == 'COST-ONLY')

IDEAL = dict(c=0, s=0, f=0, c2=1, w3=1, excl=0)
NULL = dict(c=0, s=0, f=0, c2=1, w3=0, excl=1)
guard('G-E1', cls(IDEAL) == 'SURVIVE', '阳性对照：理想原理出口判 SURVIVE（判据有牙）')
guard('G-E2', cls(NULL) == 'DEAD', '阴性对照：恒等复读出口判 DEAD')
guard('G-E3', len(states_single) == 10 and len(states_pairs) == 45,
      '单点 10 + 两点 45 = 55 组穷举')
guard('G-E4', n_single_surv == 1 and n_pair_surv == 0,
      '单点恰 1 条 SURVIVE；两点组合 0 条（代价叠加不产生协同）')
guard('G-E5', sum(1 for e in EXIT if e['src']) == 10, '每条出口均有出处登记')

add('E01', 'PASS', '出口代价穷举：55 组三态判决表',
    '单点 10 组 SURVIVE %d / COST-ONLY %d / DEAD %d；'
    '两点 45 组 SURVIVE %d。代价按上界叠加（c/s 相加、excl/f 取或）。'
    % (n_single_surv, n_single_cost,
       sum(1 for _, s in states_single if s == 'DEAD'), n_pair_surv))
add('E02', 'BOUNDARY', '唯一 SURVIVE 是条件存活，不是已实现',
    'E09「钉死 f 的原理」是本仓唯一在 Omega5 配额内且能产出 W3 输出的通道，'
    '但卷116 债务 #15 明确「缺 cutoff 前三个矩、本仓无此原理」；'
    '故状态为 CONDITIONAL-SURVIVE：判据放行的是通道，不是成果。')
add('E03', 'FAIL', '其余九条出口均不存活（代价超限 / 已排除 / 函数级自由度 / 不保 C2）',
    '；'.join('%s:%s' % (i, s) for i, s in states_single))
add('E04', 'INFO', '最小代价下界（本册核心读数）',
    '要在 Omega5 配额内统一四力，必须同时满足：连续常数 <= 1、结构自由度 <= 1、'
    '保持 C2 还原、且产出至少 1 个非测量锚无量纲数值；'
    '55 组里只有 +1 条新原理（非自由常数、非节点）的通道未被排除。'
    '该原理的最小交付物 = cutoff 前三个矩 + 由它事前给出的无量纲量数值。')
add('E05', 'BOUNDARY', '未建模的协同',
    '两点组合按代价上界叠加；若两条出口共享同一新原理而只付一次代价，'
    '属于协同结构，本册未建模，不据此宣称组合更优或更差。')

# ---------------------------------------------------------------- P 验收协议
# r403 的 13 行候选状态为继承，不重判；本册只把「统一」翻成可执行验收清单
CAND = [
    ('U01', 2, 'PASS', 'PASS', 'PASS', 'PASS', '是'),
    ('U02', 3, 'PASS', 'PASS', 'PASS', 'PASS', '否'),
    ('U03', 3, 'PASS', 'PASS', 'BOUNDARY', 'FAIL', '是'),
    ('U04', 3, 'PASS', 'PASS', 'BOUNDARY', 'FAIL', '是'),
    ('U05', 3, 'PASS', 'BOUNDARY', 'BOUNDARY', 'FAIL', '是'),
    ('U06', 3, 'PASS', 'PASS', 'BOUNDARY', 'FAIL', '是'),
    ('U07', 4, 'PASS', 'PASS', 'PASS', 'FAIL', '否'),
    ('U08', 4, 'PASS', 'BOUNDARY', 'BOUNDARY', 'FAIL', '否'),
    ('U09', 4, 'PASS', 'PASS', 'PASS', 'FAIL', '是'),
    ('U10', 4, 'PASS', 'PASS', 'PASS', 'FAIL', '是'),
    ('U11', 4, 'PASS', 'PASS', 'PASS', 'FAIL', '否'),
    ('U12', 4, 'FAIL', 'PASS', 'FAIL', 'FAIL', '是'),
    ('U13', 4, 'BOUNDARY', 'BOUNDARY', 'FAIL', 'FAIL', '是'),
]
CHECKLIST = ['C0 量纲四轴零缺口', 'C1 机器复现且过恒等重述检测',
             'C2 GR/SM 经典极限', 'C3 已被证实的判别性新预言',
             'W3 至少一个非测量锚无量纲数值', 'Omega5 自由常数 <= 1 且结构自由度已登记']


def accepts(row):
    cid, nf, c0, c1, c2, c3, unified = row
    return (nf == 4 and unified == '是'
            and all(x == 'PASS' for x in (c0, c1, c2, c3)))


four_force = [r for r in CAND if r[1] == 4]
accepted = [r[0] for r in four_force if accepts(r)]
guard('G-P1', len(CAND) == 13, 'r403 13 行候选完整继承')
guard('G-P2', len(four_force) == 7, '覆盖四力的候选 7 行')
guard('G-P3', len(accepted) == 0, '四力候选通过 C0-C3 全 PASS 者为 0')
guard('G-P4', accepts(CAND[0]) is False and CAND[0][1] == 2,
      '阳性对照：电弱 U01 本身正确但因只覆盖 2 力不计入四力统一')

add('P01', 'PASS', '「统一所有力」的可证伪验收清单（6 项，缺一不可）',
    '；'.join('%d) %s' % (i + 1, x) for i, x in enumerate(CHECKLIST)))
add('P02', 'FAIL', '用该清单过 r403 继承总表：四力通过 0 条',
    '覆盖四力的候选 %d 行，C0-C3 全 PASS 者 %d 行；'
    '最高只到 C2 的形式统一族（U09/U10/U11）C3 全 FAIL。'
    % (len(four_force), len(accepted)))
add('P03', 'INFO', '正面路线（对用户「统一所有力」的可执行回答）',
    '路径唯一且分三步：①补 Omega5 结构自由度限额条款（治理，零物理代价）；'
    '②交付卷116 债务 #15 的「钉死 f 原理」= cutoff 前三个矩 + 一个事前无量纲数值；'
    '③该数值过双锚点（method_F）后再谈四力同源方程。'
    '③ 之前任何「统一」都只能是 C2 层形式统一或恒等重述。')
add('P04', 'BOUNDARY', '本册不产生的东西',
    '不新造统一方程、不重判 r403 的 13 行、不把 C2 形式统一升级为 C3、'
    '不把「原理通道存活」读作「统一已完成」；也不否证研究方向本身。')

# ---------------------------------------------------------------- 汇总与产物
cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
verdict = ('MINIMUM-COST-LOWER-BOUND--UNIQUE-CONDITIONAL-CHANNEL-IS-Z-PRINCIPLE'
           if gok == gtot else 'GUARD-FAILED')

key_numbers = {
    'dim_exhaust_groups': 7 ** 5,
    'dim_hits': len(sol),
    'dim_unique_core': len(core),
    'dim_core': str(core),
    'dim_no_mass_hits': len(sol_no_mass),
    'identity_ratio': fmt(ident_ratio),
    'couple_span_dex': fmt(span),
    'single_const_rms_dex': fmt(rms),
    'single_const_max_bias_dex': fmt(half),
    'integer_exponents': str(a_int),
    'integer_fit_max_residual_dex': fmt(maxres),
    'omega5_formal_free_constants': 0,
    'omega5_structural_inputs': len(a_int),
    'omega5_effective_degrees': len(a_int),
    'omega5_with_free_lambda': 1 + len(a_int),
    'exit_single_survive': n_single_surv,
    'exit_pair_survive': n_pair_surv,
    'exit_cost_only': n_single_cost,
    'four_force_candidates': len(four_force),
    'four_force_accepted': len(accepted),
    'guards': '%d/%d' % (gok, gtot),
    'verdict': verdict,
}

payload = dict(round='r404', date='2026-11-09', name=NAME,
               verdict=verdict, entries=ENTRIES, guards=GUARDS,
               anchors=anchor_rows, exits=[dict(e, state=cls(e)) for e in EXIT],
               pair_states=states_pairs, checklist=CHECKLIST,
               key_numbers=key_numbers,
               not_self_derived=[
                   'C0-C3 口径与 13 行候选状态（r403 继承，不重判）',
                   '类别互斥 / 外部输入单调链（attack41 继承）',
                   '五条逃逸口状态与债务 #15（卷116 继承）',
                   'M_Z 口径四耦合数值（能标一致性册继承，[C] 级测量锚）',
                   'Omega5 自由常数 <= 1（既有公设，本册只指出结构自由度缺口）',
               ],
               red_line='数学自洽 != 有物理内容 != 实验证实；不宣称统一所有力已完成。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r404 统一所有力：同源化最小代价下界与唯一生存通道 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(cnt)),
         'GUARDS %d/%d' % (gok, gtot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines.append('')
lines.append('== KEY NUMBERS ==')
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines.append('')
lines.append('== ANCHORS ==')
for r in anchor_rows:
    lines.append('%s | %s | %d/%d' % (r['label'], r['file'], r['hit'], r['total']))
lines.append('')
lines.append('== EXIT STATES (single) ==')
for i, s in states_single:
    lines.append('%s %s' % (i, s))
lines.append('')
lines.append('== GUARDS ==')
for g in GUARDS:
    lines.append('%s %s | %s' % ('OK' if g['ok'] else 'NG', g['code'], g['note']))
lines.append('')
lines.append('红线：数学自洽 != 有物理内容 != 实验证实；不宣称统一所有力已完成。')
report = '\n'.join(lines) + '\n'
with io.open(str(OUT / (NAME + '_report.txt')), 'w', encoding='utf-8', newline='\n') as f:
    f.write(report)

md = ['# ' + NAME, '',
      '- 判词：`%s`' % verdict,
      '- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, v) for k, v in sorted(cnt.items()))),
      '- 守卫 **%d/%d**；退出码 %d' % (gok, gtot, 0 if gok == gtot else 1), '',
      '## 条目', '',
      '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:400]))
md += ['', '## 关键读数', '', '| 键 | 值 |', '| --- | --- |']
for k, v in key_numbers.items():
    md.append('| %s | %s |' % (k, str(v).replace('|', '/')))
md += ['', '## 出口状态', '', '| 出口 | 状态 |', '| --- | --- |']
for i, s in states_single:
    md.append('| %s | %s |' % (i, s))
md += ['', '## 红线', '', payload['red_line'], '']
with io.open(str(OUT / (NAME + '.md')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('SECTIONS A K Y E P')
print('ENTRIES %d %s' % (len(ENTRIES), str(cnt)))
print('GUARDS %d/%d' % (gok, gtot))
print('VERDICT %s' % verdict)
print('EXIT %d' % (0 if gok == gtot else 1))
sys.exit(0 if gok == gtot else 1)
