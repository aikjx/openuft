# -*- coding: utf-8 -*-
"""Driver for r232: run the engine directly, capture stdout to _r232_out.txt."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                   "TUFT-r232_四力统一方程_引力波层_四极辐射啁啾与HulseTaylor锚_精算与交互可视化_2026-10-26.py")
OUT = os.path.join(ROOT, "_r232_out.txt")

p = subprocess.run([sys.executable, "-X", "utf8", RUN],
                   capture_output=True, text=True, encoding="utf-8")
text = p.stdout or ""
if p.stderr:
    text += "\n[STDERR]\n" + p.stderr
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("rc=%d chars=%d out=%s" % (p.returncode, len(text), OUT))
