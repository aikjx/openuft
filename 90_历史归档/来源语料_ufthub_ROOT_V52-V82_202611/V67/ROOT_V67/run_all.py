"""Run tests and save a machine-readable, timestamped verification report."""
import sys,json,unittest,datetime,io,platform
from pathlib import Path
root=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(root/'tests'),pattern='test_*.py')
stream=io.StringIO()
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
text=stream.getvalue()
(root/'results').mkdir(exist_ok=True)
(root/'results'/'test_log.txt').write_text(text,encoding='utf-8')
report={'version':'ROOT V67','when_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'run':result.testsRun,'failures':len(result.failures),
 'errors':len(result.errors),'skipped':len(result.skipped),
 'passed':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
 'status':'PASS' if result.wasSuccessful() else 'FAIL',
 'methodology':'Unit tests of explicit assumed models; not a proof or experiment confirming unified field theory.'}
(root/'results'/'verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
print(text[-900:])
sys.exit(0 if result.wasSuccessful() else 1)
