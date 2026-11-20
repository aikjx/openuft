#!/bin/sh
set -eu
python3 -m pip install -r requirements.txt
python3 run_all.py
python3 verify_integrity.py
