"""Rebuild the ZIP + manifest from the project working tree."""
import csv,hashlib,io,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parent
path=root.parent/'ROOT_V74_统一场论严格攻坚_曲率_手性_四力审计全链路科研包.zip'
entries=[]
for p in sorted(root.rglob('*')):
    if not p.is_file():continue
    rp=p.relative_to(root).as_posix()
    if rp=='SHA256_MANIFEST.csv' or '__pycache__' in p.parts or p.suffix=='.pyc':continue
    entries.append((rp,p))
manifest=root/'SHA256_MANIFEST.csv'
with manifest.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
    for rp,p in entries:w.writerow([rp,hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for rp,p in entries:z.write(p,'ROOT_V74/'+rp)
    z.write(manifest,'ROOT_V74/SHA256_MANIFEST.csv')
with zipfile.ZipFile(path) as z:
    corrupt=z.testzip()
    if corrupt:raise ValueError('ZIP CRC error '+corrupt)
print('ZIP:',path,'files:',len(entries)+1,'size_bytes:',path.stat().st_size)
