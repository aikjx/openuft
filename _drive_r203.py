# -*- coding: utf-8 -*-
"""driver：以 ASCII runner 启动 r203 引擎（中文路径禁入 argv 的 workaround）。"""
import runpy
import sys

RUNNER = (r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
          r"\源码\_run_r203.py")
runpy.run_path(RUNNER, run_name="__main__")
sys.exit(0)
