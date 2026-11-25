#!/usr/bin/env python3
"""Execute V139 independently of older releases; uses Python stdlib + optional SymPy."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
commands=[
    [sys.executable,str(root/'src'/'verify.py')],
    [sys.executable,'-m','unittest','discover','-s','tests','-v'],
]
try:
    import sympy
except ImportError:
    print('SymPy not available; symbolic checks can be run after `pip install sympy`. Core checks have no dependencies.')
else:
    commands.append([sys.executable,str(root/'src'/'symbolic.py')])
for command in commands:
    print('RUN', ' '.join(command),flush=True)
    subprocess.run(command,cwd=root,check=True)
print('V139: mathematical/model tests complete. No direct experimental proof of force unification.')
