# -*- coding: utf-8 -*-
"""ASCII runner: glob-locate the V50 external-review recompute script."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_外部来料复核_V50_*", "v50_ext_review_recompute.py"))
assert len(hits) == 1, "expected exactly one recompute script, got %d" % len(hits)
runpy.run_path(hits[0], run_name="__main__")
