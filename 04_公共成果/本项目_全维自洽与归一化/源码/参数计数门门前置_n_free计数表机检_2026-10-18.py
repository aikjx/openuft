# -*- coding: utf-8 -*-
"""Parameter-count pre-gate (总账 §七.2): n_free <= n_obs - 1, machine-derived.

Dossier currency:
  n_free  = DISTINCT declared knob names, minus UNIVERSAL-SUBSTITUTED ones
            (derived_from a measured constant, e.g. kappa_4 := 8*pi*G) and minus
            optional terms; n_free_opt adds the optional terms back.
  n_obs   = DISTINCT registered observational targets, each cited file:line.
  verdict = PASS iff n_free <= n_obs - 1 (gate formula cited verbatim from
            三重预检 L282 "n_观测量 >= n_自由参数+1" and V48 B9 L112
            "违反 n_自由 <= n_观测−1"). n_obs==0 => FAIL with no_obs=True.

Every knob/obs row carries (file, line, token); the engine re-reads the cited
line and asserts the token is present (citation integrity). Found only within
+/-3 lines => SHIFT (warn); absent everywhere => STALE (fatal, exit 1).

Controls (总账 §七.3 -- a gate without controls cannot tell "effective" from
"always-FAIL"):
  C1 dedup: a duplicated knob name must not inflate n_free;
  C2 mutant: injecting 4 fresh distinct knobs into the PASS case flips it FAIL;
  C3 stale-citation detector fires on a synthetic bad line ref;
  C4 cross-channel: CTFA engine counts == that JSON's own self-reports, live;
  C5 budget-difference: structural count of 49A exceeds the file's recorded
     "+7"/"+9" by EXACTLY 1 in both calibers -- the difference is fully
     explained by (+m, +y declared at md L143/L148 but missing from the
     file's own budget table) minus (kappa_4 universal-substituted here);
  C6 positive control: the V9.46 N_p=0 case must PASS (known-pass in-repo).
Exit != 0 on any STALE, anchor mismatch, or control failure.
"""
import json, os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     os.pardir, os.pardir, os.pardir, os.pardir))

A49 = 'openuft/07_统一场方程/49A_阶段1任务1_EC总拉氏量与量纲逐词审计_2026-10-15.md'
A49PY = 'openuft/07_统一场方程/49A_ec_lagrangian_calc.py'
SAN = 'openuft/07_统一场方程/openuft_49_阶段1_三重预检攻破卷_2026-10-15.md'
V48 = 'openuft/07_统一场方程/空间螺旋几何化统一场论/65_TUFT-V4.8公式集_作用量量纲与场方程结构机器审计_2026-10-15.md'
CTF = 'openuft/04_公共成果/算法联盟_全维自洽与归一化/数据/张祥前CTFA_自由度预算与统一能力上限_2026-10-12.json'
V946 = 'openuft/01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/V9_四力大统一定稿线/01_全书_四力大统一_垂直原理螺旋统一场论_V9.46.md'

_cache = {}
def lines_of(rel):
    if rel not in _cache:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        with open(p, encoding='utf-8', errors='replace') as f:
            _cache[rel] = f.read().splitlines()
    return _cache[rel]

def check_cite(rel, line, token, findings):
    ls = lines_of(rel)
    if not (0 < line <= len(ls)):
        findings.append(('STALE', rel, line, token, 'file has %d lines' % len(ls)))
        return False
    if token in ls[line - 1]:
        return True
    for d in range(1, 4):
        for n in (line - d, line + d):
            if 0 < n <= len(ls) and token in ls[n - 1]:
                findings.append(('SHIFT', rel, line, token, 'found at %d' % n))
                return True
    findings.append(('STALE', rel, line, token, 'token absent within +-3'))
    return False

def row(name, rel, line, token, **kw):
    r = {'name': name, 'file': rel, 'line': line, 'token': token}
    r.update(kw)
    return r

BS = chr(92)  # backslash spelled via chr so token literals stay unambiguous

# token literals below were verified verbatim against the cited line contents.
DOSSIER = [
  {'id': 'E1_49A_EC总拉氏量',
   'knobs': [
     row('beta_1', A49, 104, 'beta_1'), row('beta_2', A49, 104, 'beta_2'),
     row('beta_3', A49, 104, 'beta_3'),
     row('gamma', A49, 105, BS + 'gamma', optional=True),
     row('zeta', A49, 120, BS + 'zeta', optional=True),
     row('m_Omega', A49, 121, 'm_' + BS + 'Omega'),
     row('lambda', A49, 121, BS + 'lambda'),
     row('xi', A49, 131, BS + 'xi(x)'),
     row('m', A49, 143, '- m' + BS + 'bar' + BS + 'psi' + BS + 'psi'),
     row('y', A49, 148, '-y' + BS + ','),
     row('kappa_4', A49, 90, '8' + BS + 'pi G', derived_from='G')],
   'obs': [
     row('PPN_gamma_Cassini', A49, 430, 'Cassini'),
     row('Nordtvedt_eta', A49PY, 977, 'eta_nordtvedt'),
     row('弱场还原GR牛顿', A49, 430, 'GR'),
     row('EDM上限', A49, 428, 'EDM')],
   'expect': {'n_free': 8, 'n_free_opt': 10, 'verdict': 'FAIL'}},
  {'id': 'E2_三重预检',
   'knobs': [
     row('耦合强度', SAN, 282, '耦合强度'), row('CP相位', SAN, 282, 'CP'),
     row('lambda_有量纲', SAN, 148, '$' + BS + 'lambda$')],
   'obs': [
     row('PPN_gamma', SAN, 91, 'PPN'), row('Nordtvedt_eta', SAN, 92, 'Nordtvedt'),
     row('第五力等效原理', SAN, 93, '第五力'), row('omega_BD', SAN, 99, '4.35'),
     row('g-2', SAN, 170, '10^{-47}'), row('EDM', SAN, 177, 'EDM'),
     row('F_P', SAN, 265, 'F_P')],
   'expect': {'n_free': 3, 'verdict': 'PASS'}},
  {'id': 'E3_V48公式集',
   'knobs': [
     row('lambda_1', V48, 37, 'λ₁'), row('lambda_2', V48, 37, 'λ₂'),
     row('lambda_3', V48, 37, 'λ₃'), row('ell_D2', V48, 145, 'ℓ')],
   'obs': [],
   'expect': {'n_free': 4, 'verdict': 'FAIL'}},
  {'id': 'E4_CTFA层',
   'knobs': [row('kappa', CTF, None, None), row('tau', CTF, None, None)],
   'obs': [],
   'expect': {'n_free': 2, 'verdict': 'FAIL'}},
  {'id': 'E5_V946_正面控制',
   'knobs': [],
   'obs': [
     row('FE_FG比', V946, 3079, '1.2356'),
     row('8粒子质量表', V946, 3211, 'm (MeV)'),
     row('g因子', V946, 3207, '2.002319')],
   'expect': {'n_free': 0, 'verdict': 'PASS'}},
]

def count(entry, extra_knobs=(), dup_knobs=()):
    base = [k for k in entry['knobs'] if 'derived_from' not in k]
    names = [k['name'] for k in base if not k.get('optional')]
    names += list(extra_knobs) + list(dup_knobs)
    n_free = len(set(names))
    opt = len(set(k['name'] for k in base if k.get('optional')))
    n_obs = len(set(o['name'] for o in entry['obs']))
    verdict = 'PASS' if (n_obs > 0 and n_free <= n_obs - 1) else 'FAIL'
    return n_free, n_free + opt, n_obs, verdict, (n_obs == 0)

findings = []
def verify_cites(entry):
    for k in entry['knobs'] + entry['obs']:
        if k['line'] is not None:
            check_cite(k['file'], k['line'], k['token'], findings)

results = {}
for e in DOSSIER:
    verify_cites(e)
    nf, nfo, no, vd, noobs = count(e)
    results[e['id']] = {'n_free': nf, 'n_free_opt': nfo, 'n_obs': no,
                        'verdict': vd, 'no_obs': noobs}
    exp = e['expect']
    ok = nf == exp['n_free'] and vd == exp['verdict'] and \
         ('n_free_opt' not in exp or nfo == exp['n_free_opt'])
    results[e['id']]['anchor'] = 'PASS' if ok else 'FAIL'
    print('%-22s n_free=%d(+opt=%d) n_obs=%-2d verdict=%-5s no_obs=%-5s anchor=%s' %
          (e['id'], nf, nfo, no, vd, noobs, results[e['id']]['anchor']))

ctrl = {}
e4 = DOSSIER[3]
ctrl['C1_dedup'] = count(e4, dup_knobs=('kappa',))[0] == 2
e5 = DOSSIER[4]
ctrl['C2_mutant_flips_pass_to_FAIL'] = (count(e5, extra_knobs=('m1', 'm2', 'm3', 'm4'))[3] == 'FAIL')
f3 = []
check_cite(V946, 999999, 'zzz', f3)
ctrl['C3_stale_fires'] = any(x[0] == 'STALE' for x in f3)
with open(os.path.join(ROOT, CTF.replace('/', os.sep)), encoding='utf-8') as f:
    cj = json.load(f)
jf = cj['dof_counting']['readings']['reading1']['n_free']
jp = cj['dof_counting']['readings']['reading1']['n_predictions']
ctrl['C4_cross_channel'] = (jf == results['E4_CTFA层']['n_free'] == 2 and
                            jp == results['E4_CTFA层']['n_obs'] == 0)
# C5: structural vs recorded budget (+7 on L357, +9 on L358): difference is
# exactly +1 in both calibers = (+m, +y) - (kappa_4 substituted away).
check_cite(A49, 357, '+7', findings)
check_cite(A49, 358, '+9', findings)
r1 = results['E1_49A_EC总拉氏量']
ctrl['C5_budget_diff_exactly_one'] = (r1['n_free'] - 7 == 1 and r1['n_free_opt'] - 9 == 1)
ctrl['C6_positive_control'] = results['E5_V946_正面控制']['verdict'] == 'PASS'
for k, v in sorted(ctrl.items()):
    print('%-32s %s' % (k, 'PASS' if v else 'FAIL'))

stale = [x for x in findings if x[0] == 'STALE']
shift = [x for x in findings if x[0] == 'SHIFT']
anchor_fails = [k for k, r in results.items() if r['anchor'] != 'PASS']
for x in shift:
    print('CITE-SHIFT %s L%d token=%r %s' % (x[1], x[2], x[3], x[4]))
for x in stale:
    print('CITE-STALE %s L%d token=%r %s' % (x[1], x[2], x[3], x[4]))

out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   os.pardir, '数据',
                                   '参数计数门门前置_n_free计数表机检_2026-10-18.json'))
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'gate_formula': 'n_free <= n_obs - 1 (三重预检 L282 / V48 B9 L112)',
               'dossier': [{k: v for k, v in e.items() if k != 'expect'} for e in DOSSIER],
               'results': results, 'controls': ctrl,
               'cite_findings': {'stale': stale, 'shift': shift}},
              f, ensure_ascii=False, indent=1)
all_ok = (not stale and not anchor_fails and all(ctrl.values()))
print('wrote %s stale=%d shift=%d anchor_fails=%d controls_all_pass=%s rc=%d' %
      (out, len(stale), len(shift), len(anchor_fails), all(ctrl.values()),
       0 if all_ok else 1))
sys.exit(0 if all_ok else 1)
