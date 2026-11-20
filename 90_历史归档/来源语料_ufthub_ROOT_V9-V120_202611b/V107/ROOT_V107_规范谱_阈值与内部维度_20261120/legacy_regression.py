"""Re-run packaged V106 native tests without relying on old installation paths."""
import sys,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    with tempfile.TemporaryDirectory(prefix='root_v106_regress_') as temp:
        with zipfile.ZipFile(ROOT/'archive'/'ROOT_V106_original.zip') as z:
            z.extractall(temp)
        root=Path(temp)
        cands=list(root.rglob('run_all.py'))
        cands=[x for x in cands if (x.parent/'tests').is_dir() and (x.parent/'src'/'symbolic.py').exists()]
        assert len(cands)==1,[(str(x)) for x in cands]
        x=cands[0]
        p=subprocess.run([sys.executable,str(x)],cwd=x.parent)
        if p.returncode:raise SystemExit(p.returncode)
        print('V106 legacy regression independently passed from extracted original ZIP')

if __name__=='__main__':main()
