# -*- coding: utf-8 -*-
"""复现入口：运行 TUFT-r146 四力统一可行性攻破复算引擎。

用法：python 源码/_run_r146.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r146_四力统一可行性_跨册归总与核心读数攻破复算_2026-10-22.py",
)

r = subprocess.run(
    [sys.executable, TARGET],
    cwd=HERE,
    encoding="utf-8",
    errors="replace",
)
sys.stdout.write(r.stdout or "")
sys.stderr.write(r.stderr or "")
sys.exit(r.returncode)
