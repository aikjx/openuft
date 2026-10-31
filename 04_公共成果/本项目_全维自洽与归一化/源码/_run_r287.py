# -*- coding: utf-8 -*-
"""r287 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r287_精细结构常数V10下一步链条可行性审计_形状量标度不变与α跑动否证_"
        "参数自由度计数与刚性定理不可借用_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r287.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4400:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
