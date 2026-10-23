# -*- coding: utf-8 -*-
# ASCII-only runner（规避中文路径入 argv 的 GBK 误码问题）
import os
import sys
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(
    HERE,
    "TUFT-r157_D5大统一力方程闭合_梯度磁场洛伦兹积分与恒等式全域判据_2026-10-23.py",
)
sys.argv = [TARGET]
runpy.run_path(TARGET, run_name="__main__")
