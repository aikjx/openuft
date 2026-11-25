#!/usr/bin/env python3
"""Verify the byte-for-byte integrity of the packaged static files."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parent
manifest=root/'MANIFEST.sha256'
errors=[];count=0
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    expected,rel=line.split('  ',1)
    f=root/rel
    if not f.is_file():errors.append(f'missing: {rel}');continue
    actual=hashlib.sha256(f.read_bytes()).hexdigest()
    if actual!=expected:errors.append(f'mismatch: {rel}')
    count+=1
for x in errors:print('FAIL',x)
if errors:sys.exit(1)
print(f'PASS SHA256 {count} static files (generated log files excluded)')
