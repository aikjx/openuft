# -*- coding: utf-8 -*-
# ASCII-only runner（规避中文路径入 argv 的 GBK 误码问题）
import os
import sys
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r152_ωfhcf完整关系组定标代价与超光速判决_2026-10-22.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
