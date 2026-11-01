# -*- coding: utf-8 -*-
"""r350 runner —— 攻 X-R336-1 · 扭转自由度两个独立群元几何允许"""
import io
import os
import subprocess
import sys

SRC = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
NAME = ("TUFT-r350_攻X-R336-1_扭转自由度两个独立群元几何允许与框架不预言3结构定理_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r350.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-9000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
