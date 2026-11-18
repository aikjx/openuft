"""Verify SHA-256 manifest in extracted ROOT_V70 package.
This is a static file-integrity check, not a physics proof.
"""
import hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=root/'SHA256SUMS.txt'
lines=manifest.read_text(encoding='utf-8').splitlines()
errors=[]; checked=0
for line in lines:
    if not line.strip(): continue
    digest,rel=line.split('  ',1)
    p=root/rel
    if not p.is_file():errors.append(f'MISSING {rel}'); continue
    current=hashlib.sha256(p.read_bytes()).hexdigest()
    if current!=digest:errors.append(f'MISMATCH {rel}')
    checked+=1
print('SHA-256 checked:',checked,'files')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('SHA-256 VERIFIED')
