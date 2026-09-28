# -*- coding: utf-8 -*-
import json,io,os
d=json.load(io.open('TUFT_归一化台账_v1.0.json',encoding='utf-8-sig'))
for k in ['v43_anomaly_slowrot_key_results','v44_mirror_slowrot_key_results','v45_a9_multiseg_key_results','v46_a6_2pn_key_results','v42_end_to_end_key_results']:
    if k in d:
        print('===',k,'===')
        s=json.dumps(d[k],ensure_ascii=False)
        print(s[:1200]); print()
print('nkeys=',len(d))
# check which claimed out files exist
for f in ['_audit_v43_slow_rotation_out.txt','_audit_v44_mirror_slowrot_out.txt','_audit_v45_multiseg_frobenius_out.txt','_audit_v46_2pn_coupling_out.txt','_audit_v43_slow_rotation.py','_audit_v44_mirror_slowrot.py','_audit_v45_multiseg_frobenius.py','_audit_v46_2pn_coupling.py']:
    print(f, os.path.exists(f))
