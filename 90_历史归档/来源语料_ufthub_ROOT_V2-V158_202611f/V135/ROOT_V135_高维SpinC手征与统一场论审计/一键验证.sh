#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python3 src/verify_v135.py
printf '%s\n' 'ROOT V135 checks finished. Inspect data/verification_results.json for scope and limitations.'
