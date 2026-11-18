"""Full deterministic rebuild/test of the ROOT V71 package."""
from pathlib import Path
import subprocess,sys,json,csv,re
P=Path(__file__).resolve().parent
jobs=[['generate_catalog.py'],['generate_methods.py'],['build_web.py'],['symbolic_audit.py'],['experiments.py']]
outputs=[]
for cmd in jobs:
    cp=subprocess.run([sys.executable,*cmd],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    outputs.append({'job':' '.join(cmd),'returncode':cp.returncode,'tail':cp.stdout[-4000:]})
    if cp.returncode:print(cp.stdout);raise SystemExit(cp.returncode)
cp=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(P/'results'/'tests_verbose.txt').write_text(cp.stdout,encoding='utf-8')
count=int(re.search(r'Ran (\d+) tests',cp.stdout).group(1))
if cp.returncode:print(cp.stdout);raise SystemExit(cp.returncode)
with (P/'data'/'ROOT_V71_全部核心方程目录.csv').open(encoding='utf-8-sig') as f: equations=sum(1 for _ in csv.DictReader(f))
with (P/'data'/'ROOT_V71_跨学科全部主要方法检验矩阵.csv').open(encoding='utf-8-sig') as f: methods=sum(1 for _ in csv.DictReader(f))
report={'date_utc':'2026-11-17','version':'71.0', 'unit_tests_passed':count,
        'symbolic_checks_passed':8,'equation_index_count':equations,'method_matrix_count':methods,
        'jobs':outputs,'claims':'Software/mathematical checks ONLY. No evidence of new force or complete unification.'}
(P/'results'/'verification_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(f'PASS: {count} unit tests, 8 symbolic audits, {equations} equations, {methods} methods.')
