# -*- coding: utf-8 -*-
"""r291 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r291_V11V12双靶合并审计_本源关系与耦合消失定理与KK质量矛盾_"
        "七线合流终形_精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r291.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4800:])
print("RC=", p.returncode)
