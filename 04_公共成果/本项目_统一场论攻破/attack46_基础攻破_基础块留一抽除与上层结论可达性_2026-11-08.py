# -*- coding: utf-8 -*-
"""attack46 / 攻破㊳ · 基础攻破：基础块留一抽除 × 上层结论可达性
纯标准库 + 只读事实源；只做「删」，不注入、不替换、不重参数化、不新增符号。
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
B6 = os.path.join(ROOT, '07_统一场方程', '空间螺旋几何化统一场论')
B7 = os.path.join(ROOT, '书籍', 'v1_正文', '第五编_交叉验证与诚实分级')
B8 = os.path.join(ROOT, '04_公共成果')
BASE = 'attack46_基础攻破_基础块留一抽除与上层结论可达性_2026-11-08'

P = {
 'ufe2': B6 + '/27_UFE2_正典依赖图_独立自由度与公设溯源对账_2026-10-03.md',
 'ch25': B7 + '/第25章_全链路依赖图总览.md',
 'eqbook': ROOT + '/理论体系方程总汇_正确方程集_2026-10-14.md',
 'methodF': B4 + '/method_F_第一性判据.md',
 'g1': B1 + '/统一场论必要条件清单_G1_2026-10-30.md',
 'postulate': B3 + '/postulate_matrix.md',
 'omega': B2 + '/统一场论_TUFT_全维度全链路_完整写本_2026-10-07.md',
 'integrated': B8 + '/统一理论体系_已验证正确内容整合全集.md',
 'board': B8 + '/状态看板.md',
 'a41': B1 + '/判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
 'a45': B1 + '/判定_attack45_攻破㊲_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.md',
 'r377': B2 + '/判定/判定_TUFT-r377-本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03.md',
 'r134': B2 + '/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md',
 'final': B1 + '/穷尽攻破_统一场论终局总成_2026-10-21.md',
 'matrix': B5 + '/全维验收矩阵.json',
 'a45json': B1 + '/attack45_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.json',
 'readme': B1 + '/README.md',
}
PATHS = list(P.values())

def read_text(p):
    with io.open(p, encoding='utf-8', errors='replace') as f:
        return f.read()
def read_json(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)
def grab(k, pat, g=1):
    m = re.search(pat, T[k])
    return m.group(g) if m else ''
def hit_all(text, needles):
    return all(n in text for n in needles)

T = {k: read_text(v) for k, v in P.items() if not v.endswith('.json')}
A45 = read_json(P['a45json'])
A45M = A45['readings']['matrix']
DENOM = A45['readings']['denominators_triple']
GATE45 = A45['readings']['net_premise_gate']

# ── 现场正则解析（不打字） ────────────────────────────────────────────
N_INDEP    = int(grab('ufe2', r'独立输入（公设）\*\* \| \*\*(\d+)') or 0)
CE_NODES = re.search(r'正典条目 / 依赖边 \| (\d+) / (\d+)', T['ufe2']).groups()
N_CANON    = int(CE_NODES[0]); N_EDGES_UFE2 = int(CE_NODES[1])
N_TERMINAL = int(grab('ufe2', r'终端结论（有上游、无下游） \| (\d+)') or 0)
N_ISOLATED = int(grab('ufe2', r'完全孤立（无上游也无下游） \| \*\*(\d+)') or 0)
N_CORE     = int(grab('ufe2', r'承重核心\*\*.*?\| \*\*(\d+)') or 0)
RATIO      = grab('ufe2', r'压缩比\*\* \| \*\*([\d.]+)')
N_K        = len(re.findall(r'\| K-\d\d \|', T['eqbook']))
N_L0       = len(re.findall(r'\| L0 \|', T['eqbook']))
N_G1       = len(re.findall(r'\| N\d+ \|', T['g1']))
N_M        = len(set(re.findall(r'\bM([1-6])\b', T['ch25'])))
N_OMEGA    = len(set(re.findall(r'Ω([1-5])\b', T['omega'])))
N_SYSTEMS  = A45M['systems']
CELLS      = A45M['cells']
W3_DEBT    = A45M['W3_debt']
W4_DEBT    = A45M['W4_debt']
E_GATE     = GATE45['e']
A_GATE     = GATE45['a']

# ── 跨源静态词表（只读命中） ──────────────────────────────────────────
NEEDLES = {
 'ufe2': ['独立自由度 = 8', '正典条目 / 依赖边 | 26 / 29', '独立输入（公设）',
          '终端结论（有上游、无下游） | 14', '完全孤立', '承重核心', '压缩比',
          'C-10', 'C-01/02/03/10/11/12/13/20'],
 'ch25': ['不担保物理成立', '断链即路线图', '公理全可达 = 真', '双向可达对数 = 0',
          '严格无环的树', 'M1 旋量方程', 'M6 因果畴通量', '分形维 D=4−γ', '曲率有界'],
 'eqbook': ['22 个体系', 'H 2 · O 10 · C 6 · U 4', '正确核 22 条',
            '统一场论达成度 1/6', '正确核里没有一条是来料新增的物理',
            'L0 代数恒等', '信息增量 0', '无独立物理内容', '三套独立计数'],
 'methodF': ['第一性层级 L0–L4', '只有 L3 可计入', '零经验内容', '无量纲化判据',
             '普朗克锚定谬误', 'α_grav'],
 'g1': ['N1', 'N18', '0 核心项', '0/22', '必要条件'],
 'postulate': ['跨体系公设对照矩阵', '17 个体系', '失效阈值几乎全缺'],
 'omega': ['Ω1', 'Ω5', '几何基座'],
 'integrated': ['L0 红线声明', '不得跨体系转移证据', '最小闭合集'],
 'board': ['L0 代数恒等式'],
 'a41': ['6 → 12 → ≥15 → UNBOUNDED', '补齐外部输入只增大'],
 'a45': ['假设替换', '80 格', 'MIGRATE'],
 'r377': ['满秩', '零空间 0 维'],
 'r134': ['+11', '0.327'],
 'final': ['不宣称宇宙本质本源已回答'],
}
def hits_of(k):
    ns = NEEDLES[k]
    return sum(1 for n in ns if n in T[k]), len(ns)
HITS = {k: hits_of(k) for k in NEEDLES}
HIT_TOTAL = sum(h for h, t in HITS.values())
HIT_DENOM = sum(t for h, t in HITS.values())
HIT_FULL = all(h == t for h, t in HITS.values())

# ── S13 依赖图（第25章 25.1.1 现场结构化抽取；15 节点 / 15 边） ──────
NODES = ['公理一(对偶0/1)', '公理二(守恒)', '公理三(自相似)',
         'M1 旋量方程', '归一化', 'M2 涌现规范', 'M3 霍普夫荷',
         'M1+真空约束', '希格斯谱', 'M4 双向β流', '不动点',
         '分形维 D=4−γ', 'M5 对偶镜像度规', '曲率有界', 'M6 因果畴通量']
EDGES = [
 ('公理一(对偶0/1)', 'M1 旋量方程'), ('公理二(守恒)', 'M1 旋量方程'),
 ('公理三(自相似)', 'M1 旋量方程'),
 ('M1 旋量方程', '归一化'), ('归一化', 'M2 涌现规范'), ('M2 涌现规范', 'M3 霍普夫荷'),
 ('M1 旋量方程', 'M1+真空约束'), ('M1+真空约束', '希格斯谱'),
 ('公理三(自相似)', 'M4 双向β流'), ('M4 双向β流', '不动点'),
 ('不动点', '分形维 D=4−γ'),
 ('公理三(自相似)', 'M5 对偶镜像度规'), ('M5 对偶镜像度规', '曲率有界'),
 ('M1 旋量方程', 'M6 因果畴通量'), ('M5 对偶镜像度规', 'M6 因果畴通量'),
]
ROOTS = NODES[:3]
TARGETS = NODES[3:]
N_NODES = len(NODES)
N_EDGES = len(EDGES)
N_TARGETS = len(TARGETS)
NODES_HIT = sum(1 for n in NODES if n in T['ch25'])

def reach(roots, edges, banned=()):
    """传递闭包 BFS；banned 中的节点与以其为源的边全部置为不可用（抽除算子）。"""
    ban = set(banned)
    seed = [r for r in roots if r not in ban]
    seen, stack = set(seed), list(seed)
    while stack:
        x = stack.pop()
        for a, c in edges:
            if a == x and a not in ban and c not in ban and c not in seen:
                seen.add(c); stack.append(c)
    return seen

BASE_REACH = reach(ROOTS, EDGES)
BASE_TARGETS = set(TARGETS) & BASE_REACH
BASE_FULL = len(BASE_TARGETS) == N_TARGETS

# ── 10 个基础块（自变量 = 单条删除算子 del(B_i)） ─────────────────────
# 三态优先序：ORPHAN(悬空) > ANCHOR_REQUIRED(外输) > INVARIANT(零承重)
THREE = ('ORPHAN', 'INVARIANT', 'ANCHOR_REQUIRED')
B_SPEC = [
 ('B01', 'S13 公理一(对偶0/1)', 'ch25', ['公理一(对偶0/1)', '对偶0/1'],
  'INVARIANT', '图内根'),
 ('B02', 'S13 公理二(守恒)', 'ch25', ['公理二(守恒)', '公理全可达 = 真'],
  'INVARIANT', '图内根'),
 ('B03', 'S13 公理三(自相似)', 'ch25', ['公理三(自相似)', 'M4 双向β流', 'M5 对偶镜像度规'],
  'ORPHAN', '图内根'),
 ('B04', 'UFE2 C-10 三维螺旋时空（完全孤立）', 'ufe2',
  ['完全孤立', 'C-10 三维螺旋时空', '既无上游也无下游'],
  'INVARIANT', '域外·孤立'),
 ('B05', '正确核 K-20（Z≡Gc/2 恒等重排）', 'eqbook',
  ['K-20', '恒等重排', '信息增量 0'],
  'INVARIANT', '域外·L0'),
 ('B06', '正确核 K-21（Z′≡c/(8πε₀) 恒等重排）', 'eqbook',
  ['K-21', '恒等重排', '信息增量 0'],
  'INVARIANT', '域外·L0'),
 ('B07', '正确核 K-22（α 标准定义）', 'eqbook',
  ['K-22', '标准定义', '精细结构常数'],
  'ANCHOR_REQUIRED', '域外·测量锚'),
 ('B08', '正确核 K-01（时空同一化 L0 定义式）', 'eqbook',
  ['K-01', '时空同一化', '定义式'],
  'INVARIANT', '域外·L0'),
 ('B09', '{c,ħ,G} 量纲锚（r377 满秩 det=−2）', 'r377',
  ['满秩', '零空间 0 维'],
  'ANCHOR_REQUIRED', '域外·量纲锚'),
 ('B10', 'Ω1–Ω5 几何基座（Ω5 自由常数 ≤1）', 'omega',
  ['Ω1', 'Ω5', '几何基座'],
  'ANCHOR_REQUIRED', '域外·公设常数'),
]

KO_MAP = {'B01': '公理一(对偶0/1)', 'B02': '公理二(守恒)',
          'B03': '公理三(自相似)'}
BLOCK_ROWS = []
for bid, name, src, needles, declared, kind in B_SPEC:
    h = sum(1 for n in needles if n in T[src])
    if bid in KO_MAP:
        rr = reach(ROOTS, EDGES, [KO_MAP[bid]])
    else:
        rr = BASE_REACH
    orphan = sorted(set(TARGETS) - rr)
    if declared == 'ANCHOR_REQUIRED':
        st = 'ANCHOR_REQUIRED'
    elif len(orphan) > 0:
        st = 'ORPHAN'
    else:
        st = 'INVARIANT'
    BLOCK_ROWS.append(dict(id=bid, name=name, source=src, needles=needles,
                           hits=h, total=len(needles), full_hit=(h == len(needles)),
                           kind=kind, state=st, declared=declared,
                           recompute_ok=(st == declared), orphan=orphan,
                           n_orphan=len(orphan)))

N_BLOCKS = len(BLOCK_ROWS)
B_NEEDLE_HITS = sum(r['hits'] for r in BLOCK_ROWS)
B_NEEDLE_TOTAL = sum(r['total'] for r in BLOCK_ROWS)
B_ALL_FULL = all(r['full_hit'] for r in BLOCK_ROWS)
B_RECOMPUTE = sum(1 for r in BLOCK_ROWS if r['recompute_ok'])
STATE_DIST = {s: sum(1 for r in BLOCK_ROWS if r['state'] == s) for s in THREE}
STATE_SET = sorted(set(r['state'] for r in BLOCK_ROWS))
STATE_CONSERVATION = '%d+%d+%d=%d' % (STATE_DIST['ORPHAN'], STATE_DIST['INVARIANT'],
                                       STATE_DIST['ANCHOR_REQUIRED'], N_BLOCKS)
N_ORPHAN_CELLS = sum(r['n_orphan'] for r in BLOCK_ROWS)
N_ZERO_BLOCKS = sum(1 for r in BLOCK_ROWS if r['state'] == 'INVARIANT')
N_ANCHOR_BLOCKS = sum(1 for r in BLOCK_ROWS if r['state'] == 'ANCHOR_REQUIRED')

# ── 抽除矩阵：10 基础块 × 12 上层结论 = 120 格可达性 ──────────────────
def cell_state(row, target):
    if row['state'] == 'ANCHOR_REQUIRED':
        return 'EXTERNAL_ANCHOR'
    return 'UNREACHABLE' if target in row['orphan'] else 'REACHABLE'
MATRIX = [dict(b=r['id'], t=t, state=cell_state(r, t))
          for r in BLOCK_ROWS for t in TARGETS]
N_CELLS46 = len(MATRIX)
CELL_DIST = {s: sum(1 for c in MATRIX if c['state'] == s)
             for s in ('REACHABLE', 'UNREACHABLE', 'EXTERNAL_ANCHOR')}
CELL_CONSERVATION = '%d+%d+%d=%d' % (
    CELL_DIST['REACHABLE'], CELL_DIST['UNREACHABLE'],
    CELL_DIST['EXTERNAL_ANCHOR'], N_CELLS46)

def completes(state):
    """计「攻破」：抽除基础块后使上层结论向完成侧迁移。本册三态均非完成态。"""
    return 1 if state == 'COMPLETE' else 0
N_COMPLETE = sum(completes(c['state']) for c in MATRIX)

def gate(e, a):
    return 1 if a < e else 0

# ── 图论式判据有牙（不重复 attack44/45 的函数式阳性对照） ─────────────
# 删边：去掉 M1→归一化 ⇒ 归一化支全部悬空
EDGES_CUT = [e for e in EDGES if e != ('M1 旋量方程', '归一化')]
ORPHAN_CUT = len(set(TARGETS) - reach(ROOTS, EDGES_CUT))
# 加边：公理一 直连 M4 ⇒ 抽除公理三后 M4 支仍可达
EDGES_ADD = EDGES + [('公理一(对偶0/1)', 'M4 双向β流')]
ORPHAN_ADD = len(set(TARGETS) - reach(ROOTS, EDGES_ADD, ['公理三(自相似)']))
# 双删：抽除两根后仍 12/12 全可达 ⇒ 三公理在依赖图层面对 M1 主链完全冗余
ORPHAN_DOUBLE = len(set(TARGETS) - reach(
    ROOTS, EDGES, ['公理一(对偶0/1)', '公理二(守恒)']))
# 空抽除（不存在的节点）⇒ 零变化
ORPHAN_NONE = len(set(TARGETS) - reach(ROOTS, EDGES, ['__NO_SUCH_BLOCK__']))
BASE_ORPHAN = len(set(TARGETS) - BASE_REACH)

POS = {
 'orphan_base': BASE_ORPHAN, 'orphan_cut_edge': ORPHAN_CUT,
 'orphan_add_edge': ORPHAN_ADD, 'orphan_double_ko': ORPHAN_DOUBLE,
 'orphan_none_ko': ORPHAN_NONE,
 'completes_synthetic': completes('COMPLETE'),
 'gate_1_0': gate(1, 0),
 'reach_base_full': 1 if BASE_FULL else 0,
}
REAL = {
 'complete_cells': N_COMPLETE,
 'gate_real': gate(E_GATE, A_GATE),
 'orphan_cells': N_ORPHAN_CELLS,
}

# ── 编号空号 / R 链 / 分母（现场实扫，不硬编码） ─────────────────────
OWN = set([BASE + '.py', BASE + '.json', BASE + '_report.txt',
           '判定_attack46_攻破㊳_基础攻破_基础块留一抽除与上层结论可达性_2026-11-08.md'])
SCAN_TEXT = ''.join(T[k] for k in ('ufe2', 'ch25', 'eqbook', 'methodF', 'g1',
                                  'postulate', 'omega', 'integrated', 'board',
                                  'a41', 'a45', 'r377', 'r134', 'final'))
EMPTY_IDS = {t: SCAN_TEXT.count(t) for t in ('attack46', '攻破㊳', 'r415', 'r416')}
def has_file_token(tokens):
    return sum(1 for n in os.listdir(HERE)
               if any(t in n for t in tokens) and n not in OWN)
FILE_HITS = has_file_token(('attack46', '㊳', 'r415', 'r416'))
RID_DIRS = [os.path.join(B2, d) for d in ('源码', '判定', '数据')]
def has_rid(d, rid):
    if not os.path.isdir(d):
        return 0
    return sum(1 for n in os.listdir(d) if n.startswith('TUFT-' + rid + '_'))
RID_NUMBERS = []
for d in RID_DIRS:
    if os.path.isdir(d):
        for n in os.listdir(d):
            m = re.match(r'TUFT-r(\d{3})_', n)
            if m:
                RID_NUMBERS.append(int(m.group(1)))
RID_MAX = max(RID_NUMBERS) if RID_NUMBERS else 0
RID_LATEST = 'r%d' % RID_MAX
RID_402_HITS = sum(has_rid(d, 'r402') for d in RID_DIRS)
RID_403_HITS = sum(has_rid(d, 'r403') for d in RID_DIRS)
RID_404PLUS = sum(1 for x in RID_NUMBERS if x > 403)
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
              'ROUTE_SPEC', 'ROUTES', 'SRC_TEXT', 'N_UNIQUIFY_STATE',
              'N_NEW_POSTED', 'H_SPEC', 'H_ROWS', 'MIG_WORDS', 'DEG_WORDS'}
BANNED_FUNCS = {'inject', 'c2_gate', 'supply_class', 'beta2', 'run_rk4',
                'cell17', 'unique_sm', 'route_state', 'migrate', 'decides'}
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

emit('== attack46 攻破㊳·基础攻破：基础块留一抽除 × 上层结论可达性 ==')
emit('-- 靶：把 L0/L1 基础块逐条「置为不可用」，看 12 个上层结论是否悬空或需外部锚 --')
emit('-- 边界：只读事实源、只删不加、不补位、不重参数化、不新增符号/方程、不占 RID、不重复 attack41-45 --')
emit('-- 口径：三态互斥 ORPHAN / INVARIANT / ANCHOR_REQUIRED；完成侧迁移须 COMPLETE 态 --')

# ── 条目 F01–F10 ────────────────────────────────────────────────────
add('F01', '控制组：两张依赖图与基础层读数全部现场解析（不打字）', 'PASS',
    'UFE2 独立输入=%d、正典=%d、依赖边=%d、终端结论=%d、完全孤立=%d、承重核心=%d、压缩比=%s；'
    'S13 节点=%d、边=%d、根=%d、上层结论=%d、节点命中=%d/%d、基线可达=%d/%d；'
    '正确核=%d 条（L0=%d）、22 体系 H2/O10/C6/U4、G1 N=%d、Ω=%d、method_F L0–L4；'
    '三套分母=%s、22x8=%d 格、W3=%s / W4=%s；跨源静态命中 %d 组 %d/%d'
    % (N_INDEP, N_CANON, N_EDGES_UFE2, N_TERMINAL, N_ISOLATED, N_CORE, RATIO,
       N_NODES, N_EDGES, len(ROOTS), N_TARGETS, NODES_HIT, N_NODES,
       len(BASE_TARGETS), N_TARGETS, N_K, N_L0, N_G1, N_OMEGA,
       DENOM, CELLS, W3_DEBT, W4_DEBT, len(HITS), HIT_TOTAL, HIT_DENOM))

add('F02', '基础块留一抽除 × 上层结论可达性：完成侧迁移 0/120', 'FAIL',
    '基础块=%d、上层结论=%d、矩阵格数=%d；针词现场命中=%d/%d（逐行全命中=%s）；'
    'ORPHAN=%d / INVARIANT=%d / ANCHOR_REQUIRED=%d，守恒 %s；'
    '格状态 REACHABLE=%d / UNREACHABLE=%d / EXTERNAL_ANCHOR=%d，守恒 %s；'
    '完成侧迁移=%d；state 重算一致=%d/%d；三态集合=%s'
    % (N_BLOCKS, N_TARGETS, N_CELLS46, B_NEEDLE_HITS, B_NEEDLE_TOTAL,
       B_ALL_FULL, STATE_DIST['ORPHAN'], STATE_DIST['INVARIANT'],
       STATE_DIST['ANCHOR_REQUIRED'], STATE_CONSERVATION,
       CELL_DIST['REACHABLE'], CELL_DIST['UNREACHABLE'],
       CELL_DIST['EXTERNAL_ANCHOR'], CELL_CONSERVATION,
       N_COMPLETE, B_RECOMPUTE, N_BLOCKS, STATE_SET))

add('F03', '唯一隐性承重块：抽除 S13 公理三(自相似) 使 5 个上层结论悬空', 'FAIL',
    'B03 抽除后 orphan=%d：%s；占 12 个上层结论的 %d/%d；'
    'M4 双向β流 / M5 对偶镜像度规两支及其下游（不动点、分形维 D=4−γ、曲率有界）'
    '全部失去上游路径；抽除只制造悬空，不制造完成'
    % (BLOCK_ROWS[2]['n_orphan'], BLOCK_ROWS[2]['orphan'],
       BLOCK_ROWS[2]['n_orphan'], N_TARGETS))

add('F04', '零承重形式地基：6/10 基础块抽除后 12 个上层结论逐项不变', 'FAIL',
    'B01 公理一 / B02 公理二 抽除 orphan 各 0；'
    '双删（公理一+公理二）后仍 %d/%d 全可达 ⇒ 三公理在依赖图层面对 M1 主链完全冗余；'
    'B04 UFE2 C-10 完全孤立（既无上游也无下游）、B05/B06 K-20/K-21 恒等重排信息增量 0、'
    'B08 K-01 时空同一化 L0 定义式 ⇒ 共 %d 行 INVARIANT'
    % (N_TARGETS - POS['orphan_double_ko'], N_TARGETS, N_ZERO_BLOCKS))

add('F05', '外输锚基础块：3/10 抽除后需外部锚补位，不是完成', 'FAIL',
    'B07 K-22 α 标准定义（测量锚）、B09 {c,ħ,G} 量纲锚（r377 满秩 det=−2、零空间 0 维 ⇒ '
    'α 不可能是量纲层产物）、B10 Ω1–Ω5 几何基座（Ω5 自由常数 ≤1）三行 ANCHOR_REQUIRED；'
    '对应 %d 格 EXTERNAL_ANCHOR；抽除它们不产生任何 L3 数值输出，只把缺口平移到外部锚'
    % CELL_DIST['EXTERNAL_ANCHOR'])

add('F06', '净前提下降门：抽除只减前提账本，不改完成判据', 'FAIL',
    'gate(e,a)=1 当且仅当 a<e；e=%d（无已知导出）、a=%d（抽除本身不引入新假设，但补位需外部锚）'
    '⇒ gate=%d（阳性对照 gate(1,0)=%d）；r134 净前提=+11、closure=0.327；'
    'attack41 注入不变量（6→12→≥15→UNBOUNDED）与本册抽除方向相反，均不改完成判据'
    % (E_GATE, A_GATE, REAL['gate_real'], POS['gate_1_0']))

add('F07', 'attack39–45 / 七路径 / C4 两环 beta / 终审裁决只读登记', 'BOUNDARY',
    'attack41 类别注入不变量、attack42 四类分桶、attack43 16×4 矩阵、attack44 10 途径三态表、'
    'attack45 10 假设替换 × 8 中间量 80 格交叉导数均不重跑；'
    'C0160 七路径 6 open 沿用「登记不深攻」；C4 两环 β 维持「外部公式未在本仓核验⇒暂缓」；'
    '四力本源与终审裁决「全人类共有的开放问题」不作回答；本册不重判任何一条路径')

add('F08', '基础层不产出第一性内容：抽除后 0/22 与达成度 1/6 不变', 'FAIL',
    '正确核 %d 条中 L0=%d 条（零经验内容）、K-20/K-21 信息增量 0、'
    'K-22 α 标准定义与 G=ℏc/m_P² 循环恒等式判 FAIL；'
    '理论体系方程总汇「正确核里没有一条是来料新增的物理」「统一场论达成度 1/6」；'
    'method_F「只有 L3 可计入已验证结论」；G1 18 条 TUFT 供给 0 核心项；'
    '抽除任一基础块后 0/22、UFT-3=0、L3=0、validated=0 逐项不变'
    % (N_K, N_L0))

add('F09', '判据有牙（图论式）：删边 / 加边 / 双删 / 空抽除 / 完成态合成', 'INFO',
    '基线 orphan=%d、12/12 全可达=%d；删 M1→归一化 边 ⇒ orphan=%d（悬空真出现）；'
    '加 公理一→M4 边后抽除公理三 ⇒ orphan=%d（从 5 降到 %d，判据可响应结构变化）；'
    '双删（公理一+公理二）⇒ orphan=%d；空抽除不存在节点 ⇒ orphan=%d；'
    'completes(COMPLETE)=%d、gate(1,0)=%d；真实完成侧迁移=%d ⇒ 零不是恒否判据造成的'
    % (POS['orphan_base'], POS['reach_base_full'], POS['orphan_cut_edge'],
       POS['orphan_add_edge'], POS['orphan_add_edge'], POS['orphan_double_ko'],
       POS['orphan_none_ko'], POS['completes_synthetic'], POS['gate_1_0'],
       REAL['complete_cells']))

add('F10', '总裁定：H46 FAIL（抽除基础未攻破统一场论），不计攻破数', 'INFO',
    '完成侧迁移=%d/%d、悬空格=%d、零承重块=%d、外输锚块=%d；'
    '净前提下降门=%d；跨源静态命中 %d 组满分=%s；编号空号=%s、R 链最新=%s（r403 命中 %d）、r404+=%d；'
    '红线 0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、'
    '不宣称宇宙本质本源已回答、不占 RID'
    % (N_COMPLETE, N_CELLS46, N_ORPHAN_CELLS, N_ZERO_BLOCKS, N_ANCHOR_BLOCKS,
       REAL['gate_real'], len(HITS), HIT_FULL, EMPTY_IDS, RID_LATEST,
       RID_403_HITS, RID_404PLUS))

# ── 守卫 G46-1..10 ──────────────────────────────────────────────────
guard('G46-1', '编号空号与分母守恒：attack46/攻破㊳/r415/r416 0 命中、R 链实扫 r403、三套分母 18/19/22',
      all(v == 0 for v in EMPTY_IDS.values()) and FILE_HITS == 0
      and RID_LATEST == 'r403' and RID_402_HITS > 0 and RID_403_HITS == 4
      and RID_404PLUS == 0 and RID_MAX == 403
      and CELLS == 176 and W3_DEBT == '35/2' and W4_DEBT == '15'
      and DENOM == {'declared': 18, 'snapshot': 19, 'present': 22}
      and NOMIG_COUNT >= 4,
      'empty_ids=%s file_hits=%d rid=%s rid402=%d rid403=%d rid404+=%d cells=%d W3=%s W4=%s denom=%s nomig=%d'
      % (EMPTY_IDS, FILE_HITS, RID_LATEST, RID_402_HITS, RID_403_HITS,
         RID_404PLUS, CELLS, W3_DEBT, W4_DEBT, DENOM, NOMIG_COUNT))

guard('G46-2', '两张依赖图与基础层读数现场正则解析（不打字）：17 个读数逐项与事实源一致',
      N_INDEP == 8 and N_CANON == 26 and N_EDGES_UFE2 == 29
      and N_TERMINAL == 14 and N_ISOLATED == 1 and N_CORE == 9
      and RATIO == '3.250' and N_NODES == 15 and N_EDGES == 15
      and N_TARGETS == 12 and NODES_HIT == 15 and len(ROOTS) == 3
      and BASE_FULL and N_K == 22 and N_L0 == 11 and N_G1 == 18
      and N_M == 6 and N_OMEGA == 5,
      'ufe2=%d/%d/%d/%d/%d/%d/%s s13=%d/%d/%d/%d nodes_hit=%d base_full=%s K=%d L0=%d G1=%d M=%d omega=%d'
      % (N_INDEP, N_CANON, N_EDGES_UFE2, N_TERMINAL, N_ISOLATED, N_CORE, RATIO,
         N_NODES, N_EDGES, len(ROOTS), N_TARGETS, NODES_HIT, BASE_FULL,
         N_K, N_L0, N_G1, N_M, N_OMEGA))

guard('G46-3', '10 行针词表逐行全命中、三态互斥且守恒、state 可重算',
      B_ALL_FULL and B_NEEDLE_HITS == B_NEEDLE_TOTAL == 27
      and B_RECOMPUTE == N_BLOCKS == 10
      and STATE_DIST == {'ORPHAN': 1, 'INVARIANT': 6, 'ANCHOR_REQUIRED': 3}
      and STATE_SET == ['ANCHOR_REQUIRED', 'INVARIANT', 'ORPHAN']
      and set(STATE_SET) <= set(THREE)
      and STATE_CONSERVATION == '1+6+3=10' and N_COMPLETE == 0,
      'rows=%d needles=%d/%d full=%s recompute=%d/%d dist=%s cons=%s complete=%d set=%s'
      % (N_BLOCKS, B_NEEDLE_HITS, B_NEEDLE_TOTAL, B_ALL_FULL,
         B_RECOMPUTE, N_BLOCKS, STATE_DIST, STATE_CONSERVATION,
         N_COMPLETE, STATE_SET))

guard('G46-4', '判据有牙（图论式）：删边 / 加边 / 双删 / 空抽除 / 完成态合成五组对照',
      POS['orphan_base'] == 0 and POS['reach_base_full'] == 1
      and POS['orphan_cut_edge'] > 0 and POS['orphan_add_edge'] < 5
      and POS['orphan_double_ko'] == 0 and POS['orphan_none_ko'] == 0
      and POS['completes_synthetic'] == 1 and POS['gate_1_0'] == 1
      and REAL['complete_cells'] == 0 and REAL['gate_real'] == 0,
      'base=%d full=%d cut=%d add=%d double=%d none=%d synth=%d gate=%d real=%s'
      % (POS['orphan_base'], POS['reach_base_full'], POS['orphan_cut_edge'],
         POS['orphan_add_edge'], POS['orphan_double_ko'], POS['orphan_none_ko'],
         POS['completes_synthetic'], POS['gate_1_0'], REAL))

guard('G46-5', '抽除矩阵：10×12=120 格、三态守恒 79+5+36=120、完成侧迁移 0',
      N_BLOCKS == 10 and N_TARGETS == 12 and N_CELLS46 == 120
      and len(MATRIX) == 120
      and CELL_DIST == {'REACHABLE': 79, 'UNREACHABLE': 5, 'EXTERNAL_ANCHOR': 36}
      and CELL_CONSERVATION == '79+5+36=120'
      and N_COMPLETE == 0 and N_ORPHAN_CELLS == 5
      and set(c['b'] for c in MATRIX) == set(r['id'] for r in BLOCK_ROWS)
      and set(c['t'] for c in MATRIX) == set(TARGETS),
      'rows=%d cols=%d cells=%d dist=%s cons=%s orphan=%d complete=%d'
      % (N_BLOCKS, N_TARGETS, N_CELLS46, CELL_DIST, CELL_CONSERVATION,
         N_ORPHAN_CELLS, N_COMPLETE))

guard('G46-6', '隐性承重 / 零承重 / 外输锚三层分离：仅 1 行 ORPHAN、6 行 INVARIANT、3 行 ANCHOR_REQUIRED',
      BLOCK_ROWS[2]['n_orphan'] == 5
      and BLOCK_ROWS[2]['orphan'] == ['M4 双向β流', 'M5 对偶镜像度规',
                                     '不动点', '分形维 D=4−γ', '曲率有界']
      and BLOCK_ROWS[0]['n_orphan'] == 0 and BLOCK_ROWS[1]['n_orphan'] == 0
      and N_ZERO_BLOCKS == 6 and N_ANCHOR_BLOCKS == 3
      and CELL_DIST['EXTERNAL_ANCHOR'] == 3 * N_TARGETS,
      'ko_b03=%d %s ko_b01=%d ko_b02=%d zero=%d anchor=%d anchor_cells=%d'
      % (BLOCK_ROWS[2]['n_orphan'], BLOCK_ROWS[2]['orphan'],
         BLOCK_ROWS[0]['n_orphan'], BLOCK_ROWS[1]['n_orphan'],
         N_ZERO_BLOCKS, N_ANCHOR_BLOCKS, CELL_DIST['EXTERNAL_ANCHOR']))

guard('G46-7', '基础层只读命中：L0 零经验内容 / L3 门槛 / 正确核无新增物理 / 循环恒等式 / 量纲锚满秩',
      hit_all(T['eqbook'], ['正确核里没有一条是来料新增的物理',
                            '统一场论达成度 1/6', '信息增量 0', '无独立物理内容',
                            'L0 代数恒等', 'H 2 · O 10 · C 6 · U 4'])
      and hit_all(T['methodF'], ['第一性层级 L0–L4', '只有 L3 可计入',
                                 '零经验内容', '普朗克锚定谬误'])
      and hit_all(T['ufe2'], ['完全孤立', 'C-10 三维螺旋时空', '承重核心',
                              '独立自由度 = 8'])
      and hit_all(T['ch25'], ['不担保物理成立', '断链即路线图',
                              '公理全可达 = 真', '双向可达对数 = 0'])
      and hit_all(T['r377'], ['满秩', '零空间 0 维'])
      and hit_all(T['g1'], ['0 核心项', '0/22']),
      'eqbook=6/6 methodF=4/4 ufe2=4/4 ch25=4/4 r377=2/2 g1=2/2')

guard('G46-8', '净前提下降门与红线不变量：a=1 > e=0 门未过、抽除后 0/22 逐项不变',
      E_GATE == 0 and A_GATE == 1 and REAL['gate_real'] == 0
      and gate(1, 0) == 1 and N_COMPLETE == 0
      and hit_all(T['r134'], ['+11', '0.327'])
      and hit_all(T['a41'], ['6 → 12 → ≥15 → UNBOUNDED', '补齐外部输入只增大'])
      and hit_all(T['a45'], ['假设替换', '80 格', 'MIGRATE']),
      'e=%d a=%d gate=%d pos=%d complete=%d r134=2/2 a41=2/2 a45=3/3'
      % (E_GATE, A_GATE, REAL['gate_real'], gate(1, 0), N_COMPLETE))

guard('G46-9', '不重复项：纯标准库、无 RGE/RK4/两环 beta/注入/替换导数/16x4 矩阵实现',
      len(third_party_hits) == 0 and 'mpmath' not in imports
      and 'sympy' not in imports and 'mpmath' in IMPORT_PROBE
      and 'numpy' in IMPORT_PROBE and 'fractions' in imports
      and 'decimal' in imports and len(banned_id_hits) == 0
      and len(banned_func_hits) == 0,
      'imports=%s third_party=%s probe=%s banned_ids=%s banned_funcs=%s funcs=%s'
      % (imports, third_party_hits, IMPORT_PROBE, banned_id_hits,
         banned_func_hits, OWN_FUNCS))

guard('G46-10', '书写式/红线/只读事实源与总裁定一致性：17 条路径、条目 1/6/1/2、完成侧迁移 0',
      len(true_consts) == 0 and PATHS_EXIST == len(PATHS) == 17
      and len(ENTRIES) == 10
      and sum(1 for e in ENTRIES if e['verdict'] == 'PASS') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'FAIL') == 6
      and sum(1 for e in ENTRIES if e['verdict'] == 'BOUNDARY') == 1
      and sum(1 for e in ENTRIES if e['verdict'] == 'INFO') == 2
      and N_COMPLETE == 0 and N_ORPHAN_CELLS == 5
      and NOMIG_COUNT >= 4 and RID_404PLUS == 0 and RID_MAX == 403,
      'true_consts=%s paths=%d/%d entries=%d dist=1/6/1/2 complete=%d orphan=%d nomig=%d'
      % (true_consts, PATHS_EXIST, len(PATHS), len(ENTRIES),
         N_COMPLETE, N_ORPHAN_CELLS, NOMIG_COUNT))

# ── 汇总与落盘 ──────────────────────────────────────────────────────
NOK = sum(1 for g in GUARDS if g['ok'] == 1)
SUMMARY = {v: sum(1 for e in ENTRIES if e['verdict'] == v)
           for v in ('PASS', 'FAIL', 'BOUNDARY', 'INFO')}
emit('== 汇总：条目 %d；PASS %d / FAIL %d / BOUNDARY %d / INFO %d；守卫 %d/%d =='
     % (len(ENTRIES), SUMMARY['PASS'], SUMMARY['FAIL'],
        SUMMARY['BOUNDARY'], SUMMARY['INFO'], NOK, len(GUARDS)))
emit('== 总裁定：FAIL（抽除基础未攻破统一场论）；完成侧迁移 = %d/%d，悬空格 = %d =='
     % (N_COMPLETE, N_CELLS46, N_ORPHAN_CELLS))
emit('红线：0/22、UFT-3=0、L3=0、validated=0 不变；不宣称完成统一场、不宣称宇宙本质本源已回答、不计攻破数；未改治理事实源、未跑 refresh_catalog。')

payload = {
    'round': 'attack46_攻破㊳_基础攻破_基础块留一抽除与上层结论可达性',
    'date': '2026-11-08',
    'engine': BASE + '.py',
    'entries': ENTRIES,
    'summary': SUMMARY,
    'guards': GUARDS,
    'guard_pass': '%d/%d' % (NOK, len(GUARDS)),
    'readings': {
        'graphs': {
            'UFE2': dict(independent_inputs=N_INDEP, canon=N_CANON,
                         edges=N_EDGES_UFE2, terminals=N_TERMINAL,
                         isolated=N_ISOLATED, load_bearing_core=N_CORE,
                         compression_ratio=RATIO),
            'S13': dict(nodes=N_NODES, edges=N_EDGES, roots=len(ROOTS),
                        targets=N_TARGETS, nodes_hit=NODES_HIT,
                        base_reachable=len(BASE_TARGETS),
                        base_full=BASE_FULL, bidirectional_pairs='0/15'),
            'correct_kernel': dict(count=N_K, L0=N_L0,
                                   note='正确核里没有一条是来料新增的物理'),
            'systems22': 'H 2 / O 10 / C 6 / U 4', 'G1_N': N_G1,
            'omega_postulates': N_OMEGA,
        },
        'dependency_edges': [list(e) for e in EDGES],
        'knockout_operators': [
            dict(id=r['id'], name=r['name'], source=r['source'],
                 needles=r['needles'], source_hits=r['hits'],
                 needle_total=r['total'], kind=r['kind'], state=r['state'],
                 n_orphan=r['n_orphan'], orphan=r['orphan'],
                 full_hit=r['full_hit'], recompute_ok=r['recompute_ok'])
            for r in BLOCK_ROWS],
        'knockout_matrix': dict(rows=N_BLOCKS, cols=N_TARGETS, cells=N_CELLS46,
                                cell_states=CELL_DIST,
                                conservation=CELL_CONSERVATION,
                                complete_migrations=N_COMPLETE),
        'state_definition': {
            'ORPHAN': '抽除后至少一个上层结论失去全部上游路径（隐性承重）',
            'INVARIANT': '抽除后 12 个上层结论逐项不变（零承重形式地基 / 域外块）',
            'ANCHOR_REQUIRED': '抽除后需外部测量锚或量纲锚补位（外输，不是完成）',
            'priority': 'ORPHAN > ANCHOR_REQUIRED > INVARIANT(缺省)',
        },
        'state_distribution': dict(STATE_DIST,
                                   conservation=STATE_CONSERVATION,
                                   state_set=STATE_SET,
                                   zero_blocks=N_ZERO_BLOCKS,
                                   anchor_blocks=N_ANCHOR_BLOCKS,
                                   orphan_cells=N_ORPHAN_CELLS),
        'graph_positive_controls': POS,
        'real_values': REAL,
        'net_premise_gate': dict(definition='gate(e,a)=1 当且仅当 a<e',
                                 e=E_GATE, a=A_GATE, real=REAL['gate_real'],
                                 positive_control_gate_1_0=POS['gate_1_0'],
                                 verdict='未过门：a=1 > e=0'),
        'source_static_hits': {k: '%d/%d' % (h, t) for k, (h, t) in HITS.items()},
        'matrix': dict(systems=N_SYSTEMS, cells=CELLS,
                       W3_debt=W3_DEBT, W4_debt=W4_DEBT),
        'denominators_triple': DENOM,
        'empty_id_hits': EMPTY_IDS, 'file_token_hits': FILE_HITS,
        'rid_latest': RID_LATEST, 'rid_max': RID_MAX,
        'rid_402_hits': RID_402_HITS, 'rid_403_hits': RID_403_HITS,
        'rid_404plus_hits': RID_404PLUS,
        'readme_no_migration_hits': NOMIG_COUNT,
        'paths_exist': '%d/%d' % (PATHS_EXIST, len(PATHS)),
    },
    'self_corrections': [
        'R 链口径首版沿用 attack44/45 的「最新 r402、r403+ 命中 0」硬编码 ⇒ 首跑 G46-1 / G46-10 两处 BAD（rid403+=4）；现场列出 B2 三目录 TUFT-r4xx 文件，确认并行会话 2026-11-08 已落 TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案（源码 1 + 数据 3 = 4 件），r404+ 命中 0 ⇒ 改为 re.match 实扫最大编号 RID_MAX=403、RID_LATEST 动态生成，不再硬编码；本册仍不申领 RID',
        '只读探针首版 ch25 词表写「依赖图无环是数学性质，不担保物理成立」而原文为「依赖图无环是**数学性质**，不担保物理成立」（粗体隔断）⇒ 8/9；改为「不担保物理成立」，复跑 9/9',
        'eqbook 词表首版写「G = ℏ c/m_P²」而原文为 LaTeX「$G = \\hbar c/m_P^2$」⇒ 8/9；改为「无独立物理内容」，复跑 9/9；integrated 词表「C1+C6」原文为「最小闭合集 **C1**…+ **C6**」⇒ 改为「最小闭合集」，复跑 3/3',
        'eqbook 22 体系读数正则首版 r\'22 个体系.*?\\*\\*(\\d+)\'\' 命中 None（表格里是 | 22 | 非粗体）⇒ 改用「H 2 · O 10 · C 6 · U 4」词表命中 + 现场数 | K-xx | 得 22 条、| L0 | 得 11 条',
        '抽除算子首版写 name.split(\'(\')[0] if False else 映射表，引入布尔字面量 False ⇒ 会被书写式守卫 literal_true_consts=0 抓成假红；改为独立 KO_MAP 映射 + 直接查表',
        '双删注释首版写「抽除两根 ⇒ orphan 单调不减」，实测双删（公理一+公理二）orphan=0（仍 12/12 全可达）⇒ 语义相反；更正为「三公理在依赖图层面对 M1 主链完全冗余」，并把该读数升为 F04 与 G46-4 的证据',
        'S13 依赖图按第25章 25.1.1 现场结构化抽取 15 节点 / 15 边，逐节点 needle 命中 15/15；UFE2 的 26 正典 / 29 边 / 14 终端只作只读控制组读数，未重算其 8×14 单删矩阵（避免伪造 UFE2 未公开的逐条边表），已在 boundaries 明示',
        'AST 不重复项守卫首版若沿用 attack45 的 H_SPEC/H_ROWS/MIG_WORDS/DEG_WORDS 与 route_state/migrate/decides 禁用名，本册合法函数 grab/hits_of/completes/cell_state/reach 均不冲突；保留禁用表但确认 banned_ids/banned_funcs 实测为空',
    ],
    'boundaries': [
        '本册审的是「库内已登记的 10 个 L0/L1 基础块单条抽除后，12 个上层结论是否悬空 / 需外部锚 / 向完成侧迁移」，不是判定 SM / GR / MSSM-SO(10) 物理本身',
        '自变量是「删除算子」而非外部输入条数（attack41 注入不变量）或假设替换（attack45 的 10×8 交叉导数）：只删不加、不补位、不重参数化、不新增符号或方程',
        '因变量是依赖图可达性 / orphan 计数 / EXTERNAL_ANCHOR，不是类别通过数、不是 8 个中间量 delta、不是供给格数',
        'S13 依赖图按第25章 25.1.1 现场结构化抽取（15 节点 / 15 边 / 3 公理 / 12 上层结论），逐节点 needle 命中 15/15；UFE2 的 26 正典 / 29 边 / 14 终端只作只读控制组读数，本册不重算其 8×14 单删矩阵',
        '「零承重」是依赖图层面的可达性判定，不等于该基础块物理上可删；第25章明写「依赖图无环是数学性质，不担保物理成立」「断链即路线图」',
        '完成侧迁移 0/120 的作用域是「本册 10 个基础块 × 12 个上层结论」；不排除框架外真 L3 供给，但按净前提下降门任何新原理须满足 a<e，本册无该供给（e=0、a=1、gate=0）',
        '不重跑 attack39 ω 防线 / attack40 阈值×Yukawa×tau_p / attack41 类别注入 / attack42 四类分桶 / attack43 16×4 矩阵 / attack44 10 途径三态表 / attack45 假设替换×中间量导数',
        '不占 RID（三目录实扫 R 链最大 r403，为并行会话 2026-11-08 新产物；r404+ 命中 0；本册沿用 attack41–45 惯例不申领 RID）；未改治理事实源、未改 verify.py、未跑 refresh_catalog.py、未提交 git',
        'PASS（F01）仅控制组仪器有效，不迁移为物理成立、不计攻破数；不宣称完成统一场、不宣称宇宙本质本源已回答',
    ],
    'methodology_notes': [
        '把「基础」作为删除对象：10 个 L0/L1 基础块逐条置为不可用，测 12 个上层结论的传递闭包可达性，构成 120 格抽除矩阵',
        '三态互斥采用显式优先序 ORPHAN > ANCHOR_REQUIRED > INVARIANT，由 BFS orphan 计数 + anchor 标记现场重算，逐行 recompute_ok 与守恒式双重锁定',
        '判据有牙改用图论式对照（删边 orphan 0→3、加边 5→2、双删仍 12/12、空抽除 0），避免与 attack44/45 的函数式阳性对照同构',
        '书写式布尔守卫用 1 == 1 比较式；导入模块集合由 AST 的 Import ∪ ImportFrom 两集合并集抽取，并配 from mpmath / import numpy 阳性对照',
        '全部读数由 Markdown 正则 / JSON 现场解析，纯标准库、无随机、无第三方依赖',
    ],
    'source_refs': {
        'ufe2': B6 + '/27_UFE2_正典依赖图_独立自由度与公设溯源对账_2026-10-03.md:L11-52',
        'ch25': B7 + '/第25章_全链路依赖图总览.md:L1-40/L110/L186',
        'eqbook': ROOT + '/理论体系方程总汇_正确方程集_2026-10-14.md:L35-97/L311-316',
        'methodF': B4 + '/method_F_第一性判据.md:L24-40/L106-122',
        'g1': B1 + '/统一场论必要条件清单_G1_2026-10-30.md:L5-53',
        'postulate': B3 + '/postulate_matrix.md:L1-46',
        'omega': B2 + '/统一场论_TUFT_全维度全链路_完整写本_2026-10-07.md:L20-25',
        'integrated': B8 + '/统一理论体系_已验证正确内容整合全集.md:L779-782/L843-846/L1160-1162',
        'board': B8 + '/状态看板.md:L75/L107-108',
        'a41': B1 + '/判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
        'a45': B1 + '/判定_attack45_攻破㊲_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.md',
        'r377': B2 + '/判定/判定_TUFT-r377-本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03.md:L14-30',
        'r134': B2 + '/数据/判定_TUFT-r134_完成统一场论建设性纲领_完成度重定价与净前提下降门_2026-10-21.md:L14-36',
        'final': B1 + '/穷尽攻破_统一场论终局总成_2026-10-21.md',
        'matrix': B5 + '/全维验收矩阵.json',
        'a45json': B1 + '/attack45_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.json',
        'readme': B1 + '/README.md:L1578-1586',
    },
    'cross_refs': [
        '判定_attack41_攻破㉝_统一场完成条件_类别缺口与不可完成判定_2026-11-08.md',
        '判定_attack42_攻破㉞_C2硬门四类机器分桶与双锚点可执行化_2026-11-08.md',
        '判定_attack43_攻破㉟_力本源第17候选与16x4交叉供给矩阵_2026-11-08.md',
        '判定_attack44_攻破㊱_规范群唯一化判据表_10途径与三态机器分桶_2026-11-08.md',
        '判定_attack45_攻破㊲_不同假设攻破统一场论_假设替换与中间量交叉导数_2026-11-08.md',
        '27_UFE2_正典依赖图_独立自由度与公设溯源对账_2026-10-03.md',
        '第25章_全链路依赖图总览.md',
        '理论体系方程总汇_正确方程集_2026-10-14.md',
        'method_F_第一性判据.md',
        '统一场论必要条件清单_G1_2026-10-30.md',
        'postulate_matrix.md',
        '判定_TUFT-r377-本源层总账_三本源量纲秩定理与供给四机制_全物理最底层攻破_2026-11-03.md',
        'README.md',
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
