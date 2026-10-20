# -*- coding: utf-8 -*-
# ASCII runner for UFT-70（规避中文路径 GBK 参数损坏）
import os
import sys
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/07_统一场方程/70_qcd_running_calc.py"

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

try:
    runpy.run_path(SRC, run_name="__main__")
except SystemExit as exc:
    sys.exit(exc.code if isinstance(exc.code, int) else 0)
