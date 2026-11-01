# -*- coding: utf-8 -*-
import glob, io, os, runpy, sys, traceback
HERE = os.path.dirname(os.path.abspath(__file__))
cands = [p for p in glob.glob(os.path.join(HERE, "TUFT-r309_*.py"))]
SRC = cands[0]
OUT = os.path.join(HERE, "_out_r309.txt")
buf = io.StringIO()
old = sys.stdout
sys.stdout = buf
rc = 0
try:
    runpy.run_path(SRC, run_name="__main__")
except SystemExit as e:
    rc = int(e.code or 0)
except Exception:
    traceback.print_exc()
    rc = 1
finally:
    sys.stdout = old
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(buf.getvalue())
print("src=", os.path.basename(SRC))
print("wrote", len(buf.getvalue()), "chars rc=", rc)
print(buf.getvalue()[-2500:])
sys.exit(rc)
