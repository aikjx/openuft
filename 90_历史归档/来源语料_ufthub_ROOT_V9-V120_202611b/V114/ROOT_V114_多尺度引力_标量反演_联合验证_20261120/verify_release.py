"""Verify ROOT V114 release manifest, research outputs and test suites.

Usage:
  python verify_release.py              # full Python tests + historical V113 regression
  python verify_release.py --browser    # also execute optional Chromium E2E
  python verify_release.py --quick      # checks only the immutable file inventory

This script never modifies the tracked source or reference screenshot.
"""
from __future__ import annotations
import csv,hashlib,json,sys,subprocess,zipfile,tempfile,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha256(p:Path)->str:
    digest=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):digest.update(c)
    return digest.hexdigest()

def checked_run(args,cwd):
    print('+',*map(str,args),'cwd=',cwd)
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=120)
    print((p.stdout or '')[-2000:])
    if p.returncode:
        print((p.stderr or '')[-1500:])
        raise RuntimeError('Subprocess failed with '+str(p.returncode))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--browser',action='store_true')
    opt=parser.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['root_unification_solved'] is False
    tracked=manifest['files']
    for ent in tracked:
        path=ROOT/ent['path']
        assert path.is_file(),ent['path']
        assert path.stat().st_size==ent['bytes'],ent['path']
        assert sha256(path)==ent['sha256'],ent['path']
    assert (ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()[0].split()[0]==sha256(ROOT/'MANIFEST.json')
    with (ROOT/'ledger/V114_ALL_396_PRESERVED.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==396 and len({row['canonical_id'] for row in rows})==396
    with zipfile.ZipFile(ROOT/'archive/ROOT_V113_original.zip') as z:
        assert z.testzip() is None
        original_file=next(n for n in z.namelist() if n.endswith('ledger/V113_ALL_396_PRESERVED.csv'))
        assert (ROOT/'ledger/V114_ALL_396_PRESERVED.csv').read_bytes()==z.read(original_file)
    print('PASS: SHA-256 files=',len(tracked),'historical issues=',len(rows),'V113 preserved')
    if not opt.quick:
        checked_run([sys.executable,'-m','pytest','tests/test_v114.py','-q'],ROOT)
        old=json.loads((ROOT/'results/V114_RESULTS.json').read_text(encoding='utf-8'))
        checked_run([sys.executable,'run_all.py'],ROOT)
        assert json.loads((ROOT/'results/V114_RESULTS.json').read_text(encoding='utf-8'))==old
        print('PASS: reproducible JSON recomputation')
        with tempfile.TemporaryDirectory(prefix='root_v114_legacy_') as d:
            with zipfile.ZipFile(ROOT/'archive/ROOT_V113_original.zip') as z:
                z.extractall(d)
            old_project=Path(d)/'ROOT_V113_五维标量_精密引力_四力统一攻坚_20261120'
            checked_run([sys.executable,'-m','pytest','tests/test_v113.py','-q'],old_project)
        if opt.browser:
            checked_run([sys.executable,'tests/browser_smoke.py'],ROOT)
        print('PASS: V114 and historical V113 tests')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print('FAIL:',repr(exc));sys.exit(1)
