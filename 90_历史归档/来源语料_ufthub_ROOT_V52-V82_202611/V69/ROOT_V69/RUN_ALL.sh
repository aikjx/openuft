#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 run_all.py
python3 experiments/run_analysis.py
python3 verify_package.py
