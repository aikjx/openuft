# -*- coding: utf-8 -*-
import io, json, collections

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT企业级归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json'
d = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

assert d['version'] == 'v6.4', d['version']
assert d['latest_round'] == 'v6.4_v52_twodomain_refine', d['latest_round']
assert d['equation_range'] == 'E1-E502', d['equation_range']

d['version'] = 'v6.5'
d['latest_round'] = 'v6.5_v53_amplitude_anchor'
d['equation_range'] = 'E1-E503'
d['date'] = '2026-09-25'
d['last_updated'] = '2026-09-25'
# erratum / latest_erratum stay 42; four_state_counts_approx unchanged

v53 = collections.OrderedDict()
v53['round'] = 'v6.5/v53'
v53['organizer_verified'] = True
v53['source_output'] = '_audit_v53_amplitude_anchor_out.txt'
v53['method'] = ('Independent re-implementation, no import of any prior-project script; GR gate first; no fake closure; '
    'mpmath dps=40; numbers copied verbatim from raw output. Absolute-amplitude-anchor audit channel (does NOT close a new physical E-number; '
    'E503 is a numerical-investigation/boundary-channel registration, NOT added to physical four-state).')
v53['ssot_anchors_verbatim'] = collections.OrderedDict([
    ('GR_n0', '(0.37367168441804166-0.0889623156889341j)'),
    ('TUFT_GradeA_w', '(0.434445178-0.05644976j)'),
    ('rho_h_R_Vmax_L', '0.609902 / 3.268 / 0.148709 / 6.9698'),
    ('|R_B|^2_gate', 0.530254),
    ('|T_B|^2', 0.220661304516),
    ('eps_toy', 0.469746),
])
v53['RW_barrier_peak_recompute'] = collections.OrderedDict([
    ('l', 2), ('M', 1), ('dps', 40),
    ('Vmax_indep', 0.151287), ('r_at_Vmax', 3.2808),
    ('SSOT_Vmax', 0.148709), ('SSOT_R', 3.268),
    ('verdict', 'PASS (consistent)'),
    ('honest_note', 'GR gate |R_B|^2 precision needs E476 WKB exiting-wave decomp, NOT repeated here; 0.530254 inherited from SSOT v31/v32 (9.1e-8), no fake closure.'),
])
v53['frequency_regime'] = [
    {'freq': 'GR w=0.373672', 'w2': 0.139631, 'Vmax': 0.148709, 'regime': 'tunneling (w^2<Vmax)'},
    {'freq': 'TUFT w=0.434445', 'w2': 0.188743, 'Vmax': 0.148709, 'regime': 'above barrier crest (w^2>Vmax), more transparent'},
]
v53['epsilon_derivation_chain'] = collections.OrderedDict([
    ('toy_E489_upper', 'wall=ideal mirror |r_wall|=1, barrier=lossless step, crest full flux; one-pass |t_B|=sqrt(1-|R_B|^2); two-pass field amp=|t_B|^2=1-|R_B|^2; physics=incoming transmit in |t_B| -> wall reflect |r_wall|=1 -> re-transmit out |t_B|; out-cavity echo amp=|t_B|^2|r_wall|=1-|R_B|^2=0.4697 (E431/E489 upper)'),
    ('strict_two_pass', '(a) one-pass power |t_B|^2=1-|R_B|^2=0.469746, two-pass |T_B|^2=(1-R)^2=0.220661; (b) wall-reflection kernel R=b/a: TUFT wall |r_wall|^2=1 (D25/E488, Gamma=0 machine precision), near-wall s^beta Frobenius bounded support beta=1.263763, reflection phase=cavity resonance round-trip; (c) crest effective flux: GR freq tunneling |R_B|^2=0.530, TUFT freq above crest more transparent; barrier two-pass field amp eps_barrier=1-|R_B|^2=0.469746 (same order as toy)'),
])
v53['six_point_28_source'] = collections.OrderedDict([
    ('toy_loudness_L', 11.993), ('toy_loudness_ref', 'E431 upper, |R_B|=0.729 reflection amplitude used as echo amplitude'),
    ('strict_realPSD_anchor', 1.91), ('strict_ref', 'E444 two-pass barrier + real PSD'),
    ('ratio', 6.2791),
    ('key_conclusion', 'Barrier transmission physics itself does NOT cause 6.28x (TUFT freq above barrier crest, more transparent); the 6.28x residual = source excitation energy absolute scale (e/f_pi next-layer term, OPEN).'),
])
v53['epsilon_strict_interval'] = collections.OrderedDict([
    ('eps_hi', 0.469746),
    ('eps_lo', 0.07481154506795630784624364212457266738931),
    ('eps_lo_ref', '= eps_toy/6.28 (E444 real-PSD anchor)'),
    ('barrier_indep_recompute', 0.469746),
    ('narrowest_interval', '[0.07481154506795630784624364212457266738931, 0.469746]'),
    ('grade', 'ESTIMATED/OPEN (next-layer uncertainty: source excitation e/f_pi not closed; this round only narrows, does not close)'),
])
v53['D_max_two_tier'] = collections.OrderedDict([
    ('setup', '60 Msun, rho_dev=1 detection threshold, Gpc'),
    ('calibration', 'L_O4=11.993, L_Voy=52.1371689 (x4.3473), sqrt(1-ov^2)=0.6319612329882268972975604929652052023706, antenna face-on=1.0000 / edge-on=sqrt(1/8)=0.3536; D_max proportional to epsilon, so strict=toy/6.28'),
    ('rows', [
        {'detector': 'O4', 'orient': 'face-on', 'D_toy_Gpc': 3.5603, 'D_strict_Gpc': 0.5670},
        {'detector': 'O4', 'orient': 'edge-on', 'D_toy_Gpc': 1.2587, 'D_strict_Gpc': 0.2005},
        {'detector': 'Voyager', 'orient': 'face-on', 'D_toy_Gpc': 15.4775, 'D_strict_Gpc': 2.4649},
        {'detector': 'Voyager', 'orient': 'edge-on', 'D_toy_Gpc': 5.4721, 'D_strict_Gpc': 0.8715},
    ]),
    ('v47_toy_crosscheck', 'O4 face-on=3.5603 (v47 3.560), Voy face-on=15.4775 (v47 15.48) -- bitwise match'),
    ('voyager_measurable_range_Gpc', '2.46-15.48 (strict->toy)'),
])
v53['GR_limit'] = collections.OrderedDict([
    ('eps_to_0', 'rho_frac=eps*sqrt(1-ov^2) -> 0 => TUFT-deviation channel D_max -> 0 (no measurable distortion)'),
    ('prompt_GR_ringdown_retained', 'L=11.993, pure GR QNM'),
    ('eps_0_Dmax_O4_faceon', 0.0),
    ('verdict', 'PASS (degenerate pure GR)'),
])
v53['four_state_grade'] = [
    'GR gate |R_B|^2@0.3737=0.530254 (SSOT v31/v32, 9.1e-8): inherited, no fake closure',
    'barrier peak Vmax independent recompute=0.151287@r=3.2808 (SSOT 0.148709@3.268): PASS',
    '|T_B|^2=0.2207 / eps_toy=0.4697: CONFIRMED',
    'eps_strict interval [0.0748115, 0.469746]: ESTIMATED/OPEN (next-layer uncertainty: source excitation e/f_pi not closed; this round only narrows; 6.28x residual=next-layer term)',
    'single-dominant-mode approximation explicit (E477 only n=1, no M-chi degeneracy/overtone/multi-event/network orthogonality)',
]
v53['E503'] = ('Absolute amplitude anchor: epsilon narrowed from single point 0.4697 to interval [0.0748, 0.4697], corresponding Voyager measurable distance 2.46-15.48 Gpc; '
    '6.28x uncertainty located to source excitation energy e/f_pi next-layer term (OPEN); barrier-transmission physics CONFIRMED '
    '(|T_B|^2=0.2207 / eps_toy=0.4697; RW l=2 barrier peak 0.151287@3.2808 independent recompute consistent with SSOT 0.148709@3.268). '
    'Numerical-investigation/boundary-channel registration, NOT added to physical four-state.')
v53['erratum'] = '#42 held (no new erratum this round; absolute-amplitude-anchor audit channel, does not close a new physical E-number)'

# insert v53 key results right after v52_twodomain_refine_key_results
newd = collections.OrderedDict()
for k, val in d.items():
    newd[k] = val
    if k == 'v52_twodomain_refine_key_results':
        newd['v53_amplitude_anchor_key_results'] = v53
d = newd

# prepend open_backlog entry
obl = ('v6.5/v53: absolute amplitude anchor close (E503; organizer-verified; numbers copied verbatim from '
 '_audit_v53_amplitude_anchor_out.txt; independent re-implementation, no import of any prior-project script; GR gate first; no fake closure; '
 'mpmath dps=40; disk backed up to .v65pre_20260925.bak; starting point v6.4/E1-E502/#42; v6.4 E502 two-domain refine, v6.3 E501 robust two-domain unit, '
 'v6.2 E500 static push, v6.1 E499 Chandrasekhar+mirror, v6.0 third-spectral-diagnosis NOT rolled back). epsilon derivation chain: eps=sqrt|T_B|^2=1-|R_B|^2; '
 '|R_B|^2=0.530254 inherited from SSOT v31/v32 (9.1e-8 gate anchor); GR freq w^2=0.1396<Vmax=0.1487 tunneling, TUFT freq w^2=0.1887>Vmax above crest more transparent; '
 'independent RW l=2 barrier peak Vmax=0.151287@r=3.2808 (Schwarzschild analytic) consistent with SSOT TUFT outer barrier 0.148709@3.268 PASS. '
 'two-pass power |T_B|^2=(1-0.530254)^2=0.2207, eps_toy=0.4697 CONFIRMED. '
 '6.28x source: toy prompt loudness L=11.993 (E431 upper) / E444 strict real-PSD anchor 1.91 = 6.28; barrier transmission physics itself does NOT cause 6.28x '
 '(TUFT freq above crest more transparent); 6.28x residual = source excitation energy absolute scale e/f_pi next-layer term (OPEN). '
 'eps_strict interval (mpmath dps=40): hi=0.469746 (toy/E431 upper), lo=0.07481154506795630784624364212457266738931 (=eps_toy/6.28 E444 real-PSD anchor), '
 'barrier independent recompute=0.469746 (same order as toy, does not explain 6.28x); narrowest interval [0.0748, 0.4697] ESTIMATED/OPEN (next-layer uncertainty, not closed this round). '
 'D_max two-tier (60 Msun, rho_dev=1 threshold, Gpc): O4 face-on toy=3.5603/strict=0.5670; O4 edge-on 1.2587/0.2005; Voyager face-on 15.4775/2.4649; Voyager edge-on 5.4721/0.8715. '
 'calibration L_O4=11.993, L_Voy=52.1371689 (x4.3473), sqrt(1-ov^2)=0.63196123, antenna edge-on=sqrt(1/8)=0.3536; D_max proportional to epsilon so strict=toy/6.28; '
 'toy tier bitwise matches v47 anchor (3.5603 vs 3.560; 15.4775 vs 15.48); Voyager measurable range 2.46-15.48 Gpc. '
 'GR limit: eps->0 => rho_frac->0 => TUFT-deviation channel D_max->0; prompt GR ringdown retained L=11.993 pure GR QNM; eps=0 => D_max(O4 face-on)=0.0 Gpc, PASS. '
 'Four-state grading: GR gate |R_B|^2@0.3737=0.530254 inherited no fake closure; Vmax independent recompute PASS; |T_B|^2=0.2207/eps_toy=0.4697 CONFIRMED; '
 'eps_strict interval ESTIMATED/OPEN (source excitation e/f_pi not closed, narrow only); single dominant mode explicit (E477 only n=1). '
 'E503 numerical-investigation/boundary-channel, NOT added to physical four-state; 35/61/18/27 frozen; erratum #42 held (no new erratum). '
 'D18 v31 UPGRADE no rollback; coalition 2/6, UFT-3 locked. open_backlog: source excitation energy absolute scale still OPEN (e/f_pi next-layer term, 6.28x residual not closed); '
 'next = close source excitation e/f_pi next-layer term (absolute amplitude anchor lower bound); barrier-transmission physics already CONFIRMED, no re-check needed. '
 'Merge report: TUFT_v53_绝对振幅锚合并报告.md.')
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
print('has v53 key results', 'v53_amplitude_anchor_key_results' in d2)
print('open_backlog len', len(d2['open_backlog']))
print('backlog[0] head', d2['open_backlog'][0][:70])
