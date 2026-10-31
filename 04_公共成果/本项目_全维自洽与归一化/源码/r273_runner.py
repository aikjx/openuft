# -*- coding: utf-8 -*-
"""ASCII runner for the TUFT-r273 engine (avoids Chinese-in-argv)."""
import runpy
import os

ENGINE = (r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/"
          r"源码/TUFT-r273_四力本源参数精算层_统一势模板标准耦合重标定及qWqπ数值核验_"
          r"精算与可视化_2026-10-31.py")

if not os.path.exists(ENGINE):
    raise SystemExit("engine not found: " + ENGINE)

runpy.run_path(ENGINE, run_name="__main__")
