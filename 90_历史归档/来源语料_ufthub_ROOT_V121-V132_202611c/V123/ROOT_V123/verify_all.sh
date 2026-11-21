#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/scripts"
echo '[1/3] V123 93 symbolic and numerical tests'
python -m pytest -q tests

echo '[2/3] V122 41 + V121 48 historical test re-run'
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python - "$TMP" <<'PY'
import sys,zipfile
from pathlib import Path
z=Path('prior_v122/ROOT_V122_original.zip')
with zipfile.ZipFile(z) as f:
    # Archive trusted as the bundled preceding version; check extraction paths.
    out=Path(sys.argv[1]).resolve()
    for obj in f.infolist():
        dest=(out/obj.filename).resolve()
        if not dest.is_relative_to(out):raise RuntimeError('unsafe ZIP member')
    f.extractall(out)
PY
(cd "$TMP/ROOT_V122" && bash verify_all.sh)
echo '[3/3] V123 exact SHA256 manifest'
python verify_manifest.py
