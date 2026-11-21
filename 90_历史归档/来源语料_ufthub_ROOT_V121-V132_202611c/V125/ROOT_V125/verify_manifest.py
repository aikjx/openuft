"""Verify all package hashes and reject path escapes in SHA256 manifest."""
import hashlib
from pathlib import Path

base=Path(__file__).resolve().parent
manifest=base/'MANIFEST.sha256'
if not manifest.is_file():
    raise SystemExit('MANIFEST_MISSING')
checked=0
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    digest, sep, name=line.partition('  ')
    if len(digest)!=64 or not sep:
        raise SystemExit(f'MANIFEST_INVALID_LINE:{line[:60]}')
    path=(base/name).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise SystemExit(f'MANIFEST_INVALID_PATH:{name}')
    got=hashlib.sha256(path.read_bytes()).hexdigest()
    if got != digest:
        raise SystemExit(f'CHECKSUM_MISMATCH:{name}')
    checked+=1
print(f'V125_MANIFEST_OK {checked} files')
