# -*- coding: utf-8 -*-
"""r277 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r277_常数本源普查_量纲代数三分类与无量纲约化K等于5_"
        "单位重标定不变性机器演示_精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r277.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4200:])
print("RC=", p.returncode)
