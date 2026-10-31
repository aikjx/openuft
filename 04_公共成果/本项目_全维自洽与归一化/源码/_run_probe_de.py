# -*- coding: utf-8 -*-
"""ASCII runner: 中文路径禁入 argv，源码内 raw 路径。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "_probe_r256.py"
path = os.path.join(HERE, NAME)
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit as e:
    sys.exit(e.code)
