# -*- coding: utf-8 -*-
"""ASCII runner for TUFT-r339 (rank-one hypersurface integrality, X-R335-2).
Glob prefix is volume specific AND asserts exactly one hit (r335/r338 incidents)."""
import glob
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
cands = [p for p in glob.glob(os.path.join(HERE, "TUFT-r339_*.py"))
         if not os.path.basename(p).startswith("_")]
cands = [p for p in cands if os.path.basename(p).startswith("TUFT-r339_\u79e9\u4e00")]
if len(cands) != 1:
    print("BAD SOURCE COUNT = %d : %r" % (len(cands), [os.path.basename(p) for p in cands]))
    sys.exit(4)

src = cands[0]
print("[runner] source = %s" % os.path.basename(src))
sys.argv = [src]
runpy.run_path(src, run_name="__main__")
