#!/bin/sh
set -eu
cd "$(dirname "$0")"
python -m pip install -r requirements.txt
python run_all.py
python verify_checksums.py
