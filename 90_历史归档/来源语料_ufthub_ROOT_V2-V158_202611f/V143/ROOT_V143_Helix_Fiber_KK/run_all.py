"""Standard-library test runner + SymPy checks and repeatable CSV/JSON reports."""
import csv
import hashlib
import io
import json
import os
import unittest
from pathlib import Path
from src.physics import diagnostics,ALPHA,PLANCK_MASS_KG
from src.symbolic_checks import main as symbolic_main

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)

def main():
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py',top_level_dir=str(ROOT))
    res=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    result=diagnostics()
    syms=symbolic_main()
    result['test_summary']={'run':res.testsRun,'failures':len(res.failures),'errors':len(res.errors),
                           'successful':res.wasSuccessful(),'symbolic':{n:v['passed'] for n,v in syms.items()}}
    (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'symbolic.json').write_text(json.dumps(syms,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'tests.log').write_text(stream.getvalue(),encoding='utf-8')
    with (OUT/'mass_coupling_scan.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['mass_over_planck_mass','alpha_minimal_KK','alpha_obs_CODATA_2022','status'])
        for r in ['1e-23','1e-20','1e-10','1e-5','0.001','0.01','0.042715','0.1']:
            ratio=float(r)
            writer.writerow([r,4*ratio**2,ALPHA,'model prediction; not observation'])
    print(stream.getvalue())
    print('Symbolic:',{n:v['passed'] for n,v in syms.items()})
    print('Saved results:',OUT)
    if not res.wasSuccessful() or not all(q['passed'] for q in syms.values()):
        raise SystemExit(1)

if __name__=='__main__':main()
