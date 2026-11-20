"""Run independent calculations, SymPy checks and all V103 tests."""
from pathlib import Path
import os,sys,json,subprocess
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT);sys.path.insert(0,str(ROOT))
from src.generate import generate
from src.symbolic import audit
r=generate(); checks=audit()
print('Numerical reconstruction:',json.dumps(r['radiation_and_power'],indent=2))
print('Symbolic / dimensional checks:',len(checks),'PASS')
p=subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT)
if p.returncode:raise SystemExit(p.returncode)
print('V103: CONDITIONAL THEORY ONLY; NOT COMPLETE FIELD UNIFICATION')
