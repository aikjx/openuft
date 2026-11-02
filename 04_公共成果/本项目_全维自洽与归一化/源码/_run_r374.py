# -*- coding: utf-8 -*-
# ASCII runner for TUFT-r374 (Chinese path must not go through argv)
import glob, io, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
pat = os.path.join(HERE, "TUFT-r374_*.py")
hits = sorted(glob.glob(pat))
hits = [h for h in hits if not os.path.basename(h).startswith("_")]
assert len(hits) == 1, ("expected exactly 1 source, got %d: %s" % (len(hits), hits))
src = hits[0]
print("RUNNER source =", os.path.basename(src))
rc = subprocess.call([sys.executable, src])
print("RC =", rc)
sys.exit(rc)
