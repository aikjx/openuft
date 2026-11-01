# -*- coding: utf-8 -*-
"""r304 runner（复现入口）—— ROOT V20 跨现象 α 本源审计来料核验"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r304_ROOTV20跨现象alpha本源审计_耦合非唯一性与全阶无固定点与统一参数计数定理_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r304.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
