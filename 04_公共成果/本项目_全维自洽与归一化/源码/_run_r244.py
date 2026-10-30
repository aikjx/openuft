# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r244_引力本质层_曲线曲率与时空曲率范畴错置_"
        "引力方向地基缺失与kappa读法二难_精算与可视化_2026-10-30.py")
PY = r"C:\Users\mo\.workbuddy\binaries\python\versions\3.13.12\python.exe"
OUT = os.path.join(SRC, "_out_r244.txt")

p = subprocess.run([PY, os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)
