# -*- coding: utf-8 -*-
"""ASCII runner for r213 (content-marker based target selection, no CJK literal)."""
import glob
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = b"R213-CALIBER-CENSUS"
CAND = []
for p in sorted(glob.glob(os.path.join(HERE, "TUFT-r213_*.py"))):
    with open(p, "rb") as f:
        head = f.read(65536)
    if MARK in head:
        CAND.append(p)
if len(CAND) != 1:
    raise SystemExit("expected exactly 1 r213 caliber engine, got %d (%s)"
                     % (len(CAND), [os.path.basename(x) for x in CAND]))
TARGET = CAND[0]
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
