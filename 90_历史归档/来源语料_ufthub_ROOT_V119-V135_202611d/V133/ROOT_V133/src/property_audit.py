#!/usr/bin/env python3
"""Reproducible randomized property checks; not experiment or theorem discovery."""
from pathlib import Path
import json,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import root_v133 as M
rng=np.random.default_rng(20261121)
N=10000
max_error={'geometric_relative':0.0,'boost_inversion_absolute':0.0,'joint_gauge_absolute':0.0,'charge_tower_relative':0.0}
for i in range(N):
    u=float(rng.uniform(-.99,.99));w=float(np.exp(rng.uniform(-4,3)))
    a=M.helix_geometry(u,w)
    er=abs(a['kappa']**2+a['torsion']**2-w*w)/w**2
    max_error['geometric_relative']=max(max_error['geometric_relative'],er)
    beta=float(rng.uniform(-.95,.95))
    new=M.boost_axis_velocity(M.boost_axis_velocity(u,beta),-beta)
    max_error['boost_inversion_absolute']=max(max_error['boost_inversion_absolute'],abs(new-u))
    th,omega,A,lam,chi,Lambdadot=rng.uniform(-2,2,size=6)
    old=M.internal_covariant_rate(th,omega,A,lam)
    anew=M.internal_covariant_rate(th+chi-lam*Lambdadot,omega-chi,A+Lambdadot,lam)
    max_error['joint_gauge_absolute']=max(max_error['joint_gauge_absolute'],abs(old-anew))
    n=int(rng.integers(1,11)); I=10*M.HBAR_SI
    lam0=M.lambda_for_alpha(1/M.ALPHA_INV_0)
    rr=M.rotor_spectrum(n,I,lam0,0)
    base=M.rotor_spectrum(1,I,lam0,0)
    er=abs(rr['alpha']/base['alpha']-n*n)/(n*n)
    max_error['charge_tower_relative']=max(max_error['charge_tower_relative'],er)
limits={'geometric_relative':3e-14,'boost_inversion_absolute':5e-14,'joint_gauge_absolute':1e-14,'charge_tower_relative':3e-14}
passed=all(max_error[k]<limits[k] for k in max_error)
report={'seed':20261121,'random_parameter_trials':N,'max_residuals':max_error,'acceptance_limits':limits,'passed':passed,'notes':'Numerical property samples, not 10000 independent physics tests; no real observation was used.'}
out=Path(__file__).resolve().parents[1]/'results'/'property_audit.json'
out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2))
if not passed:raise SystemExit(1)
