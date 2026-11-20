#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 run_all.py
printf '%s\n' 'ROOT V84 complete: ALL OBSERVATIONS SYNTHETIC.'
