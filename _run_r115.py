# -*- coding: utf-8 -*-
"""ASCII runner for r115 engine (Chinese-path argv workaround)."""
import runpy
import sys

TARGET = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r115_引力本质与引力波几何本源语料_求导验证版审计_攻破_2026-10-20.py"

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
