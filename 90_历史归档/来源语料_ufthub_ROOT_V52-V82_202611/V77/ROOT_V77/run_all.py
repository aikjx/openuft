"""One-command reproducibility suite (core requires standard Python 3.10+ only)."""
from pathlib import Path
import subprocess,sys,json,datetime
BASE=Path(__file__).resolve().parent
commands=[('unittest',[sys.executable,'-m','unittest','discover','-s','tests','-v']),
          ('numerics',[sys.executable,'scripts/numerics.py'])]
try:
    import sympy
    commands.append(('symbolic',[sys.executable,'scripts/symbolic_checks.py']))
except ImportError:
    pass
commands.append(('catalog',[sys.executable,'scripts/build_catalog.py']))
results={}
for name,cmd in commands:
    done=subprocess.run(cmd,cwd=BASE,capture_output=True,text=True)
    results[name]={'exit_code':done.returncode,'stdout_tail':done.stdout[-900:], 'stderr_tail':done.stderr[-1300:]}
    print(f'{name}:', 'PASSED' if done.returncode==0 else 'FAILED')
    if done.returncode:
        print(done.stdout);print(done.stderr)
(BASE/'results/verification_report.json').write_text(json.dumps({'commands':results,'all_passed':all(x['exit_code']==0 for x in results.values()),
   'scope':'software and symbolic checks only; not independent physical measurement',
   'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2,ensure_ascii=False),encoding='utf-8')
if not all(x['exit_code']==0 for x in results.values()):sys.exit(1)
