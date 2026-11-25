#!/usr/bin/env python3
"""Offline SHA-256 verification for all delivered files (except manifest itself)."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
rows=(root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
fail=[]
for row in rows:
    if not row.strip(): continue
    sha, name=row.split('  ',1)
    name=name.strip()
    if name.startswith('/') or '..' in Path(name).parts:
        fail.append(f'unsafe path: {name}'); continue
    path=root/name
    if not path.is_file():
        fail.append(f'missing: {name}'); continue
    got=hashlib.sha256(path.read_bytes()).hexdigest()
    if sha!=got: fail.append(f'SHA mismatch: {name}')
print(f'File manifest verification: {len(rows)-len(fail)}/{len(rows)} passed')
if fail:
    print('\n'.join(fail))
    raise SystemExit(1)
