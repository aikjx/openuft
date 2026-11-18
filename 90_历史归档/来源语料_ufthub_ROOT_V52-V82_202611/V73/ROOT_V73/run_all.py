"""Standard reproducibility entry point."""
import subprocess,sys,os,json
from pathlib import Path
root=Path(__file__).resolve().parent
cmds=[['-m','unittest','discover','-s','tests','-v'],['experiments.py'],['build_catalog.py']]
if '--symbolic' in sys.argv:cmds.append(['symbolic_checks.py'])
for cmd in cmds:
 print('>',sys.executable,*cmd,flush=True)
 p=subprocess.run([sys.executable,*cmd],cwd=root)
 if p.returncode:raise SystemExit(p.returncode)
print('V73 OK: numeric tests, data generation and catalogs. Browser is checked separately by browser_smoke.py.')
