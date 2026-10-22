# -*- coding: utf-8 -*-
"""UTF-8 安全 runner：中文路径禁入 argv，改用 runpy.run_path。"""
import runpy, os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "TUFT-r149_垂直原理与力的本源_公设层攻破与判别性定价_2026-10-22.py")
runpy.run_path(TARGET, run_name="__main__")
