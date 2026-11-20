"""Recalculate results and run tests. All outputs are MODEL/THEORY only."""
import json, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.symbolic import run as sym_run
from src.generate import run as generate
if __name__=='__main__':
    checks=sym_run()
    test=unittest.defaultTestLoader.discover(str(ROOT/'tests'), top_level_dir=str(ROOT))
    result=unittest.TextTestRunner(verbosity=1).run(test)
    if not result.wasSuccessful():raise SystemExit(1)
    info=generate()
    print(f'ROOT V106 OK: {result.testsRun} Python unit tests, {len(checks)} symbolic checks')
    print('NONUNIFICATION invariant=',info['one_loop_invariant'])
    print('Not a four-force unification or physical experiment.')
