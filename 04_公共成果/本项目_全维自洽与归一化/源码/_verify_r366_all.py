# -*- coding: utf-8 -*-
# r366 收口总验（ASCII 入口，中文路径不出 argv）
import os, subprocess, sys

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
SRC = os.path.join(BASE, "源码")

jobs = [
    ("engine", "_run_r366.py"),
    ("links", "_check_r366_links.py"),
    ("register", "_reg_r366.py"),
    ("log", "_log_r366.py"),
]

rcs = {}
for tag, fn in jobs:
    p = os.path.join(SRC, fn)
    if not os.path.exists(p):
        print("[%s] MISSING %s" % (tag, fn))
        rcs[tag] = -1
        continue
    r = subprocess.run([sys.executable, p], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=SRC)
    out = (r.stdout or "") + (r.stderr or "")
    tail = [l for l in out.splitlines() if l.strip()][-5:]
    print("=" * 60)
    print("[%s] %s  rc=%d" % (tag, fn, r.returncode))
    for l in tail:
        print("    " + l[:150])
    rcs[tag] = r.returncode

print("=" * 60)
print("[summary] " + "  ".join("%s=%d" % (k, v) for k, v in rcs.items()))
bad = [k for k, v in rcs.items() if v != 0]
print("[verdict] " + ("ALL-GREEN" if not bad else "BAD=" + ",".join(bad)))
sys.exit(0 if not bad else 5)
