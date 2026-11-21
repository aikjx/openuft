"""V131 acceptance: SHA256 integrity, new unit tests, optional preserved V130 unit tests."""
from __future__ import annotations
import argparse, hashlib, pathlib, subprocess, sys, tempfile, zipfile
ROOT=pathlib.Path(__file__).resolve().parent

def verify_hashes():
    file=ROOT/'SHA256SUMS.txt'
    rows=[line.rstrip('\n') for line in file.read_text(encoding='utf-8').splitlines() if line.strip()]
    seen=set()
    for row in rows:
        digest,rel=row.split('  ',1)
        path=ROOT/rel
        if not path.is_file():raise RuntimeError('missing: '+rel)
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=digest:raise RuntimeError('sha mismatch: '+rel)
        seen.add(rel)
    all_names={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'}
    if seen!=all_names:raise RuntimeError('manifest differs: '+str(all_names^seen))
    print('SHA-256 verified for',len(rows),'files')

def run_tests():
    subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],check=True)

def run_v130():
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ROOT/'history'/'ROOT_V130_original.zip') as z:
            if z.testzip() is not None:raise RuntimeError('corrupt historic archive')
            z.extractall(tmp)
        subprocess.run([sys.executable,'-m','unittest','discover','-s',str(pathlib.Path(tmp)/'ROOT_V130'/'tests'),'-v'],check=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--with-v130',action='store_true',help='also verify historic V130 tests')
    args=ap.parse_args()
    verify_hashes();run_tests()
    if args.with_v130:run_v130()
    print('V131 acceptance PASSED', '(plus V130)' if args.with_v130 else '')
