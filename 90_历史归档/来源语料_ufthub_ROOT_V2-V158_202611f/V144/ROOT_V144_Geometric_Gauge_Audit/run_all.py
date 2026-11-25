#!/usr/bin/env python3
"""Regenerate V144 results, verify symbolic identities, execute unit tests.
Requires numpy and sympy. No network; no experimental data fetched.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path
from src.physics import (M_E_SI,M_MU_SI,M_P_SI,ALPHA_OBS,kk_summary,
                         lie_algebra_summary,kk_alpha_for_mass,kk_radius_for_mass,
                         kk_min_mass_for_alpha,kk_radius_for_alpha,
                         product_scalar_curvature)
from src.symbolic_checks import run_symbolic

BASE=Path(__file__).resolve().parent
RESULTS=BASE/'results'
RESULTS.mkdir(exist_ok=True)

def write_json(name,obj):
    (RESULTS/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')


def main():
    symbolic=run_symbolic()
    group=lie_algebra_summary()
    kk=kk_summary()
    write_json('symbolic.json',symbolic)
    write_json('group_algebra.json',group)
    write_json('kk_electron.json',kk)
    report={'label':'ROOT V144: established mathematics + excluded minimal toy-model assumptions',
            'unit_convention':'c=1; G,hbar not set to one; c_SI restored for data conversion',
            'group':group,'kk_electron':kk,'symbolic':symbolic,
            'positive_scalar_curvature_equal_frame_scales_L0':product_scalar_curvature(),
            'untwisted_dirac_eigenvalue_sq_lower_bound_L0inv2':product_scalar_curvature()/4,
            'data_status':'CODATA measured constants only; no new observation; no actual satellite fit',
            'unification_proved':False,'original_helix_derivation_of_SM':False}
    write_json('summary.json',report)
    with (RESULTS/'mass_coupling_scan.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['name','input_mass_kg','naive_kk_alpha','observed_alpha_for_reference','radius_for_mass_m','note'])
        for name,m in [('electron',M_E_SI),('muon',M_MU_SI),('proton_composite_example',M_P_SI),('charged_kk_alpha_match_mass',kk_min_mass_for_alpha())]:
            w.writerow([name,f'{m:.12e}',f'{kk_alpha_for_mass(m):.12e}',f'{ALPHA_OBS:.12e}',f'{kk_radius_for_mass(m):.12e}',
                        'hypothetical minimally coupled n=1 KK mode, not fitted matter spectrum'])
    cmd=[sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-v']
    res=subprocess.run(cmd,cwd=BASE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (RESULTS/'tests.log').write_text(res.stdout,encoding='utf-8')
    print('=== ROOT V144 summary ===')
    print(f'Generators SU3+SU2+U1: {group["dims"]["SM_generators"]}; Jacobi SU3 max: {group["jacobi_max_su3"]:.2e}')
    print(f'alpha_KK electron: {kk["alpha_electron_naive_kk"]:.6e}; mismatch: {kk["alpha_mismatch_factor"]:.6e}')
    print(f'mass required for alpha: {kk["charged_kk_lower_mass_kg"]:.6e} kg')
    print(f'scalar at unit frame lengths: {group["scalar_product_equal_length_L0"]:.6f}; untwisted zero modes excluded under model assumptions')
    print(f'SymPy exact checks: {symbolic["checks_passed"]}')
    print(res.stdout.splitlines()[-3:] if res.stdout else 'no test output')
    if res.returncode:
        print(res.stdout, file=sys.stderr)
        raise SystemExit(res.returncode)
    print('PASS: calculation and regression tests; NOT a proof of unified physics')

if __name__=='__main__': main()
