# -*- coding: utf-8 -*-
"""ASCII runner：中文路径禁入 argv，故在脚本内以 raw 名字打开。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r267_统一场论完成度终局验收层_账面不可加与独有预言归零_"
        "参数经济性与跨卷口径分歧_十四层矩阵与三出口判决_精算与可视化_2026-10-31.py")
path = os.path.join(HERE, NAME)
src = open(path, "r", encoding="utf-8").read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
