#!/usr/bin/env python3
"""Single-command reproducible analysis (stdlib only)."""
from __future__ import annotations
import csv, json, re, sys, unittest
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v146 import illustrative_six_d, anomalies_U1F, sm_hypercharge_anomalies_per_generation

def build_results():
    out = ROOT/'results'
    out.mkdir(exist_ok=True)
    flux_scan=[]
    for n in range(0,9):
        sd=illustrative_six_d(n)
        p=sd.reduce()
        stable=p.stable()
        extrema=p.extrema()
        flux_scan.append({
            'flux_n':n, 'A':p.A, 'B':p.B, 'C':p.C,
            'discriminant':p.discriminant(),
            'stable_exists':stable is not None,
            'stable_radius':stable.radius if stable else None,
            'stable_V':stable.value if stable else None,
            'stable_mass2':stable.mass2_homogeneous if stable else None,
            'stationary_count':len(extrema),
            'note':'Minkowski by parameter tuning, not generation prediction' if n==3 else '',
        })
    with (out/'flux_vacua_scan.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(flux_scan[0])); writer.writeheader(); writer.writerows(flux_scan)
    with (out/'radion_potential_scan.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['R_over_L0','V_n1','V_n2','V_n3','V_n4']);writer.writeheader()
        for i in range(30,801):
            R=i/200
            writer.writerow({'R_over_L0':R, **{f'V_n{n}':illustrative_six_d(n).reduce().v(R) for n in range(1,5)}})
    info={
      'project':'ROOT V146',
      'status':'toy Einstein-Maxwell S2 compactification; not verified unification',
      'assumptions':{'c':1,'hbar':'retained as dimensionful action', 'G':'independent dimensionful coupling',
                     '6d_geometry':'M4 x S2','n3_selected_by_hand':True,'all_moduli_stable':'not checked'},
      'illustrative_coefficients':{'A':1.,'B':2.,'C_n3':1.,'K4':2.},
      'n3_vacuum':illustrative_six_d(3).reduce().stable().as_dict(),
      'six_dimensional_background_equations_residual':illustrative_six_d(3).minkowski_einstein_residuals(1),
      'n3_barrier_radius':illustrative_six_d(3).reduce().extrema()[1].radius,
      'n3_barrier_height':illustrative_six_d(3).reduce().extrema()[1].value,
      'illustrative_anomalies_F_one_charge_three_families':{k:str(v) for k,v in anomalies_U1F(3).items()},
      'SM_Y_anomalies_one_family':{k:str(v) for k,v in sm_hypercharge_anomalies_per_generation().items()},
      'vacua':flux_scan,
      'limits':['not a derivation of n=3', 'not a derivation of full Standard Model',
                'no full KK scalar-vector-tensor spectrum', 'no observed data fit',
                'no quantum radiative stability proof','no quantum gravity completion'],
    }
    (out/'results.json').write_text(json.dumps(info,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return info

def tests():
    suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    import io
    stream=io.StringIO()
    res=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    log=stream.getvalue()
    normalized_log = re.sub(r'Ran (\d+) tests in [0-9.]+s', r'Ran \1 tests (walltime varies)', log)
    (ROOT/'results'/'test_log.txt').write_text(normalized_log,encoding='utf-8')
    print(log)
    if not res.wasSuccessful(): raise SystemExit(1)
    print(f'CHECK: {res.testsRun}/{res.testsRun} tests passed')
    return res.testsRun

if __name__=='__main__':
    build_results()
    tests()
