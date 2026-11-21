#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/scripts"
echo '[1/4] Validate archive hashes of source bundle'
python verify_manifest.py
echo '[2/4] ROOT V125 new mathematical/numerical regression suite'
python -m pytest -q tests
echo '[3/4] Re-run ROOT V124/123/122/121 historical suites from stored ZIP'
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python - "$TMP" <<'PY'
from pathlib import Path
import sys,zipfile
p=Path('prior_v124/ROOT_V124_original.zip')
root=Path(sys.argv[1]).resolve()
with zipfile.ZipFile(p) as archive:
    if archive.testzip():raise RuntimeError('V124 historical ZIP CRC failure')
    for item in archive.infolist():
        dest=(root/item.filename).resolve()
        if not dest.is_relative_to(root):raise RuntimeError('Unsafe nested archive member')
    archive.extractall(root)
PY
(cd "$TMP/ROOT_V124" && bash verify_all.sh)
echo '[4/4] Recompute idealized V125 figures and data'
python scripts/run_v125.py
echo 'COMPLETE: 101 new tests + 235 historical = 336 tests; physical experiments not included.'
