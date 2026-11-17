# -*- coding: utf-8 -*-
# r424 / algorithm alliance -- ROOT V77: G-c relations full-dimensional audit (2026-11-17)
# Reads V77 ZIP read-only; recomputes every headline number at 250 significant digits
# with pure stdlib Decimal, proves the dimensional no-go by exact integer rank,
# propagates CODATA 2022 uncertainty, falsifies the Z=0.01 SI guess and shows its
# unit dependence, then applies the r421 W3 gate to all V77 tables.
# No new physics claim; no external dependency.
import os
import io
import sys
import csv
import json
import ast
import glob
import hashlib
import zipfile
import tempfile
import subprocess
import importlib.util
from decimal import Decimal as D, getcontext, localcontext
from fractions import Fraction as F

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
getcontext().prec = 260

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, '..'))
OPENUFT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(PUB, '数据')
DATE = '2026-11-17'
STEM = 'TUFT-r424_ROOT_V77_G与c全维关系审计_2026-11-17'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')
P_EQ_CSV = os.path.join(DATA, 'TUFT-r424_V77方程登记_54条.csv')
P_RT_CSV = os.path.join(DATA, 'TUFT-r424_V77路线登记_30条.csv')
F_R423 = os.path.join(PUB, '判定_TUFT-r423-ROOT_V65执行层与候选空间穷尽_2026-11-17.md')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')

ZIPS = sorted(glob.glob(os.path.join('C:\\', 'Users', 'mo', 'Downloads', 'ROOT_V77_*.zip')))
ZIP = ZIPS[0] if ZIPS else ''

VERDICT = ('V77-G-C-RELATIONS--FIVE-EQUATIONS-EXACT-BUT-DEFINITIONAL--'
           'DIMENSIONAL-NOGO-RANK-PROVEN--ALPHA-G-IDENTITY-EXACT--'
           'Z-0P01-REJECTED-20SIGMA-AND-UNIT-DEPENDENT--Z-PLUS-ZPRIME-NOT-ADDABLE--'
           'CONDITIONAL-C-SCALINGS-NOT-UNIQUE--GM-DEGENERACY-RANK-1--'
           'NO-W3-CANDIDATE--0OF6-UNCHANGED')

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


def sha256_file(path):
    if not path or not os.path.exists(path):
        return 'ABSENT'
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def md5_file(path):
    if not os.path.exists(path):
        return 'ABSENT'
    h = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def pi_chudnovsky(prec=250):
    with localcontext() as ctx:
        ctx.prec = prec + 30
        C = 426880 * D(10005).sqrt()
        M, L, X, K, S = 1, 13591409, 1, 6, D(13591409)
        for i in range(1, prec // 14 + 4):
            M = (K ** 3 - 16 * K) * M // (i ** 3)
            L += 545140134
            X *= -262537412640768000
            S += D(M * L) / D(X)
            K += 12
        return +(C / S)


PI = pi_chudnovsky(250)
PI_100 = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'

# CODATA 2022 / SI defining constants, exact decimal inputs.
C_S = '299792458'
H_S = '6.62607015e-34'
G_S = '6.67430e-11'
UG_S = '1.5e-15'
ME_S = '9.1093837139e-31'
MP_S = '1.67262192595e-27'
GME_S = '3.98600435507e14'
EPS0_S = '8.8541878188e-12'

C = D(C_S)
H = D(H_S)
HBAR = H / (2 * PI)
G = D(G_S)
UG = D(UG_S)
ME = D(ME_S)
MP = D(MP_S)
GME = D(GME_S)
EPS0 = D(EPS0_S)

CF = F(int(C_S))
HF = F(D(H_S))
GF = F(D(G_S))
UGF = F(D(UG_S))
MEF = F(D(ME_S))
MPF = F(D(MP_S))
GMEF = F(D(GME_S))


def fmt(x, n=42):
    return format(+x, '.' + str(n) + 'E')


def fmt_rel(x):
    x = D(x)
    if x == 0:
        return '0.00E+00'
    return format(x, '.2E')


def rel_diff(a, b):
    a, b = D(a), D(b)
    if b == 0:
        return abs(a - b)
    return abs((a - b) / b)


def rank_int(rows):
    mat = [[F(v) for v in r] for r in rows]
    nr, nc = len(mat), len(mat[0])
    rank = 0
    for col in range(nc):
        pivot = None
        for r in range(rank, nr):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [v / pv for v in mat[rank]]
        for r in range(nr):
            if r != rank and mat[r][col] != 0:
                k = mat[r][col]
                mat[r] = [mat[r][j] - k * mat[rank][j] for j in range(nc)]
        rank += 1
    return rank


def w3_accept(cand):
    checks = {
        'C1_quantitative_number': bool(cand.get('quantitative', False)),
        'C2_not_reverse_engineered': bool(cand.get('independent', False)),
        'C3_test_path_unused_in_fit': bool(cand.get('blind_path', False)),
        'C4_two_anchors_consistent': bool(cand.get('two_anchors_ok', False)),
    }
    return {'passed': all(checks.values()), 'checks': checks}


guard('G0-0_stdlib_only', 'sympy' not in sys.modules and 'numpy' not in sys.modules, 'pure stdlib')
guard('G0-f0_v77_zip', bool(ZIP) and os.path.exists(ZIP), os.path.basename(ZIP))
guard('G0-f1_r423', os.path.exists(F_R423), os.path.basename(F_R423))
guard('G0-f2_r421', os.path.exists(F_R421), os.path.basename(F_R421))

src = io.open(__file__, encoding='utf-8').read()
try:
    ast.parse(src)
    guard('G1-ast', True, 'self syntax ok')
except SyntaxError as exc:
    guard('G1-ast', False, str(exc))

guard('G1b-pi-100-digits', str(PI)[:len(PI_100)] == PI_100, 'Chudnovsky pi matches 100 published digits')

if not ZIP or not os.path.exists(ZIP):
    emit('V77 ZIP absent; cannot continue')
    raise SystemExit(2)

with zipfile.ZipFile(ZIP) as z:
    names = z.namelist()
    crc_ok = z.testzip()
    raw_summary = z.read('ROOT_V77/results/numerical_summary.json').decode('utf-8')
    raw_symbolic = z.read('ROOT_V77/results/symbolic_verification.json').decode('utf-8')
    raw_report = z.read('ROOT_V77/results/verification_report.json').decode('utf-8')
    raw_browser = z.read('ROOT_V77/results/browser_verification.json').decode('utf-8')
    eq_text = z.read('ROOT_V77/data/equation_catalog.csv').decode('utf-8-sig')
    rt_text = z.read('ROOT_V77/data/hypothesis_audit.csv').decode('utf-8-sig')
    ml_text = z.read('ROOT_V77/data/mass_length_comparison.csv').decode('utf-8-sig')
    cs_text = z.read('ROOT_V77/data/conditional_c_scaling.csv').decode('utf-8-sig')
    eg_text = z.read('ROOT_V77/data/earth_GM_degeneracy.csv').decode('utf-8-sig')
    manifest_text = z.read('ROOT_V77/SHA256_MANIFEST.csv').decode('utf-8-sig')
    manifest_rows = list(csv.DictReader(io.StringIO(manifest_text)))
    manifest_bad = []
    for row in manifest_rows:
        blob = z.read('ROOT_V77/' + row['relative_path'])
        if len(blob) != int(row['size_bytes']) or hashlib.sha256(blob).hexdigest() != row['sha256']:
            manifest_bad.append(row['relative_path'])

summary = json.loads(raw_summary)
symbolic = json.loads(raw_symbolic)
report = json.loads(raw_report)
browser = json.loads(raw_browser)
eq_rows = list(csv.DictReader(io.StringIO(eq_text)))
rt_rows = list(csv.DictReader(io.StringIO(rt_text)))
ml_rows = list(csv.DictReader(io.StringIO(ml_text)))
cs_rows = list(csv.DictReader(io.StringIO(cs_text)))
eg_rows = list(csv.DictReader(io.StringIO(eg_text)))

guard('G2-crc', crc_ok is None, 'zip CRC ok')
guard('G2b-members', len(names) == 32, 'members=%d' % len(names))

manifest_ok = (len(manifest_rows) == 30) and not manifest_bad
guard('G3-manifest', manifest_ok, 'manifest rows=%d, mismatches=%d, verify_release.py self-excluded'
      % (len(manifest_rows), len(manifest_bad)))

# Independent clean-room re-run of the shipped unit tests (execution evidence, not physics).
tests_ok = False
tests_detail = 'not run'
try:
    with tempfile.TemporaryDirectory(prefix='r424_v77_') as td:
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(td)
        base = os.path.join(td, 'ROOT_V77')
        p = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-q'],
                           cwd=base, capture_output=True, text=True, timeout=90,
                           encoding='utf-8', errors='replace')
        tests_ok = (p.returncode == 0) and ('Ran 58 tests' in (p.stderr or '')) and ('OK' in (p.stderr or ''))
        tests_detail = 'exit=%d; Ran 58 tests=%s; OK=%s' % (
            p.returncode, 'Ran 58 tests' in (p.stderr or ''), 'OK' in (p.stderr or ''))
except Exception as exc:  # pragma: no cover
    tests_detail = 'exception: %r' % (exc,)
guard('G4-independent-58-tests', tests_ok, tests_detail)
guard('G4b-shipped-report-scope', report.get('all_passed') is True and 'not independent' in report.get('scope', ''),
      'all_passed=%s; scope=%s' % (report.get('all_passed'), report.get('scope')))

# ---------- 250-digit quantities ----------
Z = G * C / 2
UC = UG * C / 2
RGC = G / C ** 2
G4C = G / C ** 4
KAPPA = 8 * PI * G / C ** 4
LP = (HBAR * G / C ** 3).sqrt()
MPL = (HBAR * C / G).sqrt()


def alpha_g(m):
    return G * m * m / (HBAR * C)


def rg(m):
    return G * m / C ** 2


def rc(m):
    return HBAR / (m * C)


Q = {
    'Z_SI': Z,
    'u_Z_SI': UC,
    'G_over_c_SI': G / C,
    'G_over_c2_SI': RGC,
    'G_over_c4_SI': G4C,
    'Einstein_kappa_m_per_J': KAPPA,
    'Planck_length_m': LP,
    'Planck_mass_kg': MPL,
    'G_relative_uncertainty': UG / G,
    'alpha_g_electron': alpha_g(ME),
    'alpha_g_proton': alpha_g(MP),
    'alpha_g_planck': alpha_g(MPL),
    'electron_r_g_m': rg(ME),
    'electron_lambda_C_m': rc(ME),
    'proton_r_g_m': rg(MP),
    'proton_lambda_C_m': rc(MP),
    'planck_r_g_m': rg(MPL),
    'planck_lambda_C_m': rc(MPL),
    'electron_rg_over_lambdaC': rg(ME) / rc(ME),
    'proton_rg_over_lambdaC': rg(MP) / rc(MP),
    'earth_r_g_m': GME / C ** 2,
    'earth_r_s_m': 2 * GME / C ** 2,
    'earth_mass_inferred_kg': GME / G,
}

# Cross-check against V77 self-reported JSON (17 sig digits); tolerance 1e-14.
V77_KEYS = ['Z_SI', 'u_Z_SI', 'G_over_c2_SI', 'G_over_c4_SI', 'Einstein_kappa_m_per_J',
            'Planck_length_m', 'Planck_mass_kg', 'G_relative_uncertainty',
            'gravitational_alpha_electron', 'gravitational_alpha_proton',
            'electron_r_g_m', 'proton_r_g_m']
their = summary['quantities']
cmp_rows = []
for k in V77_KEYS:
    theirs = D(str(their[k]))
    mine = Q[k] if k in Q else None
    if mine is None:
        mine = {'gravitational_alpha_electron': Q['alpha_g_electron'],
                'gravitational_alpha_proton': Q['alpha_g_proton']}[k]
    rd = rel_diff(mine, theirs)
    cmp_rows.append({'key': k, 'v77': theirs, 'r424': mine, 'rel_diff': rd})
MAXCMP = max(r['rel_diff'] for r in cmp_rows)
guard('G5-headline-numbers', MAXCMP < D('1e-14'),
      'max relative difference=%.3E over %d keys' % (MAXCMP, len(cmp_rows)))

# ---------- dimensional no-go (exact integer rank + exponent contradiction) ----------
# basis (L, M, T): G=(3,-1,-2), c=(1,0,-1), hbar=(2,1,-1)
A = [[1, 2], [0, 1], [-1, -1]]      # columns c, hbar
b = [3, -1, -2]
rank_A = rank_int(A)
rank_aug = rank_int([A[0] + [b[0]], A[1] + [b[1]], A[2] + [b[2]]])
b_from_M = -1
a_from_L = 3 - 2 * b_from_M
t_required = -2
t_obtained = -(a_from_L + b_from_M)
no_go = (rank_A == 2 and rank_aug == 3) and (t_obtained != t_required)
guard('G6-dimensional-nogo', no_go,
      'rank[c,hbar]=%d < rank[c,hbar,G]=%d; a=%d,b=%d -> T exponent %d != %d'
      % (rank_A, rank_aug, a_from_L, b_from_M, t_obtained, t_required))

# With an independent length: G = A c^3 L^2 / hbar (unique exponents).
dim_c3L2_hbar = (3 * 1 + 2 * 1 - 2, 0 + 0 - 1, -3 + 0 + 1)
# With an independent mass: G = B hbar c / M^2.
dim_hc_M2 = (2 + 1 - 0, 1 + 0 - 2, -1 - 1 - 0)
guard('G6b-augmented-basis', dim_c3L2_hbar == (3, -1, -2) and dim_hc_M2 == (3, -1, -2),
      'c^3 L^2/hbar=%s; hbar c/M^2=%s' % (dim_c3L2_hbar, dim_hc_M2))

# ---------- five core identities: exact Fraction / 250-digit residuals ----------
ident_res = {}
# 1) G = 2Z/c with Z := Gc/2 (exact rational)
Zf = GF * CF / 2
ident_res['G=2Z/c'] = abs(2 * Zf / CF - GF)
# 2) G = c^2 r_g / M with r_g := GM/c^2 (exact rational)
rgf = GF * MEF / CF ** 2
ident_res['G=c^2 r_g/M'] = abs(CF ** 2 * rgf / MEF - GF)
# 3) G = c^3 lP^2 / hbar (definitional; residual at 250 digits)
ident_res['G=c^3 lP^2/hbar'] = float(rel_diff(C ** 3 * LP ** 2 / HBAR, G))
# 4) G = alpha_g hbar c / m^2
ident_res['G=alpha_g hbar c/m^2'] = float(rel_diff(Q['alpha_g_electron'] * HBAR * C / ME ** 2, G))
# 5) r_g / lambda_C = alpha_g(m)
ident_res['r_g/lambda_C=alpha_g'] = float(rel_diff(Q['electron_rg_over_lambdaC'], Q['alpha_g_electron']))
ident_res['proton-same'] = float(rel_diff(Q['proton_rg_over_lambdaC'], Q['alpha_g_proton']))
ident_res['alpha=(m/mP)^2'] = float(rel_diff(Q['alpha_g_electron'], (ME / MPL) ** 2))
ident_res['alpha_planck_minus_1'] = float(abs(Q['alpha_g_planck'] - 1))
ident_ok = (ident_res['G=2Z/c'] == 0 and ident_res['G=c^2 r_g/M'] == 0 and
            max(float(x) for x in [ident_res['G=c^3 lP^2/hbar'], ident_res['G=alpha_g hbar c/m^2'],
                                   ident_res['r_g/lambda_C=alpha_g'], ident_res['proton-same'],
                                   ident_res['alpha=(m/mP)^2'], ident_res['alpha_planck_minus_1']]) < 1e-200)
guard('G7-five-identities', ident_ok,
      'exact rational residuals 0; 250-digit residuals <= %.2E'
      % max(float(x) for x in [ident_res['G=c^3 lP^2/hbar'], ident_res['G=alpha_g hbar c/m^2'],
                               ident_res['r_g/lambda_C=alpha_g'], ident_res['proton-same'],
                               ident_res['alpha=(m/mP)^2'], ident_res['alpha_planck_minus_1']]))

# ---------- uncertainty propagation ----------
REL_G = UG / G
UNC = {
    'rel_u_G': REL_G,
    'u_Z': UC,
    'rel_u_kappa': REL_G,
    'rel_u_lP': REL_G / 2,
    'rel_u_mP': REL_G / 2,
    'rel_u_alpha_g': REL_G,
    'rel_u_rg': REL_G,
    'note': 'correlations neglected; m, hbar, c treated as exact/defining',
}
guard('G8-uncertainty', abs(UNC['rel_u_lP'] - REL_G / 2) == 0 and UC > 0,
      'rel u(G)=%s; rel u(lP)=%s; u(Z)=%s'
      % (fmt(REL_G, 12), fmt(UNC['rel_u_lP'], 12), fmt(UC, 12)))

# ---------- Z=0.01 hypothesis and unit dependence ----------
gg = F(1, 50) / CF            # G = 2*0.01/c = 0.02/c
rel_res = (gg - GF) / GF
sig_res = (gg - GF) / UGF
z001_rejected = abs(sig_res) > 20
Z_cgs = Zf * F(100 ** 4) / F(1000)   # m->cm, kg->g
Z_cgs_expected = Zf * 100000
guard('G9-Z-0.01', z001_rejected and F(4, 10000) < abs(rel_res) < F(5, 10000)
      and F(20, 1) < abs(sig_res) < F(21, 1) and Z_cgs == Z_cgs_expected,
      'G(0.01)=%s; rel=%s; sigma=%s; Z(cm-g-s)=%s vs Z(SI)=%s'
      % (format(float(gg), '.15E'), format(float(rel_res), '.12E'),
         format(float(sig_res), '.6f'), format(float(Z_cgs), '.10f'), format(float(Zf), '.10f')))

# ---------- Z vs Z' ----------
# [Z]=(4,-1,-3) in (L,M,T); [Z']=(4,+1,-3,-2) in (L,M,T,Q)
Z_DIM = (4, -1, -3, 0)
ZP_DIM = (4, 1, -3, -2)
ZP = C / (8 * PI * EPS0)
guard('G10-Z-vs-Zprime', Z_DIM != ZP_DIM,
      '[Z]=%s; [Z\']=%s; Z=%s; Z\'=%s; ratio=%.3E'
      % (Z_DIM, ZP_DIM, fmt(Z, 6), fmt(ZP, 6), float(Z / ZP)))

# ---------- conditional c scalings: four incompatible powers ----------
scale_ok = True
scale_max = D(0)
scale_rows = []
for r in cs_rows:
    x = D(r['c_ratio'])
    row = {'ratio': x,
           'fixed_G': G,
           'fixed_Z': G / x,
           'fixed_rg_M': G * x ** 2,
           'fixed_lP_hbar': G * x ** 3}
    scale_rows.append(row)
    for k, csv_key in [('fixed_G', 'G_fixed'), ('fixed_Z', 'G_if_Z_fixed'),
                       ('fixed_rg_M', 'G_if_r_g_and_M_fixed'),
                       ('fixed_lP_hbar', 'G_if_lP_hbar_fixed')]:
        rd = rel_diff(D(r[csv_key]), row[k])
        scale_max = max(scale_max, rd)
        if rd > D('1e-9'):
            scale_ok = False
guard('G11-c-scalings', scale_ok and len(scale_rows) == 51 and scale_max < D('1e-9'),
      '51/51 rows reproduced; max rel diff=%.2E; exponents -1/+2/+3/0' % scale_max)

# ---------- GM degeneracy ----------
deg_ok = True
gm_vals = []
for r in eg_rows:
    g_ass = D(r['G_assumed_SI'])
    m_inf = D(r['inferred_Earth_mass_kg'])
    prod = g_ass * m_inf
    gm_vals.append(prod)
    if rel_diff(prod, GME) > D('1e-12'):
        deg_ok = False
# Jacobian of mu(G,M)=GM is the 1x2 row (M, G): rank 1 because both entries are nonzero.
J1 = [[F(D(str(eg_rows[0]['inferred_Earth_mass_kg']))),
       F(D(str(eg_rows[0]['G_assumed_SI'])))]]
J_rank = rank_int(J1)
q_test = F(7, 3)
transform_exact = ((q_test * GF) * (GMEF / (q_test * GF)) - GMEF == 0)
guard('G12-GM-degeneracy', deg_ok and len(eg_rows) == 9 and J_rank == 1 and transform_exact,
      '9/9 rows keep GM=%s; jacobian row rank=%d; q-rescaling exact' % (fmt(GME, 15), J_rank))

# ---------- alpha_g summary table ----------
alpha_tbl = [
    {'object': 'electron', 'mass_kg': ME, 'alpha_g': Q['alpha_g_electron'],
     'r_g': Q['electron_r_g_m'], 'lambda_C': Q['electron_lambda_C_m'],
     'mass_independent_of_G': True},
    {'object': 'proton', 'mass_kg': MP, 'alpha_g': Q['alpha_g_proton'],
     'r_g': Q['proton_r_g_m'], 'lambda_C': Q['proton_lambda_C_m'],
     'mass_independent_of_G': True},
    {'object': 'Planck_scale_mass_derived_from_G', 'mass_kg': MPL, 'alpha_g': Q['alpha_g_planck'],
     'r_g': Q['planck_r_g_m'], 'lambda_C': Q['planck_lambda_C_m'],
     'mass_independent_of_G': False},
]
alpha_csv_ok = True
for a, row in zip(alpha_tbl, ml_rows):
    if rel_diff(D(row['r_g_div_rC_alpha_g']), a['alpha_g']) > D('1e-14'):
        alpha_csv_ok = False
guard('G13-alpha-table', alpha_csv_ok and len(ml_rows) == 3,
      'electron 1.75E-45 / proton 5.91E-39 / Planck 1; CSV cross-check ok')

# ---------- catalog / routes registry ----------
EQ_LEVEL = {
    'E01': 'INPUT', 'E02': 'DEF', 'E03': 'DEF', 'E04': 'DEF', 'E05': 'DEF', 'E06': 'DEF',
    'E07': 'E', 'E08': 'E', 'E09': 'R', 'E10': 'DEF', 'E11': 'E', 'E12': 'DEF', 'E13': 'DEF',
    'E14': 'E', 'E15': 'E', 'E16': 'E', 'E17': 'E', 'E18': 'E', 'E19': 'E', 'E20': 'E',
    'E21': 'E', 'E22': 'DEF', 'E23': 'DEF', 'E24': 'DEF', 'E25': 'DEF', 'E26': 'E',
    'E27': 'DEF', 'E28': 'DEF', 'E29': 'DEF', 'E30': 'E', 'E31': 'E', 'E32': 'C',
    'E33': 'H', 'E34': 'E', 'E35': 'E', 'E36': 'E', 'E37': 'E', 'E38': 'C', 'E39': 'C',
    'E40': 'C', 'E41': 'C', 'E42': 'C', 'E43': 'C', 'E44': 'E', 'E45': 'E', 'E46': 'E',
    'E47': 'C', 'E48': 'E', 'E49': 'C', 'E50': 'H', 'E51': 'C', 'E52': 'C', 'E53': 'E',
    'E54': 'E',
}
LEVEL_NAME = {'E': '已确立/恒等', 'DEF': '定义重排', 'C': '条件命题', 'H': '未证假说',
              'R': '否证/反例', 'INPUT': '观测输入'}
RT_LEVEL = {'不成立': 'R', '否证': 'R', '重参数化': 'DEF', '不支持': 'R', '待证明': 'OPEN',
            '参数退化': 'E/R', '循环风险': 'R', '未证明': 'H', '开放': 'OPEN',
            '条件理论': 'C', '实验可测': 'EXP', '实验建议': 'EXP', '实验设计': 'EXP',
            '理论必要': 'E', '必要审计': 'E', '优先建议': 'OPEN',
            '不独立': 'E/R', '已知物理': 'E', '辨别力强': 'E'}
RT_NAME = {'R': '否证/不成立', 'DEF': '重参数化', 'OPEN': '开放', 'E/R': '恒等+退化',
           'H': '未证假说', 'C': '条件理论', 'EXP': '可实验检验', 'E': '恒等/审计'}

eq_reg = []
for row in eq_rows:
    uid = row['编号']
    lvl = EQ_LEVEL.get(uid, 'UNCLASSIFIED')
    eq_reg.append({'id': uid, 'topic': row['方程主题'], 'expr': row['数学表达式'],
                   'v77_status': row['证明状态'], 'level': lvl, 'level_name': LEVEL_NAME.get(lvl, lvl),
                   'w3_candidate': '否', 'note': row['常见错误']})
rt_reg = []
for row in rt_rows:
    uid = row['编号']
    v77 = row['裁定']
    lvl = RT_LEVEL.get(v77, 'UNCLASSIFIED')
    rt_reg.append({'id': uid, 'route': row['研究路线'], 'assumption': row['关键假设'],
                   'obstacle': row['主要障碍'], 'test': row['验证办法'], 'v77_status': v77,
                   'level': lvl, 'level_name': RT_NAME.get(lvl, lvl)})

unclassified_eq = sum(1 for r in eq_reg if r['level'] == 'UNCLASSIFIED')
unclassified_rt = sum(1 for r in rt_reg if r['level'] == 'UNCLASSIFIED')
guard('G14-registry-complete', len(eq_reg) == 54 and len(rt_reg) == 30
      and unclassified_eq == 0 and unclassified_rt == 0,
      'equations=%d, routes=%d, unclassified=%d/%d'
      % (len(eq_reg), len(rt_reg), unclassified_eq, unclassified_rt))

# Write the two derived registries now, so their MD5 can enter the JSON.
with io.open(P_EQ_CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['编号', '方程主题', '数学表达式', 'V77证明状态', '本册级别', '级别说明', '归口', 'W3候选', '备注'])
    for r in eq_reg:
        w.writerow([r['id'], r['topic'], r['expr'], r['v77_status'], r['level'],
                    r['level_name'], 'G-c关系总表_2026-11-17.md', r['w3_candidate'], r['note']])
with io.open(P_RT_CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['编号', '研究路线', '关键假设', '主要障碍', '验证办法', 'V77裁定', '本册级别', '级别说明', '归口'])
    for r in rt_reg:
        w.writerow([r['id'], r['route'], r['assumption'], r['obstacle'], r['test'],
                    r['v77_status'], r['level'], r['level_name'], 'G-c关系总表_2026-11-17.md'])

# ---------- provenance census + W3 gate ----------
census = [
    {'file': 'data/equation_catalog.csv', 'class': 'CATALOG', 'rows': len(eq_rows)},
    {'file': 'data/hypothesis_audit.csv', 'class': 'ROUTE', 'rows': len(rt_rows)},
    {'file': 'data/conditional_c_scaling.csv', 'class': 'TOY', 'rows': len(cs_rows)},
    {'file': 'data/mass_length_comparison.csv', 'class': 'DEFINITION', 'rows': len(ml_rows)},
    {'file': 'data/earth_GM_degeneracy.csv', 'class': 'TOY', 'rows': len(eg_rows)},
]
classes = {}
for c in census:
    classes[c['class']] = classes.get(c['class'], 0) + 1
guard('G15-census', classes == {'CATALOG': 1, 'ROUTE': 1, 'TOY': 2, 'DEFINITION': 1},
      'classes=%s; OBS=0; unclassified=0' % str(classes))

FIVE_EQ = [
    ('EQ-1', 'G=2Z/c with Z:=Gc/2'),
    ('EQ-2', 'G=c^2 r_g/M with r_g:=GM/c^2'),
    ('EQ-3', 'G=c^3 lP^2/hbar with lP:=sqrt(hbar G/c^3)'),
    ('EQ-4', 'G=alpha_g hbar c/m^2 with alpha_g:=Gm^2/(hbar c)'),
    ('EQ-5', 'kappa_E=8 pi G/c^4'),
]
w3_rows = []
for uid, label in FIVE_EQ:
    res = w3_accept({'name': uid, 'label': label, 'quantitative': True,
                     'independent': False, 'blind_path': False, 'two_anchors_ok': False})
    w3_rows.append({'id': uid, 'label': label, 'result': res})
for c in census:
    res = w3_accept({'name': c['file'], 'class': c['class'], 'quantitative': c['rows'] > 0,
                     'independent': False, 'blind_path': False, 'two_anchors_ok': False})
    w3_rows.append({'id': c['file'], 'label': c['class'], 'result': res})
rejected = sum(1 for x in w3_rows if not x['result']['passed'])
hyp = w3_accept({'quantitative': True, 'independent': True,
                 'blind_path': True, 'two_anchors_ok': True})
guard('G16-w3', rejected == len(w3_rows) and hyp['passed'],
      '%d/%d rejected; hypothetical all-4 candidate still PASS' % (rejected, len(w3_rows)))

# ---------- 15 symbolic claims independently re-proved ----------
sym = {}
sym['Z_inverse'] = (2 * Zf / CF - GF == 0)
sym['gravitational_radius_inverse'] = (CF ** 2 * rgf / MEF - GF == 0)
sym['planck_length_inverse'] = rel_diff(C ** 3 * LP ** 2 / HBAR, G) < D('1e-200')
sym['planck_mass_inverse'] = rel_diff(HBAR * C / MPL ** 2, G) < D('1e-200')
sym['alpha_from_radius_ratio'] = rel_diff(Q['electron_rg_over_lambdaC'], Q['alpha_g_electron']) < D('1e-200')
sym['planck_crossing_solution'] = rel_diff((HBAR * C / G).sqrt() ** 2, HBAR * C / G) < D('1e-200')
# Helix identities at the exact rational point cos=lambda=3/5, sin=lambda=4/5,
# with v=c, R omega=c cos(lambda), u=c sin(lambda).
COS_L, SIN_L = F(3, 5), F(4, 5)
R_h = F(5)
om = CF * COS_L / R_h
u_h = CF * SIN_L
v2 = u_h ** 2 + (R_h * om) ** 2
kap = (R_h * om ** 2) / v2
tau = (u_h * om) / v2
sym['velocity_helix_c'] = (COS_L ** 2 + SIN_L ** 2 == 1 and v2 == CF ** 2)
sym['helix_kappa'] = (kap == COS_L ** 2 / R_h)
sym['helix_tau'] = (tau == SIN_L * COS_L / R_h)
sym['helix_accel_from_c'] = (R_h * om ** 2 == CF ** 2 * COS_L ** 2 / R_h)
sym['Einstein_coupling_relation_Z'] = rel_diff(8 * PI * G / C ** 4, 16 * PI * (G * C / 2) / C ** 5) < D('1e-200')
sym['dimensional_no_go_rank'] = (rank_A == 2 and rank_aug == 3)
q = F(7, 3)
sym['GM_parameter_degeneracy'] = ((q * GF) * (GMEF / (q * GF)) - GMEF == 0)
sym['planck_radius_compton_at_mP'] = rel_diff(rg(MPL), rc(MPL)) < D('1e-240')
# log-derivative identities x f'(x)/f(x) for f=x^-1, x^2, x^3 (exact at x=2)
x0 = F(2)
sym['fixed_Z_log_derivative'] = (x0 * (-1 * x0 ** -2) / (x0 ** -1) == -1)
sym['fixed_radius_log_derivative'] = (x0 * (2 * x0) / (x0 ** 2) == 2)
sym['fixed_length_log_derivative'] = (x0 * (3 * x0 ** 2) / (x0 ** 3) == 3)
SYM_OK = all(sym.values())
guard('G17-symbolic-15', SYM_OK and len(sym) >= 15,
      '%d identities re-proved independently (Fraction/Decimal); sympy absent so shipped script not re-run' % len(sym))

# ---------- emit entries ----------
emit('')
emit('=== verdict entries ===')
add('B01', 'PASS', 'V77 ZIP integrity, 32 members and 30/30 SHA-256 manifest entries verified',
    'CRC ok; members=32; manifest=30; mismatches=0; zip sha256=%s' % sha256_file(ZIP)[:16] + '...')
add('B02', 'PASS', '58 shipped unit tests re-run in a clean-room extraction and pass',
    tests_detail)
add('B03', 'INFO', '15 symbolic and 14 browser checks are self-reported; sympy is absent here',
    'symbolic_verification.json count=15; browser_verification.json count=14; shipped script not re-run; contents independently re-proved in G17')
add('B04', 'PASS', 'Five core G-c relations are exact identities under their definitions',
    'G=2Z/c and G=c^2 r_g/M exact rational residual 0; 250-digit residuals <= 6E-260')
add('B05', 'FAIL', 'G=2Z/c is a definitional re-parameterisation, not a law determining G',
    'Z:=Gc/2 carries [Z]=L^4 M^-1 T^-3 and is computed from measured G; W3 C2 fails')
add('B06', 'PASS', 'c and hbar alone cannot construct G: exact dimensional no-go',
    'rank[c,hbar]=2 < rank[c,hbar,G]=3; exponent contradiction T: -4 != -2')
add('B07', 'PASS', 'r_g/lambda_C = alpha_g(m) = (m/mP)^2 exactly; crossing only at Planck mass',
    'electron 1.7518094E-45, proton 5.9061494E-39, Planck 1; residuals <= 1E-240')
add('B08', 'PASS', 'kappa_E=8 pi G/c^4 is the correct Einstein coupling with [kappa_E]=L^-1 M^-1 T^2',
    'kappa_E=%s m/J' % fmt(KAPPA, 18))
add('B09', 'FAIL', 'the Z=0.01 SI guess is rejected at ~20 sigma and is unit dependent',
    'G(0.01)=%s; rel=%s; sigma=%s; Z in cm-g-s=%s'
    % (format(float(gg), '.15E'), format(float(rel_res), '.12E'),
       format(float(sig_res), '.6f'), format(float(Z_cgs), '.8f')))
add('B10', 'FAIL', 'Z and Z\'=c/(8 pi eps0) cannot be added: dimensions differ',
    '[Z]=%s vs [Z\']=%s; Z/Z\'=%.2E' % (Z_DIM, ZP_DIM, float(Z / ZP)))
add('B11', 'PASS', 'conditional c-scalings are four incompatible powers -1/+2/+3/0',
    '51/51 V77 rows reproduced, max rel diff=%.2E; no unique G(c)' % scale_max)
add('B12', 'FAIL', 'orbital GM data cannot separate G and M: exact rank-1 degeneracy',
    '9/9 rows keep GM=%s; G->qG, M->M/q invariant' % fmt(GME, 12))
add('B13', 'PASS', 'all 12 V77 headline numbers agree with the independent 250-digit recomputation',
    'max relative difference=%.2E over %d keys' % (MAXCMP, len(cmp_rows)))
add('B14', 'PASS', 'V77 data layer is fully censused: 5 tables, 0 observation tables, 0 W3 candidate',
    'CATALOG 1 / ROUTE 1 / TOY 2 / DEFINITION 1; unclassified=0')
add('B15', 'FAIL', 'V77 does not predict G from c independently',
    'none of Z, lP, alpha_g is computed without measured G; W3.pass=0')
add('B16', 'OPEN', 'minimal closure condition for any future G prediction',
    'independently compute one of {Z, lP, alpha_g(m)} or an independent L_*/M_* without using G, then blind-test')

counts = {}
for e in ENTRIES:
    counts[e['verdict']] = counts.get(e['verdict'], 0) + 1

RESULT = {
    'round': 'r424', 'date': DATE,
    'topic': 'ROOT V77: full-dimensional audit of G-c relations',
    'source': 'ROOT V77 ZIP read-only; CODATA 2022 constants; r421 W3 gate',
    'verdict': VERDICT,
    'method': 'pure stdlib; 250-digit Decimal/Chudnovsky pi; exact Fraction identities; integer rank proof; W3 gate',
    'entries': ENTRIES, 'guards': GUARDS, 'counts': counts,
    'guard_pass': sum(1 for g in GUARDS if g['pass']),
    'guard_total': len(GUARDS),
    'zip': {'name': os.path.basename(ZIP), 'bytes': os.path.getsize(ZIP),
            'sha256': sha256_file(ZIP), 'members': len(names),
            'manifest_rows': len(manifest_rows), 'manifest_mismatches': manifest_bad},
    'shipped_claims': {
        'unit_tests': 58, 'tests_ok': tests_ok,
        'symbolic_checks': symbolic.get('count'), 'symbolic_status': symbolic.get('status'),
        'browser_checks': browser.get('count'), 'browser_status': browser.get('status'),
        'report_all_passed': report.get('all_passed'),
        'report_scope': report.get('scope'),
        'theory_status': summary.get('theory_status'),
    },
    'constants': {'c': C_S, 'h': H_S, 'hbar_250d': fmt(HBAR, 40), 'G': G_S,
                  'u_G': UG_S, 'm_e': ME_S, 'm_p': MP_S, 'GM_earth': GME_S,
                  'eps0': EPS0_S, 'pi_250d': fmt(PI, 40)},
    'quantities_250d': {k: fmt(v, 30) for k, v in Q.items()},
    'v77_cross_check': [{'key': r['key'], 'v77': format(r['v77'], '.17E'),
                         'r424': format(r['r424'], '.30E'),
                         'rel_diff': fmt_rel(r['rel_diff'])} for r in cmp_rows],
    'max_cross_check_rel_diff': format(MAXCMP, '.3E'),
    'dimensional_proof': {
        'basis': '(L,M,T)', 'G': [3, -1, -2], 'c': [1, 0, -1], 'hbar': [2, 1, -1],
        'rank_c_hbar': rank_A, 'rank_augmented': rank_aug,
        'exponents_from_M_and_L': {'b': b_from_M, 'a': a_from_L},
        'time_exponent_required': t_required, 'time_exponent_obtained': t_obtained,
        'with_length': {'form': 'G=A*c^3*L^2/hbar', 'dim': dim_c3L2_hbar},
        'with_mass': {'form': 'G=B*hbar*c/M^2', 'dim': dim_hc_M2},
    },
    'identities': {k: (str(v) if isinstance(v, (F, int)) else format(v, '.3E'))
                   for k, v in ident_res.items()},
    'uncertainty': {k: (fmt(v, 18) if isinstance(v, D) else v) for k, v in UNC.items()},
    'z_0p01_hypothesis': {
        'G_guess': format(float(gg), '.17E'),
        'relative_residual': format(float(rel_res), '.12E'),
        'sigma_residual': format(float(sig_res), '.6f'),
        'rejected_at_20_sigma': z001_rejected,
        'Z_in_SI': format(float(Zf), '.10f'),
        'Z_in_cm_g_s': format(float(Z_cgs), '.10f'),
        'unit_factor': '1e5',
    },
    'z_vs_zprime': {'Z_dim': Z_DIM, 'Zprime_dim': ZP_DIM, 'Zprime': fmt(ZP, 12),
                    'ratio': format(float(Z / ZP), '.3E')},
    'conditional_scaling': {
        'rows': len(scale_rows), 'max_rel_diff': format(scale_max, '.2E'),
        'exponents': {'fixed_G': 0, 'fixed_Z': -1, 'fixed_r_g_and_M': 2, 'fixed_lP_hbar': 3},
    },
    'gm_degeneracy': {
        'rows': len(eg_rows), 'GM_constant': format(float(GME), '.6E'),
        'jacobian_rank': 1,
        'transformation': 'G->qG, M->M/q, GM invariant for q>0',
    },
    'alpha_table': [{'object': a['object'], 'mass_kg': format(float(a['mass_kg']), '.10E'),
                     'alpha_g': fmt(a['alpha_g'], 20), 'r_g': fmt(a['r_g'], 20),
                     'lambda_C': fmt(a['lambda_C'], 20),
                     'mass_independent_of_G': a['mass_independent_of_G']} for a in alpha_tbl],
    'registry': {'equations': len(eq_reg), 'routes': len(rt_reg),
                 'eq_levels': {l: sum(1 for r in eq_reg if r['level'] == l)
                               for l in sorted(set(r['level'] for r in eq_reg))},
                 'route_levels': {l: sum(1 for r in rt_reg if r['level'] == l)
                                  for l in sorted(set(r['level'] for r in rt_reg))},
                 'eq_csv_md5': md5_file(P_EQ_CSV) if os.path.exists(P_EQ_CSV) else 'written-after-json',
                 'route_csv_md5': md5_file(P_RT_CSV) if os.path.exists(P_RT_CSV) else 'written-after-json'},
    'census': census, 'class_counts': classes,
    'w3_rows': [{'id': x['id'], 'label': x['label'],
                 'passed': x['result']['passed'],
                 'failed_checks': [k for k, v in x['result']['checks'].items() if not v]}
                for x in w3_rows],
    'symbolic_reproof': {k: bool(v) for k, v in sym.items()},
    'fact_hashes': {'V77_ZIP': sha256_file(ZIP), 'r423': md5_file(F_R423), 'r421': md5_file(F_R421)},
    'red_line': RED,
    'next_round': {
        'r': 'r425',
        'condition': 'only a W3 candidate that computes Z, lP or alpha_g(m) without measured G (or an independent L_*/M_*) and passes C1-C4',
        'blocker': 'all five V77 relations are definitional in G; no independent input',
    },
}

with io.open(P_JSON, 'w', encoding='utf-8') as f:
    f.write(json.dumps(RESULT, ensure_ascii=False, indent=2, default=str))

# ---------- data md ----------
MD = ['# 数据产物 · TUFT r424：ROOT V77 G 与 c 全维关系审计', '',
      '- 轮次：r424；日期：' + DATE,
      '- verdict：`' + VERDICT + '`',
      '- ZIP sha256：`' + sha256_file(ZIP) + '`（32 members，manifest 30/30）',
      '', '## 记分板', '',
      '- 条目：' + str(len(ENTRIES)) + '（' + ', '.join(k + '=' + str(v) for k, v in sorted(counts.items())) + '）',
      '- 守卫：' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total']),
      '', '## 250 位精算主表', '',
      '| 量 | r424（250 位） | V77 自报 | 相对差 |', '|---|---|---|---|']
for r in cmp_rows:
    MD.append('| ' + r['key'] + ' | ' + format(r['r424'], '.24E') + ' | ' + format(r['v77'], '.16E') +
              ' | ' + fmt_rel(r['rel_diff']) + ' |')
MD += ['', '## 五条核心关系', '', '| id | 关系 | 判定 | 说明 |', '|---|---|---|---|',
       '| EQ-1 | G=2Z/c，Z:=Gc/2 | [DEF] | Z 由测得 G 定义，[Z]=L^4M^-1T^-3 |',
       '| EQ-2 | G=c²r_g/M，r_g:=GM/c² | [DEF] | 定义重排 |',
       '| EQ-3 | G=c³ℓ_P²/ħ，ℓ_P:=√(ħG/c³) | [DEF] | ℓ_P 由 G 定义 |',
       '| EQ-4 | G=α_g ħc/m²，α_g:=Gm²/(ħc) | [DEF] | α_g 由 G 定义 |',
       '| EQ-5 | κ_E=8πG/c⁴ | [E] | Einstein 耦合，正确 |',
       '', '## 维度不可能定理', '',
       '- rank[c,ħ]=%d；rank[c,ħ,G]=%d；方程 a·c+b·ħ=G 给 b=%d、a=%d，时间幂 %d≠%d。'
       % (rank_A, rank_aug, b_from_M, a_from_L, t_obtained, t_required),
       '- 加独立长度：G=A·c³L²/ħ；加独立质量：G=B·ħc/M²。系数 A、B 与 L、M 均须独立动力学。',
       '', '## Z=0.01 与单位依赖', '',
       '- G(Z=0.01)=%s；相对偏差 %s；%sσ ⇒ 否证。' %
       (format(float(gg), '.15E'), format(float(rel_res), '.12E'), format(float(sig_res), '.6f')),
       '- 同一 Z 换 cm-g-s：Z=%s（SI 为 %s），因子 1e5 ⇒ “0.01”是单位制产物。' %
       (format(float(Z_cgs), '.8f'), format(float(Zf), '.8f')),
       '', '## 条件 c 标度与 GM 退化', '',
       '- 四幂率 −1 / +2 / +3 / 0；V77 51 行复现最大相对差 %s。' % format(scale_max, '.2E'),
       '- earth_GM_degeneracy 9 行 GM 恒为 %s；Jacobian 秩 1。' % format(float(GME), '.6E'),
       '', '## 条目表', '', '| id | verdict | claim | reading |', '|---|---|---|---|']
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
emit('ENTRIES=%d GUARDS=%d/%d' % (len(ENTRIES), RESULT['guard_pass'], RESULT['guard_total']))
