# -*- coding: utf-8 -*-
"""r182 ASCII runner: avoid passing CJK paths through argv (GBK)."""
import runpy
import sys

P = (r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
     r"\TUFT-r182_引力场定义方程A_螺旋加速度两分支与G四口径脱钩_精算_2026-10-25.py")

sys.argv = [P]
try:
    runpy.run_path(P, run_name="__main__")
except SystemExit as ex:
    sys.exit(ex.code)
