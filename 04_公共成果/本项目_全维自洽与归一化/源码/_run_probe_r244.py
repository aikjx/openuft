# -*- coding: utf-8 -*-
r"""ASCII runner: 调用 _probe_r244_meta.py（中文路径禁入 argv）"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

path = os.path.join(HERE, "_probe_r244_meta.py")
src = io.open(path, "r", encoding="utf-8").read()
code = compile(src, path, "exec")
g = {"__name__": "__main__", "__file__": path}
try:
    exec(code, g)
except SystemExit:
    pass
