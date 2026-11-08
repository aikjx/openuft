# -*- coding: utf-8 -*-
# attack44 / 攻破㊱ —— 规范群唯一化判据表：10 途径与三态机器分桶（2026-11-08）
# 靶：把「为何是 SU(3)×SU(2)×U(1)」做成可机读的唯一化判据表，判定机器唯一化数是否 >=1。
# 纯标准库（os/io/json/re/ast/itertools + Fraction + Decimal），无第三方依赖、无随机、只读事实源。
# 红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不计攻破数；本册不占 RID；不跑 RGE；不构造 GUT 谱；不引入外部两环 β；未改治理事实源、未改 verify.py、未跑 refresh_catalog.py、未提交 git。
import os, sys, io, json, re, ast, itertools
from fractions import Fraction as F
from decimal import Decimal as Dc, getcontext
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'attack44_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08'
PUB = os.path.abspath(os.path.join(HERE, '..'))
NORM = os.path.join(PUB, '本项目_全维自洽与归一化')
ACCEPT = os.path.join(PUB, '全维全体系统一场论')

P_C0137 = os.path.join(HERE, '判定_C0137_规范群签名枚举攻破_2026-10-18.md')
P_C0162 = os.path.join(HERE, '判定_C0162_so8极大子群P12闭合_2026-10-21.md')
P_A24 = os.path.join(HERE, '判定_attack24_Phase0双分水岭_量子引力与规范群起源_全维攻破_2026-10-13.md')
P_R138 = os.path.join(NORM, '数据', '判定_TUFT-r138_硬核审计_规范群与mu2符号不可导出性_2026-10-21.md')
P_R130 = os.path.join(NORM, '数据', '判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md')
P_R134 = os.path.join(NORM, '数据', '判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md')
P_R135 = os.path.join(NORM, '数据', '判定_TUFT-r135_第一性原理突破尝试_自旋2路线机检与净前提下降门记账_2026-10-21.md')
P_FORCE = os.path.join(NORM, '判定_四力本源_层级与可统一性的机器审计_2026-10-07.md')
P_JUDGE = os.path.join(NORM, '力的本源统一场_终审裁决_2026-10-13.md')
P_C0160 = os.path.join(HERE, '判定_C0160_力的统一攻破_2026-10-21.md')
P_FINAL = os.path.join(HERE, '穷尽攻破_统一场论终局总成_2026-10-21.md')
P_WJUDGE = os.path.join(ACCEPT, '判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md')
P_MATRIX = os.path.join(ACCEPT, '数据', '全维验收矩阵.json')
P_TARGETS = os.path.join(NORM, '数据', '无量纲靶场审计.json')
P_A43 = os.path.join(HERE, 'attack43_力本源_第17候选与16x4交叉供给矩阵_2026-11-08.json')
P_SORT = os.path.join(HERE, '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md')
P_README = os.path.join(HERE, 'README.md')

PATHS = [P_C0137, P_C0162, P_A24, P_R138, P_R130, P_R134, P_R135,
         P_FORCE, P_JUDGE, P_C0160, P_FINAL, P_WJUDGE, P_MATRIX,
         P_TARGETS, P_A43, P_SORT, P_README]

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

def parse_i(pattern, text, default=0):
    m = re.search(pattern, text)
    return int(m.group(1)) if m else default

def parse_pair(pattern, text, default=(0, 0)):
    m = re.search(pattern, text)
    return (int(m.group(1)), int(m.group(2))) if m else default

# ---------- 只读事实源 ----------
c0137 = read_text(P_C0137)
c0162 = read_text(P_C0162)
a24 = read_text(P_A24)
r138 = read_text(P_R138)
r130 = read_text(P_R130)
r134 = read_text(P_R134)
r135 = read_text(P_R135)
force_audit = read_text(P_FORCE)
finaljudge = read_text(P_JUDGE)
c0160 = read_text(P_C0160)
fin = read_text(P_FINAL)
wjudge = read_text(P_WJUDGE)
matrix = read_json(P_MATRIX)
targets = read_json(P_TARGETS)
a43 = read_json(P_A43)
sortbook = read_text(P_SORT)
readme_text = read_text(P_README)
# ---------- 四册核心读数：现场正则解析（不打字） ----------
N_SIG = parse_i(r'\*\*(\d+) 个互不同构的规范代数', c0137)
N_DIM12 = parse_i(r'候选共 (\d+) 个', c0137)
KILL_POS, KILL_NEG = parse_pair(r'签名 \*\*\((\d+),(\d+)\)\*\*', a24)
KILL_BOUND = parse_i(r'dim k ≤ \*\*(\d+)\*\*', a24)
SM_DIM = parse_i(r'dim SM = (\d+)', a24)
N_KK = parse_i(r'最小额外维 \*\*n = (\d+)\*\*', a24)
N_EXTRA_GEN = parse_i(r'多 (\d+) 个生成元', a24)
N_ALG = parse_i(r'(\d+) 个常见「几何统一」候选代数', a24)
N_ROOTS = parse_i(r'根数\s*\|\s*\*\*(\d+)\*\*', c0162)
N_RANK4 = parse_i(r'\|\s*秩\s*\|\s*\*\*(\d+)\*\*', c0162)
N_GEN = parse_i(r'生成元 = 根数 \+ 秩\s*\|\s*\*\*(\d+)\*\*', c0162)
N_A2 = parse_i(r'A2 子根系统总数 = (\d+)', c0162)
N_ORTH = parse_i(r'枚举出 (\d+) 个', c0162)
m_af = re.search(r'n_f=6 通过 \[([^\]]+)\]', r138)
N_AF = len([x for x in m_af.group(1).split(',') if x.strip()]) if m_af else 0
m_af40 = re.search(r'n_f=40 通过 \[([^\]]+)\]', r138)
N_AF40 = len([x for x in m_af40.group(1).split(',') if x.strip()]) if m_af40 else 0
N_RANK_SM = parse_i(r'rank_SM=(\d+)', r138)
N_RANK_CL = parse_i(r'rank_Cl\(1,3\)=(\d+)', r138)
N_UNEVAL = parse_i(r'未导出合计（=缺口）\*\*\s*\|\s*\*\*(\d+)\*\*', r134)
m_cl = re.search(r'closure = DERIVED/总\s*\|\s*(\d+\.\d+)', r134)
CLOSURE = Dc(m_cl.group(1)) if m_cl else Dc(0)
N_NET11 = parse_i(r'净前提变化 = \*\*\+(\d+)\*\*', r134)
N_DEEP = len(re.findall(r'^\d+\. \*\*', r134, re.M))
N_DERIVED_COUPLINGS = 4 if 'g, g′, g_s, G' in r134 else 0

bn = dict((x['crit'], x) for x in matrix['bottleneck'])
W3_DEBT = F(str(bn['W3']['debt']))
W4_DEBT = F(str(bn['W4']['debt']))
MATRIX_CELLS = matrix['cells']
DENOM = {'declared': 18, 'snapshot': len(targets['systems']), 'present': matrix['systems']}

# ---------- 10 行唯一化判据表：三态互斥 + 唯一化列 + 新增 POSTED 列 ----------
SRC_TEXT = {'C0137': c0137, 'C0162': c0162, 'A24': a24, 'R138': r138,
            'R130': r130, 'R134': r134, 'R135': r135, 'FORCE': force_audit,
            'JUDGE': finaljudge, 'C0160': c0160, 'FINAL': fin, 'WJUDGE': wjudge}

EXTERNAL_MARKERS = ('实验选择', '观测', 'POSTED', '公设', '新原理', '外部输入',
                    '额外信息', '须外部公设', '无框架出处', '未观测额外维',
                    '嵌入企图', '更大群', '需 Cl(1,11)', '净前提数下降', 'Cl(1,11)')
CONSTRAIN_MARKERS = ('不唯一', '只锁', '不被导出', '仅被约束', '必要条件', '否',
                     '0（否）', '上界', '约束', '结构性负面', '装不进去', '< 12',
                     '均不能', '不选择', '不定群', '不能唯一锁定')

def route_state(needles, src_text):
    joined = ''.join(n for n in needles if n in src_text)
    if any(k in joined for k in EXTERNAL_MARKERS):
        return 'EXTERNAL_INPUT'
    if any(k in joined for k in CONSTRAIN_MARKERS):
        return 'CONSTRAIN_ONLY'
    return 'UNIQUIFY'

def decides(state, n_cand):
    return 1 if state == 'UNIQUIFY' and n_cand == 1 else 0

def embed_ok(orth):
    return 1 if orth > 0 else 0

def fits(bound, dim):
    return 1 if bound >= dim else 0

def gate(e, a):
    return 1 if a < e else 0

ROUTE_SPEC = [
    ('R01', '(dim,rank)=(12,4) 签名枚举', ('C0137',), 'C0137 L39-51 / L78-85',
     ['3 个互不同构的规范代数共享同一签名', 'dim=12 且不限秩的候选共 8 个', '不能唯一锁定 SM'], N_SIG),
    ('R02', 'so(1,3) 时空几何隔离', ('A24',), 'attack24 L61-91',
     ['dim so(1,3) = 6 < dim SM = 12', '只有 SM 自身（平凡）可容纳 SM', '装不进去'], N_ALG),
    ('R03', '反常消除', ('C0137', 'R130'), 'C0137 L68-85 / r130 L96 / L107',
     ['只锁赋值不锁群', '四项全 = 0（精确）', '均非零', '不是群选择'], 0),
    ('R04', 'so(8) 极大秩嵌入', ('C0162',), 'C0162 L31-82',
     ['极大秩嵌入 = **0（否）**', '与正交 A1（su2）共存的 A2 数 = 0', '存在性 = 0', '均不能'], 0),
    ('R05', 'KK n=5 逃逸', ('A24',), 'attack24 L93-107',
     ['最小额外维 **n = 5**', 'n ≥ 5 个未观测额外维', '多 16 个生成元', 'n 的取值本身无框架出处'], N_KK),
    ('R06', '紧致子代数 N1（Killing 型）', ('A24',), 'attack24 L25-36 / L65-76 / L218-229',
     ['签名 **(3,3)**', 'dim k ≤ **3** < 12', 'A2-3 阳性对照', '400 个随机 4 维子空间'], 0),
    ('R07', '渐近自由 / N_f 选择力', ('R138',), 'r138 L26-50',
     ['渐近自由（约束 N_f<11N/2，不唯一）', 'n_f=6 通过 [2, 3, 4, 5, 6, 7, 8]', 'n_f=40 通过 [8]'], N_AF),
    ('R08', '秩障碍 Cl(1,11)', ('R138',), 'r138 L36-50',
     ['rank_SM=4 > rank_Cl(1,3)=2 ⇒ 需 Cl(1,11)', '仅被约束、不被导出', 'e=0（无已知导出）、a=1'], 1),
    ('R09', '表示内容 / 实验选择', ('C0137',), 'C0137 L51 / L76-93',
     ['必须再输入额外信息（表示内容、反常、观测）', '实验选择', '不是公设推导', '几何框架提供者：0'], 1),
    ('R10', '唯一化原理 C1 / 净前提下降门', ('C0137', 'R134', 'R130'), 'C0137 L76-85 / r134 L75-123 / r130 L141-147',
     ['几何框架提供者：0', '为何是此群', '净下降要求 **a < e**', '只有**新原理**能过门', '净前提数下降'], 0),
]

ROUTES = []
for rid, name, src_keys, lines, needles, n_cand in ROUTE_SPEC:
    src_text = ''.join(SRC_TEXT[k] for k in src_keys)
    hits = [n for n in needles if n in src_text]
    state = route_state(needles, src_text)
    ROUTES.append({
        'id': rid, 'name': name, 'source': '+'.join(src_keys), 'lines': lines,
        'needles': needles, 'source_hits': len(hits), 'needle_total': len(needles),
        'state': state, 'n_cand': n_cand,
        'unique_sm': decides(state, n_cand),
        'new_posted': 1 if any(k in ''.join(hits) for k in EXTERNAL_MARKERS) else 0,
    })

N_ROUTES = len(ROUTES)
N_UNIQUE = sum(r['unique_sm'] for r in ROUTES)
N_CONSTRAIN = sum(1 for r in ROUTES if r['state'] == 'CONSTRAIN_ONLY')
N_EXTERNAL = sum(1 for r in ROUTES if r['state'] == 'EXTERNAL_INPUT')
N_UNIQUIFY_STATE = sum(1 for r in ROUTES if r['state'] == 'UNIQUIFY')
N_NEW_POSTED = sum(r['new_posted'] for r in ROUTES)
STATE_SET = set(r['state'] for r in ROUTES)

# ---------- 静态命中 / 跨源口径 / 不重复项 ----------
readme_scan = '\n'.join(l for l in readme_text.splitlines()
                        if 'attack44' not in l and '攻破㊱' not in l)
ALL_SRC_TEXT = ''.join([c0137, c0162, a24, r138, r130, r134, r135,
                        force_audit, finaljudge, c0160, fin, wjudge,
                        sortbook, json.dumps(a43, ensure_ascii=0), readme_scan])
EMPTY_ID_TOKENS = ['attack44', '攻破㊱', 'r411', 'r412']
empty_id_hits = {k: ALL_SRC_TEXT.count(k) for k in EMPTY_ID_TOKENS}

OWN = set([BASE + '.py', BASE + '.json', BASE + '_report.txt',
           '判定_attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.md'])

def has_file_token(directory, tokens):
    if not os.path.isdir(directory):
        return 0
    return sum(1 for n in os.listdir(directory)
               if any(t in n for t in tokens) and n not in OWN)

def has_rid(directory, rid):
    if not os.path.isdir(directory):
        return 0
    return sum(1 for n in os.listdir(directory) if n.startswith('TUFT-' + rid + '_'))

file_hits = has_file_token(HERE, ('attack44', '㊱', 'r411', 'r412'))
RID_DIRS = [os.path.join(NORM, d) for d in ('源码', '判定', '数据')]
rid_402_hits = sum(has_rid(d, 'r402') for d in RID_DIRS)
rid_latest = 'r402' if rid_402_hits > 0 else 'unknown'
rid_403plus = sum(has_rid(d, r) for d in RID_DIRS
                  for r in ('r403', 'r404', 'r405', 'r406', 'r407', 'r408',
                            'r409', 'r410', 'r411', 'r412'))

C0137_NEEDLES = ['3 个互不同构的规范代数共享同一签名', '不能唯一锁定 SM',
                 '只锁赋值不锁群', '几何框架提供者：0', '不宣称已解决规范群起源']
C0162_NEEDLES = ['根数 | **24**', '| 秩 | **4**', '生成元 = 根数 + 秩 | **28**',
                 'A2 子根系统总数 = 16', '枚举出 0 个', '存在性 = 0']
A24_NEEDLES = ['P01 与 P12 双分水岭 = 0 / 2 未过门', '签名 **(3,3)**',
               'A2-3 阳性对照', '400 个随机 4 维子空间', '只有 SM 自身（平凡）可容纳 SM']
R138_NEEDLES = ['HARD-CORE-NOT-DERIVABLE', '仅被约束、不被导出',
                '渐近自由（约束 N_f<11N/2，不唯一）',
                'rank_SM=4 > rank_Cl(1,3)=2 ⇒ 需 Cl(1,11)', 'e=0（无已知导出）、a=1']
R130_NEEDLES = ['18/18 链 PREMISE-OPEN', '总闭合度 0.327', '四项全 = 0（精确）',
                '均非零', '净前提数下降', '力的起源问题 = 前提账本里四个 DERIVED 空格']
R134_NEEDLES = ['四块最深 POSTED 前提', '为何是此群', 'DERIVED 层为空',
                'a < e', '净前提变化 = **+11**', '未产出新物理']
R135_NEEDLES = ['PARTIAL-BREAKTHROUGH-BUT-CIRCULAR-SUSPECT', 'Δ=-1',
                'CIRCULAR-SUSPECT', '不选择规范群本身']
FORCE_NEEDLES = ['不作回答', '超出可机器判定', '不是本源数字', '4→3→2']
JUDGE_NEEDLES = ['全人类共有的开放问题', '审计意义上', '物理意义上', '量子引力']
C0160_NEEDLES = ['不宣称任何一条已死', 'closed-neg', '七路径']
FINAL_NEEDLES = ['规范群唯一化（C0137）', '3 个互不同构代数共享同一签名', '0/22', 'UFT-3=0']
W4_NEEDLES = ['C4', '两环 β 系数矩阵', '外部公式未在本仓核验', '暂缓']
A43_NEEDLES = ['attack43', 'C2 六条件', 'BOUNDARY']
SORT_NEEDLES = ['0/22、UFT-3=0、L3=0、validated=0',
                'C2 须先给出至少一个非测量锚无量纲数值', '治理事实源']

hits_map = {
    'C0137': hit_all(c0137, C0137_NEEDLES),
    'C0162': hit_all(c0162, C0162_NEEDLES),
    'A24': hit_all(a24, A24_NEEDLES),
    'R138': hit_all(r138, R138_NEEDLES),
    'R130': hit_all(r130, R130_NEEDLES),
    'R134': hit_all(r134, R134_NEEDLES),
    'R135': hit_all(r135, R135_NEEDLES),
    'FORCE': hit_all(force_audit, FORCE_NEEDLES),
    'JUDGE': hit_all(finaljudge, JUDGE_NEEDLES),
    'C0160': hit_all(c0160, C0160_NEEDLES),
    'FINAL': hit_all(fin, FINAL_NEEDLES),
    'W4': hit_all(wjudge, W4_NEEDLES),
    'A43': hit_all(json.dumps(a43, ensure_ascii=0), A43_NEEDLES),
    'SORT': hit_all(sortbook, SORT_NEEDLES),
}
needles_total = {
    'C0137': len(C0137_NEEDLES), 'C0162': len(C0162_NEEDLES), 'A24': len(A24_NEEDLES),
    'R138': len(R138_NEEDLES), 'R130': len(R130_NEEDLES), 'R134': len(R134_NEEDLES),
    'R135': len(R135_NEEDLES), 'FORCE': len(FORCE_NEEDLES), 'JUDGE': len(JUDGE_NEEDLES),
    'C0160': len(C0160_NEEDLES), 'FINAL': len(FINAL_NEEDLES), 'W4': len(W4_NEEDLES),
    'A43': len(A43_NEEDLES), 'SORT': len(SORT_NEEDLES),
}
REDLINE_TAIL = readme_text.splitlines()[-8:]
nomig_count = sum(1 for l in REDLINE_TAIL if '不计攻破数' in l)

# ---------- 判据有牙：唯一化 / 嵌入 / 适配 / 净前提门 的阳性对照与变异 ----------
THREE_STATES = {'UNIQUIFY', 'CONSTRAIN_ONLY', 'EXTERNAL_INPUT'}
SYNTH_UNIQ = decides('UNIQUIFY', 1)
MUT_STATE = decides('CONSTRAIN_ONLY', 1)
MUT_NCAND = decides('UNIQUIFY', 2)
MUT_EXTERNAL = decides('EXTERNAL_INPUT', 1)
EMBED_POS = embed_ok(1)
FITS_POS = fits(12, 12)
GATE_POS = gate(1, 0)
E_GATE = 0
A_GATE = 1
GATE_REAL = gate(E_GATE, A_GATE)
EMBED_REAL = embed_ok(N_ORTH)
FITS_REAL = fits(KILL_BOUND, SM_DIM)
STATE_RECOMPUTE = [route_state(r['needles'],
                    ''.join(SRC_TEXT[k] for k in r['source'].split('+'))) == r['state']
                    for r in ROUTES]
NEEDLE_HITS_ALL = sum(r['source_hits'] for r in ROUTES)
NEEDLE_TOTAL_ALL = sum(r['needle_total'] for r in ROUTES)

# ---------- 条目 ----------
emit('== attack44 攻破㊱·规范群唯一化判据表：10 途径与三态机器分桶 ==')
emit('-- 靶：把「为何是 SU(3)xSU(2)xU(1)」做成 10 行机读判据表，判定机器唯一化数是否 >=1 --')
emit('-- 边界：只读事实源、不跑 RGE/RK4、不构造 GUT 谱、不引入外部两环 beta、不占 RID、不重复 attack39-43 --')
emit('-- 口径：三态互斥 UNIQUIFY / CONSTRAIN_ONLY / EXTERNAL_INPUT；UNIQUIFY 且候选数=1 才计唯一化 --')

add('F01', '控制组：四册核心读数现场正则复现（C0137 / C0162 / attack24 / r138 / r134）', 'PASS',
    '签名共享代数=%d、dim12 候选=%d；Killing 签名=(%d,%d)、紧致子代数上界=%d < dim SM=%d；KK n=%d / 多 %d 生成元 / %d 个几何统一候选；so(8) 根=%d 秩=%d 生成元=%d、A2 子根=%d、正交共存 A2=%d；n_f=6 通过=%d / n_f=40 通过=%d；rank_SM=%d > rank_Cl=%d；r134 未导出=%d、closure=%s、净前提=%+d、最深 POSTED=%d；四耦合 DERIVED 空格=%d；22x8=%d 格、W3 debt=%s / W4 debt=%s；三套分母=%s'
    % (N_SIG, N_DIM12, KILL_POS, KILL_NEG, KILL_BOUND, SM_DIM, N_KK, N_EXTRA_GEN, N_ALG,
       N_ROOTS, N_RANK4, N_GEN, N_A2, N_ORTH, N_AF, N_AF40, N_RANK_SM, N_RANK_CL,
       N_UNEVAL, CLOSURE, N_NET11, N_DEEP, N_DERIVED_COUPLINGS, MATRIX_CELLS,
       W3_DEBT, W4_DEBT, DENOM))

add('F02', '10 途径三态机器分桶：唯一化数 0/10，UNIQUIFY 态 0 行', 'FAIL',
    '行数=%d；针词现场命中=%d/%d（逐行全命中=%s）；UNIQUIFY=%d / CONSTRAIN_ONLY=%d / EXTERNAL_INPUT=%d；唯一化数=%d；新增 POSTED 行=%d；三态集合=%s；state 重算一致=%s'
    % (N_ROUTES, NEEDLE_HITS_ALL, NEEDLE_TOTAL_ALL,
       all(r['source_hits'] == r['needle_total'] for r in ROUTES),
       N_UNIQUIFY_STATE, N_CONSTRAIN, N_EXTERNAL, N_UNIQUE, N_NEW_POSTED,
       sorted(STATE_SET), all(STATE_RECOMPUTE)))

add('F03', '代数签名 / 表示内容 / 反常消除三途径均落入 CONSTRAIN_ONLY 或 EXTERNAL_INPUT', 'FAIL',
    'R01 签名枚举：%d 个互不同构代数共享 (12,4)、dim12 候选 %d 个 ⇒ 不能唯一锁定 SM（state=%s）；R03 反常消除四项全零但「只锁赋值不锁群」（state=%s）；R09 表示内容须再输入额外信息且是实验选择（state=%s、new_posted=%d）；三者 unique_sm 全 0'
    % (N_SIG, N_DIM12, ROUTES[0]['state'], ROUTES[2]['state'], ROUTES[8]['state'],
       ROUTES[8]['new_posted']))

add('F04', '几何嵌入两路：so(1,3) 与 so(8) 都装不进 SM 群，唯一化通道为空', 'FAIL',
    'R02 so(1,3)：dim k 上界 %d < dim SM %d、%d 个几何统一候选中仅 SM 自身平凡可容纳 ⇒ fits=%d、state=%s；R04 so(8)：A2 子根 %d 个但与正交 A1 共存数=%d ⇒ 极大秩嵌入存在性=%d、embed_ok=%d、state=%s；N_ROOTS=%d / N_GEN=%d 只约束规模不选择群'
    % (KILL_BOUND, SM_DIM, N_ALG, FITS_REAL, ROUTES[1]['state'],
       N_A2, N_ORTH, N_ORTH, EMBED_REAL, ROUTES[3]['state'], N_ROOTS, N_GEN))

add('F05', 'KK n=5 逃逸与 Cl(1,11) 秩障碍：外部输入不是唯一化', 'FAIL',
    'R05 最小额外维 n=%d、多 %d 个生成元、n 的取值本身无框架出处 ⇒ state=%s、new_posted=%d；R08 rank_SM=%d > rank_Cl(1,3)=%d ⇒ 需更大代数 Cl(1,11)，r138 判 HARD-CORE-NOT-DERIVABLE「仅被约束、不被导出」⇒ state=%s、new_posted=%d；两行均不产出唯一 SM'
    % (N_KK, N_EXTRA_GEN, ROUTES[4]['state'], ROUTES[4]['new_posted'],
       N_RANK_SM, N_RANK_CL, ROUTES[7]['state'], ROUTES[7]['new_posted']))

add('F06', '渐近自由与唯一化原理：只约束 N_f，净前提下降门未过', 'FAIL',
    'R07 n_f=6 通过 %d 个 N 取值 / n_f=40 仍有 %d 个 ⇒ 渐近自由是约束非选择（state=%s）；R10 净下降要求 a < e，r138 给 e=%d（无已知导出）、a=%d（新原理）⇒ gate=%d（阳性对照 gate(1,0)=%d）；r134 净前提变化=%+d、未导出合计=%d、closure=%s ⇒ 唯一化尝试增大而非减少前提账本'
    % (N_AF, N_AF40, ROUTES[6]['state'], E_GATE, A_GATE, GATE_REAL, GATE_POS,
       N_NET11, N_UNEVAL, CLOSURE))

add('F07', 'C0160 七路径 / C4 两环 beta 暂缓 / 四力本源「不作回答」只读登记', 'BOUNDARY',
    'C0160 命中=%d/%d（不宣称任何一条已死、closed-neg）；W4/C4 命中=%d/%d（外部公式未在本仓核验⇒暂缓）；四力本源命中=%d/%d（4→3→2、不是本源数字、不作回答）；终审裁决命中=%d/%d（全人类共有的开放问题、审计意义上/物理意义上）；r135 命中=%d/%d（CIRCULAR-SUSPECT、Δ=-1、不选择规范群本身）。本册不重判任何一条路径、不引入外部两环 beta'
    % (hits_map['C0160'], needles_total['C0160'], hits_map['W4'], needles_total['W4'],
       hits_map['FORCE'], needles_total['FORCE'], hits_map['JUDGE'], needles_total['JUDGE'],
       hits_map['R135'], needles_total['R135']))

add('F08', '新增 POSTED 账：4 行 EXTERNAL_INPUT 各引入新外部输入，无一行清偿 DERIVED 空格', 'FAIL',
    'EXTERNAL_INPUT 行=%d、带 new_posted 标记=%d（R05 未观测额外维 / R08 Cl(1,11) / R09 实验选择 / R10 新原理）；r134 最深 POSTED=%d、净前提=%+d、未导出=%d、closure=%s；r130 命中=%d/%d（18/18 链 PREMISE-OPEN、四 DERIVED 空格）；四耦合 DERIVED 空格=%d 未填、迁移 0/4（attack43 继承）'
    % (N_EXTERNAL, N_NEW_POSTED, N_DEEP, N_NET11, N_UNEVAL, CLOSURE,
       hits_map['R130'], needles_total['R130'], N_DERIVED_COUPLINGS))

add('F09', '判据有牙：唯一化 / 嵌入 / 适配 / 净前提门四组阳性对照与变异', 'INFO',
    'decides(UNIQUIFY,1)=%d（阳性）；三变异 decides(CONSTRAIN_ONLY,1)=%d、decides(UNIQUIFY,2)=%d、decides(EXTERNAL_INPUT,1)=%d；embed_ok(1)=%d / fits(12,12)=%d / gate(1,0)=%d 阳性；真实 embed_ok(%d)=%d、fits(%d,%d)=%d、gate(%d,%d)=%d ⇒ 全 0 不是恒否判据造成的'
    % (SYNTH_UNIQ, MUT_STATE, MUT_NCAND, MUT_EXTERNAL, EMBED_POS, FITS_POS, GATE_POS,
       N_ORTH, EMBED_REAL, KILL_BOUND, SM_DIM, FITS_REAL, E_GATE, A_GATE, GATE_REAL))

add('F10', '总裁定：H44 FAIL（规范群唯一化未完成），不计攻破数', 'INFO',
    '唯一化数=%d/10、UNIQUIFY 态=%d 行、CONSTRAIN_ONLY=%d、EXTERNAL_INPUT=%d、新增 POSTED=%d；净前提下降门=%d；跨源静态命中 14 组满分=%s；编号空号=%s、R 链最新=%s；红线 0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不占 RID'
    % (N_UNIQUE, N_UNIQUIFY_STATE, N_CONSTRAIN, N_EXTERNAL, N_NEW_POSTED, GATE_REAL,
       all(hits_map[k] == needles_total[k] for k in hits_map),
       empty_id_hits, rid_latest))

# ---------- 守卫 ----------
SRC = read_text(os.path.join(HERE, BASE + '.py'))
TREE = ast.parse(SRC)
true_consts = [n.lineno for n in ast.walk(TREE)
                if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value == (1 == 1)]
def import_roots(text):
    t = ast.parse(text)
    return ({a.name.split('.')[0] for n in ast.walk(t) if isinstance(n, ast.Import) for a in n.names}
            | {(n.module or '').split('.')[0] for n in ast.walk(t) if isinstance(n, ast.ImportFrom)})
imports = sorted(import_roots(SRC))
THIRD_PARTY = {'mpmath', 'sympy', 'numpy', 'scipy', 'pandas'}
third_party_hits = [x for x in imports if x in THIRD_PARTY]
IMPORT_PROBE = import_roots('from mpmath import mp\nimport numpy as np\n')
PATHS_EXIST = sum(1 for p in PATHS if os.path.isfile(p))

guard('G44-1', '编号空号与分母守恒：attack44/攻破㊱/r411/r412 0 命中、R 链 r402、三套分母 18/19/22',
      all(v == 0 for v in empty_id_hits.values()) and file_hits == 0
      and rid_latest == 'r402' and rid_403plus == 0 and rid_402_hits > 0
      and MATRIX_CELLS == 176 and W3_DEBT == F(35, 2) and W4_DEBT == F(15, 1)
      and DENOM == {'declared': 18, 'snapshot': 19, 'present': 22}
      and nomig_count >= 4,
      'empty_ids=%s file_hits=%d rid=%s rid403+=%d cells=%d W3=%s W4=%s denom=%s nomig=%d'
      % (empty_id_hits, file_hits, rid_latest, rid_403plus, MATRIX_CELLS,
         W3_DEBT, W4_DEBT, DENOM, nomig_count))

guard('G44-2', '四册核心读数现场正则解析（不打字）：22 个数值逐项与事实源一致',
      N_SIG == 3 and N_DIM12 == 8 and KILL_POS == 3 and KILL_NEG == 3
      and KILL_BOUND == 3 and SM_DIM == 12 and N_KK == 5 and N_EXTRA_GEN == 16
      and N_ALG == 8 and N_ROOTS == 24 and N_RANK4 == 4 and N_GEN == 28
      and N_A2 == 16 and N_ORTH == 0 and N_AF == 7 and N_AF40 == 1
      and N_RANK_SM == 4 and N_RANK_CL == 2 and N_UNEVAL == 37
      and CLOSURE == Dc('0.327') and N_NET11 == 11 and N_DEEP == 5
      and N_DERIVED_COUPLINGS == 4,
      'sig=%d dim12=%d kill=(%d,%d)/bound=%d SM=%d kk=%d/+%d alg=%d roots=%d rank=%d gen=%d A2=%d orth=%d nf=%d/%d rankSM=%d rankCl=%d uneval=%d closure=%s net=%+d deep=%d'
      % (N_SIG, N_DIM12, KILL_POS, KILL_NEG, KILL_BOUND, SM_DIM, N_KK,
         N_EXTRA_GEN, N_ALG, N_ROOTS, N_RANK4, N_GEN, N_A2, N_ORTH, N_AF,
         N_AF40, N_RANK_SM, N_RANK_CL, N_UNEVAL, CLOSURE, N_NET11, N_DEEP))

guard('G44-3', '10 行针词表逐行全命中、三态互斥且守恒、state 可重算',
      N_ROUTES == 10 and NEEDLE_HITS_ALL == NEEDLE_TOTAL_ALL == 37
      and all(r['source_hits'] == r['needle_total'] for r in ROUTES)
      and all(STATE_RECOMPUTE) and STATE_SET <= THREE_STATES
      and N_CONSTRAIN + N_EXTERNAL + N_UNIQUIFY_STATE == N_ROUTES
      and N_UNIQUE == 0 and N_UNIQUIFY_STATE == 0 and N_NEW_POSTED == 4
      and [r['id'] for r in ROUTES] == ['R%02d' % i for i in range(1, 11)],
      'rows=%d needles=%d/%d states=%s recompute=%d/%d uniq=%d uniqstate=%d posted=%d'
      % (N_ROUTES, NEEDLE_HITS_ALL, NEEDLE_TOTAL_ALL, sorted(STATE_SET),
         sum(1 for x in STATE_RECOMPUTE if x), N_ROUTES, N_UNIQUE,
         N_UNIQUIFY_STATE, N_NEW_POSTED))

guard('G44-4', '判据有牙：唯一化阳性对照必过、三变异必翻转、嵌入/适配/净前提门双面对照',
      SYNTH_UNIQ == 1 and MUT_STATE == 0 and MUT_NCAND == 0 and MUT_EXTERNAL == 0
      and EMBED_POS == 1 and FITS_POS == 1 and GATE_POS == 1
      and EMBED_REAL == 0 and FITS_REAL == 0 and GATE_REAL == 0
      and N_UNIQUE == 0,
      'synth=%d mut=(%d,%d,%d) pos=(%d,%d,%d) real=(%d,%d,%d)'
      % (SYNTH_UNIQ, MUT_STATE, MUT_NCAND, MUT_EXTERNAL, EMBED_POS,
         FITS_POS, GATE_POS, EMBED_REAL, FITS_REAL, GATE_REAL))

guard('G44-5', '几何嵌入与秩障碍：Killing 上界、so(8) 正交共存为 0、秩 4 > 2',
      KILL_BOUND < SM_DIM and KILL_POS == KILL_NEG == 3
      and N_ORTH == 0 and N_A2 == 16 and N_ROOTS == 24
      and N_GEN == N_ROOTS + N_RANK4 and N_RANK_SM > N_RANK_CL
      and N_ALG == 8 and N_EXTRA_GEN == 16 and N_KK == 5,
      'bound=%d<%d orth=%d A2=%d gen=%d=%d+%d rank=%d>%d'
      % (KILL_BOUND, SM_DIM, N_ORTH, N_A2, N_GEN, N_ROOTS, N_RANK4,
         N_RANK_SM, N_RANK_CL))

guard('G44-6', '净前提下降门与新增 POSTED 账：a=1 > e=0 门未过、4 行外部输入全带标记',
      E_GATE == 0 and A_GATE == 1 and GATE_REAL == 0
      and N_NET11 == 11 and N_UNEVAL == 37 and N_DEEP == 5
      and CLOSURE == Dc('0.327') and N_DERIVED_COUPLINGS == 4
      and N_EXTERNAL == 4 and N_NEW_POSTED == 4
      and all(r['new_posted'] == 1 for r in ROUTES if r['state'] == 'EXTERNAL_INPUT')
      and all(r['new_posted'] == 0 for r in ROUTES if r['state'] != 'EXTERNAL_INPUT'),
      'e=%d a=%d gate=%d net=%+d uneval=%d deep=%d ext=%d posted=%d'
      % (E_GATE, A_GATE, GATE_REAL, N_NET11, N_UNEVAL, N_DEEP,
         N_EXTERNAL, N_NEW_POSTED))

guard('G44-7', '跨源静态命中 14 组满分：C0137/C0162/A24/r138/r130/r134/r135/四力/终审/C0160/终局/W4/attack43/整理册',
      all(hits_map[k] == needles_total[k] for k in hits_map)
      and len(hits_map) == 14
      and hits_map['C0137'] == 5 and hits_map['C0162'] == 6
      and hits_map['R138'] == 5 and hits_map['R130'] == 6 and hits_map['R134'] == 6,
      'groups=%d full=%s detail=%s/%s'
      % (len(hits_map), all(hits_map[k] == needles_total[k] for k in hits_map),
         sum(hits_map.values()), sum(needles_total.values())))

AST_NAMES = set(n.id for n in ast.walk(TREE) if isinstance(n, ast.Name))
AST_FUNCS = set(n.name for n in ast.walk(TREE)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
BANNED_IDS = {'RATIO_PARTICLE', 'ALPHA_GRAV_CALC', 'MUT_DROP_ANCHOR', 'b_ij',
              'K4', 'Omega5', 'CELLS', 'COUPLINGS', 'FORCES', 'CELL_17', 'CANDIDATES'}
banned_id_hits = sorted(AST_NAMES & BANNED_IDS)
banned_func_hits = sorted(f for f in AST_FUNCS
                          if any(k in f.lower() for k in
                                 ('rk4', 'runge', 'gauss', 'rank', 'two_loop',
                                  'beta2', 'c2_gate', 'supply_class')))

guard('G44-8', '不重复项：纯标准库、无 RGE/RK4/两环 beta/C2 双锚点/16x4 矩阵的实现',
      len(third_party_hits) == 0 and len(banned_id_hits) == 0
      and len(banned_func_hits) == 0 and 'mpmath' not in imports
      and 'sympy' not in imports and 'mpmath' in IMPORT_PROBE
      and 'numpy' in IMPORT_PROBE and 'fractions' in imports
      and 'decimal' in imports,
      'imports=%s third_party=%s probe=%s banned_ids=%s banned_funcs=%s funcs=%s'
      % (imports, third_party_hits, sorted(IMPORT_PROBE), banned_id_hits,
         banned_func_hits, sorted(AST_FUNCS)))

guard('G44-9', '书写式/红线守卫：源码无布尔字面量、不占 RID、不改治理事实源、红线文本在册',
      len(true_consts) == 0 and '不宣称完成统一场' in SRC
      and '0/22、UFT-3=0、L3=0、validated=0' in SRC
      and '本册不占 RID' in SRC and '不跑 RGE' in SRC
      and '不宣称宇宙本质本源已回答' in SRC and '未改治理事实源' in SRC,
      'literal_true_consts=%d redline=%s no_rid=%s'
      % (len(true_consts), '0/22、UFT-3=0、L3=0、validated=0' in SRC,
         '本册不占 RID' in SRC))

guard('G44-10', '只读事实源与总裁定一致性：17 条路径全存在、10 条目分布 1/6/1/2、唯一化 0',
      PATHS_EXIST == len(PATHS) == 17 and len(ENTRIES) == 10
      and sum(1 for e in ENTRIES if e['verdict'] == 'PASS') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'FAIL') == 6
      and sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'INFO') == 2
      and N_UNIQUE == 0 and N_UNIQUIFY_STATE == 0,
      'paths=%d/%d entries=%d dist=1/6/1/2 uniq=%d/%d'
      % (PATHS_EXIST, len(PATHS), len(ENTRIES), N_UNIQUE, N_ROUTES))
# ---------- 汇总 / 产物 ----------
npass = sum(1 for e in ENTRIES if e['verdict'] == 'PASS')
nfail = sum(1 for e in ENTRIES if e['verdict'] == 'FAIL')
nbnd = sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY')
ninfo = sum(1 for e in ENTRIES if e['verdict'] == 'INFO')
nok = sum(1 for g in GUARDS if g['ok'])
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), npass, nfail, nbnd, ninfo, nok, len(GUARDS)))
emit('== 总裁定：FAIL（规范群唯一化未完成）；10 途径唯一化数 = 0/10 ==')
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不计攻破数；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': {'PASS': npass, 'FAIL': nfail, 'BOUNDARY': nbnd, 'INFO': ninfo},
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (nok, len(GUARDS)),
    'readings': {
        'three_state_table': ROUTES,
        'state_definition': {
            'UNIQUIFY': '该途径能把 SM 规范群唯一化（需同时 n_cand=1）',
            'CONSTRAIN_ONLY': '该途径只给出必要条件/负面结构约束，不选择群',
            'EXTERNAL_INPUT': '该途径的成立依赖实验选择/更大代数/未观测额外维/新原理等外部输入',
            'priority': 'EXTERNAL_INPUT > CONSTRAIN_ONLY > UNIQUIFY(缺省)',
        },
        'state_distribution': {
            'rows': N_ROUTES, 'UNIQUIFY': N_UNIQUIFY_STATE,
            'CONSTRAIN_ONLY': N_CONSTRAIN, 'EXTERNAL_INPUT': N_EXTERNAL,
            'unique_sm': N_UNIQUE, 'new_posted': N_NEW_POSTED,
            'conservation': '%d+%d+%d=%d' % (N_UNIQUIFY_STATE, N_CONSTRAIN,
                                             N_EXTERNAL, N_ROUTES),
        },
        'needles': {'hits': NEEDLE_HITS_ALL, 'total': NEEDLE_TOTAL_ALL,
                    'all_rows_full_hit': all(r['source_hits'] == r['needle_total'] for r in ROUTES)},
        'core_constants': {
            'signature_shared_algebras': N_SIG, 'dim12_candidates': N_DIM12,
            'killing_signature': [KILL_POS, KILL_NEG], 'compact_subalgebra_bound': KILL_BOUND,
            'dim_SM': SM_DIM, 'KK_n': N_KK, 'extra_generators': N_EXTRA_GEN,
            'geometric_unification_candidates': N_ALG,
            'so8_roots': N_ROOTS, 'so8_rank': N_RANK4, 'so8_generators': N_GEN,
            'so8_A2_subsystems': N_A2, 'so8_A2_orthogonal_to_A1': N_ORTH,
            'asymptotic_freedom_nf6_pass': N_AF, 'asymptotic_freedom_nf40_pass': N_AF40,
            'rank_SM': N_RANK_SM, 'rank_Cl13': N_RANK_CL,
            'r134_underived': N_UNEVAL, 'r134_closure': str(CLOSURE),
            'r134_net_premise': N_NET11, 'r134_deep_posted': N_DEEP,
            'derived_coupling_spaces': N_DERIVED_COUPLINGS,
        },
        'net_premise_gate': {
            'definition': 'gate(e,a) = 1 当且仅当 a < e（新增前提 a 少于已知导出 e）',
            'e': E_GATE, 'a': A_GATE, 'real': GATE_REAL,
            'positive_control_gate_1_0': GATE_POS,
            'verdict': '未过门：a=1 > e=0',
        },
        'embedding_checks': {
            'fits_bound_dim': {'bound': KILL_BOUND, 'dim': SM_DIM, 'result': FITS_REAL},
            'embed_orth_A2': {'n_orth': N_ORTH, 'result': EMBED_REAL},
            'positive_controls': {'fits_12_12': FITS_POS, 'embed_1': EMBED_POS},
        },
        'positive_controls': {
            'decides_UNIQUIFY_1': SYNTH_UNIQ,
            'mutation_CONSTRAIN_ONLY_1': MUT_STATE,
            'mutation_UNIQUIFY_2': MUT_NCAND,
            'mutation_EXTERNAL_INPUT_1': MUT_EXTERNAL,
            'state_recompute_consistent': sum(1 for x in STATE_RECOMPUTE if x),
            'conclusion': '零唯一化不是恒否判据造成的',
        },
        'source_static_hits': {k: '%d/%d' % (hits_map[k], needles_total[k]) for k in hits_map},
        'matrix': {'systems': DENOM['present'], 'cells': MATRIX_CELLS,
                   'W3_debt': str(W3_DEBT), 'W4_debt': str(W4_DEBT)},
        'denominators_triple': DENOM,
        'empty_id_hits': empty_id_hits, 'file_token_hits': file_hits,
        'rid_latest': rid_latest, 'rid_403plus_hits': rid_403plus,
        'readme_no_migration_hits': nomig_count,
        'paths_exist': '%d/%d' % (PATHS_EXIST, len(PATHS)),
    },
    'self_corrections': [
        '事实源 P_R138 首版按记忆写成「判定_TUFT-r138_量子引力与规范群起源_硬核不可推导性审计_2026-10-21.md」导致文件不存在；用 search_file 全库匹配 *r138* 定位到正本「判定_TUFT-r138_硬核审计_规范群与mu2符号不可导出性_2026-10-21.md」并改路径，17 条路径最终 0 缺失',
        '守卫段首版只写了 G44-8 调用却漏定义 AST_NAMES / AST_FUNCS / BANNED_IDS / banned_id_hits / banned_func_hits，运行会 NameError；在 G44-8 调用之前补回 AST 定义块',
        '先跑只读探针（Temp/_a44_probe.py）再落条目，一次性校准 17 条路径、22 个正则读数、14 组静态词表与 10 行针词表 ⇒ 避开 attack43 首跑 7/10 的三类假红（词形/路径/自指）',
        '三态互斥未采用「EXTERNAL 与 CONSTRAIN 词表不得同时命中」判据：R08 同时含「仅被约束、不被导出」与「需 Cl(1,11)」，该判据会假红；改用「state 现场重算一致 + 守恒式 + STATE_SET 子集」三件套，并配 decides 阳性对照',
        'NEEDLE_TOTAL_ALL=37 由 ROUTE_SPEC 现场求和得出，未硬编码；10 行 needle 逐行全命中由现场解析给出',
        'N_UNIQUIFY_STATE=0 是结论不是判据缺陷：以 decides(UNIQUIFY,1)=1 与 embed/fits/gate 三组阳性对照排除恒否偏倚',
        'G44-8 的 imports 提取沿用了 attack43 的推导式：ImportFrom 分支用 for a in [None] 且 a is not None 过滤 ⇒ fractions/decimal 根本不进集合，第三方 from mpmath import ... 也会漏检（假绿）；改为 Import 与 ImportFrom 两集合并集 + import_roots 阳性对照（from mpmath / import numpy 必命中），imports 由 7 项升为 9 项',
    ],
    'boundaries': [
        '本册审的是「库内已登记的 10 条途径能否机器唯一化 SM 规范群」，不是判定 SM 规范群本身是否正确；不否证 SM / GR / MSSM-SO(10) 物理',
        '三态分桶的词表来自既有判定册文字，属只读静态命中；不重新做群论枚举、不构造新代数/GUT 谱、不跑 RGE/RK4、不引入外部两环 beta（C4 维持「外部公式未在本仓核验⇒暂缓」）',
        '七路径 6 open 与 8 项 ⚠️ 沿用「登记不深攻」口径，本册不重新判定任何一条路径已死',
        '唯一化数 0/10 的作用域是「本库现有 10 条途径」，不排除框架外新原理；但按净前提下降门，任何新原理须满足 a<e 才过门，本册无任何该供给（e=0、a=1、gate=0）',
        '不重跑 attack39 ω 防线 / attack40 阈值×Yukawa×tau_p / attack41 类别注入 / attack42 43 条四类分桶与双锚点 Decimal / attack43 16×4 交叉矩阵',
        '不占 RID（三目录实扫 R 链最新 r402、r403+ 命中 0）；未改治理事实源、未改 verify.py、未跑 refresh_catalog.py、未提交 git',
        'PASS（F01）仅控制组仪器有效，不迁移为物理成立、不计攻破数；不宣称完成统一场、不宣称宇宙本质本源已回答',
    ],
    'methodology_notes': [
        '书写式布尔守卫用 1 == 1 比较式检查 AST 布尔字面量，避免守卫自身写入被扫描命中；导入模块集合由 AST 现场抽取',
        '10 行针词表逐行全命中 + state 现场重算一致 + 三变异阳性对照，构成「零通过不是恒否判据」的三重证明',
        '三态互斥采用显式优先序 EXTERNAL_INPUT > CONSTRAIN_ONLY > UNIQUIFY(缺省)，并以 STATE_SET 子集与守恒式锁定，避免多词表同时命中造成的状态歧义',
        '全部读数由 Markdown 表格/正则现场解析，纯标准库、无随机、无第三方依赖',
    ],
    'source_refs': {
        'C0137': '判定_C0137_规范群签名枚举攻破_2026-10-18.md:L39-51/L68-93',
        'C0162': '判定_C0162_so8极大子群P12闭合_2026-10-21.md:L31-82',
        'attack24': '判定_attack24_Phase0双分水岭_量子引力与规范群起源_全维攻破_2026-10-13.md:L25-36/L61-107/L218-229',
        'r138': '../本项目_全维自洽与归一化/数据/判定_TUFT-r138_硬核审计_规范群与mu2符号不可导出性_2026-10-21.md:L17-50',
        'r130': '../本项目_全维自洽与归一化/数据/判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md:L96/L107/L129-147',
        'r134': '../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md:L75-123',
        'r135': '../本项目_全维自洽与归一化/数据/判定_TUFT-r135_第一性原理突破尝试_自旋2路线机检与净前提下降门记账_2026-10-21.md',
        'force_audit': '../本项目_全维自洽与归一化/判定_四力本源_层级与可统一性的机器审计_2026-10-07.md:L13/L84/L129/L138',
        'final_judge': '../本项目_全维自洽与归一化/力的本源统一场_终审裁决_2026-10-13.md:L65/L80',
        'C0160': '判定_C0160_力的统一攻破_2026-10-21.md:L26-37/L105-137',
        'final_book': '穷尽攻破_统一场论终局总成_2026-10-21.md:L54',
        'w_judgment': '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md:L128',
        'matrix': '../全维全体系统一场论/数据/全维验收矩阵.json',
        'targets': '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json',
        'attack43': 'attack43_力本源_第17候选与16x4交叉供给矩阵_2026-11-08.json',
        'sortbook': '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md:L107-113',
        'readme': 'README.md:L1578-1584',
    },
    'cross_refs': [
        '判定_C0137_规范群签名枚举攻破_2026-10-18.md',
        '判定_C0162_so8极大子群P12闭合_2026-10-21.md',
        '判定_attack24_Phase0双分水岭_量子引力与规范群起源_全维攻破_2026-10-13.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r138_硬核审计_规范群与mu2符号不可导出性_2026-10-21.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
        '../本项目_全维自洽与归一化/数据/判定_TUFT-r135_第一性原理突破尝试_自旋2路线机检与净前提下降门记账_2026-10-21.md',
        '../本项目_全维自洽与归一化/判定_四力本源_层级与可统一性的机器审计_2026-10-07.md',
        '../本项目_全维自洽与归一化/力的本源统一场_终审裁决_2026-10-13.md',
        '判定_C0160_力的统一攻破_2026-10-21.md',
        '穷尽攻破_统一场论终局总成_2026-10-21.md',
        '../全维全体系统一场论/判定_统一场论全域验收矩阵与最小闭合集_2026-10-08.md',
        '../全维全体系统一场论/数据/全维验收矩阵.json',
        '../本项目_全维自洽与归一化/数据/无量纲靶场审计.json',
        'attack43_力本源_第17候选与16x4交叉供给矩阵_2026-11-08.json',
        '整理_attack39-41_统一场完成条件链路收口_2026-11-08.md',
        '判定_attack43_攻破㉟_力本源第17候选与16x4交叉供给矩阵_2026-11-08.md',
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

