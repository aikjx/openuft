# -*- coding: utf-8 -*-
"""r344 runner（复现入口）—— 质量式锚口径溯源：玻尔锚 α² 结构定理"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r344_质量式锚口径溯源_玻尔锚alpha平方结构定理与双alpha双重计数_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r344.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
