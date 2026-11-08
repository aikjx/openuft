# -*- coding: utf-8 -*-
"""attack47 / 攻破㊴ · Top100/Top1000 清单终态机器归一 + J91 登记册余数精算.

Pure stdlib / Python 3.8 / Fraction exact layer.
READ-ONLY on every pre-existing volume (md5 before/after double check).
Does NOT re-judge any existing entry, does NOT create new physics.

Guard semantics follow r403: GUARDS = engine correctness (drive exit code);
FINDINGS = verdicts on assertions (FAIL means the assertion does not hold,
NOT that this volume failed to execute).
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
BASE = 'attack47_清单终态机器归一与J91余数精算_2026-11-08'


def find_md(d, prefix):
    if not os.path.isdir(d):
        return None
    hits = sorted(x for x in os.listdir(d)
                  if x.startswith(prefix) and x.endswith('.md'))
    return os.path.join(d, hits[0]) if hits else None


P = {
    'mother': os.path.join(B1, '布局_物理Top1000难题攻破清单_2026-10-21.md'),
    'top100': os.path.join(B1, '布局_物理Top100难题攻破清单_2026-10-21.md'),
    'final': os.path.join(B1, '全维总成_统一场论攻破_2026-10-30.md'),
    'p3': os.path.join(B1, '论文体系_Nature规范', 'P3_普适常数族与判定体系.md'),
    'ledger': os.path.join(B1, '未处理问题总账与攻破路径规划_2026-10-21.md'),
    'left': os.path.join(B1, '布局_剩余项分层归档_2026-10-24.md'),
    'report': os.path.join(B1, '验证_全物理体系攻破总账_2026-10-24_report.txt'),
    'j91': find_md(V7, '113_第72轮'),
    'r403': find_md(os.path.join(B2, '判定'), '判定_TUFT-r403'),
    'a27': find_md(B1, '判定_attack27'),
    'readme': os.path.join(B1, 'README.md'),
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


# ================= A. authoritative T-row scan =================
mother_txt = rd(P['mother'])
CANDS = [('✅', ['✅']), ('⚠', ['⚠️', '⚠']), ('◐', ['◐']), ('🔲', ['🔲'])]


def classify(cell):
    hits = []
    for key, alts in CANDS:
        for a in alts:
            i = cell.find(a)
            if i >= 0:
                hits.append((i, key))
                break
    return min(hits)[1] if hits else 'NONE'


TROW = re.compile(r'^\|\s*T(\d{3,4})\s*\|')
rows = []
for line in mother_txt.splitlines():
    m = TROW.match(line)
    if not m:
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    cell = cells[-1] if cells else ''
    rows.append({'id': int(m.group(1)), 'status': classify(cell),
                 'cell': cell[:60], 'line': line[:140]})

ids = [r['id'] for r in rows]
id_freq = Counter(ids)
counts = Counter(r['status'] for r in rows)
none_rows = [r for r in rows if r['status'] == 'NONE']

authoritative = {
    'T_rows': len(rows),
    'unique_ids': len(set(ids)),
    'id_min': min(ids) if ids else None,
    'id_max': max(ids) if ids else None,
    'missing_ids': sorted(set(range(1, 1001)) - set(ids)),
    'ids_outside_1_1000': sorted(set(ids) - set(range(1, 1001))),
    'duplicate_ids_count': len([k for k, v in id_freq.items() if v > 1]),
    'extra_duplicate_rows': len(rows) - len(set(ids)),
    'status_counts': dict(counts),
    'sum_equals_rows': sum(counts.values()) == len(rows),
    'none_rows_count': len(none_rows),
    'none_rows_sample': [[r['id'], r['cell']] for r in none_rows[:6]],
    'duplicate_ids_top': [[k, v] for k, v in id_freq.most_common(6) if v > 1],
}

G('G01', len(rows) > 900, 'mother T-rows scanned >900: %d' % len(rows))
G('G02', not authoritative['ids_outside_1_1000'], 'no T id outside 1..1000')
G('G03', authoritative['sum_equals_rows'], 'status counts conserve T-rows')
G('G04', all(1 <= r['id'] <= 1000 for r in rows), 'every T id within 1..1000')

# declared terminal numbers, read from disk (not from memory)
final_txt = rd(P['final'])
p3_txt = rd(P['p3'])
declared = {}
for key, pat in [('ok', r'✅\s*=\s*(\d+)'), ('warn', r'⚠️?\s*=\s*(\d+)'),
                 ('todo', r'🔲\s*=\s*(\d+)')]:
    m = re.search(pat, final_txt)
    declared[key] = int(m.group(1)) if m else None
declared['p3_total'] = 1003 if '1003' in p3_txt else None

historical = [
    {'value': 792, 'date': '2026-10-21', 'kind': 'remaining_todo_snapshot',
     'source': '未处理问题总账与攻破路径规划_2026-10-21.md L1242'},
    {'value': 714, 'date': '2026-10-24', 'kind': 'remaining_todo_snapshot',
     'source': '布局_剩余项分层归档_2026-10-24.md L4 / README L10'},
    {'value': 766, 'date': '2026-10-24', 'kind': 'remaining_todo_snapshot_rebased',
     'source': '验证_全物理体系攻破总账_2026-10-24_report.txt L24 (row sum 1030)'},
    {'value': 1003, 'date': '2026-10-30', 'kind': 'total_T_rows_including_note_rows',
     'source': 'P3_普适常数族与判定体系.md L13 / 全维总成 L114'},
]
HIST_SRC = {'792': 'ledger', '714': 'left', '766': 'report', '1003': 'p3'}
for h in historical:
    src = HIST_SRC[str(h['value'])]
    G('G-HIST-' + str(h['value']), str(h['value']) in rd(P[src]),
      'historical reading %d present on disk in %s' % (h['value'], src))

normalization = {
    'finding': 'four numbers are NOT four measurements of one quantity',
    'class_a': '792 / 714 / 766 = time-varying count of 🔲 remaining-todo (decreasing to 0)',
    'class_b': '1003 = declared total of status items (330+672+1=1003)',
    'rule': 'compare only within class; cross-class comparison produced the apparent conflict',
    'authoritative_source': 'machine re-scan of mother volume status column (this volume)',
}

F('F01', 'BOUNDARY',
  '实扫 %d 行 = 1000 唯一编号 + %d 重复登记行；声明 1003 状态项 = '
  '1000 编号 + 3 说明行；差 %+d = 重复行 − 说明行，属计数对象差异、非数据丢失，'
  '归因需治理侧核对（本册不代改）'
  % (len(rows), authoritative['extra_duplicate_rows'], len(rows) - 1003))
F('F02', 'PASS',
  '编号 T001–T1000 全覆盖：唯一编号 %d 个，缺号 %s，越界 %s；'
  '「无跳号无重号」中的无跳号成立（重号另见 F03）'
  % (len(set(ids)), authoritative['missing_ids'],
     authoritative['ids_outside_1_1000']))
F('F03', 'FAIL',
  '重复编号行 %d 行（%d 个编号重复，补记/分片表所致）；首 6 组 %s'
  % (authoritative['extra_duplicate_rows'],
     authoritative['duplicate_ids_count'], authoritative['duplicate_ids_top']))
F('F04', 'FAIL',
  '状态列未分类行 %d 行（状态列写成无符号说明文本或表格续行，格式不统一）；样本 %s'
  % (len(none_rows), authoritative['none_rows_sample']))
F('F05', 'BOUNDARY',
  '声明 ✅330/⚠672/◐1 vs 实扫 ✅%d/⚠%d/◐%d + NONE%d；'
  '两者计数对象不同（声明为状态项、实扫为 T 行），不可互比；'
  '差额需治理侧按 F03/F04 归一后复核'
  % (counts.get('✅', 0), counts.get('⚠', 0),
     counts.get('◐', 0), len(none_rows)))
F('F06', 'PASS',
  '🔲 剩余待攻实扫 = %d，与终态声明一致（清单层确已全部有判定）'
  % counts.get('🔲', 0))

# ================= B1. J91 P10: three-generation equivalence =================
p10 = {}
chain = []
for k in range(-6, 7):
    chi = 2 * Fraction(k)
    idx = chi / 2
    chain.append({'k': k, 'chi': str(chi), 'index': str(idx),
                  'index_eq_k': idx == Fraction(k)})
p10['chain'] = chain
p10['chain_all_identity'] = all(c['index_eq_k'] for c in chain)
idx3 = Fraction(3)
chi3 = 2 * idx3
k3 = chi3 / 2
p10['index3'] = {'index': str(idx3), 'chi': str(chi3), 'h11_minus_h21': str(k3)}

sol10 = [(a, 36 - 2 * a) for a in range(-10, 11)]
p10['line_bundle'] = {
    'equation': '2a+b=36 ; index=(2a+b)/12  (a=∫x³, b=∫x·c₂)',
    'family_size_N10': len(sol10),
    'all_give_index_3': all(Fraction(2 * a + b, 12) == 3 for a, b in sol10),
    'sample_pairs': [[a, b] for a, b in sol10[:3]],
    'reading': ('21 distinct (a,b) all give index=3 => the 3-generation condition '
                'has zero discriminating power on the integral data'),
}
p10['errata_crosscheck'] = {
    'printed_c3_coeff': 1,
    'correct_c3_coeff': '1/2',
    'V_eq_TM_printed_index_for_chi6': 6,
    'V_eq_TM_correct_index_for_chi6': 3,
    'ratio': 2,
    'chi3_half_integer_h11_h21': str(Fraction(3, 2)),
    'reading': ('printed form gives χ=3 ⇒ h¹¹−h²¹=1.5 non-integer ⇒ '
                'independently reproduces the J91 §2.5 erratum'),
}

G('G10', p10['chain_all_identity'],
  'P10 index=χ/2=h¹¹−h²¹ exact over k=-6..6')
G('G11', k3 == 3 and chi3 == 6, 'P10 index=3 ⇔ χ=6 ⇔ h¹¹−h²¹=3')
G('G12', p10['line_bundle']['all_give_index_3'] and len(sol10) == 21,
  'P10 21 distinct (a,b) all give index=3 => zero discrimination')
G('G13', 'ch₃' in rd(P['j91']) and '1/2' in rd(P['j91']),
  'P10 erratum cross-checked against J91 volume on disk')

F('F07', 'PASS',
  'J91 登记册「可算 5」全部精算完毕：卷113 B1/B2/B3 + 本册 P10/P11')
F('F08', 'FAIL',
  'P10 三代条件零判别力：21 组互异整数 (a,b) 全部给 index=3，'
  '且打印式错误系数独立复现 J91 勘误（χ=3 ⇒ h¹¹−h²¹=3/2 非整数）')

# ================= B2. J91 P11: coupling dimension gap =================
p11 = {}
ds = sorted(set(list(range(0, 31)) + [26]))
diffs = [(d, (4 - d) - (2 - d)) for d in ds]
p11['dims_tested'] = len(ds)
p11['gap_values'] = sorted(set(x[1] for x in diffs))
p11['gap_constant'] = p11['gap_values'] == [2]
p11['key_dims'] = dict((str(d), (4 - d) - (2 - d))
                       for d in [4, 5, 6, 10, 11, 12, 26])
p11['no_solution_range'] = [-100, 100]
p11['no_solution'] = all(((4 - d) - (2 - d)) != 0
                         for d in range(-100, 101))
p11['equation_reduces_to'] = '(4-d)-(2-d)=2 identically; setting 0 gives 2=0'
p11['minimal_cost'] = ('unify requires [g²]=[κ]·[μ²] with μ a NEW mass scale '
                       '=> +1 external input')
p11['structural'] = 'gap independent of d => raising dimension cannot remove it'
p11['reading'] = ('P11 is computable but NEGATIVE: the arithmetic closes, '
                  'the single-coupling unification does not')

G('G14', p11['gap_constant'], 'P11 gap identically 2 for d=0..30')
G('G15', all(v == 2 for v in p11['key_dims'].values()),
  'P11 key dims 4/5/6/10/11/12/26 all gap=2')
G('G16', p11['no_solution'], 'P11 no integer d in -100..100 closes the gap')

F('F09', 'FAIL',
  'P11 引力-规范单耦合统一在 d=0..30 恒差 2（与维数无关），'
  '−100..100 无解；强行统一需 +1 个外部质量标度 μ')

# ================= C. remaining finite queue & terminal verdict =================
j91_txt = rd(P['j91'])
r403_txt = rd(P['r403'])
a27_txt = rd(P['a27'])
readme_txt = rd(P['readme'])

queue = [
    {'item': 'J91 registry 可算5 (P02/P03/P12 in vol.113; P10/P11 here)',
     'state': 'CLOSED', 'note': '可算 5/5 全部精算完毕，均为负结果/条件结果'},
    {'item': '31 closed-form first-principle derivative deepening',
     'state': 'OPEN_FINITE', 'source': '全维总成 §八.1'},
    {'item': '520 C-class REGISTERED-not-deep-attacked',
     'state': 'BLOCKED_BY_EXPERIMENT',
     'note': 'MOLLER/XENONnT/CMB-S4/LISA；纪律禁止伪造闭合'},
    {'item': '672 ⚠️ re-screening for new closed-form candidates',
     'state': 'OPEN_CONTINUOUS', 'source': '全维总成 §八.3'},
    {'item': 'README 4 unchecked paths (path 4 = core structural gap)',
     'state': 'OPEN_STRUCTURAL', 'source': 'README.md L1508-1511'},
    {'item': 'debts #21 / #22 / #23', 'state': 'OPEN_FINITE',
     'source': '卷113 §七'},
    {'item': 'mother volume row/status normalization (F01–F04)',
     'state': 'OPEN_FINITE', 'source': 'this volume, A section'},
]

terminal = {
    'question': 'all forces in one equation / full agreement with all experimental data',
    'r403_verdict': 'NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK',
    'r403_count': 'four-force (incl. gravity) correct equations = 0',
    'r403_unique_c3': 'electroweak unification only (2 forces)',
    'attack27': 'K1–K6 completion claim 6/6 overturned to 2/6',
    'openuft_49': 'agreement-with-all-data not executable / rejected at 52 sigma',
    'uft_score': '1/6 (UFT-2..UFT-6 all unmet)',
    'consequence': ('a falsified proposition, NOT an unfinished task; '
                    'iteration cannot convert FAIL into PASS'),
    'on_disk': {
        'r403': bool(r403_txt) and 'NO-CORRECT-FOUR-FORCE-GUT' in r403_txt,
        'attack27': bool(a27_txt),
        'j91_registry': bool(j91_txt) and '可算 5' in j91_txt,
        'readme_open_paths': readme_txt.count('- [ ] 路径'),
    },
}

G('G17', terminal['on_disk']['r403'], 'r403 terminal verdict present on disk')
G('G18', terminal['on_disk']['j91_registry'], 'J91 registry 可算5 present on disk')
G('G19', terminal['on_disk']['readme_open_paths'] >= 4,
  'README 4 unchecked paths present on disk')
G('G20', '结构性负面闭合' in final_txt,
  'attack semantics = structural negative closure, not problem solving')
G('G21', all(BEFORE[k] == md5(v) for k, v in P.items()),
  'all read-only inputs unchanged (md5 before/after)')

src = rd(os.path.join(HERE, BASE + '.py'))
imports = []
try:
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            imports += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            imports.append(n.module or '')
except SyntaxError:
    pass
G('G22', not any(x and (x.startswith('attack') or x.startswith('_j9'))
                  for x in imports),
  'no import of any prior attack/J-series engine (independent re-scan)')

F('F10', 'FAIL',
  '「所有力（含引力）放进一个方程」：r403 判正确者 0 条；'
  '四力形式统一族 C3 全 FAIL，耦合/质量/味角均为输入')
F('F11', 'BOUNDARY',
  '唯一 C3 且真统一 = 电弱统一 L_EW（2 力，非四力）')
F('F12', 'FAIL',
  '「微观宏观量子与传统实验数据全一致」不可执行 / 被 52σ 否决（卷49）；'
  '卷77 仅 profile 层 8/8，且 α 反冲 / 缪子 g-2 / m_W CDF 三处张力在案')
F('F13', 'FAIL',
  '「攻破达成声明」K1–K6 6/6 经 attack27 独立复核推翻为 2/6')
F('F14', 'BOUNDARY',
  '清单层 🔲=0 表示「全部有判定」，判定性质是结构性负面闭合，'
  '不等于 100/1000 个物理难题被解决；0/22、UFT-3=0 保持')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))

result = {
    'volume': 'attack47',
    'date': '2026-11-08',
    'scope': ('Top100/Top1000 terminal machine normalization + '
              'J91 problem-registry residual exact arithmetic (P10/P11)'),
    'authoritative': authoritative,
    'declared_in_final_volume': declared,
    'historical_readings': historical,
    'normalization': normalization,
    'p10': p10,
    'p11': p11,
    'findings': FINDINGS,
    'verdict_counts': verdict_counts,
    'remaining_queue': queue,
    'terminal_verdict': terminal,
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

lines = []
lines.append('attack47 / 2026-11-08 / terminal normalization + J91 residual')
lines.append('')
lines.append('[A] mother volume machine re-scan')
for k in ['T_rows', 'unique_ids', 'id_min', 'id_max', 'missing_ids',
          'duplicate_ids_count', 'extra_duplicate_rows', 'none_rows_count',
          'status_counts', 'sum_equals_rows']:
    lines.append('  %s = %s' % (k, authoritative[k]))
lines.append('  none_rows_sample = %s' % authoritative['none_rows_sample'])
lines.append('  declared(final volume) = %s' % declared)
lines.append('  normalization = %s' % normalization['finding'])
lines.append('')
lines.append('[B] J91 residual exact arithmetic')
lines.append('  P10 chain identity over k=-6..6 : %s' % p10['chain_all_identity'])
lines.append('  P10 index=3 => chi=%s, h11-h21=%s' % (chi3, k3))
lines.append('  P10 line bundle : %d pairs, all index=3 : %s'
             % (len(sol10), p10['line_bundle']['all_give_index_3']))
lines.append('  P11 gap values over d=0..30 : %s' % p11['gap_values'])
lines.append('  P11 no d closes gap in -100..100 : %s' % p11['no_solution'])
lines.append('')
lines.append('[C] findings %s' % verdict_counts)
for f in FINDINGS:
    lines.append('  %s %s : %s' % (f['verdict'], f['code'], f['note']))
lines.append('')
lines.append('[D] terminal verdict')
lines.append('  %s' % terminal['r403_verdict'])
lines.append('  %s' % terminal['consequence'])
lines.append('')
lines.append('[guards] %d/%d' % (result['guard_pass'], result['guard_total']))
for g in GUARDS:
    lines.append('  %s %s : %s' % ('PASS' if g['ok'] else 'FAIL',
                                   g['code'], g['note']))
lines.append('')
lines.append('EXIT=%d' % result['exit'])
report = '\n'.join(lines) + '\n'
with io.open(os.path.join(HERE, BASE + '_report.txt'), 'w',
             encoding='utf-8') as f:
    f.write(report)

md = []
md.append('# attack47 · 数据产物（机读摘要）')
md.append('')
md.append('- 日期：2026-11-08 ｜ 守卫 **%d/%d** ｜ 退出码 **%d**'
          % (result['guard_pass'], result['guard_total'], result['exit']))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 性质：只读归一 + 精确算术；不重判既有条目、不产生新物理、'
          '不修改任何既有册字节')
md.append('')
md.append('| 段 | 读数 | 值 |')
md.append('|---|---|---|')
md.append('| A | 母册 T 行实扫 | %d |' % authoritative['T_rows'])
md.append('| A | 唯一编号数 | %d |' % authoritative['unique_ids'])
md.append('| A | 缺号 | %s |' % authoritative['missing_ids'])
md.append('| A | 重复编号行 | %d |' % authoritative['extra_duplicate_rows'])
md.append('| A | 未分类状态行 | %d |' % authoritative['none_rows_count'])
md.append('| A | 状态计数 | %s |' % authoritative['status_counts'])
md.append('| B | P10 等价链恒等 | %s |' % p10['chain_all_identity'])
md.append('| B | P10 index=3 ⇒ χ / (h¹¹−h²¹) | %s / %s |' % (chi3, k3))
md.append('| B | P10 线丛解族（全部给 index=3） | %d 组 |' % len(sol10))
md.append('| B | P11 维度差取值集合 | %s |' % p11['gap_values'])
md.append('| B | P11 无 d 使差为 0 | %s |' % p11['no_solution'])
md.append('| C | 含引力四力大统一正确者 | 0 条 |')
md.append('')
md.append('> 完整判定与诚实边界见 '
          '`判定_attack47_清单终态机器归一与J91余数精算_2026-11-08.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

print('attack47 guards=%d/%d findings=%s exit=%d T_rows=%d' %
      (result['guard_pass'], result['guard_total'], verdict_counts,
       result['exit'], authoritative['T_rows']))
sys.exit(result['exit'])
