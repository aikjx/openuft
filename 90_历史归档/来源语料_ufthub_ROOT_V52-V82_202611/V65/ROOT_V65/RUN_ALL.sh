#!/bin/sh
set -eu
cd "$(dirname "$0")"
echo '=== ROOT V65 new tests ==='
python3 -m unittest discover -s tests -v
echo '=== ROOT V64 patched legacy tests ==='
(cd legacy_v64 && python3 -m unittest discover -s tests -v)
echo '=== regenerate simulations (not observational data) ==='
python3 experiments/generate.py
printf '\nTheorems are conditional; G and four-force unification remain OPEN.\n'
