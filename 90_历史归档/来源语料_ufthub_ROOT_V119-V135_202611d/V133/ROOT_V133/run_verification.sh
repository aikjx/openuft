#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python src/root_v133.py
python src/make_figures.py
python src/property_audit.py
python -m unittest discover -s tests -v
# The manifest covers the pre-generated reproducible data and code, not refreshed logs.
sha256sum -c manifest.sha256
