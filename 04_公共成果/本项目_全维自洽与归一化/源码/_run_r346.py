# -*- coding: utf-8 -*-
"""ASCII runner for TUFT-r346 (integer Newton coefficients are elementary, X-R339-1).
Glob prefix is volume specific AND asserts exactly one hit (r335/r338 incidents)."""
import glob
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
cands = [p for p in glob.glob(os.path.join(HERE, "TUFT-r346_*.py"))
         if not os.path.basename(p).startswith("_")]
cands = [p for p in cands if os.path.basename(p).startswith("TUFT-r346_\u6574\u6570")]
if len(cands) != 1:
    print("BAD SOURCE COUNT = %d : %r" % (len(cands), [os.path.basename(p) for p in cands]))
    sys.exit(4)

src = cands[0]
print("[runner] source = %s" % os.path.basename(src))
sys.argv = [src]
runpy.run_path(src, run_name="__main__")
