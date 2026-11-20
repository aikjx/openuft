"""One-command, offline deterministic reproduction. Writes only local research results."""
from pathlib import Path
import sys
import subprocess
import json
import time
ROOT=Path(__file__).resolve().parent

def run(cmd):
    print('EXEC:', ' '.join(cmd),flush=True)
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print((p.stdout or '')[-12000:])
    print((p.stderr or '')[-12000:])
    if p.returncode !=0: raise RuntimeError(f'Failed {cmd}, return {p.returncode}')
    return p

if __name__=='__main__':
    start=time.monotonic()
    r=run([sys.executable,'-m','unittest','discover','-s','tests','-v'])
    import re
    m=re.search(r'Ran (\d+) tests',r.stderr)
    n=int(m.group(1)) if m else None
    sym=run([sys.executable,'src/symbolic_audit.py'])
    z=re.search(r'Symbolic identities checked: (\d+)',sym.stdout)
    run([sys.executable,'src/simulate.py'])
    passed={'python_unit_tests':n,'symbolic_identities_checked':int(z.group(1)) if z else None,
            'elapsed_seconds':round(time.monotonic()-start,2),
            'simulation_label':'THEORY / SYNTHETIC, NEVER OBSERVED',
            'all_passed':True,
            'scope':'fixed branch point-center gravity + Yukawa + Coulomb idealisation'}
    (ROOT/'results'/'validation_summary.json').write_text(json.dumps(passed,indent=2),encoding='utf-8')
    print('SUCCESS',json.dumps(passed,ensure_ascii=False))
