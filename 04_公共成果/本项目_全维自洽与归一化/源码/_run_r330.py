# -*- coding: utf-8 -*-
"""r330 runner —— 口径审计 · 六自由电荷 vs 反常自由一维超荷（N 自由的真实性）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r330_口径审计_六自由电荷vs反常自由一维与N自由的真实性_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r330.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-8000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
