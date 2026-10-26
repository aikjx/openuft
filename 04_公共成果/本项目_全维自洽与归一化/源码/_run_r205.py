# -*- coding: utf-8 -*-
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r205_\u7edf\u4e00\u6027\u5f52\u56e0\u5ba1\u8ba1_\u65d7\u8230\u7edf\u4e00\u6570\u5b57\u7684MSSM\u5916\u90e8\u6027\u4e0ev\u53cc\u53e3\u5f84\u52d8\u8bef_\u7cbe\u7b97_2026-10-26.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
