#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python run_tests.py
python symbolic_checks.py
python run_experiments.py
python build_catalog.py
printf '\nROOT V74: all requested command-line checks passed.\n'
