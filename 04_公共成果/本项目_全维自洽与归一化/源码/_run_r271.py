# -*- coding: utf-8 -*-
"""r271 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r271_时空曲率比攻坚_K1除K2等于beta洛伦兹不变_"
        "时空不变量复现与2000组boost机检与三维候选剪枝定理_"
        "精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r271.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-3600:])
print("RC=", p.returncode)
