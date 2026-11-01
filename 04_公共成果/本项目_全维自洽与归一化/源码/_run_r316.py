# -*- coding: utf-8 -*-
"""r316 runner（复现入口）—— 1/3 电荷子格最小带电内容搜索（X-R301-6 攻坚）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r316_三分之一电荷子格最小带电内容搜索_SM电荷结构强制性与BZ相容性与两圈口径联网核对_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r316.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
