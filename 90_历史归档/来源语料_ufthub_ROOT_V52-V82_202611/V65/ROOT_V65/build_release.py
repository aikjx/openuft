#!/usr/bin/env python3
"""Build reproducible ROOT V65 ZIP, verify ZIP CRC and SHA-256 of all files."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,sys
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'ROOT_V65_四力大统一理论审计_推导精算验证模拟科研包.zip'
ignore={'__pycache__','.pytest_cache','.git','.venv'}
manifest=root/'FILE_SHA256_MANIFEST.txt'
def source_files():
    for p in root.rglob('*'):
        if p.is_file() and p!=manifest and not any(s in ignore for s in p.relative_to(root).parts) and not p.name.endswith(('.pyc','.tmp','.bak')):
            yield p
files=sorted(source_files(),key=lambda p:p.relative_to(root).as_posix())
manifest.write_text('# ROOT V65 SHA256 manifest (self-excluded)\n'+''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(root).as_posix()+'\n' for f in files),encoding='utf-8')
files.append(manifest)
out.parent.mkdir(parents=True,exist_ok=True)
with ZipFile(out,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
    for f in files:
        name='ROOT_V65/'+f.relative_to(root).as_posix()
        member=ZipInfo(name,date_time=(2026,11,17,0,0,0));member.external_attr=(0o644<<16);member.compress_type=ZIP_DEFLATED
        z.writestr(member,f.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
with ZipFile(out) as z:
    if z.testzip() is not None:raise RuntimeError('ZIP CRC failed')
    if len(z.namelist())!=len(files):raise RuntimeError('ZIP file count mismatch')
    for f in files:
        name='ROOT_V65/'+f.relative_to(root).as_posix()
        if hashlib.sha256(z.read(name)).digest()!=hashlib.sha256(f.read_bytes()).digest():raise RuntimeError('SHA mismatch '+name)
s={'zip_path':str(out),'zip_size_bytes':out.stat().st_size,'file_count':len(files),
   'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
   'all_member_sha256_and_crc':'PASS',
   'physics_claim':'math/conditional models; G and four-force unification OPEN'}
(root.parent/'ROOT_V65_文件校验_SHA256.txt').write_text(s['sha256']+'  '+out.name+'\n',encoding='utf-8')
print(json.dumps(s,ensure_ascii=False,indent=2))
