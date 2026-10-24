# -*- coding: utf-8 -*-
"""ASCII-only runner：规避中文路径进 argv 的 GBK 误码。"""
import os
import runpy
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r165_D5四力闭合层_单粒子运动学量与源依赖冲突_2026-10-24.py")

if __name__ == "__main__":
    runpy.run_path(TARGET, run_name="__main__")
