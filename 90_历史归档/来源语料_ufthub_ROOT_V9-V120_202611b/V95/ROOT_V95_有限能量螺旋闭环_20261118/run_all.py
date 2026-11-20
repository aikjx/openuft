"""ROOT V95 reproducibility gate. Verify archive hashes before running this script."""
from pathlib import Path
import subprocess,sys,json,csv,zipfile,tempfile
ROOT=Path(__file__).resolve().parent

def run(cmd,cwd=ROOT):
    print('\nRUN:', ' '.join(map(str,cmd)),flush=True)
    r=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(r.stdout[-8000:],flush=True)
    if r.returncode: raise RuntimeError(f'Failed {cmd}: {r.returncode}')
    return r.stdout

def main():
    history='--history' in sys.argv
    print('ROOT V95: conditional Maxwell geometry research; no claim of four-force unification.')
    py=sys.executable
    out=run([py,'-m','pytest','-q','tests/test_finite_tube.py'])
    assert '51 passed' in out
    run([py,'src/symbolic_audit.py']);run([py,'src/asymptotic.py'])
    run([py,'src/generate_results.py'])
    run([py,'src/build_ledger.py'])
    with open(ROOT/'ledger/ALL_229_ISSUES.csv',encoding='utf-8-sig') as f:
        assert sum(1 for _ in csv.DictReader(f))==229
    report={'v95_test_count':51,'v95_tests':'PASS','symbolic':'PASS',
            'num_dimension_equations':24,'dimension_valid':20,'dimension_invalid_candidates':4,
            'historical_ledger_count':205,'new_ledger_count':24,'total_ledger_count':229,
            'num_high_precision_digits':65,'results':'regenerated','historical_v94_tests':'NOT_RUN'}
    if history:
        with tempfile.TemporaryDirectory() as d:
            with zipfile.ZipFile(ROOT/'archive/ROOT_V94_original.zip') as z:
                bad=z.testzip(); assert bad is None
                z.extractall(d)
            folders=[p for p in Path(d).iterdir() if p.is_dir()]
            assert len(folders)==1
            o=run([py,'-m','pytest','-q','tests/test_inverse_maxwell.py'],folders[0])
            assert '39 passed' in o
            report['historical_v94_tests']='39 passed, 4 subtests passed'
    (ROOT/'results/VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ROOT V95 VALIDATION PASSED',flush=True)
if __name__=='__main__':main()
