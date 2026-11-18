"""Verify the SHA-256 of all declared source and results files after extracting ZIP."""
import hashlib,csv,sys
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=base/'SHA256_MANIFEST.csv'
if not manifest.exists():sys.exit('missing manifest')
rows=list(csv.DictReader(manifest.open(encoding='utf-8-sig')))
for row in rows:
    path=base/row['path']
    if not path.exists():sys.exit('missing '+str(path))
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if sha!=row['sha256']:sys.exit('hash mismatch '+str(path))
print(f'ROOT V72 integrity check OK: {len(rows)} files; not a physics validation.')
