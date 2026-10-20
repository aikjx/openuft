#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""runner for TUFT-r130（中文路径禁入 argv ⇒ runpy 定位）"""
import runpy
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/"
          "源码/TUFT-r130_攻破推导链_正确理论体系与方程的隐藏前提审计_2026-10-20.py")

if __name__ == "__main__":
    runpy.run_path(TARGET, run_name="__main__")
    sys.exit(0)
