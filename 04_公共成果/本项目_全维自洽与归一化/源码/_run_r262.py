# -*- coding: utf-8 -*-
"""r262 runner：中文路径不进 argv，直接 exec 引擎。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r262_重子不对称层_选择定则写反与eps到eta链条断裂_"
        "唯一独有预言零数值与Frenet-PMNS范畴错置_精算与可视化_2026-10-31.py")
path = os.path.join(HERE, NAME)
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
