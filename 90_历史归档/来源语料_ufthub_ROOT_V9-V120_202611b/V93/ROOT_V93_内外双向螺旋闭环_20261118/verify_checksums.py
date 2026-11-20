"""Verify immutable release checksums before re-generating optional results."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
f=root/'CHECKSUMS.sha256'
if not f.exists(): sys.exit('Cannot find CHECKSUMS.sha256')
rows=[x.strip() for x in f.read_text(encoding='utf-8').splitlines() if x.strip()]
for row in rows:
    digest,name=row.split('  ',1)
    p=root/name
    assert p.is_file(),f'MISSING {name}'
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==digest,f'HASH FAILURE {name}'
print('CHECKSUMS_PASSED',len(rows))
