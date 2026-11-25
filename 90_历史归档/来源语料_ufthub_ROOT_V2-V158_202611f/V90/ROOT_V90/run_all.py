import unittest
from test_root_v90 import TestV90
suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestV90)
res=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if res.wasSuccessful() else 1)
