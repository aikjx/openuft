# -*- coding: utf-8 -*-
"""r261 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r261_全维分析审计_alpha等于玻尔速度比与螺旋映射_"
        "数字复现与标准螺旋恒等式对拍与本源恒等式自动满足_双运动区分定理_"
        "精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r261.txt")

p = subprocess.run([PY, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)
