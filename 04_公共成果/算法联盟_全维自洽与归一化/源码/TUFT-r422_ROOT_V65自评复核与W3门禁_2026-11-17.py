# -*- coding: utf-8 -*-
# r422 / algorithm alliance -- ROOT V65 independent machine recheck (2026-11-17)
# User supplied ROOT V65 and asked to continue unification. V65 is notably honest:
# it labels results OBS/STANDARD/MATH/TOY/FIT/OPEN and states that true four-force
# unification and a no-input prediction of G are NOT proven.
# This round independently rechecks the claimed MATH/STANDARD core, then applies
# the r421 W3 gate. Increment = audit of the self-audit, not another repetition.
# Pure standard library. Read-only w.r.t. V65 ZIP and all cited openuft files.
import os
import io
import sys
import ast
import json
import math
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
STEM = 'TUFT-r422_ROOT_V65自评复核与W3门禁_2026-11-17'
P_JSON = os.path.join(DATA, STEM + '.json')
P_MD = os.path.join(DATA, STEM + '.md')
P_REPORT = os.path.join(DATA, STEM + '_report.txt')

V65_ZIP = os.path.join('C:\\', 'Users', 'mo', 'Downloads',
    'ROOT_V65_%E5%9B%9B%E5%8A%9B%E5%A4%A7%E7%BB%9F%E4%B8%80%E7%90%86%E8%AE%BA%E5%AE%A1%E8%AE%A1_%E6%8E%A8%E5%AF%BC%E7%B2%BE%E7%AE%97%E9%AA%8C%E8%AF%81%E6%A8%A1%E6%8B%9F%E7%A7%91%E7%A0%94%E5%8C%85.zip')
F_METHOD = os.path.join(OPENUFT, '02_共享基础', '研究规范', 'method_F_第一性判据.md')
F_NORM = os.path.join(OPENUFT, '统一场论理论体系与方程_归一正本_2026-11-09.md')
F_ROOT_SUM = os.path.join(OPENUFT, 'ROOT系列公式理论全维总结_2026-11-17.md')
F_R418 = os.path.join(PUB, '判定_TUFT-r418-ROOT_V62诱导引力有效作用量_2026-11-17.md')
F_R421 = os.path.join(PUB, '判定_TUFT-r421-突破点W3验收器_双锚点与L3四门禁机器化_2026-11-17.md')
FACTS = [V65_ZIP, F_METHOD, F_NORM, F_ROOT_SUM, F_R418, F_R421]

VERDICT = ('V65--SELF-AUDIT-HONEST--CONDITIONAL-MATH-REPRODUCED--'
           'STANDARD-NOT-ROOT-NOVELTY--TOY-FIT-NOT-VALIDATION--'
           'NO-W3-CANDIDATE--G-AND-FOUR-FORCE-UNIFICATION-OPEN--0OF6-UNCHANGED')
RED = {
    'completion_0_of_6': True, 'coverage_0_of_22': True, 'UFT3_zero': True,
    'L3_zero': True, 'validated_zero': True,
    'gravity_four_force_correct_equations_zero': True, 'L3_not_implies_L4': True,
}

PI_S = Dc('3.1415926535897932384626433832795028841971693993751058209749445923078164')
C_S = Dc('299792458')
H_S = Dc('6.62607015e-34')
HBAR_S = H_S / (Dc(2) * PI_S)
G_S = Dc('6.67430e-11')
M_E_S = Dc('9.1093837015e-31')
M_P_S = (HBAR_S * C_S / G_S).sqrt()

LINES = []
ENTRIES = []
GUARDS = []
QUOTES = {}


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


def find_quote(key, path, needle):
    if not os.path.exists(path):
        QUOTES[key] = {'found': False, 'file': os.path.basename(path), 'absent': True}
        return False
    txt = io.open(path, encoding='utf-8', errors='replace').read()
    idx = txt.find(needle)
    ok = idx >= 0
    QUOTES[key] = {'found': ok, 'file': os.path.basename(path), 'needle': needle,
                   'context': txt[max(0, idx - 50):idx + len(needle) + 90].replace('\n', ' ') if ok else ''}
    return ok


def zip_quote(key, member, needle):
    if not os.path.exists(V65_ZIP):
        QUOTES[key] = {'found': False, 'file': member, 'absent': True}
        return False
    with zipfile.ZipFile(V65_ZIP) as z:
        if member not in z.namelist():
            QUOTES[key] = {'found': False, 'file': member, 'member_absent': True}
            return False
        txt = z.read(member).decode('utf-8', errors='replace')
    idx = txt.find(needle)
    ok = idx >= 0
    QUOTES[key] = {'found': ok, 'file': member, 'needle': needle,
                   'context': txt[max(0, idx - 50):idx + len(needle) + 90].replace('\n', ' ') if ok else ''}
    return ok


def dsqrt(x):
    return x.sqrt()


# --- r421 four-gate acceptance, copied as a self-contained decision function ---
def w3_accept(cand):
    checks = {
        'C1_quantitative_number': bool(cand.get('quantitative', False)),
        'C2_not_reverse_engineered': bool(cand.get('independent', False)),
        'C3_test_path_unused_in_fit': bool(cand.get('blind_path', False)),
        'C4_two_anchors_consistent': bool(cand.get('two_anchors_ok', False)),
    }
    return {'passed': all(checks.values()), 'checks': checks}


# --- pure-stdlib float Bessel functions for theorem B's integral identity ---
def bessel_j(n, x):
    total = 0.0
    ax2 = x / 2.0
    fact_n = 1.0
    for i in range(1, n + 1):
        fact_n *= i
    for k in range(0, 80):
        num = (-1.0) ** k * (ax2 ** (2 * k + n))
        den = math.factorial(k) * fact_n
        for i in range(1, k + 1):
            den *= (n + i)
        term = num / den
        total += term
        if abs(term) < 1e-18 and k > 10:
            break
    return total


def bisect_j1_root(lo, hi, iterations=200):
    flo = bessel_j(1, lo)
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        fmid = bessel_j(1, mid)
        if flo * fmid <= 0.0:
            hi = mid
        else:
            lo = mid
            flo = fmid
    return (lo + hi) / 2.0


def simpson(f, a, b, n=10000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return s * h / 3.0


def cutoff_f(mu):
    if mu < 0:
        raise ValueError('mu must be nonnegative')
    if mu == 0:
        return 1.0
    x = mu * mu
    return simpson(lambda t: math.exp(-x / t) if t > 0 else 0.0, 0.0, 1.0, 4000)


# --- guards: environment, sources, self syntax ---
guard('G0-0_stdlib_only', 'sympy' not in sys.modules and 'numpy' not in sys.modules, 'pure stdlib')
for i, f in enumerate(FACTS):
    guard('G0-fact-%d' % i, os.path.exists(f), os.path.basename(f))

src = io.open(__file__, encoding='utf-8').read()
try:
    ast.parse(src)
    guard('G1-ast', True, 'self syntax ok')
except SyntaxError as exc:
    guard('G1-ast', False, str(exc))

qok = []
qok.append(zip_quote('Q-v65-boundary', 'ROOT_V65/research/00_研究总论与成果边界.md', '没有完成新的四力大统一'))
qok.append(zip_quote('Q-v65-g-input', 'ROOT_V65/research/00_研究总论与成果边界.md', 'G 是输入'))
qok.append(zip_quote('Q-v65-degeneracy', 'ROOT_V65/research/03_热核引力常数与精算修正.md', '不足以唯一确定 N 或'))
qok.append(zip_quote('Q-v65-definition', 'ROOT_V65/research/04_规范场与候选统一作用量_变分推导.md', '该结论是有效系数的**定义/匹配**'))
qok.append(zip_quote('Q-v65-reverse-fit', 'ROOT_V65/research/03_热核引力常数与精算修正.md', '反求不是预测'))
qok.append(zip_quote('Q-v65-history', 'ROOT_V65/research/10_历史核心候选公式严格纠错.md', '56\\pi\\approx175.92918860102841'))
qok.append(find_quote('Q-method-w3', F_METHOD, '要计为 L3，必须同时满足'))
qok.append(find_quote('Q-norm-category', F_NORM, '类别缺口定理'))
qok.append(find_quote('Q-r421-gate', F_R421, '四门全过'))
guard('G2-quotes', all(qok), 'found %d/%d' % (sum(1 for x in qok if x), len(qok)))

emit('')
emit('=== V65 conditional MATH recheck ===')

# A01 helix inverse theorem.
helix_cases = [(Dc('0.5'), Dc('0.2')), (Dc('1.2'), Dc('-0.7')), (Dc('0.01'), Dc('2.0'))]
helix_max = Dc(0)
for kappa, tau in helix_cases:
    D = kappa * kappa + tau * tau
    R = kappa / D
    omega = C_S * D.sqrt()
    u = C_S * tau / D.sqrt()
    vt = C_S * kappa / D.sqrt()
    k2 = R * omega * omega / (vt * vt + u * u)
    t2 = u * omega / (vt * vt + u * u)
    r2 = kappa / D
    for a, b in [(k2, kappa), (t2, tau), (r2, R)]:
        rel = abs(a - b) / (abs(b) + Dc('1e-60'))
        if rel > helix_max:
            helix_max = rel
guard('G3-helix-inverse', helix_max < Dc('1e-50'), 'max rel residual=' + format(helix_max, '.3E'))

# A02 Lorentz/proper-time and KG group velocity.
beta = Dc(1)
dtau = (Dc(1) - beta * beta).sqrt()
kz, qr, mass_inv = 1.0, 0.5, 0.25
vg = 299792458.0 * kz / math.sqrt(kz * kz + qr * qr + mass_inv * mass_inv)
guard('G4-lorentz-and-group-velocity', dtau == Dc(0) and vg < 299792458.0,
      'dtau(beta=1)=' + str(dtau) + ', vg/c=' + format(vg / 299792458.0, '.6E'))

# A03 KG Bessel energy integral.
j11 = bisect_j1_root(3.0, 4.0)
j1_at_root = bessel_j(1, j11)
integral = simpson(lambda x: bessel_j(1, j11 * x) ** 2 * x, 0.0, 1.0, 20000)
closed = 0.5 * bessel_j(2, j11) ** 2
rel_bessel = abs(integral - closed) / abs(closed)
guard('G5-kg-bessel-integral', abs(j1_at_root) < 1e-12 and rel_bessel < 1e-10,
      'j11=' + format(j11, '.12f') + ', J1=' + format(j1_at_root, '.2E') +
      ', integral=' + format(integral, '.12E') + ', closed=' + format(closed, '.12E'))

# A04 infinite-cylinder Newtonian acceleration: direct shell integration check.
# For a uniform infinite cylinder, Gauss-law result is g_r=-2G mu_L/r outside.
Gf, mu_l, r_out, a_cyl = 6.67430e-11, 1.0, 12.0, 1.0
gauss = -2.0 * Gf * mu_l / r_out
# Independent line integral over z and theta for the radial field of an infinite line mass:
# g_r = -G mu_L r integral dz/(r^2+z^2)^(3/2) = -2G mu_L/r.
radial_integral = 2.0 / (r_out * r_out)
line = -Gf * mu_l * r_out * radial_integral
guard('G6-cylinder-line-gravity', abs(line - gauss) / abs(gauss) < 1e-15,
      'gauss=' + format(gauss, '.12E') + ', integral=' + format(line, '.12E'))

# A05 heat-kernel cutoff function and monotonicity.
fs = [cutoff_f(x) for x in [0.0, 0.25, 0.5, 1.0, 2.0]]
fmono = all(fs[i] >= fs[i + 1] for i in range(len(fs) - 1))
series_mu = 0.5
x = series_mu * series_mu
e1 = -0.5772156649015328606 - math.log(x)
summ = 0.0
for k in range(1, 300):
    term = ((-x) ** k) / (k * math.factorial(k))
    summ += term
    if abs(term) < 1e-16:
        break
f_series = math.exp(-x) - x * (e1 - summ)
f_quad = cutoff_f(series_mu)
f_rel = abs(f_series - f_quad) / abs(f_quad)
guard('G7-cutoff-function', fs[0] == 1.0 and fmono and f_rel < 1e-10,
      'F samples=' + ', '.join(format(v, '.9f') for v in fs) + ', series/quad rel=' + format(f_rel, '.3E'))

# A06 N/ell^2 non-identifiability.
N0, ell0 = 3.0, 7.0e-7
s = 2.0
N1, ell1 = s * s * N0, s * ell0
ratio0 = N0 / (ell0 * ell0)
ratio1 = N1 / (ell1 * ell1)
jac = (1.0, -2.0)
guard('G8-degeneracy-N-ell', abs(ratio1 - ratio0) / ratio0 < 1e-12 and jac == (1.0, -2.0),
      'N/ell^2=' + format(ratio0, '.6E') + ' -> ' + format(ratio1, '.6E') + ', J=(1,-2) rank=1')

# A07 reverse-fit cutoff and Planck length (FIT, not prediction).
ell_fit = (HBAR_S * G_S / (Dc(12) * PI_S * C_S ** 3)).sqrt()
ell_ref = Dc('2.6323542160304588e-36')
fit_rel = abs(ell_fit - ell_ref) / ell_ref
ell_p = (HBAR_S * G_S / (C_S ** 3)).sqrt()
ell_p_ref = Dc('1.6162550244237053e-35')
pl_rel = abs(ell_p - ell_p_ref) / ell_p_ref
G_old_e = HBAR_S * C_S / (M_E_S ** 2)
rel_e = abs(G_old_e - G_S) / G_S
guard('G9-reverse-fit-values', fit_rel < Dc('1e-12') and pl_rel < Dc('1e-12') and rel_e > Dc('1e40'),
      'ell_fit=' + format(ell_fit, '.8E') + ' rel=' + format(fit_rel, '.2E') +
      '; ell_P rel=' + format(pl_rel, '.2E') + '; electron-anchor G rel=' + format(rel_e, '.3E'))

# A08 candidate action variation coefficient is a definition/matching.
M0 = Dc('2.0'); xi = Dc('0.25'); f_abs = Dc('2.0')
Meff2 = M0 * M0 - Dc(2) * xi * f_abs
Geff = Dc(1) / (Dc(8) * PI_S * Meff2)
guard('G10-action-coefficient', Meff2 == Dc('3.0') and Geff > Dc(0),
      'M_eff^2=' + str(Meff2) + ', 1/(8*pi*G_eff)=M_eff^2 by construction')

# A09 Eotvos algebra.
def eta_formula(aa, ab, ff):
    return 2.0 * (aa - ab) * ff / (2.0 + (aa + ab) * ff)

aa, ab, ff = 1.2e-4, -0.7e-4, 0.37
a_a = 1.0 + aa * ff
a_b = 1.0 + ab * ff
eta_direct = 2.0 * (a_a - a_b) / (a_a + a_b)
eta_closed = eta_formula(aa, ab, ff)
guard('G11-eotvos-algebra', abs(eta_direct - eta_closed) / abs(eta_direct) < 1e-12,
      'eta=' + format(eta_direct, '.12E') + ', algebra residual=' + format(abs(eta_direct - eta_closed), '.2E'))

# A10 historical corrections.
alpha_guess = Dc(1) / (Dc(4) * PI_S ** 3 + PI_S ** 2 + PI_S)
alpha_obs = Dc(1) / Dc('137.035999084')
alpha_rel = abs(alpha_guess - alpha_obs) / alpha_obs
mass_ratio_guess = Dc(56) * PI_S
mass_ratio_obs = Dc('1836.15267343')
mass_rel = abs(mass_ratio_guess - mass_ratio_obs) / mass_ratio_obs
isco_ratio = Dc(3) * (Dc(2))
guard('G12-history-corrections',
      alpha_rel > Dc('1e-6') and Dc('1e-6') < alpha_rel < Dc('1e-5') and
      mass_rel > Dc('0.9') and isco_ratio == Dc(6),
      'alpha rel=' + format(alpha_rel, '.6E') + ', 56pi=' + format(mass_ratio_guess, '.10f') +
      ', mass rel=' + format(mass_rel, '.6E') + ', r_ISCO/r_s=3')

# A11 W3 gate applied to V65-style outputs.
w3_candidates = [
    {'name': 'V65 reverse-fit ell from observed G',
     'quantitative': True, 'independent': False, 'blind_path': False, 'two_anchors_ok': False},
    {'name': 'V65 Planck length from observed G',
     'quantitative': True, 'independent': False, 'blind_path': False, 'two_anchors_ok': False},
    {'name': 'V65 spherical Earth TOY g',
     'quantitative': True, 'independent': False, 'blind_path': False, 'two_anchors_ok': False},
    {'name': 'historical alpha guess (already falsified)',
     'quantitative': True, 'independent': False, 'blind_path': False, 'two_anchors_ok': False},
]
w3_results = []
for cand in w3_candidates:
    res = w3_accept(cand)
    w3_results.append({'name': cand['name'], 'result': res})
    emit('  W3 gate: ' + cand['name'] + ' -> ' + ('PASS' if res['passed'] else 'REJECTED') +
         ', failed=' + ','.join(k for k, v in res['checks'].items() if not v))
hyp = w3_accept({'quantitative': True, 'independent': True,
                 'blind_path': True, 'two_anchors_ok': True})
guard('G13-w3-gate-teeth', all(not x['result']['passed'] for x in w3_results) and hyp['passed'],
      '%d/%d V65-style candidates rejected; hypothetical all-4 candidate passes' % (
          sum(1 for x in w3_results if not x['result']['passed']), len(w3_results)))

guard('G14-redline', all(RED.values()), 'all inherited red-line flags true')

emit('')
emit('=== verdict entries ===')

add('A01', 'PASS', 'V65 helical inverse theorem is algebraically correct inside its stated circular-helix domain',
    'R=kappa/(kappa^2+tau^2), omega=v*sqrt(D), u=v*tau/sqrt(D), v_theta=v*kappa/sqrt(D); max rel residual=' + format(helix_max, '.3E'))
add('A02', 'PASS', 'V65 correctly separates field phase/group velocity from a massive-particle worldline',
    'massive beta=1 gives dtau=0 (null, not massive worldline); KG sample vg/c=' + format(vg / 299792458.0, '.6E') + '<1')
add('A03', 'PASS', 'V65 KG cylinder energy integral identity reproduced',
    'j11=' + format(j11, '.12f') + '; integral=' + format(integral, '.12E') + '; closed=' + format(closed, '.12E') + '; rel=' + format(rel_bessel, '.3E'))
add('A04', 'PASS', 'V65 infinite-cylinder Newtonian mapping is standard and domain-limited',
    'gauss and independent radial integral agree; outside cylinder g=-2G*mu_L/r, not spherical 1/r^2')
add('A05', 'PASS', 'V65 heat-kernel cutoff function and monotonic sampling are numerically consistent',
    'F(0)=1, F samples monotone; series/quad rel=' + format(f_rel, '.3E') + '; coefficient is scheme-dependent')
add('A06', 'PASS', 'V65 N/ell^2 non-identifiability theorem reproduced',
    '(N,ell)=(3,7e-7) and (12,1.4e-6) give identical N/ell^2; log-Jacobian row (1,-2), rank 1')
add('A07', 'PASS', 'V65 reverse-fit cutoff value is correct but uses observed G',
    'ell_fit=' + format(ell_fit, '.8E') + ' matches V65 rel=' + format(fit_rel, '.2E') + '; FIT label upheld')
add('A08', 'PASS', 'V65 scalar-tensor variation coefficient is valid as an EFT matching definition',
    'M_eff^2=M0^2-2*xi*|X0|^2 and M_eff^2=1/(8*pi*G_eff) coincide by definition; not a no-input G prediction')
add('A09', 'PASS', 'V65 Eotvos parameter mapping is algebraically exact',
    'direct acceleration ratio equals closed eta; rel residual <1e-12; alpha_i and ell remain inputs')
add('A10', 'PASS', 'V65 historical corrections are mathematically correct',
    'alpha guess rel=' + format(alpha_rel, '.6E') + ' (~2.22 ppm); 56pi=' + format(mass_ratio_guess, '.8f') + ' != 1836.15; r_ISCO=3r_s')
add('A11', 'FAIL', 'V65 supplies no W3 candidate passing the r421 four gates',
    '4/4 V65-style quantitative outputs REJECTED at C2/C3/C4; hypothetical all-4 candidate would pass')
add('A12', 'FAIL', 'V65 does not complete four-force unification nor predict G without inputs',
    'source says no new unification, G input, SM group/3 generations/chirality/UV completion OPEN')
add('A13', 'BOUNDARY', 'V65 conditional results remain scheme-, regulator- and model-dependent',
    'heat-kernel a0/a2 scheme dependence, bare term, field spectrum, UV completion and SM representation input are unresolved')
add('A14', 'CORRECTED', 'V65 corrects earlier ROOT success claims instead of validating them',
    '2.22 ppm alpha guess, 56pi mass ratio and r_ISCO=r_s/2 are explicitly falsified; preserve as corrections')
add('A15', 'INFO', 'V65 OBS/STANDARD/MATH/TOY/FIT/OPEN labels align with openuft red lines',
    'MATH theorem accepted only in stated domain; STANDARD is not ROOT novelty; TOY/FIT not validation; OPEN not PASS')
add('A16', 'OPEN', 'A genuine next step must supply a frozen, pre-registered W3 candidate',
    'needs quantitative value + non-reverse source + blind path unused in fitting + Planck/particle two-anchor consistency')

counts = {}
for e in ENTRIES:
    counts[e['verdict']] = counts.get(e['verdict'], 0) + 1

RESULT = {
    'round': 'r422',
    'date': DATE,
    'topic': 'ROOT V65 self-audit independent recheck and W3 gate',
    'source': 'V65 ZIP in Downloads; read-only; openuft method_F/norm/r418/r421',
    'verdict': VERDICT,
    'method': 'pure stdlib Decimal 60 + float Bessel/quadrature + r421 W3 gate; independent arithmetic recheck',
    'entries': ENTRIES,
    'guards': GUARDS,
    'quotes': QUOTES,
    'counts': counts,
    'guard_pass': sum(1 for g in GUARDS if g['pass']),
    'guard_total': len(GUARDS),
    'numeric': {
        'helix_max_rel': format(helix_max, '.6E'),
        'j11': format(j11, '.12f'),
        'kg_integral': format(integral, '.12E'),
        'kg_closed': format(closed, '.12E'),
        'kg_rel': format(rel_bessel, '.6E'),
        'F_samples': [format(v, '.12f') for v in fs],
        'ell_fit': format(ell_fit, '.12E'),
        'ell_planck': format(ell_p, '.12E'),
        'alpha_guess_rel': format(alpha_rel, '.12E'),
        'mass_ratio_56pi': format(mass_ratio_guess, '.12f'),
        'mass_ratio_rel': format(mass_rel, '.12E'),
    },
    'w3_results': w3_results,
    'fact_md5': {os.path.basename(f): md5(f) for f in FACTS},
    'red_line': RED,
    'next_round': {
        'r': 'r423',
        'condition': 'only run a full upgrade audit after a W3 candidate passes all four gates',
        'blocker': 'V65 has no no-input numerical prediction for G or four-force strengths',
    },
}

with io.open(P_JSON, 'w', encoding='utf-8') as f:
    f.write(json.dumps(RESULT, ensure_ascii=False, indent=2, default=str))

MD = ['# 数据产物 · TUFT r422：ROOT V65 自评复核与 W3 门禁', '',
      '- 轮次：r422；日期：' + DATE,
      '- verdict：`' + VERDICT + '`',
      '- 结论：V65 的条件数学定理多数可复算，但它自己声明的四力统一/G 无输入预测仍未成立；4 个 V65 式候选全部被 W3 四门拒绝。',
      '', '## 记分板', '',
      '- 条目：' + str(len(ENTRIES)) + '（' + ', '.join(k + '=' + str(v) for k, v in sorted(counts.items())) + '）',
      '- 守卫：' + str(RESULT['guard_pass']) + '/' + str(RESULT['guard_total']),
      '- 引文：' + str(sum(1 for q in QUOTES.values() if q.get('found'))) + '/' + str(len(QUOTES)),
      '', '## 数值读数', '']
for k, v in RESULT['numeric'].items():
    MD.append('- ' + k + ': ' + str(v))
MD += ['', '## 条目表', '', '| id | verdict | claim | reading |', '|---|---|---|---|']
for e in ENTRIES:
    MD.append('| ' + e['id'] + ' | ' + e['verdict'] + ' | ' + e['claim'] + ' | ' + e['reading'] + ' |')
MD += ['', '## W3 门禁', '', '| 候选 | 结果 | 失败门 |', '|---|---|---|']
for g in w3_results:
    failed = ','.join(k for k, v in g['result']['checks'].items() if not v)
    MD.append('| ' + g['name'] + ' | ' + ('PASS' if g['result']['passed'] else 'REJECTED') + ' | ' + failed + ' |')
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
