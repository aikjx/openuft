"""Reproducible release ZIP, per-file SHA256, archive verification and extract test."""
from __future__ import annotations
import hashlib,json,subprocess,sys,zipfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'ROOT_V66_统一场论全维求导证明精算与研究总集.zip'

def sha256(path):
    s=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):s.update(c)
    return s.hexdigest()

def filelist():
    return sorted((p for p in ROOT.rglob('*') if p.is_file() and p.name!='FILE_SHA256_MANIFEST.txt'
                   and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts),key=lambda p:str(p))

def main():
    entries=[]
    for p in filelist():
        entries.append((str(p.relative_to(ROOT)).replace('\\','/'),sha256(p)))
    manifest=ROOT/'FILE_SHA256_MANIFEST.txt'
    manifest.write_text('# ROOT V66 SHA-256; manifest itself intentionally excluded\n'+'\n'.join(f'{d}  {n}' for n,d in entries)+'\n',encoding='utf-8')
    with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
        for p in [manifest]+filelist():
            rel=p.relative_to(ROOT)
            z.write(p,arcname=str(Path('ROOT_V66')/rel))
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None,'zip corruption'
        names=set(z.namelist())
        for name,digest in entries:
            assert 'ROOT_V66/'+name in names
            assert hashlib.sha256(z.read('ROOT_V66/'+name)).hexdigest()==digest,name
        assert len(names)==len(entries)+1
    print('ZIP',OUT)
    print('COUNT',len(entries)+1,'BYTES',OUT.stat().st_size)
    print('SHA256',sha256(OUT))
    (ROOT.parent/'ROOT_V66_压缩包SHA256.txt').write_text(f'{sha256(OUT)}  {OUT.name}\n',encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='v66_zip_test_') as tmp:
        with zipfile.ZipFile(OUT) as z:z.extractall(tmp)
        unzipped=Path(tmp)/'ROOT_V66'
        r=subprocess.run([sys.executable,'run_all.py'],cwd=unzipped,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        print('EXTRACTED_RUN',r.stdout.strip()[-800:])
        if r.returncode!=0:raise SystemExit(f'extracted run failed: {r.stdout[-2000:]}')
    print('RELEASE VERIFIED')
if __name__=='__main__':main()
