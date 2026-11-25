#!/usr/bin/env python3
"""Verify exported SHA256 manifest in V136 extracted directory (stdlib)."""
import hashlib, pathlib, sys
root=pathlib.Path(__file__).resolve().parent
manifest=root/'MANIFEST_SHA256.txt'
if not manifest.exists():
    print('MANIFEST_SHA256.txt not found. Did you extract the full ZIP?')
    sys.exit(2)
checks=0
for record in manifest.read_text(encoding='utf-8').splitlines():
    if not record or record.startswith('#'): continue
    sha,rel=record.split('  ',1)
    target=root/rel
    if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=sha:
        print('[FAIL]',rel)
        sys.exit(1)
    checks+=1
print(f'[PASS] SHA-256 verified for {checks} files')
