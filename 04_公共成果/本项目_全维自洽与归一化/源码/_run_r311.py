# -*- coding: utf-8 -*-
"""r311 runner（复现入口）—— 无自由边界值耦合选择机制普查（X-R304-2 攻坚）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r311_无自由边界值耦合选择机制普查_BanksZaks红外固定点与SU5归一化刚性与自由度守恒记账_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r311.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
