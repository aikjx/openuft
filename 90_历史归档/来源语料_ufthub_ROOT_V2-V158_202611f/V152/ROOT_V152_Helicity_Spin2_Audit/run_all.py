import sys, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
jobs=[['python','-m','unittest','discover','-s','tests','-v'],['python','symbolic_audit.py'],['python','stress_audit.py'],['python','generate_results.py']]
for job in jobs:
    cmd=[sys.executable]+job[1:]
    print('RUN:', ' '.join(cmd),flush=True)
    ret=subprocess.run(cmd,cwd=ROOT,check=False)
    if ret.returncode: sys.exit(ret.returncode)
print('ALL COMPUTATIONAL CHECKS PASSED; this is NOT a proof of physical unification.')
