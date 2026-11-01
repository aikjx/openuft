# -*- coding: utf-8 -*-
"""本线程 r340 专用 runner（唯一命名，避免与并行册共用 `_run_r340.py` 被覆盖）。

背景：并行会话也拥有一份 r340（攻 X-R336-1），并写到了同名 `_run_r340.py` 上，
      覆盖了本线程的 runner（2026-11-01 实测）。故本线程改用**区别化文件名**
      `_run_r340_alpha.py`，指向本线程的 alpha 第一性预言卷。
"""
import sys
import os
import runpy

SRC_DIR = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码"
ENGINE = os.path.join(SRC_DIR, "TUFT-r340_alpha第一性预言完备机制分类与RGE链自由度显式计算_X-R311-4攻坚与最终no-go收敛_2026-11-01.py")

if not os.path.isfile(ENGINE):
    raise SystemExit("ENGINE 缺失: %s" % ENGINE)

sys.path.insert(0, SRC_DIR)
runpy.run_path(ENGINE, run_name="__main__")
