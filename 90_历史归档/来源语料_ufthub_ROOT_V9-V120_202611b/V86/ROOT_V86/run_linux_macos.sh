#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
python3 run_all.py --skip-browser
printf '%s\n' 'Open web/index.html in your browser for the offline dashboard.'
