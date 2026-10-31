# -*- coding: utf-8 -*-
"""r259 runner（复现入口；生成于引擎定稿后补建——引擎已 rc=0 定稿，见 _out_r259.txt）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r259_同一运动动力学层_辐射与自旋自旋的c幂阶梯定理_"
        "拉莫尔与四极与21cm超精细现算_Darwin首阶与二十四格穷举_"
        "精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r259.txt")

p = subprocess.run([PY, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)
