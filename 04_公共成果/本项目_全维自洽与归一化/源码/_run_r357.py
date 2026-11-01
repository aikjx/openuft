# -*- coding: utf-8 -*-
"""r357 runner：中文路径不进 argv ⇒ 源码内硬编码 raw 路径，runpy 加载引擎。"""
import sys
import os
import runpy

SRC_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
ENGINE = os.path.join(SRC_DIR, "TUFT-r357_引力渐近安全路线可计算裁决_不动点分支与刚性刻画_X-R311-4攻坚Ⅱ_2026-11-02.py")

if not os.path.isfile(ENGINE):
    raise SystemExit("ENGINE 缺失: %s" % ENGINE)

sys.path.insert(0, SRC_DIR)
runpy.run_path(ENGINE, run_name="__main__")
