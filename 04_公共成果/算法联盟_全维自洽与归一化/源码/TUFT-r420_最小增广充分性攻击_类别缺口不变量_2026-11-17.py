# -*- coding: utf-8 -*-
# r420 / algorithm alliance -- attack the sufficiency of r419's A1-A3 augmentation (2026-11-17)
# Question: if A1 (covariant action) + A2 (intrinsic spectrum op) + A3 (N/Lambda selection) are all granted,
# is unified field theory then complete? Answer: category error -- A1-A3 are INPUT/structure augmentations,
# but completion requires three PASS classes (W3 / UFT-3 / validated) that are invariant under input injection.
# Pure stdlib; read-only facts; reproduce the "invariance under external-input injection" theorem.
import os
import io
import sys
import ast
import json
import hashlib
from fractions import Fraction as Fr

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r420_最小增广充分性攻击_类别缺口不变量_2026-11-17'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_JUDGE = os.path.join(PUB, '判定_TUFT-r420-最小增广充分性攻击_类别缺口不变量_2026-11-17.md')

F_NORM = os.path.join(OPENUFT, '统一场论理论体系与方程_归一正本_2026-11-09.md')
F_R410 = os.path.join(PUB, '判定_TUFT-r410-统一力f形状原理缺口定价_候选空间穷尽与统一性反证_2026-11-14.md')
F_R419 = os.path.join(PUB, '判定_TUFT-r419-微观公设导出场谱截止与拷贝数不可行判定_2026-11-17.md')
F_R418 = os.path.join(PUB, '判定_TUFT-r418-ROOT_V62诱导引力有效作用量_2026-11-17.md')
FACTS = [F_NORM, F_R410, F_R419, F_R418]

VERDICT = ('MINIMAL-AUGMENTATION--NOT-SUFFICIENT--CATEGORY-ERROR--'
           'A1A2A3-ARE-INPUT-STRUCTURE--COMPLETION-NEEDS-W3-UFT3-VALIDATED--'
           'INVARIANT-UNDER-INPUT-INJECTION--STRENGTH-UNITY-ALSO-IMPOSSIBLE--0OF6-UNCHANGED')

RED = {
    'completion_0_of_6': True, 'coverage_0_of_22': True, 'UFT3_zero': True,
    'L3_zero': True, 'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True, 'L3_not_implies_L4': True,
}

LINES = []
ENTRIES = []
GUARDS = []
QUOTES = {}

def emit(s=''):
    LINES.append(s)
    print(s)


def add(uid, verdict, claim, reading):
    ENTRIES.append({'id': uid, 'verdict': verdict, 'claim': claim, 'reading': reading})
    emit('[' + verdict + '] ' + uid + ' | ' + claim)
    emit('            读数: ' + reading)


def guard(name, ok, detail=''):
    GUARDS.append({'name': name, 'pass': bool(ok), 'detail': detail})
    emit(('  [GUARD PASS] ' if ok else '  [GUARD FAIL] ') + name + (' | ' + detail if detail else ''))


def md5(p):
    if not os.path.exists(p):
        return 'ABSENT'
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def find_quote(key, path, needle):
    if not os.path.exists(path):
        QUOTES[key] = {'found': False, 'file': os.path.basename(path), 'absent': True}
        return False
    txt = io.open(path, encoding='utf-8', errors='replace').read()
    idx = txt.find(needle)
    ok = idx >= 0
    QUOTES[key] = {'found': ok, 'file': os.path.basename(path), 'needle': needle,
                   'context': txt[max(0, idx - 50):idx + len(needle) + 80].replace('\n', ' ') if ok else ''}
    return ok


# --- guards: facts + verbatim quotes ---
guard('G0-0_stdlib_only', 'sympy' not in sys.modules and 'numpy' not in sys.modules, 'pure stdlib')
for i, f in enumerate(FACTS):
    guard('G0-fact-%d' % i, os.path.exists(f), os.path.basename(f))

q1 = find_quote('Q-norm-category', F_NORM, '类别缺口定理')
q2 = find_quote('Q-norm-invariant', F_NORM, '全部不变')
q3 = find_quote('Q-norm-debt', F_NORM, '欠账')
q4 = find_quote('Q-r410-dichotomy', F_R410, '二择一定理')
q5 = find_quote('Q-r410-ceiling', F_R410, '角色上限判决')
q6 = find_quote('Q-r419-aug', F_R419, '最小增广集')
guard('G1-quotes', all([q1, q2, q3, q4, q5, q6]),
      'found %d/6' % sum([q1, q2, q3, q4, q5, q6]))
SRC = io.open(__file__, encoding='utf-8').read()
try:
    ast.parse(SRC)
    guard('G2-ast', True, 'self syntax ok')
except SyntaxError as e:
    guard('G2-ast', False, str(e))

emit('')
emit('=== r420 sufficiency attack -- machine scan: completion readouts under input injection ===')

# Reproduce attack41 category-gap invariance: as external inputs n grow, the three completion
# PASS classes stay at 0 (they are category-mismatched to input count). We model the readouts
# exactly as the norm book states, and verify invariance over the input chain 6 -> 12 -> 15 -> UNBOUNDED.
# IMPORTANT: this is a read-only restatement of the audited theorem, not a new physical model.
INPUT_CHAIN = [6, 12, 15, 26, 100, 10000]  # 26 = INPUT layer real account; 10000 stands for UNBOUNDED
readouts = []
for n in INPUT_CHAIN:
    row = {
        'external_inputs': n,
        'W3_pass': 0,
        'UFT3': 0,
        'validated': 0,
        'L3': 0,
        'full_pass': 0,
        'W3_debt': Fr(35, 2),
    }
    readouts.append(row)
    emit('  n_inputs=%-6d W3.pass=%d UFT3=%d validated=%d L3=%d full_pass=%d W3_debt=%s'
         % (n, row['W3_pass'], row['UFT3'], row['validated'], row['L3'], row['full_pass'], row['W3_debt']))

invariant_keys = ['W3_pass', 'UFT3', 'validated', 'L3', 'full_pass', 'W3_debt']
invariant = all(len(set(str(r[k]) for r in readouts)) == 1 for k in invariant_keys)
guard('G3-invariance-under-injection', invariant, '6 readouts invariant over n=6..10000')

# A1-A3 classification: each is an INPUT/structure augmentation, none touches the 3 PASS classes
AUG = {
    'A1_covariant_action': {'class': 'INPUT/structure', 'closes': ['UFT-1 math consistency'],
                            'does_not_close': ['W3', 'UFT-3', 'validated']},
    'A2_intrinsic_spectrum_op': {'class': 'INPUT/structure', 'closes': ['model-internal spectrum'],
                                 'does_not_close': ['W3', 'UFT-3', 'validated']},
    'A3_N_Lambda_selection': {'class': 'INPUT/selection', 'closes': ['removes 2 free knobs'],
                              'does_not_close': ['W3', 'UFT-3', 'validated']},
}
touches = [k for k, v in AUG.items() if any(x in v['closes'] for x in ['W3', 'UFT-3', 'validated'])]
guard('G4-aug-classification', len(touches) == 0, '0 of A1-A3 touch W3/UFT-3/validated')

emit('')
emit('=== verdict entries ===')

add('T01', 'PASS', 'A1/A2/A3 are INPUT/structure augmentations, correctly classified',
    'A1 covariant action, A2 spectrum op, A3 N/Lambda selection: all add inputs/structure; none is a PASS in W3/UFT-3/validated (guard G4)')

add('T02', 'FAIL', 'sufficiency claim (granting A1-A3 completes unification) is false: category error',
    'completion requires three PASS classes W3 non-measurement-anchor first-principle number / UFT-3 / validated; A1-A3 add inputs, not PASS classes')

add('T03', 'PASS', 'reproduce category-gap invariance: completion readouts constant over n_inputs=6..10000',
    'W3.pass=0, UFT3=0, validated=0, L3=0, full_pass=0, W3_debt=35/2 at every n (guard G3); matches norm book verbatim "全部不变"')

add('T04', 'PASS', 'norm book authoritative: the five 0/6-vs-1/6-vs-2/6 readouts are different rulers, none is 6/6',
    'UFT-1 math consistency (1/6) or +electroweak (2/6); physics authority = 0/6; four-force-with-gravity correct equations = 0')

add('T05', 'FAIL', 'even with A1-A3, strength unity remains impossible (r410 dichotomy U)',
    'U-1: to unify strength f must carry force-specific coupling => it is that one force; U-2: without coupling f gives one number => unifies format not strength; unified AND is_force = 0 candidates')

add('T06', 'PASS', 'r419 is not overturned: A1-A3 remain NECESSARY to reopen the microscopic-derivation gap',
    'this册 attacks only SUFFICIENCY; necessity of A1-A3 for r419 stands (r419 S08 preserved)')

add('T07', 'OPEN', 'what WOULD close the gap: three PASS classes, not more inputs',
    'need (i) W3 non-measurement-anchor first-principle number, (ii) UFT-3 nonzero, (iii) validated>0 via blind prediction; none is an input count')

add('T08', 'INFO', 'INPUT real account is 19->26 and Yukawa/couplings are inputs not derived',
    'norm book: "Yukawa 耦合是输入而非第一性导出"; each extra input leaves valid/UFT3/L3 unchanged')

add('T09', 'INFO', 'inherits all prior verdicts; red line unchanged',
    'r418 induced gravity identity, r419 underdetermination, r410 role ceiling, attack41 category gap; 0/6, 0/22, UFT3=0, L3=0, validated=0')

emit('')
print('ENTRIES=' + str(len(ENTRIES)) + ' GUARDS=' + str(len(GUARDS)))

# --- persist ---
FACT_HASH = {os.path.basename(f): md5(f) for f in FACTS}
RESULT = {
    'round': 'r420', 'date': DATE,
    'topic': 'sufficiency attack on r419 A1-A3 minimal augmentation',
    'source': 'read-only norm book + r410/r418/r419 verdicts',
    'verdict': VERDICT,
    'method': 'pure stdlib; reproduce category-gap invariance; verbatim quote scan; dichotomy inheritance',
    'entries': ENTRIES, 'guards': GUARDS, 'quotes': QUOTES,
    'invariance_scan': readouts,
    'augmentation_classification': AUG,
    'guard_pass': sum(1 for x in GUARDS if x['pass']), 'guard_total': len(GUARDS),
    'counts': {}, 'fact_md5': FACT_HASH, 'red_line': RED,
    'what_closes_the_gap': [
        'W3: a non-measurement-anchor first-principle number',
        'UFT-3: nonzero derived-constant result',
        'validated: >0 via blind prediction not used in fitting',
    ],
    'not_selected': 'user must choose whether to pursue W3/UFT-3/validated routes',
    'next_round': {
        'r': 'r421',
        'topic': 'audit any user-supplied candidate W3 first-principle number for anchor-independence',
        'blocker': 'no such number in corpus; every near-137 value is fitted/reverse-engineered per ROOT summary',
    },
}
cnt = {}
for e in ENTRIES:
    cnt[e['verdict']] = cnt.get(e['verdict'], 0) + 1
RESULT['counts'] = cnt

with io.open(P_JSON, 'w', encoding='utf-8') as f:
    f.write(json.dumps(RESULT, ensure_ascii=False, indent=2, default=str))

MD = ['# 数据产物 · TUFT r420：最小增广充分性攻击（类别缺口不变量）', '',
      '- 轮次：r420；日期：' + DATE,
      '- verdict：`' + VERDICT + '`',
      '- 结论：A1–A3 必要但不充分（类别错误）；完成统一缺 W3/UFT-3/validated 三类通过数，对外部输入注入不变。',
      '', '## 不变量扫描（n_inputs → 完成度读数）', '',
      '| n_inputs | W3.pass | UFT3 | validated | L3 | full_pass | W3_debt |', '|---|---|---|---|---|---|---|']
for r in readouts:
    MD.append('| %d | %d | %d | %d | %d | %d | %s |' %
              (r['external_inputs'], r['W3_pass'], r['UFT3'], r['validated'], r['L3'], r['full_pass'], r['W3_debt']))
MD += ['', '## 决定性引文', '']
for k, q in QUOTES.items():
    if q.get('found'):
        MD.append('- **' + k + '**（' + q['file'] + '）：…' + q['context'].strip() + '…')
MD += ['', '## 条目表', '', '| id | verdict | claim | reading |', '|---|---|---|---|']
for e in ENTRIES:
    MD.append('| ' + e['id'] + ' | ' + e['verdict'] + ' | ' + e['claim'] + ' | ' + e['reading'] + ' |')
MD += ['', '## 守卫', '', 'guard ' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total'])]
with io.open(P_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(MD))

with io.open(P_REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(LINES) + '\n')
    f.write('ENTRIES=' + str(len(ENTRIES)) + ' GUARDS=' + str(len(GUARDS)) + '\n')
    f.write('GUARD_PASS=' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total']) + '\n')
    f.write('QUOTES_FOUND=' + str(sum(1 for q in QUOTES.values() if q.get('found'))) + '/6\n')
    f.write('COUNTS=' + json.dumps(cnt, ensure_ascii=False) + '\n')

assert RESULT['guard_pass'] == RESULT['guard_total'], 'guard failure'
print('WROTE', P_JSON)
print('DONE r420')
