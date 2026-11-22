#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m unittest discover -s tests -v
python src/root_v134.py >/dev/null
python src/property_audit.py >/dev/null
python src/make_figures.py
python - <<'PY'
from pathlib import Path
import hashlib
lines=Path('manifest.sha256').read_text(encoding='utf-8').splitlines()
for line in lines:
    hash_,path=line.split('  ',1)
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==hash_, path
print('SHA-256 integrity verified for',len(lines),'files')
PY
