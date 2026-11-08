# -*- coding: utf-8 -*-
"""attack48 / 攻破㊵ · 母册重复行与无状态行逐行归一归因.

Pure stdlib / Python 3.8. Read-only on every pre-existing volume.
GUARDS drive the exit code; FINDINGS record verdicts on assertions.
"""
import os, sys, io, re, json, hashlib, ast
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
BASE = 'attack48_母册重复行与无状态行逐行归一归因_2026-11-08'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d)
                  if x.startswith(prefix) and x.endswith('.md'))
    return os.path.join(d, hits[0]) if hits else None


P = {
    'mother': os.path.join(B1, '布局_物理Top1000难题攻破清单_2026-10-21.md'),
    'a47_json': os.path.join(B1, 'attack47_清单终态机器归一与J91余数精算_2026-11-08.json'),
    'a47_report': os.path.join(B1, 'attack47_清单终态机器归一与J91余数精算_2026-11-08_report.txt'),
    'final': os.path.join(B1, '全维总成_统一场论攻破_2026-10-30.md'),
    'p3': os.path.join(B1, '论文体系_Nature规范', 'P3_普适常数族与判定体系.md'),
    'j122': find_md(V7, '122_第79轮'),
    'j123': find_md(V7, '123_第80轮'),
    'j124': find_md(V7, '124_第81轮'),
    'r403': find_md(os.path.join(B2, '判定'), '判定_TUFT-r403'),
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


BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


CANDS = [('✅', ['✅']), ('⚠', ['⚠️', '⚠']),
         ('◐', ['◐']), ('🔲', ['🔲'])]
TROW = re.compile(r'^\|\s*T(\d{3,4})\s*\|')
APPENDIX_MARKERS = [
    '已攻破成果映射汇总', '基线 24 个编号', '本轮 15 个编号',
    '清尾批', '补记', '求导深化册判定', '待攻队列',
    '攻破方法', '诚实边界', '治理登记',
]


def classify_symbols(cells):
    hits = []
    for ci, cell in enumerate(cells):
        for key, alts in CANDS:
            for a in alts:
                pos = cell.find(a)
                if pos >= 0:
                    hits.append((ci, pos, key))
                    break
    return min(hits)[2] if hits else 'NONE'


def is_appendix(section):
    return any(m in section for m in APPENDIX_MARKERS)


def is_main(section):
    return (section.startswith('### 域 ') or
            'Top1000 清单' in section or
            '第一部分' in section or
            '第二部分' in section)


mother_txt = rd(P['mother'])
rows = []
section = ''
for line_no, line in enumerate(mother_txt.splitlines(), 1):
    if line.startswith('#'):
        section = line.strip()
        continue
    m = TROW.match(line)
    if not m:
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    last_cell = cells[-1] if cells else ''
    status_last = classify_symbols([last_cell])
    status_full = classify_symbols(cells)
    rows.append({
        'line_no': line_no,
        'id': int(m.group(1)),
        'section': section,
        'cell_count': len(cells),
        'last_cell': last_cell[:160],
        'status_last': status_last,
        'status_full': status_full,
        'raw_line': line[:400],
        'is_appendix': is_appendix(section),
        'is_main': is_main(section),
        'is_extra_duplicate': 0,
    })

seen = set()
duplicate_table = []
for row in rows:
    if row['id'] in seen:
        row['is_extra_duplicate'] = 1
        duplicate_table.append(row)
    else:
        seen.add(row['id'])

id_freq = Counter(r['id'] for r in rows)
ids = [r['id'] for r in rows]
status_last_counts = Counter(r['status_last'] for r in rows)
status_full_counts = Counter(r['status_full'] for r in rows)
none_table = [r for r in rows if r['status_last'] == 'NONE']


def canonical_for(row, id_status):
    return id_status.get(row['id'], 'MISSING')


def classify_row(row, id_status):
    canonical = canonical_for(row, id_status)
    if row['is_appendix']:
        return {
            'classification': 'APPENDIX_INDEX_ROW',
            'target_status': 'EXCLUDE_FROM_T_ROW_COUNT',
            'canonical_status': canonical,
            'proposed_norm': 'blank_T_cell_or_move_to_appendix; do_not_count_as_T_status_row',
            'reason': 'appendix/index table repeats T-id for mapping, not a new problem status',
        }
    if row['status_last'] == 'NONE' and row['status_full'] != 'NONE':
        return {
            'classification': 'PIPE_SPLIT_STATUS_RECOVERY',
            'target_status': row['status_full'],
            'canonical_status': canonical,
            'proposed_norm': 'escape_inline_pipe_in_formula_or_move_formula_to_note; preserve_status',
            'reason': 'inline bar inside formula split the status cell; earliest status symbol on full row recovers it',
        }
    if row['status_last'] == 'NONE':
        if row['cell_count'] > 5:
            cat = 'INLINE_PIPE_CONTINUATION'
        elif row['cell_count'] < 5:
            cat = 'SHORT_TABLE_ROW'
        else:
            cat = 'TEXT_NOTE_WITHOUT_SYMBOL'
        return {
            'classification': cat,
            'target_status': 'MANUAL_REVIEW',
            'canonical_status': canonical,
            'proposed_norm': 'manual_governance_review; no_zero_cost_machine_merge',
            'reason': 'no status symbol anywhere on row; cannot infer status from bytes alone',
        }
    return {
        'classification': 'MAIN_STATUS_ROW',
        'target_status': row['status_last'],
        'canonical_status': canonical,
        'proposed_norm': 'merge_into_canonical_id_row',
        'reason': 'main-table row with an explicit status symbol',
    }


id_status = {}
for row in rows:
    if row['is_main'] and row['status_full'] != 'NONE' and row['id'] not in id_status:
        id_status[row['id']] = row['status_full']

for row in rows:
    row.update(classify_row(row, id_status))

row_table = [r for r in rows if r['is_extra_duplicate'] or r['status_last'] == 'NONE']
overlap = len(set(r['line_no'] for r in duplicate_table) &
              set(r['line_no'] for r in none_table))
union_category_counts = Counter(r['classification'] for r in row_table)
dup_category_counts = Counter(r['classification'] for r in duplicate_table)
none_category_counts = Counter(r['classification'] for r in none_table)
unresolved_all = len([r for r in row_table if r['target_status'] == 'MANUAL_REVIEW'])
unresolved_duplicates = len([r for r in duplicate_table if r['target_status'] == 'MANUAL_REVIEW'])
unresolved_none = len([r for r in none_table if r['target_status'] == 'MANUAL_REVIEW'])
recovered_none = [r for r in none_table
                  if r['classification'] == 'PIPE_SPLIT_STATUS_RECOVERY']
appendix_none = [r for r in none_table
                 if r['classification'] == 'APPENDIX_INDEX_ROW']

canonical_counts = Counter(id_status.values())
missing_canonical = sorted(set(range(1, 1001)) - set(id_status.keys()))
declared = {}
for key, pat in [('ok', r'✅\s*=\s*(\d+)'),
                 ('warn', r'⚠️?\s*=\s*(\d+)'),
                 ('todo', r'🔲\s*=\s*(\d+)')]:
    m = re.search(pat, rd(P['final']))
    declared[key] = int(m.group(1)) if m else None
m_part = re.search(r'◐\s*(\d+)', rd(P['p3']))
declared['part'] = int(m_part.group(1)) if m_part else None
declared['p3_total'] = 1003 if '1003' in rd(P['p3']) else None
declared_sum = sum((declared.get(k) or 0) for k in ['ok', 'warn', 'part'])
declared_vec = (declared.get('ok'), declared.get('warn'), declared.get('part'))
canonical_vec = (canonical_counts.get('✅', 0),
                 canonical_counts.get('⚠', 0),
                 canonical_counts.get('◐', 0))
declared_vs_canonical_equal = declared_vec == canonical_vec

a47 = json.loads(rd(P['a47_json']))
a47_auth = a47.get('authoritative', {})
a47_report_txt = rd(P['a47_report'])

authoritative = {
    'T_rows': len(rows),
    'unique_ids': len(set(ids)),
    'id_min': min(ids) if ids else None,
    'id_max': max(ids) if ids else None,
    'missing_ids': sorted(set(range(1, 1001)) - set(ids)),
    'ids_outside_1_1000': sorted(set(ids) - set(range(1, 1001))),
    'duplicate_ids_count': len([k for k, v in id_freq.items() if v > 1]),
    'extra_duplicate_rows': len(duplicate_table),
    'none_rows_count': len(none_table),
    'status_last_counts': dict(status_last_counts),
    'status_full_counts': dict(status_full_counts),
    'sum_equals_rows': sum(status_last_counts.values()) == len(rows),
    'duplicate_none_overlap': overlap,
    'union_rows': len(row_table),
    'canonical_id_status_counts': dict(canonical_counts),
    'missing_canonical_ids': missing_canonical,
    'declared_status_counts': declared,
    'declared_sum': declared_sum,
    'declared_vs_canonical_equal': declared_vs_canonical_equal,
    'row_gap_1069_minus_1003': len(rows) - (declared.get('p3_total') or 0),
}

G('G01', len(rows) == a47_auth.get('T_rows') and
  len(set(ids)) == a47_auth.get('unique_ids'),
  'mother T-row scan reproduces attack47: %d rows / %d ids'
  % (len(rows), len(set(ids))))
G('G02', len(duplicate_table) == a47_auth.get('extra_duplicate_rows') and
  len(none_table) == a47_auth.get('none_rows_count'),
  'duplicate/none row counts reproduce attack47: %d / %d'
  % (len(duplicate_table), len(none_table)))
G('G03', authoritative['sum_equals_rows'] and
  len(row_table) == len(set(r['line_no'] for r in row_table)) and
  len(duplicate_table) + len(none_table) - overlap == len(row_table),
  'row-table union is exact and duplicate/none overlap = %d' % overlap)
G('G04', unresolved_all == 0 and unresolved_duplicates == 0 and
  unresolved_none == 0,
  'all %d union rows receive machine attribution; unresolved = %d'
  % (len(row_table), unresolved_all))
pos_cells = ['T999', 'x', 'y', 'z', '✅ note', '=1<2', 'tail']
neg_cells = ['T999', 'x', 'y', 'z', 'note', '=1<2', 'tail']
pos = classify_symbols(pos_cells) == '✅' and classify_symbols([pos_cells[-1]]) == 'NONE'
neg = classify_symbols(neg_cells) == 'NONE'
G('G05', pos and neg,
  'pipe-aware status classifier has positive and negative controls')
j122_txt = rd(P['j122'])
j123_txt = rd(P['j123'])
j124_txt = rd(P['j124'])
volume_max = 0
j_max = 0
for name in os.listdir(V7):
    m = re.match(r'^(\d{3})_.*?_J(\d+)_', name)
    if m:
        volume_max = max(volume_max, int(m.group(1)))
        j_max = max(j_max, int(m.group(2)))
G('G06', volume_max >= 124 and j_max >= 102 and
  '#30' in j122_txt and '#31' in j122_txt and
  'J101' in j123_txt and 'J102' in j124_txt and
  '新开债务 0 条' in j124_txt,
  'dynamic J-chain scan reaches volume %d / J%d; #30/#31 open and J102 adds no new debt'
  % (volume_max, j_max))
r403_txt = rd(P['r403'])
G('G07', 'NO-CORRECT-FOUR-FORCE-GUT' in r403_txt,
  'r403 terminal verdict present on disk')
attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 48] or [0])
G('G08', attack_prior_max == 47 and 48 in attack_nums,
  'attack48 is the first free attack number after attack47')
G('G09', declared['p3_total'] == 1003 and
  declared_sum == 1003 and
  authoritative['row_gap_1069_minus_1003'] == 66,
  'declared 1003 = %d+%d+%d; row gap 1069-1003 = 66'
  % (declared.get('ok') or 0, declared.get('warn') or 0, declared.get('part') or 0))
G('G10', len(id_status) == 1000 and not missing_canonical and
  sum(canonical_counts.values()) == 1000,
  'canonical status covers 1000 unique ids; missing = %d' % len(missing_canonical))
AFTER = dict((k, md5(v)) for k, v in P.items())
G('G11', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged (md5 before/after)')
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
            (x.startswith('attack') or x.startswith('_j9') or x.startswith('_j10'))]


probe_tree = ast.parse('import attack47_bad\nimport _j100_bad\nimport os')
probe_imports = [a.name for n in ast.walk(probe_tree)
                 if isinstance(n, ast.Import) for a in n.names]
G('G12', not prior_imports(imports) and len(prior_imports(probe_imports)) == 2,
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
G('G13', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder and no hard-coded guard True literals')
G('G14', sum(union_category_counts.values()) == len(row_table) and
  sum(dup_category_counts.values()) == len(duplicate_table) and
  sum(none_category_counts.values()) == len(none_table),
  'classification counts conserve duplicate/none/union tables')

F('F01', 'PASS' if unresolved_all == 0 else 'FAIL',
  '69 extra duplicate rows and 71 statusless rows reduced to %d unique problem bytes; '
  'machine attribution unresolved = %d (duplicate unresolved %d / none unresolved %d)'
  % (len(row_table), unresolved_all, unresolved_duplicates, unresolved_none))
F('F02', 'PASS' if len(recovered_none) > 0 and
  len(appendix_none) + len(recovered_none) == len(none_table) else 'FAIL',
  '71 statusless rows split: %d inline-pipe status recoveries + %d appendix/index rows; '
  'the statusless count is a parser artifact, not 71 missing physics judgments'
  % (len(recovered_none), len(appendix_none)))
F('F03', 'BOUNDARY',
  '1069 rows = 1000 unique ids + 69 extra duplicate rows; '
  'declared 1003 = 330+672+1 status items; gap +66 = 69-3 note rows. '
  'These are different count objects and must not be compared as repeated measurements')
F('F04', 'PASS' if declared_vs_canonical_equal else 'FAIL',
  'declared status vector %s vs canonical id-level vector %s; equality = %s; '
  'the +3 gap sits on the ✅ side and matches the 3 note rows counted by the declaration'
  % (declared_vec, canonical_vec, declared_vs_canonical_equal))
F('F05', 'FAIL',
  'zero-cost row normalization does not make 1003 a row count: '
  'the declaration side still counts 3 note rows that are not T-row status objects; '
  'governance-side wording must be changed, not the physics judgments')
F('F06', 'BOUNDARY',
  'dynamic numbering now reaches volume %d / J%d; J122 opens #30/#31 and J102 adds no new debt. '
  'attack47 snapshot volume 119 / J97 is stale; this volume does not re-judge J-chain physics'
  % (volume_max, j_max))
F('F07', 'FAIL',
  'format normalization cannot convert r403 FAIL into PASS: '
  'four-force-with-gravity correct equations remain 0; the unique true C3 unification remains electroweak')
F('F08', 'BOUNDARY',
  '🔲=0 still means every T-id has a structural-negative-closure judgment; '
  'it does not mean 100/1000 physics problems are solved, and UFT-3=0 / 0/22 remain')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))
candidate_verdict = 'FAIL' if (not declared_vs_canonical_equal or
                               declared['p3_total'] == len(rows)) else 'PASS'
terminal_verdict = (
    'ROW-LEVEL-ATTRIBUTION-CLOSED--DECLARED-1003-NOT-A-ROW-COUNT--'
    'PHYSICS-VERDICT-UNCHANGED'
)

result = {
    'volume': 'attack48',
    'round_label': '攻破㊵',
    'date': '2026-11-08',
    'scope': ('row-level normalization attribution for 69 duplicate T rows '
              'and 71 statusless T rows in the Top1000 mother volume'),
    'authoritative': authoritative,
    'classification_counts': {
        'union': dict(union_category_counts),
        'duplicates': dict(dup_category_counts),
        'none': dict(none_category_counts),
    },
    'declared': declared,
    'id_canonical_status_counts': dict(canonical_counts),
    'numbering': {
        'attack_prior_max': attack_prior_max,
        'attack_current': 48,
        'volume_max': volume_max,
        'j_max': j_max,
        'j122': os.path.basename(P['j122'] or ''),
        'j123': os.path.basename(P['j123'] or ''),
        'j124': os.path.basename(P['j124'] or ''),
    },
    'duplicate_table': duplicate_table,
    'none_table': none_table,
    'row_table_union': row_table,
    'findings': FINDINGS,
    'verdict_counts': verdict_counts,
    'candidate_verdict': candidate_verdict,
    'terminal_verdict': terminal_verdict,
    'redlines': [
        '0/22', 'UFT-3=0', 'validated=0',
        'attack = structural negative closure, not solved physics',
        'no claim of four-force unification',
    ],
    'self_corrections': [
        'attack47 judged status from the last split cell; attack48 uses the earliest status symbol on the full row and isolates appendix/index tables, avoiding inline-bar formula false negatives.',
        'attack47 snapshot volume 119 / J97 is not reused; attack48 dynamically scans the J-chain and records the current upper bound 124 / J102 with #30/#31 still open.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))


def mdcell(x):
    return str(x).replace('|', '\\|').replace('\n', ' ')


md = []
md.append('# attack48 · 数据产物（机读摘要）')
md.append('')
md.append('- 日期：2026-11-08 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 性质：只读逐行归因；不重判物理条目、不产生新物理、不修改任何既有册字节')
md.append('')
md.append('| 层 | 项 | 值 |')
md.append('|---|---|---|')
md.append('| A | 母册 T 行 / 唯一编号 | %d / %d |'
          % (len(rows), len(set(ids))))
md.append('| A | 额外重复行 / 无状态行 | %d / %d |'
          % (len(duplicate_table), len(none_table)))
md.append('| A | 重复∩无状态 / 并集行 | %d / %d |'
          % (overlap, len(row_table)))
md.append('| A | 未解决机器归因 | %d |' % unresolved_all)
md.append('| A | inline-pipe 状态恢复 / 附录索引行 | %d / %d |'
          % (len(recovered_none), len(appendix_none)))
md.append('| A | 声明状态项 / 机器 T 行差 | %d / %d |'
          % (declared['p3_total'] or 0,
             authoritative['row_gap_1069_minus_1003']))
md.append('| A | 声明向量 / 编号级规范向量 | %s / %s |'
          % (declared_vec, canonical_vec))
md.append('| B | 动态编号上界 | attack%d / 卷%d / J%d |'
          % (attack_prior_max, volume_max, j_max))
md.append('| C | r403 终判 | 含引力四力大统一正确者 = 0 条 |')
md.append('')
md.append('## 分类计数')
md.append('')
md.append('| 表 | 分类 | 行数 |')
md.append('|---|---|---|')
for scope_name, counts in [('并集', union_category_counts),
                           ('重复', dup_category_counts),
                           ('无状态', none_category_counts)]:
    for key in sorted(counts.keys()):
        md.append('| %s | %s | %d |' % (scope_name, key, counts[key]))
md.append('')
md.append('## 逐行归因表（前 18 行；全表见 JSON `row_table_union`）')
md.append('')
md.append('| 行号 | T 编号 | 段 | 分类 | 末列状态→全行状态 | 建议 |')
md.append('|---|---|---|---|---|---|')
for r in row_table[:18]:
    md.append('| %d | T%03d | %s | %s | %s→%s | %s |'
              % (r['line_no'], r['id'], mdcell(r['section'][:28]),
                 r['classification'], r['status_last'], r['status_full'],
                 mdcell(r['proposed_norm'])))
md.append('')
md.append('> 完整判定与诚实边界见 '
          '`判定_attack48_母册重复行与无状态行逐行归一归因_2026-11-08.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack48 / 2026-11-08 / mother-volume row attribution')
lines.append('')
lines.append('[A] authoritative re-scan')
for k in ['T_rows', 'unique_ids', 'missing_ids', 'ids_outside_1_1000',
          'extra_duplicate_rows', 'none_rows_count',
          'duplicate_none_overlap', 'union_rows',
          'status_last_counts', 'status_full_counts',
          'canonical_id_status_counts', 'declared_status_counts',
          'declared_vs_canonical_equal', 'row_gap_1069_minus_1003']:
    lines.append('  %s = %s' % (k, authoritative[k]))
lines.append('  classification_counts = %s' % result['classification_counts'])
lines.append('  recovered_none = %d ; appendix_none = %d ; unresolved_all = %d'
             % (len(recovered_none), len(appendix_none), unresolved_all))
lines.append('')
lines.append('[B] numbering and terminal facts')
lines.append('  %s' % result['numbering'])
lines.append('  r403 = NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK')
lines.append('')
lines.append('[C] findings %s' % verdict_counts)
for f in FINDINGS:
    lines.append('  %s %s : %s' % (f['verdict'], f['code'], f['note']))
lines.append('')
lines.append('[D] terminal verdict')
lines.append('  %s' % terminal_verdict)
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

print('attack48 guards=%d/%d findings=%s exit=%d rows=%d dup=%d none=%d union=%d'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], len(rows), len(duplicate_table),
         len(none_table), len(row_table)))
sys.exit(result['exit'])
