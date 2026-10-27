# -*- coding: utf-8 -*-
"""Driver for r235."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                   "TUFT-r235_四力统一方程_总览合并轮_七层交互页统一入口_整理与验收归档_2026-10-26.py")
OUT = os.path.join(ROOT, "_r235_out.txt")
p = subprocess.run([sys.executable, "-X", "utf8", RUN], capture_output=True, text=True, encoding="utf-8")
text = (p.stdout or "") + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")
open(OUT, "w", encoding="utf-8", newline="\n").write(text)
print("rc=%d chars=%d out=%s" % (p.returncode, len(text), OUT))
