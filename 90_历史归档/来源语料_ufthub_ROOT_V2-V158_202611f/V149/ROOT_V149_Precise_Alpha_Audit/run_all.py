#!/usr/bin/env python3
"""Reproduce V149 numbers, run unittests and independent SymPy audit."""
from pathlib import Path
import os,subprocess,sys
BASE=Path(__file__).resolve().parent

def run(args,env=None):
    p=subprocess.run([sys.executable,*args],cwd=BASE,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
    print(p.stdout)
    if p.returncode:raise SystemExit(f'FAILED command {args}: exit {p.returncode}')
    return p.stdout

def main():
    env=os.environ.copy();env['PYTHONPATH']=str(BASE/'src')+os.pathsep+env.get('PYTHONPATH','')
    run(['generate_results.py'],env)
    log=run(['-m','unittest','discover','-s','tests','-v'],env)
    (BASE/'results'/'unit_test_log.txt').write_text(log,encoding='utf-8')
    log2=run(['symbolic_audit.py'],env)
    (BASE/'results'/'symbolic_test_log.txt').write_text(log2,encoding='utf-8')
    print('ALL V149 TESTS PASSED; mathematical/algorithm consistency only, not experimental validation.')
if __name__=='__main__':main()
