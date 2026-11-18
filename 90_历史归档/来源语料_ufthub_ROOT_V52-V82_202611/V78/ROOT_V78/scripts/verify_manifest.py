"""Verify SHA-256 digest manifest after extraction (not a digital signature)."""
import csv,hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=root/'SHA256_MANIFEST.csv'
if not manifest.exists():raise SystemExit('Missing manifest')
with manifest.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
for row in rows:
    target=root/row['path']
    if not target.is_file():raise SystemExit(f'Missing: {row["path"]}')
    got=hashlib.sha256(target.read_bytes()).hexdigest()
    if got!=row['sha256']:raise SystemExit(f'Hash mismatch: {row["path"]}')
print(f'Verified SHA-256 of {len(rows)} content files. This is not a cryptographic signature.')
