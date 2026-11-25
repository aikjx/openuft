#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 src/verify_v139.py
echo "Verification PASSED; see data/verification_results.json"
