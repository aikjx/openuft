"""Create immutable, independently verifiable ROOT V93 ZIP in parent folder."""
from pathlib import Path
from hashlib import sha256
import json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/(ROOT.name+'_正式科研包.zip')
EX={'CHECKSUMS.sha256','MANIFEST.json'}
def includes(p):return p.is_file() and p.name not in EX and '__pycache__' not in p.parts and p.suffix!='.pyc'
files=sorted((p for p in ROOT.rglob('*') if includes(p)),key=lambda p:p.relative_to(ROOT).as_posix())
meta=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in files]
(ROOT/'CHECKSUMS.sha256').write_text('\n'.join(x['sha256']+'  '+x['path'] for x in meta)+'\n',encoding='utf-8')
manifest={'project':'ROOT V93','scientific_status':'mathematically verified geometric model; not a unified field theory proof','release_date':'2026-11-18','file_count_excluding_manifest_and_checksums':len(meta),'files':meta}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in sorted([*files,ROOT/'CHECKSUMS.sha256',ROOT/'MANIFEST.json'],key=lambda p:p.relative_to(ROOT).as_posix()):
        z.write(p,arcname=f'{ROOT.name}/{p.relative_to(ROOT).as_posix()}')
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    for entry in meta:
        content=z.read(f'{ROOT.name}/{entry["path"]}')
        assert sha256(content).hexdigest()==entry['sha256'],entry['path']
print('ARCHIVE',OUT,'SIZE',OUT.stat().st_size,'VERIFIED_HASHES',len(meta),'ZIP_MEMBERS',len(meta)+2)
