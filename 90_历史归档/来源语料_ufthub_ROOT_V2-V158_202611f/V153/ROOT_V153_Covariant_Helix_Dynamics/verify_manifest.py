"""Verify expected static files against SHA-256.

manifest.json is excluded to avoid recursion. Generated files remain deterministic
but upgrading runtime libraries might change a regenerated plot or float serialization.
"""
import json
import hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
entries=json.loads((root/'manifest.json').read_text(encoding='utf8'))['files']
for rel,expected in entries.items():
    p=root/rel
    assert p.exists() and p.is_file(), f'missing {rel}'
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    assert got==expected, f'checksum mismatch {rel}: {got}'
print(f'PASS: SHA-256 verified for {len(entries)} static files')
