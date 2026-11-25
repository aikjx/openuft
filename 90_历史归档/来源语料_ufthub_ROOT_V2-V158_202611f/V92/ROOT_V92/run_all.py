import json,unittest
import numpy as np
from src.quantum import phases,density,negativity,delta_phase,pure_negativity,classical_shared_phase_mixture
suite=unittest.defaultTestLoader.discover('tests');result=unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():raise SystemExit(1)
p=phases(); rows=[]
for visibility in [0,0.25,0.5,0.75,1]:
 rho=density(p,visibility)
 rows.append({'visibility':visibility,'negativity':negativity(rho),'purity':float(np.trace(rho@rho).real)})
out={'parameters_SI':{'m1_kg':1e-14,'m2_kg':1e-14,'r_m':2e-4,'d_m':1e-5,'t_s':1},'nonlocal_phase_rad':delta_phase(p),'pure_negativity':pure_negativity(p),'classical_shared_random_phase_negativity':negativity(classical_shared_phase_mixture()),'visibility_scan':rows,'tests_passed':result.testsRun}
with open('results/summary.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
