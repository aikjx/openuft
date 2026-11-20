from pathlib import Path
import argparse,subprocess,sys,tempfile,zipfile,os
ROOT=Path(__file__).resolve().parent

def cmd(*args,cwd=ROOT,env=None):
    print('RUN:',*args,flush=True)
    subprocess.run(list(args),cwd=cwd,env=env,check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--regenerate',action='store_true',help='Regenerate numerical data and pictures (slow)')
    p.add_argument('--historical',action='store_true',help='Run V98 tests from original archived ZIP')
    p.add_argument('--browser',action='store_true',help='Run optional Playwright Chromium UI test')
    args=p.parse_args()
    if (ROOT/'CHECKSUMS.sha256').exists():
        cmd(sys.executable,'verify_checksums.py')
    for path in ('src/generate_v99.py','results/V99_NUMERICAL_AUDIT_THEORY.json','inputs/V98_SUMMARY.json'):
        if not (ROOT/path).exists():raise SystemExit('Missing '+path)
    if args.regenerate:
        cmd(sys.executable,'src/generate_v99.py')
        cmd(sys.executable,'src/build_web.py')
    cmd(sys.executable,'src/dimensional_audit.py')
    cmd(sys.executable,'-m','unittest','discover','-s','tests','-p','test_v99.py','-v')
    if args.historical:
        with tempfile.TemporaryDirectory(prefix='rootv98_') as td:
            with zipfile.ZipFile(ROOT/'archive/ROOT_V98_original.zip') as z:
                z.extractall(td)
            tests=list(Path(td).rglob('test_v98.py'))
            if len(tests)!=1:raise SystemExit(f'Expected 1 V98 test script, got {len(tests)}')
            old=tests[0].parents[1]
            cmd(sys.executable,'-m','unittest','discover','-s','tests','-p','test_v98.py','-v',cwd=old,env={**os.environ,'PYTHONPATH':str(old/'src')})
    if args.browser:
        cmd(sys.executable,'web/browser_smoke.py')
    print('PASS: V99 specified model checks. NOT an experimental or theory-of-everything proof.')
if __name__=='__main__':main()
