"""Reproduce complete V101 new results in a fresh unzipped directory."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent

def run(*args):
    print('RUN',*args,flush=True)
    subprocess.run([sys.executable,*args],cwd=R,check=True)

if __name__=='__main__':
    run('src/build_ledger.py')
    run('src/generate_results.py')
    run('src/symbolic_checks.py')
    run('-m','pytest','-q','tests/test_v101.py')
    print('ROOT V101 new tests and numerical regeneration PASS.\n'
          'Historical V100 source is archived unchanged; see README for its tests.')
