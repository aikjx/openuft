# -*- coding: utf-8 -*-
r"""ASCII runner for TUFT-r250（中文路径禁入 argv）"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r250_耦合常数跑动与能标层_RG自相矛盾与alpha星定义恒等式_"
        "大统一固定点证伪_精算与可视化_2026-10-30.py")
path = os.path.join(HERE, NAME)
sys.path.insert(0, HERE)
src = io.open(path, "r", encoding="utf-8").read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
