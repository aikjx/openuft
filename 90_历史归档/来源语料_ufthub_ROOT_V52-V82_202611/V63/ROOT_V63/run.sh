#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 -m unittest discover -s tests -v
python3 experiments/run_experiments.py
printf '\nOpen web/index.html in a browser for interactive visualization.\n'
