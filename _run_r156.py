# -*- coding: utf-8 -*-
"""TUFT-r156 runner：调用场论层审计引擎（v总=c 第二/三步）。"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(BASE, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                 "TUFT-r156_v总等于c第二三步_作用量电荷环流与Frank分解_全维审计_2026-10-23.py")
p = subprocess.run([sys.executable, "-B", T], capture_output=True,
                   text=True, encoding="utf-8", errors="replace")
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass
sys.stdout.write(p.stdout[-1500:] + "\n")
sys.stderr.write(p.stderr[-800:] + "\n")
sys.stdout.write("rc=%d\n" % p.returncode)
sys.exit(p.returncode)
