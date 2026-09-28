# -*- coding: utf-8 -*-
"""_ma_v60_t06_rerun.py — 台账追加 T06 审计背书（v6.0 后攻坚轮）"""
import json, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化台账_v1.0.json'
with open(p, encoding='utf-8-sig') as f:
    d = json.load(f)

d['main_agent_v60_t06_rerun'] = {
    'round': 'MainAgent independent audit of organizer T06 (N_R Hopf identity + QNM Gate B) — scripts read, .venv rerun, outputs byte-identical (normalized)',
    'date': '2026-09-24',
    'erratum': 42,
    'scripts': {
        'line1': 'tuft_t06_line1_NR_hopf_id.py(+_out.txt)',
        'line2': 'tuft_t06_line2_qnm_overtone.py(+_out.txt)'
    },
    'rerun_checks': {
        'line1_IDENTICAL': True,
        'line2_identical_except_walltime_and_tail_print': True,
        'gamma_2_over_rhoh': 3.279215613,
        'Q_ladder': {'Q_R': 1, 'Q_t': 10, 'Q_e': 14, 'Q_nu': 19},
        'M_R_GeV': {'Q1': 1.00e14, 'Q2': 6.33e12, 'Q3': 3.23e11},
        'lattice_span': 3.8635e5, 'obs_span': 3.3808e5, 'rel': 0.1428,
        'lattice_over_Gres': 114.278,
        'K_N': 23.360,
        'GR_n0': '0.373671684418-0.088962315689i (|err|=1.59e-15 vs Gate A anchor)',
        'GR_splitR_a': 0.25153232, 'GR_gateB_digits': 7.7,
        'TUFT_n0_N90vs120': '8.359e-10 PASS (<=1e-9); 8.3 digits vs Grade A anchor',
        'TUFT_overtone_best_Nconsist': '2.940e-05 -> n=1,2 OPEN (honest)',
        'Oa_vs_Leaver_diff': [6.104e-03, 6.135e-03, 1.344e-02],
        'Rayleigh_vs_cont_005': 2.00e-03
    },
    'four_state': {
        'strict': 'seesaw algebra exact; N_R gauge-singlet zero anomaly; E142/E181-E189 vetoes stand; GR Leaver n=0 14.8 digits; GR GateB 7.7 digits; O(a) vs Leaver difference = O(a^2) quantified',
        'conditional': 'Q_N=1 anchors M_R~1e14 GeV via E140 with geometric gamma=2/rho_h; Q-lattice bridges I3 gap (overshoot ~114x); TUFT n=0 fundamental Gate B PASS (8.3 digits, N-consist 8.36e-10); Rayleigh E475 split=1.635427 validated vs continuation (0.2%, O(a^2))',
        'definition': 'Q_N=1 = lowest Hopf sector of heavy N_R; gamma=2/rho_h lattice spacing; Chandrasekhar O(a) embedding = first-order perturbation',
        'open': 'Q_N uniqueness (Q=1/2/3 all phenomenologically allowed); integer assignment precision O(15-57%) < 6-digit gate; K_N=23.4>1 washout needs resonant leptogenesis or freeze-in; I6 CP phase / I7 V(n,T) still open; TUFT n=1,2 overtone/damping spectrum OPEN (N-consist 2.94e-05 > 1e-9)'
    },
    'E_number': 'E1-E498 frozen unchanged; T06 conclusions only (no new E-number allocated pending MainAgent ruling)',
    'verdict': ('ENDORSED: both scripts read in full, .venv rerun reproduced all numbers; line1 output byte-identical, line2 identical except wall time and tail print line. '
                'Honest OPEN kept for n=1,2 overtones and Q_N uniqueness; conditional bridge of I3 gap (overshoot 114x) correctly labelled as FIT not strict theorem; '
                'v50 voided values (0.5805, 2.337) not resurrected. Gate B n=0 PASS (8.3 digits, N-consist 8.359e-10) accepted. '
                'No pseudoclose. T06 ENDORSED for registration.'),
    'governance': 'master Sec21 note + diagram t06 section appended by MainAgent'
}
d['version'] = 'v6.0'
d['latest_round'] = 'v6.0_T06_endorsed'
tmp = p + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, p)
print('ledger endorsed; keys:', len(d))
