"""Reproduce model-level ROOT V91 computational results, not a quantum gravity experiment."""
from __future__ import annotations
import subprocess,sys,zipfile,tempfile,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(args,cwd=ROOT,stdout_path=None):
    result=subprocess.run([sys.executable]+list(args),cwd=cwd,encoding='utf8',
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    if stdout_path:stdout_path.write_text(result.stdout,encoding='utf8')
    print('Command',args,'return',result.returncode,'tail:',result.stdout[-400:].strip())
    if result.returncode:raise RuntimeError('Command failed: '+repr(args))
    return result.stdout

def main():
    run(['src/build_ledger.py'])
    run(['src/symbolic_audit.py'])
    run(['-m','src.simulate'])
    unit=run(['-m','unittest','discover','-s','tests','-v'],stdout_path=ROOT/'results/unittest_run.log')
    m=re.search(r'Ran (\d+) tests',unit)
    if not m:raise RuntimeError('no unittest count')
    n=int(m.group(1))
    if n<100:raise RuntimeError('expected >=100 meaningful tests')
    baseline=ROOT/'archive/ROOT_V90_原始归档.zip'
    with tempfile.TemporaryDirectory(prefix='root_v90_baseline_') as tmp:
        with zipfile.ZipFile(baseline) as z:z.extractall(tmp)
        sub=Path(tmp)/'ROOT_V90_Unification_Research_20261118'
        base_out=run(['-m','unittest','discover','-s','tests','-q'],cwd=sub,stdout_path=ROOT/'results/V90_baseline_regression.log')
        bm=re.search(r'Ran (\d+) tests',base_out)
        bn=int(bm.group(1)) if bm else 0
        if bn!=65:raise RuntimeError(f'unexpected V90 tests count {bn}')
    symbols=json.loads((ROOT/'results/symbolic_checks.json').read_text(encoding='utf8'))
    prec=json.loads((ROOT/'results/independent_100_digit_precision.json').read_text(encoding='utf8'))
    statuses=json.loads((ROOT/'ledger/STATUS_COUNTS.json').read_text(encoding='utf8'))
    summary={'date':'2026-11-18','scientific_status':'theory and software only; FULL UNIFICATION NOT SOLVED',
             'V91_python_tests_passed':n,'V90_python_tests_passed':bn,
             'SymPy_identical_checks_passed':symbols['passed'],
             '100_digit_independent_cases_passed':len(prec['data']),
             'max_relative_precision_disagreement':prec['max_relative_disagreement'],
             'issue_count':statuses['total'],'issue_statuses':statuses['statuses'],
             'theory_scan_points':151,'real_new_physics_experiments':0,
             'proof_of_G_origin':False,'four_interaction_unification_proven':False}
    (ROOT/'results/ACCEPTANCE_REPORT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
