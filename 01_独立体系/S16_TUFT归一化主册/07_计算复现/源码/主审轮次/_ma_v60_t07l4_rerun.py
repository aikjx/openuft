# -*- coding: utf-8 -*-
"""_ma_v60_t07l4_rerun.py — 台账追加 T07 线四审计背书"""
import json, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化台账_v1.0.json'
with open(p, encoding='utf-8-sig') as f:
    d = json.load(f)

d['main_agent_v60_t07_line4_rerun'] = {
    'round': 'MainAgent independent audit of organizer T07 line4 (vortex-light x spiral-worldline coupling) — script read, .venv rerun, output byte-identical (normalized)',
    'date': '2026-09-25',
    'erratum': 42,
    'script': 'tuft_t07_line4_vortex_spiral.py(+_out.txt)',
    'rerun_checks': {
        'IDENTICAL': True,
        'R_old_scaling_const': 1.4142,
        'paraxial_fail_threshold_w0_lambda': 2.251,
        'old_R_old_w050': 4.5015e-01,
        'new_R_new_w050': 1.4329e-01,
        'suppression_x': 3.1,
        'resonance_kappa_peaks_l1_6': [0.060, 0.640, 0.420, 0.320, 0.100, 0.220],
        'gamma_v': 1.0,
        'u2': '-1 (on-shell check)'
    },
    'four_state': {
        'strict': 'u_nu partial_mu T^{mu nu}=0 on shell (antisym F x sym uu) -> rest-frame power; spatial 4-force = h-projection = qF^{mu nu}u_nu; helix self-consistency E18 gamma v=c; R_old ~ 1/(k_L w0) and R_new ~ R_old/(k_L w0); resonance locus l w_s = k_L(gamma - sin theta) from Lorentz Doppler',
        'conditional': 'IF paraxial LG0l l=1 on particle ring THEN 4-force components/f.u closure/E_z suppression as tabulated (E0=1); IF resonant OAM transfer THEN axial force peaks, orbit in unstable locked band width ~Gamma/l',
        'definition': 'spin-torsion coefficient and E475-style 0.35 suppression = analogy labels (not first-principles); theta convention flip flagged (tan=tau/kappa here vs ledger)',
        'open': 'spin-torsion strength TUFT postulate not QED-derived; absolute OAM efficiency needs beam power + charge-mass inputs; full vectorial Sommerfeld closed form not summed (only E_z^(1)); Floquet/linear stability of driven helix OPEN'
    },
    'new_labels': ['D31 (4-force caliber/projector)', 'D32 (non-paraxial residual + threshold 2.25)', 'D33 (resonance locus)', 'D34 (old vs new contrast)'],
    'section_mapping': 'main ledger has NO section 13 (grep confirms); section 16 exists only as gate/discussion anchor -> per rule, section 13 established HERE as paraxial tight-focus failure config; discussion written to section 16 slot. Compliant.',
    'E_number': 'E1-E498 frozen; T07-4 labels D31-D34 only',
    'verdict': ('ENDORSED: script read in full, .venv rerun byte-identical; all four subtasks graded honestly. '
                'Key correctness: u-contraction = on-shell power (zero) is the standard antisym x sym result, spatial 4-force via h-projector is exactly Lorentz force — caliber reconciliation is first-principles correct and explicitly reported. '
                'Non-paraxial Lax E_z^(1) residual table + paraxial-fail threshold 2.25 reproduced. Resonance locus analytic + l=1..6 scan reproduced. '
                'Old-paraxial failure (45% divergence, missing E_z -> f^3 O(1) misestimate) vs new (3.1x suppression) contrast simulated; f.u=0 correctly identified as Lorentz identity in BOTH schemes (not the failure channel). '
                'Section 13/16 mapping handled per rule (no existing sections -> new structure, flagged). No pseudoclose.'),
    'governance': 'master note + diagram t07-line4 section appended by MainAgent'
}
d['version'] = 'v6.0'
d['latest_round'] = 'v6.0_T07line4_endorsed'
tmp = p + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, p)
print('ledger endorsed; keys:', len(d))
