"""Run tests, generate results, checksum manifest, build high-compression ZIP."""
import hashlib,pathlib,subprocess,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
DEST=ROOT.parent/'ROOT_V135_Unified_Field_Research_Complete.zip'
subprocess.run([sys.executable,str(ROOT/'run_all.py')],cwd=ROOT,check=True)

def inputs():
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
        if p.name=='SHA256SUMS.txt':continue
        yield p

records=[]
for p in inputs():
    records.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix())
(ROOT/'results/SHA256SUMS.txt').write_text('\n'.join(records)+'\n',encoding='utf-8')
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
        z.write(p,arcname=f'{ROOT.name}/{p.relative_to(ROOT).as_posix()}')
with zipfile.ZipFile(DEST,'r') as z:
    assert z.testzip() is None, 'ZIP CRC failed'
    names=z.namelist()
    assert len(names)>=23, 'incomplete package'
    assert all(n.startswith(ROOT.name+'/') for n in names), 'unexpected ZIP root'
print('PACKED:',DEST)
print('FILES:',len(names))
print('SIZE:',DEST.stat().st_size,'bytes')
print('SHA256:',hashlib.sha256(DEST.read_bytes()).hexdigest())
