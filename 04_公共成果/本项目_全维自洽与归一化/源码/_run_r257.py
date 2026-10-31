# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r257_同一运动定理卷_单一运动公设求导统一力方程_"
        "传播子双路机导与符号定理与磁投影_耦合不可导反定理与十六格穷举矩阵_"
        "精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r257.txt")

p = subprocess.run([PY, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)
