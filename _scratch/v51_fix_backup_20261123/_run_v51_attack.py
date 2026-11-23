# -*- coding: utf-8 -*-
"""ASCII runner: glob-locate the V51 attack recompute script."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_V51攻破_*", "v51_attack_recompute.py"))
assert len(hits) == 1, "expected exactly one V51 attack script, got %d" % len(hits)
runpy.run_path(hits[0], run_name="__main__")
