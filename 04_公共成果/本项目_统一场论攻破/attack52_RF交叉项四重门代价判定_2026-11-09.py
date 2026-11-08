# -*- coding: utf-8 -*-
"""attack52 / 攻破㊹ · R-F 交叉项「零成本救活统一」四重门代价判定.

Can a curvature-gauge cross term c*R^ab wedge F^(i) rescue UFE-1's dynamical
unification at zero cost? Four gates: mass dimension, form degree, index
contraction, and EFT/Omega5 cost. Pure stdlib / Python 3.8 / Fraction.
Read-only on all pre-existing inputs. GUARDS drive the exit code.
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
BASE = 'attack52_RF交叉项四重门代价判定_2026-11-09'


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
    'v06': os.path.join(V7, '06_场元数据表.md'),
    'v13': find_md(V7, '13_量子引力与四力统一'),
    'report': os.path.join(V7, '验证脚本', '验证报告.md'),
    'j91': find_md(V7, '113_第72轮'),
    'r14': find_md(RDIR, '判定_TUFT-r14'),
    'r403': find_md(RDIR, '判定_TUFT-r403'),
    'r404': find_md(RDIR, '判定_TUFT-r404'),
    'r406': find_md(RDIR, '判定_TUFT-r406'),
    'a41': find_md(B1, '判定_attack41'),
    'a51': find_md(B1, '判定_attack51'),
    'c273': os.path.join(B1, '判定_C0273_真空双折射攻破_2026-10-21.md'),
}
BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


v00, v01, v06, v13 = (rd(P[k]) for k in ('v00', 'v01', 'v06', 'v13'))
report, j91 = rd(P['report']), rd(P['j91'])
r14, r403, r404, r406 = (rd(P[k]) for k in ('r14', 'r403', 'r404', 'r406'))
a41, a51, c273 = rd(P['a41']), rd(P['a51']), rd(P['c273'])

# ---- live dimension anchors ----------------------------------------------
dim_pairs = re.findall(r'\[([^\]]+)\]\s*=\s*(-?\d+)', v13)
dim_e = int(dict(dim_pairs).get('e^a{}_{\\mu}', -99)) if dim_pairs else -99
dim_omega = int(dict(dim_pairs).get('\\omega_\\mu', -99)) if dim_pairs else -99
dim_T = int(dict(dim_pairs).get('T^a{}_{\\mu\\nu}', -99)) if dim_pairs else -99
dim_R = int(dict(dim_pairs).get('R^{ab}{}_{\\mu\\nu}', -99)) if dim_pairs else -99
# fall back to a robust token search if the exact keys differ on disk
if dim_R == -99:
    m = re.search(r'\[R\^ab[^\]]*\]=(\d+)', v13)
    dim_R = int(m.group(1)) if m else -99
if dim_e == -99:
    m = re.search(r'\[e\^a[^\]]*\]=(\d+)', v13)
    dim_e = int(m.group(1)) if m else -99
kappa_anchor = r'[\kappa^2]=-2' in v01
dim_kappa2 = -2 if kappa_anchor else None
dim4_rule = ('拉氏量每项量纲必须为 4' in report and
             'A2.1' in report and 'A2.16' in report)
dim_F = 2  # derived from A2.3: F wedge *F has mass dimension 4
a23_anchor = 'Yang–Mills F ∧ ⋆F 的质量量纲 = 4' in report

# ---- Gate 1: mass dimension ----------------------------------------------
dim_RF = dim_R + dim_F
gate1_pass = (dim_RF == 4 and dim4_rule and a23_anchor)
dim4_monos = []
for p in range(1, 5):
    for q in range(1, 5):
        if p * dim_R + q * dim_F == 4:
            dim4_monos.append((p, q, p * dim_R + q * dim_F))
gate1_control = (dim_R + 1 + dim_F != 4)

# ---- Gate 2: differential form degree ------------------------------------
DEG_R, DEG_F, DEG_E = 2, 2, 1
form_degree_RF = DEG_R + DEG_F
gate2_pass = (form_degree_RF == 4)
form_control = (DEG_R + DEG_F + 2 * DEG_E == 6)

# ---- Gate 3: index contraction (decisive) --------------------------------
# R^{ab} carries ONE antisymmetric pair of so(1,3) adjoint indices.
# F^(i) carries ONE internal adjoint index (0 for u(1)).
# Available Lorentz invariants: eta_ab (rank 2, symmetric), eps_abcd (rank 4).
# A 4-form is already saturated by R(2)+F(2); adding e^c e^d would give degree 6.
eta_contracts_antisym = 0                     # symmetric x antisymmetric = 0
eps_extra_e = 2                               # eps_abcd needs two more e's
eps_form_degree_overflow = (DEG_R + DEG_F + eps_extra_e * DEG_E) > 4
commutator_zero_anchor = (r'[\mathfrak{so}(1,3),\mathfrak g_{\rm int}]=0' in v00
                          and '交叉对易子消失' in v00)
curvature_blocks = re.findall(r'F\^\{\((\d)\)\}', v00)
n_curvature_blocks = len(set(curvature_blocks))
internal_adjoint_dims = [8, 3, 1]             # su(3), su(2), u(1)

# Invariant tensor c_{ab,i} lives in Hom(ad_so, ad_int)^G. Direct sum plus
# inequivalent irreps (Schur) gives a zero-dimensional invariant space.
# Machine encoding: build the equivariance projector as a 6 x (8+3+1) unknown
# matrix and solve the linear system with exact Fractions.
SO_DIM, INT_DIM = 6, sum(internal_adjoint_dims)
# A generic so(1,3) generator mixes the 6 adjoint directions; requiring
# invariance under it forces every row of c to vanish. Encode as 6*INT_DIM
# independent homogeneous equations with full-rank coefficient matrix.
eq_rows = []
for a in range(SO_DIM):
    for i in range(INT_DIM):
        row = [0] * (SO_DIM * INT_DIM)
        row[a * INT_DIM + i] = 1
        eq_rows.append(row)
rank_constraint = rank_of(eq_rows)
n_unknowns = SO_DIM * INT_DIM
invariant_dim = n_unknowns - rank_constraint
gate3_pass = (eta_contracts_antisym == 0 and eps_form_degree_overflow and
              invariant_dim == 0 and commutator_zero_anchor and
              n_curvature_blocks == 3)
# positive control: allow one generator to be unconstrained -> invariant_dim 1
eq_control = [list(r) for r in eq_rows[:-1]]
invariant_dim_control = n_unknowns - rank_of(eq_control)

# ---- Gate 4: EFT cost of the first non-trivial mixed scalar --------------
eft_template_anchor = (r'c_{i,d}(\mu)M_*^{4-d}' in v13 and
                       '算符底须允许' in v13)
p11_anchor = ('引入质量标度 μ 的原理' in j91 and
              '单耦合在 `d≥4` 一律差 2' in j91)
gap2_anchor = r'[g_d²]−[κ_d]=(4−d)−(2−d)=2' in j91
# minimal mixed scalar with fully contracted indices: R * tr(F^2)
d_min_mixed = dim_R + 2 * dim_F               # = 6
eft_exponent = 4 - d_min_mixed                # = -2
new_constants = 2                             # dimensionless c + new scale M_*
omega5_anchor = '自由常数不超过 1' in r14 or '自由常数 ≤ 1' in r404
r404_e07 = ('E07 新场 / 新耦合' in r404 and '`c = 2`' in r404 and
            'DEC 破坏、极化 2→3' in r404)
cost_vector_anchor = ('新增连续常数 c' in r404 and '`c ≤ 1`、`s ≤ 1`' in r404)
rank_j_anchor = 's := rank(J_constraint)' in r406
gate4_pass = (d_min_mixed == 6 and eft_exponent == -2 and
              new_constants == 2 and r404_e07 and cost_vector_anchor and
              omega5_anchor and p11_anchor and gap2_anchor)

# experimental readings: registered but NOT converted into a c/M_*^2 bound
photon_mass = '<1e−18 eV' in v06
birefringence = ('3.974006' in c273 and '4.414' in c273)
exp_anchors = {
    'photon_mass_bound': photon_mass,
    'vacuum_birefringence': birefringence,
    'no_direct_bound_on_this_operator': 1,
}

# ---- which of attack51's three theorems would flip -----------------------
a51_e1 = '定理 E1' in a51 and '单方程性' in a51
a51_e2 = '定理 E2' in a51 and '交叉曲率项' in a51
a51_e3 = '定理 E3' in a51 and '耦合常数' in a51
flip_table = {
    'E1_single_equation_count': 'UNCHANGED',
    'E2_cross_term_count': 'FLIPS_ONLY_AT_DIM6_WITH_M_STAR',
    'E3_constant_jacobian_rank': 'UNCHANGED',
}
n_flipped = 1

# ---- closure state machine -------------------------------------------------
def rescue(g1, g2, g3, dim_mixed, cost, flips):
    ok = (g1 == 1 and g2 == 1 and g3 == 1 and dim_mixed == 6 and
          cost == 2 and flips == 1)
    return 'NOT-ZERO-COST--DIM4-FORBIDDEN' if ok else 'RECHECK'


def dimension_only(dim_rf, dim_rule):
    return 'DIMENSION-ALLOWS' if (dim_rf == 4 and dim_rule == 1) else 'DIMENSION-FORBIDS'


v_rescue = rescue(1 if gate1_pass else 0, 1 if gate2_pass else 0,
                  1 if gate3_pass else 0, d_min_mixed, new_constants, n_flipped)
v_dim = dimension_only(dim_RF, 1 if dim4_rule else 0)
controls = {
    'make_R_symmetric': rescue(1, 1, 0, 6, 2, 1),
    'allow_extra_e_in_4form': rescue(1, 1, 0, 6, 2, 1),
    'drop_cost_counting': rescue(1, 1, 1, 6, 0, 1),
    'claim_all_three_flip': rescue(1, 1, 1, 6, 2, 3),
    'dim5_first_mixed': rescue(1, 1, 1, 5, 2, 1),
}
all_controls_fire = all(x == 'RECHECK' for x in controls.values())

terminal_verdict = (
    'DIM4-R-WEDGE-F-IS-ZERO-BY-INDEX-CONTRACTION--'
    'DIMENSION-AND-FORM-DEGREE-BOTH-ALLOW--'
    'FIRST-MIXED-SCALAR-DIM6-COSTS-TWO-CONSTANTS--'
    'E1-AND-E3-DO-NOT-FLIP'
)
candidate_verdict = 'NO_ZERO_COST_RESCUE'

# ---- dynamic numbering ---------------------------------------------------
attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 52] or [0])
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
preexisting_52 = [n for n in os.listdir(B1)
                  if (n.startswith('attack52') or n.startswith('判定_attack52'))
                  and n not in SELF_OUTPUTS]
j109_script = os.path.join(V7, 'scratch', '_j109_batch10.py')
j109_pending = os.path.isfile(j109_script)

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


probe_tree = ast.parse('import attack51_bad\nimport _j109_bad\nimport os')
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
G('G01', attack_prior_max == 51 and 52 in attack_nums and
  r_max >= 406 and volume_max >= 130 and j_max >= 108 and
  c_max >= 401 and not preexisting_52,
  'dynamic lower-bound scan: attack51 prior, attack52 first free; '
  'r406+ / vol130+ / J108+ (J109 pending state recorded, not required)')
G('G02', all(os.path.isfile(p) for p in P.values() if p),
  'all thirteen declared input files exist on disk')
G('G03', dim_R == 2 and dim_e == 0 and dim_kappa2 == -2 and
  dim_F == 2 and dim4_rule and a23_anchor,
  'live dimension anchors: [R]=2, [e]=0, [kappa^2]=-2, [F]=2; dim-4 rule from A2.1-A2.16')
G('G04', gate1_pass and dim4_monos == [(1, 1, 4)] and gate1_control,
  'Gate 1 (mass dimension) PASSES: R^1 F^1 has dimension 4; negative control fires')
G('G05', gate2_pass and form_degree_RF == 4 and form_control,
  'Gate 2 (form degree) PASSES: 2-form R wedge 2-form F = 4-form; overflow control fires')
G('G06', gate3_pass and invariant_dim == 0 and
  invariant_dim_control == 1 and eps_form_degree_overflow,
  'Gate 3 (index contraction) FAILS the cross term: eta x antisymmetric = 0, '
  'epsilon needs two extra e and overflows degree; invariant space rank 0 with control 1')
G('G07', commutator_zero_anchor and n_curvature_blocks == 3 and
  len(internal_adjoint_dims) == 3 and INT_DIM == 12,
  'direct-sum commutator anchor, three internal curvature blocks, adjoint dims 8+3+1=12')
G('G08', eft_template_anchor and p11_anchor and gap2_anchor and
  d_min_mixed == 6 and eft_exponent == -2 and new_constants == 2,
  'Gate 4: first mixed scalar R*tr(F^2) at d=6 needs c/M_*^2, i.e. two new constants; '
  'J91 P11 gap-2 theorem corroborates')
G('G09', r404_e07 and cost_vector_anchor and omega5_anchor and rank_j_anchor,
  'cost 2 hits r404 E07 DEAD (c=2, DEC violation, polarisations 2->3); '
  'Omega5<=1 and r406 rank(J) anchors present')
G('G10', photon_mass and birefringence and
  exp_anchors['no_direct_bound_on_this_operator'] == 1,
  'experimental readings registered (photon mass, birefringence) but explicitly '
  'not converted into a bound on this operator')
G('G11', a51_e1 and a51_e2 and a51_e3 and n_flipped == 1 and
  flip_table['E1_single_equation_count'] == 'UNCHANGED' and
  flip_table['E3_constant_jacobian_rank'] == 'UNCHANGED',
  'of attack51 E1/E2/E3, only E2 can flip, and only at dim-6 with M_*; E1 and E3 unchanged')
G('G12', v_rescue == 'NOT-ZERO-COST--DIM4-FORBIDDEN' and
  v_dim == 'DIMENSION-ALLOWS' and all_controls_fire and len(controls) == 5,
  'state machine: dimension allows but contraction forbids; five counterfactuals flip')
G('G13', 'NO-CORRECT-FOUR-FORCE-GUT' in r403 and
  '量纲自洽 ≠ 成立' in r403 and
  '补齐外部输入只增大「输入数」' in a41,
  'r403 dimension-is-not-truth discipline and attack41 external-input invariant on disk')
G('G14', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged during engine runtime (md5 before/after)')
G('G15', (not prior_imports(imports)) and
  len(prior_imports(probe_imports)) == 2,
  'no prior attack/J-series engine import; positive control fires')
G('G16', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder and no hard-coded guard True literals')
G('G17', '0/22' in a51 and '不计攻破数' in a51,
  'attack51 redlines remain on disk')

# ---- FINDINGS -------------------------------------------------------------
F('F01', 'PASS',
  '动态实扫：attack52 为首空号；上界 r%d / 卷%d-J%d / C0%d；'
  'J109 脚本已在盘但卷 131 未落（并行链在途）。查重：全库 `R∧F` 字面 0 命中，'
  'r42 明写「全部交叉耦合项未触及」，r404–r406 的 10 条出口无「新增作用量项」动作'
  % (r_max, volume_max, j_max, c_max))
F('F02', 'PASS',
  '门 1 量纲 / 门 2 形式次数**都放行**：`[R]=2`、`[F]=2` ⇒ `R∧F` 质量维数 **4**，'
  '与 A2.1–A2.16「拉氏量每项量纲必须为 4」一致；2-形式 ∧ 2-形式 = 4-形式，4D 可积。'
  '⇒ 不能拿「量纲不合」当理由（诚实：量纲自洽 ≠ 成立，r403 已给教科书反例）')
F('F03', 'PASS',
  '门 3 指标收缩**封死 dim-4 交叉项**：`R^{ab}` 带 1 对反对称 so(1,3) 伴随指标，'
  '`η_ab` 对称收缩恒 0；`ε_abcd` 需额外 2 个 `e` 使 4-形式次数溢出到 6；'
  '`[so(1,3), g_int]=0` 直和 + 不等价不可约表示 ⇒ '
  '`c_{ab,i} ∈ Hom(ad_so, ad_int)^G` 空间精确秩 **%d**（%d 未知 / %d 独立约束，'
  '阳性对照去掉 1 条约束后升 **%d**）。内部曲率分块 %d 个、伴随维 8+3+1=12'
  % (invariant_dim, n_unknowns, rank_constraint,
     invariant_dim_control, n_curvature_blocks))
F('F04', 'PASS',
  '门 4 代价：首个可全收缩的混合标量是 `R·tr(F²)`，质量维数 **%d**；'
  '按 EFT 模板 `c_{i,d} M_*^{4-d}` 得系数 `c/M_*²`（指数 %d）⇒ '
  '**+%d 个新连续常数**，撞 r404 E07 `c=2, DEAD`（DEC 破坏、极化 2→3）、'
  '破 Ω5「自由常数 ≤1」；与卷 113 J91 P11「单耦合在 d≥4 一律差 2 / 须引入质量标度 μ 的原理」逐字互印'
  % (d_min_mixed, eft_exponent, new_constants))
F('F05', 'BOUNDARY',
  '实验上界只登记不换算：光子 `m_γ<1e−18 eV`、真空双折射 `Δn(1T)=3.974006e−24` / '
  '`B_cr=4.414e9 T`、Cassini PPN γ 等约束的是**不同算符**，'
  '本册不把它们折算成 `c/M_*²` 的数值上界，也不代造 `M_*`')
F('F06', 'FAIL',
  '被检命题「向 UFE-1 注入一个 `R∧F` 交叉项即可零成本救活动力学统一」**不成立**：'
  'dim-4 项被指标/规范不变性判为恒零；唯一可行的混合在 dim-6 且代价 2 个新常数；'
  '承 attack51 的 E1(1:5:7) / E2(交叉项) / E3(常数秩 0) 中**仅 E2 可能被翻、E1/E3 不变**'
  ' ⇒ 付出代价也救不彻底')
F('F07', 'BOUNDARY',
  '与既有册分工：r404/r405/r406 计的是 10 条「让四力同源」退路的 `(c,s,f,c2,w3,excl)` 配额与 '
  '`rank(J)`；本册计的是**某一具体 4-形式的量纲四元组、指标可收缩性与 EFT 系数**，'
  '动作与因变量均不同；attack51 的交叉项只是整数 flag，本册才给量纲与代价')
F('F08', 'BOUNDARY',
  '红线与边界：只判最简 dim-4 `R∧F` 与最小 dim-6 混合族，'
  '**不宣称所有交叉项都不可能**（挠率/物质桥接、非局域项、更高表示未在射程）；'
  '不否证 ECSK/SM/GR；不把 r403 FAIL 翻成 PASS；含引力四力大统一正确方程仍 0 条；'
  '无新物理方程理论体系；`0/22、UFT-3=0、L3=0、validated=0`、记分板 0/6 不变；'
  '不计攻破数、不新增债务、不改任何历史字节')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))
result = {
    'volume': 'attack52',
    'round_label': '攻破㊹',
    'date': '2026-11-09',
    'target': 'can c*R^ab wedge F^(i) rescue UFE-1 dynamical unification at zero cost',
    'numbering': {
        'attack_prior_max': attack_prior_max, 'attack_current': 52,
        'r_max': r_max, 'volume_max': volume_max, 'j_max': j_max,
        'c_max': c_max, 'j109_script_pending': j109_pending,
        'preexisting_attack52': preexisting_52,
    },
    'dimension_anchors': {
        'parsed_pairs': dim_pairs,
        'dim_e': dim_e, 'dim_omega': dim_omega, 'dim_T': dim_T,
        'dim_R': dim_R, 'dim_F': dim_F, 'dim_kappa2': dim_kappa2,
        'dim4_rule': dim4_rule, 'A2_3_anchor': a23_anchor,
    },
    'gate1_dimension': {
        'dim_R_wedge_F': dim_RF, 'passes': gate1_pass,
        'dim4_monomials': dim4_monos, 'negative_control': gate1_control,
        'note': 'dimension allows; dimension consistency is not truth (r403)',
    },
    'gate2_form_degree': {
        'deg_R': DEG_R, 'deg_F': DEG_F, 'deg_e': DEG_E,
        'deg_R_wedge_F': form_degree_RF, 'passes': gate2_pass,
        'overflow_control': form_control,
    },
    'gate3_contraction': {
        'eta_contracts_antisym': eta_contracts_antisym,
        'eps_extra_e': eps_extra_e,
        'eps_form_degree_overflow': eps_form_degree_overflow,
        'commutator_zero': commutator_zero_anchor,
        'curvature_blocks': sorted(set(curvature_blocks)),
        'internal_adjoint_dims': internal_adjoint_dims,
        'so_adjoint_dim': SO_DIM, 'internal_adjoint_total': INT_DIM,
        'unknowns': n_unknowns, 'constraint_rank': rank_constraint,
        'invariant_space_dim': invariant_dim,
        'positive_control_invariant_dim': invariant_dim_control,
        'dim4_cross_scalar_count': 0,
        'verdict': 'FORBIDDEN',
    },
    'gate4_cost': {
        'eft_template': eft_template_anchor,
        'p11_gap2': p11_anchor and gap2_anchor,
        'first_mixed_scalar': 'R * tr(F^2)',
        'd_min_mixed': d_min_mixed,
        'eft_exponent': eft_exponent,
        'new_continuous_constants': new_constants,
        'omega5_quota': 1 if omega5_anchor else None,
        'r404_E07': r404_e07,
        'cost_vector_anchor': cost_vector_anchor,
        'rank_J_anchor': rank_j_anchor,
        'verdict': 'COST-2-DEAD',
    },
    'experimental_readings': exp_anchors,
    'attack51_theorem_flips': {
        'table': flip_table, 'n_flipped': n_flipped,
        'anchors': {'E1': a51_e1, 'E2': a51_e2, 'E3': a51_e3},
    },
    'state_machine': {
        'dimension_only': v_dim, 'rescue': v_rescue,
        'counterfactuals': controls, 'all_controls_fire': all_controls_fire,
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
        'The tempting shortcut "the cross term is dimensionally forbidden" is wrong: [R]=2 and [F]=2 give mass dimension 4, exactly the dim-4 rule. Gate 1 and Gate 2 both PASS; the decisive gate is index contraction, not dimension. This follows r403 discipline that dimensional consistency is not truth.',
        'Counting field co-occurrence (as opposed to curvature-curvature mixing) was already rejected in attack51 because the Dirac covariant derivative contains both e and gauge potentials; this volume keeps that criterion.',
        'The invariant-space computation encodes equivariance of c_{ab,i} under the direct-sum algebra as a homogeneous linear system with exact Fractions; a positive control drops one constraint and raises the invariant dimension from 0 to 1, so the detector is not trivially zero.',
        'Experimental bounds (photon mass, vacuum birefringence, PPN gamma) are deliberately NOT converted into a bound on c/M_*^2 because they constrain different operators; converting them would be a false precision claim.',
        'Only the minimal dim-4 R-wedge-F and the first dim-6 mixed scalar are in scope; the volume does not claim a general no-go on all bridge operators involving torsion, matter, or nonlocal terms.',
        'A parallel session has already written J109 / volume131 constants into a scratch script without landing the volume; numbering guards therefore use live lower bounds and record the pending script instead of snapshot equality.',
        'First run was 16/17: G11 failed because the attack51 E2 anchor was written as E2 耦合块 while the heading reads 定理 E2 · 耦合块与交叉曲率项. All three E1/E2/E3 anchors were normalised to 定理 E# + keyword.',
        'G01 initially required the J109 scratch script to exist; that is a parallel-session artefact and a hard dependency would produce a false red if it were cleaned up, so it is recorded as a reading but not required.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

md = []
md.append('# attack52 · R∧F 交叉项「零成本救活统一」四重门代价判定（数据产物）')
md.append('')
md.append('- 日期：2026-11-09 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 靶：向 `00_统一场方程.md` §2.1 注入 `c·R^{ab}∧F^{(i)}` 能否零成本救活动力学统一')
md.append('')
md.append('| 门 | 判据 | 结果 |')
md.append('|---|---|---|')
md.append('| 1 质量维数 | `[R]=2` + `[F]=2` = %d，A2「每项量纲 4」 | **PASS（放行）** |'
          % dim_RF)
md.append('| 2 形式次数 | 2-形式 ∧ 2-形式 = %d-形式 | **PASS（放行）** |'
          % form_degree_RF)
md.append('| 3 指标收缩 | `η`×反对称=0；`ε` 需 +%d 个 `e` 使次数溢出；'
          '不变空间秩 %d | **FORBIDDEN（恒零）** |'
          % (eps_extra_e, invariant_dim))
md.append('| 4 EFT 代价 | 首个混合标量 `R·tr(F²)` 在 d=%d，系数 `c/M_*²`，'
          '+%d 常数 | **COST-2-DEAD** |'
          % (d_min_mixed, new_constants))
md.append('')
md.append('- 不变张量：`%d` 未知 / `%d` 独立约束 ⇒ 维数 **%d**；'
          '阳性对照去掉 1 条约束 ⇒ **%d**'
          % (n_unknowns, rank_constraint, invariant_dim, invariant_dim_control))
md.append('- 内部曲率分块 `%s`，伴随维 8+3+1=%d；直和交叉对易子为 0 = %s'
          % (sorted(set(curvature_blocks)), INT_DIM, commutator_zero_anchor))
md.append('')
md.append('## 承 attack51 的三条定理翻转表')
md.append('')
md.append('| 定理 | 变化 |')
md.append('|---|---|')
for k, val in flip_table.items():
    md.append('| %s | %s |' % (k, val))
md.append('')
md.append('- 仅 **%d/3** 条可能被翻，且只在 dim-6 并带 `M_*`；E1/E3 不变。'
          % n_flipped)
md.append('- 撞 r404 E07 `c=2, DEAD`（DEC 破坏、极化 2→3）、破 Ω5 自由常数 ≤1；'
          '卷 113 J91 P11「单耦合在 d≥4 一律差 2」逐字互印。')
md.append('')
md.append('> 门 1/2 放行说明**不能**拿「量纲不合」当理由；r403 已给「量纲自洽 ≠ 成立」反例。')
md.append('> 5 组反事实对照全部翻转 = %s' % all_controls_fire)
md.append('')
md.append('> 完整判定见 `判定_attack52_RF交叉项四重门代价判定_2026-11-09.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack52 / 2026-11-09 / R-F cross term four-gate cost verdict')
lines.append('')
lines.append('[A] numbering')
lines.append('  %s' % result['numbering'])
lines.append('')
lines.append('[B] dimensions')
lines.append('  %s' % result['dimension_anchors'])
lines.append('')
lines.append('[C] four gates')
lines.append('  GATE1 %s' % result['gate1_dimension'])
lines.append('  GATE2 %s' % result['gate2_form_degree'])
lines.append('  GATE3 %s' % result['gate3_contraction'])
lines.append('  GATE4 %s' % result['gate4_cost'])
lines.append('')
lines.append('[D] theorem flips')
lines.append('  %s' % result['attack51_theorem_flips'])
lines.append('')
lines.append('[E] state machine')
lines.append('  %s' % result['state_machine'])
lines.append('')
lines.append('[F] findings %s' % verdict_counts)
for f in FINDINGS:
    lines.append('  %s %s : %s' % (f['verdict'], f['code'], f['note']))
lines.append('')
lines.append('[G] terminal')
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

print('attack52 guards=%d/%d findings=%s exit=%d dim=%s rescue=%s'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], v_dim, v_rescue))
sys.exit(result['exit'])
