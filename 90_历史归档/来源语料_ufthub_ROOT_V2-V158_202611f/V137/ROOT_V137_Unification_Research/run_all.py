"""Full V137 + legacy V136 + V135 regression and report, stdlib only."""
import subprocess,sys,pathlib
root=pathlib.Path(__file__).resolve().parent
commands=[([sys.executable,'run_all.py'],root/'legacy'/'ROOT_V136_Unification_Research'),
          ([sys.executable,'-m','unittest','discover','-s','tests','-p','test_v137.py','-v'],root),
          ([sys.executable,'src/v137_analysis.py'],root)]
for idx,(command,cwd) in enumerate(commands,1):
    print(f'\n=== ROOT V137 ({idx}/{len(commands)}): {" ".join(command)} ===',flush=True)
    p=subprocess.run(command,cwd=cwd,check=False)
    if p.returncode:
        print('FAILED phase',idx,file=sys.stderr)
        sys.exit(p.returncode)
print('\nALL PHASES PASSED. NOTE: software tests are not observational verification.')
