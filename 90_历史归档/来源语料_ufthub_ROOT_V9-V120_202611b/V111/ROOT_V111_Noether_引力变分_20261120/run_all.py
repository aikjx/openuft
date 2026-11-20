"""Run numerical and symbolic regeneration then all tests, without overwriting browser evidence."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
for cmd in ([sys.executable,'-m','src.generate'],[sys.executable,'-m','src.symbolic_audit'],[sys.executable,'-m','src.gravity_metric'],[sys.executable,'-m','pytest','-q','tests/test_v111.py']):
    print('Running',cmd,flush=True)
    subprocess.run(cmd,cwd=root,check=True)
print('V111 regeneration and tests PASS')
