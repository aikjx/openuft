# -*- coding: utf-8 -*-
"""ASCII runner for r114 engine (Chinese-path argv workaround)."""
import runpy
import sys

TARGET = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r114_引力本源宣称_G几何本源四版本机审_螺旋机制普遍性审计_攻破_2026-10-19.py"

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
