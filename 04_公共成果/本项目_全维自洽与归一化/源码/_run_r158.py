# -*- coding: utf-8 -*-
# ASCII-only runner（规避中文路径入 argv 的 GBK 误码问题）
import os
import sys
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r158_D5字典层_回旋频率同一性与退化点失效_2026-10-24.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
