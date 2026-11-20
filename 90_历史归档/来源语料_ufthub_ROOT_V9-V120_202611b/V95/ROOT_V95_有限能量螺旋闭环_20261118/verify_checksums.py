"""Verify delivered file hashes (before regenerating artifacts)."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
lines=(root/'CHECKSUMS.sha256').read_text().splitlines()
for line in lines:
    checksum,rel=line.split('  ',1)
    file=root/rel
    assert file.is_file(),f'missing file: {rel}'
    actual=hashlib.sha256(file.read_bytes()).hexdigest()
    assert checksum==actual,f'SHA256 mismatch: {rel}'
print(f'SHA-256 verified: {len(lines)} independent delivered file entries')
