#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""runner for TUFT-r129（中文路径禁入 argv ⇒ runpy 定位）"""
import runpy
import sys

TARGET = ("D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/"
          "源码/TUFT-r129_微观粒子与宏观星体第一性原理导出_判据建立与现状定价_2026-10-20.py")

if __name__ == "__main__":
    rc = runpy.run_path(TARGET, run_name="__main__")
    sys.exit(0)
