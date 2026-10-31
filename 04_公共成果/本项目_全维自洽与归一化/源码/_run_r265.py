# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r265_引力波预言层_标准模型弱一阶误判与相变参数全缺_"
        "LISA可探测边界与谱畸变零判别力_精算与可视化_2026-10-31.py")
path = os.path.join(HERE, NAME)
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
