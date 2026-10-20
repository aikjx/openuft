# -*- coding: utf-8 -*-
# ASCII runner for r126（规避中文路径 GBK 参数损坏）
# 写死 TARGET 绝对路径，sys.argv=[TARGET] 后 run_path 转发执行；逻辑零改动。
import os
import sys
import runpy

SRC = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/TUFT-r126_超宇宙与宇宙图景宣称_精算攻破与恒等式审计_2026-10-20.py"

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

sys.argv = [SRC]
runpy.run_path(SRC, run_name="__main__")
