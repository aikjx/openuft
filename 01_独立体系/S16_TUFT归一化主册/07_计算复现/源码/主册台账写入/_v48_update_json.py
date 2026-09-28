# -*- coding: utf-8 -*-
"""v48 收口：台账 JSON 升版 v5.7->v5.8。"""
import json, collections

p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json'
d = json.load(open(p, encoding='utf-8'))

# 1) 顶层字段
assert d['version'] == 'v5.7'
assert d['latest_round'] == 'v5.7_v47_a4_snr_psd_actuarial'
assert d['equation_range'] == 'E1-E497'
assert d['latest_erratum'] == 42
d['version'] = 'v5.8'
d['latest_round'] = 'v5.8_v48_rotating_qnm_beyn'
d['equation_range'] = 'E1-E498'
# latest_erratum 保持 42（本轮无新勘误）

# 2) 四态 note 追加 v5.8
fs = d['four_state_counts_approx']
assert fs['strict'] == 35 and fs['conditional'] == 61 and fs['definition'] == 18 and fs['open'] == 27
fs['note'] += (' v5.8/v48 round: E498 (rotating QNM Beyn extension - Beyn contour machine generalized to small rotation a; '
               'Lense-Thirring local frame-dragging Omega_F=2a/r^3 folded as O(a omega) local diagonal potential -4am omega/r^3; '
               'GR gate A PASS n0@a=0 |err|=2.470e-13 ~12 digits / N=40/60/90 spread=3.45e-11; '
               'GR gate B FAIL Rayleigh split/a=0.096236 vs target 0.2515323 (real part only 38%) + continuation max|Im drift|@a=0.02=1.538e-2 > 5e-3 threshold; '
               'root cause = missing Teukolsky O(a) imaginary cross-term 4i(r-1)K/Delta requiring full Chandrasekhar transform into Jansen-compactified pencil, NOT faked to 4 digits; '
               'TUFT side diagnostic-only (gate B not passed, no physical reading): static re-anchor 0.434445174-0.056449760i vs Grade A |d|=4.5e-9; '
               'rotating raw UNTRUSTED split/a@a=0.10=0.10448 / @a=0.20=-0.34306 sign flip; vs v44 first-order 0.09832 the a=0.10 ~6% match is coincidence under unstable operator; '
               'condition wall sigma_min(L)=7.7e-12, trusted a<0.10 upper bound; root cause = O(a) operator not completed, NOT Beyn contour failure; '
               'boundary-spectral methodology extension, NOT a new physical E-number) is a gate/methodological channel, NOT added to physical four-state; '
               '35/61/18/27 remain frozen; erratum #42 held (no new erratum).')

# 3) last_updated 前置 v48 叙事
v48_lu = ('2026-09-24 v5.8 / E1-E498 / erratum #42 (no new erratum this round). v48 rotating QNM Beyn-extension round E498: '
          'Beyn contour machine generalized to small rotation a; numbers copied verbatim from _audit_v48_rotating_qnm_out.txt '
          '(organizer-verified; script _audit_v48_rotating_qnm.py; double precision; NO prior-project import; NO qnm import at runtime; '
          'disk backed up to .v58pre.bak before replay; starting point v5.7/E1-E497/#42). Derivation chain: Kerr -> Lense-Thirring local drag '
          'Omega_F(r)=2a/r^3; K=(r^2+a^2)omega-am gives local frequency omega-m Omega_F; tortoise wave eq X\'\'+[omega^2-V-2m omega Omega_F]X=0 '
          '= X\'\'+[omega^2-V-4am omega/r^3]X=0, O(a omega) correction = local diagonal potential -4am omega/r^3; '
          'GR Jansen compactified quadratic pencil Q1<-Q1+diag(-4am/r^3), companion (M-omega Lm) linearized Beyn rank-1; '
          'TUFT near-wall linear pencil Q0<-Q0+i.m.diag(Omega_F)(2gD+C10), pencil stays linear, Beyn directly bypasses e^{+/-2/rho} essential-singularity wall. '
          'GR gate A PASS: n0@a=0=0.373671684418-0.088962315689i, |err|=2.470e-13 (~12 digits, require >=6), N=40/60/90 spread=3.45e-11. '
          'GR gate B FAIL: Rayleigh split/a=0.096236 (target 0.2515323, real part only 38%); continuation max|Im drift|@a=0.02=1.538e-2 (>5e-3 threshold). '
          'Diagnosis: bare-diagonal drag embedding reproduces real-part SIGN but not >=4-digit slope; direct pole jumps under O(a); '
          'missing Teukolsky O(a) imaginary cross-term 4i(r-1)K/Delta - requires full Chandrasekhar transform into Jansen-compactified pencil; not faked to 4 digits. '
          'TUFT side (gate B not passed -> diagnostic only, no physical reading): static re-anchor 0.434445174-0.056449760i vs Grade A |d|=4.5e-9; '
          'rotating raw UNTRUSTED: a=0.10 m+2=0.376860600-0.097073912i / m-2=0.366412304-0.141592932i / split/a=0.10448; '
          'a=0.20 m+2=0.345849701-0.107141431i / m-2=0.414460918-0.139554078i / split/a=-0.34306; '
          'vs v44 first-order 0.09832: a=0.10 ~6% close but a=0.20 sign flips to -0.343, drift(0.1->0.2)=0.448 = non-physical; '
          'a=0.10 match is coincidence under unstable operator, not a valid TUFT m-split prediction. '
          'Blocker (condition wall): min sigma_min(L)=7.7e-12; m=-2 two-path S1/S0=1.5e-4/3.1e-5 (degeneracy >1e-8); '
          'trusted rotating mixed-BVP pole a<0.10 under this embedding; residual divergence = pole jump + S1/S0 degeneracy + split/a non-sign-stable; '
          'root cause = O(a) operator not completed (missing imaginary Teukolsky cross-term), NOT Beyn contour failure (gate A reaches 12 digits on same machine). '
          'Next step: complete full Teukolsky-Chandrasekhar O(a) embed then re-pass GR gate B, then switch TUFT reflecting wall to report m-split. '
          'Four-state: GR gate A PASS / gate B FAIL -> TUFT rotating poles NOT declared; boundary-spectral methodology extension, no new physical E-number, no new erratum (#42 held); '
          'E498 not counted in physical four-state; 35/61/18/27 frozen. D18 v31 UPGRADE no rollback; alliance layer 2/6, UFT-3 locked. '
          'Previous: '
)
d['last_updated'] = v48_lu + d['last_updated']

# 4) v48 key_results（镜像 v47 模板字段）
d['v48_rotating_qnm_key_results'] = {
    'version': 'v5.8',
    'latest_round': 'v5.8_v48_rotating_qnm_beyn',
    'equation_range': 'E1-E498',
    'erratum': '#42 held (no new erratum this round)',
    'source_files': [
        'organizer-verified v48 rotating QNM Beyn-extension results; numbers copied verbatim from _audit_v48_rotating_qnm_out.txt '
        '(script _audit_v48_rotating_qnm.py; double precision; NO prior-project import; NO qnm import at runtime; '
        'disk backed up to .v58pre.bak before replay; starting point v5.7/E1-E497/#42)'],
    'four_state_frozen': '35/61/18/27',
    'derivation_chain': {
        'frame_drag': 'Kerr -> Lense-Thirring local Omega_F(r)=2a/r^3',
        'conserved_K': 'K=(r^2+a^2)omega-am gives local frequency omega-m Omega_F',
        'tortoise_wave_eq': "X''+[omega^2-V-2m omega Omega_F]X=0 = X''+[omega^2-V-4am omega/r^3]X=0",
        'O(a omega)_correction': 'local diagonal potential -4am omega/r^3',
        'GR_pencil': 'Jansen compactified quadratic Q1<-Q1+diag(-4am/r^3); companion (M-omega Lm) linearized Beyn rank-1',
        'TUFT_pencil': 'near-wall linear Q0<-Q0+i.m.diag(Omega_F)(2gD+C10); pencil stays linear; Beyn bypasses e^{+/-2/rho} wall (E443/A9)'
    },
    'gr_gate_A': {
        'n0_at_a0': '0.373671684418-0.088962315689i',
        'abs_err': 2.470e-13,
        'digits': '~12 (require >=6)',
        'N_spread_40_60_90': 3.45e-11,
        'verdict': 'PASS'
    },
    'gr_gate_B': {
        'rayleigh_split_over_a': 0.096236,
        'target_split_over_a_erratum42': 0.2515323,
        'real_part_fraction_of_target': '38%',
        'continuation_max_Im_drift_at_a0_02': 1.538e-2,
        'threshold': 5e-3,
        'verdict': 'FAIL',
        'diagnosis': 'bare-diagonal drag embedding reproduces real-part sign but not >=4-digit slope; direct pole jumps under O(a); '
                     'missing Teukolsky O(a) imaginary cross-term 4i(r-1)K/Delta requiring full Chandrasekhar transform into Jansen-compactified pencil; not faked to 4 digits'
    },
    'tuft_side_diagnostic_only': {
        'note': 'gate B not passed -> diagnostic only, NO physical reading (iron rule)',
        'static_reanchor_a0': '0.434445174-0.056449760i',
        'static_reanchor_vs_GradeA_abs_d': 4.5e-9,
        'rotating_raw_UNTRUSTED': {
            'a0.10_m+2': '0.376860600-0.097073912i',
            'a0.10_m-2': '0.366412304-0.141592932i',
            'a0.10_split_over_a': 0.10448,
            'a0.20_m+2': '0.345849701-0.107141431i',
            'a0.20_m-2': '0.414460918-0.139554078i',
            'a0.20_split_over_a': -0.34306
        },
        'vs_v44_first_order_0.09832': 'a=0.10 ~6% close but a=0.20 sign flips to -0.343, drift(0.1->0.2)=0.448 = non-physical; '
                                     'a=0.10 match is coincidence under unstable operator'
    },
    'blocker_condition_wall': {
        'min_sigma_min_L': 7.7e-12,
        'm_minus2_two_path_S1_over_S0': [1.5e-4, 3.1e-5],
        'degeneracy_threshold_exceeded': '>1e-8',
        'a_upper_bound_trusted': '<0.10',
        'residual_divergence_pattern': 'pole jump + S1/S0 degeneracy + split/a non-sign-stable',
        'root_cause': 'O(a) operator not completed (missing imaginary Teukolsky cross-term 4i(r-1)K/Delta); NOT Beyn contour failure (gate A reaches 12 digits on same machine)'
    },
    'next_step': 'complete full Teukolsky-Chandrasekhar O(a) embed (fold imaginary cross-term correctly into Jansen-compactified pencil), re-pass GR gate B, then switch TUFT reflecting wall to report m-split',
    'four_state': 'GR gate A PASS / gate B FAIL -> TUFT rotating poles NOT declared; boundary-spectral methodology extension; no new physical E-number, no new erratum (#42 held); E498 not counted in physical four-state; 35/61/18/27 frozen',
    'D18': 'v31 UPGRADE no rollback (additive boundary-spectral methodology channel)',
    'alliance_layer': '2/6 maintained, UFT-3 locked',
    'open_items': [
        'complete Teukolsky-Chandrasekhar O(a) embed then re-pass GR gate B, then TUFT reflecting-wall m-split (rotating mixed BVP a!=0 still OPEN)',
        'P18 e derivation', 'P19 f_pi absolute quantization',
        'theorem D parameter-space nullity_dyn=0 (downgraded to 1, not 0)',
        'Page three resources', 'Hawking thermal-spectrum side',
        'source excitation-energy absolute scale (E444/E489 OPEN)'],
    'merge_report': 'TUFT_v48_旋转QNM合并报告.md'
}

# 5) open_backlog：前置 v5.8 close 条目
v58_close = ('v5.8/v48: rotating QNM Beyn-extension close (E498; organizer-verified; numbers copied verbatim from '
              '_audit_v48_rotating_qnm_out.txt; double precision; NO prior-project import; NO qnm import at runtime; '
              'disk backed up to .v58pre.bak before replay; starting point v5.7/E1-E497/#42; v5.7 E497, v5.6 E496, v5.4 E494, '
              'erratum #32 bare-iomega ban, erratum #42 gate constant 0.25153 not rolled back). '
              'Derivation chain: Kerr Lense-Thirring Omega_F=2a/r^3 folded as O(a omega) local diagonal potential -4am omega/r^3; '
              'GR Jansen compactified pencil Q1<-Q1+diag(-4am/r^3); TUFT near-wall linear pencil Q0<-Q0+i.m.diag(Omega_F)(2gD+C10). '
              'GR gate A PASS: n0@a=0 |err|=2.470e-13 (~12 digits), N spread=3.45e-11. '
              'GR gate B FAIL: Rayleigh split/a=0.096236 vs target 0.2515323 (real part 38%); continuation max|Im drift|@a=0.02=1.538e-2 > 5e-3; '
              'root cause = missing Teukolsky O(a) imaginary cross-term 4i(r-1)K/Delta requiring full Chandrasekhar transform; not faked to 4 digits. '
              'TUFT side diagnostic-only: static re-anchor |d|=4.5e-9; rotating raw UNTRUSTED split/a@0.10=0.10448/@0.20=-0.34306 sign flip. '
              'Condition wall sigma_min(L)=7.7e-12, trusted a<0.10; root cause = O(a) operator not completed, NOT Beyn contour failure. '
              'Next step = complete Teukolsky-Chandrasekhar O(a) embed then re-pass gate B, then TUFT reflecting-wall m-split. '
              'E498 boundary-spectral methodology channel, not physical four-state; no new erratum (#42 held).')
d['open_backlog'].insert(0, v58_close)

# 6) 更新旋转 odd QNM OPEN 条目（按内容匹配）
old_rot = 'rotating odd QNM exact m-split & damping spin-slope via complex biorthogonal inner product + bare-core model (E475/E476, D27 direction->number; GR gate Kerr per-m 0.2563)'
new_rot = ('rotating odd QNM exact m-split & damping spin-slope via complex biorthogonal inner product + bare-core model (E475/E476, D27 direction->number; '
           'GR gate Kerr per-m 0.2515323 per erratum #42; STILL OPEN). '
           'v48/E498 update: Beyn contour generalized to small rotation a - GR gate A PASS n0 ~12 digits, but GR gate B FAIL '
           '(Rayleigh split/a=0.0962 vs 0.25153; missing Teukolsky O(a) imaginary cross-term 4i(r-1)K/Delta); '
           'condition wall sigma_min(L)=7.7e-12, trusted a<0.10; TUFT rotating poles NOT declared. '
           'NEXT STEP = complete full Teukolsky-Chandrasekhar O(a) embed, re-pass GR gate B, then switch TUFT reflecting wall to report m-split.')
cnt = sum(1 for x in d['open_backlog'] if x == old_rot)
assert cnt == 1, 'rotating open item count=%d' % cnt
d['open_backlog'] = [new_rot if x == old_rot else x for x in d['open_backlog']]

# 7) 写回（1 空格缩进，与原文件一致）
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 8) 复验 json.load 合法
d2 = json.load(open(p, encoding='utf-8'))
print('OK ledger JSON updated + reload valid')
print('version=', d2['version'], '| latest_round=', d2['latest_round'], '| equation_range=', d2['equation_range'], '| latest_erratum=', d2['latest_erratum'])
print('four_state=', d2['four_state_counts_approx']['strict'], d2['four_state_counts_approx']['conditional'], d2['four_state_counts_approx']['definition'], d2['four_state_counts_approx']['open'])
print('v48 key_results present=', 'v48_rotating_qnm_key_results' in d2)
print('open_backlog len=', len(d2['open_backlog']))
print('backlog[0] head=', d2['open_backlog'][0][:60])
