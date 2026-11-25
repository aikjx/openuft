#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 src/verify_v136.py
python3 verify_archive.py
printf '[PASS] ROOT V136 local verification\n'
