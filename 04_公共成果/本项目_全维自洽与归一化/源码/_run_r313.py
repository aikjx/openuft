# -*- coding: utf-8 -*-
"""r313 runner（复现入口）—— ROOT V21「精细结构常数的固定点机制」第一性核验"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r313_ROOTV21精细结构常数固定点机制第一性核验_四路线互消与未知量搬家定理与BZ截断相消_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r313.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
