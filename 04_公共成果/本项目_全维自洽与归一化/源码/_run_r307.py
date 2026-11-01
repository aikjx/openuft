# -*- coding: utf-8 -*-
"""r307 runner（复现入口）—— 常数截面计数的第一原理审计

注：本卷原定 r306，因并行会话先占 r306（GMFRE 卷）而改号 r307；
`_run_r306.py` 属并行会话，**未触碰**。
"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r307_常数截面计数的第一原理审计_"
        "Schur标量性与复制不可约化与Kmin等于N_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r307.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
