# -*- coding: utf-8 -*-
# ASCII runner for r127（规避中文路径 GBK 参数损坏）
import os
import sys
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r127_整理正确核与攻破正确理论_SMGR断裂边界精算_2026-10-20.py"

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

sys.argv = [SRC]
runpy.run_path(SRC, run_name="__main__")
