# -*- coding: utf-8 -*-
r"""ASCII runner for TUFT-r247（中文路径禁入 argv）"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ("TUFT-r247_引力本质层元审计_r244判据回溯与加固_"
        "G导出链循环与kappa_P定标二难_精算与可视化_2026-10-30.py")
path = os.path.join(HERE, NAME)
sys.path.insert(0, HERE)
src = io.open(path, "r", encoding="utf-8").read()
code = compile(src, path, "exec")
g = {"__name__": "__main__", "__file__": path}
try:
    exec(code, g)
except SystemExit as e:
    sys.exit(e.code)
