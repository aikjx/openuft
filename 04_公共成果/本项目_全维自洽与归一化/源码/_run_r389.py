# -*- coding: utf-8 -*-
"""ASCII runner for TUFT-r389（glob 定位、断言命中 == 1）"""
import os
import glob
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
pat = os.path.join(HERE, "TUFT-r389_*.py")
hits = [h for h in sorted(glob.glob(pat)) if not os.path.basename(h).startswith("_")]
assert len(hits) == 1, hits
p = subprocess.run([sys.executable, hits[0]], capture_output=True, text=True, encoding="utf-8")
sys.stdout.write(p.stdout)
sys.stderr.write(p.stderr)
print("RUNNER source = %s" % os.path.basename(hits[0]))
print("RC = %d" % p.returncode)
