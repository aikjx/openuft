"""Check original released bytes. Run before regenerating the computed charts."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
p=ROOT/'CHECKSUMS.sha256'
errors=[]; n=0
for line in p.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    hash0,name=line.split('  ',1)
    f=ROOT/name
    if not f.is_file():errors.append(f'MISSING {name}');continue
    h=hashlib.sha256(f.read_bytes()).hexdigest()
    if h!=hash0:errors.append(f'MISMATCH {name}')
    n+=1
print(f'SHA256 checked={n}, mismatches={len(errors)}')
for e in errors:print(e)
if errors:raise SystemExit(1)
