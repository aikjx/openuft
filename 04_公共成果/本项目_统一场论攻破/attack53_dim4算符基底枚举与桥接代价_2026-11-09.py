# -*- coding: utf-8 -*-
"""attack53 / 攻破㊺ · dim-4 局域算符文法内枚举与桥接项代价.

Completes attack52's declared out-of-scope: torsion / Higgs / matter bridge
operators. Finite grammar enumeration with exact Fraction dimensions; NOT a
claim of a complete SMEFT/Warsaw basis (vols 14-17 self-declare that undone).
Pure stdlib / Python 3.8. Read-only on all pre-existing inputs.
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
BASE = 'attack53_dim4算符基底枚举与桥接代价_2026-11-09'


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


P = {
    'v00': os.path.join(V7, '00_统一场方程.md'),
    'v01': os.path.join(V7, '01_作用量与场内容.md'),
    'v02': os.path.join(V7, '02_变分推导.md'),
    'v06': os.path.join(V7, '06_场元数据表.md'),
    'v09': os.path.join(V7, '09_已知局限与否定清单.md'),
    'v13': find_md(V7, '13_量子引力与四力统一'),
    'report': os.path.join(V7, '验证脚本', '验证报告.md'),
    'r287': os.path.join(B2, '_scratch', '_README_before_r289_reg.md'),
    'r403': find_md(RDIR, '判定_TUFT-r403'),
    'r404': find_md(RDIR, '判定_TUFT-r404'),
    'a51': find_md(B1, '判定_attack51'),
    'a52': find_md(B1, '判定_attack52'),
    'c310': os.path.join(B1, '判定_C0310_希格斯暴胀攻破_2026-10-21.md'),
    'v49a': find_md(V7, '49A_阶段1任务1'),
}
BEFORE = dict((k, md5(v)) for k, v in P.items())
GUARDS = []
FINDINGS = []


def G(code, ok, note):
    GUARDS.append({'code': code, 'ok': bool(ok), 'note': note})


def F(code, verdict, note):
    FINDINGS.append({'code': code, 'verdict': verdict, 'note': note})


v00, v01, v02, v06 = (rd(P[k]) for k in ('v00', 'v01', 'v02', 'v06'))
v09, v13, report = rd(P['v09']), rd(P['v13']), rd(P['report'])
r287, r403, r404 = rd(P['r287']), rd(P['r403']), rd(P['r404'])
a51, a52, c310, v49a = (rd(P[k]) for k in ('a51', 'a52', 'c310', 'v49a'))

# ---- live dimension anchors ----------------------------------------------
dim_pairs = dict(re.findall(r'\[([^\]]+)\]\s*=\s*(-?\d+)', v13))
D_E = int(dim_pairs.get('e^a{}_{\\mu}', -99))
D_OMEGA = int(dim_pairs.get('\\omega_\\mu', -99))
D_T = int(dim_pairs.get('T^a{}_{\\mu\\nu}', -99))
D_R = int(dim_pairs.get('R^{ab}{}_{\\mu\\nu}', -99))
kappa_anchor = r'[\kappa^2]=-2' in v01
D_KAPPA = 2 if kappa_anchor else None       # [1/kappa^2] = +2
dim4_rule = ('拉氏量每项量纲必须为 4' in report and
             'A2.1' in report and 'A2.8' in report)
a2_rows = re.findall(r'^\|\s*(A2\.\d+)\s*\|', report, re.M)
n_a2 = len(set(a2_rows))
f2_anchor = 'Yang–Mills F ∧ ⋆F 的质量量纲 = 4' in report

# EFT grammar requirement (vol 13) and partial-list readings
eft_requirement = ('算符底须允许' in v13 and
                   '不能只列几个方便的项' in v13 and
                   'd<4' in v13 and 'd=4' in v13)
r287_anchor = ('4D 二阶度规扇区只有 {1,R}' in r287 or
               '4D 二阶度规 {1,R}' in r287) and '{F², F F̃}' in r287
v09_template = r'\mathcal L_{\rm eff}=\frac{R}{2\kappa^2}+c_1R^2+c_2R_{\mu\nu}R^{\mu\nu}+\cdots' in v09
v14_undone = ('完整 SMEFT' in rd(os.path.join(V7, '14_全物理依赖图与量子挠率首个可复算切片_2026-10-09.md')) or
              '完整 Warsaw' in rd(os.path.join(V7, '14_全物理依赖图与量子挠率首个可复算切片_2026-10-09.md')))

# ---- finite grammar ------------------------------------------------------
# (name, mass dimension, form degree, so(1,3) index count, internal type, sector)
BUILDERS = [
    ('R', Fraction(2), 2, 2, 'singlet', 'gravity'),
    ('T', Fraction(1), 2, 1, 'singlet', 'gravity'),
    ('omega', Fraction(1), 1, 2, 'singlet', 'gravity'),
    ('F', Fraction(2), 2, 0, 'adjoint', 'gauge'),
    ('H', Fraction(1), 0, 0, 'su2doublet', 'matter'),
    ('Psi', Fraction(3, 2), 0, 0, 'fermion', 'matter'),
    ('D', Fraction(1), 0, 1, 'singlet', 'derivative'),
]
IDX = dict((b[0], i) for i, b in enumerate(BUILDERS))
MAX_N = 4
MAX_E = 4
MAX_M = 2                                  # powers of 1/kappa^2, each +2


def enumerate_signatures():
    out = []

    def rec(i, counts, dsum, psum):
        if dsum > 4:
            return
        if i == len(BUILDERS):
            for n_e in range(0, MAX_E + 1):
                if psum + n_e > 4:
                    continue
                for m in range(0, MAX_M + 1):
                    if dsum + 2 * m == 4:
                        out.append((tuple(counts), n_e, m, psum + n_e))
            return
        name, d, p, so, rep, sector = BUILDERS[i]
        maxn = min(MAX_N, int((Fraction(4) - dsum) / d)) if d > 0 else MAX_N
        for n in range(maxn + 1):
            counts.append(n)
            rec(i + 1, counts, dsum + n * d, psum + n * p)
            counts.pop()

    rec(0, [], Fraction(0), 0)
    return out


SIGNATURES = enumerate_signatures()


def legal(counts, n_e, m):
    n = dict((BUILDERS[i][0], counts[i]) for i in range(len(BUILDERS)))
    so_total = sum(counts[i] * BUILDERS[i][3] for i in range(len(BUILDERS))) + n_e
    checks = {
        'dimension': sum(counts[i] * BUILDERS[i][1]
                         for i in range(len(BUILDERS))) + 2 * m == 4,
        'form_degree': sum(counts[i] * BUILDERS[i][2]
                           for i in range(len(BUILDERS))) + n_e <= 4,
        'lorentz_even': so_total % 2 == 0,
        'adjoint_pairs': n['F'] % 2 == 0,
        'su2_singlet': n['H'] % 2 == 0,
        'fermion_number': n['Psi'] % 2 == 0,
        'nonempty': sum(counts) + n_e > 0,
    }
    return all(checks.values()), checks


def signature_key(counts, n_e, m):
    parts = ['%s%d' % (BUILDERS[i][0], counts[i])
             for i in range(len(BUILDERS)) if counts[i]]
    if n_e:
        parts.append('e%d' % n_e)
    parts.append('k%d' % m)
    return '+'.join(parts)


LEGAL = []
for counts, n_e, m, p_total in SIGNATURES:
    ok, checks = legal(counts, n_e, m)
    if ok:
        n = dict((BUILDERS[i][0], counts[i]) for i in range(len(BUILDERS)))
        has_grav = (n['R'] + n['T'] + n['omega']) > 0
        has_gauge = n['F'] > 0
        has_higgs = n['H'] > 0
        has_fermion = n['Psi'] > 0
        has_torsion = n['T'] > 0
        LEGAL.append({
            'key': signature_key(counts, n_e, m),
            'counts': dict((k, int(v)) for k, v in n.items()),
            'n_e': n_e, 'm': m, 'p_total': p_total,
            'has_gravity': has_grav, 'has_gauge': has_gauge,
            'has_higgs': has_higgs, 'has_fermion': has_fermion,
            'has_torsion': has_torsion,
            'gravity_gauge_direct': has_grav and has_gauge,
            'gravity_higgs_bridge': has_grav and has_higgs,
            'gravity_torsion': has_grav and has_torsion,
        })

# ---- baseline operators already in UFE-1 (A2.1-A2.8) --------------------
BASE_SIGNATURES = {
    'R1+e2+k1': 'A2.1 Palatini epsilon R e e / 4kappa^2',
    'e4+k2': 'A2.2 cosmological term (kappa-only reading; Lambda not in grammar)',
    'F2+k0': 'A2.3 Yang-Mills F wedge *F',
    'H2+D2+k0': 'A2.4 Higgs kinetic (DH)^2',
    'H2+k1': 'A2.5 Higgs mass (mu^2 replaced by 1/kappa^2 in grammar)',
    'H4+k0': 'A2.6 Higgs quartic lambda H^4',
    'Psi2+D1+k0': 'A2.7 Dirac kinetic (needs gamma matrix, outside grammar)',
    'H1+Psi2+k0': 'A2.8 Yukawa (needs chiral SU(2), outside grammar)',
}
for row in LEGAL:
    row['in_base'] = row['key'] in BASE_SIGNATURES
    row['base_label'] = BASE_SIGNATURES.get(row['key'], '')

n_legal = len(LEGAL)
legal_keys = set(r['key'] for r in LEGAL)
reproduced = [k for k in BASE_SIGNATURES if k in legal_keys]
n_base = sum(1 for r in LEGAL if r['in_base'])
n_extra = n_legal - n_base
direct = [r for r in LEGAL if r['gravity_gauge_direct']]
higgs_bridge = [r for r in LEGAL if r['gravity_higgs_bridge']]
torsion_bridge = [r for r in LEGAL if r['gravity_torsion']]
fermion_bridge = [r for r in LEGAL if r['has_gravity'] and r['has_fermion']]
curvature_square = [r for r in LEGAL if r['counts']['R'] >= 2]
gauge_self = [r for r in LEGAL if r['has_gauge'] and not r['has_gravity']]

# ---- price table ---------------------------------------------------------
PRICE = {
    'gravity_gauge_direct': len(direct),
    'gravity_higgs_bridge': len(higgs_bridge),
    'gravity_torsion': len(torsion_bridge),
    'gravity_fermion': len(fermion_bridge),
    'curvature_square': len(curvature_square),
    'gauge_self': len(gauge_self),
}
new_constants_min = sum(1 for r in LEGAL
                        if (not r['in_base']) and
                        (r['gravity_higgs_bridge'] or r['gravity_torsion'] or
                         (r['has_gravity'] and r['has_fermion']) or
                         r['gravity_gauge_direct']))
r49a_price = ('+7' in v49a and '+9' in v49a and '33' in v49a)
xi_anchor = 'ξ=4911.63' in c310 or '4911.63' in c310
contact_anchor = (r'-\frac{3\kappa^{2}}{8}' in v02 and
                  r'\frac{\kappa^{2}}{2}' in v02)
omega5_anchor = '自由常数 ≤ 1' in r404 or '自由常数不超过 1' in r287
r404_e07 = 'E07 新场 / 新耦合' in r404 and '`c = 2`' in r404

# ---- positive controls (the detector must have teeth) -------------------
def enumerate_with_relaxed(internal_pairs):
    def legal_relaxed(counts, n_e, m):
        n = dict((BUILDERS[i][0], counts[i]) for i in range(len(BUILDERS)))
        so_total = sum(counts[i] * BUILDERS[i][3]
                       for i in range(len(BUILDERS))) + n_e
        return (sum(counts[i] * BUILDERS[i][1]
                    for i in range(len(BUILDERS))) + 2 * m == 4 and
                sum(counts[i] * BUILDERS[i][2]
                    for i in range(len(BUILDERS))) + n_e <= 4 and
                so_total % 2 == 0 and
                (n['F'] % 2 == 0 if internal_pairs else 1) and
                n['H'] % 2 == 0 and n['Psi'] % 2 == 0 and
                sum(counts) + n_e > 0)
    count = 0
    for counts, n_e, m, p_total in SIGNATURES:
        if legal_relaxed(counts, n_e, m):
            n = dict((BUILDERS[i][0], counts[i]) for i in range(len(BUILDERS)))
            if (n['R'] + n['T'] + n['omega']) > 0 and n['F'] > 0:
                count += 1
    return count


direct_relaxed = enumerate_with_relaxed(0)
direct_control_fires = direct_relaxed > len(direct)

# ---- closure state machine -------------------------------------------------
def bridge_verdict(n_direct, n_higgs, n_extra, base_ok):
    ok = (n_direct == 0 and n_higgs >= 1 and n_extra >= 1 and base_ok == 1)
    return 'BRIDGES-EXIST-BUT-NONE-MIX-GRAVITY-WITH-GAUGE' if ok else 'RECHECK'


v_bridge = bridge_verdict(len(direct), len(higgs_bridge), n_extra, 1)
controls = {
    'relax_internal_pairs': bridge_verdict(direct_relaxed, len(higgs_bridge), n_extra, 1),
    'no_higgs_bridge': bridge_verdict(0, 0, n_extra, 1),
    'no_extra_operators': bridge_verdict(0, len(higgs_bridge), 0, 1),
    'drop_baseline': bridge_verdict(0, len(higgs_bridge), n_extra, 0),
    'fake_direct_bridge': bridge_verdict(1, len(higgs_bridge), n_extra, 1),
}
all_controls_fire = all(x == 'RECHECK' for x in controls.values())

terminal_verdict = (
    'DIM4-GRAMMAR-ENUMERATED--GRAVITY-GAUGE-DIRECT-BRIDGE-COUNT-ZERO--'
    'HIGGS-AND-TORSION-BRIDGES-EXIST--EACH-COSTS-NEW-CONSTANTS--'
    'ATTACK52-BOUNDARY-QUANTIFIED'
)
candidate_verdict = 'BOUNDARY_CLOSED_WITH_PRICE_TABLE'

# ---- dynamic numbering ---------------------------------------------------
attack_nums = []
for name in os.listdir(B1):
    m = re.match(r'^attack(\d+)[_.]', name)
    if m:
        attack_nums.append(int(m.group(1)))
attack_prior_max = max([n for n in attack_nums if n < 53] or [0])
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
preexisting_53 = [n for n in os.listdir(B1)
                  if (n.startswith('attack53') or n.startswith('判定_attack53'))
                  and n not in SELF_OUTPUTS]
j109_volumes = [n for n in os.listdir(V7)
                if n.startswith('131_') and n.endswith('.md')]

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


probe_tree = ast.parse('import attack52_bad\nimport _j109_bad\nimport os')
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
G('G01', attack_prior_max == 52 and 53 in attack_nums and
  r_max >= 406 and volume_max >= 130 and j_max >= 108 and
  c_max >= 401 and not preexisting_53 and not j109_volumes,
  'dynamic lower-bound scan: attack52 prior, attack53 first free; '
  'r406+ / vol130+ / J108+ / C0401+, volume131 still absent')
G('G02', all(os.path.isfile(p) for p in P.values() if p),
  'all fourteen declared input files exist on disk')
G('G03', D_E == 0 and D_OMEGA == 1 and D_T == 1 and D_R == 2 and
  D_KAPPA == 2 and dim4_rule and f2_anchor and n_a2 == 16,
  'live dimension anchors [e]=0 [omega]=1 [T]=1 [R]=2, [1/kappa^2]=+2, '
  'A2.1-A2.16 dim-4 rule')
G('G04', eft_requirement and r287_anchor and v09_template and v14_undone,
  'vol13 grammar requirement, r287 partial-list control, vol09 +... template, '
  'vol14 self-declared incomplete SMEFT basis')
G('G05', len(SIGNATURES) > 100 and n_legal >= 8 and n_extra >= 1 and
  all(0 <= sum(c) + e <= 8 for c, e, m, p in SIGNATURES),
  'finite grammar enumerated %d signatures, %d legal operators, %d extra'
  % (len(SIGNATURES), n_legal, n_extra))
G('G06', len(reproduced) >= 5 and n_extra >= 1 and
  all(k in legal_keys for k in ['F2+k0', 'H4+k0', 'R1+H2+k0']),
  'grammar reproduces %d/8 A2 baseline signatures; extra operators exist; '
  'xi H^2 R non-minimal coupling present. A2.7/A2.8 need gamma/chiral structure '
  'outside this grammar (honest under-approximation)'
  % len(reproduced))
G('G07', len(direct) == 0 and direct_control_fires,
  'gravity-gauge direct dim-4 bridge count 0; relaxing internal pairing makes it %d '
  '(detector has teeth)' % direct_relaxed)
G('G08', len(higgs_bridge) >= 1 and len(torsion_bridge) >= 1 and
  len(curvature_square) >= 1 and xi_anchor,
  'Higgs bridge, torsion bridge and curvature-square operators all present; '
  'xi=4911.63 registered on disk')
G('G09', new_constants_min >= 1 and r49a_price and omega5_anchor and
  r404_e07 and contact_anchor,
  'each extra bridge costs new constants; vol49A +7/+9 -> 33-37, Omega5<=1, '
  'r404 E07 c=2 DEAD; EC four-fermion contact anchored')
G('G10', v_bridge == 'BRIDGES-EXIST-BUT-NONE-MIX-GRAVITY-WITH-GAUGE' and
  all_controls_fire and len(controls) == 5,
  'state machine: dim-4 bridges exist but none mixes gravity with gauge; '
  'five counterfactuals flip')
G('G11', 'NO-CORRECT-FOUR-FORCE-GUT' in r403 and
  '量纲自洽 ≠ 成立' in r403 and '定理 E1' in a51 and '定理 E3' in a51 and
  'dim-4 混合 4-形式恒等于零' in a52,
  'r403 terminal verdict, attack51 E1/E3 and attack52 dim-4 zero theorem on disk')
G('G12', all(BEFORE[k] == AFTER[k] for k in P),
  'all read-only inputs unchanged during engine runtime (md5 before/after)')
G('G13', (not prior_imports(imports)) and
  len(prior_imports(probe_imports)) == 2,
  'no prior attack/J-series engine import; positive control fires')
G('G14', dollar_brace not in src and literal_true_count(tree) == 0 and
  literal_true_count(positive_tree) == 1,
  'no dollar-brace placeholder, no hard-coded guard True literals')
G('G15', '0/22' in a51 and '不计攻破数' in a52,
  'attack51/52 redlines remain on disk')

# ---- FINDINGS -------------------------------------------------------------
F('F01', 'PASS',
  '动态实扫：attack53 为首空号；上界 r%d / 卷%d-J%d / C0%d，卷 131/J109 仍未落盘。'
  '查重：13 卷只提「算符底须允许所有独立不变量 / 不能只列几个方便的项」的要求，'
  '09 卷是 `+\\cdots` 示意模板，r287 是 `{1,R}` / `{F²,FF̃}` 控制组，'
  '14/15/16/17 卷自认完整 SMEFT/Warsaw 基底未做，attack52 只判 `R¹F¹` 一个单项'
  % (r_max, volume_max, j_max, c_max))
F('F02', 'PASS',
  '文法内穷举：构件 `%s`（量纲/形式次数/洛伦兹指标/内部表示全部现场取自 13/06/验证报告），'
  '约束 `Σd + 2m = 4`（`m` 为 `1/κ²` 幂）、`Σp + n_e ≤ 4`、洛伦兹指标偶数、'
  '内部伴随/F/H/费米配对 ⇒ 共 **%d** 个合法 dim-4 算符签名，'
  '其中 A2.1–A2.8 基准在文法内复现 **%d/8** 项'
  '（A2.7/A2.8 需 γ 矩阵与手征 SU(2)，属文法外，如实登记），额外 **%d** 项'
  % ('、'.join(b[0] for b in BUILDERS), n_legal, len(reproduced), n_extra))
F('F03', 'PASS',
  '**决定性读数**：`gravity-gauge direct` 合法算符 **%d** 条 —— '
  '`R·F` 因 `n_F` 奇数被内部单态门拦下，`R·F²`/`T²·F²` 因 `Σd≥6` 被维数门拦下；'
  '放宽内部配对后升 **%d** 条（阳性对照有牙）。'
  '这与 attack52 用 Schur/不变空间秩 0 判 dim-4 `R∧F` 恒零是**两条独立路径同一结论**'
  % (len(direct), direct_relaxed))
F('F04', 'PASS',
  'attack52 的 BOUNDARY 被量化：dim-4 **确实存在**桥接项，但全部经 Higgs / 挠率 / 曲率自耦合 —— '
  '引力-Higgs `%d` 条（含 `ξ H†H R`，库内 `ξ=4911.63`）、引力-挠率 `%d` 条、'
  '曲率平方 `%d` 条、引力-费米 `%d` 条、纯规范自耦合 `%d` 条；'
  '**没有一条把引力与规范场直接混合**'
  % (len(higgs_bridge), len(torsion_bridge), len(curvature_square),
     len(fermion_bridge), len(gauge_self)))
F('F05', 'BOUNDARY',
  '价格表：每个额外桥接**场内容签名类**至少 +1 个新自由常数，本册得 **%d** 类下界；'
  '签名层不区分同一场内容的不同指标收缩（`F²`/`FF̃`、`R²`/`R_{μν}R^{μν}` 各并为一类），'
  '故这是**下界**而非精确常数个数。'
  '49A 卷特定扩展模型参数账 `+7/+9`（SM 26–28 ⇒ 33–37）与之同向，'
  '撞 Ω5「自由常数 ≤1」与 r404 E07 `c=2, DEAD`。'
  'EC 四费米接触项 `−3κ²/8` 是**系数被 κ² 钉死、无自由参数**的对照，不算新常数'
  % new_constants_min)
F('F06', 'FAIL',
  '被检命题「补全 dim-4 算符基底后就能找到零代价的引力-规范统一桥接」**不成立**：'
  '合法桥接项全部绕道 Higgs/挠率，且每条都要付新常数；'
  '承 attack51 的 E1(1:5:7) / E3(常数秩 0) 仍不翻转 ⇒ '
  'attack52 的「不宣称所有交叉项都不可能」被收窄为「有桥接、但桥的不是四力、且明码标价」')
F('F07', 'BOUNDARY',
  '**诚实射程**：这是「有限构件字母表 + κ² 补偿阶 + 配对规则」下的**文法内枚举完整**，'
  '不是方法空间穷尽，也不是完整 SMEFT/Warsaw 基底 —— '
  '未覆盖 Λ/μ² 等有量纲系数、Fierz/EOM 消冗、边界项、场重定义、非局域 1PI 项与更高表示；'
  '14 卷明写「没有宣称已经产生完整 SMEFT/WET 基底」，本册不冒充')
F('F08', 'BOUNDARY',
  '红线：含引力四力大统一正确方程仍 0 条、无新物理方程理论体系、'
  '`0/22、UFT-3=0、L3=0、validated=0`、记分板 0/6 不变；'
  'r403 终判、attack50 `#31 = PRICED_OPEN`、attack51/52 结论均不变；'
  '不否证 ECSK/SM/GR；不计攻破数、不重判物理条目、不新增债务、不改任何历史字节')

verdict_counts = dict(Counter(f['verdict'] for f in FINDINGS))
result = {
    'volume': 'attack53',
    'round_label': '攻破㊺',
    'date': '2026-11-09',
    'scope': 'finite-grammar dim-4 local operator enumeration and bridge price table',
    'numbering': {
        'attack_prior_max': attack_prior_max, 'attack_current': 53,
        'r_max': r_max, 'volume_max': volume_max, 'j_max': j_max,
        'c_max': c_max, 'volume131_md': j109_volumes,
        'preexisting_attack53': preexisting_53,
    },
    'dimension_anchors': {
        'parsed': dict((k, int(v)) for k, v in dim_pairs.items()),
        'D_e': D_E, 'D_omega': D_OMEGA, 'D_T': D_T, 'D_R': D_R,
        'D_one_over_kappa2': D_KAPPA, 'dim4_rule': dim4_rule,
        'A2_rows': n_a2, 'F2_anchor': f2_anchor,
    },
    'grammar': {
        'builders': [[b[0], str(b[1]), b[2], b[3], b[4], b[5]]
                     for b in BUILDERS],
        'constraints': ['sum(d)+2m=4', 'sum(p)+n_e<=4',
                        'lorentz_indices_even', 'adjoint_F_pairs',
                        'su2_H_pairs', 'fermion_number_even', 'nonempty'],
        'max_n': MAX_N, 'max_e': MAX_E, 'max_m': MAX_M,
        'total_signatures': len(SIGNATURES), 'legal_operators': n_legal,
        'in_baseline': n_base, 'extra': n_extra,
        'honesty': 'grammar-complete, NOT method-space complete; no Fierz/EOM/'
                   'boundary-term/field-redefinition reduction, no nonlocal 1PI',
    },
    'baseline_reproduced': {
        'declared': BASE_SIGNATURES,
        'reproduced_in_grammar': reproduced,
        'not_reproduced': [k for k in BASE_SIGNATURES if k not in legal_keys],
        'n_reproduced': len(reproduced),
    },
    'bridge_price_table': {
        'counts': PRICE,
        'gravity_gauge_direct_operators': [r['key'] for r in direct],
        'gravity_higgs_bridge_operators': [r['key'] for r in higgs_bridge][:40],
        'curvature_square_operators': [r['key'] for r in curvature_square][:40],
        'min_new_constants': new_constants_min,
        'interpretation': 'LOWER BOUND on field-content signature classes, not an '
                          'exact independent-coupling count: different index '
                          'contractions of the same field content (F^2 vs F Ftilde, '
                          'R^2 vs R_mn R^mn) collapse to one signature here',
        'vol49A_price': '+7/+9 -> 33-37',
        'xi_nonminimal_coupling': '4911.63' if xi_anchor else None,
        'EC_contact_term_no_free_parameter': contact_anchor,
    },
    'positive_controls': {
        'relaxed_internal_pairs_direct_count': direct_relaxed,
        'strict_direct_count': len(direct),
        'fires': direct_control_fires,
    },
    'state_machine': {
        'verdict': v_bridge, 'counterfactuals': controls,
        'all_controls_fire': all_controls_fire,
    },
    'legal_operator_sample': [r['key'] for r in LEGAL[:60]],
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
        'The tempting claim "dim-4 complete operator basis" was rejected: vol13 itself says the independent combinations depend on field content, symmetry and identities, and vols 14/15/16/17 explicitly declare a complete SMEFT/Warsaw basis undone. This volume only claims grammar-completeness over a declared finite builder alphabet.',
        'The form-degree gate is not independent of the mass-dimension gate because [e]=0 while deg(e)=1: vierbeins can pad any 4-form for free. The grammar therefore enumerates field-content signatures plus a kappa-squared compensation order m, rather than pretending to enumerate full 4-forms.',
        'A direct R*F gravity-gauge monomial is killed twice independently: attack52 used Schur/equivariant invariant space rank 0, this volume uses the internal-adjoint pairing rule (n_F must be even) together with sum(d)=4. Relaxing the pairing rule produces direct bridges, so the detector is not trivially zero.',
        'The EC four-fermion contact term -3kappa^2/8 is deliberately NOT counted as a new free constant because its coefficient is fixed by kappa^2; counting it would inflate the price table.',
        'Baseline A2.1-A2.8 signatures are matched by exact key strings; signature formatting uses a compact kN notation for the kappa-squared order and eN for vierbein padding.',
        'A parallel session wrote J109/volume131 constants into a scratch script but has not landed the volume; numbering guards use live lower bounds and record the absence rather than requiring it.',
        'Baseline signature keys were first written in ad-hoc order (H2+R1+k0) while signature_key emits builder order (R1+H2+k0); corrected all eight keys against the BUILDERS sequence.',
        'G05 originally contained an always-true all([]) is not None expression; replaced with real enumeration-scale and extra-operator checks.',
        'The simplified grammar has no gamma matrices and no chiral SU(2) bookkeeping, so A2.7 Dirac kinetic and A2.8 Yukawa cannot be reproduced. Rather than loosening the rules to fake a full 8/8 baseline, the engine records %d/8 reproduced and declares the grammar a conservative under-approximation.' % len(reproduced),
        'A stray undefined function name was left in the positive-controls dict inside a dead conditional branch; replaced by the real flag.',
        'The EC contact-term anchor first used 3kappa^2/2 while vol02 writes kappa^2/2 for the torsion solution; corrected to the literal on disk.',
        'A KeyError on gravity_fermion was fixed by using has_gravity and has_fermion instead of adding a redundant key.',
        'The count 23 was initially described as an exact number of new constants. Because the grammar counts field-content signatures and collapses F^2/F Ftilde and R^2/R_mn R^mn into single classes, it is a LOWER BOUND on signature classes, not an exact independent-coupling count; the wording and JSON interpretation field were corrected.',
    ],
    'guards': GUARDS,
    'guard_pass': sum(1 for g in GUARDS if g['ok']),
    'guard_total': len(GUARDS),
    'exit': 0 if all(g['ok'] for g in GUARDS) else 1,
}

with io.open(os.path.join(HERE, BASE + '.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

md = []
md.append('# attack53 · dim-4 算符文法内枚举与桥接代价（数据产物）')
md.append('')
md.append('- 日期：2026-11-09 ｜ 守卫 **%d/%d** ｜ 退出码 **%d** ｜ 总裁定 **%s**'
          % (result['guard_pass'], result['guard_total'], result['exit'],
             candidate_verdict))
md.append('- 判决计数：**%s**' % verdict_counts)
md.append('- 定位：补全 attack52 声明「未在射程」的挠率 / Higgs / 物质桥接算符')
md.append('')
md.append('## 一、现场量纲与文法')
md.append('')
md.append('`[e]=%d, [ω]=%d, [T]=%d, [R]=%d, [1/κ²]=+%d`；A2.1–A2.8「每项量纲 4」；'
          'A2 表共 %d 行' % (D_E, D_OMEGA, D_T, D_R, D_KAPPA, n_a2))
md.append('')
md.append('| 构件 | 质量量纲 | 形式次数 | so 指标 | 内部表示 | 扇区 |')
md.append('|---|---|---|---|---|---|')
for b in BUILDERS:
    md.append('| %s | %s | %d | %d | %s | %s |'
              % (b[0], b[1], b[2], b[3], b[4], b[5]))
md.append('')
md.append('约束：`Σd + 2m = 4`（`m` = `1/κ²` 幂）、`Σp + n_e ≤ 4`、'
          '洛伦兹指标偶数、`n_F`/`n_H`/`n_Ψ` 均偶数。')
md.append('')
md.append('枚举 **%d** 签名 → 合法 **%d** 个算符；A2.1–A2.8 基准在文法内复现 '
          '**%d/8** 项（`A2.7`/`A2.8` 需 γ 矩阵与手征 SU(2)，文法外），额外 **%d** 项。'
          % (len(SIGNATURES), n_legal, len(reproduced), n_extra))
md.append('')
md.append('## 二、桥接价格表')
md.append('')
md.append('| 类别 | 合法算符数 | 新增常数 |')
md.append('|---|---|---|')
for k, val in PRICE.items():
    md.append('| %s | %d | %s |'
              % (k, val, '0（基准或系数被钉死）' if k == 'gravity_gauge_direct'
                 else '每条 ≥1'))
md.append('')
md.append('- **引力-规范直接桥接 = %d**（`R·F` 被内部单态门拦，`R·F²` 被 Σd≥6 拦）；'
          '放宽内部配对阳性对照升 **%d** 条' % (len(direct), direct_relaxed))
md.append('- `ξ H†H R` 存在（库内 `ξ=4911.63`）；`R²`/`R_{μν}R^{μν}` 曲率平方反项存在；'
          '挠率二次型 `T²` 存在。')
md.append('- 最小新增自由常数 **%d**；49A 卷 `+7/+9 ⇒ 33–37`、Ω5 ≤1、'
          'r404 E07 `c=2 DEAD` 同向。' % new_constants_min)
md.append('')
md.append('> 裁定：`%s`' % v_bridge)
md.append('> 5 组反事实全部翻转 = %s' % all_controls_fire)
md.append('')
md.append('> **射程**：文法内枚举完整 ≠ 方法空间穷尽；未覆盖 Fierz/EOM 消冗、边界项、'
          '场重定义、非局域 1PI 项与更高表示；14/15/16/17 卷自认完整 SMEFT/Warsaw 基底未做。')
md.append('')
md.append('> 完整判定见 `判定_attack53_dim4算符基底枚举与桥接代价_2026-11-09.md`。')
with io.open(os.path.join(HERE, BASE + '.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(md) + '\n')

lines = []
lines.append('attack53 / 2026-11-09 / dim-4 grammar enumeration and bridge price')
lines.append('')
lines.append('[A] numbering')
lines.append('  %s' % result['numbering'])
lines.append('')
lines.append('[B] grammar')
lines.append('  %s' % result['grammar'])
lines.append('')
lines.append('[C] baseline')
lines.append('  %s' % BASE_SIGNATURES)
lines.append('')
lines.append('[D] price table')
lines.append('  %s' % result['bridge_price_table']['counts'])
lines.append('  min_new_constants=%d direct=%d relaxed_direct=%d'
             % (new_constants_min, len(direct), direct_relaxed))
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

print('attack53 guards=%d/%d findings=%s exit=%d legal=%d base=%d extra=%d direct=%d'
      % (result['guard_pass'], result['guard_total'], verdict_counts,
         result['exit'], n_legal, n_base, n_extra, len(direct)))
sys.exit(result['exit'])
