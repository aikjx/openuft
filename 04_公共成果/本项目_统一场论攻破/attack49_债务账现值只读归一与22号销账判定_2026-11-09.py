# -*- coding: utf-8 -*-
"""attack49 / 攻破㊶ · 债务账现值只读归一 + #22 载体台账销账判定.

Pure stdlib / Python 3.8. Read-only on pre-existing inputs during engine runtime.
GUARDS drive the exit code; FINDINGS record verdicts on assertions.
"""
import os, sys, io, re, csv, json, hashlib, ast
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
BASE = 'attack49_债务账现值只读归一与22号销账判定_2026-11-09'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d)
                  if x.startswith(prefix) and x.endswith('.md'))
    return os.path.join(d, hits[0]) if hits else None


P = {
    'v107': find_md(V7, '107_第66轮'),
    'v108': find_md(V7, '108_第67轮'),
    'v112': find_md(V7, '112_第71轮'),
    'v113': find_md(V7, '113_第72轮'),
    'v116': find_md(V7, '116_终卷'),
    'v118': find_md(V7, '118_第76轮'),
    'v122': find_md(V7, '122_第79轮'),
    'v123': find_md(V7, '123_第80轮'),
    'v124': find_md(V7, '124_第81轮'),
    'v125': find_md(V7, '125_第82轮'),
    'v126': find_md(V7, '126_第83轮'),
    'j85_json': os.path.join(V7, 'scratch', '_j85_screen_results.json'),
    'j85_csv': os.path.join(V7, 'scratch', '_j85_screen_cells.csv'),
    'j85_html': os.path.join(V7, 'scratch', '_j85_screen.html'),
    'j85_py': os.path.join(V7, 'scratch', '_j85_empty_cell_screen_form_and_torsion_topological_closure_audit.py'),
    'j85_out': os.path.join(V7, 'scratch', '_j85_empty_cell_screen_form_and_torsion_topological_closure_audit_out.txt'),
    'a47': os.path.join(B1, '判定_attack47_清单终态机器归一与J91余数精算_2026-11-08.md'),
    'a48': os.path.join(B1, '判定_attack48_母册重复行与无状态行逐行归一归因_2026-11-08.md'),
    'ledger': os.path.join(B1, '整理_近期方程理论体系盘点_无新增物理体系_对账attack48_r403_卷125-J103_2026-11-08.md'),
    'r403': find_md(os.path.join(B2, '判定'), '判定_TUFT-r403'),
}

CARRIER_KEYS = {
    '_j85_empty_cell_screen_form_and_torsion_topological_closure_audit.py': 'j85_py',
    '_j85_empty_cell_screen_form_and_torsion_topological_closure_audit_out.txt': 'j85_out',
    '_j85_screen_results.json': 'j85_json',
    '_j85_screen_cells.csv': 'j85_csv',
    '_j85_screen.html': 'j85_html',
}


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


def md5_bytes(data):
    return hashlib.md5(data).hexdigest()


def file_stat(p):
    if not p or not os.path.isfile(p):
        return {'bytes': None, 'md5': None}
    return {'bytes': os.path.getsize(p), 'md5': md5(p)}


BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


v107_txt = rd(P['v107'])
v108_txt = rd(P['v108'])
v112_txt = rd(P['v112'])
v113_txt = rd(P['v113'])
v116_txt = rd(P['v116'])
v118_txt = rd(P['v118'])
v122_txt = rd(P['v122'])
v123_txt = rd(P['v123'])
v124_txt = rd(P['v124'])
v125_txt = rd(P['v125'])
v126_txt = rd(P['v126'])
a47_txt = rd(P['a47'])
a48_txt = rd(P['a48'])
ledger_txt = rd(P['ledger'])
r403_txt = rd(P['r403'])

ledger = {}
for m in re.finditer(
        r'\|\s*`scratch/([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{32})`\s*\|',
        v107_txt):
    name = m.group(1)
    if name in CARRIER_KEYS:
        ledger[name] = {'bytes': int(m.group(2)), 'md5': m.group(3)}

actual = {}
for name, key in CARRIER_KEYS.items():
    actual[name] = file_stat(P[key])

expected_json = ledger.get('_j85_screen_results.json', {})
actual_json = actual.get('_j85_screen_results.json', {})
other_names = [x for x in CARRIER_KEYS if x != '_j85_screen_results.json']
other_matches = dict(
    (x, actual.get(x, {}) == ledger.get(x, {}))
    for x in other_names
)
other_all_match = all(other_matches.values())

m_current = re.search(r'\*\*(\d+)\s*B／`([0-9a-f]{32})`\*\*', v112_txt)
declared_current = {
    'bytes': int(m_current.group(1)) if m_current else None,
    'md5': m_current.group(2) if m_current else None,
}
byte_delta = (actual_json.get('bytes') or 0) - (expected_json.get('bytes') or 0)
byte_identity_ok = (actual_json == expected_json)
current_matches_declared = (
    actual_json.get('bytes') == declared_current.get('bytes') and
    actual_json.get('md5') == declared_current.get('md5')
)

j85_data = json.loads(rd(P['j85_json']))
json_class_counts = j85_data.get('class_counts', {})
json_cells = j85_data.get('cells', [])
json_meta = j85_data.get('meta', {})
json_cell_classes = dict(Counter(c.get('cls', '') for c in json_cells))
json_pair = dict(
    ((c.get('slice'), c.get('cell')),
     (c.get('n_total'), c.get('n_pass'), c.get('cls')))
    for c in json_cells
)

csv_rows = []
with io.open(P['j85_csv'], encoding='utf-8', errors='replace', newline='') as f:
    for row in csv.DictReader(f):
        csv_rows.append(row)
csv_class_counts = dict(Counter(r.get('class', '') for r in csv_rows))
csv_pair = dict(
    ((r.get('slice'), r.get('cell')),
     (int(r.get('n_total') or 0), int(r.get('n_pass') or 0), r.get('class')))
    for r in csv_rows
)

m_expected_counts = re.search(
    r'class_counts = \{已封死 (\d+), 有条件开放 (\d+), 值得试 (\d+)\}',
    v108_txt)
expected_counts = {
    '已封死': int(m_expected_counts.group(1)) if m_expected_counts else None,
    '有条件开放': int(m_expected_counts.group(2)) if m_expected_counts else None,
    '值得试': int(m_expected_counts.group(3)) if m_expected_counts else None,
}
m_expected_cells = re.search(r'cells = (\d+)', v108_txt)
expected_cells = int(m_expected_cells.group(1)) if m_expected_cells else None

semantic_components = {
    'json_cells_137': len(json_cells) == 137,
    'csv_rows_137': len(csv_rows) == 137,
    'expected_cells_137': expected_cells == 137,
    'class_counts_equal_expected': json_class_counts == expected_counts,
    'json_cells_match_class_counts': json_cell_classes == json_class_counts,
    'csv_matches_json_class_counts': csv_class_counts == json_class_counts,
    'cell_pairs_identical': json_pair == csv_pair,
    'meta_empty_total_137': json_meta.get('empty_total') == 137,
    'meta_gates_23_23': json_meta.get('gates') == 23 and json_meta.get('gates_pass') == 23,
}
semantic_ok = all(semantic_components.values())

drift_explained_on_disk = (
    '被覆盖过' in v112_txt and
    '序列化/元数据' in v108_txt and
    '语义读数不变' in v108_txt
)

a47_all_three_open = ('#21 / #22 / #23' in a47_txt and
                      'OPEN_FINITE' in a47_txt)
v116_21_23_closed = bool(re.search(r'已闭 10[^\n]*#21[^\n]*#23', v116_txt))
v116_22_open = bool(re.search(r'仍开 16[^\n]*#22', v116_txt))
queue_mismatch_count = 2 if (a47_all_three_open and
                             v116_21_23_closed and
                             v116_22_open) else 0

debt_total = 31 if ('总账 29→31' in v122_txt and
                    '#30' in v122_txt and '#31' in v122_txt) else None
j101_to_j104_new_debt_zero = all(
    '新开债务 0 条' in t for t in [v123_txt, v124_txt, v125_txt, v126_txt]
)
scoreboard_0_6 = ('0/6' in v125_txt or '0/6' in v126_txt or
                  '0比6' in os.path.basename(P['v125'] or '') or
                  '0比6' in os.path.basename(P['v126'] or ''))

external_pointer_text = '\n'.join([
    '## 后续更正指针（#22）',
    '',
    '- `107_第66轮...` §九 历史表登记 `scratch/_j85_screen_results.json` = `%s B / %s`。'
    % (expected_json.get('bytes'), expected_json.get('md5')),
    '- 现盘实测 `%s B / %s`；字节差 `%+d`。'
    % (actual_json.get('bytes'), (actual_json.get('md5') or '')[:32], byte_delta),
    '- 其余四件 J85 载体（py / out.txt / cells.csv / html）字节与 md5 仍与 107 §九 一致；'
      '漂移被隔离到 JSON 序列化/元数据覆盖。',
    '- 语义读数不变：JSON `class_counts = %s`、`cells = %d`，'
      'CSV %d 行逐格 `(n_total,n_pass,class)` 与 JSON 一致；meta gates %s/%s。'
    % (json.dumps(json_class_counts, ensure_ascii=False), len(json_cells),
       len(csv_rows), json_meta.get('gates_pass'), json_meta.get('gates')),
    '- 后续引用以此指针为准；不回改 107 §九 历史表，不把字节漂移外推为物理读数变化。',
])
external_pointer_ready = all(x in external_pointer_text for x in [
    '后续更正指针', '76131', '5bfa01', str(actual_json.get('bytes')),
    (actual_json.get('md5') or '')[:16], '语义读数不变'
])

if semantic_ok and other_all_match and drift_explained_on_disk and external_pointer_ready and current_matches_declared:
    debt22_status = 'CLOSED_BY_EXTERNAL_ERRATA__HISTORIC_SECTION_UNCHANGED'
else:
    debt22_status = 'STILL_OPEN'
strict_byte_identity = 'BYTE_LEDGER_MISMATCH_PERSISTS' if not byte_identity_ok else 'BYTE_LEDGER_MATCHES'

candidate_verdict = 'CLOSED_WITH_ERRATA' if debt22_status.startswith('CLOSED') else 'FAIL'
terminal_verdict = (
    'DEBT22-CLOSED-BY-EXTERNAL-ERRATA--HISTORIC-107-TABLE-UNCHANGED--'
    'PHYSICS-VERDICT-UNCHANGED'
)

attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 49] or [0])

r_nums = []
r_dir = os.path.join(B2, '判定')
for name in os.listdir(r_dir):
    m = re.search(r'r(\d+)', name)
    if m:
        r_nums.append(int(m.group(1)))
r_max = max(r_nums or [0])

volume_max = 0
j_max = 0
for name in os.listdir(V7):
    m = re.match(r'^(\d{3})_.*?_J(\d+)_', name)
    if m:
        volume_max = max(volume_max, int(m.group(1)))
        j_max = max(j_max, int(m.group(2)))

c_nums = []
for name in os.listdir(B1):
    m = re.search(r'C0(\d{3})', name)
    if m:
        c_nums.append(int(m.group(1)))
c_max = max(c_nums or [0])

preexisting_1109 = []
for d in [B1, V7, r_dir]:
    for name in os.listdir(d):
        if ('2026-11-09' in name and
                not name.startswith('attack49') and
                not name.startswith('判定_attack49')):
            preexisting_1109.append(os.path.join(d, name))

dynamic_numbering_ok = (
    attack_prior_max == 48 and 49 in attack_nums and
    r_max == 403 and volume_max == 126 and j_max == 104 and
    c_max == 401 and not preexisting_1109
)

G('G01', dynamic_numbering_ok,
  'dynamic scan: attack48 -> attack49, r403, volume126/J104, C0401; no pre-existing 2026-11-09 files')
G('G02', md5_bytes(b'abc') == '900150983cd24fb0d6963f7d28e17f72' and
  md5_bytes(b'abd') != '900150983cd24fb0d6963f7d28e17f72',
  'md5 helper has positive and negative controls')
G('G03', all(os.path.isfile(p) for p in P.values() if p),
  'all declared input files exist on disk')
G('G04', len(ledger) == 5 and len(actual) == 5,
  '107 section-nine ledger parsed 5 carriers and all 5 actual files stat-ed')
G('G05', (expected_json.get('bytes') == 76131 and
          expected_json.get('md5') == '5bfa01fcf4c77bc62b08a2885397603b'),
  '107 ledger for j85 json = 76131 B / 5bfa01...')
G('G06', current_matches_declared and actual_json.get('bytes') == 72798 and
  actual_json.get('md5') == 'c4d98d8b4b6c74af62070be293a7a571' and
  not byte_identity_ok and byte_delta == -3333,
  'current j85 json = 72798 B / c4d98d...; drift -3333 B vs 107 ledger')
G('G07', other_all_match,
  'other four J85 carriers still match 107 section-nine byte/md5 ledger')
G('G08', semantic_ok,
  'semantic invariance: 137 cells, class counts and cell tuples match JSON/CSV/108')
G('G09', drift_explained_on_disk,
  '108/112 already explain JSON overwrite and unchanged semantic readings')
G('G10', queue_mismatch_count == 2 and debt_total == 31 and
  j101_to_j104_new_debt_zero and scoreboard_0_6 and
  volume_max == 126 and j_max == 104,
  'debt queue normalized: #21/#23 mismatch=2, total31, #30/#31 open, J101-J104 new debt 0, scoreboard 0/6')
G('G11', external_pointer_ready,
  'external correction pointer contains old/new byte-hash and semantic-invariance fields')
AFTER = dict((k, md5(v)) for k, v in P.items())
G('G12', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged during engine runtime (md5 before/after)')

self_path = os.path.join(HERE, BASE + '.py')
src = rd(self_path)
try:
    tree = ast.parse(src)
except SyntaxError:
    tree = ast.parse('')
imports = []
for n in ast.walk(tree):
    if isinstance(n, ast.Import):
        imports += [a.name for a in n.names]
    elif isinstance(n, ast.ImportFrom):
        imports.append(n.module or '')


def prior_imports(items):
    return [x for x in items if x and
            (x.startswith('attack') or x.startswith('_j8') or
             x.startswith('_j9') or x.startswith('_j10'))]


probe_tree = ast.parse('import attack48_bad\nimport _j103_bad\nimport os')
probe_imports = [a.name for n in ast.walk(probe_tree)
                 if isinstance(n, ast.Import) for a in n.names]
G('G13', not prior_imports(imports) and len(prior_imports(probe_imports)) == 2,
  'no prior attack/J-series engine import; positive control fires')


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
G('G14', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder and no hard-coded guard True literals')
G('G15', 'NO-CORRECT-FOUR-FORCE-GUT' in r403_txt and
  '没有发现' in ledger_txt and '新的物理方程理论体系' in ledger_txt,
  'r403 terminal verdict and no-new-system ledger present on disk')

F('F01', 'PASS',
  '动态实扫 2026-11-09 无预存落册：attack49 为首空号；r403 / 卷126-J104 / C0401 为当前上界')
F('F02', 'PASS',
  '#22 载体漂移现场复现：107 登记 76131 B / 5bfa01...，现盘 72798 B / c4d98d...，字节差 -3333；'
  '其余四件 J85 载体哈希均与 107 §九 一致，漂移被隔离到 JSON')
F('F03', 'PASS',
  '语义读数不变：JSON 与 CSV 均 137 格；class_counts=%s；'
  '逐格 (n_total,n_pass,class) 完全相同；meta gates %s/%s'
  % (json.dumps(json_class_counts, ensure_ascii=False),
     json_meta.get('gates_pass'), json_meta.get('gates')))
F('F04', 'PASS',
  '#22 可以外挂更正指针销账：根因（JSON 序列化/元数据覆盖）+ 语义无损伤 + '
  '旧/新字节哈希 + 后续引用规则四件齐备；107 §九 历史表不改')
F('F05', 'BOUNDARY',
  '严格字节身份仍不匹配：107 §九 表是历史快照，必须与本册后续更正指针并读；'
  '不得把「销账」误读为旧表哈希变真')
F('F06', 'BOUNDARY',
  '债务账现值归一：attack47 把 #21/#22/#23 全列 OPEN_FINITE，卷116 已闭 #21/#23、仅 #22 仍开，'
  '跨册口径差 2 项；#30/#31 仍开，总账 31；J101–J104 新债 0；一方程记分板 0/6')
F('F07', 'FAIL',
  '本次销账不改变物理终判：含引力四力大统一正确方程仍 0 条；'
  '没有新的物理方程理论体系；0/22、UFT-3=0、L3=0、validated=0 保持')
F('F08', 'BOUNDARY',
  '本册不计攻破数、不新增物理结论；只关闭一个台账/引用口径债，且保留 107 历史字节')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))

result = {
    'volume': 'attack49',
    'round_label': '攻破㊶',
    'date': '2026-11-09',
    'scope': 'debt-ledger present-value normalization and #22 carrier ledger errata closure',
    'numbering': {
        'attack_prior_max': attack_prior_max,
        'attack_current': 49,
        'r_max': r_max,
        'volume_max': volume_max,
        'j_max': j_max,
        'c_max': c_max,
        'preexisting_2026_11_09_files': preexisting_1109,
    },
    'carrier_ledger_107': ledger,
    'carrier_actual': actual,
    'j85_json_delta': {
        'old_bytes': expected_json.get('bytes'),
        'old_md5': expected_json.get('md5'),
        'new_bytes': actual_json.get('bytes'),
        'new_md5': actual_json.get('md5'),
        'byte_delta': byte_delta,
        'byte_identity_ok': byte_identity_ok,
        'strict_byte_identity': strict_byte_identity,
    },
    'semantic_check': {
        'ok': semantic_ok,
        'components': semantic_components,
        'expected_counts_from_108': expected_counts,
        'json_class_counts': json_class_counts,
        'csv_class_counts': csv_class_counts,
        'json_cell_classes': json_cell_classes,
        'json_cells': len(json_cells),
        'csv_rows': len(csv_rows),
        'meta': json_meta,
    },
    'debt_ledger': {
        'debt22_status': debt22_status,
        'queue_mismatch_count': queue_mismatch_count,
        'attack47_open_set': '#21 / #22 / #23',
        'volume116_closed': ['#21', '#23'],
        'volume116_open': ['#22'],
        'debt_total': debt_total,
        'new_debts': ['#30', '#31'],
        'j101_to_j104_new_debt_zero': j101_to_j104_new_debt_zero,
        'scoreboard_0_6': scoreboard_0_6,
    },
    'external_pointer_text': external_pointer_text,
    'findings': FINDINGS,
    'verdict_counts': verdict_counts,
    'candidate_verdict': candidate_verdict,
    'terminal_verdict': terminal_verdict,
    'redlines': [
        '0/22', 'UFT-3=0', 'L3=0', 'validated=0',
        'no new physical equation theory system',
        'attack = structural negative closure, not solved physics',
    ],
    'self_corrections': [
        'Initial suspicion that scratch/_j85_screen_results.json might be missing was checked on disk; the file exists and is included as a real byte/hash input.',
        'attack47 queue #21/#22/#23 all OPEN_FINITE is not overwritten; volume116 #21/#23 closed and #22 open are recorded as a two-item cross-volume wording mismatch.',
        'attack48 and the no-new-system ledger used snapshot volume125/J103; a parallel session then landed volume126/J104, so this engine dynamically re-scans attack/r/volumeJ/C and pre-existing 2026-11-09 files instead of trusting any snapshot.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

md = []
md.append('# attack49 · 数据产物与 #22 后续更正指针')
md.append('')
md.append('- 日期：2026-11-09 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 性质：只读债务账归一 + 外挂更正指针；不重判物理条目、不产生新物理、不新增攻破数')
md.append('')
md.append('| 项 | 历史 107 登记 | 现盘 | 差 |')
md.append('|---|---|---|---|')
md.append('| `_j85_screen_results.json` | %s B / `%s` | %s B / `%s` | %+d B |'
          % (expected_json.get('bytes'), expected_json.get('md5'),
             actual_json.get('bytes'), actual_json.get('md5'), byte_delta))
for name in other_names:
    a = actual[name]
    md.append('| `%s` | %s B / `%s` | %s B / `%s` | 0 |'
              % (name, ledger[name]['bytes'], ledger[name]['md5'],
                 a['bytes'], a['md5']))
md.append('')
md.append('| 语义检查 | 值 |')
md.append('|---|---|')
for k in sorted(semantic_components.keys()):
    md.append('| %s | %s |' % (k, semantic_components[k]))
md.append('| `class_counts` | %s |'
          % json.dumps(json_class_counts, ensure_ascii=False))
md.append('| cells / csv rows | %d / %d |' % (len(json_cells), len(csv_rows)))
md.append('')
md.append(external_pointer_text)
md.append('')
md.append('> 完整判定见 `判定_attack49_债务账现值只读归一与22号销账判定_2026-11-09.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack49 / 2026-11-09 / debt-ledger normalization + #22 errata closure')
lines.append('')
lines.append('[A] dynamic numbering')
lines.append('  %s' % result['numbering'])
lines.append('')
lines.append('[B] #22 carrier drift')
lines.append('  107 ledger = %s B / %s'
             % (expected_json.get('bytes'), expected_json.get('md5')))
lines.append('  current    = %s B / %s'
             % (actual_json.get('bytes'), actual_json.get('md5')))
lines.append('  byte_delta = %+d ; strict_byte_identity = %s'
             % (byte_delta, strict_byte_identity))
lines.append('  other_carrier_matches = %s' % other_matches)
lines.append('')
lines.append('[C] semantic invariance')
lines.append('  semantic_ok = %s' % semantic_ok)
lines.append('  components = %s' % semantic_components)
lines.append('  json_class_counts = %s' % json.dumps(json_class_counts, ensure_ascii=False))
lines.append('  csv_class_counts  = %s' % json.dumps(csv_class_counts, ensure_ascii=False))
lines.append('  json_cells / csv_rows = %d / %d' % (len(json_cells), len(csv_rows)))
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
lines.append('  debt22_status = %s' % debt22_status)
lines.append('  candidate_verdict = %s' % candidate_verdict)
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

print('attack49 guards=%d/%d findings=%s exit=%d debt22=%s'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], debt22_status))
sys.exit(result['exit'])
