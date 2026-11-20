from pathlib import Path
import sys,subprocess,argparse,json,os
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--regenerate',action='store_true');ap.add_argument('--historical',action='store_true');args=ap.parse_args()
    required=['src/v98_core.py','src/coil_model.py','results/NUMERICAL_SUMMARY_THEORY.json','web/index.html']
    for r in required:
        if not (ROOT/r).is_file():raise SystemExit('Missing: '+r)
    if not args.regenerate and (ROOT/'CHECKSUMS.sha256').exists():
        subprocess.run([sys.executable,'verify_checksums.py'],cwd=ROOT,check=True)
    actions=[['python','src/symbolic_audit.py'],[sys.executable,'-m','unittest','discover','-s','tests','-v']]
    if args.regenerate:actions.insert(0,[sys.executable,'src/generate_v98.py'])
    for command in actions:
        if command[0]=='python': command[0]=sys.executable
        print('RUN',command,flush=True)
        subprocess.run(command,cwd=ROOT,check=True)
    if args.historical:
        import tempfile,zipfile
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(ROOT/'archive'/'ROOT_V97_original.zip') as zf:zf.extractall(td)
            paths=list(Path(td).rglob('test_v97.py'))
            if not paths:raise SystemExit('Missing V97 tests inside archive')
            root=paths[0].parents[1]
            print('HISTORICAL ROOT',root,flush=True)
            subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_v97.py'],cwd=root,check=True,env={**os.environ,'PYTHONPATH':str(root/'src')})
    print('ACCEPTED: current model numerical tests and mathematical checks; not full theory unification.',flush=True)

if __name__=='__main__':main()
