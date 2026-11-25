#!/usr/bin/env python3
"""Reproduce ROOT V147 calculations and unit tests, no network or 3rd party packages."""
from __future__ import annotations
import csv
import json
import os
from pathlib import Path
import sys
import unittest
from fractions import Fraction

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'src'))
from root_v147.flux import (illustrated,FluxModel,tuned_flat_vacuum,
    scalar_test_mass_squared,degeneracy,scalar_strength_brane,
    yukawa_force_fraction,yukawa_potential_fraction)
from root_v147.anomalies import (anomaly_coefficients,fields_uniform_family,
    fields_B_minus_L,multiply,chiral_index)


def write_csv(name,columns,rows):
    with (BASE/'results'/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)


def generate_results():
    (BASE/'results').mkdir(exist_ok=True)
    vac=[]
    for n in range(-8,9):
        p=illustrated(n);e=p.min()
        vac.append({'n':n,'chirality_index_q1':chiral_index(n),'discriminant':p.D,
                    'radius_min':e.radius if e else '', 'Vmin':e.energy if e else '',
                    'radion_mass2':e.radial_mass2 if e else '',
                    'type':e.kind if e else 'no_radial_minimum'})
    write_csv('flux_vacuum_scan.csv',list(vac[0]),vac)

    flat=[]
    for n in (-11,-7,-4,-3,-2,-1,1,2,3,4,7,11):
        flat.append(tuned_flat_vacuum(n))
    write_csv('tuned_flat_degeneracy.csv',list(flat[0]),flat)

    critical=[]
    for d in (1e-1,1e-2,1e-3,1e-4,1e-5,1e-6):
        C=4/3*(1-d)
        p=FluxModel(1,2,C,2);e=p.min()
        critical.append({'distance_from_critical':d,'C':C,'D':p.D,
                         'R_min':e.radius,'radion_mass2':e.radial_mass2,
                         'radion_range_L0':1/e.radial_mass2**.5,
                         'dR_dC':p.drdC_at_min()})
    write_csv('critical_sensitivity.csv',list(critical[0]),critical)

    modes=[]
    for ell in range(0,13):
        modes.append({'ell':ell,'degeneracy':degeneracy(ell),
                      'neutral_scalar_mass2_R1':scalar_test_mass_squared(ell,1.),
                      'neutral_scalar_mass2_R2':scalar_test_mass_squared(ell,2.)})
    write_csv('neutral_test_scalar_modes.csv',list(modes[0]),modes)

    profile=[]
    for k in range(0,101):
        x=k/20
        profile.append({'r_over_lambda':x,'potential_fraction':yukawa_potential_fraction(x,1.),
                        'force_fraction':yukawa_force_fraction(x,1.)})
    write_csv('conditional_radion_force.csv',list(profile[0]),profile)

    uniform=multiply(anomaly_coefficients(fields_uniform_family()),3)
    bl=multiply(anomaly_coefficients(fields_B_minus_L()),3)
    js={'version':'V147','status':'mathematical toy model not empirical proof',
        'units':'c=1 only; hbar and G dimensional',
        'illustrative_vacuum_n3':{'A':1.,'B':2.,'C':1.,'K4':2.,
          'Rstar':illustrated(3).min().radius,
          'vacuum_energy':illustrated(3).min().energy,
          'radion_mass2_L0_inverse2':illustrated(3).min().radial_mass2,
          'radion_range_over_L0':1.,'barrier_height':4/27,
          'conditional_scalar_force_alpha':scalar_strength_brane()},
        'uniform_family_anomalies_three_gen':{k:str(v) for k,v in uniform.items()},
        'B_minus_L_with_N_R_three_gen_anomalies':{k:str(v) for k,v in bl.items()},
        'critical_nearby':critical,
        'limitations':['No full KK coupled fluctuation spectrum',
                       'No six-dimensional fermion anomaly calculation',
                       'No independent derivation of n=3',
                       'No phenomenological fit to experimental data',
                       'No derivation of standard model gauge group from helix']}
    (BASE/'results'/'results.json').write_text(json.dumps(js,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return js


def main():
    data=generate_results()
    suite=unittest.defaultTestLoader.discover(str(BASE/'tests'),pattern='test_*.py')
    from io import StringIO
    buffer=StringIO()
    result=unittest.TextTestRunner(stream=buffer,verbosity=2).run(suite)
    report=buffer.getvalue()
    (BASE/'results'/'test_log.txt').write_text(report,encoding='utf-8')
    print(report)
    print('Model conclusion: sign(n) invisible to scalar potential; 4D chiral index changes sign.')
    print('Model conclusion: near-critical flux minimum has light radion and large parameter sensitivity.')
    print('Conditional brane matter coupling: alpha =',data['illustrative_vacuum_n3']['conditional_scalar_force_alpha'])
    print('WARNING: Tests confirm math and software; unification and experimental fit NOT established.')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
