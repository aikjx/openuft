#!/usr/bin/env python3
"""ROOT V130 offline verification, run from the extracted folder."""
import hashlib
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
manifest=root/'SHA256SUMS.txt'
if not manifest.exists(): raise SystemExit('Missing SHA256SUMS.txt')
entries=[l.strip().split('  ',1) for l in manifest.read_text(encoding='utf-8').splitlines() if l.strip()]
for digest,name in entries:
    f=root/name
    if not f.is_file(): raise SystemExit('MISSING: '+name)
    got=hashlib.sha256(f.read_bytes()).hexdigest()
    if got!=digest: raise SystemExit('HASH MISMATCH: '+name)
print('SHA256 verified',len(entries),'files')
run=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=root)
if run.returncode: raise SystemExit('Unit tests failed')
print('ROOT V130 verification PASSED')
