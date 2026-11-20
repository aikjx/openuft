#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python verify_checksums.py
python run_all.py
