#!/usr/bin/env python3
"""ROOT V141 fully reproducible symbolic and numerical audit."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import sys
import unittest

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from src.coupled import Params, integrate, diagnostic_summary, local_omega_squared
from src.field import lagrangian_density_units


def main():
    (BASE/'results').mkdir(exist_ok=True)
    p=Params()
    rows=integrate(p=p)
    summary=diagnostic_summary(rows,p)
    summary['status']='model-only validation, no real-world data used'
    summary['input_class']='illustrative_dimensionless_initial_conditions'
    summary['initial']=[0.3,0.2,0.0,0.3]
    summary['helicity_external_gradient_example']={
       'theta_dot':0.1,
       'omega_sq_plus':local_omega_squared(p,0.1,+1),
       'omega_sq_minus':local_omega_squared(p,0.1,-1),
       'caveat':'Local coefficient approximation only; non-backreacted background'}
    summary['units']=lagrangian_density_units()
    with (BASE/'results'/'coupled_helical_mode.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    with (BASE/'results'/'summary.json').open('w',encoding='utf-8') as f:
        json.dump(summary,f,indent=2,ensure_ascii=False)
    suite=unittest.defaultTestLoader.discover(str(BASE/'tests'),pattern='test_*.py',top_level_dir=str(BASE))
    import io
    sio=io.StringIO()
    result=unittest.TextTestRunner(stream=sio,verbosity=2).run(suite)
    log=(f'ROOT V141 automated tests: {result.testsRun} run, '
         f'{len(result.failures)} failures, {len(result.errors)} errors\n'
         + sio.getvalue())
    (BASE/'results'/'test_run.log').write_text(log,encoding='utf-8')
    print(log)
    print(json.dumps({k:v for k,v in summary.items() if k.startswith('max_') or k in ('photon_energy_min','photon_energy_max','scalar_energy_min','scalar_energy_max')},indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':sys.exit(main())
