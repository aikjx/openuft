"""Verify all immutable files against package SHA-256 snapshot."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
lines=(ROOT/'CHECKSUMS.sha256').read_text('utf-8').splitlines()
checks=0
for line in lines:
 if not line.strip():continue
 h,rel=line.split('  ',1)
 p=ROOT/rel
 if not p.is_file():raise SystemExit(f'Missing: {rel}')
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 if actual!=h:raise SystemExit(f'Integrity mismatch: {rel}')
 checks+=1
print(f'SHA-256 verified {checks} files (model results are THEORY only)')
