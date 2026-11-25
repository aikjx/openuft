"""Independent deterministic sample-based numerical cross-check (not an experiment)."""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v152.core import *
rng=np.random.default_rng(20261125)
max_err={'orthogonality':0.0,'maxwell_eom_boost':0.0,'maxwell_gauge':0.0,
         'linearized_einstein_boost':0.0,'spin2_curvature_gauge':0.0,
         'spin2_curvature_lorentz':0.0}
N=256
for _ in range(N):
    n=unit(rng.standard_normal(3))
    f=float(rng.uniform(.5,2.5))
    boost=lorentz_boost_x(float(rng.uniform(-.7,.7)))
    e1,e2,n=orthonormal_frame(n)
    max_err['orthogonality']=max(max_err['orthogonality'],float(np.max(np.abs(np.array([e1,e2,n])@np.array([e1,e2,n]).T-np.eye(3)))))
    k,a=photon_amplitude(f,n,1)
    F=field_strength_fourier(k,a)
    kt=transform_covector(boost,k)
    Ft=transform_cov2(boost,F)
    max_err['maxwell_eom_boost']=max(max_err['maxwell_eom_boost'],float(np.max(np.abs(maxwell_fourier_residual(kt,Ft)))))
    max_err['maxwell_gauge']=max(max_err['maxwell_gauge'],float(np.max(np.abs(F-field_strength_fourier(k,a+(0.2+.3j)*k)))))
    kg,h=spin2_tt_amplitude(n,2,f)
    ht=transform_cov2(boost,h)
    kgt=transform_covector(boost,kg)
    max_err['linearized_einstein_boost']=max(max_err['linearized_einstein_boost'],float(np.max(np.abs(linearized_einstein(kgt,ht)))))
    xi=rng.standard_normal(4)
    base=linearized_riemann(kg,h)
    max_err['spin2_curvature_gauge']=max(max_err['spin2_curvature_gauge'],float(np.max(np.abs(base-linearized_riemann(kg,h+spin2_gauge_shift(kg,xi))))))
    max_err['spin2_curvature_lorentz']=max(max_err['spin2_curvature_lorentz'],float(np.max(np.abs(transform_cov4(boost,base)-linearized_riemann(kgt,ht)))))
result={'seed':20261125,'trials':N,'maximum_absolute_residuals':max_err,'pass':all(v<2e-12 for v in max_err.values()),
 'interpretation':'Deterministic randomized mathematical tests, not observational confirmation.'}
(ROOT/'results'/'stress_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
if not result['pass']:sys.exit(1)
