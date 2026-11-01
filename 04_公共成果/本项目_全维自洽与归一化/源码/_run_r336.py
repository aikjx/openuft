# -*- coding: utf-8 -*-
"""r336 runner —— 族数唯一性定理 · 反常自由荷空间实为 2 维"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r336_族数唯一性定理_反常自由荷空间实为2维_单扭转唯一纯复制_双扭转反例_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r336.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-9000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
