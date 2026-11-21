#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
export PYTHONPATH="$PWD/scripts"
printf '[1/4] V122 test suite\n'
python -m pytest -q tests | tee results/V122_tests.txt
printf '[2/4] Reproduce calculations and figures\n'
python scripts/run_v122.py > results/V122_run_stdout.json
printf '[3/4] V121 predecessor suite (extracted from bundled ZIP)\n'
TEMPDIR="$(mktemp -d)"
trap 'rm -rf "$TEMPDIR"' EXIT
python - "$TEMPDIR" <<'PY'
import sys,zipfile
with zipfile.ZipFile('prior_v121/ROOT_V121_original.zip') as z:
    z.extractall(sys.argv[1])
PY
( cd "$TEMPDIR/ROOT_V121" && PYTHONPATH="$PWD/scripts" python -m pytest -q tests prior_v120/test_rootv120.py ) | tee results/V121_inherited_tests.txt
printf '[4/4] SHA256 verify\n'
python verify_manifest.py
