"""Regenerate all reports and fail if any actual test fails."""
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
for action in [[sys.executable,'build_catalog.py'],[sys.executable,'experiments.py'],[sys.executable,'-m','unittest','discover','-s','tests','-v']]:
    result=subprocess.run(action,cwd=here,check=False)
    if result.returncode:sys.exit(result.returncode)
print('ROOT V72 complete: all executed stages passed (NOT a four-force proof).')
