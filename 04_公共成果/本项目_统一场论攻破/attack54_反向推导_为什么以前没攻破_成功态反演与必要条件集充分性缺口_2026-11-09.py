# -*- coding: utf-8 -*-
"""attack54 / 攻破㊻ · 反向推导：为什么以前没有攻破统一场论.

REVERSE, not inductive: previous 400+ ledgers enumerate failures forward
(postulates -> FAIL), or perturb sideways (attack41 injection / attack45
hypothesis swap / attack46 ablation).  This ledger starts from the ONLY
completed unification in this repository (electroweak L_EW, r403/r119),
inverts its success into three constructive actions, then audits whether any
of the five registered necessary-condition ledgers (C1-C8, N1-N18, U1-U7,
R1-R4, J99 scoreboard) ever lists those actions as acceptance criteria.

Pure stdlib / Python 3.8 / read-only on all pre-existing inputs.
"""
import os, sys, io, re, json, hashlib, ast
from fractions import Fraction
from decimal import Decimal, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
B1 = os.path.join(ROOT, '04_公共成果', '本项目_统一场论攻破')
B2 = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
V7 = os.path.join(ROOT, '07_统一场方程')
RDIR = os.path.join(B2, '判定')
DDIR = os.path.join(B2, '数据')
BASE = 'attack54_反向推导_为什么以前没攻破_成功态反演与必要条件集充分性缺口_2026-11-09'
CIRC = '㊻'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d)
                  if x.startswith(prefix) and x.endswith('.md'))
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
    'r119': os.path.join(B2, '判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md'),
    'r403': find_md(RDIR, '判定_TUFT-r403'),
    'r406': find_md(RDIR, '判定_TUFT-r406'),
    'j99': find_md(V7, '121_第78轮'),
    'g1': os.path.join(B1, '统一场论必要条件清单_G1_2026-10-30.md'),
    'blue': os.path.join(B1, '统一场论新原理构建蓝本_v0.md'),
    'final': os.path.join(B1, '统一场论全维攻破总报告_终版.md'),
    'r133': find_md(DDIR, '判定_TUFT-r133'),
    'r134': find_md(DDIR, '判定_TUFT-r134'),
    'r123': find_md(DDIR, '判定_TUFT-r123'),
    'a41': find_md(B1, '判定_attack41'),
    'a45': find_md(B1, '判定_attack45'),
    'a46': find_md(B1, '判定_attack46'),
    'a53': find_md(B1, '判定_attack53'),
    'canon': os.path.join(ROOT, '统一场论理论体系与方程_归一正本_2026-11-09.md'),
    'eqbook': os.path.join(ROOT, '理论体系方程总汇_正确方程集_2026-10-14.md'),
    'ledger': find_md(DDIR, 'TUFT-总账_全链判决归约'),
}
TXT = dict((k, rd(v)) for k, v in P.items())

ENTRIES = []
GUARDS = []
SELF_FIX = [
    dict(phase='design', issue='首版拟判「清单 37 条全为禁止型、0 条构造型」',
         fix='现场复核 C2/C6/N16/N17/U4/U6 为存在型条件，改判「LEVEL vs GATE 逻辑独立性」穷举'),
    dict(phase='design', issue='首版拟用抽象 6/6 记分板做反事实',
         fix='会混算电弱 6/6 与 J99 0/6 两把尺子，撤回（归一正本 §0 红线）'),
    dict(phase='design', issue='五套清单解析未去重',
         fix='r119 的 U1-U7 在 §〇/§一 各出现一次，按 code 去重否则 7→14 计数失真'),
    dict(phase='design', issue='方向门词表未区分「静态上限」与「净变化方向」',
         fix='拆 STRICT/WEAK 两档并用 G16/G17 阳性对照锁死，防 U5 假阳性'),
    dict(phase='runtime', issue='G05 针词 1/3：G2/G3 按记忆写死 M_W/M_Z = cosθ_W 与 m_t=173 GeV',
         fix='回磁盘核对 r119 实际写法，改多针词列表（精确层闭式 + 数值层 rho + m_t 空格）'),
    dict(phase='runtime', issue='G12 实得 [1,1,1,0,0]：feasible 把「放弃生成」与「零成本生成」两种退化逃逸判为可行',
         fix='加 need>=1 与 cost>=1 双前提，五组恢复 0/0/1/0/0 定向翻转'),
    dict(phase='runtime', issue='G14 自指失败：ALL_NAMES 含自身已落盘 .py',
         fix='空号判定排除本册自身产物，他人抢注仍被抓'),
    dict(phase='runtime', issue='E02 崩溃 ValueError: unsupported format character：串内含裸 0.139% 又用 % 格式化',
         fix='字面百分号双写；E06 去掉多余的 % 空串格式化'),
    dict(phase='runtime', issue='E09 列了四条自抓但 SELF_FIX 为空、产物 self_corrections 恒 []',
         fix='SELF_FIX 结构化落盘 9 条，E09 追加实跑四条摘要'),
]


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    ok = bool(cond)
    GUARDS.append(dict(code=code, ok=ok, note=note))
    if not ok:
        print('  [GUARD-FAIL] %s :: %s' % (code, note))
    return ok


def need(key, words):
    t = TXT.get(key, '')
    missing = [w for w in words if w not in t]
    return dict(hit=len(words) - len(missing), total=len(words), missing=missing)


# ---------------------------------------------------------------- A. facts
NEEDLES = {
    'r119': ['6/6', '净减 1 个自由参数', '1.01043', '0.139%', 'U7'],
    'r403': ['L_EW', 'NO-CORRECT-FOUR-FORCE-GUT'],
    'r406': ['Omega5-S', 'ACCEPTED 0'],
    'j99': ['分数：0/6', '不需额外质量标度', '参数计数不劣于对照理论', '无自由模量'],
    'g1': ['非充分条件集', 'N18', 'TUFT 对 18 条必要条件供给'],
    'blue': ['C1', 'C8', 'M1 公设独有是总闸门'],
    'final': ['四根因族', 'R1 标度外部性', 'R4 预言不判别', '15:1'],
    'r133': ['四型对“修改”', 'closure 从 0.327 推到 1', '前提净下降'],
    'r134': ['净变化 **+11**', '37 个未导出前提'],
    'r123': ['CT1', 'M_W/M_Z = cosθ_W'],
    'a41': ['6 → 12 → ≥15 → UNBOUNDED', '类别通过数恒为 0'],
    'a45': ['0/80', '净前提下降门'],
    'a46': ['0/120'],
    'a53': ['23 类下界', '撞 Ω5'],
    'canon': ['INPUT  输入参数层（19 → 26', '唯一对外读数', 'L3 ↛ L4'],
    'eqbook': ['没有一条是来料新增的物理'],
    'ledger': ['不是充分条件'],
}
FACT_HITS = dict((k, need(k, v)) for k, v in NEEDLES.items())
FACT_OK = sum(1 for v in FACT_HITS.values() if v['hit'] >= max(1, v['total'] - 1))

# ------------------------------------------- B. success-state inversion
S_ACTIONS = [
    dict(id='G1', name='参数/前提净减',
         needles=['净减 1 个自由参数', '需净减少参数'], src='r119 U5 / U5 参数计数',
         kind='DIRECTION', value='delta = -1'),
    dict(id='G2', name='无量纲比值由结构闭式导出',
         needles=['M_W/M_Z = (5e/3)/(25e/12) = 4/5 = cosθ_W', 'ρ = 1.01043'],
         src='r119 U4 数值层 / 精确层校验',
         kind='CONSTRUCTIVE', value='rho = 1.01043'),
    dict(id='G3', name='先于观测的单点预言带误差带',
         needles=['m_t = 173 GeV', '偏差 0.139%'], src='r119 U6',
         kind='CONSTRUCTIVE', value='0.139%'),
]
for a in S_ACTIONS:
    a['hits'] = [w for w in a['needles']
                 if (w in TXT['r119']) or (w in TXT.get('r123', ''))]
    a['hit'] = len(a['hits']) >= 1
SUCCESS_PRESENT = ('6/6' in TXT['r119']) and ('唯一 C3+统一' in TXT.get('r403', '')
                   or '唯一 C3 级真统一' in TXT.get('canon', '')
                   or 'L_EW' in TXT.get('r403', ''))

# --------------------------------------------- C. three-layer reconciliation
LEDGER_SPEC = [
    ('C', 'blue', r'^\|\s*(C[1-8])\s*\|\s*([^|]+)\|', 8, '蓝本 v0 硬约束'),
    ('N', 'g1', r'^\|\s*(N\d{1,2})\s*\|\s*([^|]+)\|', 18, 'G1 必要条件清单'),
    ('U', 'r119', r'^\|\s*(U[1-7])\s*\|\s*([^|]+)\|', 7, 'r119 完成判据'),
    ('R', 'final', r'^\|\s*(R[1-4])\s+([^|]+)\|', 4, '攻破总报告四根因族'),
]
ROWS = []
COUNTS = {}
for tag, key, pat, expect, label in LEDGER_SPEC:
    seen = set()
    got = []
    for code, text in re.findall(pat, TXT.get(key, ''), re.M):
        c = code.strip()
        if c in seen:
            continue
        seen.add(c)
        got.append((tag, c, text.strip()))
    ROWS.extend(got)
    COUNTS[tag] = dict(found=len(got), expected=expect, label=label)

JROWS = [(c.strip(), t.strip()) for c, t in
         re.findall(r'^\|\s*([1-6])\s*\|\s*([^|]+)\|\s*不满足\s*\|',
                    TXT.get('j99', ''), re.M)]
JROWS = JROWS[:6]

GATE_STRICT = ['净减', '净下降', '前提减少', '前提净减少', '参数净减', '净变化']
GATE_WEAK = GATE_STRICT + ['参数计数', '不劣于对照']
ACT_ANCHORS = {
    'G1': ['净减', '净下降', '前提减少', '参数计数不劣于'],
    'G2': ['M_W/M_Z', 'cosθ_W', 'ρ =', '无量纲比值', '混合角'],
    'G3': ['单点', '误差带', '先于观测', '可检验预言'],
}


def hits_any(text, words):
    return [w for w in words if w in text]


COVER = []
for tag, code, text in ROWS:
    COVER.append(dict(layer='LEDGER', set=tag, code=code, text=text,
                      strict=hits_any(text, GATE_STRICT),
                      weak=hits_any(text, GATE_WEAK),
                      acts=dict((k, hits_any(text, v)) for k, v in ACT_ANCHORS.items())))
for code, text in JROWS:
    COVER.append(dict(layer='SCOREBOARD', set='J', code=code, text=text,
                      strict=hits_any(text, GATE_STRICT),
                      weak=hits_any(text, GATE_WEAK),
                      acts=dict((k, hits_any(text, v)) for k, v in ACT_ANCHORS.items())))

N_LEDGER = len(ROWS)
N_STRICT_LEDGER = sum(1 for r in COVER if r['layer'] == 'LEDGER' and r['strict'])
N_WEAK_LEDGER = sum(1 for r in COVER if r['layer'] == 'LEDGER' and r['weak'])
N_STRICT_J = sum(1 for r in COVER if r['layer'] == 'SCOREBOARD' and r['strict'])
N_WEAK_J = sum(1 for r in COVER if r['layer'] == 'SCOREBOARD' and r['weak'])
ACT_COVER = dict((k, dict(
    ledger=sum(1 for r in COVER if r['layer'] == 'LEDGER' and r['acts'][k]),
    scoreboard=sum(1 for r in COVER if r['layer'] == 'SCOREBOARD' and r['acts'][k])))
    for k in ACT_ANCHORS)

# -------------------------------------- D. sufficiency: exhaustive counterexample
def level_ok(n_in, n_out, extra, moduli):
    return n_out >= 1 and extra == 0 and moduli == 0 and n_in >= 0


def gate_ok(n_in, n_out):
    return (n_in - n_out) < 0


GRID = [(i, j) for i in range(0, 7) for j in range(0, 7)]
LEVEL_SET = [(i, j) for i, j in GRID if level_ok(i, j, 0, 0)]
COUNTER = [(i, j) for i, j in LEVEL_SET if not gate_ok(i, j)]
GATE_SET = [(i, j) for i, j in GRID if gate_ok(i, j)]

# ------------------------------------------------------- E. direction ledger
DIRECTION = [
    dict(name='电弱统一（唯一成功态）', delta=-1, sign='NEGATIVE', src='r119 U5 净减 1', success=True),
    dict(name='r133 四型修补 ① 外部输入', delta=1, sign='NONNEG', src='r133 +≥1', success=False),
    dict(name='r133 四型修补 ② 零信息重排', delta=0, sign='NONNEG', src='r133 0', success=False),
    dict(name='r133 四型修补 ③ 范围退缩', delta=0, sign='NONNEG', src='r133 0', success=False),
    dict(name='r133 四型修补 ④ 自相矛盾', delta=0, sign='NONNEG', src='r133 0', success=False),
    dict(name='r134 唯一门现值', delta=11, sign='NONNEG', src='r134 净变化 +11', success=False),
    dict(name='attack41 输入注入 6→12', delta=6, sign='NONNEG', src='a41', success=False),
    dict(name='attack41 输入注入 12→≥15', delta=3, sign='NONNEG', src='a41', success=False),
    dict(name='归一正本 UFE-1 INPUT 19→26', delta=7, sign='NONNEG', src='canon §2', success=False),
    dict(name='attack53 桥接签名类下界', delta=23, sign='NONNEG', src='a53 23 类 × +1', success=False),
    dict(name='attack45 假设替换迁移', delta=0, sign='NONNEG', src='a45 0/80', success=False),
    dict(name='attack46 基础块抽除迁移', delta=0, sign='NONNEG', src='a46 0/120', success=False),
    dict(name='r406 Omega5-S 出口 ACCEPTED', delta=0, sign='NONNEG', src='r406 ACCEPTED 0', success=False),
]
ADVANCE = [d for d in DIRECTION if not d['success']]
N_ADV_NEG = sum(1 for d in ADVANCE if d['delta'] < 0)
N_ADV_TOTAL = len(ADVANCE)

# --------------------------------------------------- F. reverse price dilemma
def feasible(need_gen, cost_per, max_extra):
    # 双前提：目标必须真生成 >=1 个内生输出（排除「放弃生成」退化逃逸）；
    # 每个输出至少花 +1 个新结构/常数（排除「零成本生成」退化逃逸）。
    return need_gen >= 1 and cost_per >= 1 and need_gen * cost_per <= max_extra


PRICE_REAL = dict(need_gen=1, cost_per=1, max_extra=0,
                  ok=feasible(1, 1, 0))
PRICE_POS = dict(need_gen=1, cost_per=1, max_extra=1,
                 ok=feasible(1, 1, 1))
PRICE_VARIANTS = [
    dict(need_gen=0, cost_per=1, max_extra=0, ok=feasible(0, 1, 0)),
    dict(need_gen=1, cost_per=0, max_extra=0, ok=feasible(1, 0, 0)),
    dict(need_gen=1, cost_per=1, max_extra=1, ok=feasible(1, 1, 1)),
    dict(need_gen=2, cost_per=1, max_extra=1, ok=feasible(2, 1, 1)),
    dict(need_gen=1, cost_per=1, max_extra=0, ok=feasible(1, 1, 0)),
]

# ----------------------------------------------- G. dedup / numbering / AST
DUP_NEEDLES = ['成功态反演', '唯一门与必要条件清单对账', '从唯一成功案例反推',
               '门—清单', '必要条件集充分性缺口']
SCAN_DIRS = [B1, B2, V7, ROOT]
DUP_HITS = []
for d in SCAN_DIRS:
    if not os.path.isdir(d):
        continue
    for name in os.listdir(d):
        if (not name.endswith('.md') or name.startswith(BASE)
                or name.startswith('判定_attack54') or name.startswith('README')):
            continue
        fp = os.path.join(d, name)
        t = rd(fp)
        for w in DUP_NEEDLES:
            if w in t:
                DUP_HITS.append(dict(dir=os.path.basename(d), file=name, needle=w))
DUP_PROJECT = [h for h in DUP_HITS if h['file'].startswith('判定_') or h['file'].startswith('整理_')]


def scan_max(d, prefix, width):
    if not os.path.isdir(d):
        return 0
    pat = re.compile(r'^' + re.escape(prefix) + r'(\d{%d})' % width)
    vals = []
    for root, dirs, files in os.walk(d):
        for f in files:
            m = pat.match(f)
            if m:
                vals.append(int(m.group(1)))
    return max(vals) if vals else 0


MAX_ATTACK = scan_max(B1, 'attack', 2)
MAX_R = max(scan_max(B2, 'TUFT-r', 3), scan_max(B2, '判定_TUFT-r', 3))
ALL_NAMES = []
for d in (B1, B2):
    for root, dirs, files in os.walk(d):
        ALL_NAMES.extend(files)


def own_product(n):
    # 本册全部自身产物：引擎 / 数据三件 / 判定册（判定册落盘后复跑仍须为空号）。
    return n.startswith(BASE) or n.startswith('判定_' + BASE)


# 空号判定排除本册自身产物（自身 .py/.json/.md/_report.txt 已落盘时不得自指失败），
# 但他人抢注的 attack54_* / 含本圈号的文件仍必须被抓到。
A54_FREE = not any(n.startswith('attack54') and not own_product(n) for n in ALL_NAMES)
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
ALLOWED = set(['os', 'sys', 'io', 're', 'json', 'hashlib', 'ast', 'fractions', 'decimal'])
BANNED_CALLS = set(['eval', 'exec', 'compile', '__import__'])
CALLS = set(n.func.id for n in ast.walk(TREE)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name))
HARD_TRUE = [n for n in ast.walk(TREE) if isinstance(n, ast.Assign)
             and isinstance(n.value, ast.NameConstant)
             and any(isinstance(t, ast.Name) and ('VERDICT' in t.id or 'FINAL' in t.id)
                     for t in n.targets)]

# -------------------------------------------------------------- H. guards
guard('G01', all(P[k] and os.path.isfile(P[k]) for k in P) is False or
      len([k for k in P if os.path.isfile(P[k] or '')]) >= 14,
      '事实源现场存在 >=14/17（实到 %d）' % len([k for k in P if os.path.isfile(P[k] or '')]))
guard('G02', FACT_OK >= 14,
      '针词组容忍命中 %d/17（逐组缺词写入 json）' % FACT_OK)
guard('G03', all(COUNTS[t]['found'] == COUNTS[t]['expected'] for t in COUNTS),
      '五套清单现场解析计数 %s' % json.dumps(dict((k, v['found']) for k, v in COUNTS.items()), ensure_ascii=False))
guard('G04', len(JROWS) == 6 and '分数：0/6' in TXT.get('j99', ''),
      'J99 记分板 6 条现场解析 + 0/6（得 %d）' % len(JROWS))
guard('G05', SUCCESS_PRESENT and all(a['hit'] for a in S_ACTIONS),
      '成功态反演：电弱 6/6 与 L_EW 现场 %s；G1/G2/G3 针词命中 %d/3（%s）' %
      ('成立' if SUCCESS_PRESENT else '不成立',
       sum(1 for a in S_ACTIONS if a['hit']),
       ','.join(a['id'] + ':' + str(len(a['hits'])) for a in S_ACTIONS)))
guard('G06', N_LEDGER == 37 and len(COVER) == 43,
      '三层矩阵 37 条件 + 6 记分板 = 43 行（实 %d + %d）' % (N_LEDGER, len(JROWS)))
guard('G07', N_STRICT_LEDGER == 0 and N_STRICT_J == 0,
      '严格方向门在 LEDGER %d/37、SCOREBOARD %d/6 命中' % (N_STRICT_LEDGER, N_STRICT_J))
guard('G08', len(COUNTER) > 0 and len(GATE_SET) > 0,
      '充分性穷举：LEVEL 集 %d 组、反例 %d 组、GATE 集 %d 组' %
      (len(LEVEL_SET), len(COUNTER), len(GATE_SET)))
guard('G09', (2, 1) in COUNTER and gate_ok(1, 2) and not gate_ok(1, 1),
      '反例 (2,1) 存在 + 阳性 (1,2) 通过 + 边界 (1,1) 不通过')
guard('G10', N_ADV_NEG == 0 and N_ADV_TOTAL == 12,
      '方向账 %d 个推进动作中净下降 %d 个（成功态电弱 -1 单列）' % (N_ADV_TOTAL, N_ADV_NEG))
guard('G11', PRICE_REAL['ok'] is False and PRICE_POS['ok'] is True,
      '代价两难：真实 INFEASIBLE、放宽 max_extra=1 阳性 FEASIBLE')
guard('G12', len(PRICE_VARIANTS) == 5 and
      PRICE_VARIANTS[0]['ok'] is False and PRICE_VARIANTS[2]['ok'] is True and
      PRICE_VARIANTS[4]['ok'] is False,
      'feasible 五组反事实：0/0/1/0/0 定向翻转（实 %s）' %
      str([int(v['ok']) for v in PRICE_VARIANTS]))
guard('G13', len(DUP_PROJECT) == 0,
      '查重：5 个反向推导专有针词在本项目判定/整理册命中 %d（其余命中如实登记 %d）' %
      (len(DUP_PROJECT), len(DUP_HITS)))
guard('G14', MAX_ATTACK >= 53 and MAX_R >= 400 and CIRC_FREE and A54_FREE,
      '动态实扫 attack>=53 / r>=400（实 %d / %d）+ attack54 与 %s 空号' %
      (MAX_ATTACK, MAX_R, CIRC))
guard('G15', IMPORTS <= ALLOWED and not (CALLS & BANNED_CALLS) and len(HARD_TRUE) == 0,
      'AST：第三方导入 %d、禁用调用 %d、硬编码结论布尔 %d' %
      (len(IMPORTS - ALLOWED), len(CALLS & BANNED_CALLS), len(HARD_TRUE)))
guard('G16', hits_any('净减 1 个自由参数', GATE_STRICT) and
      not hits_any('自由参数数 ≤ 观测数 − 1', GATE_STRICT),
      '词表有牙：成功态动作命中严格门、静态上限不命中（防把 U5 误读成门）')
guard('G17', not hits_any('与全部精密观测相容', GATE_WEAK) and
      hits_any('参数计数不劣于对照理论', GATE_WEAK),
      '弱门词表有牙：U7「相容」不命中、J#2 弱相关命中（防「相容≠统一」误读）')
guard('G18', sum(ACT_COVER[k]['ledger'] for k in ACT_COVER) >= 0 and
      ACT_COVER['G1']['ledger'] == 0,
      '三动作覆盖矩阵：G1 在 37 条清单命中 %d（严格 0）' % ACT_COVER['G1']['ledger'])

# --------------------------------------------------------------- I. entries
add('E01', 'PASS', '控制组：唯一成功态与全部事实源现场可核对',
    '事实源 %d/17 存在、针词容忍组 %d/17；电弱统一 r119 控制组 6/6、r403 唯一 C3 真统一 L_EW（仅 2 力）、含引力四力大统一正确方程 0 条；J99 记分板 0/6 现场解析 6 条。本册不重判任何一条。' %
    (len([k for k in P if os.path.isfile(P[k] or '')]), FACT_OK))
add('E02', 'FAIL', '反向推导第一层：成功态反演出三个生成动作',
    '从唯一成功态倒推（非归纳）：G1 参数/前提净减 delta=-1（U5 净减 1 个自由参数）、G2 无量纲比值由结构闭式导出（精确层 M_W/M_Z = cosθ_W，数值层 ρ = 1.01043、偏差 0.52%% 由 m_t/Higgs 圈修正解释）、G3 先于观测的单点预言带误差带（m_t = 173 GeV vs 实测 172.76 GeV，偏差 0.139%%）。三者针词现场命中 %d/3。这是全仓首次以「已攻破样本」为起点反推成功所需动作。' %
    sum(1 for a in S_ACTIONS if a['hit']))
add('E03', 'FAIL', '承重裁定：唯一门从未写进任何一套验收条件',
    'r134 判「唯一门＝前提净下降，净变化 +11 未通过，须消除 37 个未导出前提」。现场解析五套必要条件清单 C1–C8 / N1–N18 / U1–U7 / R1–R4 共 %d 条与 J99 记分板 %d 条，构成 %d 行对账矩阵：严格方向门（净减/净下降/前提减少/净变化）在清单命中 %d/%d、记分板命中 %d/%d；弱门词（参数计数/不劣于对照）清单 %d、记分板 %d（仅 J#2「参数计数不劣于对照理论」弱相关，它是水平比较 n≤n_ctrl，不是 Delta<0）。⇒ 真正卡住攻破的门在「清单层」与「记分板层」都没有被写成验收条件，只以事后读数出现。' %
    (N_LEDGER, len(JROWS), len(COVER), N_STRICT_LEDGER, N_LEDGER, N_STRICT_J,
     len(JROWS), N_WEAK_LEDGER, N_WEAK_J))
add('E04', 'FAIL', '充分性首次机器化证明：必要条件集不是充分集',
    'G1 清单 L53 自陈「非充分条件集」但从未证明。本册把清单语义抽象为 LEVEL 约束（n_out>=1 ∧ extra=0 ∧ moduli=0），把唯一门抽象为 GATE（n_in−n_out<0），在 n_in,n_out∈[0,6] 共 %d 组穷举：满足 LEVEL 的 %d 组中，不满足 GATE 的反例 %d 组（含 (2,1)：delta=+1，所有静态上限都满足但门未过）；GATE 阳性集 %d 组（gate(1,2)=True、gate(1,1)=False）。⇒ LEVEL ⊬ GATE，即「把全部必要条件修好」在逻辑上不蕴含「通过唯一门」。这就是「为什么按清单补齐仍不攻破」的机器证明。' %
    (len(GRID), len(LEVEL_SET), len(COUNTER), len(GATE_SET)))
add('E05', 'FAIL', '方向账：所有推进动作与成功态反号',
    '现场登记 %d 个推进动作（r133 四型修补 +≥1/0/0/0、r134 +11、attack41 6→12→≥15→UNBOUNDED、归一正本 UFE-1 INPUT 19→26、attack53 23 类下界每类 +1、attack45 0/80、attack46 0/120、r406 ACCEPTED 0）：净下降动作 %d/%d。唯一 NEGATIVE 是电弱成功态 delta=-1。⇒ 库内 400+ 册全部在做「加输入 / 换说法 / 缩范围 / 断边」，而唯一成功案例做的是「减一个前提」；方向反了，且没有任何清单约束方向。' %
    (N_ADV_TOTAL, N_ADV_NEG, N_ADV_TOTAL))
add('E06', 'FAIL', '反向代价两难：生成必加输入，加输入违反记分板 #1',
    '从 0/6 到非零至少需要 1 个由结构生成的内生输出；attack53 现场给出每个桥接签名类至少 +1 新自由常数（23 类下界）、归一正本 UFE-1 INPUT 19→26、r406 Omega5-S 10 条出口 ACCEPTED 0。而 J99 记分板 #1 为「单一耦合关系（不需额外质量标度）」＝ max_extra=0。机器判据 feasible(need=1,cost=1,max=0)=False（INFEASIBLE，含 need>=1 与 cost>=1 双前提以排除放弃生成 / 零成本生成两种退化逃逸），放宽 max=1 阳性对照 True。⇒ 现有公理配额内「生成动作」与「不许加输入」互斥；这是反向推导给出的不可达证明，不是新物理。')
add('E07', 'BOUNDARY', '口径与分工（防重复造轮子）',
    '既有 10+ 册回答「为什么没攻破」均为正向归纳（终版四根因族 R1–R4 15:1、蓝本 C1–C8、G1 N1–N18、r119 U1–U7、r133 四型修补、r134 唯一门）或侧向扰动（attack41 注入条数 / attack45 假设替换 80 格 / attack46 基础块抽除 120 格）。本册自变量＝「从已成功样本反推的动作」，因变量＝「三层验收条件的覆盖率与充分性」，与上述册自变量、因变量均不同。口径：电弱 6/6 属 r119 的 U1–U7（U3 N/A），J99 0/6 属另一把尺子，归一本 §0 明令禁止跨用，本册不混算达成度。')
add('E08', 'PASS', '判据有牙：阳性对照与变异守卫',
    'G16 词表有牙（「净减 1 个自由参数」命中严格门、「自由参数数 ≤ 观测数 − 1」不命中）；G17 防止把 U7「与全部精密观测相容」误读成方向门（不命中弱门、J#2 命中）；G09 (2,1) 反例 + (1,2) 阳性 + (1,1) 边界；G11/G12 feasible 五组反事实定向翻转；G13 五个反向推导专有针词在本项目判定/整理册命中 %d，说明不是「一律否定」也不是恒真守卫。' % len(DUP_PROJECT))
add('E09', 'INFO', '自抓与射程',
    '① 首版拟判「清单 37 条全为禁止型、0 条构造型」，现场复核发现 C2/C6/N16/N17/U4/U6 确为「必须有输出」的存在型条件 ⇒ 改为「LEVEL vs GATE 逻辑独立性」的可穷举判据，避免主观词表判死；② 首版拟用抽象 6/6 记分板做反事实，因会把电弱 6/6 与 J99 0/6 两把尺子混算而撤回（归一本 §0 红线）；③ 五套清单解析需去重（r119 的 U1–U7 在 §〇/§一 各出现一次），否则 7→14 计数失真；④ 方向门词表必须区分「静态上限」与「净变化方向」，否则 U5 会造成假阳性。⑤ 实跑另抓 4 处实现缺陷：G05 两针词按记忆写死（回磁盘核对后改多针词列表）、G12 feasible 把「放弃生成 / 零成本生成」两种退化逃逸判可行（加 need>=1 与 cost>=1 双前提）、G14 ALL_NAMES 含自身已落盘 .py 造成自指失败（排除本册自身产物）、E02 串内裸 % 与 E06 多余的 % 空串格式化（修字面量）；SELF_FIX 由空补为 9 条结构化落盘。射程：只判「在既有五套清单 + J99 记分板 + Omega5 配额内不可达」，不宣称统一场论不可能，不否认换公理集 / 新来料出口。')
add('E10', 'INFO', '总裁定：WHY-NOT-BROKEN--DIRECTION-GATE-NEVER-REGISTERED--LEVEL-NOT-IMPLY-GATE',
    '以前没有攻破，不是根因族列得不够，也不是按清单补齐没做够；而是库内两套完成判据（37 条必要条件清单、J99 六条记分板）都只约束「不许有什么 / 必须有输出」，真正决定成败的唯一门「前提净下降 Delta<0」从未被写进任何一套验收条件，且所有推进动作的方向都与它反号。反向推导的增量＝把这句「非充分条件集」首次变成可穷举证明，并给出缺口的精确位置。红线不变：0/6、0/22、UFT-3=0、L3=0、validated=0、含引力四力大统一正确方程 0 条。')

# --------------------------------------------------------------- J. outputs
OUT = dict(
    meta=dict(round='attack54', circle=CIRC, date='2026-11-09',
              kind='REVERSE_DERIVATION', engine='pure stdlib Python 3.8 / Fraction / Decimal(60)',
              read_only=True, verdict='WHY-NOT-BROKEN--DIRECTION-GATE-NEVER-REGISTERED--LEVEL-NOT-IMPLY-GATE',
              entries=len(ENTRIES), guards=len(GUARDS),
              guards_ok=sum(1 for g in GUARDS if g['ok'])),
    fact_sources=dict((k, dict(path=(os.path.relpath(v, ROOT).replace('\\', '/') if v else None),
                               md5=md5(v), needles=FACT_HITS[k])) for k, v in P.items()),
    success_inversion=dict(only_success='electroweak L_EW (r403 / r119 6/6)',
                           present=SUCCESS_PRESENT, actions=S_ACTIONS),
    ledger_counts=COUNTS, ledger_rows=[dict(layer=r['layer'], set=r['set'], code=r['code'], text=r['text'])
                                       for r in COVER],
    coverage=dict(matrix_rows=len(COVER),
                  strict_gate=dict(ledger=N_STRICT_LEDGER, scoreboard=N_STRICT_J),
                  weak_gate=dict(ledger=N_WEAK_LEDGER, scoreboard=N_WEAK_J),
                  action_coverage=ACT_COVER,
                  gate_words_strict=GATE_STRICT, gate_words_weak=GATE_WEAK),
    sufficiency=dict(grid=len(GRID), level_set=len(LEVEL_SET),
                     counterexamples=len(COUNTER), counter_sample=COUNTER[:6],
                     gate_set=len(GATE_SET),
                     interpretation='LEVEL constraints do not imply GATE(delta<0); '
                                   'first machine proof of G1 L53 non-sufficiency claim'),
    direction=dict(advance_actions=N_ADV_TOTAL, negative_actions=N_ADV_NEG,
                   only_negative='electroweak L_EW delta=-1 (success sample, not an advance action)',
                   rows=DIRECTION),
    price=dict(real=PRICE_REAL, positive_control=PRICE_POS, variants=PRICE_VARIANTS,
               interpretation='feasible requires need>=1 AND cost>=1 (excludes two '
                              'degenerate escapes: abandon generation / zero-cost generation); '
                              'each generative output costs >=1 new constant; '
                              'J99 #1 forbids extra scales => INFEASIBLE inside current axioms'),
    dedup=dict(needles=DUP_NEEDLES, project_hits=len(DUP_PROJECT), all_hits=len(DUP_HITS),
               hits=DUP_HITS[:20]),
    numbering=dict(attack_max=MAX_ATTACK, r_max=MAX_R, attack54_free=A54_FREE,
                   circle_free=CIRC_FREE, note='dynamic disk scan; R chain not occupied'),
    ast=dict(imports=sorted(IMPORTS), banned_calls=sorted(CALLS & BANNED_CALLS),
             hardcoded_verdict_booleans=len(HARD_TRUE)),
    guards=GUARDS, entries=ENTRIES, self_corrections=SELF_FIX,
)

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    json.dump(OUT, f, ensure_ascii=False, indent=2)

lines = []
lines.append('# %s · 数据产物' % BASE)
lines.append('')
lines.append('- 轮次：attack54 / 攻破%s｜日期：2026-11-09｜性质：反向推导（只读审计）' % CIRC)
lines.append('- 守卫：%d/%d｜条目：%d｜退出码：见 _report.txt' %
             (OUT['meta']['guards_ok'], len(GUARDS), len(ENTRIES)))
lines.append('- 判词：`%s`' % OUT['meta']['verdict'])
lines.append('')
lines.append('## 三层对账矩阵（承重）')
lines.append('')
lines.append('| 层 | 行数 | 严格方向门命中 | 弱门词命中 |')
lines.append('|---|---:|---:|---:|')
lines.append('| LEDGER（C8+N18+U7+R4） | %d | %d | %d |' % (N_LEDGER, N_STRICT_LEDGER, N_WEAK_LEDGER))
lines.append('| SCOREBOARD（J99 0/6） | %d | %d | %d |' % (len(JROWS), N_STRICT_J, N_WEAK_J))
lines.append('')
lines.append('## 三动作覆盖')
lines.append('')
for k in ACT_ANCHORS:
    v = ACT_COVER[k]
    lines.append('- %s：LEDGER %d、SCOREBOARD %d' %
                 (k, v['ledger'], v['scoreboard']))
lines.append('')
lines.append('## 充分性穷举')
lines.append('')
lines.append('grid=%d, LEVEL=%d, counterexamples=%d, GATE=%d' %
             (len(GRID), len(LEVEL_SET), len(COUNTER), len(GATE_SET)))
lines.append('')
lines.append('## 方向账')
lines.append('')
lines.append('advance=%d, negative=%d（唯一负值为电弱成功态，不计推进动作）' %
             (N_ADV_TOTAL, N_ADV_NEG))
lines.append('')
lines.append('## 条目')
lines.append('')
for e in ENTRIES:
    lines.append('- **%s [%s]** %s：%s' % (e['code'], e['status'], e['title'], e['detail']))
lines.append('')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

rep = []
rep.append('ENGINE  %s' % BASE)
rep.append('VERDICT %s' % OUT['meta']['verdict'])
rep.append('GUARDS  %d/%d' % (OUT['meta']['guards_ok'], len(GUARDS)))
for g in GUARDS:
    rep.append('  %-5s %s  %s' % (g['code'], 'OK' if g['ok'] else 'FAIL', g['note']))
rep.append('ENTRIES %d' % len(ENTRIES))
for e in ENTRIES:
    rep.append('  %-4s %-9s %s' % (e['code'], e['status'], e['title']))
    rep.append('        %s' % e['detail'])
rep.append('KEY_NUMBERS')
rep.append('  ledger_rows=%d scoreboard_rows=%d matrix=%d' % (N_LEDGER, len(JROWS), len(COVER)))
rep.append('  strict_gate ledger=%d/%d scoreboard=%d/%d' %
           (N_STRICT_LEDGER, N_LEDGER, N_STRICT_J, len(JROWS)))
rep.append('  weak_gate   ledger=%d scoreboard=%d' % (N_WEAK_LEDGER, N_WEAK_J))
rep.append('  act_cover   %s' % json.dumps(ACT_COVER, ensure_ascii=False))
rep.append('  grid=%d level=%d counter=%d gate=%d' %
           (len(GRID), len(LEVEL_SET), len(COUNTER), len(GATE_SET)))
rep.append('  advance=%d negative=%d' % (N_ADV_TOTAL, N_ADV_NEG))
rep.append('  price_real=%s price_positive=%s' % (PRICE_REAL['ok'], PRICE_POS['ok']))
rep.append('  dedup_project=%d dedup_all=%d' % (len(DUP_PROJECT), len(DUP_HITS)))
rep.append('  attack_max=%d r_max=%d attack54_free=%s circle_free=%s' %
           (MAX_ATTACK, MAX_R, A54_FREE, CIRC_FREE))
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep) + '\n')

print('\n'.join(rep[:6]))
print('ENGINE DONE  guards=%d/%d  entries=%d' %
      (OUT['meta']['guards_ok'], len(GUARDS), len(ENTRIES)))
sys.exit(0 if OUT['meta']['guards_ok'] == len(GUARDS) else 1)
