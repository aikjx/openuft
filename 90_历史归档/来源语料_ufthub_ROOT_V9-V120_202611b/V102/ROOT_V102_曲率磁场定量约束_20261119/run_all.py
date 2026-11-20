"""Run from any working directory: python run_all.py"""
import os,sys,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0,str(ROOT))
from src.generate_results import main
from src.symbolic_checks import audit
numerics=main()
sym=audit()
print('Symbolic checks:',len(sym),'PASS')
p=subprocess.run([sys.executable,'-m','pytest','-q',str(ROOT/'tests')],cwd=ROOT)
if p.returncode:raise SystemExit(p.returncode)
print('Numerical summary:',json.dumps({k:v for k,v in numerics.items() if k in ('B_mean_T','B_rms_T','B_knot_lower_T','E_rad_from_B_J','radiation_identity_relative')},indent=2))
print('ROOT V102 regression PASS | THEORY ONLY | NO EXPERIMENT')
