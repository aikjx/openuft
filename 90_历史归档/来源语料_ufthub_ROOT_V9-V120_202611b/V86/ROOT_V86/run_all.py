#!/usr/bin/env python3
"""One-command audit: protocol, math tests, symbolic verification, synthetic results and optional browser."""
import json,subprocess,sys,os,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
report={'version':'ROOT V86','task':'code and math reproduction, not an empirical discovery','commands':[]}
def run(args,name,required=True):
    p=subprocess.run(args,cwd=ROOT,encoding='utf8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=p.stdout[-25000:]
    (ROOT/'results'/f'{name}.log').write_text(log,encoding='utf8')
    report['commands'].append({'name':name,'ok':p.returncode==0,'return_code':p.returncode,'command':' '.join(args)})
    print(f'{name}: {"PASS" if p.returncode==0 else "FAIL"}')
    if p.returncode!=0 and required:
        print(log[-3500:]);raise SystemExit(1)
    return log
(ROOT/'results').mkdir(exist_ok=True)
run([sys.executable,'tools/build_catalogs.py'],'catalogs')
run([sys.executable,'tools/build_protocols.py'],'protocols')
unittest=run([sys.executable,'-m','pytest','tests','-q'],'pytest')
match=re.search(r'(\d+) passed',unittest)
report['pytest_passed']=int(match.group(1)) if match else None
run([sys.executable,'tools/symbolic_audit.py'],'symbolic')
run([sys.executable,'tools/generate_results.py'],'synthetic')
if '--skip-browser' in sys.argv:
    report['browser']='skipped on request'
else:
    try:
        import playwright
        run([sys.executable,'tools/browser_check.py'],'browser',required=False)
        doc=ROOT/'results/browser_report.json'
        report['browser']=json.loads(doc.read_text(encoding='utf8'))['passed'] if doc.exists() else 'not run'
    except ImportError:
        report['browser']='not installed: browser check optional'
report['symbolic_passed']=json.loads((ROOT/'results/symbolic_report.json').read_text(encoding='utf8'))['passed']
report['catalog']=json.loads((ROOT/'data/catalog_summary.json').read_text(encoding='utf8'))
report['synthetic_seed']=20261118
report['real_hardware']=False
report['independently_predicted_G']=False
report['four_forces_unified']=False
(ROOT/'results/run_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
if any(not x['ok'] for x in report['commands']): raise SystemExit('One or more checks failed')
print('PASS: all mandatory checks')
