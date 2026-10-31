# -*- coding: utf-8 -*-
"""r275 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r275_全链路自洽审计_六层链路状态总账_"
        "缪子氢Uehling真空极化数值积分与预测盈余账本_"
        "精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r275.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4200:])
print("RC=", p.returncode)
