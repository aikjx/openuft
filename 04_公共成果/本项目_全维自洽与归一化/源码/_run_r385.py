import os, sys, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
pat = os.path.join(HERE, "TUFT-r385_*.py")
hits = [h for h in sorted(glob.glob(pat)) if not os.path.basename(h).startswith("_")]
assert len(hits) == 1, hits
src = hits[0]
print("RUNNER source =", os.path.basename(src))
rc = subprocess.call([sys.executable, src])
print("RC =", rc)
sys.exit(rc)
