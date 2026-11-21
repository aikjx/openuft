from pathlib import Path
import hashlib
base=Path(__file__).resolve().parent
manifest=base/'MANIFEST.sha256'
if not manifest.exists():
    raise SystemExit('MISSING MANIFEST')
items=0
for line in manifest.read_text(encoding='utf8').splitlines():
    sha, name=line.split('  ',1)
    p=base/name
    assert p.exists(), name
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==sha, f'CHECKSUM MISMATCH {name}'
    items+=1
print(f'MANIFEST_OK {items} files')
