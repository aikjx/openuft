#!/usr/bin/env python3
"""Recalculate outputs and verify formal tests. Does not operate physical instruments."""
from pathlib import Path
import subprocess,sys,hashlib,json
root=Path(__file__).resolve().parent
commands=[
 [sys.executable,'tools/build_catalog.py'],
 [sys.executable,'tools/generate_results.py'],
 [sys.executable,'tools/symbolic_audit.py'],
 [sys.executable,'tools/independent_quadrature.py'],
 [sys.executable,'-m','unittest','discover','-s','tests','-v']
]
logs=[]
for command in commands:
 proc=subprocess.run(command,cwd=root,text=True,capture_output=True)
 logs.append({'command':' '.join(command),'exit_code':proc.returncode,'stdout_tail':proc.stdout[-2500:],'stderr_tail':proc.stderr[-2500:]})
 print('OK' if proc.returncode==0 else 'FAIL',' '.join(command))
 if proc.returncode:
  (root/'results'/'run_report.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
  print(proc.stdout,proc.stderr,file=sys.stderr);sys.exit(1)
count_test=next((x for x in logs if 'unittest' in x['command']),None)
report={'status':'PASS','mode':'mathematical and synthetic computational validation only','tasks':logs,
        'test_log':count_test['stderr_tail'] if count_test else None}
(root/'results'/'run_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('All model checks passed. No physical experiments performed.')
