"""Reproducible standard-library tests. No claim of new physics validation."""
from pathlib import Path
import unittest,io,json,sys,platform,datetime
ROOT=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
output=io.StringIO();r=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
(ROOT/'results/test_log.txt').write_text(output.getvalue(),encoding='utf-8')
report={'project':'ROOT V69','run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(), 'tests_run':r.testsRun,
        'passed':r.testsRun-len(r.failures)-len(r.errors)-len(r.skipped),
        'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),
        'status':'PASS' if r.wasSuccessful() else 'FAIL',
        'scientific_claim':'TEST PASS verifies code implementing declared approximations, not four-force unification.'}
(ROOT/'results/verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if r.wasSuccessful() else 1)
