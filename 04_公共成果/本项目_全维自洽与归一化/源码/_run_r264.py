# -*- coding: utf-8 -*-
# ASCII runner：中文路径只出现在脚本内部，不进 shell argv
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r264_自由参数总账层_ω赋值与单位依赖及四态分类与八粒子字典表自洽崩坏"
        "_精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r264.txt")

p = subprocess.run([PY, os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-14000:])
print("RC=", p.returncode)
