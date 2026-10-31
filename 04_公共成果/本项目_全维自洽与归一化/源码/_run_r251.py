# -*- coding: utf-8 -*-
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "_out_r251.txt")
with open(out, "w", encoding="utf-8") as f:
    rc = subprocess.run(["python", "TUFT-r251_下游物理应用层_垂直原理FRW与黑洞无奇点精算与可视化_2026-10-31.py"],
                        cwd=here, stdout=f, stderr=subprocess.STDOUT).returncode
print("rc=%d" % rc)
