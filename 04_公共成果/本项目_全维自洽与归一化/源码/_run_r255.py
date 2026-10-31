# -*- coding: utf-8 -*-
r"""ASCII runner for TUFT-r255（中文路径禁入 argv）"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r255_磁矩与量子修正层_裸涡旋因子2与两圈闭式符号反_"
        "dageo超窗96672倍与alpha口径二难_精算与可视化_2026-10-31.py")
path = os.path.join(HERE, NAME)
sys.path.insert(0, HERE)
src = io.open(path, "r", encoding="utf-8").read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
