from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'CHECKSUMS.sha256'
if not manifest.is_file():raise SystemExit('Missing CHECKSUMS.sha256')
rows=[l.strip().split('  ',1) for l in manifest.read_text(encoding='utf-8').splitlines() if l.strip()]
for digest,relative in rows:
    path=ROOT/relative
    if not path.exists():raise SystemExit(f'MISSING {relative}')
    got=hashlib.sha256(path.read_bytes()).hexdigest()
    if got!=digest:raise SystemExit(f'HASH MISMATCH {relative}')
print('PASS:',len(rows),'file SHA-256 checks')
