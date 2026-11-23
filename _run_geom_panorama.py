# -*- coding: utf-8 -*-
"""ASCII runner: locate and run the geometry-panorama recompute (py3.8 stdlib)."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_外部来料融合_宇宙几何全景*", "geom_panorama_recompute.py"))
assert len(hits) == 1, hits
runpy.run_path(hits[0], run_name="__main__")
