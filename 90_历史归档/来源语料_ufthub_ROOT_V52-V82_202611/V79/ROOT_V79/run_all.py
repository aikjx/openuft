"""Reproduce tests and numeric outputs, transparently report optional skips."""
import json, os, subprocess, sys, pathlib, importlib.util
ROOT=pathlib.Path(__file__).resolve().parent

def run(title,*args,optional=False):
    print('\n###',title,flush=True)
    x=subprocess.run([sys.executable,*args],cwd=ROOT,check=False)
    if x.returncode: raise SystemExit(f'{title} failed: {x.returncode}')

run('Python standard-library unit tests','-m','unittest','discover','-s','tests','-v')
run('Regenerate numerical datasets','-m','tools.build_data')
if importlib.util.find_spec('sympy'):
    run('Optional SymPy identities','-m','tools.symbolic_check')
else:print('SKIP: SymPy absent, not counted as passed')
if os.environ.get('RUN_BROWSER','0')=='1':
    if importlib.util.find_spec('playwright'):
        run('Optional Chromium interactions','-m','tools.browser_check')
    else:print('SKIP: Playwright absent, not counted as passed')
else:print('SKIP: browser intentionally not rerun (set RUN_BROWSER=1)')
print('All mandatory executions finished. Code checks do not demonstrate new physics.')
