"""Validate exact byte-level integrity of the packaged ROOT V123 artifacts."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
manifest=root/'MANIFEST.sha256'
if not manifest.exists():
    print('MANIFEST MISSING',file=sys.stderr);sys.exit(1)
errors=[]
rows=[line.split('  ',1) for line in manifest.read_text().splitlines() if line.strip()]
for expect,rel in rows:
    path=root/rel
    if not path.is_file():
        errors.append('MISSING '+rel);continue
    got=hashlib.sha256(path.read_bytes()).hexdigest()
    if got!=expect:errors.append('SHA256 MISMATCH '+rel)
print('V123_MANIFEST',len(rows),'entries', 'OK' if not errors else 'FAIL')
for err in errors:print(err,file=sys.stderr)
sys.exit(bool(errors))
