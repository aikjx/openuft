# -*- coding: utf-8 -*-
import io, json, collections

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json'
d = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

assert d['version'] == 'v6.3', d['version']
assert d['latest_round'] == 'v6.3_v51_twodomain', d['latest_round']
assert d['equation_range'] == 'E1-E501', d['equation_range']

d['version'] = 'v6.4'
d['latest_round'] = 'v6.4_v52_twodomain_refine'
d['equation_range'] = 'E1-E502'
d['date'] = '2026-09-25'
d['last_updated'] = '2026-09-25'
# erratum / latest_erratum stay 42; four_state_counts_approx unchanged

v52 = collections.OrderedDict()
v52['round'] = 'v6.4/v52'
v52['organizer_verified'] = True
v52['source_output'] = '_audit_v52_twodomain_refine_out.txt'
v52['method'] = ('Independent re-implementation of two-domain three-point refine on top of the v51 two-domain assembly (NO import of v51/v50); '
    'mpmath dps=55; rough starts, no loop calibration; numbers copied verbatim from raw output. '
    'Unknown vector u=[G1(0..p1-1)|G2(1..p2e-1)] (domain-B far-field e=+1 node dropped, so G2 starts at 1); quadratic pencil Q(w)=Q0+w Q1. '
    'row0 wall regularity changed to ChebU interior-node extrapolation (Chebyshev-U interior nodes, not on interpolation nodes): G1\'(sw)+i w G1(sw)=0; '
    'domain-A PDE interior rows; R1 interface C1 row REPLACES the domain-A interface PDE row -- after C0 fold, C1 becomes a w-independent constraint '
    'G1\' - G2\'/F1 + (F1\'/F1) G1 = 0, entering Q0 only with all-zero Q1 rows (hence solved with scipy.linalg.eig(-Q0,Q1) tolerating singular Q1); '
    'domain-B rows fold back C0; far-field e=+1 node dropped.')
v52['GR_gate_A'] = {'w': '0.373671684418041827-0.088962315688935700i', 'err': 1.605e-15, 'digits': 14.79, 'pass': True,
    'note': 'independent Leaver; validates dps=55 high-precision machinery itself; control anchor'}
v52['near_wall_U'] = {'U-2': -1.346e-01, 'U-1': 3.772e-02, 'U0': 3.220e-02, 'U1': 1.354e-02, 'U2': 2.978e-03, 'a16': 8.144e-14}
v52['GR_gate_B'] = {
    'note': 'SAME two-domain assembly on Schwarzschild RW, reproduce n0. DIAGNOSTIC FAIL -- residual located NOT to far-field truncation (Lt 30->40 does not converge), NOT to wall-row sign (c=+/-2 both fail to surface n0); judged = interface C0/C1 matching block + pencil discretization residual. Two-domain assembly itself has NOT yet passed the GR reproduction gate, so TUFT numbers are NOT trustworthy.',
    'rows': [
        {'s1': 2.0, 'p1': 24, 'p2': 36, 'Lt': 30, 'w': '0.31637214736068-0.16308697894661i', 'err': 9.369e-02, 'digits': 1.03},
        {'s1': 2.0, 'p1': 32, 'p2': 48, 'Lt': 40, 'w': '0.31775666320125-0.15964717461469i', 'err': 9.013e-02, 'digits': 1.05},
        {'s1': 3.0, 'p1': 32, 'p2': 48, 'Lt': 40, 'w': '0.31300620388456-0.15778920655484i', 'err': 9.175e-02, 'digits': 1.04},
    ],
    'best_digits': 1.05, 'pass': False, 'verdict': 'FAIL(diag)'
}
v52['TUFT_three_way_scan'] = {
    'setup': 'chebu wall, t1=0.15, p1=32 p2=48 unless noted',
    'R1_C1_on_vs_off': [
        {'C1_on': True, 'Q1_zero_rows': 1, 'Beyn': '0.261828886269+0.028714145583i', 'GEP': '0.421116194982-0.028409396321i', 'diff': 1.69e-01},
        {'C1_on': False, 'Q1_zero_rows': 0, 'Beyn': '0.436003801719-0.055416780367i', 'GEP': '0.438807280908-0.010986505080i', 'diff': 4.45e-02},
    ],
    'R1_key_negative': 'Explicit C1 row CONTRARY to the task hypothesis: C1_on=TRUE pushes Beyn FROM near-anchor 0.436-0.055i TO the wrong pole 0.262+0.029i; the v51-style interface-PDE row (C1_on=FALSE) instead stays near the anchor. Q1 zero rows reappear (Q1zr=1 when C1 on).',
    'R2_wall_node': [
        {'node': 'chebu', 'Beyn': '0.261828886269+0.028714145583i', 'GEP': '0.421116194982-0.028409396321i', 'diff': 1.69e-01},
        {'node': 'lobatto', 'result': 'FAIL (anomalous)'},
    ],
    'R3_far_truncation_Lt_C1on': [
        {'Lt': 4, 'Beyn': '0.258245799724-0.021134518238i', 'GEP': '0.451001034487-0.038999446142i', 'diff': 1.94e-01, 'near_spur': 'NONE'},
        {'Lt': 6, 'Beyn': '0.261828886269+0.028714145583i', 'GEP': '0.421116194982-0.028409396321i', 'diff': 1.69e-01, 'near_spur': 'NONE'},
        {'Lt': 8, 'Beyn': '0.310271444831+0.017538301514i', 'GEP': '0.418060395602-0.025855781764i', 'diff': 1.16e-01, 'near_spur': 'NONE'},
    ],
    'R3_note': 'near-spurious 0.44+0.008i all NONE, but this is NOT a true clearing -- Beyn has already drifted to the wrong pole.',
    'Np_convergence_monotonicity': [
        {'p1': 20, 'Beyn': '0.371652934173+0.020827667530i'},
        {'p1': 28, 'Beyn': '0.225856496180+0.058251207644i'},
        {'p1': 36, 'Beyn': '0.359929941058-0.013523677119i'},
        {'p1': 44, 'Beyn': '0.362922159528-0.097073638050i'},
    ],
    'Np_note': 'NON-monotone wandering (not a convergence sequence).'
}
v52['anchor'] = '0.434445178-0.056449760i'
v52['hard_11p6_gate'] = {'reached': False, 'grade': 'RED', 'authoritative_w0_declared': False,
    'GR_gate_B_digits': 1.05, 'TUFT_best_mutual_digits': 1.35, 'note': 'GR gate B only 1.05 digits; TUFT mutual best ~1.35 digits (C1 off, diff=4.45e-2); N/p non-monotone; no new authoritative fundamental; existing Grade-A anchor 0.434445178-0.056449760i remains highest authority.'}
v52['blockers'] = {
    'first_obstacle': 'Two-domain assembly interface C0/C1 matching block cannot reproduce Schwarzschild n0 to 11.6 digits (err~9e-2 does not decrease with resolution); before this block passes the GR gate, no TUFT high claim holds',
    'secondary_negatives': 'explicit C1 row anti-degradation (C1_on=TRUE pushes Beyn off the anchor); Q1 zero rows reappear (Q1zr=1)',
    'next_suggestion': 'freeze R1 (revert C1_on=FALSE); focus on diagnosing the interface-matching-block Jacobian/fold coefficients and endpoint-extrapolation ill-conditioning; or revert to single-domain Beyn (v50 9 digits) as baseline',
    'rotating_side': 'NOT done this pass; splitR/a=1.621367 still on hold'
}
v52['wall_time_s'] = 1590
v52['four_state_grade'] = 'RED (GR Leaver gate A 14.8-digit PASS as control anchor, but GR gate B only 1.05-digit FAIL; two-domain assembly has not passed the GR reproduction gate, TUFT numbers not trustworthy). No fake closure.'
v52['E502'] = ('Two-domain three-point refine: GR gate B only 1.05-digit FAIL (interface C0/C1 matching block cannot reproduce Schwarzschild n0 to 11.6 digits, err~9e-2 not resolution-decreasing); '
    'explicit C1 row anti-degradation (C1_on=TRUE pushes Beyn from near anchor to wrong pole); Q1 zero rows reappear; interface matching block is the first obstacle; 11.6-digit hard gate still OPEN. '
    'Gate/methodology channel, NOT added to physical four-state.')
v52['erratum'] = '#42 held (no new erratum this round)'

# insert v52 key results right after v51_twodomain_key_results (keep order)
newd = collections.OrderedDict()
for k, val in d.items():
    newd[k] = val
    if k == 'v51_twodomain_key_results':
        newd['v52_twodomain_refine_key_results'] = v52
d = newd

# prepend open_backlog entry
obl = ('v6.4/v52: two-domain three-point refine close (E502; organizer-verified; numbers copied verbatim from '
 '_audit_v52_twodomain_refine_out.txt; independent re-implementation of three-point refine on the v51 two-domain assembly, NO import of v51/v50; mpmath dps=55; '
 'rough starts, no loop calibration; disk backed up to .v64pre_20260925.bak; starting point v6.3/E1-E501/#42; v6.3 E501 robust two-domain unit, v6.2 E500 static push, '
 'v6.1 E499 Chandrasekhar+mirror, v6.0 third-spectral-diagnosis NOT rolled back). Assembly matrix block structure: unknown vector u=[G1(0..p1-1)|G2(1..p2e-1)] '
 '(domain-B far e=+1 node dropped, G2 starts at 1); quadratic pencil Q(w)=Q0+w Q1; row0 wall regularity -> ChebU interior-node extrapolation (not on interpolation nodes) '
 'G1\'(sw)+i w G1(sw)=0; domain-A PDE interior rows; R1 interface C1 row REPLACES domain-A interface PDE row -- after C0 fold, C1 becomes w-independent constraint '
 'G1\' - G2\'/F1 + (F1\'/F1) G1 = 0, entering Q0 only with all-zero Q1 rows (solved with scipy.linalg.eig(-Q0,Q1) tolerating singular Q1); domain-B rows fold back C0; '
 'far e=+1 node dropped. GR gate A independent Leaver PASS: w=0.373671684418041827-0.088962315688935700i, |err|=1.605e-15 (14.8 digits) = dps=55 machinery correct, control anchor. '
 'GR gate B (same two-domain assembly on Schwarzschild RW) DIAGNOSTIC FAIL: s1=2.0 p1=24 p2=36 Lt=30 w=0.31637214736068-0.16308697894661i |err|=9.369e-02 (1.03 digits); '
 's1=2.0 p1=32 p2=48 Lt=40 w=0.31775666320125-0.15964717461469i |err|=9.013e-02 (1.05 digits); s1=3.0 p1=32 p2=48 Lt=40 w=0.31300620388456-0.15778920655484i |err|=9.175e-02 (1.04 digits); '
 'best 1.05 digits FAIL. Residual located NOT to far-field truncation (Lt 30->40 not converging) NOT to wall-row sign (c=+/-2 both fail to surface n0); judged = interface C0/C1 matching block + pencil residual; '
 'two-domain assembly itself has NOT passed the GR reproduction gate -> TUFT numbers NOT trustworthy. TUFT three-way scan (chebu wall, t1=0.15): R1 C1_on=TRUE p1=32 p2=48 Q1zr=1 '
 'Beyn=0.261828886+0.028714146i GEP=0.421116195-0.028409396i diff=1.69e-1; C1_on=FALSE (v51-style interface PDE row) Q1zr=0 Beyn=0.436003802-0.055416780i GEP=0.438807281-0.010986505i diff=4.45e-2. '
 'KEY NEGATIVE: explicit C1 row CONTRARY to the task hypothesis -- C1_on=TRUE pushes Beyn from near-anchor 0.436-0.055i TO the wrong pole 0.262+0.029i; the v51-style interface PDE row instead stays near the anchor; Q1 zero rows reappear (Q1zr=1). '
 'R2 node=chebu same (diff 1.69e-1), node=lobatto FAIL (anomalous). R3 Lt=4/6/8 (chebu, C1 on): Beyn=0.258245800-0.021134518i / 0.261828886+0.028714146i / 0.310271445+0.017538302i; '
 'GEP=0.451001034-0.038999446i / 0.421116195-0.028409396i / 0.418060396-0.025855782i; diff=1.94e-1/1.69e-1/1.16e-1; near-spur 0.44+0.008i all NONE (but Beyn already drifted to wrong pole, not a true clearing). '
 'N/p monotonicity (chebu, C1 on, Lt=6): p1=20->0.371652934+0.020827668i, p1=28->0.225856496+0.058251208i, p1=36->0.359929941-0.013523677i, p1=44->0.362922160-0.097073638i -- NON-monotone wandering. '
 '11.6-digit hard gate NOT REACHED (RED); no new authoritative fundamental; existing Grade-A anchor 0.434445178-0.056449760i remains highest authority. First obstacle = two-domain assembly interface C0/C1 matching block cannot reproduce Schwarzschild n0 to 11.6 digits (err~9e-2 not resolution-decreasing); before this block passes the GR gate no TUFT high claim holds. '
 'Next suggestion: freeze R1 (revert C1_on=FALSE), diagnose interface-matching-block Jacobian/fold coefficients and endpoint-extrapolation ill-conditioning, or revert to single-domain Beyn (v50 9 digits) as baseline. '
 'Rotating side NOT done; splitR/a=1.621367 on hold. E502 gate/methodology channel, NOT added to physical four-state; 35/61/18/27 frozen; erratum #42 held (no new erratum). '
 'D18 v31 no rollback; coalition 2/6, UFT-3 locked. open_backlog: 11.6-digit static hard gate still OPEN (RED; two-domain assembly not past GR gate B 1.05 digits, TUFT numbers not trustworthy); '
 'next = freeze R1 revert C1_on=FALSE, diagnose interface matching block Jacobian/fold coeffs + endpoint extrapolation ill-conditioning, or revert to single-domain Beyn (v50 9 digits) baseline. '
 'Merge report: TUFT_v52_两域精修合并报告.md.')
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
print('has v52 key results', 'v52_twodomain_refine_key_results' in d2)
print('open_backlog len', len(d2['open_backlog']))
print('backlog[0] head', d2['open_backlog'][0][:70])
