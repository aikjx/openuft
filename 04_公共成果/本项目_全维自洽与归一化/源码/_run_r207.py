# -*- coding: utf-8 -*-
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r207_\u7edf\u4e00\u573a\u65b9\u7a0b_\u4e3b\u65b9\u7a0b\u7ed3\u6784\u540d\u5b9e\u5ba1\u8ba1_\u66f2\u7387\u5206\u5757\u6bd4\u5b89\u57fa\u4e0e\u6811\u7ea7\u5173\u7cfb\u53ca\u53cd\u5e38\u4ea4\u53c9\u6838_2026-10-26.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
