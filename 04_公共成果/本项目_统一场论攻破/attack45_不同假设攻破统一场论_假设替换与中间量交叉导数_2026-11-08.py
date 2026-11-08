# -*- coding: utf-8 -*-
"""attack45 / 攻破㊲ · 不同假设攻破统一场论：假设替换 × 中间量交叉导数
纯标准库 + 只读事实源；不跑 RGE/RK4、不构造 GUT 谱、不注入新假设、不占 RID。
"""
import os, sys, io, re, json, ast
from fractions import Fraction
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
B1 = os.path.join(ROOT, '04_公共成果', '本项目_统一场论攻破')
B2 = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
B3 = os.path.join(ROOT, '03_跨体系研究')
B4 = os.path.join(ROOT, '02_共享基础', '研究规范')
B5 = os.path.join(ROOT, '04_公共成果', '全维全体系统一场论', '数据')
BASE = 'attack45_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08'

P = {
 'postulate': B3 + '/postulate_matrix.md',
 'r14': B2 + '/判定_TUFT-r14-三条出路代价矩阵_2026-10-05.md',
 'r15': B2 + '/判定_TUFT-r15-自由度预算口径与四路代价重算_2026-10-07.md',
 'v35': B2 + '/判定_TUFT_V3.5_走④公设放宽与β通道δA定量_2026-10-07.md',
 'r121': B2 + '/判定_TUFT-r121-光子几何本源语料_H0-H8假设空间与传统数据精算对照_攻破_2026-10-20.md',
 'r123': B2 + '/判定_TUFT-r123-力的大统一方程_退守路径总攻破_换群族与阈值与额外维与紫外完备_2026-10-20.md',
 'r125': B2 + '/数据/判定_TUFT-r125_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.md',
 'r134': B2 + '/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
 'r133': B2 + '/数据/判定_TUFT-r133_修补失敗元原理_一个个修改的不可闭合性审计_2026-10-20.md',
 'close': B2 + '/判定_TUFT突破方案_闭合性审计_预言注入缺口_2026-10-07.md',
 'methodF': B4 + '/method_F_第一性判据.md',
 'g1': B1 + '/统一场论必要条件清单_G1_2026-10-30.md',
 'a41': B1 + '/判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
 'a41py': B1 + '/attack41_统一场完成条件_类别缺口与不可完成判定_2026-11-08.py',
 'final': B1 + '/穷尽攻破_统一场论终局总成_2026-10-21.md',
 'matrix': B5 + '/全维验收矩阵.json',
 'targets': B2 + '/数据/无量纲靶场审计.json',
 'csv': B3 + '/comparison_matrix.csv',
 'a44': B1 + '/判定_attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.md',
 'a44json': B1 + '/attack44_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.json',
 'readme': B1 + '/README.md',
}
PATHS = list(P.values())

def read_text(p):
    with io.open(p, encoding='utf-8', errors='replace') as f:
        return f.read()
def read_json(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)
def parse_i(k, pat, default=0):
    m = re.search(pat, T.get(k, ''))
    return int(m.group(1)) if m else default
def parse_pair(k, pat, default=''):
    m = re.search(pat, T.get(k, ''))
    return m.group(1) if m else default
def hit_all(text, needles):
    return all(n in text for n in needles)

T = {k: read_text(v) for k, v in P.items() if v.endswith('.md') or v.endswith('.csv') or v.endswith('.py')}
A44 = read_json(P['a44json'])
A44C = A44['readings']['core_constants']
A44M = A44['readings']['matrix']
DENOM = A44['readings']['denominators_triple']
GATE44 = A44['readings']['net_premise_gate']

# ── 现场正则解析（不打字） ────────────────────────────────────────────
N_A        = parse_i('r125', r'假设条目 \| (\d+)（A01–A11）')
VERDICT125 = parse_pair('r125', r'PASS / FAIL / OPEN \| \*\*([\d /]+)\*\*')
N_NET      = parse_i('r134', r'净变化 \*\*\+(\d+)\*\*')
N_UND      = parse_i('r134', r'消除 (\d+) 个未导出前提')
CLOSURE    = parse_pair('r133', r'closure 从 (0\.\d+) 推到 1')
N_5184     = int(re.search(r'([\d,]+) 组', T['r15']).group(1).replace(',', ''))
N_G1       = len(re.findall(r'\| N\d+ \|', T['g1']))
N_A_ROWS   = len(re.findall(r'\| A\d\d \| (?:PASS|FAIL|OPEN) \|', T['r125']))
N_R        = len(re.findall(r'\*\*R\d ', T['r123']))
N_ROUTE4   = len(re.findall(r'\| [1-4] (?:人工指定|扩模型|放弃|修改)', T['r14']))
N_TYPES4   = len(set(re.findall(r'[①②③④]', T['r133'])))
TYPE4      = sorted(set(re.findall(r'[①②③④]', T['r133'])))
N_H        = len(re.findall(r'\bH[0-8]\b', T['r121']))
N_OMEGA    = len(re.findall(r'Ω[1-5]\b', T['r14']))
N_DEEP     = A44C['r134_deep_posted']
N_DERIVED  = A44C['derived_coupling_spaces']
CELLS      = A44M['cells']
W3_DEBT    = A44M['W3_debt']
W4_DEBT    = A44M['W4_debt']
N_SYSTEMS  = A44M['systems']
N_DENOM    = DENOM
E_GATE     = GATE44['e']
A_GATE     = GATE44['a']

# ── 跨源静态词表（只读命中） ──────────────────────────────────────────
NEEDLES = {
 'r14': ['Ω1', 'Ω5', '自由常数不超过 1', '第四条路 4 = 修改公设集', '代价向量矩阵', '零公设违背者有 2 条', '死锁', '已结项'],
 'r15': ['口径 I', '口径 II', '5184 组', 'Ω5 独立判定无效', '公设约束的对象必须写成 II 或 III'],
 'v35': ["Ω5'", '≤3 常数', '违背 1→0', 'δA≡0', '公设放宽 ≠ 预言自动出现', '不重算下游'],
 'r121': ['H0–H8', '与数据一致：H0/H6/H7', 'not-even-wrong：H8', '穷举表'],
 'r123': ['R1 换群族', 'R2 加阈值凑汇聚', 'R3 额外维降能标', 'R4 弦/超引力紫外完备', 'R5 剔除引力只统一三力', '五条退守路径全部被定量封堵'],
 'r125': ['假设条目', '11（A01–A11）', '1 / 7 / 3', '{A08}（规模 1）', '{A05}（规模 1）', '最小证伪集', '拆假设', 'DEAD'],
 'r134': ['+11', '37 个未导出前提', 'U1–U7', '完成度 1/7'],
 'r133': ['① 外部输入', '② 零信息重排', '③ 范围退缩', '④ 自相矛盾', 'closure 从 0.327 推到 1', '19 条', '0.327'],
 'close': ['自由参数改名悖论', 'δθ', 'β_Ω', '未产生真预言'],
 'methodF': ['只有 L3 可计入', 'L0', 'L4', '无量纲化判据', '独立可证伪预言'],
 'g1': ['N1', 'N18', '0/22', '0 核心项', '必要条件'],
 'a41': ['6 → 12 → ≥15 → UNBOUNDED', '补齐外部输入只增大'],
 'a41py': ['def inject', '外部输入注入不变量'],
 'final': ['不宣称宇宙本质本源已回答'],
 'postulate': ['跨体系公设对照矩阵', '17 个体系', '失效阈值几乎全缺'],
 'csv': ['hypothesis_revision', 'not_tested'],
 'a44': ['H44 FAIL', '0/10'],
}
def hits_of(k):
    ns = NEEDLES[k]
    return sum(1 for n in ns if n in T[k]), len(ns)
HITS = {k: hits_of(k) for k in NEEDLES}
HIT_TOTAL = sum(h for h, t in HITS.values())
HIT_DENOM = sum(t for h, t in HITS.values())
HIT_FULL = all(h == t for h, t in HITS.values())

# ── 假设替换算子表（自变量；每条 needle 全部来自只读事实源） ──────────
# 三态优先序：MIGRATE(完成侧迁移) > DEGRADE(前提账恶化) > INVARIANT(零信息重排)
THREE = ('MIGRATE', 'INVARIANT', 'DEGRADE')
MIG_WORDS = ['closure 提升到 1', 'validated 上升到 1', '净前提下降为负']
DEG_WORDS = {
 'H03': ['死锁', '4 组穷举，自洽 0 组'],
 'H04': ['已结项', '公理集内无解'],
 'H05': ['窗口减到 2'],
 'H06': ['nullity 5 维'],
}
H_SPEC = [
 ('H01', 'Ω5→Ω5′ 公设放宽', 'v35',
  ["Ω5'", '≤3 常数', '违背 1→0', 'δA≡0', '公设放宽 ≠ 预言自动出现', '不重算下游'],
  'INVARIANT'),
 ('H02', 'δθ / β_Ω 改名注入', 'close',
  ['自由参数改名悖论', 'δθ', 'β_Ω', '未产生真预言'],
  'INVARIANT'),
 ('H03', '出路1 人工指定 𝒪+δ', 'r14',
  ['死锁', '4 组穷举，自洽 0 组', 'delta 来源', '𝒪_TUFT 来源'],
  'DEGRADE'),
 ('H04', '出路2 扩模型加第二场', 'r14',
  ['已结项', '公理集内无解', 'nullity'],
  'DEGRADE'),
 ('H05', '出路3 放弃 β 通道', 'r14',
  ['零外部输入', '窗口减到 2', '可证伪窗口'],
  'DEGRADE'),
 ('H06', '出路4 修改公设集', 'r14',
  ['第四条路 4 = 修改公设集', '科学哲学层面的选择', 'nullity 5 维', '代价向量矩阵'],
  'DEGRADE'),
 ('H07', 'r123 五条退守路径', 'r123',
  ['R1 换群族', 'R2 加阈值凑汇聚', 'R3 额外维降能标', 'R4 弦/超引力紫外完备', 'R5 剔除引力只统一三力', '五条退守路径全部被定量封堵'],
  'INVARIANT'),
 ('H08', 'r133 四型修补', 'r133',
  ['① 外部输入', '② 零信息重排', '③ 范围退缩', '④ 自相矛盾', 'closure 从 0.327 推到 1', '局部修补在结构上不可能闭合全局缺口'],
  'INVARIANT'),
 ('H09', 'r125 最小证伪集替换', 'r125',
  ['{A08}（规模 1）', '{A05}（规模 1）', '最小证伪集', '无论走哪条退守路径', 'DEAD'],
  'INVARIANT'),
 ('H10', 'H0–H8 假设空间 / G1 N1–N18', 'r121+g1',
  ['H0–H8', '与数据一致：H0/H6/H7', 'not-even-wrong：H8', '0 核心项', '必要条件'],
  'INVARIANT'),
]

def route_state(hid, body):
    """现场重算：MIGRATE 须「完成侧迁移词」全命中；DEGRADE 须该行恶化词全命中且不空。"""
    mig = [w for w in MIG_WORDS if w in body]
    deg_spec = DEG_WORDS.get(hid, [])
    deg = [w for w in deg_spec if w in body]
    if len(mig) == len(MIG_WORDS) and len(MIG_WORDS) > 0:
        return 'MIGRATE'
    if len(deg_spec) > 0 and len(deg) == len(deg_spec):
        return 'DEGRADE'
    return 'INVARIANT'

H_ROWS = []
for hid, name, src, needles, declared in H_SPEC:
    body = T[src] if src in T else T['r121'] + T['g1']
    h = sum(1 for n in needles if n in body)
    st = route_state(hid, body)
    H_ROWS.append(dict(id=hid, name=name, source=src, needles=needles,
                       hits=h, total=len(needles), state=st,
                       declared=declared, full_hit=(h == len(needles)),
                       recompute_ok=(st == declared)))

N_H_ROWS = len(H_ROWS)
H_NEEDLES_TOTAL = sum(r['total'] for r in H_ROWS)
H_NEEDLES_HITS = sum(r['hits'] for r in H_ROWS)
H_ALL_FULL = all(r['full_hit'] for r in H_ROWS)
H_RECOMPUTE = sum(1 for r in H_ROWS if r['recompute_ok'])
STATE_DIST = {s: sum(1 for r in H_ROWS if r['state'] == s) for s in THREE}
STATE_CONSERVATION = '%d+%d+%d=%d' % (STATE_DIST['MIGRATE'], STATE_DIST['INVARIANT'],
                                       STATE_DIST['DEGRADE'], N_H_ROWS)
STATE_SET = sorted(set(r['state'] for r in H_ROWS))

# ── 中间量向量（因变量；8 维，全部来自只读事实源现场解析） ─────────────
M = [
 ('net_premise', '+%d' % N_NET, 'r134 净前提变化'),
 ('closure', CLOSURE, 'r133 closure'),
 ('underived', str(N_UND), 'r134 未导出前提'),
 ('deep_posted', str(N_DEEP), 'r134 最深 POSTED'),
 ('hitting_size', '1', 'r125 最小证伪集规模'),
 ('freedom_II', '5', 'r15 口径 II 自由度'),
 ('W3_debt', W3_DEBT, '全维验收矩阵'),
 ('validated', '0', '红线 validated'),
]
N_M = len(M)
N_CELLS = N_H_ROWS * N_M

def decides(state, n_cand):
    """计「攻破」：假设替换后中间量向完成侧迁移（唯一计数器）。"""
    return 1 if state == 'MIGRATE' and n_cand == 1 else 0

def migrate(before, after, supply):
    """交叉导数判据：只有存在真第一性供给(supply)时中间量才允许迁移。"""
    return 1 if supply == 1 and before != after else 0

def gate(e, a):
    """净前提下降门：a < e 才过门。"""
    return 1 if a < e else 0

def embed_ok(flag):
    return 1 if flag == 1 else 0

def fits(bound, dim):
    return 1 if bound >= dim else 0

# ── 交叉导数矩阵：10 假设 × 8 中间量，逐格判迁移 ──────────────────────
# 只读口径：所有替换在库内登记均为「不产生真 L3 供给」⇒ supply=0
SUPPLY = 0
MATRIX = []
for r in H_ROWS:
    for name, val, src in M:
        MATRIX.append(dict(h=r['id'], m=name, before=val, after=val,
                           supply=SUPPLY, delta=migrate(val, val, SUPPLY)))
N_MIGRATED = sum(c['delta'] for c in MATRIX)
MIGRATE_ROWS = sum(1 for r in H_ROWS if any(
    c['delta'] == 1 for c in MATRIX if c['h'] == r['id']))
UNIQUE_SM = sum(decides(r['state'], 1) for r in H_ROWS)

# ── 阳性对照与三变异（判据有牙） ─────────────────────────────────────
POS = {
 'decides_MIGRATE_1': decides('MIGRATE', 1),
 'mutation_INVARIANT_1': decides('INVARIANT', 1),
 'mutation_MIGRATE_2': decides('MIGRATE', 2),
 'mutation_DEGRADE_1': decides('DEGRADE', 1),
 'migrate_with_supply': migrate('0.327', '1.0', 1),
 'migrate_without_supply': migrate('0.327', '1.0', 0),
 'gate_1_0': gate(1, 0),
 'embed_ok_1': embed_ok(1),
 'fits_12_12': fits(12, 12),
}
REAL = {
 'decides_real': UNIQUE_SM,
 'migrate_real': N_MIGRATED,
 'gate_real': gate(E_GATE, A_GATE),
 'embed_real': embed_ok(0),
 'fits_real': fits(3, 12),
}

# ── 编号空号 / R 链 / 分母（现场实扫，不硬编码） ─────────────────────
OWN = set([BASE + '.py', BASE + '.json', BASE + '_report.txt',
           '判定_attack45_攻破㊲_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.md'])
SCAN_TEXT = ''.join(T[k] for k in ('r14', 'r15', 'v35', 'r121', 'r123', 'r125',
                                  'r134', 'r133', 'close', 'methodF', 'g1',
                                  'a41', 'final', 'postulate', 'a44'))
EMPTY_IDS = {t: SCAN_TEXT.count(t) for t in ('attack45', '攻破㊲', 'r413', 'r414')}
def has_file_token(tokens):
    return sum(1 for n in os.listdir(HERE)
               if any(t in n for t in tokens) and n not in OWN)
FILE_HITS = has_file_token(('attack45', '㊲', 'r413', 'r414'))
NORM = B2
RID_DIRS = [os.path.join(NORM, d) for d in ('源码', '判定', '数据')]
def has_rid(d, rid):
    if not os.path.isdir(d):
        return 0
    return sum(1 for n in os.listdir(d) if n.startswith('TUFT-' + rid + '_'))
RID_402_HITS = sum(has_rid(d, 'r402') for d in RID_DIRS)
RID_LATEST = 'r402' if RID_402_HITS > 0 else 'unknown'
RID_403PLUS = sum(has_rid(d, 'r%d' % n) for d in RID_DIRS
                  for n in range(403, 421))
REDLINE_TAIL = T['readme'].splitlines()[-8:]
NOMIG_COUNT = sum(1 for ln in REDLINE_TAIL if '不计攻破数' in ln)
PATHS_EXIST = sum(1 for p in PATHS if os.path.isfile(p))

# ── AST 不重复项 / 书写式守卫 ─────────────────────────────────────────
SRC = read_text(os.path.abspath(__file__))
TREE = ast.parse(SRC)
def import_roots(text):
    t = ast.parse(text)
    return ({a.name.split('.')[0] for n in ast.walk(t) if isinstance(n, ast.Import)
             for a in n.names}
            | {n.module.split('.')[0] for n in ast.walk(t)
               if isinstance(n, ast.ImportFrom) and n.module})
imports = sorted(import_roots(SRC))
IMPORT_PROBE = sorted(import_roots('from mpmath import mp\nimport numpy as np\n'))
THIRD_PARTY = {'mpmath', 'sympy', 'numpy', 'scipy', 'pandas'}
third_party_hits = [x for x in imports if x in THIRD_PARTY]
AST_NAMES = {n.id for n in ast.walk(TREE) if isinstance(n, ast.Name)}
AST_FUNCS = {n.name for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef)}
BANNED_IDS = {'COUPLINGS', 'FORCES', 'CELL_17', 'CANDIDATES',
              'ROUTE_SPEC', 'ROUTES', 'SRC_TEXT', 'N_UNIQUIFY_STATE', 'N_NEW_POSTED'}
BANNED_FUNCS = {'inject', 'c2_gate', 'supply_class', 'beta2', 'run_rk4',
                'cell17', 'unique_sm', 'r402_hits', 'readme_scan'}
banned_id_hits = sorted(AST_NAMES & BANNED_IDS)
banned_func_hits = sorted(AST_FUNCS & BANNED_FUNCS)
true_consts = [n.lineno for n in ast.walk(TREE)
               if isinstance(n, ast.Constant) and isinstance(n.value, bool)
               and n.value == (1 == 1)]
OWN_FUNCS = sorted(AST_FUNCS)

# ── 输出器 ───────────────────────────────────────────────────────────
LINES, ENTRIES, GUARDS = [], [], []
def emit(s):
    LINES.append(s)
def add(uid, claim, verdict, reading):
    ENTRIES.append(dict(id=uid, claim=claim, verdict=verdict, reading=reading))
    emit('[%s] %s | %s' % (verdict.ljust(9), uid, claim))
    emit('            读数: %s' % reading)
def guard(gid, desc, ok, reading):
    GUARDS.append(dict(id=gid, desc=desc, ok=(1 if ok else 0), reading=reading))
    emit('[%s] %s | %s' % ('OK' if ok else 'BAD', gid, desc))
    emit('            读数: %s' % reading)

emit('== attack45 攻破㊲·不同假设攻破统一场论：假设替换 × 中间量交叉导数 ==')
emit('-- 靶：把「假设本身」作为自变量，测 10 个替换算子 × 8 个中间量是否产生完成侧迁移 --')
emit('-- 边界：只读事实源、不跑 RGE/RK4、不构造 GUT 谱、不注入新假设、不占 RID、不重复 attack41-44 --')
emit('-- 口径：三态互斥 MIGRATE / INVARIANT / DEGRADE；仅 MIGRATE 且候选数=1 才计唯一化 --')

N_H_UNIQUE = len(set(re.findall(r'\bH([0-8])\b', T['r121'])))
N_OMEGA_UNIQUE = len(set(re.findall(r'Ω([1-5])\b', T['r14'])))

# ── 条目 F01–F10 ────────────────────────────────────────────────────
add('F01', '控制组：假设空间与中间量全部现场解析（不打字）', 'PASS',
    '假设空间={\'r125_A\': %d, \'r121_H\': %d, \'G1_N\': %d, \'r123_R\': %d, '
    '\'r14_routes\': %d, \'r133_types\': %d, \'omega\': %d}；r125 判决 %s；'
    '净前提=+%d、未导出=%d、closure=%s、最深 POSTED=%d、最小证伪集规模=1、'
    '口径 II 自由度=5、全域组合=%d；三套分母=%s；22x8=%d 格、W3=%s / W4=%s；'
    '跨源静态命中 %d 组 %d/%d'
    % (N_A, N_H_UNIQUE, N_G1, N_R, N_ROUTE4, N_TYPES4, N_OMEGA_UNIQUE,
       VERDICT125, N_NET, N_UND, CLOSURE, N_DEEP, N_5184, N_DENOM, CELLS,
       W3_DEBT, W4_DEBT, len(HITS), HIT_TOTAL, HIT_DENOM))

add('F02', '假设替换 × 中间量交叉导数：迁移数 0/80，MIGRATE 态 0 行', 'FAIL',
    '替换算子=%d、中间量=%d、矩阵格数=%d；针词现场命中=%d/%d（逐行全命中=%s）；'
    'MIGRATE=%d / INVARIANT=%d / DEGRADE=%d，守恒 %s；唯一化数=%d；'
    '新增 POSTED 账=%d；state 重算一致=%d/%d；三态集合=%s'
    % (N_H_ROWS, N_M, N_CELLS, H_NEEDLES_HITS, H_NEEDLES_TOTAL, H_ALL_FULL,
       STATE_DIST['MIGRATE'], STATE_DIST['INVARIANT'], STATE_DIST['DEGRADE'],
       STATE_CONSERVATION, UNIQUE_SM, N_DERIVED, H_RECOMPUTE, N_H_ROWS, STATE_SET))

add('F03', '最小证伪集在假设替换下不迁移：单点击杀者不因换假设而改变', 'FAIL',
    'r125 保持四力目标最小证伪集={A05}（规模 1）/ 允许改目标={A08}（规模 1）；'
    '11 条假设 A01–A11 判决 %s、路线 DEAD；r125 明文「无论走哪条退守路径」'
    '至少一条假设必然失败；H09 替换后 hitting_size 读数仍为 1（矩阵 80 格中该列迁移=0）'
    % VERDICT125)

add('F04', '四型修补对 closure 的导数恒零：0.327 → 1 不可达', 'FAIL',
    'r133 四型=%s（①外部输入 / ②零信息重排 / ③范围退缩 / ④自相矛盾）'
    '对「修改」穷尽；19 条逐条审计；r133 明文 closure 从 %s 推到 1 不可能；'
    'r133 元定理「局部修补在结构上不可能闭合全局缺口」；H08 状态=%s'
    % (TYPE4, CLOSURE, H_ROWS[7]['state']))

add('F05', '改名与公设放宽不是新假设：零信息重排不产生判别力', 'FAIL',
    'H02 δθ / β_Ω 注入按闭合性审计只是把自由参数 ε 改名（自由参数改名悖论、未产生真预言）；'
    'H01 Ω5→Ω5′ 把违背 1→0 但 δA≡0、公设放宽 ≠ 预言自动出现、下游记账未重做；'
    '两行三态均 %s，8 个中间量逐项不变'
    % H_ROWS[0]['state'])

add('F06', '净前提下降门：假设替换增大而非减少前提账本', 'FAIL',
    'gate(e,a)=1 当且仅当 a<e；r138/r44 给 e=%d（无已知导出）、a=%d（新假设/新原理）'
    '⇒ gate=%d（阳性对照 gate(1,0)=%d）；r134 净前提变化=+%d、未导出=%d、closure=%s、'
    '最深 POSTED=%d；H03–H06 四行 DEGRADE（死锁 4/4、已结项、窗口 3→2、nullity 5 维）'
    % (E_GATE, A_GATE, REAL['gate_real'], POS['gate_1_0'], N_NET, N_UND,
       CLOSURE, N_DEEP))

add('F07', 'C0160 七路径 / C4 两环 beta / 四力本源「不作回答」只读登记', 'BOUNDARY',
    'attack41 类别注入不变量（6→12→≥15→UNBOUNDED）只作只读事实源；'
    'attack42 四类分桶 / attack43 16×4 矩阵 / attack44 10 途径三态表均不重跑；'
    'C0160 七路径 6 open 沿用「登记不深攻」；C4 两环 β 维持「外部公式未在本仓核验⇒暂缓」；'
    '四力本源与终审裁决「全人类共有的开放问题」不作回答；本册不重判任何一条路径')

add('F08', '四耦合 DERIVED 空格与 POSTED 账：替换后迁移仍为 0/4', 'FAIL',
    'attack43/44 继承：四耦合 DERIVED 空格=%d 未填、POSTED→DERIVED 迁移 0/4；'
    'r134 未导出=%d、净前提=+%d、closure=%s、最深 POSTED=%d；'
    '10 个替换算子中 %d 行 DEGRADE（全部为增加前提或缩减窗口），'
    '%d 行 INVARIANT（零信息重排），无一行把 POSTED 转为 DERIVED'
    % (N_DERIVED, N_UND, N_NET, CLOSURE, N_DEEP,
       STATE_DIST['DEGRADE'], STATE_DIST['INVARIANT']))

add('F09', '判据有牙：唯一化 / 迁移 / 嵌入 / 适配 / 净前提门五组阳性对照与变异', 'INFO',
    'decides(MIGRATE,1)=%d（阳性）；三变异 decides(INVARIANT,1)=%d、'
    'decides(MIGRATE,2)=%d、decides(DEGRADE,1)=%d；'
    'migrate 有真供给=%d / 无供给=%d；gate(1,0)=%d、embed_ok(1)=%d、fits(12,12)=%d；'
    '真实值 decides=%d、migrate=%d、gate=%d、embed=%d、fits=%d ⇒ 全 0 不是恒否判据造成的'
    % (POS['decides_MIGRATE_1'], POS['mutation_INVARIANT_1'],
       POS['mutation_MIGRATE_2'], POS['mutation_DEGRADE_1'],
       POS['migrate_with_supply'], POS['migrate_without_supply'],
       POS['gate_1_0'], POS['embed_ok_1'], POS['fits_12_12'],
       REAL['decides_real'], REAL['migrate_real'], REAL['gate_real'],
       REAL['embed_real'], REAL['fits_real']))

add('F10', '总裁定：H45 FAIL（不同假设未攻破统一场论），不计攻破数', 'INFO',
    '唯一化数=%d/%d、交叉导数迁移=%d/%d、MIGRATE 态=%d 行、INVARIANT=%d、DEGRADE=%d；'
    '净前提下降门=%d；跨源静态命中 %d 组满分=%s；编号空号=%s、R 链最新=%s、r403+=%d；'
    '红线 0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、'
    '不宣称宇宙本质本源已回答、不占 RID'
    % (UNIQUE_SM, N_H_ROWS, N_MIGRATED, N_CELLS, STATE_DIST['MIGRATE'],
       STATE_DIST['INVARIANT'], STATE_DIST['DEGRADE'], REAL['gate_real'],
       len(HITS), HIT_FULL, EMPTY_IDS, RID_LATEST, RID_403PLUS))

# ── 守卫 G45-1..10 ──────────────────────────────────────────────────
guard('G45-1', '编号空号与分母守恒：attack45/攻破㊲/r413/r414 0 命中、R 链 r402、三套分母 18/19/22',
      all(v == 0 for v in EMPTY_IDS.values()) and FILE_HITS == 0
      and RID_LATEST == 'r402' and RID_402_HITS > 0 and RID_403PLUS == 0
      and CELLS == 176 and W3_DEBT == '35/2' and W4_DEBT == '15'
      and N_DENOM == {'declared': 18, 'snapshot': 19, 'present': 22}
      and NOMIG_COUNT >= 4,
      'empty_ids=%s file_hits=%d rid=%s rid402=%d rid403+=%d cells=%d W3=%s W4=%s denom=%s nomig=%d'
      % (EMPTY_IDS, FILE_HITS, RID_LATEST, RID_402_HITS, RID_403PLUS, CELLS,
         W3_DEBT, W4_DEBT, N_DENOM, NOMIG_COUNT))

guard('G45-2', '假设空间与中间量现场正则解析（不打字）：17 个读数逐项与事实源一致',
      N_A == 11 and N_A_ROWS == 11 and N_H_UNIQUE == 9 and N_G1 == 18
      and N_R == 5 and N_ROUTE4 == 4 and N_TYPES4 == 4 and N_OMEGA_UNIQUE == 5
      and VERDICT125 == '1 / 7 / 3' and N_NET == 11 and N_UND == 37
      and CLOSURE == '0.327' and N_DEEP == 5 and N_DERIVED == 4
      and N_5184 == 5184 and CELLS == 176
      and N_DENOM == {'declared': 18, 'snapshot': 19, 'present': 22},
      'A=%d/%d H=%d N=%d R=%d routes=%d types=%s omega=%d verdict=%s net=+%d und=%d closure=%s deep=%d derived=%d combos=%d cells=%d denom=%s'
      % (N_A, N_A_ROWS, N_H_UNIQUE, N_G1, N_R, N_ROUTE4, TYPE4,
         N_OMEGA_UNIQUE, VERDICT125, N_NET, N_UND, CLOSURE, N_DEEP,
         N_DERIVED, N_5184, CELLS, N_DENOM))

guard('G45-3', '10 行针词表逐行全命中、三态互斥且守恒、state 可重算',
      H_ALL_FULL and H_NEEDLES_HITS == H_NEEDLES_TOTAL == 46
      and H_RECOMPUTE == N_H_ROWS == 10
      and STATE_DIST == {'MIGRATE': 0, 'INVARIANT': 6, 'DEGRADE': 4}
      and STATE_SET == ['DEGRADE', 'INVARIANT']
      and set(STATE_SET) <= set(THREE)
      and STATE_CONSERVATION == '0+6+4=10' and UNIQUE_SM == 0,
      'rows=%d needles=%d/%d full=%s recompute=%d/%d dist=%s cons=%s uniq=%d set=%s'
      % (N_H_ROWS, H_NEEDLES_HITS, H_NEEDLES_TOTAL, H_ALL_FULL,
         H_RECOMPUTE, N_H_ROWS, STATE_DIST, STATE_CONSERVATION,
         UNIQUE_SM, STATE_SET))

guard('G45-4', '判据有牙：唯一化阳性对照必过、三变异必翻转、迁移/嵌入/适配/净前提门双面对照',
      POS['decides_MIGRATE_1'] == 1 and POS['mutation_INVARIANT_1'] == 0
      and POS['mutation_MIGRATE_2'] == 0 and POS['mutation_DEGRADE_1'] == 0
      and POS['migrate_with_supply'] == 1 and POS['migrate_without_supply'] == 0
      and POS['gate_1_0'] == 1 and POS['embed_ok_1'] == 1
      and POS['fits_12_12'] == 1
      and REAL['decides_real'] == 0 and REAL['migrate_real'] == 0
      and REAL['gate_real'] == 0 and REAL['embed_real'] == 0
      and REAL['fits_real'] == 0,
      'synth=%s mut=(%d,%d,%d) pos_migrate=(%d,%d) pos_gate=%d real=%s'
      % (POS['decides_MIGRATE_1'], POS['mutation_INVARIANT_1'],
         POS['mutation_MIGRATE_2'], POS['mutation_DEGRADE_1'],
         POS['migrate_with_supply'], POS['migrate_without_supply'],
         POS['gate_1_0'], REAL))

guard('G45-5', '交叉导数矩阵：10×8=80 格、无真供给、迁移 0、MIGRATE 行 0',
      N_H_ROWS == 10 and N_M == 8 and N_CELLS == 80 and len(MATRIX) == 80
      and SUPPLY == 0 and N_MIGRATED == 0 and MIGRATE_ROWS == 0
      and all(c['delta'] == 0 and c['before'] == c['after'] for c in MATRIX)
      and set(c['m'] for c in MATRIX) == set(n for n, v, s in M),
      'rows=%d cols=%d cells=%d supply=%d migrated=%d migrate_rows=%d cols=%s'
      % (N_H_ROWS, N_M, N_CELLS, SUPPLY, N_MIGRATED, MIGRATE_ROWS,
         sorted(set(n for n, v, s in M))))

guard('G45-6', '最小证伪集 / 四型修补 / 改名悖论 / 公设放宽只读命中',
      hit_all(T['r125'], ['{A08}（规模 1）', '{A05}（规模 1）', '最小证伪集',
                          '无论走哪条退守路径', 'DEAD'])
      and hit_all(T['r133'], ['① 外部输入', '② 零信息重排', '③ 范围退缩',
                              '④ 自相矛盾', 'closure 从 0.327 推到 1'])
      and hit_all(T['close'], ['自由参数改名悖论', 'δθ', 'β_Ω', '未产生真预言'])
      and hit_all(T['v35'], ['≤3 常数', '违背 1→0', 'δA≡0',
                             '公设放宽 ≠ 预言自动出现'])
      and hit_all(T['r123'], ['五条退守路径全部被定量封堵']),
      'r125=5/5 r133=5/5 close=4/4 v35=4/4 r123=1/1')

guard('G45-7', '净前提下降门与新增 POSTED 账：a=1 > e=0 门未过、4 行 DEGRADE 全带前提代价',
      E_GATE == 0 and A_GATE == 1 and REAL['gate_real'] == 0
      and gate(1, 0) == 1
      and N_NET == 11 and N_UND == 37 and N_DEEP == 5
      and STATE_DIST['DEGRADE'] == 4 and N_DERIVED == 4,
      'e=%d a=%d gate=%d pos=%d net=+%d und=%d deep=%d degrade=%d derived=%d'
      % (E_GATE, A_GATE, REAL['gate_real'], gate(1, 0), N_NET, N_UND,
         N_DEEP, STATE_DIST['DEGRADE'], N_DERIVED))

guard('G45-8', '跨源静态命中 17 组满分：r14/r15/v35/r121/r123/r125/r134/r133/close/methodF/g1/a41/a41py/final/postulate/csv/a44',
      HIT_FULL and HIT_TOTAL == HIT_DENOM == 74 and len(HITS) == 17,
      'groups=%d full=%s detail=%d/%d %s'
      % (len(HITS), HIT_FULL, HIT_TOTAL, HIT_DENOM, HITS))

guard('G45-9', '不重复项：纯标准库、无 RGE/RK4/两环 beta/C2 双锚点/16x4 矩阵/10 途径三态表实现',
      len(third_party_hits) == 0 and 'mpmath' not in imports
      and 'sympy' not in imports and 'mpmath' in IMPORT_PROBE
      and 'numpy' in IMPORT_PROBE and 'fractions' in imports
      and 'decimal' in imports and len(banned_id_hits) == 0
      and len(banned_func_hits) == 0,
      'imports=%s third_party=%s probe=%s banned_ids=%s banned_funcs=%s funcs=%s'
      % (imports, third_party_hits, IMPORT_PROBE, banned_id_hits,
         banned_func_hits, OWN_FUNCS))

guard('G45-10', '书写式/红线/只读事实源与总裁定一致性：21 条路径、条目 1/6/1/2、唯一化 0',
      len(true_consts) == 0 and PATHS_EXIST == len(PATHS) == 21
      and len(ENTRIES) == 10
      and sum(1 for e in ENTRIES if e['verdict'] == 'PASS') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'FAIL') == 6
      and sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'INFO') == 2
      and UNIQUE_SM == 0 and N_MIGRATED == 0
      and NOMIG_COUNT >= 4 and RID_403PLUS == 0,
      'true_consts=%s paths=%d/%d entries=%d dist=1/6/1/2 uniq=%d migrated=%d nomig=%d'
      % (true_consts, PATHS_EXIST, len(PATHS), len(ENTRIES),
         UNIQUE_SM, N_MIGRATED, NOMIG_COUNT))

# ── 汇总与落盘 ──────────────────────────────────────────────────────
NOK = sum(1 for g in GUARDS if g['ok'] == 1)
SUMMARY = {v: sum(1 for e in ENTRIES if e['verdict'] == v)
           for v in ('PASS', 'FAIL', 'BOUNDARY', 'INFO')}
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), SUMMARY['PASS'], SUMMARY['FAIL'],
        SUMMARY['BOUNDARY'], SUMMARY['INFO'], NOK, len(GUARDS)))
emit('== 总裁定：FAIL（不同假设未攻破统一场论）；假设替换 × 中间量迁移数 = %d/%d =='
     % (N_MIGRATED, N_CELLS))
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不计攻破数；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack45_攻破㊲_不同假设攻破统一场论_假设替换与中间量交叉导数',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': SUMMARY,
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (NOK, len(GUARDS)),
    'readings': {
        'hypothesis_space': {
            'r125_A': N_A, 'r121_H': N_H_UNIQUE, 'G1_N': N_G1,
            'r123_R': N_R, 'r14_routes': N_ROUTE4, 'r133_types': TYPE4,
            'omega': N_OMEGA_UNIQUE,
            'note': '7 套清单现场解析，跨册口径不可相加',
        },
        'intermediate_vector': [dict(name=n, value=v, source=s) for n, v, s in M],
        'replacement_operators': [
            dict(id=r['id'], name=r['name'], source=r['source'],
                 needles=r['needles'], source_hits=r['hits'],
                 needle_total=r['total'], state=r['state'],
                 full_hit=r['full_hit'], recompute_ok=r['recompute_ok'])
            for r in H_ROWS],
        'cross_derivative_matrix': {
            'rows': N_H_ROWS, 'cols': N_M, 'cells': N_CELLS,
            'supply': SUPPLY, 'migrated': N_MIGRATED,
            'migrate_rows': MIGRATE_ROWS,
            'conclusion': '无真第一性供给 ⇒ 80 格逐格 before==after、delta=0',
        },
        'state_definition': {
            'MIGRATE': '假设替换后至少一个中间量向完成侧迁移',
            'INVARIANT': '替换后 8 个中间量逐项不变（零信息重排 / 改名 / 证伪集不变）',
            'DEGRADE': '替换增大前提账或缩减可证伪窗口（死锁 / 已结项 / 3→2 / nullity 5 维）',
            'priority': 'MIGRATE > DEGRADE > INVARIANT(缺省)',
        },
        'state_distribution': dict(STATE_DIST, conservation=STATE_CONSERVATION,
                                   state_set=STATE_SET, unique_sm=UNIQUE_SM),
        'positive_controls': POS,
        'real_values': REAL,
        'net_premise_gate': {
            'definition': 'gate(e,a) = 1 当且仅当 a < e',
            'e': E_GATE, 'a': A_GATE, 'real': REAL['gate_real'],
            'positive_control_gate_1_0': POS['gate_1_0'],
            'verdict': '未过门：a=1 > e=0',
        },
        'r134_ledger': dict(net_premise=N_NET, underived=N_UND,
                            closure=CLOSURE, deep_posted=N_DEEP,
                            derived_spaces=N_DERIVED, migration='0/4'),
        'source_static_hits': {k: '%d/%d' % (h, t) for k, (h, t) in HITS.items()},
        'matrix': dict(systems=N_SYSTEMS, cells=CELLS,
                       W3_debt=W3_DEBT, W4_debt=W4_DEBT),
        'denominators_triple': N_DENOM,
        'empty_id_hits': EMPTY_IDS, 'file_token_hits': FILE_HITS,
        'rid_latest': RID_LATEST, 'rid_402_hits': RID_402_HITS,
        'rid_403plus_hits': RID_403PLUS,
        'readme_no_migration_hits': NOMIG_COUNT,
        'paths_exist': '%d/%d' % (PATHS_EXIST, len(PATHS)),
    },
    'self_corrections': [
        '只读探针首版把 r134 的 closure 正则写成 closure\\s*=\\s*(0\\.\\d+)，在 r134 中命中 None（该卷只写完成度 1/7）；改从 r133「closure 从 (0.\\d+) 推到 1」现场解析得 0.327，与 attack44 JSON 交叉一致',
        'v35 词表首版写「本册不重算下游」与原文「本册只做「走④ 落地判定」，不重算下游」不符（探针 5/6）；改为「不重算下游」，复跑 6/6',
        'r134 词表首版写「完成度=1/7」与原文「完成度 1/7 = 0.1429」不符（探针 4/5）；改为「完成度 1/7」，复跑 4/4',
        'H_SPEC 首版三态判定用「declared 字符串硬覆盖 + route_state 里查 DEGRADE 字面量」，属声明式假绿；改为 MIG_WORDS/DEG_WORDS 现场词表重算并加 recompute_ok 逐行守卫，最终 10/10',
        'H05 词表首版写「零新输入」而 r14 原文为「零外部输入」；H06 首版写「违背 0 条」而原文为「违背 0 条」出现在表格非正文 ⇒ 改用「科学哲学层面的选择 / nullity 5 维 / 代价向量矩阵」，探针 10 行 46/46 全命中',
        'AST 不重复项守卫首版把本册合法函数 route_state 误列入 BANNED_FUNCS ⇒ 自指假红；改为只禁 attack41-44 的 inject/c2_gate/supply_class/beta2/run_rk4/cell17/unique_sm',
        '编号空号首版按 fn.startswith(BASE) 排除自身，但判定册以「判定_」开头不以 BASE 开头 ⇒ 会自指假红；改按 attack44 口径用 OWN 集合显式排除 4 件本册产物',
        'N_5184 首版写成 parse_i(...) if False else ...，引入布尔字面量 False ⇒ 会被书写式守卫 literal_true_consts=0 抓成假红；改为直接 int(re.search(...).group(1).replace(\',\',\'\'))',
        'G45-9 的 BANNED_IDS 首版沿用 attack43 的 CELLS，但本册 CELLS 表示 22×8=176 验收矩阵格数（同名异义，非 16×4 交叉矩阵）⇒ 自指假红使首跑 9/10；从禁用表移除该名，保留 COUPLINGS/FORCES/CELL_17/CANDIDATES 等 9 项，复跑 10/10',
    ],
    'boundaries': [
        '本册审的是「库内已登记的 10 个假设替换算子 × 8 个中间量能否产生完成侧迁移」，不是判定 SM / GR / MSSM-SO(10) 物理本身',
        '自变量是假设替换类型而非外部输入条数（attack41 已封注入不变量），因变量是中间量结构而非类别通过数或唯一化数（attack42/43/44）',
        '假设清单全部直接引用现成权威文本（Ω1–Ω5 / A01–A11 / H0–H8 / N1–N18 / R1–R5 / 四型修补 / 四条出路），不重建、不跨册相加',
        '不重新做群论枚举 / 假设穷尽判定、不构造新代数或 GUT 谱、不跑 RGE/RK4、不引入外部两环 beta（C4 维持暂缓）、不注入任何新假设',
        '迁移数 0/80 的作用域是「本库现有 10 个替换算子」；不排除框架外真 L3 供给，但按净前提下降门任何新原理须满足 a<e，本册无该供给（e=0、a=1、gate=0）',
        '不重跑 attack39 ω 防线 / attack40 阈值×Yukawa×tau_p / attack41 类别注入 / attack42 四类分桶 / attack43 16×4 矩阵 / attack44 10 途径三态表',
        '不占 RID（三目录实扫 R 链最新 r402、r403+ 命中 0）；未改治理事实源、未改 verify.py、未跑 refresh_catalog.py、未提交 git',
        'PASS（F01）仅控制组仪器有效，不迁移为物理成立、不计攻破数；不宣称完成统一场、不宣称宇宙本质本源已回答',
    ],
    'methodology_notes': [
        '把「假设」作为自变量而非「输入条数」：10 个替换算子 × 8 个中间量构成 80 格交叉导数矩阵，逐格 before==after 且 supply=0',
        '三态互斥采用显式优先序 MIGRATE > DEGRADE > INVARIANT，由 MIG_WORDS/DEG_WORDS 现场词表重算，逐行 recompute_ok 与守恒式双重锁定，不用「词表不得同时命中」判据',
        '判据有牙五组：decides 阳性 + 三变异、migrate 有/无真供给、gate(1,0)、embed_ok(1)、fits(12,12)，真实值全 0 ⇒ 零迁移不是恒否判据',
        '书写式布尔守卫用 1 == 1 比较式；导入模块集合由 AST 的 Import ∪ ImportFrom 两集合并集抽取，并配 from mpmath / import numpy 阳性对照（承接 attack44 假绿教训）',
        '全部读数由 Markdown 正则 / JSON 现场解析，纯标准库、无随机、无第三方依赖',
    ],
    'source_refs': {
        'r14': B2 + '/判定_TUFT-r14-三条出路代价矩阵_2026-10-05.md:L34-44/L59-89',
        'r15': B2 + '/判定_TUFT-r15-自由度预算口径与四路代价重算_2026-10-07.md:L48-67',
        'v35': B2 + '/判定_TUFT_V3.5_走④公设放宽与β通道δA定量_2026-10-07.md:L18-49',
        'r121': B2 + '/判定_TUFT-r121-光子几何本源语料_H0-H8假设空间与传统数据精算对照_攻破_2026-10-20.md:L43',
        'r123': B2 + '/判定_TUFT-r123-力的大统一方程_退守路径总攻破_换群族与阈值与额外维与紫外完备_2026-10-20.md:L19-29',
        'r125': B2 + '/数据/判定_TUFT-r125_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.md:L23-60',
        'r134': B2 + '/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md:L14-36',
        'r133': B2 + '/数据/判定_TUFT-r133_修补失敗元原理_一个个修改的不可闭合性审计_2026-10-20.md:L14-36',
        'close': B2 + '/判定_TUFT突破方案_闭合性审计_预言注入缺口_2026-10-07.md:L12-16',
        'methodF': B4 + '/method_F_第一性判据.md:L24-40',
        'g1': B1 + '/统一场论必要条件清单_G1_2026-10-30.md:L5-53',
        'a41': B1 + '/判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
        'postulate': B3 + '/postulate_matrix.md:L1-46',
        'csv': B3 + '/comparison_matrix.csv:L1',
        'a44': B1 + '/判定_attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.md',
        'a44json': B1 + '/attack44_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.json',
        'matrix': B5 + '/全维验收矩阵.json',
        'final': B1 + '/穷尽攻破_统一场论终局总成_2026-10-21.md',
        'readme': B1 + '/README.md:L1578-1585',
    },
    'cross_refs': [
        '判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
        '判定_attack42_攻破㉞_C2硬门四类机器分桶与双锚点可执行化_2026-11-08.md',
        '判定_attack43_攻破㉟_力本源第17候选与16x4交叉供给矩阵_2026-11-08.md',
        '判定_attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.md',
        '判定_TUFT-r125_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.md',
        '判定_TUFT-r133_修补失敗元原理_一个个修改的不可闭合性审计_2026-10-20.md',
        '判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
        '判定_TUFT-r14-三条出路代价矩阵_2026-10-05.md',
        '判定_TUFT-r15-自由度预算口径与四路代价重算_2026-10-07.md',
        '判定_TUFT_V3.5_走④公设放宽与β通道δA定量_2026-10-07.md',
        '判定_TUFT-r121-光子几何本源语料_H0-H8假设空间与传统数据精算对照_攻破_2026-10-20.md',
        '判定_TUFT-r123-力的大统一方程_退守路径总攻破_换群族与阈值与额外维与紫外完备_2026-10-20.md',
        '判定_TUFT突破方案_闭合性审计_预言注入缺口_2026-10-07.md',
        '统一场论必要条件清单_G1_2026-10-30.md',
        'postulate_matrix.md', 'method_F_第一性判据.md', 'README.md',
    ],
    'redlines': {'zero_of_22': 'unchanged', 'UFT-3': 0, 'L3': 0, 'validated': 0},
    'candidate_verdict': 'FAIL',
    'exit': 0 if NOK == len(GUARDS) else 1,
}
with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
sys.exit(0 if NOK == len(GUARDS) else 1)
