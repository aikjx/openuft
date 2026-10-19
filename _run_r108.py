# -*- coding: utf-8 -*-
# ASCII runner for r108 (avoid GBK argv corruption on Chinese paths)
import os
import runpy
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
NORM = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(NORM, "源码",
                   "TUFT-r108_TUFT-V10外部来料_主干全维攻破_量纲场方程与现象学机检_2026-10-19.py")

if not os.path.isfile(SRC):
    sys.stderr.write("SRC NOT FOUND: %s\n" % SRC)
    sys.exit(3)

runpy.run_path(SRC, run_name="__main__")
