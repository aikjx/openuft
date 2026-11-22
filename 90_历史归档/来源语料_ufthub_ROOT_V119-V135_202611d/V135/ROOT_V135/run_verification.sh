#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
python -m unittest discover -s tests -v
python - <<'PY'
from pathlib import Path
import hashlib
base=Path('.')
manifest=base/'manifest.sha256'
if not manifest.exists():
    print('manifest.sha256 not present; file verification skipped')
else:
    for row in manifest.read_text(encoding='utf-8').splitlines():
        if not row.strip():continue
        h,path=row.split('  ',1)
        actual=hashlib.sha256((base/path).read_bytes()).hexdigest()
        if actual!=h:raise AssertionError(f'Hash mismatch: {path}')
    print('SHA-256 manifest OK')
PY
