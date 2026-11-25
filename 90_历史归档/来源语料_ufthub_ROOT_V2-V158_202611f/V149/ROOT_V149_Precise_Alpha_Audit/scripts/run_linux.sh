#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 -m pip install -r requirements.txt
python3 run_all.py
python3 verify_manifest.py
