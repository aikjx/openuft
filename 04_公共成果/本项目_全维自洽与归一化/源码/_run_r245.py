# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r245_常温超导本质层_超导几何本质公式量纲数值与来源三重审计_"
        "临界温度自洽崩坏与Spearman证伪_精算与可视化_2026-10-30.py")
PY = r"C:\Users\mo\.workbuddy\binaries\python\versions\3.13.12\python.exe"
OUT = os.path.join(SRC, "_out_r245.txt")

p = subprocess.run([PY, os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)
