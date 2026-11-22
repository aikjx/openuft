#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic randomized mathematical property checks; not physical measurements."""
from pathlib import Path
import sys
import json
import numpy as np
from scipy.linalg import expm
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_v134 import SU2,SU3,commutator,curvature_constant,pure_gauge_connection,su2_color

def run(seed=13420261121,samples=1000):
    rng=np.random.default_rng(seed)
    maxima={'pure_gauge_F_norm':0.,'SU2_covariance_norm':0.,'SU3_covariance_norm':0.,
            'SU2_casimir_transform_error':0.,'SU2_bianchi_jacobi_norm':0.}
    for _ in range(samples):
        a,b,x=rng.uniform(-3,3,3)
        F=pure_gauge_connection(x,a,b)[-1]
        maxima['pure_gauge_F_norm']=max(maxima['pure_gauge_F_norm'],float(np.linalg.norm(F)))
        for name,generators in [('SU2',SU2),('SU3',SU3)]:
            n=len(generators)
            coeff=rng.normal(size=n)
            transform=expm(1j*sum((c*t for c,t in zip(coeff,generators)),np.zeros_like(generators[0])))
            ax=sum((c*t for c,t in zip(rng.normal(size=n),generators)),np.zeros_like(generators[0]))
            ay=sum((c*t for c,t in zip(rng.normal(size=n),generators)),np.zeros_like(generators[0]))
            target=transform@curvature_constant(ax,ay)@transform.conj().T
            actual=curvature_constant(transform@ax@transform.conj().T,transform@ay@transform.conj().T)
            key=f'{name}_covariance_norm'
            maxima[key]=max(maxima[key],float(np.linalg.norm(actual-target)))
        z=rng.normal(size=2)+1j*rng.normal(size=2); z=z/np.linalg.norm(z)
        U=expm(1j*sum((c*t for c,t in zip(rng.normal(size=3),SU2)),np.zeros((2,2),complex)))
        q=su2_color(z);qnew=su2_color(U@z)
        maxima['SU2_casimir_transform_error']=max(maxima['SU2_casimir_transform_error'],abs(np.dot(q,q)-np.dot(qnew,qnew)))
        A,B,C=[sum((c*t for c,t in zip(rng.normal(size=3),SU2)),np.zeros((2,2),complex)) for _ in range(3)]
        Jac=commutator(A,commutator(B,C))+commutator(B,commutator(C,A))+commutator(C,commutator(A,B))
        maxima['SU2_bianchi_jacobi_norm']=max(maxima['SU2_bianchi_jacobi_norm'],float(np.linalg.norm(Jac)))
    tolerance=1e-11
    if any(v>tolerance for v in maxima.values()):raise AssertionError(maxima)
    return dict(seed=seed,samples=samples,properties_per_sample=5,total_checked=samples*5,
                tolerance=tolerance,max_residuals=maxima,
                conclusion='All synthetic mathematical properties passed; no experimental claim')

if __name__=='__main__':
    result=run()
    out=Path(__file__).resolve().parents[1]/'results'/'random_property_audit.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
