"""Verify exact file bytes against CHECKSUMS.sha256. Does not modify files."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
checks=root/'CHECKSUMS.sha256'
if not checks.exists():raise SystemExit('missing checksums')
count=0
for line in checks.read_text(encoding='utf-8').splitlines():
    digest, relative=line.split('  ',1)
    path=root/relative
    if not path.is_file():raise SystemExit('MISSING '+relative)
    real=hashlib.sha256(path.read_bytes()).hexdigest()
    if real!=digest:raise SystemExit(f'HASH MISMATCH: {relative}')
    count+=1
print('PASS: checked',count,'files')
