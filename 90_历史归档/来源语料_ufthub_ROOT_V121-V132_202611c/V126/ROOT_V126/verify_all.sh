#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/scripts"
echo '[1/5] Check V126 file SHA256 manifest'
python verify_manifest.py
echo '[2/5] Execute V126 new mathematical and synthetic tests'
python -m pytest -q tests/test_v126.py
echo '[3/5] Extract V125 original ZIP and re-run historical V121-V125 suites'
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python - "$TMP" <<'PY'
from pathlib import Path
import sys, zipfile
root=Path(sys.argv[1]).resolve()
with zipfile.ZipFile('prior_v125/ROOT_V125_original.zip') as z:
    assert z.testzip() is None
    for entry in z.infolist():
        dest=(root/entry.filename).resolve()
        assert dest.is_relative_to(root),f'unsafe archive member {entry.filename}'
    z.extractall(root)
PY
(cd "$TMP/ROOT_V125" && bash verify_all.sh)
echo '[4/5] Recheck independent V126 core math and archived reproducible data'
python scripts/run_v126.py --verify-only
echo '[5/5] Verify generated artifact SHA256 once again'
python verify_manifest.py
echo 'ROOT V126 COMPLETE: 111 new + 336 inherited = 447 code/math tests; measured fifth force and unification are OPEN.'
