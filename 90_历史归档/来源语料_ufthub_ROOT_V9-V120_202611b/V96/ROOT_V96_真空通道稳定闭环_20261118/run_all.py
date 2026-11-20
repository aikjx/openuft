"""ROOT V96 reproducibility. No claim of discovering a new fundamental force."""
from pathlib import Path
import sys,subprocess,json,csv,zipfile,tempfile,time
ROOT=Path(__file__).resolve().parent

def run(argv,cwd=ROOT):
    print('RUN:', ' '.join(map(str,argv)),flush=True)
    proc=subprocess.run([str(a) for a in argv],cwd=str(cwd),capture_output=True,text=True)
    out=proc.stdout+'\n'+proc.stderr
    print(out[-6000:],flush=True)
    if proc.returncode:raise RuntimeError(f'Failed command: {argv}; returncode {proc.returncode}')
    return out

def main():
    start=time.time();py=sys.executable
    print('ROOT V96: finite-size external-current Maxwell field, linear weak focusing, no four-force unification.')
    output=run([py,'-m','unittest','discover','-s','tests','-p','test_*.py'])
    assert 'Ran 36 tests' in output and 'OK' in output
    so=run([py,'src/symbolic_audit.py']);assert so.count('PASS')==11
    run([py,'src/generate_results.py'])
    summary=json.loads((ROOT/'results/NUMERICAL_SUMMARY_THEORY.json').read_text())
    ref=summary['baseline']
    assert 0<ref['n']<1
    assert abs(ref['nu_r']**2+ref['nu_z']**2-1)<1e-12
    assert summary['long_trajectory']['turns']==100
    assert abs(summary['return_map']['determinant']-1)<1e-5
    with (ROOT/'ledger/ALL_253_ISSUES.csv').open(encoding='utf-8-sig',newline='') as f:
        assert sum(1 for row in csv.DictReader(f))==253
    status={'v96_unittest':'36 PASS','v96_symbolic_and_dimensions':'11 PASS (including 2 intentionally rejected equations)',
            'v96_field_source':'continuous smooth finite cross section','v96_n':ref['n'],
            'v96_100_turns':'numerically bounded for specified small perturbation',
            'v96_maxwell_local':'analytic + independent numerical finite difference',
            'ledger_total':253,'prior_v95_51_tests':'NOT_RUN','chromium':'run separately in an environment with Chromium'}
    if '--history' in sys.argv:
        with tempfile.TemporaryDirectory() as d:
            p=ROOT/'archive/ROOT_V95_original.zip'
            with zipfile.ZipFile(p) as z:
                assert z.testzip() is None
                z.extractall(d)
            folders=[x for x in Path(d).iterdir() if x.is_dir()]
            assert len(folders)==1
            hist=run([py,'-m','pytest','-q','tests/test_finite_tube.py'],folders[0])
            assert '51 passed' in hist
            status['prior_v95_51_tests']='PASS, independently extracted from original ZIP'
    status['elapsed_seconds']=round(time.time()-start,2)
    (ROOT/'results/VALIDATION_REPORT.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
    print('V96 reproducibility PASS:',status)
if __name__=='__main__':main()
