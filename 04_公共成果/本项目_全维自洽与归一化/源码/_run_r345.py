# -*- coding: utf-8 -*-
"""ASCII runner：避免中文 argv / 源码路径进 argv 的 GBK 问题，用 runpy 加载 r345 引擎。"""
import sys
import os
import runpy

SRC_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
ENGINE = os.path.join(SRC_DIR, "TUFT-r345_企业级统一验收与回归门禁_撞号防御与单门禁真相源与全卷CI式回归_2026-11-01.py")

if not os.path.isfile(ENGINE):
    raise SystemExit("ENGINE 缺失: %s" % ENGINE)

sys.path.insert(0, SRC_DIR)
runpy.run_path(ENGINE, run_name="__main__")
