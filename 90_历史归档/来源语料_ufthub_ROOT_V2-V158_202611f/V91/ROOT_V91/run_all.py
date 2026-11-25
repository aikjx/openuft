import json,unittest,numpy as np
from src.design import design_search,templates,fisher
suite=unittest.defaultTestLoader.discover('tests');result=unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():raise SystemExit(1)
grid=np.linspace(.0002,.001,13);delta=1e-5
best=design_search(grid,delta,5,noise=1e-5)
T=templates(best['radii_m'],delta);T=T/np.linalg.norm(T,axis=0)
degenerate=fisher(T[:,2],T,np.eye(5)*1e-10)
output={'model':'normalized illustrative shape discrimination; not physical EFT SNR','delta_m':delta,'candidate_distances_m':grid.tolist(),'best_five':best,'identical_background':degenerate,'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}
with open('results/design.json','w') as f:json.dump(output,f,indent=2,allow_nan=False)
print(json.dumps(output,indent=2))
