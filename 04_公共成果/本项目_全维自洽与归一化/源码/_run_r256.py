# -*- coding: utf-8 -*-
"""r256 runner：直接运行引擎，stdout 落盘到 _out_r256.txt（UTF-8, LF）。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "TUFT-r256_四力统一方程_宇宙学声学峰层_"
                   "声视界角度与声学多极及张量边界_精算与交互可视化_2026-10-31.py")
OUT = os.path.join(HERE, "_out_r256.txt")

p = subprocess.run([sys.executable, "-X", "utf8", RUN],
                   capture_output=True, text=True, encoding="utf-8")
text = (p.stdout or "") + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("rc=%d chars=%d out=%s" % (p.returncode, len(text), OUT))
sys.exit(p.returncode)
