# -*- coding: utf-8 -*-
import json,io
d=json.load(io.open('TUFT_归一化台账_v1.0.json',encoding='utf-8-sig'))
print('version',d.get('version'),'round',d.get('latest_round'),'range',d.get('equation_range'),'err',d.get('latest_erratum'))
print('keys',len(d))
for k in ['main_agent_v53_v57_unsupported_claims','main_agent_v58_a6_independent_verify','main_agent_t01_gate_hardening']:
    print(k, k in d)
print('tail keys:', list(d.keys())[-6:])
# find any v48 key
for k in d:
    if 'v48' in k.lower(): print('V48 KEY:', k, json.dumps(d[k],ensure_ascii=False)[:400])
