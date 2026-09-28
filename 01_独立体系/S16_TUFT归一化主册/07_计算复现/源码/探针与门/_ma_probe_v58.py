# -*- coding: utf-8 -*-
import json,io,os
d=json.load(io.open('TUFT_归一化台账_v1.0.json',encoding='utf-8-sig'))
for k in ['version','latest_round','equation_range','latest_erratum']:
    print(k,'=',d.get(k))
print('keys',len(d),'tail',list(d.keys())[-4:])
print('my key present:', 'main_agent_v53_v57_unsupported_claims' in d)
print('v47 key present:', 'v47_a4_snr_key_results' in d)
if 'v47_a4_snr_key_results' in d: print('v47:', json.dumps(d['v47_a4_snr_key_results'],ensure_ascii=False)[:500])
