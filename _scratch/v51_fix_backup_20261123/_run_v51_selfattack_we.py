# -*- coding: utf-8 -*-
"""ASCII runner: glob-locate the V51 self-attack Wigner-Eckart script (py38+sympy)."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_V51自噬_WignerEckart*", "v51_selfattack_we_recompute.py"))
assert len(hits) == 1, "expected exactly one WE script, got %d" % len(hits)
runpy.run_path(hits[0], run_name="__main__")
