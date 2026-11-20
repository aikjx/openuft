"""Fully offline ROOT V88 reproduction: math -> datasets -> integrity checks."""
import os,sys,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def go(args):
 print('RUN:', ' '.join(args),flush=True)
 p=subprocess.run(args,cwd=ROOT,check=True)
 return p.returncode

def main():
 go([sys.executable,'-m','unittest','discover','-s','tests','-v'])
 go([sys.executable,'tests/symbolic_checks.py'])
 go([sys.executable,'scripts/generate_results.py'])
 for f in ['results/numerical_summary.json','results/dephasing_threshold.png','data/dephasing_scan_SYNTHETIC.csv','web/index.html']:
  if not (ROOT/f).is_file():raise RuntimeError('missing '+f)
 print('ROOT V88 tests and regeneration SUCCESS',flush=True)
if __name__=='__main__':main()
