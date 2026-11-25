#!/usr/bin/env python3
"""Run all tests plus reproducible numerical outputs."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root)
if p.returncode:raise SystemExit(p.returncode)
p=subprocess.run([sys.executable,'symbolic_audit.py'],cwd=root)
if p.returncode:raise SystemExit(p.returncode)
p=subprocess.run([sys.executable,'generate_results.py'],cwd=root)
if p.returncode:raise SystemExit(p.returncode)
print('V151: tests + symbolic audit + results successfully reproduced (not four-force unification).')
