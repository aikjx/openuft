# -*- coding: utf-8 -*-
"""ASCII runner：用 runpy 定位中文名引擎，规避「中文路径入 argv」的 GBK 误码。"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE, "TUFT-r171_常数kPrime量纲最终裁定_九重量纲与公式数值脱钩_精算_2026-10-24.py")

if not os.path.isfile(TARGET):
    sys.stderr.write("TARGET NOT FOUND: %s\n" % TARGET)
    sys.exit(3)

try:
    runpy.run_path(TARGET, run_name="__main__")
    rc = 0
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else 0
sys.exit(rc)
