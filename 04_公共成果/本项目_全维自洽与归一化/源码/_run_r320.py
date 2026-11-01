# -*- coding: utf-8 -*-
"""r320 runner (repro entry) -- ROOT V24 chart-layer admissibility volume.

ASCII-only by design: SRC comes from __file__ and the engine name is globbed,
so neither this file nor its command line carries CJK bytes (the engine path
does).
"""
import glob
import io
import os
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "_out_r320.txt")

# TUFT-r320_ROOTV24<chart-admissibility...>_2026-11-01.py
NAME_PREFIX = "TUFT-r320_ROOTV24"


def find_engine():
    hits = [p for p in glob.glob(os.path.join(SRC, NAME_PREFIX + "*.py"))]
    return hits


def main():
    hits = find_engine()
    if len(hits) != 1:
        print("ENGINE-AMBIGUOUS count=%d" % len(hits))
        for h in hits:
            print("   ", os.path.basename(h))
        return 2
    name = os.path.basename(hits[0])
    p = subprocess.run([sys.executable, "-X", "utf8", name], cwd=SRC,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    txt = p.stdout.decode("utf-8", "replace")
    buf = io.open(OUT, "wb")
    buf.write(txt.encode("utf-8"))
    buf.close()
    tail = txt[-6000:]
    sys.stdout.buffer.write(tail.encode("utf-8", "replace"))
    sys.stdout.buffer.flush()
    sys.stdout.buffer.write(("\nRC= %d\n" % p.returncode).encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0 if p.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
