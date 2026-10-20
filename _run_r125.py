# -*- coding: utf-8 -*-
# ASCII runner for r125（规避中文路径 GBK 参数损坏）
import os
import sys
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r125_路线对错判定方法与统一路线假设穷尽审计_2026-10-20.py"

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

sys.argv = [SRC]
runpy.run_path(SRC, run_name="__main__")
