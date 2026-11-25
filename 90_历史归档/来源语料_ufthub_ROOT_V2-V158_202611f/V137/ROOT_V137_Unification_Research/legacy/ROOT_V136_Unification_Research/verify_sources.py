"""Verify exact original source/documents within archive, not regenerated results."""
from pathlib import Path
import hashlib
import sys
ROOT=Path(__file__).resolve().parent
p=ROOT/'results'/'SHA256_SOURCES.txt'
errors=[]
for line in p.read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    expected,relative=line.split('  ',1)
    path=ROOT/relative
    if not path.is_file():
        errors.append(f'MISSING {relative}')
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        errors.append(f'CHANGED {relative}')
print('Sources/docs verified' if not errors else '\n'.join(errors))
raise SystemExit(0 if not errors else 1)
