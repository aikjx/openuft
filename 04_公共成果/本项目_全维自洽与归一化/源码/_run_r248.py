# -*- coding: utf-8 -*-
"""ASCII runner for r248 (中文路径不进 argv)。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "TUFT-r248_单方程全域力层_主方程量纲断裂与自旋条件虚数解_精算与可视化_2026-10-30.py"
p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, NAME)],
                   cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
out = (p.stdout or "") + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")
with open(os.path.join(HERE, "_out_r248.txt"), "w", encoding="utf-8") as f:
    f.write(out + "\nrc=%d\n" % p.returncode)
print(out)
print("rc=%d" % p.returncode)
sys.exit(p.returncode)
