# -*- coding: utf-8 -*-
"""ASCII runner for 73_higgs_stability_calc.py (avoids non-ASCII argv issues)."""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "73_higgs_stability_calc.py")
if not os.path.exists(SRC):
    sys.stderr.write("missing source: %s\n" % SRC)
    sys.exit(3)
sys.argv = [SRC]
runpy.run_path(SRC, run_name="__main__")
