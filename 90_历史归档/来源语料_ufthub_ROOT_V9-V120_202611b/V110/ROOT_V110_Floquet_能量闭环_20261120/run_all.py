"""Reproduce all default ROOT V110 theoretical computations in a clean directory.
python run_all.py             -> symbolic + 52 current tests + numerical CSV/figures + manifest
python run_all.py --browser   -> also Chromium smoke when installed
python run_all.py --history   -> also unpack/run V109 archive tests (slower)
"""
import sys,subprocess,argparse,zipfile,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent

def call(args,cwd=R):
    print('RUN',args,'cwd=',cwd,flush=True)
    subprocess.run(args,cwd=cwd,check=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--browser',action='store_true');p.add_argument('--history',action='store_true');a=p.parse_args()
    call([sys.executable,'src/symbolic_audit.py'])
    call([sys.executable,'-m','pytest','-q','tests/test_v110.py'])
    call([sys.executable,'src/generate.py'])
    if a.browser:call([sys.executable,'web/browser_smoke.py'])
    if a.history:
        with tempfile.TemporaryDirectory(prefix='root_v109_history_') as dest:
            with zipfile.ZipFile(R/'archive'/'ROOT_V109_original.zip') as z:z.extractall(dest)
            dirs=list(Path(dest).glob('*/tests/test_v109.py'))
            if len(dirs)!=1: raise RuntimeError('V109 original ZIP structure unexpected: '+str(dirs))
            old=dirs[0].parents[1]
            call([sys.executable,'-m','pytest','-q','tests/test_v109.py','tests/test_independent_integrator.py'],cwd=old)
            call([sys.executable,'src/symbolic_audit.py'],cwd=old)
    call([sys.executable,'verify_integrity.py'])
    print('V110 theoretical reproduction complete; no new physics or experimental finding established.')
if __name__=='__main__':main()
