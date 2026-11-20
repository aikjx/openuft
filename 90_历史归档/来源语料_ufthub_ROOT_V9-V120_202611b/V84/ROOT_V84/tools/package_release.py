"""Reproducible package/manifest creation, no network access."""
from pathlib import Path
import csv,hashlib,json,zipfile,shutil,subprocess,sys,os
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'ROOT_V84_多距离引力调制_有限尺寸第五力_假信号反例_可复现科研包.zip'
EXCLUDED={'SHA256_MANIFEST.csv'}

def files():
    return [p for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(x in {'__pycache__','.pytest_cache'} for x in p.parts) and p.name not in EXCLUDED and not p.name.endswith('.pyc')]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def manifest():
    with (ROOT/'SHA256_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['relative_path','size_bytes','sha256'])
        for p in files():w.writerow([p.relative_to(ROOT).as_posix(),p.stat().st_size,sha(p)])

def make_zip():
    manifest()
    with zipfile.ZipFile(DEST,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in files()+[ROOT/'SHA256_MANIFEST.csv']:
            z.write(p,arcname='ROOT_V84/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(DEST) as z:
        bad=z.testzip();assert bad is None,f'bad ZIP entry {bad}'
    return DEST

if __name__=='__main__':
    z=make_zip();print(z);print('ZIP bytes=',z.stat().st_size)
