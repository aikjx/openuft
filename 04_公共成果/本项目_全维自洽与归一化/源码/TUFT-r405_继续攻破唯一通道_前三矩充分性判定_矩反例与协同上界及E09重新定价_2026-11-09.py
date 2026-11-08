# -*- coding: utf-8 -*-
"""TUFT-r405 | 继续攻破唯一通道：前三矩充分性判定、矩反例、协同上界与 E09 重新定价。

承接 r404：r404 把「统一所有力」压到唯一未被排除通道 E09
（卷116 债务 #15「钉死 f 的原理」，CONDITIONAL-SURVIVE），
并把「两点协同」登记为未建模（E05）。本册攻这两处留白：

  M 段  首次判定「cutoff 前三个矩」是充分还是仅必要：
        用精确 Fraction 构造一族正谱测度，共享 m0,m1,m2 而 m3 线性变化。
        结论：三矩对 r=m1/m0 充分，对 f 本身不充分（截断矩问题非唯一）。
  V 段  三矩派生的无量纲数值 V=0，过不了 attack42 的 C2 双锚点。
  C 段  协同最宽松上界（代价取 max）重算 45 组两点组合，闭合 r404 E05。
  R 段  对 E09 重新定价：最小交付物不足，CONDITIONAL-SURVIVE 降级。

不做：不重判既有条目、不新造统一方程、不宣称统一已完成、不改被引文件字节。
纯标准库 / Python 3.8 / Fraction 精确有理数 / Decimal 60 位展示。
控制台只打印 ASCII 摘要；中文细节写入 UTF-8 产物。
"""
import io
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from fnmatch import fnmatch

try:
    sys.stdout.reconfigure(errors='replace')
except Exception:
    pass

getcontext().prec = 60
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / '数据'
NAME = 'TUFT-r405_继续攻破唯一通道_前三矩充分性判定_矩反例与协同上界及E09重新定价_2026-11-09'

ENTRIES = []
GUARDS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def fs(x):
    return str(x)


# ---------------------------------------------------------------- A 锚点实读
ANCHOR_SPECS = [
    ('卷110 J88', '110_第69轮_*', ['缺 cutoff 的前三个矩', 'r=f₂/f₀', '族']),
    ('卷111 J89', '111_第70轮_*', ['m_k', 'R_DEP_THEOREM', '泛函']),
    ('卷116 终卷', '116_终卷_*', ['#15', '钉死 f 的原理', '封卷']),
    ('卷119 J97', '119_第77轮_*', ['f 未被钉住', '形状族', '归一原理']),
    ('卷127 J105', '127_第84轮_*', ['r 是 f 的泛函', 'FZ']),
    ('attack42 判定册', '判定_attack42_*', ['双锚点', 'V', 'C2']),
    ('r404 判定册', '判定_TUFT-r404_*', ['CONDITIONAL-SURVIVE', '协同', '55']),
    ('method_F', 'method_F_第一性判据.md', ['无量纲量', '双锚点']),
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

guard('G-A1', sum(1 for r in anchor_rows if r['hit'] > 0) >= 7,
      '至少 7/8 继承锚点磁盘实读命中')
guard('G-A2', all(r['hit'] > 0 for r in anchor_rows[:4]),
      '卷110/111/116/119 四个主锚必须命中')
add('A01', 'PASS', '继承锚点磁盘实读',
    '；'.join('%s %s %d/%d' % (r['label'], r['file'][:44], r['hit'], r['total'])
              for r in anchor_rows))
missing_anchors = [r['label'] for r in anchor_rows if r['hit'] == 0]
if missing_anchors:
    add('A02', 'BOUNDARY', '未命中锚点：' + '、'.join(missing_anchors),
        '未命中锚点不构造继承读数，相关条目降级为条件性，不冒充继承')

# ---------------------------------------------------------------- M 截断矩反例
X = (F(1), F(2), F(3), F(4))          # 谱支持点，全在 [0, inf)
W0 = (F(4), F(4), F(4), F(4))        # 基测度
C = (F(1), F(-3), F(3), F(-1))       # 四阶差分零空间：sum c_i x_i^k = 0 (k=0,1,2)


def weights(t):
    return tuple(W0[i] + t * C[i] for i in range(4))


def moment(t, k):
    return sum(weights(t)[i] * X[i] ** k for i in range(4))


def kernel(k):
    return sum(C[i] * X[i] ** k for i in range(4))


TS = (F(-1), F(0), F(1))
M = dict((t, [moment(t, k) for k in range(5)]) for t in TS)
m0, m1, m2, m3, m4 = M[F(0)]

guard('G-M1', all(kernel(k) == 0 for k in (0, 1, 2)) and kernel(3) == -6,
      '四阶差分核在 k=0,1,2 精确为 0，k=3 精确为 -6')
guard('G-M2', all(M[t][0] == 16 and M[t][1] == 40 and M[t][2] == 120 for t in TS),
      '三点见证前三矩恒为 16/40/120')
guard('G-M3', len(set(M[t][3] for t in TS)) == 3,
      'm3 在 t=-1,0,1 三点互异（406/400/394）')
guard('G-M4', M[F(-1)][3] == 406 and M[F(1)][3] == 394 and m3 == 400,
      'm3(t) = 400 - 6t 精确线性')
guard('G-M5', all(min(weights(t)) > 0 for t in TS),
      '三点见证权重全正（合法正谱测度）')
guard('G-M6', min(weights(F(4, 3))) == 0 and min(weights(F(-4, 3))) == 0,
      '正性区间端点 t = +-4/3 处权重首次触零')
guard('G-M7', all(moment(t, 3) == 400 - 6 * t for t in TS),
      '连续族恒等式 m3(t)=400-6t 逐点成立')

r_of = lambda t: M[t][1] / M[t][0]
q_of = lambda t: M[t][3] / M[t][0]
guard('G-M8', len(set(r_of(t) for t in TS)) == 1 and r_of(F(0)) == F(5, 2),
      'r=m1/m0=5/2 全族唯一（三矩对 r 充分）')
guard('G-M9', len(set(q_of(t) for t in TS)) == 3,
      'q=m3/m0 全族变化（依赖高阶矩的量不确定）')

add('M01', 'PASS', '构造性反例：一族正谱测度共享前三矩',
    '支持点 x=%s、基权重 w0=%s、扰动核 c=%s；w(t)=w0+t*c。'
    '核在 k=0,1,2 精确为零（%s），k=3 为 %s；'
    '故 m0=%s、m1=%s、m2=%s 对全体 t 恒定，而 m3(t)=%s。'
    % (str(X), str(W0), str(C), str([kernel(k) for k in (0, 1, 2)]),
       str(kernel(3)), fs(m0), fs(m1), fs(m2), '400-6t'))
add('M02', 'PASS', '不是两个点，是一维连续族',
    't=-1,0,+1 三点权重 %s / %s / %s 全正；'
    'm3 = %s / %s / %s；正性区间 t in (-4/3, 4/3)（端点权重首次触零）。'
    '交付三个矩后仍剩 1 维连续形状自由度。'
    % (str(weights(F(-1))), str(weights(F(0))), str(weights(F(1))),
       fs(M[F(-1)][3]), fs(m3), fs(M[F(1)][3])))
add('M03', 'PASS', '首次判定充分性（一）：三矩对 Z/r 充分',
    '卷111 口径 r^(a)=m1/m0=%s 在全族恒定；卷110 单迹假设 1/Z=r*(5/3)/(4*kappa6)'
    '与 N_T=1+(5/3)r 因此被三矩唯一确定。库内「缺 cutoff 前三个矩」的措辞'
    '首次被判定为充分条件（就 Z/r 层而言）。' % fs(r_of(F(0))))
add('M04', 'FAIL', '首次判定充分性（二）：三矩对 f 本身不充分',
    'q=m3/m0 = %s / %s / %s 随 t 变；任何依赖高阶矩或形状的物理量在该族内不确定。'
    '故 #15「钉死 f 的原理」若只交付三个矩，得到的是一个等价类而非唯一的 f，'
    '与卷119「f 未被钉住、仍是参数化重述」同向但更硬：'
    '卷119 的形状族改变矩，本册的族连前三矩都不改。'
    % (fs(q_of(F(-1))), fs(q_of(F(0))), fs(q_of(F(1)))))
add('M05', 'BOUNDARY', '射程声明：反例是离散正测度',
    'delta 组合是 cutoff 函数 f 的合法正测度极限表示，支持点全在 [0,inf) 且权重全正；'
    '本册不宣称连续 f 的截断矩问题一般定理，只给精确构造性反例与机器读数。')

# ---------------------------------------------------------------- V 双锚点判别力
# attack42 C2-2：V = (n_hit - n_free - n_anchor) / n_hit > 0
N_HIT, N_FREE_A, N_ANCHOR = 1, 1, 0
V_A = F(N_HIT - N_FREE_A - N_ANCHOR, N_HIT)
N_FREE_B = 3
V_B = F(N_HIT - N_FREE_B - N_ANCHOR, N_HIT)
guard('G-V1', V_A == 0 and V_B == -2,
      '两种自由输入口径下 V 分别为 0 与 -2')
guard('G-V2', V_A <= 0 and V_B <= 0,
      '三矩派生数值在两种口径下均不过 C2-2')
add('V01', 'FAIL', '三矩派生的无量纲数值过不了 attack42 的 C2 双锚点',
    'attack42 C2-2 判据 V=(n_hit-n_free-n_anchor)/n_hit>0；'
    '按该册读数 (n_hit=1,n_free=1,n_anchor=0) 得 V=%s；'
    '若把三个矩都计为自由输入 (n_free=3) 得 V=%s。'
    '两者均 <=0 ⇒ r=m1/m0 是矩比值的等价交换，无信息增益，'
    '不构成 W3 要求的「非测量锚无量纲数值」。' % (fs(V_A), fs(V_B)))
add('V02', 'CORRECTED', 'r404 E09 的「最小交付物」口径更正',
    'r404 写「三个矩 + 由它事前给出的无量纲量数值」；本册证明由三矩派生的数值 V<=0，'
    '故该数值不能充当 W3 输出。最小交付物须升级为：'
    '一条固定 f 形状/归一的原理 + 一个非矩派生且 V>0 的数值。')

# ---------------------------------------------------------------- C 协同最宽松上界
EXIT = [
    dict(id='E01', name='最小 SU(5)', c=0, s=1, f=0, c2=1, w3=0, excl=1),
    dict(id='E02', name='MSSM / 超对称', c=105, s=1, f=0, c2=1, w3=0, excl=1),
    dict(id='E03', name='SO(10)+阈值+Yukawa', c=15, s=1, f=0, c2=1, w3=0, excl=0),
    dict(id='E04', name='额外维 KK', c=1, s=2, f=0, c2=1, w3=0, excl=0),
    dict(id='E05', name='弦 / 量子引力', c=0, s=9, f=0, c2=0, w3=0, excl=0),
    dict(id='E06', name='几何 omega(r,t)', c=0, s=1, f=1, c2=1, w3=0, excl=0),
    dict(id='E07', name='新场 / 新耦合', c=2, s=0, f=0, c2=1, w3=0, excl=0),
    dict(id='E08', name='修改 Omega5 并登记输入', c=3, s=4, f=0, c2=1, w3=0, excl=0),
    dict(id='E09', name='钉死 f 的原理（卷116 #15）', c=0, s=1, f=0, c2=1, w3=1, excl=0),
    dict(id='E10', name='换理论起点', c=3, s=4, f=0, c2=1, w3=0, excl=0),
]
QUOTA_C, QUOTA_S = 1, 1


def cls(e):
    if e['excl'] or e['f'] or not e['c2']:
        return 'DEAD'
    if e['c'] > QUOTA_C or e['s'] > QUOTA_S:
        return 'DEAD'
    if e['w3'] == 1:
        return 'SURVIVE'
    return 'COST-ONLY'


def merge_upper(x, y):
    # r404 口径：代价上界叠加
    return dict(c=x['c'] + y['c'], s=x['s'] + y['s'],
                f=max(x['f'], y['f']), c2=x['c2'] and y['c2'],
                w3=max(x['w3'], y['w3']), excl=max(x['excl'], y['excl']))


def merge_synergy(x, y):
    # 最宽松协同：任意两点都视为共享同一原理，代价只付一次（取 max）
    # 这是协同的上界（最有利于存活）；在此口径下 0 存活 => 任何更严协同也 0
    return dict(c=max(x['c'], y['c']), s=max(x['s'], y['s']),
                f=max(x['f'], y['f']), c2=x['c2'] and y['c2'],
                w3=max(x['w3'], y['w3']), excl=max(x['excl'], y['excl']))


pairs = list(combinations(EXIT, 2))
st_upper = [(x['id'] + '+' + y['id'], cls(merge_upper(x, y))) for x, y in pairs]
st_syn = [(x['id'] + '+' + y['id'], cls(merge_synergy(x, y))) for x, y in pairs]
surv_upper = sum(1 for _, s in st_upper if s == 'SURVIVE')
surv_syn = sum(1 for _, s in st_syn if s == 'SURVIVE')
dead_syn = sum(1 for _, s in st_syn if s == 'DEAD')

IDEAL_PARTNER = dict(c=0, s=0, f=0, c2=1, w3=0, excl=0)
syn_ideal = cls(merge_synergy(EXIT[8], IDEAL_PARTNER))
guard('G-C1', len(pairs) == 45, '两点组合 45 组')
guard('G-C2', surv_upper == 0, 'r404 上界叠加口径 0 存活（继承复核）')
guard('G-C3', surv_syn == 0, '最宽松协同口径仍 0 存活')
guard('G-C4', syn_ideal == 'SURVIVE',
      '阳性对照：若存在零代价协同伙伴，判据会放行（判据有牙）')
guard('G-C5', dead_syn == 45, '协同口径下 45 组全 DEAD')

add('C01', 'PASS', '协同最宽松上界：45 组两点组合仍 0 存活',
    '把「两条出口共享同一新原理、代价只付一次」放宽到任意两点 '
    '（c/s 取 max、w3 取 max、excl/f 取 or、c2 取 and）——这是协同的最有利上界。'
    '结果：SURVIVE %d / DEAD %d；r404 上界叠加口径 SURVIVE %d。'
    '两种口径一致 ⇒ r404 的 E05「协同未建模」不改变结论。'
    % (surv_syn, dead_syn, surv_upper))
add('C02', 'PASS', '阳性对照证明协同判据不恒假',
    '人为注入一个零代价协同伙伴 (c=0,s=0,f=0,c2=1,w3=0,excl=0) 与 E09 组合，'
    '最宽松协同判为 %s；故「现实 45 组 0 存活」不是判据恒假所致。' % syn_ideal)
add('C03', 'PASS', 'r404 E05 开放项闭合',
    'r404 把协同登记为 BOUNDARY（未建模）；本册给出可复算的最宽松上界模型并得 0 存活，'
    '该开放项由「未建模」升级为「已建模且结论稳健」。')

# ---------------------------------------------------------------- R E09 重新定价
E09_OLD = cls(EXIT[8])
E09_NEW = dict(EXIT[8], s=2)   # 加一条固定 f 形状/归一的原理 => 结构自由度 2
E09_NEW_STATE = cls(E09_NEW)
new_single = [(e['id'], cls(E09_NEW if e['id'] == 'E09' else e)) for e in EXIT]
surv_new_single = sum(1 for _, s in new_single if s == 'SURVIVE')
guard('G-R1', E09_OLD == 'SURVIVE', 'r404 口径下 E09 为 SURVIVE（继承复核）')
guard('G-R2', E09_NEW_STATE == 'DEAD', '补形状原理后 s=2 超配额，E09 判 DEAD')
guard('G-R3', surv_new_single == 0, '重新定价后单点 SURVIVE 归零')

add('R01', 'CORRECTED', '唯一通道降级：CONDITIONAL-SURVIVE -> CONDITIONAL-INSUFFICIENT',
    'r404 的 E09 代价 (c=0,s=1,w3=1) 在补上本册 V 段与 M 段结论后须重定价：'
    '三矩对 f 不充分且派生数值 V<=0，故须再加一条固定 f 形状/归一的原理，'
    '使 s=2 > 配额 1 ⇒ 状态由 %s 变 %s；单点 SURVIVE 由 1 变 %d。'
    % (E09_OLD, E09_NEW_STATE, surv_new_single))
add('R02', 'INFO', '重新定价后的最小交付物',
    '① Ω5 结构自由度限额条款（治理）；② 一条同时固定 f 形状并给出 V>0 非测量锚数值的原理；'
    '③ 该数值过 method_F 双锚点。若一条原理能同时干两件事而仍只记 s=1，'
    '则属「原理能力」口径重定义，本册不代选（BOUNDARY R03）。')
add('R03', 'BOUNDARY', '本册不关闭研究方向',
    '「单点 SURVIVE 归零」是「当前配额口径 + 当前交付物定义」下的判定；'
    '卷116 债务 #15 仍是「仍开」（它是开放项，不是已被本册关闭的通道）。'
    'r403 §十一「不否证研究方向」的红线在此继续有效。')
add('R04', 'INFO', '正面路线（对用户「继续攻破」的回答）',
    '攻破结果不是「无路可走」，而是把路的价格标清：'
    '三矩能钉死 Z/r（首次正面判定）但钉不死 f；'
    '要继续，必须给出一条 f 归一/形状原理，且它输出的数值不能是矩比值。'
    '在此之前，卷119 的「f 未钉住、参数化重述」结论在更硬的口径下继续成立。')

# ---------------------------------------------------------------- 汇总与产物
cnt = {}
for e in ENTRIES:
    cnt[e['status']] = cnt.get(e['status'], 0) + 1
gok = sum(1 for g in GUARDS if g['ok'])
gtot = len(GUARDS)
verdict = ('THREE-MOMENTS-FIX-R-BUT-NOT-F--CHANNEL-REPRICED-TO-INSUFFICIENT'
           '--SYNERGY-DOES-NOT-RESCUE' if gok == gtot else 'GUARD-FAILED')

key_numbers = {
    'kernel_k012': str([kernel(k) for k in (0, 1, 2)]),
    'kernel_k3': str(kernel(3)),
    'support_points': str(X),
    'base_weights': str(W0),
    'null_direction': str(C),
    'm0': fs(m0), 'm1': fs(m1), 'm2': fs(m2),
    'm3_t_minus1': fs(M[F(-1)][3]), 'm3_t_0': fs(m3), 'm3_t_plus1': fs(M[F(1)][3]),
    'm3_formula': '400-6t',
    'positivity_interval': '(-4/3, 4/3)',
    'r_m1_over_m0': fs(r_of(F(0))),
    'q_t_minus1': fs(q_of(F(-1))), 'q_t_0': fs(q_of(F(0))), 'q_t_plus1': fs(q_of(F(1))),
    'V_attack42_caliber': fs(V_A), 'V_three_moments_caliber': fs(V_B),
    'pairs_upper_survive': surv_upper,
    'pairs_synergy_survive': surv_syn,
    'pairs_synergy_dead': dead_syn,
    'E09_state_r404': E09_OLD,
    'E09_state_repriced': E09_NEW_STATE,
    'single_survive_repriced': surv_new_single,
    'guards': '%d/%d' % (gok, gtot),
    'verdict': verdict,
}

payload = dict(round='r405', date='2026-11-09', name=NAME, verdict=verdict,
               entries=ENTRIES, guards=GUARDS, anchors=anchor_rows,
               moment_family=dict(t=[fs(t) for t in TS],
                                  weights=[str(weights(t)) for t in TS],
                                  moments=[str(M[t]) for t in TS]),
               exits=EXIT,
               pair_upper_states=st_upper, pair_synergy_states=st_syn,
               key_numbers=key_numbers,
               not_self_derived=[
                   '矩定义 m_k=int f(u)u^k du 与 r^(a)=m1/m0（卷111 继承）',
                   '单迹假设 1/Z=r*(5/3)/(4kappa6) 与「缺前三矩」（卷110 继承）',
                   '债务 #15/#18 与封卷重启入口（卷116 继承）',
                   'f 未被钉住 / 形状族 / 归一原理需求（卷119 继承）',
                   'C2-2 判据 V=(n_hit-n_free-n_anchor)/n_hit（attack42 继承）',
                   '10 条出口代价向量与 55 组穷举（r404 继承）',
               ],
               red_line='数学自洽 != 有物理内容 != 实验证实；不宣称统一所有力已完成，'
                        '也不把「单点 SURVIVE 归零」读作对研究方向的普遍否证。')

OUT.mkdir(parents=True, exist_ok=True)
with io.open(str(OUT / (NAME + '.json')), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

lines = ['== r405 继续攻破唯一通道：前三矩充分性 / 协同上界 / E09 重新定价 ==',
         'VERDICT %s' % verdict,
         'ENTRIES %d %s' % (len(ENTRIES), str(cnt)),
         'GUARDS %d/%d' % (gok, gtot), '']
for e in ENTRIES:
    lines.append('[%s] %s | %s' % (e['status'], e['code'], e['title']))
    lines.append('    %s' % e['detail'])
lines += ['', '== KEY NUMBERS ==']
for k, v in key_numbers.items():
    lines.append('%s = %s' % (k, v))
lines += ['', '== ANCHORS ==']
for r in anchor_rows:
    lines.append('%s | %s | %d/%d' % (r['label'], r['file'], r['hit'], r['total']))
lines += ['', '== PAIR STATES (synergy upper bound) ==']
for i, s in st_syn:
    lines.append('%s %s' % (i, s))
lines += ['', '== GUARDS ==']
for g in GUARDS:
    lines.append('%s %s | %s' % ('OK' if g['ok'] else 'NG', g['code'], g['note']))
lines += ['', payload['red_line']]
with io.open(str(OUT / (NAME + '_report.txt')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')

md = ['# ' + NAME, '', '- 判词：`%s`' % verdict,
      '- 条目 %d：%s' % (len(ENTRIES), ' / '.join('%s %d' % (k, v) for k, v in sorted(cnt.items()))),
      '- 守卫 **%d/%d**；退出码 %d' % (gok, gtot, 0 if gok == gtot else 1), '',
      '## 条目', '', '| 编号 | 状态 | 标题 | 读数 |', '| --- | --- | --- | --- |']
for e in ENTRIES:
    md.append('| %s | %s | %s | %s |' %
              (e['code'], e['status'], e['title'].replace('|', '/'),
               e['detail'].replace('|', '/').replace('\n', ' ')[:420]))
md += ['', '## 关键读数', '', '| 键 | 值 |', '| --- | --- |']
for k, v in key_numbers.items():
    md.append('| %s | %s |' % (k, str(v).replace('|', '/')))
md += ['', '## 红线', '', payload['red_line'], '']
with io.open(str(OUT / (NAME + '.md')), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('SECTIONS A M V C R')
print('ENTRIES %d %s' % (len(ENTRIES), str(cnt)))
print('GUARDS %d/%d' % (gok, gtot))
print('VERDICT %s' % verdict)
print('EXIT %d' % (0 if gok == gtot else 1))
sys.exit(0 if gok == gtot else 1)
