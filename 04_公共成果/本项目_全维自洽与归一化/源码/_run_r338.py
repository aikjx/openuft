# -*- coding: utf-8 -*-
"""r338 runner（复现入口）—— 光速螺旋 G1「ω 场方程」：自由度计数不可反解定理"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r338_螺旋频率场方程G1_自由度计数不可反解定理与函数族定价_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r338.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
