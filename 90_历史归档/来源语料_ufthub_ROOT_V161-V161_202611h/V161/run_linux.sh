#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python run_all.py
python verify.py
