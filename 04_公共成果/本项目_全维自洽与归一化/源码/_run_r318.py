# -*- coding: utf-8 -*-
"""r318 runner（复现入口）—— X-R301-1 攻防 · 合法几何源与三代可实现性"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r318_XR301攻防_合法几何源与三代可实现性_Ngen自由与不可预测性_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r318.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
