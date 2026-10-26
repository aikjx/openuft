# -*- coding: utf-8 -*-
"""Driver for r226: run the engine directly, capture stdout to _r226_out.txt."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                   "TUFT-r226_四力统一方程_量子束缚层_同一势的薛定谔谱与四力束缚判决_精算与交互可视化_2026-10-26.py")
OUT = os.path.join(ROOT, "_r226_out.txt")

p = subprocess.run([sys.executable, "-X", "utf8", RUN],
                   capture_output=True, text=True, encoding="utf-8")
text = p.stdout or ""
if p.stderr:
    text += "\n[STDERR]\n" + p.stderr
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("rc=%d chars=%d out=%s" % (p.returncode, len(text), OUT))
