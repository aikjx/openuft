#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 run_all.py
if python3 -c 'import sympy' >/dev/null 2>&1; then python3 symbolic_audit.py; fi
python3 verify_manifest.py
