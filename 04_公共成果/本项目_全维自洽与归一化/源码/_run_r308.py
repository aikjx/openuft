# -*- coding: utf-8 -*-
"""r308 runner（复现入口）—— ROOT V22 固定点非唯一性与尺度嬗变与轻子真空极化来料审计"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r308_ROOTV22固定点非唯一性与尺度嬗变与轻子真空极化_UV临界面自由度账本_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r308.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
