"""Deterministic-ish package builder with per-file source SHA256 manifest."""
from __future__ import annotations
import hashlib,zipfile,pathlib
HERE=pathlib.Path(__file__).resolve().parent
OUT=HERE.parent/(HERE.name+'_Complete.zip')
SKIP={'__pycache__','.pytest_cache'}
def included():
    return sorted((p for p in HERE.rglob('*')
                  if p.is_file() and not any(t in SKIP for t in p.relative_to(HERE).parts)
                  and p.suffix!='.pyc'),key=lambda p:p.as_posix())
files=included()
manifest='ROOT V137 source manifest; SHA256 raw file bytes; excludes itself.\n'
manifest+='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(HERE)).replace('\\','/') for p in files if p.relative_to(HERE).as_posix()!='SHA256SUMS.txt')+'\n'
(HERE/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8')
files=included()
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        arc=HERE.name+'/'+p.relative_to(HERE).as_posix()
        info=zipfile.ZipInfo(arc,(2026,11,23,12,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=(0o644&0xFFFF)<<16
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(OUT) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('archive CRC fail '+bad)
    if len(z.infolist())!=len(files):raise RuntimeError('archive count mismatch')
print('ZIP',OUT,'files',len(files),'bytes',OUT.stat().st_size,'sha256',hashlib.sha256(OUT.read_bytes()).hexdigest())
