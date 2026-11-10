# -*- coding: utf-8 -*-
"""attack55 / 攻破㊼ · 换公理集出口定价：方向门可达路径分类与全库供给普查.

REVERSE-DERIVATION continuation of attack54.  attack54 priced the inside of
the existing axiom quota (INFEASIBLE) but explicitly left two exits unpriced:
"换公理集 / 新来料出口".  This ledger parameterises those exits as executable
actions (a = new independent inputs, e = eliminated old inputs, s = axiom-swap
flag, R = stock of un-used structural dependencies among existing inputs,
o = endogenous outputs) and proves, by exhaustive enumeration, that

    GATE(delta = a - e < 0)  ==>  s == 0  AND  R >= 1,

i.e. the only GATE-reachable action class is STRUCTURE_IDENTIFY (discover a
dependence among ALREADY-EXISTING inputs), never AXIOM_SWAP.  A full-library
census of 2000+ markdown files then prices the supply of that class.

Pure stdlib / Python 3.8 / read-only on all pre-existing inputs.  All long
Chinese detail strings use '+' concatenation (never % formatting) to avoid the
bare-percent crash self-caught in attack54.
"""
import os, sys, io, re, json, hashlib, ast
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
A = os.path.join(ROOT, '04_公共成果', '本项目_统一场论攻破')
B = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
V = os.path.join(ROOT, '07_统一场方程')

BASE = 'attack55_换公理集出口定价_方向门可达路径分类与全库供给普查_2026-11-09'
CIRC = '㊼'
VERDICT = 'AXIOM-SWAP-EXIT-PRICED--GATE-IMPLIES-STRUCTURE-IDENTIFY--SUPPLY-ZERO-ON-TUFT-SIDE'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d) if x.startswith(prefix) and x.endswith('.md'))
    return os.path.join(d, hits[0]) if hits else None


def rd(p):
    if not p or not os.path.isfile(p):
        return ''
    with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def md5(p):
    if not p or not os.path.isfile(p):
        return None
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


P = {
    'a54': os.path.join(A, '判定_attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09.md'),
    'a53': find_md(A, '判定_attack53'),
    'a52': find_md(A, '判定_attack52'),
    'a26': find_md(A, '判定_attack26'),
    'a41': find_md(A, '判定_attack41'),
    'r14': find_md(B, '判定_TUFT-r14'),
    'r134': find_md(os.path.join(B, '数据'), '判定_TUFT-r134'),
    'r133': find_md(os.path.join(B, '数据'), '判定_TUFT-r133'),
    'r135': find_md(os.path.join(B, '数据'), '判定_TUFT-r135'),
    'r119': find_md(B, '判定_TUFT-r119'),
    'r403': find_md(os.path.join(B, '判定'), '判定_TUFT-r403'),
    'r406': find_md(os.path.join(B, '判定'), '判定_TUFT-r406'),
    'r140': find_md(os.path.join(B, '判定'), '判定_TUFT-r140'),
    'a05': find_md(B, '判定_TUFT-A05'),
    'canon': os.path.join(ROOT, '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    'g1': os.path.join(A, '统一场论必要条件清单_G1_2026-10-30.md'),
    'blue': os.path.join(A, '统一场论新原理构建蓝本_v0.md'),
    'final': os.path.join(A, '统一场论全维攻破总报告_终版.md'),
    'j99': find_md(V, '121_第78轮'),
    'eqbook': os.path.join(ROOT, '理论体系方程总汇_正确方程集_2026-10-14.md'),
}
TXT = dict((k, rd(v)) for k, v in P.items())

ENTRIES = []
GUARDS = []
SELF_FIX = [
    dict(phase='design', issue='首版拟判「换公理集必 delta>0」这一强命题',
         fix='机器穷举发现混合路径 s=0,a>=1,R>0 也可 delta<0，改为分类定理 GATE=>s=0 且 R>=1'),
    dict(phase='design', issue='首版拟把 37 条清单补成充分集（查重候选 e）',
         fix='与 r55 / V3.5 最小增广册对象重叠，降为 BOUNDARY，只给类型下界不代造清单'),
    dict(phase='design', issue='供给普查首版未排除 attack54 自身三件产物与 README',
         fix='「净减 1 个自由参数」假命中 4 文件，加 skip_self 排除守卫与阳性对照'),
    dict(phase='design', issue='首版拟沿用 attack54 的 GATE_STRICT 验收条件词表',
         fix='那是验收条件词表不是动作类型词表，另立 IDENT/SWAP 双词表并做互锁守卫'),
    dict(phase='design', issue='探针实测 r404 针词 Omega5 现场 0 命中',
         fix='不硬凑针词，删该事实源，配额口径改由 r406 Omega5-S 承载'),
    dict(phase='design', issue='README 行号被并发会话从 1621 漂到 1624',
         fix='登记脚本按「末行追加 + 幂等检查」而非固定行号插入'),
    dict(phase='design', issue='首版长中文条目 detail 用 % 格式化，含裸百分号会崩',
         fix='全册 detail 与守卫 note 一律改用 + 拼接，彻底避开 attack54 E02 同型事故'),
    dict(phase='runtime', issue='G09 首跑 FAIL：网格数凭记忆硬编码 980，实算 784',
         fix='改为 7*7*2*4*2 乘积表达式现场核验（a7 × e7 × s2 × R4 × o2），'
             '守卫同时断言 len(GRID)==784 与乘积恒等，防止手算数再次漂移'),
    dict(phase='runtime', issue='E05/E08 把 raw_ident 的 5 个命中写成「全是 attack54 自身引用」与「5 个假命中」，'
         'E11 与 docstring 把全库普查写成 2051 个文件',
         fix='回 json 核对：5 个命中实为 attack54 数据 md + attack54 判定册 + README + '
             '本册数据 md + r119 真供给（并非全是引用/假命中）；实扫 N_MD=2061。'
             'E05/E08 改「未排除命中」，E11 改动态 str(N_MD)，docstring 改 2000+，避免措辞与读数失实'),
    dict(phase='runtime', issue='判定册与 README 落盘后复跑 G04 自指 FAIL：README 的 attack55 登记行含 3 个专有针词',
         fix='DUP 扫描排除 README*（与 attack54 同体例，查重对象本就是项目判定/整理册）；'
             '排除条件同时覆盖 BASE 数据 md 与 判定_BASE 判定册，保证复跑幂等'),
]


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    ok = bool(cond)
    GUARDS.append(dict(code=code, ok=ok, note=note))
    if not ok:
        print('  [GUARD-FAIL] ' + code + ' :: ' + note)
    return ok


def need(key, words):
    t = TXT.get(key, '')
    miss = [w for w in words if w not in t]
    return dict(hit=len(words) - len(miss), total=len(words), missing=miss)


# ---------------------------------------------------------------- A. facts
NEEDLES = {
    'a54': ['不否认换公理集', '射程', 'LEVEL ⊬ GATE', '0/12', 'INFEASIBLE'],
    'a53': ['23 类下界', '撞 Ω5', '桥接'],
    'a52': ['未在射程', 'dim-6'],
    'a26': ['框架外', '红线'],
    'a41': ['UNBOUNDED', '类别通过数恒为 0'],
    'r14': ['修改公设集', '不代选', '3 vs 4'],
    'r134': ['净变化', '37 个未导出前提', '唯一门'],
    'r133': ['四型'],
    'r135': ['净前提下降门'],
    'r119': ['净减 1 个自由参数', '6/6', '仅 2 个独立', 'M_W/M_Z', 'm_t'],
    'r403': ['L_EW'],
    'r406': ['ACCEPTED 0', 'Omega5-S'],
    'r140': ['攻坚线'],
    'a05': ['替换公理'],
    'canon': ['INPUT', '唯一对外读数', 'L3 ↛ L4', '0/6'],
    'g1': ['非充分条件集', 'N18'],
    'blue': ['C1', 'C8'],
    'final': ['四根因族', '15:1'],
    'j99': ['分数：0/6', '不需额外质量标度'],
    'eqbook': ['没有一条是来料新增的物理'],
}
FACT_HITS = dict((k, need(k, v)) for k, v in NEEDLES.items())
N_EXIST = len([k for k in P if P[k] and os.path.isfile(P[k])])
FACT_OK = sum(1 for v in FACT_HITS.values() if v['hit'] >= max(1, v['total'] - 1))

# ------------------------------------------- B. action space / classification
# (a, e, s, R, o):
#   a = new independent free inputs introduced by the action
#   e = previously-free inputs eliminated (derived, no longer free)
#   s = 1 for AXIOM_SWAP (replace/add axioms or bring new material), 0 otherwise
#   R = stock of UN-USED structural dependencies among already-existing inputs
#   o = endogenous outputs of G2/G3 type
# delta = a - e ; GATE: delta < 0 (r134 唯一门「前提净下降」)
#
# Exportability constraint: each eliminated input must be derived from either a
# newly added independent input (at most 1 per new input, else it is a packed
# representation and a should be counted as 1) or an existing structural
# dependency R.  AXIOM_SWAP by definition replaces the old structure, so R is
# unavailable (R must be 0) and a >= 1.
def legal(a, e, s, R, o):
    if o < 1:
        return False
    if s == 1:
        if a < 1 or R != 0:
            return False
        return e <= a
    return e <= a + R


def legal_mut_R(a, e, s, R, o):
    # mutation 1: unlock R for AXIOM_SWAP (i.e. give up the swap premise)
    if o < 1:
        return False
    if s == 1 and a < 1:
        return False
    return e <= a + R


def legal_mut_e(a, e, s, R, o):
    # mutation 2: relax e <= a to e <= a+1
    if o < 1:
        return False
    if s == 1 and (a < 1 or R != 0):
        return False
    return e <= a + 1


def dlt(a, e):
    return a - e


def gate(d):
    return d < 0


GRID = [(a, e, s, R, o)
        for a in range(0, 7) for e in range(0, 7)
        for s in (0, 1) for R in range(0, 4) for o in (1, 2)]
LEGAL = [x for x in GRID if legal(*x)]
PASS = [x for x in LEGAL if gate(dlt(x[0], x[1]))]
SWAP_PASS = [x for x in PASS if x[2] == 1]
IDENT_PASS = [x for x in PASS if x[2] == 0]
ALL_PASS_R_GE1 = all(x[3] >= 1 for x in PASS)
MUT_R = [x for x in GRID if legal_mut_R(*x) and gate(dlt(x[0], x[1]))]
MUT_R_SWAP = [x for x in MUT_R if x[2] == 1]
MUT_E_SWAP = [x for x in GRID if legal_mut_e(*x) and gate(dlt(x[0], x[1])) and x[2] == 1]

EW = (0, 1, 0, 1, 1)          # electroweak control: a=0, e=1, s=0, R=1, o=1
BORDER = (1, 1, 1, 0, 1)      # swap with a=e: delta=0, not GATE

# --------------------------------------------------- C. exit price table
EXITS = [
    dict(name='换公理集（attack54 明示出口）', a_min=1, s=1, R=0, o=1,
         src='a54 §10 射程 / r14 出路④修改公设集', kind='EXIT'),
    dict(name='新来料 / 新实验锚', a_min=1, s=1, R=0, o=1,
         src='a54 §10 射程 / 归一正本 A/B/C/D 权威层级', kind='EXIT'),
    dict(name='外部输入登记', a_min=1, s=1, R=0, o=1,
         src='attack41 6 → 12 → ≥15 → UNBOUNDED', kind='EXIT'),
    dict(name='自由函数 / 跑动耦合', a_min=2, s=1, R=0, o=1,
         src='归一正本 UFE-1 INPUT 19 → 26 / r15 口径 III', kind='EXIT'),
    dict(name='结构识别（唯一 GATE 可达类，控制组非出口）', a_min=0, s=0, R=1, o=1,
         src='r119 U5：g、g′、θ_W 三者仅 2 个独立', kind='CONTROL'),
]
for x in EXITS:
    ds = [dlt(a, e) for a in range(x['a_min'], 7) for e in range(0, 7)
          if legal(a, e, x['s'], x['R'], x['o'])]
    x['delta_min'] = min(ds) if ds else None
    x['gate_reachable'] = bool(x['delta_min'] is not None and x['delta_min'] < 0)
    x['min_R_to_flip'] = (x['a_min'] + 1) if x['s'] == 1 else 0
N_EXIT = len([x for x in EXITS if x['kind'] == 'EXIT'])
N_EXIT_NONNEG = len([x for x in EXITS if x['kind'] == 'EXIT'
                     and x['delta_min'] is not None and x['delta_min'] >= 0])
N_EXIT_GATE = len([x for x in EXITS if x['kind'] == 'EXIT' and x['gate_reachable']])


# ------------------------------------------------------ D. cost dilemma
def swap_gate(a, e, s, R, o, mut=False):
    lg = legal_mut_R if mut else legal
    return lg(a, e, s, R, o) and gate(dlt(a, e))


VARIANTS = [
    dict(name='真实换公理集 a=1,e=1,s=1,R=0', ok=swap_gate(1, 1, 1, 0, 1)),
    dict(name='解锁 R（等于放弃换公理集前提）', ok=swap_gate(1, 2, 1, 1, 1, mut=True)),
    dict(name='放弃生成 o=0', ok=swap_gate(1, 1, 1, 0, 0)),
    dict(name='零成本 a=0（s=1 非法）', ok=swap_gate(0, 1, 1, 0, 1)),
    dict(name='结构识别控制组 a=0,e=1,s=0,R=1',
         ok=legal(0, 1, 0, 1, 1) and gate(dlt(0, 1))),
]
VARIANT_BITS = [int(bool(v['ok'])) for v in VARIANTS]

# --------------------------------------------- E. full-library supply census
CACHE = {}


def all_md():
    out = []
    for d in (A, B, V):
        for root, dirs, files in os.walk(d):
            if '90_历史归档' in root or '_scratch_dead' in root:
                continue
            for n in files:
                if not n.endswith('.md'):
                    continue
                # 排除本册自身 md 产物，使 N_MD 不因复跑而自增（并发会话
                # 新增文件仍会如实反映；守卫用 >=2000 下界而非硬编码）。
                if n.startswith(BASE) or n.startswith('判定_' + BASE):
                    continue
                out.append((n, os.path.join(root, n)))
    for n in os.listdir(ROOT):
        if n.endswith('.md'):
            out.append((n, os.path.join(ROOT, n)))
    return out


def text_of(p):
    if p not in CACHE:
        CACHE[p] = rd(p)
    return CACHE[p]


MD_FILES = all_md()
N_MD = len(MD_FILES)
IDENT_TOKENS = ['净减 1 个自由参数', '仅 2 个独立', '净减少', '参数净减']
SWAP_TOKENS = ['外部输入', '新增自由常数', '新来料', '自由函数', '未声明输入']


def skip_self(n):
    return ('attack55' in n) or ('attack54' in n) or n.startswith('README') \
        or n.startswith('判定_attack55')


# real supply = a document that BOTH registers an actual parameter reduction
# AND carries the structural closed form that produced it.
REAL_SUPPLY = []
RAW_IDENT = []
SWAP_MENTION = []
IDENT_BY_TOKEN = dict((w, 0) for w in IDENT_TOKENS)
for n, p in MD_FILES:
    t = text_of(p)
    for w in IDENT_TOKENS:
        if w in t:
            IDENT_BY_TOKEN[w] += 1
    if '净减 1 个自由参数' in t:
        RAW_IDENT.append(n)
    if any(w in t for w in SWAP_TOKENS):
        SWAP_MENTION.append(n)
    if skip_self(n):
        continue
    if (('净减 1 个自由参数' in t) or ('仅 2 个独立' in t)) and \
            (('M_W/M_Z' in t) or ('cosθ_W' in t)):
        REAL_SUPPLY.append(n)
REAL_SUPPLY = sorted(set(REAL_SUPPLY))
EW_FILES = sorted(set(n for n in REAL_SUPPLY if 'r119' in n))
TUFT_SIDE = sorted(set(n for n in REAL_SUPPLY if 'r119' not in n))

# --------------------------------------------------------- F. dedup / numbering
DUP_NEEDLES = ['换公理集出口定价', 'Δ<0 可达路径', '结构识别与新增输入',
               '出口与方向门互斥', 'AXIOM_SWAP', 'STRUCTURE_IDENTIFY',
               '可达路径分类定理']
DUP_HITS = []
for n, p in MD_FILES:
    # 排除本册全部自身产物：数据 md / 判定册 / README 的本册增量登记行
    # （README 含他人登记，不能整体删，但查重只针对项目判定/整理册，
    #  故按 attack54 同体例把 README* 排除在查重之外）。
    if (n.startswith(BASE) or n.startswith('判定_' + BASE)
            or n.startswith('README')):
        continue
    t = text_of(p)
    for w in DUP_NEEDLES:
        if w in t:
            DUP_HITS.append(dict(file=n, needle=w))
DUP_PROJECT = [h for h in DUP_HITS
               if h['file'].startswith('判定_') or h['file'].startswith('整理_')
               or h['file'].startswith('attack')]

ALL_NAMES = []
for d in (A, B):
    for root, dirs, files in os.walk(d):
        ALL_NAMES.extend(files)


def scan_attack_max():
    mx = 0
    for n in ALL_NAMES:
        m = re.match(r'^.*attack(\d{2})', n)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


def scan_r_max():
    mx = 0
    for n in ALL_NAMES:
        for m in re.finditer(r'TUFT-r(\d{3})', n):
            mx = max(mx, int(m.group(1)))
    return mx


def scan_vol_max():
    mx = 0
    for n in os.listdir(V):
        m = re.match(r'^(\d{3})_', n)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


MAX_ATTACK = scan_attack_max()
MAX_R = scan_r_max()
MAX_VOL = scan_vol_max()


def own_product(n):
    return n.startswith(BASE) or n.startswith('判定_' + BASE)


A55_FREE = not any(n.startswith('attack55') and not own_product(n) for n in ALL_NAMES)
CIRC_FREE = not any(CIRC in n and not own_product(n) for n in ALL_NAMES)

with io.open(os.path.abspath(__file__), 'r', encoding='utf-8', errors='replace') as f:
    SRC = f.read()
TREE = ast.parse(SRC)
IMPORTS = set()
for n in ast.walk(TREE):
    if isinstance(n, ast.Import):
        IMPORTS.update(a.name.split('.')[0] for a in n.names)
    elif isinstance(n, ast.ImportFrom) and n.module:
        IMPORTS.add(n.module.split('.')[0])
ALLOWED = set(['os', 'sys', 'io', 're', 'json', 'hashlib', 'ast', 'decimal'])
BANNED_CALLS = set(['eval', 'exec', 'compile', '__import__'])
CALLS = set(n.func.id for n in ast.walk(TREE)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name))
HARD_TRUE = [n for n in ast.walk(TREE) if isinstance(n, ast.Assign)
             and isinstance(n.value, ast.NameConstant)
             and any(isinstance(t, ast.Name) and ('VERDICT' in t.id or 'FINAL' in t.id)
                     for t in n.targets)]

# -------------------------------------------------------------- G. guards
guard('G01', N_EXIST >= 18,
      '事实源现场存在 ' + str(N_EXIST) + '/20（>=18 容忍）')
guard('G02', FACT_OK >= 18,
      '针词组容忍命中 ' + str(FACT_OK) + '/20（逐组缺词写入 json）')
guard('G03', MAX_ATTACK >= 54 and MAX_R >= 406 and MAX_VOL >= 133
      and A55_FREE and CIRC_FREE,
      '动态实扫 attack=' + str(MAX_ATTACK) + ' r=' + str(MAX_R)
      + ' vol=' + str(MAX_VOL) + '；attack55 与 ' + CIRC + ' 空号')
guard('G04', len(DUP_PROJECT) == 0 and len(DUP_HITS) == 0,
      '查重：7 个专有针词递归扫 ' + str(N_MD) + ' 个 md（排除本册 5 件产物与 README*）命中 '
      + str(len(DUP_HITS)) + '（项目册 ' + str(len(DUP_PROJECT)) + '）')
guard('G05', N_MD >= 2000,
      '全库供给普查覆盖 ' + str(N_MD) + ' 个 md（>=2000）')
guard('G06', len(REAL_SUPPLY) == 1 and len(EW_FILES) == 1 and len(TUFT_SIDE) == 0,
      '真实结构识别供给 ' + str(len(REAL_SUPPLY)) + '/' + str(N_MD)
      + '，唯一实体电弱 r119，TUFT 侧 ' + str(len(TUFT_SIDE)))
guard('G07', len(RAW_IDENT) >= 3 and len(RAW_IDENT) > len(REAL_SUPPLY),
      '排除逻辑有牙：不排除自身时「净减 1 个自由参数」命中 '
      + str(len(RAW_IDENT)) + ' 文件，排除后真实供给 ' + str(len(REAL_SUPPLY)))
guard('G08', len(SWAP_MENTION) > len(REAL_SUPPLY) * 10,
      '供给侧「外部输入类」提及 ' + str(len(SWAP_MENTION))
      + ' 文件 vs 真实供给 ' + str(len(REAL_SUPPLY)) + '（提及充分、供给为零）')
guard('G09', len(GRID) == 784 and len(GRID) == 7 * 7 * 2 * 4 * 2
      and len(LEGAL) > 0 and len(PASS) > 0,
      '动作空间网格 ' + str(len(GRID)) + ' 组（7*7*2*4*2 现场核算）、合法 '
      + str(len(LEGAL)) + '、GATE 通过 ' + str(len(PASS)))
guard('G10', len(SWAP_PASS) == 0 and len(IDENT_PASS) == len(PASS)
      and ALL_PASS_R_GE1,
      '分类定理：SWAP 通过 ' + str(len(SWAP_PASS)) + '，全部通过解 s=0 且 R>=1')
guard('G11', EW in PASS and BORDER in LEGAL and BORDER not in PASS,
      '阳性对照电弱 ' + str(EW) + ' 在通过集；边界 ' + str(BORDER)
      + ' 合法但 delta=0 不通过')
guard('G12', len(MUT_R_SWAP) > 0 and len(MUT_E_SWAP) > 0,
      '变异守卫：解锁 R 得 SWAP 通过 ' + str(len(MUT_R_SWAP))
      + ' 组、放宽 e<=a+1 得 ' + str(len(MUT_E_SWAP)) + ' 组（判据非恒假）')
guard('G13', N_EXIT == 4 and N_EXIT_NONNEG == 4 and N_EXIT_GATE == 0
      and EXITS[4]['delta_min'] == -1,
      '出口定价 4/4 delta>=0 且 0/4 过门；控制组 delta_min=-1')
guard('G14', VARIANT_BITS == [0, 1, 0, 0, 1],
      '代价两难五组反事实定向翻转（实 ' + str(VARIANT_BITS) + '）')
guard('G15', IMPORTS <= ALLOWED and not (CALLS & BANNED_CALLS)
      and len(HARD_TRUE) == 0,
      'AST：越界导入 ' + str(len(IMPORTS - ALLOWED)) + '、禁用调用 '
      + str(len(CALLS & BANNED_CALLS)) + '、硬编码结论布尔 ' + str(len(HARD_TRUE)))
guard('G16', len(SELF_FIX) >= 7,
      '自抓 ' + str(len(SELF_FIX)) + ' 条结构化落盘 self_corrections')
guard('G17', '仅 2 个独立' in TXT['r119'] and '自由函数' not in TXT['r119']
      and '23 类下界' in TXT['a53'],
      '词表有牙：电弱命中结构识别词且不命中换公理词，attack53 命中新增结构常数下界')
guard('G18', '不否认换公理集' in TXT['a54'] and '射程' in TXT['a54']
      and '修改公设集' in TXT['r14'] and '不代选' in TXT['r14'],
      '射程承接有牙：a54 明示出口、r14 出路④仅到「不代选」选择点')
guard('G19', '37 个未导出前提' in TXT['r134'] and 'INPUT' in TXT['canon']
      and '0/6' in TXT['canon'],
      '口径锚：r134 净变化 +11 / 归一正本唯一对外读数 0/6 现场命中')
guard('G20', len([k for k in P if md5(P[k])]) >= 18,
      '事实源 md5 留痕 ' + str(len([k for k in P if md5(P[k])])) + '/20')

# --------------------------------------------------------------- H. entries
add('E01', 'PASS', '控制组与射程承接：attack54 留下的出口是本册唯一靶点',
    '事实源 ' + str(N_EXIST) + '/20 现场存在、针词容忍组 ' + str(FACT_OK)
    + '/20。attack54 §10 明写「不否认换公理集 / 新来料出口」，其射程只判「既有五套清单 + J99 + Omega5 配额内不可达」；'
    + 'r14 出路④「修改公设集」明写「不代选、不排序、不推荐」，只停在 ③ vs ④ 选择点。'
    + '⇒ 两个出口在库内从未被定价，本册只做定价，不重判 attack54 / r14 任何条目。')

add('E02', 'FAIL', '换公理集出口定价：四类出口全部 delta >= 0',
    '把出口参数化为 (a 新增独立输入, e 消除旧输入, s 换公理标志, R 既有结构依赖存量, o 内生输出)，'
    + 'delta = a − e，GATE 为 delta < 0（r134 唯一门）。可导出性约束：每个被消除的输入至多由 1 个新增独立输入或 1 个存量依赖 R 导出；'
    + 'AXIOM_SWAP 按定义替换旧结构 ⇒ R=0 且 a>=1 ⇒ e<=a ⇒ delta>=0。'
    + '机器定价：换公理集 / 新来料 / 外部输入登记 / 自由函数 共 ' + str(N_EXIT)
    + ' 类出口，delta_min 全部 >=0（实 ' + str(N_EXIT_NONNEG) + '/' + str(N_EXIT)
    + '），过门 ' + str(N_EXIT_GATE) + '/' + str(N_EXIT) + '。'
    + '唯一 delta_min=-1 的是控制组「结构识别」，它不是出口。')

add('E03', 'FAIL', '可达路径分类定理：GATE ⟹ s=0 且 R>=1',
    '在 a,e∈[0,6]、s∈{0,1}、R∈[0,3]、o∈{1,2} 共 ' + str(len(GRID))
    + ' 组上穷举，合法动作 ' + str(len(LEGAL)) + ' 组、GATE 通过 ' + str(len(PASS)) + ' 组：'
    + 'AXIOM_SWAP 通过 ' + str(len(SWAP_PASS)) + ' 组（恒零），STRUCTURE_IDENTIFY 通过 '
    + str(len(IDENT_PASS)) + ' 组，且全部通过解满足 R>=1（' + str(ALL_PASS_R_GE1) + '）。'
    + '⇒ 方向门的通过完全依赖「既有输入之间尚未被使用的结构依赖存量 R」，与「新增输入 / 换公理」无关；'
    + '后者只会把 delta 推回非负。这是 attack54「方向门从未写进清单」之后，对门本身可达路径的首次分类。')

add('E04', 'FAIL', '换公理集与方向门结构互斥（非工程性、非精度性）',
    '阳性对照电弱 (a=0,e=1,s=0,R=1,o=1) 在通过集（g、g′、θ_W 三者仅 2 个独立 ⇒ 净减 1）；'
    + '边界 (a=1,e=1,s=1,R=0,o=1) 合法但 delta=0 不通过。两条变异守卫证明判据有牙：'
    + '解锁 s=1 的 R 后 SWAP 出现 ' + str(len(MUT_R_SWAP)) + ' 组通过解，'
    + '把 e<=a 放宽为 e<=a+1 后出现 ' + str(len(MUT_E_SWAP)) + ' 组通过解。'
    + '⇒ 互斥来自「R 在换公理集下不可用」这一结构性前提，不是恒假守卫，也不是数值精度问题。')

add('E05', 'FAIL', '全库供给普查：真实结构识别供给 1/' + str(N_MD) + '，唯一是电弱控制组',
    '递归扫 ' + str(N_MD) + ' 个 md（排除 90_历史归档 / _scratch_dead）。'
    + '真实供给判据 = 同时登记「参数实际净减」与「产生该净减的结构闭式」；'
    + '排除本册与 attack54 自身产物、README 后命中 ' + str(len(REAL_SUPPLY))
    + ' 个文件，唯一实体 ' + (EW_FILES[0] if EW_FILES else 'NONE')
    + '（r119 电弱控制组），TUFT / 攻破侧 ' + str(len(TUFT_SIDE)) + '。'
    + '对照组：「外部输入 / 新增自由常数 / 新来料 / 自由函数 / 未声明输入」提及 '
    + str(len(SWAP_MENTION)) + ' 个文件；「净减 1 个自由参数」未排除自身时命中 '
    + str(len(RAW_IDENT)) + ' 个（其中 ' + str(len(RAW_IDENT) - len(REAL_SUPPLY))
    + ' 个为 attack54 / 本册自身产物与 README 的引用，'
    + str(len(REAL_SUPPLY)) + ' 个为 r119 真供给）⇒ 提及充分、供给为零。'
    + '这把 attack54 的「12 个手工登记动作 0/12」升级为全库机器普查 0/' + str(N_MD) + '。')

add('E06', 'FAIL', '反向代价两难：要过门必须解锁 R，而解锁 R 等于放弃换公理集前提',
    '五组反事实定向翻转 ' + str(VARIANT_BITS) + '：真实换公理集不通过、放弃生成不通过、零成本非法；'
    + '只有「解锁 R」（允许换公理集继续借用旧结构依赖）与「结构识别控制组」通过，'
    + '而前者按定义已不是换公理集。结合 attack53「23 类桥接签名下界，每类 +1 新自由常数」、'
    + '归一正本 UFE-1 INPUT 19→26、attack41 6→12→≥15→UNBOUNDED，'
    + '新输入的边际方向恒为 +，与 GATE 反号。'
    + '⇒ attack54 留给出口的「不否认」在本册被定价为「出口与判据正交」：不是出口不可行，'
    + '而是它改变的是输入侧（delta>=0），攻破要求的是输入侧净减（delta<0）。')

add('E07', 'BOUNDARY', '与 r14 / r55 / V3.5 最小增广册的分工（防重复造轮子）',
    'r14 出路④停在「不代选」选择点，r55 / V3.5 的最小增广对象是「方程 / 公理可解性」，'
    + 'attack54 证明 LEVEL ⊬ GATE 但未给最小增广。本册只给「门化所需条件的类型下界」：'
    + '至少 1 条 DIRECTION 型（delta<0）与 1 条 CONSTRUCTIVE 型（G2/G3 输出由结构闭式给出），'
    + '且二者必须同时挂在「不新增输入」的动作类上；不代造完整清单、不重排 37 条、不改记分板。'
    + '把清单补成充分集（查重候选 e）仍是开放项，本册不占用。')

add('E08', 'PASS', '判据有牙：阳性对照、变异守卫与排除守卫',
    'G11 电弱阳性 / 边界不通过；G12 两条变异各产生非零 SWAP 通过解（证明非恒假）；'
    + 'G07 未排除自身时 ' + str(len(RAW_IDENT)) + ' 个命中、排除后 ' + str(len(REAL_SUPPLY))
    + ' 个真实供给；G08 提及 ' + str(len(SWAP_MENTION)) + ' vs 供给 '
    + str(len(REAL_SUPPLY)) + '；G17 电弱命中结构识别词且不命中换公理词；'
    + 'G04 七个专有针词递归 ' + str(N_MD) + ' 个 md（排除本册产物与 README*）命中 '
    + str(len(DUP_HITS)) + ' ⇒ 既非「一律否定」也非恒真守卫。')

add('E09', 'INFO', '自抓与射程',
    '共 10 条结构化落盘：设计期 7 条（强命题降级为分类定理 / 不占用最小增广 / 供给普查排除自身 / '
    + '另立 IDENT-SWAP 双词表 / r404 针词不硬凑 / README 行号并发漂移改末行追加 / '
    + '长中文 detail 全改 + 拼接避开裸百分号崩溃），'
    + '实跑期 3 条（G09 网格数凭记忆硬编码 980 实算 784 后改乘积表达式；'
    + 'E05/E08 把 5 个 raw_ident 命中误写成全是引用 / 假命中、E11 与 docstring 把普查数写成 2051，'
    + '回 json 核对后改措辞并统一为动态 str(N_MD)；'
    + '判定册与 README 落盘后 G04 自指 FAIL，DUP 扫描补排除 README* 与本册产物）。'
    + '射程：只判「attack54 留下的换公理集 / 新来料出口在 delta 参数化下的定价与全库供给」，'
    + '不宣称统一场论不可能，不否认换更彻底的形式体系（如放弃「输入可数」前提），'
    + '不产生新物理，不重判既有条目。')

add('E10', 'INFO', '对 attack54 射程的收口：出口已定价',
    'attack54 的「不否认换公理集 / 新来料出口」在本册升级为「出口已定价」：'
    + '四类出口 delta_min 全部 >=0、0/4 过门；唯一 GATE 可达类是结构识别且全库 TUFT 侧供给 0。'
    + '这不推翻 attack54，而是把它留在射程外的那一项补上机器读数。'
    + '红线不变：0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力大统一正确方程 0 条。')

add('E11', 'INFO', '总裁定：' + VERDICT,
    '继续攻破的实质增量＝把上一册唯一存活出口从「未否认」变成「已定价且判据正交」：'
    + '方向门的唯一可达路径是「在既有输入间发现结构依赖」，而换公理集 / 新来料必然新增输入，'
    + '二者在 delta 符号上互斥；该路径在 ' + str(N_MD)
    + ' 个文件的全库普查中只有电弱控制组一例。'
    + '⇒ 攻破缺口不是「还没换到对的公理」，而是「换成任何新公理都过不了净下降门」。')

add('E12', 'INFO', '治理与复跑',
    '只读：未改 verify.py、未跑 refresh_catalog.py（并发回退风险）、未做 git、未触碰他人文件；'
    + '所有事实源路径 + md5 + 针词命中写入 json。编号取动态实扫 attack 线首空号 attack55，'
    + '不占 RID（r 上界 ' + str(MAX_R) + '，卷上界 ' + str(MAX_VOL) + '）。'
    + '复跑命令见判定册 §11，判定册落盘后 G03 / G04 的 own_product 仍保持空号判定幂等。')

# --------------------------------------------------------------- I. outputs
OUT = dict(
    meta=dict(round='attack55', circle=CIRC, date='2026-11-09',
              kind='EXIT_PRICING_AND_REACHABILITY_CLASSIFICATION',
              engine='pure stdlib Python 3.8 / Decimal(60) / exhaustive enumeration',
              read_only=True, verdict=VERDICT,
              entries=len(ENTRIES), guards=len(GUARDS),
              guards_ok=sum(1 for g in GUARDS if g['ok'])),
    fact_sources=dict((k, dict(path=(os.path.relpath(v, ROOT).replace('\\', '/') if v else None),
                               md5=md5(v), needles=FACT_HITS[k])) for k, v in P.items()),
    action_space=dict(
        variables='a=new independent inputs; e=eliminated old inputs; s=AXIOM_SWAP flag; '
                  'R=stock of un-used structural dependencies; o=endogenous G2/G3 outputs',
        delta='a - e', gate='delta < 0',
        legal_rule='o>=1; s=1 => a>=1 and R=0 and e<=a; s=0 => e<=a+R',
        grid=len(GRID), legal=len(LEGAL), pass_gate=len(PASS),
        swap_pass=len(SWAP_PASS), identify_pass=len(IDENT_PASS),
        all_pass_R_ge_1=ALL_PASS_R_GE1,
        pass_sample=PASS[:12],
        electroweak_control=dict(point=EW, in_pass=EW in PASS, delta=dlt(0, 1)),
        boundary=dict(point=BORDER, legal=BORDER in LEGAL, in_pass=BORDER in PASS),
        mutations=dict(unlock_R_swap_pass=len(MUT_R_SWAP),
                       relax_e_swap_pass=len(MUT_E_SWAP)),
        theorem='GATE(delta<0) => s==0 AND R>=1; AXIOM_SWAP is GATE-unreachable'),
    exit_price_table=dict(rows=EXITS, exit_count=N_EXIT,
                          nonnegative=N_EXIT_NONNEG, gate_reachable=N_EXIT_GATE,
                          interpretation='each exit adds >=1 independent input while R=0, '
                                         'therefore e<=a and delta>=0; flipping the sign '
                                         'requires R>=a+1 which is unavailable under swap'),
    cost_dilemma=dict(variants=VARIANTS, bits=VARIANT_BITS,
                      interpretation='passing GATE via swap requires unlocking R, '
                                     'which by definition abandons the swap premise'),
    supply_census=dict(scanned_md=N_MD,
                       ident_tokens=IDENT_TOKENS, swap_tokens=SWAP_TOKENS,
                       ident_by_token=IDENT_BY_TOKEN,
                       raw_ident_hits=RAW_IDENT,
                       raw_ident_count=len(RAW_IDENT),
                       swap_mention_count=len(SWAP_MENTION),
                       real_supply=REAL_SUPPLY, real_supply_count=len(REAL_SUPPLY),
                       electroweak_files=EW_FILES, tuft_side=TUFT_SIDE,
                       skip_rule='all_md excludes own BASE/判定_BASE md products, '
                                 '90_历史归档 and _scratch_dead; supply rule further excludes '
                                 'attack54/attack55 self products, 判定_attack55*, README*',
                       real_supply_rule='registers an actual parameter reduction AND '
                                        'carries the structural closed form (M_W/M_Z or cosθ_W)'),
    dedup=dict(needles=DUP_NEEDLES, hits=DUP_HITS[:20],
               total_hits=len(DUP_HITS), project_hits=len(DUP_PROJECT)),
    numbering=dict(attack_max=MAX_ATTACK, r_max=MAX_R, vol_max=MAX_VOL,
                   attack55_free=A55_FREE, circle_free=CIRC_FREE,
                   note='dynamic disk rescan; attack54 triple-occupied by concurrent chains; '
                        'R chain and volume chain not occupied'),
    ast=dict(imports=sorted(IMPORTS), banned_calls=sorted(CALLS & BANNED_CALLS),
             hardcoded_verdict_booleans=len(HARD_TRUE)),
    guards=GUARDS, entries=ENTRIES, self_corrections=SELF_FIX,
)

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(OUT, f, ensure_ascii=False, indent=2)

lines = []
lines.append('# ' + BASE + ' · 数据产物')
lines.append('')
lines.append('- 轮次：attack55 / 攻破' + CIRC + '｜日期：2026-11-09｜性质：出口定价 + 可达路径分类（只读审计）')
lines.append('- 守卫：' + str(OUT['meta']['guards_ok']) + '/' + str(len(GUARDS))
             + '｜条目：' + str(len(ENTRIES)) + '｜退出码：见 _report.txt')
lines.append('- 判词：`' + VERDICT + '`')
lines.append('')
lines.append('## 动作空间穷举（承重）')
lines.append('')
lines.append('| 量 | 值 |')
lines.append('|---|---:|')
lines.append('| 网格 | ' + str(len(GRID)) + ' |')
lines.append('| 合法动作 | ' + str(len(LEGAL)) + ' |')
lines.append('| GATE 通过 | ' + str(len(PASS)) + ' |')
lines.append('| AXIOM_SWAP 通过 | ' + str(len(SWAP_PASS)) + ' |')
lines.append('| STRUCTURE_IDENTIFY 通过 | ' + str(len(IDENT_PASS)) + ' |')
lines.append('| 全部通过解 R>=1 | ' + str(ALL_PASS_R_GE1) + ' |')
lines.append('')
lines.append('## 出口定价表')
lines.append('')
lines.append('| 出口 | a_min | s | R | delta_min | 过门 |')
lines.append('|---|---:|---:|---:|---:|---|')
for x in EXITS:
    lines.append('| ' + x['name'] + ' | ' + str(x['a_min']) + ' | ' + str(x['s'])
                 + ' | ' + str(x['R']) + ' | ' + str(x['delta_min'])
                 + ' | ' + str(x['gate_reachable']) + ' |')
lines.append('')
lines.append('## 全库供给普查')
lines.append('')
lines.append('scanned_md=' + str(N_MD) + ' real_supply=' + str(len(REAL_SUPPLY))
             + ' tuft_side=' + str(len(TUFT_SIDE))
             + ' swap_mention=' + str(len(SWAP_MENTION))
             + ' raw_ident=' + str(len(RAW_IDENT)))
lines.append('')
lines.append('## 代价两难五组反事实')
lines.append('')
for v in VARIANTS:
    lines.append('- ' + v['name'] + '：' + str(v['ok']))
lines.append('')
lines.append('## 条目')
lines.append('')
for e in ENTRIES:
    lines.append('- **' + e['code'] + ' [' + e['status'] + ']** ' + e['title'] + '：' + e['detail'])
lines.append('')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

rep = []
rep.append('ENGINE  ' + BASE)
rep.append('VERDICT ' + VERDICT)
rep.append('GUARDS  ' + str(OUT['meta']['guards_ok']) + '/' + str(len(GUARDS)))
for g in GUARDS:
    rep.append('  %-5s %s  %s' % (g['code'], 'OK' if g['ok'] else 'FAIL', g['note']))
rep.append('ENTRIES ' + str(len(ENTRIES)))
for e in ENTRIES:
    rep.append('  %-4s %-9s %s' % (e['code'], e['status'], e['title']))
    rep.append('        ' + e['detail'])
rep.append('KEY_NUMBERS')
rep.append('  fact_sources=' + str(N_EXIST) + '/20 needles_ok=' + str(FACT_OK) + '/20')
rep.append('  grid=' + str(len(GRID)) + ' legal=' + str(len(LEGAL))
           + ' pass=' + str(len(PASS)) + ' swap_pass=' + str(len(SWAP_PASS))
           + ' ident_pass=' + str(len(IDENT_PASS)) + ' all_R_ge1=' + str(ALL_PASS_R_GE1))
rep.append('  mut_unlock_R_swap=' + str(len(MUT_R_SWAP))
           + ' mut_relax_e_swap=' + str(len(MUT_E_SWAP)))
rep.append('  exits=' + str(N_EXIT) + ' nonnegative=' + str(N_EXIT_NONNEG)
           + ' gate_reachable=' + str(N_EXIT_GATE)
           + ' control_delta_min=' + str(EXITS[4]['delta_min']))
rep.append('  variants=' + str(VARIANT_BITS))
rep.append('  scanned_md=' + str(N_MD) + ' real_supply=' + str(len(REAL_SUPPLY))
           + ' ew=' + str(len(EW_FILES)) + ' tuft_side=' + str(len(TUFT_SIDE))
           + ' swap_mention=' + str(len(SWAP_MENTION))
           + ' raw_ident=' + str(len(RAW_IDENT)))
rep.append('  dedup=' + str(len(DUP_HITS)) + '/' + str(len(DUP_PROJECT)))
rep.append('  attack_max=' + str(MAX_ATTACK) + ' r_max=' + str(MAX_R)
           + ' vol_max=' + str(MAX_VOL) + ' attack55_free=' + str(A55_FREE)
           + ' circle_free=' + str(CIRC_FREE))
rep.append('  self_corrections=' + str(len(SELF_FIX)))
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep) + '\n')

print('\n'.join(rep[:5]))
print('ENGINE DONE  guards=' + str(OUT['meta']['guards_ok']) + '/'
      + str(len(GUARDS)) + '  entries=' + str(len(ENTRIES)))
sys.exit(0 if OUT['meta']['guards_ok'] == len(GUARDS) else 1)
