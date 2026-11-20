from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parent
steps=[['scripts/build_catalog.py'],['scripts/build_protocols.py'],['scripts/generate_results.py'],['tests/symbolic_checks.py']]
for step in steps:
    cmd=[sys.executable,*step]
    print('RUN', ' '.join(cmd),flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True)
cmd=[sys.executable,'-m','pytest','-q','tests/test_physics.py','tests/test_reference.py']
print('RUN',' '.join(cmd),flush=True)
p=subprocess.run(cmd,cwd=ROOT,check=True,capture_output=True,text=True)
print(p.stdout)
try:
    import re
    num=int(re.search(r'(\d+) passed',p.stdout).group(1))
except Exception:num=None
sym=json.loads((ROOT/'results/symbolic_checks.json').read_text(encoding='utf8'))
report={'package':'ROOT_V89','test_count':num,'symbolic_count':sym['count'],'symbolic_passed':sym['passed'],
        'python_tests_passed':True,'data_is_synthetic':True,
        'quantum_gravity_observed':False,'G_predicted_independently':False}
(ROOT/'results/test_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('RESEARCH TEST SUITE PASSED',report)
