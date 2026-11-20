from pathlib import Path
import json, subprocess,sys,unittest
from src.gravitylab import generate_all
root=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(root/'tests'),pattern='test_*.py')
result=unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful(): sys.exit(1)
res=generate_all(root)
print(json.dumps({'tests_run':result.testsRun,'pass':result.wasSuccessful(),'synthetic_mass_adjusted':res['synthetic_mass_estimate']['adjusted_amplitude'],'theory':res['theory']['common_odd_amplitude'],'data_provenance':'SYNTHETIC_NOT_OBSERVED'},indent=2,ensure_ascii=False))
