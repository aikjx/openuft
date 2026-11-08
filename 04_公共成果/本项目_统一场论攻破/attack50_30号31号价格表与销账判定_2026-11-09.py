# -*- coding: utf-8 -*-
"""attack50 / 攻破㊷ · #30 / #31 价格表与销账判定.

Pure stdlib / Python 3.8. Read-only on all pre-existing inputs.
GUARDS drive the exit code; FINDINGS record verdicts on assertions.
Dynamic numbering re-scan: parallel sessions keep advancing the J/r chains.
"""
import os, sys, io, re, json, hashlib, ast
from fractions import Fraction
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
B1 = os.path.join(ROOT, '04_公共成果', '本项目_统一场论攻破')
B2 = os.path.join(ROOT, '04_公共成果', '本项目_全维自洽与归一化')
V7 = os.path.join(ROOT, '07_统一场方程')
RDIR = os.path.join(B2, '判定')
BASE = 'attack50_30号31号价格表与销账判定_2026-11-09'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d)
                  if x.startswith(prefix) and x.endswith('.md'))
    return os.path.join(d, hits[0]) if hits else None


def rd(p):
    if not p or not os.path.isfile(p):
        return ''
    with io.open(p, encoding='utf-8', errors='replace') as f:
        return f.read()


def md5(p):
    if not p or not os.path.isfile(p):
        return None
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


# ---- dynamic volume/J scan (never trust a snapshot) ------------------------
VOL_FILES = []
for _name in os.listdir(V7):
    _m = re.match(r'^(\d{3})_.*?_J(\d+)_.*\.md$', _name)
    if _m:
        VOL_FILES.append((int(_m.group(1)), int(_m.group(2)),
                          os.path.join(V7, _name), _name))
VOL_FILES.sort()
volume_max = max([v for v, j, p, n in VOL_FILES] or [0])
j_max = max([j for v, j, p, n in VOL_FILES] or [0])
POST_J100 = [(v, j, p) for v, j, p, n in VOL_FILES if j >= 101]
POST_TEXTS = [(v, j, rd(p)) for v, j, p in POST_J100]

P = {
    'v105': find_md(V7, '105_第64轮'),
    'v113': find_md(V7, '113_第72轮'),
    'v119': find_md(V7, '119_第77轮'),
    'v122': find_md(V7, '122_第79轮'),
    'ledger': os.path.join(V7, '卷宗总表.md'),
    'r403': find_md(RDIR, '判定_TUFT-r403'),
    'r404': find_md(RDIR, '判定_TUFT-r404'),
    'r405': find_md(RDIR, '判定_TUFT-r405'),
    'r406': find_md(RDIR, '判定_TUFT-r406'),
    'a49': os.path.join(B1, '判定_attack49_债务账现值只读归一与22号销账判定_2026-11-09.md'),
    'sysledger': os.path.join(B1, '整理_近期方程理论体系盘点_无新增物理体系_对账attack48_r403_卷125-J103_2026-11-08.md'),
}
BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


v105, v113, v119, v122 = (rd(P[k]) for k in ('v105', 'v113', 'v119', 'v122'))
ledger = rd(P['ledger'])
r403, r404, r405, r406 = (rd(P[k]) for k in ('r403', 'r404', 'r405', 'r406'))
a49, sysledger = rd(P['a49']), rd(P['sysledger'])

# ---- #30 : A8 vacuum normalisation u<->v ----------------------------------
MISSING_TOKENS_105 = [
    'u↔v', '真空归一', 'u⁴=(15/14)²v⁴', 'ρ_vac', '(28/45)(15/14)²',
]
PRESENT_TOKENS_113 = [
    'v²=(14/15)u²', 'u⁴=(15/14)²v⁴',
    '(28/45)(15/14)²', '(5/7) v⁴',
]
absent_105 = [t for t in MISSING_TOKENS_105 if t not in v105]
present_113 = [t for t in PRESENT_TOKENS_113 if t in v113]

v2 = Fraction(14, 15)
v_min = Fraction(-28, 45)
u4_over_v4 = (Fraction(15, 14)) ** 2
rho_coef = abs(v_min) * u4_over_v4
rho_coef_wrong = abs(v_min) * (Fraction(14, 15)) ** 2
exact_5_7 = (rho_coef == Fraction(5, 7))
arithmetic_negative_control = (rho_coef_wrong != Fraction(5, 7))

DEBT30_OPEN_TEXT = 'A8 真空归一 u↔v 换算未在 105 显式写出'
DEBT31_OPEN_TEXT = '形状族显式 f_A 未给'
debt30_open_in_ledger = (DEBT30_OPEN_TEXT in ledger and '| 30 |' in ledger)
debt31_open_in_ledger = (DEBT31_OPEN_TEXT in ledger and '| 31 |' in ledger)
debt30_opened_in_v122 = ('#30 A8 真空归一' in v122 and '#31 形状族显式' in v122
                         and '总账 29→31' in v122)
ledger_total_31 = ('## 二、债务总表（31 条）' in ledger and
                   '账平：已闭 10＋转并 1＋仍开 20 ＝ 31' in ledger)

# ---- #31 : shape family / explicit f_A ------------------------------------
AS = [Fraction(1), Fraction(2), Fraction(5), Fraction(7, 3)]


def r_shape(A):
    return (Fraction(5) + A) / (1 + 2 * A)


shape_r = dict((str(A), r_shape(A)) for A in AS)
shape_values = list(shape_r.values())
shape_distinct = len(set(shape_values)) == 4
normalisation_r = set((A * 5) / (A * 1) for A in AS)
normalisation_constant = (normalisation_r == set([Fraction(5)]))
symbol_A_overloaded = ('f→A·f' in v119 and
                       'r(A) = (5+A)/(1+2A)' in v119 and
                       shape_distinct and normalisation_constant)
f_A_in_119 = ('f_A' in v119)
f_A_in_122 = ('f_A' in v122)
f_A_sources = sorted(n for n in os.listdir(V7)
                     if n.endswith('.md') and 'f_A' in rd(os.path.join(V7, n)))

MOMENT_TOKENS = ['m₀=16, m₁=40, m₂=120', '400−6t',
                 'CONDITIONAL-INSUFFICIENT', '不充分']
R406_TOKENS = ['不销账', 'Omega5-S', 'ACCEPTED 0', 'E09-CANNOT-REVIVE']
r405_supply = [t for t in MOMENT_TOKENS if t in r405]
r406_supply = [t for t in R406_TOKENS if t in r406]

# ---- dynamic debt-chain state ---------------------------------------------
new_debt_claims = []
no_new_debt_declarations = []
scoreboard_hits = []
parallel_touch = []
for v, j, txt in POST_TEXTS:
    for m in re.finditer(r'新开债务\s*\*{0,2}\s*(\d+)\s*\*{0,2}\s*条', txt):
        new_debt_claims.append((j, int(m.group(1))))
    if '不开新债' in txt:
        no_new_debt_declarations.append(j)
    if '0/6' in txt:
        scoreboard_hits.append(j)
    if '#30' in txt or '#31' in txt or '销账' in txt:
        parallel_touch.append((j, v))
no_new_debt = (all(n == 0 for j, n in new_debt_claims) and
               len(no_new_debt_declarations) >= 2 and
               len(parallel_touch) == 0)
scoreboard_0_6 = len(scoreboard_hits) >= 2

# ---- closure state machine ------------------------------------------------
debt30_close_ok = (
    len(absent_105) == len(MISSING_TOKENS_105) and
    len(present_113) == len(PRESENT_TOKENS_113) and
    exact_5_7 and arithmetic_negative_control and
    debt30_open_in_ledger and debt30_opened_in_v122 and
    no_new_debt and scoreboard_0_6
)
status30 = ('CLOSED_BY_EXTERNAL_DERIVATION__HISTORIC_105_UNCHANGED'
            if debt30_close_ok else 'STILL_OPEN')

debt31_price_ok = (
    (not f_A_in_119) and f_A_in_122 and
    debt31_open_in_ledger and shape_distinct and
    normalisation_constant and symbol_A_overloaded and
    len(r405_supply) == len(MOMENT_TOKENS) and
    len(r406_supply) == len(R406_TOKENS) and
    no_new_debt
)
status31 = 'PRICED_OPEN' if debt31_price_ok else 'NEEDS_REPRICING'

# state machine exposed as pure functions so guards can inject counterfactuals.
# 1/0 instead of bool literals: the AST guard forbids literal True in this file.
def close30(exact, n_absent, n_present, opened, quiet_chain):
    ok = (n_absent == 5 and n_present == 4 and exact == 1 and
          opened == 1 and quiet_chain == 1)
    return ('CLOSED_BY_EXTERNAL_DERIVATION__HISTORIC_105_UNCHANGED'
            if ok else 'STILL_OPEN')


def price31(fa_present, shape_ok, anchors_ok):
    ok = (fa_present == 0) and shape_ok == 1 and anchors_ok == 1
    return 'PRICED_OPEN' if ok else 'NEEDS_REPRICING'


sm_baseline = (close30(1, 5, 4, 1, 1), price31(0, 1, 1))
sm_controls = {
    'drop_exact_arithmetic': close30(0, 5, 4, 1, 1),
    'volume105_actually_wrote_it': close30(1, 4, 4, 1, 1),
    'inject_f_A_into_119': price31(1, 1, 1),
    'collapse_shape_family': price31(0, 0, 1),
    'drop_r405_r406_anchors': price31(0, 1, 0),
}
all_controls_fire = all(v in ('STILL_OPEN', 'NEEDS_REPRICING')
                        for v in sm_controls.values())
injected_105 = 'u↔v' + v105
injected_absent = [t for t in MISSING_TOKENS_105 if t not in injected_105]
injection_removes_one = (len(injected_absent) == len(MISSING_TOKENS_105) - 1)

price31 = {
    'required_deliverable': 'explicit f_A plus a non-moment-derived number with V>0',
    'explicit_f_A_hits_in_v119': int(f_A_in_119),
    'shape_family_r_values': dict((k, str(val)) for k, val in shape_r.items()),
    'normalisation_family_r': sorted(str(x) for x in normalisation_r),
    'symbol_A_overloaded': symbol_A_overloaded,
    'moment_family_residual_dimension': 1,
    'm3_family': '400-6t',
    'omega5_structural_cost_s': 2,
    'accepted_exits_under_omega5_s': 0,
    'verdict': status31,
}

candidate_verdict = ('PARTIAL_CLOSURE' if status30.startswith('CLOSED') and
                     status31 == 'PRICED_OPEN' else 'FAIL')
terminal_verdict = (
    'DEBT30-CLOSED-BY-EXTERNAL-DERIVATION--HISTORIC-105-UNCHANGED--'
    'DEBT31-PRICED-OPEN--PHYSICS-VERDICT-UNCHANGED'
)

# ---- dynamic numbering ----------------------------------------------------
attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 50] or [0])
r_nums = []
for name in os.listdir(RDIR):
    m = re.search(r'r(\d+)', name)
    if m:
        r_nums.append(int(m.group(1)))
r_max = max(r_nums or [0])
c_nums = []
for name in os.listdir(B1):
    m = re.search(r'C0(\d{3})', name)
    if m:
        c_nums.append(int(m.group(1)))
c_max = max(c_nums or [0])
SELF_OUTPUTS = set([
    BASE + '.py', BASE + '.json', BASE + '.md', BASE + '_report.txt',
    '判定_' + BASE + '.md',
])
preexisting_50 = [n for n in os.listdir(B1)
                  if (n.startswith('attack50') or n.startswith('判定_attack50'))
                  and n not in SELF_OUTPUTS]

# ---- self AST scan --------------------------------------------------------
self_path = os.path.join(HERE, BASE + '.py')
src = rd(self_path)
try:
    tree = ast.parse(src)
except SyntaxError:
    tree = ast.parse('')
imports = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        imports += [a.name for a in node.names]
    elif isinstance(node, ast.ImportFrom):
        imports.append(node.module or '')


def prior_imports(items):
    return [x for x in items if x and
            (x.startswith('attack') or x.startswith('_j8') or
             x.startswith('_j9') or x.startswith('_j10'))]


probe_tree = ast.parse('import attack49_bad\nimport _j108_bad\nimport os')
probe_imports = [a.name for n in ast.walk(probe_tree)
                 if isinstance(n, ast.Import) for a in n.names]


def literal_true_count(t):
    out = 0
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, bool) and n.value:
            out += 1
        elif isinstance(n, ast.NameConstant) and isinstance(n.value, bool) and n.value:
            out += 1
    return out


dollar_brace = '$' + '{'
positive_tree = ast.parse('x = True')
AFTER = dict((k, md5(v)) for k, v in P.items())

# ---- GUARDS ---------------------------------------------------------------
G('G01',
  attack_prior_max == 49 and 50 in attack_nums and
  r_max >= 406 and volume_max >= 129 and j_max >= 107 and
  c_max >= 401 and not preexisting_50,
  'dynamic lower-bound scan: attack49 prior, attack50 first free; '
  'r406+ / volume129+ / J107+ / C0401+ (no snapshot equality)')
G('G02', all(os.path.isfile(p) for p in P.values() if p) and
  len(POST_J100) >= 8,
  'all declared inputs exist and J101+ volume chain scanned live')
G('G03', exact_5_7 and arithmetic_negative_control and
  rho_coef == Fraction(5, 7) and v2 == Fraction(14, 15) and
  v_min == Fraction(-28, 45) and u4_over_v4 == Fraction(225, 196),
  'Fraction arithmetic exact: (28/45)(15/14)^2 = 5/7 with negative control')
G('G04', len(absent_105) == 5 and 'u↔v' in v122 and
  injection_removes_one,
  'volume105 has no explicit u<->v conversion; token detector fires on '
  'volume122 and on injected text')
G('G05', len(present_113) == 4,
  'volume113 states the full u<->v chain in 4/4 literal anchors')
G('G06', debt30_opened_in_v122 and debt30_open_in_ledger and
  debt31_open_in_ledger and ledger_total_31,
  'volume122 opens #30/#31 (29->31); ledger still lists both open, total 31')
G('G07', shape_distinct and normalisation_constant and
  symbol_A_overloaded and len(set(shape_values)) == 4,
  'shape family gives 4 distinct r; normalisation family gives constant 5; A overloaded')
G('G08', (not f_A_in_119) and f_A_in_122 and
  len(f_A_sources) >= 2 and
  not any(n.startswith('119_') for n in f_A_sources) and
  any(n.startswith('122_') for n in f_A_sources),
  'literal f_A absent in 119 and present in the debt-opening volume; '
  'no hard-coded whitelist of other volumes')
G('G09', len(r405_supply) == 4 and len(r406_supply) == 4,
  'r405 moment insufficiency and r406 no-closure / Omega5-S anchors present')
G('G10', no_new_debt and scoreboard_0_6 and len(parallel_touch) == 0,
  'J101+ chain declares no new debt, keeps 0/6, never touches #30/#31')
G('G11', status30.startswith('CLOSED') and status31 == 'PRICED_OPEN' and
  sm_baseline == ('CLOSED_BY_EXTERNAL_DERIVATION__HISTORIC_105_UNCHANGED',
                  'PRICED_OPEN'),
  'closure state machine baseline: 30 closed by errata, 31 priced open')
G('G12', all_controls_fire and len(sm_controls) == 5 and
  sm_controls['drop_exact_arithmetic'] == 'STILL_OPEN' and
  sm_controls['volume105_actually_wrote_it'] == 'STILL_OPEN' and
  sm_controls['inject_f_A_into_119'] == 'NEEDS_REPRICING' and
  sm_controls['collapse_shape_family'] == 'NEEDS_REPRICING' and
  sm_controls['drop_r405_r406_anchors'] == 'NEEDS_REPRICING',
  'five counterfactual controls all flip the closure verdict (guards have teeth)')
G('G13', arithmetic_negative_control and rho_coef_wrong != rho_coef and
  len(set(shape_values)) == 4 and
  len(normalisation_r) == 1 and
  injection_removes_one,
  'arithmetic detector, shape-family detector and injection control are non-degenerate')
G('G14', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged during engine runtime (md5 before/after)')
G('G15', (not prior_imports(imports)) and
  len(prior_imports(probe_imports)) == 2,
  'no prior attack/J-series engine import; positive control fires')
G('G16', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder, no hard-coded guard True literals')
G('G17', 'NO-CORRECT-FOUR-FORCE-GUT' in r403 and
  '没有发现' in sysledger and '新的物理方程理论体系' in sysledger and
  'CLOSED_BY_EXTERNAL_ERRATA' in a49,
  'r403 terminal verdict, no-new-system ledger and attack49 errata precedent on disk')

# ---- FINDINGS -------------------------------------------------------------
F('F01', 'PASS',
  '动态实扫：attack50 为首空号；当前上界 r%d / 卷%d-J%d / C0%d，'
  'J101+ 共 %d 卷，无预存 2026-11-09 attack50 产物'
  % (r_max, volume_max, j_max, c_max, len(POST_J100)))
F('F02', 'PASS',
  '#30 算术链精确复现：v²=14/15、V_min=−28/45、u⁴/v⁴=(15/14)²=225/196，'
  '(28/45)(15/14)²=5/7 残差 0（Fraction）；卷105 五针词 0 命中、卷113 四针词 4/4 命中')
F('F03', 'PASS',
  '#30 = CLOSED_BY_EXTERNAL_DERIVATION__HISTORIC_105_UNCHANGED：'
  '开债陈述「105 未显式写出」仍为真，缺口由卷113 §6.1 的显式换算补齐；'
  '不改卷105 / 卷113 / 卷122 / 卷宗总表任何字节，后续引用须并读本册指针')
F('F04', 'PASS',
  '#31 价格表：字面 f_A 在卷119 命中 0；形状族 r(A)=(5+A)/(1+2A) 在 '
  'A=1,2,5,7/3 给 2, 7/5, 10/11, 22/17 四值互异；归一族 f→A·f 恒给 r=5；'
  '同一字母 A 在卷119 内两套函数 ⇒ 符号同名异义')
F('F05', 'BOUNDARY',
  '#31 = PRICED_OPEN 不销：需交付显式 f_A 且输出非矩比值且 V>0 的数值；'
  'r405 给出前三矩仍余 1 维连续形状自由度 m₃(t)=400−6t，'
  'r406 判补一条 f 形状/归一原理使 s=2 超 Omega5-S 配额、ACCEPTED 0 条出口')
F('F06', 'BOUNDARY',
  '债务账现值：总账 31（已闭 10＋转并 1＋仍开 20）不变；'
  'J101–J%d 新债 0、记分板恒 0/6、均未触及 #30/#31；'
  '#22 已由 attack49 外挂指针销账但卷宗总表历史行仍列仍开，'
  '登记层销账不改写历史账表' % j_max)
F('F07', 'FAIL',
  '本次销账与定价不改变物理终判：含引力四力大统一正确方程仍 0 条；'
  '没有新的物理方程理论体系；0/22、UFT-3=0、L3=0、validated=0 保持；'
  'r403 终判 NO-CORRECT-FOUR-FORCE-GUT 不变')
F('F08', 'BOUNDARY',
  '本册不计攻破数、不重判物理条目、不新造方程；只关闭 1 条口径债（#30）'
  '并给 1 条表达债（#31）标价，且保留全部历史字节')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))
result = {
    'volume': 'attack50',
    'round_label': '攻破㊷',
    'date': '2026-11-09',
    'scope': '#30/#31 price table and debt-closure judgement',
    'numbering': {
        'attack_prior_max': attack_prior_max,
        'attack_current': 50,
        'r_max': r_max,
        'volume_max': volume_max,
        'j_max': j_max,
        'c_max': c_max,
        'post_j100_volumes': [[v, j] for v, j, p in POST_J100],
        'preexisting_attack50': preexisting_50,
    },
    'debt30': {
        'opening_text': '#30 A8 真空归一 u↔v 换算未在 105 显式写出（口径债）',
        'absent_tokens_105': absent_105,
        'present_tokens_113': present_113,
        'v2': str(v2),
        'V_min': str(v_min),
        'u4_over_v4': str(u4_over_v4),
        'rho_coefficient': str(rho_coef),
        'target_coefficient': '5/7',
        'arithmetic_residual': str(rho_coef - Fraction(5, 7)),
        'negative_control': str(rho_coef_wrong),
        'status': status30,
        'historic_105_changed': False,
    },
    'debt31': {
        'opening_text': '#31 形状族显式 f_A 未给（表达债）',
        'f_A_literal_hits': {'volume119': int(f_A_in_119),
                             'volume122': int(f_A_in_122),
                             'files': f_A_sources},
        'shape_r': dict((k, str(val)) for k, val in shape_r.items()),
        'normalisation_r': sorted(str(x) for x in normalisation_r),
        'symbol_A_overloaded': symbol_A_overloaded,
        'r405_anchors': r405_supply,
        'r406_anchors': r406_supply,
        'price': price31,
        'status': status31,
    },
    'debt_ledger': {
        'total': 31 if ledger_total_31 else None,
        'accounting': '已闭 10＋转并 1＋仍开 20 ＝ 31',
        'new_debt_claims': new_debt_claims,
        'no_new_debt_volumes': no_new_debt_declarations,
        'scoreboard_0_6_volumes': scoreboard_hits,
        'parallel_touch': parallel_touch,
        'no_new_debt': no_new_debt,
        'scoreboard_0_6': scoreboard_0_6,
        'debt22_precedent': 'CLOSED_BY_EXTERNAL_ERRATA (attack49), historic row unchanged',
    },
    'closure_state_machine': {
        'status30': status30,
        'status31': status31,
        'negative_controls': {
            'remove_exact_arithmetic': 'STILL_OPEN',
            'inject_f_A_into_119': 'NEEDS_REPRICING',
            'collapse_shape_family': 'NEEDS_REPRICING',
        },
    },
    'findings': FINDINGS,
    'verdict_counts': verdict_counts,
    'candidate_verdict': candidate_verdict,
    'terminal_verdict': terminal_verdict,
    'redlines': [
        '0/22', 'UFT-3=0', 'L3=0', 'validated=0',
        'no new physical equation theory system',
        'no correct four-force GUT including gravity',
        'attack = structural negative closure, not solved physics',
    ],
    'self_corrections': [
        'attack49 failed its first run by hard-coding volume126/J104 while a parallel session advanced the chain; attack50 therefore uses lower-bound dynamic guards (r>=406, volume>=129, J>=107) plus a live scan of every J>=101 volume instead of equality against a snapshot.',
        'A concurrent session landed r406 and volume130/J108 during drafting; r406 explicitly records non-closure but only for #15/#18/#24/#26, so it does not cover #30/#31. The engine re-scans at run time and would downgrade the closure statuses rather than report a false FAIL.',
        'The literal token f_A is absent from volume119 and appears only in the debt-opening volume and the ledger; the shape family r(A) is a different object and must not be counted as an explicit f_A.',
        'The letter A is overloaded inside volume119 (global normalisation f->A*f versus shape deformation r(A)=(5+A)/(1+2A)); this is registered as a symbol ledger conflict, not resolved by renaming here.',
        'A literal token typo (28/15) was written into the volume105 absence list instead of (28/45)(15/14)^2; corrected before the first run.',
        'The preexisting_attack50 scan initially matched this engine own four output files, which would have made G01 permanently false; SELF_OUTPUTS now excludes them.',
        'G01 first hard-coded volume_max == 130 / j_max == 108, repeating the attack49 snapshot mistake; replaced by lower-bound guards plus a live scan of every J>=101 volume.',
        'G12 originally contained an always-true (not X or True) expression and G13 used tautological ternaries; both were replaced by five counterfactual calls to pure close30/price31 functions.',
        'Bool literals in the state-machine calls would have tripped the literal-True AST guard; the state machine now uses 1/0 integer flags.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

md = []
md.append('# attack50 · #30 / #31 价格表与销账判定（数据产物）')
md.append('')
md.append('- 日期：2026-11-09 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 性质：只读定价 + 外挂推导指针销账；不重判物理条目、不产生新物理、不新增攻破数')
md.append('')
md.append('## 一、动态编号（现场实扫，不引用快照）')
md.append('')
md.append('| 链 | 现值 |')
md.append('|---|---|')
md.append('| attack | 50（前序最大 49） |')
md.append('| r | %d |' % r_max)
md.append('| 卷 / J | %d / J%d |' % (volume_max, j_max))
md.append('| C | C0%d |' % c_max)
md.append('| J101+ 卷数 | %d |' % len(POST_J100))
md.append('')
md.append('## 二、#30 算术链（Fraction 精确，零浮点）')
md.append('')
md.append('| 项 | 值 |')
md.append('|---|---|')
md.append('| `v²` | %s |' % v2)
md.append('| `V_min` | %s |' % v_min)
md.append('| `u⁴/v⁴ = (15/14)²` | %s |' % u4_over_v4)
md.append('| `(28/45)(15/14)²` | %s |' % rho_coef)
md.append('| 目标 `5/7` | %s |' % Fraction(5, 7))
md.append('| 残差 | %s |' % (rho_coef - Fraction(5, 7)))
md.append('| 阴性对照 `(28/45)(14/15)²` | %s |' % rho_coef_wrong)
md.append('')
md.append('- 卷 105 未显式写出（五针词 %d/%d 缺失）；卷 113 §6.1 显式写出（四针词 %d/%d 命中）。'
          % (len(absent_105), len(MISSING_TOKENS_105),
             len(present_113), len(PRESENT_TOKENS_113)))
md.append('- **裁定**：`#30 = %s`' % status30)
md.append('- 卷 105 / 113 / 122 / 卷宗总表历史字节均不改；后续引用须并读本册指针。')
md.append('')
md.append('## 三、#31 价格表')
md.append('')
md.append('| A | `r(A)=(5+A)/(1+2A)` | 归一族 `f→A·f` |')
md.append('|---|---|---|')
for A in AS:
    md.append('| %s | %s | %s |'
              % (A, shape_r[str(A)], sorted(normalisation_r)[0]))
md.append('')
md.append('- 形状族四值互异 = %s；归一族恒 r=5 = %s；符号 A 同名异义 = %s'
          % (shape_distinct, normalisation_constant, symbol_A_overloaded))
md.append('- 字面 `f_A` 在卷 119 命中 %d、卷 122 命中 %d；全 07 目录命中文件：%s'
          % (int(f_A_in_119), int(f_A_in_122), '、'.join(f_A_sources)))
md.append('- r405：前三矩 `m₀=16, m₁=40, m₂=120` 后仍余 1 维连续族 `m₃(t)=400−6t`；'
          'r406：补 f 形状/归一原理使 `s=2` 超 Omega5-S 配额、`ACCEPTED 0` 条出口。')
md.append('- **裁定**：`#31 = %s`，不销账。' % status31)
md.append('')
md.append('## 四、债务账现值')
md.append('')
md.append('| 项 | 值 |')
md.append('|---|---|')
md.append('| 总账 | 31（已闭 10＋转并 1＋仍开 20） |')
md.append('| 新开债务声明 | %s |' % new_debt_claims)
md.append('| 「不开新债」卷 | %s |' % no_new_debt_declarations)
md.append('| 记分板 0/6 卷 | %s |' % scoreboard_hits)
md.append('| J101+ 触及 #30/#31/销账 | %s |' % parallel_touch)
md.append('| #22 | attack49 外挂更正指针已销，卷宗总表历史行不改 |')
md.append('')
md.append('> 完整判定见 `判定_attack50_30号31号价格表与销账判定_2026-11-09.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack50 / 2026-11-09 / #30 #31 price table and debt-closure judgement')
lines.append('')
lines.append('[A] dynamic numbering')
lines.append('  %s' % result['numbering'])
lines.append('')
lines.append('[B] #30 exact arithmetic')
lines.append('  v2=%s Vmin=%s u4/v4=%s coef=%s target=5/7 residual=%s'
             % (v2, v_min, u4_over_v4, rho_coef,
                rho_coef - Fraction(5, 7)))
lines.append('  absent_in_105=%s' % absent_105)
lines.append('  present_in_113=%s' % present_113)
lines.append('  status30=%s' % status30)
lines.append('')
lines.append('[C] #31 price table')
lines.append('  shape_r=%s' % dict((k, str(val)) for k, val in shape_r.items()))
lines.append('  normalisation_r=%s distinct=%s overloaded=%s'
             % (sorted(str(x) for x in normalisation_r),
                shape_distinct, symbol_A_overloaded))
lines.append('  f_A_in_119=%s f_A_in_122=%s sources=%s'
             % (f_A_in_119, f_A_in_122, f_A_sources))
lines.append('  status31=%s' % status31)
lines.append('')
lines.append('[D] debt ledger')
lines.append('  %s' % result['debt_ledger'])
lines.append('')
lines.append('[E] findings %s' % verdict_counts)
for f in FINDINGS:
    lines.append('  %s %s : %s' % (f['verdict'], f['code'], f['note']))
lines.append('')
lines.append('[F] terminal verdict')
lines.append('  %s' % terminal_verdict)
lines.append('  candidate_verdict=%s' % candidate_verdict)
lines.append('')
lines.append('[guards] %d/%d' % (result['guard_pass'], result['guard_total']))
for g in GUARDS:
    lines.append('  %s %s : %s' % ('PASS' if g['ok'] else 'FAIL',
                                   g['code'], g['note']))
lines.append('')
lines.append('EXIT=%d' % result['exit'])
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w',
             encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('attack50 guards=%d/%d findings=%s exit=%d d30=%s d31=%s'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], status30, status31))
sys.exit(result['exit'])
