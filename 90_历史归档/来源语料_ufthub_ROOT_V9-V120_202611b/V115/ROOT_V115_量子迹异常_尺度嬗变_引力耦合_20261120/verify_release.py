"""ROOT V115 reproducible integrity verification. Run from any directory:
python verify_release.py            # SHA/manifest, 396 issues, nested historical ZIP
python verify_release.py --deep     # plus new tests, history tests, offline Chromium, independent JSON
"""
import argparse,hashlib,json,csv,subprocess,sys,zipfile,tempfile,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=160)
    result='PASS' if p.returncode==0 else 'FAIL'
    print(result,' '.join(map(str,args)))
    if p.returncode!=0:
        print(p.stdout[-2000:]);print(p.stderr[-2000:])
        raise RuntimeError('command failed')
    return p.stdout

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--deep',action='store_true');opts=ap.parse_args()
    man=json.loads((BASE/'MANIFEST.json').read_text(encoding='utf-8'))
    checksum_lines=(BASE/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
    assert checksum_lines[0].split()[0]==sha(BASE/'MANIFEST.json')
    for record in man['files']:
        path=BASE/record['path'];assert path.is_file(),path
        assert path.stat().st_size==record['bytes'],path
        assert sha(path)==record['sha256'],path
    assert len(checksum_lines)==len(man['files'])+1
    print('PASS SHA256 verified files:',len(man['files']))
    with (BASE/'ledger/V115_ALL_396_PRESERVED.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==396 and len({x['canonical_id'] for x in rows})==396
    print('PASS unique historical tasks:',len(rows))
    zpath=BASE/'archive/ROOT_V114_original.zip'
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None
        print('PASS nested historical ZIP:',len(z.namelist()),'members')
    if opts.deep:
        run([sys.executable,'-m','pytest','tests/test_v115.py','-q'],BASE)
        run([sys.executable,'tests/browser_smoke.py'],BASE)
        with tempfile.TemporaryDirectory(prefix='root_v115_replay_') as temp:
            temp=Path(temp)
            current=temp/'v115';current.mkdir()
            shutil.copytree(BASE/'src',current/'src',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(BASE/'run_all.py',current/'run_all.py')
            run([sys.executable,'run_all.py'],current)
            archived=json.loads((BASE/'results/V115_NUMERICAL_SUMMARY.json').read_text())
            replay=json.loads((current/'results/V115_NUMERICAL_SUMMARY.json').read_text())
            assert archived==replay
            print('PASS independent regenerated JSON exactly identical')
            with zipfile.ZipFile(zpath) as z: z.extractall(temp/'v114hist')
            histdirs=[p for p in (temp/'v114hist').iterdir() if p.is_dir()]
            assert len(histdirs)==1
            run([sys.executable,'-m','pytest','tests/test_v114.py','-q'],histdirs[0])
    print('PASS ROOT V115 validation (not a proof of physics novelty)')

if __name__=='__main__':main()
