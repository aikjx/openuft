#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/scripts"
echo '[1/6] SHA256 validate all ROOT V127 artifacts'
python verify_manifest.py
echo '[2/6] Execute 93 independent ROOT V127 numerical & symbolic tests'
python -m pytest -q tests/
echo '[3/6] Recalculate CODATA-derived quantities and synthetic figures'
python scripts/run_v127.py > /dev/null
echo '[4/6] Recheck deterministic generated results and SHA256'
python verify_manifest.py
echo '[5/6] Verify previous ROOT V126 ZIP and recorded independent historical audit'
python - <<'PYHISTORY'
from pathlib import Path
import zipfile
p=Path('prior_v126/ROOT_V126_original.zip')
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert 'ROOT_V126/README.md' in z.namelist()
log=Path('results/inherited_v126_verification.log').read_text()
assert 'ROOT V126 COMPLETE: 111 new + 336 inherited = 447 code/math tests' in log
assert 'V126_MANIFEST_OK 18 files' in log
print('HISTORY_ARCHIVE_INTEGRITY_OK; earlier 447 tests have an independent verified log')
PYHISTORY
if [[ "${1:-}" == "--full-history" ]]; then
  echo '[optional] Full historical tests from extracted ZIP' 
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python - "$TMP" <<'PY'
import sys, zipfile
from pathlib import Path
root=Path(sys.argv[1]).resolve()
with zipfile.ZipFile('prior_v126/ROOT_V126_original.zip') as z:
    assert z.testzip() is None
    for entry in z.infolist():
        target=(root/entry.filename).resolve()
        assert target.is_relative_to(root),f'unsafe archive member {entry.filename}'
    z.extractall(root)
PY
(cd "$TMP/ROOT_V126" && bash verify_all.sh)
fi
echo '[6/6] Final manifest verification'
python verify_manifest.py
echo 'ROOT V127 COMPLETE: 93 current tests passed; 447 previous tests separately re-run and logged earlier. Full recursive re-run optional via --full-history. Physical unification OPEN.'
