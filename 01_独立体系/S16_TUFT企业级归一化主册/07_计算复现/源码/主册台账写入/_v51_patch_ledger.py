# -*- coding: utf-8 -*-
import io, json, collections

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT企业级归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json'
d = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

assert d['version'] == 'v6.2', d['version']
assert d['latest_round'] == 'v6.2_v50_static_precision', d['latest_round']
assert d['equation_range'] == 'E1-E500', d['equation_range']

d['version'] = 'v6.3'
d['latest_round'] = 'v6.3_v51_twodomain'
d['equation_range'] = 'E1-E501'
d['date'] = '2026-09-25'
d['last_updated'] = '2026-09-25'
# erratum / latest_erratum stay 42; four_state_counts_approx unchanged

v51 = collections.OrderedDict()
v51['round'] = 'v6.3/v51'
v51['organizer_verified'] = True
v51['source_output'] = '_audit_v51_twodomain_out.txt'
v51['method'] = ('Independent two-domain assembly re-implementation (NO import of v50/v49); mpmath dps=55; '
    'Jansen tortoise wave eq psi\'\'+[w^2-V(s)]psi=0, s=b*t (b=3.5+1.5i); '
    'near-wall domain A (cluster-wall map, psi=F1(s) e^{iws} G1, F1=s^beta P(s), P=sum a_k s^{k mu}, mu=2/3, K=16, a16=8.144e-14); '
    'far-field domain B (Lobatto dropping e=+1 infinity node, psi=e^{iws} G2); interface C0 fold G2[0]=F1(s1)*G1[p1-1]; '
    'block row0 wall regularity G1\'(0)+i w G1(0)=0 (Q0=gA*D, Q1=j@[0,0]); rows1..p1-1 domain-A PDE; rows p1.. domain-B PDE + fold coupling column')
v51['geometry'] = {'rho_h': 0.609901951359, 'beta': 1.263762615826, 'B_opt': '3.500+1.500i'}
v51['near_wall_U'] = {'U-2': -1.346e-01, 'U-1': 3.772e-02, 'U0': 3.220e-02, 'U1': 1.354e-02, 'U2': 2.978e-03, 'a16': 8.144e-14}
v51['Q1_interface_singularity_fix'] = {
    'root_cause': 'v50 wrote both C0/C1 as explicit rows; the C1-row Q1 part i(F1G1-G2) IS the C0 condition itself, duplicating the C0 row -> rank-deficient -> all-zero Q1 rows',
    'fix': 'C0 NOT written as a row (shared interface-node elimination fold); interface row is domain-A side PDE residual (carries nonzero Q1=i*2*gA*D); also fixed wall regularity to G\'(0)+i w G(0)=0 (not G\'(0)=0), Q1 diagonal padded W0=2F\'/F',
    'Q1_zero_rows_measured': 0,
    'engineering_grade': 'PASS (v50 singularity solved)'
}
v51['GR_gate_A'] = {'w': '0.373671684418041827-0.088962315688935700i', 'err': 1.605e-15, 'digits': 14.8, 'pass': True, 'note': 'independent Leaver; validates dps=55 two-domain assembly machinery; control anchor'}
v51['GR_gate_B'] = 'NOT DONE - two-domain TUFT side not yet converged; not running GR reproduction with unverified assembly'
v51['TUFT_two_domain_scan'] = [
    {'t1': 0.08, 'p1': 16, 'p2': 24, 'Beyn': '0.450986835512+0.014169990193i', 'GEP': '0.442585774805+0.008146878482i', 'Q1_zero_rows': 0, 'diff': 1.03e-02},
    {'t1': 0.08, 'p1': 24, 'p2': 48, 'Beyn': '0.280020879102-0.089417580740i', 'GEP': '0.438714116605-0.011157963164i', 'Q1_zero_rows': 0, 'diff': 1.77e-01},
    {'t1': 0.08, 'p1': 32, 'p2': 48, 'Beyn': '0.363410814792+0.015912370133i', 'GEP': '0.438714116605-0.011157963164i', 'Q1_zero_rows': 0, 'diff': 8.00e-02},
    {'t1': 0.15, 'p1': 32, 'p2': 48, 'Beyn': '0.431573704644-0.057295238061i', 'da': 2.99e-03, 'GEP': '0.438807281202-0.010986505427i', 'diff': 4.69e-02},
    {'t1': 0.15, 'p1': 40, 'p2': 60, 'Beyn': '0.436621597880-0.051239692541i', 'da': 5.65e-03},
]
v51['anchor'] = '0.434445178-0.056449760i'
v51['best_single_config'] = {'p1': 32, 'p2': 48, 'Beyn': '0.43157-0.05730i', 'da': 3e-3, 'digits': 2.5, 'note': 'GEP drifts to 0.44+0.008i spurious eigenvalue; two routes only ~1 digit mutual; p1=40 non-monotone'}
v51['hard_11p6_gate'] = {'reached': False, 'grade': 'RED', 'authoritative_w0_declared': False, 'mutual_digits': 1, 'note': 'Beyn-vs-GEP diff 1e-2..4e-1, ~1 digit; no clean pole; no new authoritative fundamental declared'}
v51['blockers'] = {
    'main': 'C1 derivative-continuity not written as explicit row; driven by two-side PDE spectral convergence, interface derivative jump decays algebraically; Beyn picks up pseudo-mode clusters drifting with p, not clean poles',
    'secondary': 'domain-B near-infinity cutoff L_t=6 far-field outgoing-wave convergence unverified; GEP often attracted to ~0.44+0.008i spurious eigenvalue',
    'next_step': 'explicit C1 row (Q0-only) replacing domain-A interface PDE row; domain-A wall nodes -> Gauss-Chebyshev interior nodes to remove wall-BC error source; then rescan'
}
v51['rotating_side'] = 'NOT DONE this pass (time consumed by two-domain debugging); splitR/a=1.621367 (v49 double precision) on hold'
v51['four_state_grade'] = 'RED (Q1 singularity fix = engineering PASS, but TUFT physical precision not at 11.6-digit hard gate; GR Leaver gate A = 14.8-digit PASS as control anchor). No fake closure.'
v51['E501'] = 'Robust two-domain unit: Q1 interface singularity solved (engineering PASS, zero rows=0); C1 derivative continuity not explicit row -> two routes only ~1-digit mutual; 11.6-digit hard gate still OPEN. Gate/methodology channel, NOT added to physical four-state.'
v51['erratum'] = '#42 held (no new erratum this round)'

# insert v51 key results right after v50_static_precision_key_results (keep order)
newd = collections.OrderedDict()
for k, val in d.items():
    newd[k] = val
    if k == 'v50_static_precision_key_results':
        newd['v51_twodomain_key_results'] = v51
d = newd

# prepend open_backlog entry
obl = ('v6.3/v51: robust two-domain unit close (E501; organizer-verified; numbers copied verbatim from '
 '_audit_v51_twodomain_out.txt; independent two-domain assembly re-implementation, NO import of v50/v49; mpmath dps=55; '
 'rough starts, no loop calibration; disk backed up to .v63pre_20260925.bak; starting point v6.2/E1-E500/#42; v6.2 E500 static push, '
 'v6.1 E499 Chandrasekhar+mirror, v6.0 third-spectral-diagnosis NOT rolled back). Two-domain derivation: Jansen tortoise '
 'psi\'\'+[w^2-V(s)]psi=0, s=b*t (b=3.5+1.5i); wall domain A cluster-map psi=F1(s)e^{iws}G1, F1=s^beta P(s), P=sum a_k s^{k mu}, '
 'mu=2/3, K=16, a16=8.144e-14; far domain B Lobatto dropping e=+1 infinity node psi=e^{iws}G2; interface C0 fold '
 'G2[0]=F1(s1)*G1[p1-1]; block row0 wall regularity G1\'(0)+iw G1(0)=0 (Q0=gA*D, Q1=j@[0,0]), rows1..p1-1 domain-A PDE, rows p1.. '
 'domain-B PDE + fold coupling column. Q1 interface singularity ROOT-CAUSED and FIXED (engineering PASS): v50 wrote C0/C1 both as '
 'explicit rows, the C1-row Q1 part i(F1G1-G2) IS the C0 condition itself -> duplicated C0 row -> rank-deficient -> all-zero Q1 rows; '
 'fix = C0 not written as row (shared interface-node elimination fold), interface row is domain-A side PDE residual carrying nonzero '
 'Q1=i*2*gA*D; also wall regularity corrected to G\'(0)+iw G(0)=0 (not G\'(0)=0) and Q1 diagonal padded W0=2F\'/F; measured Q1 zero '
 'rows=0 (v50 singularity solved). GR gate A independent Leaver PASS: w=0.373671684418041827-0.088962315688935700i, |err|=1.605e-15 '
 '(14.8 digits) -> dps=55 two-domain assembly machinery correct, control anchor. GR gate B NOT done (two-domain TUFT side not yet '
 'converged). TUFT two-domain Beyn-vs-direct-GEP scan (p1 x p2 x t1): t1=0.08 p1=16 p2=24 Beyn=0.45099+0.01417i GEP=0.44259+0.00815i '
 'diff=1.0e-2; p1=24 p2=48 Beyn=0.2800-0.0894i GEP=0.4387-0.0112i diff=1.8e-1; p1=32 p2=48 Beyn=0.3634+0.0159i GEP=0.4387-0.0112i '
 'diff=8.0e-2; t1=0.15 p1=32 p2=48 Beyn=0.43157-0.05730i GEP=0.43881-0.01099i diff=4.7e-2; p1=40 p2=60 Beyn=0.43662-0.05124i. '
 'Anchor=0.434445178-0.056449760i. Best single config p1=32/p2=48 Beyn=0.43157-0.05730i (|da|=3e-3, 2.5 digits) but GEP drifts to '
 '0.44+0.008i spurious eigenvalue, two routes only ~1 digit mutual, p1=40 non-monotone. 11.6-digit hard gate NOT REACHED (RED); no '
 'new authoritative fundamental declared. Main blocker: C1 derivative-continuity not explicit row (driven by two-side PDE spectral '
 'convergence, interface derivative jump algebraic decay); Beyn picks up p-drifting pseudo-mode clusters, not clean poles. Secondary '
 'blocker: domain-B near-infinity cutoff L_t=6 far-field outgoing convergence unverified; GEP attracted to ~0.44+0.008i spurious '
 'eigenvalue. Next step: explicit C1 row (Q0-only) replacing domain-A interface PDE row; domain-A wall nodes -> Gauss-Chebyshev interior '
 'nodes to remove wall-BC error source; rescan. Rotating side NOT done (time consumed); splitR/a=1.621367 on hold. E501 gate/methodology '
 'channel, NOT added to physical four-state; 35/61/18/27 frozen; erratum #42 held (no new erratum). D18 v31 no rollback; coalition 2/6, '
 'UFT-3 locked. open_backlog: 11.6-digit static hard gate still OPEN (RED; Q1 singularity engineering-fixed but two-domain mutual only '
 '~1 digit); next = explicit C1 row (Q0-only) + Gauss-Chebyshev wall interior nodes. Merge report: TUFT_v51_鲁棒两域合并报告.md.')
d['open_backlog'] = [obl] + d['open_backlog']

# write back utf-8 no BOM
io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2))

# verify reload
d2 = json.load(io.open(p, encoding='utf-8'))
print('json.load OK')
print('version', d2['version'])
print('latest_round', d2['latest_round'])
print('equation_range', d2['equation_range'])
print('latest_erratum', d2['latest_erratum'], 'erratum', d2['erratum'])
print('four_state', d2['four_state_counts_approx']['strict'], d2['four_state_counts_approx']['conditional'], d2['four_state_counts_approx']['definition'], d2['four_state_counts_approx']['open'])
print('has v51 key results', 'v51_twodomain_key_results' in d2)
print('open_backlog len', len(d2['open_backlog']))
print('backlog[0] head', d2['open_backlog'][0][:70])
