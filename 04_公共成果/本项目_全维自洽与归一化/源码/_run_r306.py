# -*- coding: utf-8 -*-
"""r306 runner（复现入口）—— 磁通手征谱混合源可实现方程 GMFRE（攻 X-R296-2）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r306_磁通手征谱混合源可实现方程GMFRE_Smith标准形推广与多源整除性松动诚实边界_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r306.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
