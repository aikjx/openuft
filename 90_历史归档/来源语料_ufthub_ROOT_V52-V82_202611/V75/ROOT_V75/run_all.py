"""Run standard-library-only 41 physics unit tests and validate data products."""
import pathlib,sys,unittest,json,csv,hashlib
root=pathlib.Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
result=unittest.TextTestRunner(verbosity=1).run(suite)
assert result.wasSuccessful(), 'unit tests failed'
assert result.testsRun == 41, f'expected 41 tests, found {result.testsRun}'
summary=json.loads((root/'results/numerical_summary.json').read_text(encoding='utf-8'))
assert summary['flags']['no_new_G_predicted']
assert summary['flags']['experimental_new_gravity_discovery'] is False
assert summary['data_rows']['magnetic_scan'] == 15
with (root/'data/ROOT_V75_核心方程与证明状态.csv').open(encoding='utf-8-sig') as f:
 assert len(list(csv.DictReader(f)))==50
with (root/'data/ROOT_V75_多维影响因素与实验控制矩阵.csv').open(encoding='utf-8-sig') as f:
 assert len(list(csv.DictReader(f)))==30
print(json.dumps({'unit_tests_passed':result.testsRun,'equations':50,'factors':30,'numerical_summary_validated':True},ensure_ascii=False))
