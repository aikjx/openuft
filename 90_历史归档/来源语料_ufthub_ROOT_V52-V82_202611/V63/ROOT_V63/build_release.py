"""Create reproducible ROOT V63 zip and sha256 checksum from this directory."""
from pathlib import Path
import zipfile, hashlib
root=Path(__file__).resolve().parent
outfile=root.parent/'ROOT_V63_引力起源与四力统一严格审计科研包.zip'
excl=('__pycache__','.pyc','.DS_Store')
paths=sorted(p for p in root.rglob('*') if p.is_file() and not any(x in str(p) for x in excl))
with zipfile.ZipFile(outfile,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in paths:
        entry=zipfile.ZipInfo('ROOT_V63/'+p.relative_to(root).as_posix(),date_time=(2026,11,17,0,0,0))
        entry.compress_type=zipfile.ZIP_DEFLATED
        entry.external_attr=0o644<<16
        z.writestr(entry,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(outfile,'r') as z:
    assert not z.testzip()
    assert any(x.endswith('ROOT_V63/README.md') for x in z.namelist())
sha=hashlib.sha256(outfile.read_bytes()).hexdigest()
(outfile.parent/(outfile.name+'.sha256.txt')).write_text(sha+'  '+outfile.name+'\n',encoding='utf-8')
print('ZIP',outfile,'size',outfile.stat().st_size,'members',len(paths))
print('SHA256',sha)
