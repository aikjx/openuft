"""Verify immutable snapshot SHA256 for every packaged file except CHECKSUMS itself."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
entries=(root/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
errors=[]
for line in entries:
    digest,rel=line.split('  ',1)
    relpath=Path(rel)
    if relpath.is_absolute() or '..' in relpath.parts:
        errors.append('unsafe relative path '+rel);continue
    path=root/relpath
    if not path.is_file(): errors.append('missing '+rel); continue
    h=hashlib.sha256(path.read_bytes()).hexdigest()
    if h!=digest:errors.append('SHA256 mismatch '+rel)
print('Verified',len(entries),'SHA-256 entries. Errors:',len(errors))
for x in errors:print('ERROR',x)
if errors:sys.exit(1)
