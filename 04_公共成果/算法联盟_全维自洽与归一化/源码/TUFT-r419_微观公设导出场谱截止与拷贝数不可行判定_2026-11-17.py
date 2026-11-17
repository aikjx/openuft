# -*- coding: utf-8 -*-
# r419 / algorithm alliance -- feasibility verdict on deriving field spectrum / UV cutoff / copy number
# from ROOT microscopic postulate (2026-11-17)
# Task from r418 handoff: attack the last decisive gap -- derive spectrum, Lambda_UV, N from
# the helix postulate instead of reverse-fitting G. Answer: structurally underdetermined in current corpus.
# Pure stdlib; read-only facts; quote source self-assessments; does NOT claim completion.
import os
import io
import sys
import ast
import json
import hashlib

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r419_微观公设导出场谱截止与拷贝数不可行判定_2026-11-17'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_JUDGE = os.path.join(PUB, '判定_TUFT-r419-微观公设导出场谱截止与拷贝数不可行判定_2026-11-17.md')

# fact sources (read-only corpus, absolute paths)
ISOK = os.path.join(os.path.expanduser('~'), 'Downloads', 'is_ok')
F_V50_THEORY = os.path.join(ISOK, '202611', 'ROOT_V50_运动几何统一研究包', 'THEORY.md')
F_V50_PLAN = os.path.join(ISOK, '202611', 'ROOT_V50_运动几何统一研究包', 'RESEARCH_PLAN.md')
F_V51 = os.path.join(ISOK, '202611', 'ROOT_V51_理论总纲与复算包', 'ROOT_V51_统一场论核心方程组_研究总纲.md')
F_V22 = os.path.join(ISOK, '202611', 'ROOT_V22_紫外临界面与精细结构常数本源_研究核验', 'ROOT_V22_临界面与电磁耦合本源_完整报告.md')
F_V16 = os.path.join(ISOK, '202611', 'ROOT_V16_固定作用量与精细结构常数审计', 'ROOT_V16_固定作用量磁通与几何控制_完整报告.md')
F_V38 = os.path.join(ISOK, '202611', 'ROOT_V38_四力本源_光速螺旋与引力源_全维核验包', 'ROOT_V38_四力几何联络与光速旋转引力源_严格核验.md')
F_R418 = os.path.join(PUB, '判定_TUFT-r418-ROOT_V62诱导引力有效作用量_2026-11-17.md')
FACTS = [F_V50_THEORY, F_V50_PLAN, F_V51, F_V22, F_V16, F_V38, F_R418]

VERDICT = ('MICROSCOPIC-DERIVATION--STRUCTURALLY-UNDERDETERMINED--'
           'KAPPA-TAU-ARE-OUTCOME-VARIABLES--SPECTRUM-OPERATOR-EXOGENOUS--'
           'LAMBDA-AND-N-REVERSE-FITTED--ACTION-MISSING--'
           'NO-FALSIFIABLE-PREDICTION--0OF6-UNCHANGED')

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


# --- fact extraction: locate a verbatim quote substring in a source file ---
def find_quote(key, path, needle):
    if not os.path.exists(path):
        QUOTES[key] = {'found': False, 'file': os.path.basename(path), 'absent': True}
        return False
    txt = io.open(path, encoding='utf-8', errors='replace').read()
    idx = txt.find(needle)
    ok = idx >= 0
    QUOTES[key] = {'found': ok, 'file': os.path.basename(path), 'needle': needle,
                   'context': txt[max(0, idx - 40):idx + len(needle) + 60].replace('\n', ' ') if ok else ''}
    return ok

# --- guards ---
guard('G0-0_stdlib_only', 'sympy' not in sys.modules and 'numpy' not in sys.modules, 'pure stdlib')
for i, f in enumerate(FACTS):
    guard('G0-fact-%d' % i, os.path.exists(f), os.path.basename(f))

# verbatim self-assessment quotes (the decisive evidence: authors themselves deny derivation)
q1 = find_quote('Q-V50-outcome', F_V50_THEORY, '仅用 κ、τ 作为轨迹的结果变量会循环论证')
q2 = find_quote('Q-V50-action', F_V50_THEORY, '应提出协变作用量')
q3 = find_quote('Q-V50-noCfg', F_V50_THEORY, '没有已证实的经典')
q4 = find_quote('Q-V51-N3', F_V51, '该机制无法回答真空为何要取')
q5 = find_quote('Q-V51-fitted', F_V51, '这些参数正是为此特意选定的')
q6 = find_quote('Q-V51-nopred', F_V51, '不是自主预测')
q7 = find_quote('Q-V22-nodrive', F_V22, '缺失可以把所有相关方向')
q8 = find_quote('Q-V22-nofirst', F_V22, '从第一性原理独立预测')
q9 = find_quote('Q-V16-freeparam', F_V16, '不能称本模型为纯引力几何的零自由参数推导')
q10 = find_quote('Q-V38-source', F_V38, '空间光速螺旋基元')
q11 = find_quote('Q-V38-stress', F_V38, '协变源张量')
guard('G1-quotes-all-found', all([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11]),
      'found %d/11 decisive self-assessment quotes' % sum([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11]))
SRC = io.open(__file__, encoding='utf-8').read()
try:
    ast.parse(SRC)
    guard('G2-ast', True, 'self syntax ok')
except SyntaxError as e:
    guard('G2-ast', False, str(e))

emit('')
emit('=== r419 microscopic-derivation feasibility -- verdict entries ===')

# S1 kappa/tau are outcome variables (circular)
add('S01', 'FAIL', 'kappa/tau from helix kinematics are outcome variables, not a force origin',
    'V50 THEORY.md verbatim: "仅用 κ、τ 作为轨迹的结果变量会循环论证：它们本来就由已发生的运动计算出来，不能自动成为力的起源"')

# S2 no covariant action at the helix-geometry layer
add('S02', 'OPEN', 'ROOT geometry layer has no covariant action; V62 S_phi is an imported standard scalar action',
    'V50 THEORY.md "应提出协变作用量、保证量纲一致和能量动量守恒"; V38 "必须说明它的协变源张量及其变分作用量"; action is a stated TODO, not derived')

# S3 spectrum operator exogenous
add('S03', 'FAIL', 'field spectrum {lambda_n} comes from an exogenous operator -Delta_K, not from kappa/tau',
    'V51 section 4 defines -Delta_K f_n=lambda_n f_n, m_n^2=m0^2+lambda_n; V51 section 3 (helix kinematics) and section 4-5 (spectrum) are independent, no derivation link')

# S4 Lambda_UV reverse-fitted
add('S04', 'FAIL', 'UV cutoff Lambda_UV is a free continuous parameter fixed only by fitting alpha_s / G',
    'V22 "缺失可以把所有相关方向、阈值与统一耦合共同锁定的独立动力学公设"; V16 "M_6,g_6,Λ_6 是独立的六维参数……不能称……零自由参数推导"')

# S5 N only topologically quantized, value 3 reverse-picked
add('S05', 'FAIL', 'copy number N: index theorem gives N in Z only; N=3 is reverse-selected, not derived',
    'V51 N=(1/2pi)∫F in Z, "该机制无法回答真空为何要取 N=3"; "这些参数正是为此特意选定的……得到 N=3 不是自主预测"')

# S6 no helix light-speed elementary entity proven
add('S06', 'BOUNDARY', 'no proven physical "space light-speed helix elementary entity" with independent action',
    'V50 "没有已证实的经典内部圆柱螺旋轨迹"; V38 "一个物理存在的空间光速螺旋基元、它的独立运动作用量……尚未证明"')

# S7 degrees-of-freedom count: underdetermination theorem
add('S07', 'FAIL', 'underdetermination: finite kinematic outputs cannot fix operator spectrum + cutoff + N',
    'helix layer outputs kappa(s),tau(s) (2 scalar functions) + no action; targets: infinite spectrum {lambda_n}, continuous Lambda_UV, integer N, gauge reps -- at least 3 independent inputs absent')

# S8 what "completion" would require (minimal augmentation, not selected)
add('S08', 'OPEN', 'minimal augmentation to reopen r419 (not chosen for the user)',
    '(1) one independent covariant action from the helix axiom; (2) a geometry-defined operator -Delta_K with no fitted parameters; (3) a selection rule fixing N=3 and Lambda_UV, then a blind prediction not used in fitting')

# S9 no falsifiable prediction without the three
add('S09', 'FAIL', 'without S08, no falsifiable prediction: any observed G/alpha can be reproduced by tuned Lambda/N',
    'G_ind=12pi/(N Lambda^2) (r418) has two free knobs (N integer, Lambda continuous); two observables are always fit-able -- zero new information')

# S10 inherited from r418
add('S10', 'INFO', 'inherits r418 verdict: induced gravity is Sakharov textbook mechanism, G_ROOT∘R_H identity',
    'r418 roundtrip residual 2.996569E-60 machine zero; red line unchanged')

# S11 red line
add('S11', 'INFO', 'red line unchanged',
    '0/6 incomplete, 0/22, UFT-3=0, L3=0, validated=0, gravity+four-force correct eq 0, L3 not=> L4')

emit('')
print('ENTRIES=' + str(len(ENTRIES)) + ' GUARDS=' + str(len(GUARDS)))

# --- persist ---
FACT_HASH = {os.path.basename(f): md5(f) for f in FACTS}
RESULT = {
    'round': 'r419', 'date': DATE,
    'topic': 'feasibility of deriving field spectrum / UV cutoff / N from ROOT microscopic postulate',
    'source': 'read-only is_ok corpus + r418 verdict',
    'verdict': VERDICT,
    'method': 'pure stdlib; verbatim self-assessment quote scan; degrees-of-freedom underdetermination',
    'entries': ENTRIES, 'guards': GUARDS, 'quotes': QUOTES,
    'guard_pass': sum(1 for x in GUARDS if x['pass']), 'guard_total': len(GUARDS),
    'counts': {}, 'fact_md5': FACT_HASH, 'red_line': RED,
    'minimal_augmentation_not_chosen': [
        'independent covariant action from the helix axiom',
        'geometry-defined spectrum operator -Delta_K with zero fitted parameters',
        'selection rule fixing N=3 and Lambda_UV, validated by a blind prediction not used in fitting',
    ],
    'next_round': {
        'r': 'r420',
        'topic': 'if user supplies a concrete helix covariant action, audit it for GR limit / dimension / falsifiable prediction',
        'blocker': 'no such action exists in corpus; V50/V38 list it as TODO',
    },
}
cnt = {}
for e in ENTRIES:
    cnt[e['verdict']] = cnt.get(e['verdict'], 0) + 1
RESULT['counts'] = cnt

with io.open(P_JSON, 'w', encoding='utf-8') as f:
    f.write(json.dumps(RESULT, ensure_ascii=False, indent=2))

MD = ['# 数据产物 · TUFT r419：微观公设导出场谱/截止/拷贝数不可行判定', '',
      '- 轮次：r419；日期：' + DATE,
      '- verdict：`' + VERDICT + '`',
      '- 结论：现有 ROOT 来料无正面推导抓手；缺口精确定位于「独立协变作用量 + 无拟合谱算符 + 选择规则」三者，非精度/算力问题。',
      '', '## 决定性的作者自评引文', '']
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
    f.write('QUOTES_FOUND=' + str(sum(1 for q in QUOTES.values() if q.get('found'))) + '/11\n')
    f.write('COUNTS=' + json.dumps(cnt, ensure_ascii=False) + '\n')

assert RESULT['guard_pass'] == RESULT['guard_total'], 'guard failure'
print('WROTE', P_JSON)
print('WROTE', P_MD)
print('WROTE', P_REPORT)
print('DONE r419')
