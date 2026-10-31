# -*- coding: utf-8 -*-
"""r283 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r283_V10选择机制审计_拓扑闭合环面结四次能量条件级数_"
        "全库总结_精算与可视化_2026-10-31.py")
OUT = os.path.join(SRC, "_out_r283.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4600:])
print("RC=", p.returncode)
