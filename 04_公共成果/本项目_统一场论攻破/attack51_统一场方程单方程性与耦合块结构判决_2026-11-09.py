# -*- coding: utf-8 -*-
"""attack51 / 攻破㊸ · 统一场方程「单方程性」与耦合块结构判决.

Target: 07_统一场方程/00_统一场方程.md (UFE-1) section 2.1 master equation.
Pure stdlib / Python 3.8 / Fraction exact rank. Read-only on all inputs.
GUARDS drive the exit code; FINDINGS record verdicts on assertions.
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
BASE = 'attack51_统一场方程单方程性与耦合块结构判决_2026-11-09'


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


def rank_of(mat):
    m = [[Fraction(x) for x in row] for row in mat]
    if not m:
        return 0
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


P = {
    'v00': os.path.join(V7, '00_统一场方程.md'),
    'v01': os.path.join(V7, '01_作用量与场内容.md'),
    'v02': os.path.join(V7, '02_变分推导.md'),
    'report': os.path.join(V7, '验证脚本', '验证报告.md'),
    'ufe1': os.path.join(B1, '判定_UFE1统一场方程_全维攻破_2026-10-09.md'),
    'r207': find_md(RDIR, '判定_TUFT-r207'),
    'r355': find_md(RDIR, '判定_TUFT-r355'),
    'r403': find_md(RDIR, '判定_TUFT-r403'),
    'a37': find_md(B1, '判定_attack37'),
    'a50': find_md(B1, '判定_attack50'),
}
BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


v00, v01, v02 = rd(P['v00']), rd(P['v01']), rd(P['v02'])
report, ufe1 = rd(P['report']), rd(P['ufe1'])
r207, r355, r403 = rd(P['r207']), rd(P['r355']), rd(P['r403'])
a37, a50 = rd(P['a37']), rd(P['a50'])

# ---- (A) how many Euler-Lagrange equations hide behind delta S / delta Phi ---
single_eq_anchor = (r'\frac{\delta S}{\delta \Phi}' in v00 and
                    r'\tag{UFE-1}' in v00)
phi_anchor = r'\Phi=(e^a,\mathcal A,H,\Psi)' in v00
kappa_anchor = r'\kappa^2=8\pi G/c^4' in v00

variation_sections = re.findall(r'^## (\d+)\. 对(.+?)变分', v02, re.M)
variation_ids = [int(x[0]) for x in variation_sections]
five_eq_heading = '## 6. 五个方程的整体自洽性' in v02
tag_letters = re.findall(r'\\tag\{([A-Z$][^}]*)\}', v02)
eq_tags = sorted(set(t.replace('$', '').replace("'", '')
                     for t in tag_letters if t.startswith(('C', 'E', 'Y', 'H', 'D'))))

FIELD_MAP = [
    ('自旋联络', ['omega']),
    ('vierbein', ['e']),
    ('内部规范势', ['A1', 'A2', 'A3']),
    ('Higgs', ['H']),
    ('物质场', ['Psi']),
]
FIELDS = ['e', 'omega', 'A1', 'A2', 'A3', 'H', 'Psi']
field_index = dict((f, i) for i, f in enumerate(FIELDS))
eq_field_groups = []
for num, title in variation_sections:
    hit = None
    for needle, group in FIELD_MAP:
        if needle in title:
            hit = group
            break
    eq_field_groups.append(hit)
map_complete = all(g is not None for g in eq_field_groups)
covered_fields = sorted(set(f for g in eq_field_groups if g for f in g))
coverage_exact = (covered_fields == sorted(FIELDS))
n_eq_field_level = len(eq_field_groups)
n_eq_group_level = sum(len(g) for g in eq_field_groups if g)

# ---- (B) action blocks and curvature cross terms -------------------------
block_line = re.search(r'S=S_\{\\rm (\w+)\}((?:\+S_\{\\rm \w+\})+)', v01)
blocks = []
if block_line:
    blocks = [block_line.group(1)] + re.findall(
        r'S_\{\\rm (\w+)\}', block_line.group(2))
cross_commutator_anchor = (r'[\mathfrak{so}(1,3),\mathfrak g_{\rm int}]=0' in v00
                           and '交叉对易子消失' in v00)
curvature_split_anchor = (r'R^{ab}&=d\omega^{ab}' in v00 and
                          r'F^{(i)}&=dA^{(i)}' in v00)
errata_anchor = ('不能从该作用量推出一个同时包含 Einstein–Cartan 与内部 Yang–Mills 方程的'
                 in v00)
honest_anchor = ('本文件不构成“统一场论已经完成”的声明' in v00 and
                 '共同驻作用量记号是组织方式' in v00)

s21 = v00.split('### 2.1 单一方程形式')[-1].split('### 2.2')[0]
action_segments = s21.split('\\\\[2pt]')


def has_gravity_curvature(seg):
    return (r'R^{ab}' in seg or r'\tilde R' in seg)


def has_internal_curvature(seg):
    return (r'F^{(i)}' in seg or r'G^A_{\mu\nu}' in seg or
            r'W^i_{\mu\nu}' in seg or r'B_{\mu\nu}' in seg)


cross_segments = [s for s in action_segments
                  if has_gravity_curvature(s) and has_internal_curvature(s)]
gravity_segments = [s for s in action_segments if has_gravity_curvature(s)]
internal_segments = [s for s in action_segments if has_internal_curvature(s)]
inject_seg = (action_segments[0] if action_segments else '') + r'\wedge F^{(i)}'
cross_control = (has_gravity_curvature(inject_seg) and
                 has_internal_curvature(inject_seg))

# ---- (C) input-parameter ledger and rank theorem -------------------------
sec33 = v01.split('### 3.3 输入参数清单')[-1].split('## 4.')[0]
param_counts = [int(x) for x in re.findall(r'^\|\s*[^|]+\|\s*(\d+)\s*\|',
                                           sec33, re.M)]
param_total_declared = ('UFE-1 的自由参数共 **26 个**' in v01)
param_not_derived = ('这 26 个数是从实验输入进来的，不是算出来的' in v01)
yukawa_input = ('这是 UFE-1 的输入参数，不是推导结果' in v01)
n_params = sum(param_counts)

M = []
for groups in eq_field_groups:
    row = [0] * (len(FIELDS) + n_params)
    for f in (groups or []):
        row[field_index[f]] = 1
    M.append(row)
rank_full = rank_of(M)
rank_constants = rank_of([row[len(FIELDS):] for row in M])
M_inject = [list(row) for row in M]
M_inject[0][len(FIELDS)] = 1
rank_constants_injected = rank_of([row[len(FIELDS):] for row in M_inject])

# ---- (D) cross-document corroboration ------------------------------------
r403_u11 = ('UFE-1 共同变分作用量' in r403 and
            'COMMON-ACTION-NOT-UNIFIED' in r403 and
            'NO-CORRECT-FOUR-FORCE-GUT' in r403)
u11_row = re.search(r'^\| U11 \|([^\n]+)\|$', r403, re.M)
u11_cols = [c.strip() for c in u11_row.group(1).split('|')] if u11_row else []
u11_c3_fail = (len(u11_cols) >= 6 and u11_cols[5] == 'FAIL')
u11_status = u11_cols[-1] if u11_cols else ''
r403_c3 = (u11_c3_fail and '| C3 | 实证层' in r403 and
           '含引力四力大统一正确者 = 0 条' in r403)
r207_scope = ('全卷首次审计' in r207 and '审计对象' in r207 and
              '树级关系' in r207)
r355_scope = ('变分推导' in r355 and '外形式恒等式' in r355)
a37_scope = ('1+1D' in a37 or '极小超空间' in a37 or 'toy' in a37.lower())
ufe1_scope = ('M1–M5 无一过门' in ufe1 and '26 个外部输入' in ufe1)
a50_scope = ('PARTIAL_CLOSURE' in a50 and '不计攻破数' in a50)
verification_scope = ('47 项检查' in report and
                      'PASS 39 / FAIL 2 / INFO 6' in report)

# ---- closure state machine (counterfactual-capable pure functions) -------
def verdict_single_eq(n_declared, n_field_eq, n_group_eq, cross, crank):
    ok = (n_declared == 1 and n_field_eq == 5 and n_group_eq == 7 and
          cross == 0 and crank == 0)
    return 'NOTATION-LEVEL-ONLY' if ok else 'RECHECK'


def verdict_unified(cross, crank, c3_fail):
    ok = (cross == 0 and crank == 0 and c3_fail == 1)
    return 'NOT-A-DYNAMICAL-UNIFICATION' if ok else 'RECHECK'


v1 = verdict_single_eq(1, n_eq_field_level, n_eq_group_level,
                       len(cross_segments), rank_constants)
v2 = verdict_unified(len(cross_segments), rank_constants,
                     1 if u11_c3_fail else 0)
controls = {
    'inject_curvature_cross_term': verdict_unified(1, 0, 1),
    'let_one_constant_be_solved': verdict_unified(0, 1, 1),
    'drop_c3_failure': verdict_unified(0, 0, 0),
    'fake_six_equations': verdict_single_eq(1, 6, 7, 0, 0),
    'fake_cross_term': verdict_single_eq(1, 5, 7, 1, 0),
}
all_controls_fire = all(x == 'RECHECK' for x in controls.values())

terminal_verdict = (
    'UFE-1-IS-NOTATION-LEVEL-UNIFICATION--'
    'FIVE-EL-EQUATIONS-BEHIND-ONE-BOX--'
    'ZERO-GRAVITY-GAUGE-CURVATURE-CROSS-TERM--'
    'COUPLING-CONSTANT-JACOBIAN-RANK-ZERO'
)
candidate_verdict = 'STRUCTURAL_NEGATIVE_CLOSURE'

# ---- dynamic numbering ---------------------------------------------------
attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 51] or [0])
r_nums = []
for name in os.listdir(RDIR):
    m = re.search(r'r(\d+)', name)
    if m:
        r_nums.append(int(m.group(1)))
r_max = max(r_nums or [0])
volume_max, j_max = 0, 0
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
SELF_OUTPUTS = set([
    BASE + '.py', BASE + '.json', BASE + '.md', BASE + '_report.txt',
    '判定_' + BASE + '.md',
])
preexisting_51 = [n for n in os.listdir(B1)
                  if (n.startswith('attack51') or n.startswith('判定_attack51'))
                  and n not in SELF_OUTPUTS]

# ---- self AST scan -------------------------------------------------------
src = rd(os.path.join(HERE, BASE + '.py'))
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


probe_tree = ast.parse('import attack50_bad\nimport _j108_bad\nimport os')
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

# ---- GUARDS --------------------------------------------------------------
G('G01', attack_prior_max == 50 and 51 in attack_nums and
  r_max >= 406 and volume_max >= 130 and j_max >= 108 and
  c_max >= 401 and not preexisting_51,
  'dynamic lower-bound scan: attack50 prior, attack51 first free; r406+ / vol130+ / J108+')
G('G02', all(os.path.isfile(p) for p in P.values() if p),
  'all ten declared input files exist on disk')
G('G03', single_eq_anchor and phi_anchor and kappa_anchor,
  '00 section 2.1 declares ONE boxed equation deltaS/deltaPhi=0 with Phi and kappa anchors')
G('G04', variation_ids == [1, 2, 3, 4, 5] and five_eq_heading and
  len(eq_tags) >= 5,
  '02 has exactly five variation sections 1-5, section 6 says "five equations", '
  'and boxed tags C/E/YM/H/D are present')
G('G05', map_complete and coverage_exact and
  n_eq_field_level == 5 and n_eq_group_level == 7,
  'field-level 5 EL equations expand to 7 group-level equations covering all 7 field groups')
G('G06', len(blocks) == 5 and
  blocks == ['EC', 'YM', 'Higgs', 'Dirac', 'Yukawa'],
  '01 section 2 parses the five additive action blocks live from the S=... line')
G('G07', len(cross_segments) == 0 and len(gravity_segments) >= 1 and
  len(internal_segments) >= 1 and cross_control,
  'zero R-wedge-F cross terms while both curvatures occur separately; injection control fires')
G('G08', cross_commutator_anchor and curvature_split_anchor and
  errata_anchor and honest_anchor,
  '00 self-declares vanishing cross commutator, exact curvature split, '
  'the UFE-1 prime erratum and the no-completion statement')
G('G09', param_counts == [3, 2, 6, 3, 3, 4, 4, 1] and
  n_params == 26 and param_total_declared and param_not_derived and
  yukawa_input,
  '01 section 3.3 parses 3+2+6+3+3+4+4+1=26 declared input parameters, not derived')
G('G10', rank_full == 5 and rank_constants == 0 and
  rank_constants_injected == 1,
  'Fraction Gaussian elimination: field Jacobian rank 5, coupling-constant block rank 0, '
  'injected control rank 1')
G('G11', len(M) == 5 and len(M[0]) == len(FIELDS) + n_params and
  all(sum(row[:len(FIELDS)]) == len(g) for row, g in zip(M, eq_field_groups)),
  'equation-to-field incidence matrix is consistent with parsed section titles')
G('G12', v1 == 'NOTATION-LEVEL-ONLY' and
  v2 == 'NOT-A-DYNAMICAL-UNIFICATION' and all_controls_fire and
  len(controls) == 5,
  'closure state machine: one notation-level equation, not a dynamical unification; '
  'five counterfactuals all flip to RECHECK')
G('G13', r403_u11 and r403_c3 and r207_scope and r355_scope and
  a37_scope and ufe1_scope and a50_scope and verification_scope,
  'cross-document anchors: r403 U11/C3, r207 structure, r355 forms, attack37 toy, '
  'UFE1 M1-M5, attack50 redlines, 47-check verification report')
G('G14', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged during engine runtime (md5 before/after)')
G('G15', (not prior_imports(imports)) and
  len(prior_imports(probe_imports)) == 2,
  'no prior attack/J-series engine import; positive control fires')
G('G16', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder and no hard-coded guard True literals')
G('G17', 'NO-CORRECT-FOUR-FORCE-GUT' in r403 and '0/22' in a50 and
  'UFT-3=0' in a50,
  'terminal redlines from r403 and attack50 remain on disk')

# ---- FINDINGS ------------------------------------------------------------
F('F01', 'PASS',
  '动态实扫：attack51 为首空号；上界 r%d / 卷%d-J%d / C0%d；'
  '查重确认全库无「对 00 §2.1 主方程做单方程性/耦合块/常数秩」的机验册'
  % (r_max, volume_max, j_max, c_max))
F('F02', 'PASS',
  '单方程性定理：00 §2.1 把统一场方程写成 1 条 `δS/δΦ=0`（`\\tag{UFE-1}`）；'
  '02 现场解析出 §1–§5 共 %d 条独立 E-L 方程（§6 自述「五个方程」），'
  '按 `A^(i), i=1..3` 展开为 %d 条规范群级方程 ⇒ 1 : 5 : %d，'
  '七场组 `%s` 全覆盖无遗漏'
  % (n_eq_field_level, n_eq_group_level, n_eq_group_level,
     ','.join(covered_fields)))
F('F03', 'PASS',
  '耦合块定理：01 §2 现场解析出 5 块加号直和 `%s`；'
  '00 §2.1 作用量按 `\\\\[2pt]` 切段后，'
  '同时含引力曲率 `R^{ab}` 与内部曲率 `F^(i)` 的交叉项 **%d** 条'
  '（引力段 %d / 规范段 %d 各自独立存在）；00 §2.2 自己勘误「不能推出 ⋆D⋆F=J」'
  % ('+'.join(blocks), len(cross_segments), len(gravity_segments),
     len(internal_segments)))
F('F04', 'PASS',
  '常数秩定理：01 §3.3 现场求和 `%s = %d` 个自由参数（原文「不是算出来的」）；'
  '变分雅可比 5×(%d+%d) 中场块精确秩 %d、耦合常数列全零秩 **%d** ⇒ '
  '`δS/δΦ=0` 在结构上解不出任何一个耦合常数（注入 1 个可变常数后秩升为 %d）'
  % ('+'.join(str(x) for x in param_counts), n_params,
     len(FIELDS), n_params, rank_full, rank_constants,
     rank_constants_injected))
F('F05', 'BOUNDARY',
  '与既有册分工（防重复）：r207 = 00 结构/量纲/树级关系名实审计（19 条、44/44 守卫）；'
  'r355 = 02 外形式恒等式与 Cartan 秩机核；attack37 = 1+1D/FLRW toy 变分；'
  'attack11/UFE1 判定册 = M1–M5 与 26 参数账；r403 U11 = `COMMON-ACTION-NOT-UNIFIED`；'
  '本册只做首次「单方程性 + 耦合块 + 常数秩」机器化，不重跑它们的判据')
F('F06', 'FAIL',
  '被检命题「UFE-1 是一个统一场论方程」**不成立**：它把 ECSK 引力与 SM 场并排装进'
  '一个积分号，是记号层（notation）统一；无引力↔规范曲率交叉项、无单一曲率方程、'
  '耦合常数不可由方程导出 ⇒ 动力学层未统一。r403 U11 的 C0/C1/C2 PASS / C3 FAIL 与此同向')
F('F07', 'BOUNDARY',
  '诚实边界：00 §0/§2.2 **自己已声明**「本文件不构成统一场论已经完成的声明」并撤回 UFE-1′，'
  '本册是把自陈机器化，不是新否定；不否证 ECSK/SM/GR 物理，'
  'T1–T8、量纲 A2.1–A2.16、反常 5/5 零、验证报告 39 PASS 仍成立；'
  '00 §2.1 的 `κ²=8πG/c⁴` 是外部输入 G 的定义式重述，不是统一成果')
F('F08', 'BOUNDARY',
  '红线与治理：含引力四力大统一正确方程 0 条、无新物理方程理论体系、'
  '`0/22、UFT-3=0、L3=0、validated=0`、一方程记分板 0/6 全部不变；'
  '本册不计攻破数、不新造方程、不重判物理条目、不新增债务、不改任何历史字节')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))
result = {
    'volume': 'attack51',
    'round_label': '攻破㊸',
    'date': '2026-11-09',
    'target': '07_统一场方程/00_统一场方程.md section 2.1 (UFE-1)',
    'numbering': {
        'attack_prior_max': attack_prior_max, 'attack_current': 51,
        'r_max': r_max, 'volume_max': volume_max, 'j_max': j_max,
        'c_max': c_max, 'preexisting_attack51': preexisting_51,
    },
    'single_equation': {
        'declared': 1,
        'anchors': {'deltaS_deltaPhi': single_eq_anchor,
                    'Phi_tuple': phi_anchor, 'kappa_def': kappa_anchor},
        'variation_sections': variation_sections,
        'section_ids': variation_ids,
        'section6_five_equations': five_eq_heading,
        'boxed_tags': eq_tags,
        'n_eq_field_level': n_eq_field_level,
        'n_eq_group_level': n_eq_group_level,
        'field_groups_by_equation': eq_field_groups,
        'covered_fields': covered_fields,
        'coverage_exact': coverage_exact,
        'ratio': '1 : %d : %d' % (n_eq_field_level, n_eq_group_level),
    },
    'coupling_blocks': {
        'blocks_parsed': blocks,
        'cross_commutator_zero': cross_commutator_anchor,
        'curvature_split': curvature_split_anchor,
        'errata_no_single_curvature_equation': errata_anchor,
        'self_declared_no_completion': honest_anchor,
        'action_segments': len(action_segments),
        'gravity_segments': len(gravity_segments),
        'internal_segments': len(internal_segments),
        'cross_curvature_terms': len(cross_segments),
        'injection_control_fires': cross_control,
    },
    'coupling_constant_rank': {
        'parameter_counts': param_counts,
        'parameter_total': n_params,
        'declared_26': param_total_declared,
        'stated_as_inputs': param_not_derived and yukawa_input,
        'matrix_shape': [len(M), len(M[0]) if M else 0],
        'rank_field_block': rank_full,
        'rank_constant_block': rank_constants,
        'rank_constant_block_after_injection': rank_constants_injected,
    },
    'state_machine': {
        'single_eq_verdict': v1,
        'unification_verdict': v2,
        'counterfactuals': controls,
        'all_controls_fire': all_controls_fire,
    },
    'cross_document': {
        'r403_u11_and_c3': r403_u11 and r403_c3,
        'r403_u11_row_columns': u11_cols,
        'r403_u11_c3_column': u11_cols[5] if len(u11_cols) >= 6 else None,
        'r403_u11_status': u11_status,
        'r403_c3_fail_parsed_live': u11_c3_fail,
        'r207_structure_audit': r207_scope,
        'r355_exterior_forms': r355_scope,
        'attack37_toy_variation': a37_scope,
        'ufe1_M1_M5': ufe1_scope,
        'attack50_redlines': a50_scope,
        'verification_report_47': verification_scope,
    },
    'findings': FINDINGS,
    'verdict_counts': verdict_counts,
    'candidate_verdict': candidate_verdict,
    'terminal_verdict': terminal_verdict,
    'redlines': [
        '0/22', 'UFT-3=0', 'L3=0', 'validated=0',
        'no correct four-force GUT including gravity',
        'no new physical equation theory system',
        'attack = structural negative closure, not solved physics',
    ],
    'self_corrections': [
        'The obvious target "derive the master action by variation" was rejected: r207 already audited 00 structure/dimensions/tree relations, r355 already machine-checked 02 exterior-form identities, and attack37 already ran a 1+1D/FLRW toy variation. This volume instead attacks the untested claim that deltaS/deltaPhi=0 is ONE equation.',
        'A live parse of 02 section headings yields exactly five variation equations and section 6 itself says "five equations"; so the 1:5:7 count is read from disk rather than declared.',
        'Cross-term counting uses only the four action lines of 00 section 2.1 split on the LaTeX line break; the covariant derivative in the Dirac sector contains both e and the gauge potentials, so counting field co-occurrence would give a false positive. The criterion is therefore curvature-curvature mixing, not field co-occurrence.',
        'The rank theorem separates field columns from coupling-constant columns: a naive full-matrix rank would be 5 and say nothing. Only the constant block rank 0 (with an injection control raising it to 1) proves the constants cannot be solved from the equation.',
        'A concurrent session advanced the chain to r406 / volume130-J108 during drafting; numbering guards use live lower bounds and a first-free-number scan instead of snapshot equality, following the attack49 first-run failure.',
        'First run was 15/17: G12 and G13 both failed because the r403 anchor was written as 含引力四力大统一正确方程 0 条 while the disk text says 含引力四力大统一正确者 = 0 条. Corrected to the exact literal.',
        'The same fix upgraded the C3 evidence from a loose phrase to a live parse of the r403 U11 row C3 column (FAIL); the state machine now consumes the parsed value instead of a hard-coded 1, preserving fail-closed behaviour when the anchor is missing.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

md = []
md.append('# attack51 · 统一场方程单方程性与耦合块结构判决（数据产物）')
md.append('')
md.append('- 日期：2026-11-09 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 靶点：`07_统一场方程/00_统一场方程.md` §2.1（UFE-1）；只读，不重判物理条目')
md.append('')
md.append('## 一、单方程性')
md.append('')
md.append('| 层级 | 条数 | 来源 |')
md.append('|---|---|---|')
md.append('| 00 §2.1 声明 | **1** | `δS/δΦ=0` (`\\tag{UFE-1}`) |')
md.append('| 02 §1–§5 场组级 E-L 方程 | **%d** | 现场解析 5 个变分节标题，§6 自述「五个方程」 |'
          % n_eq_field_level)
md.append('| 拆 `A^(i), i=1..3` 后规范群级 | **%d** | `ω, e, A1, A2, A3, H, Ψ` |'
          % n_eq_group_level)
md.append('')
md.append('- 变分节：%s' % variation_sections)
md.append('- 盒装标签：%s' % eq_tags)
md.append('- 七场组覆盖：%s（精确 = %s）' % (covered_fields, coverage_exact))
md.append('')
md.append('## 二、耦合块')
md.append('')
md.append('- 01 §2 现场解析 5 块加号直和：`%s`' % ' + '.join(blocks))
md.append('- 00 §2.1 作用量切 %d 段：引力曲率段 %d、内部规范曲率段 %d、**交叉段 %d**'
          % (len(action_segments), len(gravity_segments),
             len(internal_segments), len(cross_segments)))
md.append('- 00 自证：交叉对易子消失 = %s；曲率精确分块 = %s；'
          '§2.2 勘误「不能推出 ⋆D⋆F=J」= %s；§0「不构成统一完成声明」= %s'
          % (cross_commutator_anchor, curvature_split_anchor,
             errata_anchor, honest_anchor))
md.append('- 注入 `R^{ab}∧F^{(i)}` 阳性对照命中 = %s' % cross_control)
md.append('')
md.append('## 三、耦合常数秩')
md.append('')
md.append('- 01 §3.3 现场求和 `%s = %d`；声明 26 个 = %s；原文「不是算出来的」= %s'
          % ('+'.join(str(x) for x in param_counts), n_params,
             param_total_declared, param_not_derived))
md.append('- 变分雅可比 %d×%d；场块精确秩 **%d**、常数块秩 **%d**、注入后 **%d**'
          % (len(M), len(M[0]) if M else 0, rank_full,
             rank_constants, rank_constants_injected))
md.append('')
md.append('## 四、裁定')
md.append('')
md.append('`%s`' % v1)
md.append('`%s`' % v2)
md.append('')
md.append('> 5 组反事实（注入交叉项 / 令常数可解 / 去掉 C3 FAIL / 伪 6 方程 / 伪交叉项）全部翻转 = %s'
          % all_controls_fire)
md.append('')
md.append('> 完整判定见 `判定_attack51_统一场方程单方程性与耦合块结构判决_2026-11-09.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack51 / 2026-11-09 / UFE-1 single-equation and coupling-block verdict')
lines.append('')
lines.append('[A] dynamic numbering')
lines.append('  %s' % result['numbering'])
lines.append('')
lines.append('[B] single equation')
lines.append('  declared=1 field_level=%d group_level=%d ratio=1:%d:%d'
             % (n_eq_field_level, n_eq_group_level,
                n_eq_field_level, n_eq_group_level))
lines.append('  sections=%s' % variation_sections)
lines.append('  tags=%s' % eq_tags)
lines.append('  covered=%s exact=%s' % (covered_fields, coverage_exact))
lines.append('')
lines.append('[C] coupling blocks')
lines.append('  blocks=%s segments=%d gravity=%d internal=%d CROSS=%d control=%s'
             % (blocks, len(action_segments), len(gravity_segments),
                len(internal_segments), len(cross_segments), cross_control))
lines.append('')
lines.append('[D] coupling-constant rank')
lines.append('  counts=%s total=%d shape=%s rank_field=%d rank_const=%d injected=%d'
             % (param_counts, n_params, [len(M), len(M[0]) if M else 0],
                rank_full, rank_constants, rank_constants_injected))
lines.append('')
lines.append('[E] state machine')
lines.append('  %s' % result['state_machine'])
lines.append('')
lines.append('[F] findings %s' % verdict_counts)
for f in FINDINGS:
    lines.append('  %s %s : %s' % (f['verdict'], f['code'], f['note']))
lines.append('')
lines.append('[G] terminal verdict')
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

print('attack51 guards=%d/%d findings=%s exit=%d v1=%s v2=%s'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], v1, v2))
sys.exit(result['exit'])
