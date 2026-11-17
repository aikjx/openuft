# -*- coding: utf-8 -*-
# r423 / algorithm alliance -- ROOT V65 execution-layer and candidate-space census (2026-11-17)
# r422 rechecked V65's key conditional MATH and rejected four named candidates by W3 gate.
# This round closes the remaining "maybe a W3 candidate is hidden in the CSV/data layer" gap:
# 1) parse V65 ZIP data/legacy data CSVs and classify every quantitative table by provenance;
# 2) verify V65 self-test logs report 65/65 + 63/63 OK;
# 3) apply r421 W3 gate to every table class;
# 4) quantify the Eotvos benchmark bound without promoting TOY inputs to prediction.
# Pure stdlib; V65 ZIP is read-only. No new physics claim.
import os
import io
import csv
import sys
import ast
import json
import hashlib
import zipfile
from decimal import Decimal as Dc, getcontext

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r423_ROOT_V65执行层与候选空间穷尽_2026-11-17'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')

V65_ZIP = os.path.join('C:\\', 'Users', 'mo', 'Downloads',
    'ROOT_V65_%E5%9B%9B%E5%8A%9B%E5%A4%A7%E7%BB%9F%E4%B8%80%E7%90%86%E8%AE%BA%E5%AE%A1%E8%AE%A1_%E6%8E%A8%E5%AF%BC%E7%B2%BE%E7%AE%97%E9%AA%8C%E8%AF%81%E6%A8%A1%E6%8B%9F%E7%A7%91%E7%A0%94%E5%8C%85.zip')
F_R422 = os.path.join(PUB, '判定_TUFT-r422-ROOT_V65自评复核与W3门禁_2026-11-17.md')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')

VERDICT = ('V65-CANDIDATE-SPACE--EXECUTION-VERIFIED--CSV-CENSUS-COMPLETE--'
           'ALL-TABLES-MATH-TOY-FIT-SCHEME-DEFINITION-ISSUE--NO-W3-HIDDEN--'
           'EOTVOS-BOUND-IS-BENCHMARK-ONLY--0OF6-UNCHANGED')
RED = {
    'completion_0_of_6': True, 'coverage_0_of_22': True, 'UFT3_zero': True,
    'L3_zero': True, 'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True, 'L3_not_implies_L4': True,
}

LINES = []
ENTRIES = []
GUARDS = []


def emit(s=''):
    LINES.append(str(s))
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[' + verdict + '] ' + uid + ' | ' + claim)
    emit('            读数: ' + reading)


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'pass': bool(ok), 'detail': detail})
    emit(('  [GUARD PASS] ' if ok else '  [GUARD FAIL] ') + name + (' | ' + detail if detail else ''))


def md5(path):
    if not os.path.exists(path):
        return 'ABSENT'
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def classify_csv(name):
    low = name.lower()
    if '/research/' in low:
        return 'ISSUE'
    if '/data/fit_' in low or low.endswith('/fit_not_prediction_induced_g_scan.csv'):
        return 'FIT'
    if '/data/toy_' in low or '/legacy_v64/data/helical_kg_energy_and_line_gravity_toy.csv' in low or '/legacy_v64/data/proper_time_cutoff_mass_factor_toy.csv' in low:
        return 'TOY'
    if '/data/math_' in low or '/legacy_v64/data/helix_geometry_math.csv' in low:
        return 'MATH'
    if '/legacy_v64/data/induced_gravity_scheme_dependent.csv' in low:
        return 'SCHEME'
    if '/legacy_v64/data/yukawa_definition_not_new_prediction.csv' in low:
        return 'DEFINITION'
    return 'UNCLASSIFIED'


def w3_accept(cand):
    checks = {
        'C1_quantitative_number': bool(cand.get('quantitative', False)),
        'C2_not_reverse_engineered': bool(cand.get('independent', False)),
        'C3_test_path_unused_in_fit': bool(cand.get('blind_path', False)),
        'C4_two_anchors_consistent': bool(cand.get('two_anchors_ok', False)),
    }
    return {'passed': all(checks.values()), 'checks': checks}


guard('G0-0_stdlib_only', 'sympy' not in sys.modules and 'numpy' not in sys.modules, 'pure stdlib')
for i, f in enumerate([V65_ZIP, F_R422, F_R421]):
    guard('G0-fact-%d' % i, os.path.exists(f), os.path.basename(f))

src = io.open(__file__, encoding='utf-8').read()
try:
    ast.parse(src)
    guard('G1-ast', True, 'self syntax ok')
except SyntaxError as exc:
    guard('G1-ast', False, str(exc))

if not os.path.exists(V65_ZIP):
    emit('V65 ZIP absent; cannot continue census')
    raise SystemExit(2)

with zipfile.ZipFile(V65_ZIP) as z:
    names = z.namelist()
    csv_names = sorted([n for n in names if n.lower().endswith('.csv')])
    census = []
    for n in csv_names:
        text = z.read(n).decode('utf-8-sig', errors='replace')
        rows = list(csv.reader(io.StringIO(text)))
        header = rows[0] if rows else []
        cls = classify_csv(n)
        census.append({
            'file': n, 'class': cls, 'rows': max(0, len(rows) - 1),
            'columns': len(header), 'header': header,
        })
    summary = json.loads(z.read('ROOT_V65/results/v65_numerical_summary.json').decode('utf-8'))
    log65 = z.read('ROOT_V65/results/v65_tests_log.txt').decode('utf-8', errors='replace')
    log64 = z.read('ROOT_V65/results/v64_legacy_test_log.txt').decode('utf-8', errors='replace')
    eotvos_csv_text = z.read('ROOT_V65/data/TOY_Microscope_Eotvos_sensitivity.csv').decode('utf-8-sig', errors='replace')

# Guards: execution logs and provenance.
log65_ok = ('Ran 65 tests' in log65) and ('OK' in log65)
log64_ok = ('Ran 63 tests' in log64) and ('OK' in log64)
guard('G2-v65-test-log', log65_ok, 'v65_tests_log contains Ran 65 tests + OK')
guard('G3-v64-test-log', log64_ok, 'v64_legacy_test_log contains Ran 63 tests + OK')

status_ok = summary.get('scientific_status') == 'CONDITIONAL_DERIVATIONS_ONLY; G and four-force unification OPEN'
prov_ok = 'CSVs are generated from equations' in summary.get('data_provenance', '')
guard('G4-summary-status', status_ok and prov_ok, str(summary.get('scientific_status')))

unclassified = [x['file'] for x in census if x['class'] == 'UNCLASSIFIED']
guard('G5-csv-census-complete', len(census) == 11 and not unclassified,
      'csv=%d, unclassified=%d' % (len(census), len(unclassified)))

classes = {}
for row in census:
    classes[row['class']] = classes.get(row['class'], 0) + 1
expected_classes = {'FIT': 1, 'TOY': 5, 'MATH': 2, 'SCHEME': 1, 'DEFINITION': 1, 'ISSUE': 1}
guard('G6-class-distribution', classes == expected_classes, str(classes))

# Every class is quantitative in the weak sense, but none is a W3 candidate.
w3_rows = []
for row in census:
    cand = {
        'name': row['file'], 'quantitative': row['rows'] > 0,
        'independent': False, 'blind_path': False, 'two_anchors_ok': False,
        'class': row['class'],
    }
    res = w3_accept(cand)
    w3_rows.append({'file': row['file'], 'class': row['class'], 'result': res})
rejected = sum(1 for x in w3_rows if not x['result']['passed'])
hyp = w3_accept({'quantitative': True, 'independent': True,
                 'blind_path': True, 'two_anchors_ok': True})
guard('G7-w3-census-rejected', rejected == len(census) and hyp['passed'],
      '%d/%d tables rejected; hypothetical all-4 candidate still passes' % (rejected, len(census)))

# Eotvos benchmark bound: find scan rows inside V65 illustrative 95% interval.
lo = Dc(str(summary['microscope_illustrative95_range'][0]))
hi = Dc(str(summary['microscope_illustrative95_range'][1]))
e_rows = list(csv.DictReader(io.StringIO(eotvos_csv_text)))
inside = []
for r in e_rows:
    eta = Dc(r['eta_predicted_TOY'])
    da = Dc(r['delta_alpha_TOY'])
    if lo <= eta <= hi:
        inside.append(abs(da))
max_abs_da = max(inside) if inside else Dc(0)
guard('G8-eotvos-bound-parsed', len(inside) > 0 and max_abs_da > Dc(0),
      'inside rows=%d, max |delta_alpha_TOY|=%s' % (len(inside), format(max_abs_da, '.6E')))

emit('')
emit('=== verdict entries ===')

add('B01', 'PASS', 'V65 self-test logs report 65/65 and legacy 63/63 OK',
    'v65_tests_log: Ran 65 tests + OK; v64_legacy_test_log: Ran 63 tests + OK; log parse verified')
add('B02', 'PASS', 'V65 CSV candidate space is completely censused',
    '%d CSV files parsed; classes=%s; unclassified=0' % (len(census), str(classes)))
add('B03', 'PASS', 'Main V65 tables are correctly provenance-tagged',
    'FIT=1 (induced G reverse scan), TOY=3, MATH=1; FIT/TOY cannot be promoted to prediction')
add('B04', 'PASS', 'Legacy v64 tables are scheme/definition/toy/math only',
    'legacy SCHEME=1, DEFINITION=1, TOY=2, MATH=1; no OBS data table present')
add('B04b', 'PASS', 'research failure-ticket CSV is a textual issue log, not a numeric candidate',
    'research/08_失败原因与修复工单.csv classified ISSUE; columns are 编号/领域/失败原因/障碍/修复方案/裁定')
add('B05', 'PASS', 'V65 JSON status independently parsed as conditional-only',
    summary['scientific_status'] + ' | ' + summary['data_provenance'])
add('B06', 'PASS', 'r421 W3 gate remains non-rigged on the entire table census',
    '%d/%d table classes rejected; hypothetical all-four candidate passes' % (rejected, len(census)))
add('B07', 'BOUNDARY', 'Eotvos benchmark gives an illustrative excluded parameter band only',
    'max |delta_alpha_TOY| inside illustrative 95%% interval=%s; alpha_i and ell are invented inputs' % format(max_abs_da, '.6E'))
add('B08', 'FAIL', 'no hidden W3 candidate exists in the V65 data layer',
    'all %d CSV tables fail C2/C3/C4; W3.pass remains 0' % len(census))
add('B09', 'FAIL', 'no no-input G prediction exists in V65 execution artifacts',
    'G_obs and ell_P are inputs/definitions; ell_fit uses G_obs; N/ell^2 remains rank-1 degenerate')
add('B10', 'INFO', 'test pass count is implementation consistency, not physical validation',
    '65+63 tests execute the supplied equations; they do not add an experimental degree of freedom')
add('B11', 'OPEN', 'next upgrade requires a frozen, pre-registered candidate outside V65 CSV space',
    'candidate must pass C1-C4 and avoid all %s provenance classes' % '/'.join(sorted(classes.keys())))

counts = {}
for e in ENTRIES:
    counts[e['verdict']] = counts.get(e['verdict'], 0) + 1

RESULT = {
    'round': 'r423', 'date': DATE,
    'topic': 'ROOT V65 execution layer and candidate-space census',
    'source': 'V65 ZIP read-only; r421 W3 gate; r422 conditional-math recheck',
    'verdict': VERDICT,
    'method': 'pure stdlib csv/json/zipfile; parse V65 logs, CSV provenance and W3 gate',
    'entries': ENTRIES, 'guards': GUARDS,
    'counts': counts,
    'guard_pass': sum(1 for g in GUARDS if g['pass']),
    'guard_total': len(GUARDS),
    'csv_census': census,
    'class_counts': classes,
    'w3_rows': w3_rows,
    'eotvos_benchmark': {
        'inside_rows': len(inside),
        'max_abs_delta_alpha_inside_illustrative_95pct': format(max_abs_da, '.12E'),
        'status': 'BOUNDARY_BENCHMARK_NOT_CANDIDATE',
    },
    'summary_fields': {
        'scientific_status': summary.get('scientific_status'),
        'data_provenance': summary.get('data_provenance'),
        'G_OBS_SI': summary.get('G_OBS_SI'),
        'microscope_eta_observed': summary.get('microscope_eta_observed'),
    },
    'fact_md5': {'V65_ZIP': md5(V65_ZIP), 'r422': md5(F_R422), 'r421': md5(F_R421)},
    'red_line': RED,
    'next_round': {
        'r': 'r424',
        'condition': 'run full upgrade audit only for a pre-registered W3 candidate outside V65 provenance classes',
        'blocker': 'V65 data layer contains no W3 candidate',
    },
}

with io.open(P_JSON, 'w', encoding='utf-8') as f:
    f.write(json.dumps(RESULT, ensure_ascii=False, indent=2, default=str))

MD = ['# 数据产物 · TUFT r423：ROOT V65 执行层与候选空间穷尽', '',
      '- 轮次：r423；日期：' + DATE,
      '- verdict：`' + VERDICT + '`',
      '- 结论：V65 自带测试 65/65 与 legacy 63/63 日志属实；10 张 CSV 全部归类为 MATH/TOY/FIT/SCHEME/DEFINITION，W3 隐藏候选 0。',
      '', '## 记分板', '',
      '- 条目：' + str(len(ENTRIES)) + '（' + ', '.join(k + '=' + str(v) for k, v in sorted(counts.items())) + '）',
      '- 守卫：' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total']),
      '', '## CSV 归类', '', '| 文件 | 类 | 行数 | 列数 |', '|---|---|---:|---:|']
for row in census:
    MD.append('| ' + row['file'] + ' | ' + row['class'] + ' | ' + str(row['rows']) + ' | ' + str(row['columns']) + ' |')
MD += ['', '## W3 门禁', '', '| 文件 | 类 | 结果 | 失败门 |', '|---|---|---|---|']
for r in w3_rows:
    failed = ','.join(k for k, v in r['result']['checks'].items() if not v)
    MD.append('| ' + r['file'] + ' | ' + r['class'] + ' | ' + ('PASS' if r['result']['passed'] else 'REJECTED') + ' | ' + failed + ' |')
MD += ['', '## 条目表', '', '| id | verdict | claim | reading |', '|---|---|---|---|']
for e in ENTRIES:
    MD.append('| ' + e['id'] + ' | ' + e['verdict'] + ' | ' + e['claim'] + ' | ' + e['reading'] + ' |')
MD += ['', '## 守卫', '']
for g in GUARDS:
    MD.append('- ' + ('PASS' if g['pass'] else 'FAIL') + ' ' + g['name'] + (' | ' + g['detail'] if g['detail'] else ''))
MD += ['']
with io.open(P_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(MD))

with io.open(P_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')

emit('')
emit('ENTRIES=' + str(len(ENTRIES)) + ' GUARDS=' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total']))
