"""Execute symbolic verification, numerical benchmark and all unit tests."""
from pathlib import Path
import sys, json, unittest, io
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p))
from src.symbolic_checks import run_symbolic
from src.physics import helix_kinematics, inverse_null_helix, wave, maxwell_residuals,noether_mode_count
import numpy as np

result_dir=p/'results'
result_dir.mkdir(exist_ok=True)
sym=run_symbolic()
(result_dir/'symbolic_results.json').write_text(json.dumps(sym,ensure_ascii=False,indent=2),encoding='utf8')
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(p/'tests'),pattern='test_*.py')
res=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
log=stream.getvalue()
(result_dir/'tests.log').write_text(log,encoding='utf8')
print(log)
examples=[]
for t,z in ((0,0),(.4,.7),(1,3)):
    E,B=wave(t,z)
    ER,BR=maxwell_residuals(t,z)
    WR,WA=maxwell_residuals(t,z,magnetic_sign=-1)
    examples.append({'t':t,'z':z,'E':E.tolist(),'B':B.tolist(),
                     'poynting':np.cross(E,B).tolist(),
                     'correct_maxwell_residual_norms':[float(np.linalg.norm(ER)),float(np.linalg.norm(BR))],
                     'wrong_sign_residual_norms':[float(np.linalg.norm(WR)),float(np.linalg.norm(WA))]})
report={'study':'ROOT V142','units':'c=1; hbar and G dimensional','note':'Mathematical/model self-tests, NOT experimental proof',
        'test_count':res.testsRun,'tests_passed':res.wasSuccessful(),
        'helical_example':helix_kinematics(.6,1,.8),
        'free_field_modes':{'Maxwell':noether_mode_count(2,0),'Proca':noether_mode_count(0,2)},
        'samples':examples,'symbolic':sym}
(result_dir/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Summary saved',result_dir/'summary.json')
if not res.wasSuccessful():sys.exit(1)
