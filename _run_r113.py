# -*- coding: utf-8 -*-
# ASCII runner for r113 (avoid GBK argv corruption on Chinese paths)
import os
import runpy
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(NORM, "源码",
                   "TUFT-r113_力的统一宣称_四分支源侧结构审计_电磁支归零_飞碟动力学攻破_2026-10-19.py")

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

runpy.run_path(SRC, run_name="__main__")
