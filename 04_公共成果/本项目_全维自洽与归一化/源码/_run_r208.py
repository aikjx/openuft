# -*- coding: utf-8 -*-
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r208_\u53ef\u8bc1\u4f2a\u6027\u5ba1\u8ba1_\u5224\u522b\u529b\u56db\u5224\u636e\u4e0e\u6846\u67b6\u72ec\u6709\u9884\u8a00\u8ba1\u6570no-go_\u7cbe\u7b97_2026-10-26.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
