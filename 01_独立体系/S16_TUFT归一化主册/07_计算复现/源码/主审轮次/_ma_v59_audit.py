# -*- coding: utf-8 -*-
import os,json,io,time
for f in ['_audit_v48_rotating_qnm_out.txt','_audit_v48_rotating_qnm.py']:
    print(f, os.path.exists(f))
d=json.load(io.open('TUFT_归一化台账_v1.0.json',encoding='utf-8-sig'))
d['main_agent_v58_v48_evidence_check']={
 "round":"MainAgent check of organizer v5.8 v48 rotating QNM Beyn claim",
 "date":"2026-09-24",
 "finding":"_audit_v48_rotating_qnm.py and _audit_v48_rotating_qnm_out.txt DO NOT EXIST on disk (same pattern as v43-v47). E498 numeric claims (rotating QNM Beyn) UNVERIFIED, not endorsed.",
 "note":"organizer keeps advancing SSOT version headers concurrently while MainAgent audits (v5.6->v5.7->v5.8 during this session); version headers outpace disk evidence. Hard requirement stands: freeze + submit v43-v48 scripts+out, MainAgent re-runs each in .venv."
}
json.dump(d,io.open('TUFT_归一化台账_v1.0.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('keys',len(d),'version',d.get('version'))
