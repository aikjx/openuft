# -*- coding: utf-8 -*-
"""r301 runner（复现入口）—— 非阿贝尔电弱型最小带电内容搜索（攻 X-R300-1）
【2026-11-01 由 r312 线恢复：本线早期草稿曾误以 r301 落盘并覆盖/删除本 runner，
现按其 README 登记的「_run_r301.py → _out_r301.txt」逐字恢复入口，未改其引擎字节。】"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r301_非阿贝尔电弱型最小带电内容搜索_SU2xU1反常条件与Witten奇偶与chiral判据"
        "_X-R300-1攻坚_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r301.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)
