# -*- coding: utf-8 -*-
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = sys.argv[1]
raw = open(p, "rb").read()
print("CRLF count:", raw.count(b"\r\n"), " bare LF:", raw.count(b"\n") - raw.count(b"\r\n"),
      " bare CR:", raw.count(b"\r") - raw.count(b"\r\n"))
lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
a, b = int(sys.argv[2]), int(sys.argv[3])
for i in range(a - 1, min(b, len(lines))):
    print(i + 1, repr(lines[i]))
