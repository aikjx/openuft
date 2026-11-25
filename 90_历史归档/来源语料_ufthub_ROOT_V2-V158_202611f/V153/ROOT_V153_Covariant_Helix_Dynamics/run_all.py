"""Recreate symbolic/numeric reports and run tests. Exit nonzero on failure."""
import subprocess
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
for command in ([sys.executable,'symbolic_audit.py'],
                [sys.executable,'stress_audit.py'],
                [sys.executable,'-m','unittest','discover','-s','tests','-v']):
    print('\n$', ' '.join(command),flush=True)
    subprocess.run(command,cwd=root,check=True)
print('\nV153: all configured checks passed (model-specific mathematical tests).')
