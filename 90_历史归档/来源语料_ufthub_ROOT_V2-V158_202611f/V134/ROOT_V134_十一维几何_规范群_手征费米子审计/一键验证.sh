#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 verify_v134.py
echo '[OK] Math audit completed. Review limitations in report.'
