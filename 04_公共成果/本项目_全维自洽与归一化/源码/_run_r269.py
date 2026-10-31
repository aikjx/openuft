# -*- coding: utf-8 -*-
"""r269 runner（复现入口；预修已内联完成）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r269_候选比例多元性定理_tanθ与sinθ候选互斥_"
        "κ除τ推导机检与550nm四位复现与玻尔圆轨道τ等于零反例_六候选穷举_"
        "精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r269.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-3200:])
print("RC=", p.returncode)
