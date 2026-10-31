# -*- coding: utf-8 -*-
"""r284 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r284_精细结构常数V10选择机制审计_螺旋闭合环面结四次能量"
        "条件级数与单极KK_全维可攻破性机检_精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r284.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4400:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
