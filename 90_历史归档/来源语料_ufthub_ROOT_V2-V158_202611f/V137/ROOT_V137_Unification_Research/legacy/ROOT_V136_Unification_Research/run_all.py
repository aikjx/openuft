"""Run preserved V135 tests and new V136 tests, then regenerate V136 outputs."""
import pathlib,subprocess,sys
base=pathlib.Path(__file__).resolve().parent
steps=[([sys.executable,'run_all.py'],base/'legacy'/'ROOT_V135_Unified_Field_Research'),
       ([sys.executable,'-m','unittest','discover','-s','tests','-v'],base),
       ([sys.executable,'src/v136_analysis.py'],base)]
for cmd,cwd in steps:
    print('RUN:', ' '.join(map(str,cmd)), 'in',cwd,flush=True)
    proc=subprocess.run(cmd,cwd=cwd)
    if proc.returncode:
        print('FAIL:',proc.returncode)
        raise SystemExit(proc.returncode)
print('PASS: numerical/mathematical tests only. No raw observational validation or unified theory proof.')
