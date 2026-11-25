"""Deterministic boosts/rotations: 256 numerical covariance stress examples."""
import json
from pathlib import Path
import numpy as np
from src.physics import *

rng=np.random.default_rng(153)
max_F=0.; max_R=0.; max_puregauge_F=0.; max_puregauge_R=0.
for _ in range(256):
    beta=float(rng.uniform(-.95,.95))
    omega=float(10**rng.uniform(-2,2))
    k=k_lower(omega)
    e1,e2=vector_physical_modes()
    a=rng.normal()*e1+rng.normal()*e2
    h=spin2_tt(float(rng.normal()), float(rng.normal()))
    xi=rng.normal(size=4)
    gauge_scalar=float(rng.normal())
    S=lorentz_cov(beta)
    Ft=maxwell_field(k,a)
    Fprime=maxwell_field(S@k,S@a)
    max_F=max(max_F,np.linalg.norm(Fprime-S@Ft@S.T)/(1+np.linalg.norm(Fprime)))
    R=linear_riemann(k,h)
    Rp=linear_riemann(S@k,S@h@S.T)
    R_expected=transform_rank4_cov(R,S)
    max_R=max(max_R,np.linalg.norm(Rp-R_expected)/(1+np.linalg.norm(Rp)))
    max_puregauge_F=max(max_puregauge_F, np.max(np.abs(maxwell_field(k,gauge_scalar*k))))
    max_puregauge_R=max(max_puregauge_R,np.max(np.abs(linear_riemann(k,spin2_pure_gauge(k,xi))))/(1+omega**3*np.linalg.norm(xi)))
assert max_F<1e-12
assert max_R<1e-12
assert max_puregauge_F<1e-12
assert max_puregauge_R<1e-12
report={'random_seed':153,'samples':256,
 'max_relative_F_covariance_error':max_F,'max_relative_R_covariance_error':max_R,
 'max_abs_F_pure_gauge':max_puregauge_F,'max_relative_R_pure_gauge':max_puregauge_R}
Path(__file__).resolve().parent.joinpath('results','stress.json').write_text(json.dumps(report,indent=2)+'\n')
print('STRESS AUDIT OK:',report)
