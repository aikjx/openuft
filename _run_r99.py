# -*- coding: utf-8 -*-
"""ASCII runner: avoid Chinese path in argv (GBK mojibake workaround)."""
import runpy
import sys

TARGET = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r99_力公式体系压缩版与统一场论方程_机器审计_2026-10-18.py"

if __name__ == "__main__":
    sys.argv = [TARGET]
    runpy.run_path(TARGET, run_name="__main__")
