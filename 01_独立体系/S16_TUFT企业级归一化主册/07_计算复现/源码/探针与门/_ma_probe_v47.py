# -*- coding: utf-8 -*-
import json,io
d=json.load(io.open('TUFT_归一化台账_v1.0.json',encoding='utf-8-sig'))
for k in ['version','latest_round','equation_range','latest_erratum','four_state_frozen','crack_matrix_status','puzzle_matrix','uft_alliance_layer','main_agent_v42_e2e_endorsement','main_agent_t01_gate_rebase','main_agent_t01_gate_hardening']:
    if k in d: print(k,'=',json.dumps(d[k],ensure_ascii=False)[:400])
print('--- keys tail ---')
ks=list(d.keys()); print(len(ks), ks[-12:])
if 'v47_a4_snr_key_results' in d:
    print('v47 present:', json.dumps(d['v47_a4_snr_key_results'],ensure_ascii=False)[:800])
