# -*- coding: utf-8 -*-
"""r258 runner：中文路径不进 argv，直接 exec 引擎。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r258_暗能量与宇宙常数层_Lambda即挠率改名与零点能灾难未绕开_"
        "三候选跨121量级与w-1定义恒等式_精算与可视化_2026-10-31.py")
path = os.path.join(HERE, NAME)
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
