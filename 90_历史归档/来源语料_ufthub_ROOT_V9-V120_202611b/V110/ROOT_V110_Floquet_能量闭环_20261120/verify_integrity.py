"""Verify distributed package source/data digests (CHECKSUMS.sha256 excluded)."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
checks=root/'CHECKSUMS.sha256'
if not checks.exists():
    raise SystemExit('CHECKSUMS.sha256 missing: package not yet finalized')
records=checks.read_text(encoding='utf-8').splitlines()
for line in records:
    expected,rel=line.split('  ',1)
    path=root/rel
    if not path.is_file():raise SystemExit(f'MISSING: {rel}')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit(f'HASH MISMATCH: {rel}')
print(f'PASS: {len(records)} SHA-256 files checked')
