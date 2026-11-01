# -*- coding: utf-8 -*-
"""r299 runner（复现入口）—— ROOT V15 六维磁通稳定化全链路审计（原 r298 后到卷，碰撞治理整体改号 r299）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r299_ROOTV15六维磁通稳定化全链路审计_势平方形式与sqrt3势垒与体积模正则化与"
        "sqrt8pi口径混用与xi自由参数终局_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r299.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
