#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 run_all.py
python3 verify.py
