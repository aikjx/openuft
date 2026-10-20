# -*- coding: utf-8 -*-
"""ASCII runner for r120 engine (Chinese-path argv workaround)."""
import runpy
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/"
          "源码/TUFT-r120_所有力大统一方程式_候选全集与状态机判_2026-10-20.py")

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
