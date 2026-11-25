#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m pip install -r requirements.txt
python3 run_all.py
python3 symbolic_audit.py
python3 verify_manifest.py
