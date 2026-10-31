# -*- coding: utf-8 -*-
"""r278 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r278_四力统一方程_宇宙学距离与观测量层_共动角径光度距离与年龄声视界互印_"
        "精算与交互可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r278.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4200:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
