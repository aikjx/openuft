"""ROOT V68 test runner. Basic library tests only; never claims theoretical proof."""
import io,unittest,json,datetime,sys,platform
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
suite=unittest.defaultTestLoader.discover(str(root/'tests'),pattern='test_*.py')
out=io.StringIO();result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
(root/'results/test_log.txt').write_text(out.getvalue(),encoding='utf-8')
report={'project':'ROOT V68','date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'python':platform.python_version(),'tests_run':result.testsRun,'failures':len(result.failures),
'errors':len(result.errors),'skipped':len(result.skipped),
'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
'status':'PASS' if result.wasSuccessful() else 'FAIL',
'science_status':'OPEN: no independent G prediction, no four-force unification proof, no new experimental support',
'claim':'Tests check equations and implementation under explicit assumptions, not actual physical validity.'}
(root/'results/verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if result.wasSuccessful() else 1)
