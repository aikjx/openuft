#!/usr/bin/env python3
"""Run ROOT V145 audit using standard library only. Offline and deterministic."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from root_v145.analysis import main
if __name__=='__main__':
    report=main(ROOT/'results')
    print('ROOT V145 consistency audit')
    print('n=3: zero modes:',report['n3_zero_modes'])
    print('n=3: first massive gap (R=1e-18m): %.8f GeV'%report['n3_first_massive_gap_GeV_if_R_1e_minus18m'])
    print('flux max integral error:',report['max_abs_integral_error'])
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    outcome=unittest.TextTestRunner(verbosity=2).run(suite)
    print('Pass:',outcome.testsRun-len(outcome.failures)-len(outcome.errors),'/',outcome.testsRun)
    sys.exit(0 if outcome.wasSuccessful() else 1)
