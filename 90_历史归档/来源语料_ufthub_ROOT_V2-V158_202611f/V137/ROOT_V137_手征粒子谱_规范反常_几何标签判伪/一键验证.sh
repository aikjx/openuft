#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 src/verify_v137.py
