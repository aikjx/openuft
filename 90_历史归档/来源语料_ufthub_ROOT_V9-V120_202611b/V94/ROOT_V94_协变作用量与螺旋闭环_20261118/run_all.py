"""Reproducible V94 checks, including independent V93 archive regression."""
import json,subprocess,sys,zipfile,tempfile,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def call(args,cwd=ROOT):
    print('RUNNING',args,flush=True)
    proc=subprocess.Popen(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    lines=[]
    for line in proc.stdout:
        lines.append(line)
        if line.startswith(('NUMERIC STAGE','Ran ','Sympy checks','dimensions:','V94 results:','{')):
            print(line.rstrip(),flush=True)
    ret=proc.wait(timeout=90)
    if ret!=0:raise RuntimeError(f'failed {args}: {ret} '+''.join(lines[-50:]))
    print('FINISHED',args,flush=True)
    return ''.join(lines)

def main():
    out={}
    out['V94_tests']=call([sys.executable,'-m','unittest','discover','-s','tests','-v'])
    out['Sympy']=call([sys.executable,'-m','src.symbolic_audit'])
    out['dimensions_and_ledger']=call([sys.executable,'-m','src.dimension_and_ledger'])
    if '--skip-numeric' in sys.argv:
        assert (ROOT/'results/NUMERICAL_SUMMARY_THEORY.json').is_file(), 'missing previously generated numeric outputs'
        out['numeric_simulation']='SKIPPED_REGENERATION: separately generated numerical results verified to exist'
    else:
        out['numeric_simulation']=call([sys.executable,'-m','src.generate_results'])
    original=ROOT/'archive/ROOT_V93_original.zip'
    with tempfile.TemporaryDirectory(prefix='v94_v93_') as td:
        with zipfile.ZipFile(original) as z:
            bad=z.testzip()
            if bad:raise RuntimeError(f'V93 original checksum error {bad}')
            z.extractall(td)
        extracted=Path(td)/'ROOT_V93_内外双向螺旋闭环_20261118'
        out['V93_original_tests']=call([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=extracted)
    if '--browser' in sys.argv:
        out['Chromium']=call([sys.executable,'web/browser_smoke.py'])
    counts={'V94_new_Python_tests':int(out['V94_tests'].split('Ran ')[-1].split(' tests')[0]),
            'V93_regression_Python_tests':int(out['V93_original_tests'].split('Ran ')[-1].split(' tests')[0]),
            'V94_SymPy_checks':int(out['Sympy'].split('checks passed:')[-1].strip().splitlines()[0])}
    data={'status':'PASS','counts':counts,'commands':{k:(v[-2200:] if k.endswith('tests') else v[-1800:]) for k,v in out.items()},
          'disclaimer':'Math/numeric/browser checks do not establish experimentally confirmed new laws.'}
    p=ROOT/'results/VALIDATION_REPORT.json'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps({'status':'PASS','counts':counts,'browser_executed':'Chromium' in out,'numeric_regenerated':'--skip-numeric' not in sys.argv},ensure_ascii=False))
    return data

if __name__=='__main__':main()
