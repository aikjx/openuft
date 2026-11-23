# -*- coding: utf-8 -*-
"""ASCII runner: locate and run the S12 errata-residue audit (py3.8 stdlib)."""
import glob
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
hits = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_S12勘误残留元审计_*", "s12_errata_residue_audit.py"))
assert len(hits) == 1, hits
runpy.run_path(hits[0], run_name="__main__")
