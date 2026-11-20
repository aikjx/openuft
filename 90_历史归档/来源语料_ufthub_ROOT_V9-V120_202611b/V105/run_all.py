from src.symbolic import run as symbolic
from src.generate import run as generate
import unittest, json

if __name__=='__main__':
    tests=unittest.defaultTestLoader.discover('tests')
    result=unittest.TextTestRunner(verbosity=1).run(tests)
    if not result.wasSuccessful():raise SystemExit(1)
    sym=symbolic()
    report=generate()
    print('ROOT V105 TESTED',result.testsRun,'unittest,',len(sym),'symbolic; SU2 trace',report['su2_wilson_trace'])
