# -*- coding: utf-8 -*-
"""复现入口：运行 TUFT-r144 求导证明验证与精算引擎。

用法：python 源码/_run_r144.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r144_空间是否运动与怎么运动_跨册归总_求导证明验证精算_2026-10-21.py",
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
