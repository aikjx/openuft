# -*- coding: utf-8 -*-
r"""ASCII runner for _probe_r251.py"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
path = os.path.join(HERE, "_probe_r251.py")
src = io.open(path, "r", encoding="utf-8").read()
g = {"__name__": "__main__", "__file__": path}
try:
    exec(compile(src, path, "exec"), g)
except SystemExit:
    pass
