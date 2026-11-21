#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/scripts"
echo '[1/3] V124 53 additional mathematical and numerical tests'
python -m pytest -q tests

echo '[2/3] V123 93, V122 41, V121 48 inherited tests'
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python - "$TMP" <<'PY'
from pathlib import Path
import zipfile,sys
p=Path('prior_v123/ROOT_V123_original.zip')
with zipfile.ZipFile(p) as z:
  root=Path(sys.argv[1]).resolve()
  for entry in z.infolist():
    out=(root/entry.filename).resolve()
    if not out.is_relative_to(root):raise RuntimeError('Unsafe ZIP entry')
  z.extractall(root)
PY
(cd "$TMP/ROOT_V123" && bash verify_all.sh)
echo '[3/3] SHA-256 checksum'
python verify_manifest.py
