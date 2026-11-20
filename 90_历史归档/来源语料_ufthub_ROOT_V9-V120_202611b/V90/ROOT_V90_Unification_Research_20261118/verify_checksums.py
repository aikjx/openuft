"""Independent SHA-256 integrity check. Uses only Python standard library."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
checks=(root/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines()
for line in checks:
    digest,path=line.split('  ',1)
    f=root/path
    if not f.is_file(): raise FileNotFoundError(path)
    got=hashlib.sha256(f.read_bytes()).hexdigest()
    if got!=digest: raise AssertionError(f'checksum changed: {path}')
print(f'PASS: SHA-256 for {len(checks)} project files')
