"""Verify exact file checksums listed in CHECKSUMS.sha256.
Excludes the checksum file and manifest, avoiding self-hash cycles.
"""
from pathlib import Path
from hashlib import sha256
from sys import exit
ROOT=Path(__file__).resolve().parent
checksum=ROOT/'CHECKSUMS.sha256'
if not checksum.exists():raise SystemExit('CHECKSUMS.sha256 missing')
entries=[]
for line in checksum.read_text(encoding='utf-8').splitlines():
    digest,rel=line.split('  ',1)
    path=ROOT/rel
    if not path.is_file():raise SystemExit('Missing '+rel)
    actual=sha256(path.read_bytes()).hexdigest()
    if actual!=digest:raise SystemExit('HASH MISMATCH '+rel)
    entries.append(rel)
actual_files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('MANIFEST.json','CHECKSUMS.sha256')}
missing=actual_files-set(entries)
if missing:raise SystemExit('UNHASHED FILES: '+str(sorted(missing)))
print('PASS SHA-256',len(entries),'files')
