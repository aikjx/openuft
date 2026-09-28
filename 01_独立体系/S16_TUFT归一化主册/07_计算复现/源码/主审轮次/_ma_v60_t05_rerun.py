# -*- coding: utf-8 -*-
"""_ma_v60_t05_rerun.py — 台账追加 T05 收官审计背书（v6.0）"""
import json, os

p = 'D:/a10/aikjx/code/my_lib/TUFT_归一化台账_v1.0.json'
with open(p, encoding='utf-8-sig') as f:
    d = json.load(f)

d['main_agent_v60_t05_rerun'] = {
    'round': 'MainAgent independent audit of organizer T05 finalize (v6.0 freeze) — script read, .venv rerun, master/ledger verified',
    'date': '2026-09-24',
    'erratum': 42,
    'rerun_checks': {
        'alpha_inv': 137.035999,
        'm_Pl/m_e': 2.389222e22,
        'y_t/y_e': 3.380829e5,
        'G_residual_log10': 3.529,
        'washout': 0.354430,
        'Y_BL_required': 2.454643e-10,
        'anomaly_SU3': 0.0, 'anomaly_SU2': 0.0, 'anomaly_U1cube': 2.220e-16
    },
    'matrix_final': '0 fully-closed / 3 input-boundary (G3, P_T+eta_new+NE, M2-EXT) / 1 conditional (P17) / 10 partial / 0 untouched (sum=14)',
    'inputs9': 'I1 alpha-1=P9, I2 m_Pl/m_e, I3 y_t/y_e (G_res~3.38e3), I4 N_g=3(G3), I5 theta_QCD, I6 eta_new, I7 NE(V(n,T)), I8 M2-EXT, I9 Q=B-L (E329); P18 minimality downgraded per E483/E484; P19 not in set',
    'E329_registration': 'Q=B-L registered (definition-level identification); Q=B requires P_T freeze-N_CS as fallback, not chosen; consistent with sphaleron under SM reduction (conditional theorem)',
    'master_verified': 'Sec 21 v6.0 freeze appended (E329 + matrix + inputs9 + open-items + invariants + freeze marker); pre-write backup .ma_v60pre_20260924_052912.bak in place; E1-E498 unchanged, no new E-number closed this round',
    'ledger_verified': 'main_agent_v59_t05_finalize key present (105 keys), version=v6.0, latest_round=v6.0_T05_finalize_freeze',
    'verdict': ('ENDORSED: all rerun numbers reproduced; matrix final 0/3+1/10/0 with explicit no-pseudoclose (fully-closed frozen at 0); '
                'inputs9 authoritative registration with P-series cross-check (P18 downgrade correct per E483/E484); E329 Q=B-L definition registration completed as required; '
                'open-items freeze explicit (O-M1..M4, N_R Hopf, c_m interval, QNM spectrum, l_A 12%, Yukawa source BLOCKED, Page/D25, baryogenesis window). TUFT v6.0 final freeze ACCEPTED as normalization-loop closure.'),
    'governance': 'scripts+out: tuft_t05_finalize_v6.py(+_out.txt); rerun log _ma_t05_finalize_rerun.txt; master Sec21 appended with marker <!-- ma-t05-v60-freeze -->'
}
d['version'] = 'v6.0'
d['latest_round'] = 'v6.0_T05_finalize_endorsed'
tmp = p + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, p)
print('ledger endorsed; keys:', len(d))
