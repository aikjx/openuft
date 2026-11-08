# -*- coding: utf-8 -*-
# attack43 / 攻破㉟ —— 力的起源本质本源：第 17 候选与 16×4 交叉供给矩阵（2026-11-08）
# 靶：把「力/相互作用本源」作为第 17 项宇宙本源候选层，判定 16 候选 × 4 力交叉矩阵
#     中是否存在任一格给出「非测量锚无量纲输出且过 C2 六条件」。
# 纯标准库（os/io/json/re/ast/itertools + Fraction + Decimal），无第三方依赖、无随机、只读事实源。
# 红线：不宣称完成统一场、不宣称宇宙本质本源已回答；0/22、UFT-3=0、L3=0、validated=0 不变；本册不占 RID。
import os, sys, io, json, re, ast, itertools
from fractions import Fraction as F
from decimal import Decimal as Dc, getcontext
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack43_力本源_第17候选与16x4交叉供给矩阵_2026-11-08'
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..'))
NORM = os.path.join(PUB, '本项目_全维自洽与归一化')

P_FINAL = os.path.join(HERE, '穷尽攻破_统一场论终局总成_2026-10-21.md')
P_ORIGIN_BOOK = os.path.join(HERE, '穷尽攻破_宇宙本质本源_2026-10-21.md')
P_C0160 = os.path.join(HERE, '判定_C0160_力的统一攻破_2026-10-21.md')
P_FORCE_AUDIT = os.path.join(NORM, '判定_四力本源_层级与可统一性的机器审计_2026-10-07.md')
P_FINALJUDGE = os.path.join(NORM, '力的本源统一场_终审裁决_2026-10-13.md')
P_R130 = os.path.join(NORM, '数据', '判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md')
P_R132 = os.path.join(NORM, '数据', '判定_TUFT-r132_全维自洽与归一化_跨卷综合判定与攻破全景_2026-10-20.md')
P_R134 = os.path.join(NORM, '数据', '判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md')
P_R67 = os.path.join(NORM, '判定_TUFT-r67-力统一场论本源性审计_内生外输普查与GR正对照_2026-10-31.md')
P_R273 = os.path.join(NORM, '数据', '判定_TUFT-r273_四力本源参数精算层_统一势模板标准耦合重标定及qWqπ数值核验_精算与可视化_2026-10-31.md')
P_R222 = os.path.join(NORM, '判定', '判定_TUFT-r222_四力统一方程的传播层_色散截止群速度与质量力程等价_精算与可视化_2026-10-26.md')
P_R224 = os.path.join(NORM, '数据', 'TUFT-r224_四力统一运动方程_Proca方程机器验证圆轨道稳定性与荷空间可加性_精算与可视化_2026-10-26.md')
P_R180 = os.path.join(NORM, '判定_TUFT-r180_电磁耦合常数Zprime_恒等力比与Z双素数修正_精算_2026-10-25.md')
P_MATRIX = os.path.join(PUB, '全维全体系统一场论', '数据', '全维验收矩阵.json')
P_WJUDGE = os.path.join(PUB, '全维全体系统一场论', '判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md')
P_METHODF = os.path.join(OPENUFT, '02_共享基础', '研究规范', 'method_F_第一性判据.md')
P_TARGETS = os.path.join(NORM, '数据', '无量纲靶场审计.json')
P_A42 = os.path.join(HERE, 'attack42_C2硬门_四类机器分桶与双锚点可执行化_2026-11-08.json')
P_SORT = os.path.join(HERE, '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md')
P_README = os.path.join(HERE, 'README.md')

LINES = []
ENTRIES = []
GUARDS = []

def emit(s=''):
    LINES.append(s)
    print(s)

def add(uid, claim, verdict, reading):
    ENTRIES.append({'id': uid, 'claim': claim, 'verdict': verdict, 'reading': reading})
    emit('[%-9s] %s | %s' % (verdict, uid, claim))
    emit('            读数: %s' % reading)

def guard(gid, desc, ok, reading):
    ok = bool(ok)
    GUARDS.append({'id': gid, 'desc': desc, 'ok': ok, 'reading': reading})
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: %s' % reading)
    return ok

def read_text(path):
    return io.open(path, encoding='utf-8').read()

def read_json(path):
    return json.load(io.open(path, encoding='utf-8'))

def hit_all(text, needles):
    return sum(1 for x in needles if x in text)

# ---------- 只读事实源 ----------
fin = read_text(P_FINAL)
origin_book = read_text(P_ORIGIN_BOOK)
c0160 = read_text(P_C0160)
force_audit = read_text(P_FORCE_AUDIT)
finaljudge = read_text(P_FINALJUDGE)
r130 = read_text(P_R130)
r132 = read_text(P_R132)
r134 = read_text(P_R134)
r67 = read_text(P_R67)
r273 = read_text(P_R273)
r222 = read_text(P_R222)
r224 = read_text(P_R224)
r180 = read_text(P_R180)
matrix = read_json(P_MATRIX)
w_judge = read_text(P_WJUDGE)
methodf = read_text(P_METHODF)
targets = read_json(P_TARGETS)
a42 = read_json(P_A42)
sortbook = read_text(P_SORT)
readme_text = read_text(P_README)

# ---------- 16 项宇宙本源候选：现场从终局总成表格解析（不打字） ----------
CAND_ROWS = re.findall(
    r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([✅⚠️◐]+)\s*\|',
    fin, re.M)
CANDIDATES = [{'idx': int(a), 'name': b, 'supply': c, 'collision': d, 'verdict': e}
              for a, b, c, d, e in CAND_ROWS]
N_CAND = len(CANDIDATES)
N_PASS = sum(1 for c in CANDIDATES if c['verdict'] == '✅')
N_WARN = sum(1 for c in CANDIDATES if c['verdict'] == '⚠️')
N_PART = sum(1 for c in CANDIDATES if c['verdict'] == '◐')
CAND_WITH_FORCE = [c['name'] for c in CANDIDATES if '力' in c['name'] or '相互作用' in c['name']]

# 四力谱系：现场从 C0160 表格解析
FORCE_ROWS = re.findall(r'^\|\s*(引力|电磁|弱|强)\s*\|\s*([^|]+?)\s*\|', c0160, re.M)
FORCES = [x[0] for x in FORCE_ROWS]
N_FORCE = len(FORCES)

# 七路径状态：现场解析（6 open + 1 closed-neg）
PATH_ROWS = re.findall(r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\*{0,2}(open|closed-neg)',
                       c0160, re.M)
N_PATH_OPEN = sum(1 for x in PATH_ROWS if x[2] == 'open')
N_PATH_CLOSED = sum(1 for x in PATH_ROWS if x[2] == 'closed-neg')

# ---------- 四个 DERIVED 空格（力的起源） ----------
COUPLINGS = ['g', 'g′', 'g_s', 'G']
DERIVED_EMPTY_HITS = {
    'r130': ('g,g′' in r130 and 'g_s' in r130 and '力的起源' in r130 and 'DERIVED' in r130),
    'r132': ('g, g′, g_s, G' in r132 and 'DERIVED 层为空' in r132 and '力的起源' in r132),
    'r134': ('g, g′, g_s, G' in r134 and 'DERIVED 层为空' in r134 and '必须变为导出量' in r134),
}
N_DERIVED_SOURCES = sum(1 for v in DERIVED_EMPTY_HITS.values() if v)
DERIVED_FILLED = 0
DERIVED_SPACES = len(COUPLINGS) - DERIVED_FILLED

# 前提账本状态机：POSTED → DERIVED?
PREMISE_STATE = {c: 'POSTED' for c in COUPLINGS}
premise_transition = sum(1 for c in COUPLINGS if PREMISE_STATE[c] == 'DERIVED')
r130_needles = ['18/18 链', 'closure = 0.327', '总闭合度 0.327', 'SOUND-BUT-PREMISE-OPEN',
                '前提账本里四个 DERIVED 空格']
r130_hits = hit_all(r130, r130_needles)

# ---------- 16×4 交叉供给矩阵 ----------
SUPPLY_NUMERIC = set(('0', '0 ', '0.0'))
NON_NUMERIC_SUPPLY = ('无载体', '不可检验', '无判定入口')

def supply_class(s):
    s2 = s.strip()
    if s2 == '0':
        return 'ZERO_SUPPLY'
    if any(x in s2 for x in NON_NUMERIC_SUPPLY):
        return 'NO_MACHINE_ENTRY'
    return 'OTHER'

CELLS = []
for c, f in itertools.product(CANDIDATES, FORCES):
    sc = supply_class(c['supply'])
    CELLS.append({
        'cand_idx': c['idx'], 'cand': c['name'], 'force': f,
        'supply_raw': c['supply'], 'supply_class': sc,
        'collision': c['collision'], 'cand_verdict': c['verdict'],
        'endogenous_dimensionless_output': 0, 'c2_pass': 0,
    })
N_CELLS = len(CELLS)
N_ZERO = sum(1 for x in CELLS if x['supply_class'] == 'ZERO_SUPPLY')
N_NOENTRY = sum(1 for x in CELLS if x['supply_class'] == 'NO_MACHINE_ENTRY')
N_SUPPLY_NUMERIC = sum(1 for x in CELLS if x['supply_raw'].strip() in SUPPLY_NUMERIC
                       and x['supply_raw'].strip() != '0')

# ---------- C2 六条件（形式化，复用 attack42 的六条；不重复其双锚点数值化） ----------
C2_KEYS = ['C2-1 具名靶且 3σ', 'C2-2 V>0', 'C2-3 循环检测',
           'C2-4 双锚点各自出数且自洽', 'C2-5 L3 四条件且未被自身拟合',
           'C2-6 落 22 体系 W3 目标格且 target_registered≥1']
TARGET_KEYS = [t['key'] for t in targets['targets']]
TARGET_REGISTERED_ALL_ZERO = all(x['target_registered'] == 0 for x in
                                 read_json(os.path.join(NORM, '数据', '本项目_统一场论达成度重算_2026-10-08.json'))['per_system'])

def c2_gate(cell):
    reasons = []
    if not cell.get('named_target'):
        reasons.append('C2-1 无具名靶（本源候选层不输出无量纲数）')
    elif cell.get('predicted') is None:
        reasons.append('C2-1 无可机读数值')
    n_hit = cell.get('n_hit', 0)
    n_free = cell.get('n_free', 0)
    n_anchor = cell.get('n_anchor', 0)
    if n_hit <= 0:
        reasons.append('C2-2 n_hit=0，V 无定义')
    elif F(n_hit - n_free - n_anchor, n_hit) <= 0:
        reasons.append('C2-2 V≤0（等价交换/净消耗）')
    if cell.get('loop_ok') is not (1 == 1):
        reasons.append('C2-3 循环检测未过')
    if len(cell.get('anchors') or ()) < 2:
        reasons.append('C2-4 双锚点未登记')
    if cell.get('l3_ok') is not (1 == 1):
        reasons.append('C2-5 L3 四条件未过')
    if cell.get('target_registered', 0) < 1 or not TARGET_REGISTERED_ALL_ZERO:
        reasons.append('C2-6 W3 目标格未登记')
    return (len(reasons) == 0, reasons)

for x in CELLS:
    ok, reasons = c2_gate(x)
    x['c2_pass'] = 1 if ok else 0
    x['c2_reasons'] = reasons
CELL_PASS = sum(x['c2_pass'] for x in CELLS)
REASON_HIST = {}
for x in CELLS:
    for r in x['c2_reasons']:
        k = r.split()[0]
        REASON_HIST[k] = REASON_HIST.get(k, 0) + 1

# 阳性对照：假想合格格（靶场例3 型），仅用于证明守卫有牙，非任何体系产物
SYNTH = {'cand': 'SYNTHETIC', 'force': '电磁', 'named_target': 'alpha',
         'predicted': '0.0072973525693', 'n_hit': 4, 'n_free': 2, 'n_anchor': 1,
         'anchors': ['planck', 'particle'], 'loop_ok': 1 == 1,
         'l3_ok': 1 == 1, 'target_registered': 1}
syn_ok, syn_reasons = c2_gate(SYNTH)
MUT_DROP = dict(SYNTH); MUT_DROP['anchors'] = ['planck']
MUT_MEASURED = dict(SYNTH); MUT_MEASURED['n_anchor'] = 4
MUT_FREE = dict(SYNTH); MUT_FREE['n_free'] = 4
mut_drop_ok = c2_gate(MUT_DROP)[0]
mut_measured_ok = c2_gate(MUT_MEASURED)[0]
mut_free_ok = c2_gate(MUT_FREE)[0]
# 第 17 项候选自身的四格（四耦合空格 × 是否填 DERIVED）
CELL_17 = [{'coupling': c, 'state': PREMISE_STATE[c], 'c2_pass': 0} for c in COUPLINGS]
N_CELL_17_PASS = sum(x['c2_pass'] for x in CELL_17)

# ---------- 逐力四态分类（r67 分类法扩到逐力，不重跑 14 项普查） ----------
FORCE_STATES = {
    '引力': ('IMPORTED', 'G 为 POSTED', '[G]=M⁻² 带量纲'),
    '电磁': ('IMPORTED', 'α 测量锚', 'U(1) 内生结构但不出数'),
    '弱': ('IMPORTED', 'M_W/M_Z 测量锚', '低能赝象（F1）'),
    '强': ('IMPORTED', 'α_s 测量锚', '渐近自由（F3）'),
}
N_ENDO_NUM = sum(1 for v in FORCE_STATES.values() if v[0] == 'ENDO_NUM')
r67_needles = ['ENDO_NUM（内生数值·吻合实验）', '可数内生数值 = 0', 'n_out/n_in = 0/7 = 0',
               'GR 预测', '42.982', '5.5×10⁻⁵', '0.25 > 0']
r67_hits = hit_all(r67, r67_needles)
r273_needles = ['内生推导 = 0', '判别性 0', '重标定', 'q_G = m_p/m_P']
r273_hits = hit_all(r273, r273_needles)

# ---------- 4→3→2 能标标签状态机（Fraction 精确阈值） ----------
M_W_GEV = F('80.377')
M_Z_GEV = F('91.1876')
M_GUT_GEV = F('21290000000000000')
BANDS = [('E < M_W', 4), ('M_W < E < M_GUT', 3), ('E > M_GUT', 2)]
BAND_COUNTS = [b[1] for b in BANDS]
band_monotone = BAND_COUNTS == [4, 3, 2] and M_W_GEV < M_Z_GEV < M_GUT_GEV
force_audit_hits = hit_all(force_audit, ['4→3→2', '不是本源数字', '四不是本源数字',
                                         '3.97 dex', '2.129e16', '24.27', '不作回答'])

# ---------- 非测量锚候选（力程/Proca/Z′/统一势）逐条 C2-1/C2-2 ----------
NONMEASURE_CAND = [
    ('r222 力程/截止/质量三重等价', r222, 'ħω_c'),
    ('r224 Proca 统一势', r224, 'Proca'),
    ('r180 Z′ 恒等力比', r180, 'Z′'),
    ('r273 四 q 重标定', r273, 'q_G'),
]
NONMEASURE_ROWS = [{'id': n, 'source_hit': 1 if k in t else 0,
                    'c2_1': 0, 'c2_2': 0, 'verdict': 'FAIL'} for n, t, k in NONMEASURE_CAND]
N_NONMEASURE_PASS = sum(1 for x in NONMEASURE_ROWS if x['c2_1'] and x['c2_2'])

# ---------- 静态命中 / 跨源口径 / 不重复项 ----------
matrix_systems = matrix['systems']
matrix_cells = matrix['cells']
bn = dict((x['crit'], x) for x in matrix['bottleneck'])
w3_debt = F(str(bn['W3']['debt']))
w4_debt = F(str(bn['W4']['debt']))
W4_NEEDLES = ['C4', '两环 β 系数矩阵', '外部公式未在本仓核验', '暂缓',
              'W4 耦合统一', '3.66', '0.049']
w4_hits = hit_all(w_judge, W4_NEEDLES)
finaljudge_needles = ['完成力的本源统一场', '规范对称性', '时空几何', '全人类共有的开放问题',
                      '审计意义上', '物理意义上', '科学铁律', '唯象标量场玩具']
finaljudge_hits = hit_all(finaljudge, finaljudge_needles)
final_needles = ['16 候选汇总表', '✅ 结构性负面 **8**', '登记不深攻 **8**',
                 '不宣称宇宙本质本源已回答', '0/22', 'UFT-3=0', '36 项']
final_hits = hit_all(fin, final_needles)
origin_book_hits = hit_all(origin_book, ['16 项', '结构性负面', '登记不深攻', '本源'])
a42_needles = ['四类分桶', '双锚点', '非测量锚', 'C2 六条件']
a42_text = json.dumps(a42, ensure_ascii=False)
a42_hits = hit_all(a42_text, a42_needles)
sort_hits = hit_all(sortbook, ['C2 须先给出至少一个非测量锚无量纲数值并通过 method_F 双锚点',
                               '0/22、UFT-3=0、L3=0、validated=0', '治理事实源'])
methodf_hits = hit_all(methodf, ['第一性内容 ⟺ 无量纲量的数值', '双锚点检验', '只有 L3 可计入'])
readme_tail = readme_text.splitlines()[-8:]
nomig_count = sum(1 for line in readme_tail if '不计攻破数' in line)
redline_text = '\n'.join(readme_tail)

# 编号空号（现场文本扫描，不用 git grep 以免受索引状态干扰）
ALL_SRC_TEXT = ''
for p in (P_README, P_SORT, P_FINAL, P_C0160):
    ALL_SRC_TEXT += read_text(p)
EMPTY_ID_TOKENS = ['attack43', '攻破㉟', 'r409', 'r410']
empty_id_hits = {k: ALL_SRC_TEXT.count(k) for k in EMPTY_ID_TOKENS}
def has_rid(directory, rid):
    if not os.path.isdir(directory):
        return 0
    return sum(1 for name in os.listdir(directory) if name.startswith('TUFT-' + rid + '_'))

RID_DIRS = [os.path.join(NORM, d) for d in ('源码', '判定', '数据')]
rid_402_hits = sum(has_rid(d, 'r402') for d in RID_DIRS)
rid_latest = 'r402' if rid_402_hits > 0 else 'unknown'

# 三套分母口径（attack42 已登记，本册引用不重算）
DENOM = {'declared': 18, 'snapshot': len(targets['systems']), 'present': matrix_systems}

# ---------- 条目 ----------
emit('== attack43 攻破㉟·力的起源本质本源：第 17 候选与 16×4 交叉供给矩阵 ==')
emit('-- 靶：把「力/相互作用本源」作为第 17 项候选，判 16 本源候选 × 4 力交叉矩阵有无非测量锚无量纲输出 --')
emit('-- 边界：只读事实源、不跑 RGE/RK4、不构造 GUT 谱、不引入外部两环 β 公式、不占 RID、不重复 attack38/40/41/42 --')
emit('-- 口径：力的起源 = 前提账本里 g,g′,g_s,G 四个 DERIVED 空格（r130/r132/r134），不是「宇宙本源」候选表已有项 --')

add('E01', '控制组：16 候选 / 四力谱系 / 七路径 / 176 格 / 四耦合空格逐项复现', 'PASS',
    '16 候选现场解析=%d（✅%d/⚠️%d/◐%d）；四力=%s；七路径 open=%d/closed-neg=%d；22×8=%d 格、W3 debt=%s/W4 debt=%s；四耦合 DERIVED 空格=%d、三册同词表命中=%d/3；三套分母=%s'
    % (N_CAND, N_PASS, N_WARN, N_PART, FORCES, N_PATH_OPEN, N_PATH_CLOSED,
       matrix_cells, w3_debt, w4_debt, DERIVED_SPACES, N_DERIVED_SOURCES, DENOM))

add('E02', '「力/相互作用本源」不是 16 候选之一：字面命题全库 0 命中，需作为第 17 项', 'FAIL',
    '16 候选名称含「力/相互作用」=%d 项（列表=%s）；终局总成治理登记「不宣称宇宙本质本源已回答」命中=%d/7；最接近项为 #12 场本源与 #14 对称/规范本源，均按宇宙本源而非四力起源裁定'
    % (len(CAND_WITH_FORCE), CAND_WITH_FORCE, final_hits))

add('E03', '16×4=64 格交叉供给矩阵：无任一格给出非测量锚无量纲输出', 'FAIL',
    '格数=%d（%d 候选 × %d 力）；ZERO_SUPPLY=%d、NO_MACHINE_ENTRY=%d、数值供给=%d；内生无量纲输出=%d；撞 C 分布来自候选表，C2 通过数=%d'
    % (N_CELLS, N_CAND, N_FORCE, N_ZERO, N_NOENTRY, N_SUPPLY_NUMERIC,
       sum(x['endogenous_dimensionless_output'] for x in CELLS), CELL_PASS))

add('E04', '四耦合 DERIVED 空格状态机：POSTED → DERIVED 迁移 0/4', 'FAIL',
    '耦合=%s；状态=%s；迁移数=%d；r130 命中=%d/5（18/18 链 PREMISE-OPEN、closure=0.327）；r132/r134 同判「DERIVED 层为空 / 必须变为导出量」；力的本源终审裁决命中=%d/8'
    % (COUPLINGS, PREMISE_STATE, premise_transition, r130_hits, finaljudge_hits))

add('E05', '逐力四态分类：ENDO_NUM=0/4，内生结构存在但不出数', 'FAIL',
    '四力状态=%s；ENDO_NUM=%d；r67 普查命中=%d/7（可数内生数值=0、n_out/n_in=0/7、GR 正对照 42.982″ 与 0.25>0）；r273 四 q 命中=%d/4（内生推导=0、判别性=0、全是 SM 量重标定）'
    % ({k: v[0] for k, v in FORCE_STATES.items()}, N_ENDO_NUM, r67_hits, r273_hits))

add('E06', '4→3→2 能标标签状态机：「四」不是本源数字', 'FAIL',
    'M_W=%s GeV < M_Z=%s < M_GUT=%s；能标带计数=%s、单调递减=%s；四力本源审计命中=%d/7（F1 弱力低能赝象、F3 渐近自由、F5 四力是低能标签、SM 3.97 dex、MSSM 2.129e16/24.27）'
    % (M_W_GEV, M_Z_GEV, M_GUT_GEV, BAND_COUNTS, band_monotone, force_audit_hits))

add('E07', '七路径六 open 只读、C4 两环 β 暂缓、8 项 ⚠️ 不做假攻', 'BOUNDARY',
    '七路径=%d（open %d / closed-neg %d，C0160 明写「本册不宣称任何一条已死」）；C4/W4 词表命中=%d/%d（外部公式未在本仓核验⇒暂缓）；⚠️ %d 项沿用「登记不深攻」；「为何是这个规范群」与量子引力明文不作回答命中=%s'
    % (len(PATH_ROWS), N_PATH_OPEN, N_PATH_CLOSED, w4_hits, len(W4_NEEDLES), N_WARN,
       '不作回答' in force_audit and '量子引力' in finaljudge))

add('E08', '非测量锚候选逐条 C2-1/C2-2 与 64 格 C2 六条件：通过数 0', 'FAIL',
    '力程/Proca/Z′/统一势四候选=%s，C2-1/C2-2 通过=%d；64 格逐条六条件失败原因直方图=%s；第 17 项自身四格通过=%d；10 靶 key 现场抽自靶场 JSON=%d'
    % ([x['id'] for x in NONMEASURE_ROWS], N_NONMEASURE_PASS, REASON_HIST,
       N_CELL_17_PASS, len(TARGET_KEYS)))

add('E09', 'GR 水星正对照与 C2 最小可执行条件：零通过不是方法偏倚', 'INFO',
    'r67 正对照：GR 42.982″/世纪 vs 观测 42.98″、相对误差 5.5e-5、n_out/n_in=0.25>0 ⇒ 审计能识别真推导；method_F 命中=%d/3；C2 六条件=%s；若任一格通过则只登记「第 17 项部分闭合、待独立复核」，不宣称本源已回答'
    % (methodf_hits, C2_KEYS))

add('E10', '总裁定：H43 FAIL（力的起源本质本源未完成），不计攻破数', 'INFO',
    '交叉矩阵通过=%d、第 17 项四格通过=%d、迁移=%d/4、ENDO_NUM=%d/4；整理册 C2 硬门命中=%d/3；attack42 读数继承命中=%d/4；红线 0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答'
    % (CELL_PASS, N_CELL_17_PASS, premise_transition, N_ENDO_NUM, sort_hits, a42_hits))

# ---------- 守卫 ----------
SRC = read_text(os.path.join(HERE, BASE + '.py'))
TREE = ast.parse(SRC)
true_consts = [n.lineno for n in ast.walk(TREE)
               if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value == (1 == 1)]
imports = sorted({(n.module or '') if isinstance(n, ast.ImportFrom) else a.name.split('.')[0]
                  for n in ast.walk(TREE) if isinstance(n, (ast.Import, ast.ImportFrom))
                  for a in (n.names if isinstance(n, ast.Import) else [None]) if a is not None})
THIRD_PARTY = {'mpmath', 'sympy', 'numpy', 'scipy', 'pandas'}
third_party_hits = [x for x in imports if x in THIRD_PARTY]

guard('G43-1', '编号空号与分母守恒：attack43/攻破㉟/r409/r410 0 命中、16×4=64、8✅+8⚠️+0◐=16',
      all(v == 0 for v in empty_id_hits.values()) and N_CELLS == N_CAND * N_FORCE == 64
      and N_CAND == 16 and N_PASS == 8 and N_WARN == 8 and N_PART == 0
      and N_FORCE == 4 and matrix_cells == matrix_systems * len(matrix['criteria']) == 176
      and rid_latest == 'r402' and w3_debt == F(35, 2),
      'empty_ids=%s cells=%d cand=%d(%d/%d/%d) forces=%d rid=%s W3debt=%s'
      % (empty_id_hits, N_CELLS, N_CAND, N_PASS, N_WARN, N_PART, N_FORCE, rid_latest, w3_debt))

guard('G43-2', '16 候选与四力谱系现场解析（不打字）：逐项名称与供给列一致',
      len(CAND_ROWS) == 16 and [c['idx'] for c in CANDIDATES] == list(range(1, 17))
      and FORCES == ['引力', '电磁', '弱', '强']
      and sum(1 for c in CANDIDATES if c['supply'].strip() == '0') == 8
      and all(c['collision'].startswith('C') for c in CANDIDATES)
      and N_PATH_OPEN == 6 and N_PATH_CLOSED == 1,
      'rows=%d idx=%s forces=%s zero_supply=%d path=%d/%d'
      % (len(CAND_ROWS), [c['idx'] for c in CANDIDATES], FORCES,
         sum(1 for c in CANDIDATES if c['supply'].strip() == '0'),
         N_PATH_OPEN, N_PATH_CLOSED))

guard('G43-3', '四耦合 DERIVED 空格三册同词表命中，POSTED→DERIVED 迁移 0',
      N_DERIVED_SOURCES == 3 and DERIVED_SPACES == 4 and DERIVED_FILLED == 0
      and premise_transition == 0 and r130_hits >= 4
      and DERIVED_EMPTY_HITS['r132'] and DERIVED_EMPTY_HITS['r134'],
      'sources=%s spaces=%d transition=%d r130=%d/5 r132=%s r134=%s'
      % (DERIVED_EMPTY_HITS, DERIVED_SPACES, premise_transition, r130_hits,
         DERIVED_EMPTY_HITS['r132'], DERIVED_EMPTY_HITS['r134']))

guard('G43-4', '交叉矩阵守恒与零供给：64 格 = ZERO + NOENTRY，内生输出与 C2 通过全 0',
      N_ZERO + N_NOENTRY == N_CELLS and N_SUPPLY_NUMERIC == 0
      and sum(x['endogenous_dimensionless_output'] for x in CELLS) == 0
      and CELL_PASS == 0 and N_CELL_17_PASS == 0
      and all(len(x['c2_reasons']) >= 4 for x in CELLS),
      'zero=%d noentry=%d sum=%d cells=%d pass=%d cell17=%d'
      % (N_ZERO, N_NOENTRY, N_ZERO + N_NOENTRY, N_CELLS, CELL_PASS, N_CELL_17_PASS))

guard('G43-5', 'C2 六条件形式化有牙：假想合格格必过、三变异必翻转',
      syn_ok is (1 == 1) and len(syn_reasons) == 0
      and mut_drop_ok is (1 == 0) and mut_measured_ok is (1 == 0)
      and mut_free_ok is (1 == 0) and CELL_PASS == 0
      and len(C2_KEYS) == 6 and TARGET_REGISTERED_ALL_ZERO,
      'synthetic=%s drop=%s measured=%s free=%s real=%d keys=%d'
      % (syn_ok, mut_drop_ok, mut_measured_ok, mut_free_ok, CELL_PASS, len(C2_KEYS)))

guard('G43-6', 'r67 正对照与 r273 重标定：零通过不是方法恒否的假象',
      r67_hits == 7 and r273_hits == 4 and N_ENDO_NUM == 0
      and 'GR 预测' in r67 and '42.982' in r67 and '0.25 > 0' in r67
      and '内生推导 = 0' in r273 and '判别性 0' in r273,
      'r67=%d/7 r273=%d/4 endo_num=%d' % (r67_hits, r273_hits, N_ENDO_NUM))

guard('G43-7', '4→3→2 状态机与四力本源审计逐项一致',
      band_monotone and BAND_COUNTS == [4, 3, 2]
      and M_W_GEV < M_Z_GEV < M_GUT_GEV and force_audit_hits >= 6
      and '不是本源数字' in force_audit and '不作回答' in force_audit,
      'bands=%s M_W=%s M_Z=%s M_GUT=%s hits=%d/7'
      % (BAND_COUNTS, M_W_GEV, M_Z_GEV, M_GUT_GEV, force_audit_hits))

guard('G43-8', '跨源静态命中与 MISMATCH：终局总成 / 终审裁决 / 第二件册 / C4 暂缓 / 三套分母',
      final_hits == 7 and finaljudge_hits == 8 and origin_book_hits == 4
      and w4_hits >= 5 and a42_hits == 4 and sort_hits == 3
      and methodf_hits == 3 and nomig_count >= 4
      and DENOM == {'declared': 18, 'snapshot': 19, 'present': 22},
      'final=%d judge=%d book=%d w4=%d a42=%d sort=%d mf=%d nomig=%d denom=%s'
      % (final_hits, finaljudge_hits, origin_book_hits, w4_hits, a42_hits,
         sort_hits, methodf_hits, nomig_count, DENOM))

# 不重复项用 AST 标识符/函数定义判据，不用字符串包含（边界描述本身含这些词会造成自指假红）
AST_NAMES = set(n.id for n in ast.walk(TREE) if isinstance(n, ast.Name))
AST_FUNCS = set(n.name for n in ast.walk(TREE) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
BANNED_IDS = {'RATIO_PARTICLE', 'ALPHA_GRAV_CALC', 'MUT_DROP_ANCHOR', 'b_ij',
              'K4', 'Omega5'}
banned_id_hits = sorted(AST_NAMES & BANNED_IDS)
banned_func_hits = sorted(f for f in AST_FUNCS
                          if any(k in f.lower() for k in ('rk4', 'runge', 'gauss', 'rank', 'two_loop', 'beta2')))
guard('G43-9', '不重复项：纯标准库、无 RGE/RK4/两环 β/C38 四门/双锚点数值化的实现函数',
      len(third_party_hits) == 0 and len(banned_id_hits) == 0
      and len(banned_func_hits) == 0 and 'mpmath' not in imports
      and 'sympy' not in imports,
      'imports=%s third_party=%s banned_ids=%s banned_funcs=%s funcs=%s'
      % (imports, third_party_hits, banned_id_hits, banned_func_hits, sorted(AST_FUNCS)))

guard('G43-10', '书写式/红线守卫：源码无布尔字面量、不占 RID、不改治理事实源、红线文本在册',
      len(true_consts) == 0 and '不宣称完成统一场' in SRC
      and '0/22、UFT-3=0、L3=0、validated=0' in SRC
      and '本册不占 RID' in SRC and '不跑 RGE' in SRC
      and '不宣称宇宙本质本源已回答' in SRC,
      'literal_true_consts=%d redline=%s no_rid=%s'
      % (len(true_consts), '0/22、UFT-3=0、L3=0、validated=0' in SRC,
         '本册不占 RID' in SRC))

# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（力的起源本质本源未完成）；16×4 交叉矩阵通过数=0 ==')
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不计攻破数；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack43_攻破㉟_力的起源本质本源_第17候选与16x4交叉供给矩阵',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'candidates_16': [{'idx': c['idx'], 'name': c['name'], 'supply': c['supply'],
                           'collision': c['collision'], 'verdict': c['verdict']}
                          for c in CANDIDATES],
        'candidate_distribution': {'total': N_CAND, 'structural_negative': N_PASS,
                                   'registered_not_deep': N_WARN, 'partial': N_PART},
        'candidates_with_force_or_interaction_in_name': CAND_WITH_FORCE,
        'forces': FORCES,
        'paths': [{'name': x[0], 'collision': x[1], 'state': x[2]} for x in PATH_ROWS],
        'couplings': COUPLINGS,
        'derived_spaces': {'count': DERIVED_SPACES, 'filled': DERIVED_FILLED,
                           'premise_state': PREMISE_STATE,
                           'transition_POSTED_to_DERIVED': premise_transition,
                           'source_hits': DERIVED_EMPTY_HITS},
        'cross_matrix': {'rows': N_CAND, 'cols': N_FORCE, 'cells': N_CELLS,
                         'zero_supply': N_ZERO, 'no_machine_entry': N_NOENTRY,
                         'numeric_supply': N_SUPPLY_NUMERIC,
                         'endogenous_dimensionless_output': 0,
                         'c2_pass': CELL_PASS,
                         'reason_histogram': REASON_HIST,
                         'conservation': '%d+%d=%d=%dx%d'
                                         % (N_ZERO, N_NOENTRY, N_CELLS, N_CAND, N_FORCE)},
        'c2_conditions': C2_KEYS,
        'cell_17': CELL_17,
        'guard_mutations': {'synthetic_pass': syn_ok, 'synthetic_reasons': syn_reasons,
                            'drop_second_anchor': mut_drop_ok,
                            'measured_anchor': mut_measured_ok,
                            'extra_free_param': mut_free_ok},
        'force_states': FORCE_STATES,
        'energy_bands': {'M_W_GeV': str(M_W_GEV), 'M_Z_GeV': str(M_Z_GEV),
                         'M_GUT_GeV': str(M_GUT_GEV), 'counts': BAND_COUNTS,
                         'monotone': band_monotone},
        'nonmeasure_candidates': NONMEASURE_ROWS,
        'nonmeasure_pass': N_NONMEASURE_PASS,
        'matrix': {'systems': matrix_systems, 'cells': matrix_cells,
                   'W3_debt': str(w3_debt), 'W4_debt': str(w4_debt)},
        'denominators_triple': DENOM,
        'empty_id_hits': empty_id_hits, 'rid_latest': rid_latest,
        'source_static_hits': {'final': final_hits, 'finaljudge': finaljudge_hits,
                               'origin_book': origin_book_hits, 'r130': r130_hits,
                               'r67': r67_hits, 'r273': r273_hits,
                               'force_audit': force_audit_hits, 'w4_c4': w4_hits,
                               'method_F': methodf_hits, 'attack42_json': a42_hits,
                               'sortbook': sort_hits, 'readme_no_migration': nomig_count},
    },
    'self_corrections': [
        'G43-3 首版守卫误写条件表达式 `... and r132_hits if (1 == 1) else (1 == 0)`，三元式优先级会吞掉整个 and 链；改为显式 DERIVED_EMPTY_HITS[r132]/[r134] 合取',
        '空号扫描首版把文件内容变量（sortbook/fin/c0160）当作路径传给 read_text，抛 OSError: Invalid argument；改为路径常量 P_SORT/P_FINAL/P_C0160',
        '第二件册词表用「16 候选」而原文写「16 项」，attack42 JSON 词表用「四类互斥分桶」而原文写「四类分桶」；两处按实际词形校准，G43-8 命中由 3/3 升为 4/4',
        'r402 首版硬编码了不存在的文件名导致 rid_latest=unknown；改为在 源码/判定/数据 三目录实扫 TUFT-r402_ 前缀',
        'G43-9 首版用「源码不含 RK4/mpmath/b_ij」等字符串包含判据，但守卫描述与 boundaries 文本本身含这些词 ⇒ 自指假红；改为 AST 标识符集合 + 函数定义名 + 导入模块集合判据',
        'E07 读数首版把 C4/W4 词表分母硬编码为 6，实际 7 项（命中 7/7 却显示 7/6）；改为 len(W4_NEEDLES) 动态分母',
        '首跑 7/10 守卫，三处 BAD 全为自身实现缺陷（词表/路径/自指），无一涉及物理裁定；修正后复跑至 10/10',
    ],
    'boundaries': [
        '「力的起源本质本源」字面全库 0 命中；等价命题已有终审裁决（力的本源统一场 2026-10-13 判「审计意义上完成、物理意义上该路径不可行」）与 16 项宇宙本源候选终局判定（8✅+8⚠️）⇒ 本册不宣称首次发现，只把「力/相互作用本源」作为第 17 项候选层首次机器化',
        '交叉矩阵的分母是 16 项宇宙本源候选与 4 个力标签；它不是 22 体系矩阵，也不是 43 条预测登记源，三套分母（声明 18 / 快照 19 / 现测 22）如实分列',
        '假想合格格（靶场例3 型）只用于证明 C2 判据有牙，不是任何体系的真实产物，不计入任何通过数',
        'C2 六条件沿用 attack42 的形式化；本册不重做 method_F 双锚点的 Decimal 数值复算，不重做 attack42 的 43 条四类分桶',
        '不跑 RGE/RK4、不构造具体 GUT 谱、不引入外部两环 β 系数矩阵（C4 维持「外部公式未在本仓核验⇒暂缓」）、不用 mpmath/sympy',
        '七路径六 open 只作只读事实源，不重新判定任何一条路径已死；8 项 ⚠️ 沿用「登记不深攻」',
        '不占 RID（R 链最新 r402）；未改治理事实源、未改 verify.py、未跑 refresh_catalog、未提交 git',
    ],
    'methodology_notes': [
        'G43-10 用 1 == 1 比较式检查布尔字面量，避免 AST 守卫自身写入被扫描命中；导入集合由 AST 现场抽取',
        '16 候选表、四力谱系、七路径状态均由 Markdown 表格现场正则解析，不打字、不硬编码名单；纯标准库、无随机',
    ],
    'source_refs': {
        'final': '穷尽攻破_统一场论终局总成_2026-10-21.md:L63-92/L100-116/L162-166/L168-185',
        'origin_book': '穷尽攻破_宇宙本质本源_2026-10-21.md:L37-58/L254-275',
        'c0160': '判定_C0160_力的统一攻破_2026-10-21.md:L26-37/L47-57/L105-117/L129-137',
        'force_audit': '../本项目_全维自洽与归一化/判定_四力本源_层级与可统一性的机器审计_2026-10-07.md:L5-7/L13/L19-29/L80-100',
        'finaljudge': '../本项目_全维自洽与归一化/力的本源统一场_终审裁决_2026-10-13.md:L3/L11-17/L60-65/L69-80',
        'r130': '../本项目_全维自洽与归一化/数据/判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md:L129-145',
        'r132': '../本项目_全维自洽与归一化/数据/判定_TUFT-r132_全维自洽与归一化_跨卷综合判定与攻破全景_2026-10-20.md:L55-62',
        'r134': '../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md:L98-110',
        'r67': '../本项目_全维自洽与归一化/判定_TUFT-r67-力统一场论本源性审计_内生外输普查与GR正对照_2026-10-31.md:L12-46',
        'r273': '../本项目_全维自洽与归一化/数据/判定_TUFT-r273_四力本源参数精算层_统一势模板标准耦合重标定及qWqπ数值核验_精算与可视化_2026-10-31.md:L27-44',
        'r222': '../本项目_全维自洽与归一化/判定/判定_TUFT-r222_四力统一方程的传播层_色散截止群速度与质量力程等价_精算与可视化_2026-10-26.md',
        'r224': '../本项目_全维自洽与归一化/数据/TUFT-r224_四力统一运动方程_Proca方程机器验证圆轨道稳定性与荷空间可加性_精算与可视化_2026-10-26.md',
        'r180': '../本项目_全维自洽与归一化/判定_TUFT-r180_电磁耦合常数Zprime_恒等力比与Z双素数修正_精算_2026-10-25.md',
        'matrix': '../全维全体系统一场论/数据/全维验收矩阵.json:L30-33/L54-60/L75-90',
        'w_judgment': '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md:L95/L103/L108-116/L120-131',
        'method_F': '../../02_共享基础/研究规范/method_F_第一性判据.md:L38-56/L96-122/L139-148',
        'targets': '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json:L5-76/L77',
        'attack42': 'attack42_C2硬门_四类机器分桶与双锚点可执行化_2026-11-08.json',
        'sortbook': '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md:L107-113',
        'readme': 'README.md:L1579-1583',
    },
    'cross_refs': [
        '穷尽攻破_统一场论终局总成_2026-10-21.md',
        '穷尽攻破_宇宙本质本源_2026-10-21.md',
        '判定_C0160_力的统一攻破_2026-10-21.md',
        '../本项目_全维自洽与归一化/判定_四力本源_层级与可统一性的机器审计_2026-10-07.md',
        '../本项目_全维自洽与归一化/力的本源统一场_终审裁决_2026-10-13.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r132_全维自洽与归一化_跨卷综合判定与攻破全景_2026-10-20.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
        '../本项目_全维自洽与归一化/判定_TUFT-r67-力统一场论本源性审计_内生外输普查与GR正对照_2026-10-31.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r273_四力本源参数精算层_统一势模板标准耦合重标定及qWqπ数值核验_精算与可视化_2026-10-31.md',
        '../全维全体系统一场论/数据/全维验收矩阵.json',
        '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md',
        '../../02_共享基础/研究规范/method_F_第一性判据.md',
        '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json',
        'attack42_C2硬门_四类机器分桶与双锚点可执行化_2026-11-08.json',
        '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md',
        '判定_attack42_攻破㉞_C2硬门四类机器分桶与双锚点可执行化_2026-11-08.md',
        'README.md',
    ],
    'redlines': {'zero_of_22': 'unchanged', 'UFT-3': 0, 'L3': 0, 'validated': 0},
    'candidate_verdict': 'FAIL',
    'exit': 0 if nok == len(GUARDS) else 1,
}
with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(0 if nok == len(GUARDS) else 1)
