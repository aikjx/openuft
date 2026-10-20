# -*- coding: utf-8 -*-
# ASCII runner for r128（规避中文路径 GBK 参数损坏）
import os
import sys
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r128_正确理论体系方程全集_整理与攻破审计_2026-10-20.py"

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

try:
    runpy.run_path(SRC, run_name="__main__")
except SystemExit as exc:
    sys.exit(exc.code if isinstance(exc.code, int) else 0)
