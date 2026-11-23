# -*- coding: utf-8 -*-
"""ASCII runner: locate and run the unified-label meta-audit (py3.8 stdlib)."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_统一方程元审计_*", "unified_label_audit.py"))
assert len(hits) == 1, hits
runpy.run_path(hits[0], run_name="__main__")
