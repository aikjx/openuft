#!/usr/bin/env python3
"""Verify SHA256 list for the source/data at time of packaging."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'MANIFEST.sha256'
ok=True
for line in manifest.read_text(encoding='utf8').splitlines():
    if not line.strip():continue
    expected,rel=line.split('  ',1)
    p=ROOT/rel
    actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'
    if actual!=expected:
        print('FAIL',rel)
        ok=False
print('MANIFEST:', 'PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 1)
