"""One-command runner for Windows, Linux, macOS; no optional packages."""
import pathlib,subprocess,sys
base=pathlib.Path(__file__).resolve().parent
commands=[[sys.executable,'-m','unittest','discover','-s','tests','-v'],[sys.executable,'src/analysis.py'],[sys.executable,'src/audit.py']]
for cmd in commands:
    print('RUN',cmd,flush=True)
    result=subprocess.run(cmd,cwd=base)
    if result.returncode:raise SystemExit(result.returncode)
print('SUCCESS: numerical consistency tests and research outputs created (NOT experimental verification)')
